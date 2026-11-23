from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

RT = np.array([0.866, 0.5, 0.0])   # isometric: back-right
LT = np.array([-0.866, 0.5, 0.0])  # back-left
UPV = np.array([0.0, 1.0, 0.0])


def iso_cube(L: float, origin, color=FIXED) -> VGroup:
    """A cube of side ``L`` (inches) in isometric view, its front-bottom corner at ``origin``."""
    o = np.array(origin, dtype=float)
    right = Polygon(o, o + RT * L, o + RT * L + UPV * L, o + UPV * L, stroke_color="#0E1117", stroke_width=2,
                    fill_color=interpolate_color(ManimColor(color), ManimColor("#000000"), 0.35), fill_opacity=1)
    left = Polygon(o, o + LT * L, o + LT * L + UPV * L, o + UPV * L, stroke_color="#0E1117", stroke_width=2,
                   fill_color=interpolate_color(ManimColor(color), ManimColor("#000000"), 0.15), fill_opacity=1)
    top = Polygon(o + UPV * L, o + UPV * L + RT * L, o + UPV * L + RT * L + LT * L, o + UPV * L + LT * L,
                  stroke_color="#0E1117", stroke_width=2, fill_color=color, fill_opacity=1)
    return VGroup(left, right, top)


class Scale(VoiceoverScene):
    def construct(self):
        card(self, 4, "Bigger is cheaper", "Why does a big plant make things more cheaply, and where does that stop?",
             "Chapter four. Bigger is cheaper.", lit=("make", "dollar"))
        self.tank()
        self.pairs()
        self.mes()

    # --- the tank: surface against volume --------------------------------------------------------------------------
    def tank(self):
        L = ValueTracker(1.0)
        s = 1.25
        org = np.array([-3.6, -2.6, 0])
        cube = always_redraw(lambda: iso_cube(s * L.get_value(), org, color=FIXED))
        small = iso_cube(s, org + LEFT * 0.0, color=FIXED).set_opacity(0.0)
        lab = tx("a storage tank", 22, GREY_B).move_to([-3.6, 3.2, 0])
        rows = VGroup()
        specs = [("side", lambda: L.get_value(), GREY_A), ("steel in its walls", lambda: L.get_value() ** 2, VAR),
                 ("what it holds", lambda: L.get_value() ** 3, PROFIT),
                 ("steel per gallon held", lambda: 1 / L.get_value(), PRICE)]
        for k, (name, fn, col) in enumerate(specs):
            y = 1.9 - 0.95 * k
            t = tx(name, 22, col).move_to([1.2, y, 0], aligned_edge=LEFT)
            n = draw.number(fn, 2, prefix="×", size=36, color=col)
            n.add_updater(lambda m, y=y: m.move_to([6.4, y, 0], aligned_edge=RIGHT), call_updater=True)
            rows.add(VGroup(t, n))
        law = MathTex(r"\text{steel} \propto L^2,\quad \text{volume} \propto L^3", font_size=36).move_to([3.7, -2.25, 0])
        law2 = MathTex(r"\frac{\text{steel}}{\text{volume}} \propto \frac{1}{L}", font_size=40, color=PRICE).move_to(
            [3.7, -3.15, 0])
        with self.voiceover(
            "The first reason big is cheap is geometry. <bookmark mark='a'/> Take a tank. What it costs to build "
            "is mostly the steel in its walls, which grows with its surface. What it is worth is what it holds, "
            "which grows with its volume. <bookmark mark='b'/> Double every side. The walls take four times the "
            "steel; the tank holds eight times as much. <bookmark mark='c'/> So each gallon of storage needs half "
            "the steel. Pipes, boilers, ships, furnaces and aircraft fuselages all follow the same arithmetic: the "
            "container grows with the square, what it contains with the cube."
        ) as vo:
            self.play(FadeIn(lab), FadeIn(cube), FadeIn(small))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.2), Write(law), run_time=2.0)
            vo.wait_until("b")
            self.play(L.animate.set_value(2.0), run_time=4.0, rate_func=smooth)
            vo.wait_until("c")
            self.play(Write(law2), Indicate(rows[3], color=PRICE))
        rule = MathTex(r"\text{cost} \propto \text{capacity}^{0.6}", font_size=44, color=WHITE).to_edge(UP, buff=0.45)
        st = dict(R["scale"]["six_tenths"])
        ax = CornerAxes(x_range=[0, 4.6, 1], y_range=[0, 150, 50], x_length=7.2, y_length=3.9,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([0.3, -0.75, 0])
        caps = [0.5, 1, 2, 4, 8]
        bars = VGroup()
        for k, c in enumerate(caps):
            v = st[c] / c
            b = Rectangle(width=0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=FIXED,
                          fill_opacity=0.9).move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN)
            b.add(tx(f"{v:.0f}", 20, WHITE, bold=True).next_to(b, UP, buff=0.08))
            b.add(tx(f"×{c:g}", 18, GREY_B).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.1))
            bars.add(b)
        xl = tx("plant size (×, against a standard plant)", 18, GREY_B).next_to(ax, DOWN, buff=0.5)
        yl = tx("cost per unit of capacity (standard plant = 100)", 18, GREY_B).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        tag = estimate_tag("the six-tenths rule: an engineers' rule of thumb", corner=DR)
        with self.voiceover(
            "Engineers who price chemical plants and refineries boil this down to a rule of thumb. "
            "<bookmark mark='a'/> A plant's cost rises with its capacity to roughly the power six-tenths. "
            "<bookmark mark='b'/> Double the size and the bill goes up only about half, so each unit of capacity "
            "costs about a quarter less. Double again, and again. A plant eight times the standard size costs about "
            "three and a half times as much to build, and less than half as much per unit of capacity. "
            "<bookmark mark='c'/> It is a rule of thumb, not a law: real exponents run from about a half to nearly "
            "one, and that is exactly where things get interesting."
        ) as vo:
            self.play(*[FadeOut(m) for m in (cube, small, rows, law, law2, lab)])
            self.remove(cube)
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(rule))
        for r_ in rows:
            r_[1].clear_updaters()
        self.clear_scene()

    # --- three pairs of real machines ----------------------------------------------------------------------------
    def pairs(self):
        P = R["scale"]["pairs"]
        keys = ["gas_ct", "gas_cc", "nuclear"]
        head = tx("Same machine, two sizes: cost to build per kilowatt", 28, bold=True).to_edge(UP, buff=0.3)
        rows = VGroup()
        for k, ((name, s1, c1, s2, c2), key) in enumerate(zip(P, keys)):
            y = 1.95 - 2.1 * k
            nm = tx(name, 22, TECH[key], bold=True).move_to([-6.8, y + 0.9, 0], aligned_edge=LEFT)
            i1 = icon(key, min(0.95 * (s1 / 400) ** 0.5 + 0.3, 1.35)).move_to([-5.7, y - 0.7, 0], aligned_edge=DOWN)
            i2 = icon(key, min(0.95 * (s2 / 400) ** 0.5 + 0.3, 1.35)).move_to([-3.7, y - 0.7, 0], aligned_edge=DOWN)
            m1 = tx(f"{s1:,} MW", 17, GREY_B).next_to(i1, DOWN, buff=0.08)
            m2 = tx(f"{s2:,} MW", 17, GREY_B).next_to(i2, DOWN, buff=0.08)
            full = 5.0
            b1 = Rectangle(width=full, height=0.36, stroke_width=0, fill_color=TECH[key], fill_opacity=0.45).move_to(
                [-1.9, y + 0.2, 0], aligned_edge=LEFT)
            b2 = Rectangle(width=full * c2 / c1, height=0.36, stroke_width=0, fill_color=TECH[key],
                           fill_opacity=0.95).move_to([-1.9, y - 0.35, 0], aligned_edge=LEFT)
            v1 = tx(f"${c1:,}", 19, GREY_A).next_to(b1, RIGHT, buff=0.12)
            v2 = tx(f"${c2:,}", 19, WHITE, bold=True).next_to(b2, RIGHT, buff=0.12)
            cut = tx(f"{100 * (1 - c2 / c1):.0f}% less", 22, PROFIT, bold=True).move_to([5.9, y - 0.07, 0])
            rows.add(VGroup(nm, i1, i2, m1, m2, b1, b2, v1, v2, cut))
        src = source("EIA, Assumptions to the Annual Energy Outlook 2026, Electricity Market Module, Table 3")
        with self.voiceover(
            "Here is the rule in real machines, from the costs the US Energy Information Administration uses for new "
            "power plants. <bookmark mark='a'/> A gas turbine of the kind adapted from a jet engine, about two "
            "hundred megawatts, costs about two thousand three hundred dollars per kilowatt to build. An industrial "
            "frame turbine twice the size costs about half as much per kilowatt. Part of that is size and part is "
            "design: the small one starts in minutes and suits a plant that runs rarely. <bookmark mark='b'/> A "
            "combined-cycle gas plant of six hundred megawatts against one of twelve hundred: only five percent "
            "cheaper per kilowatt. At that size, most of the gains from scale have already been taken. "
            "<bookmark mark='c'/> And nuclear: a small modular reactor of four hundred and eighty megawatts, against "
            "a large plant of over two thousand. The small one costs about a fifth more per kilowatt. "
            "Its makers' bet is that building many identical small units in a factory will bring the cost down the "
            "learning curve faster than scale brings the large ones down. That is the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark in enumerate("abc"):
                vo.wait_until(mark)
                rw = rows[k]
                self.play(FadeIn(rw[0]), FadeIn(rw[1], shift=UP * 0.1), FadeIn(rw[2], shift=UP * 0.1), FadeIn(rw[3]),
                          FadeIn(rw[4]))
                self.play(GrowFromEdge(rw[5], LEFT), FadeIn(rw[7]))
                self.play(GrowFromEdge(rw[6], LEFT), FadeIn(rw[8]), FadeIn(rw[9], shift=LEFT * 0.2))
        self.clear_scene()

    # --- minimum efficient scale against the size of the market ------------------------------------------------------
    def mes(self):
        ax = CornerAxes(x_range=[0, 10, 1], y_range=[0, 3.2, 1], x_length=6.0, y_length=3.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-3.3, 0.65, 0])

        def lrac(q):
            return 1.0 + 1.6 * max(0.0, (2.0 - q) / 2.0) ** 2 if q < 2.0 else 1.0 + 0.012 * (q - 2.0)
        curve = ax.plot(lrac, x_range=[0.35, 9.8, 0.05], color=FIXED, stroke_width=4)
        mes_line = DashedLine(ax.c2p(2.0, 0), ax.c2p(2.0, 2.4), stroke_color=PRICE, stroke_width=2)
        mes_t = tx("minimum efficient scale", 18, PRICE).next_to(ax.c2p(2.0, 2.4), UP, buff=0.08)
        xl = tx("size of one plant", 18, GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = tx("cost per unit", 18, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        flat = tx("then the curve flattens", 17, GREY_B).next_to(ax.c2p(6.5, 1.06), UP, buff=0.1)

        market = ValueTracker(10.0)
        box_y = -2.75
        unit_w = 1.15

        def market_box():
            w = unit_w * market.get_value()
            return RoundedRectangle(corner_radius=0.08, width=w, height=1.0, stroke_color=GREY_A, stroke_width=2,
                                    fill_color="#141A24", fill_opacity=1).move_to([-6.6, box_y, 0], aligned_edge=LEFT)
        box = always_redraw(market_box)

        def plants():
            n = int(market.get_value() // 1)
            g = VGroup()
            for i in range(n):
                f = draw.factory(0.95).move_to([-6.6 + unit_w * (i + 0.5), box_y, 0])
                g.add(f)
            return g
        fleet = always_redraw(plants)
        box_t = tx("the whole market, in plants of minimum efficient size", 18, GREY_B).move_to([-1.5, -1.95, 0])
        nfirms = draw.number(lambda: int(market.get_value() // 1), 0, size=40, color=PROFIT)
        nfirms.add_updater(lambda m: m.move_to([4.6, 0.9, 0]), call_updater=True)
        nf_t = tx("plants the market can hold\nat the lowest cost", 18, GREY_B).move_to([4.6, 0.0, 0])
        tag = estimate_tag("illustrative", corner=DR)
        with self.voiceover(
            "Where does scale stop? <bookmark mark='a'/> In most industries the cost per unit falls steeply at "
            "first, then flattens. The size at which it stops falling much is called the minimum efficient scale. "
            "Beyond it, a bigger plant is not much cheaper, and it gets harder to manage and to ship from. "
            "<bookmark mark='b'/> The number that matters is that scale against the size of the market. If the "
            "market can absorb ten plants of efficient size, ten companies can each run one and compete. "
            "<bookmark mark='c'/> Shrink the market, or grow the efficient plant, and the number of firms that fit "
            "falls. At three there is room for a few rivals who watch one another. <bookmark mark='d'/> At one, a "
            "single firm can serve everybody more cheaply than two could: economists call that a natural monopoly, "
            "and it is why your town has one water main and one set of power lines."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), run_time=2.0)
            self.play(Create(mes_line), FadeIn(mes_t), FadeIn(flat))
            vo.wait_until("b")
            self.play(FadeIn(box), FadeIn(box_t), FadeIn(nfirms), FadeIn(nf_t))
            first = plants()
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.15) for f in first], lag_ratio=0.08), run_time=1.5)
            self.remove(first)
            self.add(fleet)
            vo.wait_until("c")
            self.play(market.animate.set_value(3.4), run_time=3.0)
            vo.wait_until("d")
            self.play(market.animate.set_value(1.3), run_time=2.0)
        lesson = tx("Scale decides how many firms an industry has room for.", 26, PRICE, bold=True).to_edge(DOWN,
                                                                                                         buff=0.25)
        with self.voiceover(
            "So scale does more than lower costs. It decides how many firms an industry has room for, and that, as "
            "the next part will show, goes a long way to deciding how much they earn."
        ):
            self.play(FadeOut(box_t), FadeIn(lesson, shift=UP * 0.1))
        nfirms.clear_updaters()
        self.clear_scene()
