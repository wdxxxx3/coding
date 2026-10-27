# M03 PPO 截断损失 · `PPO` `RL` `RLHF`

**入口（照念）**：「这是 PPO 的更新循环。」　**时长** 8–10 分钟

| 级别 | 问题 | 说明 |
|---|---|---|
| P0 | `logp_old` 在循环内用当前策略重算 | 实测 ratio 恒为 1，截断永远不会触发；多个 epoch 后变成没有约束的普通策略梯度，容易崩。`logp_old` 必须在**采样时**记录并冻结 |
| P0 | `torch.max` 应为 `torch.min` | PPO 取的是悲观下界。实测 A>0、ratio=1.5 时 max 返回 1.5A（不截断），min 才返回 1.2A |
| P2 | 没有 value loss、entropy、advantage 归一化 | 看候选人是否知道完整 PPO 还缺什么（不扣分，只看知识面） |

**追问 · 预研**：A<0 时截断在哪一侧起作用？PPO 截断和 KL 惩罚有什么区别？LLM 上为什么常把 value model 去掉（→ GRPO / RLOO）？
**追问 · 落地**：异步采样时，`logp_old` 应该来自哪个版本的策略（关联旧题库 R12）？训练中你会监控哪些量来判断 PPO 是否健康（clip fraction、approx KL、ratio 分位数）？

**锚点**：4 = 两个 P0 都找到，并能讲清 A 正负两种情况；3 = 找到一个 P0，第二个在提示下找到；2 = 能复述公式但看不出 bug；1 = 不理解 ratio
