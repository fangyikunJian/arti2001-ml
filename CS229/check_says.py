# -*- coding: utf-8 -*-
"""复核一部片子里所有 says(时间码, 英文原话) 是否对得上字幕。

⚠ 2026-10-07 起必跑：L15 的 `_timed.txt` 是 YouTube 原始格式，而 find_quote.py
   当时只认自家的 `[mm:ss]` 格式，**每次查询都静默返回 0:00** ——
   拿它填出来的时间码会全错。所以时间码不能只靠「当时查过」，要能随时复核。

判据：
  · 原话在字幕正文里**找得到**（忽略大小写与多余空白）
  · 片子写的时间码与字幕里该句所属时间码**相差 ≤ 45 秒**（切分点不同，允许少量偏移）

用法：python check_says.py ../复习放映厅/源码/l15_*.py ../复习放映厅/源码/build_cs229_L15.py --lec L15
"""
import io, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import find_quote as fq

SAYS = re.compile(r'says\(\s*"([^"]+)"\s*,\s*"((?:[^"\\]|\\.)*)"')
TOL = 45


# Ng 的口头语。片子里引用时都删掉了（读起来才通顺），比对时两边都要去掉，
# 否则会把「真引用」误报成「找不到」—— 2026-10-07 实测 7 条告警全是这么来的。
FILLER = re.compile(r"\b(uh|um|er|erm|ah|sort of|kind of|you know|i mean|like|so|and so|right|okay|ok)\b")


def norm(s):
    s = s.replace("\\\"", '"').replace("\\\\", "\\")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    s = FILLER.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def to_sec(ts):
    p = [int(x) for x in ts.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def check(paths, lec):
    idx, lines = fq.load(lec)
    anch = fq.anchors(idx, lines)
    if not idx:
        print("✗ %s 没有可用的时间索引" % lec); return 1
    body = [norm(l) for l in lines]
    # ⚠ 原话常常**跨两行**（字幕按行切，说话不按行停），只在单行里找会虚报「找不到」。
    #   2026-10-07 实测 4 条告警里 3 条就是这么来的。所以再准备一份「整篇拼起来」的串，
    #   并记下每个字符属于哪一行，好把命中位置换算回行号去取时间码。
    blob, owner = [], []
    for i, b in enumerate(body):
        if not b: continue
        if blob: blob.append(" "); owner.append(i)
        blob.append(b); owner.extend([i] * len(b))
    blob = "".join(blob)

    # 词级索引，给下面的模糊匹配用
    words, wowner, pos = [], [], 0
    for w in blob.split(" "):
        if w:
            words.append(w); wowner.append(owner[min(pos, len(owner) - 1)])
        pos += len(w) + 1

    def fuzzy(en, words, wowner, need=0.70):
        """原话的词能否在正文里按顺序找到 ≥need 的比例。返回命中处的行号列表。"""
        q = [w for w in norm(en).split(" ") if w]
        if len(q) < 5:
            return []
        out, span = [], int(len(q) * 2.2) + 6
        for s in range(0, max(1, len(words) - 3)):
            qi, matched = 0, 0
            for k in range(s, min(s + span, len(words))):
                if qi < len(q) and words[k] == q[qi]:
                    qi += 1; matched += 1
            if matched / len(q) >= need:
                out.append(wowner[s])
                if len(out) > 40:
                    break
        return out
    ok = miss = off = 0
    for path in paths:
        src = io.open(path, encoding="utf-8").read()
        for m in SAYS.finditer(src):
            ts, en = m.group(1), m.group(2)
            frag = norm(en.split("...")[0])[:48]      # 原话里常有省略号，取前半段去找
            if len(frag) < 12:
                continue
            hits = [i for i, b in enumerate(body) if frag in b]
            if not hits:                                   # 退一步：在拼起来的整篇里找（跨行的情形）
                start, p = 0, blob.find(frag)
                while p >= 0:
                    hits.append(owner[p]); start = p + 1; p = blob.find(frag, start)
            if not hits:
                # ⚠ 再退一步：**模糊**匹配。片子引用时除了删口头语，还会
                #   去掉 Ng 的口误重复（“what the curve- what the learning curve”）
                #   和修正字幕的听写错误（字幕 “a publishing paper” → 片子 “publishing a paper”）。
                #   精确子串对这些一律判「找不到」，2026-10-08 实测 L12 四条告警全是这么来的。
                #   判据改成：原话的词能在正文里**按顺序**找到 ≥70%。
                hits = fuzzy(en, words, wowner)
            if not hits:
                print("  ✗ 字幕里找不到　%-9s «%s»" % (ts, en[:58])); miss += 1; continue
            # ⚠ 同一句话 Ng 常常说不止一次（「concave form of Jensen」在 L13 里隔 9 分钟说了两遍）。
            #   只认第一次会把「引用了第二次」误判成错，所以取**离所写时间码最近**的那次。
            want = to_sec(ts)
            lineno = min(hits, key=lambda i: abs(fq.sec_of(anch, i) - want))
            real = fq.sec_of(anch, lineno)
            if len(hits) > 1:
                pass   # 多次出现时已取最近的一次
            d = to_sec(ts) - real
            if abs(d) > TOL:
                print("  ⚠ 时间码偏 %+4ds　片子写 %-8s 实际 %-8s «%s»"
                      % (d, ts, fq.hhmm(real), en[:46])); off += 1
            else:
                ok += 1
    print("  —— 对得上 %d　找不到原话 %d　偏差 >%ds %d" % (ok, miss, TOL, off))
    return miss + off


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    lec = "L15"
    if "--lec" in args:
        i = args.index("--lec"); lec = args[i + 1]; args = args[:i] + args[i + 2:]
    paths = []
    for a in args:
        paths += sorted(glob.glob(a)) or [a]
    paths = [p for p in paths if os.path.isfile(p)]
    print("复核 %s：%d 个源文件" % (lec, len(paths)))
    sys.exit(0 if check(paths, lec) == 0 else 1)
