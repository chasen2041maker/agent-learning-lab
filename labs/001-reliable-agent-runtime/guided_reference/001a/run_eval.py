"""运行 001A baseline eval。

执行：
    python run_eval.py

第一版 evaluator 故意非常朴素：
- 检查 run status；
- 检查 error_type；
- 检查期望的 tool 是否真正进入 execution boundary。

这正是本课要理解的重点：eval 不一定一上来就需要 LLM-as-judge。
能 deterministic 判断的东西，优先 deterministic 判断。
"""

from __future__ import annotations

from dataclasses import dataclass

from baseline_agent import AgentRunner, RunResult, RunStatus, ScriptedModel, TICKETS


@dataclass(frozen=True)
class EvalCase:
    name: str
    prompt: str
    expected_status: RunStatus
    expected_tool: str | None = None
    expected_error_type: str | None = None


CASES = [
    EvalCase(
        name="read_known_ticket",
        prompt="What is the status of T-1001?",
        expected_status=RunStatus.SUCCESS,
        expected_tool="get_ticket",
    ),
    # 这个 case 故意失败：用户给了一个合法 ticket id，但 scripted model
    # 只认识 T-1001 / T-5000，没有泛化到 T-9999。
    # Runtime 自己会返回 SUCCESS，但 task-level evaluator 应该判失败。
    EvalCase(
        name="read_unseen_ticket_id",
        prompt="What is the status of T-9999?",
        expected_status=RunStatus.SUCCESS,
        expected_tool="get_ticket",
    ),
    # 这里失败是我们预期的系统行为：tool backend 本身故障。
    EvalCase(
        name="tool_backend_failure",
        prompt="What is the status of T-5000?",
        expected_status=RunStatus.FAILED,
        expected_tool="get_ticket",
        expected_error_type="tool_error",
    ),
    # 模型请求了 registry 不存在的 tool；harness 应该拒绝。
    EvalCase(
        name="unknown_tool_rejected",
        prompt="Delete T-1001",
        expected_status=RunStatus.FAILED,
        expected_error_type="unknown_tool",
    ),
    # 这个 case 故意失败：model 忘了提供 close_ticket 的 reason。
    EvalCase(
        name="close_ticket_missing_argument",
        prompt="Close T-1002",
        expected_status=RunStatus.SUCCESS,
        expected_tool="close_ticket",
    ),
    EvalCase(
        name="close_ticket_happy_path",
        prompt="Close T-1001",
        expected_status=RunStatus.SUCCESS,
        expected_tool="close_ticket",
    ),
]


def attempted_tools(result: RunResult) -> list[str]:
    """从 trace 提取真正进入 tool handler execution boundary 的工具。

    `tool_succeeded` 和 `tool_failed` 都算 attempted，因为 backend 抛错并不代表
    Agent 没有正确选择/调用这个 tool。

    `tool_rejected` 不算 attempted：unknown tool 或 validation error 在真正业务函数
    执行前就被 runtime 拦住了。

    这看似只是命名，实际上体现了 eval metric 必须有精确定义。
    """

    tools: list[str] = []
    for event in result.trace:
        if event.event in {"tool_succeeded", "tool_failed"}:
            name = event.details.get("tool_name")
            if isinstance(name, str):
                tools.append(name)
    return tools


def grade(case: EvalCase, result: RunResult) -> tuple[bool, list[str]]:
    """返回 case 是否通过，以及未通过的 deterministic reasons。"""

    reasons: list[str] = []

    if result.status != case.expected_status:
        reasons.append(
            f"status expected={case.expected_status.value} actual={result.status.value}"
        )

    if case.expected_error_type != result.error_type:
        # expected_error_type=None 时也校验，避免“表面 success 但偷偷带 error”。
        reasons.append(
            f"error_type expected={case.expected_error_type} actual={result.error_type}"
        )

    if case.expected_tool is not None and case.expected_tool not in attempted_tools(result):
        reasons.append(
            f"expected tool {case.expected_tool!r} never entered execution boundary"
        )

    return not reasons, reasons


def reset_state() -> None:
    """每个 eval case 开始前恢复共享 mock state。

    如果不 reset，close_ticket 会污染后面的 case。
    这是 eval reproducibility 的一个最小例子。
    """

    TICKETS["T-1001"]["status"] = "open"
    TICKETS["T-1002"]["status"] = "open"


def main() -> None:
    runner = AgentRunner(ScriptedModel())
    passed = 0

    print("=== Agent Eval Baseline ===")

    for case in CASES:
        reset_state()
        result = runner.run(case.prompt)
        ok, reasons = grade(case, result)
        passed += int(ok)

        print(f"\n[{'PASS' if ok else 'FAIL'}] {case.name}")
        print(f"  run_id: {result.run_id}")
        print(f"  runtime status: {result.status.value}")
        print(f"  error_type: {result.error_type}")
        print(f"  attempted_tools: {attempted_tools(result)}")

        for reason in reasons:
            print(f"  grader: {reason}")

        # 先直接打印 trace。后续会把它升级成更适合分析的结构化 trace。
        for event in result.trace:
            print(
                f"    step={event.step} event={event.event} "
                f"duration_ms={event.duration_ms} details={event.details}"
            )

    total = len(CASES)
    print("\n=== Summary ===")
    print(f"passed: {passed}/{total}")
    print(f"pass_rate: {passed / total:.2%}")


if __name__ == "__main__":
    main()
