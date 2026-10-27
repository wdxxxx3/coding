q = qnet(s).gather(1, a[:, None]).squeeze(1)
q_next = qnet(s2).max(1).values
target = r + gamma * q_next * (1 - done)       # done = 碰撞 or 超时
loss = F.smooth_l1_loss(q, target)
opt.zero_grad(); loss.backward(); opt.step()
