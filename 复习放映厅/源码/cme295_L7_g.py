# -*- coding: utf-8 -*-
"""CME295 L7 模块 g —— 字幕第 339–404 句（39:58–47:46）：给 chunk 补上下文、
prompt caching，以及第二阶段 —— cross-encoder 重排。
"""


def add(KP):

    KP("⭐ 给 chunk 补上下文、prompt caching，与重排",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("40:14","the idea here is to prepend some piece of text that just sums up what you need",166);
  says("40:44","you are going to compute some kind of context that is relevant to each chunk",192);
  note("⭐ 还那个 chunk 的债：给每一块补一句背景",640,222,"y");
  boxNode(60,254,280,46,"整篇文档","v");
  boxNode(360,254,240,46,"要处理的 chunk","b");
  link(600,277,660,277);
  boxNode(660,254,240,46,"LLM 调用","y");
  link(900,277,960,277);
  boxNode(960,254,260,46,"一句简短的背景","g");
  note("⚠ 这句背景拼在 chunk 前面，让它脱离原文也读得懂",640,330,"r");''',
         "<b>前面那个「chunk 切得没道理怎么办」的债，在这里还了。</b><br>⭐ 办法是：<b>在 chunk 前面拼上一小段文字，把「你需要知道什么才读得懂这一块」概括出来</b>。而那段背景怎么来？<b>又是一次 LLM 调用</b>：「<b>把整篇文档和要处理的那个 chunk 一起给模型，然后说：请给我一段简短扼要的背景，好让这个 chunk 说得通</b>」。<br>⚠ 请注意这里的输入是<b>整篇文档 + 这一块</b>:<b>所以这段背景是「从全文视角看这一块」生成的 —— 这正是单独看 chunk 时丢掉的那部分信息</b>。<br>⇒ 而聪明的你应该已经想到问题了：<b>chunk 有几十万个，这得是多少次 LLM 调用</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("41:11","please give me a short succinct context to just make sense of that chunk",166);
  says("41:40","it is called prompt caching",192);
  note("⭐ 「那是很多次 LLM 调用，会非常贵」—— 而有一招压它",640,222,"y");
  boxNode(80,254,500,50,"问题：chunk 极多","r");
  boxNode(700,254,500,50,"办法：prompt caching","g");
  note("每块一次调用 ⇒ 成本爆炸",330,328,"r");
  note("它们的前缀是同一篇文档 —— 算一次就够",950,328,"g");
  note("⚠ 关键观察：这些调用里「整篇文档」那一大段是完全相同的前缀",640,374,"r");''',
         "<b>讲者自己替你把问题提了出来：「那是很多次 LLM 调用，会非常贵」。然后他给了那一招。</b><br>⭐ 关键观察是：<b>给同一篇文档的每个 chunk 生成背景时，每次调用的开头都是「整篇文档」那一大段 —— 它是完全相同的前缀</b>。<br>⚠ 而「<b>prompt caching</b>」这个名字就是在说这件事：<b>相同的前缀没必要一遍遍重算</b>。<br>⇒ 这里值得停一下体会一个<b>解题模式</b>:<b>讲者没有去削减 chunk 数量、也没有换便宜模型，他是去找「这些调用之间有什么是重复的」—— 而在批量 LLM 调用里，「共同前缀」几乎总是存在的</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("41:52","if you use the same prefix for all your prompts, well, it is going to be the same computations",166);
  says("42:18","instead of computing them again, you are just going to look them up",192);
  note("⭐ 为什么同前缀必然同激活 —— 根子在 decoder-only",640,222,"y");
  boxNode(80,254,500,50,"decoder-only ⇒ 只看左边","v");
  boxNode(700,254,500,50,"所以前缀的激活与后文无关","g");
  note("一个 token 只能看到它左边的东西",330,328,"v");
  note("前缀相同 ⇒ 这些层的激活逐位相同",950,328,"g");
  note("⚠ 做法：算一次、把激活存下来，之后只查表，然后解码剩下的",640,374,"r");''',
         "<b>为什么「相同前缀」就能省，根子在架构上 —— 而这一段正好检验你 L1 学到的东西。</b><br>⭐ 推理链条是：<b>这些模型是 decoder-only 的，也就是「只从左往右」⇒ 一个位置的激活只取决于它左边的内容 ⇒ 前缀相同，那一段的各层激活就逐位相同</b>。<br>⭐ 所以做法是：「<b>只算一次，把所有相关的激活存下来；之后不再重算，只做一次查表，然后解码剩下的部分</b>」。<br>⚠ 一个学生追问「<b>这里的激活是指语言模型的激活吗</b>」—— 是的：<b>模型拿到输入要算出所有层的激活，再在生成时对它们做注意力；而既然是只看左边，相同输入必然导致相同激活</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("43:35","this is the same prefix for all your prompts. So what we are going to do is we are just going to make it cheaper for you",166);
  says("43:59","you have the price per cached input token",192);
  note("⭐ 闭源模型也提供这个，而且是写在价目表上的",640,222,"y");
  boxNode(80,254,500,50,"普通输入 token 价","d");
  boxNode(700,254,500,50,"缓存输入 token 价","g");
  note("没被缓存的那些",330,328,"d");
  note("约是前者的十分之一",950,328,"g");
  note("⚠ 所以这不是一个「黑科技」,它是一个你能在定价页上查到的产品特性",640,374,"r");''',
         "<b>这件事不只是你自己部署时能做 —— 闭源服务商把它做成了产品。</b><br>⭐ 「<b>如果你看模型的定价页，你会看到有一个普通输入的价格（也就是没被缓存的输入）,然后有一个每缓存输入 token 的价格 —— 而这里，比如 OpenAI 的模型，它是十分之一的价</b>」。<br>⚠ 所以讲者给了一条非常实际的建议，<b>它对你写任何批量调用的代码都适用</b>：「<b>试着对 prompt 聪明一点 —— 把那些在各个 prompt 之间很可能重复的东西，都收拢到开头</b>」⇒ <b>同样的内容，只是换了个摆放顺序，账单就能差一个量级</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("44:17","try to gather all the things that are likely to be repeated across prompts in the beginning",166);
  says("44:55","now, what we want to do is to sort them in a more meaningful way",192);
  note("⭐ 第一级讲完了，进第二级",640,222,"y");
  boxNode(80,254,500,50,"第一级做到了","g");
  boxNode(700,254,500,50,"第二级要做的","y");
  note("几百万 / 上千万 ⇒ 几百个候选",330,328,"g");
  note("把它们排得更有道理，选出最终的前 k",950,328,"y");
  note("⚠ 它「更偏可选」—— 有时第一刀就够好了",640,374,"r");''',
         "<b>第一级到这里讲完了，开始第二级。</b><br>⭐ 讲者先把两级的分工重述一遍：「<b>到现在为止我们看到了怎么从可能上千上万甚至上百万个 chunk，降到大概几百个潜在相关的 chunk；现在我们要做的是把它们排得更有道理</b>」。<br>⚠ 而他特意说第二级「<b>更偏可选</b>」:「<b>因为有时候第一刀切下来可能就已经够好了 —— 但这第二步是为了在给最终分数时更有意图，好真正选出最终的前 k 个 chunk</b>」。<br>⇒ <b>这个「可选」值得记：如果你的候选集已经很准，加一级重排只是增加延迟和成本</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("45:24","the second stage is called ranking or even re-ranking",166);
  says("46:01","to actually put them both in the encoder, both of them, and have a relevance score out of that",192);
  note("⭐ 第二级的做法：query 和 chunk 一起送进编码器",640,222,"y");
  boxNode(80,254,500,50,"第一级 · bi-encoder","d");
  boxNode(700,254,500,50,"第二级 · 一起进编码器","g");
  note("各编各的，再比两个向量",330,328,"d");
  note("模型同时看到两边，直接吐一个相关性分",950,328,"g");
  note("⚠ 为什么它更有道理：第一级缺的那层「交互」,在这里被补上了",640,374,"r");''',
         "<b>第二级叫 ranking，也叫 re-ranking —— 因为第一级其实已经排过一次了。</b><br>⭐ 做法变了：<b>不再是「分别算 embedding 再比」,而是「把 query 和 chunk 两个一起放进编码器，直接得到一个相关性分数」</b>。<br>⭐ 讲者说清了为什么这更有道理：「<b>你有一个模型同时看着你的 query 和你的 chunk，然后给你一个分数；而第一步里你是一个 query 的 embedding、一个 chunk 的 embedding，没有那种模型能捕捉到的交互</b>」。<br>⚠ 这正是上一块埋的那个伏笔：<b>bi-encoder「两边独立」的那个缺点，在这里被补上了 —— 代价是它再也不能离线预计算</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("46:43","this setup is called cross-encoder setup",166);
  note("⭐ 两个名字放一起记：bi-encoder 与 cross-encoder",640,196,"y");
  boxNode(80,228,500,50,"bi-encoder（第一级）","d");
  boxNode(700,228,500,50,"cross-encoder（第二级）","g");
  note("两边分别进，所以能预先算好",330,302,"d");
  note("两边一起进，所以会算交叉注意力",950,302,"g");
  note("⚠ 「你确实会在两者之间算注意力」—— 这就是「cross」的字面意思",640,348,"r");''',
         "<b>这两个名字放在一起记，一次就记住了。</b><br>⭐ 「<b>你在外面也会看到这个设置叫 cross-encoder，因为你的两个输入都被喂进编码器，所以有一些交叉的交互</b>」—— 而第一级那个叫 <b>bi-encoder</b>。<br>⚠ 一个学生直接问到了点子上：「<b>你其实会在两者之间计算注意力</b>」—— 讲者答「<b>是的，绝对是</b>」。<b>这就是「cross」的字面含义：query 的 token 和 chunk 的 token 在注意力里互相看得到</b>。<br>⇒ 而这也立刻解释了成本：<b>每一个候选都要跑一次完整的编码器前向 ⇒ 所以它只能用在「几百个」这个量级上，不可能用在几百万上</b>。讲者推荐去读 <b>sentence transformers 的文档</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("47:13","you will actually compute the attention between the two",166);
  says("47:46","and then you finally obtain the ranking",192);
  note("⭐ 对每个候选都算一遍，得到最终排序",640,222,"y");
  boxNode(80,254,500,50,"每个候选 chunk × prompt","g");
  link(580,279,700,279);
  boxNode(700,254,500,50,"一个分数 ⇒ 排序 ⇒ 前 k","y");
  note("「现在的问题是：你对这个排序满意吗？」",640,330,"y");
  note("⚠ 而要回答这个问题，你需要一个量化表现的办法 —— 下一块四个指标",640,374,"r");''',
         "<b>把这个分数对每一个候选都算一遍，最终排序就出来了。</b><br>⭐ 「<b>你对所有潜在相关的 chunk 都做这件事，于是每个 chunk 和 prompt 之间都有了一个分数，然后你终于得到了排序</b>」。<br>⚠ 而讲者紧接着提的那个问题，是下一块的入口：「<b>现在的问题是，你对这个排序满意吗？而要回答这个问题，你需要一个量化你表现的办法</b>」。<br>⇒ <b>请注意这个顺序：先把方法讲完，再问「怎么知道它好不好」—— 这是 L4 到 L6 一直在重复的那件事；而他说「接下来五分钟」看指标，实际讲了四个</b>。", 0)],
       {"h": "⭐ 补上下文 · 缓存 · 重排",
        "k": "给 chunk 补上下文：<b>「这里的想法是在前面拼上一小段文字，把你需要知道的东西概括出来，好理解那个 chunk」—— 做法是「把整篇文档和要处理的那个 chunk 一起给模型：请给我一段简短扼要的背景，好让这个 chunk 说得通」</b>。<br>prompt caching：<b>「那是很多次 LLM 调用，会非常贵」⇒ 「它叫 prompt caching」; 「如果你对所有 prompt 用同样的前缀，那就是同样的计算一遍一遍又一遍 ⇒ 只做一次、把所有相关的激活存下来，之后不再重算，只做一次查表，然后解码剩下的」</b>；而闭源服务商把它产品化了：<b>「如果你看模型的定价页，你会看到有普通输入的价格，然后有每缓存输入 token 的价格 —— 比如 OpenAI 的是十分之一的价」⇒ 「试着对 prompt 聪明一点，把那些很可能在各 prompt 之间重复的东西都收拢到开头」</b>。<br>第二级：<b>「第二阶段叫 ranking，甚至叫 re-ranking」,「它更偏可选，因为有时候第一刀可能就够好了」;做法是「把 query 和 chunk 两个都放进编码器，直接得到一个相关性分数」—— 「你有一个模型同时看着 query 和 chunk，而第一步里没有那种交互」; 「这个设置叫 cross-encoder」,而「你确实会在两者之间计算注意力」⇒ 「对所有候选都做一遍，然后你终于得到了排序」</b>。",
        "m": "⭐ prompt caching 为什么成立，根子在架构上：<b>decoder-only ⇒ 只从左往右 ⇒ 一个位置的激活只取决于它左边的内容 ⇒ 前缀相同，那一段的各层激活逐位相同</b>。<br>⭐ 而这里有一个值得抄的<b>解题模式</b>:<b>讲者没有去削减 chunk 数量、也没有换便宜模型，他去找「这些调用之间有什么是重复的」—— 而在批量 LLM 调用里，「共同前缀」几乎总是存在的 ⇒ 同样的内容只是换个摆放顺序，账单就能差一个量级</b>。<br>⭐ 第二级补的正是第一级缺的那层<b>交互</b>:<b>bi-encoder 两边独立所以能离线预算（便宜）,cross-encoder 两边一起进所以能算交叉注意力（准）—— 代价是每个候选都要跑一次完整前向，只能用在几百个这个量级上</b>。",
        "w": " 给 chunk 补背景时，输入是<b>整篇文档 + 这一块</b>:<b>所以那段背景是「从全文视角看这一块」生成的 —— 正是单独看 chunk 时丢掉的那部分信息</b>。<br>⚠ 而第二级「<b>更偏可选</b>」这句话值得记：<b>如果你的候选集已经很准，加一级重排只是增加延迟和成本</b>。<br>⚠ 「cross」是字面意思：<b>query 的 token 和 chunk 的 token 在注意力里互相看得到</b>。",
        "r": "⇒ prompt caching 那条建议对你写任何批量调用的代码都适用：<b>把跨 prompt 重复的部分收拢到最前面</b>。<br>⇒ 而「先把方法讲完，再问『怎么知道它好不好』」这个顺序，<b>是 L4 到 L6 一直在重复的那件事</b> —— 讲者说「接下来五分钟」看指标，实际讲了四个。<br>⇒ 更多（contextual retrieval 原始做法、KV cache 与 prompt caching 的关系、sentence transformers 文档）见<b>深度笔记</b>。",
        },
       {"t": "prompt caching 为什么能成立？而 cross-encoder 和 bi-encoder 的本质差别是什么？",
        "o": ["因为缓存了磁盘读写；两者只是名字不同",
              "因为 decoder-only 只看左边 ⇒ 前缀相同则那一段各层激活逐位相同，算一次存下来之后只查表；而 bi-encoder 两边分别进编码器（所以能离线预算、便宜），cross-encoder 两边一起进（所以能算交叉注意力、更准，但每个候选都要跑一次前向）",
              "因为 token 化可以复用；两者差在模型大小",
              "因为注意力是线性的；两者差在用不用 ANN"],
        "a": 1,
        "w": "⇒ 所以 cross-encoder 只能用在「几百个候选」这个量级上，不可能用在几百万上 —— 这正是两阶段结构存在的理由。"})
