from __future__ import annotations

from videos.stats.stats26.common import *  # noqa: F403


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.exchangeable()
        self.definetti()
        self.partial()
        self.everywhere()

    def card(self):
        card = chapter_card(1, r"Upgrade", r"What Part 15 assumed", lit=(1931,), part=PART)
        with self.voiceover("Chapter one. The upgrade."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        card = upgrade_card(15, r"choose a prior, \ multiply by the likelihood, \ normalize: \ the posterior is the answer",
                            r"one parameter, \ a prior chosen by hand, \ and a model nobody checked",
                            r"many related parameters with a prior learned from the data; \ priors with reasons; \ "
                            r"tests, \ decisions and checks", width=11.4)
        with self.voiceover(
            "<bookmark mark='a'/> Part 15 laid down Bayes's machinery: choose a prior, multiply by the likelihood, "
            "normalize, and the posterior is the answer. <bookmark mark='b'/> It quietly assumed one parameter at a time, "
            "a prior picked by hand, and a model taken on trust. <bookmark mark='c'/> This part removes all three: many "
            "related parameters whose prior is partly learned from the data, priors chosen for reasons, and the tests, "
            "decisions and checks that make a Bayesian analysis a complete one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.wait(0.5)
        self.clear_scene()

    def exchangeable(self):
        rows = [
            cmath(r"p(\theta_1, \dots, \theta_J)", r"=", r"p(\theta_{\pi(1)}, \dots, \theta_{\pi(J)}) \ \text{for every permutation } \pi", font_size=28),
            cmath(r"\text{meaning}", r":", r"\text{the labels A to H carry no information}", font_size=30),
            cmath(r"\text{not}", r":", r"\text{independent: \ learning } \theta_A \text{ changes beliefs about } \theta_B", font_size=28),
            cmath(r"\text{iid given } \phi", r"\Rightarrow", r"\text{exchangeable}", font_size=30),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"Part 5's exchangeability"), why(r"before seeing the data, \ schools are alike"),
                why(r"that is how they borrow strength"), why(r"the converse is de Finetti's theorem")]
        intro = label('Sharing information requires a stated exchangeability judgement', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> What justifies a prior that ties the schools together? Part 5's exchangeability: our "
            "beliefs about the eight true effects don't change if we shuffle the schools' labels. <bookmark mark='b'/> "
            "Before seeing any data, we have no reason to expect school A to differ from school E. <bookmark mark='c'/> "
            "Exchangeable doesn't mean independent: if we learned that coaching worked wonders at A, we'd expect more of it "
            "at B too, and that is exactly how the schools borrow strength. <bookmark mark='d'/> Effects drawn "
            "independently from a common distribution are exchangeable."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def definetti(self):
        rows = [
            cmath(r"\text{de Finetti}", r":", r"\text{infinitely exchangeable } \Rightarrow \ p(\theta_{1:J}) = \int \prod_j p(\theta_j \mid \phi)\, p(\phi)\, d\phi", font_size=26),
            cmath(r"\phi", r"=", r"(\mu, \tau): \ \text{the hyperparameters}", font_size=30),
            cmath(r"p(\phi)", r":", r"\text{the hyperprior}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{normal population and hyperprior are additional choices}", font_size=28),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"de Finetti (1931), \ Hewitt \& Savage (1955)"), why(r"the population the schools come from"),
                why(r"uncertainty about that population"), why(r"Part 5, \ now put to work")]
        intro = label('Infinite exchangeability motivates a mixture; normality is an extra choice', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> An infinitely exchangeable sequence can be represented as draws that are "
            "independent and identically distributed given a random population distribution. Eight exchangeable "
            "effects alone do not guarantee this infinite extension. <bookmark mark='b'/> We additionally choose a "
            "normal population described by mu and tau. Normality is a modelling assumption, not de Finetti's "
            "conclusion. <bookmark mark='c'/> A hyperprior describes uncertainty about these population parameters. "
            "<bookmark mark='d'/> Exchangeability motivates sharing information; the population family and hyperprior"
            " still require justification."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def partial(self):
        rows = fit_rows(VGroup(
            label(r"exchangeable given what we know: \ add covariates when schools differ in known ways", font_size=24),
            label(r"school size, \ coaching hours: \ $\theta_j \sim N(x_j^\top\beta, \tau^2)$", font_size=24, color=SHRUNK),
            label(r"not exchangeable: \ a ninth `school' that is a university", font_size=24, color=RES),
            label(r"judgement enters here, \ and it should be stated", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Exchangeability is a judgement, and it can be conditional. If schools differed in a known "
            "way, say in the hours of coaching offered, we would make them exchangeable given that, <bookmark mark='b'/> by "
            "putting the covariate into the population model, as the radon counties got their uranium in Part 25. "
            "<bookmark mark='c'/> A university's programme would not belong in the same exchangeable group at all. "
            "<bookmark mark='d'/> This is where judgement enters a Bayesian analysis, and it should be stated openly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def everywhere(self):
        rows = fit_rows(VGroup(
            label(r"hospitals, \ schools, \ counties: \ Part 25's league tables and small areas", font_size=24, color=SHRUNK),
            label(r"opinion polls: \ multilevel regression and post-stratification for every state", font_size=24),
            label(r"genes: \ thousands of effects sharing one prior \ (Part 33)", font_size=24),
            label(r"sport: \ players' skills; \ medicine: \ trials in a meta-analysis", font_size=24),
            label(r"wherever many related units each have little data", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hierarchical models are everywhere this judgement fits. Hospitals, schools and counties, "
            "Part 25's league tables and small areas. <bookmark mark='b'/> Election forecasts that estimate opinion in every "
            "state from one national poll, by multilevel regression and post-stratification. <bookmark mark='c'/> Thousands of "
            "genes whose effects share one prior, Part 33's subject. <bookmark mark='d'/> Players' skills in sport, and trials "
            "in a medical meta-analysis. <bookmark mark='e'/> Wherever many related units each have little data, the "
            "hierarchy lets them inform each other."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
