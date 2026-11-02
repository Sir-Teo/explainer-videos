from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card


def omega_grid(kind: str, n=12, size=0.3):
    """An n x n heat-map of a residual covariance matrix: iid, heteroskedastic, overlapping or clustered."""
    rng = np.random.default_rng(2)
    het = 0.35 + 0.65 * rng.random(n)
    g = VGroup()
    for i in range(n):
        for j in range(n):
            if kind == "iid":
                v = 0.8 if i == j else 0.0
            elif kind == "white":
                v = het[i] if i == j else 0.0
            elif kind == "overlap":
                v = max(0.0, 1 - abs(i - j) / 4) * 0.8
            else:
                v = 0.8 if i == j else (0.45 if i // 4 == j // 4 else 0.0)
            sq = Square(side_length=size, stroke_width=0.6, stroke_color=GREY_D, fill_color=EST, fill_opacity=v)
            sq.move_to([(j - n / 2 + 0.5) * size, -(i - n / 2 + 0.5) * size, 0])
            g.add(sq)
    return g


class OLS(VoiceoverScene, ThreeDScene):
    def construct(self):
        f = load("ols_fwl")
        self.card()
        self.projection()
        self.derive()
        self.fwl(f)
        self.sandwich(f)

    def card(self):
        c = chapter_card(1, r"Least squares, seen as geometry", r"What does a regression actually compute?",
                         part=PART)
        with self.voiceover("Chapter one. Least squares, seen as geometry."):
            show_card(self, c)
        self.play(FadeOut(c))

    def projection(self):
        ax = ThreeDAxes(x_range=[-0.5, 3, 1], y_range=[-0.5, 3, 1], z_range=[-0.5, 2.5, 1], x_length=6, y_length=6,
                        z_length=4, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False,
                                                             "stroke_width": 1.5})
        o = ax.c2p(0, 0, 0)
        x1, x2, y = np.array([2.4, 0.3, 0]), np.array([0.6, 2.2, 0]), np.array([1.9, 1.6, 1.9])
        plane = Polygon(ax.c2p(-0.3, -0.3, 0), ax.c2p(3, -0.3, 0), ax.c2p(3, 3, 0), ax.c2p(-0.3, 3, 0),
                        stroke_width=0, fill_color=GREY_B, fill_opacity=0.18)
        a1 = Arrow(o, ax.c2p(*x1), buff=0, color=DATA_C, stroke_width=5)
        a2 = Arrow(o, ax.c2p(*x2), buff=0, color=ALT, stroke_width=5)
        ay = Arrow(o, ax.c2p(*y), buff=0, color=WHITE, stroke_width=5)
        yh = np.array([y[0], y[1], 0])
        ah = Arrow(o, ax.c2p(*yh), buff=0, color=EST, stroke_width=6)
        drop = DashedLine(ax.c2p(*y), ax.c2p(*yh), color=BAD, stroke_width=3)
        right = VGroup(Line(ax.c2p(*(yh + [0, 0, 0.25])), ax.c2p(*(yh + [0.25, 0, 0.25])), color=BAD),
                       Line(ax.c2p(*(yh + [0.25, 0, 0.25])), ax.c2p(*(yh + [0.25, 0, 0])), color=BAD))
        legend_ = VGroup(
            label(r"$y$: the returns, one axis per observation", font_size=22, color=WHITE),
            label(r"the plane: every combination $X b$ of the regressors", font_size=22, color=GREY_A),
            label(r"$X\hat\beta$: the closest point, the fitted values", font_size=22, color=EST),
            label(r"$\hat u = y - X\hat\beta$: the residual, perpendicular", font_size=22, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.95)
        self.add_fixed_in_frame_mobjects(legend_)
        self.remove(legend_)
        with self.voiceover(
            "Start with the picture every regression rests on. Give each observation its own axis: three months of "
            "returns are one point in three dimensions, the white arrow. <bookmark mark='a'/> The regressors are more "
            "arrows, and every combination X times b is a plane. <bookmark mark='b'/> Least squares finds the point of "
            "the plane closest to y: drop a perpendicular. Its foot is the fitted values; the perpendicular is the "
            "residual. <bookmark mark='c'/> The residual is at right angles to every regressor: X transpose times the "
            "residual is zero. Everything follows from that, in three dimensions or a thousand."
        ) as vo:
            self.play(Create(ax), FadeIn(ay), FadeIn(legend_[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(plane), FadeIn(legend_[1]))
            self.move_camera(theta=-35 * DEGREES, run_time=vo.until("b"))
            self.play(Create(drop), FadeIn(ah), FadeIn(legend_[2]), FadeIn(legend_[3]))
            vo.wait_until("c")
            self.play(Create(right))
            self.move_camera(phi=78 * DEGREES, theta=-20 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, plane, a1, a2, ay, ah, drop, right)),
                                                                  FadeOut(legend_)], run_time=1.2)
        self.clear_scene()

    def derive(self):
        C_ = {r"\hat\beta": EST, r"\Omega": BAD}
        rows = [cmath(r"X^\top (y - X\hat\beta)", r"=", r"0", font_size=38, colors=C_),
                cmath(r"\hat\beta", r"=", r"(X^\top X)^{-1} X^\top y", font_size=38, colors=C_),
                cmath(r"\hat\beta - \beta", r"=", r"(X^\top X)^{-1} X^\top u", font_size=38, colors=C_),
                cmath(r"\mathrm{Var}(\hat\beta \mid X)", r"=", r"(X^\top X)^{-1}\, X^\top \Omega X\, (X^\top X)^{-1}",
                      font_size=38, colors=C_),
                cmath(r"\Omega = \sigma^2 I", r"\Rightarrow", r"\sigma^2 (X^\top X)^{-1}", font_size=38, colors=C_)]
        whys = [why(r"the residual is perpendicular to every column of $X$: the normal equations"),
                why(r"solve them"),
                why(r"substitute $y = X\beta + u$: the error of $\hat\beta$ is a weighted sum of the scores $x_t u_t$"),
                why(r"the variance of a linear map: bread, meat, bread; $\Omega = \mathbb{E}[u u^\top \mid X]$"),
                why(r"only if the errors are uncorrelated and equally noisy do we get the textbook formula")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.75, edge=6.8)
        with self.voiceover(
            "The algebra, line by line. The residual is perpendicular to the columns of X: the normal equations. "
            "<bookmark mark='a'/> Solve them. <bookmark mark='b'/> Substitute the true model, and the estimation error "
            "is a weighted sum of the scores, each regressor times its error. <bookmark mark='c'/> Its variance is a "
            "sandwich: bread, X transpose X inverse, around a filling, X transpose omega X, where omega is the "
            "covariance of all the errors. <bookmark mark='d'/> Only if omega is a constant times the identity does it "
            "collapse to the textbook formula. Every standard error in this part is a claim about the filling."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def fwl(self, f):
        smb, y, rx, ry = (np.asarray(f[k]) for k in ("smb", "y", "rx", "ry"))
        g = axes([-0.16, 0.16], [-0.25, 0.25], x_length=6.0, y_length=4.6, xlabel=r"size factor (SMB), monthly",
                 ylabel=r"tobacco's excess return, monthly", xticks=[-0.1, 0, 0.1], yticks=[-0.2, 0, 0.2],
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.25)
        ax = g.ax
        clip = lambda v, a: float(np.clip(v, -a, a))  # noqa: E731
        dots = VGroup(*[Dot(ax.c2p(clip(a, 0.16), clip(b, 0.25)), radius=0.025, color=DATA_C, fill_opacity=0.7)
                        for a, b in zip(smb, y)])
        xs = np.linspace(-0.15, 0.15, 10)
        fit_raw = curve(ax, xs, np.mean(y) + f["alone"] * (xs - np.mean(smb)), ALT, stroke_width=3)
        targets = [ax.c2p(clip(a, 0.16), clip(b, 0.25)) for a, b in zip(rx, ry)]
        fit_res = curve(ax, xs, f["fwl"] * xs, EST, stroke_width=3.5)
        b, se_n, se_w = f["beta"], f["se_naive"], f["se_white"]
        side = VGroup(
            label(r"Frisch--Waugh--Lovell", font_size=26, color=WHITE),
            MathTex(rf"\text{{slope alone: }} {f['alone']:+.2f}", font_size=30, color=ALT),
            wrapped_label(r"now project the market out of both: regress each on the market and keep the residuals",
                          5.2, 20, GREY_A),
            MathTex(rf"\text{{residual on residual: }} {f['fwl']:+.4f}", font_size=30, color=EST),
            MathTex(rf"\text{{multiple regression: }} {b[2]:+.4f}", font_size=30, color=EST),
            MathTex(rf"\text{{difference: }} {f['gap']:.0e}".replace("e-", r"\times 10^{-") + "}", font_size=26,
                    color=GOOD),
            MathTex(rf"\hat\beta_2 = (\tilde x_2^\top \tilde x_2)^{{-1}} \tilde x_2^\top \tilde y,\ \ "
                    r"\tilde v = M_1 v", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        src = real_data(rf"Kenneth French: tobacco (Smoke), market and SMB, monthly 1927--2020, {f['n']:,} months"
                        .replace(",", "{,}"))
        q = predict(r"Add a regressor that is uncorrelated with SMB. Does SMB's slope change?").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "What does it mean to control for something? Ask how tobacco stocks load on the size factor. Alone, the "
            f"slope is {f['alone']:+.2f}: tobacco looks like a small-stock industry. <bookmark mark='a'/> But size and the "
            "market move together. The Frisch-Waugh-Lovell theorem: regress tobacco on the market and keep the "
            "residual; do the same for size. Every point slides to its residual position. <bookmark mark='b'/> The slope "
            f"of residual on residual is {f['fwl']:+.4f}: net of the market, tobacco behaves like a big-company stock. "
            "<bookmark mark='c'/> And it equals the multiple-regression coefficient to sixteen decimal places. A control "
            "is a projection, applied to both sides. <bookmark mark='d'/> Pause and predict: add a regressor "
            "uncorrelated with size. Does size's slope change? No; its standard error can."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003, run_time=1.5))
            self.play(Create(fit_raw), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(side[2]), FadeOut(fit_raw),
                      *[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=3)
            vo.wait_until("b")
            self.play(Create(fit_res), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]), FadeIn(side[5]), FadeIn(side[6]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sandwich(self, f):
        se_n, se_w = f["se_naive"], f["se_white"]
        bread_l = RoundedRectangle(width=0.7, height=3.9, corner_radius=0.15, fill_color=ALT, fill_opacity=0.35,
                                   stroke_color=ALT)
        bread_r = bread_l.copy()
        meat = omega_grid("iid")
        sand = VGroup(bread_l, meat, bread_r).arrange(RIGHT, buff=0.25).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        tags = VGroup(MathTex(r"(X^\top X)^{-1}", font_size=24, color=ALT).next_to(bread_l, UP, buff=0.15),
                      MathTex(r"X^\top \Omega X", font_size=24, color=EST).next_to(meat, UP, buff=0.15),
                      MathTex(r"(X^\top X)^{-1}", font_size=24, color=ALT).next_to(bread_r, UP, buff=0.15))
        name = label(r"iid: only the diagonal, all equal", font_size=24, color=GREY_A).next_to(sand, DOWN, buff=0.35)
        names = {"white": r"White (1980): the diagonal, each its own size",
                 "overlap": r"overlap and persistence: a band (chapter 2)",
                 "cluster": r"shared shocks: blocks (chapter 3)"}
        side = VGroup(
            label(r"tobacco's size slope, two fillings:", font_size=23, color=GREY_A),
            MathTex(rf"\text{{iid: }} {se_n[2]:.3f} \qquad \text{{White: }} {se_w[2]:.3f}", font_size=30, color=EST),
            MathTex(rf"\text{{market slope: iid }} {se_n[1]:.3f},\ \text{{White }} {se_w[1]:.3f}", font_size=28,
                    color=GREY_A),
            wrapped_label(r"the estimate is the same; only the claimed precision changes. Every robust standard "
                          r"error replaces the meat with an estimate of how the scores $x_t u_t$ co-move.", 5.4, 21,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The sandwich as a picture. The meat is the errors' covariance matrix: row and column t are month t. Under "
            "iid, only the diagonal is lit, all equally. <bookmark mark='a'/> Halbert White's 1980 estimator lets each "
            "diagonal cell have its own size, estimated by the squared residual, x t x t transpose times u hat squared: "
            "consistent even though each single cell is a terrible estimate, because the sandwich only needs their "
            f"average. For tobacco's size slope it gives {se_w[2]:.3f} against {se_n[2]:.3f}. <bookmark mark='b'/> But "
            "finance lives off the diagonal. Overlapping returns and persistent predictors light a band: chapter two. "
            "<bookmark mark='c'/> Shocks shared within a month light blocks: chapter three. The estimate never changes; "
            "how much it can be trusted does. The next three chapters are three shapes of meat."
        ) as vo:
            self.play(FadeIn(sand), FadeIn(tags), FadeIn(name), FadeIn(side[0]))
            vo.wait_until("a")
            for kind, mark in (("white", "b"), ("overlap", "c"), ("cluster", None)):
                new = omega_grid(kind).move_to(meat)
                nn = label(names[kind], font_size=24, color=GREY_A).move_to(name)
                self.play(Transform(meat, new), Transform(name, nn), run_time=1.2)
                if kind == "white":
                    self.play(FadeIn(side[1]), FadeIn(side[2]))
                if mark:
                    vo.wait_until(mark)
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
