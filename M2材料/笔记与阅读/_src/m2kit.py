# -*- coding: utf-8 -*-
"""M2 复习资料的排版工具：把结构化内容渲染成**适合打印**的 HTML，再由 Chrome 转 PDF。

体例对齐 M1材料/笔记与阅读/ 里那几份（封面 → 目录 → 按讲义页编号的章节 →
★考点 / ⚠ / Study check / 手算例题 → Tutorial 与 Practical 全解 →
附录 A 公式速查 / B 易错点 / C 术语中英对照）。

设计要点
  · A4 + 16mm 页边距，正文 10.5pt —— 和 M1 那批打印出来的密度接近。
  · 表格、题组、提示框都加 break-inside:avoid，免得一张表被切成两页。
  · 不依赖任何 CDN：公式用 HTML 上下标写，不用 MathJax（打印更稳，且离线可用）。
  · 行内标记：**粗体**、`等宽`、~~下标~~ 用 _{...}，上标用 ^{...}。
"""
import html as H
import io
import os
import re
import subprocess
import sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = r"""
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
@page { @bottom-center { content: counter(page); font-size:9pt; color:#8a97aa } }
@page :first { @bottom-center { content: "" } }
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact}
body{font-family:"Microsoft YaHei","Segoe UI",system-ui,sans-serif;
     font-size:10.5pt; line-height:1.62; color:#14181f; margin:0}
code,.mono{font-family:"Consolas","Cascadia Mono","Courier New",monospace;
   font-size:.92em; background:#eef1f6; color:#13365e; font-weight:600;
   padding:0 1.6px; border-radius:2px}

/* ── 封面 ── */
.cover{text-align:center; padding-top:52mm; page-break-after:always}
.cover h1{font-size:30pt; margin:0 0 4mm; letter-spacing:.04em}
.cover .sub{font-size:14pt; color:#334; margin:0 0 2mm}
.cover .course{font-size:11pt; color:#667; margin:0 0 14mm}
.cover .cov{display:inline-block; text-align:left; border:1px solid #b9c2d0;
     border-radius:6px; padding:6mm 9mm; font-size:10pt; line-height:1.9; background:#f7f9fc}
.cover .cov b{color:#1b3a63}
.cover .mate{margin-top:10mm; font-size:9.5pt; color:#778}

/* ── 目录 ── */
.toc{page-break-after:always}
.toc h2{border:none; margin-top:0}
.toc ol{list-style:none; padding-left:0; font-size:11pt; line-height:2.05}
.toc ol ol{font-size:10pt; line-height:1.75; color:#445; padding-left:7mm; margin:1mm 0 2mm}
.toc ol ol li::before{content:"· "; color:#8a97aa}

/* ── 标题 ── */
h2{font-size:15pt; margin:9mm 0 3mm; padding:2mm 0 1.6mm;
   border-bottom:2.2px solid #1b3a63; color:#1b3a63; page-break-after:avoid}
h3{font-size:12.2pt; margin:6mm 0 2mm; color:#20456f; page-break-after:avoid}
h4{font-size:11pt; margin:4.5mm 0 1.5mm; color:#2d4a6b; page-break-after:avoid}
h2 .pg{float:right; font-size:9.5pt; font-weight:400; color:#7a8698; padding-top:2.4mm}
p{margin:0 0 2.4mm; text-align:justify}
ol{margin:0 0 2.8mm; padding-left:6.5mm}
ul{margin:0 0 2.8mm; padding-left:5mm; list-style:none}
ul>li::before{content:"▪"; color:#4a73a8; display:inline-block;
              width:4mm; margin-left:-4mm}
li{margin:.9mm 0}
b,strong{color:#0d2b4e}

/* ── 表格 ── */
table{border-collapse:collapse; width:100%; margin:2.5mm 0 4mm; font-size:9.8pt;
      break-inside:avoid; page-break-inside:avoid}
th,td{border:1px solid #c3ccd9; padding:1.5mm 2.2mm; vertical-align:top}
th{background:#e8eef7; color:#12355c; font-weight:600; text-align:left}
tr:nth-child(even) td{background:#fafbfd}
td.n,th.n{text-align:right; font-variant-numeric:tabular-nums;
   font-feature-settings:"tnum" 1; letter-spacing:.2px}
table.tight td,table.tight th{padding:1.1mm 1.8mm; font-size:9.3pt}

/* ── 公式 ── */
.eq{margin:2.5mm 0 3mm; padding:2.4mm 4mm; background:#f4f7fb; border-left:3.5px solid #4a73a8;
    font-family:"Cambria Math","Cascadia Mono",Consolas,serif; font-size:10.6pt;
    break-inside:avoid; white-space:pre-wrap}
.eq .lbl{display:block; font-family:inherit; font-size:8.8pt; color:#6b7policy}
sub{font-size:.72em} sup{font-size:.72em}

/* ── 提示框 ── */
.cal{margin:3mm 0; padding:2.6mm 3.6mm; border-radius:4px; break-inside:avoid;
     page-break-inside:avoid; font-size:10.1pt}
.cal .ttl{font-weight:700; display:block; margin-bottom:1.2mm}
.cal p:last-child{margin-bottom:0}
.k{background:#fff6e0; border:1px solid #e3b43a; border-left:4px solid #e3b43a}      /* ★ 考点 */
.k .ttl{color:#8a5a00}
.w{background:#fdeeee; border:1px solid #d77; border-left:4px solid #d77}            /* ⚠ 易错 */
.w .ttl{color:#9a2222}
.t{background:#edf7ee; border:1px solid #6aa96f; border-left:4px solid #6aa96f}      /* ⭐ 技巧 */
.t .ttl{color:#1f6128}
.s{background:#eef2fa; border:1px solid #93a7c9; border-left:4px solid #5878ab}      /* Study check */
.s .ttl{color:#23456f}
.ng{background:#f3eefb; border:1px solid #9a84c4; border-left:4px solid #7a5fb0}     /* CS229 旁注 */
.ng .ttl{color:#4c327f}

/* ── 手算例题 ── */
.ex{margin:3.5mm 0 4.5mm; border:1px solid #9fb3cc; border-radius:5px}
.ex>.hd{break-after:avoid; page-break-after:avoid}
.ex>.hd{background:#1b3a63; color:#fff; padding:1.8mm 3.4mm; font-weight:600; font-size:10.4pt}
.ex>.bd{padding:3mm 3.6mm}
.ex>.bd>:last-child{margin-bottom:0}
.step{margin:2mm 0; padding-left:5.5mm; border-left:2px solid #c3ccd9;
   break-inside:avoid; page-break-inside:avoid}
.step .sn{font-weight:700; color:#1b3a63; margin-right:1.5mm}

/* ── 题库 ── */
.qg{margin:4mm 0 5mm; break-inside:avoid-page}
.qg>.hd{background:#20456f; color:#fff; padding:1.6mm 3.2mm; font-weight:600;
        font-size:10.5pt; border-radius:4px 4px 0 0}
.qg>.bd{border:1px solid #9fb3cc; border-top:none; border-radius:0 0 4px 4px; padding:2.6mm 3.4mm}
.q{margin:0 0 3mm; break-inside:avoid}
.q .qt{font-weight:600; margin-bottom:1.2mm}
.q .op{padding-left:6mm; font-size:10pt; line-height:1.75}
.ans{margin-top:2.5mm; padding:2.4mm 3mm; background:#f6f8fb; border-top:1.5px dashed #9fb3cc;
     font-size:9.8pt}
.ans .ttl{font-weight:700; color:#1b3a63; display:block; margin-bottom:1.2mm}
.ans .a{margin:1.1mm 0}
.ans .a b{color:#1f6128}

.pb{page-break-before:always}
.nb{page-break-inside:avoid}
hr.sep{border:none; border-top:1px solid #d6dde7; margin:5mm 0}
.note{font-size:9.4pt; color:#5a6676; margin:1.5mm 0 3mm}
"""
CSS = CSS.replace("#6b7policy", "#6b7686")   # 防手滑

