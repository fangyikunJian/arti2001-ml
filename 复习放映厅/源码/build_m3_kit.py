# -*- coding: utf-8 -*-
"""生成《M3 备考包 · 速查表与模拟卷》。

和 M2 那份同一套版式 —— ⚠ CSS 不复制一份，而是**构建时从 M2 备考包里读出来**，
这样两份永远一致（M2 那份改了配色，这份跟着变）。

内容来源：M3 的 11 份 Canvas 讲义整理 ＋ Module 3 Assessment 页。
模拟卷的题目全部是**新编的**（不和三份题库重复），数字另有 verify_m3_kit.py 复算。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HALL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M2KIT = os.path.join(HALL, "M2备考包-速查表与模拟卷.html")
OUT = os.path.join(HALL, "M3备考包-速查表与模拟卷.html")

css = io.open(M2KIT, encoding="utf-8").read()
css = css[css.find("<style>"):css.find("</style>") + len("</style>")]
assert len(css) > 6000, "CSS 没读全"

B = []
A = B.append


def mcq(n, stem, opts, ans, why):
    """一道选择题。答案放在 <details> 里，考完再开。"""
    ol = "".join("<li>%s</li>" % o for o in opts)
    return ('<div class="q"><div class="stem"><span class="n">%d</span>%s</div>'
            '<ol type="A">%s</ol>'
            '<details><summary>答案</summary><p><b>%s</b> —— %s</p></details></div>'
            % (n, stem, ol, ans, why))


# ═════════════════════ 头部 ═════════════════════
A('''<h1>Module 3 <span>备考包</span></h1>
<div class="sub">神经网络 · 训练 · 评估 —— 速查表 · 答题模板 · 整卷模拟</div>

<div class="box y">
  <div class="h">这份包怎么用</div>
  <p><b>考试是开卷的</b>，所以决定分数的不是「记得多少」，而是<b>在 110 分钟里翻不翻得到</b>。
  用法：<span class="k">① 速查表打印出来</span>，按 T1/T2/T3 三栏贴标签；
  <span class="k">② 答题模板背成条件反射</span>，四类大题各一套句式；
  <span class="k">③ 模拟卷限时做一遍</span>，做完再看答案。</p>
  <p class="lead" style="margin-bottom:0">考试：<b>Week 13（11 月 9–15 日）</b>的 assessment / practical 课时 ·
  <b>110 分钟、100 分</b> · 20 选择 ×3 分 + 4 大题 ×10 分 · 开卷、可带任意印刷或手写材料 ·
  只能用普通<b>非编程非图形</b>科学计算器。⚠ Canvas 的 due-date 字段是空的，
  页面写明「<b>空的截止日期不代表考试没排</b>」—— 具体时间看 course roadmap 和自己的课表。</p>
</div>''')

# ═════════════════════ 计划 ═════════════════════
A('''<h2 id="plan">三周计划 <em>不绑日历，按块推进</em></h2>
<p class="lead">离考试约三周。下面按「块」排，可以一天一块也可以两天一块 —— 但<b>顺序别换</b>，
后面的块依赖前面的。⚠ 三份 Tutorial 在 Canvas 上按周解锁（T2 10-18、T1 10-19、T3 10-25），
所以第 ④ 块要往后排。</p>

<table>
<tr><th style="width:74px">块</th><th>做什么</th><th>产出</th></tr>
<tr><td><b>① 立记号</b></td>
    <td>读 <code>M3材料/笔记与阅读/M3_总目录.pdf</code> 和 T1 册最前面的<b>记号表</b>。
    把 <b>w<sub>ji</sub> 的下标读法</b>、<b>ℓ 与 L</b>、<b>δ 与 Δ</b> 三件事记死。</td>
    <td>后面所有公式不会读错</td></tr>
<tr><td><b>② 通读</b></td>
    <td>按 <b>T1 → T2 → T3</b> 走完三册知识点整理（21 / 27 / 22 页）。不懂的标记，不停下来。</td>
    <td>错题本里自动攒出薄弱小节</td></tr>
<tr><td><b>③ 手算</b></td>
    <td><b>三类手算各练三遍</b>（换数字）：<span class="k">单神经元一次更新</span> /
    <span class="k">隐藏层一个权重的梯度</span> / <span class="k">混淆矩阵四指标 + ROC 点与 AUC</span>。
    每一遍都把中间步骤写全。</td>
    <td>三类都能 10 分钟内做完</td></tr>
<tr><td><b>④ 三份 Tutorial</b></td>
    <td>解锁后<b>盖住答案先做一遍</b>。官方点名：T1 Q1–3 前向/BCE/去掉 ReLU；
    T2 Q1–3 激活与输出选择、各类损失的 logit 梯度、一个隐藏层权重的梯度 + 自动微分 + batch/epoch 计数；
    T3 Q1–3 数据划分与诊断、混淆矩阵与错误代价、ROC 点与 AUC。</td>
    <td>官方题型全过一遍</td></tr>
<tr><td><b>⑤ 做题库</b></td>
    <td>三册题库共 <b>205 道</b>，每组 5 题，遮住解析作答。做错的回到对应小节。</td>
    <td>概念题的分稳住</td></tr>
<tr><td><b>⑥ 写作</b></td>
    <td>练<b>答题四步</b>：报结果 → 解释机制 → 给证据 → 说局限。拿本包四套模板各写两道。
    ⚠ 官方原话：<b>只给出正确的最终数字，可能不足以体现所需的理解。</b></td>
    <td>大题不再只写数字</td></tr>
<tr><td><b>⑦ 模拟</b></td>
    <td>本包模拟卷，<b>严格计时 110 分钟</b>，只带你打印的速查表。做完批改，统计哪一类丢分最多。</td>
    <td>知道自己的实际配速</td></tr>
<tr><td><b>⑧ 定稿</b></td>
    <td>按模拟暴露的问题改速查表，<b>打印定稿</b>，贴索引标签。考前只看速查表和陷阱清单。</td>
    <td>带进考场的那一叠</td></tr>
</table>''')

# ═════════════════════ 配速 ═════════════════════
A('''<h2 id="pace">考场配速与开卷打法</h2>
<div class="grid2">
<div class="box b">
  <div class="h">110 分钟怎么分</div>
  <table style="margin:4px 0">
    <tr><td><b>选择题 20 道</b></td><td class="k">30 分钟</td><td>≈1.5 分钟/题</td></tr>
    <tr><td><b>大题 4 道</b></td><td class="k">60 分钟</td><td>≈15 分钟/题</td></tr>
    <tr><td><b>检查</b></td><td class="k">20 分钟</td><td>重算 + 每页签名</td></tr>
  </table>
  <p class="lead" style="margin-bottom:0">剩 15 分钟时会有提醒。⚠ 按<b>分值</b>分配时间：
  一道大题 10 分 = 三道选择题。</p>
</div>
<div class="box g">
  <div class="h">开卷怎么带</div>
  <ul style="margin-bottom:0">
    <li><b>速查表在最上面</b>，三个 Topic 各一栏，侧边贴标签。</li>
    <li><b>三个手算模板</b>各留一份<b>做过的完整例题</b>——考场上换数字照抄流程。</li>
    <li><b>陷阱清单</b>单独一页，开考前 10 分钟和交卷前各看一遍。</li>
    <li class="w">⚠ 别带没做过标记的整本讲义：翻不到就等于没带。</li>
  </ul>
</div>
</div>

<div class="box r">
  <div class="h">⚠ 三条会直接丢分的操作习惯</div>
  <ul style="margin-bottom:0">
    <li><b>算梯度时提前更新了参数。</b>所有梯度必须在<b>同一个（更新前的）参数状态</b>上求值，
    全部算完再一起更新 —— T1、T2 两课都专门强调过，是最容易被扣分的地方。</li>
    <li><b>中间步骤过早四舍五入。</b>讲义反复提醒「中间多留几位，最后一步才四舍五入」；
    p = 0.750260 这种六位数就是提示你别只留两位。</li>
    <li><b>只写最终数字。</b>官方评分口径明说这样<b>可能不足以体现所需的理解</b>。
    每道大题至少写出：用了哪个公式 → 代入了什么 → 结果说明什么。</li>
  </ul>
</div>''')

# ═════════════════════ T1 速查 ═════════════════════
A('''<h2 id="t1">T1 · 神经网络基础 <em>速查</em></h2>

<h3>一条主线：预测 → 损失 → 梯度 → 更新 → 复查</h3>
<div class="eq">前向：  z = Σ w<sub>i</sub>x<sub>i</sub> + b            p = σ(z) = 1/(1+e<sup>−z</sup>)
损失：  y=1 ⇒ <b>L = −log p</b>        y=0 ⇒ <b>L = −log(1−p)</b>
信号：  <b>δ = ∂L/∂z = p − y</b>        ← sigmoid + BCE 专属化简
梯度：  <b>∂L/∂w<sub>i</sub> = δ·x<sub>i</sub></b>        <b>∂L/∂b = δ</b>
更新：  <b>θ<sub>new</sub> = θ − η·∂L/∂θ</b>   ← 全部梯度用原参数算完再一起更新</div>

<h3>官方那个算例（背下来，考场上换数字照搬）</h3>
<div class="eq">x = [1, 2]   y = 1   w = [0.2, 0.4]   b = 0.1   η = 0.1

z = 1.1            p = 0.750260         L = 0.287335
δ = p − y = <b>−0.249740</b>
∂L/∂w₁ = −0.249740   ∂L/∂w₂ = <b>−0.499480</b>   ∂L/∂b = −0.249740
w₁ → 0.224974   w₂ → <b>0.449948</b>   b → 0.124974     ← ⚠ 减去负数 = 增大
复查： z = 1.249844   p = <b>0.777273</b>   L = <b>0.251964</b>   ← 概率靠近目标、损失下降</div>
<div class="box r" style="margin-top:6px">
  <p style="margin:0">⚠ w₂ 的梯度是 w₁ 的两倍，<b>只是因为 x₂ = 2 而 x₁ = 1</b>。
  <b>这不构成「第二个特征更重要」的排序</b> —— 讲义专门警告的一个误读。</p>
</div>

<h3>为什么一个神经元不够（必考）</h3>
<table>
<tr><th style="width:230px">问的是什么</th><th>标准答法</th></tr>
<tr><td><b>概率输出</b>是非线性的吗？</td><td class="k">是。sigmoid 让 p 对输入非线性，曲面是弯的</td></tr>
<tr><td><b>决策边界</b>是什么形状？</td><td class="w">仍是直线。阈值 0.5 对应 z = 0，而 z = 0 是一条直线</td></tr>
<tr><td>为什么？</td><td><b>sigmoid 保序</b>：正分数给 &gt;0.5、负分数给 &lt;0.5，
  所以「哪里越过 0.5」完全由「哪里 z 越过 0」决定</td></tr>
<tr><td>限制究竟来自什么？</td><td class="n">来自<b>「仿射分数 + 单调激活 + 固定阈值」这个组合</b>，
  <s>不是单纯因为只有一个神经元</s> —— 多个仿射层叠在 sigmoid 前面，限制照旧</td></tr>
<tr><td>异或型数据训练更久行不行？</td><td class="w">不行。<b>这是模型表达能力的限制</b>，
  「再 train 久一点」是错误选项</td></tr>
</table>

<h3>塌缩论证（带数字那一版）</h3>
<div class="eq">没有激活： h = 2x + 1,  s = 3h + 4  ⇒  s = 3(2x+1)+4 = <b>6x + 7</b>   ← 两层塌缩成一层
                「加权和 + 偏置」这种函数叫 <b>仿射函数（affine）</b>

插入 ReLU： h = max(0, 2x+1),  s = 3h + 4
     x ≤ −0.5 ⇒ h = 0      ⇒ s = <b>4</b>      （平的）
     x &gt; −0.5 ⇒ h = 2x+1   ⇒ s = <b>6x + 7</b>  （上升）
     两段在 x = −0.5 处相接 ⇒ <b>出现折点，不再是一条直线</b>

自测： x = −1 ⇒ 有 ReLU 得 4、无 ReLU 得 1；x = 1 ⇒ 两者都是 13</div>
<div class="box y" style="margin-top:6px">
  <p style="margin:0"><b>「只在最后放个 sigmoid」行不行？</b>不行。没有非线性的隐藏激活，
  送进最后那个 sigmoid 之前的分数<b>仍然是输入的仿射函数</b>，边界还是直的。</p>
</div>

<h3>计算图：相乘与相加</h3>
<table>
<tr><th style="width:150px">运算</th><th style="width:200px">局部导数</th><th>含义</th></tr>
<tr><td>r = a + b</td><td class="k">∂r/∂a = 1；∂r/∂b = 1</td><td><b>加法原样传递</b>变化</td></tr>
<tr><td>r = a·b</td><td class="k">∂r/∂a = b；∂r/∂b = a</td><td><b>另一个因子</b>决定缩放倍数</td></tr>
<tr><td>r = a²</td><td class="k">∂r/∂a = 2a</td><td>敏感度取决于当前值</td></tr>
<tr><td>p = σ(z)</td><td class="k"><b>∂p/∂z = p(1−p)</b></td><td>敏感度取决于<b>它自己的输出</b></td></tr>
</table>
<div class="box b">
  <p style="margin:0"><b>一条路径内部 → 相乘；多条路径汇合 → 相加。</b>
  官方小例子：q → r = 2q、q → t = 3q、F = r + t ⇒ <b>dF/dq = 1×2 + 1×3 = 5</b>
  （只算一支得 2，<span class="w">漏掉另一支</span>）。
  ⭐ 网络里<b>一个隐藏激活可能喂给后面多个单元，它的梯度要收集所有路径的贡献</b>。</p>
</div>''')

# ═════════════════════ T2 速查 ═════════════════════
A('''<h2 id="t2">T2 · 训练神经网络 <em>速查</em></h2>

<h3>⭐ 激活函数表（必须会默写）</h3>
<table>
<tr><th>函数</th><th>定义</th><th>导数</th><th>z = −2</th><th>z = 0</th><th>z = 2</th></tr>
<tr><td><b>Sigmoid</b></td><td>1/(1+e<sup>−z</sup>)</td><td class="k"><b>g(1−g)</b></td>
    <td>0.119 / <b>0.105</b></td><td>0.500 / <b>0.250</b></td><td>0.881 / <b>0.105</b></td></tr>
<tr><td><b>tanh</b></td><td>(e<sup>z</sup>−e<sup>−z</sup>)/(e<sup>z</sup>+e<sup>−z</sup>)</td>
    <td class="k"><b>1 − g²</b></td>
    <td>−0.964 / <b>0.071</b></td><td>0 / <b>1</b></td><td>0.964 / <b>0.071</b></td></tr>
<tr><td><b>ReLU</b></td><td>max(0, z)</td><td class="k">0 (z&lt;0)；1 (z&gt;0)</td>
    <td>0 / <b>0</b></td><td>0 / <b class="w">0</b></td><td>2 / <b>1</b></td></tr>
<tr><td><b>Leaky ReLU</b></td><td>max(αz, z)，α = 0.01</td><td class="k">α (z&lt;0)；1 (z&gt;0)</td>
    <td class="w">−0.02 / <b>+0.01</b></td><td>0 / <b class="w">0.01</b></td><td>2 / <b>1</b></td></tr>
</table>
<p class="lead">每格是「输出 / 导数」。⚠ <b>本课规定 ReLU′(0) = 0、LeakyReLU′(0) = α = 0.01</b>，
各家软件约定不同，<b>考试按本课的判</b>。tanh(1) ≈ 0.7616，导数 = 1 − 0.7616² ≈ <b>0.4200</b>。</p>
<div class="box r">
  <p style="margin:0">⚠⚠ <b>Leaky ReLU 在 z = −2 处输出是负的（−0.02）、导数却是正的（+0.01）</b>
  —— 页面原话：<b>输出的符号和斜率的符号是两回事</b>。
  另一条同样容易错：<b>大的输出不代表大的梯度</b>，这两件事互不相干。</p>
</div>

<h3>饱和、梯度消失、死亡 ReLU —— 答题的分寸</h3>
<table>
<tr><th style="width:170px">概念</th><th>要点（⚠ 是讲义特意加的限定，答题要带上）</th></tr>
<tr><td><b>饱和</b></td><td>sigmoid / tanh 在 |z| 大时导数非常小；连乘会<b>梯度消失</b>
  （量级感：五个 0.1 连乘 = 0.00001）。
  <span class="w">⚠ 真实梯度还包含权重和跨多条路径的求和，
  「激活斜率小」只是一个成因，不是完整的诊断。</span></td></tr>
<tr><td><b>死亡 ReLU</b></td><td>预激活<b>对所有相关样本都为负</b> ⇒ 梯度恒为 0，收不到有用更新。
  <span class="w">⚠「某个样本上输出 0」≠「这个单元死了」</span>
  —— 它对别的观测可能是激活的。</td></tr>
</table>

<h3>⭐ 输出层与损失的配对（考纲逐条点名）</h3>
<table>
<tr><th>任务</th><th>输出层</th><th>损失</th><th>要点</th></tr>
<tr><td><b>回归</b></td><td class="k">线性输出</td><td class="k">MSE 或 MAE</td>
    <td>MSE 单位是目标单位的<b>平方</b>；MSE→条件均值，MAE→条件中位数</td></tr>
<tr><td><b>二分类</b></td><td class="k">一个 sigmoid</td><td class="k">BCE</td>
    <td>输出表示 P(y=1 | x)</td></tr>
<tr><td><b>互斥多分类</b></td><td class="k">softmax</td><td class="k">多类交叉熵</td>
    <td>概率<b>加起来等于 1</b>；<b>整数标签用 sparse 版</b></td></tr>
<tr><td><b>多标签</b></td><td class="k">每标签一个 sigmoid</td><td class="k">每标签各做一次 BCE</td>
    <td><b>不必加起来等于 1</b>；⚠ 标签之间<b>不必统计独立</b></td></tr>
</table>
<div class="box r">
  <p style="margin:0">⚠ <b>软件里数值稳定的损失常常直接接收原始 logits，内部自己做 sigmoid 或 softmax
  —— 用这种选项时不要再套一遍激活。</b>
  ⭐ <b>softmax 平移不变</b>：给每个 logit 都加同一个数，概率完全不变
  （所以可以「先减去最大 logit」来避免巨大的指数）。
  算例：logits [1, 2, 0] ⇒ [0.245, 0.665, 0.090]。</p>
</div>

<h3>⭐⭐ 为什么 sigmoid 配 BCE（本课最该记的推导）</h3>
<div class="eq">sigmoid + <b>半平方误差</b> ½(a−y)²：  ∂ℓ/∂z = (a − y) · <b>a(1−a)</b>   ← 多出来的因子是祸根
sigmoid + <b>BCE</b>：               ∂ℓ/∂z = <b>a − y</b>              ← 干净

算例 y = 1、a = 0.01（非常自信地判错）：
    半平方： (0.01−1) × 0.01 × 0.99 = <b>−0.009801</b>
    BCE：    0.01 − 1              = <b>−0.99</b>      ← 相差两个数量级</div>
<p class="lead">⚠ 讲义的限定：<b>这个优势只针对这一对输出–损失的组合，BCE 并不能阻止深层网络中别处出现小梯度。</b>
⚠ 「半平方」不是 MSE：普通平方误差求导给 2(a−y)，取平均还多一个 1/N ——<b>推导前先说清用的是哪个约定</b>。</p>
<div class="box b">
  <p style="margin:0"><b>softmax + 交叉熵</b>的 logit 梯度是 <b>∂ℓ/∂z<sub>k</sub> = p<sub>k</sub> − y<sub>k</sub></b>，
  把二分类的 p − y 推广到互斥多类。算例 p = (0.1, 0.7, 0.2)、真类是 2 ⇒ 梯度 (0.1, −0.3, 0.2)，
  <b>三项加起来等于 0</b>（很好的自查）。⚠ 这是<b>对 logit 的</b>导数，不是对概率、也不是对权重的。</p>
</div>

<h3>⭐ 隐藏层梯度四步（M3 T2 Tutorial Q3 就考这个）</h3>
<div class="eq">① ∂L/∂s   = <b>p − y</b>                     （sigmoid + BCE）
② ∂L/∂h<sub>j</sub> = (∂L/∂s) × <b>v<sub>j</sub></b>               （乘上该隐藏单元的<b>输出权重</b>）
③ ∂L/∂z<sub>j</sub> = (∂L/∂h<sub>j</sub>) × <b>g′(z<sub>j</sub>)</b>            （穿过激活；ReLU 时是 1 或 0）
④ ∂L/∂w<sub>ji</sub> = (∂L/∂z<sub>j</sub>) × <b>x<sub>i</sub></b>              ∂L/∂b<sub>j</sub> = ∂L/∂z<sub>j</sub></div>
<table>
<tr><th style="width:250px">官方算例（x = [1,2]，y = 1，η = 0.1）</th><th>数值</th></tr>
<tr><td>隐藏 1 [0.2, 0.4] b 0.1 · ReLU</td><td>z₁ = <b>1.1</b> ⇒ h₁ = 1.1（激活）</td></tr>
<tr><td>隐藏 2 [−0.5, 0.3] b −0.2 · ReLU</td><td>z₂ = −0.1 ⇒ h₂ = <b>0</b>（不激活）</td></tr>
<tr><td>输出 [0.7, −0.4] c −0.1 · sigmoid</td><td>s = 0.67，p = <b>0.661503</b>，L = 0.413241</td></tr>
<tr><td>① ∂L/∂s</td><td class="k">−0.338497</td></tr>
<tr><td>② ∂L/∂h₁ = −0.338497 × 0.7</td><td class="k">−0.236948</td></tr>
<tr><td>③ z₁ &gt; 0 ⇒ ×1</td><td class="k">−0.236948</td></tr>
<tr><td>④ ∂L/∂w₁₂ = −0.236948 × x₂ = ×2</td><td class="k"><b>−0.473896</b> ⇒ w₁₂ → 0.447390</td></tr>
<tr><td>一步之后</td><td>p = <b>0.700487</b>，L = <b>0.355979</b></td></tr>
</table>
<div class="box r">
  <p style="margin:0">⚠ 这一步里有<b>两处「没变」</b>，都要会解释：
  <b>隐藏 2 整个没动</b>（它不激活，输入权重梯度全为 0）；
  <b>输出的第二个权重 −0.4 也没动</b>（梯度 = (p−y)·h₂ = (p−y)·0 = 0）。
  ⚠ 计算隐藏层梯度时用的是<b>原来的输出权重 0.7</b>，不是更新后的 0.737235
  ——<b>所有梯度都要在同一个参数状态上求值</b>。</p>
</div>

<h3>batch · epoch · 自动微分</h3>
<div class="eq"><b>batch</b> = 算一次更新所用的那组观测      <b>epoch</b> = 把训练集完整过一遍
100 个观测 / 批大小 20  ⇒  <b>1 epoch = 5 次更新，3 epoch = 15 次</b>
全批量（full-batch）：每个 epoch 只更新一次

平均损失 L = (1/N)ΣL<sub>n</sub>，输出分数梯度数组 = <b>(P − Y)/N</b>
⚠ <b>这个 1/N 只除一次，别在每一层再除一遍</b>
⚠ 两个样本梯度 −0.2 和 +0.6 ⇒ 平均 +0.2 ⇒ 参数减小
   <b>一次基于平均损失的更新，可能在改善平均的同时让某一个观测变差</b></div>
<table>
<tr><th style="width:210px">GradientTape 三问（考纲明确要求）</th><th>答案</th></tr>
<tr><td>tape 记录了什么？</td><td><code>tf.Variable</code> 标记哪些量可训练，
  tape 在<b>前向期间记录涉及这些变量的运算</b></td></tr>
<tr><td><code>tape.gradient</code> 返回什么？</td><td>按请求顺序返回<b>梯度</b>
  —— <span class="w">⚠ 它不更新参数</span></td></tr>
<tr><td>哪个操作真正改变参数？</td><td class="k"><b><code>assign_sub</code></b></td></tr>
</table>
<div class="eq">官方例子： w = 1.5, b = −1.0, 输入 2.0, ReLU, loss = 0.5(a−5)², η = 0.05
z = 2  ⇒  a = 2  ⇒  loss = <b>4.5</b>
∂loss/∂a = a − 5 = −3 ；z &gt; 0 ⇒ ReLU 倍数 1
<b>g<sub>w</sub> = −3 × 1 × 2.0 = −6</b>      <b>g<sub>b</sub> = −3 × 1 × 1 = −3</b>
w → 1.5 − 0.05(−6) = <b>1.8</b>      b → −1.0 − 0.05(−3) = <b>−0.85</b>
重新前向： z = 2.75 = a ⇒ loss = <b>2.53125</b>   ← 从 4.5 降下来了</div>
<div class="box r">
  <p style="margin:0">⚠⚠ 自动微分<b>不</b>做这些：<b>不替你选一个有用的目标、不修复数据泄漏、
  不保证学习率是好的</b>。<b>参数更新是优化器完成的</b>——把两行 <code>assign_sub</code> 删掉，
  光调用 <code>tape.gradient</code> 训练不了模型。</p>
</div>
<div class="box y">
  <p style="margin:0"><b>代码 vs 手推的转置坑。</b>手推把一个输入存成「列」，代码把观测存成「行」
  ⇒ <b>代码里每个权重矩阵都是手推版本的转置</b>，<b>转置只是行列互换，不改变网络本身</b>。
  ⚠ 官方例子里 W1 恰好是方阵，<b>转置不改变形状但确实挪动了元素</b>——这个巧合会掩盖问题。
  换成 <b>3 个隐藏单元、2 个输入</b>：手推 <b>3×2</b>，代码 <b>2×3</b>，输出权重代码矩阵 <b>3×1</b>。</p>
</div>''')

# ═════════════════════ T3 速查 ═════════════════════
A('''<h2 id="t3">T3 · 模型评估 <em>速查</em></h2>

<h3>三种数据角色与防泄漏五步</h3>
<table>
<tr><th style="width:96px">角色</th><th>用来做什么</th></tr>
<tr><td><b>训练集</b></td><td>拟合权重<b>以及其它学到的量</b> —— ⚠ <b>包括缩放参数和缺失值填补参数</b></td></tr>
<tr><td><b>验证集</b></td><td>比较各种<b>选择</b>：隐藏层大小、激活函数、正则化、<b>停止点</b>、<b>判定阈值</b>
  （统称<b>开发决策</b>）</td></tr>
<tr><td><b>测试集</b></td><td>评估<b>已经选定并冻结</b>的流程。
  <span class="w">⚠ 不得用它的标签或结果来做这个选择</span></td></tr>
</table>
<div class="eq"><b>防泄漏五步</b>
1. 先把数据划分成 训练 / 验证 / 测试
2. <b>只用训练集</b>计算填补参数和缩放参数
3. 把这些学到的参数<b>应用</b>到验证集和测试集 —— <b>不要重新拟合</b>
4. 用<b>验证</b>结果选择模型和超参数
5. 所有选择固定之后，在<b>没碰过的测试集</b>上评估<b>一次</b></div>
<div class="box r">
  <p style="margin:0">⚠⚠ <b>不用标签也会泄漏。</b>训练值 [0, 2] 的均值是 1，留出值 100 应当中心化成 99；
  若三个值放一起算均值 ≈ 34，<b>留出的那个案例就改变了连训练数据本身的表示方式</b>。
  ⇒ <b>「无监督」不等于「可以安全地在测试数据上拟合」</b>——PCA 同理，
  必须<b>在每个训练划分或折的内部</b>拟合。</p>
</div>
<table>
<tr><th style="width:130px">划分方式</th><th>什么时候用</th></tr>
<tr><td><b>分层 Stratified</b></td><td>类别不平衡时，<b>保持各类比例</b></td></tr>
<tr><td><b>分组 Grouped</b></td><td><b>同一个人/病人/设备/站点</b>的记录放进<b>同一个</b>子集</td></tr>
<tr><td><b>按时间 Time-ordered</b></td><td>预测未来时，<b>早的训练、晚的验证</b></td></tr>
</table>
<p class="lead">⚠ <b>随机划分不是自动就合适的</b>；70/15/15 这类比例<b>是举例不是规则</b>。
<b>评估设计应当复现「真正没见过的数据将以什么方式到来」。</b></p>

<h3>⭐ 诊断表（措辞要照抄）</h3>
<table>
<tr><th style="width:190px">证据</th><th>标准答法</th></tr>
<tr><td><b>训练和验证都差</b></td><td class="n"><b>可能欠拟合或优化困难</b>：模型太受限、特征不足、或优化失败。
  <span class="w">⚠ 这个模式本身并不能断定「统计偏差高」</span></td></tr>
<tr><td><b>训练很强、验证明显更差</b></td><td class="n"><b>可能过拟合</b>。
  <span class="w">⚠⚠ 在把差距归因于方差之前，还要检查<b>分布差异、验证样本过小、以及泄漏</b></span></td></tr>
<tr><td><b>两边都强且接近</b></td><td class="k">学到的模式<b>迁移到了未见的验证样本</b></td></tr>
</table>
<p class="lead">⚠⚠ <b>这些是诊断模式，不是证明。</b>下一步都在验证集上做：加正则化 / 减小模型 / 增加数据 / 早停，
并<b>复核划分方式</b>（该不该用分组或时间划分）。</p>

<h3>学习率证据与重复训练证据</h3>
<div class="eq"><b>一步实验</b>（每行都是从同一初始参数<b>重置后只走一步</b>，不是连续步骤）
  η = 0    ⇒ 0.580352（没变）      η = 0.1 ⇒ 0.574996
  η = 1    ⇒ 0.533347              η = 10  ⇒ <b>0.371611</b>（这步最低）
  η = 100  ⇒ <b>9.965953</b>  ← <span class="w">飞了</span>
⚠ <b>单步最优 ≠ 全程最优</b>；大学习率后续可能震荡或发散

<b>连续 100 次更新</b>（η = 0.1，全批量）
  平均 BCE  0.580352 → <b>0.369420</b>
  正例 [1,2]   0.6615 → <b>0.9592</b>
  正例 [−1,−2] 0.4750 → <b class="w">0.4859</b>  ← <b>仍在 0.5 以下，一直判错</b>
  原因：<b>它的两个隐藏 ReLU 从一开始就是零，正类分数只依赖输出偏置</b></div>
<p class="lead">⚠⚠ <b>平均损失更低，不代表每个样本都被正确分类。</b>
⚠ <b>一次损失下降不能确立收敛</b>；看起来稳定也可能只是<b>优化变慢或卡住</b>。
真实任务里要：<b>定期监控验证表现、用开发数据定一条停止规则、保留验证最好的检查点</b>。</p>

<h3>⚠⚠ 混淆矩阵：先声明正类，再看摆法</h3>
<table>
<tr><th style="width:170px">来源</th><th>摆法</th><th style="width:76px">左上角</th></tr>
<tr><td><b>Canvas 讲义页</b></td><td>行 = 真实，列 = 预测，<b>正类在前</b> ⇒
  <code>[[TP, FN], [FP, TN]]</code></td><td>TP</td></tr>
<tr><td class="w"><b>M3 T3 复习课件</b></td><td>行 = 真实，列 = 预测，<b>负类在前</b> ⇒
  <code>[[TN, FP], [FN, TP]]</code></td><td class="w"><b>TN</b></td></tr>
<tr><td>sklearn <code>labels=[0,1]</code></td><td>同上 ⇒
  <code>[[TN, FP], [FN, TP]]</code></td><td>TN</td></tr>
<tr><td>CS229 评估指标幻灯</td><td class="w">列 = 真实，和前面都<b>转置</b></td><td>视定义</td></tr>
</table>
<div class="box r">
  <p style="margin:0">⚠⚠ <b>别背摆法 —— 两份官方材料是反的。</b>
  <b>Canvas 讲义页</b>把正类放前面（左上角 TP），而 <b>M3 T3 复习课件</b>画的是
  <code>Pred −/Pred +</code> 作列、<code>Actual −/Actual +</code> 作行，<b>左上角是 TN</b>。
  ⇒ 照课件自己给的办法做：<b>先定正类，再按「actual ?, predicted ?」逐格认，
  然后写一句「四格之和 = 样本数」自查。</b>
  四个计数在两种摆法下<b>完全相同</b>，变的只是位置。
  <span class="k">知道这件事反而是送分点——无论题目用哪种排法你都不会填反。</span></p>
</div>
<div class="eq"><b>Accuracy</b>  = (TP+TN)/总数
<b>Precision</b> = TP/(TP+FP)      分母 = <b>「我预测为正的」</b>
<b>Recall</b>    = TP/(TP+FN)      分母 = <b>「真实为正的」</b>
<b>F1</b>        = 2PR/(P+R) = <b>2TP/(2TP+FP+FN)</b>      ⚠ <b>不含 TN</b>

降低阈值： 预测为正<b>只增不减</b> ⇒ <b>recall 不会下降</b>；<b>precision 可升可降</b>
选阈值：   在<b>验证集</b>上用<b>代价与约束</b>选，⚠ 不要在测试集上调
代价法：   总代价 = c<sub>FN</sub>·FN + c<sub>FP</sub>·FP   ⭐ <b>代价一变结论就可能翻转</b></div>
<p class="lead">⚠ F1 里的 <b>P 是 precision 不是概率</b>；<b>TPR 是 recall 的另一个名字</b>。
F1 用<b>调和</b>平均：precision = 1、recall = 0.1 ⇒ F1 ≈ <b>0.182</b>（算术平均是 0.55）——<b>被小的那个拖住</b>。
⚠⚠ <b>F1 忽略 TN、把两者看得同等重要，并不自动就是每个不平衡问题的正确指标。</b></p>

<h3>⭐ ROC / AUC</h3>
<div class="eq">TPR = TP/(TP+FN) = <b>recall</b>        FPR = FP/(FP+TN) = <b>1 − specificity</b>

画 ROC： ① 定正类，分数越大 = 越支持该类
        ② <b>真实正例数、真实负例数这两个分母全程固定</b>
        ③ 从 <b>(0,0)</b> 开始（全判负），阈值往下降，⚠ <b>同分数的观测必须一起加</b>
        ④ <b>加正例 → 往上走；加负例 → 往右走</b>
        ⑤ 到 <b>(1,1)</b> 结束（全判正）

AUC 两种算法（互相验算）：
  梯形： Σ (ΔFPR) × (TPR<sub>i</sub> + TPR<sub>i+1</sub>)/2    ⚠ <b>竖直段面积为 0</b>
  配对： <b>P[随机正例分数 &gt; 随机负例分数]</b>，⭐ <b>平局算半胜</b>，不需要选任何阈值

四样本算例 A(0.90,1) B(0.80,0) C(0.40,1) D(0.10,0)：
  点 (0,0) → (0,0.5) → (0.5,0.5) → (0.5,1) → (1,1)
  梯形 0.25 + 0.50 = <b>0.75</b>；配对 3 胜/4 对 = <b>0.75</b>  ✓</div>
<div class="box r">
  <p style="margin:0">⚠⚠ <b>AUC 不决定四件事</b>：<b>① 不替你选工作阈值；② 不衡量概率校准；
  ③ 不编码误报与漏报的真实代价；④ 负例很多时可能掩盖掉数量不可接受的误报。</b><br>
  <b>AUC = 1</b> 只说明<b>在被评估的这个样本上排序完美</b>，不保证未来的准确率；
  <b>AUC &lt; 0.5</b> 要去<b>检查分数方向、标签约定和抽样</b>，
  <s>而不是拿测试结果自动把模型反过来用</s>。<br>
  两个系统 AUC 相同，<b>可用阈值与误报代价不一定相同</b>——
  <b>AUC 概括的是整条曲线，不是某一个工作点</b>。</p>
</div>
<div class="box y">
  <p style="margin:0"><b>⭐ 稀有正例那个算例（最该记的数字）。</b>
  1000 个观测、只有 10 个正例；在 <b>TPR = 0.8、FPR = 0.1</b> 处：
  TP = 8、FN = 2、<b>FP = 0.1 × 990 = 99</b> ⇒
  <b>recall = 80%，precision = 8/107 ≈ 7.5%</b>。<br>
  原因：<b>两者分母完全不同</b> —— recall 的分母是 10 个真实正例，
  precision 的分母是 107 个「被预测为正」。
  ⇒ <b>ROC 衡量类内条件的排序行为；precision 揭示在这个 prevalence 下正类预测的实际质量。</b>
  <b>单独改变 prevalence 不一定改变 ROC AUC，但 precision 可能变化很大。</b></p>
</div>''')

# ═════════════════════ Python ═════════════════════
A('''<h2 id="py">Python 速查 <em>考概念，不考写码</em></h2>
<p class="lead">考纲原文：<b>不要求手写 Python 代码</b>，但要能解读出现过的函数、参数、属性、
简短工作流和输出的<b>机器学习含义</b>。下面四件是页面<b>点名</b>的。</p>
<table>
<tr><th style="width:230px">点名的概念</th><th>要能说出什么</th></tr>
<tr><td><b>预测概率与阈值</b></td><td><code>predict_proba</code> 之类给的是<b>分数/概率</b>；
  <b>阈值把分数变成类别</b>。<b>换阈值不改变已拟合的权重</b>，只改变判定。</td></tr>
<tr><td><b>验证指标</b></td><td>训练历史里的 <code>val_*</code> 是<b>留出数据上的证据</b>；
  <b>和训练曲线对比</b>才能诊断欠拟合/过拟合。</td></tr>
<tr><td><b>GradientTape 自动微分</b></td><td>三问见 T2 速查：<b>tape 记录 → gradient 返回梯度
  → assign_sub 才改参数</b>。</td></tr>
<tr><td><b>标签编码要匹配损失</b></td><td><b>整数标签 ⇒ sparse categorical cross-entropy</b>；
  one-hot ⇒ 普通 categorical cross-entropy。
  ⚠ <code>from_logits</code> 的实现<b>内部自己做激活，别套第二遍</b>。</td></tr>
</table>
<p class="lead">⚠ 形状自查：N 个观测、2 个输入特征、3 个隐藏单元 ⇒
<code>H</code> 是 <b>(N, 3)</b>、<code>P</code> 是 <b>(N, 1)</b>、<code>Y</code> 是 <b>(N, 1)</b>；
代码的 <code>W1</code> 是 <b>(2, 3)</b>（<b>每一列属于一个接收的隐藏单元</b>）。
<b>PyTorch 对照和外部框架教程是可选的；M3T1 的 notebook 用的是 NumPy。</b></p>''')

# ═════════════════════ 英文句库 ═════════════════════
A('''<h2 id="en">英文句库 <em>直接抄进答卷</em></h2>
<div class="grid2">
<div class="box b">
  <div class="h">机制与计算</div>
  <ul style="margin-bottom:0">
    <li>The forward pass uses the <b>current</b> parameters; <b>no parameter changes</b>, so no learning has occurred yet.</li>
    <li>Back-propagation <b>computes</b> the gradients; gradient descent <b>uses</b> them to change the parameters.</li>
    <li>All gradients are evaluated at the <b>same (pre-update) parameter state</b>, then the parameters are updated together.</li>
    <li>For a sigmoid output with binary cross-entropy the chain rule simplifies to <b>δ = p − y</b>.</li>
    <li>The unit is <b>inactive for this observation</b>, so its local derivative is zero and its input-weight gradients vanish.</li>
  </ul>
</div>
<div class="box g">
  <div class="h">解释与局限</div>
  <ul style="margin-bottom:0">
    <li>This shows the loss decreased <b>on this training example</b>; it is <b>not evidence of generalisation</b>.</li>
    <li>The decision boundary is a straight line because the threshold at 0.5 corresponds to <b>z = 0</b>.</li>
    <li>The limitation comes from the combination of an <b>affine score, a monotonic activation and a fixed threshold</b>.</li>
    <li>A larger gradient here reflects the <b>larger input value</b>, not a general ranking of feature importance.</li>
    <li>These are <b>diagnostic patterns, not proof</b>.</li>
  </ul>
</div>
<div class="box y">
  <div class="h">评估与泄漏</div>
  <ul style="margin-bottom:0">
    <li>Fit the scaler on the <b>training split only</b> and <b>apply</b> it to the validation and test data.</li>
    <li>Learning from the inputs can cross the evaluation boundary <b>even when no labels are used</b>.</li>
    <li>Select the threshold on <b>validation</b> evidence together with the <b>costs</b> of the application, then <b>freeze</b> it.</li>
    <li>Report the frozen pipeline on the <b>held-out test set once</b>.</li>
    <li>Before attributing the gap to variance, check <b>distribution differences, a small validation sample, and leakage</b>.</li>
  </ul>
</div>
<div class="box v">
  <div class="h">指标与 ROC</div>
  <ul style="margin-bottom:0">
    <li>Accuracy is dominated by the <b>large number of negatives</b> and does not express the cost of each error type.</li>
    <li>Lowering the threshold cannot decrease recall, but precision <b>need not improve</b>.</li>
    <li>AUC is the probability that a randomly chosen positive is <b>ranked above</b> a randomly chosen negative.</li>
    <li>AUC summarises the <b>whole curve</b>, not the operating point that would actually be used.</li>
    <li>With a low prevalence a small FPR still produces <b>many false positives</b>, so precision can be low even when recall is high.</li>
  </ul>
</div>
</div>''')

# ═════════════════════ 陷阱清单 ═════════════════════
A('''<h2 id="trap">陷阱清单 <em>考前 10 分钟看这栏</em></h2>
<table>
<tr><th style="width:92px">归属</th><th>陷阱</th><th>正确做法</th></tr>
<tr><td><b>T1</b></td><td>把激活输出 a 当成参数</td><td class="k">参数<b>只有权重和偏置</b>；a、z 是每个样本现算的</td></tr>
<tr><td><b>T1</b></td><td>以为 sigmoid 非线性 ⇒ 边界是曲线</td><td class="k">边界仍是<b>直线</b>（z = 0）</td></tr>
<tr><td><b>T1</b></td><td>「异或型数据再 train 久一点」</td><td class="k">这是<b>表达能力</b>的限制，训练再久也不行</td></tr>
<tr><td><b>T1</b></td><td>梯度绝对值大 ⇒ 特征更重要</td><td class="k">只是<b>输入数值不同</b>，不构成重要性排序</td></tr>
<tr><td><b>T1/T2</b></td><td>算一个参数就更新一个</td><td class="k"><b>全部梯度用原参数算完，再一起更新</b></td></tr>
<tr><td><b>T2</b></td><td>把 1 − g² 当成 sigmoid 的导数</td><td class="k">1 − g² 是 <b>tanh</b>；sigmoid 是 <b>g(1−g)</b></td></tr>
<tr><td><b>T2</b></td><td>ReLU′(0) 填 1</td><td class="k"><b>本课约定 0</b>；Leaky 在 0 处是 <b>α = 0.01</b></td></tr>
<tr><td><b>T2</b></td><td>「这个样本上 ReLU 输出 0」= 这个单元死了</td><td class="k">要<b>在相关的那批输入上一直不激活</b>才算</td></tr>
<tr><td><b>T2</b></td><td>把梯度消失全归给激活函数</td><td class="k">真实梯度还含<b>权重与多路径求和</b>，这只是一个成因</td></tr>
<tr><td><b>T2</b></td><td>多标签用 softmax</td><td class="k">多标签是<b>每标签一个 sigmoid</b>，和不必为 1</td></tr>
<tr><td><b>T2</b></td><td><code>from_logits</code> 之外又套了一次 sigmoid</td><td class="k">这类损失<b>内部已经做了激活</b></td></tr>
<tr><td><b>T2</b></td><td>把 ∂ℓ/∂p 和 ∂ℓ/∂z 混用</td><td class="k"><b>p − y 是对 logit 的</b>，已含 sigmoid 的链式因子</td></tr>
<tr><td><b>T2</b></td><td>平均损失在每层又除一次 N</td><td class="k"><b>1/N 只除一次</b></td></tr>
<tr><td><b>T2</b></td><td>以为 <code>tape.gradient</code> 会更新参数</td><td class="k"><b><code>assign_sub</code></b> 才更新</td></tr>
<tr><td><b>T3</b></td><td>在划分之前对全部数据做缩放 / PCA</td><td class="k"><b>只在训练折内部拟合</b>，不用标签也会泄漏</td></tr>
<tr><td><b>T3</b></td><td>同一个人的记录分散到训练和测试</td><td class="k">用<b>分组划分</b></td></tr>
<tr><td><b>T3</b></td><td>在测试集上挑阈值 / 挑模型</td><td class="k">用<b>验证集</b>；测试集只评估一次冻结的流程</td></tr>
<tr><td><b>T3</b></td><td>「训练强验证差 ⇒ 就是方差高」</td><td class="k">先排除<b>分布差异、验证集过小、泄漏</b></td></tr>
<tr><td><b>T3</b></td><td>背死了「左上角是 TP」</td><td class="k"><b>先读行列标签</b>；讲义页左上角是 TP，<b>T3 复习课件左上角是 TN</b></td></tr>
<tr><td><b>T3</b></td><td>把 F1 里的 P 当成概率</td><td class="k">P 是 <b>precision</b></td></tr>
<tr><td><b>T3</b></td><td>以为降阈值 precision 一定变好</td><td class="k"><b>recall 不降，precision 可升可降</b></td></tr>
<tr><td><b>T3</b></td><td>用 AUC 回答「该用哪个阈值」</td><td class="k">AUC <b>不决定阈值、不衡量校准、不编码代价</b></td></tr>
<tr><td><b>全局</b></td><td>只写最终数字</td><td class="k">官方：<b>只给正确数字可能不足以体现理解</b></td></tr>
</table>''')

# ═════════════════════ 答题模板 ═════════════════════
A('''<h2 id="tpl">大题答题模板 <em>四类，各背一套</em></h2>

<details open><summary>模板 A ·「前向 + 梯度 + 一次更新」（最可能出现）</summary>
<ol>
<li><b>声明设定</b>：写出用的激活与损失（例：sigmoid 输出 + BCE，单个观测），以及学习率。</li>
<li><b>前向</b>：z = Σw<sub>i</sub>x<sub>i</sub> + b → p = σ(z) → L。<span class="k">每一步都留 ≥ 4 位小数。</span></li>
<li><b>梯度</b>：先写 <b>δ = ∂L/∂z = p − y</b>（并说明这是 sigmoid + BCE 的化简），
  再写 ∂L/∂w<sub>i</sub> = δ·x<sub>i</sub>、∂L/∂b = δ，代入数字。</li>
<li><b>更新</b>：θ − η·∂L/∂θ 逐个写出。
  <span class="w">明说一句：三个梯度都用更新前的原参数算，然后同时更新。</span></li>
<li><b>复查</b>：重算 z、p、L，指出<b>概率朝目标移动、损失下降</b>。</li>
<li><b>局限</b>（⚠ 这一句经常是最后 1–2 分）：
  <span class="k">这只证明在这一个样本上有改进，不证明泛化；要再走一步必须重新跑前向、重新算梯度。</span></li>
</ol></details>

<details><summary>模板 B ·「隐藏层的某个权重梯度」</summary>
<ol>
<li><b>画/写出路径</b>：w<sub>ji</sub> → z<sub>j</sub> → h<sub>j</sub> → s → p → L。</li>
<li><b>四步</b>依次写：① p − y ② ×输出权重 v<sub>j</sub> ③ ×g′(z<sub>j</sub>) ④ ×x<sub>i</sub>。
  <span class="k">每一步都说这一乘是哪个局部导数。</span></li>
<li><b>检查激活状态</b>：若 z<sub>j</sub> ≤ 0（ReLU），明说<b>局部导数为 0 ⇒ 该单元这一步完全不动</b>；
  同时 h<sub>j</sub> = 0 ⇒ <b>它的输出权重梯度也是 0</b>。</li>
<li><b>更新并复查</b>：重新跑<b>完整</b>前向，才能确认改变全部参数的合并效果。</li>
<li><b>解释</b>：为什么上层权重会出现在下层的梯度里 ——
  <span class="k">隐藏激活对损失的影响必须穿过输出层，那个权重正是 s 对 h<sub>j</sub> 的局部导数。</span></li>
</ol></details>

<details><summary>模板 C ·「给混淆矩阵/预测表，算指标并做决策」</summary>
<ol>
<li><b>声明正类</b>，并说明在这个应用里 FP 和 FN 各自意味着什么。</li>
<li><b>逐行比对得四个计数</b>，<span class="k">写一句自查：四个数之和 = 样本总数。</span></li>
<li><b>写公式再代数字</b>：accuracy、precision（分母 TP+FP）、recall（分母 TP+FN）、
  F1 = 2TP/(2TP+FP+FN)。</li>
<li><b>解释为什么只看 accuracy 不够</b>：
  <span class="k">它被大量负例主导，表达不出漏报和误报各自的代价。</span>
  必要时给出「全判多数类」的基线准确率作对照。</li>
<li><b>代价分析</b>：写出总代价 = c<sub>FN</sub>·FN + c<sub>FP</sub>·FP，比较两个阈值；
  <span class="w">并指出代价改变时结论可能翻转，不存在普适最优阈值。</span></li>
<li><b>流程</b>：<span class="k">阈值用验证证据加应用代价选定并冻结，再在没碰过的测试集上评估一次。</span></li>
</ol></details>

<details><summary>模板 D ·「评价一个做法 / 指出流程里的问题」</summary>
<ol>
<li><b>先判定</b>：这个做法<b>有问题 / 没问题</b>，一句话说清。</li>
<li><b>指出机制</b>：问题出在哪一步、违反了哪条边界。
  （常见：<span class="w">在划分前拟合预处理</span>、<span class="w">用测试集做选择</span>、
  <span class="w">同源记录跨划分</span>、<span class="w">只用训练证据下结论</span>。）</li>
<li><b>说后果</b>：会让估计偏乐观 / 破坏最终评估的独立性 / 衡量的不是对新样本的表现。</li>
<li><b>给正确做法</b>：按防泄漏五步重写流程。</li>
<li><b>加限定</b>：
  <span class="k">即使改正，划分给出的也只是对未见数据表现的估计，不保证泛化或分布漂移下的稳健性。</span></li>
</ol></details>''')


# ═════════════════════ 模拟卷 · 选择题 ═════════════════════
A("""<h2 id="mcq">模拟卷 · 第一部分 <em>20 题 × 3 分 = 60 分 · 建议 30 分钟</em></h2>
<p class="lead">全部<b>新编</b>，不和三册题库重复。按真卷比例覆盖三个 Topic。
⚠ 先把 20 题做完再展开答案。</p>""")

MCQ = [
 ("一个神经元的输入是 x = [3, −1]，权重 w = [0.4, 0.6]，偏置 b = −0.2。预激活 z 是多少？",
  ["0.4", "1.0", "1.2", "1.8"], "A",
  "z = 0.4(3) + 0.6(−1) + (−0.2) = 1.2 − 0.6 − 0.2 = <b>0.4</b>。"),

 ("下面哪一个量<b>不会</b>被优化器更新？",
  ["隐藏层的偏置", "输出层的权重", "隐藏层的激活输出 h", "输入层到隐藏层的权重"], "C",
  "<b>激活是每个样本重新算出来的中间值</b>，不是存下来的参数。参数只有权重和偏置。"),

 ("某个 sigmoid 神经元对一个样本给出 p = 0.93，而这个样本的真实标签是 0。关于这次前向传播，下面哪句对？",
  ["损失一定为 0，因为 0.93 ≥ 0.5", "目标 y 没有参与这次前向计算",
   "参数已经朝降低损失的方向改变了一点", "必须先把 p 四舍五入成类别才能算损失"], "B",
  "前向只用<b>当前参数</b>把输入算到输出；<b>y 在这一步没被用到</b>，参数也没有改变。"
  "而且 BCE 用的是<b>概率本身</b>，不是四舍五入后的类别。"),

 ("两层都不加激活函数：h = 4x − 1，s = 2h + 5。等价的单层是什么？",
  ["s = 8x + 3", "s = 8x + 4", "s = 6x + 3", "s = 2x + 5"], "A",
  "s = 2(4x − 1) + 5 = 8x − 2 + 5 = <b>8x + 3</b>。两层<b>塌缩成一个仿射函数</b>。"),

 ("关于单个 sigmoid 神经元的决策边界，下面哪句是讲义的准确说法？",
  ["边界是曲线，因为 sigmoid 是非线性的",
   "边界是直线，限制来自「仿射分数 + 单调激活 + 固定阈值」这个组合",
   "边界是直线，唯一原因是模型只有一个神经元",
   "边界形状取决于学习率，步长够小就会变弯"], "B",
  "⚠ 措辞很讲究：<b>多个仿射层叠在 sigmoid 前面，直边界的限制依然在</b>，"
  "所以不能说「唯一原因是只有一个神经元」。"),

 ("共享值 q 分别影响 r = 5q 和 t = −2q，再合并成 F = r + t。dF/dq 是多少？",
  ["−10", "3", "5", "7"], "B",
  "1×5 + 1×(−2) = <b>3</b>。<b>一条路径内部相乘，多条路径汇合相加。</b>"),

 ("y = 0、p = 0.25 时，二元交叉熵损失约等于多少？",
  ["0.2877", "1.3863", "0.1250", "0.7500"], "A",
  "y = 0 ⇒ L = −log(1 − p) = −log(0.75) ≈ <b>0.2877</b>。"
  "（−log(0.25) ≈ 1.3863 是 y = 1 时的答案。）"),

 ("sigmoid 输出 + BCE，p = 0.3、y = 1、x = [2, −4]。∂L/∂w₂ 是多少？",
  ["−1.4", "2.8", "−0.7", "0.3"], "B",
  "δ = p − y = −0.7；∂L/∂w₂ = δ·x₂ = (−0.7)(−4) = <b>+2.8</b>。"
  "⚠ 负负得正，符号别丢。"),

 ("tanh 在某点的输出是 −0.6，它在该点的导数是多少？",
  ["−0.36", "0.40", "0.64", "1.60"], "C",
  "tanh′ = 1 − g² = 1 − 0.36 = <b>0.64</b>。⚠ 别套成 sigmoid 的 g(1−g)。"),

 ("按本课的约定，z = 0 处 ReLU 和 Leaky ReLU（α = 0.01）的导数分别是：",
  ["1 和 1", "0 和 0.01", "0.5 和 0.01", "0 和 0"], "B",
  "⚠ 数学上这两点不可导，<b>本课规定 ReLU′(0) = 0、LeakyReLU′(0) = α</b>，考试按这个判。"),

 ("一条反向路径上传入的损失梯度是 −0.8，这一步的激活是 Leaky ReLU 且该处 z = −3（α = 0.01）。传出去的梯度是多少？",
  ["−0.8", "−0.008", "0", "+0.008"], "B",
  "z &lt; 0 ⇒ 局部导数 α = 0.01 ⇒ −0.8 × 0.01 = <b>−0.008</b>。"
  "若换成 ReLU 则是 0 —— <b>这条路径彻底断掉</b>。"),

 ("一个模型要给新闻打上「体育」「政治」「国际」等标签，一篇文章可以同时属于多个。应该用什么输出与损失？",
  ["softmax + sparse categorical cross-entropy",
   "一个线性输出 + 均方误差",
   "每个标签一个 sigmoid + 对每个标签各做一次 BCE",
   "softmax + 多类交叉熵"], "C",
  "这是<b>多标签</b>（可共现），不是互斥多分类。各 sigmoid <b>不必加起来等于 1</b>。"),

 ("softmax 的 logits 从 [2, 5, 1] 改成 [7, 10, 6]，输出概率会怎样？",
  ["完全不变", "最大的那个变大，其余变小", "全部趋近 1/3", "全部乘以 e⁵"], "A",
  "⭐ <b>softmax 平移不变</b>：给每个 logit 加同一个数，概率不变。"
  "数值稳定技巧「先减最大 logit」正是用这一点。"),

 ("某隐藏 ReLU 单元对当前观测的预激活是 −0.4。关于这一步，下面哪句对？",
  ["这个单元已经死了，应该重新初始化",
   "它这次的输入权重梯度全为 0，但它对别的观测可能是激活的",
   "它的输出是 −0.4，导数是 1",
   "它的梯度会反号传给下一层"], "B",
  "⚠ <b>「这个样本上不激活」≠「这个单元死了」</b> —— 要在相关的那批输入上<b>一直</b>不激活才算。"),

 ("训练集有 240 个观测，批大小 16，跑 4 个 epoch。一共更新多少次？",
  ["15 次", "60 次", "64 次", "960 次"], "B",
  "每个 epoch 240 ÷ 16 = 15 次，4 个 epoch = <b>60 次</b>。"),

 ("下面关于 <code>tape.gradient(loss, [w, b])</code> 的说法，哪一句对？",
  ["它返回更新后的参数值",
   "它返回梯度，但不改变任何参数",
   "它等价于一次完整的梯度下降更新",
   "它只能用于最后一层的参数"], "B",
  "⚠ <b>真正改变参数的是 <code>assign_sub</code></b>。"
  "这正是「反向传播算梯度、优化器改参数」在代码里的体现。"),

 ("某团队先用全部 5000 条数据拟合了标准化器，再划分训练/验证/测试。这样做的问题是什么？",
  ["没有问题，标准化不使用标签",
   "没有问题，只要测试集足够大",
   "构成信息泄漏：从输入里学习同样会越过评估边界",
   "问题只在于标准化应该放在模型之后"], "C",
  "⚠⚠ 讲义的关键一句：<b>从输入里学习、即使没用到标签，一样可能越过评估边界。</b>"
  "正确顺序是<b>先划分，只用训练集算缩放参数，再应用到验证和测试</b>。"),

 ("一个二分类器的训练准确率 0.96、验证准确率 0.71。按讲义的措辞，正确的结论是什么？",
  ["确定是过拟合，方差过高，应当立刻加正则化并减小模型",
   "可能过拟合；在归因于方差之前还要检查分布差异、验证样本过小和泄漏",
   "确定是欠拟合，模型容量不足，应当加宽隐藏层并延长训练",
   "无法判断，必须先看测试集上的结果才能作出诊断"], "B",
  "⚠⚠ <b>这些是诊断模式，不是证明</b>；而且<b>测试集在最终流程选定之前一直不要碰</b>。"),

 ("在固定的预测分数上把判定阈值从 0.6 降到 0.3，下面哪句一定成立？",
  ["precision 一定上升", "recall 不会下降", "accuracy 一定上升", "AUC 会变大"], "B",
  "预测为正的数量<b>只增不减</b> ⇒ TP 不减 ⇒ recall 不降；"
  "<b>precision 可升可降</b>。⚠ <b>AUC 与阈值无关</b>，改阈值不会改变 AUC。"),

 ("某检测器 TP = 15、FP = 45、FN = 5、TN = 435。它的 precision 和 recall 分别是多少？",
  ["0.25 和 0.75", "0.75 和 0.25", "0.25 和 0.25", "0.30 和 0.75"], "A",
  "precision = 15/(15+45) = <b>0.25</b>；recall = 15/(15+5) = <b>0.75</b>。"
  "⚠ accuracy = 450/500 = 0.90 看着很高，<b>但「全判负」的基线就有 480/500 = 0.96</b>。"),
]

assert len(MCQ) == 20, len(MCQ)

# ⚠ 我写题时正确答案天然堆在 B（先写错项、再写正确那条）：这 20 题原始分布是
#   A5 / B11 / C4 / D0 —— 一份「从来不选 D」的模拟卷是会被直接看穿的。
#   用和题库同一套洗牌袋打散：每连续 4 题 A/B/C/D 各一次，极差 ≤ 1。
#   只轮换选项顺序，不改任何文字；这 20 题里没有「以上都不是」这类位置相关选项。
import collections
import random


def _balance(items, seed=20261109):
    rnd = random.Random(seed)
    bag = []
    while len(bag) < len(items):
        b = [0, 1, 2, 3]
        rnd.shuffle(b)
        bag += b
    out = []
    for (stem, ops, ans, why), tgt in zip(items, bag):
        cur = "ABCD".index(ans)
        ops = list(ops)
        ops[cur], ops[tgt] = ops[tgt], ops[cur]
        out.append((stem, ops, "ABCD"[tgt], why))
    return out


MCQ = _balance(MCQ)
_pos = collections.Counter(a for _, _, a, _ in MCQ)
_c = [_pos[k] for k in "ABCD"]
print("模拟卷答案位置 A/B/C/D = %d/%d/%d/%d　极差 %d %s"
      % (tuple(_c) + (max(_c) - min(_c), "✓" if max(_c) - min(_c) <= 1 else "✗")))
for _s, _o, _a, _ in MCQ:                      # 正确答案明显更长也是一种泄题
    _i = "ABCD".index(_a)
    _L = [len(x) for x in _o]
    if _L[_i] > 1.9 * (sum(_L) - _L[_i]) / 3 and _L[_i] - max(_L[:_i] + _L[_i + 1:]) > 12:
        print("   ⚠ 正确答案比其它选项长太多：", _s[:34])

for i, (stem, ops, ans, why) in enumerate(MCQ, 1):
    A(mcq(i, stem, ops, ans, why))

# ═════════════════════ 模拟卷 · 大题 ═════════════════════
A("""<h2 id="erq">模拟卷 · 第二部分 <em>4 题 × 10 分 = 40 分 · 建议 60 分钟</em></h2>
<p class="lead">⚠ 按官方评分口径作答：<b>写出中间步骤、说明相关假设、解释推理过程</b>。
<b>只给出正确的最终数字，可能不足以体现所需的理解。</b>每题的参考答案都给了<b>该写到什么程度</b>。</p>""")

A("""<div class="box b">
<div class="h">第 21 题 · 一个神经元的完整一次更新（10 分）</div>
<p>一个二分类神经元计算 z = w₁x₁ + w₂x₂ + b，p = σ(z)，损失用二元交叉熵。
某个样本 <b>x = [2, 1]，y = 0</b>；当前 <b>w = [0.3, −0.5]，b = 0.4</b>；学习率 <b>η = 0.2</b>。</p>
<ol>
  <li>计算 z、p、L，并按「p ≥ 0.5 判类 1」给出这一步的预测类别。（3 分）</li>
  <li>写出 ∂L/∂z 的化简式并说明它为什么成立，然后求 w₁、w₂、b 的梯度。（3 分）</li>
  <li>做一次同步更新，并重新跑前向给出新的 z、p、L 与预测类别。（2 分）</li>
  <li>这次更新证明了什么、没有证明什么？（2 分）</li>
