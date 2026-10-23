# -*- coding: utf-8 -*-
"""把片子里每一条 says 的时间码，拿 retime.py 的插值估计重新核一遍。

⚠ 这个脚本必须以**文件**形式跑，不能塞进 python -c：
   正则里的 [^"\\] 经过 shell 一层会被折叠成 [^"\]，报 unterminated character set。

用法：python crosscheck.py L18 build_cs229_L18.py l18_disc.py ...
（源码文件名相对于 复习放映厅/源码/）
"""
import io, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"G:/Adelaide COMSC/2026S2/Machine Learning/复习放映厅/源码/"
CS229 = r"G:/Adelaide COMSC/2026S2/Machine Learning/CS229"
HERE = os.path.dirname(os.path.abspath(__file__))

SAYS = re.compile(r'says\("([0-9:]+)","((?:[^"\\]|\\.)*)"')


def sec(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def main():
    lec = sys.argv[1]
    qs = []
    for fn in sys.argv[2:]:
        s = io.open(SRC + fn, encoding="utf-8").read()
        for m in SAYS.finditer(s):
            qs.append((m.group(1), m.group(2), fn))
    print("片子里共 %d 条 says" % len(qs))
    if not qs:
        return 0

    r = subprocess.run([sys.executable, os.path.join(HERE, "retime.py"), lec]
                       + [q for _, q, _ in qs],
                       capture_output=True, text=True, encoding="utf-8", cwd=CS229)
    rows = [l for l in r.stdout.split("\n") if l.startswith("  ")]
    if len(rows) != len(qs):
        print("⚠ 返回 %d 行，和 %d 条对不上" % (len(rows), len(qs)))
        print(r.stdout[-900:], r.stderr[-400:])
        return 1

    bad = 0
    for (shown, q, fn), ln in zip(qs, rows):
        got = ln.strip().split()[0]
        if got == "?????":
            print("   ? 正文里找不到：«%s»  [%s]" % (q[:52], fn))
            bad += 1
            continue
        d = sec(shown) - sec(got)
        if abs(d) > 20:
            print("   ✗ 片子写 %-7s 估计 %-7s 差 %+ds  «%s»  [%s]"
                  % (shown, got, d, q[:44], fn))
            bad += 1
    print("不一致 %d 条 / 共 %d 条" % (bad, len(qs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
