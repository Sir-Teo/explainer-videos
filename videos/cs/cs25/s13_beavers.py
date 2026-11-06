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
            label(r"why: \ an interpreter for a total language is itself total, \ but it can't be written in that "
                  r"language", font_size=21, color=LAM),
            label(r"if \texttt{interp} were in it, \ so is $d(x) = \texttt{interp}(x, x) + 1$; \ then $d(\ulcorner d "
                  r"\urcorner) = d(\ulcorner d \urcorner) + 1$ \ (Part 14)", font_size=20, color=GREY_A),
            label(r"the busy beaver outgrows even Ackermann: \ it outgrows \textbf{every} computable function",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Three speeds of growth. <bookmark mark='a'/> Programs whose loops have bounds fixed before they start, "
            "what logicians call primitive recursion, can compute two to the n, towers of twos, and any fixed "
            "stack of such things. <bookmark mark='b'/> Part 11 met Wilhelm Ackermann's function and promised to "
            "say why it matters. It is computable and always finishes, yet it eventually outgrows every function "
            "that bounded loops can compute. A of four, four is already a tower of twos with sixty-five thousand "
            "five hundred and thirty-six in the top exponent. <bookmark mark='c'/> The reason is the diagonal "
            "argument once more. A language in which every program finishes has an interpreter that always "
            "finishes too, but the interpreter cannot be written in that language. <bookmark mark='d'/> If it "
            "could, so could d of x, the interpreter run on x with input x, plus one. Run d on its own code and "
            "you get d of d equals d of d plus one. That is the argument Part 14 pointed to, for why the typed "
            "lambda calculus cannot interpret itself. <bookmark mark='e'/> And the third column outgrows even Ackermann. Part 1 "
            "stated that the busy beaver outgrows every computable function. Now the proof."
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
            region(3.0, 0.8, r"compute $f(2n)$ \ ($c$ states)", HEAD, font_size=20),
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
            "The proof is a machine built in three pieces. <bookmark mark='a'/> Take any computable function f, "
            "computed by a machine with c states. For each n, build a machine that first writes n on its tape, "
            "which takes n states; <bookmark mark='b'/> then computes f of two n, which takes c states; then counts "
            "that number down to zero, a few states more. <bookmark mark='c'/> It has n plus a constant states, and "
            "it halts after more than f of two n steps. <bookmark mark='d'/> So the busy beaver of n plus that "
            "constant is bigger than f of two n. <bookmark mark='e'/> Once n is larger than the constant, the busy "
            "beaver of two n is bigger still. The busy beaver passes f and stays ahead. <bookmark mark='f'/> No "
            "computable function can even bound it."
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
                [r"432 -- 7,910", r"the consistency of ZFC", r"Yedidia and Aaronson \ (2016) \ and after"]]
        tab = grid_table([r"states", r"the machine halts iff \ldots \ is false", r"by"], rows,
                         widths=[1.6, 6.6, 4.6], row_h=0.5, font_size=19, mono_cols=(),
                         colors=[[HEAD, WHITE, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.35).set_x(0)
        lines = VGroup(
            label(r"knowing $S(27)$ would settle Goldbach: \ run the machine $S(27)$ steps \ (in principle)",
                  font_size=21, color=YES),
            label(r"a sound theory $T$ proves the value of $S(n)$ for only finitely many $n$: \ a machine that "
                  r"searches $T$ for a contradiction has a fixed size", font_size=21, color=NO),
            label(r"where the line falls for ZFC, \ between 6 and 432, \ is unknown", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Part 1 told how the five-state value was proved, and why six may be out of reach. Here is the larger "
            "map. <bookmark mark='a'/> Many open problems are the halting of a single small machine. A fifteen-state "
            "machine, from Tristan Stérin and Damien Woods in 2021, halts exactly if Erdős was wrong that every "
            "power of two beyond the eighth has a digit two in base three. A twenty-seven-state machine, posted "
            "online in 2015 and not yet checked carefully, halts if Goldbach's conjecture fails. Seven hundred and "
            "forty-four states encode the Riemann hypothesis. <bookmark mark='b'/> So knowing the busy beaver of "
            "twenty-seven would settle Goldbach, at least in principle: run the machine that long. <bookmark "
            "mark='c'/> And some machine of a few hundred states halts only if set theory is inconsistent, so by "
            "chapter eight, set theory cannot prove its busy-beaver value. Any sound theory pins down only finitely "
            "many values. <bookmark mark='d'/> Somewhere between six and four hundred and thirty-two, set theory's "
            "knowledge stops. Where, exactly, nobody knows."
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
