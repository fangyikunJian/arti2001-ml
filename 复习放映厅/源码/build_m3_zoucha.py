# -*- coding: utf-8 -*-
"""M3 考前框架走查。样式复用 M2 那份（★M2考前框架走查.html）的 <style> 块，保证视觉一致。

内容来自 M3 的 11 份 Canvas 讲义整理 ＋ Module 3 Assessment 页；
出现的数字都在 `M3材料/笔记与阅读/_src/verify_m3.py` 里复算过（165/165 通过）。

⚠ 这份是**框架**不是速查表 —— 公式细节看《M3 备考包》。
   做它的理由：用户反馈过「都是细节，却不知道在说什么」，
   所以这一页只负责把三个 Topic 锁成一根主线。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HALL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HALL, "★M2考前框架走查.html")
OUT = os.path.join(HALL, "★M3考前框架走查.html")

src = io.open(SRC, encoding="utf-8").read()
head = src[:src.index("</style>") + len("</style>")]
head = head.replace("<title>M2 考前框架走查</title>", "<title>M3 考前框架走查</title>")
assert "<title>M3 考前框架走查</title>" in head, "标题没换成功"

BODY = r"""
<div class="controls">
  <button id="themeBtn">☾ 暗色</button>
  <button onclick="window.print()">🖨 打印</button>
</div>

<div class="wrap">
<header>
  <h1>M3 考前框架走查 <span class="tag">开卷 · 110 分钟 · 20 选×3 + 4 大题×10 = 100 分</span></h1>
  <p class="sub">睡醒后 <b>~50 分钟</b>走一遍这张图，把 T1–T3 锁成<b>一根主线</b>。这是框架不是速查表——公式细节看备考包。<b>Week 13（11 月 9–15 日），在你排定的 assessment / practical 时段。</b>⚠ Canvas 的 due-date 字段是空的，页面写明「空的截止日期不代表考试没排」。</p>
</header>

<h2>整个 M3 就一条链</h2>
<div class="flow">
  <div class="node"><b>前向</b>：用当前参数算出预测</div><div class="arw">→</div>
  <div class="node"><b>损失</b>：和目标比，得一个数</div><div class="arw">→</div>
  <div class="node"><b>反向</b>：算每个参数的梯度</div><div class="arw">→</div>
  <div class="node"><b>更新</b>：优化器改参数</div><div class="arw">→</div>
  <div class="node"><b>评估</b>：用留出证据判断</div>
</div>
<div class="thread">
  <b>三个 Topic 不是三个话题，是同一条链被切成三段。</b>
  <b>T1</b> 让<b>一个</b>神经元把这条链从头走到尾（所以 T1 的算例最完整）；
  <b>T2</b> 把链<b>加宽</b>——多了隐藏层、多种激活与损失、一次处理一批；
  <b>T3</b> 退后一步问：<b>这条链产生的结果，凭什么可信</b>。<br>
  ⭐ 所以每道大题的套路都一样：<b>先把数算对，再说这串数说明了什么、不说明什么。</b>
  官方评分口径原话：<b>A correct final number alone may not demonstrate the required understanding.</b>
</div>

