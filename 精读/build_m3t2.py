# -*- coding: utf-8 -*-
"""把 m3t2_a / m3t2_b / m3t2_quiz 合成 data/M3T2.json。

⚠⚠ 两道防线（见 [[slide-reader]]）：
  ① **扫描选项里有没有 <b>** —— 正确答案被加粗等于直接印出答案
  ② **用固定种子打散每题选项顺序并回写 a** —— 否则答案位置高度集中
     打散按**文本定位**回写，不是按下标，所以多次运行结果一致且正确。

⚠ 种子不是随便填的：在候选里搜出一个让 A/B/C/D 极差 ≤1 的，记在 SEED 旁边。
用法：python build_m3t2.py   （再跑 python build_reader.py M3T2）
"""
import io
import json
import os
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from m3t2_a import PART_A          # noqa: E402
from m3t2_b import PART_B          # noqa: E402
from m3t2_quiz import QUIZ         # noqa: E402

NOTES = PART_A + PART_B
PAGES = 20

# ── 自检 ① 逐页覆盖、无重叠、无越界 ──
covered = {}
for n in NOTES:
    a, b = n["r"]
    assert 1 <= a <= b <= PAGES, "页码越界: %s" % (n["r"],)
    for p in range(a, b + 1):
        assert p not in covered, "第 %d 页被两条 note 覆盖" % p
        covered[p] = n["t"]
missing = [p for p in range(1, PAGES + 1) if p not in covered]
assert not missing, "这些页没有讲解: %s" % missing
print("✓ 覆盖自检：%d 页全覆盖、无重叠" % PAGES)

# ── 自检 ② quiz 的键必须是某条 note 的起始页 ──
starts = {n["r"][0] for n in NOTES}
bad = [k for k in QUIZ if k not in starts]
assert not bad, "这些 quiz 键不是任何 note 的起始页，题会不显示: %s" % bad
print("✓ quiz 键自检：%d 条全部落在 note 起始页上" % len(QUIZ))

# ── 自检 ③ 选项里不许有 <b>（泄题）──
leak = []
for k, qs in QUIZ.items():
    for i, q in enumerate(qs):
        assert len(q["o"]) == 4, "p%s 第%d题选项不是 4 个" % (k, i + 1)
        assert 0 <= q["a"] < 4, "p%s 第%d题答案下标越界" % (k, i + 1)
        for o in q["o"]:
            if "<b>" in o or "<strong>" in o:
                leak.append("p%s 第%d题: %s" % (k, i + 1, o[:30]))
assert not leak, "选项里有加粗，等于印出答案：\n  " + "\n  ".join(leak)
print("✓ 泄题自检：选项中加粗 0 处")

# ── 自检 ④ 位置相关选项（打散会破坏它们）──
# ⚠ 「都对」后面要排除「应」：「所有梯度都对应同一次前向」不是位置相关选项，
#   不加这个否定前瞻会每次都误报一条。
POSREL = re.compile(r"以上皆|以上都|A\s*和\s*B|都对(?!应)|都不对|上述")
sus = []
for k, qs in QUIZ.items():
    for q in qs:
        for o in q["o"]:
            if POSREL.search(o):
                sus.append("p%s: %s" % (k, o[:30]))
if sus:
    print("⚠ 疑似位置相关选项，打散前请人工确认：")
    for s in sus:
        print("   ", s)
else:
    print("✓ 位置相关选项：无")


# ── 选种子：要让 A/B/C/D 极差 ≤1 ──
def spread(seed):
    rnd = random.Random(seed)
    cnt = {c: 0 for c in "ABCD"}
    for k in sorted(QUIZ):
        for q in QUIZ[k]:
            opts = list(q["o"])
            right = opts[q["a"]]
            rnd.shuffle(opts)
            cnt["ABCD"[opts.index(right)]] += 1
    v = [cnt[c] for c in "ABCD"]
    return max(v) - min(v), v


SEED = None
for cand in range(20261100, 20261500):
    d, v = spread(cand)
    if d <= 1:
        SEED = cand
        break
assert SEED, "400 个候选里没找到极差 ≤1 的种子"
print("✓ 种子 %d：打散后分布 %s" % (SEED, spread(SEED)[1]))

# ── 打散：固定种子，按文本定位回写 a ──
rnd = random.Random(SEED)
before, after = {c: 0 for c in "ABCD"}, {c: 0 for c in "ABCD"}
total = 0
for k in sorted(QUIZ):
    for q in QUIZ[k]:
        total += 1
        before["ABCD"[q["a"]]] += 1
        right = q["o"][q["a"]]
        opts = list(q["o"])
        rnd.shuffle(opts)
        q["o"] = opts
        q["a"] = opts.index(right)          # 按文本定位，不是按下标
        after["ABCD"[q["a"]]] += 1

print("✓ 打散：%d 题　答案位置 %s → %s"
      % (total,
         "/".join(str(before[c]) for c in "ABCD"),
         "/".join(str(after[c]) for c in "ABCD")))

DATA = {
    "tag": "M3T2",
    "title": "训练神经网络：激活、损失、隐藏层梯度与实现",
    "sub": "M3 T2",
    "pdf": "slides/M3T2_Activation_Loss.pdf",
    "pages": PAGES,
    "notes": NOTES,
    "quiz": {str(k): v for k, v in sorted(QUIZ.items())},
}

os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
out = os.path.join(HERE, "data", "M3T2.json")
io.open(out, "w", encoding="utf-8").write(
    json.dumps(DATA, ensure_ascii=False, indent=1))


# ── 规模统计（对照 M1 自制笔记的密度标准：每页 ≥1200 字）──
def wc(n):
    s = ""
    for key in ("one", "quote", "eq", "say", "exam"):
        s += str(n.get(key, "") or "")
    for p in n.get("pts", []):
        s += p
    for t in n.get("tbl", []):
        s += t.get("cap", "") + "".join(t.get("head", []))
        for row in t.get("rows", []):
            s += "".join(row)
    tip = n.get("tip")
    if tip:
        s += tip.get("t", "") + tip.get("v", "")
    return len(re.sub(r"<[^>]+>", "", s))


lens = [(n["r"], wc(n)) for n in NOTES]
tot = sum(x for _, x in lens)
print("\n写入 data/M3T2.json")
print("  条目 %d · 总字数 %d · 每页平均 %.0f 字" % (len(NOTES), tot, tot / float(PAGES)))
print("  题目 %d 道，分布在 %d 页" % (total, len(QUIZ)))
thin = [(r, x) for r, x in lens if x < 1000]
if thin:
    print("  ⚠ 这些条目偏薄（<1000 字）：%s"
          % ["p%d:%d" % (r[0], x) for r, x in thin])
