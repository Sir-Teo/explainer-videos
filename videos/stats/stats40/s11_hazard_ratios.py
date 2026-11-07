from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403
from videos.stats.stats40.s04_km import km_axes


class HazardRatios(VoiceoverScene):
    def construct(self):
        self.card()
        self.selection()
        self.drift()
        self.frail_share()
        self.why()
        self.rmst_def()
        self.rmst_gehan()

    def card(self):
        card = chapter_card(10, r"What hazard ratios mean", r"A ratio among survivors who are no longer comparable", lit=(2010, 2013), part=PART)
        with self.voiceover("Chapter ten. What hazard ratios mean."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def selection(self):
        rows = [
            cmath(r"\text{HR}(t)", r"=", r"\dfrac{h_1(t)}{h_0(t)}: \ \text{among those still alive at } t", font_size=30),
            cmath(r"\text{randomized at } 0", r":", r"\text{the arms are comparable at } t = 0 \text{ only}", font_size=30),
            cmath(r"\text{later}", r":", r"\text{a good treatment keeps frailer people alive}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{HR}(t) \text{ mixes the effect with who has survived}", font_size=30),
        ]
        rows[3][-1].set_color(MISSC)
        whys = [why(r"a conditional quantity"), why(r"randomization's guarantee"), why(r"selection by survival"),
                why(r"Hern\'an (2010)")]
        with self.voiceover(
            "<bookmark mark='a'/> A hazard ratio at time t compares the event rates among those still alive at t. "
            "<bookmark mark='b'/> Randomization makes the arms comparable at the start, and only at the start. <bookmark "
            "mark='c'/> If the treatment works, it keeps alive people who would otherwise have died, typically the frailer "
            "ones. <bookmark mark='d'/> So later in the trial the treated survivors are frailer on average than the control "
            "survivors, and the hazard ratio mixes the effect of the treatment with the selection it caused. Miguel Hernán "
            "called this the hazards of hazard ratios."
        ) as vo:
            heading = label('Survival changes the composition of treatment groups', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def drift(self):
        d = load("hr")
        P = d["periods"]
        hrs = np.asarray(d["hrs"], float)
        A = axes([0, 4], [0, 1.1], x_length=7.4, y_length=4.2, xlabel=r"years since randomization", ylabel=r"period incidence-rate ratio",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        segs = VGroup(*[Line(ax.c2p(a, h), ax.c2p(b, h), color=HAZC, stroke_width=6) for (a, b), h in zip(P, hrs)])
        truth = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=TRUEC, stroke_width=2.5)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(4, 1), color=GREY_D, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"a seeded trial: \ 20,000 patients", font_size=22),
            label(r"every patient's own HR: \ 0.5 \ (gold)", font_size=22, color=TRUEC),
            label(r"an unmeasured gamma frailty, \ variance 1", font_size=22, color=GREY_A),
            label(rf"period HRs: \ {hrs[0]:.2f}, \ {hrs[1]:.2f}, \ {hrs[2]:.2f}, \ {hrs[3]:.2f}", font_size=22, color=HAZC),
            label(rf"Cox HR (fixed 1,000-patient subsample): \ {d['cox_hr']:.2f}", font_size=22, color=SURVC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A seeded trial with twenty thousand patients. <bookmark mark='b'/> For every single"
            " patient, the treatment halves the hazard at every moment. <bookmark mark='c'/> Patients differ in an "
            "unmeasured frailty that multiplies their hazard. <bookmark mark='d'/> The empirical incidence-rate ratio"
            " in each period starts near one half, then drifts up toward one: " + ", ".join(say(h, 2) for h in hrs) + ". Nothing about the treatment changed. <bookmark mark='e'/> For speed, Cox is fitted to a fixed "
            "one-in-twenty subsample of one thousand patients and reports " + say(d["cox_hr"], 2)
            + ", an average of ratios among ever more different groups."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(one), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.4), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def frail_share(self):
        d = load("hr")
        ts = np.asarray(d["ts"], float)
        A = axes([0, 4], [0, 0.15], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"share of survivors with frailty $> 2$",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 0.05, 0.1, 0.15], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c0 = polyline(ax, ts, np.asarray(d["frail"]["0"], float), PLC, 3)
        c1 = polyline(ax, ts, np.asarray(d["frail"]["1"], float), MPC, 3)
        side = fit_rows(VGroup(
            label(r"at the start: about 13.5\% expected in each arm", font_size=22),
            label(r"control \ (red): \ the frail die fast", font_size=22, color=PLC),
            label(r"treated \ (green): \ more of them survive", font_size=22, color=MPC),
            label(r"the survivors are no longer comparable", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The mechanism. At randomization, about thirteen and a half percent are very frail "
            "in expectation in each arms. <bookmark mark='b'/> In the control arm the frail die quickly, <bookmark "
            "mark='c'/> and in the treated arm more of them survive. <bookmark mark='d'/> So the later comparison "
            "sets frailer treated survivors against hardier controls: randomized at the start, confounded by survival"
            " afterwards."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why(self):
        rows = fit_rows(VGroup(
            label(r"the log-rank test remains valid under its null and regularity conditions", font_size=26, color=SURVC),
            label(r"as a causal effect it is hard to read, \ even in a perfect trial", font_size=26, color=MISSC),
            label(r"report absolute quantities: \ survival at $t$, \ or the restricted mean", font_size=26, color=TAUC),
            label(r"and show the curves", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> None of this breaks the log-rank test: under the no-treatment-effect null, "
            "independent censoring and the usual risk-set conditions, the test is valid. <bookmark mark='b'/> But "
            "read as a causal effect, a hazard ratio is hard to interpret, even in a perfect randomized trial. "
            "<bookmark mark='c'/> Hernán's advice: report absolute quantities, the difference in survival at chosen "
            "times, or the difference in restricted mean survival, <bookmark mark='d'/> and show the curves."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rmst_def(self):
        rows = [
            cmath(r"\text{RMST}(\tau)", r"=", r"E \min(T, \tau) = \textstyle\int_0^\tau S(t)\, dt", font_size=32),
            cmath(r"\widehat{\text{RMST}}", r"=", r"\text{the area under the KM curve up to } \tau", font_size=30),
            cmath(r"\widehat{\text{Var}}", r"=", r"\textstyle\sum_{t_k \le \tau} A_k^2\, d_k / (n_k (n_k - d_k))", font_size=30),
            cmath(r"\text{difference}", r":", r"\text{time gained in the event-free state by }\tau;\ \text{no PH needed}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"the restricted mean"), why(r"Irwin (1949); \ Royston \& Parmar (2013)"), why(r"$A_k$: \ area after $t_k$"),
                why(r"a causal contrast")]
        with self.voiceover(
            "<bookmark mark='a'/> The restricted mean survival time is the expected lifetime capped at a horizon tau: the "
            "area under the survival curve up to tau. <bookmark mark='b'/> Its estimate is the area under the Kaplan-Meier "
            "curve, an old idea of Oscar Irwin's revived by Patrick Royston and Mahesh Parmar. <bookmark mark='c'/> Its "
            "variance has a Greenwood-like formula. <bookmark mark='d'/> The difference between arms is the average time "
            "gained by tau, in units a patient understands, and it needs no proportional hazards."
        ) as vo:
            heading = label('Restricted means measure event-free time over a chosen horizon', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rmst_gehan(self):
        d = load("gehan")
        t, e, g = (np.asarray(d[k], float) for k in ("time", "event", "group"))
        A = km_axes()
        ax = A.ax
        K1 = KMStaircase(ax, t[g == 1], e[g == 1].astype(int), color=MPC)
        K0 = KMStaircase(ax, t[g == 0], e[g == 0].astype(int), color=PLC)

        def area(K, col):
            pts = [ax.c2p(0, 0)] + [ax.c2p(a, b) for a, b in K._steps(K.km["surv"])] + [ax.c2p(35, 0)]
            pts = [p for p in pts]
            return Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.25)

        a1, a0 = area(K1, MPC), area(K0, PLC)
        r = d["rmst_diff"]
        side = fit_rows(VGroup(
            label(r"$\tau$ = 35 weeks; 3,999 matched-pair bootstrap resamples", font_size=22),
            label(rf"6-MP: \ {d['mp']['rmst']['rmst']:.1f} weeks \ (green area)", font_size=22, color=MPC),
            label(rf"placebo: \ {d['pl']['rmst']['rmst']:.1f} weeks \ (red area)", font_size=22, color=PLC),
            label(rf"gain: \ {r['diff']:.1f} weeks \ (95\% CI {r['ci'][0]:.1f}--{r['ci'][1]:.1f})", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Gehan's data, to thirty-five weeks. <bookmark mark='b'/> Under the 6-MP curve lies an "
            "area of " + say(d["mp"]["rmst"]["rmst"], 1) + " weeks, <bookmark mark='c'/> under the placebo curve "
            + say(d["pl"]["rmst"]["rmst"], 1) + ". <bookmark mark='d'/> Over the first thirty-five weeks, the drug gave "
            "patients on average " + say(r["diff"], 1) + " more weeks in remission, with an interval from "
            + say(r["ci"][0], 1) + " to " + say(r["ci"][1], 1) + ". This approximate percentile interval resamples the twenty-one original pairs, keeping each pair together and carrying its estimated curve flat to thirty-five weeks."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(K1.curve()), Create(K0.curve()), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(a1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(a0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
