# -*- coding: utf-8 -*-
"""CS229 讲座 L18 · 连续状态 MDP 与模型模拟 —— 2026-10-15 新做。

接 L17。L17 全程假设状态有限，末尾留了一句「连续状态怎么办，下一讲讲」。
这一讲先说离散化（为什么能用、什么时候就不能用了），再给出真正的办法：
拟合值迭代 —— 用线性回归去近似价值函数。

⚠ 时间码全部用 scratchpad/retime.py 的字符位置插值反查过（L18 的 timed 只覆盖 11.5%）。
   见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹且写成一行；LaTeX 两个反斜杠
  · note 的 y ≤ 405；matrix 的 rect 底边 = y+(rows-1)*ch+(ch-3) 也要 ≤ 405
  · boxNode 的底边 = y+h，同样 ≤ 405
  · curve(pts,cls) 内部已加 "fit "；fn() 只算点不画线；axes 认 x0/x1/y0/y1
"""
import io, sys, re as _re
sys.stdout.reconfigure(encoding="utf-8")
head = io.open("eng.txt", encoding="utf-8").read()
def js(t): return '"' + t.replace('\\','\\\\').replace('"','\\"') + '"'
C = []

C.append(r'''(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng;
var clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
var CFG={title:"CS229 讲座 L18 · 连续状态 MDP 与模型模拟",
  subtitle:"离散化的极限 · 模拟器 · 拟合值迭代 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=QFu5nuc-S0s&t="};

function says(ts,en,y){
  note("🎙 Ng "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 阶梯函数（画离散化的那个比喻）── */
function stair(x0,x1,y0,y1,n){
  var p=[],i;
  for(i=0;i<n;i++){
    var xa=x0+(x1-x0)*i/n, xb=x0+(x1-x0)*(i+1)/n;
    var yy=y0+(y1-y0)*(i+0.5)/n;
    p.push([xa,yy]); p.push([xb,yy]);
    if(i<n-1) p.push([xb,y0+(y1-y0)*(i+1.5)/n]);}
  return p;}

/* ── 网格世界：cols×rows 个格子，cb(i,j) 返回 [文字, 类名]，null 跳过 ──
   ⚠ 2026-10-15：补充镜里用了 grid() 但主文件忘了定义，整片在第一个用到它的
     帧上抛 ReferenceError。静态体检查不出来，是浏览器实扫抓到的。 */
function grid(x0,y0,cw,ch,cols,rows,cb){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++){
    var v=cb(i,j); if(v===null) continue;
    boxNode(x0+i*cw, y0+j*ch, cw-6, ch-6, v[0], v[1]||"");}}

/* ── 网格（画离散化切格子）── */
function mesh(x0,y0,x1,y1,n){
  var i;
  for(i=0;i<=n;i++){
    var x=x0+(x1-x0)*i/n, y=y0+(y1-y0)*i/n;
    curve([[x,y0],[x,y1]],"d"); curve([[x0,y],[x1,y]],"d");}}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讲座 L18","连续状态 MDP 与模型模拟",
      "11 个格子变成无穷多个");},
    "L17 把 MDP 彻底解决了——<b>但那一整套方法从头到尾都建立在一个前提上：状态只有有限多个。</b><br><b>11 个方程 11 个未知数、对每个状态遍历更新、解线性方程组——每一步都需要能把状态一个个数过来。</b><br><b>⚠ 而真实问题几乎都不是这样。</b>一辆车的状态是<b>位置、朝向、速度</b>，一架直升机还要加上<b>三个姿态角</b>，<b>这些全是实数，有无穷多种取值</b>。<br><b>这一讲给两条路。</b><br><b>第一条是离散化</b>：<b>把连续空间切成格子，每格当一个状态，退回 L17 的框架</b>。<b>⭐ 它简单、好使，在低维问题上完全够用</b>——<b>但有一个会要命的毛病，维度一高就彻底崩。</b><br><b>第二条是这一讲真正的主角：拟合值迭代。</b><b>它绕开离散化，直接去近似那个价值函数</b>——<b>用的工具你早就学过，就是线性回归。</b><br><b>⚠ 中间还要补一个 L17 没提过的零件：模拟器。</b><b>它是「模型化强化学习」的核心，而 Ng 会讲一个很硬的实战教训：模拟器做成确定性的，学出来的策略在视频里很好看，搬上真机就废。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from l18_shots import EXTRA
from l18_shots2 import EXTRA2
EXTRA.update(EXTRA2)      # 分两批补的第二镜，合并成一张表

def KP(name, shots, summ, quiz, t=0):
    extra = EXTRA.get(name)
    if extra:
        shots = list(shots) + [extra]
        EXTRA.pop(name)
    _kpn[0] += 1
    n = _kpn[0]
    nm = '%d · %s' % (n, _re.sub(r'^\s*\d+\s*·\s*', '', name))
    b=['KP(%s,function(){'%js(nm)]
    for scene,narr,sec in shots:
        b.append('  S(%d,function(){%s},%s);'%(sec,scene,js(narr)))
    fields=",".join('%s:%s'%(k,js(v)) for k,v in summ.items() if v and k!='kp')
    b.append('  SUM(%d,%d,{%s});'%(t,n,fields))
    quiz = fix_quiz(quiz, n)
    opts=",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(%d,%d,{t:%s,o:[%s],a:%d,w:%s});'%(t,n,js(quiz['t']),opts,quiz['a'],js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))


import l18_disc, l18_model, l18_fvi
from l18_shots import add_more
l18_disc.add(KP)    # 连续状态长什么样 → 离散化 → 阶梯毛病 → 维数灾难 → 何时够用
add_more(KP)        # 状态里放什么是你的选择 / 运动学vs动力学 / 倒立摆 / 为何需要模拟器
l18_model.add(KP)   # 直接近似 V* → θᵀφ(s) → 模拟器 → 物理引擎 → 从数据学 → 确定性的坑
l18_fvi.add(KP)     # 选特征 → 数据便宜 → 拟合值迭代 → 采样估期望 → 拟合 → 实际怎么用

C.append(r'''KP("完 · 从格子到函数",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 L18 · 完","连续状态 MDP",
      "离散化的极限 · 模拟器 · 拟合值迭代");},
    "收一下。<b>问题的起点是：L17 的全部方法都要求能把状态一个个数过来，而真实系统的状态是连续的。</b>Ng 给的三个例子很具体：<b>车要记位置、朝向和速度；直升机要记 x、y、z 三个位置，加上 roll、pitch、yaw 三个姿态角，再加上它们的变化率；倒立摆是一个四维状态空间</b>（小车的位置和速度、杆的角度和角速度）。<br><b>第一条路是离散化</b>：<b>把每一维切成若干段，每个格子当一个状态</b>，于是退回 L17 的框架。<b>⚠ 但它有两个毛病。</b><b>其一，它把价值函数表示成了阶梯</b>——Ng 的类比是<b>用阶梯去拟合房价随面积的变化</b>，<b>明明是一条光滑的曲线，你却只能用一段段平台去凑</b>；想更准就得切得更细。<b>⚠⚠ 其二就是切得更细的代价：如果状态空间是 n 维、每一维切成 k 段，总状态数是 k 的 n 次方。</b>Ng 举的数是<b>每维只切 10 段，就已经是 10 的 n 次方，随维度指数增长</b>。<b>⇒ 这就是维数灾难。</b><br><b>⭐ 但分寸要讲清楚：Ng 并不否定离散化。</b>他明确说<b>低维问题用它完全没问题——二维很轻松，四维的倒立摆也还行</b>。<b>它简单、容易实现、而且在小问题上效果不错。</b><b>⇒ 真正的问题出在更高的维度上。</b><br><b>第二条路是直接近似 V*，不经过离散化。</b>做法是<b>把 V*(s) 写成 θᵀφ(s)</b>——<b>φ(s) 是你为状态设计的特征，θ 是要学的参数</b>。<b>⭐ 这正是线性回归的形状</b>：<b>线性回归用特征去预测房价，这里用特征去预测「从这个状态出发能拿多少」</b>。<br><b>⚠ 但要先补一个零件：模型（也叫模拟器）。</b><b>它就是一个函数：输入当前状态和动作，输出下一个状态。</b><b>⭐ 有两条途径。</b><b>一是物理引擎</b>——<b>翻物理书推出运动方程，或者直接用开源物理引擎，填进尺寸和质量就能跑</b>。<b>二是从数据里学</b>：<b>让机器人（哪怕是随机地）动一阵，记下每一刻的状态和动作，然后用线性回归拟合 s_{t+1} ≈ A·s_t + B·a_t</b>。⭐ <b>Ng 点明这等价于做 n 次线性回归，每次预测状态向量的一个分量。</b><br><b>⚠⚠ 这里有一条很硬的实战教训。</b><b>模型可以做成确定性的（输出一个确定的 s′），也可以做成随机的（再加一个高斯噪声项）。</b>Ng 说<b>用确定性模拟器，强化学习算法往往学出一个很脆弱的策略——在模拟器里完美，到真机上就不行</b>。<b>⭐ 根子在于「模拟器永远不可能 100% 准确」</b>，<b>而一个能在带噪声的模拟器里站住的策略，迁移到真实世界的胜算要大得多</b>。<b>⇒ 他的建议很直接：想让 model-based RL 在真机上能用，就把模拟器做成随机的。</b><br><b>最后是拟合值迭代本身。</b><b>第一步选特征 φ(s)</b>——<b>Ng 提示：价值函数衡量的是「机器人从这儿开始能做得多好」，所以挑那些能反映「现在情况好不好」的量</b>，比如倒立摆里<b>杆的角度乘以小车的速度</b>这种交互项，<b>因为杆倒向右边这件事是好是坏，取决于小车是不是正在往右追</b>。<b>⭐ 而且 model-based RL 有个便宜可占：数据是模拟器生成的，要多少有多少</b>，<b>所以不必像平时那样死抠特征数量、担心过拟合</b>。<br><b>算法本身是「值迭代 + 监督学习」的缝合</b>：<b>先采样 m 个状态；对每个状态的每个动作，用模拟器采 k 次下一状态，取 V 的平均值来估那个期望</b>（⭐ <b>这一步是关键——连续状态没法把所有 s′ 加起来，只能采样估计</b>）；<b>再对动作取 max 得到目标值 y_i</b>；<b>最后用监督学习把 θ 拟合到这些 (s_i, y_i) 上</b>。<br><b>⚠ 注意最后一步和 L17 的根本差别：L17 是「把算出来的值直接写进表格」，这里是「把算出来的值当成训练数据去拟合一个函数」。</b><b>⭐ 这正是「拟合」两个字的来源，也是它能处理无穷多个状态的原因——你不再需要为每个状态存一个数，只需要存一组 θ。</b><br><b>下一讲 L19 继续往下：当模型是线性的、奖励是二次型时，有一个漂亮得多的精确解法，叫 LQR。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讲座 L18 · 连续状态 MDP 与模型模拟</title>")
io.open("cs229-L18.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-L18.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ l18_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
