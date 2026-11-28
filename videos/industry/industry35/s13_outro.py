from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, C, Cs = R["hook"], R["contract"], R["casino"]
        lines = [
            (f"the brands sell names, bookings and loyalty; Marriott owns {100 * H['own_share']:.1f}% of its rooms", BRAND),
            ("owners buy and borrow for the buildings, and are paid last, after the brand and the bank", OWNER),
            (f"fees on revenue are paid every month; fees on profit only when owners clear their hurdle ({C['imf_us']}% in the U.S.)", GOOD),
            ("the agents sit in the middle, buy attention and earn the most of all", AGENT),
            ("ships, casinos and parks still own their capacity, and live by filling it", CRUISE),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So why do the biggest hotel companies own almost no hotels? <bookmark mark='a'/> Because what they sell is not "
             "the building but the guest: a name, a booking system and a loyalty programme. <bookmark mark='b'/> Owners pay "
             "for the buildings, borrow against them, and are paid last. <bookmark mark='c'/> The brand's fees come off the "
             "top of revenue every month; the fees on profit arrive only when the owner has done well. "
             "<bookmark mark='d'/> The online agents, in the middle, earn the most of all. <bookmark mark='e'/> And the "
             "businesses that still own their capacity, the ships, the casinos and the parks, live by keeping it full. A hotel "
             "brand is a name on someone else's building.",
             base=[head("A brand on someone else's building")], steps=list(g))

    def close(self):
        ht = draw.hotel(2.2, floors=12, seed=9).move_to([-3.0, 0.0, 0])
        draw.light(ht.windows, 0.7)
        sh = draw.cruise_ship(3.6).move_to([2.6, -0.3, 0])
        nxt = tx("Next: Part 36, Software", 26, BRAND, bold=True).move_to([0, -2.6, 0])
        with self.voiceover("A hotel and a ship. Next time, Act Seven begins: software, a product that costs almost nothing "
                            "to copy, and the companies that sell it by the month."):
            self.play(LaggedStart(FadeIn(ht), FadeIn(sh), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
