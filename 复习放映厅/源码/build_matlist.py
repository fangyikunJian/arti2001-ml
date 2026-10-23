# -*- coding: utf-8 -*-
"""把 ★总入口.html 里「原始材料」那几块从「只给文件夹链接」换成「逐个文件点名」。

起因（2026-09-28）：用户说「你看下我 t1 的内容，做的远比目前多，你的总入口是不是少放了内容」。
一查：103 个可打开文件里，总入口只点名了 28 个，M1 的 19 份知识点/题库 PDF、
M1+M2 的 37 份 Tutorial/Practical、CS229 的 15 份讲义，全都藏在文件夹链接后面，
名字都看不到。这个脚本按 Topic 生成可折叠的文件清单，重跑即可刷新。

用法：在本目录跑 `python build_matlist.py`（路径相对于课程根目录自动解析）。
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
HUB = os.path.join(BASE, "★总入口.html")

# ── 文件类型标签 ─────────────────────────────────────────────────
KIND = {".pdf": ("PDF", "pdf"), ".pptx": ("PPTX", "ppt"), ".html": ("HTML", "htm"),
        ".ipynb": ("NB", "nb"), ".txt": ("TXT", "txt"), ".py": ("PY", "txt")}


def pages(rel):
    """PDF 页数；读不到就返回 None（不猜）。"""
    p = os.path.join(BASE, rel)
    if not p.lower().endswith(".pdf") or not os.path.exists(p):
        return None
    try:
        from pypdf import PdfReader
        return len(PdfReader(p).pages)
    except Exception:
        return None


# ── 每个文件一句话。★ 开头 = 我认为最该先看的 ──────────────────
D = {
 # ── M2 T1 PCA ──
 "M2材料/课件/M2T1_PCA.pptx": "官方课件本体，每页自带 Study check。三份逐页精读就是照它做的",
 "M2材料/课件/M2T1_PCA.pdf": "官方 expanded notes。⚠ 正文是图片，搜不了字也复制不了",
 "M2材料/Canvas讲义/T1-A_总览与评估框架.txt": "★ 四类证据框架＋silhouette 完整公式＋选 k 决策表。官方标 <b>Core and assessable</b>，而 PPT 几乎没讲",
 "M2材料/Canvas讲义/T1-B_PCA讲义.txt": "PCA 讲义正文：中心化、S 与 Σ、解释方差、缩放与泄漏",
 "M2材料/Tutorial与Practical/M2 T1 Tutorial.pdf": "Tutorial 题目",
 "M2材料/Tutorial与Practical/M2 T1 Tutorial_ans.pdf": "官方答案",
 "M2材料/Tutorial与Practical/M2 T1 - Tutorial Answers by hand.pdf": "★ 手算全过程（考试就考这个写法）。⚠ 图片版",
 "M2材料/Tutorial与Practical/M2 T1 PCA Guided Self-Study.html": "自学引导，可当额外练习",
 "M2材料/Tutorial与Practical/M2 T1 PCA Guided Self-Study solution.html": "自学引导的解答",
 # ── M2 T2 聚类 ──
 "M2材料/课件/M2T2_Clustering.pptx": "官方课件本体",
 "M2材料/课件/M2T2_Prac_KMeans_DBSCAN.pdf": "Practical 讲义：K-means 与 DBSCAN 的 Python 工作流",
 "M2材料/Canvas讲义/T2-A_聚类与K-means讲义.txt": "★ J/inertia、肘部、k–inertia–silhouette 示例表、全局最优 vs 实际拟合的单调性",
 "M2材料/Canvas讲义/T2-B_DBSCAN与Python工作流.txt": "★ <b>DBSCAN 的唯一来源</b>——CS229 完全不讲 DBSCAN。五点算例、ε 与 MinPts、k-距离图",
 "M2材料/Tutorial与Practical/M2 T2 Tutorial.pdf": "Tutorial 题目",
 "M2材料/Tutorial与Practical/M2 T2 Tutorial_ans.pdf": "官方答案",
 "M2材料/Tutorial与Practical/M2 T2 Prac.ipynb": "Practical 空白本",
 "M2材料/Tutorial与Practical/M2_T2_Prac_completed.ipynb": "Practical 完成版（含运行输出）",
 "M2材料/Tutorial与Practical/M2 T2 Prac solution.html": "Practical 解答，浏览器直接看",
 # ── M2 T3 GMM ──
 "M2材料/课件/M2T3_GMM.pptx": "官方课件本体",
 "M2材料/课件/GMM.pdf": "官方 expanded notes。⚠ 正文是图片",
 "M2材料/Canvas讲义/T3-A_GMM前置概率基础.txt": "前置概率：联合/边缘/条件、贝叶斯、责任度算例",
 "M2材料/Canvas讲义/T3-B_混合高斯概念.txt": "混合的生成故事、软分配 vs 硬分配",
 "M2材料/Canvas讲义/T3-C_GMM数学与EM.txt": "★ E 步 M 步的完整公式与一轮手算（含方差更新）",
 "M2材料/Canvas讲义/T3-D_GMM_Python与模型选择.txt": "sklearn 参数、协方差类型、AIC/BIC",
 "M2材料/Tutorial与Practical/M2 T3 Tutorial.pdf": "★ T3 Tutorial 原题（三道核心题＋扩展）",
 "M2材料/Tutorial与Practical/M2 T3 Tutorial_ans.pdf": "★ <b>T3 Tutorial 官方答案</b>——2026-10-07 才发布，含混合密度/责任度/M 步三题完整解",
 "M2材料/Tutorial与Practical/M2T3_Prac_general_feedback_for_students.pdf": "★ <b>讲师共性反馈</b>：逐题点名失分处，等同评分细则（完成度 50 / 理解 50）",
 "M2材料/Tutorial与Practical/M2 T3 Prac solution.html": "★ T3 Practical 官方解答（网页版，直接看）",
 "M2材料/Tutorial与Practical/M2 T3 Prac solution.ipynb": "T3 Practical 官方解答（notebook）",
 "M2材料/Tutorial与Practical/M2 T2 Prac solution.ipynb": "T2 Practical 官方解答（notebook）",
 "M2材料/Tutorial与Practical/M2 T3 Prac.ipynb": "Practical 空白本",
 "M2材料/Tutorial与Practical/M2_T3_Prac.ipynb": "Practical（较大的一份，含输出）",
 # ── M1 T1 ──
 "M1材料/课件/M1T1_overview.pptx": "官方课件。第 1–16 页是课务，考点从第 17 页开始",
 "M1材料/Tutorial与Practical/M1 T1 Tutorial.pdf": "Tutorial 题目",
 "M1材料/Tutorial与Practical/M1 T1 Tutorial_ans.pdf": "官方答案",
 "M1材料/Tutorial与Practical/M1 T1 Prac.ipynb": "Practical 空白本",
 "M1材料/Tutorial与Practical/M1 T1 Prac solution.ipynb": "Practical 解答（notebook）",
 "M1材料/Tutorial与Practical/M1 T1 Prac solution.html": "Practical 解答，浏览器直接看",
 "M1材料/Tutorial与Practical/M1T1_Prac_general_feedback_for_students.pdf": "讲师给全班的共性反馈——写法上的扣分点",
 "M1材料/笔记与阅读/M1T1_知识点全集.pdf": "★ 知识点全集：课件 17–31 页＋专题深入＋Practical 代码精讲＋考前速查",
 "M1材料/笔记与阅读/M1T1_题库全集.pdf": "★ 68 道选择题 ＋ 93 张术语速记卡，全部含解析",
 # ── M1 T2 ──
 "M1材料/课件/M1T2_LinearRegression.pptx": "官方课件本体",
 "M1材料/Tutorial与Practical/M1 T2 Tutorial.pdf": "Tutorial 题目",
 "M1材料/Tutorial与Practical/M1 T2 Tutorial_ans.pdf": "官方答案",
 "M1材料/Tutorial与Practical/M1 T2 Prac.ipynb": "Practical 空白本",
 "M1材料/Tutorial与Practical/M1 T2 Prac solution.ipynb": "Practical 解答（notebook）",
 "M1材料/Tutorial与Practical/M1 T2 Prac solution.html": "Practical 解答，浏览器直接看",
 "M1材料/Tutorial与Practical/M1T2_Prac_general_feedback_for_students.pdf": "讲师给全班的共性反馈",
 "M1材料/笔记与阅读/M1T2_线性回归_知识点全集.pdf": "★ 知识点全集",
 "M1材料/笔记与阅读/M1T2_线性回归_知识点_合并版.pdf": "知识点合并版（与上一份内容重叠，挑一份看即可）",
 "M1材料/笔记与阅读/M1T2_线性回归_Quizlet题库.pdf": "★ 28 组共 140 题，全部含答案与解析",
 "M1材料/笔记与阅读/Calculating linear regression coefficients.pdf": "官方阅读：闭式解系数怎么算",
 "M1材料/笔记与阅读/General form and gradient descent.pdf": "官方阅读：一般形式与梯度下降",
 "M1材料/笔记与阅读/Linear Regression A Probability Interpretation.pdf": "官方阅读：最小二乘的概率解释（＝CS229 的 MLE⇒最小二乘）",
 # ── M1 T3 ──
 "M1材料/课件/M1T3_Classification.pptx": "官方课件本体",
 "M1材料/Tutorial与Practical/M1 T3 Tutorial.pdf": "Tutorial 题目",
 "M1材料/Tutorial与Practical/M1 T3 Tutorial_ans.pdf": "官方答案",
 "M1材料/Tutorial与Practical/M1 T3 Prac.ipynb": "Practical 空白本",
 "M1材料/Tutorial与Practical/M1 T3 Prac solution.ipynb": "Practical 解答（notebook）",
 "M1材料/Tutorial与Practical/M1 T3 Prac solution.html": "Practical 解答，浏览器直接看",
 "M1材料/Tutorial与Practical/M1T3_Prac_general_feedback_for_students.pdf": "讲师给全班的共性反馈",
 "M1材料/笔记与阅读/M1T3_分类_知识点全集.pdf": "知识点全集",
 "M1材料/笔记与阅读/M1T3_分类_知识点全集_含推导.pdf": "★ 同上再加 <b>15 项数学推导</b>，标了易错与高频失分点",
 "M1材料/笔记与阅读/M1T3_分类_Quizlet全集.pdf": "★ 题库全集，含答案与解析",
 "M1材料/笔记与阅读/How to train your perceptron.pdf": "官方阅读：感知机训练",
 "M1材料/笔记与阅读/Logistic Regression A Step Beyond the Perceptron.pdf": "官方阅读：从感知机到逻辑回归",
 # ── M1 T4 ──
 "M1材料/课件/M1T4_SVM.pptx": "官方课件本体",
 "M1材料/Tutorial与Practical/M1 T4 Tutorial.pdf": "Tutorial 题目",
 "M1材料/Tutorial与Practical/M1 T4 Tutorial_ans.pdf": "官方答案",
 "M1材料/Tutorial与Practical/M1 T4 Prac.ipynb": "Practical 空白本",
 "M1材料/Tutorial与Practical/M1_T4_Prac_completed.ipynb": "Practical 完成版（含运行输出）",
 "M1材料/Tutorial与Practical/M1 T4 Prac solution.html": "Practical 解答，浏览器直接看",
 "M1材料/Tutorial与Practical/M1T4_Prac_general_feedback_for_students.pdf": "讲师给全班的共性反馈",
 "M1材料/Tutorial与Practical/M1_T4_Prac_Workflow_QA.pdf": "★ SVM Practical 工作流问答：间隔、核、诚实调参",
 "M1材料/笔记与阅读/M1T4_SVM_知识点整理.pdf": "★ 知识点整理",
 "M1材料/笔记与阅读/M1T4_SVM_题库与解析.pdf": "★ 题库与解析",
 "M1材料/笔记与阅读/SVM - margin.pdf": "官方阅读：间隔。⚠ 图片版",
 "M1材料/笔记与阅读/SVM - margin maximisation via its dual form.pdf": "官方阅读：对偶形式下的间隔最大化",
 "M1材料/笔记与阅读/SVM - kernel trick.pdf": "官方阅读：核技巧",
 "M1材料/笔记与阅读/Other classical machine-learning algorithms.pdf": "官方阅读：其它经典算法综述（跨 Topic）",
 # ── CS229 讲义 ──
 "CS229/notes/main_notes.pdf": "★ 2026 版合订讲义，<b>无监督全部章节都在里面</b>",
 "CS229/notes/ch10_kmeans.txt": "★ 已抽好：k-means（含失真函数 J 与坐标下降那段）",
 "CS229/notes/ch11_em.txt": "★ 已抽好：EM（Jensen、ELBO、变分视角）——T3 GMM 的深度来源",
 "CS229/notes/ch12_pca.txt": "★ 已抽好：PCA",
 "CS229/notes/cs229-notes7a.pdf": "2018 分册：k-means",
 "CS229/notes/cs229-notes7b.pdf": "2018 分册：混合高斯",
 "CS229/notes/cs229-notes8.pdf": "2018 分册：EM 算法",
 "CS229/notes/cs229-notes10.pdf": "2018 分册：PCA",
 "CS229/notes/cs229-notes1.pdf": "分册：监督学习与线性回归（M1 用）",
 "CS229/notes/cs229-notes3.pdf": "分册：核方法与 SVM（M1 T4 用）",
 "CS229/notes/cs229-notes5.pdf": "分册：正则化与模型选择",
 "CS229/notes/cs229-linalg.pdf": "线性代数复习（特征值那部分对 PCA 有用）",
 "CS229/notes/cs229-prob.pdf": "概率复习（对 T3 GMM 有用）",
 "CS229/notes/ML-advice.pdf": "Ng 的实务建议",
 "CS229/notes/error-analysis.pdf": "误差分析",
 "CS229/notes/cs229-notes2.pdf": "★ 分册：生成式学习（GDA ＋ 朴素贝叶斯）——<b>朴素贝叶斯在课程学习成果里但课件没讲</b>",
 "CS229/notes/cs229-notes4.pdf": "分册：学习理论（偏差方差的理论版）",
 "CS229/notes/cs229-notes6.pdf": "分册：在线学习与感知机收敛性",
 "CS229/notes/cs229-notes9.pdf": "分册：因子分析（和 PCA 同一行，但是概率模型）",
 "CS229/notes/cs229-notes11.pdf": "分册：ICA 独立成分分析",
 "CS229/notes/cs229-notes12.pdf": "分册：强化学习与控制（不在本课考纲）",
 "CS229/notes/cs229-notes13.pdf": "分册：线性二次调节与策略梯度（不在本课考纲）",
 "CS229/notes/cs229-notes-deep_learning.pdf": "★ 分册：深度学习（M3 用）——<b>已做成精读</b>：精读/CS229-DL-精读.html",
 "CS229/notes/gaussians.pdf": "多元高斯的性质（GDA / GMM 的底子）",
 "CS229/notes/more_on_gaussians.pdf": "高斯的边缘分布与条件分布闭式解（推 GMM 责任度要用）",
 "CS229/notes/cs229-hmm.pdf": "隐马尔可夫模型（不在本课考纲）",
 "CS229/notes/cs229-gaussian_processes.pdf": "高斯过程（不在本课考纲）",
 "CS229/notes/cs229-cvxopt.pdf": "凸优化 I（SVM 对偶那套的来源）",
 "CS229/notes/cs229-cvxopt2.pdf": "凸优化 II",
 "CS229/notes/loss-functions.pdf": "各种损失函数的对照",
 "CS229/notes/boosting.pdf": "提升方法（不在本课考纲）",
 "CS229/notes/representer-function.pdf": "表示定理（核方法为什么成立）",
 "CS229/notes/hoeffding.pdf": "Hoeffding 不等式（学习理论的工具）",
 "CS229/notes/_slides_probability.pdf": "★ 讨论课幻灯：概率复习 —— <b>CS229 少数真有幻灯的材料</b>",
 "CS229/notes/_slides_evaluation_metrics.pdf": "★ 讨论课幻灯：评估指标 —— 同上，对 M3 模型评估有用",
 # ── CS229 字幕（2018 秋全部 20 讲 + 1 节讨论课；由 CS229/fetch_transcripts.py 下载生成）──
 # 无监督（M2）
 "CS229/transcripts/L13.txt": "★ L13：k-means ＋ 混合高斯 ＋ EM（M2 T2/T3 的深度来源）",
 "CS229/transcripts/L14.txt": "★ L14：EM 的下界视角 ＋ 因子分析",
 "CS229/transcripts/L15.txt": "★ L15：PCA ＋ ICA（M2 T1 的深度来源）",
 "CS229/transcripts/L13_timed.txt": "L13 每 30 秒一条的定位索引（查时间码用）",
 "CS229/transcripts/L14_timed.txt": "L14 定位索引",
 "CS229/transcripts/L15_timed.txt": "L15 定位索引",
 # 神经网络与诊断（M3）
 "CS229/transcripts/L10.txt": "★ L10：神经网络入门（M3 计算图/激活）。<b>已做成片子</b>：影片/CS229讲座L10",
 "CS229/transcripts/L11.txt": "★ L11：反向传播 ＋ 改进网络（M3 计算图/激活与损失）。<b>已做成片子</b>：影片/CS229讲座L11",
 "CS229/transcripts/L12.txt": "★ L12：调试模型与误差分析（M3 模型评估）。<b>已做成片子</b>：影片/CS229讲座L12",
 "CS229/transcripts/L10_timed.txt": "L10 每 30 秒一条的定位索引（查时间码用）",
 "CS229/transcripts/L11_timed.txt": "L11 定位索引",
 "CS229/transcripts/L12_timed.txt": "L12 定位索引",
 # 监督学习（M1）
 "CS229/transcripts/L1.txt": "L1：开课——课程安排 ＋ 机器学习全景（监督 / 无监督 / 强化）",
 "CS229/transcripts/L2.txt": "L2：线性回归、批量/随机梯度下降、正规方程",
 "CS229/transcripts/L3.txt": "L3：局部加权回归、MLE ⇒ 最小二乘、逻辑回归、牛顿法",
 "CS229/transcripts/L4.txt": "L4：感知机 → 指数族 → 广义线性模型 GLM（解释线性回归与逻辑回归梯度为何同形）",
 "CS229/transcripts/L5.txt": "L5：生成式学习——高斯判别分析 GDA 对比判别式；朴素贝叶斯做垃圾邮件过滤",
 "CS229/transcripts/L6.txt": "L6：朴素贝叶斯收尾（拉普拉斯平滑）＋ SVM 开篇：泛函间隔、几何间隔、最优间隔分类器",
 "CS229/transcripts/L7.txt": "L7：表示定理、对偶、核技巧与 Mercer 定理、L1 软间隔（SVM 深度来源）",
 "CS229/transcripts/L8.txt": "L8：偏差方差、正则化、训练/验证/测试划分、k 折交叉验证、特征选择（M3 模型评估也用）",
 "CS229/transcripts/DS_LearningTheory.txt": "讨论课（助教讲）：学习理论——误差分解、一致收敛、VC 维，L8 的数学补充",
 "CS229/transcripts/L1_timed.txt": "L1 每 30 秒一条的定位索引（查时间码用）",
 "CS229/transcripts/L2_timed.txt": "L2 定位索引",
 "CS229/transcripts/L3_timed.txt": "L3 定位索引",
 "CS229/transcripts/L4_timed.txt": "L4 定位索引",
 "CS229/transcripts/L5_timed.txt": "L5 定位索引",
 "CS229/transcripts/L6_timed.txt": "L6 定位索引",
 "CS229/transcripts/L7_timed.txt": "L7 定位索引",
 "CS229/transcripts/L8_timed.txt": "L8 定位索引",
 "CS229/transcripts/DS_LearningTheory_timed.txt": "讨论课定位索引",
 # 不在本课考纲
 "CS229/transcripts/L9.txt": "L9：决策树与集成方法——bagging、随机森林、boosting（Raphael Townshend 讲）",
 "CS229/transcripts/L16.txt": "L16：ICA 收尾（用 CDF 推导模型）＋ 强化学习开篇",
 "CS229/transcripts/L17.txt": "L17：MDP——价值函数、值迭代与策略迭代",
 "CS229/transcripts/L18.txt": "L18：连续状态 MDP——离散化、模型与仿真、拟合值迭代",
 "CS229/transcripts/L19.txt": "L19：状态-动作奖励、有限时域 MDP、线性动力系统",
 "CS229/transcripts/L20.txt": "L20：强化学习的调试与诊断 ＋ 全课总结",
 "CS229/transcripts/L9_timed.txt": "L9 每 30 秒一条的定位索引（查时间码用）",
 "CS229/transcripts/L16_timed.txt": "L16 定位索引",
 "CS229/transcripts/L17_timed.txt": "L17 定位索引",
 "CS229/transcripts/L18_timed.txt": "L18 定位索引",
 "CS229/transcripts/L19_timed.txt": "L19 定位索引",
 "CS229/transcripts/L20_timed.txt": "L20 定位索引",
 # 工具
 "CS229/fetch_transcripts.py": "下载 ＋ 转换全部字幕的脚本（<code>python fetch_transcripts.py --check</code> 可做回归测试）",
}

# ── 分组：(区块 id, 组标题, 副标题, [文件相对路径]) ────────────────
GROUPS = [
 ("m2", "T1 · PCA", "主成分分析", [
   "M2材料/课件/M2T1_PCA.pptx", "M2材料/课件/M2T1_PCA.pdf",
   "M2材料/Canvas讲义/T1-A_总览与评估框架.txt", "M2材料/Canvas讲义/T1-B_PCA讲义.txt",
   "M2材料/Tutorial与Practical/M2 T1 Tutorial.pdf",
   "M2材料/Tutorial与Practical/M2 T1 Tutorial_ans.pdf",
   "M2材料/Tutorial与Practical/M2 T1 - Tutorial Answers by hand.pdf",
   "M2材料/Tutorial与Practical/M2 T1 PCA Guided Self-Study.html",
   "M2材料/Tutorial与Practical/M2 T1 PCA Guided Self-Study solution.html"]),
 ("m2", "T2 · 聚类", "K-means 与 DBSCAN", [
   "M2材料/课件/M2T2_Clustering.pptx", "M2材料/课件/M2T2_Prac_KMeans_DBSCAN.pdf",
   "M2材料/Canvas讲义/T2-A_聚类与K-means讲义.txt",
   "M2材料/Canvas讲义/T2-B_DBSCAN与Python工作流.txt",
   "M2材料/Tutorial与Practical/M2 T2 Tutorial.pdf",
   "M2材料/Tutorial与Practical/M2 T2 Tutorial_ans.pdf",
   "M2材料/Tutorial与Practical/M2 T2 Prac.ipynb",
   "M2材料/Tutorial与Practical/M2_T2_Prac_completed.ipynb",
   "M2材料/Tutorial与Practical/M2 T2 Prac solution.html",
   "M2材料/Tutorial与Practical/M2 T2 Prac solution.ipynb"]),
 ("m2", "T3 · GMM", "高斯混合与 EM", [
   "M2材料/课件/M2T3_GMM.pptx", "M2材料/课件/GMM.pdf",
   "M2材料/Canvas讲义/T3-A_GMM前置概率基础.txt", "M2材料/Canvas讲义/T3-B_混合高斯概念.txt",
   "M2材料/Canvas讲义/T3-C_GMM数学与EM.txt", "M2材料/Canvas讲义/T3-D_GMM_Python与模型选择.txt",
   "M2材料/Tutorial与Practical/M2 T3 Tutorial.pdf",
   "M2材料/Tutorial与Practical/M2 T3 Tutorial_ans.pdf",
   "M2材料/Tutorial与Practical/M2T3_Prac_general_feedback_for_students.pdf",
   "M2材料/Tutorial与Practical/M2 T3 Prac solution.html",
   "M2材料/Tutorial与Practical/M2 T3 Prac solution.ipynb",
   "M2材料/Tutorial与Practical/M2 T3 Prac.ipynb",
   "M2材料/Tutorial与Practical/M2_T3_Prac.ipynb"]),
 ("m1", "T1 · ML 流程与评估", "", [
   "M1材料/课件/M1T1_overview.pptx",
   "M1材料/笔记与阅读/M1T1_知识点全集.pdf", "M1材料/笔记与阅读/M1T1_题库全集.pdf",
   "M1材料/Tutorial与Practical/M1 T1 Tutorial.pdf",
   "M1材料/Tutorial与Practical/M1 T1 Tutorial_ans.pdf",
   "M1材料/Tutorial与Practical/M1 T1 Prac.ipynb",
   "M1材料/Tutorial与Practical/M1 T1 Prac solution.ipynb",
   "M1材料/Tutorial与Practical/M1 T1 Prac solution.html",
   "M1材料/Tutorial与Practical/M1T1_Prac_general_feedback_for_students.pdf"]),
 ("m1", "T2 · 线性回归", "", [
   "M1材料/课件/M1T2_LinearRegression.pptx",
   "M1材料/笔记与阅读/M1T2_线性回归_知识点全集.pdf",
   "M1材料/笔记与阅读/M1T2_线性回归_知识点_合并版.pdf",
   "M1材料/笔记与阅读/M1T2_线性回归_Quizlet题库.pdf",
   "M1材料/Tutorial与Practical/M1 T2 Tutorial.pdf",
   "M1材料/Tutorial与Practical/M1 T2 Tutorial_ans.pdf",
   "M1材料/Tutorial与Practical/M1 T2 Prac.ipynb",
   "M1材料/Tutorial与Practical/M1 T2 Prac solution.ipynb",
   "M1材料/Tutorial与Practical/M1 T2 Prac solution.html",
   "M1材料/Tutorial与Practical/M1T2_Prac_general_feedback_for_students.pdf",
   "M1材料/笔记与阅读/Calculating linear regression coefficients.pdf",
   "M1材料/笔记与阅读/General form and gradient descent.pdf",
   "M1材料/笔记与阅读/Linear Regression A Probability Interpretation.pdf"]),
 ("m1", "T3 · 分类", "感知机与逻辑回归", [
   "M1材料/课件/M1T3_Classification.pptx",
   "M1材料/笔记与阅读/M1T3_分类_知识点全集_含推导.pdf",
   "M1材料/笔记与阅读/M1T3_分类_知识点全集.pdf",
   "M1材料/笔记与阅读/M1T3_分类_Quizlet全集.pdf",
   "M1材料/Tutorial与Practical/M1 T3 Tutorial.pdf",
   "M1材料/Tutorial与Practical/M1 T3 Tutorial_ans.pdf",
   "M1材料/Tutorial与Practical/M1 T3 Prac.ipynb",
   "M1材料/Tutorial与Practical/M1 T3 Prac solution.ipynb",
   "M1材料/Tutorial与Practical/M1 T3 Prac solution.html",
   "M1材料/Tutorial与Practical/M1T3_Prac_general_feedback_for_students.pdf",
   "M1材料/笔记与阅读/How to train your perceptron.pdf",
   "M1材料/笔记与阅读/Logistic Regression A Step Beyond the Perceptron.pdf"]),
 ("m1", "T4 · SVM", "", [
   "M1材料/课件/M1T4_SVM.pptx",
   "M1材料/笔记与阅读/M1T4_SVM_知识点整理.pdf",
   "M1材料/笔记与阅读/M1T4_SVM_题库与解析.pdf",
   "M1材料/Tutorial与Practical/M1 T4 Tutorial.pdf",
   "M1材料/Tutorial与Practical/M1 T4 Tutorial_ans.pdf",
   "M1材料/Tutorial与Practical/M1 T4 Prac.ipynb",
   "M1材料/Tutorial与Practical/M1_T4_Prac_completed.ipynb",
   "M1材料/Tutorial与Practical/M1 T4 Prac solution.html",
   "M1材料/Tutorial与Practical/M1_T4_Prac_Workflow_QA.pdf",
   "M1材料/Tutorial与Practical/M1T4_Prac_general_feedback_for_students.pdf",
   "M1材料/笔记与阅读/SVM - margin.pdf",
   "M1材料/笔记与阅读/SVM - margin maximisation via its dual form.pdf",
   "M1材料/笔记与阅读/SVM - kernel trick.pdf"]),
 ("m1", "跨 Topic 阅读", "", ["M1材料/笔记与阅读/Other classical machine-learning algorithms.pdf"]),
 ("ng", "讲义 · 无监督（M2 直接用）", "", [
   "CS229/notes/ch10_kmeans.txt", "CS229/notes/ch11_em.txt", "CS229/notes/ch12_pca.txt",
   "CS229/notes/main_notes.pdf",
   "CS229/notes/cs229-notes7a.pdf", "CS229/notes/cs229-notes7b.pdf",
   "CS229/notes/cs229-notes8.pdf", "CS229/notes/cs229-notes10.pdf"]),
 ("ng", "字幕 · 无监督 L13–L15（M2 直接用）", "", [
   "CS229/transcripts/L13.txt", "CS229/transcripts/L14.txt", "CS229/transcripts/L15.txt",
   "CS229/transcripts/L13_timed.txt", "CS229/transcripts/L14_timed.txt",
   "CS229/transcripts/L15_timed.txt"]),
 ("ng", "字幕 · 神经网络与诊断 L10–L12（M3 直接用）", "", [
   "CS229/transcripts/L10.txt", "CS229/transcripts/L11.txt", "CS229/transcripts/L12.txt",
   "CS229/transcripts/L10_timed.txt", "CS229/transcripts/L11_timed.txt",
   "CS229/transcripts/L12_timed.txt"]),
 ("ng", "讲义 · 监督（M1）", "", [
   "CS229/notes/cs229-notes1.pdf", "CS229/notes/cs229-notes2.pdf",
   "CS229/notes/cs229-notes3.pdf", "CS229/notes/cs229-notes4.pdf",
   "CS229/notes/cs229-notes5.pdf", "CS229/notes/cs229-notes6.pdf"]),
 ("ng", "讲义 · 神经网络（M3）", "", [
   "CS229/notes/cs229-notes-deep_learning.pdf"]),
 ("ng", "字幕 · 监督学习 L1–L8 ＋ 讨论课（M1）", "", [
   "CS229/transcripts/L1.txt", "CS229/transcripts/L2.txt", "CS229/transcripts/L3.txt",
   "CS229/transcripts/L4.txt", "CS229/transcripts/L5.txt", "CS229/transcripts/L6.txt",
   "CS229/transcripts/L7.txt", "CS229/transcripts/L8.txt",
   "CS229/transcripts/DS_LearningTheory.txt",
   "CS229/transcripts/L1_timed.txt", "CS229/transcripts/L2_timed.txt", "CS229/transcripts/L3_timed.txt",
   "CS229/transcripts/L4_timed.txt", "CS229/transcripts/L5_timed.txt", "CS229/transcripts/L6_timed.txt",
   "CS229/transcripts/L7_timed.txt", "CS229/transcripts/L8_timed.txt",
   "CS229/transcripts/DS_LearningTheory_timed.txt"]),
 ("ng", "字幕 · 其余讲次（不在本课考纲）", "决策树 · ICA 收尾 · 强化学习", [
   "CS229/transcripts/L9.txt", "CS229/transcripts/L16.txt", "CS229/transcripts/L17.txt",
   "CS229/transcripts/L18.txt", "CS229/transcripts/L19.txt", "CS229/transcripts/L20.txt",
   "CS229/transcripts/L9_timed.txt", "CS229/transcripts/L16_timed.txt",
   "CS229/transcripts/L17_timed.txt", "CS229/transcripts/L18_timed.txt",
   "CS229/transcripts/L19_timed.txt", "CS229/transcripts/L20_timed.txt"]),
 ("ng", "讲义 · 本课不直接考，但能补底子", "因子分析 / ICA / 高斯性质 / 凸优化 / 学习理论工具", [
   "CS229/notes/cs229-notes9.pdf", "CS229/notes/cs229-notes11.pdf",
   "CS229/notes/gaussians.pdf", "CS229/notes/more_on_gaussians.pdf",
   "CS229/notes/cs229-cvxopt.pdf", "CS229/notes/cs229-cvxopt2.pdf",
   "CS229/notes/loss-functions.pdf", "CS229/notes/representer-function.pdf",
   "CS229/notes/hoeffding.pdf"]),
 ("ng", "讲义 · 完全不在考纲", "强化学习 / HMM / 高斯过程 / 提升方法", [
   "CS229/notes/cs229-notes12.pdf", "CS229/notes/cs229-notes13.pdf",
   "CS229/notes/cs229-hmm.pdf", "CS229/notes/cs229-gaussian_processes.pdf",
   "CS229/notes/boosting.pdf"]),
 ("ng", "参考与工具", "", [
   "CS229/notes/cs229-linalg.pdf", "CS229/notes/cs229-prob.pdf",
   "CS229/notes/_slides_probability.pdf", "CS229/notes/_slides_evaluation_metrics.pdf",
   "CS229/notes/ML-advice.pdf", "CS229/notes/error-analysis.pdf",
   "CS229/fetch_transcripts.py"]),
]

CSS = """
/* ══ 材料清单（逐个文件点名，可折叠） ══ */
details.mat{border:1px solid var(--line);border-radius:10px;background:var(--panel);
  margin:8px 0;overflow:hidden}
