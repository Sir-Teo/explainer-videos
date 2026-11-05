from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Heaps(VoiceoverScene):
    def construct(self):
        self.card()
        self.interface()
        self.fibonacci()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Priority queues", r"How cheap can ``decrease a key'' be?", lit=(1987,),
                            extra=((1987, r"Fredman and Tarjan: \ Fibonacci heaps"),), part=PART)
        with self.voiceover("Chapter ten. Priority queues."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def interface(self):
        head = label(r"Insert, \ delete-min, \ decrease-key", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"binary heap \ (Part 16)", r"$O(\log n)$", r"$O(\log n)$", r"$O(\log n)$"],
            [r"binomial heap \ (Vuillemin, \ 1978)", r"$O(1)$ am.", r"$O(\log n)$", r"$O(\log n)$"],
            [r"Fibonacci heap \ (1987)", r"$O(1)$ am.", r"$O(\log n)$ am.", r"$O(1)$ am."],
            [r"pairing heap \ (1986)", r"$O(1)$", r"$O(\log n)$ am.", r"$o(\log n)$ am., \ open"],
        ]
        tab = grid_table([r"heap", r"insert", r"delete-min", r"decrease-key"], rows, widths=[4.6, 2.2, 2.6, 3.4],
                         row_h=0.6, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, GREY_A, NO], [WHITE, GREY_A, GREY_A, GREY_A],
                                 [LAM, YES, GREY_A, YES], [WHITE, GREY_A, GREY_A, HEAD]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"Dijkstra's shortest paths \ (Part 18): \ $n$ delete-mins, \ up to $m$ decrease-keys", font_size=22,
                  color=GREY_A),
            MathTex(r"O(m \log n) \text{ with a binary heap} \quad\to\quad O(m + n \log n) \text{ with a Fibonacci "
                    r"heap}", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "A priority queue holds items with keys and always hands back the smallest. <bookmark mark='a'/> Part "
            "16's binary heap does insert, delete-min and decrease-key, which lowers an item's key, all in "
            "logarithmic time. Binomial heaps make insert constant on average. Fibonacci heaps, from Michael "
            "Fredman and Robert Tarjan in 1987, make decrease-key constant too, amortized. <bookmark mark='b'/> "
            "Why care about decrease-key? Dijkstra's shortest-path algorithm, in Part 18, does one delete-min per "
            "vertex but can do a decrease-key per edge. <bookmark mark='c'/> With a binary heap that costs m log n; "
            "with a Fibonacci heap, m plus n log n, which is much less on dense graphs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def fibonacci(self):
        head = label(r"How a Fibonacci heap is lazy", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{insert}: \ add a one-node tree to a list of roots; \ do nothing else", font_size=22,
                  color=DATA),
            label(r"\textbf{delete-min}: \ remove it, \ then link roots of equal degree until all degrees "
                  r"differ", font_size=22, color=LAM),
            label(r"\textbf{decrease-key}: \ cut the node from its parent, \ make it a root; \ a parent that "
                  r"loses a second child is cut too \ (\textbf{cascading cut})", font_size=22, color=CTRL),
            label(r"the cuts keep a node of degree $k$ above $F_{k+2} \ge \varphi^k$ descendants: \ degrees stay "
                  r"$O(\log n)$, \ hence the name", font_size=21, color=YES),
            MathTex(r"\Phi = \#\text{roots} + 2\,\#\text{marked nodes}", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The Fibonacci heap gets its bounds by putting off work. <bookmark mark='a'/> An insert just adds a "
            "one-node tree to a list of roots. <bookmark mark='b'/> Delete-min removes the minimum, puts its "
            "children on the root list, and only then tidies up, linking trees of equal degree until no two roots "
            "have the same degree. <bookmark mark='c'/> Decrease-key cuts the node away from its parent and makes it "
            "a root. To keep trees bushy, a parent that loses a second child is cut as well, and the cuts can "
            "cascade upward. <bookmark mark='d'/> That rule guarantees that a node with k children has at least a "
            "Fibonacci number of descendants, so degrees stay logarithmic: hence the name. <bookmark mark='e'/> "
            "The potential counts roots and marked nodes, and pays for the delayed linking and the cascades."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("heaps")
        head = label(r"Dijkstra on random graphs, \ counted", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), words(r["m"]), words(r["decrease"]), words(r["binary"]), words(r["pairing"]),
                 words(r["fibonacci"])] for r in d["rows"]]
        tab = grid_table([r"vertices", r"edges", r"decrease-keys", r"binary", r"pairing", r"Fibonacci"], rows,
                         widths=[1.8, 1.8, 2.4, 2.0, 2.0, 2.0], row_h=0.5, font_size=20,
                         colors=[[WHITE, WHITE, HEAD, GREY_A, YES, LAM]] * len(rows)).next_to(head, DOWN, buff=0.6)
        sub = label(r"key comparisons in the heap", font_size=19, color=GREY_B).next_to(tab, UP, buff=0.12).align_to(
            tab, RIGHT)
        pts = VGroup(
            label(r"the Fibonacci heap saves comparisons, \ but only a fifth: \ few decrease-keys on random graphs",
                  font_size=21, color=GREY_A),
            label(r"its pointers and bookkeeping cost more than they save: \ in practice binary and pairing heaps "
                  r"win \ (Larkin, \ Sen and Tarjan, \ 2014)", font_size=21, color=NO),
            label(r"the asymptotic winner is not always the fastest; \ the amortized bound matters on the "
                  r"inputs that need it", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Does it pay? <bookmark mark='a'/> We ran Dijkstra's algorithm on random graphs with each heap and "
            "counted the comparisons inside the heap. The Fibonacci heap does make fewer, about a fifth fewer than "
            "the binary heap, because random graphs need relatively few decrease-keys. <bookmark mark='b'/> In real "
            "time the advantage disappears: each Fibonacci node carries four pointers and a mark, and the "
            "bookkeeping costs more than the comparisons it saves. A careful study by Daniel Larkin, Siddhartha Sen "
            "and Tarjan himself found simple binary and pairing heaps faster in practice. <bookmark mark='c'/> The "
            "lesson recurs throughout this course: an asymptotic bound is a statement about large, hard inputs, "
            "and it is worth its constant only on inputs that need it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(sub))
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
