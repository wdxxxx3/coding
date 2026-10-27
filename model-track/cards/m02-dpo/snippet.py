def seq_logp(model, ids, resp_mask):                 # resp_mask: response 位置为 1
    logits = model(ids).logits
    logp = logits.log_softmax(-1).gather(-1, ids.unsqueeze(-1)).squeeze(-1)
    return (logp * resp_mask).sum(-1) / resp_mask.sum(-1)

def dpo_loss(policy, ref, b, beta=0.1):
    pc = seq_logp(policy, b.chosen, b.chosen_mask)
    pr = seq_logp(policy, b.rejected, b.rejected_mask)
    rc = seq_logp(ref, b.chosen, b.chosen_mask)
    rr = seq_logp(ref, b.rejected, b.rejected_mask)
    return -F.logsigmoid(beta * ((pc - pr) - (rc - rr))).mean()
