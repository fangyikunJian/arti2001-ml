# -*- coding: utf-8 -*-
"""验收《M3 备考包》：① 打散选项之后，答案字母仍然指向原来那条正确选项；
② 模拟卷里出现的数字全部复算一遍。

⚠ 为什么要查第 ① 条：打散是「把正确选项和目标位置对调」，
  只要有一处把字母和文字对错，整份模拟卷的答案就全废了，而且肉眼很难发现。
"""
import html as H
import io
import math
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_m3_kit.py")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "M3备考包-速查表与模拟卷.html")

# ── ① 打散前后的一致性 ──────────────────────────────
ns = {}
src = io.open(SRC, encoding="utf-8").read()
# 只执行到 MCQ 定义和 _balance 定义为止，不跑落盘
head = src[:src.index("MCQ = _balance(MCQ)")]
head = head[head.index("MCQ = ["):]          # 丢掉前面画页面的部分
exec("import collections, random\n" + head, ns)          # noqa: S102
raw = ns["MCQ"]
bal = ns["_balance"](list(raw))
bad = 0
for (s0, o0, a0, _), (s1, o1, a1, _) in zip(raw, bal):
    want = o0["ABCD".index(a0)]
    got = o1["ABCD".index(a1)]
    assert s0 == s1
    if want != got:
        bad += 1
        print("   ✗ 打散后答案错位：", s0[:30], "｜应为", want[:28], "｜实为", got[:28])
    if sorted(o0) != sorted(o1):
        bad += 1
        print("   ✗ 打散后选项集合变了：", s0[:30])
print("① 打散一致性：%d 题，%s" % (len(raw), "全部对得上 ✓" if not bad else "%d 处错 ✗" % bad))

# ── 落盘的 HTML 里，字母指向的也应当是同一条 ──────────
doc = io.open(OUT, encoding="utf-8").read()
# ⚠ 一道题是以 </details></div> 收尾的，不是 </div></div>——
#   写错会让这一项「0 题全部通过」，等于白查。
qs = re.findall(r'<div class="q">.*?</details></div>', doc, re.S)
assert len(qs) == 20, "只抓到 %d 道题，正则不对" % len(qs)
miss = 0
for k, blk in enumerate(qs):
    ops = [H.unescape(re.sub(r"<[^>]+>", "", o)).strip()
           for o in re.findall(r"<li>(.*?)</li>", blk, re.S)]
    a = re.search(r"<p><b>([ABCD])</b>", blk).group(1)
    want = H.unescape(re.sub(r"<[^>]+>", "", bal[k][1]["ABCD".index(bal[k][2])])).strip()
    if ops["ABCD".index(a)] != want:
        miss += 1
        print("   ✗ 第 %d 题 HTML 里字母对不上" % (k + 1))
print("② HTML 落盘一致性：%d 题，%s" % (len(qs), "✓" if not miss else "✗"))

# ── ③ 数字复算 ─────────────────────────────────────
ok = err = 0


def chk(name, got, want, tol=5e-6):
    global ok, err
    if abs(got - want) <= tol:
        ok += 1
    else:
        err += 1
        print("   ✗ %-34s 算出 %.6f　卷面写 %.6f" % (name, got, want))


sig = lambda z: 1.0 / (1.0 + math.exp(-z))
relu = lambda v: max(0.0, v)