</ol>
</div>
<details><summary>第 21 题 · 参考答案</summary>
<div class="eq">(1) z = 0.3(2) + (−0.5)(1) + 0.4 = 0.6 − 0.5 + 0.4 = <b>0.5</b>
    p = σ(0.5) = <b>0.622459</b>
    y = 0 ⇒ L = −log(1 − p) = −log(0.377541) = <b>0.974077</b>
    0.622459 ≥ 0.5 ⇒ 预测类别 <b>1</b>  ← <span class="w">判错了</span>

(2) sigmoid 输出 + BCE 时链式法则化简为 <b>δ = ∂L/∂z = p − y</b>
    （(−y/p + (1−y)/(1−p)) × p(1−p) 约掉后就是 p − y）
    δ = 0.622459 − 0 = <b>0.622459</b>
    ∂L/∂w₁ = δ·x₁ = 0.622459 × 2 = <b>1.244919</b>
    ∂L/∂w₂ = δ·x₂ = <b>0.622459</b>
    ∂L/∂b  = δ     = <b>0.622459</b>

(3) 三个梯度都用<b>更新前</b>的参数算，然后一起更新：
    w₁ = 0.3   − 0.2(1.244919) = <b>0.051016</b>
    w₂ = −0.5  − 0.2(0.622459) = <b>−0.624492</b>
    b  = 0.4   − 0.2(0.622459) = <b>0.275508</b>
    新 z = 2(0.051016) + 1(−0.624492) + 0.275508 = <b>−0.246951</b>
    新 p = σ(−0.246951) = <b>0.438574</b>        新 L = −log(0.561426) = <b>0.577275</b>
    0.438574 &lt; 0.5 ⇒ 预测类别 <b>0</b>  ← <span class="k">这次对了</span></div>
