# -*- coding: utf-8 -*-
"""CME295 讲座 L4 · LLM Training —— 2026-10-28 新做。

这一讲回答「这些模型到底是怎么训出来的」，分两场：
  上半场（Afshine）：**预训练** —— 迁移学习的范式、数据与算力的量级、规模定律与
    Chinchilla、训练时内存里要存什么、数据并行 / ZeRO / 模型并行、FlashAttention、量化与混合精度。
  下半场（Shervine）：**微调** —— 为什么要 SFT、指令微调、数据与安全、评估为什么难、
    alignment 与 mid-training、LoRA 与 QLoRA。

⚠ 这是期中考范围的最后一讲（讲者开场说期中考 L1–L4）。

底料：CME295/transcripts/L4.txt（983 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L4 build_cme295_L4.py cme295_L4_*.py

引擎的坑（memory/projector-engine-traps.md，十五条，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**；⚠ 里面不许「< 紧跟字母」（坑 11）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=150 ⇒ 其下 note 至少 178；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜两条 note 的 y **至少差 19**（文字框高 18）（坑 12）
  · ⚠ stack()/seq() 自己算几何，⑨⑩ 看不见 ⇒ 底边与末格标签要手算（坑 13）
  · ⚠ 有**居中** setEq 的镜，note 只能落在 [178,265]
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
var CFG={title:"CME295 讲座 L4 · LLM 是怎么训出来的",
  subtitle:"预训练与规模定律 · 并行与 FlashAttention · 微调 / 评估 / LoRA · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=VlA_jt_3Qc4&t="};

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

/* ── 几块 GPU 并排，每块里标注它持有什么 ── */
function gpus(x0,y,n,hold,cls,bw,bh){
  bw=bw||250; bh=bh||44; var i;
  for(i=0;i<n;i++){
    var x=x0+i*(bw+16);
    boxNode(x,y,bw,bh,"GPU "+(i+1),cls||"b");
    if(hold&&hold[i]) note(hold[i],x+bw/2,y+bh+26,"d");}}

/* ── 一个矩形被切成若干块（画 tiling / 分片）── */
function tiles(x0,y,cols,rows,cw,ch,cls,mark){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++)
    boxNode(x0+i*cw,y+j*ch,cw-4,ch-4,"",
      (mark&&mark(i,j))?(mark(i,j)):(cls||"b"));}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L4","LLM 是怎么训出来的",
      "九讲的第 4 讲 · 约 107 分钟");},
    "第四讲，而讲者开场说他「一直很期待今天」。<br><b>把前四讲连起来看，这一讲的位置就很清楚了</b>：<b>L1 讲了自注意力和 Transformer 是什么；L2 讲了今天的模型做了哪些改动；L3 定义了 LLM 并讲了它怎么<u>生成</u>；而这一讲讲它怎么<u>被训出来</u>。</b><br><b>⚠ 这也是期中考的范围终点 —— 讲者在开场说期中考考 L1 到 L4。</b><br><b>分两场，而两场的性质很不一样</b>：<br><b>上半场（预训练）<u>几乎全是工程</u></b>：<b>数据从哪来、算力怎么量、固定预算下模型该多大、一块 GPU 装不下怎么办、怎么把注意力算得更快、精度能砍到多低。</b><br><b>下半场（微调）<u>几乎全是「怎么定义你要什么」</u></b>：<b>为什么预训练完的模型不好用、怎么教它当助手、数据从哪来、安全怎么管、<u>以及最难的那个问题：怎么判断一个模型好不好</u>。</b><br><b>★★ 我建议你用两个完全不同的姿态看这两场。</b><b>⭐ 上半场看「<u>资源之间怎么搬运</u>」—— 几乎每个技巧都是拿一种资源换另一种（算力换内存、通信换显存、重算换存储）。</b><b>⭐ 下半场看「<u>目标怎么被一步步说清楚</u>」—— 从「预测下一个词」到「当个有用的助手」再到「还要无害」，每一步都要把一个模糊的要求变成可优化的东西。</b><br><b>⇒ 而这两件事，正好是你做研究时反复要做的两件事。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("LLM 的训练流水线：这一讲讲前两段",640,186,"v");
    stack(250,214,[["① 预训练 pre-training","g"],["目标：预测下一个 token","d"],["数据：整个互联网","d"],["⭐ 最贵的一步","y"]],340,34,8);
    stack(640,214,[["② 微调 SFT","b"],["目标：当个有用的助手","d"],["数据：指令—回答对","d"],["⭐ 小几个数量级","y"]],340,34,8);
    stack(1030,214,[["③ 偏好调优","d"],["下一讲（L5）","d"],["② + ③ 合称 alignment","v"],["⚠ 还有个新冒出来的 mid-training","r"]],340,34,8);
    note("⇒ 两条主线：上半场「资源怎么搬运」，下半场「目标怎么说清楚」",640,386,"y");},
    "<b>先把流水线摆出来，因为这一讲的内容要挂在这条线上才不散。</b><br><b>① 预训练</b>：<b>在海量数据上训练，目标就是<u>预测下一个 token</u>。</b><b>讲者说它<u>在算力、成本、一切方面都是最贵的那一步</u>。</b><br><b>② 微调（SFT）</b>：<b>把预训练好的权重再训一轮，让它<u>能当个有用的助手</u>。</b><b>⭐ 数据量比预训练<u>小好几个数量级</u>，但质量要求高得多。</b><br><b>③ 偏好调优</b>：<b>下一讲（L5）的内容。而 ② + ③ 合起来叫 <u>alignment</u>（对齐）。</b><br><b>⚠ 讲者还提了一个很新的东西：<u>mid-training</u>（中期训练）—— 在预训练和微调<u>之间</u>的一步，目标函数仍是预测下一个 token，但数据换成和你真正关心的任务更贴近的那些。他说这是个「正在冒头的趋势」。</b><br><b>⇒ 这一讲讲前两段；第三段下一讲讲。</b><br><b>★ 最后给一个看这一讲的实用提醒：这一讲的缩写和术语密度同样很高（FLOPs/FLOPS、ZeRO、DP、SFT、MMLU、LoRA、NF4…）。</b><b>⚠ 而其中<u>有一对是故意长得几乎一样的</u> —— FLOPs 和 FLOPS。讲者专门停下来区分了它们，而且提醒说「论文里有人会把两者混用」。那一段值得特别留意。</b>");
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


import cme295_L4_a, cme295_L4_b, cme295_L4_c, cme295_L4_d
cme295_L4_a.add(KP)   # 迁移学习 → 预训练 → FLOPs/FLOPS → 规模定律 → Chinchilla → 四个挑战
cme295_L4_b.add(KP)   # 训练要存什么 → 数据并行 → ZeRO → 模型并行
cme295_L4_c.add(KP)   # FlashAttention（两种内存 / tiling / 重算）→ 量化 → 混合精度
cme295_L4_d.add(KP)   # SFT → 指令微调 → 数据与安全 → 评估为什么难 → alignment → LoRA → QLoRA

C.append(r'''KP("完 · 两场，两种思路",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L4 · 完","LLM 是怎么训出来的",
      "资源的搬运 · 目标的说清");},
    "收一下这一讲，两场各带走一条主线。<br><b>★★ 上半场：几乎每一个技巧都是<u>把一种资源换成另一种</u>。</b><br><span class='w'><b>数据并行</b>：拿<u>通信</u>换<u>每卡的内存</u>（但每张卡仍要装下整个模型）。</span><br><span class='w'><b>ZeRO</b>：把优化器状态 / 梯度 / 参数依次切开 —— 拿<u>更多通信</u>换<u>更少冗余</u>。</span><br><span class='w'><b>模型并行</b>（专家 / 张量 / 流水线）：把一次前向本身切开。</span><br><span class='k'><b>FlashAttention</b>：⭐ 这一个最特别 —— 它拿「<u>多算一些</u>」换「<u>少读写显存</u>」，而因为瓶颈本来就是读写，<b>结果是又省内存又更快</b>。讲者自己说这「很了不起」，因为重算通常是拿运行时间换内存，而这里<u>两头都赚</u>。</span><br><span class='w'><b>量化 / 混合精度</b>：拿<u>数值精度</u>换<u>内存和速度</u>。</span><br><b>⇒ 可带走的判断方法：看到一个优化，先问「它<u>省了什么、又多花了什么</u>」。几乎没有凭空的节省 —— 而 FlashAttention 那种两头都赚的，恰恰说明原来的做法在瓶颈上判断错了。</b><br><br><b>★★★ 下半场：每一步都是在<u>把一个模糊的要求变成可优化的东西</u>，而这条线越往后越难。</b><br><span class='w'>「预测下一个 token」—— 完全可优化，<b>而且标签免费</b>。但它训出来的东西<u>不是助手</u>：你问「泰迪熊能放洗衣机吗」，它会接着聊泰迪熊是什么做的。</span><br><span class='w'>「当个有用的助手」—— 要人写的指令—回答对，<b>而且损失只从回答开始算</b>（不对输入做 teacher forcing）。贵，但还算说得清。</span><br><span class='k'>「还要无害」—— 拒答、hedging 也被写进了数据混合里。<b>到这里「好」已经不是一个单一的量了。</b></span><br><span class='k'>⭐ 「到底好不好」—— <b>这一步讲者明说是难题</b>：benchmark 会被「在测试任务上训练」污染；Chatbot Arena 的排名可被操纵、而且用户判断不了事实性、还对 emoji 和拒答有偏好偏差。</span><br><b>⇒ 他的结论很诚实：<u>没有哪一个数字能告诉你你关心的东西，是所有这些合起来，而且最终要看你自己的用途</u>。</b><br><br><b>★ 对你的课题，这一讲最值钱的是最后这条线。</b><b>⭐ 你也要把「最便宜的可行配置」从一句话变成一个可优化、可度量的东西，而这一讲展示了这个过程中会踩到的坑</b>：<b>代理指标会被过度优化（training on the test task）、单一数字会掩盖多个维度、以及<u>评判者本身的偏好会带进偏差</u>。</b><br><b>⇒ 而最该照抄的是他的那个结论形式：<u>不要只报一个数，要报一组维度，并说清每个维度量的是什么</u>。</b><br><br><b>⇒ 下一讲 L5 是 LLM Tuning：偏好调优（alignment 的后半段）。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L4 · LLM 是怎么训出来的</title>")
io.open("cme295-L4.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L4.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