_SUB = re.compile(r"_\{([^}]*)\}")
_SUP = re.compile(r"\^\{([^}]*)\}")
_B = re.compile(r"\*\*(.+?)\*\*", re.S)
_C = re.compile(r"`([^`]+)`")


def mk(s):
    """行内标记 → HTML。先转义，再按 **粗** / `码` / _{下标} / ^{上标} 还原。"""
    s = H.escape(s, quote=False)
    s = _C.sub(lambda m: "<code>%s</code>" % m.group(1), s)
    s = _B.sub(lambda m: "<b>%s</b>" % m.group(1), s)
    s = _SUB.sub(lambda m: "<sub>%s</sub>" % m.group(1), s)
    s = _SUP.sub(lambda m: "<sup>%s</sup>" % m.group(1), s)
    return s


# ─────────────────────── 构件 ───────────────────────
def P(t):            return "<p>%s</p>" % mk(t)
def NOTE(t):         return '<p class="note">%s</p>' % mk(t)
def H3(t, pg=None):  return "<h3>%s</h3>" % mk(t)
def H4(t):           return "<h4>%s</h4>" % mk(t)


def H2(t, pg=None):
    tag = '<span class="pg">%s</span>' % mk(pg) if pg else ""
    return "<h2>%s%s</h2>" % (tag, mk(t))


