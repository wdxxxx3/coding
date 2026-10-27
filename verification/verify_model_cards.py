"""Reproduce the planted issues in model-track cards. Requires torch (CPU is fine)."""
import math
import torch
import torch.nn.functional as F

torch.manual_seed(0)

print("== M01 SFT: pad_id == eos_id masks the real EOS label")
eos = pad = 2
ids = torch.tensor([[5, 6, 7, 8, eos, pad, pad]])   # prompt 5,6 | response 7,8,eos | pad
labels = ids.clone(); labels[ids == pad] = -100
print("labels:", labels.tolist(), "-> EOS supervised?", bool((labels == eos).any()))

print("== M03 PPO: logp_old recomputed inside loop -> ratio is always 1; max() never clips")
lp = torch.tensor([-1.0, -2.0], requires_grad=True)
ratio = torch.exp(lp - lp.detach())
print("ratio:", ratio.tolist())
r, A = torch.tensor(1.5), torch.tensor(1.0)
print("adv>0, ratio=1.5: max ->", torch.max(r * A, r.clamp(0.8, 1.2) * A).item(),
      " min ->", torch.min(r * A, r.clamp(0.8, 1.2) * A).item())

print("== M04 GRPO: global normalisation vs per-group; k3 direction")
reward = torch.tensor([1., 1., 1., 1., 0., 1., 0., 1.])   # G=4, group0 all equal
glob = (reward - reward.mean()) / reward.std()
g = reward.view(2, 4); per = ((g - g.mean(1, keepdim=True)) / (g.std(1, keepdim=True) + 1e-6)).view(-1)
print("global adv group0:", [round(x, 3) for x in glob[:4].tolist()], " per-group:", per[:4].tolist())
same = torch.ones(8); print("all rewards equal -> adv:", ((same - same.mean()) / same.std())[:2].tolist())
# KL(pi||ref), pi=N(0,1) ref=N(1,1): true KL = 0.5
x = torch.randn(2_000_000)
logp = -0.5 * x**2; ref = -0.5 * (x - 1) ** 2
k3 = torch.exp(ref - logp) - (ref - logp) - 1
bad = torch.exp(logp - ref) - (logp - ref) - 1
print("true KL=0.5  correct k3=%.3f  snippet's version=%.3f" % (k3.mean(), bad.mean()))

print("== M05 RM: right padding -> index -1 reads a pad position; log(sigmoid) underflow")
attn = torch.tensor([[1, 1, 1, 0, 0], [1, 1, 1, 1, 1]])
last = attn.sum(1) - 1
print("snippet reads position 4 for both; real last tokens:", last.tolist())
d = torch.tensor([-120.0])
print("log(sigmoid(-120)) =", torch.log(torch.sigmoid(d)).item(), " logsigmoid =", F.logsigmoid(d).item())

print("== M06 VLM: 1 placeholder per image but 256 tokens per image")
emb = torch.zeros(1, 10, 4); ids6 = torch.zeros(1, 10, dtype=torch.long); ids6[0, 3] = 99
try:
    emb[ids6 == 99] = torch.ones(1, 256, 4).flatten(0, 1)
except Exception as e:
    print("error:", type(e).__name__, str(e).splitlines()[0][:90])

print("== M07 VLA bins")
lo, hi = torch.tensor([-5., -0.2]), torch.tensor([5., 0.2])
a = torch.tensor([[5., 0.2], [0.03, 0.0]])
tok = ((a - lo) / (hi - lo) * 256).long()
print("tokenize(hi) =", tok[0].tolist(), "(valid range 0..255)")
back = tok[1].float() / 256 * (hi - lo) + lo
print("roundtrip of", a[1].tolist(), "->", [round(v, 5) for v in back.tolist()], "(left edge, bias = half bin)")
half_k = (0.4 / 256) / 2
print("curvature half-bin %.5f 1/m -> lateral accel error at 30 m/s = %.2f m/s^2" % (half_k, 900 * half_k))

print("== M08 diffusion: alpha_bar[t] shape [B] vs x0 [B,16]")
for B in (8, 16):
    x0 = torch.randn(B, 16); ab = torch.rand(1000); t = torch.randint(0, 1000, (B,))
    try:
        xt = ab[t].sqrt() * x0
        ok = torch.allclose(xt, ab[t].sqrt()[:, None] * x0)
        print(f"B={B}: no error, correct={ok}")
    except RuntimeError as e:
        print(f"B={B}: RuntimeError")

print("== M09 flow matching: d(xt)/dt vs target")
x1 = torch.randn(4, 8, 2); x0 = torch.randn_like(x1)
t = torch.rand(4, 1, 1, requires_grad=True)
xt = t * x0 + (1 - t) * x1
dxdt = torch.autograd.grad(xt.sum(), t)[0]
print("d(xt)/dt == x0 - x1:", torch.allclose(dxdt.squeeze(), (x0 - x1).sum((1, 2))),
      "| snippet target x1 - x0 has opposite sign; xt(t=0) is data, but sampler starts from noise at t=0")

print("== M12 focal: confident correct prediction gives NaN")
logits, targets = torch.tensor([100.0, -3.0]), torch.tensor([1.0, 0.0])
p = torch.sigmoid(logits)
ce = -(targets * torch.log(p) + (1 - targets) * torch.log(1 - p))
print("ce =", ce.tolist(), " BCE-with-logits =", F.binary_cross_entropy_with_logits(logits, targets, reduction='none').tolist())
print("num_pos = 0 (empty highway frame) -> loss =", (torch.tensor(0.3) / 0).item())

print("== M13 DQN: gradient flows into the bootstrap target")
qnet = torch.nn.Linear(3, 2)
s, s2 = torch.randn(4, 3), torch.randn(4, 3); a = torch.tensor([0, 1, 0, 1])
q = qnet(s).gather(1, a[:, None]).squeeze(1); q_next = qnet(s2).max(1).values
print("target requires_grad:", (1.0 + 0.99 * q_next).requires_grad)

print("== M14 left padding positions")
ids14 = torch.tensor([[0, 0, 7, 8, 9], [5, 6, 7, 8, 9]])   # pad=0
pos = torch.arange(5).expand_as(ids14)
good = ((ids14 != 0).long().cumsum(-1) - 1).clamp(min=0)
print("snippet pos:", pos.tolist(), "\ncorrect pos:", good.tolist())

print("== M14b RoPE is shift-invariant; learned absolute positions are not")
def rope(x, pos, base=10000.0):
    d = x.shape[-1]; inv = base ** (-torch.arange(0, d, 2).double() / d)
    ang = pos.double()[:, None] * inv[None]
    x1, x2 = x[..., ::2].double(), x[..., 1::2].double()
    return torch.stack([x1 * ang.cos() - x2 * ang.sin(), x1 * ang.sin() + x2 * ang.cos()], -1).flatten(-2)
q, k = torch.randn(3, 8), torch.randn(3, 8)
p = torch.arange(3)
s0 = rope(q, p) @ rope(k, p).T; s2 = rope(q, p + 2) @ rope(k, p + 2).T
print("RoPE scores equal after shifting positions by 2:", torch.allclose(s0, s2, atol=1e-9))
table = torch.randn(16, 8)
print("learned absolute pos embeddings equal after shift:", torch.allclose(table[p], table[p + 2]))
