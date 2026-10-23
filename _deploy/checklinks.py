# -*- coding: utf-8 -*-
"""交叉核对：总入口里被标成「仅本地」的链接，和 git 实际挡下的文件，必须是同一批。

两种错法都要查出来：
  · **漏标** —— 文件没进仓库，链接却还是可点的 ⇒ 公开站上一个 404
  · **错标** —— 文件明明发布了，链接却被划掉 ⇒ 白白让人点不到

匹配规则必须和 `apply.py` 注入的那段 JS 完全一致，所以这里照抄它的写法
（前缀以 `/` 结尾按目录前缀比，否则按整串相等）。
"""
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import rules  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def git(*a):
    r = subprocess.run(("git",) + a + ("-z",), capture_output=True,
                       encoding="utf-8", errors="replace")
    return {p for p in r.stdout.split("\0") if p}


published = git("ls-files", "-co", "--exclude-standard")


def would_mark(href):
    """和 apply.py 里的 hit() 同一套判据。"""
    p = urllib.parse.unquote(href)
    p = re.sub(r"^\./", "", p).split("?")[0].split("#")[0]
    for m in rules.MISSING_PREFIXES:
        if (p.startswith(m) if m.endswith("/") else p == m):
            return True
    return False


s = open("★总入口.html", encoding="utf-8").read()
hrefs = [h for h in re.findall(r'href="([^"]+)"', s)
         if not h.startswith(("http", "mailto", "#"))]

missed, wrong, ok_marked = [], [], 0
for h in sorted(set(hrefs)):
    path = urllib.parse.unquote(h).split("?")[0].split("#")[0]
    on_disk = os.path.exists(path)
    in_repo = path in published or (
        os.path.isdir(path) and any(q.startswith(path.rstrip("/") + "/")
                                    for q in published))
    mark = would_mark(h)
    if mark:
        ok_marked += 1
        if in_repo:
            wrong.append((h, "文件其实发布了，却被标成仅本地"))
    else:
        if on_disk and not in_repo:
            missed.append((h, "没进仓库却没被标 ⇒ 公开站 404"))

print("总入口本地链接 %d 条（去重后 %d）" % (len(hrefs), len(set(hrefs))))
print("  公开站会标成「仅本地」：%d 条" % ok_marked)
print("  漏标（会 404）：%d 条" % len(missed))
for h, why in missed[:20]:
    print("     ✗ %-62s %s" % (h[:62], why))
print("  错标（其实能点）：%d 条" % len(wrong))
for h, why in wrong[:20]:
    print("     ✗ %-62s %s" % (h[:62], why))

bad = len(missed) + len(wrong)
print("\n%s" % ("✓ 两边完全对得上" if not bad else "✗ 有 %d 条对不上" % bad))
sys.exit(1 if bad else 0)
