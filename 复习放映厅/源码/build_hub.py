# -*- coding: utf-8 -*-
"""把多部课件放映厅合并到一页，带课件切换菜单。输出 hub.html。"""
import io, re
csdocs = io.open("cs_docs.json", encoding="utf-8").read()   # {"l2":"b64",...} 由 build_cs.py 生成

s = io.open("eng.txt", encoding="utf-8").read()   # 已含标题遮挡修复 + 可读性

# ── 1. 再入式改造：切换课件时清空旧 pip 条 ──────────────────────────
s = s.replace(
  'var cur=-1,kpsEl=document.getElementById("kps"),pipEls=[];',
  'var cur=-1,kpsEl=document.getElementById("kps"),pipEls=[];kpsEl.innerHTML="";', 1)

# ── 2. go() 把当前镜号同步到 window.__cur ───────────────────────────
s = s.replace('cur=n;clearQuiz();clearSum();',
              'cur=n;window.__cur=n;clearQuiz();clearSum();', 1)

# ── 3. 菜单函数 + resetFilm（放在 startProjector 之前）─────────────
home_funcs = r'''var homeEl=document.getElementById("home");
function showHome(){if(homeEl)homeEl.style.display="flex";}
function hideHome(){if(homeEl)homeEl.style.display="none";}
function homeOpen(){return !!homeEl&&homeEl.style.display!=="none";}
(function(){var hb=document.getElementById("homeBtn");if(hb)hb.addEventListener("click",showHome);})();
function resetFilm(){SHOTS.length=0;KPS.length=0;window.__cur=-1;
  clearScene();clearQuiz();clearSum();setNarr(null);setBig(null);setEq(null);setCap(null);noTitle();}
function startProjector(CFG){'''
s = s.replace('function startProjector(CFG){', home_funcs, 1)

# ── 4. 事件绑定改成「只绑一次 + 走 window.__go」并加返回菜单键 ───────
i = s.find('window.__go=go;window.__n=SHOTS.length;')
j = s.find('go(0);\n}', i) + len('go(0);\n}')
old_tail = s[i:j]
new_tail = r'''window.__go=go;window.__n=SHOTS.length;window.__kps=KPS;window.__cur=-1;
  if(!window.__wired){window.__wired=1;
    document.getElementById("next").addEventListener("click",function(){if(window.__go)window.__go(window.__cur+1);});
    document.getElementById("prev").addEventListener("click",function(){if(window.__go)window.__go(window.__cur-1,true);});
    window.addEventListener("keydown",function(e){
      if(homeOpen()){if(e.key==="Escape"&&window.__go){e.preventDefault();hideHome();}return;}
      if(e.key===" "||e.key==="ArrowRight"||e.key==="ArrowDown"||e.key==="Enter"){e.preventDefault();window.__go(window.__cur+1);}
      else if(e.key==="ArrowLeft"||e.key==="ArrowUp"||e.key==="Backspace"){e.preventDefault();window.__go(window.__cur-1,true);}
      else if(e.key==="Home"){e.preventDefault();window.__go(0,true);}
      else if(e.key>="1"&&e.key<="9"){var k=KPS[+e.key-1];if(k){e.preventDefault();window.__go(k.from,true);}}
      else if(e.key==="n"||e.key==="N"){e.preventDefault();narrOn=!narrOn;
        var sh=SHOTS[window.__cur];setNarr(sh&&!sh.sum&&!sh.quiz?sh.n:null);
        document.getElementById("kbd").textContent="空格 推进 · ← 回退 · N "+(narrOn?"讲解":"显示讲解");}
      else if(e.key==="Escape"||e.key==="h"||e.key==="H"){e.preventDefault();showHome();}
    });
  }
  go(0);
}'''
assert old_tail in s
s = s.replace(old_tail, new_tail, 1)

# ── 5. __engine 暴露 resetFilm/showHome/hideHome ────────────────────
s = s.replace('W:W,H:H};',
  'W:W,H:H,resetFilm:resetFilm,showHome:showHome,hideHome:hideHome};', 1)