details.mat>summary{cursor:pointer;padding:11px 15px;font-size:14px;font-weight:620;
  list-style:none;display:flex;align-items:baseline;gap:9px}
details.mat>summary::-webkit-details-marker{display:none}
details.mat>summary::before{content:"\\25B8";color:var(--dim);font-size:11px;
  display:inline-block;transition:transform .15s}
details.mat[open]>summary::before{transform:rotate(90deg)}
details.mat>summary:hover{background:var(--panel2)}
details.mat>summary .sub{font-size:12px;font-weight:400;color:var(--dimmer)}
details.mat>summary .ct{margin-left:auto;font-family:var(--mono);font-size:11px;
  color:var(--dimmer);font-weight:400}
.fl{border-top:1px solid var(--line);padding:5px}
a.f{display:grid;grid-template-columns:46px minmax(180px,.95fr) 1.6fr;gap:11px;
  align-items:baseline;padding:7px 10px;border-radius:7px;text-decoration:none;color:inherit}
a.f:hover{background:var(--panel2)}
a.f+a.f{border-top:1px solid var(--stripe)}
a.f .nm{font-size:13.5px;font-weight:560;line-height:1.5}
a.f .dd{font-size:12.5px;color:var(--dim);line-height:1.55}
a.f .dd b{color:var(--yellow);font-weight:600}
a.f .pg{font-family:var(--mono);font-size:11px;color:var(--dimmer)}
a.f.star .nm{color:var(--blue)}
i.k{font-style:normal;font-family:var(--mono);font-size:9.5px;text-align:center;
  padding:2px 0;border-radius:4px;letter-spacing:.3px;display:block}
