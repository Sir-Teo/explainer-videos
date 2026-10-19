from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, PART, PENALTY, REWARD, SEARCH, VALUE, axes, curve, legend, load

MAXC, MINC = C.MODEL_Q, C.TRUE_P  # the player to move (maximizing) and the opponent (minimizing)
LEAVES = [3, 12, 8, 2, 4, 6, 14, 5, 2, 9, 1, 7, 6, 11, 4, 2, 8, 13, 5, 9, 3, 10, 6, 2, 7, 4, 12]


def toy_tree(b=3, depth=3):
    it = iter(LEAVES)

    def make(d):
        if d == depth:
            return {"v": next(it), "children": []}
        return {"children": [make(d + 1) for _ in range(b)]}

    return make(0)


def minimax(t, d=0):
    if not t["children"]:
        return t["v"]
    vals = [minimax(c, d + 1) for c in t["children"]]
    t["v"] = max(vals) if d % 2 == 0 else min(vals)
    return t["v"]


def alphabeta(t, d, a, b, visited):
    visited.add(id(t))
    if not t["children"]:
        return t["v"]
    if d % 2 == 0:
        v = -math.inf
        for c in t["children"]:
            v = max(v, alphabeta(c, d + 1, a, b, visited))
            a = max(a, v)
            if a >= b:
                break
        return v
    v = math.inf
    for c in t["children"]:
        v = min(v, alphabeta(c, d + 1, a, b, visited))
        b = min(b, v)
        if a >= b:
            break
    return v


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.minimax_tree()
        self.counts()
        self.deep_blue()
        self.go()

    def card(self):
        card = chapter_card(10, r"Search before learning", r"How did machines play games before they learned?",
                            lit=(1959, 1997), part=PART)
        with self.voiceover("Chapter ten. Search before learning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def minimax_tree(self):
        t = toy_tree()
        minimax(t)
        visited = set()
        alphabeta(t, 0, -math.inf, math.inf, visited)
        nodes_in_order = []

        def walk(x):
            nodes_in_order.append(x)
            for c in x["children"]:
                walk(c)

        walk(t)
        tree = SearchTree(t, width=10.0, level_height=1.45, radius=0.16, center=[1.5, 0.2, 0])
        n = len(tree.nodes)
        data = tree.node_data
        depth = tree.level
        for i in range(n):
            col = MAXC if depth[i] % 2 == 0 else MINC
            tree.nodes[i].set_color(col)
        vals = VGroup(*[MathTex(str(data[i]["v"]), font_size=24, color=MAXC if depth[i] % 2 == 0 else MINC)
                        .next_to(tree.nodes[i], DOWN if not data[i]["children"] else LEFT, buff=0.1) for i in range(n)])
        leaves = [i for i in range(n) if not data[i]["children"]]
        levels = {d: [i for i in range(n) if depth[i] == d] for d in range(4)}
        rl = VGroup(label(r"you move: \ take the max", font_size=22, color=MAXC),
                    label(r"they move: \ take the min", font_size=22, color=MINC),
                    label(r"you move: \ max", font_size=22, color=MAXC),
                    label(r"positions, \ scored by an evaluation", font_size=22, color=GREY_A))
        for d, r_ in enumerate(rl):
            r_.move_to([-5.2, tree.pos[levels[d][0]][1], 0])
            if r_.width > 3.0:
                r_.width = 3.0
        pruned = [i for i in range(n) if id(data[i]) not in visited]
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        best = max(range(3), key=lambda k: data[tree.kids[0][k]]["v"])
        with self.voiceover(
            "Games are where search was born. A game tree: from the current position, your possible moves, then the "
            "replies to each, and so on. <bookmark mark='a'/> Look a few moves ahead, and score the positions at "
            "the bottom with an evaluation function, a hand-made judgment of who's ahead. <bookmark mark='b'/> Then "
            "back the scores up. Where the opponent moves, assume the reply that's worst for you: the minimum. "
            "<bookmark mark='c'/> Where you move, take the best: the maximum. <bookmark mark='d'/> The root's value "
            "is what you can guarantee against any reply. That's minimax, from von Neumann's 1928 theorem on games, "
            "and the first programs, Shannon's design in 1950 and Samuel's checkers, played this way. "
            "<bookmark mark='e'/> But most of this tree never needed looking at. Once a reply shows a move is worse "
            "than one you already have, the move's other replies don't matter. Skipping them is alpha-beta pruning, "
            f"and here it skips {len(pruned)} of the {n} positions without changing the answer."
        ) as vo:
            self.play(Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rl[3]), LaggedStart(*[FadeIn(vals[i]) for i in leaves], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(FadeIn(rl[2]), LaggedStart(*[FadeIn(vals[i]) for i in levels[2]], lag_ratio=0.05))
            self.play(FadeIn(rl[1]), LaggedStart(*[FadeIn(vals[i]) for i in levels[1]], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(Indicate(rl[1], color=MINC))
            vo.wait_until("d")
            self.play(FadeIn(rl[0]), FadeIn(vals[0]), tree.edges[tree.kids[0][best]].animate.set_stroke(MAXC, 6))
            vo.wait_until("e")
            dim = [tree.nodes[i] for i in pruned] + [tree.edges[i] for i in pruned if tree.edges[i] is not None] + \
                  [vals[i] for i in pruned]
            self.play(*[m.animate.set_opacity(0.15) for m in dim], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("alphabeta")
        D = np.asarray(d["depths"])
        g = axes([1, 9], [0, 8], x_length=6.0, y_length=4.2, xlabel=r"how many moves ahead",
                 ylabel=r"positions examined \ (log scale)", xticks=[1, 3, 5, 7, 9], yticks=[0, 2, 4, 6, 8],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.4, -0.3, 0])
        items = (("minimax", GREY_B, r"minimax"), ("ab_random", MINC, r"alpha-beta, \ random order"),
                 ("ab_ordered", MAXC, r"alpha-beta, \ best-looking first"))
        lines = VGroup(*[curve(g.ax, D, np.log10(np.asarray(d[k])), c, 4) for k, c, _ in items])
        dots = VGroup(*[VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=c) for x, y in zip(D, np.log10(np.asarray(d[k])))])
                        for k, c, _ in items])
        lg = legend([(c, t) for _, c, t in items], font_size=20).next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        mm, ab = float(d["minimax"][-1]), float(d["ab_ordered"][-1])
        th = theorem_card(r"alpha-beta", r"with the best move always tried first, a depth-$d$ search of a tree with "
                          r"$b$ moves per position examines about $2\, b^{d/2}$ positions instead of $b^d$",
                          who=r"Knuth \& Moore (1975)", width=5.2, color=MAXC).next_to(lg, DOWN, buff=0.4)
        if th.get_right()[0] > 6.95:
            th.shift(LEFT * (th.get_right()[0] - 6.95))
        tag = note(r"computed: \ Connect Four, \ $4$ openings").to_corner(DR, buff=0.2)
        with self.voiceover(
            "How much does it save? On Connect Four, searching nine moves deep: plain minimax examines about "
            f"{mm / 1e6:.0f} million positions. <bookmark mark='a'/> Alpha-beta, trying moves in random order, a "
            "fraction of that. <bookmark mark='b'/> Try the best-looking move first, and it examines "
            f"{ab:,.0f}. <bookmark mark='c'/> Knuth and Moore proved that with perfect ordering, the cost falls "
            "from b to the d to about b to the d over two: alpha-beta lets you search twice as deep for the same work."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(lines[0]), FadeIn(dots[0]), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(lg[2]))
            vo.wait_until("c")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def deep_blue(self):
        hc = history_card(1997, r"IBM's Deep Blue beats Garry Kasparov, $3\tfrac12$--$2\tfrac12$",
                          r"alpha-beta on $480$ custom chess chips, \ about $200$ million positions a second; \ an "
                          r"evaluation function of about $8{,}000$ hand-tuned features; \ an opening book and endgame "
                          r"tables", width=8.4, color=MAXC).move_to(UP * 1.2)
        recipe = VGroup(label(r"search", font_size=34, color=SEARCH), label(r"$+$", font_size=34),
                        label(r"a human-designed evaluation", font_size=34, color=GREY_A)).arrange(RIGHT, buff=0.3)
        recipe.move_to(DOWN * 1.6)
        cite_ = cite(r"Campbell, Hoane \& Hsu, \textit{Deep Blue}, Artificial Intelligence (2002)")
        with self.voiceover(
            "This recipe beat the world chess champion. In 1997 IBM's Deep Blue defeated Garry Kasparov over six "
            "games. It ran alpha-beta on four hundred and eighty special-purpose chess chips, about two hundred "
            "million positions a second, with an evaluation function of some eight thousand features tuned by "
            "grandmasters and engineers. <bookmark mark='a'/> Search, plus a human-designed sense of what a good "
            "position looks like."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(recipe, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def go(self):
        d = load("alphabeta")
        rows = VGroup(
            VGroup(VectorizedPoint(), label(r"moves per position", font_size=24, color=GREY_A),
                   label(r"moves per game", font_size=24, color=GREY_A), label(r"game tree", font_size=24, color=GREY_A)),
            VGroup(label(r"chess", font_size=30), MathTex(r"\approx 35", font_size=34), MathTex(r"\approx 80", font_size=34),
                   MathTex(r"\approx 10^{123}", font_size=34, color=VALUE)),
            VGroup(label(r"Go", font_size=30), MathTex(r"\approx 250", font_size=34), MathTex(r"\approx 150", font_size=34),
                   MathTex(r"\approx 10^{360}", font_size=34, color=VALUE)),
        )
        for r_ in rows:
            for j, m in enumerate(r_):
                m.move_to([-4.6 + 3.1 * j, 0, 0])
        rows.arrange(DOWN, buff=0.45)
        for r_ in rows:
            for j, m in enumerate(r_):
                m.set_x(-4.6 + 3.1 * j)
        rows.move_to(UP * 1.4)
        cite_ = cite(r"L.~V.~Allis, \textit{Searching for Solutions in Games and Artificial Intelligence} (1994)")
        hard = VGroup(label(r"and no good evaluation function:", font_size=28, color=PENALTY),
                      label(r"who is winning a Go position is a matter of judgment", font_size=26, color=GREY_A))
        hard.arrange(DOWN, buff=0.15).move_to(DOWN * 1.4)
        with self.voiceover(
            "Go was different. <bookmark mark='a'/> A chess position offers about thirty-five moves; a Go position, "
            "about two hundred and fifty, and a game lasts about a hundred and fifty moves. The full game tree has "
            "something like ten to the three hundred and sixty positions. <bookmark mark='b'/> Worse, nobody could "
            "write down an evaluation function. Counting material works in chess; in Go, who is ahead depends on "
            "shape and influence that strong players feel rather than calculate. Nearly twenty years after Deep "
            "Blue, the "
            "best Go programs were still far below the best humans."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.4), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(hard, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