<h2>三个主题 · 各记 4–5 条 + 头号陷阱</h2>
<div class="grid">

  <div class="tcard t1">
    <h3>T1 · 神经网络基础 <span class="code">走完整条链</span></h3>
    <p class="role">一个神经元 + sigmoid + BCE，<b>所有公式都在这一课定型</b></p>
    <ul>
      <li>前向 <span class="fml">z = Σwᵢxᵢ + b</span>，<span class="fml">p = σ(z)</span>。<b>此刻还没有学习发生</b>——参数没变，<b>目标 y 也还没被用到</b></li>
      <li>损失用<b>概率</b>不用阈值后的类别：y=1 ⇒ <span class="fml">L = −log p</span>。<b>p=0.75 和 p=0.90 判类相同，但损失不同——这就是阈值之外多出来的信号</b></li>
      <li><b>δ = ∂L/∂z = p − y</b>（sigmoid+BCE 专属化简），再往回 <span class="fml">∂L/∂wᵢ = δ·xᵢ</span>、<span class="fml">∂L/∂b = δ</span></li>
      <li>更新 <span class="fml">θ ← θ − η·∂L/∂θ</span>。<b>全部梯度用更新前的原参数算完，再一起更新</b></li>
      <li>计算图：<b>一条路径内部相乘，多条路径汇合相加</b>。官方小例 q→r=2q、q→t=3q、F=r+t ⇒ <b>dF/dq = 5</b>（只算一支得 2，漏了）</li>
    </ul>
    <div class="trap"><b>头号陷阱：</b>「sigmoid 是非线性的，边界应该是曲线」——<b>错</b>。阈值 0.5 对应 <b>z = 0</b>，两个输入时那是<b>一条直线</b>。而且限制来自<b>「仿射分数 + 单调激活 + 固定阈值」这个组合</b>，<b>不是单纯因为只有一个神经元</b>——多个仿射层叠在 sigmoid 前面，直边界照旧。所以异或型数据<b>再训练多久也分不开</b>，「再 train 久一点」是错误选项。</div>
  </div>

  <div class="tcard t2">
    <h3>T2 · 训练神经网络 <span class="code">把链加宽</span></h3>
    <p class="role">激活怎么选、损失怎么配、隐藏层怎么拿到梯度</p>
    <ul>
      <li><b>输出值和导数是两件事</b>：a 往前传，g′(z) 在反向<b>乘</b>在传回的梯度上。<b>大的输出不代表大的梯度</b></li>
      <li>导数要会默写：<b>σ′ = σ(1−σ)</b>、<b>tanh′ = 1 − tanh²</b>、ReLU′ = 0/1。<b>本课约定 ReLU′(0) = 0、Leaky′(0) = α = 0.01</b></li>
      <li>配对：回归→线性+MSE/MAE；二分类→sigmoid+BCE；<b>互斥多类→softmax+CCE</b>；<b>多标签→每标签一个 sigmoid+BCE</b>（和不必为 1）。<b>整数标签用 sparse 版</b></li>
      <li>隐藏层梯度四步：<b>(p−y) → ×输出权重 vⱼ → ×g′(zⱼ) → ×xᵢ</b>。上层权重会出现在下层梯度里，因为<b>影响必须穿过输出层</b></li>
      <li>batch = 算一次更新用的那组观测；epoch = 过完一遍训练集。<b>100 个 / 批 20 ⇒ 1 epoch = 5 次更新</b>。平均损失的 <b>1/N 只除一次</b></li>
    </ul>
    <div class="trap"><b>头号陷阱：</b>某个隐藏 ReLU 对这个观测<b>不激活</b>时，<b>它的输入权重梯度全是 0，这一步整个单元不动</b>；同时 <b>h=0 的那个输出权重梯度 = (p−y)·0 = 0，也不动</b>。考场上漏掉这两处「没变」直接丢分。⚠ 但<b>「这个样本上输出 0」≠「这个单元死了」</b>——要在相关的那批输入上<b>一直</b>不激活才叫死亡 ReLU。</div>
  </div>

  <div class="tcard t3">
    <h3>T3 · 模型评估 <span class="code">凭什么可信</span></h3>
    <p class="role">划分 → 不泄漏 → 诊断 → 选阈值 → 只评估一次</p>
    <ul>
      <li>三角色：<b>训练=拟合（含缩放与填补参数）</b>、<b>验证=一切选择（含阈值与停止点）</b>、<b>测试=评估冻结的流程，一次</b></li>
      <li>防泄漏五步：<b>先划分 → 只在训练集上算预处理参数 → 原样应用 → 用验证选 → 测试评一次</b>。⚠ <b>不用标签也会泄漏</b>（[0,2] 均值 1，混入 100 就变 34）</li>
      <li>划分方式要复现「新数据怎么来」：不平衡→<b>分层</b>；同源记录→<b>分组</b>；预测未来→<b>按时间</b>。<b>随机划分不是自动合适的</b></li>
      <li>指标：precision 分母 <b>TP+FP</b>，recall 分母 <b>TP+FN</b>，<b>F1 = 2TP/(2TP+FP+FN)，不含 TN</b>。<b>先声明哪一类是正类</b></li>
      <li>ROC：两个分母固定，<b>加正例往上、加负例往右</b>；AUC 两种算法（梯形 / <b>正负配对，平局半胜</b>）<b>互相验算</b></li>
    </ul>
    <div class="trap"><b>头号陷阱：</b>正例稀少时 <b>accuracy 和 AUC 都会骗人</b>。1000 个里只有 10 个正例、TPR=0.8、FPR=0.1 ⇒ <b>FP = 0.1×990 = 99</b> ⇒ <b>recall 80% 但 precision 只有 8/107 ≈ 7.5%</b>。原因是<b>两者分母完全不同</b>。⚠ <b>单独改变 prevalence 不一定改变 AUC，但 precision 可能天翻地覆</b>——所以要同时看 precision–recall 和 prevalence。</div>
  </div>

  <div class="tcard t4">
    <h3>贯穿三块 · 算完之后说什么 <span class="code">M3 的主线</span></h3>
    <p class="role">这一栏是大题后半段的全部分数</p>
    <ul>
      <li><b>① 这个数说明了什么</b>：概率朝目标移动 / 损失下降 / 某条路径梯度为零</li>
      <li><b>② 机制是什么</b>：是哪个局部导数、哪条路径、哪个分母在起作用</li>
      <li><b>③ 它没有说明什么</b>：<b>单样本的改进不是泛化的证据</b>；<b>诊断模式不是证明</b>；<b>排序好不等于校准好</b></li>
      <li><b>④ 该怎么做才算规范</b>：用验证证据选、冻结、在没碰过的测试集上评估一次</li>
    </ul>
    <div class="trap"><b>用法：</b>任何一道大题，前半段把数算对拿基础分，<b>后半段逐条扫这四项</b>。⚠ <b>只写最终数字，官方明说「可能不足以体现所需的理解」。</b></div>
  </div>

