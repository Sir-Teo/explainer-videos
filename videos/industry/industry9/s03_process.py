from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


def crusher(w=1.0):
    jaw = Polygon([-0.5 * w, 0.5 * w, 0], [0.5 * w, 0.5 * w, 0], [0.15 * w, -0.3 * w, 0], [-0.15 * w, -0.3 * w, 0],
                  stroke_color="#C9D3E0", stroke_width=2, fill_color="#3E4553", fill_opacity=1)
    teeth = VGroup(*[Line([-0.4 * w + 0.07 * k * w, 0.4 * w - 0.08 * k * w, 0], [-0.3 * w + 0.07 * k * w,
                                                                                0.4 * w - 0.08 * k * w, 0],
                          stroke_color="#8C929B", stroke_width=2) for k in range(5)])
    return VGroup(jaw, teeth, VGroup(*[Dot([x * w, -0.42 * w, 0], radius=0.03 * w, color=ROCK)
                                       for x in (-0.08, 0, 0.08)]))


def furnace(w=1.2):
    body = RoundedRectangle(corner_radius=0.08, width=w, height=0.8 * w, stroke_color="#C9D3E0", stroke_width=2,
                            fill_color="#3E4553", fill_opacity=1)
    mouth = Rectangle(width=0.5 * w, height=0.22 * w, stroke_width=0, fill_color="#FF8C3A", fill_opacity=1).move_to(
        body.get_bottom() + UP * 0.22 * w)
    stack = Rectangle(width=0.14 * w, height=0.5 * w, stroke_width=0, fill_color="#5B6372", fill_opacity=1).next_to(
        body, UP, buff=0).shift(RIGHT * 0.25 * w)
    return VGroup(stack, body, mouth)


def cell_tank(w=1.2):
    tank = Rectangle(width=w, height=0.7 * w, stroke_color="#C9D3E0", stroke_width=2, fill_color="#2F6FA8",
                     fill_opacity=0.5)
    plates = VGroup(*[Rectangle(width=0.06 * w, height=0.6 * w, stroke_width=0,
                                fill_color=COPPER if k % 2 else "#8C929B", fill_opacity=1).move_to(
        tank.get_center() + RIGHT * (k - 2.5) * 0.16 * w + UP * 0.08 * w) for k in range(6)])
    return VGroup(tank, plates)


