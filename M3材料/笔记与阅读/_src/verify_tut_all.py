# -*- coding: utf-8 -*-
"""复算三份官方 Tutorial 答案里的每一个数字。

来源（2026-11-03 用户下载，均在 .gitignore 内）：
    M3材料/Tutorial与Practical/M3 T1 Tutorial_ans.pdf
    M3材料/Tutorial与Practical/M3 T2 tutorial_ans.pdf
    M3材料/Tutorial与Practical/M3 T3 Tutorial_ans.pdf

⚠ 这次是**反过来用**：官方答案是「期望值」，脚本独立算一遍去对。
  对不上就说明我读错了数字（或官方印错），两种都得查出来。
  T1 的部分另见 verify_tut_t1.py（那是在拿到答案之前自己解的，54/54 已全部吻合）。
"""
import math
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
ok = bad = 0


def chk(name, got, want, tol=5e-6):
    global ok, bad
    if abs(float(got) - float(want)) <= tol:
        ok += 1
    else:
        bad += 1
        print("   ✗ %-46s 算出 %.6f　官方写 %.6f" % (name, got, want))


sig = lambda t: 1.0 / (1.0 + math.exp(-t))

# ═══════════════════ T1 ═══════════════════
print("── T1：答案里新出现的两处 ──")
# 官方 extension 给的捷径：每次更新把 ηδ 乘「乘在该参数上的值」减掉
# ⇒ s_new = s − ηδ(h₁² + h₂² + h₃² + 1)，最后那个 1 是偏置
H = np.array([6.0, 4.0, 0.0])
p0, delta0, eta = sig(1.0), sig(1.0) - 0.0, 0.1   # extension 里 y = 0
shortcut = 1.0 - eta * delta0 * (float(H @ H) + 1)
chk("extension 捷径 s_new", shortcut, -2.874610, 5e-5)
chk("  其中 ‖h‖²+1", float(H @ H) + 1, 53.0)
chk("y=0 时更新前的 BCE", -math.log(1 - sig(1.0)), 1.313262, 5e-6)

# ═══════════════════ T2 ═══════════════════
print("── T2 Q1：激活函数三行表 ──")
for z, want in [(-3, (.0474, .0452, -.9951, .0099, 0, 0)),
                (-1, (.2689, .1966, -.7616, .4200, 0, 0)),
                (1, (.7311, .1966, .7616, .4200, 1, 1))]:
    s_, t_ = sig(z), math.tanh(z)
    chk("σ(%d)" % z, s_, want[0], 5e-5)
    chk("σ′(%d)" % z, s_ * (1 - s_), want[1], 5e-5)
    chk("tanh(%d)" % z, t_, want[2], 5e-5)
    chk("tanh′(%d)" % z, 1 - t_ * t_, want[3], 5e-5)
    chk("ReLU(%d)" % z, max(0.0, z), want[4])
    chk("ReLU′(%d)" % z, 1.0 if z > 0 else 0.0, want[5])

print("── T2 Q2：损失值与学习信号 ──")
y_, yh = np.array([3.0, 1.0]), np.array([2.5, 4.0])
res = y_ - yh
chk("MSE", float(np.mean(res ** 2)), 4.625)
chk("MAE", float(np.mean(np.abs(res))), 1.75)
chk("大残差占平方误差的比例", 9 / 9.25, 0.97, 5e-3)
chk("大残差占绝对误差的比例", 3 / 3.5, 0.86, 5e-3)
b1, b2, b3 = -math.log(.9), -math.log(1 - .2), -math.log(.6)
chk("BCE (1,.9)", b1, .105361, 5e-6)
chk("BCE (0,.2)", b2, .223144, 5e-6)
chk("BCE (1,.6)", b3, .510826, 5e-6)
chk("三者之和", b1 + b2 + b3, .839330, 5e-6)
chk("三者均值", (b1 + b2 + b3) / 3, .279777, 5e-6)
chk("半平方 logit 梯度 (y=1,p=.6)", (.6 - 1) * .6 * .4, -.096)
chk("  多出来的 sigmoid 斜率", .6 * .4, .24)
chk("BCE logit 梯度 (y=1,p=.6)", .6 - 1, -.4)
chk("三类 CE：L = −ln(.3)", -math.log(.3), 1.203973, 5e-6)
g3 = np.array([.2, .5, .3]) - np.array([0.0, 0.0, 1.0])
for i, w in enumerate([.2, .5, -.7]):
    chk("三类 logit 梯度[%d]" % i, g3[i], w)
