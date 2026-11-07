from __future__ import annotations

from videos.stats.stats35.common import *  # noqa: F403


class Adjust(VoiceoverScene):
    def construct(self):
        self.card()
        self.ancova_()
        self.trial()
        self.freedman()
        self.lin_()
        self.design()
        self.board()
        self.rules()

    def card(self):
        card = chapter_card(7, r"Adjustment", r"Freedman's critique and Lin's answer", lit=(2008, 2013), part=PART)
        with self.voiceover("Chapter seven. Regression adjustment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ancova_(self):
        rows = [
            cmath(r"Y_i", r"=", r"\alpha + \tau Z_i + \beta' x_i + \varepsilon_i", font_size=34),
            cmath(r"\hat\tau_{\rm ANCOVA}", r":", r"\text{the coefficient on } Z", font_size=32),
            cmath(r"\text{the hope}", r":", r"\text{the covariates soak up noise, \ as blocking does}", font_size=30),
            cmath(r"\text{but}", r":", r"\text{randomization did not justify this model}", font_size=32),
        ]
        rows[1][-1].set_color(ESTC)
        whys = [why(r"Fisher's analysis of covariance"), why(r"the usual report"), why(r"precision after the fact"),
                why(r"Freedman's point")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual way to use baseline covariates after a trial is Fisher's analysis of "
            "covariance: regress the outcome on the treatment indicator and the covariates. <bookmark mark='b'/> The "
            "coefficient on treatment is the adjusted estimate. <bookmark mark='c'/> The hope is that the covariates soak up "
            "outcome noise, as blocking would have. <bookmark mark='d'/> But nothing in the randomization says that the "
            "outcomes follow this linear model with a common slope and constant variance."
        ) as vo:
            intro=label('Regression adjustment is an analysis choice after randomization',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trial(self):
        d = load("adjust")
        rows = fit_rows(VGroup(
            label(r"the World's trial, \ adjusting for baseline pressure and age:", font_size=26),
            label(rf"SD of the estimate, \ 600 randomizations: \ unadjusted {d['sd_unadj']:.3f}", font_size=26, color=GREY_B),
            label(rf"ANCOVA {d['sd_ancova']:.3f}; \ Lin {d['sd_lin']:.3f}", font_size=26, color=BANDC),
            label(r"variance cut by 38\%: \ the same gain as blocking", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World's trial, with two thousand patients and equal arms, adjust for baseline "
            "pressure and age. <bookmark mark='b'/> Over six hundred randomizations, the unadjusted estimate has a standard "
            "deviation of " + say(d["sd_unadj"], 3) + ". <bookmark mark='c'/> Both adjusted estimates have about "
            + say(d["sd_ancova"], 3) + ". <bookmark mark='d'/> The variance falls by nearly two fifths, the same gain blocking achieved. Here "
            "the baseline covariates improve precision. Lin's result describes the asymptotic comparison under "
            "suitable conditions."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def freedman(self):
        rows = fit_rows(VGroup(
            label(r"David Freedman (2008), \ `On regression adjustments to experimental data':", font_size=26),
            label(r"1. \ the adjusted estimate is biased, \ of order $1/n$", font_size=26, color=GREY_A),
            label(r"2. \ with unequal arms and varying effects, \ it can be \emph{less} precise than no adjustment", font_size=26, color=MISSC),
            label(r"3. \ its conventional standard error can be wrong, \ even as $n \to \infty$", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2008 David Freedman, analysing regression adjustment entirely within Neyman's "
            "framework, with no model for the outcomes, published three uncomfortable results. <bookmark mark='b'/> First, "
            "the adjusted estimate is biased, though only by something of order one over n. <bookmark mark='c'/> Second, "
            "when the arms are of unequal size and the treatment effect varies with the covariate, adjustment can actually "
            "make the estimate less precise. <bookmark mark='d'/> Third, the conventional regression standard error, which "
            "assumes a common slope and constant variance, can be wrong, even in very large samples."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lin_(self):
        rows = [
            cmath(r"Y_i", r"\sim", r"\alpha + \tau Z_i + \beta'(x_i - \bar x) + \gamma' Z_i (x_i - \bar x)", font_size=30),
            cmath(r"\text{equivalently}", r":", r"\text{separate regressions in each arm}", font_size=30),
            cmath(r"\text{SE}", r":", r"\text{Huber--White, \ HC2}", font_size=32),
            cmath(r"\text{result}", r":", r"\text{never less precise, \ asymptotically; \ SE valid or conservative}", font_size=28),
        ]
        rows[0][-1].set_color(BANDC)
        whys = [why(r"interact $Z$ with centred covariates"), why(r"each arm its own slope"),
                why(r"Part 23's sandwich"), why(r"Lin (2013)")]
        with self.voiceover(
            "<bookmark mark='a'/> Winston Lin, then a graduate student at Berkeley, answered in 2013. Centre the "
            "covariates, and interact them with the treatment indicator. <bookmark mark='b'/> That is the same as "
            "fitting a separate regression in each arm and comparing their predictions at the average covariate. "
            "<bookmark mark='c'/> And use Part 23's sandwich standard errors, the HC2 version. <bookmark mark='d'/> "
            "Lin proved that this estimate is, asymptotically, never less precise than the unadjusted difference in "
            "means, and that its sandwich standard error is consistent or conservative, all within Neyman's "
            "framework, with a fixed number of covariates, stable treatment fractions and regular finite-population "
            "moments. Interactions and robust errors address the efficiency and variance problems. Small "
            "finite-sample bias can still remain."
        ) as vo:
            intro=label('Interactions and robust errors give an asymptotic precision guarantee',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def design(self):
        d = load("adjust")
        rows = [[r"", r"SD of $\hat\tau$", r"mean SE", r"90\% coverage"],
                [r"unadjusted", rf"{d['f_sd_unadj']:.2f}", r"", r""],
                [r"ANCOVA, \ conventional SE", rf"{d['f_sd_ancova']:.2f}", rf"{d['f_se_ancova']:.2f}", rf"{100 * d['f_cover_ancova']:.1f}\%"],
                [r"Lin, \ HC2", rf"{d['f_sd_lin']:.2f}", rf"{d['f_se_lin']:.2f}", rf"{100 * d['f_cover_lin']:.1f}\%"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_A, GREY_B, MISSC, BANDC]).move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"200 units, \ only 50 treated; \ the effect grows with $x$, \ and so does the noise", font_size=24),
            label(r"ANCOVA's SE is too small: \ it assumes both arms share a slope and a variance", font_size=24, color=MISSC),
        ), 12.4, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A design in Freedman's spirit: two hundred units, only fifty of them treated, with a "
            "treatment effect that grows with the covariate, and noise that grows with it too. Four thousand "
            "randomizations. <bookmark mark='b'/> Both adjustments improve on the unadjusted estimate here, Lin's by more. "
            "<bookmark mark='c'/> But ANCOVA's conventional standard error, " + say(d["f_se_ancova"]) + ", understates its "
            "real variability, " + say(d["f_sd_ancova"]) + ", and its ninety percent intervals cover only "
            + say(100 * d["f_cover_ancova"], 1) + " percent of the time. <bookmark mark='d'/> Lin's sandwich error matches its "
            "variability, and covers " + say(100 * d["f_cover_lin"], 1) + " percent."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2][:2]), FadeIn(tab[3][:2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2][2:]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3][2:]))
        self.clear_scene()

    def board(self):
        rows = board_rows("ANCOVA", "Lin, \\ HC2")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board. ANCOVA with its conventional standard error, in the unbalanced "
                   "design: broken. <bookmark mark='b'/> Lin's interacted regression with HC2: kept.",
                   [("a", [0]), ("b", [1])])

    def rules(self):
        rows = fit_rows(VGroup(
            label(r"choose the covariates before seeing outcomes: \ in the protocol", font_size=26, color=BANDC),
            label(r"interact them with treatment; \ use sandwich standard errors", font_size=26, color=BANDC),
            label(r"in small trials, \ adjust for a few strong predictors only", font_size=26, color=GREY_A),
            label(r"FDA (2023): \ prespecify prognostic covariates; \ interactions are optional", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The practical rules that came out of this exchange: choose the covariates before "
            "seeing any outcomes, and write them into the protocol, so that adjustment cannot become a fishing "
            "expedition. <bookmark mark='b'/> Interact them with treatment, and use sandwich standard errors. "
            "<bookmark mark='c'/> In small trials, adjust for a few strong predictors of the outcome only. <bookmark "
            "mark='d'/> The American Food and Drug Administration's 2023 guidance emphasizes prespecified prognostic "
            "covariates and appropriate standard errors. Interactions are allowed, rather than universally required."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
