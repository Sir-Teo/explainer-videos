from __future__ import annotations

import math

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403


class SurveyReport(VoiceoverScene):
    def construct(self):
        self.card()
        self.rv()
        self.contour()
        self.trial()
        self.memo_()
        self.truth()

    def card(self):
        card = chapter_card(6, r"Case 2: \ sensitivity and the report", r"How wrong could we be, \ and what do we say?", lit=(2021,), part=PART)
        with self.voiceover("Chapter six. How wrong could we be, and what do we tell the minister?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rv(self):
        o = load("obs")
        b, se = o["ols"]
        rows = [
            cmath(r"\hat\tau_{\text{OLS}}", r"=", rf"{b:.2f}, \ \ \text{{SE}} = {se:.2f}, \ \ t = {o['t_stat']:.2f} \ \text{{on {o['dof']:,} df}}", font_size=32),
            cmath(r"f", r"=", rf"|t| / \sqrt{{\text{{df}}}} = {abs(o['t_stat']) / math.sqrt(o['dof']):.4f}", font_size=32),
            cmath(r"\text{RV}", r"=", rf"\tfrac12\big(\sqrt{{f^4 + 4f^2}} - f^2\big) = {o['rv']:.3f}", font_size=34),
            cmath(r"\text{RV}_{0.05}", r"=", rf"{o['rv_a']:.3f}: \ \text{{approximate classical-OLS significance threshold}}", font_size=32),
        ]
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"one completed dataset; classical OLS sensitivity"), why(r"the partial Cohen's $f$"), why(r"Cinelli \& Hazlett (2020)"), why(r"a weaker bar")]
        with self.voiceover(
            f"<bookmark mark='a'/> The estimate rests on one assumption the data cannot check: that the graph has every common cause of switching and pressure. Part thirty-six's robustness value asks how strong a missing one would have to be. Start from one seeded completed dataset and its adjusted regression, using classical OLS standard errors for the partial-variance identities. This is a sensitivity illustration for that OLS coefficient, not pooled MI-AIPW inference: {say(b, 2)}, with a t statistic of {say(o['t_stat'], 2)} on almost three thousand degrees of freedom. <bookmark mark='b'/> Divide the t by the root of the degrees of freedom. <bookmark mark='c'/> Carlos Cinelli and Chad Hazlett's robustness value is then {say(o['rv'], 3)}: a hidden confounder explaining {100 * o['rv']:.1f} percent of the residual variance of both switching and pressure would erase the effect. <bookmark mark='d'/> One explaining {100 * o['rv_a']:.1f} percent of each would make it no longer significant at five percent."
        ) as vo:
            heading = label('Classical OLS sensitivity on one completed dataset', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def contour(self):
        o = load("obs")
        f2 = o["t_stat"] ** 2 / o["dof"]
        A = axes([0, 0.16], [0, 0.16], x_length=5.2, y_length=4.6, xlabel=r"partial $R^2$ of the confounder with switching",
                 ylabel=r"partial $R^2$ with pressure", xticks=[0, 0.05, 0.1, 0.15], yticks=[0, 0.05, 0.1, 0.15], center=[-2.8, 0.1, 0])
        ax = A.ax
        xs = np.linspace(0.03, 0.16, 120)
        ys = f2 * (1 - xs) / xs
        k = ys <= 0.16
        zero = curve(ax, xs[k], ys[k], S.RESID, 4)
        region = Polygon(*([ax.c2p(a, b) for a, b in zip(xs[k], ys[k])] + [ax.c2p(0.16, 0.16), ax.c2p(xs[k][0], 0.16)]),
                         stroke_width=0, fill_color=S.RESID, fill_opacity=0.15)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.16, 0.16), color=GREY_C, stroke_width=1.5)
        rvdot = Dot(ax.c2p(o["rv"], o["rv"]), color=S.ACCENT, radius=0.08)
        bench = VGroup()
        for m in (1, 2, 3):
            bx, by = m * o["bench_r2d"], m * o["bench_r2y"]
            bench.add(VGroup(Dot(ax.c2p(bx, by), color=GOODC, radius=0.08),
                             label(rf"{m}$\times$", font_size=20, color=GOODC).next_to(ax.c2p(bx, by), RIGHT, buff=0.1)))
        side = fit_rows(VGroup(
            label(r"red: \ confounders strong enough to erase the effect", font_size=24, color=S.RESID),
            label(rf"on the diagonal: \ RV $= {o['rv']:.3f}$", font_size=24, color=S.ACCENT),
            label(rf"benchmark, \ ``told: \ high pressure'': \ ({o['bench_r2d']:.3f}, \ {o['bench_r2y']:.3f})", font_size=24, color=GOODC),
            label(r"twice as strong: \ the effect survives", font_size=24, color=GOODC),
            label(r"three times: \ it would not", font_size=24, color=GREY_A),
        ), 5.4, 0.42, [3.7, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Draw it. Across, how much of switching a hidden confounder explains; up, how much of "
            f"pressure. In the red region, the adjusted effect would be zero or positive. <bookmark mark='b'/> The robustness "
            f"value is where the boundary crosses the diagonal. <bookmark mark='c'/> Is that a lot? Compare a confounder we "
            f"did measure, the strongest: having been told one's pressure is high. It explains {100 * o['bench_r2d']:.1f} "
            f"percent of switching and {100 * o['bench_r2y']:.1f} percent of pressure. <bookmark mark='d'/> A hidden factor "
            f"twice as strong as a doctor's diagnosis would not erase the effect. <bookmark mark='e'/> Three times as strong "
            f"would. Whether such a factor exists is a question for physicians and sociologists, not for the data; the "
            f"analysis can only say how strong it would have to be."
        ) as vo:
            self.play(FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(FadeIn(region), Create(zero), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(rvdot), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bench[0]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bench[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(bench[2]), FadeIn(side[4]))
        self.clear_scene()

    def trial(self):
        hc = history_card(2021, r"B. Neal and colleagues, \ the Salt Substitute and Stroke Study",
                          r"in the \emph{New England Journal of Medicine}: \ 20,995 adults with a past stroke, \ or over 60 with high "
                          r"pressure, \ in 600 villages of rural China; \ villages randomized to a salt substitute (75\% sodium "
                          r"chloride, \ 25\% potassium chloride) \ or ordinary salt, \ followed for about five years",
                          color=CASE2, width=11.6, font_size=22).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"systolic pressure: \ 3.3 mm Hg lower in the substitute villages", font_size=26, color=GOODC),
            label(r"strokes: \ rate ratio 0.86 \ (95\% CI 0.77 to 0.96); \ deaths also fewer", font_size=26, color=GOODC),
            label(r"a cluster-randomized trial: \ Case 1's design, \ answering Case 2's question", font_size=24, color=S.ACCENT),
        ), 12.4, 0.4, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Observational evidence is strongest when it agrees with experiments, and here there"
            " is a real one. Bruce Neal and colleagues' Salt Substitute and Stroke Study, published in 2021, "
            "randomized six hundred villages in rural China, with about twenty-one thousand adults at high risk, to a"
            " salt substitute of three quarters sodium chloride and one quarter potassium chloride, or to ordinary "
            "salt, for about five years. <bookmark mark='b'/> Pressure fell by about three point three millimetres in"
            " the substitute villages, <bookmark mark='c'/> and strokes by fourteen percent, with fewer deaths. "
            "<bookmark mark='d'/> It is a cluster-randomized trial, Case one's design, and it supports the same "
            "direction of effect in its own high-risk rural Chinese population. Transporting its magnitude to the "
            "island requires further assumptions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def memo_(self):
        o = load("obs")
        r = o["res"]["mi_aipw"]
        lines = [
            (rf"Finding: \ under the stated assumptions, \ the estimated pressure reduction is", WHITE),
            (rf"by about {-r[0]:.1f} mm Hg \ (90\% interval {-r[3]:.1f} to {-r[2]:.1f}).", WHITE),
            (r"Why the newspapers saw the opposite: \ people already told their pressure was high", GREY_A),
            (r"were three times as likely to switch.", GREY_A),
            (r"Assumptions: \ every common cause of switching and pressure was measured;", GREY_A),
            (r"income missing at random, \ given what was seen.", GREY_A),
            (r"OLS sensitivity illustration: \ a hidden factor needs more than twice the strength", GREY_A),
            (r"of a diagnosis of high pressure to erase the effect.", GREY_A),
            (r"Agreement: \ a randomized trial in 600 villages found 3.3 mm Hg, \ and 14\% fewer strokes.", GREY_A),
            (r"Advice: \ keep it on sale; \ promote it through Case 1's health workers;", S.ACCENT),
            (r"obtain clinical advice for kidney disease or potassium-raising medicines.", S.ACCENT),
        ]
        m = memo(lines, r"To the Minister \ \textbullet\ \ the salt substitute \ \textbullet\ \ one page", width=12.8, font_size=24).move_to([0, 0, 0])
        groups = [[2, 3], [4, 5], [6, 7], [8], [9, 10]]
        with self.voiceover(
            f"<bookmark mark='a'/> And then the page the minister will actually read. It leads with the finding, in the minister's units: among comparable adults, using the substitute lowered pressure by about {say(-r[0], 1)} millimetres, with an interval from {say(-r[3], 1)} to {say(-r[2], 1)}. <bookmark mark='b'/> It explains, in one sentence, why the newspapers saw the opposite. <bookmark mark='c'/> It states the assumptions in plain words, <bookmark mark='d'/> and a separate OLS sensitivity illustration. It does not quantify sensitivity to the missing-at-random assumption or directly bound the pooled AIPW effect. <bookmark mark='e'/> It says what independent evidence agrees. <bookmark mark='f'/> And it ends with advice the data support: keep the substitute on sale, promote it, and recommend clinical review for kidney disease or potassium-raising medicines because extra potassium can cause hyperkalaemia. No p-values, no Greek; every number in it traceable to the analysis."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(m[0]), FadeIn(m[1]), FadeIn(m[2][0]), FadeIn(m[2][1]))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(*[FadeIn(m[2][i], shift=RIGHT * 0.15) for i in groups[k]])
        self.wait(1.5)
        self.clear_scene()

    def truth(self):
        o = load("obs")
        r = o["res"]
        rows = fit_rows(VGroup(
            label(rf"the World's truth: \ the substitute lowers pressure by {-o['tau']:.1f} mm Hg, \ for everyone", font_size=26, color=EXACT),
            label(rf"our estimate: \ ${r['mi_aipw'][0]:.2f}$, \ interval [{r['mi_aipw'][2]:.2f}, \ {r['mi_aipw'][3]:.2f}]: \ it covers", font_size=26, color=GOODC),
            label(rf"with every income known: \ ${o['true_aipw'][0]:.2f}$: \ sampling variation and fitted-model approximation remain", font_size=24, color=GREY_A),
            label(rf"the headline's estimate: \ $+{r['naive'][0]:.1f}$: \ the wrong sign, \ with great confidence", font_size=26, color=NAIVEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The World can tell us what no real consultant ever learns. The substitute lowers everyone's pressure by exactly three millimetres. <bookmark mark='b'/> Our estimate, {say(r['mi_aipw'][0], 2)}, has an interval that covers it. <bookmark mark='c'/> Had every income been known, the same estimator would have given {say(o['true_aipw'][0], 2)}; the remaining gap can reflect sampling variation and fitted-model approximation, which the interval was built to allow for. <bookmark mark='d'/> The headline's comparison had the wrong sign, and a narrow interval around it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
