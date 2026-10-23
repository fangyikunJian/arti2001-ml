# -*- coding: utf-8 -*-
"""用 CS234 中文精读的 HTML 壳，生成 ARTI2001 M2 的逐页精读。

用法：python build_reader.py M2T1
读 data/M2T1.json，写 M2T1-精读.html（数据内联进 HTML，file:// 直接双击可开）。

data JSON 结构（与 CS234 那套一致）：
{
  "tag": "M2T1", "title": "PCA 与降维", "sub": "Module 2 Topic 1",
  "pdf": "slides/M2T1_PCA.pdf", "pages": 45,
  "notes": [ {"r":[1,2], "t":"标题", "star":2, "one":"一句话",
              "eq":"公式（\\n 换行）", "pts":["要点<b>加粗</b>"],
              "say":"CS229/讲义补的深度",
              "tip":{"t":"标签","v":"内容","w":1}} ],
  "quiz":  { "3": [ {"q":"题干","o":["A","B","C","D"],"a":1,"why":"解析"} ] }
}
注意：quiz 的键必须是某条 note 的 **起始页码**，引擎按 r[0] 取题。
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
# 本地固化的模板壳。原来指向 G:\open course\... 那个外部路径，
# 2026-09-29 那个目录被清空导致构建中断，因此就地固化。
SHELL = os.path.join(HERE, "_shell.html")
_EXTERNAL_FALLBACK = r"G:\open course\reinforcement learning\corpus\cs234-2019\中文精读\L01-精读.html"
if not os.path.exists(SHELL) and os.path.exists(_EXTERNAL_FALLBACK):
    SHELL = _EXTERNAL_FALLBACK


def build(tag):
    data = json.load(io.open(os.path.join(HERE, "data", tag + ".json"), encoding="utf-8"))
    h = io.open(SHELL, encoding="utf-8").read()

    # ── 1. 换掉数据块：从 "var Q = {" 到 "];\n\n(function(){" ──
    i0 = h.index("var Q = {")
    i1 = h.index("(function(){", i0)
    payload = ("var Q = " + json.dumps(data["quiz"], ensure_ascii=False) + ";\n\n"
               "var N = " + json.dumps(data["notes"], ensure_ascii=False) + ";\n\n")
    h = h[:i0] + payload + h[i1:]

    # ── 2. 换 PDF 路径与总页数 ──
    h = re.sub(r'var PDF="[^"]*",\s*MAX=\d+;',
               'var PDF="%s", MAX=%d;' % (data["pdf"], data["pages"]), h)

    # ── 3. 标题、页数徽标 ──
    full = "ARTI2001 " + data["sub"]
    # 正则替换：对「原始 CS234 壳」和「已构建过的阅读器」都成立
    h = re.sub(r"<title>.*?</title>",
               lambda m: "<title>%s · %s · 逐页精读</title>" % (data["sub"], data["title"]),
               h, count=1, flags=re.S)
    h = re.sub(r"<h1>.*?</h1>",
               lambda m: "<h1>%s · <span>%s</span></h1>" % (data["sub"], data["title"]),
               h, count=1, flags=re.S)
    h = re.sub(r'<span id="tot">.*?</span>',
               lambda m: '<span id="tot">/ %d</span>' % data["pages"], h, count=1, flags=re.S)

    # ── 4. localStorage 键（每份独立，互不干扰）──
    # 正则：原始壳是 "l01p"/"l01quiz"，已构建的阅读器是 "m2t1p"/"m2t1quiz" 之类
    h = re.sub(r'"(?:l01|m2t\d)p"', '"%sp"' % tag.lower(), h)
    h = re.sub(r'"(?:l01|m2t\d)quiz"', '"%squiz"' % tag.lower(), h)

    # ── 5. 「打不开？」里的路径说明（整块替换，用非贪婪匹配）──
    new_help = ('<div id="miss">\n'
                '      <p><b>左边没显示课件？</b></p>\n'
                '      <p>本页直接引用同目录下的 <code>{pdf}</code>。</p>\n'
                '      <p>确认文件在即可。若浏览器拦本地 iframe 读 PDF，在 <code>精读</code> 目录下执行\n'
                '      <code>python -m http.server 8080</code>，再访问\n'
                '      <code>http://127.0.0.1:8080/{tag}-精读.html</code>。</p>\n'
                '    </div>').format(pdf=data["pdf"], tag=tag)
    h2, cnt = re.subn(r'<div id="miss">.*?</div>', lambda m: new_help, h, count=1, flags=re.S)
    if cnt != 1:
        print("  ⚠ 没找到 #miss 块，说明文字未替换")
    h = h2

    # ── 6. 「讲稿里补的」标签改成适合本课的说法 ──
    h = h.replace("讲稿里补的", "CS229 / 讲义补充")

    # ── 7. 换成「浅色纸感默认 + 暗色可切换」──
    import theme
    h = theme.apply_theme(h)

    out = os.path.join(HERE, tag + "-精读.html")
    io.open(out, "w", encoding="utf-8").write(h)

    npages = sum(n["r"][1] - n["r"][0] + 1 for n in data["notes"])
    nq = sum(len(v) for v in data["quiz"].values())
    print("%s-精读.html  %d 字节 | %d 条笔记覆盖 %d 页（共 %d 页）| %d 道题"
          % (tag, len(h), len(data["notes"]), npages, data["pages"], nq))

    # 覆盖率自检：每一页都必须有讲解
    covered = set()
    for n in data["notes"]:
        for p in range(n["r"][0], n["r"][1] + 1):
            if p in covered:
                print("  ⚠ 第 %d 页被多条笔记重复覆盖" % p)
            covered.add(p)
    missing = [p for p in range(1, data["pages"] + 1) if p not in covered]
    print("  覆盖率：%d/%d%s" % (len(covered), data["pages"],
                                "" if not missing else "  ⚠ 缺页：%s" % missing))
    # quiz 键必须落在某条笔记的起始页
    starts = {n["r"][0] for n in data["notes"]}
    bad = [k for k in data["quiz"] if int(k) not in starts]
    if bad:
        print("  ⚠ 这些 quiz 键不是任何笔记的起始页，题目不会显示：%s" % bad)


if __name__ == "__main__":
    for t in (sys.argv[1:] or ["M2T1"]):
        build(t)
