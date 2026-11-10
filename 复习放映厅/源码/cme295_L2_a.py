# -*- coding: utf-8 -*-
"""CME295 L2 模块 a —— 字幕第 1–82 句（00:12–09:06）：两条后勤、L1 回顾（自注意力与
硬件）、⭐ attention map 把「多头到底学到了什么」变成了证据，以及一条读论文的建议。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（18 镜 → 10 镜）。
   被砍掉的延伸分析在「CME295讲座L2-深度笔记」里。
"""


def add(KP):

    KP("⭐ L1 回顾，与 attention map",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("00:12","So before we start, I wanted to give you a heads up about two logistical things",166);
  says("00:50","Point number 2 is about the final exam",192);
  note("⭐ 两条后勤，而它们旁证了一件值得知道的事",640,222,"y");
  boxNode(80,254,500,50,"① 换了录音设备","g");
  boxNode(700,254,500,50,"② 期末考日期待定","y");
  note("「我们回看了第 1 讲的录像，没法不注意到音频是不理想的」",330,328,"g");
  note("「占位日期是 12 月 10 日⋯⋯我们在看能不能挪早一点」",950,328,"y");
  note("⚠ 这门课是「正在进行时」录下来的 —— 不是事后剪辑的精品课",640,374,"r");''',
         "<b>开场是两条后勤，而它们旁证了一件对你有用的事。</b><br>⭐ 第一条：<b>「我和 Shervine 一起回看了第 1 讲的录像，而我们没法不注意到音频是不理想的 —— 所以这一讲我们换了另一套设备」</b>（新设备带来的新问题是他的声音传不开，于是他当场问了「后排能听清吗」）。第二条是<b>期末考日期还待定</b>。<br>⚠ 为什么留一镜给它们：<b>它说明这门课是「正在进行时」录下来的 —— 不是事后剪辑的精品课程，而是一个学期里真实发生的九次课</b> ⇒ <b>这解释了这门课的很多特点：问答没有被剪掉、讲者会当场改口、时间不够时他会说出来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("01:14","So with that aside, let us go into",166);
  says("01:38","what self-attention is that each token is attending to all other tokens in the sequence",192);
  note("⭐ 「像往常一样」—— 每一讲开头都有一份前情提要",640,222,"y");
  boxNode(140,254,1000,50,"自注意力：每个 token 都去关注序列里所有其它的 token","y");
  note("两个词值得留意：「通过注意力这个机制」（关注是算出来的）· 「所有其它」",640,330,"g");
  note("⚠ 而这个固定环节有实际价值：跳着看某一讲的成本比你想的低",640,374,"r");''',
         "<b>过渡只有一句，但「像往常一样」这四个字说明这是个固定环节。</b><br>⭐ 「<b>在那之前，像往常一样，我们要做的是快速回顾一下前几集看过的东西</b>」 ⇒ <b>每一讲的开头都有一份前情提要 —— 所以如果你想跳着看某一讲，成本比想象中低：讲者会先把你需要的前置知识复述一遍</b>（L5 开场回顾 L4、L6 开场回顾 L5，都是这样）。<br>⭐ 而 L1 的核心一句话复述完：「<b>第 1 讲讲的全是引入自注意力这个概念。而自注意力是什么？就是每个 token 都通过注意力这个机制，去关注序列里所有其它的 token —— 所以你有 queries、keys、values 这些记号</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("02:09","So we saw that the self-attention mechanism can be expressed with this formula",166);
  says("02:41","These are big matrix multiplications, or hardware, is very capable of doing",192);
  setEq("$$\\mathrm{softmax}\\!\\left(\\frac{QK^{\\top}}{\\sqrt{d_k}}\\right)V$$","top");
  note("⭐ 「而只要知道一点：这条公式是被高度优化过的」",640,322,"y");
  note("⚠ 一条公式好不好，不只看数学优雅，还看它能不能被现有硬件高效执行",640,362,"r");''',
         "<b>那条公式又出现了，而讲者这次补了一句 L1 里只是一带而过的话。</b><br>⭐ 「<b>我希望这条公式对你们来说已经熟悉了。而只要知道一点：这条公式是被高度优化过的 —— 这些是大的矩阵乘法，而我们的硬件非常有能力做这件事</b>」。<br>⭐ 把它和 L1 里那句「<b>GPU 爱矩阵</b>」接起来，一条完整的论证就出来了：<b>① 自注意力可以写成矩阵形式（这是 Q/K/V 这种表达方式给的）;② 矩阵乘法正是 GPU 的强项；③ ⇒ 所以它不只是「数学上说得通」,它是「在现有硬件上跑得飞快」</b>。<br>⚠ <b>而这正是 RNN 输掉的另一半原因：它天然顺序，GPU 再多也排不上用场</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("03:12","And the transformer was initially introduced in the context of machine translation",166);
  note("⭐ 架构为什么是两半的 —— 答案在它的出身里",640,196,"y");
  boxNode(140,228,440,50,"encoder（左）：源语言","b");
  boxNode(680,228,460,50,"decoder（右）：目标语言","g");
  note("「transformer 最初是在机器翻译这个语境里被引入的」",640,304,"y");
  note("⭐ 翻译天生有两半：一段给定的输入，一段要生成的输出",640,344,"g");
  note("⚠ 记住这一点 —— 下半场讲「为什么今天几乎都是 decoder-only」时要用到",640,384,"r");''',
         "<b>架构的回顾，而讲者点出了一件解释力很强的事：它的出身。</b><br>⭐ 「<b>transformer 由两个主要部分组成：左边的 encoder 和右边的 decoder。而 transformer 最初是在机器翻译这个语境里被引入的 —— 所以你可以把左边想成处理源语言的输入文本，而右边负责把译文解码成目标语言</b>」。<br>⭐ 「<b>最初是在机器翻译的语境里</b>」这一句解释了原始架构为什么是两半的：<b>翻译这个任务天生就有两段 —— 一段是给定的输入，一段是要生成的输出</b>。<br>⚠ <b>请记住这一点：这一讲下半场会讲「三类架构」,而「为什么今天几乎都是 decoder-only」的答案，正是从「不是所有任务都长这样」开始的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("03:43","it is called multi-head attention layer",166);
  says("04:13","And you can think of each head as an opportunity for the model to learn one way of projecting",192);
  note("⭐ 讲者特意回头处理 L1 遗留的那个问题：head 到底是什么",640,222,"y");
  boxNode(140,254,1000,50,"一个 head = 模型学会「某一种投影方式」的一次机会","y");
  note("「这些小方块的个数，基本上就是 head 的数量」",640,330,"g");
  note("⚠ 「一次机会」这个词很准：不是「每个头会学到不同的东西」,而是「它有机会」",640,374,"r");''',
         "<b>讲者特意回头处理了 L1 遗留的一个问题，而他的措辞比 L1 更准。</b><br>⭐ 「<b>我记得当时关于这个有很多问题 —— 它叫 multi-head attention 层，所以有好几个 head，那对应的是什么？</b>」 ⇒ 他的定义是：「<b>你可以把每一个 head 想成：模型学会『把输入投影成一个 query、一个 key、或一个 value』的某一种方式的一次机会</b>」。<br>⚠ 请留意「<b>一次机会（an opportunity）</b>」这个词选得有多准：<b>它不是说「每个头会学到不同的东西」,而是说「它有机会学到不同的东西」—— 这和 L1 里那个「什么都没有约束它们不一样」是同一个分寸</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("04:43","which is a way to interpret what each of these heads do",166);
  says("05:14","what we are interested in is to see which other token is being most similar to token its",192);
  note("⭐ 工具登场：attention map",640,222,"y");
  boxNode(80,254,500,50,"它画的是什么","g");
  boxNode(700,254,500,50,"例子挑得很巧","y");
  note("QKᵀ 那个 n×n 矩阵里的某一行",330,328,"g");
  note("代词消解：「its」到底指谁",950,328,"y");
  note("⚠ 「一种去解释的方式」—— 他没说「这张图显示了模型在想什么」",640,374,"r");''',
         "<b>回答「多头各自在学什么」的工具登场了，而讲者的用词分寸值得注意。</b><br>⭐ 「<b>我们有一个概念叫 attention map，它基本上试图把这些 query 的点积的值表示出来</b>」 ⇒ 对上 L1 的形状：<b>这就是 QKᵀ 那个 n×n 矩阵里的某一行 —— 第 j 个数就是「这个 query 对第 j 个 token 的注意力」</b>。<br>⭐ 例子挑得很巧：<b>「我们感兴趣的是看其它哪个 token 和 token『its』最相似」—— 这是一个代词消解问题，而人类读者一眼就知道答案</b>。<br>⚠ 他说的是「<b>一种去解释…的方式</b>」,不是「这张图显示了模型在想什么」—— <b>这个分寸贯穿整段</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("05:47","you have these two words, so application and law, which are highlighted",166);
  note("⭐ 结果确实对上了人的直觉",640,196,"y");
  boxNode(140,228,1000,50,"its  ⟶  高注意力落在 law 和 application 上","g");
  note("而 token「its」指的就是 law —— 它和 application 是关联的",640,304,"y");
  note("⭐ 这是一个可检验的结果：有标准答案，而模型给的权重和它对上了",640,344,"y");
  note("⚠ 但也别过度解读 —— 这是一个被挑出来展示的例子，不是统计结论",640,384,"r");''',
         "<b>结果出来了，而它确实对上了人的直觉。</b><br>⭐ 「<b>你有这两个词 —— application 和 law —— 被高亮为具有高注意力权重；而这里的注意力权重，就是 its 这个 query 和每个 token 的 key 的点积</b>」 ⇒ 而这<b>说得通，因为 token「its」指的就是 law</b>。<br>⭐ 这个例子之所以有说服力，是因为它<b>可检验</b>:<b>代词指谁有标准答案，而模型算出来的权重和那个答案对上了 ⇒ 这不是「看图说话」,是一次对照</b>。<br>⚠ 不过也别过度解读：<b>它是一个被论文挑出来展示的例子，不是在整个数据集上的统计结论</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("06:52","these are the intensity for heads, for let us say the first heads",166);
  note("⭐ 整段的落点 —— 也是 L1 那个追问的答案",640,196,"y");
  boxNode(80,228,500,50,"第一个 head","y");
  boxNode(700,228,500,50,"第二个 head","v");
  note("对某些词强度高",330,302,"y");
  note("对 law 的强度非常高",950,302,"v");
  note("⭐ 「长话短说：这些 head 可能学到了不同的、去判断哪些词要紧的方式」",640,348,"y");
  note("⚠ 注意是「可能（may）」—— 证据形式的答案，但依然带着限定词",640,386,"r");''',
         "<b>这是整段的落点，也是 L1 里那个追问的答案。</b><br>⭐ 「<b>作者选择做的事，是把这些值作为『不同的 head』的函数展示出来 —— 比如左边这些是第一个 head 的强度，而第二个 head 显示出对 law 的强度非常高 ⇒ 长话短说：这些 head 可能学到了不同的、去判断哪些词要紧的方式</b>」。<br>⭐ 回想 L1：<b>当时学生问「各个头会不会学成一样」,Shervine 的回答是「什么都没约束它们，但梯度下降没有动机去复制」—— 那是一个激励论证；而这里给的是证据：你真的能看到不同的头亮在不同的词上</b>。<br>⚠ 但他仍然说「<b>可能</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("07:30","So the question is, when we are doing all these computations, are they going through different MLPs",166);
  says("08:01","So each head is going to have one result here, that is then going to be concatenated",192);
  note("⭐ 一个实现细节的提问，而回答顺带纠了一个用词",640,222,"y");
  boxNode(80,254,500,50,"学生说：不同的 MLP？","b");
  boxNode(700,254,500,50,"讲者：不同的「投影矩阵」","g");
  note("MLP 意味着多层 + 非线性",330,328,"b");
  note("W_q / W_k / W_v 只是一次线性变换",950,328,"g");
  note("⚠ 流程照旧：每个 head 一个结果 ⟶ 拼接 ⟶ 再被输出矩阵 W_o 投影一次",640,374,"r");''',
         "<b>这个提问问的是实现细节，而讲者的回答顺带纠了一个用词。</b><br>⭐ 学生问「<b>这些计算是过不同的 MLP 吗</b>」,而他答的是「<b>我们会为它们每一个都有不同的投影矩阵⋯⋯每个 head 都会有它自己的投影，而这些计算是并行发生的</b>」 ⇒ <b>留意他用的是「投影矩阵」而不是「MLP」:MLP 意味着多层加非线性，而 W_q / W_k / W_v 只是一次线性变换 —— 一字之差，复杂度差很远</b>。<br>⭐ 而流程和 L1 的走查完全吻合：「<b>每个 head 在这里会有一个结果，然后它会被拼接起来，再被输出矩阵投影一次 —— 长话短说，它是高度并行化的</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("08:32","Any other questions on this?",166);
  says("09:06","I highly recommend that you read the transformers paper",192);
  note("⭐ 收尾，以及一条时机选得很好的读论文建议",640,222,"y");
  boxNode(140,254,1000,50,"《Attention is All You Need》——「非常密，只有几页长」","y");
  note("⭐ 短和密是同一件事：每一句都压缩得很狠，省略的全靠你自己补",640,330,"y");
  note("⚠ 而现在是读它最好的时机 —— 你刚把被省略的那些补齐了",640,374,"r");''',
         "<b>回顾结束，讲者给了一条读论文的建议，而这条建议的时机选得很好。</b><br>⭐ 「<b>我强烈建议你去读 transformer 那篇论文，也就是《Attention is All You Need》。它是一篇非常密的论文，只有几页长 —— 但我希望，你在第 1 讲看到的那些东西，能让你以一种对你说得通的方式去消化它的内容</b>」。<br>⭐ 「<b>非常密，只有几页长</b>」这两个描述放在一起说，其实是同一件事：<b>短，是因为每一句都压缩得很狠，而被省略的那些全靠读者自己补</b> ⇒ <b>而你刚在 L1 把那些补齐了，所以现在正是读它的时机</b>。<br>⚠ 另外请留意「<b>一种方式</b>」这个词在这一段里出现了三次 —— <b>讲者始终没有说「这就是多头的工作原理」</b>。", 0)],
       {"h": "⭐ L1 回顾与 attention map",
        "k": "两条后勤：<b>「我和 Shervine 一起回看了第 1 讲的录像，而我们没法不注意到音频是不理想的 —— 所以这一讲我们换了另一套设备」; 期末考「有一个占位日期⋯⋯我们在看有没有办法把它挪到那一周更早一些」</b>。<br>L1 回顾：<b>「第 1 讲讲的全是引入自注意力这个概念 —— 每个 token 都通过注意力这个机制，去关注序列里所有其它的 token」; 「自注意力机制可以用这条公式表达⋯⋯而只要知道一点：这条公式是被高度优化过的 —— 这些是大的矩阵乘法，而我们的硬件非常有能力做这件事」; 「transformer 由两个主要部分组成：左边的 encoder 和右边的 decoder。而 transformer 最初是在机器翻译这个语境里被引入的」</b>。<br>⭐ 多头与 attention map：<b>「你可以把每一个 head 想成：模型学会把输入投影成一个 query、一个 key、或一个 value 的某一种方式的一次机会」; 「我们有一个概念叫 attention map，它基本上试图把这些 query 的点积的值表示出来」—— 例子是看「其它哪个 token 和 token『its』最相似」,结果是「application 和 law 被高亮」,而「token its 指的就是 law」⇒ 「作者把这些值作为不同 head 的函数展示出来⋯⋯长话短说：这些 head 可能学到了不同的、去判断哪些词要紧的方式」</b>;一个提问：<b>「这些计算是过不同的 MLP 吗」——「我们会为它们每一个都有不同的投影矩阵⋯⋯而这些计算是并行发生的」</b>⇒ 建议：<b>「我强烈建议你去读 transformer 那篇论文⋯⋯它是一篇非常密的论文，只有几页长」</b>。",
        "m": "⭐ <b>attention map 把 L1 那个追问变成了证据</b>:<b>L1 里「各个头会不会学成一样」的回答是「什么都没约束，但梯度下降没有动机去复制」（激励论证）;而这里你真的能看到不同的头亮在不同的词上</b> —— 不过他仍然说「<b>可能</b>」。<br>⭐ 而「<b>这条公式是被高度优化过的</b>」接上 L1 那句「GPU 爱矩阵」,论证就完整了：<b>① 自注意力能写成矩阵形式；② 矩阵乘法正是 GPU 的强项 ⇒ 它不只是数学上说得通，而是在现有硬件上跑得飞快 —— 这正是 RNN 输掉的另一半</b>。<br>⭐ 而「<b>最初是在机器翻译的语境里</b>」解释了原始架构为什么是两半的：<b>翻译天生有两段 —— 一段给定的输入，一段要生成的输出</b>。",
        "w": " 「<b>一次机会（an opportunity）</b>」这个词选得很准：<b>不是「每个头会学到不同的东西」,而是「它有机会学到」—— 和 L1 那个分寸一致</b>;而「一种方式」在这一段里出现了三次，<b>讲者始终没有说「这就是多头的工作原理」</b>。<br>⚠ 另外那个 attention map 的例子<b>是被挑出来展示的</b>,不是在整个数据集上的统计结论。<br>⚠ 用词也要分清：<b>「投影矩阵」不是「MLP」——MLP 意味着多层加非线性，而 W_q / W_k / W_v 只是一次线性变换</b>。",
        "r": "⇒ 「<b>像往常一样</b>」说明前情提要是固定环节：<b>所以跳着看某一讲的成本比想象中低 —— 讲者会先把你需要的前置知识复述一遍</b>。<br>⇒ 而「transformer 出身于机器翻译」这一点<b>下半场要用</b>:「为什么今天几乎都是 decoder-only」的答案，正是从「不是所有任务都长这样」开始的。<br>⇒ 读论文的时机也值得照做：<b>「非常密，只有几页长」是同一件事 —— 短是因为每句都压缩得很狠，而你刚把被省略的补齐了</b>。<br>⇒ 更多（录音设备与课程的「正在进行时」、attention map 的解读限度、MLP 与线性投影的区别）见<b>深度笔记</b>。",
        },
       {"t": "attention map 回答了 L1 留下的什么问题？它给的是什么形式的答案？",
        "o": ["回答了「位置编码怎么加」；给的是公式推导",
              "回答了「多个 head 到底学到了不同的东西吗」——L1 里只能给「梯度下降没有动机去复制」这种激励论证，而这里给的是证据：把注意力权重按 head 画出来，能看到不同的头亮在不同的词上（但讲者仍然说「可能」）",
              "回答了「为什么要除以 √d_k」；给的是实验曲线",
              "回答了「decoder 为什么要 mask」；给的是反例"],
        "a": 1,
        "w": "⇒ 而那个例子之所以有说服力，是因为它可检验：代词 its 指谁有标准答案，而模型算出来的高权重正好落在 law 和 application 上。"})
