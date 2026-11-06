from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403

HALTS = [[1, 0, 1, 1, 0], [0, 0, 1, 0, 1], [1, 1, 1, 0, 0], [0, 1, 0, 1, 1], [1, 0, 0, 1, 0]]   # illustrative


class Undecidable(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"No machine decides validity", r"Can logic be mechanized completely?",
                            lit=(1928, 1936), part=PART)
        with self.voiceover("Chapter ten. No machine decides validity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.halting()
        self.reduction()
        self.asymmetry()
        self.brick()
        self.fragments()
        self.industry()

    def problem(self):
        hc = history_card(1928, r"Hilbert \& Ackermann", r"the \textit{Entscheidungsproblem}, `the main problem of "
                          r"mathematical logic'", width=6.6, color=HIST).to_corner(UL, buff=0.4)
        q = VGroup(label(r"Is there a mechanical procedure that takes any first-order sentence", font_size=30),
                   label(r"and decides, in finitely many steps, whether it is valid?", font_size=30)).arrange(
            DOWN, buff=0.15).move_to([0, 0.2, 0])
        lb = label(r"Leibniz's \textit{calculemus}, for all of first-order logic", font_size=26, color=GOAL).next_to(
            q, DOWN, buff=0.5)
        ans = VGroup(history_card(1936, r"Alonzo Church", r"no: \ via the $\lambda$-calculus", width=4.6,
                                  color=BAD, font_size=20),
                     history_card(1936, r"Alan Turing", r"no: \ via machines that halt or run forever", width=4.6,
                                  color=BAD, font_size=20)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Truth tables decide propositional logic. Is there something like them for first-order logic? "
            "<bookmark mark='a'/>Hilbert and Ackermann called this the Entscheidungsproblem, the decision problem, "
            "and named it the main problem of mathematical logic: <bookmark mark='b'/>a mechanical procedure that "
            "takes any sentence and decides, in finitely many steps, whether it is valid. It would be Leibniz's "
            "calculemus, for all of logic. <bookmark mark='c'/>In 1936 Alonzo Church in Princeton and Alan Turing "
            "in Cambridge, independently and within weeks, proved that there is no such procedure."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Indicate(hc, color=HIST, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(lb))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in ans], lag_ratio=0.3))
        self.clear_scene()

    def halting(self):
        n = len(HALTS)
        cw, ch = 0.85, 0.55
        x0, y0 = -5.4, 2.0
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                v = HALTS[i][j]
                cells.add(VGroup(Rectangle(width=cw, height=ch, stroke_color=GREY_C, stroke_width=1,
                                           fill_color=OK if v else BAD, fill_opacity=0.25),
                                 label(r"halts" if v else r"loops", font_size=18, color=OK if v else BAD)).move_to(
                    [x0 + j * cw, y0 - i * ch, 0]))
        rows_l = VGroup(*[MathTex(rf"P_{{{i + 1}}}", font_size=26, color=P.CLAIM).move_to([x0 - 0.85, y0 - i * ch, 0])
                          for i in range(n)])
        cols_l = VGroup(*[MathTex(rf"P_{{{j + 1}}}", font_size=26, color=P.AGENT).move_to([x0 + j * cw, y0 + 0.5, 0])
                          for j in range(n)])
        ax = VGroup(label(r"program", font_size=20, color=P.CLAIM).next_to(rows_l, UP, buff=0.18),
                    label(r"run on input", font_size=20, color=P.AGENT).next_to(cols_l, UP, buff=0.15))
        diag = VGroup(*[SurroundingRectangle(cells[i * n + i], color=GOAL, buff=0.02, stroke_width=3)
                        for i in range(n)])
        drow = VGroup()
        for j in range(n):
            v = 1 - HALTS[j][j]
            drow.add(VGroup(Rectangle(width=cw, height=ch, stroke_color=GOAL, stroke_width=2,
                                      fill_color=OK if v else BAD, fill_opacity=0.35),
                            label(r"halts" if v else r"loops", font_size=18, color=OK if v else BAD)).move_to(
                [x0 + j * cw, y0 - n * ch - 0.45, 0]))
        dl = MathTex(r"D", font_size=30, color=GOAL).move_to([x0 - 0.85, y0 - n * ch - 0.45, 0])
        txt = VGroup(
            label(r"suppose a program $H$ could tell, for any program $P$ and input $x$, whether $P$ halts on $x$",
                  font_size=22),
            label(r"build $D$: \ on input $P$, ask $H$ about $P$ run on itself, and do the opposite", font_size=22,
                  color=GOAL),
            label(r"$D$ differs from every row on the diagonal, \ so $D$ is no program in the list", font_size=22,
                  color=BAD),
            label(r"but $H$ makes $D$ a program: \ so $H$ cannot exist", font_size=24, color=BAD))
        for t in txt:
            if t.width > 7.2:
                t.width = 7.2
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        txt.move_to([-1.2 + txt.width / 2, 0.3, 0])
        note_ = label(r"illustrative table; \ the argument is Cantor's diagonal again", font_size=20,
                      color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Turing's proof starts from a question about programs. <bookmark mark='a'/>List every program, and for "
            "each one, record whether it halts or runs forever on each input. <bookmark mark='b'/>Suppose some "
            "program H could fill in this table: given any program and any input, it says whether the program "
            "halts. <bookmark mark='c'/>Then build a new program D. On input P, D asks H whether P halts when run on "
            "itself, and does the opposite: if P would halt, D loops; if P would loop, D halts. "
            "<bookmark mark='d'/>D's row disagrees with every row of the table at the diagonal, so D is not "
            "anywhere in the list. <bookmark mark='e'/>But if H existed, D would be a program, and the list "
            "contains every program. So H cannot exist: halting is undecidable. It is the same diagonal that "
            "Cantor used for the reals."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows_l), FadeIn(cols_l), FadeIn(ax),
                      LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), Create(diag))
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in drow], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(FadeIn(txt[2]))
            vo.wait_until("e")
            self.play(FadeIn(txt[3]), FadeIn(note_))
        self.clear_scene()

    def reduction(self):
        m = VGroup(RoundedRectangle(width=3.0, height=1.4, corner_radius=0.15, stroke_color=P.CLAIM),
                   label(r"a machine $T$", font_size=28, color=P.CLAIM))
        m[1].move_to(m[0])
        s = VGroup(RoundedRectangle(width=4.2, height=1.4, corner_radius=0.15, stroke_color=GOAL),
                   MathTex(r"\varphi_T", font_size=44, color=GOAL))
        s[1].move_to(s[0])
        both = VGroup(m, s).arrange(RIGHT, buff=2.2).move_to([0, 1.3, 0])
        ar = Arrow(m.get_right(), s.get_left(), buff=0.15, color=GREY_B)
        al = label(r"translate", font_size=22, color=GREY_A).next_to(ar, UP, buff=0.1)
        desc = VGroup(label(r"$\varphi_T$ describes $T$'s tape, its rules, \ and says: \ `the halting state is "
                            r"reached'", font_size=24, color=GREY_A),
                      MathTex(r"T \text{ halts} \iff \ \models \varphi_T", font_size=44, color=GOAL),
                      label(r"a decision procedure for validity would decide halting: \ impossible", font_size=26,
                            color=BAD)).arrange(DOWN, buff=0.4).move_to([0, -1.3, 0])
        with self.voiceover(
            "Now connect halting to logic. <bookmark mark='a'/>Given any machine T, write down a first-order "
            "sentence phi T. It describes T's tape and its rules, one step to the next, and it ends by saying that "
            "the machine reaches its halting state. <bookmark mark='b'/>Turing showed that the sentence is valid "
            "exactly when the machine halts. <bookmark mark='c'/>So a procedure that decided validity would decide "
            "halting, and nothing can. That is the answer to the Entscheidungsproblem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(m), GrowArrow(ar), FadeIn(al), FadeIn(s))
            self.play(FadeIn(desc[0]))
            vo.wait_until("b")
            self.play(Write(desc[1]))
            vo.wait_until("c")
            self.play(FadeIn(desc[2]))
        self.clear_scene()

    def asymmetry(self):
        d = load("infinity")
        left = VGroup(label(r"valid sentences", font_size=30, color=OK),
                      label(r"can be listed: \ search all proofs \ (completeness)", font_size=22, color=GREY_A),
                      label(r"every valid sentence is eventually confirmed", font_size=22, color=OK)).arrange(
            DOWN, buff=0.15)
        right = VGroup(label(r"invalid sentences", font_size=30, color=BAD),
                       label(r"cannot be listed: \ else validity would be decidable", font_size=22, color=GREY_A),
                       label(r"some are never refuted by any search", font_size=22, color=BAD)).arrange(DOWN,
                                                                                                      buff=0.15)
        lr = VGroup(left, right).arrange(RIGHT, buff=1.3).to_edge(UP, buff=0.5)
        inf = MathTex(d["tex"], font_size=30, color=GOAL).move_to([0, -0.2, 0])
        il = label(r"`everything has something above it; \ nothing is above itself; \ `above' is transitive'",
                   font_size=22, color=GREY_A).next_to(inf, DOWN, buff=0.2)
        chk = d["checked"]
        res = label(rf"true in $(\mathbb{{N}}, <)$; \ no model of size 1--4 \ ({chk[-1][1]:,} relations checked "
                    r"at size 4)".replace(",", "{,}"), font_size=24, color=OK).next_to(il, DOWN, buff=0.35)
        moral = label(r"its negation is invalid, \ but every countermodel is infinite: \ no finite search finds one",
                      font_size=24, color=BAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "So validity is lopsided. <bookmark mark='a'/>The valid sentences can be listed: by completeness, a "
            "machine that searches all proofs will eventually confirm each one. <bookmark mark='b'/>The invalid "
            "ones cannot be listed, or running both searches side by side would decide validity. "
            "<bookmark mark='c'/>Here is a sentence that shows why the second search can fail. Everything has "
            "something above it; nothing is above itself; and 'above' is transitive. <bookmark mark='d'/>It is "
            "true in the natural numbers, ordered by size. But it has no finite model: the Reasoner checked every "
            "relation on up to four objects. Follow the arrows in a finite world and you must come back to where you "
            "started. <bookmark mark='e'/>So its negation is invalid, and yet every countermodel is infinite. No "
            "finite search will ever exhibit one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(Write(inf), FadeIn(il))
            vo.wait_until("d")
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def brick(self):
        w = wall(upto=3, current=3).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(3, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "This is the third brick in the Wall. <bookmark mark='a'/>The dream: settle every question of logic by "
            "calculation. The wall: for full first-order logic, no algorithm can. What survives is "
            "semi-decidability: validity can be confirmed by calculation, but never in general refuted. "
            "<bookmark mark='b'/>The same diagonal will build the next bricks too: Gödel's incompleteness in Part 7, "
            "and Tarski's theorem on truth in Part 8."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(wc, shift=LEFT * 0.2), Indicate(w.brick[3], color=P.WALL))
            vo.wait_until("b")
            self.play(Indicate(wc, color=P.WALL, scale_factor=1.02))
        self.clear_scene()

    def fragments(self):
        d = load("monadic")
        head = label(r"Islands of decidability", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        mon = VGroup(label(r"monadic logic: \ only one-place predicates \ (Löwenheim 1915, Behmann 1922)",
                           font_size=24, color=GOAL),
                     label(r"objects that agree on all $k$ predicates can be merged: \ a model needs at most $2^k$ "
                           r"objects", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        mon.next_to(head, DOWN, buff=0.4)
        sz = d["smallest_model_sizes"]
        bars = bar_row([sz[k] for k in sorted(sz)], [rf"smallest model: {k}" for k in sorted(sz)],
                       [OBJ] * len(sz), width=3.6, height=0.34, font_size=22).move_to([-3.4, -0.9, 0])
        bl = label(rf"{d['satisfiable']} random satisfiable sentences in $k = {d['k']}$ predicates: \ never more "
                   rf"than $2^{d['k']} = {d['bound']}$", font_size=22, color=OK).to_edge(DOWN, buff=0.45)
        frs = VGroup(label(r"also decidable:", font_size=24, color=GREY_A),
                     label(r"$\exists^*\forall^*$ sentences \ (Bernays--Schönfinkel 1928)", font_size=22),
                     label(r"two variables only \ (Mortimer 1975)", font_size=22),
                     label(r"the guarded fragment \ (Andréka, van Benthem, Németi 1998)", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        frs.next_to(bars, RIGHT, buff=0.9)
        if frs.get_right()[0] > 6.8:
            frs.shift(LEFT * (frs.get_right()[0] - 6.8))
        with self.voiceover(
            "The wall has gaps, and they matter. <bookmark mark='a'/>If every predicate takes one argument, as in "
            "Aristotle's logic, validity is decidable. Löwenheim saw why in 1915. With k predicates, each object is "
            "described by which of them it has, and two objects with the same description can be merged. So a "
            "satisfiable sentence has a model with at most two to the k objects, and a finite search settles it. "
            "<bookmark mark='b'/>The Reasoner tested this on random sentences with two predicates. The smallest "
            "models had one, two, three or four objects, and never more than four. <bookmark mark='c'/>Other "
            "decidable fragments: sentences whose existential quantifiers all come before the universal ones; "
            "sentences with only two variables; and the guarded fragment, which keeps every quantifier tied to a "
            "relation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mon))
            vo.wait_until("b")
            for r in bars:
                self.play(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value), run_time=0.6)
            self.play(FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in frs], lag_ratio=0.3))
        self.clear_scene()

    def industry(self):
        head = label(r"Decidable fragments at work", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"description logics, \ OWL", font_size=26, color=GOAL),
                   label(r"the ontology language of the semantic web: \ two-variable and guarded logics", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"SNOMED CT", font_size=26, color=GOAL),
                   label(r"a medical terminology of about 350,000 concepts, classified by a reasoner", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"SMT solvers \ (Z3, cvc5)", font_size=26, color=GOAL),
                   label(r"SAT plus decidable theories of arithmetic, arrays and bit-vectors: \ software verification",
                         font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"Trakhtenbrot 1950", font_size=26, color=BAD),
                   label(r"over finite structures only, validity is not even semi-decidable: \ databases cannot "
                         r"escape the wall", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "These islands are where industry lives. <bookmark mark='a'/>Description logics, close cousins of the "
            "two-variable and guarded fragments, are the language of ontologies on the web. "
            "<bookmark mark='b'/>The medical terminology SNOMED CT, hundreds of thousands of concepts, is "
            "classified by such a reasoner. <bookmark mark='c'/>SMT solvers combine the SAT solvers of Part 2 with "
            "decidable theories of arithmetic and data structures, and check software and hardware every day. "
            "<bookmark mark='d'/>And one more wall: Boris Trakhtenbrot proved in 1950 that if we only care about "
            "finite structures, as databases do, validity becomes even harder: not even semi-decidable."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