</div>

<h2>★ 4 道大题的命根子：答题四步</h2>
<div class="rubric">
  <div class="steps">
    <div class="s"><b>①</b> 报结果</div><div class="a">→</div>
    <div class="s"><b>②</b> 解释机制</div><div class="a">→</div>
    <div class="s"><b>③</b> 给证据</div><div class="a">→</div>
    <div class="s"><b>④</b> 说出局限</div>
  </div>
  <p style="margin:10px 0 4px"><b>大多数人停在第①步，那最多拿一半分。</b>第④步的句子直接从下表挑一句抄上去：</p>
  <div class="swap"><table>
    <thead><tr><th>你报了什么</th><th>就补这一句局限</th></tr></thead>
    <tbody>
      <tr><td>一次更新后损失下降</td><td>只证明<b>在这一个训练样本上</b>有改进，<b>不是泛化的证据</b>；要再走一步必须<b>重新跑前向、重新算梯度</b></td></tr>
      <tr><td>某个参数的梯度更大</td><td>只反映<b>那个输入的数值更大</b>，<b>不构成「这个特征更重要」的排序</b></td></tr>
      <tr><td>某个隐藏单元梯度为 0</td><td>只说明它<b>对这个观测不激活</b>，<b>不等于这个单元死了</b></td></tr>
      <tr><td>训练损失一直在降</td><td>只说明<b>在拟合训练目标</b>，<b>不说明能预测没见过的数据</b></td></tr>
      <tr><td>某个学习率一步后损失最低</td><td>只是<b>单步</b>结果，<b>一步走得远不等于长期收敛得好</b>；也只属于这个批次和这个起点</td></tr>
      <tr><td>平均损失下降了</td><td><b>不代表每个样本都被正确分类</b>——讲义算例里跑完 100 次更新，仍有一个正例停在 0.4859</td></tr>
      <tr><td>训练强、验证差</td><td><b>可能</b>过拟合；<b>在归因于方差之前还要检查分布差异、验证样本过小、以及泄漏</b></td></tr>
      <tr><td>一个划分给出的分数</td><td>是对未见数据表现的<b>估计</b>；<b>不保证泛化，也不保证分布漂移下的稳健性</b></td></tr>
      <tr><td>五折交叉验证的平均</td><td><b>不是五次独立实验</b>（训练集互相重叠），仍依赖抽样与划分假设</td></tr>
      <tr><td>很高的 accuracy</td><td>可能被<b>大量负例主导</b>；要和<b>「全判多数类」的基线</b>比，并说明两类错误的代价</td></tr>
      <tr><td>一个 AUC 数值</td><td>概括的是<b>整条曲线的排序能力</b>，<b>不决定阈值、不衡量校准、不编码代价</b>；AUC=1 只说明<b>在这个样本上</b>排序完美</td></tr>
      <tr><td>选定了某个阈值</td><td>依赖<b>代价假设</b>；<b>代价一变结论可能翻转，不存在普适最优的阈值</b></td></tr>
    </tbody>
  </table></div>
