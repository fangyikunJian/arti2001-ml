# -*- coding: utf-8 -*-
"""把 M3T1 逐页精读登记进 ★总入口.html。

⚠ 总入口里每份材料只有**一处**卡片（不像放映厅片子有卡片＋紧凑列表两处）。
⚠ 插入位置：排在「M3 材料」那张卡之后、CS229 的三份精读之前
   —— 学校一手材料优先于 CS229 的补充材料。
⚠ 见 [[course-hub]]：整块换 HTML 时别用 .*?</div> 这种正则，会吃掉后面的内容；
   这里用「锚点字符串 + 前插」的办法，不做任何删除。
"""
import io, sys

sys.stdout.reconfigure(encoding="utf-8")
HUB = r"G:\Adelaide COMSC\2026S2\Machine Learning\★总入口.html"
F = "精读/M3T1-精读.html"

s = io.open(HUB, encoding="utf-8").read()
if F in s:
    print("⚠ 总入口里已经有这份了，没有重复插入")
    sys.exit(0)

ANCHOR = '  <a class="card v" href="精读/CS229-evalmetrics-精读.html">'
assert s.count(ANCHOR) == 1, "锚点不唯一：%d" % s.count(ANCHOR)

CARD = '''  <a class="card v" href="''' + F + '''">
    <div class="t"><span class="tag n">★★ M3 T1 官方课件</span><span class="tag d">35 页 / 33 题</span>逐页精读 · 神经网络</div>
    <div class="m">''' + F + '''</div>
    <div class="d"><b>2026-10-24 新做。</b>⭐ <b>这是 M3 T1 的官方幻灯本体</b>（<code>M3T1_NeuralNetworks.pdf</code>，裁掉末页校徽后 35 页），左栏原课件、右栏逐页讲解＋自测，<b>每一页都有</b>。⭐⭐ 全讲用<b>同一个算例</b>贯穿：<b>x=(1,2)、y=1、w=(0.2,0.4)、b=0.1 ⇒ z=1.1 ⇒ p=0.7503 ⇒ L=0.2873 ⇒ δ=−0.2497 ⇒ 更新后 p=0.7773、L=0.2520</b>——课件上每个数字都已复算核对。⭐ 最该掌握的六页：<b>p6–7 前向四步</b>、<b>p11–12 XOR 为什么要隐藏层</b>、<b>p13 数参数个数</b>、<b>p18 没有非线性则多层塌回一层</b>（s=3(2x+1)+4=6x+7）、<b>p24 链式法则沿路径相乘</b>、<b>p29 δ = p − y 的捷径</b>。⚠ 这份课件<b>没有 pptx、没有备注讲稿</b>，其中 16 页是纯图，讲解是逐页看图写的。</div>
  </a>
'''

io.open(HUB, "w", encoding="utf-8").write(s.replace(ANCHOR, CARD + ANCHOR, 1))
print("✓ M3T1 逐页精读已登记进总入口")
