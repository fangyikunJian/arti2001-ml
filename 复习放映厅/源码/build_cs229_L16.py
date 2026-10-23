# -*- coding: utf-8 -*-
"""CS229 讲座 L16 · ICA 收尾与强化学习开篇 —— 2026-10-15 新做。

这一讲前 49 分钟讲完 ICA（CDF、密度、三种歧义、为什么必须非高斯、学习规则），
49:45 之后开启全课第四大主题：强化学习与 MDP。

⚠ 时间码全部用修好的 find_quote.py 反查过（2026-10-14 修了锚点对齐的 bug，
   修之前它把 50:17 的内容报成 38:10，差 12 分钟）。见 memory/find-quote-anchor-bug.md。

引擎的坑（memory/projector-engine-traps.md）：
  · setEq 必须 $$ 包裹，**且必须写成一行**（JS 字符串不能跨行，否则整片打不开）
  · LaTeX 在源码里写两个反斜杠
  · note 的 y 上限 405
  · fn() 只算点不画线，要套 curve(fn(...))
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
var CFG={title:"CS229 讲座 L16 · ICA 收尾与强化学习开篇",
  subtitle:"为什么 ICA 必须非高斯 · 第四大主题登场 · 空格推进 · N 讲解",
  video:"https://www.youtube.com/watch?v=YQA9lLdLig8&t="};

function says(ts,en,y){
  note("🎙 Ng "+ts+"  «"+en+"»",640,y||150,"g");}

/* ── S 形曲线（当 CDF 用）── */
function sig(cx,cy,w,h,cls){
  var p=[],i;
  for(i=0;i<=80;i++){
    var t=-6+12*i/80, v=1/(1+Math.exp(-t));
    p.push([cx+w*t/12, cy-h*(v-0.5)]);}
  curve(p,cls||"b");}

/* ── 网格世界：cols×rows 个格子，cb(i,j) 返回 [文字, 类名] 或 null（墙）── */
function grid(x0,y0,cw,ch,cols,rows,cb){
  var i,j;
  for(j=0;j<rows;j++)for(i=0;i<cols;i++){
    var v=cb(i,j); if(v===null) continue;
    boxNode(x0+i*cw, y0+j*ch, cw-6, ch-6, v[0], v[1]||"");}}

KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("CS229 讲座 L16","ICA 收尾与强化学习开篇",
      "一讲跨两个世界");},
    "这一讲是全课的一个转折点，<b>前后半场讲的几乎是两门不同的学问。</b><br><b>前半场把 ICA 讲完。</b>L15 已经讲了鸡尾酒会问题——好几个声音混在一起，要把它们拆开。<b>但还欠一个关键问题没答：为什么这件事能做成？</b><br><b>⭐ 答案出人意料地苛刻：只有当信号「不是高斯的」，ICA 才可能成立。</b>这一讲会讲清楚三种「拆不开」的歧义，<b>其中旋转歧义正是高斯会让整件事垮掉的那个原因</b>。<br><b>后半场换一个世界。</b>Ng 说这是本课<b>四大主题里的最后一个：强化学习</b>。<br><b>⚠ 它和前面所有内容最大的不同在于——没有人告诉你正确答案是什么。</b>教直升机飞行时，<b>没有哪个专家能在每一毫秒告诉你操纵杆该推多少</b>。<b>⭐ 你能做的只是说清楚「什么算好、什么算坏」，剩下的让算法自己摸索。</b><br>这一讲会把这个想法形式化成 <b>MDP（马尔可夫决策过程）</b>——它是后面四讲的共同语言。");
});''')

from quizfix import fix_quiz, report as quizreport
_kpn = [0]

def KP(name, shots, summ, quiz, t=0):
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


# ══════════════ ICA 回顾 ══════════════
KP("回顾：鸡尾酒会问题要解什么",
 [(r'''clearScene();setEq(null);setCap("混进去容易，拆出来难");
   boxNode(120,195,230,66,"声源 s","g");
   boxNode(500,195,280,66,"混合矩阵 A","y");
   boxNode(930,195,230,66,"录音 x","b");
   link(350,228,500,228); link(780,228,930,228);
   note("x = A·s　　这是物理上真实发生的事",640,300,"d");
   note("⭐ 我们只看得到 x，要反推出 s",640,352,"y");
   note("办法：找一个「解混矩阵」W，使 W·x ≈ s",640,398,"g");''',
   "<b>先把上一讲的设定收拢一下。</b><br><b>房间里有几个人同时说话</b>（这些是<b>声源 s</b>），<b>几个麦克风各自录到一段混音</b>（这是 <b>x</b>）。每个麦克风离每个人远近不同，所以<b>录到的是各个声音按不同比例相加的结果</b>——这个比例关系写成一个<b>混合矩阵 A</b>，于是 <b>x = A·s</b>。<br><b>⚠ 关键在于：我们只看得到 x。</b>A 不知道，s 也不知道。<br><b>⭐ ICA 要做的是找一个「解混矩阵」W，让 W·x 尽量还原出 s。</b><br><b>这一讲要回答的是一个更根本的问题：凭什么这件事做得成？</b>", 130)],
 {'kp':0,'h':"鸡尾酒会：x = A·s，只给 x 求 s",
  'k':"<b>声源 s</b> 经<b>混合矩阵 A</b> 得到<b>录音 x</b>：<b>x = A·s</b>。混合是物理上真实发生的（麦克风离各人远近不同）。",
  'm':"⚠ <b>我们只看得到 x</b>——A 不知道，s 也不知道。",
  'w':"⭐ ICA 要找一个<b>解混矩阵 W</b>，使 <b>W·x ≈ s</b>。",
  'e':"⭐ <b>这一讲回答的是更根本的问题：凭什么这件事做得成？</b>答案会很苛刻。"},
 {'kp':0,'t':"ICA 的输入和目标分别是什么？",
  'o':["已知 A 和 x，求 s",
       "只已知录音 x，要同时反推出混合方式和原始声源——办法是找一个解混矩阵 W 使 W·x ≈ s",
       "已知 s，求 A",
       "已知 x 和 s，求 A"],'a':1,
  'w':"⚠ <b>A 和 s 都是未知的</b>，这正是问题难的地方。⭐ 下面会看到，正因为未知得这么彻底，<b>必然留下三种拆不开的歧义</b>。"}, t=130)

KP("先铺词：累积分布函数 CDF",
 [(r'''clearScene();setEq(null);setCap("「小于等于某个值」的概率");
   axes({x0:300,x1:980,y0:380,y1:190});
   sig(640,285,560,170,"b");
   note("F(v) = P(s ≤ v)",640,170,"b");
   note("⭐ 从 0 单调爬到 1，永不下降",640,230,"y");
   note("左端趋近 0：几乎不可能比「很小的数」还小",400,340,"d");
   note("右端趋近 1：几乎必然比「很大的数」小",900,340,"d");''',
   "<b>这一讲要用到一个新词，先单独讲清楚：累积分布函数，简称 CDF。</b><br><b>它的定义只有一句话：F(v) 就是「这个随机变量小于等于 v 的概率」。</b><br><b>⭐ 所以它天生有三个性质</b>：<b>取值永远在 0 和 1 之间</b>（因为它是个概率）；<b>单调不下降</b>（门槛往右移，被框进来的只会更多）；<b>左端趋近 0、右端趋近 1</b>。<br><b>⚠ 别把 CDF 和概率密度混了</b>——<b>密度回答「在这一点附近有多密」，CDF 回答「到这一点为止累计了多少」</b>。<b>下一节讲它们的关系。</b>", 494)],
 {'kp':0,'h':"CDF：F(v) = P(s ≤ v)",
  'k':"定义只有一句：<b>随机变量小于等于 v 的概率</b>。",
  'm':"⭐ 三个天生的性质：<b>取值在 0 到 1 之间</b>、<b>单调不下降</b>、<b>左端趋近 0 右端趋近 1</b>。",
  'w':"⚠ <b>别和概率密度混</b>：<b>密度问「这一点附近多密」，CDF 问「到这一点累计了多少」</b>。",
  'e':"⭐ 下一节给出两者的关系——那正是 ICA 需要它的理由。"},
 {'kp':0,'t':"累积分布函数 F(v) 的定义是什么？",
  'o':["随机变量恰好等于 v 的概率",
       "随机变量小于等于 v 的概率",
       "随机变量在 v 附近的密度",
       "随机变量的平均值"],'a':1,
  'w':"⭐ 由定义直接得到三个性质：<b>取值在 [0,1]</b>、<b>单调不下降</b>（门槛右移只会框进更多）、<b>两端分别趋近 0 和 1</b>。"}, t=494)

KP("★ 密度是 CDF 的导数",
 [(r'''clearScene();setEq("$$p(s) \\;=\\; F'(s)$$","top");setCap("两者只差一次求导");
   note("CDF 爬得陡的地方 ⇒ 密度大",640,232,"b");
   note("CDF 走得平的地方 ⇒ 密度小",640,285,"d");
   note("⭐ 所以「指定一个 CDF」就等于「指定了一个密度」",640,392,"y");''',
   "<b>密度和 CDF 的关系非常简单：密度就是 CDF 的导数。</b><br><b>直觉上很好理解</b>：CDF 在某处<b>爬得陡</b>，说明<b>那一小段里累计了很多概率</b> ⇒ 密度大；CDF 在某处<b>几乎是平的</b>，说明<b>那一带几乎没有概率</b> ⇒ 密度小。<br><b>⭐ 这个关系带来一个很实用的后果：只要你指定一个 CDF，就等于指定了一个密度。</b><br><b>⚠ 而且指定 CDF 往往更省事</b>——<b>CDF 只需要满足「从 0 单调爬到 1」，这个条件比「处处非负且积分为 1」好凑得多。</b><b>下一节就靠这一点挑出 ICA 要用的那个分布。</b>", 618)],
 {'kp':0,'h':"★ p(s) = F′(s)：密度是 CDF 的导数",
  'k':"CDF <b>爬得陡 ⇒ 密度大</b>；<b>走得平 ⇒ 密度小</b>。",
  'm':"⭐ <b>指定一个 CDF 就等于指定了一个密度。</b>",
  'w':"⚠ <b>而且指定 CDF 更省事</b>：只要「从 0 单调爬到 1」，比「处处非负且积分为 1」好凑得多。",
  'e':"⭐ ICA 正是靠这一点来挑它需要的那个分布。"},
 {'kp':0,'t':"概率密度和 CDF 是什么关系？",
  'o':["密度是 CDF 的积分",
       "密度是 CDF 的导数——CDF 爬得越陡，该处密度越大",
       "两者相等",
       "密度是 CDF 的倒数"],'a':1,
  'w':"⭐ 实用后果：<b>指定一个 CDF 就等于指定了一个密度</b>，而且<b>凑一个合法的 CDF 比凑一个合法的密度容易</b>（只要单调从 0 爬到 1）。"}, t=618)

# ══════════════ 其余知识点（分文件写）══════════════
import l16_ica, l16_rl
l16_ica.add(KP)     # 密度 → 三种歧义 → 非高斯定理 → sigmoid → 学习规则 → 稀疏编码/EEG/麦克风数
l16_rl.add(KP)      # 换场 → 直升机 → 状态/奖励/信用分配 → MDP 五元组 → 轨迹与总回报 → 策略

# ══════════════ 收尾 ══════════════
C.append(r'''KP("完 · 一讲跨两个世界",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("CS229 L16 · 完","ICA 收尾 ＋ 强化学习开篇",
      "非高斯是前提，MDP 是语言");},
    "收一下，这一讲前后半场几乎是两门学问。<br><b>前半场 ICA。</b>要用极大似然就<b>必须先有 s 的密度</b>——因为<b>似然的定义里就含着密度，没有密度就没有可优化的目标</b>。可 s 本身是未知量，<b>只能自己挑一个分布</b>。挑的办法是<b>先指定 CDF 再求导</b>（CDF 只要「从 0 单调爬到 1」，比直接凑一个合法密度容易），于是<b>拿 sigmoid 当 CDF，密度就是 σ(s)(1−σ(s))</b>。<b>⚠ 选它的真正理由不是好算，而是它不是高斯。</b><br><b>为什么非高斯这么要紧？因为 ICA 必然留下三种歧义。</b>前两种无害：<b>① 顺序</b>——分出来的两路不知道谁该编号为 1；<b>② 幅度与符号</b>——把 s 放大 α 倍、同时把 A 缩小 α 倍，<b>乘出来的 x 完全相同</b>，而 α 取负时波形整体翻转、人耳几乎听不出差别。<b>⭐ 第三种是致命的：旋转。</b>两个标准高斯画出来是一团<b>圆形</b>点云，<b>转任意角度看上去都一样</b> ⇒ <b>没有任何方向是「特别」的</b>，而 ICA 恰恰要找那些特别的方向。<b>⇒ 于是有了那条硬性定理：只有数据非高斯，ICA 才可能成立。</b>非高斯的点云有棱角、有朝向，<b>棱角才是算法的依据</b>。⚠ <b>实践推论：信号若接近高斯，ICA 表现差，而且调参救不了。</b><br><b>学习规则</b>就是老流程：<b>假定各源独立 ⇒ 联合密度相乘</b>（这正是 Independent Component Analysis 名字的由来），<b>代入 s = Wx 时补上 |det W|</b>（变量替换会改变体积，漏了它最大化似然会把 W 推向零），再<b>对 W 做随机梯度上升</b>（是上升——我们在最大化似然）。<br><b>后半场换世界：强化学习。</b>监督学习给每个 x 配答案 y，无监督只给 x，<b>而 RL 给的只是一个「好还是坏」的信号</b>。<b>直升机的例子说明了为什么必须这样</b>：<b>连顶尖飞行员也说不出「这个姿态下操纵杆该精确推到哪」</b>，他们凭手感飞，手感没法逐条标注；<b>⭐ 但「飞得好不好」一眼就看得出来</b>。<b>RL 就建立在这个不对称上：说清「什么算好」比说清「该怎么做」容易得多。</b>所以<b>你的职责是设计奖励函数</b>，⚠ 而<b>奖励写歪了算法会非常忠实地追求那个歪目标</b>（只奖励不摔机 ⇒ 它学会停在地上不起飞）。<b>⚠⚠ RL 真正难的地方是信用分配</b>：下 50 步后输了，<b>唯一反馈只有最后那个「输」</b>，却要分辨出到底哪一步该负责。<br><b>最后把这一切形式化成 MDP 的五个零件</b>：<b>S</b> 状态集合（⚠ 状态要含<b>做决定所需的全部信息</b>，这就是<b>马尔可夫性质</b>，MDP 的「M」）、<b>A</b> 动作集合、<b>P_sa</b> 状态转移概率（⚠ <b>是概率不是确定结果</b>——命令「往北」只有 0.8 概率真往北，因为轮子会打滑）、<b>γ</b> 折扣因子（<b>第 k 步乘 γ^k</b>；γ=0.9 时第 50 步只剩约 0.005 的权重。既反映「早拿到更值钱」，<b>也保证无限过程的总回报不发散</b>）、<b>R</b> 奖励函数。<b>算法最终交出的是策略 π：从状态到动作的映射。</b>⚠⚠ <b>它不是一条路线而是一本说明书</b>——路线一旦被随机性带偏后续全错位，<b>而说明书让你无论偏到哪格都知道下一步</b>。<b>⭐ 网格世界里最精彩的地方：整个下排的箭头都朝左、背离 +1，它宁可从左边绕上去，也不走右边那条贴着 −1 的近路。Ng 在这一格上停了很久——<b>往北快，但这一步有 0.1 的概率滑进 −1；往西安全，可是路更长、折扣更重、沿途一直在扣分</b>。他说这种权衡人光用眼睛是看不出来的，而解出来的最优动作正是「走更长但更安全的那条路」。<b>这就是整套 MDP 机器存在的理由：它能做出人凭直觉做不出的细微区分。</b></b><br><b>下一讲 L17 讲怎么把这样的策略真正算出来：值迭代与策略迭代。</b>");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>",
                    "<title>CS229 讲座 L16 · ICA 收尾与强化学习开篇</title>")
io.open("cs229-L16.html", "w", encoding="utf-8").write(full)
ns = len(_re.findall(r"\bS\(\d+,function", body))
print("cs229-L16.html: %d chars; %d KP / %d 讲解镜 + %d 总结卡 + %d 测验 = %d 帧"
      % (len(full), body.count("KP("), ns, body.count("SUM("), body.count("QUIZ("),
         ns + body.count("SUM(") + body.count("QUIZ(")))
print(quizreport())
bad = [m.group(1)[:40] for m in _re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', body)
       if m.group(1).strip() and not m.group(1).startswith("$$")]
if bad:
    print("  ⚠ 这些 setEq 没有 $$ 包裹：", bad)
for m in _re.finditer(r"matrix\(\{rows:(\d+),.*?var t=(\[\[.*?\]\]);", body, _re.S):
    want, rows = int(m.group(1)), len(_re.findall(r'\[\s*"', m.group(2)))
    if want != rows:
        print("  ⚠ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))
