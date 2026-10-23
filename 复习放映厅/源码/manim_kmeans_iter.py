# -*- coding: utf-8 -*-
"""Manim 短片 ②：k-means 的两步交替
   —— 分配、更新、J 只降不升；末尾用同一份数据换一个初始，落进更差的局部最优。
渲染：python -m manim -qh --disable_caching manim_kmeans_iter.py KMeansIter
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

CL = [BLUE, GREEN, PURP]            # 三个簇各自的颜色

# 三团点，坐标风格沿用 M2 T2 那一集
X = np.array([[-2.6, 1.4], [-2.0, 1.9], [-2.9, 1.9],        # 左上团
              [2.0, -1.2], [2.6, -1.7], [2.1, -2.0],        # 右下团
              [-0.3, -2.5], [0.4, -2.9], [-0.8, -2.9]])     # 正下团
K = 3
MU_GOOD = np.array([[-1.0, -3.0], [0.0, -3.0], [1.0, -3.0]])   # 三个挤在下方
MU_BAD  = np.array([[-2.9, 1.9], [-2.3, 1.4], [0.9, -2.2]])    # 两个落进同一团


def kmeans(mu0, maxit=10):
    """返回 [(分配, 旧质心, 新质心, J分配后, J更新后), ...]"""
    mu, hist = np.array(mu0, float), []
    for _ in range(maxit):
        d = ((X[:, None, :] - mu[None, :, :]) ** 2).sum(-1)
        c = d.argmin(1)                                      # 分配步
        Ja = float(((X - mu[c]) ** 2).sum())
        nm = np.array([X[c == k].mean(0) if (c == k).any() else mu[k]
                       for k in range(K)])                   # 更新步
        Ju = float(((X - nm[c]) ** 2).sum())
        hist.append((c.copy(), mu.copy(), nm.copy(), Ja, Ju))
        if np.allclose(nm, mu):
            break
        mu = nm
    return hist


HG, HB = kmeans(MU_GOOD), kmeans(MU_BAD)
JSEQ = [j for h in HG for j in (h[3], h[4])]                 # 每个半步一个 J
assert all(a >= b - 1e-9 for a, b in zip(JSEQ, JSEQ[1:])), "J 必须单调不增"
assert abs(HG[-1][4] - 1.9533) < 1e-3 and abs(HB[-1][4] - 12.7250) < 1e-3
JMAX = JSEQ[0]
NP = 2 * len(HG) - 1          # 真正会画到图上的 J 个数（最后一轮只画分配那半步）

# ── 布局 ──
O, S = LEFT * 3.55 + UP * 0.25, 1.02          # 点云原点 / 数据单位→场景单位
MO = RIGHT * 1.35 + DOWN * 2.45               # J 折线图的原点
MW, MH = 4.6, 3.35                            # 折线图的宽 / J 映射到的高
PADX = 0.5                                    # 第一个点离纵轴留一点空


def sc(p):
    return O + np.array([p[0] * S, p[1] * S, 0.0])


def jpt(i, j):
    return MO + np.array([PADX + i / (NP - 1) * (MW - PADX), j / JMAX * MH, 0.0])


def cross(p, color, size=0.19, w=6.5):
    """质心画成一个叉，组的中心正好落在 sc(p)，所以可以直接 move_to 搬家"""
    a = np.array([size, size, 0.0])
    b = np.array([size, -size, 0.0])
    return VGroup(Line(sc(p) - a, sc(p) + a, color=color, stroke_width=w),
                  Line(sc(p) - b, sc(p) + b, color=color, stroke_width=w))


class KMeansIter(Scene):
    def construct(self):
        self.camera.background_color = BG
        HEAD = {"m": None}

        def say(txt, color=INK, size=30):
            """顶部那行话。先把旧的收干净再放新的，别让两句字叠在一起"""
            new = Text(txt, font=FONT, font_size=size, color=color).move_to(UP * 3.42)
            if HEAD["m"] is not None:
                self.play(FadeOut(HEAD["m"], shift=UP * 0.2), run_time=0.3)
            self.play(FadeIn(new, shift=DOWN * 0.2), run_time=0.4)
            HEAD["m"] = new

        # ── 开场 ──
        title = Text("k-means：两步交替，J 只降不升", font=FONT, font_size=44, color=INK)
        sub = Text("看它怎么从一组糟糕的质心走到分好的簇", font=FONT, font_size=26, color=DIM)
        sub.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, sub)), run_time=0.6)

        # ── 点云 ──
        frame = VGroup(
            Line(sc([-3.3, 0]), sc([3.1, 0]), color=GRID, stroke_width=2),
            Line(sc([0, -3.4]), sc([0, 2.4]), color=GRID, stroke_width=2))
        dots = VGroup(*[Dot(sc(p), radius=0.09, color=DIM) for p in X])
        self.play(Create(frame), run_time=0.7)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.07),
                  run_time=1.2)
        say("9 个点，我们要它分成 K = 3 个簇", DIM, 28)
        self.wait(1.2)

        # ── 初始质心 ──
        crs = VGroup(*[cross(MU_GOOD[k], CL[k]) for k in range(K)])
        say("初始质心随便放 —— 三个都挤在下面", YELLO, 28)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in crs], lag_ratio=0.2),
                  run_time=1.0)
        self.wait(1.1)

        # ── 右侧 J 折线图（纵轴画得比数据顶端高一截，免得标签压在轴上）──
        ax = VGroup(Line(MO, MO + RIGHT * MW, color=GRID, stroke_width=2),
                    Line(MO, MO + UP * (MH + 0.75), color=GRID, stroke_width=2))
        ylab = Text("J", font=FONT, font_size=26, color=YELLO).move_to(
            MO + UP * (MH + 0.75) + LEFT * 0.3)
        xlab = Text("每半步一次", font=FONT, font_size=20, color=DIM).next_to(
            MO + RIGHT * MW / 2, DOWN, buff=0.26)
        chart = VGroup(ax, ylab, xlab)
        jart = VGroup()                     # 折线上陆续长出来的点、线、数字
        jdef = Text("J = 每个点到自己质心的平方距离，全部加起来",
                    font=FONT, font_size=23, color=DIM).move_to(DOWN * 3.62)
        self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), run_time=0.8)
        self.play(FadeIn(jdef), run_time=0.6)
        self.wait(0.9)

        jshown = []

        def push_J(j, color):
            i = len(jshown)
            d = Dot(jpt(i, j), radius=0.075, color=color)
            lbl = Text("%.2f" % j, font=FONT, font_size=21, color=color)
            lbl.next_to(d, UP, buff=0.14)           # 一律朝上，下面留给横轴说明
            anims = [GrowFromCenter(d), FadeIn(lbl)]
            if jshown:
                seg = Line(jpt(i - 1, jshown[-1]), jpt(i, j), color=color, stroke_width=3)
                anims.insert(0, Create(seg))
                jart.add(seg)
            jart.add(d, lbl)
            self.play(*anims, run_time=0.55)
            jshown.append(j)

        # ── 三轮交替 ──
        for rnd, (c, mu_old, mu_new, Ja, Ju) in enumerate(HG, 1):
            last = (rnd == len(HG))

            # ① 分配步
            if last:
                say("再分配一次 —— 每个点的归属都没变", GREEN, 29)
            else:
                say("① 分配：每个点归给离它最近的质心", INK, 30)
            legs = VGroup(*[Line(sc(X[i]), sc(mu_old[c[i]]), color=CL[c[i]],
                                 stroke_width=2, stroke_opacity=0.5)
                            for i in range(len(X))])
            self.play(LaggedStart(*[Create(l) for l in legs], lag_ratio=0.05), run_time=1.0)
            self.play(*[dots[i].animate.set_color(CL[c[i]]) for i in range(len(X))],
                      run_time=0.7)
            push_J(Ja, YELLO)
            if rnd == 2:
                ring = Circle(radius=0.26, color=YELLO, stroke_width=3).move_to(dots[8])
                note = Text("只有这一个点换了簇", font=FONT, font_size=23, color=YELLO)
                note.next_to(ring, RIGHT, buff=0.25)
                self.play(FadeIn(note), Create(ring), run_time=0.6)
                self.wait(1.2)
                self.play(FadeOut(note), FadeOut(ring), run_time=0.4)
            else:
                self.wait(0.9)

            if last:
                self.play(FadeOut(legs), run_time=0.5)
                break

            # ② 更新步
            say("② 更新：质心搬到自己那一簇的重心", INK, 30)
            self.play(FadeOut(legs), run_time=0.4)
            self.play(*[crs[k].animate.move_to(sc(mu_new[k])) for k in range(K)],
                      run_time=1.3)
            push_J(Ju, GREEN)
            self.wait(0.8)

        say("分配不再变化 ⇒ 停下来", GREEN, 32)
        self.wait(1.5)

        # ── 结论：清场，整屏讲 ──
        self.play(FadeOut(jdef), FadeOut(chart), FadeOut(jart),
                  FadeOut(frame), FadeOut(dots), FadeOut(crs), run_time=0.8)
        concl = VGroup(
            Text("两个半步各自都让 J 不增", font=FONT, font_size=34, color=INK),
            Text("分配步：每个点改选最近的质心 —— 不可能让 J 变大",
                 font=FONT, font_size=26, color=BLUE),
            Text("更新步：重心正是「平方距离和」最小的那个点",
                 font=FONT, font_size=26, color=GREEN),
            Text("分配方式只有有限种，J 又一路不增 ⇒ 一定会停",
                 font=FONT, font_size=28, color=YELLO),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.15)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in concl], lag_ratio=0.3),
                  run_time=2.4)
        self.wait(2.6)
        self.play(FadeOut(concl), run_time=0.6)

        # ── 尾声：同一份数据，换一组初始 ──
        say("但停在哪儿，要看初始质心", CORAL, 32)
        for k in range(K):
            crs[k].move_to(sc(MU_BAD[k]))
        for d in dots:
            d.set_color(DIM)
        self.play(FadeIn(frame), FadeIn(dots), FadeIn(crs), run_time=0.9)
        say("同一份数据，换一组初始质心", YELLO, 30)
        self.wait(1.1)

        cB, muB = HB[-1][0], HB[-1][2]
        self.play(*[crs[k].animate.move_to(sc(muB[k])) for k in range(K)],
                  *[dots[i].animate.set_color(CL[cB[i]]) for i in range(len(X))],
                  run_time=1.4)
        legsB = VGroup(*[Line(sc(X[i]), sc(muB[cB[i]]), color=CL[cB[i]],
                              stroke_width=2, stroke_opacity=0.5) for i in range(len(X))])
        self.play(LaggedStart(*[Create(l) for l in legsB], lag_ratio=0.05), run_time=0.9)
        say("它也停了 —— 可左上那团被劈成了两半", CORAL, 28)
        self.wait(1.6)

        cmp = VGroup(
            VGroup(Text("刚才那次", font=FONT, font_size=23, color=DIM),
                   Text("J = 1.95", font=FONT, font_size=36, color=GREEN)
                   ).arrange(RIGHT, buff=0.3),
            Text("↓  足足 6.5 倍", font=FONT, font_size=24, color=YELLO),
            VGroup(Text("这一次", font=FONT, font_size=23, color=DIM),
                   Text("J = 12.73", font=FONT, font_size=36, color=CORAL)
                   ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.6 + UP * 1.5)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in cmp], lag_ratio=0.3),
                  run_time=1.8)
        self.wait(1.8)

        tail = VGroup(
            Text("两次都「收敛」了", font=FONT, font_size=26, color=INK),
            Text("只是收敛到了不同的局部最优", font=FONT, font_size=26, color=INK),
            Text("J 不保证全局最小 —— 换几组初始多跑几次，", font=FONT, font_size=23, color=YELLO),
            Text("取 J 最小的那一次", font=FONT, font_size=23, color=YELLO),
            Text("或者用 k-means++：让初始质心互相离得远",
                 font=FONT, font_size=23, color=GREEN),
        ).arrange(DOWN, buff=0.26).move_to(RIGHT * 3.6 + DOWN * 1.55)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in tail], lag_ratio=0.28),
                  run_time=2.2)
        self.wait(2.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.3)
