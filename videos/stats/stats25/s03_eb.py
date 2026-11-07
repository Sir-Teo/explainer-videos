from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class EB(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.normal()
        self.js_is_eb()
        self.robbins()
        self.prior()
        self.winners()

    def card(self):
        card = chapter_card(2, r"Empirical Bayes", r"Estimate the prior from the data", lit=(1956,), part=PART)
        with self.voiceover("Chapter two. Empirical Bayes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        u = upgrade_card(15, r"with a normal prior, \ the posterior mean pulls the data towards the prior mean",
                         r"the prior is known, \ or chosen",
                         r"with many parallel problems, \ the prior can be estimated: \ empirical Bayes",
                         width=11.0, font_size=24).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 15 showed that with a normal prior, the posterior mean pulls the observation towards "
            "the prior mean, by an amount set by the relative variances. <bookmark mark='b'/> It assumed the prior was known, "
            "or chosen. <bookmark mark='c'/> But when we face many parallel problems at once, eighteen hitters, four hundred "
            "schools, two hundred towns, the spread of the estimates themselves tells us what the prior must be. Estimating "
            "it from the data is empirical Bayes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(u[0]), FadeIn(u[1][0]), FadeIn(u[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(u[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(u[1][1][2]))
        self.wait(1.0)
        self.clear_scene()

    def normal(self):
        rows = [
            cmath(r"\theta_i", r"\sim", r"N(\mu, \tau^2), \ \ x_i \mid \theta_i \sim N(\theta_i, 1)", font_size=30),
            cmath(r"E(\theta_i \mid x_i)", r"=", r"\mu + (1 - B)(x_i - \mu), \ \ B = \dfrac{1}{1 + \tau^2}", font_size=30),
            cmath(r"x_i", r"\sim", r"N(\mu, 1 + \tau^2) \ \text{marginally}", font_size=30),
            cmath(r"E\Big[\dfrac{p - 3}{\sum (x_i - \bar x)^2}\Big]", r"=", r"B,\ \ p>3 \text{; untruncated ratio}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"a population of abilities"), why(r"Part 15's posterior mean"), why(r"the data reveal $\mu$ and $\tau^2$"),
                why(r"an unbiased estimate of the shrinkage")]
        intro = label('Normal empirical Bayes estimates the population shrinkage factor', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the true abilities come from a normal population with mean mu and variance "
            "tau squared, and each observation adds unit-variance noise. <bookmark mark='b'/> Bayes' posterior mean "
            "is mu plus one minus B times the distance from mu, with B equal to one over one plus tau squared. "
            "<bookmark mark='c'/> We don't know mu or tau squared, but the observations, averaged over the "
            "population, are normal with mean mu and variance one plus tau squared, so the data reveal both. "
            "<bookmark mark='d'/> For p greater than three, the untruncated ratio p minus three over the centered sum"
            " of squares is unbiased for B. Truncating it changes that property."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def js_is_eb(self):
        rows = fit_rows(VGroup(
            label(r"plug the estimated $B$ into Bayes' rule:", font_size=24),
            label(r"$\bar x + \big(1 - \frac{p - 3}{\sum (x_i - \bar x)^2}\big)(x_i - \bar x)$ \ $=$ \ James--Stein", font_size=26, color=SHRUNK),
            label(r"Efron \& Morris (1973): \ Stein's estimator is empirical Bayes", font_size=24, color=GREY_A),
            label(r"a large spread: \ little shrinkage; \ a small spread: \ a lot", font_size=24),
            label(r"the baseball: \ the early averages spread about as much as luck alone allows", font_size=24, color=PATH),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Plug that estimate into Bayes' rule <bookmark mark='b'/> and out comes exactly the "
            "James–Stein estimator shrinking towards the grand mean. <bookmark mark='c'/> Efron and Morris made this "
            "connection in 1973: Stein's mysterious estimator is Bayes with a prior estimated from the data. "
            "<bookmark mark='d'/> When the estimates are much more spread out than noise alone would make them, the "
            "prior is wide and they are left almost alone; when they spread no more than noise would, they are pulled"
            " almost all the way in. <bookmark mark='e'/> The eighteen early batting averages spread out only a "
            "little more than luck alone allows, so James–Stein kept just a fifth of each player's transformed-scale "
            "distance from the middle."       ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def robbins(self):
        rows = [
            cmath(r"\text{any prior } g", r":", r"x \sim f(x) = \textstyle\int \phi(x - \theta)\, g(\theta)\, d\theta", font_size=30),
            cmath(r"\text{Tweedie}", r":", r"E(\theta \mid x) = x + \sigma^2 \dfrac{d}{dx}\log f(x)", font_size=30),
            cmath(r"\text{needs only}", r":", r"\text{the marginal density of the data}", font_size=30),
            cmath(r"\text{estimate } g", r":", r"\text{the NPMLE (Kiefer \& Wolfowitz 1956)}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"Robbins (1956): \ no normal prior needed"), why(r"Efron (2011): \ ``Tweedie's formula''"),
                why(r"which the data estimate directly"), why(r"EM on a grid: \ few atoms")]
        intro = label('Tweedie links a posterior mean to the marginal density derivative', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Herbert Robbins went further in 1956: the prior needn't be normal. With any prior, "
            "the data have a marginal density, the noise smeared over the prior. <bookmark mark='b'/> A remarkable "
            "identity, which Efron called Tweedie's formula, says the posterior mean is the observation plus the "
            "noise variance times the slope of the log marginal density. <bookmark mark='c'/> So it needs only the "
            "density of the data, which many parallel observations can help estimate, although derivatives in the "
            "tails remain difficult. <bookmark mark='d'/> Or estimate the prior itself, by Jack Kiefer and Jacob "
            "Wolfowitz's nonparametric maximum likelihood, Here we approximate it using finite iterations of EM on a "
            "fixed grid. This is not a certificate of the unrestricted optimum."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def prior(self):
        d = load("winners")
        gr, w = np.asarray(d["grid"]), np.asarray(d["w"])
        A = axes([-7, 7], [0, max(0.15, 1.1 * w.max())], x_length=8.0, y_length=4.2, xlabel=r"$\theta$", ylabel=r"estimated prior mass",
                 xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[0, 0.05, 0.1, 0.15], center=[-1.6, 0.3, 0])
        ax = A.ax
        keep = (w > 0) & (gr >= -7) & (gr <= 7)
        bars = VGroup(*[Line(ax.c2p(t, 0), ax.c2p(t, v), color=PRIOR, stroke_width=5) for t, v in zip(gr[keep], w[keep])])
        rows = fit_rows(VGroup(
            label(r"1,000 $z$-scores: \ 90\% true nulls, \ 10\% real effects", font_size=22),
            label(r"purple: \ fixed-grid EM estimate; \ full atom heights", font_size=22, color=PRIOR),
            label(rf"{100 * d['null_share']:.0f}\% of its mass near zero", font_size=22, color=PRIOR),
            VGroup(label(r"generating nonnulls: $N(0,3^2)$", font_size=20, color=GREY_A), label(r"0.11\% fitted mass outside the shown range", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.12),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An example in the spirit of genomics: a thousand z-scores, ninety percent from true"
            " nulls and ten percent from real effects of various sizes. <bookmark mark='b'/> The nonparametric "
            "maximum likelihood prior, estimated from the z-scores alone, <bookmark mark='c'/> puts eighty-nine "
            "percent of its mass near zero, <bookmark mark='d'/> and much of the remainder in two fitted clumps. The "
            "generating nonnull effects were normal with standard deviation three, not concentrated at those two "
            "points."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def winners(self):
        d = load("winners")
        P = ShrinkagePlot(d["z_top"], d["tweedie_top"], d["theta_top"], x_range=(3, 8.5), width=10.4, center=[0.6, 0.3, 0], gap=1.6,
                          labels={"raw": r"top 10 $z$", "shrunk": "Tweedie", "truth": "true effect"}, ticks=[3, 4, 5, 6, 7, 8],
                          colors={"raw": RAW, "shrunk": SHRUNK, "truth": TRUE})
        rows = fit_rows(VGroup(
            label(rf"the ten largest $z$: \ average {d['mean_z_top']:.2f}", font_size=22, color=RAW),
            label(rf"their true effects: \ average {d['mean_theta_top']:.2f}: \ the winner's curse", font_size=22, color=TRUE),
            label(rf"Tweedie's estimates: \ average {d['mean_tw_top']:.2f}", font_size=22, color=SHRUNK),
        ), 12.0, 0.22, [0, -2.9, 0])
        head=label("Selection inflates extreme estimates; shrinkage uses all observations",font_size=36).move_to([0,3.3,0])
        if head.width>12.5:head.width=12.5
        with self.voiceover(
            "<bookmark mark='a'/> Now select the ten largest z-scores, the discoveries. Their average is five point six one. "
            "<bookmark mark='b'/> But the true effects behind them average only five point oh seven: they were selected "
            "partly for being lucky. This is the winner's curse, and it's why the first report of a large effect is so "
            "often followed by smaller ones. <bookmark mark='c'/> Tweedie's formula, using the estimated prior, pulls the "
            "selected estimates back to an average of four point eight four. Because the correction comes from the whole "
            "distribution, it applies even after selection."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(P.lines), FadeIn(P.names), FadeIn(P.ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in P.raw], lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in P.truth], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(a) for a in P.arrows], lag_ratio=0.05), LaggedStart(*[FadeIn(x) for x in P.shrunk], lag_ratio=0.05),
                      FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()
