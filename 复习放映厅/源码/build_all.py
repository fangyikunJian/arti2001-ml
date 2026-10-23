# -*- coding: utf-8 -*-
"""生成《全部材料总目》——把整个课程文件夹里的每一个文件都收进一张页面。

设计要点：**不漏是结构上保证的，不是靠人记**。
  1. 扫全盘 → 每个文件必须命中一条分类规则；
  2. 命中不了就进「⚠ 未分类」并在控制台报警（退出码非 0）；
  3. 页尾印一张完整性自检表：磁盘总数 == 各类之和。
描述文字从 ★总入口.html 里已经写好的卡片/文件行里抓过来复用，不重写。

跑法：在 复习放映厅/源码/ 下  python build_all.py
"""
import io, os, re, sys, html as H
from collections import OrderedDict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
OUT = "全部材料.html"
HUB = "★总入口.html"

# ── 不计入的构建产物 ────────────────────────────────────────────
def ignored(p):
    return ("/media/" in p or "/__pycache__/" in p or p.endswith(".pyc")
            or p.endswith(".DS_Store"))

# ── 分类规则：顺序敏感，先匹配先算 ──────────────────────────────
#    (类别键, 判定函数)
def R(pat):
    rx = re.compile(pat)
    return lambda p: bool(rx.match(p))

RULES = [
    ("入口",        lambda p: p in (HUB, OUT)),
    ("备份",        R(r"复习放映厅/_备份-修复前/")),
    ("字幕·VTT原始", R(r"CS229/transcripts/_vtt/")),
    ("字幕·旧版",    R(r"CS229/transcripts/_旧版/")),
    ("字幕·时间索引", R(r"CS229/transcripts/.*_timed\.txt$")),
    ("字幕·正文",    R(r"CS229/transcripts/.*\.txt$")),
    ("CS229讲义",   R(r"CS229/notes/")),
    ("工具",        R(r"CS229/.*\.py$")),
    ("精读·成品",    R(r"精读/.*-精读\.html$")),
    ("精读·骨架",    R(r"精读/_shell\.html$")),
    ("精读·数据",    R(r"精读/data/")),
    ("精读·左栏PDF", R(r"精读/slides/")),
    ("精读·素材",    R(r"精读/src/")),
    ("精读·生成器",  R(r"精读/.*\.py$")),
    ("短片",        R(r"复习放映厅/短片/")),
    ("英文版",      R(r"复习放映厅/en/")),
    ("英文版·源码",  R(r"复习放映厅/源码/en/")),
    ("片子·构建产物", R(r"复习放映厅/源码/.*\.html$")),
    ("片子·源码",    R(r"复习放映厅/源码/")),
    ("片子",        R(r"复习放映厅/影片/")),
    ("备考包",      R(r"复习放映厅/.*备考包.*\.html$")),
    ("片子",        R(r"复习放映厅/[^/]+\.html$")),
    ("说明文档",    R(r"复习放映厅/[^/]+\.md$")),
    ("M1材料",      R(r"M1材料/")),
    ("M2材料",      R(r"M2材料/")),
    ("M3材料",      R(r"M3材料/")),
    ("其它",        R(r"其它/")),
]

EXTS = (".html", ".pdf", ".txt", ".ipynb", ".pptx", ".mp4", ".py",
        ".json", ".md", ".csv", ".vtt", ".webp", ".png", ".jpg", ".svg")

# ── 扫盘 ───────────────────────────────────────────────────────
files = []
for dirpath, dirnames, filenames in os.walk("."):
    for fn in filenames:
        p = os.path.join(dirpath, fn)[2:].replace("\\", "/")
        if ignored("/" + p):
            continue
        if not fn.lower().endswith(EXTS):
            continue
        files.append(p)
files.sort()

