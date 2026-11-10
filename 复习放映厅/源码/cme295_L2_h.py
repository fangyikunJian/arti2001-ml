# -*- coding: utf-8 -*-
"""CME295 L2 模块 h —— 字幕第 533–610 句（62:46–71:45）：Shervine 接手下半场 ——
三类架构。① encoder-decoder 与 T5 家族（mT5 / ByT5）、span corruption 与 sentinel token；
② encoder-only（不能生成，而那正是重点）；③ decoder-only，以及它为什么赢了。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（20 镜 → 10 镜）。
⚠ 旁白里不许出现半角双引号；setEq 里反斜杠写双份。
"""


def add(KP):

    KP("⭐ Shervine 接手：三类架构，先看 T5 家族",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("62:46","we are going to continue this lecture with some deeper dive into the kinds of models",166);
  says("63:38","So T5 is a paper that is an abbreviation of multiple Ts",192);
  note("⭐ 下半场两件事，以及一个最容易被误解的名字",640,222,"y");
  boxNode(80,254,500,50,"① 把 transformer 格局里的模型分类","b");
  boxNode(700,254,500,50,"② 对一个偏分类的架构做深入","g");
  note("⇒ T5 ＝ Transfer Text-to-Text Transformer",330,328,"v");
  note("⚠ 不是「第五代」,那个 5 只是数 T 的个数",950,328,"r");
  note("⭐ 而 Text-to-Text 是真正的卖点：所有任务都改写成「文本进、文本出」",640,374,"y");''',
         "<b>换人了，而下半场的两件事他说得很清楚。</b><br>⭐ 「<b>我们要继续这一讲，对 transformer 格局里我们有的那些种类的模型做一些更深的深入。然后我们要对一个特定的、对分类场景非常有用的架构做一次深入</b>」。<br>⭐ 第一类是 encoder-decoder，代表是 T5：「<b>T5 是一篇论文，它是多个 T 的缩写 —— 第一个是 transfer，然后是 text-to-text，transformers。所以这就是 T5 这个命名的来处</b>」 ⇒ <b>拆开来是 Transfer Text-to-Text Transformer，所以那个 5 只是数 T 的个数，不是「第五代」</b>。<br>⭐ 而 <b>Text-to-Text</b> 是真正的卖点：<b>翻译、分类、摘要、问答全都改写成「文本进、文本出」,于是一个模型一套训练流程就能做所有任务</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("64:02","And then it had mT5. m stands for multilingual",166);
  says("64:14","And then you have ByT5",192);
  note("⭐ 两个派生版本，而两处改动都不在模型结构上",640,222,"y");
  boxNode(80,254,500,50,"mT5：multilingual","b");
  boxNode(700,254,500,50,"ByT5：byte —— 免 tokenizer","v");
  note("改的是训练数据，和词表在什么上面算",330,328,"b");
  note("⇒ 直接在字节层面操作",950,328,"v");
  note("⚠ 这正好回答了 L1 那整段 tokenization 的讨论：那一层可以整个拿掉",640,374,"r");''',
         "<b>两个派生版本，而讲者点出的改动都不在模型结构上。</b><br>⭐ 「<b>T5 就像是那个原味的论文。然后它有了 mT5 —— m 代表 multilingual（多语言）,那里在它被训练的数据上做了更多工作，以及在词表是在什么上面被计算出来的这件事上</b>」 ⇒ <b>同一个架构，换数据、换词表，就是一个新模型 —— 这在那几年是非常典型的做法</b>。<br>⭐ 而第二个变体很激进：「<b>然后你有 ByT5，它是某种免 tokenizer 的方法 —— 你放弃了做 tokenization 这件事，取而代之你基本上在字节的层面上操作。所以 By 就是 byte</b>」 ⇒ <b>回想 L1 里那整段关于 tokenization 的讨论（BPE、OOV、拼写错误）—— ByT5 的回答是：那一层可以整个拿掉</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("64:33","So instead of having an o of 30k, you have 2 to the power of 8",166);
  says("65:03","the objective function changes a bit with what the original transformer did",192);
  note("⭐⭐ 这个数字对比很有冲击力，而它顺带解释了参数量去哪儿了",640,222,"y");
  boxNode(80,254,500,50,"词表 3 万 × d_model","b");
  boxNode(700,254,500,50,"⇒ 变成 256 × d_model","g");
  note("嵌入表动辄上千万参数",330,328,"b");
  note("⇒ 几乎可以忽略",950,328,"g");
  note("⚠ 代价是序列变长好几倍 —— 而注意力是 n² ⇒ 省下的参数用算力还回去了",640,374,"r");''',
         "<b>这个数字对比很有冲击力，而它顺带解释了参数量去哪儿了。</b><br>⭐ 「<b>你有一个小得多的词表大小。所以与其有 3 万这个量级，你有 2 的 8 次方 —— 因为一个字节是 8 比特。然后你可以把每一个字符都表示成字节</b>」 ⇒ <b>嵌入表的大小是「词表 × d_model」,3 万词表动辄上千万参数；而 256 行的表几乎可以忽略</b>。<br>⚠ 但代价很实在：<b>一个字节一个 token，序列长度要变长好几倍 —— 而注意力是 n² ⇒ 省下来的参数，用算力还回去了。这就是为什么免 tokenizer 的路线至今没有成为主流</b>。<br>⭐ 然后是关于 T5 最该记住的一件事：「<b>目标函数和原始 transformer 做的那个有一点变化</b>」。", 0)],
       {"h": "⭐ T5 家族",
        "k": "<b>「所以我们要继续这一讲，对 transformer 格局里我们有的那些种类的模型做一些更深的深入。然后我们要对一个特定的、对分类场景非常有用的架构做一次深入」; 「所以这里我们讲 T5 这个模型家族。T5 是一篇论文，它是多个 T 的缩写。所以第一个是 transfer，然后是 text-to-text，transformers。所以这就是 T5 这个命名的来处」</b>。<br>⭐ 两个派生：<b>「然后它有了 mT5 —— m 代表 multilingual，那里在它被训练的数据上做了更多工作，以及在词表是在什么上面被计算出来的这件事上」; 「然后你有 ByT5，它是某种免 tokenizer 的方法 —— 在这里你放弃了「做 tokenization」这件事。而取而代之，你基本上在字节的层面上操作。所以 By 就是 byte」; 「而基本上，你有一个小得多的词表大小。所以与其有 3 万这个量级，你有 2 的 8 次方 —— 因为一个字节是 8 比特」</b>;以及：<b>「关于 T5 家族我想提的一件事是：目标函数和原始 transformer 做的那个有一点变化」</b>。",
        "m": "⭐ T5 的名字拆开是 <b>Transfer Text-to-Text Transformer</b>——<b>那个 5 只是数 T 的个数，不是「第五代」; 而 Text-to-Text 是真正的卖点：翻译、分类、摘要、问答全都改写成「文本进、文本出」,一个模型一套流程做所有任务</b>。<br>⭐⭐ ByT5 的账要两边一起算：<b>嵌入表从「3 万 × d_model」（上千万参数）降到「256 × d_model」（几乎可忽略）; 但一个字节一个 token，序列长好几倍，而注意力是 n² ⇒ 省下的参数用算力还回去了</b>。<br>⭐ 而 mT5 说明了那几年一个典型的做法：<b>同一个架构，换数据、换词表，就是一个新模型</b>。",
        "w": " ByT5 正好回答了 L1 那整段关于 tokenization 的讨论：<b>BPE、OOV、拼写错误这些麻烦全都来自那一层 —— 而 ByT5 的回答是「那一层可以整个拿掉」。但它至今没成主流，原因就是上面那笔算力账</b>。<br>⚠ 而嵌入表的大小是「<b>词表 × d_model</b>」这件事值得记住：<b>它解释了为什么多语言模型的参数量看起来虚高 —— 很大一块在嵌入表里</b>。",
        "r": "⇒ 「一个模型做所有任务」这个思路在今天已经是常识（所有任务都写成 prompt）,<b>而 T5 是最早把它当成架构卖点的那一批</b>。<br>⇒ 更多（T5 各尺寸的参数分布、ByT5 的实测长度膨胀、mT5 的词表构造）见<b>深度笔记</b>。",
        },
       {"t": "ByT5 的「免 tokenizer」路线省下了什么、代价是什么？",
        "o": ["省下了注意力的计算，代价是嵌入表变大",
              "省下了嵌入表（词表从 3 万降到 256，上千万参数变成几乎可忽略）;代价是一个字节一个 token、序列长好几倍，而注意力是 n² ⇒ 省下的参数用算力还回去了，所以这条路至今不是主流",
              "省下了位置编码，因为字节天然有序",
              "两边都省，所以它应该早就取代 BPE 了"],
        "a": 1,
        "w": "⇒ 而 T5 这个名字拆开是 Transfer Text-to-Text Transformer —— 那个 5 只是数 T 的个数。"})

    KP("⭐ span corruption：T5 换掉了训练目标",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("65:33","instead of putting everything to the encoder, you would leave blanks",166);
  says("65:44","so for example, my teddy bear is cute and reading",192);
  note("⭐⭐ 关键在那个「片段」:缺的不是一个词，是一整段",640,222,"y");
  boxNode(80,254,500,50,"原始 transformer：next token prediction","d");
  boxNode(700,254,500,50,"T5：span corruption（挖空重建）","y");
  note("⇒ 挖掉 my teddy bear，留下 is reading",330,328,"y");
  note("⚠ 一个空位可以对应任意长度的内容",950,328,"r");
  note("⭐ 而这个难度是刻意的：猜一个词靠局部搭配，补一整段要理解整句",640,374,"g");''',
         "<b>做法本身很直观，而关键在那个「片段」上。</b><br>⭐ 「<b>你会有你的句子作为 encoder 的输入。而不是把所有东西都放进 encoder，你会留下一些空白。而这就是我们叫做 span corruption 的东西。然后这个 span corruption 可以是一个、也可以是多个 token 缺失</b>」; 例子还是那句招牌：「<b>比如说 my teddy bear is cute and reading，那么你可以把「my teddy bear」这段 span corrupted 掉，然后留下「is reading」</b>」。<br>⭐⭐ 挖掉的是<b>一整段</b>而不是一个词，<b>而这个难度是刻意的：猜一个被挖掉的词往往靠局部搭配就够了，而补一整段必须理解整句在说什么 —— 一个空位可以对应任意长度的内容</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("66:14","And then the T5 families calls them sentinel tokens",166);
  says("66:26","to find each of these spans in series",192);
  note("⭐⭐ 术语，以及 span corruption 最精巧的那一半：输出端",640,222,"y");
  boxNode(80,254,500,50,"输入：<X> is reading","b");
  boxNode(700,254,500,50,"输出：<X> my teddy bear <Y>","g");
  note("一个符号代表一整段",330,328,"b");
  note("⇒ decoder 只输出缺的部分，不重复原文",950,328,"g");
  note("⚠ 而下一个 sentinel token 就是「这一段讲完了」的信号 —— 长度由模型自己决定",640,374,"r");''',
         "<b>这是该记住的那个术语，而它的妙处在于「一个符号代表一整段」。</b><br>⭐ 「<b>n 是「被损坏的 span 的数量」那个参数化⋯⋯T5 家族把它们叫做 sentinel tokens</b>」; 而输出端是：「<b>decoder 的工作就是按序把这些 span 一个个找出来 —— 你从一个标示第一个被损坏 span 的 token 开始，然后开始解码过程，直到它碰到一个预测出「下一个 sentinel token」的预测</b>」。<br>⭐⭐ 这一半很精巧：<b>decoder 只输出缺掉的那些片段，不重复原文 —— 而每一段的结束信号就是「下一个 sentinel token」, 于是每段的长度由模型自己决定。这比「告诉模型这里缺 3 个词」难得多，也更接近真实的理解</b>。", 0)],
       {"h": "⭐ span corruption",
        "k": "<b>「所以基本上你会有你的句子作为 encoder 的输入。而不是把所有东西都放进 encoder，你会留下一些空白。而这就是我们叫做 span corruption 的东西。然后这个 span corruption 可以是一个、也可以是多个 token 缺失」; 「所以如果我想举个例子 —— 比如说，my teddy bear is cute and reading。那么你可以把「my teddy bear」这段 span corrupted 掉，然后留下「is reading」」; 「然后 T5 家族把它们叫做 sentinel tokens」; 「然后 decoder 的工作就是按序把这些 span 一个个找出来。所以你从一个标示第一个被损坏 span 的 token 开始，然后你开始解码过程，直到它碰到一个预测出「下一个 sentinel token」的预测」</b>。",
        "m": "⭐⭐ 关键在「<b>片段</b>」:<b>挖掉的是一整段而不是一个词 ⇒ 猜一个被挖掉的词往往靠局部搭配就够，而补一整段必须理解整句在说什么；而且一个空位可以对应任意长度的内容</b>。<br>⭐⭐ 输出端是最精巧的那一半：<b>decoder 只输出缺掉的片段、不重复原文，而每段的结束信号就是「下一个 sentinel token」⇒ 每段的长度由模型自己决定，这比「告诉它这里缺 3 个词」难得多</b>。<br>⭐ 而 sentinel token 的妙处是<b>一个符号代表一整段</b>:<b>输入 <X> is reading、输出 <X> my teddy bear <Y> —— 输入和输出用同一套符号对齐</b>。",
        "w": " 这个目标函数的难度是<b>刻意的</b>:<b>它强迫模型去用双向的上下文（左边和右边都在），而这正是 encoder 的长处 —— 所以 span corruption 和 encoder-decoder 架构是配套的设计，不是随便换的</b>。<br>⚠ 而 next token prediction 只能看左边：<b>所以 decoder-only 模型不可能用这个目标函数训练</b>。",
        "r": "⇒ 这件事在八分钟后会变成一个关键论据：<b>decoder-only 赢了的理由之一，就是 next-word prediction 比 span corruption「更容易扩大规模」—— 而那正是因为后者需要你去设计「怎么损坏」</b>。<br>⇒ 更多（T5 的损坏比例与片段长度超参、BERT 的 MLM 与它的区别）见<b>深度笔记</b>。",
        },
       {"t": "T5 的 span corruption 和「下一个 token 预测」比，难在哪里？",
        "o": ["难在要预测的 token 更多，所以算得更慢",
              "难在挖掉的是一整段而不是一个词：补一整段必须理解整句在说什么，而且一个空位可以对应任意长度的内容 —— 每段何时结束由模型自己决定（信号是下一个 sentinel token）",
              "难在 sentinel token 不在词表里，需要额外训练",
              "难在 decoder 必须把原文也一起重复输出一遍"],
        "a": 1,
        "w": "⇒ 而这个难度是刻意的：它强迫模型用双向上下文，而那正是 encoder 的长处 —— 所以 span corruption 和 encoder-decoder 架构是配套设计。"})

    KP("⭐ 那个括号、teacher forcing，与「忘掉 decoder」",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:03","So these parentheses is basically a shift from the next token prediction objective function",166);
  says("67:34","So you have sentinel tokens that denote some missing text",192);
  note("⭐ 他用的词是「转变」,而不是「改进」—— 这个中性很准确",640,222,"y");
  boxNode(80,254,500,50,"没说 improvement","d");
  boxNode(700,254,500,50,"也没说 complication","d");
  note("⇒ 只是「不一样」",330,328,"v");
  note("⚠ 而历史给了答案：换掉的这一步后来被放弃了",950,328,"r");
  note("⭐ 学生要求复述解码过程，而讲者当场确认：你说的完全正确",640,374,"g");''',
         "<b>这一镜很短，但讲者的用词值得留意。</b><br>⭐ 「<b>所以这些括号基本上是对 next token prediction 这个目标函数的一个转变</b>」 ⇒ <b>「转变（shift）」是中性的：他没说 improvement（改进）, 也没说 complication（复杂化）, 只是「不一样」—— 而在一门课里，对一个后来被主流放弃的设计保持这种中性，是很专业的态度</b>。<br>⭐ 然后学生要求把解码过程再说一遍，而讲者的复述把这件事钉死了：「<b>你刚才说的关于重建那部分完全正确。所以你有 sentinel token，它们标示某些缺失的文本。所以你想要解码出来的就是那段缺失的文本</b>」 ⇒ <b>decoder 的任务不是重建整句，只是把那些洞填上</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("67:50","you do a teacher-forcing mechanism where you input everything in the decoder",166);
  says("68:18","you just forget about the decoder and then just deal with the encoder",192);
  note("⭐⭐⭐ teacher forcing 解释了训练和推理为什么看起来完全不同",640,222,"y");
  boxNode(80,254,500,50,"训练：把正确答案整段喂进 decoder","g");
  boxNode(700,254,500,50,"推理：只能一个个往外吐","r");
  note("⇒ 所有位置并行算，一次重建全部",330,328,"g");
  note("⇒ 上一步错了，后面就顺着错下去",950,328,"r");
  note("⭐ 而第二类架构：干脆忘掉 decoder ——「你这样没法做生成啊」「是的，那正是重点」",640,374,"v");''',
         "<b>这是一个很重要的机制，而它解释了训练和推理为什么看起来完全不同。</b><br>⭐ 「<b>如果你想知道训练是怎么工作的 —— 你做一个 teacher-forcing 机制，在那里你把所有东西都输入到 decoder 里，然后试着一次性把所有东西重建出来</b>」 ⇒ <b>训练时把正确答案整段喂进 decoder（配上因果掩码）, 所有位置并行算；而推理时没有正确答案，只能一个个往外吐，上一步错了后面就顺着错下去 —— 这个差距叫 exposure bias</b>。<br>⭐ 然后是第二类架构，而这段对话很漂亮：「<b>你有这个 encoder/decoder 结构，而你干脆忘掉 decoder，只处理 encoder。所以你可能会跟我说：好，嘿，你这样没法做生成啊。而我会回答你：是的，那正是重点</b>」。", 0)],
       {"h": "⭐ teacher forcing 与「忘掉 decoder」",
        "k": "<b>「所以这些括号基本上是对 next token prediction 这个目标函数的一个转变」</b>;学生要求复述解码过程，回答：<b>「所以你刚才说的关于重建那部分完全正确。所以你有 sentinel token，它们标示某些缺失的文本」</b>;训练机制：<b>「然后如果你想知道训练是怎么工作的 —— 你做一个 teacher-forcing 机制，在那里你把所有东西都输入到 decoder 里，然后试着一次性把所有东西重建出来」</b>。<br>⭐ 第二类架构：<b>「然后现在我们要讲另一类 transformer —— 基本上你有这个 encoder/decoder 结构，而你干脆忘掉 decoder，只处理 encoder。所以你可能会跟我说：好，嘿，你这样没法做生成啊。而我会回答你：是的，那正是重点」</b>。",
        "m": "⭐⭐⭐ <b>teacher forcing</b> 解释了训练和推理为什么看起来完全不同：<b>训练时把正确答案整段喂进 decoder（配因果掩码）,所有位置并行算、一次重建全部；推理时没有正确答案，只能一个个往外吐，上一步错了后面顺着错下去 ⇒ 这个差距叫 exposure bias</b>。<br>⭐ 而「<b>转变（shift）</b>」这个中性用词很准确：<b>他没说 improvement 也没说 complication —— 而历史给了答案：这一步后来被主流放弃了</b>。<br>⭐ 「<b>是的，那正是重点</b>」这句翻转很漂亮：<b>不能生成不是缺陷，它是分工 —— encoder-only 的目标从来不是生成</b>。",
        "w": " decoder 的任务不是重建整句，<b>只是把那些洞填上</b>——<b>所以输出序列比输入短得多，而这也是 span corruption 效率上的一个好处</b>。<br>⚠ 而 teacher forcing 不是 T5 独有的：<b>所有自回归模型的训练都这么做 —— 它是「训练能并行、推理不能并行」这个根本不对称的来源</b>。",
        "r": "⇒ exposure bias 这个词值得记住：<b>它是后来一大批工作（scheduled sampling、强化学习微调）要解决的问题 —— 而今天 RLHF 之所以有效，一部分原因也在这里</b>。<br>⇒ 更多（因果掩码与并行训练的细节、exposure bias 的缓解手段）见<b>深度笔记</b>。",
        },
       {"t": "teacher forcing 是什么，它造成了什么后果？",
        "o": ["它是一种让老师模型指导学生模型的蒸馏方法",
              "它是训练时把正确答案整段喂进 decoder（配因果掩码）、所有位置并行算；而推理时没有正确答案、只能一个个往外吐，上一步错了后面顺着错下去 —— 这个训练与推理的差距叫 exposure bias",
              "它是在损失里强制对齐 encoder 和 decoder 的表示",
              "它只在 T5 这类 encoder-decoder 模型里出现，decoder-only 不用"],
        "a": 1,
        "w": "⇒ 而它是「训练能并行、推理不能并行」这个根本不对称的来源 —— 所有自回归模型的训练都这么做。"})

    KP("⭐⭐ encoder-only，以及 decoder-only 为什么赢了",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("68:37","it has encoder representations that can be used for tasks that might be more geared towards classification",166);
  says("69:10","So BERT, which is like the central one, I would say in this landscape",192);
  note("⭐ encoder-only 的用途，以及下半场的三个主角",640,222,"y");
  boxNode(60,254,360,50,"BERT：这个格局里最中心的","g");
  boxNode(460,254,360,50,"DistilBERT","b");
  boxNode(860,254,360,50,"RoBERTa","b");
  note("情感抽取、token 分类",240,328,"g");
  note("⇒ 两条「改进的轴」上的探索",840,328,"b");
  note("⚠ 过去要用专门的语言模型来做的事，现在都能用 transformer 的 encoder 做",640,374,"v");''',
         "<b>这一镜给出了 encoder-only 的用途，而讲者那句定位最值得记。</b><br>⭐ 「<b>它有 encoder 的表示，这些表示可以用在那些可能更偏向分类的任务上。所以情感抽取、token 分类、所有这些过去要用专门的语言模型来做的事情 —— 它们都能用 transformer 的 encoder 部分来做</b>」 ⇒ <b>关键是「过去要用专门的语言模型」:在 BERT 之前，每个任务都要自己训一个模型；而 BERT 之后，一个预训练 encoder 加一个小分类头就够了</b>。<br>⭐ 而下半场的三个主角公布了：「<b>BERT —— 我会说它是这个格局里最中心的那个 —— 然后另外两个架构，DistilBERT 和 RoBERTa，它们是在若干条改进的轴上做探索的</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("69:40","when you have no encoder, you do not have your encoder embeddings",166);
  says("70:17","the main hypothesis was that the encoder part is very useful",192);
  note("⭐⭐ 第三类架构，而它的结构简洁到让人意外",640,222,"y");
  boxNode(80,254,500,50,"没有 encoder ⇒ 没有 encoder 嵌入","b");
  boxNode(700,254,500,50,"⇒ cross-attention 这个模块整个消失","r");
  note("每个 block 只剩：带掩码自注意力 ＋ FFN",330,328,"b");
  note("⚠ 而那场转向的本质是：一个假设被推翻了",950,328,"r");
  note("⭐ 那个假设是「encoder 那部分对拿到 decoder 的表示非常有用」",640,374,"y");''',
         "<b>第三类架构，而它的结构简洁到让人意外。</b><br>⭐ 「<b>今天的 LLM 把 encoder 那部分整个去掉了。而当你没有 encoder 时，你在你那堆叠起来的 encoder 的末端就没有 encoder 嵌入可以喂给 cross-attention。所以这个模块整个消失了</b>」 ⇒ <b>于是每个 block 只剩两样：带掩码自注意力 ＋ FFN。L1 里那个三层 block（自注意力、交叉注意力、FFN）在今天的模型里只剩两层</b>。<br>⭐⭐ 而那场转向的本质是一个<b>假设被推翻</b>:「<b>你过去有这种类似 transformer 的架构，它在一开始很流行，那时主要的假设是：encoder 那部分对于得到 decoder 的表示非常有用。但随着时间过去，人们意识到⋯⋯</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("70:44","easiest to scale up and generalize",166);
  says("71:05","it proved to be wonders and well-aligned with the task of being a helpful kind of chatbot",192);
  note("⭐⭐⭐ 两个理由，而第一个比「简单就是好」要深",640,222,"y");
  boxNode(80,254,500,50,"① 最容易扩大规模和泛化","g");
  boxNode(700,254,500,50,"② 恰好和「做个有帮助的聊天机器人」对齐","y");
  note("任何一段文本都是现成的训练样本",330,328,"g");
  note("⇒ 而这一点是很难事先预料到的",950,328,"y");
  note("⚠ 对照 span corruption：你得先决定损坏什么、损坏多少 —— 那是要设计的",640,374,"r");''',
         "<b>这是整段最该记住的一镜，而第一个理由比「简单就是好」要深。</b><br>⭐ 「<b>有更多的投入流向了那种我会说「最容易扩大规模和泛化」的任务 —— next-word prediction —— 而不是我刚为 T5 提到的那个任务，那个可能更定制。所以你得去损坏一些东西</b>」 ⇒ <b>next-word prediction 不需要任何设计：任何一段文本都是现成的训练样本；而 span corruption 要你先决定损坏什么、损坏多少、片段多长 —— 那是超参，而超参是扩规模的摩擦</b>。<br>⭐ 第二个理由很难事先预料：「<b>它被证明创造了奇迹，而且和「做一个有帮助的那种聊天机器人」这个任务高度对齐 —— 而那基本上就是今天主要的应用</b>」。", 0)],
       {"h": "⭐⭐ decoder-only 为什么赢了",
        "k": "<b>「所以它有 encoder 的表示，这些表示可以用在那些可能更偏向分类的任务上。所以情感抽取、token 分类、所有这些过去要用专门的语言模型来做的事情 —— 它们都能用 transformer 的 encoder 部分来做」; 「所以 BERT —— 我会说它是这个格局里最中心的那个 —— 然后另外两个架构，DistilBERT 和 RoBERTa，它们是在若干条改进的轴上做探索的」</b>。<br>⭐ 第三类：<b>「就像 Afshine 刚提到的，今天的 LLM 把 encoder 那部分整个去掉了。而当你没有 encoder 时，你在你那堆叠起来的 encoder 的末端就没有 encoder 嵌入可以喂给 cross-attention。所以这个模块整个消失了」; 「那时主要的假设是：encoder 那部分对于得到 decoder 的表示非常有用。但随着时间过去，人们意识到⋯⋯」; 「然后有更多的投入流向了那种我会说「最容易扩大规模和泛化」的任务 —— next-word prediction —— 而不是我刚刚为 T5 提到的那个任务，那个可能更定制。所以你得去损坏一些东西」; 「而它被证明创造了奇迹，而且和「做一个有帮助的那种聊天机器人」这个任务高度对齐 —— 而那基本上就是今天主要的应用」</b>。",
        "m": "⭐⭐ decoder-only 的结构简洁到让人意外：<b>没有 encoder ⇒ 没有 encoder 嵌入 ⇒ cross-attention 整个消失 ⇒ 每个 block 只剩「带掩码自注意力 ＋ FFN」—— L1 里那个三层 block 在今天只剩两层</b>。<br>⭐⭐⭐ 第一个理由比「简单就是好」要深：<b>next-word prediction 不需要任何设计，任何一段文本都是现成的训练样本；而 span corruption 要你先决定损坏什么、损坏多少、片段多长 ⇒ 那是超参，而超参是扩规模的摩擦</b>。<br>⭐ 第二个理由是运气成分：<b>「和做一个有帮助的聊天机器人这个任务高度对齐」—— 这件事在 2018 年几乎不可能预料到</b>。",
        "w": " encoder-only 的价值在那句「<b>过去要用专门的语言模型来做的事情</b>」里：<b>在 BERT 之前每个任务都要自己训一个模型；BERT 之后，一个预训练 encoder 加一个小分类头就够了 —— 这才是那一代的真正贡献</b>。<br>⚠ 而「那正是重点」这句翻转要记住：<b>不能生成不是缺陷，它是分工</b>。",
        "r": "⇒ 这一讲的收口很清楚：<b>上半场讲了八年里变过的三个部件（位置编码、归一化、注意力）, 下半场讲了三类架构，而赢的那一类是结构最简单、训练目标最不需要设计的那一类</b>。<br>⇒ 而 decoder-only 的细节是后面几讲的核心内容，<b>这里只需要带走那两个理由</b>。<br>⇒ 更多（那个假设被推翻的实证过程、三类架构的流行度曲线）见<b>深度笔记</b>。",
        },
       {"t": "讲者给的「decoder-only 赢了」的两个理由是什么？",
        "o": ["① 参数更少所以更便宜；② 不需要位置编码",
              "① next-word prediction「最容易扩大规模和泛化」——任何一段文本都是现成样本，而 span corruption 要你先决定损坏什么、多少、多长（超参是扩规模的摩擦）;② 它恰好和「做一个有帮助的聊天机器人」这个任务高度对齐",
              "① encoder 在数学上被证明是冗余的；② 分类任务不再重要了",
              "① decoder 可以用 KV cache 而 encoder 不能；② 它支持更长的上下文"],
        "a": 1,
        "w": "⇒ 而被推翻的那个假设是「encoder 那部分对于得到 decoder 的表示非常有用」; 结构上，cross-attention 整个消失，每个 block 只剩带掩码自注意力 ＋ FFN。"})
