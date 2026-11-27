from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Making(VoiceoverScene):
    def construct(self):
        card(self, 2, "How a car is made", "What happens between a coil of steel and a car on a truck?",
             "Chapter two. How a car is made: what happens between a coil of steel and a car on a truck?", lit=("unit", "make"))
        self.stages()
        self.census()

    def stages(self):
        M = R["making"]
        xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        names = ["stamping", "welding", "painting", "assembly", "inspection, shipping"]
        icons = [draw.press(1.5), draw.robot_arm(1.4, SUPPLIER), draw.paint_booth(1.9), draw.crowd(3, 0.45, "#C9D3E0", cols=3),
                 draw.car_carrier(2.1)]
        st = VGroup()
        for x, nm, ic in zip(xs, names, icons):
            ic.move_to([x, 1.3, 0])
            lab = tx(nm, 17, PRICE, bold=True).move_to([x, 0.05, 0])
            st.add(VGroup(ic, lab))
        belt = Line([-6.6, -1.05, 0], [6.6, -1.05, 0], stroke_color=GREY_B, stroke_width=3)
        coil = draw.coil(0.45).move_to([-6.2, -0.7, 0])
        panel = Rectangle(width=1.0, height=0.08, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([-5.4, -0.95, 0])
        body = draw.car(1.8, "#AEB6C4").move_to([-2.7, -0.75, 0])
        painted = draw.car(1.8, MAKER).move_to([0.0, -0.75, 0])
        parts = VGroup(draw.engine(0.5).move_to([2.1, -2.0, 0]), draw.wrench(0.45).move_to([2.7, -2.0, 0]),
                       draw._wheel(0.18).move_to([3.3, -2.0, 0]))
        finished = draw.car(1.8, MAKER).move_to([2.7, -0.75, 0])
        count = VGroup(tx(f"some {M['parts']:,.0f} parts", 24, PRICE, bold=True), tx("Toyota's count for one car", 14, GREY_B)).arrange(DOWN, buff=0.05).move_to([0.0, -2.7, 0])
        src = source("Toyota Motor Corporation, 'Plant tours' and 'Toyota Production System'", size=13)
        with self.voiceover(
            "Toyota describes its plants in five steps, the same steps most car plants follow. "
            "<bookmark mark='a'/> Coils of sheet steel arrive and huge presses stamp them into the panels of a body: doors, "
            "roof, sides, floor. <bookmark mark='b'/> Robots weld the panels into a shell, called the body in white because "
            "it is still bare metal. <bookmark mark='c'/> The shell is dipped and sprayed in coat after coat of paint. "
            "<bookmark mark='d'/> Then final assembly: "
            "the engine or the battery, the wiring, the dashboard, the seats, the glass, the wheels. Toyota counts "
            f"some {M['parts']:,.0f} parts in a car, many of them made by other companies. <bookmark mark='e'/> Last, every "
            "car is checked, driven off the line and loaded for the dealers."
        ) as vo:
            self.play(FadeIn(belt), FadeIn(src), FadeIn(ghost(st, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(st[0]), FadeIn(coil))
            self.play(st[0][0].ram.animate.shift(DOWN * st[0][0].stroke * 0.9), run_time=0.4)
            self.play(st[0][0].ram.animate.shift(UP * st[0][0].stroke * 0.9), FadeIn(panel), run_time=0.4)
            vo.wait_until("b")
            arm = st[1][0]
            self.play(FadeIn(st[1]), FadeIn(body))
            self.play(Rotate(arm.upper, angle=-0.25, about_point=arm.elbow), run_time=0.5)
            self.play(Rotate(arm.upper, angle=0.25, about_point=arm.elbow), Flash(body.get_top(), color=PRICE), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(st[2]), FadeIn(painted))
            vo.wait_until("d")
            self.play(FadeIn(st[3]), FadeIn(finished), LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in parts], lag_ratio=0.2))
            self.play(FadeIn(count))
            vo.wait_until("e")
            self.play(FadeIn(st[4]))
            self.play(finished.animate.move_to([5.4, -0.75, 0]), run_time=1.5)
        self.clear_scene()

    def census(self):
        M = R["making"]
        a22 = M["us_assemblies"][2022]
        hours = M["employees"] * 2000 / (a22 * 1e6)
        stats = [(f"{M['firms']:,.0f}", "companies"), (f"{M['plants']:,.0f}", "plants"),
                 (f"{M['employees']:,.0f}", "people"), (f"${M['shipments']:,.0f}bn", "of cars and light trucks shipped")]
        g = VGroup()
        for i, (v, k) in enumerate(stats):
            g.add(VGroup(tx(v, 34, MAKER, bold=True), tx(k, 16, GREY_A)).arrange(DOWN, buff=0.06).move_to([-4.9 + 3.25 * i, 1.4, 0]))
        head = tx("America's car and light-truck assembly, 2022 Economic Census", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        calc = VGroup(tx(f"{M['employees']:,.0f} people x about 2,000 hours a year", 18, GREY_A),
                      tx(f"/ {a22:.1f} million vehicles assembled in 2022", 18, GREY_A),
                      tx(f"= about {hours:.0f} hours of work per vehicle", 24, PRICE, bold=True)).arrange(DOWN, buff=0.12).move_to([-2.0, -1.3, 0])
        model = VGroup(tx("The Works' model plant:", 16, GREY_B), tx(f"2 shifts of {M['people']:,} people,", 16, GREY_B),
                       tx(f"{M['line_hours']:,} hours each a year,", 16, GREY_B),
                       tx(f"250,000 cars: {M['hours']:.0f} hours a car", 18, YOU, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.3, -1.3, 0])
        src = source("US Census Bureau, 2022 Economic Census, NAICS 336110; Federal Reserve G.17, motor vehicle assemblies (via FRED)", size=12)
        tag = estimate_tag("hours per vehicle: estimates", size=13)
        with self.voiceover(
            "How much work goes into one? America's census of businesses counts it. <bookmark mark='a'/> In 2022 "
            f"{M['firms']:,.0f} companies ran {M['plants']:,.0f} plants that assemble cars and light trucks. They employed "
            f"{M['employees']:,.0f} people and shipped {M['shipments']:,.0f} billion dollars' worth of vehicles. "
            f"<bookmark mark='b'/> Those plants put together about {a22:.1f} million vehicles that year. If each person "
            f"worked about two thousand hours, that is roughly {hours:.0f} hours of work for each vehicle: a rough figure, "
            "since not everyone in those plants works on the line. <bookmark mark='c'/> The model plant of the Run it game, "
            f"with two shifts of two thousand people, comes to about {M['hours']:.0f} hours a car, and finishes one about "
            "every minute. Roughly one person's working week, for a machine of thirty thousand parts. That is what a "
            "century of the moving line bought."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(ghost(g, opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in g], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in calc], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(model, shift=LEFT * 0.2))
        self.clear_scene()
