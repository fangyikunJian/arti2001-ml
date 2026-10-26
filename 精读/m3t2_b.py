# -*- coding: utf-8 -*-
"""M3 T2《训练神经网络》逐页精读 —— 第 12–20 页（Tutorial 与 Practical 段）。

⭐ 这一段的价值在于：**T2 的 Tutorial PDF 本地还没有**（T1 的有、T2/T3 的没下到），
   而课件 p13–p18 把 Q1/Q2/Q3 的**结构、要求和评分口径**全写出来了，
   讲稿里还交代了「没有单独的 Q4」「extension 不计分」这类只有老师会说的信息。
   ⇒ 在拿到 Tutorial 原件之前，这六页就是最接近官方题型的材料。

⚠ 页码：本页 p12 = 原课件 p13（裁掉了致辞页）。
"""

PART_B = [

{"r": [12, 12], "t": "第 1 节收尾：五条要点 + 五条「上 Tutorial 之前先会」", "star": 2,
 "one": "左栏是知识点总结，右栏是 Tutorial 的入场要求 —— 右栏比左栏更该背。",
 "quote": "<b>Key Takeaways</b>: Activation and loss must match the task · Hidden weights learn through the final loss · Local slopes can shrink or block gradients · Batches combine examples before an update · Autodiff computes gradients; optimisers use them.<br><b>Ready for the Tutorial</b>: Calculate activation values before derivatives · <b>State the derivative convention at z=0 for ReLU</b> · <b>Distinguish total loss from mean loss</b> · Apply the correct BCE term for each label · Interpret why a confidently wrong prediction is costly.",
 "pts": [
   "⭐⭐ <b>右栏那五条是「会被扣分的点」清单</b>，比左栏的总结更值钱，因为它直接说了老师在批改时看什么。",
   "<b>① Calculate activation values before derivatives</b> —— <b>先算激活值，再算导数</b>。因为 σ′ = g(1−g)、tanh′ = 1 − g² 都要用到<b>输出本身</b>，顺序反了就得重算。",
   "<b>② State the derivative convention at z = 0 for ReLU</b> —— <b>要把 z=0 处的约定写出来</b>，不是默认它。本课约定 ReLU′(0) = 0、Leaky′(0) = α。⚠️ 这是一个<b>只要写上就有分、不写就没有</b>的点。",
   "<b>③ Distinguish total loss from mean loss</b> —— <b>区分总损失和平均损失</b>。看公式前面有没有 (1/N)Σ：有就是平均，没有就是单样本或总和。⚠️ 讲义的记号是 <b>ℓᵢ 单样本、L = (1/N)Σℓᵢ 平均</b>；而 <b>T1 里的 L 指的是单个观测</b>——跨 Topic 最容易混。",
   "<b>④ Apply the correct BCE term for each label</b> —— <b>按标签选对那一项</b>：y = 1 时只剩 −log p，y = 0 时只剩 −log(1−p)。⚠️ y = 0、p = 0.8 时正确类的概率是 <b>0.2</b>，损失 −ln(0.2) ≈ <b>1.609</b>，不是 −ln(0.8)。",
   "<b>⑤ Interpret why a confidently wrong prediction is costly</b> —— <b>要能解释「自信地判错」为什么代价大</b>。两层含义：损失上 −log(0.01) ≈ 4.6 很大；梯度上 BCE 给 p − y = −0.99 的强信号，而半平方只给 −0.0098。",
 ],
 "exam": "⭐ 这五条每一条都能单独成为扩展题的一个<b>得分点</b>。做题时把它们当 checklist：算完先自检「我写了 z=0 的约定吗」「我说清楚用的是总和还是平均吗」。",
},

{"r": [13, 13], "t": "第 2 节：Tutorial 只有三题（讲稿把结构说死了）", "star": 2,
 "one": "Q1 激活值与输出/损失选择、Q2 回归与分类损失及 logit 梯度、Q3 隐藏梯度与实现 —— 没有单独的 Q4，extension 不计分。",
 "quote": "Three core questions and one optional extension. Q1: activation values, behaviour and output/loss choices · Q2: regression and classification losses and logit gradients · Q3: hidden gradient, autodiff and batch/epoch counts · <b>Use the original network supplied within Q3</b> · Extension: full hidden gradients and saturation.",
 "pts": [
   "⚠️⚠️ <b>讲稿里三句只有老师会说的话</b>：① <em>Complete and hand in Q1–Q3 in this tutorial. <b>There is no separate continuation or Q4.</b></em> ② <em>Q1 supplies two activation rows; calculate only the missing row.</em> ③ <em>The extension is <b>optional and unmarked</b>.</em>",
   "⭐ <b>「Use the original network supplied within Q3」这句很关键</b>：Q3 自带网络设定，<b>不要去用别处（比如 Q1）的参数</b>。而且「original」还有第二层意思——<b>所有梯度都对应同一次前向、同一组原始参数</b>。",
   "<b>Q1 已经给了两行激活值</b>，只要算缺的那一行。讲稿说这是 <em>to reduce repeated calculator work</em>——<b>减少重复按计算器</b>，说明这一题的重点不在算，在<b>比较和解释</b>。",
   "<b>Q2 的后半段（多分类）也给了后续结果</b>，让你<b>focus on its meaning</b>——同样是重解释轻计算。⚠️ 这个倾向和考纲那句 <b>「只给出正确的最终数字，可能不足以体现所需的理解」</b> 完全一致。",
   "⚠️ <b>Tutorial 是堂内纸质 worksheet，当堂交</b>（M3-00 记号表里写了：tutor 当场发、课上做完、离开前交给 tutor，<b>不要线上提交</b>）。",
 ],
 "tbl": [{"cap": "三道题 ↔ 考纲条目 ↔ 本精读对应页",
   "head": ["题", "问什么", "考纲条目", "看哪几页"],
   "rows": [
     ["Q1", "算缺的激活值、比较行为、选输出与损失", "sigmoid/tanh/ReLU 及导数；饱和；四种任务的输出与损失", "p4、p6、p7、p14、p15"],
     ["Q2", "MSE/MAE、三个 BCE 值、logit 梯度、多分类", "MSE 与交叉熵", "p7、p16、p17"],
     ["Q3", "一个隐藏权重的梯度、两处零梯度、自动微分、batch/epoch 计数", "部分隐藏层权重的梯度；batch、epoch、自动微分", "p8、p9、p10、p18"],
   ]}],
 "exam": "⭐ <b>Tutorial 的三题几乎就是扩展题的原型</b>。考纲页自己写明「去哪儿找类似练习」时点名的就是 <b>M3 T2 Tutorial Q1–3</b>。把这三题做熟，T2 的 10 分题就有底了。",
},

{"r": [14, 14], "t": "Q1 前半：算激活值与局部导数，再解释行为", "star": 2,
 "one": "四步 —— 求值 → 求导 → 比较值域 → 解释梯度；重点在第 4 步的两个区分。",
 "quote": "1 Evaluate: complete only the missing row → 2 Differentiate: use each supplied derivative rule → 3 Compare ranges: connect output range to task meaning → 4 Interpret gradients: <b>distinguish saturation from inactive ReLU</b>.",
 "pts": [
   "⭐ <b>第 4 步是这一题的得分点</b>：<em>distinguish saturation from inactive ReLU</em>——<b>把「饱和」和「ReLU 不激活」区分开</b>。两者都让梯度变小，但机制完全不同：",
   "<b>饱和</b>：sigmoid/tanh 在 |z| 大时导数<b>趋近</b>于 0（但不等于 0），是<b>连续地变小</b>；而且<b>两端都会</b>。<b>ReLU 不激活</b>：z &lt; 0 时导数<b>恰好等于 0</b>，是<b>硬截断</b>；而且<b>只有负半轴</b>。",
   "⚠️ <b>讲稿要求的两句解释</b>：<em>Explain how small slopes affect a hidden learning signal</em>（小斜率怎样影响隐藏层的学习信号——乘上去之后传下去的梯度变小，层数多了会连乘衰减）和 <em>why inactivity on one observation does not establish a permanently dead unit</em>（<b>单个观测上不激活，不足以认定这个单元永久死亡</b>）。",
   "<b>计算要求</b>：讲稿说 <em>Calculate the six missing entries only, showing one output and its derivative calculation.</em> —— <b>只算六个缺的格子，而且要展示其中一个输出和它的导数的计算过程</b>。⚠️ 「展示过程」是明确要求，光填表不够。",
   "<b>Q1 还有后半段</b>（输出与损失选择），在下一页——讲稿特意说 <em>Q1 also asks for output/loss choices, on the following supporting slide</em>，<b>那不是另一道题</b>。",
 ],
 "exam": "⭐ 这一题对应的选择题形态：给 z 问输出或导数（照 p4 那张表）；或者给「某隐藏 ReLU 这次输出 0」问能否断定它死了（答<b>不能</b>）。扩展题则要你<b>写出一个完整的求值 + 求导过程</b>，别省步骤。",
},

{"r": [15, 15], "t": "Q1 后半：四种任务的输出与损失（考纲逐条点名）", "star": 3,
 "one": "回归 / 二分类 / 多分类 / 多标签，每一种都要给出输出激活 + 损失 + 一句理由。",
 "quote": "<b>The output range must agree with what the target represents.</b> 1 Regression: identify the required output range → 2 Binary class: decide whether the output must be a probability → 3 Multiclass: consider how mutually exclusive scores are normalised → 4 Multi-label: <b>several labels may be true at once</b>.",
 "eq": "回归      → 线性输出            + MSE 或 MAE\n二分类    → 一个 sigmoid        + 二元交叉熵 BCE\n互斥多类  → softmax            + 多类交叉熵（整数标签用 sparse 版）\n多标签    → 每标签一个 sigmoid  + 每标签各做一次 BCE\n\n⚠ 软件里数值稳定的损失常直接吃原始 logits，内部自己做激活 —— 别再套第二遍",
 "pts": [
   "⭐ <b>第一句就是判据</b>：<em>The output range must agree with what the target represents.</em> —— <b>输出的值域必须和目标代表的东西对得上</b>。回归目标是无约束实数 ⇒ 线性；二分类目标是概率 ⇒ sigmoid；互斥多类要一组和为 1 的概率 ⇒ softmax。",
   "⚠️⚠️ <b>讲稿点名要你解释的两件事</b>：① <em>why ReLU cannot guarantee a binary probability</em>——<b>ReLU 保证不了二分类概率</b>（输出无上界，可以是 3.7，既不是概率也不是类别）；② <em>why softmax forces competition between co-occurring labels</em>——<b>softmax 会在可共现的标签之间强行制造竞争</b>（概率和必须为 1，一个涨另一个就得跌，而「猫」和「户外」本可以同时为真）。",
   "<b>多标签的关键区分</b>：<em>several labels may be true at once</em>。所以用<b>各自独立的 sigmoid</b>，和<b>不必</b>等于 1。⚠️ 讲义还补了一句：<b>标签之间不必统计独立</b>——共享的隐藏特征仍然可能捕捉到标签间的关系。",
   "<b>标签编码要和损失接口匹配</b>：<em>Match integer versus one-hot multiclass labels to the corresponding loss interface.</em> —— <b>整数 ⇒ sparse categorical CE；one-hot ⇒ categorical CE</b>。两者表示同一个计算。",
   "⚠️ <b>考纲页给的官方示例选择题就是这个</b>：「每张照片恰好属于六个类别中的一个，标签存成整数 0–5」⇒ 答案是 <b>六个 softmax 输出 + sparse categorical cross-entropy</b>。",
 ],
 "tbl": [{"cap": "四选一时问自己的三句话",
   "head": ["问", "若是", "则"],
   "rows": [
     ["目标是连续的吗？", "是", "线性输出 + MSE/MAE，到此为止"],
     ["类别互斥吗？", "互斥", "softmax + 交叉熵"],
     ["", "可共现", "每标签一个 sigmoid + 各做一次 BCE"],
     ["标签怎么存的？", "整数", "sparse categorical CE"],
     ["", "one-hot", "categorical CE"],
   ]}],
 "exam": "⭐⭐⭐ <b>考纲逐条点名、官方示例题直接覆盖的一页</b>。扩展题会给一个场景（比如「一篇新闻可以同时属于体育和国际」），要你<b>写出输出层 + 损失 + 为什么另一个选项不行</b>。⚠️ 最后那句「为什么不行」是分，别省。",
},

{"r": [16, 16], "t": "Q2 前半：回归损失、三个 BCE 值与两种 logit 梯度", "star": 3,
 "one": "先算 MSE 与 MAE 并比较对大残差的敏感度，再算三个 BCE、报总和与均值，最后比较两种搭配的 logit 梯度。",
 "quote": "For y=1, only −log p remains; for y=0, only −log(1−p) remains. <b>BCE logit gradient: dL/dz = p − y</b>. Compare BCE with half-squared error. <b>The latter has an extra sigmoid slope p(1−p)</b>. Four checks: losses · summaries (<b>report total and mean</b>) · interpretation (explain the largest loss) · gradient comparison.",
 "eq": "回归（讲义算例）： 目标 [3, −1]，预测 [2, 1]  ⇒  残差 [−1, 2]\n    MSE = (1 + 4)/2 = 2.5          MAE = (1 + 2)/2 = 1.5\n    ⚠ 残差从 2 变 4：平方贡献 ×4（4→16），绝对值贡献 ×2（2→4）\n\n分类： y=1 ⇒ L = −log p        y=0 ⇒ L = −log(1−p)\n    −ln(0.8) ≈ 0.2231      −ln(0.7) ≈ 0.3567      −ln(0.2) ≈ 1.6094",
 "pts": [
   "⭐ <b>讲稿把做题顺序写死了</b>：<em>Start with the regression part</em>——<b>先做回归那一半</b>（算 MSE 和 MAE，解释哪个对更大的残差更敏感），<b>再</b>算三个 BCE 值和它们的<b>总和与均值</b>，<b>最后</b>比较两种 logit 梯度。",
   "⚠️ <b>「report total and mean」是明确要求</b>：<b>总和与均值都要报</b>。这正好呼应 p12 那条「Distinguish total loss from mean loss」。",
   "<b>「explain the largest loss」</b>：三个 BCE 里最大的那个，一定是<b>给观测到的那一类分配了最低概率</b>的那个样本。解释时要点出 <b>−log 在概率趋近 0 时急剧上升</b>。",
   "⭐⭐ <b>梯度比较是这一题的核心</b>：<b>BCE 给 p − y，半平方给 (p−y)·p(1−p)</b>。讲稿要求 <em>Explain the role of p(1−p) near saturation</em>——<b>解释 p(1−p) 在饱和附近起什么作用</b>（p 接近 0 或 1 时它极小，把梯度压没了）。",
   "⚠️ <b>讲稿划了两条范围</b>：① <em>No separate probability derivative is required.</em>——<b>不要求单独求对概率的导数</b>（只要对 logit 的）；② <em>The confidently wrong comparison is in the optional extension.</em>——<b>「自信地判错」那个对比属于选做的 extension</b>，不计分。",
 ],
 "tbl": [{"cap": "两个最容易混的导数",
   "head": ["对什么求导", "式子", "说明"],
   "rows": [
     ["对概率 p", "∂ℓ/∂p = −y/p + (1−y)/(1−p)", "本题不要求"],
     ["对 logit z（BCE）", "∂ℓ/∂z = p − y", "已含 sigmoid 的链式因子，就是 T1 的 δ"],
     ["对 logit z（半平方）", "∂ℓ/∂z = (p − y)·p(1−p)", "多出来的那个因子是祸根"],
   ]}],
 "exam": "⭐⭐ 扩展题常见形态：给两个残差算 MSE/MAE 并解释敏感度差异；给三个 (y, p) 算 BCE 并报总和与均值；给一个 p 比较两种 logit 梯度。⚠️ <b>每一问都要带一句解释</b>，只给数字拿不满。",
},

{"r": [17, 17], "t": "Q2 后半：多分类损失与学习信号", "star": 2,
 "one": "写 one-hot 目标 → 用 −Σ yₖ log pₖ 算损失 → 算 logit 梯度 p − y → 解释给出的后续结果。",
 "quote": "<b>The one-hot label identifies which class probability enters the loss.</b> 1 Target: write the one-hot vector for the true class → 2 Loss: use −Σₖ yₖ log pₖ <b>with natural logarithms</b> → 3 Gradient: calculate the logit gradient p − y → 4 Comparison: <b>interpret the supplied later result</b>.",
 "eq": "讲义算例： 概率 p = (0.1, 0.7, 0.2)，真实类别是第 2 类\n    one-hot 目标   y = (0, 1, 0)\n    损失           ℓ = −ln(0.7) ≈ 0.3567     ← 只有正确类那一项留下来\n    logit 梯度     p − y = (0.1, −0.3, 0.2)  ← 三项之和恰好为 0（自查）",
 "pts": [
   "⭐ <b>第一句就是整题的钥匙</b>：one-hot 目标<b>指出哪一个类别概率进入损失</b>。因为只有一个分量是 1，所以<b>单样本损失 = 给正确类别那个概率的负对数</b>。",
   "⚠️ <b>with natural logarithms</b> —— <b>全部用自然对数</b>。课件把这句单独标出来，说明有人用过 log₁₀。",
   "⭐ <b>梯度的符号要会读</b>：<b>正确类别那一项是负的</b>（梯度下降会<b>抬高</b>那个 logit），<b>其余项是正的</b>（它们的 logit 被<b>压低</b>）。⭐ <b>三项之和为 0</b> 是很好的自查。",
   "<b>第 4 步是解释题</b>：<em>interpret the supplied later result</em>——后续的损失和梯度<b>题目直接给你</b>，要解释的是<b>正确类的概率提高了、类别判定怎么变</b>，而不是重复一遍算术。",
   "⚠️ <b>讲稿要求的最后一句</b>：<em>Explain why a parameter gradient needs additional chain-rule factors.</em> —— <b>为什么参数的梯度还需要额外的链式因子</b>。因为 p − y 是<b>对 logit 的</b>导数，要得到对权重的导数还得再乘 ∂z/∂w；而且<b>一个权重可能影响好几个 logit 和好几个观测</b>。",
 ],
 "exam": "⭐ 选择题高发点：「p − y 是对什么求导」（答<b>对 logit</b>，不是对概率、不是对权重）；「三项之和等于多少」（答 <b>0</b>）。扩展题要你完整走四步，⚠️ 第 4 步的解释别省。",
},

{"r": [18, 18], "t": "Q3：隐藏梯度、两处零梯度、自动微分与计数", "star": 3,
 "one": "一条标量链式梯度 + 一次更新，两个不同的零梯度解释，自动微分与优化器的分工，最后一个 batch/epoch 计数。",
 "quote": "<b>Use the compact network setup printed directly above Question 3.</b> 1 Original state: use the supplied original network → 2 Hidden gradient: multiply local derivatives along the selected path → 3 Zero gradient: explain the effect of an inactive ReLU on this case → 4 Implementation: explain autodiff, updates and epochs.",
 "pts": [
   "⚠️⚠️ <b>讲稿把 Q3 的四个得分块说得非常清楚</b>：<em>Q3 asks for <b>one scalar chain-rule gradient and update</b>, <b>two distinct zero-gradient explanations</b>, and <b>the roles of autodiff and the optimiser</b>. Finish with the short batch/epoch count.</em>",
   "⭐⭐ <b>「two distinct zero-gradient explanations」是最容易漏的</b>——要写<b>两个不同的</b>零梯度，不是同一个说两遍：<br>① <b>隐藏单元的输入权重梯度为 0</b>：因为 z &lt; 0 ⇒ ReLU 局部导数 g′ = 0，整条路径被截断；<br>② <b>该单元的输出权重梯度也为 0</b>：因为它的梯度 = (p − y)·h，而 <b>h = 0</b>。<br>⚠️ 这两个零的<b>成因不同</b>：一个来自导数为零，一个来自激活值为零。",
   "<b>第 1 步「Original state」强调两次</b>：用<b>给定的原始网络</b>，而且讲稿说 <em>All gradients refer to the same original forward pass.</em> —— <b>所有梯度都对应同一次原始前向</b>。",
   "<b>第 4 步要讲清分工</b>：<b>自动微分记录前向运算并按链式法则算出梯度；优化器才执行参数更新</b>。⚠️ 加一句范围：<b>它不替你选目标、不修数据泄漏、不保证学习率合适</b>。",
   "⚠️ <b>最后那个计数是送分的</b>，别忘了做：样本数 ÷ 批大小 = 每个 epoch 的更新次数，再乘 epoch 数。",
   "<b>完整的矩阵版隐藏梯度属于 extension</b>：<em>The full hidden matrix calculation is extension work only.</em> —— <b>不计分</b>，时间不够可以跳过。",
 ],
 "tbl": [{"cap": "Q3 的四块 ↔ 该写什么 ↔ 对应本精读哪一页",
   "head": ["块", "该写什么", "看哪页"],
   "rows": [
     ["① 原始状态", "明说所有梯度都用这一次前向、这一组原参数", "p8"],
     ["② 隐藏梯度", "(p−y) → ×vⱼ → ×g′(zⱼ) → ×xᵢ，逐因子说明；再做一次更新", "p8"],
     ["③ 两处零梯度", "输入权重梯度 = 0（g′ = 0）；输出权重梯度 = 0（h = 0）——成因不同", "p8"],
     ["④ 实现", "autodiff 算梯度 / 优化器改参数；加一句它不做什么；再算 batch·epoch", "p9、p10"],
   ]}],
 "exam": "⭐⭐⭐ <b>这一题和 M3 考纲页给的官方示例扩展题结构几乎一样</b>（前向 → 梯度 → 更新 → 解释自动微分）。官方示例的答案校验是：z = 2、a = 2、L = 2，∂L/∂w = −6、∂L/∂b = −2，η = 0.05 更新后 w = 0.8、b = 0.6。⚠️ <b>两个梯度都用更新前的原参数算</b>。",
},

{"r": [19, 19], "t": "第 3 节：Practical 的五道题", "star": 1,
 "one": "Q1 激活值与局部梯度、Q2 比较损失、Q3 前向与改隐藏偏置、Q4 用验证 log loss 选激活、Q5 修输出/损失不匹配。",
 "quote": "Q1: calculate activation values and local gradients · Q2: compare losses and the penalties they encode · Q3: trace a forward pass and test a hidden-bias change · <b>Q4: select by validation log loss; refit and test once</b> · Q5: diagnose and repair output/loss mismatches.",
 "pts": [
   "⭐ <b>Q4 是 T3 的预告，而且是考点</b>：<em>select an activation using validation log loss, refits and evaluates the test data <b>once</b></em>——<b>用验证集的 log loss 选激活函数，重新拟合，然后在测试集上评估一次</b>。⚠️ 这正是 T3「用验证做选择、测试只评一次」那条纪律的具体落地。",
   "<b>Q5 也值得记</b>：<em>repairs output and loss combinations according to target semantics, including integer versus one-hot class labels</em>——<b>按目标的语义修复输出与损失的搭配，包括整数标签与 one-hot 的区别</b>。这就是 p15 那张配对表的反向用法：给一个错配，让你指出错在哪。",
   "<b>Q3 的做法很值得学</b>：<em>traces a forward pass, <b>predicts</b> the effect of changing a hidden bias, <b>then checks it</b></em>——<b>先预测改一个隐藏偏置会怎样，再实际算一遍验证</b>。⭐ 「先预测再验证」是本课反复用的方法（T1 的计算图活动也是这个套路）。",
   "⚠️ <b>Practical 不计分但很值得做</b>：它把 T2 的每个概念都落到一个可运行的例子上，而且 Q4/Q5 的思路直接能搬进扩展题。",
 ],
 "exam": "Practical 本身不考，但 <b>Q4 的流程（验证选择 → 重拟合 → 测试评一次）和 Q5 的错配诊断是扩展题的现成素材</b>。",
},

{"r": [20, 20], "t": "怎么走这个 notebook：按顺序跑、看中间值、用证据下结论", "star": 1,
 "one": "四步：按顺序算激活与导数 → 比较三种损失的惩罚 → 搭前向 → 验证选择、重拟合、测一次。",
 "quote": "1 Run in order: calculate activations and local derivatives → 2 Compare penalties: connect MSE, MAE and BCE to errors → 3 Build forward pass: implement <b>affine → activation → output</b> → 4 <b>Validate, refit, test</b>: select activation on validation; test once.",
 "pts": [
   "⭐ <b>讲稿点出了 practical 的真正重点</b>：<em>The practical emphasises <b>correct experimental reasoning</b> as well as code.</em> —— <b>正确的实验推理和代码同样重要</b>。接着那句更直接：<em>justify conclusions from evidence rather than from a single score</em>——<b>结论要有证据支撑，不能只看一个分数</b>。",
   "<b>第 3 步的三段式要记</b>：<b>affine → activation → output</b>。每一层都是「先仿射，再激活」，输出层的激活由任务决定。",
   "⚠️ <b>Study check 里那句话是 T3 的核心</b>：<em>Which output, plot, or comparison will you use as evidence, and <b>how will you avoid using test data to make development decisions</b>?</em> —— <b>你打算用哪个输出/图/对比当证据，又怎样避免用测试数据做开发决策</b>。",
   "<b>「inspect intermediate outputs」</b>再次出现（p10 讲稿也说过）。⭐ <b>先查形状和一个中间值，再信结果</b>——这是本讲重复了两次的建议。",
 ],
 "exam": "⭐ 最后那句「怎样避免用测试数据做开发决策」<b>就是 T3 扩展题的标准问法</b>。答法：<b>所有选择（模型、超参数、阈值、停止点）都用验证证据做，选定后冻结，最后在没碰过的测试集上评估一次</b>。",
 "tip": {"t": "T2 收尾，T3 接上", "v": "T2 的最后两页（p19 Q4、p20 Study check）已经完全是 T3 的语言了：<b>验证选择、重拟合、测试只评一次</b>。读完这一讲直接接 <b>M3T3 逐页精读</b>，衔接是连着的。", "w": 0},
},

]