buckets = OrderedDict()
unclassified = []
for p in files:
    for key, test in RULES:
        if test(p):
            buckets.setdefault(key, []).append(p)
            break
    else:
        unclassified.append(p)
        buckets.setdefault("⚠ 未分类", []).append(p)

# ── 从总入口抓已写好的描述 ──────────────────────────────────────
hub = io.open(HUB, encoding="utf-8").read()
desc = {}
for m in re.finditer(r'<a class="card v" href="([^"]+)">(.*?)</a>', hub, re.S):
    d = re.search(r'<div class="d">(.*?)</div>', m.group(2), re.S)
    if d:
        desc[H.unescape(m.group(1))] = d.group(1).strip()
for m in re.finditer(r'<a class="f[^"]*" href="([^"]+)">(.*?)</a>', hub, re.S):
    d = re.search(r'<span class="dd">(.*?)</span>', m.group(2), re.S)
    if d:
        desc.setdefault(H.unescape(m.group(1)), d.group(1).strip())
# 紧凑列表里的 <small>
for m in re.finditer(r'<a href="([^"]+)">([^<]*)<small>(.*?)</small></a>', hub):
    desc.setdefault(H.unescape(m.group(1)), m.group(3).strip())

import urllib.parse
linked_in_hub = {urllib.parse.unquote(x).rstrip("/")
                 for x in re.findall(r'href="([^"]+)"', hub)
                 if not x.startswith(("http", "#", "mailto"))}