i.k.pdf{background:var(--tcoral);color:var(--coral)}
i.k.ppt{background:var(--tyellow);color:var(--yellow)}
i.k.htm{background:var(--tblue);color:var(--blue)}
i.k.nb{background:var(--tgreen);color:var(--green)}
i.k.txt{background:var(--tdim);color:var(--dim)}
@media(max-width:720px){a.f{grid-template-columns:46px 1fr}a.f .dd{grid-column:2}}
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row(rel):
    """一行文件。返回 (html, 存在与否)。"""
    p = os.path.join(BASE, rel)
    if not os.path.exists(p):
        return None
    ext = os.path.splitext(rel)[1].lower()
    label, cls = KIND.get(ext, ("FILE", "txt"))
    name = os.path.splitext(os.path.basename(rel))[0]
    desc = D.get(rel, "")
    star = desc.startswith("★")
    if star:
        desc = desc[1:].strip()
    n = pages(rel)
    meta = ' <span class="pg">%d 页</span>' % n if n else ""
    href = rel.replace("\\", "/")
    # 名字里的 < > & 要转义，描述里我自己写的 <b> 保留
    return ('<a class="f%s" href="%s"><i class="k %s">%s</i>'
            '<span class="nm">%s%s</span><span class="dd">%s</span></a>'
            % (" star" if star else "", href, cls, label, esc(name), meta, desc))


