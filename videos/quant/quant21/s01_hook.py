from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, PART, era_strip, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.archegos()
        self.history()
        self.objectives()
        self.scope()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The other side of every trade")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-one. Counterparty risk, valuation adjustments and clearing. Every derivative is a promise "
            "between two parties, and either of them can fail before it is kept."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def archegos(self):
        rows = [("Credit Suisse", 5.5), ("Nomura", 2.9), ("Morgan Stanley", 0.9), ("UBS", 0.9), ("MUFG", 0.3)]
        g = axes([0, 6], [0.4, 5.6], x_length=6.4, y_length=4.0, xlabel=r"reported loss, \$ billion", ylabel=r"",
                 xticks=[0, 2, 4, 6], yticks=[], font_size=14).to_edge(LEFT, buff=1.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (n_, v) in enumerate(rows):
            y = 5 - i
            b_ = Rectangle(width=ax.c2p(v, 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=BAD,
                           fill_opacity=0.8).move_to([(ax.c2p(0, 0)[0] + ax.c2p(v, 0)[0]) / 2, ax.c2p(0, y)[1], 0])
            bars.add(VGroup(b_, label(n_, font_size=18).next_to(b_, LEFT, buff=0.2).align_to(
                [ax.c2p(0, 0)[0] - 0.2, 0, 0], RIGHT), MathTex(rf"{v:.1f}", font_size=24).next_to(b_, RIGHT, buff=0.1)))
        for b_ in bars:
            b_[1].next_to([ax.c2p(0, 0)[0] - 0.15, b_[0].get_y(), 0], LEFT, buff=0)
        cc = crisis_card(r"26 March 2021", r"Archegos Capital Management",
                         r"a family office that held concentrated stock positions through total return swaps with "
                         r"several prime brokers, each seeing only its own part; when the stocks fell, it could not meet "
                         r"margin calls, and the banks sold the collateral in a race",
                         stats=[(r"> \$10\,\text{bn}", r"banks' combined losses (public reports)")], width=4.6,
                         font_size=18).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "In March 2021, a family office in New York, Archegos Capital Management, failed to meet its margin "
            "calls. It held enormous positions in a handful of stocks, not directly but through total return swaps "
            "with several banks, and each bank saw only its own slice. <bookmark mark='a'/> When the stocks fell, the "
            "banks raced to sell the collateral. Those that sold first lost less; Credit Suisse lost about five and "
            "a half billion dollars, and Nomura almost three. Every one of those losses was counterparty risk: the "
            "chance that the other side of a derivative cannot pay what it owes."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
        self.add(illustration(r"Paul, Weiss report to Credit Suisse's board (July 2021); company disclosures"))
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1987, r"ISDA master agreement", R_), (1998, r"LTCM's counterparties", C),
                   (2005, r"CVA in pricing", I), (2008, r"Lehman's swaps", C), (2010, r"Basel III CVA capital", R_),
                   (2011, r"Burgard--Kjaer: FVA", I), (2012, r"the FVA debate", I), (2013, r"FVA in earnings", F),
                   (2014, r"SA-CCR; KVA", R_), (2016, r"margin rules begin", R_), (2020, r"March 2020 margin calls", C),
                   (2021, r"Archegos", C), (2022, r"LME nickel", C), (2023, r"deep xVA solvers", I)]
        strip = era_strip(entries, y0=1984, y1=2026, font_size=15).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 9), (9, 14)]
        with self.voiceover(
            "How we got here. In 1987 dealers agreed a master contract for swaps, with netting on default. In 1998 "
            "the rescue of Long-Term Capital Management was a rescue of its counterparties. By the mid-2000s the big "
            "dealers were charging a credit valuation adjustment on their trades; then Lehman left thousands of "
            "swaps to be closed out. <bookmark mark='a'/> The Basel Committee found that most counterparty losses in "
            "the crisis came not from defaults but from the falling value of CVA, and charged capital for it. "
            "Burgard and Kjaer added funding in 2011, Hull and White argued in 2012 it does not belong in prices, and "
            "in 2013 the banks booked it anyway. <bookmark mark='b'/> Then the standardised approach to counterparty "
            "exposure, the capital adjustment, mandatory margin from 2016, and three episodes: March 2020, Archegos, "
            "and the London Metal Exchange's nickel market in 2022."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Exposure: what a counterparty could owe you, path by path, netted and collateralised",
            r"CVA and DVA derived and computed; wrong-way risk",
            r"FVA, KVA and MVA: the costs of funding, capital and margin, and the debate about them",
            r"Sensitivities by one backward pass (AAD), and a network that learns future values",
            r"Initial margin, its procyclicality, and central clearing's default waterfall",
            r"Capital: SA-CCR; and from the record, the LME's nickel market and Archegos",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: exposure, simulated and netted; the credit adjustment and its mirror; when default and exposure "
            "move together; the costs of funding, capital and margin; sensitivities by a single backward pass, and a "
            "network that learns what the book will be worth; initial margin, clearing houses and their waterfalls; "
            "capital; and two episodes from the public record. Along the way: why netting is a matter of law, how a "
            "CVA desk hedges, why a new trade's price depends on everything else the client has done with you, when "
            "a clearing house makes the system safer and when it does not, and how much margin a concentrated "
            "position really needs. Every number is computed by the House's code, and every case comes from the "
            "public record."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=11))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("credit",))
        with self.voiceover(
            "In the House, the credit desk becomes an XVA desk: every trade the House does is also a loan to whoever "
            "is on the other side, and is priced as one."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["credit"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    def scope(self):
        cards = objectives_card([r"Dated curve; historical volatility proxies, not option-price calibration", r"Swap exposure sketch: floating reset approximation; invented credit quotes", r"Deterministic-discount CVA and policy-dependent cost accounting"], color=QC.IDEA)
        with self.voiceover('Before computing, fix the experiment. We use the public curve dated December 2025, with historical rate-volatility proxies rather than calibration to traded option prices. <bookmark mark="a"/> The swap engine resets the current floating period at each valuation date, ignoring past fixings. It is a controlled exposure sketch, not a production mark. Default curves and all policy parameters are illustrative. <bookmark mark="b"/> The CVA calculations multiply expected exposure by deterministic discount factors. A general stochastic-rate valuation needs the joint discounted exposure, default and closeout. Funding, capital and margin costs require a consistent policy; adding labels mechanically can double-count the same economic cost.') as vo:
            self.play(FadeIn(cards.head), FadeIn(cards.rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards.rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards.rows[2]))
        self.clear_scene()
