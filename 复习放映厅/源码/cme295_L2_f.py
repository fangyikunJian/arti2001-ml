# -*- coding: utf-8 -*-
"""CME295 L2 模块 f —— 字幕第 374–428 句（43:47–50:51）：第二个变过的部件 ——
层归一化。add & norm 是什么、γ 和 β、post-norm → pre-norm、LayerNorm → RMSNorm，
以及两个很好的提问（为什么要归一化、和 BatchNorm 的区别）。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（16 镜 → 7 镜）。
⚠ 旁白里不许出现半角双引号；setEq 里反斜杠写双份。
"""


def add(KP):

    KP("⭐ 第二个变过的部件：层归一化（add & norm）",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("43:47","And that component is the layer normalization",166);
  says("44:17","We add them together, and then we normalize",192);
  note("⭐ Add & Norm 这一个方块里，装的是两个独立的机制",640,222,"y");
  boxNode(80,254,500,50,"Add ＝ 残差连接","b");
  boxNode(700,254,500,50,"Norm ＝ 层归一化","g");
  note("解决梯度在深网络里传不回去",330,328,"b");
  note("解决激活的尺度到处乱跑",950,328,"g");
  note("⚠ 它们被画在同一个方块里，但解决的是两个完全不同的问题",640,374,"r");''',
         "<b>第二个部件登场，而讲者的切入点选得很好。</b><br>⭐ 「<b>位置嵌入是 transformer 里变了一点的一个部分⋯⋯现在我们要看另一个也变了一点点的部件 —— 而那个部件就是层归一化。如果你记得，你有那些写着 add and norm 的方块</b>」; 做法是：「<b>我们取这个子层的输入、以及这个子层的输出，我们把它们加起来，然后我们归一化。这是作者做的一个小技巧，而它在实践中被证明能改善收敛</b>」。<br>⭐⭐ 请注意 <b>Add & Norm 这一个方块里装的是两个独立的机制</b>:<b>Add 是残差连接，解决的是梯度在深网络里传不回去；Norm 是层归一化，解决的是激活的尺度到处乱跑 —— 它们被画在一起，但针对的是两个完全不同的问题</b>。", 0),
        (r'''clearScene();setBig(null);setCap(null);noTitle();
  setEq("$$\\hat{x}=\\frac{x-\\mu}{\\sigma}$$");
  says("44:48","if you have a vector, sometimes the components of the vector can be super large, sometimes they can be super small",166);
  says("45:05","you are going to take your vector, and then subtract it by the computed mean",192);
  note("⭐⭐⭐ 盯住一个词：它说的是「你这个向量的分量」",640,224,"y");
  note("⇒ 均值和方差是在一个样本自己的 d 个分量上算的 —— 和别的样本完全无关",640,256,"g");
  note("⚠ 这就是 Layer 这个字的全部含义，也是它和 BatchNorm 的唯一区别",640,288,"r");''',
         "<b>问题陈述很朴素，但请盯住一个词：它说的是「一个向量内部」的分量。</b><br>⭐ 「<b>如果你有一个向量，有时候这个向量的分量可以超级大，有时候可以超级小。这里的想法是把你这个向量的分量归一化到某个范围里⋯⋯你要取你的向量，然后把它减掉算出来的均值，然后基本上用它的标准差去归一化它</b>」。<br>⭐⭐⭐ 「<b>你这个向量的分量</b>」这几个字就是 LayerNorm 的定义核心：<b>均值 μ 和标准差 σ 是在「这一个样本自己的 d 个分量」上算出来的，和 batch 里别的样本完全无关 ⇒ 这就是 Layer 这个字的含义，也是它和 BatchNorm 的唯一区别</b>。<br>⭐ 两个动作两个作用：<b>减均值去掉整体偏移、除标准差把尺度拉成 1</b>。", 0),
        (r'''clearScene();setBig(null);setCap(null);noTitle();
  setEq("$$y=\\gamma\\cdot\\frac{x-\\mu}{\\sigma}+\\beta$$","top");
  says("45:20","you are going to learn two quantities-- one, gamma, which is going to be the rescaling factor",192);
  says("45:43","what this does is it helps with training stability and with convergence time",218);
  note("⭐ 一个自然的疑问：归一化完又学 γ、β 缩放回去，不是白做了吗？",640,254,"y");
  note("⇒ 不是。归一化改的是「起点」,γ 和 β 让模型自己决定「终点」",640,288,"g");
  note("⇒ 从一个良态的分布出发去调整，比从一个乱跑的分布出发容易得多",640,322,"b");
  note("⚠ 两个好处要分开：稳定性＝不会炸；收敛时间＝同样步数走得更远",640,356,"r");''',
         "<b>公式补完了，而这里有一个值得想一想的设计。</b><br>⭐ 「<b>你要学两个量 —— 一个是 gamma，它是那个重新缩放的因子；然后是 beta，它是另一个你也要学的项⋯⋯而这个东西做的事是：它帮助训练的稳定性、以及收敛的时间</b>」。<br>⭐⭐ 一个很自然的疑问：<b>你费劲把它归一化成均值 0、方差 1，然后又学 γ 和 β 把它缩放平移回去 —— 这不是白做了吗？不是：归一化改的是优化的「起点」,而 γ 和 β 让模型自己决定「终点」—— 从一个良态的分布出发去调整，比从一个尺度乱跑的分布出发容易得多</b>。<br>⚠ 而那两个好处要分开看：<b>稳定性是「不会炸、不会死」,收敛时间是「同样的步数走得更远」—— 前者关乎能不能训，后者关乎要花多少钱</b>。", 0)],
       {"h": "⭐ Add & Norm 与 γ、β",
        "k": "<b>「所以位置嵌入是 transformer 里变了一点的一个部分⋯⋯那么现在我们要看 transformer 的另一个部件，它也变了一点点 —— 而那个部件就是层归一化⋯⋯你有那些写着 add and norm 的方块」; 「这里我们做的是：我们取这个子层的输入、以及这个子层的输出，我们把它们加起来，然后我们归一化。所以这是作者做的一个小技巧。而它在实践中被证明能改善收敛」</b>。<br>⭐ 做法：<b>「如果你有一个向量，有时候这个向量的分量可以超级大，有时候它们可以超级小。这里的想法是把你这个向量的分量归一化到某个范围里」; 「你要取你的向量，然后把它减掉算出来的均值 —— 那基本上就是它各个分量的和 —— 然后基本上用它的标准差去归一化它」; 「而你要做的是，你要学两个量 —— 一个是 gamma，它会是那个重新缩放的因子；然后是 beta，它是另一个你也要学的项」; 「这个东西做的事是：它帮助训练的稳定性、以及收敛的时间」</b>。",
        "m": "⭐⭐ <b>Add & Norm 这一个方块里装的是两个独立的机制</b>:<b>Add 是残差连接（解决梯度在深网络里传不回去）, Norm 是层归一化（解决激活的尺度到处乱跑）—— 画在一起，但针对两个完全不同的问题</b>。<br>⭐⭐⭐ 「<b>你这个向量的分量</b>」是 LayerNorm 的定义核心：<b>μ 和 σ 是在这一个样本自己的 d 个分量上算的，和 batch 里别的样本完全无关 ⇒ 这就是 Layer 这个字的含义</b>。<br>⭐ 而 γ、β 不是白做：<b>归一化改的是优化的起点，γ 和 β 让模型自己决定终点 —— 从一个良态分布出发去调整，比从一个乱跑的分布出发容易得多</b>。",
        "w": " 两个好处要分开理解：<b>稳定性是「不会炸、不会死」（没有归一化时，某一层的激活爆大会让后面所有层的梯度一起爆）; 收敛时间是「同样的步数走得更远」—— 前者关乎能不能训，后者关乎要花多少钱</b>。<br>⚠ 而减均值和除标准差也是两个动作：<b>前者去掉这个向量的整体偏移（归一化后均值为 0）,后者把尺度拉成 1 —— 下一段 RMSNorm 砍掉的正是前者</b>。",
        "r": "⇒ 残差和归一化虽然画在同一个方块里，但在后来的架构演化里<b>各自走了不同的路</b>:<b>残差连接八年没动过，而归一化既换了位置（post→pre）又换了算式（LayerNorm→RMSNorm）</b>。<br>⇒ 更多（残差为什么能救梯度、γ/β 的参数量、归一化与学习率的互动）见<b>深度笔记</b>。",
        },
       {"t": "LayerNorm 里的均值 μ 和标准差 σ 是在什么范围上算出来的？",
        "o": ["在整个训练集上算一次，然后固定下来",
              "在一个样本自己的 d 个分量上算的，和 batch 里别的样本完全无关 —— 这就是 Layer 这个字的含义，也是它和 BatchNorm 的唯一区别",
              "在整个 batch 的同一个维度上算的，所以依赖 batch 大小",
              "在前一层的权重矩阵上算的"],
        "a": 1,
        "w": "⇒ 而归一化之后又学 γ 和 β 并不是白做：归一化改的是优化的起点，γ 和 β 让模型自己决定终点。"})

    KP("⭐ 两处改动：post-norm → pre-norm，LayerNorm → RMSNorm",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("46:21","what we have done is to change where the normalization is located",166);
  says("46:40","which basically consists of having the LayerNorm right before the vector goes into the sublayer",192);
  note("⭐ 第一处改动：只是把一个操作挪了个位置 —— 而差别只在括号",640,222,"y");
  boxNode(80,254,500,50,"post-norm：Norm(x ＋ 子层(x))","r");
  boxNode(700,254,500,50,"pre-norm：x ＋ 子层(Norm(x))","g");
  note("原论文的版本",330,328,"r");
  note("⇒ 残差这条路上再没有归一化挡着",950,328,"g");
  note("⚠ 子层既可以是注意力层也可以是 FFN ⇒ 一个 block 里有两处归一化",640,374,"v");''',
         "<b>这是第一处改动，而它只是把一个操作挪了个位置。</b><br>⭐ 「<b>我们从「归一化（输入 ＋ 子层的输出）」变成了「输入 ＋ 子层(归一化后的输入)」的和。换句话说，我们做的是改变归一化所处的位置 —— 在 transformer 论文里它是我们现在叫做 post-norm 的版本，而如今我们用 pre-norm 版本</b>」; 而 pre-norm 就是「<b>把 LayerNorm 放在向量进入子层之前，而这里的子层可以是注意力层，也可以是 FFN</b>」。<br>⭐⭐ 请把两条式子对齐看，差别只在括号：<b>post-norm 的残差路径上压着一个归一化，梯度回传时每一层都要穿过它；而 pre-norm 的残差是一条干净的直路 —— 这就是为什么深层模型几乎全都转向了 pre-norm</b>。", 0),
        (r'''clearScene();setBig(null);setCap(null);noTitle();
  setEq("$$y=\\gamma\\cdot\\frac{x}{\\sqrt{\\frac{1}{d}\\sum_j x_j^2}}$$","top");
  says("46:56","nowadays, people, they do not use LayerNorm. They use something else called RMSNorm",192);
  says("47:19","they just normalize x by the root mean square of the components of x, and they learn gamma, only gamma",218);
  note("⭐ RMSNorm 砍掉了两样东西：减均值 μ，和偏置 β",640,254,"y");
  note("⇒ 所以它不做中心化（均值不一定是 0）,也没有平移，只有缩放",640,288,"g");
  note("⭐ 而理由是那个熟悉的模式：收敛性质相当，但参数更少、更快",640,322,"b");
  note("⚠ 第三次见这个模式了 —— 两个方案打平时，选结构上更干净的那个",640,356,"r");''',
         "<b>第二处改动，而这次变的是算式本身。</b><br>⭐ 「<b>如今人们不用 LayerNorm 了。他们用另一个东西，叫 RMSNorm —— Root Mean Square Normalization，均方根归一化⋯⋯与其算那个，他们就用 x 各分量的均方根去归一化 x，而且他们学 gamma —— 只学 gamma</b>」 ⇒ <b>对照 LayerNorm，被砍掉的是：① 减均值 μ（所以不做中心化，归一化后均值不一定为 0）; ② 偏置 β（所以只有缩放、没有平移）</b>。<br>⭐ 理由很干脆：「<b>他们展示了收敛性质基本上是相当的。但这里你要学的参数更少，所以它基本上更快</b>」 ⇒ <b>这是今天第三次见这个模式了：两个方案指标打平时，选那个结构上更干净的 —— 而 LLaMA、Mistral、Qwen 全都用 RMSNorm</b>。", 0)],
       {"h": "⭐ pre-norm 与 RMSNorm",
        "k": "<b>「所以我们从「归一化（输入 ＋ 子层的输出）」,变成了「输入 ＋ 子层(归一化后的输入)」的和。所以换句话说，我们做的是改变归一化所处的位置。所以这里在 transformer 论文里，它是我们现在叫做 post-norm 的版本。而如今我们用 pre-norm 版本」; 「它基本上就是把 LayerNorm 放在向量进入子层之前。而这里的子层，可以是注意力层，也可以是 FFN」</b>。<br>⭐ 第二处：<b>「但不只是那个，还有另一个变化。所以如今，人们不用 LayerNorm 了。他们用另一个东西，叫 RMSNorm —— RMS，Root Mean Square，Normalization」; 「与其算这个，人们基本上做的是：他们就用 x 各分量的均方根去归一化 x，而且他们学 gamma —— 只学 gamma」; 「那他们为什么这么做？基本上，他们展示了收敛性质基本上是相当的。但这里你要学的参数更少，所以它基本上更快」</b>。",
        "m": "⭐⭐ post-norm 和 pre-norm 的差别只在括号，但后果很大：<b>post-norm 的残差路径上压着一个归一化，梯度回传时每一层都要穿过它；而 pre-norm 的残差是一条干净的直路 ⇒ 深层模型几乎全都转向了 pre-norm</b>。<br>⭐ RMSNorm 砍掉的正是 LayerNorm 的两样东西：<b>减均值 μ（不做中心化）和偏置 β（没有平移，只有缩放）</b>。<br>⭐ 而那个决策模式今天第三次出现：<b>第二代位置编码（效果相当但多一个外推性质）· ALiBi 之后的 RoPE · RMSNorm（收敛相当但参数更少）⇒ 两个方案打平时，选结构上更干净的那个</b>。",
        "w": " 「子层」这个词决定了归一化在一个 block 里出现几次：<b>子层一是多头注意力、子层二是 FFN ⇒ 每个 block 里有两处归一化、两处残差加法</b>。<br>⚠ 而「人们不用 LayerNorm 了」听起来绝对，但对今天的主流 LLM 基本成立：<b>LLaMA、Mistral、Qwen 这些都用 RMSNorm；而 BERT、GPT-2 那一代用的还是 LayerNorm</b>。",
        "r": "⇒ 这两处改动合起来说明了一件事：<b>八年里 transformer 的骨架没动，而动的全是这种「同样功能、更干净的实现」—— 位置编码从加在输入换成旋转 Q/K，归一化从 post 搬到 pre、从 LayerNorm 砍成 RMSNorm</b>。<br>⇒ 更多（pre-norm 为什么对深层更友好、RMSNorm 省下的参数量实测、各模型用哪种归一化）见<b>深度笔记</b>。",
        },
       {"t": "RMSNorm 相比 LayerNorm 砍掉了什么？为什么大家都换过去了？",
        "o": ["砍掉了 γ，只保留 β；因为 γ 容易梯度爆炸",
              "砍掉了除标准差这一步，只保留减均值；因为方差估计不稳",
              "砍掉了减均值 μ（不做中心化）和偏置 β（只有缩放、没有平移）;因为收敛性质和 LayerNorm 基本相当，而要学的参数更少、算得更快 —— 两个方案打平时选结构上更干净的那个",
              "砍掉了可学参数，整个变成无参数操作"],
        "a": 2,
        "w": "⇒ 而另一处改动是位置：post-norm 的残差路径上压着一个归一化，pre-norm 的残差是一条干净的直路 —— 所以深层模型几乎全都转向了 pre-norm。"})

    KP("⭐ 两个很好的提问：为什么要归一化、和 BatchNorm 的区别",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("47:35","they show that the convergence properties, they are basically comparable",166);
  says("48:12","So the question is, what is the intuition behind normalizing?",192);
  says("48:45","the model is typically having trouble in learning the weights in each of these layers if these activations, they vary too much",218);
  note("⭐⭐⭐ 关键词是「变化太大」,而不是「太大」",640,250,"y");
  boxNode(80,282,500,50,"太大：缩一下就行","d");
  boxNode(700,282,500,50,"变化太大：你不知道该缩多少","r");
  note("⚠ 上一层的权重刚适应一种尺度，下一批数据又换了一种 —— 这才是真正的麻烦",640,358,"r");''',
         "<b>这个提问讲者评为好问题，而他的回答里顺手铺了一个术语。</b><br>⭐ 先把 RMSNorm 的理由补完：「<b>他们展示了收敛性质基本上是相当的</b>」—— <b>打平而更便宜，所以换</b>。然后学生问「<b>归一化背后的直觉是什么？</b>」,回答从一个名词开始：「<b>你看到的那个从这里走到那里的向量，基本上就叫做 activation（激活）</b>」。<br>⭐ 正题是：「<b>有时候激活在它某一部分分量上有极端值，有时候在另一部分。而如果这些激活变化太大，模型在学习这些层里每一层的权重时，通常会有困难</b>」。<br>⭐⭐⭐ 关键词是「<b>变化太大</b>」而不是「太大」:<b>如果激活一直很大，那缩一下就行；而问题是它一会儿大一会儿小、这个样本大那个样本小 —— 于是上一层的权重刚适应了一种尺度，下一批数据又换了一种</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("49:09","there is this key word, internal covariate shift",166);
  says("49:32","batch normalization is normalization across the other dimension, which is the dimension of the batch",192);
  says("50:10","because BatchNorm, you are basically also dependent on the batch",218);
  note("⭐⭐ 和 BatchNorm 的区别就一个字：方向",640,250,"y");
  boxNode(80,282,500,50,"LayerNorm：在一个样本的 d 个分量上","g");
  boxNode(700,282,500,50,"BatchNorm：在 batch 里同一个分量上","b");
  note("⚠ 依赖 batch ⇒ 训练和推理之间有差异；而对变长序列还有「这个位置上有几个样本有值」的麻烦",640,358,"r");''',
         "<b>那个关键词，以及一个被连说了两次「很好的问题」的提问。</b><br>⭐ 「<b>万一你感兴趣，有这么一个关键词 —— internal covariate shift（内部协变量偏移）—— 它基本上就是给我在这里描述的这个现象起的那个名字</b>」 ⇒ <b>它出自 2015 年 BatchNorm 那篇论文，后来的研究质疑过这个解释，但归一化确实有效</b>。<br>⭐ 而区别的答案就一个字：方向。「<b>batch normalization 是沿着另一个维度做的归一化，也就是 batch 那个维度 —— 把每一个分量，相对于「同一个维度上、但属于其它那些向量的」所有分量去归一化</b>」; 而 transformer 用 LayerNorm 是「<b>可能因为经验上它效果更好，但也因为 BatchNorm 你基本上也依赖于那个 batch —— 它可以引入训练和推理之间的差异</b>」。", 0)],
       {"h": "⭐ 归一化的直觉与 BatchNorm 的区别",
        "k": "学生问「归一化背后的直觉是什么」,回答：<b>「这个直觉是：如果你看你的模型，你有好几层。在某些层里，你的向量 —— 更准确地说是你的激活⋯⋯你看到的那个从这里走到那里的向量，基本上就叫做 activation」; 「有时候激活在它某一部分分量上有极端值，有时候在另一部分。而如果这些激活变化太大，模型在学习这些层里每一层的权重时，通常会有困难。所以想法是把激活各分量的值带到某个不会在某个方向上偏太远的范围里」; 「万一你感兴趣，有这么一个关键词 —— internal covariate shift —— 它基本上就是给我在这里描述的这个现象起的那个名字」</b>。<br>⭐ 第二个提问：<b>「batch normalization 是沿着另一个维度做的归一化，也就是 batch 那个维度。所以假设你有一堆向量 —— 你做的是：把每一个分量，相对于「同一个维度上、但属于其它那些向量的」所有分量去归一化」; 「当涉及到这些基于 transformer 的模型时，人们典型地用 LayerNorm —— 可能是因为经验上它效果更好。但也因为 BatchNorm，你基本上也依赖于那个 batch。而它可以引入训练和推理之间的差异」</b>。",
        "m": "⭐⭐⭐ 关键词是「<b>变化太大</b>」而不是「太大」:<b>如果激活一直很大，缩一下就行；而问题是它一会儿大一会儿小、这个样本大那个样本小 ⇒ 上一层的权重刚适应了一种尺度，下一批数据又换了一种</b>。<br>⭐⭐ 而 LayerNorm 和 BatchNorm 的区别只有一个字：<b>方向</b>。<b>同样一个数值矩阵，LayerNorm 横着归一化（一个样本自己的 d 个分量）, BatchNorm 竖着归一化（batch 里所有样本的同一个分量）</b>。<br>⭐ transformer 选 LayerNorm 的硬理由是：<b>BatchNorm 依赖 batch ⇒ 推理时常常只有一个样本，必须改用训练期攒的滑动平均，于是训练和推理的行为不一致；而对变长序列，它还要面对「这个位置上有几个样本有值」的麻烦</b>。",
        "w": " internal covariate shift 出自 2015 年 BatchNorm 那篇论文，<b>它是归一化最初被提出时给的解释 —— 而后来的研究质疑过这个解释（有工作认为真正起作用的是让损失曲面更平滑）。但不管解释是哪一个，归一化确实有效，而这个词仍然是最常见的说法</b>。<br>⚠ 而 LayerNorm 和别的样本无关这件事有一个很实际的好处：<b>batch 多大都一样，batch 为 1 也一样 —— 这对推理极其重要</b>。",
        "r": "⇒ 「<b>activation（激活）</b>」这个名词值得记住：<b>它就是层与层之间传的那些向量 —— 而显存里占最多的那一块通常就是它们（为反传而缓存的 activation）</b>。<br>⇒ 更多（internal covariate shift 的争议、BatchNorm 在变长序列上的具体麻烦、归一化与损失曲面平滑性）见<b>深度笔记</b>。",
        },
       {"t": "为什么 transformer 用 LayerNorm 而不是 BatchNorm？",
        "o": ["因为 BatchNorm 没有可学参数，表达力不够",
              "因为 LayerNorm 的计算量更小",
              "因为 BatchNorm 只能用在卷积网络上，数学上不适用于序列",
              "因为经验上 LayerNorm 效果更好，而且 BatchNorm 依赖 batch ⇒ 推理时常常只有一个样本，必须改用训练期攒的滑动平均，于是训练和推理的行为不一致；对变长序列它还要面对「这个位置上有几个样本有值」的麻烦"],
        "a": 3,
        "w": "⇒ 两者的区别只有一个字：方向。LayerNorm 横着归一化（一个样本自己的 d 个分量）, BatchNorm 竖着归一化（batch 里所有样本的同一个分量）。"})
