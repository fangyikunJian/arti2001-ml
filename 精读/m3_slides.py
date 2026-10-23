# -*- coding: utf-8 -*-
"""M3 版的 make_slides：裁页 + 抽正文/备注讲稿，供写逐页讲解用。

素材（2026-10-24 用户下载，已归位到 M3材料/课件/）：
  · M3T1_NeuralNetworks.pdf   36 页  ← 本来就是 PDF，没有 pptx，所以**没有备注讲稿**
  · M3T2_Activation_Loss.pptx 21 张  备注 13454 字符
  · M3T3_Model_Evaluation.pptx 18 张  备注 13155 字符

剔除规则：只删原住民致辞页。
⚠ T1 的 p17/p28/p30 抽不到文字但**都是图表页**，不能删；
  p36 看过是纯校徽页（只有 Adelaide University logo），**要删**（p17/p28/p30 是图表页），
  是图表页不是空白页，**不能删**。

⚠⚠ 裁页是**原地覆盖**的，重复跑会越裁越少。所以这里加了守卫：
   先看当前页数，等于原始页数才裁；已经裁过就跳过。
   （M2 做 T2 时就因为重复跑把真实内容切掉过一页。）

用法：python m3_slides.py
"""
import io, os, re, sys, zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader, PdfWriter

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"G:\Adelaide COMSC\2026S2\Machine Learning"
HERE = os.path.join(BASE, "精读")
OUT = os.path.join(HERE, "slides")
TXT = os.path.join(HERE, "src")
PPTDIR = os.path.join(BASE, "M3材料", "课件")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TXT, exist_ok=True)

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# (tag, pptx 文件名或 None, 原始页数, 要删的原始页码)
JOBS = [
    ("M3T1_NeuralNetworks", None,                        36, [36]),   # p36 是纯校徽页
    ("M3T2_Activation_Loss", "M3T2_Activation_Loss.pptx", 21, [2]),
    ("M3T3_Model_Evaluation", "M3T3_Model_Evaluation.pptx", 18, [2]),
]


def para_texts(z, name):
    if name not in z.namelist():
        return []
    root = ET.fromstring(z.read(name))
    out = []
    for p in root.iter(A + "p"):
        t = "".join(r.text or "" for r in p.iter(A + "t")).strip()
        if t:
            out.append(t)
    return out


for tag, pptx, orig_n, drop in JOBS:
    src = os.path.join(OUT, tag + ".pdf")
    if not os.path.exists(src):
        print("MISSING", src)
        continue

    r = PdfReader(src)
    cur = len(r.pages)
    if cur != orig_n:
        print("%-24s 当前 %d 页 ≠ 原始 %d 页 ⇒ 已裁过，跳过裁页" % (tag, cur, orig_n))
        kept = [i for i in range(1, orig_n + 1) if i not in drop]
    else:
        w = PdfWriter()
        kept = []
        for i, page in enumerate(r.pages, 1):
            if i in drop:
                continue
            w.add_page(page)
            kept.append(i)
        with open(src, "wb") as f:
            w.write(f)
        print("%-24s %d → %d 页（剔除 %s）" % (tag, orig_n, len(kept), drop or "无"))

    # ── 抽文本 ──
    buf = []
    if pptx:
        z = zipfile.ZipFile(os.path.join(PPTDIR, pptx))
        slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                        key=lambda s: int(re.findall(r"\d+", s)[0]))
        for new_no, old_no in enumerate(kept, 1):
            body = para_texts(z, slides[old_no - 1])
            notes = para_texts(z, "ppt/notesSlides/notesSlide%d.xml" % old_no)
            notes = [x for x in notes if not x.isdigit()]
            buf.append("=" * 24 + " p%d （原第 %d 页）" % (new_no, old_no) + "=" * 24)
            buf.append("【正文】 " + " | ".join(body))
            if notes:
                buf.append("【备注讲稿】 " + " ".join(notes))
            buf.append("")
    else:
        # T1 只有 PDF，没有备注讲稿；逐页抽文字，并标出纯图页
        rr = PdfReader(src)
        for i, page in enumerate(rr.pages, 1):
            t = " ".join((page.extract_text() or "").split())
            res = page.get("/Resources") or {}
            nimg = 0
            try:
                xo = res.get("/XObject").get_object()
                nimg = len([k for k, v in xo.items()
                            if v.get_object().get("/Subtype") == "/Image"])
            except Exception:
                pass
            buf.append("=" * 24 + " p%d " % i + "=" * 24)
            buf.append("【正文】 " + (t if t else "（抽不到文字）"))
            buf.append("【图】 %d 个" % nimg + ("   ⚠ 纯图页，写讲解时需逐页看图" if len(t) < 20 else ""))
            buf.append("")

    io.open(os.path.join(TXT, tag + ".txt"), "w", encoding="utf-8").write("\n".join(buf))
    print("   → src/%s.txt  (%d 页)" % (tag, len(kept) if pptx else len(PdfReader(src).pages)))
