# -*- coding: utf-8 -*-
"""CME295 讲座 L6 · LLM Reasoning —— 2026-10-29 新做。

这一讲回答两个问题（讲者自己立的目标）：**推理模型是什么**，以及**它们是怎么训出来的**。
  上半场（Afshine）：vanilla LLM 的四个弱点 → 推理的操作性定义 → 把 CoT 放大 →
    两个直觉（难题拆成见过的零件 / 多生成 token = 多给算力）→ 时间线与计费 →
    benchmark 与 ★ pass@k 的完整推导 → 为什么用 RL 不用 SFT → 两个可验证奖励 →
    思考预算 → ★ GRPO（group relative advantage）→ 模型账 → 两个损失的异同 →
    ★★ 长度膨胀的根因（1/|o_i|）与 DAPO / Dr. GRPO。
  下半场（Shervine）：R1-Zero 的配方与毛病 → R1 的四阶段流水线 → 结果 → ★ 推理能力的蒸馏。

⚠ 这一讲是期末考范围（L5–L9）的第二讲。
⚠ 讲者自己说 GRPO 与 PPO 两个损失的对照「**大概是整门课最难的部分**」。

底料：CME295/transcripts/L6.txt（878 句人工字幕）
⚠ says() 时间码全部由 源码/tools/quote_ts.py 精确定位。落盘前必跑：
   python tools/quote_ts.py --check CME295 L6 build_cme295_L6.py cme295_L6_*.py

引擎的坑（memory/projector-engine-traps.md，十七条，写之前全读过）：
  · setEq 必须 $$ 包裹、**写成一行**；里面不许「< 紧跟字母」（坑 11）
  · ⚠ setEq 里的反斜杠要写 \\\\ —— 场景 JS 是 JS 源码，`\\theta` 的 `\\t` 会变制表符（坑 16）
  · ⚠ note()/boxNode() 的文字走 .text() ⇒ **不许 HTML 标签**，强调用「」（坑 10）
  · says() y=150 ⇒ 其下 note 至少 178；note ≤386；boxNode 底边 ≤390
  · ⚠ 同一镜两条 note 的 y **至少差 19**（文字框高 18）（坑 12）
  · ⚠ stack()/seq() 自己算几何，⑨⑩ 看不见 ⇒ 底边与末格标签要手算（坑 13）
  · ⚠ 有**居中** setEq 的镜，note 只能落在 [178,265]
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
var CFG={title:"CME295 讲座 L6 · LLM 推理",
  subtitle:"推理模型是什么 · pass@k · GRPO · 长度膨胀的根因 · DeepSeek R1 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=k5Fh-UgTuCo&t="};

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
    setTitle("CME295 讲座 L6","LLM 推理：让模型「先想，再答」",
      "九讲的第 6 讲 · 约 107 分钟");},
    "第六讲，而讲者开场说<b>「今天其实是个令人兴奋的日子」</b> —— 因为要讲过去一年最热的那个话题：<b>LLM 推理</b>。<br><b>★ 他给这一讲立了两个目标，而且说得很明确：「<u>今天的目标是知道「推理模型是什么」，第二个大目标是「它们是怎么训出来的」。希望这一讲结束时，如果你对这两个问题有好答案，那就说明我们做得不错</u>。」</b><br><b>⇒ 所以你听的时候可以一直用这两个问题自检。</b><br><br><b>先说它和上一讲的关系，因为这一讲<u>不是另起一摊</u></b>：<b>讲者说「<u>这和上次讲的偏好调优接得很好，因为我们在第 5 讲用的很多方法，正是这一讲要用作地基的那些</u>」。</b><b>⇒ 具体接的是 L5 的后半截：<u>RL 的那张翻译表、advantage、clip、KL、PPO 的两个变体</u>。</b><br><b>★★★ 而今天只加了一件新东西，但它改变了整件事的性质：<u>奖励不用学了</u>。</b><b>L5 为了拿到奖励必须先训一个奖励模型（那是「两段式」和「四个模型」的根源）；而推理任务<u>天然有可验证的奖励</u> —— <u>代码过不过测试、数学答案对不对，直接能算</u>。</b><b>⇒ 这一条会在这一讲里反复生效，所以现在就记住它。</b><br><br><b>⚠ 两个提醒。</b><b>① 讲者自己说 GRPO 与 PPO 两个损失的对照「<u>大概是整门课最难的部分</u>」，而且他给了一个「<u>最低限度记住这两句就算过关</u>」的版本 —— 我会把那个版本单独摆出来。</b><b>② 这一讲的内容<u>几乎全来自 2024 或 2025</u>。但讲者说我们算幸运，因为「<u>现在我们有足够的后见之明，能知道哪一块比别的更重要</u>」。</b><br><b>⇒ 顺带一个时间感：这一讲录于 2025 年 11 月上旬（讲者提到「前几天我们有一场选举」，并说今天是 11 月 7 日）。</b>");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的四段路线",640,186,"v");
    stack(250,214,[["① 是什么","g"],["推理的操作性定义","d"],["把 CoT 放大","d"],["★ 想得久 = 算得多","y"]],340,34,8);
    stack(640,214,[["② 怎么量","b"],["代码 / 数学 benchmark","d"],["★ pass@k 的完整推导","y"],["温度与多样性","d"]],340,34,8);
    stack(1030,214,[["③ 怎么训","y"],["为什么 RL 不 SFT","d"],["★ GRPO 与组内相对基线","g"],["④ ★★ 长度膨胀 + R1 流水线","r"]],340,34,8);
    note("⇒ 而全讲最精彩的一段是：一个「取平均」的因子造出了方向明确的错误激励",640,386,"y");},
    "<b>把路线先摆出来，因为这一讲的四段是一条很干净的「先定义、再度量、再训练、再修 bug」的线。</b><br><b>① 是什么。</b><b>⚠ 讲者先承认<u>推理这个词没有公认定义</u>，然后给了一个操作性的：<u>解决问题的能力，而且需要多步</u>。</b><b>核心想法不新 —— <u>就是把第 2、3 讲讲过的 CoT 放大到很大规模</u>。而他给的两个直觉都很硬，尤其第二个：<u>多生成 token 字面上就是多给算力（每一步生成都是一次完整前向）</u>。</b><br><b>② 怎么量。</b><b>代码类靠「过不过测试」、数学类靠「解析答案再比真值」。</b><b>⭐ 而 <u>pass@k</u> 那一段讲者<u>完整推导了一遍</u>（补事件 → 不放回抽样 → 组合数），因为「答案不见得平凡，我不想让你被它的样子吓到」。<u>这是全讲数学上最漂亮的一小节</u>。</b><br><b>③ 怎么训。</b><b>三个理由否掉 SFT、选中 RL（<u>最关键的一条：推理任务天然有可验证奖励</u>）。然后是 <u>GRPO</u> —— 它和 PPO 只差一处：<u>用「同组其它回答的均值」当基线，于是不需要价值函数</u>。</b><br><b>④ ★★ 修 bug 与完整配方。</b><b>这是我认为全讲最精彩的部分：<u>输出长度会不受控地膨胀，而根因是目标函数里一个用来「取平均」的 1/|o_i| 因子</u>。</b><b>⇒ 它造出了一个方向明确的错误激励（<u>宁可输出长的坏答案</u>），而<u>找出它靠的不是跑实验，是把那个因子换个位置重新读一遍</u>。</b><br><b>⇒ 最后是 DeepSeek R1 的完整流水线，以及一个反直觉的结论：<u>小模型上蒸馏比从头做 RL 更有效</u>。</b>");
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


import cme295_L6_a, cme295_L6_b, cme295_L6_c, cme295_L6_d
cme295_L6_a.add(KP)   # 四个弱点 → 推理的定义 → 放大 CoT → 两个直觉 → 时间线 → 摘要 → 计费
cme295_L6_b.add(KP)   # 代码/数学 benchmark → pass@k 的定义与推导 → 温度 → consensus@k
cme295_L6_c.add(KP)   # 为什么 RL → 两个可验证奖励 → 思考预算 → GRPO → 模型账 → 损失异同
cme295_L6_d.add(KP)   # 长度膨胀 → 1/|o| 根因 → DAPO/Dr.GRPO → 另两个改良 → R1-Zero → R1 → 蒸馏

C.append(r'''KP("完 · 一条可验证的奖励，和一个被钻的归一化",
function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","LLM 推理",
      "奖励不用学 · 基线不用学 · 而偏置藏在取平均里");},
    "收一下这一讲。<b>讲者立的两个目标是「推理模型是什么」和「它们怎么训出来的」，我按这两个目标各给一句话，再给三条我觉得对你最值钱的。</b><br><b>★ 推理模型是什么</b>：<b>输出<u>不只是答案，而是「推理链 + 答案」</u>。而它为什么有用有两个直觉 —— <u>难题没在训练集里出现过，所以拆成见过的零件；以及多生成 token 字面上就是多给算力</u>。</b><br><b>★ 它们怎么训出来的</b>：<b><u>用 RL，奖励是「格式对不对 + 答案对不对」两个可验证的布尔判断</u>。R1-Zero 证明了<u>连 SFT 都可以不要</u>；而完整的 R1 是四段流水线，用一点点 SFT 给它<u>加一个锚</u>。</b><br><br><b>★★ 三条脉络，我建议按这个顺序记。</b><br><span class='k'><b>① 这一讲省掉了两个模型，而两次「省」的来源完全不同。</b><u>奖励模型是「任务可验证」省掉的</u>（环境的性质 —— 换个任务，比如要调语气，它就省不掉了，而且 PPO 在推理场景里也一样不需要）；<u>价值函数是「换算法」省掉的</u>（GRPO 用同组其它回答的均值当基线 —— 这才是 GRPO 真正的功劳，而且与任务无关、可迁移）。<b>⇒ 读论文时的追问：这个改进是因为换了问题，还是因为换了方法？只有后者能迁移。</b></span><br><span class='k'><b>② 两次「用多采样代替学一个模型」。</b>L5 的 Best-of-N 用多生成代替训练；L6 的 GRPO 用多生成代替价值函数。<b>⇒ 这笔交换在 LLM 上划算，原因很具体：<u>生成可并行，而且生成不会「训坏」；多一个要训的网络会</u>。</b>而代价也很具体：<u>每个 prompt 的生成成本乘了 g 倍</u>。</span><br><span class='k'><b>③ ⭐ 全讲最精彩的一段：长度膨胀的根因。</b>现象是「性能已经平了、长度还在涨」—— <b>而这个「脱钩」才是证据</b>（一路同涨就没理由怀疑）。根因是目标函数里的 <u>1/|o_i|</u>：把它挪到外层读，它就是「<u>只取决于你在哪条输出里</u>」的权重 ⇒ 短输出里的 token 权重更大 ⇒ advantage 为负时<u>短的坏答案被压得更狠</u> ⇒ 模型学会<u>宁可输出长的坏答案</u>。<b>⇒ 这是 reward hacking 最具体的一个版本：被钻的不是奖励模型，而是一个用来「取平均」的归一化因子。而找出它靠的不是跑实验，是把那个因子换个位置重新读一遍。</b></span><br><br><b>★★★ 对你的课题，我认为这一讲有四条能直接用。</b><br><span class='w'><b>① 你和推理训练处在同一个幸运位置。</b>你的「可行」与「代价」是<u>可精确判定</u>的，所以你<u>不需要学一个奖励模型</u>，可以直接拿真值当信号。<b>⇒ 这一点该在论文里明说，它是你能用更强搜索的前提</b>；而 L5 那个最棘手的 reward hacking，在这个设定下也不会从奖励侧发生。</span><br><span class='w'><b>② GRPO 的基线给了你一条绕开「价值函数之难」的路。</b>你的 MCTS 若难以给<u>部分配置</u>一个可靠的价值估计（那正是 PPO 的 value function 难的地方），可以改用<u>同一父节点下兄弟分支的相对表现</u>当基线 —— <b>不用学模型，只要多展开几个</b>。而「<u>减掉同条件均值以消除实例难度</u>」这条，也是你跨实例汇总结果时必须做的归一化（讲者的直觉：<u>简单题拿高分可能只是因为题简单</u>）。</span><br><span class='w'><b>③ pass@k 那一段给了你两样东西。</b>一是<u>要报的量和用来估它的样本量可以不一样</u> —— 用 n 个样本去估「若只抽 k 个会怎样」，是用数据换方差；<b>你报「预算 k 次调用下的成功率」时就该这么估，而不是真的只跑 k 次</b>。二是<u>极限情形自检</u>（代 k=1 得 c/n）—— 这个动作该成为你每个公式的默认收尾。</span><br><span class='w'><b>④ ⚠ 去检查你自己的归一化因子。</b>按配置规模归一化的代价、按分支数平均的 UCT 分数、按相对比例设的剪枝阈值（「比当前最优差 10% 就剪」在代价小的实例上过严、在代价大的实例上过松）—— <b>任何一个 1/n 都可能在悄悄偏向某个 n</b>。而本讲给的检查办法很便宜：<u>把那个因子换个位置重新读一遍，再问「它和我的判据符号配起来，会偏向什么」</u>。</span><br><br><b>⇒ 另外两条实验习惯，比技术内容还值钱</b>：<b>① <u>按机制预测的那一部分去拆分验证</u> —— 修 1/|o| 的证据不是「平均长度下降了」，而是「<u>正确样本长度不变、错误样本长度大降</u>」，正好对应那个偏置只在答错时起坏作用。② <u>先验证一个极端做法能走多远，再把毛病逐个补上</u> —— R1-Zero（纯 RL、零监督）就是这么用的，它既是最强的消融基线，也告诉你后来加的每一样东西各自在补什么。</b><br><br><b>⇒ 下一讲 L7 是 Agentic LLMs，修的是本讲开头那张弱点清单上的第二和第三条（知识截止、光说不做）。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CME295 讲座 L6 · LLM 推理</title>")
io.open("cme295-L6.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cme295-L6.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
