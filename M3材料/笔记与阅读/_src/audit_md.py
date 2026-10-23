# -*- coding: utf-8 -*-
"""md2doc 的验收：确认**一个字都没丢**，顺带报页数与结构。

做法：把 markdown 的每一行剥成「纯文字」（去掉 #、>、|、*、`、空白），
再把生成的 HTML 剥成纯文字，逐行检查是否被包含。
⚠ 不能只比总字数——丢一整个表格、或把某行当标题截断，总字数照样接近。
"""
import glob
import io
import os
import re
import sys
import html as H
import subprocess

sys.stdout.reconfigure(encoding="utf-8")
MD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# _{…} ^{…} 会被 mk() 渲染成 <sub>/<sup>，下划线和花括号不会留在文字里
STRIP = re.compile(r"[\s*`>|#\-–—:：、，。；！？（）()\[\]「」『』《》…·.,/\\_{}^]+")


def plain(s):
    # md2doc 会把彩色 emoji ⭐/📌 换成普通字形 ★，两边要按同一口径比
    return STRIP.sub("", s.replace("⭐", "★").replace("📌", "★"))


def html_text(p):
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    return plain(H.unescape(s))


def pages(pdf):
    try:
        raw = io.open(pdf, "rb").read()
        n = raw.count(b"/Type /Page") - raw.count(b"/Type /Pages")
        return n if n > 0 else len(re.findall(rb"/Type\s*/Page[^s]", raw))
    except Exception:
        return 0


BOOKS = {
    "M3T1_神经网络基础_知识点整理": ["M3-00_模块总览与记号表.md",
                                     "M3T1-1_神经网络能学什么_知识点整理.md",
                                     "M3T1-2_计算图与链式法则_知识点整理.md",
                                     "M3T1-3_单个神经元怎么学_知识点整理.md"],
    "M3T2_训练神经网络_知识点整理": ["M3T2-1_激活函数_知识点整理.md",
                                     "M3T2-2_损失函数_知识点整理.md",
                                     "M3T2-3_隐藏层怎么学_知识点整理.md",
                                     "M3T2-4_批量epoch与自动微分_知识点整理.md"],
    "M3T3_模型评估_知识点整理": ["M3T3-1_数据划分与训练证据_知识点整理.md",
                                 "M3T3-2_混淆矩阵与四个指标_知识点整理.md",
                                 "M3T3-3_ROC曲线与AUC_知识点整理.md"],
}

bad = 0
for stem, files in BOOKS.items():
    hp = os.path.join(MD, stem + ".html")
    pp = os.path.join(MD, stem + ".pdf")
    txt = html_text(hp)
    miss, total = [], 0
    for f in files:
        infence = False
        for ln in io.open(os.path.join(MD, f), encoding="utf-8"):
            s = ln.strip()
            if s.startswith("```"):
                infence = not infence
                continue
            if not s or re.fullmatch(r"[-*_]{3,}", s):
                continue
            if re.fullmatch(r"\|[\s:|-]+\|", s):      # 表格分隔行
                continue
            # 有序列表的「1.」由 <ol> 自己编号，不会出现在文字里
            t = plain(re.sub(r"^\d+\.\s+", "", s))
            if len(t) < 2:
                continue
            total += 1
            if t not in txt:
                miss.append((f, s[:72]))
    n = pages(pp)
    sz = os.path.getsize(pp) / 1024 if os.path.exists(pp) else 0
    flag = "✓" if not miss else "✗"
    print("%s %-34s %3d 页  %5.0f KB   行 %d/%d 落地"
          % (flag, stem, n, sz, total - len(miss), total))
    for f, s in miss[:8]:
        print("     丢：%s ｜ %s" % (f, s))
    bad += len(miss)

print("\n合计缺失行：", bad)
