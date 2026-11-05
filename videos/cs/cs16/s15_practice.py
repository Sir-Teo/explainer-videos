from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.timsort()
        self.bug()
        self.external()

    def card(self):
        card = chapter_card(14, r"Sorting in practice", r"What do real libraries do?", lit=(2002,),
                            extra=((2002, r"Peters: \ Timsort"),), part=PART)
        with self.voiceover("Chapter fourteen. Sorting in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def timsort(self):
        d = load("practice")
        head = label(r"Timsort: \ use the order that is already there", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r["input"].replace("%", r"\%"), words(r["timsort"]), words(r["merge"])] for r in d["rows"]]
        tab = grid_table([rf"$n = {words(d['n'])}$", r"Python's \texttt{sorted}", r"our merge sort"], rows,
                         widths=[3.8, 3.2, 3.0], row_h=0.48, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, GREY_B]] * len(rows)).next_to(head, DOWN, buff=0.45)
        pts = VGroup(
            label(r"Timsort \ (Tim Peters, \ 2002): \ find the runs already in the data, \ extend short ones by "
                  r"insertion sort, \ merge them cleverly", font_size=20, color=GREY_A),
            label(r"sorted or reversed input: \ $n - 1$ comparisons; \ ten runs: \ a few merges", font_size=21,
                  color=YES),
            label(r"Python, \ Java's objects, \ Android, \ Swift and Rust's stable sort descend from it", font_size=20,
                  color=GREY_B),
            label(r"unstable sorts went the other way: \ pdqsort \ (Orson Peters, \ 2021) \ in Rust and Go", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real data is rarely random. It arrives sorted, or nearly sorted, or as several sorted pieces "
            "concatenated. <bookmark mark='a'/> We counted the comparisons made by Python's own sort on a hundred "
            "thousand items. On random input it does what merge sort does. On sorted or reversed input it makes "
            "n minus one comparisons. On ten concatenated sorted runs, a few merges. <bookmark mark='b'/> That is "
            "Timsort, written by Tim Peters for Python in 2002. It scans for runs that are already in order, "
            "extends short ones with insertion sort, and merges runs of similar length so the merging stays "
            "balanced. <bookmark mark='c'/> Its descendants sort objects in Java, Android, Swift and Rust. For "
            "sorts that need not be stable, the newest standard is pattern-defeating quicksort, in Rust and Go."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()

    def bug(self):
        head = label(r"A bug found by proof \ (de Gouw et al., \ 2015)", font_size=34).to_edge(UP, buff=0.3)
        inv = VGroup(
            label(r"Timsort keeps a stack of runs, \ and an invariant on their lengths:", font_size=22, color=GREY_A),
            MathTex(r"r_{i-2} > r_{i-1} + r_i \quad\text{and}\quad r_{i-1} > r_i \quad\text{for every } i",
                    font_size=32, color=YES),
            label(r"which keeps the stack short: \ its lengths grow like Fibonacci numbers", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"the code checked it only for the top three runs; \ a merge could break it further down", font_size=21,
                  color=NO),
            label(r"found while proving Java's \texttt{TimSort} correct with the KeY verifier", font_size=21,
                  color=GREY_A),
            label(r"a crafted array overflowed the fixed-size run stack: \ an exception, \ in a library sort used by "
                  r"billions of devices", font_size=21, color=NO),
            label(r"fixed in OpenJDK and CPython; \ Part 54: \ what proofs find that tests do not", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(inv, DOWN, buff=0.45)
        with self.voiceover(
            "Even this code, among the most used in the world, hid a bug for more than a decade. <bookmark "
            "mark='a'/> Timsort keeps a stack of runs waiting to be merged, with an invariant on their lengths: "
            "each is longer than the next two together. That makes the lengths grow like Fibonacci numbers, so "
            "the stack stays short, and Java allocated it with a fixed size. <bookmark mark='b'/> In 2015 Stijn de "
            "Gouw and colleagues tried to prove Java's implementation correct with the KeY verifier, and could "
            "not: the code restored the invariant only for the top three runs, and a merge could break it further "
            "down. <bookmark mark='c'/> They built an input that overflowed the run stack and crashed the sort. "
            "The fix went into OpenJDK and into CPython. Part 54 returns to what proofs find that tests miss."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(inv))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()

    def external(self):
        d = load("practice")
        head = label(r"When the data does not fit: \ external merge sort", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"1. \ read what fits in memory, \ sort it, \ write it out as a \textbf{run}", font_size=22,
                  color=GREY_A),
            label(r"2. \ merge $k$ runs at once with a heap, \ one block of each in memory", font_size=22,
                  color=GREY_A),
            label(r"\textbf{replacement selection}: \ a heap of $M$ records emits runs of $2M$ on random input "
                  r"\ (Knuth)", font_size=22, color=YES),
            label(rf"ours: \ $M = {words(d['rs_m'])}$, \ {words(d['rs_records'])} random records: \ {d['rs_runs']} runs, "
                  rf"\ the inner ones average {d['rs_mean']:,.0f}", font_size=22, color=YES),
            label(r"on sorted input, \ a single run: \ the whole file", font_size=21, color=GREY_B),
            label(r"the cost that matters is passes over the disk: \ the external-memory model of chapter 1",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Sorting a file larger than memory changes what is expensive. <bookmark mark='a'/> Read as much as "
            "fits, sort it, and write it back as a sorted run. <bookmark mark='b'/> Then merge many runs at once, "
            "keeping one block of each in memory and a heap to pick the smallest head. <bookmark mark='c'/> A "
            "classic trick makes the runs longer than memory. Replacement selection keeps a heap of M records: "
            "output the smallest, read the next record, and if it is still at least the last output, it joins the "
            "current run. Knuth showed that on random input the runs average two M. <bookmark mark='d'/> Ours, "
            "with a thousand records of memory, made runs averaging two thousand. <bookmark mark='e'/> On sorted "
            "input it makes one run: the whole file. <bookmark mark='f'/> Fewer runs means fewer passes over the "
            "disk, which is the cost that matters in the external-memory model, and in every database's sort."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
