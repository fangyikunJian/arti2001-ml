# -*- coding: utf-8 -*-
"""T2 线性回归「精读动画版」样张：放映厅形式 + 精读详实内容 + 解释动画。"""
import io
head = io.open("eng.txt", encoding="utf-8").read()
def js(t): return '"' + t.replace('\\','\\\\').replace('"','\\"') + '"'
C = []
# 开场 + 共享绘图前奏（数据、坐标映射）
C.append(r'''(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng;
var clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
var CFG={title:"M1 T2 · 线性回归（精读动画版 · 样张）",
  subtitle:"放映厅形式 + 精读详实内容 + 解释动画 · 空格推进 · N 讲解",video:""};
/* ── 共享：房价数据 + 坐标映射（散点图贯穿全片）── */
var DATA=[[1.0,145],[1.2,175],[1.5,190],[1.8,200],[2.0,230],[2.3,255],[2.6,258],[2.9,290],[3.2,315],[3.5,325]];
var PL={l:250,r:1035,t:150,b:558};
function PX(x){return PL.l+(x-1.0)/2.5*(PL.r-PL.l);}
function PY(y){return PL.b-(y-120)/225*(PL.b-PL.t);}
function FIT(x){return 72*x+78;}
function PLOT(){return DATA.map(function(d){return [PX(d[0]),PY(d[1])];});}
function axLabels(){
  note("面积 (千平方英尺)",PL.r,PL.b+34,"","end");
  note("价格 (千美元)",PL.l-14,PL.t-16,"","start");
  [1,2,3].forEach(function(v){note(String(v),PX(v),PL.b+30,"");});
  [150,250,325].forEach(function(v){note(String(v),PL.l-18,PY(v)+5,"","end");});
}
KP("开场",function(){
  S(0,function(){clearScene();setEq(null);setBig(null);setCap(null);
    setTitle("M1 T2 · 线性回归","精读动画版 · 样张",
      "把逐页精读的详实内容，搬进放映厅、配上解释动画");},
    "这是<b>精读动画版</b>的样张：形式还是你熟悉的<b>放映厅幻灯片</b>，但内容换成逐页精读那种<b>详实讲法</b>——散点会一颗颗浮现、拟合线会自己画出来、残差竖线会逐条落下，配上精读级的详细解释和 <s>⚠️陷阱</s>/<b>⭐重点</b>/<i>◇小八卦</i>。挑了线性回归里最适合动画的两页给你看感觉。<b>空格推进、N 开关讲解。</b>");
});''')

def KP(name, shots, summ, quiz):
    b=['KP(%s,function(){'%js(name)]
    for scene,narr in shots:
        b.append('  S(0,function(){%s},%s);'%(scene,js(narr)))
    fields=",".join('%s:%s'%(k,js(v)) for k,v in summ.items() if v and k!='kp')
    b.append('  SUM(0,%d,{%s});'%(summ['kp'],fields))
    opts=",".join(js(o) for o in quiz['o'])
    b.append('  QUIZ(0,%d,{t:%s,o:[%s],a:%d,w:%s});'%(quiz['kp'],js(quiz['t']),opts,quiz['a'],js(quiz['w'])))
    b.append('});'); C.append("\n".join(b))

