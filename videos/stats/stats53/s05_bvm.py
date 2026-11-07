from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class BvM(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.proof()
        self.chart()
        self.merge()
        self.dimension()
        self.meaning()

    def card(self):
        card = chapter_card(4, r"Bernstein--von Mises", r"When a posterior is a confidence distribution", part=PART)
        with self.voiceover("Chapter four. Bernstein–von Mises: when a posterior is a confidence distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\text{a smooth parametric model}", r":", r"\text{interior LAN, nonsingular }I_{\theta_0},\ \text{root-}n\text{ localization}", font_size=32),
            cmath(r"\text{a prior}", r":", r"\text{continuous and positive at } \theta_0", font_size=34),
            cmath(r"\big\|\Pi(\cdot \mid X_{1:n}) - N\big(\hat\theta_n, (nI_{\theta_0})^{-1}\big)\big\|_{TV}", r"\to", r"0 \ \text{ in } P_{\theta_0}\text{-probability}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{credible sets are asymptotic confidence sets}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BALLC)
        whys = [why(r"Part 47"), why(r"any reasonable prior"), why(r"Le Cam's form (1953, 1986)"), why(r"the bridge")]
        heading = label('Posterior convergence requires both local and global model conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem that reconciles Bayesians and frequentists, for parametric models. Take a model that is locally asymptotically normal at the truth, in the sense of Part forty-seven, <bookmark mark='b'/> with nonsingular interior information, posterior localization at the root-n scale, and a prior density continuous and positive there. <bookmark mark='c'/> Then the posterior, in total variation, approaches a normal distribution centred at an efficient estimator with the inverse Fisher information over n as its variance. Sergei Bernstein and Richard von Mises had versions early in the century; Lucien Le Cam gave the modern one. <bookmark mark='d'/> Regular quantile intervals and corresponding ellipsoids then have pointwise asymptotic coverage. Uniform honesty over a class needs additional uniform assumptions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"h = \sqrt n(\theta - \theta_0)", r":", r"\text{the local parameter}", font_size=34),
            cmath(r"\log \frac{p_{\theta_0 + h/\sqrt n}}{p_{\theta_0}}(X)", r"=", r"h^\top \Delta_n - \tfrac12 h^\top I h + o_P(1)", font_size=32),
            cmath(r"\pi(h \mid X)", r"\propto", r"\pi(\theta_0 + h/\sqrt n)\, e^{h^\top\Delta_n - \frac12 h^\top I h} \approx \pi(\theta_0)\, N(I^{-1}\Delta_n, I^{-1})", font_size=30),
            cmath(r"\text{plus}", r":", r"\text{tests to rule out } |h| \to \infty \ \ \text{(Schwartz again)}", font_size=34),
        ]
        rows[2][-1].set_color(POSTC)
        whys = [why(r"zoom in at rate $\sqrt n$"), why(r"LAN, \ Part 47"), why(r"the prior flattens out"), why(r"the tails")]
        heading = label('LAN and posterior localization yield a local Gaussian approximation', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The proof, in three moves. Zoom in at the root-n scale, with the local parameter h. "
            "<bookmark mark='b'/> By local asymptotic normality, the log-likelihood ratio is a quadratic in h, plus a "
            "negligible remainder. <bookmark mark='c'/> So the posterior density of h is the prior, evaluated at points "
            "converging to theta zero and hence nearly constant, times the exponential of a quadratic: a normal distribution "
            "centred at I inverse times the score. <bookmark mark='d'/> The last step uses tests, as in Schwartz's theorem, to "
            "show the posterior puts vanishing mass far from the truth, so the local picture is the whole picture."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("bvm")
        ln = np.log10(d["ns"])
        A = axes([0.9, 4.1], [-2.8, 0.1], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ TV(posterior, normal)",
                 xticks=[1, 2, 3, 4], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-2.5, -2, -1.5, -1, -0.5, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cs = {p: VGroup(polyline(ax, ln, np.log10(v), c, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(ln, np.log10(v))])
              for (p, v), c in zip(d["tv"].items(), (POSTC, BADC))}
        ref = DashedLine(ax.c2p(1, np.log10(d["tv"]["0.3"][0])), ax.c2p(4, np.log10(d["tv"]["0.3"][0]) - 1.5), color=TRUTHC, stroke_width=2)
        slope = float(np.polyfit(ln[2:], np.log10(d["tv"]["0.3"][2:]), 1)[0])
        t = d["tv"]
        side = fit_rows(VGroup(
            label(r"rounded counts $k\approx np$, \ not a data-averaged TV curve", font_size=22),
            label(rf"blue: \ $p = 0.3$: \ {t['0.3'][0]:.3f} at $n = 10$, \ {t['0.3'][-1]:.4f} at $10^4$", font_size=22, color=POSTC),
            label(rf"slope {slope:.2f}: \ the TV error is of order $n^{{-1/2}}$ \ (white)", font_size=22, color=TRUTHC),
            label(rf"red: \ $p = 0.02$: \ slower, \ {t['0.02'][-1]:.3f} at $10^4$", font_size=22, color=BADC),
            label(r"near the boundary, \ the normal arrives late", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The theorem made visible. Coin flips with a uniform prior, so the posterior is a Beta, compared by exact integration with the normal centred at the sample proportion. <bookmark mark='b'/> For a probability of point three, the total variation distance falls from {say(t['0.3'][0], 3)} at ten flips to {say(t['0.3'][-1], 4)} at ten thousand. <bookmark mark='c'/> The slope is {say(slope, 2)}: the error is of order one over root n, the white reference. <bookmark mark='d'/> The plotted counts are rounded n times the reference probability, rather than averages over data. At zero successes the MLE normal is a point mass and its total variation from the continuous Beta is exactly one. For the interior counts at reference probability two percent the approach is slower, {say(t['0.02'][-1], 3)} even at ten thousand. <bookmark mark='e'/> Near the edge of the parameter space the posterior stays skewed, and so do the frequentist pivots of Part eleven."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact, \ by quadrature")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["0.3"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ref), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["0.02"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def merge(self):
        d = load("bvm")
        rows = [[r"$n$"] + [f"{n:,}" for n in d["ns"]],
                [r"TV(Beta(1, 1) posterior, \ Beta(20, 2) posterior)"] + [f"{v:.3f}" for v in d["merge"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.5, row_buff=0.45, colors=[GREY_B, POSTC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.8, 0])
        foot = label(r"two priors, \ one flat and one confidently wrong (mean 0.91 for a truth of 0.3), \ merge", font_size=24, color=GREY_A).move_to([0, -0.6, 0])
        foot2 = label(r"but slowly: \ the prior washes out at rate $1/\sqrt n$ \ times how wrong it was", font_size=24, color=BALLC).move_to([0, -1.4, 0])
        m = d["merge"]
        with self.voiceover(
            f"<bookmark mark='a'/> The theorem's other face: the prior washes out. Two analysts see the same coin flips, one "
            f"with a flat prior and one with a confident prior centred at point nine one, for a truth of point three. "
            f"<bookmark mark='b'/> The total variation between their posteriors is {say(m[0], 2)} at ten flips and "
            f"{say(m[-1], 2)} at ten thousand: they merge, as Bernstein–von Mises promises. <bookmark mark='c'/> But slowly. "
            f"A prior worth twenty pseudo-observations needs many times that many real ones before its influence disappears."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"one simulated sequence; \ exact posteriors")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def dimension(self):
        rows = [
            cmath(r"p \text{ growing with } n", r":", r"\text{does BvM survive?}", font_size=36),
            cmath(r"\text{exponential families}", r":", r"\text{dimension, derivative, information and prior conditions matter}", font_size=34),
            cmath(r"\text{linear regression}", r":", r"\text{known variance, flat prior: exact Gaussian if full rank and }p<n", font_size=32),
            cmath(r"p/n \to \gamma > 0", r":", r"\text{model-specific; not a universal BvM failure}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"high-dimensional parametric"), why(r"Ghosal (1999, 2000)"), why(r"Bontemps (2011)"), why(r"proportional asymptotics")]
        heading = label('Growing-dimensional normal approximation is model and prior dependent', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Does the theorem survive when the number of parameters grows with the sample? <bookmark mark='b'/> For particular growing-dimensional exponential families and priors, sufficient dimension bounds depend on likelihood derivatives, information and prior concentration; a power of p over n alone is not a universal theorem. <bookmark mark='c'/> In Gaussian linear regression, Bontemps obtained prior- and design-dependent bounds. With known variance and a flat prior, the conditional coefficient posterior is exactly Gaussian for any full-rank p less than n. <bookmark mark='d'/> Proportional dimension requires a model-specific analysis. It does not by itself imply that every posterior has the wrong shape or location."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"what BvM does and does not say:", font_size=28, color=GREY_A),
            label(r"it does: \ regular credible intervals: \ pointwise asymptotic coverage", font_size=26, color=GOODC),
            label(r"it does not: \ cover small $n$, \ boundaries, \ or $p$ growing with $n$", font_size=26, color=BADC),
            label(r"nor misspecified models: \ the variance is then wrong (chapter 11)", font_size=26, color=BADC),
            label(r"nor infinite-dimensional ones: \ there it can fail outright (chapter 5)", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What the theorem does and does not say. <bookmark mark='b'/> It does say that credible regular intervals for smooth finite-dimensional parameters have pointwise asymptotic coverage under the stated assumptions. <bookmark mark='c'/> It says nothing about small samples, parameters near a boundary, or dimensions that grow with n. <bookmark mark='d'/> Nor about misspecified models, where, as chapter eleven shows, the posterior's spread is wrong. <bookmark mark='e'/> And in infinite-dimensional models, the next chapter shows, it can fail outright."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
