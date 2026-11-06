from __future__ import annotations

import numpy as np

from videos.stats.stats57.common import *  # noqa: F403


class Impossible(VoiceoverScene):
    def construct(self):
        self.card()
        self.conditional()
        self.local_chart()
        self.theorem()
        self.bins()
        self.bins_worked()
        self.relaxed()
        self.functionals()

    def card(self):
        card = chapter_card(3, r"Impossibility", r"What no distribution-free method can do", lit=(2014,), part=PART)
        with self.voiceover("Chapter three. Impossibility: what no distribution-free method can do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def conditional(self):
        rows = [
            cmath(r"\text{marginal}", r":", r"P\big(Y_{n+1} \in C(X_{n+1})\big) \ge 1 - \alpha: \ \text{on average over } x", font_size=34),
            cmath(r"\text{conditional}", r":", r"P\big(Y_{n+1} \in C(x) \mid X_{n+1} = x\big) \ge 1 - \alpha \ \text{ for every } x", font_size=34),
            cmath(r"\text{the gap}", r":", r"\text{marginal coverage can hide a subgroup covered half the time}", font_size=32),
            cmath(r"\text{wanted}", r":", r"\text{conditional coverage, \ distribution-free}", font_size=36),
        ]
        rows[1][-1].set_color(TESTPT)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"what the lemma gives"), why(r"what a patient wants"), why(r"the next chart"), why(r"the obvious goal")]
        with self.voiceover(
            "<bookmark mark='a'/> The lemma's guarantee is marginal: coverage on average over the test point's features. "
            "<bookmark mark='b'/> What a patient wants is conditional coverage: given my features, the interval covers my "
            "outcome with probability one minus alpha. <bookmark mark='c'/> The two can be very different: marginal coverage of "
            "ninety percent can hide a subgroup covered half the time. <bookmark mark='d'/> So the obvious goal is conditional "
            "coverage, with no assumptions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def local_chart(self):
        d = load("local")
        mid = np.asarray(d["mid"])
        A = axes([0, 1], [0.5, 1.02], x_length=7.4, y_length=4.4, xlabel=r"$x$ \ (noise SD grows from 0.1 to 1.3)", ylabel=r"coverage within the bin",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.5, 0.75, 0.9, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.9), ax.c2p(1, 0.9), color=GREY_B, stroke_width=2)
        cp = VGroup(polyline(ax, mid, d["plain"], MISSC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=MISSC) for a, b in zip(mid, d["plain"])])
        cs = VGroup(polyline(ax, mid, d["scaled"], COVC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=COVC) for a, b in zip(mid, d["scaled"])])
        side = fit_rows(VGroup(
            label(r"heteroscedastic regression, \ 2,000 test points", font_size=22),
            label(rf"red: \ split conformal, \ absolute residuals: \ {100 * d['marg_plain']:.1f}\% overall", font_size=22, color=MISSC),
            label(rf"100\% where the noise is small, \ {100 * d['plain'][-1]:.0f}\% where it is large", font_size=22, color=MISSC),
            label(rf"green: \ residuals divided by a fitted spread: \ {100 * d['marg_scaled']:.1f}\%", font_size=22, color=COVC),
            label(r"better, \ but only because the spread model is right", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> An example: a regression whose noise grows across the range of x. <bookmark mark='b'/> Split "
            f"conformal with absolute residuals covers {100 * d['marg_plain']:.1f} percent overall, as promised. <bookmark "
            f"mark='c'/> But it covers everyone where the noise is small, and only {100 * d['plain'][-1]:.0f} percent where it is "
            f"large. <bookmark mark='d'/> Dividing the residuals by a fitted spread evens it out, with "
            f"{100 * d['marg_scaled']:.1f} percent overall and every bin close to ninety. <bookmark mark='e'/> But that works "
            f"only because the spread model happens to be right, which is an assumption."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\text{if } C \text{ has conditional coverage}", r":", r"\text{for every } P \text{ and every non-atom } x", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"E\,\mathrm{Leb}\big(C(x)\big) = \infty \ \text{ for almost every such } x", font_size=34),
            cmath(r"\text{idea}", r":", r"\text{near } x \text{ there is almost no data: \ any law can be hidden there}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{exact conditional coverage forces infinite intervals}", font_size=34),
        ]
        rows[1][-1].set_color(MISSC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"distribution-free"), why(r"Vovk (2012); \ Lei \& Wasserman (2014)"), why(r"Bahadur--Savage, \ locally"), why(r"the impossibility")]
        with self.voiceover(
            "<bookmark mark='a'/> And the impossibility. Suppose a procedure has conditional coverage for every distribution, at "
            "every point x that is not an atom. <bookmark mark='b'/> Vladimir Vovk, and Jing Lei and Larry Wasserman, proved "
            "that its intervals must then have infinite expected length at almost every such point. <bookmark mark='c'/> The "
            "idea is Bahadur and Savage again, locally: near a non-atom there are almost no data, so any conditional law can be "
            "hidden there. <bookmark mark='d'/> Exact conditional coverage, distribution-free, forces infinite intervals."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bins(self):
        rows = [
            cmath(r"\text{local conformal}", r":", r"\text{calibrate within bins or neighbourhoods of } x", font_size=34),
            cmath(r"\text{gives}", r":", r"\text{coverage within each bin, \ exactly}", font_size=36),
            cmath(r"\text{as bins shrink}", r":", r"\text{fewer calibration points: \ wider, \ eventually infinite}", font_size=34),
            cmath(r"\text{the trade}", r":", r"\text{resolution in } x \text{ against interval length}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"Lei \& Wasserman (2014)"), why(r"Mondrian by bins"), why(r"the theorem, \ in practice"), why(r"bias against variance, \ again")]
        with self.voiceover(
            "<bookmark mark='a'/> The practical response is local conformal prediction: calibrate within bins, or "
            "neighbourhoods, of x. <bookmark mark='b'/> That gives exact coverage within each bin. <bookmark "
            "mark='c'/> But as the bins shrink, each holds fewer calibration points, the inflated quantile grows, and "
            "in the limit the intervals become infinite, exactly as the theorem says. <bookmark mark='d'/> Resolution "
            "in x trades against interval length: the old bias–variance trade-off in a new form."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bins_worked(self):
        rows = [
            cmath(r"n = 1{,}200, \ 10 \text{ bins}", r":", r"120 \text{ each: \ } k = 109 \text{ of } 120", font_size=36),
            cmath(r"100 \text{ bins}", r":", r"12 \text{ each: \ } k = 12 \text{ of } 12, \ \text{the largest score}", font_size=36),
            cmath(r"200 \text{ bins}", r":", r"6 \text{ each: \ } k = 7 > 6: \ \text{the whole line}", font_size=36),
            cmath(r"\text{so}", r":", r"\text{resolution is bounded by } n\alpha/(1 - \alpha)", font_size=36),
        ]
        rows[1][-1].set_color(WEIGHTC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"fine"), why(r"already the extreme"), why(r"infinite intervals"), why(r"about 133 bins here")]
        with self.voiceover(
            "<bookmark mark='a'/> In numbers: twelve hundred calibration points in ten bins leave a hundred and twenty "
            "in each, and the threshold is the hundred-and-ninth of them. <bookmark mark='b'/> With a hundred bins, "
            "twelve in each, the threshold is already the largest score in the bin. <bookmark mark='c'/> With two "
            "hundred bins, six in each, k would be seven, and every interval is the whole line. <bookmark mark='d'/> "
            "So the number of bins can be at most about n alpha over one minus alpha, a hundred and thirty-three here, "
            "before the intervals become infinite: the impossibility theorem, counted."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def relaxed(self):
        rows = [
            cmath(r"\text{approximately}", r":", r"\text{coverage over every set of probability} \ge \delta: \ \text{still hard}", font_size=34),
            cmath(r"\text{Barber et al. (2021)}", r":", r"\text{length lower bounds for that relaxation}", font_size=34),
            cmath(r"\text{what is possible}", r":", r"\text{coverage over a chosen finite family of groups or shifts}", font_size=34),
            cmath(r"\text{next}", r":", r"\text{Gibbs, \ Cherian \& Cand\`es: \ conditional over a function class}", font_size=32),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"a weaker target"), why(r"Foygel Barber, \ Cand\`es, \ Ramdas \& Tibshirani"), why(r"Mondrian, \ chapter 9"), why(r"chapter 4")]
        with self.voiceover(
            "<bookmark mark='a'/> A relaxation asks for coverage over every subset of feature space with probability at least "
            "delta. <bookmark mark='b'/> Barber, Candès, Ramdas and Tibshirani proved lower bounds on the length of any interval "
            "achieving that, too. <bookmark mark='c'/> What is possible is coverage over a chosen, finite family of groups or "
            "shifts: the Mondrian idea of chapter nine. <bookmark mark='d'/> And the next chapter's generalization, from Isaac "
            "Gibbs, John Cherian and Candès, gives exact coverage over a whole function class."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def functionals(self):
        rows = [
            cmath(r"\text{binary } Y", r":", r"\text{a confidence interval for } P(Y = 1 \mid X = x)", font_size=36),
            cmath(r"\text{distribution-free}", r"\Rightarrow", r"\text{its length cannot shrink to } 0 \text{ unless } X \text{ has atoms}", font_size=32),
            cmath(r"\text{in general}", r":", r"\text{regression functions, \ means, \ quantiles of } P: \ \text{need assumptions}", font_size=32),
            cmath(r"\text{the boundary}", r":", r"\text{predict an observable, \ distribution-free; \ estimate a parameter, \ not}", font_size=30),
        ]
        rows[1][-1].set_color(MISSC)
        rows[3][-1].set_color(TESTPT)
        whys = [why(r"Barber (2020)"), why(r"another impossibility"), why(r"Bahadur--Savage's family"), why(r"the lesson of the part")]
        with self.voiceover(
            "<bookmark mark='a'/> Functionals of the distribution are worse. For a binary outcome, consider a confidence "
            "interval for the conditional probability that Y is one, given X equals x. <bookmark mark='b'/> Rina Foygel Barber "
            "proved in 2020 that without assumptions its length cannot shrink to zero, however much data there is, unless X has "
            "atoms. <bookmark mark='c'/> Regression functions, means and quantiles of P all need assumptions. <bookmark "
            "mark='d'/> That is the boundary: distribution-free methods predict observables; parameters of the distribution "
            "require assumptions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
