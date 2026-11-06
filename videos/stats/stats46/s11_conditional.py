from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Conditional(VoiceoverScene):
    def construct(self):
        self.card()
        self.welch()
        self.buehler()
        self.table()
        self.betting()
        self.resolution()

    def card(self):
        card = chapter_card(10, r"Conditional inference", r"Does 95\% hold for \emph{this} data set?", lit=(1959,), part=PART)
        with self.voiceover("Chapter ten. Conditional inference: does ninety-five percent hold for this data set?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def welch(self):
        rows = [
            cmath(r"x_1, x_2 \sim U(\theta - \tfrac12, \theta + \tfrac12)", r":", r"C = [\min x_i, \ \max x_i]", font_size=32),
            cmath(r"P_\theta(\theta \in C)", r"=", r"P(\text{one above } \theta, \text{ one below}) = \tfrac12", font_size=32),
            cmath(r"\text{but if } \max - \min > \tfrac12", r":", r"\theta \in C \ \text{for certain}", font_size=32),
            cmath(r"\text{a 50\% interval}", r":", r"\text{and sometimes we can see that it is right}", font_size=32),
        ]
        rows[2][-1].set_color(REJC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"two observations"), why(r"exact coverage"), why(r"the range is ancillary"), why(r"Welch (1939)")]
        with self.voiceover(
            "<bookmark mark='a'/> Bernard Welch's example of 1939. Two observations from a uniform distribution of width one "
            "centred at theta; take the interval between them. <bookmark mark='b'/> It covers theta exactly when one "
            "observation falls on each side, which has probability one half: a fifty percent confidence interval. <bookmark "
            "mark='c'/> But if the two observations are more than a half apart, theta must lie between them: the interval "
            "is certainly right. <bookmark mark='d'/> Reporting fifty percent confidence for a statement known to be true is "
            "absurd. Part forty-five's answer was to condition on the ancillary range."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def buehler(self):
        rows = [
            cmath(r"B \text{ a relevant subset}", r":", r"P_\theta(\theta \in C \mid X \in B) \ge 1 - \alpha + \varepsilon \ \ \forall \theta", font_size=30),
            cmath(r"\text{or}", r":", r"\le 1 - \alpha - \varepsilon \ \ \forall \theta \ \ \text{(negatively biased)}", font_size=30),
            cmath(r"\text{the } t \text{ interval}, \ n = 2", r":", r"B = \{|\bar x| / s \le 1 + \sqrt 2\}: \ \text{coverage} > 1 - \alpha \ \text{always}", font_size=28),
            cmath(r"\text{so}", r":", r"\text{someone who sees } B \text{ can bet against the stated level and win}", font_size=30),
        ]
        rows[2][-1].set_color(REJC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"Buehler (1959)"), why(r"either direction"), why(r"Buehler \& Feddersen (1963); \ Brown (1967)"), why(r"a recognizable subset")]
        with self.voiceover(
            "<bookmark mark='a'/> Robert Buehler made the worry precise in 1959. A relevant subset is a set of samples, "
            "recognizable from the data alone, on which the interval's conditional coverage is bounded away from its stated "
            "level, at every value of the parameter, <bookmark mark='b'/> above it or below it. <bookmark mark='c'/> Even "
            "Student's t interval has them. With two normal observations, Buehler and Feddersen, and then Lawrence Brown, "
            "showed that on the set where the mean is small compared with the standard deviation, the fifty percent t "
            "interval covers more than half the time, whatever the true mean and variance. <bookmark mark='d'/> Someone who "
            "can see the set can bet against the stated confidence, at the stated odds, and expect to win."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("buehler")
        rows = [[r"$\mu/\sigma$"] + [f"{r['mu']:g}" for r in d["rows"]],
                [r"coverage, \ overall"] + [f"{100 * r['overall']:.1f}\\%" for r in d["rows"]],
                [r"coverage on $B$"] + [f"{100 * r['conditional']:.1f}\\%" for r in d["rows"]],
                [r"share of samples in $B$"] + [f"{100 * r['share']:.0f}\\%" for r in d["rows"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.35, colors=[GREY_A, H0C, REJC, GREY_A]).move_to([0, 0.8, 0])
        if tab.width > 13:
            tab.width = 13
        note_ = label(r"the 50\% $t$ interval $\bar x \pm s/\sqrt2$, \ $n = 2$; \ $B = \{|\bar x|/s \le 1 + \sqrt 2\}$; \ 200,000 samples each", font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Simulated, at six values of mu over sigma. <bookmark mark='b'/> The overall coverage is "
            "fifty percent, as advertised, at every one. <bookmark mark='c'/> On the recognizable set it is sixty-one percent "
            "at worst and eighty-six at best: never fifty. <bookmark mark='d'/> And the set is not rare: it contains most "
            "samples when the mean is small."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_), FadeIn(exact_tag(r"simulated: 200,000 samples per column")))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def betting(self):
        rows = fit_rows(VGroup(
            label(r"Buehler's betting game: \ you state $C(x)$ with confidence $1 - \alpha$; \ I may bet against it at those odds", font_size=24),
            label(r"if I can win on average whatever $\theta$ is, \ your confidence is incoherent", font_size=26, color=REJC),
            label(r"Robinson (1979): \ a general theory of relevant and semi-relevant subsets", font_size=24, color=GREY_A),
            label(r"intervals that are posterior intervals for a proper prior \ have no relevant subsets", font_size=26, color=UMPC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Buehler's framing is a betting game. You announce an interval with confidence one minus "
            "alpha; I may bet against it at the odds you implied. <bookmark mark='b'/> If I have a strategy that wins on "
            "average whatever theta is, your stated confidence is incoherent for the case in hand. <bookmark mark='c'/> "
            "Geoffrey Robinson's 1979 theory of relevant and semi-relevant subsets made this systematic; for the t "
            "interval the bettor's edge is small in large samples. <bookmark mark='d'/> And intervals that are also Bayesian posterior intervals under a proper prior admit "
            "no relevant subsets at all: Part forty-five's theme, that the good frequentist procedures are Bayes in "
            "disguise, appears again."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def resolution(self):
        rows = fit_rows(VGroup(
            label(r"in practice:", font_size=28, color=GREY_A),
            label(r"condition on ancillaries when they exist: \ Welch, \ Cox, \ the observed information", font_size=26, color=UMPC),
            label(r"otherwise report the procedure's guarantee as what it is: \ an average over repetitions", font_size=26),
            label(r"and prefer procedures whose conditional behaviour is close to their stated level", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What should a practitioner do? <bookmark mark='b'/> Condition on ancillary statistics when "
            "they exist, as Welch's and Cox's examples demand. <bookmark mark='c'/> Otherwise, describe a confidence level "
            "for what it is: a guarantee about the procedure over repetitions, not a probability for the case in hand. "
            "<bookmark mark='d'/> And when choosing among procedures, prefer those whose conditional behaviour stays close to "
            "their stated level."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
