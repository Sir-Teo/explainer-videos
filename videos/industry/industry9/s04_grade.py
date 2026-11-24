from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Grade(VoiceoverScene):
    def construct(self):
        card(self, 3, "Grade is destiny", "How much copper is in each tonne, and why does it decide everything?",
             "Chapter three. Grade is destiny.", lit=("make", "unit"))
        self.grid()
        self.rock()
        self.cost()
        self.escondida()

    def grid(self):
        cells = VGroup(*[Square(0.27, stroke_width=0.6, stroke_color="#1A1410", fill_color=ROCK, fill_opacity=1)
                         for _ in range(400)]).arrange_in_grid(rows=20, cols=20, buff=0)
        cells.move_to([-3.0, -0.2, 0])
        head = tx("400 tonnes of ore", 22, WHITE, bold=True).next_to(cells, UP, buff=0.2)
        tr = ValueTracker(3.0)
        order = np.random.default_rng(4).permutation(400)


        def paint_fast(g):
            n = int(round(tr.get_value() * 4))
            want = set(order[:n].tolist())
            for k, c in enumerate(g):
                c.set_fill(COPPER if k in want else ROCK)
        cells.add_updater(paint_fast)
        g_num = draw.number(lambda: tr.get_value(), decimals=2, suffix="% copper", size=40, color=COPPER)
        g_num.move_to([3.4, 1.4, 0])
        t_num = draw.number(lambda: tr.get_value() * 4, decimals=1, suffix=" tonnes of copper", size=30, color=WHITE)
        t_num.move_to([3.4, 0.5, 0])
        eras = VGroup(tx("3%: rich ore", 18, GREY_A), tx("1%: Escondida last year", 18, GREY_A),
                      tx("0.5%: the model deposit", 18, GREY_A), tx("0.21%: Freeport's leach pads in Arizona", 18, GREY_A))
        era_ys = [3.0, 1.02, 0.5, 0.21]
        era_pos = [-0.6, -1.1, -1.6, -2.1]
        for e, y in zip(eras, era_pos):
            e.move_to([3.4, y, 0])
        src = source("illustration; grades: BHP (Escondida, year to June 2025), Freeport-McMoRan 10-K for 2025", size=13)
        with self.voiceover(
            "Every square here is a tonne of rock, four hundred tonnes in all. Grade is the share of each tonne that is "
            "copper. <bookmark mark='a'/> At three percent, a very rich ore, twelve of the four hundred tonnes would be "
            "copper. <bookmark mark='b'/> At one percent, roughly what Escondida milled last year, four. "
            "<bookmark mark='c'/> At half a percent, the grade of our model deposit, two. <bookmark mark='d'/> And at "
            "zero point two one percent, the grade of the ore that Freeport stacks on its leach pads in Arizona and New "
            "Mexico, less than one. Not one copper square in four hundred. The rock is mostly rock, and the miner pays to "
            "dig, haul and grind every tonne of it."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(head), FadeIn(src), FadeIn(g_num), FadeIn(t_num))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(tr.animate.set_value(era_ys[k]), FadeIn(eras[k]), run_time=2.0)
                self.play(Indicate(eras[k], color=COPPER, scale_factor=1.05), run_time=0.8)
        cells.clear_updaters()
        g_num.clear_updaters()
        t_num.clear_updaters()
        self.clear_scene()

    def rock(self):
        G = R["grade"]
        grades = G["grades"]
        pa = viz.plot_axes([0, 1800], [-0.5, len(grades) - 0.5], x_length=8.6, y_length=4.6,
                           xticks=[0, 500, 1000, 1500], yticks=[], xfmt=lambda v: f"{v:,.0f} t", size=15,
                           grid=False).move_to([1.2, -0.4, 0])
        rows = VGroup()
        for k, (g, ore, tot) in enumerate(zip(grades, G["rock"], G["rock_strip"])):
            y = len(grades) - 1 - k
            p0 = pa.ax.c2p(0, y)
            w_ore = pa.ax.c2p(ore, y)[0] - p0[0]
            w_tot = pa.ax.c2p(tot, y)[0] - p0[0]
            waste = Rectangle(width=w_tot, height=0.5, stroke_width=0, fill_color="#5A4A3C", fill_opacity=1).move_to(
                [p0[0] + w_tot / 2, p0[1], 0])
            orebar = Rectangle(width=w_ore, height=0.5, stroke_width=0, fill_color="#A48464", fill_opacity=1).move_to(
                [p0[0] + w_ore / 2, p0[1], 0])
            lab = tx(f"{g:g}%", 20, COPPER, bold=True).next_to(p0, LEFT, buff=0.2)
            num = tx(f"{tot:,.0f} t", 16, WHITE).next_to(waste, RIGHT, buff=0.1)
            rows.add(VGroup(waste, orebar, lab, num))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color="#A48464", fill_opacity=1), tx("ore", 16, GREY_A)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color="#5A4A3C", fill_opacity=1),
                            tx("waste stripped to reach it (2 t per t of ore)", 16, GREY_A)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.05)
        head = tx("Rock moved for one tonne of copper, by grade", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
        tag = estimate_tag("computed: the Works (mine.py), 85% recovery", corner=DR, size=14)
        with self.voiceover(
            "Turn that around, and ask how much rock it takes to make one tonne of copper. <bookmark mark='a'/> At "
            f"three percent, about {G['rock'][0]:.0f} tonnes of ore, or {G['rock_strip'][0]:.0f} tonnes of rock once you "
            "count the waste you strip to reach it. <bookmark mark='b'/> At one percent, three times as much. At half a "
            f"percent, six times. <bookmark mark='c'/> At zero point two one percent, {G['rock_strip'][-1]:,.0f} tonnes "
            "of rock for a single tonne of copper. The rule is simple and brutal: halve the grade and you double the "
            "rock, and with it the diesel, the power, the water and the wear for every pound you sell."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(rows[0][0], LEFT), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2:]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[0], LEFT), GrowFromEdge(r_[1], LEFT),
                                                   FadeIn(r_[2:])) for r_ in rows[1:4]], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[0], LEFT), GrowFromEdge(r_[1], LEFT),
                                                   FadeIn(r_[2:])) for r_ in rows[4:]], lag_ratio=0.5), run_time=2.4)
            self.play(Indicate(rows[-1][3], color=COPPER))
        self.clear_scene()

    def cost(self):
        C = R["gradecost"]
        gs, cs, bes = C["grades"], C["cost"], C["breakeven"]
        pa = viz.plot_axes([0.2, 2.0], [0, 7], x_length=8.0, y_length=4.6, xticks=[0.25, 0.5, 1.0, 1.5, 2.0],
                           yticks=[1, 2, 3, 4, 5, 6], xfmt=lambda v: f"{v:g}%", yfmt=lambda v: f"${v:g}",
                           xlabel="copper in the ore", ylabel="dollars a pound", size=15).move_to([-1.2, -0.3, 0])
        cost_l = VMobject(stroke_color=COST, stroke_width=4).set_points_smoothly([pa.ax.c2p(g, c) for g, c in zip(gs, cs)])
        be_l = VMobject(stroke_color=PRICE, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(g, min(b, 7)) for g, b in zip(gs, bes) if b <= 7.2])
        tr = ValueTracker(2.0)

        def at(arr):
            return float(np.interp(tr.get_value(), gs, arr))
        dot_c = always_redraw(lambda: Dot(pa.ax.c2p(tr.get_value(), at(cs)), radius=0.08, color=COST))
        dot_b = always_redraw(lambda: Dot(pa.ax.c2p(tr.get_value(), min(at(bes), 7)), radius=0.08, color=PRICE))
        vline = always_redraw(lambda: DashedLine(pa.ax.c2p(tr.get_value(), 0), pa.ax.c2p(tr.get_value(), 7),
                                                 stroke_color=GREY_B, stroke_width=1.2))
        panel = VGroup(
            VGroup(tx("grade", 18, GREY_A), draw.number(lambda: tr.get_value(), 2, suffix="%", size=30, color=COPPER)
                   ).arrange(DOWN, buff=0.06),
            VGroup(tx("cash cost a pound", 18, COST), draw.number(lambda: at(cs), 2, prefix="$", size=30, color=COST)
                   ).arrange(DOWN, buff=0.06),
            VGroup(tx("price it needs to be worth building", 18, PRICE),
                   draw.number(lambda: at(bes), 2, prefix="$", size=30, color=PRICE)).arrange(DOWN, buff=0.06),
        ).arrange(DOWN, buff=0.45).move_to([4.9, -0.2, 0])
        lme = DashedLine(pa.ax.c2p(0.2, get("lme.copper.2025")), pa.ax.c2p(2.0, get("lme.copper.2025")),
                         stroke_color=WHITE, stroke_width=1.6)
        lme_l = tx(f"copper's 2025 average, ${get('lme.copper.2025'):.2f}", 15, WHITE).next_to(lme, UP, buff=0.06
                                                                                                ).align_to(lme, RIGHT)
        head = tx("The same mine, at other grades", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
        tag = estimate_tag("the Works' model mine (mine.py): 40 Mt a year, $3bn to build, 8% return", corner=DR, size=14)
        with self.voiceover(
            "Now put that into money. Take our model mine and change only the grade. <bookmark mark='a'/> The purple "
            "line is the cash cost of a pound of copper, and the gold line is the price the mine needs over its life to "
            "be worth building at all, once the three billion dollars of construction is paid back. "
            "<bookmark mark='b'/> At two percent, copper costs under a dollar a pound to produce, and the mine pays its "
            "way at about a dollar thirty. <bookmark mark='c'/> Slide down to one percent, and both rise slowly. "
            "<bookmark mark='d'/> Below half a percent they climb steeply, because the copper is shared out over ever "
            "more rock. <bookmark mark='e'/> The white line is what copper actually sold for on average in 2025. A "
            "deposit at a quarter of a percent is not worth building at that price, and a deposit at one percent is a "
            "fortune. The same hole, the same machines, the same people: grade decides which one you have."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cost_l), Create(be_l), run_time=2.0)
            self.add(vline, dot_c, dot_b)
            self.play(FadeIn(panel))
            vo.wait_until("b")
            self.play(Indicate(panel, scale_factor=1.03))
            vo.wait_until("c")
            self.play(tr.animate.set_value(1.0), run_time=3.0)
            vo.wait_until("d")
            self.play(tr.animate.set_value(0.25), run_time=4.0)
            vo.wait_until("e")
            self.play(Create(lme), FadeIn(lme_l))
            self.play(tr.animate.set_value(1.0), run_time=2.5)
        for m in panel:
            m[1].clear_updaters()
        self.clear_scene()

    def escondida(self):
        E = R["esc"]
        lo, hi = span("esc.output.2026")
        mill = draw.mill_drum(1.0).move_to([-4.6, 0.6, 0])
        mill.drum.add_updater(lambda m, dt: m.rotate(-1.2 * dt))
        feed = tx("same mills, about the same ore a year", 17, GREY_A).next_to(mill, DOWN, buff=0.3)
        g_tr = ValueTracker(E["grade25"])
        cu = draw.number(lambda: E["output"] * g_tr.get_value() / E["grade25"], 0, suffix=" kt of copper", size=34,
                         color=COPPER).move_to([-4.6, -1.9, 0])
        gl = VGroup(tx("copper in the ore fed to the mills", 16, GREY_A),
                    draw.number(lambda: g_tr.get_value(), 2, suffix="%", size=34, color=WHITE)).arrange(
            DOWN, buff=0.08).move_to([-4.6, 2.5, 0])
        lab = tx("if nothing else changed", 15, GREY_B).next_to(cu, DOWN, buff=0.12)
        rows = [("year to June 2025", f"{E['grade25']:.2f}%", f"{E['output']:,.0f} kt", f"${E['unit_cost']:.2f}"),
                ("year to June 2026 (BHP's guidance)", f"{E['grade26']:.2f}%", f"{lo:,.0f}-{hi:,.0f} kt",
                 f"${span('esc.cost.2026')[0]:.2f}-{span('esc.cost.2026')[1]:.2f}"),
                ("2027-2031, a year (BHP's outlook)", "", f"{span('esc.medium')[0]:,.0f}-{span('esc.medium')[1]:,.0f} kt",
                 f"${span('esc.cost.medium')[0]:.2f}-{span('esc.cost.medium')[1]:.2f}")]
        hdr = VGroup(tx("Escondida", 22, COPPER, bold=True), tx("grade", 17, GREY_A), tx("copper", 17, GREY_A),
                     tx("cost a pound", 17, GREY_A))
        table = VGroup(hdr)
        for r_ in rows:
            table.add(VGroup(*[tx(c, 17, WHITE if i else GREY_A, bold=bool(i)) for i, c in enumerate(r_)]))
        xs = [-0.6, 2.6, 4.1, 5.8]
        for k, row_ in enumerate(table):
            for x, c in zip(xs, row_):
                c.move_to([x, 1.4 - 0.75 * k, 0])
            row_[0].move_to([xs[0], 1.4 - 0.75 * k, 0])
            row_[0].align_to([xs[0] - 1.9, 0, 0], LEFT)
        rule = Line([-2.5, 1.05, 0], [6.8, 1.05, 0], stroke_color=GREY_B, stroke_width=1)
        note = tx("Grade falls 17%; output and cost follow it.", 22, STATE, bold=True).move_to([2.1, -2.2, 0])
        src = source("BHP, results for the year to June 2025 (actuals, guidance and medium-term outlook)", size=13)
        with self.voiceover(
            "This is happening right now at Escondida. <bookmark mark='a'/> In the year to June 2025, the ore going into "
            f"its concentrators held {E['grade25']:.2f} percent copper. This year BHP expects about "
            f"{E['grade26']:.2f}. <bookmark mark='b'/> The mills grind roughly the same tonnage, so if nothing else "
            "changed, the copper would fall with the grade, by about a sixth. <bookmark mark='c'/> BHP's own guidance "
            f"says the same: between {lo:,.0f} and {hi:,.0f} thousand tonnes this year, and nine hundred thousand to a "
            "million a year after that. And because the mine still moves and grinds all that rock, the cost of each "
            f"pound rises, from {say_money(E['unit_cost'])} last year to between a dollar fifty and a dollar eighty. "
            "<bookmark mark='d'/> This is the treadmill every miner runs on. The best rock goes first, the grade falls "
            "every year, and the company must find new ore, or new ways to process old ore, just to stand still."
        ) as vo:
            self.play(FadeIn(mill), FadeIn(feed), FadeIn(gl), FadeIn(cu), FadeIn(lab), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(table[0]), Create(rule), FadeIn(table[1]))
            self.play(g_tr.animate.set_value(E["grade26"]), FadeIn(table[2][:2]), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(cu, color=STATE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(table[2][2:]))
            self.play(FadeIn(table[3]))
            vo.wait_until("d")
            self.play(FadeIn(note, shift=UP * 0.1))
        mill.drum.clear_updaters()
        cu.clear_updaters()
        gl[1].clear_updaters()
        self.clear_scene()
