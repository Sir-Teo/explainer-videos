from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, U, L, P, D = R["hook"]["ors"], R["run"], R["ltl"], R["parcels"], R["door"]
        lines = [
            (f"the price of a lane is set by the trip home: ${U['be_empty']:.2f} a loaded mile with one truck, about "
             f"${U['needed'][U['knx_empty'] / 100]:.2f} with a network", TRUCK),
            (f"own the road, and density pays: Union Pacific spent {H['Union Pacific'][2025]:.1f} cents per dollar in 2025", RAIL),
            (f"anyone can buy a truck: {R['hook']['carriers']:,.0f} firms, and margins of a few cents", TRUCK),
            (f"buildings are a moat: Old Dominion's {L['sc']:.0f} service centers", LTL),
            (f"the last mile is the dearest: ${D['city']:.2f} a parcel in the city, ${D['rural']:.2f} in the country (the Works)", PARCEL),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So why is one freight business a set of regional monopolies and the next a market of half a million firms? "
             "<bookmark mark='a'/> Because every freight business is about filling the trip, and the firm with the most "
             "freight in the most places fills it best. <bookmark mark='b'/> A railway owns its road, so traffic it adds "
             "costs little and nobody can lay a second track beside it. <bookmark mark='c'/> A truck uses the public road, "
             "so anyone can enter, and a boom fills the road with trucks. <bookmark mark='d'/> Buildings, the part-load "
             "carriers' service centers and the parcel hubs, are the trucker's version of track. "
             "<bookmark mark='e'/> And at the door, density decides everything.",
             base=[head("Who owns the road")], steps=list(g))

    def close(self):
        tr = draw.train(6, 0.9, kinds=("well", "hopper", "box"), colors=("#E8554E", "#B58CFF", "#7BD88F")).move_to([-2.2, 1.0, 0])
        s = draw.semi(2.4, cab_color=TRUCK).move_to([3.6, -0.4, 0])
        v = draw.van(1.4, color=PARCEL).move_to([-3.4, -0.6, 0])
        nxt = tx("Next: Part 30, Telecoms", 26, RAIL, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A train, a truck and a van, each filling its trip. Next time: telecoms, the companies that carry "
                            "everything and capture so little of what it is worth."):
            self.play(LaggedStart(FadeIn(tr), FadeIn(s), FadeIn(v), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
