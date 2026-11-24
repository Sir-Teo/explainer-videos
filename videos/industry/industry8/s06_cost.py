from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Cost(VoiceoverScene):
    def construct(self):
        card(self, 5, "What a barrel costs", "Three dollars or sixty-six: which is the cost of oil?",
             "Chapter five. What a barrel costs.", lit=("make", "dollar"))
        self.ladder()
        self.margin()

    def ladder(self):
        C = R["cost"]
        S = R["shock"]
        u = 0.075  # inches per dollar
        x0 = -2.2
        rows = [("Saudi Aramco: lifting", [(C["lifting"], GAS)], "per barrel, 2025, excluding royalty and depreciation"),
                ("Saudi Aramco: lifting + capital", [(C["lifting"], GAS), (C["capex"], "#4FA36A")],
                 "capital spending per barrel produced, 2025"),
                ("US shale: keep existing wells", [(C["dallas_existing"], SHALE)], "Dallas Fed survey, March 2026"),
                ("US shale: drill a new well", [(C["dallas_new"], STATE)],
                 f"Permian ${C['dallas_permian']:.0f}; large firms ${C['dallas_large']:.0f}")]
        bars = VGroup()
        for k, (name, segs, note) in enumerate(rows):
            y = 2.0 - 1.05 * k
            lab = tx(name, 19, WHITE, bold=True).move_to([x0 - 0.25, y + 0.05, 0], aligned_edge=RIGHT)
            nt = tx(note, 13, GREY_B).next_to(lab, DOWN, buff=0.05).align_to(lab, RIGHT)
            g = VGroup()
            x = x0
            for v, col in segs:
                b = Rectangle(width=v * u, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to(
                    [x, y, 0], aligned_edge=LEFT)
                g.add(b)
                x += v * u
            tot = sum(v for v, _ in segs)
            val = tx(f"${tot:.2f}" if tot < 10 else f"${tot:.0f}" if k else f"${tot:.2f}", 20, WHITE, bold=True).next_to(
                g, RIGHT, buff=0.15)
            bars.add(VGroup(lab, nt, g, val))
        axis = Line([x0, 2.6, 0], [x0, -1.6, 0], stroke_color=GREY_B, stroke_width=1.5)
        price_lines = VGroup()
        for v, lab, col in ((S["brent_2025"], "Brent, 2025: $69", BRENT), (S["brent_oct"], "Brent, Oct 2026: $124", PRICE)):
            x = x0 + v * u
            if x > 6.9:
                x = 6.9
            ln = DashedLine([x, 2.6, 0], [x, -1.7, 0], stroke_color=col, stroke_width=2)
            t = tx(lab, 15, col).next_to(ln, DOWN, buff=0.08)
            price_lines.add(VGroup(ln, t))
        note = tx("Brent, Oct 2026: $124, off the scale", 15, PRICE).move_to([5.4, -2.2, 0])
        src = source("Saudi Aramco, Annual Report 2025; Federal Reserve Bank of Dallas, Energy Survey, Q1 2026; Brent (EIA)",
                     size=13)
        with self.voiceover(
            "What does a barrel of oil cost? It depends whose, and what you count. <bookmark mark='a'/> Saudi Aramco, "
            "the state oil company of Saudi Arabia, reports what it costs to lift a barrel out of its fields: "
            f"{C['lifting']:.2f} dollars in 2025. <bookmark mark='b'/> Add what it spends on new wells and plant, "
            f"another {C['capex']:.0f} dollars a barrel, and it is still under twelve. <bookmark mark='c'/> Every year "
            "the Federal Reserve Bank of Dallas asks American oil executives two questions. What price do you need to "
            f"keep your existing wells running? This spring, on average, {C['dallas_existing']:.0f} dollars. "
            f"<bookmark mark='d'/> And what price do you need to drill a new well and make money on it? "
            f"{C['dallas_new']:.0f} dollars; in the Permian Basin of Texas and New Mexico, {C['dallas_permian']:.0f}. "
            "<bookmark mark='e'/> Brent averaged sixty-nine dollars in 2025. At that price, Saudi Arabia's barrels "
            "earned fortunes, and an American driller was close to the line on a new well."
        ) as vo:
            chead = tx("What a barrel costs, dollars", 24, WHITE, bold=True).to_edge(UP, buff=0.35)
            self.play(FadeIn(src), Create(axis), FadeIn(chead), FadeIn(bars[0][0]), FadeIn(bars[0][1]))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                g = bars[k]
                anims = [GrowFromEdge(b, LEFT) for b in g[2]] + [FadeIn(g[3])]
                if k:
                    anims += [FadeIn(g[0]), FadeIn(g[1])]
                self.play(*anims, run_time=1.1)
            vo.wait_until("e")
            self.play(Create(price_lines[0][0]), FadeIn(price_lines[0][1]))
            self.play(FadeIn(note))
        self.clear_scene()

    def margin(self):
        C = R["cost"]
        # a supply curve built from the two kinds of barrel: cheap ones first, then shale
        blocks = [("Gulf state fields", 30, 12, GAS), ("other conventional", 25, 35, "#4FA36A"),
                  ("deep water", 12, 48, BRENT), ("oil sands", 5, 55, CRUDE), ("US shale, new wells", 14, C["dallas_new"], STATE)]
        pa = viz.plot_axes([0, 90], [0, 100], x_length=9.0, y_length=4.2, xticks=[0, 30, 60, 90],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}m b/d", yfmt=lambda v: f"${v:g}", size=14)
        pa.move_to([0.4, -0.6, 0])
        x = 0
        rects = VGroup()
        for name, w, c, col in blocks:
            p0, p1 = pa.ax.c2p(x, 0), pa.ax.c2p(x + w, c)
            r_ = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color="#0E1117", stroke_width=1.5,
                           fill_color=col, fill_opacity=0.9).move_to((p0 + p1) / 2)
            t = tx(name, 13, WHITE).next_to(r_, UP, buff=0.06)
            rects.add(VGroup(r_, t))
            x += w
        demand = DashedLine(pa.ax.c2p(80, 0), pa.ax.c2p(80, 98), stroke_color=PRICE, stroke_width=2.5)
        dl = tx("what the world wants", 15, PRICE).next_to(demand, UP, buff=0.05)
        price = DashedLine(pa.ax.c2p(0, C["dallas_new"]), pa.ax.c2p(86, C["dallas_new"]), stroke_color=WHITE, stroke_width=2)
        pl = tx("the price must cover the last barrel needed", 16, WHITE, bold=True).next_to(price, UP, buff=0.08).align_to(
            price, LEFT).shift(RIGHT * 0.2)
        head = tx("Part 4's cost curve, for the world's oil", 22, WHITE, bold=True).to_edge(UP, buff=0.45)
        tag = estimate_tag("illustrative blocks; only the shale height is a survey figure", corner=DR, size=14)
        with self.voiceover(
            "Part 4 showed why both numbers matter. <bookmark mark='a'/> Line up the world's barrels from cheapest to "
            "dearest: the giant fields of the Gulf states first, then other conventional fields, deep water, oil "
            "sands, and last, the new American shale wells. <bookmark mark='b'/> When the world wants this much "
            "oil, the last barrel it needs is a shale barrel. <bookmark mark='c'/> So over the long run, the price "
            "has to cover that barrel's cost, or it will not be drilled. Everyone cheaper keeps the difference. That "
            "difference, between a three-dollar barrel and a sixty-dollar price, is one of the largest sources of "
            "money in the world, and the next chapter asks who gets it."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.15) for r_ in rects], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(demand), FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(price), FadeIn(pl))
            self.play(rects[0][0].animate.set_fill(opacity=1), Indicate(rects[0], color=WHITE, scale_factor=1.02))
        self.clear_scene()
