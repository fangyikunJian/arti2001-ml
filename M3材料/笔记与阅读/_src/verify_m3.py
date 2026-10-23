# -*- coding: utf-8 -*-
"""逐个复算 M3 资料里出现的数字。

为什么要做：知识点整理和题库里的数字是从讲义抄来的，抄错一个考场上就按错的记。
M2 那套当时复算了 58 个数，这里同样处理 —— 连讲义里那两张表（学习率一步实验、
100 次更新）也用 numpy 把网络重搭一遍，顺便验证讲义本身。
"""
import math
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

ok = bad = 0


def chk(name, got, want, tol=5e-6):
    global ok, bad
    good = abs(got - want) <= tol
    if good:
        ok += 1
    else:
        bad += 1
        print("   ✗ %-46s 算出 %.6f　资料写 %.6f" % (name, got, want))
    return good


sig = lambda z: 1.0 / (1.0 + math.exp(-z))

print("── T1：单神经元算例 ──")
x1, x2, w1, w2, b, y = 1.0, 2.0, 0.2, 0.4, 0.1, 1.0
z = w1 * x1 + w2 * x2 + b
p = sig(z)
chk("z", z, 1.1)
chk("p = σ(1.1)", p, 0.750260)
chk("L = −log p", -math.log(p), 0.287335)
chk("p(1−p)", p * (1 - p), 0.187370)
chk("∂p/∂w₂ = p(1−p)·x₂", p * (1 - p) * x2, 0.374740)
chk("w₂ 加 0.01 的导数预测增量", p * (1 - p) * x2 * 0.01, 0.003747, 1e-5)
chk("z = 1.12 的 p", sig(1.12), 0.753989)
chk("实际增量", sig(1.12) - p, 0.003729, 1e-5)
chk("∂L/∂p = −1/p", -1 / p, -1.332871)
delta = p - y
chk("δ = p − y", delta, -0.249740)
chk("∂L/∂w₁", delta * x1, -0.249740)
chk("∂L/∂w₂", delta * x2, -0.499480)
eta = 0.1
w1n, w2n, bn = w1 - eta * delta * x1, w2 - eta * delta * x2, b - eta * delta
chk("w₁ 更新后", w1n, 0.224974)
chk("w₂ 更新后", w2n, 0.449948)
chk("b 更新后", bn, 0.124974)
zn = w1n * x1 + w2n * x2 + bn
chk("新 z", zn, 1.249844)
chk("新 p", sig(zn), 0.777273)
chk("新 L", -math.log(sig(zn)), 0.251964)
chk("w₁ 用加号的错误结果", w1 + eta * delta * x1, 0.175026)
chk("−log(0.5)", -math.log(0.5), 0.6931, 1e-4)
chk("−log(0.9)", -math.log(0.9), 0.1054, 1e-4)

print("── T1：标量与多路径小例子 ──")
chk("f(3.01) = 3.01²", 3.01 ** 2, 9.0601)
chk("实际变化", 3.01 ** 2 - 9, 0.0601)
chk("导数估计", 6 * 0.01, 0.06)
chk("dF/dq = 1·2 + 1·3", 1 * 2 + 1 * 3, 5)
chk("q=1.01 时 F", 2 * 1.01 + 3 * 1.01, 5.05)
chk("塌缩后 3(2x+1)+4 在 x=0", 3 * (2 * 0 + 1) + 4, 7)
chk("塌缩斜率", (3 * (2 * 1 + 1) + 4) - (3 * (2 * 0 + 1) + 4), 6)
relu = lambda v: max(0.0, v)
chk("加 ReLU，x=−1 时 s", 3 * relu(2 * -1 + 1) + 4, 4)
chk("不加 ReLU，x=−1 时 s", 3 * (2 * -1 + 1) + 4, 1)
chk("x=1 时两者", 3 * relu(2 * 1 + 1) + 4, 13)

print("── 考纲示例大题 1（ReLU + 半平方）──")
xe, ye, we, be = 3.0, 4.0, 0.5, 0.5
ze = we * xe + be
ae = relu(ze)
chk("z", ze, 2.0)
chk("a", ae, 2.0)
chk("L = (a−y)²/2", (ae - ye) ** 2 / 2, 2.0)
dz = (ae - ye) * 1.0
chk("∂L/∂w", dz * xe, -6.0)
chk("∂L/∂b", dz, -2.0)
chk("w 更新后（η=0.05）", we - 0.05 * dz * xe, 0.8)
chk("b 更新后", be - 0.05 * dz, 0.6)

