from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Brown(VoiceoverScene):
    def construct(self):
        self.card()
        self.tweedie()
        self.theorem()
        self.integrals()
        self.hitting()
        self.intuition()
        self.priors()

    def card(self):
        card = chapter_card(11, r"Why three dimensions", r"Admissibility and the recurrence of Brownian motion", lit=(1971,), part=PART)
        with self.voiceover("Chapter eleven. Why three dimensions: admissibility and the recurrence of Brownian motion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def tweedie(self):
        rows = [
            cmath(r"m(x)", r"=", r"\textstyle\int \phi_p(x - \theta)\, \pi(d\theta): \ \text{the marginal}", font_size=34),
            cmath(r"\delta_\pi(x)", r"=", r"E_\pi[\theta \mid x] = x + \nabla \log m(x)", font_size=36),
            cmath(r"\text{flat } \pi", r"\Rightarrow", r"m \equiv 1, \ \ \delta_\pi(x) = x", font_size=34),
            cmath(r"\text{risk}", r"=", r"p - E\big[\|\nabla \log m\|^2 - 2\Delta m / m\big] \ \ \text{(SURE)}", font_size=32),
        ]
        rows[1][-1].set_color(BAYESC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"prior $\ast$ noise"), why(r"Tweedie's formula"), why(r"the obvious estimator"), why(r"chapter 10, \ with $g = \nabla \log m$")]
        with self.voiceover(
            "<bookmark mark='a'/> Why should the dimension three matter? Lawrence Brown's answer of 1971 starts from "
            "generalized Bayes rules. A prior, possibly improper, convolved with the normal noise gives the marginal density "
            "of the data, m. <bookmark mark='b'/> The posterior mean is x plus the gradient of log m: Tweedie's formula, "
            "which Robbins credited to Maurice Tweedie. <bookmark mark='c'/> The flat prior has constant marginal, so its "
            "generalized Bayes rule is x itself. <bookmark mark='d'/> And chapter ten's SURE, with g equal to the gradient "
            "of log m, shows that the risk is p minus an expectation that involves the Laplacian of m: the analysis of "
            "estimators has become potential theory."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = fit_rows(VGroup(
            label(r"Brown (1971): \ the generalized Bayes rule $\delta_\pi$ is admissible", font_size=28, color=ADMC),
            label(r"if and only if \ (essentially) \ the diffusion $dY = \nabla \log m(Y)\, dt + dB$ is recurrent", font_size=26),
            label(r"for spherical $m$: \ \ admissible \ $\iff \ \displaystyle\int^\infty \frac{dr}{r^{p - 1}\, m(r)} = \infty$", font_size=28, color=S.ACCENT),
            label(r"flat prior, \ $m \equiv 1$: \ \ $\int^\infty r^{1 - p}\, dr = \infty \iff p \le 2$", font_size=28, color=MMC),
            label(r"$X$ is admissible exactly when Brownian motion is recurrent", font_size=28, color=JSC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Brown's theorem. The generalized Bayes rule for a prior is admissible <bookmark "
            "mark='b'/> if and only if, essentially, the diffusion that moves like Brownian motion pushed along the gradient "
            "of log m is recurrent: it keeps coming back to every ball. <bookmark mark='c'/> When the marginal is "
            "spherically symmetric, the condition becomes an integral test: the integral of one over r to the p minus one "
            "times m of r must diverge. <bookmark mark='d'/> For the flat prior, m is constant and the integral of r to the "
            "one minus p diverges exactly when p is at most two. <bookmark mark='e'/> So X is admissible exactly in the "
            "dimensions where Brownian motion is recurrent: one and two. Stein's paradox in three dimensions is Pólya's "
            "transience in three dimensions."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def integrals(self):
        d = load("brown")
        R = np.asarray(d["R"])
        lr = np.log10(R)
        A = axes([0, 6], [0, 6], x_length=7.4, y_length=4.4, xlabel=r"$\log_{10} R$", ylabel=r"$\int_1^R r^{1 - p}\, dr$",
                 xticks=[0, 2, 4, 6], yticks=[0, 2, 4, 6], center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = clip_curve(ax, lr, d["int1"], INADC, 4, ymax=6)
        c2 = clip_curve(ax, lr, d["int2"], MMC, 4, ymax=6)
        c3 = polyline(ax, lr, d["int3"], JSC, 4)
        lim = DashedLine(ax.c2p(0, 1), ax.c2p(6, 1), color=JSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"red: \ $p = 1$: \ $R - 1$, \ diverges fast", font_size=22, color=INADC),
            label(r"gold: \ $p = 2$: \ $\log R$, \ diverges, \ barely", font_size=22, color=MMC),
            label(r"green: \ $p = 3$: \ $1 - 1/R \to 1$, \ converges", font_size=22, color=JSC),
            label(r"$p = 2$: \ $X$ admissible, \ but only just", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The integral test, drawn against the log of the upper limit R. In one dimension, R minus "
            "one: it diverges quickly. <bookmark mark='b'/> In two, the log of R: it diverges, but only logarithmically. "
            "<bookmark mark='c'/> In three, one minus one over R, which converges to one. <bookmark mark='d'/> Two dimensions "
            "is the borderline: X is admissible there, but only just, which is why James and Stein need p minus two, and why "
            "the paradox starts at three."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact integrals")))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c3), Create(lim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def hitting(self):
        d = load("brown")
        R = np.asarray(d["R"])
        k = R > 2.05
        lr = np.log10(R[k])
        A = axes([0.3, 6], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$\log_{10} R$", ylabel=r"$P(\text{hit the unit ball before radius } R)$",
                 xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        h1 = polyline(ax, lr, np.asarray(d["hit1"])[k], INADC, 4)
        h2 = polyline(ax, lr, np.asarray(d["hit2"])[k], MMC, 4)
        h3 = polyline(ax, lr, np.asarray(d["hit3"])[k], JSC, 4)
        half = DashedLine(ax.c2p(0.3, 0.5), ax.c2p(6, 0.5), color=JSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"Brownian motion started at radius 2", font_size=22),
            label(r"$p = 1$: \ $(R - 2)/(R - 1) \to 1$", font_size=22, color=INADC),
            label(r"$p = 2$: \ $\log(R/2)/\log R \to 1$, \ slowly", font_size=22, color=MMC),
            label(r"$p = 3$: \ $\to 2^{2 - p} = \tfrac12$: \ half the paths never return", font_size=22, color=JSC),
            label(r"Part 44's walks: \ returns 0.987, \ 0.713, \ 0.327", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same dichotomy for Brownian motion itself. Start it at distance two from the origin "
            "and ask whether it reaches the unit ball before wandering out to radius R. <bookmark mark='b'/> In one "
            "dimension, almost surely, as R grows. <bookmark mark='c'/> In two, also almost surely in the limit, though the "
            "probability creeps up like a ratio of logarithms. <bookmark mark='d'/> In three, it tends to one half: half "
            "the paths escape to infinity and never come back. <bookmark mark='e'/> Part forty-four saw the same thing for "
            "random walks: within ten thousand steps they had returned to the origin with probability point nine nine, "
            "point seven one and point three three in one, two and three dimensions."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ harmonic functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(h1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(h2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(h3), Create(half), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def intuition(self):
        rows = [
            cmath(r"\text{Blyth}", r":", r"\text{improve on } \delta \text{ near 0, \ pay in Bayes risk far away}", font_size=32),
            cmath(r"\text{gap}", r":", r"r(\pi_\tau, \delta) - r(\pi_\tau, \delta_\tau) \to 0", font_size=34),
            cmath(r"\text{cost of escaping}", r":", r"\text{the capacity of a ball in } \mathbb R^p: \ 0 \text{ for } p \le 2, \ > 0 \text{ for } p \ge 3", font_size=30),
            cmath(r"p \ge 3", r":", r"\text{a rival can push risk out to } \infty \text{ for free: \ shrinkage}", font_size=32),
        ]
        rows[2][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(JSC)
        whys = [why(r"chapter 3's race"), why(r"wide priors"), why(r"potential theory"), why(r"transience")]
        with self.voiceover(
            "<bookmark mark='a'/> Why should recurrence be the criterion? Recall chapter three's race. To beat X, a rival "
            "must improve somewhere and is pinned down by Bayes risks under wider and wider priors. <bookmark mark='b'/> "
            "The gap between X and the best Bayes rule closes as the priors widen. <bookmark mark='c'/> Whether a rival can "
            "slip through the gap is measured by a quantity from potential theory, the capacity of a ball: how much "
            "charge it takes to hold it at unit potential against infinity. It is zero in one and two dimensions, positive "
            "in three or more. <bookmark mark='d'/> In three or more, a rival can move risk away from the origin and lose it "
            "at infinity at no cost, and shrinkage toward a point does exactly that. The space is too big for X to be "
            "admissible."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def priors(self):
        rows = [[r"prior $\pi(\theta)$", r"tail of $m(r)$", r"$\int^\infty \frac{dr}{r^{p-1} m(r)}$", r"generalized Bayes rule"],
                [r"flat", r"$1$", r"$= \infty$ iff $p \le 2$", r"$X$: \ admissible iff $p \le 2$"],
                [r"$\|\theta\|^{-k}$, \ $k < p$", r"$\sim r^{-k}$", r"$= \infty$ iff $k \ge p - 2$", r"admissible iff $k \ge p - 2$"],
                [r"$\|\theta\|^{2 - p}$ \ (harmonic)", r"$\sim r^{2 - p}$", r"$= \infty$", r"admissible and minimax \ (Stein 1981)"],
                [r"any proper prior", r"integrable", r"$= \infty$", r"admissible \ (unique Bayes)"]]
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.32, colors=[GREY_A, INADC, MMC, JSC, ADMC]).move_to([0, 0.5, 0])
        if tab.width > 13:
            tab.width = 13
        note_ = label(r"the heavier the prior's tails, \ the closer to $X$; \ just light enough, \ and the rule is admissible", font_size=24, color=S.ACCENT).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The test sorts priors by their tails. <bookmark mark='b'/> The flat prior gives X, "
            "admissible only up to two dimensions. <bookmark mark='c'/> A prior falling like the norm of theta to the minus "
            "k gives a marginal with the same tail, and the integral diverges exactly when k is at least p minus two. "
            "<bookmark mark='d'/> The borderline case, k equal to p minus two, is the harmonic prior, whose generalized Bayes "
            "rule Stein showed in 1981 to be both admissible and minimax. <bookmark mark='e'/> And proper priors always pass, "
            "as chapter three proved directly. <bookmark mark='f'/> The heavier the prior's tails, the closer its rule is to "
            "X; just light enough, and the rule becomes admissible."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            vo.wait_until("f")
            self.play(FadeIn(note_))
        self.clear_scene()