</div>

<h2>三个必背算例（手算大题的原型）</h2>
<div class="swap"><table>
  <thead><tr><th>题型</th><th>给定</th><th>过程</th><th>答案</th></tr></thead>
  <tbody>
    <tr><td>单神经元<br>一次更新</td><td>x=[1,2]，y=1，w=[0.2,0.4]，b=0.1，η=0.1</td>
        <td>z=1.1 → p=0.750260 → L=0.287335<br>δ = p−y = −0.249740<br>梯度 −0.249740 / <b>−0.499480</b> / −0.249740</td>
        <td><b>w→0.224974, 0.449948；b→0.124974</b><br>复查 z=1.249844，<b>p=0.777273，L=0.251964</b></td></tr>
    <tr><td>隐藏层<br>一个权重</td><td>隐1 [0.2,0.4] b 0.1 · 隐2 [−0.5,0.3] b −0.2 · 输出 [0.7,−0.4] c −0.1，x=[1,2]，y=1，η=0.1</td>
        <td>z₁=1.1⇒h₁=1.1；<b>z₂=−0.1⇒h₂=0</b><br>s=0.67，p=0.661503<br>四步：−0.338497 → ×0.7 → ×1 → ×2</td>
        <td><b>∂L/∂w₁₂ = −0.473896 ⇒ w₁₂→0.447390</b><br>一步后 <b>p=0.700487，L=0.355979</b><br><b>隐2 与输出的 −0.4 完全不动</b></td></tr>
    <tr><td>TensorFlow<br>那个例子</td><td>w=1.5，b=−1.0，输入 2.0，ReLU，loss=0.5(a−5)²，η=0.05</td>
        <td>z=2 ⇒ a=2 ⇒ <b>loss=4.5</b><br>∂loss/∂a = a−5 = −3，ReLU 倍数 1</td>
        <td><b>g_w=−6，g_b=−3 ⇒ w→1.8，b→−0.85</b><br>重新前向 z=2.75 ⇒ <b>loss=2.53125</b></td></tr>
    <tr><td>混淆矩阵<br>四指标</td><td>TP=18, FP=12, FN=6, TN=164（考纲示例）</td>
        <td>先声明正类；自查 18+12+6+164=200</td>
        <td><b>acc=0.91，precision=0.60<br>recall=0.75，F1=2/3≈0.667</b></td></tr>
    <tr><td>ROC 与 AUC</td><td>A(0.90,1) B(0.80,0) C(0.40,1) D(0.10,0)</td>
        <td>点 (0,0)→(0,0.5)→(0.5,0.5)→(0.5,1)→(1,1)<br>梯形 0.25+0.50；配对 3 胜/4 对</td>
        <td><b>AUC = 0.75</b>（两法一致）<br>⚠ <b>竖直段面积为 0</b></td></tr>
  </tbody>
