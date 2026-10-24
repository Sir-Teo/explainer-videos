from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (COMM_COLORS, GNN_C, HIST, PAIR_C, PART, PLAIN, STRUCT, SYM, graph_mob, load,
                                   take_away, takeaway_anims)


class Messages(VoiceoverScene):
    def construct(self):
        self.card()
        self.graphs()
        self.mpnn()
        self.history()
        self.replay()

    def card(self):
        card = chapter_card(4, r"Message passing", r"How does a network read a graph?", lit=(), part=PART)
        with self.voiceover("Chapter four. Message passing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def graphs(self):
        w = load("wl")
        m = w["molecules"]
        pos, edges = np.asarray(m["layout"][0]), m["edges"][0]
        g = graph_mob(pos, edges, scale=2.0, center=[-4.4, 0.4, 0], node_r=0.14)
        gl = label(r"decalin: \ $10$ carbon atoms, \ $11$ bonds", font_size=22, color=GREY_A).next_to(g, DOWN,
                                                                                                    buff=0.35)
        n = 10
        A = np.zeros((n, n), int)
        for a, b in edges:
            A[a, b] = A[b, a] = 1
        perm = np.array([3, 7, 0, 9, 5, 1, 8, 2, 6, 4])

        def matrix(M, color):
            cells = VGroup()
            for i in range(n):
                for j in range(n):
                    cells.add(Square(0.31, stroke_width=0.6, stroke_color=GREY_D,
                                     fill_color=color if M[i, j] else "#121722", fill_opacity=0.9 if M[i, j] else 1))
            return cells.arrange_in_grid(n, n, buff=0.02)

        M1 = matrix(A, SYM).move_to([0.5, 0.5, 0])
        Ap = A[np.ix_(perm, perm)]
        M2 = matrix(Ap, SYM).move_to([0.5, 0.5, 0])
        ml = label(r"its adjacency matrix $A$", font_size=22, color=SYM).next_to(M1, DOWN, buff=0.3)
        f = cmath(r"f(PX,\ PAP^\top)", r"=", r"P\,f(X, A)", font_size=34).move_to([4.7, 1.2, 0])
        f[2].set_color(STRUCT)
        fl = label(r"renumber the nodes: \ the answers \\ must be renumbered too, \ nothing else", font_size=22,
                   color=GREY_A).next_to(f, DOWN, buff=0.3)
        ex = label(r"graphs everywhere: \ molecules, \ road maps, \ social networks, \ meshes, \ proteins "
                   r"(residues within $8$\,\AA)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A graph is a set with connections: nodes, and edges between some pairs. Here is decalin, ten carbons and eleven "
            "bonds. <bookmark mark='a'/> A computer stores it as a table, the adjacency matrix, with a one wherever two nodes "
            "are joined. <bookmark mark='b'/> But number the nodes differently and the matrix's rows and columns shuffle, "
            "though the molecule is the same. <bookmark mark='c'/> So a network on graphs must be equivariant to renumbering: "
            "permute the nodes, and its answers permute the same way. <bookmark mark='d'/> Graphs are everywhere: molecules, "
            "road maps, social networks, weather meshes, and proteins, residues joined when close in space."
        ) as vo:
            self.play(FadeIn(g), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(M1), FadeIn(ml))
            vo.wait_until("b")
            self.play(ReplacementTransform(M1, M2), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mpnn(self):
        w = load("wl")
        m = w["molecules"]
        pos, edges = np.asarray(m["layout"][1]), m["edges"][1]
        g = graph_mob(pos, edges, scale=2.1, center=[-4.2, 0.2, 0], node_r=0.15)
        v = 0
        nbrs = [b if a == v else a for a, b in edges if v in (a, b)]
        rows = [
            cmath(r"m_v", r"=", r"\sum_{u \in N(v)} M(h_v, h_u, e_{uv})", font_size=36),
            cmath(r"h_v'", r"=", r"U(h_v, m_v)", font_size=36),
            cmath(r"y", r"=", r"R\Big(\sum_v h_v\Big)", font_size=36),
        ]
        rows[0][2].set_color(STRUCT)
        whys = [why(r"messages from the neighbours, \ summed"), why(r"each node updates its state"),
                why(r"a readout for the whole graph")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=2.1, buff=0.5, edge=6.9)
        proof = label(r"a sum over neighbours doesn't care how they are numbered: \ equivariant, \ by construction",
                      font_size=22, color=STRUCT).to_edge(DOWN, buff=1.05)
        gcn = cmath(r"\text{GCN:}\quad H'", r"=", r"\sigma\big(\hat D^{-1/2} (A + I) \hat D^{-1/2} H W\big)",
                    font_size=30).to_edge(DOWN, buff=0.4)
        pulses = VGroup()
        for u in nbrs:
            pulses.add(Dot(g.pts[u], radius=0.09, color=PAIR_C))
        with self.voiceover(
            "In 2017 Justin Gilmer and colleagues at Google put these networks into one form, message passing. Every node "
            "keeps a state, a vector h. <bookmark mark='a'/> In each layer every node sums messages from its neighbours, a "
            "learned function M of the two states and the edge, <bookmark mark='b'/> then updates its state from the old one "
            "and the sum. <bookmark mark='c'/> After a few layers, a readout sums the states into an answer about the whole "
            "graph. <bookmark mark='d'/> Every step is a sum over neighbours, so the numbering can't matter: equivariant by "
            "construction. <bookmark mark='e'/> The graph convolutional network of Thomas Kipf and Max Welling is the "
            "simplest case: average the neighbours' states, normalized by degree, and apply one weight matrix."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            step(0)
            self.play(*[p.animate.move_to(g.pts[v]) for p in pulses], FadeIn(pulses), run_time=1.2)
            self.play(Flash(g.nodes[v], color=PAIR_C), FadeOut(pulses))
            vo.wait_until("b")
            step(1)
            self.play(g.nodes[v].animate.set_color(STRUCT))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(proof))
            vo.wait_until("e")
            self.play(Write(gcn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1997, r"Sperduti \& Starita", r"networks that read labelled trees and graphs", width=4.2,
                         color=HIST),
            history_card(2005, r"Gori, Monfardini \& Scarselli", r"the graph neural network: \ states updated from "
                         r"neighbours until they settle (2009 in full)", width=4.2, color=HIST),
            history_card(2014, r"Bruna, Zaremba, Szlam \& LeCun", r"convolutions in the graph's spectrum \ (Defferrard "
                         r"et al.\ 2016; \ Kipf \& Welling 2017)", width=4.2, color=HIST),
            history_card(2015, r"Duvenaud et al.", r"learned molecular fingerprints", width=4.2, color=HIST),
            history_card(2017, r"Gilmer et al.", r"message passing; \ on $134{,}000$ small molecules (QM9), \ "
                         r"chemical accuracy on $11$ of $13$ properties", width=4.2, color=HIST),
            history_card(2018, r"Battaglia et al.", r"graph networks: \ relational inductive biases", width=4.2,
                         color=HIST),
        )
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.35)).move_to(DOWN * 0.2)
        head = label(r"Networks on graphs, \ 1997--2018", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The idea is older than its name. <bookmark mark='a'/> In 1997 Alessandro Sperduti and Antonina Starita trained "
            "networks on labelled graphs. <bookmark mark='b'/> In 2005 Marco Gori and colleagues proposed the graph neural "
            "network, its node states updated from their neighbours until they settled. <bookmark mark='c'/> In 2014 Joan "
            "Bruna and colleagues defined convolutions through the graph's spectrum. <bookmark mark='d'/> In 2015 David "
            "Duvenaud and colleagues learned fingerprints of molecules. <bookmark mark='e'/> Gilmer's network then predicted "
            "thirteen quantum properties of small molecules, eleven within chemical accuracy. <bookmark mark='f'/> And Peter "
            "Battaglia and colleagues argued that graphs are the general way to give a network relational structure."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("sbm")
        pos = np.asarray(d["layout"])
        edges = [tuple(e) for e in np.asarray(d["edges"])]
        y = np.asarray(d["y"])
        tr = np.asarray(d["train"]).astype(bool)
        frames = d["frames_gcn"]
        snaps = list(d["snaps"])
        g = graph_mob(pos, edges, colors=[GREY_C] * len(pos), scale=2.9, center=[-3.3, -0.25, 0], node_r=0.055,
                      edge_w=0.6, edge_color=GREY_D, stroke=False)
        for i in np.flatnonzero(tr):
            g.nodes[i].set_color(COMM_COLORS[y[i]]).scale(1.5)
        cnt = label(r"before training", font_size=22, color=GREY_A).next_to(g, UP, buff=0.1)
        cg, cm = np.asarray(d["curve_gcn"]), np.asarray(d["curve_mlp"])
        ax = axes([0, cg[-1, 0]], [0.2, 1.0], x_length=4.6, y_length=2.8, xlabel=r"training step",
                  ylabel=r"accuracy on the unlabelled nodes", xticks=[0, cg[-1, 0]], yticks=[1 / 3, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", center=[3.6, 0.6, 0])
        dot = Dot(ax.ax.c2p(cg[0, 0], cg[0, 1]), color=STRUCT)
        acc_m = [d[f"s{s}"]["mlp"] for s in (0, 1, 2)]
        acc_g = [d[f"s{s}"]["gcn"] for s in (0, 1, 2)]
        res = VGroup(
            label(rf"MLP on the hints alone: \ ${100 * np.mean(acc_m):.0f}\%$ \ "
                  rf"(${100 * min(acc_m):.0f}$--${100 * max(acc_m):.0f}$)", font_size=22, color=PLAIN),
            label(rf"GCN, \ two layers: \ ${100 * np.mean(acc_g):.0f}\%$ \ "
                  rf"(${100 * min(acc_g):.0f}$--${100 * max(acc_g):.0f}$)", font_size=22, color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, DOWN, buff=0.45).align_to(ax, LEFT)
        deg = d["s0"]["deg"]
        intra = d["s0"]["intra"]
        n_lab = int(tr.sum())
        tag = note(rf"computed: \ $300$ nodes, \ $3$ communities, \ ${n_lab}$ labelled; \ three seeds", font_size=20)
        tag.to_corner(DR, buff=0.2)
        if np.mean(acc_g) > 2 * np.mean(acc_m):
            verdict = "Passing messages more than doubles what the hints alone give"
        elif np.mean(acc_g) > np.mean(acc_m) + 0.1:
            verdict = "Passing messages lifts it well above the hints alone"
        else:
            verdict = "Passing messages helps only a little here"
        with self.voiceover(
            "Let's train one. Three hundred people in three communities, friendships mostly within: "
            f"{100 * intra:.0f} percent of the edges, about {deg:.0f} per person. Each person carries only a weak, noisy "
            f"hint of their community, and only {n_lab} are labelled. <bookmark mark='a'/> A two-layer graph convolutional "
            "network learns from those labels and the graph: watch its guesses for everyone else. <bookmark mark='b'/> Each "
            "layer mixes in the neighbours, so two layers see two hops. <bookmark mark='c'/> An MLP that sees only each "
            f"person's own hint gets {100 * np.mean(acc_m):.0f} percent right; the graph network "
            f"{100 * np.mean(acc_g):.0f} percent, over three seeds. {verdict}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cnt), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(dot))
            per = max(0.4, (vo.until("c") - 0.5) / max(1, len(frames)))
            for k, fr in enumerate(frames):
                new = label(rf"after ${snaps[k]}$ steps", font_size=22, color=GREY_A).move_to(cnt)
                idx = np.searchsorted(cg[:, 0], snaps[k])
                idx = min(idx, len(cg) - 1)
                anims = [g.nodes[i].animate.set_color(COMM_COLORS[fr[i]]) for i in range(len(fr)) if not tr[i]]
                self.play(*anims, ReplacementTransform(cnt, new), dot.animate.move_to(ax.ax.c2p(cg[idx, 0], cg[idx, 1])),
                          run_time=0.6 * per)
                cnt = new
                self.wait(0.4 * per)
            self.play(Create(curve(ax.ax, cg[:, 0], cg[:, 1], STRUCT, 3)),
                      Create(curve(ax.ax, cm[:, 0], cm[:, 1], PLAIN, 3)))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.6)
        tk = take_away(r"message passing: \ a sum over neighbours, \ repeated; \ $L$ layers see $L$ hops")
        with self.voiceover(
            "That is message passing: a learned sum over neighbours, repeated, so that after L layers each node has heard "
            "from everything within L hops. What can such a network tell apart?"
        ):
            self.play(FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
