from __future__ import annotations

from videos.stats.stats53.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.model()
        self.result()
        self.lesson()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1986,)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"1986: \ Persi Diaconis and David Freedman, \ ``On inconsistent Bayes estimates of location''", font_size=28),
            label(r"a location problem: \ estimate the centre $\theta$ of a symmetric distribution", font_size=26, color=GREY_A),
            label(r"a reasonable Bayesian: \ a prior on $\theta$, \ and a Dirichlet-process prior on the shape", font_size=26, color=PRIORC),
            label(r"the data come from a nice, \ symmetric distribution centred at 0", font_size=26, color=TRUTHC),
            label(r"the posterior for $\theta$ never settles at 0: \ it need not concentrate on the true centre", font_size=26, color=BADC),
        ), 12.4, 0.55, [0, -0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1986, Persi Diaconis and David Freedman published a paper on inconsistent Bayes estimates of location that unsettled a generation of Bayesians. <bookmark mark='b'/> The problem could hardly be simpler: estimate the centre of a symmetric distribution. <bookmark mark='c'/> Their Bayesian was reasonable: a smooth prior on the centre, and a Dirichlet-process prior, the standard nonparametric choice, on the shape of the distribution, symmetrized about the centre. <bookmark mark='d'/> The data came from a perfectly well-behaved symmetric distribution, centred at zero. <bookmark mark='e'/> And as the data grew, the posterior for the centre did not settle at zero. Their constructed model shows that increasing the sample size need not force posterior concentration at the true centre."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"X_i = \theta + \varepsilon_i", r":", r"\varepsilon_i \sim F, \ F \text{ symmetric about } 0", font_size=34),
            cmath(r"\text{prior}", r":", r"\theta \sim \text{a smooth density}, \ \ F \sim \text{symmetrized DP}(\alpha, \text{Cauchy})", font_size=30),
            cmath(r"\text{truth}", r":", r"\theta_0 = 0, \ F_0 \text{ a smooth symmetric density, \ chosen carefully}", font_size=30),
            cmath(r"\text{the posterior for } \theta", r":", r"\text{can fail to concentrate near }0\text{ in their constructed setting}", font_size=32),
        ]
        rows[1][-1].set_color(PRIORC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"a symmetric location model"), why(r"Ferguson's prior (1973)"), why(r"infinitely many such $F_0$"), why(r"inconsistent")]
        heading = label('A prior can remain influential in an infinite-dimensional model', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The model: observations equal a centre plus symmetric noise. <bookmark mark='b'/> The prior: a smooth density for the centre, and for the noise distribution, Thomas Ferguson's Dirichlet process of 1973, symmetrized, with a Cauchy base measure. <bookmark mark='c'/> The truth: centre zero, and a smooth symmetric noise density, which they constructed, within the class used for their counterexample. <bookmark mark='d'/> The posterior need not concentrate at the true centre. That is a statement about posterior mass, not about every possible point estimate: a symmetric two-mode distribution can have its mean exactly at zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def result(self):
        rows = [
            cmath(r"\text{Doob (1949)}", r":", r"\text{consistent for prior-almost every truth}", font_size=34),
            cmath(r"\text{Freedman (1963)}", r":", r"\text{generic inconsistency in specified infinite-dimensional settings}", font_size=32),
            cmath(r"\text{Diaconis \& Freedman (1986)}", r":", r"\text{and it happens for a natural prior, \ on a natural truth}", font_size=30),
            cmath(r"\text{the moral}", r":", r"\text{in infinite dimensions, \ the prior does not wash out by itself}", font_size=32),
        ]
        rows[0][-1].set_color(GOODC)
        rows[1][-1].set_color(BADC)
        rows[3][-1].set_color(BALLC)
        whys = [why(r"chapter 1"), why(r"a residual set"), why(r"the shock"), why(r"chapters 2--11")]
        heading = label('Prior-almost-everywhere consistency does not cover every fixed truth', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> How could this happen? Joseph Doob had proved in 1949 that a Bayesian is consistent for almost every truth, almost every in the sense of the prior itself. <bookmark mark='b'/> David Freedman had shown in 1963 that the exceptional set, though of prior probability zero, can be large in another sense: in specific infinite-dimensional model and prior spaces, genericity results can make inconsistency topologically large. This is not a statement about every prior in every infinite-dimensional model. <bookmark mark='c'/> Diaconis and Freedman's example made it concrete, with a prior people actually used, on a truth nobody would call strange. <bookmark mark='d'/> The moral: with infinitely many parameters, the prior does not wash out on its own. Which priors do, at what rate, and whether their credible sets can be trusted, is the subject of this part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the questions:", font_size=28, color=GREY_A),
            label(r"when does a posterior concentrate at the truth? \ (Doob, \ Schwartz)", font_size=26, color=POSTC),
            label(r"how fast? \ (Ghosal, \ Ghosh \& van der Vaart)", font_size=26, color=POSTC),
            label(r"when does it look like a normal centred at an efficient estimator? \ (Bernstein--von Mises)", font_size=26, color=FREQC),
            label(r"and when is a 95\% credible set a 95\% confidence set?", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The questions, then. <bookmark mark='b'/> When does a posterior concentrate at the truth, "
            "Doob's and Schwartz's question? <bookmark mark='c'/> How fast, the question of Ghosal, Ghosh and van der Vaart? "
            "<bookmark mark='d'/> When does the posterior look like a normal distribution centred at an efficient estimator, "
            "the Bernstein–von Mises question? <bookmark mark='e'/> And the one practitioners care about most: when is a "
            "ninety-five percent credible set also a ninety-five percent confidence set?"
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(26, r"the posterior summarizes uncertainty; \ the prior washes out with data", r"finitely many parameters",
                         r"chapters 1--5: \ when it washes out, \ and when not"),
            upgrade_card(47, r"Le Cam's LAN and local asymptotic normality", r"frequentist estimators",
                         r"chapter 4: \ Bernstein--von Mises, \ from LAN"),
            upgrade_card(50, r"minimax rates over smoothness classes", r"frequentist estimators",
                         r"chapters 3, \ 7--10: \ posteriors at the same rates"),
        ]
        for c in cards:
            c.scale(0.86)
        stack = VGroup(*cards).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises come due. Part twenty-six said the prior washes out as data accumulate, for "
            "models with finitely many parameters; chapters one to five ask when it does in general. <bookmark mark='b'/> Part "
            "forty-seven built local asymptotic normality for frequentist estimators; chapter four uses it to prove the "
            "Bernstein–von Mises theorem. <bookmark mark='c'/> And Part fifty found minimax rates; chapters three and seven to "
            "ten ask whether Bayesian posteriors contract at those rates, and adapt to unknown smoothness."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(stack[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 53", font_size=34, color=GREY_B), label(r"Bayesian Asymptotics and Nonparametric Bayes", font_size=44)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Doob's and Schwartz's theorems; \ contraction rates from prior mass, \ entropy and tests",
            r"Bernstein--von Mises, \ parametric and semiparametric, \ and its failures",
            r"Dirichlet processes, \ Pólya trees, \ Gaussian processes; \ adaptation by empirical and hierarchical Bayes",
            r"when credible sets cover; \ spike-and-slab and the horseshoe; \ misspecification and generalized posteriors",
        ], color=BALLC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 26, \ 47, \ 50").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.bnp}, \ the contraction ball").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-three: Bayesian asymptotics and nonparametric Bayes. <bookmark mark='b'/> We'll "
            "prove Doob's theorem and Schwartz's, and find contraction rates from prior mass, entropy and tests; prove "
            "Bernstein–von Mises in parametric and semiparametric models, and see where it fails; meet Dirichlet processes, "
            "Pólya trees and Gaussian processes, with adaptation by empirical and hierarchical Bayes; and find when credible "
            "sets cover, how the spike-and-slab and horseshoe priors behave, and what happens to a posterior when the model "
            "is wrong."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
