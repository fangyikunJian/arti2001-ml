# -*- coding: utf-8 -*-
"""CS229 讨论课 · 学习理论 —— 2026-10-16 新做。CS229 片子的最后一块。

这是助教的讨论课，不是 Ng 的正课，所以引文标的是「讨论课」而不是「Ng」。
它把正课里的偏差-方差讲得更深：从**参数视角**看（采样分布是否以真参数为中心），
再走到误差三分解、经验风险最小化、Hoeffding 不等式与一致收敛。

⚠ 时间码全部用 源码/tools/retime.py 的字符位置插值反查过（timed 只覆盖 13.0%）。
   见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹且写成一行；LaTeX 两个反斜杠
  · note 的 y ≤ 405；matrix 底边 = y+(rows-1)*ch+(ch-3)；boxNode 底边 = y+h，都 ≤ 405
  · says() 默认 y=150，文字框约 [137,169]，紧跟其下的 note 至少 y≥178
  · 补充镜用到的辅助函数，主文件必须定义
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
var CFG={title:"CS229 讨论课 · 学习理论",
  subtitle:"参数视角的偏差方差 · 误差三分解 · 一致收敛 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=iVOxMcumR4A&t="};

/* ⚠ 这是助教的讨论课，不是 Ng 的正课，所以标「讨论课」而不是「Ng」 */
function says(ts,en,y){
  note("🎙 讨论课 "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 一团采样分布的点（cx,cy 中心，sd 分散度，n 个点）── */
function cloud(cx,cy,sd,n,cls,seed){
  var r=rng(seed||7), p=[], i;
  for(i=0;i<n;i++){
    var a=r()*Math.PI*2, d=sd*Math.sqrt(r());
    p.push([cx+d*Math.cos(a), cy+d*Math.sin(a)]);}
  dots(p,cls||"b",5);}

/* ── 靶心：真参数 θ* 的位置，外面套几圈 ──
   ⚠ 不能用 fn() 画圆：fn 是按 x 扫的，一个 x 只能有一个 y。圆要自己按角度生成点。*/
function ring(cx,cy,r0,cls){
  var p=[],i;
  for(i=0;i<=72;i++){var a=i/72*Math.PI*2;
    p.push([cx+r0*Math.cos(a), cy+r0*Math.sin(a)]);}
  curve(p,cls||"d");}
function bull(cx,cy,r0){
  ring(cx,cy,r0,"d"); ring(cx,cy,r0*0.62,"d");
  dots([[cx,cy]],"r",7);}

/* ── 一条衰减曲线 ── */
function decay(x0,x1,ybase,amp,k){
  return fn(function(x){return ybase-amp*Math.exp(-k*(x-x0)/(x1-x0));},x0,x1,90);}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讨论课","学习理论",
      "把偏差方差讲到底");},
    "这是一节助教主持的讨论课，专门补深正课里的学习理论。<b>它的开场就说明了路线：先框定学习问题，然后深入偏差-方差权衡，再讲经验风险最小化，最后花不少时间在一致收敛和 VC 维上。</b><br><b>⭐ 它最值钱的地方，是用一个和正课完全不同的角度重讲偏差和方差。</b><br><b>你在正课里见过的多半是那张「欠拟合 / 过拟合」的曲线图——模型太简单就欠拟合，太复杂就过拟合。</b><b>⚠ 那张图很直观，但它讲不清「偏差」和「方差」到底是什么量。</b><br><b>这节课换成参数视角：想象你把整个训练过程重复无数次，每次用一批新数据，得到一个 θ̂。</b><b>这些 θ̂ 会形成一个分布。</b><b>⭐ 于是偏差就是「这团分布有没有以真参数为中心」，方差就是「这团分布有多散」——两个都变成了可以精确说清楚的量。</b><br><b>后半段会把泛化误差拆成三块，再用 Hoeffding 不等式和 union bound 证明：只要假设类不太大、数据不太少，训练误差小就意味着泛化误差也小。</b>");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]
from ds_shots import EXTRA
from ds_shots2 import EXTRA2
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


import ds_bias, ds_erm
from ds_shots import add_more
ds_bias.add(KP)   # 参数视角 → 偏差/方差的定义 → 方差随 m 降 → 效率与一致性 → 三个 h → 误差分解
ds_erm.add(KP)    # 经验风险 vs 风险 → ERM → Hoeffding → 一致收敛 → union bound → 样本复杂度 → VC
add_more(KP)      # 数据生成过程 / 假设类的例子 / 这需要慢慢想 / 一致收敛的几何 / 四步链 / 适用边界
from ds_shots2 import add_last
add_last(KP)      # g 到底是什么：不受假设类限制的最优假设

C.append(r'''KP("完 · 从直觉到可证明的保证",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 讨论课 · 完","学习理论",
      "偏差方差 · 三分解 · 一致收敛");},
    "收一下。这节讨论课做的事，是把正课里几个靠直觉理解的概念，换成可以精确说清、甚至可以证明的东西。<br><b>★★★ 第一件是用参数视角重讲偏差和方差。</b><b>设想把整个训练过程重复无数次，每次喂一批新数据，得到一个 θ̂——这些 θ̂ 构成一个「采样分布」。</b><b>⭐ 于是：偏差问的是「这个采样分布有没有以真参数 θ* 为中心」，方差问的是「它有多分散」。</b>讨论课点明了一句很精炼的话：<b>偏差和方差本质上就是采样分布的一阶矩和二阶矩的性质</b>——一阶矩是均值（看是否居中），二阶矩就是方差本身。<br><b>⚠ 这个视角比「欠拟合/过拟合」那张图强在哪？强在它能解释那张图解释不了的事。</b>比如<b>参数个数相同的两个算法，偏差和方差可以完全不同</b>——<b>加了正则化，方差就会降下来</b>。<br><b>⭐ 几个和样本量 m 有关的性质</b>：<b>数据越多，方差趋于 0</b>；而<b>方差随 m 下降的速率叫统计效率</b>（有的算法方差按 1/m² 降，有的按 e⁻ᵐ 降）；<b>如果 m 趋于无穷时 θ̂ 收敛到 θ*，这个算法叫「一致的」</b>；<b>而如果对任何 m，θ̂ 的期望都等于 θ*，那叫「无偏的」</b>。⚠ <b>这两件事不一样</b>：一致说的是极限行为，无偏说的是任何样本量下都居中。<br><b>★★ 第二件是把三个假设分清楚。</b><b>g 是最好的可能假设（可能根本不在你的假设类里）；h* 是你的假设类里最好的那个；ĥ 是你用有限数据实际学到的那个。</b><b>⇒ 三者之间的落差，正好对应误差的三块。</b><br><b>★★★ 于是有了误差三分解</b>：<b>不可约误差（无论你用什么假设、有多少数据都去不掉）＋ 近似误差（因为你把自己限定在某个假设类里，比如只用逻辑回归）＋ 估计误差（因为数据有限、算法有脾气）</b>。<b>⭐ 而估计误差还能再拆成估计偏差和估计方差。</b><br><b>⚠ 讨论课点出了一件容易混的事：同一件事有两种拆法。</b><b>「偏差-方差分解」和「近似-估计误差分解」是从两个角度切同一块误差</b>——<b>通常说的「方差」对应估计方差，「偏差」对应近似误差加估计偏差</b>。看到不同教材用不同拆法时，不必以为它们在说不同的事。<br><b>后半段转向可证明的保证。</b><b>先区分两个量：风险（也叫泛化误差）是在整个数据分布上的期望损失，这是个无限的过程；而经验风险是在你手上那有限几个样本上的出错比例。</b><b>★ 然后限定一类算法：经验风险最小化（ERM）——就是「在假设类里挑训练误差最小的那个」。</b>⭐ <b>为什么要限定？因为只有限定了算法，才能推出更强的理论结果。</b><br><b>★★ 工具是 Hoeffding 不等式</b>：它说<b>用 m 个样本估计一个概率时，估计值偏离真值超过 γ 的概率，会随 m 指数级地变小</b>。<b>⇒ 把它用在「某一个假设 h 的经验风险 vs 真实风险」上，就得到了这个 h 的保证。</b><br><b>⚠ 但只保证一个 h 是不够的——ERM 会从整个假设类里挑，而且是挑那个在训练集上看起来最好的，这个「挑」的动作本身就带来风险。</b><b>★★★ 所以要的是一致收敛：假设类里所有的 h 同时都满足那个保证。</b><b>做法是对 K 个假设套 union bound——代价就是把概率界乘上一个 K。</b><br><b>⇒ 由此得到样本复杂度：要达到某个精度和置信度，你需要多少个样本。</b><b>⭐ 结论的形状很值得记：需要的样本数随假设类大小的对数增长。</b><b>是对数，不是线性——所以假设类大一点并不可怕。</b><br><b>最后，讨论课提了 VC 维但没展开：它是用来给「无限大的假设类」也定出一个「尺寸」的概念，衡量这个类有多强的表达能力。</b><b>⚠ 讨论课明说了「今天不讲这个」，所以这里也不假装讲过。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讨论课 · 学习理论</title>")
io.open("cs229-DS.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-DS.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ ds_shots.py 里这些键没对上任何知识点：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
