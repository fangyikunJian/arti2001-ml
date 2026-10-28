# -*- coding: utf-8 -*-
"""给 says() 找**精确**时间码：直接在原始 VTT 的 cue 流里定位，不做插值。

为什么要有这个工具（见 memory/find-quote-anchor-bug.md）：
  · CS229/find_quote.py 按**行号**找最近锚点 —— 锚点稀疏时整段被压到同一时间，
    实测把 19:03 报成 17:27（差 96 秒）。
  · tools/retime.py 改成**字符位置插值**，准确多了，但仍是估计：它只拿
    `_timed.txt` 里每 ≥30 秒一条的锚点当基准，误差上界 = 左右锚点的间距。

本脚本不插值：**原始 `_vtt/*.vtt` 里每 3–4 秒就有一条 cue**，
把全部 cue 拼成一条归一化字符流、记下每个字符属于哪条 cue，
查一句话就能落到**具体某一条 cue** 上，报它的真实起始秒。

  用法：
    python quote_ts.py CME295 L1 "a quote" "another quote" ...
    python quote_ts.py --check CME295 L1 build_cme295_L1.py cme295_L1_a.py ...
    python quote_ts.py --selftest CME295 L1

  --check   把这些源码文件里每一条 says("mm:ss","en") 的时间码重新核一遍，
            只报对不上的（容差默认 6 秒，cue 边界 + 口头语删减带来的抖动）。
  --selftest 阳性对照：拿 `_timed.txt` 里**已知时间码**的句子当题目反查，
            看本工具报出的秒数是否对得上；再人为改一个字看它是否报「找不到」。
            ⚠ 每次改动归一化规则之后都要跑这个 —— 不然「全绿」只说明我没报错。
"""
import argparse, glob, html, io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:/Adelaide COMSC/2026S2/Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码")

TS = re.compile(r"(\d+):(\d\d):(\d\d)\.(\d+)\s+-->")
TAG = re.compile(r"<[^>]*>")
SAYS = re.compile(r'says\(\s*"([0-9:]+)"\s*,\s*"((?:[^"\\]|\\.)*)"')

# 片子里按书面语写，讲稿里是口语 —— 两边都展开成同一种写法。与 retime.py 保持一致。
CONTR = [("you're", "you are"), ("we're", "we are"), ("they're", "they are"),
         ("it's", "it is"), ("that's", "that is"), ("there's", "there is"),
         ("what's", "what is"), ("here's", "here is"), ("i'm", "i am"),
         ("don't", "do not"), ("doesn't", "does not"), ("isn't", "is not"),
         ("can't", "can not"), ("won't", "will not"), ("let's", "let us"),
         ("you'll", "you will"), ("we'll", "we will"), ("you've", "you have"),
         ("we've", "we have"), ("didn't", "did not"), ("aren't", "are not")]
# 讲课口头语：引用时按惯例删掉，比对时两边都去掉
FILLER = re.compile(r"\b(uh|um|er|erm|ah|like|right|okay|ok|i guess|you know|"
                    r"i mean|sort of|kind of|basically|actually|so)\b")


