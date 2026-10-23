# -*- coding: utf-8 -*-
"""把 CCP 那套上发现的两处修复回补到本文件夹的全部 HTML。可重复运行（幂等）。

修复 A · charset
    这些 HTML 都以 <title> 开头、没有 <meta charset>。在线 artifact 正常是因为
    外壳补了 charset；本地双击打开时浏览器按系统编码猜，中文就变乱码。
    → 在文件最前面补 <meta charset="utf-8"> 和 viewport。

修复 B · 面板残留（CSS 版，对所有引擎变体都成立）
    setCap/setBig/setEq/setTitle 靠 .off 类把 opacity 过渡到 0 来隐藏。
    页面被切到后台时 CSS 过渡会停在中途 —— 实测 class 已经是 off、computed
    opacity 仍是 0.96，于是上一镜的大字半透明残留、压在当前镜内容上。
    → 给 .off 加 visibility:hidden。visibility 不参与过渡，所以加上 .off 的
      那一刻就真的看不见了；去掉 .off 时 opacity 淡入照旧（淡出变成立即消失，
      这是刻意的取舍）。用 visibility 而不是 display:none，是因为 flip() 要
      靠 getBoundingClientRect 量位置，display:none 会把它量成 0。

修复 C · 总结卡/测验卡可能卡在看不见（只有标准引擎有这个模式）
    showSum/askQ 先加 .off 再用 setTimeout(50~60ms) 去掉它。后台标签页里
    setTimeout 会被节流，卡片就停在 opacity 0 → 整张总结卡看不见。
    → 改成 hidden=false → 强制 reflow → 同步去掉 .off，不再依赖定时器。

改之前会把原文件整份拷到 _备份-修复前/。
"""
import base64, io, json, os, re, shutil, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 复习放映厅/
BACKUP = os.path.join(ROOT, "_备份-修复前")

META = ('<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n')

MARKER = "/* fix: 面板 .off 立即不可见 */"
OFF_CSS = (MARKER + "\n"
           "#big.off,#cap.off,#eqBox.off,#titleBox.off,#sum.off,#quiz.off{visibility:hidden}\n")

RE_SUM = re.compile(
    r'sumEl\.hidden=false;\s*if\(FAST\)\{sumEl\.classList\.remove\("off"\);return;\}\s*'
    r'sumEl\.classList\.add\("off"\);setTimeout\(function\(\)\{sumEl\.classList\.remove\("off"\);\},\d+\);')
RE_QUIZ = re.compile(
    r'quizEl\.hidden=false;setTimeout\(function\(\)\{quizEl\.classList\.remove\("off"\);\},\d+\);')


def patch_text(s, want_meta=True):
    """对一份 HTML（或 eng.txt）正文套用三处修复，返回 (新文本, 应用了哪几项)。"""
    done = []

    if want_meta and "charset" not in s[:600].lower():
        s = META + s
        done.append("A:charset")

    if "</style>" in s and MARKER not in s:
        s = s.replace("</style>", OFF_CSS + "</style>", 1)
        done.append("B:off-css")

    n = 0
    s, k = RE_SUM.subn('sumEl.hidden=false;void sumEl.offsetWidth;sumEl.classList.remove("off");', s)
    n += k
    s, k = RE_QUIZ.subn('quizEl.hidden=false;void quizEl.offsetWidth;quizEl.classList.remove("off");', s)
    n += k
    if n:
        done.append("C:sync-show(%d)" % n)

    return s, done


def backup(path):
    rel = os.path.relpath(path, ROOT)
    dst = os.path.join(BACKUP, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(path, dst)


def main():
    targets = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html"):
            targets.append(os.path.join(ROOT, name))
    films = os.path.join(ROOT, "影片")
    for name in sorted(os.listdir(films)):
        if name.endswith(".html"):
            targets.append(os.path.join(films, name))
    targets.append(os.path.join(ROOT, "源码", "eng.txt"))

    print("%-44s %s" % ("file", "applied"))
    print("-" * 78)
    for path in targets:
        s = io.open(path, encoding="utf-8").read()
        # eng.txt 是模板头，同样需要 meta（它是每部片子的开头）
        new, done = patch_text(s, want_meta=True)
        if done:
            backup(path)
            io.open(path, "w", encoding="utf-8").write(new)
        print("%-44s %s" % (os.path.relpath(path, ROOT), ", ".join(done) or "(已是最新)"))

    # ── 内嵌的 CS229 讲座片（base64 srcdoc）──────────────────────────
    cs_path = os.path.join(ROOT, "源码", "cs_docs.json")
    hub_path = os.path.join(ROOT, "★放映厅-总入口.html")
    if os.path.exists(cs_path):
        docs = json.loads(io.open(cs_path, encoding="utf-8").read())
        changed = {}
        for k, b64 in docs.items():
            inner = base64.b64decode(b64).decode("utf-8")
            new_inner, done = patch_text(inner, want_meta=True)
            if done:
                docs[k] = base64.b64encode(new_inner.encode("utf-8")).decode("ascii")
                changed[k] = done
        if changed:
            backup(cs_path)
            new_json = json.dumps(docs, ensure_ascii=False)
            io.open(cs_path, "w", encoding="utf-8").write(new_json)
            # 同步写回 hub 里内嵌的那份
            hub = io.open(hub_path, encoding="utf-8").read()
            m = re.search(r'var CSDOC=(\{.*?\});', hub, re.S)
            if m:
                backup(hub_path)
                hub = hub[:m.start(1)] + new_json + hub[m.end(1):]
                io.open(hub_path, "w", encoding="utf-8").write(hub)
                print("\nhub 内嵌 CSDOC 已同步重写")
            else:
                print("\n⚠ 在 hub 里没找到 var CSDOC={...};，内嵌片未同步")
        for k, done in changed.items():
            print("  cs_docs[%s]: %s" % (k, ", ".join(done)))
        if not changed:
            print("\ncs_docs.json: (已是最新)")

    print("\n备份在: %s" % BACKUP)


if __name__ == "__main__":
    main()
