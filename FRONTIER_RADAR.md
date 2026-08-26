# Frontier Radar

> Last reviewed: 2026-08-26

这个文件专门追踪 Agent Engineering 的技术变化。

它不是新闻收藏夹。每个候选技术都要回答三个问题：

1. 它解决了什么真实工程问题？
2. 它改变的是 API，还是改变了系统设计方式？
3. 是否值得投入实验时间？

状态定义：

- **ADOPT**：应进入主线实战；
- **TRIAL**：值得做实验，但不急着作为长期依赖；
- **WATCH**：继续观察规范、生态和生产采用；
- **IGNORE FOR NOW**：当前收益不足以占用学习时间。

---

## ADOPT — MCP 2026-07-28

### 为什么重要

MCP 已经不只是“给 Claude 接几个本地工具”的协议。2026-07-28 版本把核心改成 stateless request/response 模型，移除原来的 session/handshake 依赖，更适合普通 HTTP 基础设施和水平扩展。

值得学习的工程点：
- stateless protocol core；
- header-based routing；
- capability discovery；
- authorization hardening；
- cacheable tool lists；
- extensions；
- Tasks；
- protocol versioning / deprecation。

### 学习重点

不要只会用 SDK 起一个 MCP server。必须理解：
- 为什么 stateless 更容易扩容；
- MCP server 如何做鉴权；
- tool schema 如何成为远程能力契约；
- MCP gateway 能做什么；
- protocol upgrade 如何兼容旧 client。

Official sources:
- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://blog.modelcontextprotocol.io/posts/mcp-roadmap/

---

## ADOPT — A2A 1.0

### 为什么重要

MCP 主要解决 Agent/application 与 tools/data 的连接；A2A 解决独立 Agent 之间的发现、任务委托和互操作。

关键概念：
- Agent Card / discovery；
- messages vs tasks；
- delegation；
- streaming / long-running interaction；
- opaque agents；
- interoperability across frameworks/vendors。

### 学习重点

重点不是“多 Agent 很高级”，而是判断：
- 什么时候应该直接 tool call；
- 什么时候应该调用远程 Agent；
- 远程 Agent 的信任边界在哪里；
- MCP 与 A2A 怎样组合。

Official source:
- https://a2a-protocol.org/v1.0.0/

---

## ADOPT — Long-horizon Agent Runtime + Sandbox

### 为什么重要

新一代 coding / computer-use / research agents 越来越像一个长时间运行的执行系统，而不是一次 LLM request。

OpenAI 在 2026 Agents SDK 更新中强调 model-native harness、文件/命令执行、long-horizon tasks 和 controlled sandbox execution。

需要掌握：
- harness vs model；
- agent loop；
- sandbox boundary；
- compute isolation；
- state persistence；
- long-running task lifecycle；
- cancellation / timeout / resource limits。

Official source:
- https://openai.com/index/the-next-evolution-of-the-agents-sdk/

---

## ADOPT — Durable Agents

### 为什么重要

真实 Agent 不能假设：
- 进程永远不挂；
- HTTP 请求永远不断；
- tool call 永远一次成功；
- human approval 会立刻回来。

当前主流 Agent runtimes 越来越明确地引入 checkpoint、pause/resume、retryable steps 和 durable workflow。

值得对比：
- LangGraph checkpoint / interrupts；
- Vercel WorkflowAgent / Workflow DevKit；
- Temporal-style workflow concepts；
- 自研 state machine + queue。

Official sources:
- https://docs.langchain.com/oss/python/langgraph/interrupts
- https://vercel.com/blog/ai-sdk-7

---

## ADOPT — Agent Observability + Evals

### 为什么重要

Agent 的输出不是单个 completion，而是一条 trajectory：

```text
model → tool → model → retrieval → tool → approval → model → result
```

只记录最终 answer 无法排查失败。

需要逐步掌握：
- run / trace / span；
- model span；
- tool span；
- workflow span；
- token / cost / latency；
- trajectory eval；
- regression dataset；
- tool selection / argument correctness；
- sensitive telemetry policy。

OpenTelemetry 的 semantic conventions 仍在演进，GenAI conventions 已独立演进，因此学习时要区分稳定标准与 development 状态。

Official sources:
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/

---

## ADOPT — Human-in-the-loop as Runtime Primitive

危险工具不能只靠 prompt 写一句“请小心”。

需要掌握：
- risk classification；
- approval before side effect；
- resumable approval；
- timeout / expiry；
- actor identity；
- audit trail；
- approval data binding（批准的到底是哪一个参数版本）。

LangGraph interrupts、现代 Agent SDK 的 tool approval 都说明 HITL 正逐渐从产品补丁变成 runtime primitive。

---

## TRIAL — Vercel AI SDK 7 / Framework-independent Agent Harness Integration

AI SDK 7 增加了 reasoning control、runtime context、skills、MCP Apps、WorkflowAgent、timeouts、sandbox、telemetry，并允许集成不同 agent harness。

为什么先放 TRIAL：
- 技术方向值得学习；
- 但仓库目标不是绑定 TypeScript framework；
- 应先理解 runtime semantics，再比较框架抽象是否合理。

Official source:
- https://vercel.com/blog/ai-sdk-7

---

## WATCH — MCP Agentic Messaging / Identity

2026-08-22 MCP roadmap 的后续重点包括：
- agentic messaging primitives；
- HTTP-native transport hardening；
- agent identity；
- enterprise security；
- SDK DX。

这部分很可能影响未来 Agent-to-Agent / Agent-to-Tool 的基础设施设计，持续跟踪，但等规范进一步落地后再做深度实现。

Official source:
- https://blog.modelcontextprotocol.io/posts/mcp-roadmap/

---

## 永久关注的问题，而不是永久追某个框架

真正需要长期追踪的是这些问题：

1. Agent 如何可靠执行副作用？
2. Agent 如何暂停、恢复和跨进程存活？
3. 上下文如何构建、压缩和记忆？
4. Agent 如何连接外部工具和其他 Agent？
5. 权限、身份和信任边界怎么设计？
6. 如何知道 Agent 真的变好了？
7. 如何观察一条复杂 trajectory？
8. 如何控制 token、延迟和成本？
9. 如何安全运行模型生成的代码/命令？
10. 哪些决策根本不应该交给模型？

框架会换，这十个问题不会很快消失。
