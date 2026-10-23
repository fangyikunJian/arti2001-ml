# -*- coding: utf-8 -*-
"""Manim 短片 ③：DBSCAN 的密度判定
   —— ε 窗口逐点扫过去，数邻居（含自己！），分出核心 / 边界 / 噪声。
渲染：python -m manim -qh --disable_caching manim_dbscan_density.py DBScanDensity
"""
from manim import *
import numpy as np

BG    = "#080B11"
INK   = "#F0F4FA"
DIM   = "#93A1B5"
GRID  = "#2A3546"
BLUE  = "#54A9F7"
GREEN = "#5BDDA8"
YELLO = "#FFD36E"
CORAL = "#FF7C87"
PURP  = "#B48BF5"
FONT  = "Microsoft YaHei"

# 一维算例，和 M2 T2 那一集用的是同一组数
NAMES = ["A", "B", "C", "D", "E"]
POS   = np.array([0.0, 0.5, 1.0, 3.0, 3.4])
EPS, MINPTS = 0.6, 3

# ── 判定（先算清楚，动画只是把算出来的东西演出来）──
NB   = [[j for j in range(5) if abs(POS[i] - POS[j]) <= EPS] for i in range(5)]
CORE = [i for i in range(5) if len(NB[i]) >= MINPTS]
BORD = [i for i in range(5) if i not in CORE and any(c in NB[i] for c in CORE)]
NOIS = [i for i in range(5) if i not in CORE and i not in BORD]
assert CORE == [1] and BORD == [0, 2] and NOIS == [3, 4], (CORE, BORD, NOIS)

# ── 布局 ──
LY = 1.52                       # 数轴的高度
SX = 2.5                        # 数据单位 → 场景单位
HDR_Y, ROW_Y, ROW_DY = -0.72, -1.24, -0.5
COL = [-4.35, -2.45, 0.35, 2.55]         # 点 / 邻域 / 个数 / 判定 四列的 x


def X(v):
    return (v - 1.7) * SX


def at(v, y=LY):
    return np.array([X(v), y, 0.0])


