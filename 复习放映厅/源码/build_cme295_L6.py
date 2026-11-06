# -*- coding: utf-8 -*-
"""CME295 讲座 L6 · LLM Reasoning —— 2026-10-29 新做。

这一讲回答两个问题（讲者自己立的目标）：**推理模型是什么**，以及**它们是怎么训出来的**。
  上半场（Afshine）：vanilla LLM 的四个弱点 → 推理的操作性定义 → 把 CoT 放大 →
    两个直觉（难题拆成见过的零件 / 多生成 token = 多给算力）→ 时间线与计费 →
    benchmark 与 ⭐ pass@k 的完整推导 → 为什么用 RL 不用 SFT → 两个可验证奖励 →
    思考预算 → ⭐ GRPO（group relative advantage）→ 模型账 → 两个损失的异同 →
     长度膨胀的根因（1/|o_i|）与 DAPO / Dr. GRPO。
  下半场（Shervine）：R1-Zero 的配方与毛病 → R1 的四阶段流水线 → 结果 → ⭐ 推理能力的蒸馏。

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

/* ⚠ 2026-11-05：items 既收 ["文字", …] 也收 [["文字","cls"], …]（坑 21）。*/
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
    setTitle("CME295 讲座 L6","LLM 推理：让模型「先想，再答」",
      "九讲的第 6 讲 · 约 107 分钟");},
    "第六讲，而讲者开场说<b>「今天其实是个令人兴奋的日子」</b> —— 因为要讲过去一年最热的那个话题：<b>LLM 推理</b>。<br>⭐ 他给这一讲立了两个目标，而且说得很明确：「今天的目标是知道「推理模型是什么」，第二个大目标是「它们是怎么训出来的」。希望这一讲结束时，如果你对这两个问题有好答案，那就说明我们做得不错。」<br>所以你听的时候可以一直用这两个问题自检。<br><br>先说它和上一讲的关系，因为这一讲<b>不是另起一摊</b>：讲者说「这和上次讲的偏好调优接得很好，因为我们在第 5 讲用的很多方法，正是这一讲要用作地基的那些」。具体接的是 L5 的后半截：RL 的那张翻译表、advantage、clip、KL、PPO 的两个变体。<br>⭐ 而今天只加了一件新东西，但它改变了整件事的性质：<b>奖励不用学了</b>。L5 为了拿到奖励必须先训一个奖励模型（那是「两段式」和「四个模型」的根源）；而推理任务<b>天然有可验证的奖励</b> —— 代码过不过测试、数学答案对不对，直接能算。这一条会在这一讲里反复生效，所以现在就记住它。<br><br>⚠ <b>两个提醒。</b>① 讲者自己说 GRPO 与 PPO 两个损失的对照「<b>大概是整门课最难的部分</b>」，而且他给了一个「<b>最低限度记住这两句就算过关</b>」的版本 —— 我会把那个版本单独摆出来。② 这一讲的内容<b>几乎全来自 2024 或 2025</b>。但讲者说我们算幸运，因为「现在我们有足够的后见之明，能知道哪一块比别的更重要」。<br>顺带一个时间感：这一讲录于 2025 年 11 月上旬（讲者提到「前几天我们有一场选举」，并说今天是 11 月 7 日）。");
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);noTitle();
    note("这一讲的四段路线",640,186,"v");
    stack(250,214,[["① 是什么","g"],["推理的操作性定义","d"],["把 CoT 放大","d"],["⭐ 想得久 = 算得多","y"]],340,32,6);
    stack(640,214,[["② 怎么量","b"],["代码 / 数学 benchmark","d"],["⭐ pass@k 的完整推导","y"],["温度与多样性","d"]],340,32,6);
    stack(1030,214,[["③ 怎么训","y"],["为什么 RL 不 SFT","d"],["⭐ GRPO 与组内相对基线","g"],["④ ⭐ 长度膨胀 + R1 流水线","r"]],340,32,6);
    note("⇒ 而全讲最精彩的一段是：一个「取平均」的因子造出了方向明确的错误激励",640,386,"y");},
    "<b>把路线先摆出来，因为这一讲的四段是一条很干净的「先定义、再度量、再训练、再修 bug」的线。</b><br><b>① 是什么。</b>⚠ 讲者先承认<b>推理这个词没有公认定义</b>，然后给了一个操作性的：<b>解决问题的能力，而且需要多步</b>。核心想法不新 —— 就是把第 2、3 讲讲过的 CoT 放大到很大规模。而他给的两个直觉都很硬，尤其第二个：多生成 token 字面上就是多给算力（每一步生成都是一次完整前向）。<br><b>② 怎么量。</b>代码类靠「过不过测试」、数学类靠「解析答案再比真值」。⭐ 而 <b>pass@k</b> 那一段讲者<b>完整推导了一遍</b>（补事件 → 不放回抽样 → 组合数），因为「答案不见得平凡，我不想让你被它的样子吓到」。<b>这是全讲数学上最漂亮的一小节</b>。<br><b>③ 怎么训。</b>三个理由否掉 SFT、选中 RL（最关键的一条：推理任务天然有可验证奖励）。然后是 <b>GRPO</b> —— 它和 PPO 只差一处：用「同组其它回答的均值」当基线，于是不需要价值函数。<br><b>④  修 bug 与完整配方。</b>这是我认为全讲最精彩的部分：输出长度会不受控地膨胀，而根因是目标函数里一个用来「取平均」的 1/|o_i| 因子。它造出了一个方向明确的错误激励（<b>宁可输出长的坏答案</b>），而找出它靠的不是跑实验，是把那个因子换个位置重新读一遍。<br>最后是 DeepSeek R1 的完整流水线，以及一个反直觉的结论：<b>小模型上蒸馏比从头做 RL 更有效</b>。");
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


# ⚠ 2026-11-06 重做为「走查式」：顺着字幕第 1 句走到第 876 句，每镜 ≤6 句。
import cme295_L6_a, cme295_L6_b, cme295_L6_c, cme295_L6_d, cme295_L6_e
import cme295_L6_f, cme295_L6_g, cme295_L6_h, cme295_L6_i, cme295_L6_j
import cme295_L6_k, cme295_L6_l, cme295_L6_m, cme295_L6_n
cme295_L6_a.add(KP)   # 句 1–57     开场 / 训练三步回顾 / RL 的设定 / RL 损失两部分 / PPO 两变体
cme295_L6_b.add(KP)   # 句 58–113   vanilla LLM 的强项与四个弱点 / 两个目标 / 推理的定义
cme295_L6_c.add(KP)   # 句 114–167  借 CoT / preamble 追问 / 两个直觉 / 输出 = 推理 + 答案
cme295_L6_d.add(KP)   # 句 168–217  时间线 o1→R1 / 怎么认出推理模型 / 思考摘要 / 定价
cme295_L6_e.add(KP)   # 句 218–285  编程与数学 benchmark / 可验证 / pass@k 的定义与辩护
cme295_L6_f.add(KP)   # 句 286–355  pass@k 的完整推导（取补 → 无放回 → 组合数）/ pass@1
cme295_L6_g.add(KP)   # 句 356–416  温度与 pass@k / consensus@k / 为什么不走 SFT / 试 RL
cme295_L6_h.add(KP)   # 句 417–475  两个可验证奖励 / R1-Zero 曲线 / 思考预算 / takeaway
cme295_L6_i.add(KP)   # 句 476–539  GRPO 登场 / value function 瓶颈 / 组内相对 / 为什么
cme295_L6_j.add(KP)   # 句 540–610  两张流程图走查 / 冻结与要训 / 损失的异同
cme295_L6_k.add(KP)   # 句 611–680  「最难的部分」/ 两句话 / 长度膨胀 / 损失逐项 / 1/|o_i|
cme295_L6_l.add(KP)   # 句 681–740  坏激励的完整论证 / DAPO 与 Dr. GRPO / 另两个修改 / 交棒
cme295_L6_m.add(KP)   # 句 741–790  旧流程 / R1 两段式 / R1-Zero 配方 / 模板 / 两个问题
cme295_L6_n.add(KP)   # 句 791–876  R1 四阶段流水线 / 结果两簇 / 蒸馏「另一种口味」/ 收尾

C.append(r'''KP("完 · 一条可验证的奖励，和三处被钻的归一化",
function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","LLM 推理","两个目标，各一句话");},
    "收一下这一讲。⭐ <b>讲者自己立的两个目标是「推理模型是什么」和「它们怎么训出来的」——我按这两个目标各给一句话。</b><br><span class='k'><b>① 推理模型是什么</b>：输出从「答案」变成「<b>推理链 + 答案</b>」。就这一处结构差别 —— 没有新架构、没有新的层、没有新的注意力机制，它本质上是「把 2022 年那个 chain-of-thought 的 prompting 技巧放大」，并让模型自己就这么做。</span><br><span class='k'><b>② 它们怎么训出来的</b>：在「可验证奖励」上做 RL（GRPO）。而 GRPO 和 PPO 只差一处：PPO 用一个学出来的 value function 当基线，GRPO 用「同一个 prompt 采 g 条的平均奖励」当基线。那一处替换省掉了一整个要训练的模型。</span>");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","地基","奖励不用学 —— 以及它的边界");},
    "<b>而这一讲真正的地基是一句讲者说得很平淡的话：「这就是我们验证一个被生成的回答是否真的正确的方式。」</b><br><span class='w'>这条因果链请背下来：推理任务（数学 / 代码）可验证 ⇒ 奖励可以是一个「函数」而不是一个「模型」⇒ 不用标注、不会被 reward hacking、训练信号可以无限量生成 ⇒ RL 终于能在 LLM 上大规模地跑。<br>⚠ 而它同时划出了<b>边界</b>：这一讲的全部方法都依赖「答案可验证」—— 换到「写一封好邮件」上，整套东西立刻不成立。</span><br><span class='k'>⭐ 请把它和 L5 对照一次，差距是结构性的：L5 要养「四个模型」（策略 / 价值 / 参考 / 奖励），其中奖励模型最麻烦；L6 在推理场景里是「两个神经网络 + 一段代码」—— 而「要训的」从 2 个降到 1 个。</span>");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","三处归一化偏置","看起来中立的细节");},
    "⭐ <b>三处「看起来中立的技术细节，其实塞进了一个你没打算要的偏好」——我认为这是这一讲最该带走的方法论。</b><br><span class='w'>① 1/|o_i|（按自己长度归一化）：它只取决于「这一条有多长」，对整条统一打折 ⇒ <b>同样答错，写短了被罚得更重</b> ⇒ 模型学会「要错就错得长一点」。修法：DAPO 把分母换成整组总长度；Dr. GRPO 把它整个删掉。而最漂亮的验证是：修完之后只有「错解」变短，「对解」长度不变 —— 这正是那个诊断的独有预测。</span><br><span class='w'><b>② 除以组内标准差</b>：难题几乎全错 ⇒ 标准差小 ⇒ advantage 被放大 ⇒ <b>一条「蒙对」的侥幸路径拿到最大梯度</b>。讲者自己就说了「那可能不是最好的做法」。</span><br><span class='w'><b>③ 对称的 clip（同一个 ε）</b>：ε 是乘在 π_old 上的 ⇒ 概率 0.0001 的 token 一轮只能涨到 0.00012 ⇒ 低概率的好想法永远长不起来（熵坍缩）。修法：Clip-Higher，上界放宽、下界留着。</span><br>一句话：每一个归一化、每一个对称假设，都是一个隐含的偏好声明。");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","两段推导","产出都不是公式");},
    "<b>两段推导，而它们的产出都不是公式。</b><br><span class='k'><b>pass@k</b>：1 − C(n−c,k) / C(n,k)。讲者说他推它的理由是「我不想让你在不知道它从哪来的情况下被它长什么样吓到」——而真正要记住的只有一句：<b>「它只是无放回抽样」</b>，公式随时能从这句话重推。边界自检：c=0 给 0、c=n 给 1、k=1 给 c/n（就是普通准确率）。⚠ 而报 pass@k 必须同时报 <b>温度、n、k</b> —— 温度为 0 时 k 条答案逐字相同，这个指标直接退化。</span><br><span class='k'><b>GRPO vs PPO</b>：讲者亲口说这「<b>大概是整门课最难的部分</b>」，并给了「只要告诉自己两件事」的及格线：① 这些算法只是 RL 阶段用来调模型的 ② GRPO 不需要 value function，它用同组其它 completion 的奖励做比较。难点不在单个概念，而在「同时持有五个彼此纠缠的定义」—— 所以「只记差异」才是对策。</span>");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","R1 的两段式","以及那个自举");},
    "⭐ <b>R1 那篇论文的结构，以及那个自举。</b><br><span class='k'><b>R1-Zero</b>（概念验证）：<b>跳过 SFT</b>，直接对一个「还没见过任何监督」的基础模型做 RL。它成功了（AIME 一路涨），而这说明 RL 不是在「教新东西」，是在「把预训练里本来就有的能力调出来」—— 正好接上 L5 那把总钥匙。⚠ 但它的链会<b>混语言、语法乱</b>：讲者的解释是「它没有一个作为背景的「<b>锚</b>」」，而这揭示了 SFT 的第二个作用 —— 它不只教格式，还给后面的 RL 一个合理的原点（π_ref）。</span><br><span class='k'><b>R1</b>（四阶段：SFT → RL → SFT → RL）：<b>① 冷启动</b>：让 R1-Zero 生成链、人去「<b>改</b>」几千条 —— 把「写」这个不可行的任务变成「改」这个可行的任务；<b>② RL</b>：加一个「目标语言 token 比例」的语言一致性奖励（仍然是可验证的）；<b>③ 混合 SFT</b>：3:1，推理那 60 万条用<b>拒绝采样</b>由「上一步训出来的模型」自己生成 —— <b>模型在给自己造教材</b>；<b>④ 最后一轮 RL</b>：有帮助 + 无害，而无害覆盖 think 里的思考过程，有帮助只看用户看到的部分。</span>");
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CME295 L6 · 完","发现很贵，复制很便宜","接到你的课题");},
    "⭐ <b>最后一条结论，我认为是整讲最该带走的那一条。</b><br><span class='k'>「为什么要费劲蒸馏，你本来就可以做同样的 RL」——作者的回答是：在更小的尺寸层级上，蒸馏比直接从零学更高效。原因：<b>RL 是搜索</b>，而小模型的初始分布里那些复杂推理路径概率极低 ⇒ 它几乎采不到、也就学不到；而蒸馏绕过了搜索，直接把答案摆在它面前让它模仿。所以：推理能力需要「足够大的模型 + RL」才能第一次「长」出来，但一旦长出来就可以被「传」下去—— 发现很贵，复制很便宜，而这正好解释了这一整年的格局。</span><br><br><b>⇒ 接到你的课题，我挑三条</b>：① 「可验证 ⇒ 奖励可程序化」正是你那个「代价/可行性可以被精确求解器复核」的结构 —— 而 L5 的 reward hacking 风险在这里被结构性地消掉了，这是一个很强的设计论点；② GRPO 的「用同组采样的均值当基线」就是最朴素的「减基线降方差」，而它的启示是与其学一个估计器，不如找一个不用训练就能得到的基线；③ 那三处归一化偏置值得你在自己的实验里逐条检查 —— 任何「按实例长度 / 难度归一化」的指标，都可能悄悄塞进一个偏好。<br><br>下一讲 L7 是 Agentic LLMs，答的是 vanilla LLM 的弱点二和弱点三：知识过时，和「全是说，没有做」。");
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
