# -*- coding: utf-8 -*-
"""放映厅影片静态体检 —— 八项检查。每一条都对应一次真实踩过的坑。
见 memory/projector-engine-traps.md 与 projector-quality-bar.md。

  ① setEq 必须 $$ 包裹        —— 不包裹 MathJax 不渲染，画面上是一行裸 LaTeX
  ② setEq 不能跨行            —— JS 字符串不能跨行，整片打不开（白屏）
  ③ note 的 y ≤ 405           —— 超了就被讲解条压住
  ④ matrix 的 rows 要和数据行数一致
  ⑤ 类名必须在 CSS 里真的存在  —— 2026-10-14 查出 dots(...,"y") 一直在画白点
  ⑥ axes 的键名               —— 写错导致「所有片子的坐标轴从没画出来」
  ⑦ 多文字系统异常字符         —— 打字时混进过俄文 над/входящ/работ、韩文 억（已 4 次）
  ⑧ node --check              —— 抽出内联脚本做真正的语法检查

⚠ 静态检查过了不代表版面没问题 —— 碰撞和超线必须用真浏览器在 1440×860 下扫。

用法：python audit_film.py <影片.html> [更多...]
"""
import io, os, re, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"G:/Adelaide COMSC/2026S2/Machine Learning/复习放映厅/源码"


def css_classes():
    css = io.open(os.path.join(SRC, "eng.txt"), encoding="utf-8").read()
    out = {}
    for base in ("pt", "fit", "slbl", "box", "cellbg", "celltx"):
        out[base] = set(re.findall(r"\.%s\.([a-z]+)\b" % base, css))
    return out


NOTE  = re.compile(r'note\(\s*("(?:[^"\\]|\\.)*"|[^,]+?)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*(?:,\s*"([a-z ]*)")?')
DOTS  = re.compile(r'dots\(\s*\[.*?\]\s*,\s*"([a-z ]*)"', re.S)
CURVE = re.compile(r'curve\(\s*(?:\[.*?\]|fn\(.*?\)|\w+\(.*?\))\s*,\s*"([a-z ]*)"', re.S)
BOXN  = re.compile(r'boxNode\([^)]*?,\s*"([a-z ]*)"\s*\)')
SETEQ = re.compile(r'setEq\(\s*"((?:[^"\\]|\\.)*)"')
AXES  = re.compile(r"axes\(\{([^}]*)\}\)")
MATRX = re.compile(r"matrix\(\{rows:(\d+),\s*cols:(\d+).*?var t=(\[\[.*?\]\]);", re.S)
ODD   = re.compile(r"[\u0400-\u04FF\uAC00-\uD7AF\u3040-\u30FF\u0600-\u06FF]")

Y_LIMIT = 405
AX_OK = {"x0", "x1", "y0", "y1", "l", "r", "t", "b"}
# "d" 是全体基类统一的「无修饰」约定：落回基础样式。
# 四个基础样式都可读（.pt=ink / .fit=blue / .box=中性灰 / .slbl=--dim 7.51:1）。
NOOP = {"d", "fit", "hl"}


