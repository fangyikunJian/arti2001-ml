# -*- coding: utf-8 -*-
"""CS229 讲座 L20 · 强化学习的调试与诊断 —— 2026-10-15 新做。CS229 的最后一讲。

这一讲是整个 CS229 里最实用的一讲之一：当强化学习做不出效果时，
怎么判断该修模拟器、该修奖励函数、还是该修算法。Ng 用自主直升机项目做案例。
后半讲策略搜索（直接找策略，不绕价值函数）与 REINFORCE。

⚠ 时间码全部用 源码/tools/retime.py 的字符位置插值反查过（L20 的 timed 只覆盖 10.1%）。
   见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹且写成一行；LaTeX 两个反斜杠
  · note 的 y ≤ 405；matrix 底边 = y+(rows-1)*ch+(ch-3)；boxNode 底边 = y+h，都 ≤ 405
  · says() 默认 y=150，文字框约 [137,169]，紧跟其下的 note 至少 y≥178
  · 补充镜用到的辅助函数，主文件必须定义
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
var CFG={title:"CS229 讲座 L20 · 强化学习的调试与诊断",
  subtitle:"三句话诊断法 · 策略搜索 · REINFORCE · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=pLhPQynL0tY&t="};

function says(ts,en,y){
  note("🎙 Ng "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 决策树的一个分叉：条件 → 结论 ── */
function fork(x,y,w,cond,yes,no){
  boxNode(x,y,w,54,cond,"b");
  boxNode(x-w*0.30,y+76,w*0.56,54,yes,"g");
  boxNode(x+w*0.74,y+76,w*0.56,54,no,"r");
  link(x+w/2,y+54,x-w*0.30+w*0.28,y+76);
  link(x+w/2,y+54,x+w*0.74+w*0.28,y+76);}

/* ── 网格世界 ── */
function grid(x0,y0,cw,ch,cols,rows,cb){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++){
    var v=cb(i,j); if(v===null) continue;
    boxNode(x0+i*cw, y0+j*ch, cw-6, ch-6, v[0], v[1]||"");}}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讲座 L20","强化学习的调试与诊断",
      "全课最后一讲");},
    "这是 CS229 的最后一讲。Ng 开场说：<b>欢迎来到本季度的最后一课，对网上的观众来说——欢迎收看季终集。</b><br><b>⭐ 这一讲是整门课里最实用的几讲之一，而且它回答的是一个你迟早会亲自撞上的问题。</b><br><b>场景是这样的</b>：<b>你照着前面几讲做完了全部工作——建好模拟器、写好奖励函数、跑完强化学习算法，拿到了一个控制器。</b><b>然后你把它装上真的直升机，结果它飞得比人类飞行员差得多。</b><br><b>⚠ 接下来该做什么？</b><b>是去改进模拟器？是去改奖励函数？还是去换一个更好的强化学习算法？</b><br><b>⭐ 这三条路都很花时间，而且 Ng 说这是一个多年的项目——选错方向的代价是以月计的。</b><br><b>这一讲给出的是一套能真正判断方向的诊断法，只用三句话。</b><br><b>后半段讲一类之前没提过的算法：策略搜索——直接去找策略，根本不经过价值函数。</b><b>那段著名的「直升机倒着飞」的视频，用的就是这类算法。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from l20_shots import EXTRA
from l20_more2 import EXTRA2
EXTRA.update(EXTRA2)      # 分两批补的第二镜，合并成一张表

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


import l20_diag, l20_ps
from l20_shots import add_more
l20_diag.add(KP)   # 直升机项目 → 三条路的困境 → 三句话 → 三个诊断 → 工作流与判断
add_more(KP)       # 诊断法的一般形式 / 改算法的岔路 / RL 前景 / 人类参照 / 整条线收束
l20_ps.add(KP)     # 策略搜索是什么 → 选策略形式 → 随机策略 → REINFORCE → 什么时候用
from l20_more2 import add_more2
add_more2(KP)      # 优化目标 / 策略的形状 / 梯度的来历 / AlphaGo / 机器狗

C.append(r'''KP("完 · 季终集",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 L20 · 完","强化学习的调试与诊断",
      "三句话，和一整门课");},
    "收一下这一讲，也收一下整条强化学习的线。<br><b>★★★ 这一讲最值钱的东西是那套三句话诊断法。</b><b>场景是：控制器飞得比人类飞行员差得多，而你面前有三条都很花时间的路——改模拟器、改奖励函数、改算法。</b><br><b>Ng 的办法是先写下三句话</b>：<b>① 模拟器是准的；② 强化学习算法确实在模拟器里最大化了期望回报；③ 最大化这个期望回报，确实对应着「飞得好」。</b><b>⭐ 关键在于：如果这三句都成立，那学出来的控制器就应该飞得很好。</b><b>既然它没有，那至少有一句是假的——而三句话正好对应三条路。</b><br><b>然后用三个测试把假的那句找出来。</b><b>测试一：它在模拟器里飞得好吗？</b><b>⭐ 如果在模拟器里飞得好、在真机上不行，那问题就是模拟器——去采更多数据、学一个更好的模型。</b><b>测试二：拿人类飞行员来比。</b><b>用你自己那个奖励函数去算人类飞行的收益，和算法的收益比一比。</b><b>⭐ 如果算法的收益比人类低，说明算法没有真正在最大化——该去改算法。</b><b>★★★ 测试三是最精彩的：如果算法的收益反而比人类高，可人类明明飞得更好——那只能说明你的奖励函数写错了。</b><b>⚠ 因为「把你写的那个和式最大化」已经做到了，可结果并不是你想要的飞行。</b><br><b>⭐ Ng 还讲了两件关于工作流的事，都很实在。</b><b>第一，该修的问题会不断移动</b>——<b>项目前两个月可能一直是「模拟器不够好」，解决之后暴露出来的就是下一个最重要的问题，如此往复。</b><b>第二，⚠ 他特意说这不是一套刚性的数学流程</b>：<b>实际做的时候是一个团队把三个测试的证据摆在一起，然后判断「模拟器也许不够好，但可能够用了，我们先去弄别的」。</b><b>判断是跑不掉的。</b><br><b>后半段讲了策略搜索。</b><b>前面所有方法的路线都是：先估价值函数，再用 argmax 导出策略。</b><b>⭐ 而直接策略搜索跳过中间那一步，直接去找一个好策略。</b><b>做法是先给策略定一个形式（Ng 类比逻辑回归：当初也是「先定下 sigmoid 这个形式」），再对它的参数 θ 做梯度上升。</b><b>它用的是随机策略——输出的不是一个动作，而是各个动作的概率。</b><b>★ 算法叫 REINFORCE：跑一条轨迹、算出这条轨迹的总回报、然后朝着「让这条轨迹更可能发生」的方向更新 θ，更新的幅度乘上总回报。</b><b>⇒ 回报高的轨迹被加强，回报低的被削弱，名字就是这么来的。</b><br><b>⚠ 什么时候用哪个？Ng 给的判据很清楚：看任务是不是「低层控制」。</b><b>把车保持在直路上、把倒立摆立住——这类任务的最优策略形状简单，策略搜索很合适。</b><b>⭐ 而下棋、围棋、或者「先超过这辆车再躲开那个行人」这种需要多步推理的任务，最优策略没法用一个简单函数表示，这时价值函数近似更有希望。</b><b>Ng 还给了自己的经历：他最早飞直升机用的就是直接策略搜索，那段倒着飞的视频用的也是策略搜索；但要飞更复杂的机动，就得转向价值函数近似那一类方法。</b><br><b>⭐ 最后说一句整条线。</b>从 L16 把问题形式化成 MDP，到 L17 用值迭代解出来，到 L18 处理连续状态，到 L19 的 LQR 精确解，再到这一讲的调试方法和策略搜索——<b>这五讲合起来是一套完整的工程能力：不只是「会这些算法」，而是「做不出来时知道该查哪儿」。</b><b>⚠ 而 L20 教的恰恰是其中最难学、也最少被写进教科书的那一半。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讲座 L20 · 强化学习的调试与诊断</title>")
io.open("cs229-L20.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-L20.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ l20_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
