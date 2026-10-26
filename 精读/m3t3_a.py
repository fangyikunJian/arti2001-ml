# -*- coding: utf-8 -*-
"""M3 T3《模型评估》逐页精读 —— 第 1–9 页（训练证据与数据划分段）。

素材：M3材料/课件/M3T3_Model_Evaluation.pptx（18 张，裁掉 p2 致辞页 ⇒ 17 页）
⭐ 有 pptx ⇒ 有备注讲稿，而且这一份讲稿写得特别细（p5 把实验的控制变量全列了，
   p10 把混淆矩阵的构造规则逐格说明）。

⚠ 数字全部取自 M3材料/笔记与阅读/ 的讲义整理，已被 verify_m3.py 复算（165/165）。
字段见 [[slide-reader]]：r/t/star/one/quote/eq/pts/tbl/say/exam/tip
"""

PART_A = [

{"r": [1, 1], "t": "评估回答的是另一个问题", "star": 1,
 "one": "前两讲都在问「怎么把参数调好」，这一讲问的是「调好之后，凭什么相信它在新数据上也行」。",
 "quote": "<b>Model Evaluation</b> — <em>Training evidence, stopping and generalisation</em>（M3 Topic 3）",
 "pts": [
   "<b>副标题三个词就是三块</b>：<em>training evidence</em>（训练过程留下的证据怎么读）、<em>stopping</em>（什么时候停）、<em>generalisation</em>（泛化——在没见过的数据上的表现）。",
   "⭐ <b>讲稿把这一讲的全部依赖列全了</b>：<em>Reliable conclusions depend on <b>protected data splits</b>, <b>correctly constructed metrics</b>, <b>appropriate thresholds</b>, and awareness of <b>leakage, imbalance, sampling, and shift</b>.</em> —— 可靠的结论依赖四件事：<b>受保护的数据划分、正确构造的指标、合适的阈值</b>，以及对<b>泄漏 / 不平衡 / 抽样 / 漂移</b>这四种坑的警觉。",
   "⚠️ <b>和 T1、T2 的分工</b>：T1 和 T2 讲的是<b>优化</b>（怎么把损失降下去），T3 讲的是<b>评估</b>（降下去之后说明了什么）。讲稿第 2 页说得很直接：<em>Topic 2 explained how to calculate and implement updates. Topic 3 now <b>interprets</b> the resulting training evidence.</em>",
   "⚠️ <b>原课件第 2 页是致辞页，裁页时已去掉</b>，所以本页 p2 = 原 p3，后面每页都少 1。",
 ],
 "exam": "T3 在考纲里占六条：<b>训练/验证/测试的角色与泄漏、欠拟合过拟合的证据、学习率证据、重复训练证据、基于验证集的早停、混淆矩阵与四个指标、ROC/AUC 与阈值权衡</b>——几乎这一讲的每一页都对应一条。",
},

{"r": [2, 2], "t": "六段路线图：从训练证据走到 ROC", "star": 2,
 "one": "训练证据 → 划分与停止 → 混淆矩阵 → precision/recall → ROC/AUC → Tutorial 与复习。",
 "quote": "1 Training evidence: Learning rate and repeated updates · 2 Splits and stopping: Development decisions and <b>a protected test set</b> · 3 Confusion Matrix: Count four kinds of outcomes · 4 Precision and Recall: <b>Different views of error</b> · 5 ROC and AUC: <b>Ranking across thresholds</b> · 6 Tutorial &amp; Revision: Calculate metrics; prepare for the <b>Week 13 test</b>.",
 "pts": [
   "⭐ <b>每一段的副标题都点出了那一段的「一句话」</b>：划分那段是「<b>受保护的</b>测试集」；precision/recall 那段是「<b>对误差的不同视角</b>」；ROC 那段是「<b>跨阈值的排序</b>」。这三句分别是三块最该记的定性结论。",
   "<b>讲稿交代了学习顺序</b>：<em>Study data roles and stopping, then confusion-matrix metrics and ROC/AUC.</em> —— <b>先数据角色与停止，再指标，最后 ROC</b>。",
   "⚠️⚠️ <b>讲稿还交代了 Python 练习的安排，和 T1/T2 不一样</b>：<em>Optional Python practice includes <b>Q3 of the M3 T1 notebook</b> for learning-rate experiments, then the <b>M3 T3 evaluation notebook</b>.</em> —— T3 <b>没有排定的 practical</b>（p17 会再说一次），这两个 notebook 都是<b>选做、不计分</b>。",
   "<b>「The tutorial questions are unchanged」</b> —— T3 的 Tutorial 题目<b>没有改动</b>（对照 T2 那边「四题合并成三题」的说明）。",
 ],
 "exam": "选择题可能考「T3 有没有 practical」（答<b>没有排定的</b>，只有选做 notebook）。更重要的是这六段就是 T3 扩展题的分类框架。",
},

{"r": [3, 3], "t": "训练和评估回答的是不同的问题", "star": 3,
 "one": "优化拟合参数，评估估计未来行为 —— 而且课件对每一种「表现」都加了限定，别一口咬定。",
 "quote": "<b>Optimisation fits parameters; evaluation estimates future behaviour.</b> Training: Poor training fit — inspect capacity and optimisation. <b>Strong training performance alone is not enough.</b> Evaluation: Uses validation/test data not used for fitting. <b>A large train–validation gap needs investigation.</b> Compare against a baseline and the intended use.",
 "pts": [
   "⭐⭐ <b>这一页的价值全在讲稿的限定词里</b>，正文反而是概括。逐条抄下来：",
   "<b>① 训练表现差</b>：<em>Poor training performance can reflect limited capacity, insufficient optimisation, poor preprocessing or data issues; <b>it does not by itself prove underfitting</b>.</em> —— 可能是<b>容量不足 / 优化不够 / 预处理差 / 数据问题</b>，<b>本身不能证明欠拟合</b>。",
   "<b>② 训练–验证差距大</b>：<em>A train–validation gap can suggest overfitting, <b>but also check sampling and distribution differences</b>.</em> —— 可以<b>提示</b>过拟合，但<b>还要检查抽样和分布差异</b>。",
   "<b>③ 两边分数接近</b>：<em><b>Similar scores can both be poor.</b></em> —— <b>接近也可能是「两边都很差」</b>。⚠️ 这条最容易被忽略：很多人看到训练和验证接近就下「泛化良好」的结论，其实要先看<b>这个数值本身够不够好</b>。",
   "<b>④ 怎么才算好</b>：<em>Compare the same metric on comparable populations and examine <b>an appropriate baseline</b>.</em> —— <b>在可比的人群上比同一个指标，并且要看一个合适的基线</b>。基线是什么？对不平衡的二分类，最常用的就是「全判多数类」的准确率。",
 ],
 "tbl": [{"cap": "三种「训练–验证」模式的标准答法（照这个措辞写）",
   "head": ["看到什么", "可以说", "⚠ 必须补的限定"],
   "rows": [
     ["训练差、验证也差", "可能欠拟合或优化困难", "可能是容量、优化、预处理或数据问题；<b>本身不证明欠拟合</b>"],
     ["训练强、验证明显更差", "可能过拟合", "归因于方差之前要先查<b>分布差异、验证集过小、泄漏</b>"],
     ["两边都强且接近", "学到的模式迁移到了未见样本", "⚠ <b>接近也可能两边都差</b>；要和<b>基线</b>比"],
   ]}],
 "exam": "⭐⭐ <b>扩展题最爱考的一页</b>。给一组训练/验证分数让你诊断。<b>满分结构 = 判定 + 机制 + 限定 + 下一步（都在验证集上做）</b>。⚠️ 只写「这是过拟合」最多一半分。",
 "tip": {"t": "一句万能的收尾", "v": "任何诊断题的最后都可以加这一句：<b>这些是诊断模式，不是证明；要把差距归因于方差之前，还需要排除分布差异、验证样本过小和数据泄漏。</b>", "w": 0},
},

{"r": [4, 4], "t": "每个数据划分只有一个主要角色", "star": 3,
 "one": "训练拟合、验证选择、测试估计 —— 一旦拿测试结果做决定，它就变成验证集了。",
 "quote": "<b>Reusing test data for decisions turns it into validation data.</b> train → fit; validation → choose; test → estimate. <b>Hyperparameters and thresholds are decisions and therefore belong before the final test.</b> Cross-validation supports development choices; <b>keep a separate final test set</b>. … future data — <b>may still shift from all splits</b>.",
 "pts": [
   "⭐⭐ <b>副标题那句是整讲最该背的一句</b>：<em>Reusing test data for decisions <b>turns it into</b> validation data.</em> —— 拿测试数据做决定，<b>它就变成了验证数据</b>。不是「不太好」，是<b>性质变了</b>。",
   "<b>训练集拟合的不只是权重</b>：讲稿写明 <em>Training fits parameters, <b>including preprocessing parameters</b>.</em> —— <b>包括预处理的参数</b>（缩放的均值方差、缺失值填补的值）。这是泄漏最常见的入口。",
   "<b>验证集管哪些决定</b>：<em>architecture, learning rate, <b>threshold</b> and <b>stopping checkpoint</b></em> —— 结构、学习率、<b>判定阈值</b>、<b>停止的检查点</b>。⚠️ 阈值和停止点是<b>决定</b>，不是参数，所以归验证管。",
   "⚠️⚠️ <b>测试集也不是真相</b>：<em>A held-out estimate <b>still has sampling uncertainty</b> and depends on whether its cases represent the intended population.</em> —— 留出估计<b>仍带抽样不确定性</b>，而且取决于它的样本能不能代表目标人群。",
   "⭐ <b>第四列那个 future data 是课件自己加的第四种「数据」</b>：<em>may still shift from all splits</em> —— <b>未来的数据可能和三个划分全都不一样</b>。这就是 p9 要讲的 shift（分布漂移）。",
   "<b>交叉验证的位置</b>：<em>Cross-validation supports development choices; <b>keep a separate final test set</b>.</em> 而且 <em>Cross-validation folds must also keep preprocessing <b>inside each training fold</b>.</em> —— <b>每一折的预处理都要在那一折的训练部分里拟合</b>。",
 ],
 "eq": "防泄漏五步（讲义版，顺序不能乱）：\n  1. 先划分成 训练 / 验证 / 测试\n  2. 只用训练集算填补与缩放参数\n  3. 把学到的参数**应用**到验证集和测试集 —— 不要重新拟合\n  4. 用验证结果选择模型与超参数（含阈值、停止点）\n  5. 所有选择固定之后，在没碰过的测试集上评估**一次**",
 "exam": "⭐⭐⭐ <b>考纲第一条就是这个</b>。官方示例选择题（阈值那道）的正确答案就是这句话的改写：<b>测试集已经影响了模型选择；阈值应当用验证数据选，测试集留给最终评估。</b>",
},

{"r": [5, 5], "t": "学习率：三行是三次互相独立的实验，不是三步", "star": 3,
 "one": "每一行都从同一组初始参数重置后只走一步 —— 所以「η=10 这一步最低」不能推出「η=10 最好」。",
 "quote": "<b>Reset to the same initial parameters for each row; use the same full-batch gradient.</b> η = 0.1 → 0.574996 · η = 10 → 0.371611 · η = 100 → 9.965953. Initial mean BCE = 0.580352. <b>These are separate experiments, not successive updates.</b> <b>The best one-step result does not establish the best rate for a full run or new data.</b>",
 "eq": "θ_new = θ − η·∇L        ← η 乘在梯度上\n\n起始平均 BCE = 0.580352\n  η = 0     ⇒ 0.580352（参数没变）\n  η = 0.1   ⇒ 0.574996\n  η = 1     ⇒ 0.533347\n  η = 10    ⇒ 0.371611   ← 这一步最低\n  η = 100   ⇒ 9.965953   ← 飞了",
 "pts": [
   "⚠️⚠️ <b>这一页最容易误读</b>：三行不是「连着走了三步」，而是<b>三次独立实验</b>——每次都回到同一个起点，只改 η。课件在正文和讲稿里各强调了一次。",
   "⭐ <b>讲稿把控制变量列全了</b>（课件右栏也有）：<b>data</b> 同样四个观测、<b>start</b> 同样的初始参数、<b>gradient</b> 同样的初始批梯度、<b>change</b> 只有学习率。⇒ 这是一个标准的受控实验，<b>答题时可以照着说「唯一变化的是 η」</b>。",
   "<b>那四个观测是什么</b>：讲稿写明 <em>([1,2],1), ([-1,-2],1), ([2,-1],0), ([-2,1],0)</em>，网络是<b>隐藏层那一课的初始两隐藏单元 ReLU 网络 + sigmoid 输出 + 平均 BCE</b>。⇒ 和 T2 p8 那个算例<b>是同一个网络</b>。",
   "⚠️ <b>η = 100 为什么会飞</b>：<em>A very large step can overshoot <b>or change which ReLU units are active</b>.</em> —— <b>过冲，或者改变「哪些 ReLU 单元是激活的」</b>。后半句很精彩：步子太大会把 z 推过 0，整个网络的「哪条路通」都变了。",
   "⚠️⚠️ <b>两条限定必须写进答案</b>：① <em>These data have <b>no validation/test sample</b>, so the table demonstrates <b>optimisation behaviour only</b>.</em>——<b>这组数据没有验证/测试样本，所以这张表只说明优化行为</b>，和泛化无关；② <em>A rate that helps now may fail later as gradients and activation regions change.</em>——<b>现在管用的学习率，后面可能失效</b>。",
 ],
 "exam": "⭐⭐ 选择题：「η=10 在表里最低，它是最佳学习率吗」（答<b>不是</b>，这只是单步结果）。扩展题：给这张表让你<b>解释它能说明什么、不能说明什么</b>——「能说明优化对步长敏感；不能说明泛化，因为没有留出数据，也不能确定普适最佳步长」。",
},

{"r": [6, 6], "t": "平均损失下降，会掩盖不均衡的进展", "star": 3,
 "one": "一次连续训练：平均 BCE 从 0.580352 降到 0.369420，但有一个正例始终停在 0.5 阈值以下，一直判错。",
 "quote": "<b>One continuous run</b>: four training examples, full-batch mean BCE and η = 0.1. Mean BCE: <b>0.580352 → 0.369420</b>. p([1,2]): 0.6615 → 0.9592. <b>p([−1,−2]): 0.4750 → 0.4859. The second remains below threshold 0.5.</b>",
 "eq": "更新次数    平均 BCE     p([1,2]) y=1    p([−1,−2]) y=1\n    0       0.580352      0.6615          0.4750\n    1       0.574996      0.6664          0.4749\n   10       0.527730      0.7158          0.4750\n   50       0.406138      0.8987          0.4788\n  100       0.369420      0.9592          0.4859   ← 仍 < 0.5，判成类 0",
 "pts": [
   "⚠️ <b>先把它和上一页区分开</b>：讲稿第一句就是 <em>This table follows <b>one uninterrupted run</b>, unlike the independent learning-rate comparisons.</em> —— 这一张是<b>一次不间断的训练</b>，上一张是<b>互相独立的对比</b>。两张表长得像，含义完全不同。",
   "<b>这里一次全批量更新 = 一个 epoch</b>：<em>One full-batch update equals one epoch here.</em> 所以 100 次更新就是 100 个 epoch。",
   "⭐⭐ <b>第二个正例为什么学不动</b>：讲稿给了机制——<em>After 100 updates its <b>two hidden ReLU activations are zero</b>, so its score depends on the <b>output bias</b>.</em> —— 它的两个隐藏 ReLU 激活都是 0，所以它的分数<b>只取决于输出偏置</b>，隐藏层那条路对它完全没用。",
   "⭐ <b>三种证据给的是不同的信息</b>：<em>Average loss, per-example probabilities and accuracy provide <b>different evidence</b>.</em> —— <b>平均损失、逐样本概率、准确率</b>是三种不同的证据，不能互相替代。",
   "⚠️⚠️ <b>最后那条限定三连</b>：<em>Stopping at a budget of 100 updates does not prove <b>convergence</b>, <b>global optimality</b> or <b>generalisation</b>.</em> —— 跑满 100 次就停，<b>既不证明收敛、也不证明全局最优、更不证明泛化</b>。",
 ],
 "exam": "⭐⭐⭐ <b>这是 T3 最锋利的一页</b>。扩展题问法：「平均损失一直在降，能说明模型变好了吗」——标准答法：<b>平均在降不代表每个样本都改善</b>，举这个例子（100 次更新后仍有一个正例 p = 0.4859 < 0.5 判错），再给机制（它的隐藏 ReLU 全为 0），最后加那三条限定。",
},

{"r": [7, 7], "t": "停止要用开发证据，固定预算不是收敛的证明", "star": 2,
 "one": "四步：按约定间隔监控 → 事先定好「改善」和 patience → 保留验证最好的检查点 → 冻结后再评测试集。",
 "quote": "<b>A fixed update budget is a stopping choice, not proof of convergence.</b> 1 Monitor: track training and validation at agreed intervals → 2 Choose a rule: <b>define improvement and patience before the final test</b> → 3 Keep a checkpoint: <b>retain the parameters with best validation evidence</b> → 4 Evaluate: freeze the procedure, then assess the held-out test set.",
 "pts": [
   "<b>patience 的定义</b>（讲稿给的）：<em>the number of validation checks without sufficient improvement that you allow before stopping</em> —— <b>允许连续多少次验证检查没有足够改善才停</b>。⚠️ 单位是「检查次数」，不是 epoch 数。",
   "⭐ <b>「改善」要自己定义</b>：<em>Specify <b>what metric and direction</b> define improvement.</em> —— <b>说清楚用哪个指标、往哪个方向算改善</b>（损失是越小越好，AUC 是越大越好）。",
   "⭐⭐ <b>保留最好的，不是最后的</b>：<em>Retain the <b>best validation checkpoint</b> rather than automatically the last step.</em> —— 这是早停最容易做错的一步：训练结束时的参数未必是验证表现最好的那一组。",
   "⚠️ <b>训练损失几乎不动，说明不了什么</b>：<em>Tiny training-loss changes can mean <b>stabilisation</b>, <b>a small learning rate</b> or <b>stalled optimisation</b>. They do not prove a global optimum.</em> —— 可能是稳定了、可能是步长太小、也可能是<b>卡住了</b>。",
   "⚠️⚠️ <b>一句硬规定</b>：<em><b>Never use the test set to choose the stopping time.</b></em>",
 ],
 "exam": "⭐ 考纲点名「基于验证集的早停」。标准答法四句：<b>定期在验证集上监控；事先定义改善与 patience；保留验证最好的检查点；测试集留到最后只评一次。</b>",
},

{"r": [8, 8], "t": "评估是一套纪律，不是一个指标", "star": 2,
 "one": "四步的顺序本身就是防止「结论过于乐观」的机制。",
 "quote": "<b>The order of decisions prevents optimistic conclusions.</b> 1 Define target: <b>positive class, costs and deployment population</b> → 2 Split safely: <b>stratify or group by the real sampling unit</b> → 3 Develop: fit and tune using training/validation only → 4 Evaluate once: <b>report test metrics, uncertainty and limitations</b>.",
 "pts": [
   "⭐ <b>第 1 步要定三样</b>，不只是正类：<b>正类是谁、两类错误的代价、部署时面对的人群</b>。后两样决定了你最后该选什么阈值、该报什么指标。",
   "<b>第 2 步的措辞很关键</b>：<em>stratify or group by <b>the real sampling unit</b></em> —— 按<b>真正的抽样单位</b>分层或分组。⚠️ 「真正的抽样单位」可能不是一行数据：同一个病人的 10 条记录，抽样单位是<b>病人</b>不是<b>记录</b>，所以要用分组划分。",
   "<b>第 4 步要报三样</b>：<em>test metrics, <b>uncertainty</b> and <b>limitations</b></em> —— 指标、<b>不确定性</b>、<b>局限</b>。⚠️ 只报一个数字是不完整的答案。",
   "⭐ <b>为什么顺序能防乐观</b>：因为每一步都把「做选择」关在测试集之前。顺序一乱（比如先看测试结果再定阈值），乐观偏差就进来了。",
 ],
 "exam": "⭐ 扩展题「说明如何选定并报告这个阈值」就照这四步答，重点在第 3、4 步：<b>用训练/验证做开发 → 冻结 → 在测试集上评估一次，并报告不确定性与局限</b>。",
},

{"r": [9, 9], "t": "没有上下文，指标会骗人：五个坑", "star": 3,
 "one": "泄漏 / 不平衡 / 阈值 / 抽样 / 漂移 —— 课件把它们并列成一张表，每一个都能单独出一道题。",
 "quote": "<b>Leakage</b> — Information crosses the intended split boundary. <b>Imbalance</b> — Accuracy can hide failure on a rare class. <b>Threshold</b> — Precision and recall change together. <b>Sampling</b> — Random rows may duplicate people, time or locations. <b>Shift</b> — Future data may differ from the evaluation distribution.",
 "pts": [
   "<b>① Leakage（泄漏）</b>：<em>Information crosses the intended split boundary</em>——<b>信息越过了你打算划的那条边界</b>。⚠️ 讲义强调：<b>不用标签也会泄漏</b>（训练值 [0,2] 均值是 1，把留出的 100 混进来算就变成 34，连训练数据的表示方式都被改了）。",
   "<b>② Imbalance（不平衡）</b>：<em>Accuracy can <b>hide failure on a rare class</b></em>——准确率会<b>掩盖在稀有类上的失败</b>。⭐ 极端例子：正例占 2%，全判负的准确率就有 98%，但 recall = 0。",
   "<b>③ Threshold（阈值）</b>：<em>Precision and recall <b>change together</b></em>——它们<b>一起变</b>。⚠️ 但方向不同：降阈值时 <b>recall 不会下降</b>，<b>precision 可升可降</b>。",
   "<b>④ Sampling（抽样）</b>：<em>Random rows may <b>duplicate people, time or locations</b></em>——随机按行划分，可能让<b>同一个人、同一时段、同一地点</b>的记录同时出现在训练和测试里。⇒ 这正是 p8 说的「按真正的抽样单位分组」。",
   "<b>⑤ Shift（漂移）</b>：<em>Future data may differ from the evaluation distribution</em>——<b>未来的数据可能和评估时的分布不一样</b>。⚠️ 这一条<b>任何划分都挡不住</b>，所以讲义说「划分给出的是估计，不保证分布漂移下的稳健性」。",
 ],
 "tbl": [{"cap": "五个坑 ↔ 它让哪个结论失效 ↔ 怎么防",
   "head": ["坑", "让什么失效", "怎么防"],
   "rows": [
     ["Leakage 泄漏", "整个留出估计都偏乐观", "先划分，预处理只在训练折内拟合"],
     ["Imbalance 不平衡", "accuracy 失去信息量", "和「全判多数类」基线比，看 precision/recall"],
     ["Threshold 阈值", "单个工作点的指标不代表模型", "在验证集上按代价选，选定后冻结"],
     ["Sampling 抽样", "测试集其实不是「新」样本", "按真正的抽样单位分组划分"],
     ["Shift 漂移", "部署后表现与评估时不同", "⚠ 划分防不住，只能说明局限"],
   ]}],
 "exam": "⭐⭐ <b>「这个评估流程有什么问题」型扩展题的素材库</b>。看到题目描述里出现「随机划分」「同一个病人」「准确率 95%」「在测试集上调阈值」，就对应到这五条里的某一条。",
},

]