# ── 6. 加入菜单按钮 + 菜单容器 的 markup（放在底部控制条之后）───────
s = s.replace(
  '<div id="strip"><div id="kps"></div><span id="hint"></span></div>',
  '<div id="strip"><div id="kps"></div><span id="hint"></span></div>\n'
  '<button id="homeBtn">≡ 课件库</button>\n<div id="home"></div>', 1)

# ── 7. 菜单 CSS（插到 </style> 之前）────────────────────────────────
home_css = r'''
#homeBtn{position:fixed;top:14px;left:16px;z-index:40;font-family:var(--mono);font-size:12.5px;
  color:var(--dim);background:rgba(16,23,36,.72);border:1px solid var(--edge);border-radius:8px;
  padding:6px 11px;cursor:pointer;backdrop-filter:blur(6px);transition:color .2s,border-color .2s}
#homeBtn:hover{color:var(--ink);border-color:var(--blue)}
#home{position:fixed;inset:0;z-index:60;background:radial-gradient(120% 90% at 50% 0%,#0C1119 0%,#06090E 72%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:36px;padding:5vh 4vw;overflow-y:auto}
.homehd{text-align:center}
.hometitle{font-family:var(--sans);font-weight:800;font-size:clamp(26px,4.6vw,50px);letter-spacing:-.02em;
  color:var(--ink);text-shadow:0 0 40px rgba(84,169,247,.25)}
.homesub{margin-top:.75em;font-family:var(--mono);font-size:clamp(11.5px,1.3vw,15px);color:var(--dim)}
.homegrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;width:100%;max-width:960px}
.filmcard{position:relative;text-align:left;display:flex;flex-direction:column;gap:7px;
  background:#101724;border:1px solid var(--edge);border-left:3px solid var(--acc);border-radius:12px;
  padding:20px 20px 22px;cursor:pointer;color:var(--ink);font-family:var(--sans);
  transition:transform .16s cubic-bezier(.2,.7,.3,1),border-color .16s,box-shadow .16s}
.filmcard:hover{transform:translateY(-3px);border-color:var(--acc);box-shadow:0 12px 34px rgba(0,0,0,.5)}
.filmcard .ftag{font-family:var(--mono);font-size:12px;color:var(--acc);letter-spacing:.06em}
.filmcard .ftitle{font-weight:600;font-size:19px;line-height:1.25}
.filmcard .fsub{font-size:13px;color:var(--dim);line-height:1.5}
.filmcard.soon{cursor:default;opacity:.5;border-left-color:var(--dimmer)}
.filmcard.soon:hover{transform:none;border-color:var(--edge);box-shadow:none}
.filmcard .fsoon{position:absolute;top:14px;right:14px;font-family:var(--mono);font-size:10.5px;
  color:var(--dim);border:1px solid var(--edge);border-radius:20px;padding:2px 8px}
.filmcard.link{text-decoration:none}
.homesec{width:100%;max-width:960px;font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dim);margin:6px 0 -6px;padding-left:2px}
'''
s = s.replace('</style>', home_css + '</style>', 1)

# ── 8. 取标题 ───────────────────────────────────────────────────────
s = s.replace('<title>放映厅模板</title>', '<title>ARTI2001 复习放映厅</title>', 1)

# ── 9. 抽取各片 cfg + body ──────────────────────────────────────────
def extract(fn):
    h = io.open(fn, encoding="utf-8").read()
    c = [b for b in re.findall(r'<script>(.*?)</script>', h, re.S) if 'CFG={title' in b][0]
    i = c.find('var CFG='); end = c.find('};', i) + 1
    cfg = c[i+8:end]                         # {title:...,subtitle:...,video:...}
    sp = c.find('window.__startProjector')
    body = c[end+1:sp].strip()
    return cfg, body

t3cfg, t3body = extract("t3-ppt.html")
t4cfg, t4body = extract("t4-ppt.html")
t2cfg, t2body = extract("t2-ppt.html")
t1cfg, t1body = extract("t1-ppt.html")
n1cfg, n1body = extract("notes1-ppt.html")
n3cfg, n3body = extract("notes3-ppt.html")

