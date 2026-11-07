from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Likelihood(VoiceoverScene):
    def construct(self):
        self.card()
        self.loglik()
        self.reml()
        self.table()
        self.nu()
        self.cost()

    def card(self):
        card = chapter_card(6, r"Likelihood", r"Fitting the covariance and the trend together", lit=(1985,), part=PART)
        with self.voiceover("Chapter six. Likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def loglik(self):
        rows = [
            cmath(r"Z", r"\sim", r"N\big(X\beta, \ \Sigma(\theta)\big), \ \ \Sigma = \sigma^2 R_\rho + \tau^2 I", font_size=32),
            cmath(r"\ell(\beta, \theta)", r"=", r"-\tfrac12 \log|\Sigma| - \tfrac12 (Z - X\beta)^\top \Sigma^{-1} (Z - X\beta)", font_size=30),
            cmath(r"\hat\beta(\theta)", r"=", r"(X^\top \Sigma^{-1} X)^{-1} X^\top \Sigma^{-1} Z", font_size=30),
            cmath(r"\text{profile}", r":", r"\text{maximize } \ell(\hat\beta(\theta), \theta) \text{ over } \theta = (\rho, \sigma^2, \tau^2)", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"one draw of an $n$-variate normal"), why(r"Part 22's likelihood"), why(r"GLS, \ given $\theta$"),
                why(r"Mardia \& Marshall (1984)")]
        with self.voiceover(
            "<bookmark mark='a'/> Variogram fitting by eye or by least squares was the geostatistician's way. Statisticians "
            "prefer the likelihood. For a Gaussian field, the whole data vector is a single draw from a multivariate "
            "normal, with mean X beta and a covariance built from the field and the nugget. <bookmark mark='b'/> The "
            "log-likelihood has a log-determinant and a quadratic form. <bookmark mark='c'/> For fixed covariance "
            "parameters the best beta is generalized least squares, <bookmark mark='d'/> so we can profile it out and "
            "maximize over the few covariance parameters numerically. Kanti Mardia and Roger Marshall gave the asymptotics "
            "in 1984."
        ) as vo:
            intro=label('Gaussian likelihood profiles out a generalized least-squares trend',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reml(self):
        rows = [
            cmath(r"\text{ML}", r":", r"\hat\sigma^2 \text{ biased down: \ it ignores that } \beta \text{ was estimated}", font_size=30),
            cmath(r"\text{REML}", r":", r"\text{the likelihood of } A^\top Z, \ \ A^\top X = 0", font_size=30),
            cmath(r"\ell_R(\theta)", r"=", r"\ell(\hat\beta(\theta), \theta) - \tfrac12 \log |X^\top \Sigma^{-1} X|", font_size=30),
            cmath(r"\text{e.g.}", r":", r"\text{for i.i.d. data, \ REML gives } s^2 = \text{RSS}/(n - p)", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"known correlation shape: ML scale uses $n$, REML uses $n-p$"), why(r"error contrasts"), why(r"Patterson \& Thompson (1971)"),
                why(r"the familiar correction")]
        with self.voiceover(
            "<bookmark mark='a'/> With a known correlation shape, maximum likelihood for the scale is biased downward"
            " because it treats the estimated trend as if it were known: the familiar n against n minus p. With "
            "jointly estimated covariance shapes the bias comparison is more complicated, and REML is not universally"
            " unbiased. <bookmark mark='b'/> Restricted maximum likelihood uses only the error contrasts, linear "
            "combinations of the data whose distribution does not involve beta at all. <bookmark mark='c'/> The "
            "result is the profile likelihood with one extra term, a log-determinant that penalizes the trend, "
            "<bookmark mark='d'/> and for independent data it gives back the familiar residual variance with n minus "
            "p in the denominator."
        ) as vo:
            intro=label('Restricted likelihood uses contrasts that remove the fixed trend',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("world")
        f, ml, tp = d["fits"]["1.5"], d["ml"], d["truth_params"]
        rows = [[r"the World, \ $\nu = 3/2$", r"$\rho$", r"$\sigma^2$", r"$\tau^2$", r"$\beta_0$", r"$\beta_{\text{traffic}}$"],
                [r"truth", f"{tp['rho']:.2f}", f"{tp['sigma2']:.2f}", f"{tp['tau2']:.2f}", f"{tp['beta'][0]:.2f}", f"{tp['beta'][1]:.2f}"],
                [r"ML", f"{ml['rho']:.2f}", f"{ml['sigma2']:.2f}", f"{ml['tau2']:.2f}", f"{ml['beta'][0]:.2f}", f"{ml['beta'][1]:.2f}"],
                [r"REML", f"{f['rho']:.2f}", f"{f['sigma2']:.2f}", f"{f['tau2']:.2f}", f"{f['beta'][0]:.2f}", f"{f['beta'][1]:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.34, colors=[GREY_A, TRUEC, FIELDC, BANDC]).move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"REML range and variance are larger here; this ordering is not universal", font_size=24, color=BANDC),
            label(r"both overshoot the truth together, \ along chapter five's ridge", font_size=24, color=TAUC),
            label(r"the trend, \ which kriging needs most, \ is close", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Both fits on the World's stations, with smoothness three halves. <bookmark mark='b'/> "
            "Restricted likelihood gives a range of " + say(f["rho"], 2) + " and a variance of " + say(f["sigma2"], 1) +
            ", against the truth of one point five and six point two five; in this fit maximum likelihood gives "
            "smaller values of both, which is not a universal ordering theorem. <bookmark mark='c'/> Both overshoot "
            "the range and the variance together, along chapter five's ridge: one island cannot separate them. "
            "<bookmark mark='d'/> The trend coefficients, which matter most for the predictions, are close to the "
            "truth."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def nu(self):
        d = load("world")
        F = d["fits"]
        best = max(F, key=lambda k: F[k]["ll"])
        rows = [[r"smoothness", r"REML log-likelihood", r"$\hat\rho$", r"$\hat\sigma^2$"]]
        for k, name in (("0.5", r"$\nu = 1/2$"), ("1.5", r"$\nu = 3/2$ \ (true)"), ("2.5", r"$\nu = 5/2$")):
            rows.append([name, f"{F[k]['ll']:.2f}", f"{F[k]['rho']:.2f}", f"{F[k]['sigma2']:.2f}"])
        cols = [GREY_A] + [BANDC if k == best else FIELDC for k in ("0.5", "1.5", "2.5")]
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.34, colors=cols).move_to([0, 0.9, 0])
        gap = F["1.5"]["ll"] - max(F["0.5"]["ll"], F["2.5"]["ll"])
        foot = fit_rows(VGroup(
            label(rf"the true $\nu$ wins by {gap:.1f} log-likelihood units: \ a modest margin, \ but the right way", font_size=24, color=BANDC),
            label(r"the range adjusts to compensate: \ a rougher model wants a longer range", font_size=24, color=TAUC),
            label(r"in practice: \ compare a few half-integers, \ or put $\nu$ in the optimizer", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Can the data choose the smoothness? Fit the World with nu of one half, three halves and "
            "five halves. <bookmark mark='b'/> The true value wins, by " + say(gap, 1) + " log-likelihood units over the "
            "nearest rival: a modest margin, but the data lean the right way, because smoothness governs the behaviour at short "
            "distances, where three hundred stations give many close pairs. "
            "<bookmark mark='c'/> The estimated range moves to compensate. <bookmark mark='d'/> In practice one compares a "
            "few half-integers by likelihood or cross-validation, or lets the optimizer estimate nu along with the rest."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def cost(self):
        d = load("scale")
        t = d["times"]
        ns = [250, 500, 1000, 2000]
        ys = [float(t[str(n)]) for n in ns]
        lo = int(np.floor(np.log10(min(ys)))) - 0
        hi = int(np.ceil(np.log10(max(ys))))
        A = axes([2, 3.5], [lo, hi], x_length=7.0, y_length=4.2, xlabel=r"number of locations $n$", ylabel=r"seconds per likelihood",
                 xticks=[np.log10(n) for n in ns], yticks=list(range(lo, hi + 1)), xfmt=lambda v: f"{10 ** v:,.0f}",
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.6, 0.1, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(n), np.log10(y)), radius=0.08, color=FIELDC) for n, y in zip(ns, ys)])
        ref = DashedLine(ax.c2p(np.log10(250), np.log10(ys[-1]) - 3 * np.log10(8)), ax.c2p(np.log10(2000), np.log10(ys[-1])),
                         color=TAUC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"each likelihood: \ a Cholesky factor of an $n \times n$ matrix", font_size=22),
            label(r"memory $O(n^2)$, \ time $O(n^3)$", font_size=22, color=TAUC),
            label(rf"2,000 locations: \ {ys[-1]:.2f} s; \ the optimizer needs hundreds", font_size=22, color=FIELDC),
            label(rf"100,000: cubic extrapolation {d['cubic_extrap_hours']:,.0f} hours, not measured", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The catch is the cost. Every evaluation of the likelihood needs the Cholesky factor of an "
            "n by n covariance matrix. <bookmark mark='b'/> That is n squared memory and n cubed time; the gold line has "
            "slope three. <bookmark mark='c'/> Two thousand locations take " + say(ys[-1], 2) + " seconds per evaluation, and the optimizer needs hundreds of evaluations. <bookmark mark='d'/> A hundred"
            " thousand locations, a modest satellite image, under a simple cubic extrapolation from this machine and "
            "load would take about " + f"{d['cubic_extrap_hours']:,.0f}" + " hours for each one. Chapter seven "
            "is about getting around this."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), Create(ref), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
