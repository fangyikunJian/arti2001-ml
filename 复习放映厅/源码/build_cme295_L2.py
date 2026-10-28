# -*- coding: utf-8 -*-
"""CME295 讲座 L2 · Transformer-Based Models & Tricks —— 2026-10-28 新做。

这一讲回答两个问题：
  ① 2017 年那个架构，**八年过去哪几个零件变了**（位置嵌入 / 归一化 / 注意力）；
  ② 今天的模型分成哪三类，以及**为什么只剩 decoder-only 活下来**。
后半场 Shervine 把 encoder-only 这一支讲透（BERT + DistilBERT + RoBERTa）。

底料：CME295/transcripts/L2.txt（933 句人工字幕）
⚠ 全部 says() 的时间码用 源码/tools/quote_ts.py **精确**定位（VTT cue 流，非插值）。
   落盘前必跑：python tools/quote_ts.py --check CME295 L2 build_cme295_L2.py cme295_L2_*.py

引擎的坑（memory/projector-engine-traps.md，十三条，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**、LaTeX 两个反斜杠
  · ⚠ setEq 里 `<` 紧跟字母会被 innerHTML 当标签 ⇒ 公式整个不渲染（坑 11）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许有 HTML 标签**，强调用「」（坑 10）
  · says() 默认 y=150 ⇒ 其下 note 至少 y≥178；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜有**居中** setEq 时，公式带占 279–441 ⇒ 该镜 note 只能落在 [178,265]
  · matrix 底边 = y+(rows-1)*ch+(ch-3) ≤390，且末行文字中心 ≤ 下方 note 的 y−35
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
var CFG={title:"CME295 讲座 L2 · Transformer 的变体与技巧",
  subtitle:"八年里变了哪三个零件 · 为什么只剩 decoder-only · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=yT84Y5zCnaA&t="};

function says(ts,en,y){
  note("🎙 Amidi "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 一串 token 画成一排方块，返回每块中心 x ── */
function seq(x0,y,toks,cls,bw,bh){
  bw=bw||104; bh=bh||44; var cx=[],i;
  for(i=0;i<toks.length;i++){
    var x=x0+i*(bw+10);
    boxNode(x,y,bw,bh,toks[i],(cls instanceof Array)?cls[i]:(cls||"b"));
    cx.push(x+bw/2);}
  return cx;}

/* ── 竖着堆的模块 ── */
function stack(cx,ytop,items,bw,bh,gap){
  bw=bw||250; bh=bh||36; gap=gap==null?8:gap; var i,ys=[];
  for(i=0;i<items.length;i++){
    var y=ytop+i*(bh+gap);
    boxNode(cx-bw/2,y,bw,bh,items[i][0],items[i][1]||"");
    ys.push(y);
    if(i) link(cx,y,cx,y-gap);}
  return ys;}

/* ── 二维平面上的一个向量（画 RoPE 的旋转用）：从原点到 (角度, 长度) ── */
function vec(ox,oy,deg,len,cls,lab){
  var r=deg*Math.PI/180, x=ox+len*Math.cos(r), y=oy-len*Math.sin(r);
  link(ox,oy,x,y); dots([[x,y]],cls||"b",6);
  if(lab) note(lab,x+(x>ox?34:-34),y-6,cls||"b");
  return [x,y];}

/* ── 注意力矩阵：哪些格子被允许看（画全注意力 / 滑窗 / 因果掩码）── */
function attnGrid(x0,y0,n,cell,allow,hlcls){
  var i,j;
  for(i=0;i<n;i++)for(j=0;j<n;j++){
    if(!allow(i,j)) continue;
    boxNode(x0+j*cell, y0+i*cell, cell-4, cell-4, "", hlcls||"b");}}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CME295 讲座 L2","Transformer 的变体与技巧",
      "九讲的第 2 讲 · 约 107 分钟");},
    "第二讲。<b>这一讲的结构很干净，分上下两场，而且两场问的是两个不同层面的问题。</b><br><b>上半场（Afshine）问的是：2017 年那个架构，<u>八年过去哪几个零件变了？</u></b><b>答案是三个 —— 位置嵌入、归一化、注意力本身。</b><br><b>下半场（Shervine）问的是：今天的模型分成哪几类，<u>为什么只剩一类活下来？</u></b><b>然后他把已经「退场」的那一类（encoder-only，代表是 BERT）反而讲得最细 —— 这个安排是有道理的，后面会说。</b><br><b>★★ 而这一讲真正的价值在于它示范了一种读文献的方式</b>：<b>⭐ 不是「有哪些模型」，而是「同一个零件被换过几次，每次为什么」。</b><br><b>⚠ 举个例子你就明白差别了：位置嵌入这一个零件，这一讲里出现了<u>五</u>种做法</b>（<b>学出来的 → 正弦余弦 → T5 的相对位置偏置 → ALiBi → RoPE</b>），<b>而每一种都是前一种的某个具体毛病逼出来的。</b><b>⭐ 记住这条演化链，比记住「现在用 RoPE」有用得多 —— 因为下一个变化来的时候，你能看懂它在修什么。</b><br><b>讲者自己给了这一讲的定调，而这句话值得先记住</b>：<b>这个 2017 年提出的架构，这些年来居然一直都还站得住；有几个部件稍微变了，但总体上，今天的模型或多或少都还是基于最初那个 Transformer。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    var y=200;
    note("这一讲的两场与五条线",640,186,"v");
    boxNode(70,y,520,40,"上半场：哪三个零件变了","y");
    note("① 位置嵌入 —— 换了五次（本讲最长的一条线）",330,y+70,"d");
    note("② 归一化 —— 位置变了（post → pre）、形式也变了（LayerNorm → RMSNorm）",330,y+104,"d");
    note("③ 注意力 —— 治它的 O(n²)：滑窗；以及共享 K/V 投影：MQA / GQA",330,y+138,"d");
    boxNode(690,y,520,40,"下半场：三类模型，谁活下来了","g");
    note("④ encoder-decoder（T5）· encoder-only（BERT）· decoder-only（今天的 LLM）",950,y+70,"d");
    note("⑤ BERT 讲到底：CLS/SEP · MLM+NSP · 蒸馏 · RoBERTa",950,y+104,"d");
    note("⚠ 盯住每一次更换的「理由」，别只记结论 —— 理由才是可迁移的",640,y+180,"y");},
    "<b>先把地图摆出来，这一讲信息量大，没有地图很容易变成名词堆。</b><br><b>上半场三条线</b>：<br><b>① 位置嵌入</b> —— <b>这是最长的一条，占了上半场一大半时间。</b><span class='w'>五种做法依次登场，而讲者在每一种上都明确说了「它的毛病是什么」。</span><br><b>② 归一化</b> —— <b>两处变化：<u>位置</u>从 post-norm 挪到了 pre-norm；<u>形式</u>从 LayerNorm 换成了 RMSNorm。</b><br><b>③ 注意力</b> —— <b>两个方向：一个治 O(n²) 的计算量（滑动窗口注意力），一个治显存（共享 K/V 的投影矩阵，也就是 MQA 与 GQA）。</b><span class='w'>⚠ 这两个方向是「正交」的 —— 讲者自己用了 orthogonal 这个词，意思是可以同时用。</span><br><b>下半场两条线</b>：<br><b>④ 三类架构</b>：<b>encoder-decoder（T5 那一支）· encoder-only（BERT）· decoder-only（今天所有的 LLM）。</b><br><b>⑤ 把 BERT 讲到底</b>，<b>连同两个改进它的工作：DistilBERT（蒸馏）与 RoBERTa（去掉一个目标函数）。</b><br><b>★ 最后给一个看这一讲的建议：每遇到一个新名字，先别管它叫什么，先问「它在修什么毛病」。</b><b>⭐ 这一讲里十几个缩写，真正需要记住的只有「毛病 → 对策」这五六对。名字查得到，因果关系查不到。</b>");
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


import cme295_L2_a, cme295_L2_b, cme295_L2_c, cme295_L2_d
cme295_L2_a.add(KP)   # 回顾与注意力图 → 位置嵌入：学出来的 / 正弦余弦 / 为什么说得通 / 频率
cme295_L2_b.add(KP)   # 位置信息挪进注意力层：T5 偏置 → ALiBi → RoPE；归一化的两处变化
cme295_L2_c.add(KP)   # O(n²) 与滑动窗口；共享 K/V 投影（MQA/GQA）；三类架构与 T5
cme295_L2_d.add(KP)   # BERT 讲到底 + 蒸馏（DistilBERT）+ RoBERTa

C.append(r'''KP("完 · 八年里换了什么",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L2 · 完","Transformer 的变体与技巧",
      "零件换了，骨架没换");},
    "收一下这一讲。<br><b>★★★ 一句话总结：骨架八年没换，但三个零件各换了一遍，而每一次更换都能说出具体理由。</b><br><b>把三条线各自的「毛病 → 对策」列一遍，这是最该带走的东西</b>：<br><b>① 位置嵌入，换了五次</b>：<br><span class='w'>学出来的嵌入 —— 毛病是<b>依赖训练集</b>，而且<b>只能学到训练时见过的最大位置</b>；</span><br><span class='w'>正弦余弦 —— 治好了外推，<b>而且点积只依赖相对距离</b>；但它是加在<b>输入</b>上的，而我们真正想影响的是<b>注意力层</b>；</span><br><span class='w'>T5 的相对位置偏置 —— 直接加进 softmax 里，但<b>要学</b>，于是又带回了过拟合；</span><br><span class='w'>ALiBi —— 不学了，用确定性公式，<b>但太简单、太受限</b>；</span><br><span class='k'>RoPE —— 回到正弦余弦的世界，但改成<b>旋转 query 和 key</b>，于是 QKᵀ 天然只依赖相对距离。今天多数模型用它。</span><br><b>② 归一化，换了两处</b>：<b>位置从 post-norm 挪到 pre-norm（更稳）；形式从 LayerNorm 换成 RMSNorm（少学一半参数、速度更快，而收敛性相当）。</b><br><b>③ 注意力，两个正交的方向</b>：<b>滑动窗口治 O(n²) 的<u>计算</u>；共享 K/V 投影（MQA / GQA）治 KV 缓存的<u>显存</u>。</b><span class='w'>⚠ 这两件事常被混为一谈，但它们治的是不同的资源。</span><br><br><b>★★ 下半场那条线同样值得单独记：三类架构里，<u>赢的那一类不是因为更聪明，而是因为更好扩展</u>。</b><b>讲者的原话是：人们意识到<u>算力预算最好全部投在 decoder 上</u>；而 next-word prediction「是你能做的最简单的事情」，却被证明效果惊人。</b><br><b>⭐ 把它和 T5 的 span corruption 对比就更清楚了：span corruption 更<u>精巧</u>（要挖空、要 sentinel token、要按序重建），而 next-word prediction 更<u>笨</u>。</b><b>⚠ 结果是笨的那个赢了 —— 因为它更容易扩展，而且和「当一个有用的聊天助手」这件事天然对齐。</b><br><b>★ 这条教训对你的课题是直接可用的：一个更精巧的目标/判据，如果它的代价是「难以扩展」或「需要额外的构造步骤」，那它在大规模下很可能输给一个更朴素但更容易扩展的方案。</b><b>⇒ 所以比较方法时，<u>把扩展性当成一个和精度并列的轴</u>来报，而不是只报固定预算下的精度。</b><br><br><b>⇒ 下一讲 L3 是 Transformers & Large Language Models：正式进入 LLM，而上半场提到的 KV 缓存就在那一讲。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L2 · Transformer 的变体与技巧</title>")
io.open("cme295-L2.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L2.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
