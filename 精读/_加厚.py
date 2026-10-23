# -*- coding: utf-8 -*-
"""给逐页精读加厚：每页补「与考试的联系」栏、补要点、重要页加题。
用法：python _加厚.py M2T1
数据放在 enrich_<tag>.py 里，键是页码。merge 是幂等的：同一条不会重复追加。
"""
import importlib, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def merge(tag):
    mod = importlib.import_module("enrich_" + tag)
    p = os.path.join(HERE, "data", tag + ".json")
    d = json.load(io.open(p, encoding="utf-8"))
    notes = {n["r"][0]: n for n in d["notes"]}

    added_pts = added_exam = added_q = 0
    for page, e in mod.DATA.items():
        n = notes.get(page)
        if n is None:
            print("  ⚠ 没有第 %s 页的笔记，跳过" % page)
            continue
        if "exam" in e:
            if not n.get("exam"):
                added_exam += 1
            n["exam"] = e["exam"]
        for extra in e.get("pts", []):
            if extra not in n.setdefault("pts", []):
                n["pts"].append(extra)
                added_pts += 1
        if "say" in e:
            n["say"] = (n.get("say", "") + " " + e["say"]).strip() if e.get("append") else e["say"]
        if "tip" in e:
            n["tip"] = e["tip"]
        for q in e.get("quiz", []):
            lst = d["quiz"].setdefault(str(page), [])
            if not any(x["q"] == q["q"] for x in lst):
                lst.append(q)
                added_q += 1

    # ⚠ 打散正确答案的位置：写题时手容易一直放同一个位置，那本身就是泄题
    import random
    rng = random.Random(20261012)
    for k in sorted(d["quiz"], key=lambda x: int(x)):
        for q in d["quiz"][k]:
            correct = q["o"][q["a"]]
            idx = list(range(len(q["o"])))
            rng.shuffle(idx)
            q["o"] = [q["o"][i] for i in idx]
            q["a"] = q["o"].index(correct)

    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))

    total_q = sum(len(v) for v in d["quiz"].values())
    withexam = sum(1 for n in d["notes"] if n.get("exam"))
    print("%s：新增 %d 条要点、%d 个考试联系栏、%d 道题" % (tag, added_pts, added_exam, added_q))
    print("  现在：%d 页，%d 页有考试联系栏，共 %d 道题（平均 %.1f 题/页）"
          % (len(d["notes"]), withexam, total_q, total_q / len(d["notes"])))
    # 泄题复查
    leak = [q["q"][:24] for v in d["quiz"].values() for q in v if any("<b>" in o for o in q["o"])]
    print("  选项加粗泄题：%s" % (leak if leak else "无 ✓"))
    # 答案分布（别让正确答案总落在同一个位置）
    from collections import Counter
    dist = Counter(q["a"] for v in d["quiz"].values() for q in v)
    print("  正确答案位置分布：%s" % dict(sorted(dist.items())))


if __name__ == "__main__":
    for t in (sys.argv[1:] or ["M2T1"]):
        merge(t)
