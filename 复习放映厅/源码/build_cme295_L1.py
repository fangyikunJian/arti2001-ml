# -*- coding: utf-8 -*-
"""CME295 讲座 L1 · Transformer —— 2026-10-28 新做。这门课的第一部片子。

Stanford CME 295《Transformers and Large Language Models》Autumn 2025，
Afshine & Shervine Amidi 兄弟开的，共 9 讲、每讲约 107 分钟、无作业、两场考试各占 50%。
用户是为**科研**看这门课，所以 SUM 卡的第五格用新加的 r「接到你的课题」，
而不是课程片那种「与你的考试」。

底料：CME295/transcripts/L1.txt（924 句人工字幕）＋ L1_timed.txt
⚠ 全部 says() 的时间码用 源码/tools/quote_ts.py **精确**定位（不是插值）：
   该工具直接在原始 VTT 的 1685 条 cue 里找，阳性对照 191/191 命中且 ≤3 秒。
   旧的 find_quote.py（行号法）与 retime.py（字符插值）都只是估计，见
   memory/find-quote-anchor-bug.md。落盘前跑：
     python tools/quote_ts.py --check CME295 L1 build_cme295_L1.py cme295_L1_*.py

这一讲的内容线（也是 KP 的顺序）：
   NLP 三类任务 → 评估指标的两难 → 为什么 80 年代做不出来
   → 关口一：模型只懂数字 ⇒ 分词（词级/子词/字符级 + OOV）
   → 关口二：token 怎么变向量 ⇒ one-hot 全正交 ⇒ Word2vec 用代理任务学出来
   → 关口三：不看上下文、不看词序 ⇒ RNN（隐藏状态）⇒ 三个病（长程/梯度消失/串行慢）
   → 注意力：在「要预测的」与「过去的某处」之间架直连
   → 自注意力 + Q/K/V + 矩阵形式 ⇒ Transformer 架构（三处注意力各司其职）
   → 端到端走一遍：分词 → 嵌入+位置 → QKᵀ/√dk → 多头拼接+Wo → FFN → N 层 → 解码到 EOS

引擎的坑（memory/projector-engine-traps.md，写之前全部读过）：
  · setEq 必须 $$ 包裹、**写成一行**、LaTeX 两个反斜杠（scene 是原样拼进 JS 的）
  · says() 默认 y=150，文字框约 [137,169] ⇒ 紧随其下的 note 至少 y≥178
  · note 的 y ≤ 386；boxNode 底边 = y+h ≤ 390；matrix 底边 = y+(rows-1)*ch+(ch-3) ≤ 390
  · ⚠ 同一镜里有**居中** setEq 时，公式带占 279–441 ⇒ 该镜的 note 只能落在 [178,265]
  · curve(pts,cls) 内部已加 "fit "；fn() 只算点不画线，要 curve(fn(...))
  · 类名用**颜色首字母** g/y/b/r/v/d；axes 两套键名都认
  · 本文件定义的辅助函数，补充模块里也能直接调（同一个 IIFE）
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
var CFG={title:"CME295 讲座 L1 · Transformer",
  subtitle:"从「模型只懂数字」一路到自注意力 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=Ub3GoFaUcds&t="};

/* 讲者原话。时间码由 tools/quote_ts.py 在原始 VTT 里精确定位。
   ⚠ y 默认 150，文字框约 [137,169] —— 同一镜里紧随其下的 note 至少 178。*/
function says(ts,en,y){
  note("🎙 Amidi "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 一串 token 画成一排方块。返回每块的中心 x，供连线用 ── */
function seq(x0,y,toks,cls,bw,bh){
  bw=bw||104; bh=bh||44; var cx=[],i;
  for(i=0;i<toks.length;i++){
    var x=x0+i*(bw+10);
    boxNode(x,y,bw,bh,toks[i],(cls instanceof Array)?cls[i]:(cls||"b"));
    cx.push(x+bw/2);}
  return cx;}

/* ── 一个 token 向全部 token 连直线（自注意力那张图）── */
function fan(fromx,fromy,xs,toy,skip){
  for(var i=0;i<xs.length;i++){ if(i===skip) continue; link(fromx,fromy,xs[i],toy);} }

/* ── 竖着堆的模块（encoder / decoder 的内部）── */
function stack(cx,ytop,items,bw,bh,gap){
  bw=bw||250; bh=bh||40; gap=gap==null?12:gap; var i,ys=[];
  for(i=0;i<items.length;i++){
    var y=ytop+i*(bh+gap);
    boxNode(cx-bw/2,y,bw,bh,items[i][0],items[i][1]||"");
    ys.push(y);
    if(i) link(cx,y,cx,y-gap);}
  return ys;}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L1","Transformer",
      "9 讲的第 1 讲 · 约 102 分钟");},
    "这是 Stanford <b>CME 295《Transformers and Large Language Models》</b>的第一讲，<b>2025 年秋</b>这一期，讲者是 <b>Afshine 与 Shervine Amidi</b> 兄弟俩（就是写那套 CS229 速查表的两个人）。<br><b>⚠ 先说这门课的形状，因为它决定了该怎么看</b>：<b>一共 9 讲，每讲约 107 分钟，每周五一次；没有编程作业；成绩是期中 50% + 期末 50%</b>。<b>配套的书叫 Super Study Guide — Transformers & LLMs，另外有一份压缩过的 VIP cheat sheet 挂在 GitHub 上</b>。<br><b>⭐ 对你来说最要紧的一点：这门课不是「教你调 API」，它是从底层机制讲起的。</b>讲者自己把目标说成两条——<b>第一条是搞懂让这一切跑起来的底层机制，第二条才是这些模型怎么训练、用在哪</b>。<br><b>而这第一讲的位置很特殊：它是唯一一讲「从零开始」的。</b><b>它不假设你懂 NLP，从「模型只懂数字，不懂文本」这句话出发，一步一步推到自注意力。</b><br><b>⚠ 我把这一讲的结构整理成了一条「关口链」，因为它真正的讲法是「上一步不够用，所以必须有下一步」</b>：<b>关口一是文本怎么变成数字（分词）；关口二是 token 怎么变成有意义的向量（Word2vec）；关口三是怎么把顺序和上下文吃进来（RNN）；而 RNN 的三个病，正好逼出了注意力。</b><br><b>⭐ 看这一讲的正确姿势是盯住每一处「所以」</b>——每一个新机制都是上一个机制的毛病逼出来的，<b>而不是因为它更时髦。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    var y=196;
    boxNode(90,y,300,46,"① 文本 → 数字","b"); note("分词 tokenization",240,y+72,"d");
    boxNode(90,y+104,300,46,"② token → 有意义的向量","b"); note("Word2vec / 代理任务",240,y+176,"d");
    boxNode(490,y,300,46,"③ 吃进顺序与上下文","y"); note("RNN / LSTM",640,y+72,"d");
    boxNode(490,y+104,300,46,"④ 直连代替串行","g"); note("注意力 → 自注意力",640,y+176,"d");
    boxNode(890,y+52,300,46,"⑤ 拼成一个架构","v"); note("Transformer",1040,y+124,"d");
    link(390,y+23,490,y+23); link(240,y+46,240,y+104); link(790,y+23,890,y+75);
    link(640,y+46,640,y+104); link(390,y+127,490,y+127); link(790,y+127,890,y+75);
    note("每一步都是上一步「不够用」逼出来的 —— 盯住每一处「所以」",640,y+230,"y");},
    "<b>先把整讲的地图摆出来，后面每一个知识点都能挂到这张图上。</b><br><b>① 文本 → 数字</b>：<b>模型只会算数，不认字。所以第一件事是把句子切成一个个单位——这叫分词，切出来的单位叫 token。</b>而怎么切，有三种路子、各有代价。<br><b>② token → 有意义的向量</b>：<b>切开了还不够，得给每个 token 一个向量。</b><b>最朴素的做法（one-hot）有一个致命毛病，而修这个毛病的办法就是 Word2vec 的「代理任务」。</b><br><b>③ 吃进顺序与上下文</b>：<b>Word2vec 学出来的向量有两个硬限制——不看上下文、不看词序。</b><b>于是需要一类能按顺序处理的模型，那就是 RNN 与 LSTM。</b><br><b>④ 直连代替串行</b>：<b>⚠ 而 RNN 自己有三个病：记不住远处的、梯度会消失、而且因为必须串行所以慢。</b><b>注意力就是冲着「记不住远处的」来的——在「要预测的东西」和「过去的某一处」之间直接架一条线。</b><b>⭐ 2017 年那篇论文干脆把串行整个扔了，只留直连，这就是自注意力。</b><br><b>⑤ 拼成一个架构</b>：<b>把自注意力、位置编码、多头、前馈层拼起来，就是 Transformer。</b><br><b>⚠ 注意这条链是「被迫」的，不是「设计」的</b>——<b>⭐ 这也是为什么这一讲值得当成一个方法论样本来看：它展示了一个领域怎么被一连串具体的失败推着往前走。</b>");
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


import cme295_L1_a, cme295_L1_b, cme295_L1_c, cme295_L1_d
cme295_L1_a.add(KP)   # NLP 三类任务 → 指标的两难 → 时间线 → 分词三种切法 → OOV
cme295_L1_b.add(KP)   # one-hot → 余弦相似度 → 全正交 → 代理任务 → 玩具网络 → 两个硬限制
cme295_L1_c.add(KP)   # 句向量求平均 → RNN → 三个病 → LSTM → 注意力的想法
cme295_L1_d.add(KP)   # 自注意力 → Q/K/V → 架构 → 位置编码 → 多头 → 端到端走一遍

C.append(r'''KP("完 · 这一讲给了你什么",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L1 · 完","Transformer",
      "一条被失败推着走的链");},
    "收一下这一讲。<br><b>★★★ 如果只带走一句话，带走这一句：Transformer 不是被设计出来的，是被一连串具体的失败逼出来的。</b><br><b>把那条链再走一遍，每一环都是「上一环的毛病」</b>：<br><b>① one-hot 的毛病是<span class='k'>任意两个向量都正交</span></b>——于是「相似度」这件事根本无法表达。<b>⇒ 所以要把向量学出来，这就是 Word2vec，而它学的办法是代理任务：真正想要的不是预测结果，是训练过程中顺带长出来的那层权重。</b><br><b>② Word2vec 的毛病是<span class='k'>一个词只有一个向量</span></b>——河岸的 bank 和银行的 bank 共用一个。<b>而且词序完全不进来。⇒ 所以要能按顺序处理的模型，这就是 RNN。</b><br><b>③ RNN 的毛病有三个</b>：<b>整句话的意思全压在一个隐藏状态里（长程依赖）、反向传播要连乘一串因子（梯度消失/爆炸）、而且必须一个一个走（慢）。</b><b>⇒ 注意力冲着第一个病来：在要预测的东西和过去的某一处之间架一条直连。</b><br><b>④ ⭐ 而 2017 年那一步是整条链上最大的一跳</b>：<b>既然直连有用，那干脆把串行<u>全部</u>扔掉，只留直连——所有 token 一次性互相看。</b><b>这一刀同时治了三个病：直连解决长程、一次性解决慢（可以并行、能写成矩阵乘法）。</b><b>⚠ 代价是顺序信息也被扔掉了，所以要用位置编码把它加回来。</b><br><b>⭐ 这里有一个非常值得记住的模式：一个机制的代价，往往要靠另一个机制去补。</b><b>扔掉串行换来了并行，然后补一个位置编码；用 softmax 做软加权换来了可微，然后补一个 √d_k 的缩放。</b><br><b>★★ 最后说一句这一讲和科研的接口，因为这是你看它的理由。</b><b>⭐ 自注意力的骨架是「用一个 query 去和一堆 key 比，按相似度加权地取 value」——这是一个<u>在候选集合上做软选择</u>的通用机制</b>，<b>而「在候选集合上选」正是你那类问题的形状。</b><b>⚠ 区别也很关键：注意力取的是 softmax 加权和（软的、可微的、全部候选都有份），而你的搜索取的是 argmin（硬的、只留一个）。</b><b>⭐ 软硬之差带来两件事：软的可以反向传播、但永远不会真正排除任何候选；硬的能剪掉整片子树、但不可微。</b><b>这条分界线在第 6、7 讲（LLM Reasoning 与 Agentic LLMs）会以「要不要做树搜索」的形式正面出现——那两讲是这门课离你课题最近的地方。</b><br><b>⇒ 下一讲 L2 是 Transformer-Based Models & Tricks：把这个架构拆成只用 encoder、只用 decoder 两种用法，并讲一批实际工程里必备的技巧。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L1 · Transformer</title>")
io.open("cme295-L1.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L1.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
