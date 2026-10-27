# reward: [B*G]，每个 prompt 连续采样 G 条；logp / ref_logp / mask: [B*G, T]
adv = (reward - reward.mean()) / reward.std()
ratio = torch.exp(logp - logp_old)
pg = -(ratio * adv[:, None])
kl = torch.exp(logp - ref_logp) - (logp - ref_logp) - 1      # k3 估计
loss = (((pg + beta * kl) * mask).sum(-1) / mask.sum(-1)).mean()
