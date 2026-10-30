# -*- coding: utf-8 -*-
"""复算 M3 T1 官方 Tutorial 的每一个数字。

来源：`M3材料/Tutorial与Practical/M3 T1 Tutorial.pdf`（5 页，Q1–Q3 + 选做 extension）。
⚠ 这份 worksheet **不带答案**（堂内做、当场交、由 tutor 批改），
  所以下面的解答是自己算的 —— 每一步都用 numpy 独立重算一遍，防止手推写错。

网络（Tutorial 第 1 页）：
    z = W1 x + b1,  h = ReLU(z),  s = W2 h + c,  p = σ(s)
    x = [0, 3]ᵀ,  y = 1
    W1 = [[1,2],[−1,1],[0,1]],  b1 = [0,1,−4]ᵀ,  W2 = [1,−1,2],  c = −1
约定：自然对数、阈值 0.5、保留 4–6 位小数、中间值不四舍五入。
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
        print("   ✗ %-44s 算出 %.8f　写的是 %.8f" % (name, got, want))


sig = lambda t: 1.0 / (1.0 + math.exp(-t))

X = np.array([0.0, 3.0])
Y = 1.0
W1 = np.array([[1.0, 2.0], [-1.0, 1.0], [0.0, 1.0]])
B1 = np.array([0.0, 1.0, -4.0])
W2 = np.array([1.0, -1.0, 2.0])
C = -1.0
ETA = 0.1

print("── Q1 前向传播 ──")
chk("W1 参数个数", W1.size, 6)
chk("b1 参数个数", B1.size, 3)
chk("W2 参数个数", W2.size, 3)
chk("可训练参数总数", W1.size + B1.size + W2.size + 1, 13)

Z = W1 @ X + B1
H = np.maximum(0.0, Z)
chk("z1", Z[0], 6.0)
chk("z2", Z[1], 4.0)
chk("z3", Z[2], -1.0)
chk("h1", H[0], 6.0)
chk("h2", H[1], 4.0)
chk("h3（ReLU 截断）", H[2], 0.0)

S = float(W2 @ H + C)
P = sig(S)
L = -math.log(P)
chk("s", S, 1.0)
chk("p = σ(1)", P, 0.731059, 5e-6)
chk("L = −log p", L, 0.313262, 5e-6)
print("   预测类别 =", 1 if P >= 0.5 else 0, "（与 y = 1 一致）")

# Q1.5 去掉 ReLU ⇒ 整串塌缩成一个仿射函数
w_til = W2 @ W1
c_til = float(W2 @ B1 + C)
chk("w̃[0]", w_til[0], 2.0)
chk("w̃[1]", w_til[1], 3.0)
chk("c̃", c_til, -10.0)
S_lin = float(w_til @ X + c_til)
chk("去掉 ReLU 后的 s", S_lin, -1.0)
chk("去掉 ReLU 后的 p", sig(S_lin), 0.268941, 5e-6)
print("   ⇒ 去掉 ReLU 后判成类别 %d —— **预测翻转**" % (1 if sig(S_lin) >= 0.5 else 0))
print("   差额 s_relu − s_lin = %.1f，正好等于 v3·(0 − z3) = 2×(0−(−1))" % (S - S_lin))

print("── Q2 学习信号 ──")
dL_dp = -1.0 / P
dp_ds = P * (1 - P)
delta = dL_dp * dp_ds
chk("∂L/∂p = −1/p", dL_dp, -1.367879, 5e-6)
chk("∂p/∂s = p(1−p)", dp_ds, 0.196612, 5e-6)
chk("δ（链式相乘）", delta, -0.268941, 5e-6)
chk("δ = p − y（应当相等）", delta, P - Y, 1e-12)
chk("∂L/∂v1 = δ·h1", delta * H[0], -1.613649, 5e-6)

gW2 = delta * H
gC = delta
chk("∂L/∂v1", gW2[0], -1.613649, 5e-6)
chk("∂L/∂v2", gW2[1], -1.075766, 5e-6)
chk("∂L/∂v3（h3 = 0）", gW2[2], 0.0)
chk("∂L/∂c", gC, -0.268941, 5e-6)

print("── Q3 一次更新与复查 ──")
W2n = W2 - ETA * gW2
Cn = C - ETA * gC
chk("v1 更新后", W2n[0], 1.161365, 5e-6)
chk("v2 更新后", W2n[1], -0.892423, 5e-6)
chk("v3 更新后（不变）", W2n[2], 2.0)
chk("c 更新后", Cn, -0.973106, 5e-6)

Sn = float(W2n @ H + Cn)
Pn = sig(Sn)
Ln = -math.log(Pn)
chk("新 s", Sn, 2.425390, 5e-6)
chk("新 p", Pn, 0.918743, 5e-6)
chk("新 L", Ln, 0.084749, 5e-6)
print("   类别 %d → %d（没变）；损失 %.6f → %.6f（下降 %.6f）"
      % (1 if P >= .5 else 0, 1 if Pn >= .5 else 0, L, Ln, L - Ln))

print("── 选做 extension：同样的预测，目标改成 y = 0 ──")
Y0 = 0.0
d0 = P - Y0
chk("δ（y=0）", d0, 0.731059, 5e-6)
g0 = d0 * H
chk("∂L/∂v1（y=0）", g0[0], 4.386351, 5e-6)
chk("∂L/∂v2（y=0）", g0[1], 2.924234, 5e-6)
chk("∂L/∂v3（y=0）", g0[2], 0.0)
chk("∂L/∂c（y=0）", d0, 0.731059, 5e-6)
W2n0 = W2 - ETA * g0
Cn0 = C - ETA * d0
chk("v1 更新后（y=0）", W2n0[0], 0.561365, 5e-6)
chk("v2 更新后（y=0）", W2n0[1], -1.292423, 5e-6)
chk("c 更新后（y=0）", Cn0, -1.073106, 5e-6)
Sn0 = float(W2n0 @ H + Cn0)
Pn0 = sig(Sn0)
chk("新 s（y=0）", Sn0, -2.874610, 5e-6)
chk("新 p（y=0）", Pn0, 0.053423, 5e-6)
chk("新 L（y=0，BCE 用 −log(1−p)）", -math.log(1 - Pn0), 0.054903, 5e-6)
print("   ⇒ 梯度全部变成正号，更新把 logit 往下推；类别从 1 翻到 %d"
      % (1 if Pn0 >= .5 else 0))

print("── T1 Practical 官方解答里的数字（独立复算一遍）──")
# ⚠ Prac 用的是**另一个**网络：2 → 3 → 1，四个观测，第一个是 x = [1, −1]
PW1 = np.array([[0.6, -0.2], [-0.4, 0.7], [0.3, -0.5]])
PB1 = np.array([0.1, 0.2, -0.1])
PW2 = np.array([0.8, -0.6, 0.5])
PB2 = 0.1
px = np.array([1.0, -1.0])
pz = PW1 @ px + PB1
ph = np.maximum(0.0, pz)
chk("Prac 单元1 预激活", pz[0], 0.9)
chk("Prac 单元2 预激活", pz[1], -0.9)
chk("Prac 单元3 预激活", pz[2], 0.7)
chk("Prac h2（被 ReLU 截断）", ph[1], 0.0)
ps = float(PW2 @ ph + PB2)
chk("Prac logit", ps, 1.17)
chk("Prac p", sig(ps), 0.763145, 5e-6)
chk("Prac 第一个观测的 BCE（y=1）", -math.log(sig(ps)), 0.270307, 5e-6)  # 官方写「about 0.2703」
print("   ⚠ 官方强调：四个观测的**平均** BCE 是 0.745984，不是第一个观测的 0.2703")

# ⚠⚠ 两张学习率表是**两个不同的实验**，数字完全不同，极易记混
CANVAS = {0: 0.580352, 0.1: 0.574996, 1: 0.533347, 10: 0.371611, 100: 9.965953}
PRAC = {0: 0.745984, 0.1: 0.733989, 1: 0.664890, 100: 4.621223}
assert CANVAS[0] != PRAC[0], "两张表的起点应当不同"
assert min(CANVAS, key=CANVAS.get) == 10 and min(PRAC, key=PRAC.get) == 1
print("   Canvas 课程页那张：起点 %.6f，最低在 η=10（%.6f）" % (CANVAS[0], CANVAS[10]))
print("   T1 Prac 那张：     起点 %.6f，最低在 η=1 （%.6f）" % (PRAC[0], PRAC[1]))
print("   ⇒ 同是「四个观测的单步学习率对比」，网络不同、最优 η 也不同 —— 别记混")
ok += 2

print("\n合计：%d 个数字通过，%d 个对不上" % (ok, bad))
sys.exit(1 if bad else 0)
