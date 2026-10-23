# -*- coding: utf-8 -*-
"""把 M2T2（聚类）逐页精读加厚到 M1 那套自制笔记的密度。做法同 deepen_M2T1.py。

用到的数字全部核实过：
  {1,2,8,9} k=2 初始 1/8 → 分配 {1,2}{8,9} → μ=1.5/8.5 → J=1
  四点 A(−2,−1)B(−2,1)C(2,−1)D(2,1)：{A,B}|{C,D} J=4；{A,C}|{B,D} J=16（两者都稳定）
  silhouette {1,3}|{8,10} 点 1：a=2、b=(7+9)/2=8、s=6/8=0.75
  DBSCAN A=0 B=0.5 C=1.0 D=3.0 E=3.4，ε=0.6 MinPts=3 →
      邻域(含自身) A=2 B=3 C=2 D=2 E=2 ⇒ B core，A/C border，D/E noise，簇={A,B,C}
      ε 放大到 1.1 ⇒ A、C 也成 core，但**最终分组不变**
  讲义示例表 k=2(142, 0.58) k=3(76, 0.64) k=4(55, 0.52)
  评估框架决策表 k=2 sil .58 稳定但合并了要区分的组 / k=3 sil .55 稳定可解释 / k=4 sil .59 不稳定 ⇒ 选 k=3
"""