# ── 10. 组装内容脚本 ────────────────────────────────────────────────
content = r'''<script>
(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng,
    clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
var FILMS=[];
function film(o){FILMS.push(o);}

film({id:"t4",tag:"T4",accent:"#FFD36E",title:"支持向量机 SVM",sub:"12 知识点 · 间隔 → 核 → 软间隔",
  cfg:__T4CFG__,
  build:function(){
__T4BODY__
  }});

film({id:"t3",tag:"T3",accent:"#54A9F7",title:"分类：感知机 & 逻辑回归",sub:"17 知识点 · 含 Tutorial Q1/Q2 手算",
  cfg:__T3CFG__,
  build:function(){
__T3BODY__
  }});

film({id:"t2",tag:"T2",accent:"#5BDDA8",title:"线性回归",sub:"15 知识点 · 代价函数/梯度下降/正规方程",
  cfg:__T2CFG__,
  build:function(){
__T2BODY__
  }});
film({id:"t1",tag:"T1",accent:"#B48BF5",title:"总览 Overview",sub:"6 知识点 · AI/范式/数学/流程与防泄漏",
  cfg:__T1CFG__,
  build:function(){
__T1BODY__
  }});

/* CS229 讲座片：以 srcdoc 隔离内嵌，页内切换（各自独立引擎，零改写） */
var CS=[
 {tag:"L1",accent:"#7FB3FF",title:"第一讲 · 什么是机器学习",sub:"监督/无监督/强化 · 对应 T1",href:"https://claude.ai/code/artifact/0babad6b-40c9-4d5f-b73e-990d87f490d6"},
 {tag:"L2",accent:"#5BDDA8",title:"第二讲 · 线性回归与梯度下降",sub:"最小二乘 · 批量/随机 · 对应 T2",lec:"l2"},
 {tag:"L3",accent:"#54A9F7",title:"第三讲 · 为什么是平方误差 + 逻辑回归",sub:"MLE⇒最小二乘 · sigmoid · 对应 T2/T3",lec:"l3"},
 {tag:"L6+7",accent:"#FFD36E",title:"第六·七讲 · 支持向量机",sub:"间隔 → 核 → 软间隔 · 对应 T4",lec:"l67"},
 {tag:"L8",accent:"#B48BF5",title:"第八讲 · 偏差方差与诚实评估",sub:"过拟合 · 交叉验证 · 对应 T1",lec:"l8"}
];

/* CS229 官方讲义（notes）深度推导，原生页内切换 */
var NOTES=[
 {tag:"讲义①",accent:"#5BDDA8",title:"监督学习（notes1）",sub:"LMS·正规方程·MLE⇒最小二乘·逻辑回归·GLM · 对 T2/T3",
  cfg:__N1CFG__, build:function(){
__N1BODY__
  }},
 {tag:"讲义③",accent:"#FFD36E",title:"核方法与 SVM（notes3）",sub:"特征映射·核技巧·Mercer·间隔·对偶·支持向量 · 对 T4",
  cfg:__N3CFG__, build:function(){
__N3BODY__
  }}
];

/* ── 隔离内嵌讲座（srcdoc iframe）机制 ── */
var CSDOC=__CSDOC__;
var ifr=document.createElement("iframe");
ifr.id="filmFrame";ifr.setAttribute("sandbox","allow-scripts allow-popups allow-popups-to-escape-sandbox");
ifr.style.cssText="position:fixed;inset:0;width:100%;height:100%;border:0;z-index:65;background:#080B11;display:none";
document.body.appendChild(ifr);
var ifBack=document.createElement("button");
ifBack.id="ifBack";ifBack.textContent="≡ 课件库";
ifBack.style.cssText="position:fixed;top:13px;left:15px;z-index:80;display:none;font-family:var(--mono);"
 +"font-size:12.5px;color:#C7D2E0;background:rgba(16,23,36,.86);border:1px solid #2A3546;border-radius:8px;"
 +"padding:7px 12px;cursor:pointer;backdrop-filter:blur(6px)";
document.body.appendChild(ifBack);
function b64utf8(b){return new TextDecoder().decode(Uint8Array.from(atob(b),function(c){return c.charCodeAt(0);}));}
window.__openLecture=function(id){var b=CSDOC[id];if(!b)return;
  ifr.srcdoc=b64utf8(b);ifr.style.display="block";ifBack.style.display="block";
  setTimeout(function(){try{ifr.focus();}catch(e){}},80);};
ifBack.addEventListener("click",function(){ifr.style.display="none";ifr.removeAttribute("srcdoc");ifBack.style.display="none";E.showHome();});

window.__loadFilm=function(f){if(f.soon||f.href||f.lec)return;E.resetFilm();f.build();window.__startProjector(f.cfg);E.hideHome();};
function makeCard(f){
  var isLink=!!f.href, isLec=!!f.lec, tagName=isLink?"a":(f.soon?"div":"button");
  var c=document.createElement(tagName);c.className="filmcard"+(f.soon?" soon":"")+(isLink?" link":"");
  c.style.setProperty("--acc",f.accent||"#54A9F7");
  var badge=f.soon?'<span class="fsoon">即将上线</span>':(isLink?'<span class="fsoon">新标签 ↗</span>':'');
  c.innerHTML='<span class="ftag">'+f.tag+'</span><span class="ftitle">'+f.title+'</span>'
    +'<span class="fsub">'+f.sub+'</span>'+badge;
  if(isLink){c.href=f.href;c.target="_blank";c.rel="noopener";}
  else if(isLec)c.addEventListener("click",function(){window.__openLecture(f.lec);});
  else if(!f.soon)c.addEventListener("click",function(){window.__loadFilm(f);});
  return c;
}
function renderHome(){
  var h=document.getElementById("home");h.innerHTML="";
  var hd=document.createElement("div");hd.className="homehd";
  hd.innerHTML='<div class="hometitle">ARTI2001 复习放映厅</div>'
    +'<div class="homesub">点课件页内进入 · 空格推进 · N 讲解 · 左上「≡ 课件库」返回菜单</div>';
  h.appendChild(hd);
  var s1=document.createElement("div");s1.className="homesec";s1.textContent="官方课件（逐张精读 · 页内切换）";
  h.appendChild(s1);
  var g=document.createElement("div");g.className="homegrid";
  FILMS.forEach(function(f){g.appendChild(makeCard(f));});
  h.appendChild(g);
  var s2=document.createElement("div");s2.className="homesec";s2.textContent="CS229 斯坦福讲座（理解「为什么」· 页内切换）";
  h.appendChild(s2);
  var g2=document.createElement("div");g2.className="homegrid";
  CS.forEach(function(f){g2.appendChild(makeCard(f));});
  h.appendChild(g2);
  var s3=document.createElement("div");s3.className="homesec";s3.textContent="CS229 官方讲义（深度推导 · 页内切换）";
  h.appendChild(s3);
  var g3=document.createElement("div");g3.className="homegrid";
  NOTES.forEach(function(f){g3.appendChild(makeCard(f));});
  h.appendChild(g3);
}
renderHome();E.showHome();
})();
</script>
'''
content = (content.replace("__T4CFG__", t4cfg).replace("__T3CFG__", t3cfg)
                  .replace("__T4BODY__", t4body).replace("__T3BODY__", t3body)
                  .replace("__T2CFG__", t2cfg).replace("__T2BODY__", t2body)
                  .replace("__T1CFG__", t1cfg).replace("__T1BODY__", t1body)
                  .replace("__N1CFG__", n1cfg).replace("__N1BODY__", n1body)
                  .replace("__N3CFG__", n3cfg).replace("__N3BODY__", n3body)
                  .replace("__CSDOC__", csdocs))

full = s + content
io.open("hub.html", "w", encoding="utf-8").write(full)
print("hub.html written:", len(full), "bytes")
print("films embedded: T4(", len(t4body), ") T3(", len(t3body), ") + T2/T1 stubs")
