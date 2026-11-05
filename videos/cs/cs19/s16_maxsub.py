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
            label(r"which contiguous stretch has the largest sum? \ (the empty case aside)", font_size=22,
                  color=GREY_A),
            label(r"1977: \ Ulf Grenander, \ finding the brightest rectangle in a digitized image; \ the 1-D case "
                  r"first", font_size=21, color=GREY_A),
            label(r"told in Jon Bentley's \textit{Programming Pearls} \ (1984), \ four algorithms in a week",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "To close the paradigms, one small problem solved four ways. <bookmark mark='a'/> Given a sequence of "
            "positive and negative numbers, which contiguous stretch has the largest sum? Here, the first six, "
            "adding to eighteen. <bookmark mark='b'/> Ulf Grenander at Brown University posed it in 1977, as a "
            "simplification of finding the brightest rectangle in a digitized picture. <bookmark mark='c'/> Jon "
            "Bentley told the story in his column Programming Pearls: within a short time it had four algorithms, "
            "each a different paradigm, and each asymptotically faster than the last."
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
            self.play(FadeIn(head))
            for mk, a_ in zip("abcd", algs):
                vo.wait_until(mk)
                self.play(FadeIn(a_))
            self.play(FadeIn(kad))
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
            label(r"dashes: \ not attempted; \ the cubic method on a million numbers would take centuries",
                  font_size=20, color=GREY_B),
            label(rf"a million numbers: \ Kadane {t(last['kadane'])}, \ divide and conquer {t(last['divide'])}",
                  font_size=22, color=YES),
            label(r"the algorithm, \ not the machine, \ sets what is possible", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Measured, the four separate like the curves of Part 16. <bookmark mark='a'/> The cubic method needs "
            "over half a second for four hundred numbers; on a million it would need centuries. <bookmark mark='b'/> "
            "The quadratic one takes five seconds for ten thousand. Divide and conquer handles a million numbers in "
            "six seconds, and Kadane's algorithm in under half a second. <bookmark mark='c'/> On the same machine, "
            "in the same language, the difference between the slowest and the fastest is not a constant factor. "
            "It is what can be done at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
