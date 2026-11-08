from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Addition(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Mere addition", r"Can adding good lives make things worse?", lit=(1984,), part=PART)
        with self.voiceover("Chapter three. Mere addition."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.staircase()
        self.verdicts()
        self.benign()
        self.price()

    def staircase(self):
        d = load("addition")
        rows = {r["name"]: r for r in d["rows"]}
        head = label(r"The mere addition paradox \ (Parfit, \ 1984)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert rows["A+"]["groups"] == [[10, 10.0], [10, 4.0]] and rows["B"]["groups"] == [[20, 7.5]]
        assert (rows["A"]["total"], rows["A+"]["total"], rows["B"]["total"]) == (100, 140, 150)
        assert (rows["A"]["average"], rows["A+"]["average"], rows["B"]["average"]) == (10, 7, 7.5)
        base = -1.9
        xs = {"A": -6.5, "A+": -4.5, "B": -1.3, "B+": 1.6, "C": 4.4}
        cols = {"A": WELL, "A+": WELL, "B": POP, "B+": POP, "C": FUT}
        blocks = VGroup()
        for name in ("A", "A+", "B", "B+", "C"):
            groups = rows[name]["groups"]
            g = parfit_bars([(int(n), w) for n, w in groups], xs[name], base, unit_w=0.06, unit_h=0.2,
                            color=cols[name], gap=0.04)
            if name in ("A+", "B+"):
                g[1].set_fill(opacity=0.45)
            nm = label(name, font_size=22, color=GOAL).next_to(g, DOWN, buff=0.15)
            st = label(rf"total {rows[name]['total']:g}, \ average {rows[name]['average']:g}", font_size=15,
                       color=GREY_A).next_to(nm, DOWN, buff=0.1)
            blocks.add(VGroup(g, nm, st))
        arrows = VGroup(*[Arrow(blocks[i][0].get_right() + RIGHT * 0.05 + UP * 0.6,
                                blocks[i + 1][0].get_left() + LEFT * 0.05 + UP * 0.6, buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.25) for i in range(4)])
        tags = VGroup(*[label(t, font_size=15, color=c).next_to(a, UP, buff=0.05) for t, c, a in
                        zip([r"add", r"equalize", r"add", r"equalize"], [WELL, POP, WELL, POP], arrows)])
        side = stack([(r"A+: \ A, \ plus 10 people at 4 who affect no one: \ not worse", WELL),
                      (r"B: \ the same 20 people, \ equal, \ more in total and on average: \ better than A+", POP),
                      (r"so B is better than A; \ repeat, \ and the steps end at Z", FUT)],
                     font_size=19, aligned_edge=LEFT, width=9.0, buff=0.22).move_to([0, 2.1, 0])
        with self.voiceover(
            "Parfit's deepest argument for the conclusion does not assume the total view at all. "
            "<bookmark mark='a'/>Start with A: ten people, each at ten. <bookmark mark='b'/>Now add ten more people, "
            "each at four, living somewhere that affects no one in A: a mere addition. A plus is hard to call worse "
            "than A: the new people have lives worth living, and no one else is touched. <bookmark mark='c'/>Now "
            "compare A plus with B: the same twenty people, all at seven and a half. B has more in total, more on "
            "average, and perfect equality; it seems better than A plus. <bookmark mark='d'/>So, by transitivity, B "
            "is better than A. <bookmark mark='e'/>Now repeat: add twenty people at three, then equalize at five and "
            "a half. Each step looks harmless, and the staircase runs down to Z."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(blocks[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(tags[0]), FadeIn(blocks[1]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(tags[1]), FadeIn(blocks[2]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            for i in (2, 3):
                self.play(GrowArrow(arrows[i]), FadeIn(tags[i]), FadeIn(blocks[i + 1]))
        self.clear_scene()

    def verdicts(self):
        d = load("addition")
        v = d["verdicts"]
        head = label(r"What each view says about each step", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert v["average"] == {"A+ vs A": "worse", "B vs A+": "better", "B vs A": "worse", "C vs A": "worse"}
        assert all(v[k] == {"A+ vs A": "better", "B vs A+": "better", "B vs A": "better", "C vs A": "better"}
                   for k in ("total", "critical level", "variable value", "prioritarian"))
        names = ["total", "average", "critical level", "variable value", "prioritarian"]
        steps = ["A+ vs A", "B vs A+", "B vs A", "C vs A"]
        hd = [r"\text{view}", r"\text{A+ against A}", r"\text{B against A+}", r"\text{B against A}",
              r"\text{C against A}"]
        cols = {"better": OK, "worse": BAD}
        cells = [[label(n, font_size=18, color=WHITE)] + [label(v[n][s], font_size=18, color=cols[v[n][s]])
                                                          for s in steps] for n in names]
        grid = ValueGrid(hd, cells, col_w=[3.0, 2.4, 2.4, 2.4, 2.4], cell_h=0.5, font_size=17).move_to([0, 0.2, 0])
        foot = stack([(r"only the average view resists the first step, \ and it resists by calling a mere addition "
                       r"worse", POP),
                      (r"in these small worlds the others accept every step; \ the critical level 2 is passed by "
                       r"lives at 3 and 4", GREY_A)], font_size=18, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner asks each view about each step. <bookmark mark='a'/>The total view accepts them all. "
            "<bookmark mark='b'/>The average view resists the first: since the added people are below the average, it "
            "calls A plus worse than A, though no one in A is touched and the new lives are good. "
            "<bookmark mark='c'/>The critical-level, variable-value and prioritarian views accept every step in "
            "these small worlds: the added lives at four and three are above the critical level of two, and too few "
            "to drag down a variable-value score. <bookmark mark='d'/>Followed far enough, each of them faces the "
            "same staircase, with steps of their own size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for k in range(2, 5) for c in grid.cell[k]], FadeIn(foot[1]))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def benign(self):
        d = load("benign")
        head = label(r"Benign addition \ (Arrhenius; \ Huemer, \ 2008)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["worse_by"] == ["average"]
        assert (d["A"]["average"], d["A++"]["average"], d["A"]["total"], d["A++"]["total"]) == (10.0, 7.25, 100.0, 145.0)
        base = -1.6
        A = parfit_bars([(10, 10)], -5.8, base, unit_w=0.12, unit_h=0.22, color=WELL)
        App = parfit_bars([(10, 10.5), (10, 4)], -2.4, base, unit_w=0.12, unit_h=0.22, color=WELL, gap=0.05)
        App[1].set_fill(POP, opacity=0.6).set_stroke(POP)
        la = label(r"A: \ 10 at 10", font_size=19, color=GOAL).next_to(A, DOWN, buff=0.2)
        lb = label(r"A++: \ the same 10 at 10.5, \ plus 10 at 4", font_size=19, color=GOAL).next_to(App, DOWN,
                                                                                                    buff=0.2)
        side = stack([(r"everyone in A is better off, \ and the new lives are good", WELL),
                      (r"total 145 against 100; \ every view but one prefers A++", WELL),
                      (r"the average view: \ 7.25 against 10, \ worse", POP),
                      (r"Huemer: \ deny this and you deny a Pareto improvement plus mere addition; \ he accepts Z",
                       GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.3, -0.2, 0])
        with self.voiceover(
            "Arrhenius and Michael Huemer sharpened the first step. <bookmark mark='a'/>Instead of a mere addition, "
            "take a benign one: from A, ten people at ten, to A plus plus, in which the same ten people are a little "
            "better off, at ten and a half, and ten new people live at four. <bookmark mark='b'/>Everyone who exists "
            "in A is better off, and every added life is good. The total rises from a hundred to a hundred and forty "
            "five, and every view the Reasoner knows prefers A plus plus, but one. <bookmark mark='c'/>The average "
            "view still calls it worse, seven and a quarter against ten. <bookmark mark='d'/>Huemer's In Defence of "
            "Repugnance, of 2008, argues that this is decisive: denying the step means denying an improvement for "
            "everyone combined with a mere addition. He follows the staircase all the way down, and accepts Z."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(A, DOWN), FadeIn(la))
            self.play(GrowFromEdge(App, DOWN), FadeIn(lb))
            for mk, r in zip("bcd", side[1:]):
                vo.wait_until(mk)
                if mk == "b":
                    self.play(FadeIn(side[0]), FadeIn(r))
                else:
                    self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["AZ", "MA", "NAE", "TRANS"]]
        assert sorted(d["mcs"]) == [["AZ"], ["MA"], ["NAE"], ["TRANS"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the repugnant conclusion")
        positions = [(("AZ",), r"accept Z", r"Tännsjö; \ Huemer; \ total utilitarians"),
                     (("MA",), r"mere addition can be worse", r"average and critical-level views"),
                     (("NAE",), r"perfectionism", r"Parfit \ (1986): \ losing the best things makes B worse"),
                     (("TRANS",), r"`better than' intransitive", r"Temkin \ (2012); \ Rachels \ (1998)")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>Adding lives worth living, affecting no one else, "
            "does not make an outcome worse. A larger total, shared more equally among the same people, is better. "
            "Better than is transitive. And A is better than Z. <bookmark mark='b'/>Together, the staircase makes the "
            "first three entail that Z is better than A. <bookmark mark='c'/>Accept Z, with Tännsjö, Huemer and the "
            "total utilitarians. <bookmark mark='d'/>Deny mere addition, with the average and critical-level views: "
            "adding good lives can make things worse. <bookmark mark='e'/>Deny that B beats A plus: Parfit himself "
            "suggested a perfectionism on which losing the best things in life, the music of Mozart, is not made up "
            "by any amount of lesser goods. <bookmark mark='f'/>Or deny transitivity, as Larry Temkin did in "
            "Rethinking the Good, in 2012, and Stuart Rachels before him: better than may not be a single ranking at "
            "all."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
