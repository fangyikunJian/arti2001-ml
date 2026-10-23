# -*- coding: utf-8 -*-
"""把 M2T3（高斯混合与 EM）逐页精读加厚到 M1 那套自制笔记的密度。

三个算例全部用 numpy 独立复算过，与讲义逐位一致：
  算例1 π=(0.7,0.3) μ=(−1,2) σ²=1，x=0 → 密度 0.2420/0.0540 → 加权 0.1694/0.0162
        → p(0)=0.1856 → r=(0.913, 0.087)
  算例2 x=(−2,0,3)，r=(0.9/0.1, 0.6/0.4, 0.1/0.9) → N=(1.6,1.4) → π=(0.5333,0.4667)
        → μ=(−0.9375, 1.785714) → σ²=(1.933594, 2.882653) → σ=(1.391, 1.698)
        ⚠ 误用 N_k−1 会得到 5.16 / 10.09
  算例3 x=(−1,1) 初始对称 → r=0.880797/0.119203 → μ=∓0.761594、σ²=0.419974、π 不变
        → ℓ 从 −2.9703 升到 −2.4394；下一轮 r=0.974090/0.025910
  参数个数 p=3K−1；300 obs、K=2、p=5、logL=−516.30 → BIC 1061.12 / AIC 1042.60
"""

