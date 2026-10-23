# -*- coding: utf-8 -*-
"""阅读页统一主题：浅色纸感为默认，暗色可一键切换。

用途：被 build_reader.py 调用，把 CS234 那套写死暗色的 HTML 壳改造成双主题。
放映厅的片子不用这套（它们保持暗场）。
"""

# ── 写死的颜色 → 变量名 ────────────────────────────────────────────
HARDCODED = {
    "#0a0e14": "--sunken",     # 按钮 / 输入框 / 代码底
    "#0d141c": "--hover",      # 选项 hover 底
    "#070a0f": "--stage",      # 左栏舞台底（PDF 四周）
    "#26303f": "--dot",        # 答题历史小方块（空）
    "#18212e": "--dot",        # strip 空页
    "#2c3c52": "--dot2",       # strip 有讲解
    "#7a3a3a": "--errdot",     # strip 错题
    "#2a3b4f": "--line2",      # .say 边框
    "#4a2b2e": "--warnline",   # .tip.w2 边框
    "#f4f8fd": "--ink2",       # .one 亮字
    "#c3d2e3": "--ink3",       # .why 次正文
    "#cfe3f5": "--codeink",    # 行内代码字
    "#dbe8f7": "--eqink",      # 公式块字
    "#d8fff4": "--okink",      # 答对选项字
    "#ffdede": "--noink",      # 答错选项字
}

# 半透明填充 → 变量名（浅色下原值太淡或反了，必须换）
RGBA = {
    "rgba(111,211,187,.13)": "--okfill",
    "rgba(255,143,143,.12)": "--nofill",
    "rgba(10,14,20,.97)": "--missbg",       # 「打不开？」遮罩，暗色下是近黑
    "rgba(111,211,187,.09)": "--tintacc",   # .one 左条底
    "rgba(111,211,187,.07)": "--tintacc2",  # .why 左条底
    "rgba(127,184,255,.055)": "--tintblue", # .say 底
    "rgba(255,120,120,.055)": "--tintwarn", # .tip.w2 底
    "rgba(255,143,143,.08)": "--tintwarn2", # 复习模式 chip
    "rgba(255,255,255,.022)": "--lift",     # .qq 底（暗色下靠提亮，浅色下要反过来）
    "rgba(255,255,255,.025)": "--lift2",    # .tip 底
    "rgba(6,9,13,.82)": "--scrim",          # 错题本遮罩
    "0 10px 34px rgba(0,0,0,.55)": "--shadow",  # #stage 投影
}

# ── 两套调色板 ────────────────────────────────────────────────────
LIGHT = """
  --bg:#F5F3EE; --panel:#FFFFFF; --panel2:#FAF8F4; --sunken:#EDEAE3;
  --stage:#E9E6DF; --hover:#F0EDE6;
  --line:#E3DFD6; --line2:#D2CCC0;
  --dot:#DDD8CE; --dot2:#B9B1A2; --errdot:#D08A8A;
  --ink:#23272C; --ink2:#111417; --ink3:#4A525C; --dim:#616973;
  --acc:#0E7355; --acc2:#845808; --warn:#B23540; --blue:#1C6AA6;
  --mark:#FFF6DC; --codeink:#17506E; --eqink:#1E2833;
  --okink:#0B5B43; --noink:#8F2A33; --violet:#6A4BA3; --tintviolet:rgba(106,75,163,.07);
  --okfill:rgba(14,115,85,.10); --nofill:rgba(178,53,64,.09);
  --missbg:rgba(245,243,238,.97);
  --tintacc:rgba(14,115,85,.07); --tintacc2:rgba(14,115,85,.05);
  --tintblue:rgba(28,106,166,.06); --tintwarn:rgba(178,53,64,.05);
  --tintwarn2:rgba(178,53,64,.06);
  --lift:rgba(60,54,44,.022); --lift2:rgba(60,54,44,.028);
  --scrim:rgba(58,52,42,.40);
  --shadow:0 1px 2px rgba(40,34,20,.05), 0 6px 18px rgba(40,34,20,.05);
"""

