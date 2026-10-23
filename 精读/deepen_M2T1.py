# -*- coding: utf-8 -*-
"""把 M2T1 逐页精读加厚到「M1材料/笔记与阅读」那套自制笔记的密度。

用户 2026-09-29 指出：那批笔记（如 M1T3_分类_知识点全集_含推导，19 页 34461 字，
每页约 1814 字）质量更高，理想形态是「左边 ppt，右边是目前笔记的程度，加上题目」。
量下来我原来的 M2 精读平均每页只有 819 字，差 2.2 倍。

照搬那批笔记的做法：① 论点式页标题 ② 表格密集（对比表/情况表/数值表）
③ 引课件英文原话 ④ 讲「为什么」不只讲「是什么」 ⑤ 手算例带验证步 ⑥ 点名本课特有约定。

数据全部复算过：
  Tutorial（rank-one）(1,2)(2,4)(−1,−2)(−2,−4) → S=[[10,20],[20,40]]，λ=(50,0)，
      PC1=(1,2)/√5≈(0.4472,0.8944)，解释方差(1,0)，重构误差 0
  by-hand (−3,0)(3,0)(0,−1)(0,1) → S=[[18,0],[0,2]]，λ=(18,2)，Cov λ=(6,0.6667)，
      解释方差(0.9,0.1)，Z=(−3,3,0,0)，重构误差 2 = 被丢掉的特征值
"""

