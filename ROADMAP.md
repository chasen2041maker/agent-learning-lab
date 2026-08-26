# Roadmap

这份路线不是固定课程表，而是能力地图。顺序可以根据工作中遇到的问题动态调整，但每个阶段都有明确的“通过标准”。

## Stage A — Reliable Agent Runtime

重点：先把 Agent 从“会调用模型”升级成“可控执行系统”。

学习内容：
- tool loop / agent loop
- structured tool input / output
- state transition
- max steps / token budget / cost budget
- timeout / retry / cancellation
- idempotency / deduplication
- side effect classification
- human approval
- error taxonomy
- trace / run id / tool call id
- sandbox boundary

通过标准：
- 能自己画出一次 Agent run 的完整执行链路；
- 能解释模型错误、工具错误、网络错误、业务错误的区别；
- 能证明危险工具在重试时不会重复产生副作用；
- 能从 trace 定位一次失败发生在哪个 step；
- 不依赖 Agent framework 也能实现最小 runtime。

对应实验：`labs/001-reliable-agent-runtime/`

---

## Stage B — Context & Memory Engineering

重点：从“prompt engineering”升级到“context system design”。

学习内容：
- context assembly
- system / developer / user / tool result boundaries
- context window 与 token economics
- compaction / summarization
- short-term state vs long-term memory
- episodic / semantic / procedural memory
- retrieval memory
- memory write policy / forgetting policy
- tool-result compression
- prompt caching
- context poisoning

通过标准：
- 能解释什么时候应该 retrieval，什么时候应该 memory；
- 能设计 context budget；
- 能避免无限历史消息导致成本和质量同时恶化；
- 能评估 memory 写入是否真的提升任务成功率。

---

## Stage C — Agent Protocols & Interoperability

重点：理解 Agent 如何从“一个应用里的工具调用”扩展到跨服务、跨厂商协作。

学习内容：
- MCP 2026-07-28 stateless core
- MCP tools / resources / extensions / tasks
- HTTP transport
- MCP authorization / client identity
- A2A 1.0
- Agent Card / discovery
- task delegation
- MCP vs A2A boundary
- protocol versioning / compatibility

通过标准：
- 能自己实现一个最小 MCP server + client；
- 能解释为什么 MCP 与 A2A 不是竞争关系；
- 能设计远程 Agent/tool 的鉴权和权限边界；
- 能分析协议升级带来的兼容性问题。

---

## Stage D — Durable & Long-running Agents

重点：让 Agent 不依赖单个 HTTP 请求活着。

学习内容：
- checkpoint / persistence
- pause / resume
- interrupts
- durable workflow
- retryable steps
- task queue
- lease / heartbeat
- crash recovery
- compensation
- workflow determinism
- exactly-once illusion

候选实现：
- LangGraph persistence / interrupts
- Vercel WorkflowAgent / Workflow DevKit
- Temporal-style durable execution concepts
- 自研最小 state machine

通过标准：
- Agent 进程被杀掉后可以恢复；
- 人工审批等待数小时不会占住一个请求；
- 重放 workflow 不会重复危险 side effect；
- 能解释 durable workflow 与普通 async task 的本质差异。

---

## Stage E — Evals & Observability

重点：不靠“我试了几次感觉不错”评价 Agent。

学习内容：
- trace / span / event
- trajectory evaluation
- task success metrics
- tool-selection accuracy
- argument correctness
- groundedness
- latency / token / cost metrics
- regression dataset
- LLM-as-judge 的边界
- deterministic evaluator
- online vs offline eval
- OpenTelemetry GenAI conventions

通过标准：
- 每次 Agent run 可追踪；
- 修改 prompt/model/tool 后能跑 regression；
- 能定位质量下降发生在模型、检索、工具还是 orchestration；
- 能同时看成功率、延迟和成本，而不是只看模型输出。

---

## Stage F — Agent Security & Safety Engineering

学习内容：
- prompt injection
- indirect prompt injection
- tool privilege escalation
- least privilege
- capability-based tool access
- secret isolation
- sandbox
- approval policy
- data exfiltration
- MCP/A2A trust boundary
- audit log

通过标准：
- 能为每个工具定义权限和危险等级；
- untrusted content 不能直接获得高权限 tool execution；
- 敏感操作有审批、审计和回滚策略；
- 能进行基础 Agent threat modeling。

---

## Stage G — Retrieval & Knowledge Systems

不重复只会“embedding + vector DB”的基础 RAG，而是重点研究：
- hybrid retrieval
- metadata filtering
- reranking
- query decomposition
- agentic retrieval
- retrieval eval
- index freshness
- chunking trade-offs
- citation / provenance
- permission-aware retrieval
- GraphRAG 适用边界

通过标准：
- 能用数据证明 retrieval 改动带来的收益；
- 能定位召回失败与生成失败；
- 能设计企业级权限隔离和 freshness 策略。

---

## Stage H — Multi-agent & Delegation

学习内容：
- manager / worker
- planner / executor
- handoff
- specialist agents
- shared state vs isolated state
- delegation budget
- multi-agent failure amplification
- A2A-based interoperability

原则：默认先证明单 Agent 不够，再引入 multi-agent。

通过标准：
- 能说明增加一个 Agent 带来的明确收益；
- 能量化额外延迟、token 和故障面；
- 不用“多 Agent 看起来高级”作为架构理由。

---

## Stage I — Model & Runtime Strategy

学习内容：
- model routing
- reasoning budget
- small model / large model split
- fallback
- provider abstraction
- rate limit
- batch / async
- caching
- speculative / parallel execution
- voice / multimodal / computer-use runtimes

通过标准：
- 能根据任务风险、复杂度、延迟和成本选模型；
- provider 故障时有降级路径；
- 能解释什么时候不应该让模型参与决策。

---

## Capstone — Production Agent Platform

最终综合项目应具备：
- API service
- persistent run state
- reliable tool execution
- sandbox / approval
- MCP integration
- optional A2A delegation
- retrieval / memory
- durable workflow
- trace + metrics + evals
- auth / tenant isolation
- failure recovery
- CI tests
- deployment architecture

它不是为了“功能最多”，而是证明已经具备生产 Agent 系统设计能力。
