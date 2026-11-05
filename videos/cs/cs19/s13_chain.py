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
            label(r"multiplying $p \times q$ by $q \times r$ costs $pqr$ scalar products; \ the result is the same "
                  r"in any order", font_size=21, color=GREY_A),
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
            "Matrix multiplication is associative, so a product of six matrices can be bracketed in any order "
            "with the same answer, but not the same cost. <bookmark mark='a'/> Multiplying p by q by q by r takes "
            "p q r scalar products. <bookmark mark='b'/> For these six, from the standard textbook example, "
            "multiplying left to right costs forty thousand five hundred products, and the worst of the forty-two "
            "possible orders costs fifty-eight thousand. <bookmark mark='c'/> The subproblems are the contiguous "
            "runs from i to j. For each, try every place for the last multiplication, and add the best costs of "
            "the two sides. <bookmark mark='d'/> This is the recurrence. <bookmark mark='e'/> The best order costs "
            "fifteen thousand one hundred and twenty-five, about a quarter of the worst. <bookmark mark='f'/> The "
            "table has n squared entries with n choices each: cubic time, where the number of orders grows "
            "exponentially. Compilers and query planners face the same problem, choosing the order of joins in "
            "Part 35's databases."
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
            label(r"so each range tries only a few roots: \ $O(n^3)$ becomes $O(n^2)$", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.45)
        tab.next_to(pts, DOWN, buff=0.4)
        last = d["bst"][-1]
        note_ = label(rf"at {last['n']} keys: \ {last['plain_iters'] / last['knuth_iters']:.0f}$\times$ fewer steps; "
                      r"\ the quadrangle inequality behind it speeds up many other DPs", font_size=20,
                      color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A cousin of this problem goes back to Part 17. <bookmark mark='a'/> Suppose we know how often each "
            "key will be looked up. Which binary search tree minimizes the expected search cost? Frequent keys "
            "should be near the root, but the tree must stay ordered. <bookmark mark='b'/> The recurrence has the "
            "same shape: for every range of keys, try every key as the root. Cubic time. <bookmark mark='c'/> In "
            "1971 Donald Knuth proved that the best root of a range never moves left when the range grows on the "
            "right, and never right when it grows on the left. <bookmark mark='d'/> So each range needs to try "
            "only the roots between two neighbours' answers, and the total falls to quadratic. <bookmark "
            "mark='e'/> At two hundred keys, the same answer in thirty-three times fewer steps. The inequality "
            "behind it, later called the quadrangle inequality, speeds up many other dynamic programmes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
