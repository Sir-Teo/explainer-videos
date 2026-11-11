from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, FWD, GOOD, PART, ZERO, ask, fit_right, illustration, load


class Multicurve(VoiceoverScene):
    def construct(self):
        m = load("multicurve")
        self.card()
        self.ted(m)
        self.curves()
        self.numbers(m)
        self.collateral()

    def card(self):
        c = chapter_card(10, r"Multi-curve and collateral", r"Why did one curve become many?", lit=(2008,), part=PART)
        with self.voiceover("Chapter ten. One curve becomes many: what 2008 did to the arithmetic of swaps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ted(self, m):
        t, v = np.asarray(m["t"]), np.asarray(m["ted"])
        g = axes([1986, 2022.5], [0, 5], x_length=8.6, y_length=4.4, xlabel=r"year",
                 ylabel=r"3-month LIBOR minus 3-month bill, \%", xticks=[1990, 2000, 2010, 2020], yticks=[0, 1, 2, 3, 4, 5],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, BAD, stroke_width=2.2)
        pk = m["peak"]
        pd = pk["date"]
        pt = Dot(ax.c2p(pd // 10000 + (pd // 100 % 100 - 1) / 12, pk["pct"]), color=BAD, radius=0.08)
        s20 = (t > 2020) & (t < 2020.5)
        mar = float(v[s20].max())
        side = VGroup(
            MathTex(rf"\text{{peak}} = {pk['pct']:.2f}\%", font_size=30, color=BAD),
            label(rf"{pd % 100} October {pd // 10000}", font_size=19, color=GREY_A),
            MathTex(rf"\text{{2000--mid 2007 average}} = {m['pre2007']:.2f}\%", font_size=24),
            wrapped_label(r"the TED spread: what banks charged each other for unsecured three-month money, over what the "
                          r"US government paid. Before the crisis, a rounding error; in it, a measure of fear", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"The TED spread compares three-month unsecured dollar bank funding with a three-month Treasury bill. It includes bank credit and funding liquidity, as well as the bill's safety, liquidity and quotation conventions; it is not a pure default probability. Its pre-2007 average in this saved sample is {m['pre2007']:.2f} percent. <bookmark mark='a'/> It reached {pk['pct']:.2f} percent on October tenth, 2008. The March-2020 episode reached {mar:.2f} percent in this dataset. Central-bank facilities and changing market conditions coincided with the subsequent decline; this chart cannot isolate their causal contributions. These episodes motivate pricing index and collateral exposures separately, rather than treating unsecured bank rates as a universal risk-free discount curve."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[2]), FadeIn(side[3]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(pt, scale=1.5), FadeIn(side[0]), FadeIn(side[1]))
        self.add(illustration(r"FRED: TEDRATE (discontinued January 2022)"))
        self.wait(0.4)
        self.clear_scene()

    def curves(self):
        rows = [cmath(r"F^{\text{3m}}(t; T)", r"=", r"\frac{1}{\delta}\Big(\frac{P(t, T)}{P(t, T{+}\delta)} - 1\Big)",
                      font_size=38, colors={r"F^{\text{3m}}(t; T)": FWD}),
                cmath(r"F^{\text{3m}}", r"\ne", r"F^{\text{6m}}\ \ne\ F^{\text{OIS}}", font_size=40,
                      colors={r"F^{\text{3m}}": FWD}),
                cmath(r"S", r"=", r"\frac{\sum_i \delta\,P^{\text{OIS}}(0, T_{i+1})\,F^{\text{3m}}_i}"
                      r"{\sum_i \delta\,P^{\text{OIS}}(0, T_{i+1})}", font_size=38, colors={r"S": ZERO})]
        whys = [why(r"before 2008, one curve: the forward LIBOR rate followed from the same discount factors used to "
                    r"value every cash flow"),
                why(r"after, each tenor carries its own bank credit and liquidity: 3-month, 6-month and overnight "
                    r"forwards each need a curve of their own, and their gaps (basis swaps) trade"),
                why(r"so a swap is valued with two curves: one to project the floating rate, another, the overnight "
                    r"(OIS) curve, to discount every cash flow")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "The single-curve approximation used the same discount factors to infer forward rates and value cash flows. It was a convention and approximation, not an identity that a crisis could break. <bookmark mark='a'/> Bank credit, liquidity, tenor and funding differences became too large to ignore. A projection curve can encode each tenor's forward quotes, but its pseudo-discount factors need not be prices of tradable zero-coupon bonds. <bookmark mark='b'/> For a standard fully collateralized swap, project each floating coupon on the relevant index curve and discount using the collateral-consistent curve. Different accrual conventions also mean that three-month, six-month and overnight rates are not directly interchangeable even without a credit crisis."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def numbers(self, m):
        bp = m["basis"] * 1e4
        cols = VGroup(
            VGroup(label(r"one curve", font_size=26, color=BAD),
                   label(rf"discount on LIBOR = OIS + {bp:.0f} bp", font_size=19, color=GREY_A),
                   MathTex(rf"\text{{par rate}} = {100 * m['fixed_one']:.3f}\%", font_size=30),
                   MathTex(rf"\text{{receive }} {100 * m['K_off']:.1f}\%\text{{: }} {m['off_one']:.2f}", font_size=30)
                   ).arrange(DOWN, buff=0.35),
            VGroup(label(r"two curves", font_size=26, color=GOOD),
                   label(rf"project LIBOR, discount on OIS", font_size=19, color=GREY_A),
                   MathTex(rf"\text{{par rate}} = {100 * m['fixed_two']:.3f}\%", font_size=30),
                   MathTex(rf"\text{{receive }} {100 * m['K_off']:.1f}\%\text{{: }} {m['off_two']:.2f}", font_size=30)
                   ).arrange(DOWN, buff=0.35),
        ).arrange(RIGHT, buff=1.6).shift(UP * 0.6)
        diff = abs(m["off_two"] - m["off_one"])
        head = label(rf"A 5-year swap against 3-month LIBOR, the Fed's curve of 31 December 2025, a {bp:.0f} bp basis; "
                     r"values per 100 of notional", font_size=21).to_edge(UP, buff=0.5)
        foot = wrapped_label(
            rf"at the money the two methods agree to {1e4 * abs(m['fixed_two'] - m['fixed_one']):.2f} bp. Off the money "
            rf"they differ by {diff:.2f} per 100: {diff * 1e7:,.0f} dollars on a billion of notional, on every old swap "
            r"in a dealer's book. In 2010 LCH moved its cleared interest rate swaps to OIS discounting", 12.0, 20,
            GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How much does the second curve matter? Value a five-year swap both ways, with a quarter-point gap between "
            "LIBOR and the overnight rate. <bookmark mark='a'/> At the money, almost not at all: the par rates agree "
            f"to {1e4 * abs(m['fixed_two'] - m['fixed_one']):.2f} of a basis point, because the projection does the "
            "work and the discounting only reweights it. <bookmark mark='b'/> But an old swap, struck when rates were "
            f"low, receiving one and a half percent, changes value by {diff:.2f} per hundred between the two "
            f"curves: {diff * 1e7:,.0f} dollars on a billion. Across a dealer's trillions, and every swap that clears, "
            "that was a revaluation large enough to change books and margin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0][:2]), FadeIn(cols[1][:2]))
            vo.wait_until("a")
            self.play(FadeIn(cols[0][2]), FadeIn(cols[1][2]))
            vo.wait_until("b")
            self.play(FadeIn(cols[0][3]), FadeIn(cols[1][3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def collateral(self):
        rows = [cmath(r"V_0", r"=", r"\mathbb{E}^{\mathbb{Q}^{c}}\Big[e^{-\int_0^T c_s\,ds}\,V_T\Big]", font_size=42,
                      colors={r"V_0": ZERO}),
                cmath(r"\text{CVA, FVA, ...}", r"=", r"\text{the adjustments for what collateral does not cover}",
                      font_size=34, colors={r"\text{CVA, FVA, ...}": BAD})]
        whys = [why(r"Piterbarg (2010): a fully collateralised trade grows at the rate paid on its collateral, $c$, so "
                    r"that is its discount rate; for cash collateral under a standard agreement, the overnight rate"),
                why(r"uncollateralised trades carry the counterparty's default risk and the dealer's funding cost: the "
                    r"valuation adjustments, priced on desks of their own (Parts 20 and 21)")]
        step = ladder(self, rows, whys, keep=2, top=2.3, x=-0.8, buff=0.8, edge=6.9)
        sofr = wrapped_label(r"October 2020: LCH and CME switch the discounting of cleared USD swaps from Fed funds to "
                             r"SOFR. A standard USD SOFR OIS with SOFR collateral may use one curve; this does not merge "
                             r"all USD tenor, collateral-currency or funding curves", 12.0, 19, GOOD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For a perfectly cash-collateralized idealization, with continuous margining, symmetric collateral remuneration, and the relevant replication assumptions, use the collateral rate to discount under a consistent pricing measure. Collateral does not make every contract risk-free in practice: thresholds, margin periods, default and funding terms matter. <bookmark mark='a'/> CVA, funding and other adjustments address specific remaining risks; they require a consistent framework so the same effect is not counted twice. <bookmark mark='b'/> In October 2020, major clearing houses switched cleared dollar-swap discounting and price-alignment interest to SOFR. A plain SOFR overnight-indexed swap with SOFR cash collateral can use a common projection and discount curve. This did not merge every dollar curve: term-rate conventions, tenor bases, cross-currency collateral and funding can still require separate treatment. Ask which index is paid and which rate remunerates the collateral."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(sofr))
        q = ask(r"a swap is collateralised in euros but pays dollars. Which curve discounts it, and why might that "
                r"differ from the dollar OIS curve?")
        with self.voiceover("A dollar swap collateralised in euros: which curve discounts it, and why might that differ "
                            "from the dollar overnight curve?"):
            self.play(FadeOut(sofr), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
