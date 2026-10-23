# -*- coding: utf-8 -*-
"""把这个目录准备成可以公开发布的 GitHub Pages 站点。

做六件事（全部幂等，可以反复跑）：
  1. 写 `.gitignore`（内容来自 rules.py）
  2. 写 `.nojekyll`  —— 否则 Jekyll 会吞掉 `_deploy/` 这种下划线开头的目录
  3. 写 `README.md`
  4. 把根目录的 `index.html` 换成跳转页（它现在是一份 10-16 的旧总入口副本）
  5. 给 `★总入口.html` 注入「公开站模式」：把指向未收录材料的链接标成不可点，
     并在顶部挂一条说明
  6. 给 `精读/*-精读.html` 注入同样的处理：左栏 PDF 不在仓库里时显示一段说明，
     而不是一个空白的 iframe

⚠ 为什么要第 5、6 步：不做的话，公开站上几百条链接直接 404，
  看起来像站坏了。标出来比断掉诚实。
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
import rules  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "deploy-public-mode"          # 注入块的哨兵，用来做幂等替换


def w(rel, text):
    p = os.path.join(ROOT, rel)
    old = io.open(p, encoding="utf-8").read() if os.path.exists(p) else None
    if old == text:
        print("   = %s（没变）" % rel)
        return False
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)
    print("   %s %s" % ("~" if old else "+", rel))
    return True


# ─────────── 1. .gitignore ───────────
print("① .gitignore")
w(".gitignore", rules.gitignore_text())

# ─────────── 2. .nojekyll ───────────
print("② .nojekyll")
w(".nojekyll", "")

# ─────────── 3. README ───────────
print("③ README.md")
README = """# ARTI2001 Machine Learning · 自学资料站

阿德莱德大学 ARTI2001（2026 S2）的一套自用复习材料：**放映厅式逐知识点动画**、
**左课件右讲解的逐页精读**、**可打印的知识点整理与题库**、以及每个 Module 的**备考包**。
三场测验都是开卷纸笔，所以这里的东西都奔着「考场上翻得到、看得懂」做。

> **本仓库里的中文内容全部是原创笔记。学校课件、Tutorial 与官方答案、
> Canvas 讲义原文、CS229 讲义与字幕都不在仓库内**，原因见下。

