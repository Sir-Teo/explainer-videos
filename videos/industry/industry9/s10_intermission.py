from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.story()

    def film(self):
        cu = R["bet"]["series"]["copper"]
        ys = sorted(cu)
        pts = [(y, cu[y]) for y in ys]
        pa = viz.plot_axes([1900, 2021], [0, 10000], x_length=11.4, y_length=4.8,
                           xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[2500, 5000, 7500, 10000],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}", size=14).move_to([0, -0.4, 0])
        t = ValueTracker(ys[0])

        def line():
            x = t.get_value()
            q = [pa.ax.c2p(a, b) for a, b in pts if a <= x]
            return VMobject(stroke_color=COPPER, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()

        def peak(a, b, fn=max):
            y = fn(range(a, b + 1), key=lambda k: cu[k])
            return y, cu[y]
        eps = [(*peak(1914, 1918), "First World War"), (*peak(1930, 1934, min), "the Depression"),
               (*peak(1964, 1975), "the 1960s boom"), (*peak(1998, 2003, min), "the 2002 low"),
               (*peak(2005, 2012), "China's boom")]
        marks = VGroup()
        for x, y, name in eps:
            p = pa.ax.c2p(x, y)
            up = y > 3500
            marks.add(VGroup(Dot(p, radius=0.06, color=WHITE),
                             VGroup(tx(name, 15, WHITE, bold=True), tx(f"{x}: ${y:,.0f}", 13, GREY_A)).arrange(
                                 DOWN, buff=0.02).next_to(p, UP if up else DOWN, buff=0.12)))
        head = tx("A tonne of copper, in 1998 dollars, year by year since 1900", 22, WHITE, bold=True).to_edge(UP,
                                                                                                         buff=0.35)
        src = source("US Geological Survey, Data Series 140, copper: unit value in 1998 dollars", size=13)
        with self.voiceover(
            "An intermission: one hundred and twenty years of copper, from the US Geological Survey's historical "
            "statistics, in constant dollars. <bookmark mark='a'/> The First World War sent it soaring, "
            "<bookmark mark='b'/> and the Depression sent it to the floor. <bookmark mark='c'/> It rose again with "
            "the electrification of the post-war world and peaked in the 1960s and early 70s. "
            "<bookmark mark='d'/> Then came thirty years of decline, to a low in 2002, as new mines in Chile and new "
            "methods like leaching flooded the market. <bookmark mark='e'/> And then China. Look at the ends: in "
            f"constant dollars, a tonne cost about {cu[ys[-1]]:,.0f} in {ys[-1]}, against {cu[1900]:,.0f} in 1900, "
            "after a century in which the world used more copper every decade. Demand rose enormously, and the "
            "industry kept finding ways to dig poorer rock more cheaply."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.add(ln, yr)
            prev = 0
            for m, x1 in zip("abcde", (1919, 1936, 1976, 2003, 2020)):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.5, rate_func=linear)
                new = [marks[i] for i in range(len(marks)) if prev < eps[i][0] <= x1]
                if new:
                    self.play(*[FadeIn(g, shift=DOWN * 0.1) for g in new], run_time=0.6)
                prev = x1
        for m in (ln, yr):
            m.clear_updaters()
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["A mine is billions spent up front, repaid over decades at prices nobody knows.",
                 "Ore at 1% means moving about 350 tonnes of rock for each tonne of copper.",
                 "Grade falls as the best rock goes first; output falls and costs rise with it.",
                 "Waiting has value: build when the price is well above break-even.",
                 "Every miner takes the exchange's price; the low-cost mine survives the bad years.",
                 "Chile digs the most copper; China refines almost half of it.",
                 "Next: the supercycle, the state's share, critical minerals, gold, and the landscape."]
        pics = [draw.coin_stack(3, r=0.15), Square(0.45, stroke_width=0, fill_color=ROCK, fill_opacity=1),
                draw.open_pit(0.9, 0.35, benches=2), VGroup(Circle(0.22, stroke_color="#7EC8F5", stroke_width=3),
                                                           Line(ORIGIN, UP * 0.16, stroke_color="#7EC8F5")),
                draw.haul_truck(0.6), draw.cathode(0.45), Arrow(LEFT * 0.3, RIGHT * 0.3, color=GOLD, buff=0)]
        rows = VGroup()
        for pic, l_ in zip(pics, lines):
            pic.scale_to_fit_height(min(pic.height, 0.42))
            box = VGroup(pic).set_width(0.6) if pic.width > 0.6 else VGroup(pic)
            rows.add(VGroup(box, tx(l_, 21, WHITE)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The story so far. A mine is billions of dollars spent up front and repaid over decades, at prices nobody "
            "knows. At one percent copper, the industry moves about three hundred and fifty tonnes of rock for every "
            "tonne of metal. The grade falls as the best rock is dug first, so output falls and costs rise. Waiting "
            "has value, so mines get built in booms. Every miner takes the exchange's price, and the low-cost mine is "
            "the one that survives. And Chile digs the most copper while China refines almost half of it. Next: the "
            "supercycle, the state's share, the critical minerals, gold, and the landscape."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()
