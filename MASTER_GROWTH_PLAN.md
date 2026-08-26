# Master Growth Plan — Production Agent Engineer

> Baseline: 2026-08-26
>
> Target: 从已有 Agent 应用经验，成长为具备大厂标准的 Production Agent / Applied AI / Agent Systems Engineer。

这不是按月份强制推进的课程表，而是一张 **能力地图 + 晋级标准**。工作繁忙时可以降低节奏，但不降低验收标准。

---

## 0. 当前起点

默认已具备或接触过：

- Python 开发；
- RAG 基本流程；
- LangChain；
- LangGraph；
- Agent / workflow 基本概念；
- tool calling / function calling；
- 使用 Codex 等 coding agent 参与实际项目。

因此下面内容不再从纯入门重学。只有实际暴露知识缺口时按需回补。

当前最值得补齐的差异化能力：

1. Agent eval / failure analysis；
2. Agent harness / runtime semantics；
3. backend / distributed systems；
4. long-running / durable execution；
5. context & memory engineering；
6. observability / performance / cost；
7. sandbox / auth / security；
8. MCP / A2A interoperability；
9. production architecture / platform thinking。

---

# Capability Ladder

## Level 1 — Agent Application Engineer

能够把模型、RAG、工具和 workflow 拼成可用应用。

典型能力：
- 调模型；
- prompt / structured output；
- RAG；
- framework graph/workflow；
- 简单 tools；
- 基础 API service。

这不是本仓库的终点，当前基础大体已覆盖。

## Level 2 — Production Agent Engineer

能够解释和解决：
- 为什么 Agent 会失败；
- tool timeout 后能不能 retry；
- side effect 如何保证安全；
- 怎么测 agent 成功率；
- 怎么定位失败 step；
- 如何控制 latency / tokens / cost；
- context 为什么退化；
- 如何让任务可以暂停、恢复、重跑。

这是近期核心目标。

## Level 3 — Agent Systems / Platform Engineer

能够设计：
- reusable agent harness；
- execution runtime；
- durable workflow；
- sandbox / isolation；
- multi-tenant state；
- tool platform；
- MCP/A2A gateway；
- observability + eval platform；
- fleet / concurrency / capacity / cost controls。

## Level 4 — Advanced Applied AI / Core Agent Engineer

能够围绕真实任务持续提高 agent performance：
- solve rate；
- trajectory quality；
- context construction；
- tool-use strategy；
- model + harness ablation；
- production feedback loop；
- model routing；
- long-horizon reliability。

---

# Phase 1 — Evals, Traces & Failure Analysis

**优先级：最高。**

原因：不会评估，就无法科学改 Agent。大厂 Agent 工程越来越强调 eval、experimentation、production failure analysis，而不只是“跑通 demo”。

## 必修能力

- agent trajectory / step / event；
- task success metric；
- deterministic grader；
- LLM-as-judge 的适用边界；
- regression dataset；
- tool-selection accuracy；
- argument correctness；
- retrieval / model / tool / harness failure taxonomy；
- trace correlation；
- latency / tokens / cost measurement；
- experiment / ablation thinking。

## 实验

### Lab 001 — Agent Harness Evaluation Baseline

拿一个小型 tool-using Agent，建立：
- 20~30 条最小 eval cases；
- structured run trace；
- success/failure taxonomy；
- latency/token/tool-call metrics；
- fault injection；
- 一次明确的 before/after experiment。

## 通过标准

能够回答：
- 这次 Agent 失败到底是 model、context、retrieval、tool 还是 harness？
- 修改 prompt 后成功率有没有真的提高？
- 成功率提高 3%，但 cost 翻倍，值不值？
- 一个 case 为什么应该进入 regression set？

---

# Phase 2 — Reliable Agent Harness / Runtime

## 必修能力

- agent loop；
- tool registry；
- tool schema validation；
- execution state machine；
- run_id / step_id / call_id；
- timeout / cancellation；
- retry policy；
- retryable vs non-retryable errors；
- idempotency；
- approval boundary；
- side-effect semantics；
- max steps / token budget / cost budget；
- deterministic orchestration vs model decisions。

## Backend 按需补齐

- HTTP lifecycle；
- context/deadline；
- exceptions / error taxonomy；
- concurrency / async；
- request IDs；
- idempotency keys。

## 实验

### Lab 002 — Reliable Tool Runtime

要求证明：
- timeout 后结果可能是 unknown outcome；
- dangerous tool 不会因 retry 重复副作用；
- approval 绑定具体 args；
- 每个 step 都能从 trace 还原。