<p><b>(4) 该写什么。</b>这次更新证明：<span class="k">在这一个训练样本上，概率朝目标 0 移动了
（0.6225 → 0.4386），损失从 0.9741 降到 0.5773，而且判定也跟着翻了过来。</span>
它<b>没有</b>证明：<span class="w">模型能泛化到没见过的观测</span>
—— 这只是单个样本上的局部改进；
也<span class="w">不说明 η = 0.2 是好的步长</span>（一步走得好 ≠ 长期收敛得好）；
要再走一步必须<b>重新跑前向、重新算梯度</b>。</p>
<p class="lead" style="margin-bottom:0">⚠ 给分点通常落在：写出 δ = p − y 并说明来源、
明说「三个梯度用原参数算完再同时更新」、以及最后那条局限。</p>
</details>""")

A("""<div class="box b">
<div class="h">第 22 题 · 隐藏层权重的梯度（10 分）</div>
<p>一个网络有两个 ReLU 隐藏单元和一个 sigmoid 输出，损失用 BCE。观测 <b>x = [1, 3]，y = 1</b>，η = 0.5。</p>
<table style="margin:8px 0">
<tr><th>单元</th><th>输入权重</th><th>偏置</th><th>激活</th></tr>
<tr><td>隐藏 1</td><td>[0.5, −0.2]</td><td>0.1</td><td>ReLU</td></tr>
<tr><td>隐藏 2</td><td>[−0.3, 0.4]</td><td>0.2</td><td>ReLU</td></tr>
<tr><td>输出（输入 h₁, h₂）</td><td>[0.6, 0.5]</td><td>−0.3</td><td>Sigmoid</td></tr>
</table>
<ol>
  <li>做一次前向，给出 z₁、z₂、h₁、h₂、s、p、L。（3 分）</li>
  <li>用四步链式法则求<b>从 x₂ 到隐藏单元 2 的那个权重</b>的梯度，每一步说明乘的是哪个局部导数。（3 分）</li>
  <li>指出这一步里<b>哪些参数完全不会改变</b>，并解释原因。（2 分）</li>
  <li>更新全部参数后重新跑前向，给出新的 p。（2 分）</li>
