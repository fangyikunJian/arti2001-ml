# -*- coding: utf-8 -*-
"""Manim 短片 ④：EM 的软分配
   —— 同一个点不是「归谁」，而是按比例分给两个高斯；一轮 E+M 下来，对数似然必然上升。
渲染：python -m manim -qh --disable_caching manim_em_soft.py EMSoft
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

# ── 算例：两个点、两个一维高斯，初始左右对称（和 M2 T3 那一集同一组数）──
XS   = np.array([-1.0, 1.0])
MU0  = np.array([-1.0, 1.0])
VAR0 = np.array([1.0, 1.0])
PI0  = np.array([0.5, 0.5])


def pdf(x, m, v):
    return np.exp(-(x - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)


def loglik(mu, var, pi):
    return float(np.sum(np.log(np.sum(pi * pdf(XS[:, None], mu, var), axis=1))))


W  = PI0 * pdf(XS[:, None], MU0, VAR0)       # 加权密度 π_k · N(x | μ_k, σ_k²)
R  = W / W.sum(1, keepdims=True)             # E 步：责任度
NK = R.sum(0)
MU1  = (R * XS[:, None]).sum(0) / NK         # M 步
VAR1 = (R * (XS[:, None] - MU1) ** 2).sum(0) / NK
PI1  = NK / len(XS)
LL0, LL1 = loglik(MU0, VAR0, PI0), loglik(MU1, VAR1, PI1)

assert abs(R[0, 0] - 0.880797) < 1e-5 and abs(MU1[0] + 0.761594) < 1e-5
assert abs(VAR1[0] - 0.419974) < 1e-5 and LL1 > LL0
assert abs(LL0 + 2.9703) < 1e-3 and abs(LL1 + 2.4394) < 1e-3

# ── 布局 ──
SX, SY, Y0 = 1.833, 8.0, -0.55        # x 缩放 / 密度缩放 / 基线高度
BAR_Y, BAR_W, BAR_H = -2.05, 6.0, 0.5


def px(x, dens=0.0):
    return np.array([x * SX, Y0 + dens * SY, 0.0])


def curve(mu, var, pi, color, lo=-3.25, hi=3.25, n=160):
    return VMobject(color=color, stroke_width=4.5).set_points_smoothly(
        [px(x, pi * pdf(x, mu, var)) for x in np.linspace(lo, hi, n)])


def bar(r1, cols=(BLUE, GREEN)):
    """左右两段拼成一条，宽度就是两边的比例"""
    left, g = -BAR_W / 2, VGroup()
    for frac, c in ((r1, cols[0]), (1 - r1, cols[1])):
        if frac < 1e-6:
            continue
        seg = Rectangle(width=BAR_W * frac, height=BAR_H, stroke_width=0,
                        fill_color=c, fill_opacity=0.88)
        seg.move_to([left + BAR_W * frac / 2, BAR_Y, 0])
        left += BAR_W * frac
        g.add(seg)
    return g


class EMSoft(Scene):
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
        title = Text("EM：不逼它二选一", font=FONT, font_size=46, color=INK)
        sub = Text("一个点可以 88% 属于这边、12% 属于那边", font=FONT, font_size=26, color=DIM)
        sub.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.6)

        # ── 数轴与两个点 ──
        axis = Line(px(-3.4), px(3.4), color=GRID, stroke_width=2)
        pts = VGroup(*[Dot(px(x), radius=0.12, color=YELLO) for x in XS])
        plab = VGroup(*[Text("x = %s1" % ("−" if x < 0 else "+"),
                             font=FONT, font_size=24, color=YELLO)
                        .move_to(px(x) + DOWN * 0.42) for x in XS])
        self.play(Create(axis), run_time=0.6)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in pts], lag_ratio=0.2), run_time=0.8)
        self.play(FadeIn(plab), run_time=0.5)
        say("就两个数据点：−1 和 +1", DIM, 28)
        self.wait(1.2)

        # ── 两个高斯 ──
        c1 = curve(MU0[0], VAR0[0], PI0[0], BLUE)
        c2 = curve(MU0[1], VAR0[1], PI0[1], GREEN)
        par = VGroup(
            Text("μ₁ = −1", font=FONT, font_size=24, color=BLUE),
            Text("μ₂ = +1", font=FONT, font_size=24, color=GREEN),
            Text("σ² = 1    π = 0.5", font=FONT, font_size=24, color=DIM),
        ).arrange(RIGHT, buff=0.85).move_to(UP * 2.6)
        say("我们猜了两个高斯，左右对称摆着", INK, 28)
        self.play(Create(c1), Create(c2), run_time=1.3)
        self.play(FadeIn(par), run_time=0.6)
        self.wait(1.3)

        # ── 先看 k-means 会怎么做 ──
        say("k-means 会问：x = −1 到底归谁？", DIM, 29)
        hard = bar(1.0, (BLUE, GREEN))
        hcap = Text("硬分配：100% 给左边，0% 给右边", font=FONT, font_size=25, color=DIM)
        hcap.move_to([0, BAR_Y + 0.62, 0])
        self.play(FadeIn(hcap), FadeIn(hard), run_time=0.8)
        self.wait(1.6)

        # ── E 步：量两条曲线在 x=−1 处的高度 ──
        say("EM 换个问法：两边各占多少？", YELLO, 30)
        x0 = XS[0]
        h = [PI0[k] * pdf(x0, MU0[k], VAR0[k]) for k in range(2)]
        stems = VGroup(
            DashedLine(px(x0), px(x0, h[0]), color=BLUE, stroke_width=3, dash_length=0.1),
            DashedLine(px(x0), px(x0, h[1]), color=GREEN, stroke_width=3, dash_length=0.1))
        hv = VGroup(
            Text("%.4f" % h[0], font=FONT, font_size=23, color=BLUE)
            .move_to(px(x0, h[0]) + LEFT * 0.78),
            Text("%.4f" % h[1], font=FONT, font_size=23, color=GREEN)
            .move_to(px(x0, h[1]) + RIGHT * 0.98 + UP * 0.2))
        self.play(FadeOut(hcap), FadeOut(hard), run_time=0.4)
        self.play(Create(stems), run_time=0.9)
        self.play(FadeIn(hv), run_time=0.6)
        say("在 x = −1 处，量一下两条曲线各有多高", INK, 28)
        self.wait(1.6)

        # ── 归一化成责任度 ──
        say("两个高度一归一化，就是责任度 r", YELLO, 30)
        soft = bar(R[0, 0], (BLUE, GREEN))
        scap = Text("软分配：按高度的比例来分", font=FONT, font_size=25, color=YELLO)
        scap.move_to([0, BAR_Y + 0.62, 0])
        snum = VGroup(
            # 写在蓝条里面，所以要用深色，不然蓝字压蓝底看不见
            Text("%.1f%%" % (100 * R[0, 0]), font=FONT, font_size=28, color=BG)
            .move_to([-BAR_W / 2 + BAR_W * R[0, 0] / 2, BAR_Y, 0]),
            Text("%.1f%%" % (100 * R[0, 1]), font=FONT, font_size=24, color=INK)
            .move_to([BAR_W / 2 - BAR_W * R[0, 1] / 2, BAR_Y - 0.62, 0]))
        self.play(FadeIn(scap), FadeIn(soft), run_time=0.8)
        self.play(FadeIn(snum), run_time=0.6)
        self.wait(1.8)
        say("那 12% 不是零 —— 右边那个高斯也分到了一点", GREEN, 27)
        self.wait(1.9)

        # ── M 步 ──
        self.play(FadeOut(VGroup(stems, hv, scap, soft, snum)), run_time=0.6)
        say("M 步：拿这些比例当权重，重算 μ 和 σ²", INK, 29)
        calc = VGroup(
            Text("μ₁ = [ 0.881×(−1) + 0.119×(+1) ] ÷ 1 = −0.7616",
                 font=FONT, font_size=26, color=BLUE),
            Text("σ₁² = 0.4200    （比原来的 1 窄了一大截）",
                 font=FONT, font_size=26, color=YELLO),
        ).arrange(DOWN, buff=0.34).move_to([0, BAR_Y - 0.1, 0])
        self.play(FadeIn(calc[0], shift=UP * 0.15), run_time=0.9)
        self.wait(1.5)
        self.play(FadeIn(calc[1], shift=UP * 0.15), run_time=0.7)
        self.wait(1.3)

        n1 = curve(MU1[0], VAR1[0], PI1[0], BLUE)
        n2 = curve(MU1[1], VAR1[1], PI1[1], GREEN)
        npar = VGroup(
            Text("μ₁ = −0.76", font=FONT, font_size=24, color=BLUE),
            Text("μ₂ = +0.76", font=FONT, font_size=24, color=GREEN),
            Text("σ² = 0.42    π = 0.5", font=FONT, font_size=24, color=DIM),
        ).arrange(RIGHT, buff=0.85).move_to(UP * 2.6)
        say("两个高斯各自朝自己负责的点靠过去，也变瘦了", INK, 27)
        self.play(Transform(c1, n1), Transform(c2, n2),
                  Transform(par, npar), run_time=2.0)
        self.wait(1.4)

        # ── 对数似然 ──
        self.play(FadeOut(calc), run_time=0.5)
        ll = VGroup(
            Text("对数似然 ℓ", font=FONT, font_size=26, color=DIM),
            # 数字里的负号用真正的减号，和上面的 μ₁ = −0.76 对齐
            Text(("%.4f" % LL0).replace("-", "−"), font=FONT, font_size=34, color=DIM),
            Text("→", font=FONT, font_size=30, color=YELLO),
            Text(("%.4f" % LL1).replace("-", "−"), font=FONT, font_size=34, color=GREEN),
            Text("升了", font=FONT, font_size=26, color=GREEN),
        ).arrange(RIGHT, buff=0.45).move_to([0, BAR_Y - 0.15, 0])
        say("这一轮没白走", GREEN, 30)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in ll], lag_ratio=0.25),
                  run_time=1.8)
        self.wait(2.2)

        # ── 结论 ──
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not HEAD["m"]])),
                  run_time=0.8)
        say("两步轮流，各管一半", INK, 32)
        concl = VGroup(
            Text("E 步：参数先按住不动，算每个点的责任度 r",
                 font=FONT, font_size=28, color=BLUE),
            Text("M 步：责任度按住不动，用加权平均更新 μ、σ²、π",
                 font=FONT, font_size=28, color=GREEN),
            Text("每走一轮，ℓ 一定不下降 —— 所以它会收敛",
                 font=FONT, font_size=28, color=YELLO),
            Text("但和 k-means 一样，收敛到的可能只是局部最优",
                 font=FONT, font_size=26, color=CORAL),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.1)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in concl], lag_ratio=0.3),
                  run_time=2.6)
        self.wait(3.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.3)
