from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


def carriage(kind: str, width: float = 3.0) -> VGroup:
    """A railway carriage: first class closed and padded, second with a roof, third open to the weather."""
    body = Rectangle(width=width, height=0.9, stroke_color=GREY_B, stroke_width=2,
                     fill_color={"first": "#5B4A7A", "second": "#3E5C7A", "third": "#5A4A36"}[kind], fill_opacity=0.85)
    wheels = VGroup(*[Circle(radius=0.16, color=GREY_B, stroke_width=2, fill_color=BLACK, fill_opacity=1).move_to(
        body.get_bottom() + RIGHT * dx * width * 0.32 + DOWN * 0.12) for dx in (-1, 1)])
    g = VGroup(body, wheels)
    if kind in ("first", "second"):
        roof = Polygon(body.get_corner(UL) + LEFT * 0.08, body.get_corner(UR) + RIGHT * 0.08,
                       body.get_corner(UR) + UP * 0.25 + LEFT * 0.2, body.get_corner(UL) + UP * 0.25 + RIGHT * 0.2,
                       stroke_color=GREY_B, stroke_width=2, fill_color="#2E2E38", fill_opacity=0.95)
        g.add(roof)
        n = 3 if kind == "first" else 4
        for k in range(n):
            g.add(Rectangle(width=width / (n + 1.5), height=0.4, stroke_color=GREY_A, stroke_width=1.2,
                            fill_color="#F2D98B" if kind == "first" else "#9FB8F2", fill_opacity=0.35).move_to(
                body.get_center() + RIGHT * (k - (n - 1) / 2) * width / (n + 0.5) + UP * 0.08))
    else:
        for k in range(5):
            g.add(Line(body.get_top() + RIGHT * (k - 2) * width / 5.5, body.get_top() + RIGHT * (k - 2) * width / 5.5
                       + DOWN * 0.35, color=GREY_B, stroke_width=2))
    return g


def rain(area, n=60, seed=3):
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = area
    return VGroup(*[Line([x, y, 0], [x - 0.06, y - 0.25, 0], color="#7EC8F5", stroke_width=1.5, stroke_opacity=0.7)
                    for x, y in zip(rng.uniform(x0, x1, n), rng.uniform(y0, y1, n))])


