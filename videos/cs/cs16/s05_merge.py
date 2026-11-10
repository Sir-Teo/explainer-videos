from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, words)


class Merge(VoiceoverScene):
    def construct(self):
        self.card()
        self.merging()
        self.tree()
        self.substitution()

    def card(self):
        card = chapter_card(4, r"Merge sort and the recursion tree", r"What does dividing buy?", lit=(1945,),
                            extra=((1945, r"von Neumann's merge sort"),), part=PART)
        with self.voiceover("Chapter four. Merge sort and the recursion tree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def merging(self):
        head = label(r"Merging two sorted lists", font_size=34).to_edge(UP, buff=0.3)
        A, B = [1, 4, 7, 9], [2, 3, 8, 10]

        def row(vals, color, y):
            g = VGroup(*[VGroup(Rectangle(width=0.7, height=0.55, color=color, stroke_width=2).set_fill(color, 0.1),
                                mono(str(v), 20, WHITE)) for v in vals])
            for c in g:
                c[1].move_to(c[0])
            return g.arrange(RIGHT, buff=0.1).move_to([0, y, 0])
        ra, rb = row(A, DATA, 1.6), row(B, LAM, 0.6)
        ra.shift(LEFT * 2.6)
        rb.shift(LEFT * 2.6)
        out_slots = VGroup(*[Rectangle(width=0.7, height=0.55, color=GREY_D, stroke_width=1.5) for _ in range(8)]).arrange(
            RIGHT, buff=0.1).move_to(DOWN * 1.0)
        la, lb = label(r"left", font_size=19, color=DATA).next_to(ra, LEFT, buff=0.3), label(
            r"right", font_size=19, color=LAM).next_to(rb, LEFT, buff=0.3)
        lo = label(r"output", font_size=19, color=GREY_B).next_to(out_slots, LEFT, buff=0.3)
        pa = Triangle(color=HEAD, fill_opacity=1).scale(0.12).rotate(PI).next_to(ra[0], UP, buff=0.08)
        pb = Triangle(color=HEAD, fill_opacity=1).scale(0.12).next_to(rb[0], DOWN, buff=0.08)
        pts = VGroup(
            label(r"compare the two front elements; \ move the smaller to the output; \ advance", font_size=22,
                  color=GREY_A),
            label(r"each comparison places one element: \ at most $n - 1$ comparisons for $n$ elements", font_size=22,
                  color=YES),
            label(r"take from the left on ties, \ and equal keys keep their order: \ merge sort is \textbf{stable}",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Everything in merge sort rests on one operation. <bookmark mark='a'/> Two lists, each already sorted. "
            "Look at the front of each, move the smaller one to the output, and advance in that list. <bookmark "
            "mark='b'/> Repeat until one list runs out, then copy the rest of the other. Each comparison places one "
            "element, so merging n elements takes at most n minus one comparisons. <bookmark mark='c'/> And if we "
            "take from the left list whenever the fronts are equal, equal keys keep their original order. That "
            "makes merge sort stable, which the Job will rely on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ra), FadeIn(rb), FadeIn(out_slots), FadeIn(la), FadeIn(lb), FadeIn(lo))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pb), FadeIn(pts[0]))
            vo.wait_until("b")
            i = j = 0
            for o in range(8):
                if j >= len(B) or (i < len(A) and A[i] <= B[j]):
                    src, i = ra[i], i + 1
                    mv = [pa.animate.next_to(ra[min(i, 3)], UP, buff=0.08)] if i < len(A) else [FadeOut(pa)]
                else:
                    src, j = rb[j], j + 1
                    mv = [pb.animate.next_to(rb[min(j, 3)], DOWN, buff=0.08)] if j < len(B) else [FadeOut(pb)]
                self.play(src.animate.move_to(out_slots[o]), *mv, run_time=0.5)
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def tree(self):
        head = label(r"The recursion tree of $T(n) = 2T(n/2) + n$", font_size=32).to_edge(UP, buff=0.3)
        n = 16
        levels = 5
        boxes = VGroup()
        sums = VGroup()
        W = 9.6
        for d in range(levels):
            k = 2 ** d
            size = n // k
            w = W / k
            row = VGroup()
            for j in range(k):
                r = Rectangle(width=w - 0.08, height=0.5, stroke_color=DATA, stroke_width=1.6).set_fill(DATA, 0.12)
                r.move_to([-W / 2 + w / 2 + j * w - 1.2, 2.0 - d * 0.95, 0])
                t = mono(str(size), 14 if k < 16 else 11, WHITE).move_to(r)
                row.add(VGroup(r, t))
            boxes.add(row)
            s = MathTex(rf"{k} \times {size} = {n}", font_size=26, color=YES).move_to([W / 2 - 0.4, 2.0 - d * 0.95, 0])
            sums.add(s)
        brace = BraceBetweenPoints([5.25, 2.25, 0], [5.25, -2.05, 0],
                                   direction=RIGHT, color=GREY_B)
        bl = MathTex(r"\substack{\lg n + 1\\\text{levels}}", font_size=18, color=GREY_B).next_to(brace, RIGHT, buff=0.12)
        tot = MathTex(r"T(n) = n \lg n + n \quad(n=2^h,\ T(1)=1)", font_size=30, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Merge sort splits, sorts each half, then merges. We will draw a simple work recurrence, with n a "
            "power of two and base cost T of one equal to one. <bookmark mark='a'/> The root pays n for "
            "combining. <bookmark mark='b'/> At each internal level the subproblem sizes sum to n, so the level "
            "pays n again. <bookmark mark='c'/> There are log base two n internal levels, plus n leaves of unit "
            "cost. <bookmark mark='d'/> The sum is n log n plus n. This is the chosen toll model; the exact "
            "number of key comparisons is a different count, measured next."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]), FadeIn(sums[0]))
            vo.wait_until("a")
            self.play(Indicate(boxes[0], color=DATA), Indicate(sums[0], color=YES))
            vo.wait_until("b")
            for d in range(1, levels):
                self.play(FadeIn(boxes[d]), FadeIn(sums[d]), run_time=0.7)
            vo.wait_until("c")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("d")
            self.play(Write(tot))
        self.wait(0.3)
        self.clear_scene()

    def substitution(self):
        d = load("merge")
        head = label(r"Proving it, \ and measuring it", font_size=34).to_edge(UP, buff=0.3)
        proof = VGroup(
            label(r"include the base: \ guess $T(n) \le c\, n \lg n+n$, \ with $T(1)=1$",
                  font_size=22, color=GREY_A),
            MathTex(r"T(n) \le 2\left(c\,\tfrac{n}{2} \lg \tfrac{n}{2}+\tfrac n2\right)+n = c n\lg n-cn+2n \le c n\lg n+n "
                    r"\quad \text{when } c \ge 1", font_size=30),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[words(r["n"]), words(r["cmp"]), words(r["worst"]), words(r["nlgn"]), words(lb)]
                for r, lb in zip(d["rows"], d["lower"]) if r["n"] in (16, 256, 4096, 65536)]
        tab = grid_table([r"$n$", r"comparisons, \ random", r"worst case", r"$n \lg n$", r"$\lceil \lg n! \rceil$"],
                         rows, widths=[1.8, 2.8, 2.2, 2.2, 2.2], row_h=0.46, font_size=19).next_to(proof, DOWN,
                                                                                               buff=0.45)
        pts = label(r"worst case: $n\lg n-n+1$; \ gap to the information bound is $O(n)$, ratio tends to one", font_size=21, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "A guessed bound also needs a base case. <bookmark mark='a'/> For this recurrence use c n log n plus "
            "n, which covers T of one equal to one. Substitute the bound into the two half-size calls: the extra "
            "linear terms leave the inequality true when c is at least one. <bookmark mark='b'/> Our measured "
            "sort counts key comparisons instead of charging n at every merge. For powers of two its worst case "
            "is exactly n log n minus n plus one. <bookmark mark='c'/> Compare that with the information lower "
            "bound in the last column. The gap is linear in n, so the ratio approaches one as n grows."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(proof))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
