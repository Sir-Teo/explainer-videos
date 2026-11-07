from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load


class Industry(VoiceoverScene):
    def construct(self):
        self.card()
        self.exchanges()
        self.dealers()
        self.builder()

    def card(self):
        c = chapter_card(18, r"Who builds surfaces, and who sells them", r"How do the firms that live on this do it?",
                         part=PART)
        with self.voiceover("Chapter eighteen. Who builds surfaces, and who sells them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def exchanges(self):
        steps = [(1993, r"Cboe publishes the VIX: an average of at-the-money implied vols on S\&P 100 options "
                        r"(Robert Whaley's design)"),
                 (2003, r"September: the VIX becomes a strip of S\&P 500 options, designed with Goldman Sachs"),
                 (2004, r"March: VIX futures on the Cboe Futures Exchange; options on the VIX follow in February 2006"),
                 (2021, 'March: Deribit launches variance-based DVOL, with its own filters; DVOL futures follow in 2023'),
                 (2023, r"April: Cboe's one-day VIX (VIX1D), for same-day options"),
                 (2024, r"November: options on BlackRock's bitcoin ETF (IBIT) list on Nasdaq; about \$1.9bn notional "
                        r"traded on the first day, as reported by Nasdaq"),
                 (2025, '14 August: Coinbase closes Deribit acquisition; filing consideration about \\$4.3bn (earlier announcement: \\$2.9bn)')]
        rows = VGroup()
        for y, t in steps:
            rows.add(VGroup(label(str(y), font_size=24, color=QC.FIRM), wrapped_label(t, 10.6, 20, GREY_A)
                            ).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN).shift(DOWN * 0.2)
        head = label(r"Exchanges compute surfaces as indices", font_size=30).to_edge(UP, buff=0.35)
        q = label(r"pause and predict: why can an exchange publish a VIX for bitcoin, but not a true variance-swap rate?",
                  font_size=19, color=QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            """An index is the public face of the surface. Cboe's original VIX used S&P 100 options; the 2003 redesign uses an SPX option strip. Futures followed in 2004, options in 2006. <bookmark mark='a'/> Deribit launched DVOL in March 2021 and its futures in 2023. Cboe introduced VIX1D in 2023. IBIT options began trading in November 2024. Coinbase closed its Deribit acquisition on August fourteenth, 2025. Its filing records total consideration of about four point three billion dollars; the earlier two point nine billion announcement valued the stock component at a different date. <bookmark mark='b'/> An exchange can publish a precisely specified truncated index. Inferring a continuum-strike variance price still needs assumptions about unquoted tails and the target contract's sampling, jump and carry conventions."""
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows[:3]], lag_ratio=0.4, run_time=3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[3:]], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    def dealers(self):
        cards = VGroup(
            firm_card(r"Goldman Sachs Quantitative Strategies",
                      r"Derman and Kani's implied tree (1994); Derman's ``Regimes of volatility'' (1999); Demeterfi, Derman, "
                      r"Kamal and Zou's variance-swap note (1999), the desk's manual for replication.", width=6.3,
                      font_size=20),
            firm_card(r"Paribas; Merrill Lynch",
                      r"Bruno Dupire's local volatility (1994), written at Paribas. SVI, devised at Merrill Lynch in 1999 "
                      r"and made public by Jim Gatheral in 2004.", width=6.3, font_size=20),
            firm_card(r"Danske Bank",
                      r"Andreasen and Huge's ``Volatility interpolation'' (\emph{Risk}, 2011): an arbitrage-free surface "
                      r"from sparse quotes by one implicit finite-difference step per expiry, fast enough for real time.",
                      width=6.3, font_size=20),
            firm_card(r"What a bank's builder adds to ours",
                      r"dividends and rates in the forward; marking through the day as quotes arrive; many underlyings "
                      r"sharing one model; stress surfaces for risk; a record of every fit, for the auditors.", width=6.3,
                      font_size=20),
        )
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "Behind the indices, the field was written by dealers' quants, and much of it in published research. At "
            "Goldman Sachs' quantitative strategies group: Derman and Kani's implied tree, Derman's regimes of "
            "volatility, and the variance-swap note of Demeterfi, Derman, Kamal and Zou, which became the desk's "
            "manual. <bookmark mark='a'/> At Paribas, Bruno Dupire's local volatility. At Merrill Lynch, SVI, used "
            "internally from 1999 and made public by Gatheral in 2004. <bookmark mark='b'/> At Danske Bank, Jesper "
            "Andreasen and Brian Huge's volatility interpolation, which builds an arbitrage-free surface from sparse "
            "quotes with one implicit finite-difference step per expiry, fast enough to run as quotes arrive. "
            "<bookmark mark='c'/> And what does a bank's surface builder do that ours does not? Dividends and rates in "
            "the forward, marking through the day, many underlyings in one model, stressed surfaces for risk, and a "
            "record of every fit for the auditors."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
            vo.wait_until("c")
            self.play(FadeIn(cards[3]))
        self.wait(0.5)
        self.clear_scene()

    def builder(self):
        chart = house_chart(PART, lit=("vol",)).scale(0.55).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{fit\_svi}, \texttt{svi\_jw}", r"one expiry, in raw and jump-wings form (Chapter 4)"),
            (r"\texttt{fit\_ssvi}, \texttt{ssvi\_butterfly\_bound}", r"the whole surface, and where its proof holds (5)"),
            (r"\texttt{g\_function}, \texttt{lee\_moment}", r"butterflies and wings (3)"),
            (r"\texttt{dupire\_local\_var}, \texttt{derman\_kani}", r"local volatility, as a formula and as a tree (6)"),
            (r"\texttt{strip\_replication}, \texttt{vix}, \texttt{rn\_moments}", r"variance, indices, moments (9--13)"),
            (r"\texttt{vx\_index}, \texttt{inverse\_note}", r"futures indices and the notes built on them (14)"),
            (r"\texttt{train\_surface\_net}", r"a surface learned without arbitrage (17)"),
        ]
        names = VGroup(*[label(a, font_size=19, color=QC.HOUSE) for a, _ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        x1 = names.get_right()[0] + 0.4
        tab = VGroup()
        for nm, (_, b) in zip(names, rows):  # two aligned columns: names flush left, descriptions flush left after them
            d = label(b, font_size=18, color=GREY_A)
            d.move_to([x1 + d.width / 2, nm.get_y(), 0])
            tab.add(VGroup(nm, d))
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        tab.set_x(0)
        with self.voiceover(
            """Here is the House's surface builder: SVI and its trader's coordinates; SSVI and the maturity domain of its sufficient conditions; sampled butterfly and wing diagnostics; local volatility as a formula and a tree; strips for variance, indices and moments; a futures-index and daily-reset-note illustration; and neural fits with grid penalties and explicit remaining violations. Tests check these implementations. They do not certify every fitted surface, every extrapolated strike or every future market scenario. Last, the frontier."""
        ) as vo:
            self.play(FadeIn(chart))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
        self.wait(0.4)
        self.clear_scene()
