# -*- coding: utf-8 -*-
"""geom_stack.py —— 补上 audit_film.py 看不见的那一块（坑 13）。

audit_film 只能看见 note()/boxNode() 的字面坐标；stack()/seq()/gpus()/tiles() 的
几何是在 JS 里算出来的，静态扫不到，一直靠手算 —— 而手算一错，末格就会被下面的
note 压住。这个脚本把那几个 helper 的几何照 build 脚本里的定义复算一遍，然后检查：

  ① says(…,y) 之下的首条 note：Δy ≥ 19（note 文字框高 18）
  ② note 的 y ≤ 386；boxNode / helper 的底边 ≤ 390
  ③ 同一镜里，排在某个 helper 之后的 note 的文字框顶（y−14）≥ 那个 helper 的底边
  ④ 同一镜里相邻两条 note：x 区间可能重叠时 Δy ≥ 19（和 audit ⑮ 同一条线）

用法：python tools/geom_stack.py cme295_L4_*.py     （在 源码/ 下跑）
"""
import io, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")

NOTE_GAP = 19
NOTE_MAX = 386
BOX_MAX = 390
TXT_UP = 14          # note 文字框 = [y-14, y+4]
CJK_W = 13.0         # 一个汉字约 13px；用来估 note 的横向宽度

# helper 的默认值，照 build_cme295_L4.py 里的定义
DEF = {
    "stack": dict(bw=250, bh=32, gap=6),
    "seq":   dict(bw=104, bh=44, gap=10),
    "gpus":  dict(bw=250, bh=44, gap=16),
}


def nums(s):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


def split_args(s):
    """按顶层逗号切参数（跳过括号、方括号、花括号和字符串里的逗号）。"""
    out, depth, q, cur = [], 0, None, ""
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            cur += c
            if c == "\\":
                cur += s[i + 1] if i + 1 < len(s) else ""
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
            cur += c
        elif c in "([{":
            depth += 1
            cur += c
        elif c in ")]}":
            depth -= 1
            cur += c
        elif c == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return out


