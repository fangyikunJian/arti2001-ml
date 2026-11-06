# -*- coding: utf-8 -*-
"""量「放映厅到底还像不像放映厅」—— 两个数，对着 ARTI2001 M2/M3 那批片子的基准看。

  ① 有图的镜占比：用了 boxNode / seq / link / curve / dots / axes / matrix /
     fn / tiles / gpus / setBig / setEq 的镜。只有 note + stack 的算「纯文字」。
  ② 画面平均字数/镜：scene JS 里所有字符串去掉标签后的字数。

基准（2026-11-06 量的）：
      ARTI2001 M2 T1   有图 81%   画面 69 字/镜      ← 用户认可的那批
      CME295 L6 改之前  有图 17%   画面 258 字/镜     ← 用户说「字多了、动画少了」
  目标：有图 ≥ 60%，画面 ≤ 130 字/镜。

用法：
    python tools/viz_ratio.py cme295_L6_*.py
    python tools/viz_ratio.py --base          # 顺便打印基准那几部
"""
import io
import re
import sys
import glob

sys.stdout.reconfigure(encoding="utf-8")

VIS = ("boxNode(", "seq(", "link(", "curve(", "dots(", "axes(", "matrix(",
       "fn(", "tiles(", "gpus(", "setBig(", "setEq(")
SCENE = re.compile(r"\(r'''([\s\S]*?)''',")
TXT = re.compile(r'"((?:[^"\\]|\\.)*)"')
TAG = re.compile(r"<[^>]+>")
# says() 是时间码锚点，每镜都有，基准那批片子没有 —— 不计入画面字数
SAYS = re.compile(r"says\([^;]*?\);")
# 每镜开头那串 clearScene();setEq(null);setBig(null);... 是「重置」,不算图
RESET = re.compile(r"(?:clearScene|setEq|setBig|setCap|noTitle)\(\s*(?:null)?\s*\);")

GOAL_VIS = 60
GOAL_CHARS = 130


def per_shot(files):
    """逐镜列出画面字数，方便找出还没改的那几镜。"""
    for f in files:
        try:
            src = io.open(f, encoding="utf-8").read()
        except OSError:
            continue
        print("── %s ──" % f)
        for i, m in enumerate(SCENE.finditer(src), 1):
            sc = RESET.sub("", SAYS.sub("", m.group(1)))
            c = 0
            for t in TXT.findall(sc):
                if t.startswith(("$$", "http")) or len(t) <= 3:
                    continue
                c += len(TAG.sub("", t))
            mark = []
            if "stack(" in sc:
                mark.append("stack")
            if not any(v in sc for v in VIS):
                mark.append("纯文字")
            print("   镜 %2d  %3d 字  %s" % (i, c, " ".join(mark)))


def audit(files, label, quiet=False):
    tot = vis = chars = 0
    kinds = {}
    for f in files:
        try:
            s = io.open(f, encoding="utf-8").read()
        except OSError:
            continue
        for m in SCENE.finditer(s):
            sc = RESET.sub("", SAYS.sub("", m.group(1)))
            tot += 1
            hit = False
            for v in VIS:
                # setEq(null) / setBig(null) 是「关掉」，不算图
                if v in sc:
                    hit = True
                    kinds[v[:-1]] = kinds.get(v[:-1], 0) + 1
            if hit:
                vis += 1
            for t in TXT.findall(sc):
                if t.startswith(("$$", "http")) or len(t) <= 3:
                    continue
                chars += len(TAG.sub("", t))
    if not tot:
        return None
    pv = 100.0 * vis / tot
    pc = chars // tot
    flag = "" if (pv >= GOAL_VIS and pc <= GOAL_CHARS) else "   ✗"
    print("%-20s 镜 %3d ｜ 有图 %3d (%2.0f%%) ｜ 画面 %3d 字/镜%s"
          % (label, tot, vis, pv, pc, flag))
    if not quiet:
        top = sorted(kinds.items(), key=lambda kv: -kv[1])[:8]
        if top:
            print("     图元：" + "  ".join("%s×%d" % (k, v) for k, v in top))
    return pv, pc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--base" in sys.argv or not args:
        print("── 基准（用户认可的那批）──")
        audit(["build_m2t1.py"], "ARTI2001 M2 T1", quiet=True)
        audit(["build_m3t1.py", "m3t1film_shots.py"], "ARTI2001 M3 T1", quiet=True)
        audit(["build_m3t2.py", "m3t2film_shots.py"], "ARTI2001 M3 T2", quiet=True)
        print("   目标：有图 ≥ %d%%，画面 ≤ %d 字/镜\n" % (GOAL_VIS, GOAL_CHARS))
    if not args:
        sys.exit()
    files = []
    for a in args:
        files += sorted(glob.glob(a)) or [a]
    if "--per" in sys.argv:
        per_shot(files)
    r = audit(files, "待查", quiet=False)
    if r and (r[0] < GOAL_VIS or r[1] > GOAL_CHARS):
        sys.exit(1)
