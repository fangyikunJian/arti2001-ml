# -*- coding: utf-8 -*-
"""查一部片子有没有「顺着字幕从头走到尾、中间不跳段」。

为什么要有这个工具（2026-11-03）：
  用户看完 CME295 L1–L7 的评价是「**内容太少了，不是逐帧字幕讲解的**」。
  量出来的确如此：CS229 那批（用户认可过）平均 **每镜扛 13.5 句字幕**，
  而 CME295 是 **18.8 句**（L7 最糟 22.1 句）。
  根子是质量线用错了：`≥25 KP / ≥45 镜` 是**绝对**线，而 CME295 一讲 107 分钟、
  比 CS229 的 75 分钟长 40% —— 同样的镜数摊在更长的讲座上，密度就被稀释了。
  ⇒ 质量线必须是**密度线**。

本工具把「逐段不跳」变成可验证的东西，判据有三条：
  ① 密度：讲解镜数 ≥ 字幕句数 / MAX_LINES_PER_SHOT
  ② 顺序：says() 的时间码必须**单调递增**（顺着讲座走，不来回跳）
  ③ 不跳段：相邻两条 says() 的间隔 ≤ MAX_GAP 秒；并报出所有超标的空洞

  用法：
    python tools/coverage.py CME295 L1 cme295-L1.html
    python tools/coverage.py --all CME295        # 扫该课全部已建片子
"""
import argparse, glob, io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:/Adelaide COMSC/2026S2/Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码")

# ── 判据的两个常数 ──────────────────────────────────────────────
MAX_LINES_PER_SHOT = 6.0   # 每个讲解镜最多扛 6 句字幕（CS229 那批是 13.5，这里要严得多）
MAX_GAP = 90               # 相邻两条讲者原话之间最多隔 90 秒，超了就是跳段了

SHOT = re.compile(r"S\(\d+,function")
KPRE = re.compile(r'KP\("')
# ⚠ 场景 JS 是原样插进 html 的，所以这里是 says("11:03","…")，
#   不是渲染后的「Amidi 11:03」。
SAYS = re.compile(r'says\(\s*"(\d+):(\d\d)"')


def mmss(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


def lecture_seconds(course, tag):
    """从 _vtt 里读出这一讲的总时长（最后一条 cue 的结束时间）。"""
    pats = os.path.join(ROOT, course, "transcripts", "_vtt", "*.vtt")
    best = 0
    # ⚠ 视频 id 在 `L<n>.txt` 的第二行（`# https://…v=<id>`），不在 _timed.txt 里
    head = os.path.join(ROOT, course, "transcripts", "%s.txt" % tag)
    vid = None
    if os.path.exists(head):
        m = re.search(r"v=([A-Za-z0-9_-]{11})",
                      io.open(head, encoding="utf-8").read(400))
        if m:
            vid = m.group(1)
    for p in glob.glob(pats):
        if vid and vid not in os.path.basename(p):
            continue
        for m in re.finditer(r"-->\s*(\d+):(\d\d):(\d\d)", io.open(p, encoding="utf-8").read()):
            s = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            best = max(best, s)
        if vid:
            break
    return best


def check(course, tag, html):
    path = html if os.path.isabs(html) else os.path.join(SRC, html)
    h = io.open(path, encoding="utf-8").read()
    sub = [l for l in io.open(os.path.join(ROOT, course, "transcripts", "%s.txt" % tag),
                             encoding="utf-8").read().splitlines()
           if l.strip() and not l.startswith("#")]
    shots = len(SHOT.findall(h))
    kps = len(KPRE.findall(h))
    anchors = [int(a) * 60 + int(b) for a, b in SAYS.findall(h)]
    total = lecture_seconds(course, tag)

    bad = []
    # ① 密度
    need = int(len(sub) / MAX_LINES_PER_SHOT + 0.999)
    dens = len(sub) / shots if shots else 999
    if shots < need:
        bad.append("① 密度不够：%d 句字幕要求 ≥%d 镜，现在只有 %d 镜（每镜扛 %.1f 句，上限 %.0f）"
                   % (len(sub), need, shots, dens, MAX_LINES_PER_SHOT))
    # ② 顺序
    for i in range(1, len(anchors)):
        if anchors[i] < anchors[i - 1]:
            bad.append("② 第 %d 条原话时间码回退：%s 之后出现了 %s"
                       % (i + 1, mmss(anchors[i - 1]), mmss(anchors[i])))
            break
    # ③ 不跳段
    gaps = []
    seq = [0] + sorted(anchors) + ([total] if total else [])
    for i in range(1, len(seq)):
        g = seq[i] - seq[i - 1]
        if g > MAX_GAP:
            gaps.append((seq[i - 1], seq[i], g))
    for a, b, g in gaps:
        bad.append("③ %s → %s 这 %d 秒没有任何讲者原话锚点（上限 %d 秒）"
                   % (mmss(a), mmss(b), g, MAX_GAP))

    ok = "✓ 通过" if not bad else "✗ %d 项" % len(bad)
    print("%-22s 字幕 %4d 句  KP %3d  镜 %3d  每镜 %4.1f 句  原话 %3d 条  %s"
          % (os.path.basename(path), len(sub), kps, shots, dens, len(anchors), ok))
    for b in bad[:12]:
        print("   " + b)
    if len(bad) > 12:
        print("   …… 另有 %d 项同类问题" % (len(bad) - 12))
    return len(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("tag", nargs="?")
    ap.add_argument("html", nargs="?")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        n = 0
        pre = a.course.lower()
        for p in sorted(glob.glob(os.path.join(SRC, "%s-L*.html" % pre))):
            tag = re.search(r"-(L\d+)\.html$", p).group(1)
            n += check(a.course, tag, p)
        print("\n合计 %d 个问题" % n)
        sys.exit(1 if n else 0)
    n = check(a.course, a.tag, a.html)
    print("\n合计 %d 个问题" % n)
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