def body_of(src, start):
    """从 '(' 处取到配对的 ')'，返回里面的内容和右括号位置。"""
    depth, q, i = 0, None, start
    while i < len(src):
        c = src[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return src[start + 1:i], i
        i += 1
    return "", len(src)


def width_of(text):
    """估一条 note 的横向半宽（只数汉字和全角标点，拉丁字母算半个）。"""
    w = 0.0
    for ch in text:
        w += CJK_W if ord(ch) > 0x2000 else CJK_W * 0.55
    return w / 2


def scan_shot(src):
    """返回这一镜里按出现顺序排列的元素列表。"""
    items = []
    for m in re.finditer(r"\b(says|note|boxNode|stack|seq|gpus|tiles|matrix)\s*\(", src):
        name = m.group(1)
        inner, end = body_of(src, m.end() - 1)
        args = split_args(inner)
        pos = m.start()
        if name == "says":
            y = nums(args[2])[0] if len(args) > 2 and nums(args[2]) else 150.0
            items.append(dict(k="says", y=y, pos=pos))
        elif name == "note":
            if len(args) < 3:
                continue
            ny = nums(args[2])
            nx = nums(args[1])
            if not ny or not nx:
                continue
            txt = args[0].strip()[1:-1]
            items.append(dict(k="note", y=ny[0], x=nx[0], hw=width_of(txt), pos=pos))
        elif name == "boxNode":
            v = [nums(a)[0] if nums(a) else 0 for a in args[:4]]
            if len(v) == 4:
                items.append(dict(k="box", bottom=v[1] + v[3], pos=pos))
        elif name in ("stack", "seq", "gpus"):
            d = DEF[name]
            if name == "stack":
                ytop = nums(args[1])[0]
                n = len(split_args(args[2].strip()[1:-1]))
                rest = [nums(a)[0] for a in args[3:6] if nums(a)]
                bw = rest[0] if len(rest) > 0 else d["bw"]
                bh = rest[1] if len(rest) > 1 else d["bh"]
                gap = rest[2] if len(rest) > 2 else d["gap"]
                bottom = ytop + (n - 1) * (bh + gap) + bh
                items.append(dict(k=name, bottom=bottom, pos=pos))
            elif name == "seq":
                y = nums(args[1])[0]
                rest = [nums(a)[0] for a in args[4:6] if nums(a)]
                bh = rest[1] if len(rest) > 1 else d["bh"]
                items.append(dict(k=name, bottom=y + bh, pos=pos))
            else:  # gpus(x0,y,n,hold,cls,bw,bh) —— 带 hold 时下方还有一行 note
                y = nums(args[1])[0]
                rest = [nums(a)[0] for a in args[5:7] if nums(a)]
                bh = rest[1] if len(rest) > 1 else d["bh"]
                has_hold = args[3].strip() not in ("null", "")
                bottom = y + bh + (26 + 4 if has_hold else 0)
                items.append(dict(k=name, bottom=bottom, pos=pos))
        elif name == "tiles":
            v = [nums(a)[0] if nums(a) else 0 for a in args[:6]]
            if len(v) == 6:
                y, rows, ch = v[1], v[3], v[5]
                items.append(dict(k="tiles", bottom=y + (rows - 1) * ch + ch - 4, pos=pos))
        elif name == "matrix":
            o = inner
            y = nums(re.search(r"\by\s*:\s*(-?\d+)", o).group(1))[0] if re.search(r"\by\s*:\s*(-?\d+)", o) else None
            r = re.search(r"\brows\s*:\s*(\d+)", o)
            c = re.search(r"\bch\s*:\s*(\d+)", o)
            if y is not None and r:
                ch = float(c.group(1)) if c else 42.0
                items.append(dict(k="matrix", bottom=y + (float(r.group(1)) - 1) * ch + ch - 3, pos=pos))
    items.sort(key=lambda d: d["pos"])
    return items


def check(path):
    src = io.open(path, encoding="utf-8").read()
    bad = []
    # 每一镜是 (r'''…''', "…", 秒) 里的第一段
    for sm in re.finditer(r"\(r'''(.*?)''',", src, re.S):
        shot = sm.group(1)
        line0 = src[:sm.start()].count("\n") + 1
        items = scan_shot(shot)
        last_helper = None
        prev_note = None
        said = None
        for it in items:
            if it["k"] == "says":
                if not (140 <= it["y"] <= 220):
                    bad.append("L%d ⑤ says 的 y=%g 不在 [140,220] 里（多半是手滑）"
                               % (line0, it["y"]))
                said = it
                prev_note = None
                continue
            if it["k"] == "note":
                if said is not None:
                    d = it["y"] - said["y"]
                    if 0 <= d < NOTE_GAP:
                        bad.append("L%d ① says y=%g 之下首条 note y=%g，只差 %g（要 ≥ %d）"
                                   % (line0, said["y"], it["y"], d, NOTE_GAP))
                    said = None
                if it["y"] > NOTE_MAX:
                    bad.append("L%d ② note y=%g 超过 %d" % (line0, it["y"], NOTE_MAX))
                if last_helper is not None:
                    top = it["y"] - TXT_UP
                    if top < last_helper["bottom"]:
                        bad.append("L%d ③ note y=%g（文字框顶 %g）压在 %s 的底边 %g 上"
                                   % (line0, it["y"], top, last_helper["k"], last_helper["bottom"]))
                        last_helper = None
                    else:
                        last_helper = None
                if prev_note is not None:
                    dy = abs(it["y"] - prev_note["y"])
                    if dy < NOTE_GAP:
                        xo = abs(it["x"] - prev_note["x"]) < (it["hw"] + prev_note["hw"])
                        if xo:
                            bad.append("L%d ④ 两条 note 的 y 只差 %g 且横向重叠（x=%g / %g）"
                                       % (line0, dy, prev_note["x"], it["x"]))
                prev_note = it
                continue
            # helper / boxNode
            if it["bottom"] > BOX_MAX:
                bad.append("L%d ② %s 底边 %g 超过 %d" % (line0, it["k"], it["bottom"], BOX_MAX))
            last_helper = it
            said = None
    return bad


def main(argv):
    pats = argv[1:] or ["cme295_L4_*.py"]
    files = []
    for p in pats:
        files += sorted(glob.glob(p))
    total = 0
    for f in files:
        b = check(f)
        total += len(b)
        if b:
            print("── %s ──" % f)
            for x in b:
                print("   " + x)
    print("geom_stack：%d 个文件，%d 处问题" % (len(files), total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
