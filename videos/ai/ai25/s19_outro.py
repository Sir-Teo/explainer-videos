from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, CHAIN_GRAD, COMM_COLORS, GNN_C, KIND_COLOR, MIRROR_C, MSA_C, PAIR_C, PART,
                                   PLAIN, PRED_C, SEARCH_C, STRUCT, SYM, TRUE_C, WL_COLORS, chain2d_mob, chain3d,
                                   field_image, graph_mob, load, matrix_image, node_box)


def mini_axes(TW, TH):
    return Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                axis_config={"stroke_color": GREY_D, "include_ticks": False})


def norm(v, lo=None, hi=None):
    v = np.asarray(v, float)
    lo = v.min() if lo is None else lo
    hi = v.max() if hi is None else hi
    return (v - lo) / max(hi - lo, 1e-12)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 2.6, 1.45
        out = []
        e = load("equivariance")
        ax = mini_axes(TW, TH)
        th = norm(e["sweep_theta"])
        allv = np.concatenate([e[f"sweep_energy_{k}"] for k in ("inv", "mlp")])
        out.append((VGroup(ax, curve(ax, th, norm(e["sweep_energy_mlp"], allv.min(), allv.max()), PLAIN, 2.5),
                           curve(ax, th, norm(e["sweep_energy_inv"], allv.min(), allv.max()), STRUCT, 2.5)),
                    r"turn it: \ invariant or not", STRUCT))
        d = load("deepsets")
        ax = mini_axes(TW, TH)
        xs = norm(np.log10(d["sizes"]))
        g = VGroup(ax)
        for k in ("mlp", "mlp_aug", "deepsets"):
            a = np.array([[d[f"{k}_{n}_s{s}"]["acc"] for s in d["seeds"]] for n in d["sizes"]]).mean(1)
            g.add(curve(ax, xs, norm(a, 0.25, 1.0), KIND_COLOR[k], 2.5))
        out.append((g, r"functions of sets", STRUCT))
        w = load("wl")
        m = w["molecules"]
        out.append((VGroup(*[graph_mob(np.asarray(m["layout"][k]), m["edges"][k], [WL_COLORS[c] for c in
                                                                                  m["colors"][-1][k]],
                                       scale=0.55, center=[1.3 * (2 * k - 1), 0, 0], node_r=0.06, edge_w=1.2)
                             for k in (0, 1)]), r"the limit of message passing", GNN_C))
        o = load("oversmooth")
        ax = mini_axes(TW, TH)
        E = np.log10(np.maximum(np.asarray(o["energy"]), 1e-30))
        out.append((VGroup(ax, curve(ax, norm(np.arange(len(E))), norm(E), GNN_C, 2.5)), r"over-smoothing", GNN_C))
        nb = load("nbody")
        ax = mini_axes(TW, TH)
        xs = norm(np.log10(nb["sizes"]))
        allm = np.log10(np.array([[np.mean(nb["table"][k][str(n)]) for n in nb["sizes"]] for k in nb["kinds"]]))
        g = VGroup(ax, *[curve(ax, xs, norm(allm[i], allm.min(), allm.max()), KIND_COLOR[k], 2.5)
                         for i, k in enumerate(nb["kinds"])])
        out.append((g, r"equivariant networks", STRUCT))
        f = load("fold")
        X = np.asarray(f["X"])
        out.append((VGroup(chain3d(X, scale=0.045, center=[-0.65, 0, 0], angle=0.6, tilt=0.5, gradient=CHAIN_GRAD,
                                   width=2, dots=False),
                           chain3d(X * np.array([1, 1, -1]), scale=0.045, center=[0.65, 0, 0], angle=0.6, tilt=0.5,
                                   color=MIRROR_C, width=2, dots=False)), r"distances and the mirror", MIRROR_C))
        p = load("pair")
        out.append((Group(matrix_image(np.asarray(p["ex_true"]), 1.35), matrix_image(np.asarray(p["ex_triangle"]),
                                                                                     1.35)).arrange(RIGHT, buff=0.15),
                    r"triangle updates", PAIR_C))
        dd = load("diffusion")
        S = np.asarray(dd["egnn_s0"]["samples"])[:3]
        out.append((VGroup(*[chain2d_mob(P, scale=0.22, center=[0.85 * (k - 1), 0, 0], color=STRUCT, width=1.8,
                                         dot_r=0.025) for k, P in enumerate(S)]), r"diffusion over atoms", STRUCT))
        wt = load("weather")
        out.append((Group(field_image(np.asarray(wt["show_truth"])[3], 1.35),
                          field_image(np.asarray(wt["multimesh"]["show"])[3], 1.35)).arrange(RIGHT, buff=0.15),
                    r"weather on a mesh", MSA_C))
        fo = load("fno")
        ax = mini_axes(TW, TH)
        xs = norm(np.log2(fo["test_res"]))
        g = VGroup(ax)
        for k in ("fno", "cnn"):
            a = np.array([np.mean([fo[f"{k}_s{s}"]["err"][str(r)] for s in (0, 1, 2)]) for r in fo["test_res"]])
            g.add(curve(ax, xs, np.minimum(norm(a, 0, 0.5), 1.0), KIND_COLOR[k], 2.5))
        out.append((g, r"operators, \ any resolution", STRUCT))
        ma = load("materials")
        ax = mini_axes(TW, TH)
        xs = np.asarray(ma["sys_x"])
        Ev = np.asarray(ma["sys_E"])
        H = np.asarray(ma["sys_hull"])
        lo, hi = min(Ev.min(), H[:, 1].min()), max(Ev.max(), 0.05)
        g = VGroup(ax, *[Dot(ax.c2p(a, (b - lo) / (hi - lo)), radius=0.025, color=MSA_C if s else GREY_B)
                         for a, b, s in zip(xs, Ev, ma["sys_stable"])],
                   VMobject(stroke_color=PAIR_C, stroke_width=2).set_points_as_corners(
                       [ax.c2p(a, (b - lo) / (hi - lo)) for a, b in H]))
        out.append((g, r"crystals on the hull", MSA_C))
        b = load("binpack")
        ax = mini_axes(TW, TH)
        hist = b["s0"]["history"]
        sc = np.array([h_["score"] for h_ in hist])
        out.append((VGroup(ax, curve(ax, norm(np.arange(len(sc))), norm(sc, sc.min() - 0.5, sc.max() + 0.5),
                                     SEARCH_C, 2.5)), r"discovery by search", SEARCH_C))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.2)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=3, cols=4, buff=(0.2, 0.22)).move_to(DOWN * 0.35)
        if tiles.height > 6.4:
            tiles.height = 6.4
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, \ in twelve pictures", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. A symmetry is a transformation that shouldn't change the answer, and a network can "
            "respect it exactly, by construction, or approximately, from examples. Sums make functions of sets; "
            "sums over neighbours make graph networks, which see exactly what colour refinement sees, and lose "
            "detail when stacked too deep. Building rotations in made our molecule model far better with the same "
            "data. AlphaFold reads a protein through pairs kept consistent by triangles, builds it from frames, "
            "scores it with a loss that knows left from right, and its successor hands the atoms to diffusion. "
            "The weather runs on a mesh; equations are learned as operators; crystals are screened by the "
            "million; and in mathematics, where the checker is perfect, search discovers."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"search with an exact checker", [26, 28]),
            (r"learned simulators of the world", [29]),
            (r"what networks represent inside", [30]),
            (r"blind tests, \ saturated benchmarks", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. <bookmark mark='a'/> Search guided by a network and judged by an exact checker "
            "is AlphaZero, next time, and the reasoning models of Part 28. <bookmark mark='b'/> A learned simulator "
            "that rolls the world forward, like our mesh network, is the world model of Part 29. <bookmark "
            "mark='c'/> What the layers of a network represent, and whether its features respect the symmetries "
            "we expect, is the subject of Part 30. <bookmark mark='d'/> And CASP's blind tests, and an olympiad "
            "that machines have nearly saturated, lead into Part 31's question of how to evaluate at all."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for k, mk in enumerate("bcd", 1):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that a composition of $G$-equivariant maps is $G$-equivariant, \ and that an invariant map applied "
            r"after equivariant layers makes the whole network invariant.",
            r"Deep Sets: \ number a countable universe by $c(x) \in \{1, 2, \dots\}$. \ Show that $X \mapsto \sum_{x "
            r"\in X} 4^{-c(x)}$ is one-to-one on finite sets. \ What goes wrong for multisets, \ and how does a larger "
            r"base fix it for multiplicities below the base?",
            r"Show that colour refinement gives every node of a $d$-regular graph the same colour at every round, \ "
            r"and conclude that no message-passing network can tell a $6$-cycle from two triangles.",
            r"For a connected graph, \ show that $\hat A = D^{-1/2}(A + I)D^{-1/2}$ has top eigenvalue $1$ with "
            r"eigenvector $\propto D^{1/2}\mathbf 1$, \ and that $\hat A^k X$ converges to the projection of $X$ onto "
            r"it.",
            r"EGNN: \ show that $x_i' = x_i + C\sum_j (x_i - x_j)\,\phi(\|x_i - x_j\|^2)$ satisfies "
            r"$x'(Rx + t) = R\,x'(x) + t$ for every orthogonal $R$. \ Is it then blind to reflections?",
            r"Fourier layer: \ show that $v \mapsto \mathcal F^{-1}[R_k \hat v_k]$ commutes with shifts of the "
            r"periodic grid, \ and that the same $R_k$ define the layer on any grid with more than $2k_{\max}$ points.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from equivariant compositions to the Fourier layer. Pause here and work "
            "through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 26, \ Reinforcement Learning", font_size=40).to_edge(UP, buff=0.45)
        tree = {"children": [{"children": [{"children": []}, {"children": []}]},
                             {"children": [{"children": []}, {"children": [{"children": []}, {"children": []}]},
                                           {"children": []}], "color": SEARCH_C},
                             {"children": [{"children": []}]}]}
        st = SearchTree(tree, width=5.6, level_height=1.1, radius=0.12, center=[-3.2, -0.6, 0])
        path = st.path_to(len(st.nodes) - 2)
        loop = VGroup(node_box(r"an agent acts", STRUCT, font_size=24), node_box(r"the world answers: \ a reward",
                                                                                  PAIR_C, font_size=24))
        loop.arrange(DOWN, buff=0.9).move_to([3.6, -0.2, 0])
        la = CurvedArrow(loop[0].get_right(), loop[1].get_right(), angle=-1.6, color=GREY_B, stroke_width=3)
        lb = CurvedArrow(loop[1].get_left(), loop[0].get_left(), angle=-1.6, color=GREY_B, stroke_width=3)
        sch = note(r"schematic", font_size=20).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Next time, the fifth act: agency. The search loop of this chapter, propose, check, keep the best, "
            "becomes learning from reward: an agent acts, the world answers, and the agent improves, all the way "
            "to AlphaZero, which we will train ourselves. Part 26: reinforcement learning, from Bellman to AlphaZero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sch))
            self.play(Create(st.edge_group), FadeIn(st.nodes), run_time=1.5)
            self.play(*[st.nodes[i].animate.set_color(SEARCH_C) for i in path],
                      *[st.edges[i].animate.set_color(SEARCH_C).set_stroke(width=4) for i in path if st.edges[i]])
            self.play(FadeIn(loop), Create(la), Create(lb), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"M.~M.~Bronstein, J.~Bruna, T.~Cohen \& P.~Veli\v{c}kovi\'c, \textit{Geometric Deep Learning: Grids, "
             r"Groups, Graphs, Geodesics, and Gauges} (2021)",
             r"W.~L.~Hamilton, \textit{Graph Representation Learning} (2020)",
             r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 13",
             r"P.~Lynch, \textit{The Emergence of Numerical Weather Prediction} (2006)"],
            [r"Zaheer et al.\ (2017); \ Qi et al.\ (2017); \ Wagstaff et al.\ (2019); \ Weisfeiler \& Leman (1968); \ "
             r"Babai (2016); \ Xu et al.\ (2019); \ Morris et al.\ (2019); \ Maron et al.\ (2019); \ Sato et al.\ (2021)",
             r"Sperduti \& Starita (1997); \ Gori et al.\ (2005); \ Scarselli et al.\ (2009); \ Bruna et al.\ (2014); \ "
             r"Duvenaud et al.\ (2015); \ Kipf \& Welling (2017); \ Gilmer et al.\ (2017); \ Battaglia et al.\ (2018); "
             r"\ Veli\v{c}kovi\'c et al.\ (2018); \ Brody et al.\ (2022); \ Li, Han \& Wu (2018); \ Oono \& Suzuki "
             r"(2020); \ Alon \& Yahav (2021); \ Topping et al.\ (2022)",
             r"Sch\"utt et al.\ (2017); \ Thomas et al.\ (2018); \ Satorras, Hoogeboom \& Welling (2021); \ Batzner et "
             r"al.\ (2022); \ Batatia et al.\ (2022)",
             r"Anfinsen (1961, 1973); \ Levinthal (1969); \ Moult et al.\ (1995); \ Marks et al.\ (2011); \ Morcos et "
             r"al.\ (2011); \ Senior et al.\ (2020); \ Jumper et al.\ (2021); \ Baek et al.\ (2021); \ Abramson et "
             r"al.\ (2024)",
             r"Kuhlman et al.\ (2003); \ Dauparas et al.\ (2022); \ Watson et al.\ (2023); \ Krishna et al.\ (2025)",
             r"Richardson (1922); \ Charney, Fj\o rtoft \& von Neumann (1950); \ Bauer, Thorpe \& Brunet (2015); \ "
             r"Lam et al.\ (2023); \ Price et al.\ (2024); \ Lang et al.\ (2024); \ Li et al.\ (2021); \ Lu et al.\ "
             r"(2021); \ Pathak et al.\ (2022)",
             r"Merchant et al.\ (2023); \ Cheetham \& Seshadri (2024); \ Szymanski et al.\ (2023); \ Leeman et al.\ "
             r"(2024); \ Zeni et al.\ (2025)",
             r"Trinh et al.\ (2024); \ Chervonyi et al.\ (2025); \ Hubert et al.\ (2025); \ Romera-Paredes et al.\ "
             r"(2024); \ Novikov et al.\ (2025); \ Dumas, Pernet \& Sedoglavic (2025); \ Georgiev et al.\ (2025); \ "
             r"Feng et al.\ (2026); \ Sim, Renau \& Hart (2025); \ Strassen (1969); \ Winograd (1971)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "To go deeper, Bronstein, Bruna, Cohen and Veličković's book on geometric deep learning is the map of "
            "this whole part, and William Hamilton's short book covers graph networks clearly. Thanks for watching, "
            "and see you in Part 26."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
