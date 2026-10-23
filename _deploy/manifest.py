# -*- coding: utf-8 -*-
"""发布前的体检：会公开什么、挡下了什么、还有没有漏网的敏感内容。

⚠ 推送到**公开**仓库是不可逆的（GitHub 会缓存、别人会 fork、搜索引擎会收录），
  所以这份清单要在 push 之前人眼过一遍。
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


def git(*a):
    """⚠ 必须用 -z：git 默认会把非 ASCII 路径**加引号并转成八进制转义**
    （"M1\\346\\235\\220\\346\\226\\231/..."），那样 os.path.getsize 一个都找不到，
    统计会静默变成 0。踩过一次：343 个文件只算出 0.1 MB。"""
    r = subprocess.run(("git",) + a + ("-z",), capture_output=True,
                       encoding="utf-8", errors="replace")
    return [p for p in r.stdout.split("\0") if p]


if not os.path.isdir(".git"):
    sys.exit("还没 git init —— 先跑 `git init`")

tracked = [p for p in git("ls-files", "-co", "--exclude-standard") if p]
ignored = [p for p in git("ls-files", "-o", "-i", "--exclude-standard") if p]


def tally(paths):
    n = collections.Counter()
    s = collections.Counter()
    tot = 0
    for p in paths:
        e = os.path.splitext(p)[1].lower() or "(无后缀)"
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        n[e] += 1
        s[e] += sz
        tot += sz
    return n, s, tot


n1, s1, t1 = tally(tracked)
n2, s2, t2 = tally(ignored)
print("═══ 会公开 ═══  %d 个文件，%.1f MB" % (len(tracked), t1 / 1024 ** 2))
for e, c in n1.most_common(10):
    print("   %-10s %5d 个 %8.1f MB" % (e, c, s1[e] / 1024 ** 2))
print("\n═══ 挡下了 ═══  %d 个文件，%.1f MB" % (len(ignored), t2 / 1024 ** 2))
top = collections.Counter()
for p in ignored:
    try:
        top[p.split("/")[0] if "/" in p else "(根目录)"] += os.path.getsize(p)
    except OSError:
        pass
for k, v in top.most_common(10):
    print("   %-28s %8.1f MB" % (k, v / 1024 ** 2))

# ── 会公开的文件里还有没有敏感内容 ──
print("\n═══ 对将要公开的文件复查敏感内容 ═══")
PAT = [
    ("联系方式（邮箱）", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:edu|com|org|net)"
                                   r"(?:\.[a-z]{2})?")),
    ("密码/口令", re.compile(r"(?i)(password|passwd|密码|口令)\s*[:=：]\s*\S{3,}")),
    ("凭据文件", re.compile(r"(?i)\.htpasswd|AuthUserFile|Authorization:\s*Basic")),
    ("密钥/令牌", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{30,}"
                             r"|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{30,}")),
    ("服务器地址", re.compile(r"(?i)aliyun|阿里云|\becs\b|rsync\s+-\w*\s+\S+@")),
]
TEXT = {".html", ".py", ".md", ".json", ".txt", ".js", ".css", ".yml",
        ".yaml", ".ipynb", ".tex", ".vtt"}
# 自己写的说明里会提到「密码」「阿里云」这些词，不算问题
SELF = ("_deploy/", "README.md")
bad = 0
for p in tracked:
    if os.path.splitext(p)[1].lower() not in TEXT:
        continue
    if p.startswith(SELF):
        continue
    try:
        s = io.open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for name, rx in PAT:
        for m in rx.finditer(s):
            g = m.group(0)
            # mailto: 形式的公开学术联系方式（论文作者）不拦；这里一个都不该有
            print("   ✗ %-46s %-12s %s" % (p[:46], name, g[:48]))
            bad += 1
            break
if not bad:
    print("   ✓ 没有命中")

# ── 大文件 ──
print("\n═══ 大文件（GitHub 超 50 MB 会警告、100 MB 拒收）═══")
big = sorted(((os.path.getsize(p), p) for p in tracked
              if os.path.exists(p)), reverse=True)[:5]
for sz, p in big:
    print("   %7.1f MB  %s" % (sz / 1024 ** 2, p))

print("\n%s" % ("✓ 可以发布" if not bad else "✗ 先处理上面的命中再发布"))
sys.exit(1 if bad else 0)
