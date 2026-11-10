# -*- coding: utf-8 -*-
"""CME295 L1 模块 i —— 字幕第 731–924 句（85:07–100:32）：label smoothing，以及
Shervine 的端到端走查 —— 从分词一路走到生成出 EOS。

⚠ 2026-11-10 按 L6 / L7 定稿的线重做：每镜旁白约 260 字（33 镜 → 18 镜）。
"""


def add(KP):

    KP("⭐ label smoothing 与端到端走查",
       [(r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("85:07","So the question is, are the projections different?",166);
  note("⭐ 多头最脆弱的一环：凭什么保证各头不一样？",640,196,"y");
  boxNode(80,228,500,50,"有约束吗","r");
  boxNode(700,228,500,50,"那为什么还不一样","g");
  note("「我们通常不去约束任何东西 —— 我们就让模型去学」",330,302,"r");
  note("「但实践中，它就是倾向于学出说同一件事的不同方式」",950,302,"g");
  note("⚠ 多头的全部价值建立在「各头学到不同东西」上，而这件事没有任何保证",640,348,"r");''',
         "<b>这个追问问到了多头机制最脆弱的一环，而讲者的回答很坦率。</b><br>⭐ 「<b>我们通常不去约束任何东西 —— 我们就让模型去学。但实践中，它就是倾向于学出『说同一件事的不同方式』。所以是的，典型地你没有任何约束</b>」。<br>⚠ 请体会这个回答里的<b>张力</b>:<b>多头的全部价值建立在「不同的头学到不同的东西」上 —— 而这件事没有任何机制上的保证，只有经验上的观察</b>。<br>⇒ 这类「<b>没有约束，但实践中就是这样</b>」的说法在深度学习里很常见，<b>而 Shervine 在走查末尾会给出一个更完整的回答</b>（那个回答比这里好得多）。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("85:39","OK, I will just mention one trick, another trick that the transformer authors use",166);
  says("86:44","And instead of saying it is a 1, 0, 0, 0, that you need to predict",192);
  note("⭐ label smoothing：它修的是那个「不可能达到的目标」",640,222,"y");
  boxNode(80,254,500,50,"原来的真值","d");
  boxNode(700,254,500,50,"平滑之后","g");
  note("(1, 0, 0, 0) —— 要求「只能是这一个词」",330,328,"d");
  note("目标词 1−ε，其余各分 ε/(v−1)",950,328,"g");
  note("⚠ 它承认的事实：「在 NLP 里，当你想预测接下来是什么时，通常不止一种方式」",640,374,"r");''',
         "<b>本讲最后一个技术点，而它修的正是前面那个别扭。</b><br>⭐ 它要处理的事实是：「<b>在 NLP 里，当你想预测接下来是什么时，通常不止一种方式 —— 『what a great day』『what a great lecture』都说得通</b>」 ⇒ 而原来的 one-hot 真值在要求「<b>只能是这一个词，别的全是 0</b>」,这是一个<b>不可能达到、而且也不该达到</b>的目标。<br>⭐ 做法只是改标签：「<b>不是说『100% 预测这个词、没有别的词』,而是说『预测这个词，但有一定机会它不是这个词』</b>」 ⇒ 具体是<b>目标词分到 1−ε，剩下的 ε 平摊给其余 v−1 个词</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("87:19","But in practice, the authors see that it tends to improve metrics like BLEU",166);
  says("88:32","So question is, is there a relation with explore and exploit?",192);
  note("⭐ 它管用吗？作者给的是经验证据；而学生的联想也有道理",640,222,"y");
  boxNode(80,254,500,50,"证据","g");
  boxNode(700,254,500,50,"学生的联想","y");
  note("「倾向于提升像 BLEU 这样的指标」",330,328,"g");
  note("这和「探索 vs 利用」有关系吗？",950,328,"y");
  note("⚠ 注意他把 BLEU 叫做「代理指标」—— 和「代理任务」同一个词根、同一个意思",640,374,"r");''',
         "<b>它管用吗？作者给的是经验证据。而随后那个联想很有意思。</b><br>⭐ 「<b>实践中，作者们看到它倾向于提升像 BLEU 这样的指标 —— 而 BLEU 是翻译任务的一个代理指标</b>」 ⇒ <b>注意「代理指标（proxy metric）」这个词：和前面那个「代理任务」同一个词根、同一个意思 —— BLEU 不是我们真正关心的东西，但它好测、而且和我们关心的相关</b>。<br>⚠ 而学生问「<b>这和探索与利用有关系吗</b>」:<b>这个联想有道理 ——「探索 vs 利用」说的是「要不要偶尔试试不是当前最优的那个」,而 label smoothing 做的正是不让模型把全部概率押在一个词上</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("89:02","So I guess the question here is, do you want to compare with 1, 0, 0, 0",166);
  note("⭐ 一个真实的混淆点：softmax 不是已经免费给了这个吗？",640,196,"y");
  boxNode(80,228,500,50,"softmax 管的是","g");
  boxNode(700,228,500,50,"label smoothing 管的是","y");
  note("模型「输出」的那一侧 —— 它本来就是分布",330,302,"g");
  note("你拿来「比对」的那一侧 —— 真值长什么样",950,302,"y");
  note("⚠ 两者在式子的两边，互相替代不了 —— 这是这一问最该带走的区分",640,348,"r");''',
         "<b>学生的追问抓住了一个真实的混淆点，而讲者的回答把两侧分清了。</b><br>⭐ 学生问「<b>softmax 不是已经免费给了这个吗？</b>」讲者反问「<b>softmax 为什么会免费给它呢？</b>」然后点破关键：「<b>归根结底，你想做的是把你的预测和标签去比较 —— 所以问题是：你是想和 (1,0,0,0) 比，还是想和某个不是 (1,0,0,0) 的东西比？</b>」<br>⚠ 区分就在这里：<b>softmax 作用在模型「输出」那一侧（它本来就产出一个分布）;而 label smoothing 作用在你拿来「比对」的那一侧（真值长什么样）⇒ 两者在式子的两边，互相替代不了</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("89:34","And yes, so we saw basically how the transformer worked",166);
  note("⭐ 最后二十分钟交给 Shervine —— 他要把所有零件装起来",640,196,"y");
  boxNode(80,228,500,50,"前面讲的是","d");
  boxNode(700,228,500,50,"接下来讲的是","g");
  note("每个部件各自在做什么",330,302,"d");
  note("它们怎么串成一条真的能跑的流水线",950,302,"g");
  note("⚠ 例子还是那句：a cute teddy bear is reading —— 从分词一路走到 EOS",640,348,"r");''',
         "<b>最后二十分钟交给 Shervine，而他要做的事是把前面所有零件装起来。</b><br>⭐ 「<b>我们基本上看了 transformer 是怎么工作的。而现在我们要用一个具体的例子把它全部拼起来 —— 就拿我们最爱的例子：a cute teddy bear is reading，然后我们一起走过每一步</b>」。<br>⭐ 为什么这一段值得你花最多时间：<b>前面讲的是「这个部件在做什么」,而这一段讲的是「它们怎么串成一条真的能跑的流水线」—— 而形状（每个矩阵多大、每一行每一列代表什么）只有在走查里才看得见</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("90:06","So as we said, we can use any arbitrary decomposition to decompose this into tokens",166);
  note("⭐ 第一步：分词 —— 他特意呼应了那个「任意」",640,196,"y");
  seq(90,228,["a","cute","teddy bear","is","reading"],"b",210,48);
  note("「我们可以用任意的分解方式把它分解成 token」—— 所以走查里用哪种切法都不重要",640,306,"y");
  note("⚠ 而紧接着他引出了一个之前没提过的必需品 —— 下一镜",640,350,"r");''',
         "<b>走查的第一步是分词，而 Shervine 特意呼应了前面那个「任意」。</b><br>⭐ 「<b>我们先从分词开始。如我们所说，我们可以用任意的分解方式把它分解成 token</b>」 ⇒ <b>这正好接上前面那条：切法是人定的，不存在「正确的切法」—— 所以在走查里用哪种切法并不重要，重要的是后面每一步的形状</b>。<br>⚠ 然后他引出了一个之前没正式提过的必需品：「<b>正如有人提到的，你需要有某种办法去指明一个序列的开始和结束</b>」 ⇒ 「<b>正如有人提到的</b>」指的是前面那个问「生成什么时候停」的学生 —— <b>而答案在下一镜</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("90:17","So typically, this is done with the BOS and EOS tokens",166);
  says("90:25","So now let us focus on the composition of each token representation",192);
  note("⭐ 两个特殊 token，以及每个 token 携带的两样东西",640,222,"y");
  boxNode(80,254,500,50,"BOS = 序列开始","g");
  boxNode(700,254,500,50,"EOS = 序列结束","y");
  note("解码的起点：「我们要开始预测了」",330,328,"g");
  note("生成的终点：「什么时候停」",950,328,"y");
  note("⚠ 而每个 token 送进去时携带两样：它的 embedding（学出来的）+ 位置信息",640,374,"r");''',
         "<b>两个特殊 token，而它们是生成任务能自洽运转的最后两块拼图。</b><br>⭐ 「<b>正如有人提到的，你需要有某种办法去指明一个序列的开始和结束 —— 典型地这是用 BOS 和 EOS token 来做的</b>」 ⇒ <b>两者的角色对称而不同：EOS 回答「什么时候停」（那个学生早先问的问题）,BOS 回答「从哪开始」—— 解码的第一步总得有个输入</b>。<br>⭐ 然后他聚焦到每个 token 携带什么：「<b>你有它的 embedding —— 那是学出来的</b>」 ⇒ <b>这就是那张嵌入表；区别只在于 Word2vec 里它是用代理任务单独训的，而在 transformer 里它和整个模型一起训</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("90:42","you have some added information that is in the form of a position embedding",166);
  says("91:07","So now you have a position-aware embedding for your token",192);
  note("⭐ 那笔债在这里被具体地还上了",640,222,"y");
  boxNode(60,254,320,48,"token embedding","b");
  boxNode(420,254,120,48,"＋","d");
  boxNode(580,254,320,48,"position embedding","v");
  link(900,278,960,278);
  boxNode(960,254,240,48,"位置感知的嵌入","g");
  note("⚠ 注意是「加性地」加上去 —— 逐元素相加，不是拼接",640,330,"r");
  note("原论文用的是一组正弦和余弦",640,370,"d");''',
         "<b>前面欠下的那笔债，在这里被具体地还上了。</b><br>⭐ 「<b>为了有一个关于『这个 token 在序列里处于什么位置』的概念，你有一些额外加上去的信息，形式是一个 position embedding；而原论文用的约定是一组正弦和余弦，它把它们『加性地』加到那个表示上 —— 所以这就像一次逐元素的加法</b>」。<br>⚠ 请特别留意「<b>加</b>」这个字：<b>不是拼接（那会改变维度）,而是逐元素相加 ⇒ 维度完全不变，位置信息被「掺」进了同一组数字里</b>。<br>⇒ 于是你得到一个「<b>位置感知的（position-aware）嵌入</b>」:<b>它既携带「我是哪个词」,也携带「我在第几位」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("91:07","So now you can see all of these embeddings in the format of a matrix",166);
  note("⭐ 走查里第一个要记住的形状 —— 后面每一步都在它上面做文章",640,196,"y");
  boxNode(340,228,600,50,"X：n × d_model","b");
  note("n = 序列长度（有多少个 token）  ｜  d_model = 嵌入维度（比如 768）",640,304,"y");
  note("⭐ 每一行是一个 token，每一列是嵌入的一个维度",640,344,"g");
  note("⚠ 这两个符号会用到整门课结束 —— 现在就把它们钉死",640,384,"r");''',
         "<b>这是走查里第一个要记住的形状，而后面每一步都在这个形状上做文章。</b><br>⭐ 「<b>现在你可以把所有这些嵌入看成一个矩阵的格式 —— 它的大小是 d_model，也就是你嵌入的大小；而另一个维度是序列的长度，通常是 n</b>」。<br>⭐ 两个符号正式登场，<b>它们会用到整门课结束</b>:<b>d_model = 嵌入维度（就是前面那个 d，比如 768）;n = 序列长度</b> ⇒ <b>而 X 是 n × d_model：每一行是一个 token，每一列是嵌入的一个维度</b>。<br>⚠ 接下来几镜会出现的形状，可以先记一下：<b>Q、K、V 各是 n × d_k；而 QKᵀ 是 n × n —— 全场唯一一个两个维度都是 n 的矩阵</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("91:39","So now we will send this representation through the encoder",166);
  says("92:21","you can apply the formula that Afshine mentioned, that is the self-attention formula",192);
  note("⭐ 进 encoder：同一份输入，投到三个空间",640,222,"y");
  boxNode(460,250,360,46,"X：n × d_model","b");
  link(500,296,230,322);
  link(640,296,640,322);
  link(780,296,1050,322);
  boxNode(110,322,240,46,"× W_q ⟹ Q","y");
  boxNode(520,322,240,46,"× W_k ⟹ K","v");
  boxNode(930,322,240,46,"× W_v ⟹ V","g");
  note("⚠ 三者同源 —— 这正是「self」的含义；而三个投影矩阵都是学出来的",640,384,"r");''',
         "<b>进 encoder 的第一步，而它把前面那个抽象说法变成了三个具体的矩阵。</b><br>⭐ 「<b>你拿这个输入，把它投影到三个空间上：投到空间 W_q 得到 queries，把同样的那些嵌入投到 W_k 得到 keys，对 values 做同样的事</b>」 ⇒ <b>「同样的那些嵌入」这几个字就是「self」的含义：Q、K、V 全都来自同一份输入</b>。<br>⭐ 然后就可以套公式了：「<b>softmax of Q K transpose over square root of d_k, times V —— 它从这一切里给你另一个矩阵</b>」。<br>⚠ 「<b>另一个矩阵</b>」这句话里有信息：<b>输出还是一个矩阵，而且形状和输入一样 —— 这一点后面会被说成「维度不变」</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("92:42","Now let us pause for a second and look at how this computation is done in practice",166);
  says("93:07","When you say k transpose, it is basically the same matrix, but transposed",192);
  note("⭐ 为什么要转置：为了让「行乘列」正好是「query 对 key」",640,222,"y");
  boxNode(80,254,500,50,"Q：n × d_k","y");
  boxNode(700,254,500,50,"Kᵀ：d_k × n","v");
  note("每一行是一个 query",330,328,"y");
  note("每一列是一个 key",950,328,"v");
  note("⚠ 矩阵乘法的规则是「左边的行 × 右边的列」—— 于是每一次乘正好是一次 query·key",640,374,"r");''',
         "<b>Shervine 把计算逐块拆开，而他的问法很好：你得到了什么？</b><br>⭐ 先看 Q：「<b>当你计算 Q 时，你基本上是把你的嵌入投影到那个空间里。你得到了什么？你得到一个矩阵，它的每一行代表一个给定的 query</b>」 ⇒ <b>Q 是 n × d_k：n 行（每个 token 一行）,每行是一个 d_k 维的 query 向量</b>。<br>⭐ 再看 Kᵀ：「<b>它基本上是同一个矩阵，只是被转置了 —— 在那里，每一列代表每个 token 的 key 表示</b>」。<br>⚠ 转置这个动作的意义正在于让后面的乘法说得通：<b>矩阵乘法是「左边的行 × 右边的列」⇒ 每一次乘，正好是一个 query 和一个 key 做点积</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("93:25","So when you multiply each of them, you see that each row represents the projection of the query over each key",166);
  says("93:32","such that when you take the matrix multiplication and get the softmax of all of this",192);
  note("⭐ 相乘之后：一个 n × n 的矩阵，记录「每个 token 对每个 token」",640,222,"y");
  boxNode(140,254,460,50,"QKᵀ：n × n","r");
  link(600,279,700,279);
  boxNode(700,254,460,50,"softmax 之后：每一行一个概率分布","g");
  note("第 i 行第 j 个数 = 第 i 个 token 和第 j 个 token 有多相关",640,330,"y");
  note("⚠ 而这个 n × n 正是「复杂度是序列长度的平方」的全部来源",640,374,"r");''',
         "<b>相乘之后的结果，Shervine 一句话就说清了它的结构。</b><br>⭐ 「<b>每一行代表『这个 query 在每一个 key 上的投影』</b>」 ⇒ 翻译成具体的：<b>第 i 行有 n 个数，第 j 个数是「第 i 个 token 和第 j 个 token 有多相关」⇒ 整个矩阵是 n × n，完整记录了「每个 token 对每个 token」的关系</b>。<br>⭐ 而 softmax 之后：「<b>对每一个 query，你得到一个『query 在那些 key 上的投影』的概率分布 —— 每一行都会有这个</b>」 ⇒ <b>第 i 行是一组加起来为 1 的权重，告诉你「第 i 个 token 该把多少注意力分给第 j 个」</b>。<br>⚠ <b>这个 n × n 正是全课那句「复杂度是序列长度的函数」的全部来源</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("93:55","And I do not know if anyone asked the question regarding why do we scale by square root of dk",166);
  says("94:16","And basically, what you see is that these dot products has the dimension of key and queries grows",192);
  note("⭐ 那个缩放因子的理由 —— 而它比看上去重要",640,222,"y");
  boxNode(80,254,500,50,"维度 d_k 越大","r");
  boxNode(700,254,500,50,"所以要归一化","g");
  note("点积是 d_k 项相加 ⇒ 项越多，和越大",330,328,"r");
  note("除以 √d_k，把量级拉回来",950,328,"g");
  note("⚠ 不缩放的后果：点积过大 ⇒ softmax 极度尖锐 ⇒ 梯度几乎消失，训不动",640,374,"r");''',
         "<b>这是 Shervine 主动补的一个点，而他特意说「不知道有没有人问过」—— 说明他认为它值得讲。</b><br>⭐ 他先澄清了一件事：「<b>其实写成 d_q 也可以，因为矩阵乘法 —— 也就是这里的点积 —— 强制了 d_q 等于 d_k</b>」（query 和 key 要做点积，维度必须相同）。<br>⭐ 理由：「<b>随着 key 和 query 的维度变大，这些点积也会倾向于跟着变大，所以你想把这些点积归一化 —— 这就是为什么你要除以 key 的维度的平方根</b>」 ⇒ 直觉是：<b>点积是 d 项相加，项越多和越大；而对随机独立的项，和的标准差大致按 √d 增长 —— 所以除以 √d_k 正好把量级拉回来</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("94:37","And this is Afshine explained as having the query projected on the space of keys",166);
  note("⭐ 最后一步，闭合了「比 key、给权重、取 value」那条线",640,196,"y");
  boxNode(80,228,500,50,"softmax 的结果","g");
  link(580,253,700,253);
  boxNode(700,228,500,50,"× V","v");
  note("「于是你对每一个 query，最后得到一个 value 的加权和」",640,304,"y");
  note("⭐ 而输出的形状是 n × d_k —— 每个 token 还是一行，只是内容换了",640,348,"y");
  note("⚠ 换成了什么：它自己的表示，被整句话按相关度重新调配过一遍",640,386,"r");''',
         "<b>最后一步，而它正好闭合了前面那条「比 key、给权重、取 value」。</b><br>⭐ 「<b>现在你有了这一切的 softmax，你把它乘上矩阵 V —— 而这就是 Afshine 解释的那个：把 query 投影到 key 的空间上，然后乘以对应的 value ⇒ 于是你对每一个 query，最后得到一个 value 的加权和</b>」。<br>⭐ 输出的形状是 <b>n × d_k</b>:<b>每个 token 还是一行，只是内容换了 —— 换成了「它自己的表示，被整句话按相关度重新调配过一遍」</b>。<br>⚠ <b>这就是「上下文化」这件事在矩阵层面的全部内容：一次加权平均，权重由内容决定</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("95:20","So you are right, it is not just single one, one time that it is done",166);
  says("95:37","And at the end of this, you have another projection matrix that you call Wo",192);
  note("⭐ 多头完整走一遍：做 h 次 ⟶ 拼接 ⟶ 投回原维度",640,222,"y");
  seq(70,254,["h 组投影各做一次","并行","按列拼接","× W_o 投回 d_model"],"g",265,48);
  note("⭐ 于是整块是「n × d_model 进、n × d_model 出」—— 维度不变",640,332,"y");
  note("⚠ 而「维度不变」正是能把它一层层堆起来的前提",640,374,"r");''',
         "<b>多头在这里被完整交代了一遍，而重点在最后两步。</b><br>⭐ 「<b>它不是只做单独一次，它实际上是每次都做 —— 所有这些是并行做的，最后你得到 h 个这样的矩阵，然后你把它们按列拼接起来</b>」 ⇒ 拼完之后维度变成 h·d_k，<b>于是需要最后一步</b>：「<b>你有另一个投影矩阵，你叫它 W_o，它会把所有这些投影回嵌入原来的维度 —— 所以这是一种办法，让网络有一个维度不变的方式</b>」。<br>⚠ 「<b>维度不变（dimension-invariant）</b>」点出了要害：<b>多头注意力整块是「n × d_model 进、n × d_model 出」—— 而这正是能把它一层层堆起来的前提</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("96:24","So what makes it different?",166);
  says("96:57","So what makes it such that you do not have the same thing?",192);
  note("⭐ 回到那个追问：凭什么各头不一样？这次的回答完整得多",640,222,"y");
  boxNode(80,254,500,50,"约束？","r");
  boxNode(700,254,500,50,"那靠什么","g");
  note("「什么都没有。你没有任何约束」",330,328,"r");
  note("「那是梯度下降的魔法 —— 它有自由度，也有激励」",950,328,"g");
  note("⚠ 「它没有动机去复制同一个东西」—— 论证的是激励，不是机制",640,374,"r");''',
         "<b>那个追问在这里被完整回答了，而这个回答比前面那个好得多。</b><br>⭐ 「<b>那是什么让它们不一样？那是梯度下降的魔法。网络在最后有一个目标函数，它有自由度，它的激励是去建出一个有助于学习下一个词的表示 ⇒ 它没有动机去复制同一个东西、或者做同样的机制 —— 而这就是为什么实践中你看到模型会收敛到建出不同的表示</b>」。<br>⚠ 而他也诚实地承认了另一半：「<b>那么是什么让你不会得到同样的东西？什么都没有 —— 你没有任何约束。但『你让模型去进行的那种学习』的性质，使得它实践中就这么做了</b>」 ⇒ <b>这个论证讲的是「激励」而不是「机制」—— 值得学，也值得保持清醒</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("97:27","So now that we have gone through the self-attention layer, you have another component that is the FFN",166);
  says("98:11","And you do not have just one encoder module",192);
  note("⭐ FFN 的维度，和 Word2vec 正好相反；然后是堆叠",640,222,"y");
  boxNode(80,254,500,50,"Word2vec 的隐层","d");
  boxNode(700,254,500,50,"transformer 的 FFN","g");
  note("比输入输出更小 ⇒ 压缩",330,328,"d");
  note("比输入输出更大 ⇒ 先升维再降回来",950,328,"g");
  note("⚠ 而 encoder 不止一个：原论文是大写的 N 个，堆起来",640,374,"r");''',
         "<b>自注意力讲完，还有一个部件；而它的维度和 Word2vec 正好相反。</b><br>⭐ 「<b>当 Afshine 讲 Word2vec 时，你通常有一个比输入输出更小的维度；但这里，实际上隐层的维度比输入和输出都更大</b>」 ⇒ <b>Word2vec 那里「小」是为了逼出压缩；而这里「大」是为了给模型更多空间去做非线性变换，然后再降回来</b>。<br>⭐ 然后是堆叠：「<b>你不是只有一个 encoder 模块 —— 你实际上有 N 个（原论文里是大写的 N）;而在这一切的最后，你得到一组编码过的、上下文感知的嵌入</b>」。<br>⚠ 而这里有一个容易搞错的细节：<b>那组编码过的嵌入，会被喂给每一个 decoder</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("98:57","So how do we even start the decoding process?",166);
  says("99:51","And then you have what I mentioned to be the cross-attention",192);
  note("⭐ 解码起步，以及 decoder 里的三件事",640,222,"y");
  boxNode(50,254,270,46,"BOS 进来","b");
  boxNode(340,254,300,46,"① 因果自注意力","v");
  boxNode(660,254,290,46,"② cross-attention","g");
  boxNode(970,254,230,46,"③ FFN","y");
  note("只能看已解码的  ｜  K、V 来自 encoder，Q 来自上一层  ｜  让表示更丰富",640,324,"g");
  note("⚠ 「因果（causal）」就是前面那个 masked 的另一个名字 —— 不许看未来",640,374,"r");''',
         "<b>解码起步，而这里的「因果」正是前面那个 masked 的另一个名字。</b><br>⭐ 「<b>你从 BOS token 开始，基本上是在跟模型说：嘿，我们需要预测下一个词了，咱们开始吧</b>」 ⇒ 然后 decoder 里按顺序走三件事：<b>① 因果自注意力（只能看已经解码出来的）;② cross-attention ——「它把这些编码过的嵌入作为 key 和 value 输入，而 query 是从自注意力层出来的那些」;③ FFN，让表示更丰富</b>。<br>⚠ <b>第 ② 件正好印证那个通用记法：谁在提问谁就是 Q —— 这里 decoder 在问「输入里哪些要紧」,所以 Q 来自 decoder，K、V 来自 encoder</b>。", 0),
        (r'''clearScene();setEq(null);setBig(null);setCap(null);noTitle();
  says("100:32","And at the very end of the decoding process, you have a linear projection and a softmax layer",166);
  note("⭐ 最后一步，整个循环闭合 —— 本讲所有伏笔在这里收完",640,196,"y");
  boxNode(60,228,280,46,"线性投影","v");
  link(340,251,400,251);
  boxNode(400,228,280,46,"softmax","g");
  link(680,251,740,251);
  boxNode(740,228,440,46,"词表大小的概率分布","y");
  note("⭐ 取出那个 token，把它的嵌入放回 decoder，再预测下一个 —— 一遍又一遍",640,302,"y");
  note("⚠ 直到生成出 EOS 为止 —— 而「什么时候停」这件事本身也是学出来的",640,346,"r");
  note("⇒ 从分词、嵌入、位置、注意力到解码，这一讲是一条线走完的",640,386,"g");''',
         "<b>最后一步，整个循环闭合，而本讲的所有伏笔都在这里收完。</b><br>⭐ 「<b>在解码过程的最末尾，你有一个线性投影和一个 softmax 层，把『下一个词的预测』变成词表上的一个概率分布 ⇒ 然后你找到你的下一个 token，拿那个嵌入放回 decoder，继续下去 —— 一遍又一遍</b>」。<br>⭐ <b>而那个「词表大小的概率分布」,和 Word2vec 输出端的形状一模一样 —— 这一讲是一条线走完的</b>。<br>⚠ 停在哪：<b>直到生成出 EOS 为止；而「什么时候停」这件事本身也是学出来的 ——EOS 和别的 token 一样参与训练，只是词表里的又一个位置</b>。", 0)],
       {"h": "⭐ label smoothing 与端到端走查",
        "k": "label smoothing：<b>「在 NLP 里，当你想预测接下来是什么时，通常不止一种方式」⇒ 「不是说 100% 预测这个词、没有别的词，而是说预测这个词，但有一定机会它不是这个词」—— 实践中是「不说你需要预测的是 (1,0,0,0)，而说其实是 1 减去 epsilon，然后那些是 epsilon 除以 v 减 1」; 「实践中作者们看到它倾向于提升像 BLEU 这样的指标」</b>;一个混淆点：<b>「softmax 不是已经免费给了这个吗？」——「归根结底你想做的是把你的预测和标签去比较⋯⋯问题是你想和 (1,0,0,0) 比，还是和某个不是它的东西比」</b>。<br>走查（Shervine）:<b>① 分词「可以用任意的分解方式」,加上 BOS / EOS；② 每个 token 的表示 =「它的 embedding —— 那是学出来的」+「一个 position embedding⋯⋯把它们『加性地』加到那个表示上」⇒ 得到「位置感知的嵌入」; ③ 「把所有这些嵌入看成一个矩阵的格式 —— 大小是 d_model，另一个维度是序列长度 n」; ④ 「把这个输入投影到三个空间上」得到 Q / K / V ⇒ 套公式「softmax of Q K transpose over square root of dk, times V」; ⑤ 逐块读：「Q 的每一行代表一个 query」「Kᵀ 的每一列代表每个 token 的 key」「相乘之后每一行代表这个 query 在每一个 key 上的投影」「softmax 之后对每一个 query 得到一个概率分布」; ⑥ 缩放 ——「随着 key 和 query 的维度变大，这些点积也会倾向于跟着变大，所以你想把它们归一化」; ⑦ 多头 ——「并行做 h 次，按列拼接」,再「用另一个投影矩阵 W_o 投影回嵌入原来的维度」; ⑧ FFN「隐层的维度比输入和输出都更大」,而 encoder 有 N 个堆起来；⑨ 解码从 BOS 开始，走因果自注意力 ⟶ cross-attention（K、V 来自 encoder）⟶ FFN；⑩ 「最末尾有一个线性投影和一个 softmax 层，把下一个词的预测变成词表上的一个概率分布」,然后一遍又一遍</b>。",
        "m": "⭐ 位置编码是「<b>加</b>」不是「拼接」:<b>逐元素相加 ⇒ 维度完全不变，位置信息被「掺」进同一组数字里</b>。<br>⭐ 三个形状把整条流水线钉死：<b>X 是 n × d_model（每行一个 token）· Q / K / V 各是 n × d_k · QKᵀ 是 n × n（全场唯一两个维度都是 n 的）—— 而那个 n × n 正是「复杂度是序列长度的平方」的全部来源</b>。<br>⭐ 缩放因子的理由：<b>点积是 d_k 项相加，项越多和越大；对随机独立的项，和的标准差按 √d 增长 ⇒ 除以 √d_k 正好拉回量级。不缩放则 softmax 极度尖锐、梯度几乎消失</b>。<br>⭐ 而 <b>W_o 的作用是「维度不变」</b>:<b>多头整块是「n × d_model 进、n × d_model 出」—— 这正是能把它一层层堆起来的前提</b>。",
        "w": " 多头「各头不一样」<b>没有任何机制上的保证</b>:<b>「什么都没有，你没有任何约束」—— 靠的是「它没有动机去复制同一个东西」这个激励论证 ⇒ 值得学，也值得保持清醒</b>。<br>⚠ 而 <b>softmax 和 label smoothing 在式子的两边</b>:<b>前者作用在模型「输出」那一侧，后者作用在你拿来「比对」的真值那一侧 —— 互相替代不了</b>。<br>⚠ FFN 的隐层维度<b>和 Word2vec 正好相反</b>:<b>那里「小」是为了逼出压缩，这里「大」是为了给非线性变换更多空间，然后再降回来</b>。",
        "r": "⇒ 这一段值得花最多时间，因为<b>前面讲的是「这个部件在做什么」,而走查讲的是「它们怎么串成一条真的能跑的流水线」—— 形状（每个矩阵多大、每行每列代表什么）只有在走查里才看得见</b>。<br>⇒ 而最后那个「词表大小的概率分布」<b>和 Word2vec 输出端一模一样</b> —— 这一讲是从「怎么切文本」一条线走到「怎么生成下一个词」的。<br>⇒ 另外 BLEU 被叫做「<b>代理指标</b>」,和「代理任务」同一个词根：<b>不是我们真正关心的，但它好测、而且和我们关心的相关</b>。<br>⇒ 更多（label smoothing 与探索/利用、各头为什么会分化、N 个 encoder 与 decoder 怎么连、每个矩阵的完整形状表）见<b>深度笔记</b>。",
        },
       {"t": "走查里 QKᵀ 是什么形状、代表什么？而为什么要除以 √d_k？",
        "o": ["是 d_k × d_k，代表投影矩阵；除以 √d_k 是为了省显存",
              "是 n × n（全场唯一两个维度都是 n 的矩阵），第 i 行第 j 个数是「第 i 个 token 和第 j 个 token 有多相关」；而除以 √d_k 是因为点积是 d_k 项相加、维度越大点积越大，不缩放会让 softmax 极度尖锐、梯度几乎消失",
              "是 n × d_model，代表上下文化后的表示；除以 √d_k 是为了归一化长度",
              "是 d_model × d_model，代表权重；除以 √d_k 是论文里的经验值"],
        "a": 1,
        "w": "⇒ 而那个 n × n 正是全课那句「复杂度是序列长度的函数」的全部来源。另外多头最后那个 W_o 的作用是「维度不变」——它是能把注意力一层层堆起来的前提。"})
