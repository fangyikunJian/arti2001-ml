# -*- coding: utf-8 -*-
"""CME295 L2 模块 h —— 字幕第 533–610 句（63:01–71:45）：Shervine 接手下半场 ——
三类架构。① encoder-decoder 与 T5 家族（mT5 / ByT5）、span corruption 与 sentinel token；
② encoder-only（不能生成，而那正是重点）；③ decoder-only，以及它为什么赢了。

⚠ 每镜 ≤6 句；旁白里不许出现半角双引号；setEq 里反斜杠写双份。
本模块 78 句 / 20 镜 = 3.9 句每镜。
"""


def add(KP):

    # ───────────────────────────────────────────── 35 ── 句 533–554
    KP("Shervine 接手：三类架构，先看 T5 家族",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("62:46","we are going to continue this lecture with some deeper dive into the kinds of models");
  note("换人了：Shervine 讲下半场",640,186,"v");
  boxNode(70,214,520,44,"下半场第一件事","g");
  note("深入看 transformer 格局里「有哪些种类的模型」",330,284,"g");
  boxNode(690,214,520,44,"下半场第二件事","b");
  note("深入一个「对分类场景特别有用」的具体架构",950,284,"b");
  note("⇒ 他先回到上一讲那个传统的 encoder/decoder 架构 —— 两个部件都有的那个",640,326,"y");
  note("★ 这个分工也和 L1 一样：Afshine 讲机制，Shervine 讲格局",640,364,"d");''',
         "<b>换人了，而下半场的两件事他说得很清楚。</b><br><b>他的话</b>：<b>「<u>好的，太好了。谢谢你，Afshine。所以我们要继续这一讲，对 transformer 格局里我们有的那些种类的模型做一些更深的深入。然后我们要对一个特定的、对分类场景非常有用的架构做一次深入。所以首先，我们要回到上次我们一起看过的那个架构 —— 这个传统的 encoder/decoder 架构，你两个部件都有的那个</u>。」</b><br><b>★★ 下半场的结构值得先记住，因为它决定了接下来四十分钟怎么走</b>：<b>⇒ <u>先横着扫一遍</u>：transformer 分成三类架构（encoder-decoder、encoder-only、decoder-only），各自能干什么。</b><b>⇒ <u>再竖着挖一个</u>：BERT 从头到尾走一遍，加上 DistilBERT 和 RoBERTa。</b><br><b>★★★ 这个「<u>先横扫再竖挖</u>」的结构是讲一个领域最有效的办法之一</b>：<b>⇒ 只横扫，你知道有哪些东西但什么都不会；<u>只竖挖，你懂一个但不知道它在哪</u>。</b><br><b>⇒ 而 L1 的下半场也是这个结构：<u>Shervine 先扫了一遍 NLP 的三个桶，再把 transformer 端到端走了一遍</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("63:38","So T5 is a paper that is an abbreviation of multiple Ts");
  note("⭐ T5 这个名字里的五个 T",640,186,"y");
  seq(90,214,["Transfer","Text","to","Text","Transformer"],["g","y","d","y","b"],210,44);
  note("⇒ 讲者：第一个是 transfer，然后是 text-to-text，transformers",640,290,"d");
  note("★★ 所以 T5 = T 开头的五个词，而不是「第 5 版」",640,322,"y");
  note("⚠ 很多人以为 T5 是版本号 —— 它不是",640,360,"r");''',
         "<b>这个名字的来历值得专门记一下，因为它最容易被误解。</b><br><b>讲者的话</b>：<b>「<u>所以这里我们讲 T5 这个模型家族。T5 是一篇论文，它是多个 T 的缩写。所以第一个是 transfer，然后是 text-to-text，transformers。所以这就是 T5 这个命名的来处</u>。」</b><br><b>★★★ 拆开来就是 <u>Transfer Text-to-Text Transformer</u> —— 数一下 T 开头的词：<u>Transfer、Text、to、Text、Transformer</u>，五个 T。</b><br><b>⚠ 所以 <u>T5 不是「第 5 版」</u>，这是一个很常见的误解。</b><b>⇒ 对比一下：<u>GPT-4 的 4 是版本号，Llama 3 的 3 是版本号；而 T5 的 5 是「有五个 T」</u>。</b><br><b>★★ 而这个名字里最重要的信息是中间那段：<u>Text-to-Text</u></b>：<b>⇒ T5 的核心主张是「<u>把所有 NLP 任务都写成「输入一段文本、输出一段文本」</u>」。</b><b>⇒ 分类？输出类别名这个词。翻译？输出译文。摘要？输出摘要。<u>甚至回归 —— 输出那个数字的文本形式</u>。</b><br><b>⇒ <u>这个想法在 2019 年是相当激进的，而它今天已经是常识了</u> —— 所有 LLM 都是这么用的。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("64:02","And then it had mT5. m stands for multilingual");
  note("家族成员一：mT5",640,186,"v");
  boxNode(130,214,1020,44,"m = multilingual（多语言）","g");
  note("⇒ 在「它被训练的那些数据」上做了更多工作",640,292,"y");
  note("★ 以及在「词表是在什么上面算出来的」这件事上也做了更多工作",640,324,"g");
  note("⚠ 留意他特别点出了「词表」—— 多语言模型最难的部分往往就在这里",640,362,"r");''',
         "<b>第一个变体，而讲者点出的两处改动都不在模型结构上。</b><br><b>讲者的话</b>：<b>「<u>然后它派生出了多个版本。所以 T5 就像是那个原味的论文。然后它有了 mT5 —— m 代表 multilingual（多语言），那里在它被训练的数据上做了更多工作，以及在词表是在什么上面被计算出来的这件事上</u>。」</b><br><b>★★ 请注意改的是什么：<u>数据 + 词表，而不是架构</u>。</b><br><b>★★★ 而「<u>词表</u>」这一点是多语言模型最实际的难题，值得展开</b>：<b>⇒ 回想 L1 讲 tokenization：<u>词表是在训练语料上学出来的合并规则</u>。</b><b>⇒ 如果你的语料 95% 是英文，<u>那学出来的词表几乎全是英文的子词</u>。</b><br><b>⚠ 后果是：一个中文词可能被切成五六个 token，<u>而同样意思的英文词只占一个</u>。</b><b>⇒ <u>于是中文用户为同样的内容付更多的 token 费、而且更快撞到上下文上限</u>。</b><b>⇒ 这不是一个假想的问题，<u>它在今天所有的 LLM 上都真实存在</u>。</b><br><b>★ 所以 mT5 做的事是：<u>重新在一个语言分布更均衡的语料上学词表</u>。而这件事远比「加几层」要紧。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("64:14","And then you have ByT5");
  note("⭐ 家族成员二：ByT5 —— 干脆不要 tokenizer",640,186,"y");
  boxNode(130,214,1020,44,"By = byte（字节）；它是一种「免 tokenizer」的方法","g");
  note("⇒ 你放弃「做 tokenization」这件事本身",640,292,"y");
  note("★★ 取而代之：你基本上在「字节层面」操作",640,324,"g");
  note("⚠ 这是对 L1 那整段 tokenization 讨论的一个激进回答",640,362,"r");''',
         "<b>这个变体很激进，而它直接回答了 L1 里那整段关于 tokenization 的讨论。</b><br><b>讲者的话</b>：<b>「<u>然后你有 ByT5，它是某种免 tokenizer 的方法 —— 在这里你放弃了「做 tokenization」这件事。而取而代之，你基本上在字节的层面上操作。所以 By 就是 byte</u>。」</b><br><b>★★★ 回想 L1 里讲过的那四种切法：<u>按词切（OOV 问题）、按字符切（序列太长）、按子词切（折中，今天的主流）、按字节切</u>。</b><b>⇒ <u>ByT5 就是把最后那条路走到底</u>。</b><br><b>★★ 它解决了什么：<u>tokenization 的全部麻烦都消失了</u></b>：<b>⇒ <u>没有 OOV</u> —— 任何字符串都能表示成字节。</b><b>⇒ <u>没有语言偏见</u> —— 词表不是从某个语料学出来的。</b><b>⇒ <u>没有拼写盲区</u> —— 模型能看到每个字符，<u>所以它能数字母、能处理错别字</u>（这是今天 LLM 的一个著名弱点）。</b><br><b>⚠ 而代价很大：<u>序列长度暴增</u>。</b><b>⇒ 一个英文词平均 4–5 个字节，而子词切法下大约是 1.3 个 token。<u>所以序列长了三四倍</u>。</b><b>⇒ 而注意力是 O(n²) ⇒ <u>计算量涨十倍以上</u>。</b><b>⇒ <u>这就是为什么字节级方法到今天仍然是少数派</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("64:33","So instead of having an o of 30k, you have 2 to the power of 8");
  note("⭐⭐ 词表大小的对比，这个数字很有冲击力",640,186,"y");
  boxNode(70,214,520,44,"子词切法（典型）","b");
  note("词表约 3 万（o of 30k）",330,284,"b");
  boxNode(690,214,520,44,"ByT5（字节级）","g");
  note("词表 2⁸ = 256",950,284,"g");
  note("⇒ 讲者：一个字节是 8 比特，而你可以把每个字符都表示成字节",640,326,"y");
  note("★★ 3 万 → 256，整整两个数量级",640,364,"r");''',
         "<b>这个数字对比很有冲击力，而它顺带解释了参数量去哪儿了。</b><br><b>讲者的话</b>：<b>「<u>而基本上，你有一个小得多的词表大小。所以与其有 3 万这个量级，你有 2 的 8 次方 —— 因为一个字节是 8 比特。然后你可以把每一个字符都表示成字节。所以这就是他们做的事</u>。」</b><br><b>★★★ 把这个变化的后果算一下，因为它影响的不只是词表那一行</b>：<b>⇒ <u>嵌入矩阵</u>：从 <u>30000 × d</u> 变成 <u>256 × d</u>。如果 d = 768，那是从 <u>2300 万参数</u>降到 <u>20 万</u>。</b><b>⇒ <u>输出层（softmax 那一层）</u>同样从 2300 万降到 20 万。</b><br><b>★★ 于是一个很有意思的结果：<u>字节级模型把「词表」这件事上的参数几乎全省了，可以把它们投到层数和宽度上去</u>。</b><br><b>⚠ 但代价仍然在那里：<u>序列长三四倍，而 O(n²) 让它变成十倍以上的计算</u>。</b><b>⇒ <u>省下的参数远远补不上多出来的计算</u>。</b><br><b>★ 不过这条路没有死：<u>今天仍有人在做字节级和「无 tokenizer」的模型</u>（比如 2024 年的一些工作用层级结构来压缩字节序列）。</b><b>⇒ <u>因为 tokenization 带来的那些麻烦是真实的，而它一直是 LLM 里最不优雅的那个部件</u>。</b>", 0)],
       {"h": "Shervine 接手：三类架构，先看 T5 家族",
        "k": "下半场两件事：<b>① 深入看 transformer 格局里「有哪些种类的模型」；② 深入一个「对分类场景特别有用」的具体架构</b>。先看 <b>T5 家族</b>：<b>T5 = 多个 T 的缩写 —— Transfer Text-to-Text Transformer</b>（不是「第 5 版」）。变体：<b>mT5（m = multilingual，在数据和「词表在什么上面算出来」这两件事上做了更多工作）</b>；<b>ByT5（By = byte，一种「免 tokenizer」的方法 —— 放弃 tokenization，在字节层面操作，词表从约 3 万降到 2⁸ = 256）</b>。",
        "m": "★★ 名字里最重要的是中间那段 <b>Text-to-Text</b>：T5 的核心主张是「<b>把所有 NLP 任务都写成「输入一段文本、输出一段文本」</b>」（分类就输出类别名、翻译就输出译文、甚至回归就输出数字的文本形式）⇒ <b>这个想法在 2019 年相当激进，今天已是常识 —— 所有 LLM 都是这么用的</b>。",
        "w": "★★★ mT5 改的是<b>数据 + 词表，不是架构</b>，而「词表」是多语言最实际的难题：<b>如果语料 95% 是英文，学出来的词表几乎全是英文子词 ⇒ 一个中文词被切成五六个 token，而同义的英文词只占一个</b> ⇒ <b>中文用户为同样内容付更多 token 费、更快撞到上下文上限</b>（今天所有 LLM 上都真实存在）。所以 mT5 做的是<b>在语言分布更均衡的语料上重学词表</b> —— 比「加几层」要紧得多。",
        "r": "ByT5 解决了 tokenization 的全部麻烦：<b>没有 OOV、没有语言偏见、没有拼写盲区</b>（能看到每个字符 ⇒ 能数字母、能处理错别字，这是今天 LLM 的著名弱点）。⇒ 参数也省：<b>嵌入矩阵从 30000×d 降到 256×d —— d=768 时从 2300 万降到 20 万</b>，输出层同样。⚠ 但代价很大：<b>一个英文词平均 4–5 字节、子词切法下约 1.3 个 token ⇒ 序列长三四倍，而注意力 O(n²) ⇒ 计算量涨十倍以上，省下的参数远远补不上</b>。⇒ 这就是<b>字节级方法至今仍是少数派</b>的原因，但这条路没死 —— <b>tokenization 一直是 LLM 里最不优雅的那个部件</b>。"},
       {"t": "T5 这个名字里的「5」是什么意思？",
        "o": ["第 5 个版本",
              "T 开头的五个词：Transfer Text-to-Text Transformer —— 而核心主张是「把所有 NLP 任务写成文本进、文本出」",
              "5 个 encoder 层",
              "5 种预训练任务"],
        "a": 1,
        "w": "⇒ 这个「Text-to-Text」的想法在 2019 年相当激进，今天已是常识 —— 所有 LLM 都是这么用的。"})

    # ───────────────────────────────────────────── 36 ── 句 555–574
    KP("⭐ span corruption：T5 换掉了训练目标",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:03","the objective function changes a bit with what the original transformer did");
  note("⭐ 关于 T5 家族最该知道的一件事",640,186,"y");
  boxNode(70,214,520,44,"原始 transformer","b");
  note("训练任务 = next token prediction（预测下一个 token）",330,284,"b");
  boxNode(690,214,520,44,"T5 家族","g");
  note("改成了所谓的 span corruption 任务",950,284,"g");
  note("⇒ 讲者：关于 T5 家族我想提的一件事就是目标函数变了一点",640,326,"y");
  note("★★ 请记住这个区别 —— 它是 71:14 那个「为什么 decoder-only 赢」的关键",640,364,"r");''',
         "<b>这是关于 T5 最该记住的一件事，而它在八分钟后会变成一个关键论据。</b><br><b>讲者的话</b>：<b>「<u>然后关于 T5 家族我想提的一件事是：目标函数和原始 transformer 做的那个有一点变化。所以原始 transformer 为训练任务做的是 next token prediction（下一个 token 预测）。但 T5 家族，他们做的是在所谓的 span corruption 任务上操作</u>。」</b><br><b>★★★ 请把这个对比记牢，因为它是 <u>71:14</u> 那个结论的核心论据</b>：<b>⇒ 讲者后面会说：<u>人们的投入流向了「最容易 scale up 和泛化」的任务 —— next-word prediction，而不是 T5 那个「更定制、更复杂」的任务</u>。</b><br><b>★★ 所以这里不只是「两个不同的预训练任务」，<u>它是一场关于「预训练任务该有多复杂」的路线之争</u></b>：<b>⇒ <u>T5 的立场</u>：精心设计的任务能学到更好的表示。</b><b>⇒ <u>GPT 的立场</u>：最简单的任务 + 最多的数据和算力，赢。</b><br><b>⇒ <u>历史给出的答案是后者，而这件事值得想清楚为什么</u>。</b><b>⇒ 讲者在 70:44 那镜会给出理由，而它比「简单就是好」要深。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:33","instead of putting everything to the encoder, you would leave blanks");
  note("span corruption 是什么",640,186,"v");
  stack(640,200,["你的句子作为 encoder 的输入","但不是把「全部」都放进 encoder","⇒ 你要留下一些「空白」"],560,32,8);
  note("⇒ 而这就是我们叫做 span corruption（片段损坏）的东西",640,328,"y");
  note("★ 而被损坏的那个 span，可以是「一个」也可以是「多个」token 缺失",640,356,"g");
  note("⚠ 注意「span（片段）」这个词 —— 它和 BERT 的「单个 token」掩码不一样",640,386,"r");''',
         "<b>做法本身很直观，而关键在那个「片段」上。</b><br><b>讲者的话</b>：<b>「<u>所以基本上你会有你的句子作为 encoder 的输入。而不是把所有东西都放进 encoder，你会留下一些空白。而这就是我们叫做 span corruption 的东西。然后这个 span corruption 可以是一个、也可以是多个 token 缺失</u>。」</b><br><b>★★★ 「<u>span（片段）</u>」这个词是 T5 和 BERT 的分界线，值得现在就对比清楚</b>：<b>⇒ <u>BERT 的 MLM</u>：随机挑<u>单个 token</u> 遮住（89:08 那镜会讲）。</b><b>⇒ <u>T5 的 span corruption</u>：挖掉<u>连续的一段</u>，而且<u>不告诉模型那段有多长</u>。</b><br><b>★★ 第二点是关键：<u>BERT 遮一个 token，模型知道要填一个词；T5 挖一段，模型得自己决定填几个词</u>。</b><b>⇒ 所以 span corruption <u>更难，而且更接近「生成」</u>。</b><br><b>⇒ 这也是为什么 T5 需要 decoder：<u>填一个词可以用一个分类头（BERT 那样），但填一段不定长的文本必须生成</u>。</b><br><b>⚠ 而这正好解释了三类架构的分工：<u>任务决定架构</u>。</b><b>⇒ T5 的任务要生成，所以它留着 decoder；<u>BERT 的任务只要分类，所以它可以扔掉 decoder</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:44","so for example, my teddy bear is cute and reading");
  note("⭐ 招牌例句又回来了",640,186,"y");
  boxNode(70,214,520,44,"原句","b");
  note("my teddy bear is cute and reading",330,284,"b");
  boxNode(690,214,520,44,"损坏后（送进 encoder）","g");
  note("my ⟦span⟧ is reading",950,284,"g");
  note("⇒ 讲者：你可以把 teddy bear 这段损坏掉，而留下 is reading",640,326,"y");
  note("★ 注意被挖掉的是「teddy bear」两个词 —— 一个 span，不是一个 token",640,364,"r");''',
         "<b>那个招牌例句又回来了，而这次它用来演示 span corruption。</b><br><b>讲者的话</b>：<b>「<u>所以如果我想举个例子 —— 比如说，my teddy bear is cute and reading。那么你可以把「my teddy bear」这段 span corrupted 掉，然后留下「is reading」。所以那可能就是一个潜在的 encoder 输入</u>。」</b><br><b>★★ 把 <u>teddy bear</u> 挑出来挖掉是个很好的示范，因为它刚好是一个<u>复合名词</u></b>：<b>⇒ 「teddy」和「bear」单独看都有别的意思；<u>合起来才是「泰迪熊」</u>。</b><b>⇒ 所以挖掉整个 span 迫使模型<u>把这个短语当成一个语义单位来恢复</u>。</b><br><b>★★★ 这就是 span 比单 token 更有价值的地方</b>：<b>⇒ 如果你只遮住「bear」，<u>模型看到「my teddy ___ is reading」几乎可以靠搭配猜出来</u> —— 这学到的东西很浅。</b><b>⇒ 而遮住「teddy bear」整段，<u>模型必须从「my ___ is reading」推断出一个合理的主语</u>。<u>这需要真正的语义理解</u>。</b><br><b>⚠ 顺带留意：<u>这句例句这一讲里稍微变了形</u>。</b><b>⇒ Afshine 在 12:18 用的是「<u>a cute teddy bear is reading</u>」，<u>而 Shervine 这里是「my teddy bear is cute and reading」</u>，稍后（95:26）又变成「<u>this teddy bear is so cute</u>」。</b><b>⇒ 两位讲者共用这个「主角」但不严格对齐 —— <u>这是真实课堂的常态</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("66:14","And then the T5 families calls them sentinel tokens");
  note("⭐⭐ 关键术语：sentinel token（哨兵 token）",640,186,"y");
  boxNode(130,214,1020,44,"n 是「被损坏的 span 数量」的那个参数化 ⇒ 你会在这里有 n 个这样的 token","g");
  note("⇒ T5 家族把它们叫做 sentinel tokens",640,292,"y");
  note("★★ 如果你看到 sentinel tokens，它们代表的是「一段被损坏的 token」",640,324,"g");
  note("⚠ 注意是「一段」而不是「一个」—— 一个 sentinel 对应任意长度的一段",640,362,"r");''',
         "<b>这是该记住的那个术语，而它的妙处在于「一个符号代表一整段」。</b><br><b>讲者的话</b>：<b>「<u>然后你可以有最多 n 个 —— 我的意思是，n 是「被损坏的 span 的数量」那个参数化。所以你会在这里有 n 个这样的 token。然后 T5 家族把它们叫做 sentinel tokens。所以如果你看到 sentinel tokens，它们代表的是一段被损坏的 token</u>。」</b><br><b>★★★ 请体会这个设计的经济性</b>：<b>⇒ 你挖掉了「teddy bear」两个词，<u>但在输入里只放一个 sentinel token</u>（比如 <u>⟨extra_id_0⟩</u>）。</b><b>⇒ 于是 <u>encoder 的输入变短了</u> —— 挖掉 10 个词只放 1 个符号，输入省了 9 个位置。</b><br><b>★★ 而这带来一个微妙但重要的后果：<u>模型不知道那段有多长</u>。</b><b>⇒ 对比 BERT：<u>BERT 用一个 [MASK] 换一个 token，所以长度信息是保留的</u>。</b><b>⇒ <u>而 T5 一个 sentinel 换一整段，长度信息被丢掉了</u>。</b><br><b>⇒ <u>这让任务更难，但也更接近真实的生成场景</u> —— 真实写作时你也不知道该写几个词。</b><br><b>⚠ 实现上 T5 预留了 100 个 sentinel token（⟨extra_id_0⟩ 到 ⟨extra_id_99⟩），<u>用编号来区分「这是第几段空白」</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("66:26","to find each of these spans in series");
  note("⭐⭐⭐ decoder 这边怎么工作",640,186,"y");
  stack(640,200,["从一个「标示第一个被损坏 span」的 token 开始","一直解码，直到它预测出「下一个 sentinel token」","两个连续 sentinel 之间解出的 token = 被恢复的那一段"],620,32,8);
  note("⇒ 一直这样走到第 n+1 个",640,328,"y");
  note("★★ 所以 sentinel token 在输出里起的是「分隔符」的作用",640,356,"g");
  note("⚠ 讲者的定性：这基本上是对 next token prediction 目标函数的一个「转变」",640,386,"r");''',
         "<b>这是 span corruption 最精巧的一半：输出端怎么组织。</b><br><b>讲者的话</b>：<b>「<u>所以你们在 encoder 里有它们。然后 decoder 的工作就是按序把这些 span 一个个找出来。所以你从一个标示第一个被损坏 span 的 token 开始，然后你开始解码过程，直到它碰到一个预测出「下一个 sentinel token」的预测，一直到第 n+1 个 —— 其中两个连续的 sentinel token 之间被解码出来的那些 token，就对应着被恢复的那些损坏片段</u>。」</b><br><b>★★★ 用那个例句走一遍，整件事就清楚了</b>：<b>⇒ <u>encoder 输入</u>：<u>my ⟨id_0⟩ is reading</u>。</b><b>⇒ <u>decoder 目标输出</u>：<u>⟨id_0⟩ teddy bear cute and ⟨id_1⟩</u>。</b><br><b>★★ 请注意输出的形式：<u>它不是完整的原句，而是「每个 sentinel 后面跟着它该填的内容」</u>。</b><b>⇒ 为什么这样设计：<u>因为这样输出序列只包含被挖掉的部分，而不用重复抄一遍没被挖的部分</u>。</b><b>⇒ <u>于是训练效率高得多</u> —— 一个句子挖掉 15%，输出就只有 15% 那么长。</b><br><b>⚠ 而 sentinel token 在这里有<u>两个</u>角色：<u>在输入里它是占位符，在输出里它是分隔符</u>。</b><b>⇒ 一个符号干两件事，<u>这是很漂亮的设计</u>。</b>", 0)],
       {"h": "⭐ span corruption：T5 换掉了训练目标",
        "k": "关于 T5 家族最该知道的一件事：<b>目标函数变了</b>。<b>原始 transformer：next token prediction；T5 家族：span corruption</b> —— 句子进 encoder，但<b>不是把全部都放进去，而是留下一些「空白」</b>，而被损坏的 span <b>可以是一个也可以是多个 token 缺失</b>。例：<b>my teddy bear is cute and reading → my ⟦span⟧ is reading</b>。",
        "m": "⭐⭐ 关键术语 <b>sentinel token（哨兵 token）</b>：n 是被损坏 span 的数量，<b>输入里放 n 个这样的 token，而「一个 sentinel 代表一整段被损坏的 token」</b>。⇒ decoder 的工作是<b>按序把每个 span 找出来</b>：从标示第一段的 token 开始解码，<b>直到预测出下一个 sentinel，而两个连续 sentinel 之间解出的 token 就是被恢复的那一段</b>。走一遍：<b>encoder 输入 my ⟨id_0⟩ is reading ⇒ decoder 输出 ⟨id_0⟩ teddy bear cute and ⟨id_1⟩</b>。",
        "w": "★★★ 「<b>span（片段）</b>」是 T5 和 BERT 的分界：<b>BERT 的 MLM 挑单个 token 遮住，模型知道要填一个词；T5 挖连续一段，而且一个 sentinel 换一整段 ⇒ 长度信息被丢掉，模型得自己决定填几个词</b>。⇒ 所以 span corruption <b>更难、更接近生成</b>，而这也解释了三类架构的分工 —— <b>任务决定架构</b>：T5 的任务要生成所以留着 decoder，BERT 只要分类所以能扔掉 decoder。⇒ 输出形式的妙处：<b>只包含被挖掉的部分，不用重抄没挖的 ⇒ 挖 15% 输出就只有 15% 长，训练效率高得多</b>；而 sentinel 在输入里是占位符、在输出里是分隔符，<b>一个符号干两件事</b>。",
        "r": "★★ 记牢这个对比，它是 71:14 那个结论的核心论据：讲者后面会说<b>人们的投入流向了「最容易 scale up 和泛化」的 next-word prediction，而不是 T5 那个「更定制、更复杂」的任务</b>。⇒ 所以这是一场<b>关于「预训练任务该有多复杂」的路线之争</b>：<b>T5 的立场是精心设计的任务学到更好的表示；GPT 的立场是最简单的任务 + 最多的数据和算力</b> —— 而历史给出的答案是后者。⇒ 另：挑 <b>teddy bear</b> 挖是好示范，因为它是<b>复合名词</b> —— 只遮「bear」模型靠搭配就猜出来了（学得很浅），<b>遮整段才迫使它从「my ___ is reading」推断出一个合理主语</b>。"},
       {"t": "T5 的 span corruption 和 BERT 的 MLM 最本质的区别是什么？",
        "o": ["T5 遮的 token 更多",
              "一个 sentinel 换一整段（长度信息被丢掉，模型得自己决定填几个词），而 BERT 一个 [MASK] 换一个 token",
              "T5 只在 decoder 里遮",
              "BERT 的遮罩是确定性的"],
        "a": 1,
        "w": "⇒ 所以 span corruption 更接近生成，而这解释了架构分工：T5 的任务要生成所以留着 decoder，BERT 只要分类所以能扔掉。"})

    # ───────────────────────────────────────────── 37 ── 句 575–583
    KP("一个关于解码过程的提问，与 teacher forcing",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:03","So these parentheses is basically a shift from the next token prediction objective function");
  note("讲者给 span corruption 的定性",640,186,"v");
  boxNode(130,214,1020,44,"这基本上是对「next token prediction」这个目标函数的一个「转变（shift）」","g");
  note("⇒ 他用的词是 shift，不是 improvement（改进）",640,292,"y");
  note("★ 这个用词很中性 —— 它不预判哪个更好",640,324,"g");
  note("⚠ 而四分钟后他会说：历史选了 next-word prediction",640,362,"r");''',
         "<b>这一镜很短，但讲者的用词值得留意。</b><br><b>他的话</b>：<b>「<u>所以这些括号基本上是对 next token prediction 这个目标函数的一个转变</u>。」</b><br><b>★★ 「<u>转变（shift）</u>」这个词是中性的</b>：<b>⇒ 他没有说 <u>improvement（改进）</u>，也没有说 <u>complication（复杂化）</u>。</b><b>⇒ <u>只是「不一样了」</u>。</b><br><b>★★★ 而这个中性在这里是对的，因为<u>在 2019 年，T5 的这个选择看起来是很有道理的</u></b>：<b>⇒ T5 论文本身做了大量的消融实验，<u>比较了各种预训练目标，而 span corruption 在他们的实验里确实最好</u>。</b><b>⇒ 所以这不是一个拍脑袋的决定，<u>它是有实验支持的</u>。</b><br><b>⚠ 但四分钟后（70:44）讲者会说：<u>人们的算力投向了「最容易 scale up」的那个任务</u>。</b><b>⇒ <u>也就是说，T5 在「同等规模下哪个目标更好」这个问题上赢了，而在「哪个目标更能扩大规模」这个问题上输了</u>。</b><br><b>⇒ <u>这两个问题不一样，而后者才决定了历史</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:34","So you have sentinel tokens that denote some missing text");
  note("提问：能把「解码过程」再说详细点吗？",640,186,"v");
  boxNode(130,214,1020,44,"讲者：你刚说的关于「重建」那部分「完全正确」","g");
  note("⇒ 你有 sentinel token，它们标示某些「缺失的文本」",640,292,"y");
  note("★ 所以你想解码出来的就是那段缺失的文本",640,324,"g");
  note("⇒ 于是 decoder 的输出就恰好是「每一个 span 被重建出来」的样子",640,362,"d");''',
         "<b>学生要求把解码过程再说一遍，而讲者的复述把这件事钉死了。</b><br><b>学生的问题</b>：<b><u>你能把解码过程再说详细一点吗？</u></b><br><b>讲者的回答</b>：<b>「<u>所以你刚才说的关于重建那部分完全正确。所以你有 sentinel token，它们标示某些缺失的文本。所以你想要解码出来的就是那段缺失的文本。所以 decoder 的输出就会恰好是「每一个 span 被重建出来」的样子</u>。」</b><br><b>★★ 这个复述值得停一下，因为它排除了一个很自然的误解</b>：<b>⇒ <u>误解</u>：decoder 输出<u>完整的原句</u>（my teddy bear is cute and reading）。</b><b>⇒ <u>正解</u>：decoder 只输出<u>被挖掉的那些段</u>，用 sentinel 隔开。</b><br><b>★★★ 为什么这个区别要紧</b>：<b>⇒ 如果输出完整原句，<u>那模型大部分的工作是在抄写 encoder 已经看到的内容</u>。</b><b>⇒ 抄写是一个很容易学的任务，<u>它会把梯度和容量都浪费掉</u>。</b><br><b>⇒ 而只输出缺失部分，<u>每一个被预测的 token 都是真正需要推断的</u>。</b><b>⇒ <u>这是一个关于「如何设计训练目标」的普遍原则：让模型只为「它真正需要学会的东西」付出预测</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:50","you do a teacher-forcing mechanism where you input everything in the decoder");
  note("⭐ 训练时怎么跑：teacher forcing",640,186,"y");
  stack(640,200,["把「全部」都输入到 decoder 里","然后试着「一次性」把全部重建出来","⇒ 这叫 teacher forcing（教师强制）"],560,32,8);
  note("⇒ 讲者：如果你想知道训练是怎么工作的 —— 你做一个 teacher-forcing 机制",640,328,"y");
  note("★★ 关键在「一次性（all at once）」—— 训练时不是一个词一个词生成的",640,356,"g");
  note("⚠ 这是训练和推理的一个根本差异，很多人在这里卡住",640,386,"r");''',
         "<b>这是一个很重要的机制，而它解释了训练和推理为什么看起来完全不同。</b><br><b>讲者的话</b>：<b>「<u>然后如果你想知道训练是怎么工作的 —— 你做一个 teacher-forcing 机制，在那里你把所有东西都输入到 decoder 里，然后试着一次性把所有东西重建出来</u>。」</b><br><b>★★★ 把训练和推理并排看，差别很大</b>：<b>⇒ <u>推理时</u>：生成第 1 个词 ⇒ 把它接到输入上 ⇒ 生成第 2 个词 ⇒ …… <u>完全串行，n 个词要跑 n 次</u>。</b><b>⇒ <u>训练时（teacher forcing）</u>：<u>把正确答案整个塞进 decoder</u>，配上因果掩码，<u>一次前向就同时得到所有位置的预测</u>。</b><br><b>★★ 为什么能这样：<u>因为因果掩码保证了第 t 个位置看不到第 t 之后的内容</u>。</b><b>⇒ 所以虽然你把完整答案都塞进去了，<u>每个位置的预测仍然只依赖它之前的部分</u> —— <u>和串行生成在数学上等价</u>。</b><br><b>⚠ 而「<u>教师强制</u>」这个名字说的是：<u>每一步喂给模型的都是「正确答案」，而不是模型上一步自己的输出</u>。</b><b>⇒ 这带来一个著名的问题，叫 <u>exposure bias</u>：<u>训练时它从来没见过自己的错误，而推理时它必须接着自己的错误往下写</u>。</b>", 0)],
       {"h": "解码过程，与 teacher forcing",
        "k": "讲者给 span corruption 的定性：<b>这基本上是对 next token prediction 这个目标函数的一个「转变（shift）」</b>。提问「能把解码过程再说详细点」⇒ <b>sentinel token 标示缺失的文本，你要解码出来的就是那段缺失文本，所以 decoder 的输出恰好是「每一个 span 被重建出来」的样子</b>。训练：<b>做一个 teacher-forcing 机制 —— 把全部输入到 decoder 里，然后试着「一次性」把全部重建出来</b>。",
        "m": "★★ 这个复述排除了一个自然的误解：<b>误解是 decoder 输出完整原句，正解是只输出被挖掉的那些段、用 sentinel 隔开</b>。⇒ 为什么要紧：<b>输出完整原句时模型大部分工作是在抄写 encoder 已经看到的内容，而抄写很容易学、会把梯度和容量都浪费掉</b>；只输出缺失部分则<b>每个被预测的 token 都是真正需要推断的</b>。⇒ 普遍原则：<b>让模型只为「它真正需要学会的东西」付出预测</b>。",
        "w": "★★★ teacher forcing 解释了训练和推理为什么看起来完全不同：<b>推理时完全串行（生成一个接上去再生成下一个，n 个词跑 n 次）；训练时把正确答案整个塞进 decoder、配因果掩码，一次前向就得到所有位置的预测</b>。⇒ 能这样是因为<b>因果掩码保证第 t 个位置看不到 t 之后的内容 ⇒ 和串行生成在数学上等价</b>。⚠ 而「教师强制」这个名字说的是<b>每一步喂的都是「正确答案」而不是模型自己上一步的输出</b> ⇒ 带来著名的 <b>exposure bias</b>：<b>训练时它从来没见过自己的错误，推理时却必须接着自己的错误往下写</b>。",
        "r": "★★ 「<b>转变（shift）</b>」这个用词是中性的 —— 他没说 improvement 也没说 complication，<b>只是「不一样了」</b>。而这个中性是对的：<b>T5 论文本身做了大量消融实验比较各种预训练目标，而 span corruption 在他们的实验里确实最好</b> —— 不是拍脑袋的决定。★★★ 但四分钟后讲者会说算力投向了「最容易 scale up」的那个 ⇒ <b>T5 在「同等规模下哪个目标更好」上赢了，而在「哪个目标更能扩大规模」上输了 —— 这两个问题不一样，而后者才决定了历史</b>。"},
       {"t": "训练 T5 时用 teacher forcing，关键在哪一点？",
        "o": ["它让训练更准确",
              "把正确答案整个塞进 decoder、配因果掩码 ⇒ 一次前向同时得到所有位置的预测，而不用串行生成",
              "它避免了梯度消失",
              "它让 encoder 不必参与训练"],
        "a": 1,
        "w": "⚠ 代价是著名的 exposure bias：训练时模型从来没见过自己的错误，推理时却必须接着自己的错误往下写。"})

    # ───────────────────────────────────────────── 38 ── 句 584–593
    KP("第二类：encoder-only —— 它不能生成，而那正是重点",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("68:18","you just forget about the decoder and then just deal with the encoder");
  note("⭐⭐ 第二类架构，以及一段很漂亮的对话",640,186,"y");
  boxNode(130,214,1020,44,"做法：有 encoder/decoder 这个结构 ⇒ 你干脆忘掉 decoder，只处理 encoder","g");
  note("⇒ 讲者模拟学生：好，嘿，你这样没法做生成啊",640,292,"b");
  note("★★ 而他的回答是：是的 —— 那正是重点（that is exactly the point）",640,324,"y");
  note("⚠ 这句回答值得记住，它把一个「缺陷」翻成了「设计」",640,362,"r");''',
         "<b>这段对话很漂亮，而它翻转了一个判断。</b><br><b>讲者的话</b>：<b>「<u>然后现在我们要讲另一类 transformer —— 基本上你有这个 encoder/decoder 结构，而你干脆忘掉 decoder，只处理 encoder。所以你可能会跟我说：好，嘿，你这样没法做生成啊。而我会回答你：是的，那正是重点</u>。」</b><br><b>★★★ 「<u>是的，那正是重点</u>」—— 这句话把一个看起来的缺陷翻成了一个设计选择，而它的理由是实在的</b>：<b>⇒ 如果你的任务是<u>情感分类</u>，你根本不需要生成能力。</b><b>⇒ 而<u>带着一个用不上的 decoder，意味着一半的参数在白吃显存</u>。</b><br><b>★★ 但「那正是重点」还有一层更深的意思，<u>这一层才是真正的理由</u></b>：<b>⇒ <u>去掉 decoder 之后，你可以让注意力「双向」</u>。</b><b>⇒ 因为 decoder 必须用因果掩码（不能看未来），<u>而 encoder 没有这个限制</u>。</b><br><b>⇒ <u>所以 encoder-only 不只是「砍掉一半更省」，它换来了一个 decoder 永远做不到的能力 —— 每个 token 都能看到整个句子</u>。</b><b>⇒ 而这正是 BERT 名字里那个 <u>Bidirectional</u> 的来源（71:45 那镜）。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("68:37","it has encoder representations that can be used for tasks that might be more geared towards classification");
  note("encoder-only 能干什么",640,186,"v");
  boxNode(130,214,1020,44,"它有 encoder 的「表示」，可以用在「更偏向分类」的任务上","g");
  note("⇒ 举例：情感抽取（sentiment extraction）、token 分类（token classification）",640,292,"y");
  note("★★ 讲者的那句定位最要紧：所有这些「过去要用专门的语言模型来做」的事",640,324,"g");
  note("⇒ 现在都能用 transformer 的 encoder 部分来做",640,356,"y");
  note("⚠ 「过去要用专门模型」—— 这就是 BERT 当年带来的那场变化",640,386,"r");''',
         "<b>这一镜给出了 encoder-only 的用途，而讲者那句定位最值得记。</b><br><b>他的话</b>：<b>「<u>所以它有 encoder 的表示，这些表示可以用在那些可能更偏向分类的任务上。所以情感抽取、token 分类、所有这些过去要用专门的语言模型来做的事情 —— 它们都能用 transformer 的 encoder 部分来做</u>。」</b><br><b>★★★ 「<u>过去要用专门的语言模型来做</u>」这几个字，说的是 BERT 当年带来的那场变化，而它的分量值得交代</b>：<b>⇒ <u>BERT 之前</u>（2018 年以前）：每个 NLP 任务都有自己的一套模型。<u>情感分析一个、命名实体识别一个、句法分析一个</u>。</b><b>⇒ 每个都要<u>从头设计特征、从头训练、从头调参</u>。</b><br><b>★★ <u>BERT 之后</u>：<u>一个预训练好的 encoder + 一个小小的分类头</u>，就能在几乎所有这些任务上刷新纪录。</b><b>⇒ 而那个分类头<u>往往只是一层线性映射</u>。</b><br><b>⇒ <u>这就是「预训练 + 微调」这个范式的诞生，而它彻底改变了 NLP 的工作方式</u>。</b><br><b>⚠ 而今天我们已经走到了下一步：<u>连微调都不需要了，直接用 prompt</u>。<u>但 BERT 那一步是关键的中间环节</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("69:10","So BERT, which is like the central one, I would say in this landscape");
  note("⭐ 下半场要深入的三个 encoder-only 模型",640,186,"y");
  boxNode(60,214,350,44,"BERT","g");
  note("这个格局里「最中心」的那个",235,284,"g");
  boxNode(465,214,350,44,"DistilBERT","y");
  note("在一条改进轴上做研究",640,284,"y");
  boxNode(870,214,350,44,"RoBERTa","b");
  note("在另一条改进轴上",1045,284,"b");
  note("⇒ 讲者：这两个架构是在「若干条改进的轴」上做探索的",640,326,"d");
  note("★ 而「两条轴」的具体内容在 103:02 会被明确说出来",640,364,"r");''',
         "<b>下半场的三个主角公布，而「改进的轴」这个说法预告了结构。</b><br><b>讲者的话</b>：<b>「<u>而我们待会儿会深入一点，讲三个关键的 encoder-only 模型。所以 BERT —— 我会说它是这个格局里最中心的那个 —— 然后另外两个架构，DistilBERT 和 RoBERTa，它们是在若干条改进的轴上做探索的。所以这会很值得一看</u>。」</b><br><b>★★★ 「<u>改进的轴（axis of improvements）</u>」这个说法预告了整段的结构，而那两条轴在 <u>103:02</u> 那镜会被明确说出来</b>：<b>⇒ <u>轴一：延迟/成本</u> —— BERT base 有 1.1 亿参数，<u>有办法做得更小更快吗？</u> ⇒ <u>DistilBERT 的答案</u>。</b><b>⇒ <u>轴二：预训练目标</u> —— MLM 和 NSP 这两个目标<u>真的都有用吗？能不能简化？</u> ⇒ <u>RoBERTa 的答案</u>。</b><br><b>★★ 这个讲法值得学：<u>先讲一个基准模型，再用「它有什么毛病」来组织后续的模型</u>。</b><b>⇒ 比按时间顺序讲一串论文好得多，<u>因为你记住的是「每个模型解决了什么问题」而不是「它叫什么、哪年发的」</u>。</b><br><b>⇒ 而这也是一个读论文的办法：<u>任何一篇「改进了 X」的论文，先去找它认为 X 的毛病是什么</u>。</b>", 0)],
       {"h": "第二类：encoder-only —— 不能生成，而那正是重点",
        "k": "做法：<b>有 encoder/decoder 结构，而你干脆忘掉 decoder，只处理 encoder</b>。⇒ 讲者模拟学生「<b>你这样没法做生成啊</b>」，而他的回答是「<b>是的 —— 那正是重点</b>」。它能干什么：<b>有 encoder 的「表示」，用在更偏向分类的任务上 —— 情感抽取、token 分类，所有这些「过去要用专门的语言模型来做」的事</b>。下半场要深入三个：<b>BERT（这个格局里最中心的那个）、DistilBERT、RoBERTa（在若干条「改进的轴」上做探索）</b>。",
        "m": "★★★ 「那正是重点」还有一层更深的理由：<b>去掉 decoder 之后，你可以让注意力「双向」</b> —— 因为 <b>decoder 必须用因果掩码（不能看未来），而 encoder 没有这个限制</b>。⇒ 所以 encoder-only 不只是「砍掉一半更省」，<b>它换来了一个 decoder 永远做不到的能力：每个 token 都能看到整个句子</b> —— 而这正是 BERT 名字里那个 <b>Bidirectional</b> 的来源。",
        "w": "★★★ 「<b>过去要用专门的语言模型来做</b>」说的是 BERT 当年带来的那场变化：<b>BERT 之前每个 NLP 任务都有自己一套模型（情感分析一个、NER 一个、句法分析一个），每个都要从头设计特征、从头训练、从头调参</b>；<b>BERT 之后一个预训练好的 encoder + 一个往往只是一层线性映射的分类头，就能在几乎所有这些任务上刷新纪录</b>。⇒ <b>这就是「预训练 + 微调」范式的诞生</b>，而今天我们已走到下一步（连微调都不要、直接 prompt），但 BERT 那一步是关键的中间环节。",
        "r": "★★ 「<b>改进的轴</b>」预告了整段结构，而那两条轴在 103:02 会被明确说出：<b>轴一是延迟/成本（BERT base 有 1.1 亿参数，能更小更快吗 ⇒ DistilBERT）；轴二是预训练目标（MLM 和 NSP 真的都有用吗、能简化吗 ⇒ RoBERTa）</b>。⇒ 这个讲法值得学：<b>先讲一个基准模型，再用「它有什么毛病」来组织后续的模型</b> —— 比按时间顺序讲一串论文好得多，<b>因为你记住的是「每个模型解决了什么问题」而不是「它叫什么、哪年发的」</b>。⇒ 也是一个读论文的办法：<b>任何一篇「改进了 X」的论文，先去找它认为 X 的毛病是什么</b>。"},
       {"t": "encoder-only 模型「不能生成」为什么反而是设计上的重点？",
        "o": ["因为生成任务不重要",
              "去掉 decoder 后注意力可以「双向」（decoder 必须用因果掩码），换来了每个 token 都能看到整句这个能力",
              "因为 encoder 的参数更多",
              "因为分类任务的数据更容易收集"],
        "a": 1,
        "w": "★★★ 这正是 BERT 名字里那个 Bidirectional 的来源 —— 而它是 decoder 永远做不到的。"})

    # ───────────────────────────────────────────── 39 ── 句 594–610
    KP("⭐⭐ 第三类：decoder-only，以及它为什么赢了",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("69:40","when you have no encoder, you do not have your encoder embeddings");
  note("⭐ 第三类：把 encoder 整个去掉",640,186,"y");
  stack(640,200,["没有 encoder ⇒ 没有 encoder 嵌入","而 cross-attention 本来是靠这些嵌入喂的","⇒ 所以 cross-attention 这个模块「整个消失」"],620,32,8);
  note("⇒ 于是每一个被堆起来的 decoder 里，只剩下 masked self-attention 和一个 FFN",640,328,"y");
  note("★★ 这就是今天 LLM 的架构 —— 一个 block 只有两样东西",640,356,"g");
  note("⚠ 对比原始 decoder：它有三样（masked self-attn、cross-attn、FFN）",640,386,"r");''',
         "<b>第三类架构，而它的结构简洁到让人意外。</b><br><b>讲者的话</b>：<b>「<u>然后还有最后一类。所以就像 Afshine 刚提到的，今天的 LLM 把 encoder 那部分整个去掉了。而当你没有 encoder 时，你在你那堆叠起来的 encoder 的末端就没有 encoder 嵌入可以喂给 cross-attention。所以这个模块整个消失了。所以每一个被堆起来的 decoder 里，就只有 masked self-attention 和一个 FFN 作为它的组成部分</u>。」</b><br><b>★★★ 把三种 block 并排数一下</b>：<b>⇒ <u>原始 encoder block</u>：自注意力 + FFN（<u>两样</u>）。</b><b>⇒ <u>原始 decoder block</u>：带掩码自注意力 + 交叉注意力 + FFN（<u>三样</u>）。</b><b>⇒ <u>今天的 decoder-only block</u>：带掩码自注意力 + FFN（<u>两样</u>）。</b><br><b>★★ 于是一个有点反直觉的事实：<u>今天 LLM 的 block 结构和原始的 encoder block 几乎一样</u>。</b><b>⇒ <u>唯一的区别就是那个因果掩码</u>。</b><br><b>⇒ 所以「decoder-only」这个名字其实有点误导：<u>它的 block 长得像 encoder，只是加了掩码</u>。</b><b>⇒ <u>它叫 decoder 是因为它的「功能」是解码（自回归生成），不是因为它的结构来自 decoder</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:17","the main hypothesis was that the encoder part is very useful");
  note("⭐⭐ 历史的转向：当初的假设被推翻了",640,186,"y");
  boxNode(70,214,520,44,"一开始（流行的）","b");
  note("transformer 那种架构（两半都有）",330,284,"b");
  note("假设：encoder 对「得到 decoder 的表示」非常有用",330,314,"d");
  boxNode(690,214,520,44,"随着时间","g");
  note("人们意识到：你的算力预算",950,284,"g");
  note("最好「全部投在 decoder 上」",950,314,"g");
  note("★★ 这是一个「假设被数据推翻」的具体例子",640,364,"r");''',
         "<b>这就是那场转向，而它的本质是一个假设被推翻了。</b><br><b>讲者的话</b>：<b>「<u>因为当你看每一类模型的流行度时 —— 你过去有这种类似 transformer 的架构，它在一开始的时候很流行，那时主要的假设是：encoder 那部分对于得到 decoder 的表示非常有用。但随着时间过去，人们意识到你的算力预算最好全部投在 decoder 上</u>。」</b><br><b>★★★ 把这件事说准：<u>当初的假设不是「胡说」，它是一个合理但错了的假设</u></b>：<b>⇒ <u>合理在哪</u>：直觉上，先用一个双向的 encoder「彻底理解」输入，再让 decoder 基于这个理解去生成，<u>听起来比「只能从左往右看」要强</u>。</b><b>⇒ <u>错在哪</u>：在固定的算力预算下，<u>encoder 占掉的那一半参数，用在 decoder 上收益更大</u>。</b><br><b>★★ 「<u>算力预算（compute budget）</u>」这个词是整件事的关键，<u>它把问题从「哪个更好」改成了「同样的钱买哪个</u>」。</b><b>⇒ <u>这两个问题的答案常常不一样，而工程里永远是第二个问题在起作用</u>。</b><br><b>⇒ 而 decoder-only 为什么收益更大，<u>有一个很具体的原因：encoder-decoder 里只有 decoder 那一半在学「生成」，而 decoder-only 里全部参数都在学生成</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:44","easiest to scale up and generalize");
  note("⭐⭐⭐ 真正的理由：哪个任务「最容易扩大规模」",640,186,"y");
  boxNode(70,214,520,44,"next-word prediction","g");
  note("最容易 scale up、最容易泛化的任务",330,284,"g");
  note("讲者：我会说这是你能做的「最简单的事」",330,314,"d");
  boxNode(690,214,520,44,"T5 那个任务","b");
  note("可能更「定制（bespoke）」",950,284,"r");
  note("你得去「损坏」东西 ⇒ 所以它更复杂",950,314,"r");
  note("★★ 请注意他比的不是「哪个学得更好」，而是「哪个更好扩大」",640,364,"y");''',
         "<b>这是整段最该记住的一镜，而它比「简单就是好」要深。</b><br><b>讲者的话</b>：<b>「<u>然后有更多的投入流向了那种我会说「最容易扩大规模和泛化」的任务 —— next-word prediction（下一个词预测）—— 而不是我刚刚为 T5 提到的那个任务，那个可能更定制。所以你得去损坏一些东西，所以它更复杂。而 next-word prediction，我会说是你能做的最简单的事情</u>。」</b><br><b>★★★ 请注意他比较的维度：<u>不是「哪个任务学得更好」，而是「哪个任务更容易扩大规模」</u>。</b><br><b>⇒ 而 next-word prediction 在这一点上有一个压倒性的优势：<u>任何一段文本，不经任何处理，都是训练数据</u>。</b><b>⇒ 整个互联网、所有的书、所有的代码 —— <u>拿来就能用，一个字都不用标、一个字都不用改</u>。</b><br><b>★★ 而 span corruption 需要什么：<u>你得决定挖多少、挖在哪、挖多长、用几个 sentinel</u>。</b><b>⇒ 这些都是<u>超参数</u>，而每一个超参数都是一个要调的东西、一个可能调错的地方。</b><b>⇒ <u>更要紧的是：这些选择把一个「通用的数据」变成了一个「为某个任务预处理过的数据」</u>。</b><br><b>⇒ <u>而规模的敌人正是预处理</u>。你要用 10 万亿 token 训练时，<u>任何一步额外的处理都是巨大的成本</u>。</b>", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("71:05","it proved to be wonders and well-aligned with the task of being a helpful kind of chatbot");
  note("⭐⭐ 第二个理由：它和「今天的应用」刚好对齐",640,186,"y");
  boxNode(130,214,1020,44,"next-word prediction 被证明「创造奇迹」","g");
  note("⇒ 而且它和「做一个有帮助的聊天机器人」这个任务高度对齐",640,292,"y");
  note("★★ 而那正是今天主要的应用形态",640,324,"g");
  note("⇒ 讲者收口：decoder-only 架构我今天不讲，它会是后面几讲的核心",640,362,"d");''',
         "<b>第二个理由，而它说的是一件很难事先预料到的事。</b><br><b>讲者的话</b>：<b>「<u>而它被证明创造了奇迹，而且和「做一个有帮助的那种聊天机器人」这个任务高度对齐 —— 而那基本上就是今天主要的应用。然后 decoder-only 架构 —— 我今天不打算讲它们，但它会是后面几讲的核心部分，那时我们会越来越多地讲 LLM</u>。」</b><br><b>★★★ 「<u>和「做一个有帮助的聊天机器人」高度对齐</u>」—— 这一点在 2019 年是完全看不出来的</b>：<b>⇒ 当时没人知道「<u>把下一个词预测做到极致</u>」会长出一个能对话、能写代码、能推理的东西。</b><b>⇒ <u>而回头看，对齐的理由其实很直接</u>：<u>聊天就是「给定前面的对话，接着写下一句」</u>。</b><b>⇒ <u>这在形式上和 next-word prediction 是同一件事</u>。</b><br><b>★★ 对比一下 BERT 的 MLM：<u>「填空」这个形式和「对话」不对齐</u>。</b><b>⇒ 你没法让一个填空模型自然地接着你的话往下说。<u>所以 BERT 再强，也长不出 ChatGPT</u>。</b><br><b>⇒ <u>于是这件事的教训是：预训练任务的「形式」会决定模型最终能变成什么</u>。</b><b>⇒ 而 next-word prediction 碰巧选中了那个<u>和人类使用语言的方式最接近</u>的形式。</b>", 0)],
       {"h": "⭐⭐ 第三类：decoder-only，与它为什么赢",
        "k": "<b>今天的 LLM 把 encoder 那部分整个去掉了</b>：<b>没有 encoder ⇒ 没有 encoder 嵌入可以喂给 cross-attention ⇒ 这个模块整个消失</b>，所以<b>每个堆起来的 decoder 里只剩 masked self-attention 和一个 FFN</b>。为什么赢：<b>① 一开始的假设是「encoder 对得到 decoder 的表示非常有用」，但随着时间人们意识到「算力预算最好全部投在 decoder 上」；② 更多投入流向「最容易 scale up 和泛化」的任务 —— next-word prediction（最简单的事），而不是 T5 那个「更定制、更复杂」的（你得去损坏东西）；③ 它被证明「创造奇迹」，而且和「做一个有帮助的聊天机器人」高度对齐 —— 那正是今天主要的应用</b>。",
        "m": "★★★ 把三种 block 并排数：<b>原始 encoder block 两样（自注意力+FFN）、原始 decoder block 三样（带掩码自注意力+交叉注意力+FFN）、今天的 decoder-only block 两样（带掩码自注意力+FFN）</b>。⇒ 一个反直觉的事实：<b>今天 LLM 的 block 和原始 encoder block 几乎一样，唯一区别是那个因果掩码</b> ⇒ 所以「decoder-only」这个名字有点误导 —— <b>它叫 decoder 是因为「功能」是自回归解码，不是因为结构来自 decoder</b>。",
        "w": "★★★ 第二个理由的关键是比较的<b>维度</b>：<b>不是「哪个任务学得更好」，而是「哪个任务更容易扩大规模」</b>。而 next-word prediction 有压倒性优势：<b>任何一段文本不经任何处理都是训练数据 —— 整个互联网、所有书、所有代码，拿来就用，一个字都不用标</b>。而 span corruption 要决定<b>挖多少、挖在哪、挖多长、用几个 sentinel</b>，每个都是超参数，<b>更要紧的是这些选择把「通用的数据」变成了「为某个任务预处理过的数据」—— 而规模的敌人正是预处理</b>（用 10 万亿 token 时任何额外一步都是巨大成本）。",
        "r": "★★ 当初那个假设<b>不是胡说，是一个合理但错了的假设</b>：合理在「先用双向 encoder 彻底理解输入、再让 decoder 生成」听起来比「只能从左往右」强；错在「<b>固定算力预算下，encoder 占掉的那一半参数用在 decoder 上收益更大</b>」。⇒ 「<b>算力预算</b>」这个词把问题从「哪个更好」改成了「<b>同样的钱买哪个</b>」—— 两个答案常常不一样，<b>而工程里永远是第二个问题在起作用</b>。★★★ 第三个理由在 2019 年完全看不出来，但回头看很直接：<b>聊天就是「给定前面的对话接着写下一句」，形式上和 next-word prediction 是同一件事；而 BERT 的「填空」和「对话」不对齐 —— 所以 BERT 再强也长不出 ChatGPT</b>。⇒ 教训：<b>预训练任务的「形式」会决定模型最终能变成什么</b>。"},
       {"t": "decoder-only 为什么赢了 encoder-decoder？讲者给的核心理由是什么？",
        "o": ["decoder 的参数利用率更高",
              "比的不是「哪个任务学得更好」而是「哪个更容易扩大规模」—— next-word prediction 下任何文本不经处理就是训练数据",
              "因为 cross-attention 太慢",
              "因为 encoder 无法用 RoPE"],
        "a": 1,
        "w": "★★★ 加上第三个理由：它和「做一个有帮助的聊天机器人」高度对齐 —— 聊天就是「接着前面的对话写下一句」，形式上和 next-word prediction 是同一件事。而 BERT 的「填空」和对话不对齐，所以 BERT 再强也长不出 ChatGPT。"})
