# -*- coding: utf-8 -*-
"""（课件已移至 M2材料/课件/）① 把三份官方课件（PPT 本体）裁成「只剩学习内容」的 PDF，放进 精读/slides/
   ② 同时把每页的正文 + 备注讲稿抽成文本，供写逐页讲解用。
剔除：原住民致辞页、空白页。分节页保留（带章节名）。
"""
import io, os, re, sys, zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader, PdfWriter

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"G:\Adelaide COMSC\2026S2\Machine Learning"
HERE = os.path.join(BASE, "精读")
OUT = os.path.join(HERE, "slides")
TXT = os.path.join(HERE, "src")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TXT, exist_ok=True)

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

JOBS = [
    ("M2T1_PCA", "M2T1_PCA.pptx", [2, 20]),
    ("M2T2_Clustering", "M2T2_Clustering.pptx", [2]),
    ("M2T3_GMM", "M2T3_GMM.pptx", [2]),
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


for tag, pptx, drop in JOBS:
    # ── 裁页 ──
    src = os.path.join(OUT, tag + ".pdf")
    if not os.path.exists(src):
        print("MISSING", src)
        continue
    r = PdfReader(src)
    w = PdfWriter()
    kept = []
    for i, page in enumerate(r.pages, 1):
        if i in drop:
            continue
        w.add_page(page)
        kept.append(i)
    with open(src, "wb") as f:   # 原地覆盖
        w.write(f)

    # ── 抽正文 + 备注（按裁页后的新页码编号）──
    z = zipfile.ZipFile(os.path.join(BASE, "M2材料", "课件", pptx))
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda s: int(re.findall(r"\d+", s)[0]))
    buf = []
    for new_no, old_no in enumerate(kept, 1):
        body = para_texts(z, slides[old_no - 1])
        notes = para_texts(z, "ppt/notesSlides/notesSlide%d.xml" % old_no)
        notes = [x for x in notes if not x.isdigit()]
        buf.append("=" * 24 + " p%d （原第 %d 页）" % (new_no, old_no) + "=" * 24)
        buf.append("【正文】 " + " | ".join(body))
        if notes:
            buf.append("【备注讲稿】 " + " ".join(notes))
        buf.append("")
    io.open(os.path.join(TXT, tag + ".txt"), "w", encoding="utf-8").write("\n".join(buf))

    print("%-20s %d -> %d 页（剔除 %s）；正文+讲稿已写入 src/%s.txt"
          % (tag, len(r.pages), len(kept), drop, tag))
