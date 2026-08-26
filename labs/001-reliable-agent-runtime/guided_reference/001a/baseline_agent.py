"""001A reference: 一个故意很小、但分层清晰的 tool-using agent harness。

本文件不使用 LangChain / LangGraph。
不是因为这些框架不好，而是为了把它们通常隐藏的边界直接暴露出来：

    user input
        -> model decision
        -> tool lookup
        -> argument validation
        -> tool execution
        -> tool result
        -> model final answer

真正的生产系统会复杂很多，但 eval / tracing / failure analysis 都建立在这些边界上。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import perf_counter
from typing import Any, Callable
from uuid import uuid4


# ---------------------------------------------------------------------------
# 1. Contracts
# ---------------------------------------------------------------------------


class DecisionType(str, Enum):
    """模型本轮输出的类型。

    Agent harness 最重要的职责之一，就是把“模型文本输出”变成明确状态。
    当前只有两种：最终回答，或者请求调用工具。
    """

    FINAL = "final"
    TOOL_CALL = "tool_call"


class RunStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class ModelDecision:
    """模型输出经过解析后的结构化表示。"""

    kind: DecisionType
    text: str | None = None
    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolSpec:
    """描述一个可被 Agent 使用的 capability。

    handler 是真实业务函数；required_args 是非常简化的 schema。
    后续课程会替换成更严格的 JSON Schema / typed validation。
    """

    name: str
    required_args: tuple[str, ...]
    handler: Callable[..., dict[str, Any]]


@dataclass
class TraceEvent:
    """一条可观测事件。

    现在先用 list[TraceEvent] 保存在内存里。
    后面会映射到真正的 span/event/metric。
    """

    run_id: str
    step: int
    event: str
    details: dict[str, Any]
    duration_ms: float | None = None


@dataclass
class RunResult:
    run_id: str
    status: RunStatus
    answer: str | None
    trace: list[TraceEvent]
    error_type: str | None = None
    error_message: str | None = None


# ---------------------------------------------------------------------------
# 2. Mock business tools
# ---------------------------------------------------------------------------


TICKETS: dict[str, dict[str, str]] = {
    "T-1001": {"status": "open", "title": "Cannot login"},
    "T-1002": {"status": "open", "title": "Payment failed"},
}


def get_ticket(ticket_id: str) -> dict[str, Any]:
    """读取工单。

    这里故意让 T-5000 模拟下游服务故障，供 eval/fault analysis 使用。
    """

    if ticket_id == "T-5000":
        raise RuntimeError("ticket backend unavailable")

    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return {"found": False, "ticket_id": ticket_id}

    return {"found": True, "ticket_id": ticket_id, **ticket}


def close_ticket(ticket_id: str, reason: str) -> dict[str, Any]:
    """关闭工单。

    注意：这已经是 side effect。
    当前 baseline 故意没有 approval / idempotency；后续我们会用测试证明它为什么危险。
    """

    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return {"closed": False, "reason": "not_found", "ticket_id": ticket_id}

    ticket["status"] = "closed"
    return {"closed": True, "ticket_id": ticket_id, "reason": reason}


TOOL_REGISTRY: dict[str, ToolSpec] = {
    "get_ticket": ToolSpec("get_ticket", ("ticket_id",), get_ticket),
    "close_ticket": ToolSpec("close_ticket", ("ticket_id", "reason"), close_ticket),
}


# ---------------------------------------------------------------------------
# 3. A deterministic fake model
# ---------------------------------------------------------------------------


class ScriptedModel:
    """一个 deterministic model double。

    为什么第一课先不用真实 LLM？

    因为我们现在学的是 eval harness 和 failure attribution。
    如果一开始就混入随机模型输出，很难判断测试失败到底来自模型随机性还是 harness。

    后面只要保持 decide() 这个边界，就可以换成真实模型 adapter。
    """

    def decide(self, user_text: str, tool_result: dict[str, Any] | None) -> ModelDecision:
        # 工具执行过后，模型生成最终回答。
        if tool_result is not None:
            return ModelDecision(
                kind=DecisionType.FINAL,
                text=f"Tool result: {tool_result}",
            )

        text = user_text.lower()

        # 正常读取场景。
        if "status" in text and "t-1001" in text:
            return ModelDecision(
                kind=DecisionType.TOOL_CALL,
                tool_name="get_ticket",
                arguments={"ticket_id": "T-1001"},
            )

        # 下游故障场景。
        if "status" in text and "t-5000" in text:
            return ModelDecision(
                kind=DecisionType.TOOL_CALL,
                tool_name="get_ticket",
                arguments={"ticket_id": "T-5000"},
            )

        # 正常关闭场景。
        if "close" in text and "t-1001" in text:
            return ModelDecision(
                kind=DecisionType.TOOL_CALL,
                tool_name="close_ticket",
                arguments={"ticket_id": "T-1001", "reason": "resolved"},
            )

        # 故意制造“模型选错 tool”的 failure。
        # 这是为了让 eval 能区分 model failure 和 tool failure。
        if "delete" in text:
            return ModelDecision(
                kind=DecisionType.TOOL_CALL,
                tool_name="delete_ticket",
                arguments={"ticket_id": "T-1001"},
            )

        # 故意制造“模型参数缺失”的 failure。
        if "close" in text and "t-1002" in text:
            return ModelDecision(
                kind=DecisionType.TOOL_CALL,
                tool_name="close_ticket",
                arguments={"ticket_id": "T-1002"},  # missing reason
            )

        return ModelDecision(
            kind=DecisionType.FINAL,
            text="I cannot determine the requested action.",
        )


# ---------------------------------------------------------------------------
# 4. Harness
# ---------------------------------------------------------------------------


class AgentRunner:
    """最小 agent execution harness。

    重点不是这段代码有多高级，而是你要能指出每一个 execution boundary：

    - model boundary
    - tool registry boundary
    - validation boundary
    - tool execution boundary
    - trace boundary

    之后 retry、approval、idempotency、sandbox、durability 都会插入这些边界。
    """

    def __init__(self, model: ScriptedModel) -> None:
        self.model = model

    def run(self, user_text: str) -> RunResult:
        run_id = str(uuid4())
        trace: list[TraceEvent] = []
        tool_result: dict[str, Any] | None = None

        # 当前最多两轮：第一次模型决定是否调用工具；第二次模型生成最终答案。
        for step in range(1, 3):
            model_started = perf_counter()
            decision = self.model.decide(user_text, tool_result)
            trace.append(
                TraceEvent(
                    run_id=run_id,
                    step=step,
                    event="model_decision",
                    details={
                        "kind": decision.kind.value,
                        "tool_name": decision.tool_name,
                        "arguments": decision.arguments,
                    },
                    duration_ms=(perf_counter() - model_started) * 1000,
                )
            )

            if decision.kind == DecisionType.FINAL:
                return RunResult(
                    run_id=run_id,
                    status=RunStatus.SUCCESS,
                    answer=decision.text,
                    trace=trace,
                )

            # ---- Tool registry boundary ----
            # 模型“想调用”某个工具，不代表 runtime 就允许它执行。
            spec = TOOL_REGISTRY.get(decision.tool_name or "")
            if spec is None:
                trace.append(
                    TraceEvent(
                        run_id=run_id,
                        step=step,
                        event="tool_rejected",
                        details={"reason": "unknown_tool", "tool_name": decision.tool_name},
                    )
                )
                return RunResult(
                    run_id=run_id,
                    status=RunStatus.FAILED,
                    answer=None,
                    trace=trace,
                    error_type="unknown_tool",
                    error_message=f"unknown tool: {decision.tool_name}",
                )

            # ---- Validation boundary ----
            # 先检查 required args，再进入业务函数。
            # 生产中应该使用严格 schema，而不是这段简化逻辑。
            missing = [
                arg
                for arg in spec.required_args
                if arg not in decision.arguments or decision.arguments[arg] in (None, "")
            ]
            if missing:
                trace.append(
                    TraceEvent(
                        run_id=run_id,
                        step=step,
                        event="tool_rejected",
                        details={
                            "reason": "validation_error",
                            "tool_name": spec.name,
                            "missing": missing,
                        },
                    )
                )
                return RunResult(
                    run_id=run_id,
                    status=RunStatus.FAILED,
                    answer=None,
                    trace=trace,
                    error_type="validation_error",
                    error_message=f"missing required args: {missing}",
                )

            # ---- Tool execution boundary ----
            tool_started = perf_counter()
            try:
                tool_result = spec.handler(**decision.arguments)
            except Exception as exc:  # baseline 故意粗糙，后续课程会拆 error semantics。
                trace.append(
                    TraceEvent(
                        run_id=run_id,
                        step=step,
                        event="tool_failed",
                        details={"tool_name": spec.name, "exception": type(exc).__name__},
                        duration_ms=(perf_counter() - tool_started) * 1000,
                    )
                )
                return RunResult(
                    run_id=run_id,
                    status=RunStatus.FAILED,
                    answer=None,
                    trace=trace,
                    error_type="tool_error",
                    error_message=str(exc),
                )

            trace.append(
                TraceEvent(
                    run_id=run_id,
                    step=step,
                    event="tool_succeeded",
                    details={"tool_name": spec.name, "result": tool_result},
                    duration_ms=(perf_counter() - tool_started) * 1000,
                )
            )

        # 理论上当前 scripted model 不会走到这里。
        # 仍然明确处理它，是为了让 runtime 的终止条件可观察。
        return RunResult(
            run_id=run_id,
            status=RunStatus.FAILED,
            answer=None,
            trace=trace,
            error_type="step_limit",
            error_message="agent exceeded max steps",
        )
