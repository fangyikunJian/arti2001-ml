# -*- coding: utf-8 -*-
"""把一讲的模块源码排成「深度笔记」网页（任意一讲通用）。

为什么要有它（2026-11-07 / 11-10）：
  放映厅从「每镜 430–490 字」压到「约 260 字」之后，砍掉的是延伸分析
  （方法论点评、和课题的联系、论文背景、讲者的措辞与口误）。
  那些文字原封不动就在压缩前的模块源码里 —— 直接取出来排版，
  比重写一遍准确，也不会丢。

  用法（压缩之前先跑，拿当前工作区的源码当底料）：
    python tools/deepnotes.py L1
    python tools/deepnotes.py L6 --rev bfd63af     # 从某个 commit 取
"""
import argparse, io, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:/Adelaide COMSC/2026S2/Machine Learning"
SRC = os.path.join(ROOT, "复习放映厅", "源码")
OUT = os.path.join(ROOT, "复习放映厅", "影片")

SHOT = re.compile(r"\(r'''([\s\S]*?)''',\n\s*\"([\s\S]*?)\", 0\)")
SAYS = re.compile(r'says\(\s*"([\d:]+)"\s*,\s*"((?:[^"\\]|\\.)*)"')
# 模块文件头部那行 `"""CME295 L6 模块 a —— …"""`，取破折号后面那句当小标题
HEAD = re.compile(r'"""CME295 L\d+ 模块 .*?——\s*([\s\S]*?)"""')
TITLE = re.compile(r'title:"(.*?)"')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(narr):
    """旁白是一串 <b>…</b> 和 <br>，切成段落，给 ⭐ / ⚠ 开头的段上色。"""
    out = []
    for p in (x.strip() for x in narr.split("<br>")):
        if not p:
            continue
        plain = re.sub(r"<[^>]+>", "", p).lstrip()
        cls = "star" if plain.startswith("⭐") else ("warn" if plain.startswith("⚠") else "")
        out.append('<p class="%s">%s</p>' % (cls, p))
    return "\n".join(out)


def read(path, rev):
    if rev:
        rel = "复习放映厅/源码/" + os.path.basename(path)
        d = subprocess.run(["git", "show", "%s:%s" % (rev, rel)],
                           cwd=ROOT, capture_output=True).stdout.decode("utf-8")
    else:
        d = io.open(path, encoding="utf-8").read()
    return d.replace(chr(13) + chr(10), chr(10))


