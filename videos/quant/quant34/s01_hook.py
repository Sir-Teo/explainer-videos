from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import firm as F
from videos.quant.quant34.common import (BAD, FIRM_C, GOOD, PEAK_C, PLAT_C, PM_C, PNL_C, PART, STOP_C, era_strip,
                                         illustration, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.stop()
        self.claims(load("virtu"), load("theory"), load("platform"))
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Inside a Quant Firm")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        self.add(card, disc)
        with self.voiceover(
            "Part thirty-four. Inside a quant firm: how the firms that run these strategies are built, paid, governed "
            "and policed, and the arithmetic that decides how long a trader keeps their seat."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def stop(self):
        rng = np.random.default_rng(34)
        dt = 1 / 252
        T = 252 * 2
        x = np.cumsum(1.0 * 0.10 * dt + 0.10 * np.sqrt(dt) * rng.standard_normal(T))
        pk = np.maximum.accumulate(np.r_[0.0, x])[1:]
        hit = np.argmax(pk - x >= 0.05) if np.any(pk - x >= 0.05) else T - 1
        t = np.arange(T) / 252
        y0 = float(np.floor(min(x.min(), -0.06) * 100 / 5) * 5)
        y1 = float(np.ceil(max(x.max(), 0.06) * 100 / 5) * 5)
        g = axes([0, 2], [y0, y1], x_length=8.0, y_length=4.4, xlabel=r"years", ylabel=r"the manager's P\&L, \% of capital",
                 xticks=[0, 1, 2], yticks=[y0, 0, y1], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, t[:hit + 1], 100 * x[:hit + 1], PNL_C, stroke_width=3)
        c2 = curve(ax, t[:hit + 1], 100 * pk[:hit + 1], PEAK_C, stroke_width=2)
        c3 = curve(ax, t[:hit + 1], 100 * (pk[:hit + 1] - 0.05), STOP_C, stroke_width=2)
        dot = Dot(ax.c2p(t[hit], 100 * x[hit]), radius=0.09, color=STOP_C)
        leg = legend([(PNL_C, r"P\&L"), (PEAK_C, r"running peak"), (STOP_C, r"peak less 5\%: the stop")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        ill = illustration(r"illustration: a simulated manager with a true Sharpe ratio of 1 at 10\% volatility")
        et = F.stop_time_sharpe(1.0, 0.5)
        months = 12 * et
        self.add(g, c1, c2, c3, leg, ill)
        with self.voiceover(
            f"""Consider a stipulated manager with constant arithmetic Brownian profit, known annual Sharpe one and annual volatility ten percent of initial capital. The running maximum includes zero. A continuously monitored drawdown of five percent stops the full book. <bookmark mark='a'/> This fixed-seed daily path illustrates the rule, with discrete overshoot. <bookmark mark='b'/> Under the continuous model, the exact expected stopping time is {months:.1f} months. That is a conditional mathematical lifetime, not a forecast for an actual manager or a guarantee about a platform's contract."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c2), Create(c3), Create(c1), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=1.5))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, v, t, p):
        S1 = t["grid"][t["S"].index(1.0)]
        on, off = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"], p["5% vol, no stops | skill sd 0.5"]
        s_on, s_off = on["investor_sharpe"], off["investor_sharpe"]
        cards = VGroup(
            desk_question(r"one losing day in 1{,}238", rf"Virtu's 2014 S-1: if daily P\&L were normal, a daily Sharpe "
                          rf"ratio of {v['normal']:.2f}, about {v['annual']:.0f} annualized under iid assumptions; one possible model is "
                          r"aggregation of many independent small trades; the count alone cannot establish it", width=12.4, font_size=26),
            desk_question(r"a stop half a volatility deep", rf"a Sharpe-1 manager hits it in {12 * S1[0]:.1f} months on "
                          rf"average in the known-parameter Brownian model; one volatility deep, {S1[2]:.1f} years; at large positive $S\delta$, the leading term involves "
                          r"$e^{2S\delta}$", width=12.4, font_size=26),
            desk_question(r"why firms stop managers anyway", r"a chosen stopping rule can inform a specified skill test and tends to stop "
                          rf"lower-drift processes sooner in the model; the stipulated platform's investor ratio goes "
                          rf"from {s_off:.2f} to {s_on:.2f}", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            f"""Three distinctions guide this lesson. <bookmark mark='a'/> Virtu's 2014 filing reported one losing day in twelve hundred and thirty-eight. A Gaussian daily model maps that frequency to ratio {v['normal']:.2f}; square-root annualization additionally assumes independent, stable daily variance. A loss count alone does not identify trading skill. <bookmark mark='b'/> For a known Brownian Sharpe-one process, these two continuous stop depths give means {12*S1[0]:.1f} months and {S1[2]:.1f} years. <bookmark mark='c'/> The chosen platform simulation gives investor ratios {s_off:.2f} without stops and {s_on:.2f} with them. Selection, exposure, free replacement and payout accounting all affect that comparison."""
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        self.add(smap)
        with self.voiceover(
            "Where this sits. Parts thirty to thirty-three built portfolios, risk models and strategies. This part steps "
            "back to the firm that runs them: its business model, its capital, its risk limits, its technology, its "
            "compliance desk, and the people it hires. It uses Part eight's drawdown control, Part twenty-six's "
            "multiple testing and Part thirty-one's capacity."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1969, r"Princeton/Newport", I), (1982, r"Renaissance", I), (1988, r"D. E. Shaw; Medallion", I),
                   (1989, r"Millennium", I), (1990, r"Citadel", I), (1998, r"AQR", I), (2000, r"Jane Street", I),
                   (2001, r"Two Sigma", I), (2008, r"Virtu", I), (2012, r"Knight's 45 minutes", BAD),
                   (2015, r"XTX; Sarao charged", I), (2020, r"a \$920m spoofing case", BAD)]
        strip = era_strip(entries, y0=1965, y1=2026, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Fifty years of quant firms", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 9), (9, 12)]
        self.add(head, strip[0], strip[1], strip.items[0])
        with self.voiceover(
            "The firms, by founding date, from the public record. Princeton/Newport in 1969; Renaissance in 1982; D. E. "
            "Shaw in 1988; Millennium in 1989. <bookmark mark='a'/> Citadel in 1990; AQR in 1998; Jane Street in 2000; "
            "Two Sigma in 2001; Virtu in 2008. <bookmark mark='b'/> And the firm's other history: Knight Capital's "
            "forty-five minutes in 2012, the spoofing cases, and the rules that followed."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Six business models, and how each is paid",
            r"What firms have disclosed, and what one statistic implies",
            r"The pod model: capital, stops, payouts; a platform simulated",
            r"From idea to capital; risk at the firm level; technology",
            r"Surveillance and the cases; the interview",
            r"Founding stories, as told in public; drawdown stops on real premia",
            r"For the researcher: how long a seat lasts, exactly",
        ], color=QC.IDEA)
        self.add(card.head, card.rows[0])
        with self.voiceover(
            "The plan: six business models; what firms have disclosed and what it implies; the pod model, simulated; "
            "how an idea becomes capital; risk at the level of the firm; technology; surveillance and the cases; the "
            "interview; the founding stories, as told in public; whether drawdown stops help on real premia; and an "
            "exact formula for how long a manager keeps their seat."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("compliance",))
        self.add(chart)
        with self.voiceover(
            'This part proposes a firm-level checklist for the educational House: independent limits, authority to stop, records and review. The chart describes responsibilities; it does not establish that a trading or surveillance system has been implemented or that a strategy is approved.'
        ):
            self.play(FadeIn(chart))
            self.wait(0.4)
        self.wait(0.3)
        self.clear_scene()
