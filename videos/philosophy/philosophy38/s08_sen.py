from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Sen(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The liberal paradox", r"Can society respect both liberty and unanimity?", lit=(1970,), part=PART)
        with self.voiceover("Chapter seven. The liberal paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lady()
        self.theorem()
        self.search()
        self.responses()
        self.wall_brick()

    def lady(self):
        d = load("sen")["sen"]
        assert d["prude"] == ["n", "p", "l"] and d["lewd"] == ["p", "l", "n"]
        assert [s[:2] for s in d["social"]] == [["n", "p"], ["l", "n"], ["p", "l"]]
        head = label(r"\textit{Lady Chatterley's Lover} \ (Sen, \ 1970)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pos = {"n": np.array([-3.3, 1.3, 0]), "p": np.array([-5.5, -2.1, 0]), "l": np.array([-1.1, -2.1, 0])}
        nodes = {k: VGroup(Circle(radius=0.42, color=LIB, fill_opacity=0.15, stroke_width=3).move_to(pos[k]),
                           MathTex(k, font_size=40).move_to(pos[k])) for k in pos}
        tags = {"n": label(r"no one reads it", font_size=19, color=GREY_A).next_to(nodes["n"], UP, buff=0.15),
                "p": label(r"the prude reads it", font_size=19, color=GREY_A).next_to(nodes["p"], DOWN, buff=0.15),
                "l": label(r"the lewd reads it", font_size=19, color=GREY_A).next_to(nodes["l"], DOWN, buff=0.15)}

        def arrow(a, b, c):
            s, e = pos[a], pos[b]
            u = (e - s) / np.linalg.norm(e - s)
            return Arrow(s + u * 0.48, e - u * 0.48, buff=0, color=c, stroke_width=6,
                         max_tip_length_to_length_ratio=0.1)

        cols = [POW, MKT, FAIR]
        arrows = [arrow(x, y, c) for (x, y, _), c in zip(d["social"], cols)]
        prefs = stack([(r"the prude: \ $n \succ p \succ l$", POW), (r"the lewd: \ $p \succ l \succ n$", MKT)],
                      font_size=24, buff=0.2, aligned_edge=LEFT).move_to([3.6, 1.6, 0])
        rules = VGroup(*[wrapped_label(rf"${x} \succ {y}$: \ {t}", 6.0, 20, c)
                         for (x, y, t), c in zip(d["social"], cols)]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        rules.move_to([3.6, -0.5, 0])
        cyc = label(r"$n \succ p \succ l \succ n$: \ a cycle, \ so no option is best", font_size=24,
                    color=BAD).move_to([3.6, -2.6, 0])
        with self.voiceover(
            "Amartya Sen's example, from 1970, uses a book once thought scandalous, Lady Chatterley's Lover. There is "
            "one copy and two people. <bookmark mark='a'/>Three options: the prude reads it, the lewd reads it, or no "
            "one does. <bookmark mark='b'/>The prude would most like no one to read it; but if someone must, he would "
            "rather read it himself than let the lewd enjoy it. The lewd would most like the prude to read it, to "
            "broaden his mind; next best, to read it himself; worst, that no one does. <bookmark mark='c'/>Now give "
            "each a small sphere of liberty. Whether the prude reads a book is his business: he prefers that no one "
            "read it to reading it himself, so society should rank n above p. <bookmark mark='d'/>Whether the lewd "
            "reads is his business: he prefers reading it to no one reading it, so l above n. <bookmark mark='e'/>And "
            "both prefer the prude reading it to the lewd reading it, so by the Pareto principle, p above l. "
            "<bookmark mark='f'/>The social ranking is a cycle: n over p, p over l, l over n. Whatever is chosen, "
            "something else is socially better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(nodes[k]) for k in pos], *[FadeIn(tags[k]) for k in pos])
            vo.wait_until("b")
            self.play(FadeIn(prefs))
            for mk, i in zip("cde", range(3)):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[i]), FadeIn(rules[i]))
            vo.wait_until("f")
            self.play(FadeIn(cyc), *[Indicate(a, color=BAD, scale_factor=1.05) for a in arrows])
        self.clear_scene()

    def search(self):
        d = load("sen")
        assert d["pairs_checked"] == 6 and d["all_cycle"]
        head = label(r"Every way to grant two rights, \ searched", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def pair(p):
            return label(rf"$\{{{p[0]}, \ {p[1]}\}}$", font_size=20, color=LIB)

        def order(o):
            return label(rf"${o[0]} \succ {o[1]} \succ {o[2]}$", font_size=20)

        hd = [r"\text{1 decides}", r"\text{2 decides}", r"\text{person 1}", r"\text{person 2}", r"\text{forced cycle}"]
        cells = []
        for r in d["results"]:
            o1, o2, c = r["profile"]["o1"], r["profile"]["o2"], r["profile"]["cycle"]
            cells.append([pair(r["d1"]), pair(r["d2"]), order(o1), order(o2),
                          label(rf"${c[0]} \succ {c[1]} \succ {c[2]} \succ {c[0]}$", font_size=20, color=BAD)])
        grid = ValueGrid(hd, cells, col_w=[1.9, 1.9, 2.4, 2.4, 3.0], cell_h=0.55, font_size=19).move_to([0, 0.6, 0])
        foot = stack([(r"36 profiles of strict rankings for each assignment; \ the first that cycles is shown", GREY_A),
                      (r"rights plus Pareto alone force the cycle, \ for every assignment", BAD)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Is this a quirk of one story? The Reasoner checks every case. <bookmark mark='a'/>With two people and "
            "three options, give person one the right to decide one pair and person two the right to decide another: "
            "there are six ways. <bookmark mark='b'/>For each, it searches all thirty six combinations of strict "
            "rankings for a profile on which the two rights and the Pareto principle alone force a cycle. <bookmark "
            "mark='c'/>Every assignment has one. Nothing depends on books or prudes: whenever two people each have "
            "even one protected choice, there are preferences that make liberty and unanimity contradict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[i][j]) for i in range(6) for j in range(2)])
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), *[FadeIn(grid.cell[i][j]) for i in range(6) for j in (2, 3)])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[i][4]) for i in range(6)], lag_ratio=0.2), FadeIn(foot[1]))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=38, current=38).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(38, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty eighth brick in the Wall. <bookmark mark='a'/>The dream was a social ranking that "
            "respects both liberty and unanimity: that lets each person decide what is their own business, and never "
            "chooses an option everyone thinks worse than another. Sen's theorem shows that no rule does this for "
            "every possible set of preferences. <bookmark mark='b'/>What it forces is a decision about which comes "
            "first. If rights are to mean anything, they must sometimes constrain what welfare would recommend, even "
            "unanimous welfare."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[38], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        head = history_card(1970, r"Amartya Sen", r"``The Impossibility of a Paretian Liberal''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"unrestricted domain", r"the rule must work for every profile of individual rankings", GREY_A),
                (r"weak Pareto", r"if everyone prefers $x$ to $y$, \ society ranks $x$ above $y$", FAIR),
                (r"minimal liberalism", r"at least two people are each decisive over at least one pair of options", LIB),
                (r"the theorem", r"no social decision function satisfies all three: \ some profile yields a cycle, \ and nothing can be chosen", BAD),
                (r"the lesson", r"the Pareto principle, \ the weakest welfarist axiom, \ is already at odds with any rights at all", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Sen's paper, The Impossibility of a Paretian Liberal, is two pages long. <bookmark mark='a'/>A rule must "
            "work for every profile of individual rankings. <bookmark mark='b'/>Weak Pareto: if everyone prefers x to "
            "y, society ranks x above y. <bookmark mark='c'/>Minimal liberalism: at least two people are each "
            "decisive over at least one pair. <bookmark mark='d'/>No rule meets all three: some profile yields a "
            "cycle, and then nothing can be chosen. <bookmark mark='e'/>The lesson is sharp. The Pareto principle is "
            "the weakest welfarist axiom there is, accepted even by those who reject utilitarianism. Yet it already "
            "conflicts with any rights at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def responses(self):
        head = label(r"Where the paradox leads", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Gibbard \ (1974)", r"rights over one's own affairs conflict even with each other: \ make them waivable", LIB),
                (r"Sen's own reply", r"meddlesome preferences about others' affairs should not count: \ restrict Pareto", FAIR),
                (r"Nozick \ (1974)", r"rights are not rankings: \ they fix which options are open; \ welfare chooses among the rest", MKT),
                (r"game forms", r"Gärdenfors \ (1981); \ Sugden \ (1985); \ Gaertner, \ Pattanaik and Suzumura \ (1992): \ rights as permissible strategies", COM),
                (r"contract", r"Buchanan; \ Harel and Nitzan \ (1987): \ the lewd and the prude can trade, \ and the Pareto-better contract needs someone to enforce it", POW)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "There are four main lines of response. <bookmark mark='a'/>Allan Gibbard showed in 1974 that rights over "
            "one's own affairs can conflict even with each other, without Pareto, and proposed that rights be "
            "waivable. <bookmark mark='b'/>Sen's own suggestion was that meddlesome preferences, about what others "
            "read, should not count, which restricts the Pareto principle. <bookmark mark='c'/>Nozick replied that "
            "rights are not part of a social ranking at all: they fix which options are open, and welfare or anything "
            "else may choose among what is left. <bookmark mark='d'/>Peter Gärdenfors, Robert Sugden and others "
            "modelled rights as game forms, sets of permissible strategies, rather than as decisive pairs. <bookmark "
            "mark='e'/>And the two readers could make a contract, the lewd agreeing not to read if the prude does; "
            "but then a voluntary contract that is better for both takes away a right each would want to keep, and "
            "someone has to enforce it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
