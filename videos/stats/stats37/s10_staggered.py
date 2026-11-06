from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403

COH = {2004.0: Y1C, 2009.0: TAUC, 2014.0: IVC}
KIND = {"vs never": BANDC, "early vs later": Y0C, "later vs earlier": MISSC}


class Staggered(VoiceoverScene):
    def construct(self):
        self.card()
        self.staircase()
        self.verdict()
        self.bacon()
        self.why()
        self.fixes()
        self.event()
        self.board()

    def card(self):
        card = chapter_card(9, r"Staggered adoption", r"When two-way fixed effects get the sign wrong", lit=(2021,), part=PART)
        with self.voiceover("Chapter nine. Staggered adoption."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def staircase(self):
        d = load("staggered")
        c = d["counts"]
        years = np.arange(2000, 2020)
        cw, total_h = 0.34, 3.8
        groups = [(2004.0, c["2004"]), (2009.0, c["2009"]), (2014.0, c["2014"]), (np.inf, c["never"])]
        g = VGroup()
        labels = VGroup()
        y = total_h / 2 + 0.6
        for G, n in groups:
            h = total_h * n / 200
            row = VGroup(*[Rectangle(width=cw * 0.92, height=h * 0.94, stroke_width=0,
                                     fill_color=(COH[G] if (np.isfinite(G) and yr >= G) else "#2a3242"), fill_opacity=0.9)
                           .move_to([-4.6 + (yr - 2000) * cw, y - h / 2, 0]) for yr in years])
            g.add(row)
            name = rf"{int(G)}: \ {n} towns" if np.isfinite(G) else rf"never: \ {n} towns"
            labels.add(label(name, font_size=20, color=COH.get(G, GREY_A)).next_to(row, LEFT, buff=0.2))
            y -= h
        yl = VGroup(label(r"2000", font_size=18, color=GREY_B).next_to(g[-1][0], DOWN, buff=0.15),
                    label(r"2019", font_size=18, color=GREY_B).next_to(g[-1][-1], DOWN, buff=0.15))
        side = fit_rows(VGroup(
            label(r"the World's rollout: \ 200 towns adopt in three waves", font_size=22),
            label(r"the effect grows with time since adoption", font_size=22, color=TAUC),
            label(r"faster in early towns: \ 0.7, \ 0.3, \ 0.05 points a year", font_size=22, color=Y1C),
            label(rf"the truth: \ ATT = {d['truth']:.2f} points", font_size=22, color=TRUEC),
        ), 3.8, 0.42, [4.9, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Most real policies do not start everywhere at once. In the World's full rollout, " +
            str(c["2004"]) + " towns adopt the jobs programme in 2004, " + str(c["2009"]) + " in 2009, " + str(c["2014"])
            + " in 2014, and " + str(c["never"]) + " never do. Each coloured cell is a treated town-year. <bookmark mark='b'/> "
            "The programme's effect grows the longer a town has had it: workers are trained, firms move in. <bookmark "
            "mark='c'/> It grows faster in the early towns, which were keenest: seven tenths of a point a year, against three "
            "tenths and five hundredths. <bookmark mark='d'/> Averaged over all treated town-years, the true effect is "
            + say(d["truth"], 2) + " points of employment."
        ) as vo:
            self.add(rollout_tag())
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), FadeIn(labels), FadeIn(yl), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def verdict(self):
        d = load("staggered")
        tw = d["twfe"]
        rows = fit_rows(VGroup(
            label(r"the standard regression: \ $Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \varepsilon_{it}$", font_size=28),
            label(rf"two-way fixed effects: \ $\hat\beta$ = {tw['beta']:.2f} \ (clustered SE {tw['se']:.2f})", font_size=28, color=MISSC),
            label(rf"the truth: \ +{d['truth']:.2f}", font_size=28, color=TRUEC),
            label(r"a programme that raised employment everywhere it went, \ estimated to have lowered it", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For decades the standard analysis was the regression of chapter seven: town effects, "
            "year effects, and a treatment indicator. <bookmark mark='b'/> On the World's rollout it says minus "
            + say(-tw["beta"], 2) + ", with a clustered standard error of " + say(tw["se"], 2) + ". <bookmark mark='c'/> The "
            "truth is plus " + say(d["truth"], 2) + ". <bookmark mark='d'/> A programme that raised employment in every town "
            "and every year it ran is estimated, confidently, to have lowered it. Every town has parallel trends, and no "
            "assumption of chapter seven is violated. The regression itself is the problem."
        ) as vo:
            self.add(rollout_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def bacon(self):
        d = load("staggered")
        bac = d["bacon"]
        A = axes([0, 0.25], [-6, 6], x_length=6.6, y_length=4.4, xlabel=r"weight in the TWFE estimate", ylabel=r"2$\times$2 DiD estimate",
                 xticks=[0, 0.1, 0.2], yticks=[-6, -3, 0, 3, 6], xfmt=lambda v: f"{v:g}", center=[-2.6, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(o["w"], o["est"]), radius=0.1, color=KIND[o["kind"]]) for o in bac])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.25, 0), color=GREY_C, stroke_width=1.5)
        tw = DashedLine(ax.c2p(0, d["twfe"]["beta"]), ax.c2p(0.25, d["twfe"]["beta"]), color=MISSC, stroke_width=2.5)
        bk = d["by_kind"]
        rows = [[r"comparison", r"weight", r"average"]]
        for k, nm in (("vs never", r"vs never treated"), ("early vs later", r"early vs not-yet-treated"),
                      ("later vs earlier", r"later vs already treated")):
            rows.append([nm, f"{bk[k]['w']:.2f}", f"{bk[k]['est']:+.2f}"])
        tab = table_rows(rows, font_size=22, col_buff=0.45, row_buff=0.22, colors=[GREY_A, KIND["vs never"], KIND["early vs later"], KIND["later vs earlier"]])
        tab.move_to([4.3, 0.9, 0])
        foot = label(rf"weighted sum: \ {d['twfe']['beta']:.2f} \ = TWFE", font_size=22, color=MISSC).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Andrew Goodman-Bacon showed in 2021 what the regression actually does. Its coefficient is a "
            "weighted average of every simple two-by-two difference-in-differences between groups of towns that adopt at "
            "different times. <bookmark mark='b'/> Comparisons with the never-treated towns: good comparisons, positive. "
            "<bookmark mark='c'/> Early adopters against towns that have not adopted yet: also fine, positive. <bookmark "
            "mark='d'/> But also the later adopters against towns that already have the programme, using them as controls. "
            "Their outcomes are still rising, because their effect is still growing, so the later adopters look bad by "
            "comparison. These forbidden comparisons get almost half the weight, and they are strongly negative. <bookmark "
            "mark='e'/> The weighted sum is exactly the regression's minus " + say(-d["twfe"]["beta"], 2) + "."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), Create(zero), FadeIn(tab[0]))
            for k, kind in zip("bcd", ("vs never", "early vs later", "later vs earlier")):
                vo.wait_until(k)
                self.play(*[FadeIn(dots[i], scale=0.5) for i, o in enumerate(bac) if o["kind"] == kind],
                          FadeIn(tab["bcd".index(k) + 1]))
            vo.wait_until("e")
            self.play(Create(tw), FadeIn(foot))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"\text{a 2}{\times}\text{2 with already-treated controls}", r":", r"\Delta Y_{\text{late}} - \Delta Y_{\text{early}}", font_size=30),
            cmath(r"\Delta Y_{\text{early}}", r"=", r"\Delta Y(0) + \Delta\tau_{\text{early}}", font_size=30),
            cmath(r"\Rightarrow", r":", r"\tau_{\text{late}} - \Delta\tau_{\text{early}}", font_size=30),
            cmath(r"\text{fine iff}", r":", r"\text{effects are constant over time}", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"the forbidden comparison"), why(r"the controls' effect is still changing"),
                why(r"can be negative when every effect is positive"), why(r"de Chaisemartin \& D'Haultf\oe uille (2020)")]
        with self.voiceover(
            "<bookmark mark='a'/> Why the forbidden comparisons mislead: a two-by-two with already-treated towns as the "
            "control subtracts their change in outcomes. <bookmark mark='b'/> But their change includes the growth in their "
            "own treatment effect. <bookmark mark='c'/> So the comparison estimates the late towns' effect minus the change "
            "in the early towns' effect, which can be negative even when every effect is positive. <bookmark mark='d'/> If "
            "effects were constant over time, the problem would vanish. They rarely are. Clément de Chaisemartin and Xavier "
            "D'Haultfœuille showed the same thing in 2020: some treated units can even get negative weights."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fixes(self):
        d = load("staggered")
        cs = d["cs"]
        rows = fit_rows(VGroup(
            label(r"never use the already treated as controls", font_size=26, color=TAUC),
            label(rf"Callaway \& Sant'Anna (2021): \ ATT$(g,t)$ against the never treated, \ then average: \ {cs['att']:.2f} \ ({cs['ci'][0]:.2f} to {cs['ci'][1]:.2f})", font_size=26, color=BANDC),
            label(rf"Borusyak, \ Jaravel \& Spiess (2024): \ fit $\alpha_i + \gamma_t$ on untreated cells, \ impute $Y(0)$: \ {d['imputation']:.2f}", font_size=26, color=BANDC),
            label(rf"Sun \& Abraham (2021): \ interact the event-study leads and lags with cohort; \ the truth {d['truth']:.2f}", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The cure, discovered by several teams at once, is never to use already-treated units as "
            "controls. <bookmark mark='b'/> Brantly Callaway and Pedro Sant'Anna estimate a separate effect for each "
            "adoption cohort and each year, against the never-treated towns, then average them: " + say(cs["att"], 2) + ", "
            "with an interval from " + say(cs["ci"][0], 2) + " to " + say(cs["ci"][1], 2) + ". <bookmark mark='c'/> Kirill "
            "Borusyak, Xavier Jaravel and Jann Spiess fit the town and year effects on untreated town-years only, impute "
            "what every treated town-year would have been, and average the differences: " + say(d["imputation"], 2) + ". "
            "<bookmark mark='d'/> Liyang Sun and Sarah Abraham fix the event study by interacting it with cohort. All of "
            "them land near the truth, " + say(d["truth"], 2) + "."
        ) as vo:
            self.add(rollout_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def event(self):
        d = load("staggered")
        es = d["es"]
        k = np.asarray(es["k"], float)
        b = np.asarray(es["b"], float)
        ce = {float(a): v for a, v in d["cs_event"].items()}
        e = np.arange(-6, 11, 1.0)
        csv = np.array([ce.get(x, np.nan) for x in e])
        te = {float(a): v for a, v in d["truth_e"].items()}
        tr = np.array([te.get(x, 0.0) for x in e])
        A = axes([-6, 10], [-1, 9], x_length=7.6, y_length=4.4, xlabel=r"years since adoption", ylabel=r"effect estimate",
                 xticks=[-6, -3, 0, 3, 6, 9], yticks=[0, 3, 6, 9], center=[-1.8, 0.2, 0])
        ax = A.ax
        tw = VGroup(*[Dot(ax.c2p(a, v), radius=0.07, color=MISSC) for a, v in zip(k, b)])
        cs = VGroup(*[Dot(ax.c2p(a, v), radius=0.07, color=BANDC) for a, v in zip(e, csv) if np.isfinite(v)])
        trl = polyline(ax, e, tr, TRUEC, 2.5)
        zero = DashedLine(ax.c2p(-6, 0), ax.c2p(10, 0), color=GREY_C, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"red: \ the TWFE event study \ (ends binned)", font_size=22, color=MISSC),
            label(r"green: \ Callaway--Sant'Anna by event time", font_size=22, color=BANDC),
            label(r"gold: \ the truth", font_size=22, color=TRUEC),
            label(r"TWFE shows a pre-trend that is not there", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The event-study version of the regression suffers too. Its coefficients mix effects from "
            "other years and cohorts, as Sun and Abraham showed. <bookmark mark='b'/> Here it shows leads well above zero, "
            "a pre-trend that does not exist, and lags that are too small. <bookmark mark='c'/> The Callaway and Sant'Anna "
            "estimates by event time sit close to zero before adoption, and follow the truth after it, which keeps rising "
            "because the early towns dominate the later years."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(Create(trl), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(tw), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(cs), FadeIn(side[1]))
        self.clear_scene()

    def board(self):
        rows = board_rows("TWFE", "Callaway")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, five hundred fresh draws of the rollout. The two-way fixed-effects "
                   "interval covers the true effect on the treated " + f"{100 * rows[0].achieved:.0f}" + " percent of the "
                   "time: broken. <bookmark mark='b'/> Callaway and Sant'Anna's interval covers it "
                   + f"{100 * rows[1].achieved:.0f}" + " percent of the time: kept, a shade low with only twenty "
                   "never-treated towns.",
                   [("a", [0]), ("b", [1])])
