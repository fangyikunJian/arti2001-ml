# -*- coding: utf-8 -*-
"""Patch CS229 讲座片的字幕可读性，base64 编码，供 hub 以 srcdoc 内嵌。"""
import io, re, base64, json, os

TR = r"C:/Users/donot/.claude/projects/G--Adelaide-COMSC-2026S2-Machine-Learning/ace97a38-4e9e-4f48-a9db-e29cb077bcfd/tool-results"
FILES = {
 "l2":"artifact-9d00034c-1788364593-cadc.html",
 "l3":"artifact-179bf910-1788446564-2996.html",
 "l67":"artifact-9f7332b5-1788446574-35b8.html",
 "l8":"artifact-69ebcf8b-1788446577-0902.html",
}

NARR_CSS = ('#narr{margin:.7em 0 0;max-width:min(90ch,100%);text-align:left;'
 'font-size:clamp(12.5px,1.12vw,16px);font-weight:400;line-height:1.72;color:#D9E1ED;'
 'background:rgba(8,11,17,.86);border:1px solid rgba(46,58,82,.7);border-radius:12px;'
 'padding:12px 17px;box-shadow:0 8px 30px rgba(0,0,0,.5);opacity:1}')

re_narr_fn = re.compile(r'narrEl\.classList\.add\("off"\);\s*setTimeout\(function\(\)\{\s*narrEl\.innerHTML=t;\s*narrEl\.classList\.remove\("off"\);\s*\},1\d0\);')
re_cap_fn  = re.compile(r'cap\.classList\.add\("off"\);\s*setTimeout\(function\(\)\{\s*cap\.innerHTML=h;\s*cap\.classList\.remove\("off"\);\s*\},1\d0\);')
re_narr_css = re.compile(r'#narr\{[^}]*\}')
re_capwrap  = re.compile(r'(#capWrap\{[^}]*?)\}')   # 让字幕块盖在渐变兜底之上，别被压暗

out = {}
for k, fn in FILES.items():
    s = io.open(os.path.join(TR, fn), encoding="utf-8").read()
    n1 = len(re_narr_fn.findall(s)); s = re_narr_fn.sub('narrEl.innerHTML=t;narrEl.classList.remove("off");', s)
    n2 = len(re_cap_fn.findall(s));  s = re_cap_fn.sub('cap.innerHTML=h;cap.classList.remove("off");', s)
    n3 = len(re_narr_css.findall(s)); s = re_narr_css.sub(NARR_CSS, s, count=1)
    n4 = 1 if re_capwrap.search(s) else 0
    s = re_capwrap.sub(lambda m: m.group(1)+';position:relative;z-index:2}', s, count=1)
    # 讲解面板更高、不再裁掉长讲解（L3/L67/L8 有 38vh 上限；L2 本就无上限）
    s = s.replace('max-height:38vh;overflow-y:auto;margin-bottom:58px', 'max-height:62vh;overflow-y:auto;margin-bottom:50px')
    assert n1>=1 and n2>=1 and n3>=1 and n4>=1, (k, n1, n2, n3, n4)
    out[k] = base64.b64encode(s.encode("utf-8")).decode("ascii")
    print(k, "patched setNarr=%d setCap=%d narrCSS=%d capWrap=%d  b64=%dKB" % (n1, n2, n3, n4, len(out[k])//1024))

io.open("cs_docs.json","w",encoding="utf-8").write(json.dumps(out))
print("cs_docs.json written, total", sum(len(v) for v in out.values())//1024, "KB base64")
