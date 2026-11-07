from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, CASH, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range, pause_card


class Industry(VoiceoverScene):
    def construct(self):
        m = load("modelrisk")
        d = load("decompose")
        env = load("envelope")
        self.card()
        self.prudent(m)
        self.dayone(d)
        self.capital()
        self.house(env)

    def card(self):
        c = chapter_card(17, r"Industry: how desks mark, reserve and report", r"What do banks and regulators actually "
                         r"require of an exotics book?", part=PART)
        with self.voiceover("Chapter seventeen. Industry: how desks mark, reserve and report exotics."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def prudent(self, m):
        M = m["models"]
        names = ["LV", "Heston", "Bates", "VG"]
        cp = np.array([M[k]["coupon"] for k in names])
        g = axes([0, 5], [0.0, float(cp.max()) * 1.2], x_length=5.2, y_length=4.2, ylabel=r"fair coupon, 4-month BTC "
                 r"autocall", xticks=[], yticks=[0, round(float(cp.max()), 2)], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=14).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        ax = g.ax
        cols = [QC.SPOT, QC.OPTION, QC.GAIN, QC.IMPLIED]
        bars = VGroup()
        for i, (v, c_) in enumerate(zip(cp, cols)):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(Rectangle(width=0.7, height=y1 - y0, stroke_width=0, fill_color=c_, fill_opacity=0.8)
                     .move_to([ax.c2p(i + 1, 0)[0], (y0 + y1) / 2, 0]))
        names_l = VGroup(*[label(n, font_size=17, color=c_).next_to(b, DOWN, buff=0.1) for n, b, c_ in zip(
            [r"local vol", r"Heston", r"Bates", r"VG"], bars, cols)])
        mark = DashedLine(ax.c2p(0.4, cp[1]), ax.c2p(4.6, cp[1]), stroke_color=WHITE, stroke_width=2)
        lo = DashedLine(ax.c2p(0.4, cp.min()), ax.c2p(4.6, cp.min()), stroke_color=BAD, stroke_width=2)
        brace = BraceBetweenPoints(ax.c2p(4.7, cp.min()), ax.c2p(4.7, cp[1]), direction=RIGHT, color=BAD)
        bl = label(r"coupon gap illustration", font_size=19, color=BAD).next_to(brace, RIGHT, buff=0.1)
        side = VGroup(
            definition_card(r"Prudent valuation (EU)", r"Delegated Regulation (EU) 2016/101: banks hold additional "
                            r"valuation adjustments (AVAs) against fair value, among them market price uncertainty, "
                            r"close-out costs and model risk (Article 11), estimated from a range of plausible valuations "
                            r"under alternative models at a 90\% level of certainty, and deducted from capital", color=BAD,
                            width=5.2, font_size=19),
        ).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Under the applicable EU prudent-valuation rules, additional valuation adjustments address uncertainty including model risk. Article eleven of Regulation 2016/101 uses plausible alternative valuations and a ninety-percent exit-value certainty target when a range can be formed. Market-input calibration uncertainty is addressed separately. <bookmark mark='a'/> Our coupon bars only illustrate sensitivity. Before calculating an adjustment, compare the same fixed contract's monetary value under justified alternatives; different fair coupons are different contracts, and our approximate calibrations are unequal. A simple highest-minus-lowest coupon gap is not a regulatory AVA or a statistical ninety-percent quantile. The example motivates review; the actual adjustment depends on the applicable methodology and valuation evidence."
        ) as vo:
            self.play(FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(names_l))
            self.play(Create(mark), Create(lo), GrowFromCenter(brace), FadeIn(bl))
        self.wait(0.4)
        self.clear_scene()

    def dayone(self, d):
        B = d["B"]
        margin = 0.03 * B
        g = axes([0, 2], [0, margin * 1.4], x_length=6.0, y_length=3.6, xlabel=r"years since the sale",
                 ylabel=r"margin recognised, per 1 of notes", xticks=[0, 1, 2], yticks=[0, round(margin, 3)],
                 font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        ax = g.ax
        t = np.linspace(0, 2, 50)
        a = Line(ax.c2p(0, margin), ax.c2p(2, margin), stroke_color=BAD, stroke_width=3)
        b = curve(ax, t, margin * t / 2, GOOD, stroke_width=3)
        leg = legend([(BAD, r"booked on day one (fair value evidenced by observable inputs)"),
                      (GOOD, r"deferred; illustrative release as valuation factors change")], font_size=16)
        leg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        side = definition_card(r"Day-one profit (IFRS 9 B5.1.2A)", 'initial price minus fair value: immediate recognition requires an active-market quote for an identical instrument, or a valuation using only observable market data. Otherwise defer and release as relevant valuation factors, including time, change; the straight line is schematic',
                               color=GOOD, width=5.6, font_size=19).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"Reducing the coupon by three percentage points gives an initial model-value difference of {margin:.3f} per note in our calculation, before costs and reserves. It is not guaranteed realized profit. <bookmark mark='a'/> IFRS 9's day-one rule distinguishes fair value evidenced by an active-market quote for an identical instrument, or a valuation using only observable market data, from other valuations. In the latter case the initial difference is deferred and recognized as relevant valuation factors, including time, change. Whether a particular note qualifies depends on its evidence, not simply its snowball label. The green straight line is an illustrative release path, not a prescribed accounting schedule."
        ) as vo:
            self.play(FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(leg), Create(a), Create(b))
        self.wait(0.4)
        self.clear_scene()

    def capital(self):
        cards = VGroup(
            definition_card(r"Capital: FRTB", r"Basel's standardised approach adds a residual risk add-on (MAR23) for "
                            r"instruments whose risk its sensitivities miss: 1\% of gross notional for exotic underlyings, "
                            r"0.1\% for other residual risks such as path-dependent payoffs. Under internal models, "
                            r"autocallables must pass P\&L attribution: Zeron, Wu and Ruiz (2023) cut the cost of the "
                            r"expected-shortfall runs by about 90\% with Chebyshev proxies", color=IV, width=6.2,
                            font_size=19),
            definition_card(r"Conduct", r"EU PRIIPs (Regulation 1286/2014): a key information document with risk class "
                            r"and performance scenarios for in-scope packaged retail investment and insurance products. FINRA Regulatory Notice 12-03: "
                            r"heightened supervision of complex products. Korea's FSS: compensation in 2024, penalty "
                            r"notices in 2025 (chapter 10)", color=OPT, width=6.2, font_size=19),
            definition_card(r"Model validation", r"the Federal Reserve's model-risk guidance (SR 11-7, 2011, superseded "
                            r"by SR 26-2 in April 2026): independent validation, limits on model use, ongoing "
                            r"monitoring. Natixis's 2018 loss (chapter 10) is the case of a hedging model that failed "
                            r"in live markets", color=GOOD, width=6.2, font_size=19),
        )
        cards[:2].arrange(RIGHT, buff=0.3, aligned_edge=UP)
        VGroup(cards[:2], cards[2]).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        if VGroup(*cards).height > 7.2:
            VGroup(*cards).scale_to_fit_height(7.2)
        pp = pause_card(r"Why can a bank not book a structured note's margin on day one?", width=5.0).to_corner(UR, buff=0.2)
        with self.voiceover(
            "Capital rules add another layer. Basel's standardized residual-risk add-on uses one percent of gross notional for exotic underlyings and a tenth of a percent for other in-scope residual risks, subject to its definitions, exemptions and local implementation. Internal-model desks also face attribution requirements; Zeron and co-authors' computational benchmark is one tested approach. <bookmark mark='a'/> Conduct requirements have their own scope: EU PRIIPs information documents, FINRA's dated complex-products guidance, and Korea's compensation and enforcement episodes. <bookmark mark='b'/> Model governance is separate again. The US agencies issued revised guidance in April 2026, SR 26-2, replacing SR 11-7 and emphasizing a tailored risk-based approach. Natixis's public 2018 announcement is a reminder that valuation, hedging and model use each need validation; it does not establish that the original pricing model was correct."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def house(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.6).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{down\_out\_call}, \texttt{bgk\_barrier}, \texttt{static\_dic\_hedge}", r"barriers, watched and hedged as the term sheet says"),
            (r"\texttt{digital\_call}, \texttt{call\_spread\_digital}, \texttt{one\_touch}", r"digitals, touches, and the hedge the desk can run"),
            (r"\texttt{geometric\_asian\_call}, \texttt{lookback\_floating\_call}", r"closed forms and control variates"),
            (r"\texttt{snowball\_AB}, \texttt{autocall\_on\_paths}", r"the snowball as a linear solve, under any model"),
            (r"\texttt{worst\_of\_autocall\_AB}, \texttt{margrabe}, \texttt{cliquet\_bs}", r"correlation and forward volatility"),
            (r"\texttt{uvm\_solve}, \texttt{uvm\_lagrangian}, \texttt{kl\_worst\_case}", r"the price of not knowing the model"),
            (r"\texttt{digital\_delta\_estimators}", r"Greeks for payoffs with jumps (chapter 18)"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 15: before a note is sold, the desk prices it under at least two models, holds a reserve "
                             r"for the gap, and simulates its hedge through the worst path on record for the underlying, "
                             r"including what the hedge must trade on the barrier day. The existing numerical regression suite supplies "
                             rf"checks. The trial counter still reads {env['trials']}.", 12.4, 21, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"The House now has an exotics library with numerical regression checks, not a complete independent validation report for every function. <bookmark mark='a'/> Its tools cover specified barrier monitoring, digitals, averages, affine coupon solves, dependence and uncertainty. The contract, pricing model and numerical error must accompany each use. <bookmark mark='b'/> Rule fifteen is the project's proposed discipline: compare at least two justified models, state a reserve policy, and simulate the hedge on stressed historical paths, including barrier days. One historical worst path is not a guarantee against future losses. No new market strategy trial or sealed holdout was opened; the cumulative part counter remains {env['trials']}. Next, selected research."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
