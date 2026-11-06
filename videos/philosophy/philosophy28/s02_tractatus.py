from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403

DEPTH_COL = {0: WORD, 1: WORLD, 2: USE, 3: HEAR}


class Tractatus(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The picture theory", r"How can a sentence say how things are?", lit=(1921,), part=PART)
        with self.voiceover("Chapter one. The picture theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.picture()
        self.space()
        self.operation()
        self.ladder()

    def picture(self):
        hc = history_card(1921, r"Ludwig Wittgenstein", r"\textit{Tractatus Logico-Philosophicus}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"1", r"The world is all that is the case.", WORLD),
            (r"2", r"What is the case, \ a fact, \ is the existence of states of affairs.", WORLD),
            (r"4.01", r"A proposition is a picture of reality.", WORD),
            (r"4.022", r"A proposition \textit{shows} how things stand if it is true. \ And it \textit{says} that they "
                       r"do so stand.", WORD),
        ]
        g = rows_table(rows, top=1.1, gap=0.5, width=8.6, x_text=-4.4, label_size=24, text_size=22)
        foot = stack([(r"a picture shares a logical form with what it pictures: \ the arrangement of its elements "
                       r"mirrors an arrangement of objects", RULE_C),
                      (r"Wittgenstein's model: \ a Paris court that reconstructed a traffic accident with toy cars", HIST)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Wittgenstein's first book, the Tractatus, published in 1921, is a sequence of numbered remarks. "
            "<bookmark mark='a'/>It opens: the world is all that is the case. <bookmark mark='b'/>What is the case, a "
            "fact, is the existence of states of affairs. <bookmark mark='c'/>And a proposition is a picture of "
            "reality. <bookmark mark='d'/>A proposition shows how things stand if it is true, and says that they do "
            "so stand. <bookmark mark='e'/>A picture works by sharing a logical form with what it pictures: the way "
            "its elements are arranged mirrors a way objects could be arranged. <bookmark mark='f'/>The idea came to "
            "him, it is said, from a report of a Paris court reconstructing a traffic accident with toy cars and "
            "dolls."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def space(self):
        head = label(r"Logical space, \ and truth tables", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cells = VGroup()
        combos = [(a, b) for a in (True, False) for b in (True, False)]
        for i, (a, b) in enumerate(combos):
            sq = Square(1.2, color=GREY_B, stroke_width=2).move_to([-4.6 + 1.3 * (i % 2), 0.9 - 1.3 * (i // 2), 0])
            t = MathTex(("p" if a else r"\neg p") + r",\ " + ("q" if b else r"\neg q"), font_size=24).move_to(sq)
            cells.add(VGroup(sq, t))
        ctag = label(r"four possible worlds for two elementary propositions", font_size=18, color=GREY_A).next_to(
            cells, DOWN, buff=0.2)
        region = VGroup(cells[0][0].copy(), cells[1][0].copy(), cells[2][0].copy()).set_fill(USE, opacity=0.35)
        rtag = label(r"`$p$ or $q$': \ true in three of them", font_size=20, color=USE).next_to(ctag, DOWN, buff=0.15)
        hd = [r"p", r"q", r"p \wedge q", r"p \vee q", r"p \rightarrow q"]
        rows = [[tv(a, 24), tv(b, 24), tv(a and b, 24), tv(a or b, 24), tv((not a) or b, 24)] for a, b in combos]
        grid = ValueGrid(hd, rows, col_w=[1.0, 1.0, 1.4, 1.4, 1.6], cell_h=0.5, font_size=22).move_to([2.8, 0.6, 0])
        side = stack([(r"truth tables: \ \textit{Tractatus} 4.31, \ the same year as Post \ (Part 2)", HIST),
                      (r"16 possible columns: \ 16 truth functions of two propositions", RULE_C)], font_size=20,
                     aligned_edge=LEFT, width=6.0, buff=0.22).next_to(grid, DOWN, buff=0.35)
        with self.voiceover(
            "The picture has a precise logical core. <bookmark mark='a'/>Elementary propositions are independent of "
            "one another; with two of them, p and q, there are four ways things could be. <bookmark mark='b'/>Every "
            "other proposition is a truth function of the elementary ones, true in some of these possibilities and "
            "false in the rest: p or q is true in three of the four. <bookmark mark='c'/>Wittgenstein set this out "
            "with truth tables, in the same year that Emil Post did, as Part 2 told. <bookmark mark='d'/>With two "
            "propositions there are sixteen possible columns, so sixteen truth functions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), FadeIn(ctag))
            vo.wait_until("b")
            self.play(FadeIn(region), FadeIn(rtag))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def operation(self):
        d = load("opn")
        head = label(r"One operation makes them all", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["count"] == 16 and d["max_steps"] == 3
        f = MathTex(r"N(\xi_1, \dots, \xi_k) \;=\; \text{true iff every } \xi_i \text{ is false}", font_size=32,
                    color=RULE_C).move_to([0, 2.2, 0])
        tiles = VGroup()
        for i, r in enumerate(d["rows"]):
            col = DEPTH_COL[r["steps"]]
            box = RoundedRectangle(width=2.6, height=0.95, corner_radius=0.1, color=col, stroke_width=2)
            t1 = MathTex(r"\texttt{" + r["table"] + "}", font_size=24, color=col)
            t2 = label(r["name"] if r["name"] else r"\ ", font_size=15, color=GREY_A)
            VGroup(t1, t2).arrange(DOWN, buff=0.08).move_to(box)
            tiles.add(VGroup(box, t1, t2))
        tiles.arrange_in_grid(rows=4, cols=4, buff=(0.25, 0.18)).move_to([-1.2, -0.7, 0])
        legend = VGroup(*[label(rf"{k} application" + ("" if k == 1 else "s"), font_size=19, color=c)
                          for k, c in DEPTH_COL.items()]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([5.4, -0.4, 0])
        by = {k: [i for i, r in enumerate(d["rows"]) if r["steps"] == k] for k in DEPTH_COL}
        assert [len(by[k]) for k in DEPTH_COL] == [2, 3, 5, 6]
        with self.voiceover(
            "Wittgenstein made a stronger claim: one operation generates every truth function. <bookmark mark='a'/>"
            "Call it N: applied to any collection of propositions, it is true when every one of them is false. "
            "Applied to one proposition, it is negation; to two, neither, nor. <bookmark mark='b'/>The Reasoner "
            "starts from p and q, written as columns of their truth table. <bookmark mark='c'/>One application of N "
            "gives not p, not q, and neither p nor q. <bookmark mark='d'/>Two give five more, among them and, or, and "
            "the contradiction. <bookmark mark='e'/>Three give the last six, including if-then, if and only if, and "
            "the tautology. All sixteen, from a single operation: what the Tractatus calls the general form of a "
            "proposition."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, k in zip("bcde", (0, 1, 2, 3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(tiles[i]) for i in by[k]], FadeIn(legend[k]))
        self.clear_scene()

    def ladder(self):
        head = label(r"Throwing away the ladder", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"6.54", r"anyone who understands me eventually recognizes my propositions as nonsensical: \ he must, \ so "
                      r"to speak, \ throw away the ladder after he has climbed up it", RULE_C),
            (r"7", r"Whereof one cannot speak, \ thereof one must be silent.", WORD),
            (r"the Vienna Circle", r"took the book as a manifesto for verificationism \ (Part 18)", HIST),
            (r"the later Wittgenstein", r"the \textit{Investigations} \ (1953) \ criticizes `the author of the "
                                        r"\textit{Tractatus}' \ by name", USE),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "The book ends strangely. <bookmark mark='a'/>Its own sentences, it says, are nonsense: whoever "
            "understands them must throw away the ladder after climbing up it. <bookmark mark='b'/>And the last "
            "line: whereof one cannot speak, thereof one must be silent. <bookmark mark='c'/>The Vienna Circle read "
            "the Tractatus as a manifesto for the verificationism of Part 18. <bookmark mark='d'/>Its author, after "
            "years away from philosophy, came to think its picture of language was a distortion. The Investigations, "
            "published after his death, names the author of the Tractatus among the logicians who got the "
            "multiplicity of language wrong."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