## 通过标准

关闭框架文档，也能画出一个 production agent execution loop，并解释每个失败边界。

---

# Phase 3 — Backend & Distributed Systems for Agents

不是单独学一本后端教材，而是围绕 Agent 生产问题学习。

## 必修能力

### API / service
- HTTP / REST / RPC；
- streaming；
- rate limit；
- authn / authz；
- graceful shutdown。

### Database
- transaction；
- isolation；
- optimistic / pessimistic concurrency；
- unique constraint；
- atomic state transition；
- schema migration。

### Async / Messaging
- queue；
- consumer；
- ack；
- retry；
- DLQ；
- at-least-once；
- ordering；
- lease / heartbeat。

### Cache / coordination
- Redis；
- TTL；
- distributed state；
- locks 的边界；
- cache consistency。

## 实验

### Lab 003 — Durable Run Store

把 Agent run 从进程内存迁移到持久化状态。

必须实验：
- process crash；
- duplicate delivery；
- concurrent resume；
- commit 成功但 response 丢失；
- stale worker。

---

# Phase 4 — Context & Memory Engineering

从 prompt engineering 升级为 context system design。

## 必修能力

- context assembly；
- token budget；
- prompt caching；
- compaction；
- summarization loss；
- tool result compression；
- short-term state；
- episodic / semantic / procedural memory；
- memory write policy；
- memory retrieval policy；
- forgetting / invalidation；
- provenance；
- context poisoning。

## 实验

### Lab 004 — Context Budget Experiment

固定任务集，对比：
- full history；
- sliding window；
- summarized history；
- retrieval memory；
- structured state。

同时测：
- success rate；
- tokens；
- latency；
- cost；
- failure type。

---

# Phase 5 — Advanced Retrieval

已有 RAG 基础，因此不重复 embedding + vector DB 入门。

## 必修能力

- lexical + dense hybrid retrieval；
- reranker；
- metadata filtering；
- query decomposition；
- query rewriting；
- retrieval routing；
- multi-hop retrieval；
- freshness；
- provenance / citation；
- permission-aware retrieval；
- retrieval eval；
- GraphRAG 的适用边界。

## 实验

### Lab 005 — Retrieval Failure Lab

建立数据集，明确区分：
- 没召回；
- 召回了但没排到前面；
- context 有答案但模型没使用；
- 数据过期；
- 权限过滤导致缺失。

目标不是“再做一个 RAG”，而是学会诊断 RAG。

---

# Phase 6 — Durable / Long-Horizon Agents

## 必修能力

- checkpoint；
- persistence；
- pause / resume；
- human interrupt；
- durable timer；
- workflow replay；
- determinism；
- compensation；
- crash recovery；
- lease / heartbeat；
- exactly-once illusion。

## 实验

### Lab 006 — Kill the Agent

运行一个多 step Agent，在不同位置主动 kill process：
- model call 前；
- tool call 前；
- side effect commit 后；
- checkpoint 前后；
- waiting approval 时。

要求恢复后不重复危险动作。

对比：
- 自研 state machine；
- LangGraph persistence；
- 一种 durable workflow/runtime 实现。

---

# Phase 7 — Security, Identity & Sandbox

## 必修能力

- prompt injection；
- indirect injection；
- tool privilege escalation；
- least privilege；
- capability-based access；
- OAuth / delegated auth；
- secrets isolation；
- sandbox；
- filesystem/network policy；
- approval；
- audit log；
- data exfiltration；
- tenant isolation。

## 实验

### Lab 007 — Adversarial Tool Agent

构造恶意网页/文档输入，引诱 Agent：
- 泄露 secret；
- 调高权限 tool；
- 修改不相关资源；
- 绕过 approval。

要求建立 threat model + defense tests。

---

# Phase 8 — MCP / A2A / Agent Interoperability

学习协议，但重点是协议背后的系统问题。

## MCP

跟踪 2026-07-28 以后：
- stateless core；
- HTTP routing；
- authorization；
- Tasks / extensions；
- cacheability；
- protocol versioning；
- production deployment。

## A2A

重点理解：
- agent discovery；
- task delegation；
- agent identity；
- remote lifecycle；
- MCP vs A2A boundary。

## 实验

### Lab 008 — Agent Interop Gateway

实现：
- 一个 MCP tool/service；
- 一个 remote agent；
- auth boundary；
- tracing；
- version / failure handling。

---

# Phase 9 — Model & Runtime Strategy

## 必修能力

