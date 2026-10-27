# -*- coding: utf-8 -*-
"""M3 T3《模型评估：训练证据、停止与泛化》精读动画版 —— 2026-10-27。

底料：M3材料/课件/M3T3_Model_Evaluation.pptx（裁后 17 页，带 13155 字符备注讲稿）
      ＋ 精读/data/M3T3.json ＋ M3材料/Canvas讲义/T0_考纲与考试形式.txt

⚠ 课件上每个数字都复算核对过：
   混淆矩阵 TP=4 FP=2 FN=1 TN=5（共 12）⇒ acc .75 / pre 4/6≈.667 / rec 4/5=.80 / F1 8/11≈.727
   考纲示例 TP=18 FP=12 FN=6 TN=164（共 200）⇒ acc .91 / pre .60 / rec .75 / F1 36/54≈.667
   学习率 起始 0.580352；η=0.1→0.574996；η=1→0.533347；η=10→0.371611；η=100→9.965953
   连续训练 0/1/10/50/100 次：0.580352→0.369420；p([1,2]) 0.6615→0.9592；p([−1,−2]) 0.4750→0.4859
   代价 5·FN+1·FP：阈值 0.5 ⇒ 34；阈值 0.3 ⇒ 22；代价相等时 10 vs 14（结论翻转）
   ROC 四样本 A.90(+) B.80(−) C.40(+) D.10(−) ⇒ 梯形法与配对法都给 AUC = 0.75

⚠⚠ 混淆矩阵摆法：两份官方材料是反的（Canvas 讲义正类在前，复习课件负类在前）。
   片中按课件自己给的安全办法讲：先定正类、再读行列标签逐格确认，别背位置。

版面预算（2026-10-27 实测）：note 的 y ≤ 386；boxNode/matrix 底边 ≤ 390；
   setEq(…,"top") 那一镜的内容从 y ≥ 196 起；表格末行文字中心 ≤ 下方 note 的 y − 35。
"""
import io, sys, re as _re
sys.stdout.reconfigure(encoding="utf-8")
head = io.open("eng.txt", encoding="utf-8").read()
def js(t): return '"' + t.replace('\\','\\\\').replace('"','\\"') + '"'
C = []

