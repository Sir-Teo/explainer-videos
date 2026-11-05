from __future__ import annotations

import numpy as np
from scipy import special

from videos.stats.stats24.common import *  # noqa: F403
from videos.stats.stats24.s01_hook import beetle_panel


class IRLS(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.working()
        self.steps()
        self.deviance_drop()
        self.noncanonical()
        self.cost()

    def card(self):
        card = chapter_card(3, r"IRLS derived", r"Fisher scoring is weighted least squares", part=PART)
        with self.voiceover("Chapter three. Iteratively reweighted least squares, derived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"U(\beta)", r"=", r"\textstyle\sum_i \dfrac{(y_i - \mu_i)}{\phi V(\mu_i)} \dfrac{\partial\mu_i}{\partial\eta_i} x_i = X^\top W (z - \eta)/\phi", font_size=28),
            cmath(r"\mathcal I(\beta)", r"=", r"X^\top W X/\phi, \ \ W = \mathrm{diag}\Big\{\dfrac{(\partial\mu_i/\partial\eta_i)^2}{V(\mu_i)}\Big\}", font_size=28),
            cmath(r"\beta^{\text{new}}", r"=", r"\beta + \mathcal I^{-1} U = (X^\top W X)^{-1} X^\top W z", font_size=30),
            cmath(r"z_i", r"=", r"\eta_i + (y_i - \mu_i)\, \partial\eta_i/\partial\mu_i", font_size=30),
        ]
        rows[2][2].set_color(MODEL)
        whys = [why(r"the chain rule through the link"), why(r"the expected information"),
                why(r"a Fisher scoring step, \ rearranged"), why(r"the working response: \ a linearized $y$")]
        with self.voiceover(
            "<bookmark mark='a'/> The score of a generalized linear model follows from the chain rule: residuals, divided by "
            "the variance, times the slope of the inverse link, times the covariates. <bookmark mark='b'/> The expected "
            "information is X transpose W X over phi, with weights equal to that slope squared over the variance. "
            "<bookmark mark='c'/> A Fisher scoring step, beta plus the inverse information times the score, rearranges into "
            "a weighted least squares fit, <bookmark mark='d'/> of a working response z: the current linear predictor plus "
            "the residual stretched back onto the linear-predictor scale. Every step is Part 23's weighted least squares; "
            "only the weights and the working response change."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def working(self):
        d = load("irls")
        b = load("bliss")
        x = np.asarray(b["x"])
        z, w = np.asarray(d["z0"]), np.asarray(d["w0"])
        A = axes([1.67, 1.9], [-4, 4], x_length=8.0, y_length=4.4, xlabel=r"$\log_{10}$ dose", ylabel=r"working response $z$",
                 xticks=[1.7, 1.75, 1.8, 1.85, 1.9], yticks=[-4, -2, 0, 2, 4], center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, c), radius=0.04 + 0.006 * np.sqrt(ww), color=OBSC) for a, c, ww in zip(x, z, w)])
        P = np.asarray(d["path"])
        l1 = Line(ax.c2p(1.67, P[1, 0] + 1.67 * P[1, 1]), ax.c2p(1.9, P[1, 0] + 1.9 * P[1, 1]), color=MODEL, stroke_width=3.5)
        rows = fit_rows(VGroup(
            label(r"step 1, \ from $\beta = 0$: \ every $\mu = \tfrac12$", font_size=22),
            label(r"$z = (k/n - \tfrac12)/\tfrac14$", font_size=22, color=OBSC),
            label(r"weights $n \cdot \tfrac14$: \ dot size", font_size=22, color=GREY_A),
            label(rf"weighted line: \ slope {P[1, 1]:.1f}", font_size=22, color=MODEL),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Watch it on Bliss's beetles with the logit link, starting from all coefficients zero, "
            "so every fitted probability is one half. <bookmark mark='b'/> The working response is the observed proportion "
            "minus a half, divided by a quarter. <bookmark mark='c'/> The weights are the number of beetles times a "
            "quarter, nearly equal here. <bookmark mark='d'/> A weighted straight line through those points gives the first "
            "step's coefficients, a slope of twenty-one point three."
        ) as vo:
            self.add(bliss_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in dots], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(l1), FadeIn(rows[3]))
        self.clear_scene()

    def steps(self):
        d = load("irls")
        b = load("bliss")
        P = np.asarray(d["path"])
        Pn = beetle_panel(b)
        curves = [Pn.curve(special.expit, P[i], interpolate_color(ManimColor(GREY_B), ManimColor(MODEL), min(1, i / 4)), 3)
                  for i in range(1, 6)]
        dev = d["deviance"]
        rows = fit_rows(VGroup(
            label(r"step: \ slope, \ deviance", font_size=22, color=GREY_B),
            *[label(rf"{i}: \ {P[i, 1]:.2f}, \ {dev[i]:.2f}", font_size=22,
                    color=GREY_A if i < 4 else MODEL) for i in range(1, 6)],
            label(rf"converged after {d['iters']} steps", font_size=22, color=HIT),
        ), 3.6, 0.36, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Recompute the weights and working response at the new fit, and fit again. The first curve "
            "is far too shallow. <bookmark mark='b'/> The second is closer, the deviance falling from three hundred and six "
            "to thirteen. <bookmark mark='c'/> By the fourth step the coefficients have three correct digits, and "
            "<bookmark mark='d'/> after seven the changes are below the computer's precision: Newton's quadratic "
            "convergence, from Part 21."
        ) as vo:
            self.add(bliss_tag())
            self.play(FadeIn(Pn))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(ReplacementTransform(curves[0], curves[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(ReplacementTransform(curves[1], curves[2]), FadeIn(rows[3]))
            self.play(ReplacementTransform(curves[2], curves[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(ReplacementTransform(curves[3], curves[4]), FadeIn(rows[5]), FadeIn(rows[6]))
        self.clear_scene()

    def deviance_drop(self):
        d = load("irls")
        dev = np.asarray(d["deviance"])
        it = np.arange(len(dev))
        A = axes([0, len(dev) - 1], [0, 2.6], x_length=8.0, y_length=4.2, xlabel=r"IRLS step",
                 ylabel=r"$\log_{10}$ deviance", xticks=list(range(len(dev))), yticks=[0, 1, 2], center=[-1.6, 0.3, 0])
        ax = A.ax
        pl = VGroup(polyline(ax, it, np.log10(dev), MODEL, 3.5), *[Dot(ax.c2p(i, np.log10(v)), radius=0.07, color=MODEL)
                                                                  for i, v in zip(it, dev)])
        floor = DashedLine(ax.c2p(0, np.log10(dev[-1])), ax.c2p(len(dev) - 1, np.log10(dev[-1])), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"start: \ {dev[0]:.1f}", font_size=22),
            label(rf"minimum: \ {dev[-1]:.2f}", font_size=22, color=TRUE),
            label(r"step-halving: \ never let it rise", font_size=22, color=GREY_A),
            label(r"the deviance is minus twice the log likelihood, \ shifted", font_size=22, color=MODEL),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The deviance, which chapter four defines properly, falls at every step from three hundred "
            "and six <bookmark mark='b'/> to its minimum, eleven point two three. <bookmark mark='c'/> Far from the answer a "
            "full Newton step can overshoot, so the software halves the step until the deviance stops rising, the line "
            "search of Part 21. <bookmark mark='d'/> Minimizing the deviance is maximizing the likelihood."
        ) as vo:
            self.play(FadeIn(A), Create(floor))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def noncanonical(self):
        rows = [
            cmath(r"\text{canonical}", r":", r"W \text{ from the observed = expected curvature}", font_size=30),
            cmath(r"\text{probit, \ cloglog}", r":", r"\text{IRLS uses the expected information}", font_size=30),
            cmath(r"\text{Newton}", r":", r"\text{the observed: \ different steps, \ same answer}", font_size=30),
            cmath(r"\text{SEs}", r":", r"\text{expected vs observed: \ Part 22, \ chapter four}", font_size=30),
        ]
        rows[2][-1].set_color(MODEL)
        whys = [why(r"the logit, \ the log for counts"), why(r"Fisher scoring: \ always positive weights"), why(r"the same maximum, \ by another road"), why(r"they differ slightly away from canonical links")]
        with self.voiceover(
            "<bookmark mark='a'/> One subtlety. With a canonical link, the weights are both the observed and the expected "
            "curvature. <bookmark mark='b'/> With the probit or the complementary log-log, IRLS uses the expected "
            "information: Fisher scoring, whose weights are always positive. <bookmark mark='c'/> Newton's method would use "
            "the observed curvature, taking different steps to the same maximum. <bookmark mark='d'/> The two give slightly "
            "different standard errors, the observed against the expected information, Part 22's chapter four; software "
            "usually reports the expected."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cost(self):
        rows = [
            cmath(r"\text{each step}", r":", r"\text{one weighted QR: \ } O(np^2)", font_size=30),
            cmath(r"\text{steps}", r":", r"\text{usually } 4 \text{ to } 10", font_size=30),
            cmath(r"\text{start}", r":", r"\mu_i^{(0)} = y_i \ \text{(adjusted)}, \ \eta^{(0)} = g(\mu^{(0)})", font_size=30),
            cmath(r"\text{SEs}", r":", r"(X^\top W X)^{-1}\phi \ \text{at the last step}", font_size=30),
        ]
        rows[0][2].set_color(MODEL)
        whys = [why(r"Part 23's numerics, \ unchanged"), why(r"quadratic convergence"),
                why(r"start from the data, \ not from zero"), why(r"free: \ the last $W$")]
        with self.voiceover(
            "<bookmark mark='a'/> Each step costs one weighted least squares fit, done by Part 23's QR decomposition. "
            "<bookmark mark='b'/> Usually four to ten steps suffice. <bookmark mark='c'/> Software starts not from zero but "
            "from the data, nudged away from zero and one, which saves steps. <bookmark mark='d'/> And the standard errors "
            "come for free: the inverse of X transpose W X at the last step, times the dispersion. Bliss computed all this "
            "by hand in 1935; R's glm runs this same loop."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
