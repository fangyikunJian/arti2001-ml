# -*- coding: utf-8 -*-
"""放映厅片子的静态体检。直接读**生成好的 HTML**（而不是源码 .py），
所以不管片子是哪一代生成器做的都能查。

⚠ 2026-10-06 重建：原版写在会话的临时目录里，会话一过就没了——
   同一个教训（「构建脚本不要依赖项目目录之外的文件」）在审计脚本上又犯了一次。
   这次放进 复习放映厅/源码/，跟着项目走。

查八项（前四项来自 [[projector-quality-bar]]，中间三项来自 [[projector-engine-traps]]）：
  1. 颗粒度        KP 数 ≥ 25、讲解镜 ≥ 45（新标准；老片子按 ≥20/≥45 看）
  2. 过短讲解      单镜讲解 < 60 字
  3. 推诿词        「详版见」「不在考纲」「这里不展开」这类把责任推走的说法
  4. 术语出场顺序  硬术语必须「先铺后用」：期望 → 凸函数 → Jensen 之类
  5. setEq 包裹    setEq 的内容没有 $$…$$ ⇒ MathJax 不认，LaTeX 原样糊在画面上
  6. note 的 y     上限 405（标题最坏会顶到 417）
  7. note ↔ 公式   同一镜里有居中公式时，note 必须压进 [170, 265]
  8. JS 能不能跑   用 node --check 解析内联脚本。⚠ 前七项都是**静态文本**检查，
                   查不出语法错误 —— 2026-10-08 一个跨行的字符串字面量让整部 L9
                   打不开，而审计照报「全部通过」。有 node 才查，没有就跳过。

用法：
    python audit_film.py ../影片/CS229讲座L9-*.html
    python audit_film.py ../影片/*.html          # 批量，只打印汇总行
"""
import io, os, re, sys, glob

sys.stdout.reconfigure(encoding="utf-8")

# ── 推诿词：把该讲的内容推给别处 ──
DEFLECT = ["详版见", "详见", "详细见", "见 T", "见T", "另见", "参见",
           "不在考纲", "不在本课", "超出本课", "这里不展开", "不再展开",
           "不细讲", "略过", "跳过不讲", "自行", "请参阅"]

# ── 硬术语的依赖关系：(先决术语, 依赖它的术语) ──
#    左边必须在右边之前第一次出现，否则就是「没铺就用」
ORDER = [
    ("期望", "方差"), ("期望", "凸函数"), ("凸函数", "Jensen"), ("期望", "Jensen"),
    ("概率密度", "高斯"), ("高斯", "混合"), ("似然", "最大似然"),
    ("隐变量", "EM"), ("似然", "下界"), ("范数", "正则"),
    ("梯度", "梯度下降"), ("内积", "核"), ("间隔", "对偶"),
    ("熵", "信息增益"), ("方差", "偏差方差"), ("超平面", "间隔"),
]
TERMS = sorted({t for pair in ORDER for t in pair})


def shots(js):
    """抓出所有 S(秒, function(){场景}, "讲解")，返回 [(镜号, 秒, 场景源码, 讲解)]。

    用花括号配对找 function(){…} 的结尾，再取紧随其后的那个字符串字面量——
    正则配不了嵌套花括号，这里只能自己走一遍。
    """
    out = []
    # ⚠ 三代引擎的签名不同：
    #   现行     S(秒, function(){…}, "讲解")
    #   L6-7 那代 S(秒, 源页, function(){…}, "讲解")   ← 中间多一个数字
    #   L2 那代   act(名, [ S_(秒, fn) … ])            ← 讲解不在这里，本脚本不解析
    for m in re.finditer(r"\bS\((\d+)\s*,\s*(?:\d+\s*,\s*)?function\(\)\s*\{", js):
        i = m.end() - 1          # 指向 {
        depth, j, n = 0, i, len(js)
        instr, q, esc = False, "", False
        while j < n:
            c = js[j]
            if instr:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == q: instr = False
            elif c in "\"'":
                instr, q = True, c
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        scene = js[i + 1:j]
        rest = js[j + 1:j + 60000]
        sm = re.match(r'\s*,\s*"((?:[^"\\]|\\.)*)"', rest)
        narr = sm.group(1) if sm else ""
        out.append((len(out), int(m.group(1)), scene, narr))
    return out


