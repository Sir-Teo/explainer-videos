from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.compute import load as load18
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class TreeDp(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.graphs()
        self.sequences()

    def card(self):
        card = chapter_card(13, r"Dynamic programming on trees, \ graphs and sequences",
                            r"What are the subproblems of a tree?", lit=(1967,),
                            extra=((1962, r"Held and Karp"), (1967, r"Viterbi")), part=PART)
        with self.voiceover("Chapter thirteen. Dynamic programming on trees, graphs and sequences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("tree")
        head = label(r"Guests who must not meet their boss", font_size=34).to_edge(UP, buff=0.3)
        parent = {int(k): v for k, v in d["parent"].items()}
        n, w = d["n"], d["w"]
        children = {}
        for v, p in sorted(parent.items()):
            children.setdefault(p, []).append(v)
        depth, xs, cnt = {0: 0}, {}, [0]

        def lay(v):
            for c in children.get(v, []):
                depth[c] = depth[v] + 1
                lay(c)
            if v not in children:
                xs[v] = cnt[0]
                cnt[0] += 1
            else:
                xs[v] = sum(xs[c] for c in children[v]) / len(children[v])
        lay(0)
        span = max(xs.values())
        pos = {v: [-6.2 + 6.4 * xs[v] / span, 2.2 - 0.95 * depth[v], 0] for v in range(n)}
        edges = VGroup(*[Line(pos[p], pos[v], color=GREY_D, stroke_width=1.6) for v, p in parent.items()])
        nodes = {v: VGroup(Circle(radius=0.22, color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1),
                           mono(str(w[v]), 15, WHITE)).move_to(pos[v]) for v in range(n)}
        chosen = set(d["chosen"])
        side = VGroup(
            label(r"a company tree; \ each person has a fun score; \ invite no one together with their boss",
                  font_size=20, color=GREY_A),
            label(r"maximum-weight \textbf{independent set}: \ NP-hard on graphs, \ easy on trees", font_size=21,
                  color=HEAD),
            label(r"for each person $v$, \ two numbers, \ from the children up:", font_size=20, color=GREY_A),
            MathTex(r"\text{in}(v) = w_v + \sum_c \text{out}(c), \qquad \text{out}(v) = \sum_c \max(\text{in}(c), "
                    r"\text{out}(c))", font_size=24, color=LAM),
            label(rf"here: \ fun {d['best']}; \ {d['big_n']:,} people in {d['big_s']:.2f} s", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "On trees, the subproblems are subtrees. <bookmark mark='a'/> A company is planning a party. Each "
            "employee has a fun score, written in their circle, and nobody may be invited together with their "
            "direct boss. Who should come? <bookmark mark='b'/> This is the maximum-weight independent set, which "
            "is NP-hard on general graphs. On a tree it is easy. <bookmark mark='c'/> For each person compute two "
            "numbers, from the bottom of the tree up: the best total for their subtree if they come, and if they "
            "do not. <bookmark mark='d'/> If they come, their reports cannot; if they stay home, each report's "
            "subtree may do whichever is better. <bookmark mark='e'/> The best party here has a total of "
            "forty-seven, and a company of two hundred thousand takes a third of a second."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(nd) for nd in nodes.values()])
            for mk, s in zip("abcd", side[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), *[nodes[v][0].animate.set_fill(YES, 0.5) for v in chosen])
        self.wait(0.3)
        self.clear_scene()

    def graphs(self):
        h = load18("hard")
        head = label(r"Part 18, \ seen again", font_size=34).to_edge(UP, buff=0.3)
        row16 = next(r for r in h["rows"] if r["n"] == 16)
        rows = [
            [r"Bellman--Ford", r"best path to $v$ using at most $k$ edges", r"$V \cdot E$"],
            [r"Floyd--Warshall", r"best $i \to j$ path through the first $k$ vertices", r"$V^3$"],
            [r"Held--Karp", r"best path through the set $S$, \ ending at $j$", r"$2^n n^2$"],
            [r"DAG longest path", r"best path ending at $v$, \ in topological order", r"$V + E$"],
        ]
        tab = grid_table([r"algorithm", r"subproblem", r"time"], rows, widths=[3.0, 6.8, 2.0], row_h=0.58,
                         font_size=21, mono_cols=(), colors=[[DATA, GREY_A, YES]] * 4).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"each is a dynamic programme: \ the subproblems differ, \ the method is the same", font_size=22,
                  color=HEAD),
            label(rf"Held--Karp: \ 16 cities in {row16['held_karp_s']:.1f} s, \ against "
                  rf"${row16['brute'] / 1e11:.1f} \times 10^{{11}}$ tours to try: \ exponential, \ but exponentially better", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Several algorithms of Part 18 were dynamic programmes in disguise. <bookmark mark='a'/> Bellman–Ford's "
            "subproblems are the best paths using at most k edges; Floyd–Warshall's, the best paths through the "
            "first k vertices; Held–Karp's, the best path through a set of cities ending at a given one; and the "
            "longest path in a DAG, the best path ending at each vertex in topological order. <bookmark "
            "mark='b'/> Different subproblems, one method. <bookmark mark='c'/> Held–Karp shows the method's reach "
            "and its limit: sixteen cities in a little over a second, against six hundred and fifty billion tours by brute "
            "force. Still exponential, but exponentially better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def sequences(self):
        head = label(r"And on sequences", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{Viterbi} \ (1967): \ the likeliest hidden states behind observations: \ best path "
                  r"through a trellis \ (\textit{AI, Built}, \ Part 7)", font_size=21, color=DATA),
            label(r"\textbf{CYK} \ (Cocke, \ Younger, \ Kasami, \ 1960s): \ can a grammar derive a string? \ "
                  r"subproblems are substrings, \ $O(n^3)$ \ (Part 12)", font_size=21, color=YES),
            label(r"\textbf{speedups}: \ the convex-hull trick, \ divide-and-conquer optimization, \ Knuth's "
                  r"inequality: \ an $n^2$ or $n^3$ table, \ filled faster by structure", font_size=21, color=HEAD),
            label(r"the price: \ memory for the table; \ Hirschberg \ (1975) \ recovered edit scripts in linear "
                  r"space", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "Sequences are dynamic programming's home ground. <bookmark mark='a'/> Andrew Viterbi's algorithm of "
            "1967 finds the likeliest sequence of hidden states behind a sequence of observations, as a best path "
            "through a trellis; it decodes every mobile phone call, and AI, Built's seventh part used it for "
            "speech. <bookmark mark='b'/> The Cocke–Younger–Kasami algorithm decides whether a grammar can "
            "derive a string, using its substrings as subproblems, in cubic time, as Part 12 showed. <bookmark "
            "mark='c'/> Many dynamic programmes can be sped up when the table has structure, like Knuth's "
            "inequality: the convex-hull trick and divide-and-conquer optimization each shave a factor of n. "
            "<bookmark mark='d'/> The price of the method is memory for the table. Dan Hirschberg showed in 1975 "
            "that edit scripts can be recovered in linear space, combining dynamic programming with divide and "
            "conquer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
