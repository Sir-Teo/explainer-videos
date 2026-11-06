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
            label(r"give it the halting set $K$ as oracle: \ now every $\Sigma_1$ question is one step", font_size=22,
                  color=DATA),
            label(r"but the diagonal argument \textbf{relativizes}: \ oracle machines cannot decide their own halting "
                  r"problem $K'$", font_size=22, color=NO),
            label(r"so $\emptyset < K < K' < K'' < \cdots$: \ an infinite tower of ever harder problems, \ the "
                  r"\textbf{jumps}", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(VGroup(m, o), DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "Is halting the hardest problem there is? <bookmark mark='a'/> Turing asked in 1939 what a machine "
            "could do with a magic box, an oracle, that answers membership in some set in a single step. A problem "
            "is Turing-reducible to B if a machine with an oracle for B solves it. <bookmark mark='b'/> Give a "
            "machine the halting set as its oracle. Every question of the form, does some search succeed, is now "
            "one step. <bookmark mark='c'/> But Part 1's diagonal argument works just as well for oracle machines: "
            "they cannot decide whether oracle machines halt. That is a new, harder problem, the jump of K. "
            "<bookmark mark='d'/> Give that an oracle and jump again. There is an infinite tower of problems, each "
            "strictly harder than the last."
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
        head = label(r"Count the quantifiers", font_size=34).to_edge(UP, buff=0.3)
        rungs = [
            (r"$\Delta_0$: \ decidable", r"$x$ is prime; \ $M$ halts within 100 steps", YES),
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
            label(r"Post's theorem \ (1948): \ $\Sigma_{n+1}$ = recognizable with an oracle for the $n$-th jump",
                  font_size=20, color=WHITE),
            label(r"FIN is $\Sigma_2$-complete; \ TOT is $\Pi_2$-complete; \ COF is $\Sigma_3$-complete", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is a ruler for this tower: count the alternating quantifiers. <bookmark mark='a'/> At the bottom, "
            "questions a program settles by bounded search: is x prime, does M halt within a hundred steps. "
            "<bookmark mark='b'/> One existential quantifier in front, there exists a time t at which M has halted, "
            "gives sigma one: halting itself, and the equations of chapter seven. <bookmark mark='c'/> One "
            "universal quantifier gives pi one: M never halts. So do Goldbach's conjecture and the Riemann "
            "hypothesis, and the consistency of set theory; each says some search never succeeds. <bookmark "
            "mark='d'/> Two quantifiers. Halting on only finitely many inputs is sigma two. <bookmark mark='e'/> "
            "Halting on every input, TOT, is pi two: for every input, there is a time. So are the twin prime "
            "conjecture, the Collatz conjecture, and P not equal to NP, the subject of Part 26. <bookmark mark='f'/> "
            "And halting on all but finitely many inputs is sigma three. <bookmark mark='g'/> Emil Post proved in "
            "1948 that each level is exactly what a recognizer can do with an oracle for the jump below, and each of "
            "these machine problems is complete for its level."
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
            label(r"every undecidable set so far computes $K$: \\ is every recognizable set decidable, \\ or as "
                  r"hard as $K$?", font_size=21, color=WHITE),
            label(r"Post \ (1944) \ asked; \\ Friedberg \ (1957) \ and Muchnik \ (1956) \ answered \textbf{no}",
                  font_size=21, color=HEAD),
            label(r"the \textbf{priority method}: \ build $A$ and $B$ in stages, \\ meeting infinitely many demands, "
                  r"\ each injured finitely often", font_size=21, color=DATA),
            label(r"Sacks \ (1964): \ between any two such degrees lies a third: \\ the picture is dense, \ not a "
                  r"ladder", font_size=21, color=LAM),
            label(r"but no \textit{natural} problem is known to sit strictly between: \\ every one we meet is "
                  r"decidable or complete", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(VGroup(A, B), RIGHT, buff=0.9).shift(DOWN * 0.2)
        fit_right(lines)
        with self.voiceover(
            "One last question about the recognizable sets. <bookmark mark='a'/> Every undecidable one we have met "
            "so far is exactly as hard as halting. Is that always so? <bookmark mark='b'/> Emil Post asked in 1944, "
            "and it took twelve years. Albert Muchnik in Moscow and Richard Friedberg, an undergraduate at Harvard, "
            "independently built two recognizable sets, neither of which can compute the other, so both lie "
            "strictly between the decidable sets and K. <bookmark mark='c'/> Their technique, the priority method, "
            "builds the sets in stages, satisfying an infinite list of requirements, each one disturbed only "
            "finitely often by those ranked above it. <bookmark mark='d'/> Gerald Sacks showed later that between "
            "any two such degrees there is another: the structure is dense. <bookmark mark='e'/> And yet every "
            "natural problem anyone has found is either decidable or exactly as hard as halting. Nobody knows why."
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
