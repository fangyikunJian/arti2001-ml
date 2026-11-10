# -*- coding: utf-8 -*-
"""CME295 L2 模块 i —— 字幕第 611–708 句（71:45–82:11）：BERT 开讲 ——
名字拆解（Bidirectional / Encoder / Representations / Transformers）、ELMo 那段八卦、
CLS 与 SEP、多阶段训练（预训练 MLM+NSP → 微调），以及这套方法的好处与坏处。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（28 镜 → 12 镜）。
⚠ 旁白里不许出现半角双引号；setEq 里反斜杠写双份。
"""


def add(KP):

    KP("⭐ BERT 这个名字拆开来",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("71:52","BERT, it is an acronym that denotes Bidirectional Encoder Representations from Transformers",166);
  says("72:15","we just dropped the decoder. So this encoder from transformer is basically exactly what it means",192);
  note("⭐ 用名字本身当大纲 —— 而这个名字恰好把设计全写进去了",640,222,"y");
  boxNode(60,254,280,50,"Bidirectional","y");
  boxNode(360,254,280,50,"Encoder","g");
  boxNode(660,254,280,50,"Representations","b");
  boxNode(960,254,280,50,"Transformers","v");
  note("⇒ Encoder 这一半 BERT 什么都没改：就是把 decoder 扔了",640,330,"g");
  note("⚠ 所以 BERT 的全部创新都在「怎么训」那一侧，不在结构上",640,374,"r");''',
         "<b>BERT 开讲，而讲者选了一个很好的大纲：名字本身。</b><br>⭐ 「<b>首先我们要从「BERT 是什么意思」开始看。BERT 是一个缩写，表示 Bidirectional Encoder Representations from Transformers。而我们要一起看这个缩写的每一部分各自对应什么</b>」 ⇒ <b>用名字当大纲是个好办法，而这个名字恰好把设计全写进去了：双向 · 只要 encoder · 产出表示 · 基于 transformer</b>。<br>⭐ 先从最容易的那个词开始：「<b>我们就从 encoder 那部分开始，它是最容易把握的。就像我们说的，我们就是把 decoder 扔了。所以这个「来自 transformer 的 encoder」基本上就是它字面上的意思</b>」 ⇒ <b>BERT 在结构上什么都没改，它的全部创新都在「怎么训」那一侧</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("72:39","we are able from a given input to get output representations that have attended to everything",166);
  says("73:07","the mask is making the attention mechanism causal",192);
  note("⭐⭐ 这就是双向的全部内容，而对照项是「因果」",640,222,"y");
  boxNode(80,254,500,50,"BERT：每个 token 关注过一切","g");
  boxNode(700,254,500,50,"decoder：只能关注自己和之前","r");
  note("⇒ 没有掩码 ⇒ 真正的双向",330,328,"g");
  note("⇒ 有掩码 ⇒ 注意力变成因果的",950,328,"r");
  note("⚠ causal 这个词是借来的：它说的是「结果不能影响原因」—— 未来不能影响现在",640,374,"v");''',
         "<b>这就是双向的全部内容，而讲者选的对照项很有意思。</b><br>⭐ 「<b>这篇论文的结果是了不起的，因为我们能够从一个给定的输入，得到那种「每一个 token 都关注过一切」的输出表示。而这确实是这样的，因为既然我们只有 encoder，我们就有这个真正的双向性</b>」。<br>⭐ 对照是：「<b>这和你有的那种带掩码的自注意力形成对比 —— 那个掩码是让注意力机制变成因果的，所以每个 token 都能关注它自己、以及它之前的那些 token</b>」 ⇒ <b>「因果（causal）」这个词是从物理和统计里借来的：它说的是「结果不能影响原因」—— 在序列里就是「未来不能影响现在」。而 BERT 不做生成，所以它可以把这个限制整个去掉</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("73:25","saying that GPT came out, GPT they are not truly bidirectional",166);
  says("73:56","the mask is exactly there to prevent links from tokens to those that come after them",192);
  note("⭐⭐ 那个 truly 终于点名了 —— 这是一场同期的路线之争",640,222,"y");
  boxNode(80,254,500,50,"2018 年 6 月：GPT-1","b");
  boxNode(700,254,500,50,"2018 年 10 月：BERT","g");
  note("单向、能生成",330,328,"b");
  note("双向、不能生成",950,328,"g");
  note("⚠ 而这场争论的赢家在当时很清楚（BERT 刷榜）,在今天完全反过来了",640,374,"r");''',
         "<b>那个 truly 终于点名了，而这是一场同期的路线之争。</b><br>⭐ 「<b>这也是作者在论文里讨论了很多的一件事 —— 他们说 GPT 出来了，而 GPT 它们不是真正双向的。而这些能被用于分类任务的编码，它们真的是双向的</b>」 ⇒ <b>时间线很紧：GPT-1 是 2018 年 6 月，BERT 是同年 10 月 —— 两条路线几乎同时出手，而当时的赢家很清楚（BERT 在十一个任务上刷新了纪录）; 但今天完全反过来了</b>。<br>⭐ 而学生确认了一次掩码的作用，讲者的措辞很干净：「<b>那个掩码就恰恰是在那里，用来阻止从一个 token 到它后面那些 token 的链接</b>」 ⇒ <b>「阻止链接」比「加负无穷」更准确地说出了它在做什么</b>。", 0)],
       {"h": "⭐ BERT 这个名字",
        "k": "<b>「所以首先我们要从「BERT 是什么意思」开始看。所以 BERT，它是一个缩写，表示 Bidirectional Encoder Representations from Transformers。而我们要一起看这个缩写的每一部分各自对应什么」; 「那么我们就从 encoder 那部分开始，它是最容易把握的。所以就像我们说的，我们就是把 decoder 扔了。所以这个「来自 transformer 的 encoder」基本上就是它字面上的意思」</b>。<br>⭐ 双向：<b>「这篇论文的结果是了不起的，因为我们能够从一个给定的输入，得到那种「每一个 token 都关注过一切」的输出表示。而这确实是这样的，因为既然我们只有 encoder，我们就有这个真正的双向性」; 「而这和你有的那种带掩码的自注意力形成对比 —— 那个掩码是让注意力机制变成因果的。所以每个 token 都能关注它自己、以及它之前的那些 token」; 「他们说 GPT 出来了，而 GPT 它们不是真正双向的。而这些能被用于分类任务的编码，它们真的是双向的」; 「而那个掩码就恰恰是在那里，用来阻止从一个 token 到它后面那些 token 的链接」</b>。",
        "m": "⭐ 名字当大纲是个好办法，而这个名字把设计全写进去了：<b>Bidirectional（双向）· Encoder（只要 encoder）· Representations（产出表示而不是文本）· Transformers（底座）</b>。<br>⭐ 而 <b>BERT 在结构上什么都没改</b>:<b>它就是 transformer 的 encoder 堆叠 ⇒ 全部创新都在「怎么训」那一侧（MLM + NSP + 微调）</b>。<br>⭐⭐ 「<b>因果（causal）</b>」这个词是从物理和统计里借来的：<b>它说的是「结果不能影响原因」—— 在序列里就是「未来不能影响现在」; 而 BERT 不做生成，所以可以把这个限制整个去掉</b>。",
        "w": " 这是一场同期的路线之争，时间线很紧：<b>GPT-1 是 2018 年 6 月、BERT 是同年 10 月 —— 当时的赢家很清楚（BERT 在十一个任务上刷新纪录）,而今天完全反过来了</b>。<br>⚠ 而「<b>阻止链接</b>」这个说法比「加负无穷」更准确地说出了掩码在做什么：<b>它改的是图的连通性，而不只是一个数值技巧</b>。",
        "r": "⇒ 那个 <b>truly</b> 值得记住：<b>它是一个有针对性的词 —— 论文作者在用它区分自己和 GPT，而这类措辞在论文里通常都指向一场正在进行的争论</b>。<br>⇒ 更多（GPT-1 与 BERT 的指标对照、双向性在分类任务上的具体优势）见<b>深度笔记</b>。",
        },
       {"t": "BERT 的「真正双向」具体指什么？它和 decoder 的差别在哪里？",
        "o": ["指它同时从左到右和从右到左各跑一遍，然后把两个结果拼起来",
              "指它没有因果掩码 ⇒ 每个 token 都关注过一切（左边和右边都在）; 而 decoder 的掩码让注意力变成「因果的」,每个 token 只能关注自己和之前的 —— BERT 不做生成，所以可以把这个限制整个去掉",
              "指它的位置编码是双向对称的",
              "指它既能做分类又能做生成"],
        "a": 1,
        "w": "⇒ 而这是一场同期的路线之争：GPT-1 是 2018 年 6 月、BERT 是同年 10 月，当时 BERT 赢了，今天反过来了。"})

    KP("⭐ ELMo 那段八卦，与一个第三次出现的理由",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("74:21","you had another landmark paper that same year, which was called ELMo",166);
  says("74:52","it was based on a bidirectional LSTM where you had multiple layers",192);
  note("⭐ 同一年的另一篇里程碑，而讲者对它带着一点惋惜",640,222,"y");
  boxNode(80,254,500,50,"ELMo ＝ Embeddings from Language Models","b");
  boxNode(700,254,500,50,"做法：多层双向 LSTM","v");
  note("⇒ 讲者：那篇论文的时机有点不幸",330,328,"b");
  note("⚠ 它的「双向」和 BERT 的不是同一种东西",950,328,"r");
  note("⭐ 两个方向各跑一遍再拼起来 ≠ 每个位置同时看到两边",640,374,"g");''',
         "<b>讲者把 BERT 放进语境，而他对 ELMo 的评价带着一点惋惜。</b><br>⭐ 「<b>当时 NLP 这个领域正在爆发。所以同一年你还有另一篇里程碑论文，它叫 ELMo —— 也就是 Embeddings from Language Models。而我会说那篇论文的时机有点不幸</b>」; 做法是：「<b>它基于一个双向 LSTM，你有多个层，一层堆在另一层上面。而多亏这个架构，你能够为每一个词构建一个双向的表示</b>」。<br>⭐⭐ 但两种「双向」不是同一种东西：<b>ELMo 是两个单向 LSTM 各跑一遍再把结果拼起来 —— 每个方向内部仍然只看一边；而 BERT 的每个位置在每一层都同时看到两边。前者是「拼接的双向」,后者是「融合的双向」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("75:22","It is because you had the same downsides as the previous models",166);
  says("75:36","because they are characters in Sesame Street",192);
  says("75:58","They try to fit their acronyms into themes",218);
  note("⭐⭐⭐ 这是这门课第三次用同一个理由解释一个历史结果",640,250,"y");
  boxNode(80,282,500,50,"因为那个递推，它很难 scale","r");
  boxNode(700,282,500,50,"⇒ RNN 输了、ELMo 输了","r");
  note("⭐ 而那两个名字是《芝麻街》的角色 —— 研究者挺爱玩，缩写往往就是方法的摘要",640,358,"g");''',
         "<b>这就是答案，而它又一次回到了那条贯穿全课的线。</b><br>⭐ 「<b>那么为什么它没有变得像 BERT 那样流行？是因为你有和之前那些模型一样的缺点 —— 基本上，因为这个递推，它很难 scale</b>」 ⇒ <b>这是这门课第三次用同一个理由解释一个历史结果：RNN 输给 transformer 是因为它、ELMo 输给 BERT 是因为它，而 L1 里 word2vec 之后的那一段也是它</b>。<br>⭐ 然后是最轻松的一段：「<b>你们很多人想到 ELMo 和 BERT 时，第一反应不是这两篇论文 —— 因为它们是《芝麻街》里的角色⋯⋯而研究者们普遍挺爱玩的，他们会试着把自己的缩写套进某些主题里</b>」 ⇒ <b>而这件事的实用面是：一个好的缩写往往就是方法的摘要</b>。", 0)],
       {"h": "⭐ ELMo 与那个第三次的理由",
        "k": "<b>「所以我只想把这篇论文放进语境里。而当时 NLP 这个领域正在爆发。所以同一年你还有另一篇里程碑论文，它叫 ELMo —— 也就是 Embeddings from Language Models。而我会说那篇论文的时机有点不幸」; 「所以 ELMo —— 就给个大概的脉络 —— 它基于一个双向 LSTM，你有多个层，一层堆在另一层上面。而基本上，多亏了这个架构，你能够为每一个词构建一个双向的表示」; 「那么为什么它没有变得像 BERT 那样流行？是因为你有和之前那些模型一样的缺点 —— 基本上，因为这个递推，它很难 scale」</b>。<br>⭐ 那段八卦：<b>「而我想你们很多人想到 ELMo 和 BERT 时，第一反应不是这两篇论文 —— 因为它们是《芝麻街》里的角色」; 「而研究者们，他们普遍挺爱玩的。他们会试着把自己的缩写套进某些主题里。所以如果你去看论文的名字，你会被娱乐到」</b>。",
        "m": "⭐⭐ 两种「双向」不是同一种东西：<b>ELMo 是两个单向 LSTM 各跑一遍再把结果拼起来（每个方向内部仍只看一边）; 而 BERT 的每个位置在每一层都同时看到两边 ⇒ 前者是「拼接的双向」,后者是「融合的双向」</b>。<br>⭐⭐⭐ 而这门课第三次用同一个理由解释历史结果：<b>「因为这个递推，它很难 scale」——RNN 输给 transformer、ELMo 输给 BERT、L1 里那一段也是它 ⇒ 可并行性是这个领域里最硬的那条约束</b>。",
        "w": " 「时机有点不幸」这个评价要公允地读：<b>ELMo 不是方法不好，它是在同一年遇到了一个可并行的对手 —— 而在那之后，所有基于递推的路线都很难再被投入资源</b>。<br>⚠ 而缩写的实用面：<b>ALBERT（A Lite BERT）· RoBERTa（Robustly optimized BERT approach）· DistilBERT（蒸馏）—— 名字本身就是方法的摘要，看名字能省很多时间</b>。",
        "r": "⇒ 「可并行性」这条线值得单独记住：<b>它解释了 L1 的 RNN→transformer、L2 的 ELMo→BERT、以及后面 decoder-only 赢在「最容易扩大规模」—— 同一条约束在三个不同的地方给出了同一个答案</b>。<br>⇒ 更多（ELMo 的具体做法、拼接式双向的局限、《芝麻街》那串论文名）见<b>深度笔记</b>。",
        },
       {"t": "ELMo 为什么没有像 BERT 那样流行？",
        "o": ["因为它的「双向」是两个单向 LSTM 拼起来的，而 BERT 是融合的",
              "因为它没有开源，社区用不上",
              "因为它基于递推（LSTM）——讲者的原话是「因为这个递推，它很难 scale」; 而这是这门课第三次用同一个理由解释历史结果：RNN 输给 transformer、ELMo 输给 BERT，都是因为可并行性",
              "因为它的名字取自《芝麻街》,不够严肃"],
        "a": 2,
        "w": "⇒ 它的「双向」确实也和 BERT 不同（拼接 vs 融合），但讲者给出的理由是 scale —— 而「时机有点不幸」说的是它遇到了一个可并行的对手。"})

    KP("⭐ CLS 和 SEP：两个「结构性」的 token",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("76:23","the goal here is to perform tasks that might be focused on projecting some representation somewhere",166);
  says("76:46","So you have first the CLS token, which stands for classification",192);
  note("⭐⭐ BERT 最聪明的那个设计，而关键在「占位」这个词",640,222,"y");
  boxNode(80,254,500,50,"CLS 放在序列最开头","y");
  boxNode(700,254,500,50,"⇒ 走完整个 encoder 后被投影成分类用的向量","g");
  note("它自己不代表任何词",330,328,"y");
  note("⇒ 所以它可以专职代表「整句」",950,328,"g");
  note("⚠ 妙处在于：不用改架构，就给模型加了一个「句子级」的出口",640,374,"r");''',
         "<b>这一镜引出两个特殊的 token，而「结构性」这个词选得很好。</b><br>⭐ 「<b>这里的目标是去做那些可能聚焦在「把某个表示投影到某处」的任务，所以典型就是分类任务</b>」; 而第一个是：「<b>你首先有 CLS token，它代表 classification。它基本上是一个占位 token，被放在序列的开头 —— 它接着会在走完整个注意力、投影、以及整个 encoder 机制之后，被投影成一个我们可以用来做分类的东西</b>」。<br>⭐⭐ 关键在「<b>占位</b>」:<b>CLS 自己不代表任何词，所以它可以专职去代表「整句」。而妙处在于不用改架构 —— 只是在输入前面多塞一个 token，就给模型加了一个「句子级」的出口</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("77:13","CLS is just some kind of placeholder that will carry the bidirectional information of your whole input",166);
  says("77:36","It aims at separating two sentences",192);
  note("⭐⭐⭐ 这句总结里藏着一个很关键的依赖关系",640,222,"y");
  boxNode(80,254,500,50,"CLS 在开头，却要携带整个输入的信息","y");
  boxNode(700,254,500,50,"⇒ 这只有在双向注意力下才可能","g");
  note("⚠ 若有因果掩码，开头那个 token 只能看到自己",330,328,"r");
  note("⇒ 所以 CLS 这个设计和「双向」是绑死的",950,328,"g");
  note("⭐ 而 SEP 的存在本身就透露了训练任务：BERT 的输入可以是「两个句子」",640,374,"v");''',
         "<b>这句总结里藏着一个很关键的依赖关系。</b><br>⭐ 「<b>CLS 只是某种占位符，它会携带你整个输入的双向信息</b>」 ⇒ <b>请想清楚：CLS 放在序列的开头，而它要携带整个输入的信息 —— 这只有在双向注意力下才可能。如果有因果掩码，开头那个 token 只能看到自己，什么也携带不了。所以 CLS 这个设计和「双向」是绑死的，它不是一个可以搬到 GPT 上去的小技巧</b>。<br>⭐ 第二个结构性 token：「<b>另一个可能有用去看的 token 是这个 SEP token —— 它就像 separator（分隔符）。它的目标是分开两个句子</b>」 ⇒ <b>而它的存在本身就透露了训练任务：BERT 的输入可以是「两个句子」, 而那正是 NSP</b>。", 0)],
       {"h": "⭐ CLS 与 SEP",
        "k": "<b>「那么为了更深入地讲我提到的 encoder-only 模型的目标 —— 你有你那一串 token 作为输入。而这里的目标是去做那些可能聚焦在「把某个表示投影到某处」的任务，所以典型就是分类任务」; 「所以你首先有 CLS token，它代表 classification。而它基本上是一个占位 token，被放在序列的开头 —— 它接着会在走完整个注意力、然后投影、以及整个 encoder 机制之后，被投影成一个我们可以用来做分类的东西」; 「所以 CLS 只是某种占位符，它会携带你整个输入的双向信息」; 「而另一个可能有用去看的 token，是这个 SEP token。所以它就像 separator。而它的目标是分开两个句子」</b>。",
        "m": "⭐⭐ 关键在「<b>占位</b>」:<b>CLS 自己不代表任何词，所以它可以专职代表「整句」; 而妙处在于不用改架构 —— 只在输入前面多塞一个 token，就给模型加了一个「句子级」的出口</b>。<br>⭐⭐⭐ 而这里藏着一个绑死的依赖：<b>CLS 在开头却要携带整个输入的信息 ⇒ 这只有在双向注意力下才可能；若有因果掩码，开头那个 token 只能看到自己，什么也携带不了 ⇒ CLS 不是一个可以搬到 GPT 上的小技巧</b>。<br>⭐ 而 SEP 的存在本身就透露了训练任务：<b>BERT 的输入可以是「两个句子」, 而那正是 NSP</b>。",
        "w": " 「结构性 token」这个类别值得记住：<b>它们不对应任何真实的词，只负责给模型提供一个结构上的抓手 —— 而今天的 chat 模板里那些角色标记（system / user / assistant）走的是完全同一条思路</b>。",
        "r": "⇒ 这两个 token 是 BERT 时代留下的最通用的设计之一：<b>「在输入里塞一个专职 token，让它去承载某个句子级的量」—— 后来的 ViT 用 CLS token 做图像分类，用的就是一字不改的同一个办法</b>。<br>⇒ 更多（CLS 的池化替代方案、SEP 与 segment embedding 的配合）见<b>深度笔记</b>。",
        },
       {"t": "BERT 的 CLS token 为什么只能在双向注意力下工作？",
        "o": ["因为它要携带整个输入的信息，而它放在序列最开头 —— 若有因果掩码，开头那个 token 只能看到自己，什么也携带不了 ⇒ CLS 这个设计和「双向」是绑死的",
              "因为它需要和 SEP 配对，而 SEP 只在双向模型里有定义",
              "因为分类头只能接在第一个位置上",
              "因为单向模型的位置编码不支持额外的 token"],
        "a": 0,
        "w": "⇒ 而它的妙处是不用改架构：只在输入前面多塞一个不代表任何词的占位 token，就给模型加了一个句子级的出口。"})

    KP("⭐ 多阶段训练：预训练（MLM + NSP）→ 微调",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("77:53","you have this concept of multi-stage training",166);
  says("78:14","two objective functions that are respectively MLM and NSP",192);
  says("78:25","masked language model, it is a way for the model to learn the internal structure of the inputs",218);
  note("⭐⭐⭐ 这是 BERT 留给整个领域最重要的那个遗产",640,250,"y");
  boxNode(80,282,500,50,"MLM：挖掉词让它猜 ⇒ 学内部结构","g");
  boxNode(700,282,500,50,"NSP：两句是否相接 ⇒ 学句间关系","y");
  note("⚠ 一个管「词与词」,一个管「句与句」—— 而对 NSP 讲者的语气明显更松",640,358,"r");''',
         "<b>这是 BERT 留给整个领域最重要的那个遗产。</b><br>⭐ 「<b>关于这个模型有一件非常有意思的事 —— 就是你有这个「多阶段训练」的概念。所以你不是一次就把模型训好的，你是分多个阶段做的</b>」; 而预训练「<b>是用两个目标函数做的，它们分别是 MLM 和 NSP —— MLM 代表 Masked Language Model，而 NSP 是 Next Sentence Prediction</b>」。<br>⭐⭐ 两个名字各在问一个完全不同的问题：<b>MLM「是让模型去学输入的内部结构的一种方式」（管词与词）; 而 NSP「可以被看成是一种去看句子的排序说不说得通的方式」（管句与句）—— 而对 NSP，讲者的语气明显更松：一个说「它是」,一个说「它可以被看成是」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("78:49","it is a combination of objective function that the authors assumed to be helpful",166);
  says("79:29","this is what we call fine tuning",192);
  note("⭐⭐ 关键是一个动词：假定 —— 而不是证明、不是发现",640,222,"y");
  boxNode(80,254,500,50,"第一阶段：预训练，学通用嵌入","b");
  boxNode(700,254,500,50,"第二阶段：微调，接一个线性投影","g");
  note("昂贵、一次性、在海量无标注数据上",330,328,"b");
  note("⇒ 新加的部分小到几乎可以忽略",950,328,"g");
  note("⚠ 而那个「假定」的分量在三十分钟后兑现：RoBERTa 把 NSP 整个去掉了，效果更好",640,374,"r");''',
         "<b>这一镜的关键是一个动词，而它的分量在三十分钟后才兑现。</b><br>⭐ 「<b>我们会稍微深入看每一个，但它是作者假定对「学到高质量的通用嵌入」有帮助的一个目标函数的组合</b>」 ⇒ <b>「假定（assumed）」—— 而不是「证明」、不是「发现」。这个措辞是精确的：BERT 论文并没有证明 MLM+NSP 是最优组合，而后来 RoBERTa 做的事之一就是把 NSP 整个去掉，结果更好</b>。<br>⭐ 第二阶段是：「<b>一旦你有了这一切，你还有一个进一步的阶段 —— 你保留你已经学到的那些嵌入，然后在它上面附上某个别的网络，典型是一个线性投影，来把你学到的那些嵌入微调到某个目标任务上。这就是我们叫做 fine tuning 的东西</b>」。", 0)],
       {"h": "⭐ 多阶段训练",
        "k": "<b>「关于这个模型有一件非常有意思的事可以看 —— 就是你有这个「多阶段训练」的概念。所以你不是一次就把模型训好的，你是分多个阶段做的」; 「而这个预训练 —— 我们会详细看 —— 是用两个目标函数做的，它们分别是 MLM 和 NSP。所以 MLM 代表 Masked Language Model。而 NSP 是 Next Sentence Prediction」; 「所以掩码语言模型，它是让模型去学输入的内部结构的一种方式。然后 NSP，它可以被看成是一种去看「句子的排序说不说得通」的方式」; 「所以我们会稍微深入看每一个，但它是作者假定对「学到高质量的通用嵌入」有帮助的一个目标函数的组合」; 「你保留你已经学到的那些嵌入，然后在它上面附上某个别的网络，典型是一个线性投影，来把你学到的那些嵌入微调到某个目标任务上。这就是我们叫做 fine tuning 的东西」</b>。",
        "m": "⭐⭐⭐ 「多阶段训练」是 BERT 留给整个领域最重要的遗产：<b>第一阶段昂贵、一次性、在海量无标注数据上；第二阶段便宜、按任务做、只加一个线性投影 ⇒ 这就是今天「预训练 ＋ 微调」范式的原型</b>。<br>⭐⭐ 两个目标各管一层：<b>MLM 管词与词（学输入的内部结构）, NSP 管句与句（看排序说不说得通）—— 而讲者对两者的语气不同：一个说「它是」,一个说「它可以被看成是」</b>。<br>⭐⭐ 而那个动词是「<b>假定</b>」而不是「证明」:<b>BERT 论文没有证明 MLM+NSP 是最优组合 —— 后来 RoBERTa 把 NSP 整个去掉，效果更好</b>。",
        "w": " 第二阶段最该注意的是<b>新加的部分有多小</b>:<b>典型只是一个线性投影 ⇒ 你不是在重新训一个模型，你是在一个已经理解语言的表示之上接一个很小的读出头</b>。<br>⚠ 而「假定」这个措辞值得学：<b>当一篇论文说「我们假定这个组合有帮助」时，它其实在告诉你这里还没被验证 —— 而那往往就是下一篇论文的入口</b>。",
        "r": "⇒ 这套范式今天还在，只是名字换了：<b>预训练 → 指令微调 → 偏好对齐，还是同一个「一次昂贵、多次便宜」的结构</b>。<br>⇒ 更多（MLM 的 15% 掩码细节、NSP 的构造方式、RoBERTa 去掉 NSP 的实证）见<b>深度笔记</b>。",
        },
       {"t": "讲者说 MLM + NSP 是「作者假定对学到高质量通用嵌入有帮助」的组合 —— 这个措辞为什么重要？",
        "o": ["因为它说明两个目标函数在数学上等价",
              "因为「假定」不是「证明」:BERT 论文并没有证明这是最优组合，而后来 RoBERTa 做的事之一就是把 NSP 整个去掉，结果更好 —— 一篇论文说「我们假定」的地方，往往就是下一篇论文的入口",
              "因为作者其实做过完整的消融实验，只是没写进论文",
              "因为 NSP 后来被证明比 MLM 更重要"],
        "a": 1,
        "w": "⇒ 而讲者对两者的语气本身就有差别：MLM 说「它是」,NSP 说「它可以被看成是」。"})

    KP("⭐ 一个好提问，以及这套范式的好处与坏处",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("79:47","So the question is, do we still have just an encoder here?",166);
  says("79:59","The next-sentence prediction task is actually us putting two sentences, one after the other",192);
  says("80:12","Yeah, great point. And yeah, we are going to see that in detail very soon",218);
  note("⭐⭐ 这个提问很敏锐，而它是被名字误导的 —— 但那个误导值得分析",640,250,"y");
  boxNode(80,282,500,50,"误导：名字里有 prediction","r");
  boxNode(700,282,500,50,"真相：输入两句，输出一个是 / 否","g");
  note("⚠ 它是一个分类任务，所以 CLS 那个出口就够了 —— 一个 token 都不用生成",640,358,"r");''',
         "<b>这个提问很敏锐，而它被名字误导了 —— 但那个误导本身值得分析。</b><br>⭐ 学生问「<b>这里还是只有一个 encoder 吗？因为「下一句预测」可以被看成是一个 decoder 的任务</b>」 ⇒ <b>怀疑很合理：名字里有 prediction，而「预测下一个」在这门课里到此为止一直是 decoder 的活</b>。<br>⭐ 而答案很干脆：「<b>下一句预测这个任务，实际上是我们把两个句子一前一后放进去，然后预测它们是不是真的连续的。所以它是一个分类任务</b>」 ⇒ <b>输入是「句 A ＋ SEP ＋ 句 B」, 输出是一个是 / 否 —— 它不生成任何 token，所以 CLS 那个出口就够了。它叫 next sentence prediction，但它预测的是「这是不是下一句」,而不是「下一句是什么」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("80:27","this pre-training mechanism can be done on fairly unlabeled data",166);
  says("81:01","this is a very interesting way to learn interesting embeddings out of unlabeled data",192);
  says("81:17","you need very little data to build on top of it",218);
  note("⭐⭐⭐ 两个好处连起来才是完整的故事",640,250,"y");
  boxNode(80,282,500,50,"① 预训练用无标注数据（自监督）","g");
  boxNode(700,282,500,50,"② 微调只需要很少的数据","y");
  note("⚠ 便宜的那一半用海量数据、贵的那一半只要一点点 ⇒ 这才是它改变整个领域的原因",640,358,"r");''',
         "<b>好处里最根本的那一条，而它的论证方式值得体会。</b><br>⭐ 「<b>这个预训练机制可以在相当没有标注的数据上做。你仍然有这个下一句预测的任务，但这是某个你控制的东西，因为你知道哪些句子是彼此相接的 —— 所以它是某个你知道它是自监督的东西</b>」; 而 MLM「<b>也是某种无监督的东西。所以这是一个从未标注数据里学到有意思嵌入的非常有趣的方式</b>」。<br>⭐⭐⭐ 第二个好处必须和第一个连起来看：「<b>你只需要非常少的数据就能在它上面搭东西 —— 在微调阶段你从这些非常好的嵌入出发，然后只有少量几个权重要调。而这通常导向一个超过当时最先进水平的性能</b>」 ⇒ <b>便宜的那一半用海量数据、贵的那一半只要一点点</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("81:40","we have of course all the text generation tasks that are out of reach because we do not have a decoder",166);
  says("82:11","This could be seen as a downside",192);
  note("⭐ 两个坏处，而第一个和十三分钟前那句话是同一件事的两面",640,222,"y");
  boxNode(80,254,500,50,"① 所有生成任务都够不着","r");
  boxNode(700,254,500,50,"② 两阶段流程本身是个障碍","r");
  note("⇒「你这样没法做生成」「是的，那正是重点」",330,328,"v");
  note("⇒ 对比那些一次搞定的传统方法",950,328,"r");
  note("⚠ 而历史的判决是：第一个坏处最终决定了一切 —— 生成才是那个最大的市场",640,374,"r");''',
         "<b>两个坏处，而第一个和十三分钟前那句话恰好是同一件事的两面。</b><br>⭐ 「<b>关于坏处 —— 我们当然有所有那些文本生成任务是够不着的，因为我们没有 decoder</b>」 ⇒ <b>回想 68:18 那一镜：学生说「你这样没法做生成」,讲者答「是的，那正是重点」—— 同一个事实，在讲架构定位时是「分工」, 在讲优劣时是「坏处」。而历史的判决很清楚：生成才是那个最大的市场</b>。<br>⭐ 第二个坏处常被忽略但很真实：「<b>我们也可以把这个两阶段的流程、以及「我们需要进一步去调那些嵌入」这件事，看成是某种需要被跨过去的障碍。所以当你把这种方法论和那些更传统的、可以一次搞定的方法相比时 —— 这可能可以被看成一个坏处</b>」。", 0)],
       {"h": "⭐ 好处与坏处",
        "k": "学生问「这里还是只有一个 encoder 吗？因为下一句预测可以被看成是一个 decoder 的任务」,回答：<b>「下一句预测这个任务，实际上是我们把两个句子一前一后放进去，然后预测它们是不是真的连续的。所以它是一个分类任务」; 「对，很好的点。而我们很快就会详细看到那个」</b>。<br>⭐ 好处：<b>「那么在好处这一面：这个预训练机制可以在相当没有标注的数据上做。所以你仍然有这个下一句预测的任务，但这是某个你控制的东西，因为你知道哪些句子是彼此相接的。所以它是某个你知道它是自监督的东西」; 「而掩码语言模型这个任务也是某种无监督的东西。所以这是一个从未标注数据里学到有意思嵌入的非常有趣的方式」; 「然后你只需要非常少的数据就能在它上面搭东西。所以在微调阶段，你就从这些你学到的非常好的嵌入出发，然后你只有少量几个权重要调。而这通常导向一个超过当时最先进水平的性能」</b>;坏处：<b>「我们当然有所有那些文本生成任务是够不着的，因为我们没有 decoder」; 「而且我们也可以把这个两阶段的流程⋯⋯看成是某种需要被跨过去的障碍⋯⋯这可能可以被看成一个坏处」</b>。",
        "m": "⭐⭐ NSP 的名字是误导源：<b>它叫 next sentence prediction，但它预测的是「这是不是下一句」而不是「下一句是什么」⇒ 输入「句 A ＋ SEP ＋ 句 B」、输出一个是 / 否，不生成任何 token，所以 CLS 那个出口就够了</b>。<br>⭐⭐⭐ 两个好处连起来才是完整的故事：<b>预训练用无标注数据（自监督：你知道哪些句子相接、你知道你挖掉了哪个词）, 微调只需要很少的标注 ⇒ 便宜的那一半用海量数据、贵的那一半只要一点点 —— 这才是它改变整个领域的原因</b>。<br>⭐ 而第一个坏处和「那正是重点」是同一件事的两面：<b>讲架构定位时是分工，讲优劣时是坏处 —— 而历史的判决是：生成才是最大的市场</b>。",
        "w": " 「自监督」和「无监督」在这里被混用了：<b>讲者对 NSP 说 self-supervised、对 MLM 说 unsupervised，而两者其实都是自监督（标签是从数据本身构造出来的，而不是没有标签）—— 这是一个很常见的用词松动</b>。<br>⚠ 而第二个坏处在实践中很真实：<b>两阶段流程意味着你要维护两套数据、两套训练脚本、以及一个「预训练检查点」的分发问题 —— 相比那些一次搞定的传统方法，这是实打实的工程成本</b>。",
        "r": "⇒ 这一段的三件事可以这样带走：<b>CLS / SEP 这类结构性 token（今天的 chat 模板还在用）· 预训练＋微调的范式（今天还在用）· 而「没有 decoder」这个定位最终让这条路线退居二线</b>。<br>⇒ 更多（自监督与无监督的区别、NSP 的误导性命名、两阶段的工程成本）见<b>深度笔记</b>。",
        },
       {"t": "NSP（next sentence prediction）为什么不需要 decoder？",
        "o": ["因为它用 encoder 的最后一层直接生成下一句",
              "因为它预测的是「这是不是下一句」而不是「下一句是什么」:输入「句 A ＋ SEP ＋ 句 B」、输出一个是 / 否 —— 它是一个分类任务，不生成任何 token，所以 CLS 那个出口就够了",
              "因为 decoder 的功能被 SEP token 替代了",
              "因为 BERT 其实有一个很小的 decoder，只是讲者没提"],
        "a": 1,
        "w": "⇒ 学生的怀疑很合理，而它被名字误导了 —— 名字里有 prediction，而「预测下一个」到此为止一直是 decoder 的活。"})
