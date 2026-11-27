from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U, S, L = R["run"], R["seat"], R["loyalty"]
        lines = [
            (f"perishable seats, fixed costs: one flight from a ${abs(U['first']['profit']):,.0f} loss to a ${U['both']['profit']:,.0f} profit by pricing alone", BIZ),
            (f"thin margins: Delta {S['dal'][0] - S['dal'][1]:.2f} cents a seat-mile, Southwest {S['luv'][0] - S['luv'][1]:.2f}, Spirit {S['save'][0] - S['save'][1]:.2f}", SKY),
            (f"costs it does not control: ${R['called']['hit']:.0f}bn more for Delta's fuel in 2026", FUEL),
            (f"costs it cannot cut: planes {R['pandemic']['lf_m']['2020-04']:.0f}% full in April 2020, and ${R['pandemic']['psp']:.0f}bn of public help", BAD),
            (f"the bank in the airline: American Express paid Delta ${L['amex']:.1f}bn, more than Delta's profit", CARD),
            (f"the owners of the planes keep more: AerCap {100 * R['lessors']['aer']:.0f}%, Delta {100 * R['lessors']['dal']:.0f}%", GOOD),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So why has an industry that changed the world made so little money? <bookmark mark='a'/> Because it sells the "
             "most perishable thing there is, a seat on a departing flight, at a cost fixed in advance, so every airline is "
             "tempted to fill the last seat at any price. <bookmark mark='b'/> Because competition, which the law of 1978 "
             "unleashed, pushes the margin on a seat-mile towards zero. <bookmark mark='c'/> Because its second-largest cost "
             "is set by wars and oil markets, <bookmark mark='d'/> and most of the rest cannot be cut when the passengers "
             "stop coming, as 2020 showed. <bookmark mark='e'/> The airlines that do well have found money outside the "
             "seat, above all in the banks that buy their miles; <bookmark mark='f'/> and the steadiest money is with whoever "
             "owns the planes and rents them out.",
             base=[head("Perishable seats, fixed costs")], steps=list(g))

    def close(self):
        plane = draw.plane(4.4).move_to([-2.4, 0.4, 0])
        cab = draw.cabin(rows=20, seats=(3, 3), size=0.16, gap=0.03).move_to([3.6, 0.4, 0])
        fill(cab, 90, 24)
        nxt = tx("Next: Part 29, Rail, Trucks and Parcels", 26, BIZ, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("An aircraft, and the seats inside it sold at many prices. Next time: rail, trucks and parcels, how "
                            "goods move on land, from the freight train to the van at your door."):
            self.play(LaggedStart(FadeIn(plane), FadeIn(cab), lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
