from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Cracker(VoiceoverScene):
    def construct(self):
        card(self, 3, "The cracker", "What happens inside the furnace at the root of the plastics industry?",
             "Chapter three. The cracker.", lit=("make", "dollar"))
        self.inside()
        self.yields()
        self.cost()

    def inside(self):
        cu = draw.cracker_unit(6.0).move_to([1.4, -1.0, 0])
        e = draw.molecule("C2H6", bond=0.45).move_to([-5.6, 1.6, 0])
        steam = VGroup(*[Circle(0.08, stroke_width=0, fill_color="#C9D3E0", fill_opacity=0.6).move_to([-5.9 + 0.25 * k, 0.9, 0])
                         for k in range(5)])
        el = VGroup(tx("ethane", 16, GAS, bold=True), tx("+ steam", 14, GREY_A)).arrange(RIGHT, buff=0.15).next_to(e, UP, buff=0.15)
        prods = VGroup(draw.molecule("C2H4", bond=0.42), draw.molecule("H2", bond=0.42)).arrange(RIGHT, buff=0.6).move_to([4.6, 2.4, 0])
        pl = VGroup(tx("ethylene", 16, ETHYL, bold=True).next_to(prods[0], DOWN, buff=0.1),
                    tx("hydrogen", 16, GREY_A).next_to(prods[1], DOWN, buff=0.1))
        eq = tx("C2H6  →  C2H4  +  H2", 30, WHITE, bold=True).to_edge(UP, buff=0.4)
        notes = VGroup(tx("1. the furnace: tubes heated red hot,", 15, WHITE), tx("   the gas inside for a fraction of a second", 15, GREY_A),
                       tx("2. quench: cooled at once, so it cracks no further", 15, WHITE),
                       tx("3. compress and chill, and separate in tall columns", 15, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(LEFT, buff=0.4).shift(UP * 0.4)
        with self.voiceover(
            "Here is the plant this whole industry turns on. <bookmark mark='a'/> Ethane, or naphtha, is mixed with steam "
            "and sent through tubes inside a furnace, heated red hot. <bookmark mark='b'/> For a fraction of a second "
            "the molecules shake themselves apart. An ethane molecule loses two hydrogen atoms and becomes ethylene, "
            "with a double bond that makes it eager to join other molecules. <bookmark mark='c'/> The gas is cooled "
            "at once, so the cracking stops, then compressed, chilled, and separated in tall columns into ethylene, "
            "propylene, hydrogen, methane and the rest. <bookmark mark='d'/> A world-scale cracker is one of the largest "
            "and most expensive single machines in industry, and it runs flat out, day and night, for decades."
        ) as vo:
            self.play(FadeIn(cu), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(e, shift=RIGHT * 0.3), FadeIn(steam), FadeIn(el))
            self.play(e.animate.move_to(cu.box.get_center()).scale(0.6), steam.animate.move_to(cu.box.get_center()).set_opacity(0),
                      FadeOut(el), run_time=1.5)
            vo.wait_until("b")
            self.play(*[f.animate.scale(1.3) for f in cu.flames], Wiggle(e), run_time=1.2)
            self.play(ReplacementTransform(e, prods), FadeIn(pl), run_time=1.5)
            vo.wait_until("c")
            flow = VGroup(*[Dot(radius=0.07, color=ETHYL).move_to(cu[0].get_start()) for _ in range(6)])
            self.play(FadeIn(notes), LaggedStart(*[MoveAlongPath(d_, Line(cu[0].get_start(), cu[0].get_end()), rate_func=linear)
                                                   for d_ in flow], lag_ratio=0.25), run_time=2.0)
            self.play(FadeOut(flow), LaggedStart(*[Indicate(t_, color=ETHYL) for t_ in cu.towers], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("d")
            self.play(*[f.animate.scale(1 / 1.3) for f in cu.flames], run_time=1.0)
        self.clear_scene()

    def yields(self):
        C = R["cracker"]
        y = C["yields"]
        groups = [("ethylene", ["ethylene"], ETHYL), ("propylene", ["propylene"], "#9AD1F5"), ("butadiene, butylenes",
                                                                                               ["butadiene", "butylenes"], OIL),
                  ("aromatics", ["benzene", "toluene", "xylene", "aromatics"], SPEC),
                  ("fuel: methane, hydrogen", ["methane", "hydrogen"], GREY_B), ("fuel oil", ["fuel oil"], "#5D6B82")]
        bars = VGroup()
        for row, feed in enumerate(("ethane", "naphtha")):
            x = -4.4
            yy = 1.2 - 2.2 * row
            lab = tx(f"a tonne of {feed}", 20, GAS if feed == "ethane" else OIL, bold=True).move_to([-5.6, yy + 0.65, 0], aligned_edge=LEFT)
            segs = VGroup()
            for name, ks, col in groups:
                v = sum(y[feed][k] for k in ks)
                if v <= 0:
                    continue
                w = 9.6 * v
                r_ = Rectangle(width=w, height=0.75, stroke_color="#0E1117", stroke_width=1.5, fill_color=col,
                               fill_opacity=0.9).move_to([x + w / 2, yy, 0])
                t_ = tx(f"{100 * v:.0f}%", 14, "#0E1117", bold=True).move_to(r_) if w > 0.55 else VGroup()
                segs.add(VGroup(r_, t_))
                x += w
            bars.add(VGroup(lab, segs))
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9), tx(n, 13, GREY_A)).arrange(RIGHT, buff=0.08)
                       for n, _, c in groups]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.75)
        if key.width > 13:
            key.scale_to_fit_width(13)
        head = tx("What a tonne of feed becomes", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
        src = source("EIA, AEO2026 Industrial Demand Module assumptions, Table 6 (from the American Chemistry Council)", size=13)
        with self.voiceover(
            "What comes out depends on what goes in. <bookmark mark='a'/> Crack a tonne of ethane, and about "
            f"{100 * y['ethane']['ethylene']:.0f} per cent of it comes out as ethylene, by the government's engineering "
            "figures. Most of the rest is hydrogen and methane, burned as fuel. <bookmark mark='b'/> Crack a tonne of "
            f"naphtha, and only about {100 * y['naphtha']['ethylene']:.0f} per cent is ethylene. The rest is a little of "
            f"everything: propylene, about {100 * y['naphtha']['propylene']:.0f} per cent, butadiene for rubber, benzene "
            "and the other aromatics for fibres and resins, and fuel. <bookmark mark='c'/> So an ethane cracker is an "
            "ethylene machine, and a naphtha cracker is a supermarket: more complicated, more flexible, and, as we are "
            "about to see, usually dearer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in bars[0][1]], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in bars[1][1]], lag_ratio=0.15), run_time=2.2)
            vo.wait_until("c")
            c1 = tx("an ethylene machine", 18, ETHYL, bold=True).next_to(bars[0][1], DOWN, buff=0.2).align_to(bars[0][1], LEFT)
            c2 = tx("a supermarket of molecules", 18, OIL, bold=True).next_to(bars[1][1], DOWN, buff=0.2).align_to(bars[1][1], LEFT)
            self.play(Indicate(bars[0][1][0], color=ETHYL), FadeIn(c1, shift=UP * 0.1), run_time=1.0)
            self.play(FadeIn(c2, shift=UP * 0.1), run_time=1.0)
        self.clear_scene()

    def cost(self):
        C = R["cracker"]
        P = R["prices"]
        y = C["year"]
        scale = 4.4 / 1900
        base = -2.45
        panels = []
        for name, b, col, x0, feedcol in (("Texas, ethane", C["ethane"], TEXAS, -6.0, GAS),
                                          ("Europe, naphtha", C["naphtha"], EUROPE, 0.9, OIL)):
            steps = [("feed", b["feed"], feedcol), ("by-products sold", -b["credits"], GOOD), ("furnace fuel", b["fuel"], PRICE),
                     ("other cash", b["other"], COST)]
            level = 0.0
            bars, vals, labs, joins = VGroup(), VGroup(), VGroup(), VGroup()
            for k, (lab, v, c) in enumerate(steps + [("cash cost", None, col)]):
                xc = x0 + 0.5 + k * 1.2
                if v is None:
                    lo, hi = 0.0, level
                    r_ = Rectangle(width=0.85, height=max(hi * scale, 0.02), stroke_color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.35).move_to([xc, base, 0], aligned_edge=DOWN)
                    vt = tx(f"${level:,.0f}", 22, col, bold=True).next_to(r_, UP, buff=0.1)
                else:
                    lo, hi = sorted((level, level + v))
                    r_ = Rectangle(width=0.85, height=max((hi - lo) * scale, 0.02), stroke_width=0, fill_color=c,
                                   fill_opacity=0.9 if v > 0 else 0.45).move_to([xc, base + lo * scale, 0], aligned_edge=DOWN)
                    vt = tx(("+" if v > 0 else "-") + f"${abs(v):,.0f}", 14, c, bold=True).next_to(r_, UP, buff=0.08)
                    if k:
                        joins.add(DashedLine([xc - 1.2 + 0.425, base + level * scale, 0], [xc - 0.425, base + level * scale, 0],
                                             stroke_color=GREY_C, stroke_width=1.2, dash_length=0.06))
                    level += v
                lt = tx(lab, 12, GREY_A).move_to([xc, base - 0.25, 0])
                bars.add(r_)
                vals.add(vt)
                labs.add(lt)
            nm = tx(name, 20, col, bold=True).move_to([x0 + 0.5 + 2.4, base - 0.72, 0])
            panels.append((bars, vals, labs, joins, nm))
        axis = Line([-6.4, base, 0], [6.6, base, 0], stroke_color=GREY_D, stroke_width=1.5)
        head = tx(f"The cash cost of a tonne of ethylene, at {y} prices", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        pr = tx(f"{y}: US gas ${P['us'][y]:.2f}, European gas ${P['eu'][y]:.2f} per million Btu; Brent ${P['brent'][y]:.0f} a barrel",
                14, GREY_A).next_to(head, DOWN, buff=0.12)
        tag = estimate_tag("the Works (cracker.py): EIA's yields; feed, fuel and other prices assumed from gas and Brent",
                           corner=DR, size=12)
        src = source("IMF prices via FRED (annual averages)", size=13)
        with self.voiceover(
            f"Now the money, for a tonne of ethylene at {y}'s prices, in this series' model, drawn to one scale. "
            f"<bookmark mark='a'/> In Texas, the ethane for a tonne costs about {C['ethane']['feed']:,.0f} dollars. "
            f"Sell the hydrogen and methane, add the fuel the furnace burns and the other running costs, and a tonne "
            f"costs about {C['ethane']['cost']:,.0f} dollars. <bookmark mark='b'/> In Europe, on naphtha, the feed for a "
            f"tonne of ethylene costs about {C['naphtha']['feed']:,.0f} dollars, because it takes more than two and a half "
            "tonnes. The by-products are worth a great deal, and they bring most of it back. But the furnace burns "
            "European gas, and after everything a tonne costs about "
            f"{C['naphtha']['cost']:,.0f} dollars. <bookmark mark='c'/> The lesson of the cracker: the feedstock and the "
            "fuel are most of the cost, and the cheapest molecules win."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pr), FadeIn(tag), FadeIn(src), Create(axis), FadeIn(panels[0][4]), FadeIn(panels[1][4]))
            for m_, (bars, vals, labs, joins, nm) in zip("ab", panels):
                vo.wait_until(m_)
                for k in range(5):
                    anims = [GrowFromEdge(bars[k], UP if k == 1 else DOWN), FadeIn(vals[k]), FadeIn(labs[k])]
                    if 0 < k < 4:
                        anims.append(Create(joins[k - 1]))
                    self.play(*anims, run_time=0.7)
            vo.wait_until("c")
            self.play(Indicate(panels[0][1][4], color=TEXAS), Indicate(panels[1][1][4], color=EUROPE))
        self.clear_scene()
