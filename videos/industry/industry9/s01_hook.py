from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.holes()
        self.mine()
        self.title()

    def holes(self):
        E = R["esc"]
        sky = Rectangle(width=14.4, height=4.2, stroke_width=0, fill_color="#1C2B44", fill_opacity=1).move_to([0, 2.0, 0])
        sand = Rectangle(width=14.4, height=4.0, stroke_width=0, fill_color="#B98E5C", fill_opacity=1).move_to([0, -2.0, 0])
        dune = VMobject(stroke_width=0, fill_color="#A47A4C", fill_opacity=1).set_points_smoothly(
            [[-7.2, 0.0, 0], [-4, 0.35, 0], [-1, 0.1, 0], [2, 0.45, 0], [5, 0.15, 0], [7.2, 0.3, 0], [7.2, -0.2, 0],
             [-7.2, -0.2, 0]])
        sun = draw.sun(0.5).move_to([5.6, 3.0, 0])
        where = VGroup(tx("The Atacama desert, northern Chile", 22, WHITE, bold=True),
                       tx("March 1981", 18, GREY_A)).arrange(DOWN, buff=0.06).to_corner(UL, buff=0.4)
        xs = [-5.6, -4.2, -2.8, -1.4, 0.0]
        rig = draw.derrick(1.6, color="#C9A26B").move_to([xs[0], 0.8, 0])
        marks = VGroup()
        for k, x in enumerate(xs):
            hole = Line([x, -0.1, 0], [x, -2.4, 0], stroke_color="#5B4630", stroke_width=4)
            cross = VGroup(Line([x - 0.15, -2.55, 0], [x + 0.15, -2.85, 0]), Line([x - 0.15, -2.85, 0],
                                                                                [x + 0.15, -2.55, 0])).set_stroke(STATE, 4)
            marks.add(VGroup(hole, cross, tx(f"{k + 1}", 16, GREY_B).move_to([x, -3.1, 0])))
        x6 = 2.6
        hole6 = Line([x6, -0.1, 0], [x6, -2.4, 0], stroke_color="#5B4630", stroke_width=4)
        ore = Ellipse(width=3.2, height=0.7, stroke_width=0, fill_color=COPPER, fill_opacity=0.9).move_to([x6 + 0.4, -2.3, 0])
        six = tx("6", 18, COPPER, bold=True).move_to([x6, -3.1, 0])
        est = VGroup(tx(f"about {E['first_estimate']:.0f} million tonnes", 20, COPPER, bold=True),
                     tx("of ore at 1.3-1.5% copper", 18, WHITE)).arrange(DOWN, buff=0.05).move_to([4.6, -1.0, 0])
        src = source("Francisco Ortiz, 'El descubrimiento del yacimiento Escondida' (CESCO, 2024)", size=13)
        with self.voiceover(
            "In March 1981, a drilling crew working for two American companies was in the Atacama desert of northern "
            "Chile, the driest place on Earth, looking for copper hidden under the gravel. <bookmark mark='a'/> They "
            "had money for nine holes. The first came up empty. <bookmark mark='b'/> So did the second, the third, the "
            "fourth and the fifth. The geologists considered packing up and moving the rig a hundred kilometres south. "
            "<bookmark mark='c'/> They drilled the sixth hole anyway, on a low hill. It was finished on the fourteenth "
            "of March, and it went through rock rich in copper. <bookmark mark='d'/> The first, careful estimate was "
            f"{E['first_estimate']:.0f} million tonnes of ore at well over one percent copper. The whole exploration "
            f"project had cost about {E['cost']:.0f} million dollars."
        ) as vo:
            self.play(FadeIn(sky), FadeIn(sand), FadeIn(dune), FadeIn(sun), FadeIn(where), FadeIn(src), FadeIn(rig))
            vo.wait_until("a")
            self.play(Create(marks[0][0]), run_time=1.0)
            self.play(FadeIn(marks[0][1]), FadeIn(marks[0][2]))
            vo.wait_until("b")
            for k in range(1, 5):
                self.play(rig.animate.move_to([xs[k], 0.8, 0]), run_time=0.5)
                self.play(Create(marks[k][0]), FadeIn(marks[k][1]), FadeIn(marks[k][2]), run_time=0.5)
            vo.wait_until("c")
            self.play(rig.animate.move_to([x6, 0.8, 0]), run_time=0.8)
            self.play(Create(hole6), FadeIn(six), run_time=1.2)
            self.play(GrowFromCenter(ore), Flash([x6, -2.3, 0], color=COPPER, line_length=0.4))
            vo.wait_until("d")
            self.play(FadeIn(est, shift=UP * 0.1))
        self.clear_scene()

    def mine(self):
        E = R["esc"]
        pit = draw.open_pit(7.0, 2.0).move_to([0, -0.6, 0])
        bars = VGroup()
        vals = [("1991: built for", E["first_capacity"]), ("2025: produced", E["output"]),
                ("2026: expected", 1200), ("2027-2031: a year", E["medium"])]
        for k, (lab, v) in enumerate(vals):
            b = Rectangle(width=0.8, height=v / 1305 * 2.6, stroke_width=0, fill_color=COPPER if k < 2 else "#8C5A3C",
                          fill_opacity=0.9).move_to([2.2 + 1.3 * k, -2.2, 0], aligned_edge=DOWN)
            n = tx(f"{v:,.0f} kt" if k != 2 else "1,150-1,250 kt", 15, WHITE, bold=True).next_to(b, UP, buff=0.08)
            l_ = VGroup(*[tx(w, 13, GREY_B) for w in lab.split(": ")]).arrange(DOWN, buff=0.02).next_to(b, DOWN, buff=0.1)
            bars.add(VGroup(b, n, l_))
        bars.shift(LEFT * 0.4)
        pit.scale(0.62).move_to([-3.6, 0.2, 0])
        tag = VGroup(tx("Escondida, today", 24, WHITE, bold=True), tx("the largest copper mine on Earth", 17, GREY_A)
                     ).arrange(DOWN, buff=0.05).to_corner(UL, buff=0.4)
        money = tx(f"year to June 2025: {E['output']:,.0f} kt of copper, ${E['ebitda']:.1f}bn of operating profit", 18,
                   COPPER).to_edge(UP, buff=0.45).shift(RIGHT * 1.8)
        grade = VGroup(tx(f"grade: {E['grade25']:.2f}% in 2025", 20, WHITE, bold=True),
                       tx(f"about {E['grade26']:.2f}% in 2026", 20, STATE, bold=True)).arrange(DOWN, buff=0.08).move_to(
            [-3.6, -2.6, 0])
        src = source("BHP, results for the year to June 2025; Ortiz (2024)", size=13)
        with self.voiceover(
            "The hill became Escondida. <bookmark mark='a'/> It opened in 1991, built to produce three hundred and "
            "twenty thousand tonnes of copper a year, and it became the largest copper mine on Earth. "
            f"<bookmark mark='b'/> In the year to June 2025 it produced {E['output']:,.0f} thousand tonnes and earned "
            f"{E['ebitda']:.1f} billion dollars of operating profit for its owners, BHP, Rio Tinto and two Japanese "
            "partners. <bookmark mark='c'/> But the rock is getting poorer. The ore going into its mills held "
            f"{E['grade25']:.2f} percent copper last year; this year, about {E['grade26']:.2f}. <bookmark mark='d'/> So "
            "output is expected to fall, to about a million tonnes a year by the end of the decade, while the cost of "
            "each pound rises. A mine is a bet of billions on a price decades away, made on rock that only gets worse."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(pit), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(money))
            vo.wait_until("c")
            self.play(FadeIn(grade, shift=UP * 0.1))
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