chk("三类梯度之和应为 0", float(g3.sum()), 0.0, 1e-12)
chk("后来的损失 −ln(.6)", -math.log(.6), .510826, 5e-6)
chk("损失下降量 = ln 2", -math.log(.3) - (-math.log(.6)), .693147, 5e-6)

print("── T2 Q3：隐藏权重梯度（复用 T1 的网络）──")
W1 = np.array([[1.0, 2.0], [-1.0, 1.0], [0.0, 1.0]])
B1 = np.array([0.0, 1.0, -4.0])
W2 = np.array([1.0, -1.0, 2.0])
X = np.array([0.0, 3.0])
Z = W1 @ X + B1
Hm = np.maximum(0.0, Z)
delta = sig(float(W2 @ Hm - 1.0)) - 1.0
chk("δ = p − y", delta, -.268941, 5e-6)
# ∂L/∂w₁₂ = δ · v₁ · ReLU′(z₁) · x₂
gw12 = delta * W2[0] * (1.0 if Z[0] > 0 else 0.0) * X[1]
chk("∂L/∂w₁₂", gw12, -.806824, 5e-6)
chk("w₁₂ 更新后", 2.0 - 0.1 * gw12, 2.080682, 5e-6)
chk("∂L/∂h₃ = 2δ（非零！）", float(W2[2] * delta), 2 * delta, 1e-12)
chk("一个 epoch 的更新次数", 100 // 20, 5)
chk("三个 epoch", 3 * (100 // 20), 15)

print("── T2 extension：整个第一层 ──")
mask = (Z > 0).astype(float)
g = W2 * delta * mask                      # g = W₂ᵀδ ⊙ ReLU′(z)
for i, w in enumerate([-.268941, .268941, 0.0]):
    chk("g[%d]" % i, g[i], w, 5e-6)
gW1 = np.outer(g, X)
chk("∂L/∂W₁[0,1]", gW1[0, 1], -.806824, 5e-6)
chk("∂L/∂W₁[1,1]", gW1[1, 1], .806824, 5e-6)
chk("∂L/∂W₁ 第一列全 0（因为 x₁ = 0）", float(np.abs(gW1[:, 0]).max()), 0.0)
chk("∂L/∂W₁ 第三行全 0（因为 ReLU′ = 0）", float(np.abs(gW1[2]).max()), 0.0)
W1n = W1 - 0.1 * gW1
chk("W₁,new[0,1]", W1n[0, 1], 2.080682, 5e-6)
chk("W₁,new[1,1]", W1n[1, 1], .919318, 5e-6)
B1n = B1 - 0.1 * g
for i, w in enumerate([.026894, .973106, -4.0]):
    chk("b₁,new[%d]" % i, B1n[i], w, 5e-6)
chk("p=.02 时 BCE 的 logit 梯度", .02 - 1, -.98)
chk("p=.02 时半平方的 logit 梯度", (.02 - 1) * .02 * .98, -.019208)
chk("幅度比 = 1/[p(1−p)]", 1 / (.02 * .98), 51.0204, 5e-4)

# ═══════════════════ T3 ═══════════════════
print("── T3 Q1：划分与诊断 ──")
chk("训练集", 10000 * .6, 6000)
chk("验证集", 10000 * .2, 2000)
chk("测试集", 10000 * .2, 2000)

print("── T3 Q2：混淆矩阵与代价 ──")
TP, FN, FP, TN = 42, 8, 18, 132
chk("四格之和", TP + FN + FP + TN, 200)
chk("accuracy", (TP + TN) / 200, .870)
chk("precision", TP / (TP + FP), .700)
chk("recall", TP / (TP + FN), .840)
P_, R_ = TP / (TP + FP), TP / (TP + FN)
chk("F1", 2 * P_ * R_ / (P_ + R_), .764, 5e-4)
chk("全判负的基线 accuracy", (FP + TN) / 200, .750)
chk("原阈值总代价 5·FN + FP", 5 * FN + FP, 58)
TP2, FN2, FP2, TN2 = 47, 3, 35, 115
chk("低阈值四格之和", TP2 + FN2 + FP2 + TN2, 200)
chk("低阈值总代价", 5 * FN2 + FP2, 50)
chk("低阈值 recall", TP2 / (TP2 + FN2), .940)
chk("低阈值 precision", TP2 / (TP2 + FP2), .573, 5e-4)
chk("低阈值 accuracy", (TP2 + TN2) / 200, .810)

print("── T3 Q3：ROC 与 AUC ──")
rows = [(0.9, 1), (0.8, 0), (0.7, 1), (0.7, 0), (0.4, 1), (0.2, 0)]   # A..F
Pn = sum(l for _, l in rows)
Nn = len(rows) - Pn
chk("正例数", Pn, 3)
chk("负例数", Nn, 3)
pts, tp, fp = [(0.0, 0.0)], 0, 0
for thr in sorted({s for s, _ in rows}, reverse=True):      # ⚠ 同分一起进
    for s_, l in rows:
        if s_ == thr:
            tp += l
            fp += 1 - l
    pts.append((fp / Nn, tp / Pn))
want_pts = [(0, 0), (0, 1 / 3), (1 / 3, 1 / 3), (2 / 3, 2 / 3), (2 / 3, 1), (1, 1)]
for i, (f, t) in enumerate(want_pts):
    chk("ROC 点%d FPR" % i, pts[i][0], f, 5e-4)
    chk("ROC 点%d TPR" % i, pts[i][1], t, 5e-4)
pos = [s for s, l in rows if l]
neg = [s for s, l in rows if not l]
wins = sum(1 if a > b else .5 if a == b else 0 for a in pos for b in neg)
chk("正确排序的配对数（平局算半个）", wins, 5.5)
chk("配对法 AUC", wins / 9, .611, 5e-4)

roc2 = [(0.0, 0.0), (0.1, 0.4), (0.2, 0.5), (0.4, 0.7), (0.8, 0.9), (1.0, 1.0)]
areas = [(roc2[i + 1][0] - roc2[i][0]) * (roc2[i][1] + roc2[i + 1][1]) / 2
         for i in range(len(roc2) - 1)]
for i, w in enumerate([.020, .045, .120, .320, .190]):
    chk("第二个分类器 A%d" % (i + 1), areas[i], w, 5e-4)
chk("第二个分类器 AUC 合计", sum(areas), .695, 5e-4)

print("── T3 extension：稀有正例 ──")
pos_n, tot = 20, 2000
tp3 = .8 * pos_n
fn3 = pos_n - tp3
fp3 = .05 * (tot - pos_n)
tn3 = (tot - pos_n) - fp3
chk("TP", tp3, 16)
chk("FN", fn3, 4)
chk("FP", fp3, 99)
chk("TN", tn3, 1881)
chk("precision", tp3 / (tp3 + fp3), .139, 5e-4)
chk("accuracy", (tp3 + tn3) / tot, .9485)
chk("全判负的基线 accuracy", (tot - pos_n) / tot, .990)

print("\n合计：%d 个官方数字复算通过，%d 个对不上" % (ok, bad))
sys.exit(1 if bad else 0)
