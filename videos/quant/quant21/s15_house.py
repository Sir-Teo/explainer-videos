from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, PART, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.report(load("cva"), load("fva"), load("im"), load("saccr"), load("exposure"))
        self.night()
        self.module()
        self.test()

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
            f"One illustrative House ticket, under an explicit internal charging policy. <bookmark mark='a'/> Use bilateral CVA for the netting set, report DVA separately, and do not let the own-credit gain reduce this internal charge. Add the assumed funding, capital and initial-margin costs. These conventions are a teaching policy, not an accounting mandate or a complete replication model. <bookmark mark='b'/> The resulting internal charge is {abs(1e3 * total):,.0f} thousand on two hundred million of swaps. A real quote needs incremental netting-set effects, an agreed cost policy and checks against overlap or double counting."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tot), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def night(self):
        steps = [(r"scenarios", r"rates, credit and FX on every path and date (chapter 1)"),
                 (r"values", r"every trade on every path: formulas, or a learned network (chapter 7)"),
                 (r"netting and collateral", r"by legal agreement: thresholds, transfer amounts, margin period (chapters 1--2)"),
                 (r"adjustments", r"CVA, DVA, FVA, KVA, MVA per counterparty, and per new trade as an increment (3--5)"),
                 (r"sensitivities", r"one backward pass for every curve node and spread (chapter 6)"),
                 (r"hedges and limits", r"CDS and swaps against the CVA's risks; PFE against each credit line; "
                                        r"wrong-way and margin-period stresses (Rule 21)")]
        boxes = VGroup()
        for i, (h_, d_) in enumerate(steps):
            b_ = RoundedRectangle(corner_radius=0.12, width=3.9, height=1.25, stroke_color=CVA_C if i == 3 else GREY_B,
                                  stroke_width=2, fill_opacity=0)
            t_ = VGroup(label(h_, font_size=20), wrapped_label(d_, 3.6, 14, GREY_A)).arrange(DOWN, buff=0.08).move_to(b_)
            boxes.add(VGroup(b_, t_))
        boxes.arrange_in_grid(rows=2, cols=3, buff=(0.45, 0.7)).move_to(DOWN * 0.2)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, color=GREY_B, stroke_width=3)
                          for i in (0, 1, 3, 4)],
                        Arrow(boxes[2].get_bottom(), boxes[5].get_top(), buff=0.06, color=GREY_B, stroke_width=3))
        # the grid reads 0 1 2 / 3 4 5: route 2 -> 3 as the turn of the line
        arrows[-1].become(CurvedArrow(boxes[2].get_bottom() + DOWN * 0.05, boxes[3].get_top() + UP * 0.05, angle=-0.6,
                                      color=GREY_B, stroke_width=3))
        title = label(r"The XVA desk's night", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"the same machinery prices a client's new trade during the day: rerun only the increment "
                             r"its netting set changes", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Behind the ticket is a process that runs every night. <bookmark mark='a'/> Simulate the markets, on "
            "thousands of paths and dates. Value every trade on every path, by formula where one exists and by a "
            "learned approximation where it does not. Net and collateralise by legal agreement. "
            "<bookmark mark='b'/> Compute every adjustment for every counterparty, and their sensitivities in one "
            "backward pass. Then hedge the credit and rate risks of the CVA, check potential exposure against each "
            "credit line, and run the stresses the rule requires. <bookmark mark='c'/> During the day, the same "
            "machinery quotes a new trade by rerunning only the netting set it changes."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(boxes[0]), GrowArrow(arrows[0]), FadeIn(boxes[1]), GrowArrow(arrows[1]),
                                  FadeIn(boxes[2]), lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(Create(arrows[4]))
            self.play(LaggedStart(FadeIn(boxes[3]), GrowArrow(arrows[2]), FadeIn(boxes[4]), GrowArrow(arrows[3]),
                                  FadeIn(boxes[5]), lag_ratio=0.4, run_time=3))
            vo.wait_until("c")
            self.play(FadeIn(foot))
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


    def test(self):
        cards = VGroup(
            desk_question(r"Archegos, 2021", r"the rule asks for the client's concentration and its positions at other "
                          r"dealers before margin is set; at a few days' volume per name, the liquidation-horizon margin "
                          r"of chapter 13 is several times 20\%. The House would have refused the size, or charged for it",
                          width=12.0, font_size=20),
            desk_question(r"a power trader at a clearing house, 2018", r"a member's one-way bet on a spread is a "
                          r"concentration the CCP's margin model did not price; the House, as a member, stresses its "
                          r"default-fund share for the largest such positions it can learn of", width=12.0, font_size=20),
            desk_question(r"nickel, 2022", r"a margin period twice the contract's, and wrong-way stress on the "
                          r"collateral, would have shown the short side's calls as unpayable in a day; the House limits "
                          r"exposure to any client whose calls it could not meet in cash", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Would the rule have helped in this part's three cases? <bookmark mark='a'/> For Archegos, it asks what "
            "the client holds elsewhere and how concentrated it is before setting margin. At several days' volume per "
            "name, the margin of chapter thirteen is several times twenty percent: the House would have refused the "
            "size, or charged for it. <bookmark mark='b'/> For the power trader, the House as a clearing member "
            "stresses its share of the default fund against the largest one-way positions it can learn of. "
            "<bookmark mark='c'/> And for nickel, a doubled margin period and stressed collateral show calls that "
            "cannot be paid in a day. No rule prevents every loss. This one asks the questions whose answers were "
            "available, and ignored."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
