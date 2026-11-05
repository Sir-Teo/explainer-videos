from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, value_bars, words)


class Insertion(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariant()
        self.inversions()
        self.binary()

    def card(self):
        card = chapter_card(3, r"Insertion sort and its invariant", r"How do we know a loop is right?", lit=(1969,),
                            extra=((1969, r"Hoare's logic"),), part=PART)
        with self.voiceover("Chapter three. Insertion sort and its invariant."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def invariant(self):
        d = load("insertion")
        head = label(r"The sorted part grows by one", font_size=34).to_edge(UP, buff=0.3)
        src = code(["for i in 1 .. n-1:", "    x = a[i]", "    j = i - 1", "    while j >= 0 and a[j] > x:",
                    "        a[j+1] = a[j];  j = j - 1", "    a[j+1] = x"], size=17, color=CODE).to_edge(
            LEFT, buff=0.5).shift(UP * 1.2)
        frames = [d["example"]] + d["steps"]
        bars = value_bars(frames[0], width=0.55, gap=0.12, scale=0.42).move_to(RIGHT * 3.2 + UP * 0.6)
        inv = label(r"\textbf{invariant}: \ before step $i$, \ $a[0..i)$ holds the first $i$ elements, \ in order",
                    font_size=21, color=YES).to_edge(DOWN, buff=1.4)
        proof = VGroup(
            label(r"true at the start \ ($i = 1$); \ each step keeps it; \ at the end \ ($i = n$) \ it says: \ sorted",
                  font_size=20, color=GREY_A),
            label(r"induction on the loop: \ Floyd \ (1967) \ and Hoare \ (1969); \ Part 54 makes machines check it",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)

        def color_prefix(i):
            return [b.animate.set_fill(YES if k < i else DATA, 0.85) for k, b in enumerate(bars.bars)]
        with self.voiceover(
            "The simplest sort worth analysing is the one card players use. <bookmark mark='a'/> Take the next "
            "element, and shift larger elements right until its place opens up. <bookmark mark='b'/> Watch the "
            "green prefix: before each step, the first i elements are in order. That sentence is the loop's "
            "invariant. <bookmark mark='c'/> It is true at the start, when the prefix has one element. Each step "
            "keeps it true. And when the loop ends, with i equal to n, it says the whole array is sorted. This is "
            "induction, applied to a loop, as Robert Floyd and Tony Hoare taught; Part 54 has machines check such "
            "proofs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(bars))
            vo.wait_until("a")
            self.play(*color_prefix(1))
            vo.wait_until("b")
            for i, fr in enumerate(frames[1:], start=2):
                new = value_bars(fr, width=0.55, gap=0.12, scale=0.42).move_to(bars)
                for k, b in enumerate(new.bars):
                    b.set_fill(YES if k < i else DATA, 0.85)
                self.play(Transform(bars, new), run_time=0.8)
            self.play(FadeIn(inv))
            vo.wait_until("c")
            self.play(FadeIn(proof))
        self.wait(0.3)
        self.clear_scene()

    def binary(self):
        d = load("lower")
        r = next(x for x in d["rows"] if x["n"] == 12)
        head = label(r"Fewer comparisons, \ same work", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{binary insertion}: \ find each element's place in the sorted prefix by binary search",
                  font_size=22, color=GREY_A),
            MathTex(r"\sum_{k=1}^{n} \lceil \lg k \rceil \;\approx\; n \lg n \text{ comparisons}", font_size=32,
                    color=YES),
            label(r"but making room still shifts the larger elements: \ $n(n-1)/4$ moves on average", font_size=22,
                  color=NO),
            label(r"comparisons are not the only cost: \ which steps to count depends on the machine", font_size=22,
                  color=HEAD),
            label(rf"for 12 items: \ binary insertion needs {r['binary']} comparisons in the worst case, \ "
                  rf"the bound of chapter 6 is {r['bound']}", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "One improvement is obvious. <bookmark mark='a'/> The prefix is sorted, so find each new element's "
            "place by binary search instead of scanning. <bookmark mark='b'/> The comparisons drop to about n log "
            "n. <bookmark mark='c'/> But the elements still have to be shifted to make room, and the shifts are "
            "still the inversions: quadratic on average. <bookmark mark='d'/> Whether that matters depends on what "
            "a step costs. When comparing is expensive, as with long strings, binary insertion wins; when moving "
            "is, it does not help. Counting steps always begins with deciding which steps to count. <bookmark "
            "mark='e'/> For twelve items it needs thirty-three comparisons in the worst case; chapter six will "
            "show that no method can use fewer than twenty-nine."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def inversions(self):
        d = load("insertion")
        head = label(r"Counting the work: \ inversions", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            label(r"an \textbf{inversion}: \ a pair $i < j$ with $a[i] > a[j]$", font_size=23, color=GREY_A),
            label(r"each shift in the inner loop removes exactly one inversion", font_size=23, color=GREY_A),
            MathTex(r"\mathbb{E}[\text{inversions}] = \binom{n}{2} \cdot \tfrac12 = \frac{n(n-1)}{4}", font_size=34,
                    color=YES),
            label(r"each pair is out of order with probability one half", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.4)
        rows = [[str(r["n"]), f"{r['inv']:,.0f}", f"{r['formula']:,.0f}", f"{r['cmp']:,.0f}"] for r in d["rows"]
                if r["n"] in (10, 100, 1000)]
        tab = grid_table([r"$n$", r"inversions, \ measured", r"$n(n-1)/4$", r"comparisons"], rows,
                         widths=[1.4, 3.2, 2.4, 2.6], row_h=0.46, font_size=19).next_to(defs, DOWN, buff=0.35)
        pts = label(rf"sorted input: \ {words(d['sorted'])} comparisons; \ reversed: \ {words(d['reversed'])}: \ "
                    r"$\Theta(n)$ to $\Theta(n^2)$, \ and the average is quadratic", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How much work does it do? <bookmark mark='a'/> Call a pair of positions an inversion if the earlier "
            "element is larger. Each shift in the inner loop swaps one adjacent inverted pair, so it removes "
            "exactly one inversion, and the total work is the number of inversions plus n. <bookmark mark='b'/> In "
            "a random order each of the n choose two pairs is inverted with probability one half, so the expected "
            "number is n times n minus one over four. <bookmark mark='c'/> Measured over random arrays, the "
            "formula holds. <bookmark mark='d'/> On sorted input insertion sort is linear; on reversed input, and "
            "on average, quadratic. It is the right choice for small or nearly sorted arrays, which is exactly how "
            "real libraries use it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2:]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
