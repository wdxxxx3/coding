# 右 padding；value_head 对每个位置输出一个标量
h = backbone(ids, attention_mask=attn).last_hidden_state     # [B, T, D]
r = value_head(h).squeeze(-1)[:, -1]                         # 取最后一个位置作为序列奖励
r_chosen, r_rejected = r[: B // 2], r[B // 2 :]
loss = -torch.log(torch.sigmoid(r_chosen - r_rejected)).mean()
