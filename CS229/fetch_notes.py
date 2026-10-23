# -*- coding: utf-8 -*-
"""把 CS229 (2018 秋) 大纲上挂的全部讲义 PDF 下到 CS229/notes/。

⚠ 先说清楚一件事：**CS229 的 20 节主讲没有幻灯片**，Ng 全程白板。
   大纲 Materials 栏挂的全是 Class Notes（讲义 PDF）；带 [slides] 的只有讨论课
   （Probability / Python / Evaluation Metrics / 对 ML 的批评）与 Andrew 的 ML-advice。
   所以「CS229 的课件」实际就是这些 PDF —— 逐页精读的左栏放的也是它们。

⚠ 旧路径 cs229.stanford.edu/notes/cs229-notesN.pdf 有一部分已经 404
   （会返回一个约 200 字节的错误页，不是 PDF），所以每个文件都试多个镜像，
   并且**按「是不是真 PDF + 大小合理」验收**，不只看 HTTP 200。

用法：
    python fetch_notes.py           # 下载缺的
    python fetch_notes.py --check   # 只校验已有文件，不联网
    python fetch_notes.py --force   # 全部重下
"""
import io, os, sys, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "notes")

UA = {"User-Agent": "Mozilla/5.0 (compatible; study-notes-fetch/1.0)"}

# (本地文件名, 大纲上的相对路径, 一句话说明)
# 路径里的目录决定了镜像怎么拼：notes/ · section/ · extra-notes/ · materials/
NOTES = [
    # ── 主线讲义（按大纲顺序）──
    ("cs229-notes1.pdf",            "notes/cs229-notes1.pdf",            "监督学习与判别式算法（线性回归、逻辑回归、GLM）"),
    ("cs229-notes2.pdf",            "notes/cs229-notes2.pdf",            "生成式算法（GDA、朴素贝叶斯）"),
    ("cs229-notes3.pdf",            "notes/cs229-notes3.pdf",            "支持向量机与核方法"),
    ("cs229-notes4.pdf",            "notes/cs229-notes4.pdf",            "学习理论"),
    ("cs229-notes5.pdf",            "notes/cs229-notes5.pdf",            "正则化与模型选择"),
    ("cs229-notes6.pdf",            "notes/cs229-notes6.pdf",            "在线学习与感知机（选读）"),
    ("cs229-notes7a.pdf",           "notes/cs229-notes7a.pdf",           "无监督学习：k-means"),
    ("cs229-notes7b.pdf",           "notes/cs229-notes7b.pdf",           "混合高斯"),
    ("cs229-notes8.pdf",            "notes/cs229-notes8.pdf",            "EM 算法"),
    ("cs229-notes9.pdf",            "notes/cs229-notes9.pdf",            "因子分析"),
    ("cs229-notes10.pdf",           "notes/cs229-notes10.pdf",           "主成分分析 PCA"),
    ("cs229-notes11.pdf",           "notes/cs229-notes11.pdf",           "独立成分分析 ICA"),
    ("cs229-notes12.pdf",           "notes/cs229-notes12.pdf",           "强化学习与控制"),
    ("cs229-notes13.pdf",           "notes/cs229-notes13.pdf",           "LQR、DDP 与 LQG"),
    # ⚠ 2026-10-01 实测：决策树与集成方法的讲义已从 CS229 站点下架（/notes/ 整个目录 404，
    #   各年份镜像也都没有），而且 main_notes.pdf 的现代课纲里也删掉了这两章。
    #   对应的 L9 本来就不在 ARTI2001 考纲内，不影响。
    ("cs229-notes-deep_learning.pdf", "notes/cs229-notes-deep_learning.pdf", "深度学习"),
    # ⚠ 单独的 backprop 讲义也下架了，但 **main_notes.pdf §7.4（99–113 页）就是反向传播**，
    #   内容更新更全，M3 用那个即可。
    # ── 讨论课 / 复习讲义 ──
    ("cs229-linalg.pdf",            "section/cs229-linalg.pdf",          "线性代数复习"),
    ("cs229-prob.pdf",              "section/cs229-prob.pdf",            "概率论复习"),
    ("cs229-cvxopt.pdf",            "section/cs229-cvxopt.pdf",          "凸优化概览 I"),
    ("cs229-cvxopt2.pdf",           "section/cs229-cvxopt2.pdf",         "凸优化概览 II"),
    ("cs229-hmm.pdf",               "section/cs229-hmm.pdf",             "隐马尔可夫模型"),
    ("gaussians.pdf",               "section/gaussians.pdf",             "多元高斯分布"),
    ("more_on_gaussians.pdf",       "section/more_on_gaussians.pdf",     "高斯分布进阶"),
    ("cs229-gaussian_processes.pdf", "section/cs229-gaussian_processes.pdf", "高斯过程"),
    ("error-analysis.pdf",          "section/error-analysis.pdf",        "偏差方差权衡与误差分析"),
    # ── 补充讲义 ──
    ("loss-functions.pdf",          "extra-notes/loss-functions.pdf",    "±1 标签下的二分类"),
    ("boosting.pdf",                "extra-notes/boosting.pdf",          "Boosting 与弱学习"),
    ("representer-function.pdf",    "extra-notes/representer-function.pdf", "表示定理"),
    ("hoeffding.pdf",               "extra-notes/hoeffding.pdf",         "Hoeffding 不等式"),
    # ── 幻灯片（只有讨论课才有）──
    ("_slides_probability.pdf",     "section/cs229-prob-slide.pdf",      "讨论课幻灯：概率"),
    ("_slides_evaluation_metrics.pdf", "section/evaluation_metrics_spring2020.pdf", "讨论课幻灯：评估指标"),
    ("ML-advice.pdf",               "materials/ML-advice.pdf",           "Ng：如何让 ML 算法在实践中跑起来"),
]