def audit(path):
    src = io.open(path, encoding="utf-8").read()
    name = os.path.basename(path)
    bad = []
    CC = css_classes()
    blocks = re.findall(r"<script>(.*?)</script>", src, re.S)
    body = blocks[-1] if blocks else src

    for m in SETEQ.finditer(body):
        q = m.group(1)
        if not q.strip():
            continue
        if not q.startswith("$$"):
            bad.append("① setEq 没有 $$ 包裹: %s" % q[:52])
        if "\n" in q:
            bad.append("② setEq 跨行（整片会打不开）: %s" % q[:52])
    if re.search(r'setEq\(\s*"[^"]*$', body, re.M):
        bad.append("② 有 setEq 的字符串没在同一行闭合")

    for m in NOTE.finditer(body):
        y = float(m.group(3))
        if y > Y_LIMIT:
            bad.append("③ note 的 y=%g 超过 %d: %s" % (y, Y_LIMIT, m.group(1)[:42]))

    for m in MATRX.finditer(body):
        want = int(m.group(1))
        rows = len(re.findall(r'\[\s*"', m.group(3)))
        if want != rows:
            bad.append("④ matrix 声明 rows:%d 但数据有 %d 行" % (want, rows))

    def chk(cls, where, base):
        for c in cls.split():
            if c in NOOP:
                continue
            if c not in CC[base]:
                bad.append('⑤ %s 用了未定义的类名 "%s"（CSS 里只有 %s）'
                           % (where, c, "/".join(sorted(CC[base])) or "无"))
    for m in DOTS.finditer(body):
        chk(m.group(1), "dots", "pt")
    for m in CURVE.finditer(body):
        chk(m.group(1), "curve", "fit")
    for m in NOTE.finditer(body):
        if m.group(4):
            chk(m.group(4), "note", "slbl")
    for m in BOXN.finditer(body):
        chk(m.group(1), "boxNode", "box")

    for m in AXES.finditer(body):
        for k in re.findall(r"(\w+)\s*:", m.group(1)):
            if k not in AX_OK:
                bad.append('⑥ axes 用了不认的键名 "%s"（只认 %s）'
                           % (k, "/".join(sorted(AX_OK))))

    for m in ODD.finditer(src):
        a, b = max(0, m.start() - 22), m.end() + 22
        bad.append("⑦ 混进了非中英文字符 %r：…%s…"
                   % (m.group(0), src[a:b].replace("\n", " ")))

    fd, tmp = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    io.open(tmp, "w", encoding="utf-8").write(body)
    try:
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode:
            bad.append("⑧ node --check 不通过：\n     "
                       + (r.stderr or "").strip().replace("\n", "\n     ")[:600])
    except FileNotFoundError:
        bad.append("⑧ 没装 node，跳过了语法检查")
    finally:
        os.unlink(tmp)

    # ⑨⑩ 几何：matrix 和 boxNode 的底边必须 ≤ 405（否则被讲解条压住）
    #    公式：matrix 底边 = y+(rows-1)*ch+(ch-3)；boxNode 底边 = y+h
    for m in re.finditer(r"matrix\(\{rows:(\d+),\s*cols:\d+,\s*cw:\d+,\s*ch:(\d+),\s*x:-?\d+,\s*y:(\d+)", body):
        rows, ch, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        bot = y + (rows - 1) * ch + (ch - 3)
        if bot > Y_LIMIT:
            bad.append("⑨ matrix(rows=%d,ch=%d,y=%d) 底边 y=%d 超过 %d"
                       % (rows, ch, y, bot, Y_LIMIT))
    for m in re.finditer(r"boxNode\(\s*-?\d+\s*,\s*(\d+)\s*,\s*\d+\s*,\s*(\d+)", body):
        y, h = int(m.group(1)), int(m.group(2))
        if y + h > Y_LIMIT:
            bad.append("⑩ boxNode(y=%d,h=%d) 底边 y=%d 超过 %d" % (y, h, y + h, Y_LIMIT))

    # ⑪ 调用了却没定义的辅助函数 —— node --check 只查语法，查不出这个。
    #    2026-10-15：L18 的补充镜用了 grid() 而主文件没定义，整片在那一帧抛
    #    ReferenceError，静态体检全绿，是浏览器实扫才抓到的。
    defined = set(re.findall(r"function\s+(\w+)\s*\(", body))
    defined |= set(re.findall(r"var\s+(\w+)\s*=\s*E\.", body))
    defined |= set(re.findall(r"(\w+)\s*=\s*E\.\w+", body))
    builtin = {"Math", "JSON", "Object", "Array", "String", "Number", "Boolean",
               "parseFloat", "parseInt", "isNaN", "console", "window", "document",
               "setTimeout", "d3", "MathJax", "require", "function", "return",
               "if", "for", "while", "var", "new", "typeof", "catch"}
    called = set(re.findall(r"([a-z]\w*)\s*\(", body))
    missing = sorted(c for c in called - defined - builtin
                     if c not in ("t", "cb", "cell", "dim", "hl", "enter", "map",
                                  "join", "push", "split", "slice", "replace",
                                  "indexOf", "toFixed", "exp", "sin", "cos", "pow",
                                  "sqrt", "min", "max", "abs", "round", "floor"))
    for c in missing:
        bad.append("⑪ 调用了未定义的函数 %s()" % c)

    kp = len(re.findall(r'KP\("', body))
    sh = len(re.findall(r"S\(\d+,function", body))
    qz = len(re.findall(r"QUIZ\(", body))
    print("%-34s KP=%-3d 镜=%-3d 测验=%-3d  %s"
          % (name, kp, sh, qz, "✓ 通过" if not bad else "✗ %d 个问题" % len(bad)))
    for b in bad:
        print("   " + b)
    if kp < 25 or sh < 45:
        print("   ⚠ 低于质量线（要求 ≥25 KP、≥45 镜）")
    return len(bad)


if __name__ == "__main__":
    n = sum(audit(p) for p in sys.argv[1:])
    print("\n合计 %d 个问题" % n)
