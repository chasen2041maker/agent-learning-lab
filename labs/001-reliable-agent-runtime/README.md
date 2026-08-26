# Lab 001 — Agent Harness, Evals & Reliability

## Why this lab exists

你已经会基础 Agent、RAG、LangChain、LangGraph，所以本实验不再从“怎么创建一个 Agent”开始。

真正要训练的是：

> **如何判断一个 Agent 为什么失败，以及如何用工程证据证明它变好了。**

生产 Agent 常见问题包括：

- runtime 正常结束，但用户任务其实没完成；
- 模型选错 tool；
- tool 参数错；
- tool backend 故障；
- tool 已产生 side effect，但响应丢失；
- retry 导致重复业务动作；
- Agent 无限循环；
- context 退化；
- 修改 prompt 后某些 case 变好、另一些 regression；
- 成功率提高，但 latency / tokens / cost 大幅恶化。

因此 Lab 001 的顺序是：

```text
先会测
  ↓
再会定位
  ↓
再改 harness
  ↓
再增加 reliability
```

而不是先堆一套复杂框架。

---

# Architecture We Will Grow

```text
User Task
    │
    ▼
Agent Run Controller
    │
    ├── model decision
    ├── context
    ├── budgets
    │
    ▼
Tool Execution Boundary
    │
    ├── registry
    ├── validation
    ├── authorization
    ├── approval
    ├── idempotency
    ├── timeout
    └── retry
    │
    ▼
Business / External Systems

整个执行过程
    │
    ├── trace/events
    ├── metrics
    └── eval dataset
            ↓
      failure analysis
            ↓
      before/after experiment
```

---

# Learning Sequence

## 001A — Eval Baseline

Teacher 提供最小 reference harness。

学习：
- execution path；
- structured trace；
- deterministic eval；
- runtime success vs task success；
- failure attribution。

当前入口：[`CURRENT_TASK.md`](./CURRENT_TASK.md)

Reference：

```text
guided_reference/001a/
├── baseline_agent.py
└── run_eval.py
```

## 001B — Failure Taxonomy & Regression

增加：
- model / harness / validation / tool / business failure taxonomy；
- aggregate metrics；
- regression cases；
- 第一次 before/after experiment。

## 001C — Reliable Tool Boundary

增加：
- typed/schema validation；
- retryable vs non-retryable；
- timeout；
- cancellation；
- side-effect classification。

## 001D — Approval & Idempotency

证明：
- dangerous action 未批准不会执行；
- approval 绑定具体 args；
- duplicate delivery 不重复业务副作用；
- timeout 后不能假设 tool 没执行。

## 001E — Run Control

增加：
- max_steps；
- token/cost budget；
- cancellation；
- runaway-loop detection。

## 001F — Persistent State & Crash Recovery

引入后端能力：
- database transaction；
- checkpoint；
- resume；
- process crash；
- stale worker；
- outbox / durable execution concepts。

## 001G — Production Observability

把内存 trace 演进成：
- trace / span / event mental model；
- latency distribution；
- tool error metrics；
- task success metrics；
- cost/token metrics；
- regression dashboard thinking。

---

# Learning Method

本实验采用 guided implementation：

```text
reference code
→ Teacher explanation
→ run / inspect
→ targeted modification
→ break it
→ tests/eval
→ review
```

不是要求把所有 boilerplate 从零写一遍。

但 retry/idempotency、failure classification、state transition、crash recovery 等关键逻辑会要求学习者自己修改或重写，因为这些才是真正值得形成工程能力的地方。

---

# What This Lab Is Preparing For

完成 Lab 001 后应该能够比较自然地理解：

- 为什么 Agent SDK 需要 harness；
- LangGraph 的 state/checkpoint 在解决什么；
- durable Agent 为什么需要传统分布式系统知识；
- eval 为什么必须进入开发循环；
- tool calling 为什么不是简单的“模型返回函数名然后调用”；
- 为什么生产 Agent 的 reliability 是模型 + harness + backend 共同决定的。

这些能力随后会接到 context/memory、durable agents、security、MCP/A2A 和 Agent Platform。
