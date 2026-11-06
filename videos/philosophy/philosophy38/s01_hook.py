from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.flute()
        self.societies()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Justice is the first virtue of social institutions, \ as truth is of systems of thought.",
                       r"John Rawls", r"\textit{A Theory of Justice} \ (1971), \ \S 1", width=8.8,
                       font_size=30).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Parts 35 to 37 asked what a person ought to do, and what claims about it are. This part asks what a "
            "society owes its members, and what they owe one another. <bookmark mark='a'/>John Rawls began A Theory "
            "of Justice, in 1971, with a sentence that sets the stakes: justice is the first virtue of social "
            "institutions, as truth is of systems of thought. <bookmark mark='b'/>A theory, however elegant, must be "
            "rejected if it is untrue; laws and institutions, however efficient, must be reformed or abolished if "
            "they are unjust."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=FAIR, scale_factor=1.03))
        self.clear_scene()

    def flute(self):
        head = label(r"One flute, \ three children \ (Sen, \ 2009)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        flute = label(r"one flute", font_size=30, color=WHITE).move_to([0, 1.5, 0])
        kids = [(r"Anne", r"``I am the only one who can play it''", r"the utilitarian: \ the greatest enjoyment", MKT),
                (r"Bob", r"``I am poor, \ and have no toys at all''", r"the egalitarian: \ the worst off", FAIR),
                (r"Carla", r"``I made it, \ with my own hands''", r"the libertarian: \ the fruits of one's labour", LIB)]
        cards = VGroup()
        for name, claim, view, c in kids:
            box = RoundedRectangle(width=4.1, height=2.3, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                   fill_color="#0B0F17", fill_opacity=0.9)
            txt = VGroup(label(name, font_size=28, color=c), wrapped_label(claim, 3.7, 20, WHITE)).arrange(DOWN, buff=0.2)
            txt.move_to(box)
            tag = wrapped_label(view, 3.9, 19, c)
            cards.add(VGroup(VGroup(box, txt), tag))
        for i, cd in enumerate(cards):
            cd[0].move_to([(i - 1) * 4.4, -0.4, 0])
            cd[1].next_to(cd[0], DOWN, buff=0.25)
        lines = VGroup(*[Line(flute.get_bottom(), cd[0].get_top(), color=GREY_C, stroke_width=1.5) for cd in cards])
        with self.voiceover(
            "Amartya Sen opens The Idea of Justice, of 2009, with three children and a flute. <bookmark "
            "mark='a'/>Anne says the flute should be hers, because she is the only one who can play it. <bookmark "
            "mark='b'/>Bob says it should be his, because he is so poor that he has no toys at all. <bookmark "
            "mark='c'/>Carla says it should be hers, because she made it, with her own labour. <bookmark "
            "mark='d'/>Each claim is serious, and each has a theory behind it: the utilitarian looks to Anne's "
            "enjoyment, the egalitarian to Bob's need, and the libertarian to Carla's work. Sen's point is that no "
            "one needs to be confused or selfish to disagree here."
        ) as vo:
            self.play(FadeIn(head), FadeIn(flute))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(cards[i][0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(cd[1]) for cd in cards], lag_ratio=0.4))
        self.clear_scene()

    def societies(self):
        d = load("three")
        S = d["societies"]
        assert (d["total"], d["maximin"], d["equality"]) == ("C", "B", "A")
        assert [S[k]["gini"] for k in "ABC"] == [0.0, 0.169, 0.427]
        assert [S[k]["total"] for k in "ABC"] == [50.0, 90.0, 150.0] and [S[k]["minimum"] for k in "ABC"] == [10.0, 12.0, 6.0]
        head = label(r"Three societies, \ five people each", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        xs, base, sc = {"A": -4.4, "B": 0.0, "C": 4.4}, -1.1, 0.038
        cols = {"A": FAIR, "B": LIB, "C": MKT}
        groups, stats, tops = {}, {}, {}
        for k in "ABC":
            bars = VGroup()
            for i, v in enumerate(S[k]["incomes"]):
                r = Rectangle(width=0.5, height=v * sc, stroke_width=1, stroke_color=cols[k], fill_color=cols[k],
                              fill_opacity=0.6)
                r.move_to([xs[k] + (i - 2) * 0.62, base + v * sc / 2, 0])
                bars.add(VGroup(r, label(f"{v}", font_size=16, color=GREY_A).next_to(r, UP, buff=0.06)))
            axis = Line([xs[k] - 1.6, base, 0], [xs[k] + 1.6, base, 0], color=GREY_C, stroke_width=1.5)
            name = label(rf"society {k}", font_size=24, color=cols[k]).move_to([xs[k], base - 0.35, 0])
            groups[k] = VGroup(axis, bars, name)
            stats[k] = VGroup(label(rf"total {S[k]['total']:g}", font_size=19),
                              label(rf"least {S[k]['minimum']:g}", font_size=19),
                              label(rf"Gini {S[k]['gini']:.2f}", font_size=19)).arrange(DOWN, buff=0.12)
            stats[k].next_to(name, DOWN, buff=0.2)
            tops[k] = max(b.get_top()[1] for b in bars)
        tags = {"C": r"largest total", "B": r"best-off worst-off", "A": r"most equal"}
        tag = {k: label(tags[k], font_size=22, color=GOAL).move_to([xs[k], max(tops.values()) + 0.45, 0]) for k in "ABC"}
        boxes = {k: SurroundingRectangle(groups[k][1], color=GOAL, buff=0.12) for k in "ABC"}
        nozick = label(r"Nozick: \ none of these numbers settles it; \ ask how each came about", font_size=22,
                       color=POW).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the question in its simplest form. <bookmark mark='a'/>Three societies of five people each; the "
            "bars are incomes. In society A, everyone has ten. In B, incomes run from twelve to twenty eight. In C, "
            "from six to seventy two. <bookmark mark='b'/>The Reasoner computes, for each, the total, the least "
            "income, and the Gini coefficient of inequality: fifty, ninety and a hundred and fifty in total; ten, "
            "twelve and six at the bottom; and Ginis of zero, point one seven and point four three. <bookmark "
            "mark='c'/>A principle that maximizes the total picks C. <bookmark mark='d'/>One that makes the worst-off "
            "person as well off as possible picks B. <bookmark mark='e'/>One that minimizes inequality picks A. "
            "<bookmark mark='f'/>And Robert Nozick would say that none of these numbers settles anything: what "
            "matters is how each distribution came about. Each of these four answers has a great book behind it, and "
            "this part builds them all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(groups[k]) for k in "ABC"])
            vo.wait_until("b")
            self.play(*[FadeIn(stats[k]) for k in "ABC"])
            for mk, k in zip("cde", "CBA"):
                vo.wait_until(mk)
                if k != "C":
                    self.play(FadeOut(boxes[prev]), run_time=0.4)
                self.play(Create(boxes[k]), FadeIn(tag[k]))
                prev = k
            vo.wait_until("f")
            self.play(FadeOut(boxes[prev]), FadeIn(nozick))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Thrasymachus, \ Gyges, \ and justice in Plato's city and soul",
            r"the social contract: \ Hobbes, \ Locke, \ Rousseau, \ and Hume's objection",
            r"Rawls: \ the original position, \ two principles, \ the difference principle drawn",
            r"maximin against the average: \ 200 societies chosen behind the veil",
            r"Nozick's entitlement theory; \ Wilt Chamberlain, \ run; \ the Price List",
            r"equality of what? \ Dworkin's auction, \ built; \ Anderson; \ capabilities",
            r"Sen's liberal paradox, \ searched \ (the Wall); \ liberty, \ three ways",
            r"fair division, \ built; \ community and role; \ justice beyond borders",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Thrasymachus's challenge, the ring of Gyges, and Plato's answer in the "
            "city and the soul. <bookmark mark='b'/>The social contract, from Hobbes, Locke and Rousseau, and Hume's "
            "objection to it. <bookmark mark='c'/>Rawls's original position and his two principles, with the "
            "difference principle drawn. <bookmark mark='d'/>Maximin against the average, with two hundred societies "
            "chosen behind the veil. <bookmark mark='e'/>Nozick's entitlement theory, Wilt Chamberlain run as a toy "
            "economy, and a Price List. <bookmark mark='f'/>Equality of what: Dworkin's auction, built, Elizabeth "
            "Anderson's critique, and capabilities. <bookmark mark='g'/>Sen's liberal paradox, checked by exhaustive "
            "search, which is this part's brick in the Wall, and three ideas of liberty. <bookmark mark='h'/>And fair "
            "division, built, from cake cutting to rent; then community, role, and justice beyond borders."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
