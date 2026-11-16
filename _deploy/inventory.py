# -*- coding: utf-8 -*-
"""往 ★总入口.html 的维护区写一张**全量文件清单**。

为什么要有：原先有两个入口页 —— `★总入口.html`（243 条，精选导向）和
`全部材料.html`（721 条，全量目录，2026-10-29 另一个会话做的）。两个入口本身就是「乱」的来源。
2026-11-16 决定只留一个：把全量清单生成进总入口的维护区（默认折叠），然后删掉 全部材料.html。

⚠ 和 `build_matlist.py` 的分工：
  · build_matlist 管的是**学习材料**（课件 / 讲义 / Tutorial / 字幕），有逐条的人工说明；
  · 这里管的是**剩下的一切**（脚本、工具、库、原始字幕、构建产物），只给路径和大小，不写说明。
  两者都插在各自的哨兵之间，互不覆盖。

用法：python _deploy/inventory.py
"""
import collections
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
P = "★总入口.html"
BEGIN = "<!-- ══ 全量清单:BEGIN ══ -->"
END = "<!-- ══ 全量清单:END ══ -->"

# 已经被「材料清单」逐条点名的，这里不重复列
listed = set()
s0 = io.open(P, encoding="utf-8").read()
for h in re.findall(r'href="([^"#][^"]*)"', s0):
    listed.add(__import__("urllib.parse", fromlist=["unquote"]).unquote(h).split("?")[0])

GROUPS = [
    ("片子 · 生成脚本与体检工具", r"^复习放映厅/源码/"),
    ("逐页精读 · 生成器与内容源", r"^精读/.*\.py$"),
    ("逐页精读 · 数据与素材", r"^精读/(data|src)/"),
    ("打印资料 · 生成脚本", r"^M[123]材料/笔记与阅读/_src/"),
    ("公开课 · 原始字幕", r"^(CS229|CME295)/transcripts/"),
    ("公开课 · 抓取脚本", r"^(CS229|CME295)/.*\.py$"),
    ("发布工具链", r"^_deploy/"),
    ("前端库", r"^复习放映厅/lib/"),
]

allf = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
    for f in files:
        p = os.path.relpath(os.path.join(root, f), ".").replace("\\", "/")
        if p.startswith((".git", ".nojekyll")):
            continue
        try:
            allf.append((p, os.path.getsize(p)))
        except OSError:
            pass

rows, used = [], set()
for title, pat in GROUPS:
    rx = re.compile(pat)
    hit = sorted((p, z) for p, z in allf if rx.match(p) and p not in used)
    if not hit:
        continue
    used |= {p for p, _ in hit}
    rows.append((title, hit))

rest = sorted((p, z) for p, z in allf if p not in used and p not in listed)

html = [BEGIN,
        '<details class="mat">',
        '<summary>全量文件清单<span class="ct">%d 个文件 · %.0f MB</span></summary>'
        % (len(allf), sum(z for _, z in allf) / 1024 ** 2),
        '<div class="tl"><p class="lead">「材料清单」里已经逐条点名的学习材料不在这里重复；'
        '下面是工具链、脚本与原始素材。<b>2026-11-16 起这是唯一的入口页</b>，'
        '原先并存的 <code>全部材料.html</code> 已并入此处。</p>']
for title, hit in rows:
    html.append('<p><b>%s</b>（%d 个 · %.1f MB）</p><p class="lead" style="margin-top:2px">%s</p>'
                % (title, len(hit), sum(z for _, z in hit) / 1024 ** 2,
                   "、".join("<code>%s</code>" % os.path.basename(p) for p, _ in hit[:40])
                   + ("… 等" if len(hit) > 40 else "")))
if rest:
    html.append('<p><b>其它</b>（%d 个）</p><p class="lead" style="margin-top:2px">%s</p>'
                % (len(rest), "、".join("<code>%s</code>" % p for p, _ in rest[:60])))
html += ["</div></details>", END]
block = "\n".join(html)

s = s0
if BEGIN in s:
    s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, s, flags=re.S)
else:
    anchor = '<section id="build">'
    i = s.index(anchor)
    i = s.index("</p>", i) + 4            # 插在维护区那句 lead 之后
    s = s[:i] + "\n\n" + block + "\n" + s[i:]
io.open(P, "w", encoding="utf-8").write(s)
print("✓ 全量清单已写入维护区：%d 个文件 / %.1f MB，分 %d 组"
      % (len(allf), sum(z for _, z in allf) / 1024 ** 2, len(rows) + (1 if rest else 0)))
