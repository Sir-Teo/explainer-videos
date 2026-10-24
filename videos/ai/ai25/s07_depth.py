from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (COMM_COLORS, GNN_C, PAIR_C, PART, PLAIN, STRUCT, SYM, load, node_box, take_away,
                                   takeaway_anims)


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.smoothing()
        self.energy()
        self.sweep()
        self.squash()
        self.attention()

    def card(self):
        card = chapter_card(6, r"Deep graph networks", r"Why don't graph networks get deeper?", lit=(), part=PART)
        with self.voiceover("Chapter six. Deep graph networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def smoothing(self):
        cols = {r"\lambda_1": STRUCT, r"\lambda_2": PLAIN}
        rows = [
            cmath(r"\hat A", r"=", r"\sum_i \lambda_i u_i u_i^\top", r",\quad", r"1 = \lambda_1 > |\lambda_2| \ge \dots",
                  font_size=34),
            cmath(r"\hat A^k H", r"=", r"\sum_i \lambda_i^k \, u_i (u_i^\top H)", font_size=34),
            cmath(r"\hat A^k H", r"\to", r"u_1 (u_1^\top H)", r",\quad", r"u_1 \propto \sqrt{\deg}", font_size=34),
            cmath(r"\big\| \hat A^k H - u_1 u_1^\top H \big\|", r"\le", r"|\lambda_2|^k \, \|H\|", font_size=34),
        ]
        rows[3][2].set_color(PLAIN)
        whys = [why(r"symmetric: \ the spectral theorem (Part 3)"), why(r"a power acts on each eigenvalue"),
                why(r"every other $\lambda_i^k \to 0$"), why(r"the slowest term to die")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.5, edge=6.9)
        head = label(r"a layer of a GCN, \ without its weights: \ $H \leftarrow \hat A H$", font_size=28, color=GNN_C)
        head.to_edge(UP, buff=0.3)
        rest = label(r"every node ends with the same features, \ up to its degree: \ \textit{over-smoothing} "
                     r"\ (Li, Han \& Wu 2018; \ Oono \& Suzuki 2020)", font_size=23, color=PLAIN).to_edge(DOWN,
                                                                                                      buff=0.45)
        depth = VGroup(
            VGroup(Rectangle(width=5.4, height=0.3, stroke_width=0, fill_color=STRUCT, fill_opacity=0.8),
                   label(r"image networks: \ up to $152$ layers \ (ResNet, \ Part 9)", font_size=22, color=STRUCT)),
            VGroup(Rectangle(width=5.4 * 4 / 152, height=0.3, stroke_width=0, fill_color=GNN_C, fill_opacity=0.9),
                   label(r"graph networks: \ usually $2$ to $4$", font_size=22, color=GNN_C)),
        )
        for b_ in depth:
            b_[0].move_to([-6.2 + b_[0].width / 2, 0, 0])
            b_[1].next_to(b_[0], RIGHT, buff=0.25)
        depth[0].move_to([depth[0].get_center()[0], -1.95, 0])
        depth[1].move_to([depth[1].get_center()[0], -2.55, 0])
        with self.voiceover(
            "Graph networks are usually shallow, two to four layers; image networks run past a hundred. One reason: strip a "
            "graph convolution of its weights and it is an average over neighbours, applied again and again. <bookmark "
            "mark='a'/> The averaging matrix is symmetric, with orthonormal eigenvectors and eigenvalues at most one. "
            "<bookmark mark='b'/> Applying it k times raises each eigenvalue to the k. <bookmark mark='c'/> Every term but "
            "the first dies away; the first is one pattern on every node, scaled by the square root of its degree. <bookmark "
            "mark='d'/> The rate is the second eigenvalue to the k. <bookmark mark='e'/> Every node ends with the same "
            "features: over-smoothing, named by Qimai Li and colleagues in 2018."
        ) as vo:
            self.play(FadeIn(head))
            self.play(GrowFromEdge(depth[0][0], LEFT), FadeIn(depth[0][1]), GrowFromEdge(depth[1][0], LEFT),
                      FadeIn(depth[1][1]), run_time=1.5)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if k == 3:
                    self.play(FadeOut(depth), run_time=0.6)
                step(k)
            vo.wait_until("e")
            self.play(FadeIn(rest))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        o = load("oversmooth")
        E = np.asarray(o["energy"], float)
        lam2 = float(o["lam2"])
        ks = np.arange(len(E))
        logE = np.log10(np.maximum(E, 1e-30))
        lo = float(np.floor(logE.min())) - 1
        g = axes([0, ks[-1]], [lo, float(np.ceil(logE[0])) + 0.5], x_length=5.6, y_length=3.8,
                 xlabel=r"rounds of averaging, \ $k$", ylabel=r"Dirichlet energy \ (how different neighbours are)",
                 xticks=[0, 16, 32, 48, 64], yticks=list(range(int(lo), int(np.ceil(logE[0])) + 1, 3)),
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-3.2, -0.3, 0])
        cE = curve(g.ax, ks, logE, GNN_C, 3.5)
        k0 = 4
        theory = DashedLine(g.ax.c2p(k0, logE[k0]), g.ax.c2p(ks[-1], logE[k0] + 2 * (ks[-1] - k0) * np.log10(lam2)),
                            color=PLAIN, dash_length=0.08)
        tl = label(rf"slope $\lambda_2^{{2k}}$, \ $\lambda_2 = {lam2:.3f}$", font_size=20, color=PLAIN)
        k_lab = 36
        tl.next_to(g.ax.c2p(k_lab, logE[k0] + 2 * (k_lab - k0) * np.log10(lam2)), UR, buff=0.12)
        y = np.asarray(o["y"])
        show = [str(k) for k in o["show_k"]]
        panels = Group()
        for k in show:
            Z = np.asarray(o["pca"][k], float)
            sc = np.abs(np.asarray(o["pca"]["0"])).max()
            box = Square(1.5, stroke_color=GREY_D, stroke_width=1)
            pts = VGroup(*[Dot(box.get_center() + 0.7 * np.array([z[0], z[1], 0]) / sc, radius=0.018,
                               color=COMM_COLORS[c]) for z, c in zip(Z, y)])
            panels.add(Group(box, pts, label(rf"$k = {k}$", font_size=18, color=GREY_A).next_to(box, DOWN, buff=0.06)))
        panels[:3].arrange(RIGHT, buff=0.15)
        panels[3:].arrange(RIGHT, buff=0.15)
        Group(panels[:3], panels[3:]).arrange(DOWN, buff=0.25).move_to([3.7, -0.1, 0])
        pl = label(r"the nodes' features, \ same scale throughout", font_size=20, color=GREY_A).next_to(panels, UP,
                                                                                                     buff=0.15)
        drop = E[16] / E[0]
        mags = -np.log10(max(drop, 1e-300))
        tag = note(r"computed: \ chapter 4's graph, \ eight random features per node", font_size=20)
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here it is on our three-community graph: the Dirichlet energy, how much neighbours differ, after each round of "
            f"averaging. <bookmark mark='a'/> It falls in a straight line on this log scale, {mags:.0f} powers of ten in "
            f"sixteen rounds, at the rate the second eigenvalue, {lam2:.3f}, predicts. <bookmark mark='b'/> In pictures: the "
            "features start as noise; a few rounds separate the communities, which is why two layers help; many rounds "
            "collapse everything to a point."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            self.play(Create(cE), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(theory), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        o = load("oversmooth")
        depths = list(o["depths"])
        lx = np.log2(depths)
        g = axes([lx[0], lx[-1]], [0.2, 1.0], x_length=6.0, y_length=3.8, xlabel=r"layers",
                 ylabel=r"accuracy on unlabelled nodes", xticks=list(lx), yticks=[1 / 3, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{2 ** v:.0f}", yfmt=lambda v: f"{v:.2f}", center=[-2.4, -0.3, 0])
        chance = DashedLine(g.ax.c2p(lx[0], 1 / 3), g.ax.c2p(lx[-1], 1 / 3), color=GREY_D)
        objs = {}
        stats = {}
        for kind, col in (("plain", PLAIN), ("res", STRUCT)):
            A = np.array([[o[f"{kind}_{d_}_s{s}"]["acc"] for s in (0, 1, 2)] for d_ in depths])
            stats[kind] = A
            objs[kind] = VGroup(band(g.ax, lx, A.min(1), A.max(1), col, 0.22), curve(g.ax, lx, A.mean(1), col, 3.5),
                                VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(lx, A.mean(1))]))
        lg = legend([(PLAIN, r"plain: \ $h \leftarrow \mathrm{relu}(\hat A h W)$"),
                     (STRUCT, r"residual: \ $h \leftarrow h + \mathrm{relu}(\mathrm{LN}(\hat A h W))$")], font_size=20)
        lg.move_to([3.9, 1.6, 0])
        P, R = stats["plain"].mean(1), stats["res"].mean(1)
        collapse = [d_ for d_, a in zip(depths, P) if a < 0.45]
        best = depths[int(np.argmax(P))]
        best_txt = (f"The plain network does best with {best} layers" if best != depths[0] else
                    f"The plain network does best with the fewest, {best} layers")
        col_txt = (f"from {collapse[0]} layers on, the plain network is at chance, about one in three" if collapse
                   else "the plain network weakens with depth but never falls to chance")
        res_txt = (f"The residual network, which adds each layer's output to its input, holds at "
                   f"{100 * R[-1]:.0f} percent at {depths[-1]} layers" if R[-1] > 0.6 else
                   f"Even the residual network falls, to {100 * R[-1]:.0f} percent at {depths[-1]} layers")
        tag = note(r"computed: \ three seeds per point \ (band: \ min--max), \ $300$ training steps", font_size=20)
        tag.to_corner(DR, buff=0.2)
        notes = label(r"with weights, \ the collapse is also \\ an optimization problem: \\ gradients pass back "
                      r"through $64$ averages", font_size=22, color=GREY_B).move_to([4.2, -1.3, 0])
        notes.width = min(notes.width, 5.2)
        with self.voiceover(
            "Now with weights and training: the same task at depths from two to sixty-four, three seeds each. <bookmark "
            f"mark='a'/> {best_txt}; {col_txt}. <bookmark mark='b'/> {res_txt}: the skip connection keeps each node's own "
            "information from being averaged away, the fix that made image networks deep in Part 9. <bookmark mark='c'/> "
            "Part of the collapse is also an optimization problem: gradients must pass back through all those averages."
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(objs["plain"]), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(FadeIn(objs["res"]), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def squash(self):
        levels = 4
        root = np.array([-3.5, 1.8, 0])
        tree = VGroup()
        pts = {(0, 0): root}
        dots = VGroup(Dot(root, radius=0.12, color=PAIR_C))
        for L in range(1, levels + 1):
            n = 2 ** L
            for i in range(n):
                x = root[0] + (i - (n - 1) / 2) * (6.4 / n)
                p = np.array([x, root[1] - 1.05 * L, 0])
                pts[(L, i)] = p
                tree.add(Line(pts[(L - 1, i // 2)], p, color=GREY_D, stroke_width=1.5))
                dots.add(Dot(p, radius=0.06, color=GNN_C))
        cnt = VGroup(*[label(rf"$2^{L} = {2 ** L}$", font_size=20, color=GREY_B).move_to([root[0] + 3.8,
                                                                                         root[1] - 1.05 * L, 0])
                       for L in range(1, levels + 1)])
        txt = VGroup(
            label(r"$L$ hops away: \ up to $(\deg)^L$ nodes", font_size=24, color=GNN_C),
            label(r"all squeezed into one vector \\ of fixed size", font_size=24, color=PLAIN),
            label(r"\textit{over-squashing}: \ Alon \& Yahav (2021); \\ bottlenecks, curvature: \ Topping et al.\ "
                  r"(2022)", font_size=22, color=GREY_B),
            label(r"remedies: \ rewire the graph, \\ add global nodes, \ or attend to everything", font_size=22,
                  color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        txt.move_to([0, 0.3, 0]).align_to(np.array([1.35, 0, 0]), LEFT)
        with self.voiceover(
            "A second problem appears when the answer depends on distant nodes. <bookmark mark='a'/> The nodes within L hops "
            "can grow exponentially, <bookmark mark='b'/> yet all their information must squeeze into one fixed-size vector. "
            "<bookmark mark='c'/> Uri Alon and Eran Yahav called this over-squashing, in 2021; Jake Topping and colleagues "
            "traced it to bottlenecks. <bookmark mark='d'/> Remedies: rewire the graph, add nodes that see everything, or "
            "attend to every node directly."
        ) as vo:
            self.play(FadeIn(dots[0]))
            vo.wait_until("a")
            self.play(Create(tree), FadeIn(dots[1:]), FadeIn(cnt), FadeIn(txt[0]), run_time=2.0)
            vo.wait_until("b")
            pulses = VGroup(*[Dot(pts[(levels, i)], radius=0.07, color=PAIR_C) for i in range(2 ** levels)])
            self.play(FadeIn(pulses))
            self.play(*[p_.animate.move_to(root) for p_ in pulses], run_time=1.5)
            self.play(FadeOut(pulses), Flash(dots[0], color=PAIR_C), FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]))
            vo.wait_until("d")
            self.play(FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        f1 = cmath(r"h_v'", r"=", r"\sum_{u \in N(v)} \alpha_{vu} W h_u", font_size=36).move_to([0, 2.4, 0])
        f2 = cmath(r"\alpha_{vu}", r"=", r"\mathrm{softmax}_u \, \mathrm{LeakyReLU}\big(a^\top [W h_v \,\|\, W h_u]\big)",
                   font_size=34).next_to(f1, DOWN, buff=0.35)
        f1[2].set_color(GNN_C)
        f2[0].set_color(PAIR_C)
        gat = label(r"graph attention (Veli\v{c}kovi\'c et al.\ 2018): \ neighbours weighed, \ not just summed",
                    font_size=22, color=GREY_A).next_to(f2, DOWN, buff=0.25)
        v2 = label(r"GATv2 (Brody, Alon \& Yahav 2022): \ the original's ranking of neighbours is the same for every "
                   r"node; \ moving the nonlinearity inside fixes it", font_size=20, color=GREY_B)
        v2.next_to(gat, DOWN, buff=0.2)
        boxes = VGroup(node_box(r"a transformer \ = \ attention on the complete graph", GNN_C, font_size=22),
                       node_box(r"graph transformers: \ plus the graph's structure, \ as encodings", SYM,
                                font_size=22),
                       node_box(r"AlphaFold's Evoformer: \ attention on pairs, \ biased by triangles", PAIR_C,
                                font_size=22)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Attention is the third idea. <bookmark mark='a'/> Instead of summing its neighbours equally, a node weighs them: "
            "in Petar Veličković's graph attention network of 2018, by a softmax of learned scores. <bookmark mark='b'/> "
            "GATv2, from Shaked Brody and colleagues, fixed a flaw: the original scores ranked neighbours the same way for "
            "every node. <bookmark mark='c'/> A transformer, from Part 13, is this on the complete graph; <bookmark "
            "mark='d'/> graph transformers add the graph back as encodings of where each node sits. <bookmark mark='e'/> And "
            "AlphaFold's core is attention over pairs of residues, biased by triangles: last chapter's pair network, grown up."
        ) as vo:
            self.play(Write(f1))
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(gat))
            vo.wait_until("b")
            self.play(FadeIn(v2))
            vo.wait_until("c")
            self.play(FadeIn(boxes[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(boxes[1], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(boxes[2], shift=UP * 0.1))
        self.wait(0.6)
        tk = take_away(r"deep graph networks: \ averaging washes out, \ bottlenecks squash; \ skips and attention help")
        with self.voiceover(
            "So deep graph networks fight two forces: repeated averaging washes out the differences between nodes, "
            "and bottlenecks squash distant information. Skip connections and attention push back. Next: the "
            "symmetry of space itself."
        ):
            self.play(FadeOut(boxes), FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
