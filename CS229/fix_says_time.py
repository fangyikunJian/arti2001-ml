# -*- coding: utf-8 -*-
"""把片子源码里**偏得太离谱**的 says() 时间码改成字幕里查到的真实位置。

为什么需要：时间码是给人点的 —— 写错 2–4 分钟，点 ▶ 过去听到的是别的内容。
2026-10-07 用 check_says.py 查出 L13 有 5 处偏 +120~+240 秒、L4 有 1 处偏 +260 秒。

判据与 check_says.py 一致，只是阈值更宽：
  · 时间索引**本身**大约 31 秒一条、最大 59 秒，`sec_of` 取的是「不晚于该行的锚点」，
    所以「实际」天然偏早，**90 秒以内不动**，免得把正常的粒度误差也改掉。
  · 改成锚点时间（宁可早一点点落在原话之前，也不要晚）。

用法：
    python fix_says_time.py ../复习放映厅/源码/l13_*.py --lec L13          # 空跑看清单
    python fix_says_time.py ../复习放映厅/源码/l13_*.py --lec L13 --write   # 真写
"""
import io, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import find_quote as fq
from check_says import SAYS, norm, to_sec

LIMIT = 90


def run(paths, lec, write):
    idx, lines = fq.load(lec)
    anch = fq.anchors(idx, lines)
    body = [norm(l) for l in lines]
    blob, owner = [], []
    for i, b in enumerate(body):
        if not b: continue
        if blob: blob.append(" "); owner.append(i)
        blob.append(b); owner.extend([i] * len(b))
    blob = "".join(blob)

    total = 0
    for path in paths:
        src = io.open(path, encoding="utf-8").read()
        out, last, n = [], 0, 0
        for m in SAYS.finditer(src):
            ts, en = m.group(1), m.group(2)
            frag = norm(en.split("...")[0])[:48]
            if len(frag) < 12:
                continue
            hits = [i for i, b in enumerate(body) if frag in b]
            if not hits:
                p, start = blob.find(frag), 0
                while p >= 0:
                    hits.append(owner[p]); start = p + 1; p = blob.find(frag, start)
            if not hits:
                continue
            want = to_sec(ts)
            real = fq.sec_of(anch, min(hits, key=lambda i: abs(fq.sec_of(anch, i) - want)))
            if abs(want - real) <= LIMIT:
                continue
            new = fq.hhmm(real)
            # 只替换这一处 says 的第一个参数，不碰别处同样的字符串
            a, b = m.span(1)
            out.append(src[last:a]); out.append(new); last = b
            n += 1; total += 1
            print("  %s  %-8s → %-8s (%+ds)  «%s»"
                  % (os.path.basename(path), ts, new, real - want, en[:44]))
        if n and write:
            out.append(src[last:])
            io.open(path, "w", encoding="utf-8").write("".join(out))
    print("  共 %d 处%s" % (total, "，已写入" if (total and write) else "（空跑，加 --write 才改）"))
    return total


if __name__ == "__main__":
    args = sys.argv[1:]
    write = "--write" in args
    if write: args.remove("--write")
    lec = "L13"
    if "--lec" in args:
        i = args.index("--lec"); lec = args[i + 1]; args = args[:i] + args[i + 2:]
    paths = []
    for a in args:
        paths += sorted(glob.glob(a)) or [a]
    paths = [p for p in paths if os.path.isfile(p)]
    print("%s：扫 %d 个源文件，阈值 %ds" % (lec, len(paths), LIMIT))
    run(paths, lec, write)
