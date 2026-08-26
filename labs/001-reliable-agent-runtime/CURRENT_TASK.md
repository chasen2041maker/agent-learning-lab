# Current Task — 001A: Agent Eval Baseline

> Mode: guided reference implementation
>
> 当前不是从零写 Agent，而是 **读懂 → 运行 → 看 trace → 判断 failure**。

## Why

你已经会 RAG、LangChain、LangGraph 和基础 Agent 开发。

现在第一优先级不是再学一个 framework，而是建立一个大厂 Agent Engineer 非常核心的习惯：

> **先定义怎么测，再讨论怎么改。**

Agent 输出“看起来不错”不是工程证据。生产环境需要知道：

- task 到底成功没有；
- 哪一步失败；
- 是 model、tool、context 还是 harness；
- 修改以后 solve rate 是否真的提高；
- 提高的同时 latency / cost 是否恶化。

本课只建立第一层 eval mental model。

---

# Reference Code

本轮直接使用 Teacher 提供的带注释代码：

```text
guided_reference/001a/
├── agent_runtime/
│   └── __init__.py
├── baseline_agent.py
└── run_eval.py
```

重点文件：

1. `baseline_agent.py`
   - contracts
   - mock tools
   - deterministic fake model
   - minimal agent harness
   - trace events

2. `run_eval.py`
   - eval cases
   - deterministic grader
   - trace inspection
   - baseline pass rate

第一遍允许照着代码重新打一遍，也可以直接运行仓库版本。

---

# Mental Model

先只记住这条链：

```text
User Task
   ↓
Model Decision
   ↓
Harness
   ↓
Tool Registry
   ↓
Validation
   ↓
Tool Execution
   ↓
Tool Result
   ↓
Model Final Answer
```

旁边还有一条非常重要的链：

```text
每一步
  ↓
Trace Event
  ↓
Evaluator
  ↓
Pass / Fail + Failure Reason
```

没有第二条链，你通常只能“看输出猜 Agent 好不好”。

---

# Step 1 — Run It

进入：

```text
labs/001-reliable-agent-runtime/guided_reference/001a
```

运行：

```bash
python run_eval.py
```

当前 baseline 预期：

```text
4 / 6 PASS
2 / 6 FAIL
```

如果不是这个结果，先不要继续改代码，回来告诉 Teacher 实际输出。

---

# Step 2 — 找出两个真正失败的 case

不要先看“怎么修”。

先根据输出和 trace 判断：

1. 哪两个 case 没通过？
2. 每个 case 在 execution path 的哪一层开始偏离预期？
3. runtime status 是否一定等于 task success？

特别观察：

```text
read_unseen_ticket_id
```

这里会出现一个很重要的现象：

> runtime 可以 SUCCESS，但任务本身仍然 FAIL。

这是 Agent eval 和普通 API health check 很大的区别。

---

# Step 3 — 读懂这 6 个对象/边界

暂时不用背代码，只需要能够用自己的话解释：

- `ModelDecision`
- `ToolSpec`
- `TraceEvent`
- `RunResult`
- `TOOL_REGISTRY`
- `AgentRunner.run()`

重点不是 Python 语法，而是：

> 每一个对象在 Agent execution lifecycle 中负责表达什么事实？

---

# Step 4 — 回来和 Teacher 对话

完成运行后，不需要马上自己改。

直接告诉 ChatGPT：

> **001A 跑完了，结果是 X/6，开始给我讲。**

最好把你认为失败的两个 case 名字一起说出来。

Teacher 下一步会：

1. 按真实执行顺序逐段讲 `baseline_agent.py`；
2. 讲 runtime success vs task success；
3. 讲 deterministic evaluator 为什么比一上来 LLM-as-judge 更重要；
4. 让你自己修改一个 failure taxonomy；
5. 再做第一次 before/after eval。

---

# 当前不要做

为了控制学习边界，本轮先不要：

- 接真实 LLM；
- 改成 LangGraph；
- 加 retry；
- 加 idempotency；
- 加数据库；
- 加 MCP；
- 引入 observability SaaS；
- 优化那两个失败 case。

先学会**读取一次 Agent execution，并用 eval 证明它哪里失败**。

---

# Pass Criteria for 001A-Read

这一小步通过只需要：

- 能运行 baseline；
- 得到预期结果；
- 能找到两个 failing cases；
- 能从 trace 大概说出 failure 发生在哪里；
- 能解释为什么 `RunStatus.SUCCESS` 不等于“用户任务成功”。

通过后进入：

**001A-Modify — Failure Taxonomy + Before/After Eval**。