</ol>
</div>
<details><summary>第 22 题 · 参考答案</summary>
<div class="eq">(1) z₁ = 0.5(1) + (−0.2)(3) + 0.1 = 0.5 − 0.6 + 0.1 = <b>0</b>   ⇒ h₁ = ReLU(0) = <b>0</b>
    z₂ = (−0.3)(1) + 0.4(3) + 0.2 = −0.3 + 1.2 + 0.2 = <b>1.1</b>  ⇒ h₂ = <b>1.1</b>
    s  = 0.6(0) + 0.5(1.1) − 0.3 = <b>0.25</b>
    p  = σ(0.25) = <b>0.562177</b>        L = −log p = <b>0.575939</b>

(2) 路径 w₂₂ → z₂ → h₂ → s → p → L
    ① ∂L/∂s  = p − y = 0.562177 − 1 = <b>−0.437823</b>   （sigmoid + BCE 的化简）
    ② ∂L/∂h₂ = (∂L/∂s) × v₂ = (−0.437823)(0.5) = <b>−0.218912</b>   （×该单元的输出权重）
    ③ z₂ = 1.1 &gt; 0 ⇒ ReLU 局部导数 = 1 ⇒ ∂L/∂z₂ = <b>−0.218912</b>
    ④ ∂z₂/∂w₂₂ = x₂ = 3 ⇒ <b>∂L/∂w₂₂ = −0.656735</b>
    更新： w₂₂ = 0.4 − 0.5(−0.656735) = <b>0.728368</b>

