# -*- coding: utf-8 -*-
"""在 CS229 全部字幕里查一句话，返回「讲次 + 时间码 + 可点链接」。

写 精读/deepen_*.py 的 ng 栏（「从零补基础 · Andrew Ng CS229」）时用它核对引用位置。
⚠ 时间码必须这样反查，不能凭印象填 —— 2026-09-28 做 L15 片子时凭印象填的
   47 处时间码里大部分是错的（把 49:07 的内容标成了 2 分钟处）。

用法：
    python find_quote.py "coordinate descent"          # 全部讲次里找
    python find_quote.py "covariance matrix" L15       # 只在 L15 里找
    python find_quote.py --at L15 2947                 # 反查：L15 第 2947 秒讲的是什么
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(HERE, "transcripts")

VID = {}
for line in io.open(os.path.join(HERE, "fetch_transcripts.py"), encoding="utf-8"):
    m = re.match(r'\s*\("([\w]+)",\s*"([\w-]+)"', line)
    if m:
        VID[m.group(1)] = m.group(2)


def load(tag):
    """返回 [(秒, 该条文本)]，以及全文行列表。"""
    tp = os.path.join(TDIR, tag + "_timed.txt")
    fp = os.path.join(TDIR, tag + ".txt")
    idx = []
    if os.path.exists(tp):
        raw = [l.rstrip("\n") for l in io.open(tp, encoding="utf-8")]
        # 格式 A（本脚本自己生成的）：`[mm:ss] 文本` 内联一行
        for ln in raw:
            m = re.match(r"\[(\d+):(\d\d)\]\s*(.*)", ln.strip())
            if m:
                idx.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3)))
        # 格式 B（从 YouTube 页面直接拷下来的）：**时间码单独占一行**，文本在后面几行。
        # ⚠ 2026-10-07 发现 L15_timed.txt 就是这种，而本脚本只认格式 A，
        #   于是**每一次查询都静默返回 0:00** —— 拿它去填时间码会全填错。
        #   超过一小时的讲次时间码是 `1:18:27` 三段式，要一并兼容。
        if not idx:
            pend = None
            for ln in raw:
                s = ln.strip()
                m = re.match(r"^(?:(\d+):)?(\d+):(\d\d)$", s)
                if m:
                    hh = int(m.group(1) or 0)
                    pend = hh * 3600 + int(m.group(2)) * 60 + int(m.group(3))
                elif s and pend is not None:
                    idx.append((pend, s))       # 取该时间码后的第一行文本当锚点
                    pend = None
    lines = [l.rstrip("\n") for l in io.open(fp, encoding="utf-8")] if os.path.exists(fp) else []
    return idx, lines


def link(tag, sec):
    return "https://www.youtube.com/watch?v=%s&t=%ds" % (VID.get(tag, "?"), sec)


def hhmm(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


def anchors(idx, lines):
    """把索引条目单调地对齐到正文行号，返回 [(行号, 秒)]。

    ⚠ 早先写成「对每条索引从 pos 往后找第一处匹配、找到但行号超了就 break」是错的：
      pos 不前进会让后面的条目回头匹配到更早的行，时间码会乱窜（实测把 44:55 的内容
      报成了 70:55，差了半小时）。这里改成严格单调：匹配成功就把起点推到 i+1。

    ⚠⚠ 2026-10-14 又修一处：原来用 `lines[i].strip().startswith(frag[:26])`，
      而 timed 的片段**常常出现在正文某一行的中间**而非行首，于是大面积落空 ——
      全讲次锚点匹配率只有 20–43%。一旦中间断档，sec_of() 会把后面所有查询
      都退回到最后一个成功匹配的锚点：**实测 L16 把 50:17 的内容报成 38:10**。
      改成子串匹配 `frag[:26] in lines[i]` 后匹配率升到 90% 以上。
    """
    out, start = [], 0
    for s, frag in idx:
        frag = frag.strip()
        # ⚠ 太短的片段（L15 的 timed 里有一堆 "OK?" "OK." ）在子串匹配下
        #   几乎能命中任意一行，会把锚点钉在错误的早期行上，把后面的对齐全带偏。
        if len(frag) < 12:
            continue
        for i in range(start, len(lines)):
            if frag[:26] in lines[i]:
                out.append((i, s))
                start = i + 1
                break
    return out


def sec_of(anch, lineno):
    """行号 → 秒：取该行之前最后一个锚点。"""
    best = 0
    for i, s in anch:
        if i <= lineno:
            best = s
        else:
            break
    return best


def search(phrase, only=None):
    tags = [only] if only else sorted(
        (f[:-4] for f in os.listdir(TDIR) if f.endswith(".txt") and "_timed" not in f),
        key=lambda t: (t[0] != "L", int(t[1:]) if t[1:].isdigit() else 999))
    hits = 0
    for tag in tags:
        idx, lines = load(tag)
        if not lines:
            continue
        anch = anchors(idx, lines)
        for i, l in enumerate(lines):
            if phrase.lower() in l.lower():
                s = sec_of(anch, i)
                print("%-18s %-7s  %s" % (tag, hhmm(s), link(tag, s)))
                print("    %s" % l.strip()[:150])
                hits += 1
                if hits >= 12:
                    print("  …（命中过多，已截断）")
                    return
    if not hits:
        print("没找到：%s" % phrase)


def at(tag, sec):
    idx, lines = load(tag)
    near = [(abs(s - sec), s, t) for s, t in idx]
    near.sort()
    print("%s 第 %s（%ds）附近：%s\n" % (tag, hhmm(sec), sec, link(tag, sec)))
    for _, s, t in sorted(near[:5], key=lambda x: x[1]):
        print("  [%s] %s" % (hhmm(s), t[:120]))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--at":
        at(a[1], int(a[2]))
    else:
        search(a[0], a[1] if len(a) > 1 else None)
