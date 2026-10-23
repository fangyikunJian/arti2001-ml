# -*- coding: utf-8 -*-
"""「官方讲义精读放映厅」的共用骨架。

⚠ 这一批刻意**不**按 CS229 重做版那套参数来写。2026-10-11 量过两条线：
      用户夸的 M2Tx 版：单镜 137–150 字，加粗 30–47%
      用户说「都是细节」的 CS229 重做版：单镜 191–221 字，加粗 62–65%
   而且 M2T1 总字数（14489）其实**比** L15（9693）还多 ——
   所以问题从来不是「内容太多」，是**单屏负荷**和**强调密度**。
   ⇒ 本批的硬指标：**每镜讲解 120–165 字；加粗 ≤35%；每个 KP 第一镜先说「这节回答什么」**。
   三级强调都要用上：<b> 结论 / <em> 次要重点 / <s> 错误说法，别只靠加粗。

⚠ 引擎的坑（见 [[projector-engine-traps]]）：
   · scene 原样插进 JS，只有讲解词过 js() ⇒ LaTeX 写两个反斜杠，**字符串不能跨行**
   · setEq 的内容必须 $$ 包裹
   · note 的 y 上限 405；boxNode 标签画在 y+h/2+5；matrix 底边 = y+rows*ch
   · axes() 两套键名都收（l/r/t/b 或 x0/x1/y0/y1）
"""
import io
import re as _re
import sys

sys.stdout.reconfigure(encoding="utf-8")

TAG = _re.compile(r"<[^>]+>")
BOLD = _re.compile(r"<b>(.*?)</b>", _re.S)


def js(t):
    return '"' + t.replace('\\', '\\\\').replace('"', '\\"') + '"'


MARK = _re.compile(r"[\u26a0\u2605\u2b50\u2016]")


def tone(narr, keep=22):
    """强调降级：长的 <b> 改成 <em>，短的保留；带 ⚠/★/⭐ 的一律保留。

    ⚠ 这不是美化，是可读性问题：加粗过半时读者无法扫读，
      2026-10-11 量出来 CS229 重做版 65%、用户反馈「都是细节」。
    """
    def f(m):
        inner = m.group(1)
        plain = TAG.sub("", inner)
        if len(plain) <= keep or MARK.search(plain):
            return m.group(0)
        return "<em>" + inner + "</em>"
    return BOLD.sub(f, narr)


