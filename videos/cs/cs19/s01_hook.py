from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def dur(s):
    if s >= 3600:
        return rf"{s / 3600:.0f} hours"
    if s >= 1:
        return rf"{s:.2f} s"
    return rf"{s * 1000:.1f} ms"


class Hook(VoiceoverScene):
    def construct(self):
        self.million()
        self.multiply()
        self.ideas()
        self.plan()

    def million(self):
        d = load("pi")
        head = label(r"A million digits of $\pi$", font_size=36).to_edge(UP, buff=0.35)
        digits = d["head"]
        lines = VGroup(*[mono(digits[i:i + 26], 26, DATA) for i in range(0, 52, 26)]).arrange(DOWN, buff=0.12)
        dots = mono("...", 26, GREY_B)
        tail = mono("..." + d["tail"], 26, HEAD)
        VGroup(lines, dots, tail).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        series = MathTex(r"\frac{1}{\pi} = 12 \sum_{k=0}^{\infty} \frac{(-1)^k (6k)!\,(13591409 + 545140134\,k)}"
                         r"{(3k)!\,(k!)^3\,640320^{3k + 3/2}}", font_size=30, color=GREY_A).to_edge(DOWN, buff=1.5)
        t = label(rf"the Chudnovskys' series \ (1988), \ in Python, \ on this machine: \ {d['seconds']:.0f} seconds",
                  font_size=22, color=YES).next_to(series, DOWN, buff=0.3)
        certificate = VGroup(
            MathTex(r"L \le \pi\,10^D \le U,\qquad \lfloor L\rfloor=\lfloor U\rfloor",font_size=27,color=HEAD),
            label("series bound + integer square-root bound + guard digits",font_size=19,color=GREY_A),
        ).arrange(DOWN,buff=.12).to_edge(DOWN,buff=.22)
        with self.voiceover(
            "Here are leading digits of pi, and the final ten after one million decimal places. <bookmark mark='a'/> "
            "The Chudnovsky brothers' series adds roughly fourteen digits per term. Our binary splitting sums "
            "rational terms with exact integers. <bookmark mark='b'/> A finite sum and an integer square root still "
            'need error bounds. We bracket the infinite series between adjacent alternating partial sums, bracket the'
            ' square root, and keep guard digits until both bounds give the same truncated integer. The displayed '
            'time covers that certified calculation; decimal conversion is separate.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines), FadeIn(dots), FadeIn(tail))
            vo.wait_until("a")
            self.play(FadeIn(series))
            vo.wait_until("b")
            self.play(FadeIn(t),FadeIn(certificate))
        self.wait(0.3)
        self.clear_scene()

    def multiply(self):
        d = load("pi")
        c = load("fftcore")
        head = label(r"Two million-digit numbers, \ multiplied", font_size=36).to_edge(UP, buff=0.35)
        last = d["rows"][-1]
        core = next(r for r in c["rows"] if r["digits"] == 1_000_000)
        rows = [
            [r"grade school, \ digit by digit", r"$n^2$", rf"about {d['school_1m_s'] / 3600:.0f} hours \ (projected)"],
            [r"Python's integers: \ Karatsuba", r"$n^{1.58}$", dur(last["python_int_s"])],
            [r"Python's \texttt{decimal}: \ a number-theoretic transform", r"$n \log n$", dur(last["decimal_s"])],
            [r"floating FFT: conversion, round, carry", r"$n \log n$ arithmetic", dur(last["fft_s"])],
        ]
        tab = grid_table([r"method", r"grows like", r"time"], rows, widths=[6.4, 2.0, 3.6], row_h=0.62, font_size=22,
                         mono_cols=(), colors=[[NO, NO, NO], [DATA, DATA, DATA], [LAM, LAM, LAM], [YES, YES, YES]])
        tab.next_to(head, DOWN, buff=0.6)
        note_ = label('complete products above; school row is an unexecuted model projection', font_size=22,
                      color=HEAD).next_to(tab, DOWN, buff=0.5)
        core_panel = VGroup(
            label("separate FFT core",font_size=22,color=YES),
            mono(dur(core["fft_core_s"]),22,YES),
            label("different arrays; conversion and carry excluded",font_size=21,color=GREY_A),
        ).arrange(DOWN,buff=.12).next_to(note_,DOWN,buff=.35)
        core_frame = SurroundingRectangle(core_panel,buff=.18,color=YES,stroke_width=1.2)
        with self.voiceover(
            "Compare the work carefully. <bookmark mark='a'/> Grade-school digit convolution has quadratic growth; "
            "this million-digit time is an unexecuted projection from smaller tests. <bookmark mark='b'/> Python's "
            'integer row is a complete multiplication of two fixed million-digit operands, already converted to '
            "integers. <bookmark mark='c'/> The decimal row uses the same values with preconverted decimal operands; "
            "every product is checked exactly outside the timer. <bookmark mark='d'/> The separate FFT-core row times"
            ' convolution and rounding on different digit arrays. It excludes conversion and carry, so it is not an '
            "end-to-end speed comparison. <bookmark mark='e'/> Algorithm, representation and timing boundary all "
            'matter. Chapters three and seven separate them.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r), shift=RIGHT * 0.1))
                if mk == "d": self.play(FadeIn(core_panel),Create(core_frame))
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def ideas(self):
        head = label(r"A handful of ideas", font_size=38).to_edge(UP, buff=0.4)
        rows = VGroup(*[VGroup(label(a, font_size=30, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.12) for a, b, c in (
            (r"\textbf{greedy}", r"take the best-looking step, \ and prove you never regret it", YES),
            (r"\textbf{divide and conquer}", r"split, \ solve the parts, \ combine: \ Karatsuba, \ Strassen, \ the "
                                             r"FFT", DATA),
            (r"\textbf{dynamic programming}", r"solve every subproblem once, \ in the right order", LAM),
            (r"\textbf{search}", r"try, \ and undo what fails, \ cleverly", CTRL))]).arrange(DOWN, buff=0.45)
        rows.next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Several ideas organize this part. <bookmark mark='a'/> Greedy chooses the best-looking next step; an "
            "exchange proof tells us when that choice is safe. <bookmark mark='b'/> Divide and conquer splits a "
            'problem, solves smaller pieces and combines their answers. The right decomposition gives Karatsuba, '
            "Strassen and the FFT. <bookmark mark='c'/> Dynamic programming reuses subproblem answers in a valid "
            "dependency order. <bookmark mark='d'/> Search explores choices and restores state when it backtracks. We"
            ' will compare their mathematics, actual work and measured implementations.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ The Great Paradigms", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"greedy algorithms, \ exchange arguments, \ and matroids",
            r"Karatsuba and Strassen: \ fewer products, \ by algebra",
            r"the fast Fourier transform, \ derived, \ and what it multiplies",
            r"dynamic programming: \ edit distance, \ knapsack, \ chains, \ trees",
            r"backtracking and Dancing Links; \ one problem solved four ways",
            r"the frontier: \ the exponent of matrix multiplication, \ and why edit distance seems quadratic",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 19 of Computer Science, Built: The Great Paradigms. <bookmark mark='a'/> In this part: greedy "
            "algorithms and when they are right; multiplying numbers and matrices with fewer products; the fast "
            "Fourier transform, from scratch; dynamic programming in five settings; search, from the eight queens "
            "to Sudoku; one problem solved four ways; and the open questions about how fast we can multiply."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
