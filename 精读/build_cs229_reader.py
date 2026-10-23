# -*- coding: utf-8 -*-
"""把 cs229_<name>.py 里的 META / NOTES / QUIZ 组装成 data/<tag>.json，再调 build_reader。

CS229 系列精读的左栏放的是**讲义 PDF**（主讲没有幻灯片，大纲核实过），
所以这个脚本比 make_slides.py 简单：不用转格式、不用裁页，直接把讲义复制进 slides/。

用法：python build_cs229_reader.py PCA [EM ...]
"""
import io, json, os, shutil, sys, importlib, subprocess, random, re

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(HERE, "..", "CS229", "notes")

BOLD = re.compile(r"</?b>")
SEED = 20261012
POSITIONAL = ("以上皆", "以上都", "上述都", "上述皆", "以上全部", "A 和 B", "前两项")


def fix_quiz(q, key, target=None):
    """防泄题：清掉选项里的加粗 + 把正确答案挪到指定位置。

    ⚠ 纯随机打散在题量少时会留下可利用的规律 —— 本份 9 道题第一次跑出来
      A/B/C/D = 0/2/3/4，**一个 A 都没有**，考生能摸出「别选 A」。
      所以改成由调用方**均衡派位**（round-robin + 打乱顺序），这里只负责搬运。
    """
    raw = q["o"]
    opts = [BOLD.sub("", o) for o in raw]
    n = len(opts)
    if target is None or any(p in o for o in opts for p in POSITIONAL):
        target = q["a"]                      # 位置相关选项不动
    # 把正确项搬到 target，其余项按原相对顺序填进剩下的位置
    order = [i for i in range(n) if i != q["a"]]
    random.Random(SEED * 1000 + key).shuffle(order)
    slot = [None] * n
    slot[target] = q["a"]
    for i in [k for k in range(n) if k != target]:
        slot[i] = order.pop(0)
    out = dict(q)
    out["o"] = [opts[i] for i in slot]
    out["a"] = target
    return out, sum(1 for a, b in zip(raw, opts) if a != b)


def build(name):
    mod = importlib.import_module("cs229_" + name)
    META, NOTES, QUIZ = mod.META, mod.NOTES, getattr(mod, "QUIZ", {})

    # 讲义 PDF 复制进 slides/
    src_pdf = os.path.join(NOTES_DIR, os.path.basename(META["pdf"]))
    dst_pdf = os.path.join(HERE, META["pdf"])
    os.makedirs(os.path.dirname(dst_pdf), exist_ok=True)
    if not os.path.exists(src_pdf):
        print("✗ 找不到讲义 %s" % src_pdf); return
    shutil.copyfile(src_pdf, dst_pdf)

    # 页数自检：以 PDF 实际页数为准，META 写错就报出来
    try:
        from pypdf import PdfReader
        real = len(PdfReader(dst_pdf).pages)
        if real != META["pages"]:
            print("  ⚠ META 写的 %d 页，PDF 实际 %d 页，按实际来" % (META["pages"], real))
            META["pages"] = real
    except Exception as e:
        print("  ⚠ 读不出页数：%s" % e)

    # 题目防泄题处理。先按 round-robin 给每道题派一个目标位置，再整体打乱派位序列，
    # 这样既保证 A/B/C/D 大致均衡，又不会形成「ABCDABCD」这种可数的循环。
    flat = [(page, j, q) for page, items in QUIZ.items() for j, q in enumerate(items)]
    targets = [i % 4 for i in range(len(flat))]
    random.Random(SEED).shuffle(targets)

    cleaned, nbold, pos = {}, 0, {}
    for (page, j, q), tgt in zip(flat, targets):
        fq, nb = fix_quiz(q, page * 10 + j, tgt)
        nbold += nb
        pos[fq["a"]] = pos.get(fq["a"], 0) + 1
        cleaned.setdefault(str(page), []).append(fq)

    data = {"tag": META["tag"], "title": META["title"], "sub": META["sub"],
            "pdf": META["pdf"], "pages": META["pages"],
            "notes": NOTES, "quiz": cleaned}
    out = os.path.join(HERE, "data", META["tag"] + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    chars = sum(len(json.dumps(v, ensure_ascii=False)) for n in NOTES for v in n.values())
    nq = sum(len(v) for v in cleaned.values())
    print("data/%s.json：%d 条讲解 / %d 页 / %d 题 / 正文 %d 字（均 %d 字每条）"
          % (META["tag"], len(NOTES), META["pages"], nq, chars, chars // max(len(NOTES), 1)))
    print("  防泄题：清掉加粗 %d 处；答案位置 A/B/C/D = %s"
          % (nbold, "/".join(str(pos.get(i, 0)) for i in range(4))))

    # 覆盖率自检
    covered = set()
    for n in NOTES:
        for p in range(n["r"][0], n["r"][1] + 1):
            covered.add(p)
    miss = [p for p in range(1, META["pages"] + 1) if p not in covered]
    print("  覆盖率 %d/%d%s" % (len(covered), META["pages"],
                                "" if not miss else "  ⚠ 缺页 %s" % miss))
    starts = {n["r"][0] for n in NOTES}
    badk = [k for k in cleaned if int(k) not in starts]
    if badk:
        print("  ⚠ 这些 quiz 键不是任何讲解的起始页，题目不会显示：%s" % badk)

    subprocess.run([sys.executable, os.path.join(HERE, "build_reader.py"), META["tag"]],
                   cwd=HERE)


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["PCA"]):
        build(n)