(4) 其余梯度（都用原参数算）：
    ∂L/∂w₂₁ = −0.218912 × 1 = −0.218912   ∂L/∂b₂ = −0.218912
    ∂L/∂v₂  = (p−y)·h₂ = −0.481606        ∂L/∂c  = p − y = −0.437823
    更新后： 隐藏 2 = [−0.190544, 0.728368]，b₂ = 0.309456
             v₂ = <b>0.740803</b>，c = <b>−0.081088</b>
    重新前向： z₁ 仍 = 0 ⇒ h₁ = 0
               z₂ = −0.190544 + 3(0.728368) + 0.309456 = <b>2.304015</b>
               s = 0.740803(2.304015) − 0.081088 = <b>1.625733</b>
               <b>p = σ(1.625733) = 0.835584</b>   （L 从 0.575939 降到 0.179624）</div>
<p><b>(3) 该写什么。</b><span class="k">隐藏单元 1 的两个权重和它的偏置完全不变</span>：
它的预激活 z₁ = 0，<b>按本课约定 ReLU′(0) = 0</b>，局部导数为零 ⇒ 这条路径的梯度全是 0。
<span class="k">输出层的第一个权重 v₁ = 0.6 也不变</span>：它的梯度 = (p − y)·h₁ = (p − y)×0 = 0。</p>
<p class="lead" style="margin-bottom:0">⚠ 两个容易丢的分：<b>第 ② 步必须说明那个 0.5 是输出权重</b>
（隐藏激活对损失的影响必须穿过输出层）；
<b>算隐藏层梯度时用的是原来的 v₂ = 0.5，不是更新后的 0.740803</b> ——
所有梯度都在同一个参数状态上求值。</p>
</details>""")

A("""<div class="box b">
<div class="h">第 23 题 · 指标、基线与阈值代价（10 分）</div>
<p>某工厂用一个二分类器筛查次品（<b>类别 1 = 次品</b>，预测为正就安排一次人工复检）。
在 300 件产品上，当前阈值给出 <b>TP = 24，FP = 36，FN = 16，TN = 224</b>。</p>
<ol>
  <li>写出公式并计算 accuracy、precision、recall、F1。（4 分）</li>
  <li>把它和「永远预测非次品」的基线比较，说明为什么这里只看 accuracy 会误导。（2 分）</li>
  <li>漏掉一个次品代价 8 个单位、一次不必要复检代价 1 个单位。另一个更低的阈值给出
      TP = 32、FP = 70、FN = 8、TN = 190。哪个阈值更优？若两类错误代价相等呢？（2 分）</li>
  <li>说明应当如何选定并报告这个阈值。（2 分）</li>
