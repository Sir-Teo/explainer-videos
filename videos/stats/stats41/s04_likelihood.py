from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Likelihood(VoiceoverScene):
    def construct(self):
        self.card()
        self.air()
        self.em_steps()
        self.buck()
        self.scatter_fill()
        self.path()
        self.why_em()
        self.louis()
        self.fiml()

    def card(self):
        card = chapter_card(3, r"Likelihood under MAR", r"Use everything you saw", lit=(1977,), part=PART)
        with self.voiceover("Chapter three. Likelihood under missing at random."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def air(self):
        d = load("em")
        rows = fit_rows(VGroup(
            label(rf"New York, \ May to September 1973: \ {d['n']} days of ozone, \ sunlight, \ wind and temperature", font_size=26),
            label(rf"ozone missing on {d['n_miss_oz']} days, \ solar radiation on {d['n_miss_solar']}", font_size=26, color=GREY_A),
            label(rf"complete cases: \ {d['n_cc']} days; \ a quarter of the data thrown away", font_size=26, color=CCC),
            label(r"MAR is plausible: \ the monitor's failures need not depend on the ozone", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real data set with holes: daily air quality in New York from May to September 1973, "
            "one of R's oldest examples. <bookmark mark='b'/> Ozone is missing on " + str(d["n_miss_oz"]) + " of the "
            + str(d["n"]) + " days, and solar radiation on " + str(d["n_miss_solar"]) + ". <bookmark mark='c'/> Dropping "
            "incomplete days leaves " + str(d["n_cc"]) + ", throwing away a quarter of the data. <bookmark mark='d'/> Missing "
            "at random is plausible: the monitors failed for reasons that need not depend on the ozone that day, and "
            "temperature and wind, always recorded, carry information about it."
        ) as vo:
            self.add(air_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def em_steps(self):
        rows = [
            cmath(r"\text{E-step}", r":", r"E[x_{\text{mis}} \mid x_{\text{obs}}] = \mu_m + \Sigma_{mo} \Sigma_{oo}^{-1} (x_o - \mu_o)", font_size=28),
            cmath(r"\phantom{E}", r"\;", r"\text{and } \text{Var}[x_{\text{mis}} \mid x_{\text{obs}}] = \Sigma_{mm} - \Sigma_{mo} \Sigma_{oo}^{-1} \Sigma_{om}", font_size=28),
            cmath(r"\text{M-step}", r":", r"\mu = \tfrac1n \textstyle\sum \hat x_i, \ \ \Sigma = \tfrac1n \textstyle\sum (\hat x_i \hat x_i^\top + C_i) - \mu\mu^\top", font_size=28),
            cmath(r"\text{repeat}", r":", r"\text{the observed log-likelihood rises at every step}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"Part 5's conditional normal"), why(r"the uncertainty of the fill"), why(r"complete-data MLE, \ with $C_i$"),
                why(r"Dempster, \ Laird \& Rubin (1977)")]
        with self.voiceover(
            "<bookmark mark='a'/> For a multivariate normal with holes, EM alternates two steps. The E-step replaces each "
            "missing block by its conditional expectation given that row's observed values, Part five's regression formula, "
            "<bookmark mark='b'/> and remembers the conditional variance, the uncertainty of the fill. <bookmark mark='c'/> "
            "The M-step computes the usual mean and covariance from the filled data, adding those variances back, so the "
            "spread is not understated. <bookmark mark='d'/> Arthur Dempster, Nan Laird and Donald Rubin proved in 1977 that "
            "the observed-data likelihood never decreases."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scatter_fill(self):
        d = load("em")
        temp, oz = np.asarray(d["temp"], float), np.asarray(d["ozone"], dtype=float)
        miss = np.asarray(d["miss"], bool)
        A = axes([55, 100], [0, 170], x_length=7.4, y_length=4.2, xlabel=r"temperature ($^\circ$F)", ylabel=r"ozone (ppb)",
                 xticks=[60, 70, 80, 90, 100], yticks=[0, 50, 100, 150], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        obs = scatter(ax, temp[~miss], np.clip(oz[~miss], 0, 168), OBSV, 0.05)
        fills = np.asarray(d["fills"], float)
        fdots = scatter(ax, temp[miss], np.clip(fills, 0, 168), IMPC, 0.06)
        rugs = VGroup(*[Line(ax.c2p(t, 0), ax.c2p(t, 6), color=IMPC, stroke_width=2) for t in temp[miss]])
        side = fit_rows(VGroup(
            label(r"blue: \ days with ozone measured", font_size=22, color=OBSV),
            label(r"gold ticks: \ days without it, \ at their temperature", font_size=22, color=IMPC),
            label(r"gold dots: \ EM's conditional means", font_size=22, color=IMPC),
            label(r"each on the regression, \ given that day's sun, \ wind and heat", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Ozone against temperature on the days it was measured. <bookmark mark='b'/> The gold ticks "
            "mark the days with no ozone reading, at their temperatures; they are spread across the range. <bookmark "
            "mark='c'/> EM's E-step places each at its conditional mean given that day's sunlight, wind and temperature. "
            "<bookmark mark='d'/> The filled values sit on the regression surface; the M-step's added variance accounts for "
            "the scatter they lack."
        ) as vo:
            self.add(air_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(obs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(rugs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(fdots), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def path(self):
        d = load("em")
        ll = np.asarray(d["ll"], float)
        it = np.arange(len(ll))
        lo = float(np.floor(ll.min() / 10) * 10)
        hi = float(np.ceil(ll.max() / 10) * 10)
        A = axes([0, len(ll) - 1], [lo, hi], x_length=6.0, y_length=4.0, xlabel=r"EM iteration", ylabel=r"observed log-likelihood",
                 xticks=list(range(0, len(ll), 3)), yticks=[lo, (lo + hi) / 2, hi], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-3.0, 0.2, 0])
        ax = A.ax
        c = polyline(ax, it, ll, TAUC, 3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=TAUC) for a, b in zip(it, ll)])
        side = fit_rows(VGroup(
            label(rf"converged in {d['iters']} iterations", font_size=22, color=TAUC),
            label(rf"mean ozone, \ complete cases: \ {d['cc_mean']:.1f}", font_size=22, color=CCC),
            label(rf"mean ozone, \ EM: \ {d['em_mean']:.1f}", font_size=22, color=MIC),
            label(rf"missing days just as hot: \ {d['temp_miss_mean']:.1f} vs {d['temp_obs_mean']:.1f}$^\circ$F", font_size=22, color=GREY_A),
        ), 5.0, 0.42, [4.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The observed log-likelihood climbs at every iteration and settles within "
            + str(d["iters"]) + ". <bookmark mark='b'/> The mean ozone from the complete cases is " + say(d["cc_mean"], 1)
            + " parts per billion; <bookmark mark='c'/> EM's maximum likelihood estimate is " + say(d["em_mean"], 1) + ". "
            "<bookmark mark='d'/> They are close, because the days without readings were, on average, just as hot as the "
            "others. EM helps most when the missing differ on the observed predictors; and it always gives the right "
            "spread, which complete cases need not."
        ) as vo:
            self.add(air_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(c), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why_em(self):
        rows = [
            cmath(r"\log f(y_{\text{obs}} \mid \theta)", r"=", r"Q(\theta \mid \theta_t) - H(\theta \mid \theta_t)", font_size=30),
            cmath(r"Q", r"=", r"E_{\theta_t}[\log f(y_{\text{obs}}, y_{\text{mis}} \mid \theta) \mid y_{\text{obs}}]", font_size=30),
            cmath(r"H(\theta \mid \theta_t)", r"\le", r"H(\theta_t \mid \theta_t): \ \text{Jensen}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{raising } Q \text{ raises the likelihood \ (Part 22's EM)}", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"an identity"), why(r"the expected complete log-likelihood"), why(r"a Kullback--Leibler gap"), why(r"monotone ascent")]
        with self.voiceover(
            "<bookmark mark='a'/> Why EM climbs. The observed log-likelihood splits into Q, the expected complete-data "
            "log-likelihood, minus a term H. <bookmark mark='b'/> Q averages the complete log-likelihood over the missing "
            "values' conditional distribution at the current guess. <bookmark mark='c'/> By Jensen's inequality, H is "
            "largest at the current guess. <bookmark mark='d'/> So any step that raises Q raises the likelihood, the "
            "argument of Part twenty-two, here with the missing values as the latent variables."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fiml(self):
        rows = fit_rows(VGroup(
            label(r"full-information ML: \ each row contributes the likelihood of what it has", font_size=26, color=MIC),
            label(r"the standard in structural equation software; \ the same answer as EM", font_size=26),
            label(r"standard errors: \ the observed information, \ not EM's complete-data one \ (Louis 1982)", font_size=26, color=TAUC),
            label(r"its weakness: \ one model for everything; \ change the analysis, \ refit the model", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Maximizing the observed-data likelihood directly is called full-information maximum "
            "likelihood: each row contributes the likelihood of whatever it has. <bookmark mark='b'/> It is the standard in "
            "structural equation software, and gives the same estimates as EM. <bookmark mark='c'/> Its standard errors must "
            "come from the observed information, which Thomas Louis showed in 1982 how to extract from EM. <bookmark "
            "mark='d'/> Its weakness is that the missing-data model and the analysis are one and the same; every new "
            "analysis needs a new likelihood. Multiple imputation separates them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def buck(self):
        rows = [
            cmath(r"\text{Buck (1960)}", r":", r"\text{regress each variable on the others, \ fill the holes}", font_size=30),
            cmath(r"\text{then}", r":", r"\text{add the residual variance back to the covariance}", font_size=30),
            cmath(r"\text{iterate}", r":", r"\text{until nothing changes: \ that is EM}", font_size=30),
            cmath(r"\text{lesson}", r":", r"\text{filling is fine if the uncertainty is put back}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"an early method"), why(r"the correction"), why(r"seventeen years before EM"), why(r"the theme of the part")]
        with self.voiceover(
            "<bookmark mark='a'/> The idea is older than EM. In 1960 S. F. Buck filled holes in a multivariate data set by "
            "regressing each variable on the others. <bookmark mark='b'/> Crucially, he added the residual variance back "
            "when computing the covariance matrix, so the filled values did not shrink it. <bookmark mark='c'/> Repeat until "
            "nothing changes, and you have the EM algorithm for the normal, seventeen years before it had a name. <bookmark "
            "mark='d'/> The lesson runs through this part: filling holes is fine, as long as the uncertainty is put back."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def louis(self):
        rows = [
            cmath(r"I_{\text{obs}}", r"=", r"I_{\text{complete}} - I_{\text{missing}}", font_size=32),
            cmath(r"\text{EM's speed}", r":", r"\text{the rate is the fraction of missing information}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{much missing information: \ slow EM, \ wide intervals}", font_size=30),
            cmath(r"\text{SEs}", r":", r"\text{Louis (1982), \ SEM (Meng \& Rubin 1991), \ or the bootstrap}", font_size=28),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"the missing information principle"), why(r"Dempster et al."), why(r"one number, \ two meanings"), why(r"three routes")]
        with self.voiceover(
            "<bookmark mark='a'/> The information in the observed data is the information we would have had with complete "
            "data, minus the information the holes took away: Orchard and Woodbury's missing information principle. "
            "<bookmark mark='b'/> EM's rate of convergence is exactly the fraction of information missing, <bookmark "
            "mark='c'/> so a slow EM is a warning that the data say little, and the intervals will be wide. <bookmark "
            "mark='d'/> Standard errors come from Louis's formula, from Meng and Rubin's supplemented EM, or from the "
            "bootstrap."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

