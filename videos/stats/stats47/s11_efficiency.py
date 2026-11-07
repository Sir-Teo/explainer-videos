from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class TestEfficiency(VoiceoverScene):
    def construct(self):
        self.card()
        self.pitman()
        self.table()
        self.design()
        self.bahadur()
        self.chart()
        self.which()

    def card(self):
        card = chapter_card(10, r"Efficiency of tests", r"How many more observations does the worse test need?", part=PART)
        with self.voiceover("Chapter ten. The efficiency of tests: how many more observations does the worse test need?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pitman(self):
        rows = [
            cmath(r"\mathrm{ARE}_{1,2}", r"=", r"\lim \frac{n_2}{n_1} \ \text{for equal power at } \theta_n = \theta_0 + h/\sqrt n", font_size=32),
            cmath(r"\text{efficacy}", r":", r"e = \mu'(\theta_0) / \sigma(\theta_0), \ \ T_n \approx N(\mu(\theta), \sigma^2/n)", font_size=32),
            cmath(r"\mathrm{ARE}_{1,2}", r"=", r"(e_1 / e_2)^2 = (\tau_1/\tau_2)^2 \ \ \text{(chapter 8's shifts)}", font_size=32),
            cmath(r"\text{sign vs } t, \ \text{normal}", r":", r"(\sqrt{2/\pi})^2 = 2/\pi = 0.637", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Pitman (1948), \ local alternatives"), why(r"slope over spread"), why(r"the third lemma"), why(r"57\% more data")]
        with self.voiceover(
            "<bookmark mark='a'/> Edwin Pitman's efficiency compares two tests by the ratio of sample sizes they need for the "
            "same power against the same local alternatives. <bookmark mark='b'/> Each test statistic has an efficacy: the "
            "rate at which its mean moves with theta, divided by its spread. <bookmark mark='c'/> The relative efficiency is "
            "the squared ratio of efficacies, which are chapter eight's shifts tau per unit h. <bookmark mark='d'/> For the "
            "sign test against the t test at the normal, two over pi: point six four. That number, and Wilcoxon's point "
            "nine five five, are Pitman efficiencies."
        ) as vo:
            heading=label('Pitman efficiency compares local sample-size requirements',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        rows = [[r"test vs $t$", r"normal", r"logistic", r"Laplace", r"$t_3$", r"worst case"],
                [r"sign", r"0.637", r"0.822", r"2.000", r"1.62", r"1/3 \ (symmetric unimodal); \ 0 \ (general symmetric)"],
                [r"Wilcoxon", r"0.955", r"1.097", r"1.500", r"1.90", r"0.864"],
                [r"normal scores", r"1.000", r"1.047", r"1.273", r"1.64", r"1 \ (Chernoff--Savage)"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.35, colors=[GREY_A, HODC, GOODC, S.ACCENT]).move_to([0, 0.7, 0])
        note_ = label(r"Pitman efficiencies against the $t$ test, \ symmetric shift alternatives \ (Hodges \& Lehmann 1956; \ Lehmann 1975)", font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        if note_.width > 12.6:
            note_.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> The classic table. <bookmark mark='b'/> The sign test loses efficiency at the "
            "normal, but has twice the local efficiency at the Laplace. Its often quoted one-third lower bound needs "
            "symmetric unimodal densities; over arbitrary symmetric bimodal densities, central density can vanish and"
            " sign efficiency can approach zero. <bookmark mark='c'/> Wilcoxon's test is never below point eight six "
            "four and beats t for every heavy-tailed law shown. <bookmark mark='d'/> And under the continuous "
            "finite-variance regularity conditions of Chernoff–Savage, the normal-scores ARE is at least one: a rank "
            "test that costs nothing at the normal and gains elsewhere."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def bahadur(self):
        rows = [
            cmath(r"\text{exact slope}", r":", r"-\tfrac2n \log p_n \to c(\theta) \ \text{a.s.\ under a fixed } \theta \ne \theta_0", font_size=30),
            cmath(r"z \text{ test}", r":", r"c(\theta) = \theta^2", font_size=34),
            cmath(r"\text{sign test}", r":", r"c(\theta) = 2\, \mathrm{KL}\big(\mathrm{Bern}(\Phi(\theta)) \,\|\, \mathrm{Bern}(\tfrac12)\big)", font_size=32),
            cmath(r"\text{Bahadur efficiency}", r"=", r"c_1(\theta)/c_2(\theta) \ \to \ \text{Pitman's, \ as } \theta \to \theta_0", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Bahadur (1960): \ how fast $p \to 0$"), why(r"large deviations, \ Part 43"), why(r"Chernoff--Sanov"), why(r"usually")]
        with self.voiceover(
            "<bookmark mark='a'/> Raghu Raj Bahadur's alternative fixes the alternative and asks how fast the p-value goes to "
            "zero: minus two over n times its log converges to the exact slope. <bookmark mark='b'/> For the z test the slope "
            "is theta squared. <bookmark mark='c'/> For the sign test it is twice a Kullback–Leibler divergence between "
            "coins, from Part forty-three's large deviations. <bookmark mark='d'/> The ratio of slopes is the Bahadur "
            "efficiency, and as the alternative approaches the null it usually tends to the Pitman efficiency."
        ) as vo:
            heading=label('Bahadur slopes describe fixed-alternative p-value decay',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("bahadur")
        th = np.asarray(d["theta"])
        A = axes([0, 2.5], [0.3, 1.0], x_length=7.4, y_length=4.4, xlabel=r"a fixed alternative $\theta$", ylabel=r"Bahadur efficiency, \ sign vs $z$",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5], yticks=[0.4, 0.6, 2 / np.pi, 0.8, 1.0], yfmt=lambda v: f"{v:.2f}", center=[-2.5, 0.2, 0])
        ax = A.ax
        cr = polyline(ax, th, d["ratio"], HODC, 4)
        pit = DashedLine(ax.c2p(0, d["pitman"]), ax.c2p(2.5, d["pitman"]), color=GOODC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"normal data: \ the sign test against the $z$ test", font_size=22),
            label(r"red: \ the ratio of exact slopes", font_size=22, color=HODC),
            label(r"green: \ Pitman's $2/\pi$, \ the limit at $\theta \to 0$", font_size=22, color=GOODC),
            label(r"far alternatives: \ the sign test is relatively worse", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For normal data, the sign test against the z test. <bookmark mark='b'/> The ratio of exact "
            "slopes, as the alternative moves away from zero. <bookmark mark='c'/> At small theta it approaches Pitman's two "
            "over pi, in green. <bookmark mark='d'/> For distant alternatives it falls further: the sign test's p-values "
            "shrink more slowly than the z test's when the evidence is overwhelming, because a sign can only say plus or "
            "minus."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ Kullback--Leibler divergences")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cr), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pit), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def which(self):
        rows = fit_rows(VGroup(
            label(r"Pitman: \ hard problems, \ alternatives near the null: \ what matters for design", font_size=26, color=GOODC),
            label(r"Bahadur: \ easy problems, \ how decisively a test rejects", font_size=26, color=S.ACCENT),
            label(r"Hodges--Lehmann efficiency: \ fixed alternative, \ power $\to 1$, \ type II errors", font_size=26, color=GREY_A),
            label(r"they can disagree: \ choose the one that matches the question", font_size=26, color=HODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which efficiency should one use? Pitman's describes hard problems, with alternatives near "
            "the null, which is what matters when designing a study to detect a small effect. <bookmark mark='b'/> "
            "Bahadur's describes easy problems, and how decisively a test rejects. <bookmark mark='c'/> A third, Hodges and "
            "Lehmann's, fixes the alternative and compares how fast the type two error goes to zero. <bookmark mark='d'/> "
            "They can disagree, and the right one is the one that matches the scientific question."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def design(self):
        rows = [
            cmath(r"\text{a } t \text{ test with } n = 100", r":", r"80\% \text{ power against some small shift}", font_size=32),
            cmath(r"\text{the sign test}", r":", r"n \approx 100 \times \pi/2 = 157 \ \text{for the same power}", font_size=32),
            cmath(r"\text{Wilcoxon}", r":", r"n \approx 100 / 0.955 = 105", font_size=34),
            cmath(r"\text{if the data are Laplace}", r":", r"\text{Wilcoxon needs } 67, \ \text{the sign test } 50", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a planned study"), why(r"57\% more patients"), why(r"5\% more"), why(r"efficiencies 1.5 and 2")]
        with self.voiceover(
            "<bookmark mark='a'/> Pitman efficiencies approximate sample-size ratios in the local large-sample "
            "regime; they are not exact finite-sample power calculations. Suppose a t test with a hundred "
            "observations has eighty percent power against a small shift. <bookmark mark='b'/> The sign test needs "
            "about a hundred and fifty-seven for the same power, if the data are normal. <bookmark mark='c'/> "
            "Wilcoxon's test needs about a hundred and five. <bookmark mark='d'/> But if the errors are Laplace, "
            "Wilcoxon needs only sixty-seven and the sign test fifty. In a clinical trial, these are patients."
        ) as vo:
            heading=label('Asymptotic efficiencies approximate design sample-size ratios',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
