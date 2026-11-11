from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load, tt


class Decay(VoiceoverScene):
    def construct(self):
        d = load("decay")
        self.card()
        self.lags(d)
        self.years(d)
        self.model()
        self.speed(d)
        self.factory()
        self.crowding()
        self.question()

    def card(self):
        c = chapter_card(9, r"Decay, crowding and the alpha factory", r"How long does a mined signal last, and who else "
                         r"has found it?", part=PART)
        with self.voiceover("Chapter nine. A signal can fade in two ways: over the days after it is measured, and over "
                            "the years, as others find it. How long does a mined signal last?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lags(self, d):
        L = d["lag"]
        hs = np.array(sorted(int(k) for k in L), float)
        tr = np.array([L[str(int(h))]["train"] for h in hs])
        va = np.array([L[str(int(h))]["valid"] for h in hs])
        top = float(np.ceil(max(tr.max(), va.max()) * 100 + 1) / 100)
        g = axes([1, hs[-1]], [0, top], x_length=7.2, y_length=4.4, xlabel=r"the day ahead, $h$",
                 ylabel=r"IC with the return on day $t + h$ alone", xticks=[1, 5, 10], yticks=[0, top / 2, top],
                 yfmt=lambda v: f"{v:.2f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lt = VGroup(curve(ax, hs, tr, TRAIN_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.05, color=TRAIN_C)
                                                                  for a, b in zip(hs, tr)])
        lv = VGroup(curve(ax, hs, va, VALID_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.05, color=VALID_C)
                                                                  for a, b in zip(hs, va)])
        leg = legend([(TRAIN_C, r"2018--19"), (VALID_C, r"2020")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(label(r"the best random formula:", font_size=15, color=GREY_B),
                      label(tt(d["formula"], 44), font_size=13, color=FORMULA),
                      wrapped_label(r"Kakushadze's 101 alphas hold for 0.6 to 6.4 days on average; this one fades far "
                                    r"more slowly", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(
            leg, DOWN, buff=0.35)
        fit_right(side)
        h10 = L[str(int(hs[-1]))]
        with self.voiceover(
            f"""First measure prediction by horizon in the supplied research grid. <bookmark mark='a'/> The training-selected formula is held fixed while its rank correlation is measured against each individual future day's log return. <bookmark mark='b'/> Training IC is {tr[0]:.3f} tomorrow and {h10['train']:.3f} ten days ahead; validation gives {va[0]:.3f} and {h10['valid']:.3f}. Shared observations and overlapping horizons make these related diagnostics. Persistence can reflect stable characteristics and data conventions. It does not by itself identify a crowding mechanism, feasible execution or lower costs; the measured book turnover is a separate calculation."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def years(self, d):
        by = d["by_year"]
        ys = sorted(by)
        vals = [by[y] for y in ys]
        top = float(np.ceil(max(vals) * 100 + 1) / 100)
        g = axes([2017.4, 2020.6], [0, top], x_length=6.0, y_length=4.0, xlabel=r"", ylabel=r"mean daily IC",
                 xticks=[2018, 2019, 2020], yticks=[0, top / 2, top], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                 font_size=15).move_to(LEFT * 2.2 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=(VALID_C if int(y) == 2020 else TRAIN_C), fill_opacity=0.85).move_to(
            ax.c2p(int(y), 0), aligned_edge=DOWN) for y, v in zip(ys, vals)])
        labs = VGroup(*[MathTex(f"{v:.3f}", font_size=22).next_to(b, UP, buff=0.1) for b, v in zip(bars, vals)])
        side = wrapped_label(r"three research years cannot identify a crowding-decay rate; later strategy evaluation "
                             r"is excluded from this review", 4.0, 16, GREY_A).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            f"""Within the original research slice, the formula's yearly means are {vals[0]:.3f}, {vals[1]:.3f} and {vals[2]:.3f}. <bookmark mark='a'/> These are three observations for a training-selected formula, with one repeatedly inspected validation year. <bookmark mark='b'/> Changes can reflect sampling, universe composition and regimes, not just crowding. Three years do not identify a causal rate of alpha decay. The sealed strategy evaluation remains excluded; this review adds no later performance observations."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"IC_h", r"\approx", r"IC_1\,\phi^{\,h - 1}", font_size=34, colors={r"IC_h": TRAIN_C}),
                cmath(r"\text{turnover}", r"\propto", r"\sqrt{1 - \operatorname{Corr}(s_t, s_{t-1})}", font_size=32),
                cmath(r"\text{net}", r"=", r"\text{edge} - \text{cost} \times \text{turnover}", font_size=34,
                      colors={r"\text{net}": GOOD}),
                cmath(r"\text{edge}_{\text{after}}", r"\approx", r"0.42 \times \text{edge}_{\text{before}}\quad "
                      r"\text{(McLean and Pontiff)}", font_size=30, colors={r"\text{edge}_{\text{after}}": BAD})]
        whys = [why(r"decay with the horizon: a fast signal has $\phi$ near zero, a slow one near one"),
                why(r"stationary Gaussian positions with fixed variance and a fixed linear holdings rule: "
                    r"mean absolute changes scale with the square root of one minus autocorrelation"),
                why(r"the desk keeps what the costs leave: fast alphas need cheap execution (Part 31)"),
                why(r"decay through time: across 97 published US anomalies, returns fell 26\% out of sample and 58\% "
                    r"after publication (McLean and Pontiff 2016, \textit{Journal of Finance})")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Separate two illustrative mechanisms from one reported comparison. <bookmark mark='a'/> The geometric horizon pattern assumes a chosen phi; it is not fitted as a universal law here. <bookmark mark='b'/> For a stationary Gaussian position process with fixed variance and a fixed linear mapping to holdings, mean absolute changes scale with square root one minus autocorrelation. Rank books, changing membership and constraints need separate turnover accounting. <bookmark mark='c'/> Net edge subtracts costs using a stated exposure denominator and convention. <bookmark mark='d'/> McLean and Pontiff report26percent lower predictor returns out of sample and58percent lower after publication across97 stock predictors. Those are particular sample comparisons, not universal decay constants or a complete causal decomposition of crowding."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def speed(self, d):
        sp = d["speed"]
        names = [("mined", r"the mined alpha", FORMULA), ("Alpha#12", r"Alpha\#12", BAD), ("Alpha#41", r"Alpha\#41", BAD),
                 ("Alpha#101", r"Alpha\#101", BAD)]
        hx = [-3.6, 0.4, 3.4]
        head = VGroup(label(r"signal", font_size=18, color=GREY_B), label(r"rank autocorrelation, day to day", font_size=18,
                                                                          color=GREY_B),
                      label(r"turnover a day, per \$1 long", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for k, t, col in names:
            tab.add(VGroup(label(t, font_size=20, color=col), MathTex(f"{sp[k]['autocorr']:+.3f}", font_size=26),
                           MathTex(rf"\${sp[k]['turnover']:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        cost_m = 365 * sp["mined"]["turnover"] * 5 / 1e4
        cost_c = 365 * sp["Alpha#12"]["turnover"] * 5 / 1e4
        foot = wrapped_label(rf"linear cost illustration: 365 days times mean dollars traded times 5 bp one way; "
                             rf"{100 * cost_m:.0f}\% mined, {100 * cost_c:.0f}\% Alpha\#12, per dollar long per year", 11.4, 17,
                             GREY_A).to_edge(DOWN, buff=0.6)
        a_m, t_m = sp["mined"]["autocorr"], sp["mined"]["turnover"]
        t_12 = sp["Alpha#12"]["turnover"]
        pc_m, pc_c = 100 * cost_m, 100 * cost_c
        with self.voiceover(
            f"""Measure signal persistence and dollar trading separately. <bookmark mark='a'/> The mined signal has rank autocorrelation {a_m:.3f} and trades {t_m:.2f} dollars per day per dollar long. <bookmark mark='b'/> The adapted classic signals have autocorrelations near zero. Alpha twelve trades about {t_12:.1f} dollars per dollar long per day; that dollar-flow ratio does not mean every holding was replaced. A linear illustration multiplies mean daily dollars traded by 365 and five basis points one way: about {pc_c:.0f} percent a year for Alpha twelve and {pc_m:.0f} for the mined formula, per dollar long. These are cost illustrations under fixed conventions, without compounding, financing, borrow or market impact; they do not establish attainable execution."""
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def factory(self):
        card = firm_card(r"WorldQuant", r"Finding Alphas (2015) describes organising many small candidate signals, "
                         r"research rules and portfolio combination; it is an account of a research pipeline",
                         numbers=((r"\text{BRAIN}", r"a platform for outside researchers to write and simulate formulas"),
                                  (r"\text{scope}", r"platform scale does not establish independent ideas, valid inference "
                                                   r"or attainable returns")),
                         source=r"Finding Alphas (2015); BRAIN platform description", kind=r"Industry example", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover("WorldQuant provides a public example of distributed formula research. <bookmark mark='a'/> Finding Alphas describes organising many small candidate signals, research rules and portfolio combination. A published account of a pipeline is not independent evidence that every candidate or business unit is profitable. <bookmark mark='b'/> BRAIN gives outside researchers a platform for writing and simulating formulas. Platform access, user counts and industrial scale do not establish independent ideas, complete historical information, valid inference or attainable returns. The economic value of continued research depends on changing opportunities and costs, not a universal law that every signal must decay.") as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def crowding(self):
        cards = VGroup(
            desk_question(r"a shared grammar finds shared signals", r"many miners on the same data with the same operators "
                          r"find the same cousins: Chapter 7's correlation, across firms", width=12.4, font_size=19),
            desk_question(r"possible crowding channels", r"shared positions and funding constraints can compress returns or "
                          r"transmit selling; positions and flows are needed to identify the mechanism", width=12.4,
                          font_size=19),
            desk_question(r"research possible defences", r"new data, new horizons, and a library whose members "
                          r"are as uncorrelated as possible: AlphaAgent's originality penalty, in Chapter 6", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Consider possible crowding channels. <bookmark mark='a'/> Similar data and operators can produce related exposures, but string resemblance does not measure positions across firms. <bookmark mark='b'/> Capital flows and shared funding constraints can compress an edge or transmit selling. Those are possible mechanisms, not an inevitable sign pattern or a causal finding from our formula correlations. <bookmark mark='c'/> New information, horizons, position limits and diverse exposures may help, subject to costs and capacity. Novel syntax alone offers no protection; identifying a crowding episode requires positions, flows and funding evidence."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an alpha's IC halves every two years as others find it. Starting from 0.03, after how many years "
                       r"is it below 0.01?")
        with self.voiceover(
            "Pause and predict. An alpha's IC halves every two years as others find it. Starting from point zero three, "
            "after how many years is it below point zero one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
