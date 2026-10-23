# -*- coding: utf-8 -*-
"""把 M3 的 11 份 markdown 知识点整理转成和 M2 同一套版式的可打印 HTML / PDF。

为什么要转：M3 测验（Week 13）也是**开卷**，而笔记现在只是 .md —— 打印出来没有
版式、表格会散架、⚠/⭐ 的层次全丢。M2 那套（封面 → 目录 → 章节 → 彩色提示框）
是用户认可过的，直接复用 `m2kit.py`，不另起炉灶。

markdown → 构件：
    # 标题          → 本册内的分篇标题（H2）
    ## / ### / #### → H2 / H3 / H4
    | 表格 |        → TB            ``` 围栏 ```  → EQ
    - / 1.          → UL / OL        **粗** `码`  → m2kit.mk()
    > 引用          → 彩色提示框，颜色按行首标记分：
                       ⚠→红(w)  ⭐→绿(t)  ★/📌→黄(k)  无标记→蓝(s)

⚠ 两个踩过的坑，别改回去：
  ① 一个引用块里可能**混着多种标记**（实测 189 块里有 22 块混），所以是
     「按标记切成多段、每段一个框」，不是「整块一个框」。
  ② 本语料里**连续两行不是同一段**（常见 `⇒ 结论` 紧跟 `⚠ 但是…`），
     所以一行一个 <p>，不做 markdown 标准的软换行合并。
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from m2kit import (H2, H3, H4, P, NOTE, UL, EQ, TB, CAL, PB,  # noqa: E402
                   build, to_pdf, mk)

MD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # …/笔记与阅读
OUT = MD

MARK = "⚠⭐★📌"
KIND = {"⚠": "w", "⭐": "t", "★": "k", "📌": "k"}
LABEL = {"w": "容易错", "t": "技巧", "k": "考点", "s": "说明"}
_LEAD = re.compile(r"^([" + MARK + r"]+)\s*(.*)$", re.S)
_BOLDLEAD = re.compile(r"^\*\*([^*]{2,34})\*\*[：:　 ]*(.*)$", re.S)
_ROW = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
_BAR = re.compile(r"(?<!\\)\|")        # 单元格里的 \| 不算分隔符


def cells(line):
    """切一行表格。按**未转义**的竖线切，再把 \\| 还原成 | 。"""
    return [c.strip().replace("\\|", "|")
            for c in _BAR.split(line.strip().strip("|").strip())]


# ───────────────────────── 引用块 ─────────────────────────
def quote(lines, head_block):
    """一个引用块 → 若干个提示框。head_block=True 时是文件头的来源信息。"""
    if head_block:
        return [NOTE(" ｜ ".join(l.strip() for l in lines if l.strip()))]

    runs = []           # [(kind, 标记, [行]), …]
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        m = _LEAD.match(s)
        if m:
            glyph = m.group(1)
            kind = KIND.get(glyph[0], "s")
            # 同一个引用块里连着好几条同类标记时，合成一个框。
            # 两条 ⚠ 排成两个红框，纸上会显得很碎。
            if runs and runs[-1][0] == kind:
                runs[-1][2].append(glyph + " " + m.group(2))
            else:
                runs.append([kind, glyph, [m.group(2)]])
        elif runs:
            runs[-1][2].append(s)
        else:
            runs.append(["s", "", [s]])

    out = []
    for kind, glyph, body in runs:
        body = [b for b in body if b.strip()]
        if not body:
            continue
        # 标记后紧跟一小段粗体 ⇒ 拿它当框标题（实测 68 处是这种写法）。
        # ⚠ 没有粗体引子时**不要**硬塞「容易错 / 技巧」这种通用标题：
        #   框的颜色和行首的 ⚠/⭐ 已经说明了类型，再加一行只是噪音，
        #   而且会把原文和标记切开。这时把标记留在正文首行里。
        bm = _BOLDLEAD.match(body[0])
        if bm:
            ttl, body[0] = (glyph + " " + bm.group(1)).strip(), bm.group(2)
        else:
            ttl, body[0] = "", (glyph + " " + body[0]).strip()
        body = [b for b in body if b.strip()]
        # 框里偶尔有列表（实测 5 行）
        parts, buf = [], []
        for b in body:
            if re.match(r"^\s*[-*] ", b):
                buf.append(re.sub(r"^\s*[-*]\s*", "", b))
            else:
                if buf:
                    parts.append(UL(buf)); buf = []
                parts.append(P(b))
        if buf:
            parts.append(UL(buf))
        if ttl:
            out.append(CAL(kind, ttl, *parts))
        else:
            # 空标题不能走 CAL：它会留下一个空的 .ttl（display:block + 下边距），
            # 在纸上就是每个框顶上多出一条空行。
            out.append('<div class="cal %s">%s</div>' % (kind, "".join(parts)))
    return out


# ───────────────────────── 主转换 ─────────────────────────
def conv(path):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    out, i, n = [], 0, len(lines)
    title, secs, seen_head = "", [], False

    while i < n:
        raw, s = lines[i], lines[i].strip()

        if s.startswith("# "):
            title = s[2:].strip(); i += 1; continue
        if s in ("---", "***", "___"):
            i += 1; continue
        if s.startswith("#### "):
            out.append(H4(s[5:])); i += 1; continue
        if s.startswith("### "):
            out.append(H3(s[4:])); i += 1; continue
        if s.startswith("## "):
            t = s[3:].strip()
            secs.append(t); out.append(H3(t)); i += 1; continue

        if s.startswith("```"):                      # 代码／算式围栏
            j, buf = i + 1, []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j].rstrip()); j += 1
            while buf and not buf[-1].strip():
                buf.pop()
            if buf:
                out.append(EQ(*buf))
            i = j + 1; continue

        if s.startswith("|") and i + 1 < n and _ROW.match(lines[i + 1]):
            head = cells(s)
            j, rows = i + 2, []
            while j < n and lines[j].strip().startswith("|"):
                r = cells(lines[j])
                if len(r) > len(head):          # 单元格里有没转义的竖线
                    r = r[:len(head) - 1] + [" | ".join(r[len(head) - 1:])]
                    print("   ⚠ 表格行列数多出来，已把多余的并回最后一列：",
                          lines[j].strip()[:60])
                rows.append((r + [""] * len(head))[:len(head)]); j += 1
            out.append(TB(head, rows))
            i = j; continue

        if s.startswith(">"):
            j, buf = i, []
            while j < n and lines[j].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[j]).rstrip()); j += 1
            out += quote(buf, not seen_head and buf and buf[0].startswith("源页面"))
            seen_head = True
            i = j; continue

        if re.match(r"^\s*[-*] ", raw):
            j, items = i, []
            while j < n and re.match(r"^\s*[-*] ", lines[j]):
                items.append(re.sub(r"^\s*[-*]\s*", "", lines[j]).strip()); j += 1
            out.append(UL(items)); i = j; continue

        if re.match(r"^\s*\d+\. ", raw):
            j, items = i, []
            while j < n and re.match(r"^\s*\d+\. ", lines[j]):
                items.append(re.sub(r"^\s*\d+\.\s*", "", lines[j]).strip()); j += 1
            out.append(UL(items, ordered=True)); i = j; continue

        if not s:
            i += 1; continue

        out.append(P(s))
        i += 1

    return title, secs, out


# ───────────────────────── 分册 ─────────────────────────
BOOKS = [
    ("M3T1_神经网络基础_知识点整理", "神经网络基础",
     "Module 3 · Topic 1 — 知识点完整整理",
     ["M3-00_模块总览与记号表.md",
      "M3T1-1_神经网络能学什么_知识点整理.md",
      "M3T1-2_计算图与链式法则_知识点整理.md",
      "M3T1-3_单个神经元怎么学_知识点整理.md"],
     ["涵盖 **模块总览与记号表** ＋ **Topic 1 三课**",
      "网络结构与参数维度 · 前向传播",
      "**计算图** · 链式法则基础 · 输出神经元的损失梯度",
      "**一次梯度下降更新的完整手算**",
      "⚠ 记号表全模块通用，先看它"]),
    ("M3T2_训练神经网络_知识点整理", "训练神经网络",
     "Module 3 · Topic 2 — 知识点完整整理",
     ["M3T2-1_激活函数_知识点整理.md",
      "M3T2-2_损失函数_知识点整理.md",
      "M3T2-3_隐藏层怎么学_知识点整理.md",
      "M3T2-4_批量epoch与自动微分_知识点整理.md"],
     ["涵盖 **Topic 2 四课**",
      "sigmoid / tanh / ReLU 及导数 · **饱和与梯度行为**",
      "MSE 与交叉熵 · **四种任务的输出层与损失选择**",
      "**隐藏层权重梯度的完整反向传播手算**",
      "batch · epoch · **自动微分（GradientTape 三问）**"]),
    ("M3T3_模型评估_知识点整理", "模型评估",
     "Module 3 · Topic 3 — 知识点完整整理",
     ["M3T3-1_数据划分与训练证据_知识点整理.md",
      "M3T3-2_混淆矩阵与四个指标_知识点整理.md",
      "M3T3-3_ROC曲线与AUC_知识点整理.md"],
     ["涵盖 **Topic 3 三课**",
      "训练/验证/测试的角色 · **数据泄漏** · 欠拟合与过拟合的证据",
      "学习率证据 · 重复训练证据 · **基于验证集的早停**",
      "混淆矩阵 · **accuracy / precision / recall / F1**",
      "**ROC / AUC 与阈值权衡**"]),
]

MATE = "M3 测验：Week 13（2026-11-09 ~ 11-15）· 110 分钟 · 开卷 · 20 选择×3 ＋ 4 大题×10"

CSS_EXTRA = """
/* ── md2doc 追加（只影响 M3 这三册） ── */
.note{text-align:left; word-break:break-all}   /* 源页面那行有长 URL，
        继承 p 的 justify 会把「源 页 面 ：」拉成一行稀疏的大字 */