class DBScanDensity(Scene):
    def construct(self):
        self.camera.background_color = BG
        HEAD = {"m": None}

        def say(txt, color=INK, size=30):
            new = Text(txt, font=FONT, font_size=size, color=color).move_to(UP * 3.42)
            if HEAD["m"] is not None:
                self.play(FadeOut(HEAD["m"], shift=UP * 0.2), run_time=0.3)
            self.play(FadeIn(new, shift=DOWN * 0.2), run_time=0.4)
            HEAD["m"] = new

        # ── 开场 ──
        title = Text("DBSCAN：密度说了算", font=FONT, font_size=46, color=INK)
        sub = Text("不用先说要几个簇，但要说清「多挤才算挤」", font=FONT, font_size=26, color=DIM)
        sub.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.6)

        # ── 数轴与五个点 ──
        line = Line(at(-0.45), at(3.85), color=GRID, stroke_width=2)
        ticks, dots, tags, vals = VGroup(), VGroup(), VGroup(), VGroup()
        for i, v in enumerate(POS):
            ticks.add(Line(at(v) + DOWN * 0.1, at(v) + UP * 0.1, color=GRID, stroke_width=2))
            dots.add(Dot(at(v), radius=0.11, color=DIM))
            tags.add(Text(NAMES[i], font=FONT, font_size=27, color=INK).move_to(at(v, LY + 0.46)))
            vals.add(Text("%.1f" % v, font=FONT, font_size=20, color=DIM).move_to(at(v, LY - 0.42)))
        self.play(Create(line), Create(ticks), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=1.1)
        self.play(FadeIn(tags), FadeIn(vals), run_time=0.6)
        say("五个点排在一条线上：A B C 挨着，D E 在远处", DIM, 27)
        self.wait(1.4)

        # ── 参数 ──
        par = VGroup(
            Text("ε = 0.6", font=FONT, font_size=30, color=YELLO),
            Text("MinPts = 3", font=FONT, font_size=30, color=YELLO),
        ).arrange(RIGHT, buff=1.0).move_to(UP * 2.62)
        say("两个参数：看多远（ε），要多少个（MinPts）", YELLO, 28)
        self.play(FadeIn(par, shift=DOWN * 0.15), run_time=0.8)
        self.wait(1.3)

        # ── 表头 ──
        hdr = VGroup(
            Text("点", font=FONT, font_size=22, color=DIM).move_to([COL[0], HDR_Y, 0]),
            Text("ε 邻域", font=FONT, font_size=22, color=DIM).move_to([COL[1], HDR_Y, 0]),
            Text("有几个", font=FONT, font_size=22, color=DIM).move_to([COL[2], HDR_Y, 0]),
            Text("判定", font=FONT, font_size=22, color=DIM).move_to([COL[3], HDR_Y, 0]),
        )
        rule = Line([COL[0] - 0.55, HDR_Y - 0.26, 0], [COL[3] + 1.15, HDR_Y - 0.26, 0],
                    color=GRID, stroke_width=2)

        # ── ε 窗口逐点扫过去 ──
        win = Rectangle(width=2 * EPS * SX, height=1.55,
                        color=YELLO, stroke_width=2.5, stroke_opacity=0.7,
                        fill_color=YELLO, fill_opacity=0.10).move_to(at(POS[0]))
        win.set_z_index(-1)
        say("把一个宽 2ε 的窗口套在每个点上，数窗口里有几个点", INK, 27)
        self.play(FadeIn(win), run_time=0.6)
        self.play(FadeIn(hdr), Create(rule), run_time=0.6)

        for i in range(5):
            y = ROW_Y + i * ROW_DY
            if i:
                self.play(win.animate.move_to(at(POS[i])), run_time=0.85)
            inside = NB[i]
            is_core = len(inside) >= MINPTS
            # 窗口里的点亮一下
            pulse = [Flash(dots[j], color=YELLO, line_length=0.14, flash_radius=0.28,
                           num_lines=10, run_time=0.5) for j in inside]
            self.play(*pulse)

            col = GREEN if is_core else DIM
            row = VGroup(
                Text(NAMES[i], font=FONT, font_size=25, color=INK).move_to([COL[0], y, 0]),
                Text("{%s}" % ", ".join(NAMES[j] for j in inside),
                     font=FONT, font_size=24, color=INK).move_to([COL[1], y, 0]),
                Text("%d %s 3" % (len(inside), "≥" if is_core else "<"),
                     font=FONT, font_size=24, color=col).move_to([COL[2], y, 0]),
                Text("核心点 ✓" if is_core else "不是核心",
                     font=FONT, font_size=24, color=col).move_to([COL[3], y, 0]),
            )
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.5)

            if i == 0:      # 第一个点就把「含自己」这件事挑明
                warn = Text("⚠ 窗口里的 A 就是它自己 —— 自己也要数进去",
                            font=FONT, font_size=24, color=YELLO).move_to(UP * 0.34)
                self.play(FadeIn(warn), run_time=0.5)
                self.wait(2.0)
                self.play(FadeOut(warn), run_time=0.4)
            elif is_core:
                self.play(dots[i].animate.set_color(GREEN).scale(1.5), run_time=0.5)
                self.wait(1.1)
            else:
                self.wait(0.7)

        self.play(FadeOut(win), run_time=0.4)
        say("五个点里，只有 B 够得上核心点", GREEN, 30)
        self.wait(1.5)

        # ── 边界点 ──
        say("A 和 C 自己不够密，但它们落在核心 B 的 ε 里", BLUE, 27)
        reach = VGroup(*[Arrow(at(POS[1], LY + 0.95), at(POS[j], LY + 0.28),
                               color=BLUE, stroke_width=3, buff=0.05,
                               max_tip_length_to_length_ratio=0.22) for j in BORD])
        self.play(LaggedStart(*[GrowArrow(a) for a in reach], lag_ratio=0.25), run_time=1.0)
        self.play(*[dots[j].animate.set_color(BLUE) for j in BORD], run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(Text("⇒ 边界点：跟着核心进簇，但自己不往外扩",
                              font=FONT, font_size=25, color=BLUE).move_to(UP * 0.34)),
                  run_time=0.6)
        self.wait(2.0)

        # ── 噪声 ──
        say("D 和 E 呢？它俩互相是邻居 —— 可是也就两个", CORAL, 27)
        self.play(*[dots[j].animate.set_color(CORAL) for j in NOIS], run_time=0.6)
        marks = VGroup(*[Text("×", font=FONT, font_size=34, color=CORAL)
                         .move_to(at(POS[j], LY + 0.46)) for j in NOIS])
        self.play(*[FadeOut(tags[j]) for j in NOIS], FadeIn(marks), run_time=0.6)
        self.wait(1.7)
        say("两个够不着 MinPts，身边又没有核心点 ⇒ 噪声", CORAL, 27)
        self.wait(2.0)

        # ── 结果 ──
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not HEAD["m"]])),
                  run_time=0.8)
        res = VGroup(
            Text("一个簇：{ A, B, C }", font=FONT, font_size=38, color=GREEN),
            Text("噪声：{ D, E }", font=FONT, font_size=34, color=CORAL),
        ).arrange(DOWN, buff=0.42).move_to(UP * 1.35)
        say("结果", INK, 32)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in res], lag_ratio=0.35),
                  run_time=1.6)
        self.wait(1.8)

        tail = VGroup(
            Text("和 k-means 比：不用事先定 k，还能把噪声单独拎出来",
                 font=FONT, font_size=26, color=INK),
            Text("簇也不必是圆的 —— 沿着密度连起来，形状随便",
                 font=FONT, font_size=26, color=BLUE),
            Text("代价是 ε 和 MinPts 得自己调；密度不均匀时，一套参数难兼顾",
                 font=FONT, font_size=25, color=YELLO),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 1.55)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in tail], lag_ratio=0.3),
                  run_time=2.2)
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.3)
