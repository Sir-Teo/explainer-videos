from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Neyman(VoiceoverScene):
    def construct(self):
        self.card()
        self.variance()
        self.why_cons()
        self.numbers()
        self.dist()
        self.board()
        self.bounds()

    def card(self):
        card = chapter_card(5, r"Neyman's variance", r"Repeated randomization of a fixed science", lit=(1923,), part=PART)
        with self.voiceover("Chapter five. Neyman's variance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def variance(self):
        rows = [
            cmath(r"\hat\tau", r"=", r"\bar Y_1 - \bar Y_0, \ \ E\hat\tau = \bar\tau", font_size=32),
            cmath(r"\mathrm{Var}\,\hat\tau", r"=", r"\dfrac{S_1^2}{n_1} + \dfrac{S_0^2}{n_0} - \dfrac{S_\tau^2}{n}", font_size=32),
            cmath(r"S_1^2, \ S_0^2, \ S_\tau^2", r":", r"\text{variances of } Y(1), \ Y(0), \ \tau \text{ over the } n \text{ units}", font_size=28),
            cmath(r"\widehat{\mathrm{Var}}", r"=", r"\dfrac{s_1^2}{n_1} + \dfrac{s_0^2}{n_0} \ \ \ge \ \text{the truth on average}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"unbiased over the design"), why(r"Neyman (1923): \ sampling without replacement"),
                why(r"finite-population variances, \ divisor $n - 1$"), why(r"$S_\tau^2$ cannot be estimated")]
        with self.voiceover(
            "<bookmark mark='a'/> Neyman asked a different question from Fisher. Not whether the effect is zero, but how "
            "precisely the difference in means estimates the average effect, over repeated randomizations of the same "
            "fixed patients. It is unbiased, as we saw. <bookmark mark='b'/> Its variance, which Neyman derived by treating "
            "the treated group as a sample drawn without replacement from the patients, is S one squared over n one, plus "
            "S nought squared over n nought, minus S tau squared over n. <bookmark mark='c'/> The S's are the variances, "
            "across the patients, of the treated outcomes, the untreated outcomes, and the individual effects. <bookmark "
            "mark='d'/> The first two can be estimated from the two arms. The third cannot, because no patient shows us "
            "their effect. So the usual estimate drops it, and is too large on average: conservative."
        ) as vo:
            intro=label('Neyman variance describes complete randomization of a fixed population',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_cons(self):
        rows = [
            cmath(r"\text{constant effect}", r":", r"S_\tau^2 = 0, \ \text{the estimate is unbiased}", font_size=30),
            cmath(r"\text{heterogeneous}", r":", r"S_\tau^2 > 0, \ \text{the estimate overstates}", font_size=30),
            cmath(r"\text{the } -S_\tau^2/n \text{ term}", r":", r"\text{units' effects partly cancel across arms}", font_size=28),
            cmath(r"\text{superpopulation}", r":", r"\text{the term disappears: } s_1^2/n_1 + s_0^2/n_0 \text{ is right}", font_size=28),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"Fisher's world"), why(r"the usual world"), why(r"a finite population gives back a little"),
                why(r"for the PATE, \ not the SATE")]
        with self.voiceover(
            "<bookmark mark='a'/> If every patient had the same effect, S tau would be zero and the usual estimate "
            "would be exactly unbiased. <bookmark mark='b'/> When effects vary, it overstates the variance. <bookmark"
            " mark='c'/> The subtracted term reflects a finite population: a patient in the treated group is, by that"
            " fact, absent from the control group, and the two arms' errors partly cancel. <bookmark mark='d'/> If "
            "instead we want the average effect in a superpopulation from which the patients were sampled "
            "independently and identically, the extra sampling variation exactly restores the missing term, and the "
            "usual estimate is right. The conservative formula is the correct one for the population average."
        ) as vo:
            intro=label('Heterogeneous effects create a gap in the conservative variance',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("neyman")
        rows = [[r"quantity", r"value"],
                [r"$S_1$, \ $S_0$ \ (mm Hg)", rf"{d['S1']:.2f}, \ {d['S0']:.2f}"],
                [r"$S_\tau$", rf"{d['S_tau']:.2f}"],
                [r"true SD of $\hat\tau$", rf"{d['true_sd']:.3f}"],
                [r"conservative SD", rf"{d['cons_sd']:.3f}"],
                [r"SD over 4,000 re-randomizations", rf"{d['sim_sd']:.3f}"],
                [r"constant-effect science: \ true = conservative", rf"{d['const_true']:.3f}"]]
        tab = table_rows(rows, font_size=26, col_buff=1.0, row_buff=0.28,
                         colors=[GREY_A, None, TAUC, BANDC, Y0C, None, GREY_B]).move_to([0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the World we can compute every term. The patients' treated and untreated outcomes "
            "vary with standard deviations of about ten; their individual effects, with a standard deviation of "
            + say(d["S_tau"], 1) + ". <bookmark mark='b'/> The true standard deviation of the estimate, with a thousand "
            "patients per arm, is " + say(d["true_sd"], 3) + "; the conservative formula gives " + say(d["cons_sd"], 3)
            + ". <bookmark mark='c'/> Re-randomizing the same two thousand patients four thousand times gives "
            + say(d["sim_sd"], 3) + ", matching the true value. <bookmark mark='d'/> Here the effects vary much less than the "
            "outcomes do, so the conservative formula is only three percent too large."
        ) as vo:
            self.add(trial_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(tab[5]))
            vo.wait_until("d")
            self.play(FadeIn(tab[6]))
        self.clear_scene()

    def dist(self):
        d = load("neyman")
        h, e = np.asarray(d["hist"], float), np.asarray(d["edges"], float)
        lo, hi = float(e[0]), float(e[-1])
        A = axes([lo, hi], [0, 1.15 * h.max() / h.sum() / (e[1] - e[0])], x_length=7.4, y_length=4.2,
                 xlabel=r"$\hat\tau$ over re-randomizations (mm Hg)", ylabel=r"density",
                 xticks=[round(lo, 1), round(d["ate"], 1), round(hi, 1)], yticks=[0, 0.5], xfmt=lambda v: rf"{v:.1f}",
                 yfmt=lambda v: rf"{v:.1f}", center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / h.sum() / (e[1] - e[0]), color=ESTC, opacity=0.6)
        xs = np.linspace(lo, hi, 200)
        nor = curve(ax, xs, np.exp(-0.5 * ((xs - d["ate"]) / d["true_sd"]) ** 2) / (d["true_sd"] * np.sqrt(2 * np.pi)), TAUC, 3)
        side = fit_rows(VGroup(
            label(r"4,000 re-randomizations \ of the same patients", font_size=22),
            label(r"gold: \ normal with Neyman's SD", font_size=22, color=TAUC),
            label(rf"90\% intervals cover the SATE: \ {100 * d['cover']:.1f}\%", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The randomization distribution of the estimate, over four thousand draws of the "
            "coin. <bookmark mark='b'/> It is close to normal, with Neyman's standard deviation, as a "
            "finite-population central limit theorem predicts when neither arm is dominated by a few extreme units. "
            "<bookmark mark='c'/> Ninety percent intervals built from the conservative standard error cover the "
            "trial's average effect " + say(100 * d["cover"], 1) + " percent of the time: slightly above ninety percent in this example. A conservative variance supports "
            "asymptotic coverage under regularity; it does not by itself guarantee finite-sample normal-interval "
            "coverage."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(nor), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def board(self):
        rows = board_rows("randomized, \\ Neyman")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: the randomized trial with Neyman's conservative interval, over a "
                   "thousand fresh randomizations. Kept. Set it beside the doctor's choice from chapter three, which never "
                   "covered at all.",
                   [("a", [0])])

    def bounds(self):
        rows = fit_rows(VGroup(
            label(r"$S_\tau^2$ is not identified, \ but it is bounded by the marginals", font_size=26),
            label(r"its smallest possible value: \ pair the sorted $Y(1)$'s with the sorted $Y(0)$'s", font_size=26, color=TAUC),
            label(r"a sharper, \ still valid, \ variance estimate \ (Aronow, \ Green \& Lee 2014)", font_size=26, color=BANDC),
            label(r"the general lesson: \ some features of the science are beyond any experiment", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The variance of the effects cannot be estimated, but it can be bounded, because we "
            "do know the distributions of the treated and untreated outcomes separately. <bookmark mark='b'/> Its "
            "smallest value consistent with those distributions comes from pairing the sorted treated outcomes with "
            "the sorted untreated ones. <bookmark mark='c'/> Peter Aronow, Donald Green and Donald Lee used this in "
            "2014 to sharpen Neyman's variance estimate while retaining asymptotic validity under their regularity "
            "conditions. <bookmark mark='d'/> The lesson is more general: some features of the science, such as the "
            "exact share of patients harmed, are not generally identified by a parallel-arm randomized trial alone."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
