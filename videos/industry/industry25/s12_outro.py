from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, U, P, B = R["hook"], R["run"], R["prices"], R["builder"]
        lines = [
            (f"the loan: the same new house cost {money(H['pay'][H['m21']])} a month in 2021 and {money(H['pay'][H['m26']])} in 2026", LOAN),
            (f"the land: prices x{P['cs'][2025]:.1f} since 2000, materials x{P['ppi'][2025]:.1f}; the gap is land and permission", LAND),
            (f"the builder: own the lot or option it; Lennar controls {B['len']['controlled'][1]:.0f}% of its homesites by option", OPTION),
            (f"the squeeze: incentives of ${B['len']['incent'][1]:.1f}k a home; D.R. Horton's margin {B['dhi']['gm_prev']}% to {B['dhi']['gm']}%", BAD),
            ("the middlemen: commissions renegotiated in 2024; portals and brokers barely profitable", PRICE),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So where does the price of a house come from? <bookmark mark='a'/> From the loan: what a buyer can pay is "
             "what a buyer can borrow, and the rate on a thirty-year loan has moved the monthly cost more than the price "
             "has. <bookmark mark='b'/> From the land: house prices have outrun the cost of building, and the difference "
             "is land near jobs and the permission to build on it. <bookmark mark='c'/> From the builder's bet on both: "
             "land secured years ahead, which is why the largest builders now control their land by option rather than "
             "own it. <bookmark mark='d'/> When rates rise, the builders pay to bring the buyer's payment down, and their "
             "margins pay for it. <bookmark mark='e'/> And from the people in between, whose rules changed in 2024. The "
             "house itself is the smallest part of the story.",
             base=[head("The house, the land and the loan")], steps=list(g))

    def close(self):
        lot = draw.plot_lot(1.8).move_to([-4.4, 0.4, 0])
        frame = draw.house_frame(1.8).move_to([-1.4, 0.6, 0])
        house = draw.house(1.6, color="#F2D0A4").move_to([1.6, 0.6, 0])
        key = draw.house_key(1.4).move_to([4.6, 0.8, 0])
        nxt = tx("Next: Part 26, Property", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A plot, a frame, a house and a key: four things bought with four different kinds of money. Next "
                            "time: property, the offices, shops and warehouses that companies rent, and the investors who own "
                            "them.") as vo:
            self.play(LaggedStart(FadeIn(lot), FadeIn(frame), FadeIn(house), FadeIn(key), lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(nxt))
        self.clear_scene()