print("── T2：激活函数数值表 ──")
for zz, so, sd, to, td in [(-2, 0.119, 0.105, -0.964, 0.071),
                           (0, 0.500, 0.250, 0.0, 1.0),
                           (2, 0.881, 0.105, 0.964, 0.071)]:
    s = sig(zz)
    chk("σ(%d)" % zz, s, so, 5e-4)
    chk("σ′(%d)" % zz, s * (1 - s), sd, 5e-4)
    chk("tanh(%d)" % zz, math.tanh(zz), to, 5e-4)
    chk("tanh′(%d)" % zz, 1 - math.tanh(zz) ** 2, td, 5e-4)
chk("tanh(1)", math.tanh(1), 0.7616, 5e-5)
chk("tanh′(1)", 1 - math.tanh(1) ** 2, 0.4200, 5e-5)
chk("Leaky(−2), α=0.01", max(0.01 * -2, -2.0), -0.02)
chk("传出梯度 0.6×0.25", 0.6 * 0.25, 0.15)
chk("过 Leaky 0.6×0.01", 0.6 * 0.01, 0.006)
chk("(1,−1) 的 z", 1 + (-1), 0)
chk("(−1,−1) 的 p", sig(-2), 0.119, 5e-4)
chk("(1,1) 的 p", sig(2), 0.881, 5e-4)

print("── T2：损失算例 ──")
tgt, prd = np.array([3.0, -1.0]), np.array([2.0, 1.0])
chk("MSE", float(np.mean((prd - tgt) ** 2)), 2.5)
chk("MAE", float(np.mean(np.abs(prd - tgt))), 1.5)
chk("−ln 0.7", -math.log(0.7), 0.3567, 5e-5)
chk("y=0,p=0.8 的损失", -math.log(0.2), 1.609, 5e-4)
chk("y=0,p=0.1 的损失", -math.log(0.9), 0.105, 5e-4)
chk("−ln 0.8", -math.log(0.8), 0.2231, 5e-5)
chk("两样本平均 BCE", (-math.log(0.8) - math.log(0.7)) / 2, 0.2899, 5e-5)
ex = np.exp(np.array([1.0, 2.0, 0.0]))
sm = ex / ex.sum()
chk("softmax 和", float(ex.sum()), 11.107, 5e-4)
for i, v in enumerate([0.245, 0.665, 0.090]):
    chk("softmax[%d]" % i, float(sm[i]), v, 5e-4)
ex2 = np.exp(np.array([1.0, 2.0, 0.0]) - 2)
chk("减去最大 logit 后不变", float(np.abs(ex2 / ex2.sum() - sm).max()), 0.0, 1e-12)
chk("半平方 logit 梯度 (a=0.01,y=1)", (0.01 - 1) * 0.01 * 0.99, -0.009801)
chk("BCE logit 梯度", 0.01 - 1, -0.99)
chk("F1 调和(1, 0.1)", 2 * 1 * 0.1 / (1 + 0.1), 0.182, 5e-4)

print("── T2：隐藏层完整算例 ──")
X = np.array([1.0, 2.0])
W1 = np.array([[0.2, 0.4], [-0.5, 0.3]])     # 行 = 隐藏单元
b1 = np.array([0.1, -0.2])
W2 = np.array([0.7, -0.4])
c = -0.1
Z = W1 @ X + b1
H = np.maximum(0.0, Z)
s = float(W2 @ H + c)
pp = sig(s)
chk("z₁", float(Z[0]), 1.1)
chk("z₂", float(Z[1]), -0.1)
chk("h₂", float(H[1]), 0.0)
chk("s", s, 0.67)
chk("p", pp, 0.661503)
chk("L", -math.log(pp), 0.413241)
d_s = pp - 1.0
chk("∂L/∂s", d_s, -0.338497)
d_h = d_s * W2
chk("∂L/∂h₁", float(d_h[0]), -0.236948)
d_z = d_h * (Z > 0)
chk("∂L/∂w₁₂", float(d_z[0] * X[1]), -0.473896)
chk("w₁₂ 更新后", 0.4 - 0.1 * float(d_z[0] * X[1]), 0.447390)
gW2 = d_s * H
chk("输出权重梯度 v₁", float(gW2[0]), -0.372347)
chk("输出权重梯度 v₂", float(gW2[1]), 0.0)
W1n = W1 - 0.1 * np.outer(d_z, X)
b1n = b1 - 0.1 * d_z
W2n = W2 - 0.1 * gW2
cn = c - 0.1 * d_s
chk("隐藏1 新权重 w₁₁", float(W1n[0, 0]), 0.223695)
chk("隐藏1 新偏置", float(b1n[0]), 0.123695)
chk("隐藏2 新权重 未变", float(W1n[1, 0]), -0.5)
chk("输出新权重 v₁", float(W2n[0]), 0.737235)
chk("输出新偏置", cn, -0.066150)
Zn = W1n @ X + b1n
chk("新隐藏分数 z₁", float(Zn[0]), 1.242169)
sn = float(W2n @ np.maximum(0, Zn) + cn)
chk("新 s", sn, 0.849619)
chk("新 p", sig(sn), 0.700487)
chk("新 L", -math.log(sig(sn)), 0.355979)

