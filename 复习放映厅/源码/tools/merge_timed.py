# -*- coding: utf-8 -*-
"""把 `L<n>.txt`（全文、无时间码）和 `L<n>_timed.txt`（约 200 条 [mm:ss] 标记行）
合成一份「**带时间码的全文**」，供写走查式片子时一次读完。

为什么需要（2026-11-03）：
  用户要的是「逐帧字幕讲解」—— 顺着字幕从头走到尾、不跳段。写这种片子必须
  同时看到**全部内容**（在 L<n>.txt 里）和**精确时间码**（在 _timed.txt 里），
  而两边分开读既费劲又容易对错位置。

  ⭐ 关键事实（已用 quote_ts 复核）：`_timed.txt` 里的 [mm:ss] 是**精确**的。
     所以写 says() 时引用被标到的那一句，精确时间码就是白拿的。

⚠ 坑：_timed.txt 的标记文本是**从那个时刻起的字幕原文**，它常常落在句子**中间**
   （例如「[02:14] that makes all this work.」只是某句的后半截），所以不能用
   「句首前缀匹配」去对齐 —— 第一版那么写只对上了 4/191 条。
   正确做法和 quote_ts 一样：把全文拼成一条归一化字符流、记下每个字符属于第几句，
   再把标记文本在流里**顺序向前**定位，把时间码挂到命中位置所在的那一句上。

  用法：
    python tools/merge_timed.py CME295 L1          # 打到标准输出
    python tools/merge_timed.py CME295 L1 --out    # 落盘 transcripts/L1_merged.txt
    python tools/merge_timed.py CME295 L1 --range 200 320   # 只要第 200–320 句
"""
import argparse, io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:/Adelaide COMSC/2026S2/Machine Learning"
NONWORD = re.compile(r"[^a-z0-9]")


def merge(course, tag):
    base = os.path.join(ROOT, course, "transcripts")
    full = io.open(os.path.join(base, "%s.txt" % tag), encoding="utf-8").read().splitlines()
    timed = io.open(os.path.join(base, "%s_timed.txt" % tag), encoding="utf-8").read().splitlines()

    # ① 全文拼成归一化字符流，owner[i] = 第 i 个字符属于哪一行（full 的下标）
    stream, owner = [], []
    for idx, l in enumerate(full):
        if not l.strip() or l.startswith("#"):
            continue
        s = NONWORD.sub("", l.lower())
        stream.append(s)
        owner.extend([idx] * len(s))
    stream = "".join(stream)

    # ② 标记文本在流里顺序定位
    ts_of = {}
    pos = 0
    hit = 0
    marks = []
    for l in timed:
        m = re.match(r"\[(\d+):(\d\d)\]\s*(.*)", l)
        if m:
            marks.append((m.group(1) + ":" + m.group(2), NONWORD.sub("", m.group(3).lower())))
    for ts, key in marks:
        if not key:
            continue
        probe = key[:36]                      # 太长容易因断句差异错过
        j = stream.find(probe, pos)
        if j < 0:                             # 往回找一点，容忍轻微乱序
            j = stream.find(probe, max(0, pos - 400))
        if j < 0:
            continue
        pos = j + len(probe)
        line = owner[j]
        ts_of.setdefault(line, ts)            # 一行上只挂第一个落进来的时间码
        hit += 1

    out, n = [], 0
    for idx, l in enumerate(full):
        if not l.strip() or l.startswith("#"):
            out.append(l)
            continue
        n += 1
        ts = ts_of.get(idx, "")
        out.append("%-8s %4d  %s" % ("[" + ts + "]" if ts else "", n, l))
    return out, n, hit, len(marks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("tag")
    ap.add_argument("--out", action="store_true")
    ap.add_argument("--range", nargs=2, type=int)
    a = ap.parse_args()
    lines, n, hit, total = merge(a.course, a.tag)
    sys.stderr.write("%s %s：%d 句，%d/%d 条时间码挂上了\n" % (a.course, a.tag, n, hit, total))
    if a.range:
        lo, hi = a.range
        keep = []
        for l in lines:
            m = re.match(r"\S*\s+(\d+)\s\s", l)
            if m and lo <= int(m.group(1)) <= hi:
                keep.append(l)
        lines = keep
    text = "\n".join(lines)
    if a.out:
        p = os.path.join(ROOT, a.course, "transcripts", "%s_merged.txt" % a.tag)
        io.open(p, "w", encoding="utf-8").write(text + "\n")
        print("已落盘：" + p)
    else:
        print(text)


if __name__ == "__main__":
    main()
