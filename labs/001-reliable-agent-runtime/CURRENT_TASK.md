# Current Task — 001A-1: Define the Tool Execution Contract

当前只做这一小步。不要提前实现 retry、idempotency、数据库、真实 LLM 或 Agent framework。

## 目标

建立一个最小的 Tool Execution Boundary，让系统能够明确表达：

```text
谁在执行？
执行哪个 tool？
输入是什么？
这个 tool 有什么风险属性？
执行结果是什么？
失败属于哪一类？
```

这一步的重点不是代码量，而是把 Agent Runtime 的核心数据契约设计正确。

## 你需要自己实现

建议目录：

```text
labs/001-reliable-agent-runtime/
├── CURRENT_TASK.md
├── README.md
└── src/
    └── ...
```

文件如何拆分由你决定。

至少需要表达这些概念：

- `Run`
- `ToolSpec`
- `ToolCall`
- `ToolResult`
- `ToolRisk`
- `ExecutionStatus`

可以使用 `dataclass`、`Enum`、普通 class 等 Python 标准能力，自行选择。

## 第一版只支持两个 mock tools

### `get_ticket`

输入：

```json
{"ticket_id":"T-1001"}
```

属性：

- read-only
- low risk
- 暂时不做 retry
- 不需要 approval

### `close_ticket`

输入：

```json
{"ticket_id":"T-1001","reason":"resolved"}
```

属性：

- 会产生 side effect
- higher risk
- 以后需要 approval / idempotency，但这一小步先只把这些属性表达在 `ToolSpec` 中，不实现机制

## 需要实现的最小执行入口

设计一个类似下面职责的函数，但函数签名由你自己决定：

```text
execute_tool(...)
```

当前只要求它完成：

1. 根据 `tool_name` 从 registry 找 tool；
2. unknown tool 明确失败；
3. 在业务函数执行前完成最小参数校验；
4. 调用对应 mock tool；
5. 返回结构化 `ToolResult`；
6. 不把异常全部吞成一个字符串。

## 暂时不要做

- retry
- timeout
- approval enforcement
- idempotency
- persistence
- tracing platform
- async
- LLM API
- MCP
- LangGraph / Agents SDK / CrewAI

这些都会在后续逐层加入。

## 验收测试

至少自己写测试证明：

### Test 1 — known tool succeeds

```text
get_ticket(T-1001)
→ ToolResult.status == success
→ result 中能拿到 mock ticket
```

### Test 2 — unknown tool is rejected

```text
delete_everything
→ 明确的 unknown-tool failure
→ 没有任何 business function 被执行
```

### Test 3 — invalid arguments fail before business execution

```text
get_ticket(ticket_id="")
→ validation failure
→ get_ticket 的实际执行次数仍为 0
```

### Test 4 — side-effect metadata is visible

程序能够从 `ToolSpec` 判断：

```text
get_ticket  = read-only / low risk
close_ticket = side-effect / higher risk
```

当前不需要阻止 `close_ticket`，只是要证明 runtime 已经知道两者不同。

## 写完后你必须能回答

1. `ToolSpec` 和 `ToolCall` 为什么不能合成一个对象？
2. 为什么参数校验必须在业务函数执行前？
3. 为什么 Agent Runtime 需要知道 tool 是否有 side effect？
4. `ToolResult` 为什么最好包含明确 status，而不是只返回任意 Python 对象？
5. registry 在 Agent runtime 里解决了什么问题？

## 完成方式

你自己提交代码到仓库后，在 ChatGPT 中说：

> 审查 001A-1

下一步才进入 `001A-2: approval boundary + risk enforcement`。
