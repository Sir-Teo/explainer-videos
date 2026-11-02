from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CCP, PART, TRADE, load, node


class Clearing(VoiceoverScene):
    def construct(self):
        n = load("netting")
        self.card()
        self.novation()
        self.netting(n)
        self.settlement()

    def card(self):
        c = chapter_card(3, r"Clearing and settlement", r"Who guarantees that you get paid?", part=PART)
        with self.voiceover("Chapter three. Clearing and settlement."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def novation(self):
        a, b = node(r"buyer A", TRADE), node(r"seller B", TRADE)
        VGroup(a, b).arrange(RIGHT, buff=5.0).shift(UP * 1.6)
        ab = DoubleArrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        before = label(r"before: A is exposed to B failing, and B to A", font_size=24, color=GREY_A).next_to(VGroup(a, b), UP, buff=0.3)
        a2, c, b2 = node(r"buyer A", TRADE), node(r"CCP", CCP, width=2.0), node(r"seller B", TRADE)
        VGroup(a2, c, b2).arrange(RIGHT, buff=2.0).shift(DOWN * 1.2)
        ac = DoubleArrow(a2.get_right(), c.get_left(), buff=0.1, color=CCP, stroke_width=3)
        cb = DoubleArrow(c.get_right(), b2.get_left(), buff=0.1, color=CCP, stroke_width=3)
        after = label(r"after novation: each faces only the clearing house", font_size=24, color=CCP).next_to(c, DOWN, buff=0.4)
        protect = wrapped_label(r"the CCP protects itself with margin from every member, a default fund they all pay "
                                r"into, and its own capital: the default waterfall (Part 21)", 11.0, 22, GREY_A)
        protect.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A trade is a promise between two strangers. If the seller fails to deliver, or the buyer fails to pay, "
            "the other side is left exposed. <bookmark mark='a'/> A central counterparty removes that risk by "
            "novation: the original trade is replaced by two, buyer with the clearing house and clearing house with "
            "seller. Everyone now faces one counterparty, the most closely watched one in the market. "
            "<bookmark mark='b'/> To survive a member's default, the clearing house collects margin from every "
            "member, keeps a default fund they all contribute to, and puts up its own capital: a waterfall that "
            "Part twenty-one drains, layer by layer."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), GrowFromCenter(ab), FadeIn(before))
            vo.wait_until("a")
            self.play(TransformFromCopy(a, a2), TransformFromCopy(b, b2), FadeIn(c))
            self.play(GrowFromCenter(ac), GrowFromCenter(cb), FadeIn(after))
            vo.wait_until("b")
            self.play(FadeIn(protect))
        self.wait(0.4)
        self.clear_scene()

    def netting(self, n):
        vals = [n["gross"], n["bilateral"], n["multilateral"]]
        names = [r"gross: every trade settled", r"bilateral: each pair nets", r"through a CCP: each member nets"]
        cols = [GREY_B, QC.IDEA, CCP]
        g = axes([-0.5, 2.5], [0, vals[0] * 1.15 / 1e9], x_length=7.0, y_length=4.4,
                 ylabel=r"obligations to settle, \$ billion", yticks=[0, 4, 8, 12], font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        tags = VGroup()
        for i, (v, nm, col) in enumerate(zip(vals, names, cols)):
            h = ax.c2p(0, v / 1e9)[1] - ax.c2p(0, 0)[1]
            b = Rectangle(width=1.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to(ax.c2p(i, v / 2e9))
            bars.add(b)
            tags.add(VGroup(MathTex(rf"\${v / 1e9:.1f}\,\text{{bn}}", font_size=30, color=col).next_to(b, UP, buff=0.1),
                            wrapped_label(nm, 2.0, 18, GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15)))
        res = VGroup(
            label(rf"{n['trades']:,} trades among {n['n']} members".replace(",", "{,}"), font_size=24),
            MathTex(rf"\text{{netting removes}}\ {100 * n['saved']:.0f}\%", font_size=36, color=CCP),
            label(r"simulated: heavy-tailed trade sizes, a few busy members", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        with self.voiceover(
            "The clearing house's second gift is netting. Here is a simulated day: "
            f"{n['trades']:,} trades among {n['n']} members. Settled one by one, they would move "
            f"{n['gross'] / 1e9:.0f} billion dollars. <bookmark mark='a'/> If each pair of members nets its trades "
            f"against each other, {n['bilateral'] / 1e9:.1f} billion. <bookmark mark='b'/> If the clearing house "
            "nets everything, each member pays or receives only its net position: "
            f"{n['multilateral'] / 1e9:.1f} billion. Netting removes {100 * n['saved']:.0f} percent of what must "
            "move, and of what can go wrong."
        ) as vo:
            self.play(FadeIn(g), GrowFromEdge(bars[0], DOWN), FadeIn(tags[0]), FadeIn(res[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(tags[2]))
            self.play(FadeIn(res[1:]))
        self.wait(0.4)
        self.clear_scene()

    def settlement(self):
        steps = [(r"before 1995", r"T+5"), (r"June 1995", r"T+3"), (r"September 2017", r"T+2"), (r"28 May 2024", r"T+1")]
        items = VGroup()
        for when, t in steps:
            items.add(VGroup(MathTex(t, font_size=50, color=CCP), label(when, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15))
        items.arrange(RIGHT, buff=1.3).shift(UP * 1.0)
        arrows = VGroup(*[Arrow(items[i].get_right(), items[i + 1].get_left(), buff=0.15, color=GREY_B, stroke_width=3)
                          for i in range(3)])
        why_ = wrapped_label(r"every day between trade and settlement is a day of risk the clearing house must "
                             r"collateralize: shorter settlement means smaller deposits, and less time to find the "
                             r"cash", 11.0, 24, WHITE).next_to(items, DOWN, buff=0.8)
        tag = note(r"US equities; China's A-shares settle securities T+1 as well, and do not let a share bought today be "
                   r"sold until tomorrow (chapter 9)", font_size=18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Settlement is when shares and cash actually move. American stocks once settled five business days "
            "after the trade, then three from 1995, two from 2017, and since the 28th of May 2024, one. "
            "<bookmark mark='a'/> Every day between trade and settlement is a day in which someone might fail, and "
            "the clearing house asks for collateral to cover it. Shorter settlement means smaller deposits, and "
            "less time to find the cash: the trade-off behind Robinhood's morning in January 2021."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in items], lag_ratio=0.4), LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                                         lag_ratio=0.4), run_time=4)
            vo.wait_until("a")
            self.play(FadeIn(why_), FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()
