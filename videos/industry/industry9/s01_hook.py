from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.holes()
        self.mine()
        self.title()

    def holes(self):
        E = R["esc"]
        sky = Rectangle(width=14.4, height=4.0, stroke_width=0, fill_color="#1C2B44", fill_opacity=1).move_to([0, 2.1, 0])
        rock = Rectangle(width=14.4, height=3.2, stroke_width=0, fill_color="#4E4034", fill_opacity=1).move_to(
            [0, -2.5, 0])
        gravel = VMobject(stroke_width=0, fill_color="#B98E5C", fill_opacity=1).set_points_as_corners(
            [[-7.2, 0.1, 0], [-4, 0.25, 0], [-1, 0.12, 0], [2, 0.45, 0], [3.2, 0.5, 0], [5, 0.2, 0], [7.2, 0.3, 0],
             [7.2, -0.9, 0], [-7.2, -0.9, 0], [-7.2, 0.1, 0]])
        layer = VGroup(tx("gravel", 14, "#6E5233").move_to([-6.4, -0.45, 0]),
                       tx("bedrock", 14, "#9C8A78").move_to([-6.4, -1.4, 0]))
        sun = draw.sun(0.5).move_to([5.9, 3.1, 0])
        where = VGroup(tx("The Atacama desert, northern Chile", 22, WHITE, bold=True),
                       tx("March 1981", 18, GREY_A)).arrange(DOWN, buff=0.06).to_corner(UL, buff=0.4)
        budget = VGroup(*[Circle(radius=0.11, stroke_color=GREY_A, stroke_width=2, fill_color=GREY_A,
                                 fill_opacity=0.9) for _ in range(9)]).arrange(RIGHT, buff=0.14)
        budget_l = tx("money for nine holes", 16, GREY_A)
        purse = VGroup(budget_l, budget).arrange(RIGHT, buff=0.25).move_to([0.6, 3.2, 0])
        xs = [-5.4, -4.2, -3.0, -1.8, -0.6]
        rig = draw.derrick(1.6, color="#C9A26B").move_to([xs[0], 1.0, 0])
        marks = VGroup()
        for k, x in enumerate(xs):
            hole = Line([x, 0.15, 0], [x, -2.7, 0], stroke_color="#1A1410", stroke_width=5)
            cross = VGroup(Line([x - 0.15, -2.85, 0], [x + 0.15, -3.15, 0]), Line([x - 0.15, -3.15, 0],
                                                                                [x + 0.15, -2.85, 0])).set_stroke(STATE, 4)
            marks.add(VGroup(hole, cross, tx(f"{k + 1}", 16, GREY_A).move_to([x, -3.45, 0])))
        x6 = 2.2
        hole6 = Line([x6, 0.45, 0], [x6, -2.7, 0], stroke_color="#1A1410", stroke_width=5)
        ore = VGroup(Ellipse(width=3.6, height=1.1, stroke_width=0, fill_color=COPPER, fill_opacity=0.85),
                     *[Dot(radius=0.03, color="#FFD2A8").move_to([1.5 * np.cos(a) * r_, 0.4 * np.sin(a) * r_, 0])
                       for a, r_ in zip(np.linspace(0, 40, 40), np.linspace(0.1, 0.95, 40))]).move_to([x6 + 0.3, -2.2, 0])
        six = tx("6", 18, COPPER, bold=True).move_to([x6, -3.45, 0])
        hill = tx("a low hill", 15, GREY_A).move_to([x6 - 1.05, 0.75, 0])
        est = VGroup(tx(f"about {E['first_estimate']:.0f} million tonnes of ore", 21, COPPER, bold=True),
                     tx("at 1.3-1.5% copper", 18, WHITE),
                     tx(f"the whole search: ${E['cost']:.1f} million", 18, GREY_A)).arrange(DOWN, buff=0.07)
        plate = RoundedRectangle(corner_radius=0.1, width=est.width + 0.4, height=est.height + 0.3, stroke_color=COPPER,
                                 stroke_width=1.5, fill_color="#141A24", fill_opacity=0.95)
        estp = VGroup(plate, est).move_to([5.05, 1.75, 0])
        hidden = tx("Escondida: Spanish for 'hidden'", 19, WHITE, bold=True).next_to(estp, DOWN, buff=0.2)
        src = source("Francisco Ortiz, 'El descubrimiento del yacimiento Escondida' (CESCO, 2024)", size=13)
        with self.voiceover(
            "In March 1981, a drilling crew was working in the Atacama desert of northern Chile, the driest place on "
            "Earth, for an exploration project of two American companies, Utah International and Getty Oil. They were "
            "looking for copper hidden in the bedrock beneath the gravel. <bookmark mark='a'/> They had money for nine "
            "holes. The first came up empty. <bookmark mark='b'/> So did the second, the third, the fourth and the "
            "fifth. More than half the money was gone, and there was nothing to show for it. <bookmark mark='c'/> They "
            "moved the rig to a low hill and drilled the sixth hole. It was finished on the fourteenth of March, and it "
            "went through rock rich in copper. <bookmark mark='d'/> The first careful estimate was "
            f"{E['first_estimate']:.0f} million tonnes of ore at well over one percent copper. The whole search, two "
            f"years of it, had cost {E['cost']:.0f} million dollars. They called it Escondida: Spanish for hidden."
        ) as vo:
            self.play(FadeIn(sky), FadeIn(rock), FadeIn(gravel), FadeIn(sun), FadeIn(where), FadeIn(src), FadeIn(layer))
            self.play(FadeIn(rig, shift=DOWN * 0.3), FadeIn(purse))
            vo.wait_until("a")
            self.play(Create(marks[0][0]), rig.animate.shift(DOWN * 0.08), run_time=1.0, rate_func=there_and_back)
            self.play(FadeIn(marks[0][1]), FadeIn(marks[0][2]), budget[0].animate.set_fill(opacity=0.1))
            vo.wait_until("b")
            for k in range(1, 5):
                self.play(rig.animate.move_to([xs[k], 1.0, 0]), run_time=0.45)
                self.play(Create(marks[k][0]), FadeIn(marks[k][1]), FadeIn(marks[k][2]),
                          budget[k].animate.set_fill(opacity=0.1), run_time=0.55)
            vo.wait_until("c")
            self.play(rig.animate.move_to([x6, 1.3, 0]), FadeIn(hill), run_time=1.0)
            self.play(Create(hole6), FadeIn(six), budget[5].animate.set_fill(COPPER, opacity=1).set_stroke(COPPER),
                      run_time=1.4)
            self.play(FadeIn(ore, scale=0.6), Flash([x6, -2.2, 0], color=COPPER, line_length=0.5, num_lines=16),
                      run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(estp, shift=UP * 0.1))
            self.wait(2.5)
            self.play(Write(hidden), run_time=1.2)
        self.clear_scene()

    def mine(self):
        E = R["esc"]
        pit = draw.open_pit(6.4, 2.2, benches=6)
        pit.scale_to_fit_width(6.2).move_to([-3.6, 0.2, 0])
        trucks = VGroup(*[draw.haul_truck(0.55, color="#F2C14E") for _ in range(3)])
        anchors = pit[2].get_anchors()
        cx = pit[2].get_center()[0]
        right = sorted({(round(a[0], 4), round(a[1], 4)) for a in anchors if a[0] > cx - 0.3}, key=lambda q: (q[0], q[1]))
        right = [(cx, right[0][1])] + right
        road = VMobject().set_points_as_corners([[x, y + trucks[0].height / 2 + 0.02, 0] for x, y in right])
        for t_ in trucks:
            t_.move_to(road.get_start())
        bars = VGroup()
        vals = [("1991", "built for", E["first_capacity"]), ("2025", "produced", E["output"]),
                ("2026", "expected", get("esc.output.2026")), ("2027-31", "a year", E["medium"])]
        for k, (y_, lab, v) in enumerate(vals):
            b = Rectangle(width=0.85, height=v / 1305 * 3.2, stroke_width=0, fill_color=COPPER if k < 2 else "#8C5A3C",
                          fill_opacity=0.9).move_to([1.7 + 1.35 * k, -2.6, 0], aligned_edge=DOWN)
            lo_, hi_ = span("esc.output.2026")
            n = tx(f"{v:,.0f} kt" if k != 2 else f"{lo_:,.0f}-{hi_:,.0f}", 16, WHITE, bold=True).next_to(b, UP, buff=0.08)
            l_ = VGroup(tx(y_, 15, WHITE), tx(lab, 13, GREY_B)).arrange(DOWN, buff=0.03).next_to(b, DOWN, buff=0.1)
            bars.add(VGroup(b, n, l_))
        unit = tx("copper, thousand tonnes a year", 15, GREY_B).move_to([3.7, 1.4, 0])
        tag = VGroup(tx("Escondida, today", 26, WHITE, bold=True), tx("the largest copper mine on Earth", 18, GREY_A)
                     ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).to_corner(UL, buff=0.4)
        money = VGroup(tx(f"year to June 2025: ${E['ebitda']:.1f}bn of operating profit", 19, PRICE, bold=True),
                       tx("owners: BHP 57.5%, Rio Tinto 30%, Japanese partners 12.5%", 15, GREY_A)).arrange(
            DOWN, buff=0.06).move_to([3.7, 2.6, 0])
        grade = VGroup(tx(f"copper in the ore: {E['grade25']:.2f}% in 2025", 20, WHITE, bold=True),
                       tx(f"about {E['grade26']:.2f}% in 2026", 20, STATE, bold=True)).arrange(DOWN, buff=0.08).move_to(
            [-3.6, -2.7, 0])
        src = source("BHP, results and operational review for the year to June 2025; Ortiz (2024)", size=13)

        def haul(t_, d):
            return Succession(Wait(d), MoveAlongPath(t_, road, run_time=3.0, rate_func=linear))

        with self.voiceover(
            "The hill became Escondida. <bookmark mark='a'/> It opened in 1991, built to produce three hundred and "
            "twenty thousand tonnes of copper a year, and it grew into the largest copper mine on Earth. "
            f"<bookmark mark='b'/> In the year to June 2025 it produced {E['output']:,.0f} thousand tonnes, and earned "
            f"{E['ebitda']:.1f} billion dollars of operating profit for its owners: BHP, Rio Tinto and a group of "
            "Japanese partners. <bookmark mark='c'/> But the rock is getting poorer. The ore going into its mills held "
            f"{E['grade25']:.2f} percent copper last year. This year, about {E['grade26']:.2f}. <bookmark mark='d'/> So "
            "BHP expects output to fall, to under a million tonnes a year by the end of the decade, while the cost of "
            "each pound rises. A mine is a bet of billions on a price decades away, made on rock that only gets worse."
        ) as vo:
            self.play(FadeIn(pit), FadeIn(tag), FadeIn(src), FadeIn(unit))
            self.play(LaggedStart(*[haul(t_, 0) for t_ in trucks], lag_ratio=0.35), run_time=4.2)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(money))
            self.play(LaggedStart(*[haul(t_, 0) for t_ in trucks], lag_ratio=0.35), run_time=4.2)
            vo.wait_until("c")
            self.play(FadeIn(grade, shift=UP * 0.1), pit.ore.animate.set_fill(opacity=0.45))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(g[0], DOWN), FadeIn(g[1:])) for g in bars[2:]],
                                  lag_ratio=0.4), run_time=1.8)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part nine: mining and metals. Why is a mine worth a fortune in one decade and nothing in "
            "the next?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