# 选择题
chk("Q1 z", 0.4 * 3 + 0.6 * -1 - 0.2, 0.4)
chk("Q4 塌缩 x=0", 2 * (4 * 0 - 1) + 5, 3)
chk("Q4 塌缩 斜率", (2 * (4 * 1 - 1) + 5) - (2 * (4 * 0 - 1) + 5), 8)
chk("Q6 dF/dq", 1 * 5 + 1 * -2, 3)
chk("Q7 y=0 p=0.25 的 BCE", -math.log(0.75), 0.2877, 5e-5)
chk("Q7 干扰项 −log0.25", -math.log(0.25), 1.3863, 5e-5)
chk("Q8 ∂L/∂w₂", (0.3 - 1) * -4, 2.8)
chk("Q9 tanh′", 1 - 0.6 ** 2, 0.64)
chk("Q11 过 Leaky", -0.8 * 0.01, -0.008)
chk("Q15 更新次数", 4 * (240 // 16), 60)
chk("Q20 precision", 15 / 60, 0.25)
chk("Q20 recall", 15 / 20, 0.75)
chk("Q20 accuracy", (15 + 435) / 500, 0.90)
chk("Q20 全判负基线", 480 / 500, 0.96)

# 第 21 题
x, y, w, b, eta = [2.0, 1.0], 0.0, [0.3, -0.5], 0.4, 0.2
z = w[0] * x[0] + w[1] * x[1] + b
p = sig(z)
chk("Q21 z", z, 0.5)
chk("Q21 p", p, 0.622459)
chk("Q21 L", -math.log(1 - p), 0.974077)
d = p - y
chk("Q21 δ", d, 0.622459)
chk("Q21 ∂L/∂w₁", d * x[0], 1.244919)
chk("Q21 ∂L/∂w₂", d * x[1], 0.622459)
w1n, w2n, bn = w[0] - eta * d * x[0], w[1] - eta * d * x[1], b - eta * d
chk("Q21 新 w₁", w1n, 0.051016)
chk("Q21 新 w₂", w2n, -0.624492)
chk("Q21 新 b", bn, 0.275508)
zn = w1n * x[0] + w2n * x[1] + bn
chk("Q21 新 z", zn, -0.246951)
chk("Q21 新 p", sig(zn), 0.438574)
chk("Q21 新 L", -math.log(1 - sig(zn)), 0.577275)

# 第 22 题
x, y, eta = [1.0, 3.0], 1.0, 0.5
W = [[0.5, -0.2], [-0.3, 0.4]]
bb = [0.1, 0.2]
v = [0.6, 0.5]
c = -0.3
z = [W[j][0] * x[0] + W[j][1] * x[1] + bb[j] for j in (0, 1)]
h = [relu(t) for t in z]
s = v[0] * h[0] + v[1] * h[1] + c
p = sig(s)
chk("Q22 z₁", z[0], 0.0)
chk("Q22 z₂", z[1], 1.1)
chk("Q22 h₁", h[0], 0.0)
chk("Q22 s", s, 0.25)
chk("Q22 p", p, 0.562177)
chk("Q22 L", -math.log(p), 0.575939)
d = p - y
g = lambda t: 1.0 if t > 0 else 0.0        # ⚠ 本课约定 ReLU′(0) = 0
dz = [d * v[j] * g(z[j]) for j in (0, 1)]
chk("Q22 ∂L/∂s", d, -0.437823)
chk("Q22 ∂L/∂h₂", d * v[1], -0.218912)
chk("Q22 ∂L/∂w₂₂", dz[1] * x[1], -0.656735)
chk("Q22 ∂L/∂w₂₁", dz[1] * x[0], -0.218912)
chk("Q22 ∂L/∂v₂", d * h[1], -0.481606)
chk("Q22 隐藏1 梯度为 0", dz[0], 0.0)
chk("Q22 v₁ 梯度为 0", d * h[0], 0.0)
Wn = [[W[j][i] - eta * dz[j] * x[i] for i in (0, 1)] for j in (0, 1)]
bn2 = [bb[j] - eta * dz[j] for j in (0, 1)]
vn = [v[0] - eta * d * h[0], v[1] - eta * d * h[1]]
cn = c - eta * d
chk("Q22 新 w₂₂", Wn[1][1], 0.728368)
chk("Q22 新 w₂₁", Wn[1][0], -0.190544)
chk("Q22 新 b₂", bn2[1], 0.309456)
chk("Q22 新 v₂", vn[1], 0.740803)
chk("Q22 新 c", cn, -0.081088)
z2 = [Wn[j][0] * x[0] + Wn[j][1] * x[1] + bn2[j] for j in (0, 1)]
h2 = [relu(t) for t in z2]
s2 = vn[0] * h2[0] + vn[1] * h2[1] + cn
chk("Q22 新 z₂", z2[1], 2.304015)
chk("Q22 新 s", s2, 1.625733)
chk("Q22 新 p", sig(s2), 0.835584)
chk("Q22 新 L", -math.log(sig(s2)), 0.179624)

# 第 23 题
TP, FP, FN, TN = 24, 36, 16, 224
chk("Q23 计数合计", TP + FP + FN + TN, 300)
chk("Q23 accuracy", (TP + TN) / 300, 0.8267, 5e-5)
chk("Q23 precision", TP / (TP + FP), 0.40)
chk("Q23 recall", TP / (TP + FN), 0.60)
chk("Q23 F1", 2 * TP / (2 * TP + FP + FN), 0.48)
chk("Q23 基线准确率", (FP + TN) / 300, 0.8667, 5e-5)
chk("Q23 代价 8FN+FP 当前", 8 * 16 + 36, 164)
chk("Q23 代价 8FN+FP 更低阈值", 8 * 8 + 70, 134)
chk("Q23 等代价 当前", 16 + 36, 52)
chk("Q23 等代价 更低阈值", 8 + 70, 78)
chk("Q23 低阈值计数合计", 32 + 70 + 8 + 190, 300)

# 第 24 题
rows = [(0.95, 1), (0.70, 1), (0.60, 0), (0.40, 1), (0.20, 0)]
Pn = sum(l for _, l in rows)
Nn = len(rows) - Pn
chk("Q24 正例数", Pn, 3)
chk("Q24 负例数", Nn, 2)
pts, tp, fp = [(0.0, 0.0)], 0, 0
for sc, l in rows:
    tp += l
    fp += 1 - l
    pts.append((fp / Nn, tp / Pn))
for i, (f, t) in enumerate([(0, 0), (0, 1 / 3), (0, 2 / 3), (0.5, 2 / 3), (0.5, 1), (1, 1)]):
    chk("Q24 点%d FPR" % i, pts[i][0], f)
    chk("Q24 点%d TPR" % i, pts[i][1], t)
auc = sum((pts[i + 1][0] - pts[i][0]) * (pts[i][1] + pts[i + 1][1]) / 2
          for i in range(len(pts) - 1))
chk("Q24 梯形 AUC", auc, 5 / 6)
pos = [sc for sc, l in rows if l]
neg = [sc for sc, l in rows if not l]
wins = sum(1 if a > bq else 0.5 if a == bq else 0 for a in pos for bq in neg)
chk("Q24 配对 AUC", wins / (len(pos) * len(neg)), 5 / 6)
chk("Q24 阈值0.5 precision", 2 / 3, 0.667, 5e-4)
chk("Q24 部署 TP", 1000 * 0.02 * (2 / 3), 13.333, 1e-3)
chk("Q24 部署 FP", 1000 * 0.98 * 0.5, 490.0)
chk("Q24 部署 precision", (1000 * .02 * 2 / 3) / ((1000 * .02 * 2 / 3) + 490), 0.0265, 5e-4)

print("③ 数字复算：%d 个通过，%d 个对不上" % (ok, err))
sys.exit(1 if (bad or miss or err) else 0)
