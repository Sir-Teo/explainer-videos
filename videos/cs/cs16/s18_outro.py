from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono,
                                   value_bars)


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
        tiles = Group(
            tile(MathTex(r"f = \Theta(g)", font_size=44, color=DATA), r"orders of growth", DATA),
            tile(value_bars([1, 2, 4, 5, 6, 3], labels=False), r"invariants and inversions", YES),
            tile(MathTex(r"T(n) = aT(n/b) + f(n)", font_size=34, color=LAM), r"the master theorem", LAM),
            tile(MathTex(r"\lg n! \approx n \lg n - 1.44n", font_size=34, color=HEAD), r"the lower bound", HEAD),
            tile(MathTex(r"\tfrac{2}{j - i + 1}", font_size=48, color=CTRL), r"quicksort's $2n \ln n$", CTRL),
            tile(MathTex(r"T(n/5) + T(7n/10) + n", font_size=32, color=FUNC), r"linear selection", FUNC),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Counting Steps", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. A model of computation, and the notation that ignores constants. "
            "Insertion sort with its invariant and its inversions. Merge sort and the recursion tree, and the "
            "master theorem that sums such trees. The lower bound every comparison sort obeys, and merge insertion, "
            "which meets it for small n. Quicksort's average from one probability, and ten thousand runs showing "
            "how tightly it holds. Sorting faster than n log n by reading keys, selection in linear time, "
            "generating functions, amortized analysis, and the Job, sorted, eleven times faster than before on the "
            "same core."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"hash tables: \ the Job in expected linear time, \ ledger row 8", [17]),
            (r"heaps in Dijkstra's algorithm; \ graph search", [18]),
            (r"divide and conquer, \ dynamic programming", [19]),
            (r"randomized algorithms and concentration", [20]),
            (r"suffix arrays: \ sorting all the suffixes", [21]),
            (r"lower bounds, \ and P against NP", [26]),
            (r"sort-merge joins and external sorting", [35]),
            (r"MapReduce's shuffle: \ a distributed sort", [39]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 17 replaces the sort with a hash table, for ledger row eight. Part 18's "
            "graph algorithms run on heaps. Part 19 generalizes divide and conquer, and adds dynamic programming. "
            "Part 20 builds the probability tools that chapter nine only previewed. Part 21 sorts all the suffixes "
            "of a text to search it. Part 26 asks which lower bounds can be proved at all. Part 35's database "
            "sorts and joins tables larger than memory, and Part 39's MapReduce is, at heart, a distributed sort."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"libraries", r"know your language's sort: \ stable or not, \ by key, \ worst case"),
            (r"review", r"a loop inside a loop over the same data is $n^2$: \ the commonest performance bug"),
            (r"interviews", r"the first questions: \ complexity, \ an invariant, \ a recursion tree"),
            (r"data", r"\texttt{ORDER BY} on big tables is an external merge sort"),
            (r"choosing", r"measure on real data: \ presorted input changes the winner"),
        ])
        with self.voiceover(
            "In practice. Know your language's sort: whether it is stable, how it takes a key, what its worst case "
            "is. In code review, a loop inside a loop over the same collection is quadratic, and it is the most "
            "common performance bug there is: it is the Job v0. Interviews begin with exactly this chapter: a "
            "complexity, an invariant, a recursion tree. Sorting a large table in a database is an external merge "
            "sort. And when choosing, measure on real data, because presorted input changes the winner."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that insertion sort makes at most $I + n - 1$ comparisons, \ where $I$ is the number of "
            r"inversions, \ and that $\mathbb{E}[I] = n(n-1)/4$ for a random order.",
            r"Solve $T(n) = 4T(n/2) + n^2 \lg n$, \ where the master theorem's three cases do not apply, \ with a "
            r"recursion tree.",
            r"Prove that finding both the minimum and the maximum of $n$ items needs $\lceil 3n/2 \rceil - 2$ "
            r"comparisons, \ and give an algorithm that uses exactly that many.",
            r"Show that quickselect, \ asked for the minimum, \ makes $2n - 2H_n$ comparisons on average.",
            r"\textit{Build.} \ Rewrite the Job v1 with a radix sort on letters, \ in the Pebble language, \ and "
            r"compare its instruction count with the merge sort on our passages.",
            r"$\bigstar$ \textit{Research.} \ Sort $n$ word-size integers in $O(n)$ time on a word-RAM, \ or prove "
            r"that no algorithm can, \ in a model that allows the usual arithmetic.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: sort the Job's words with a radix sort instead, and measure it on Pebble against the merge "
            "sort. The last, marked with a star, is a research problem: its answer is not known, and the notes say "
            "where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 17, \ Data Structures", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"hashing, \ and the birthday bound", DATA), (r"balanced trees: \ AVL, \ red--black, \ splay", LAM),
            (r"union--find and the inverse Ackermann function", YES), (r"the Job with a hash table: \ ledger row 8",
                                                                        COST))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"the Job is a dictionary problem: \ insert, \ look up, \ count", font_size=26,
                  color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. The Job is really a dictionary problem: insert a word, look it up, add one. Hashing does "
            "it in expected constant time, if the hash function cannot be gamed; balanced trees guarantee their "
            "time; and union–find runs in time bounded by the inverse of Ackermann's function. Part 17, Data "
            "Structures."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Cormen, Leiserson, Rivest and Stein, \textit{Introduction to Algorithms}, \ chapters 1--9",
             r"Knuth, \textit{The Art of Computer Programming}, \ volume 3, \ \textit{Sorting and Searching}",
             r"Sedgewick and Flajolet, \textit{An Introduction to the Analysis of Algorithms}",
             r"Graham, Knuth and Patashnik, \textit{Concrete Mathematics}; \ Flajolet and Sedgewick, "
             r"\textit{Analytic Combinatorics}",
             r"Kleinberg and Tardos, \textit{Algorithm Design}; \ Erickson, \textit{Algorithms}"],
            [r"Hoare, ``Quicksort'' (1961, 1962); \ Williams (1964); \ Floyd (1964)",
             r"Ford and Johnson (1959); \ Wells (1965); \ Blum, Floyd, Pratt, Rivest and Tarjan (1973)",
             r"Bentley, Haken and Saxe (1980); \ Akra and Bazzi (1998); \ Tarjan, ``Amortized complexity'' (1985)",
             r"McDiarmid and Hayward (1996); \ Yaroslavskiy (2009); \ Peters, Timsort (2002), \ pdqsort (2021)",
             r"de Gouw et al., ``OpenJDK's java.utils.Collection.sort() is broken'' (2015)",
             r"Han and Thorup (2002); \ Spielman and Teng (2001); \ Backurs and Indyk (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
