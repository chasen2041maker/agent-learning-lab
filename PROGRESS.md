# Progress

> Started: 2026-08-26

这个文件记录的是“能力进度”，不是视频/章节进度。

状态：
- `TODO`：尚未开始；
- `LEARNING`：正在学习或实验；
- `REVIEW`：能实现，但解释/稳定性还不够；
- `PASSED`：通过代码、测试和解释验证；
- `REVISIT`：以前会，但需要重新验证。

## Current Focus

| Area | Status | Evidence |
|---|---|---|
| Reliable Agent Runtime | LEARNING | Lab 001 |
| Context / Memory Engineering | TODO | — |
| MCP 2026 | TODO | — |
| A2A 1.0 | TODO | — |
| Durable Execution | TODO | — |
| Agent Evals | TODO | — |
| Agent Observability | TODO | — |
| Agent Security | TODO | — |
| Advanced Retrieval | REVISIT | later evaluation-focused lab |
| Multi-agent | TODO | — |
| Model / Cost / Latency Strategy | TODO | — |

## Backend Support Skills

这些能力只在 Agent 工程中真正用到时深入补齐。

| Skill | Status | Why it matters to agents |
|---|---|---|
| HTTP request lifecycle | REVISIT | remote tools, MCP/A2A, streaming |
| timeout / cancellation | LEARNING | prevent stuck runs |
| retry | LEARNING | transient model/tool failures |
| idempotency | LEARNING | safe side-effect retries |
| database transactions | TODO | persistent state / tool actions |
| queue semantics | TODO | durable tasks / async tools |
| concurrency / async | REVISIT | parallel tool execution |
| auth / authorization | TODO | tool and agent trust boundaries |
| tracing | LEARNING | agent trajectory debugging |
| Docker / sandbox isolation | TODO | safe code/tool execution |
| Kubernetes / distributed runtime | TODO | scale long-running services |

## Completed Evidence

暂空。

这里以后只记录真正通过的证据，例如：

```text
2026-xx-xx  PASSED idempotent tool execution
- implemented idempotency key store
- concurrent duplicate test passed
- crash-after-commit scenario explained
- retry does not duplicate business side effect
```

## Learning Rule

一个主题只有同时满足下面至少三项，才能进入 `PASSED`：

1. 能用自己的话解释；
2. 能独立写出关键实现；
3. 有测试或实验；
4. 能解释 failure mode；
5. 能比较至少两种方案及 trade-off；
6. 能把它用到一个真实 Agent 系统设计中。