class Hook(VoiceoverScene):
    def construct(self):
        self.bridge()
        self.carriages()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def bridge(self):
        hc = history_card(1844, r"Jules Dupuit, \ an engineer of the Ponts et Chauss\'ees", r"``On the measurement of "
                          r"the utility of public works'': \ what a bridge is worth to those who cross it is more than "
                          r"what they pay to cross", color=E.ACCENT, width=11.4, font_size=24).to_edge(UP, buff=0.5)
        deck = Line(LEFT * 4.5, RIGHT * 4.5, color=GREY_B, stroke_width=6).shift(DOWN * 1.2)
        arches = VGroup(*[ArcBetweenPoints(LEFT * 4.5 + RIGHT * 3 * k + DOWN * 1.2, LEFT * 1.5 + RIGHT * 3 * k +
                                           DOWN * 1.2, angle=-PI * 0.6, color=GREY_B, stroke_width=4) for k in range(3)])
        water = VGroup(*[ArcBetweenPoints(LEFT * 0.3 + RIGHT * x + DOWN * 3.45, RIGHT * 0.3 + RIGHT * x + DOWN * 3.45,
                                          angle=-PI / 2, color="#5DADEC", stroke_width=2) for x in np.arange(-5, 5.5, 0.8)])
        toll = VGroup(Rectangle(width=0.6, height=0.8, stroke_color=E.ACCENT, stroke_width=2, fill_color="#3A3020",
                                fill_opacity=1), label(r"toll", font_size=18, color=E.ACCENT)).arrange(DOWN, buff=0.05)
        toll.next_to(deck, UP, buff=0.02).shift(LEFT * 3.8)
        rows = VGroup(
            label(r"a crossing costs the bridge almost nothing", font_size=24),
            label(r"a toll keeps away everyone who values crossing less than the toll", font_size=24, color=HOLD),
            label(r"the value they lose is lost to everyone", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.18).next_to(deck, DOWN, buff=0.45)
        tag = published_tag(r"Dupuit, Annales des ponts et chauss\'ees (1844)", corner=DR, font_size=14)
        with self.voiceover(
            "In 1844 a French engineer of the corps of bridges and roads, Jules Dupuit, asked what a bridge is worth. "
            "<bookmark mark='a'/> Not what it cost, he argued, and not what the tolls bring in. It is worth what "
            "crossing it is worth to everyone who crosses, and that is more than they pay. <bookmark mark='b'/> "
            "Once the bridge is built, one more crossing costs almost nothing. <bookmark mark='c'/> So a toll does "
            "something strange: it turns away people who would gain from crossing, at no saving to anyone. "
            "<bookmark mark='d'/> The value they lose is simply lost. Dupuit had invented consumer surplus and "
            "deadweight loss in one argument."
        ) as vo:
            self.play(FadeIn(tag), Create(deck), Create(arches), FadeIn(water), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(toll), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def carriages(self):
        cars = VGroup(*[VGroup(carriage(k), label(t, font_size=20, color=GREY_A)) for k, t in
                        (("first", r"first class"), ("second", r"second class"), ("third", r"third class"))])
        for c in cars:
            c[1].next_to(c[0], DOWN, buff=0.25)
        cars.arrange(RIGHT, buff=0.5).move_to(UP * 0.9)
        wet = rain((cars[2].get_left()[0], cars[2].get_right()[0], cars[2].get_top()[1], cars[2].get_top()[1] + 1.4))
        hc = history_card(1849, r"Dupuit, \ on tolls and railway fares", r"the railway companies leave third-class "
                          r"carriages open and the benches bare, \ he argued, \ not to save the cost of a roof, \ but to "
                          r"keep passengers who could pay for second class from travelling third", color=HOLD, width=11.6,
                          font_size=23).to_edge(DOWN, buff=0.5)
        note_ = label(r"Dupuit's argument, \ paraphrased", font_size=16, color=GREY_B).next_to(hc, UP, buff=0.1
                                                                                              ).align_to(hc, RIGHT)
        with self.voiceover(
            "Five years later he looked at the railways. <bookmark mark='a'/> French trains ran first, second and "
            "third classes, and in Dupuit's telling the third-class carriages were open to the weather, with bare "
            "benches. <bookmark mark='b'/> It wasn't, Dupuit argued, to save the few thousand francs a roof would "
            "cost. It was to make third class unpleasant enough that anyone who could afford second class would pay "
            "for it. The company hurt the poor passenger not to hurt him, but to keep the richer one from trading "
            "down. <bookmark mark='c'/> A seller who can set her own prices does not just pick a number. She "
            "designs a menu, and sometimes she makes part of it worse on purpose."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cars], lag_ratio=0.3), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(wet))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(note_))
            vo.wait_until("c")
            self.play(Indicate(cars[2], color=HOLD, scale_factor=1.04))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"fare classes", r"the cheapest seat with no bag \\ and no choice of seat", DEM),
            (r"software tiers", r"the same program, \\ features switched off", MR),
            (r"discounts", r"students, \ pensioners, \\ coupons, \ early birds", CS),
            (r"subscriptions", r"a fee to join, \\ a price per use", PROFIT),
            (r"bundles", r"channels, \ albums, \\ suites of programs", STUD),
            (r"personal prices", r"a price for you, \\ from your data", DWL),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"Dupuit's carriages, \ everywhere", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "That idea is everywhere now. <bookmark mark='a'/> The cheapest airline seat that won't let you choose "
            "your seat or bring a bag. The same software with features switched off. Discounts for students and "
            "pensioners, and coupons for anyone patient enough to clip them. A fee to join a club, and a price for "
            "each visit. Channels sold in bundles. And now prices tailored to each customer from their data. "
            "<bookmark mark='b'/> Every one of these is a way of charging different people different amounts for "
            "nearly the same thing, and this part takes them one at a time."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what price does a single seller choose, \ and what does it cost the rest of us?", font_size=29,
                  color=PROFIT),
            label(r"how does she charge different buyers different prices?", font_size=29, color=STUD),
            label(r"and what should a regulator do about it?", font_size=29, color=CS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part nine assumed that nobody sets prices. This part asks: what does a seller do when the price is hers "
            "to set? <bookmark mark='a'/> What price does a single seller choose, and what does it cost everyone "
            "else? <bookmark mark='b'/> How does she charge different buyers different prices? <bookmark mark='c'/> "
            "And what should a regulator do about it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = ferry_glyph(1.8)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 10 \ $\cdot$ \ The Price Maker", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part ten: the price maker."):
            self.play(FadeIn(logo, shift=RIGHT * 0.3), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act III \ $\cdot$ \ Markets", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"set a fare yourself; \ marginal revenue, \ the monopoly price, \ the Lerner index",
            r"what monopoly costs: \ Harberger's triangles, \ Posner's rectangles",
            r"price discrimination of three kinds; \ two-part tariffs; \ bundling",
            r"durable goods and the Coase conjecture; \ natural monopoly, \ Ramsey prices, \ regulation",
            r"monopsony, \ pass-through from bean to shelf, \ markups, \ and prices set by machine learning",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Three, on markets, with the simplest market power: one seller. "
            "<bookmark mark='a'/> You'll set a fare yourself, and then we'll derive marginal revenue, the monopoly "
            "price and the Lerner index. <bookmark mark='b'/> We'll ask what monopoly costs, with two famous and "
            "very different answers. <bookmark mark='c'/> Then price discrimination, in three kinds, two-part "
            "tariffs and bundling. <bookmark mark='d'/> Durable goods and a conjecture of Coase's; natural "
            "monopolies and the prices a regulator should set. <bookmark mark='e'/> And an employer with no "
            "rivals, how cost changes reach shelf prices, how large markups are, and prices set by machine learning."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