</table></div>

<h2>全 M3 高频陷阱清单（考前扫一眼）</h2>
<div class="traps">
  <div class="t"><b>把激活输出 a 当成参数。</b><span class="ok">参数只有权重和偏置</span>；a、z 是每个样本现算的中间值。</div>
  <div class="t"><b>以为前向传播里用到了 y。</b><span class="ok">没有</span>——y 是后面算损失时才用来评判这个预测的。</div>
  <div class="t"><b>先把 p 四舍五入成类别再取对数。</b><span class="ok">BCE 用概率本身</span>，否则连续的学习信号就没了。</div>
  <div class="t"><b>算一个参数就更新一个。</b><span class="ok">全部梯度用同一个（更新前）状态算完，再一起更新。</span></div>
  <div class="t"><b>把 1−g² 当成 sigmoid 的导数。</b><span class="ok">1−g² 是 tanh；sigmoid 是 g(1−g)。</span></div>
  <div class="t"><b>ReLU′(0) 填 1。</b><span class="ok">本课约定 0</span>；Leaky ReLU 在 0 处是 α = 0.01。</div>
  <div class="t"><b>看到 Leaky ReLU 输出 −0.02 就以为导数是负的。</b><span class="ok">导数是 +0.01</span>——输出的符号和斜率的符号是两回事。</div>
  <div class="t"><b>把梯度消失全归给激活函数。</b><span class="ok">真实梯度还包含权重与多条路径的求和</span>，激活斜率只是一个成因。</div>
  <div class="t"><b>多标签任务用 softmax。</b><span class="ok">多标签是每个标签一个 sigmoid</span>，各自输出不必加起来等于 1。</div>
  <div class="t"><b>用 from_logits 的损失时又套了一次激活。</b><span class="ok">这类实现内部已经做了 sigmoid / softmax。</span></div>
  <div class="t"><b>把 ∂ℓ/∂p 和 ∂ℓ/∂z 混用。</b><span class="ok">p − y 是对 logit 的导数</span>，已经含了 sigmoid 的链式因子。</div>
  <div class="t"><b>平均损失在每一层又除一次 N。</b><span class="ok">1/N 只除一次。</span></div>
  <div class="t"><b>以为 tape.gradient 会更新参数。</b><span class="ok">assign_sub 才更新</span>；tape 只记录与求导。</div>
  <div class="t"><b>以为自动微分能保证模型好。</b><span class="ok">它不替你选目标、不修数据泄漏、不保证学习率合适。</span></div>
  <div class="t"><b>划分之前对全部数据做缩放或 PCA。</b><span class="ok">只在训练折内部拟合</span>——不用标签一样会泄漏。</div>
  <div class="t"><b>同一个人的记录分散进训练和测试。</b><span class="ok">用分组划分</span>，否则测得的不是「对新病人的表现」。</div>
  <div class="t"><b>在测试集上挑阈值或挑模型。</b><span class="ok">用验证集</span>；测试集只评估一次冻结的流程。</div>
  <div class="t"><b>看过测试结果后又继续开发。</b><span class="ok">那个测试集已成为开发历史的一部分</span>，新结论需要一次全新的独立评估。</div>
  <div class="t"><b>「训练强验证差 ⇒ 方差高」一口咬定。</b><span class="ok">先排除分布差异、验证集过小、泄漏。</span></div>
  <div class="t"><b>背死了「混淆矩阵左上角是 TP」。</b><span class="ok">先定正类再逐格读行列标签</span>——⚠ <b>Canvas 讲义页左上角是 TP，而 M3 T3 复习课件左上角是 TN</b>（同 sklearn）。两份都是官方材料，顺序相反，计数却相同。</div>
  <div class="t"><b>把 F1 里的 P 当成概率。</b><span class="ok">P 是 precision</span>，R 是 recall。</div>
  <div class="t"><b>以为降低阈值 precision 一定变好。</b><span class="ok">recall 不会下降，precision 可升可降。</span></div>
  <div class="t"><b>用 AUC 回答「该用哪个阈值」。</b><span class="ok">AUC 不决定阈值、不衡量校准、不编码代价。</span></div>
  <div class="t"><b>AUC &lt; 0.5 就把预测反过来用。</b><span class="ok">先检查分数方向、标签约定和抽样。</span></div>
  <div class="t"><b>只写最终数字。</b><span class="ok">官方：只给正确数字可能不足以体现所需的理解。</span></div>
