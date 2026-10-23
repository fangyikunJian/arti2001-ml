# -*- coding: utf-8 -*-
"""Manim 短片 ①：PCA 找主方向 —— 一根轴连续旋转，投影方差实时变化，峰值处即 PC1。
渲染：manim -qh manim_pca_direction.py PCADirection
"""
from manim import *
import numpy as np

BG    = "#080B11"
INK   = "#F0F4FA"
DIM   = "#93A1B5"
BLUE  = "#54A9F7"
GREEN = "#5BDDA8"
YELLO = "#FFD36E"
CORAL = "#FF7C87"
FONT  = "Microsoft YaHei"

# 与放映厅同一朵点云（已中心化）
RAW = np.array([[-2.66, -0.94], [-1.65, -1.16], [-1.19, -0.31], [-0.27, -0.58],
                [0.22, 0.45], [1.10, 0.27], [1.52, 1.21], [2.48, 0.85]])
PTS = RAW - RAW.mean(axis=0)
N = len(PTS)

COV = np.cov(PTS.T, ddof=1)
EVALS, EVECS = np.linalg.eigh(COV)
LAM1 = float(EVALS[-1])
V1 = EVECS[:, -1]
THETA_STAR = float(np.arctan2(V1[1], V1[0]) % np.pi)


def variance_at(theta):
    u = np.array([np.cos(theta), np.sin(theta)])
    return float(np.var(PTS @ u, ddof=1))


VMAX = max(variance_at(t) for t in np.linspace(0, np.pi, 721))
VMIN = min(variance_at(t) for t in np.linspace(0, np.pi, 721))

# ── 布局 ──
O = LEFT * 3.4 + UP * 0.15         # 点云原点
S = 1.05                            # 数据单位 → 场景单位
HALF = 2.9                          # 轴半长（数据单位）

MO = RIGHT * 1.5 + DOWN * 1.9       # 方差曲线坐标原点
MW = 4.3                            # 曲线宽（对应 θ ∈ [0, π]）
MH = 2.6                            # 曲线高（对应 var ∈ [0, VMAX]）


def to_scene(p):
    return O + np.array([p[0] * S, p[1] * S, 0.0])


def meter_point(theta, var):
    return MO + np.array([theta / np.pi * MW, var / VMAX * MH, 0.0])


