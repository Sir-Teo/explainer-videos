from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


def staircase(ax, values, color, start=0.0, stroke_width=4):
    """Values, highest first, as a falling staircase from quantity ``start``, one unit per value."""
    steps = [(start + k, start + k + 1, v) for k, v in enumerate(values)]
    return step_curve(ax, steps, color, stroke_width)


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Demand, one buyer at a time", r"How many would be bought at each price, and why fewer at a "
             r"higher one?", "Chapter two. Demand, one buyer at a time.", scale=("person", "market"),
             horizon=("a day",))
        self.one()
        self.three()
        self.crowd()
        self.law()

    # ------------------------------------------------------------------
    def one(self):
        d = load("demand")
        cups = d["ana"]
        ax = price_axes(5, (0, 5), x_length=6.4, y_length=4.4, qticks=[0, 1, 2, 3, 4, 5], pticks=[0, 1, 2, 3, 4, 5],
                        qlabel=r"cups of coffee a day", plabel=r"Ana's value of one more cup",
                        center=LEFT * 2.8 + DOWN * 0.5)
        a = ax.ax
        ana = islander("ana", 0.9, name=True).to_corner(UR, buff=0.6).shift(LEFT * 1.6)
        bars = VGroup(*[Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0] - 0.06,
                                  height=a.c2p(0, v)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=ANA,
                                  fill_opacity=0.55).move_to((a.c2p(k, 0) + a.c2p(k + 1, v)) / 2)
                        for k, v in enumerate(cups)])
        vals = VGroup(*[label(dollars(v), font_size=22, color=WHITE).next_to(b, UP, buff=0.08)
                        for b, v in zip(bars, cups)])
        ordinals = (r"first", r"second", r"third", r"fourth")
        rows = VGroup(*[label(rf"her {o} cup: \ {dollars(v)}", font_size=24, color=GREY_A)
                        for o, v in zip(ordinals, cups)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.next_to(ana, DOWN, buff=0.4).align_to(ana, LEFT).shift(LEFT * 0.6)
        stairs = staircase(a, cups, ANA)
        price = 1.50
        pl = DashedLine(a.c2p(0, price), a.c2p(5, price), color=E.ACCENT, stroke_width=2.5)
        plab = label(rf"price {dollars(price)}", font_size=22, color=E.ACCENT).next_to(a.c2p(5, price), UP, buff=0.1)
        plab.align_to(pl, RIGHT)
        buys = label(r"she buys 2 cups", font_size=28, color=E.ACCENT).next_to(rows, DOWN, buff=0.45)
        buys.align_to(rows, LEFT)
        tag = illustrative_tag(corner=DR, font_size=17)
        with self.voiceover(
            "Start with one buyer. This is Ana, from the island's new village; she fishes, and sells her catch at "
            "the market. "
            "<bookmark mark='a'/> Ask her what a cup of coffee a day is worth to her, and the answer depends on how "
            "many she has already had. Her first cup is worth four dollars to her. Her second, two fifty. Her "
            "third, one twenty, and a fourth only forty cents. <bookmark mark='b'/> Each cup is worth less than "
            "the one before. That's the margin again, the same falling curve as the water. "
            "<bookmark mark='c'/> Now suppose coffee costs a dollar fifty a cup. Ana buys a cup whenever it's worth "
            "more to her than the price. That's two cups; the third isn't worth a dollar fifty to her. "
            "<bookmark mark='d'/> Draw her values as steps, and you have her demand curve: at each price, read "
            "across to the step, and down to how many cups she buys."
        ) as vo:
            self.play(FadeIn(ana, shift=DOWN * 0.2), FadeIn(tag), FadeIn(ax))
            vo.wait_until("a")
            for b, v, r in zip(bars, vals, rows):
                self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(r, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("b")
            self.play(Indicate(rows, color=ANA, scale_factor=1.03))
            vo.wait_until("c")
            self.play(Create(pl), FadeIn(plab))
            self.play(bars[0].animate.set_fill(E.ACCENT, 0.7), bars[1].animate.set_fill(E.ACCENT, 0.7),
                      bars[2].animate.set_fill(GREY_D, 0.4), bars[3].animate.set_fill(GREY_D, 0.4))
            self.play(FadeIn(buys, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Create(stairs), bars.animate.set_fill(opacity=0.15), run_time=1.5)
        self.clear_scene()

    def three(self):
        d = load("demand")
        who = {"Ana": ANA, "Bo": BO, "Chidi": CHIDI}
        ax = price_axes(9, (0, 5), x_length=8.6, y_length=4.2, qticks=list(range(10)), pticks=[0, 1, 2, 3, 4, 5],
                        qlabel=r"cups a day, \ all three together", plabel=r"value of one more cup",
                        center=LEFT * 1.3 + DOWN * 0.7)
        a = ax.ax
        people = VGroup(*[VGroup(islander(k.lower(), 0.7), label(rf"{k}: \ " + r", ".join(dollars(v) for v in vs),
                                                                    font_size=22, color=who[k])).arrange(RIGHT, buff=0.3)
                          for k, vs in d["three"].items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        people.to_corner(UR, buff=0.4)
        # every cup of every drinker, sorted from the most valued: the market's staircase
        cups = sorted([(v, k) for k, vs in d["three"].items() for v in vs], reverse=True)
        bars = VGroup(*[Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0] - 0.05, height=a.c2p(0, v)[1] - a.c2p(0, 0)[1],
                                  stroke_width=0, fill_color=who[k], fill_opacity=0.6)
                        .move_to((a.c2p(i, 0) + a.c2p(i + 1, v)) / 2) for i, (v, k) in enumerate(cups)])
        stairs = staircase(a, [v for v, _ in cups], E.DEMAND)
        price = 1.50
        n = sum(1 for v, _ in cups if v >= price)
        pl = DashedLine(a.c2p(0, price), a.c2p(9, price), color=E.ACCENT, stroke_width=2.5)
        q = DashedLine(a.c2p(n, 0), a.c2p(n, price), color=E.ACCENT, stroke_width=2.5)
        qlab = label(rf"at {dollars(price)}: \ {n} cups", font_size=26, color=E.ACCENT).next_to(a.c2p(n, price), UR,
                                                                                               buff=0.15)
        side = label(r"add the buyers sideways: \ every cup, \ most valued first", font_size=24, color=GREY_A)
        side.next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
        with self.voiceover(
            "Now three drinkers. <bookmark mark='a'/> Ana, as before; Bo, who values his first cup at three dollars "
            "and his second at one fifty; and Chidi, who'll pay five for his first and two for his second. "
            "<bookmark mark='b'/> To get the market's demand, take every cup that anyone wants, and line them up "
            "from the most valued to the least. Economists say you add the demands sideways: at each price, count "
            "the cups. <bookmark mark='c'/> The result is another staircase, with more and smaller steps. "
            f"<bookmark mark='d'/> At a dollar fifty, the three of them buy {n} cups between them."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in people], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(side))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=3)
            vo.wait_until("c")
            self.play(Create(stairs), bars.animate.set_fill(opacity=0.25), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(pl), Create(q), FadeIn(qlab))
        self.clear_scene()

    def crowd(self):
        d = load("demand")
        choke = d["choke"]
        panels = VGroup()
        for n in d["crowd_n"]:
            v = np.sort(np.array(d[f"crowd_{n}"]))[::-1]
            ax = price_axes(1, (0, 6), x_length=2.7, y_length=2.6, qticks=[0, 1], pticks=[0, 6],
                            qlabel=r"share of buyers", plabel="", font_size=16)
            a = ax.ax
            pts = []
            for k, x in enumerate(v):
                pts += [a.c2p(k / n, x), a.c2p((k + 1) / n, x)]
            stairs = VMobject(stroke_color=E.DEMAND, stroke_width=3).set_points_as_corners(pts)
            ideal = DashedLine(a.c2p(0, choke), a.c2p(1, 0), color=E.TRUTH, stroke_width=2)
            title = label(rf"{n:,} buyers".replace(",", "{,}"), font_size=22, color=WHITE).next_to(ax, UP, buff=0.15)
            g = VGroup(ax, ideal, stairs, title)
            g.stairs, g.ideal = stairs, ideal
            panels.add(g)
        panels.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.2)
        cap = label(r"values spread at random between \$0 and \$6: \ the staircase becomes a line", font_size=26,
                    color=GREY_A).to_edge(UP, buff=0.5)
        line_lab = label(r"dashed: \ the straight line the crowd tends to", font_size=22, color=E.TRUTH)
        line_lab.to_edge(DOWN, buff=0.5)
        tag = agora_tag(r"computed: Agora (random cards)", corner=DR, font_size=17)
        with self.voiceover(
            "With three drinkers the steps are big. <bookmark mark='a'/> Give the market ten buyers, each with a "
            "value drawn at random between nothing and six dollars, and draw how many would buy at each price, as a "
            "share of all of them. <bookmark mark='b'/> With a hundred buyers the steps shrink. "
            "<bookmark mark='c'/> With a thousand, and then ten thousand, the staircase is a smooth line. That's "
            "why textbooks draw demand as a curve: it's a staircase with too many steps to see. "
            "<bookmark mark='d'/> When the values are spread evenly, as these are, the line is straight, and it "
            "hits zero at six dollars, the price nobody will pay."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][3]), Create(panels[0].stairs))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][3]), Create(panels[1].stairs))
            vo.wait_until("c")
            for p in panels[2:]:
                self.play(FadeIn(p[0]), FadeIn(p[3]), Create(p.stairs), run_time=1.0)
            vo.wait_until("d")
            self.play(*[Create(p.ideal) for p in panels], FadeIn(line_lab))
        self.clear_scene()

    def law(self):
        head = heading(r"The law of demand")
        items = [
            (r"more buyers come in", r"at a lower price, \ more people's values are above it", E.DEMAND),
            (r"each buys more", r"at a lower price, \ another cup clears the bar for each of them", ANA),
            (r"what moves the curve", r"income, \ tastes, \ the prices of other goods: \ Parts 5 and 6", GREY_B),
        ]
        pc = point_cards(items, width=12.8, cols=3, font_size=23).move_to(UP * 0.5)
        foot = label(r"the exception, \ Giffen's goods: \ rice in Hunan, \ Part 6", font_size=22, color=GREY_B)
        foot.to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "That gives the law of demand, and both of its reasons. <bookmark mark='a'/> At a lower price, more "
            "people's values clear the bar, so more buyers come in. <bookmark mark='b'/> And each buyer goes "
            "further down her own staircase: another cup becomes worth buying. <bookmark mark='c'/> Everything else "
            "that matters to a buyer, her income, her tastes, the prices of tea and milk, moves the whole curve, and "
            "Parts five and six build it from choices. <bookmark mark='d'/> There are exceptions, goods people buy "
            "more of when they get dearer, and Part six finds one in the data, among poor households buying rice in "
            "China. They are rare, and they need a special kind of poverty."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abc", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
