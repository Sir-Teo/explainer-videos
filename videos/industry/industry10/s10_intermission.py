from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.story()

    def film(self):
        r = R["income"]["real"]
        ys = sorted(r)
        pa = viz.plot_axes([1929, 2027], [0, 230], x_length=11.4, y_length=4.8,
                           xticks=[1930, 1950, 1970, 1990, 2010, 2026], yticks=[50, 100, 150, 200],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=14).move_to([0, -0.4, 0])
        t = ValueTracker(ys[0])

        def line():
            q = [pa.ax.c2p(y, r[y]) for y in ys if y <= t.get_value()]
            return VMobject(stroke_color=FARM, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()

        def pick(a, b, f):
            y = f(range(a, b + 1), key=lambda k: r[k])
            return y, r[y]
        eps = [(*pick(1929, 1935, min), "the Depression"), (*pick(1940, 1950, max), "the war and after"),
               (*pick(1970, 1976, max), "the 1970s grain boom"), (*pick(1980, 1990, min), "the farm crisis"),
               (*pick(2010, 2015, max), "the biofuel boom"), (*pick(2020, 2026, max), "2022")]
        marks = VGroup()
        for x, y, name in eps:
            p = pa.ax.c2p(x, y)
            up = y > 100
            marks.add(VGroup(Dot(p, radius=0.06, color=WHITE), VGroup(tx(name, 15, WHITE, bold=True),
                                                                       tx(f"{x}: ${y:.0f}bn", 13, GREY_A)).arrange(
                DOWN, buff=0.02).next_to(p, UP if up else DOWN, buff=0.12)))
        head = tx("US net farm income, in 2026 dollars", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("USDA ERS, Farm Income and Wealth Statistics (3 September 2026; 2026 is a forecast), deflated "
                     "with ERS's GDP deflator", size=13)
        with self.voiceover(
            "An intermission: ninety-seven years of what all American farms together earned, after their costs, in "
            "today's dollars. <bookmark mark='a'/> The Depression, when farm income collapsed and the government began "
            "to pay farmers to grow less. <bookmark mark='b'/> The war and the years after it, when the world needed "
            "American food. <bookmark mark='c'/> The 1970s, when the Soviet Union bought American grain and prices "
            "soared, and farmers borrowed to buy land. <bookmark mark='d'/> The farm crisis of the 1980s, when interest "
            "rates and land prices broke them. <bookmark mark='e'/> The biofuel boom, and 2022's war in Ukraine. Look at "
            "the shape: a century in which farms grew far more food, with no lasting rise in what farming earned, and "
            "income shared among far fewer farms."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.add(ln, yr)
            prev = 0
            for m, x1 in zip("abcde", (1936, 1951, 1977, 1991, 2026)):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.2, rate_func=linear)
                new = [marks[i] for i in range(len(marks)) if prev < eps[i][0] <= x1]
                if new:
                    self.play(*[FadeIn(g, shift=DOWN * 0.1) for g in new], run_time=0.6)
                prev = x1
        for m in (ln, yr):
            m.clear_updaters()
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["Farms keep about 13 cents of a US food dollar; farm work adds about 6.",
                 "An acre of corn rarely covers all its costs; the family's land and labour absorb the bad years.",
                 "The treadmill: new methods raise output, the price falls, and the gain passes to eaters.",
                 "Farmers buy from a few and sell to a few, and are one of very many.",
                 "Traders live on spreads; packers on the number of animals; the price is set by the weather.",
                 "A forward sale removes the price risk, not the weather's.",
                 "Next: brands and shops, the state, land, the tropics, and the landscape."]
        pics = [draw.coin_stack(3, r=0.15), draw.corn_plant(0.5), draw.tractor(0.6), draw.castle(0.6), draw.grain_elevator(0.5),
                draw.sack(0.45, label_="SOLD"), Arrow(LEFT * 0.3, RIGHT * 0.3, color=GOLD, buff=0)]
        rows = VGroup()
        for pic, l_ in zip(pics, lines):
            pic.scale_to_fit_height(min(pic.height, 0.42))
            if pic.width > 0.6:
                pic.scale_to_fit_width(0.6)
            rows.add(VGroup(pic, tx(l_, 20, WHITE)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The story so far. Farms keep about thirteen cents of an American food dollar, and the work done on farms "
            "adds about six. An acre of corn rarely covers all its costs, and the family's land and labour absorb the "
            "bad years. The treadmill turns every new method into a lower price, and the gain passes to the people who "
            "eat. The farmer buys from a few companies, sells to a few, and is one of very many. Traders live on "
            "spreads, packers on the number of animals, and the price itself is set by the weather. A forward sale "
            "removes the risk of the price, not of the weather. Next: brands and shops, the state, the land, the "
            "tropics, and the landscape."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()
