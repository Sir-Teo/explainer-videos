from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.berkeley()
        self.risk()
        self.unrelated()
        self.question()
        self.upgrades()
        self.objectives()

    def berkeley(self):
        tl = timeline(lit=(1956, 1961)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"Berkeley, \ 1954--55: \ the Third Symposium on Mathematical Statistics and Probability", font_size=26, color=GREY_A),
            label(r"Charles Stein: \ for three or more normal means, \ the sample means are \emph{inadmissible}", font_size=26, color=JSC),
            label(r"another estimator has smaller expected squared error \ for every value of the means", font_size=26),
            label(r"1961: \ with Willard James, \ an explicit one: \ the James--Stein estimator", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> At the Third Berkeley Symposium, held in 1954 and 1955 and published in 1956, "
            "Charles Stein presented a result that many statisticians at first refused to believe. <bookmark "
            "mark='b'/> If you estimate three or more normal means, each from its own observation, the obvious "
            "estimate, the observations themselves, is inadmissible. <bookmark mark='c'/> There is another estimator "
            "whose expected squared error is smaller for every possible value of the means, with no exceptions. "
            "<bookmark mark='d'/> In 1961, with Willard James, he wrote one down: the James–Stein estimator, which "
            "shrinks every observation toward zero."       ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def risk(self):
        d = load("hook")
        nrm = np.asarray(d["norm2"])
        A = axes([0, 30], [0, 1.15], x_length=7.4, y_length=4.4, xlabel=r"$\|\theta\|^2$", ylabel=r"risk $/\, p$",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        mle = polyline(ax, [0, 30], [1, 1], MLEC, 4)
        cols = {3: S.ALT, 5: S.PRIOR, 10: JSC}
        js = {p: polyline(ax, nrm, np.asarray(d[f"js{p}"]) / p, c, 4) for p, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"$X \sim N_p(\theta, I)$; \ loss $\|\hat\theta - \theta\|^2$", font_size=22),
            label(r"blue: \ $\hat\theta = X$, \ risk $p$ everywhere", font_size=22, color=MLEC),
            label(r"$\hat\theta_{JS} = \big(1 - \tfrac{p - 2}{\|X\|^2}\big) X$", font_size=22, color=JSC),
            label(r"exact risk: \ teal $p = 3$, \ purple $5$, \ green $10$", font_size=22, color=JSC),
            label(r"at $\theta = 0$: \ risk 2 for every $p\ge3$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the claim, drawn exactly. Observe X, normal with mean vector theta and "
            "identity covariance in p dimensions, and pay the squared distance from your estimate to theta. <bookmark"
            " mark='b'/> The obvious estimate, X itself, has expected loss p, whatever theta is: the flat blue line, "
            "divided by p. <bookmark mark='c'/> James and Stein multiply X by one minus p minus two over the squared "
            "length of X. <bookmark mark='d'/> Its risk, computed exactly from a Poisson mixture of chi-squares, lies"
            " below the line everywhere, in three, five and ten dimensions. <bookmark mark='e'/> At theta equal to "
            "zero the risk is two, for every dimension at least three; far away it creeps back up to p, but never "
            "reaches it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ Poisson mixtures of $\chi^2$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mle), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[Create(js[p]) for p in (3, 5, 10)], FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def unrelated(self):
        rows = fit_rows(VGroup(
            label(r"$\theta_1$: \ the price of tea in Leeds; \ $\theta_2$: \ a hitter's average; \ $\theta_3$: \ a star's brightness", font_size=26),
            label(r"measure each once, \ with unit noise", font_size=26, color=GREY_A),
            label(r"the combined estimate shrinks all three \ toward 0, \ by a common factor", font_size=26, color=JSC),
            label(r"its \emph{total} squared error is smaller on average, \ for every $(\theta_1, \theta_2, \theta_3)$", font_size=26, color=S.ACCENT),
            label(r"no single coordinate is guaranteed to improve", font_size=26, color=INADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What made the result so hard to accept is that the coordinates need have nothing to"
            " do with each other: the price of tea in Leeds, a hitter's batting average, the brightness of a star. "
            "<bookmark mark='b'/> Measure each once, with independent unit-variance Gaussian noise after choosing the"
            " measurement scale and squared-error weights. <bookmark mark='c'/> The James–Stein estimate shrinks all "
            "three toward zero by a common factor that depends on all three measurements. <bookmark mark='d'/> And "
            "its total squared error is smaller on average, for every combination of tea, hitter and star. <bookmark "
            "mark='e'/> The catch, which we will make precise, is that the guarantee is for the total; no single "
            "coordinate is promised an improvement."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"what does ``best'' mean for an estimator?", font_size=36, color=S.ACCENT),
            label(r"Wald (1950): \ a game against nature, \ scored by risk", font_size=28),
            label(r"sufficiency, \ completeness, \ equivariance: \ when a best estimator exists", font_size=28, color=ADMC),
            label(r"Stein, \ and Brown (1971): \ why it fails in three dimensions, \ and what Brownian motion has to do with it", font_size=26, color=JSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So this part asks what best means for an estimator. <bookmark mark='b'/> Abraham Wald's "
            "decision theory gives the language: estimation as a game against nature, each strategy scored by its risk. "
            "<bookmark mark='c'/> Sufficiency, completeness and equivariance tell us when a best estimator exists within a "
            "natural class. <bookmark mark='d'/> And Stein's paradox, explained by Lawrence Brown in 1971 through the "
            "recurrence of Brownian motion from Part forty-four, shows where that search for the best runs out."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(9, r"the UMVUE is the best unbiased estimator; \ the Cram\'er--Rao bound", r"best means best among unbiased ones",
                         r"chapters 1--8: \ risk, \ admissibility, \ Lehmann--Scheff\'e proved, \ and where unbiasedness is absurd"),
            upgrade_card(25, r"James--Stein beats the raw averages on Efron--Morris's hitters", r"a simulation, \ and a sketch of Stein's lemma",
                         r"chapters 10--13: \ exact risks, \ why three dimensions, \ proper Bayes minimax rules"),
        ]
        for c in cards:
            c.scale(0.9)
        VGroup(*cards).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises are due. Part nine called the minimum-variance unbiased estimator best and "
            "proved the Cramér–Rao bound, but best only among unbiased estimators; chapters one to eight set out what best "
            "means in general, prove Lehmann–Scheffé, and show where unbiasedness becomes absurd. <bookmark mark='b'/> Part "
            "twenty-five showed James–Stein winning on Efron and Morris's hitters, by simulation and a sketch; chapters ten "
            "to thirteen give exact risks, the reason for three dimensions, and proper Bayes estimators that are minimax."
        ) as vo:
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 45", font_size=34, color=GREY_B), label(r"The Theory of Estimation", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"risk, \ admissibility, \ minimax and Bayes rules; \ risk sets and complete classes",
            r"exponential families as convex duality; \ sufficiency, \ completeness, \ ancillarity",
            r"Rao--Blackwell, \ Lehmann--Scheff\'e, \ information bounds, \ equivariance",
            r"Stein's lemma, \ James--Stein, \ Brown's theorem, \ empirical Bayes",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 9, \ 25, \ 43").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.decision}, \ the risk-set explorer").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-five: the theory of estimation. <bookmark mark='b'/> We'll set up risk, "
            "admissibility, minimax and Bayes rules, and draw the risk set of a whole problem; read exponential families as "
            "convex duality; prove the sufficiency theorems, Rao–Blackwell and Lehmann–Scheffé, with Basu's theorem and the "
            "information bounds; find best equivariant estimators; and then follow Stein, Brown and Robbins to the frontier "
            "of shrinkage and empirical Bayes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
