from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Toolkit(VoiceoverScene):
    def construct(self):
        self.card()
        self.orders()
        self.slutsky()
        self.delta()
        self.multi()
        self.chart()
        self.second()

    def card(self):
        card = chapter_card(1, r"Stochastic orders and the toolkit", r"Bookkeeping for things that go to zero at random", part=PART)
        with self.voiceover("Chapter one. Stochastic orders and the toolkit: bookkeeping for things that go to zero at random."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def orders(self):
        rows = [
            cmath(r"X_n = o_P(r_n)", r":", r"X_n / r_n \to 0 \ \text{in probability}", font_size=34),
            cmath(r"X_n = O_P(r_n)", r":", r"\forall \varepsilon\ \exists M: \ P(|X_n / r_n| > M) < \varepsilon \ \ \forall n", font_size=32),
            cmath(r"O_P(1)", r"\iff", r"\text{tight} \ \iff \ \text{every subsequence has a weakly convergent sub-subsequence}", font_size=28),
            cmath(r"\text{arithmetic}", r":", r"O_P(1)\, o_P(1) = o_P(1), \ \ o_P(1) + O_P(1) = O_P(1)", font_size=32),
        ]
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"little-oh in probability"), why(r"big-oh: \ bounded in probability"), why(r"Prokhorov, \ Part 43"), why(r"like $o$ and $O$")]
        with self.voiceover(
            "<bookmark mark='a'/> Two pieces of notation carry most of the subject. X n is little-oh-P of r n if X n over r "
            "n goes to zero in probability. <bookmark mark='b'/> It is big-oh-P of r n if it is bounded in probability: for "
            "any epsilon, a single bound M works for every n except with probability epsilon. <bookmark mark='c'/> Bounded "
            "in probability is the same as tight, and by Prokhorov's theorem from Part forty-three, the same as every "
            "subsequence having a weakly convergent subsequence. <bookmark mark='d'/> They combine like their deterministic "
            "cousins: bounded times small is small, small plus bounded is bounded."
        ) as vo:
            heading=label('Stochastic orders describe bounded and vanishing random terms',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def slutsky(self):
        rows = [
            cmath(r"X_n \Rightarrow X, \ Y_n \to_P c", r"\Rightarrow", r"X_n + Y_n \Rightarrow X + c, \ \ Y_n X_n \Rightarrow c X", font_size=30),
            cmath(r"g \text{ continuous } (P_X\text{-a.e.})", r"\Rightarrow", r"g(X_n) \Rightarrow g(X)", font_size=32),
            cmath(r"\text{e.g.}", r":", r"\sqrt n (\bar x - \mu)/s \Rightarrow N(0, 1) \ \text{for i.i.d.\ data, }0<\sigma^2<\infty", font_size=32),
            cmath(r"\text{the } t \text{ statistic}", r":", r"\text{robust to non-normality in large samples, \ by Slutsky}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Slutsky (1925)"), why(r"the continuous mapping theorem"), why(r"$s \to_P \sigma$"), why(r"Part 10's $t$, \ justified")]
        with self.voiceover(
            "<bookmark mark='a'/> Slutsky's lemma: if X n converges in distribution and Y n converges in probability "
            "to a constant, their sum and product converge to what you would expect. <bookmark mark='b'/> The "
            "continuous mapping theorem: continuous functions preserve convergence in distribution. <bookmark "
            "mark='c'/> Together they give the most used fact in statistics: the t statistic is asymptotically "
            "standard normal for independent identically distributed observations with finite, strictly positive "
            "variance, because s converges in probability to sigma. <bookmark mark='d'/> The usual t calibration is "
            "asymptotically valid in that setting. Finite variance does not ensure fast convergence, and dependence "
            "requires an appropriate variance estimate and limit theorem."
        ) as vo:
            heading=label('Studentization needs an iid CLT and a consistent scale',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def delta(self):
        rows = [
            cmath(r"\sqrt n(T_n - \theta) \Rightarrow T", r",", r"\ g \text{ differentiable at } \theta", font_size=32),
            cmath(r"g(T_n) - g(\theta)", r"=", r"g'(\theta)(T_n - \theta) + o_P(|T_n - \theta|)", font_size=32),
            cmath(r"\sqrt n(g(T_n) - g(\theta))", r"=", r"g'(\theta)\sqrt n(T_n - \theta) + o_P(1) \Rightarrow g'(\theta)\, T", font_size=30),
            cmath(r"\text{proof of the remainder}", r":", r"T_n - \theta = O_P(n^{-1/2}), \ \text{so } o(|T_n - \theta|) = o_P(n^{-1/2})", font_size=28),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a limit, \ and a smooth map"), why(r"the definition of a derivative"), why(r"the delta method"), why(r"the toolkit at work")]
        with self.voiceover(
            "<bookmark mark='a'/> The delta method, proved. Suppose root n times T n minus theta converges in distribution, "
            "and g is differentiable at theta. <bookmark mark='b'/> By the definition of the derivative, g of T n minus g "
            "of theta is g prime times the difference, plus something small compared with the difference. <bookmark "
            "mark='c'/> Multiply by root n: the first term converges by the continuous mapping theorem, <bookmark "
            "mark='d'/> and the remainder is small, because the difference is of order one over root n in probability, so "
            "anything small compared with it is little-oh-P of one over root n. Part eleven used this; here is why it holds."
        ) as vo:
            heading=label('A differentiable map transfers a root-n limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("delta")
        e = np.asarray(d["edges"])
        A = axes([-4, 4], [0, 0.5], x_length=7.4, y_length=4.4, xlabel=r"$\sqrt n \log \bar x$, \ Exp(1) data", ylabel=r"density",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        h5 = hist_bars(ax, e, d["hists"]["5"], color=HODC, opacity=0.45)
        h200 = hist_bars(ax, e, d["hists"]["200"], color=MLEC, opacity=0.6)
        zz = np.linspace(-4, 4, 200)
        nc = polyline(ax, zz, np.exp(-zz ** 2 / 2) / np.sqrt(2 * np.pi), LIMC, 4)
        r = {row["n"]: row for row in d["rows"]}
        side = fit_rows(VGroup(
            label(r"$g = \log$, \ $g'(1) = 1$: \ the limit is $N(0, 1)$", font_size=22),
            label(rf"red: \ $n = 5$: \ skewness {r[5]['skew']:.2f}, \ KS {r[5]['ks']:.3f}", font_size=22, color=HODC),
            label(rf"blue: \ $n = 200$: \ skewness {r[200]['skew']:.2f}, \ KS {r[200]['ks']:.3f}", font_size=22, color=MLEC),
            label(r"white: \ the delta method's normal", font_size=22, color=LIMC),
            label(r"the remainder is $O_P(n^{-1/2})$: \ visible at small $n$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Watch it work: root n times the log of the mean of exponential data, whose limit by the delta method is standard normal. <bookmark mark='b'/> With five observations the distribution is skewed, skewness {say(r[5]['skew'], 2)}, and visibly off. <bookmark mark='c'/> With two hundred, the skewness is {say(r[200]['skew'], 2)} and the histogram sits on the curve. <bookmark mark='d'/> The white curve is the limit. <bookmark mark='e'/> For the twice differentiable log map, the scaled Taylor remainder is of order one over root n. The plotted gap also includes finite-sample error in the central limit approximation, the subject of chapter twelve's saddlepoints and Part forty-three's Edgeworth expansions."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 40,000 samples per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(h5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h200), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(nc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def second(self):
        d = load("delta")
        q, c = d["second_q"], d["chi2_q"]
        rows = [
            cmath(r"g\in C^2 \text{ locally}, \ g'(\theta) = 0", r":", r"\text{the first-order term vanishes}", font_size=34),
            cmath(r"n(g(T_n) - g(\theta))", r"\Rightarrow", r"\tfrac12 g''(\theta)\, T^2", font_size=34),
            cmath(r"g(x) = x^2, \ \mu = 0", r":", r"n \bar x^2 \Rightarrow \sigma^2 \chi^2_1", font_size=34),
            cmath(r"\text{quantiles}, \ n = 50", r":", rf"{q[0]:.2f}, \ {q[1]:.2f}, \ {q[2]:.2f} \ \ \text{{vs}} \ \ {c[0]:.2f}, \ {c[1]:.2f}, \ {c[2]:.2f}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a stationary point"), why(r"the next term, \ and a faster rate"), why(r"not normal at all"), why(r"simulated vs $\chi^2_1$")]
        with self.voiceover(
            "<bookmark mark='a'/> If g is twice differentiable near theta and its first derivative is zero, the "
            "first-order term vanishes, <bookmark mark='b'/> and the second-order term takes over, at the faster rate"
            " n, with a limit that is half the second derivative times the square of the limiting variable. <bookmark"
            " mark='c'/> For the square of the mean of data centred at zero, n times x-bar squared tends to sigma "
            "squared times a chi-square with one degree of freedom, not a normal. <bookmark mark='d'/> The simulated "
            "quantiles agree. Non-normal limits at singular points recur in chapter thirteen."
        ) as vo:
            heading=label('A zero first derivative can give a quadratic limit at rate n',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def multi(self):
        rows = [
            cmath(r"\text{Cram\'er--Wold}", r":", r"X_n \Rightarrow X \text{ in } \mathbb R^k \iff a^\top X_n \Rightarrow a^\top X \ \forall a", font_size=32),
            cmath(r"\sqrt n(\bar X - \mu)", r"\Rightarrow", r"N_k(0, \Sigma): \ \text{the multivariate CLT, \ from the univariate}", font_size=30),
            cmath(r"\sqrt n(g(\bar X) - g(\mu))", r"\Rightarrow", r"N(0, \ \nabla g^\top \Sigma \nabla g)", font_size=32),
            cmath(r"\text{e.g.\ the correlation}", r":", r"g(\text{five moments}): \ \mathrm{Var} = (1 - \rho^2)^2/n \ \text{(normal)}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Part 43"), why(r"one direction at a time"), why(r"the gradient"), why(r"Part 12's Fisher $z$, \ explained")]
        with self.voiceover(
            "<bookmark mark='a'/> The vector versions come cheaply. By the Cramér–Wold device from Part forty-three, a "
            "random vector converges in distribution exactly when every linear combination does. <bookmark mark='b'/> So the "
            "multivariate central limit theorem follows from the univariate one, one direction at a time. <bookmark "
            "mark='c'/> And the delta method uses the gradient: the limit variance is the gradient times the covariance "
            "times the gradient. <bookmark mark='d'/> Applied to the sample correlation, a smooth function of five sample "
            "moments, it gives a variance of one minus rho squared, squared, over n for normal data; Fisher's z "
            "transformation is the function that makes that variance constant."
        ) as vo:
            heading=label('Cramer-Wold and a gradient transfer a joint limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