print("── T2：ReLU by hand 与 TensorFlow 例子 ──")
r = lambda v: relu(v) - relu(v - 2)
chk("r(−1)", r(-1), 0)
chk("r(1)", r(1), 1)
chk("r(5)", r(5), 2)
wt, bt = 1.5, -1.0
zt = wt * 2.0 + bt
at = relu(zt)
chk("TF z", zt, 2.0)
chk("TF loss", 0.5 * (at - 5.0) ** 2, 4.5)
gt = at - 5.0
chk("TF gw", gt * 1 * 2.0, -6.0)
chk("TF gb", gt * 1 * 1.0, -3.0)
wt2, bt2 = wt - 0.05 * gt * 2.0, bt - 0.05 * gt
chk("TF w 更新后", wt2, 1.8)
chk("TF b 更新后", bt2, -0.85)
chk("TF 新 loss", 0.5 * (relu(wt2 * 2 + bt2) - 5.0) ** 2, 2.53125)
chk("1 epoch 更新次数", 100 // 20, 5)
chk("3 epoch 更新次数", 3 * (100 // 20), 15)

print("── T3：四样本批量（学习率表 / 100 次更新表）──")
XB = np.array([[1.0, 2.0], [-1.0, -2.0], [2.0, -1.0], [-2.0, 1.0]])
YB = np.array([1.0, 1.0, 0.0, 0.0])


def fwd(W1, b1, W2, c):
    Z = XB @ W1.T + b1
    H = np.maximum(0.0, Z)
    S = H @ W2 + c
    P = 1.0 / (1.0 + np.exp(-S))
    # ⚠ η=100 那一行的 logit 大到 sigmoid 直接饱和成 0/1，再取对数就是 inf。
    #   讲义说代码「直接从 logits 算 BCE，为的是避免对四舍五入过的概率取对数」，
    #   所以这里也用数值稳定式：max(S,0) − S·Y + log(1 + e^(−|S|))。
    L = float(np.mean(np.maximum(S, 0) - S * YB + np.log1p(np.exp(-np.abs(S)))))
    return Z, H, S, P, L


def step(W1, b1, W2, c, eta):
    Z, H, S, P, _ = fwd(W1, b1, W2, c)
    N = len(YB)
    dS = (P - YB) / N
    gW2 = H.T @ dS
    gc = float(dS.sum())
    dH = np.outer(dS, W2)
    dZ = dH * (Z > 0)
    gW1 = dZ.T @ XB
    gb1 = dZ.sum(axis=0)
    return (W1 - eta * gW1, b1 - eta * gb1, W2 - eta * gW2, c - eta * gc)


P0 = (np.array([[0.2, 0.4], [-0.5, 0.3]]), np.array([0.1, -0.2]),
      np.array([0.7, -0.4]), -0.1)
chk("起始平均 BCE", fwd(*P0)[4], 0.580352)
for eta_, want in [(0.0, 0.580352), (0.1, 0.574996), (1.0, 0.533347),
                   (10.0, 0.371611), (100.0, 9.965953)]:
    chk("η=%g 一步后" % eta_, fwd(*step(*P0, eta_))[4], want, 5e-5)

cur, trace = P0, {0: (0.580352, 0.6615, 0.4750)}
for want_n, want in [(1, (0.574996, 0.6664, 0.4749)), (5, (0.552753, 0.6867, 0.4748)),
                     (10, (0.527730, 0.7158, 0.4750)), (20, (0.484156, 0.7770, 0.4759)),
                     (50, (0.406138, 0.8987, 0.4788)), (100, (0.369420, 0.9592, 0.4859))]:
    while True:
        trace[len(trace)] = None
        cur = step(*cur, 0.1)
        n_done = sum(1 for k in trace if trace[k] is None)
        if n_done >= want_n:
            break
    _, _, _, P, L = fwd(*cur)
    chk("%3d 次更新后 平均 BCE" % want_n, L, want[0], 5e-5)
    chk("%3d 次更新后 p[1,2]" % want_n, float(P[0]), want[1], 5e-5)
    chk("%3d 次更新后 p[−1,−2]" % want_n, float(P[1]), want[2], 5e-5)

print("── T3：混淆矩阵与指标 ──")


def mets(TP, FN, FP, TN):
    acc = (TP + TN) / (TP + TN + FP + FN)
    pre = TP / (TP + FP)
    rec = TP / (TP + FN)
    f1 = 2 * TP / (2 * TP + FP + FN)
    return acc, pre, rec, f1


a, pr, re, f1 = mets(4, 1, 2, 5)
chk("12 例 accuracy", a, 0.75)
chk("12 例 precision", pr, 0.667, 5e-4)
chk("12 例 recall", re, 0.8)
chk("12 例 F1", f1, 0.727, 5e-4)
chk("12 例 F1 = 8/11", f1, 8 / 11)
a, pr, re, f1 = mets(6, 3, 2, 9)
chk("20 顾客 accuracy", a, 0.75)
chk("20 顾客 precision", pr, 0.75)
chk("20 顾客 recall", re, 0.667, 5e-4)
chk("20 顾客 F1 = 12/17", f1, 12 / 17)
chk("全判 0 的基线", 11 / 20, 0.55)
chk("代价 5FN+FP，阈值0.5", 5 * 6 + 4, 34)
chk("代价 5FN+FP，阈值0.3", 5 * 2 + 12, 22)
chk("代价相等，阈值0.5", 6 + 4, 10)
chk("代价相等，阈值0.3", 2 + 12, 14)
a, pr, re, f1 = mets(18, 6, 12, 164)
chk("考纲大题 accuracy", a, 0.91)
chk("考纲大题 precision", pr, 0.60)
chk("考纲大题 recall", re, 0.75)
chk("考纲大题 F1", f1, 2 / 3)

print("── T3：ROC / AUC ──")
rows = [(0.90, 1), (0.80, 0), (0.40, 1), (0.10, 0)]
P_, N_ = sum(1 for _, l in rows if l), sum(1 for _, l in rows if not l)
pts, TP_, FP_ = [(0.0, 0.0)], 0, 0
for sc, lb in rows:
    TP_ += lb
    FP_ += 1 - lb
    pts.append((FP_ / N_, TP_ / P_))
for i, (f, t) in enumerate([(0, 0), (0, 0.5), (0.5, 0.5), (0.5, 1), (1, 1)]):
    chk("ROC 点%d FPR" % i, pts[i][0], f)
    chk("ROC 点%d TPR" % i, pts[i][1], t)
auc = sum((pts[i + 1][0] - pts[i][0]) * (pts[i][1] + pts[i + 1][1]) / 2
          for i in range(len(pts) - 1))
chk("梯形法 AUC", auc, 0.75)
pos = [s for s, l in rows if l]
neg = [s for s, l in rows if not l]
wins = sum((1 if a_ > b_ else 0.5 if a_ == b_ else 0) for a_ in pos for b_ in neg)
chk("配对法 AUC", wins / (len(pos) * len(neg)), 0.75)
chk("稀有正例 TP", 0.8 * 10, 8)
chk("稀有正例 FP", 0.1 * 990, 99)
chk("稀有正例 precision", 8 / 107, 0.075, 5e-4)
chk("稀有正例 recall", 8 / 10, 0.80)
chk("PR 参考线 = 正例占比", 2 / 4, 0.5)

print("\n合计：%d 个数字通过，%d 个对不上" % (ok, bad))
sys.exit(1 if bad else 0)
