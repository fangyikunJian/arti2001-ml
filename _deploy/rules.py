# -*- coding: utf-8 -*-
"""公开发布时**不进仓库**的东西 —— 这是唯一的一份清单。

`.gitignore` 和「总入口在公开站上把哪些链接标成不可用」都从这里生成，
所以两者不会各说各话（漏一边的后果是：公开站上一堆 404 链接，看着像站坏了）。

分三类：
  ① 第三方材料 —— 学校课件、Tutorial 与官方答案、讲师反馈、Canvas 讲义原文、
     Stanford CS229 讲义与字幕、以及从这些东西里抽出来的幻灯 PDF。
     ⚠ 著作权属于学校与各课作者，本仓库不转载；本地照常用。
  ② 个人信息 —— `ppt_M1T1_overview.txt` 里有五位任课老师的 @adelaide.edu.au 邮箱
     （从官方 PPT 抽文本时带出来的）。**公开站上不能有活人的联系方式。**
  ③ 构建中间产物与本地文件 —— manim 的 partial_movie_files、__pycache__、备份等。
"""

# ── ① 第三方材料（目录整个不收）──────────────────────────
THIRD_PARTY_DIRS = [
    "M1材料/课件/", "M2材料/课件/", "M3材料/课件/",
    "M1材料/Tutorial与Practical/", "M2材料/Tutorial与Practical/",
    "M3材料/Tutorial与Practical/",
    "M2材料/Canvas讲义/", "M3材料/Canvas讲义/",
    "CS229/notes/", "CS229/transcripts/",
    "精读/slides/",
    # ⚠ 别看名字像自己的源码 —— `精读/src/*.txt` 是官方课件的**逐页全文抽取**，
    #   而且连【备注讲稿】（老师的讲稿备注）都抽出来了。等于把整份课件换成文本发布。
    "精读/src/",
    "其它/",
]

# ── ① 第三方材料（散落的单个文件）────────────────────────
THIRD_PARTY_FILES = [
    # 根目录上那三份官方 PDF（前两份和 M2材料/课件/ 里的逐字节相同）
    "M2T1_PCA.pdf", "GMM.pdf", "Assessment 2 Revision.pdf",
    # M1 的官方阅读材料；同目录下 M1T* 开头的是我自己写的，照收
    "M1材料/笔记与阅读/Calculating linear regression coefficients.pdf",
    "M1材料/笔记与阅读/General form and gradient descent.pdf",
    "M1材料/笔记与阅读/How to train your perceptron.pdf",
    "M1材料/笔记与阅读/Linear Regression A Probability Interpretation.pdf",
    "M1材料/笔记与阅读/Logistic Regression A Step Beyond the Perceptron.pdf",
    "M1材料/笔记与阅读/Other classical machine-learning algorithms.pdf",
    "M1材料/笔记与阅读/SVM - kernel trick.pdf",
    "M1材料/笔记与阅读/SVM - margin maximisation via its dual form.pdf",
    "M1材料/笔记与阅读/SVM - margin.pdf",
]

# ── ② 含个人信息 ─────────────────────────────────────
PERSONAL = [
    "复习放映厅/源码/ppt_M1T1_overview.txt",       # ⚠ 五个老师的邮箱在这里
    "复习放映厅/源码/ppt_M1T2_LinearRegression.txt",
    "复习放映厅/源码/ppt_M1T3_Classification.txt",
    "复习放映厅/源码/ppt_M1T4_SVM.txt",
]

# ── ③ 构建产物与本地文件（不出现在总入口里，所以不用标记）──
BUILD_ONLY = [
    "__pycache__/", "*.pyc", "*.bak", "*.bak-*",
    "复习放映厅/源码/media/",        # manim 的 partial_movie_files，392 个 mp4
    "复习放映厅/_备份-修复前/",
    "M2材料/笔记与阅读.zip",
    ".claude/",
    "nul", "**/nul",               # Windows 保留设备名，git 索引不了
    ".DS_Store", "Thumbs.db",
]

#: 公开站上要标成「只在本地有」的路径前缀 —— 给总入口那段脚本用
MISSING_PREFIXES = THIRD_PARTY_DIRS + THIRD_PARTY_FILES + PERSONAL

#: 少数**显眼位置**的链接指向了没收进来的材料，划掉会很别扭。
#: 这里给它们一个已发布的替代目标：公开站上改指替代品，本地照旧指原件。
#: ⚠ 只给「替代品真的覆盖了同样内容」的链接配，别为了好看乱指。
#: 实测总入口 148 条被标记的链接里有 147 条在可折叠的「材料清单」里（本来就是原件索引），
#: 真正显眼的只有下面这一条。
ALTERNATIVES = {
    # 行动条第 1 步「先读考纲那一页」。考纲原文是 Canvas 页面的抄录，不发布；
    # 但同样的内容在总目录 PDF 的「考试形式（Canvas 原文要点）」一节里有。
    "M3材料/Canvas讲义/T0_考纲与考试形式.txt": "M3材料/笔记与阅读/M3_总目录.pdf",
}


def gitignore_text():
    L = ["# 由 _deploy/rules.py 生成，别手改 —— 跑 `python _deploy/apply.py`",
         "",
         "# ── 构建产物与本地文件 ──"]
    L += BUILD_ONLY
    L += ["",
          "# ── 第三方材料：学校课件 / Tutorial 与官方答案 / 讲师反馈 /",
          "#    Canvas 讲义原文 / CS229 讲义与字幕 / 幻灯 PDF ──",
          "#    著作权属于学校与各课作者，本仓库不转载。本地照常用，",
          "#    公开站上这些链接会被标成「只在本地有」。"]
    L += THIRD_PARTY_DIRS
    L += [f.replace("[", "\\[").replace("]", "\\]") for f in THIRD_PARTY_FILES]
    L += ["",
          "# ── 含个人信息：从官方 PPT 抽文本时带出了任课老师的邮箱 ──"]
    L += PERSONAL
    return "\n".join(L) + "\n"
