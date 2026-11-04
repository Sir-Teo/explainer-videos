from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, PART, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.report(load("cva"), load("fva"), load("im"), load("saccr"), load("exposure"))
        self.module()

    def card(self):
        c = chapter_card(14, r"Rule 21: the XVA desk", r"What must every trade's price include?", part=PART)
        with self.voiceover("Chapter fourteen. The House's twenty-first rule, for its XVA desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def report(self, v, f, im, s, e):
        rows = [(r"risk-free value", r"0 (par swaps)", GREY_A),
                (r"$-$ CVA (bilateral)", rf"{-1e3 * v['cva_bilateral']:,.0f}", CVA_C),
                (r"$+$ DVA, reported, excluded from capital", rf"{1e3 * v['dva']:,.0f}", QC.GAIN),
                (r"$-$ FVA (funding cost less benefit)", rf"{-1e3 * f['FVA']:,.0f}", QC.OPTION),
                (r"$-$ KVA (cost of capital)", rf"{-1e3 * f['KVA']:,.0f}", BAD),
                (r"$-$ MVA (initial margin)", rf"{-1e3 * f['MVA']:,.0f}", QC.REALIZED)]
        hx = [-2.6, 3.2]
        tab = VGroup()
        for i, (a, b, c_) in enumerate(rows):
            y = 2.0 - 0.58 * i
            tab.add(VGroup(label(a, font_size=20, color=c_).move_to([hx[0], y, 0]),
                           MathTex(b.replace(",", "{,}"), font_size=28).move_to([hx[1], y, 0])))
        total = -v["cva_bilateral"] - f["FVA"] - f["KVA"] - f["MVA"]  # DVA reported, but not allowed to lower the price
        tot = VGroup(label(r"price to the client, \$ thousand", font_size=21).move_to([hx[0], 2.0 - 0.58 * 6.3, 0]),
                     MathTex(rf"{1e3 * total:,.0f}".replace(",", "{,}"), font_size=32).move_to([hx[1], 2.0 - 0.58 * 6.3, 0]))
        title = label(r"One trade ticket, every adjustment", font_size=28).to_edge(UP, buff=0.35)
        foot = wrapped_label(rf"the netting set of chapter 1, uncollateralised, a BBB-like client; also reported: peak PFE "
                             rf"\${max(e['net']['PFE']):.0f}m against the credit limit, SA-CCR EAD \${s['net']['EAD']:.1f}m, "
                             rf"SIMM-style IM \${im['im']:.1f}m", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Rule twenty-one is about what a price must include. One ticket for the netting set, with a client that "
            "posts no collateral. <bookmark mark='a'/> The risk-free value, zero for par swaps. Less the credit "
            "adjustment. The debit adjustment is reported, but the House does not let it reduce a price or count it "
            "as capital. Less funding, less the cost of the capital the trades consume, less the cost of initial "
            f"margin. <bookmark mark='b'/> The client pays about {abs(1e3 * total):,.0f} thousand dollars for two "
            "hundred million of swaps, before any profit. A desk that quotes the screen price is giving that away."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tot), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("credit",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{swap\_values\_hw}, \texttt{exposure\_profile}", r"values on every path; EE, ENE, PFE"),
            (r"\texttt{collateralised}", r"thresholds, transfer amounts, the margin period of risk"),
            (r"\texttt{cva}, \texttt{dva}, \texttt{fva}, \texttt{capital\_cost}", r"the adjustments, bilateral"),
            (r"\texttt{wrong\_way\_cva}", r"default tied to exposure by a copula"),
            (r"\texttt{cva\_torch}", r"CVA and every sensitivity in one backward pass"),
            (r"\texttt{simm\_like\_ir\_delta}, \texttt{sa\_ccr\_ir\_ead}", r"initial margin and capital exposure"),
            (r"\texttt{ccp\_waterfall}", r"a clearing house's default resources"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=17, color=QC.HOUSE), label(b_, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.8)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 21: every derivative is priced with its CVA, FVA, KVA and MVA against the "
                             r"counterparty's whole netting set, never alone; DVA is reported but never counted as profit "
                             r"or capital; every exposure is stressed for wrong-way risk and for a margin period twice "
                             r"the contractual one; and no client's margin is set without knowing its concentration and "
                             r"its positions at other dealers, as far as they can be learned.", 12.4, 20,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The credit desk becomes an XVA desk with these tools. <bookmark mark='a'/> Values on every path and the "
            "exposure profiles; collateral and the margin period; the adjustments; wrong-way risk; every sensitivity "
            "in one backward pass; initial margin and capital exposure; and a clearing house's waterfall. "
            "<bookmark mark='b'/> And the twenty-first rule. Every derivative is priced with its credit, funding, "
            "capital and margin adjustments, against the counterparty's whole netting set, never alone. DVA is "
            "reported, but never counted as profit or capital. Every exposure is stressed for wrong-way risk, and for "
            "a margin period twice the one in the contract. And no client's margin is set without knowing how "
            "concentrated it is, and what it holds at other dealers, as far as that can be learned."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["credit"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
