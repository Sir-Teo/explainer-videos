from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, C, K = R["hook"], R["cycle"], R["choke"]
        lines = [
            (f"nearly free: about {100 * H['per_pair'][2025]:.0f} cents to carry a pair of trainers across an ocean in 2025", GOOD),
            ("one box, one crane: the container made every port and every ship part of one machine", BOX),
            (f"never safe: ZIM's freight ${C['rate'][2019]:,.0f}, ${C['rate'][2022]:,.0f}, ${C['rate'][2023]:,.0f} a TEU in 2019, 2022, 2023", RATE),
            ("the boom builds the bust: ships ordered at the top arrive three years later", SHIP),
            (f"a few narrow places: Suez halved in 2024; Hormuz from {K['hormuz_2025']:.0f} ships a day to {K['hormuz_last']:.0f}", BAD),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So how did moving a tonne across an ocean become nearly free? <bookmark mark='a'/> Through enormous ships, slow "
             "and full, so that the voyage costs a pair of trainers pennies. <bookmark mark='b'/> Through one standard box "
             "that every crane, ship, train and lorry can take. And why do the companies swing between fortune and ruin? "
             "<bookmark mark='c'/> Because a full fleet can charge almost anything and a half-empty one almost nothing, "
             "<bookmark mark='d'/> because everyone orders ships at the same moment and they arrive years later, together, "
             "<bookmark mark='e'/> and because the whole system squeezes through a few narrow places, any of which can close. "
             "The cheapness and the violence are the same machine.",
             base=[head("Nearly free, and never safe")], steps=list(g))

    def close(self):
        vessel = draw.ship(3.4, boxes=18).move_to([-3.6, -0.2, 0])
        crane = draw.quay_crane(2.4).move_to([1.2, 0.2, 0])
        tk = draw.tanker(3.0).move_to([4.6, -0.6, 0])
        nxt = tx("Next: Part 28, Airlines", 26, RATE, bold=True).move_to([0, -2.6, 0])
        with self.voiceover("A ship, a crane and a tanker: the machine that made distance cheap. Next time, the industry that "
                            "made it fast, and has lost money over most of its history: airlines."):
            self.play(LaggedStart(FadeIn(vessel), FadeIn(crane), FadeIn(tk), lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(nxt))
        self.clear_scene()
