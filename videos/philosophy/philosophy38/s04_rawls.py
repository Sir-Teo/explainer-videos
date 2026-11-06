from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Rawls(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Justice as fairness", r"What would we choose, \ not knowing who we would be?", lit=(1971,), part=PART)
        with self.voiceover("Chapter three. Justice as fairness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.position()
        self.principles()
        self.conditions()
        self.frontier()
        self.regimes()

    def position(self):
        head = history_card(1971, r"John Rawls", r"\textit{A Theory of Justice}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the question", r"which principles would free and equal persons choose to govern the basic structure of their society?", COM),
                (r"the veil of ignorance", r"choose without knowing your class, \ talents, \ race, \ sex, \ conception of the good, \ or even your generation", FAIR),
                (r"primary goods", r"rights, \ liberties, \ opportunities, \ income, \ wealth, \ and the social bases of self-respect: \ what anyone wants, \ whatever else she wants", MKT),
                (r"fairness", r"if the situation of choice is fair, \ so are the principles chosen: \ justice as fairness", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "John Rawls's A Theory of Justice, of 1971, revived the social contract as a thought experiment. "
            "<bookmark mark='a'/>Which principles would free and equal persons choose to govern the basic structure "
            "of their society? <bookmark mark='b'/>Choose them behind a veil of ignorance: without knowing your "
            "class, your talents, your race or sex, your conception of the good life, or even which generation you "
            "belong to. <bookmark mark='c'/>What you do know is that you will want primary goods: rights and "
            "liberties, opportunities, income and wealth, and the social bases of self-respect, things anyone wants "
            "whatever else she wants. <bookmark mark='d'/>If the situation of choice is fair, so are the principles "
            "chosen in it: justice as fairness."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def principles(self):
        head = label(r"The two principles", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"first", r"each person has an equal right to the most extensive scheme of equal basic liberties compatible with a similar scheme for all", LIB),
                (r"second (a)", r"offices and positions open to all under fair equality of opportunity", FAIR),
                (r"second (b)", r"the difference principle: \ social and economic inequalities are to be to the greatest benefit of the least advantaged", FAIR),
                (r"lexical order", r"the first principle before the second: \ no trade of basic liberty for economic gain", GOAL),
                (r"the argument", r"behind the veil, \ reason as if your place will be assigned by your enemy: \ maximin", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Rawls argued that the parties would choose two principles. <bookmark mark='a'/>First, each person has an "
            "equal right to the most extensive scheme of equal basic liberties compatible with a similar scheme for "
            "all. <bookmark mark='b'/>Second, offices and positions must be open to all under fair equality of "
            "opportunity, <bookmark mark='c'/>and social and economic inequalities must be to the greatest benefit of "
            "the least advantaged: the difference principle. <bookmark mark='d'/>The first principle has lexical "
            "priority over the second: no basic liberty may be traded for economic gain. <bookmark mark='e'/>His "
            "central argument was that, behind the veil, a rational person would choose as if her place would be "
            "assigned by her enemy: the maximin rule, which the next chapter puts to the test."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def frontier(self):
        d = load("difference")
        pts = d["points"]
        head = label(r"The difference principle, \ drawn", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert pts["equality"] == {"t": 0.0, "uA": 5.0, "uL": 5.0}
        assert pts["difference"] == {"t": 1.0, "uA": 8.0, "uL": 6.0}
        assert pts["utilitarian"] == {"t": 2.5, "uA": 12.5, "uL": 3.75}
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 7, 1], x_length=6.2, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([-3.2, -0.6, 0])
        xl = label(r"the more advantaged", font_size=16, color=MKT).next_to(ax.x_axis, DOWN, buff=0.42)
        yl = label(r"the least advantaged", font_size=16, color=FAIR).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        curve = VMobject(color=COM, stroke_width=3).set_points_smoothly([ax.c2p(a, l) for a, l in zip(d["uA"], d["uL"])])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(7, 7), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(pts[k]["uA"], pts[k]["uL"]), radius=0.08, color=c) for k, c in
                        (("equality", GREY_A), ("difference", FAIR), ("utilitarian", MKT))])
        tags = VGroup(label(r"equality", font_size=15, color=GREY_A).next_to(dots[0], LEFT, buff=0.12),
                      label(r"difference principle", font_size=15, color=FAIR).next_to(dots[1], UP, buff=0.12),
                      label(r"utilitarian", font_size=15, color=MKT).next_to(dots[2], UP, buff=0.12))
        side = stack([(r"incentives for the advantaged raise output, \ and at first everyone's prospects", COM),
                      (r"equality: \ (5, 5)", GREY_A),
                      (r"difference principle: \ as much as possible for the least advantaged: \ (8, 6)", FAIR),
                      (r"utilitarian: \ the largest sum, \ 16.25: \ (12.5, 3.75)", MKT),
                      (r"inequality is just only if it works to the benefit of the least advantaged", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "Here is the difference principle, drawn. <bookmark mark='a'/>Suppose that letting the more advantaged "
            "keep more, as an incentive, raises output, and at first raises everyone's prospects; past a point, the "
            "extra goes to them alone, and the least advantaged lose. The curve shows the possibilities. <bookmark "
            "mark='b'/>Strict equality sits on the diagonal: five each. <bookmark mark='c'/>The difference principle "
            "picks the highest point for the least advantaged: eight and six. They are better off than under "
            "equality, so this inequality is justified to them. <bookmark mark='d'/>The utilitarian picks the largest "
            "sum, twelve and a half and three and three quarters, sacrificing the worst off for a larger total. "
            "<bookmark mark='e'/>Inequality, on Rawls's view, is just only if it works to the benefit of the least "
            "advantaged."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(diag))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]), run_time=1.5)
            for mk, k in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(dots[k]), FadeIn(tags[k]), FadeIn(side[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def conditions(self):
        head = label(r"When is maximin rational? \ (Rawls, \ 1971, \ \S 26)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"no probabilities", r"behind a thick veil there is no basis for estimating the chance of being anyone", GREY_A),
                (r"a guaranteed minimum", r"the chooser cares little for what he might gain above what the principles guarantee", FAIR),
                (r"grave risks", r"the rejected alternatives have outcomes one could hardly accept: \ slavery, \ persecution", BAD),
                (r"the verdict", r"all three hold in the original position, \ Rawls argued: \ so maximin is rational there, \ though not in ordinary choice", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Rawls did not claim that maximin is rational in general; it is not, as Harsanyi pointed out. He claimed it is "
            "rational in the original position, because three conditions hold there. <bookmark mark='a'/>First, the "
            "veil is thick: there is no basis for estimating the chance of being anyone in particular. <bookmark "
            "mark='b'/>Second, the chooser cares little for what he might gain above the minimum the principles "
            "guarantee, since that minimum is a decent life. <bookmark mark='c'/>Third, the alternatives have "
            "outcomes one could hardly accept, such as slavery or persecution, if one landed in the wrong place. "
            "<bookmark mark='d'/>When all three hold, he argued, it is wise to choose as if one's enemy will assign "
            "one's place. Each condition has been disputed, and the next chapter tests what happens when they are "
            "relaxed."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def regimes(self):
        head = label(r"Which economy? \ (Rawls, \ 2001)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"laissez-faire capitalism", r"formal equality of opportunity only: \ fails both principles", BAD),
                (r"welfare-state capitalism", r"a decent minimum, \ but a small class controls the economy and politics", BAD),
                (r"state socialism", r"a command economy under one party: \ fails the first principle", BAD),
                (r"property-owning democracy", r"disperse wealth and capital before the market runs \ (Meade, \ 1964): \ passes", FAIR),
                (r"liberal socialism", r"democratic, \ socially owned firms in competitive markets: \ passes", FAIR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Late in life, in Justice as Fairness: A Restatement, of 2001, Rawls asked which economic system could "
            "realize his principles. <bookmark mark='a'/>Laissez-faire capitalism secures only formal equality of "
            "opportunity, and fails both. <bookmark mark='b'/>Welfare-state capitalism, surprisingly, also fails: it "
            "provides a decent minimum after the fact, but lets a small class control the economy, and through it, "
            "politics. <bookmark mark='c'/>State socialism with a command economy fails the first principle. "
            "<bookmark mark='d'/>A property-owning democracy, a term from the economist James Meade, passes: it "
            "disperses wealth and capital before the market runs, rather than redistributing afterwards. <bookmark "
            "mark='e'/>So does liberal socialism, with democratic, socially owned firms competing in markets. Which "
            "of the two suits a society depends on its history."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
