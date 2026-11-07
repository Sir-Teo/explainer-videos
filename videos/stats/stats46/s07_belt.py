from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Belt(VoiceoverScene):
    def construct(self):
        self.card()
        self.duality()
        self.belt()
        self.coverage()
        self.uma()
        self.pratt()

    def card(self):
        card = chapter_card(6, r"Confidence sets by inversion", r"Invert a family of tests into a confidence set", lit=(1937,), part=PART)
        with self.voiceover("Chapter six. Confidence sets by inversion: inverting a family of tests gives a confidence set, which "
            "need not be an interval."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def duality(self):
        rows = [
            cmath(r"A(\theta_0)", r":", r"\text{the acceptance region of a level-}\alpha \text{ test of } \theta = \theta_0", font_size=30),
            cmath(r"C(x)", r"=", r"\{\theta_0 : x \in A(\theta_0)\}", font_size=36),
            cmath(r"P_\theta(\theta \in C(X))", r"=", r"P_\theta(X \in A(\theta)) \ge 1 - \alpha \ \ \forall \theta", font_size=32),
            cmath(r"\text{conversely}", r":", r"A(\theta_0) = \{x : \theta_0 \in C(x)\} \ \text{is a level-}\alpha\text{ test}", font_size=30),
        ]
        rows[1][-1].set_color(CIC)
        rows[2][-1].set_color(UMPC)
        whys = [why(r"one test per $\theta_0$"), why(r"keep the $\theta_0$ not rejected"), why(r"Neyman (1937)"), why(r"the duality")]
        with self.voiceover(
            "<bookmark mark='a'/> Neyman's construction of 1937. For each possible value theta nought, take the acceptance "
            "region of a level-alpha test of theta equal to theta nought. <bookmark mark='b'/> The confidence set for data x "
            "is every theta nought that the data do not reject. <bookmark mark='c'/> It covers the true theta exactly when "
            "the data fall in that theta's acceptance region, which happens with probability at least one minus alpha, "
            "whatever theta is. <bookmark mark='d'/> And conversely, any confidence set defines a family of tests. Tests and "
            "confidence sets are the same objects, and the optimality of one transfers to the other."
        ) as vo:
            heading=label('A confidence set retains every parameter value not rejected',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def belt(self):
        d = load("belt")
        n = d["n"]
        A = axes([-0.6, 20.6], [0, 1], x_length=7.4, y_length=4.6, xlabel=r"successes $x$ in 20 trials", ylabel=r"$p$",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.1, 0])
        ax = A.ax
        segs = VGroup(*[Line(ax.c2p(x, lo), ax.c2p(x, hi), color=CIC, stroke_width=5) for x, (lo, hi) in enumerate(d["cp"])])
        lo_pts = [ax.c2p(x, lo) for x, (lo, hi) in enumerate(d["cp"])]
        hi_pts = [ax.c2p(x, hi) for x, (lo, hi) in enumerate(d["cp"])]
        belt = Polygon(*(lo_pts + hi_pts[::-1]), stroke_width=0, fill_color=CIC, fill_opacity=0.15)
        p0 = 0.3
        acc = [x for x, (lo, hi) in enumerate(d["cp"]) if lo <= p0 <= hi]
        hline = Line(ax.c2p(acc[0] - 0.4, p0), ax.c2p(acc[-1] + 0.4, p0), color=H0C, stroke_width=6)
        x0 = 6
        vline = Line(ax.c2p(x0, d["cp"][x0][0]), ax.c2p(x0, d["cp"][x0][1]), color=UMPC, stroke_width=8)
        side = fit_rows(VGroup(
            label(r"the Clopper--Pearson belt, \ $n = 20$, \ 95\%", font_size=22),
            label(rf"across, \ at $p = {p0}$: \ the acceptance region \ $x = {acc[0]}, \ldots, {acc[-1]}$", font_size=22, color=H0C),
            label(rf"up, \ at $x = {x0}$: \ the interval \ $[{d['cp'][x0][0]:.3f}, \ {d['cp'][x0][1]:.3f}]$", font_size=22, color=UMPC),
            label(r"read the belt one way for tests, \ the other for intervals", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The construction drawn: the confidence belt for a binomial proportion with twenty "
            f"trials, from Clopper and Pearson's equal-tailed tests. Each gold segment is the interval for one count. "
            f"<bookmark mark='b'/> Read it across, at p equal to {p0}: the counts whose intervals contain point three form "
            f"the acceptance region of the test, from {acc[0]} to {acc[-1]}. <bookmark mark='c'/> Read it up, at {x0} "
            f"successes: the p's whose acceptance regions contain {x0} form the interval, from {say(d['cp'][x0][0], 2)} to "
            f"{say(d['cp'][x0][1], 2)}. <bookmark mark='d'/> One belt, read in two directions."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ beta quantiles")))
            vo.wait_until("a")
            self.play(FadeIn(belt), LaggedStart(*[Create(s) for s in segs], lag_ratio=0.05), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(hline), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vline), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def coverage(self):
        d = load("belt")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"exact coverage, \ $n = 20$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 0.95], center=[-2.5, 0.2, 0])
        ax = A.ax
        ccp = polyline(ax, ps, d["cov_cp"], CIC, 3)
        cw = polyline(ax, ps, d["cov_wald"], REJC, 3)
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=GREY_B, stroke_width=2)
        cw_min = float(np.min(d["cov_wald"]))
        side = fit_rows(VGroup(
            label(r"gold: \ Clopper--Pearson, \ inverted exact tests", font_size=22, color=CIC),
            label(rf"globally $\ge95\%$; \ displayed-grid min {100 * float(np.min(d['cov_cp'])):.1f}\%", font_size=22, color=CIC),
            label(r"red: \ Wald, \ $\hat p \pm 1.96\sqrt{\hat p(1 - \hat p)/n}$", font_size=22, color=REJC),
            label(rf"fails uniform 95\% level; \ displayed coverage down to {100 * cw_min:.0f}\%", font_size=22, color=REJC),
            label(r"the sawtooth: \ discreteness, \ as in Part 11", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The exact binomial coverage evaluated on the displayed parameter grid: <bookmark mark='b'/> never below ninety-five percent, as the construction guarantees, with the sawtooth of a discrete distribution. <bookmark mark='c'/> Against it, the Wald interval, estimate plus or minus 1.96 standard errors, <bookmark mark='d'/> whose induced tests do not maintain the claimed level uniformly, and whose coverage falls to {100 * cw_min:.0f} percent near the edges. <bookmark mark='e'/> Part eleven met these curves; here is the reason. Uniform coverage and uniformly valid induced tests are equivalent. The parameter grid illustrates this equivalence; its observed minimum is not a proof of a global numerical minimum."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(exact_tag(r"exact coverage functions")))
            vo.wait_until("a")
            self.play(Create(ccp), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cw), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def uma(self):
        rows = [
            cmath(r"C \text{ uniformly most accurate}", r":", r"P_\theta(\theta' \in C(X)) \text{ minimal for every false } \theta'", font_size=30),
            cmath(r"\text{invert UMP tests}", r"\Rightarrow", r"\text{UMA bounds; \ e.g.\ the upper bound } \bar p(x)", font_size=32),
            cmath(r"\text{invert UMPU tests}", r"\Rightarrow", r"\text{UMA \emph{unbiased} sets: \ } P_\theta(\theta' \in C) \le 1 - \alpha", font_size=30),
            cmath(r"\text{the } t \text{ interval}", r":", r"\text{UMA unbiased, \ from chapter 3's } t \text{ test}", font_size=32),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"Neyman's accuracy"), why(r"one-sided"), why(r"two-sided"), why(r"optimality transferred")]
        with self.voiceover(
            "<bookmark mark='a'/> What makes an interval good? Neyman's answer: it should rarely contain false "
            "values. A confidence set is uniformly most accurate if, at every true theta, its chance of covering each"
            " false value is as small as possible. <bookmark mark='b'/> Inverting uniformly most powerful tests gives"
            " uniformly most accurate bounds, including randomized exact upper bounds for a proportion. The usual "
            "nonrandomized Clopper–Pearson bound is conservative and does not automatically inherit strict UMA "
            "optimality among randomized procedures. <bookmark mark='c'/> Inverting UMPU tests gives the most "
            "accurate among unbiased sets, those that cover any false value with probability no more than one minus "
            "alpha. <bookmark mark='d'/> The t interval is one: chapter three's optimality, transferred."
        ) as vo:
            heading=label('Optimal false-coverage probabilities follow from optimal tests',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pratt(self):
        rows = [
            cmath(r"E_\theta\, \mathrm{length}(C(X))", r"=", r"E_\theta \textstyle\int \mathbf 1\{\theta' \in C(X)\}\, d\theta'", font_size=32),
            cmath(r"\phantom{E}", r"=", r"\textstyle\int P_\theta(\theta' \in C(X))\, d\theta'", font_size=32),
            cmath(r"\text{minimize false coverage}", r"\Rightarrow", r"\text{minimize expected length}", font_size=32),
            cmath(r"\text{but}", r":", r"\text{the expected length can be infinite \ (chapter 7)}", font_size=32),
        ]
        rows[2][-1].set_color(UMPC)
        rows[3][-1].set_color(REJC)
        whys = [why(r"length as an integral"), why(r"Tonelli: \ nonnegative integrands"), why(r"Pratt (1961)"), why(r"Fieller")]
        with self.voiceover(
            "<bookmark mark='a'/> John Pratt noticed in 1961 that integrated false coverage determines expected "
            "length. The length of a set is the integral of the indicator that each theta prime lies in it. <bookmark"
            " mark='b'/> Taking expectations and exchanging the nonnegative integrals by Tonelli, even when the "
            "answer is infinite, the expected length is the integral of the probabilities of covering each theta "
            "prime. <bookmark mark='c'/> So the most accurate sets, which make those probabilities small for false "
            "values, also have the smallest expected length. <bookmark mark='d'/> But some problems force the "
            "expected length to be infinite, for every valid procedure. That is the next chapter."
        ) as vo:
            heading=label('Tonelli integrates false coverage into expected length',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
