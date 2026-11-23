from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        B = [b for b in R["fleet"]["blocks"] if b["key"] != "oil"]
        total = sum(b["gw"] for b in B)
        W = 12.6
        y_cap, y_gen = 1.1, -1.6
        head = tx("Intermission: what America's power plants could make, and what they made, in 2025", 24).to_edge(
            UP, buff=0.35)
        caps, gens, labs = VGroup(), VGroup(), VGroup()
        x = -W / 2
        for b in B:
            w = W * b["gw"] / total
            r_ = Rectangle(width=w, height=1.3, stroke_color="#0E1117", stroke_width=2, fill_color=TECH[b["key"]],
                           fill_opacity=0.9).move_to([x + w / 2, y_cap, 0])
            caps.add(r_)
            g = Rectangle(width=w * b["cf"], height=1.3, stroke_color="#0E1117", stroke_width=2,
                          fill_color=TECH[b["key"]], fill_opacity=0.9).move_to([x + w * b["cf"] / 2, y_gen, 0])
            gens.add(g)
            ic = icon(b["key"], 0.4).next_to(r_, UP, buff=0.12)
            if ic.width > w * 0.95:
                ic.scale_to_fit_width(w * 0.95)
            cf = tx(f"{100 * b['cf']:.0f}%", 18, TECH[b["key"]], bold=True).move_to([x + w / 2, y_gen - 0.95, 0])
            labs.add(VGroup(ic, cf))
            x += w
        cap_t = tx("capacity: what the plants could make running all year", 19, GREY_B).next_to(caps, DOWN, buff=0.15)
        gen_t = tx("what each actually made, as a share of what it could (its capacity factor)", 19, GREY_B).move_to(
            [0, y_gen - 1.45, 0])
        src = source("EIA, Electric Power Annual 2025, tables 4.3 and 4.8 (oil left out; it ran 5% of the time)")
        nuc = next(i for i, b in enumerate(B) if b["key"] == "nuclear")
        sol = next(i for i, b in enumerate(B) if b["key"] == "solar")
        ct = next(i for i, b in enumerate(B) if b["key"] == "gas_ct")
        with self.voiceover(
            "An intermission, and a picture of chapter three in a whole industry. <bookmark mark='a'/> Each block is "
            "one kind of power plant in America, as wide as its capacity: what it could make if it ran every hour "
            "of 2025. <bookmark mark='b'/> Now squeeze each block down to what it actually made. "
            "<bookmark mark='c'/> The reactors barely shrink: they ran ninety-one percent of the time. "
            "<bookmark mark='d'/> Solar shrinks to a quarter, because the sun sets. <bookmark mark='e'/> And the gas "
            "turbines that wait for the peak shrink to a sliver. Every one of those idle megawatts was paid for. "
            "Somebody has to cover the cost of a plant that runs one hour in seven, and the next chapters show who."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, LEFT) for r_ in caps], lag_ratio=0.12),
                      LaggedStart(*[FadeIn(l_[0]) for l_ in labs], lag_ratio=0.12), FadeIn(cap_t), run_time=2.5)
            vo.wait_until("b")
            ghosts = caps.copy().set_fill(opacity=0.15).move_to([0, y_gen, 0])
            self.play(FadeIn(ghosts))
            self.play(LaggedStart(*[ReplacementTransform(caps[i].copy(), gens[i]) for i in range(len(B))],
                                  lag_ratio=0.15), run_time=4.0)
            self.play(LaggedStart(*[FadeIn(l_[1]) for l_ in labs], lag_ratio=0.1), FadeIn(gen_t))
            vo.wait_until("c")
            self.play(Indicate(gens[nuc], color=WHITE, scale_factor=1.06))
            vo.wait_until("d")
            self.play(Indicate(gens[sol], color=WHITE, scale_factor=1.1))
            vo.wait_until("e")
            self.play(Indicate(gens[ct], color=WHITE, scale_factor=1.4))
        self.clear_scene()
        self.story()

    def story(self):
        so = VGroup(tx("The story so far", 36, PRICE, bold=True),
                    tx("A decision should weigh what it changes: the cost of one more, not the average.", 24),
                    tx("Whether a cost is fixed depends on how far ahead you look; sunk costs never count.", 24),
                    tx("The more a business pays up front, the more it needs to run full.", 24),
                    tx("Size, a second product and a full street all make each unit cheaper,", 24),
                    tx("and so does experience: about 20 to 30% off with every doubling.", 24),
                    tx("Next: what that does to an airline, a power market and a chip maker.", 21, GREY_B)
                    ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The story so far. A decision should weigh what it changes: the cost of one more, not the average. "
            "Whether a cost is fixed depends on how far ahead you look, and costs already sunk never count. The more "
            "a business pays up front, the more it needs to run full. Size, a second product and a full street all "
            "make each unit cheaper, and so does experience: twenty or thirty percent off with every doubling. Next: "
            "what all that does to an airline, a power market and a chip maker."
        ):
            self.play(LaggedStart(*[FadeIn(x_, shift=UP * 0.1) for x_ in so], lag_ratio=0.5), run_time=5)
        self.clear_scene()
