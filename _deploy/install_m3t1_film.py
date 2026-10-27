# -*- coding: utf-8 -*-
"""把 M3T1 放映厅片子装进 复习放映厅/ 并登记进 ★总入口.html。

⚠ 源码产物 源码/m3t1-film.html 引的是 ../lib/，装到上一层要改成 lib/。
⚠ 总入口插卡用「锚点 + 前插」，不做任何删除（见 [[course-hub]]：
   整块换 HTML 时用 .*?</div> 这种正则会吃掉后面的内容）。
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\Adelaide COMSC\2026S2\Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码", "m3t1-film.html")
DST_NAME = "M3T1-神经网络-精读动画深度版.html"
DST = os.path.join(ROOT, "复习放映厅", DST_NAME)
HUB = os.path.join(ROOT, "★总入口.html")

# ── 装片子：把 ../lib/ 改回 lib/ ──
s = io.open(SRC, encoding="utf-8").read()
n = s.count('src="../lib/')
assert n == 2, "预期 2 处 ../lib/，实际 %d 处" % n
io.open(DST, "w", encoding="utf-8").write(s.replace('src="../lib/', 'src="lib/'))
print("✓ 装好 复习放映厅/%s（%d 字符）" % (DST_NAME, len(s)))

# ── 登记进总入口 ──
h = io.open(HUB, encoding="utf-8").read()
href = "复习放映厅/" + DST_NAME
if href in h:
    print("⚠ 总入口里已经有这张卡，没有重复插入")
    sys.exit(0)

ANCHOR = '  <a class="card v" href="精读/M3T2-精读.html">'
assert h.count(ANCHOR) == 1, "锚点不唯一：%d" % h.count(ANCHOR)

CARD = '''  <a class="card v" href="''' + href + '''">
    <div class="t"><span class="tag n">★★ M3 T1 放映厅</span><span class="tag d">27 知识点 / 107 帧</span>T1 神经网络 · 精读动画深度版</div>
    <div class="m">''' + href + '''</div>
    <div class="d"><b>2026-10-27 新做。</b>⭐ <b>按官方课件 M3T1 做的逐知识点动画片</b>，空格推进、每个知识点配总结卡＋一道自测（共 25 道）。⭐⭐ <b>全片一个算例贯穿到底</b>：<b>x=(1,2)、y=1、w=(0.2,0.4)、b=0.1 ⇒ z=1.1 ⇒ p=0.750260 ⇒ L=0.287335 ⇒ δ=−0.249740 ⇒ 更新后 p=0.777273、L=0.251964</b>——每个数都在 Python 里复算核对过。⭐ 最硬的七个点：<b>前向四步</b>、<b>XOR 对角同类</b>（训练只能移动旋转那条线，不能掰弯）、<b>表达能力 vs 优化</b>、<b>数参数 3→4→1 = 21</b>、<b>线性叠线性仍是直线</b>（3(2x+1)+4 = 6x+7）、<b>链式法则沿路径相乘 0.187370×1×2 = 0.374740</b>、<b>δ = p − y 的捷径</b>。⚠ 另含<b>「为什么不用准确率」</b>的标准答法与<b>扩展题五行满分写法</b>。</div>
  </a>
'''

io.open(HUB, "w", encoding="utf-8").write(h.replace(ANCHOR, CARD + ANCHOR, 1))
print("✓ 已登记进 ★总入口.html（插在 M3 那一组的精读卡之前）")