/* 目录分两栏：原本单栏 2.05 行距要占两页，考场上翻目录还要翻页就没意义了。
   每一「篇」整体不许被拆到两栏（break-inside），否则子项会和标题分家。 */
.toc>ol{column-count:2; column-gap:8mm; line-height:1.72}
.toc>ol>li{break-inside:avoid; -webkit-column-break-inside:avoid; margin-bottom:1.5mm}
.toc ol ol{line-height:1.52; margin:.6mm 0 0; padding-left:4.5mm}
.toc ol ol li{margin:.2mm 0}
"""

# ⭐/📌 在 Chrome 里是**彩色 emoji**，印出来是个黄团子，连写两三个尤其吵；
# ★ 是普通字形，和正文一个颜色。框的底色已经区分了类型，统一换成 ★。
GLYPH = {"⭐": "★", "📌": "★"}


def main():
    made = []
    for stem, title, sub, files, cover in BOOKS:
        body, toc = [], []
        for k, f in enumerate(files):
            p = os.path.join(MD, f)
            assert os.path.exists(p), "找不到 " + p
            t, secs, parts = conv(p)
            if k:
                body.append(PB())
            body.append(H2(t))
            body += parts
            toc.append((t, secs))
        path = build(os.path.join(OUT, stem + ".html"), title, sub, cover, toc, body, mate=MATE)
        doc = io.open(path, encoding="utf-8").read()
        assert doc.count("</style>") == 1
        doc = doc.replace("</style>", CSS_EXTRA + "</style>")
        for a, b in GLYPH.items():
            doc = doc.replace(a, b)
        io.open(path, "w", encoding="utf-8").write(doc)
        pdf = to_pdf(path)
        made.append((stem, path, pdf))
        print("  %-28s → %s" % (title, os.path.basename(pdf) if pdf else "✗ PDF 失败"))
    return made


if __name__ == "__main__":
    main()
