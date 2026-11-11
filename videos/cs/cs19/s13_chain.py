from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Chain(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.bst()

    def card(self):
        card = chapter_card(12, r"Matrix chains and optimal search trees", r"Where do the brackets go?",
                            lit=(1971,), extra=((1971, r"Knuth's speedup"),), part=PART)
        with self.voiceover("Chapter twelve. Matrix chains and optimal search trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def chain(self):
        d = load("chain")
        dims = d["dims"]
        head = label(r"The order of multiplication", font_size=34).to_edge(UP, buff=0.3)
        mats = VGroup()
        for k in range(len(dims) - 1):
            r, c = dims[k], dims[k + 1]
            box = Rectangle(width=c / 22, height=r / 22, stroke_color=DATA, stroke_width=2, fill_color=DATA,
                            fill_opacity=0.25)
            mats.add(VGroup(box, MathTex(rf"A_{k + 1}", font_size=24).move_to(box),
                            label(rf"${r} \times {c}$", font_size=15, color=GREY_B).next_to(box, DOWN, buff=0.1)))
        mats.arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label('classical $p\\times q$ by $q\\times r$: $pqr$ scalar products; associativity is exact-arithmetic', font_size=21, color=GREY_A),
            label(rf"left to right: \ {d['left_to_right']:,}; \ worst of the {d['catalan']} orders: \ "
                  rf"{d['worst']:,}", font_size=22, color=NO),
            label(r"subproblem: \ the best cost for $A_i \cdots A_j$, \ choosing the last split $k$:", font_size=21,
                  color=GREY_A),
            MathTex(r"C(i, j) = \min_{i \le k < j} C(i, k) + C(k+1, j) + d_{i-1} d_k d_j", font_size=30, color=LAM),
            label(rf"best: \ {d['best']:,}, \ as $\texttt{{{d['brackets']}}}$", font_size=23, color=YES),
            label(r"$O(n^2)$ subproblems, \ $O(n)$ splits each: \ $O(n^3)$; \ the number of orders grows like "
                  r"$4^n$", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Matrix multiplication is associative in exact arithmetic, but parenthesization changes the scalar work. <bookmark mark='a'/> A p-by-q matrix times a q-by-r matrix uses p q r scalar multiplications in the classical algorithm. <bookmark mark='b'/> For these six matrices, left-to-right costs forty thousand five hundred, and the worst of forty-two bracketings costs fifty-eight thousand. <bookmark mark='c'/> For each contiguous range, choose its final split and add the best left and right costs plus the final product cost. <bookmark mark='d'/> The recurrence enumerates these last-split choices. <bookmark mark='e'/> The optimum is fifteen thousand one hundred and twenty-five, with the bracketing shown. <bookmark mark='f'/> There are quadratically many ranges and at most linearly many splits each. Floating evaluation can also change rounding, and query-planning costs need richer models than this matrix example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mats))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def bst(self):
        d = load("chain")
        head = label(r"Optimal search trees, \ and Knuth's speedup", font_size=34).to_edge(UP, buff=0.3)
        rows = [[str(r["n"]), f"{r['plain_iters']:,}", f"{r['knuth_iters']:,}",
                 f"{r['plain_s'] * 1000:.1f} ms", f"{r['knuth_s'] * 1000:.1f} ms"] for r in d["bst"]]
        tab = grid_table([r"keys", r"steps, \ plain", r"steps, \ Knuth", r"time, \ plain", r"time, \ Knuth"], rows,
                         widths=[1.4, 2.6, 2.6, 2.2, 2.2], row_h=0.46, font_size=20,
                         colors=[[WHITE, NO, YES, NO, YES]] * len(rows))
        pts = VGroup(
            label(r"keys searched with known frequencies: \ which binary search tree minimizes the expected cost?",
                  font_size=21, color=GREY_A),
            label(r"the same shape of recurrence: \ choose the root $r$ of each range $i..j$", font_size=21,
                  color=GREY_A),
            label(r"Knuth \ (1971): \ the best root moves monotonically: \ $R(i, j-1) \le R(i, j) \le R(i+1, j)$",
                  font_size=21, color=HEAD),
            label('nonnegative probabilities + root monotonicity: quadratic total root trials', font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.45)
        tab.next_to(pts, DOWN, buff=0.4)
        last = d["bst"][-1]
        note_ = label(rf"at {last['n']} keys: \ {last['plain_iters'] / last['knuth_iters']:.0f}$\times$ fewer steps; "
                      r"\ the quadrangle inequality behind it speeds up many other DPs", font_size=20,
                      color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here we model successful searches for ordered keys with nonnegative probabilities. <bookmark mark='a'/> "
            'We seek a binary search tree of minimum expected search depth; the key order must remain intact. '
            "<bookmark mark='b'/> The direct recurrence tries every root for every interval and sums the interval's "
            "probability mass. <bookmark mark='c'/> With the required monotonicity conditions and a consistent tie "
            "convention, optimal roots lie between the roots of neighboring intervals. <bookmark mark='d'/> Knuth's "
            'restricted ranges give quadratic total root trials, not a constant number for every interval. Both '
            "implementations are checked for equal costs. <bookmark mark='e'/> The table shows actual root-trial "
            "counts and separate timings. This optimization requires proof of the recurrence's structure; it does not"
            ' apply to arbitrary dynamic programs.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
