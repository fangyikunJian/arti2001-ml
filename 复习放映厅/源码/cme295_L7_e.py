# -*- coding: utf-8 -*-
"""CME295 L7 模块 e —— 字幕第 233–290 句（27:46–34:12）：候选召回这一级怎么做 ——
余弦相似、近似最近邻、bi-encoder、S-BERT，以及「语义相似」到底是什么意思。
"""


def add(KP):

    KP("⭐ 候选召回：embedding、余弦相似与 bi-encoder",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("27:46","the first step is candidate retrieval",166);
  note("⭐ 第一级怎么做：用建库时就算好的那些 embedding",640,196,"y");
  boxNode(80,228,500,50,"知识库（几百万 chunk）","d");
  link(580,253,700,253);
  boxNode(700,228,500,50,"一百多个潜在相关候选","y");
  note("手段：语义相似度搜索（semantic similarity search）",640,304,"g");
  note("⚠ 关键在「建库时就算好了」—— 查询时不用再跑一遍整个知识库的编码",640,348,"r");''',
         "<b>第一级的做法：直接用建知识库时就算好的那些 embedding。</b><br>⭐ 「<b>我们要在那个可能很庞大的知识库里，把它过滤到比如一百多个潜在相关的候选 —— 办法是做一次语义相似度搜索</b>」。<br>⚠ 请注意「<b>建库时就算好了</b>」这件事有多重要：<b>chunk 的 embedding 是离线一次性算完存起来的 ⇒ 查询时只需要给「这一条 query」算一个 embedding，然后和库里的比 —— 而不是把几百万个 chunk 再编码一遍</b>。<br><b>这就是为什么这一级能做到「便宜」</b>:它把绝大部分计算挪到了离线。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("28:31","cosine similarity is typically one way one good way to compare embeddings",166);
  says("29:10","you perform a similarity operation, which is most of the time cosine similarity",192);
  note("⭐ 整个第一级的流程，四步",640,222,"y");
  boxNode(50,254,250,46,"query","b");
  boxNode(50,310,250,46,"chunk","v");
  link(300,300,400,300);
  boxNode(400,278,260,50,"各算一个 embedding","g");
  link(660,303,760,303);
  boxNode(760,278,220,50,"余弦相似度","y");
  link(980,303,1060,303);
  boxNode(1060,278,160,50,"取前 100","g");
  note("⚠ 「相似度得分排序、留前 100，就这么走」—— 这一级的全部内容",640,374,"r");''',
         "<b>第一级的完整流程，四步就走完了。</b><br>⭐ <b>query 算一个 embedding ⇒ chunk 的 embedding 库里现成 ⇒ 算余弦相似度 ⇒ 取排在最前的一百个</b>。讲者问了一句「<b>你们记得我们怎么比较 embedding 吗</b>」,学生答余弦相似度 —— 他确认「<b>余弦相似度典型地是一个、是一个很好的比较 embedding 的办法</b>」。<br>⚠ 请体会这一级有多<b>粗糙</b>:它完全不看 query 和 chunk 之间的任何交互，<b>只是把两个各自独立算出来的向量比一下夹角</b> ⇒ <b>而这个「粗糙」正是它能在几百万条上跑起来的原因</b>。第二级要补的就是这个缺的交互。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("29:40","what people do is typically use what we call approximate nearest neighbor methods",166);
  says("30:08","make you avoid doing like just a naive linear search",192);
  note("⭐ 一个实现上的复杂度：知识库可能非常大",640,222,"y");
  boxNode(80,254,500,50,"朴素做法：线性扫一遍","r");
  boxNode(700,254,500,50,"ANN：近似最近邻","g");
  note("几百万条每条都算一次余弦",330,328,"r");
  note("建库时就把 embedding 分好区",950,328,"g");
  note("⚠ 「近似」两个字是真的：它用一点准确率换巨大的速度",640,374,"r");''',
         "<b>这一级有一个实现上的坑：知识库大起来，连「算一遍余弦」都嫌贵。</b><br>⭐ 「<b>人们典型地用所谓的近似最近邻（approximate nearest neighbor）方法</b>」—— 做法是「<b>建知识库时就把 embedding 做某种分区，好让你避免做一次朴素的线性搜索</b>」。讲者说<b>不展开，但要点出来</b>,因为你会在很多库里看到 ANN 这个词。<br>⚠ 「<b>近似</b>」两个字请当真：<b>ANN 不保证找到真正最近的那些，它用一点召回率换巨大的速度 ⇒ 所以它本身也是第一级「漏掉」的一个来源</b>，而这正好又回到那条规矩：<b>第一级漏掉的，第二级救不回来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("30:53","so you may hear the term bi encoder",166);
  says("31:30","you would have something like a BERT-like model that you would use to encode these documents",192);
  note("⭐ 这个架构有名字：bi-encoder（双编码器）",640,222,"y");
  boxNode(80,254,300,50,"query","b");
  link(380,279,450,279);
  boxNode(450,254,260,50,"编码器","v");
  boxNode(80,310,300,50,"chunk","g");
  link(380,335,450,335);
  boxNode(450,310,260,50,"编码器","v");
  boxNode(820,278,360,52,"两个 embedding，再比","y");
  note("⚠ 「两边是独立的」—— 这就是 bi 的意思，也是它便宜的原因",640,380,"r");''',
         "<b>这个架构有一个你会反复看到的名字。</b><br>⭐ 「<b>你可能会听到 bi-encoder 这个词 —— 它指的是我们把 query 过一个编码器、把 chunk 过一个编码器，两边是独立的，然后比较两个 embedding</b>」。而编码器典型是 <b>encoder-only</b> 的，比如 <b>BERT</b>（L2 / L3 讲过）。<br>⚠ 「<b>两边是独立的</b>」这五个字<b>既是它的优点也是它的缺点</b>：<b>优点是 chunk 那一边可以离线算完存起来（所以便宜）;缺点是模型从来没有「同时看到」query 和 chunk，捕捉不到两者之间的交互</b> ⇒ <b>请记住这个缺点，因为第二级（cross-encoder）要补的正是它</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("31:47","that is called Sentence BERT",166);
  says("32:17","a loss function that will incentivize having a high cosine similarity for relevant entities",192);
  note("⭐ 那个 embedding 模型怎么训的：S-BERT",640,222,"y");
  boxNode(80,254,500,50,"相关的一对","g");
  boxNode(700,254,500,50,"不相关的一对","r");
  note("损失推高它们的余弦相似度",330,328,"g");
  note("损失压低它们的余弦相似度",950,328,"r");
  note("⚠ 所以这个 embedding 是「为相似度搜索定制」的 —— 不是通用表示",640,374,"r");''',
         "<b>前面那个「embedding 模型怎么训」的问题，在这里还了。</b><br>⭐ 讲者<b>强烈推荐</b>一篇论文：<b>Sentence BERT（S-BERT）</b> —— 「它是 BERT 的一个扩展，<b>让你能为一个序列（你的 query、你的文档）算一个专门为相似度搜索定制的 embedding</b>」。而做法就是损失函数：「<b>让相关的实体之间余弦相似度高、不相关的之间余弦相似度低</b>」。<br>⚠ 这正好回答了前面那个问题：<b>embedding 不是「通用的语义表示」,它是被一个损失专门塑形成「相关的靠近、不相关的远离」的表示</b>。讲者说「<b>如果你已经懂 BERT，这篇读起来很容易，强烈推荐</b>」。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("32:54","what is the default way to compute the similarity",166);
  says("33:15","but then if everything has a norm of 1, there is a lot of simplifications that can happen",192);
  note("⭐ 一个追问：一定得用余弦吗？",640,222,"y");
  boxNode(80,254,500,50,"余弦相似度","g");
  boxNode(700,254,500,50,"L2 距离等等","y");
  note("默认，也是最常见的",330,328,"g");
  note("在不同实现里也会看到",950,328,"y");
  note("⚠ 「如果所有向量范数都是 1，很多化简就会发生」—— 两者其实是一回事",640,374,"r");''',
         "<b>有人追问：计算相似度的默认方式是什么？一定得是余弦吗？</b><br>⭐ 答案是「<b>是的，余弦相似度</b>」,但讲者加了一个很有价值的提示：「<b>你在不同实现里会看到人们用别的距离 —— 而我鼓励你去想想它们彼此之间是什么关系</b>」。他举的例子是 <b>L2 距离</b>:「<b>如果所有东西的范数都是 1，就会有很多化简发生</b>」⇒ 「<b>所以你会看到一些变体，但我会说它们或多或少都是余弦相似度</b>」。<br>⚠ 这个提示值得照着做：<b>读实现时碰到一个陌生的距离，先问「在归一化之后它和余弦差在哪」—— 多半是同一个东西换了写法</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("33:48","what does semantic similarity mean",166);
  says("34:19","they do not have any word in common, but they mean the same",192);
  note("⭐ 「语义相似」到底是什么意思 —— 而它有一个明确的缺口",640,222,"y");
  boxNode(80,254,500,50,"它保证的","g");
  boxNode(700,254,500,50,"它不保证的","r");
  note("找出「意思相同 / 相关」的东西",330,328,"g");
  note("不强制任何关键词匹配",950,328,"r");
  note("⚠ 取回来的文档「可能一个共同的词都没有，但意思一样」—— 下一块就补这个缺口",640,374,"r");''',
         "<b>讲者回头给「语义相似」下了一个定义，而定义本身就暴露了它的缺口。</b><br>⭐ 「<b>它的意思是找出那些意思相同、或者相关的东西；但按我们算 embedding 的方式，我们并没有强制任何关键词匹配 —— 这样取回来的文档完全可能一个共同的词都没有，但它们意思一样</b>」。<br>⚠ 请把这句话的两面都看清：<b>「不要求字面重合」正是语义检索的卖点（问「怎么退货」能找到写着「退换流程」的文档）;但它同时意味着「你明确要找的那个词，它不保证给你」</b> ⇒ <b>而「有时候你就是要确保含某个关键词」—— 这就是下一块 BM25 和混合检索要解决的问题</b>。", 0)],
       {"h": "⭐ 候选召回这一级",
        "k": "<b>「第一步是 candidate retrieval」—— 用建库时算好的 embedding，「做一次语义相似度搜索」去捞潜在相关的候选；「余弦相似度典型地是一个很好的比较 embedding 的办法」⇒ 「query 和 chunk 各求一个 embedding，然后做一次相似度运算（大多数时候是余弦相似度）,得到一个相似度分，留前 100」</b>。<br>实现：<b>「人们典型地用所谓的近似最近邻（ANN）方法 —— 建知识库时就把 embedding 做某种分区，好让你避免做一次朴素的线性搜索」</b>。<br>架构：<b>「你可能会听到 bi-encoder 这个词 —— 它指的是我们把 query 过一个编码器、把 chunk 过一个编码器，两边是独立的，然后比较两个 embedding」,而编码器典型是 BERT 那样的 encoder-only 模型</b>。<br>怎么训：<b>「有一篇我强烈推荐读的论文，叫 Sentence BERT」—— 它「让你能为一个序列算一个专门用于相似度搜索的 embedding」,做法是「一个损失函数，激励相关实体之间有高余弦相似度、不相关的之间低余弦相似度」</b>。<br>两个追问：<b>默认距离是余弦，而「如果所有东西范数都是 1，很多化简会发生」⇒ 别的距离「或多或少都是余弦相似度」; 「语义相似是什么意思」—— 找意思相同或相关的，「但我们并没有强制任何关键词匹配」</b>。",
        "m": "⭐ 这一级能「便宜」的根本原因是<b>它把绝大部分计算挪到了离线</b>:<b>chunk 的 embedding 建库时一次性算完存起来 ⇒ 查询时只给这一条 query 算一个 embedding 再去比，而不是把几百万个 chunk 重编码一遍</b>。<br>⭐ 而 <b>bi-encoder 的「两边独立」既是优点也是缺点</b>：<b>优点是 chunk 那边能离线算；缺点是模型从来没有「同时看到」query 和 chunk，捕捉不到两者的交互 ⇒ 第二级（cross-encoder）要补的正是这个</b>。<br>⭐ S-BERT 那个损失说清了一件事：<b>embedding 不是「通用的语义表示」,它是被一个损失专门塑形成「相关的靠近、不相关的远离」的表示</b>。",
        "w": " 「<b>近似</b>最近邻」里的「近似」请当真：<b>ANN 不保证找到真正最近的那些，它用一点召回率换巨大的速度 ⇒ 它本身也是第一级「漏掉」的一个来源</b>,而这又回到那条规矩：第一级漏掉的，第二级救不回来。<br>⚠ 而「语义相似」的两面要一起看：<b>「不要求字面重合」是它的卖点（问「怎么退货」能找到「退换流程」）;但它同时意味着「你明确要找的那个词，它不保证给你」—— 下一块的 BM25 就是来补这个缺口的</b>。",
        "r": "⇒ 讲者那个关于距离的提示值得照着做：<b>读实现时碰到一个陌生的距离，先问「在归一化之后它和余弦差在哪」—— 多半是同一个东西换了写法</b>。<br>⇒ 而 <b>S-BERT 那篇是他这一讲里唯一「强烈推荐」的论文</b>（后面问到对比损失时他又推了一次）:「如果你已经懂 BERT，这篇读起来很容易」。<br>⇒ 更多（ANN 的常见库与分区思路、BERT 回顾、对比损失的几种形式）见<b>深度笔记</b>。",
        },
       {"t": "bi-encoder 的「两边独立」带来了什么好处和什么缺点？",
        "o": ["好处是更准，缺点是更慢",
              "好处是 chunk 那边的 embedding 能离线一次算完存起来（所以这一级便宜）；缺点是模型从来没有「同时看到」query 和 chunk，捕捉不到两者的交互 —— 而第二级的 cross-encoder 补的正是这个",
              "好处是省显存，缺点是只能用余弦距离",
              "好处是支持 ANN，缺点是必须用 BERT"],
        "a": 1,
        "w": "⇒ 而「语义相似」还有一个明确的缺口：它不强制关键词匹配，取回来的文档「可能一个共同的词都没有」—— 这就是下一块 BM25 要补的。"})
