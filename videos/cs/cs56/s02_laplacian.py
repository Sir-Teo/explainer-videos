from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def adjacency(n, edges):
    A = np.zeros((n, n))
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def lap(A):
    return np.diag(A.sum(axis=1)) - A


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from hand-placed vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def two_clusters():
    """Two hexagons with two chords each (12 vertices); the bridge (0, 9) joins them."""
    pos, edges = [], []
    for c, off in ((-1.45, 0), (1.45, 6)):
        for k in range(6):
            a = 2 * math.pi * k / 6
            pos.append((c + 0.85 * math.cos(a), 0.85 * math.sin(a)))
        edges += [(off + k, off + (k + 1) % 6) for k in range(6)] + [(off, off + 2), (off + 3, off + 5)]
    return pos, edges


class Laplacian(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrices()
        self.energy()
        self.zero()
        self.connectivity()
        self.spectrum()
        self.normalized()

    def card(self):
        card = chapter_card(1, r"The Laplacian", r"Which matrix sees the shape of a graph?", lit=(1847, 1973),
                            extra=((1847, r"Kirchhoff: \ circuits and spanning trees"),
                                   (1973, r"Fiedler: \ algebraic connectivity")), part=PART)
        with self.voiceover("Chapter one. The Laplacian, the matrix that sees the shape of a graph."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def matrices(self):
        head = label(r"$L = D - A$", font_size=36).to_edge(UP, buff=0.3)
        pos = [(-1.6, 0.7), (-1.6, -0.7), (-0.4, 0.0), (0.8, 0.0), (2.0, 0.0)]
        edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
        g = draw(pos, edges, center=UP * 1.55 + LEFT * 0.2, scale=0.95, r=0.11)
        names = VGroup(*[label(rf"{i + 1}", font_size=18, color=GREY_A).next_to(
            g.pts[i], UP if i != 1 else DOWN, buff=0.12) for i in range(5)])
        A = adjacency(5, edges).astype(int)
        D = np.diag(A.sum(axis=1))
        Lm = D - A
        cfg = {"font_size": 26}

        def mat(M, diag_col, off_col):
            m = Matrix([[str(v) for v in row] for row in M], element_to_mobject_config=cfg, h_buff=0.62,
                       v_buff=0.5)
            for (i, j), e in zip([(i, j) for i in range(5) for j in range(5)], m.get_entries()):
                e.set_color(GREY_D if M[i][j] == 0 else (diag_col if i == j else off_col))
            return m
        mD, mA, mL = mat(D, HEAD, HEAD), mat(A, DATA, DATA), mat(Lm, HEAD, DATA)
        minus, eq = MathTex(r"-", font_size=40), MathTex(r"=", font_size=40)
        VGroup(mD, minus, mA, eq, mL).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.35)
        caps = VGroup(label(r"degrees $D$", font_size=20, color=HEAD).next_to(mD, DOWN, buff=0.15),
                      label(r"adjacency $A$", font_size=20, color=DATA).next_to(mA, DOWN, buff=0.15),
                      label(r"Laplacian $L$", font_size=20, color=WHITE).next_to(mL, DOWN, buff=0.15))
        rowbox = SurroundingRectangle(mL.get_rows()[2], color=HEAD, buff=0.08, stroke_width=2)
        hl = VGroup(g[1][2].copy().set_color(HEAD).scale(1.3),
                    *[g[0][k].copy().set_color(HEAD).set_stroke(width=4) for k in (1, 2, 3)])
        ones = MathTex(r"L\,\mathbf{1} = 0", font_size=34, color=YES).next_to(g, RIGHT, buff=0.9)
        ones_note = label(r"every row sums to zero", font_size=19, color=GREY_A).next_to(ones, DOWN, buff=0.15)
        with self.voiceover(
            "Start with a small graph: five vertices and five edges. <bookmark mark='a'/> Write down two matrices. "
            "The degree matrix, D, has each vertex's number of neighbours on its diagonal. <bookmark mark='b'/> The "
            "adjacency matrix, A, has a one wherever two vertices are joined. <bookmark mark='c'/> Their "
            "difference, D minus A, is the Laplacian of the graph. <bookmark mark='d'/> Read one row, the third "
            "vertex's: its degree, three, on the diagonal, and minus one for each of its three neighbours. "
            "<bookmark mark='e'/> So every row sums to zero, and the Laplacian sends the all-ones vector to zero. "
            "The name comes from physics: the Laplacian at a vertex compares its value with its neighbours' values, "
            "a discrete second derivative, up to sign."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(mD), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeIn(minus), FadeIn(mA), FadeIn(caps[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(mL), FadeIn(caps[2]))
            vo.wait_until("d")
            self.play(Create(rowbox), FadeIn(hl))
            vo.wait_until("e")
            self.play(Write(ones), FadeIn(ones_note))
        self.wait(0.4)
        self.clear_scene()

    def energy(self):
        head = label(r"The quadratic form is an energy", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"(x_i - x_j)^2": HEAD}
        lhs = r"x^{\mathsf T} L x"
        steps = VGroup(
            cmath(lhs, r"=", r"x^{\mathsf T} D x", r"-", r"x^{\mathsf T} A x", font_size=34),
            cmath(lhs, r"=", r"\sum_i d_i x_i^2", r"-", r"2\sum_{(i,j) \in E} x_i x_j", font_size=34),
            cmath(lhs, r"=", r"\sum_{(i,j) \in E}", r"\left(x_i^2 + x_j^2 - 2 x_i x_j\right)", font_size=34),
            cmath(lhs, r"=", r"\sum_{(i,j) \in E}", r"(x_i - x_j)^2", colors=cols, font_size=34),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(LEFT * 3.2 + UP * 0.55)
        for st in steps[1:]:
            st[0].set_opacity(0)
        pos = [(-1.6, 0.7), (-1.6, -0.7), (-0.4, 0.0), (0.8, 0.0), (2.0, 0.0)]
        edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
        smooth, rough = [2, 2, 1, -1, -2], [2, -2, 1, -1, 2]
        centre = RIGHT * 3.9 + UP * 0.7

        def labelled(x):
            g = draw(pos, edges, center=centre, scale=1.15, r=0.13)
            mx = max(abs(v) for v in x)
            for d, v in zip(g[1], x):
                d.set_color(interpolate_color(ManimColor(GREY_C), ManimColor(KERN if v > 0 else DATA), abs(v) / mx))
            for ln, (a, b) in zip(g[0], edges):
                e = (x[a] - x[b]) ** 2
                ln.set_stroke(color=HEAD if e else GREY_D, width=1.5 + 0.7 * e)
            vals = VGroup(*[MathTex(rf"{v:+d}", font_size=24, color=WHITE).next_to(
                g.pts[i], UP if i != 1 else DOWN, buff=0.14) for i, v in enumerate(x)])
            en = sum((x[a] - x[b]) ** 2 for a, b in edges)
            read = label(rf"energy $= {en}$", font_size=24, color=YES if en < 10 else NO).next_to(
                VGroup(g, vals), DOWN, buff=0.35)
            return VGroup(g, vals, read)
        gs, gr = labelled(smooth), labelled(rough)
        spring = wrapped_label(r"each edge a spring; \ $x_i$ the height of vertex $i$; \ $x^{\mathsf T} L x$ the "
                               r"energy in the springs", 5.4, font_size=20, color=GREY_A).next_to(
            steps, DOWN, buff=0.5).align_to(steps, LEFT)
        same = label(r"same values, \ rearranged: \ $\|x\|^2 = 14$ in both", font_size=19,
                     color=GREY_A).next_to(spring, DOWN, buff=0.35).align_to(spring, LEFT)
        ill = note(r"illustrative labellings", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Why this matrix? Because of the number it gives when you put a vector on both sides of it: x "
            "transpose L x, for any labelling x of the vertices by numbers. <bookmark mark='a'/> Split L into its "
            "two parts. <bookmark mark='b'/> The degree part counts each vertex's square once for every edge it "
            "touches; the adjacency part gives twice the product across every edge. <bookmark mark='c'/> Gather "
            "both by edges: each edge brings x i squared, plus x j squared, minus twice their product. "
            "<bookmark mark='d'/> And that is a perfect square. The quadratic form of the Laplacian is the sum, over "
            "the edges, of the squared difference across each edge. <bookmark mark='e'/> Think of each edge as a "
            "spring and of x as the heights of the vertices: this is the energy stored in the springs. A labelling "
            "that changes slowly along the edges stores little energy, seven units here. <bookmark mark='f'/> "
            "The same five values, rearranged so that they jump across edges, store thirty-nine."
        ) as vo:
            self.play(FadeIn(head), Write(steps[0][0]))
            vo.wait_until("a")
            self.play(Write(steps[0][1:]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]))
            self.play(Circumscribe(steps[3][3], color=HEAD))
            vo.wait_until("e")
            self.play(FadeIn(gs), FadeIn(spring), FadeIn(ill))
            vo.wait_until("f")
            self.play(ReplacementTransform(gs, gr), FadeIn(same))
        self.wait(0.4)
        self.clear_scene()

    def zero(self):
        head = label(r"Zero energy means one value per component", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = two_clusters()
        n = 12
        centre = UP * 1.0 + LEFT * 3.0
        g = draw(pos, edges, center=centre, scale=1.0, r=0.11)
        bridge = Line(g.pts[0], g.pts[9], color=HEAD, stroke_width=3)
        facts = VGroup(
            MathTex(r"x^{\mathsf T} L x = \sum_{(i,j)\in E} (x_i - x_j)^2 \ \ge\ 0", font_size=30),
            MathTex(r"0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n", font_size=30, color=HEAD),
            MathTex(r"x^{\mathsf T} L x = 0 \iff x \text{ constant on each component}", font_size=30, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.1 + UP * 1.0)
        if facts.width > 6.6:
            facts.scale_to_fit_width(6.6).move_to(RIGHT * 3.25 + UP * 1.0)
        L0 = lap(adjacency(n, edges))
        L1 = lap(adjacency(n, edges + [(0, 9)]))
        w0, w1 = np.linalg.eigvalsh(L0), np.linalg.eigvalsh(L1)
        nl = NumberLine(x_range=[0, 7, 1], length=10.5, color=GREY_C, include_numbers=False).move_to(DOWN * 2.2)
        ticks = VGroup(*[label(rf"{k}", font_size=17, color=GREY_B).next_to(nl.n2p(k), DOWN, buff=0.12)
                         for k in range(8)])
        nl_cap = label(r"the twelve eigenvalues of $L$", font_size=19, color=GREY_A).next_to(nl, UP, buff=0.55)
        nl_cap.align_to(nl, LEFT)

        def marks(w):
            seen = {}
            ds = VGroup()
            for v in w:
                k = round(float(v), 2)
                seen[k] = seen.get(k, 0) + 1
                ds.add(Dot(nl.n2p(max(float(v), 0)) + UP * 0.2 * seen[k], radius=0.07,
                           color=HEAD if float(v) < 0.5 else DATA))
            return ds
        m0, m1 = marks(w0), marks(w1)
        ind = [interpolate_color(ManimColor(GREY_D), ManimColor(KERN), 1.0 if i < 6 else 0.0) for i in range(n)]
        ind2 = [interpolate_color(ManimColor(GREY_D), ManimColor(KERN), 0.0 if i < 6 else 1.0) for i in range(n)]
        lam2 = label(rf"one bridge: \ $\lambda_2 = {w1[1]:.2f}$", font_size=22, color=HEAD).next_to(
            g, DOWN, buff=0.3)
        ill = note(r"illustrative graph; \ eigenvalues computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "That energy is never negative, so every eigenvalue of the Laplacian is at least zero. "
            "<bookmark mark='a'/> We number them from the smallest: lambda one, which is always zero, with the "
            "all-ones vector, then lambda two, and up to lambda n. <bookmark mark='b'/> When is the energy exactly "
            "zero? Only when no edge has a difference across it: when x is constant on every connected piece of "
            "the graph. <bookmark mark='c'/> This graph has two pieces, and two independent ways to do that: light "
            "up the left piece, <bookmark mark='d'/> or the right one. So zero is an eigenvalue twice. In general, "
            "the number of zero eigenvalues is the number of components. <bookmark mark='e'/> Now add a single "
            "bridge. The graph is connected, one zero eigenvalue rises, and it does not rise far: lambda two is "
            "small, because one edge barely holds the halves together."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]), Create(nl), FadeIn(ticks), FadeIn(nl_cap),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in m0], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(*[d.animate.set_color(c) for d, c in zip(g[1], ind)])
            vo.wait_until("d")
            self.play(*[d.animate.set_color(c) for d, c in zip(g[1], ind2)])
            self.play(Indicate(VGroup(m0[0], m0[1]), color=HEAD))
            vo.wait_until("e")
            self.play(Create(bridge), *[d.animate.set_color(WHITE) for d in g[1]],
                      ReplacementTransform(m0, m1), FadeIn(lam2), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    def connectivity(self):
        head = label(r"$\lambda_2$: \ algebraic connectivity", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        path = [(i, i + 1) for i in range(n - 1)]
        cyc = path + [(n - 1, 0)]
        cube = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]
        comp = [(a, b) for a in range(8) for b in range(a + 1, 8)]
        ring = [(math.cos(2 * math.pi * k / 8 + math.pi / 8), math.sin(2 * math.pi * k / 8 + math.pi / 8))
                for k in range(8)]
        line = [(-1.05 + 0.3 * k, 0.0) for k in range(8)]
        cubepos = []
        for v in range(8):
            s = 1.0 if v & 4 else 0.5
            x = s * (1 if v & 1 else -1)
            y = s * (1 if v & 2 else -1)
            cubepos.append((x, y))
        specs = [(r"path", line, path), (r"cycle", ring, cyc), (r"cube $Q_3$", cubepos, cube),
                 (r"complete $K_8$", ring, comp)]
        tiles = VGroup()
        vals = []
        for k, (nm, ps, es) in enumerate(specs):
            g = draw(ps, es, center=ORIGIN, scale=1.0, r=0.08, sw=1.5)
            lam = float(np.linalg.eigvalsh(lap(adjacency(8, es)))[1])
            vals.append(lam)
            cap = label(nm, font_size=21, color=GREY_A)
            val = MathTex(rf"\lambda_2 = {lam:.2f}" if lam < 7.9 else rf"\lambda_2 = {lam:.0f}", font_size=30,
                          color=interpolate_color(ManimColor(NO), ManimColor(YES), k / 3))
            box = Rectangle(width=2.6, height=2.3, stroke_width=0).move_to(g)
            tiles.add(VGroup(VGroup(box, g), cap, val).arrange(DOWN, buff=0.25))
        tiles.arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.45)
        y_arr = tiles.get_bottom()[1] - 0.3
        arrow = Arrow([tiles.get_left()[0] + 0.4, y_arr, 0], [tiles.get_right()[0] - 0.4, y_arr, 0], buff=0,
                      color=GREY_B, stroke_width=2)
        arr_l = label(r"more edges, \ better connected", font_size=19, color=GREY_A).next_to(arrow, DOWN, buff=0.1)
        side = VGroup(
            wrapped_label(r"$\lambda_2 > 0$ \ exactly when the graph is connected; \ Fiedler \ (1973) \ named it "
                          r"the \textbf{algebraic connectivity}", 6.0, font_size=21, color=WHITE),
            wrapped_label(r"adding an edge never lowers it \ (chapter 2 proves why); \ unless the graph is "
                          r"complete it is at most the vertex connectivity", 6.0, font_size=21, color=GREY_A),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(arr_l, DOWN, buff=0.5)
        with self.voiceover(
            "So lambda two is zero exactly when the graph falls apart, and its size says how firmly the graph holds "
            "together. <bookmark mark='a'/> Here are four graphs on eight vertices, from the sparsest connected one, "
            "a path, through a cycle and a cube, to the complete graph. <bookmark mark='b'/> Their second "
            "eigenvalues climb from about fifteen hundredths to eight. <bookmark mark='c'/> Miroslav Fiedler studied "
            "this number in 1973 and named it the algebraic connectivity. Adding an edge can never lower it, which "
            "the next chapter proves, and unless the graph is complete it is at most the vertex connectivity, the "
            "fewest vertices whose removal disconnects the graph. It is a robust, continuous measure of something "
            "the drawing only hints at."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(t[0], t[1])) for t in tiles], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t[2], shift=UP * 0.1) for t in tiles], lag_ratio=0.3),
                      GrowArrow(arrow), FadeIn(arr_l))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def spectrum(self):
        p = load("partition")
        w = p["eigenvalues"]
        n, m = p["n"], p["edges"]
        sizes = (p["labels"].count(0), p["labels"].count(1))
        head = label(r"Two communities in the spectrum", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 13, 1], y_range=[0, 8, 2], x_length=7.4, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 2.6 + DOWN * 0.35)
        yt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 2, 4, 6, 8)])
        xt = VGroup(*[label(rf"$\lambda_{{{k}}}$", font_size=17, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in (1, 2, 3, 6, 12)])
        bars = VGroup()
        for k, v in enumerate(w, start=1):
            col = HEAD if k <= 2 else DATA
            h = max(0.02, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            bars.add(Rectangle(width=0.36, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                ax.c2p(k, 0) + UP * h / 2))
        gap = BraceBetweenPoints(ax.c2p(1.95, w[1]), ax.c2p(1.95, w[2]), direction=RIGHT, color=YES)
        side = VGroup(
            wrapped_label(rf"{n} vertices, \ {m} edges: \ two planted communities of {sizes[0]} and {sizes[1]}, \ "
                          r"dense inside, \ sparse between", 4.6, font_size=19, color=GREY_A),
            wrapped_label(rf"$\lambda_1 = 0$; \ $\lambda_2 = {w[1]:.2f}$ stands apart; \ the bulk starts at "
                          rf"$\lambda_3 = {w[2]:.2f}$", 4.6, font_size=20, color=HEAD),
            wrapped_label(r"one eigenvalue near zero for each piece the graph almost falls into", 4.6,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 4.05 + DOWN * 0.2)
        cap = label(r"the twelve smallest eigenvalues of $L$, \ computed", font_size=18, color=GREY_A).next_to(
            ax, UP, buff=0.15).align_to(ax, LEFT)
        with self.voiceover(
            "Real graphs rarely fall apart completely, but they often nearly do. <bookmark mark='a'/> This graph "
            "has a hundred and twenty vertices in two planted communities of sixty, with edges dense inside each "
            "community and sparse between. <bookmark mark='b'/> Its twelve smallest eigenvalues: zero, as always; then one "
            "eigenvalue that stands apart, about three; and then the bulk, starting above four and a half. "
            "<bookmark mark='c'/> The pattern generalizes the exact case: a graph that almost falls into k pieces "
            "has k eigenvalues near zero, followed by a gap."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(gap), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def normalized(self):
        s = load("series")
        head = label(r"The normalized Laplacian", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            cmath(r"N", r"=", r"D^{-1/2}", r"L", r"D^{-1/2}", font_size=36),
            cmath(r"N", r"=", r"D^{-1/2}", r"(D - A)", r"D^{-1/2}", font_size=36),
            cmath(r"N", r"=", r"I", r"-", r"D^{-1/2} A D^{-1/2}", font_size=36),
        )
        for st in steps:
            st.move_to(UP * 1.95)
        props = VGroup(
            label(r"eigenvalues between 0 and 2", font_size=24, color=HEAD),
            label(r"as many zeros as components, \ as before", font_size=24, color=YES),
            label(r"every vertex weighted by its degree: \ fair to hubs", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(steps[0], DOWN, buff=0.45)
        if props.width > 13.2:
            props.scale_to_fit_width(13.2)
        rows = [[nm, rf"{r['n']}", rf"{r['edges']:,}", rf"{r['lambda2']:.3f}"] for nm, r in s.items()]
        tab = grid_table([r"graph", r"vertices", r"edges", r"$\lambda_2(N)$"], rows, widths=[4.8, 2.0, 1.8, 2.2],
                         row_h=0.68, font_size=25, mono_cols=())
        tab.next_to(props, DOWN, buff=0.6)
        for c in tab.cells[1:]:
            c[3].set_color(HEAD)
        with self.voiceover(
            "One adjustment makes graphs with very uneven degrees comparable. <bookmark mark='a'/> Scale the "
            "Laplacian on both sides by one over the square root of each degree. <bookmark mark='b'/> Expanding, "
            "this normalized Laplacian is the identity minus a rescaled adjacency matrix. <bookmark mark='c'/> Its "
            "eigenvalues lie between zero and two, its zeros still count the components, and every vertex counts "
            "in proportion to its degree, so a hub cannot dominate. <bookmark mark='d'/> This is the version the "
            "hook measured on the series' own graphs: the city grid of Part 18 barely holds together, while the "
            "internet and the novel's words are far better knit. Cheeger's inequality and random walks, chapters "
            "three and four, are both about this matrix."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0], steps[1]))
            self.play(TransformMatchingTex(steps[1], steps[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in props], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO)
