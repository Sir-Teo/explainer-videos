from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H = R["hook"]
        lines = [
            ("the first copy is costly; the rest are almost free, so margins rise with scale", ENG),
            ("selling is the largest cost: customers are won at a loss and paid back if they stay", SALES),
            ("subscriptions trade a sale today for revenue every year, paid in advance", SUB),
            ("what keeps customers is lock-in: their data, their staff, their workflows", PROFIT),
            (f"AI makes each answer cost something again: Microsoft's cloud margin fell to {H['cloudgm']}%", AI),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So what is a business worth when the second copy costs nothing? <bookmark mark='a'/> A great deal, at scale: "
             "the costs stay put while the revenue grows. <bookmark mark='b'/> But finding each customer is expensive, and "
             "they are won at a loss. <bookmark mark='c'/> Subscriptions turn one sale into a stream, paid in advance. "
             "<bookmark mark='d'/> What keeps the stream flowing is lock-in: the data, the staff and the habits built around "
             "the product. <bookmark mark='e'/> And now artificial intelligence makes each answer cost something again. A "
             "software company is worth what its customers will keep paying for the next copy.",
             base=[head("Paid for the next copy")], steps=list(g))

    def close(self):
        lap = draw.laptop(2.6).move_to([-2.8, 0.2, 0])
        rack = draw.server_rack(1.6).move_to([2.8, 0.2, 0])
        nxt = tx("Next: Part 37, Cloud and Data Centres", 26, STOCK, bold=True).move_to([0, -2.6, 0])
        with self.voiceover("A laptop and a server rack. Next time: cloud and data centres, the factories where software, and "
                            "now artificial intelligence, actually runs."):
            self.play(LaggedStart(FadeIn(lap), FadeIn(rack), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
