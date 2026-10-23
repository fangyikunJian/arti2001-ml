# -*- coding: utf-8 -*-
"""放映厅选择题的防泄题处理：① 选项里不许出现加粗 ② 正确答案位置打散。

⚠ 2026-09-28：逐页精读里犯过一次（50 题全加粗、48 题答案在 B，用户当场发现）。
放映厅的片子当时没查，结果一模一样地中招（T1 24/24 加粗、23/24 在 B；T2 22/22 全中）。
两条防线合并在这里，build_*.py 的 KP() 统一调用。

⚠ 2026-10-04 第二次改进：**纯随机打散在题量少时照样会漏出规律**。
   做 L4 时 7 道题跑出 A/B/C/D = 2/3/**0**/2 —— 一个 C 都没有，考生能摸出「别选 C」。
   改成**洗牌袋派位**：位置 0..n-1 装进一个袋子打乱，每题取一个，袋空了再装满重打乱。
   于是**每连续 n 道题，n 个位置各出现恰好一次**，结构上不可能出现空洞。
   （精读那边的 build_cs229_reader.py 用的是 round-robin + 整体打乱，同一思路。）
"""
import random, re

BOLD = re.compile(r"</?b>")
SEED = 20261012

# 位置相关的选项（「以上皆是」之类）打散会变得不通，命中就保持原序并报告
POSITIONAL = ("以上皆", "以上都", "上述都", "上述皆", "以上全部", "A 和 B", "A、B 都", "前两项")

_report = {"bold": 0, "skipped": [], "pos": {}}
_bags = {}      # 每种「选项个数」各有一个洗牌袋
_refills = {}   # 各自补过几次 —— 让每次补袋顺序不同，但仍可复现


def _next_target(n):
    """从洗牌袋里取一个目标位置；袋空了就重新装满并打乱。"""
    bag = _bags.get(n)
    if not bag:
        k = _refills.get(n, 0)
        _refills[n] = k + 1
        bag = list(range(n))
        random.Random(SEED * 1000 + n * 7919 + k).shuffle(bag)
        _bags[n] = bag
    return bag.pop()


def fix_quiz(q, key):
    """返回处理后的 quiz 副本；key（知识点序号）用来生成稳定的每题种子。"""
    raw = q["o"]
    opts = [BOLD.sub("", o) for o in raw]
    _report["bold"] += sum(1 for a, b in zip(raw, opts) if a != b)
    n = len(opts)

    out = dict(q)
    if any(p in o for o in opts for p in POSITIONAL):
        _report["skipped"].append(key)          # 位置相关：保持原序
        out["o"] = opts
        out["a"] = q["a"]
    else:
        tgt = _next_target(n)
        # 正确项搬到 tgt，其余项按打乱后的相对顺序填进剩下的位置
        order = [i for i in range(n) if i != q["a"]]
        random.Random(SEED * 1000 + key).shuffle(order)
        slot = [None] * n
        slot[tgt] = q["a"]
        for i in range(n):
            if i != tgt:
                slot[i] = order.pop(0)
        out["o"] = [opts[i] for i in slot]      # 按下标搬运，重复文本也不会搬错
        out["a"] = tgt

    _report["pos"][out["a"]] = _report["pos"].get(out["a"], 0) + 1
    return out


def report():
    d = _report["pos"]
    tot = sum(d.values())
    worst = max(d.get(i, 0) for i in range(4)) if tot else 0
    best = min(d.get(i, 0) for i in range(4)) if tot else 0
    flag = "" if tot == 0 or worst - best <= 1 else "  ⚠ 分布不均"
    return "防泄题：清掉加粗 %d 处；答案位置 A/B/C/D = %s；未打散（位置相关选项）%s%s" % (
        _report["bold"],
        "/".join(str(d.get(i, 0)) for i in range(4)),
        _report["skipped"] or "无",
        flag,
    )
