from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, HIST, MODEL, PART, curve, hist_shape, load, normal_pdf

COND = C.BITS  # the conditional: what is left after a coordinate is known


class Gauss(VoiceoverScene):
    def construct(self):
        self.card()
        self.shape()
        self.derive()
        self.check()
        self.uses()

    def card(self):
        card = chapter_card(2, r"Bells in many dimensions", r"What does knowing one coordinate tell you about another?",
                            part=PART)
        with self.voiceover("Chapter two. Bells in many dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def plane(self):
        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[-4, 4, 1], x_length=5.6, y_length=6.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": True, "tick_size": 0.04}).move_to([-3.6, -0.3, 0])
        xl = MathTex(r"x_1", font_size=30, color=GREY_A).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
        yl = MathTex(r"x_2", font_size=30, color=GREY_A).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)
        return ax, VGroup(xl, yl)

    def shape(self):
        d = load("gauss")
        z, pts, S, L = (np.asarray(d[k]) for k in ("z", "pts", "S", "L"))
        evals, evecs = np.asarray(d["evals"]), np.asarray(d["evecs"])
        ax, names = self.plane()
        n = 800
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=DATA, fill_opacity=0.8) for p in z[:n]])
        target = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=DATA, fill_opacity=0.8) for p in pts[:n]])
        unit = 0.8  # screen units per data unit (both axes)

        def ellipse(k, col, sw=3):
            e = Ellipse(width=2 * k * math.sqrt(evals[1]) * unit, height=2 * k * math.sqrt(evals[0]) * unit, color=col,
                        stroke_width=sw)
            return e.rotate(math.atan2(evecs[1, 1], evecs[0, 1])).move_to(ax.c2p(0, 0))

        circ = VGroup(Circle(radius=unit, color=MODEL, stroke_width=3), Circle(radius=2 * unit, color=MODEL,
                                                                              stroke_width=2).set_stroke(opacity=0.5))
        circ.move_to(ax.c2p(0, 0))
        ells = VGroup(ellipse(1, MODEL), ellipse(2, MODEL, 2).set_stroke(opacity=0.5))
        axes_ = VGroup(*[Arrow(ax.c2p(0, 0), ax.c2p(*(math.sqrt(evals[i]) * evecs[:, i])), buff=0, color=C.BITS,
                               stroke_width=4, max_tip_length_to_length_ratio=0.15) for i in (0, 1)])
        f1 = cmath(r"x", "=", r"\mu", "+", r"L\,z", colors={r"L\,z": MODEL}, font_size=40)
        f1n = label(r"$z$: \ independent standard bells; \ $L$: \ a linear map", font_size=22, color=GREY_A)
        f2 = cmath(r"\Sigma", "=", r"L L^\top", font_size=40, colors={r"\Sigma": MODEL})
        f2n = label(r"the covariance: \ $\Sigma_{ij} = \mathbb{E}[(x_i - \mu_i)(x_j - \mu_j)]$", font_size=22,
                    color=GREY_A)
        f3 = cmath(r"p(x)", "=", r"\frac{1}{\sqrt{(2\pi)^d \det \Sigma}}", r"\, e^{-\frac12 (x-\mu)^\top \Sigma^{-1} (x-\mu)}",
                   font_size=36)
        f3n = label(r"contours: \ ellipses, \ along the eigenvectors of $\Sigma$ \ (Part 3)", font_size=22, color=C.BITS)
        right = VGroup(VGroup(f1, f1n).arrange(DOWN, buff=0.12), VGroup(f2, f2n).arrange(DOWN, buff=0.12),
                       VGroup(f3, f3n).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.45).move_to([3.3, 0.3, 0])
        r_, s1, s2 = float(d["r"]), float(d["s1"]), float(d["s2"])
        vals = label(rf"here: \ spreads ${s1:g}$ and ${s2:g}$, \ correlation ${r_:g}$", font_size=24, color=GREY_A)
        vals.to_edge(DOWN, buff=0.3).set_x(3.3)
        with self.voiceover(
            "Start with the simplest cloud in the plane: two independent standard bells, one along each axis. "
            "<bookmark mark='a'/> Every Gaussian in any dimension is this, put through a linear map: x equals mu "
            "plus L times z. <bookmark mark='b'/> The map is summed up by the covariance, sigma, which is L times L "
            "transposed: how each pair of coordinates moves together. <bookmark mark='c'/> The density's contours "
            "are ellipses, with their axes along the eigenvectors of the covariance and lengths set by the square "
            "roots of its eigenvalues, straight out of part three."
        ) as vo:
            self.play(Create(ax), FadeIn(names), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.001), run_time=1.5)
            self.play(Create(circ))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(f1n))
            self.play(Transform(dots, target), Transform(circ, ells), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(f2n), FadeIn(vals))
            vo.wait_until("c")
            self.play(Write(f3), FadeIn(f3n), GrowArrow(axes_[0]), GrowArrow(axes_[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\Lambda": C.INTERVAL, r"\Lambda_{aa}": C.INTERVAL, r"m": COND}
        rows = [
            cmath(r"p(x_a \mid x_b)", r"\propto", r"p(x_a, x_b)", font_size=34),
            cmath(r"\log p", "=", r"-\tfrac12 \begin{bmatrix} x_a - \mu_a \\ x_b - \mu_b \end{bmatrix}^{\!\top}",
                  r"\Lambda", r"\begin{bmatrix} x_a - \mu_a \\ x_b - \mu_b \end{bmatrix} + c", colors=colors,
                  font_size=32),
            cmath(r"\log p", "=", r"-\tfrac12 (x_a - m)^\top", r"\Lambda_{aa}", r"(x_a - m) + c'", colors=colors,
                  font_size=32),
            cmath(r"\Lambda_{aa}^{-1}", "=", r"\Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}", font_size=34),
            cmath(r"m", "=", r"\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b)", colors=colors, font_size=34),
        ]
        whys = [why(r"$x_b$ fixed: \ its density is a constant"),
                why(r"$\Lambda = \Sigma^{-1}$, \ the precision"),
                why(r"complete the square in $x_a$"),
                why(r"invert in blocks: \ the Schur complement"),
                why(r"the same block inverse")]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-2.2, buff=0.42, edge=6.8)
        res = label(r"the conditional is again a bell: \ mean $m$, \ covariance the Schur complement", font_size=26,
                    color=COND).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the question that matters for prediction: if we learn some coordinates, x b, what is left of the "
            "others, x a? <bookmark mark='a'/> With x b fixed, the conditional density is the joint density, "
            "rescaled. <bookmark mark='b'/> Its log is a quadratic form in the inverse of the covariance, called the "
            "precision. <bookmark mark='c'/> Collect the terms in x a and complete the square: a bell again, with "
            "precision lambda a a. <bookmark mark='d'/> Inverting the covariance in blocks gives its covariance: "
            "sigma a a minus sigma a b sigma b b inverse sigma b a, the Schur complement. <bookmark mark='e'/> And "
            "its mean moves from mu a by a linear function of what we learned."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("gauss")
        pts, S = np.asarray(d["pts"]), np.asarray(d["S"])
        a, w = float(d["a"]), float(d["w"])
        m_th, v_th, m_e, v_e, n_sl = (float(d[k]) for k in ("m_th", "v_th", "m_emp", "v_emp", "n_slice"))
        sl = np.asarray(d["slice_x1"])
        ax, names = self.plane()
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.02, color=DATA, fill_opacity=0.45) for p in pts[:900]])
        y_ = ax.c2p(0, a)[1]
        strip = Rectangle(width=ax.x_length, height=0.12, stroke_width=0, fill_color=COND, fill_opacity=0.25)
        strip.move_to([ax.get_center()[0], y_, 0])
        sdots = VGroup(*[Dot(ax.c2p(v, a), radius=0.03, color=COND, fill_opacity=0.7) for v in sl[:200]])
        slope = S[0, 1] / S[1, 1]
        reg = Line(ax.c2p(slope * -4, -4), ax.c2p(slope * 4, 4), color=COND, stroke_width=3)
        reg_l = label(r"the conditional mean: \ Galton's regression line", font_size=22, color=COND)
        reg_l.next_to(ax.c2p(slope * 3.6, 3.6), RIGHT, buff=0.15)
        sl_l = label(rf"$x_2 = {a:g}$", font_size=24, color=COND).next_to(strip, LEFT, buff=0.1).shift(RIGHT * 0.9 + UP * 0.25)
        hx = Axes(x_range=[-1.5, 3.0, 1], y_range=[0, 0.7, 0.2], x_length=5.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, 1.1, 0])
        edges = np.linspace(-1.5, 3.0, 31)
        cnt, _ = np.histogram(sl, bins=edges)
        hh = hist_shape(hx, edges, cnt / cnt.sum() / (edges[1] - edges[0]), color=COND, opacity=0.4)
        xs = np.linspace(-1.5, 3.0, 200)
        pred = curve(hx, xs, normal_pdf(xs, m_th, math.sqrt(v_th)), color=MODEL, stroke_width=3.5)
        hl = label(rf"$x_1$ of the points in the strip \ (of $400{{,}}000$; \ width $\pm {w:g}$)", font_size=22,
                   color=COND).next_to(hx, UP, buff=0.15)
        tbl = VGroup(
            label(r"", font_size=24), label(r"predicted", font_size=24, color=MODEL), label(r"measured", font_size=24, color=COND),
            label(r"mean", font_size=24, color=GREY_A), MathTex(f"{m_th:.3f}", font_size=30, color=MODEL),
            MathTex(f"{m_e:.3f}", font_size=30, color=COND),
            label(r"variance", font_size=24, color=GREY_A), MathTex(f"{v_th:.3f}", font_size=30, color=MODEL),
            MathTex(f"{v_e:.3f}", font_size=30, color=COND))
        tbl.arrange_in_grid(rows=3, cols=3, buff=(0.45, 0.2)).move_to([3.4, -1.55, 0])
        four = label(rf"in four dimensions, \ two given two: \ off by at most ${float(d['err4']):.3f}$ \ "
                     rf"(${int(d['n4']):,}$ points in the box)".replace(",", "{,}"), font_size=22, color=GREY_A)
        four.next_to(tbl, DOWN, buff=0.3)
        hc = history_card(1886, r"Francis Galton", r"heights of parents and children: \ elliptical contours, \ and "
                          r"``regression towards mediocrity''", width=4.4).to_corner(DL, buff=0.3)
        good = abs(m_e - m_th) < 0.03 and abs(v_e / v_th - 1) < 0.05
        verdict = ("Both agree with the formulas to within the sampling error." if good else
                   "Close, but not within the sampling error: the strip has a width, and that biases it a little.")
        with self.voiceover(
            "Check it on samples. Draw four hundred thousand points and keep the ones in a thin strip where x two "
            f"is {a:g}. <bookmark mark='a'/> Their x one values form a bell. The formulas predict its mean, "
            f"{m_th:.3f}, and its variance, {v_th:.3f}; the {n_sl:,} points in the strip give {m_e:.3f} and "
            f"{v_e:.3f}. {verdict} <bookmark mark='b'/> Slide the strip, and the conditional mean traces a straight "
            "line. Galton drew it in 1886 for the heights of parents and children, and called it regression: tall "
            "parents have children who are tall, but less so."
        ) as vo:
            self.play(Create(ax), FadeIn(names), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.001), run_time=1.5)
            self.play(FadeIn(strip), FadeIn(sl_l), FadeIn(sdots))
            vo.wait_until("a")
            self.play(Create(hx), FadeIn(hh), FadeIn(hl))
            self.play(Create(pred), FadeIn(tbl))
            self.play(FadeIn(four))
            vo.wait_until("b")
            self.play(FadeOut(four), FadeIn(hc), Create(reg), FadeIn(reg_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        cards = VGroup(
            history_card(1960, r"Rudolf K\'alm\'an: \ the Kalman filter",
                         r"track a state by conditioning a Gaussian on each new measurement; \ it steered Apollo",
                         width=4.2),
            history_card(r"1990s", r"Gaussian processes", r"a bell over whole functions: \ conditioning on data "
                         r"\emph{is} the regression", width=4.2),
            history_card(2020, r"diffusion models \ (Part 21)", r"the step back from noise is a Gaussian conditional, "
                         r"\ computed by this formula", width=4.2),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.6)
        head = label(r"Conditioning a Gaussian, \ at work", font_size=36).to_edge(UP, buff=0.4)
        f = cmath(r"x_a \mid x_b", r"\;\sim\;", r"\mathcal{N}\big(\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b),\;"
                  r"\Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}\big)", font_size=34).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "This one formula does a great deal of work. <bookmark mark='a'/> In 1960, Rudolf Kalman used it to "
            "track a moving object, conditioning on each new measurement; his filter navigated Apollo. "
            "<bookmark mark='b'/> A Gaussian process puts a bell over whole functions, and fitting it to data is "
            "this conditioning. <bookmark mark='c'/> And in part twenty-one, each step of a diffusion model back "
            "from noise is a Gaussian conditional, written down with exactly this formula."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
