# 路测问题单 #2317：高速无前车急减速

**场景**：重卡满载，高速最右车道，ACC 巡航 80 km/h。天气晴，平直路段。
**现象**：车辆无明显原因减速，减速度约 -3 m/s²，持续约 0.6 s 后恢复。安全员反馈"前方没有车"，
后车距离较近，有追尾风险。同一路段上周也出现过一次。

**传感器配置**：前向毫米波雷达（无俯仰角测量），前视相机（有效检测距离约 150 m），无激光雷达参与此功能。
**融合规则**：仅雷达检测到的目标，置信度随连续检测帧数上升，≥ 0.5 发布给规划。

## 日志片段（ego speed = 80 km/h）

```
t=1203.40 [radar]   obj#57 range=142.3m rel_v=-22.1m/s az=0.3deg rcs=28dBsm
t=1203.40 [camera]  no object in ego lane within 150m
t=1203.40 [fusion]  obj#57 src=RADAR_ONLY conf=0.42 -> not published
t=1203.50 [radar]   obj#57 range=140.1m rel_v=-22.2m/s az=0.2deg rcs=29dBsm
t=1203.50 [fusion]  obj#57 src=RADAR_ONLY conf=0.48 -> not published
t=1203.60 [radar]   obj#57 range=137.9m rel_v=-22.2m/s az=0.2deg rcs=30dBsm
t=1203.60 [camera]  no object in ego lane within 150m
t=1203.60 [fusion]  obj#57 src=RADAR_ONLY conf=0.53 -> published lane=EGO type=UNKNOWN
t=1203.60 [planner] CIPV=obj#57 dist=137.9m ttc=6.2s -> decel request -3.0 m/s^2
t=1203.70 [radar]   obj#57 range=135.7m rel_v=-22.2m/s az=0.2deg rcs=31dBsm
...
t=1204.10 [radar]   obj#57 range=126.9m rel_v=-22.1m/s az=0.1deg rcs=24dBsm
t=1204.20 [radar]   obj#57 range=124.8m rel_v=-22.1m/s az=0.1deg rcs=17dBsm
t=1204.20 [camera]  no object in ego lane within 150m
t=1204.20 [fusion]  obj#57 conf=0.47 -> dropped
t=1204.20 [planner] CIPV=none -> resume cruise
```

## 问题
1. obj#57 最可能是什么？请说出你的推理依据（尽量用日志里的数字）。
2. 感知、融合、规划三个环节，各自有什么值得改进的地方？
3. 如果直接"过滤掉所有仅雷达检测到的静止目标"，会有什么风险？对重卡来说为什么尤其严重？
4. 你会怎么修？修完之后怎么证明修好了，并且没有引入新问题？
