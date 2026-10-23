# -*- coding: utf-8 -*-
"""全部片子的 says 时间码偏差总览，按量级分档。

⚠ 为什么不能只看「偏差 > 20s」：
   L15 的 _timed.txt 是密集的（99.9%），用 verify_says.py 直接法验过 **27 条全对**；
   而插值法对它仍报出 3 条 22–36s 的差。
   ⇒ 20–40s 这个量级是**两种方法的固有差**（直接法报语块开头，插值法报句内位置），
     不是时间码错了。真正要修的是**上百秒**那种。

⚠ 必须以文件形式跑：正则里的 [^"\\] 经 shell 一层会被折叠成 [^"\]。

用法：python tools/drift_report.py        （在 复习放映厅/源码 下跑）
"""
import io, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CS229 = r"G:/Adelaide COMSC/2026S2/Machine Learning/CS229"
HERE = os.path.dirname(os.path.abspath(__file__))

SAYS = re.compile(r'says\("([0-9:]+)","((?:[^"\\]|\\.)*)"')
LECS = ["L4", "L5", "L9", "L10", "L11", "L12", "L13", "L14", "L15",
        "L16", "L17", "L18", "L19", "L20", "DS_LearningTheory"]


def sec(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def files_for(lec):
    pref = "ds_" if lec.startswith("DS") else lec.lower() + "_"
    build = "build_cs229_%s.py" % ("DS" if lec.startswith("DS") else lec)
    out = []
    for f in sorted(os.listdir(SRC)):
        if f.endswith(".py") and (f == build or f.startswith(pref)):
            out.append(f)
    return out


def main():
    print("%-6s %5s %6s %7s %8s %9s" % ("讲次", "says", "找不到", ">60s", ">120s", "最大偏差"))
    bad = []
    for lec in LECS:
        fs = files_for(lec)
        if not fs:
            continue
        qs = []
        for fn in fs:
            s = io.open(os.path.join(SRC, fn), encoding="utf-8").read()
            qs += [(m.group(1), m.group(2)) for m in SAYS.finditer(s)]
        if not qs:
            continue
        r = subprocess.run([sys.executable, os.path.join(HERE, "retime.py"), lec]
                           + [q for _, q in qs],
                           capture_output=True, text=True, encoding="utf-8", cwd=CS229)
        rows = [l for l in r.stdout.split("\n") if l.startswith("  ")]
        if len(rows) != len(qs):
            print("%-6s  ⚠ 返回 %d 行 / %d 条，跳过" % (lec, len(rows), len(qs)))
            continue
        diffs, nf, worst = [], 0, None
        for (shown, q), ln in zip(qs, rows):
            g = ln.strip().split()[0]
            if g == "?????":
                nf += 1
                continue
            d = sec(shown) - sec(g)
            diffs.append(abs(d))
            if worst is None or abs(d) > abs(worst[0]):
                worst = (d, shown, g, q)
        g60 = sum(1 for x in diffs if x > 60)
        g120 = sum(1 for x in diffs if x > 120)
        mx = max(diffs) if diffs else 0
        flag = " ⚠⚠" if g120 else ("  ·" if g60 else "   ✓")
        name = "DS" if lec.startswith("DS") else lec
        print("%-6s %5d %6d %7d %8d %7ds%s" % (name, len(qs), nf, g60, g120, mx, flag))
        if g120:
            bad.append((name, g120, worst))

    if bad:
        print("\n⚠ 需要修的（偏差 >120s）：")
        for name, n, w in bad:
            print("   %-5s %d 条，最严重：片子写 %s 估计 %s 差 %+ds  «%s»"
                  % (name, n, w[1], w[2], w[0], w[3][:44]))
    else:
        print("\n✓ 没有偏差超过 120s 的")


if __name__ == "__main__":
    main()
