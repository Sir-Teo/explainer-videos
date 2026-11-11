from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, mono)


class Degrees(VoiceoverScene):
    def construct(self):
        self.card()
        self.oracles()
        self.ladder()
        self.post()

    def card(self):
        card = chapter_card(9, r"Oracles and the arithmetic hierarchy", r"Is there anything harder than halting?",
                            lit=(1939, 1957), extra=((1939, r"Turing's oracles"), (1957, r"Friedberg--Muchnik")),
                            part=PART)
        with self.voiceover("Chapter nine. Oracles and the arithmetic hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def oracles(self):
        head = label(r"A machine with a magic box", font_size=34).to_edge(UP, buff=0.35)
        m = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.12, color=DATA).set_fill(BG, 1).shift(
            LEFT * 3.4 + UP * 1.0)
        ml = label(r"machine $M^A$", font_size=22, color=DATA).move_to(m)
        o = RoundedRectangle(width=2.2, height=1.6, corner_radius=0.12, color=HEAD).set_fill(HEAD, 0.25).shift(
            RIGHT * 1.4 + UP * 1.0)
        ol = label(r"oracle for $A$", font_size=22, color=HEAD).move_to(o)
        q = Arrow(m.get_right() + UP * 0.3, o.get_left() + UP * 0.3, buff=0.05, color=WHITE, stroke_width=2.5)
        a = Arrow(o.get_left() + DOWN * 0.3, m.get_right() + DOWN * 0.3, buff=0.05, color=YES, stroke_width=2.5)
        ql = label(r"is $x \in A$?", font_size=18, color=WHITE).next_to(q, UP, buff=0.05)
        al = label(r"yes / no, \ in one step", font_size=18, color=YES).next_to(a, DOWN, buff=0.05)
        lines = VGroup(
            label(r"Turing \ (1939): \ $A \le_T B$ \ if some machine with a $B$-oracle decides $A$", font_size=22,
                  color=WHITE),
            label('a $K$ oracle: one query AFTER a computable reduction decides a $\\Sigma_1$ question', font_size=22,
                  color=DATA),
            label(r"but the diagonal argument \textbf{relativizes}: \ oracle machines cannot decide their own halting "
                  r"problem $K'$", font_size=22, color=NO),
            label(r"so $\emptyset < K < K' < K'' < \cdots$: \ an infinite tower of ever harder problems, \ the "
                  r"\textbf{jumps}", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(VGroup(m, o), DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "An oracle answers a chosen membership query in one abstract step. <bookmark mark='a'/> Turing reducibility permits an algorithm to query the oracle during its computation. <bookmark mark='b'/> A K oracle decides a sigma-one question after a computable reduction to K and one query. The reduction itself still takes computation; the whole task is not necessarily one step. <bookmark mark='c'/> The diagonal argument relativizes: machines with a K oracle cannot decide their own halting problem, K prime. <bookmark mark='d'/> Repeating the jump produces an infinite strictly increasing tower of Turing degrees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(m), FadeIn(ml), FadeIn(o), FadeIn(ol))
            vo.wait_until("a")
            self.play(GrowArrow(q), FadeIn(ql), GrowArrow(a), FadeIn(al), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ladder(self):
        head = label('Alternating quantifier blocks over computable predicates', font_size=34).to_edge(UP, buff=0.3)
        rungs = [
            ('$\\Delta_1$: decidable', r"$x$ is prime; \ $M$ halts within 100 steps", YES),
            (r"$\Sigma_1$: \ $\exists t$", r"$M$ halts \ ($K$); \ an equation has a solution \ (ch. 7)", DATA),
            (r"$\Pi_1$: \ $\forall t$", r"$M$ never halts; \ Goldbach; \ the Riemann hypothesis; \ Con(ZFC)", DATA),
            (r"$\Sigma_2$: \ $\exists \forall$", r"FIN: \ $M$ halts on only finitely many inputs", HEAD),
            (r"$\Pi_2$: \ $\forall \exists$", r"TOT: \ $M$ halts on \textbf{every} input; \ twin primes; \ Collatz; "
                                              r"\ P $\ne$ NP", HEAD),
            (r"$\Sigma_3$: \ $\exists \forall \exists$", r"COF: \ $M$ halts on all but finitely many inputs", LAM),
        ]
        ladder = VGroup()
        for i, (lv, ex, col) in enumerate(rungs):
            box_ = RoundedRectangle(width=3.0, height=0.62, corner_radius=0.08, color=col).set_fill(col, 0.18)
            lt = label(lv, font_size=21, color=col).move_to(box_)
            et = label(ex, font_size=19, color=WHITE).next_to(box_, RIGHT, buff=0.3)
            ladder.add(VGroup(box_, lt, et))
        ladder.arrange(UP, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        fit_right(ladder)
        notes = VGroup(
            label('Post: $\\Sigma_{n+1}$ is r.e. relative to $\\emptyset^{(n)}$; $\\Pi_{n+1}$ is co-r.e. relative to it',
                  font_size=20, color=WHITE),
            label(r"FIN is $\Sigma_2$-complete; \ TOT is $\Pi_2$-complete; \ COF is $\Sigma_3$-complete", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Count alternating quantifier BLOCKS over computable predicate matrices. <bookmark mark='a'/> Delta one means decidable sets. Bounded-formula delta zero is a different syntactic class. <bookmark mark='b'/> A leading existential block gives sigma one: for example there exists a time when M halts. <bookmark mark='c'/> A universal block gives pi one, including the displayed nonhalting formulations. These are upper-level formulations of conjectures, not completeness classifications of individual closed sentences. <bookmark mark='d'/> Finitely many halting inputs, FIN, is sigma-two-complete. <bookmark mark='e'/> Totality, TOT, is pi-two-complete. The other displayed conjectures admit pi-two formulations; that does not make them complete. <bookmark mark='f'/> Cofinitely many halting inputs, COF, is sigma-three-complete. <bookmark mark='g'/> Post's theorem says sigma n plus one is recognizable relative to the n-th jump; pi n plus one is co-recognizable relative to that oracle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", ladder):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.15))
            vo.wait_until("g")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    def post(self):
        head = label(r"Post's problem", font_size=34).to_edge(UP, buff=0.35)
        lo = Dot(DOWN * 2.0 + LEFT * 3.0, color=YES, radius=0.1)
        hi = Dot(UP * 1.2 + LEFT * 3.0, color=NO, radius=0.1)
        lol = label(r"decidable", font_size=20, color=YES).next_to(lo, DOWN, buff=0.1)
        hil = label(r"$K$", font_size=22, color=NO).next_to(hi, UP, buff=0.1)
        A = Dot(LEFT * 4.0 + DOWN * 0.4, color=HEAD, radius=0.09)
        B = Dot(LEFT * 2.0 + DOWN * 0.4, color=HEAD, radius=0.09)
        Al = label(r"$A$", font_size=22, color=HEAD).next_to(A, LEFT, buff=0.1)
        Bl = label(r"$B$", font_size=22, color=HEAD).next_to(B, RIGHT, buff=0.1)
        edges = VGroup(*[Line(x.get_center(), y.get_center(), color=GREY_B, stroke_width=1.5)
                         for x, y in ((lo, A), (lo, B), (A, hi), (B, hi))])
        cross = label(r"$A \not\le_T B, \ B \not\le_T A$", font_size=20, color=HEAD).next_to(VGroup(A, B), DOWN,
                                                                                         buff=0.25)
        lines = VGroup(
            label('Post: must every c.e. degree below $K$ be decidable or complete?', font_size=21, color=WHITE),
            label(r"Post \ (1944) \ asked; \\ Friedberg \ (1957) \ and Muchnik \ (1956) \ answered \textbf{no}",
                  font_size=21, color=HEAD),
            label(r"the \textbf{priority method}: \ build $A$ and $B$ in stages, \\ meeting infinitely many demands, "
                  r"\ each injured finitely often", font_size=21, color=DATA),
            label('Sacks density: between DISTINCT COMPARABLE c.e. degrees; not between incomparable $A,B$', font_size=21, color=LAM),
            label('natural intermediate examples: a research theme; naturalness is an informal criterion', font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(VGroup(A, B), RIGHT, buff=0.9).shift(DOWN * 0.2)
        fit_right(lines)
        with self.voiceover(
            "Post asked about the computably enumerable degrees below K. <bookmark mark='a'/> Must a recognizable set be decidable or complete? <bookmark mark='b'/> Friedberg and Muchnik constructed incomparable computably enumerable sets A and B. Both degrees are strictly between the decidable degree and K. <bookmark mark='c'/> Their priority constructions meet infinitely many requirements, each injured only finitely often by higher priorities. <bookmark mark='d'/> Sacks's density theorem inserts a degree between any two DISTINCT COMPARABLE computably enumerable degrees. It does not insert one between the incomparable A and B in this drawing. <bookmark mark='e'/> Finding convincing natural intermediate examples is a research theme, with naturalness an informal criterion. It is not the theorem that every conceivable natural problem is decidable or complete."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lo), FadeIn(hi), FadeIn(lol), FadeIn(hil))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(B), FadeIn(Al), FadeIn(Bl), Create(edges), FadeIn(cross), FadeIn(lines[1]))
            for mk, ln in zip("cde", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
