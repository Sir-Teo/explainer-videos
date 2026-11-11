from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, mono, region)


class Beavers(VoiceoverScene):
    def construct(self):
        self.card()
        self.growth()
        self.dominate()
        self.knowledge()

    def card(self):
        card = chapter_card(12, r"Busy beavers, again", r"Where does knowledge run out?", lit=(1962, 2024),
                            extra=((1962, r"Rad\'o"), (2016, r"Yedidia--Aaronson"), (2024, r"BB(5)")), part=PART)
        with self.voiceover("Chapter twelve. Busy beavers, again."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def growth(self):
        head = label(r"Three speeds of growth", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"1", r"2", r"2", r"3", r"1"],
            [r"2", r"4", r"4", r"7", r"6"],
            [r"3", r"8", r"16", r"61", r"21"],
            [r"4", r"16", r"65,536", r"$2^{2^{2^{65536}}} - 3$", r"107"],
            [r"5", r"32", r"$2^{65536}$", r"far larger", r"47,176,870"],
            [r"6", r"64", r"$2 \uparrow\uparrow 6$", r"far larger still", r"unknown \ (Part 1)"],
        ]
        tab = grid_table([r"$n$", r"$2^n$", r"$2 \uparrow\uparrow n$", r"Ackermann $A(n, n)$", r"busy beaver $S(n)$"],
                         rows, widths=[0.9, 1.3, 2.2, 3.7, 3.1], row_h=0.5, font_size=20, mono_cols=(),
                         colors=[[WHITE, GREY_A, DATA, HEAD, NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        notes = VGroup(
            label(r"\textbf{loops with fixed bounds} \ (primitive recursion): \ $2^n$, \ towers, \ any fixed stack of "
                  r"them", font_size=21, color=DATA),
            label(r"Ackermann \ (1928): \ computable, \ total, \ and outgrows every one of them \ (the promise of Part "
                  r"11)", font_size=21, color=HEAD),
            label('effective total Nat-to-Nat syntax; total interpreter; closure under the displayed diagonal operation', font_size=21, color=LAM),
            label(r"if \texttt{interp} were in it, \ so is $d(x) = \texttt{interp}(x, x) + 1$; \ then $d(\ulcorner d "
                  r"\urcorner) = d(\ulcorner d \urcorner) + 1$ \ (Part 14)", font_size=20, color=GREY_A),
            label(r"the busy beaver outgrows even Ackermann: \ it outgrows \textbf{every} computable function",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Compare primitive recursive, total computable and busy-beaver growth. <bookmark mark='a'/> Primitive recursion computes exponentials, variable-height towers, and fixed iterations of such constructions. <bookmark mark='b'/> Ackermann's diagonal growth eventually dominates every primitive recursive function, while remaining total computable. <bookmark mark='c'/> For an effectively enumerable total language of functions from unbounded natural numbers to natural numbers, assume a computable total interpreter on valid codes, extended by a default on invalid codes. <bookmark mark='d'/> If the language also represented that interpreter and the diagonal function interpreter of x on x plus one, applying the diagonal to its own code would contradict equality. The coding and closure assumptions matter, including for typed languages. <bookmark mark='e'/> The LAST column, S, eventually dominates every total computable function, including Ackermann."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), run_time=2.5)
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def dominate(self):
        head = label(r"$S$ eventually exceeds every computable $f$", font_size=34).to_edge(UP, buff=0.35)
        parts = VGroup(
            region(3.0, 0.8, r"write $n$ \ ($n$ states)", DATA, font_size=20),
            region(3.0, 0.8, 'compute $\\max(f(2n),f(2n+1))$ \\\\ (fixed $c$ states)', HEAD, font_size=20),
            region(3.0, 0.8, r"count down \ ($\approx$ 3 states)", LAM, font_size=20),
        ).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.5)
        arr = VGroup(*[Arrow(parts[i].get_right(), parts[i + 1].get_left(), buff=0.05, color=GREY_B,
                             stroke_width=2) for i in range(2)])
        brace = Brace(parts, DOWN, color=GREY_B)
        bl = label(r"one machine $M_n$ with $n + c'$ states, \ halting after more than $f(2n)$ steps", font_size=20,
                   color=WHITE).next_to(brace, DOWN, buff=0.1)
        lines = VGroup(
            label(r"so $S(n + c') > f(2n)$ \ for every $n$", font_size=24, color=HEAD),
            label(r"for $n \ge c'$: \ $S(2n) \ \ge \ S(n + c') \ > \ f(2n)$ \ (and the odd sizes alike)", font_size=24,
                  color=YES),
            label(r"so no computable function bounds $S$: \ knowing such a bound would decide halting", font_size=22,
                  color=NO),
        ).arrange(DOWN, buff=0.3).next_to(bl, DOWN, buff=0.5)
        with self.voiceover(
            "The proof is a machine built in three pieces. <bookmark mark='a'/> Take any TOTAL computable natural-valued function f, computed by a machine with c states. For each n, build a machine that first writes n on its tape, which takes n states; <bookmark mark='b'/> then computes the larger of f of two n and f of two n plus one, using a fixed number c of states; then counts that number down to zero, a few states more. <bookmark mark='c'/> It has n plus a constant states, and it halts after more than f of two n steps. <bookmark mark='d'/> So the busy beaver of n plus that constant is bigger than f of two n. <bookmark mark='e'/> Once n is larger than the constant, the busy beaver of two n is bigger still. The same maximum also covers the next odd size, by monotonicity of S. Thus S passes f at every sufficiently large size and stays ahead. <bookmark mark='f'/> No computable function can even bound it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(parts[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(parts[1]), GrowArrow(arr[1]), FadeIn(parts[2]))
            vo.wait_until("c")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def knowledge(self):
        head = label(r"Famous questions as busy-beaver values", font_size=32).to_edge(UP, buff=0.3)
        rows = [[r"5", r"settled: \ $S(5) = 47{,}176{,}870$", r"bbchallenge, \ checked in Coq \ (2024)"],
                [r"6", r"Antihydra: \ a Collatz-like question", r"mxdys \ (2024; \ Part 1)"],
                [r"15", r"Erd\H{o}s: \ does every $2^n$, $n > 8$, \ have a 2 in base 3?", r"St\'erin and Woods "
                                                                                        r"\ (2021)"],
                [r"27", r"Goldbach's conjecture", r"posted in 2015 \ (unverified)"],
                [r"744", r"the Riemann hypothesis", r"Aaronson, \ Matiyasevich, \ O'Rear \ (2016)"],
                ['7,910; 432 claimed (2025)', r"the consistency of ZFC", r"Yedidia and Aaronson \ (2016) \ and after"]]
        tab = grid_table([r"states", 'value or conjecture encoding; evidence differs by row', r"by"], rows,
                         widths=[1.6, 6.6, 4.6], row_h=0.5, font_size=19, mono_cols=(),
                         colors=[[HEAD, WHITE, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        lines = VGroup(
            label('S($n$) settles an encoded conjecture only AFTER its at-most-$n$-state encoding is verified',
                  font_size=21, color=YES),
            label('effective sound sufficiently strong arithmetic $T$: only finitely many exact $S(n)$ values provable', font_size=21, color=NO),
            label('checked published upper bound: 7,910; 432 (2025) conditional on construction verification', font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Busy-beaver tables combine established values and conditional encoding claims. <bookmark mark='a'/> S of five is established. Other rows describe particular conjecture-search machines: the reported twenty-seven-state Goldbach encoding still needs verification, while larger published constructions have different evidence. <bookmark mark='b'/> Knowing S of n settles a conjecture only after a CORRECT at-most-n-state encoding is established. We therefore make no unconditional Goldbach conclusion from the unverified twenty-seven-state claim. <bookmark mark='c'/> An effectively axiomatized sound sufficiently strong arithmetic theory can prove only finitely many exact S values: otherwise theorem enumeration would give a computable bound contradicting domination. <bookmark mark='d'/> A checked seven-thousand-nine-hundred-and-ten-state construction gives a published ZFC upper bound under the usual consistency assumptions. The smaller four-hundred-and-thirty-two-state 2025 claim is conditional on its construction checking out. The first unprovable value is unknown."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=3.0)
            for mk, ln in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
