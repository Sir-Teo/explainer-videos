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
            label(r"Timsort family, powersort merge policy here: \ find runs, \ extend short ones by "
                  r"insertion sort, \ merge them cleverly", font_size=20, color=GREY_A),
            label(r"sorted or reversed input: \ $n - 1$ comparisons; \ ten runs: \ a few merges", font_size=21,
                  color=YES),
            label(r"measured interpreter: \ " + d["python"].split(" (")[0]+r"; \ comparison wrapper, not elapsed time", font_size=20,
                  color=GREY_B),
            label(r"Rust changed both standard sorts in 1.81 (2024); \ inspected Go source uses a pdqsort variant", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Existing order is useful information. <bookmark mark='a'/> We count comparisons made by this Python "
            "interpreter's sorted function through a comparison wrapper. These are comparison counts, not elapsed "
            "times. One input uses exactly a thousand random transpositions of an initially sorted "
            "hundred-thousand-element array; that is not exactly one percent of positions shuffled. <bookmark "
            "mark='b'/> Python's sort detects natural runs, extends short runs and merges them. Current "
            "measurements here use the interpreter reported on screen; its modern merge policy is powersort, "
            "within the Timsort family. <bookmark mark='c'/> Implementations evolve. Rust changed both standard "
            "sorting implementations in version one point eight one, so the old Timsort and pattern-defeating "
            "quicksort labels should not be read as current Rust guarantees. Go's inspected sort source uses a "
            "pattern-defeating quicksort variant with a heapsort fallback."
        )
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
            label(r"historical failure; \ later repairs and merge-policy changes; \ Part 54 returns to proof", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(inv, DOWN, buff=0.45)
        with self.voiceover(
            (
            "The historical Timsort bug shows why an invariant must hold everywhere it is needed. <bookmark "
            "mark='a'/> The old merge policy intended run lengths to grow fast enough down the pending stack to "
            "keep its height logarithmic. <bookmark mark='b'/> In 2015, de Gouw and colleagues found that local "
            "repairs near the top did not always restore the required invariant deeper down. Their verification "
            "work led to a constructed input that exhausted the allocated Java run stack. <bookmark mark='c'/> "
            "Implementations adopted repairs, and merge policies later evolved; this is a historical case study, "
            "not a claim that the measured modern Python sort still has that failure. Part 54 returns to the role "
            "of machine-checked proofs."
        )
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
            label(r"\textbf{replacement selection}: \ iid continuous input, long-run expected run length about $2M$ "
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
