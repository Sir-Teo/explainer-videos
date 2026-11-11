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
            label("after round $k$: \\ at least as good as every path with at most $k$ edges \\\\ (induction on $k$)",
                  font_size=22, color=GREY_A),
            label("without a reachable negative cycle: \\ a simple shortest path uses at most $V-1$ edges \\\\ $V-1$ rounds suffice; \\ $O(VE)$", font_size=22,
                  color=YES),
            label("source-reachable negative cycle: downstream distances have no lower bound \\\\ an improvement in round $V$ detects one", font_size=22, color=NO),
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
            "Bellman-Ford permits negative edges. <bookmark mark='a'/> Repeatedly relax every directed "
            "edge. <bookmark mark='b'/> After round k, distances are at least as good as every source "
            "path using at most k edges. With in-place updates, a round may propagate farther; the table "
            "shows this distinction. <bookmark mark='c'/> If no reachable negative cycle exists, a "
            "shortest path can be simple and uses at most V minus one edges. That many rounds suffice, "
            "giving order V times E. <bookmark mark='d'/> An improvement in one more round detects a "
            "negative cycle reachable from the source. Only vertices downstream of such a cycle have "
            "distances unbounded below; unrelated finite distances need not disappear. <bookmark "
            "mark='e'/> Distributed distance-vector routing uses related relaxations, with separate "
            "convergence and failure-handling issues."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ex), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
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
            "A rate product gives a negative-cycle example. <bookmark mark='a'/> These four-currency "
            "rates are invented illustrations, not market observations. Multiplying rates around a loop "
            "gives the gross conversion factor, before fees, spreads and execution constraints. <bookmark"
            " mark='b'/> Weight each edge by minus the logarithm of its rate. A product greater than one "
            "becomes a negative cycle because logarithms turn products into sums. <bookmark mark='c'/> "
            "The checked example finds yen to pounds to euros and back to yen. <bookmark mark='d'/> Its "
            "gross gain is about half a percent. The implementation uses floating arithmetic and a small "
            "relaxation tolerance, so a nearly zero cycle needs numerical care. <bookmark mark='e'/> This"
            " mathematical detector alone does not establish that a real sequence of trades can be "
            "executed profitably."
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
