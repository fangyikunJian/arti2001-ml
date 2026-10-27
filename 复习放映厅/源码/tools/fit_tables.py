# -*- coding: utf-8 -*-
"""按实测的文字框模型，自动把每张 matrix 的行高收到不会压住下方 note 为止。

实测模型（1440×860）：
  · matrix 单元文字：中心 = y + (rows-1)*ch + (ch-3)/2，文字框 ≈ 中心 ±11
  · note 文字框 = [ny-14, ny+4]
  · 要留 ≥10px 空隙 ⇒ 中心 ≤ ny - 35
  · 另外 matrix 底边 = y+(rows-1)*ch+(ch-3) ≤ 390

用法：python fit_tables.py <模块.py> [<模块.py> ...]
"""
import io, re, sys, ast

sys.stdout.reconfigure(encoding="utf-8")

MAT = re.compile(r'matrix\(\{rows:(\d+),cols:(\d+),cw:(\d+),ch:(\d+),x:(-?\d+),y:(\d+)')
NOTE = re.compile(r'note\(\s*"[^"]*"\s*,\s*-?\d+\s*,\s*(\d+)\s*,')
EQTOP = re.compile(r'setEq\(".*?",\s*"top"\s*\)')


def center(rows, ch, y):
    return y + (rows - 1) * ch + (ch - 3) / 2.0


def bottom(rows, ch, y):
    return y + (rows - 1) * ch + (ch - 3)


def fit(path):
    s = io.open(path, encoding="utf-8").read()
    out, last, changed = [], 0, 0
    # 按镜切开，这样才知道同一镜里 matrix 下方有哪些 note
    for shot in re.finditer(r"clearScene\(\);(.*?)(?=clearScene\(\);|\Z)", s, re.S):
        blk = shot.group(1)
        m = MAT.search(blk)
        if not m:
            continue
        rows, cols, cw, ch, x, y = [int(v) for v in m.groups()]
        y_floor = 196 if EQTOP.search(blk) else 150
        # ⚠ 同一镜里 cite 占着 [y-14, y+4]，表不能提到它头上
        cites = [int(v) for v in re.findall(r'cite\(\s*"[^"]*"\s*,\s*(\d+)\)', blk)]
        if cites:
            y_floor = max(y_floor, max(cites) + 36)
        below = [int(v) for v in NOTE.findall(blk) if int(v) > y]
        limit_c = (min(below) - 35) if below else 9e9
        ny, nch = y, ch
        while nch >= 26:
            if center(rows, nch, ny) <= limit_c and bottom(rows, nch, ny) <= 390:
                break
            nch -= 2
            if nch < 30 and ny > y_floor:          # 行高压得太狠就先把表往上提
                ny = y_floor
        if (ny, nch) == (y, ch):
            continue
        new = "matrix({rows:%d,cols:%d,cw:%d,ch:%d,x:%d,y:%d" % (rows, cols, cw, nch, x, ny)
        a, b = shot.start(1) + m.start(), shot.start(1) + m.end()
        out.append(s[last:a]); out.append(new); last = b
        changed += 1
        print("  rows=%d  ch %d→%d  y %d→%d   中心 %.1f→%.1f（上限 %s）  底边 %d→%d"
              % (rows, ch, nch, y, ny, center(rows, ch, y), center(rows, nch, ny),
                 "—" if limit_c > 1e8 else int(limit_c),
                 bottom(rows, ch, y), bottom(rows, nch, ny)))
    if changed:
        out.append(s[last:])
        s2 = "".join(out)
        ast.parse(s2)
        io.open(path, "w", encoding="utf-8").write(s2)
    print("%s：调整 %d 张表" % (path, changed))


for p in sys.argv[1:]:
    fit(p)
