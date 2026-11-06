from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Cox(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.partial()
        self.ties()
        self.gehan()
        self.mayo()
        self.curves()
        self.trial()

    def card(self):
        card = chapter_card(8, r"Cox's partial likelihood", r"Regression without the baseline hazard", lit=(1972,), part=PART)
        with self.voiceover("Chapter eight. Cox's partial likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"h(t \mid x)", r"=", r"h_0(t)\, e^{x^\top \beta}", font_size=36),
            cmath(r"h_0(t)", r":", r"\text{any baseline hazard, \ left unspecified}", font_size=30),
            cmath(r"e^{\beta_j}", r":", r"\text{the hazard ratio for one unit of } x_j, \ \text{the same at every } t", font_size=30),
            cmath(r"\text{semiparametric}", r":", r"\text{a finite } \beta, \ \text{an infinite-dimensional } h_0", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"proportional hazards"), why(r"no shape assumed"), why(r"a multiplicative effect"), why(r"Part 49's subject")]
        with self.voiceover(
            "<bookmark mark='a'/> David Cox's model of 1972: each person's hazard is a common baseline hazard multiplied "
            "by e to the linear predictor. <bookmark mark='b'/> The baseline can have any shape at all, and is left "
            "unspecified. <bookmark mark='c'/> Each e to the beta j is a hazard ratio, the factor by which the hazard "
            "is multiplied for one unit of x j, and it is the same at every time: the proportional hazards assumption. "
            "<bookmark mark='d'/> A few parameters of interest and an infinite-dimensional nuisance: a semiparametric "
            "model, the kind Part forty-nine studies."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def partial(self):
        rows = [
            cmath(r"P(i \text{ fails} \mid \text{one failure at } t_i)", r"=", r"\dfrac{h_0(t_i) e^{x_i^\top \beta}}{\sum_{j \in R(t_i)} h_0(t_i) e^{x_j^\top \beta}}", font_size=30),
            cmath(r"\phantom{P}", r"=", r"\dfrac{e^{x_i^\top \beta}}{\sum_{j \in R(t_i)} e^{x_j^\top \beta}}: \ h_0 \text{ cancels}", font_size=30),
            cmath(r"PL(\beta)", r"=", r"\textstyle\prod_{\text{events } i} e^{x_i^\top \beta} \big/ \textstyle\sum_{j \in R(t_i)} e^{x_j^\top \beta}", font_size=30),
            cmath(r"U(\beta)", r"=", r"\textstyle\sum_i \big(x_i - \bar x(t_i; \beta)\big): \ \text{observed minus risk-set average}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"who, \ of those at risk?"), why(r"the baseline disappears"), why(r"Cox (1972, \ 1975)"),
                why(r"$\bar x$ weighted by $e^{x^\top\beta}$")]
        with self.voiceover(
            "<bookmark mark='a'/> Cox's insight. At each event time, ask: given that one of the people at risk fails "
            "now, what is the chance it is this one? It is their hazard over the sum of everyone's hazards in the risk set. "
            "<bookmark mark='b'/> The unknown baseline hazard multiplies the top and every term at the bottom, so it "
            "cancels. <bookmark mark='c'/> Multiply these conditional probabilities over the event times: the partial "
            "likelihood, which depends on beta alone. Cox showed in 1975 that maximizing it behaves like ordinary maximum "
            "likelihood. <bookmark mark='d'/> Its score is a sum over events of each failure's covariate minus the "
            "hazard-weighted average among those at risk: observed minus expected once more."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ties(self):
        rows = [
            cmath(r"\text{tied events}", r":", r"\text{times are rounded \ (weeks, \ days)}", font_size=30),
            cmath(r"\text{Breslow}", r":", r"\text{every tied failure faces the full risk set}", font_size=30),
            cmath(r"\text{Efron}", r":", r"\text{the tied failures leave the risk set one share at a time}", font_size=30),
            cmath(r"\text{exact}", r":", r"\text{all orderings, \ or a conditional logistic likelihood}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"continuous time, \ discrete data"), why(r"Breslow (1974): \ simple, \ biased toward 0"),
                why(r"Efron (1977): \ the usual default"), why(r"Kalbfleisch \& Prentice")]
        with self.voiceover(
            "<bookmark mark='a'/> The model is for continuous time, but real times are rounded, so several events share a "
            "time. <bookmark mark='b'/> Norman Breslow's approximation lets every tied failure face the full risk set; it "
            "is simple, and pulls estimates toward zero when ties are many. <bookmark mark='c'/> Efron's approximation of "
            "1977 removes the tied failures from the risk set gradually, one average share at a time, and is the usual "
            "default. <bookmark mark='d'/> Exact methods average over all orderings."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gehan(self):
        d = load("gehan")
        b, e = d["cox_breslow"], d["cox_efron"]
        rows = [[r"Gehan's data, \ placebo vs 6-MP", r"Breslow", r"Efron"],
                [r"$\hat\beta$ \ (SE)", f"{b['beta']:.3f} ({b['se']:.3f})", f"{e['beta']:.3f} ({e['se']:.3f})"],
                [r"hazard ratio", f"{b['hr']:.2f}", f"{e['hr']:.2f}"],
                [r"95\% CI", f"{b['ci'][0]:.2f}--{b['ci'][1]:.2f}", f"{e['ci'][0]:.2f}--{e['ci'][1]:.2f}"],
                [r"score test", f"{b['score']:.2f}", f"{e['score']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.34, colors=[GREY_A, None, TAUC, None, GREY_B]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"the placebo arm's hazard is about {e['hr']:.1f} times the drug arm's, \ at every week", font_size=24, color=TAUC),
            label(rf"without ties, \ Cox's score test is the log-rank test exactly \ (here: \ {b['score']:.1f} vs {d['logrank']['chi2']:.1f})", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Gehan's data, with placebo as the covariate. <bookmark mark='b'/> Efron's method gives a "
            "hazard ratio of " + say(e["hr"], 1) + ", with a ninety-five percent interval from " + say(e["ci"][0], 1)
            + " to " + say(e["ci"][1], 1) + "; Breslow's, with these many ties, a little less. <bookmark mark='c'/> On "
            "placebo the hazard of relapse is nearly five times that on the drug, week after week, if the hazards are "
            "proportional. <bookmark mark='d'/> And with no tied times, Cox's score test for a single group indicator is "
            "exactly the log-rank test; here the ties make them differ a little."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]])
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def mayo(self):
        d = load("pbc")
        rows = [[r"Mayo PBC model \ (312 patients, \ 125 deaths)", r"HR", r"95\% CI"]]
        for n, h, lo, hi in zip(d["names"], d["hr"], d["lo"], d["hi"]):
            rows.append([n, f"{h:.2f}", f"{lo:.2f}--{hi:.2f}"])
        tab = table_rows(rows, font_size=26, col_buff=1.0, row_buff=0.3, colors=[GREY_A, None, MISSC, MISSC, BANDC, MISSC]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"doubling bilirubin multiplies the hazard by {d['hr'][2] ** np.log(2):.2f}", font_size=24, color=MISSC),
            label(r"the Mayo risk score \ (Dickson et al.\ 1989): \ these five, \ used to time liver transplants", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real regression. Primary biliary cholangitis is a slow autoimmune disease of the "
            "liver's bile ducts. The Mayo Clinic's trial of 1974 to 1984 followed three hundred and twelve patients; one "
            "hundred and twenty-five died. <bookmark mark='b'/> Cox's model with age, oedema, and the logs of bilirubin, "
            "albumin and prothrombin time reproduces the famous Mayo model. Older age, oedema, high bilirubin and slow "
            "clotting raise the hazard; albumin lowers it. <bookmark mark='c'/> Doubling bilirubin multiplies the hazard by "
            + say(d["hr"][2] ** np.log(2), 2) + ". <bookmark mark='d'/> E. Rolland Dickson and colleagues turned these five "
            "into a risk score that hepatologists used to decide when to transplant."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]])
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def curves(self):
        d = load("pbc")
        grid = np.asarray(d["grid"], float)
        A = axes([0, 12], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"predicted survival",
                 xticks=[0, 3, 6, 9, 12], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = polyline(ax, grid, np.asarray(d["S_med"], float), SURVC, 3)
        c2 = polyline(ax, grid, np.asarray(d["S_high"], float), MISSC, 3)
        side = fit_rows(VGroup(
            label(r"Breslow's baseline: \ $\hat H_0(t) = \sum_{t_k \le t} d_k / \sum_{R} e^{x^\top \hat\beta}$", font_size=22),
            label(rf"blue: \ a typical patient \ (bilirubin {d['bili_med']:.1f})", font_size=22, color=SURVC),
            label(r"red: \ the same patient with bilirubin 8", font_size=22, color=MISSC),
            label(r"$S(t \mid x) = \exp(-\hat H_0(t)\, e^{x^\top \hat\beta})$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> To predict, the baseline is needed after all. Breslow's estimator is a Nelson-Aalen "
            "estimator in which each person at risk counts by their hazard ratio. <bookmark mark='b'/> A typical patient, "
            "with median values of all five, <bookmark mark='c'/> and the same patient with a bilirubin of eight: half are "
            "dead within about five years. <bookmark mark='d'/> Each curve is the baseline raised to the power of that "
            "patient's hazard ratio."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def trial(self):
        d = load("pbc")
        A = axes([0, 12.5], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"survival",
                 xticks=[0, 3, 6, 9, 12], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax

        def stair(k, col):
            t, s = np.asarray(k["t"], float), np.asarray(k["surv"], float)
            pts = [(0, 1.0)]
            prev = 1.0
            for a, b in zip(t, s):
                pts += [(a, prev), (a, b)]
                prev = b
            pts.append((12.5, prev))
            m = VMobject(stroke_color=col, stroke_width=3)
            m.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
            return m

        c1, c2 = stair(d["km_trt"]["1"], MPC), stair(d["km_trt"]["2"], GREY_B)
        side = fit_rows(VGroup(
            label(r"green: \ D-penicillamine; \ grey: \ placebo", font_size=22),
            label(rf"HR {d['trt_hr']:.2f} \ (95\% CI {d['trt_ci'][0]:.2f}--{d['trt_ci'][1]:.2f})", font_size=22, color=TAUC),
            label(rf"log-rank $p = {d['trt_logrank_p']:.2f}$", font_size=22, color=TAUC),
            label(r"a well-powered null: \ the drug does not help", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The trial itself tested D-penicillamine against placebo. <bookmark mark='b'/> The "
            "curves lie on top of each other: a hazard ratio of " + say(d["trt_hr"], 2) + ", with an interval from "
            + say(d["trt_ci"][0], 2) + " to " + say(d["trt_ci"][1], 1) + ", <bookmark mark='c'/> and a log-rank p-value of "
            + say(d["trt_logrank_p"], 2) + ". <bookmark mark='d'/> The drug did not help. The lasting value of the trial was "
            "its careful follow-up, which gave medicine the prognostic model."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(c1), Create(c2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
