# -*- coding: utf-8 -*-
"""把 M3T2 放映厅片子装进 复习放映厅/ 并登记进 ★总入口.html。

⚠ 源码产物引的是 ../lib/，装到上一层要改成 lib/。
⚠ 总入口插卡用「锚点 + 前插」，不做任何删除（见 [[course-hub]]）。
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\Adelaide COMSC\2026S2\Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码", "m3t2-film.html")
DST_NAME = "M3T2-激活与损失-精读动画深度版.html"
DST = os.path.join(ROOT, "复习放映厅", DST_NAME)
HUB = os.path.join(ROOT, "★总入口.html")

s = io.open(SRC, encoding="utf-8").read()
n = s.count('src="../lib/')
assert n == 2, "预期 2 处 ../lib/，实际 %d 处" % n
io.open(DST, "w", encoding="utf-8").write(s.replace('src="../lib/', 'src="lib/'))
print("✓ 装好 复习放映厅/%s（%d 字符）" % (DST_NAME, len(s)))

h = io.open(HUB, encoding="utf-8").read()
href = "复习放映厅/" + DST_NAME
if href in h:
    print("⚠ 总入口里已经有这张卡，没有重复插入")
    sys.exit(0)

# 排在 M3T1 片子那张卡之后
ANCHOR = '  <a class="card v" href="精读/M3T2-精读.html">'
assert h.count(ANCHOR) == 1, "锚点不唯一：%d" % h.count(ANCHOR)

CARD = '''  <a class="card v" href="''' + href + '''">
    <div class="t"><span class="tag n">★★ M3 T2 放映厅</span><span class="tag d">27 知识点 / 106 帧</span>T2 激活与损失 · 精读动画深度版</div>
    <div class="m">''' + href + '''</div>
    <div class="d"><b>2026-10-27 新做。</b>⭐ <b>按官方课件 M3T2 做的逐知识点动画片</b>，空格推进、每个知识点配总结卡＋一道自测（共 25 道）。⭐⭐ <b>全片一个两层算例贯穿</b>：<b>x=[1,2]、y=1、两个 ReLU 隐藏单元（z₁=1.1 激活、z₂=−0.1 不激活）、sigmoid 输出 ⇒ s=0.67、p=0.661503 ⇒ ∂L/∂w₁₂ = −0.338497 × 0.7 × 1 × 2 = −0.473896 ⇒ w₁₂ → 0.447390 ⇒ 更新后 p=0.700487、L=0.355979</b>——每个数都在 Python 里复算核对过。⭐ 最硬的七个点：<b>激活的两个身份</b>（大的输出不代表大的梯度）、<b>三个激活在 z=−2/0/2 的「输出/导数」默写表</b>、<b>ReLU′(0)=0 的本课约定</b>、<b>MSE 配 sigmoid 比 BCE 的梯度小 101 倍</b>（y=1、p=0.01：−0.009801 vs −0.990000）、<b>四种任务 ↔ 输出层 ↔ 损失</b>、<b>隐藏梯度四因子 (p−y)·vⱼ·g′(zⱼ)·xᵢ</b>、<b>两处成因不同的零梯度</b>。⚠ 另含 <b>batch/epoch 计数</b>、<b>形状与转置</b>、<b>自动微分三个角色与它不做的事</b>。</div>
  </a>
'''

io.open(HUB, "w", encoding="utf-8").write(h.replace(ANCHOR, CARD + ANCHOR, 1))
print("✓ 已登记进 ★总入口.html（排在 M3T1 片子之后）")
