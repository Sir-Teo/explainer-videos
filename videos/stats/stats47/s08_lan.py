from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class LAN(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.limit()
        self.chart()
        self.scoretest()
        self.qmd()

    def card(self):
        card = chapter_card(7, r"Local asymptotic normality", r"Every regular model, \ seen up close, \ is one Gaussian observation", lit=(1960,), part=PART)
        with self.voiceover("Chapter seven. Local asymptotic normality: every regular model, seen up close, is one Gaussian observation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\Lambda_n(h)", r"=", r"\log \prod_i \frac{p_{\theta + h/\sqrt n}(X_i)}{p_\theta(X_i)}", font_size=36),
            cmath(r"\Lambda_n(h)", r"=", r"h^\top \Delta_n - \tfrac12 h^\top I_\theta h + o_P(1)", font_size=36),
            cmath(r"\Delta_n", r"=", r"\tfrac{1}{\sqrt n}\textstyle\sum_i \dot\ell_\theta(X_i) \Rightarrow N(0, I_\theta)", font_size=34),
            cmath(r"\text{the same as}", r":", r"\log \frac{dN(h, I^{-1})}{dN(0, I^{-1})}(Y) = h^\top I Y - \tfrac12 h^\top I h", font_size=30),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"local alternatives $\theta + h/\sqrt n$"), why(r"Le Cam (1960)"), why(r"the normalized score"), why(r"one observation $Y \sim N(h, I^{-1})$")]
        with self.voiceover(
            "<bookmark mark='a'/> Lucien Le Cam's idea of 1960. Fix theta and look at alternatives h over root n away. The "
            "log-likelihood ratio between them is a random function of h. <bookmark mark='b'/> In regular models it is, up "
            "to a negligible error, a linear term in h minus half a quadratic term with the Fisher information. <bookmark "
            "mark='c'/> The linear coefficient is the normalized score, asymptotically normal with variance I. <bookmark "
            "mark='d'/> And that is exactly the log-likelihood ratio of a single Gaussian observation with mean h and "
            "variance the inverse information. Locally, every regular model looks like one normal observation of the "
            "local parameter."
        ) as vo:
            heading=label('LAN approximates fixed local likelihood ratios quadratically',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def limit(self):
        rows = fit_rows(VGroup(
            label(r"Le Cam: \ the local experiments $\{P^n_{\theta + h/\sqrt n} : h \in \mathbb R^k\}$", font_size=26),
            label(r"converge to the Gaussian shift experiment $\{N(h, I_\theta^{-1}) : h \in \mathbb R^k\}$", font_size=26, color=GOODC),
            label(r"finite local parameter sets: \ weak experiment convergence; \ stronger uniform claims need more", font_size=26, color=S.ACCENT),
            label(r"and nothing more: \ the Gaussian problem's limits are the model's limits", font_size=26, color=HODC),
            label(r"local decision bounds transfer for suitable losses and regular experiments", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Le Cam's theorem says more than a statement about likelihood ratios. On each fixed "
            "finite set of local parameters, convergence of the joint likelihood ratios gives weak convergence of the"
            " local experiments. Stronger uniform statements on compact sets require corresponding uniform LAN and "
            "tightness assumptions. The local models <bookmark mark='b'/> converges, as a statistical experiment, to "
            "the Gaussian shift: one normal observation with unknown mean h and known variance. <bookmark mark='c'/> "
            "For suitable bounded continuous loss and local decision problems, limits and lower bounds can be "
            "transferred to the Gaussian experiment, <bookmark mark='d'/> and nothing more. <bookmark mark='e'/> So "
            "many regular local questions reduce to Gaussian decision problems. That reduction is local and subject "
            "to loss and convergence conditions; it is not a global equivalence for every parameter value and action."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def chart(self):
        d = load("lan")
        e = np.asarray(d["edges"])
        A = axes([-5, 3], [0, 0.5], x_length=7.4, y_length=4.4, xlabel=r"$\Lambda_n(h)$, \ Cauchy location, \ $h = 1.5$", ylabel=r"density",
                 xticks=[-4, -2, 0, 2], yticks=[0, 0.2, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        h25 = hist_bars(ax, e, d["25"]["hist"], color=HODC, opacity=0.4)
        h400 = hist_bars(ax, e, d["400"]["hist"], color=MLEC, opacity=0.6)
        u = np.linspace(-5, 3, 300)
        m, v = d["lan_mean"], d["lan_var"]
        nc = polyline(ax, u, np.exp(-(u - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v), LIMC, 4)
        side = fit_rows(VGroup(
            label(r"Cauchy: \ $I = 1/2$; \ LAN: \ $N(-h^2 I/2, \ h^2 I)$", font_size=22),
            label(rf"red: \ $n = 25$: \ mean {d['25']['mean']:.3f}, \ variance {d['25']['var']:.3f}", font_size=22, color=HODC),
            label(rf"blue: \ $n = 400$: \ mean {d['400']['mean']:.3f}, \ variance {d['400']['var']:.3f}", font_size=22, color=MLEC),
            label(rf"white: \ the limit: \ mean {m:.4f}, \ variance {v:.3f}", font_size=22, color=LIMC),
            label(r"mean $= -$ variance$/2$: \ the normalized Gaussian log-likelihood-ratio identity", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Even the Cauchy family, heavy tails and all, is locally asymptotically normal. Its Fisher information is one half. Take h equal to one and a half. <bookmark mark='b'/> With twenty-five observations the simulated log-likelihood ratio has mean {say(d['25']['mean'], 3)} and variance {say(d['25']['var'], 2)}; <bookmark mark='c'/> with four hundred, {say(d['400']['mean'], 3)} and {say(d['400']['var'], 2)}. <bookmark mark='d'/> The limit is normal with mean minus h squared I over two, {say(m, 3)}, and variance h squared I. <bookmark mark='e'/> The mean is minus half the variance, as required for a normally distributed log-likelihood ratio with normalized exponential mean one. An arbitrary nonnormal log-likelihood ratio need not have mean minus half its variance."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 samples per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(h25), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h400), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(nc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def qmd(self):
        rows = [
            cmath(r"\text{QMD}", r":", r"\textstyle\int \big(\sqrt{p_{\theta + h}} - \sqrt{p_\theta} - \tfrac12 h^\top \dot\ell_\theta \sqrt{p_\theta}\big)^2 = o(|h|^2)", font_size=28),
            cmath(r"\text{QMD at } \theta", r"\Rightarrow", r"\text{LAN, \ for i.i.d.\ data}", font_size=34),
            cmath(r"\text{Cauchy, \ logistic, \ Laplace}", r":", r"\text{QMD, \ though the Laplace density has a kink}", font_size=30),
            cmath(r"U(0, \theta)", r":", r"\text{not QMD: \ squared Hellinger change is order $|h|$; \ no root-$n$ LAN \ (chapter 13)}", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(HODC)
        whys = [why(r"differentiable in quadratic mean"), why(r"Le Cam; \ Hájek"), why(r"weaker than smoothness"), why(r"rate $n$, \ not $\sqrt n$")]
        with self.voiceover(
            "<bookmark mark='a'/> When does LAN hold? The right condition is differentiability in quadratic mean: the"
            " square root of the density, as a curve in L two, has a derivative. <bookmark mark='b'/> For independent"
            " identically distributed observations, quadratic-mean differentiability gives LAN. We require finite "
            "positive definite information for the nonsingular Gaussian shift used here. <bookmark mark='c'/> It is "
            "weaker than classical smoothness: the Laplace density, with its kink at the centre, qualifies. <bookmark"
            " mark='d'/> The uniform on zero to theta does not, because its square-root-density change has squared "
            "L-two size of order the parameter shift, rather than the quadratic differentiability remainder required "
            "here. Moving support alone does not rule out QMD in every other model. There the rate is n, not root n, "
            "and the local limit is not Gaussian: chapter thirteen."
        ) as vo:
            heading=label('Quadratic-mean differentiation gives an iid LAN expansion',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scoretest(self):
        rows = [
            cmath(r"Y \sim N(h, I^{-1})", r":", r"\text{best test of } h = 0 \text{ vs } h > 0: \ \text{large } Y", font_size=34),
            cmath(r"Y", r"\leftrightarrow", r"I^{-1}\Delta_n: \ \text{the normalized score}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{the score test: \ asymptotically UMP, \ one-sided}", font_size=34),
            cmath(r"\text{two-sided}, \ k > 1", r":", r"\chi^2 \text{ tests: \ asymptotically optimal invariant}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Part 46's Neyman--Pearson"), why(r"what plays the role of $Y$"), why(r"optimality, \ transferred"), why(r"Part 46's invariance")]
        with self.voiceover(
            "<bookmark mark='a'/> LAN turns large-sample questions into small-sample ones. In the limit experiment, a"
            " single normal observation with mean h, the most powerful test of h equal to zero against positive h "
            "rejects for large Y, by Part forty-six's Neyman–Pearson lemma. <bookmark mark='b'/> The normalized score"
            " plays the role of Y. <bookmark mark='c'/> So the score test is asymptotically uniformly most powerful "
            "against one-sided local alternatives, and no test can do better in the limit. <bookmark mark='d'/> For "
            "two-sided or multivariate problems, after specifying the corresponding rotation-invariant Gaussian "
            "testing problem, chi-square tests have optimality within that invariant class, so the Wald, score and "
            "likelihood ratio tests are asymptotically optimal in that class."
        ) as vo:
            heading=label('Gaussian local tests give power bounds in a specified class',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