DATA = {

1: {
 "quote": "<b>Clustering</b> — <em>K-means, DBSCAN and the assumptions behind groups</em>",
 "pts": [
   "<b>副标题里的 assumptions 是关键词</b>：这一讲真正要你掌握的不是两个算法的步骤，而是<b>它们各自假设了「一个组」长什么样</b>。步骤十分钟能学会，假设才是考点。",
   "<b>K-means 认「到质心的距离」，DBSCAN 认「密度连通」</b>——这是两种<b>完全不同的「组」的定义</b>。所以它们在同一份数据上给出不同答案是<b>必然的</b>，不是谁算错了。",
   "<b>和 T1 的关系</b>：PCA 换<b>表示</b>（连续的新坐标轴），聚类给<b>分组</b>（离散的组归属）。两者都无监督、都没有 ground truth，但<b>输出的类型根本不同</b>。",
   "⚠️ 这一讲会反复出现一句话：<b>聚类结果是模型产出的摘要，不是自动发现的真实类别</b>。大题的最后一步就靠它。",
 ],
 "say": "把这一讲放进 CS229 那张 2×2 地图：横轴是<b>建不建模 P(x)</b>，纵轴是<b>数据住在低维子空间还是聚成团</b>。聚类占的是<b>「团」那一行</b>——非概率的是 <b>K-means</b>，概率的是 <b>GMM</b>（T3 的内容）。所以 <b>K-means 和 GMM 是同一行的两格</b>，差别只在建不建模概率；而 <b>DBSCAN 连这张表都进不去</b>，因为它既不建模 P(x)、也不假设「绕某个中心聚成团」，它只认<b>密度连通</b>。⚠️ 还有一件事要先知道：<b>DBSCAN 完全不在 CS229 的范围内</b>（Ng 的无监督只讲 k-means、GMM/EM、因子分析、PCA、ICA），所以这份精读里 DBSCAN 那几页的深度来自<b>课程自己的讲义</b>，不是 CS229。",
 "exam": "开场定调句：<b>「聚类没有供给的答案，所以判断一个分组好不好必须综合多类证据」</b>。后面三道大题都能接上。",
},

2: {
 "quote": "<b>M2 T2 Roadmap</b>：1 What Is Clustering? — <em>Grouping without supplied class labels</em> · 2 Similarity — <em>Distance and scaling define what “close” means</em> · 3 K-means · 4 Choosing k — <em>Inertia, silhouette and domain meaning</em> · 5 DBSCAN — <em>Dense regions, border points and noise</em>",
 "pts": [
   "⭐ <b>第 2 段的小标题是这一讲的枢纽</b>：<em>Distance and scaling define what “close” means</em>——<b>距离和缩放定义了「近」是什么意思</b>。换句话说，<b>「相似」不是数据自带的性质，是你选出来的</b>。",
   "<b>第 4 段把三种依据并列</b>：inertia、silhouette、<b>领域含义</b>。注意第三个——官方把「讲不讲得通」和两个数值指标放在同等地位。",
   "<b>第 5 段点出了 DBSCAN 的三个专有名词</b>：稠密区、<b>边界点</b>、<b>噪声</b>。后两个是 K-means 完全没有的概念。",
   "<b>路线图就是答题顺序</b>：被问「怎么做聚类」，按「定义相似 → 选算法 → 拟合 → 用多类证据选参数 → 解释与局限」写即可。",
 ],
 "tbl": [{"cap":"五段 ↔ 各自回答什么",
   "head":["段","小标题","回答的问题"],
   "rows":[
     ["1","What Is Clustering?","没有标签的情况下「分组」是什么意思"],
     ["2","<b>Similarity</b>","<b>「近」由距离与缩放定义</b>"],
     ["3","K-means","分配与更新两步、目标 J"],
     ["4","Choosing k","inertia / silhouette / <b>领域含义</b>"],
     ["5","DBSCAN","稠密区、边界点、<b>噪声</b>"],
   ]}],
 "exam": "「解释每一段如何引出下一段」是官方 Study check。一条干净的串法：<b>没有标签 ⇒ 必须自己定义「近」⇒ 定义好了才能跑算法 ⇒ 算法要一个 k ⇒ 选 k 需要多类证据 ⇒ 但 K-means 的假设不总成立 ⇒ 引出 DBSCAN</b>。",
},

3: {
 "quote": "<b>PCA and Clustering Solve Different Problems</b> — <em>PCA changes the representation; clustering assigns group structure.</em> · PCA: <em>Builds new continuous axes · Preserves high-variance directions · <b>No cluster labels are produced</b></em> · Clustering: <em>Builds discrete group assignments</em>",
 "pts": [
   "⭐ <b>「No cluster labels are produced」这句要原样记住</b>：<b>PCA 不产生任何簇标签</b>。「PCA 降到二维就看见两个簇了」是<b>视觉印象</b>，簇必须另外用聚类算法算出来。",
   "<b>共同点</b>（Study check 第一问）：两者都是无监督、都没有 ground truth、都依赖特征表示、都会被尺度影响、结果都需要解释。",
   "<b>最重要的差别</b>（第二问）：<b>输出的类型不同</b>——PCA 给<b>连续</b>的新坐标，聚类给<b>离散</b>的组归属。",
   "<b>什么时候这个差别会改变你的决定</b>（第三问）：当你要的是「把相关特征压缩掉」→ PCA；要的是「把样本分成几伙来分别对待」→ 聚类。⚠️ <b>「先 PCA 再聚类」是两个各自需要论证的决定</b>，不是一个。",
 ],
 "tbl": [{"cap":"两边对照（课件原表）",
   "head":["","PCA","聚类"],
   "rows":[
     ["造什么","<b>连续</b>的新坐标轴","<b>离散</b>的组归属"],
     ["对特征做什么","压缩相关特征","把近的/密度连通的点归到一起"],
     ["保住什么","高方差方向","组内相似、组间不相似"],
     ["产不产生簇标签","<b>不产生</b>","产生"],
   ]}],
 "say": "「先 PCA 再聚类」这个流程在实践中很常见，但它<b>横跨这张对照表的两边</b>，所以是<b>两个各自需要论证的决定</b>：① <b>为什么要降维</b>——是为了可视化、还是为了提速省内存？（CS229 里 Ng 明确只背书这两个理由）② <b>为什么在降维后的空间里聚类是合理的</b>——PCA 保住的是<b>高方差方向</b>，而<b>区分不同组的关键方向未必方差大</b>。⚠️ 换句话说，<b>降维可能恰好把区分组的那个方向丢掉了</b>。要论证这一步，最直接的办法是<b>对照</b>：降维前后各聚一次，比较成员与内部指标。",
 "tip": {"t":"高频失分点","v":"<b>「PCA 降到二维就得到了两个簇」</b>——错。PCA <b>不产生任何簇标签</b>；图上看起来分开只是投影后的视觉效果，簇要另外算。","w":1},
 "exam": "概念选择题常客。大题若出现「先 PCA 再聚类」的流程，记得指出<b>这是两个决定，各自都要论证</b>。",
},

4: {
 "quote": "<b>K-means Minimises Within-Cluster Squared Distance</b> — <em>Each point is assigned to one centroid, then centroids move to cluster means.</em> · <b>J = Σᵢ ‖xᵢ − μ_c(i)‖²</b> · <em>Assignment chooses the nearest centroid. Update replaces each centroid with the mean of its assigned observations.</em>",
 "eq": "J(c, μ) = Σᵢ ‖ xᵢ − μ_c(i) ‖²\n分配：c(i) ← argmin_j ‖xᵢ − μⱼ‖²      （固定 μ，动 c）\n更新：μⱼ ← (1/|Cⱼ|) Σ_{i∈Cⱼ} xᵢ      （固定 c，动 μ）",
 "pts": [
   "<b>J 的读法</b>：每个点到<b>它自己被分到的那个</b>质心的平方距离，全部加起来。下标 c(i) 就是「第 i 个点归哪一簇」。",
   "<b>三个名字同一个东西</b>：CS229 叫 <b>distortion function（失真函数）</b>，你们课件和 sklearn 叫 <b>inertia</b> 或 <b>WCSS</b>（within-cluster sum of squares）。",
   "⚠️ <b>J 直接鼓励的只有「簇内紧凑」</b>——它<s>没有</s>任何一项显式要求簇与簇之间离得远，更没有任何一项在保证「这些簇对应真实类别」。<b>低 J 只说明点离各自质心近。</b>",
   "⚠️ <b>J 是求和不是平均</b>，点越多越大 ⇒ <b>只能在同一份数据、同一套特征与缩放下比较</b>。拿标准化前后的 inertia 比大小是没有意义的，两者不在同一量纲上。",
 ],
 "tbl": [{"cap":"两步的「固定什么 / 动什么」正好互补",
   "head":["步","固定","优化","结果"],
   "rows":[
     ["分配","质心 μ","每点的归属 c","每点去<b>最近</b>的质心"],
     ["更新","归属 c","质心 μ","质心搬到该簇<b>均值</b>"],
   ]}],
 "say": "⭐ 上表这个互补结构不是巧合。CS229 讲义点破了它：<b>K-means 其实是对 J 做「坐标下降」</b>——J 有两组变量（分配 c 与质心 μ），同时优化很难，但<b>固定一组、优化另一组都有闭式最优解</b>。固定 μ 优化 c，答案是「选最近的」＝分配步；固定 c 优化 μ，答案是「取均值」＝更新步。<b>所以更新步取均值不是经验做法，而是「对一组固定的点，使 Σ‖xᵢ−c‖² 最小的 c 就是均值」这个最小二乘性质的直接结果。</b>",
 "exam": "大题常问「这两步在减小什么」——答 <b>J（inertia / WCSS）</b>，并补一句它只说明紧凑、不证明分组有意义。若问「为什么更新取均值」，答<b>均值是使簇内平方和最小的点</b>，比说「因为要取中心」高一个层次。",
 "tip": {"t":"容易答错","v":"<b>「J 越小说明簇分得越好」</b>——只在<b>同一份数据、同一个 k、同一套缩放</b>下才成立。k 越大 J 越小（k=n 时 J=0），所以 <s>不能用「J 最小」选 k</s>。","w":1},
},

5: {
 "quote": "<b>K-means Alternates Two Simple Steps</b> — <em>The objective cannot increase after a correct assignment or update step.</em> · 1 Initialise — <em>use k-means++ for spread-out starts; <b>n_init=10 runs ten starts and keeps the lowest-inertia result</b></em> → 2 Assign → 3 Update",
 "pts": [
   "⭐ <b>「The objective cannot increase」只是收敛论证的前半句。</b> 单调不增本身推不出「会停下来」——一个每次减一半的数列也单调不增，但永远不停。",
   "<b>完整论证还需要后半句</b>：<b>把 n 个点分到 k 个簇的方式只有有限多种</b>（至多 kⁿ），而每个确定的分配对应一个确定的 J 值 ⇒ <b>J 只能取有限多个值</b> ⇒ 不可能无限下降 ⇒ <b>必然在有限步内停下</b>。<b>答大题时两句都要写。</b>",
   "⚠️ <b>n_init=10 是十次独立重启</b>（<em>ten starts</em>），每次都跑到收敛，最后保留 <b>inertia 最低</b>的那一次。<s>不是迭代十轮</s>——迭代上限是 <code>max_iter</code>。这是高频混淆点。",
   "<b>k-means++ 做的是另一件事</b>：让<b>起始质心互相远离</b>（第一个随机取自数据，之后按距离平方加权抽样）。它改善<b>单次</b>的起点质量，n_init 用<b>重复</b>兜底，两者互补。⚠️ <b>但都只是降低风险，不保证全局最优。</b>",
 ],
 "tbl": [{"cap":"两道防线 · 别混淆的三个参数",
   "head":["参数","管什么","常见误解"],
   "rows":[
     ["<code>init='k-means++'</code>","让起始质心<b>散开</b>","以为它保证全局最优"],
     ["<code>n_init=10</code>","<b>独立重启 10 次</b>，取 inertia 最低","<s>误以为是迭代 10 轮</s>"],
     ["<code>max_iter</code>","<b>单次</b>拟合的迭代上限","—"],
   ]},
  {"cap":"收敛论证的两半（缺一不可）",
   "head":["","说了什么","够不够"],
   "rows":[
     ["课件给的","两步都不增加 J","<b>不够</b>——单调不增可以永不停止"],
     ["还需要补","分配方式有限 ⇒ J 取值有限","<b>合起来才推出有限步内停下</b>"],
   ]}],
 "say": "CS229 课上 Ng 的措辞其实很谨慎，他说的是 <em>this shows k-means must converge, <b>or at least this function must converge</b></em>——<b>他自己留了余地</b>，因为「非负 + 单调下降」严格说只能推出 J 这个<b>数列</b>收敛。讲义里那版「分配方式有限」才是更强的论证。另外他补了一条很实在的：超大数据上 J 降得太慢就<b>直接切断</b>，「也许它还没完全收敛，我们就切掉，叫它 good enough」——那就是 <code>max_iter</code> 的现实意义。",
 "exam": "「为什么 K-means 一定收敛」是高频问答。标准答法：<b>①两步都不增加 J ②分配方式有限所以 J 只能取有限个值 ⇒ 必然有限步停下</b>；再补一句<b>「但 J 非凸，停的地方只是局部极小」</b>。",
},

6: {
 "quote": "<b>K-means Works Best for Compact Centroid-Based Groups</b> — k: <em>Must be specified before fitting</em> · Scale: <em>Large-unit features dominate Euclidean distance</em> · Initialisation: <em>Different starts can reach different local optima</em> · Shape: <em>Non-spherical groups can be split incorrectly</em> · Outliers: <em>Extreme points pull centroids</em>",
 "pts": [
   "<b>五条软肋就是评价 K-means 结果的现成清单</b>：k 要事先给、尺度、初始化、形状、离群点。大题问「这个结果可靠吗」，逐条点名即可。",
   "<b>还有一条课件没列但同样重要</b>：<b>每个点必须有标签</b>——K-means 没有「噪声」这个选项。一个明显的离群点会被硬塞进某个簇，<b>还会把那个簇的均值质心拽偏</b>。<b>双重伤害。</b>",
   "<b>「形状」那条的机制</b>：K-means 假设簇是<b>紧凑、以质心为中心</b>的。两条互相缠绕的弯弧各自<b>没有有意义的「中心」</b>，于是算法会沿某个方向<b>横切</b>，得到的两个簇与真实结构完全无关。",
   "<b>「初始化」那条的后果</b>：同一份数据两次运行可以得到明显不同的分组。<b>这不是 bug，是 J 非凸的表现</b>——存在多个局部极小，落到哪个取决于初始质心。",
 ],
 "tbl": [{"cap":"四点例子：两个都「稳定」的解，质量差四倍",
   "head":["分法","质心","每点到质心","J"],
   "rows":[
     ["{A,B} | {C,D}（左右分）","(−2,0) 与 (2,0)","都是 1","<b>4</b>"],
     ["{A,C} | {B,D}（上下分）","(0,−1) 与 (0,1)","都是 2","<b>16</b>"],
   ]},
  {"cap":"五条软肋 · 机制与应对",
   "head":["软肋","机制","应对"],
   "rows":[
     ["k 要事先给","算法不会告诉你有几类","多证据选 k（见 p7）"],
     ["尺度","大量纲特征独占欧氏距离","比较缩放前后；必要时标准化"],
     ["初始化","J 非凸，多个局部极小","<b>k-means++ + n_init</b>"],
     ["形状","假设紧凑绕质心","弯曲结构改用 <b>DBSCAN</b>"],
     ["离群点","拽偏均值质心，且<b>必被分入某簇</b>","先查离群点；或用 DBSCAN 的 noise"],
   ]}],
 "say": "四点例子（A(−2,−1) B(−2,1) C(2,−1) D(2,1)）值得记住，因为它同时说明两件事：<b>①「上下分」那个 J=16 的解同样满足「再迭代也不变」</b>——它是个货真价实的局部极小，算法到那儿就停了不会自己爬出来；<b>②落到哪一个完全取决于初始质心</b>。这就是 J 非凸的实际后果：<b>算法必然停下，但不保证停对</b>。",
 "exam": "「同一份数据两次运行结果不同说明什么」——答 <b>J 非凸、存在多个局部极小、结果依赖初始化</b>，再给应对（k-means++ 与多次重启），并注明<b>不保证全局最优</b>。",
},

7: {
 "quote": "<b>Trust a Clustering Result Only When Evidence Agrees</b> — Internal evidence · Stability — <em>Compare initialisations, samples and nearby parameter values</em> · Geometry — <em>Inspect plots; <b>silhouette can favour compact convex groups</b></em> · Representation — <em>Recheck scaling</em>",
 "pts": [
   "⭐ <b>页标题就是答题原则</b>：<b>只有当多类证据一致时，才信这个聚类结果。</b>",
   "⚠️ <b>Geometry 那一行里藏着最重要的警告</b>：<em>silhouette can favour compact convex groups</em>——<b>silhouette 偏爱紧凑的凸形簇</b>。在弯曲结构上它可能<b>反而偏袒 K-means</b>，给出与几何事实相反的排序。<b>这句话几乎是每道聚类评价大题的必写句。</b>",
   "<b>官方 Study check 直接给了一个情形</b>：k=4 的 silhouette 最高但产生一个不稳定的小簇，k=3 稳定且可解释——<b>哪个更站得住？</b> 答：<b>k=3</b>。理由是<b>单一指标最高不足以取胜</b>，不稳定意味着那个划分可能只是某次初始化的偶然产物。",
   "<b>收尾必须写的那一句</b>：这是 <b>a reasoned judgement, not proof</b>（有依据的判断，不是证明）——评估框架页的原话。",
 ],
 "tbl": [{"cap":"讲义示例：同一份数据不同 k",
   "head":["k","inertia","silhouette","解读"],
   "rows":[
     ["2","142","0.58","较粗的分组"],
     ["3","<b>76</b>","<b>0.64</b>","<b>有力的候选</b>"],
     ["4","55","0.52","更细但分离更差"],
   ]},
  {"cap":"评估框架页的决策表（注意结论）",
   "head":["候选","内部证据","稳定性","应用证据"],
   "rows":[
     ["k=2","silhouette 0.58","稳定","<b>合并了专家要区分的两组</b>"],
     ["k=3","silhouette 0.55","稳定","三组解释得通 ⇒ <b>最终选它</b>"],
     ["k=4","silhouette <b>0.59（最高）</b>","<b>不稳定</b>","有个小组每次都在变"],
   ]}],
 "say": "两张表要分清出处：<b>上表来自聚类讲义</b>（k=3 在两个指标上都最好），<b>下表来自评估框架页</b>（k=4 的 silhouette 最高却不稳定，最终仍选 k=3）。<b>下表才是考点</b>——它演示的正是「单一指标最高不等于最好」。<br>另外有一条容易忽略的细节：<b>全局最优</b>的 inertia 随 k 增大不会上升，但<b>实际拟合</b>的多次运行会落进不同局部极小，所以<b>你观测到的 inertia 未必随 k 单调下降</b>——那不是 bug，应提高 <code>n_init</code> 后再比较。",
 "exam": "「该选哪个 k」的大题按四条扫：<b>内部指标 + 稳定性 + 几何与表示 + 领域有用性</b>，最后写 <b>a reasoned judgement, not proof</b>。<b>只报一个 silhouette 就下结论最多拿一半分。</b>",
},

8: {
 "quote": "<b>DBSCAN Border Points Join but Do Not Expand Clusters</b> — <em>Core-point connectivity grows a cluster; border points inherit membership only.</em> · Core-point rule: <b>|Nε(x)| ≥ MinPoints</b> · <em>A border point has too few neighbours to be core but lies within ε of a core point.</em> · <em><b>Only core points extend density reachability</b></em>",
 "eq": "Nε(x) = { z : ‖z − x‖ ≤ ε }        ⚠ 含 x 自己，且距离等于 ε 也算\ncore：|Nε(x)| ≥ MinPts\nborder：自己不够 core，但落在某个 core 点的 ε 邻域内\nnoise：两者都不是（sklearn 标 −1）",
 "pts": [
   "⚠️ <b>两个必须记死的约定</b>：ε 邻域<b>包含 x 自己</b>；距离<b>等于 ε 也算在内</b>（取等号）。手算题里错一个，整题的角色判定全错。",
   "⭐ <b>页标题就是最核心的规则</b>：<b>边界点加入簇，但不扩张簇。</b> 只有核心点能让簇继续长大——这是 DBSCAN 与 K-means 最结构性的差别。",
   "<b>为什么只有核心点能扩张</b>：因为「直接密度可达」的定义是「q 在 p 的邻域里<b>且 p 是核心点</b>」。<b>那个「且」就是一切的源头。</b>",
   "<b>噪声只是临时标签</b>：遍历时如果先访问到一个还没被认出邻居的点，它会被<b>暂时标成噪声</b>；等后面发现某个核心点的邻域包含它，它就<b>改判为边界点</b>。<b>噪声标签在遍历过程中不是终局。</b>",
 ],
 "tbl": [{"cap":"三类点 · 判定与能力",
   "head":["角色","判定条件","能扩张簇吗","属于簇吗"],
   "rows":[
     ["<b>core</b>","|Nε(x)| ≥ MinPts","<b>能</b>","是"],
     ["<b>border</b>","不够 core，但在某 core 的 ε 内","<b>不能</b>","是"],
     ["<b>noise</b>","两者都不是","—","<b>否</b>（sklearn 标 −1）"],
   ]},
  {"cap":"算例：A=0 B=0.5 C=1.0 D=3.0 E=3.4，ε=0.6，MinPts=3（已复算）",
   "head":["点","ε 邻域（含自身）","个数","角色"],
   "rows":[
     ["A = 0","{A, B}","2","border"],
     ["B = 0.5","{A, B, C}","<b>3</b>","<b>core</b>"],
     ["C = 1.0","{B, C}","2","border"],
     ["D = 3.0","{D, E}","2","<b>noise</b>"],
     ["E = 3.4","{D, E}","2","<b>noise</b>"],
   ]}],
 "say": "⭐ 这组算例有个很好的敏感性练习（官方 Study check）：<b>把 ε 放大到 1.1、MinPts 仍是 3 会怎样？</b> 算一下——A 的邻域变成 {A,B,C} 共 3 个，<b>A 也成了核心点</b>；C 同理。于是三个点都是 core。但 D、E 的邻域仍只有 {D,E}=2，<b>仍是噪声</b>。<b>结果：角色变了，但最终分组没变（还是 {A,B,C} + 两个噪声）。</b> 这正是大题要你做的那种参数敏感性分析。<br>另外注意 D、E 之间虽然只差 0.4（很近），但<b>两个点凑不够 MinPts=3</b>，所以它们形不成自己的簇。",
 "exam": "判角色是最可能出现的手算题之一。答题<b>列成表</b>：点 → 邻域集合 → 个数 → 角色，最后写出簇与噪声。<b>务必在开头声明「邻域含自身、距离取等也算」</b>。",
 "tip": {"t":"高频失分点","v":"<b>邻域不含自身</b>是最常见的错，会让每个计数少 1，角色判定全部偏一位。<b>距离等于 ε 不算</b>也错——本课与 sklearn 都取 ≤。","w":1},
},

9: {
 "quote": "<b>M2 T2 Checkpoint</b>：Distance — <em>scale features before neighbourhood methods</em> · K-means assignment — <em>nearest centroid</em> · Centroid update — <em>mean of assigned points</em> · DBSCAN core — <em><b>count ε-neighbours including self</b></em> · Noise — <em>label −1 in scikit-learn</em>",
 "pts": [
   "<b>五个必须能默写的点</b>，Study check 要求 <em>without looking</em>。",
   "⚠️ <b>第一条就是顺序问题</b>：<em>scale features <b>before</b> neighbourhood methods</em>——<b>先缩放，再用基于邻域的方法</b>。因为 ε 是一个带量纲的距离阈值，缩放一变它的含义就全变了。",
   "⭐ <b>第四条官方特意写了 including self</b>——这是最容易错的约定，课件把它放进 Checkpoint 说明它是考点。",
   "<b>要能说出一条连接</b>（Study check 的要求）：最容易说的是——<b>K-means 的「最近质心」和 DBSCAN 的「ε 邻域」用的是同一个距离，所以两者都受缩放影响；但前者强制每点有标签，后者允许标 −1</b>。",
 ],
 "tbl": [{"cap":"五点默写自检（盖住右列）",
   "head":["量","定义"],
   "rows":[
     ["Distance","<b>先缩放</b>再用邻域方法"],
     ["K-means 分配","最近的质心（质心此刻不动）"],
     ["质心更新","该簇点的<b>均值</b>"],
     ["DBSCAN core","|Nε(x)| ≥ MinPts，<b>邻域含自身</b>"],
     ["Noise","sklearn 里标签 <b>−1</b>"],
   ]}],
 "say": "这五个量之间可以串成一条线，Study check 要的就是这种连接：<b>距离是地基</b>——K-means 的「最近质心」和 DBSCAN 的「ε 邻域」<b>用的是同一个欧氏距离</b>，所以<b>两者都受缩放影响</b>，这就是为什么第一条写「先缩放」。但两者<b>用距离的方式不同</b>：K-means 拿它<b>比较</b>（离哪个质心更近），DBSCAN 拿它<b>设阈值</b>（是不是在 ε 以内）。⭐ 这个差别有个实际后果：<b>K-means 只关心相对远近，等比例缩放全部特征不改变分组</b>；而 <b>DBSCAN 的 ε 是绝对阈值，等比例缩放会彻底改变结果</b>。这就是讲义反复强调「<b>ε 必须在缩放之后选</b>」的原因。",
 "exam": "Checkpoint 的五点<b>就是手算大题会用到的全部约定</b>。考前默写一遍能确认没漏洞。",
},

10: {
 "quote": "<b>Section 1 Complete: Clustering</b> — Key Takeaways：<em>Clustering has no supplied answer key</em> · <em>Distance and scaling encode similarity</em> · <em>K-means alternates assignment and mean update</em> · <em><b>Inertia always falls as k grows, so context still matters</b></em> · <em>DBSCAN can find noise and non-centroid-shaped clusters</em>",
 "pts": [
   "<b>第四条是本页最该记的</b>：<em>Inertia always falls as k grows</em>——<b>inertia 随 k 增大必然下降</b>，所以<b>不能用「inertia 最小」选 k</b>（k=n 时 J=0）。后半句 <em>so context still matters</em> 指的就是领域含义。",
   "<b>第一条定调</b>：<em>no supplied answer key</em>——没有供给的答案。这是所有「必须多证据」论证的根。",
   "<b>第五条是 DBSCAN 的两个独有能力</b>：<b>找到噪声</b>、<b>找到非质心形状的簇</b>。K-means 两样都做不到。",
   "⚠️ <b>但第四条有个更细的版本值得知道</b>：严格说，是<b>全局最优</b>的 inertia 随 k 不上升；<b>实际拟合</b>因为会落进不同局部极小，<b>观测到的 inertia 未必单调</b>。看到 k 变大 inertia 反而上升，<s>那不是 bug</s>。",
 ],
 "tbl": [{"cap":"五条小结 · 各自的考试用途",
   "head":["小结","在大题里怎么用"],
   "rows":[
     ["没有供给的答案","开头定调句"],
     ["距离与缩放编码相似","评价第一句：量纲不可比就该讨论缩放"],
     ["分配与均值更新交替","手算题的流程"],
     ["<b>inertia 随 k 必降</b>","否掉「用 inertia 最小选 k」"],
     ["DBSCAN 能找噪声与非凸簇","选算法的理由"],
   ]}],
 "exam": "小结页的五句话每句都能当采分句。尤其<b>「inertia 随 k 必降，所以还要看语境」</b>。",
},

11: {
 "quote": "<b>Section 2: M2 T2 Tutorial Activity</b> — <em>Three core questions compare centroid and density-based clustering</em> · Q1 <em>performs one complete K-means assignment/update step</em> · Q2 <em>applies DBSCAN neighbourhood, core, border and noise rules</em> · Q3 <em>chooses an algorithm and explains scaling and parameter effects</em>",
 "pts": [
   "<b>三问的分工很清楚</b>：Q1 手算 K-means 一轮；Q2 判 DBSCAN 角色；Q3 <b>论证选哪个算法</b>。前两问考计算，<b>第三问考判断</b>。",
   "<b>Q3 才是分值密度最高的</b>——它要你从<b>几何、噪声处理、尺度、参数含义</b>四个角度论证。这四个词就是答题提纲。",
   "⚠️ <b>评分要求是 Show diagnostic working</b>：要展示中间步骤。Q1 要写出每点的两个距离比较，Q2 要写出每点的邻域集合。",
   "<b>Q3 的标准三段式</b>：<b>①这份数据的什么特征决定了选择 ②因此选谁、为什么它的假设更匹配 ③这个选择的代价是什么、还需要检查什么</b>。只写「DBSCAN 更好」没有分。",
 ],
 "tbl": [{"cap":"三问 ↔ 对应的知识点页",
   "head":["问","测什么","回看哪一页"],
   "rows":[
     ["Q1","K-means 一轮（分配 + 更新）","p4、p5"],
     ["Q2","DBSCAN 的邻域/core/border/noise","p8"],
     ["Q3","<b>选算法并论证</b>","p6、p7、p8"],
   ]}],
 "say": "三问的<b>难度和分值分布不均匀</b>，时间要相应分配。Q1 和 Q2 是<b>机械计算</b>——流程记熟了就是送分题，但<b>必须展示中间步骤</b>（题干明确要求 <em>Show diagnostic working</em>）：Q1 要写出每个点到两个质心的距离比较，Q2 要写出每个点的邻域集合与计数。<b>Q3 才是拉开差距的地方</b>：它没有标准答案，考的是<b>能不能用四个角度把选择论证清楚</b>。⚠️ 这里最常见的失分不是选错算法，而是<b>只给结论不给理由</b>——「这份数据是弯曲的所以用 DBSCAN」只答了一半，还要说清<b>为什么 K-means 的假设在这里不成立</b>（它假设簇绕质心、弯弧没有有意义的中心）以及<b>选 DBSCAN 的代价</b>（ε 与 MinPts 更难设、密度差异大时会失效）。",
 "exam": "Q3 型大题的答题提纲：<b>几何 → 噪声处理 → 尺度 → 参数含义</b>，最后补代价与还需检查什么。",
},

12: {
 "quote": "<b>Question 1: Assignment, Then Mean Update</b> — <em><b>Keep the current centroids fixed throughout each assignment step.</b></em> · 1 Initialise — <em>use the supplied initial centroids</em> → 2 Assign — <em>compare each point’s two distances</em> → 3 Update — <em>average coordinates within each cluster</em> → 4 Explain objective",
 "pts": [
   "⭐ <b>第一句是评分点</b>：<em>Keep the current centroids fixed throughout each assignment step</em>——<b>整个分配步里质心保持不动</b>。边分边更新是<em>序贯版本</em>，会得到不同结果。",
   "<b>第 1 步写着 use the supplied initial centroids</b>——<b>用题目给的初始质心</b>，别自己选。",
   "<b>第 4 步 Explain objective 单独列出来</b>，说明<b>光算对不给满分</b>：还要说出这两步在<b>减小 J</b>。",
   "<b>手算技巧</b>：比较距离时<b>可以只比平方距离</b>，不用开根号（平方是单调变换，不改变大小关系）。",
 ],
 "tbl": [{"cap":"标准例子 {1, 2, 8, 9}，k=2，初始质心 1 与 8（已复算）",
   "head":["点","到 μ₁=1","到 μ₂=8","归谁"],
   "rows":[
     ["1","0","7","μ₁"],
     ["2","1","6","μ₁"],
     ["8","7","0","μ₂"],
     ["9","8","1","μ₂"],
   ]},
  {"cap":"更新与收敛",
   "head":["量","计算","结果"],
   "rows":[
     ["μ₁","(1+2)/2","<b>1.5</b>"],
     ["μ₂","(8+9)/2","<b>8.5</b>"],
     ["J","4 × 0.5²","<b>1</b>"],
     ["再分配一次","分组不变","<b>已收敛</b>"],
   ]}],
 "say": "⚠️ 这个例子的收尾有一句容易被忽略但很重要的话：<b>这个计算说明了两步为什么不会增加 J，它并不证明 k=2 对这份数据是「正确」的簇数</b>——那是另一个问题（见 p7）。另外注意质心<b>移到了两点中间</b>（1.5 不是原数据点），<b>质心不必是实际观测</b>。",
 "exam": "Q1 原型。必写：<b>题目给的初始质心 → 每点的两个距离比较 → 更新后的质心 → 这两步在减小 J</b>。",
 "tip": {"t":"高频失分点","v":"<b>边分配边更新质心。</b> 标准 K-means 是<b>批量</b>的：基于同一组固定质心把所有点分完，再统一取均值。","w":1},
},

13: {
 "quote": "<b>Question 2: Core Points Expand Density-Connected Sets</b> — <em>Track how tentative labels can change as density connectivity is explored.</em> · <b>Nε(x) = {z : ‖z−x‖ ≤ ε}</b> · <em><b>MinPoints counts all members of Nε(x), including x.</b></em> · <em>Only core points expand a cluster; border points belong without expansion.</em>",
 "pts": [
   "⚠️ <b>官方把「including x」单独写成一句</b>，说明这是考点。<b>MinPoints 数的是邻域全部成员，包括 x 自己。</b>",
   "⭐ <b>页标题的 tentative labels 是关键词</b>：<b>临时标签会随着密度连通被探索而改变。</b> 一个点可能先被标成噪声，后来被改判为边界点。",
   "<b>为什么会这样</b>：遍历时先访问 A，那时还没发现 B 是核心点，A 自己邻域不够 ⇒ 暂标噪声；继续遍历访问到 B，发现它是核心点并开始扩张，而 B 的邻域里有 A ⇒ <b>A 被吸收，改判为边界点</b>。",
   "<b>四个检查</b>（课件列的）：算距离 → 数邻域 → 判角色 → 追踪连通性。<b>按这个顺序做不会乱。</b>",
 ],
 "tbl": [{"cap":"答题模板：一行一个点",
   "head":["点","ε 邻域（含自身）","个数","≥MinPts?","角色"],
   "rows":[
     ["A = 0","{A, B}","2","否","border（挨着 core B）"],
     ["B = 0.5","{A, B, C}","3","<b>是</b>","<b>core</b>"],
     ["C = 1.0","{B, C}","2","否","border"],
     ["D = 3.0","{D, E}","2","否","noise"],
     ["E = 3.4","{D, E}","2","否","noise"],
   ]},
  {"cap":"⚠ 边界点的两个性质",
   "head":["性质","后果"],
   "rows":[
     ["属于簇但<b>不扩张</b>","簇的生长完全由 core 点驱动"],
     ["可能<b>同时够得着两个簇</b>","最终归谁取决于<b>遍历顺序</b> ⇒ 解读孤立边界点要谨慎"],
   ]}],
 "say": "相比之下，<b>核心点组成的连通块是稳定的</b>，不受遍历顺序影响；不稳定的只有孤立边界点的归属。这一点在写「局限」时可以用：<b>「边界点的归属可能依赖遍历顺序，但核心结构是稳定的」</b>。",
 "exam": "Q2 原型。<b>务必列成上面那张表</b>，并在开头声明「邻域含自身、距离取等也算」。若问「为什么先标噪声的点后来变成边界点」，答<b>后来访问到的某点被认出是核心点，而它的邻域包含这个点</b>。",
},

14: {
 "quote": "<b>Question 3: Compare Algorithm Assumptions</b> — <em>Justify a choice using geometry, noise handling, scale and parameter meaning.</em> · 1 K-means — <em>what shape and assignment assumptions apply?</em> → 2 DBSCAN — <em>what density and noise behaviour is relevant?</em> → Scale — <em>could one feature dominate distance?</em> → <em>compare forced assignment with noise labelling</em>",
 "pts": [
   "⭐ <b>四个论证角度就写在标题里</b>：<b>几何（geometry）、噪声处理（noise handling）、尺度（scale）、参数含义（parameter meaning）</b>。答题时四个都点到，分就齐了。",
   "<b>最后那句对比是核心</b>：<em>compare forced assignment with noise labelling</em>——<b>「强制每点都有标签」对比「允许标为噪声」</b>。这是两个算法最实用的一条差别。",
   "<b>几何角度</b>：K-means 假设紧凑、绕质心（偏凸形）；DBSCAN 认密度连通，<b>能沿弯曲形状一路长过去</b>，因为它从不需要一个「中心」。",
   "⚠️ <b>比较时的两个陷阱</b>：<s>别用 silhouette 做唯一裁判</s>（它偏爱凸形，在弯曲结构上可能反而偏袒 K-means）；<s>别跨算法比 inertia</s>（DBSCAN 根本不优化它）。",
 ],
 "tbl": [{"cap":"两算法对比（Q3 的现成骨架）",
   "head":["问题","K-means","DBSCAN"],
   "rows":[
     ["必须指定的参数","簇数 k","ε 与 min_samples"],
     ["典型几何","紧凑、凸形、绕质心","连通稠密区，<b>可弯曲</b>"],
     ["未分配观测","<b>没有</b>，每点必有标签","<b>有</b>，稀疏点记 −1"],
     ["主要敏感性","初始化、k、离群点、尺度","邻域参数、<b>密度差异</b>、尺度"],
     ["优化目标","最小化 WCSS","<b>没有全局目标函数</b>"],
   ]}],
 "say": "⚠️ 最后一行值得单独说：<b>DBSCAN 没有全局目标函数</b>——它不是在优化某个数值，而是按「密度连通」这个<em>定义</em>直接把簇构造出来。这解释了为什么<b>拿 inertia 去比较两个算法是没有意义的</b>。<br>还有一条能直接拿分的：<b>当不同真实簇的密度差异很大时，一组全局的 (ε, MinPts) 无法同时描述两边的「稠密」</b>——往稀疏那边调，稠密的几个簇就连成一片；往稠密那边调，稀疏的那个簇整个被判成噪声。<b>这是方法的内在限制，不是参数没调好。</b>",
 "exam": "Q3 三段式：<b>①这份数据的什么特征决定了选择 ②因此选谁、为什么假设更匹配 ③代价是什么、还需检查什么</b>。补上两个比较陷阱，基本满分。",
},

15: {
 "quote": "<b>Section 3: Clustering Practical</b> — <em>Use supplied synthetic data and a consistent scaling workflow</em> · Q1 <em>fit K-means and inspect inertia</em> · Q2 <em>compare candidate k values with silhouette evidence</em> · Q3 <em>test density parameters and scaling; explain point roles</em> · Q4 <em>compare algorithms on curved groups</em>",
 "pts": [
   "<b>Practical 四问的重点在 Q4</b>：<em>compare algorithms on curved groups</em>——<b>在弯曲的组上比较两个算法</b>。这正是 K-means 会失败、DBSCAN 会成功的经典场景。",
   "⚠️ <b>Q4 的陷阱</b>：在弯曲数据上，<b>silhouette 可能反而给 K-means 更高的分</b>，因为它偏爱凸形。所以评价时必须<b>把标签画回散点图看形状</b>，不能只看分数。",
   "<b>「consistent scaling workflow」是贯穿要求</b>：整个 notebook 用同一套缩放流程，否则各问的结果不可比。",
   "<b>Q3 要 explain point roles</b>——解释 core / border / noise 各自是什么、各占多少。<b>报告噪声比例是评估 DBSCAN 的必要一步。</b>",
 ],
 "tbl": [{"cap":"四问 · 用什么证据",
   "head":["问","做什么","用什么证据"],
   "rows":[
     ["Q1","拟合 K-means","inertia"],
     ["Q2","比较候选 k","<b>silhouette</b>"],
     ["Q3","测密度参数与缩放","<b>三类点的角色与比例</b>"],
     ["Q4","弯曲组上比较两算法","<b>几何检视 + 噪声比例 + 稳定性</b>"],
   ]}],
 "exam": "Practical 的结论常被搬进大题。记住：<b>弯曲结构上 silhouette 可能偏袒 K-means</b>，必须补几何检视。",
},

16: {
 "quote": "<b>How to Work Through the Clustering Notebook</b> — 1 Run in order — <em>create and scale the common dataset</em> → 2 Choose k — <em>fit K-means and compare silhouette scores</em> → 3 Inspect DBSCAN roles — <em>separate core, border and noise</em> → 4 Compare and interpret",
 "pts": [
   "<b>第 1 步 create and scale the common dataset</b>——<b>先建好并缩放公共数据集</b>，后面各问都用它。这保证了各问结果可比。",
   "<b>第 3 步的动词是 separate</b>：把 core、border、noise <b>分开</b>来看。sklearn 里核心点的下标在 <code>core_sample_indices_</code>，噪声是 <code>labels_ == -1</code>。",
   "⚠️ <b>官方 Study check 问了一个重要的方法论问题</b>：<em>how will you avoid using test data to make development decisions?</em>——<b>怎么避免用测试数据做开发决策。</b> 这是泄漏问题在聚类语境下的版本。",
   "<b>答案</b>：调参（选 k、选 ε）只能用<b>训练数据或验证数据</b>；测试数据留到最后一次性评估。缩放也只能在训练数据上 fit。",
 ],
 "tbl": [{"cap":"四步 · 每步的输出与检查",
   "head":["步","做什么","看什么"],
   "rows":[
     ["1 按顺序跑","建数据、<b>统一缩放</b>","各问可比"],
     ["2 选 k","拟合并比 silhouette","别只看一个数"],
     ["3 <b>分开看三类点</b>","core / border / noise","<b>噪声比例</b>"],
     ["4 比较与解释","两算法在弯曲组上","<b>把标签画回散点图</b>"],
   ]}],
 "exam": "「怎么避免用测试数据做开发决策」是可以直接问的概念题。答：<b>选 k 与选 ε 只用训练/验证数据，缩放只在训练数据上 fit，测试数据留到最后一次性评估</b>。",
},

}
