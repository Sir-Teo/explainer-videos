from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono, words)


def cell_text(c):
    if len(c) == 2 and c[0] in "qa":
        return c[0] + c[1]
    return c


class CookLevin(VoiceoverScene):
    def construct(self):
        self.card()
        self.tableau()
        self.formula()
        self.sizes()

    def card(self):
        card = chapter_card(5, r"Cook--Levin: \ SAT is NP-complete", r"How can one formula capture every NP problem?",
                            lit=(1971, 1973), extra=((1971, r"Cook"), (1973, r"Levin")), part=PART)
        with self.voiceover("Chapter five. Cook-Levin: SAT is NP-complete."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def grid(self, tab, cw=0.62, ch=0.5, origin=LEFT * 5.6 + UP * 1.6):
        g = VGroup()
        cells = {}
        for r, row in enumerate(tab):
            for c, s in enumerate(row):
                sq = Rectangle(width=cw, height=ch, stroke_color=GREY_B, stroke_width=1.0)
                sq.move_to(origin + RIGHT * c * cw + DOWN * r * ch)
                head = len(s) == 2
                if head:
                    sq.set_fill(HEAD if s[0] == "q" else YES, 0.45)
                t = mono(cell_text(s), 18, WHITE).move_to(sq)
                g.add(VGroup(sq, t))
                cells[(r, c)] = sq
        return g, cells

    def tableau(self):
        d = load("tableau")
        head = label(r"The tableau: \ one row per step, \ one column per tape cell", font_size=30).to_edge(UP,
                                                                                                 buff=0.3)
        g, cells = self.grid(d["tableau"])
        rl = VGroup(*[mono(f"t={r}", 16, GREY_B).next_to(cells[(r, 0)], LEFT, buff=0.12)
                      for r in range(len(d["tableau"]))])
        mach = VGroup(
            label(r"an NTM: \ ``does $w$ contain a 1?'' \ state $q$ moves right; \\ on a 1 it may \textbf{guess} "
                  r"to accept \ ($a$)", font_size=20, color=WHITE),
            label(rf"input $w$ = {d['w']}: \ $T$ = 6 rows, \ 10 columns \ (borders \#)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g, DOWN, buff=0.4).align_to(g, LEFT)
        win = SurroundingRectangle(VGroup(cells[(1, 1)], cells[(2, 3)]), color=LAM, buff=0.02, stroke_width=4)
        notes = VGroup(
            label(r"a \textbf{window}: \ 2 rows $\times$ 3 columns", font_size=21, color=LAM),
            label(r"the machine is local: \ a cell changes only \\ next to the head", font_size=21, color=WHITE),
            label(rf"so a list of \textbf{{legal windows}} \ ({d['legal']} here) \\ describes every step", font_size=21,
                  color=DATA),
            label(r"if every window is legal, \\ each row follows from the last", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        fit_right(notes)
        with self.voiceover(
            "Stephen Cook in 1971, and Leonid Levin independently in the Soviet Union, proved that satisfiability is "
            "NP-complete. The proof writes a whole computation as a table. <bookmark mark='a'/> Take any problem in "
            "NP, decided by a nondeterministic machine in polynomial time. Ours asks whether the input contains a "
            "one: it moves right, and on a one it may guess to accept. <bookmark mark='b'/> Write the computation "
            "as a tableau. Row t is the tape at time t, with the head's cell marked by its state. Here the input is "
            "zero, zero, one, zero; at time two the head reaches the one and guesses, and from then on it sits in "
            "the accept state. <bookmark mark='c'/> Now look at "
            "a small window, two rows by three columns. <bookmark mark='d'/> A machine is local: in one step, only "
            "the cells next to the head can change. <bookmark mark='e'/> So a finite list of legal windows, four "
            "hundred and eight for our machine, describes every possible step. <bookmark mark='f'/> If every window "
            "in the tableau is on the list, each row really is a successor of the one above."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mach[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.01), FadeIn(rl), FadeIn(mach[1]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(Create(win), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(win.animate.move_to(VGroup(cells[(2, 2)], cells[(3, 4)])), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(win.animate.move_to(VGroup(cells[(3, 3)], cells[(4, 5)])), FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(win.animate.move_to(VGroup(cells[(0, 0)], cells[(1, 2)])), FadeIn(notes[3]))
            self.play(win.animate.move_to(VGroup(cells[(4, 7)], cells[(5, 9)])), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def formula(self):
        head = label(r"The formula: \ a variable $x_{t,j,s}$ for ``cell $(t, j)$ holds $s$''", font_size=30).to_edge(
            UP, buff=0.35)
        parts = VGroup(
            MathTex(r"\varphi \;=\; \varphi_{\text{cell}} \wedge \varphi_{\text{start}} \wedge "
                    r"\varphi_{\text{move}} \wedge \varphi_{\text{accept}}", font_size=40, color=HEAD),
            label(r"$\varphi_{\text{cell}}$: \ every cell holds exactly one symbol", font_size=22, color=WHITE),
            label(r"$\varphi_{\text{start}}$: \ row 0 is the input, \ head on the left, \ in the start state",
                  font_size=22, color=DATA),
            label(r"$\varphi_{\text{move}}$: \ every window is one of the legal ones", font_size=22, color=LAM),
            label(r"$\varphi_{\text{accept}}$: \ some cell in some row holds the accept state", font_size=22,
                  color=YES),
            label(r"$\varphi$ is satisfiable $\iff$ some branch accepts $\iff$ $w \in L$", font_size=24, color=HEAD),
            label(r"size: \ $T \times T$ cells, \ a constant number of symbols and windows each: \ polynomial in $T$",
                  font_size=22, color=GREY_A),
            label(r"the formula is built \textbf{without} knowing the answer: \ a reduction from every NP problem",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Now turn the tableau into a formula. <bookmark mark='a'/> For every cell and every symbol, a variable: "
            "true if that cell holds that symbol. The formula has four parts. <bookmark mark='b'/> Every cell holds "
            "exactly one symbol. <bookmark mark='c'/> The first row is the input, with the machine in its start "
            "state at the left. <bookmark mark='d'/> Every window is legal. <bookmark mark='e'/> And somewhere, the "
            "accept state appears. <bookmark mark='f'/> A satisfying assignment is exactly an accepting tableau, so "
            "the formula is satisfiable if and only if some branch accepts. <bookmark mark='g'/> The tableau is T by "
            "T, with a constant amount of formula per cell, so the size is polynomial. <bookmark mark='h'/> And the "
            "construction needs only the machine and the input, never the answer. That is a polynomial reduction "
            "from every problem in NP to SAT."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdefgh", parts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def sizes(self):
        d = load("tableau")
        head = label(r"We built the formulas and solved them", font_size=32).to_edge(UP, buff=0.35)
        rows = [[str(r["n"]), str(r["T"]), words(r["vars"]), words(r["clauses"]), f"{r['seconds']:.2f} s"]
                for r in d["rows"]]
        tab = grid_table([r"input length", r"rows $T$", r"variables", r"clauses", r"solved in"], rows,
                         widths=[2.2, 1.6, 2.2, 2.2, 2.0], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[WHITE, GREY_A, DATA, DATA, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(r"inputs \texttt{0}$\cdots$\texttt{01}: \ the variables grow like $T^2$, \ as promised", font_size=21,
                  color=WHITE),
            label(rf"our CDCL solver finds the accepting tableau; \ for \texttt{{0000}} it proves the formula "
                  rf"unsatisfiable", font_size=21, color=YES),
            label(r"decoding the solver's assignment gives back the table of the first slide", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "We implemented the construction. <bookmark mark='a'/> For inputs of two to eight symbols, the formula "
            "grows from three thousand variables to twenty-three thousand, roughly as the square of the time bound. "
            "<bookmark mark='b'/> Our SAT solver, the one chapter thirteen explains, finds a satisfying assignment "
            "in a fraction of a second, and for the input zero, zero, zero, zero it proves there is none. <bookmark "
            "mark='c'/> Reading the assignment back cell by cell reproduces the accepting tableau we drew. A "
            "question about a machine has become a question about a formula."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(notes[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
