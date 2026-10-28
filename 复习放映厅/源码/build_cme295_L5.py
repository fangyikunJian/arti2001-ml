# -*- coding: utf-8 -*-
"""CME295 讲座 L5 · LLM Tuning —— 2026-10-28 新做。

这一讲讲 alignment 的**后半段**：偏好调优（preference tuning）。分两场：
  上半场（Afshine）：为什么还要第三步 → 偏好数据怎么来 → RL 基础与映射 →
    RLHF 第一段（奖励模型、Bradley-Terry、损失推导）→ RL 那一段（KL、advantage、
    value function、PPO-Clip、KL penalty、四个模型）→ RL 的五个挑战 → Best-of-N。
  下半场（Shervine）：Best-of-N 的延迟论证 → DPO（损失、四步推导、
    「your LM is secretly a reward model」）→ PPO vs DPO 的取舍 → 泰迪熊收尾。

⚠ 这一讲是期末考范围的起点（讲者开场说期末考 L5 到 L9）。
⚠ 本讲的总钥匙（讲者在最后才明说）：**偏好调优不教新事实**，它只是在已有的
   输出分布上，把模型该返回的那一个向人类偏好的一边挪。

底料：CME295/transcripts/L5.txt（969 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L5 build_cme295_L5.py cme295_L5_*.py

引擎的坑（memory/projector-engine-traps.md，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**；里面不许「< 紧跟字母」（坑 11）
  · ⚠ setEq 里的反斜杠要写 \\\\ —— 场景 JS 是 JS 源码，`\\theta` 的 `\\t` 会变制表符（新坑）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=150 ⇒ 其下 note 至少 178；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜两条 note 的 y **至少差 19**（文字框高 18）（坑 12）
  · ⚠ stack()/seq() 自己算几何，⑨⑩ 看不见 ⇒ 底边与末格标签要手算（坑 13）
  · ⚠ 有**居中** setEq 的镜，note 只能落在 [178,265]；setEq(...,"top") ⇒ says 放 206
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
var CFG={title:"CME295 讲座 L5 · 偏好调优",
  subtitle:"偏好对与奖励模型 · RLHF / PPO · Best-of-N · DPO · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=PmW_TMQ3l0I&t="};

function says(ts,en,y){
  note("🎙 Amidi "+ts+"  «"+en+"»",640,y||150,"g");}

function seq(x0,y,toks,cls,bw,bh){
  bw=bw||104; bh=bh||44; var cx=[],i;
  for(i=0;i<toks.length;i++){
    var x=x0+i*(bw+10);
    boxNode(x,y,bw,bh,toks[i],(cls instanceof Array)?cls[i]:(cls||"b"));
    cx.push(x+bw/2);}
  return cx;}

function stack(cx,ytop,items,bw,bh,gap){
  bw=bw||250; bh=bh||32; gap=gap==null?6:gap; var i,ys=[];
  for(i=0;i<items.length;i++){
    var y=ytop+i*(bh+gap);
    boxNode(cx-bw/2,y,bw,bh,items[i][0],items[i][1]||"");
    ys.push(y);
    if(i) link(cx,y,cx,y-gap);}
  return ys;}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L5","偏好调优：怎么把模型「对齐」到人的偏好上",
      "九讲的第 5 讲 · 约 107 分钟");},
    "第五讲，而它的位置很特别 —— <b>讲者开场就说：期末考考 L5 到 L9，也就是「从今天这一讲开始」。</b><br><b>先把这一讲挂到流水线上。</b><b>L4 讲了两步：<u>预训练</u>（学语言是怎么回事）和 <u>SFT 微调</u>（学该生成什么）。</b><b>而这一讲讲第三步：<u>偏好调优</u>（preference tuning）—— SFT 与它合起来叫 alignment，所以这一讲是 alignment 的后半段。</b><br><b>★★★ 这一讲有一把总钥匙，讲者直到最后一分钟才明说，但我建议你从开场就带着它听</b>：<b>「<u>我们不想学新的事实。我们要做的是聚焦在已有的 completion 分布上，并把模型该返回的东西，向人类所偏好的那一边对齐</u>。」</b><br><b>⇒ 这句话能解释这一讲几乎每一个设计</b>：<b>为什么要约束「别离原模型太远」（因为你不是要换一个模型）、为什么数据是<u>成对</u>的而不是标准答案（因为你在表达偏好，不是在教内容）、为什么 Best-of-N 这种<u>一个权重都不改</u>的办法也算一种偏好调优（因为你只需要在已有候选里挑）。</b><br><br><b>⭐ 这一讲的结构值得先知道，因为它是一条很干净的「问题驱动」的线</b>：<b>先给出标准答案 <u>RLHF / PPO</u>，然后把它的代价一笔一笔算清（<u>要四个模型、五个挑战</u>），再给两个「不想付这个代价」的方案 —— <u>Best-of-N</u>（完全不训，把成本挪到推理）和 <u>DPO</u>（把两段变一段，四个模型变两个）。</b><br><b>★ 所以你听的时候可以一直问一个问题：<u>这一步在省什么、又为此付了什么</u>。本讲没有免费的午餐，但每一笔交易都说得很清楚。</b><br><b>⚠ 最后提个醒：这一讲有<u>三个符号陷阱</u>，讲者自己都主动点了出来（他说当初也把他搞糊涂了）。到那一条我会专门标出来。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的四段路线，以及每一段在「省什么、付什么」",640,186,"v");
    stack(250,214,[["① 偏好数据","g"],["成对比较最好标","d"],["⇒ 放弃信息量换可靠","d"],["★ 同一判断用了三次","y"]],340,34,8);
    stack(640,214,[["② RLHF / PPO","b"],["两段式：RM + RL","d"],["⚠ 要四个模型","r"],["⚠ 五个挑战","r"]],340,34,8);
    stack(1030,214,[["③ Best-of-N","y"],["一个权重都不训","d"],["⚠ 成本挪到推理端","r"],["④ DPO ⇒ 两个模型","g"]],340,34,8);
    note("⇒ 听的时候一直问：这一步省了什么、又为此付了什么",640,386,"y");},
    "<b>把路线先摆出来，因为这一讲的方法是「一个比一个更省」地排开的，而顺序本身就是论证。</b><br><b>① 偏好数据怎么来。</b><b>这一段表面上在讲数据收集，<u>其实只有一条判断，而它被用了三次</u>：产出答案 → 改成比较答案；pointwise → 改成 pairwise；细粒度刻度 → 改成二元。<u>三次都是主动放弃信息量，去换标注的可靠性</u>。</b><br><b>② RLHF / PPO。</b><b>标准答案。先训一个<u>奖励模型</u>（它有一条漂亮的性质：训练时成对、使用时逐点），再用 RL 把策略对齐。</b><b>⚠ 代价是：<u>显存里要同时养四个模型</u>，而且有五个实打实的工程挑战。</b><br><b>③ Best-of-N。</b><b>最省事的路：<u>一个权重都不训</u>，生成 N 条用奖励模型挑最好的。</b><b>⚠ 代价是把成本<u>全推到推理端</u> —— 而且讲者给了一个很漂亮的论证：<u>就算钱无限，延迟也救不回来</u>。</b><br><b>④ DPO。</b><b>把两段变一段、四个模型变两个，<u>而且式子里再没有奖励</u>。</b><b>⚠ 代价是分布漂移，<u>而这是内在的，不是实现问题</u>。</b><br><b>★★ 我特别建议你留意第 ④ 段的推导（四步，没有任何额外假设）。</b><b>它的关键一步用到了前面一条看起来只是注解的性质 —— <u>Bradley-Terry 只看分数的差</u>。<u>一个顺带提到的性质，后来成了一个方法能不能成立的承重点</u>，这种事在研究里非常常见，值得体会。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]

def KP(name, shots, summ, quiz, t=0):
    _kpn[0] += 1
    n = _kpn[0]
    nm = '%d · %s' % (n, _re.sub(r'^\s*\d+\s*·\s*', '', name))
    b = ['KP(%s,function(){' % js(nm)]
    for scene, narr, sec in shots:
        b.append('  S(%d,function(){%s},%s);' % (sec, scene, js(narr)))
    fields = ",".join('%s:%s' % (k, js(v)) for k, v in summ.items() if v and k != 'kp')
    b.append('  SUM(%d,%d,{%s});' % (t, n, fields))
    quiz = fix_quiz(quiz, n)
    opts = ",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(%d,%d,{t:%s,o:[%s],a:%d,w:%s});'
             % (t, n, js(quiz['t']), opts, quiz['a'], js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))


import cme295_L5_a, cme295_L5_b, cme295_L5_c, cme295_L5_d
cme295_L5_a.add(KP)   # 第三阶段在改什么 → 四个理由 → 三种形态 → 偏好对怎么造 → 评判者与刻度
cme295_L5_b.add(KP)   # RL 词汇 → 映射到 LLM → 稀疏信号 → RLHF 两段式 → BT → 损失推导 → 成对/逐点
cme295_L5_c.add(KP)   # RM 架构与尺度 → RL 回路 → 别跑太远（reward hacking）→ KL → advantage → PPO-Clip → 四个模型
cme295_L5_d.add(KP)   # 五个挑战 → on/off-policy → Best-of-N → 延迟论证 → DPO → 四步推导 → 取舍与收尾

C.append(r'''KP("完 · 每一步都在交易",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L5 · 完","偏好调优",
      "一把总钥匙 · 四笔交易 · 三个符号陷阱");},
    "收一下这一讲。<br><b>★★★ 先把总钥匙再说一遍，因为它是这一讲唯一需要你背下来的东西</b>：<b>「<u>我们不想学新的事实。我们要做的是聚焦在已有的 completion 分布上，并把模型该返回的东西，向人类所偏好的那一边对齐</u>。」</b><br><span class='k'>⭐ 而这句话在本讲里拿到了一个<b>数学形式的证明</b>：DPO 推导出的最优策略是 <b>π* ∝ π_ref · exp(r/β)</b> —— <u>最优策略只是「把参考策略按奖励重新加权」</u>。π_ref 给 0 概率的回答，乘任何指数还是 0。<b>偏好调优变不出参考模型本来就不会说的东西。</b></span><br><br><b>★★ 然后是四笔交易，每一笔都写清了价码。</b><br><span class='w'><b>交易一（数据）</b>：放弃信息量，换标注可靠性。产出→比较、pointwise→pairwise、细刻度→二元，<u>同一条判断用了三次</u>。⚠ 但这个方向不是无条件的 —— <b>放弃信息量是为了避噪声，评判者本身可靠时就不必放弃</b>。</span><br><span class='w'><b>交易二（RLHF/PPO）</b>：拿<u>四个模型 + 五个挑战</u>，换<u>最高的性能上限</u>。而「别跑太远」不是正则，是目标的另一半 —— 它有三个理由：灾难性遗忘、<b>reward hacking</b>、训练不稳。</span><br><span class='w'><b>交易三（Best-of-N）</b>：拿<u>每次服务都变贵</u>，换<u>一个权重都不用训</u>。⭐ 而讲者那个论证最漂亮：<b>就算钱无限，N 条里最慢那条的延迟也救不回来</b> —— 最大值的分布比单个样本右移。</span><br><span class='k'><b>交易四（DPO）</b>：拿<u>分布漂移</u>，换<u>两段变一段、四个模型变两个</u>。而这个漂移是 off-policy 这个选择的必然后果，<b>不是实现缺陷</b>。</span><br><br><b>★ 三个符号陷阱（讲者自己主动点的，他说当初也把他搞糊涂了）</b>：<b>① PPO-Clip 写成 L = …，但它是要<u>最大化</u>的；② 那个 r_θ <u>不是奖励</u>，是新旧策略的概率比值；③ 公式里的 old <u>不是 SFT 模型</u>，是 RL 阶段的上一轮。</b><br><br><b>★★★ 对你的课题，这一讲我认为有三条是能直接用的。</b><br><span class='k'><b>① reward hacking 是你最该防的那个失败模式。</b>你用代理的可行性/代价模型去引导搜索，<u>搜索越强，越会找到「骗过代理」的配置</u> —— 报出来的「最便宜可行配置」可能只在代理眼里可行。⇒ 而本讲给的对策是成套的：<b>限制偏离参考策略（KL / clip），并保留一条用精确求解器复核 top-k 的通道</b>。注意讲者说得很清楚：<u>解法不是换一个更好的代理（代理永远不完美），而是限制优化的强度</u>。</span><br><span class='k'><b>② Best-of-N 就是你要打败的那个 baseline。</b>它的结构是「<u>把预算均匀分给 N 个候选，再取 argmax</u>」—— 这正是 best-arm identification 的 naive 基线。<u>successive halving 之类的方法在同样预算下显著更好</u>，因为它们把预算挪给还没分清的候选。⇒ 所以你的实验里应该<b>同时报一个 BoN 式均匀分配的对照</b>，这个对比本身就是你方法价值的说明。</span><br><span class='k'><b>③ value function 就是你要的那个东西。</b>「<u>给一段部分生成，估计按策略写完后的最终奖励</u>」—— 把「部分生成」换成「部分配置」，这就是 MCTS 的节点价值，<b>也正是 dominance 剪枝需要的那个对部分解的估计</b>。⇒ 而「减基线降方差」也照搬得上：不同实例的代价基准不同，减掉同条件下的期望能把与实例难度无关的共同成分消掉。</span><br><br><b>⇒ 另外两条写论文时的习惯，我觉得比技术内容还值钱</b>：<b>① 讲者推损失函数是<u>从第一性原理推的</u>（要最大化什么概率 → 独立假设 → 取 log → 变最小化），而不是抄公式；② 他回答「用哪个」时给的是<u>以读者处境为输入的规则</u>，而不是「X 比 Y 好」，而且他把「<u>愿意花多少精力看着训练</u>」当成一项真实成本列了出来。</b><br><br><b>⇒ 下一讲 L6 是 LLM Reasoning，会讲 GRPO（DeepSeekMath 那篇）—— 正是本讲末尾那个「真的需要这么多模型吗」的另一个答案。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L5 · 偏好调优</title>")
io.open("cme295-L5.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L5.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
