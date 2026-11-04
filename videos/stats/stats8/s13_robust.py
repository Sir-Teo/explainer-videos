from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403

DISTS = [("normal", r"normal", S.EST), ("uniform", r"uniform", S.LIK), ("t5", r"$t_5$", S.POST), ("exponential", r"exponential", S.RESID)]


class Robust(VoiceoverScene):
    def construct(self):
        self.card()
        self.sizes()
        self.why()
        self.onesided()
        self.box()

    def card(self):
        card = chapter_card(12, r"How robust is normal theory?", r"When the data are not normal", lit=(1953,), part=PART)
        with self.voiceover("Chapter twelve. How robust is normal theory?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sizes(self):
        d = load("robust")
        A = axes([-0.5, 3.5], [0, 0.26], x_length=6.0, y_length=4.4, ylabel=r"false-alarm rate, \ nominal 5\%", xticks=[],
                 yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], center=[-2.6, -0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(-0.5, 0.05), ax.c2p(3.5, 0.05), color=GREY_B, stroke_width=2)
        groups = VGroup()
        for k, (key, nm, c) in enumerate(DISTS):
            vt, vf = d["t"][key], d["F"][key]
            bt = Rectangle(width=0.34, height=max(0.01, ax.c2p(0, vt)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=c, fill_opacity=0.9)
            bt.move_to(ax.c2p(k - 0.2, vt / 2))
            bf = Rectangle(width=0.34, height=max(0.01, ax.c2p(0, vf)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=c, fill_opacity=0.4)
            bf.move_to(ax.c2p(k + 0.2, vf / 2))
            lt = MathTex(f"{100 * vt:.1f}", font_size=20, color=c).next_to(bt, UP, buff=0.05)
            lf = MathTex(f"{100 * vf:.1f}", font_size=20, color=c).next_to(bf, UP, buff=0.05)
            nmL = label(nm, font_size=22, color=c).next_to(ax.c2p(k, 0), DOWN, buff=0.25)
            groups.add(VGroup(bt, lt, bf, lf, nmL))
        leg = VGroup(label(r"solid: \ the $t$-test for a mean", font_size=22), label(r"faded: \ the $F$-test for variances", font_size=22))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 2.2, 0])
        rows = fit_rows(VGroup(
            label(r"$t$: \ near 5\% except under strong skew", font_size=24, color=S.EST),
            label(r"$F$: \ 1\% to 23\%: \ ruled by the tails", font_size=24, color=S.RESID),
            label(r"samples of 10; \ variances matched", font_size=20, color=GREY_A),
        ), 4.8, 0.3, [4.4, 0.2, 0])
        tag = note(r"simulated: 20,000 samples per bar").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Normal theory gives exact answers for normal data. How wrong are they when the data aren't normal? "
            "<bookmark mark='a'/> Test a mean with the t-test, at the five percent level, when the null hypothesis is "
            "true, with samples of ten from four distributions. For normal, uniform and t with five degrees of freedom, "
            "the false-alarm rate stays close to five percent. Only the strongly skewed exponential pushes it to ten. "
            "<bookmark mark='b'/> Now test whether two variances are equal with the F-test. For normal data, five "
            "percent. For uniform data, one percent: far too cautious. For t five, twelve and a half; for the "
            "exponential, twenty-three. <bookmark mark='c'/> The t-test for means is fairly robust. The F-test for "
            "variances is not robust at all."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(tag), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(gp[0], gp[1], gp[4])) for gp in groups], FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(gp[2], gp[3])) for gp in groups], FadeIn(rows[1:]))
            vo.wait_until("c")
            self.play(Indicate(rows[1], color=S.RESID))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"\bar x", r"\approx", r"\text{normal by the CLT, \ whatever the data}", font_size=32),
            cmath(r"\mathrm{Var}(s^2)", r"=", r"\sigma^4\Big(\frac{2}{n - 1} + \frac{\kappa}{n}\Big)", font_size=34),
            cmath(r"\kappa = 6\ (t_5,\ \text{exponential})", r":\ ", r"\mathrm{Var}(s^2) \text{ is } 4\times \text{ the normal theory value at } n = 10",
                  font_size=28),
        ]
        rows[1][2].set_color(S.RESID)
        whys = [why(r"the $t$ statistic leans on the mean: \ protected by averaging"),
                why(r"$\kappa$: \ the excess kurtosis; \ normal theory assumes $\kappa = 0$"),
                why(r"the $F$-test's reference distribution is simply wrong, \ at every $n$")]
        with self.voiceover(
            "Why the difference? <bookmark mark='a'/> The t statistic leans on the sample mean, which the central limit "
            "theorem makes nearly normal whatever the data. <bookmark mark='b'/> The F-test leans on the variance of "
            "the sample variance, and that depends on the data's kurtosis, the heaviness of the tails, through a term "
            "that never goes away. Normal theory assumes the excess kurtosis is zero. <bookmark mark='c'/> For "
            "distributions with excess kurtosis six, the sample variance is four times as variable as normal theory "
            "says at n equals ten, so the F-test's reference distribution is wrong, and more data doesn't fix it."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def box(self):
        hc = history_card(1953, r"George Box, \ ``Non-normality and tests on variances''", r"\emph{Biometrika} 40: \ to test variances "
                          r"before an analysis of variance is like ``putting to sea in a rowing boat to find out whether conditions are "
                          r"sufficiently calm for an ocean liner to leave port''", color=S.MUSEUM, width=9.6, font_size=24).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"he also coined the word \emph{robust} for statistics", font_size=24, color=GREY_A),
            label(r"lesson: \ check what a method assumes, \ and which assumptions it actually leans on", font_size=26, color=S.ACCENT),
            label(r"remedies: \ Levene-type tests, \ the bootstrap (Part 16), \ robust statistics (Part 30)", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> George Box made this point in 1953, in the paper where he introduced the word robust "
            "into statistics. Testing whether variances are equal before an analysis of variance, he wrote, is like "
            "putting to sea in a rowing boat to find out whether conditions are calm enough for an ocean liner to "
            "leave port: the preliminary test is far more fragile than the analysis it's meant to protect. "
            "<bookmark mark='b'/> The lesson is to know which assumptions a method actually leans on. "
            "<bookmark mark='c'/> Remedies for comparing spreads come later: tests based on absolute deviations, the "
            "bootstrap in Part 16, and robust statistics in Part 30."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def onesided(self):
        d = load("extras")["tails"]
        rows = fit_rows(VGroup(
            label(r"exponential data, \ $n = 10$, \ the two-sided $t$-test at 5\%:", font_size=26),
            MathTex(rf"\text{{rejects too low: }} {100 * d['lo']:.1f}\%\qquad \text{{too high: }} {100 * d['hi']:.1f}\%", font_size=30, color=RESID),
            label(r"nominal: \ 2.5\% in each tail", font_size=24, color=GREY_A),
            label(r"a right-skewed sample: \ big $\bar x$ comes with big $s$, \ small $\bar x$ with small $s$", font_size=24),
            label(r"the errors don't cancel: \ one-sided conclusions can be badly wrong (Part 16's bootstrap-$t$)", font_size=24,
                  color=S.ACCENT),
        ), 12.6, 0.35, [0, 0.2, 0])
        with self.voiceover(
            "There's more to the exponential's ten percent than a number. <bookmark mark='a'/> Split it by tail. "
            "<bookmark mark='b'/> The test rejects in the lower tail nine and a half percent of the time, and in the "
            "upper tail less than half a percent. <bookmark mark='c'/> Each should be two and a half. "
            "<bookmark mark='d'/> In a right-skewed sample, a high mean comes with a high standard deviation, damping "
            "the t statistic, and a low mean with a low one, inflating it. <bookmark mark='e'/> The two errors don't "
            "cancel; they pile up on one side. A one-sided conclusion from skewed data can be badly wrong even when "
            "the two-sided rate looks tolerable. Part 16's bootstrap-t is built to fix exactly this."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