def kb(n):
    return "%.1f MB" % (n / 1048576.0) if n >= 1048576 else "%d KB" % (n // 1024 or 1)


# ── 页面分区：(大标题, 导语, [(小标题, 类别键, 是否学习材料)]) ──
SECTIONS = [
 ("放映厅", "暗场电影式的逐知识点讲解。空格推进，每个知识点末尾有总结卡和一道必答测验。", [
   ("中文片子", "片子", True),
   ("Manim 短片", "短片", True),
   ("英文版（4 部原创英文片）", "英文版", True),
 ]),
 ("精读", "左栏是课件 / 讲义 PDF 原页，右栏是逐页讲解。每页配自测题，错题自动进错题本。", [
   ("精读成品", "精读·成品", True),
 ]),
 ("公开课 · CS229（吴恩达）", "21 讲全套字幕 + 官方讲义分册。字幕可全文搜索，讲义是精读的左栏来源。", [
   ("讲义 PDF", "CS229讲义", True),
   ("字幕 · 正文（整段可读）", "字幕·正文", True),
   ("字幕 · 时间索引（带时间码，用于定位）", "字幕·时间索引", True),
 ]),
 ("学校材料", "Canvas 上下载的官方课件、讲义、Tutorial 与 Practical。", [
   ("Module 1 · 监督学习", "M1材料", True),
   ("Module 2 · 无监督学习", "M2材料", True),
   ("Module 3 · 神经网络", "M3材料", True),
 ]),
 ("备考", "", [
   ("备考包与走查", "备考包", True),
 ]),
 ("工具与源码", "要改内容、补讲次、重新生成时看这里。平时不用点。", [
   ("工具脚本", "工具", False),
   ("片子源码与素材", "片子·源码", False),
   ("精读生成器", "精读·生成器", False),
   ("精读数据（JSON）", "精读·数据", False),
   ("精读左栏 PDF（讲义副本）", "精读·左栏PDF", False),
   ("精读素材", "精读·素材", False),
   ("精读骨架", "精读·骨架", False),
   ("英文版源码", "英文版·源码", False),
   ("说明文档", "说明文档", False),
 ]),
 ("重复副本与历史存档", "这些不用看：要么是别处同一份文件的副本，要么是被取代的旧版本。列在这里只为「不漏」。", [
   ("片子构建产物（与「中文片子」同内容，改名前的）", "片子·构建产物", False),
   ("字幕 · VTT 原始文件", "字幕·VTT原始", False),
   ("字幕 · 旧版", "字幕·旧版", False),
   ("修复前的备份", "备份", False),
   ("其它（与本课无关）", "其它", False),
   ("入口页本身", "入口", False),
 ]),
]

# ── 生成 ───────────────────────────────────────────────────────
m = re.search(r"<head>(.*?)</head>", hub, re.S)
head = m.group(1)
head = re.sub(r"<title>.*?</title>", "<title>全部材料总目 · ARTI2001</title>", head, flags=re.S)

EXTRA = """
<style>
.allsec{margin:34px 0 0}
.allsec>h2{font-size:25px;margin:0 0 6px;letter-spacing:.3px}
.allsec>p.lead{margin:0 0 14px;color:var(--dim);font-size:14px;line-height:1.75}
.grp{margin:16px 0 0;border:1px solid var(--line);border-radius:12px;
     background:var(--panel);overflow:hidden}
.grp>h3{margin:0;padding:11px 16px;font-size:15px;background:var(--panel2);
        border-bottom:1px solid var(--line);font-weight:600}
.grp>h3 .ct{float:right;color:var(--dim);font-weight:400;font-size:13px}
.grp ul{list-style:none;margin:0;padding:0}
.grp li{display:flex;gap:10px;align-items:baseline;padding:7px 16px;
        border-top:1px solid var(--line);font-size:13.5px;line-height:1.6}
.grp li:first-child{border-top:none}
.grp li:nth-child(even){background:var(--stripe)}
.grp li a{color:var(--blue);text-decoration:none;flex:0 0 auto;max-width:46%;
          word-break:break-all}
.grp li a:hover{text-decoration:underline}
.grp li .sz{color:var(--dimmer);font-size:12px;flex:0 0 auto;min-width:56px;text-align:right}
.grp li .dd{color:var(--dim);font-size:12.5px;flex:1 1 auto}
.grp.aux li a{color:var(--dim)}
.sumtbl td,.sumtbl th{font-size:13px}
.big{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 6px}
.big div{flex:1 1 150px;border:1px solid var(--line);border-radius:11px;
         background:var(--panel);padding:13px 15px}
.big b{display:block;font-size:27px;line-height:1.2;color:var(--ink2)}
.big span{color:var(--dim);font-size:12.5px}
.warnbox{border-left:3px solid var(--coral);background:var(--tcoral);
         padding:11px 15px;border-radius:9px;margin:14px 0;font-size:13.5px}
</style>
"""

B = []
A = B.append
A("<!doctype html><html lang=\"zh-CN\"><head>" + head + EXTRA + "</head><body>")
A('<div class="wrap">')
A('<h1 style="margin:22px 0 4px">全部材料总目</h1>')
A('<p class="lead" style="margin:0 0 4px;color:var(--dim)">'
  '这一页由 <code>复习放映厅/源码/build_all.py</code> <b>扫描整个课程文件夹自动生成</b>——'
  '每个文件都必须落进下面某一类，落不进就会在页尾的自检表里报出来。'
  '<b>所以它不会漏。</b></p>')
A('<p class="lead" style="margin:0 0 10px;color:var(--dim)">'
  '想要有讲解、有顺序的学习路径，回 <a href="%s" style="color:var(--blue)">★总入口</a>；'
  '这一页是<b>穷尽式清单</b>，用来找东西和确认什么都在。</p>' % H.escape(HUB))

n_study = sum(len(buckets.get(k, [])) for _, _, gs in SECTIONS for _, k, s in gs if s)
n_all = len(files)
A('<div class="big">')
A('<div><b>%d</b><span>文件总数</span></div>' % n_all)
A('<div><b>%d</b><span>学习材料</span></div>' % n_study)
A('<div><b>%d</b><span>放映厅片子</span></div>'
  % (len(buckets.get("片子", [])) + len(buckets.get("英文版", []))))
A('<div><b>%d</b><span>精读</span></div>' % len(buckets.get("精读·成品", [])))
A('<div><b>%d</b><span>CS229 讲次</span></div>' % len(buckets.get("字幕·正文", [])))
A('</div>')

if unclassified:
    A('<div class="warnbox"><b>⚠ 有 %d 个文件没能分类</b>，见页尾。'
      '这说明分类规则需要补——不是文件有问题。</div>' % len(unclassified))

used = set()
for title, lead, groups in SECTIONS:
    rows = [(st, k, is_study) for st, k, is_study in groups if buckets.get(k)]
    if not rows:
        continue
    A('<div class="allsec"><h2>%s</h2>' % H.escape(title))
    if lead:
        A('<p class="lead">%s</p>' % lead)
    for subtitle, key, is_study in rows:
        ps = buckets[key]
        used.add(key)
        A('<div class="grp%s"><h3>%s<span class="ct">%d 个</span></h3><ul>'
          % ("" if is_study else " aux", H.escape(subtitle), len(ps)))
        for p in ps:
            try:
                sz = kb(os.path.getsize(p))
            except OSError:
                sz = "—"
            d = desc.get(p, "")
            d = re.sub(r"\s+", " ", d).strip()
            if len(d) > 150:
                d = d[:150] + "…"
            A('<li><a href="%s">%s</a><span class="sz">%s</span>'
              '<span class="dd">%s</span></li>'
              % (urllib.parse.quote(p), H.escape(os.path.basename(p)), sz, d))
        A("</ul></div>")
    A("</div>")

# ── 完整性自检 ─────────────────────────────────────────────────
A('<div class="allsec"><h2>完整性自检</h2>')
A('<p class="lead">各类之和必须等于磁盘总数，否则就是漏了。</p>')
A('<table class="sumtbl"><tr><th>类别</th><th>个数</th><th>在总入口里挂了</th></tr>')
tot = 0
for key, ps in buckets.items():
    tot += len(ps)
    inhub = sum(1 for p in ps if p in linked_in_hub)
    A("<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % (H.escape(key), len(ps), inhub))
A("<tr><td><b>合计</b></td><td><b>%d</b></td><td>%d</td></tr>" % (tot, len(linked_in_hub)))
A("</table>")
ok = (tot == n_all and not unclassified)
A('<p style="margin:12px 0 0;font-size:14px;color:var(--%s)"><b>%s</b></p>'
  % ("green" if ok else "coral",
     ("✓ 磁盘 %d 个文件，全部归类，一个不少。" % n_all) if ok
     else ("✗ 磁盘 %d 个，归类 %d 个，未分类 %d 个。" % (n_all, tot, len(unclassified)))))
if unclassified:
    A("<ul>" + "".join("<li><code>%s</code></li>" % H.escape(p)
                       for p in unclassified) + "</ul>")
A("</div>")
A('<p style="margin:30px 0 40px;color:var(--dimmer);font-size:12.5px">'
  '本页自动生成，不要手改——改了下次重跑就没了。'
  '要调整分类或措辞，改 <code>复习放映厅/源码/build_all.py</code> 再重跑。</p>')
A("</div></body></html>")

io.open(OUT, "w", encoding="utf-8").write("\n".join(B))

# ── 控制台报告 ─────────────────────────────────────────────────
print("%s：%d 字符" % (OUT, sum(len(x) for x in B)))
print("磁盘 %d 个文件 → 归类 %d 个，未分类 %d 个" % (n_all, tot, len(unclassified)))
for key, ps in buckets.items():
    print("  %-14s %4d" % (key, len(ps)))
unused = [k for _, _, gs in SECTIONS for _, k, _ in gs if k not in used and buckets.get(k)]
if unused:
    print("⚠ 有类别没被任何分区展示：", unused)
if unclassified:
    print("⚠ 未分类：")
    for p in unclassified:
        print("   ", p)
    sys.exit(1)
print("✓ 一个不漏")