</ol>
</div>
<details><summary>第 23 题 · 参考答案</summary>
<div class="eq">(1) 正类 = 次品；FP = 一次不必要的复检，FN = 漏掉一个次品
    自查： 24 + 36 + 16 + 224 = <b>300</b> ✓

    accuracy  = (TP+TN)/N        = (24+224)/300   = <b>0.8267</b>
    precision = TP/(TP+FP)       = 24/60          = <b>0.40</b>
    recall    = TP/(TP+FN)       = 24/40          = <b>0.60</b>
    F1        = 2TP/(2TP+FP+FN)  = 48/(48+36+16)  = 48/100 = <b>0.48</b>

(3) 总代价 = 8·FN + 1·FP
    当前阈值： 8(16) + 36 = <b>164</b>
    更低阈值： 8(8)  + 70 = <b>134</b>   ⇒ <b>更低的阈值更优</b>
    代价相等时 总代价 = FN + FP
    当前阈值： 16 + 36 = <b>52</b>
    更低阈值： 8  + 70 = <b>78</b>       ⇒ <b>结论翻转，当前阈值更优</b></div>
<p><b>(2) 该写什么。</b>基线「全判非次品」在 <b>36 + 224 = 260</b> 个真实负例上全对，
准确率 = 260/300 = <b>0.8667</b> —— <span class="w">比这个模型的 0.8267 还高</span>。
<span class="k">accuracy 被大量负例主导，而且把两类错误一视同仁；
这里漏报（放走一个次品）和误报（多做一次复检）的代价差很远，
所以要看 precision / recall 以及代价加权的总损失。</span>
（基线的 recall = 0，一个次品也找不到，对任务毫无用处。）</p>
<p><b>(4) 该写什么。</b><span class="k">阈值是一个开发决策：用<b>验证数据</b>上的预测分数，
结合应用场景的代价与复检产能来选，选定后<b>冻结</b>，再在没碰过的测试集上评估<b>一次</b>。</span>
<span class="w">⚠ 不要在测试集上反复调阈值</span> —— 那会让测试集参与选择，
报出来的指标就不再是独立的最终估计。并且<b>代价假设变了结论就可能翻转，
不存在普适最优的阈值</b>。</p>
</details>""")

A("""<div class="box b">
<div class="h">第 24 题 · 从分数到 ROC、AUC 与部署（10 分）</div>
<p>五个样本的预测分数与真实标签（分数越大越支持正类）：</p>
<div class="eq">A (0.95, 1)   B (0.70, 1)   C (0.60, 0)   D (0.40, 1)   E (0.20, 0)</div>
<ol>
  <li>把阈值从高到低扫过各个分数，列出 ROC 上的全部点。（3 分）</li>
  <li>用梯形法算 AUC，再用「正负配对法」复核。（3 分）</li>
  <li>取阈值 0.5，给出混淆矩阵与 precision。（2 分）</li>
  <li>该模型要部署到正例只占 2% 的场景。在同样的 TPR 和 FPR 下，说明会发生什么。（2 分）</li>
