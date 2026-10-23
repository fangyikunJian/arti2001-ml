# -*- coding: utf-8 -*-
"""把题库的正确答案位置重排均匀。

我写题时正确答案天然会堆在 B（先写错项、再写正确那条），实测 50 题里 38 题是 B。
这种规律能被直接利用，所以必须打散。

做法用**洗牌袋**（和放映厅的 quizfix.py 同一套）：每连续 4 题保证 A/B/C/D
各用一次，于是整体极差 ≤ 1，而且不会出现「连着三题都是 C」这种新规律。
重排只是**轮换选项顺序**，不改任何文字；
⚠ 选项里出现「以上都不是」「A 和 B 都对」这类**位置相关**的表述时跳过不动。
"""
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
# ⚠ 只认「引用了选项字母」或「以上/上述」的那种；
#   「两者都不受影响」这类普通措辞**不是**位置相关，照常打散。
POSDEP = re.compile(r"(以上(各项|都|选项)|上述(各项|都|选项)|前两(项|个)|[ABCD]\s*和\s*[ABCD]\s*都|选项\s*[ABCD])")


def _bag(n, seed=20261012):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        b = [0, 1, 2, 3]
        rnd.shuffle(b)
        out += b
    return out[:n]


def balance(groups, seed=20261012):
    """就地重排；返回 (改动题数, 跳过题数)。"""
    total = sum(len(i) for _, i in groups)
    targets = _bag(total, seed)
    t = moved = skipped = 0
    for gi, (title, items) in enumerate(groups):
        for qi, (q, ops, a, why) in enumerate(items):
            want = targets[t]; t += 1
            if any(POSDEP.search(o) for o in ops):
                skipped += 1
                continue
            if want == a:
                continue
            new = list(ops)
            new[a], new[want] = new[want], new[a]      # 只和目标位互换
            items[qi] = (q, new, want, why)
            moved += 1
    return moved, skipped