class PCADirection(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── 开场 ──
        title = Text("PCA 到底在找什么方向？", font=FONT, font_size=44, color=INK)
        sub = Text("一根轴转一圈，看投影散得有多开", font=FONT, font_size=26, color=DIM)
        sub.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.6)

        # ── 点云 ──
        axes_l = VGroup(
            Line(to_scene([-HALF, 0]), to_scene([HALF, 0]), color="#2A3546", stroke_width=2),
            Line(to_scene([0, -1.9]), to_scene([0, 1.9]), color="#2A3546", stroke_width=2),
        )
        dots = VGroup(*[Dot(to_scene(p), radius=0.085, color=BLUE) for p in PTS])
        cap = Text("已中心化的点云：均值在原点", font=FONT, font_size=24, color=DIM)
        cap.next_to(axes_l, UP, buff=0.35)

        self.play(Create(axes_l), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=1.3)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(cap), run_time=0.4)

        # ── 旋转的轴 + 投影 ──
        th = ValueTracker(0.0)

        def u_of():
            t = th.get_value()
            return np.array([np.cos(t), np.sin(t)])

        axis_line = always_redraw(lambda: Line(
            to_scene(-HALF * u_of()), to_scene(HALF * u_of()),
            color=GREEN, stroke_width=4.5))

        feet = always_redraw(lambda: VGroup(*[
            Dot(to_scene((p @ u_of()) * u_of()), radius=0.06, color=GREEN)
            for p in PTS]))

        resid = always_redraw(lambda: VGroup(*[
            Line(to_scene(p), to_scene((p @ u_of()) * u_of()),
                 color=CORAL, stroke_width=1.8, stroke_opacity=0.55)
            for p in PTS]))

        lbl_v = always_redraw(lambda: Text("v", font=FONT, font_size=26, color=GREEN)
                              .move_to(to_scene((HALF + 0.28) * u_of())))

        self.play(Create(axis_line), FadeIn(lbl_v), run_time=0.8)
        # ⚠ 不要对 always_redraw 的组做逐元素动画：那会把「当前这一帧」的副本永久留在场上
        self.add(resid, feet)
        self.wait(0.6)

        # ── 右侧：方差读数 + Var(θ) 曲线 ──
        m_axes = VGroup(
            Line(MO, MO + RIGHT * MW, color="#2A3546", stroke_width=2),
            Line(MO, MO + UP * MH, color="#2A3546", stroke_width=2),
        )
        m_xlab = Text("方向角 θ", font=FONT, font_size=20, color=DIM).next_to(
            MO + RIGHT * MW / 2, DOWN, buff=0.28)
        m_ylab = Text("投影方差", font=FONT, font_size=20, color=DIM).next_to(
            MO + UP * MH, UP, buff=0.18)

        readout = VGroup(
            Text("Var(Xc v) =", font=FONT, font_size=28, color=INK),
            DecimalNumber(variance_at(0), num_decimal_places=3, font_size=34, color=YELLO),
        ).arrange(RIGHT, buff=0.22).move_to(RIGHT * 3.6 + UP * 2.4)
        readout[1].add_updater(lambda m: m.set_value(variance_at(th.get_value())))

        # 已经扫过的角度要留在图上：记录到达过的最大 θ，回摆时曲线不缩回去
        swept = {"max": 0.0}

        def trace_mob():
            swept["max"] = max(swept["max"], th.get_value())
            return VMobject(color=YELLO, stroke_width=4).set_points_smoothly(
                [meter_point(t, variance_at(t))
                 for t in np.linspace(0, max(swept["max"], 1e-3), 120)])

        trace = always_redraw(trace_mob)

        head = always_redraw(lambda: Dot(
            meter_point(th.get_value(), variance_at(th.get_value())), radius=0.07, color=YELLO))

        self.play(Create(m_axes), FadeIn(m_xlab), FadeIn(m_ylab), FadeIn(readout), run_time=0.9)
        self.add(trace, head)

        hint = Text("轴在转 —— 投影时而挤、时而散", font=FONT, font_size=24, color=DIM)
        hint.next_to(axes_l, DOWN, buff=0.55)
        self.play(FadeIn(hint), run_time=0.5)

        # 转一圈（0 → π 即可覆盖所有方向）
        self.play(th.animate.set_value(np.pi), run_time=11, rate_func=linear)
        self.play(FadeOut(hint), run_time=0.4)

        # ── 回到峰值 ──
        peak_note = Text("方差在这个角度达到最大", font=FONT, font_size=24, color=GREEN)
        peak_note.next_to(axes_l, DOWN, buff=0.55)
        self.play(th.animate.set_value(THETA_STAR), run_time=2.2, rate_func=smooth)
        self.play(FadeIn(peak_note), run_time=0.5)

        peak_dot = Dot(meter_point(THETA_STAR, LAM1), radius=0.1, color=GREEN)
        peak_line = DashedLine(meter_point(THETA_STAR, 0), meter_point(THETA_STAR, LAM1),
                               color=GREEN, stroke_width=2, dash_length=0.08)
        self.play(GrowFromCenter(peak_dot), Create(peak_line), run_time=0.8)
        self.wait(0.8)

        # ── 结论 ──
        self.play(FadeOut(peak_note), run_time=0.4)
        concl = VGroup(
            Text("这个方向 = PC1", font=FONT, font_size=30, color=GREEN),
            Text("Σv = λv", font=FONT, font_size=34, color=INK),
            Text("特征向量 = 主方向", font=FONT, font_size=24, color=DIM),
            Text("特征值 λ = 该方向上的投影方差", font=FONT, font_size=24, color=YELLO),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.4 + UP * 0.55)

        lam_txt = Text(f"λ₁ = {LAM1:.3f}", font=FONT, font_size=26, color=YELLO)
        lam_txt.next_to(concl, DOWN, buff=0.4)

        self.play(FadeOut(readout), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in concl], lag_ratio=0.25),
                  run_time=2.0)
        self.play(FadeIn(lam_txt), run_time=0.6)
        self.wait(1.6)

        # ── 对偶视角：方差最大 ⟺ 垂直重构误差最小 ──
        self.play(FadeOut(VGroup(concl, lam_txt, trace, head, peak_dot, peak_line,
                                 m_axes, m_xlab, m_ylab)), run_time=0.8)
        dual = VGroup(
            Text("同一件事的另一种说法：", font=FONT, font_size=26, color=DIM),
            Text("投影方差最大  ⟺  红色垂线的平方和最小", font=FONT, font_size=28, color=INK),
            Text("这就是「PCA 最小化正交重构误差」", font=FONT, font_size=24, color=CORAL),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.2 + UP * 0.3)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in dual], lag_ratio=0.3),
                  run_time=2.0)
        self.wait(2.2)
        self.play(FadeOut(VGroup(dual, axis_line, feet, resid, lbl_v, dots, axes_l)),
                  run_time=1.0)
        self.wait(0.4)
