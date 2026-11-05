from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def heap_tree(vals, dy=0.85, dx0=3.2, font_size=18, color=DATA):
    nodes = []
    edges = VGroup()
    for i, v in enumerate(vals):
        depth = (i + 1).bit_length() - 1
        pos_in = i - (2 ** depth - 1)
        width = 2 ** depth
        x = (pos_in - (width - 1) / 2) * (dx0 * 2 / width)
        y = -depth * dy
        c = VGroup(Circle(radius=0.28, color=color, stroke_width=2).set_fill(BG, 1), mono(str(v), font_size, WHITE))
        c[1].move_to(c[0])
        c.move_to([x, y, 0])
        nodes.append(c)
        if i > 0:
            p = nodes[(i - 1) // 2]
            edges.add(Line(p.get_center(), c.get_center(), buff=0.28, color=GREY_B, stroke_width=1.6))
    return VGroup(edges, VGroup(*nodes))


class Heap(VoiceoverScene):
    def construct(self):
        self.card()
        self.shape()
        self.heapify()
        self.sort()

    def card(self):
        card = chapter_card(7, r"Heapsort", r"Can a tree live in an array?", lit=(1964,),
                            extra=((1964, r"Williams: \ heapsort; \ Floyd: \ heapify"),), part=PART)
        with self.voiceover("Chapter seven. Heapsort."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shape(self):
        head = label(r"A heap: \ a tree stored in an array", font_size=34).to_edge(UP, buff=0.3)
        vals = [9, 7, 8, 3, 5, 6, 2, 1, 4, 0]
        t = heap_tree(vals).move_to(LEFT * 2.6 + UP * 0.4)
        arr = VGroup(*[VGroup(Rectangle(width=0.55, height=0.45, color=GREY_B, stroke_width=1.5),
                              mono(str(v), 16, WHITE)) for v in vals])
        for a in arr:
            a[1].move_to(a[0])
        arr.arrange(RIGHT, buff=0).to_edge(DOWN, buff=1.4)
        idx = VGroup(*[mono(str(k), 12, GREY_B).next_to(a, DOWN, buff=0.06) for k, a in enumerate(arr)])
        pts = VGroup(
            label(r"children of position $i$: \ $2i+1$ and $2i+2$; \ parent: \ $\lfloor (i-1)/2 \rfloor$",
                  font_size=21, color=GREY_A),
            label(r"\textbf{heap order}: \ every parent is at least as large as its children", font_size=21,
                  color=YES),
            label(r"so the maximum is at the root; \ the height is $\lfloor \lg n \rfloor$", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
        if pts.width > 5.8:
            pts.scale_to_fit_width(5.8)
        with self.voiceover(
            "J. W. J. Williams invented heapsort in 1964 around a data structure that is also his: the heap. "
            "<bookmark mark='a'/> A heap is a binary tree with no pointers. Its nodes are stored in an array, level "
            "by level, so the children of position i are at two i plus one and two i plus two. <bookmark "
            "mark='b'/> It is kept in heap order: every parent is at least as large as its children. <bookmark "
            "mark='c'/> So the largest element is always at the root, and because the tree is complete, its height "
            "is the logarithm of n."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t), FadeIn(arr), FadeIn(idx))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), Indicate(t[1][0], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def heapify(self):
        d = load("heap")
        head = label(r"Building a heap in linear time \ (Floyd, \ 1964)", font_size=32).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"sift each node down, \ from the last parent back to the root", font_size=22, color=GREY_A),
            label(r"a node at height $h$ costs at most $2h$ comparisons; \ there are about $n / 2^{h+1}$ of them",
                  font_size=22, color=GREY_A),
            MathTex(r"\sum_{h \ge 0} \frac{n}{2^{h+1}}\, 2h \;=\; n \sum_{h \ge 1} \frac{h}{2^h} \;=\; 2n",
                    font_size=36, color=YES),
            label(r"most nodes are near the bottom, \ where sifting is cheap", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.45)
        rows = [[words(r["n"]), words(r["build"]), f"{r['build'] / r['n']:.2f}"] for r in d["rows"]]
        tab = grid_table([r"$n$", r"comparisons to build", r"per element"], rows, widths=[2.2, 3.6, 2.4],
                         row_h=0.4, font_size=19).next_to(steps, DOWN, buff=0.35)
        with self.voiceover(
            "Inserting n elements one by one would build a heap in n log n. Robert Floyd found a better way. "
            "<bookmark mark='a'/> Treat the array as a heap that is wrong everywhere, and fix it from the bottom "
            "up: sift each parent down until it is larger than its children. <bookmark mark='b'/> A node at height "
            "h costs at most two h comparisons, and only about n over two to the h plus one nodes have that height. "
            "<bookmark mark='c'/> The sum of h over two to the h converges to two, so the whole build costs at most "
            "two n comparisons: linear. Most nodes are near the bottom, where sifting is cheap. <bookmark "
            "mark='d'/> Measured, it costs under two comparisons per element at every size."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(Write(steps[2]), FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def sort(self):
        d = load("heap")
        r = d["rows"][-1]
        head = label(r"Heapsort", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"swap the root, \ the maximum, \ to the end; \ the heap shrinks by one; \ sift the new root down",
                  font_size=22, color=GREY_A),
            label(r"$n - 1$ times, \ each at most $2 \lg n$ comparisons: \ $O(n \log n)$ in the \textit{worst} case",
                  font_size=22, color=YES),
            label(rf"measured, \ $n = {words(r['n'])}$: \ {words(r['total'])} comparisons, \ about "
                  rf"{r['total'] / r['nlgn']:.2f} $n \lg n$", font_size=22, color=GREY_A),
            label(r"in place, \ no extra memory; \ not stable; \ poor cache behaviour: \ the parent and its children "
                  r"are far apart", font_size=21, color=GREY_A),
            label(r"libraries keep it as the safety net: \ introsort switches to heapsort if quicksort goes badly",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "With the heap built, sorting is a loop. <bookmark mark='a'/> The maximum is at the root. Swap it to "
            "the end of the array, shrink the heap by one, and sift the new root down to restore order. <bookmark "
            "mark='b'/> Each of the n minus one rounds costs at most two log n comparisons, so heapsort is n log n "
            "even in the worst case. <bookmark mark='c'/> Measured on sixty-five thousand elements, it makes about "
            "one point eight times n log n comparisons, nearly twice merge sort. <bookmark mark='d'/> Its virtues "
            "are elsewhere. It needs no extra memory, and its worst case is guaranteed. Its weakness is the memory "
            "hierarchy: a parent and its children sit far apart in the array, so it misses the cache. <bookmark "
            "mark='e'/> That is why libraries keep it as a safety net. Introsort, used in C++'s standard library, "
            "runs quicksort, and switches to heapsort if the recursion gets too deep."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
