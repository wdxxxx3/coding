# 轨迹扩散：x0 = 未来 H=8 个点 (x,y) 展平为 [B, 16]；模型设计为预测噪声 eps
t = torch.randint(0, T, (B,))
noise = torch.randn_like(x0)
xt = alpha_bar[t].sqrt() * x0 + (1 - alpha_bar[t]).sqrt() * noise
loss = F.mse_loss(model(xt, t, cond), x0)

# 推理时 classifier-free guidance
eps = model(x, t, null_cond) + w * (model(x, t, cond) - model(x, t, null_cond))
