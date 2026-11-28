from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, U, S, T = R["hook"], R["run"]["runs"], R["sub"], R["towers"]
        lines = [
            (f"the airwaves are sold like land: in the Works, asking for less cut the price from ${U[4]['price']:.2f}bn to ${U[2]['price']:.2f}bn a block", TOWER),
            (f"a subscriber is worth about ${S['life']:,.0f} and leaves at {100 * S['churn']:.2f}% a month, and the three look alike", WIRELESS),
            (f"the network is never finished: about {100 * R['net']['capex']['AT&T'][0] / R['net']['capex']['AT&T'][1]:.0f} cents of AT&T's dollar went on it in 2025", BAD),
            (f"the landlords keep more: American Tower {T['amt_margin'][2025]:.0f}% operating margin", TOWER),
            (f"and what runs over the pipe earns more: ${H['over'][2025]:.0f}bn against ${H['carriers3'][2025]:.0f}bn", OVER),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So why do the companies that carry everything capture so little of it? <bookmark mark='a'/> Because they pay "
             "up front for airwaves sold like land. <bookmark mark='b'/> Because three networks sell nearly the same thing "
             "to customers who leave for a better price. <bookmark mark='c'/> Because the network is never finished. "
             "<bookmark mark='d'/> Because the scarce pieces, the airwaves and the towers, belong to governments and "
             "landlords. <bookmark mark='e'/> And because the value of what travels over the pipe belongs to whoever made "
             "it, not to whoever carried it. The carriers are not failing: they earn steady money from customers who rarely "
             "leave. But they are the road, not the traffic, and the road is paid by the mile.",
             base=[head("Essential, costly, alike")], steps=list(g))

    def close(self):
        tw = draw.cell_tower(2.6).move_to([-3.0, 0.4, 0])
        ph = VGroup(*[draw.phone(0.9, screen=c) for c in (WIRELESS, OVER, CABLE)]).arrange(RIGHT, buff=0.3).move_to([2.6, 0.4, 0])
        nxt = tx("Next: Part 31, Grocery and Mass Retail", 26, TOWER, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A tower, and the phones it serves. Next time: grocery and mass retail, the business of "
                            "selling everything else, a few cents at a time."):
            self.play(LaggedStart(FadeIn(tw), FadeIn(ph), lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
