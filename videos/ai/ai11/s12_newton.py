from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.charopt import NS_CUBIC, NS_EXACT, NS_JORDAN
from videos.ai.ai11.common import OPT_COLORS, PART, dec, load, takeaway_card

MU = OPT_COLORS["muon"]
CUB, HYB = "#7FD3FF", C.BITS


def poly(c):
    a, b, cc = c
    return lambda x: a * x + b * x ** 3 + cc * x ** 5


class NewtonSchulz(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.polys()
        self.rounds()
        self.hybrid()
        self.takeaway()

    def card(self):
        c = chapter_card(11, r"Newton--Schulz", r"How do you set every singular value to one without an SVD?", part=PART)
        with self.voiceover("Chapter eleven. Newton–Schulz."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"one round, \ only matrix products:", font_size=30).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"X", r"\leftarrow", r"a\,X + b\,(X X^\top) X + c\,(X X^\top)^2 X", font_size=34),
            cmath(r"X X^\top", "=", r"U \Sigma^2 U^\top", r",\quad X = U \Sigma V^\top", font_size=34),
            cmath(r"X", r"\leftarrow", r"U\,\big(a\Sigma + b\Sigma^3 + c\Sigma^5\big)\,V^\top", font_size=34),
            cmath(r"\sigma", r"\leftarrow", r"p(\sigma) = a\sigma + b\sigma^3 + c\sigma^5", font_size=36,
                  colors={r"p(\sigma) = a\sigma + b\sigma^3 + c\sigma^5": MU}),
        ]
        whys = [why(r"start from $G / \|G\|_F$: \ every $\sigma \le 1$"), why(r"the SVD, \ which we never compute"),
                why(r"the $U$s and $V$s cancel in between"), why(r"the same polynomial on every singular value")]
        step = ladder(self, rows, whys, keep=4, top=2.3, x=-1.2, buff=0.5, edge=6.9)
        goal = label(r"choose $a, b, c$ so that repeating $p$ sends every $\sigma$ in $(0, 1]$ to $1$", font_size=26,
                     color=MU).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "An SVD is slow on a GPU, but multiplying matrices is what a GPU does best. <bookmark mark='a'/> So "
            "scale the gradient so its singular values are at most one, and repeat a round made only of products: X "
            "becomes a X, plus b X X transpose X, plus c times X X transpose squared, X. <bookmark mark='b'/> Write X "
            "by its singular value decomposition, which we never actually compute. <bookmark mark='c'/> Inside each "
            "product the U's and V's cancel, and the round leaves the singular vectors alone. <bookmark mark='d'/> "
            "It just applies one polynomial, p of sigma, to every singular value at once. <bookmark mark='e'/> So the "
            "whole problem is a question about one function of one variable: which polynomial, repeated, sends "
            "everything between zero and one to one?"
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("e")
            self.play(FadeIn(goal))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polys(self):
        ax = CornerAxes(x_range=[0, 1.25, 0.25], y_range=[0, 1.4, 0.5], x_length=5.6, y_length=5.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.4, 0])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1.25, 1.25), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1.25, 1), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        ticks = VGroup(MathTex("1", font_size=22, color=GREY_B).next_to(ax.c2p(1, 0), DOWN, buff=0.08),
                       MathTex("1", font_size=22, color=GREY_B).next_to(ax.c2p(0, 1), LEFT, buff=0.08),
                       MathTex(r"\sigma", font_size=26, color=GREY_A).next_to(ax.c2p(1.25, 0), DOWN, buff=0.1))
        curves = {}
        for key, c_, col in (("cubic", NS_CUBIC, CUB), ("exact", NS_EXACT, HYB), ("jordan", NS_JORDAN, MU)):
            curves[key] = ax.plot(poly(c_), x_range=[0, 1.22 if key != "jordan" else 1.16, 0.005], color=col, stroke_width=3.5)
        rows = VGroup(
            label(r"classical: \ $p(\sigma) = 1.5\sigma - 0.5\sigma^3$", font_size=22, color=CUB),
            label(r"$p(1) = 1$, \ $p'(1) = 0$: \ settles on $1$ exactly; \ slope $1.5$ at $0$: \ slow to start",
                  font_size=20, color=GREY_A),
            label(r"Jordan, 2024: \ $3.4445\sigma - 4.7750\sigma^3 + 2.0315\sigma^5$", font_size=22, color=MU),
            label(r"slope $3.4$ at $0$: \ small values grow fast; \ never settles, \ ends in $[0.7, 1.3]$", font_size=20,
                  color=GREY_A),
            label(r"$2\sigma - 1.5\sigma^3 + 0.5\sigma^5$: \ $p(1) = 1$, \ $p'(1) = 0$", font_size=22, color=HYB),
            label(r"near $1$ the error goes $e \mapsto e^2/2$, \ against the cubic's $\tfrac32 e^2$; \ slope $2$ at $0$",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 0.4, 0])
        for i in (1, 3, 5):
            rows[i].shift(DOWN * 0.02)
        keep_in_frame(rows)
        with self.voiceover(
            "Here are three candidates. <bookmark mark='a'/> The classical Newton–Schulz polynomial, one and a half "
            "sigma minus half sigma cubed. It fixes one with zero slope, so near one it converges very fast; but its "
            "slope at zero is only one and a half, so a tiny singular value takes many rounds to grow. "
            "<bookmark mark='b'/> Keller Jordan tuned the coefficients of a fifth-degree polynomial for Muon: a "
            "slope at zero of three point four, so small values grow fast, at the price of never quite reaching one. "
            "Everything ends between about zero point seven and one point three, which training doesn't mind. "
            "<bookmark mark='c'/> And a third, two sigma minus one and a half sigma cubed plus a half sigma to the "
            "fifth: it also fixes one with zero slope, and near one it squares the error and halves it, three times "
            "better than the cubic, so it pins values that are already close."
        ) as vo:
            self.play(Create(ax), FadeIn(ticks), Create(diag), Create(one))
            vo.wait_until("a")
            self.play(Create(curves["cubic"]), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(curves["jordan"]), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(Create(curves["exact"]), FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounds(self):
        m = load("ns")
        h = np.asarray(m["hist_grad_jordan"], float)  # round x singular values (largest first)
        hc = np.asarray(m["hist_grad_cubic"], float)
        s0 = np.asarray(m["sv_grad"], float)
        big = s0 > 0.01 * s0.max()
        nb = int(m["nbig_grad"])
        lo_b, hi_b = (float(v) for v in m["band_grad_jordan"])
        dev_c = np.asarray(m["dev_grad_cubic"], float)
        R = h.shape[0] - 1
        bx = CornerAxes(x_range=[0, R, 1], y_range=[0, 1.4, 0.5], x_length=4.6, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -0.5, 0])
        xt = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(bx.c2p(k, 0), DOWN, buff=0.08) for k in range(R + 1)])
        xn = label(r"rounds of Jordan's $p$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(rf"the gradient's ${len(s0)}$ singular values", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.15)
        one = DashedLine(bx.c2p(0, 1), bx.c2p(R, 1), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        g = np.random.default_rng(1)
        jit = g.uniform(-0.18, 0.18, h.shape[1])
        cols = [interpolate_color(ManimColor(GREY_B), ManimColor(MU), k / R) for k in range(R + 1)]
        dots = [VGroup(*[Dot(bx.c2p(min(R, max(0, k + j)), float(min(v, 1.4))), radius=0.022, color=cols[k])
                         for v, j in zip(h[k], jit)]) for k in range(R + 1)]
        bandr = Rectangle(width=bx.c2p(R, 0)[0] - bx.c2p(R - 0.3, 0)[0], height=bx.c2p(0, hi_b)[1] - bx.c2p(0, lo_b)[1],
                          stroke_color=MU, stroke_width=1.5).move_to(bx.c2p(R - 0.15, (hi_b + lo_b) / 2))
        # the cobweb of one middling value under Jordan's p
        a_ = CornerAxes(x_range=[0, 1.2, 0.5], y_range=[0, 1.3, 0.5], x_length=3.4, y_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([2.0, 0.5, 0])
        p = poly(NS_JORDAN)
        pc = a_.plot(p, x_range=[0, 1.16, 0.005], color=MU, stroke_width=3)
        dg = DashedLine(a_.c2p(0, 0), a_.c2p(1.2, 1.2), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        xx = float(np.median(h[0][big]))
        web = VGroup()
        for _ in range(R):
            y_ = p(xx)
            web.add(Line(a_.c2p(xx, xx if len(web) else 0), a_.c2p(xx, y_), stroke_width=2, color=C.BITS),
                    Line(a_.c2p(xx, y_), a_.c2p(min(y_, 1.2), y_), stroke_width=2, color=C.BITS))
            xx = y_
        wl = label(r"one middling singular value, \ round by round", font_size=18, color=C.BITS).next_to(a_, UP, buff=0.1)
        res = VGroup(
            label(rf"after ${R}$ rounds, \ the ${nb}$ above $1\%$ of the largest: \ ${lo_b:.2f}$ to ${hi_b:.2f}$",
                  font_size=22, color=MU),
            label(rf"the classical cubic after ${R}$ rounds: \ worst ${dev_c[R]:.2f}$ from $1$; \ after ${len(dev_c) - 1}$: "
                  rf"\ ${dev_c[-1]:.2f}$", font_size=22, color=CUB),
            label(r"the scalar $p$ on the singular values matches the matrix rounds \ to $" + sci(float(m["match_grad"]), 0)
                  + "$", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -2.5, 0])
        keep_in_frame(res)
        tag = note(r"computed: \ the character model's gradient, \ float32").to_corner(UL, buff=0.2)
        said1 = (f"more rounds to catch up: after {len(dev_c) - 1}, {dev_c[-1]:.2f}."
            if dev_c[-1] < dev_c[R] else "many more rounds than that.")
        with self.voiceover(
            "Now on real data: the gradient matrix from Chapter ten. <bookmark mark='a'/> Follow one middling "
            "singular value through Jordan's polynomial: each round bounces it up towards one. "
            f"<bookmark mark='b'/> And here are all {len(s0)} of them, round by round. After {R} rounds, every one "
            f"above a hundredth of the largest, {nb} of them, sits between {lo_b:.2f} and {hi_b:.2f}. The tiniest, "
            "numerical dust, climb but don't arrive, which costs nothing. <bookmark mark='c'/> The classical cubic, "
            f"in the same {R} rounds, leaves its worst value {dev_c[R]:.2f} from one, and needs "
            + said1
        ) as vo:
            self.play(Create(a_), Create(dg), Create(pc), FadeIn(wl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(web), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(xt), FadeIn(xn), FadeIn(yn), Create(one), FadeIn(dots[0]))
            for k in range(1, R + 1):
                self.play(TransformFromCopy(dots[k - 1], dots[k]), run_time=0.7)
            self.play(Create(bandr), FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hybrid(self):
        m = load("ns")
        keys = [("jordan", r"Jordan's $p$, \ $5$ rounds", MU), ("hybrid", r"DeepSeek-V4: \ $8$ of Jordan's, \ then $2$ exact",
                                                                       HYB),
                ("cubic", r"the classical cubic", CUB)]
        lo = -4.0
        ax = CornerAxes(x_range=[0, 12, 2], y_range=[lo, 0.5, 1], x_length=6.4, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.6, -0.5, 0])
        xt = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(ax.c2p(k, lo), DOWN, buff=0.08) for k in range(0, 13, 2)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                      for k in range(int(lo), 1)])
        xn = label(r"rounds", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"the worst singular value's distance from $1$", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        out = VGroup()
        legs = VGroup()
        for key, name, col in keys:
            for mat, dash in (("grad", False), ("weight", True)):
                d = np.log10(np.maximum(np.asarray(m[f"dev_{mat}_{key}"], float), 10 ** lo))
                c_ = curve(ax, np.arange(len(d)), d, col, 3 if not dash else 2)
                out.add(DashedVMobject(c_, num_dashes=24) if dash else c_)
            legs.add(label(name, font_size=20, color=col))
        legs.add(label(r"solid: \ the gradient; \ dashed: \ the trained weight matrix", font_size=18, color=GREY_A))
        legs.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.2, 1.2, 0])
        dh = float(m["dev_grad_hybrid"][-1])
        dj = float(m["dev_grad_jordan"][-1])
        dh_s = dec(dh)
        hist = history_card(2026, r"DeepSeek-V4", r"Muon for most of the model; \ $10$ Newton--Schulz rounds: \ $8$ "
                            r"with Jordan's coefficients to get close, \ $2$ with $(2, -1.5, 0.5)$ to settle on $1$",
                            width=5.6).move_to([3.9, -1.9, 0])
        cite_ = cite(r"N.~Amsel et al., \textit{The Polar Express} (2025): \ a new optimal polynomial each round", corner=DL)
        with self.voiceover(
            "The newest practice combines them. <bookmark mark='a'/> Plot the worst distance from one, round by "
            "round. Jordan's polynomial gets close fast and then stalls, at "
            f"{dj:.2f}. <bookmark mark='b'/> DeepSeek's fourth generation, in 2026, runs eight rounds of Jordan's "
            "polynomial and then two of the exact one, which settles everything that is already close: "
            + f"on our gradient the worst value ends {dh_s} from one. "
            + "<bookmark mark='c'/> The same holds for the trained weight matrix, dashed. And in 2025 Noah Amsel and "
            "colleagues derived the best polynomial for each round, the Polar Express: the search for cheap "
            "orthogonalization is still on."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(out[0]), Create(out[1]), FadeIn(legs[0]), Create(out[4]), Create(out[5]), FadeIn(legs[2]))
            vo.wait_until("b")
            self.play(Create(out[2]), Create(out[3]), FadeIn(legs[1]), FadeIn(hist))
            vo.wait_until("c")
            self.play(FadeIn(legs[3]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Orthogonalize with a polynomial",
                          r"Newton--Schulz applies $p(\sigma) = a\sigma + b\sigma^3 + c\sigma^5$ to every singular value "
                          r"at once, \ using only matrix products. \ The coefficients trade speed for exactness.",
                          r"Next: \ all of them, \ in a fair race")
        with self.voiceover(
            "So orthogonalizing is a polynomial applied to every singular value at once, using nothing but matrix "
            "products, and choosing that polynomial trades speed against exactness. Now let's race all the "
            "optimizers of this part, fairly, on our own model."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
