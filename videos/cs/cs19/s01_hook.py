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
        with self.voiceover(
            "Here are the first fifty digits of pi, and the last ten of the first million. <bookmark mark='a'/> "
            "They came from this series, found by the brothers David and Gregory Chudnovsky in 1988, which adds "
            "about fourteen correct digits per term. <bookmark mark='b'/> Seventy thousand terms, summed exactly "
            "with whole numbers in plain Python on this machine, took sixteen seconds. The sum is the easy part. "
            "The hard part is multiplying numbers a million digits long, again and again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines), FadeIn(dots), FadeIn(tail))
            vo.wait_until("a")
            self.play(FadeIn(series))
            vo.wait_until("b")
            self.play(FadeIn(t))
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
            [r"our FFT, \ the transform itself", r"$n \log n$", dur(core["fft_core_s"])],
        ]
        tab = grid_table([r"method", r"grows like", r"time"], rows, widths=[6.4, 2.0, 3.6], row_h=0.62, font_size=22,
                         mono_cols=(), colors=[[NO, NO, NO], [DATA, DATA, DATA], [LAM, LAM, LAM], [YES, YES, YES]])
        tab.next_to(head, DOWN, buff=0.6)
        note_ = label(r"the same answer four ways: \ three ideas, \ chapters 3, \ 5--7", font_size=22,
                      color=HEAD).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "So how long does it take to multiply two numbers of a million digits? <bookmark mark='a'/> The way "
            "we learned at school, every digit times every digit, is a trillion small products: measured on smaller "
            "numbers and projected, about twenty-seven hours in Python. <bookmark mark='b'/> Python's own integers "
            "take under a second, because they use a trick found by a Moscow student in 1960. <bookmark mark='c'/> "
            "Python's decimal module is four times faster again, with a transform over a finite field. <bookmark "
            "mark='d'/> And the fast Fourier transform, the heart of this part, does the multiplication itself "
            "in four hundredths of a second. <bookmark mark='e'/> Same numbers, same answer: the difference is "
            "the idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r), shift=RIGHT * 0.1))
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
            "Most good algorithms come from a handful of ideas, and this part names them. <bookmark mark='a'/> "
            "Greedy algorithms take the best-looking step each time; the work is in proving they never regret it, "
            "and knowing when they would. <bookmark mark='b'/> Divide and conquer splits a problem, solves the "
            "parts, and combines them; applied to the right points it gives the most important algorithm of the "
            "twentieth century. <bookmark mark='c'/> Dynamic programming solves every subproblem once, in an order where "
            "each answer is ready when it is needed. <bookmark mark='d'/> And when nothing cleverer is known, we "
            "search, trying choices and undoing them, as cleverly as possible."
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
