# -*- coding: utf-8 -*-
"""CME295 讲座 L3 · Transformers & Large Language Models —— 2026-10-28 新做。

这一讲正式进入 LLM，分三大块：
  ① 什么是 LLM（定义）＋ **MoE 混合专家**（怎么把模型做大而不把推理做贵）
  ② **解码策略**：贪心 / beam search / 采样 / top-k / top-p / 温度 —— 以及「唯一的随机性在哪」
  ③ 提示与推理效率：context rot · ICL · CoT · self-consistency ·
     KV 缓存 · GQA · PagedAttention · MLA · 投机解码 · 多 token 预测

⭐ 这一讲离用户课题特别近：beam search / 采样 / self-consistency 本质上都是
   **在序列空间上做搜索**，而「局部最优 ≠ 全局最优」正是用户那类问题的核心张力。

底料：CME295/transcripts/L3.txt（1074 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L3 build_cme295_L3.py cme295_L3_*.py

引擎的坑（memory/projector-engine-traps.md，十三条，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**、LaTeX 两个反斜杠；⚠ 里面不许「< 紧跟字母」（坑 11）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=150 ⇒ 其下 note 至少 178；note ≤386；boxNode 底边 ≤390
  · ⚠ 有**居中** setEq 的镜，note 只能落在 [178,265]
  · matrix 底边 = y+(rows-1)*ch+(ch-3) ≤390，末行文字中心 ≤ 下方 note 的 y−35
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
var CFG={title:"CME295 讲座 L3 · Transformers 与大语言模型",
  subtitle:"MoE · 解码策略与温度 · KV 缓存与投机解码 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=Q5baLehv5So&t="};

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
  bw=bw||250; bh=bh||34; gap=gap==null?8:gap; var i,ys=[];
  for(i=0;i<items.length;i++){
    var y=ytop+i*(bh+gap);
    boxNode(cx-bw/2,y,bw,bh,items[i][0],items[i][1]||"");
    ys.push(y);
    if(i) link(cx,y,cx,y-gap);}
  return ys;}

/* ── 概率柱状图（画温度、top-k、top-p）──
   vals 是 0..1 的高度；base 是基线 y；每根柱子宽 bw。 */
function bars(x0,base,vals,bw,maxh,cls,labs){
  var i,gap=12;
  for(i=0;i<vals.length;i++){
    var h=Math.max(3,vals[i]*maxh), x=x0+i*(bw+gap);
    boxNode(x,base-h,bw,h,"",(cls instanceof Array)?cls[i]:(cls||"b"));
    if(labs&&labs[i]) note(labs[i],x+bw/2,base+22,"d");}
  return x0+vals.length*(bw+gap)-gap;}

/* ── 一棵两层的搜索树（画 beam search / 贪心）── */
function tree(rootx,rooty,kids,dy,bw,bh){
  var i,n=kids.length,span=190,x0=rootx-(n-1)*span/2;
  boxNode(rootx-bw/2,rooty,bw,bh,"BOS","y");
  for(i=0;i<n;i++){
    var x=x0+i*span;
    boxNode(x-bw/2,rooty+dy,bw,bh,kids[i][0],kids[i][1]||"d");
    link(rootx,rooty+bh,x,rooty+dy);
    note(kids[i][2]||"",x,rooty+dy+bh+20,kids[i][1]||"d");}
  return x0;}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L3","Transformers 与大语言模型",
      "九讲的第 3 讲 · 约 109 分钟");},
    "第三讲，而讲者开场说「今天是很让人兴奋的一天，因为我们终于要介绍大语言模型了」。<br><b>这一讲的结构是三大块，而且三块回答的是三个<u>完全不同层面</u>的问题</b>：<br><b>① 什么是 LLM，以及怎么把模型做大而不把推理做贵</b> —— <b>答案是 MoE（混合专家）。</b><span class='w'>这一块是关于<u>架构</u>的。</span><br><b>② 拿到概率分布之后，到底怎么挑下一个词</b> —— <b>贪心 / beam search / 采样 / top-k / top-p / 温度。</b><span class='w'>这一块是关于<u>解码</u>的，而且它是前两讲完全没碰过的一个维度。</span><br><b>③ 怎么把提示写好，以及怎么让推理跑得更快</b> —— <b>ICL、CoT、self-consistency、KV 缓存、投机解码。</b><span class='w'>这一块是关于<u>使用</u>的。</span><br><b>★★ 对你来说，第 ② 块值得花最多时间，因为它整块都是「在序列空间上做搜索」。</b><br><b>⭐ 讲者会在那里正面讲一个你很熟的张力：<u>每一步都挑最好的，不等于整条路最好</u>。</b><b>而他给出的三种对策（贪心 / 保留 k 条路径 / 随机采样），正好对应搜索里的三种经典姿态。</b><br><b>⚠ 而最有意思的是最后的结局：<u>beam search 这个「更接近全局最优」的方法，实践中反而不用</u>。</b><b>原因不是它不对，而是人们要的根本不是「最可能的那条路」。这个转折值得你认真想一想。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的三块，和它们各自在问什么",640,186,"v");
    boxNode(60,214,370,44,"① 架构：MoE","g");
    note("怎么把模型做「大」",245,286,"d");
    note("而不把一次推理做「贵」",245,320,"d");
    note("关键词：专家 / 路由 / 稀疏",245,356,"y");
    boxNode(455,214,370,44,"② 解码：怎么挑下一个词","y");
    note("⭐ 这一块整个是「搜索」",640,286,"g");
    note("贪心 · beam · 采样 · 温度",640,320,"d");
    note("关键词：局部最优 ≠ 全局最优",640,356,"y");
    boxNode(850,214,370,44,"③ 使用：提示与效率","b");
    note("提示怎么写、推理怎么快",1035,286,"d");
    note("ICL · CoT · KV 缓存 · 投机解码",1035,320,"d");
    note("关键词：复用 / 近似 / 并行",1035,356,"y");},
    "<b>三块的地图，而我建议你带着不同的问题去看每一块。</b><br><b>① MoE 那一块，带的问题是：<u>怎么在「参数更多」和「算得更慢」之间解耦？</u></b><span class='w'>这两件事通常绑在一起 —— 参数多就算得慢。而 MoE 的全部意义就是把它们拆开。</span><br><b>② 解码那一块，带的问题是：<u>给定一个打分函数，怎么从一个指数大的空间里挑出一条好的路径？</u></b><b>⭐ 这个问法你应该立刻觉得眼熟 —— 它就是搜索问题的标准形式。</b><br><span class='w'>而且这一块会出现三个你在搜索文献里见过的东西：贪心、束搜索（beam search 就是受限宽度的广度优先）、以及随机化。</span><br><b>③ 效率那一块，带的问题是：<u>哪些计算是重复的、哪些可以近似、哪些可以并行？</u></b><span class='w'>讲者自己把这一块分成了「精确」与「近似」两类，而这个分法很干净。</span><br><b>⚠ 一个提醒：这一讲的缩写密度是全课最高的（MoE、FLOPS、ICL、CoT、KV、GQA、MLA…）。</b><b>按第一讲那个建议 —— 每个缩写都当场落实成「它到底指哪个具体东西」，别让它们堆成一团。</b>");
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


import cme295_L3_a, cme295_L3_b, cme295_L3_c, cme295_L3_d
cme295_L3_a.add(KP)   # LLM 的定义 → MoE 的动机、形式、dense/sparse、放在哪
cme295_L3_b.add(KP)   # token 级路由 → routing collapse → MoE 的真正卖点 → 解码问题的提出
cme295_L3_c.add(KP)   # beam search → 采样 → top-k/top-p → 温度 → 确定性 → guided decoding
cme295_L3_d.add(KP)   # context rot → 提示结构 → ICL → CoT → self-consistency → 推理效率五件事

C.append(r'''KP("完 · 这一讲给了你三样东西",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L3 · 完","Transformers 与大语言模型",
      "架构 · 解码 · 使用");},
    "收一下这一讲，三块各带走一样东西。<br><b>★★ ① 架构那一块，带走「把两件事解耦」这个动作。</b><br><b>参数量和计算量本来是绑死的 —— 参数越多，一次前向算得越久。</b><b>⭐ 而 MoE 把它们拆开了：<u>总参数</u>可以涨到万亿，而<u>激活参数</u>（真正参与这一次前向的）保持不变。</b><br><span class='w'>代价是三条：要多存那么多参数（显存）、要处理路由坍塌（辅助损失）、路由本身也要学。</span><br><b>⇒ 可带走的一般形式：<u>当两个你关心的量被绑在一起时，先问「有没有办法只让其中一个涨」</u>。</b><br><br><b>★★★ ② 解码那一块，是这一讲对你最有价值的部分，而且结局很反直觉。</b><br><b>问题是标准的搜索问题：给一个打分函数，从指数大的空间里挑一条路径。</b><br><span class='w'>贪心 —— 每步挑最大。<b>快，但局部最优 ≠ 全局最优</b>，而且完全确定（没有多样性）。</span><br><span class='w'>beam search —— 保留 k 条路径。<b>更接近全局最优</b>，但算得贵，而且<b>还要额外处理长度偏置</b>（否则它偏爱短序列）。</span><br><span class='k'>采样 —— 按概率抽。<b>有多样性</b>，而且配 top-k / top-p 把长尾切掉。</span><br><b>⭐ 而结局是：<u>实践中用的是采样，不是 beam search</u>。</b><b>讲者说得很明白 —— beam search 只在机器翻译那种「需要最可能的答案」的场合才用。</b><br><b>★★ 这个结局的教训对你很直接：<u>「更接近最优」不自动等于「更有用」</u>。</b><b>要先问清楚：你的目标函数真的是你要的那个东西吗？</b><span class='w'>⚠ 在 LLM 这里，「最可能的序列」往往是乏味、重复、甚至退化的 —— 所以人们宁可要一个概率略低但更好的输出。</span><br><b>⇒ 而你的课题里这一问有一个很清楚的版本：<u>你的代理模型的最优，和真实目标的最优，差多远？</u></b><b>如果差得远，那把搜索做得更接近代理模型的最优，只是在更精确地走错路。</b><br><br><b>★★ ③ 效率那一块，带走那个「精确 / 近似」的分法。</b><br><span class='w'>精确的（结果一模一样，只是算得更聪明）：<b>KV 缓存</b>（别重算）、<b>PagedAttention</b>（别浪费显存）、<b>MLA</b>（把要存的东西压小）。</span><br><span class='w'>近似的（结果可能不同，换速度）：<b>GQA</b>、<b>投机解码</b>、<b>多 token 预测</b>。</span><br><b>⭐ 而投机解码那一条最漂亮：用一个小模型猜几个 token，再让大模型<u>一次</u>验证全部 —— 而且有一个接受/拒绝规则保证<u>输出分布和大模型完全一致</u>。</b><b>⚠ 它成立的前提是一个硬件事实：推理时瓶颈是<u>显存带宽</u>而不是算力，所以「一次验证 5 个」和「一次验证 1 个」几乎一样快。</b><br><b>⇒ 这条对你也直接可用：<u>先搞清楚你的瓶颈是算力还是访存，再决定优化什么</u>。优化错了的那一头，花再大力气也看不到变化。</b><br><br><b>⇒ 下一讲 L4 是 LLM Training：模型怎么训出来 —— 预训练、数据、规模定律。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L3 · Transformers 与大语言模型</title>")
io.open("cme295-L3.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L3.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
