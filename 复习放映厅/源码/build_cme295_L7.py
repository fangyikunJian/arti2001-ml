# -*- coding: utf-8 -*-
"""CME295 讲座 L7 · Agentic LLMs —— 2026-10-29 新做。

这一讲一次修掉 L6 开头那张弱点清单上的第 ② 和第 ③ 条：
  上半场（Afshine）：**知识停在 cutoff date** ⇒ RAG。
    为什么不能继续训、为什么不能全塞进 prompt（装不下 / 大海捞针 / 要花钱）→
    R-A-G 三步 → 知识库与三个超参 → ★ 两阶段检索 → bi-encoder / S-BERT /
    BM25 与混合 / HyDE / 给 chunk 补上下文与 prompt caching / cross-encoder 重排 →
    NDCG 与另外三个指标 → MTEB。
  下半场（Shervine）：**光说不做** ⇒ tool calling 与 agent。
    结构化 vs 非结构化 → 函数定义里 LLM 只看得到 API 与文档 → 三阶段 →
    两组 SFT 对 → ⭐ 用 explanation 代替 SFT（并让推理模型帮你迭代）→
    工具的三类用途 → 工具太多的五个问题 → tool selection → MCP →
    ★ agent 与 ReAct 循环 → A2A → 安全与实务忠告。

⚠ 这一讲是期末考范围（L5–L9）的第三讲。
⭐ 贯穿全讲的一条线：**「候选多 + 评估贵」的地方，都会长出两阶段结构**
   （文档检索是一次，工具选择又是一次）。

底料：CME295/transcripts/L7.txt（1021 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L7 build_cme295_L7.py cme295_L7_*.py

引擎的坑（memory/projector-engine-traps.md，十七条，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**；里面不许「< 紧跟字母」（坑 11）
  · ⚠ setEq 里的反斜杠要写 \\\\ —— 场景 JS 是 JS 源码（坑 16）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=150 ⇒ 其下 note 至少 178；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜两条 note 的 y **至少差 19**（坑 12）
  · ⚠ stack()/seq() 自己算几何，⑨⑩ 看不见 ⇒ 底边与末格标签要手算（坑 13）
  · ⚠ 有**居中** setEq 的镜，note 只能落在 [178,265]
  · ⚠⚠ 浏览器逐帧扫要用 `__go(i,true)`，否则被测验闸挡住、**假通过**（坑 17）
  · ⚠ 打字时混进过俄文（这次又在 L7_d 混进「работ」，第 6 次）—— audit ⑦ 能抓
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
var CFG={title:"CME295 讲座 L7 · 把 LLM 接到外部世界",
  subtitle:"RAG 与两阶段检索 · tool calling · agent 与 ReAct · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=h-7S6HNq0Vg&t="};

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
    setTitle("CME295 讲座 L7","把 LLM 接到外部世界：RAG · 工具 · agent",
      "九讲的第 7 讲 · 约 110 分钟");},
    "第七讲，而它的定位在 L6 开头那张清单上就已经写好了。<br><b>讲者的开场</b>：<b>「<u>今天我们要聚焦在一些实用技术上，让我们的 LLM 能和外部世界、和其它系统交互。因为到现在为止，我们的 LLM 完全是靠它自己的</u>。」</b><br><b>⇒ 所以这一讲一次修掉 vanilla LLM 四个弱点里的<u>两条</u></b>：<b>上半场修<u>「知识停在 cutoff date」</u>（RAG），下半场修<u>「光说不做」</u>（tool calling 与 agent）。</b><br><br><b>★★ 而这一讲和前两讲的性质完全不同，我建议你一开始就意识到这一点</b>：<b>L5 讲偏好调优、L6 讲推理训练，改的都是<u>模型的权重</u>；而这一讲<u>几乎一个权重都不改</u> —— 它改的是<u>模型周围的系统</u>。</b><br><b>⇒ 同一个能力缺口，可以从「训练」这一侧补，也可以从「架构」这一侧补。<u>这一讲全程走后一条</u>，而且你会看到它常常更快、更好解释。</b><br><br><b>⭐ 另外有一条线贯穿全讲，我希望你带着它听：<u>凡是「候选很多 + 逐个评估很贵」的地方，都会长出同一个两阶段结构</u></b>：<b><u>第一级用极便宜的判据粗筛（指标是 recall，因为漏了就永远救不回来），第二级才用昂贵而精确的判据排序</u>。</b><br><b>⇒ 这一讲里它出现了<u>两次</u>：一次是<u>文档检索</u>（bi-encoder 粗筛 → cross-encoder 重排），一次是<u>工具选择</u>（只给名字粗选 → 再放完整 API）。</b><b>★ 同一个结构在一讲里独立出现两次，说明它不是某个领域的技巧，而是这类问题的通用解。</b><br><br><b>⚠ 最后提醒一件事：这一讲的最后一段讲<u>安全</u>，而它不是例行公事。</b><b>因为工具让模型<u>第一次能改变外部世界</u> —— 前面所有讲里，模型最坏也只是「说错话」。<u>而讲者举的例子就发生在课前一天</u>。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的两半，各修一条弱点",640,186,"v");
    stack(330,210,[["上半场：RAG","g"],["修「知识停在 cutoff date」","d"],["处理「非结构化」数据","d"],["★ 全部难点在「检索」那一步","y"]],460,34,8);
    stack(950,210,[["下半场：工具与 agent","g"],["修「光说不做」","d"],["处理「结构化」数据","d"],["★ 模型第一次能「改变世界」","r"]],460,34,8);
    note("⇒ 两半的交界处很有意思：tool calling 的定义里有「并可能作用于」这几个字",640,386,"y");},
    "<b>把两半的分工摆出来，因为它们处理的数据性质不同，手段也就完全不同。</b><br><b>上半场 RAG</b>：<b>处理<u>非结构化</u>的数据 —— <u>文档里全是词、词、词，而你只想把相关的那几篇捞出来</u>。</b><b>⇒ 它的三步是 <u>Retrieve → Augment → Generate</u>，而学生当场就问到了要害：<u>万一检索那一步做砸了呢？</u> 讲者的回答定下了全讲重心：<u>谈 RAG 主要就是在聚焦「把检索做得尽可能好」</u>。</b><br><b>下半场工具与 agent</b>：<b>处理<u>结构化</u>的数据 —— <u>输入和输出之间有确定的关系，比如一张表</u>。⇒ 那就可以把它重述成一个<u>函数</u>，让 LLM 去调用。</b><br><b>★★★ 而两半的交界处有一个字眼值得你现在就记住。</b><b>Shervine 特意去找了一个权威定义来锚住 tool calling：<u>它让自主系统能通过「动态访问、并可能作用于」外部资源，来完成复杂任务</u>。</b><br><b>⇒ 「<u>并可能作用于</u>」这几个字，就是 tool calling 和 RAG 最根本的区别：<u>RAG 只能「读」，tool calling 可以「写」</u>。</b><br><b>⚠ 而这一字之差，既是弱点清单第 ③ 条被修掉的地方，也是本讲最后必须专门讲安全的原因 —— <u>前两类工具（查信息、做计算）出错只是「答案不对」，第三类（替你行动）出错是「世界被改坏了」</u>。</b><br><br><b>⭐ 最后预告一个我认为全讲最可迁移的技巧（在第 21 条）：<u>怎么让模型替你写那段教它用工具的说明</u> —— 把你想要的行为写成评测集，跑一遍打分，再把「配置 + 每个样本的得分」一起交给一个强模型，让它提出改法。<u>Shervine 说：我不建议你端到端地自己写</u>。</b>");
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


import cme295_L7_a, cme295_L7_b, cme295_L7_c, cme295_L7_d
cme295_L7_a.add(KP)   # 位置 → 为什么不继续训 → 三个「不能全塞」的理由 → RAG 三步 → 知识库
cme295_L7_b.add(KP)   # 两阶段 → 候选召回 → S-BERT → BM25 与混合 → HyDE → 上下文与缓存 → 重排
cme295_L7_c.add(KP)   # NDCG → 另三个指标与 MTEB → tool calling 定义 → 函数定义 → 三阶段 → SFT → explanation
cme295_L7_d.add(KP)   # 三类用途 → 工具太多 → tool selection → MCP → agent 与 ReAct → A2A → 安全与忠告

C.append(r'''KP("完 · 两阶段，和那一个「可能作用于」",
function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","把 LLM 接到外部世界",
      "读 · 算 · 写 · 以及一个反复出现的结构");},
    "收一下这一讲。<b>它修了两条弱点，而我想按「一个结构 + 一个字眼 + 三条对你的用处」来收。</b><br><br><b>★★★ 一个结构：两阶段。</b><span class='k'>这一讲里它<b>独立出现了两次</b> —— <u>文档检索</u>（bi-encoder 粗筛 → cross-encoder 重排）和<u>工具选择</u>（只给名字粗选 → 再放完整 API）。而它的逻辑每次都一样：<b>量级大的那一级只能用便宜判据 ⇒ 它的指标必须是 recall（漏掉的，后面永远救不回来）；量级小的那一级才负担得起昂贵判据 ⇒ 它负责精度</b>。</span><br><span class='k'>⇒ 两个推论值得单独记：<b>① 两类错误的代价不对称 —— 第一级「多留了无关的」可被修正，「漏掉了相关的」不可逆 ⇒ 第一级的参数该往松调。② 整条流水线的上限由第一级定 ⇒ 调优先看第一级的 recall，它不高时优化第二级是白费。</b></span><br><span class='w'>⚠ 而这个结构<b>不是某人的巧思</b>：bi-encoder 能预计算所以便宜但看不到交互，cross-encoder 看得到交互但什么都不能预算 —— <b>两阶段是被这两种结构各自的约束逼出来的唯一解</b>。</span><br><br><b>★★ 一个字眼：「并可能作用于」。</b><span class='k'>tool calling 的定义里这几个字，就是它和 RAG 的根本区别：<b>RAG 只能读，tool calling 可以写</b>。而工具的三类用途正好是递进的 —— <u>① 读外部状态；② 算（纯函数、无副作用）；③ 改变外部状态</u>。<b>前两类出错只是「答案不对」，第三类出错是「世界被改坏了」</b>。</span><br><span class='w'>⇒ 这就是为什么最后要专门讲安全，而讲者举的例子<b>就发生在课前一天</b>（Anthropic 披露的那次从 Claude 发起的大规模攻击）。两类防线：<b>训练期</b>（SFT 与 RL 数据混合里的 harmlessness，接上 L6 那条「作用在全部输出 token、含 think 段」）与<b>推理期</b>（安全分类器看整段对话）。</span><br><br><b>★★★ 对你的课题，这一讲我认为有三条能直接用。</b><br><span class='w'><b>① 两阶段就是你的骨架，而且它给了你一个硬要求。</b><u>dominance 剪枝 / 便宜代理 = 第一级；精确求解器复核 top-k = 第二级</u>。而「第一级犯漏的错不可逆」这句话的形式化版本，正是<b>你的剪枝判据必须是可采纳的（admissible）</b>。⇒ 实验里该<b>单独报第一级的 recall</b>（被剪掉的分支里事后发现含最优解的比例），它定了整个方法的上限 —— 只报最终解的质量，是看不出这一层的。</span><br><span class='w'><b>② ReAct 的循环就是你的搜索循环。</b><u>observe = 读当前部分配置与已知约束；plan = 决定下一个要定的分量；act = 调求解器或评估器；再回到 observe</u>。而「<b>每一步都检查目标达成了没有</b>」正是你的终止与剪枝判据所在的位置。⇒ 这个对应让 agent 那边的工程经验直接可用，尤其是那条风险模型：<b>每步 95% 正确，十步只剩 60%</b> —— 所以<u>剪枝判据的单步错误率必须按路径长度折算</u>，而不是单看它自己好不好。</span><br><span class='w'><b>③ ⭐ 那个「让模型替你迭代说明」的闭环。</b><u>把你想要的行为写成评测集 → 跑当前这版配置 → 逐条打分 → 把「配置 + 每个样本的得分」一起交给一个强模型，问它「你会怎么改才能让评测变好」→ 再跑</u>。Shervine 说<b>我不建议你端到端地自己写</b>。⇒ 你的搜索超参、剪枝阈值、启发式规则都能这样自动迭代，而<b>关键前提是你先有一个能自动打分的评测集</b> —— 这又回到你和这一讲共有的那个幸运：<u>可验证</u>。</span><br><br><b>⇒ 另外三条小而实用的</b>：<b>① <u>prompt caching</u> 是「把一个架构事实（因果注意力 ⇒ 相同前缀相同激活）直接变成省钱策略」的范例 —— 对应你搜索里<u>共享的部分配置只该评估一次</u>；② <u>docstring 是模型的唯一输入</u>，不是给人看的注释 —— 对应你暴露给策略的接口说明；③ <u>start small, start smart</u>：先跑通一个极简用例，再用最强的配置摸清天花板，最后才去优化成本。<b>先知道上限在哪，才知道省下来的代价值不值。</b></b><br><br><b>⇒ 下一讲 L8 是 LLM Evaluation，修清单上的最后一条（自由文本难评估）。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L7 · 把 LLM 接到外部世界</title>")
io.open("cme295-L7.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L7.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