DATA = {

1: {
 "quote": "<b>Gaussian Mixture Models</b> — <em>Soft clustering with probability distributions</em>",
 "pts": [
   "<b>副标题三个词各有分量</b>：<em>Soft</em>（软——归属是概率不是标签）、<em>clustering</em>（仍然在做分组）、<em>with probability distributions</em>（用概率分布来做）。",
   "⚠️ 但<b>把 GMM 只当成「软版 K-means」会漏掉一半</b>。它首先是一个<b>密度模型</b>：拟合完你得到完整的 p(x)，能回答「这个观测有多罕见」。<b>分组只是副产品。</b>",
   "<b>和前两讲的关系</b>：T1 的 PCA 换<b>表示</b>，T2 的聚类给<b>分组</b>，T3 的 GMM 给<b>密度</b>。三种输出，三类问题。",
   "<b>这一讲最容易出的问题是「公式记住了但不知道为什么」</b>——E 步为什么长那样、M 步的分母为什么是 N_k、为什么不能直接求导。后面每一页都会回到这些「为什么」。",
 ],
 "say": "把三个 Topic 放在 CS229 那张 2×2 地图上看，T3 的位置一下就清楚了：横轴是<b>建不建模 P(x)</b>，纵轴是<b>数据住在低维子空间还是聚成团</b>。<b>GMM 占的是「团 × 概率」那一格</b>，正上方是 K-means（团 × 非概率），左边同一行是因子分析（子空间 × 概率），左上是 PCA（子空间 × 非概率）。⭐ Ng 还补了一句很关键的：<b>EM 管的是整个「概率」列</b>——只要模型里有隐变量 z、你想建模 P(x)，EM 就适用。<b>这顺带解释了 K-means 为什么没有 EM 步骤</b>：它在非概率那一列，压根没有 P(x)，也就没有「对隐变量求期望」这回事。所以 <b>K-means 与 GMM 是同一行的两格</b>，差别只在建不建模概率——这也是为什么 GMM 常被叫作「软版 K-means」，以及为什么那个叫法只说对了一半。",
 "exam": "开场定调：<b>「GMM 是生成式概率模型，给出的是每个成分的后验责任度与完整密度，而不是硬标签」</b>。",
},

2: {
 "quote": "<b>M2 T3 Roadmap</b>：1 Hard → Soft Clusters — <em>Membership can be uncertain</em> · 2 Mixture Density — <em>Weighted sum of Gaussian components</em> · 3 Responsibilities — <em>Posterior probability of each component</em> · 4 EM Algorithm · 5 Model Selection — <em>Covariance choices, AIC and BIC</em>",
 "pts": [
   "<b>第 1 段就是这一讲的出发点</b>：<em>Membership can be uncertain</em>——<b>归属可以是不确定的</b>。K-means 强行给每点一个标签，GMM 承认「这个点我不确定」。",
   "<b>第 3 段给了责任度的正式身份</b>：<em>Posterior probability</em>——<b>后验概率</b>。注意是「后验」：先有先验权重 π，观测到 x 之后才更新成 r。",
   "<b>第 5 段是 T3 独有的能力</b>：<b>AIC 和 BIC</b>。前两讲选 k 只能靠肘部和 silhouette，GMM <b>有似然，所以能用信息准则</b>。",
   "<b>路线图就是答题顺序</b>：硬→软 → 混合密度 → 责任度 → EM → 选 K。",
 ],
 "tbl": [{"cap":"五段 ↔ 各自回答什么",
   "head":["段","小标题","回答的问题"],
   "rows":[
     ["1","Hard → Soft","为什么需要「不确定的归属」"],
     ["2","Mixture Density","p(x) 怎么由成分加权而来"],
     ["3","<b>Responsibilities</b>","r 是什么、怎么算"],
     ["4","EM Algorithm","两步怎么交替、为什么有效"],
     ["5","Model Selection","协方差类型、<b>AIC / BIC</b>"],
   ]}],
 "say": "这条路线图和 T2 的一个关键差别值得先点出来：<b>T2 选 k 只能靠肘部和 silhouette 这类「内部指标」，而 T3 多了一整条路——AIC/BIC</b>。原因很直接：<b>GMM 是概率模型，能算出似然</b>，有了似然就能套信息准则；K-means 和 DBSCAN 没有似然，只能用几何意义上的指标。⚠️ 但别把这理解成「T3 选 K 更容易」——<b>似然本身不能用来选 K</b>（加成分不会降低最好的训练似然），必须加罚项；而且<b>不同 EM 运行会落进不同局部最优</b>，所以实际拟合出的似然<b>未必随 K 单调上升</b>。<b>多出来的是一条证据，不是一个免死金牌</b>——四类证据框架在这一讲同样适用。",
 "exam": "「解释每段如何引出下一段」的串法：<b>归属可能不确定 ⇒ 需要一个能表达不确定性的模型（混合密度）⇒ 不确定性量化成责任度 ⇒ 但参数未知，要用 EM 交替估计 ⇒ 成分数也未知，用 AIC/BIC 选</b>。",
},

3: {
 "quote": "<b>K-means and GMM Represent Membership Differently</b> — <em>Both can describe groups, but GMM also models <b>shape and uncertainty</b>.</em> · K-means: <em>Hard centroid assignment · One label per observation · Spherical distance-based groups</em> · GMM: <em>Hidden state and posterior responsibility · Latent zᵢ</em>",
 "pts": [
   "⭐ <b>这一页最重要的是把 z 和 r 分清</b>（官方 Study check 第一问就是这个）。<b>z 是生成模型里真实但未观测的归属</b>（one-hot，非 0 即 1）；<b>r 是观测到 x 之后算出的后验概率</b>（0~1 的小数，每个观测各成分之和为 1）。",
   "<b>讲义有一句话说得极准</b>：<em>观测到 x 之后，我们并不是把隐藏变量替换成一个已知的标签，而是算一个后验概率。</em> 换句话说——<b>EM 从来没有「猜出」z，它只是算出了 z 的分布。</b>",
   "<b>第二个差别是 shape</b>：K-means 隐含假设球形（各向同性的距离）；GMM 每个成分有自己的协方差，<b>可以又扁又斜</b>。",
   "⚠️ <b>Study check 第二问：为什么两次正确的 GMM 运行可以给成分编不同的号？</b> 答：<b>成分标签是任意的</b>——把两个成分的编号对调，<b>混合密度一点都不变</b>。所以要通过<b>估计出的参数和它描述的那些观测</b>来解释一个成分，<s>不能靠编号</s>。这和 T2 里「比成员不比标签号」是同一件事。",
 ],
 "tbl": [{"cap":"z 与 r：最容易混的一对",
   "head":["","z（潜变量）","r（责任度）"],
   "rows":[
     ["是什么","生成模型里的<b>真实</b>归属","观测 x 之后的<b>后验概率</b>"],
     ["取值","one-hot，非 0 即 1","0~1 的小数"],
     ["约束","恰好一个成分为 1","<b>Σₖ rᵢₖ = 1</b>"],
     ["看得到吗","<b>看不到</b>","算得出来"],
   ]},
  {"cap":"K-means vs GMM",
   "head":["","K-means","GMM"],
   "rows":[
     ["归属","<b>硬</b>：一个标签","<b>软</b>：一个责任度向量"],
     ["形状","球形、基于距离","各成分自己的协方差，<b>可扁可斜</b>"],
     ["目标","最小化簇内平方和","<b>最大化似然</b>"],
     ["额外产出","无","<b>完整密度 p(x)</b>"],
   ]}],
 "exam": "「z 与 r 各代表什么」「为什么成分编号可以不同」都是官方 Study check 原题，极可能原样出现。",
 "tip": {"t":"高频失分点","v":"<b>把责任度当成临时硬标签。</b> 责任度 [0.55, 0.45] 的真实含义是<b>「这个点其实很难分」</b>；压成硬标签就把这个信息丢了。sklearn 里 <code>predict</code> 丢掉不确定性，<code>predict_proba</code> 保留。","w":1},
},

4: {
 "quote": "<b>A Mixture Density Is a Weighted Sum</b> — <em>Weights describe how often components occur; densities describe where they occur.</em> · <b>p(x) = Σₖ πₖ N(x|μₖ,Σₖ)</b> · <em>Each πₖ ≥ 0 and the weights sum to one.</em> · <em><b>For continuous data, p(x) is a density—not P(X=x).</b></em>",
 "eq": "p(x) = Σₖ πₖ · N(x | μₖ, Σₖ)\nπₖ ≥ 0，  Σₖ πₖ = 1   ⇒ 只有 K−1 个自由权重",
 "pts": [
   "⭐ <b>那句对照极其精炼</b>：<b>权重说「这个成分多常出现」，密度说「它出现在哪里」。</b> 两件事相乘再相加，就是混合密度。",
   "⚠️ <b>官方特意写了一句 not P(X=x)</b>：对连续数据，<b>p(x) 是密度不是概率</b>。「恰好取到某个值」的概率<b>严格等于 0</b>；概率要对<b>区间</b>积分。<b>推论：密度值可以大于 1</b>——看到 p(x)=1.8 别以为算错。",
   "<b>权重的两个约束</b>：非负、和为 1。⭐ <b>「和为 1」意味着 K 个权重只有 K−1 个是自由的</b>——最后一个由前面决定。这直接决定了后面数参数个数时的 (K−1) 那一项。",
   "⚠️ <b>成分数不等于峰数</b>：两个成分靠得近、方差又大时，叠出来<b>只有一个峰</b>。所以<b>看到单峰不能断定只有一个成分</b>，反过来 K 选大了也未必能从图上看出来。",
 ],
 "tbl": [{"cap":"式子里每个符号读作什么",
   "head":["符号","读作","约束"],
   "rows":[
     ["πₖ","混合权重（这个成分<b>多常</b>出现）","≥0，<b>Σ=1</b>"],
     ["μₖ","成分中心（出现在<b>哪里</b>）","—"],
     ["Σₖ","成分的离散与朝向","正定"],
     ["p(x)","混合<b>密度</b>","<b>可以 &gt;1</b>；对区间积分才是概率"],
   ]}],
 "say": "⚠️ 讲义在收尾的「四条警告」里还点了一条容易忽略的：<b>混合的方差有两个来源</b>——每个成分<b>内部</b>的离散，加上<b>成分均值之间</b>的差异。所以<b>混合方差不等于各成分方差的加权平均</b>。举个极端例子：两个成分各自方差都很小，但中心离得很远，<b>混合的整体方差会很大</b>。这是选择题爱设的陷阱，p9 的 Checkpoint 也专门列了它。",
 "exam": "「p(x) 是不是概率」「成分数是否等于峰数」「混合方差怎么算」都是现成的选择题。",
},

5: {
 "quote": "<b>Expectation–Maximisation Alternates Soft Assignment and Update</b> — <em><b>Each iteration improves or preserves the fitted log-likelihood.</b></em> · 1 Initialise → 2 E-step — <em>compute posterior responsibilities rᵢₖ</em> → 3 M-step — <em>update parameters using responsibility weights</em> → 4 repeat",
 "pts": [
   "⭐ <b>那句保证要读准</b>：<em>improves <b>or preserves</b></em>——<b>不会变差</b>，但可能原地不动。它<s>没有</s>说「一定找到最好的」。",
   "<b>官方 Study check 三问，逐个答</b>：<b>E 步固定什么？</b> 固定<b>参数</b>（π、μ、Σ），算责任度。<b>M 步更新什么？</b> 更新<b>参数</b>，而<b>责任度在整个 M 步里保持不动</b>。<b>为什么责任度叫「分数计数」？</b> 见下一条。",
   "⭐ <b>fractional counts（分数计数）的含义</b>：如果归属已知，每个观测对某成分的贡献要么 1 要么 0；<b>在 GMM 里归属不确定，责任度 0.9 就贡献 0.9 个计数</b>。加起来得到的 N_k 是<b>该成分预期生成了多少个观测</b>，通常<b>不是整数</b>，<b>绝不能凑整</b>。",
   "⚠️ <b>初始化不能省</b>：责任度是由参数算出来的，<b>参数不存在就算不了责任度</b>。所以必须先选 K 并给出合法的初始权重、均值、协方差（常用 K-means 的结果来初始化）。",
 ],
 "tbl": [{"cap":"两步各自固定什么、动什么（Study check 的答案）",
   "head":["步","固定","计算/更新","输出"],
   "rows":[
     ["E 步","<b>参数</b> π, μ, Σ","每个观测的后验","责任度 rᵢₖ"],
     ["M 步","<b>责任度</b> rᵢₖ","加权统计量","新的 π, μ, Σ"],
   ]},
  {"cap":"⚠ 三个关于 N_k 的错误理解（讲义都点名了）",
   "head":["说法","对不对"],
   "rows":[
     ["N_k 是责任度超过 0.5 的点的个数","<b>错</b>"],
     ["一个观测被物理地拆开了","<b>错</b>"],
     ["N_k 要四舍五入成整数","<b>错</b>"],
     ["N_k 是<b>期望计数</b>，且 <b>Σₖ N_k = N</b>","<b>对</b>（自检点）"],
   ]}],
 "exam": "「E 步固定什么、M 步更新什么、为什么叫分数计数」是官方 Study check 原题。",
},

6: {
 "quote": "<b>GMM Results Depend on Distributional Choices</b> — Components: <em>Too few underfit; too many can fragment structure</em> · Covariance type: <em>Controls permitted component shapes</em> · Initialisation: <em>Different starts can reach local optima</em> · Gaussian assumption: <em>Skewed or irregular groups may fit poorly</em> · Likelihood: <em>More components</em>…",
 "pts": [
   "<b>五条依赖就是评价 GMM 结果的清单</b>：成分数、协方差类型、初始化、高斯假设、似然随复杂度上升。",
   "<b>「Gaussian assumption」那条是 GMM 的根本边界</b>：<b>偏斜或形状不规则的组拟合不好</b>。GMM 比 K-means 灵活（成分可扁可斜），但<b>比 DBSCAN 死板</b>——它仍然假设每个成分是高斯，处理不了弯月形。",
   "<b>「Likelihood」那条要展开</b>：参数约束兼容时，<b>加成分不会降低最好的训练似然</b>，因为更大的模型能表示更小的模型。<b>所以「似然最大」永远指向「成分最多」，毫无信息</b>——这就是需要 AIC/BIC 的原因。",
   "⚠️ <b>还有一条课件没列的数值陷阱</b>：<b>成分坍缩</b>——一个成分收缩到单个点上，方差趋近 0，<b>似然可以趋向无穷大</b>。实现里靠<b>协方差正则化</b>（sklearn 的 <code>reg_covar</code>）和合理初始化来防。讲义原话：<b>高似然本身并不保证模型有用。</b>",
 ],
 "tbl": [{"cap":"covariance_type 的四个取值",
   "head":["取值","含义","参数最多/最少"],
   "rows":[
     ["<code>full</code>","每个成分<b>各自</b>完整的协方差（可扁可斜）","最多"],
     ["<code>tied</code>","所有成分<b>共用</b>一个协方差","中"],
     ["<code>diag</code>","各自对角：允许不同尺度但<b>轴对齐</b>","较少"],
     ["<code>spherical</code>","各自一个标量方差：<b>球形</b>","最少"],
   ]}],
 "say": "⚠️ <b>一维数据上，full 就是「每个成分一个方差」</b>——四个取值的差别在一维下会塌缩，别被名字绕进去。<br>另外这组选项和 CS229 是对得上的：Ng 说<b>按约定每个高斯有自己的 Σ，但你想强制它们相同也可以</b>——那就是 <code>tied</code>。<b>限制越强，参数越少，AIC/BIC 的罚项也越小</b>，所以协方差类型的选择会直接影响模型选择的结果。",
 "exam": "「为什么训练似然最高的模型不一定最好」是 p7 的 Study check，答案的第一半就在这一页：<b>加成分不会降低最好的训练似然</b>。",
},

7: {
 "quote": "<b>Choose a GMM with Fit, Parsimony and Stability</b> — Fit: <em>Log-likelihood describes fit but usually rises with complexity</em> · Parsimony: <em>Prefer lower AIC or BIC among fitted candidates</em> · Stability: <em>Compare seeds because EM can reach different local solutions</em> · Assumptions",
 "eq": "AIC = −2 log L + 2p\nBIC = −2 log L + p · log N\n一维、每成分一个方差：p = (K−1) + K + K = 3K − 1",
 "pts": [
   "⭐ <b>页标题给了三个判据</b>：<b>拟合（Fit）、简约（Parsimony）、稳定（Stability）</b>。官方 Study check 问「哪两个额外检查能加强你的选择」——答案就是<b>后两个</b>。",
   "<b>为什么训练似然最高的不一定最好</b>：<em>usually rises with complexity</em>——<b>似然通常随复杂度上升</b>。所以要用加了罚项的 AIC/BIC。",
   "<b>AIC 与 BIC 的差别只在罚项</b>：<b>AIC 是 2p，与样本量无关</b>；<b>BIC 是 p·log N，样本越多罚得越狠</b>。N 超过约 7 时 log N 就大于 2，所以 <b>BIC 通常更保守、选出的成分数更少</b>。两者不一致时用其它证据判。",
   "⚠️ <b>两者都是越小越好</b>，而且<b>只能在同一份数据、同样的候选之间比</b>。另外这里的 <b>p 是「参数个数」不是密度 p(x)</b>——同一个字母两个意思。",
 ],
 "tbl": [{"cap":"参数个数 p = 3K − 1（一维，每成分一个方差）",
   "head":["K","权重 K−1","均值 K","方差 K","p"],
   "rows":[
     ["2","1","2","2","<b>5</b>"],
     ["3","2","3","3","<b>8</b>"],
     ["4","3","4","4","<b>11</b>"],
   ]},
  {"cap":"讲义给的实际数字（300 个观测，已复算）",
   "head":["K","p","log L","BIC","AIC"],
   "rows":[
     ["2","5","−516.30","<b>1061.12</b>","<b>1042.60</b>"],
     ["3","8","略有改善","改善<b>不足以抵消</b>多出的参数","—"],
   ]}],
 "say": "⭐ <b>「权重只有 K−1 个自由」这一点最容易数错</b>，原因就在 p4：权重<b>必须加起来等于 1</b>，所以最后一个由前面决定，不是自由参数。<br>还有一条边界和 T2 的 inertia 完全平行：<b>不同的 EM 运行可能落进不同的局部最优</b>，所以<b>你实际拟合出的似然未必随 K 单调上升</b>——看到这种情况<s>不是 bug</s>，应提高 <code>n_init</code> 后再比较。",
 "exam": "选 K 的大题必考。<b>算 p 用 3K−1</b>；结论后面必须补那句：<b>「最小值是模型选择的证据，不是『确实存在这么多自然分组』的证明」</b>。",
 "tip": {"t":"高频失分点","v":"<b>把权重数成 K 个。</b> 一维 K 成分（每成分一个方差）的参数个数是 <b>3K−1</b> 不是 3K——因为权重之和为 1，只有 K−1 个自由。","w":1},
},

8: {
 "quote": "<b>EM Alternates Soft Assignment and Parameter Updates</b> — <em>E-step estimates responsibilities; M-step uses them as fractional counts.</em> · <b>rᵢₖ = πₖN(xᵢ|μₖ,Σₖ) / ΣⱼπⱼN(xᵢ|μⱼ,Σⱼ)</b> · <em>For every observation i, responsibilities across components sum to one.</em>",
 "eq": "E 步：rᵢₖ = πₖ N(xᵢ|μₖ,Σₖ) ÷ Σⱼ πⱼ N(xᵢ|μⱼ,Σⱼ)\nM 步：Nₖ = Σᵢ rᵢₖ  →  πₖ = Nₖ/N，μₖ = (1/Nₖ)Σᵢ rᵢₖ xᵢ  →  Σₖ = (1/Nₖ)Σᵢ rᵢₖ (xᵢ − μₖ^new)²",
 "pts": [
   "<b>E 步就是一次贝叶斯计算</b>：<b>后验 = 先验权重 × 成分密度 ÷ 混合密度</b>。⚠️ <b>分母正是 p(xᵢ) 本身</b>，所以每个观测的各成分责任度<b>自动加起来等于 1</b>——这是个免费的自检，手算完一定要核。",
   "<b>M 步三步，顺序不能错</b>：① 有效计数 → ② 权重与均值 → ③ 协方差，<b>而且协方差要用刚算出的新均值</b>。",
   "⚠️ <b>三个分母都是 N_k</b>——<s>不是 N</s>（那就变成普通平均了），<s>也不是 N_k−1</s>（那是<b>无偏样本方差</b>的公式，而 EM 做的是<b>极大似然</b>）。",
   "⭐ <b>责任度谁大，看的是「权重 × 密度」的乘积</b>，不是单看权重、也不是单看离哪个均值近。<b>两个因素可以反向</b>：权重小的成分如果在该点密度高得多，照样会赢。",
 ],
 "tbl": [{"cap":"E 步四步（讲义给的顺序）· 算例 π=(0.7,0.3)、μ=(−1,2)、σ²=1、x=0",
   "head":["步","做什么","成分 1","成分 2"],
   "rows":[
     ["①","在<b>同一个 x</b> 上算每个成分的密度","0.2420","0.0540"],
     ["②","各自乘以当前权重 πₖ","0.7×0.2420 = <b>0.1694</b>","0.3×0.0540 = <b>0.0162</b>"],
     ["③","相加得分母 p(x)","0.1694 + 0.0162 = <b>0.1856</b>",""],
     ["④","各自除以这个共同分母","<b>0.913</b>","<b>0.087</b>"],
   ]},
  {"cap":"⚠ 分母用错的后果（算例 2 的方差，已复算）",
   "head":["分母","σ₁²","σ₂²"],
   "rows":[
     ["<b>N_k（正确）</b>","<b>1.933594</b>","<b>2.882653</b>"],
     ["N_k − 1（错）","5.16","10.09"],
   ]}],
 "say": "⭐ CS229 里 Ng 点破了一件事，能让 M 步的公式一下子讲通：<b>责任度 wᵢⱼ 恰好就是指示函数 1{zᵢ=j} 的期望</b>（因为一个指示函数的期望就等于它为真的概率）。所以 <b>M 步的公式和「如果 z 可见」那版长得几乎一样，只是把 1{zᵢ=j} 整个换成了 rᵢₖ</b>。<b>这就是「E 步」里 E（Expectation，期望）这个名字的由来</b>——E 步做的正是把那个看不见的指示函数替换成它的期望。<br>顺带说：如果 z 可见，公式就<b>退化成你 M1 学过的 GDA</b>。GMM 说白了就是<b>把 GDA 的标签藏起来</b>。",
 "exam": "手算大题的主体。<b>E 步列成上面那张四行表，M 步按三步写</b>，每步都核一次自检（行和为 1、ΣN_k = N）。",
 "tip": {"t":"高频失分点","v":"<b>方差分母用 N_k−1。</b> 差距不是一点点——本页算例里 1.93/2.88 会变成 <b>5.16/10.09</b>，整题全毁。记住：<b>EM 是极大似然，分母就是 N_k</b>。","w":1},
},

9: {
 "quote": "<b>M2 T3 Checkpoint</b>：Density — <em>weight each Gaussian before summing</em> · Mean — <b>E[X] = Σπₖμₖ</b> · Variance — <em><b>include within- and between-component variation</b></em> · Sampling — <em>choose component, then draw from it</em> · BIC — <em>lower is preferred among fitted candidates</em>",
 "pts": [
   "<b>五个必须能默写的量</b>，Study check 要求 <em>without looking</em>。",
   "<b>Mean 那条很好记</b>：<b>混合的期望 = 各成分均值按权重加权平均</b>，E[X] = Σπₖμₖ。这个是「加权平均」，符合直觉。",
   "⚠️ <b>但 Variance 那条正好相反</b>：<b>混合方差要包含成分<u>内</u>与成分<u>间</u>两部分</b>，<s>不是</s>各成分方差的加权平均。这是本页最容易错的一条，也是课件特意大写标出的。",
   "<b>Sampling 那条就是生成故事</b>：<b>先选成分，再从它里面抽</b>——两步。这正好解释了 z 是什么（第一步的结果）。",
 ],
 "tbl": [{"cap":"五个量默写自检（盖住右列）",
   "head":["量","定义"],
   "rows":[
     ["Density","<b>先按权重加权</b>再相加"],
     ["Mean","E[X] = Σπₖμₖ（<b>加权平均</b>）"],
     ["Variance","<b>成分内 + 成分间</b>两部分"],
     ["Sampling","<b>先选成分，再从它抽</b>"],
     ["BIC","<b>越小越好</b>（在已拟合的候选之间比）"],
   ]}],
 "say": "要说出一条<b>连接</b>（Study check 的要求），最漂亮的一条是：<b>Sampling 那两步正好解释了前三条</b>——「先选成分」对应权重 πₖ（Density 里的加权、Mean 里的加权平均都来自它），「再从它抽」对应成分密度；而<b>正因为「先选哪个成分」本身是随机的，混合的方差才会多出「成分间」那一项</b>。<b>一个生成故事同时解释了密度、均值和方差三个量。</b>",
 "exam": "Checkpoint 五点就是手算与概念题的全部基础。<b>「混合方差有两个来源」</b>几乎必考。",
},

10: {
 "quote": "<b>Section 1 Complete: Gaussian Mixture Models</b> — Key Takeaways：<em>GMM is a generative probability model</em> · <em>Membership is soft where components overlap</em> · <em>EM alternates responsibility and parameter updates</em> · <em>Mixture variance includes more than component variances</em> · <em>BIC helps compare component counts but <b>does not replace judgement</b></em>",
 "pts": [
   "<b>第一条定性</b>：<em>generative probability model</em>——<b>生成式概率模型</b>。「生成式」的意思就是它描述了「数据是怎么被produce出来的」（先选成分、再抽点）。",
   "<b>第二条点出软归属真正起作用的地方</b>：<em>where components overlap</em>——<b>在成分重叠的地方</b>。远离重叠区的点责任度接近 0/1，和硬分配没区别；<b>软分配的价值全在交界处</b>。",
   "<b>第四条又强调了一次混合方差</b>（p4 和 p9 都提过）——课件在三个地方反复讲同一件事，说明它是考点。",
   "⭐ <b>第五条是收尾必写句</b>：<em>BIC helps compare component counts but does not replace judgement</em>——<b>BIC 帮你比较成分数，但不能代替判断。</b>",
 ],
 "tbl": [{"cap":"五条小结 · 在大题里怎么用",
   "head":["小结","用途"],
   "rows":[
     ["生成式概率模型","开头定性；解释为什么能算 p(x)"],
     ["<b>重叠处才软</b>","解读责任度 [0.55,0.45] 时用"],
     ["EM 交替两步","手算题流程"],
     ["<b>混合方差 ≠ 成分方差加权平均</b>","选择题陷阱"],
     ["<b>BIC 不能代替判断</b>","<b>结论后的局限句</b>"],
   ]}],
 "exam": "小结五句每句都能当采分句。最后一句是<b>答题第四步「说出局限」的标准落点</b>。",
},

11: {
 "quote": "<b>Section 2: M2 T3 Tutorial Activity</b> — <em>Three core questions connect density, responsibility and EM</em> · Q1 <em>use supplied densities for two observations; compare overall density with membership ambiguity</em> · Q2 <em>change the priors and recalculate responsibilities</em> · Q3 <em>diagnose a denominator</em>",
 "pts": [
   "<b>三问是递进的</b>：Q1 用给定密度算责任度；Q2 <b>只改先验权重</b>再算一次，看责任度怎么变；Q3 <b>先诊断分母</b>再做参数更新。",
   "⭐ <b>Q1 的关键词是 compare overall density with membership ambiguity</b>——<b>把「整体密度」和「归属的模糊程度」分开看</b>。这两件事无关：一个点可以<b>密度很高但归属很模糊</b>（落在两个成分中间的高密度区），也可以<b>密度很低但归属很确定</b>（远离所有成分，但明显更靠近其中一个）。",
   "<b>Q2 测的是「权重与密度的乘积」这个理解</b>：密度不变、只改权重，责任度就会变——<b>说明责任度不是只由「离哪个近」决定的</b>。",
   "<b>Q3 的 diagnose a denominator 是个很实际的技能</b>：分母是所有加权密度之和，<b>如果它接近 0，责任度就不可靠</b>（数值不稳定）。",
 ],
 "tbl": [{"cap":"三问 ↔ 对应的知识点页",
   "head":["问","测什么","回看哪一页"],
   "rows":[
     ["Q1","混合密度与责任度的区别","p4、p8"],
     ["Q2","<b>权重×密度</b>的乘积关系","p8"],
     ["Q3","分母诊断 + M 步更新","p5、p8"],
   ]}],
 "say": "Q1 那个「密度高 ≠ 归属确定」的区分值得多想一层：<b>混合密度 p(x) 大，说明「这个位置常出现观测」；责任度接近 0.5，说明「说不清它来自哪个成分」。</b> 两个成分重叠的区域<b>恰好同时满足这两点</b>——那里密度往往最高（两个成分都在贡献），而归属最模糊。<b>所以「这个点很典型」和「这个点好归类」是两回事。</b>",
 "exam": "Q1/Q2 是纯计算送分题，<b>但必须写出四步中间量</b>。Q3 要先说「分母是否正常」再往下算。",
},

12: {
 "quote": "<b>Question 1: Density and Membership</b> — <em>Use the supplied component densities for each of the two observations.</em> · 1 Read densities → 2 Weight them — <em>multiply each density by its mixing weight</em> → 3 Sum and divide — <em>find total density, then normalise contributions</em>",
 "pts": [
   "<b>三步就是 E 步的压缩版</b>：读密度 → 乘权重 → 求和再归一化。⚠️ <b>密度是题目给的，不用自己算高斯</b>（<em>supplied</em>）——别浪费时间去套指数公式。",
   "<b>第 3 步的两个动作要分开写</b>：<b>先求和得到 p(x)</b>（这本身就是一个有意义的量——混合密度），<b>再各自除</b>（得到责任度）。很多人直接跳到责任度，把 p(x) 漏了。",
   "<b>自检</b>：两个责任度<b>加起来必须等于 1</b>。算完立刻核。",
   "<b>要能解释结果</b>：责任度大的那个成分为什么赢——是<b>权重大</b>、还是<b>该处密度高</b>、还是<b>两者都占</b>？这三种情形的答法不同。",
 ],
 "tbl": [{"cap":"标准算例走一遍（π=(0.7,0.3)、μ=(−1,2)、σ²=1、x=0，已复算）",
   "head":["步","成分 1","成分 2","小计"],
   "rows":[
     ["密度 N(0|μ,1)","0.2420","0.0540","—"],
     ["× 权重","0.7×0.2420 = 0.1694","0.3×0.0540 = 0.0162","—"],
     ["求和 = <b>p(0)</b>","—","—","<b>0.1856</b>"],
     ["÷ p(0) = 责任度","<b>0.913</b>","<b>0.087</b>","和 = 1 ✓"],
   ]}],
 "say": "这个算例里<b>成分 1 赢得很彻底（0.913）</b>，讲义特意说明了原因：<b>它同时具备更大的先验权重（0.7 vs 0.3）和该处更高的密度（0.2420 vs 0.0540）——两个因素同向</b>。⚠️ <b>但它们完全可以反向</b>：比如 π=(0.2, 0.8) 而密度是 0.90 / 0.15 时，加权后是 0.18 vs 0.12，<b>权重小的成分反而赢</b>（r₁=0.6）。<b>所以判断责任度谁大，必须看乘积。</b>",
 "exam": "Q1 原型。必写：<b>两个密度 → 两个加权值 → p(x) → 两个责任度 → 核对和为 1</b>，最后解释谁赢、为什么。",
},

13: {
 "quote": "<b>Question 2: Changing Priors Changes Membership</b> — <em><b>Keep the supplied densities fixed; use the new mixing weights.</b></em> · <b>γₖ(x) = πₖN(x|μₖ,σₖ²) / ΣⱼπⱼN(x|μⱼ,σⱼ²)</b> · <em>The responsibilities for one observation must sum to one.</em> · 四个检查：numerator / denominator / ratio / sum",
 "pts": [
   "⭐ <b>第一句是这一问的全部要点</b>：<b>密度不变，只换权重。</b> 很多人会不自觉地把密度也重算一遍——题目明确说了保持不变。",
   "<b>这一问在演示什么</b>：<b>责任度不是只由「离哪个成分近」决定的</b>。同一个点、同样的密度，<b>先验权重一变，归属就可能翻过来</b>。",
   "<b>四个检查</b>（课件列的）：分子对不对 → 分母对不对 → 比值算对没 → <b>和是不是 1</b>。最后一条是最省事的自检。",
   "⚠️ <b>符号换了但东西没换</b>：这一页用 γₖ(x)，p8 用 rᵢₖ，<b>是同一个量</b>。看到不同记号别慌。",
 ],
 "tbl": [{"cap":"同一组密度、不同先验 → 责任度翻转（已复算）",
   "head":["先验 π","加权密度","分母","r₁"],
   "rows":[
     ["(0.7, 0.3)，密度 0.2420/0.0540","0.1694 / 0.0162","0.1856","<b>0.913</b>"],
     ["(0.2, 0.8)，密度 0.90/0.15","0.18 / 0.12","0.30","<b>0.6</b>（权重小的赢）"],
   ]}],
 "say": "下面那一行值得记住，它是选择题的经典设计：<b>π=(0.2, 0.8)</b> 看起来成分 2 占压倒优势，但该点处成分 1 的密度是成分 2 的<b>六倍</b>（0.90 vs 0.15），乘完之后 <b>0.18 &gt; 0.12</b>，<b>成分 1 反而赢</b>。⭐ <b>这就是「必须看乘积」最干净的例子</b>——只看权重会答错，只看距离也会答错。",
 "exam": "Q2 原型，也是选择题高发区。答题<b>必须把两个加权值和分母都写出来</b>，不能直接跳到比值。",
 "tip": {"t":"容易答错","v":"<b>以为权重大的成分一定赢。</b> 责任度比的是 <b>π × 密度</b> 的乘积；权重小但该处密度高得多时，<b>小权重的成分照样赢</b>。","w":1},
},

14: {
 "quote": "<b>Question 3: Check Responsibilities, Then Update</b> — <em>Diagnose the denominator before treating responsibilities as soft counts.</em> · 1 Check denominator — <em>sum all weighted component densities</em> → 2 Effective counts — <b>Nₖ = Σᵢrᵢₖ</b> → 3 Update parameters — <b>πₖ = Nₖ/n；μₖ = Σᵢrᵢₖxᵢ/Nₖ</b> → 4 Interpret EM",
 "pts": [
   "⭐ <b>第 1 步是个诊断步骤</b>，别跳过：<b>分母是所有加权成分密度之和</b>。如果它接近 0，说明<b>所有成分在这个点上的密度都极低</b>，责任度会变得数值不稳定——这时报出来的软归属不可信。",
   "<b>第 2 步和第 3 步就是 M 步</b>：先<b>按列求和</b>得有效计数，再算权重与均值。⚠️ <b>μₖ 的分母是 Nₖ 不是 n</b>——这是加权平均。",
   "<b>第 4 步 Interpret EM 是分值所在</b>：要说清 <b>E 步在做什么、M 步在做什么、为什么要交替</b>。",
   "⚠️ <b>整个 M 步里责任度保持不动</b>，重算是下一轮 E 步的事。官方 Study check 专门问过：<b>为什么 M 步更新完参数之后必须重算责任度？</b> 答：<b>责任度是由参数算出来的，参数变了它就过期了。</b>",
 ],
 "tbl": [{"cap":"完整 M 步算例：x=(−2,0,3)，r 如下（已复算）",
   "head":["步","成分 1","成分 2","自检"],
   "rows":[
     ["责任度","0.9, 0.6, 0.1","0.1, 0.4, 0.9","<b>每行和 = 1</b> ✓"],
     ["Nₖ = 按<b>列</b>求和","<b>1.6</b>","<b>1.4</b>","<b>1.6+1.4 = 3 = N</b> ✓"],
     ["πₖ = Nₖ/3","0.5333","0.4667","和 = 1 ✓"],
     ["μₖ（加权平均）","−1.5/1.6 = <b>−0.9375</b>","2.5/1.4 = <b>1.785714</b>","分母是 Nₖ"],
     ["σₖ²（围绕<b>新</b>均值）","<b>1.933594</b>","<b>2.882653</b>","分母也是 Nₖ"],
   ]}],
 "say": "⚠️ 三个容易翻车的细节，讲义都特意强调了：<b>① x=0 这个观测对分子贡献 0，但它的责任度仍然算进分母</b>——所以它照样影响结果，「除以 3 是错的」。<b>② 算成分 2 的方差时要用未四舍五入的 μ₂ = 2.5/1.4</b>，全程保留完整精度，只在显示时才四舍五入。<b>③ 方差不是标准差</b>：σ₁² = 1.933594，开根号才是 σ₁ ≈ 1.391。本课一维高斯的第二个参数是<b>方差</b>，而 NumPy 的 <code>random.normal</code> 用的是<b>标准差</b>。",
 "exam": "Q3 原型，也是手算大题的主体。按上表五行写，<b>每行都带自检</b>。最后一问「Interpret EM」要写：<b>E 步算责任度、M 步用它们更新参数、交替直到似然改善可忽略</b>。",
},

15: {
 "quote": "<b>Section 3: GMM Practical</b> — <em>Generate a reproducible overlapping one-dimensional mixture</em> · Q1 <em>fit two Gaussian components and inspect parameters</em> · Q2 <em>interpret responsibilities near overlap</em> · Q3 <em>interpret mixture density and compare counts using BIC</em> · Q4 <em>implement one E-step</em>",
 "pts": [
   "<b>关键词 overlapping</b>：数据是<b>特意造成重叠</b>的——因为<b>软归属的价值全在重叠区</b>（见 p10）。",
   "<b>Q2 是重点</b>：<em>interpret responsibilities <b>near overlap</b></em>——解读重叠附近的责任度。那里的责任度会接近 0.5，<b>正是「硬分配会掩盖什么」的最好例证</b>。",
   "<b>Q4 要你亲手实现一次 E 步</b>——这是把公式变成代码的检验。实现时最容易错的就是<b>忘了除以分母</b>（那样各成分的值加起来不等于 1）。",
   "<b>reproducible 的意思是固定随机种子</b>（<code>random_state</code>），否则每次跑出来的数不一样，没法讨论。",
 ],
 "tbl": [{"cap":"四问 · 用什么证据",
   "head":["问","做什么","看什么"],
   "rows":[
     ["Q1","拟合两成分","<code>weights_</code> / <code>means_</code> / 标准差"],
     ["Q2","<b>解读重叠处的责任度</b>","<code>predict_proba</code>"],
     ["Q3","混合密度 + 比较成分数","<b>BIC</b>"],
     ["Q4","实现一次 E 步","各成分责任度<b>和为 1</b>"],
   ]}],
 "exam": "Practical 的结论常被搬进大题：<b>重叠处责任度接近 0.5，硬分配会掩盖这个不确定性</b>。",
},

16: {
 "quote": "<b>How to Work Through the GMM Notebook</b> — <em>Fitting and plotting scaffolds are supplied; complete the density, model-selection and EM challenges.</em> · 1 Fit two components — <em>inspect weights, means and standard deviations</em> → 2 Read responsibilities — <em>explain soft membership near overlap</em> → 3 Plot and select",
 "pts": [
   "⚠️ <b>第 1 步就有个陷阱</b>：<em>inspect weights, means and <b>standard deviations</b></em>——sklearn 给的 <code>covariances_</code> 在一维下是<b>方差</b>，要开根号才是标准差。<b>看到一个数先问：这是 σ 还是 σ²？</b>",
   "<b>第 2 步是这个 notebook 的核心</b>：解释重叠附近的软归属。用 <code>predict_proba</code>，<b>不是 <code>predict</code></b>——后者丢掉不确定性。",
   "<b>官方 Study check 又问了一次方法论问题</b>：<em>how will you avoid using test data to make development decisions?</em> 答：<b>选 K、调参只用训练/验证数据，测试数据留到最后一次性评估。</b>",
   "<b>sklearn 三个方法要分清</b>：<code>score_samples</code> 给<b>对数</b>混合密度；<code>predict</code> 给 argmax 成分（丢不确定性）；<code>predict_proba</code> 给<b>完整责任度向量</b>。",
 ],
 "tbl": [{"cap":"常考的 sklearn 属性与方法",
   "head":["写法","返回什么","注意"],
   "rows":[
     ["<code>weights_</code>","各成分权重 π","和为 1"],
     ["<code>means_</code> / <code>covariances_</code>","均值与协方差","<b>一维下是方差，不是标准差</b>"],
     ["<code>score_samples(X)</code>","<b>对数</b>混合密度","是对数，不是密度本身"],
     ["<code>predict(X)</code>","责任度最大的成分","<b>丢掉不确定性</b>"],
     ["<code>predict_proba(X)</code>","<b>完整责任度向量</b>","每行和为 1"],
     ["<code>n_init=10</code>","<b>十次初始化</b>","<s>不是十轮迭代</s>"],
   ]}],
 "exam": "「读输出」型选择题。记牢：<b>predict vs predict_proba 的差别</b>、<b>score_samples 是对数密度</b>、<b>n_init 是初始化次数</b>。",
},

}