def norm(s):
    """归一化到只剩 [a-z0-9 ]。删口头语是为了让「片子里引的书面版」能对上口语原文。"""
    s = re.sub(r"\[[a-z ]+\]", " ", s.lower())          # [LAUGHTER] 之类
    for a, b in CONTR:
        s = s.replace(a, b)
    s = FILLER.sub(" ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def cues(course, key):
    """返回 [(起始秒, 原文), ...]。只认人工字幕，没有才退自动稿 —— 与 fetch_transcripts 一致。"""
    tdir = os.path.join(ROOT, course, "transcripts")
    vid = None
    head = io.open(os.path.join(tdir, key + ".txt"), encoding="utf-8").read(400)
    m = re.search(r"v=([\w-]+)", head)
    if m:
        vid = m.group(1)
    if not vid:
        raise SystemExit("%s/%s.txt 头部没有视频链接，取不到视频 ID" % (course, key))
    pats = [vid + ".en.vtt", vid + ".en-US.vtt", vid + ".en-GB.vtt",
            vid + ".en-*.vtt", vid + ".en-orig.vtt"]
    path = None
    for p in pats:
        hit = sorted(glob.glob(os.path.join(tdir, "_vtt", p)))
        if hit:
            path = hit[0]
            break
    if not path:
        raise SystemExit("找不到 %s 的 vtt（%s/transcripts/_vtt/）" % (key, course))

    out, prev = [], None
    blocks = re.split(r"\n\s*\n", io.open(path, encoding="utf-8").read().replace("\r\n", "\n"))
    for b in blocks:
        lines = b.strip("\n").split("\n")
        for i, ln in enumerate(lines):
            m = TS.search(ln)
            if not m:
                continue
            h, mi, s, ms = m.groups()
            t = int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 10 ** len(ms)
            txt = " ".join(TAG.sub("", x).strip() for x in lines[i + 1:])
            txt = re.sub(r"\s+", " ", html.unescape(txt)).strip()
            if txt and txt != prev:          # 人工字幕偶尔把同一句连放两条
                out.append((t, txt))
                prev = txt
            break
    return out, os.path.basename(path)


def build(course, key):
    """拼成一条归一化字符流，并记下每个字符来自哪条 cue。"""
    cs, src = cues(course, key)
    stream, owner = [], []
    for idx, (t, txt) in enumerate(cs):
        n = norm(txt)
        if not n:
            continue
        if stream:
            stream.append(" ")
            owner.append(idx)
        stream.append(n)
        owner.extend([idx] * len(n))
    return "".join(stream), owner, cs, src


def mmss(t):
    """分钟不进位到小时 —— 与 _timed.txt 以及片子里 says() 的写法一致。"""
    t = int(t)
    return "%02d:%02d" % (t // 60, t % 60)


def locate(stream, owner, cs, quote):
    """返回 [(秒, mm:ss, cue 序号), ...]，全部命中位置。精确，不插值。"""
    q = norm(quote)
    if not q:
        return []
    hits, i = [], stream.find(q)
    while i >= 0:
        idx = owner[i]
        hits.append((cs[idx][0], mmss(cs[idx][0]), idx))
        i = stream.find(q, i + 1)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--tol", type=int, default=6, help="--check 的容差秒数")
    ap.add_argument("course")
    ap.add_argument("key")
    ap.add_argument("rest", nargs="*")
    a = ap.parse_args()

    stream, owner, cs, src = build(a.course, a.key)
    print("%s %s：%d 条 cue，归一化后 %d 字符（%s）"
          % (a.course, a.key, len(cs), len(stream), src))

    if a.selftest:
        # 阳性对照①：_timed.txt 里的句子带着真时间码，反查应当对上。
        tp = os.path.join(ROOT, a.course, "transcripts", a.key + "_timed.txt")
        rows = [l for l in io.open(tp, encoding="utf-8").read().splitlines()
                if l.startswith("[")]
        ok = miss = bad = 0
        worst = (0, "")
        for l in rows:
            m = re.match(r"\[(\d+):(\d\d)\] (.+)", l)
            if not m:
                continue
            want = int(m.group(1)) * 60 + int(m.group(2))
            hits = locate(stream, owner, cs, m.group(3))
            if not hits:
                miss += 1
                continue
            d = min(abs(h[0] - want) for h in hits)
            if d <= 3:
                ok += 1
            else:
                bad += 1
                if d > worst[0]:
                    worst = (d, m.group(3)[:60])
        print("  对照① %d 条带已知时间码的句子：%d 条命中且 ≤3 秒 · %d 条偏差大 · %d 条定位不到"
              % (len(rows), ok, bad, miss))
        if worst[0]:
            print("     最差偏差 %.0f 秒：%s…" % worst)
        # 阳性对照②：故意改一个词，必须查不到 —— 否则说明匹配太松，"全绿"不可信。
        probe = re.match(r"\[\d+:\d\d\] (.+)", rows[len(rows) // 2]).group(1)
        fake = probe + " zzqq nonexistent phrase"
        print("  对照② 人为污染后的句子：%s"
              % ("✓ 正确地找不到" if not locate(stream, owner, cs, fake) else "✗ 居然还能命中（匹配太松）"))
        return

    if a.check:
        tot = wrongs = unknown = 0
        for f in a.rest:
            p = f if os.path.isabs(f) else os.path.join(SRC, f)
            body = io.open(p, encoding="utf-8").read()
            for m in SAYS.finditer(body):
                tot += 1
                mm, ss = m.group(1).split(":")[-2:]
                want = int(mm) * 60 + int(ss)
                quote = m.group(2).replace('\\"', '"')
                hits = locate(stream, owner, cs, quote)
                if not hits:
                    unknown += 1
                    print("  ？ %s  %-8s 定位不到：%s…" % (os.path.basename(f), m.group(1), quote[:58]))
                    continue
                d = min(abs(h[0] - want) for h in hits)
                if d > a.tol:
                    wrongs += 1
                    print("  ✗ %s  写的 %s，实际 %s（差 %.0f 秒）：%s…"
                          % (os.path.basename(f), m.group(1),
                             min(hits, key=lambda h: abs(h[0] - want))[1], d, quote[:52]))
        print("  共 %d 条 says：%d 条时间码对不上，%d 条定位不到" % (tot, wrongs, unknown))
        sys.exit(1 if (wrongs or unknown) else 0)

    for q in a.rest:
        hits = locate(stream, owner, cs, q)
        if not hits:
            print("  ？ 定位不到：%s" % q[:70])
        else:
            tag = "" if len(hits) == 1 else "  ⚠ %d 处命中" % len(hits)
            print('  %s  says("%s","%s");%s' % (hits[0][1], hits[0][1], q, tag))


if __name__ == "__main__":
    main()
