from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Intuition(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Proof instead of truth", r"What if `true' means `proved'?", lit=(1930,), part=PART)
        with self.voiceover("Chapter eight. Proof instead of truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.brouwer()
        self.bhk()
        self.godel()
        self.kripke()

    def brouwer(self):
        hc = history_card(1908, r"L.\ E.\ J.\ Brouwer", r"`The unreliability of the logical principles'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        lem = MathTex(r"A \lor \lnot A", font_size=56, color=GOAL).move_to([0, 1.0, 0])
        ex = VGroup(label(r"$A$: \ `there are infinitely many twin primes'", font_size=28),
                    label(r"we have no proof of $A$, \ and no proof of $\lnot A$", font_size=26, color=GREY_A),
                    label(r"so, for Brouwer, \ no right to assert $A \lor \lnot A$", font_size=26, color=BAD)
                    ).arrange(DOWN, buff=0.25).next_to(lem, DOWN, buff=0.5)
        fin = label(r"excluded middle is safe for finite searches, \ not for the infinite", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The deepest challenge to classical logic came from mathematics. <bookmark mark='a'/>In 1908 the Dutch "
            "mathematician L. E. J. Brouwer published a paper on the unreliability of the logical principles. His "
            "target was excluded middle: A or not A. <bookmark mark='b'/>Take A to say that there are infinitely "
            "many twin primes. Nobody has proved it, or its negation. For Brouwer, a mathematical statement is true "
            "only when proved, so we have no right to assert 'A or not A'. <bookmark mark='c'/>For a finite search, "
            "excluded middle is harmless: in principle, look and see. For the infinite, there is nothing to look "
            "at, only proofs."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(lem))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(fin))
        self.clear_scene()

    def bhk(self):
        head = label(r"The BHK reading: \ what counts as a proof \ (Brouwer, Heyting 1930, Kolmogorov 1932)",
                     font_size=28, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"A \land B", r"a proof of $A$ and a proof of $B$"),
                (r"A \lor B", r"a proof of $A$ or of $B$, \ and which"),
                (r"A \to B", r"a method turning any proof of $A$ into a proof of $B$"),
                (r"\lnot A", r"a method turning any proof of $A$ into a proof of $\bot$"),
                (r"\exists x\, A(x)", r"a particular $c$, \ and a proof of $A(c)$")]
        tab = VGroup()
        for i, (f, t) in enumerate(rows):
            y = 1.8 - 0.78 * i
            m = MathTex(f, font_size=36, color=GOAL)
            m.move_to([-4.6, y, 0])
            l_ = label(t, font_size=26).move_to([-3.2, y, 0])
            l_.shift(RIGHT * l_.width / 2)
            tab.add(VGroup(m, l_))
        cap = label(r"a proof of $A \lor \lnot A$ would decide every question: \ so it is not a law",
                    font_size=26, color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Brouwer's student Arend Heyting wrote down the logic in 1930, and the meaning of the connectives came "
            "to be called the BHK interpretation, after Brouwer, Heyting and Kolmogorov. <bookmark mark='a'/>A proof "
            "of A and B is a proof of each. A proof of A or B is a proof of one of them, together with which one. "
            "<bookmark mark='b'/>A proof of 'if A then B' is a method that turns any proof of A into a proof of B. "
            "Not A is a method that turns any proof of A into an absurdity. <bookmark mark='c'/>And a proof that "
            "something exists must produce it. <bookmark mark='d'/>On this reading, a proof of 'A or not A' would be "
            "a universal method for deciding every question. There is none, so excluded middle is not a law."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.clear_scene()

    def godel(self):
        d = load("godel")
        g3 = d["g3"]
        T = load("tables")["G3"]
        tab = VGroup(label(r"Heyting's three values, G3", font_size=26, color=P.CLAIM),
                     VGroup(ConnTable("not", T["values"], T["not"], designated=["1"], size=0.6, font_size=26),
                            ConnTable("imp", T["values"], T["imp"], designated=["1"], size=0.6, font_size=26)
                            ).arrange(RIGHT, buff=0.8, aligned_edge=UP)).arrange(DOWN, buff=0.35).move_to([-3.8, 1.0, 0])
        verdicts = VGroup(
            VGroup(MathTex(r"p \lor \lnot p", font_size=32), tv(g3["LEM"], 28)).arrange(RIGHT, buff=0.3),
            VGroup(MathTex(r"\lnot\lnot p \models p", font_size=32), tv(g3["DNE"], 28)).arrange(RIGHT, buff=0.3),
            VGroup(MathTex(r"p \models \lnot\lnot p", font_size=32), tv(d["p_to_nnp"], 28)).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        thm = theorem_card(r"Gödel (1932)", r"no finite matrix gives exactly intuitionistic logic", width=6.0,
                           font_size=24).move_to([3.4, 2.2, 0])
        dn = MathTex(r"D_n = \bigvee_{0 \le i < j \le n} (p_i \leftrightarrow p_j)", font_size=34).next_to(thm, DOWN,
                                                                                                   buff=0.4)
        hd = [label(r"$n$", font_size=22, color=P.CLAIM), label(r"in $n$ values", font_size=22, color=P.CLAIM),
              label(r"in $n{+}1$", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(str(r["n"]), font_size=26), r["valid_n"], r["valid_n1"]] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.0, 2.0, 1.6], cell_h=0.52, font_size=26).next_to(dn, DOWN, buff=0.4)
        why = label(r"$n{+}1$ atoms, \ $n$ values: \ two atoms must agree \ (the pigeonhole)", font_size=22,
                    color=GOAL).next_to(grid, DOWN, buff=0.3)
        with self.voiceover(
            "Can intuitionistic logic be given by a matrix, like the logics of this part? <bookmark mark='a'/>"
            "Heyting's three-valued table comes close. In it, excluded middle fails, and so does 'not not p, so p', "
            "while 'p, so not not p' holds, exactly as intuitionists want. <bookmark mark='b'/>But in 1932 Gödel "
            "proved that no finite matrix gives exactly intuitionistic logic. <bookmark mark='c'/>His witness is a "
            "disjunction: among n plus one atoms, some two are equivalent. <bookmark mark='d'/>In a chain of n "
            "values, it must hold, by the pigeonhole principle: n plus one atoms, n values, two atoms agree. In a "
            "chain of n plus one values, the atoms can all differ, and it fails. The Reasoner confirms it for n "
            "from two to four. <bookmark mark='e'/>So each finite chain proves too much, and intuitionistic logic "
            "needs infinitely many values, or a different semantics altogether."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            self.play(LaggedStart(*[FadeIn(v) for v in verdicts], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(Write(dn))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in range(3)], FadeIn(why))
            vo.wait_until("e")
            self.play(Indicate(grid.column(2), color=BAD))
        self.clear_scene()

    def kripke(self):
        d = load("intkripke")
        hc = history_card(1965, r"Saul Kripke", r"`Semantical analysis of intuitionistic logic I'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        w0 = VGroup(Circle(radius=0.48, color=P.WORLD, stroke_width=3), MathTex(r"\cdot", font_size=34))
        w1 = VGroup(Circle(radius=0.48, color=P.WORLD, stroke_width=3), MathTex(r"p", font_size=34, color=OK))
        w0.move_to([-4.2, -0.6, 0])
        w1.move_to([-1.2, -0.6, 0])
        for w in (w0, w1):
            w[1].move_to(w[0])
        arr = Arrow(w0.get_right(), w1.get_left(), buff=0.1, color=CONN)
        names = VGroup(label(r"today: \ not yet proved", font_size=22, color=GREY_A).next_to(w0, DOWN, buff=0.25),
                       label(r"later: \ $p$ proved", font_size=22, color=GREY_A).next_to(w1, DOWN, buff=0.25))
        hd = [label(r"formula", font_size=22, color=P.CLAIM), label(r"today", font_size=22, color=P.CLAIM),
              label(r"later", font_size=22, color=P.CLAIM)]
        rows = [[mxf(f, 28)] + d["table"][f] for f in d["forms"]]
        grid = ValueGrid(hd, rows, col_w=[2.8, 1.3, 1.3], cell_h=0.54, font_size=26).move_to([3.6, -0.3, 0])
        rule = label(r"$\lnot p$ holds at a stage when $p$ fails at every later stage", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.7)
        nxt = label(r"Part 9: \ intuitionism, \ and proofs as programs", font_size=24, color=GREY_B).to_edge(DOWN,
                                                                                                       buff=0.3)
        with self.voiceover(
            "The different semantics came from Kripke in 1965, with the same picture as Part 4. "
            "<bookmark mark='a'/>Points are stages of knowledge, and arrows lead to later stages, where more has been "
            "proved. Today p is unproved; later it is proved. <bookmark mark='b'/>Not p holds at a stage only when p "
            "fails at every later stage. <bookmark mark='c'/>So today, p is not established, and neither is not p, "
            "since p will be proved. Excluded middle fails today. 'Not not p' holds, but 'not not p, so p' fails. "
            "<bookmark mark='d'/>Part 9 returns to intuitionism, and to the discovery that its proofs are programs."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(w0), GrowArrow(arr), FadeIn(w1), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in range(3)])
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.clear_scene()
