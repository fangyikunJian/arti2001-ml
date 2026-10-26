# -*- coding: utf-8 -*-
"""M3 T3《模型评估》逐页精读 —— 第 10–17 页（指标、Tutorial 与备考段）。

⚠⚠ p10 查出一处**官方材料内部的不一致**（见该条）：
    Canvas 讲义页把混淆矩阵写成「正类在前」[[TP,FN],[FP,TN]]，
    而这份**复习课件**写成「负类在前」[[TN,FP],[FN,TP]]（= sklearn 的顺序）。
    ⇒ 不能再说「本课考试按正类在前」。课件自己给的办法才是对的：**先读行列标签**。
"""

PART_B = [

{"r": [10, 10], "t": "⚠ 先建混淆矩阵再算指标（这一页有个必须知道的冲突）", "star": 3,
 "one": "先定正类 → 逐个观测归格 → 四格之和要等于样本数 → 才轮到算指标。",
 "quote": "<b>Rows are actual classes; columns are predicted classes. Fix the positive class first.</b><br>　　　　　　　Pred −　　Pred +<br>Actual −　　TN = 5　　FP = 2<br>Actual +　　FN = 1　　TP = 4<br><b>Check the total: 5 + 2 + 1 + 4 = 12 observations.</b> Accuracy = 9/12 = .75; Precision = 4/6 = .67; Recall = 4/5 = .80; F1 ≈ .73",
 "eq": "构造规则（课件右栏，逐格给的）：\n  TP = actual +, predicted +      FN = actual +, predicted −\n  FP = actual −, predicted +      TN = actual −, predicted −\n\n指标：\n  Accuracy  = (TP+TN)/总数   = (4+5)/12 = 0.75\n  Precision = TP/(TP+FP)     = 4/6 ≈ 0.667   ← 分母是「我预测为正的」\n  Recall    = TP/(TP+FN)     = 4/5 = 0.80    ← 分母是「真实为正的」\n  F1        = 2PR/(P+R) = 2TP/(2TP+FP+FN) = 8/11 ≈ 0.727",
 "pts": [
   "⚠️⚠️⚠️ <b>这一页和 Canvas 讲义页的摆法不一致，必须知道</b>：<br>· <b>Canvas 讲义页</b>（Accuracy, precision, recall 那一页）给的是<b>正类在前</b>：<code>[[TP, FN], [FP, TN]]</code>；<br>· <b>这份复习课件</b>给的是<b>负类在前</b>：<code>[[TN, FP], [FN, TP]]</code>——<b>和 sklearn 的 <code>labels=[0,1]</code> 输出顺序相同</b>。<br>⇒ <b>两份都是官方材料，顺序却相反。</b>",
   "⭐⭐ <b>所以不能背「本课固定某一种摆法」</b>。课件自己给的办法才是唯一安全的：<em>Rows are actual classes; columns are predicted classes. <b>Fix the positive class first.</b></em> ——<b>先定正类，再逐个读行列标签，按构造规则（actual ?, predicted ?）把每个格子认出来</b>。四个计数（TP=4, FN=1, FP=2, TN=5）在两种摆法下<b>完全相同</b>，变的只是位置。",
   "<b>讲稿把流程说得很死</b>：<em>Compare actual and predicted labels <b>one observation at a time</b> and place each case into <b>exactly one cell</b>.</em> 然后 <em><b>Only after this check</b> should metrics be calculated.</em> —— <b>先逐个归格、先做合计自查，再算指标。</b>",
   "⭐ <b>两个分母的「条件」说法要记</b>：<em>Precision <b>conditions on</b> predicted positives, 4/(4+2). Recall <b>conditions on</b> actual positives, 4/(4+1).</em> —— precision 的条件是「我预测为正的那一组」，recall 的条件是「真实为正的那一组」。<b>两组有重叠但不是同一组。</b>",
   "⚠️ <b>换正类，格子的名字就全变了</b>：<em>Changing the positive class changes the names of the cells and therefore precision and recall. <b>State the convention every time.</b></em> —— <b>每次都要声明约定。</b>",
 ],
 "tbl": [{"cap": "⚠ 三套摆法并列（计数相同，位置不同）",
   "head": ["来源", "摆法", "左上角是"],
   "rows": [
     ["Canvas 讲义页", "行=真实，列=预测，正类在前 ⇒ [[TP, FN], [FP, TN]]", "TP"],
     ["本复习课件（这一页）", "行=真实，列=预测，负类在前 ⇒ [[TN, FP], [FN, TP]]", "TN"],
     ["sklearn labels=[0,1]", "同上 ⇒ [[TN, FP], [FN, TP]]", "TN"],
     ["CS229 评估指标幻灯", "列=真实（和前面都转置）", "视定义而定"],
   ]}],
 "say": "⭐ <b>这个不一致其实是个送分点，只要你知道</b>：考场上拿到一张混淆矩阵，<b>第一件事是读轴标签</b>，第二件事是用构造规则逐格确认（「这个格子是 actual + 还是 actual −？predicted 是哪边？」）。这样无论题目用哪种排法你都不会填反。⚠️ <b>最危险的做法是背「左上角一定是 TP」</b>——在这份官方复习课件里，<b>左上角是 TN</b>。",
 "exam": "⭐⭐⭐ <b>必考，而且这是最可能因为「背错摆法」而整题全废的地方</b>。答题模板：<b>① 声明正类 → ② 读行列标签 → ③ 逐个观测归格 → ④ 四格之和 = 样本数（写出来） → ⑤ 套公式 → ⑥ 结合代价解释</b>。考纲官方示例大题给的数就是这个套路：TP=18, FP=12, FN=6, TN=164 ⇒ accuracy 0.91、precision 0.60、recall 0.75、F1 = 2/3 ≈ 0.667。",
 "tip": {"t": "F1 用计数版更稳", "v": "<b>F1 = 2TP/(2TP + FP + FN)</b>。好处是<b>避免先把 precision/recall 四舍五入再算</b>——本页例子用计数版得 8/11 ≈ 0.727，和 2PR/(P+R) 一致。⚠️ F1 <b>不含 TN</b>。", "w": 1},
},

{"r": [11, 11], "t": "Checkpoint：五个词自测", "star": 1,
 "one": "训练证据 / 验证决定 / 测试集 / 混淆矩阵 / ROC 点 —— 盖住右边先自己说。",
 "quote": "Training evidence — check progress across updates. Validation decisions — <b>choose settings, threshold and stopping</b>. Test set — estimate final generalisation. Confusion matrix — map TP, FP, FN, TN. <b>ROC point — FPR on x; TPR on y.</b>",
 "pts": [
   "⭐ <b>第二条把验证集管的三件事列全了</b>：<b>设置、阈值、停止点</b>。考试里问「这个决定该用哪部分数据做」，答案基本都落在这三样里。",
   "⚠️ <b>最后一条是送分也是陷阱</b>：<b>FPR 在横轴，TPR 在纵轴</b>。画反了整道题就废了。记法：<b>TPR 就是 recall，是「好事」，所以在上面（纵轴）</b>。",
   "<b>讲稿版本还多一条</b>：正文写「Training evidence」，讲稿里是 <em>Training set — fit model parameters</em>。两个版本合起来看更完整：<b>训练集拟合参数，训练证据看进展</b>。",
 ],
 "exam": "不出题，但<b>考前最后十分钟该看的一页</b>。特别是最后那条坐标轴方向。",
},

{"r": [12, 12], "t": "第 1 节收尾：五条要点 + 五条「上 Tutorial 之前先会」", "star": 2,
 "one": "右栏五条是评分点清单：写正类、逐格映射、分母对题、ROC 轴别画反、用代价解释阈值。",
 "quote": "<b>Key Takeaways</b>: Training loss can fall while some cases remain wrong · Choose settings and stopping with validation evidence · Keep test data separate from development · Precision and recall describe different errors · <b>AUC measures ranking, not calibration or error cost</b>.<br><b>Ready for the Tutorial</b>: <b>Write the positive class explicitly</b> · Map every confusion-matrix cell before calculating · <b>Keep denominators tied to the metric question</b> · <b>Plot ROC axes in the correct order</b> · Explain the threshold using error costs.",
 "pts": [
   "⭐⭐ <b>右栏那五条直接对应扣分点</b>，逐条拆：",
   "<b>① Write the positive class explicitly</b> —— <b>把正类显式写出来</b>。不是心里知道，是要写在答卷上。",
   "<b>② Map every confusion-matrix cell before calculating</b> —— <b>先把每个格子映射好再算</b>（呼应 p10 的「Only after this check」）。",
   "<b>③ Keep denominators tied to the metric question</b> —— <b>分母要和问题对应</b>：问「我说是正的时候对了多少」就用 TP+FP；问「真正的正例找到了多少」就用 TP+FN。",
   "<b>④ Plot ROC axes in the correct order</b> —— <b>ROC 的轴别画反</b>（FPR 横、TPR 纵）。",
   "<b>⑤ Explain the threshold using error costs</b> —— <b>用错误代价解释阈值</b>，不能只说「0.3 比 0.5 好」。",
   "⭐ <b>左栏第五条是 AUC 的边界</b>：<em>AUC measures <b>ranking</b>, not <b>calibration</b> or <b>error cost</b>.</em> 讲稿版本还多一个词：<em>not calibration or <b>business value</b></em>——<b>也不衡量业务价值</b>。",
 ],
 "exam": "⭐ 这五条每条都是独立的得分点。做完题自检一遍：<b>正类写了吗？格子映射写了吗？分母对题吗？轴画对了吗？阈值解释里提代价了吗？</b>",
},

{"r": [13, 13], "t": "第 2 节：Tutorial 三题（而且这份是要交的）", "star": 2,
 "one": "Q1 数据角色与训练证据、Q2 计数与指标与代价、Q3 从分数建 ROC 并估 AUC；extension 讲稀有正例与 PR。",
 "quote": "Three core questions connect <b>data splits → metrics → ROC/AUC</b>. Q1: data roles, training evidence and stopping · Q2: counts, metrics, baseline and validation error costs · Q3: build ROC points from scores, estimate AUC and discuss thresholds · Interpret metrics in the context of error costs · The optional extension considers <b>rare positives and precision–recall</b>.",
 "pts": [
   "⚠️⚠️ <b>讲稿交代了做法和评分</b>：<em>Work independently first, then revise your answers after the tutor's walkthrough and hand in Q1–Q3; <b>the final worksheet is marked</b>.</em> —— <b>先自己做，tutor 讲完之后修订，然后交 Q1–Q3；最终的 worksheet 是计分的</b>。⚠️ 这一点和 T2 不同（T2 的 extension 不计分，但这里说<b>最终 worksheet 要批改</b>）。",
   "⭐ <b>三题的链条很清楚</b>：<b>数据划分 → 指标 → ROC/AUC</b>。这也是 T3 扩展题最可能的三种形态。",
   "<b>讲稿把每题的考点说细了</b>：<br>· <b>Q1</b> 分配 train/validation/test 角色并<b>识别泄漏</b>；<br>· <b>Q2</b> 先<b>识别给定的计数</b>再算 precision/recall/F1；<br>· <b>Q3</b> 从打分的案例建 ROC 点（<b>包含一个平局</b>）、<b>用配对计数核对 AUC</b>、再对给定曲线估 AUC 并讨论阈值。",
   "⭐ <b>extension 的主题值得看一眼</b>：<em>rare positives and precision–recall</em>——<b>稀有正例与 precision–recall</b>。这正是讲义那个 1000 个里 10 个正例、recall 80% 但 precision 只有 7.5% 的算例。",
 ],
 "exam": "⭐ 考纲页点名「去哪儿找类似练习」时列的就是 <b>M3 T3 Tutorial Q1–3</b>：数据划分与诊断、混淆矩阵指标与错误代价、从分数得到 ROC 上的点与 AUC 阈值决策。<b>这三题就是扩展题的原型。</b>",
},

{"r": [14, 14], "t": "Q1：数据角色、泄漏、拟合诊断与停止", "star": 2,
 "one": "四步：算各子集大小并说明用途 → 指出哪些操作从留出数据里学了东西 → 对照基线诊断拟合 → 比较单步学习率证据并用验证来停。",
 "quote": "1 Split roles: calculate counts and explain each subset's purpose → 2 Leakage: <b>identify which operations learn from held-out data</b> → 3 Fit patterns: compare training and validation <b>with the benchmark</b> → 4 Rate and stopping: compare one-step evidence; <b>use validation to stop</b>.",
 "pts": [
   "⭐ <b>第 2 步的措辞是判据</b>：<em>identify which <b>operations learn from</b> held-out data</em> —— 找出<b>哪些操作从留出数据里「学」了东西</b>。⚠️ 关键词是 learn：缩放器、填补器、PCA 都在「学」参数，<b>即使不用标签</b>。",
   "⚠️⚠️ <b>讲稿给了两条「不要推出」</b>：<em><b>Do not infer a universal rate</b> or <b>correct predictions for every observation</b> from a lower mean loss.</em> —— 从更低的平均损失，<b>既不能推出普适的学习率，也不能推出每个观测都预测对了</b>。这两条正好对应 p5 和 p6。",
   "<b>第 3 步要「对照基线」</b>：<em>compare training and validation <b>with the benchmark</b></em>。⇒ 呼应 p3 那句「Similar scores can both be poor」——没有基线就判断不了「好」。",
   "<b>讲稿提到预处理的解释被合并进泄漏那一问</b>：<em>The preprocessing explanation is integrated into the leakage part to avoid duplication.</em> ⇒ 答泄漏时<b>要把预处理顺序一并写出来</b>（防泄漏五步）。",
 ],
 "exam": "⭐ 扩展题形态：给一个开发流程描述，问「这里有什么问题」。按 <b>① 指出哪一步越过了边界 ② 说明它学了什么 ③ 给出正确顺序（五步） ④ 加一句限定（划分只给估计，不保证泛化与漂移稳健性）</b> 作答。",
},

{"r": [15, 15], "t": "Q2：先把四个计数命名，再谈公式", "star": 3,
 "one": "公式只有在正类固定之后才可靠 —— 而且这一题还要算全判负的基线和两个阈值的验证代价。",
 "quote": "<b>Metric formulas are reliable only after the positive class is fixed.</b> P=TP/(TP+FP), R=TP/(TP+FN), F1=2PR/(P+R). <b>Precision conditions on predicted positive; recall conditions on actual positive.</b> Also compare <b>the all-negative baseline</b> and <b>validation error costs at the two thresholds</b>.",
 "eq": "代价比较（讲义算例）：漏一个次品代价 5，一次不必要检验代价 1\n    总代价 = 5·FN + 1·FP\n    阈值 0.5： FN=6, FP=4  ⇒ 5(6)+4 = 34\n    阈值 0.3： FN=2, FP=12 ⇒ 5(2)+12 = 22   ← 更优\n\n⚠ 代价改成相等： 6+4 = 10  vs  2+12 = 14   ← 结论翻转，0.5 更优",
 "pts": [
   "⭐ <b>三件事都要做，别漏</b>：① 三个指标；② <b>全判负的准确率基线</b>；③ <b>两个阈值的验证代价比较</b>。讲稿用了 <em>Also</em> 起头，说明后两样是容易漏掉的部分。",
   "<b>代价怎么算</b>：<em>Multiply each error count by its stated cost, then add.</em> —— <b>每类错误的计数乘它的代价，然后相加</b>。就这么简单，但必须把式子写出来。",
   "⚠️⚠️ <b>两条纪律</b>：① <em>Select the threshold using <b>validation</b> evidence; <b>do not consult the test results</b> to make this choice.</em>；② <em>The cost ratio describes <b>this exercise's priorities</b>, not a universal preference for precision or recall.</em> —— <b>这个代价比只属于这道题，不是「precision 比 recall 重要」的普遍结论</b>。",
   "<b>基线为什么重要</b>：正例稀少时「全判负」的准确率可能比模型还高。讲义那个 300 件产品的例子：模型 accuracy = 0.8267，而<b>全判非次品的基线是 0.8667</b>——<b>比模型还高</b>。",
   "⚠️ <b>F1 要和计数保持一致</b>：<em>Calculate F1 consistently with these counts.</em> ⇒ 用 <b>2TP/(2TP+FP+FN)</b> 最稳，避免中途四舍五入。",
 ],
 "exam": "⭐⭐⭐ <b>考纲官方示例大题就是这一题的形态</b>（TP=18, FP=12, FN=6, TN=164）。四问：算四个指标并写公式 / 解释为什么只看 accuracy 不够 / 降阈值的权衡 / 如何在不动测试集的前提下选阈值并评估。",
},

{"r": [16, 16], "t": "Q3：按阈值顺序建 ROC 点，再估 AUC", "star": 3,
 "one": "四步：按每个不同分数列出 (FPR, TPR)（平局一起进）→ 从严到松连起来 → 梯形求和 → 解释排序质量与代价。",
 "quote": "<b>As the threshold falls, both true and false positive rates can increase.</b> 1 Build: list (FPR, TPR) at each distinct score; <b>ties enter together</b> → 2 Connect: follow thresholds from strict to permissive → 3 Estimate AUC: <b>sum trapezoid areas</b> → 4 Interpret: ranking quality plus cost-based threshold choice.",
 "eq": "两个固定不变的分母： 真实正例数、真实负例数\n\n起点 (0,0) 全判负 → 阈值下降 → 终点 (1,1) 全判正\n    加入一个正例 ⇒ 点往上走      加入一个负例 ⇒ 点往右走\n    ⚠ 分数相同的观测必须一起加入 ⇒ 同时往上又往右 ⇒ **一段斜线**\n\n梯形法：  面积 = 宽 × (两个高的平均)\n    ⚠ 竖直段宽度为 0，面积为 0\n配对法：  AUC = P[随机正例分数 > 随机负例分数]，⭐ 平局算半胜",
 "pts": [
   "⭐⭐ <b>平局产生斜线，这是这一题的特色</b>：讲稿写明 <em>move tied cases together (<b>this gives a diagonal segment</b>)</em>。⚠️ 平局时 TP 和 FP 同时增加，所以点<b>同时往上和往右</b>，画出来是一条斜线而不是阶梯。",
   "<b>讲稿把 Q3 拆成两部分</b>：<b>前半</b>用六个打分案例自己建点（<em>Start with the six scored cases: fix the positive and negative totals</em>）；<b>后半</b>换一个分类器，<b>给定几个阈值</b>让你算梯形面积——<em>Q3 supplies the first two areas; calculate the remaining segments and <b>add all five</b>.</em> ⚠️ <b>题目给前两块面积，你算剩下的，最后五块全加起来。</b>",
   "⭐ <b>配对法是核对手段</b>：<em>Check the area by counting correctly ordered positive–negative pairs, <b>with a tie counting half</b>.</em> —— <b>数「正例分数高于负例」的配对数，平局算半个</b>。两种方法应当一致，考场上互相验算。",
   "<b>轴的方向再强调一次</b>：<em>place false-positive rate on the <b>horizontal</b> axis and true-positive rate on the <b>vertical</b> axis</em>。",
   "⚠️⚠️ <b>最后一句划清了 AUC 的边界</b>：<em>AUC describes ranking across thresholds. <b>An operating threshold still requires a decision about error costs and the intended setting.</b></em> —— <b>AUC 说的是跨阈值的排序；真正要用的那个阈值，仍然要靠错误代价和应用场景来定。</b>",
 ],
 "tbl": [{"cap": "讲义四样本算例（A 0.90 正 / B 0.80 负 / C 0.40 正 / D 0.10 负）",
   "head": ["阈值", "被判为正", "FPR", "TPR", "ROC 点"],
   "rows": [
     ["高于 0.90", "无", "0", "0", "(0, 0)"],
     ["0.85", "A", "0", "0.5", "(0, 0.5)"],
     ["0.60", "A, B", "0.5", "0.5", "(0.5, 0.5)"],
     ["0.30", "A, B, C", "0.5", "1", "(0.5, 1)"],
     ["0.05", "全部", "1", "1", "(1, 1)"],
   ]}],
 "say": "⭐ <b>那个四样本例子的 AUC 两种算法都给 0.75</b>：梯形 0.5×0.5 + 0.5×1 = 0.25 + 0.50 = <b>0.75</b>；配对 A&gt;B ✓、A&gt;D ✓、C&lt;B ✗、C&gt;D ✓ ⇒ <b>3 胜 / 4 对 = 0.75</b>。⚠️ 注意 FPR 没变化的那几段<b>宽度为 0，面积为 0</b>，别把它们算进去。",
 "exam": "⭐⭐⭐ <b>考纲点名「从分数得到 ROC 上的点、AUC 与阈值决策」</b>。扩展题标准结构：① 固定两个分母 ② 列出全部 ROC 点（<b>平局要一起加并说明产生斜线</b>） ③ 梯形算 AUC ④ <b>用配对法复核</b> ⑤ 讨论工作阈值要靠代价决定。⚠️ 第 ④ 步写出来是加分项。",
},

{"r": [17, 17], "t": "第 3 节：复习与备考（时间和材料都在这一页）", "star": 2,
 "one": "T3 没有排定的 practical；两个 notebook 选做；Week 12 复习，Week 13（11 月 9–15 日）考试。",
 "quote": "<b>No scheduled coding practical in Topic 3.</b> Optional: M3 T1 notebook Q3 explores learning rates · Optional: M3 T3 notebook practises evaluation · <b>Week 12: review and revision</b> · <b>Week 13 (9–15 November): Module 3 test</b> · <b>Confirm your session and permitted materials on Canvas.</b>",
 "pts": [
   "⚠️ <b>T3 和 T1/T2 不一样：没有排定的 practical</b>。两个 notebook 都是 <em>ungraded self-study, with worked solutions for review</em>——<b>不计分的自学材料，但有参考答案</b>。",
   "⭐ <b>两个 notebook 各练什么（讲稿写明）</b>：<b>M3 T1 notebook 的 Q3</b> 练<b>学习率实验</b>（正好对应 p5）；<b>M3 T3 notebook</b> 练<b>泄漏防范、指标、验证选择与阈值代价</b>（对应 p4、p10、p15）。",
   "<b>Tutorial 仍然按时在课上进行</b>：<em>The tutorial remains scheduled in class.</em>",
   "⚠️⚠️ <b>最后那句是行动项，别忽略</b>：<em>Confirm <b>your session</b> and <b>permitted materials</b> on Canvas.</em> —— <b>到 Canvas 上确认你自己那一场的时间，以及允许带什么材料</b>。考纲页说的是普通非编程非图形科学计算器 + 任意印刷或手写材料，但<b>以你那一场的公告为准</b>。",
 ],
 "tbl": [{"cap": "M3 测验的硬信息（考纲页 + 本页）",
   "head": ["项", "内容"],
   "rows": [
     ["时间", "Week 13，2026 年 11 月 9–15 日，在排定的 assessment / practical 课时"],
     ["时长与分值", "110 分钟 · 100 分"],
     ["题型", "Q1–Q20 单选每题 3 分；Q21–Q24 扩展题每题 10 分"],
     ["资料", "开卷：任意印刷或手写笔记；考试期间不得互相传阅"],
     ["计算器", "普通非编程、非图形科学计算器"],
     ["⚠ 提醒", "Canvas 的 due-date 字段是空的，<b>不代表考试没排</b>；自己确认场次"],
   ]}],
 "exam": "这一页不出题，但<b>它是行动清单</b>：① 去 Canvas 确认自己那一场；② 把两个选做 notebook 至少看一遍参考答案；③ Week 12 是官方给的复习周，别排别的事。",
 "tip": {"t": "三讲读完之后", "v": "T1 讲一个神经元走完整条链，T2 把链加宽到隐藏层与批量，T3 退后一步问「凭什么可信」。⭐ 接下来直接用 <b>《M3 备考包》</b>（速查表 + 答题模板 + 整卷模拟）和 <b>《M3 考前框架走查》</b>（考试当天早上 50 分钟）收口。", "w": 0},
},

]
