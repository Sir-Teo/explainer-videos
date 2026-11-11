from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, curve, grid_table, load, mono, words)


class Sorting(VoiceoverScene):
    def construct(self):
        self.card()
        self.inside()
        self.crossover()
        self.topk()

    def card(self):
        card = chapter_card(11, r"Sorting in practice", r"When does $n \log n$ lose to $n$?", lit=(1887, 2021),
                            extra=((1887, r"Hollerith's tabulator"), (2021, r"vqsort, \ IPS$^4$o")), part=PART)
        with self.voiceover("Chapter eleven. Sorting in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def crossover(self):
        d = load("sorting")
        rows = d["rows"]
        head = label(r"Comparison sort against radix sort", font_size=32).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[4, 24, 4], y_range=[0, 110, 20], x_length=6.6, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        yt = VGroup(*[mono(str(v), 15, GREY_B).next_to(ax.c2p(4, v), LEFT, buff=0.1) for v in range(0, 101, 20)])
        xt = VGroup(*[MathTex(rf"2^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in range(4, 25, 4)])
        yl = label(r"ns per key", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xl = label(r"keys \ (random 32-bit)", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        xs = [r["logn"] for r in rows]
        cs = curve(ax, xs, [min(r["std_sort"], 110) for r in rows], NO)
        cr = curve(ax, xs, [min(r["radix"], 110) for r in rows], YES)
        kl = VGroup(label(r"\texttt{std::sort} \ (introsort)", font_size=18, color=NO),
                    label(r"LSD radix, \ 4 passes of 8 bits", font_size=18, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(4.3, 108), DR, buff=0.05)
        big_ = rows[-1]
        small = rows[0]
        side = VGroup(
            label('comparison lower bound: $\\lceil\\log_2(n!)\\rceil$ in the worst case; \\\\ radix uses fixed-width digits and extra counters', font_size=20, color=WHITE),
            label(rf"{small['n']} keys: \ \texttt{{std::sort}} {small['std_sort']:.0f} ns a key, \ radix "
                  rf"{small['radix']:.0f}: \\ counting 256 buckets four times is overhead", font_size=20, color=NO),
            label(rf"crossover: \ about {d['crossover']} keys", font_size=20, color=HEAD),
            label('three fixed repetitions; every batch checked; cache effects not isolated', font_size=20, color=YES),
            label(r"in practice: \ hybrids. \ ska\_sort, \ vqsort \ (Google, 2021, SIMD), \\ IPS$^4$o \ (parallel, "
                  r"in place); \ Timsort for nearly sorted data", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        if side.width > 5.4:
            side.width = 5.4
            side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            'Comparison sorting has an n log n worst-case lower bound for arbitrary distinct keys. <bookmark '
            "mark='a'/> Our radix sort instead uses thirty-two-bit unsigned keys and four stable byte passes, "
            "including a fixed counter-array cost per pass. <bookmark mark='b'/> Small batches can be dominated "
            "by that overhead. <bookmark mark='c'/> The crossover in this measurement is a finite workload "
            "result, not a universal threshold. <bookmark mark='d'/> Each timed batch includes its input copy; "
            'every output element of every batch is retained until checked against the library sort after the '
            "timer. Three repetitions supply the plotted minima. <bookmark mark='e'/> The word-RAM explanation "
            'assumes bounded-width keys. Wider integers, memory traffic, temporary storage and parallel '
            'implementations change the comparison.'
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), Create(cr), FadeIn(kl), FadeIn(side[1]), run_time=2.5)
            for mk, n_ in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def inside(self):
        head = label(r"Inside \texttt{std::sort}", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{introsort} \ (Musser, 1997): \ quicksort with a median-of-three pivot", font_size=22,
                  color=WHITE),
            label(r"if the recursion gets deeper than $2 \log_2 n$, \ switch to heapsort: \ never quadratic",
                  font_size=22, color=NO),
            label('small partitions: insertion-sort finish in this libstdc++ build', font_size=22, color=HEAD),
            label('pdqsort: a pattern-defeating quicksort family; library choices change',
                  font_size=22, color=LAM),
            label('Timsort family: stable natural-run merging; type and version matter', font_size=22,
                  color=YES),
            label(r"every one of them is Part 16's algorithms, \ stitched together by measurement", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "What does this production sort do? <bookmark mark='a'/> This GCC libstdc++ implementation uses an "
            "introsort family: quicksort partitioning with a depth limit. <bookmark mark='b'/> A fallback "
            'prevents the quadratic worst case of unguarded quicksort. The C++ interface specifies complexity '
            "requirements without mandating one algorithm for all libraries. <bookmark mark='c'/> This "
            'implementation finishes small partitions with insertion sorting. The cutoff is an implementation '
            "detail. <bookmark mark='d'/> Pattern-defeating quicksort is another important family, rather than a "
            "timeless description of every language's current library. <bookmark mark='e'/> Timsort and related "
            'run-merging policies exploit existing order. Python and Java have type- and version-specific '
            "choices; primitive arrays need not use the object-sorting algorithm. <bookmark mark='f'/> Match any "
            'library claim to a concrete version, type, comparator contract and retained build.'
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def topk(self):
        t = load("topk")
        head = label(r"The top 20 of 16 million", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"sort everything", r"$O(n \log n)$", f"{t['sort'] * 1000:,.0f} ms"],
                [r"\texttt{nth\_element}, \ then sort 20", r"$O(n)$ expected", f"{t['nth_element'] * 1000:.0f} ms"],
                [r"\texttt{partial\_sort}", r"$O(n \log k)$", f"{t['partial_sort'] * 1000:.0f} ms"],
                [r"a heap of 20, \ one pass", r"$O(n \log k)$", f"{t['heap'] * 1000:.0f} ms"]]
        tab = grid_table([r"", r"cost", r"time"], rows, widths=[5.2, 2.8, 2.2], row_h=0.5, font_size=22,
                         mono_cols=(), colors=[[NO] * 3, [HEAD] * 3, [YES] * 3, [YES] * 3])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"the Job's last step is exactly this: \ the 20 most frequent of 58,000 words", font_size=22,
                  color=WHITE),
            label(rf"the heap compares each key with its smallest member and almost always stops there: \ "
                  rf"{t['sort'] / t['heap']:.0f}$\times$ faster than sorting", font_size=22, color=YES),
            label('\\texttt{nth\\_element}: linear average complexity; \\\\ timings include extracting and sorting the selected twenty',
                  font_size=22, color=HEAD),
            label(r"ask for what you need: \ ``the top $k$'' is a different, \ easier problem than ``sorted''",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Often the complete order is unnecessary. <bookmark mark='a'/> Here four methods extract the twenty "
            "largest of sixteen million generated keys. <bookmark mark='b'/> Full sort, partial sort and a small "
            'heap solve different amounts of ordering work. An independent fixed-size sorted insertion reference '
            "checks every returned top-twenty list. <bookmark mark='c'/> The standard nth-element contract gives "
            'linear average complexity for this nonparallel overload, rather than a universal worst-case linear '
            'promise. Its timing includes sorting and extracting the selected twenty. Array input copies are '
            "outside these timers; heap construction and extraction are inside its timer. <bookmark mark='d'/> "
            'The measured winner belongs to this fixed k and distribution. Choosing the required output '
            'specification can matter more than tuning a full sort.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
