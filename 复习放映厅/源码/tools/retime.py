# -*- coding: utf-8 -*-
"""用「字符位置线性插值」重算 CS229 片子的 says() 时间码。

⚠ 不要用 CS229/find_quote.py 来填时间码。它按**行号**找最近锚点，
   而多数讲次的 _timed.txt 只覆盖正文 11–15%，锚点稀疏时一个锚点要覆盖几十行，
   整段内容被压到同一个时间上。实测它把 19:03 的 sigmoid 报成 17:27（差 96 秒）。
   详见 memory/find-quote-anchor-bug.md。

本脚本的做法：
  ① 把每个 timed 块的文本在**正文**里定位，得到 (字符偏移, 秒) 锚点序列（严格单调往后找）
  ② 查一句话时定位它的字符偏移，**在左右两个锚点之间按字符数线性插值**
  ③ 报出左右锚点的间距 —— 间距越大越不可信，这就是误差上界

⚠ 覆盖率低 ≠ 锚点少：L16 正文只有 11.3% 带时间码，但锚点有 135 个、从 0:03 铺到 78:00。

用法：python retime.py L16 "quote one" "quote two" ...
（放在项目里而不是 scratchpad —— 2026-10-15 scratchpad 被清空过一次，工具全丢了。）
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = r"G:/Adelaide COMSC/2026S2/Machine Learning/CS229"
TDIR = os.path.join(HERE, "transcripts")

# Ng 讲课的口头语：片子引用时按惯例删掉，比对时两边都去掉
FILLER = re.compile(r"\b(uh|um|er|erm|ah|right|okay|ok|you know|i mean|sort of|kind of)\b")

# 片子里按书面语写全，讲稿里是口语缩写 —— 两边都展开成同一种写法
CONTR = [("you're", "you are"), ("we're", "we are"), ("they're", "they are"),
         ("it's", "it is"), ("that's", "that is"), ("there's", "there is"),
         ("what's", "what is"), ("here's", "here is"), ("i'm", "i am"),
         ("don't", "do not"), ("doesn't", "does not"), ("isn't", "is not"),
         ("can't", "can not"), ("won't", "will not"), ("let's", "let us"),
         ("you'll", "you will"), ("we'll", "we will"), ("you've", "you have")]


def norm(s):
    s = re.sub(r"\[[a-z]+\]", " ", s.lower())      # [NOISE] 之类
    for a, b in CONTR:
        s = s.replace(a, b)
    s = FILLER.sub(" ", s)
    s = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()
    # 讲稿里的口吃（"a-a state"、"these-these"）归一化后成了叠词，折叠掉
    prev = None
    while s != prev:
        prev = s
        s = re.sub(r"\b(\w+) \1\b", r"\1", s)
    return s


def to_sec(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def build(tag):
    """返回 (正文归一化串, [(字符偏移, 秒)] 锚点)。"""
    full = io.open(os.path.join(TDIR, tag + ".txt"), encoding="utf-8").read()
    nf = norm(full)

    raw = [l.rstrip("\n") for l in io.open(os.path.join(TDIR, tag + "_timed.txt"),
                                           encoding="utf-8")]
    TS = re.compile(r"^\[?((?:\d+:)?\d+:\d\d)\]?\s*(.*)$")
    blocks, pend, buf = [], None, []
    for ln in raw:
        m = TS.match(ln.strip())
        if m:
            if pend is not None:
                blocks.append((pend, " ".join(buf)))
            pend = to_sec(m.group(1)); buf = [m.group(2)] if m.group(2) else []
        elif pend is not None:
            buf.append(ln.strip())
    if pend is not None:
        blocks.append((pend, " ".join(buf)))

    anchors, start = [], 0
    for sec, txt in blocks:
        q = norm(txt)
        if len(q) < 14:
            continue
        off = nf.find(q[:40], start)        # 严格单调：只往后找
        if off < 0:
            off = nf.find(q[:22], start)
        if off < 0:
            continue
        anchors.append((off, sec))
        start = off + 1
    return nf, anchors


def at(nf, anchors, quote):
    """返回 (估计秒, 左右锚点跨度秒, 说明)。"""
    q = norm(quote)
    off = nf.find(q)
    if off < 0:
        off = nf.find(q[:max(14, int(len(q) * 0.6))])
    if off < 0:
        return None, None, "正文里找不到这句话"
    lo = hi = None
    for a_off, a_sec in anchors:
        if a_off <= off:
            lo = (a_off, a_sec)
        else:
            hi = (a_off, a_sec); break
    if lo and hi:
        f = (off - lo[0]) / float(hi[0] - lo[0])
        return lo[1] + f * (hi[1] - lo[1]), hi[1] - lo[1], "内插"
    if lo:
        return lo[1], None, "⚠ 在最后一个锚点之后，只能外推"
    if hi:
        return hi[1], None, "⚠ 在第一个锚点之前，只能外推"
    return None, None, "没有锚点"


def fmt(s):
    s = int(round(s)); return "%d:%02d" % (s // 60, s % 60)


if __name__ == "__main__":
    tag = sys.argv[1]
    nf, anchors = build(tag)
    print("%s：正文 %d 字符，定位到 %d 个锚点（%s – %s）"
          % (tag, len(nf), len(anchors),
             fmt(anchors[0][1]) if anchors else "?",
             fmt(anchors[-1][1]) if anchors else "?"))
    print()
    for q in sys.argv[2:]:
        sec, span, how = at(nf, anchors, q)
        if sec is None:
            print("  ?????    %-54s  %s" % (q[:54], how))
        else:
            flag = "" if (span is not None and span <= 90) else "  ⚠ 锚点间隔 %s" % (
                ("%ds" % span) if span is not None else "外推")
            print("  %-8s %-54s  %s%s" % (fmt(sec), q[:54], how, flag))
