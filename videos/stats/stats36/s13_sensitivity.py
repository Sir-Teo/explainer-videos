from __future__ import annotations

import numpy as np

from videos.stats.stats36.common import *  # noqa: F403


class Sensitivity(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.rosenbaum()
        self.gamma_chart()
        self.evalue()
        self.ch()
        self.ch_numbers()
        self.board()
        self.lesson()

    def card(self):
        card = chapter_card(12, r"Sensitivity analysis", r"How wrong could we be?", lit=(1959, 2017, 2020), part=PART)
        with self.voiceover("Chapter twelve. Sensitivity analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_(self):
        d = load("sens")
        rows = fit_rows(VGroup(
            label(r"the World's study again, \ but now doctors also judge an unrecorded frailty", font_size=26),
            label(r"frail patients are treated more, \ and their pressure is higher anyway", font_size=26, color=MISSC),
            label(rf"adjusting for the four recorded covariates: \ ${d['est']:.2f}$ \ (SE {d['se']:.2f})", font_size=26, color=Y0C),
            label(rf"the truth: \ ${d['ate']:.2f}$; \ with frailty measured: \ ${d['est_with_u']:.2f}$", font_size=26, color=TRUEC),
            label(r"no test can detect this; \ but we can ask how strong a confounder would have to be", font_size=26, color=TAUC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Return to the World's study, but now let the doctors also judge each patient's frailty, "
            "which no data set records. <bookmark mark='b'/> Frail patients are treated more often, and their pressure would "
            "be higher anyway. <bookmark mark='c'/> Adjusting for the four recorded covariates gives minus "
            + say(-d["est"], 1) + ", with a small standard error. <bookmark mark='d'/> The truth is minus " + say(-d["ate"], 1)
            + "; had frailty been measured, adjusting for it would have given minus " + say(-d["est_with_u"], 1) + ". <bookmark mark='e'/> The observed data alone do not generally identify this hidden-confounding bias. "
            "What we can do is ask how strong an unmeasured confounder would have to be to change the conclusion."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rosenbaum(self):
        rows = [
            cmath(r"\text{matched pair } j", r":", r"\text{under no hidden bias, \ each member equally likely treated}", font_size=28),
            cmath(r"\text{hidden bias } \Gamma", r":", r"\tfrac{1}{\Gamma} \le \tfrac{\text{odds}_i}{\text{odds}_{i'}} \le \Gamma", font_size=30),
            cmath(r"\text{for each } \Gamma", r":", r"\text{the exact worst-case one-sided } p\text{-value of the signed-rank test}", font_size=28),
            cmath(r"\Gamma^\star", r":", r"\text{the smallest } \Gamma \text{ that makes it insignificant}", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"a coin within the pair"), why(r"two patients alike on $X$ may differ in odds by $\Gamma$"),
                why(r"Rosenbaum (1987, 2002)"), why(r"a one-number summary of robustness")]
        with self.voiceover(
            "<bookmark mark='a'/> Paul Rosenbaum's approach starts from matched pairs. If there is no hidden bias, "
            "the two members of a pair, alike on the measured covariates, were equally likely to be the treated one: "
            "a coin within each pair. <bookmark mark='b'/> Hidden bias of size gamma allows their odds of treatment "
            "to differ by up to a factor gamma, because of something unmeasured. <bookmark mark='c'/> For each gamma,"
            " compute a worst-case one-sided signed-rank tail probability under the sharp null and the matched-pair "
            "assignment model. We compute the signed-rank tail by exact dynamic programming over independent pair "
            "signs, including average-rank ties. <bookmark mark='d'/> The smallest gamma that makes the effect "
            "insignificant summarizes how robust the finding is."
        ) as vo:
            intro=label('A matched-pair sensitivity model limits hidden assignment odds',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gamma_chart(self):
        d = load("sens")
        rw = d["rosen_world"]
        gs = sorted(float(k) for k in rw)
        lp = [max(-np.log10(max(rw[str(g) if str(g) in rw else f"{g:.1f}"], 1e-300)), 0) for g in gs]
        A = axes([1, 7], [0, 150], x_length=7.4, y_length=4.2, xlabel=r"hidden bias $\Gamma$", ylabel=r"$-\log_{10}$ worst $p$",
                 xticks=[1, 2, 3, 4, 5, 6, 7], yticks=[0, 50, 100, 150], center=[-2.0, 0.2, 0])
        ax = A.ax
        line = VGroup(polyline(ax, gs, lp, PSC, 3), *[Dot(ax.c2p(g, v), radius=0.06, color=PSC) for g, v in zip(gs, lp)])
        sig = DashedLine(ax.c2p(1, -np.log10(0.05)), ax.c2p(7, -np.log10(0.05)), color=MISSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"frailty study: \ {d['world_pairs']} disjoint pairs; \ logit-score caliper", font_size=22),
            label(rf"matched estimate: \ ${d['world_match']:.1f}$ mm Hg", font_size=22, color=Y0C),
            label(rf"still significant until $\Gamma^\star \approx {d['gamma_star']:.1f}$", font_size=22, color=TAUC),
            label(r"the real frailty biases the size, \ not the sign", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the World's frailty study, we form disjoint pairs without reusing controls, "
            "using a caliper on the estimated logit propensity score. Unmatched treated patients are omitted. "
            "<bookmark mark='b'/> the matched estimate is minus " + say(-d["world_match"], 1) + ". <bookmark mark='c'/> The displayed gamma threshold describes loss of significance for this matched "
            "sample under the sensitivity model. Approximate matching also leaves some measured-covariate imbalance. "
            "<bookmark mark='d'/> The simulator tells us that the average effect is negative despite substantial bias"
            " in its estimated size. The sensitivity threshold alone does not establish the actual confounder's "
            "strength, identify the causal sign, or bound all estimation bias."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(A), Create(sig), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def evalue(self):
        rows = [
            cmath(r"\text{observed risk ratio}", r":", r"RR", font_size=32),
            cmath(r"E", r"=", r"RR + \sqrt{RR\,(RR - 1)}", font_size=34),
            cmath(r"\text{meaning}", r":", r"\text{equal strengths } E; \ \text{otherwise use } B=ab/(a+b-1)", font_size=26),
            cmath(r"RR = 2", r"\Rightarrow", r"E = 3.41", font_size=32),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"e.g. a cohort study"), why(r"VanderWeele \& Ding (2017)"),
                why(r"both associations below $E$ are insufficient"), why(r"a single number to report")]
        with self.voiceover(
            "<bookmark mark='a'/> For risk ratios, Tyler VanderWeele and Peng Ding proposed in 2017 a number that is "
            "easy to report. Given an observed risk ratio, <bookmark mark='b'/> the E-value is the risk ratio plus "
            "the square root of the risk ratio times the risk ratio minus one. <bookmark mark='c'/> The E-value is an"
            " equal-strength threshold: if both sensitivity associations are below E, this confounding bound cannot "
            "explain the association. One association can be smaller than E if the other is sufficiently larger. "
            "Their trade-off is the product divided by the sum minus one, under the specified risk-ratio sensitivity "
            "model. <bookmark mark='d'/> For a risk ratio of two, the equal-strength threshold is three point four "
            "one. An association of ten on one side and three on the other can also exceed the required bias factor."
        ) as vo:
            intro=label('The E-value is an equal-strength threshold with unequal-strength tradeoffs',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ch(self):
        rows = [
            cmath(r"R^2_{T \sim U \mid X}, \ R^2_{Y \sim U \mid X, T}", r":", r"\text{the confounder's partial } R^2\text{s}", font_size=28),
            cmath(r"|\text{bias}|", r"\le", r"\mathrm{se}(\hat\tau)\sqrt{\text{df}} \sqrt{\tfrac{R^2_{Y \sim U} R^2_{T \sim U}}{1 - R^2_{T \sim U}}}", font_size=28),
            cmath(r"RV", r"=", r"\tfrac12\big(\sqrt{f^4 + 4f^2} - f^2\big), \ \ f = |t| / \sqrt{\text{df}}", font_size=30),
            cmath(r"\text{benchmark}", r":", r"\text{compare with the } R^2 \text{ of measured covariates}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"how much each would explain"), why(r"omitted-variable bias, \ exactly"),
                why(r"the robustness value: \ equal $R^2$s that erase the estimate"), why(r"Cinelli \& Hazlett (2020)")]
        with self.voiceover(
            "<bookmark mark='a'/> For regression estimates, Carlos Cinelli and Chad Hazlett described a confounder by two "
            "partial R-squared values: how much of the treatment's variation it explains, and how much of the outcome's, "
            "beyond what is measured. <bookmark mark='b'/> The omitted-variable bias is then bounded exactly by a formula in "
            "the standard error, the degrees of freedom and those two numbers. <bookmark mark='c'/> Their robustness value is "
            "the common partial R-squared a confounder would need with both to erase the estimate entirely, computable from "
            "the t statistic alone. <bookmark mark='d'/> And it can be benchmarked: compare it with how much the strongest "
            "measured covariate explains."
        ) as vo:
            intro=label('Robustness values describe sensitivity of a specified regression',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ch_numbers(self):
        d = load("sens")
        rows = fit_rows(VGroup(
            label(rf"$t = {d['t']:.1f}$ \ on {d['dof']:,} df", font_size=26),
            label(rf"robustness value: \ {d['rv']:.2f}; \ to lose significance at 5\%: \ {d['rv_sig']:.2f}", font_size=26, color=TAUC),
            label(rf"the actual frailty: \ partial $R^2$ {d['r2_tu']:.3f} with treatment, \ {d['r2_yu']:.3f} with outcome", font_size=26, color=MISSC),
            label(r"this actual frailty leaves a negative coefficient; \ its size is still biased", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the frailty study, the adjusted estimate has a t statistic of about minus twenty. "
            "<bookmark mark='b'/> Its robustness value is " + say(d["rv"]) + ": a confounder explaining thirty percent of the residual variation in both treatment and outcome would "
            "be needed to erase it. <bookmark mark='c'/> The actual frailty explains about nine percent of each. "
            "<bookmark mark='d'/> That is far below thirty, so this particular measured-in-the-simulator frailty does"
            " not erase the adjusted regression coefficient; but it is large enough to bias the estimate by over a "
            "quarter, and a full sensitivity analysis would plot the bias for every pair of R-squared values, not "
            "just report one number."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("unmeasured frailty")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: regression adjustment for the recorded covariates when doctors also "
                   "use an unrecorded frailty, over five hundred studies. Broken. Adjusting for these measured covariates "
                   "alone does not identify the effect under this graph. Further assumptions, additional data or a "
                   "sensitivity analysis are needed.",
                   [("a", [0])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"report the estimate with its sensitivity, \ not alone", font_size=26, color=TAUC),
            label(r"Cornfield's 1959 argument: \ an early formal sensitivity analysis", font_size=26, color=GREY_A),
            label(r"next: \ the case where it mattered most", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson is to report an observational estimate with its sensitivity analysis, "
            "never alone. <bookmark mark='b'/> An early formal sensitivity analysis was Jerome Cornfield's, in 1959, "
            "<bookmark mark='c'/> in the case where it mattered most."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
