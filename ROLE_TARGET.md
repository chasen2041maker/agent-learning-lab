# Role Target — Big-Tech Standard Agent Engineer

> Baseline date: 2026-08-26

本仓库的目标不是“会做 RAG / 会用 LangChain / LangGraph”的应用开发者，而是逐步接近大厂当前真实招聘中的以下能力方向：

- Production Agent Engineer
- Applied AI Engineer
- Agent Systems / Harness Engineer
- Agent Runtime / Platform Engineer

## 当前已有经验：默认加速处理

以下内容不再作为从零主课程：

- RAG 基本流程
- Agent 基本概念
- LangChain
- LangGraph
- 基础 tool calling / workflow 使用

这些能力在后续项目中继续使用，但只有遇到明确知识缺口时再回补。

## 当前大厂岗位反复出现的能力

基于 2026-08-26 仍在招聘的 OpenAI / Anthropic Agent 相关岗位，核心能力集中在：

### 1. Agent harness / runtime

- core execution loop
- tool execution
- state / orchestration
- long-horizon workflows
- sandbox / isolation
- memory / context
- safe action execution

### 2. Evals / experimentation

- task success metrics
- regression evals
- trajectory analysis
- graders
- ablation experiments
- failure-mode taxonomy
- production feedback loops

### 3. Production reliability

- timeout / cancellation
- retry semantics
- idempotency
- crash recovery
- durable workflows
- observability / diagnostics
- reproducibility

### 4. Performance engineering

必须同时关注：

```text
quality / solve rate
latency
tokens
cost
reliability
capacity
```

不能只看“回答是否看起来不错”。

### 5. Backend / distributed systems

Agent 系统进入生产后，本质上会大量遇到传统后端和分布式系统问题：

- API / RPC
- database / transaction
- queue
- distributed state
- concurrency
- permissions / identity
- cloud runtime
- observability

### 6. Security

- sandboxing
- least privilege
- secrets
- tool authorization
- approval
- prompt / tool injection
- auditability

## 学习策略

因此仓库不按下面方式推进：

```text
RAG → LangChain → LangGraph → CrewAI → 再换一个框架
```

而按：

```text
已有 Agent 能力
        ↓
Eval + failure analysis
        ↓
Reliable tool/runtime semantics
        ↓
Context / memory engineering
        ↓
Durable long-running agents
        ↓
Sandbox / identity / security
        ↓
MCP / A2A interoperability
        ↓
Production observability + performance
        ↓
Agent platform / advanced systems
```

框架作为实现工具，能力模型不绑定任何单一框架。

## 当前参考岗位

- OpenAI — Applied AI Engineer, Codex Core Agent
- OpenAI — AI Systems Engineer, Codex Agents
- OpenAI — Software Engineer, API Agents
- OpenAI — Software Engineer, Cloud Agents
- OpenAI — Software Engineer, Enterprise AI Platform
- Anthropic — Agent Runtime Platform / AI Reliability related roles

这些岗位共同说明：大厂 Agent Engineer 的差异化不在“是否会调用 Agent framework”，而在能否把模型能力转化为**可测量、可调试、可靠、安全、经济可行的生产系统**。
