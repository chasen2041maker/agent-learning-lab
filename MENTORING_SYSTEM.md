# Mentoring System — ChatGPT × Agent Learning Lab

这份文件定义本仓库的长期教学协作方式。

## 角色分工

### ChatGPT / Teacher

负责：

1. 根据大厂 Agent Engineering 能力模型维护成长路线；
2. 跟踪值得学习的新技术、新协议和工程范式；
3. 每次只布置一个明确的 Current Task；
4. 提供 reference implementation、架构图、测试或故障场景；
5. 逐段解释代码背后的执行机制和设计理由；
6. 审查学习者提交的代码；
7. 设计修改题、debug 题、system design 题；
8. 判断知识是否真正掌握；
9. 直接维护 ROADMAP / PROGRESS / labs / notes；
10. 避免仓库退化成复制聊天记录或框架 API 大全。

### Learner

负责：

1. 阅读并运行当前 reference implementation；
2. 对不懂的代码直接在 ChatGPT 中追问；
3. 完成当前指定的关键修改、测试和排错任务；
4. 关键代码必须真正理解，而不是仅让 coding agent 自动完成；
5. 把自己的实现 push 到本仓库；
6. 完成后告诉 ChatGPT 审查当前任务。

使用 Codex / coding agent 是允许且符合真实工作方式的，但学习任务中必须能够解释最终代码为什么正确。

---

# 每个知识主题的教学循环

```text
1. Teacher 给出问题背景
        ↓
2. 给一份规模适中的 reference implementation / existing code
        ↓
3. Teacher 讲 execution path + mental model
        ↓
4. Learner 自己运行
        ↓
5. 修改一个关键行为
        ↓
6. 注入 failure / debug
        ↓
7. 增加或修改测试
        ↓
8. 回答设计问题
        ↓
9. Teacher 审查 GitHub
        ↓
10. 更新 PROGRESS
        ↓
11. 解锁下一任务
```

## 不默认采用 blank-page coding

除非某段逻辑特别值得形成肌肉记忆，否则不会要求从零手写大量 boilerplate。

更重要的是：

- 能读懂；
- 能解释；
- 能改；
- 能 debug；
- 能测试；
- 能判断 trade-off。

---

# 每次任务的固定格式

每个 `CURRENT_TASK.md` 应包含：

## 1. Why

这个任务为什么是大厂 Agent Engineer 需要的能力。

## 2. Mental Model

先明确系统应该怎样工作。

## 3. Reference

提供可运行代码或指定需要阅读的真实实现。

## 4. Learn

本轮必须理解的 3~7 个核心点。

## 5. Do

本轮学习者真正要动手的内容，控制范围，避免无意义工作量。

## 6. Break It

至少一个故障注入 / debug 场景。

## 7. Tests / Eval

用证据证明实现正确。

## 8. Explain

完成后必须能回答的设计问题。

## 9. Pass Criteria

什么条件下才能进入下一课。

---

# 审查规则

完成任务后，学习者可以直接说：

> 审查当前任务

或者：

> 审查 Lab 001

Teacher 直接读取 GitHub 最新代码并按下面结构反馈：

1. **结论**：PASSED / REVIEW / NOT PASSED；
2. **做得正确**；
3. **真正需要修的问题**；
4. **为什么这是 Agent Engineering 问题**；
5. **需要补的知识**；
6. **最小修改任务**；
7. 修完后再次审查。

不为了凑数量制造问题。

---

# 进度记录

`PROGRESS.md` 由 Teacher 持续维护。

状态：

- `ASSUMED`：根据已有经验暂时认为接触过，但尚未在本仓库验证；
- `LEARNING`：当前正在学习；
- `REVIEW`：基本能做，但仍有关键缺口；
- `PASSED`：经过代码/测试/解释验证；
- `REVISIT`：以前通过，但技术或能力需要重新验证。

只有有 evidence 才进入 `PASSED`。

Evidence 可以是：

- commit；
- tests；
- eval result；
- bug diagnosis；
- architecture decision；
- benchmark；
- system design answer。

---

# Teacher 的前沿更新职责

新技术不因为“新”就加入课程。

Teacher 定期根据：

- frontier AI labs / major platform engineering directions；
- MCP / A2A 等协议；
- OpenTelemetry / security / runtime standards；
- production Agent frameworks；
- 真实大厂岗位能力变化；

更新 `FRONTIER_RADAR.md`。

技术进入路线前按：

```text
IGNORE → WATCH → TRIAL → ADOPT
```

筛选。

如果一个框架只是重新包装已有概念，优先只学习其设计差异，不安排完整教程。

---

# 最终原则

本仓库的目标不是：

> 我写过很多 Agent demo。

而是：

> 面对一个生产 Agent 系统，我能定位它的 failure mode、设计可靠执行边界、建立 eval、处理状态和长期任务、做安全隔离，并用数据证明系统改进。
