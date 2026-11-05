from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, value_bars, words)


class Quick(VoiceoverScene):
    def construct(self):
        self.card()
        self.partition()
        self.hoare()
        self.analysis()
        self.measured()
        self.pivots()

    def card(self):
        card = chapter_card(8, r"Quicksort, \ and $2n \ln n$", r"How can a random choice give a sure answer?",
                            lit=(1961,), extra=((1961, r"Hoare: \ Quicksort"),), part=PART)
        with self.voiceover("Chapter eight. Quicksort, and two n natural log n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def partition(self):
        head = label(r"Partition around a pivot \ (Hoare, \ 1961)", font_size=32).to_edge(UP, buff=0.3)
        vals = [6, 2, 9, 4, 7, 1, 8, 3, 5]
        bars = value_bars(vals, width=0.6, gap=0.15, scale=0.27).move_to(UP * 1.5)
        pivot = 5
        after = [v for v in vals if v < pivot] + [pivot] + [v for v in vals if v > pivot]
        bars2 = value_bars(after, width=0.6, gap=0.15, scale=0.27).move_to(DOWN * 1.25)
        for k, v in enumerate(after):
            bars2.bars[k].set_fill(YES if v < pivot else (HEAD if v == pivot else CTRL), 0.85)
        nsmall = sum(v < pivot for v in vals)
        lab = VGroup(label(r"smaller than the pivot", font_size=19, color=YES),
                     label(r"larger", font_size=19, color=CTRL))
        for g, part in ((lab[0], bars2.bars[:nsmall]), (lab[1], bars2.bars[nsmall + 1:])):
            g.next_to(bars2, DOWN, buff=0.2).set_x(VGroup(*part).get_x())
        pts = label(r"one pass, \ $n - 1$ comparisons; \ then sort each side \ --- \ the pivot is already home",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Tony Hoare invented quicksort in 1959, as a visiting student in Moscow, and published it in 1961. "
            "<bookmark mark='a'/> Pick one element, the pivot. <bookmark mark='b'/> In one pass, compare every "
            "other element with it, moving the smaller ones to its left and the larger ones to its right. That "
            "costs n minus one comparisons, and afterwards the pivot is in its final place. <bookmark mark='c'/> "
            "Then sort the two sides the same way. Unlike merge sort, the work happens before the recursion, and "
            "there is nothing to combine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars))
            vo.wait_until("a")
            self.play(bars.bars[vals.index(pivot)].animate.set_fill(HEAD, 1))
            vo.wait_until("b")
            self.play(TransformFromCopy(bars, bars2), run_time=1.5)
            self.play(FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def hoare(self):
        head = label(r"Partitioning in place: \ two pointers", font_size=34).to_edge(UP, buff=0.3)
        vals = [5, 2, 9, 4, 7, 1, 8, 3, 6]
        p = vals[0]

        def cells(vs):
            g = VGroup(*[VGroup(Rectangle(width=0.7, height=0.6, color=GREY_B, stroke_width=1.6),
                                mono(str(v), 22, WHITE)) for v in vs])
            for c in g:
                c[1].move_to(c[0])
            return g.arrange(RIGHT, buff=0.08).move_to(UP * 0.6)
        arr = cells(vals)
        arr[0][0].set_fill(HEAD, 0.25)
        pl = label(rf"pivot {p}", font_size=20, color=HEAD).next_to(arr[0], UP, buff=0.15)
        # Hoare's scheme: i from the left looks for >= p, j from the right for <= p, swap; stop when they cross
        a = list(vals)
        i, j = -1, len(a)
        frames = []
        while True:
            i += 1
            while a[i] < p:
                i += 1
            j -= 1
            while a[j] > p:
                j -= 1
            if i >= j:
                frames.append(("cross", i, j, list(a)))
                break
            a[i], a[j] = a[j], a[i]
            frames.append(("swap", i, j, list(a)))
        ip = Triangle(color=YES, fill_opacity=1).scale(0.13).rotate(PI)
        jp = Triangle(color=CTRL, fill_opacity=1).scale(0.13)
        il = label(r"$i$", font_size=20, color=YES)
        jl = label(r"$j$", font_size=20, color=CTRL)
        pts = VGroup(
            label(r"$i$ moves right past elements smaller than the pivot; \ $j$ moves left past larger ones",
                  font_size=21, color=GREY_A),
            label(r"when both stop, \ swap: \ each swap fixes two misplaced elements at once", font_size=21,
                  color=YES),
            label(r"when they cross, \ everything left of $j$ is $\le$ the pivot, \ everything right of it is "
                  r"$\ge$: \ no extra memory", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Hoare's own partition needs no second array. <bookmark mark='a'/> Take the first element as the pivot. "
            "One pointer, i, starts at the left and moves right past elements smaller than the pivot; another, j, "
            "starts at the right and moves left past larger ones. <bookmark mark='b'/> When both have stopped, each "
            "is pointing at an element on the wrong side, so swap them, and continue. <bookmark mark='c'/> When the "
            "pointers cross, everything up to j is at most the pivot and everything after it is at least the "
            "pivot. It uses no extra memory and makes few swaps, which is part of why quicksort is fast in "
            "practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(arr), FadeIn(pl))
            vo.wait_until("a")
            ip.next_to(arr[0], DOWN, buff=0.1)
            jp.next_to(arr[-1], DOWN, buff=0.1)
            il.next_to(ip, DOWN, buff=0.05)
            jl.next_to(jp, DOWN, buff=0.05)
            self.play(FadeIn(ip), FadeIn(jp), FadeIn(il), FadeIn(jl), FadeIn(pts[0]))
            vo.wait_until("b")
            for kind, fi, fj, state in frames:
                self.play(ip.animate.next_to(arr[min(fi, len(vals) - 1)], DOWN, buff=0.1),
                          jp.animate.next_to(arr[max(fj, 0)], DOWN, buff=0.1),
                          il.animate.next_to(arr[min(fi, len(vals) - 1)], DOWN, buff=0.3),
                          jl.animate.next_to(arr[max(fj, 0)], DOWN, buff=0.3), run_time=0.6)
                if kind == "swap":
                    a_, b_ = arr[fi][1], arr[fj][1]
                    self.play(a_.animate.move_to(arr[fj][0]), b_.animate.move_to(arr[fi][0]), run_time=0.6)
                    arr[fi].submobjects[1], arr[fj].submobjects[1] = b_, a_
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            for k, c in enumerate(arr):
                c[0].set_fill(YES if k <= frames[-1][2] else CTRL, 0.2)
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def analysis(self):
        head = label(r"The average, \ in one idea", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"name the elements by rank: \ $z_1 < z_2 < \cdots < z_n$; \ pivots chosen uniformly at random",
                  font_size=21, color=GREY_A),
            label(r"$z_i$ and $z_j$ are compared \textbf{exactly when} one of them is the first pivot chosen from "
                  r"$z_i, \ldots, z_j$", font_size=21, color=YES),
            label(r"any other pivot from that range separates them forever; \ one outside it leaves them together",
                  font_size=20, color=GREY_B),
            MathTex(r"\Pr[z_i \text{ and } z_j \text{ compared}] = \frac{2}{j - i + 1}", font_size=34),
            MathTex(r"\mathbb{E}[C_n] = \sum_{i<j} \frac{2}{j-i+1} = 2(n+1)H_n - 4n \;\approx\; 2n \ln n "
                    r"\;\approx\; 1.39\, n \lg n", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Quicksort's average cost has a famously short derivation. <bookmark mark='a'/> Name the elements by "
            "their rank in sorted order, z one up to z n, and choose every pivot uniformly at random. <bookmark "
            "mark='b'/> Two elements z i and z j are compared at most once, and they are compared exactly when one "
            "of them is the first pivot chosen from the range between them. <bookmark mark='c'/> If some element "
            "strictly between them is chosen first, they land on opposite sides and never meet. If an element "
            "outside the range is chosen, they stay together and wait. <bookmark mark='d'/> So the probability is "
            "two out of the j minus i plus one elements in the range. <bookmark mark='e'/> Add over all pairs, and "
            "the expected number of comparisons is two times n plus one times the harmonic number, minus four n: "
            "about two n natural log n, or one point three nine n log base two n. Only thirty-nine percent above "
            "the lower bound, on average."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps[:2].submobjects + [steps[2], steps[3], steps[4]]):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("quick")
        head = label(r"Measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), words(round(r["mean"])), words(round(r["exact"])), words(round(r["nlgn"]))]
                for r in d["rows"]]
        tab = grid_table([r"$n$", r"mean comparisons, \ random pivots", r"$2(n+1)H_n - 4n$", r"$n \lg n$"], rows,
                         widths=[1.8, 4.2, 3.2, 2.2], row_h=0.48, font_size=20,
                         colors=[[WHITE, YES, HEAD, GREY_B]] * len(rows)).next_to(head, DOWN, buff=0.5)
        note = label(r"the formula is exact for the expectation; \ the measurements average 15 to 60 runs",
                     font_size=20, color=GREY_B).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Our quicksort counts its comparisons. <bookmark mark='a'/> Averaged over many runs with random pivots, "
            "the counts match the exact formula to within a fraction of a percent, at every size. And they sit a "
            "little above n log n: the thirty-nine percent that random pivots cost."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def pivots(self):
        d = load("quick")
        p = d["pivots"]
        n = d["pivot_n"]
        head = label(r"Which pivot?", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"the first element", words(p["first"]["random"]), words(p["first"]["sorted"])],
                [r"median of three", words(p["median3"]["random"]), words(p["median3"]["sorted"])],
                [r"random", words(p["random"]["random"]), words(p["random"]["sorted"])]]
        tab = grid_table([rf"pivot rule, \ $n = {words(n)}$", r"random input", r"sorted input"], rows,
                         widths=[4.0, 3.0, 3.0], row_h=0.5, font_size=21, mono_cols=(),
                         colors=[[WHITE, WHITE, NO], [WHITE, WHITE, YES], [WHITE, WHITE, YES]]).next_to(head, DOWN,
                                                                                                buff=0.5)
        pts = VGroup(
            label(r"the first element on sorted input: \ every split is $0$ and $n - 1$: \ $n(n-1)/2$ comparisons",
                  font_size=21, color=NO),
            label(r"real inputs are often sorted, \ or nearly: \ a fixed rule invites the worst case", font_size=21,
                  color=GREY_A),
            label(r"randomness moves the risk from the input to the coin flips, \ which no adversary controls",
                  font_size=21, color=YES),
            label(r"dual-pivot quicksort \ (Yaroslavskiy, \ 2009): \ Java's sort for primitives since Java 7",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The analysis assumed random pivots. What if we take the first element, as the earliest versions did? "
            "<bookmark mark='a'/> On random input it hardly matters. On sorted input it is a disaster: every "
            "partition splits off nothing, and quicksort makes n times n minus one over two comparisons, two "
            "million for two thousand elements. <bookmark mark='b'/> And sorted input is common. The median of the "
            "first, middle and last elements fixes this case. <bookmark mark='c'/> A random pivot fixes every case "
            "at once: the expected cost no longer depends on the input at all, only on coin flips no adversary can "
            "see. <bookmark mark='d'/> Modern versions refine it further. Vladimir Yaroslavskiy's dual-pivot "
            "quicksort has sorted Java's primitive arrays since Java 7."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, pt in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(pt))
        self.wait(0.3)
        self.clear_scene()
