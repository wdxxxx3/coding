# 约定：t=0 为噪声，t=1 为数据；推理从噪声出发，按 x += dt * v 积分到 t=1
x1 = actions                                   # 数据 [B, H, A]
x0 = torch.randn_like(x1)                      # 噪声
t = torch.rand(B, 1, 1)
xt = t * x0 + (1 - t) * x1
v_target = x1 - x0
loss = ((model(xt, t, obs) - v_target) ** 2).mean()