# 镜像前缀，按顺序试
MIRRORS = [
    "https://cs229.stanford.edu/",
    "http://cs229.stanford.edu/",
    "https://cs229.stanford.edu/summer2019/",   # 旧 /notes/ 404 时这里常常还在
    "https://cs229.stanford.edu/notes2020spring/",  # 2026-10 实测：notes6/13 只有这里还有
]


def looks_like_pdf(path):
    """真 PDF 要以 %PDF 开头且不能太小（404 页通常只有几百字节）。"""
    try:
        if os.path.getsize(path) < 8000:
            return False, "太小（%d 字节），多半是 404 页" % os.path.getsize(path)
        with open(path, "rb") as f:
            if f.read(4) != b"%PDF":
                return False, "不是 PDF（开头不是 %PDF）"
        return True, ""
    except OSError as e:
        return False, str(e)


def candidates(rel):
    """给一个大纲相对路径，生成所有要试的完整 URL。"""
    out = []
    base = os.path.basename(rel)
    for m in MIRRORS:
        # 年份镜像（summer2019 / notes2020spring）是**平铺**的，没有 notes/ section/ 子目录；
        # 只有主站保留原来的目录结构。搞混会让每个文件都 404。
        if "summer2019/" in m or "notes2020spring/" in m:
            out.append(m + base)
        else:
            out.append(m + rel)
    return out


def grab(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    os.makedirs(OUT, exist_ok=True)
    check_only = "--check" in sys.argv
    force = "--force" in sys.argv

    ok = bad = skipped = 0
    failures = []
    for name, rel, desc in NOTES:
        dest = os.path.join(OUT, name)
        if os.path.exists(dest) and not force:
            good, why = looks_like_pdf(dest)
            if good:
                skipped += 1
                continue
            print("  ⚠ 已存在但不合格（%s），重下：%s" % (why, name))
        if check_only:
            if not os.path.exists(dest):
                print("  ✗ 缺失：%-34s %s" % (name, desc))
                bad += 1
            continue

        got = False
        for url in candidates(rel):
            try:
                grab(url, dest)
            except Exception:
                continue
            good, why = looks_like_pdf(dest)
            if good:
                print("  ✓ %-34s %7.0fKB  %s" % (name, os.path.getsize(dest) / 1024, desc))
                ok += 1
                got = True
                break
            else:
                try:
                    os.remove(dest)
                except OSError:
                    pass
        if not got:
            print("  ✗ %-34s 所有镜像都拿不到  %s" % (name, desc))
            failures.append((name, desc))
            bad += 1
        time.sleep(0.3)

    print("\n新下载 %d · 已有跳过 %d · 失败 %d" % (ok, skipped, bad))
    if failures:
        print("拿不到的：")
        for n, d in failures:
            print("   -", n, "|", d)


if __name__ == "__main__":
    main()