# page -> 要写入/覆盖的字段。pts 与 say 为整体覆盖，quote/tbl 为新增。
DATA = {

1: {
 "quote": "<b>Unsupervised Learning and PCA</b> — <em>Finding lower-dimensional structure without labels</em>",
 "pts": [
   "<b>标题里已经给了这一讲的全部承诺</b>：<em>lower-dimensional</em>（更少的维度）、<em>structure</em>（结构）、<em>without labels</em>（没有标签）。三个词对应三件事——做什么、找什么、在什么条件下找。",
   "<b>「没有标签」不是省事，是换了一类问题。</b> M1 里你总能拿预测和真值比对，算个准确率就知道好不好；这里<b>没有那个数字</b>。所以这门课把重心整个挪到了「你凭什么相信这个结果」。",
   "<b>PCA 在这一讲里的定位</b>：它是「降维」这一族里最经典的一个，做法是找<b>正交的高方差方向</b>。注意<em>正交</em>和<em>高方差</em>这两个限定词——后面所有性质都从它们推出来。",
   "⚠️ <b>第 2 页 Acknowledgement of Country 不考</b>，裁页时已经去掉了，所以这份精读的页码比原课件少 1（原第 2 页起整体前移）。",
 ],
 "say": "把这一讲放进整幅地图：CS229 用一张 2×2 给无监督分类——横轴「建不建模 P(x)」、纵轴「数据住在低维子空间还是聚成团」。<b>PCA = 子空间 × 非概率</b>；同一行的概率版是因子分析，下一行是 K-means（非概率）与 GMM（概率）。<b>M2 的三个 Topic 正好占这张表的三格。</b>",
 "exam": "选择题会考「PCA 属于哪一类任务」「无监督与监督的根本差别」。大题开头那一句定调的话就从这里来：<b>「因为无监督学习没有供给的目标标签，不存在唯一裁判，所以需要综合多类证据来判断」</b>。",
},

2: {
 "quote": "<b>M2 T1 Roadmap</b>：1 Unsupervised Landscape · 2 Why Reduce Dimensions · 3 Centre and Scale — <em>Preprocessing changes PCA directions</em> · 4 Principal Directions — <em>Eigenvectors of covariance</em> · 5 Project, Reconstruct &amp; Implement",
 "pts": [
   "<b>路线图本身就是答题顺序。</b> 大题要你「完整做一遍 PCA」时，按这五段写下来就不会漏步骤。",
   "<b>第 3 段的小标题是这一讲最该记的一句</b>：<em>Preprocessing changes PCA directions</em>——<b>预处理会改变主方向</b>。不是「影响一点点」，是<b>换一组方向</b>。所以中心化与缩放不是格式化步骤，是建模决定。",
   "<b>第 4 段点明了主方向的身份</b>：<em>Eigenvectors of covariance</em>——协方差矩阵的特征向量。⚠️ 这不是定义，是<b>推出来的结论</b>（在约束 ‖v‖=1 下最大化 vᵀΣv，用拉格朗日乘子解出 Σv=λv）。",
   "<b>第 5 段把三件容易混的事并列</b>：投影（得到得分）、重构（回到特征空间）、实现（sklearn）。这三者的区别是 p10 和 p12 的主题，也是最常考的概念题。",
 ],
 "tbl": [{"cap":"五段路线图 ↔ 它各自回答什么问题",
   "head":["段","小标题","回答的问题"],
   "rows":[
     ["1","Unsupervised Landscape","无监督都有哪些任务，本课考哪几个"],
     ["2","Why Reduce Dimensions","为什么要降维：压缩、可视化、去噪"],
     ["3","Centre and Scale","<b>为什么预处理会换掉主方向</b>"],
     ["4","Principal Directions","主方向是什么、怎么解出来"],
     ["5","Project / Reconstruct / Implement","得分与重构的区别；sklearn 怎么对应"],
   ]}],
 "exam": "官方 Study check 问的是：<b>「解释为什么特征准备会改变 PCA 的方向，并说出一个能帮你决定保留几个成分的实现输出」</b>。后半问的答案是 <code>explained_variance_ratio_</code>。",
},

3: {
 "quote": "<b>Unsupervised Learning Is a Landscape of Tasks</b> — <em>Core methods are studied in depth; wider task families provide non-assessed context.</em>",
 "pts": [
   "<b>这一页明确划了考试范围</b>，值得先看清楚：<em>studied in depth</em> 的是<b>四个核心方法</b>，<em>awareness only · not assessed</em> 的是更广的任务族。别在不考的部分花时间。",
   "<b>三类核心任务对应三个 Topic</b>：降维（PCA）= T1，聚类（K-means、DBSCAN）= T2，密度估计（GMM）= T3。<b>整个 M2 就这三块。</b>",
   "⚠️ <b>「用无监督学习」还不是一个完整的建模决定</b>——这是官方 Study check 的原话。你还得说清楚：属于哪一类任务、用哪个方法、在什么特征与缩放下、用什么证据判断好坏。",
   "<b>任务类型怎么认</b>：要「更少的特征」→ 降维；要「有用的分组」→ 聚类；要「这个观测有多罕见」→ 密度估计。<b>第三个是 GMM 能做而 K-means 做不到的。</b>",
 ],
 "tbl": [{"cap":"考什么 / 不考什么",
   "head":["范围","内容","考不考"],
   "rows":[
     ["核心方法","降维 <b>PCA</b>","<b>深入考</b>"],
     ["","聚类 <b>K-means、DBSCAN</b>","<b>深入考</b>"],
     ["","密度估计 <b>GMM</b>","<b>深入考</b>"],
     ["更广的任务族","关联规则、异常检测、表示学习等","<b>只需知道存在</b>，不考"],
   ]},
  {"cap":"给任务定类型（Study check 的三个例子）",
   "head":["场景","任务族","本课的方法"],
   "rows":[
     ["压缩互相关联的特征","降维","PCA"],
     ["把客户分组","聚类","K-means / DBSCAN"],
     ["标记异常交易","密度估计","GMM（算 p(x) 很小就报警）"],
   ]}],
 "exam": "这一页是概念选择题的直接来源。<b>「把任务归类」型的题按上表两问定位：要少的特征 / 要分组 / 要罕见度。</b>",
},

4: {
 "quote": "<b>A Reliable Unsupervised-Learning Workflow</b>：1 Define the Question · 2 Define Similarity — <em>Choose features, scales and distance</em> · 3 Prepare Features · 4 Match Assumptions · 5 Fit and Inspect · 6 Interpret and report limitations",
 "pts": [
   "<b>第 2 步「定义相似」是整条流程的枢纽</b>，也是最容易被跳过的一步。<em>Choose features, scales and distance</em>——特征、缩放、距离，<b>三者任何一个变了，「谁和谁相似」就变了</b>。",
   "⚠️ <b>官方 Study check 直接问：为什么对同一份数据做标准化会得到不同的簇？</b> 答案就在第 2 步：标准化改变了距离的含义，于是改变了「相似」的定义，于是改变了分组。<b>这不是算法不稳定，是你换了问题。</b>",
   "<b>第 4 步「匹配假设」问的是</b>：你要找的结构是什么形状（球形？弯曲？）、密度均不均匀、有没有噪声、维度多高。<b>选算法的理由就写在这一步。</b>",
   "<b>第 6 步「解释并报告局限」是评分点</b>，不是客套。大题最后一句必须写「这个结果不能证明什么」。",
 ],
 "tbl": [{"cap":"六步工作流 · 每步的产出与常见失分",
   "head":["步","做什么","这一步没做好会怎样"],
   "rows":[
     ["1 定义问题","什么样的结构能回答它","做出来的结构没人用得上"],
     ["2 <b>定义相似</b>","选特征、缩放、距离","大量纲特征独占距离，分组只由它决定"],
     ["3 准备特征","缺失值、单位、尺度","尺度不可比，后面全歪"],
     ["4 匹配假设","形状、密度、噪声、维度","用 K-means 去切弯曲结构"],
     ["5 拟合与检视","看投影、看簇、看成员","只报数字不看图，看不出失败模式"],
     ["6 <b>解释与局限</b>","连回原问题、说清边界","<b>最多拿一半分</b>"],
   ]}],
 "say": "第 2 步和第 3 步的顺序有实际后果：<b>DBSCAN 的 ε 必须在缩放之后选</b>，因为 ε 是一个带量纲的距离阈值，缩放一变它的含义就全变了。讲义原话是 <em>Select eps AFTER scaling, because its numerical meaning changes with the representation</em>。",
 "exam": "「为什么标准化会改变聚类结果」是高频问答。答：<b>标准化改变了距离的含义 ⇒ 改变了「相似」的定义 ⇒ 改变了分组</b>；并补一句这是建模决定不是格式化步骤。",
},

5: {
 "quote": "<b>Evaluate Unsupervised Results with Multiple Signals</b>：Internal evidence — <em>Use method-appropriate scores, but never one score alone</em> · Stability · Assumptions · Inspection · Usefulness",
 "pts": [
   "⭐ <b>这一页是整个 M2 的主线</b>，官方在 Canvas 的评估页把它标为 <b>Core and assessable</b>，而 PPT 只给了五个词。四道大题里至少两道要用到它。",
   "<b>五类证据各自问什么</b>：内部证据问「按这个方法自己的标准，结构好不好」；稳定性问「换个种子/样本/邻近参数还在不在」；假设检查问「表示与模型对这份数据合不合理」；检视问「画出来长什么样」；有用性问「连回原问题有没有用」。",
   "⚠️ <b>关键的限定词是 never one score alone</b>——<b>永远不要只用一个分数</b>。原话还有一句：<em>one attractive plot or one high score is not enough</em>。",
   "<b>什么时候算「站得住」</b>：官方的说法是 <em>A result is defensible when these signals broadly agree</em>——<b>几类信号大致一致</b>时才站得住。注意是「大致一致」，不是「全部最优」。",
 ],
 "tbl": [{"cap":"五类证据 · 在三个 Topic 里各自长什么样",
   "head":["证据","PCA","聚类","GMM"],
   "rows":[
     ["内部证据","解释方差比、重构误差","inertia、silhouette","对数似然、<b>AIC/BIC</b>"],
     ["稳定性","换样本看子空间稳不稳","换种子/重采样比<b>成员</b>","多次初始化比最终似然"],
     ["假设","线性、方差≈信息","形状是凸的吗、密度均匀吗","高斯假设成立吗"],
     ["检视","看散点、看重构","把标签画回散点图","看成分与数据的贴合"],
     ["有用性","降维后下游好用吗","这些组讲得通吗","责任度对业务有意义吗"],
   ]}],
 "say": "官方 Study check 给了一个很好的情形：<b>「一个 PCA 投影保留了很高的方差，但保留下来的方向被某个未缩放的特征主导。框架里哪几部分会警告你别马上接受？」</b> 答案至少有两条——<b>假设检查</b>（缩放不当，表示不合理）和<b>检视</b>（看载荷就能发现一个特征独大）；还可以补<b>有用性</b>（这个主成分连不回原问题）。",
 "exam": "「评价某个无监督结论」的大题按这五条逐条扫，每条都能得分。<b>只报一个 silhouette 或一个解释方差就下结论，最多拿一半分。</b>",
},

6: {
 "quote": "<b>Labels Change the Question We Ask</b> — <em>Supervised learning predicts a target; unsupervised learning describes structure.</em>",
 "pts": [
   "<b>监督</b>：用带标签的样本，<b>目标 y 指挥目标函数</b>，评估就是把预测和真值对比（回归、分类）。",
   "<b>无监督</b>：只用特征之间的模式，训练时<b>没有任何供给的目标</b>，<em>Structure needs interpretation</em>——<b>得到的结构需要人来解释</b>。",
   "<b>共同点别忽略</b>：两者都在优化某个准则、都依赖特征表示、都会被尺度影响。<b>所以「无监督没有目标函数」是错的</b>——没有的是<b>标签</b>，不是目标函数。",
   "<b>最重要的差别</b>：<b>无监督没有唯一裁判</b>。这一句直接决定了上一页那套多证据框架为什么必须存在，也决定了四道大题的写法。",
   "<b>什么时候这个差别会改变你的建模决定</b>（Study check 的第三问）：当你手上<b>有部分标签</b>时——那就该考虑半监督或直接做监督，而不是硬套无监督；反过来，当标签<b>昂贵或根本不存在</b>时，无监督是唯一选择，但你必须准备好用多类证据来论证。",
 ],
 "tbl": [{"cap":"两边对照（课件原表 + 补充）",
   "head":["","监督 Supervised","无监督 Unsupervised"],
   "rows":[
     ["用什么","带标签的样本","只用特征之间的模式"],
     ["谁指挥目标","<b>目标 y</b>","没有供给的目标"],
     ["怎么评估","预测 vs 真值","<b>多类证据，需要解释</b>"],
     ["例子","回归、分类","PCA、聚类、GMM"],
     ["有没有唯一裁判","<b>有</b>（准确率 / MSE）","<b>没有</b>"],
   ]}],
 "tip": {"t":"容易答错","v":"<b>「无监督就是没有目标函数」是错的。</b> 没有的是<b>标签</b>，不是目标函数——K-means 在最小化 J，PCA 在最大化投影方差，GMM 在最大化似然，每个都有明确的目标函数。"},
 "say": "「没有唯一裁判」带来的第二个后果常被忽略：<b>无监督结果的「对错」依赖于你选的表示</b>。同一批客户，用「年消费额 + 到访次数」和用「客单价 + 到访频率」聚出来的组可以完全不同，而<b>两者都没算错</b>。所以讲义反复强调聚类结果是<b>模型产出的摘要</b>，需要解释和验证，<s>不是自动发现的真实类别</s>。这也是为什么大题的最后一步必须写局限——你报的从来不是「真相」，而是「在这组选择下看到的结构」。",
 "ng": "<b>Ng 用一张 2×2 把无监督算法全放进去</b>——Lecture 15 的 <a href=\"https://www.youtube.com/watch?v=dyb_cFywuik&t=2947s\" target=\"_blank\">49:07</a> 起，他在课上让同学一起填这张表：横轴是<b>建不建模 P(x)</b>，纵轴是<b>你假设数据长什么样</b>。<b>数据住在低维子空间</b>那一行：非概率的是 <b>PCA</b>，概率的是<b>因子分析</b>；<b>数据聚成团</b>那一行：非概率的是 <b>K-means</b>，概率的是<b>混合高斯</b>。到 <a href=\"https://www.youtube.com/watch?v=dyb_cFywuik&t=3110s\" target=\"_blank\">51:50</a> 他补了一句关键的：<b>EM 管的是整个「概率」列</b>（任何含隐变量 z 的 P(x,z)），这也顺带解释了<b>K-means 为什么没有 EM 步骤</b>——它在非概率那一列，压根没有 P(x)。<span class=\"src\">CS229/transcripts/L15.txt · 本地已下载</span>",
 "exam": "概念选择题的常客。也很适合写进大题开头一句：<b>「因为无监督学习没有供给的目标标签，不存在唯一裁判，所以需要综合多类证据来判断……」</b>——这一句给后面所有论证定调。",
},

7: {
 "quote": "<b>PCA Finds Directions of Maximum Variance</b> — <em>Mean-centring makes covariance describe variation around the data centre.</em> · <b>S = XcᵀXc</b>；<em>Sample covariance is S/(n−1); the scale changes eigenvalues, not eigenvectors.</em> · <em>The eigenvector with the largest eigenvalue is the first principal direction.</em>",
 "eq": "S = Xcᵀ Xc\nCov = S / (n − 1)\nΣv = λ v，‖v‖ = 1  ⇒  vᵀΣv = λ",
 "pts": [
   "<b>为什么必须中心化</b>：协方差衡量的是「围绕数据中心的变化」。不减均值的话，「方差最大的方向」会被数据<b>离原点多远</b>牵着走——那是位置信息，不是形状信息。中心化之后，S 才真正描述形状。",
   "⭐ <b>这一页最常考的一句</b>：<em>the scale changes eigenvalues, not eigenvectors</em>。S 与 Cov=S/(n−1) 只差一个正常数倍，所以<b>特征向量完全相同，特征值差 (n−1) 倍</b>。推论：<b>主方向一样，解释方差比也一样</b>（分子分母同时除以 n−1，比值不变）。",
   "<b>实战结论</b>：手算时<b>直接用 S</b>，因为通常是整数、不用一路带分数。<b>只有一种情况必须除</b>——题目明确问「这个方向上的<b>方差</b>是多少」，或要你和 sklearn 的 <code>explained_variance_</code> 对数。",
   "<b>vᵀΣv = λ 的含义</b>：把 Σv=λv 左乘 vᵀ，配合 vᵀv=1 即得。<b>特征值就是该方向上的投影方差</b>——所以「取最大特征值」和「取方差最大的方向」是同一件事。",
 ],
 "tbl": [{"cap":"by-hand 数据 (−3,0)(3,0)(0,−1)(0,1)：S 与 Cov 的对照（已复算）",
   "head":["量","用 S","用 Cov = S/3"],
   "rows":[
     ["矩阵","[[18, 0], [0, 2]]","[[6, 0], [0, 0.667]]"],
     ["特征值","18 与 2","<b>6 与 0.667</b>（差 3 倍）"],
     ["特征向量","(1,0) 与 (0,1)","<b>完全相同</b>"],
     ["解释方差比","18/20 = <b>0.9</b>","6/6.667 = <b>0.9</b>（一样）"],
     ["对应 sklearn","—","<code>explained_variance_</code> ≈ [6, 0.667]"],
   ]}],
 "say": "记号对照：<b>CS229 把投影长度写作 uᵀx</b>（单个点与单位向量做内积），<b>你们课件写作 Z = Xc W</b>（整个矩阵一次投影）——<em>同一件事的两种写法</em>，看到别慌。另外 CS229 里 Ng 是用<b>拉格朗日乘子</b>把 Σu=λu 解出来的：在 ‖u‖=1 约束下最大化 uᵀΣu，对 u 求导令零，<b>「主方向必须是特征向量」是解出来的结论，不是定义</b>。",
 "exam": "「S 与 Σ 的特征向量/特征值关系」几乎必考。答题写：<b>特征向量相同、特征值差 (n−1) 倍、解释方差比不变</b>；问方差数值或对 sklearn 才除。",
 "tip": {"t":"高频失分点","v":"<b>忘记中心化就直接算 XᵀX。</b> 那样得到的第一「主方向」往往指向数据中心的方位，而不是数据的伸展方向。手算题里中心化后<b>每一列的和应当为 0</b>——这是官方给的自检步骤，算完务必核一下。","w":1},
},

8: {
 "quote": "<b>PCA Is a Sequence of Linear-Algebra Decisions</b> — <em>Each step has a diagnostic students can check.</em> · 1 Prepare — <em>centre features; standardise if units differ</em> → 2 Covariance → 3 Decompose — <em>sort eigenvectors by decreasing eigenvalue</em> → 4 Project",
 "pts": [
   "⭐ <b>这一页的关键词是 diagnostic——每一步都有一个可以当场检查的量。</b> 手算大题写出这些检查，就是在给自己送分。",
   "<b>第 1 步 Prepare</b>：中心化是<b>必须</b>的；标准化是<em>if units differ</em>——<b>有条件的</b>。这两者的地位不同，别混为一谈。",
   "<b>第 3 步 Decompose 的动词是 sort</b>：解出特征对之后<b>必须按特征值从大到小排序</b>。不排序的话「第一主成分」就没有意义。",
   "<b>第 4 步 Project 之后还有一个动作</b>：<em>inspect retained variance</em>——算完得分要<b>检视保留了多少方差</b>，这是决定保留几个成分的依据。",
 ],
 "tbl": [{"cap":"四步 · 每步的自检量（考试写出来就是采分点）",
   "head":["步","做什么","<b>当场能检查的量</b>"],
   "rows":[
     ["1 Prepare","减均值；必要时标准化","<b>每一列的和 = 0</b>"],
     ["2 Covariance","S = XcᵀXc 或 S/(n−1)","<b>S 对称</b>；对角线非负"],
     ["3 Decompose","解特征对，<b>按 λ 降序排</b>","<b>Σλ = trace(S)</b>；‖v‖ = 1；两向量点积 = 0"],
     ["4 Project","Z = Xc W，看保留方差","解释方差比<b>加起来为 1</b>（全保留时）"],
   ]}],
 "say": "第 3 步那两个自检值得多说一句。<b>Σλ = trace(S)</b>（特征值之和等于对角线之和）是线性代数的恒等式，手算时<b>一秒钟就能验出特征值解错没有</b>——by-hand 例子里 18+2 = 18+2 ✓。而<b>特征向量两两正交</b>不是 PCA 额外要求的，是因为 <b>S 是对称矩阵，而对称矩阵的特征向量必然正交</b>。",
 "exam": "大题要求「展示矩阵计算与中心化步骤」。<b>把上表第三列的自检写进答卷</b>——「中心化后列和为 0」「Σλ=trace(S)」「‖v‖=1」，既防止自己算错，也是明确的采分点。",
},

9: {
 "quote": "<b>PCA Preserves Variance, Not Necessarily Meaning</b> — Scaling: <em>Large-unit features can dominate directions</em> · Outliers: <em>Extreme points can rotate components</em> · Linearity: <em>Curved manifolds may not be represented well</em> · Variance: <em>High variance may be unrelated to a target</em> · Interpretation: <em>Component signs are arbitrary and loadings need context</em>",
 "pts": [
   "⭐ <b>页标题就是结论</b>：<b>PCA 保的是方差，不一定保意义。</b> 这句话是大题「说出局限」那一步最常用的一句。",
   "<b>五条局限各自的机制</b>——<b>缩放</b>：大量纲特征在协方差里贡献大，方向就被它拽过去；<b>离群点</b>：平方距离对极端值极其敏感，几个点就能把成分转过去；<b>线性</b>：PCA 只会找<b>线性</b>子空间，弯曲的流形它表示不了；<b>方差</b>：高方差和「对任务有用」<b>没有必然联系</b>；<b>解释</b>：成分的<b>符号是任意的</b>。",
   "⚠️ <b>成分符号任意这一条经常被忽略</b>：v 和 −v 是同一个特征向量（都满足 Σv=λv、‖v‖=1），所以 sklearn 给你 (0.6, 0.8) 还是 (−0.6, −0.8) <b>纯看求解器</b>。<b>得分会整体变号，但解释方差、重构结果完全不变。</b>",
   "<b>为什么低方差方向仍可能要紧</b>（Study check 第一问）：方差大小衡量的是<b>输入自己的变化</b>，和<b>类别可不可分</b>没有关系。一个方向上两类正好分得开、但整体幅度很小，PCA 会第一个把它丢掉。",
 ],
 "tbl": [{"cap":"五条局限 · 机制与应对",
   "head":["局限","机制","应对"],
   "rows":[
     ["缩放","大量纲特征在协方差里占比大","比较缩放前后的结果；必要时标准化"],
     ["离群点","平方距离对极端值敏感，成分会被转向","先查离群点；或用稳健方法"],
     ["线性","只能表示<b>线性</b>子空间","弯曲结构考虑非线性降维"],
     ["方差","<b>高方差 ≠ 与目标相关</b>","用<b>验证数据</b>比较有无 PCA"],
     ["解释","<b>符号任意</b>、载荷需要上下文","别解读单个成分的符号；看子空间"],
   ]},
  {"cap":"⚠ PCA 与线性回归最小化的误差不是同一个（Study check 第二问）",
   "head":["","PCA","线性回归"],
   "rows":[
     ["最小化什么","到子空间的<b>正交（垂直）距离</b>","y 方向的<b>竖直</b>残差"],
     ["用不用 y","<b>不用</b>","用"],
     ["对称性","x 与 y 地位对称","不对称（换轴结果就变）"],
   ]}],
 "say": "CS229 里 Ng 对这一页有更重的说法。他说自己跑 PCA 时<b>从不去看任何单个特征向量</b>，因为<b>单个特征向量的位置在数值上是不稳定的</b>——改一个训练样本、动一下小数点第五位，基就可能在子空间里大幅旋转。<b>稳定的是前 k 个特征向量张成的子空间，不是单根轴。</b> 他用这一点解释了为什么 K-means 的簇质心可以解释、而主成分不可以，也用它否掉了 eigenfaces 那套解读（「至少一半是研究者的想象」）。",
 "exam": "「PCA 降维后分类反而变差」是选择题原型。答：<b>PCA 只最大化输入方差、从不看 y</b>，被丢掉的低方差方向可能正是判别关键；要判断只能用<b>验证数据</b>比较有无 PCA。若目的是抗过拟合，<b>正则化是更直接的手段</b>。",
 "tip": {"t":"高频失分点","v":"<b>「解释方差 95% 所以信息几乎没丢」</b>——丢没丢<b>对任务有用的</b>信息，解释方差答不了。它只说明保住了多少<b>输入的</b>变化。","w":1},
},

10: {
 "quote": "<b>Projection Separates Coordinates from Reconstruction</b> — <em>Scores are new coordinates; reconstruction maps them back to feature space.</em> · <b>Z = XcWₖ，X̂ = ZWₖᵀ + μ</b> · <em>Use centred data for the projection; add the mean only during reconstruction.</em> · <em>Retained variance = selected eigenvalue sum ÷ total eigenvalue sum.</em>",
 "eq": "Z = Xc Wₖ        （得分：n × k）\nX̂ = Z Wₖᵀ + μ    （重构：n × d）\n保留方差 = (λ₁+…+λₖ) / (λ₁+…+λ_d)",
 "pts": [
   "⭐ <b>三个对象必须分清</b>，这是这一页的全部重点：<b>方向</b>（特征向量 v，d 维，单位长度）、<b>得分</b>（标量 z，新坐标）、<b>重构</b>（x̂，回到原特征空间，d 维）。",
   "⚠️ <b>投影用中心化数据，均值只在重构时加回去。</b> 这是官方明说的顺序（<em>add the mean only during reconstruction</em>）。顺序错了重构结果会整体平移。",
   "<b>为什么重构要加回均值</b>：投影是在<b>中心化后</b>的坐标系里做的，z·vᵀ 得到的是「相对于数据中心的偏移」；要回到原始特征空间，必须把当初减掉的 μ 加回来。",
   "<b>保留方差的比值</b>：选中的特征值之和 ÷ 全部特征值之和。<b>全部保留时比值加起来是 1</b>——这是一个自检。",
 ],
 "tbl": [{"cap":"三个对象 · 只保留 PC1 时的形状与含义",
   "head":["对象","形状（d 维、n 个样本）","是什么"],
   "rows":[
     ["方向 v₁","d × 1","<b>一个方向</b>，单位长度"],
     ["得分 zᵢ","每个样本一个<b>标量</b>","<b>新坐标</b>：该样本在 v₁ 上投影多远"],
     ["重构 x̂ᵢ","d × 1","<b>回到原特征空间</b>的近似点"],
     ["components_","k × d（<b>一行一个方向</b>）","sklearn 存主方向的地方"],
     ["transform(X)","n × k","得分矩阵"],
   ]},
  {"cap":"by-hand 例子只留 PC1（已复算）",
   "head":["原始点","得分 z","重构 x̂","误差²"],
   "rows":[
     ["(−3, 0)","−3","(−3, 0)","0"],
     ["(3, 0)","+3","(3, 0)","0"],
     ["(0, −1)","<b>0</b>","(0, 0)","1"],
     ["(0, 1)","<b>0</b>","(0, 0)","1"],
     ["合计","—","—","<b>2</b>"],
   ]}],
 "say": "⭐ 上表最后一行藏着一个漂亮的恒等式：<b>重构误差的平方和 = 被丢掉的特征值之和</b>。这个例子里被丢掉的是 λ₂ = 2，而误差合计正好也是 2（我用 numpy 复算过）。这解释了为什么<b>「最大化投影方差」和「最小化正交重构误差」是同一件事</b>——总方差固定，保住的多，丢掉的就少。CS229 用勾股定理给了这个等价性的完整证明。",
 "exam": "「哪个是方向、哪个是坐标、为什么逆变换要加回均值」是官方 Study check 原题。另一道常考：<b>给一组特征值，问保留 k 个的解释方差比</b>——直接用上面那个比值。",
 "tip": {"t":"容易混","v":"<b>得分 z 不是「距离」。</b> 它是<b>带符号的坐标</b>：z 可以是负数，表示在 v₁ 的反方向。上表里 (−3,0) 的得分是 <b>−3</b> 不是 3。","w":1},
},

11: {
 "quote": "<b>M2 T1 Checkpoint</b>：Centre — <em>subtract each feature mean</em> · Covariance — <em>compute from centred observations</em> · PC1 — <em>eigenvector of largest eigenvalue</em> · Score — <b>zᵢ = xᵢ,cᵀ v₁</b> · Reconstruct — <b>x̂ᵢ = zᵢ v₁ᵀ + μ</b>",
 "pts": [
   "<b>这一页是官方给的「必须能默写」清单</b>，五个量。Study check 的要求是 <em>without looking</em>——合上书能写出来才算过关。",
   "<b>五个量之间的连接</b>（Study check 要你说出一条）：最容易说的一条是——<b>PC1 是协方差矩阵最大特征值对应的特征向量，而那个特征值就等于得分的方差</b>。也就是说，<b>λ₁ = Var(z)</b>。",
   "<b>另一条连接</b>：得分用<b>中心化</b>的 xᵢ,c，重构时<b>加回</b> μ——两个式子里 μ 的出现位置正好互补。",
   "⚠️ <b>zᵢ = xᵢ,cᵀ v₁ 里的转置位置</b>：xᵢ,c 是列向量，转置后是行向量，和 v₁ 做内积得到<b>标量</b>。写成 v₁ᵀ xᵢ,c 是同一个数。",
 ],
 "tbl": [{"cap":"五个量 · 默写自检表（盖住右两列试试）",
   "head":["量","定义","by-hand 例子的值"],
   "rows":[
     ["Centre","减去每个特征的均值","μ = (0, 0)，本来就已中心化"],
     ["Covariance","<b>从中心化后的观测</b>算","S = [[18,0],[0,2]]"],
     ["PC1","<b>最大特征值</b>对应的特征向量","v₁ = (1, 0)，λ₁ = 18"],
     ["Score","zᵢ = xᵢ,cᵀ v₁","(−3, 3, 0, 0)"],
     ["Reconstruct","x̂ᵢ = zᵢ v₁ᵀ + μ","(−3,0) (3,0) (0,0) (0,0)"],
   ]}],
 "exam": "Checkpoint 页的内容<b>就是手算大题会用到的全部量</b>。考前把这张表默写一遍，能确认没有漏洞。",
},

12: {
 "quote": "<b>The scikit-learn API Mirrors the PCA Workflow</b> — <em>Use fitted attributes to connect code back to the mathematics.</em> · <code>PCA(n_components=k).fit(X)</code> <em>learns the mean and directions</em> · <code>components_</code> <em>stores the principal axes as rows</em> · <code>transform(X)</code> <em>gives scores</em>",
 "pts": [
   "<b>考的是「读输出」不是「写代码」。</b> 重点在于每个属性对应数学里的哪个量。",
   "⚠️ <b>components_ 是「一行一个方向」</b>（<em>as rows</em>）。所以保留 1 个成分、原始 2 个特征时，<code>components_</code> 的形状是 <b>(1, 2)</b>，而 <code>transform(X)</code> 的形状是 <b>(n, 1)</b>——这正是官方 Study check 的第二问。",
   "<b>fit 学到了两样东西</b>：<em>the mean and directions</em>——<b>均值和方向</b>。均值存在 <code>mean_</code> 里，这就是为什么 <code>inverse_transform</code> 能自动把均值加回去。",
   "<b>explained_variance_ 是协方差矩阵的特征值</b>（by-hand 例子里是 6 和 0.667），<b>explained_variance_ratio_ 是比例</b>（0.9 和 0.1）。⚠️ 前者是<b>除过 (n−1) 的</b>，别和 S 的特征值 18、2 搞混。",
 ],
 "tbl": [{"cap":"属性 ↔ 数学量（by-hand 例子的实际值）",
   "head":["sklearn","数学里是什么","例子里的值"],
   "rows":[
     ["<code>mean_</code>","拟合时学到的 μ","(0, 0)"],
     ["<code>components_</code>","主方向，<b>一行一个</b>","[[1, 0]]（k=1 时形状 1×2）"],
     ["<code>explained_variance_</code>","<b>协方差</b>的特征值","[6, 0.667]"],
     ["<code>explained_variance_ratio_</code>","该方向占总方差的比例","[0.9, 0.1]"],
     ["<code>transform(X)</code>","得分 Z","形状 n×k"],
     ["<code>inverse_transform(Z)</code>","重构 X̂（<b>自动加回 μ</b>）","形状 n×d"],
   ]}],
 "tip": {"t":"高频失分点","v":"<b>把 explained_variance_ 和 S 的特征值混为一谈。</b> 前者 = 后者 ÷ (n−1)。例子里是 <b>6 与 0.667</b>，不是 18 与 2。但<b>比例（0.9 / 0.1）两边一样</b>。","w":1},
 "exam": "「读输出」型选择题。记牢三件事：<b>components_ 一行一个方向</b>、<b>explained_variance_ 是协方差的特征值</b>、<b>k=1 时形状是 (1,d) 与 (n,1)</b>。",
},

13: {
 "quote": "<b>Scaling and Leakage Change the PCA Result</b> — Centre: <em>PCA centres features, but does not standardise their scales</em> · Split first: <em>Create train and test sets before learning preprocessing parameters</em> · Fit on train: <em>Fit StandardScaler and PCA using training data only</em>",
 "pts": [
   "⚠️ <b>第一句就纠正了一个常见误解</b>：<em>PCA centres features, but does not standardise their scales</em>——<b>PCA 自己会中心化，但不会标准化</b>。想要标准化必须你自己加 <code>StandardScaler</code>。",
   "<b>为什么大量纲特征会主导</b>：协方差里每个特征的贡献是它<b>自身方差</b>的量级。一个以元为单位、方差上万的特征，和一个 0~1 的特征放在一起，前者几乎独占第一主方向——<b>这时 PC1 基本就是那个特征本身</b>，没有信息量。",
   "⭐ <b>顺序是：先切分 → 只在训练集上 fit → 用同一变换 transform 两边。</b> 三步一步都不能换。",
   "<b>两种错法的毛病不同</b>：<b>全量 fit</b> ⇒ 测试集信息渗进了变换，是<b>数据泄漏</b>；<b>测试集上重新 fit</b> ⇒ 两边坐标系<b>不一致</b>，得分根本没法比。",
 ],
 "tbl": [{"cap":"哪些操作会「学参数」（学了就不能在测试集上重学）",
   "head":["操作","学到什么参数","测试集上"],
   "rows":[
     ["<code>StandardScaler</code>","每个特征的<b>均值与标准差</b>","<b>只 transform</b>"],
     ["<code>PCA</code>","<b>均值 μ 与主方向 W</b>","<b>只 transform</b>"],
     ["缺失值填补","填补用的统计量","<b>只 transform</b>"],
     ["取对数 / 平方等","<b>不学参数</b>","可各自做"],
   ]},
  {"cap":"三种做法对照",
   "head":["做法","问题"],
   "rows":[
     ["全量数据上 fit 后再切分","<b>数据泄漏</b>：测试集信息进了变换"],
     ["训练集与测试集各自 fit","<b>坐标系不一致</b>，得分不可比"],
     ["<b>切分 → train 上 fit → 两边 transform</b>","<b>✓ 正确</b>"],
   ]}],
 "say": "CS229 课上有学生问过一模一样的问题：<b>「用 PCA 的话，测试集上是不是也要求一遍特征向量？」</b> Ng 的回答是 <b>The answer is actually no</b>——在训练集上跑一次，<b>特征向量从此永久固定</b>，测试数据一律用同一组 uᵢ 映射过去。实务上把 <code>StandardScaler</code> 和 <code>PCA</code> 放进 <code>Pipeline</code> 最稳，交叉验证时每一折会自动只在训练折上 fit。",
 "exam": "泄漏题是 T1 选择题的固定考点。答题写全三步：<b>split → train 上 fit → 同一变换 transform 两边</b>，并点明<b>放进 Pipeline</b>。",
 "tip": {"t":"高频失分点","v":"<b>「PCA 不用标签，所以全量 fit 不算泄漏」</b>——错。<b>泄漏与用不用标签无关</b>，只要测试集的信息进了变换，评估就偏乐观了。","w":1},
},

14: {
 "quote": "<b>Section 1 Complete</b> — Key Takeaways：<em>PCA is unsupervised: no target guides the directions</em> · <em>Mean-centring is required for the standard derivation</em> · <em>Scaling is a modelling decision, not a cosmetic step</em> · <em>Eigenvalues rank directions by captured variance</em> · <em>Projection and reconstruction answer different questions</em>",
 "pts": [
   "<b>五条小结按重要性排</b>，第 3 条和第 5 条最常出题。",
   "<b>「Scaling is a modelling decision, not a cosmetic step」</b>——缩放是<b>建模决定</b>，不是化妆。这句话可以整句抄进大题。",
   "<b>「Projection and reconstruction answer different questions」</b>——投影回答「这个样本在新坐标系里的位置」，重构回答「只用这些方向能把原始观测还原到什么程度」。<b>前者给坐标，后者给误差。</b>",
   "<b>Study check 要求</b>：说清<b>主方向 / 得分 / 重构观测</b>三者的区别，并各自指出对应的 sklearn 方法或属性——答案见 p10 与 p12 的表。",
 ],
 "tbl": [{"cap":"三个对象 ↔ sklearn（Study check 的答案）",
   "head":["对象","是什么","sklearn"],
   "rows":[
     ["主方向 principal direction","一个单位向量","<code>components_</code>"],
     ["得分 score","新坐标（标量）","<code>transform(X)</code>"],
     ["重构观测 reconstructed observation","回到原特征空间的近似点","<code>inverse_transform(Z)</code>"],
   ]}],
 "exam": "小结页的五句话<b>每一句都可以直接当大题的采分句</b>。尤其「缩放是建模决定」和「投影与重构回答不同的问题」。",
},

15: {
 "quote": "<b>Section 2: M2 T1 Tutorial Activity</b> — <em>Three core questions reproduce PCA on a small rank-one dataset</em> · Q1 <em>centres data and forms scatter/covariance matrices</em> · Q2 <em>verifies eigenpairs and normalises the first component</em> · Q3 <em>projects, reconstructs and explains retained variance</em> · <em>Show matrix calculations and centring steps</em>",
 "pts": [
   "⚠️ <b>关键词是 rank-one（秩 1）</b>——Tutorial 用的数据<b>完全共线</b>。这不是巧合，是特意设计的：秩 1 意味着<b>第二个特征值恰好是 0</b>，于是解释方差是 100% / 0%，重构误差是 0。",
   "<b>三问各自测什么</b>：Q1 测<b>中心化与矩阵构造</b>；Q2 测<b>特征对求解与归一化</b>；Q3 测<b>投影、重构与解释方差</b>。三问正好覆盖 p7–p10 的全部内容。",
   "⭐ <b>「Show matrix calculations and centring steps」是评分要求</b>：<b>要展示中间步骤</b>，只写最后答案拿不到全部分数。",
   "<b>Study check 的第二问很值得想</b>：<em>为什么 PCA 可能保住了方差却丢掉了对目标要紧的信息？</em>——因为方差衡量的是<b>输入自身</b>的变化，与<b>类别可分性</b>无关（见 p9）。",
 ],
 "tbl": [{"cap":"Tutorial 数据 (1,2)(2,4)(−1,−2)(−2,−4)：秩 1 的后果（已复算）",
   "head":["量","值","为什么"],
   "rows":[
     ["均值","(0, 0)","数据本来就已中心化"],
     ["S = XcᵀXc","[[10, 20], [20, 40]]","两列严格成 1:2"],
     ["det(S)","<b>0</b>","两行成比例 ⇒ 秩 1"],
     ["特征值","<b>50 与 0</b>","Σλ = 50 = trace ✓"],
     ["PC1","(1,2)/√5 ≈ (0.4472, 0.8944)","归一化后 ‖v‖=1"],
     ["解释方差","<b>100% / 0%</b>","λ₂ = 0"],
     ["重构误差","<b>0</b>","= 被丢掉的特征值之和 = 0"],
   ]}],
 "say": "<b>秩 1 数据的特殊性要拿捏好</b>：它让每一步的数字都很干净，非常适合手算；但也意味着<b>「投影垂线长度 = 丢掉的信息」这个几何直觉在这组数据上看不出来</b>——所有点本来就在那条线上，垂线长度全是 0。想理解那个几何含义，要看<b>不共线</b>的例子（比如 by-hand 那组，垂线长度分别是 0、0、1、1）。",
 "exam": "Tutorial 三问就是大题的原型。答题结构：<b>列出中心化后的矩阵 → 写 S → 解特征对并排序 → 归一化 → 投影 → 算解释方差 → 解释含义</b>。",
},

16: {
 "quote": "<b>Question 1: Centre Before Covariance</b> — <em>A correct covariance calculation begins with the correct origin.</em> · 1 Find means → 2 Centre rows → 3 <b>Verify: each centred column should sum to zero</b> → 4 Form matrix — <b>S = XcᵀXc 和 Cov = S/(n−1)</b>",
 "pts": [
   "⭐ <b>第 3 步「Verify」是官方写进流程的自检</b>：<b>中心化后每一列的和应当为 0</b>。算完立刻核一下，能挡掉绝大多数低级错误。",
   "<b>页标题的说法很准</b>：<em>A correct covariance calculation begins with the correct origin</em>——<b>协方差算得对不对，取决于原点选得对不对</b>。不中心化，原点就还在 (0,0)，算出来的不是「围绕数据中心的变化」。",
   "<b>S 与 Cov 都要会写</b>：S = XcᵀXc 是<b>散布矩阵</b>（scatter matrix），Cov = S/(n−1) 是<b>样本协方差</b>。手算优先用 S（整数），除非题目问方差数值。",
   "⚠️ <b>Xcᵀ Xc 的顺序不能反</b>：Xc 是 n×d，所以 Xcᵀ Xc 是 <b>d×d</b>（特征之间的关系，正确）；Xc Xcᵀ 是 n×n（样本之间的关系，那是另一回事）。",
 ],
 "tbl": [{"cap":"Q1 四步 · Tutorial 数据实做",
   "head":["步","操作","结果"],
   "rows":[
     ["1 求均值","每个特征一个均值","μ = (0, 0)"],
     ["2 中心化","逐行减去均值向量","Xc = X（本来就中心化了）"],
     ["3 <b>验证</b>","<b>每列求和应为 0</b>","1+2−1−2 = 0 ✓；2+4−2−4 = 0 ✓"],
     ["4 构造矩阵","S = XcᵀXc；Cov = S/3","S = [[10,20],[20,40]]；Cov = [[3.33,6.67],[6.67,13.33]]"],
   ]}],
 "exam": "Q1 是送分题，但<b>必须把第 3 步的验证写出来</b>。评分要求明确说了 <em>Show matrix calculations and centring steps</em>。",
 "tip": {"t":"容易算错","v":"<b>S 的非对角元算错符号。</b> S₁₂ = Σ xᵢ₁·xᵢ₂ = 1·2 + 2·4 + (−1)(−2) + (−2)(−4) = 2+8+2+8 = <b>20</b>——<b>负负得正</b>，四项全是正的。","w":1},
},

17: {
 "quote": "<b>Question 2: Eigenvalues Rank the Directions</b> — <em>The characteristic equation supplies candidate directions.</em> · <b>Sv = λv</b>；<em>Solve det(S−λI)=0, then solve (S−λI)v=0.</em> · <em>Normalise the leading eigenvector before using it as an axis.</em> · 四步检查：determinant → null space → order → normalise",
 "eq": "det(S − λI) = 0        → 求出各个 λ\n(S − λI) v = 0         → 对每个 λ 求出 v\n按 λ 从大到小排序 → 归一化使 ‖v‖ = 1",
 "pts": [
   "<b>官方把这一问拆成四个检查</b>：<em>determinant</em>（求 λ）→ <em>null space</em>（求各自的 v）→ <em>order</em>（按最大 λ 排在前）→ <em>normalise</em>（保证 ‖v‖=1）。<b>四步缺一不可，尤其后两步最容易漏。</b>",
   "⚠️ <b>「归一化」不是可选项</b>：原话是 <em>Normalise the leading eigenvector <b>before using it as an axis</b></em>。因为特征向量方程 Sv=λv 对任意倍数都成立，不归一化的话「投影长度」可以靠拉长 v 随意放大，得分就没有意义了。",
   "<b>自检一：Σλ = trace(S)</b>。Tutorial 数据里 50 + 0 = 10 + 40 ✓。<b>这一秒钟的检查能挡住大部分特征值解错。</b>",
   "<b>自检二：det(S) = λ₁·λ₂</b>。这里 det = 10·40 − 20·20 = <b>0</b>，而 λ₁λ₂ = 50·0 = 0 ✓。<b>det = 0 本身就说明数据是秩 1 的。</b>",
 ],
 "tbl": [{"cap":"Q2 四步 · Tutorial 数据实做（已复算）",
   "head":["步","做什么","结果"],
   "rows":[
     ["determinant","解 det(S−λI)=0","λ² − 50λ + 0 = 0 ⇒ <b>λ = 50, 0</b>"],
     ["null space","对 λ=50 解 (S−50I)v=0","[[−40,20],[20,−10]]v=0 ⇒ v ∝ <b>(1, 2)</b>"],
     ["order","按 λ 降序","50 在前 ⇒ PC1 用 (1,2)"],
     ["<b>normalise</b>","除以 ‖v‖ = √5","v₁ = <b>(1,2)/√5 ≈ (0.4472, 0.8944)</b>"],
   ]},
  {"cap":"两个一秒钟自检",
   "head":["恒等式","这里的值","通过？"],
   "rows":[
     ["Σλ = trace(S)","50 + 0 = 10 + 40 = 50","✓"],
     ["λ₁·λ₂ = det(S)","50 × 0 = 0 = 10·40 − 20²","✓（det=0 ⇒ 秩 1）"],
   ]}],
 "exam": "求特征对是大题主体。<b>把两个自检写进答卷</b>——既防算错，也是采分点。归一化那一步<b>务必写出 √5</b>，只写 (1,2) 会扣分。",
 "tip": {"t":"高频失分点","v":"<b>忘记归一化</b>，直接拿 (1,2) 当轴去投影。那样算出的得分会是真实值的 √5 倍，解释方差比虽然不变，但<b>得分数值和重构结果全错</b>。","w":1},
},

18: {
 "quote": "<b>Question 3: Project and Reconstruct</b> — <em>A one-dimensional PCA result is one score per observation.</em> · 1 Choose PC1 — <em>use the normalised leading eigenvector</em> → 2 Project — <b>Z = Xc v₁</b> → 3 Reconstruct — <em>map the first score back and add μ</em> → 4 Interpret — <em>calculate and interpret the retained variance</em>",
 "pts": [
   "<b>第一句就是这一问的全部形状</b>：<em>A one-dimensional PCA result is one score per observation</em>——<b>降到一维，就是每个观测一个数</b>。n 个样本得到 n 个得分。",
   "<b>第 3 步的两个动作不能漏</b>：<em>map the first score back</em>（用 z·v₁ᵀ 映射回去）<b>and add μ</b>（加回均值）。",
   "<b>第 4 步是 calculate and interpret</b>——不只算出解释方差，还要<b>解释它意味着什么</b>。这里是 100%，意思是<b>这组数据本来就住在一条直线上，降到一维不丢任何信息</b>。",
   "⚠️ <b>但「不丢信息」要说清楚是在什么意义上</b>：不丢的是<b>输入的方差</b>。如果这两个特征背后还有个你关心的目标，PCA 照样可能把有用的东西丢掉（见 p9）。",
 ],
 "tbl": [{"cap":"Q3 四步 · Tutorial 数据实做（已复算）",
   "head":["步","操作","结果"],
   "rows":[
     ["1 选 PC1","归一化后的首特征向量","v₁ = (1,2)/√5"],
     ["2 投影","Z = Xc v₁","(2.236, 4.472, −2.236, −4.472) = (√5, 2√5, −√5, −2√5)"],
     ["3 重构","x̂ = z·v₁ᵀ + μ","<b>完全等于原始点</b>（误差 0）"],
     ["4 解释","λ₁/(λ₁+λ₂) = 50/50","<b>100%</b> —— 秩 1，降维无损"],
   ]},
  {"cap":"⚠ 对照：如果换成 by-hand 那组不共线的数据",
   "head":["","Tutorial（秩 1）","by-hand（不共线）"],
   "rows":[
     ["特征值","50, <b>0</b>","18, <b>2</b>"],
     ["解释方差","100% / 0%","<b>90% / 10%</b>"],
     ["重构误差","<b>0</b>","<b>2</b>（= 丢掉的 λ₂）"],
     ["几何上","点本来就在线上，垂线长度全 0","有两点各差 1，垂线可见"],
   ]}],
 "say": "⭐ 两组数据对照着看，能一次理解<b>「重构误差 = 被丢掉的特征值之和」</b>这个恒等式：Tutorial 丢掉 λ₂=0，误差就是 0；by-hand 丢掉 λ₂=2，误差就是 2（两者我都用 numpy 复算过）。这也正是<b>「最大化投影方差」与「最小化正交重构误差」等价</b>的数值体现——总方差是固定的，保住的越多、丢掉的就越少。CS229 用勾股定理给了这个等价性的严格证明。",
 "exam": "Q3 是完整流程的收尾。答题必须包含：<b>归一化的 v₁ → 每个得分 → 重构结果 → 解释方差的数值与含义</b>，最后补一句<b>「保住方差不等于保住对目标有用的信息」</b>。",
},

}
