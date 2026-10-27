# 两段式端到端：检测 -> 规划
det = detector(images)
boxes = gt_boxes if self.training else det.boxes
plan = planner(boxes, ego_state)       # ego_state = [v, a, yaw_rate, 导航指令]
loss = det_loss(det, gt) + plan_loss(plan, gt_traj)
# 评估：开环 L2 (1s/2s/3s) + 碰撞率，L2 明显优于基线
