# -*- coding: utf-8 -*-
"""CME295 讲座 L7 · Agentic LLMs —— 2026-11-09 按新标准重做。

⚠ 旧版（2026-10-29）只有 43 镜扛 1020 句字幕 = 23.7 句/镜，正是用户退回过的
   「内容太少、不是逐帧字幕讲解」那种。这一版按 L6 定稿的线重做：
   **每镜旁白 250–300 字、每镜扛 7–8 句字幕、一讲约 165 帧**。

这一讲一次修掉 L6 开头那张弱点清单上的第 ② 和第 ③ 条：
  上半场（Afshine）：**知识停在 cutoff date** ⇒ RAG。
    为什么不能继续训、为什么不能全塞进 prompt（装不下 / 大海捞针 / 要花钱）→
    R-A-G 三步 → 知识库与三个超参 → ★ 两阶段检索 → bi-encoder / S-BERT /
    BM25 与混合 / HyDE / 给 chunk 补上下文与 prompt caching / cross-encoder 重排 →
    NDCG / MRR / recall@k / precision@k → MTEB。
  下半场（Shervine）：**光说不做** ⇒ tool calling 与 agent。
    结构化 vs 非结构化 → 函数定义里 LLM 只看得到 API 与文档 → 三阶段 →
    两组 SFT 对 → ⭐ 用 explanation 代替 SFT（并让推理模型帮你迭代）→
    工具的三类用途 → 工具太多的五个问题 → tool selection → MCP →
    ★ agent 与 ReAct 循环 → A2A → 安全与实务忠告。

⭐ 贯穿全讲的一条线：**「候选多 + 评估贵」的地方，都会长出两阶段结构**
   （文档检索是一次，工具选择又是一次）。

底料：CME295/transcripts/L7.txt（1020 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L7 build_cme295_L7.py cme295_L7_*.py

引擎的坑（memory/projector-engine-traps.md，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**；里面不许「< 紧跟字母」（坑 11）
  · ⚠ setEq 里的反斜杠要写 \\\\ —— 场景 JS 是 JS 源码（坑 16）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=166 ⇒ 其下 note 至少 194；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜两条 note 的 y **至少差 19**（坑 12）
  · ⚠ stack()/seq() 自己算几何 ⇒ 底边与末格标签要手算（坑 13）
  · ⚠⚠ 浏览器逐帧扫要用 `__go(i,true)`，否则被测验闸挡住、**假通过**（坑 17）
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
var CFG={title:"CME295 讲座 L7 · 接到外部世界",
  subtitle:"RAG · 两阶段检索 · tool calling · MCP · agent 与 ReAct · 空格推进 · N 讲解",
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
    var it=items[i];
    var lab=(typeof it==="string")?it:it[0],
        cl =(typeof it==="string")?"":(it[1]||"");
    boxNode(cx-bw/2,y,bw,bh,lab,cl);
    ys.push(y);
    if(i) link(cx,y,cx,y-gap);}
  return ys;}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L7","接到外部世界：RAG · 工具 · agent",
      "九讲的第 7 讲 · 约 109 分钟");},
    "第七讲，而它要做的事一句话说得清：<b>把 LLM 从「自己一个人」接到外面去</b>。讲者开场说「到现在为止，我们的 LLM 纯粹是靠它自己」—— 我们训了它、让它会推理，而今天要让它<b>用上别的系统</b>。<br>⭐ 它修的正是 L6 开头那张弱点清单上的<b>第二条和第三条</b>：<b>② 知识停在 cutoff date ⇒ RAG；③ 全是说、没有做 ⇒ tool calling 与 agent</b>。所以这一讲是两个半场拼起来的，中间由 Afshine 交棒给 Shervine。<br>⚠ 先给你一个提醒：这一讲<b>新概念密度很高但数学很少</b> —— 难的不是推导，是「哪个词指哪件事」。所以我会把术语对照做得很密。");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的两个半场",640,190,"v");
    stack(330,218,[["上半场 · RAG","g"],["为什么不能继续训 / 不能全塞进 prompt","d"],["R-A-G 三步","d"],["⭐ 两阶段检索（召回 → 重排）","y"],["四个排序指标","d"]],560,32,6);
    stack(960,218,[["下半场 · 工具与 agent","b"],["函数定义里 LLM 只看得到什么","d"],["三阶段 + 两组 SFT 对","d"],["⭐ 用 explanation 代替 SFT","y"],["MCP · ReAct · A2A · 安全","d"]],560,32,6);
    note("⭐ 一条线贯穿两个半场：「候选多 + 评估贵」的地方，都会长出两阶段结构",640,386,"y");},
    "<b>把路线先摆出来，因为这一讲表面上是两个话题，底下其实是同一个结构。</b><br>⭐ 那条线是：<b>凡是「候选很多、而逐个仔细评估很贵」的地方，都会长出两阶段 —— 第一级用便宜判据粗筛（所以它的指标必须是 recall，漏了永远救不回来），第二级才负担得起昂贵判据</b>。<br>这一讲里它<b>独立出现了两次</b>：上半场是「几百万个 chunk ⇒ 粗筛一百个 ⇒ 重排取前 k」,下半场是「几百个工具 ⇒ tool selector 选几个 ⇒ 只把这几个放进上下文」。<br>⚠ 看到第二次出现时请回头对一下 —— <b>认出同一个结构，比记住两套名词有用得多</b>。");
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
import cme295_L7_e, cme295_L7_f, cme295_L7_g, cme295_L7_h
import cme295_L7_i, cme295_L7_j, cme295_L7_k, cme295_L7_l
import cme295_L7_m, cme295_L7_n, cme295_L7_o, cme295_L7_p
cme295_L7_a.add(KP)   # 句 1–47     开场 / L6 回顾（GRPO 与长度偏置）/ 今天的两件事
cme295_L7_b.add(KP)   # 句 48–104   cutoff / 为什么不继续训 / 装不下 / 大海捞针 / 要花钱
cme295_L7_c.add(KP)   # 句 105–152  RAG 是什么 / R-A-G 三步 / 为什么检索那一步最关键
cme295_L7_d.add(KP)   # 句 153–232  知识库：chunk 与 embedding / 三个超参 / ⭐ 两阶段检索
cme295_L7_e.add(KP)   # 句 233–290  候选检索：余弦相似 / ANN / bi-encoder / S-BERT / 语义相似
cme295_L7_f.add(KP)   # 句 291–338  BM25 与混合检索 / 查询与文档不可比 / HyDE
cme295_L7_g.add(KP)   # 句 339–404  给 chunk 补上下文 / prompt caching / cross-encoder 重排
cme295_L7_h.add(KP)   # 句 405–470  评估的设定 / NDCG 逐项拆开
cme295_L7_i.add(KP)   # 句 471–521  MRR / recall@k / precision@k / MTEB / 上半场收尾
cme295_L7_j.add(KP)   # 句 522–588  交棒 / 结构化 vs 非结构化 / tool calling 的定义 / 那个例子
cme295_L7_k.add(KP)   # 句 589–660  函数定义 / LLM 只看得到 API 与文档 / 三阶段 / 两组 SFT 对
cme295_L7_l.add(KP)   # 句 661–749  SFT 样本要多样 / ⭐ 用 explanation 代替 SFT / 让模型帮你迭代
cme295_L7_m.add(KP)   # 句 750–810  工具的三类用途 / 工具太多 / 四个缺点的小结
cme295_L7_n.add(KP)   # 句 811–880  tool selection / MCP / agent 的定义
cme295_L7_o.add(KP)   # 句 881–950  ⭐ ReAct 循环逐步走查 / 多 agent 与 A2A
cme295_L7_p.add(KP)   # 句 951–1020 安全（数据外泄 / 两类防线）/ 实务忠告 / 收尾

C.append(r'''KP("完 · 两阶段这个结构，出现了两次",
function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","两个弱点，两条解法","而它们是互补的");},
    "⭐ <b>这一讲一次修掉了 L6 那张弱点清单上的两条，而两条解法的性质不同。</b><br><span class='k'><b>弱点② 知识停在 cutoff ⇒ RAG</b>：不改权重、不重训，<b>只在 prompt 里补上「相关的那一小块」</b>。三步是 Retrieve → Augment → Generate，而全部难度都在第一步。</span><br><span class='k'><b>弱点③ 全是说没有做 ⇒ tool calling</b>：给模型一个<b>它能调用、而且能作用于外部世界</b>的函数 API。讲者自己点明两者「<b>在某种意义上都在做同一件事</b>」—— 都在补模型没有的东西，<b>RAG 补「读到的」,工具补「做得到的」</b>。</span><br>⚠ 而一个实际的判断依据：<b>你要的是「非结构化的文字」就用 RAG，要的是「结构化的输入输出关系」就用函数</b>。");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","那条贯穿全讲的线","候选多 + 评估贵 ⇒ 两阶段");},
    "⭐ <b>这是我认为这一讲最该带走的一条，而它在课上独立出现了两次。</b><br><span class='w'><b>第一次 · 文档检索</b>：几百万个 chunk ⇒ ① 候选召回（双编码器、余弦相似、ANN）粗筛到约一百个 ⇒ ② 重排（交叉编码器）取前 k。</span><br><span class='w'><b>第二次 · 工具选择</b>：几百个工具 API ⇒ ① tool selector 只看名字和一句话描述，挑出可能相关的 ⇒ ② 只把这几个的完整定义放进上下文。</span><br><b>两次的结构完全一样</b>：第一级只能用便宜判据，所以它的指标必须是 <b>recall</b>（第一级漏掉的，第二级永远救不回来）；第二级候选少了，才负担得起昂贵判据（把 query 和候选<b>一起</b>送进模型算交互）。<br>⚠ 而这个结构不是 LLM 发明的 —— <b>讲者说它是从推荐系统和搜索借过来的</b>。所以你在自己的课题里碰到「候选多 + 评估贵」,第一反应就该是它。");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","上半场的要点","RAG 的坑都在检索那一步");},
    "<b>上半场值得单独记的几处。</b><br><span class='k'><b>三个超参</b>：embedding 维度（太大慢、太小表达不够）、chunk 大小（太小脱离上下文、太大表示不准，典型 500 token）、chunk 重叠（典型一两百 token）。</span><br><span class='k'><b>语义检索和关键词检索的失败模式正好互补</b>：embedding 找「意思像的」—— 但不保证含你的关键词（Huggy 和 Cuddly 语义相近，查 Cuddly 可能给你 Huggy）；<b>BM25</b> 是一个按词重叠算的启发式分，保证含关键词 ⇒ 所以实践里做<b>混合</b>。</span><br><span class='k'><b>两个「用 LLM 调用来补救」的手法</b>：<b>HyDE</b>（查询短、文档长，两个 embedding 不可比 ⇒ 先让 LLM 生成一篇假文档，再拿它去检索）；<b>给 chunk 补上下文</b>（让 LLM 读整篇、给每个 chunk 写一句背景 ⇒ 而这会产生海量 LLM 调用，靠 <b>prompt caching</b> 把成本压到约 1/10）。</span><br>⚠ 四个排序指标：<b>NDCG</b>（位置越靠前得分越高，再除以理想值归一化到 1）、<b>MRR</b>（只看第一个相关文档排第几）、<b>recall@k / precision@k</b>。");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","下半场的要点","工具、agent，与那条省力的路");},
    "<b>下半场值得单独记的几处。</b><br><span class='k'><b>LLM 看得到什么</b>：只有<b>函数 API（输入输出签名）和文档字符串</b> —— 实现细节它看不到。所以「<b>文档写得好不好，直接决定工具用得对不对</b>」。</span><br><span class='k'><b>三阶段</b>：① LLM 读 preamble 里的 API，<b>只负责填参数</b>；② 代码<b>真的执行</b>那个函数（这一步和 LLM 无关）；③ 把结构化结果喂回 LLM，让它写成自然语言。</span><br><span class='k'>⭐ <b>那条省力的路</b>：本来要造两组 SFT 对（查询→工具调用、工具结果→最终回答）;而今天可以<b>用一段「说明」代替 SFT</b> —— 而且不要自己写：<b>把 SFT 对当评测集、让一个推理模型根据得分反复改那段说明</b>。讲者说「我不建议你从头到尾自己写」。</span><br><span class='k'><b>agent</b> = 工具 + <b>循环</b>：ReAct 的 observe → plan → act 反复走，直到达成目标才退出。而 <b>MCP</b> 标准化「工具怎么暴露给模型」,<b>A2A</b> 标准化「agent 之间怎么说话」。</span>");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L7 · 完","安全与忠告","接到外面，风险也接进来了");},
    "⚠ <b>讲者把安全放在最后，但他说得很重。</b><br><span class='w'>能力变了性质：<b>模型现在能「替你动手」—— 于是出现了以前不存在的风险</b>。他举的例子是<b>数据外泄</b>：一个能发邮件的工具 + 一句「把我的密码发到这个地址」,数据就出去了。<br>两类防线：<b>训练期</b>（像 R1 那样在 SFT 和 RL 的数据里掺进安全样本）和<b>推理期</b>（一个安全分类器看着对话，判断要不要放行）。</span><br><span class='k'>而他提到<b>就在前一天 Anthropic 公布了一起大规模网络攻击</b>，攻击方正是用了工具和 agent 能力 —— 他的判断是「<b>这不是一场必输的仗</b>，只是防御手段也必须跟上」。</span><br><b>⇒ 最后三句实务忠告，很具体</b>：① <b>start small</b> —— 先用一个最简单的用例跑通；② <b>start smart</b> —— 先上最强的模型，知道能力的天花板在哪，再去省延迟和成本；③ <b>看推理链</b> —— 它们会把思考过程打出来，调试时一定要读。<br>而他自己最喜欢的 agent 用法是<b>写代码</b>，但附了一句很值得记的话：<b>「生成代码是便宜的，判断一段代码对不对才是难的」</b>。<br><br>下一讲 <b>L8</b> 讲评测 —— 答的是弱点清单上的最后一条：自由形式的输出很难评估。");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L7 · 接到外部世界</title>")
io.open("cme295-L7.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L7.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