# ═══ KP1 · 为什么预测数字（散点动画） ═══
KP("1 · 为什么预测一个数字",
 [("clearScene();setCap(\"<b>贯穿例子</b>：房屋面积 → 成交价格\");axes(PL);axLabels();"
   "dots(PLOT(),\"a\",9);",
   "很多真实问题，要预测的是一个<b>连续量</b>（continuous quantity）——房价、气温、考试分数——<s>而不是一个类别</s>。这里的贯穿例子是<i>房屋面积→价格</i>。看这张散点：这是 10 套房子（<b>m=10</b>），横轴面积、纵轴价格，每个点是一套房的真实成交记录。先把数据看清楚，是一切的起点。"),
  ("clearScene();setCap(\"第一件事：<b>有明显的上升趋势</b>\");axes(PL);axLabels();"
   "dots(PLOT(),\"a\",9);note(\"面积越大 → 价格越高\",PX(2.55),PY(140),\"y\",\"start\");",
   "看散点要抓两件事，第一件：<b>有明显的上升趋势</b>——面积越大、价格越高。<em>正因为趋势近似是一条直线</em>，用「直线去拟合」才是合理的。如果点是一团乱的，线性回归就不合适了。所以每次上手先问：<i>数据像不像一条线？</i>"),
  ("clearScene();setCap(\"第二件事：<s>点不会精确落在任何一条直线上</s>\");axes(PL);axLabels();"
   "dots(PLOT(),\"a\",9);note(\"抓趋势，不追每个点\",PX(1.05),PY(320),\"g\",\"start\");",
   "第二件事，也是初学者最容易搞错的：<s>不存在任何一条直线能穿过全部 10 个点</s>。真实数据里有噪声、有没测到的因素（地段、装修、房龄）。所以我们的目标是<b>抓住整体趋势</b>，<em>而不是追逐每一个点</em>。这句话请刻进脑子，后面代价函数、梯度下降全是它的展开。"),
  ("clearScene();setBig(null);boxNode(300,235,680,120,\"完美穿过所有点 = 过拟合\",\"r\");"
   "note(\"⚠ 陷阱\",300,215,\"r\",\"start\");",
   "顺着上一镜要立刻堵一个<s>坑</s>：既然点不在一条线上，那能不能画一条<em>弯弯扭扭、穿过每一个点</em>的曲线？<s>能，但那叫过拟合（overfitting）</s>——它把噪声也当成规律记下来了，换一批新房子就预测得一塌糊涂。<b>完美拟合训练点从来不是目标</b>，泛化到新数据才是。这是全课反复出现的主题。"),
  ("clearScene();setBig(null);boxNode(320,240,640,110,\"regression ← Galton 身高研究\",\"v\");"
   "note(\"◇ 小八卦\",320,220,\"v\",\"start\");",
   "<i>放松一下，一个小八卦</i>：为什么叫「regression（回归）」这么奇怪的名字？它来自 <i>Galton</i> 19 世纪研究身高的工作——他发现<em>高个父母的孩子，身高会「回归」到平均值</em>。这个名字纯属历史遗留，<s>跟这个方法今天在做什么其实没关系</s>。知道来历，考试碰到术语就不慌。")],
 {'kp':1,'h':"回归 = 预测连续量，抓趋势不追点",
  'k':"回归预测<b>连续量</b>（房价/气温/分数），不是类别。散点两件事：① <em>有上升趋势</em>→用直线合理；② <s>点不落在任何直线上</s>→抓趋势、不追每个点。",
  'm':"真实数据有噪声和未测因素，所以完美拟合不是目标。<s>穿过每个点=过拟合</s>，会把噪声当规律、换新数据就崩。",
  'w':"<s>「输出是数字」不等于回归的目标是精确命中</s>；泛化到新数据才是目标。regression 之名来自 Galton 身高研究，是历史遗留。",
  'e':"T2 开篇必考「回归 vs 分类」「为什么用直线」。答题带上『抓趋势不追点』『完美拟合=过拟合』两句。"},
 {'kp':1,'t':"散点图上，「点不会精确落在任何一条直线上」说明我们的目标应该是？",
  'o':["画一条穿过所有点的曲线","<b>抓住整体趋势，而不是追逐每一个点</b>","删掉偏离直线的点","把价格四舍五入"],'a':1,
  'w':"真实数据有噪声和未测因素，<s>没有直线能穿过所有点</s>。硬要穿过每个点就是<s>过拟合</s>——记住噪声、泛化差。所以目标是<b>抓整体趋势</b>。"})