DARK = """
  --bg:#0b0f15; --panel:#121823; --panel2:#0d141c; --sunken:#0a0e14;
  --stage:#070a0f; --hover:#0d141c;
  --line:#212c3c; --line2:#2a3b4f;
  --dot:#18212e; --dot2:#2c3c52; --errdot:#7a3a3a;
  --ink:#e7eef7; --ink2:#f4f8fd; --ink3:#c3d2e3; --dim:#8b9ab0;
  --acc:#6fd3bb; --acc2:#f2bd63; --warn:#ff8f8f; --blue:#7fb8ff;
  --mark:#16202e; --codeink:#cfe3f5; --eqink:#dbe8f7;
  --okink:#d8fff4; --noink:#ffdede; --violet:#B48BF5; --tintviolet:rgba(180,139,245,.08);
  --okfill:rgba(111,211,187,.13); --nofill:rgba(255,143,143,.12);
  --missbg:rgba(10,14,20,.97);
  --tintacc:rgba(111,211,187,.09); --tintacc2:rgba(111,211,187,.07);
  --tintblue:rgba(127,184,255,.055); --tintwarn:rgba(255,120,120,.055);
  --tintwarn2:rgba(255,143,143,.08);
  --lift:rgba(255,255,255,.022); --lift2:rgba(255,255,255,.025);
  --scrim:rgba(6,9,13,.82);
  --shadow:0 10px 34px rgba(0,0,0,.55);
"""

# 浅色下需要补的细节：卡片投影、字重微调、面板去掉过重的边框
EXTRA_CSS = """
/* ══ EXTRA_CSS:BEGIN ══ */
/* ══ 讲解区里的链接兜底 ══
   ⚠ 2026-10-03 查出来的：原先只给 .ng a 上了色，放在 tip / say / pts / exam 里的链接
   会退回浏览器默认的 #0000EE —— 浅色下还能看（8.47:1），**暗色下只有 1.95:1**。
   做 notes2 时第一次往 tip 里放时间码链接就撞上了。这条规则管住所有其它位置。 */
#card a{color:var(--blue);text-decoration:none;border-bottom:1px solid var(--blue)}
#card a:hover{opacity:.75}

/* ══ 「从零补基础 · Andrew Ng」栏 ══ */
.ng{border:1px solid var(--line);border-left:3px solid var(--violet);border-radius:0 8px 8px 0;
  padding:11px 15px;margin:14px 0;font-size:13.5px;line-height:1.72;background:var(--tintviolet)}
.ng .t{display:block;font-size:11.5px;font-family:var(--mono);color:var(--violet);
  letter-spacing:.4px;margin-bottom:5px}
/* ⚠ 要用 #card .ng a 而不是 .ng a —— 上面的兜底规则带了 #card 这个 id，
   光写 .ng a（0,1,1）会被 #card a（1,0,1）压过去，紫色链接会变蓝。 */
#card .ng a{color:var(--violet);text-decoration:none;border-bottom:1px solid var(--violet)}
#card .ng a:hover{opacity:.75}
.ng .src{display:block;margin-top:6px;font-family:var(--mono);font-size:11.5px;color:var(--dim)}
:root:not([data-theme="dark"]) .ng{box-shadow:var(--shadow)}

/* ══ 「课件原话」栏：引官方英文 ══ */
.quote{border-left:3px solid var(--dim);background:var(--lift2);border-radius:0 8px 8px 0;
  padding:10px 15px;margin:12px 0;font-size:13px;line-height:1.7;color:var(--ink3)}
.quote .t{display:block;font-size:11.5px;font-family:var(--mono);color:var(--dim);
  letter-spacing:.4px;margin-bottom:5px}
.quote b{color:var(--ink2)}
.quote em{font-style:normal;color:var(--ink2);font-weight:560}

/* ══ 笔记表格：对比表 / 情况表 / 数值表 ══ */
.tw{margin:13px 0;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.tc{font-size:11.5px;font-family:var(--mono);color:var(--dim);letter-spacing:.3px;
  padding:7px 12px;background:var(--sunken);border-bottom:1px solid var(--line)}
table.nt{width:100%;border-collapse:collapse;font-size:12.8px;line-height:1.55}
table.nt th{text-align:left;font-weight:620;font-size:11.5px;color:var(--dim);
  background:var(--panel2);padding:7px 11px;border-bottom:1px solid var(--line);white-space:nowrap}
table.nt td{padding:7px 11px;border-bottom:1px solid var(--line);vertical-align:top}
table.nt tbody tr:last-child td{border-bottom:none}
table.nt td:first-child{font-weight:560;color:var(--ink2)}
table.nt b{color:var(--ink2)}
:root:not([data-theme="dark"]) .tw{box-shadow:var(--shadow)}

/* ══ 「与考试的联系」栏 ══ */
.exam{border:1px solid var(--line);border-left:3px solid var(--acc2);border-radius:0 8px 8px 0;
  padding:11px 15px;margin:14px 0;font-size:13.5px;line-height:1.72;background:var(--tintacc2)}
.exam .t{display:block;font-size:11.5px;font-family:var(--mono);color:var(--acc2);
  letter-spacing:.4px;margin-bottom:5px}
:root:not([data-theme="dark"]) .exam{box-shadow:var(--shadow)}

/* ══ 双主题补丁：浅色下的可读性与质感 ══ */
html{color-scheme:light dark}
:root:not([data-theme="dark"]) #right{background:var(--bg)}
:root:not([data-theme="dark"]) .quiz,
:root:not([data-theme="dark"]) details,
:root:not([data-theme="dark"]) .opt{box-shadow:var(--shadow)}
:root:not([data-theme="dark"]) body{-webkit-font-smoothing:antialiased}
:root:not([data-theme="dark"]) h2{letter-spacing:-.1px}
:root:not([data-theme="dark"]) .one{font-weight:520}
:root:not([data-theme="dark"]) .pg{color:#fff}
:root:not([data-theme="dark"]) #strip b.on{background:var(--acc2)}
/* 主题切换按钮 */
#themeBtn{min-width:34px;text-align:center;font-size:14px;line-height:1}
/* ══ EXTRA_CSS:END ══ */
"""

