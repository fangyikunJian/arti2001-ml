# -*- coding: utf-8 -*-
"""CME295 L7 模块 i —— 字幕第 471–521 句（54:09–59:21）：另外三个指标（MRR、
recall@k、precision@k）、MTEB，以及上半场收尾的两个提问与交棒。
"""


def four(cur):
    labs = ("NDCG", "MRR", "precision@k", "recall@k")
    out = ""
    for i, lab in enumerate(labs):
        cls = '"y"' if (i + 1) == cur else '"d"'
        out += '  boxNode(%d,228,250,46,"%s",%s);\n' % (90 + i * 270, lab, cls)
    return out


def add(KP):

    KP("⭐ 另外三个指标、MTEB，与交棒",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("54:09","you have another one that is called the reciprocal rank",166);
  says("54:19","it takes the inverse of the highest rank of all the relevant documents",192);
  note("⭐ 第二个指标：MRR —— 简单得多",640,222,"y");
  seq(110,254,["第 1 位 · 不相关","第 2 位 · 相关","第 3 位 · 相关","…"],"d",250,48);
  note("第一个相关文档排在第 2 位 ⇒ 分数就是 1/2，后面全不看",640,332,"y");
  note("⚠ 它只关心「第一条对的在第几位」—— 这既是它的简单，也是它的盲区",640,374,"r");''',
         "<b>第二个指标叫 reciprocal rank，而它比 NDCG 简单得多。</b><br>⭐ 「<b>它取所有相关文档里名次最高的那个的倒数 —— 比如在你的前 k 个里，第一个相关文档出现在第 2 位，那 rank 就等于 2</b>」⇒ 分数是 1/2。<br>⚠ 而讲者点出了它的盲区：「<b>它基本上不关心第一个相关文档之后的任何相关文档</b>」。<br>⇒ 那为什么还用它？他的理由很实在：「<b>这是一个更简单的指标，而它典型地相关性很好 —— 所以人们用它</b>」。<b>「和复杂指标高度相关、而且便宜」是指标被采用的常见理由，这一点值得记</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("55:14","it takes a look at all the actually positive observations",166);
  note("⭐ 第三个：recall@k —— 它就是你学过的那个召回率",640,196,"y");
  boxNode(80,228,500,50,"分母：所有「实际相关」的文档","v");
  boxNode(700,228,500,50,"分子：其中落进前 k 的","g");
  note("「在所有实际为正的样本里，你真的预测为正的是哪些」",640,304,"y");
  note("⚠ 它正是第一级那条规矩的量化版 —— 「漏没漏」就是用它量的",640,348,"r");''',
         "<b>第三个指标就是你早就学过的召回率，只是换到排序场景。</b><br>⭐ 讲者先复述了二分类版本：「<b>recall 看的是所有实际为正的观测，然后问自己：在这些实际为正的样本里，你真的预测为正的是哪些</b>」⇒ 排序版本是：「<b>在所有实际相关的文档里，哪些是你预测为相关的 —— 也就是哪些落进了前 k</b>」。<br>⚠ 请把它和前面那条规矩接上：<b>第一级要「最大化 recall」,而 recall@k 正是那条规矩的量化版 ⇒ 第一级的调参目标，就是把这个数推高</b>。<br>⇒ 到这里你应该能回答一个问题：<b>为什么第一级看 recall、第二级看 NDCG？因为第一级只管「别漏」,第二级才管「排得对不对」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("55:44","which are the ones that you actually predicted as being relevant",166);
  says("56:04","precision is out of all the ones that you have predicted to be positives, how many of them are actually positive",192);
  note("⭐ 第四个：precision@k —— 和 recall 互为镜像",640,222,"y");
  boxNode(80,254,500,50,"recall@k","g");
  boxNode(700,254,500,50,"precision@k","y");
  note("分母是「所有实际相关的」",330,328,"g");
  note("分母是「你选进前 k 的」",950,328,"y");
  note("⚠ 一句话分清：recall 问「漏了没」,precision 问「混进来多少垃圾」",640,374,"r");''',
         "<b>第四个和第三个互为镜像，一起记最省事。</b><br>⭐ 「<b>precision 是：在你预测为正的那些里，有多少是真的为正 ⇒ 在这里就是：你选进前 k 的那些里，有多少是真的相关</b>」。<br>⚠ 两者的区别只在<b>分母</b>:<b>recall 的分母是「所有实际相关的」（所以它问「漏了没」）;precision 的分母是「你选进前 k 的」（所以它问「混进来多少垃圾」）</b>。<br>⇒ 而在 RAG 里两个都重要，但重要的方式不同：<b>recall 低 ⇒ 答案根本不在 prompt 里，模型只能编；precision 低 ⇒ 答案在 prompt 里，但被一堆无关内容淹着 —— 而「无关内容会让表现退化」正是这一讲开头讲的那件事</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("56:44","these four metrics, NDCG, MRR, precision at k, recall at k, we see this in a bunch of papers",166);
  note("⭐ 四个指标收一次 —— 它们会在很多论文里出现",640,196,"y");
''' + four(0) + r'''  note("位置加权的总分  ｜  第一条对的排第几  ｜  选进来的有多准  ｜  漏了多少",640,300,"y");
  note("讲者的建议：「熟悉它们的想法，也许还有公式」",640,344,"g");
  note("⚠ 而它们量的是「检索器做得好不好」,不是「最终答案对不对」",640,384,"r");''',
         "<b>四个指标到齐了，讲者把它们收在一起。</b><br>⭐ 「<b>NDCG、MRR、precision@k、recall@k —— 我们在一大堆论文里都会看到这四个 ⇒ 我强烈建议你熟悉它们的想法，也许还有它们的公式；而这些就是你用来量化你的检索器做得好不好的那些</b>」。<br>⚠ 最后半句请留意：<b>它们量的是「检索器」,不是「整个 RAG 系统」—— 检索全对，而模型照样可能把答案读错 ⇒ 端到端的质量要另外评，而那是 L8 的内容</b>。<br>⇒ 这也是 RAG 工程里一个很实际的调试顺序：<b>先用这四个确认检索没问题，再去怀疑生成那一步</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("57:05","massive text embedding benchmark",166);
  says("57:10","if you want to test your retriever, if it performs well or not",192);
  note("⭐ 有现成的 benchmark：MTEB",640,222,"y");
  boxNode(60,254,280,46,"你的检索器","b");
  link(340,277,400,277);
  boxNode(400,254,300,46,"放到 MTEB 上跑","y");
  link(700,277,760,277);
  boxNode(760,254,420,46,"四个指标一次全算出来","g");
  note("有几套方案时，就拿这些指标横着比",640,330,"y");
  note("⚠ 「massive text embedding benchmark」—— 名字里的 embedding 说明它测的是哪一级",640,374,"r");''',
         "<b>不用自己从零搭评测：这类东西有现成的 benchmark。</b><br>⭐ 「<b>有一个相当流行的，叫 massive text embedding benchmark（MTEB）—— 如果你想测你的检索器表现好不好，典型地就把它拿过来在那个 benchmark 上评，然后这些指标就都算出来了；如果你有不同的方案，你就拿这些指标来比</b>」。<br>⚠ 注意名字里的 <b>embedding</b>:<b>它主要测的是「embedding 把相关的东西放得近不近」,也就是第一级那一层 —— 所以它是选 embedding 模型时的参考，不是整个 RAG 管线的成绩单</b>。<br>⇒ 上半场的方法论到这里就完整了：<b>怎么建库 · 怎么两级检索 · 怎么量</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("57:58","for the re-ranking, we are using an encoder that will output a relevance score",166);
  note("⭐ 收尾提问一：重排那个模型从哪来、为什么能更重",640,196,"y");
  boxNode(80,228,500,50,"第一级","d");
  boxNode(700,228,500,50,"第二级（重排）","g");
  note("要在几十万到几百万条上跑",330,302,"d");
  note("只在一百多个候选上跑",950,302,"g");
  note("⇒ 所以这里「你负担得起花更多时间去产生那个分数」",640,348,"y");
  note("⚠ 而这个模型是要训的 —— 「有一些预训练的，但你完全可以有自己的」",640,386,"r");''',
         "<b>第一个收尾提问：重排用的那个编码器是哪来的？</b><br>⭐ 答案是<b>要训的</b>：「<b>我们典型地会训一个做这件事的模型 —— 我相信外面有一些预训练好的，但你完全可以有自己定制的</b>」。<br>⚠ 而他给出的「为什么它可以更重」的理由，正好把整个两阶段结构又说了一遍：「<b>那个模型典型地会比第一步的复杂一点 —— 因为在这里你负担得起花更多时间去产生那个分数，因为你是在一百多个候选上操作，而不是几百万、几十万</b>」。<br>⇒ <b>这是这一讲里这个论证第三次出现 —— 可见它有多核心</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("58:50","how about training with contrastive loss",166);
  says("59:19","give it to Shervine",192);
  note("⭐ 收尾提问二，以及交棒",640,222,"y");
  boxNode(80,254,500,50,"问：用对比损失训行吗","b");
  boxNode(700,254,500,50,"答：那是 S-BERT 里的一种","y");
  note("「训这些模型会有一大堆不同类型的损失函数」",330,328,"b");
  note("「强烈推荐读 S-BERT 那篇，它比较了好几个」",950,328,"y");
  note("⚠ 上半场结束，下半场 Shervine 讲工具与 agent",640,374,"r");''',
         "<b>第二个收尾提问，然后上半场结束。</b><br>⭐ 问题是「<b>用对比损失来训呢</b>」,而讲者的回答把这件事归位了：「<b>这是一个细节，我们这里不展开；但要训这些模型，你会有一大堆不同类型的损失函数 —— 我强烈推荐你读 S-BERT 那篇，因为那篇论文里比较了好几个损失函数，而这是其中之一</b>」。<br>⚠ 这是他<b>第二次</b>推荐同一篇论文（第一次是讲 embedding 怎么训时）—— <b>整堂课里被推荐两次的只有这一篇，如果你只打算读一篇 RAG 相关的论文，就读它</b>。<br>⇒ 「<b>就这样，我把它交给 Shervine</b>」—— 下半场换人，主题从「读得到」变成「做得到」。", 0)],
       {"h": "⭐ 另外三个指标与交棒",
        "k": "<b>MRR</b>：<b>「你有另一个叫 reciprocal rank 的 —— 这个简单得多，它取所有相关文档里名次最高的那个的倒数」,比如第一个相关文档在第 2 位，「那 rank 就等于 2」⇒ 「它基本上不关心第一个相关文档之后的任何相关文档」,但「它是一个更简单的指标，而且典型地相关性很好，所以人们用它」</b>。<br><b>recall@k / precision@k</b>：<b>「recall 看所有实际为正的观测，问自己在这些里你真的预测为正的是哪些」⇒ 排序版是「在所有实际相关的文档里，哪些是你预测为相关的 —— 也就是哪些在前 k 里」;「precision 是在你预测为正的那些里，有多少是真的为正」⇒ 「你选进前 k 的那些里，哪些是真的相关」</b>。<br>收一次：<b>「这四个指标 —— NDCG、MRR、precision@k、recall@k —— 我们在一大堆论文里都会看到；我强烈建议你熟悉它们的想法，也许还有公式」</b>;benchmark：<b>「有一个相当流行的，叫 massive text embedding benchmark」</b>。<br>两个收尾提问：<b>① 重排那个模型「我们典型地会训一个」,「我相信外面有一些预训练好的，但你完全可以有自己定制的」,而「那个模型典型地会比第一步的复杂一点 —— 因为在这里你负担得起花更多时间，你是在一百多个候选上操作，而不是几百万」; ② 「用对比损失训呢」——「这是一个细节⋯⋯但我强烈推荐你读 S-BERT 那篇，那里面比较了好几个损失函数」</b>⇒ <b>「就这样，我把它交给 Shervine」</b>。",
        "m": "⭐ 四个指标各管一件事：<b>NDCG 是位置加权的总分 · MRR 是「第一条对的排第几」· precision@k 是「选进来的有多准」· recall@k 是「漏了多少」</b>;而<b>两级各看哪一个是有道理的</b>:<b>第一级只管「别漏」⇒ 看 recall@k；第二级才管「排得对不对」⇒ 看 NDCG</b>。<br>⭐ 在 RAG 里两种错的<b>后果不同</b>:<b>recall 低 ⇒ 答案根本不在 prompt 里，模型只能编；precision 低 ⇒ 答案在 prompt 里但被无关内容淹着 —— 而「无关内容会让表现退化」正是这一讲开头讲的那件事</b>。<br>⭐ 而「重排可以更重」的理由在这一讲里<b>第三次出现</b>:候选少了，才负担得起昂贵判据。",
        "w": " 这四个指标量的是<b>检索器</b>,不是整个 RAG 系统：<b>检索全对，模型照样可能把答案读错 ⇒ 端到端质量要另外评，那是 L8</b> —— 而这给了一个实际的调试顺序：<b>先用这四个确认检索没问题，再去怀疑生成那一步</b>。<br>⚠ MTEB 名字里的 <b>embedding</b> 说明它测的是哪一级：<b>它主要测「embedding 把相关的东西放得近不近」,是选 embedding 模型时的参考，不是整条管线的成绩单</b>。<br>⚠ MRR 的盲区是「只看第一条对的」—— <b>但「和复杂指标高度相关、而且便宜」是指标被采用的常见理由</b>。",
        "r": "⇒ <b>S-BERT 那篇被推荐了两次</b>（讲 embedding 怎么训时一次，讲对比损失时又一次）—— <b>整堂课里只有这一篇有这个待遇；只读一篇 RAG 论文的话就读它</b>。<br>⇒ 上半场的方法论到这里完整了：<b>怎么建库 · 怎么两级检索 · 怎么量</b> ⇒ 下半场换人，主题从「读得到」变成「做得到」。<br>⇒ 更多（MTEB 的任务构成、对比损失的几种形式、重排模型的训练数据）见<b>深度笔记</b>。",
        },
       {"t": "为什么第一级看 recall@k、第二级看 NDCG？而 recall 低和 precision 低的后果有什么不同？",
        "o": ["只是习惯；两者后果一样",
              "因为第一级只管「别漏」（漏掉的第二级永远救不回来），第二级才管「排得对不对」；而 recall 低 ⇒ 答案根本不在 prompt 里，模型只能编；precision 低 ⇒ 答案在但被无关内容淹着，而无关内容本身就会让表现退化",
              "因为 NDCG 算得慢；两者都只影响速度",
              "因为第一级没有标签；recall 低只影响成本"],
        "a": 1,
        "w": "⇒ 另外这四个指标量的是「检索器」，不是整个 RAG 系统 —— 检索全对，模型照样可能把答案读错。所以实际调试顺序是：先确认检索没问题，再怀疑生成那一步。"})
