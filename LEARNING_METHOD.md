# Learning Method

这个仓库采用 **guided reference implementation（带讲解的参考实现）+ targeted modification（关键修改）** 的学习方式。

目标不是训练“从空白文件手敲所有样板代码”的速度，而是在有限业余时间内，高密度建立 Production Agent Engineering 的 mental model、代码阅读能力、排错能力和系统设计能力。

## 为什么不用纯 blank-page 学习

当前学习者已经在实际 Agent 工程岗位工作，并且日常会使用 AI coding tools 参与真实项目。此时如果每个主题都要求从零搭目录、写数据类、补样板代码，学习成本很高，但很多时间消耗并不对应更高的工程理解。

因此默认不采用：

```text
看需求
→ 从空文件开始
→ 自己写全部 boilerplate
→ 写完再看答案
```

而采用：

```text
看架构问题
→ 阅读/重打一份高质量带注释 reference implementation
→ ChatGPT 逐段解释 execution path 和 design decision
→ 运行测试
→ 修改关键逻辑
→ 故意制造 failure
→ 排错
→ 用自己的话解释
→ 必要时重写少量核心模块
```

## 时间分配

默认大约：

- 50%：读懂真实代码、execution path、架构和 trade-off；
- 25%：自己修改 / 扩展 / debug；
- 15%：测试、failure experiment、trace 分析；
- 10%：从空白重写真正重要且值得形成肌肉记忆的核心代码。

比例不是固定规则，但原则是：**减少低价值样板代码，增加高价值判断和排错。**

## Reference Implementation 的要求

ChatGPT 提供的参考实现应尽量满足：

1. 规模可在一次或几次学习中读完；
2. 代码可以直接运行；
3. 对关键行写“为什么”，而不仅是“这行做什么”；
4. 明确指出 production code 中还缺什么；
5. 配套测试和 failure cases；
6. 不因为追求“高级”而加入无意义抽象；
7. 框架出现时，同时解释框架隐藏的底层机制。

## 学习者不是被动抄代码

“照着写一遍”只是第一遍建立代码地图，不算掌握。

一个主题至少还要经过下面几种动作中的若干项：

- 关闭参考答案后解释完整调用链；
- 修改一个需求；
- 修一个故意埋下的 bug；
- 新增测试；
- 预测一个 failure scenario 的结果；
- 比较两种实现的 trade-off；
- 删除一层框架并解释它原本替你做了什么；
- 把关键模块重新写一遍。

## 哪些内容仍应该自己从零写

以下代码通常值得自己写：

- 一个核心状态机；
- retry / idempotency 的关键决策逻辑；
- transaction boundary；
- concurrency control；
- eval evaluator；
- context assembly policy；
- authorization / approval policy；
- failure recovery 的核心步骤。

而下面内容通常不值得反复从零手写：

- 普通 dataclass / DTO boilerplate；
- 项目初始化样板；
- 重复 CRUD；
- 明显的 SDK 接线代码；
- 与当前学习目标无关的配置胶水。

## 最终验收标准

不以“代码是不是完全自己原创”判断是否掌握，而以这些问题判断：

- 你能不能读懂？
- 你能不能解释为什么这样设计？
- 需求变化时你能不能改？
- 出错时你能不能定位？
- 你能不能写测试证明自己的判断？
- 换一个框架后你还能不能迁移这些 mental model？

这才是本仓库希望形成的工程能力。