def UL(items, ordered=False):
    tag = "ol" if ordered else "ul"
    return "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % mk(i) for i in items), tag)


def EQ(*lines):
    return '<div class="eq">%s</div>' % "<br>".join(mk(l) for l in lines)


def TB(head, rows, tight=False, numcols=()):
    cls = ' class="tight"' if tight else ""
    th = "".join('<th%s>%s</th>' % (' class="n"' if j in numcols else "", mk(c))
                 for j, c in enumerate(head))
    tr = ""
    for r in rows:
        tds = "".join('<td%s>%s</td>' % (' class="n"' if j in numcols else "", mk(c))
                      for j, c in enumerate(r))
        tr += "<tr>%s</tr>" % tds
    return "<table%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (cls, th, tr)


def CAL(kind, title, *body):
    """kind: k=★考点 w=⚠易错 t=⭐技巧 s=Study check ng=CS229 旁注"""
    inner = "".join(b if b.startswith("<") else P(b) for b in body)
    return '<div class="cal %s"><span class="ttl">%s</span>%s</div>' % (kind, mk(title), inner)


def EX(title, *body):
    inner = "".join(b if b.startswith("<") else P(b) for b in body)
    return '<div class="ex"><div class="hd">%s</div><div class="bd">%s</div></div>' % (mk(title), inner)


def STEP(n, *body):
    inner = "".join(b if b.startswith("<") else P(b) for b in body)
    return '<div class="step"><span class="sn">%s</span>%s</div>' % (mk(n), inner)


def QG(title, items):
    """题组。items = [(题干, [四个选项], 正确下标, 解析), ...]"""
    qs, ans = "", ""
    for i, (q, ops, a, why) in enumerate(items, 1):
        ophtml = "<br>".join("%s. %s" % ("ABCD"[j], mk(o)) for j, o in enumerate(ops))
        qs += '<div class="q"><div class="qt">%d. %s</div><div class="op">%s</div></div>' % (i, mk(q), ophtml)
        ans += '<div class="a"><b>%d. %s</b> —— %s</div>' % (i, "ABCD"[a], mk(why))
    return ('<div class="qg"><div class="hd">%s</div><div class="bd">%s'
            '<div class="ans"><span class="ttl">答案与解析</span>%s</div></div></div>'
            % (mk(title), qs, ans))


def PB():
    return '<div class="pb"></div>'


# ─────────────────────── 文档 ───────────────────────
def build(path, title, sub, cover_lines, toc, body, mate=""):
    cov = "<br>".join(mk(l) for l in cover_lines)
    def toc_html(items, top=True):
        out = "<ol>"
        for it in items:
            if isinstance(it, tuple):
                out += "<li>%s%s</li>" % (mk(it[0]), toc_html(it[1], False))
            else:
                out += "<li>%s</li>" % mk(it)
        return out + "</ol>"
    doc = (
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        "<title>%s</title><style>%s</style></head><body>"
        '<div class="cover"><h1>%s</h1><p class="sub">%s</p>'
        '<p class="course">ARTI2001 Machine Learning · 2026 Semester 2</p>'
        '<div class="cov">%s</div><p class="mate">%s</p></div>'
        '<div class="toc"><h2>目录</h2>%s</div>'
        "%s</body></html>"
        % (H.escape(title), CSS, mk(title), mk(sub), cov, mk(mate), toc_html(toc), "".join(body))
    )
    io.open(path, "w", encoding="utf-8").write(doc)
    return path


def to_pdf(html_path):
    pdf = os.path.splitext(html_path)[0] + ".pdf"
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", "--print-to-pdf=" + pdf,
                        "--virtual-time-budget=8000", html_path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not os.path.exists(pdf):
        print("✗ 生成 PDF 失败：", (r.stderr or "")[-500:])
        return None
    return pdf
