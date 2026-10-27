for epoch in range(4):
    for mb in minibatches(buffer):
        logp_old = policy.log_prob(mb.obs, mb.act).detach()
        logp = policy.log_prob(mb.obs, mb.act)
        ratio = torch.exp(logp - logp_old)
        surr1 = ratio * mb.adv
        surr2 = ratio.clamp(1 - 0.2, 1 + 0.2) * mb.adv
        loss = -torch.max(surr1, surr2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