# ═══ KP2 · 最佳拟合线 + 残差（动画核心） ═══
KP("2 · ★ 最佳拟合线与残差",
 [("clearScene();setEq(\"$$f(x)=72x+78\\\\quad(w=72,\\\\;b=78)$$\",\"top\");"
   "axes(PL);axLabels();dots(PLOT(),\"a\",9);",
   "现在把上一页的公式<b>画出来</b>。对这堆房子学出来的直线是 <b>f(x)=72x+78</b>，也就是斜率 w=72、截距 b=78。先摆好散点，下一镜让这条线自己长出来。<i>w=72 的意思</i>：面积每多 1 千平方英尺，预测价格约多 7.2 万美元。"),
  ("clearScene();setEq(\"$$f(x)=72x+78$$\",\"top\");axes(PL);axLabels();dots(PLOT(),\"a\",9);"
   "curve([[PX(1.0),PY(FIT(1.0))],[PX(3.5),PY(FIT(3.5))]],\"fit y\");"
   "note(\"模型的预测\",PX(3.05),PY(FIT(3.05))-18,\"y\",\"start\");",
   "看——<b>橙线自己画出来了</b>。这条线在每一个面积上都给出一个<i>预测价格</i>。<em>它不穿过任何一个点</em>，而是从所有点<b>中间</b>穿过、同时靠近所有点，是一个<b>折中</b>。回想上一页那句：抓趋势、不追点——这条线就是「趋势」的样子。"),
  ("clearScene();setEq(\"$$f(2.5)=72(2.5)+78=258$$\",\"top\");axes(PL);axLabels();dots(PLOT(),\"a\",9);"
   "curve([[PX(1.0),PY(FIT(1.0))],[PX(3.5),PY(FIT(3.5))]],\"fit y\");"
   "dots([[PX(2.5),PY(FIT(2.5))]],\"c\",11);note(\"没见过的面积也能预测\",PX(2.5),PY(FIT(2.5))+40,\"g\");",
   "这条线<b>最有用的地方</b>：数据表里<em>根本没有</em> 2.5 千平方英尺的房子，但直线照样能算——<b>f(2.5)=72×2.5+78=258</b>（那个绿点）。用学到的规律去预测<i>没见过的新数据</i>，这叫<b>泛化（generalisation）</b>，也是模型存在的全部意义。训练不是为了背下这 10 个点，是为了预测第 11 个。"),
  ("clearScene();setEq(null);setCap(\"每条竖线 = 一个样本的<b>误差</b>（残差 residual）\");"
   "axes(PL);axLabels();curve([[PX(1.0),PY(FIT(1.0))],[PX(3.5),PY(FIT(3.5))]],\"fit y\");"
   "DATA.forEach(function(d){link(PX(d[0]),PY(d[1]),PX(d[0]),PY(FIT(d[0])));});"
   "dots(PLOT(),\"a\",9);",
   "这镜是<b>整页的关键</b>：从每个真实点，向橙线<b>竖直落下一条线</b>——这些竖线，就是模型在每套房上<b>犯的误差</b>，正式名字叫<b>残差（residual）= 真实 y − 预测 ŷ</b>。<i>有的点在线上方（低估）、有的在下方（高估）</i>。<em>把这些竖线整体变短</em>，就是「让直线更好」的确切含义。下一页就把这些残差加起来，变成一个能被最小化的数——代价函数。"),
  ("clearScene();setEq(null);boxNode(250,235,780,120,\"associated 关联，不是 causes 导致\",\"b\");"
   "note(\"§ 语言纪律\",250,215,\"b\",\"start\");",
   "在收尾前插一条课件专门强调的<i>语言纪律</i>：解释 w=72 时要说「面积和价格<i>相关联（associated）</i>」，<s>不要说「面积导致（causes）价格」</s>。把房子硬扩建 1 千平方英尺，并不会可靠地给它加 7.2 万——模型学到的只是观测里的<b>模式</b>，里面混着地段、房龄、装修等没被区分的因素。<s>相关 ≠ 因果</s>，写报告和答题都要用对词，这是本课第一次强调、以后反复考。"),
  ("clearScene();setEq(null);setBig(\"好，怎么定义？\",\"→ 把残差平方求和 = 代价函数\");",
   "这条线看着不错，于是逼出下一页那个精确的问题：<b>「好」到底按什么定义来衡量？</b>光说「靠近所有点」不够精确。答案就是把刚才那些<b>残差各自平方、再全部加起来</b>——得到一个<em>单一的数</em>，越小代表这条线越好。这个数就是<b>代价函数（cost function）</b>，也是梯度下降要去最小化的目标。样张到这里，后面每一页都照这个精读+动画的方式做。")],
 {'kp':2,'h':"★ 拟合线 f(x)=72x+78、残差、泛化",
  'k':"学出的线 <b>f(x)=72x+78</b>（w=72/b=78），从点<em>中间</em>穿过=折中。<b>残差=真实y−预测ŷ</b>=每个点到线的竖直距离。能算没见过的 x（<b>泛化</b>）。",
  'm':"把残差整体变短=让线更好。下一步：残差<b>平方后求和</b>=代价函数，最小化它就得到最佳 w,b。w=72=面积每+1k sqft、价格约+7.2 万。",
  'w':"<s>拟合线不穿过任何点</s>，是折中不是命中。<s>说 associated 别说 causes</s>——相关≠因果，模型只学到混杂因素的模式。",
  'e':"T2 核心。会读拟合线、算预测（f(2.5)=258）、指出残差、并用『相关≠因果』的语言纪律答开放题。"},
 {'kp':2,'t':"图中从每个数据点竖直连到拟合线的那条线段，代表的是？",
  'o':["特征的大小","<b>残差（residual）——该样本的真实值与预测值之差，即模型的误差</b>","学习率","预测的置信区间"],'a':1,
  'w':"竖直间隙 = <b>真实 y − 预测 ŷ = 残差</b>，就是模型在这个样本上的误差。<em>把所有残差平方求和</em>就得到代价函数——最小化它=让直线最好。这是通往梯度下降的第一步。"})

# 收尾
C.append(r'''KP("样张 · 完",function(){
  S(0,function(){clearScene();setBig(null);setCap(null);setEq(null);
    setTitle("样张 · 完","精读动画版：形式=幻灯片，内容=精读，讲解=动画",
      "确认这个感觉后，我把 T2 全 27 页按这套做，并整合进放映厅");},
    "样张就到这。这就是<b>精读动画版</b>的感觉：<b>幻灯片形式没变</b>，但每一页都是精读级的详实讲解，配上<b>散点浮现、拟合线自绘、残差逐条落下</b>这类解释动画，还有 <s>⚠️陷阱</s>/<b>⭐重点</b>/<i>◇小八卦</i>/<i>§语言纪律</i>的标注卡。<b>确认这个方向后</b>，我就把 T2 全 27 页都按这套做透，并整合进你的放映厅入口。哪里想调（动画多少、每页镜数、标注卡样式）现在说。");
});
window.__startProjector(CFG);
})();''')

body = "\n".join(C)
full = head + "<script>\n" + body + "\n</script>\n"
full = full.replace("<title>放映厅模板</title>","<title>T2 线性回归 · 精读动画版样张</title>")
io.open("t2sample-ppt.html","w",encoding="utf-8").write(full)
print("t2sample-ppt.html:", len(full), "bytes;", body.count("S(0,function"), "shots;",
      body.count("KP("), "KP;", body.count("QUIZ("), "quiz")
