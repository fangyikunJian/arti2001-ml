# -*- coding: utf-8 -*-
"""题库的防泄题自检。

两条规则来自做放映厅测验时踩过的坑：
  1. **选项里不能出现粗体**（`**…**`）—— 正确答案往往是内容最充实的那一条，
     一加粗就等于把答案指出来了。
  2. **答案位置要均衡** —— A/B/C/D 四个位置的出现次数极差应 ≤ 1，
     否则「总选 B」之类的规律能被直接利用。
"""
import collections
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BOLD = re.compile(r"\*\*.+?\*\*", re.S)


def audit(name, groups):
    """groups = [(组标题, [(题干, [4 选项], 答案下标, 解析), ...]), ...]"""
    pos = collections.Counter()
    leaks, bad = [], []
    n = 0
    for title, items in groups:
        for q, ops, a, why in items:
            n += 1
            pos["ABCD"[a]] += 1
            if len(ops) != 4:
                bad.append("%s：选项不是 4 个 —— %s" % (title, q[:28]))
            if not (0 <= a < len(ops)):
                bad.append("%s：答案下标越界 —— %s" % (title, q[:28]))
            for o in ops:
                if BOLD.search(o):
                    leaks.append("%s：选项里有粗体 —— %s" % (title, o[:36]))
            # 正确答案明显比别的长很多，也是一种泄题
            L = [len(o) for o in ops]
            if L[a] > 1.9 * (sum(L) - L[a]) / 3 and L[a] - max(L[:a] + L[a + 1:]) > 12:
                leaks.append("%s：正确答案比其它选项长太多 —— %s" % (title, q[:30]))
    c = [pos[k] for k in "ABCD"]
    spread = max(c) - min(c)
    print("【%s】%d 组 / %d 题　答案位置 A/B/C/D = %d/%d/%d/%d　极差 %d %s"
          % (name, len(groups), n, c[0], c[1], c[2], c[3], spread,
             "✓" if spread <= 1 else "✗ 需要调整"))
    for m in leaks:
        print("   ⚠ 泄题风险：", m)
    for m in bad:
        print("   ✗ 结构错误：", m)
    return spread <= 1 and not leaks and not bad