class Process(VoiceoverScene):
    def construct(self):
        card(self, 2, "From rock to metal", "What happens between the hole in the ground and a copper wire?",
             "Chapter two. From rock to metal.", lit=("make", "unit"))
        self.chain()
        self.funnel()
        self.leach()

    def chain(self):
        pit = draw.open_pit(2.6, 0.9, benches=3)
        pit.ore.set_opacity(0)
        truck = draw.haul_truck(1.1)
        cr = crusher(1.0)
        mill = draw.mill_drum(0.55)
        flot = draw.flotation_cell(1.1)
        conc = Polygon([-0.6, 0, 0], [0.6, 0, 0], [0, 0.55, 0], stroke_width=0, fill_color="#6E4A30", fill_opacity=1)
        row1 = [pit, truck, cr, mill, flot, conc]
        for m in row1:
            m.scale_to_fit_height(min(m.height, 1.1))
        VGroup(*row1).arrange(RIGHT, buff=0.75).move_to([0, 1.55, 0])
        ship = draw.ship(1.9, boxes=0) if True else None
        fur = furnace(1.1)
        anode = draw.cathode(0.8, color="#B9683A")
        refine = cell_tank(1.2)
        cath = VGroup(*[draw.cathode(0.75) for _ in range(3)]).arrange(RIGHT, buff=-0.45)
        row2 = [ship, fur, anode, refine, cath]
        for m in row2:
            m.scale_to_fit_height(min(m.height, 1.1))
        VGroup(*row2).arrange(RIGHT, buff=0.95).move_to([0, -1.75, 0])
        names1 = ["blast and dig", "haul", "crush", "grind", "float", "concentrate"]
        names2 = ["ship", "smelt", "anode", "refine", "cathode"]
        grade1 = ["about 1% copper", "", "", "finer than sand", "", "25-35% copper"]
        grade2 = ["", "", "about 99% copper", "", "99.99% copper"]
        labs = VGroup()
        for m, n, g in zip(row1 + row2, names1 + names2, grade1 + grade2):
            l_ = VGroup(tx(n, 17, WHITE, bold=True))
            if g:
                l_.add(tx(g, 14, COPPER))
            l_.arrange(DOWN, buff=0.04).next_to(m, DOWN, buff=0.15)
            labs.add(l_)
        arrows = VGroup()
        for a, b in zip(row1[:-1], row1[1:]):
            arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B,
                             max_tip_length_to_length_ratio=0.3, tip_length=0.14))
        turn = Arrow(conc.get_bottom() + DOWN * 0.75 + LEFT * 0.3, ship.get_top() + UP * 0.25 + RIGHT * 0.5, buff=0.05,
                     stroke_width=2.5, color=GREY_B, tip_length=0.16, max_tip_length_to_length_ratio=0.05)
        arrows2 = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B,
                                 max_tip_length_to_length_ratio=0.3, tip_length=0.14) for a, b in zip(row2[:-1], row2[1:])])
        zone1 = tx("at the mine", 18, GREY_A).to_corner(UL, buff=0.4)
        zone2 = tx("often a continent away", 18, GREY_A).move_to([-5.2, -0.45, 0])
        mill_spin = mill.drum.add_updater(lambda m, dt: m.rotate(-1.4 * dt))
        bubbles = VGroup(*[Circle(0.035, stroke_color="#E8EAED", stroke_width=1).move_to(
            flot.tank.get_bottom() + UP * 0.1 + RIGHT * (k - 3) * 0.12) for k in range(7)])
        t0 = ValueTracker(0)

        def rise(g):
            for k, b_ in enumerate(g):
                f = (t0.get_value() * 0.6 + k / 7) % 1
                b_.move_to(flot.tank.get_bottom() + UP * (0.05 + f * (flot.tank.height - 0.1)) +
                           RIGHT * (k - 3) * 0.12 * flot.tank.width / 1.1)
        bubbles.add_updater(rise)
        src = source("the standard route for sulphide copper ores; grades are typical, not one mine's", size=13)
        with self.voiceover(
            "Copper does not come out of the ground as metal. It comes as a mineral, mostly copper and iron and sulphur, "
            "spread through rock as grains you can barely see. <bookmark mark='a'/> So the mine blasts the rock and "
            "digs it, and trucks the size of houses haul it out of the pit. <bookmark mark='b'/> Crushers break it into "
            "gravel. <bookmark mark='c'/> Huge rotating mills, full of steel balls, grind it finer than sand, because "
            "every grain of copper mineral must be set free from the rock around it. <bookmark mark='d'/> Then comes the "
            "trick that makes modern mining possible: flotation. The powder is mixed with water and chemicals that "
            "make the copper minerals repel water, air is blown through, and the copper grains cling to the bubbles and "
            "rise to the top as a froth, while the waste sinks. <bookmark mark='e'/> The froth, dried, is concentrate: "
            "from about one percent copper to about a quarter or a third. <bookmark mark='f'/> Concentrate is light "
            "enough to ship, and much of it crosses an ocean, to smelters in China, Japan and elsewhere. "
            "<bookmark mark='g'/> A smelter melts it and burns off the sulphur and iron, leaving plates that are about "
            "ninety-nine percent copper. <bookmark mark='h'/> A refinery hangs those plates in an acid bath and runs an "
            "electric current through it, and pure copper builds up on the other side: cathode, ninety-nine point nine "
            "nine percent copper, the metal the world trades."
        ) as vo:
            self.add(t0)
            t0.add_updater(lambda m, dt: m.increment_value(dt))
            self.play(FadeIn(zone1), FadeIn(src), FadeIn(pit), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(truck, shift=RIGHT * 0.3), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(cr), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(mill), FadeIn(labs[3]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[3]), FadeIn(flot), FadeIn(labs[4]))
            self.add(bubbles)
            vo.wait_until("e")
            self.play(GrowArrow(arrows[4]), FadeIn(conc, shift=UP * 0.2), FadeIn(labs[5]))
            vo.wait_until("f")
            self.play(Create(turn), FadeIn(zone2), FadeIn(ship, shift=RIGHT * 0.3), FadeIn(labs[6]))
            vo.wait_until("g")
            self.play(GrowArrow(arrows2[0]), FadeIn(fur), FadeIn(labs[7]))
            self.play(GrowArrow(arrows2[1]), FadeIn(anode), FadeIn(labs[8]))
            vo.wait_until("h")
            self.play(GrowArrow(arrows2[2]), FadeIn(refine), FadeIn(labs[9]))
            self.play(GrowArrow(arrows2[3]), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cath], lag_ratio=0.3),
                      FadeIn(labs[10]))
        mill.drum.clear_updaters()
        bubbles.clear_updaters()
        t0.clear_updaters()
        self.clear_scene()

    def funnel(self):
        F = R["funnel"]
        vals = [("rock moved", F["moved"], ROCK, "ore plus two tonnes of waste rock for each tonne of ore"),
                ("ore milled", F["ore"], "#A48464", "at 1% copper, with 85% of it recovered"),
                ("concentrate", F["concentrate"], "#6E4A30", "at about 28% copper"),
                ("copper", F["cathode"], COPPER, "one tonne of cathode")]
        k = 5.0 / np.sqrt(F["moved"])
        sq = VGroup()
        for name, v, col, note in vals:
            s_ = Square(k * np.sqrt(v), stroke_width=0, fill_color=col, fill_opacity=0.95)
            sq.add(s_)
        for s_, x in zip(sq, [-4.0, -0.3, 2.5, 5.0]):
            s_.move_to([x, -2.4 + s_.height / 2, 0])
        labs = VGroup()
        for s_, (name, v, col, note) in zip(sq, vals):
            labs.add(VGroup(tx(f"{v:,.0f} t" if v >= 10 else f"{v:.1f} t", 24, WHITE, bold=True),
                            tx(name, 18, col if col != ROCK else "#C9A98A", bold=True)).arrange(DOWN, buff=0.05).next_to(
                s_, UP, buff=0.15))
        notes = VGroup(*[tx(n, 14, GREY_B) for *_, n in vals])
        for n_, s_ in zip(notes, sq):
            n_.next_to(s_, DOWN, buff=0.15)
        notes[0].shift(RIGHT * 0.0)
        head = tx("To make one tonne of copper from ore at 1%", 26, WHITE, bold=True).to_edge(UP, buff=0.45)
        tag = estimate_tag("computed: the Works (mine.py); a 2:1 strip ratio and 85% recovery are assumptions",
                           corner=DR, size=13)
        with self.voiceover(
            "Now count the tonnes. Take ore at one percent copper, about what Escondida milled last year. "
            "<bookmark mark='a'/> To make one tonne of copper, the mill has to process about "
            f"{F['ore']:.0f} tonnes of ore, because the ore is one percent copper and the mill recovers only about "
            "eighty-five percent of that. <bookmark mark='b'/> But an open pit cannot take only the ore. To reach it, the "
            "mine strips away the waste rock around and above it, here two tonnes of waste for every tonne of ore. So "
            f"the mine moves about {F['moved']:.0f} tonnes of rock for each tonne of copper. <bookmark mark='c'/> The "
            f"mill turns that into about {F['concentrate']:.1f} tonnes of concentrate, <bookmark mark='d'/> and the "
            "smelter and refinery turn that into one tonne of metal. Each square here has an area in proportion to its "
            "tonnes. Almost everything a copper mine does is moving and grinding rock that is not copper. That is why "
            "the costs of a mine are mostly diesel, electricity, water, tyres, steel balls and wages, and why they "
            "depend so much on how much copper is in each tonne."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromCenter(sq[1]), FadeIn(labs[1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(GrowFromCenter(sq[0]), FadeIn(labs[0]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(TransformFromCopy(sq[1], sq[2]), FadeIn(labs[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(TransformFromCopy(sq[2], sq[3]), FadeIn(labs[3]), FadeIn(notes[3]))
            self.play(Indicate(sq[3], color=WHITE, scale_factor=1.6))
        self.clear_scene()

    def leach(self):
        G = R["grade"]
        heap = Polygon([-2.6, 0, 0], [2.6, 0, 0], [1.7, 1.1, 0], [-1.7, 1.1, 0], stroke_width=0, fill_color=ROCK,
                       fill_opacity=1).move_to([-3.2, 0.2, 0])
        liner = Line(heap.get_corner(DL) + LEFT * 0.2, heap.get_corner(DR) + RIGHT * 0.2, stroke_color="#2F6FA8",
                     stroke_width=5)
        sprink = VGroup(*[Line([x, 1.0, 0], [x, 1.5, 0], stroke_color="#5DA9E9", stroke_width=2).shift(
            heap.get_center() + DOWN * 0.3) for x in np.linspace(-1.4, 1.4, 6)])
        drops = VGroup(*[Dot(radius=0.04, color="#5DA9E9") for _ in range(18)])
        t = ValueTracker(0)

        def fall(g):
            for k, d in enumerate(g):
                f = (t.get_value() * 0.5 + k / 18) % 1
                x = heap.get_center()[0] + (k % 6 - 2.5) * 0.56
                d.move_to([x, heap.get_top()[1] + 0.5 - f * (heap.height + 0.3), 0])
        drops.add_updater(fall)
        pond = Rectangle(width=1.6, height=0.4, stroke_color="#C9D3E0", stroke_width=2, fill_color="#3FA7A0",
                         fill_opacity=0.7).move_to([0.6, -0.6, 0])
        ew = cell_tank(1.4).move_to([3.4, -0.4, 0])
        arr = VGroup(Arrow(heap.get_right() + DOWN * 0.3, pond.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B,
                           tip_length=0.14),
                     Arrow(pond.get_right(), ew.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B, tip_length=0.14))
        cath = draw.cathode(0.9).next_to(ew, RIGHT, buff=0.5)
        labs = VGroup(tx("crushed low-grade ore, stacked", 17, WHITE).next_to(heap, DOWN, buff=0.35),
                      tx("weak acid dissolves the copper", 17, "#5DA9E9").next_to(heap, UP, buff=0.7),
                      tx("copper-rich solution", 15, "#3FA7A0").next_to(pond, DOWN, buff=0.15),
                      tx("electrowinning", 17, WHITE).next_to(ew, DOWN, buff=0.2),
                      tx("cathode, at the mine", 15, COPPER).next_to(cath, DOWN, buff=0.15))
        head = tx("The other route: leaching", 26, WHITE, bold=True).to_edge(UP, buff=0.45)
        fact = VGroup(tx(f"Freeport's US mines leach ore at {G['us_leach']:.2f}% copper", 20, COPPER, bold=True),
                      tx(f"that is {R['grade']['rock'][-1]:,.0f} tonnes of ore for a tonne of copper, before waste",
                         17, WHITE)).arrange(DOWN, buff=0.06).move_to([0.3, -2.6, 0])
        src = source("Freeport-McMoRan, Form 10-K for 2025 (leach grade); computed, the Works (mine.py), 85% recovery",
                     size=13)
        with self.voiceover(
            "There is a second route, for poorer ore and for ores where the copper has already been changed by air and "
            "water. <bookmark mark='a'/> The rock is crushed and stacked in great heaps on a waterproof liner, "
            "<bookmark mark='b'/> and weak acid is sprinkled over it for months. The acid dissolves the copper and "
            "trickles out at the bottom as a blue-green solution. <bookmark mark='c'/> A chemical step concentrates it, "
            "and an electric current plates the copper straight out as cathode, at the mine. No mill, no flotation, no "
            "smelter, so it is cheap per tonne of rock, and it can make money from rock that a mill never could. "
            f"<bookmark mark='d'/> Freeport's mines in Arizona and New Mexico put ore holding just "
            f"{G['us_leach']:.2f} percent copper on their leach pads in 2025. At that grade, a tonne of copper needs more "
            f"than {R['grade']['rock'][-1]:,.0f} tonnes of ore. A copper mine, in other words, is a machine for moving "
            "rock cheaply, and what decides whether it pays is how much copper each tonne holds."
        ) as vo:
            self.add(t)
            t.add_updater(lambda m, dt: m.increment_value(dt))
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(liner), FadeIn(heap, shift=DOWN * 0.2), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(FadeIn(sprink), FadeIn(labs[1]))
            self.add(drops)
            self.play(GrowArrow(arr[0]), FadeIn(pond), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(ew), FadeIn(labs[3]))
            self.play(FadeIn(cath, shift=UP * 0.2), FadeIn(labs[4]))
            vo.wait_until("d")
            self.play(FadeIn(fact, shift=UP * 0.1))
        drops.clear_updaters()
        t.clear_updaters()
        self.clear_scene()
