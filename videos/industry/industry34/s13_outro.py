from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U, Ct, Sp = R["run"], R["contract"], R["split"]
        lines = [
            (f"the franchisee owns the kitchen, hires the crew and keeps about {100 * U['base']['margin']:.0f} cents a dollar", OP),
            (f"the franchisor collects about {100 * Ct['take']:.0f} cents of every franchised dollar, most of it as rent", FR),
            (f"and keeps {100 * Sp['fr_margin']:.0f} cents of each dollar it collects, on restaurants it did not pay to build", GOOD),
            ("wages, a fall in sales or a shift to the apps can take most of the owner's margin", BAD),
            ("the fee is bounded by what it takes to persuade the next owner to open", MASTER),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So who owns a fast-food restaurant, and who makes the money? <bookmark mark='a'/> Usually a local owner, who "
             "paid for the kitchen, hires the crew and keeps a few cents of each dollar. <bookmark mark='b'/> The brand "
             "collects about thirteen cents of every franchised dollar, most of it as rent, <bookmark mark='c'/> and keeps "
             "most of that, on restaurants it did not build. <bookmark mark='d'/> The owner carries the risk of wages, bad "
             "years and the apps. <bookmark mark='e'/> And the brand's fee is limited only by its need for the next owner. "
             "McDonald's is a landlord with a menu.",
             base=[head("A landlord with a menu")], steps=list(g))

    def close(self):
        rs = draw.restaurant(3.4).move_to([-2.4, 0.3, 0])
        bg = draw.burger(1.4).move_to([2.8, 0.2, 0])
        nxt = tx("Next: Part 35, Travel and Hotels", 26, FR, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A restaurant and a burger. Next time: travel and hotels, where the brand on the building is "
                            "often not the owner either."):
            self.play(LaggedStart(FadeIn(rs), FadeIn(bg), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
