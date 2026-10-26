# -*- coding: utf-8 -*-
"""M3 T2《训练神经网络》逐页精读 —— 第 1–11 页（教学段）。

素材：M3材料/课件/M3T2_Activation_Loss.pptx（21 张，裁掉 p2 致辞页 ⇒ 20 页）
⭐ 这份**有 pptx，所以有备注讲稿**（Purpose / Explanation / Study check / Sources），
   信息量比正文大得多，很多考点只写在讲稿里（例如 p10 那句「practical 用的是
   MLPClassifier + L-BFGS，不是手算那条梯度下降规则」）。

⚠ 数字全部取自 M3材料/笔记与阅读/ 的讲义整理，并已被
  `M3材料/笔记与阅读/_src/verify_m3.py` 复算过（165/165 通过）。
字段见 [[slide-reader]]：r/t/star/one/quote/eq/pts/tbl/say/exam/tip
⚠ 选项里一律不许出现 <b>（泄题），答案位置由 build 时打散。
"""

PART_A = [

{"r": [1, 1], "t": "这一讲把 T1 的那条链加宽", "star": 1,
 "one": "T1 让一个神经元走完「前向 → 损失 → 梯度 → 更新」；T2 问的是同一个损失怎么喂给隐藏层，以及这件事怎么变成代码。",
 "quote": "<b>Training Neural Networks</b> — <em>Activation, loss, hidden gradients and implementation</em>（M3 Topic 2）",
 "pts": [
   "<b>副标题四个词就是这一讲的四块</b>：<em>activation</em>（激活函数选什么）、<em>loss</em>（损失函数配什么）、<em>hidden gradients</em>（隐藏层怎么拿到梯度）、<em>implementation</em>（这一切在代码里长什么样）。",
   "<b>和 T1 的关系</b>：讲稿原话——<em>Topic 1 ended with an output-layer update. This topic asks how the same loss supplies gradients to hidden weights.</em> ⭐ <b>注意是「同一个损失」</b>：隐藏层没有自己的目标，它靠链式法则从最终损失那里拿方向。",
   "⚠️ <b>这一讲的新东西其实只有两个</b>：① 激活与损失的<b>选择与搭配</b>（T1 只用了 sigmoid + BCE 一种）；② 梯度要<b>穿过隐藏层</b>。剩下的 batch/epoch 与自动微分是把前两件事放大到一批数据上。",
   "⚠️ <b>原课件第 2 页是 Acknowledgement of Country，裁页时已去掉</b>。所以这份精读的页码从第 2 页起比原课件少 1（本页 p2 = 原 p3），每页右下角的页码可以对照。",
 ],
 "exam": "M3 测验 110 分钟、20 选择（每题 3 分）+ 4 道扩展题（每题 10 分），<b>开卷</b>，Week 13（11 月 9–15 日）。T2 在考纲里占六条：<b>sigmoid/tanh/ReLU 及导数、饱和与梯度行为、MSE 与交叉熵、四种任务的输出层与损失、部分隐藏层权重的梯度、batch·epoch·自动微分</b>——这六条正好对应本讲 p4、p6、p7、p5/p15、p8、p9/p10。",
 "tip": {"t": "这一讲最值钱的一页", "v": "如果只看一页，看 <b>p8</b>：它把隐藏层梯度压成一个公式 <b>∂L/∂wⱼᵢ = (p − y)·vⱼ·g′(zⱼ)·xᵢ</b>，扩展题照着它逐因子写就能拿满结构分。", "w": 0},
},

{"r": [2, 2], "t": "六段路线图，也是复习顺序", "star": 2,
 "one": "激活 → 损失 → 隐藏梯度 → 批量与 epoch → 实现 → Tutorial 与 Practical，讲稿明确要求按这个顺序学。",
 "quote": "<b>Study activation function, loss function, how a hidden layer learns, and from one update to a training process in that order.</b>",
 "pts": [
   "<b>六段标题本身就是答题提纲</b>：<em>Activation choices</em>（比形状和局部斜率）、<em>Loss choices</em>（匹配目标与输出含义）、<em>Hidden gradients</em>（把损失追过一个隐藏神经元）、<em>Batches and epochs</em>（组织样本与重复更新）、<em>Implementation</em>（公式映射到数组与自动微分）、<em>Tutorial &amp; Practical</em>。",
   "⭐ <b>第 1 段和第 2 段的措辞要分清</b>：激活比的是「<b>函数形状</b>与<b>局部斜率</b>」——形状管前向、斜率管反向；损失匹配的是「<b>目标</b>与<b>输出的含义</b>」——不是哪个损失更好，是哪个和任务对得上。",
   "⚠️ <b>讲稿透露了 Tutorial 的结构</b>：<em>The tutorial has its four original questions plus the transferred hidden-layer question</em>——原来的四题<b>加上一道从别处挪过来的隐藏层题</b>。到 p13 讲稿又明确说<b>只有 Q1–Q3，没有单独的 Q4</b>，可见题目被重新合并过。",
   "<b>Course reading 链接</b>：<code>learn.adelaide.edu.au/courses/30362/pages/module-3-topic-2-overview</code>。本讲每一页讲稿末尾都带这样一条，指向 Canvas 对应页面——<b>本地抓下来的版本在 <code>M3材料/笔记与阅读/</code> 的 11 份 markdown 里</b>。",
 ],
 "tbl": [{"cap": "六段 ↔ 它在课件哪几页展开 ↔ 对应考纲哪一条",
   "head": ["段", "展开在", "考纲条目"],
   "rows": [
     ["1 Activation choices", "p3–p6", "sigmoid、tanh、ReLU 及导数；饱和与梯度行为"],
     ["2 Loss choices", "p7", "MSE 与交叉熵；四种任务的输出层与损失"],
     ["3 Hidden gradients", "p8", "部分隐藏层权重的梯度"],
     ["4 Batches and epochs", "p9", "batch、epoch"],
     ["5 Implementation", "p10", "自动微分"],
     ["6 Tutorial & Practical", "p13–p20", "（练习，不单独考）"],
   ]}],
 "exam": "选择题爱考「这一讲和 T1 的分工」。标准答法：<b>T1 在输出层做完一次更新；T2 问同一个损失怎样把梯度送到隐藏权重，再把重复更新变成实现</b>。",
},

{"r": [3, 3], "t": "没有非线性，叠多少层都还是一层", "star": 3,
 "one": "W₂(W₁x+b₁)+b₂ 还是一个仿射映射 —— 光加深度，不会多出一条弯的边界。",
 "quote": "<b>Linear stack</b> — Affine maps collapse. <b>W₂(W₁x+b₁)+b₂ is another affine map.</b> Depth alone adds no curved boundary. Gradients are simple but expressiveness is limited.",
 "eq": "无激活：  h = W₁x + b₁,  s = W₂h + b₂\n       ⇒ s = W₂W₁x + (W₂b₁ + b₂)  ← 仍是「一个矩阵乘 + 一个偏置」\n\n带数字（讲义版）： h = 2x + 1,  s = 3h + 4\n       ⇒ s = 3(2x+1) + 4 = 6x + 7   ← 两层塌缩成一层",
 "pts": [
   "<b>「塌缩」的意思</b>：两层仿射复合起来，<b>仍然是一个仿射函数</b>（affine = 加权和 + 偏置）。所以存在一个单层网络，<b>对任何输入都给出完全相同的输出</b>——多出来的那一层一点表达能力都没加。",
   "⭐ <b>课件把代价说得很全</b>：<em>Gradients are simple but expressiveness is limited</em>——<b>梯度确实好算，但表达力被限死了</b>。这不是「线性网络算不出来」，而是「它能表示的函数集合太小」。",
   "<b>插入非线性之后</b>：<em>h = g(Wx+b)</em>，课件说 <em>Different regions can respond differently</em>——<b>不同的输入区域可以有不同的响应</b>。讲义里那个带数字的例子最直观：把 h 换成 <b>max(0, 2x+1)</b> 之后，<b>x ≤ −0.5 那一段是平的（s = 4），x &gt; −0.5 那一段是 6x + 7</b>，两段在 x = −0.5 处接上，<b>出现一个折点</b>。",
   "⚠️ <b>最后一句是考点</b>：<em>Choice affects gradient flow and output meaning</em>——<b>选哪个激活，同时影响「梯度怎么流」和「输出是什么含义」</b>。这句话把本讲前两块（激活、损失）的因果关系点明了。",
   "⚠️ <b>别把这条和 T1 的「边界是直线」混为一谈</b>。T1 说的是<b>单个 sigmoid 神经元</b>的决策边界必然是直线；这一页说的是<b>多层但没有隐藏激活</b>时，整个网络塌缩成单层，所以边界<b>还是</b>直线。两者的结论一样，<b>原因是同一个</b>：送进最后那个 sigmoid 之前的分数仍是输入的仿射函数。",
 ],
 "say": "⭐ <b>讲义给了一个很漂亮的追问</b>：「只在最后放个 sigmoid 行不行？」答案是<b>不行</b>——sigmoid 让<b>概率输出</b>变成非线性，但它的 0.5 阈值仍然对应<b>分数为零</b>，而那个分数还是输入的仿射函数，所以<b>边界依旧是一条直线</b>。⚠️ 讲义还补了一句措辞很讲究的限定：<b>限制来自「仿射分数 + 单调激活 + 固定阈值」这个组合</b>，不是单纯因为「只有一个神经元」。",
 "exam": "⭐ <b>这是 T2 最稳的选择题之一</b>。常见干扰项是「加深度就能画出弯边界」「只要最后有 sigmoid 就够了」。标准答法两句：<b>① 仿射复合仍是仿射，等价于一个单层；② 必须有非线性的隐藏激活，输出分数才可能不是输入的仿射函数。</b>扩展题可能让你<b>代一组数字验证塌缩</b>（例如 h = 4x − 1、s = 2h + 5 ⇒ s = 8x + 3）。",
},

{"r": [4, 4], "t": "激活函数有两个身份：前向的值和反向的斜率", "star": 3,
 "one": "g(z) 往下一层传，g′(z) 乘在传回来的梯度上 —— 这两件事互不相干，必须分开记。",
 "quote": "<b>An activation must be understood as both a forward function and a local derivative.</b> … Sigmoid and tanh derivatives approach zero in saturated regions. ReLU positive → gradient remains 1. ReLU negative → zero gradient; <b>dead-unit risk</b>.",
 "eq": "σ(z) = 1/(1+e^(−z))        σ′(z) = σ(z)·(1−σ(z))\ntanh(z)                    tanh′(z) = 1 − tanh²(z)\nReLU(z) = max(0, z)        ReLU′(z) = 1 (z>0)，0 (z<0)\nLeaky(z) = max(αz, z)      Leaky′(z) = 1 (z>0)，α (z<0)\n\n⚠ 本课约定： ReLU′(0) = 0 ，  LeakyReLU′(0) = α = 0.01",
 "pts": [
   "<b>两个身份分别管什么</b>：<em>forward function</em> g(z) 决定<b>往下一层传什么值</b>；<em>local derivative</em> g′(z) 决定<b>反向时乘多少倍</b>。⭐ 讲义把这句话说得更狠：<b>大的输出不代表大的梯度</b>（a large output need not imply a large gradient），两件事互不相干。",
   "⚠️ <b>z = 0 处的约定必须记死</b>。讲稿原话：<em>At z=0 the mathematical derivative is undefined; the worksheet uses 0 as its implementation convention.</em> —— <b>数学上不可导，本课（和 worksheet）一律用 0</b>。Leaky ReLU 在 0 处则用 α。各家软件约定不同，<b>考试按本课的判</b>。",
   "<b>饱和（saturation）</b>：sigmoid 和 tanh 在 |z| 很大时导数趋近 0。连乘很多层就产生<b>梯度消失</b>——讲义给的量级感是<b>五个 0.1 连乘 = 0.00001</b>。",
   "⚠️ <b>但讲稿给了一条很重要的限定</b>：<em>A negative ReLU score blocks this local gradient for this observation; it does not alone prove the neuron is permanently inactive across all inputs.</em> —— <b>「这个样本上梯度被挡住」不等于「这个单元死了」</b>。要在相关的那批输入上<b>一直</b>不激活才叫死亡 ReLU。",
   "⚠️ <b>tanh 的两个坑</b>：① 它<b>不是</b>三角函数里的正切，是双曲正切 (e^z − e^(−z))/(e^z + e^(−z))，用计算器的 hyperbolic 键；② 讲稿专门加了 <em>Tanh's symmetric range does not guarantee a zero empirical mean</em>——<b>输出范围关于零对称 ≠ 实际激活的均值为零</b>。",
 ],
 "tbl": [{"cap": "三个点上的数值表（最可能直接出计算题；每格是「输出 / 导数」）",
   "head": ["函数", "z = −2", "z = 0", "z = 2", "值域"],
   "rows": [
     ["Sigmoid", "0.119 / 0.105", "0.500 / 0.250", "0.881 / 0.105", "(0, 1)"],
     ["tanh", "−0.964 / 0.071", "0 / 1", "0.964 / 0.071", "(−1, 1)"],
     ["ReLU", "0 / 0", "0 / 0 ←约定", "2 / 1", "[0, ∞)"],
     ["Leaky ReLU (α=0.01)", "−0.02 / +0.01", "0 / 0.01 ←约定", "2 / 1", "(−∞, ∞)"],
   ]}],
 "say": "⚠️⚠️ <b>Leaky ReLU 在 z = −2 那一格是本讲最爱考的陷阱</b>：<b>输出是负的（−0.02），导数却是正的（+0.01）</b>。讲义原话：<b>输出的符号和斜率的符号是两回事。</b> 配套的自测：传入损失梯度 0.6 时，<b>过 ReLU 传出 0.6 × 0 = 0（这条路径彻底断了）</b>，<b>过 Leaky ReLU 传出 0.6 × 0.01 = 0.006（很小，但没断）</b>。",
 "exam": "⭐⭐ <b>这张表必须会默写</b>。选择题形态：给一个 z 问输出或导数；给「tanh 输出 −0.6」问导数（答 1 − 0.36 = <b>0.64</b>，别套成 sigmoid 的 g(1−g)）；问 ReLU′(0)（答 <b>0</b>）。扩展题里它是中间步骤——算隐藏层梯度时第 ③ 步就要乘 g′(zⱼ)。",
 "tip": {"t": "两个最容易写反的导数", "v": "<b>σ′ = g(1−g)</b>（sigmoid），<b>tanh′ = 1 − g²</b>。两个都用「输出本身」表示，所以很容易张冠李戴。记法：sigmoid 的输出在 (0,1)，<b>g 和 1−g 都是正的、相乘才有意义</b>；tanh 输出在 (−1,1)，<b>平方才保证非负</b>。", "w": 1},
},

{"r": [5, 5], "t": "按「层的角色」选激活：先定输出，再定隐藏", "star": 2,
 "one": "四步顺序是固定的：认任务 → 定输出层 → 定隐藏层 → 训练中监控。",
 "quote": "<b>Hidden-layer and output-layer requirements are different.</b> 1 Identify output: continuous, binary, single-label or multi-label → 2 Choose output: linear, sigmoid or softmax as appropriate → 3 Choose hidden: <b>ReLU is a strong baseline</b>; tanh can suit bounded states → 4 Monitor training: inspect saturation, dead units and validation performance.",
 "pts": [
   "⭐ <b>顺序不能反</b>：先看<b>目标是什么类型</b>，再定输出层，<b>最后</b>才轮到隐藏层。原因很直白——输出层由<b>任务</b>决定（没得选），隐藏层是<b>调参</b>（有得选）。",
   "<b>第 3 步的措辞值得记</b>：<em>ReLU is a strong baseline; tanh can suit bounded states</em>——<b>ReLU 是强基线，tanh 适合「有界状态」</b>。⚠️ 注意课件没有说「ReLU 最好」，它说的是 baseline（默认起点）。",
   "⚠️ <b>第 4 步常被忽略，但它是 T3 的接口</b>：<em>inspect saturation, dead units and validation performance</em>——要看三件事：<b>有没有饱和、有没有死单元、验证表现如何</b>。前两个是本讲的内容，<b>第三个直接指向 T3 的训练/验证证据</b>。",
   "<b>隐藏层和输出层的根本区别</b>：隐藏层的激活是为了<b>造表示</b>（让后面的层能用上非线性的中间特征）；输出层的激活是为了<b>让输出有正确的含义</b>（概率要落在 (0,1)、多类概率要和为 1）。⚠️ 所以 <b>ReLU 不能做二分类输出层</b>——它的输出无上界，不是概率。",
 ],
 "exam": "选择题常考「给一个任务描述，选输出层」。⭐ <b>先问自己三句</b>：目标是连续的还是离散的？离散的话类别<b>互斥</b>吗？互斥的话标签存成<b>整数</b>还是 <b>one-hot</b>？三问答完，输出层和损失就定了（配对表见 p7 和 p15）。",
},

{"r": [6, 6], "t": "每个常用激活都有代价", "star": 3,
 "one": "四个激活各有一条短板，课件把它们并排列出来 —— 考试爱考「哪一句描述是对的」。",
 "quote": "<b>Sigmoid</b> — Saturates and is not zero-centred. <b>Tanh</b> — Zero-centred but still saturates. <b>ReLU</b> — Can create permanently inactive units. <b>Leaky ReLU</b> — Nonzero slope for negative inputs; choose its size. <b>Output mismatch</b> — Wrong range can make predictions uninterpretable.",
 "pts": [
   "<b>Sigmoid 的两条短板</b>：<em>saturates</em>（两端导数趋近 0）<b>而且</b> <em>is not zero-centred</em>（输出全是正的，落在 (0,1)）。⚠️ 第二条常被忽略——输出恒正会让后一层的权重梯度<b>符号一致</b>，更新方向受限。",
   "<b>Tanh</b>：<em>zero-centred but still saturates</em>——<b>解决了「不以零为中心」，没解决饱和</b>。所以 tanh 是 sigmoid 的改良，不是替代品。",
   "<b>ReLU</b>：<em>can create permanently inactive units</em>——注意措辞是 <b>can</b>（可能），不是 will。配合 p4 讲稿那句「单个观测不激活不等于死了」，<b>这两处合起来才是完整的说法</b>。",
   "<b>Leaky ReLU</b>：<em>nonzero slope for negative inputs; choose its size</em>——<b>负侧有一个非零斜率，而且这个斜率的大小要你自己选</b>。⚠️ 讲稿补了一句很重要的：<em>The incoming loss gradient is multiplied by alpha; it is not necessarily negative.</em>——<b>传入的梯度乘以 α，结果不一定是负的</b>（乘一个小正数不改变符号）。",
   "⭐ <b>第五条「Output mismatch」是另一个层级的问题</b>：<em>Wrong range can make predictions uninterpretable</em>——<b>输出范围选错了，预测就没法解释</b>。这不是「训练得慢」，是「算出来的数根本不是你以为的那个东西」。例如用 ReLU 做二分类输出，得到 3.7，它既不是概率也不是类别。",
 ],
 "tbl": [{"cap": "四个激活的取舍一览",
   "head": ["激活", "优点", "短板", "典型用处"],
   "rows": [
     ["Sigmoid", "输出就是概率，落在 (0,1)", "会饱和；输出不以零为中心", "二分类输出层"],
     ["tanh", "以零为中心，范围 (−1,1)", "仍然会饱和", "隐藏层（有界状态）"],
     ["ReLU", "正半轴不饱和、算得快", "负输入零梯度，可能永久不激活", "隐藏层默认起点"],
     ["Leaky ReLU", "负侧保留 α 的斜率，缓解死亡", "α 要自己选；仍非零中心", "ReLU 死单元多时"],
   ]}],
 "exam": "⭐⭐ <b>「哪一句描述正确」型选择题的高发区</b>。几个标准错项：「tanh 不会饱和」（错，只是零中心）、「ReLU 一定会产生死单元」（错，是 can）、「Leaky ReLU 的负输入会让梯度变成负的」（错，乘正的 α 不改符号）、「输出范围不影响结果，只影响速度」（错，会让预测无法解释）。",
},

{"r": [7, 7], "t": "损失函数定义「什么算错」", "star": 3,
 "one": "损失要同时匹配两件事：目标的类型，和输出的含义 —— 搭配错了，梯度会在最需要的地方变得极小。",
 "quote": "<b>The loss must match the target type and output interpretation.</b> For L_MSE = ½(y−p)² and p = σ(z): <b>∂L/∂z = (p−y)p(1−p)</b>. For sigmoid + BCE: <b>∂L/∂z = p − y</b>. The extra p(1−p) factor can make the MSE gradient small when sigmoid saturates. <b>Integer class labels → sparse categorical CE; one-hot labels → categorical CE.</b>",
 "eq": "sigmoid + 半平方误差：  ∂L/∂z = (p − y)·p(1−p)      ← 多出来的因子是祸根\nsigmoid + BCE：         ∂L/∂z = p − y               ← 干净\n\n算例  y = 1, p = 0.01（非常自信地判错）：\n  半平方： (0.01 − 1) × 0.01 × 0.99 = −0.009801\n  BCE：    0.01 − 1                = −0.99          ← 相差两个数量级",
 "pts": [
   "⭐⭐ <b>这一页最该记的是那两行梯度对比</b>。两者的<b>符号都主张抬高 logit</b>（都是负的，梯度下降会把 z 调大），但<b>半平方误差的幅度小了整整两个数量级</b>——因为 sigmoid 在 p = 0.01 处的斜率 p(1−p) ≈ 0.0099 本身就极小。",
   "<b>为什么这叫「搭配」问题</b>：BCE 的 −log 恰好把 sigmoid 的 p(1−p) 约掉了，所以<b>对一个「有把握但判错」的预测，BCE 给出的纠正梯度强得多</b>。这不是 BCE 单独的优点，是 <b>sigmoid + BCE 这一对</b>的优点。",
   "⚠️ <b>限定条件要跟着写</b>：讲义原话——<b>这个优势只针对这一对输出–损失的组合，BCE 并不能阻止深层网络中别处出现小梯度。</b>",
   "⚠️ <b>「半平方」不是 MSE</b>：ℓ = ½(y−p)² 对 p 的导数是 (p − y)；普通平方误差求导给 <b>2(p−y)</b>，在 N 个观测上取平均还多一个 <b>1/N</b>。<b>推导前先说清用的是哪个约定</b>，否则系数就错了。",
   "⭐ <b>标签编码那一句是考纲点名的</b>：<em>Integer class labels → sparse categorical CE; one-hot labels → categorical CE.</em> 两者<b>表示的是同一个计算</b>，只是接口不同。⚠️ 整数编码可能是 0–5 也可能是 1–6，<b>永远要核对映射关系</b>。",
 ],
 "tbl": [{"cap": "任务 ↔ 输出 ↔ 损失（课件 Match task to loss 那一栏）",
   "head": ["任务", "输出层", "损失", "要点"],
   "rows": [
     ["连续回归", "线性", "MSE 或 MAE", "MSE 单位是目标单位的平方；MSE→条件均值，MAE→条件中位数"],
     ["二分类", "一个 sigmoid", "BCE", "输出表示 P(y=1 | x)"],
     ["互斥多类", "softmax", "交叉熵", "概率和为 1；整数标签用 sparse 版"],
     ["多标签", "每标签一个 sigmoid", "每标签各一次 BCE", "和不必为 1；标签之间不必统计独立"],
   ]}],
 "say": "⭐ <b>softmax + 交叉熵的 logit 梯度也化简得很干净</b>：<b>∂ℓ/∂z_k = p_k − y_k</b>，把二分类的 p − y 推广到互斥多类。讲义给的算例：p = (0.1, 0.7, 0.2)、真实类别是 2 ⇒ 梯度 (0.1, <b>−0.3</b>, 0.2)，<b>三项加起来等于 0</b>（很好的自查）。⚠️ 这是<b>对 logit 的</b>导数，不是对概率、也不是对权重的。",
 "exam": "⭐⭐ <b>考纲逐条点名的两块都在这一页</b>（MSE 与交叉熵、四种任务的输出与损失）。扩展题常见问法：给一个任务描述，要你<b>写出输出层 + 损失 + 一句理由</b>；或者给 y = 1、p = 0.01，要你<b>比较两种搭配的梯度并解释差别的来源</b>。⚠️ 最后那句解释必须点出 <b>p(1−p) 在饱和区极小</b>。",
},

{"r": [8, 8], "t": "⭐ 隐藏权重通过最终损失学习（一条公式搞定）", "star": 3,
 "one": "∂L/∂wⱼᵢ = (p − y)·vⱼ·g′(zⱼ)·xᵢ —— 四个因子，每个因子都对应路径上的一步。",
 "quote": "<b>Scalar chain rule for one observation: ∂L/∂wⱼᵢ = (p − y) vⱼ g′(zⱼ) xᵢ</b>. wⱼᵢ connects input i to hidden unit j; vⱼ connects hidden unit j to the output. <b>All factors use the same forward pass and original parameters. Update only after gradients are ready.</b>",
 "eq": "路径：  wⱼᵢ → zⱼ → hⱼ → s → p → L\n\n    zⱼ = Σᵢ wⱼᵢ xᵢ + bⱼ        hⱼ = g(zⱼ)\n    s  = Σⱼ vⱼ hⱼ + c          p  = σ(s)        L = BCE(p, y)\n\n逐因子读：\n    p − y    输出分数的敏感度（sigmoid + BCE 化简的结果）\n    vⱼ       这个隐藏单元通往输出的连接权重\n    g′(zⱼ)   隐藏激活在该点的斜率（ReLU 时是 1 或 0）\n    xᵢ       这个权重对应的那个输入",
 "pts": [
   "⭐⭐ <b>这四个因子就是四步链式法则</b>，课件把它压成一行。考场上按 <b>① (p−y) → ② ×vⱼ → ③ ×g′(zⱼ) → ④ ×xᵢ</b> 逐步写，每一步说明乘的是哪个局部导数，结构分就拿到了。",
   "⚠️ <b>为什么上层权重 vⱼ 会出现在下层的梯度里</b>：因为<b>隐藏激活对损失的影响必须穿过输出层</b>，而 vⱼ 正是 s 对 hⱼ 的局部导数。没有它这条链就断了。",
   "⚠️⚠️ <b>课件专门强调的纪律</b>：<em>All factors use the same forward pass and original parameters. Update only after gradients are ready.</em> —— <b>所有因子都用同一次前向、同一组（更新前的）参数；全部梯度算完之后才更新</b>。中途换用新值，算的就不是这一点处的梯度。",
   "⭐ <b>ReLU 不激活时整条路径归零</b>：讲稿原话 <em>If hidden g is ReLU and zⱼ&lt;0, this path contributes zero.</em> 这会带来<b>两处「没变」</b>——该隐藏单元的输入权重梯度全为 0，<b>而且</b>它的输出权重梯度 = (p−y)·hⱼ = (p−y)·0 = 0 也是零。",
   "⚠️ <b>更大的图里要把多条路径相加</b>：<em>In larger graphs, add contributions from all downstream paths.</em> ——<b>一条路径内部相乘，多条路径汇合相加</b>。本讲的两层网络每个隐藏单元只有一条通往输出的路，所以看不到求和；三层以上就会出现。",
 ],
 "tbl": [{"cap": "讲义那个完整算例（x = [1,2]，y = 1，η = 0.1；数字已复算）",
   "head": ["步骤", "计算", "结果"],
   "rows": [
     ["隐藏 1（w=[0.2,0.4], b=0.1, ReLU）", "z₁ = 0.2(1) + 0.4(2) + 0.1", "1.1 ⇒ h₁ = 1.1（激活）"],
     ["隐藏 2（w=[−0.5,0.3], b=−0.2, ReLU）", "z₂ = −0.5(1) + 0.3(2) − 0.2", "−0.1 ⇒ h₂ = 0（不激活）"],
     ["输出（v=[0.7,−0.4], c=−0.1, sigmoid）", "s = 0.7(1.1) − 0.4(0) − 0.1", "0.67 ⇒ p = 0.661503"],
     ["① ∂L/∂s = p − y", "0.661503 − 1", "−0.338497"],
     ["② ×v₁ = 0.7", "−0.338497 × 0.7", "−0.236948"],
     ["③ ×g′(z₁)，z₁ > 0 ⇒ ×1", "不变", "−0.236948"],
     ["④ ×x₂ = 2", "−0.236948 × 2", "−0.473896 ⇒ w₁₂ → 0.447390"],
     ["整步更新后重新前向", "新 s ≈ 0.849619", "p = 0.700487，L = 0.355979"],
   ]}],
 "say": "⚠️ <b>讲稿最后一句点出了和 worksheet 的关系</b>：<em>This scalar rule matches the worksheet's matrix delta rule, where superscripts identify layers.</em> —— <b>这条标量规则和作业纸上的矩阵 δ 规则是同一回事</b>，矩阵版用<b>上标</b>标层号（W₁、W₂ 的下标在讲义里表示「第几层」，<b>不是幂次</b>）。考场上两种写法都可以，<b>标量版更不容易写错</b>。",
 "exam": "⭐⭐⭐ <b>M3 T2 Tutorial Q3 考的就是这个</b>（见 p18）。扩展题标准结构：① 写出路径 ② 四步逐个代数字 ③ 指出哪些参数这一步完全不动并解释原因 ④ 更新后<b>重新跑完整前向</b>给出新的 p ⑤ 加一句「这只证明在这一个样本上有改进，不是泛化的证据」。",
 "tip": {"t": "两处最容易丢的分", "v": "① 第 ② 步必须<b>说明那个 0.7 是输出权重</b>（隐藏激活的影响要穿过输出层），只写数字不说来源会扣分；② 算隐藏层梯度时用的是<b>原来的</b> v₁ = 0.7，<b>不是更新后的 0.737235</b>。", "w": 1},
},

{"r": [9, 9], "t": "batch 与 epoch 是两个不同的单位", "star": 2,
 "one": "batch 是「算一次更新所用的那组观测」，epoch 是「把训练集完整过一遍」—— 100 个样本、批大小 20，一个 epoch 就是 5 次更新。",
 "quote": "<b>A batch supplies one update; an epoch describes one pass through the training set.</b> 1 Forward → 2 Backward: calculate <b>fresh</b> gradients from this forward pass → 3 Update → 4 Repeat: use the next batch and <b>recompute all values</b>.",
 "eq": "一个 epoch 的更新次数 = 训练样本数 ÷ 批大小\n\n  100 个样本 / 批大小 20  ⇒  1 epoch = 5 次更新，3 epoch = 15 次\n  全批量（full-batch）     ⇒  每个 epoch 只更新 1 次\n\n平均损失：  L_batch = (1/N) Σₙ Lₙ        梯度数组 = (P − Y)/N\n⚠ 这个 1/N 只除一次，别在每一层再除一遍",
 "pts": [
   "⚠️ <b>讲稿把计数条件说全了</b>：<em>With 100 examples and batches of 20, one epoch contains five updates, <b>assuming no dropped or repeated observations</b>.</em> —— <b>前提是不丢样本也不重复取</b>。考试里如果样本数除不尽批大小，要说明最后一个批次怎么处理。",
   "<b>四步循环的两个关键词</b>：第 2 步是 <em>fresh</em> gradients（<b>新鲜的</b>梯度，从<b>这一次</b>前向算），第 4 步是 <em>recompute all values</em>（<b>把所有值重算一遍</b>）。⚠️ 复用旧激活或旧梯度，算出来的就不是当前这一点处的下降方向。",
   "⭐ <b>平均只做一次</b>：<em>For mean loss, divide the sum of individual gradients by the batch size N exactly once.</em> —— 讲稿用了 <b>exactly once</b>，可见这是个常见错误。",
   "⚠️⚠️ <b>最该带走的一句</b>：<em>Individual examples may favour different parameter changes; decreasing the mean does not mean every example improves.</em> —— <b>平均在降，不代表每个样本都变好</b>。讲义给的数值例子：两个样本对某参数的梯度是 −0.2 和 +0.6，<b>平均 +0.2</b>，梯度下降会<b>减小</b>这个参数——对第一个样本来说方向是反的。",
   "<b>和 T3 的接口</b>：讲义里那张「连续 100 次更新」的表就是这条的极端版——平均 BCE 从 0.580352 降到 0.369420，<b>但有一个正例的概率从 0.4750 只爬到 0.4859，始终在 0.5 阈值以下，一直判错</b>。原因是它的两个隐藏 ReLU 从一开始就是零。",
 ],
 "exam": "⭐ <b>计数题几乎必出，而且是送分题</b>：给样本数和批大小，问一个 epoch 多少次更新、几个 epoch 多少次。⚠️ 概念题的高发点是「平均损失下降 = 每个样本都改善」——<b>这是错的</b>。",
},

{"r": [10, 10], "t": "公式、数组与自动微分：存法变了，算法没变", "star": 3,
 "one": "手推把输入当列、代码把观测当行，所以代码里的权重矩阵是手推版本的转置 —— 转置只是行列互换，网络本身没变。",
 "quote": "<b>The storage convention changes; the underlying computation stays the same.</b> Rows store observations in Python. <b>X: (N,d); W: (d,h); b: (h,)</b>. Z = X @ W + b has shape (N,h). The column-input equation uses Wᵀ. … <b>Record a forward computation and its loss → Autodiff calculates parameter gradients → The optimiser applies the parameter update.</b>",
 "eq": "N = 批大小，d = 输入特征数，h = 隐藏单元数\n\n  代码（行 = 观测）：  X (N,d)   W (d,h)   b (h,)   ⇒  Z = X @ W + b  是 (N,h)\n  手推（列 = 输入）：  W 的形状是 (h,d)，即代码那个 W 的转置\n\n例： 3 个隐藏单元、2 个输入特征\n  手推矩阵 3×2        代码矩阵 2×3        输出权重的代码矩阵 3×1",
 "pts": [
   "⭐ <b>转置的来源只有一个</b>：手推时把一个输入写成<b>列</b>向量，代码里把每个观测存成<b>一行</b>。<b>转置只是行列互换，不改变网络本身</b>。",
   "⚠️ <b>一个会掩盖问题的巧合</b>：讲义那个例子里 W1 恰好是<b>方阵</b>（2×2），所以转置<b>不改变形状但确实挪动了元素</b>——形状检查通不过的问题被藏住了。换成 3 隐藏单元、2 输入就立刻暴露：手推 3×2，代码 2×3。",
   "<b>广播</b>：<em>Broadcasting adds the same bias vector to every observation.</em> —— b 的形状是 (h,)，加到 (N,h) 上时 NumPy 自动复制到每一行。",
   "⭐⭐ <b>自动微分的三个角色必须分清</b>（考纲明确要求）：<b>① 记录</b>——TensorFlow 的 <code>GradientTape</code> 记录涉及 <code>tf.Variable</code> 的前向运算；<b>② 求导</b>——<code>tape.gradient</code> 按链式法则返回梯度，<b>它不更新参数</b>；<b>③ 更新</b>——优化器（<code>assign_sub</code> / <code>optimiser.step</code>）才真正改参数。",
   "⚠️ <b>PyTorch 那一句是本页独有的</b>：<em>PyTorch loss.backward accumulates gradients. Clear accumulated gradients when the intended update should use only the current batch, and call the optimiser separately.</em> —— <b>backward 是累加的</b>，只想用当前批次时要先清零（<code>zero_grad</code>），而且优化器要<b>单独调用</b>。",
 ],
 "say": "⚠️⚠️ <b>这一页讲稿里藏着一句考点级别的话，正文里完全没有</b>：<em>The M3 T2 practical uses MLPClassifier with L-BFGS, which uses gradients but is not the simple gradient-descent rule used by hand.</em> —— <b>Practical 用的是 MLPClassifier + L-BFGS，它用梯度，但不是手算的那条 θ ← θ − η·∂L/∂θ</b>。⭐ 所以<b>「notebook 跑出来的结果和手算对不上」是正常的</b>，不是你算错了。另一句同样只在讲稿里：<em>Inspect array shapes and an intermediate value before trusting the result.</em>——<b>先查形状和一个中间值，再信结果</b>。",
 "exam": "⭐⭐ <b>自动微分「做什么、不做什么」是考纲明确点名的</b>。标准答法：<b>它追踪一次前向计算里的各个运算并应用链式法则求导数</b>；⚠️ <b>它不替你选一个有用的目标、不修复数据泄漏、也不保证学习率是好的；参数更新是优化器完成的。</b> 形状题也常考：N 个观测、2 个特征、3 个隐藏单元 ⇒ H 是 (N,3)、P 是 (N,1)、Y 是 (N,1)。",
},

{"r": [11, 11], "t": "Checkpoint：五个词自测", "star": 1,
 "one": "前向激活 / 局部梯度 / 隐藏梯度 / 批平均损失 / 训练循环 —— 盖住解释，先自己说一遍。",
 "quote": "Forward activation — compute g(z). Local gradient — compute g′(z). Hidden gradient — <b>multiply path derivatives; sum branches</b>. Batch mean loss — <b>average example losses once</b>. Training cycle — forward → backward → update → repeat.",
 "pts": [
   "<b>讲稿给了用法</b>：<em>Use each item as an active-recall prompt: cover the explanation, define the term, then uncover it to check your answer.</em> —— <b>盖住右边，先自己定义，再对答案</b>。这比重读一遍有效得多。",
   "⭐ <b>第三条把 p8 的规则压成两个动词</b>：<em>multiply path derivatives; <b>sum branches</b></em>——<b>沿路径相乘，遇到分叉相加</b>。这两个动词是整个反向传播的全部。",
   "<b>第四条那个 once 又出现了</b>：<em>average example losses <b>once</b></em>。课件在两页里重复同一个警告，说明这是高频错误。",
   "<b>课件原版还有一条「Saturation: large |z| can shrink gradients」</b>（在讲稿里），正文排版时被压掉了——<b>饱和也属于 checkpoint 的五个词之一</b>。",
 ],
 "exam": "这一页不出题，但它是<b>考前最后十分钟该看的那一页</b>：五个词能说清楚，T2 的概念题基本不会丢分。",
},

]