</ol>
</div>
<details><summary>第 24 题 · 参考答案</summary>
<div class="eq">真实正例 <b>3 个</b>（A、B、D），真实负例 <b>2 个</b>（C、E）
⇒ TPR = TP/3，FPR = FP/2，<b>这两个分母全程固定</b>

(1) 阈值高于 0.95：全判负        ⇒ <b>(0, 0)</b>
    加入 A（正）⇒ 往上          ⇒ <b>(0, 1/3)</b>
    加入 B（正）⇒ 往上          ⇒ <b>(0, 2/3)</b>
    加入 C（负）⇒ 往右          ⇒ <b>(1/2, 2/3)</b>
    加入 D（正）⇒ 往上          ⇒ <b>(1/2, 1)</b>
    加入 E（负）⇒ 往右          ⇒ <b>(1, 1)</b>

(2) 梯形： (1/2 − 0) × (2/3 + 2/3)/2 = 0.5 × 2/3 = <b>1/3</b>
          (1 − 1/2) × (1 + 1)/2     = 0.5 × 1   = <b>1/2</b>
          ⚠ FPR 没有变化的那几段<b>宽度为 0，面积为 0</b>
          AUC = 1/3 + 1/2 = <b>5/6 ≈ 0.8333</b>

    配对（3 正 × 2 负 = 6 对）：
          A&gt;C ✓   A&gt;E ✓   B&gt;C ✓   B&gt;E ✓   D&lt;C ✗   D&gt;E ✓
          <b>5 胜 / 6 对 = 5/6 ≈ 0.8333</b>  ✓ 两法一致