TOGGLE_JS = """
/* ══ 主题切换：浅色默认，记住选择 ══ */
(function(){
  var KEY = "mlreader-theme";
  var root = document.documentElement, btn = document.getElementById("themeBtn");
  function apply(t){
    root.setAttribute("data-theme", t);
    if (btn) btn.textContent = (t === "dark" ? "☀" : "☾");
    if (btn) btn.title = (t === "dark" ? "切到浅色" : "切到暗色");
  }
  var saved;
  try { saved = localStorage.getItem(KEY); } catch(e){}
  apply(saved === "dark" ? "dark" : "light");
  if (btn) btn.addEventListener("click", function(){
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    apply(next);
    try { localStorage.setItem(KEY, next); } catch(e){}
  });
})();
"""


def apply_theme(html, btn_anchor='<button class="btn" id="help">'):
    """把写死暗色的 HTML 壳改造成「浅色默认 + 暗色可切换」。"""
    import re

    # 幂等守卫：已经上过主题的文件重复调用会重复插按钮与脚本。
    # ⚠ 2026-10-03 改：原来是直接 return，于是改了 EXTRA_CSS 也传不到成品上
    #   —— 因为 _shell.html 本身早就上过主题，每次构建都走这条早退分支。
    #   现在改成「按哨兵定位，把旧的样式块换成当前的 EXTRA_CSS」，仍然幂等
    #   （连跑两次 md5 不变），但样式改动能真正生效。
    if 'id="themeBtn"' in html:
        block = re.search(r"/\* ══ EXTRA_CSS:BEGIN ══ \*/.*?/\* ══ EXTRA_CSS:END ══ \*/",
                          html, re.S)
        if block:
            html = html[:block.start()] + EXTRA_CSS.strip() + html[block.end():]
        else:
            print("  ⚠ 壳里没有 EXTRA_CSS 哨兵，样式块未刷新（老文件，跑一次 --reshell 即可）")
        return html

    # 0a. 让渲染函数认识新的 exam 字段（「与考试的联系」栏，排在 say 之后、tip 之前）
    tip_line = ('if(n.tip) h+=\'<div class="tip\'+(n.tip.w?" w2":"")+\'">'
                '<span class="t">\'+n.tip.t+\'</span>\'+n.tip.v+\'</div>\';')
    if tip_line in html:
        # 课件原话：引官方英文。M1 那套高质量笔记的标志性做法之一
        quote_line = ('if(n.quote) h+=\'<div class="quote"><span class="t">课件原话</span>\''
                      '+n.quote+\'</div>\';')
        # 表格：对比表 / 情况表 / 数值表。tbl 是 [{cap,head,rows}] 数组
        tbl_line = ('if(n.tbl) h+=n.tbl.map(function(T){'
                    'var s=\'<div class="tw">\'+(T.cap?\'<div class="tc">\'+T.cap+\'</div>\':"")'
                    '+\'<table class="nt">\';'
                    'if(T.head) s+=\'<thead><tr>\'+T.head.map(function(c){'
                    'return \'<th>\'+c+\'</th>\';}).join("")+\'</tr></thead>\';'
                    's+=\'<tbody>\'+T.rows.map(function(r){return \'<tr>\'+r.map(function(c){'
                    'return \'<td>\'+c+\'</td>\';}).join("")+\'</tr>\';}).join("")'
                    '+\'</tbody></table></div>\';'
                    'return s;}).join("");')
        ng_line = ('if(n.ng) h+=\'<div class="ng"><span class="t">从零补基础 · Andrew Ng CS229</span>\''
                   '+n.ng+\'</div>\';')
        exam_line = ('if(n.exam) h+=\'<div class="exam"><span class="t">与考试的联系</span>\''
                     '+n.exam+\'</div>\';')
        html = html.replace(tip_line,
                            ng_line + '\n    ' + exam_line + '\n    ' + tip_line, 1)

        one_line = 'if(n.one) h+=\'<div class="one">\'+n.one+\'</div>\';'
        if one_line in html:
            html = html.replace(one_line, one_line + '\n    ' + quote_line, 1)
        else:
            print("  ⚠ 没找到 one 渲染行，quote 未接入")

        pts_line = ('if(n.pts) h+=\'<ul>\'+n.pts.map(function(x){ return "<li>"+x+"</li>"; })'
                    '.join("")+\'</ul>\';')
        if pts_line in html:
            html = html.replace(pts_line, pts_line + '\n    ' + tbl_line, 1)
        else:
            print("  ⚠ 没找到 pts 渲染行，tbl 未接入")

    # 0. ⚠ 加粗字被写死成纯白（暗色下是最亮层，浅色下对比度只有 1.11 等于隐形）。
    #    只能定点替换：#fff 还被 #stage（PDF 底）和 .pg（彩底上的白字）用着，不能一刀切。
    html = html.replace("b{font-weight:650;color:#fff}",
                        "b{font-weight:650;color:var(--ink2)}")

    # 1. 写死的颜色 → 变量
    for hexv, var in HARDCODED.items():
        html = re.sub(re.escape(hexv), "var(%s)" % var, html, flags=re.I)
    for rg, var in RGBA.items():
        html = html.replace(rg, "var(%s)" % var)

    # 2. 替换 :root 里的调色板（保留字体与尺寸变量）
    m = re.search(r":root\{(.*?)\}", html, re.S)
    keep = [ln.strip() for ln in m.group(1).split("\n")
            if ln.strip() and ln.strip().startswith("--")
            and not re.match(r"--(bg|panel|line|ink|dim|acc|acc2|warn|blue|mark)\s*:", ln.strip())]
    html = (html[:m.start()]
            + ":root{" + LIGHT + "\n  " + "\n  ".join(keep) + "\n}\n"
            + ':root[data-theme="dark"]{' + DARK + "}\n"
            + html[m.end():])

    # 2b. 补丁 CSS 必须放在 <style> 末尾 —— 否则同级选择器被后面的原规则盖掉
    html = html.replace("</style>", EXTRA_CSS + "\n</style>", 1)

    # 3. 插入切换按钮
    html = html.replace(btn_anchor,
                        '<button class="btn" id="themeBtn" title="切换主题">☾</button>\n  ' + btn_anchor, 1)

    # 4. 插入切换脚本（放在第一个 <script> 之后最稳）
    i = html.index("<script>") + len("<script>")
    html = html[:i] + "\n" + TOGGLE_JS + html[i:]
    return html
