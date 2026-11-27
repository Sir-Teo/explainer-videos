from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class England(VoiceoverScene):
    def construct(self):
        card(self, 4, "England's experiment", "What happens when a monopoly is sold, borrowed against and then asked to invest?",
             "Chapter four. England's experiment.", lit=("dollar", "moat", "change"))
        self.owners()
        self.review()
        self.thames()

    def owners(self):
        G = R["regulated"]
        def boxes(n, col, label):
            return VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.55, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85)
                            for _ in range(n)])
        then = boxes(int(G["wascs"]), UK, "listed").arrange(RIGHT, buff=0.1)
        then_l = VGroup(tx("1989", 26, WHITE, bold=True), tx(f"{G['wascs']:.0f} water and sewerage companies,", 15, GREY_A),
                        tx("all listed on the London Stock Exchange", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        row1 = VGroup(then_l, then).arrange(RIGHT, buff=0.5).move_to([0, 1.6, 0])
        now = VGroup(boxes(int(G["listed"]), UK, ""), boxes(7, "#B58CFF", ""), boxes(1, GOOD, "")).arrange(RIGHT, buff=0.35)
        for g_ in now:
            g_.arrange(RIGHT, buff=0.1)
        now.arrange(RIGHT, buff=0.35)
        now_keys = VGroup(tx("listed", 13, UK).next_to(now[0], DOWN, buff=0.1), tx("privately owned", 13, "#B58CFF").next_to(now[1], DOWN, buff=0.1),
                          tx("not for profit\n(Welsh Water)", 12, GOOD).next_to(now[2], DOWN, buff=0.1))
        now_l = VGroup(tx("2025", 26, WHITE, bold=True), tx("water and sewerage companies", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        row2 = VGroup(now_l, VGroup(now, now_keys)).arrange(RIGHT, buff=0.5).move_to([0, -0.5, 0])
        wocs = tx(f"water-only companies: {G['wocs'][0]:.0f} in 1989, {G['wocs'][1]:.0f} today", 18, GREY_A).move_to([0, -2.3, 0])
        src = source("Independent Water Commission, Final Report (July 2025), paragraphs 671-672", size=13)
        with self.voiceover(
            "England is where this model was pushed furthest. <bookmark mark='a'/> In 1989 the government sold its "
            f"{G['wascs']:.0f} regional water and sewerage authorities as companies listed on the stock exchange, with "
            "little debt and a regulator, Ofwat, to set their prices. <bookmark mark='b'/> By 2025 only "
            f"{G['listed']:.0f} were still listed. Seven had been bought by private owners, from private equity funds to "
            "international infrastructure companies, and Welsh Water is run not for profit. <bookmark mark='c'/> The smaller water-only companies "
            f"were consolidated from {G['wocs'][0]:.0f} to {G['wocs'][1]:.0f}. A steady, inflation-linked return on a "
            "monopoly is exactly what long-term investors want to own."
        ) as vo:
            ghost = VGroup(then.copy().set_fill(opacity=0.15), now.copy().set_fill(opacity=0.15))
            self.play(FadeIn(src), FadeIn(ghost), FadeIn(then_l[0]), FadeIn(now_l[0]))
            vo.wait_until("a")
            self.play(FadeIn(then_l), LaggedStart(*[GrowFromCenter(b) for b in then], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(now_l), LaggedStart(*[GrowFromCenter(b) for g_ in now for b in g_], lag_ratio=0.06), FadeIn(now_keys), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(wocs, shift=UP * 0.1))
        self.clear_scene()

    def review(self):
        G = R["regulated"]
        sc = 2.4 / 110
        b19 = Rectangle(width=1.1, height=G["allow19"] * sc, stroke_width=0, fill_color="#5D6B82", fill_opacity=0.9).move_to([-5.2, -1.6, 0], aligned_edge=DOWN)
        b24 = Rectangle(width=1.1, height=G["allow24"] * sc, stroke_width=0, fill_color=UK, fill_opacity=0.9).move_to([-3.7, -1.6, 0], aligned_edge=DOWN)
        l19 = VGroup(tx(f"£{G['allow19']:.0f}bn", 20, WHITE, bold=True).next_to(b19, UP, buff=0.08), tx("2020-25", 14, GREY_A).next_to(b19, DOWN, buff=0.08))
        l24 = VGroup(tx(f"£{G['allow24']:.0f}bn", 20, UK, bold=True).next_to(b24, UP, buff=0.08), tx("2025-30", 14, GREY_A).next_to(b24, DOWN, buff=0.08))
        h1 = tx("what Ofwat allows the sector to spend", 15, GREY_A).move_to([-4.45, 1.9, 0])
        wacc = VGroup(tx("allowed return, after inflation", 16, GREY_A),
                      tx(f"2020-25: {G['wacc19']:.2f}%", 22, WHITE, bold=True),
                      tx(f"2025-30: {G['wacc24']:.2f}%", 22, UK, bold=True),
                      tx(f"(for five companies that appealed, the CMA: {G['cma_wacc']:.2f}%)", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([0.4, 0.9, 0])
        bill = VGroup(tx("the average bill, 2025/26", 16, GREY_A), tx(f"£{G['bill']:.0f} a year", 30, PRICE, bold=True),
                      tx(f"of which £{G['wacc_bill']:.0f} more from the higher return", 15, GREY_A),
                      tx(f"then about £{G['bill_rise']:.0f} more each year to 2029/30, before inflation", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.4, 0.9, 0])
        eq = VGroup(tx(f"£{G['enh']:.0f}bn of improvements needs £{G['equity'][0]:.0f}-{G['equity'][1]:.0f}bn of new equity", 18, WHITE, bold=True),
                    tx("the Water Commission's estimate", 14, GREY_A)).arrange(DOWN, buff=0.05).move_to([2.4, -1.9, 0])
        src = source("CMA, PR24 redeterminations: final determinations summary (March 2026); Independent Water Commission, "
                     "Final Report (July 2025); Water UK", size=13)
        with self.voiceover(
            "Then came the bill for the pipes. The government and the regulators wanted far more investment: in sewage "
            "works and storm overflows, in reservoirs and in mains. <bookmark mark='a'/> For 2020 to 2025, Ofwat had allowed "
            f"the sector about £{G['allow19']:.0f} billion of spending. <bookmark mark='b'/> For 2025 to 2030, about "
            f"£{G['allow24']:.0f} billion, in today's prices. <bookmark mark='c'/> To attract the money, it raised the "
            f"return it allows on the asset base, from {G['wacc19']:.2f} per cent to {G['wacc24']:.2f} per cent after "
            f"inflation; five companies appealed, and the competition authority gave them {G['cma_wacc']:.2f}. "
            f"<bookmark mark='d'/> The average bill for 2025-26 is about £{G['bill']:.0f} a year, of which about "
            f"£{G['wacc_bill']:.0f} is the higher return alone, and Ofwat expects bills to keep rising by about "
            f"£{G['bill_rise']:.0f} a year before inflation. <bookmark mark='e'/> And because the companies borrowed so "
            "much in the cheap years, the Water Commission reckoned they would need "
            f"£{G['equity'][0]:.0f} to {G['equity'][1]:.0f} billion of new equity from their owners to pay for it."
        ) as vo:
            ghost = VGroup(b19.copy().set_fill(opacity=0.15), b24.copy().set_fill(opacity=0.15), l19[1].copy(), l24[1].copy(),
                           tx("England and Wales: the 2024 price review", 22, WHITE, bold=True).to_edge(UP, buff=0.35))
            self.play(FadeIn(src), FadeIn(h1), FadeIn(ghost))
            vo.wait_until("a")
            self.play(GrowFromEdge(b19, DOWN), FadeIn(l19))
            vo.wait_until("b")
            self.play(GrowFromEdge(b24, DOWN), FadeIn(l24))
            vo.wait_until("c")
            self.play(FadeIn(wacc, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(bill, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(eq, shift=UP * 0.1))
        self.clear_scene()

    def thames(self):
        G = R["regulated"]
        events = [("July 2025", "the Water Commission:", f"Thames is '£{G['thames_debt']:.1f} billion in debt'", GREY_A),
                  ("6 March 2026", "a group of its creditors", "proposes to recapitalize it", UK),
                  ("16 June 2026", "the Environment Secretary: the", "proposal does not 'go far enough'", PRICE),
                  ("November 2026", "the decision is Ofwat's;", "none announced in the records we checked", BAD)]
        line = Line([-5.6, -0.6, 0], [5.6, -0.6, 0], stroke_color=GREY_B, stroke_width=3)
        marks = VGroup()
        for i, (d, a, b, col) in enumerate(events):
            x = -5.0 + 3.35 * i
            dot = Dot([x, -0.6, 0], radius=0.1, color=col)
            lab = VGroup(tx(d, 21, col, bold=True), tx(a, 15, GREY_A), tx(b, 15, GREY_A)).arrange(DOWN, buff=0.05)
            lab.next_to(dot, UP if i % 2 == 0 else DOWN, buff=0.2)
            marks.add(VGroup(dot, lab))
        head = VGroup(tx("Thames Water", 30, WHITE, bold=True),
                      tx(f"{G['thames_customers']:.0f} million customers in and around London", 16, GREY_A)).arrange(DOWN, buff=0.06).to_edge(UP, buff=0.35)
        lorry = VGroup(draw.drop(0.7), tx(f"£{G['thames_debt']:.1f}bn of debt", 34, BAD, bold=True)).arrange(RIGHT, buff=0.25).move_to([0, 1.6, 0])
        src = source("Independent Water Commission, Final Report (July 2025), Box 21; Hansard, HC Deb 16 June 2026 "
                     "(Thames Water); GOV.UK", size=13)
        with self.voiceover(
            "The sharpest case is the company that serves the city where this story began. <bookmark mark='a'/> Thames "
            f"Water has about {G['thames_customers']:.0f} million customers. When the Water Commission reported in July "
            f"2025, it noted that Thames was £{G['thames_debt']:.1f} billion in debt, and that Ofwat had just penalized "
            f"it £{G['thames_penalty']:.0f} million over its business plan. <bookmark mark='b'/> In "
            "March 2026, a consortium of the company's own lenders proposed to take it over and put in new money. "
            "<bookmark mark='c'/> In June, the Environment Secretary told Parliament that the offer did not go far "
            "enough to protect customers and the environment. <bookmark mark='d'/> The decision is Ofwat's, and would "
            "then need a public consultation and a court. When this film was made, none had been announced. The model "
            "that works so smoothly in the Works, a steady return on a growing base, fails when the company is "
            "heavily indebted and the next round of pipes has to be paid for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(line))
            for m_, mk in zip("abcd", marks):
                vo.wait_until(m_)
                self.play(GrowFromCenter(mk[0]), FadeIn(mk[1], shift=UP * 0.1 if m_ in "ac" else DOWN * 0.1))
                if m_ == "a":
                    self.play(FadeIn(lorry, shift=UP * 0.1))
        self.clear_scene()
