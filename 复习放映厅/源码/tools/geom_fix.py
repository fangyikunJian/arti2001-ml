# -*- coding: utf-8 -*-
"""geom_fix.py —— 把 geom_stack 查出来的「note 压在 stack/seq/gpus/tiles 末格底边上」
就地改好：把第一条越界的 note 下移到「底边 + 16」（文字框顶比底边低 2），
后面的 note 若因此挤到 19 以内，再依次往下推；一旦有人会超过 386 就整镜不动并报出来。

⚠ 只改 note() 的 y，不动任何文字、不动 stack 的参数。
用法：python tools/geom_fix.py cme295_L3_*.py        （在 源码/ 下跑）
"""
import io, re, sys, glob

sys.path.insert(0, "tools")
import geom_stack as G

sys.stdout.reconfigure(encoding="utf-8")

CLEAR = 16          # 底边 + 16 ⇒ 文字框顶（y−14）比底边低 2
GAP = G.NOTE_GAP
MAXY = G.NOTE_MAX


def note_y_spans(shot):
    """返回这一镜里每个 note 的 (y 参数在 shot 内的起止位置, 当前 y)。"""
    out = []
    for m in re.finditer(r"\bnote\s*\(", shot):
        inner, end = G.body_of(shot, m.end() - 1)
        args = G.split_args(inner)
        if len(args) < 3 or not G.nums(args[2]):
            continue
        # 第三个参数在 inner 里的偏移
        off = m.end() - 1 + 1 + sum(len(a) + 1 for a in args[:2])
        a2 = args[2]
        lead = len(a2) - len(a2.lstrip())
        tok = a2.strip()
        out.append((off + lead, off + lead + len(tok), float(tok)))
    return out


def fix_file(path, dry=False):
    src = io.open(path, encoding="utf-8").read()
    edits = []        # (abs_start, abs_end, new_text)
    skipped = []
    for sm in re.finditer(r"\(r'''(.*?)''',", src, re.S):
        shot = sm.group(1)
        base = sm.start(1)
        items = G.scan_shot(shot)
        spans = note_y_spans(shot)
        # 把 note 的 pos 和 spans 对上（顺序一致）
        notes = [it for it in items if it["k"] == "note"]
        if len(notes) != len(spans):
            continue
        newy = [s[2] for s in spans]
        # 找第一条压在 helper 上的 note
        helper = None
        hit = None
        ni = 0
        for it in items:
            if it["k"] == "note":
                if helper is not None:
                    if it["y"] - G.TXT_UP < helper["bottom"]:
                        hit = (ni, helper["bottom"])
                        break
                    helper = None
                ni += 1
            elif it["k"] in ("stack", "seq", "gpus", "tiles", "matrix", "box"):
                helper = it
        if hit is None:
            continue
        i0, bottom = hit
        newy[i0] = bottom + CLEAR
        for k in range(i0 + 1, len(newy)):
            if newy[k] - newy[k - 1] < GAP:
                newy[k] = newy[k - 1] + GAP
        if max(newy) > MAXY:
            line = src[:sm.start()].count("\n") + 1
            skipped.append("L%d 推不下去（最低会到 %g ＞ %d），要手工调"
                           % (line, max(newy), MAXY))
            continue
        for (s, e, old), nv in zip(spans, newy):
            if nv != old:
                txt = ("%g" % nv)
                edits.append((base + s, base + e, txt))
    if not edits:
        return 0, skipped
    for s, e, t in sorted(edits, reverse=True):
        src = src[:s] + t + src[e:]
    if not dry:
        io.open(path, "w", encoding="utf-8").write(src)
    return len(edits), skipped


def main(argv):
    pats = argv[1:] or ["cme295_L4_*.py"]
    files = []
    for p in pats:
        files += sorted(glob.glob(p))
    tot = 0
    for f in files:
        n, sk = fix_file(f)
        tot += n
        if n or sk:
            print("%-22s 改了 %2d 处" % (f, n) + ("  ⚠ " + "；".join(sk) if sk else ""))
    print("geom_fix：%d 个文件，共改 %d 处 note 的 y" % (len(files), tot))


if __name__ == "__main__":
    main(sys.argv)
