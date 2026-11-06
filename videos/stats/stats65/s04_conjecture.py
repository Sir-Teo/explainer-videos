from __future__ import annotations

import numpy as np

from videos.stats.stats65.common import *  # noqa: F403


class Conjecture(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. A conjecture, stated precisely enough to be wrong.", 3, r"A conjecture",
                            r"Precise enough to be wrong")
        self.idea()
        self.statement()
        self.gaussian()
        self.chart()
        self.doubts()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The idea came from a change of viewpoint. <bookmark mark='b'/> Any weight function w hat "
            "is the exact likelihood ratio for some distribution: the source reweighted by w hat, call it P sub w hat. "
            "<bookmark mark='c'/> So weighted conformal with wrong weights is not a broken method; it is a correct method "
            "for the wrong target. It covers P sub w hat exactly. <bookmark mark='d'/> The question becomes: how far is the "
            "wrong target from the right one? That suggests the distance to use: total variation, Part forty-three's "
            "largest difference in the probability of any event.",
            [(r"\text{any } \hat w", r":", r"\text{an exact ratio for some law}", 40),
             (r"P_{\hat w}(dx)", r"=", r"\hat w(x) P(dx) / E_P \hat w", 40),
             (r"\text{so}", r":", r"\text{right method, \ wrong target}", 40),
             (r"\text{distance}", r":", r"\mathrm{TV}(P_{\hat w}, Q) = \sup_A |P_{\hat w}(A) - Q(A)|", 40)],
            [r"the change of view", r"the reweighted source", r"the insight", r"Part 43"],
            colors=[(2, THESISC)])

    def statement(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The conjecture. <bookmark mark='b'/> Let the weights w hat be fixed, estimated on data "
            "independent of the calibration set, and let the conditional law of Y given X be the same in source and target. "
            "<bookmark mark='c'/> Then the weighted split-conformal interval covers a test point from Q with probability at "
            "least one minus alpha minus the total variation distance between P sub w hat and Q's covariate law. <bookmark "
            "mark='d'/> When w hat is the true ratio, the distance is zero and Part fifty-seven's guarantee returns. A good "
            "conjecture contains the known case.",
            [(r"\text{assume}", r":", r"\hat w \perp \text{calibration data}, \ \ P_{Y \mid X} = Q_{Y \mid X}", 40),
             (r"\text{claim}", r":", r"Q(Y \in \hat C(X)) \ \ge \ 1 - \alpha - \mathrm{TV}(P_{\hat w}, Q_X)", 40),
             (r"\hat w = w", r"\Rightarrow", r"\mathrm{TV} = 0: \ \text{Part 57's guarantee}", 40),
             (r"\text{falsifiable}", r":", r"\text{one cell below the bound refutes it}", 40)],
            [r"sample splitting", r"the conjecture", r"contains the known case", r"chapter 5 checks"],
            colors=[(1, THESISC)])

    def gaussian(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A special case where everything is explicit. <bookmark mark='b'/> Source N of zero and "
            "one, target N of mu and one: the true ratio is e to the mu x minus mu squared over two. <bookmark mark='c'/> An "
            "over-regularized classifier shrinks the log ratio by a factor lambda between zero and one: tempered weights, w "
            "to the lambda. Reweighting N of zero and one by them gives N of lambda mu and one. <bookmark mark='d'/> The "
            "total variation between two unit-variance normals is two Phi of half the distance between their means, minus "
            "one. So the bound is one minus alpha minus two Phi of one minus lambda times mu over two, plus one.",
            [(r"w(x)", r"=", r"e^{\mu x - \mu^2/2}", 40),
             (r"\hat w = w^\lambda", r"\Rightarrow", r"P_{\hat w} = N(\lambda\mu, 1)", 40),
             (r"\mathrm{TV}(N(a,1), N(b,1))", r"=", r"2\Phi(|a - b|/2) - 1", 40),
             (r"\text{bound}", r"=", r"1 - \alpha - \big(2\Phi(|1 - \lambda||\mu|/2) - 1\big)", 40)],
            [r"Gaussian tilt", r"tempered weights", r"an exact formula", r"computable"],
            colors=[(3, BOUNDC)])

    def chart(self):
        d = load("bound")
        lam = np.asarray(d["lam"])
        A = axes([0, 1.2], [0.3, 1.0], x_length=7.2, y_length=4.4, xlabel=r"temper $\lambda$ of the weights ($w^\lambda$)",
                 ylabel=r"the conjectured lower bound on coverage", xticks=[0, 0.25, 0.5, 0.75, 1, 1.2], yticks=[0.4, 0.6, 0.8, 0.9],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-2.4, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.9), ax.c2p(1.2, 0.9), color=GREY_B, stroke_width=2)
        cols = {"0.5": HONC, "1.0": ESTC, "1.5": NAIVEC}
        curves = VGroup(*[polyline(ax, lam, d["curves"][k], cols[k], 3.5) for k in ("0.5", "1.0", "1.5")])
        one = DashedLine(ax.c2p(1, 0.3), ax.c2p(1, 0.9), color=WHITE, stroke_width=1.5)
        b05 = float(np.interp(0.5, lam, d["curves"]["1.0"]))
        b0 = float(np.interp(0.0, lam, d["curves"]["1.0"]))
        side = side_groups([
            [(r"grey dashes: \ the nominal 90\%", GREY_B)],
            [(r"green, blue, red: \ $\mu = 0.5, \ 1, \ 1.5$", WHITE)],
            [(rf"$\mu = 1$: \ no weights ($\lambda = 0$): \ {100 * b0:.0f}\%", ESTC), (rf"half-strength weights: \ {100 * b05:.0f}\%", ESTC)],
            [(r"white: \ $\lambda = 1$, \ the true weights", WHITE), (r"overshooting is penalized too", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The conjectured bound against the temper lambda, for three shifts. <bookmark mark='b'/> "
            f"Larger shifts, from green to red, make every error in the weights more costly. <bookmark mark='c'/> With a "
            f"shift of one standard deviation, using no weights at all, lambda of zero, guarantees only "
            f"{100 * b0:.0f} percent; half-strength weights guarantee {100 * b05:.0f}. <bookmark mark='d'/> At lambda of one "
            f"the bound is the full ninety percent, and weights that overshoot are penalized as well. The conjecture makes a "
            f"sharp, checkable prediction in every cell of a simulation: coverage above these curves."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(exact_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.4), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(one), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def doubts(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A conjecture should come with its doubts. <bookmark mark='b'/> The bound uses only the "
            "covariates. If the scores do not depend on x at all, ordinary conformal is already exact under any shift, and "
            "the bound is wildly pessimistic. <bookmark mark='c'/> So the bound should be tight only when the scores depend "
            "strongly on x. <bookmark mark='d'/> That is a second, sharper prediction, and the simulation study is designed "
            "to test it, by varying how strongly the noise depends on x.",
            [(r"\text{doubt}", r":", r"\text{the bound ignores the scores}", 40),
             (r"\text{scores } \perp X", r"\Rightarrow", r"\text{exact anyway; \ bound very loose}", 40),
             (r"\text{tight when}", r":", r"\text{scores depend strongly on } x", 40),
             (r"\text{test it}", r":", r"\text{vary } \gamma \text{ in the study}", 40)],
            [r"honesty", r"exchangeable scores", r"a refinement", r"chapter 5"],
            colors=[(2, THESISC)])
