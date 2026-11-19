from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Diamonds(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Water and diamonds", r"Why is the most useful thing nearly free?",
             "Chapter one. Water and diamonds.", lit={1776: r"Smith's paradox", 1871: r"Jevons and Menger"},
             scale=("person", "market"), horizon=("a day",))
        self.paradox()
        self.cost()
        self.margin()
        self.solved()

    # ------------------------------------------------------------------
    def paradox(self):
        q = quote_card(r"Nothing is more useful than water; but it will purchase scarce any thing; scarce any thing "
                       r"can be had in exchange for it. A diamond, on the contrary, has scarce any value in use; but a "
                       r"very great quantity of other goods may frequently be had in exchange for it.",
                       r"Adam Smith, \emph{The Wealth of Nations} (1776), Book I, ch.~4", width=11.6, font_size=30)
        q.to_edge(UP, buff=0.6)
        two = VGroup(
            VGroup(label(r"value in use", font_size=30, color=E.DEMAND),
                   label(r"how useful a thing is", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.12),
            VGroup(label(r"value in exchange", font_size=30, color=E.ACCENT),
                   label(r"what it will buy: \ its price", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=2.4).next_to(q, DOWN, buff=0.7)
        drop = drop_glyph(0.9).next_to(two[0], DOWN, buff=0.4)
        gem = gem_glyph(1.1).next_to(two[1], DOWN, buff=0.45)
        src = published_tag(r"Smith (1776), Book I, ch.~4 (Project Gutenberg text)", corner=DR, font_size=17)
        with self.voiceover(
            "Adam Smith put the puzzle in 1776. <bookmark mark='a'/> Nothing is more useful than water, he wrote, "
            "but it will purchase scarce anything; scarce anything can be had in exchange for it. A diamond, on the "
            "contrary, has scarce any value in use, but a very great quantity of other goods may frequently be had "
            "in exchange for it. <bookmark mark='b'/> So Smith split value in two. Value in use is how useful a "
            "thing is. Value in exchange is what it will buy, which is its price. And the two, it seemed, had "
            "nothing to do with each other."
        ) as vo:
            self.play(FadeIn(src), FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(two[0]), FadeIn(drop))
            self.play(FadeIn(two[1]), FadeIn(gem))
        self.clear_scene()

    def cost(self):
        ric = history_card(1817, r"David Ricardo, \ \emph{Principles of Political Economy}",
                           r"the exchange value of most goods is set by the labour it takes to make them",
                           color=E.SUPPLY, width=6.2, font_size=24)
        marx = history_card(1867, r"Karl Marx, \ \emph{Capital}", r"value as the labour time socially necessary "
                            r"to produce a thing", color=E.MISS, width=6.2, font_size=24)
        VGroup(ric, marx).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(UP, buff=0.5)
        pearl = quote_card(r"It is not that pearls fetch a high price because men have dived for them; but on the "
                           r"contrary, men dive for them because they fetch a high price.",
                           r"Richard Whately, \emph{Introductory Lectures on Political Economy} (1832), Lecture IX",
                           width=11.4, font_size=30, color=E.DEMAND).to_edge(DOWN, buff=0.7)
        src = published_tag(r"Whately (2nd ed., 1832), Lecture IX (Internet Archive scan)", corner=DR, font_size=17)
        with self.voiceover(
            "The classical economists who followed Smith looked to the cost side. <bookmark mark='a'/> David "
            "Ricardo argued in 1817 that what most goods exchange for is set by the labour it takes to make them; "
            "diamonds are dear because finding one takes a great deal of work. <bookmark mark='b'/> Karl Marx built "
            "his economics on a version of the same idea fifty years later. <bookmark mark='c'/> But the cost theory "
            "has a hole in it, and a churchman named Richard Whately pointed at it. It is not, he said, that pearls "
            "fetch a high price because men have dived for them; on the contrary, men dive for them because they "
            "fetch a high price. Work spent making something nobody wants gives it no value at all."
        ) as vo:
            self.play(FadeIn(ric, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(marx, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(pearl, shift=UP * 0.2), FadeIn(src))
        self.clear_scene()

    def margin(self):
        d = load("diamonds")
        q, mv = np.array(d["q"]), np.array(d["mv"])
        cap = 12.0
        ax = price_axes(200, (0, cap), x_length=10.4, y_length=3.9, qticks=[0, 50, 100, 150, 200],
                        pticks=[0, 4, 8, 12], qlabel=r"litres of water a day, already in hand",
                        plabel=r"what one more litre is worth to you", center=DOWN * 1.05 + LEFT * 0.4)
        a = ax.ax
        pts = [a.c2p(x, min(y, cap)) for x, y in zip(q, mv)]
        curve = VMobject(stroke_color=WATER, stroke_width=4).set_points_smoothly(pts[::2])
        k = int(np.searchsorted(q, d["used"]))
        area = Polygon(a.c2p(0, 0), *[a.c2p(x, min(y, cap)) for x, y in zip(q[:k + 1:2], mv[:k + 1:2])],
                       a.c2p(q[k], 0), stroke_width=0, fill_color=WATER, fill_opacity=0.22)
        edge = DashedLine(a.c2p(q[k], 0), a.c2p(q[k], 3.0), color=GREY_B)
        dot = Dot(a.c2p(q[k], mv[k]), radius=0.08, color=E.ACCENT)
        lab_first = label(r"the first litres: \ life itself \ (off the scale)", font_size=22, color=WATER)
        lab_first.next_to(a.c2p(34, cap), RIGHT, buff=0.2)
        lab_total = label(r"total value: \ the whole shaded area", font_size=24, color=WHITE).move_to(a.c2p(48, 1.4))
        lab_price = label(r"the price: \ the value of the last litre", font_size=24, color=E.ACCENT)
        lab_price.move_to(a.c2p(165, 4.2))
        arrow = Arrow(lab_price.get_bottom(), dot.get_center(), buff=0.1, color=E.ACCENT, stroke_width=3,
                      max_tip_length_to_length_ratio=0.15)
        names = VGroup(
            history_card(1871, r"William Stanley Jevons", r"\emph{The Theory of Political Economy}", color=E.DEMAND,
                         width=4.1, font_size=19),
            history_card(1871, r"Carl Menger", r"\emph{Principles of Economics}", color=E.DEMAND, width=4.1,
                         font_size=19),
            history_card(1874, r"L\'eon Walras", r"\emph{Elements of Pure Economics}", color=E.DEMAND, width=4.1,
                         font_size=19),
        ).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.4)
        tag = illustrative_tag(r"illustrative: a falling value for each further litre", corner=DL, font_size=17)
        with self.voiceover(
            "The answer came in the 1870s, from three economists working separately: William Stanley Jevons in "
            "England, Carl Menger in Vienna and Léon Walras in Lausanne. <bookmark mark='a'/> Their idea was to "
            "ask what one more unit is worth, given what you already have. Here is what one more litre of water a "
            "day might be worth to you. <bookmark mark='b'/> The first few litres are worth almost anything: "
            "they keep you alive. The next ones wash you and cook your food. <bookmark mark='c'/> By the time you "
            "have a hundred and fifty litres a day, one more is worth almost nothing; you'd water the garden with "
            "it. <bookmark mark='d'/> Smith's value in use is the whole area under the curve, and it's enormous. "
            "<bookmark mark='e'/> But a price is paid for one more litre, and it's the height of the curve where "
            "you stop. Water is cheap because we have so much of it that the last litre is worth very little."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.2) for n in names], lag_ratio=0.3), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(curve), run_time=2.5)
            self.play(FadeIn(lab_first))
            vo.wait_until("c")
            self.play(Create(edge), FadeIn(dot, scale=0.5))
            vo.wait_until("d")
            self.play(FadeIn(area), FadeIn(lab_total))
            vo.wait_until("e")
            self.play(FadeIn(lab_price), GrowArrow(arrow))
            self.play(Indicate(dot, color=E.ACCENT, scale_factor=1.6))
        self.clear_scene()

    def solved(self):
        left = panel(6.2, 4.4, center=[-3.4, -0.2, 0])
        right = panel(6.2, 4.4, center=[3.4, -0.2, 0])
        drop = drop_glyph(1.0).move_to(left.get_top() + DOWN * 0.9)
        gem = gem_glyph(1.2).move_to(right.get_top() + DOWN * 0.9)
        lw = VGroup(label(r"so much of it", font_size=28, color=WATER),
                    label(r"the last litre is worth almost nothing", font_size=22, color=GREY_A),
                    label(r"low price, \ huge total value", font_size=26, color=WHITE)).arrange(DOWN, buff=0.18)
        lw.next_to(drop, DOWN, buff=0.4)
        rw = VGroup(label(r"so little of it", font_size=28, color=DIAMOND),
                    label(r"the last carat is still wanted badly", font_size=22, color=GREY_A),
                    label(r"high price, \ small total value", font_size=26, color=WHITE)).arrange(DOWN, buff=0.18)
        rw.next_to(gem, DOWN, buff=0.4)
        bottom = label(r"a price measures the margin, \ not the whole", font_size=34, color=E.ACCENT).to_edge(DOWN,
                                                                                                           buff=0.4)
        with self.voiceover(
            "That dissolves Smith's paradox. <bookmark mark='a'/> Water is so plentiful that the last litre is "
            "worth almost nothing, even though water as a whole is worth more than anything. <bookmark mark='b'/> "
            "Diamonds are so scarce that the last carat is still wanted badly, even though diamonds as a whole "
            "matter very little. <bookmark mark='c'/> A price measures the margin, not the whole. That's the "
            "first half of the answer to this part's question, the half that comes from buyers. The other half "
            "comes from what it costs to supply one more unit, and that's where Ricardo was right after all."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), FadeIn(drop), FadeIn(gem))
            vo.wait_until("a")
            self.play(FadeIn(lw, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rw, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(bottom, shift=UP * 0.1))
        self.clear_scene()