👉 **入口：[★总入口.html](https://fangyikunjian.github.io/arti2001-ml/)**

## 有什么

| 区 | 内容 |
|---|---|
| **放映厅** | 暗场逐镜动画，一个知识点一镜。CS229 全 21 讲 + 本课 M2 三个 Topic 的深度片，每部 ≥25 知识点 / ≥45 镜 |
| **逐页精读** | 左边挂原始课件、右边逐页写讲解，每页带自测题（共 18 份 242 页 372 题） |
| **打印资料** | M1 / M2 / M3 三套知识点整理与题库 PDF，开卷考试直接带进考场 |
| **备考包** | 速查表 · 答题模板 · 陷阱清单 · 整卷模拟（20 选择 + 4 大题，带参考答案） |
| **考前框架走查** | 考试当天早上 50 分钟，把一个 Module 锁成一根主线 |

## 为什么没有课件和 Tutorial

`.gitignore` 挡着这些（清单在 [`_deploy/rules.py`](_deploy/rules.py)）：

1. **著作权** —— 课件、Tutorial 题目与官方答案、讲师反馈属于阿德莱德大学；
   CS229 讲义与字幕属于 Stanford 与各讲作者。**本仓库不转载。**
2. **个人信息** —— 从官方 PPT 抽出来的文本里带着任课老师的邮箱，不公开。
3. **体积** —— 这些材料占 120 MB 以上，而自己写的内容只有 80 MB 左右。

公开站上，指向这些材料的链接会**自动标成「只在本地有」且不可点**，
不会给你一堆 404。要让它们显示出来，把材料放回对应目录即可：

```
M1材料/课件/           M1材料/Tutorial与Practical/
M2材料/课件/           M2材料/Tutorial与Practical/     M2材料/Canvas讲义/
M3材料/课件/           M3材料/Tutorial与Practical/     M3材料/Canvas讲义/
CS229/notes/          CS229/transcripts/
精读/slides/
```

## 自己跑

纯静态，没有后端。本地直接双击 `★总入口.html` 就能用；
要让逐页精读的左栏 PDF 正常翻页，用一个静态服务器打开：

```bash
python -m http.server 8732
```

## 工具链

| 目录 | 做什么 |
|---|---|
| `复习放映厅/源码/` | 放映厅片子的生成脚本与体检工具（`audit_film.py`、`check_matrix.py` 等） |
| `精读/` | 逐页精读的生成器与各讲内容（`build_reader.py` + `cs229_*.py`） |
| `M*材料/笔记与阅读/_src/` | 打印资料与题库的生成器（`md2doc.py`、`*_quiz.py`、`qcheck.py`、`qbalance.py`） |
| `_deploy/` | 发布规则与这份站点的准备脚本 |

出题有两道闸门：`qcheck.py` 查「选项里带粗体」和「正确答案明显更长」这两种泄题，
`qbalance.py` 用洗牌袋把答案位置打散到极差 ≤ 1。
手算例题的数字都有复算脚本（例如 M3 那套 `verify_m3.py`，165 个数字逐个对）。

## 许可

自己写的内容（HTML / JSON / Python / 生成的 PDF）随便用。
课件等第三方材料不在本仓库内，其权利归原作者所有。
"""
w("README.md", README)

# ─────────── 4. 根目录跳转页 ───────────
print("④ index.html（跳转页）")
INDEX = """<!doctype html>
<meta charset="utf-8">
<title>ARTI2001 Machine Learning</title>
<!--
  根目录跳转页。

  静态服务器在根路径上要么找 index.html、要么列目录，而这个站的真入口叫
  「★总入口.html」。文件名里有 ★（U+2605）和中文，所以三条路都留着：
    1. meta refresh —— 用百分号编码的地址，最稳
    2. <a> 链接 —— 浏览器自己会编码，给跳转被拦时用
    3. 原名写在这条注释里：★总入口.html

  ⚠ 这个文件以前是一份 2026-10-16 的总入口副本（74 KB），会和真入口越差越远。
    2026-10-23 换成跳转页。
-->
<meta http-equiv="refresh"
      content="0; url=%E2%98%85%E6%80%BB%E5%85%A5%E5%8F%A3.html">
<style>
  :root { color-scheme: light dark; }
  body { margin:0; min-height:100vh; display:flex; align-items:center;
         justify-content:center; background:#F5F3EE; color:#23272C;
         font:16px/1.7 "PingFang SC","Microsoft YaHei",system-ui,sans-serif }
  @media (prefers-color-scheme: dark){ body{ background:#080B11; color:#F0F4FA } }
  a { color:#1C6AA6 }
  @media (prefers-color-scheme: dark){ a{ color:#54A9F7 } }
  .box { text-align:center }
  .hint { opacity:.6; font-size:14px; margin-top:1.2em }
</style>
<div class="box">
  <p>正在进入 <a href="★总入口.html">★总入口</a> ……</p>
  <p class="hint">没有自动跳转的话，点上面那个链接。</p>
</div>
"""
w("index.html", INDEX)

# ─────────── 5 / 6 的公共部分：注入块 ───────────
MISSING_JSON = json.dumps(rules.MISSING_PREFIXES, ensure_ascii=False)
ALT_JSON = json.dumps(rules.ALTERNATIVES, ensure_ascii=False)

HUB_PATCH = """
<!-- %s : start ── 由 _deploy/apply.py 注入，别手改 ── -->
<style>
a.nolocal{pointer-events:none;opacity:.42;text-decoration:line-through;
  text-decoration-color:currentColor}
a.nolocal::after{content:"仅本地";font-size:11px;letter-spacing:.02em;
  margin-left:6px;padding:1px 6px;border:1px solid currentColor;border-radius:99px;
  opacity:.8;text-decoration:none;display:inline-block;vertical-align:middle}
#pubnote{max-width:1180px;margin:14px auto 0;padding:11px 16px;border-radius:10px;
  border:1px solid var(--line2,#D2CCC0);background:var(--panel2,#FAF8F4);
  color:var(--dim,#616973);font-size:13.5px;line-height:1.7}
#pubnote b{color:var(--ink,#23272C)}
</style>
<script>
(function(){
  /* 公开站模式：在 *.github.io 上自动生效。本地双击打开、或本地起 http.server
     预览时都不触发 —— 那两种情况下原始材料就在旁边，照常能点。
     本地想看公开站长什么样，地址后面加 ?public=1 。*/
  if (!/\\.github\\.io$/.test(location.hostname)
      && !/[?&]public=1\\b/.test(location.search)) return;
  var MISSING = %s, ALT = %s;
  function hit(href){
    var p; try { p = decodeURIComponent(href); } catch(e) { p = href; }
    p = p.replace(/^\\.\\//, "").split(/[?#]/)[0];
    for (var i = 0; i < MISSING.length; i++){
      var m = MISSING[i];
      if (m.slice(-1) === "/" ? p.indexOf(m) === 0 : p === m) return true;
    }
    return false;
  }
  var n = 0, swapped = 0;
  [].forEach.call(document.querySelectorAll("a[href]"), function(a){
    var h = a.getAttribute("href");
    if (!h || /^(https?:|mailto:|#)/.test(h)) return;
    if (!hit(h)) return;
    var key; try { key = decodeURIComponent(h); } catch(e) { key = h; }
    key = key.replace(/^\\.\\//, "").split(/[?#]/)[0];
    if (ALT[key]) {                       /* 有已发布的替代品 ⇒ 改指它，不划掉 */
      a.setAttribute("href", ALT[key]);
      a.title = "原件（" + key + "）不在公开仓库里，这里改指已发布的 " + ALT[key];
      swapped++;
      return;
    }
    a.classList.add("nolocal");
    a.setAttribute("aria-disabled", "true");
    a.title = "学校课件 / Tutorial 答案 / CS229 讲义等第三方材料不收进公开仓库，"
            + "这一份只在本地有。把文件放回 " + h.split("/").slice(0, -1).join("/") + "/ 即可。";
    n++;
  });
  var note = document.createElement("div");
  note.id = "pubnote";
  note.innerHTML = "<b>这是公开站。</b>学校课件、Tutorial 与官方答案、Canvas 讲义原文、"
    + "CS229 讲义与字幕<b>不在本仓库内</b>（著作权属于学校与各课作者，另有一份抽取文本里带着"
    + "老师的邮箱）。页面上 <b>" + n + "</b> 条指向这些材料的链接已标成「仅本地」并停用"
    + (swapped ? "，另有 " + swapped + " 条改指了已发布的替代品" : "")
    + "；其余内容都是自己写的，照常可用。做法与清单见 "
    + "<a href=\\"https://github.com/fangyikunJian/arti2001-ml#readme\\">README</a>。";
  var hdr = document.querySelector("header.hero") || document.body.firstElementChild;
  if (hdr && hdr.parentNode) hdr.parentNode.insertBefore(note, hdr.nextSibling);
})();
</script>
<!-- %s : end -->
""" % (MARK, MISSING_JSON, ALT_JSON, MARK)

READER_PATCH = """
<!-- %s : start ── 由 _deploy/apply.py 注入，别手改 ── -->
<style>
#nopdf{height:100%%;display:flex;align-items:center;justify-content:center;padding:28px}
#nopdf .in{max-width:380px;text-align:center;font-size:14px;line-height:1.85;
  color:var(--dim,#6a7686)}
#nopdf b{color:var(--ink,#23272c)}
#nopdf code{font-size:12.5px}
</style>
<script>
(function(){
  /* 公开站上 slides/*.pdf 不在仓库里（著作权）。与其让左栏挂一个空 iframe，
     不如说清楚它去哪了 —— 右栏的讲解和自测题完全不受影响。
     本地预览同样加 ?public=1 。*/
  if (!/\\.github\\.io$/.test(location.hostname)
      && !/[?&]public=1\\b/.test(location.search)) return;
  function go(){
    var stage = document.getElementById("stage");
    var frame = document.getElementById("pdf");
    if (!stage) return;
    if (frame) frame.remove();
    var d = document.createElement("div");
    d.id = "nopdf";
    d.innerHTML = '<div class="in"><p><b>原课件不在公开仓库里。</b></p>'
      + '<p>课件著作权属于学校与各课作者，本仓库不转载。</p>'
      + '<p>右栏的逐页讲解与自测题是自己写的，<b>照常可用</b>。</p>'
      + '<p style="opacity:.75">要让这一栏显示出来：把原 PDF 放回 <code>精读/slides/</code>，'
      + '用本地静态服务器打开即可。</p></div>';
    stage.appendChild(d);
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", go);
  else go();
})();
</script>
<!-- %s : end -->
""" % (MARK, MARK)

BLOCK = re.compile(r"\n?<!-- " + MARK + r" : start.*?" + MARK + r" : end -->\n?", re.S)


def inject(rel, patch):
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding="utf-8").read()
    s2 = BLOCK.sub("\n", s)                       # 先清掉上一次注入的，保证幂等
    i = s2.rfind("</body>")
    if i < 0:
        i = len(s2.rstrip())                      # 有些片子没写 </body>
        s3 = s2[:i] + patch + s2[i:]
    else:
        s3 = s2[:i] + patch + s2[i:]
    if s3 == s:
        print("   = %s（没变）" % rel)
        return False
    io.open(p, "w", encoding="utf-8").write(s3)
    print("   ~ %s" % rel)
    return True


print("⑤ ★总入口.html 注入公开站模式")
inject("★总入口.html", HUB_PATCH)

print("⑥ 精读 reader 注入左栏说明")
cnt = 0
for f in sorted(os.listdir(os.path.join(ROOT, "精读"))):
    if f.endswith("-精读.html"):
        cnt += inject(os.path.join("精读", f), patch=READER_PATCH)
print("   共 %d 份有改动" % cnt)

print("\n完成。接着跑 `python _deploy/manifest.py` 看会发布什么。")