</div>

<h2>睡醒 50 分钟 · 走查顺序</h2>
<ol class="plan">
  <li><span class="min">5 分钟</span> 看一遍<b>最上面那条链</b>和它下面那段话。把「三个 Topic 是同一条链的三段」这句话在心里复述一遍。</li>
  <li><span class="min">12 分钟</span> 三张主题卡<b>各读两遍</b>：第一遍读条目，第二遍只读<b>头号陷阱</b>。读完合上页面，口头说出每个 Topic 的一句话定位。</li>
  <li><span class="min">10 分钟</span> 把<b>三个必背算例</b>的「过程」列遮住，只看「给定」，在草稿纸上<b>把答案推出来</b>。推不动的那一行，立刻翻备考包对应小节。</li>
  <li><span class="min">8 分钟</span> 读<b>答题四步</b>和那张「局限句」表。挑出<b>你最可能用到的三句</b>，抄到速查表首页。</li>
  <li><span class="min">10 分钟</span> 扫<b>陷阱清单</b>。每条问自己「我上次做题时踩过吗」，踩过的打勾，勾出来的回头再看一遍。</li>
  <li><span class="min">5 分钟</span> 最后确认考试设定：<b>110 分钟、100 分、20 选×3 + 4 大题×10、开卷、非编程非图形计算器</b>。按分值分配时间：<b>选择 30 分钟 / 大题 60 分钟 / 检查 20 分钟</b>。</li>
</ol>

<div class="foot">
  <b>这一页不覆盖什么。</b>公式表、激活函数数值表、输出–损失配对表、英文句库、四套答题模板、整卷模拟，
  都在<b>《M3 备考包 · 速查表与模拟卷》</b>里；逐节的讲义整理与 205 道题在
  <b><code>M3材料/笔记与阅读/</code></b> 那七册 PDF 里。<br>
  <b>数字来源。</b>这一页出现的每个数都取自 Canvas 讲义的官方算例，
  并用 numpy 逐个复算过（<code>M3材料/笔记与阅读/_src/verify_m3.py</code>，165/165 通过）。
</div>

</div>

<script>
(function(){
  var KEY="mlreader-theme", root=document.documentElement, btn=document.getElementById("themeBtn");
  function apply(t){ root.setAttribute("data-theme",t);
    if(btn) btn.textContent = (t==="dark" ? "☀ 浅色" : "☾ 暗色"); }
  var saved; try{ saved=localStorage.getItem(KEY); }catch(e){}
  apply(saved==="dark" ? "dark" : "light");
  if(btn) btn.addEventListener("click", function(){
    var next = root.getAttribute("data-theme")==="dark" ? "light" : "dark";
    apply(next); try{ localStorage.setItem(KEY,next); }catch(e){}
  });
})();
</script>
"""

io.open(OUT, "w", encoding="utf-8").write(head + BODY)
print("%s：%d 字符" % (os.path.basename(OUT), len(head + BODY)))
print("  复用 M2 样式 %d 字符；正文 %d 字符" % (len(head), len(BODY)))
_tbl = re.findall(r"<tbody>(.*?)</tbody>", BODY, re.S)      # [0] 局限句表 [1] 算例表
print("  主题卡 %d　陷阱条目 %d　局限句 %d　算例 %d　走查步骤 %d"
      % (BODY.count('class="tcard'), BODY.count('<div class="t">'),
         _tbl[0].count("<tr>"), _tbl[1].count("<tr>"),
         BODY.count('<li><span class="min">')))
