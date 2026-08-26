# Engineering Principles

这份文件定义本仓库长期不轻易改变的学习与工程原则。

## 职业目标

目标不是停留在“会调用模型 API / 会使用某个 Agent 框架”的开发者，而是逐步形成以下方向的能力：

- Production Agent Engineer
- Applied AI Engineer
- Agent Runtime / Platform Engineer

核心能力组合：

```text
AI / model understanding
        +
Agent architecture
        +
Backend engineering
        +
Distributed systems
        +
Reliability
        +
Evaluation / Observability
        +
Security
        +
System design
```

职位名称和框架会变化，底层问题不会轻易消失。

## 抗技术迭代原则

### 1. 学框架，但不把能力绑定到框架

可以学习 OpenAI Agents SDK、LangGraph、Claude Agent SDK、Vercel AI SDK 等，但必须继续追问：

- state 在哪里？
- context 如何构造？
- tool 为什么可以被调用？
- retry 由谁负责？
- side effect 如何避免重复？
- pause / resume 怎么实现？
- failure 如何被观察和恢复？

框架变化时，这些 mental model 可以迁移。

### 2. 学协议，但重点理解协议解决的问题

例如 MCP / A2A 不只是记 API，而是理解：

- capability discovery
- remote invocation
- identity / authorization
- trust boundary
- versioning
- failure semantics
- interoperability

未来协议变化时，应能判断新协议解决了什么旧问题，而不是重新从零学习。

### 3. 模型更强，不等于工程问题消失

即使模型未来拥有更强的 planning、reasoning 和 autonomous capability，生产系统仍然需要处理：

- 权限
- 状态
- 数据
- transaction
- idempotency
- timeout / cancellation
- cost / latency
- observability
- eval
- security
- failure recovery

因此 Backend / Distributed Systems 是 Agent Engineering 的长期支撑能力，而不是旁支。

### 4. 优先学习“难被封装掉”的能力

优先级高：

- runtime semantics
- context engineering
- tool execution boundary
- durability
- eval methodology
- observability
- security / authorization
- distributed state
- model / cost / latency trade-off

优先级低：

- 单纯记框架 API
- 没有实验支撑的 Prompt 技巧
- 只为了追热点而更换框架
- 无法说明收益的 multi-agent 复杂度

## 新技术进入仓库的标准

面对一个新框架、新协议、新模型能力，先回答：

1. 它解决的工程问题是什么？
2. 它改变了已有 mental model，还是只是新的 API？
3. 它是否已经产生真实生产价值或形成重要生态趋势？
4. 能否通过小实验验证？
5. 学会以后能否迁移到其他实现？

根据结果进入：

```text
IGNORE → WATCH → TRIAL → ADOPT
```

仓库追求的是持续升级的工程能力，而不是持续增长的技术名词数量。
