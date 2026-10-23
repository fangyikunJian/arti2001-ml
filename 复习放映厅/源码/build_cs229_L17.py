# -*- coding: utf-8 -*-
"""CS229 讲座 L17 · MDP 的解法：值迭代与策略迭代 —— 2026-10-15 新做。

接 L16。L16 把问题形式化成了 MDP 五元组，并留了个悬念：
网格世界里 −1 陷阱旁边那格，往北还是往西？这一讲把它真正算出来（0.740 对 0.676）。

⚠ 时间码全部用 scratchpad/retime.py 的「字符位置插值」反查过。
   不要用 find_quote.py —— L17 的 timed 只覆盖正文 12.0%，它的行号法会偏上百秒。
   见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹，**且必须写成一行**（JS 字符串不能跨行，否则整片打不开）
  · LaTeX 在源码里写两个反斜杠
  · note 的 y 上限 405；matrix 的 rect 底边 = y+(rows-1)*ch+(ch-3)，也要 ≤405
  · curve(pts,cls) 内部已加 "fit "，cls 只传 "b"/"y"/"r"
  · fn() 只算点不画线，要套 curve(fn(...))
  · axes 认 x0/x1/y0/y1（y0 是底、y1 是顶）
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
var CFG={title:"CS229 讲座 L17 · MDP 的解法",
  subtitle:"价值函数 · Bellman 方程 · 值迭代与策略迭代 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=d5gaWTo6kDM&t="};

function says(ts,en,y){
  note("🎙 Ng "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── 网格世界：cols×rows 个格子，cb(i,j) 返回 [文字, 类名]，null 跳过 ── */
function grid(x0,y0,cw,ch,cols,rows,cb){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++){
    var v=cb(i,j); if(v===null) continue;
    boxNode(x0+i*cw, y0+j*ch, cw-6, ch-6, v[0], v[1]||"");}}

/* ── 一条收敛曲线（误差按比例下降）── */
function decay(x0,x1,ybase,amp,k){
  return fn(function(x){return ybase-amp*Math.exp(-k*(x-x0)/(x1-x0));},x0,x1,90);}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讲座 L17","MDP 的解法",
      "把上一讲那个悬念算出来");},
    "上一讲把「学开直升机」这类问题形式化成了 <b>MDP 五元组：S、A、P_sa、γ、R</b>，<b>并说算法最终要交出的是一个策略 π</b>。<br><b>但怎么把那个策略算出来，一个字都还没讲。</b>这一讲补上。<br><b>⭐ 它还会兑现一个具体的悬念。</b>L16 结尾时 Ng 指着网格世界里 −1 陷阱旁边那一格说：<b>往北还是往西，其实并不显然</b>——往北快但可能滑进陷阱，往西安全但路更长。<b>他当时说「这个光用眼睛看是看不出来的」。</b><br><b>这一讲会把两个数真正算出来：往西 0.740，往北 0.676。</b><br><b>路线是三步。</b>先定义<b>价值函数</b>——<b>它回答「待在某个状态有多好」</b>；再推出 <b>Bellman 方程</b>，它把这个问题变成一组可解的方程；最后给出两个算法：<b>值迭代</b>和<b>策略迭代</b>。<br><b>⚠ 最后还有一段很实际的内容</b>：<b>前面一直假装 P_sa 是已知的，可现实里它从哪来？</b>以及<b>一个光靠「每次都选当前最优」会掉进去的坑</b>。");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]

from l17_shots import EXTRA

def KP(name, shots, summ, quiz, t=0):
    # 后补的第二镜按标题查表追加（见 l17_shots.py），避免回去改十几处调用
    extra = EXTRA.get(name)
    if extra:
        shots = list(shots) + [extra]
        EXTRA.pop(name)          # 用过即删，收尾时好检查有没有键名写错
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


# ══════════════ 各部分分文件写 ══════════════
import l17_value, l17_iter, l17_learn, l17_more
l17_more.add_roadmap(KP)   # 路线图：V^π → V* → π*（要在三个定义之前）
l17_value.add(KP)          # 枚举策略为何不行 → V^π → Bellman → 线性方程组 → V* → π*
l17_more.add_optimal(KP)   # π* 的同时最优性（紧跟在 argmax 之后）
l17_iter.add(KP)           # 值迭代 → 同步/异步 → 收敛 → 0.740 对 0.676 → 策略迭代 → 怎么选
l17_more.add_tail(KP)      # 收敛性证明在哪 / 有限步停止 / 连续状态预告
l17_learn.add(KP)          # 学 P_sa → 没见过怎么办 → 完整算法 → 探索 vs 利用 → ε-greedy

# ══════════════ 收尾 ══════════════
C.append(r'''KP("完 · 从一个 MDP 到一个能跑的算法",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 L17 · 完","MDP 的解法",
      "价值函数 → Bellman → 值迭代 → 真正的算法");},
    "收一下。<b>出发点是一个很实际的困难：策略的数量是组合爆炸的。</b>Ng 算给你看——<b>11 个状态、每个状态 4 个动作，就有 4¹¹ 种策略</b>，而<b>一般是「动作数的状态数次方」</b>。<b>⇒ 枚举是没指望的，必须换一条路。</b><br><b>那条路是价值函数。</b><b>V^π(s) 的定义是：从状态 s 出发、一路按 π 行动，能拿到的期望总回报。</b>⭐ <b>它把「策略好不好」这个笼统问题，变成了每个状态上的一个数。</b><br><b>★★★ 核心是 Bellman 方程</b>：<b>V^π(s) = R(s) + γ · E[V^π(s′)]</b>——<b>当前状态的价值 ＝ 立刻拿到的奖励 ＋ 折扣后的未来期望价值</b>。⭐ <b>它的威力在于把一个「无限长的未来」压缩成了「一步 + 剩下的价值」</b>，而剩下的价值也满足同样的方程。<br><b>⇒ 于是 11 个状态给出 11 个方程、11 个未知数，这是一个线性方程组，可以直接解。</b><br><b>然后是两种价值函数，⚠ Ng 专门说这是术语上最容易混的地方</b>：<b>V^π 是某个具体策略的价值</b>（那个策略可能很烂），<b>V* 是最优价值函数</b>，定义成<b>所有策略里取最大</b>。<b>V* 的 Bellman 方程里多了一个 max</b>——因为你可以挑动作。<b>⭐ 有了 V*，最优策略就是一个 argmax：在每个状态挑那个让期望未来价值最大的动作。</b><br><b>值迭代</b>：<b>把所有状态的价值初始化为 0，然后反复用 Bellman 方程更新</b>。⚠ <b>同步更新</b>是算完全部 11 个再一起替换，<b>异步更新</b>是算一个就立刻覆盖一个；<b>两种都收敛，多数人用异步</b>。<b>收敛很快</b>：<b>γ=0.9 时几十次迭代就很接近了，γ=0.99 时要几百次</b>。<br><b>⭐ 算完 V* 再用 argmax，就兑现了上一讲的悬念</b>：那一格<b>往西的期望未来回报是 0.8×0.75 + 0.1×0.69 + 0.1×0.71 = 0.740</b>，<b>往北是 0.8×0.69 + 0.1×0.75 + 0.1×0.49 = 0.676</b>。<b>往西明显更高 ⇒ 绕路才是对的。</b>⚠ Ng 补了一句严谨的：<b>实际上四个方向都要算一遍再比。</b><br><b>策略迭代</b>换了个焦点：<b>盯着策略而不是价值函数</b>。<b>随便初始化一个 π，解线性方程组得到 V^π，再把 V^π 当成最优的来更新 π，如此反复</b>。<b>它在有限步内就会停止变化。</b><br><b>⚠ 怎么选</b>：<b>策略迭代每轮都要解一次线性方程组</b>，<b>状态只有十几个到几百个时很快</b>；<b>状态一多，解方程组就成了瓶颈，Ng 说他会偏向值迭代</b>。<br><b>最后两件很实际的事。</b>其一，<b>P_sa 现实里是估出来的</b>：<b>让机器人按某个策略跑一阵，然后数次数</b>——<b>在 s 做 a 后到达 s′ 的次数，除以在 s 做 a 的总次数</b>。<b>这就是极大似然估计。</b>⚠ <b>没试过的动作会出现 0/0</b>，常见做法是<b>假定它等概率通向任意状态（1/11）</b>；也可以用拉普拉斯平滑，<b>但 Ng 说 MDP 的解法对 0 概率不像朴素贝叶斯那么敏感，所以实践中不常用</b>。<br><b>⚠⚠ 其二是探索与利用。</b>上面那套算法是<b>纯粹贪心的</b>——<b>永远按当前估计的最优去走</b>。<b>后果是：它可能一辈子都发现不了角落里那个 +10 的宝藏，因为它从没去过那儿。</b>Ng 用在线广告平台做类比：<b>纯利用就是只推你最可能点的广告</b>，<b>而适当探索才能发现你自己都没意识到的兴趣</b>。<b>常用的办法是 ε-greedy：每一步以 90% 的概率照当前最优走，10% 的概率随便走一步。</b>⭐ <b>Ng 还吐槽这个名字起反了——ε 是「随机」的概率而不是「贪心」的概率，叫 1−ε greedy 才对。</b><br><b>下一讲 L18 处理一个这一讲回避了的前提：状态是连续的怎么办。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讲座 L17 · MDP 的解法</title>")
io.open("cs229-L17.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-L17.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
if EXTRA:
    print("  ⚠ l17_shots.py 里这些键没对上任何知识点（标题写错了？）：", list(EXTRA))
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
