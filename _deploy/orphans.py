# -*- coding: utf-8 -*-
"""找出「磁盘上有、但 ★总入口.html 点不到」的成品页面。

为什么要有（2026-11-17）：CME295 的 L2/L3/L4/L5 四份深度笔记在磁盘上躺了一周，
总入口从没链过 —— L1 那张卡只在**描述文字里用散文写了文件名**，要手敲路径才打得开。
这种断链肉眼翻页面是发现不了的（页面看上去满满当当），只能靠对账。

判据：影片/ 短片/ 备考/ en/ 精读/ 底下的成品（.html/.mp4），
      凡是没出现在总入口任何一个 href 里的，都报出来。

⚠ `影片/_旧稿/` 是**故意**不链的（被取代的早期版本），单独列成一组，不算问题。

用法：python _deploy/orphans.py
"""
import io
import os
import re
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def hrefs(path):
    """一个本地 HTML 里指向本地文件的链接，统一成相对仓库根的正斜杠路径。"""
    try:
        s = io.open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out = []
    d = os.path.dirname(path)
    for h in re.findall(r'href="([^"#][^"]*)"', s):
        h = urllib.parse.unquote(h).split("?")[0]
        if h.startswith(("http:", "https:", "mailto:", "data:")):
            continue
        out.append(os.path.normpath(os.path.join(d, h)).replace(os.sep, "/"))
    return out


# ⚠ 不能只看总入口的直接链接 —— 英文版那四部是通过 en/index.html 到达的，
#   只查一层会把它们误报成断链。所以从总入口出发做**可达性**遍历。
linked, queue = set(), ["★总入口.html"]
while queue:
    cur = queue.pop()
    for p in hrefs(cur):
        if p in linked:
            continue
        linked.add(p)
        if p.endswith(".html") and os.path.exists(p):
            queue.append(p)

SCAN = ["复习放映厅/影片", "复习放映厅/短片", "复习放映厅/备考", "复习放映厅/en", "精读"]
EXPECTED_ORPHAN = "复习放映厅/影片/_旧稿/"      # 故意不链
# 不是成品，是生成器用的外壳模板 —— 单独点名排除，别用后缀规则，
# 免得将来真有叫 _xxx 的成品也被悄悄漏掉。
TEMPLATES = {"精读/_shell.html"}

orphans, deliberate = [], []
for base in SCAN:
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ("lib", "data", "src", "__pycache__")]
        for f in files:
            if not f.endswith((".html", ".mp4")):
                continue
            p = os.path.join(root, f).replace(os.sep, "/")
            if p in linked or p in TEMPLATES:
                continue
            (deliberate if p.startswith(EXPECTED_ORPHAN) else orphans).append(p)

for p in sorted(deliberate):
    print("  ·（故意不链·旧稿）", p)
print()
if orphans:
    print("✗ 点不到的成品 %d 个：" % len(orphans))
    for p in sorted(orphans):
        print("   ", p, "%.0f KB" % (os.path.getsize(p) / 1024))
else:
    print("✓ 没有断链：每一个成品页面都能从总入口点到")

# ── ② 首页「这学期留下了什么」那条统计，和磁盘对账 ────────────
# ⚠ 2026-11-17 查出它写「53 部」而自己的分项是 15+22+13=50，两边都不对，
#   而且英文版 4 部根本没算进去。这种数字飘了没人看得出来，所以写成检查。
import glob

hub = io.open("★总入口.html", encoding="utf-8").read()


def n(pat):
    return len(glob.glob(pat))


films = {"本课": n("复习放映厅/影片/本课M1/*.html") + n("复习放映厅/影片/本课M2/*.html")
                 + n("复习放映厅/影片/本课M3/*.html"),
         "CS229": n("复习放映厅/影片/CS229/*.html"),
         "CME295": n("复习放映厅/影片/CME295/*.html"),
         "英文版": n("复习放映厅/en/*.html") - 1}          # 减掉 index.html
readers = len([f for f in glob.glob("精读/*.html")
               if not os.path.basename(f).startswith("_")])
tot = sum(films.values())
bad = []
for label, want in [("%d 部动画片子" % tot, tot), ("%d 份逐页精读" % readers, readers)]:
    if label not in hub:
        bad.append(label)
for k, v in films.items():
    if "%s %d 部" % (k, v) not in hub:
        bad.append("%s %d 部" % (k, v))
print("\n② 首页统计对账：片子 %d（%s）· 精读 %d —— %s"
      % (tot, " + ".join("%s %d" % kv for kv in films.items()), readers,
         "全部对得上 ✓" if not bad else "✗ 首页上找不到这些写法：%s" % bad))
sys.exit(1 if (orphans or bad) else 0)
