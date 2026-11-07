from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Nonlinear(VoiceoverScene):
    def construct(self):
        self.card()
        self.methods()
        self.benchmark()
        self.scores()
        self.pmcmc()
        self.hamilton_model()
        self.gdp()

    def card(self):
        card = chapter_card(9, r"Nonlinear filtering and regimes", r"When the Gaussian ellipse breaks", lit=(1989, 1993, 1997), part=PART)
        with self.voiceover("Chapter nine. Nonlinear filtering, and switching regimes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def methods(self):
        rows = [
            cmath(r"x_t", r"=", r"f(x_{t-1}) + w_t, \quad y_t = h(x_t) + v_t", font_size=32),
            cmath(r"\text{EKF}", r":", r"\text{linearize } f, h \text{ at the current mean}", font_size=30),
            cmath(r"\text{UKF}", r":", r"\text{push } 2k + 1 \text{ sigma points through } f, h \text{; refit a Gaussian}", font_size=30),
            cmath(r"\text{particle filter}", r":", r"\text{propagate, \ weight by } p(y_t \mid x), \text{ resample}", font_size=30),
        ]
        rows[3][-1].set_color(STATEC)
        whys = [why(r"nonlinear dynamics or measurements"), why(r"Schmidt (1960s)"), why(r"Julier \& Uhlmann (1997)"),
                why(r"Gordon, \ Salmond \& Smith (1993); \ Part 27")]
        with self.voiceover(
            "<bookmark mark='a'/> When the dynamics or the measurement are nonlinear, the state's distribution is no longer "
            "Gaussian, and the ellipses no longer tell the truth. <bookmark mark='b'/> The extended filter linearizes the "
            "functions at the current estimate and applies Kalman's equations. <bookmark mark='c'/> Simon Julier and Jeffrey "
            "Uhlmann's unscented filter, of 1997, instead pushes a few carefully placed sigma points through the "
            "nonlinearity and fits a Gaussian to where they land. <bookmark mark='d'/> And the particle filter of Neil "
            "Gordon, David Salmond and Adrian Smith, in 1993, met in Part twenty-seven, drops the Gaussian altogether: it "
            "carries thousands of samples forward, weights each by how well it explains the new observation, and resamples."
        ) as vo:
            intro=label('Nonlinear filters approximate the evolving state distribution',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def benchmark(self):
        d = load("nonlinear")
        x = np.asarray(d["x"], float)
        t = np.arange(len(x))
        low = min(float(np.min(d[k])) for k in ("x", "ekf", "pf_lo")) - 2
        high = max(float(np.max(d[k])) for k in ("x", "ekf", "pf_hi")) + 2
        A = axes([0, 100], [low, high], x_length=10.0, y_length=4.0, xlabel=r"time", ylabel=r"state", xticks=[0, 50, 100],
                 yticks=[-20, 0, 20], center=[0, 0.5, 0])
        ax = A.ax
        tr = polyline(ax, t, x, TRUEC, 2.5)
        ek = polyline(ax, t, d["ekf"], MISSC, 2)
        b = band(ax, t, np.asarray(d["pf_lo"], float), np.asarray(d["pf_hi"], float), STATEC, 0.25)
        pf = polyline(ax, t, d["pf"], STATEC, 2)
        foot = fit_rows(VGroup(
            label(r"$x_t = \frac{x}{2} + \frac{25x}{1 + x^2} + 8\cos 1.2t + w_t$, \ \ $y_t = x_t^2/20 + v_t$: \ sign is unobserved; filters share prior N(0.1,5), generator starts at 0.1", font_size=22),
            label(r"gold: \ truth; \ red: \ extended filter; \ blue: \ particle filter, \ 3,000 particles, \ 90\% band", font_size=22, color=GREY_A),
        ), 12.4, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The standard test, used by Gordon and his colleagues: a state that swings between "
            "positive and negative values, observed through its square, so the sign is never measured directly. The "
            "truth is in gold. <bookmark mark='b'/> The extended filter, in red, often locks onto the wrong sign and "
            "stays there, because its linearization cannot represent two possibilities at once. <bookmark mark='c'/> "
            "The particle filter, in blue, can retain both modes. The plotted central quantile band spans them rather"
            " than splitting, and can include low-density states; its mean can lie between modes."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(tr), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Create(ek), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(b), Create(pf))
        self.clear_scene()

    def scores(self):
        d = load("nonlinear")["rmse30"]
        rows = [[r"filter", r"RMSE, \ 30 simulated series"],
                [r"extended Kalman", f"{d['ekf']:.1f}"], [r"unscented Kalman", f"{d['ukf']:.1f}"],
                [r"particle, \ 2,000 particles", f"{d['pf']:.1f}"]]
        tab = table_rows(rows, font_size=30, col_buff=1.2, row_buff=0.36, colors=[GREY_A, MISSC, TAUC, STATEC]).move_to([0, 0.6, 0])
        foot = label(r"particle count is not a measured wall-time ratio; performance is benchmark-specific",
                     font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over thirty simulated series: <bookmark mark='b'/> the extended filter's error is about "
            + say(d["ekf"], 0) + ". <bookmark mark='c'/> The unscented filter halves it. <bookmark mark='d'/> The particle "
            "filter cuts it to about " + say(d["pf"], 0) + ", with a much larger particle population; no wall-time ratio is measured here. When the distribution is "
            "close to Gaussian, Kalman's equations or their extensions are cheaper and nearly as good."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def hamilton_model(self):
        rows = [
            cmath(r"s_t \in \{0, 1\}", r":", r"\text{a hidden Markov chain: \ recession or expansion}", font_size=30),
            cmath(r"y_t", r"=", r"\mu_{s_t} + \sigma \varepsilon_t, \quad P(s_t = j \mid s_{t-1} = i) = p_{ij}", font_size=30),
            cmath(r"\text{filter}", r":", r"P(s_t \mid y_{1:t}) \propto p(y_t \mid s_t) \textstyle\sum_i p_{i s_t} P(s_{t-1} = i \mid y_{1:t-1})", font_size=28),
            cmath(r"\text{likelihood}", r":", r"\text{the normalizers, \ multiplied: \ maximize}", font_size=30),
        ]
        rows[2][-1].set_color(STATEC)
        whys = [why(r"a discrete hidden state"), why(r"Hamilton (1989)"), why(r"a two-point Kalman filter"),
                why(r"as in chapter 8")]
        with self.voiceover(
            "<bookmark mark='a'/> A hidden state can also be discrete. James Hamilton's model of 1989 lets the economy switch "
            "between two regimes, recession and expansion, following a Markov chain. <bookmark mark='b'/> Growth has a "
            "different mean in each. <bookmark mark='c'/> The filter is the same recursion with two points instead of a "
            "Gaussian: predict the regime probabilities with the transition matrix, then reweight them by how likely this "
            "quarter's growth is under each. <bookmark mark='d'/> The product of the normalizing constants is the "
            "likelihood, maximized as before."
        ) as vo:
            intro=label('A switching-mean model filters a discrete hidden regime',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gdp(self):
        d = load("nonlinear")["gdp"]
        t, gr, p = (np.asarray(d[k], float) for k in ("t", "growth", "p_low"))
        A = axes([1959, 2010], [-10, 16], x_length=10.0, y_length=2.4, xlabel=r"", ylabel=r"GDP growth (\%)", xticks=[],
                 yticks=[-8, 0, 8], center=[0, 1.6, 0])
        B = axes([1959, 2010], [0, 1], x_length=10.0, y_length=1.8, xlabel=r"year", ylabel=r"P(low regime)",
                 xticks=[1960, 1970, 1980, 1990, 2000, 2010], yticks=[0, 1], xfmt=lambda v: f"{v:.0f}", center=[0, -1.3, 0])
        shades = VGroup(*[Rectangle(width=B.ax.c2p(b, 0)[0] - B.ax.c2p(a, 0)[0], height=B.ax.c2p(0, 1)[1] - B.ax.c2p(0, 0)[1],
                                    stroke_width=0, fill_color=GREY_C, fill_opacity=0.35).move_to(B.ax.c2p((a + b) / 2, 0.5))
                          for a, b in d["nber"]])
        cg = series_line(A.ax, t, gr, OBSC, 1.8)
        cp = series_line(B.ax, t, p, MISSC, 2.5)
        foot = label(rf"regimes: \ {d['mu'][0]:.1f}\% and {d['mu'][1]:.1f}\% a year; \ they last {d['dur_low']:.0f} and {d['dur_high']:.0f} quarters on average; \ grey: \ NBER recessions",
                     font_size=22, color=GREY_A).move_to([0, -3.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> US real growth, quarter by quarter, annualized, 1959 to 2009. <bookmark mark='b'/> "
            "Hamilton's model finds one regime growing at about " + say(d["mu"][1], 1) + " percent a year and another "
            "shrinking at about " + say(-d["mu"][0], 1) + " percent, lasting on average " + str(round(d["dur_high"])) + " "
            "and " + str(round(d["dur_low"])) + " quarters. <bookmark mark='c'/> The filtered probability of the low regime, "
            "in red, rises in the recessions that the National Bureau of Economic Research later dated by committee, in grey: "
            "an average of " + say(d["p_in"], 2) + " inside them and " + say(d["p_out"], 2) + " outside, filtered using GDP observations only up to each displayed quarter, but with parameters "
            "estimated from the entire sample. This is a retrospective filter, not a real-time forecast evaluation."
        ) as vo:
            self.add(macro_tag())
            self.play(FadeIn(A), Create(cg))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(shades), Create(cp))
        self.clear_scene()

    def pmcmc(self):
        rows = fit_rows(VGroup(
            label(r"the product of stepwise mean unnormalized weights estimates the likelihood without bias", font_size=26, color=STATEC),
            label(r"Andrieu, \ Doucet \& Holenstein (2010): \ use it inside Metropolis--Hastings: \ PMCMC", font_size=26, color=TAUC),
            label(r"exact Bayesian inference for parameters of nonlinear state space models", font_size=26, color=BANDC),
            label(r"stochastic volatility, \ epidemic models, \ ecology: \ Part 27's ideas, \ at scale", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The particle filter also gives a likelihood. The average of each step's "
            "unnormalized weights, multiplied over time, is an unbiased estimate of the likelihood of the parameters."
            " <bookmark mark='b'/> Christophe Andrieu, Arnaud Doucet and Roman Holenstein showed in 2010 that "
            "plugging this noisy but unbiased estimate into a Metropolis-Hastings sampler still targets the exact "
            "posterior: particle Markov chain Monte Carlo. <bookmark mark='c'/> With a nonnegative unbiased "
            "likelihood estimate and the extended-state construction, its invariant parameter distribution is the "
            "exact posterior. Finite MCMC runs still require convergence checks. <bookmark mark='d'/> Stochastic "
            "volatility, epidemic models and animal populations are fitted this way: the ideas of Part twenty-seven, "
            "at scale."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
