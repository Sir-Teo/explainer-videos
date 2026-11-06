from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.first()
        self.second()
        self.repeat()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1983,)).to_edge(UP, buff=0.35)
        hc = history_card(1983, r"David Freedman, \ \emph{The American Statistician}",
                          r"take 100 observations of a response and 50 predictors, \ all of them independent random noise. \ "
                          r"Regress, \ keep the predictors that look promising, \ and regress again. \ The second regression "
                          r"is `highly significant': \ a model found in nothing at all",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"`A note on screening regression equations'", font_size=24),
            label(r"the standard practice of the day, \ run on pure noise", font_size=24, color=RES),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1983 David Freedman ran an experiment on an empty box. A hundred observations of a "
            "response and fifty predictors, every one of them independent random noise. Regress the response on all fifty, "
            "keep the predictors that look promising, and run the regression again. <bookmark mark='b'/> It was the standard "
            "practice of the day. <bookmark mark='c'/> Run on pure noise, it finds a significant model."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def pvalues(self, stage, color, center):
        d = load("freedman")["one"][stage]
        p = np.asarray(d["p"])
        k = len(p)
        A = axes([-0.5, 50 - 0.5], [0, 1], x_length=10.0, y_length=2.4, xlabel=r"", ylabel=r"$p$-value",
                 xticks=[], yticks=[0, 0.25, 1], center=center)
        ax = A.ax
        cols = d["cols"]
        dots = VGroup(*[Dot(ax.c2p(int(c), v), radius=0.07, color=RES if v < 0.05 else (color if v < 0.25 else GREY_B))
                        for c, v in zip(cols, p)])
        cut = DashedLine(ax.c2p(-0.5, 0.25), ax.c2p(49.5, 0.25), color=PATH, stroke_width=2)
        return A, dots, cut, d

    def first(self):
        A, dots, cut, d = self.pvalues("first", AICC, [0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(rf"round 1: \ all 50 noise predictors; \ $R^2 = {d['r2']:.2f}$, \ overall $F$ test $p = {d['pF']:.2f}$", font_size=24),
            label(rf"{d['n_sig25']} predictors with $p < 0.25$: \ keep them", font_size=24, color=AICC),
            label(rf"{d['n_sig05']} with $p < 0.05$ \ (2.5 expected by chance)", font_size=24, color=RES),
        ), 12.0, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Round one. Each dot is one predictor's p-value. With fifty predictors and a hundred "
            "observations, R squared is point four six, but the overall F test, p of point seven six, rightly says there is "
            "nothing here. <bookmark mark='b'/> Fourteen predictors have p-values below point two five: keep those. "
            "<bookmark mark='c'/> Two are below point oh five, about what chance would give."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(cut))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[x.animate.scale(1.4) for x in dots if x.get_color() != ManimColor(GREY_B)], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def second(self):
        A, dots, cut, d = self.pvalues("second", AICC, [0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(rf"round 2: \ only the {len(d['cols'])} kept; \ $R^2 = {d['r2']:.2f}$", font_size=24),
            label(rf"overall $F = {d['F']:.2f}$, \ $p = {d['pF']:.3f}$: \ `significant'", font_size=24, color=RES),
            label(rf"{d['n_sig05']} coefficients with $p < 0.05$", font_size=24, color=RES),
            label(r"every number here is pure noise", font_size=24, color=PATH),
        ), 12.0, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Round two: regress again on only the fourteen kept. R squared is still point two seven, "
            "from fewer predictors. <bookmark mark='b'/> Now the overall F test gives p of point oh one three: significant. "
            "<bookmark mark='c'/> Four individual coefficients are significant at five percent. <bookmark mark='d'/> Every "
            "number in this regression is noise. The p-values were computed as if the fourteen had been chosen in advance, "
            "but they were chosen for looking significant."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(cut))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def repeat(self):
        d = load("freedman")
        h = np.asarray(d["pF_hist"], float)
        edges = np.linspace(0, 1, 21)
        h = h / h.sum() / (edges[1] - edges[0])
        A = axes([0, 1], [0, float(h.max()) * 1.1], x_length=7.4, y_length=4.2, xlabel=r"round-2 $F$-test $p$-value",
                 ylabel=r"density, \ 1,000 noise experiments", xticks=[0, 0.05, 0.5, 1], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=RES, opacity=0.6)
        unif = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"repeat Freedman's experiment 1,000 times", font_size=22),
            label(r"grey: \ what honest $p$-values would look like", font_size=22, color=GREY_B),
            label(rf"round 2 `significant' at 5\%: \ {100 * d['share_sig']:.0f}\% of the time", font_size=22, color=RES),
            label(rf"median {d['median_kept']:.0f} predictors kept; \ {d['mean_sig']:.1f} `significant' on average", font_size=22, color=GREY_A),
        ), 4.4, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Was that run unlucky? Repeat the experiment a thousand times. <bookmark mark='b'/> Honest "
            "p-values would spread evenly between zero and one, the grey line. <bookmark mark='c'/> The second-round p-values "
            "pile up near zero: ninety-five percent of the time, pure noise produces a significant regression. "
            "<bookmark mark='d'/> Typically twelve predictors survive screening, and five or six of them look individually "
            "significant."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(unif))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"choosing a model with the data, \ then testing it on the same data, \ is circular", font_size=26, color=RES),
            label(r"the fit always improves with more choice: \ that is optimism", font_size=26),
            label(r"so: \ estimate it (AIC, \ BIC, \ CV), \ avoid it (splitting), \ or correct for it", font_size=26, color=HIT),
            label(r"and ask what the chosen model is for: \ prediction, \ or truth?", font_size=26, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson: choosing a model with the data, then testing it on the same data, is circular. "
            "<bookmark mark='b'/> The more choice you have, the better the chosen fit looks, whether or not anything is "
            "there; statisticians call the gap optimism. <bookmark mark='c'/> This part shows how to estimate it, with AIC, "
            "BIC and cross-validation, how to avoid it, by splitting the data, and how to correct inference for it. "
            "<bookmark mark='d'/> And it asks what the chosen model is for: to predict well, or to find the truth, which turn "
            "out to be different goals."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 28", font_size=34, color=GREY_B), label(r"Which Model?", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"optimism, \ degrees of freedom, \ Cp, \ AIC and TIC",
            r"BIC, \ consistency vs efficiency; \ cross-validation's theory",
            r"Bayesian LOO and WAIC; \ singular models; \ MDL",
            r"averaging vs choosing: \ BMA and stacking",
            r"inference after selection; \ subset selection; \ calibrated forecasts",
        ], color=AICC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 19, \ 22 and 26").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.select}; \ the model-selection bench").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-eight: which model? <bookmark mark='b'/> We'll measure optimism and degrees of "
            "freedom and derive Mallows's Cp, Akaike's criterion and Takeuchi's; derive BIC and see why consistency and "
            "efficiency conflict; learn what cross-validation really estimates; compute Bayesian leave-one-out and WAIC; see "
            "singular models break BIC; meet minimum description length; compare averaging with choosing; correct inference "
            "after selection; pit best subset against the lasso; and grade probability forecasts for calibration."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
