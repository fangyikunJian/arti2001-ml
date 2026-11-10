# -*- coding: utf-8 -*-
"""CME295 L1 模块 h —— 字幕第 576–730 句（65:00–83:46）：注意力的想法、transformer、
Q/K/V、架构里三处注意力各自在做什么、位置编码，以及多头。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（32 镜 → 19 镜）。
"""


def qkv(hi):
    c = lambda i: '"y"' if i == hi else '"d"'
    return ('  boxNode(80,254,330,50,"Q · query 我在找什么",%s);\n'
            '  boxNode(475,254,330,50,"K · key 我以什么被找",%s);\n'
            '  boxNode(870,254,330,50,"V · value 我贡献什么",%s);\n'
            % (c(1), c(2), c(3)))


def add(KP):

    KP("⭐ 注意力与 transformer：Q / K / V",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:00","people have tried having more direct connections",166);
  says("65:32","So in this example, let us suppose I am trying to translate an English sentence into a French one",192);
  note("⭐ 注意力的想法，是直接从 RNN 的病引出来的",640,222,"y");
  boxNode(80,254,500,50,"RNN：信息走长路","r");
  boxNode(700,254,500,50,"注意力：别走长路","g");
  note("一百步之前的信息要沿着链传一百次",330,328,"r");
  note("在「要预测的」和「过去某处」之间直接连一条线",950,328,"g");
  note("⚠ 「如果我知道我正试图预测的是哪个词，那该多好」—— 这个念头就是起点",640,374,"r");''',
         "<b>注意力的想法，讲者是直接从 RNN 的病引出来的。</b><br>⭐ 「<b>出于『模型记不住过去的东西』这个事实，人们试着让『某个东西』和『过去的那个东西』之间有更直接的连接 —— 而这就是 attention 背后的想法</b>」。<br>⭐ 请看清这个想法有多朴素：<b>既然信息走长路会被挤掉，那就别走长路</b> ⇒ <b>对照 RNN：要用到一百步之前的信息，它得沿着链一棒一棒传一百次；而注意力直接在两点之间连一条线</b>。<br>⚠ 而他把自己放在「<b>解码到一半</b>」的位置上来讲这个直觉：「<b>当我想生成译文的下一个词时，如果我知道我正试图预测的是哪个词，那该多好</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("66:07","Or in other words, it would be great if I could take a peek at a certain area of the input text",166);
  says("66:42","And this concept is going to actually be key for this class",192);
  note("⭐ 整个机制最好的那句直觉：朝输入的某个区域「瞥一眼」",640,222,"y");
  boxNode(80,254,500,50,"接力棒（RNN）","r");
  boxNode(700,254,500,50,"直拨电话（注意力）","g");
  note("一棒一棒传，远了就损耗，而且要排队",330,328,"r");
  note("任意两点之间一条线，距离不重要，还能同时拨",950,328,"g");
  note("⚠ 代价：n 个位置两两连线 = n² 条 —— 序列长一倍，连线多四倍",640,374,"r");''',
         "<b>这一句是整个注意力机制最好的直觉表述。</b><br>⭐ 「<b>如果我能朝输入文本的某个区域瞥一眼（take a peek），那该多好</b>」—— 「瞥一眼」这个词选得很好，<b>它暗示了两件事：① 是有选择的（不是把整个输入都看一遍）;② 是直接的（不经过中间任何人转手）</b>。它<b>2014 年被引入，同样是为了解决长程依赖</b>。<br>⭐ 而讲者给了它一个很高的定位：「<b>这个概念实际上会是这门课的关键 —— 注意力机制就是那个让一切、我是说让大部分东西能工作起来的东西</b>」（<b>留意那个自我更正：他不愿意说一句稍微夸张一点的话</b>）。<br>⚠ 但直拨电话有代价：<b>n 个位置两两连线就是 n² 条 —— 这正是前面那句「复杂度是序列长度的函数」的兑现</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:12","So the transformer, which is the core architecture that we will see in this class",166);
  says("67:28","So what the authors tried to do was to move away from this sequential way of processing the text",192);
  note("⭐ 论文标题本身就是一句主张：Attention is All You Need（2017）",640,222,"y");
  boxNode(80,254,500,50,"在那之前","d");
  boxNode(700,254,500,50,"这篇论文","g");
  note("注意力是加在 RNN 上的一个增强",330,328,"d");
  note("把 RNN 整个拿掉，只留注意力",950,328,"g");
  note("⚠ 两个关键词：「一次性」⇒ 能并行；「直接连接」⇒ 距离无关",640,374,"r");''',
         "<b>本课的核心架构登场，而它的论文标题本身就是一句主张。</b><br>⭐ 「<b>光从标题《Attention is All You Need》你就能看出来，作者们想要只依赖那一个部分</b>」—— <b>在那之前注意力是加在 RNN 上的增强；而这篇把 RNN 整个拿掉了，这在当时是很强的主张</b>。<br>⭐ 作者做的事一句话说完：「<b>摆脱这种顺序处理文本的方式，转而让模型一次性地、直接地与文本的所有部分相连 —— 那个东西叫 self-attention</b>」 ⇒ 两个关键词：<b>「一次性（at once）」是并行性的来源；「直接连接」是距离无关的来源</b>。<br>⚠ 而「<b>self（自）</b>」这个字是名字的要害：<b>它指的是「序列自己关注自己」,不是去关注另一个序列</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("68:03","Here what we would say is that in order to compute the representation of the token teddy bear",166);
  says("68:36","So back to your question about riverbank and robbing a bank",192);
  note("⭐ 那个学生早就问过的问题，在这里被回答了",640,222,"y");
  boxNode(80,254,500,50,"river bank","b");
  boxNode(700,254,500,50,"robbing a bank","v");
  note("周围是 river、water ⇒ 混进来的是这些",330,328,"b");
  note("周围是 rob、money ⇒ 混进来的是那些",950,328,"v");
  note("⚠ 两边 bank 的「输入嵌入」是同一个（查同一张表）—— 变的是算完之后的表示",640,374,"r");''',
         "<b>自注意力具体在做什么，用老例子一看就清楚；而它正好回答了那个被提前问到的问题。</b><br>⭐ 「<b>为了算出 token『teddy bear』的表示，我们要一次性地、用直接的链接，看序列里所有其它的 token</b>」 ⇒ 而结果是决定性的：「<b>这里我们会得到一个 teddy bear 的表示，而它对『它所处的那个上下文』是独一无二的</b>」。<br>⭐ 机制：<b>两个句子里 bank 的输入嵌入是同一个（查同一张表）;但自注意力算表示时，会把周围所有词的信息按权重混进来 ⇒ 「river bank」混进 river、water，「robbing a bank」混进 rob、money ⇒ 算完之后两个 bank 的表示就不同了</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  note("⭐ 停下来结一次账：补上了什么，又新欠了什么",640,196,"y");
  boxNode(60,228,250,46,"意义 ✓","g");
  boxNode(330,228,250,46,"上下文化 ✓","g");
  boxNode(600,228,250,46,"记远处 ✓","g");
  boxNode(870,228,250,46,"能并行 ✓","g");
  note("加权求和，权重由内容定  ｜  表示随语境变  ｜  直连  ｜  一次性算",640,296,"g");
  boxNode(340,322,600,46,"⚠ 顺序 ✗ —— 这一条是新欠下的债","r");
  note("⚠ 而且是自找的：主动扔掉顺序处理，就同时扔掉了顺序信息",640,384,"r");''',
         "<b>停下来结一次账，你会看到这条线走得非常完整 —— 只有一个例外。</b><br>⭐ 回到取平均丢掉的三样：<b>① 意义 —— 自注意力是加权求和，权重由内容决定，不是无差别抹平；② 顺序 —— 这一条自注意力自己修不了；③ 与语境无关 —— 刚刚解决</b>。<br>⭐ 再回到 RNN 的三宗罪：<b>记不住远处（解决，直连）· 算得慢（解决，可并行）· 不够上下文化（解决）</b>。<br>⚠ <b>唯独「顺序」是新欠下的债，而且是自找的：transformer 主动扔掉了顺序处理，于是也扔掉了顺序信息</b> ⇒ <b>这笔债讲者后面会专门来还，还的方式叫位置编码</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("69:17","So when you want to express something in terms of something else",166);
  says("69:52","And so what you are going to do is to look at all the other tokens",192);
  note("⭐ 全课最该记牢的一组术语",640,222,"y");
''' + qkv(0) + r'''  note("一句话定义：「当你想用别的东西来表达某个东西时」—— 这就是自注意力",640,330,"y");
  note("⚠ 名字来自检索的隐喻：拿你的 query 去和一堆 key 比，取出对应的 value",640,374,"r");''',
         "<b>这是整门课最该记牢的一组术语，而讲者的引入方式很讲究。</b><br>⭐ 「<b>当你想要用别的东西来表达某个东西时，我们用 query、key、value 这几个词</b>」—— <b>请抓住这句话，因为它就是自注意力的一句话定义：我要算 teddy bear 的新表示，而我要用「句子里所有其它词」来表达它</b>。<br>⭐ 而 <b>Q/K/V 这组术语来自「检索」的隐喻</b>,知道这个会好记很多：<b>你拿着一个 query 去和一堆 key 比对，比对上了就取出那个 key 对应的 value</b>。<br>⇒ 落到例子里：「<b>我们的目标是弄清楚 query（也就是 teddy bear）和其它哪些 token 更相似⋯⋯而其它那些 token 基本上由 key 和 value 组成</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:23","What you are going to do is you are going to take the query teddy bear",166);
  note("⭐ 整个过程走一遍，而最关键的是最后那个「加权」",640,196,"y");
  seq(70,228,["拿 query","和所有 key 比","给更像的加权","取它们的 value"],"g",265,48);
  note("⭐ 注意是「加权」,不是「挑一个」—— 不是只用最相似的那个",640,304,"y");
  note("所有 value 都参与，只是权重不同 ⇒ 这是一个加权平均",640,344,"g");
  note("⚠ 「挑一个」不可导、没法训；「加权」可导 —— 这是它能被学出来的前提",640,384,"r");''',
         "<b>整个过程走一遍，而最关键的是最后那个词。</b><br>⭐ 「<b>你拿 query teddy bear，把那个 query 和所有其它的 key 做比较，看哪个元素最相似，然后给更相似的那些加权，并取它们关联的 value</b>」。<br>⭐ 请注意「<b>加权</b>」和「挑一个」有本质区别：<b>不是找出最相似的那一个然后只用它，而是所有 value 都参与、只是权重不同 —— 这是一个加权平均</b>。<br>⚠ 而这个区别不只是精度问题，<b>它是这个机制能被训练出来的前提</b>:<b>「挑一个」是一个离散操作，不可导、没法反向传播；而「按相似度加权」是连续的、可导的 ⇒ 所以注意力权重可以被学出来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:55","And speaking of query and key and value, we will also see that one benefit",166);
  setBig("「而 GPU 爱矩阵」","用 Q / K / V 表达，整个计算就能写成矩阵形式");
  note("⭐ 「它真的是为我们手上这种硬件而做的」—— 一个算法能不能赢，也看它和硬件合不合",640,322,"y");
  note("⚠ 对照 RNN：它天然顺序、天然不能并行 —— 这正是它输掉的另一半原因",640,362,"r");''',
         "<b>这一条讲的是一个「意外之喜」,但它可能才是 transformer 能赢的真正原因。</b><br>⭐ 「<b>用这种方式表达东西的一个好处：我们可以把『在整个序列上做这个自注意力计算』这件事，表达成矩阵的形式。而 GPU 爱矩阵 —— 所以它真的是为我们手上这种硬件而做的</b>」。<br>⚠ 这五个字值得认真对待，<b>因为它解释了一件更大的事</b>:<b>一个算法能不能赢，不只取决于它的数学性质，还取决于它和硬件合不合得来</b> ⇒ <b>对照 RNN：它天然顺序、天然不能并行，无论 GPU 多少块都派不上用场 —— 这正是它输掉的另一半原因</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("71:26","And I guess what I mentioned here can be expressed in a form of softmax of the query and the key",166);
  setEq("$$\\mathrm{Attention}(Q,K,V)=\\mathrm{softmax}\\!\\left(\\frac{QK^{\\top}}{\\sqrt{d_k}}\\right)V$$","top");
  note("⭐ 逐块读：QKᵀ 是「每个 query 和每个 key 的相似度」",640,318,"y");
  note("除以 √d_k 是缩放 ｜ softmax 把它们变成一组和为 1 的权重 ｜ 再乘 V 做加权平均",640,358,"g");''',
         "<b>这就是这门课最核心的那条公式，而讲者此刻只给直觉，细节留给了最后的走查。</b><br>⭐ 他的说法是：「<b>可以表达成『query 和 key 的 softmax』的形式 —— 它基本上是一种办法，去得到某种权重，表示哪些 value 会更重要；如果一个 value 更重要，你就有更大的权重⋯⋯然后你基本上把那个乘以 value</b>」。<br>⭐ 对着公式逐块读一遍：<b>QKᵀ 给出「每个 query 对每个 key 的相似度」;除以 √d_k 是缩放（维度越高点积越大，不缩放 softmax 会过于尖锐）;softmax 把这些相似度变成一组和为 1 的权重；最后乘 V，就是按权重把各个 value 加起来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("72:47","So first of all, I just want to say that these quantities, they are learned",166);
  says("73:10","So here, you will have something like you want to express this in terms of all the values",192);
  note("⭐ 一个追问：key 和 value 到底代表什么？",640,222,"y");
  boxNode(80,254,500,50,"先划边界","r");
  boxNode(700,254,500,50,"再给一个解释层面的说法","g");
  note("「这些量是学出来的，你不是在把它们固定下来」",330,328,"r");
  note("key 用来比相似，value 是真正被取走的那个向量",950,328,"g");
  note("⚠ 「从解释的角度」—— 他特意区分了「机制上是什么」和「可以怎么理解」",640,374,"r");''',
         "<b>这个追问问到了点子上，而讲者的第一句回答就划清了边界。</b><br>⭐ 「<b>首先我想说的是：这些量是学出来的 —— 所以你不是在把它们固定下来</b>」 ⇒ <b>这纠正了一个很自然的误解：很多人以为 key 和 value 是人为设计的、有明确语义的东西；不是，它们是三个投影矩阵的输出，而那三个矩阵是训练出来的 ⇒ 「key 代表什么」没有人给的答案</b>。<br>⭐ 但他接着给了一个<b>解释层面</b>的说法：「<b>key 在那里，是为了让你弄清哪一个和 query 最相似；而 value 是和那个元素关联的实际的值</b>」 ⇒ <b>注意他特意说了「从解释的角度」—— 他在区分「机制上是什么」和「可以怎么理解」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("73:40","And these projections are actually learned by the model",166);
  note("⭐ 学生逼出来的最后一个关键细节：三者同源",640,196,"y");
  boxNode(460,224,360,46,"同一份输入表示","b");
  link(500,270,260,296);
  link(640,270,640,296);
  link(780,270,1020,296);
  boxNode(140,296,240,46,"× W_q ⟹ Q","y");
  boxNode(520,296,240,46,"× W_k ⟹ K","v");
  boxNode(900,296,240,46,"× W_v ⟹ V","g");
  note("⚠ 不投影会怎样？Q 和 K 就是同一组向量 ⇒ 每个词最关注的永远是它自己",640,370,"r");''',
         "<b>这是学生逼出来的最后一个关键细节，而它把机制补全了。</b><br>⭐ 「<b>还有一件我没提到的事 —— 但你说对了 —— 我们实际上要做投影来得到这些量。而这些投影实际上是模型学出来的</b>」 ⇒ <b>Q、K、V 全都来自同一份输入表示：乘 W_q 得 Q，乘 W_k 得 K，乘 W_v 得 V —— 三者同源，只是被三个不同的、学出来的矩阵变换过</b>（这正是「self」的含义）。<br>⚠ 反过来想就知道为什么必须投影：<b>如果直接拿嵌入当 Q、K、V，那 Q 和 K 就是同一组向量 ⇒ 每个词和自己的点积一定最大 ⇒ 每个词主要在关注自己，机制就退化了</b> ⇒ <b>三个投影给了模型三个自由度：以什么角度去找、以什么角度被找、被找到后贡献什么</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("74:12","the authors propose an architecture that is composed of two parts",166);
  says("75:13","So multi-head attention layer, but multi-head is just doing this computation in different ways",192);
  note("⭐ 架构：两部分，而它的形状直接来自翻译这个任务",640,222,"y");
  boxNode(140,254,420,50,"encoder（左）：源语言输入","b");
  boxNode(680,254,460,50,"decoder（右）：目标语言输出","g");
  note("encoder 内部只有两样：注意力层 + 前馈网络",640,332,"y");
  note("⚠ 而 multi-head「只是用不同的方式去做这个计算，好让模型学到不同的投影」",640,374,"r");''',
         "<b>架构登场，而它的形状直接来自它要解决的那个任务。</b><br>⭐ 「<b>作者提出了一个由两部分组成的架构：一个 encoder 在左边，一个 decoder 在右边。他们的应用是翻译 —— 所以走 encoder 的是你源语言的输入文本，而走 decoder 的是你正在预测的目标语言</b>」 ⇒ <b>这个两段式你在 RNN 那里见过：先把整个源文本处理完得到 context vector，再拿它解码</b>。<br>⭐ encoder 内部只有两样东西：<b>一个 multi-head attention 层，加一个前馈网络</b>。<br>⚠ 而 <b>multi-head 讲者先给了一句话</b>:「<b>只是用不同的方式去做这个计算，好让模型学到不同的表示、不同的投影</b>」—— <b>细节留到最后一个提问</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("75:46","you are going to compute the representation of all the tokens in this text basically as a function of others",166);
  note("⭐ encoder 在做的事，落到那句老例子上",640,196,"y");
  seq(70,228,["a","cute","teddy bear","is","reading"],"b",210,46);
  note("每一个 token 的表示，都被算成「其它所有 token 的函数」",640,300,"y");
  note("⭐ 而 encoder 的自注意力是「全看」的：左边右边都看得到",640,344,"y");
  note("⚠ 这正是 RNN 做不到的那一半 —— 它的隐状态只带左边的上下文",640,384,"r");''',
         "<b>这一镜把 encoder 在做的事落到那句老例子上。</b><br>⭐ 「<b>比如『a cute teddy bear is reading』,你要把这段文本里所有 token 的表示，基本上都算成其它 token 的函数 —— 而你是用 encoder 来做这件事的</b>」。<br>⭐ 请留意一个这里没被强调、但很要紧的性质：<b>encoder 的自注意力是「全看」的 —— 算 teddy bear 的表示时，它既看左边的 a、cute，也看右边的 is、reading</b>。<br>⚠ <b>这正是 RNN 做不到的那一半</b>:<b>RNN 的隐状态只包含「到目前为止」,右边的词还没被处理 ⇒ 而很多时候正是右边的词决定了词义</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("76:50","So this what I just said is the cross-attention layer",166);
  says("77:36","So the way to think about it is you are trying to ask yourself, what are the words from the input that matter",192);
  note("⭐ 第二处注意力：cross-attention —— 而讲者当堂考了一道",640,222,"y");
  boxNode(80,254,500,50,"来自 decoder 的那个箭头","y");
  boxNode(700,254,500,50,"来自 encoder 的两个箭头","b");
  note("是 Q —— 因为这正是「你想弄清楚的那个东西」",330,328,"y");
  note("是 K 和 V —— 被查询的那一方",950,328,"b");
  note("⚠ 记法很通用：谁在「提问」谁就是 Q，被查询的一方提供 K 和 V",640,374,"r");''',
         "<b>第二处注意力，而讲者在这里设计了一道很好的当堂提问。</b><br>⭐ 场景是：<b>你要真的去翻译了，从句首 token 开始，用输入句子的所有表示来弄清接下来该预测什么</b> ⇒ 他问：「<b>decoder 那个箭头代表什么？decoder 是 query、key 还是 value？</b>」<br>⭐ 答案和推理方式：「<b>你在问自己 —— 输入里的哪些词才是要紧的？所以给定你的 query，你想知道输入里哪些元素是要紧的 ⇒ 这个箭头确实是 query；而 key 和 value 实际上来自 encoder，也就是来自输入序列</b>」。<br>⚠ <b>记法很简单而且通用：谁在「提问」谁就是 Q，被查询的那一方提供 K 和 V</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("78:17","And that one is trying to figure out what other tokens of the output sentence",166);
  note("⭐ 第三处注意力，而它的名字 masked 说明了一切",640,196,"y");
  boxNode(80,228,500,50,"已经解码出来的","g");
  boxNode(700,228,500,50,"还没解码的","r");
  note("「un ours en peluche」—— 这些可以看",330,302,"g");
  note("后面的词必须被遮住（mask）",950,302,"r");
  note("⭐ 理由很硬：生成时那些词根本还不存在，看了就是作弊",640,348,"y");
  note("⚠ 而训练时整句真值是给定的 ⇒ 不遮住，模型就会直接抄答案",640,386,"r");''',
         "<b>第三处注意力，而它的名字 masked（被遮住的）说明了一切。</b><br>⭐ 「<b>那一个在试图弄清楚：你正在解码的那个输出句子里，还有哪些 token 会对预测下一个 token 有用</b>」—— 比如你已经说了「un ours en peluche」,要预测下一个词时，<b>你想知道已经翻译出来的那些 token 里哪些有用</b>。<br>⚠ 而为什么要 mask：<b>推理时后面的词根本还不存在；而训练时整句真值是给定的 —— 如果不遮住，模型就能直接看到答案，那它学不到任何东西 ⇒ 所以必须把「当前位置之后」的全部遮掉</b>。<br>⇒ <b>这是 encoder 的「全看」和 decoder 的「只看左边」之间唯一的差别</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("79:28","So the attention layer here aims at computing embeddings from the input sentence as a function of themselves",166);
  note("⭐ 三处注意力的总表 —— 我认为是全讲最该记住的一张",640,194,"y");
  boxNode(50,226,360,50,"① encoder 自注意力","b");
  boxNode(440,226,360,50,"② decoder masked 自注意力","v");
  boxNode(830,226,360,50,"③ cross-attention","g");
  note("输入表达成自己的函数",230,300,"b");
  note("表达成「已解码的一切」的函数",620,300,"v");
  note("表达成「输入里有什么」的函数",1010,300,"g");
  note("⚠ 三处用的是同一个机制 —— 只有 Q / K / V 各自来自哪里不同",640,350,"r");''',
         "<b>这是讲者对三处注意力的完整总结，而我认为它是全讲最该记住的一张表。</b><br>⭐ 「<b>这个 attention 层在 encoder 里出现、也在 decoder 里出现，但它有好几种用法</b>」:<b>① encoder 里那个，目标是「从输入句子算出嵌入，而这些嵌入是它们自己的函数」;② decoder 里第一个（masked 自注意力）,目标是「把东西表达成到目前为止已经解码出来的一切的函数」;③ 第二个（cross-attention）,把东西表达成「输入里有什么」的函数</b>。<br>⚠ <b>三处用的是完全同一个机制（同一条公式）—— 唯一的差别是 Q、K、V 各自来自哪里</b> ⇒ <b>抓住这一点，这张图就不用背了</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("80:10","So here, given that you are having direct links to different tokens, you do not have this sense of order",166);
  note("⭐ 前面欠的那笔债，在这里点名还了",640,196,"y");
  boxNode(80,228,500,50,"并行处理","g");
  boxNode(700,228,500,50,"知道顺序","y");
  note("所有位置同时算 ⇒ 快",330,302,"g");
  note("但「同时」本身就意味着没有先后",950,302,"y");
  note("⭐ 解法：position encodings —— 把位置信息直接加进表示里",640,348,"y");
  note("⚠ 「今天不讲，但知道就好」—— 这一块留到了 L2",640,386,"r");''',
         "<b>前面欠下的那笔债，讲者在这里点名还了。</b><br>⭐ 「<b>既然你和不同的 token 之间有直接链接，你就没有那种顺序感 —— 因为在 RNN 里你是一次一个地表达东西，所以你有某种词序的感觉；但这里你没有了 ⇒ 这就是为什么你有 position encodings，它们在那儿是为了告知『这个词在序列里的位置』</b>」。<br>⭐ 请看清这个因果：<b>并行处理和「知道顺序」是天然冲突的 —— 如果所有位置同时算，那「同时」本身就意味着没有先后 ⇒ 顺序信息必须被显式地加回去</b>。<br>⚠ 讲者说「<b>今天不讲，但知道就好</b>」—— <b>这一块（含 RoPE）留到了 L2</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("80:40","So we are not going to dig into that today, but I just want to call that out",166);
  says("81:35","And then it goes through a feedforward neural network",192);
  says("82:46","So you have a vector of vocabulary size",218);
  note("⭐ 完整流程走一遍 —— 这正好把本讲前面所有内容串起来",640,250,"y");
  seq(50,282,["分词","input embedding","加位置编码","encoder","decoder","词表大小的向量"],"g",192,48);
  note("⚠ 最后那个向量的形状，和 Word2vec 输出端一模一样 —— 一条线走到这里",640,358,"r");''',
         "<b>讲者完整走了一遍流程，而它正好把本讲前面所有内容串起来。</b><br>⭐ 「<b>为了把一个句子从源语言翻到目标语言：我们首先把文本分词，也就是切成任意的单位；我们要为这些 token 学一个嵌入，这就是 input embedding；然后加上关于位置的某种编码；然后过 encoder</b>」 ⇒ 接着：「<b>一旦你有了输入的这些表示，你就开始翻译 —— 从 BOS token 开始，先用 masked multi-head attention 看已翻译出来的哪些有用，再用 cross-attention 把它表达成输入的函数，然后又一个前馈网络</b>」。<br>⚠ 而最后那一步：「<b>你有一个词表大小的向量</b>」—— <b>和 Word2vec 输出端一模一样，这一讲是一条线走到这里的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("83:16","So I guess I went too fast",166);
  says("83:46","And when you have several heads, what you are doing is you are allowing your model to learn different projections",192);
  note("⭐ 最后一个提问：head 到底是什么？",640,222,"y");
  boxNode(80,254,500,50,"一个 head","y");
  boxNode(700,254,500,50,"多个 head","g");
  note("一组 W_q / W_k / W_v 投影矩阵",330,328,"g");
  note("并行跑好几次，各用各的投影矩阵",950,328,"g");
  note("⚠ 类比：就像卷积里的多个 filter —— 每个学一种「关注的角度」",640,374,"r");''',
         "<b>最后一个提问，而讲者又一次坦白了自己的疏漏：「我想我讲太快了，我把那部分忽略掉了」。</b><br>⭐ 「<b>当你做自注意力计算时，你让 query 和 key 互动，然后取对应的 value；但没有什么能阻止你把这件事做好几次 —— 所以 head 这个词，是给『你用来得到 query、key 和 value 的那些投影矩阵』的名字</b>」 ⇒ <b>接上前面那一镜就全通了：一组 W_q / W_k / W_v 就是一个 head，多头就是有好几组</b>。<br>⚠ 而他给的类比很好用：「<b>如果你有计算机视觉的背景，这类似于在你的卷积里有多个 filter</b>」—— <b>每个 filter 学一种模式（边缘、纹理）,每个 head 学一种「关注的角度」(语法、指代、语义)</b>。", 0)],
       {"h": "⭐ 注意力与 transformer",
        "k": "想法：<b>「出于『模型记不住过去的东西』这个事实，人们试着让某个东西和过去的那个东西之间有更直接的连接 —— 而这就是 attention 背后的想法」; 「如果我能朝输入文本的某个区域瞥一眼，那该多好」（2014 年引入）;「这个概念实际上会是这门课的关键」</b>。<br>transformer：<b>「2017 年由一篇叫《Attention is All You Need》的论文引入 —— 光从标题你就能看出来，作者们想要只依赖那一个部分」; 「摆脱这种顺序处理文本的方式，转而让模型一次性地、直接地与文本的所有部分相连 —— 那个东西叫 self-attention」⇒ 「为了算出 token teddy bear 的表示，我们要一次性地、用直接的链接，看序列里所有其它的 token⋯⋯而它对它所处的那个上下文是独一无二的」</b>。<br>⭐ Q / K / V：<b>「当你想要用别的东西来表达某个东西时，我们用 query、key、value」; 「你拿 query teddy bear，把那个 query 和所有其它的 key 做比较⋯⋯然后给更相似的那些加权，并取它们关联的 value」; 「我们可以把这件事表达成矩阵的形式 —— 而 GPU 爱矩阵」; 「这些量是学出来的」,而「我们实际上要做投影来得到这些量，而这些投影是模型学出来的」</b>。<br>架构与三处注意力：<b>「一个 encoder 在左边，一个 decoder 在右边」;① encoder 自注意力「从输入句子算出嵌入，而这些嵌入是它们自己的函数」;② decoder 的 masked 自注意力「把东西表达成到目前为止已经解码出来的一切的函数」;③ cross-attention —— decoder 那个箭头「确实是 query，而 key 和 value 来自 encoder」</b>;还债：<b>「既然你和不同的 token 之间有直接链接，你就没有那种顺序感 ⇒ 这就是为什么你有 position encodings」</b>;多头：<b>「head 这个词，是给你用来得到 query、key、value 的那些投影矩阵的名字⋯⋯类似于在你的卷积里有多个 filter」</b>。",
        "m": "⭐ 注意力的想法朴素到一句话：<b>既然信息走长路会被挤掉，那就别走长路 ——RNN 像接力棒（远了损耗、要排队）,注意力像直拨电话（距离不重要、能同时拨）;而代价是 n 个位置两两连线 = n² 条</b>。<br>⭐ 「<b>加权</b>」不是「挑一个」,而这个区别<b>是这个机制能被训练出来的前提</b>:<b>「挑一个」离散不可导；「按相似度加权」连续可导 ⇒ 注意力权重才能被学出来</b>。<br>⭐ 而<b>三处注意力用的是完全同一个机制（同一条公式）—— 唯一的差别是 Q、K、V 各自来自哪里</b> ⇒ <b>记法通用：谁在「提问」谁就是 Q，被查询的一方提供 K 和 V</b>。<br>⭐ 为什么必须<b>投影</b>:<b>不投影则 Q 和 K 是同一组向量 ⇒ 每个词和自己的点积最大 ⇒ 每个词主要在关注自己，机制退化</b>。",
        "w": " 自注意力补上了「意义 / 上下文化 / 记远处 / 能并行」,<b>唯独「顺序」是新欠下的债，而且是自找的</b>:<b>并行处理和「知道顺序」天然冲突 —— 所有位置同时算，「同时」本身就意味着没有先后 ⇒ 顺序必须被显式加回去，那就是位置编码（留到 L2）</b>。<br>⚠ 而 <b>masked 的理由很硬</b>:<b>推理时后面的词还不存在；训练时整句真值给定，不遮住模型就直接抄答案 ⇒ 这是 encoder「全看」和 decoder「只看左边」之间唯一的差别</b>。<br>⚠ 另外 key / value <b>不是人为设计的、有明确语义的东西</b>:它们是三个学出来的投影矩阵的输出 —— 讲者特意说那只是「从解释的角度」。",
        "r": "⇒ 「<b>GPU 爱矩阵</b>」这五个字解释了一件更大的事：<b>一个算法能不能赢，不只取决于数学性质，还取决于它和硬件合不合得来 —— 对照 RNN：它天然顺序、天然不能并行，GPU 再多也派不上用场</b>。<br>⇒ 而那条核心公式逐块读就不可怕：<b>QKᵀ 是相似度 · 除以 √d_k 是缩放（维度越高点积越大，不缩放 softmax 会过于尖锐）· softmax 变成和为 1 的权重 · 乘 V 做加权平均</b>。<br>⇒ 另外讲者两次自我克制值得留意：<b>「让一切 —— 我是说让大部分东西 —— 能工作」,以及「从解释的角度」</b>。<br>⇒ 更多（接力棒 / 直拨电话的比喻、不投影会怎样、多头与 filter 的类比、位置编码的预告）见<b>深度笔记</b>。",
        },
       {"t": "架构里三处注意力有什么不同？而「谁是 Q」怎么判断？",
        "o": ["三处用的是三套不同的机制；Q 永远来自 encoder",
              "三处用的是完全同一个机制（同一条公式），唯一差别是 Q/K/V 各自来自哪里：encoder 自注意力（输入表达成自己的函数）、decoder masked 自注意力（表达成已解码一切的函数）、cross-attention（表达成输入的函数）；而判断很通用 —— 谁在「提问」谁就是 Q，被查询的一方提供 K 和 V",
              "三处差在层数；Q 永远来自 decoder",
              "三处差在 head 数；Q 由位置编码决定"],
        "a": 1,
        "w": "⇒ 而自注意力补上了「意义 / 上下文化 / 记远处 / 能并行」，唯独「顺序」是新欠的债 —— 因为并行处理和「知道顺序」天然冲突，所以要用位置编码显式加回去。"})