def block(title, sub, files):
    rows, missing = [], []
    for rel in files:
        r = row(rel)
        if r:
            rows.append(r)
        else:
            missing.append(rel)
    if not rows:
        return "", missing
    h = ['<details class="mat"><summary>%s%s<span class="ct">%d 份</span></summary>'
         % (esc(title), (' <span class="sub">%s</span>' % esc(sub)) if sub else "", len(rows)),
         '<div class="fl">'] + rows + ['</div></details>']
    return "\n".join(h), missing


def main():
    html = io.open(HUB, encoding="utf-8").read()
    missing_all = []
    built = {}
    for sid, title, sub, files in GROUPS:
        b, miss = block(title, sub, files)
        missing_all += miss
        built.setdefault(sid, []).append(b)

    # 1. 注入 CSS（幂等：先删旧的）
    #    连同块前的全部换行和块尾的 \n 一起删；原来只删到 \n</style> 之前，
    #    每跑一次就多留一个空行（2026-09-29 查出，已积了 4 个）。
    html = re.sub(r"\n+/\* ══ 材料清单.*?\n(?=</style>)", "", html, flags=re.S)
    html = html.replace("</style>", CSS + "</style>", 1)

    # 2. 替换各区块里的「原始材料 / 文字素材」slim 列表
    def swap(section_id, heading, new_html):
        nonlocal html
        m = re.search(r'(<section id="%s".*?)(<h3>%s</h3>\s*<div class="slim">.*?</div>)'
                      % (section_id, heading), html, re.S)
        if not m:
            # 已经换过一轮：替换已生成的 details 串
            m2 = re.search(r'(<section id="%s".*?)(<h3>%s</h3>)(\s*(?:<details class="mat">.*?</details>\s*)+)'
                           % (section_id, heading), html, re.S)
            if not m2:
                print("  ⚠ 找不到锚点: #%s / %s" % (section_id, heading))
                return False
            html = html[:m2.start(3)] + "\n" + new_html + "\n" + html[m2.end(3):]
            return True
        html = html[:m.start(2)] + "<h3>%s</h3>\n" % heading + new_html + html[m.end(2):]
        return True

    ok = 0
    ok += swap("m2", "原始材料", "\n".join(built["m2"]))
    ok += swap("m1", "原始材料", "\n".join(built["m1"]))
    ok += swap("ng", "文字素材", "\n".join(built["ng"]))

    io.open(HUB, "w", encoding="utf-8").write(html)
    total = sum(b.count('class="f') for bs in built.values() for b in bs)
    print("材料清单已写入 ★总入口.html：%d 个区块替换成功，点名文件 %d 个" % (ok, total))
    if missing_all:
        print("⚠ 清单里有但磁盘上找不到的 %d 个：" % len(missing_all))
        for m in missing_all:
            print("   -", m)


if __name__ == "__main__":
    main()
