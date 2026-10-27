# 二分类 focal loss；targets 为 0/1；num_pos = 本 batch 正样本数
p = torch.sigmoid(logits)
ce = -(targets * torch.log(p) + (1 - targets) * torch.log(1 - p))
pt = p * targets + (1 - p) * (1 - targets)
loss = (alpha * (1 - pt) ** gamma * ce).sum() / num_pos
