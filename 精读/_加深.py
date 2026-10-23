# -*- coding: utf-8 -*-
"""把 deepen_<tag>.py 里的加厚内容并进 data/<tag>.json。

用法：python _加深.py M2T1 [M2T2 M2T3]
幂等：同一条重跑不会叠加（字段是整体覆盖，不是追加）。
合并后打印每页字数，用来和「M1材料/笔记与阅读」那套笔记的 ~1814 字/页 对标。
"""
import io, json, sys, importlib, os

sys.stdout.reconfigure(encoding="utf-8")

# 整体覆盖的字段（新值直接替换旧值）
OVERRIDE = ("t", "one", "quote", "eq", "pts", "tbl", "say", "ng", "exam", "tip", "star")


def chars(note):
    return sum(len(json.dumps(v, ensure_ascii=False)) for v in note.values())


def run(tag):
    path = "data/%s.json" % tag
    if not os.path.exists(path):
        print("✗ 找不到", path); return
    # 三批内容依次合并，后一批覆盖前一批的同名字段：
    #   deepen_<tag>  主体加厚
    #   fill_<tag>    后来补的 say/ng 空栏
    #   tutans_<tag>  ⭐ 官方 Tutorial/Practical 答案发布后补的（2026-10-07 起）——
    #                 这批是**一手材料**，所以放最后、优先级最高
    DATA = {}
    loaded = []
    for prefix in ("deepen_", "fill_", "tutans_"):
        mod_name = prefix + tag
        if not os.path.exists(mod_name + ".py"):
            continue
        if mod_name in sys.modules:
            mod = importlib.reload(sys.modules[mod_name])
        else:
            mod = importlib.import_module(mod_name)
        for page, fields in mod.DATA.items():
            DATA.setdefault(page, {}).update(fields)   # 后一批覆盖前一批的同名字段
        loaded.append(mod_name)
    if not DATA:
        print("✗ 找不到 deepen_%s.py / fill_%s.py，跳过" % (tag, tag)); return

    d = json.load(io.open(path, encoding="utf-8"))
    notes = d["notes"]
    by_start = {}
    for n in notes:
        by_start.setdefault(n["r"][0], n)

    before = sum(chars(n) for n in notes)
    touched, missing = 0, []
    for page, fields in DATA.items():
        n = by_start.get(page)
        if n is None:
            missing.append(page); continue
        for k, v in fields.items():
            if k in OVERRIDE:
                n[k] = v
            else:
                print("  ⚠ 未知字段 %s（第 %d 页），已忽略" % (k, page))
        touched += 1
    after = sum(chars(n) for n in notes)

    json.dump(d, io.open(path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    per = [(n["r"][0], chars(n)) for n in notes]
    thin = [p for p, c in per if c < 1200]
    print("\n═══ %s ═══" % tag)
    print("  加厚 %d/%d 页%s" % (touched, len(notes),
          ("；⚠ 这些页码在数据里不存在：%s" % missing) if missing else ""))
    print("  正文 %d → %d 字（%+d，×%.2f）" % (before, after, after - before,
          after / max(before, 1)))
    print("  每页平均 %d 字   对标：M1 那套笔记 ~1814 字/页" % (after // max(len(notes), 1)))
    print("  字段覆盖：" + "  ".join(
        "%s %d/%d" % (k, sum(1 for n in notes if k in n), len(notes))
        for k in ("quote", "tbl", "eq", "pts", "say", "ng", "exam", "tip")))
    if thin:
        print("  ⚠ 仍不足 1200 字的页：%s" % thin)
    else:
        print("  ✓ 每一页都在 1200 字以上")


if __name__ == "__main__":
    tags = sys.argv[1:] or ["M2T1", "M2T2", "M2T3"]
    for t in tags:
        run(t)
