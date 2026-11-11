from __future__ import annotations

import random
from collections import deque

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, load


def laplacian_of(n, edges, w=None):
    L = np.zeros((n, n))
    for k, (a, b) in enumerate(edges):
        c = 1.0 if w is None else w[k]
        L[a, a] += c
        L[b, b] += c
        L[a, b] -= c
        L[b, a] -= c
    return L


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def ladder(steps, whys, buff=0.26):
    """A derivation: each line with its grey reason under it, the pairs stacked flush left."""
    pairs = VGroup(*[VGroup(s_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for s_, w_ in zip(steps, whys)])
    return pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def cg_iterates(L, b, kmax):
    """Plain conjugate gradients from x = 0; the iterates x_0, x_1, ... until the residual vanishes."""
    x = np.zeros(len(b))
    r = b.copy()
    p = r.copy()
    out = [x.copy()]
    for _ in range(kmax):
        Ap = L @ p
        a = (r @ r) / (p @ Ap)
        x = x + a * p
        r2 = r - a * Ap
        out.append(x.copy())
        if np.linalg.norm(r2) < 1e-10 * np.linalg.norm(b):
            break
        p = r2 + (r2 @ r2) / (r @ r) * p
        r = r2
    return out


def grid_edges(w, h):
    idx = {(x, y): x * h + y for x in range(w) for y in range(h)}
    E = []
    for x in range(w):
        for y in range(h):
            if x + 1 < w:
                E.append((idx[(x, y)], idx[(x + 1, y)]))
            if y + 1 < h:
                E.append((idx[(x, y)], idx[(x, y + 1)]))
    return idx, E


def tree_path(n, T, a, b):
    nb = {i: [] for i in range(n)}
    for u, v in T:
        nb[u].append(v)
        nb[v].append(u)
    par = {a: None}
    q = deque([a])
    while q:
        u = q.popleft()
        for v in nb[u]:
            if v not in par:
                par[v] = u
                q.append(v)
    path = [b]
    while path[-1] != a:
        path.append(par[path[-1]])
    return path


class Solvers(VoiceoverScene):
    def construct(self):
        self.card()
        self.krylov()
        self.precondition()
        self.foster()
        self.sampling()
        self.resistances()
        self.trees()

    def card(self):
        card = chapter_card(9, r"Laplacian solvers and sparsifiers", r"How fast can we solve $Lx = b$?",
                            lit=(2004, 2008), extra=((2004, r"Spielman and Teng: \ nearly-linear solver"),
                                                     (2008, r"Spielman and Srivastava: \ sparsifiers")), part=PART)
        with self.voiceover("Chapter nine. Laplacian solvers, and the sparse graphs that make them fast."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ each iteration sees one hop further
    def krylov(self):
        head = label(r"Each iteration sees one hop further", font_size=36).to_edge(UP, buff=0.3)
        n = 20
        E = [(i, i + 1) for i in range(n - 1)]
        L = laplacian_of(n, E)
        b = np.zeros(n)
        b[0], b[-1] = 1.0, -1.0
        xs = cg_iterates(L, b, 40)
        ev = np.linalg.eigvalsh(L)
        kappa = ev[-1] / ev[1]
        sp = 0.6
        base_y = -1.75
        xs_pos = [(-sp * (n - 1) / 2 + sp * i) for i in range(n)]
        line = Line([xs_pos[0], base_y, 0], [xs_pos[-1], base_y, 0], color=GREY_D, stroke_width=2)
        dots = VGroup(*[Dot([x, base_y, 0], radius=0.06, color=GREY_B) for x in xs_pos])
        unit = 0.14

        def bars(x):
            g = VGroup()
            for xp, val in zip(xs_pos, x):
                h = max(abs(val) * unit, 0.001)
                col = KERN if val > 0 else DATA
                g.add(Rectangle(width=0.36, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    [xp, base_y + (h / 2 if val > 0 else -h / 2), 0]))
            return g
        cur = bars(xs[0])
        k_lab = label(r"iteration $k = 0$", font_size=22, color=HEAD).move_to([xs_pos[2], base_y + 1.55, 0])
        cap = label(r"a path of 20 vertices; \ $b = e_1 - e_{20}$; \ bars: \ the iterate $x_k$", font_size=18,
                    color=GREY_A).move_to([xs_pos[14], base_y + 1.55, 0])
        steps = VGroup(
            cmath(r"x_k", r"\in", r"\mathrm{span}\{\, b,\ Lb,\ L^2 b,\ \dots,\ L^{k-1} b \,\}", font_size=30),
            cmath(r"(L^j b)_u \ne 0", r"\ \Rightarrow\ ", r"u \text{ within } j \text{ hops of } s \text{ or } t",
                  font_size=30),
            cmath(r"\text{iterations}", r"\approx", r"\sqrt{\kappa}\,\log(1/\varepsilon)", r",\qquad",
                  r"\kappa = \lambda_n / \lambda_2", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 1.6 + UP * 1.85)
        steps[2][2].set_color(HEAD)
        side = VGroup(
            label(r"one multiplication by $L$ per step: \ $O(m)$ work", font_size=18, color=GREY_B),
            label(rf"this path: \ $\kappa = {kappa:.0f}$, \ and {len(xs) - 1} steps to the exact answer",
                  font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(steps, RIGHT, buff=0.4).align_to(steps, UP)
        if side.get_right()[0] > 6.85:
            VGroup(steps, side).shift(LEFT * (side.get_right()[0] - 6.85))
        ill = note(r"illustrative path; \ iterates computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Everything that follows needs to solve L x equals b fast. Gaussian elimination costs cubic time and, "
            "as Part 52 showed, fills a sparse matrix in. Conjugate gradients do better. "
            "<bookmark mark='a'/> The k-th iterate is built from b, L b, L squared b and so on: k multiplications "
            "by L. <bookmark mark='b'/> And L to the j times b is non-zero only within j hops. "
            "<bookmark mark='c'/> Watch it on a path, with current in at one end and out at the other. The answer "
            "is a straight ramp, but each iteration extends it by one vertex from each end. <bookmark mark='d'/> "
            "In general the iterations grow like the square root of the condition number, the largest eigenvalue "
            "over lambda two. Long, thin graphs are badly conditioned; expanders are not."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(dots), FadeIn(cap), FadeIn(k_lab))
            vo.wait_until("a")
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.add(cur)
            for k in range(1, len(xs)):
                self.play(Transform(cur, bars(xs[k])),
                          Transform(k_lab, label(rf"iteration $k = {k}$", font_size=22, color=HEAD).move_to(k_lab)),
                          run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(side), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ preconditioning by a sparsifier
    def precondition(self):
        d = load("solver")
        head = label(r"Precondition with a sparser graph", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            cmath(r"(1 - \varepsilon)\, L_G", r"\preceq", r"L_H", r"\preceq", r"(1 + \varepsilon)\, L_G",
                  font_size=32),
            cmath(r"(1 - \varepsilon)\, x^{\mathsf T} L_G x", r"\le", r"x^{\mathsf T} L_H x", r"\le",
                  r"(1 + \varepsilon)\, x^{\mathsf T} L_G x", r"\quad \text{for all } x", font_size=28),
            cmath(r"\text{eigenvalues of } L_H^{+} L_G", r"\in",
                  r"\Big[\tfrac{1}{1 + \varepsilon},\ \tfrac{1}{1 - \varepsilon}\Big]", font_size=28),
        )
        steps[0][2].set_color(YES)
        steps[1][2].set_color(YES)
        whys = VGroup(
            label(r"$H$ is a \textbf{spectral sparsifier} of $G$", font_size=18, color=GREY_B),
            label(r"every energy, \ hence every cut, \ is kept within $1 \pm \varepsilon$", font_size=18,
                  color=GREY_B),
            label(r"so conjugate gradients preconditioned by $H$ needs few iterations", font_size=18, color=YES),
        )
        lad = ladder(steps, whys, buff=0.3).to_edge(LEFT, buff=0.45).shift(UP * 0.7)
        edges = bar_chart([d["edges"], d["sparsifier_edges"]], [r"$G$", r"$H$"], [DATA, YES], height=2.0,
                          bar_w=0.75, gap=0.6, fmt_=lambda v: f"{v:,.0f}", font_size=20)
        iters = bar_chart([d["cg_iters"], d["pcg_iters"]], [r"plain", r"with $H$"], [NO, YES], height=2.0,
                          bar_w=0.75, gap=0.6, fmt_=lambda v: f"{v:.0f}", font_size=20)
        ct = VGroup(label(r"edges", font_size=20, color=GREY_A), label(r"CG iterations", font_size=20,
                                                                       color=GREY_A))
        charts = VGroup(VGroup(ct[0], edges).arrange(DOWN, buff=0.25),
                        VGroup(ct[1], iters).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        charts.move_to(RIGHT * 4.2 + DOWN * 1.65)
        facts = wrapped_label(rf"$G$: \ {d['n']} vertices, \ a grid plus many weak random edges; \ "
                              rf"$\kappa = {d['kappa_L']:.1f}$. \ On 200 random $x$, \ "
                              rf"$x^{{\mathsf T}} L_H x / x^{{\mathsf T}} L_G x$ \ lay in "
                              rf"$[{d['ratio_min']:.3f},\ {d['ratio_max']:.3f}]$", 5.6, font_size=19,
                              color=GREY_A).next_to(lad, DOWN, buff=0.45).align_to(lad, LEFT)
        caveat = note(r"computed; \ $H$ applied through its pseudo-inverse, \ for illustration", font_size=16)
        caveat.to_corner(DR, buff=0.25)
        with self.voiceover(
            "The cure for bad conditioning is preconditioning: solve with a nearby matrix that is easier, and let "
            "conjugate gradients correct the difference. <bookmark mark='a'/> For Laplacians, the natural nearby "
            "matrix is the Laplacian of a sparser graph H, whose quadratic form stays within one plus or minus "
            "epsilon of G's <bookmark mark='b'/> for every vector x at once: every energy, and so every cut. "
            "Spielman and Teng called such an H a spectral sparsifier. <bookmark mark='c'/> Then the preconditioned "
            "system has all its eigenvalues near one. <bookmark mark='d'/> Our test graph has three hundred vertices "
            "and thirteen thousand six hundred and fifty-seven edges. Its sparsifier keeps one thousand five "
            "hundred and ninety-one, and conjugate gradients drop from sixty-seven iterations to fourteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts), FadeIn(charts[0]))
            self.play(FadeIn(charts[1]), FadeIn(caveat))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ which edges matter: Foster's theorem
    def foster(self):
        head = label(r"Which edges matter? \ Their resistance says", font_size=36).to_edge(UP, buff=0.3)
        k = 8
        E = [(a, b) for a in range(k) for b in range(a + 1, k)]
        E += [(a + k, b + k) for a in range(k) for b in range(a + 1, k)]
        E += [(0, k)]
        n = 2 * k
        Lp = np.linalg.pinv(laplacian_of(n, E))
        R = [Lp[a, a] + Lp[b, b] - 2 * Lp[a, b] for a, b in E]
        pos = []
        for c in (-1.0, 1.0):
            for j in range(k):
                ang = np.pi * (0 if c > 0 else 1) + 2 * np.pi * j / k
                pos.append((c * 1.75 + 0.95 * np.cos(ang), 0.95 * np.sin(ang)))
        g = draw(pos, E, center=LEFT * 3.6 + UP * 0.55, scale=0.95, r=0.07, ecolor=GREY_D, sw=1.5)
        rmax = max(R)
        for ln, r in zip(g[0], R):
            ln.generate_target()
            ln.target.set_stroke(color=interpolate_color(ManimColor(GREY_D), ManimColor(HEAD), r / rmax),
                                 width=1.2 + 4 * r / rmax)
        reads = VGroup(label(rf"bridge: \ $R_{{\mathrm{{eff}}}} = {R[-1]:.2f}$", font_size=20, color=HEAD),
                       label(rf"inside a clique: \ $R_{{\mathrm{{eff}}}} = {R[0]:.2f}$", font_size=20, color=GREY_A),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, DOWN, buff=0.4)
        cols = {r"n - 1": YES}
        steps = VGroup(
            cmath(r"\sum_e w_e R_e", r"=", r"\sum_e w_e\, b_e^{\mathsf T} L^{+} b_e", font_size=30),
            cmath(r"\sum_e w_e R_e", r"=", r"\mathrm{tr}\Big(L^{+} \sum_e w_e\, b_e b_e^{\mathsf T}\Big)",
                  font_size=30),
            cmath(r"\sum_e w_e R_e", r"=", r"\mathrm{tr}\big(L^{+} L\big)", r"=", r"n - 1", colors=cols,
                  font_size=30),
        )
        for st in steps[1:]:
            st[0].set_opacity(0)
        whys = VGroup(
            label(r"$b_e = e_u - e_v$ for the edge $e = (u, v)$", font_size=18, color=GREY_B),
            label(r"a number is its own trace, \ and the trace is linear", font_size=18, color=GREY_B),
            label(r"$L^{+} L$ projects away the constants \ (connected $G$)", font_size=18, color=YES),
        )
        lad = ladder(steps, whys, buff=0.3).move_to(RIGHT * 2.95 + UP * 0.85)
        check = label(rf"here: \ {len(E)} edges, \ $\sum_e R_e = {sum(R):.0f} = n - 1$", font_size=21,
                      color=YES).next_to(lad, DOWN, buff=0.45).align_to(lad, LEFT)
        ill = note(r"illustrative graph; \ resistances computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Which edges can a sparsifier drop? <bookmark mark='a'/> Two cliques of eight, joined by one bridge. "
            "Colour each edge by its effective resistance. <bookmark mark='b'/> The bridge has resistance one: it "
            "is the only way across, and every cut between the cliques depends on it. An edge inside a clique has "
            "a quarter: plenty of other routes do its job. <bookmark mark='c'/> And the total is fixed. Each "
            "resistance is a quadratic form; <bookmark mark='d'/> gather them into one trace; "
            "<bookmark mark='e'/> the weighted resistances of a connected graph's edges sum to n minus one. This "
            "is Foster's theorem, from 1949. Resistance is a budget of importance, n minus one in all, however "
            "many edges there are."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(*[MoveToTarget(ln) for ln in g[0]])
            vo.wait_until("b")
            self.play(FadeIn(reads), FadeIn(ill))
            vo.wait_until("c")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            self.play(FadeIn(check))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ sample by resistance, reweight
    def sampling(self):
        head = label(r"Spielman--Srivastava: \ sample by resistance", font_size=36).to_edge(UP, buff=0.3)
        k = 8
        E = [(a, b) for a in range(k) for b in range(a + 1, k)]
        E += [(a + k, b + k) for a in range(k) for b in range(a + 1, k)]
        E += [(0, k)]
        n = 2 * k
        Lp = np.linalg.pinv(laplacian_of(n, E))
        R = np.array([Lp[a, a] + Lp[b, b] - 2 * Lp[a, b] for a, b in E])
        p = R / R.sum()
        q = 40
        rng = random.Random(0)
        draws = rng.choices(range(len(E)), weights=list(p), k=q)
        wH = np.zeros(len(E))
        for e in draws:
            wH[e] += 1.0 / (q * p[e])
        kept = int((wH > 0).sum())
        miss_r = (1 - p[-1]) ** q
        miss_u = (1 - 1 / len(E)) ** q
        bridge = r"the bridge among them" if wH[-1] > 0 else r"but not the bridge"
        pos = []
        for c in (-1.0, 1.0):
            for j in range(k):
                ang = np.pi * (0 if c > 0 else 1) + 2 * np.pi * j / k
                pos.append((c * 1.75 + 0.95 * np.cos(ang), 0.95 * np.sin(ang)))
        g = draw(pos, E, center=LEFT * 3.6 + UP * 0.55, scale=0.95, r=0.07, ecolor=GREY_C, sw=1.5)
        sparse = VGroup()
        for (a, b), w in zip(E, wH):
            if w > 0:
                sparse.add(Line(g.pts[a], g.pts[b], color=YES, stroke_width=1.2 + 1.3 * min(w, 4.0)))
        steps = VGroup(
            cmath(r"p_e", r"=", r"\frac{w_e R_e}{n - 1}", font_size=32),
            cmath(r"\text{draw } q \text{ edges from } p,", r"\ \ ", r"\text{each with weight } \frac{w_e}{q\, p_e}",
                  font_size=28),
            cmath(r"\mathbb E\, L_H", r"=", r"\sum_e q\, p_e \cdot \frac{w_e}{q\, p_e}\, b_e b_e^{\mathsf T}", r"=",
                  r"L_G", font_size=30),
            cmath(r"q", r"=", r"O\!\left(\frac{n \log n}{\varepsilon^2}\right)", r"\ \Rightarrow\ ",
                  r"(1 \pm \varepsilon) \text{ with high probability}", font_size=28),
        )
        steps[2][4].set_color(YES)
        steps[3][2].set_color(HEAD)
        whys = VGroup(
            label(r"probability in proportion to importance", font_size=18, color=GREY_B),
            label(r"a rare edge, \ when drawn, \ stands for many", font_size=18, color=GREY_B),
            label(r"unbiased: \ right on average", font_size=18, color=GREY_B),
            label(r"a matrix concentration bound makes it right every time, \ nearly", font_size=18, color=YES),
        )
        lad = ladder(steps, whys, buff=0.25).move_to(RIGHT * 3.0 + UP * 0.25)
        if lad.get_right()[0] > 6.85:
            lad.shift(LEFT * (lad.get_right()[0] - 6.85))
        res = wrapped_label(rf"{q} draws kept {kept} of {len(E)} edges, \ {bridge}. \ Chance of missing the "
                            rf"bridge: \ {miss_r * 100:.0f}\% by resistance, \ {miss_u * 100:.0f}\% uniformly", 5.2,
                            font_size=19, color=YES).next_to(g, DOWN, buff=0.45)
        bss = wrapped_label(r"Batson, \ Spielman and Srivastava: \ $O(n/\varepsilon^2)$ edges always suffice, "
                            r"\ found deterministically; \ for the complete graph, \ as good as a Ramanujan "
                            r"expander with twice the edges", 12.6, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        ill = note(r"illustrative sample; \ computed", font_size=16).next_to(res, DOWN, buff=0.15)
        with self.voiceover(
            "In 2008 Daniel Spielman and Nikhil Srivastava turned that budget into an algorithm. "
            "<bookmark mark='a'/> Sample edges with probability proportional to weight times effective "
            "resistance. <bookmark mark='b'/> Draw q of them, each drawn edge weighted by one over q times its "
            "probability. <bookmark mark='c'/> On average the sample's Laplacian is exactly G's. "
            "<bookmark mark='d'/> With about n log n over epsilon squared draws, a matrix concentration "
            "inequality makes it right within one plus or minus epsilon, with high probability. "
            "<bookmark mark='e'/> Forty draws from our two cliques keep the bridge and thin the cliques; uniform "
            "draws would miss the bridge half the time, and with it every path between the halves. "
            "<bookmark mark='f'/> Joshua Batson, Spielman and Srivastava then showed that a linear number of "
            "edges always suffices. For the complete graph their sparsifiers match Ramanujan expanders with twice "
            "as many edges: twice-Ramanujan sparsifiers."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(g[0].animate.set_stroke(opacity=0.15), LaggedStart(*[Create(s) for s in sparse],
                                                                         lag_ratio=0.05))
            self.play(FadeIn(res), FadeIn(ill))
            vo.wait_until("f")
            self.play(FadeIn(bss))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ all resistances at once, by projection
    def resistances(self):
        head = label(r"Every resistance at once, \ by random projection", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"R_e": HEAD}
        steps = VGroup(
            cmath(r"R_e", r"=", r"b_e^{\mathsf T} L^{+} b_e", colors=cols, font_size=32),
            cmath(r"R_e", r"=", r"b_e^{\mathsf T} L^{+} L\, L^{+} b_e", colors=cols, font_size=32),
            cmath(r"R_e", r"=", r"b_e^{\mathsf T} L^{+} B^{\mathsf T} W B\, L^{+} b_e", colors=cols, font_size=32),
            cmath(r"R_e", r"=", r"\big\| W^{1/2} B\, L^{+} b_e \big\|^2", colors=cols, font_size=32),
            cmath(r"R_e", r"\approx", r"\big\| Q\, W^{1/2} B\, L^{+} b_e \big\|^2", colors=cols, font_size=32),
        )
        whys = VGroup(
            label(r"the quadratic form of chapter eight", font_size=18, color=GREY_B),
            label(r"$L^{+} L L^{+} = L^{+}$", font_size=18, color=GREY_B),
            label(r"$L = B^{\mathsf T} W B$: \ $B$ the $m \times n$ edge--vertex matrix, \ $W$ the weights",
                  font_size=18, color=GREY_B),
            label(r"a squared distance between two columns", font_size=18, color=GREY_B),
            label(r"Johnson--Lindenstrauss: \ $Q$ random, \ $k = O(\log n / \varepsilon^2)$ rows", font_size=18,
                  color=YES),
        )
        ladder(steps, whys, buff=0.22).to_edge(LEFT, buff=0.5).shift(DOWN * 0.15)

        def block(w, h, col, txt):
            r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.18)
            return VGroup(r, label(txt, font_size=20, color=col).move_to(r))
        big = block(1.1, 2.6, DATA, r"$m \times n$")
        Q = block(2.2, 0.55, HEAD, r"$k \times m$")
        Z = block(1.1, 0.55, YES, r"$k \times n$")
        times = MathTex(r"\times", font_size=32)
        eq = MathTex(r"=", font_size=32)
        mats = VGroup(Q, times, big, eq, Z).arrange(RIGHT, buff=0.2).move_to(RIGHT * 3.9 + UP * 0.6)
        if mats.get_right()[0] > 6.75:
            mats.shift(LEFT * (mats.get_right()[0] - 6.75))
        caps = VGroup(label(r"$W^{1/2} B L^{+}$", font_size=18, color=DATA).next_to(big, DOWN, buff=0.12),
                      label(r"$Q$", font_size=18, color=HEAD).next_to(Q, DOWN, buff=0.12),
                      label(r"$Z$", font_size=18, color=YES).next_to(Z, DOWN, buff=0.12))
        note_r = wrapped_label(r"each of the $k$ rows of $Z$ is one Laplacian solve: \ $L z_i = (Q W^{1/2} B)_i$; "
                               r"\ then every $R_e \approx \|z_u - z_v\|^2$", 5.6, font_size=19,
                               color=GREY_A).next_to(mats, DOWN, buff=0.75)
        circ = wrapped_label(r"the sparsifier needs resistances, \ resistances need a solver, \ the solver needs "
                             r"a sparsifier: \ Spielman and Srivastava broke the circle with Spielman and Teng's "
                             r"solver", 5.6, font_size=19, color=HEAD).next_to(note_r, DOWN, buff=0.35)
        with self.voiceover(
            "But computing an effective resistance means solving a Laplacian system, and we want all m of them. "
            "<bookmark mark='a'/> Rewrite the quadratic form. <bookmark mark='b'/> Insert L between two "
            "pseudo-inverses, <bookmark mark='c'/> and factor L through the edge-vertex incidence matrix. "
            "<bookmark mark='d'/> Now each resistance is a squared distance between two columns of one matrix. "
            "<bookmark mark='e'/> Distances survive random projection: this is the Johnson–Lindenstrauss lemma "
            "from AI, Built and Part 20's sketches. A random matrix with about log n rows keeps every one of "
            "these distances within one plus or minus epsilon. <bookmark mark='f'/> So log n Laplacian solves give "
            "every resistance at once. <bookmark mark='g'/> The circle, sparsifiers needing resistances needing "
            "solvers, was broken by a solver that came first."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]),
                      FadeIn(big), FadeIn(caps[0]))
            self.play(FadeIn(Q), FadeIn(times), FadeIn(caps[1]))
            vo.wait_until("f")
            self.play(FadeIn(eq), GrowFromEdge(Z, LEFT), FadeIn(caps[2]), FadeIn(note_r))
            vo.wait_until("g")
            self.play(FadeIn(circ))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ low-stretch trees and Spielman–Teng
    def trees(self):
        head = label(r"Trees as preconditioners: \ stretch", font_size=36).to_edge(UP, buff=0.3)
        W = H = 6
        idx, G = grid_edges(W, H)
        n = W * H
        order = []
        for x in range(W):
            order += [idx[(x, y)] for y in (range(H) if x % 2 == 0 else range(H - 1, -1, -1))]
        snake = [(order[i], order[i + 1]) for i in range(n - 1)]
        mid = W // 2 - 1
        spine = [(idx[(x, y)], idx[(x + 1, y)]) for y in range(H) for x in range(W - 1)]
        spine += [(idx[(mid, y)], idx[(mid, y + 1)]) for y in range(H - 1)]
        LG = laplacian_of(n, G)

        def stats(T):
            st = sum(len(tree_path(n, T, a, b)) - 1 for a, b in G)
            ev = np.sort(np.linalg.eigvals(np.linalg.pinv(laplacian_of(n, T)) @ LG).real)
            return st, ev[-1]
        st1, k1 = stats(snake)
        st2, k2 = stats(spine)
        pos = [(x - (W - 1) / 2, y - (H - 1) / 2) for x in range(W) for y in range(H)]
        centre = LEFT * 4.1 + UP * 0.35
        g = draw(pos, G, center=centre, scale=0.6, r=0.06, color=GREY_B, ecolor=GREY_D, sw=1.5)

        def tree_lines(T, col):
            return VGroup(*[Line(g.pts[a], g.pts[b], color=col, stroke_width=4) for a, b in T])
        t1, t2 = tree_lines(snake, KERN), tree_lines(spine, YES)
        e_off = (idx[(0, 0)], idx[(1, 0)])
        path = tree_path(n, snake, *e_off)
        ph = VGroup(*[Line(g.pts[a], g.pts[b], color=HEAD, stroke_width=6) for a, b in zip(path, path[1:])])
        offe = Line(g.pts[e_off[0]], g.pts[e_off[1]], color=NO, stroke_width=5)
        st_l = label(rf"stretch of the red edge: \ {len(path) - 1}", font_size=20, color=HEAD).next_to(
            g, UP, buff=0.25)
        r1 = label(rf"snake: \ total stretch {st1}, \ $\kappa = {k1:.1f}$", font_size=20, color=KERN)
        r2 = label(rf"spine: \ total stretch {st2}, \ $\kappa = {k2:.1f}$", font_size=20, color=YES)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, DOWN, buff=0.35)
        steps = VGroup(
            cmath(r"\mathrm{st}_T(e)", r"=", r"w_e \cdot R_T(u, v)", font_size=30),
            cmath(r"L_T", r"\preceq", r"L_G", r"\preceq", r"\mathrm{st}(T)\, L_T", font_size=30),
            cmath(r"\kappa(L_T^{+} L_G)", r"\le", r"\mathrm{st}(T)", r"=", r"\sum_e \mathrm{st}_T(e)", font_size=30),
        )
        steps[2][2].set_color(HEAD)
        whys = VGroup(
            label(r"the resistance of the tree path that replaces edge $e = (u, v)$", font_size=18, color=GREY_B),
            label(r"$T$ is part of $G$; \ each edge is at most its stretch times its tree path", font_size=18,
                  color=GREY_B),
            label(r"and solving with a tree is linear time: \ peel off leaves", font_size=18, color=YES),
        )
        lad = ladder(steps, whys, buff=0.28).move_to(RIGHT * 2.75 + UP * 1.1)
        if lad.get_right()[0] > 6.85:
            lad.shift(LEFT * (lad.get_right()[0] - 6.85))
        st_box = wrapped_label(r"Spielman and Teng \ (2004): \ precondition by a low-stretch tree plus a few "
                               r"edges, \ eliminate the vertices of degree one and two, \ recurse on what is "
                               r"left; \ time $O(m \log^{c} n \log(1/\varepsilon))$", 6.4, font_size=19,
                               color=HEAD).next_to(lad, DOWN, buff=0.4).align_to(lad, LEFT)
        ill = note(r"illustrative grid; \ stretch and $\kappa$ computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The simplest sparse graph is a spanning tree. <bookmark mark='a'/> Lay a snake-shaped tree on a "
            "grid. <bookmark mark='b'/> An edge it leaves out must be replaced by its path through the tree; that "
            "path's length is the edge's stretch, here eleven. <bookmark mark='c'/> The tree is part of the "
            "graph, and each edge costs at most its stretch times its tree path, so the condition number is at "
            "most the total stretch. <bookmark mark='d'/> And a tree system is solved in linear time, by peeling "
            "off leaves. <bookmark mark='e'/> A tree with a central spine stretches less, and conditions better. "
            "<bookmark mark='f'/> Spielman and Teng, in 2004, built a recursion from low-stretch trees and "
            "sparsifiers: precondition by a tree plus a few edges, eliminate vertices of degree one and two, "
            "recurse. Laplacian systems became solvable in nearly linear time."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(Create(t1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(offe), Write(steps[0]), FadeIn(whys[0]))
            self.play(Create(ph), FadeIn(st_l), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]), FadeIn(r1))
            vo.wait_until("e")
            self.play(FadeOut(ph), FadeOut(offe), FadeOut(st_l), ReplacementTransform(t1, t2), FadeIn(r2), FadeIn(ill))
            vo.wait_until("f")
            self.play(FadeIn(st_box))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO)
