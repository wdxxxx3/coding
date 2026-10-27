# 评估世界模型 2 秒（20 帧）预测质量。obs: [B, 21, ...]，actions[:, t] 是在 obs[:, t] 时刻执行的动作
z = wm.encode(obs[:, 0])
errs = []
for t in range(20):
    z = wm.posterior(z, actions[:, t + 1], obs[:, t + 1])
    errs.append(F.mse_loss(wm.decode(z), obs[:, t + 1]))
report("2s rollout MSE", torch.stack(errs).mean())
