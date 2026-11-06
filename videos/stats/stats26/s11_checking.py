from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class Checking(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.schools()
        self.visits()
        self.conservative()
        self.prior_predictive()

    def card(self):
        card = chapter_card(10, r"Checking", r"Could the model have produced these data?", lit=(1984,), part=PART)
        with self.voiceover("Chapter ten. Model checking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"y^{\text{rep}}", r"\sim", r"p(y^{\text{rep}} \mid y) = \textstyle\int p(y^{\text{rep}} \mid \theta)\, p(\theta \mid y)\, d\theta", font_size=28),
            cmath(r"T(y)", r":", r"\text{a feature the model might get wrong}", font_size=30),
            cmath(r"p_B", r"=", r"P\{T(y^{\text{rep}}) \ge T(y) \mid y\}", font_size=32),
            cmath(r"\text{read}", r":", r"p_B \text{ near 0 or 1: \ the model misses that feature}", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"replicated data from the fitted model"), why(r"zeros, \ extremes, \ spread"),
                why(r"Rubin (1984); \ Gelman, Meng \& Stern (1996)"), why(r"a check, \ not a test of truth")]
        with self.voiceover(
            "<bookmark mark='a'/> A posterior is only as good as its model, and Bayesian inference never says so on its own. "
            "Posterior predictive checking asks: if the fitted model were true, what data would it produce? Draw parameters "
            "from the posterior, then replicated data sets. <bookmark mark='b'/> Pick a feature of the data the model might "
            "get wrong. <bookmark mark='c'/> Compare the real data's value with the replicates': the posterior predictive "
            "p-value of Donald Rubin, and Andrew Gelman, Xiao-Li Meng and Hal Stern. <bookmark mark='d'/> A value near zero "
            "or one says the model doesn't reproduce that feature."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def schools(self):
        d = load("ppc")["school"]
        panels = VGroup()
        anims = []
        for k, (key, name) in enumerate((("max", r"largest effect"), ("min", r"smallest effect"), ("sd", r"SD of the effects"))):
            P = d[key]
            e, h = np.asarray(P["edges"]), np.asarray(P["hist"], float)
            h = h / h.sum() / (e[1] - e[0])
            A = axes([float(e[0]), float(e[-1])], [0, float(h.max()) * 1.15], x_length=3.8, y_length=2.8, xlabel=name,
                     ylabel=r"", xticks=[], yticks=[], center=[-4.5 + 4.5 * k, 0.7, 0])
            bars = hist_bars(A.ax, e, h, color=POST, opacity=0.6)
            obs = Line(A.ax.c2p(P["obs"], 0), A.ax.c2p(P["obs"], float(h.max()) * 1.15), color=PATH, stroke_width=4)
            pl = label(rf"$y$: \ {P['obs']:.1f}; \ $p_B = {P['p']:.2f}$", font_size=22, color=PATH).next_to(A, DOWN, buff=0.25)
            panels.add(A)
            anims.append((bars, obs, pl))
        foot = fit_rows(VGroup(
            label(r"orange: \ 20,000 replicated sets of eight estimates from the hierarchical model", font_size=22, color=POST),
            label(r"yellow: \ the real eight schools; \ nothing unusual", font_size=22, color=PATH),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The eight schools, checked. Twenty thousand replicated sets of eight estimates from the "
            "fitted hierarchical model. <bookmark mark='b'/> The real largest estimate, school A's twenty-eight, is typical: "
            "about half the replicates have a larger maximum. <bookmark mark='c'/> The smallest, minus three, is a little "
            "high but unremarkable. <bookmark mark='d'/> And the spread of the eight is ordinary too. The model reproduces "
            "the features we'd worry about, including that one large effect at A."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(panels), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                if k == 0:
                    vo.wait_until("a")
                vo.wait_until(m_)
                bars, obs, pl = anims[k]
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), Create(obs), FadeIn(pl))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def visits(self):
        d = load("ppc")
        e = np.asarray(d["edges"])
        hp, hn = np.asarray(d["zero_pois"], float), np.asarray(d["zero_nb"], float)
        hp, hn = hp / hp.sum() / (e[1] - e[0]), hn / hn.sum() / (e[1] - e[0])
        A = axes([0, 0.6], [0, float(max(hp.max(), hn.max())) * 1.1], x_length=7.4, y_length=4.2, xlabel=r"share of adults with no visits",
                 ylabel=r"replicated", xticks=[0, 0.2, 0.4, 0.6], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bp = hist_bars(ax, e, hp, color=RES, opacity=0.6)
        bn = hist_bars(ax, e, hn, color=SHRUNK, opacity=0.6)
        obs = Line(ax.c2p(d["zero_obs"], 0), ax.c2p(d["zero_obs"], float(max(hp.max(), hn.max())) * 1.1), color=PATH, stroke_width=4)
        rows = fit_rows(VGroup(
            label(rf"500 of the World's adults: \ {100 * d['zero_obs']:.0f}\% had no visits", font_size=22, color=PATH),
            label(rf"red: \ Poisson replicates; \ $p_B = {d['p_pois']:.3f}$", font_size=22, color=RES),
            label(rf"green: \ negative binomial; \ $p_B = {d['p_nb']:.2f}$", font_size=22, color=SHRUNK),
            label(rf"mean {d['mean']:.2f}, \ variance {d['var']:.1f}: \ overdispersed", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the doctor visits from chapter four, where the Poisson model's interval missed. Of five "
            "hundred adults, forty-three percent saw no doctor all year. <bookmark mark='b'/> Replicated data from the "
            "fitted Poisson model have about eleven percent zeros, never more than seventeen: the check's p-value is zero, "
            "and the model is plainly wrong. <bookmark mark='c'/> A negative binomial model, Part 24's, reproduces the zeros easily, "
            "with a p-value of point four seven. <bookmark mark='d'/> The sample variance, eleven point six, is five times the "
            "mean; the check makes that failure impossible to miss."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(obs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bp], lag_ratio=0.01), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bn], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def conservative(self):
        rows = fit_rows(VGroup(
            label(r"posterior predictive $p$-values use the data twice: \ to fit, \ then to check", font_size=24),
            label(r"so they are not uniform under the model: \ they pile up near $\tfrac12$", font_size=24, color=RES),
            label(r"a check that fails is informative; \ one that passes is weak evidence", font_size=24, color=PATH),
            label(r"calibrated versions: \ cross-validated, \ or held-out checks", font_size=24, color=SHRUNK),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One caution. These p-values use the data twice, once to fit and once to check, "
            "<bookmark mark='b'/> so even when the model is right they aren't uniform; they crowd towards a half. "
            "<bookmark mark='c'/> A failed check, like the Poisson's, is real news. A passed check, like the schools', is "
            "weaker evidence than it looks. <bookmark mark='d'/> Calibrated alternatives check each observation against a "
            "fit made without it, or check against fresh data."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def prior_predictive(self):
        d = load("priorpred")
        e = np.asarray(d["edges"])
        A = axes([0, 1], [0, 9], x_length=7.4, y_length=4.2, xlabel=r"predicted probability, \ before any data",
                 ylabel=r"prior predictive density", xticks=[0, 0.5, 1], yticks=[0, 4, 8], center=[-2.0, 0.3, 0])
        ax = A.ax
        bw = hist_bars(ax, e, np.minimum(d["wide"]["hist"], 9), color=RES, opacity=0.55)
        bk = hist_bars(ax, e, np.minimum(d["weak"]["hist"], 9), color=SHRUNK, opacity=0.6)
        rows = fit_rows(VGroup(
            label(r"logistic regression, \ 5 standardized predictors", font_size=22),
            label(rf"red: \ coefficients $\sim N(0, 10^2)$: \ {100 * d['wide']['extreme']:.0f}\% below 1\% or above 99\%", font_size=22, color=RES),
            label(rf"green: \ $N(0, 1)$: \ {100 * d['weak']['extreme']:.0f}\%", font_size=22, color=SHRUNK),
            label(r"the `vague' prior is a strong belief in near-certainty", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Prior predictive checks run the same idea before seeing data: simulate from the prior and "
            "the model, and ask whether the results are believable. A logistic regression with five standardized "
            "predictors. <bookmark mark='b'/> With 'vague' normal priors of standard deviation ten on every coefficient, the "
            "model predicts that eighty-three percent of people have a probability below one percent or above ninety-nine: "
            "it is nearly sure of every outcome before it has seen one. <bookmark mark='c'/> Standard normal priors give six "
            "percent, a far more sensible belief. <bookmark mark='d'/> Flat-looking priors on one scale can be strong "
            "beliefs on the scale that matters, chapter three's lesson, caught by simulation."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bw], lag_ratio=0.01), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bk], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
