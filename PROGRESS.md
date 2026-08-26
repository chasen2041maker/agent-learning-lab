# Progress

> Started: 2026-08-26

这个文件记录“能力证据”，不是视频/章节进度。

## Status

- `ASSUMED`：根据已有工作/学习经验认为接触过，但尚未在本仓库验证；
- `LEARNING`：正在学习或实验；
- `REVIEW`：基本掌握，但仍存在关键缺口；
- `PASSED`：通过代码、测试、eval、debug 或设计题验证；
- `REVISIT`：以前通过，但技术或能力需要重新验证。

---

# Current Focus

**Phase 1 — Agent Evals & Failure Analysis**

当前任务入口：

[`labs/001-reliable-agent-runtime/CURRENT_TASK.md`](./labs/001-reliable-agent-runtime/CURRENT_TASK.md)

目标不是重新学习 LangGraph，而是建立下面这个能力：

> 面对一次 Agent failure，能够用 trace + eval 证据判断问题来自 model、context、retrieval、tool 还是 harness，并验证修改是否真的提高系统表现。

---

# Agent Engineering Skill Matrix

| Capability | Status | Current evidence / note |
|---|---|---|
| Python for Agent systems | ASSUMED | 有实际开发经验，待任务验证 |
| RAG fundamentals | ASSUMED | 已有学习/实现经验，不重走入门 |
| LangChain | ASSUMED | 已使用，不作为主课程 |
| LangGraph | ASSUMED | 已使用，不作为主课程 |
| Tool calling / workflow | ASSUMED | 已接触，后续从 production semantics 验证 |
| Agent eval methodology | LEARNING | Phase 1 |
| Agent failure taxonomy | LEARNING | Phase 1 |
| Trajectory / trace analysis | LEARNING | Phase 1 |
| Reliable agent harness | TODO | Phase 2 |
| Timeout / retry semantics | TODO | Phase 2 |
| Idempotent side effects | TODO | Phase 2/3 |
| Context engineering | TODO | Phase 4 |
| Memory engineering | TODO | Phase 4 |
| Advanced retrieval diagnosis | ASSUMED | 有 RAG 基础，Phase 5 重做 eval-based verification |
| Durable execution | TODO | Phase 6 |
| Long-running agent recovery | TODO | Phase 6 |
| Agent security / threat modeling | TODO | Phase 7 |
| Sandbox / isolation | TODO | Phase 7 |
| MCP 2026 | TODO | Phase 8 |
| A2A interoperability | TODO | Phase 8 |
| Model routing / cost / latency | TODO | Phase 9 |
| Multi-agent trade-offs | TODO | Phase 10 |
| Agent platform architecture | TODO | Phase 11 |

---

# Backend Support Skill Matrix

这些能力根据 Agent 系统实际需求验证和补齐。

| Capability | Status | Agent relevance |
|---|---|---|
| HTTP / API lifecycle | ASSUMED | model/tool/MCP remote calls |
| async / concurrency | ASSUMED | parallel calls / cancellation |
| timeout / cancellation | LEARNING | bounded agent execution |
| error semantics | LEARNING | retry/failure classification |
| SQL / transaction | TODO | run state / side effects |
| idempotency | TODO | safe retry |
| Redis / cache | TODO | state/cache/coordination |
| queue semantics | TODO | durable async work |
| lease / heartbeat | TODO | worker ownership / recovery |
| authn / authz | TODO | tool/agent permissions |
| structured logging | LEARNING | trace/failure diagnosis |
| metrics / tracing | LEARNING | eval + production observability |
| Docker / process isolation | TODO | sandbox |
| Kubernetes / distributed runtime | TODO | agent platform scale |

---

# Evidence Log

目前尚无 `PASSED` 项。

以后只记录真实证据，例如：

```text
2026-xx-xx  PASSED — Agent failure taxonomy
Evidence:
- 30-case regression set
- failures labelled model/context/tool/harness
- evaluator tests pass
- one production-style trace independently diagnosed
- before/after experiment showed measurable improvement
```

---

# Teacher Tracking Rule

每次任务完成后，ChatGPT 直接审查仓库，并执行：

1. 判断 `PASSED / REVIEW / NOT PASSED`；
2. 把有效 evidence 写入本文件；
3. 更新相关 skill status；
4. 记录仍暴露的知识缺口；
5. 修改当前任务；
6. 只有当前任务通过后再推进下一核心任务。

不会因为“代码跑通”自动标记 PASSED。

---

# Passing Rule

一个核心能力通常需要满足至少 4 项：

1. 能解释 mental model；
2. 能读懂 reference / production-style implementation；
3. 能修改关键逻辑；
4. 能写或修改测试/eval；
5. 能独立定位 failure；
6. 能分析 trade-off；
7. 换框架仍能迁移理解；
8. 能回答对应 system design 问题。