- model routing；
- capability routing；
- reasoning effort / budget；
- fallback；
- provider abstraction；
- rate limiting；
- caching；
- parallel tool calls；
- speculative strategies；
- multimodal / realtime / computer use；
- quality-latency-cost frontier。

## 实验

### Lab 009 — Model Router

同一 eval set 对多种模型/配置测：
- quality；
- p50/p95 latency；
- tokens；
- cost；
- tool correctness。

设计 routing policy，而不是默认所有请求都用最大模型。

---

# Phase 10 — Multi-Agent & Delegation

原则：**先证明单 Agent 不够，再增加 Agent。**

## 必修能力

- supervisor / worker；
- planner / executor；
- handoff；
- shared vs isolated context；
- delegation budget；
- conflict resolution；
- failure amplification；
- observability；
- cost accounting。

## 实验

### Lab 010 — Single vs Multi-Agent Ablation

同一个任务集比较：
- 单 Agent；
- planner + executor；
- specialist agents。

必须量化增加复杂度是否真的提高成功率。

---

# Phase 11 — Agent Platform / Infrastructure

这是从“做 Agent 应用”进入“做 Agent 基础设施”的关键阶段。

## 必修能力

- multi-tenant runtime；
- worker pool；
- scheduler；
- sandbox fleet；
- storage；
- queue；
- orchestration；
- secret / identity propagation；
- quotas；
- observability；
- capacity；
- cost controls；
- deployment / Kubernetes fundamentals。

## 实验

### Lab 011 — Mini Agent Platform

让多个用户可以提交长任务，并具有：
- durable state；
- isolated workspace；
- tool permissions；
- retries；
- cancellation；
- trace；
- quota；
- worker recovery。

---

# Capstone — Production Agent System

最终不是做一个“功能很多”的 demo，而是做一个可被系统设计面试和真实工程审查的项目。

必须包含：

- real business scenario；
- API service；
- agent harness；
- persistent state；
- durable execution；
- reliable tool boundary；
- RAG/context/memory；
- sandbox / approval；
- MCP；
- optional A2A；
- eval dataset；
- regression pipeline；
- traces / metrics；
- auth / tenant isolation；
- failure recovery；
- cost / latency analysis；
- tests / CI；
- architecture decision records。

最终必须能够回答：

> 为什么这个系统这样设计？
> 最危险的 failure mode 是什么？
> 怎么证明改动让系统更好？
> 如果扩大 100 倍流量哪里先坏？
> 如果模型换代，哪些层需要改，哪些层不用改？

---

# 并行能力：Backend Support Track

后端不独立排成几十章，而是跟主线绑定：

| Agent 问题 | 顺带深入的后端能力 |
|---|---|
| Tool timeout/retry | HTTP deadline、error semantics、idempotency |
| Persistent run | SQL、transaction、concurrency |
| Long-running task | queue、lease、heartbeat、DLQ |
| Memory | database、Redis、cache consistency |
| MCP/A2A | HTTP/RPC、OAuth、service boundary |
| Sandbox | process/container/Linux isolation |
| Agent platform | Docker、Kubernetes、distributed systems |
| Observability | logs、metrics、traces、OpenTelemetry |

---

# 学习方式

默认采用：

```text
高质量 reference implementation
        ↓
逐段讲解
        ↓
运行 + trace
        ↓
关键修改
        ↓
fault injection / debugging
        ↓
tests / eval
        ↓
设计题
        ↓
记录进度
```

不要求每个项目从空白文件开始。

但下面这些核心逻辑会要求独立实现或重写：
- state transition；
- retry / idempotency；
- context policy；
- evaluator；
- concurrency control；
- auth / approval；
- crash recovery。

---

# 晋级规则

一个能力只有在以下至少 4 项成立时才算 PASSED：

1. 能解释 mental model；
2. 能读懂 production-style implementation；
3. 能修改关键逻辑；
4. 能写/改测试；
5. 能 debug failure；
6. 能分析 trade-off；
7. 能在不同框架间迁移；
8. 能通过 system design 问题。

“看过”“抄过”“跑通了”都不算真正通过。

---

# 当前顺序

当前优先路径：

```text
Phase 1 Evals & Failure Analysis
   ↓
Phase 2 Reliable Harness
   ↓
Phase 3 Backend/Distributed Foundations
   ↓
Phase 4 Context & Memory
   ↓
Phase 6 Durable Agents
   ↓
Phase 7 Security
   ↓
Phase 8 MCP/A2A
   ↓
Phase 9 Runtime Strategy
   ↓
Phase 11 Agent Platform
```

Advanced Retrieval 和 Multi-Agent 根据工作需求穿插，不为了课程顺序强行学习。
