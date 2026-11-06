from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Craft(VoiceoverScene):
    def construct(self):
        self.card()
        self.polya()
        self.worked()
        self.repertoire()

    def card(self):
        card = chapter_card(13, r"Problem solving as a craft", r"What do you do with a problem you have never seen?",
                            lit=(1945,), extra=((1945, r"P\'olya, \textit{How to Solve It}"),), part=PART)
        with self.voiceover("Chapter thirteen. Problem solving as a craft."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def polya(self):
        head = label(r"P\'olya's four steps, \ for programs", font_size=34).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"\textbf{1. Understand the problem.} \ Work three tiny examples by hand; \ find the edge cases "
                  r"(empty, \ one element, \ duplicates, \ overflow)", font_size=22, color=WHITE),
            label(r"\textbf{2. Make a plan.} \ Have you seen it before, \ in disguise? \ Reduce it to a known problem; "
                  r"\ specialize; \ generalize; \ work backwards", font_size=22, color=DATA),
            label(r"\textbf{3. Carry it out.} \ Write the brute force first: \ it is the reference you test against",
                  font_size=22, color=HEAD),
            label(r"\textbf{4. Look back.} \ Check the invariant; \ stress-test the fast version against the slow one "
                  r"on thousands of random inputs", font_size=22, color=YES),
            label(r"every algorithm in this series was checked this way: \ \texttt{tests/test\_cs24\_practice.py} "
                  r"compares each structure with brute force", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        if steps.width > 13.0:
            steps.width = 13.0
        with self.voiceover(
            "In 1945 George Pólya wrote a small book on how to solve mathematical problems, and it is still the best "
            "advice for algorithms. <bookmark mark='a'/> First, understand the problem: work three tiny examples by "
            "hand, and find the edge cases before they find you. <bookmark mark='b'/> Second, make a plan, and the "
            "most powerful question is: have I seen this before, in disguise? Booking meeting rooms is interval "
            "colouring; the cheapest way to connect cities is a spanning tree; a puzzle with a monotone answer is a "
            "binary search. <bookmark mark='c'/> Third, carry it out, and write the brute force first, because it is "
            "the reference you will test the fast version against. <bookmark mark='d'/> Fourth, look back: state the "
            "invariant, and stress-test the fast solution against the slow one on thousands of random inputs. "
            "<bookmark mark='e'/> That is how every structure in this part was checked."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s_ in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def worked(self):
        d = load("pairs")
        head = label(r"The four steps on one problem", font_size=34).to_edge(UP, buff=0.35)
        prob = label(r"count the pairs $i < j$ with $a_i + a_j \le T$", font_size=26, color=WHITE).next_to(
            head, DOWN, buff=0.4)
        b = sorted([7, 2, 9, 4, 1, 6, 3])
        T = 8
        cw = 0.6
        cells = VGroup(*[VGroup(Rectangle(width=cw, height=0.5, stroke_color=GREY_B, stroke_width=1.2),
                                mono(str(v), 20, WHITE)) for v in b])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0).next_to(prob, DOWN, buff=0.45)
        tl = label(rf"sorted, \ $T = {T}$", font_size=18, color=GREY_A).next_to(cells, LEFT, buff=0.25)
        pi = Triangle(color=YES, fill_opacity=1).scale(0.1).next_to(cells[0], DOWN, buff=0.06)
        pj = Triangle(color=NO, fill_opacity=1).scale(0.1).next_to(cells[-1], DOWN, buff=0.06)
        rows = [[words(r["n"]), f"{r['brute_s'] * 1000:.0f} ms", f"{r['fast_s'] * 1000:.2f} ms"] for r in d["rows"]]
        tab = grid_table([r"$n$", r"brute force, \ $O(n^2)$", r"sort + two pointers"], rows, widths=[1.6, 3.4, 3.4],
                         row_h=0.38, font_size=20, mono_cols=(), colors=[[WHITE, NO, YES]] * len(rows))
        notes = VGroup(
            label(r"\textbf{understand}: \ $[1, 2, 3]$, $T = 4$: \ pairs $(1,2), (1,3)$; \ empty input: \ 0", font_size=21,
                  color=WHITE),
            label(r"\textbf{plan}: \ order doesn't matter, \ so sort; \ if $a_i + a_j \le T$, \ every partner of $a_i$ up "
                  r"to $j$ works too", font_size=21, color=DATA),
            label(r"\textbf{carry out}: \ the brute force first, \ then two pointers: \ add $j - i$ and advance $i$, \ "
                  r"or retreat $j$", font_size=21, color=HEAD),
            label(rf"\textbf{{look back}}: \ {words(d['tests'])} random small inputs, \ {d['fails']} disagreements; "
                  r"\ then time both", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(cells, DOWN, buff=0.4)
        tab.next_to(notes, DOWN, buff=0.3).set_x(0)
        with self.voiceover(
            "Here are the four steps on a small problem: count the pairs whose sum is at most T. <bookmark mark='a'/> "
            "Understand it with tiny cases: one, two, three with T equal to four gives two pairs; an empty array gives "
            "none. <bookmark mark='b'/> Plan. The pairs don't depend on the order, so sort. Then if the smallest "
            "remaining value plus the largest fits under T, so does the smallest plus everything in between: all "
            "those pairs at once. <bookmark mark='c'/> Carry it out: brute force first, then two pointers from the "
            "ends. If the pair fits, count j minus i and move i right; if not, move j left. <bookmark mark='d'/> Look "
            "back: two thousand random small inputs, and the fast version never disagreed with the slow one. Only "
            "then time it: on four thousand numbers in Python, four hundred milliseconds for the brute force, under "
            "one millisecond for the two pointers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prob))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells), FadeIn(tl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(pi), FadeIn(pj), FadeIn(notes[2]))
            i, j = 0, len(b) - 1
            while i < j:
                if b[i] + b[j] <= T:
                    i += 1
                    self.play(pi.animate.next_to(cells[i], DOWN, buff=0.06), run_time=0.4)
                else:
                    j -= 1
                    self.play(pj.animate.next_to(cells[j], DOWN, buff=0.06), run_time=0.4)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    def repertoire(self):
        head = label(r"The repertoire, \ and where this course builds it", font_size=32).to_edge(UP, buff=0.3)
        rows = [
            [r"hash maps, \ counting, \ dedup", r"Part 17", r"two pointers, \ sliding windows", r"24 ch. 5"],
            [r"stacks, \ queues, \ monotonic stacks", r"17, \ 24", r"binary search on the answer", r"24 ch. 6"],
            [r"heaps, \ top-$k$, \ merge $k$ lists", r"Part 17", r"prefix sums, \ difference arrays", r"24 ch. 1"],
            [r"BFS, \ DFS, \ topological sort", r"Part 18", r"intervals, \ sweeps, \ greedy", r"19, \ 22"],
            [r"shortest paths, \ union-find, \ MST", r"17, \ 18", r"dynamic programming", r"Part 19"],
            [r"tries, \ string matching", r"Part 21", r"backtracking, \ subsets, \ bitmasks", r"19, \ 24"],
            [r"an LRU cache", r"9, \ 17, \ 23", r"Fenwick and segment trees", r"24 ch. 2--3"],
        ]
        tab = grid_table([r"pattern", r"built in", r"pattern", r"built in"], rows, widths=[4.6, 1.8, 4.6, 1.8],
                         row_h=0.46, font_size=20, mono_cols=(), colors=[[WHITE, DATA, WHITE, DATA]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"interviews test fluency with about twenty patterns; \ the job tests judgment: \ which one, \ and "
                  r"what it costs on the machine", font_size=21, color=YES),
            label(r"Skiena's \textit{Algorithm Design Manual}: \ a catalogue of problems in disguise", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Programming interviews draw on a repertoire of about twenty patterns, and this course has now built all "
            "of them. <bookmark mark='a'/> Hash maps for counting, from Part 17; two pointers and sliding windows "
            "from this part; heaps for the top k; breadth-first and depth-first search and topological order from "
            "Part 18; union-find and spanning trees; dynamic programming and backtracking from Part 19; tries and "
            "string matching from Part 21; and the least-recently-used cache, a hash map threaded with a doubly linked "
            "list, which needed Part 9's hierarchy and Part 23's competitive analysis to justify. <bookmark mark='b'/> An interview tests "
            "fluency. The job tests judgment: which tool, and what it costs on a real machine, which is what the "
            "second half of this part measured. <bookmark mark='c'/> Steven Skiena's Algorithm Design Manual is a "
            "catalogue of problems in disguise, for when Pólya's second step needs help."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()
