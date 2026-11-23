from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Carrier(VoiceoverScene):
    def construct(self):
        card(self, 6, "The carrier's side of the deal", "How can a carrier sell a phone for less than it paid?",
             "Chapter six. The carrier's side of the deal.", lit=("dollar", "moat"))
        self.tmobile()
        self.meaning()

    def tmobile(self):
        K = R["carrier"]
        sc = 4.2 / K["sv_rev"]
        base = DOWN * 2.0

        def bar(v, x, c, op=0.9):
            return Rectangle(width=1.25, height=sc * v, fill_color=c, fill_opacity=op, stroke_width=0).move_to(
                base + RIGHT * x, aligned_edge=DOWN)
        eq_r, eq_c = bar(K["eq_rev"], -5.0, I.CHANNEL), bar(K["eq_cost"], -3.3, I.COST)
        sv_r, sv_c = bar(K["sv_rev"], 1.2, I.PROFIT), bar(K["sv_cost"], 2.9, I.COST)
        axis = Line(LEFT * 6, RIGHT * 4.2, color=I.FAINT).move_to(base, aligned_edge=LEFT).shift(LEFT * 0.0)
        axis.set_x(-0.9)
        def lab(b, top, sub, c):
            return VGroup(TB(top, 22, c), T(sub, 15, I.DIM)).arrange(DOWN, buff=0.04).next_to(b, UP, buff=0.1)
        l1 = lab(eq_r, money_short(K["eq_rev"]), "phones sold", I.CHANNEL)
        l2 = lab(eq_c, money_short(K["eq_cost"]), "what they cost it", I.COST)
        l3 = lab(sv_r, money_short(K["sv_rev"]), "monthly plans", I.PROFIT)
        l4 = lab(sv_c, money_short(K["sv_cost"]), "cost of the network*", I.COST)
        g1 = VGroup(TB("The phones", 24, I.TEXT)).next_to(VGroup(eq_r, eq_c), DOWN, buff=0.25)
        g2 = TB("The service", 24, I.TEXT).next_to(VGroup(sv_r, sv_c), DOWN, buff=0.25)
        loss = VGroup(TB(f"-{money_short(-K['eq_loss'])}", 30, I.COST), T("sold below cost", 18, I.TEXT)
                      ).arrange(DOWN, buff=0.05).next_to(VGroup(eq_r, eq_c), RIGHT, buff=0.35).shift(UP * 0.4)
        head = VGroup(TB("T-Mobile US, 2025", 28, I.TEXT), T("from its annual report", 18, I.DIM)
                      ).arrange(DOWN, buff=0.05).to_edge(UP, buff=0.45)
        foot = T("*cost of services before depreciation; selling and overheads come on top", 15, I.FAINT).to_corner(DR,
                                                                                                                 buff=0.3)
        src = source("T-Mobile US Form 10-K, 2025")
        with self.voiceover(
            "Many people in America do not walk into a shop and hand over 1,099 dollars. They get the phone from a "
            "carrier, often paid for over two or three years, often with a large discount for signing up or trading "
            "in an old phone. What does the carrier make on the phone itself? <bookmark mark='a'/> T-Mobile's annual "
            "report answers it. In 2025 it sold phones and other equipment for 16 billion dollars. <bookmark mark='b'/> "
            "They cost it 21.3 billion. <bookmark mark='c'/> It sold them for 5.3 billion dollars less than it paid. "
            "<bookmark mark='d'/> Why would anyone do that? Because of the other line in the report: 71.3 billion "
            "dollars of monthly service, <bookmark mark='e'/> against 11.5 billion of direct network costs. The phone "
            "is the bait; the monthly bill is the business."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(GrowFromEdge(eq_r, DOWN), FadeIn(l1), FadeIn(g1))
            vo.wait_until("b")
            self.play(GrowFromEdge(eq_c, DOWN), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(loss, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(GrowFromEdge(sv_r, DOWN), FadeIn(l3), FadeIn(g2))
            vo.wait_until("e")
            self.play(GrowFromEdge(sv_c, DOWN), FadeIn(l4), FadeIn(foot))
        self.clear_scene()

    def meaning(self):
        K = R["carrier"]
        lo, hi = 0.03 * 0.6 * 1099, 0.15 * 0.6 * 1099
        rows = VGroup(
            VGroup(TB("In the Dollar of chapter five", 24, I.ACCENT),
                   T(f"the shop or carrier keeps {money(amount('channel'))} on average, range {money(lo)} to "
                     f"{money(hi)}", 22, I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(TB("For a carrier", 24, I.CHANNEL),
                   T("the slice of the phone's price can be zero or less:", 22, I.TEXT),
                   T("it pays Apple for the phone and recovers the discount from your bill", 22, I.TEXT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(TB("For Apple", 24, I.BRAND),
                   T("nothing changes: it is paid for the phone either way", 22, I.TEXT)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(TB("AT&T, 2025", 24, I.TEXT),
                   T(f"equipment {money_short(K['att_eq'])}, about 18% of its revenue; the service is the rest", 22,
                     I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(LEFT * 0.4)
        src = source("AT&T Form 10-K, 2025; this film's model", corner=DR)
        with self.voiceover(
            "So the shop's slice in our Dollar needs a second look. <bookmark mark='a'/> In chapter five we gave the "
            "shop or carrier about 66 dollars on average, with a range from about 20 to about 100. <bookmark "
            "mark='b'/> For a carrier, the slice of the phone's own price can be zero, or less: it pays Apple for "
            "the phone, gives part of it away, and earns the money back from the monthly bill. <bookmark mark='c'/> "
            "For Apple nothing changes. It is paid for the phone either way. <bookmark mark='d'/> AT&T tells the same "
            "story: equipment was about a fifth of its revenue in 2025, and the service was the rest. A carrier is "
            "not really in the business of selling phones. It is in the business of renting you its network, and "
            "Part 30 of this series is about that business."
        ) as vo:
            self.play(FadeIn(src), FadeIn(rows[0], shift=RIGHT * 0.15))
            for i, m in enumerate("bcd", start=1):
                vo.wait_until(m)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
