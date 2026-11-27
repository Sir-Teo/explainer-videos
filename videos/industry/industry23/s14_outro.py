from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

MAC = "Macy's"


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U, D, O, L, F = R["run"]["choices"], R["turns"]["days"], R["offprice"], R["luxury"], R["fickle"]
        lines = [
            (f"the guess: in the Works, a base bought early and the hits chased late earns {100 * (U['chase']['profit'] / U['far']['profit'] - 1):.0f}% more", CHASE),
            (f"guess less: Inditex holds {D['Inditex']:.0f} days of stock, owes more than it holds, gross margin {R['hook']['gm']}%", FAST),
            (f"sell the mistakes: TJX's sales x{O['index']['TJX'][2026]:.1f} since 2015; Macy's x{O['index'][MAC][2026]:.1f}", OFF),
            (f"make too few: Hermès keeps {R['hook']['rms_margin']:.0f}c of each euro, and grows as its workshops do", LUX),
            (f"but taste turns: Gucci's sales fell from €{F['gucci'][2022][0] / 1e3:.1f}bn to €{F['gucci'][2025][0] / 1e3:.1f}bn in three years", BAD),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So how do two industries that sell clothes run on opposite rules? <bookmark mark='a'/> Both face the same "
             "problem: the clothes must be ordered before anyone knows what will sell, and every wrong guess ends in the "
             "sale. <bookmark mark='b'/> Fast fashion answers it with speed: buy a little early, make the hits again close "
             "to home, and hold little stock. <bookmark mark='c'/> The off-price shops answer it by buying everyone else's "
             "wrong guesses and selling them on. <bookmark mark='d'/> Luxury answers it with the wait: make fewer than "
             "people want, own the shops, never hold a sale. <bookmark mark='e'/> And all of them rest on contract "
             "factories they do not own, and on a taste that can turn in a season. Speed sells what people want now; the "
             "wait sells the wanting itself.",
             base=[head("Speed and the wait")], steps=list(g))

    def close(self):
        items = VGroup(draw.tshirt(1.0), draw.sneaker(1.4), draw.handbag(1.2, color=LEATHER), draw.price_tag("$40", 1.0),
                       draw.tshirt(1.0, color=LUX)).arrange(RIGHT, buff=0.5).move_to([0, 0.6, 0])
        nxt = tx("Next: Part 24, Construction", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("Clothes are cheap to make and expensive to guess: the whole industry, from the chain in Spain "
                            "to the workshop in Charente and the factory in Vietnam, is organised around that one fact. Next "
                            "time: construction, how the buildings and roads around us get built, and why it is so hard to "
                            "build them faster.") as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in items], lag_ratio=0.2), run_time=2)
            self.play(items.animate.scale(1.1), run_time=1.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
