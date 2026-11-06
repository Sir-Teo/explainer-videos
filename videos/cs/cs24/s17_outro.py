from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (BG, COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, load)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        h = load("hook")["rows"][-1]
        j = load("job")
        tiles = Group(
            tile(MathTex(r"S_{r+1} - S_l", font_size=46, color=DATA), r"prefix sums", DATA),
            tile(MathTex(r"i \mathbin{\&} -i", font_size=48, color=LAM), r"Fenwick; \ segment trees", LAM),
            tile(MathTex(r"\min(x, x) = x", font_size=42, color=HEAD), r"sparse tables; \ LCA", HEAD),
            tile(MathTex(r"3^n", font_size=52, color=CTRL), r"bits; \ the Four Russians", CTRL),
            tile(MathTex(rf"{h['ratio']:.0f}\times", font_size=50, color=NO), r"same big-O, \ measured", NO),
            tile(MathTex(rf"{j['engineered']['best'] * 1000:.0f}\,\text{{ms}}", font_size=46, color=COST),
                 r"the Job: \ ledger row 10", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Algorithms in Practice", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Prefix sums and difference arrays, and the integral image. Fenwick trees "
            "from a single bit trick, and segment trees for any associative operation, lazily. Sparse tables, "
            "lowest common ancestors and the Cartesian tree that makes them the same problem. Two pointers, "
            "monotonic stacks and binary search on the answer. Bit tricks, submasks and the Four Russians; meet in "
            "the middle and square roots. Then the machine: two linear loops a hundred and forty times apart, "
            "search layouts, vector scans, Swiss tables and radix sort, all measured honestly, and the Job at "
            "seventy-five milliseconds."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"B+ trees and vectorized query execution", [35]),
            (r"merge bases as lowest common ancestors", [41]),
            (r"columnar files and SIMD scans", [46]),
            (r"galloping intersection and SIMD posting-list codecs", [47]),
            (r"caches, \ tail latency and p99 against load", [48]),
            (r"the roofline: \ when memory, \ not arithmetic, \ is the limit", [60]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 35's database indexes a billion rows with three levels of a B-plus tree, the "
            "layout of chapter nine, and executes queries in vectors. Part 41 finds merge bases as lowest common "
            "ancestors. Part 46 scans columnar files with vector instructions. Part 47's search engine gallops "
            "through posting lists and decodes them with SIMD. Part 48 measures tail latency under load, which needs "
            "the benchmarking of chapter twelve. And Part 60's roofline model makes this part's lesson exact: most "
            "programs are limited by memory, not by arithmetic."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"interviews", r"the twenty patterns of chapter 13, \ with complexity and edge cases"),
            (r"databases", r"B+ trees, \ bitmaps, \ vectorized scans, \ radix-partitioned joins"),
            (r"search", r"posting lists, \ galloping, \ SIMD decoding, \ top-$k$ heaps"),
            (r"games, \ finance", r"Fenwick trees for leaderboards and order books; \ segment trees for ranges"),
            (r"performance work", r"profilers, \ microbenchmarks with confidence intervals, \ layouts before "
                                  r"algorithms"),
        ])
        with self.voiceover(
            "In practice. Interviews test the patterns of chapter thirteen, with their costs and edge cases. Databases "
            "and search engines are built from B-plus trees, bitmaps, galloping intersections and vector scans. "
            "Games and exchanges keep leaderboards and order books in Fenwick and segment trees. And performance "
            "work on a hot path starts with a profiler and an honest benchmark, and usually ends with a better "
            "memory layout."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that a Fenwick prefix query visits at most $\lfloor \log_2 n \rfloor + 1$ cells, \ and that its "
            r"ranges tile $[1, i]$.",
            r"Prove that the sliding-window maximum's deque does at most $2n$ pushes and pops in total.",
            r"Show that every range-minimum query is a lowest-common-ancestor query in the Cartesian tree, \ and "
            r"build the tree in $O(n)$.",
            r"Prove that enumerating every submask of every mask of $n$ bits takes exactly $3^n$ steps.",
            r"\textit{Build.} \ A Fenwick tree in the Pebble language, \ over the Job's word counts: \ answer ``how "
            r"many words of the novel are among the top $k$?'' \ for every $k$.",
            r"$\bigstar$ \textit{Research.} \ Our corpus's learned-index segments grow like $\varepsilon^{1.4}$, \ "
            r"not $\varepsilon^2$. \ Model the gaps of real text, \ with their correlations, \ and prove a bound that "
            r"matches; \ or show which property of text breaks the independent-gaps theory.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: a Fenwick tree in the Pebble language, run on the emulator over the Job's own counts. The last, "
            "marked with a star, is a research problem: its answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 25, \ Undecidable", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"reductions, \ and Rice's theorem", DATA),
            (r"Diophantine equations and tilings of the plane", YES),
            (r"G\"odel's incompleteness, \ from a program that prints itself", LAM),
            (r"the busy beaver: \ where provability runs out", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Act Five begins, with limits. Part 1 proved that one problem cannot be solved. Part 25 finds "
            "the same impossibility everywhere: in every non-trivial question about what programs do, in equations "
            "over the integers, in tilings of the plane, and in Gödel's theorem, all from the fact that a program "
            "can print its own source. And the busy beaver marks the place where proof itself runs out. Part 25, "
            "Undecidable."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Skiena, \textit{The Algorithm Design Manual}; \ Bentley, \textit{Programming Pearls}; \ Warren, "
             r"\textit{Hacker's Delight}",
             r"Laaksonen, \textit{Guide to Competitive Programming}; \ Halim and Halim, \textit{Competitive "
             r"Programming}",
             r"M\"uller-Hannemann and Schirra (eds.), \textit{Algorithm Engineering}; \ P\'olya, \textit{How to Solve "
             r"It}"],
            [r"Fenwick (1994); \ Bender and Farach-Colton (2000); \ Fischer and Heun (2011); \ Horowitz and Sahni "
             r"(1974)",
             r"Arlazarov, Dinic, Kronrod and Faradzev (1970); \ Allison and Dix (1986); \ Hyyr\"o (2004)",
             r"Khuong and Morin (2017); \ Langdale and Lemire (2019); \ Mytkowicz et al. (2009); \ Curtsinger and "
             r"Berger (2013)",
             r"Kraska et al. (2018); \ Ferragina and Vinciguerra (2020); \ Purohit, Svitkina and Kumar (2018); \ "
             r"Lykouris and Vassilvitskii (2018)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
