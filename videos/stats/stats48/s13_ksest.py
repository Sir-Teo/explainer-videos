from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class EstimatedParameters(VoiceoverScene):
    def construct(self):
        self.card()
        self.process()
        self.chart()
        self.sizes()
        self.newcomb()
        self.board()

    def card(self):
        card = chapter_card(12, r"KS with estimated parameters, \ done right", r"Testing a family, \ not a single law", lit=(1973,), part=PART)
        with self.voiceover("Chapter twelve. The Kolmogorov–Smirnov test with estimated parameters, done right: testing a family, not a single law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def process(self):
        rows = [
            cmath(r"\sqrt n\,(F_n(x) - F_{\hat\theta}(x))", r"=", r"\sqrt n(F_n - F_{\theta}) - \sqrt n(F_{\hat\theta} - F_\theta)", font_size=32),
            cmath(r"\phantom{\sqrt n}", r"\approx", r"\mathbb G_n \mathbf 1\{\cdot \le x\} - \dot F_\theta(x)^\top I^{-1} \mathbb G_n \dot\ell_\theta", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"B(F(x)) - \dot F_\theta(x)^\top I^{-1} \textstyle\int \dot\ell_\theta\, dB(F): \ \text{not a bridge}", font_size=30),
            cmath(r"\text{normal, } (\mu, \sigma) \text{ estimated}", r":", r"\mathrm{Var} = \Phi(1-\Phi) - \phi^2 - \tfrac12 (z\phi)^2", font_size=32),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"add and subtract"), why(r"chapter 8's footprint, \ with the MLE's influence"), why(r"Durbin (1973)"), why(r"smaller than $\Phi(1 - \Phi)$")]
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-six met Lilliefors's discovery: if the parameters are estimated, the "
            "Kolmogorov–Smirnov table is wrong. Here is why. The gap between the empirical distribution and the fitted one "
            "splits into the ordinary empirical process minus the movement of the fitted distribution. <bookmark mark='b'/> "
            "The movement is the derivative of F in theta times the estimator's error, and the maximum likelihood estimator's "
            "error is the inverse information times the empirical process applied to the score. This is chapter eight's "
            "footprint in function space. <bookmark mark='c'/> So the limit is a Brownian bridge minus a random term built "
            "from the same bridge: a Gaussian process, but not a bridge, as James Durbin showed in 1973. <bookmark mark='d'/> "
            "For the normal family with mean and standard deviation estimated, its variance at the standardized point z is "
            "the bridge's, Phi times one minus Phi, minus phi squared, minus half of z phi squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("ksest")
        z = np.asarray(d["zg"])
        A = axes([-3, 3], [0, 0.27], x_length=7.4, y_length=4.4, xlabel=r"$z = (x - \mu)/\sigma$", ylabel=r"variance of the limit",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.1, 0.2, 0.25], center=[-2.5, 0.2, 0])
        ax = A.ax
        cb = polyline(ax, z, d["var_bridge"], BRIDGEC, 4)
        cd = polyline(ax, z, d["var_dur"], CLASSC, 4)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=EMPC) for a, b in zip(z[::3], np.asarray(d["var_sim"])[::3])])
        i0 = int(np.argmin(np.abs(z)))
        side = fit_rows(VGroup(
            label(r"normal data, \ $n = 100$, \ 20,000 samples", font_size=22),
            label(r"white: \ known parameters, \ $\Phi(1-\Phi)$", font_size=22, color=BRIDGEC),
            label(r"gold: \ estimated, \ Durbin's formula", font_size=22, color=CLASSC),
            label(rf"blue: \ simulated; \ at $z = 0$: \ {d['var_sim'][i0]:.4f} vs {d['var_dur'][i0]:.4f}", font_size=22, color=EMPC),
            label(r"fitting removes two thirds at $z = 0$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Normal samples of a hundred. <bookmark mark='b'/> In white, the variance of the ordinary "
            f"empirical process, a quarter at the centre. <bookmark mark='c'/> In gold, Durbin's variance for the process "
            f"with fitted parameters. <bookmark mark='d'/> The dots are simulated variances: at the centre, "
            f"{say(d['var_sim'][i0], 4)} against the formula's {say(d['var_dur'][i0], 4)}. <bookmark mark='e'/> Fitting the "
            f"mean and the standard deviation pulls the fitted curve toward the data, and removes nearly two thirds of the "
            f"variance in the middle. The supremum is correspondingly smaller, so Kolmogorov's critical values are far too "
            f"large."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"dots simulated; \ curves exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cd), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dots), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def sizes(self):
        d = load("ksest")
        rows = [[r"family, \ $n$", r"Kolmogorov's 95\% point", r"correct 95\% point", r"size with Kolmogorov's"],
                [r"normal, \ 20", f"{d['crit_kolm']:.4f}", f"{d['crit_est']:.4f}", f"{100 * d['size_norm_naive']:.3f}\\%"],
                [r"exponential, \ 50", f"{d['crit_kolm50']:.4f}", f"{d['crit_exp']:.4f}", f"{100 * d['size_exp_naive']:.2f}\\%"]]
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.4, colors=[GREY_B, None, None])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.9, 0])
        foot = label(r"the law of $D$ with estimated location--scale or scale parameters is \emph{parameter-free}: \ one table per family and $n$", font_size=24, color=CLASSC).move_to([0, -1.3, 0])
        foot2 = label(r"so a parametric bootstrap is exact, \ up to Monte Carlo error: \ simulate from $F_{\hat\theta}$, \ refit, \ recompute", font_size=24, color=GOODC).move_to([0, -2.1, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> How far off? For normal samples of twenty, the correct ninety-five percent point of D is "
            f"{say(d['crit_est'], 3)}, against Kolmogorov's {say(d['crit_kolm'], 3)}. A test using Kolmogorov's table almost "
            f"never rejects: its true size is about {100 * d['size_norm_naive']:.3f} percent. For the exponential with an "
            f"estimated rate, at fifty, the size is {100 * d['size_exp_naive']:.1f} percent instead of five. <bookmark "
            f"mark='b'/> The remedy rests on a lucky fact. For location–scale and scale families, the law of D with fitted "
            f"parameters does not depend on the true parameters. <bookmark mark='c'/> So a parametric bootstrap, simulating "
            f"from the fitted distribution, refitting, and recomputing D, gets the right critical value, up to Monte Carlo "
            f"error. For other families the bootstrap is still consistent, by chapter eleven's argument."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated: \ 40,000 samples")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def newcomb(self):
        d = load("ksest")
        f, t = d["newcomb"], d["newcomb_trim"]
        rows = [
            cmath(rf"\text{{all {d['nc_n']} times}}", r":", rf"D = {f['D']:.3f}; \ \ p_{{\text{{Kolm}}}} = {f['naive_p']:.4f}, \ \ p_{{\text{{boot}}}} = {max(f['p'], 1e-4):.4f}", font_size=32),
            cmath(rf"\text{{without the two outliers}} \ ({d['nc_trim_n']})", r":", rf"D = {t['D']:.3f}; \ \ p_{{\text{{Kolm}}}} = {t['naive_p']:.2f}, \ \ p_{{\text{{boot}}}} = {t['p']:.2f}", font_size=30),
            cmath(r"\text{the naive } p", r":", r"\text{far too large: \ it would hide real departures}", font_size=32),
            cmath(r"\text{the bootstrap's verdict}", r":", r"\text{the outliers are the problem; \ the rest is plausibly normal}", font_size=30),
        ]
        rows[0][-1].set_color(BADC)
        rows[1][-1].set_color(GOODC)
        whys = [why(r"9,999 parametric resamples"), why(r"Part 30's outliers removed"), why(r"Kolmogorov's table, \ misused"), why(r"a calibrated test")]
        with self.voiceover(
            f"<bookmark mark='a'/> Newcomb's passage times again. Testing normality with the mean and standard deviation "
            f"fitted, D is {say(f['D'], 3)}. Kolmogorov's table gives a p-value of {say(f['naive_p'], 4)}; the parametric "
            f"bootstrap, with ten thousand resamples, finds none as extreme, a p-value below one in ten thousand. <bookmark "
            f"mark='b'/> Without the two famous outliers, D falls to {say(t['D'], 3)}. The naive p-value is "
            f"{say(t['naive_p'], 2)}, but the correct one is {say(t['p'], 2)}. <bookmark mark='c'/> The naive p-value is "
            f"three times too large: used routinely, it would hide real departures from normality. <bookmark mark='d'/> The "
            f"calibrated verdict: the two outliers are the problem, and the rest of the data are plausibly normal."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.add(museum_tag(r"Newcomb (1882), \ via Stigler (1977)"))
        self.wait(0.5)
        self.clear_scene()

    def board(self):
        rows = board_rows("estimated rate")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board, testing exponentiality with an estimated rate, thirty observations: "
                   "Kolmogorov's table gives a test that rejects less than one percent of the time when it should reject five, "
                   "conservative to the point of uselessness. <bookmark mark='b'/> The parametric bootstrap, two hundred resamples "
                   "per test, keeps the five percent promise.",
                   [("a", [0]), ("b", [1])])
