from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Kochen(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Kochen--Specker and the magic square", r"Can every quantity have a value?",
                            lit=(1967, 1990), part=PART)
        with self.voiceover("Chapter eight. Kochen, Specker, and the magic square."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.square()
        self.parity()
        self.contextual()

    def theorem(self):
        hc = history_card(1967, r"Simon Kochen and Ernst Specker", r"`The Problem of Hidden Variables'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"a non-contextual value assignment: \ every observable has a value, \ whatever else is "
                       r"measured with it", CLASS),
                      (r"and the values respect the algebra: \ if $C = AB$ for commuting $A, B$, \ then $v(C) = v(A)\,"
                       r"v(B)$", ABS),
                      (r"Kochen and Specker: \ in three or more dimensions, \ no such assignment exists", BAD),
                      (r"their proof used 117 directions in space; \ Peres and Mermin found a square of nine", GOAL)],
                     font_size=22, aligned_edge=LEFT, width=11.4, buff=0.34).move_to([0, -0.4, 0])
        with self.voiceover(
            "Bell needs two separated particles. Kochen and Specker's theorem of 1967 needs only one system. "
            "<bookmark mark='a'/>Ask for a non-contextual assignment: every observable has a definite value, the "
            "same whatever else is measured alongside it. <bookmark mark='b'/>And the values respect the algebra: if "
            "one observable is the product of two commuting ones, its value is the product of their values. "
            "<bookmark mark='c'/>Kochen and Specker proved that in a space of three or more dimensions no such "
            "assignment exists. <bookmark mark='d'/>Their proof used a hundred and seventeen directions in space. "
            "Asher Peres and David Mermin, around 1990, found one that fits in a three by three square."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def square(self):
        d = load("pm")
        head = label(r"The Peres--Mermin square", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        tex = {"I": r"1", "X": r"X", "Y": r"Y", "Z": r"Z"}
        cells = VGroup()
        for r, row in enumerate(d["square"]):
            for c, s in enumerate(row):
                box = Square(side_length=1.15, color=WAVE, stroke_width=2).move_to([-4.4 + 1.3 * c, 1.0 - 1.3 * r, 0])
                t = MathTex(rf"{tex[s[0]]} \otimes {tex[s[1]]}", font_size=26, color=WHITE).move_to(box)
                cells.add(VGroup(box, t))
        rp = VGroup(*[MathTex(rf"{v:+d}", font_size=28, color=OK).next_to(cells[3 * r + 2], RIGHT, buff=0.3)
                      for r, v in enumerate(d["row_products"])])
        cp = VGroup(*[MathTex(rf"{v:+d}", font_size=28, color=OK if v > 0 else BAD).next_to(cells[6 + c], DOWN,
                                                                                          buff=0.3)
                      for c, v in enumerate(d["column_products"])])
        side = stack([(r"each row and each column: \ three commuting observables", WAVE),
                      (r"right: \ the product of each row, \ as an operator: \ $+1, +1, +1$", OK),
                      (r"below: \ the product of each column: \ $+1, +1, -1$", BAD),
                      (r"values $\pm 1$ in the cells: \ multiply all nine by rows, \ $+1$; \ by columns, \ $-1$",
                       ABS),
                      (rf"the Reasoner tries all {d['assignments']}: \ {d['consistent_assignments']} work; \ the best "
                       rf"meets {d['best_constraints_met']} of the 6 constraints", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=5.8, buff=0.3).move_to([3.6, -0.4, 0])
        assert d["commuting"] and d["consistent_assignments"] == 0
        with self.voiceover(
            "Here is the square. <bookmark mark='a'/>Nine observables on a pair of qubits, built from Pauli "
            "matrices. The three in each row commute, and so do the three in each column, so each row and each column "
            "can be measured together. <bookmark mark='b'/>The Reasoner multiplies them as matrices. Each row "
            "multiplies to the identity, plus one. <bookmark mark='c'/>The first two columns multiply to plus one, "
            "and the third to minus one. <bookmark mark='d'/>Now try to write a value, plus or minus one, in every "
            "cell. Multiplying all nine values row by row gives plus one; column by column, minus one. They are the "
            "same nine numbers. <bookmark mark='e'/>So no assignment can work, and the Reasoner confirms it, trying "
            "all five hundred and twelve: none satisfies all six constraints, and the best manage five."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(rp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(cells[8], color=BAD))
        self.clear_scene()

    def parity(self):
        d = load("cabello")
        head = label(r"A proof by parity", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["n_vectors"] == 18 and d["n_bases"] == 9 and d["orthogonal"] and d["each_in_two"]
        assert d["consistent_assignments"] == 0 and d["best_bases_met"] == 8 and d["assignments"] == 262144

        def vec(v):
            return "".join(r"\bar1" if c < 0 else str(c) for c in v)

        palette = [WAVE, ALICE, BOB, CLASS, ABS, PART_C, OK, BAD, HIST]
        first = {}
        cols = VGroup()
        for j, b in enumerate(Q.CABELLO):
            col = VGroup()
            for v in b:
                k = tuple(v)
                if k not in first:
                    first[k] = len(first)
                col.add(MathTex(vec(v), font_size=22, color=GREY_A))
            col.arrange(DOWN, buff=0.22)
            frame = SurroundingRectangle(col, color=GREY_D, buff=0.12, corner_radius=0.08)
            tag = label(rf"basis {j + 1}", font_size=16, color=GREY_B).next_to(frame, UP, buff=0.08)
            cols.add(VGroup(frame, col, tag))
        cols.arrange(RIGHT, buff=0.18).move_to([0, 0.75, 0])
        if cols.width > 13.2:
            cols.width = 13.2
        # one direction, shown in both of its bases
        target = (1, 1, 0, 0)
        hits = [cols[j][1][i] for j, b in enumerate(Q.CABELLO) for i, v in enumerate(b) if tuple(v) == target]
        assert len(hits) == 2
        side = stack([(r"18 directions in 4 dimensions; \ 9 bases of 4 orthogonal directions", WHITE),
                      (r"checked: \ every basis orthogonal, \ every direction in exactly two bases", OK),
                      (r"a non-contextual assignment: \ exactly one `yes' in each basis", ABS)], font_size=21,
                     aligned_edge=LEFT, width=12.0, buff=0.22).move_to([0, -1.55, 0])
        count = VGroup(MathTex(r"\text{by bases: } \underbrace{1 + 1 + \cdots + 1}_{9} = 9 \;\;(\text{odd})",
                               font_size=28, color=PART_C),
                       MathTex(r"\text{by directions: } 2 \times \#\{\text{yes}\} \;\;(\text{even})", font_size=28,
                               color=PART_C)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)
        final = label(r"all $2^{18} = 262\,144$ assignments tried: \ none works; \ the best satisfies 8 bases of 9",
                      font_size=21, color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is an even simpler proof, by counting. <bookmark mark='a'/>In 1996 Adán Cabello, José Estebaranz "
            "and Guillermo García-Alcaine found eighteen directions in a four-dimensional space, arranged in nine "
            "groups of four mutually orthogonal directions. <bookmark mark='b'/>The Reasoner checks the geometry: "
            "every group is orthogonal, and every direction appears in exactly two groups. "
            "<bookmark mark='c'/>Each group is a complete measurement, so a non-contextual assignment must say yes "
            "to exactly one direction in each group. <bookmark mark='d'/>Now count the yeses. Group by group, there "
            "are nine, an odd number. Direction by direction, each yes is counted twice, so the total is even. "
            "<bookmark mark='e'/>No assignment can exist. The Reasoner tries all two hundred and sixty-two thousand, "
            "one hundred and forty-four anyway: none works, and the best satisfies eight groups of the nine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.12), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), *[h.animate.set_color(PART_C) for h in hits])
            self.play(*[Indicate(h, color=PART_C, scale_factor=1.3) for h in hits])
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Write(count[0]))
            self.play(Write(count[1]))
            vo.wait_until("e")
            self.play(FadeOut(count), FadeIn(final))
        self.clear_scene()

    def contextual(self):
        head = label(r"Contextuality", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the lesson", r"if observables have values, \ the value of one can depend on which others are measured "
                            r"with it", ABS),
            (r"Bohm", r"accepts it: \ outcomes depend on the whole experimental arrangement, \ as Bohr insisted",
             CLASS),
            (r"the test", r"contextuality has been seen with trapped ions, \ photons and neutrons", OK),
            (r"the use", r"contextuality is a resource: \ it powers some quantum speed-ups \ (Howard et al., \ 2014)",
             GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "The lesson is contextuality. <bookmark mark='a'/>If observables have values at all, the value of one "
            "must depend on which others are measured alongside it. <bookmark mark='b'/>Bohmian mechanics accepts "
            "this: outcomes depend on the whole experimental arrangement, a point on which Bohm and Bohr agreed. "
            "<bookmark mark='c'/>Contextuality has been seen directly in experiments with trapped ions, photons and "
            "neutrons. <bookmark mark='d'/>And it turns out to be useful: Mark Howard and colleagues showed in 2014 "
            "that contextuality is the resource behind a leading approach to fault-tolerant quantum computing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
