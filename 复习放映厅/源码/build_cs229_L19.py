# -*- coding: utf-8 -*-
"""CS229 讲座 L19 · 奖励模型与线性动态系统（LQR）—— 2026-10-15 新做。

接 L18。L18 的拟合值迭代很通用，但要采样、要拟合、不保证收敛。
这一讲先给 MDP 框架做两个推广（state-action 奖励、有限时域），
再讲一个漂亮的特例：模型线性 ＋ 奖励二次型 ⇒ 最优策略有精确闭式解。

⚠ 时间码全部用 源码/tools/retime.py 的字符位置插值反查过（L19 的 timed 只覆盖 12.3%）。
   不要用 find_quote.py。见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹且写成一行；LaTeX 两个反斜杠
  · note 的 y ≤ 405；matrix 底边 = y+(rows-1)*ch+(ch-3)；boxNode 底边 = y+h，都要 ≤ 405
  · curve(pts,cls) 内部已加 "fit "；fn() 只算点不画线；axes 认 x0/x1/y0/y1
  · ⚠ 补充镜里用到的辅助函数，主文件必须定义（2026-10-15 L18 漏了 grid() 整片抛错）
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
var CFG={title:"CS229 讲座 L19 · 奖励模型与线性动态系统",
  subtitle:"state-action 奖励 · 有限时域 · LQR · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=0rt2CsEQv6U&t="};

function says(ts,en,y){
  note("🎙 Ng "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 网格世界 ── */
function grid(x0,y0,cw,ch,cols,rows,cb){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++){
    var v=cb(i,j); if(v===null) continue;
    boxNode(x0+i*cw, y0+j*ch, cw-6, ch-6, v[0], v[1]||"");}}

/* ── 时间轴：n 个刻度，cb(i) 返回标签 ── */
function timeline(x0,x1,y,n,cb){
  curve([[x0,y],[x1,y]],"d");
  var i;
  for(i=0;i<n;i++){
    var x=x0+(x1-x0)*i/(n-1);
    curve([[x,y-9],[x,y+9]],"d");
    var lb=cb(i); if(lb) note(lb,x,y-20,"y");}}

/* ── 抛物线（画二次型代价）── */
function parab(cx,cy,w,h,cls,up){
  return fn(function(x){var t=(x-cx)/(w/2);
    return up ? cy-h*t*t : cy+h*t*t;}, cx-w/2, cx+w/2, 70);}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讲座 L19","奖励模型与线性动态系统",
      "一个漂亮的特例");},
    "L18 给出了拟合值迭代——<b>它很通用，不管模型什么形状、奖励什么样都能用。</b><b>⚠ 但代价也实在：要采样估期望、要拟合、而且不保证收敛。</b><br><b>这一讲分两段。</b><br><b>前半段给 MDP 框架做两个推广，都是很实用的小改动。</b><b>第一个是让奖励依赖于动作</b>——<b>写成 R(s, a) 而不是 R(s)</b>，<b>这样才能表达「不同动作代价不同」</b>（机器人原地不动比移动省电，直升机猛拉操纵杆该罚）。<b>第二个是有限时域</b>：<b>用一个固定的步数 T 代替折扣因子 γ</b>。<b>⭐ 它会带来一个意外的后果——最优动作开始依赖「现在几点」。</b><br><b>后半段是这一讲的主角：线性二次型调节，简称 LQR。</b><b>Ng 一上来就把分寸说清楚了：LQR 只适用于相当小的一类问题。</b><br><b>⭐ 但在它适用的地方，它好得惊人：如果模型是线性的、奖励是二次型的，那么最优价值函数恰好是一个二次函数，而最优动作恰好是状态的线性函数——都有精确的闭式解。</b><br><b>⚠ 不用采样、不用拟合、不用迭代到收敛。</b><b>这就是为什么值得为它单开一讲。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from l19_shots import EXTRA

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


import l19_gen, l19_lqr
from l19_more import add_more
l19_gen.add(KP)     # R(s,a) → 有限时域 → 非平稳策略 → 倒着算的动态规划
l19_lqr.add(KP)     # LQR 的设定与两个假设 → 线性化 → 关键性质 → 倒推 → 线性最优动作
add_more(KP)        # 完整算法 / 没有任何近似 / π* 不依赖噪声 / Φ 的递推结构 / 三讲对照

C.append(r'''KP("完 · 两个推广与一个特例",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 L19 · 完","奖励模型与 LQR",
      "适用面换来了精确解");},
    "收一下。这一讲是两个推广加一个特例。<br><b>推广一：把奖励从 R(s) 换成 R(s, a)。</b><b>⭐ 动机是「不同动作的代价不同」</b>，Ng 举了好几个例子：<b>网格机器人原地不动可以给 0，移动给一点负奖励，因为移动要耗电</b>；<b>开直升机时，猛拉操纵杆应该被罚更高的代价，因为那会让机身颠簸</b>；<b>导航时不同路段因为限速和拥堵而代价不同</b>；<b>工厂维护时「派人检修」和「什么都不做」的代价也不一样</b>。<b>⚠ 算法几乎不用改：值迭代照样能用，最优动作仍然是那个 argmax，只是 R 现在跟着 a 一起进了括号。</b><br><b>推广二：有限时域 MDP。</b><b>用一个固定的步数 T 代替折扣因子 γ</b>——<b>这个 MDP 只跑 T 步就结束</b>。<b>⚠ Ng 说这时通常就不必再折扣了</b>（γ 的作用之一本来就是保证无限过程不发散，而有限时域天然不会发散）。<br><b>★★★ 它带来一个意外后果：最优动作会依赖「现在是第几步」。</b>直觉很好理解——<b>还剩 100 步时，值得花几步绕远路去拿那个大奖励；而只剩 2 步时，就只能抓眼前够得着的</b>。<b>这种随时间变化的策略有个专门名字：非平稳策略。</b><b>⭐ 对照 L17：那里的策略是平稳的，π(s) 只看状态不看时钟。</b><b>⚠ 既然已经非平稳了，顺手还能让转移概率和奖励也随时间变</b>（写成 P_t 和 R_t）——Ng 举的例子是<b>工厂 24 小时运转时，不同时段的人力成本和故障概率都不一样</b>。<br><b>解有限时域 MDP 的办法是动态规划，而且是倒着算的</b>：<b>先算最后一步的 V*_T，再用它算 V*_{T−1}，一路倒推回第 0 步</b>。<b>⭐ 为什么能倒着算：最后一步没有未来，它的最优值直接就是即时奖励的最大值，不依赖任何别的东西——这就是递推的起点。</b><br><b>然后是 LQR。⚠ Ng 开门见山地说它只适用于相当小的一类问题，这个分寸要先立住。</b><b>它的设定是：状态是 n 维实向量、动作是 d 维实向量</b>，再加两个关键假设。<br><b>假设一，动力学是线性的</b>：<b>s_{t+1} = A·s_t + B·a_t + w_t</b>，<b>w_t 是高斯噪声</b>（⭐ 呼应 L18 那条教训——模拟器要带随机性）。<b>A 和 B 怎么来？两条路：从数据里做线性回归学出来（就是 L18 讲的那个），或者把一个非线性模型在某个工作点附近线性化</b>（⭐ <b>就是泰勒展开取一阶</b>）。<br><b>假设二，奖励是二次型的</b>：<b>R(s, a) = −(sᵀU s + aᵀV a)</b>，<b>其中 U、V 都是半正定矩阵</b>。<b>⭐ 取 U、V 为单位阵时它就变成 −(‖s‖² + ‖a‖²)</b>——<b>含义是「同时惩罚状态偏离 0 和动作用力过大」</b>，这正是「把系统稳在原点、而且别太费劲」这个目标的数学写法。<br><b>★★★ 然后是那个 remarkable 的性质：在这两个假设下，V* 恰好是一个二次函数。</b><b>推导是倒着做的动态规划。</b><b>基准情形很漂亮：最后一步因为 V 半正定，aᵀV a 总是非负的，而奖励前面有负号，所以最优动作就是「什么都不做」——取 a = 0</b>，于是 <b>V*_T(s) = −sᵀU s</b>，正是二次型。<b>归纳步骤：假设 V*_{t+1} 是二次的，代进去做一堆代数之后，V*_t 仍然是二次的</b>——<b>形式由两个量 Φ_t 和 Ψ_t 决定，而它们可以从 Φ_{t+1}、Ψ_{t+1} 递推出来。</b><br><b>★★★ 最精彩的结论是：最优动作是状态的线性函数，π*_t(s_t) = L_t · s_t。</b><b>⚠ Ng 特意澄清了一句：这不是说「你拟合一条直线去近似最优动作」，而是说最优动作本身精确地就是线性的</b>——<b>这是推导出来的结果，不是近似。</b><br><b>⇒ 所以实现 LQR 时，你只要倒着递推出那一串矩阵 L_t，运行时每一步做一次矩阵乘法就行了。</b><b>没有采样、没有拟合、没有收敛判据。</b><br><b>⭐ 把这一讲和 L18 放在一起看，是一个很典型的权衡：拟合值迭代什么都能做但什么都做得粗；LQR 只能做一小类问题，但做得精确又高效。</b><b>工程上的常见套路正是——先把问题尽量化成 LQR 能吃的形状（线性化 + 二次型代价），实在不行再上通用方法。</b><br><b>下一讲 L20 转向一个完全不同的话题：强化学习做不出效果时，怎么诊断到底是哪一环出了问题。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讲座 L19 · 奖励模型与线性动态系统</title>")
io.open("cs229-L19.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-L19.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ l19_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
