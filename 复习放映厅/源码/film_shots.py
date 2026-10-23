# -*- coding: utf-8 -*-
"""列出一部片子**每个知识点各有几镜**，用来找「该拆而没拆」的地方。

`audit_film.py` 只告诉你「总镜数不够」，这个告诉你**不够在哪一节**。
质量线的补法是「**把每个 KP 拆成更多步**，不是把讲解写更长」（见 memory/projector-quality-bar.md），
所以先看哪些 KP 只有 1–2 镜。

用法：python film_shots.py ../影片/CS229讲座L15-*.html
"""
import io, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from audit_film import shots, plain   # 复用同一套解析，省得两份实现走偏

KPRE = re.compile(r'\bKP\(\s*"((?:[^"\\]|\\.)*)"')
SRE = re.compile(r"\bS\((\d+)\s*,\s*(?:\d+\s*,\s*)?function\(\)\s*\{")


def report(path, need=45):
    h = io.open(path, encoding="utf-8", errors="replace").read()
    sh = shots(h)
    kp = [(m.start(), m.group(1)) for m in KPRE.finditer(h)]
    spos = [m.start() for m in SRE.finditer(h)]
    if not kp:
        print("—  %s：不是现行引擎的片子" % os.path.basename(path)); return
    # 每一镜归到它前面最近的那个 KP
    group, narrs = {}, {}
    for idx, p in enumerate(spos):
        owner = kp[0][1]
        for s, name in kp:
            if s < p: owner = name
            else: break
        group[owner] = group.get(owner, 0) + 1
        narrs.setdefault(owner, []).append(len(plain(sh[idx][3])) if idx < len(sh) else 0)

    print("\n%s" % os.path.basename(path))
    print("  %d KP / %d 镜　标准 ≥25 / ≥%d　⇒ %s"
          % (len(kp), len(sh), need,
             "已达标" if len(sh) >= need and len(kp) >= 25 else "还缺 %d 镜" % max(0, need - len(sh))))
    print("  %-4s %-46s %s" % ("镜", "知识点", "讲解字数"))
    for _, name in kp:
        c = group.get(name, 0)
        ws = narrs.get(name, [])
        tag = "  ← 该拆" if c <= 1 else ("  ← 偏少" if c == 2 else "")
        print("  %-4d %-46s %s%s"
              % (c, name[:46], "/".join(str(w) for w in ws[:5]), tag))
    thin = [n for _, n in kp if group.get(n, 0) <= 2]
    print("  ⇒ 只有 1–2 镜的知识点：%d 个" % len(thin))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(0)
    for a in args:
        for p in (sorted(glob.glob(a)) or [a]):
            if os.path.isfile(p): report(p)
