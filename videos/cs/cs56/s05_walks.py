from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.compute import load as load18
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def adjacency(n, edges):
    A = np.zeros((n, n))
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from hand-placed vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def toy():
    """Two hexagons with two chords each (12 vertices), joined by two parallel bridges."""
    pos, edges = [], []
    for c, off in ((-1.45, 0), (1.45, 6)):
        for k in range(6):
            a = 2 * math.pi * k / 6
            pos.append((c + 0.85 * math.cos(a), 0.85 * math.sin(a)))
        edges += [(off + k, off + (k + 1) % 6) for k in range(6)] + [(off, off + 2), (off + 3, off + 5)]
    return pos, edges + [(0, 9), (1, 8)]


def masses(pts, p, color=HEAD, k=0.55):
    """A distribution drawn as discs on the vertices, area proportional to probability."""
    return VGroup(*[Circle(radius=0.04 + k * math.sqrt(max(float(v), 0.0)), stroke_width=0, fill_color=color,
                           fill_opacity=0.75).move_to(q) for q, v in zip(pts, p)])


class Walks(VoiceoverScene):
    def construct(self):
        self.card()
        self.walk()
        self.lazy()
        self.modes()
        self.bound()
        self.measured()
        self.pagerank()

    def card(self):
        card = chapter_card(4, r"Random walks and mixing", r"How fast does a random walk forget where it started?",
                            lit=(1906, 1998), extra=((1906, r"Markov: \ chains"),
                                                     (1998, r"Brin and Page: \ PageRank")), part=PART)
        with self.voiceover("Chapter four. Random walks, and how fast they mix."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def walk(self):
        head = label(r"A walk forgets where it started", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = toy()
        n = 12
        A = adjacency(n, edges)
        d = A.sum(axis=1)
        P = A / d[:, None]
        g = draw(pos, edges, center=LEFT * 3.3 + UP * 0.6, scale=1.0, r=0.06, color=GREY_B)
        p = np.zeros(n)
        p[3] = 1.0
        dists = [p]
        for _ in range(14):
            dists.append(dists[-1] @ P)
        pi = d / d.sum()
        mass = masses(g.pts, dists[0])
        tl = label(r"$t = 0$", font_size=24, color=HEAD).next_to(g, DOWN, buff=0.4)
        steps = VGroup(
            cmath(r"p_{t+1}", r"=", r"p_t", r"D^{-1} A", font_size=32),
            cmath(r"(\pi D^{-1} A)_j", r"=", r"\sum_i \frac{d_i}{2m} \cdot \frac{A_{ij}}{d_i}", font_size=32),
            cmath(r"(\pi D^{-1} A)_j", r"=", r"\sum_i \frac{A_{ij}}{2m}", r"=", r"\frac{d_j}{2m}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 3.4 + UP * 0.9)
        steps[2][4].set_color(YES)
        whys = VGroup(label(r"each step: \ split your mass equally among your neighbours", font_size=18,
                            color=GREY_B),
                      label(r"try $\pi_i = d_i / 2m$ \ ($m$ edges)", font_size=18, color=GREY_B),
                      label(r"$\pi$ is \textbf{stationary}: \ one step leaves it unchanged", font_size=18,
                            color=YES))
        for w, s in zip(whys, steps):
            w.next_to(s, DOWN, buff=0.1).align_to(s, LEFT)
        pmass = masses(g.pts, pi, color=YES)
        pil = label(r"$\pi$: \ mass in proportion to degree", font_size=21, color=YES).move_to(tl)
        ill = note(r"illustrative graph; \ distributions computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Put a walker on a vertex and let it step to a random neighbour, again and again, and follow the "
            "probability of where it is. <bookmark mark='a'/> At each step every vertex "
            "splits its probability equally among its neighbours: multiply by D inverse A. <bookmark mark='b'/> "
            "Start with all the mass on one vertex at the far left, and watch it spread: first through its own "
            "cluster, then, slowly, across the two bridges. <bookmark mark='c'/> Where does it settle? Try giving "
            "each vertex mass proportional to its degree, d i over twice the number of edges. "
            "<bookmark mark='d'/> One step sends each neighbour exactly its share back, and the degrees "
            "reappear: this distribution does not change. It is stationary, and on a connected graph that is not "
            "bipartite, every start converges to it."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(mass), FadeIn(tl))
            for t in range(1, 15):
                self.play(Transform(mass, masses(g.pts, dists[t])),
                          Transform(tl, label(rf"$t = {t}$", font_size=24, color=HEAD).move_to(tl)), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            self.play(Transform(mass, pmass), Transform(tl, pil), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    def lazy(self):
        head = label(r"Bipartite graphs, \ and the lazy walk", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        pos = [(1.35 * math.cos(2 * math.pi * k / n + math.pi / 2), 1.35 * math.sin(2 * math.pi * k / n + math.pi / 2))
               for k in range(n)]
        edges = [(k, (k + 1) % n) for k in range(n)]
        A = adjacency(n, edges)
        P = A / A.sum(axis=1)[:, None]
        W = 0.5 * (np.eye(n) + P)
        g = draw(pos, edges, center=LEFT * 4.1 + UP * 0.4, r=0.06, color=GREY_B)
        p = np.zeros(n)
        p[0] = 1.0
        simple, lazy = [p], [p]
        for _ in range(12):
            simple.append(simple[-1] @ P)
            lazy.append(lazy[-1] @ W)
        mass = masses(g.pts, p, k=0.45)
        tl = label(r"simple walk, \ $t = 0$", font_size=22, color=NO).next_to(g, DOWN, buff=0.4)
        steps = VGroup(
            cmath(r"W", r"=", r"\tfrac12\,(I + D^{-1} A)", font_size=32),
            cmath(r"D^{1/2} W D^{-1/2}", r"=", r"\tfrac12\,(I + D^{-1/2} A D^{-1/2})", font_size=32),
            cmath(r"D^{1/2} W D^{-1/2}", r"=", r"\tfrac12\,(I + I - N)", font_size=32),
            cmath(r"D^{1/2} W D^{-1/2}", r"=", r"I - \tfrac12 N", font_size=32),
            MathTex(r"1 = \mu_1 \ \ge\ \mu_2 = 1 - \tfrac{\gamma}{2} \ \ge\ \cdots \ \ge\ \mu_n \ \ge\ 0",
                    font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(RIGHT * 2.4 + UP * 0.25)
        gam = label(r"$\gamma = \lambda_2(N)$: \ the \textbf{spectral gap}", font_size=21, color=HEAD).next_to(
            steps, DOWN, buff=0.35).align_to(steps, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> On a bipartite graph, such as this cycle of eight, the walker "
            "alternates sides: all the mass on the even vertices, then all on the odd ones, for ever. It never "
            "settles. <bookmark mark='b'/> The cure is laziness. At each step, stay put with probability one half, "
            "and otherwise move. Now the mass spreads and settles. <bookmark mark='c'/> Conjugate the lazy walk by "
            "the square root of the degrees: <bookmark mark='d'/> what appears "
            "is one half of the identity plus the rescaled adjacency matrix, which is the identity minus half of "
            "the normalized Laplacian. <bookmark mark='e'/> So the lazy walk's eigenvalues are one minus half of "
            "N's: all between zero and one, the top one exactly one, and the next one minus half of lambda two, "
            "the spectral gap."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(FadeIn(mass), FadeIn(tl))
            for t in range(1, 6):
                self.play(Transform(mass, masses(g.pts, simple[t], k=0.45)),
                          Transform(tl, label(rf"simple walk, \ $t = {t}$", font_size=22, color=NO).move_to(tl)),
                          run_time=0.6)
            vo.wait_until("b")
            self.play(Transform(mass, masses(g.pts, lazy[0], k=0.45)),
                      Transform(tl, label(r"lazy walk, \ $t = 0$", font_size=22, color=YES).move_to(tl)),
                      Write(steps[0]))
            for t in range(1, 13):
                self.play(Transform(mass, masses(g.pts, lazy[t], k=0.45, color=YES)),
                          Transform(tl, label(rf"lazy walk, \ $t = {t}$", font_size=22, color=YES).move_to(tl)),
                          run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]))
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]), FadeIn(gam))
        self.wait(0.4)
        self.clear_scene()

    def modes(self):
        head = label(r"Every mode decays; \ the gap decays last", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = toy()
        n = 12
        A = adjacency(n, edges)
        d = A.sum(axis=1)
        N = np.eye(n) - A / np.sqrt(np.outer(d, d))
        nu = np.linalg.eigvalsh(N)
        mu = 1 - nu / 2
        t = ValueTracker(0)
        base = DOWN * 1.9
        width = 0.55

        def bars():
            g = VGroup()
            for i, m in enumerate(mu):
                h = 3.0 * (1.0 if i == 0 else max(float(m), 0.0) ** t.get_value())
                col = YES if i == 0 else (HEAD if i == 1 else DATA)
                g.add(Rectangle(width=width * 0.8, height=max(h, 0.005), stroke_width=0, fill_color=col,
                                fill_opacity=0.85).move_to(base + RIGHT * (i - 5.5) * width * 1.6 + UP * h / 2))
            return g
        bar_m = always_redraw(bars)
        names = VGroup(*[MathTex(rf"\mu_{{{i + 1}}}", font_size=22, color=GREY_B).move_to(
            base + RIGHT * (i - 5.5) * width * 1.6 + DOWN * 0.3) for i in range(n)])
        rule = Line(base + LEFT * 5.2, base + RIGHT * 5.2, color=GREY_C, stroke_width=1.5)
        tl = always_redraw(lambda: label(rf"$t = {t.get_value():.0f}$", font_size=26, color=WHITE).to_corner(
            UR, buff=0.5).shift(DOWN * 0.6))
        keys = VGroup(label(r"$\mu_1 = 1$: \ the stationary part, \ which stays", font_size=19, color=YES),
                      label(rf"$\mu_2 = 1 - \gamma/2 = {mu[1]:.3f}$: \ the slowest mode", font_size=19, color=HEAD),
                      label(r"the rest shrink like $\mu_i^t$, \ faster", font_size=19, color=DATA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.5).shift(DOWN * 0.6)
        ill = note(r"the lazy walk on the two-bridge graph; \ eigenvalues computed", font_size=16).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Here is why the gap sets the speed. <bookmark mark='a'/> Write the starting distribution in the "
            "eigenvectors of the lazy walk. Each step multiplies the component along the i-th eigenvector by mu i. "
            "The first component, with mu one equal to one, is the stationary distribution itself, and it stays. "
            "<bookmark mark='b'/> Run the walk, and every other component decays geometrically. "
            "<bookmark mark='c'/> The last to go is the second, which shrinks by only one minus half "
            "the spectral gap per step. On this graph the two bridges make the gap small, so that one mode, the "
            "imbalance between the two clusters, lingers long after the rest have gone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(names), FadeIn(bar_m), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(keys), FadeIn(tl))
            vo.wait_until("b")
            self.play(t.animate.set_value(8), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(40), run_time=6, rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    def bound(self):
        head = label(r"Mixing time from the spectral gap", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"\|p - \pi\|_{\mathrm{TV}} = \tfrac12 \sum_i |p_i - \pi_i|", font_size=28, color=GREY_A),
            MathTex(r"t_{\mathrm{mix}} = \min\{t : \|p_t - \pi\|_{\mathrm{TV}} \le \tfrac14\ \text{from every start}\}",
                    font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        rhs = r"\tfrac12 \sqrt{1/\pi_{\min}}"
        steps = VGroup(
            cmath(r"\|p_t - \pi\|_{\mathrm{TV}}", r"\le", rhs, r"\left(1 - \tfrac{\gamma}{2}\right)^{t}",
                  font_size=32),
            cmath(r"\|p_t - \pi\|_{\mathrm{TV}}", r"\le", rhs, r"e^{-\gamma t / 2}", font_size=32),
            cmath(r"t_{\mathrm{mix}}", r"\le", r"\frac{1}{\gamma}", r"\ln \frac{4}{\pi_{\min}}", font_size=32),
            cmath(r"t_{\mathrm{mix}}", r"\ge", r"\left(\frac{2}{\gamma} - 1\right)", r"\ln 2", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(defs, DOWN, buff=0.55).align_to(defs, LEFT)
        steps[2][2].set_color(HEAD)
        steps[3][2].set_color(HEAD)
        whys = VGroup(
            wrapped_label(r"every mode but $\pi$ shrinks by $1 - \gamma/2$ a step; \ Cauchy--Schwarz turns the "
                          r"degree-weighted length into total variation, \ at a cost $\sqrt{1/\pi_{\min}}$", 5.0,
                          font_size=18, color=GREY_B),
            label(r"$1 - x \le e^{-x}$", font_size=18, color=GREY_B),
            label(r"set it to $\tfrac14$ and solve for $t$", font_size=18, color=GREY_B),
            wrapped_label(r"and the slow mode itself cannot be hidden: \ a lower bound \ (Levin, \ Peres and "
                          r"Wilmer's textbook)", 5.0, font_size=18, color=GREY_B),
        )
        for w, s in zip(whys, steps):
            w.next_to(s, RIGHT, buff=0.5)
        if whys.get_right()[0] > 6.8:
            shift = whys.get_right()[0] - 6.8
            for w in whys:
                w.shift(LEFT * shift)
        punch = wrapped_label(r"mixing time $\approx 1/\gamma$, \ up to a logarithm: \ the spectral gap \textbf{is} "
                              r"the speed of mixing", 12.4, font_size=23, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Measure the distance from stationarity by total "
            "variation, half the sum of the differences, and define the mixing time as the first step at which that "
            "distance is at most a quarter, from any start. <bookmark mark='b'/> Every mode except the stationary one "
            "shrinks by at least one minus half the gap per step, and Cauchy–Schwarz converts the result into total "
            "variation, at the cost of the square root of one over the smallest stationary probability. "
            "<bookmark mark='c'/> One minus x is at most e to the minus x, <bookmark mark='d'/> so the walk mixes "
            "within one over the gap, times the logarithm of four over that smallest probability. "
            "<bookmark mark='e'/> And the slowest mode forces at least about two over the gap steps, times the "
            "logarithm of two. <bookmark mark='f'/> So, up to a logarithm, the mixing "
            "time is one over the spectral gap."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2], shift=DOWN * 0.1), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3], shift=DOWN * 0.1), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(punch))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        m = load("mixing")
        head = label(r"Four graphs, \ 64 vertices each", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 300, 50], y_range=[-4, 0, 1], x_length=5.4, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 3.6 + DOWN * 0.45)
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (-4, -2, 0)])
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -4), DOWN, buff=0.1)
                      for v in (0, 100, 200, 300)])
        xl = label(r"steps of the lazy walk", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"distance from stationarity \ (TV, \ computed)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.3).align_to(ax, LEFT)
        quarter = DashedLine(ax.c2p(0, math.log10(0.25)), ax.c2p(300, math.log10(0.25)), color=GREY_B,
                             stroke_width=1.5)
        ql = label(r"$\tfrac14$", font_size=18, color=GREY_B).next_to(quarter, RIGHT, buff=0.08)
        cols = {"cycle": NO, "grid": KERN, "random 4-regular": YES, "barbell": LAM}

        def curve(vals, col, dashed=False):
            pts = [ax.c2p(t, math.log10(v)) for t, v in enumerate(vals) if 1e-4 <= v <= 1.0]
            c = VMobject(color=col, stroke_width=2.5 if not dashed else 2).set_points_as_corners(pts)
            return DashedVMobject(c, num_dashes=40) if dashed else c
        curves = VGroup(*[curve(v["tv"], cols[k]) for k, v in m.items()])
        bounds = VGroup(*[curve(m[k]["bound"], cols[k], dashed=True) for k in ("grid", "random 4-regular")])
        rows, rcols = [], []
        for k, v in m.items():
            g = v["gap"]
            up = math.ceil(math.log(4 * v["bound"][0]) / -math.log(1 - g / 2))
            lo = math.ceil((2 / g - 1) * math.log(2))
            meas = rf"{v['t_mix']}" if v["t_mix"] is not None else r"$> 300$"
            rows.append([k, rf"{v['edges']}", rf"{g:.4f}", rf"{lo:,}", meas, rf"{up:,}"])
            rcols.append([cols[k], WHITE, HEAD, GREY_A, YES, GREY_A])
        tab = grid_table([r"graph", r"edges", r"gap $\gamma$", r"lower", r"$t_{\mathrm{mix}}$", r"upper"], rows,
                         widths=[2.0, 0.85, 1.05, 0.85, 0.8, 0.85], row_h=0.55, font_size=18, colors=rcols,
                         mono_cols=())
        tab.move_to(RIGHT * 3.55 + UP * 0.9)
        side = VGroup(
            wrapped_label(r"dashed: \ the upper bound's curve for the grid and the random graph", 6.2,
                          font_size=18, color=GREY_A),
            wrapped_label(r"every measured mixing time lies between the two bounds; \ the barbell's single bridge, "
                          r"a tiny conductance, \ gives a tiny gap \ (chapter 3)", 6.2, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Now measure. Four graphs on sixty-four vertices: a cycle, an eight by eight grid, a random graph in "
            "which every vertex has four neighbours, and a barbell, two dense cliques joined by a single edge. "
            "<bookmark mark='a'/> Start a lazy walk at one vertex of each. <bookmark mark='b'/> The random graph mixes in fifteen steps and the grid in fifty-one; "
            "the cycle and the barbell are still far away after three hundred. <bookmark mark='c'/> Their spectral "
            "gaps tell the same story before any walking is done, and every mixing time we could measure falls "
            "between the two bounds. <bookmark mark='d'/> The barbell's gap is the smallest of all, though it has the most "
            "edges: one bridge is a cut of tiny conductance, and by Cheeger's inequality, a tiny conductance "
            "forces a tiny gap."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl), Create(quarter),
                      FadeIn(ql))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      *[FadeIn(VGroup(*r[:2])) for r in tab.cells[1:]])
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(*[FadeIn(r[4]) for r in tab.cells[1:]])
            vo.wait_until("c")
            self.play(*[FadeIn(VGroup(r[2], r[3], r[5])) for r in tab.cells[1:]], Create(bounds), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(Indicate(tab.cells[4][2], color=LAM), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def pagerank(self):
        pr = load18("pagerank")
        res = pr["residuals"]
        k = len(res)
        rate = (res[-1] / res[0]) ** (1 / (k - 1))
        head = label(r"PageRank, \ revisited", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 55, 10], y_range=[-13, 1, 4], x_length=6.4, y_length=4.3, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 3.0 + DOWN * 0.4)
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (-12, -8, -4, 0)])
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -13), DOWN, buff=0.1)
                      for v in (0, 25, 50)])
        xl = label(r"power-iteration step", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"change per step \ (Part 18's run)", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        line = VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [ax.c2p(i + 1, math.log10(r)) for i, r in enumerate(res)])
        guide = DashedVMobject(VMobject(color=NO, stroke_width=2).set_points_as_corners(
            [ax.c2p(i + 1, max(math.log10(res[0]) + i * math.log10(0.85), -13)) for i in range(k)]), num_dashes=30)
        gl = label(r"$0.85^k$: \ the guarantee", font_size=18, color=NO).next_to(ax.c2p(30, -1.2), UP, buff=0.1)
        dl = label(rf"measured: \ about ${rate:.2f}$ per step", font_size=18, color=DATA).next_to(
            ax.c2p(16, -11.5), RIGHT, buff=0.1)
        steps = VGroup(
            MathTex(r"G = 0.85\, P + 0.15\, \tfrac{1}{n} \mathbf{1}\mathbf{1}^{\mathsf T}", font_size=30),
            MathTex(r"|\mu_2(G)| \le 0.85", font_size=30, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.9 + UP * 1.6).to_edge(RIGHT, buff=2.2)
        side = VGroup(
            wrapped_label(r"follow a random link with probability 0.85, \ else jump anywhere \ (Brin and Page, \ "
                          r"1998)", 4.9, font_size=19, color=GREY_A),
            wrapped_label(r"Haveliwala and Kamvar \ (2003): \ no other eigenvalue exceeds the damping factor; \ the "
                          r"jump guarantees a gap", 4.9, font_size=19, color=YES),
            wrapped_label(rf"Part 18's random web: \ {pr['n']:,} pages, \ {pr['m']:,} links; \ {k} steps to "
                          r"$10^{-12}$", 4.9, font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(steps, DOWN, buff=0.4).align_to(steps, LEFT)
        with self.voiceover(
            "PageRank, from Part 18, is a random walk with a restart. <bookmark mark='a'/> With probability "
            "eighty-five hundredths the surfer follows a random link; otherwise it jumps to a page chosen "
            "uniformly. <bookmark mark='b'/> The jump buys a spectral gap: Taher "
            "Haveliwala and Sepandar Kamvar showed in 2003 that no other eigenvalue of this matrix is larger in "
            "size than the damping factor. So power iteration's error shrinks by at least that factor every "
            "step. <bookmark mark='c'/> On Part 18's random web of twenty thousand pages, the change per step fell "
            "faster still, by about fifty-eight hundredths a step, reaching ten to the minus twelve in fifty-two "
            "steps. Random links make a graph that mixes fast: the next chapter's expanders."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(side[1]), Create(guide), FadeIn(gl))
            vo.wait_until("c")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(dl), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
