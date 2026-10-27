# 动作 = (纵向加速度 m/s^2, 曲率 1/m)，离散成 256 个 token
lo = train_actions.min(0).values; hi = train_actions.max(0).values

def tokenize(a, n_bins=256):
    return ((a - lo) / (hi - lo) * n_bins).long()             # 0..255

def detokenize(tok, n_bins=256):
    return tok.float() / n_bins * (hi - lo) + lo
