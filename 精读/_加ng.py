# -*- coding: utf-8 -*-
"""给逐页精读补「从零补基础 · Andrew Ng CS229」栏。
⚠ CS229 这几讲没有 PPT（Ng 全程白板），官方材料只有讲义 PDF + 视频。
   所以给的是「讲次 + 时间段 + 可点击带时间码的链接 + 讲义章节 + 本地文件」。
⚠ CS229 没讲的内容（DBSCAN、sklearn API、本课自己的评估框架）必须如实说明，不能硬凑。
用法：python _加ng.py
"""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

L13 = "rVfZHWTwXSA"   # Lecture 13 K-means / Mixture of Gaussians / EM
L14 = "tw6cmL5STuY"   # Lecture 14 EM & Factor Analysis
L15 = "dyb_cFywuik"   # Lecture 15 PCA & ICA


def V(vid, mmss, label):
    """生成一个跳到指定时间的链接。mmss 形如 '02:09'。"""
    m, s = mmss.split(":")
    return '<a href="https://www.youtube.com/watch?v=%s&t=%ds" target="_blank">%s</a>' % (
        vid, int(m) * 60 + int(s), label)


NONE = ('<b>CS229 没有对应内容。</b>')

DATA = {
"M2T1": {
 1: "<b>「PCA 到底是什么」就听这 9 分钟</b>——Lecture 15 的 "
    + V(L15, "02:09", "02:09") + " 到 11:20。他先举一个例子：一份数据里有两列其实是<b>同一个速度的 mph 和 km/h</b>，"
    "两列几乎完全线性相关，于是数据实际只住在低一维的空间里；接着换成遥控直升机飞手的「技术 vs 享受程度」，"
    "两个特征强相关、数据沿一条对角轴分布；最后用一张二维点云问「要压到一维，该往哪个方向投」。"
    "<b>全程没有公式，就是在回答『PCA 想干什么』。</b>听完再回来看这份精读会顺很多。"
    "<span class='src'>视频：CS229 Lecture 15 · 讲义：main_notes.pdf 第 168–173 页（本地已抽成 CS229/notes/ch12_pca.txt）</span>",

 3: "开头 " + V(L15, "00:07", "00:07") + "–02:00 给了 PCA 的<b>定位</b>：它<b>不建模 P(x)</b>（那是密度估计/因子分析的事），"
    "只回答「数据近似落在哪个子空间」。这条区分决定了后面所有结果该怎么解释。"
    "<span class='src'>视频：CS229 Lecture 15 开场</span>",

 5: NONE + " 这套「四类证据」框架是<b>本课自己的教学设计</b>（Canvas 标为 Core and assessable），"
    "CS229 没有单独讲评估无监督结果的通用框架。所以这一页只能按 Canvas 那页来背，没有替代来源。"
    "<span class='src'>来源：Canvas「Evaluating Unsupervised Learning」，本地 M2材料/Canvas讲义/T1-A_总览与评估框架.txt</span>",

 7: "推导从 " + V(L15, "11:28", "11:28") + " 开始：先讲预处理，再说「投影长度就是 xᵀu」，"
    "到 " + V(L15, "15:14", "15:14") + " 写出「最大化投影方差」并展开，"
    + V(L15, "16:58", "16:58") + " 那里他指着式子说<b>「这就是协方差矩阵」</b>，"
    "接着 18:36–21:20 用拉格朗日解出 <b>Σu = λu</b>。"
    "<b>想弄懂「为什么偏偏是特征向量」，听这 10 分钟最直接。</b>"
    "<span class='src'>视频：CS229 Lecture 15 · 讲义：ch12_pca.txt「Why covariance eigenvectors appear」一节</span>",

 8: "预处理那一段在 " + V(L15, "11:28", "11:28") + "–14:40。CS229 把它拆成<b>两件事</b>并说明各自何时可省："
    "减均值只有在已知均值为 0 时才能省（如声学信号）；除标准差只在各特征本来同尺度时能省（如灰度图 0–255）。"
    "<span class='src'>视频：CS229 Lecture 15 · 讲义：ch12_pca.txt 预处理段</span>",

 9: "两处值得听：" + V(L15, "28:55", "28:55") + " 讲为什么要标准化（举了具体例子）；"
    + V(L15, "56:33", "56:33") + " 他直接问 <b>「Can PCA overfit?」</b>。"
    "更有意思的是 38:00 之后他把「用 PCA 降过拟合」列为<b>可疑的应用</b>，说实测下来<b>成败各半</b>，"
    "而成功的那一半发了论文——但讲义里又写「降维可减小假设类复杂度」。<b>这个张力本身就是理解这一页的钥匙。</b>"
    "<span class='src'>视频：CS229 Lecture 15 后半 · 讲义：ch12_pca.txt 应用段</span>",

 10: "对应 " + V(L15, "21:20", "21:20") + "–27:00：取前 k 个特征向量、写出 y=(u₁ᵀx,…,u_kᵀx)，"
     "并说明<b>解压就是 x ≈ y₁u₁+…+y_ku_k</b>——他把「压缩 1000 维到 10 个数、再解压回去」讲得很具体。"
     "<span class='src'>视频：CS229 Lecture 15 · 讲义：ch12_pca.txt top-k 与应用段</span>",

 12: NONE + " CS229 是 2018 年的课，作业用 Python/NumPy 手写，<b>没有讲 scikit-learn 的 API</b>。"
     "这一页的属性方法只能按 Canvas 的 Python 工作流页来记。"
     "<span class='src'>来源：Canvas「PCA in Python: a guided workflow」，本地 M2材料/Canvas讲义/T1-B_PCA讲义.txt</span>",

 13: "标准化那段在 " + V(L15, "28:55", "28:55") + "–32:00。⚠️ <b>泄漏（train-only fit）CS229 是在 Lecture 8 讲的</b>"
     "（偏差方差与模型选择那一讲），不在 PCA 这一讲里；本地对应 <code>CS229/transcripts/L8.txt</code>。"
     "<span class='src'>视频：CS229 Lecture 15（标准化）+ Lecture 8（划分与泄漏）</span>",

 17: "严格解在 " + V(L15, "18:36", "18:36") + "–21:20：用拉格朗日乘子把带约束的最大化解成 <b>Σu = λu</b>，"
     "并说明<b>为什么取最大的特征值</b>。讲义里这一步写在脚注（「try using the method of Lagrange multipliers」）。"
     "<span class='src'>视频：CS229 Lecture 15 · 讲义：ch12_pca.txt 脚注 1</span>",
},

"M2T2": {
 1: "<b>k-means 从零听</b>：Lecture 13 的开头到 18:00 就是完整的 k-means。"
    + V(L13, "00:07", "00:00") + " 起讲算法本身，"
    + V(L13, "13:00", "13:00") + " 讲<b>为什么一定收敛</b>，"
    + V(L13, "15:41", "15:41") + " 讲<b>会卡在局部极小</b>。"
    "⚠️ <b>DBSCAN 在 CS229 完全没有讲</b>，那部分只能看 Canvas 讲义。"
    "<span class='src'>视频：CS229 Lecture 13 前 18 分钟 · 讲义：main_notes.pdf 第 147–149 页（本地 CS229/notes/ch10_kmeans.txt）</span>",

 4: "目标函数在 CS229 里叫 <b>distortion function（失真函数）</b>，就是这一页的 J。"
    "他还点出一个本课课件没说的视角：<b>k-means 是对 J 做坐标下降</b>——先固定质心对分配求最优，再固定分配对质心求最优。"
    "<span class='src'>视频：CS229 Lecture 13 前段 · 讲义：ch10_kmeans.txt</span>",

 5: "收敛性论证在 " + V(L13, "13:00", "13:00") + "：J 单调不增，<b>而且把 n 个点分到 k 个簇的方式只有有限多种</b>，"
    "所以必然停下。紧接着 " + V(L13, "15:41", "15:41") + " 他说「k-means get stuck on local minima」——"
    "<b>J 非凸，所以要多次随机初始化</b>。这两段合起来就是本页那道必考问答的完整答案。"
    "<span class='src'>视频：CS229 Lecture 13 · 讲义：ch10_kmeans.txt</span>",

 7: NONE + " 「多证据框架」「silhouette」「肘部法」都是<b>本课自己的教学内容</b>，CS229 这一讲没有涉及。"
    "只能按 Canvas 的评估页来准备。"
    "<span class='src'>来源：Canvas「Evaluating Unsupervised Learning」，本地 M2材料/Canvas讲义/T1-A_总览与评估框架.txt</span>",

 8: "⚠️ <b>CS229 完全没有讲 DBSCAN</b>——Ng 的无监督部分只覆盖 k-means、GMM/EM、因子分析、PCA、ICA。"
    "所以这一页<b>没有 Andrew Ng 的对应资源</b>，要补基础只能看 Canvas 的 DBSCAN 页"
    "（core/border/noise 三类点、密度可达、参数敏感性都在那里，而且写得比 PPT 细）。"
    "<span class='src'>来源：Canvas「DBSCAN」，本地 M2材料/Canvas讲义/T2-B_DBSCAN与Python工作流.txt</span>",

 12: "手算一轮 k-means 的流程，CS229 在 Lecture 13 开头用图示走过一遍（"
     + V(L13, "00:07", "00:00") + "–08:00），比纯文字好懂。"
     "<span class='src'>视频：CS229 Lecture 13 开头 · 讲义：ch10_kmeans.txt</span>",

 13: NONE + " 同第 8 页：DBSCAN 不在 CS229 范围内。"
     "<span class='src'>来源：Canvas「DBSCAN」，本地 M2材料/Canvas讲义/T2-B_DBSCAN与Python工作流.txt</span>",
},

"M2T3": {
 1: "<b>GMM 从零听</b>：Lecture 13 从 23:00 起进入混合高斯——他先说「你只看到数据，不知道它来自哪个高斯」，"
    "再和<b>高斯判别分析（GDA）</b>对照（" + V(L13, "26:52", "26:52") + "），"
    "然后 " + V(L13, "30:54", "30:54") + " 给出 <b>EM 的两个步骤</b>。"
    "<span class='src'>视频：CS229 Lecture 13 中后段 · 讲义：main_notes.pdf 第 150–166 页（本地 CS229/notes/ch11_em.txt）</span>",

 3: "隐变量的直觉在 " + V(L13, "26:52", "26:52") + " 附近：GMM 和 <b>GDA 的模型几乎一样，唯一差别是 GDA 知道 z（有标签）、"
    "GMM 不知道</b>。整个 EM 就是为了对付这个「不知道」。理解了这一句，责任度是什么就自然清楚了。"
    "<span class='src'>视频：CS229 Lecture 13 · 讲义：ch11_em.txt 11.1 节</span>",

 4: "混合密度与成分能拟合什么形状，见 " + V(L13, "39:40", "39:40") + "："
    "他演示了两个高斯的混合能拟合什么、更多成分又能拟合什么。"
    "<span class='src'>视频：CS229 Lecture 13 · 讲义：ch11_em.txt 11.1 节</span>",

 5: "<b>这是 CS229 最有价值的一段。</b>" + V(L13, "30:54", "30:54") + " 先给出 EM 两步；"
    "之后从 47:00 起他从头推导<b>为什么</b>要这么做：先讲凹函数，"
    + V(L13, "52:49", "52:49") + " 引入 <b>Jensen 不等式</b>，"
    + V(L13, "62:46", "62:46") + " <b>构造下界</b>。Lecture 14 开头 "
    + V(L14, "02:11", "02:11") + "–06:23 再复述一遍：<b>E 步选 Q 让下界贴住，M 步最大化下界</b>。"
    "⚠️ 考纲写明<b>收敛性证明不考</b>，但听懂这段之后，E/M 步的公式就不用背了。"
    "<span class='src'>视频：CS229 Lecture 13 后段 + Lecture 14 开头 · 讲义：ch11_em.txt 11.2–11.3 节</span>",

 6: NONE + " <b>spherical / diag / tied / full 四种协方差类型是 scikit-learn 的参数</b>，"
    "CS229 讲的是一般的 full 协方差。这一页按 Canvas 的 GMM 页准备即可。"
    "<span class='src'>来源：Canvas「Mixture of Gaussians」，本地 M2材料/Canvas讲义/T3-B_混合高斯概念.txt</span>",

 7: NONE + " <b>AIC/BIC 不在 CS229 这两讲里</b>（Ng 把模型选择放在 Lecture 8 的正则化与交叉验证那一讲，"
    "而且讲的是交叉验证不是信息准则）。这一页只能按 Canvas 的评估页与 GMM 页准备。"
    "<span class='src'>来源：Canvas「Evaluating Unsupervised Learning」+「GMM in Python」</span>",

 8: "责任度公式在 " + V(L13, "30:54", "30:54") + " 之后紧跟着给出，"
    "他还用了一个很好的类比（" + V(L13, "37:30", "37:30") + "）：<b>把责任度类比成 k-means 的簇质心分配，"
    "只是这里是「软」的</b>。讲义 11.1 节有完整的 E 步/M 步公式。"
    "<span class='src'>视频：CS229 Lecture 13 · 讲义：ch11_em.txt 11.1 节</span>",

 14: "M 步把责任度当<b>分数计数</b>用，这一点 CS229 讲义 11.1 节写得最清楚（"
     "<code>CS229/notes/ch11_em.txt</code>，搜 <code>effective number</code>）。"
     "视频里对应 " + V(L13, "30:54", "30:54") + " 之后那几分钟。"
     "<span class='src'>视频：CS229 Lecture 13 · 讲义：ch11_em.txt 11.1 节</span>",
},
}

for tag, pages in DATA.items():
    p = os.path.join(HERE, "data", tag + ".json")
    d = json.load(io.open(p, encoding="utf-8"))
    notes = {n["r"][0]: n for n in d["notes"]}
    n_set = 0
    for page, txt in pages.items():
        if page in notes:
            notes[page]["ng"] = txt
            n_set += 1
        else:
            print("  ⚠ %s 没有第 %d 页" % (tag, page))
    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    has_none = sum(1 for t in pages.values() if "CS229 没有对应内容" in t)
    print("%s：%d 页补了 Andrew Ng 对应（其中 %d 页如实标注「CS229 没讲」）" % (tag, n_set, has_none))
