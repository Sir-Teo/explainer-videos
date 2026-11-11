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
            VGroup(
                MathTex(r"\text{in}(v) = w_v + \sum_c \text{out}(c)", font_size=28, color=LAM),
                MathTex(r"\text{out}(v) = \sum_c \max(\text{in}(c), \text{out}(c))", font_size=28, color=LAM),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            label(rf"here: \ fun {d['best']}; \ {d['big_n']:,} people in {d['big_s']:.2f} s", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.55)
        if side.width > 5.8:
            side.scale_to_fit_width(5.8).to_edge(RIGHT, buff=0.55)
        take={};skip={}
        def evaluate(v):
            for c in children.get(v,[]): evaluate(c)
            take[v]=w[v]+sum(skip[c] for c in children.get(v,[]))
            skip[v]=sum(max(take[c],skip[c]) for c in children.get(v,[]))
        evaluate(0)
        witness=MathTex(rf"\mathrm{{in}}(0)={take[0]},\quad\mathrm{{out}}(0)={skip[0]},\quad\max={max(take[0],skip[0])}",font_size=25,color=HEAD).to_edge(DOWN,buff=.35)
        with self.voiceover(
            "A tree lets us combine independent subtrees. <bookmark mark='a'/> Each employee has a fun score, and a "
            "direct boss and report cannot both attend. <bookmark mark='b'/> This maximum-weight independent-set "
            "problem is hard on general graphs but has a simple tree recurrence. <bookmark mark='c'/> Store a take "
            "value and a skip value for every subtree. <bookmark mark='d'/> Taking a vertex forces each child to "
            'skip; skipping it lets each child choose its better state. An iterative postorder handles deep paths '
            "without raising the process recursion limit. <bookmark mark='e'/> The highlighted small-tree selection "
            'is checked by exhaustive search. The large-tree time covers the complete public iterative solver on two '
            'hundred thousand vertices, checked against a separate array recurrence; input generation is excluded.'
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(nd) for nd in nodes.values()])
            for mk, s in zip("abcd", side[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("e")
            self.play(FadeIn(side[4]),FadeIn(witness), *[nodes[v][0].animate.set_fill(YES, 0.5) for v in chosen])
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
            "Several graph algorithms use staged dynamic programming. <bookmark mark='a'/> Bellman-Ford limits the "
            'number of edges; Floyd-Warshall limits permitted intermediate vertices; Held-Karp records a visited '
            "subset and endpoint; DAG longest paths use a topological dependency order. <bookmark mark='b'/> These "
            "state spaces differ, so their costs differ even though all reuse smaller answers. <bookmark mark='c'/> "
            "Held-Karp has exponentially many subsets. Part eighteen's small checked example makes a dramatic "
            'improvement over tour enumeration without turning the problem polynomial. Its time is a measurement from'
            ' that episode, not a new timing in this table.'
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
            label('CYK: substring and grammar states; $O(n^3)$ for a fixed grammar in normal form', font_size=21, color=YES),
            label('convex-hull, divide-and-conquer and Knuth optimizations require structural hypotheses', font_size=21, color=HEAD),
            label(r"the price: \ memory for the table; \ Hirschberg \ (1975) \ recovered edit scripts in linear "
                  r"space", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.7)
        # An explicit layered state graph gives the introductory sentence a visual referent.
        positions = {(t, state): [-3 + 2*t, -1.0 - .8*state, 0] for t in range(4) for state in range(3)}
        edges = VGroup(*[Line(positions[t, a], positions[t+1, b], buff=.18,
                              color=GREY_D, stroke_width=1)
                         for t in range(3) for a in range(3) for b in range(3)])
        nodes = VGroup(*[VGroup(Circle(radius=.18, stroke_color=DATA, fill_color=BG,
                                       fill_opacity=1, stroke_width=1.5),
                                MathTex(rf"s_{{{state}}}", font_size=16)).move_to(positions[t, state])
                         for t in range(4) for state in range(3)])
        route = [1, 0, 2, 1]
        path = VGroup(*[Line(positions[t, route[t]], positions[t+1, route[t+1]],
                            buff=.18, color=HEAD, stroke_width=3) for t in range(3)])
        times = VGroup(*[MathTex(rf"t_{{{t}}}", font_size=19, color=GREY_A).move_to([-3+2*t, -3.0, 0])
                        for t in range(4)])
        trellis = VGroup(edges, path, nodes, times)
        caption = label("Viterbi example: paths through successive hidden-state layers", font_size=17,
                        color=DATA).to_edge(DOWN, buff=.32)
        with self.voiceover(
            "Sequence models offer further examples. <bookmark mark='a'/> Viterbi chooses a maximum-probability path "
            'through a hidden-state trellis; it appears in communication decoding and speech models. <bookmark '
            "mark='b'/> For a fixed context-free grammar in the required normal form, CYK combines substring and "
            "grammar states; grammar size also matters when it is part of the input. <bookmark mark='c'/> Knuth "
            'optimization, divide-and-conquer optimization and convex-hull methods accelerate particular recurrences '
            'only when their structural hypotheses hold. They do not promise the same factor for every table. '
            "<bookmark mark='d'/> Memory can sometimes be reduced too: Hirschberg's divide-and-conquer reconstruction"
            ' recovers an alignment in linear auxiliary space while preserving quadratic time in the general case.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(trellis), FadeIn(caption))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
                if mk == "a":
                    self.play(ShowPassingFlash(path.copy().set_color(YES), time_width=.5), run_time=.8)
        self.wait(0.3)
        self.clear_scene()