C.append(r'''(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng;
var clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
var CFG={title:"M3 T3 · 模型评估（精读动画版）",
  subtitle:"训练证据 · 停止 · 泛化 · 混淆矩阵 · ROC/AUC · 空格推进 · N 讲解",
  video:""};

/* ── 引课件/讲稿原话（课程片没有讲课视频，所以不是 says）── */
function cite(en,y){ note("📄 课件原话  «"+en+"»",640,y||150,"g"); }

/* ── 2×2 混淆矩阵：cells 按 [左上,右上,左下,右下] 给 ── */
function cmat(x,y,cw,ch,rowlab,collab,cells,hl){
  var i;
  note(collab[0],x+cw*0.5,y-14,"d"); note(collab[1],x+cw*1.5,y-14,"d");
  note(rowlab[0],x-78,y+ch*0.5+5,"d"); note(rowlab[1],x-78,y+ch*1.5+5,"d");
  for(i=0;i<4;i++){
    var r=Math.floor(i/2), c=i%2;
    boxNode(x+c*cw, y+r*ch, cw-8, ch-8, cells[i], (hl&&hl.indexOf(i)>=0)?"g":"b");
  }
}

/* ── ROC 画布：把 (FPR,TPR) 映到画布坐标 ── */
function rocxy(f,t,x0,x1,yb,yt){ return [x0+(x1-x0)*f, yb-(yb-yt)*t]; }
function rocpath(pts,x0,x1,yb,yt){
  var out=[],i; for(i=0;i<pts.length;i++) out.push(rocxy(pts[i][0],pts[i][1],x0,x1,yb,yt));
  return out;
}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("M3 T3 · 模型评估","训练证据 · 停止 · 泛化",
      "降下去了，凭什么相信它在新数据上也行");},
    "前两讲都在问同一类问题：<b>怎么把参数调好</b>。<b>T3 问的是另一个问题：调好之后，凭什么相信它在新数据上也行。</b><br><b>⭐ 讲稿把分工说得很干净</b>：<b>Topic 2 explained how to calculate and implement updates. Topic 3 now interprets the resulting training evidence.</b>——<b>T1、T2 讲的是优化，T3 讲的是评估</b>。<br><b>副标题三个词就是三块</b>：<b>training evidence</b>（训练过程留下的证据怎么读）、<b>stopping</b>（什么时候停）、<b>generalisation</b>（在没见过的数据上的表现）。<br><b>⭐ 而讲稿第一页就把这一讲的全部依赖列全了，这句值得抄下来</b>：<b>可靠的结论依赖四件事——受保护的数据划分、正确构造的指标、合适的阈值，以及对泄漏 / 不平衡 / 抽样 / 漂移的警觉。</b><br><b>⚠ 这一讲有一个和别处不同的气质：它满篇都是限定词。</b><b>can、but also、does not by itself、not proof</b>——<b>这些词不是客套，它们就是考点</b>。<b>把限定词写进答案，才是满分结构。</b><br><b>⚠ 考试：110 分钟、100 分、开卷；20 道选择每题 3 分，4 道扩展题每题 10 分。T3 在考纲里占六条。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from m3t3film_shots import EXTRA

def KP(name, shots, summ, quiz, t=0):
    extra = EXTRA.get(name)
    if extra:
        shots = list(shots) + [extra]
        EXTRA.pop(name)
    _kpn[0] += 1
    n = _kpn[0]
    nm = '%d · %s' % (n, _re.sub(r'^\s*\d+\s*·\s*', '', name))
    b=['KP(%s,function(){'%js(nm)]
    for scene,narr,sec in shots:
        b.append('  S(%d,function(){%s},%s);'%(sec,scene,js(narr)))
    fields=",".join('%s:%s'%(k,js(v)) for k,v in summ.items() if v and k!='kp')
    b.append('  SUM(%d,%d,{%s});'%(t,n,fields))
    quiz = fix_quiz(quiz, n)
    opts=",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(%d,%d,{t:%s,o:[%s],a:%d,w:%s});'%(t,n,js(quiz['t']),opts,quiz['a'],js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))


import m3t3film_a, m3t3film_b
m3t3film_a.add(KP)   # 分工 → 路线图 → 诊断三模式 → 划分角色 → 防泄漏 → 学习率 → 连续训练 → 停止 → 纪律 → 五个坑
m3t3film_b.add(KP)   # 混淆矩阵 → 摆法冲突 → 四个指标 → F1 → 换正类 → 基线 → 代价 → ROC → AUC → 边界 → 评分点

C.append(r'''KP("完 · 这一讲要带走的七件事",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("M3 T3 · 完","模型评估",
      "划分 → 停止 → 混淆矩阵 → precision/recall → ROC");},
    "收一下，七件事。<br><b>① 三个划分各一个角色</b>：<b>训练拟合、验证选择、测试估计</b>。⭐⭐ 最该背的一句是：<b>拿测试数据做决定，它就变成了验证数据</b>——<b>不是「不太好」，是性质变了</b>。⚠ <b>阈值和停止点是「决定」，不是参数，所以归验证管</b>。<br><b>② 防泄漏五步</b>：<b>先划分 → 只用训练集算填补与缩放参数 → 把学到的参数应用到验证/测试（不要重新拟合）→ 用验证结果做选择 → 全部固定后在测试集上评估一次</b>。⚠ <b>训练集拟合的不只是权重，还包括预处理参数</b>——这是泄漏最常见的入口。<br><b>③ 诊断要带限定词</b>。<b>训练差 ⇒ 可能容量不足/优化不够/预处理差/数据问题，本身不证明欠拟合</b>；<b>训练强而验证差 ⇒ 可能过拟合，但要先排除分布差异、验证集过小、泄漏</b>；⚠⚠ <b>两边接近也可能是「两边都差」</b>，<b>所以要和基线比</b>。<br><b>④ 平均会骗人</b>。⭐ 那张连续训练表是全讲最锋利的证据：<b>平均 BCE 从 0.580352 降到 0.369420，可有一个正例的概率只从 0.4750 爬到 0.4859，始终在 0.5 以下、一直判错</b>。<b>机制是它的两个隐藏 ReLU 都是 0，分数只剩输出偏置在撑。</b>⚠ <b>跑满 100 次就停，既不证明收敛、不证明全局最优、也不证明泛化。</b><br><b>⑤ 混淆矩阵先定正类</b>。⚠⚠⚠ <b>两份官方材料的摆法是反的</b>（Canvas 讲义正类在前 [[TP,FN],[FP,TN]]，复习课件和 sklearn 负类在前 [[TN,FP],[FN,TP]]），<b>所以绝不能背位置</b>。<b>课件自己给的安全办法是：行是真实、列是预测，先固定正类，再逐个观测归格，四格之和 = 样本数，这一步查完才算指标。</b><br><b>⑥ 四个指标与两个分母</b>：<b>Accuracy = (TP+TN)/N = 9/12 = 0.75</b>；<b>Precision = TP/(TP+FP) = 4/6 ≈ 0.667，条件是「我预测为正的那一组」</b>；<b>Recall = TP/(TP+FN) = 4/5 = 0.80，条件是「真实为正的那一组」</b>；<b>F1 = 2TP/(2TP+FP+FN) = 8/11 ≈ 0.727</b>。⚠ <b>F1 不含 TN</b>。<br><b>⑦ ROC 与 AUC</b>：<b>FPR 横轴、TPR 纵轴；从 (0,0) 全判负走到 (1,1) 全判正；加一个正例往上走，加一个负例往右走，分数相同的必须一起加入 ⇒ 画出一段斜线</b>。<b>梯形法与配对法要互相验算</b>——四样本那个例子两种方法都给 <b>AUC = 0.75</b>。⚠⚠ <b>AUC 只衡量排序，不衡量校准、也不衡量错误代价</b>；<b>真正要用的那个阈值，仍然要靠代价和场景来定</b>（本例 <b>5·FN + 1·FP：阈值 0.5 得 34，阈值 0.3 得 22</b>；<b>代价改成相等就翻转成 10 vs 14</b>）。");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>M3 T3 · 模型评估（精读动画版）</title>")
io.open("m3t3-film.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("m3t3-film.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ m3t3film_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