def build(key, rev=None):
    mods = sorted(f for f in os.listdir(SRC)
                  if re.fullmatch(r"cme295_%s_[a-z]\.py" % key, f))
    if not mods:
        sys.exit("没找到 %s 的模块文件" % key)
    sections, nav, n = [], [], 0
    for f in mods:
        mod = f[:-3].rsplit("_", 1)[1]
        src = read(os.path.join(SRC, f), rev)
        m = HEAD.search(src)
        sub = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        sub = sub.split("。")[0]
        rng = ""
        r = re.search(r"字幕第 ([\d–\-]+) 句（([\d:–\-]+)）", src)
        if r:
            rng = "句 %s · %s" % (r.group(1), r.group(2))
        cards = []
        for sh in SHOT.finditer(src):
            scene, narr = sh.group(1), sh.group(2)
            sa = SAYS.search(scene)
            n += 1
            cards.append(
                '<article class="card"><div class="meta">'
                '<span class="ts">%s</span><span class="en">%s</span></div>'
                '<div class="body">%s</div></article>'
                % (esc(sa.group(1) if sa else ""), esc(sa.group(2) if sa else ""), fmt(narr)))
        if not cards:
            continue
        sections.append('<section id="m-%s"><h2><span class="tag">模块 %s</span>%s'
                        '<small>%s</small></h2>\n%s\n</section>'
                        % (mod, mod, esc(sub), esc(rng), "\n".join(cards)))
        nav.append('<a href="#m-%s"><b>%s</b> %s</a>' % (mod, mod, esc(sub)))

    bld = read(os.path.join(SRC, "build_cme295_%s.py" % key), rev)
    t = TITLE.search(bld)
    name = t.group(1) if t else ("CME295 " + key)

    html = TPL % dict(name=esc(name), n=n, nav="\n".join(nav),
                      body="\n".join(sections))
    out = os.path.join(OUT, "CME295讲座%s-深度笔记.html" % key)
    io.open(out, "w", encoding="utf-8").write(html)
    print("写出 %s（%d 段，%d KB）" % (os.path.basename(out), n, len(html.encode()) // 1024))


TPL = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(name)s · 深度笔记</title>
<style>
  :root{--bg:#070a12;--panel:#0d1220;--line:#1d2537;--ink:#d7dced;--dim:#8a93ab;
        --y:#f2c94c;--g:#6fcf97;--r:#eb8f7a;--v:#b39ddb;--b:#7fb3ff;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:16px/1.85 -apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;}
  header{position:sticky;top:0;z-index:9;background:rgba(7,10,18,.94);
         border-bottom:1px solid var(--line);backdrop-filter:blur(8px);padding:14px 24px;}
  header h1{margin:0;font-size:17px;letter-spacing:.3px}
  header h1 small{color:var(--dim);font-weight:400;margin-left:10px;font-size:13px}
  .wrap{display:grid;grid-template-columns:270px minmax(0,1fr);gap:28px;
        max-width:1180px;margin:0 auto;padding:24px;}
  nav{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 100px);overflow:auto}
  nav a{display:block;padding:6px 10px;border-radius:7px;color:var(--dim);
        text-decoration:none;font-size:13.5px;line-height:1.5}
  nav a b{color:var(--y);margin-right:7px;font-weight:600}
  nav a:hover{background:#121a2b;color:var(--ink)}
  section{margin:0 0 46px}
  h2{font-size:19px;margin:0 0 18px;padding-bottom:10px;border-bottom:1px solid var(--line)}
  h2 .tag{display:inline-block;font-size:11px;color:var(--bg);background:var(--y);
          border-radius:5px;padding:2px 8px;margin-right:10px;vertical-align:2px;font-weight:700}
  h2 small{display:block;color:var(--dim);font-size:12.5px;font-weight:400;margin-top:5px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;
        padding:16px 20px;margin:0 0 14px}
  .meta{display:flex;gap:12px;align-items:baseline;margin-bottom:10px;
        padding-bottom:9px;border-bottom:1px dashed var(--line)}
  .ts{color:var(--y);font:600 13px ui-monospace,SFMono-Regular,Menlo,monospace;flex:none}
  .en{color:var(--dim);font:13px ui-monospace,SFMono-Regular,Menlo,monospace;
      font-style:italic;word-break:break-word}
  .body p{margin:0 0 9px} .body p:last-child{margin-bottom:0}
  .body p.star{color:var(--y)} .body p.warn{color:var(--r)}
  .body b{color:#fff;font-weight:600}
  .body p.star b{color:var(--y)} .body p.warn b{color:var(--r)}
  .note{background:#101828;border:1px solid var(--line);border-left:3px solid var(--y);
        border-radius:9px;padding:14px 18px;margin:0 0 26px;color:var(--dim);font-size:14.5px}
  .note b{color:var(--ink)}
  @media(max-width:860px){.wrap{grid-template-columns:1fr}
    nav{position:static;max-height:none;display:flex;flex-wrap:wrap;gap:4px}
    nav a{font-size:12.5px}}
</style></head><body>
<header><h1>%(name)s · 深度笔记<small>放映厅精简版之外的延伸分析 —— %(n)d 段，按讲座时间顺序</small></h1></header>
<div class="wrap"><nav>%(nav)s</nav><main>
<div class="note"><b>这份文档是什么。</b>放映厅那部片子走的是精简版：每一镜约 260 字，
只留「讲者说了什么 + 关键机制 + 一个陷阱」。而这里是<b>没被砍的完整版</b> ——
方法论点评、和你课题的联系、论文背景、讲者的措辞与口误，全部保留，按讲座时间顺序排列。<br>
用法建议：<b>先看片子走一遍主线，想深挖某一段时再回到这里按时间码查</b>。
每张卡片的时间码和片子里的原话锚点是同一套。</div>
%(body)s
</main></div></body></html>
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("key", help="比如 L1 / L6")
    ap.add_argument("--rev", default=None, help="从某个 commit 取源码（默认用工作区）")
    a = ap.parse_args()
    build(a.key, a.rev)
