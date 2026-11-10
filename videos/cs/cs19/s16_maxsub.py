from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, words)


def t(s):
    if s is None:
        return r"---"
    return f"{s * 1e6:.0f} µs" if s < 1e-3 else (f"{s * 1000:.1f} ms" if s < 1 else f"{s:.2f} s")


class MaxSub(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.four()
        self.measured()

    def card(self):
        card = chapter_card(15, r"One problem, \ four paradigms", r"How fast can the best stretch be found?",
                            lit=(1984,), extra=((1977, r"Grenander's question"), (1984, r"Bentley's column")),
                            part=PART)
        with self.voiceover("Chapter fifteen. One problem, four paradigms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("maxsub")
        a = d["show"]
        i0, j0 = d["show_range"]
        head = label(r"The maximum subarray", font_size=34).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(Square(side_length=0.62, stroke_color=GREY_B, stroke_width=1.5,
                                       fill_color=YES if x > 0 else NO, fill_opacity=min(0.85, 0.1 + abs(x) / 11)),
                                mono(str(x), 17, WHITE)) for x in a]).arrange(RIGHT, buff=0.1).move_to(UP * 1.4)
        best = SurroundingRectangle(cells[i0:j0 + 1], color=HEAD, buff=0.08, stroke_width=3)
        lab = label(rf"best: \ {d['show_best']}", font_size=24, color=HEAD).next_to(best, DOWN, buff=0.2)
        pts = VGroup(
            label('nonempty contiguous stretch; all-negative input returns its largest element', font_size=22,
                  color=GREY_A),
            label(r"1977: \ Ulf Grenander, \ finding the brightest rectangle in a digitized image; \ the 1-D case "
                  r"first", font_size=21, color=GREY_A),
            label(r"told in Jon Bentley's \textit{Programming Pearls} \ (1984), \ four algorithms in a week",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Choose a nonempty contiguous subarray of maximum sum. <bookmark mark='a'/> The checked example "
            'highlights the first six values, totaling eighteen. Requiring nonempty matters: for an all-negative '
            "input the answer is the largest element, not zero. <bookmark mark='b'/> The problem arose in work on "
            "locating bright regions of digitized images. <bookmark mark='c'/> Bentley's Programming Pearls presents "
            'several algorithms for it. Comparing the same objective across these methods lets us see how reusing '
            'information changes the amount of work.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(Create(best), FadeIn(lab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def four(self):
        head = label(r"Four algorithms", font_size=34).to_edge(UP, buff=0.3)
        algs = VGroup(*[VGroup(label(a, font_size=23, color=c), label(b, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1) for a, b, c in (
            (r"\textbf{brute force}: \ $O(n^3)$", r"every pair $i \le j$, \ add up the stretch", NO),
            (r"\textbf{running sums}: \ $O(n^2)$", r"for each start, \ extend the end, \ keeping the sum", HEAD),
            (r"\textbf{divide and conquer}: \ $O(n \log n)$", r"best in the left half, \ in the right half, \ or "
                                                             r"crossing the middle: \ the crossing one in $O(n)$", DATA),
            (r"\textbf{dynamic programming} \ (Kadane): \ $O(n)$", r"best stretch ending at $i$ $=$ "
                                                                   r"$\max(a_i, \ \text{best ending at } i-1 + a_i)$",
             YES))]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        kad = code([
            "best = cur = a[0]",
            "for x in a[1:]:",
            "    cur = max(x, cur + x)",
            "    best = max(best, cur)",
        ], size=20).to_edge(RIGHT, buff=0.6).shift(DOWN * 1.6)
        values=load("maxsub")["show"][:6]
        current=[];best=[]
        for value in values:
            current.append(value if not current else max(value,current[-1]+value))
            best.append(current[-1] if not best else max(best[-1],current[-1]))
        trace=grid_table(["state"]+[str(v) for v in values],
                         [["ending here"]+[str(v) for v in current],["best so far"]+[str(v) for v in best]],
                         widths=[1.9]+[.58]*6,row_h=.44,font_size=17,mono_cols=()).move_to([3.5,1.3,0])
        negative=MathTex(r"[-5,-2,-7]\quad\longrightarrow\quad -2",font_size=24,color=HEAD).next_to(kad,DOWN,buff=.35)
        with self.voiceover(
            "The four. <bookmark mark='a'/> Brute force tries every start and every end, and adds up each stretch: "
            "cubic. <bookmark mark='b'/> Keeping a running sum while the end moves avoids re-adding: quadratic. "
            "<bookmark mark='c'/> Divide and conquer, Michael Shamos's: the best stretch lies in the left half, in "
            "the right half, or across the middle, and the best crossing one is found by scanning outwards in "
            "linear time. n log n, the recurrence of the closest pair. <bookmark mark='d'/> And dynamic "
            "programming, found by the statistician Jay Kadane, as Bentley tells it, within a minute of hearing "
            "the problem at a seminar: the best stretch ending at each position is either the number there alone, "
            "or the best stretch ending one earlier, extended. One pass, four lines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(trace), FadeIn(algs[0]))
            for mk, a_ in zip("abcd", algs):
                vo.wait_until(mk)
                self.play(Indicate(a_, color=NO) if mk == "a" else FadeIn(a_))
            self.play(FadeIn(kad), Indicate(trace, color=YES), FadeIn(negative))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("maxsub")
        head = label(r"Measured on this machine", font_size=34).to_edge(UP, buff=0.3)
        rows = [[f"{r['n']:,}", t(r.get("cubic")), t(r.get("quadratic")), t(r.get("divide")), t(r.get("kadane"))]
                for r in d["rows"]]
        tab = grid_table([r"$n$", r"$n^3$", r"$n^2$", r"$n \log n$", r"$n$"], rows, widths=[2.2, 2.2, 2.2, 2.2, 2.2],
                         row_h=0.44, font_size=20, colors=[[WHITE, NO, HEAD, DATA, YES]] * len(rows)).next_to(
            head, DOWN, buff=0.45)
        last = d["rows"][-1]
        pts = VGroup(
            label('dashes: unexecuted; million-element cubic growth is a model projection',
                  font_size=20, color=GREY_B),
            label(rf"a million numbers: \ Kadane {t(last['kadane'])}, \ divide and conquer {t(last['divide'])}",
                  font_size=22, color=YES),
            label('same arrays at each size; independent prefix-minimum checks outside every timer', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "All executed methods use the same array at a given size. <bookmark mark='a'/> Cubic runs stop at four "
            'hundred elements; the million-element cubic number is an unexecuted growth-model projection, not a '
            "runtime measurement. <bookmark mark='b'/> Quadratic, divide-and-conquer and Kadane runs stop at the "
            'limits shown. Every timed answer agrees with a separate prefix-minimum formulation, checked after the '
            "stopwatch stops. Raw repeats and minima are recorded. <bookmark mark='c'/> The measured gaps depend on "
            'this implementation and host. The asymptotic difference follows from their work, not from fitting a few '
            'timing rows or assigning a hardware cause.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
