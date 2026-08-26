# Agent Learning Lab

一个面向 **Agent / AI 工程师长期成长** 的实战学习仓库。

这个仓库不是“AI 笔记大全”，也不是从零开始照章节学框架。目标是把日常工作、ChatGPT 对话学习、前沿技术跟踪和工程实验沉淀成一套可验证、可复用、持续演进的个人 Agent Engineering 知识与代码体系。

## 学习定位

主线分为两条，但不是 50/50 平分：

1. **Agent / AI Engineering（主线）**
   - Agent runtime / tool loop
   - Tool calling / structured output
   - Context engineering / memory
   - RAG / retrieval / reranking
   - MCP / A2A / agent interoperability
   - Durable execution / long-running agents
   - Human-in-the-loop / approvals
   - Evals / tracing / observability
   - Sandbox / security / authorization
   - Multi-agent / delegation
   - Model routing / cost / latency / reliability
   - Computer-use / coding agents / autonomous workflows

2. **Backend Engineering（支撑线）**
   - HTTP / API / RPC
   - concurrency / async
   - database / transaction
   - Redis / cache
   - queue / event
   - timeout / retry / idempotency
   - auth / permission
   - Docker / Kubernetes
   - logging / metrics / tracing
   - distributed systems fundamentals

后端知识不会脱离 Agent 单独背概念。优先在真实 Agent 工程问题里补齐：例如学 durable agent 时理解 checkpoint、事务和消息队列；学 tool execution 时理解 timeout、retry、idempotency；学 MCP/A2A 时理解 HTTP、RPC、OAuth 和服务治理。

## 长期工程原则

职业目标不是停留在“会调用模型 API / 会使用某个 Agent 框架”，而是逐步具备 **Production Agent Engineer / Applied AI Engineer / Agent Runtime or Platform Engineer** 的能力。

框架和职位名称会变，但 runtime、context、state、tool execution、durability、eval、observability、security 和 backend reliability 等问题会长期存在。

详细原则见：[`ENGINEERING_PRINCIPLES.md`](./ENGINEERING_PRINCIPLES.md)。

## 学习原则

### 1. 不从纯小白路线重新开始

已经知道的内容快速验证后跳过；知识缺口在实际工程问题中补。学习速度由“能否解释 + 能否实现 + 能否排错”决定，而不是由看完多少教程决定。

### 2. 不追框架 API，先掌握运行机制

可以学习 OpenAI Agents SDK、LangGraph、Vercel AI SDK、MCP SDK 等，但必须能回答：

- framework 帮我隐藏了什么？
- state 存在哪里？
- tool call 失败后发生什么？
- 一个 side effect 被重试会怎样？
- Agent 为什么能暂停和恢复？
- trace 如何把一次执行串起来？
- 模型输出正确，但业务为什么仍然可能失败？

### 3. 新技术必须经过“前沿雷达”筛选

不是 GitHub Trending 出现什么就学什么。优先选择同时满足以下条件的技术：

- 对生产 Agent 系统有实际价值；
- 正在形成行业标准或被主流生态采用；
- 能提升工程能力，而不是只增加一个框架名字；
- 可以通过实验验证。

见 [`FRONTIER_RADAR.md`](./FRONTIER_RADAR.md)。

### 4. 每个核心主题尽量落到实验

仓库里长期保留的是：

- mental model；
- architecture / data flow；
- failure modes；
- 关键代码；
- tests；
- benchmark / eval；
- debugging 记录；
- 最终工程结论。

临时聊天、重复解释和未经验证的结论不进入仓库。

## 仓库工作流

日常学习流程：

```text
工作中遇到问题 / 想学新技术
        ↓
ChatGPT 解释、追问、设计实验
        ↓
自己先写关键代码 / 做判断
        ↓
代码审查、测试、失败分析
        ↓
形成稳定结论
        ↓
ChatGPT 更新本仓库
        ↓
PROGRESS / ROADMAP 同步推进
```

## 当前结构

```text
agent-learning-lab/
├── README.md
├── ENGINEERING_PRINCIPLES.md
├── ROADMAP.md
├── PROGRESS.md
├── FRONTIER_RADAR.md
└── labs/
    └── 001-reliable-agent-runtime/
        ├── README.md
        └── CURRENT_TASK.md
```

结构会随着学习真实增长，不预先创建几十个空目录。

## 当前起点

第一个实验不是聊天机器人，而是：

**Lab 001 — Reliable Agent Runtime**

目标是自己建立一个最小但工程语义正确的 Agent 执行循环，逐步加入：tool boundary、side effect、approval、idempotency、timeout、retry、step budget 和 trace。

Lab 总说明：[`labs/001-reliable-agent-runtime/README.md`](./labs/001-reliable-agent-runtime/README.md)

**当前唯一任务：** [`001A-1 — Define the Tool Execution Contract`](./labs/001-reliable-agent-runtime/CURRENT_TASK.md)

不要提前做后面的 retry、approval、idempotency、LLM 或 MCP。先把执行契约做对。

## 长期目标

最终能够独立回答并实现下面这类问题：

> 如何设计一个可以运行数分钟到数小时、会调用多个外部系统、允许人工审批、宕机后可恢复、不会重复执行危险操作、可观测、可评估、可控成本，并能通过 MCP/A2A 与外部能力协作的生产级 Agent？

当这个问题不再只是“会用某个 Agent 框架”，而是能够从 runtime、backend、protocol、security、eval 和 infra 层完整设计时，这个仓库才真正达到目标。
