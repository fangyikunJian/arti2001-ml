# -*- coding: utf-8 -*-
"""M3 T1《神经网络》精读动画版 —— 2026-10-27 新做。

底料：M3材料/课件/M3T1_NeuralNetworks.pdf（35 页，已逐页看过）
      ＋ 精读/data/M3T1.json（同一批内容的逐页版）
      ＋ M3材料/Canvas讲义/T0_考纲与考试形式.txt（考纲与示例题）

⚠ 课件上每个数字都复算核对过：
   x=(1,2) y=1 w=(0.2,0.4) b=0.1 ⇒ z=1.1 ⇒ p=0.750260 ⇒ L=0.287335
   p(1−p)=0.187370 ⇒ δ=p−y=−0.249740 ⇒ 梯度 −0.249740 / −0.499480 / −0.249740
   η=0.1 更新后 w=(0.224974, 0.449948) b=0.124974 ⇒ z=1.249844 p=0.777273 L=0.251964
   走错方向（加号）：0.2+0.1×(−0.249740)=0.175026

⚠ 这是课程片不是 CS229 片，没有讲课视频，所以没有 says()；引课件原话用 cite()。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹且写成一行；LaTeX 两个反斜杠
  · note 的 y ≤ 405（2026-10-27 实测：1440×860 遮挡从 457 起，1280×620 时 432，405 留足余量）
  · matrix 底边 = y+(rows-1)*ch+(ch-3)；boxNode 底边 = y+h，都 ≤ 405
  · curve(pts,cls) 内部已加 "fit "；fn() 只算点不画线；axes 认 x0/x1/y0/y1
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
var CFG={title:"M3 T1 · 神经网络（精读动画版）",
  subtitle:"一个神经元 · 一次前向传播 · 一次学习步 · 全程一个算例 · 空格推进 · N 讲解",
  video:""};

/* ── 引课件原话（课程片没有讲课视频，所以不是 says）── */
function cite(en,y){ note("📄 课件原话  «"+en+"»",640,y||150,"g"); }

/* ── 一个神经元：输入圈 → 权重 → Σ → g → 输出 ── */
function neuron(cx,cy,xs,ws,b,zt,at){
  var n=xs.length, i, top=cy-(n-1)*46/2;
  for(i=0;i<n;i++){
    var y=top+i*46;
    boxNode(cx-470,y-21,120,42,xs[i],"b");
    boxNode(cx-300,y-19,96,38,ws[i],"v");
    link(cx-350,y,cx-300,y); link(cx-204,y,cx-70,cy);
  }
  if(b){ boxNode(cx-120,cy-96,110,38,b,"y"); link(cx-65,cy-58,cx-40,cy-28); }
  boxNode(cx-70,cy-30,80,60,"Σ","");
  link(cx+10,cy,cx+70,cy);
  boxNode(cx+70,cy-26,130,52,"g(·)","v");
  link(cx+200,cy,cx+260,cy);
  boxNode(cx+260,cy-26,150,52,at||"a","g");
  if(zt) note(zt,cx+40,cy-44,"y");
}

/* ── sigmoid 曲线（画在 axes 里）── */
function sigcurve(x0,x1,ybase,ytop,cls){
  return fn(function(x){
    var z=-6+12*(x-x0)/(x1-x0);
    return ybase-(ybase-ytop)/(1+Math.exp(-z));},x0,x1,90);
}

/* ── 2×2 的点阵（画 XOR）── */
function quad(cx,cy,d,lab){
  var pos=[[-1,-1],[-1,1],[1,-1],[1,1]], i;
  for(i=0;i<4;i++){
    boxNode(cx+pos[i][0]*d-46, cy-pos[i][1]*d-30, 92, 60, lab[i][0], lab[i][1]);
  }
}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("M3 T1 · 神经网络","一个神经元、一次前向传播、一次学习步",
      "全程只用一个算例");},
    "这一讲是 M3 的地基。<b>副标题本身就是提纲</b>：<b>一个神经元</b>长什么样、<b>一次前向传播</b>怎么从输入算到预测、<b>一次学习步</b>怎么把参数改一次。<br><b>⭐ 它最聪明的地方是只用一个算例，从头贯穿到尾</b>：<b>输入 x = (1, 2)，目标 y = 1，权重 0.2 和 0.4，偏置 0.1</b>。<b>后面所有的数字——z = 1.1、p = 0.7503、L = 0.2873、δ = −0.2497、更新后的 0.7773——全都是从这四个数算出来的。</b><br><b>⚠ 所以这一讲的正确学法不是背概念，是把这个算例亲手算一遍。</b>算通了，神经网络给人的那种「层数多、参数多」的压迫感就没了——<b>因为每个神经元做的事完全一样，把一个讲透，剩下的只是重复和连接。</b><br><b>⚠ 考试形式先记住</b>：<b>110 分钟、100 分、开卷纸笔</b>；<b>20 道选择每题 3 分，4 道扩展题每题 10 分</b>。考纲原话说得很硬：<b>只给出正确的最终数字，可能不足以体现所需的理解</b>——所以中间步骤必须写。");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from m3t1film_shots import EXTRA

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


import m3t1film_a, m3t1film_b
m3t1film_a.add(KP)   # 骨架 → 神经元三动作 → 前向传播 → 置信度不等于学习 → XOR → 网络 → 激活 → 非线性
m3t1film_b.add(KP)   # 损失 → 计算图 → 敏感度 → 链式法则 → 目标 → δ → 更新 → 减号 → 总图

C.append(r'''KP("完 · 五步走完一次学习",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("M3 T1 · 完","神经网络",
      "Predict → Target → Gradients → Update → Check");},
    "收一下，整讲就是五步。<br><b>① Predict（预测）</b>：<b>每个输入乘权重、连同偏置求和得到分数 z、再过激活函数</b>——这三步就是神经元的全部定义。本例 <b>z = 0.2×1 + 0.4×2 + 0.1 = 1.1</b>，<b>p = σ(1.1) = 0.750260</b>，<b>L = −log p = 0.287335</b>。⚠ 记住 <b>概率和标签是两件事</b>：p 是估计的机会，「类别 1」是拿它跟 0.5 比之后的决定。<br><b>② Target（目标）</b>：<b>y = 1</b>。⭐ 它必须单独算一步，因为<b>没有目标就没有方向</b>——把权重调大会让 p 上升，这是好是坏完全取决于 y。<br><b>③ Gradients（梯度）</b>：⭐⭐ <b>δ = p − y = −0.249740</b>，然后 <b>∂L/∂wᵢ = δ·xᵢ</b>、<b>∂L/∂b = δ</b>。<b>三个梯度分别是 −0.249740、−0.499480、−0.249740</b>；<b>w₂ 的梯度是两倍，因为 x₂ = 2</b>。<br><b>④ Update（更新）</b>：<b>θ ← θ − η·梯度</b>，η = 0.1。<b>梯度是负的，减去负数等于加上正数</b>，所以三个参数都变大：<b>w = (0.224974, 0.449948)，b = 0.124974</b>。⚠ <b>用加号会走反</b>：0.2 + 0.1×(−0.249740) = 0.175026，p 下降、损失上升。<br><b>⑤ Check（检查）</b>：重做一次前向，<b>z = 1.249844、p = 0.777273、L = 0.251964</b>，三个量都朝好的方向动了。⚠ 但课件特意加了一句：<b>改善只发生在这一个样本上</b>。<br><br><b>中间那一大段讲的是「为什么要多层」。</b>⭐ <b>单个 sigmoid 神经元的决策边界是一条直线</b>，训练只能移动和旋转它，<b>永远不能把它掰弯、也不能再加一条</b>；而 <b>XOR 的同类点落在对角线上，任何直线都分不开</b>。<b>⚠ 但光加层还不够</b>：<b>h = 2x+1 再 s = 3h+4 代入展开是 s = 6x+7，还是一条直线</b>——<b>没有非线性，多少层都塌回一层</b>。<b>插进 ReLU 之后在 x = −0.5 处出现折点，很多折点被下一层组合起来，才画得出灵活的形状。</b><br><b>⭐ 最后两个最容易混的区分</b>：<b>反向传播算梯度、梯度下降迈步子，光算斜率什么都不会动</b>；<b>梯度给方向、学习率给距离，而「下坡」只是一个局部的承诺——步子太大会跨过谷底落得更高</b>。");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>M3 T1 · 神经网络（精读动画版）</title>")
io.open("m3t1-film.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("m3t1-film.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ m3t1film_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
