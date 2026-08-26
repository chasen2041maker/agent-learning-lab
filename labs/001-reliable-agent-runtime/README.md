# Lab 001 — Reliable Agent Runtime

## Why this lab exists

很多 Agent demo 的核心只有：

```text
LLM decides tool → call function → append result → call LLM again
```

这在 demo 中可以工作，但一进入生产就会遇到：

- tool 超时；
- 网络在成功之后断开；
- 同一个 side effect 被执行两次；
- 参数合法但业务上危险；
- Agent 无限循环；
- tool 返回巨大结果撑爆 context；
- 进程在第 7 个 step 崩溃；
- 用户批准的是旧参数，但 Agent 后来改了参数；
- 最终只看到“agent failed”，不知道哪一步出了问题。

本实验的目标是：**不依赖 Agent framework，自己建立一个最小、可解释、可测试的 Agent runtime。**

框架以后再接。先知道框架究竟应该替我们解决什么。

---

# Final Architecture

最终逐步演进到：

```text
User Request
    │
    ▼
Run Controller
    │
    ├── budget / max_steps / cancellation
    │
    ▼
Model Adapter
    │
    ├── final answer ───────────────► DONE
    │
    └── tool call
            │
            ▼
      Tool Execution Boundary
            │
            ├── schema validation
            ├── authorization
            ├── risk classification
            ├── approval
            ├── idempotency
            ├── timeout
            ├── retry
            └── trace
            │
            ▼
        Tool Result
            │
            └────────────► next model step
```

后续再加入 persistent state / pause / resume / durable execution。

---

# Current Assignment — 001A: Reliable Tool Execution Boundary

先不要接真实 LLM。

原因：tool execution 是确定性后端逻辑。如果一开始就把模型随机性混进来，你很难知道错误究竟来自 runtime 还是模型。

## Scenario

实现两个 mock tools：

### `get_ticket`

读取工单。

特征：
- read-only；
- 可以安全重试；
- 不需要人工审批。

输入示例：

```json
{"ticket_id":"T-1001"}
```

### `close_ticket`

关闭工单。

特征：
- side effect；
- 必须审批；
- 必须有 idempotency protection；
- duplicate request 不能关闭两次。

输入示例：

```json
{"ticket_id":"T-1001","reason":"resolved"}
```

---

## You need to design

建议使用 Python。

不要使用 LangGraph / CrewAI / Agents SDK 等 Agent framework。

你可以使用标准库和测试框架。

至少需要表达这些概念：

```text
Run
ToolSpec
ToolCall
ToolResult
ToolRisk
ExecutionStatus
RetryableError
NonRetryableError
ApprovalRequired
```

具体 class / dataclass / enum 怎么设计，由你决定。

---

## `execute_tool(...)` must guarantee

### 1. Unknown tool cannot execute

tool name 不在 registry 中时直接失败。

### 2. Arguments are validated before execution

不要等业务函数跑到一半才发现输入不合法。

### 3. Side-effect tools require approval

`close_ticket` 未批准时不能进入真正的 tool function。

### 4. Retry depends on error semantics

不要写：

```python
except Exception:
    retry()
```

至少区分：
- transient / retryable；
- permanent / non-retryable；
- timeout；
- validation；
- authorization / approval。

### 5. Side effect is idempotent

相同 idempotency key 的 `close_ticket` 即使收到重复请求，也只能产生一次业务副作用。

注意：

> “函数调用一次”与“业务副作用一次”不是同一个概念。

这个区别后面会连接到数据库 transaction、outbox 和 crash recovery。

### 6. Every execution is traceable

至少记录：

```text
run_id
call_id
tool_name
attempt
start/end or duration
status
error_type
```

先用 structured event / dict 即可，不要求上 observability platform。

---

# Acceptance Tests

至少证明以下场景：

## Test 1 — unknown tool

```text
model/tool caller asks for delete_everything
→ registry rejects
→ no business function executes
```

## Test 2 — invalid arguments

```text
close_ticket(ticket_id="")
→ validation error
→ close function execution count = 0
```

## Test 3 — retryable read failure

```text
get_ticket
attempt 1 → RetryableError
attempt 2 → success
→ final success
→ trace contains 2 attempts
```

## Test 4 — non-retryable failure

```text
get_ticket
attempt 1 → NonRetryableError
→ no attempt 2
```

## Test 5 — approval boundary

```text
close_ticket without approval
→ ApprovalRequired
→ business side effect count = 0
```

## Test 6 — idempotent duplicate

```text
close_ticket(call A, idempotency_key=K1)
close_ticket(call B, idempotency_key=K1)

→ both callers receive a deterministic result
→ actual close side effect occurs exactly once
```

## Test 7 — trace correlation

一次 run 中的所有事件必须能通过 `run_id` 串起来；一个 tool call 的所有 retry attempt 必须能通过 `call_id` 串起来。

---

# Questions you must be able to answer after the lab

1. 为什么 retry 是 Agent runtime 的职责之一，而不能简单交给模型“再试一次”？
2. 为什么 `close_ticket` 需要 idempotency，而 `get_ticket` 通常风险更低？
3. tool 返回 timeout 时，你能确定它没有执行成功吗？
4. 为什么 approval 必须绑定具体 tool call / arguments，而不能只存一个 `approved=True`？
5. `run_id`、`call_id`、`idempotency_key` 分别解决什么问题？
6. 为什么不能对所有 Exception 使用同一个 retry policy？
7. 如果业务数据库 commit 成功后进程立刻崩溃，会发生什么？

第 7 题会直接引出后面的 transaction / outbox / durable execution。

---

# Not required yet

当前阶段故意不做：
- 真实 LLM API；
- MCP；
- database；
- Redis；
- message queue；
- LangGraph；
- distributed execution；
- UI。

先把 execution semantics 做正确。

---

# Next evolution

001A 通过后再逐步增加：

```text
001B  Model tool loop
001C  run budget + max steps + cancellation
001D  persistent run state
001E  crash recovery
001F  resumable human approval
001G  OpenTelemetry-style tracing
001H  sandboxed tools
```

这些阶段不会一次性全部实现，每次只推进一个可验收的工程问题。
