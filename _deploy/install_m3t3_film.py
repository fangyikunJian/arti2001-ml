# -*- coding: utf-8 -*-
"""把 M3T3 放映厅片子装进 复习放映厅/ 并登记进 ★总入口.html。

⚠ 源码产物引的是 ../lib/，装到上一层要改成 lib/。
⚠ 总入口插卡用「锚点 + 前插」，不做任何删除（见 [[course-hub]]）。
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\Adelaide COMSC\2026S2\Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码", "m3t3-film.html")
DST_NAME = "M3T3-模型评估-精读动画深度版.html"
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

ANCHOR = '  <a class="card v" href="精读/M3T2-精读.html">'
assert h.count(ANCHOR) == 1, "锚点不唯一：%d" % h.count(ANCHOR)

CARD = '''  <a class="card v" href="''' + href + '''">
    <div class="t"><span class="tag n">★★ M3 T3 放映厅</span><span class="tag d">26 知识点 / 101 帧</span>T3 模型评估 · 精读动画深度版</div>
    <div class="m">''' + href + '''</div>
    <div class="d"><b>2026-10-27 新做。</b>⭐ <b>按官方课件 M3T3 做的逐知识点动画片</b>，空格推进、每个知识点配总结卡＋一道自测（共 24 道）。⚠⚠⚠ <b>专门讲清了混淆矩阵的摆法冲突</b>：Canvas 讲义是正类在前 <code>[[TP,FN],[FP,TN]]</code>，复习课件和 sklearn 是负类在前 <code>[[TN,FP],[FN,TP]]</code>，<b>两张图并排画出来——四个计数完全相同，变的只是位置，所以绝不能背位置</b>。⭐⭐ 核心数字全部复算核对：<b>TP=4 FP=2 FN=1 TN=5 ⇒ acc .75 / pre 4/6≈.667 / rec 4/5=.80 / F1 8/11≈.727</b>；<b>考纲示例 TP=18 FP=12 FN=6 TN=164 ⇒ .91 / .60 / .75 / ≈.667</b>；<b>代价 5·FN+1·FP：阈值 0.5 得 34、0.3 得 22，代价改成相等就翻转成 10 vs 14</b>；<b>ROC 四样本梯形法与配对法都给 AUC = 0.75</b>。⭐ 最锋利的一页：<b>平均 BCE 从 0.580352 降到 0.369420，却有正例停在 0.4859 一直判错</b>（它的两个隐藏 ReLU 都是 0）。⚠ 另含<b>防泄漏五步</b>、<b>五个坑</b>、<b>早停保留最好检查点</b>、<b>稀有正例 recall .80 而 precision 仅 .075</b>、<b>五条评分点清单</b>。</div>
  </a>
'''

io.open(HUB, "w", encoding="utf-8").write(h.replace(ANCHOR, CARD + ANCHOR, 1))
print("✓ 已登记进 ★总入口.html（排在 M3T1 / M3T2 片子之后）")
