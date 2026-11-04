from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import CURV, LEVEL, PART, SLOPE, ask, illustration, load, surf3d_axes

COLS = [LEVEL, SLOPE, CURV]
NAMES = [r"level", r"slope", r"curvature"]


class PCA(VoiceoverScene, ThreeDScene):
    def construct(self):
        p = load("pca")
        self.card()
        self.derive()
        self.loadings(p)
        self.day(p)
        self.decades(p)
        self.walk(p)

    def card(self):
        c = chapter_card(10, r"Level, slope and curvature", r"How many numbers move the whole curve?", lit=(1991,),
                         part=PART)
        with self.voiceover("Chapter ten. Level, slope and curvature."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\Sigma", r"=", r"\operatorname{Cov}(\Delta y_{1}, \dots, \Delta y_{30})", font_size=40,
                      colors={r"\Sigma": WHITE}),
                cmath(r"v_1", r"=", r"\arg\max_{\|v\| = 1}\ \operatorname{Var}(v^\top \Delta y) = \arg\max\ v^\top\Sigma v",
                      font_size=40, colors={r"v_1": LEVEL}),
                cmath(r"\Sigma\,v_k", r"=", r"\lambda_k\,v_k,\qquad \text{share}_k = \lambda_k / \textstyle\sum_j \lambda_j",
                      font_size=40, colors={r"\Sigma\,v_k": WHITE}),
                cmath(r"\Delta y", r"\approx", r"s_1 v_1 + s_2 v_2 + s_3 v_3", font_size=42,
                      colors={r"s_1 v_1": LEVEL, r"s_2 v_2": SLOPE, r"s_3 v_3": CURV})]
        whys = [why(r"the covariance of daily changes in nine zero yields, 1 to 30 years, over 40 years"),
                why(r"the first component: the direction of change with the most variance"),
                why(r"the solution is an eigenvector; each further one is the best direction orthogonal to those before"),
                why(r"a day's move is a sum of a few patterns, each scaled by that day's score")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.8, buff=0.55, edge=6.9)
        with self.voiceover(
            "Take the daily changes of the curve at nine maturities, forty years of them, and their covariance matrix. "
            "<bookmark mark='a'/> Ask for the single direction in which the curve moves the most: the unit vector "
            "with the largest variance. <bookmark mark='b'/> The answer is the top eigenvector of the covariance, and "
            "its eigenvalue is the variance it explains; the next one is the best direction at right angles to it, "
            "and so on. <bookmark mark='c'/> If a few of them carry most of the variance, each day's move is a few "
            "patterns, each scaled by a daily score."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def loadings(self, p):
        mats = np.asarray(p["mats"], float)
        L = np.asarray(p["loadings"])
        sh = np.asarray(p["share"])
        g = axes([0, 30], [-0.9, 0.6], x_length=7.6, y_length=4.6, xlabel=r"maturity, years", ylabel=r"loading",
                 xticks=[1, 5, 10, 20, 30], yticks=[-0.8, -0.4, 0, 0.4], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), color=GREY_D, stroke_width=1.5)
        lines = VGroup(*[VGroup(curve(ax, mats, L[k], COLS[k], stroke_width=3.5),
                                *[Dot(ax.c2p(a, b), radius=0.045, color=COLS[k]) for a, b in zip(mats, L[k])])
                         for k in range(3)])
        bars = VGroup()
        for k in range(3):
            r = VGroup(label(NAMES[k], font_size=22, color=COLS[k]),
                       MathTex(rf"{100 * sh[k]:.1f}\%", font_size=34, color=COLS[k])).arrange(RIGHT, buff=0.3)
            bars.add(r)
        bars.add(MathTex(rf"\text{{three together: }}{100 * sh[:3].sum():.1f}\%", font_size=30))
        bars.add(wrapped_label(rf"{p['n_days']:,} daily changes, Dec 1985--2025; daily standard deviations of the "
                               rf"scores: {p['sd_bp'][0]:.1f}, {p['sd_bp'][1]:.1f} and {p['sd_bp'][2]:.1f} bp".replace(
                                   ",", "{,}", 1), 4.4, 17, GREY_A))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here are the first three, from the Fed's curve since 1985. <bookmark mark='a'/> The first loads with the "
            f"same sign everywhere: the whole curve up or down together. It explains {100 * sh[0]:.0f} percent of "
            "daily variance. Call it level. <bookmark mark='b'/> The second runs from negative at the short end to "
            f"positive at the long end: a tilt, steepening or flattening. {100 * sh[1]:.0f} percent. Slope. "
            "<bookmark mark='c'/> The third bends the middle against the ends: "
            f"{100 * sh[2]:.1f} percent. Curvature. <bookmark mark='d'/> Three numbers carry "
            f"{100 * sh[:3].sum():.0f} percent of how the curve moves. Robert Litterman and José Scheinkman found the "
            "same three in 1991, in research done at Goldman Sachs; every rates desk has used them since."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            for k, m in enumerate(("a", "b", "c")):
                vo.wait_until(m)
                self.play(Create(lines[k][0]), FadeIn(VGroup(*lines[k][1:])), FadeIn(bars[k]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(bars[3]), FadeIn(bars[4]))
        self.add(illustration(r"principal components of daily changes in GSW zero yields at 1, 2, 3, 5, 7, 10, 15, 20, 30 years"))
        self.wait(0.4)
        self.clear_scene()

    def day(self, p):
        mats = np.asarray(p["mats"], float)
        L = np.asarray(p["loadings"])
        e = p["example_day"]
        dy = np.asarray(e["dy"])
        sc = L @ dy
        parts = [sc[k] * L[k] for k in range(3)]
        g = axes([-0.5, 8.5], [-90, 30], x_length=8.4, y_length=4.6, ylabel=r"change in the zero yield, bp",
                 xticks=list(range(9)), xfmt=lambda v: f"{int(mats[int(v)])}" + r"\,\text{y}", yticks=[-80, -40, 0],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax

        def bars(vals, col, op=0.85, w=0.6):
            return VGroup(*[Rectangle(width=ax.c2p(i + w / 2, 0)[0] - ax.c2p(i - w / 2, 0)[0],
                                      height=max(abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), 0.01), stroke_width=0,
                                      fill_color=col, fill_opacity=op).move_to(
                [ax.c2p(i, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for i, v in enumerate(vals)])
        real = bars(dy, GREY_B, 0.6)
        acc = np.zeros_like(dy)
        stages = []
        for k in range(3):
            acc = acc + parts[k]
            stages.append(VGroup(*[Dot(ax.c2p(i, v), radius=0.07, color=COLS[k]) for i, v in enumerate(acc)]))
        d = e["date"]
        side = VGroup(
            label(rf"{d // 10000}-{d // 100 % 100:02d}-{d % 100:02d}: the day after Black Monday", font_size=22),
            label(r"grey: the actual change", font_size=19, color=GREY_B),
            *[MathTex(rf"s_{k + 1} = {sc[k]:+.0f}", font_size=30, color=COLS[k]) for k in range(3)],
            wrapped_label(rf"three factors: the largest miss is {np.max(np.abs(acc - dy)):.0f} bp, at "
                          rf"{mats[int(np.argmax(np.abs(acc - dy)))]:.0f} years", 4.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "One day, decomposed: the twentieth of October 1987, the day after the stock market's Black Monday, when "
            "money ran into Treasuries and yields fell sixty to seventy-seven basis points. <bookmark mark='a'/> The "
            "level factor alone, in green, gets most of it. <bookmark mark='b'/> Add slope: the short end fell a little "
            "less than the middle. <bookmark mark='c'/> Add curvature, and three numbers reproduce the whole curve's "
            f"move, missing by at most {np.max(np.abs(acc - dy)):.0f} basis points, at the "
            f"{mats[int(np.argmax(np.abs(acc - dy)))]:.0f}-year point."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b_, UP) for b_ in real], lag_ratio=0.1), FadeIn(side[0]),
                      FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(stages[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(ReplacementTransform(stages[0], stages[1]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(ReplacementTransform(stages[1], stages[2]), FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def decades(self, p):
        dec = p["dec"]
        mats = np.asarray(p["mats"], float)
        keys = list(dec)
        panels = VGroup()
        for kk in keys:
            g = axes([0, 30], [-0.9, 0.7], x_length=2.8, y_length=2.2, xlabel=kk, xticks=[], yticks=[], font_size=12)
            ax = g.ax
            Ls = np.asarray(dec[kk]["loadings"])
            ls = VGroup(*[curve(ax, mats, Ls[k] * np.sign(Ls[k][np.argmax(np.abs(np.asarray(p["loadings"])[k]))] *
                                                          np.asarray(p["loadings"])[k][np.argmax(np.abs(np.asarray(
                                                              p["loadings"])[k]))]), COLS[k], stroke_width=2.5)
                          for k in range(3)])
            sh = np.asarray(dec[kk]["share"])
            t = MathTex(rf"{100 * sh[0]:.0f} / {100 * sh[1]:.0f} / {100 * sh[2]:.0f}\%", font_size=22).next_to(g, DOWN,
                                                                                                         buff=0.1)
            panels.add(VGroup(g, ls, t))
        panels.arrange(RIGHT, buff=0.35).shift(DOWN * 0.2)
        head = label(r"the same three shapes in every decade", font_size=28).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"shares of variance: level / slope / curvature. Slope's share rose after 2006: with short "
                             r"rates pinned at zero, the long end moved alone", 12.0, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Is this a law or a coincidence of one sample? Split the forty years into decades and redo it. The same "
            "three shapes come back each time. <bookmark mark='a'/> The shares shift: after 2006 the slope factor "
            "matters more, because with short rates pinned at zero for years, only the long end could move."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.3, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def walk(self, p):
        c = np.asarray(p["cum"])
        t = np.asarray(p["t"])
        lo, hi = c.min(0), c.max(0)
        ax = surf3d_axes([lo[0] - 50, hi[0] + 50, 400], [lo[1] - 50, hi[1] + 50, 200], [lo[2] - 50, hi[2] + 50, 100],
                         x_length=6.2, y_length=4.4, z_length=3.2)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        pts = [ax.c2p(*v) for v in c]
        path = VGroup()
        for i in range(0, len(pts) - 1, 2):
            col = interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.LOSS), i / len(pts))
            path.add(Line(pts[i], pts[min(i + 2, len(pts) - 1)], color=col, stroke_width=2.5))
        key = VGroup(label(r"cumulative level (across), slope (back), curvature (up), in bp", font_size=19, color=GREY_A),
                     label(r"colour: 1986 (blue) to 2025 (red)", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "Add up each factor's daily scores and the curve's forty years become a walk through three dimensions. "
            "The long drift is along level: rates falling for decades, then the climb of 2022. <bookmark mark='a'/> "
            "Slope swings back and forth with the cycle; curvature barely wanders. A rates book is managed in these "
            "coordinates: so much exposure to level, to slope, to curvature, each hedged or held on purpose."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(path), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.move_camera(theta=-120 * DEGREES, run_time=5)
        q = ask(r"a DV01-neutral 2s10s steepener has no level risk. Which factor is it a bet on, and which would a "
                r"butterfly remove too?")
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover("A DV01-neutral steepener carries no level risk. Which factor is it a bet on? And which "
                            "would a butterfly remove as well?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
