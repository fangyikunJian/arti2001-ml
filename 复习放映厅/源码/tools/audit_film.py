# -*- coding: utf-8 -*-
"""放映厅影片静态体检 —— 十七项检查（⑰ 扫构建脚本 .py，其余扫产物 html）。每一条都对应一次真实踩过的坑。
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
import io, os, os, re, subprocess, sys, tempfile

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
# note("文字",…) 与 boxNode(x,y,w,h,"文字",…) 的那个文字实参
NOTE_TXT = re.compile(r'(?:note|boxNode)\(\s*(?:[^,()]*,\s*){0,4}?"((?:[^"\\]|\\.)*)"')
HTMLTAG  = re.compile(r"</?(?:b|u|i|em|strong|span|br|div|p)\b[^>]*>")
# setEq 的内容里「< 紧跟字母/斜杠」会被 innerHTML 当成标签开头 ⇒ 公式整个不渲染。
# 白名单是老片子故意写在公式里的 HTML（加粗之类），要放过。
LT_TAG   = re.compile(r"<[A-Za-z/]")
LT_OK    = re.compile(r"</?(?:b|u|i|em|strong|span|br)\b[^>]*>")
ODD   = re.compile(r"[\u0400-\u04FF\uAC00-\uD7AF\u3040-\u30FF\u0600-\u06FF]")

Y_LIMIT = 390     # 2026-10-27 实测：讲解条（#cap）顶边稳定在画布 y=403。
                  # ⚠ 之前记的「遮挡从 457 起」是在标题帧上量的，字幕当时是空的，不作数。
                  # ⚠ 字幕被下方的讲解文字顶上来，所以讲解越长字幕越高；403 是实测的下限。
NOTE_Y    = 386
NOTE_GAP  = 19   # note 文字框高 18 ⇒ 同镜内相邻两条的 y 至少差这么多   # note 的文字框是 [y-14, y+4]，y<=399 底边才 <=403
EQTOP_MIN = 196    # setEq(…,"top") 的方程底边实测 194，内容不得高于这一行
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
        if y > NOTE_Y:
            bad.append("③ note 的 y=%g 超过 %d: %s" % (y, NOTE_Y, m.group(1)[:42]))

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

    # ⑬ note()/boxNode() 的文字走 d3 的 .text()，**HTML 标签会原样显示在画面上**。
    #    （引擎第 245 行：note 用 .text(t)；boxNode 的 label 也转交给 note。）
    #    2026-10-28 加：build_m2t1.py 里就有一处 note("…<b>要用验证集比</b>")，
    #    一直把 <b> 两个标签画在屏幕上，而前十二项检查全都放过它。
    #    ⚠ 讲解词（narr）走 innerHTML，那里的 HTML 是**对的**，所以只查这两个函数的实参。
    for m in NOTE_TXT.finditer(src):
        t = m.group(1)
        hit = HTMLTAG.findall(t)
        if hit:
            bad.append("⑬ note()/boxNode() 的文字里有 HTML 标签 %s —— "
                       "会原样画在画面上（它走 .text() 不是 innerHTML）：%s"
                       % ("/".join(sorted(set(hit))), t[:46]))

    # ⑭ setEq 里的 `<` 紧跟字母 ⇒ innerHTML 把它当标签，公式整个不渲染（运行时才坏，
    #    前 13 项全查不出来）。2026-10-28 在 CME295 L1 的 perplexity 公式上实测过。
    for m in SETEQ.finditer(src):
        q = m.group(1)
        if not q.strip():
            continue
        rest = LT_OK.sub(" ", q)
        if LT_TAG.search(rest):
            bad.append("⑭ setEq 的 LaTeX 里有「< 紧跟字母」，innerHTML 会当成 HTML 标签 ⇒ "
                       "公式整个不渲染。改写成 \\lt 或换记法：%s"
                       % q[:60])

    # ⑮ 同一镜里两条 note 竖直挨太近 ⇒ 文字框相触。
    #    note 的文字框实测是 [y−14, y+4]（高 18）⇒ 相邻两条的 y 至少差 19。
    #    2026-10-28：CME295 L3 里连犯三次（都是 368/386，正好差 18），前 14 项全放过。
    #    只在「横向也可能重叠」时报 —— 左右两栏各一条、Δy 再近也不碰。
    for shot in re.split(r"S\(\s*\d+\s*,\s*function", src)[1:]:
        ns = []
        for m in re.finditer(r'note\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)', shot):
            t, x, y = m.group(1), float(m.group(2)), float(m.group(3))
            if not t.strip():
                continue
            w = max(40.0, len(t) * 11.0)          # 中文约 11px/字，保守下限 40
            ns.append((y, x - w / 2, x + w / 2, t))
        for a in range(len(ns)):
            for b in range(a + 1, len(ns)):
                ya, la, ra, ta = ns[a]
                yb, lb, rb, tb = ns[b]
                if abs(ya - yb) >= NOTE_GAP:
                    continue
                if ra < lb or rb < la:            # 横向完全错开
                    continue
                bad.append("⑮ 同一镜里两条 note 的 y 只差 %g（文字框高 18，至少要差 %d）"
                           "：「%s」与「%s」" % (abs(ya - yb), NOTE_GAP, ta[:26], tb[:26]))

    # ⑯ stack() / seq() 的几何：这两个辅助函数**自己算**每一格的 y，
    #    所以⑨⑩那种「只认字面 boxNode」的检查完全看不见它们。
    #    2026-10-28：CME295 L3 里 stack 两次把底边算到 390 以上，并压住下方的 note。
    #    签名（本项目通用）：stack(cx, ytop, items, bw, bh, gap) / seq(x0, y, toks, cls, bw, bh)
    for shot in re.split(r"S\(\s*\d+\s*,\s*function", src)[1:]:
        notes_y = []                  # [(y, 左, 右), ...]
        for m in re.finditer(
                r'note\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)', shot):
            if not m.group(1).strip():
                continue
            w = max(40.0, len(m.group(1)) * 11.0)
            nx = float(m.group(2))
            notes_y.append((float(m.group(3)), nx - w / 2, nx + w / 2))
        notes_y.sort()
        for m in re.finditer(r"stack\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*\[(.*?)\]\s*,\s*"
                             r"(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)", shot, re.S):
            ytop, bh, gap = float(m.group(2)), float(m.group(5)), float(m.group(6))
            n = m.group(3).count('["')
            if n < 1:
                continue
            bottom = ytop + (n - 1) * (bh + gap) + bh
            if bottom > Y_LIMIT:
                bad.append("⑯ stack(ytop=%g, n=%d, bh=%g, gap=%g) 底边 y=%g 超过 %d"
                           % (ytop, n, bh, gap, bottom, Y_LIMIT))
            # ⚠ 不能只看「末格标签下方」的 note —— note 也可能落在标签**上方**几像素
            #   （CME295 L4 第 88 帧就是这样漏掉的）。逐格标签都比一遍。
            cx, bw = float(m.group(1)), float(m.group(4))
            sl, sr = cx - bw / 2, cx + bw / 2          # stack 的横向范围
            for k in range(n):
                lab = ytop + k * (bh + gap) + bh / 2 + 5
                near = [t for t in notes_y
                        if abs(t[0] - lab) < NOTE_GAP and not (t[2] < sl or sr < t[1])]
                if near:
                    bad.append("⑯ stack 第 %d 格标签 y=%g 与 note y=%g 只差 %g（至少要差 %d）"
                               % (k + 1, lab, near[0][0], abs(near[0][0] - lab), NOTE_GAP))
                    break
        for m in re.finditer(r"seq\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*\[[^\]]*\]\s*,\s*"
                             r'(?:"[a-z ]*"|\[[^\]]*\])\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)', shot, re.S):
            y, bh = float(m.group(2)), float(m.group(4))
            if y + bh > Y_LIMIT:
                bad.append("⑯ seq(y=%g, bh=%g) 底边 y=%g 超过 %d" % (y, bh, y + bh, Y_LIMIT))
            last = y + bh / 2 + 5
            near = [t for t in notes_y if abs(t[0] - last) < NOTE_GAP]
            if near:
                bad.append("⑯ seq 方块标签 y=%g 与 note y=%g 只差 %g（至少要差 %d）"
                           % (last, near[0][0], abs(near[0][0] - last), NOTE_GAP))

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

    # ⑫ setEq(…,"top") 的方程占到画布 y=194（2026-10-27 在 1440×860 实测：
    #    顶部对齐的两行公式占 y 48→194），所以同一镜的内容不能高于 EQTOP_MIN。
    #    上线片子里最高的是 y=196，这条线和它一致。
    for m in re.finditer(r"clearScene\(\);(.*?)(?=clearScene\(\);|\Z)", body, re.S):
        blk = m.group(1)
        if not re.search(r'setEq\(".*?",\s*"top"\s*\)', blk):
            continue
        ys = []
        for pat in (r"note\(\s*\"[^\"]*\"\s*,\s*-?\d+\s*,\s*(\d+)",
                    r"boxNode\(\s*-?\d+\s*,\s*(\d+)",
                    r"matrix\(\{rows:\d+,\s*cols:\d+,\s*cw:\d+,\s*ch:\d+,\s*x:-?\d+,\s*y:(\d+)",
                    r"axes\(\{x0:\d+,x1:\d+,y0:\d+,y1:(\d+)"):
            ys += [int(x) for x in re.findall(pat, blk)]
        if ys and min(ys) < EQTOP_MIN:
            cap = re.search(r'setCap\("([^"]*)"\)', blk)
            bad.append('⑫ setEq(…,"top") 那一镜的内容从 y=%d 开始，高过 %d：%s'
                       % (min(ys), EQTOP_MIN, (cap.group(1) if cap else "?")[:30]))

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


# ⑰ setEq 的 LaTeX 里不许有「单个反斜杠」—— 场景 JS 会被当成 JS 源码插进 <script>，
#    setEq("$$\theta$$") 里的 \t 在 JS 字符串里是制表符，公式会**静默**变形。
#    ⚠ 这一项扫**构建脚本 .py**，不是产物 html。
EQ_CALL = re.compile(r'setEq\(\s*"((?:[^"' + "\\\\" + r']|' + "\\\\" + r'.)*)"')
LONE_BS = re.compile(r'(?<!' + "\\\\" + r')' + "\\\\" + r'(?!' + "\\\\" + r')')


def check_source(path):
    """扫一个构建脚本/模块，只做第 ⑰ 项；返回问题列表。"""
    src = io.open(path, encoding="utf-8").read()
    out = []
    for m in EQ_CALL.finditer(src):
        inner = m.group(1)
        if LONE_BS.search(inner):
            out.append("⑰ 第 %d 行 setEq 里有单个反斜杠（要写成两个）：%s"
                       % (src.count("\n", 0, m.start()) + 1, inner[:66]))
    return out


def audit_source(path):
    bad = check_source(path)
    name = os.path.basename(path)
    print("%-34s %s" % (name, "✓ 通过（⑰）" if not bad else "✗ %d 个问题" % len(bad)))
    for b in bad:
        print("   " + b)
    return len(bad)


def selftest_17():
    """⑰ 的自检：三条该报、三条不该报。改了正则就要重跑。"""
    import tempfile
    fire = ['setEq("$$' + chr(92) + 'theta$$");',
            'setEq("$$' + chr(92) + 'frac{a}{b}$$");',
            'setEq("$$x ' + chr(92) + 'mid y$$","top");']
    quiet = ['setEq("$$' + chr(92) * 2 + 'theta$$");',
             'setEq("$$' + chr(92) * 2 + 'frac{a}{b}$$","top");',
             'setEq("$$a+b=c$$");']
    bad = []
    for i, line in enumerate(fire + quiet):
        fd, p = tempfile.mkstemp(suffix=".py"); os.close(fd)
        io.open(p, "w", encoding="utf-8").write(line + "\n")
        hit = bool(check_source(p))
        os.unlink(p)
        want = i < len(fire)
        if hit != want:
            bad.append("⑰ 自检第 %d 条%s：%s"
                       % (i + 1, "该报没报" if want else "误报", line))
    return bad


if __name__ == "__main__":
    if "--selftest17" in sys.argv:
        probs = selftest_17()
        print("\n".join(probs) if probs else "⑰ 自检：6/6 条都对")
        sys.exit(1 if probs else 0)
    n = 0
    for p in sys.argv[1:]:
        n += audit_source(p) if p.endswith(".py") else audit(p)
    print("\n合计 %d 个问题" % n)
