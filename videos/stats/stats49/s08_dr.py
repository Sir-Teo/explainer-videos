from __future__ import annotations

from videos.stats.stats49.common import *  # noqa: F403


class DoubleRobust(VoiceoverScene):
    def construct(self):
        self.card()
        self.remainder()
        self.table()
        self.others()
        self.structure()

    def card(self):
        card = chapter_card(7, r"Double robustness", r"A property of the influence function, \ not a trick", lit=(1994,), part=PART)
        with self.voiceover("Chapter seven. Double robustness: a property of the influence function, not a trick."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def remainder(self):
        rows = [
            cmath(r"E\big[\hat\mu_1 + \tfrac{T}{\hat e}(Y - \hat\mu_1)\big] - E\,\mu_1", r"=", r"E\Big[\frac{(e - \hat e)(\mu_1 - \hat\mu_1)}{\hat e}\Big]", font_size=32),
            cmath(r"\hat\mu_1 = \mu_1", r"\Rightarrow", r"0, \ \text{whatever } \hat e", font_size=36),
            cmath(r"\hat e = e", r"\Rightarrow", r"0, \ \text{whatever } \hat\mu_1", font_size=36),
            cmath(r"\text{both wrong}", r":", r"\text{the bias is the product of the two errors}", font_size=34),
        ]
        rows[0][-1].set_color(EFFC)
        rows[1][-1].set_color(TANC)
        rows[2][-1].set_color(TANC)
        rows[3][-1].set_color(NUIC)
        whys = [why(r"the one-step's remainder $R_2$, \ exactly"), why(r"outcome model right"), why(r"propensity model right"), why(r"chapter 8's product rate")]
        with self.voiceover(
            "<bookmark mark='a'/> Take the treated half of the one-step estimator of the average treatment effect and compute "
            "its bias exactly. It is the expected product of the propensity's error and the outcome regression's error, "
            "divided by the estimated propensity. <bookmark mark='b'/> If the outcome regression is right, the product is "
            "zero, whatever the propensity estimate. <bookmark mark='c'/> If the propensity is right, it is zero, whatever "
            "the outcome regression. <bookmark mark='d'/> That is double robustness, found by James Robins, Andrea Rotnitzky "
            "and Lue Ping Zhao in 1994. It is not a trick of this estimator: it is what the second-order remainder of the "
            "efficient influence function looks like, a product."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("dr")
        c = d["cells"]
        rows = [[r"", r"propensity right", r"propensity wrong \ (a constant)"],
                [r"outcome right", f"{c['right_right']['bias']:+.3f}", f"{c['right_wrong']['bias']:+.3f}"],
                [r"outcome wrong \ (arm means)", f"{c['wrong_right']['bias']:+.3f}", f"{c['wrong_wrong']['bias']:+.3f}"]]
        tab = table_rows(rows, font_size=32, col_buff=1.0, row_buff=0.5, colors=[GREY_B, None, None])
        tab.move_to([0, 0.9, 0])
        tab[1][1].set_color(TANC)
        tab[1][2].set_color(TANC)
        tab[2][1].set_color(TANC)
        tab[2][2].set_color(NUIC)
        foot = label(rf"bias of the one-step ATE, \ true 1.5; \ $n = {d['n']:,}$, \ {d['reps']} samples; \ simulation SE about {c['wrong_wrong']['se']:.3f}", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"three cells of four are unbiased; \ only when both models fail does the bias appear", font_size=24, color=EFFC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> In the smooth world, with each working model either right or deliberately wrong: the wrong "
            f"outcome model ignores the covariates and uses the arm means; the wrong propensity is a constant. With either "
            f"one right, the bias is within simulation error of zero. <bookmark mark='b'/> With both wrong, it is "
            f"{say(c['wrong_wrong']['bias'], 2)}, the product of the two errors, about three and a half standard errors of the estimator "
            f"at this sample size."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def others(self):
        d = load("dr")
        c = d["cells"]
        rows = [[r"working models \ (outcome, \ propensity)", r"plug-in", r"IPW", r"one-step"]]
        lab = {"right_right": r"right, \ right", "right_wrong": r"right, \ wrong", "wrong_right": r"wrong, \ right", "wrong_wrong": r"wrong, \ wrong"}
        for k in ("right_right", "right_wrong", "wrong_right", "wrong_wrong"):
            rows.append([lab[k], f"{c[k]['plugin']:+.3f}", f"{c[k]['ipw']:+.3f}", f"{c[k]['bias']:+.3f}"])
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.38, colors=[GREY_B, None, None, None, None])
        tab.move_to([0, 0.8, 0])
        for i, k in enumerate(("right_right", "right_wrong", "wrong_right", "wrong_wrong"), start=1):
            for j, key in ((1, "plugin"), (2, "ipw"), (3, "bias")):
                tab[i][j].set_color(NUIC if abs(c[k][key]) > 0.05 else TANC)
        foot = label(r"bias of three estimators of the ATE \ (true 1.5); \ red: \ more than 0.05", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        foot2 = label(r"the plug-in needs the outcome model; \ IPW needs the propensity; \ the one-step needs either", font_size=24, color=EFFC).move_to([0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Compare the single-model estimators in the same four worlds. The plug-in uses only the "
            f"outcome model, so it is unbiased exactly when that model is right, and off by about {say(c['wrong_right']['plugin'], 1)} "
            f"when it is wrong. Inverse probability weighting uses only the propensity, so it fails whenever the propensity "
            f"is wrong. <bookmark mark='b'/> The one-step estimator needs only one of the two. And in the last row, with "
            f"both wrong, all three estimators coincide: with arm means and a constant propensity, every method reduces to the "
            f"naive difference in means."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def structure(self):
        rows = fit_rows(VGroup(
            label(r"why products? \ $\phi^*$ is linear in $1/e$ and in $\mu$, \ and the two enter multiplied", font_size=26),
            label(r"other doubly robust estimators, \ same reason: \ the mean under MAR, \ the ATT, \ mediation, \ IV", font_size=26, color=TANC),
            label(r"but `double robustness' is a \emph{bias} property: \ the variance is efficient only when both are right", font_size=26, color=EFFC),
            label(r"and with both slightly wrong, \ the bias is small but can be larger than the SE: \ Kang \& Schafer (2007)", font_size=26, color=NUIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why a product? Because the efficient influence function involves the propensity and the "
            "outcome regression multiplied together, and nothing else that depends on either. <bookmark mark='b'/> Every "
            "functional with that structure has a doubly robust estimator: the mean of an outcome missing at random, the "
            "effect on the treated, mediation and instrumental-variable effects. <bookmark mark='c'/> But double "
            "robustness is about bias only. The variance is the efficient one only when both models are right. <bookmark "
            "mark='d'/> And when both are a little wrong, as Part thirty-six's Kang and Schafer example showed, a product of "
            "two small errors can still exceed the standard error. The cure is not more robustness but better nuisance "
            "estimates, fast enough, which is the next chapter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
