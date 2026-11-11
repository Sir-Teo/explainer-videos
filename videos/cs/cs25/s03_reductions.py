from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, mono)


class Reductions(VoiceoverScene):
    def construct(self):
        self.card()
        self.mapping()
        self.table()

    def card(self):
        card = chapter_card(2, r"Mapping reductions", r"How do you prove a new problem impossible?", lit=(1944,),
                            extra=((1944, r"Post's reducibilities"),), part=PART)
        with self.voiceover("Chapter two. Mapping reductions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def mapping(self):
        head = label('$A\\le_m B$: TOTAL computable $f$ with $w\\in A\\iff f(w)\\in B$', font_size=32).to_edge(
            UP, buff=0.35)
        A = Ellipse(width=3.2, height=3.8, color=DATA).shift(LEFT * 3.5 + UP * 0.25)
        B = Ellipse(width=3.2, height=3.8, color=HEAD).shift(RIGHT * 3.5 + UP * 0.25)
        ina = Ellipse(width=1.8, height=2.0, color=DATA).set_fill(DATA, 0.25).move_to(A).shift(UP * 0.6)
        inb = Ellipse(width=1.8, height=2.0, color=HEAD).set_fill(HEAD, 0.25).move_to(B).shift(UP * 0.6)
        la = label(r"$\Sigma^*$, \ with $A$ inside", font_size=20, color=DATA).next_to(A, DOWN, buff=0.1)
        lb = label(r"$\Sigma^*$, \ with $B$ inside", font_size=20, color=HEAD).next_to(B, DOWN, buff=0.1)
        arrows = VGroup(*[Arrow(ina.get_center() + d, inb.get_center() + d * 0.8, buff=0.1, color=YES,
                                stroke_width=2) for d in (UP * 0.4, DOWN * 0.3)],
                        *[Arrow(A.get_center() + DOWN * 1.2 + d, B.get_center() + DOWN * 1.2 + d * 0.8, buff=0.1,
                                color=NO, stroke_width=2) for d in (LEFT * 0.2, RIGHT * 0.2)])
        notes = VGroup(
            label(r"members go to members, \ non-members to non-members", font_size=22, color=WHITE),
            label(r"if $B$ is decidable, \ so is $A$: \ compute $f$, \ then ask $B$", font_size=22, color=YES),
            label(r"so if $A$ is \textbf{un}decidable, \ $B$ is too: \ the impossibility flows forward", font_size=22,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Almost every impossibility proof after the first one is a reduction. <bookmark mark='a'/> A maps to B "
            "if a computable function f turns every question about A into a question about B with the same answer: "
            "members land inside B, and non-members land outside. <bookmark mark='b'/> Then a decider for B gives a "
            "decider for A: compute f, and ask. <bookmark mark='c'/> Read backwards, if A is undecidable, B must be "
            "too. To prove a new problem impossible, you show that the halting problem reduces to it."
        ) as vo:
            self.play(FadeIn(head), Create(A), Create(B), FadeIn(la), FadeIn(lb), FadeIn(ina), FadeIn(inb))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        head = label(r"A first catalogue", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"$A_{TM}$: \ does $M$ accept $w$?", r"recognizable", 'from $K$: simulate self-input; accept after ANY halt'],
                [r"$E_{TM}$: \ does $M$ accept nothing?", r"co-recognizable", r"$M'$ ignores its input and runs $M$ on "
                 r"$w$"],
                [r"$EQ_{TM}$: \ do $M_1, M_2$ accept the same?", r"neither", 'two reductions: see worked exercise 1'],
                [r"TOT: \ does $M$ halt on every input?", r"neither", r"Chapter 9: \ it is $\Pi_2$-complete"]]
        tab = grid_table([r"problem", r"status", r"the reduction"], rows, widths=[5.4, 2.6, 5.0], row_h=0.56,
                         font_size=20, mono_cols=(), colors=[[WHITE, DATA, GREY_A], [WHITE, LAM, GREY_A],
                                                              [WHITE, NO, GREY_A], [WHITE, NO, GREY_A]])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"the trick in every row: \ build a machine that \textbf{ignores its input} and simulates the hard "
                  r"case", font_size=22, color=YES),
            label(r"a decider for $E_{TM}$ would tell whether $M'$ accepts nothing, \ that is, whether $M$ rejects "
                  r"or loops on $w$", font_size=22, color=WHITE),
            label(r"next: \ one theorem that handles all such questions at once", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here is the catalogue. <bookmark mark='a'/> Acceptance is recognizable and undecidable. To reduce K to acceptance, wrap M so that it simulates M on its own description and ACCEPTS after any halt, including rejection. Emptiness is co-recognizable; equivalence and totality are neither. <bookmark mark='b'/> A standard construction ignores the new machine's input and simulates a chosen computation. <bookmark mark='c'/> Make M prime accept everything if M accepts w, and nothing otherwise. Then M prime has an empty language exactly when M does NOT accept w. A decider for emptiness would decide acceptance by reversing its answer. The exercises give both reductions needed for equivalence. <bookmark mark='d'/> Rice's theorem handles many nontrivial semantic questions together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=3.0)
            for mk, n_ in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
