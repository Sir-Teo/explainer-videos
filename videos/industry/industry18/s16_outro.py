from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        P, T, E, D = R["programme"], R["two"], R["engines"], R["defence"]
        tdg = next(c for c in R["landscape"]["companies"] if c["name"] == "TransDigm")["margin"]
        lines = [
            (f"a new airliner: ${P['dev']:.0f}bn and {P['dev_years']} years before the first delivery; even after "
             f"{P['be']['units']:,.0f} aircraft (the Works)", AIRBUS),
            (f"two makers, each with about ten years of orders: Airbus {T['ab_years']:.0f}, Boeing {T['ba_years']:.0f}", PRICE),
            (f"GE's engines: ${E['services'] / 1e3:.0f}bn of servicing against ${E['equipment'] / 1e3:.0f}bn of new "
             "engines", ENGINE),
            (f"parts makers with their own designs kept the most: TransDigm about {100 * tdg:.0f} cents in the dollar", SUPPLIER),
            (f"defence: one buyer per country, margins of five to ten per cent; Lockheed {D['usg']}% American government", DEFENCE),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So, why are there only two makers of large airliners? <bookmark mark='a'/> Because a new one costs tens of "
             "billions and a decade before the first delivery, and pays back only after a thousand aircraft. "
             "<bookmark mark='b'/> Because the two that exist have built thousands each, are far down their learning "
             "curves, and hold ten years of orders. <bookmark mark='c'/> And why does the engine maker sell at a loss? "
             "Because the engine is a ticket to decades of servicing, which brings in three times what new engines do. "
             "<bookmark mark='d'/> The same logic rewards the parts makers that own their designs, <bookmark mark='e'/> "
             "while defence runs on a different one: one buyer, budgets set in public, and margins it keeps in check.",
             base=[head("Two makers, measured")], steps=list(g))

    def close(self):
        a = draw.plane(4.0, AIRBUS).move_to([-8.5, 1.2, 0])
        b = draw.plane(4.0, BOEING).move_to([8.5, -0.6, 0]).flip(UP)
        nxt = tx("Next: Part 19, Machinery", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("The story of an industry where two companies share a market, one wrong bet can cost a "
                            "decade, and the money is made long after the sale. Next time: machinery, the industry that "
                            "makes the machines that make everything else.") as vo:
            self.play(a.animate.move_to([8.5, 1.2, 0]), b.animate.move_to([-8.5, -0.6, 0]), run_time=6, rate_func=linear)
            self.play(FadeIn(nxt))
        self.clear_scene()
