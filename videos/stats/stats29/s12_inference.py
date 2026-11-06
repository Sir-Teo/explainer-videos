from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats29.common import *  # noqa: F403


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.picture()
        self.fixes()
        self.rbc()
        self.board()
        self.bands()

    def card(self):
        card = chapter_card(11, r"Inference for curves", r"Intervals that admit their bias", lit=(2018,), part=PART)
        with self.voiceover("Chapter eleven. Inference for curves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\dfrac{\hat f_h(x) - f(x)}{\mathrm{SE}}", r"=", r"\dfrac{\hat f_h - E\hat f_h}{\mathrm{SE}} + \dfrac{\text{bias}}{\mathrm{SE}}", font_size=30),
            cmath(r"\text{at } h^* \propto n^{-1/5}", r":", r"\dfrac{\text{bias}}{\mathrm{SE}} \to \text{a constant} \ne 0", font_size=30),
            cmath(r"\text{so}", r":", r"\hat f \pm 1.96\, \mathrm{SE} \ \text{undercovers, \ for ever}", font_size=30),
            cmath(r"\text{worst at}", r":", r"\text{peaks and valleys, \ where } |f''| \text{ is large}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"noise plus a shift"), why(r"MSE-optimal means bias and SD of the same order"),
                why(r"the centre is in the wrong place"), why(r"bias $= \frac12 h^2 f''$")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual interval, estimate plus or minus one point nine six standard errors, assumes the "
            "standardized error is standard normal. For a curve estimate it is that plus the bias over the standard error. "
            "<bookmark mark='b'/> At the MSE-optimal bandwidth, chosen precisely to balance bias against variance, that "
            "ratio doesn't shrink as n grows: it converges to a nonzero constant. <bookmark mark='c'/> So the interval is "
            "centred in the wrong place and undercovers, however much data you have. <bookmark mark='d'/> Worst at peaks "
            "and valleys, where the curvature, and so the bias, is largest."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("rbc")
        f0, m, s = d["f0"], d["mean_est"], d["sd_est"]
        xs = np.linspace(0.38, 0.82, 300)
        A = axes([0.38, 0.82], [0, 8.5], x_length=7.4, y_length=4.4, xlabel=r"$\hat f_h(4.3)$ over 2,000 samples",
                 ylabel=r"density", xticks=[0.45, 0.55, 0.65, 0.75], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        dist = curve(ax, xs, stats.norm.pdf(xs, m, s), KDEC, 3)
        tl = DashedLine(ax.c2p(f0, 0), ax.c2p(f0, 8.2), color=TRUE, stroke_width=3)
        ml = DashedLine(ax.c2p(m, 0), ax.c2p(m, 8.2), color=KDEC, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"the long eruptions' mode, \ $x = {d['x0']}$; \ $n = {d['n']}$", font_size=22),
            label(rf"gold: \ the truth, \ {f0:.3f}", font_size=22, color=TRUE),
            label(rf"blue: \ the estimates: \ mean {m:.3f}, \ SD {s:.3f}", font_size=22, color=KDEC),
            label(rf"bias {m - f0:.3f} \ (theory {d['bias_theory']:.3f}): \ {abs(m - f0) / s:.2f} SD", font_size=22, color=BIASC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> At the long eruptions' mode, with three hundred observations from the two-humped density and "
            "the pointwise MSE-optimal bandwidth. <bookmark mark='b'/> The true density there is point six one seven. "
            "<bookmark mark='c'/> Two thousand simulated estimates centre at point five eight seven: <bookmark mark='d'/> a "
            "bias of minus point oh three, as the formula predicts, more than half a standard deviation. The interval built "
            "around such an estimate misses the truth too often."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(tl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(dist), Create(ml), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fixes(self):
        rows = [
            cmath(r"\text{undersmooth}", r":", r"h = o(n^{-1/5}): \ \text{bias/SE} \to 0", font_size=30),
            cmath(r"\text{bias-correct}", r":", r"\hat f_h - \tfrac12 h^2 \mu_2 \hat f''_b", font_size=32),
            cmath(r"\text{but}", r":", r"\text{the correction is noisy; \ the usual SE ignores it}", font_size=30),
            cmath(r"\text{robust}", r":", r"\text{use the SE of the corrected estimator}", font_size=32),
        ]
        rows[3][2].set_color(SPLC)
        whys = [why(r"less bias, \ wider intervals, \ which $h$?"), why(r"subtract an estimate of the bias"),
                why(r"Hall (1992): \ undersmoothing usually wins"), why(r"Calonico, Cattaneo \& Farrell (2018)")]
        with self.voiceover(
            "<bookmark mark='a'/> Two classical fixes. Undersmooth: use a smaller bandwidth than optimal, so the bias becomes "
            "negligible relative to the noise; but how much smaller is a new tuning problem. <bookmark mark='b'/> Or "
            "estimate the bias, which needs f double prime, and subtract it. <bookmark mark='c'/> Peter Hall showed in 1992 "
            "that, done naively, the second loses: the estimated correction adds variance that the usual standard error "
            "ignores. <bookmark mark='d'/> Sebastian Calonico, Matias Cattaneo and Max Farrell's robust bias correction keeps "
            "the correction but computes the standard error of the corrected estimator itself, and proved this gives better "
            "coverage than undersmoothing."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rbc(self):
        rows = [
            cmath(r"\hat f''_h(x)", r"=", r"\tfrac{1}{nh^3} \textstyle\sum_i K''\bigl(\tfrac{x - x_i}{h}\bigr)", font_size=30),
            cmath(r"\hat f_{\mathrm{bc}}", r"=", r"\tfrac{1}{nh} \textstyle\sum_i M\bigl(\tfrac{x - x_i}{h}\bigr), \ \ M = K - \tfrac12 K''", font_size=30),
            cmath(r"\mathrm{SE}_{\mathrm{rbc}}", r"=", r"\mathrm{sd}\bigl(\tfrac1h M(\tfrac{x - x_i}{h})\bigr) / \sqrt n", font_size=30),
            cmath(r"M", r":", r"\text{a fourth-order kernel: \ bias } O(h^4)", font_size=30),
        ]
        rows[1][2].set_color(SPLC)
        whys = [why(r"pilot $b = h$"), why(r"the correction folded into one kernel"), why(r"its own variability, \ honestly"),
                why(r"$\int u^2 M = 0$")]
        with self.voiceover(
            "<bookmark mark='a'/> With the pilot bandwidth equal to h, the estimated curvature is a kernel sum with the "
            "kernel's second derivative. <bookmark mark='b'/> The bias-corrected estimate is then a kernel estimate with a "
            "new kernel M, K minus half K double prime. <bookmark mark='c'/> The robust standard error is just the standard "
            "error of that average. <bookmark mark='d'/> M has zero second moment: it is a fourth-order kernel, with bias of "
            "order h to the fourth. The interval is wider than the naive one, because it is honest about both the bias and "
            "its correction."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=29) if r.part == 29]
        b = coverage_board(rows, lit_part=29, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        d = load("rbc")
        w = d["width"]
        with self.voiceover(
            "<bookmark mark='a'/> The Board: two thousand samples, the ninety-five percent interval for the density at the "
            "long eruptions' mode. At the MSE-optimal bandwidth the conventional interval covers ninety-one percent: broken, "
            f"and with three hundred observations the shortfall is not going away. <bookmark mark='b'/> Undersmoothing, with "
            "the bandwidth shrunk by n to the minus a tenth, restores ninety-five, with intervals forty-four percent wider. "
            "<bookmark mark='c'/> Robust bias correction also restores ninety-five, at almost the same width, without "
            "choosing a second bandwidth."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        del w
        self.wait(1.0)
        self.clear_scene()

    def bands(self):
        rows = fit_rows(VGroup(
            label(r"pointwise: \ 95\% at each $x$; \ the whole curve: \ much less", font_size=24),
            label(r"simultaneous bands: \ the supremum of a Gaussian process \ (Bickel \& Rosenblatt 1973)", font_size=24, color=KDEC),
            label(r"Bayesian spline bands: \ good average coverage \ (Nychka 1988)", font_size=24, color=SPLC),
            label(r"bias is never visible in the data: \ only theory can bound it \ (Part 53)", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> These are pointwise intervals: each covers at its own x. Covering the whole curve at once "
            "needs simultaneous bands, <bookmark mark='b'/> built from the distribution of the supremum of a Gaussian process, "
            "Peter Bickel and Murray Rosenblatt's result. <bookmark mark='c'/> The spline's Bayesian bands, from the "
            "mixed-model view, have good coverage averaged over x, Douglas Nychka showed. <bookmark mark='d'/> But bias can "
            "never be seen in the data alone: it is bounded only by assumptions about smoothness, which Part 53 studies in "
            "Bayesian form."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
