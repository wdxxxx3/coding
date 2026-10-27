# 智驾算法岗代码面试题库（AI 时代版）

面向 L4 重卡自动驾驶算法岗的**校招代码面试**，单场 45 分钟。**候选人不需要写代码**：读陌生代码、找问题、审核改动、从日志定位问题，并说清楚后果。

> ⚠️ 本仓库包含面试答案，请保持**私有**，只对面试官开放。

## 先读这些
| 文档 | 内容 |
|---|---|
| [docs/01-analysis.md](docs/01-analysis.md) | 为什么不再以力扣为主，各种面试形式的对比，关于"用 AI 辅助写代码"和"做 diff 平台"的建议 |
| [docs/02-interview-flow.md](docs/02-interview-flow.md) | 45 分钟流程、开场话术、追问技巧 |
| [docs/03-rubric.md](docs/03-rubric.md) | 五维评分标准、结论线、可信度标记 |
| [docs/04-interviewer-training.md](docs/04-interviewer-training.md) | 面试官培训流程、疑似作弊的处理、题目保密 |
| [templates/feedback-form.md](templates/feedback-form.md) | 面试反馈表 |

## 题目一览

| 题号 | 题目 | 形式 | 方向 | 语言 | 难度 | 时长 |
|---|---|---|---|---|---|---|
| [Q01](questions/q01-heading/interviewer.md) | 航向角工具函数 | 阅读 + 找错 | 通用 / 规控 | Python | ★★ | 12–15′ |
| [Q02](questions/q02-bev-nms/interviewer.md) | BEV 框 IoU 与 NMS | 找错 | 感知 | C++ | ★★ | 15′ |
| [Q03](questions/q03-kf-diff/interviewer.md) | 前车跟踪滤波器 PR | Diff 审核 | 融合 / 规控 | C++ | ★★★ | 18′ |
| [Q04](questions/q04-pure-pursuit/interviewer.md) | 横向控制器 | 陌生代码讲解 | 规控 | Python | ★★ | 15′ |
| [Q05](questions/q05-pose-buffer/interviewer.md) | 位姿缓存与运动补偿 | 找错 + 并发 | 定位 / 感知 | C++ | ★★★ | 15–18′ |
| [Q06](questions/q06-augment-diff/interviewer.md) | 3D 检测数据增强 PR | Diff 审核 | 感知（DL） | Python | ★★ | 15′ |
| [Q07](questions/q07-transform/interviewer.md) | 坐标变换 | 找错 + 测试设计 | 通用 | Python | ★★ | 12–15′ |
| [Q08](questions/q08-acc-refactor/interviewer.md) | ACC 跟车逻辑 | 口述重构 | 规控 | Python | ★★★ | 18–20′ |
| [Q09](questions/q09-voxel/interviewer.md) | 点云体素下采样 | 找错 | 感知 | C++ | ★★★ | 15′ |
| [Q10](questions/q10-ai-frenet/interviewer.md) | 审核 AI 写的 Frenet 转换 | AI 代码审核 | 规控 / 预测 | Python | ★★★ | 18′ |
| [Q11](questions/q11-log-ghost-brake/interviewer.md) | 无前车急减速 | 日志推理 | 通用 | 无代码 | ★★★ | 15–18′ |
| [Q12](questions/q12-pid-diff/interviewer.md) | 纵向 PID PR | Diff 审核 | 控制 | C++ | ★★ | 15′ |
| [M1–M6](questions/mini-coding.md) | 微型手写题 | 当面手写 + 改需求 | 通用 | 任意 | ★ | ≤10′ |

每道题的目录结构：
```
qXX-name/
  candidate/        ← 只把这里的内容展示给候选人（面试中再展示，不要提前发送）
  interviewer.md    ← 答案、提示阶梯、追问树、现场变体、评分锚点（不要给候选人看）
```

## 组卷方案（每场 2 道主题，形式不同）

| 方向 | 题 A（阅读 / 找错） | 题 B（Diff / 日志 / AI 审核） | 备选 |
|---|---|---|---|
| 感知（点云） | Q09 | Q06 | Q02、Q11 |
| 感知（视觉 / DL） | Q02 | Q06 | Q07、Q11 |
| 规划 / 预测 | Q01 | Q10 | Q08、Q11 |
| 控制 | Q04 | Q12 | Q01、Q03 |
| 融合 / 定位 | Q05 | Q03 | Q07、Q11 |
| 通用 / 不确定方向 | Q07 | Q11 | Q01、Q10 |

同一位候选人的多轮面试之间不要重复题目；终面验证时，可以抽前面轮次的题目换一个变体。

## 题目的验证
所有题目中埋的问题都已经实际运行验证过（Python 脚本、C++ 配合 AddressSanitizer / UBSan、卡尔曼滤波仿真）。各题 `interviewer.md` 中标注"实测"的数字均来自这些运行结果。

## 维护
- 新题优先来自团队真实的 bug 和事故复盘（脱敏后），按 `questions/` 现有格式添加
- 每季度回顾每道题的分数分布，区分度低的题淘汰或改写
