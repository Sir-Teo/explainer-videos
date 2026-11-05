from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, grid_table,
                                   load, mono, words)


class Bellman(VoiceoverScene):
    def construct(self):
        self.card()
        self.broken()
        self.rounds()
        self.arbitrage()

    def card(self):
        card = chapter_card(7, r"Negative edges", r"What if a road pays you to take it?", lit=(1958,),
                            extra=((1956, r"Ford"), (1958, r"Bellman")), part=PART)
        with self.voiceover("Chapter seven. Negative edges."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def broken(self):
        head = label(r"Dijkstra fails with a negative edge", font_size=34).to_edge(UP, buff=0.3)
        pos = {"s": (-5.8, 0.0), "a": (-3.8, 1.5), "b": (-3.8, -1.5), "t": (-1.8, 0.0)}
        w = {("s", "a"): 2, ("s", "b"): 5, ("b", "a"): -4, ("a", "t"): 1}
        g, nodes, es = draw_graph(pos, list(w), directed=True, weights=w)
        pts = VGroup(
            label(r"Dijkstra settles $a$ at distance 2, \ and never looks back", font_size=22, color=GREY_A),
            label(r"but $s \to b \to a$ costs $5 - 4 = 1$", font_size=22, color=NO),
            label(r"the invariant's step ``a path only gets longer'' is false", font_size=22, color=HEAD),
            label(r"negative edges are real: \\ costs and rebates, \ potentials, \ exchange rates", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Dijkstra's proof needed every edge to be non-negative. <bookmark mark='a'/> Here, the algorithm "
            "settles a at distance two, because that is the smallest tentative distance, and moves on. <bookmark "
            "mark='b'/> But going through b costs five, minus four: one. The path that looked worse became better "
            "after its last step. <bookmark mark='c'/> The step of the proof that said a path only grows as it "
            "continues is simply false here. <bookmark mark='d'/> And negative weights are not exotic: they model "
            "rebates and gains, they appear when costs are measured against a reference, and in the next minute "
            "they will model exchange rates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(nodes["a"][0].animate.set_fill(YES, 0.5), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(es[("s", "b")].animate.set_color(NO), es[("b", "a")].animate.set_color(NO), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def rounds(self):
        head = label(r"Bellman--Ford: \ relax everything, \ $V - 1$ times", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"round $k$: \ relax every edge once", font_size=23, color=GREY_A),
            label(r"after round $k$, \ every shortest path with at most $k$ edges is found \\ (induction on $k$)",
                  font_size=22, color=GREY_A),
            label(r"a shortest path has at most $V - 1$ edges, \ so $V - 1$ rounds suffice: \ $O(VE)$", font_size=22,
                  color=YES),
            label(r"a \textbf{negative cycle} makes ``shortest'' meaningless: \\ round $V$ still improves something, \ "
                  r"and that detects it", font_size=22, color=NO),
            label(r"distance-vector routing \ (RIP, \ Part 36) \ is Bellman--Ford spread across routers, \\ each "
                  r"relaxing its own links", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.4)
        # a worked example: edges relaxed in an unlucky order, so each round extends the paths by one edge
        names = ["s", "a", "b", "c", "t"]
        order = [("c", "t", 2), ("b", "c", -3), ("a", "b", 1), ("s", "a", 3), ("s", "c", 4)]
        dist = {v: math.inf for v in names}
        dist["s"] = 0
        hist = [dict(dist)]
        for _ in range(len(names) - 1):
            for u, v, w in order:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
            hist.append(dict(dist))
        fmt = lambda x: r"$\infty$" if x == math.inf else str(x)
        tab = grid_table([r"after round"] + [rf"${v}$" for v in names],
                         [[str(k)] + [fmt(h[v]) for v in names] for k, h in enumerate(hist)],
                         widths=[2.0] + [1.0] * 5, row_h=0.4, font_size=20, mono_cols=(0,),
                         colors=[[GREY_B] + [YES] * 5] * len(hist)).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.7)
        ex = VGroup(label(r"edges, \ in the order relaxed:", font_size=18, color=GREY_B),
                    *[MathTex(rf"{u} \to {v}: \ {w}", font_size=26) for u, v, w in order]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(tab, RIGHT, buff=0.7)
        with self.voiceover(
            "Lester Ford in 1956 and Richard Bellman in 1958 gave an algorithm that tolerates negative edges. "
            "<bookmark mark='a'/> Simply relax every edge, again and again. <bookmark mark='b'/> After the first round, "
            "every shortest path that uses one edge is right; after round k, every shortest path with at most k "
            "edges, by induction. <bookmark mark='c'/> A shortest path never needs more than V minus one edges, so "
            "that many rounds suffice, for a total of V times E. <bookmark mark='d'/> If a cycle has negative total "
            "length, going around it again and again makes paths arbitrarily short, and shortest is meaningless. The "
            "algorithm detects this: one more round would still improve something. <bookmark mark='e'/> The internet's "
            "early routing protocols ran exactly this computation spread across routers, each one relaxing its own "
            "links, as Part 36 will show."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(ex), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            for row in tab.cells[2:]:
                self.play(FadeIn(VGroup(*row), shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def arbitrage(self):
        d = load("bellman")
        head = label(r"Arbitrage is a negative cycle", font_size=34).to_edge(UP, buff=0.3)
        cur = ["USD", "EUR", "GBP", "JPY"]
        rows = []
        for a in cur:
            row = [a]
            for b in cur:
                r = d["rates"].get(f"{a}>{b}")
                row.append("" if r is None else (f"{r:.4f}" if r < 10 else f"{r:.1f}"))
            rows.append(row)
        tab = grid_table([r"from \ $\backslash$ \ to"] + cur, rows, widths=[2.0, 1.5, 1.5, 1.5, 1.5], row_h=0.42,
                         font_size=19).next_to(head, DOWN, buff=0.35)
        cap = label(r"illustrative rates, \ not market data", font_size=17, color=GREY_B).next_to(tab, DOWN, buff=0.2)
        cyc = d["cycle"]
        steps = VGroup(
            MathTex(r"r_1 r_2 \cdots r_k > 1 \iff \sum_i \bigl(-\log r_i\bigr) < 0", font_size=32, color=YES),
            label(r"weight each edge $-\log(\text{rate})$: \ a profitable loop is a negative cycle", font_size=21,
                  color=GREY_A),
            label(r"Bellman--Ford's extra round finds one: \ " + r" $\to$ ".join(cyc + cyc[:1]), font_size=21,
                  color=HEAD),
            label(rf"one trip round it multiplies the money by {d['gain']:.4f}: \ a {100 * (d['gain'] - 1):.2f}\% "
                  r"profit, \ before fees", font_size=21, color=NO),
            label(r"real markets close such gaps in microseconds: \ trading firms race to find them", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(cap, DOWN, buff=0.3)
        hot = [(cur.index(a_) + 1, cur.index(b_) + 1) for a_, b_ in zip(cyc, cyc[1:] + cyc[:1])]
        with self.voiceover(
            "Here is a negative cycle with money attached. <bookmark mark='a'/> These are exchange rates between four "
            "currencies; they are illustrative, not market data. Converting around a loop multiplies the amount by "
            "the product of the rates, and if that product exceeds one, the loop makes money from nothing. "
            "<bookmark mark='b'/> Take logarithms: a product above one is a sum of logs above zero, so weight each "
            "edge by minus the log of its rate, and a profitable loop becomes a negative cycle. <bookmark mark='c'/> "
            "Bellman–Ford's extra round finds one: yen to pounds to euros and back to yen. <bookmark mark='d'/> One "
            "trip around it returns half a percent more than it started with, before fees. <bookmark mark='e'/> "
            "Real markets close such gaps in microseconds, because trading firms run exactly this search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), *[tab.cells[r][c].animate.set_color(HEAD).scale(1.15) for r, c in hot])
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()
