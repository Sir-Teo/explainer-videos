from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class AIPW(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.why_()
        self.world()
        self.kang()
        self.table()
        self.board()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Double robustness", r"Two chances to be right", lit=(1994, 2007), part=PART)
        with self.voiceover("Chapter nine. Double robustness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def formula(self):
        rows = [
            cmath(r"\psi_i", r"=", r"\hat\mu_1(x_i) - \hat\mu_0(x_i) + \dfrac{T_i (Y_i - \hat\mu_1(x_i))}{\hat e(x_i)} - \dfrac{(1 - T_i)(Y_i - \hat\mu_0(x_i))}{1 - \hat e(x_i)}", font_size=24),
            cmath(r"\hat\tau_{\rm AIPW}", r"=", r"\tfrac1n \textstyle\sum_i \psi_i, \ \ \widehat{\mathrm{se}} = \mathrm{sd}(\psi)/\sqrt n", font_size=30),
            cmath(r"\text{reading}", r":", r"\text{g-computation, \ plus IPW of its residuals}", font_size=30),
            cmath(r"\text{or}", r":", r"\text{IPW, \ plus a regression correction}", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"augmented IPW"), why(r"Robins, \ Rotnitzky \& Zhao (1994)"), why(r"fix the outcome model's errors"),
                why(r"stabilize the weights")]
        with self.voiceover(
            "<bookmark mark='a'/> Combine the two strategies. For each patient, take g-computation's predicted effect, and "
            "add inverse-probability-weighted corrections from the residuals of the outcome models. <bookmark mark='b'/> "
            "Average these, and take the standard error from their spread. This augmented inverse probability weighted "
            "estimator was introduced by James Robins, Andrea Rotnitzky and Lue Ping Zhao in 1994. <bookmark mark='c'/> One "
            "reading is g-computation, corrected by weighting its own mistakes. <bookmark mark='d'/> The other is IPW, with "
            "the outcome model removing most of the noise that the weights would amplify."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_(self):
        rows = [
            cmath(r"\hat\mu \text{ right}", r":", r"E[Y - \mu_t \mid X] = 0: \ \text{the corrections vanish on average}", font_size=28),
            cmath(r"\hat e \text{ right}", r":", r"\text{the corrections exactly undo } \hat\mu\text{'s bias}", font_size=28),
            cmath(r"\text{either one}", r"\Rightarrow", r"\text{consistent: \ double robustness}", font_size=30),
            cmath(r"\text{both right}", r"\Rightarrow", r"\text{the smallest possible variance}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"whatever the weights"), why(r"whatever the outcome model"), why(r"two chances"),
                why(r"the efficient influence function, \ Part 49")]
        with self.voiceover(
            "<bookmark mark='a'/> Its key property: if the outcome models are right, the residual corrections average to "
            "zero whatever the weights, so the estimate is consistent. <bookmark mark='b'/> If instead the propensity model is "
            "right, the weighted residuals exactly cancel the outcome models' bias, whatever it is. <bookmark mark='c'/> So "
            "the estimator is consistent if either model is right: doubly robust. <bookmark mark='d'/> And when both are "
            "right, its variance is the smallest that any regular estimator can achieve under these assumptions, because psi "
            "is the efficient influence function, which Part 49 derives."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world(self):
        d = load("obs")
        a = d["aipw"]
        rows = fit_rows(VGroup(
            label(rf"the World's study: \ AIPW ${a['est']:.2f}$ \ [{a['lo']:.1f}, \ {a['hi']:.1f}]", font_size=26, color=BANDC),
            label(rf"IPW ${d['ipw']['est']:.2f}$; \ g-computation ${d['gcomp']:.2f}$; \ truth ${d['ate']:.2f}$", font_size=26, color=GREY_A),
            label(rf"standard error {a['se']:.2f}, \ against IPW's {d['ipw']['se']:.2f}", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World's study, the doubly robust estimate is minus " + say(-a["est"], 1) + ", "
            "<bookmark mark='b'/> very close to the truth, with an interval that covers it. <bookmark mark='c'/> And its "
            "standard error is about two thirds of IPW's: the outcome models absorb most of the noise."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def kang(self):
        rows = [
            cmath(r"Z", r"\sim", r"N(0, I_4); \ \ Y = 210 + 27.4 Z_1 + 13.7(Z_2 + Z_3 + Z_4) + \varepsilon", font_size=28),
            cmath(r"P(\text{observed} \mid Z)", r"=", r"\mathrm{expit}(-Z_1 + 0.5 Z_2 - 0.25 Z_3 - 0.1 Z_4)", font_size=28),
            cmath(r"\text{but we see}", r":", r"X = (e^{Z_1/2}, \ \ldots, \ (Z_2 + Z_4 + 20)^2)", font_size=28),
            cmath(r"\text{models on } X", r":", r"\text{both slightly wrong}", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"Kang \& Schafer (2007)"), why(r"estimate $E[Y] = 210$ from the observed"),
                why(r"smooth, \ monotone transformations"), why(r"each wrong model looks fine")]
        with self.voiceover(
            "<bookmark mark='a'/> But what if both models are wrong? In 2007 Joseph Kang and Joseph Schafer published a "
            "simulation that became famous. Four standard normal variables determine an outcome linearly, <bookmark "
            "mark='b'/> and whether it is observed, logistically: the task is to estimate its mean, two hundred and ten, from "
            "the observed cases, a missing-data version of the causal problem. <bookmark mark='c'/> The analyst sees only "
            "smooth transformations of the four variables, <bookmark mark='d'/> so both a linear outcome model and a logistic "
            "observation model fitted to them are slightly wrong, and each looks fine by the usual diagnostics."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("kang")
        rows = [[r"estimator", r"bias", r"RMSE", r"90\% coverage"],
                [r"outcome model, \ wrong", rf"{d['or_wrong']['bias']:.2f}", rf"{d['or_wrong']['rmse']:.2f}", r""],
                [r"IPW, \ wrong", rf"{d['ipw_wrong']['bias']:.2f}", rf"{d['ipw_wrong']['rmse']:.2f}", r""],
                [r"AIPW, \ propensity right", rf"{d['aipw_right_wrong']['bias']:.2f}", rf"{d['aipw_right_wrong']['rmse']:.2f}", rf"{100 * d['aipw_right_wrong']['cover']:.0f}\%"],
                [r"AIPW, \ outcome right", rf"{d['aipw_wrong_right']['bias']:.2f}", rf"{d['aipw_wrong_right']['rmse']:.2f}", rf"{100 * d['aipw_wrong_right']['cover']:.0f}\%"],
                [r"AIPW, \ both wrong", rf"{d['aipw_wrong_wrong']['bias']:.1f}", rf"{d['aipw_wrong_wrong']['rmse']:.0f}", rf"{100 * d['aipw_wrong_wrong']['cover']:.0f}\%"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.28, colors=[GREY_A, GREY_B, PSC, BANDC, BANDC, MISSC]).move_to([0, 0.8, 0])
        foot = label(rf"1,000 samples of 1,000; \ the largest weight in one sample: \ {d['max_max_weight']:,.0f}", font_size=22, color=GREY_A).move_to([0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A thousand samples of a thousand. The wrong outcome model alone is only slightly biased, by "
            "less than one. <bookmark mark='b'/> IPW with the wrong propensity model is worse, biased by five with a large "
            "error. <bookmark mark='c'/> The doubly robust estimator with either model right is unbiased and covers about "
            "ninety percent of the time, as promised. <bookmark mark='d'/> With both wrong, it is a disaster: a bias of "
            "minus twenty-one and a root mean squared error of about two hundred, far worse than the simple outcome model, "
            "because a few observations with near-zero estimated propensity receive weights in the tens of thousands, and "
            "the doubly robust correction multiplies their residuals by those weights."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]), FadeIn(foot))
        self.clear_scene()

    def board(self):
        rows = board_rows("AIPW, \\ both models fitted", "PS right", "both models wrong")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board. AIPW on the World's study, both models fitted: <bookmark mark='b'/> "
                   "kept. In Kang and Schafer's design with the propensity model right: kept. <bookmark mark='c'/> With both "
                   "models wrong: broken.",
                   [("a", [0]), ("b", [1]), ("c", [2])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"double robustness is insurance against one mistake, \ not two", font_size=26, color=TAUC),
            label(r"the replies: \ bounded weights, \ better propensity fits, \ targeted estimators (TMLE)", font_size=26, color=GREY_A),
            label(r"and the modern answer: \ flexible models for both, \ fitted carefully", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So double robustness is insurance against one mistake, not against two. <bookmark "
            "mark='b'/> The replies to Kang and Schafer proposed bounded weights, propensity models fitted for balance, and "
            "targeted maximum likelihood estimators, Mark van der Laan's TMLE, which keep estimates inside the range of the "
            "data. <bookmark mark='c'/> The modern answer is to fit both models flexibly, with machine learning, so that "
            "neither is badly wrong, and to do it carefully, which is the next chapter."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
