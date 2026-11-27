from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U, P, K, F = R["run"]["choices"], R["productivity"], R["carillion"], R["concession"]
        lines = [
            (f"the bid: add 8% like the rivals and keep {100 * U['0.08']['margin']:.1f}%; the lowest estimate wins (the Works)", PRICE),
            ("the contract: fixed prices put the estimate's error on the builder; Fluor now takes 81% cost-reimbursable", MAKE),
            (f"the cash: paid first, pay later, until the wins stop; Carillion lost £{K['cash']:.0f}m of cash in 2017", BAD),
            (f"the output: per worker x{P['per']['construction'][2025]:.2f} since 1970, prices x{P['price']['construction'][2025]:.0f}", BUILD),
            (f"the way out: own something; Ferrovial's roads keep {100 * F['hwy'][1] / F['hwy'][0]:.0f}%, its building {100 * F['con'][1] / F['con'][0]:.0f}%", GOOD),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So why has almost everything become cheaper to make, except a building? <bookmark mark='a'/> Because a "
             "building is sold before it is designed, by sealed bid, and the lowest bid is usually the most optimistic "
             "estimate, so builders keep a few cents of each dollar and cannot afford to experiment. "
             "<bookmark mark='b'/> Because the risk of a wrong estimate sits with whoever signs the fixed price, and the "
             "builders have learned to avoid it. <bookmark mark='c'/> Because the business runs on other people's cash, "
             "which flatters a growing contractor and sinks a shrinking one. <bookmark mark='d'/> Because every site is "
             "a prototype, and the output per worker has gone backwards for half a century while prices rose nineteen-fold. "
             "<bookmark mark='e'/> And because the money is with whoever owns the quarry, the crane or the road, not with "
             "whoever does the building.",
             base=[head("Every building a prototype")], steps=list(g))

    def close(self):
        frame = draw.skyscraper_frame(floors=24, w=1.3, floor_h=0.13).move_to([-3.6, -0.6, 0])
        crane = draw.tower_crane(1.5).move_to([-1.4, 0.3, 0])
        brg = draw.bridge(4.0).move_to([3.2, -0.6, 0])
        nxt = tx("Next: Part 25, Homes", 26, PRICE, bold=True).move_to([0, -2.8, 0])
        with self.voiceover("A building is still made the way the Empire State Building was: once, on one plot, by a crowd of "
                            "firms that each bid for their slice. Next time: homes, the largest thing most people ever buy.") as vo:
            self.play(LaggedStart(*[FadeIn(f) for f in frame.floors], lag_ratio=0.05), FadeIn(frame[0]), run_time=2)
            self.play(FadeIn(crane), FadeIn(brg), run_time=1.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