(3) 阈值 0.5 ⇒ 预测为正：A、B、C
          TP = 2（A、B）  FP = 1（C）  FN = 1（D）  TN = 1（E）
          precision = 2/3 ≈ <b>0.667</b>   recall = 2/3   TPR = 2/3，FPR = 1/2</div>
<p><b>(4) 该写什么。</b>在正例占 2% 的场景里，每 1000 个案例约有 <b>20 个正例、980 个负例</b>。
同样的 TPR = 2/3、FPR = 1/2 给出：
<span class="k">TP ≈ 13、FP ≈ 490 ⇒ precision ≈ 13/503 ≈ <b>2.6%</b></span>，
而 recall 仍是 67%。<span class="w">⚠ ROC 和 AUC 用的是「类内条件率」，
单独改变 prevalence 不一定改变 AUC，但 precision 和实际可用性可能变化很大。</span>
所以部署前<b>还要看 precision–recall 与 prevalence</b>，并用<b>验证数据加上误报的真实代价</b>
重新选一个更高的阈值，然后在没碰过的测试集上评估一次。</p>
<p class="lead" style="margin-bottom:0">⚠ 这一题最容易丢的分是第 (2) 问只写一个数字。
<b>两种算法都要写，并点出它们互相验算</b>；另外记得说明<b>竖直段面积为零</b>。</p>
</details>""")

A("""<div class="box y" style="margin-top:26px">
  <div class="h">批改之后</div>
  <p style="margin-bottom:0">把丢分按<b>三类</b>归档：<span class="k">① 算错</span>（回去重练对应的手算模板）、
  <span class="n">② 记号/约定错</span>（回 T1 册的记号表和 T2 的激活表）、
  <span class="w">③ 措辞不到位</span>（回本包的答题模板和英文句库）。
  ⚠ 第 ③ 类在开卷考里是最值钱的 —— 它不需要你多记东西，只需要把句式抄熟。</p>
</div>""")

# ═════════════════════ 落盘 ═════════════════════
NAV = ('<nav><div class="in">'
       '<a href="#plan">计划</a><a href="#pace">配速</a>'
       '<a href="#t1">T1 基础</a><a href="#t2">T2 训练</a><a href="#t3">T3 评估</a>'
       '<a href="#py">Python</a><a href="#en">英文句库</a><a href="#trap">陷阱</a>'
       '<a href="#tpl">答题模板</a><a href="#mcq">模拟·选择</a><a href="#erq">模拟·大题</a>'
       '<button id="themeBtn" title="切换主题">☾</button>'
       '<button onclick="window.print()">打印</button>'
       '</div></nav>')

JS = """<script>
(function(){
  var r=document.documentElement, b=document.getElementById('themeBtn');
  var saved=null; try{saved=localStorage.getItem('m3kit-theme');}catch(e){}
  if(saved) r.setAttribute('data-theme',saved);
  function now(){ return r.getAttribute('data-theme') ||
    (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); }
  function paint(){ b.textContent = now()==='dark' ? '☀' : '☾'; }
  b.onclick=function(){ var t = now()==='dark'?'light':'dark';
    r.setAttribute('data-theme',t); try{localStorage.setItem('m3kit-theme',t);}catch(e){} paint(); };
  paint();
})();
</script>"""

doc = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
       '<title>ARTI2001 Module 3 备考包 · 速查表与模拟卷</title>\n'
       + css + '\n</head>\n<body>\n\n' + NAV + '\n\n<div class="wrap">\n\n'
       + "\n\n".join(B)
       + '\n\n</div>\n' + JS + '\n</body>\n</html>\n')

io.open(OUT, "w", encoding="utf-8").write(doc)
print("→ %s（%.0f KB，%d 道选择题 + 4 道大题）"
      % (os.path.basename(OUT), len(doc.encode("utf-8")) / 1024, len(MCQ)))
