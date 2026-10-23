# -*- coding: utf-8 -*-
"""静态检查：matrix 的底边有没有压住同一镜里的 note。

matrix 自己会画出整块单元格，**底边 = y + rows × ch**，
而我总习惯把收尾那条 note 放在 396–404 —— 两者很容易撞上。
这个坑在 [[projector-engine-traps]] 的坑 6 里记过，但一直靠浏览器逐帧扫才发现，
而浏览器那一轮很慢。这里做成静态检查，写完源码立刻能查。

判据：matrix 底边 > 最低 note 的 y − 8，就算撞。
用法：python check_matrix.py build_deck_gmm.py [更多源码...]
"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 场景字符串：r'''…''' 或 r"""…"""
SCENE = re.compile(r"r(?:'''|\"\"\")(.*?)(?:'''|\"\"\")", re.S)
MAT = re.compile(r"matrix\(\{([^}]*?rows\s*:\s*(\d+)[^}]*?)\}", re.S)
NUM = re.compile(r"\b(rows|ch|y)\s*:\s*(\d+)")
NOTE = re.compile(r"note\(\s*(?:\"[^\"]*\"|'[^']*')\s*,\s*[\d.+\-*/A-Za-z()]+\s*,\s*(\d+)")


def check(path):
    src = io.open(path, encoding="utf-8", errors="replace").read()
    bad = []
    for si, m in enumerate(SCENE.finditer(src)):
        scene = m.group(1)
        if "matrix(" not in scene:
            continue
        # 这一镜里 matrix 的几何
        for mm in MAT.finditer(scene):
            d = {k: int(v) for k, v in NUM.findall(mm.group(1))}
            if not {"rows", "ch", "y"} <= set(d):
                continue
            bottom = d["y"] + d["rows"] * d["ch"]
            notes = [int(x) for x in NOTE.findall(scene)]
            low = [n for n in notes if n > d["y"]]          # 只看矩阵下方的 note
            for n in low:
                if bottom > n - 8:
                    line = src[:m.start()].count("\n") + 1
                    bad.append((line, bottom, n, scene.strip()[:46].replace("\n", " ")))
                    break
    return bad


if __name__ == "__main__":
    total = 0
    for p in sys.argv[1:]:
        b = check(p)
        total += len(b)
        print("%-26s %s" % (p, "✓ 没有 matrix 压 note" if not b else "✗ %d 处" % len(b)))
        for line, bot, n, s in b:
            print("    第 %d 行附近：矩阵底边 %d > note 的 %d　｜ %s…" % (line, bot, n, s))
    sys.exit(0 if total == 0 else 1)
