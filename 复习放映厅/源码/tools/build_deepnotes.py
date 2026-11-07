# -*- coding: utf-8 -*-
"""从第三轮（commit bfd63af）的模块源码，生成「CME295 L6 深度笔记」独立网页。

为什么这样做：第四轮把旁白从 430 字压到 264 字，砍掉的是延伸分析（方法论点评、
和课题的联系、论文背景）。而那些文字原封不动都在 bfd63af 里 —— 直接取出来排版，
比重写一遍更准确，也不会丢。
"""
import io, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"G:/Adelaide COMSC/2026S2/Machine Learning/复习放映厅/源码"
REPO = r"G:/Adelaide COMSC/2026S2/Machine Learning"
REV = "bfd63af"

TITLES = {
    "a": ("开场，与 L4 / L5 的回顾", "00:13–08:36"),
    "b": ("vanilla LLM 的四个弱点，与「推理」的定义", "09:15–15:27"),
    "c": ("核心想法：把 chain of thought 放大", "15:59–22:09"),
    "d": ("时间线、思考摘要，与那张账单", "22:35–27:33"),
    "e": ("怎么量推理：benchmark、可验证，与 pass@k", "28:05–35:08"),
    "f": ("pass@k 的推导：它只是无放回抽样", "35:47–44:39"),
    "g": ("温度与 pass@k，以及「为什么不走 SFT」", "45:07–51:15"),
    "h": ("两个可验证奖励、那张曲线，与思考预算", "51:48–58:27"),
    "i": ("GRPO：它只改了 advantage 那一处", "58:58–66:04"),
    "j": ("两张流程图，与两个损失函数的异同", "66:49–73:16"),
    "k": ("最难的那一段，与长度膨胀这个 bug", "73:54–81:23"),
    "l": ("那个坏激励，与三个修改", "82:11–89:40"),
    "m": ("R1-Zero 的配方，与它的两个问题", "90:17–95:23"),
    "n": ("R1 的四个阶段，与蒸馏", "95:49–106:48"),
}

SHOT = re.compile(r"\(r'''([\s\S]*?)''',\n\s*\"([\s\S]*?)\", 0\)")
SAYS = re.compile(r'says\(\s*"([\d:]+)"\s*,\s*"((?:[^"\\]|\\.)*)"')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def old_source(mod):
    return subprocess.run(
        ["git", "show", "%s:复习放映厅/源码/cme295_L6_%s.py" % (REV, mod)],
        cwd=REPO, capture_output=True).stdout.decode("utf-8").replace(chr(13)+chr(10), chr(10))


def fmt(narr):
    """旧旁白是一长串 <b>…</b> 和 <br>，这里切成段落，并给 ⭐ / ⚠ 开头的段上色。"""
    parts = [p.strip() for p in narr.split("<br>") if p.strip()]
    out = []
    for p in parts:
        plain = re.sub(r"<[^>]+>", "", p)
        cls = "star" if plain.lstrip().startswith("⭐") else (
              "warn" if plain.lstrip().startswith("⚠") else "")
        out.append('<p class="%s">%s</p>' % (cls, p))
    return "\n".join(out)


sections, nshot = [], 0
for mod in "abcdefghijklmn":
    src = old_source(mod)
    cards = []
    for m in SHOT.finditer(src):
        scene, narr = m.group(1), m.group(2)
        sa = SAYS.search(scene)
        ts = sa.group(1) if sa else ""
        en = sa.group(2) if sa else ""
        nshot += 1
        cards.append(
            '<article class="card">\n'
            '  <div class="meta"><span class="ts">%s</span>'
            '<span class="en">%s</span></div>\n'
            '  <div class="body">%s</div>\n'
            '</article>' % (esc(ts), esc(en), fmt(narr)))
    t, rng = TITLES[mod]
    sections.append(
        '<section id="m-%s">\n'
        '  <h2><span class="tag">模块 %s</span>%s<small>%s</small></h2>\n%s\n</section>'
        % (mod, mod, esc(t), esc(rng), "\n".join(cards)))

nav = "\n".join(
    '<a href="#m-%s"><b>%s</b> %s</a>' % (m, m, esc(TITLES[m][0])) for m in "abcdefghijklmn")

html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CME295 L6 深度笔记 · LLM 推理</title>
<style>
  :root{
    --bg:#070a12; --panel:#0d1220; --line:#1d2537; --ink:#d7dced; --dim:#8a93ab;
    --y:#f2c94c; --g:#6fcf97; --r:#eb8f7a; --v:#b39ddb; --b:#7fb3ff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:16px/1.85 -apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;}
  header{position:sticky;top:0;z-index:9;background:rgba(7,10,18,.94);
         border-bottom:1px solid var(--line);backdrop-filter:blur(8px);padding:14px 24px;}
  header h1{margin:0;font-size:17px;letter-spacing:.3px}
  header h1 small{color:var(--dim);font-weight:400;margin-left:10px;font-size:13px}
  .wrap{display:grid;grid-template-columns:260px minmax(0,1fr);gap:28px;
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
  .body p{margin:0 0 9px}
  .body p:last-child{margin-bottom:0}
  .body p.star{color:var(--y)}
  .body p.warn{color:var(--r)}
  .body b{color:#fff;font-weight:600}
  .body p.star b{color:var(--y)}
  .body p.warn b{color:var(--r)}
  .note{background:#101828;border:1px solid var(--line);border-left:3px solid var(--y);
        border-radius:9px;padding:14px 18px;margin:0 0 26px;color:var(--dim);font-size:14.5px}
  .note b{color:var(--ink)}
  @media(max-width:860px){.wrap{grid-template-columns:1fr}nav{position:static;max-height:none;
    display:flex;flex-wrap:wrap;gap:4px}nav a{font-size:12.5px}}
</style></head><body>
<header><h1>CME295 L6 深度笔记 · LLM 推理<small>放映厅精简版之外的延伸分析 ——
%d 段，按讲座时间顺序</small></h1></header>
<div class="wrap">
<nav>%s</nav>
<main>
<div class="note"><b>这份文档是什么。</b>放映厅那部片子（145 帧）走的是精简版：
每一镜约 260 字，只留「讲者说了什么 + 关键机制 + 一个陷阱」。
而这里是<b>没被砍的完整版</b> —— 方法论点评、和你课题的联系、论文背景、
讲者的措辞与口误，全部保留，按讲座时间顺序排列。<br>
用法建议：<b>先看片子走一遍主线，想深挖某一段时再回到这里按时间码查</b>。
每张卡片的时间码和片子里的原话锚点是同一套。</div>
%s
</main></div></body></html>
""" % (nshot, nav, "\n".join(sections))

out = os.path.join(REPO, "复习放映厅", "影片", "CME295讲座L6-深度笔记.html")
io.open(out, "w", encoding="utf-8").write(html)
print("写出 %s（%d 段，%d 字节）" % (os.path.basename(out), nshot, len(html.encode("utf-8"))))