class Deck(object):
    def __init__(self, title, subtitle, out, htmltitle):
        self.C = []
        self.n = 0
        self.out = out
        self.htmltitle = htmltitle
        self.head = io.open("eng.txt", encoding="utf-8").read()
        self.C.append(r'''(function(){
var E=window.__engine;
var S=E.S,KP=E.KP,SUM=E.SUM,QUIZ=E.QUIZ,W=E.W,H=E.H,rng=E.rng;
var clearScene=E.clearScene,setTitle=E.setTitle,setBig=E.setBig,setCap=E.setCap,
    setEq=E.setEq,flip=E.flip,T=E.T,note=E.note,dots=E.dots,curve=E.curve,fn=E.fn,
    boxNode=E.boxNode,link=E.link,matrix=E.matrix,axes=E.axes,noTitle=E.noTitle;
/* ── 等比坐标映射，安全区 y∈[90,470] ── */
function PX(x){return 640+52*x;}
function PY(y){return 285-52*y;}
function ax(w,h){w=w||5.2;h=h||3.4;
  link(PX(-w),PY(0),PX(w),PY(0));link(PX(0),PY(-h),PX(0),PY(h));
  note("x₁",PX(w)+16,PY(0)+5,"","start");note("x₂",PX(0)+18,PY(h)+2,"","start");}
function P(pts,cls,r){dots(pts.map(function(p){return [PX(p[0]),PY(p[1])];}),cls,r||9);}
function dirLine(vx,vy,t,cls){var n=Math.sqrt(vx*vx+vy*vy),ux=vx/n,uy=vy/n;
  curve([[PX(-t*ux),PY(-t*uy)],[PX(t*ux),PY(t*uy)]],cls||"fit g");}
function feet(pts,vx,vy,cls){var n=Math.sqrt(vx*vx+vy*vy),ux=vx/n,uy=vy/n;
  var F=pts.map(function(p){var s=p[0]*ux+p[1]*uy;return [s*ux,s*uy];});
  pts.forEach(function(p,i){link(PX(p[0]),PY(p[1]),PX(F[i][0]),PY(F[i][1]));});
  P(F,cls||"c",7);return F;}
/* ── 一维高斯 ── */
function bell(cx,cy,w,h,cls){var p=[],i;
  for(i=0;i<=90;i++){var t=-3.4+6.8*i/90;
    p.push([cx+w*t/6.8, cy-h*Math.exp(-t*t/2)]);}
  curve(p,cls||"fit b");}
/* ── 讲义页码标记（右上角）── */
function src(s){note("讲义 "+s,1180,96,"","end");}
''')
        self.CFG = (u'var CFG={title:%s,subtitle:%s,video:""};\n' % (js(title), js(subtitle)))

    # ── 质检：单镜字数与加粗比例 ──
    def _audit(self, nm, narr):
        plain = TAG.sub("", narr.replace("<br>", "　"))
        b = sum(len(TAG.sub("", x)) for x in BOLD.findall(narr))
        pct = 100.0 * b / max(len(plain), 1)
        self.stat.append((nm, len(plain), pct))

    stat = []

    def KP(self, name, shots, summ, quiz):
        self.n += 1
        n = self.n
        nm = '%d · %s' % (n, _re.sub(r'^\s*\d+\s*·\s*', '', name))
        b = ['KP(%s,function(){' % js(nm)]
        for scene, narr in shots:
            narr = tone(narr)          # 强调降级，见上面 tone() 的说明
            self._audit(nm, narr)
            b.append('  S(0,function(){%s},%s);' % (scene, js(narr)))
        fields = ",".join('%s:%s' % (k, js(v)) for k, v in summ.items() if v and k != 'kp')
        b.append('  SUM(0,%d,{%s});' % (n, fields))
        from quizfix import fix_quiz
        quiz = fix_quiz(quiz, n)
        opts = ",".join(js(o) for o in quiz['o'])
        b.append('  QUIZ(0,%d,{t:%s,o:[%s],a:%d,w:%s});'
                 % (n, js(quiz['t']), opts, quiz['a'], js(quiz['w'])))
        b.append('});')
        self.C.append("\n".join(b))

    def raw(self, s):
        self.C.append(s)

    def finish(self):
        self.C.insert(1, self.CFG)
        self.C.append('window.__startProjector(CFG);\n})();')
        body = "\n".join(self.C)
        full = self.head + "<script>\n" + body + "\n</script>\n"
        full = full.replace("<title>放映厅模板</title>",
                            "<title>%s</title>" % self.htmltitle)
        io.open(self.out, "w", encoding="utf-8").write(full)

        import statistics as st
        lens = [x[1] for x in self.stat]
        pcts = [x[2] for x in self.stat]
        over = [(a, b, c) for a, b, c in self.stat if b > 175 or c > 40]
        print("%s: %d bytes | %d KP | %d 镜" % (self.out, len(full), self.n, len(self.stat)))
        print("   单镜字数 中位 %d（%d–%d）   加粗 中位 %.0f%%   "
              "—— 目标 120–165 字 / ≤35%%"
              % (st.median(lens), min(lens), max(lens), st.median(pcts)))
        if over:
            print("   ⚠ 超标 %d 镜：" % len(over))
            for a, b, c in over[:10]:
                print("      %-34s %3d 字  %.0f%%" % (a[:32], b, c))
        from quizfix import report as quizreport
        print("  ", quizreport())
        return not over
