# batch 生成，左 padding；RoPE 使用 position_ids
attn = (ids != pad_id).long()                              # [B, T]
pos = torch.arange(ids.shape[1]).expand_as(ids)
out = model(ids, attention_mask=attn, position_ids=pos, use_cache=True)
# 之后每步：
next_pos = pos[:, -1:] + 1
