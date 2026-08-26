# Agent Learning Lab

一个面向 **Production Agent / Applied AI / Agent Systems Engineer** 长期成长的实战学习仓库。

这个仓库不是“AI 笔记大全”，也不是从零开始按框架章节学习。目标是把日常工作、ChatGPT 对话学习、前沿技术跟踪和工程实验沉淀成一套可验证、可迁移、持续演进的个人 Agent Engineering 能力体系。

## 当前定位

已具备/接触：Python、RAG、LangChain、LangGraph、Agent/workflow、tool calling，并有实际 Agent 项目经验。

因此这些内容默认不从零重学。主线直接进入大厂 Agent Engineer 更看重的能力：

```text
Evals + Failure Analysis
        ↓
Reliable Agent Harness / Runtime
        ↓
Backend & Distributed Systems
        ↓
Context / Memory Engineering
        ↓
Durable Long-Running Agents
        ↓
Security / Sandbox / Identity
        ↓
MCP / A2A Interoperability
        ↓
Observability / Performance / Cost
        ↓
Agent Platform / Infrastructure
```

Advanced Retrieval、Multi-Agent、Model Routing 根据工作和实验需要穿插。

## 最重要的文件

- [`MASTER_GROWTH_PLAN.md`](./MASTER_GROWTH_PLAN.md)：完整成长路线、阶段实验和晋级标准；
- [`MENTORING_SYSTEM.md`](./MENTORING_SYSTEM.md)：ChatGPT 如何教学、布置任务、审查和维护进度；
- [`ROLE_TARGET.md`](./ROLE_TARGET.md)：当前大厂 Agent Engineering 目标能力；
- [`ENGINEERING_PRINCIPLES.md`](./ENGINEERING_PRINCIPLES.md)：长期不轻易变化的工程原则；
- [`FRONTIER_RADAR.md`](./FRONTIER_RADAR.md)：2026+ 前沿技术雷达；
- [`PROGRESS.md`](./PROGRESS.md)：当前能力状态和已通过证据；
- [`ROADMAP.md`](./ROADMAP.md)：能力地图摘要。

## 两条学习线

### Agent / AI Engineering — 主线

- agent harness / runtime
- evals / experiments / failure analysis
- tool execution
- context / memory
- advanced retrieval
- durable execution
- MCP / A2A
- security / sandbox
- observability
- model routing / cost / latency
- multi-agent / delegation
- agent platform

### Backend Engineering — 支撑线

后端不与 Agent 脱离学习，而是在真实 Agent 系统问题里补：

- HTTP / API / RPC
- concurrency / async
- SQL / transaction
- Redis / cache
- queue / event
- timeout / retry / idempotency
- auth / permission
- Docker / Kubernetes
- logging / metrics / tracing
- distributed systems

例如：

```text
Tool retry        → idempotency / transaction
Long-running run  → queue / lease / heartbeat
Agent memory      → DB / cache consistency
MCP / A2A         → HTTP / RPC / OAuth
Sandbox           → process / container isolation
Agent platform    → distributed systems / Kubernetes
```

## 学习方式

不默认要求从空白文件手写所有代码。

默认采用：

```text
Teacher 给高质量带注释 reference implementation
        ↓
逐段讲解 execution path / mental model
        ↓
自己运行
        ↓
修改关键行为
        ↓
fault injection / debugging
        ↓
增加 tests / eval
        ↓
回答设计问题
        ↓
Teacher 直接审 GitHub
        ↓
更新 PROGRESS
        ↓
解锁下一任务
```

关键状态机、retry/idempotency、context policy、eval、authorization、concurrency 和 crash recovery 等核心逻辑仍会要求自己实现或重写。

详见 [`LEARNING_METHOD.md`](./LEARNING_METHOD.md) 和 [`MENTORING_SYSTEM.md`](./MENTORING_SYSTEM.md)。

## 当前任务

当前阶段从 **Agent Evals & Failure Analysis** 开始，而不是重新学习 RAG/LangChain/LangGraph。

入口：[`labs/001-reliable-agent-runtime/CURRENT_TASK.md`](./labs/001-reliable-agent-runtime/CURRENT_TASK.md)

完成代码/实验后，只需要在 ChatGPT 中说：

> 审查当前任务

ChatGPT 会直接读取仓库最新实现，给出结论并维护 `PROGRESS.md`。

## 长期目标

最终能够独立设计和解释一个生产 Agent 系统：

> 它能执行长任务、调用外部系统、处理副作用、允许人工审批、宕机恢复、隔离不可信执行、控制权限与成本，并且可以通过 trace/eval 数据持续证明系统在变好。

真正的目标不是“会某个 Agent 框架”，而是具备即使模型、框架和协议继续快速变化，也能迁移的 Agent Systems Engineering 能力。
