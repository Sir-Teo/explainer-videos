from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Distribution(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Equality and priority", r"Does it matter how the good is shared?", lit=(1991,),
                            part=PART)
        with self.voiceover("Chapter four. Equality and priority."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.views()
        self.ranked()
        self.levelling()
        self.monster()
        self.pond()

    def views(self):
        head = label(r"Four ways to value a distribution", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        fs = VGroup(MathTex(r"\text{utilitarian: } \sum_i w_i", font_size=30, color=GOOD),
                    MathTex(r"\text{prioritarian: } \sum_i \sqrt{w_i}", font_size=30, color=AGG),
                    MathTex(r"\text{maximin: } \min_i w_i", font_size=30, color=DUTY),
                    MathTex(r"\text{egalitarian: penalize } G = \frac{\sum_{i,j}|w_i - w_j|}{2 n^2 \bar w}", font_size=30,
                            color=VIRT)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-2.0, 0.2, 0])
        side = stack([(r"priority \ (Parfit, \ 1991): \ a benefit matters more the worse off its recipient", AGG),
                      (r"maximin: \ only the worst off counts \ (Rawls's difference principle, \ Part 38)", DUTY),
                      (r"equality: \ inequality itself is bad", VIRT),
                      (r"Atkinson \ (1970): \ $1 - \text{equally distributed equivalent}/\text{mean}$", GREY_A)],
                     font_size=18, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, 0.0, 0])
        with self.voiceover(
            "Utilitarianism adds up welfare and ignores how it is shared. There are three main alternatives. "
            "<bookmark mark='a'/>The utilitarian sum. <bookmark mark='b'/>The prioritarian sum, which counts a "
            "benefit for more the worse off its recipient is, here by adding square roots, as Derek Parfit proposed "
            "in 1991. <bookmark mark='c'/>Maximin, which looks only at the worst off, the core of Rawls's "
            "difference principle in Part 38. <bookmark mark='d'/>And egalitarianism, which holds inequality itself "
            "bad, measured by the Gini index or by Anthony Atkinson's index of 1970, the share of the mean one "
            "would give up for perfect equality."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f, r in zip("abcd", fs, side):
                vo.wait_until(mk)
                self.play(Write(f), FadeIn(r))
        self.clear_scene()

    def ranked(self):
        d = load("distribution")["rows"]
        head = label(r"Three societies, \ five verdicts", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        names = ["equal", "unequal, larger", "spread"]
        assert [d[n]["total"] for n in names] == [50, 60, 50]
        assert [d[n]["gini"] for n in names] == [0.0, 0.3867, 0.08]
        assert [d[n]["prioritarian"] for n in names] == [15.811, 16.125, 15.771]
        hd = [r"\text{society}", r"\text{people}", r"\sum w", r"\sum\sqrt{w}", r"\min", r"\text{Gini}",
              r"\text{Atkinson}_1"]
        cells = []
        for n in names:
            r = d[n]
            cells.append([label(n, font_size=17, color=WHITE), label(r"\ ".join(map(str, r["people"])), font_size=16,
                                                                     color=GREY_A),
                          label(str(r["total"]), font_size=17, color=GOOD), label(f"{r['prioritarian']:.2f}",
                                                                               font_size=17, color=AGG),
                          label(str(r["maximin"]), font_size=17, color=DUTY), label(f"{r['gini']:.3f}", font_size=17,
                                                                                  color=VIRT),
                          label(f"{r['atkinson1']:.3f}", font_size=17, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.6, 1.2, 1.4, 1.0, 1.3, 1.6], cell_h=0.6, font_size=17).move_to(
            [0, 0.5, 0])
        foot = stack([(r"utilitarian and prioritarian: \ the unequal society, \ larger in total", GOOD),
                      (r"maximin: \ the equal society \ (10 against 2)", DUTY),
                      (r"by Gini, \ `spread' beats `unequal' though it is smaller", VIRT)], font_size=19,
                     buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The Reasoner scores three societies of five people. <bookmark mark='a'/>One where everyone has ten; one "
            "larger in total but unequal, from two to twenty six; and one mildly spread, from eight to twelve. "
            "<bookmark mark='b'/>The utilitarian prefers the unequal society, sixty against fifty. With square roots "
            "the prioritarian agrees, but only just, sixteen point one against fifteen point eight. "
            "<bookmark mark='c'/>Maximin prefers the equal society: its worst off has ten, against two. "
            "<bookmark mark='d'/>And the Gini index ranks the mild spread far above the unequal society. Each view "
            "is a different answer to how much a gain for the better off can make up for a loss to the worse off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for k in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[k][:2]], run_time=0.4)
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[k][j]) for k in range(3) for j in (2, 3)], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[k][4]) for k in range(3)], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[k][j]) for k in range(3) for j in (5, 6)], FadeIn(foot[2]))
        self.clear_scene()

    def levelling(self):
        d = load("distribution")["rows"]
        head = label(r"The levelling-down objection \ (Parfit, \ 1991)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        a, b = d["before levelling"], d["levelled down"]
        assert a["people"] == [6, 6, 6, 6, 26] and b["people"] == [6, 6, 6, 6, 6]
        assert (a["gini"], b["gini"]) == (0.32, 0.0) and (a["prioritarian"], b["prioritarian"]) == (14.897, 12.247)
        bars = VGroup()
        for k, (r, x0) in enumerate(((a, -5.4), (b, -1.4))):
            g = VGroup()
            for i, w in enumerate(r["people"]):
                h = 0.14 * w
                g.add(Rectangle(width=0.5, height=h, stroke_width=0, fill_color=GOOD if w < 20 else VIRT,
                                fill_opacity=0.8).move_to([x0 + 0.65 * i, -2.4 + h / 2, 0]))
            g.add(label([r"before", r"after: \ the best off brought down"][k], font_size=17, color=GREY_A).next_to(
                g, DOWN, buff=0.15))
            bars.add(g)
        arrow = Arrow([-2.2, 0.0, 0], [-1.6, 0.0, 0], buff=0, color=HARM)
        side = stack([(r"no one is better off, \ and one person is worse off", HARM),
                      (r"yet inequality falls from Gini 0.32 to 0", VIRT),
                      (r"telic egalitarianism: \ it is better in one respect", VIRT),
                      (r"Parfit: \ that seems absurd; \ so prefer priority", AGG),
                      (r"priority ranks it lower: \ 12.2 against 14.9", AGG)], font_size=19, aligned_edge=LEFT,
                     width=5.0, buff=0.3).move_to([3.9, -0.2, 0])
        with self.voiceover(
            "Derek Parfit's Lindley lecture of 1991 posed the sharpest objection to egalitarianism. "
            "<bookmark mark='a'/>Suppose four people have six and one has twenty six. Now bring the best off down to "
            "six, by some natural disaster that helps no one. <bookmark mark='b'/>No one is better off, and one "
            "person is worse off. <bookmark mark='c'/>Yet inequality has fallen from a Gini of point three two to "
            "zero. <bookmark mark='d'/>An egalitarian who thinks inequality bad in itself must say the levelled world "
            "is better in one respect. Parfit found that absurd, and proposed priority instead: what matters is not "
            "how people compare with each other, but how badly off they are. <bookmark mark='e'/>The prioritarian sum "
            "rightly ranks the levelled world lower."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            self.play(GrowArrow(arrow), FadeIn(bars[1]))
            for mk, r in zip("bcde", [side[0], side[1], VGroup(side[2], side[3]), side[4]]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def monster(self):
        d = load("monster")
        head = label(r"The utility monster \ (Nozick, \ 1974)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        b = d["best"]
        assert (d["k"], d["people"], d["total"]) == (10.0, 10, 100)
        assert b["utilitarian"]["monster"] == 90.91 and b["utilitarian"]["each_other"] == 0.91
        assert (b["prioritarian"]["monster"], b["prioritarian"]["each_other"]) == (31.7, 6.83)
        assert (b["maximin"]["monster"], b["maximin"]["each_other"]) == (0.1, 9.99)
        assert d["utilitarian_exact"] == 90.909
        ax = Axes(x_range=[0, 100, 20], y_range=[0, 1, 0.25], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.7, 0])
        ax.y_axis.numbers.become(VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                                          for t, v in (("0", 0), ("0.5", 0.5), ("1", 1))]))
        xl = label(r"units given to the monster, \ of 100", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN,
                                                                                                buff=0.42)
        yl = label(r"curves: \ each view's value, \ as a share of its best", font_size=15, color=GREY_A).next_to(
            xl, DOWN, buff=0.12)
        cols = {"utilitarian": GOOD, "prioritarian": AGG, "maximin": DUTY}
        curves, peaks = VGroup(), VGroup()
        for name, col in cols.items():
            curves.add(VMobject(color=col, stroke_width=3).set_points_as_corners(
                [ax.c2p(m, v) for m, v in zip(d["curve"]["m"], d["curve"][name])]))
            peaks.add(Dot(ax.c2p(b[name]["monster"], 1.0), radius=0.07, color=col))
        tags = VGroup(label(r"utilitarian: \ 90.9", font_size=15, color=GOOD).next_to(peaks[0], DOWN, buff=0.15),
                      label(r"prioritarian: \ 31.7", font_size=15, color=AGG).next_to(peaks[1], UP, buff=0.12),
                      label(r"maximin: \ 0.1", font_size=15, color=DUTY).next_to(peaks[2], UR, buff=0.08))
        side = stack([(r"ten people, \ welfare $\sqrt{x}$; \ a monster, \ welfare $10\sqrt{x}$", GREY_A),
                      (r"utilitarian: \ the monster takes 90.9, \ each other person 0.9", GOOD),
                      (r"closed form: \ $\frac{k^2}{k^2 + n}\times 100 = \frac{100}{110}\times 100$", GOOD),
                      (r"prioritarian: \ 31.7, \ and 6.8 each", AGG),
                      (r"maximin: \ 0.1, \ and 10.0 each: \ equal welfare", DUTY),
                      (r"``utilitarianism does not take seriously the distinction between persons'' \ (Rawls)",
                       HARM)],
                     font_size=18, aligned_edge=LEFT, width=4.9, buff=0.28).move_to([3.95, -0.3, 0])
        with self.voiceover(
            "Robert Nozick, in Anarchy, State, and Utopia of 1974, imagined a utility monster, who gets, in his "
            "words, enormously greater gains in utility from any sacrifice of others than these others lose. "
            "<bookmark mark='a'/>The Reasoner builds one: ten ordinary people, each with welfare the square root of "
            "their resources, and a monster whose welfare is ten times anyone's from the same resources. There are a "
            "hundred units to share. <bookmark mark='b'/>The utilitarian sum peaks when the monster takes ninety one "
            "of the hundred, leaving each of the others less than one. In closed form, the monster's share is k "
            "squared over k squared plus n, with k and n both ten. <bookmark mark='c'/>The prioritarian, who counts "
            "the square root of each person's welfare, gives it thirty two. <bookmark mark='d'/>Maximin, which looks "
            "only at the worst off, gives it a tenth of a unit, just enough to make it exactly as well off as "
            "everyone else. <bookmark mark='e'/>The monster dramatizes John Rawls's charge that utilitarianism does "
            "not take seriously the distinction between persons: it treats people as containers of welfare, and "
            "pours into whichever container is most efficient."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(curves[0]), run_time=1.5)
            self.play(FadeIn(peaks[0]), FadeIn(tags[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(curves[1]), run_time=1.2)
            self.play(FadeIn(peaks[1]), FadeIn(tags[1]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(curves[2]), run_time=1.2)
            self.play(FadeIn(peaks[2]), FadeIn(tags[2]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def pond(self):
        d = load("pond")
        w = d["world"]
        head = label(r"Famine, \ affluence and morality \ (Singer, \ 1972)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["rich"], d["poor"], d["ratio"], d["best_gift"]) == (50000, 500, 100, 24750)
        assert (w["full_share"], w["alone_share"], w["full_compliance_gift"]) == (0.891, 0.979, 44550)
        assert d["prerogative"] == {"1": 24750, "10": 4091, "100": 0}
        quote = label(r"``if it is in our power to prevent something bad from happening, \ without thereby "
                      r"sacrificing anything of comparable moral importance, \ we ought, \ morally, \ to do it.''",
                      font_size=19, color=WHITE)
        if quote.width > 12.4:
            quote = wrapped_label(r"``if it is in our power to prevent something bad from happening, \ without "
                                  r"thereby sacrificing anything of comparable moral importance, \ we ought, \ "
                                  r"morally, \ to do it.''", 12.0, 19, WHITE)
        quote.next_to(head, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 50000, 10000], y_range=[0, 3.5, 1], x_length=5.8, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15}).move_to([-3.4, -1.3, 0])
        xn = VGroup(*[label(f"{v // 1000}k", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                      for v in (0, 10000, 20000, 30000, 40000, 50000)])
        yn = VGroup(*[label(str(v), font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (0, 1, 2, 3)])
        xl = label(r"your gift, \ in dollars", font_size=16, color=GREY_A).next_to(xn, DOWN, buff=0.15)
        yl = label(r"gain in total welfare, \ $\log$ income", font_size=16, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)
        c = VMobject(color=GOOD, stroke_width=3).set_points_smoothly(
            [ax.c2p(g, v) for g, v in zip(d["gifts"], d["welfare_gain"])])
        top = max(d["welfare_gain"])
        pk = Dot(ax.c2p(24750, top), radius=0.08, color=WHITE)
        pkl = label(r"24,750: \ incomes equal", font_size=15, color=WHITE).next_to(pk, UP, buff=0.12)
        side = stack([(r"welfare $\log$ income: \ a dollar on \$500 is worth 100 times a dollar on \$50,000", GREY_A),
                      (r"two people: \ give until you are equal", GOOD),
                      (r"10 rich, \ 90 poor: \ all comply, \ each gives 89\%; \ you alone, \ 98\%", HARM),
                      (r"Murphy \ (2000): \ never more than your share under full compliance: \ still 89\%", AGG),
                      (r"Scheffler \ (1982): \ weight yourself $M$ times: \ $M = 10$, \ \$4,091; \ $M = 100$, \ "
                       r"nothing", DUTY),
                      (r"demandingness; \ integrity \ (Williams, \ 1973)", VIRT)],
                     font_size=18, aligned_edge=LEFT, width=5.2, buff=0.26).move_to([3.75, -1.0, 0])
        with self.voiceover(
            "In 1972, after the famine and the flood of refugees in East Bengal, Peter Singer published Famine, "
            "Affluence, and Morality. If you walk past a shallow pond and see a child drowning, you ought to wade in, "
            "though it ruins your clothes. <bookmark mark='a'/>Distance, and the number of others who could help, "
            "make no moral difference, so: if it is in our power to prevent something bad from happening, without "
            "thereby sacrificing anything of comparable moral importance, we ought, morally, to do it. "
            "<bookmark mark='b'/>The Reasoner puts numbers to it, with welfare the logarithm of income. A dollar to "
            "someone living on five hundred a year is worth a hundred times a dollar to someone on fifty thousand. "
            "<bookmark mark='c'/>Between two such people, total welfare rises with every dollar given until their "
            "incomes are equal: a gift of twenty four thousand, seven hundred and fifty. <bookmark mark='d'/>In a "
            "world of ten rich and ninety poor, if every rich person complies, each gives eighty nine percent of "
            "their income; if you alone comply, ninety eight. <bookmark mark='e'/>Liam Murphy's cooperative "
            "principle, of 2000, says no one need do more than her share under full compliance; in a world this "
            "unequal, that share is still eighty nine percent. <bookmark mark='f'/>Samuel Scheffler proposed instead, "
            "in 1982, an agent-centred prerogative: you may weight your own welfare above a stranger's, by some "
            "factor M. Weighted ten times, the gift falls to four thousand and ninety one dollars; a hundred times, "
            "to nothing. <bookmark mark='g'/>The demandingness objection, and Bernard Williams's complaint of 1973 "
            "that such a theory alienates agents from their own projects, are the price consequentialism pays for "
            "impartiality."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xn), FadeIn(yn), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(c), run_time=1.5)
            self.play(FadeIn(pk), FadeIn(pkl), FadeIn(side[1]))
            for mk, r in zip("defg", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
