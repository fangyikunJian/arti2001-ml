# -*- coding: utf-8 -*-
"""M3 T2《训练神经网络：激活、损失、隐藏层梯度与实现》精读动画版 —— 2026-10-27。

底料：M3材料/课件/M3T2_Activation_Loss.pptx（裁后 20 页，带 13454 字符备注讲稿）
      ＋ 精读/data/M3T2.json（同一批内容的逐页版）
      ＋ M3材料/Canvas讲义/T0_考纲与考试形式.txt

⚠ 课件上每个数字都复算核对过（build 之前跑过一遍 Python）：
   x=[1,2] y=1 η=0.1
   隐藏1 w=[0.2,0.4] b=0.1 ReLU ⇒ z₁=1.1  h₁=1.1（激活）
   隐藏2 w=[−0.5,0.3] b=−0.2 ReLU ⇒ z₂=−0.1 h₂=0（不激活）
   输出 v=[0.7,−0.4] c=−0.1 sigmoid ⇒ s=0.67 p=0.661503 L=0.413241
   ∂L/∂s = −0.338497 → ×v₁=0.7 → −0.236948 → ×g′(z₁)=1 → −0.236948 → ×x₂=2 → −0.473896
   w₁₂ ← 0.4+0.0473896 = 0.447390 ; v₁ ← 0.7+0.0372347 = 0.737235
   更新后 z₁=1.242169 s=0.849619 p=0.700487 L=0.355979
   MSE vs BCE（y=1, p=0.01）：−0.009801 vs −0.990000，正好差 101 倍

⚠ 这是课程片不是 CS229 片，没有讲课视频，所以没有 says()；引课件/讲稿原话用 cite()。

版面预算（2026-10-27 在 1440×860 实测，见 tools/audit_film.py 顶部）：
  · 讲解条（#cap）顶边 y=403；note 的文字框是 [y−14, y+4]
  · ⇒ note 的 y ≤ 386；boxNode / matrix 的底边 ≤ 390
  · setEq(…,"top") 的方程占到 y=194，同一镜的内容要从 y ≥ 196 开始
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
var CFG={title:"M3 T2 · 训练神经网络（精读动画版）",
  subtitle:"激活 · 损失 · 隐藏层梯度 · 实现 · 全程一个两层算例 · 空格推进 · N 讲解",
  video:""};

/* ── 引课件/讲稿原话（课程片没有讲课视频，所以不是 says）── */
function cite(en,y){ note("📄 课件原话  «"+en+"»",640,y||150,"g"); }

/* ── 2 输入 → 2 隐藏 → 1 输出 的小网络 ── */
function net2(cx,cy,lab){
  boxNode(cx-520,cy-70,150,46,lab[0],"b");
  boxNode(cx-520,cy+24,150,46,lab[1],"b");
  boxNode(cx-240,cy-70,190,46,lab[2],"v");
  boxNode(cx-240,cy+24,190,46,lab[3],"v");
  boxNode(cx+110,cy-23,210,46,lab[4],"g");
  link(cx-370,cy-47,cx-240,cy-47); link(cx-370,cy-47,cx-240,cy+47);
  link(cx-370,cy+47,cx-240,cy-47); link(cx-370,cy+47,cx-240,cy+47);
  link(cx-50,cy-47,cx+110,cy); link(cx-50,cy+47,cx+110,cy);
}

/* ── 激活函数曲线（画在 axes 里；z 从 −4 到 4）── */
function actcurve(kind,x0,x1,ybase,ytop,mid){
  var span=ybase-ytop, zc=mid!=null?mid:(ybase+ytop)/2;
  return fn(function(x){
    var z=-4+8*(x-x0)/(x1-x0), v;
    if(kind==="sig"){ v=1/(1+Math.exp(-z)); return ybase-span*v; }
    if(kind==="tanh"){ v=Math.tanh(z); return zc-(span/2)*v; }
    if(kind==="relu"){ v=Math.max(0,z)/4; return ybase-span*Math.min(1,v); }
    if(kind==="leaky"){ v=(z>0?z:0.35*z)/4; return zc-(span/2)*Math.max(-1,Math.min(1,v*2)); }
    return ybase;
  },x0,x1,90);
}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("M3 T2 · 训练神经网络","激活 · 损失 · 隐藏层梯度 · 实现",
      "同一个损失，怎么喂给隐藏层");},
    "T1 讲完了<b>一个神经元</b>怎么走完「前向 → 损失 → 梯度 → 更新」。<b>T2 问的是同一条链上的下一个问题：同一个损失，怎么把梯度送给隐藏层。</b><br><b>⭐ 讲稿的原话值得抄下来</b>：<b>Topic 1 ended with an output-layer update. This topic asks how the same loss supplies gradients to hidden weights.</b>——注意是「<b>同一个</b>损失」：<b>隐藏层没有自己的目标，它靠链式法则从最终损失那里拿方向</b>。<br><b>⚠ 这一讲真正的新东西只有两个</b>：<b>① 激活和损失的选择与搭配</b>（T1 只用了 sigmoid + BCE 一种）；<b>② 梯度要穿过隐藏层</b>。<b>剩下的 batch/epoch 和自动微分，是把前两件事放大到一批数据、再放进代码里。</b><br><b>⭐ 全片还是只用一个算例</b>：<b>x = [1, 2]、y = 1、两个 ReLU 隐藏单元、一个 sigmoid 输出</b>。<b>其中第二个隐藏单元恰好不激活</b>——这个设计很妙，它让「ReLU 归零」在同一个例子里就能看见。<br><b>⚠ 考试：110 分钟、100 分、开卷；20 道选择每题 3 分，4 道扩展题每题 10 分。T2 在考纲里占六条，这一讲每一块都对得上。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from m3t2film_shots import EXTRA

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


import m3t2film_a, m3t2film_b
m3t2film_a.add(KP)   # 分工 → 路线图 → 塌缩 → 两个身份 → 数值表 → z=0 → 饱和 → 死亡ReLU → tanh → 选法 → 取舍
m3t2film_b.add(KP)   # 损失匹配 → MSE vs BCE → 配对表 → 四因子 → 算例 → 纪律 → 归零 → batch/epoch → 形状 → autodiff → 答题

C.append(r'''KP("完 · 这一讲要带走的六件事",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("M3 T2 · 完","训练神经网络",
      "激活 → 损失 → 隐藏梯度 → 批量 → 实现");},
    "收一下，六段路线图就是答题提纲。<br><b>① 激活</b>：<b>每个激活有两个身份——前向的值 g(z) 和反向的斜率 g′(z)，两件事互不相干</b>。⭐ 讲义说得很狠：<b>大的输出不代表大的梯度</b>。三个数值必须会默写：<b>σ(2)=0.881 导数 0.105</b>、<b>tanh(2)=0.964 导数 0.0707</b>、<b>ReLU(2)=2 导数 1</b>。⚠⚠ 本课约定 <b>ReLU′(0)=0、LeakyReLU′(0)=α</b>。<br><b>② 塌缩</b>：<b>W₂(W₁x+b₁)+b₂ 仍是一个仿射映射</b>，带数字就是 <b>3(2x+1)+4 = 6x+7</b>。<b>光加深度，不会多出一条弯的边界。</b><br><b>③ 损失</b>：<b>要同时匹配目标的类型和输出的含义</b>。⭐⭐ 最该记的是那组对比——<b>y=1、p=0.01 时，半平方误差的 ∂L/∂z = (p−y)p(1−p) = −0.009801，而 BCE 的 = p−y = −0.990000，正好差 101 倍</b>。<b>原因是 sigmoid 在 p=0.01 处的斜率 p(1−p) 本身就极小，而 BCE 的 −log 恰好把它约掉了。</b>⚠ 这是 <b>sigmoid + BCE 这一对</b>的优点，不是 BCE 单独的优点。<br><b>④ 隐藏梯度</b>：⭐⭐⭐ <b>∂L/∂wⱼᵢ = (p − y)·vⱼ·g′(zⱼ)·xᵢ</b>，四个因子对应路径上的四步。本例 <b>−0.338497 → ×0.7 → ×1 → ×2 = −0.473896</b>，<b>w₁₂ 从 0.4 变成 0.447390</b>，更新后 <b>p 从 0.661503 升到 0.700487</b>。⚠⚠ 两条纪律：<b>所有因子用同一次前向、同一组更新前的参数</b>；<b>全部梯度算完才更新</b>。⚠ <b>z₂ = −0.1 < 0，所以第二个隐藏单元两处全零</b>——它的输入权重梯度是 0，它的输出权重梯度 (p−y)·h₂ = (p−y)·0 也是 0。<br><b>⑤ 批量</b>：<b>batch 供一次更新，epoch 是把训练集过一遍</b>。<b>100 个样本、批大小 20 ⇒ 一个 epoch 5 次更新，3 个 epoch 15 次</b>。⚠⚠ <b>平均损失在降，不代表每个样本都变好</b>——两个样本的梯度 −0.2 和 +0.6，平均 +0.2，对第一个样本方向是反的。<br><b>⑥ 实现</b>：<b>代码把观测存成行（X 是 (N,d)、W 是 (d,h)），手推把输入写成列，所以代码里的 W 是手推版本的转置</b>——<b>转置只是行列互换，网络没变</b>。⭐⭐ <b>自动微分三个角色要分清：记录前向、按链式法则求导、而更新参数是优化器干的</b>。⚠ 它<b>不替你选目标、不修数据泄漏、也不保证学习率合适</b>。");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>M3 T2 · 训练神经网络（精读动画版）</title>")
io.open("m3t2-film.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("m3t2-film.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ m3t2film_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
