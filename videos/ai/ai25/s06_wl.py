from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, GNN_C, PAIR_C, PART, PLAIN, STRUCT, SYM, WL_COLORS, graph_mob, load,
                                   take_away, takeaway_anims, words_num)


def circle_layout(parts):
    """Unions of cycles drawn as rings side by side."""
    pos, k, x = [], 0, -1.0
    total = sum(parts)
    for L in parts:
        r = 0.18 + 0.55 * L / total
        x += r + 0.12
        for i in range(L):
            a = 2 * np.pi * i / L + np.pi / 2
            pos.append((x + r * np.cos(a), r * np.sin(a)))
        x += r + 0.12
        k += L
    P = np.array(pos)
    return P - P.mean(0)


class WL(VoiceoverScene):
    def construct(self):
        self.card()
        self.refine()
        self.theorem()
        self.aggregators()
        self.cycles()
        self.beyond()

    def card(self):
        card = chapter_card(5, r"What message passing can't see", r"Which graphs look the same to a graph network?",
                            lit=(), part=PART)
        with self.voiceover("Chapter five. What message passing can't see."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def refine(self):
        w = load("wl")
        m = w["molecules"]
        cols = m["colors"]
        gs = []
        for k, cx in ((0, -3.4), (1, 3.4)):
            pos = np.asarray(m["layout"][k])
            g = graph_mob(pos, m["edges"][k], colors=[WL_COLORS[c] for c in cols[0][k]], scale=1.45,
                          center=[cx, 0.85, 0], node_r=0.14)
            gs.append(g)
        names = VGroup(label(r"decalin", font_size=26, color=GREY_A).next_to(gs[0], UP, buff=0.3),
                       label(r"bicyclopentyl", font_size=26, color=GREY_A).next_to(gs[1], UP, buff=0.3))
        algo = definition_card(r"colour refinement (1-WL)", r"every node starts with the same colour; \ each round, "
                               r"a node's new colour names its old colour and the multiset of its neighbours' "
                               r"colours; \ stop when nothing splits", width=6.2, font_size=21, kind=r"Algorithm")
        algo.to_edge(DOWN, buff=0.15)

        def hist(k, r):
            cnt = np.bincount(cols[r][k], minlength=max(max(c) for c in cols[r]) + 1)
            items = VGroup()
            for c, nn in enumerate(cnt):
                if nn:
                    items.add(VGroup(Dot(radius=0.09, color=WL_COLORS[c]), MathTex(rf"\times {nn}", font_size=24))
                              .arrange(RIGHT, buff=0.08))
            return items.arrange(RIGHT, buff=0.25)

        rl = label(r"round $0$", font_size=24, color=GREY_A).move_to([0, 2.6, 0])
        h0 = VGroup(hist(0, 0).next_to(gs[0], DOWN, buff=0.35), hist(1, 0).next_to(gs[1], DOWN, buff=0.35))
        rounds = len(cols)
        same = not any(m["differ"])
        verdict = ("At every round the two molecules have exactly the same colours in the same numbers, so the "
                   "test says they might be the same graph" if same else "The colour counts differ, so the test "
                   "tells them apart")
        tag = note(r"computed", font_size=20).to_corner(UR, buff=0.25)
        with self.voiceover(
            "In 1968 Boris Weisfeiler and Andrei Leman described colour refinement, the standard first test of whether two "
            "graphs are the same up to numbering. <bookmark mark='a'/> Every node starts with one colour. <bookmark "
            "mark='b'/> Each round, a node's new colour names its old colour and its neighbours' colours: here the carbons "
            "with three neighbours split off. <bookmark mark='c'/> Then their neighbours, until nothing changes. Different "
            f"colour counts mean different graphs. <bookmark mark='d'/> Decalin and bicyclopentyl, {rounds - 1} rounds: "
            f"{verdict}. Yet one is two six-rings sharing an edge, the other two five-rings joined by a bond."
        ) as vo:
            self.play(FadeIn(gs[0]), FadeIn(gs[1]), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(algo), FadeIn(rl), FadeIn(h0))
            per = max(0.6, vo.until("d") / max(1, rounds - 1))
            for r in range(1, rounds):
                nr = label(rf"round ${r}$", font_size=24, color=GREY_A).move_to(rl)
                nh = VGroup(hist(0, r).next_to(gs[0], DOWN, buff=0.35), hist(1, r).next_to(gs[1], DOWN, buff=0.35))
                anims = []
                for k in (0, 1):
                    anims += [d_.animate.set_color(WL_COLORS[c % len(WL_COLORS)]) for d_, c in
                              zip(gs[k].nodes, cols[r][k])]
                self.play(*anims, ReplacementTransform(rl, nr), ReplacementTransform(h0, nh), run_time=0.8)
                rl, h0 = nr, nh
                self.wait(max(0.2, per - 0.8))
            vo.wait_until("d")
            self.play(Indicate(h0[0]), Indicate(h0[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        th = theorem_card(r"message passing $\le$ 1-WL", r"if colour refinement gives two nodes the same colour after "
                          r"$t$ rounds, \ every message-passing network gives them the same state after $t$ layers; "
                          r"\ GIN, \ $h_v \leftarrow \mathrm{MLP}\big((1 + \epsilon) h_v + \sum_{u \in N(v)} h_u\big)$,"
                          r" \ distinguishes exactly what 1-WL does", who=r"Xu, Hu, Leskovec \& Jegelka (2019); "
                          r"Morris et al.\ (2019)", width=11.6, color=STRUCT).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"c^{t}_v = c^{t}_w", r"\Rightarrow", r"h^{t}_v = h^{t}_w", font_size=32),
            cmath(r"c^{t+1}_v = c^{t+1}_w", r"\Rightarrow", r"c^t_v = c^t_w, \ \{\!\{c^t_u\}\!\}_{N(v)} = "
                  r"\{\!\{c^t_u\}\!\}_{N(w)}", font_size=32),
            cmath(r"c^{t+1}_v = c^{t+1}_w", r"\Rightarrow", r"h^t_v = h^t_w, \ \{\!\{h^t_u\}\!\}_{N(v)} = "
                  r"\{\!\{h^t_u\}\!\}_{N(w)}", font_size=32),
            cmath(r"c^{t+1}_v = c^{t+1}_w", r"\Rightarrow", r"h^{t+1}_v = h^{t+1}_w", font_size=32),
        ]
        whys = [why(r"the claim, \ by induction on $t$ \ ($t = 0$: \ all equal)"),
                why(r"a new colour names the old one \ and the neighbours' multiset"),
                why(r"the induction hypothesis, \ node by node"),
                why(r"a layer is a function of exactly these")]
        step = ladder(self, rows, whys, keep=4, top=0.9, x=-1.6, buff=0.45, edge=6.9)
        with self.voiceover(
            "And no message-passing network can do better. Keyulu Xu and colleagues, and Christopher Morris and colleagues, "
            "proved in 2019: if colour refinement can't separate two nodes after t rounds, no message-passing network "
            "separates them after t layers. <bookmark mark='a'/> By induction: at the start, everything is equal. <bookmark "
            "mark='b'/> Two nodes with the same colour next round had the same colour and the same multiset of neighbours' "
            "colours; <bookmark mark='c'/> by hypothesis, then, the same state and the same multiset of neighbours' states, "
            "<bookmark mark='d'/> from which a layer computes identical new states. <bookmark mark='e'/> And the bound is "
            "reached: a sum followed by an MLP, the graph isomorphism network, separates everything colour refinement does."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.1))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("e")
            self.play(Indicate(th, color=STRUCT, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aggregators(self):
        gi = load("gin")
        A = VGroup(*[Dot(radius=0.14, color=c) for c in (SYM, SYM, PAIR_C, PAIR_C)]).arrange(RIGHT, buff=0.15)
        B = VGroup(*[Dot(radius=0.14, color=c) for c in (SYM, PAIR_C)]).arrange(RIGHT, buff=0.15)
        A.move_to([-4.6, 1.0, 0])
        B.move_to([-4.6, -0.1, 0])
        la = label(r"neighbours $\{\!\{a, a, b, b\}\!\}$", font_size=26).next_to(A, RIGHT, buff=0.3)
        lb = label(r"neighbours $\{\!\{a, b\}\!\}$", font_size=26).next_to(B, RIGHT, buff=0.3)
        ops = VGroup(
            label(r"mean: \ the same; \ max: \ the same; \ sum: \ different", font_size=26, color=GREY_A),
        ).move_to([-2.6, -1.3, 0])
        rows = []
        for agg, col in (("sum", STRUCT), ("mean", PLAIN), ("max", PLAIN)):
            rm = [gi[f"deg_{agg}_s{s}"]["rmse"] for s in (0, 1, 2)]
            ex = [gi[f"deg_{agg}_s{s}"]["exact"] for s in (0, 1, 2)]
            rows.append((agg, col, float(np.mean(rm)), float(np.mean(ex))))
        tab = VGroup(label(r"learn each node's degree, \ starting from identical nodes:", font_size=24,
                           color=GREY_A))
        for agg, col, rm, ex in rows:
            tab.add(label(rf"{agg}: \ error ${rm:.2f}$, \ exactly right ${100 * ex:.0f}\%$", font_size=27, color=col))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.2, 0])
        sd = gi["deg_std"]
        tag = note(rf"computed: \ $400$ random graphs of $12$ nodes, \ three seeds; \ the degrees' own spread is "
                   rf"${sd:.2f}$", font_size=20).to_corner(DR, buff=0.25)
        sum_rm, mean_rm, max_rm = rows[0][2], rows[1][2], rows[2][2]
        with self.voiceover(
            "Why a sum? Aggregation must not lose information about the multiset of neighbours. <bookmark mark='a'/> "
            "Neighbours a, a, b, b and neighbours a, b have the same mean and the same maximum; only the sum differs. "
            "<bookmark mark='b'/> Computed: give every node of a random graph the same features, and ask a one-layer network "
            f"for each node's degree. A sum gets within {sum_rm:.2f}. <bookmark mark='c'/> A mean or a maximum, "
            f"{mean_rm:.2f} and {max_rm:.2f}, hardly better than the spread of the degrees, {sd:.2f}: to them every node "
            "with a neighbour looks alike."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(ops))
            vo.wait_until("b")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycles(self):
        gi = load("gin")
        exs = gi["examples"]
        gs = VGroup()
        for k, ex in enumerate(exs):
            pos = circle_layout(ex["parts"])
            g = graph_mob(pos, [tuple(e) for e in ex["edges"]], scale=1.25, node_r=0.07, edge_w=1.6)
            lab = label(r"triangle: \ yes" if 3 in ex["parts"] else r"triangle: \ no", font_size=20,
                        color=PAIR_C if 3 in ex["parts"] else GREY_B).next_to(g, DOWN, buff=0.15)
            gs.add(VGroup(g, lab))
        gs.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.5)
        base = gi["base_rate"]
        acc = {k: [gi[f"{k}_s{s}"]["acc"] for s in (0, 1, 2)] for k in ("gin", "gin_rni", "pair")}
        spread = max(gi[f"gin_s{s}"]["spread"] for s in (0, 1, 2))
        seeds_txt = lambda k: r", \ ".join(rf"${100 * a:.1f}\%$" for a in acc[k])  # noqa: E731
        res = VGroup(
            label(rf"base rate \ (always say \textit{{yes}}): \ ${100 * base:.1f}\%$", font_size=21, color=GREY_B),
            VGroup(label(r"GIN:", font_size=22, color=GNN_C), label(seeds_txt("gin"), font_size=22, color=GNN_C)),
            VGroup(label(r"GIN, \ random numbers on the nodes:", font_size=22, color=AUG),
                   label(seeds_txt("gin_rni"), font_size=22, color=AUG)),
            VGroup(label(r"a network on pairs of nodes:", font_size=22, color=STRUCT),
                   label(seeds_txt("pair"), font_size=22, color=STRUCT)),
        )
        for r_ in res[1:]:
            r_.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.75, -1.55, 0])
        res_h = label(r"test accuracy, \ three seeds", font_size=20, color=GREY_A).next_to(res, UP, buff=0.2)
        res_h.align_to(res, LEFT)
        cv = {k: np.asarray(gi[f"{k}_s0"]["curve"]) for k in ("gin", "gin_rni", "pair")}
        top = max(float(c_[-1, 0]) for c_ in cv.values())
        g = axes([0, top], [0.5, 1.0], x_length=5.4, y_length=2.5, xlabel=r"training step (seed $0$)",
                 ylabel=r"held-out", xticks=[0, top / 2, top], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=18, center=[-3.4, -1.75, 0])
        base_l = DashedLine(g.ax.c2p(0, base), g.ax.c2p(top, base), color=GREY_D)
        lines = {k: curve(g.ax, cv[k][:, 0], np.clip(cv[k][:, 1], 0.5, 1.0), c_, 3)
                 for k, c_ in (("gin", GNN_C), ("gin_rni", AUG), ("pair", STRUCT))}
        n = gi["n_nodes"]
        gin_exact = spread < 1e-6
        gin_line = (f"Every graph gets exactly the same output, to the last digit, so GIN can do no better than "
                    f"always answering yes: {100 * np.mean(acc['gin']):.1f} percent, the base rate." if gin_exact else
                    f"GIN's outputs barely differ between graphs: {100 * np.mean(acc['gin']):.1f} percent.")
        learned = [a for a in acc["gin_rni"] if a > base + 0.1]
        nl = len(learned)
        if nl == 0:
            rni_line = ("Giving every node a few random numbers breaks the symmetry in principle, but in our budget "
                        "GIN never learned to use them: it stayed at the base rate in all three seeds.")
        elif nl == 3:
            rni_line = ("Giving every node a few random numbers breaks the symmetry: in all three seeds GIN learned "
                        f"to find the triangles, {100 * min(learned):.1f} percent or better.")
        else:
            rni_line = ("Giving every node a few random numbers breaks the symmetry in principle, but it is hard to "
                        f"learn: {words_num(nl)} of three seeds got there, {100 * max(learned):.1f} percent, the "
                        "others stayed at the base rate.")
        p_ok = [a for a in acc["pair"] if a > base + 0.1]
        if len(p_ok) == 3:
            pair_line = (f"sees triangles directly: {100 * min(p_ok):.1f} percent or better, in every seed, and its "
                         "training curve leaves the base rate within a few hundred steps")
        elif p_ok:
            pair_line = (f"can see triangles directly: {words_num(len(p_ok))} of three seeds reached "
                         f"{100 * max(p_ok):.1f} percent, though the others stayed at the base rate")
        else:
            pair_line = "can see triangles in principle, though in our budget it never learned to"
        tag = note(rf"computed: \ $2{{,}}000$ training graphs, \ $600$ test, \ {n} nodes each, \ three seeds",
                   font_size=18).to_corner(DR, buff=0.15)
        with self.voiceover(
            f"Now make a network fail on purpose. Graphs of {n} nodes that are unions of cycles: is there a triangle? "
            "<bookmark mark='a'/> To colour refinement they are all identical: every node has two neighbours, whose "
            "neighbours have two neighbours, forever. So every message-passing network must answer the same for all of them. "
            f"<bookmark mark='b'/> {gin_line} <bookmark mark='c'/> {rni_line} <bookmark mark='d'/> A network whose features "
            f"live on pairs of nodes, updating each pair through every third node, {pair_line}. Remember that construction: "
            "it is the heart of AlphaFold."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g_) for g_ in gs], lag_ratio=0.3), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(base_l), FadeIn(res_h), FadeIn(res[0]))
            vo.wait_until("b")
            self.play(Create(lines["gin"]), FadeIn(res[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines["gin_rni"]), FadeIn(res[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(lines["pair"]), FadeIn(res[3]), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        w = load("wl")
        rp, rs = int(w["random_pairs"]), int(w["random_separated"])
        gp, gsep = int(w["regular_pairs"]), int(w["regular_separated"])
        facts = VGroup(
            label(rf"random graphs, \ $10$ nodes: \ colour refinement separates ${rs}$ of ${rp}$ different pairs",
                  font_size=24, color=STRUCT),
            label(rf"random graphs where every node has $3$ neighbours: \ ${gsep}$ of ${gp}$", font_size=24,
                  color=PLAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6)
        ways = VGroup(
            node_box_(r"$k$-WL: \ colour $k$-tuples of nodes \ (cost $n^k$)", SYM),
            node_box_(r"count small subgraphs \ (triangles, cycles)", PAIR_C),
            node_box_(r"positional encodings: \ random numbers, \ Laplacian eigenvectors", AUG),
            node_box_(r"graph transformers: \ attention over all pairs", GNN_C),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.45)).move_to(DOWN * 0.3)
        babai = label(r"telling graphs apart in general: \ Babai (2016), \ quasi-polynomial time", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        tk = take_away(r"message passing sees what colour refinement sees: \ almost every graph, \ but not all")
        with self.voiceover(
            "How bad is it in practice? On random graphs, hardly at all: colour refinement separated "
            f"{rs} of {rp} different pairs. <bookmark mark='a'/> On graphs where every node has three neighbours, {gsep} of "
            f"{gp}. <bookmark mark='b'/> The fixes add what a neighbour sum can't build: colouring tuples of nodes, at a cost "
            "growing as n to the k; counting triangles and other patterns; positions; or attention over every pair. "
            "<bookmark mark='c'/> Graph isomorphism itself is not known to be easy or hard; László Babai showed in 2016 that "
            "quasi-polynomial time suffices."
        ) as vo:
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in ways], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(babai))
        self.play(FadeOut(babai), FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(1.0)
        self.clear_scene()


def node_box_(text, color):
    from videos.ai.ai25.common import node_box

    return node_box(text, color, font_size=25, height=0.95)