def plain(s):
    """去掉 HTML 标签和转义，量真实字数。"""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\\n", "").replace("\\\"", '"').replace("\\\\", "\\")
    return re.sub(r"\s+", "", s)


def js_syntax(html):
    """用 node --check 解析每个内联 <script>。返回报错信息列表；没有 node 就返回 []。"""
    import shutil, subprocess, tempfile, os as _os
    node = shutil.which("node")
    if not node:
        return []
    bad = []
    # ⚠ 片子开头的 HTML 注释里**举例写了 <script>**，不先去掉注释的话，
    #   正则会从那个假标签一路吃到真标签的 </script>，把中文注释当 JS 解析 ⇒ 误报。
    body = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    for i, blk in enumerate(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", body, re.S)):
        if not blk.strip():
            continue
        fd, tmp = tempfile.mkstemp(suffix=".js")
        _os.close(fd)
        io.open(tmp, "w", encoding="utf-8").write(blk)
        try:
            r = subprocess.run([node, "--check", tmp], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if r.returncode != 0:
                err = (r.stderr or "").splitlines()
                # node 的输出形如：<tmp>:<行号>  /  <出错的那行源码>  /  ^  /  SyntaxError: ...
                kind = next((l.strip() for l in err if l.startswith("SyntaxError")), "语法错误")
                lineno = ""
                if err and ":" in err[0]:
                    lineno = err[0].rsplit(":", 1)[-1].strip()
                src = err[1].strip()[:60] if len(err) > 1 else ""
                bad.append("第 %d 个内联脚本 第 %s 行：%s　｜　%s"
                           % (i + 1, lineno or "?", kind[:60], src))
        finally:
            try: _os.remove(tmp)
            except OSError: pass
    return bad


def audit(path, brief=False):
    html = io.open(path, encoding="utf-8", errors="replace").read()
    name = os.path.basename(path)
    sh = shots(html)
    kps = re.findall(r'\bKP\(\s*"((?:[^"\\]|\\.)*)"', html)
    issues = []

    # 不是片子（备考包/走查/逐页精读那类页面），或是本脚本不解析的老引擎 —— 直接说清楚，
    # 别报一个会误导人的「0 KP / 0 镜」
    if not sh and not kps:
        kind = "老引擎 act/S_（本脚本不解析）" if "function S_(" in html else "不是放映厅片子"
        print("—  %-44s %s" % (name[:44], kind))
        return 0

    # 0. JS 语法（最先查：语法错了整部片子打不开，别的问题都是次要的）
    for b in js_syntax(html):
        issues.append(("JS 语法", b))

    # 1. 颗粒度
    if len(kps) < 25: issues.append(("颗粒度", "KP 只有 %d 个（标准 ≥25）" % len(kps)))
    if len(sh) < 45:  issues.append(("颗粒度", "讲解镜只有 %d 个（标准 ≥45）" % len(sh)))

    # 2. 过短讲解
    short = [(i, len(plain(n))) for i, _, _, n in sh if 0 < len(plain(n)) < 60]
    empty = [i for i, _, _, n in sh if not plain(n)]
    if short: issues.append(("过短讲解", "%d 镜 < 60 字：%s" %
                             (len(short), ", ".join("#%d(%d字)" % x for x in short[:6]))))
    if empty: issues.append(("空讲解", "%d 镜没有讲解：%s" % (len(empty), empty[:8])))

    # 3. 推诿词
    #   ⚠ 「」里的不算：那是在**引用**（常见于「上一版写了『详版见 X 片』就跳过去了，
    #   这一版补上」这种自述），不是在推诿。2026-10-06 为此误报过 L15 两处。
    hits = []
    for i, _, _, n in sh:
        t = re.sub(r"[「『][^」』]*[」』]", "", plain(n))
        for w in DEFLECT:
            if w in t: hits.append((i, w))
    if hits: issues.append(("推诿", "%d 处：%s" %
                            (len(hits), ", ".join("#%d「%s」" % x for x in hits[:6]))))

    # 4. 术语出场顺序
    #   ⚠ 跳过第 0 镜：开场那一镜是**整节课的路线图**，本来就会把后面所有术语
    #   都点一遍（「这一讲讲 k-means、混合高斯、EM」），拿它算「首次出现」全是误报。
    first = {}
    for i, _, sc, n in sh:
        if i == 0: continue
        t = plain(n) + plain(sc)
        for term in TERMS:
            if term in t and term not in first: first[term] = i
    bad = [(a, first[a], b, first[b]) for a, b in ORDER
           if a in first and b in first and first[a] > first[b]]
    if bad:
        issues.append(("术语顺序", "; ".join("%s@%d 晚于 %s@%d" % (a, x, b, y)
                                             for a, x, b, y in bad[:4])))

    # 5. setEq 必须 $$ 包裹
    raw = [m.group(1) for m in re.finditer(r'setEq\(\s*"((?:[^"\\]|\\.)*)"', html)]
    naked = [e for e in raw if not (e.strip().startswith("$$") and e.strip().endswith("$$"))]
    if naked:
        issues.append(("setEq", "%d 处没用 $$ 包裹（LaTeX 会原样糊在画面上）：%s" %
                       (len(naked), naked[0][:46])))

    # 6/7. note 的 y，以及同镜有公式时的 note 区间
    #   ⚠ 上限不是写死的 405：标题那一列底部对齐，**讲解越长面板越高、标题被顶得越上去**
    #   （engine-traps 实测：面板 163px → 标题 y=491；245px → 417）。
    #   所以按**这一镜自己的讲解长度**取上限，否则讲解短的老片子会被大面积误报。
    def ylimit(chars):
        if chars >= 200: return 405
        if chars >= 140: return 440
        return 470
    over, collide = [], []
    for i, _, sc, n in sh:
        ys = [float(m.group(1)) for m in
              re.finditer(r'\bnote\(\s*(?:"(?:[^"\\]|\\.)*"|[^,]+)\s*,\s*[^,]+,\s*(-?[\d.]+)', sc)]
        lim = ylimit(len(plain(n)))
        hi = [y for y in ys if y > lim]
        if hi: over.append((i, max(hi), lim))
        # 居中公式占 279–441，只有讲解长（标题高）的镜头才会挤到 note
        if re.search(r'setEq\(\s*"\$\$', sc) and len(plain(n)) >= 200:
            bad_y = [y for y in ys if y > 265]
            if bad_y: collide.append((i, max(bad_y)))
    if over:
        issues.append(("note 出界", "%d 镜超上限（按讲解长度算，浏览器复核为准）：%s" %
                       (len(over), ", ".join("#%d(y=%g>%d)" % x for x in over[:6]))))
    if collide:
        issues.append(("note 压公式", "%d 镜有居中公式却有 y>265 的 note：%s" %
                       (len(collide), ", ".join("#%d(y=%g)" % x for x in collide[:6]))))

    lens = sorted(len(plain(n)) for _, _, _, n in sh if plain(n))
    med = lens[len(lens) // 2] if lens else 0
    flag = "✓" if not issues else "✗"
    print("%s %-44s %2d KP / %2d 镜 / 讲解中位 %d 字 / %d 条 note / %d 个公式"
          % (flag, name[:44], len(kps), len(sh), med,
             len(re.findall(r"\bnote\(", html)), len(raw)))
    if not brief:
        for kind, msg in issues:
            print("      ⚠ %-10s %s" % (kind, msg))
    return len(issues)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(0)
    paths = []
    for a in args:
        paths += sorted(glob.glob(a)) or [a]
    bad = 0
    for p in paths:
        if os.path.isfile(p): bad += audit(p, brief=len(paths) > 6)
    print("\n%d 个文件，%s" % (len(paths), "全部通过" if not bad else "共 %d 项待修" % bad))
