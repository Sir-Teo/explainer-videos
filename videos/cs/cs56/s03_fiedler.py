from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


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


def vcolor(v, vmax):
    """An eigenvector entry as a colour: blue below zero, orange above, grey at zero."""
    a = float(np.clip(v / vmax, -1, 1))
    return interpolate_color(ManimColor(GREY_C), ManimColor(KERN if a > 0 else DATA), abs(a) ** 0.7)


def colour_key(width=2.4):
    bar = VGroup(*[Rectangle(width=width / 24, height=0.16, stroke_width=0, fill_opacity=1,
                             fill_color=vcolor(-1 + 2 * k / 23, 1.0)) for k in range(24)]).arrange(RIGHT, buff=0)
    lo = label(r"$-$", font_size=20, color=DATA).next_to(bar, LEFT, buff=0.1)
    hi = label(r"$+$", font_size=20, color=KERN).next_to(bar, RIGHT, buff=0.1)
    return VGroup(bar, lo, hi)


def two_clusters():
    """Two hexagons with two chords each (12 vertices), joined by the bridge (0, 9)."""
    pos, edges = [], []
    for c, off in ((-1.45, 0), (1.45, 6)):
        for k in range(6):
            a = 2 * math.pi * k / 6
            pos.append((c + 0.85 * math.cos(a), 0.85 * math.sin(a)))
        edges += [(off + k, off + (k + 1) % 6) for k in range(6)] + [(off, off + 2), (off + 3, off + 5)]
    return pos, edges + [(0, 9)]


def three_clusters():
    """Three pentagons with two chords each (15 vertices), joined in a triangle by one edge each."""
    pos, edges = [], []
    for c in range(3):
        ang = math.pi / 2 + 2 * math.pi * c / 3
        cx, cy = 1.9 * math.cos(ang), 1.9 * math.sin(ang)
        for k in range(5):
            a = 2 * math.pi * k / 5 + ang
            pos.append((cx + 0.6 * math.cos(a), cy + 0.6 * math.sin(a)))
        edges += [(5 * c + k, 5 * c + (k + 1) % 5) for k in range(5)] + [(5 * c, 5 * c + 2), (5 * c + 1, 5 * c + 3)]
    return pos, edges + [(2, 8), (7, 13), (12, 3)]


class Fiedler(VoiceoverScene):
    def construct(self):
        self.card()
        self.rayleigh()
        self.minmax()
        self.relax()
        self.vector()
        self.planted()
        self.clustering()

    def card(self):
        card = chapter_card(2, r"Rayleigh quotients and the Fiedler vector",
                            r"Why does an eigenvector know where to cut?", lit=(1905, 1973),
                            extra=((1905, r"Fischer: \ the min-max principle"),
                                   (1973, r"Fiedler: \ algebraic connectivity")), part=PART)
        with self.voiceover("Chapter two. Rayleigh quotients, and the Fiedler vector."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rayleigh(self):
        head = label(r"The Rayleigh quotient", font_size=36).to_edge(UP, buff=0.3)
        self.head = head
        cols = {r"\lambda_i": HEAD, r"c_i^2": DATA}
        steps = VGroup(
            cmath(r"R(x)", r"=", r"\frac{x^{\mathsf T} L x}{x^{\mathsf T} x}", font_size=34),
            cmath(r"x", r"=", r"\sum_i", r"c_i", r"v_i", font_size=34),
            cmath(r"x^{\mathsf T} L x", r"=", r"\sum_i", r"\lambda_i", r"c_i^2", r",\qquad", r"x^{\mathsf T} x",
                  r"=", r"\sum_i", r"c_i^2", colors=cols, font_size=34),
            cmath(r"R(x)", r"=", r"\frac{\sum_i \lambda_i c_i^2}{\sum_i c_i^2}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 2.7 + UP * 0.8)
        whys = VGroup(
            label(r"energy per unit size", font_size=19, color=GREY_B),
            label(r"$L$ is symmetric: \ orthonormal eigenvectors $v_i$", font_size=19, color=GREY_B),
            label(r"the cross terms vanish", font_size=19, color=GREY_B),
            label(r"a weighted average of the eigenvalues", font_size=19, color=YES),
        )
        for w, s in zip(whys, steps):
            w.next_to(s, RIGHT, buff=0.45)
        pos, edges = two_clusters()
        lam = np.linalg.eigvalsh(lap(adjacency(12, edges)))
        nl = NumberLine(x_range=[0, 6.5, 1], length=11.0, color=GREY_C, include_numbers=False).move_to(DOWN * 2.75)
        ticks = VGroup(*[label(rf"{k}", font_size=16, color=GREY_B).next_to(nl.n2p(k), DOWN, buff=0.1)
                         for k in range(7)])
        groups = {}
        for i, v in enumerate(lam):
            groups.setdefault(round(float(max(v, 0)), 2), []).append(i)
        lam_marks = VGroup(*[Dot(nl.n2p(k), radius=0.05, color=HEAD) for k in groups])
        cap = label(r"the eigenvalues of chapter 1's bridged graph; \ bar height $c_i^2$", font_size=18,
                    color=GREY_A).next_to(nl, UP, buff=1.3).align_to(nl, RIGHT)
        rng = np.random.default_rng(3)
        W = [rng.random(12), np.r_[np.zeros(8), 1, 2, 3, 4], np.r_[1, np.zeros(11)] + 0.0]
        W = [w / w.sum() for w in W]
        self.W, self.lam, self.groups, self.nl = W, lam, groups, nl
        tr = ValueTracker(0)
        self.tr = tr

        def cur():
            t = tr.get_value()
            Wl = self.W
            k = min(int(t), len(Wl) - 2)
            f = t - k
            return (1 - f) * Wl[k] + f * Wl[k + 1]

        def bars():
            c = cur()
            g = VGroup()
            for v, idx in groups.items():
                h = 1.2 * float(sum(c[i] for i in idx)) + 0.001
                g.add(Rectangle(width=0.16, height=h, stroke_width=0, fill_color=DATA, fill_opacity=0.85).move_to(
                    nl.n2p(v) + UP * h / 2))
            return g

        def pointer():
            c = cur()
            r = float((c * np.maximum(lam, 0)).sum() / c.sum())
            tri = Triangle(color=YES, fill_opacity=1, stroke_width=0).scale(0.11).move_to(nl.n2p(r) + DOWN * 0.42)
            t = MathTex(r"R(x)", font_size=24, color=YES).next_to(tri, DOWN, buff=0.06)
            return VGroup(tri, t)
        self.cur = cur
        bar_m = always_redraw(bars)
        ptr = always_redraw(pointer)
        with self.voiceover(
            "Chapter one promised that adding an edge never lowers lambda two. The tool that proves it, and much "
            "more, is the Rayleigh quotient: the energy of a labelling divided by its size. <bookmark mark='a'/> "
            "Because L is symmetric, its eigenvectors can be chosen orthonormal, and any x is a combination of "
            "them. <bookmark mark='b'/> In that basis the cross terms vanish: the energy is a sum of eigenvalues "
            "times squared coefficients, and the size is the sum of the squared coefficients. "
            "<bookmark mark='c'/> So the Rayleigh quotient is a weighted average of the eigenvalues, each weighted "
            "by how much of x lies along its eigenvector. <bookmark mark='d'/> Move the weights and the average "
            "moves, but it never leaves the range of the eigenvalues. <bookmark mark='e'/> Its smallest value, "
            "zero, comes from putting all the weight on the first eigenvector, the constant one."
        ) as vo:
            self.play(FadeIn(head), Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            self.play(Create(nl), FadeIn(ticks), FadeIn(lam_marks), FadeIn(cap), FadeIn(bar_m),
                      FadeIn(ptr))
            vo.wait_until("d")
            self.play(tr.animate.set_value(1), run_time=3)
            vo.wait_until("e")
            self.play(tr.animate.set_value(2), run_time=2.5)
        self.wait(0.4)
        self.keep = VGroup(nl, ticks, lam_marks)
        self.bar_m, self.ptr, self.cap = bar_m, ptr, cap
        self.clear_scene(self.keep, bar_m, ptr)

    def minmax(self):
        head = label(r"Courant--Fischer: \ eigenvalues as min-max", font_size=36).to_edge(UP, buff=0.3)
        nl = self.nl
        tr = self.tr
        rng = np.random.default_rng(5)
        w2 = rng.random(12)
        w2[0] = 0
        w3 = np.r_[0, 1, np.zeros(10)]
        self.W = [self.cur(), w2 / w2.sum(), w3]
        tr.set_value(0)
        steps = VGroup(
            cmath(r"x \perp \mathbf{1}", r"\ \Rightarrow\ ", r"c_1 = 0", font_size=32),
            cmath(r"R(x)", r"=", r"\frac{\sum_{i \ge 2} \lambda_i c_i^2}{\sum_{i \ge 2} c_i^2}", r"\ \ge\ ",
                  r"\lambda_2", font_size=32),
            cmath(r"\lambda_2", r"=", r"\min_{x \perp \mathbf{1}}", r"\frac{x^{\mathsf T} L x}{x^{\mathsf T} x}",
                  font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 3.6 + UP * 1.4)
        steps[1][4].set_color(HEAD)
        steps[2][0].set_color(HEAD)
        thm = VGroup(
            MathTex(r"\lambda_k = \min_{\dim S = k}\ \max_{x \in S,\, x \neq 0}\ \frac{x^{\mathsf T} L x}"
                    r"{x^{\mathsf T} x}", font_size=32, color=YES),
            label(r"Fischer \ (1905); \ Courant \ (1920)", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.15)
        box = SurroundingRectangle(thm, color=YES, buff=0.2, corner_radius=0.1, stroke_width=1.5)
        thm_g = VGroup(box, thm).move_to(RIGHT * 3.4 + UP * 1.65)
        cor = wrapped_label(r"an edge adds $(x_i - x_j)^2 \ge 0$ to every numerator: \ every $\lambda_k$ can only "
                            r"rise", 5.4, font_size=20, color=HEAD).next_to(thm_g, DOWN, buff=0.35)
        cross = Cross(Dot(nl.n2p(0)), stroke_color=NO, stroke_width=4).scale(2.4).move_to(nl.n2p(0) + UP * 0.25)
        with self.voiceover(
            "Now forbid the constant vector: allow only labellings orthogonal to the all-ones vector, whose values "
            "sum to zero. <bookmark mark='a'/> Then the first weight is zero, "
            "<bookmark mark='b'/> the average runs over lambda two and above, and it can never be smaller than "
            "lambda two. <bookmark mark='c'/> Put all the weight on the second eigenvector and the average "
            "reaches lambda two exactly. So lambda two is the smallest Rayleigh quotient among vectors orthogonal "
            "to the constant. <bookmark mark='d'/> The general statement is the Courant–Fischer theorem: the k-th "
            "eigenvalue is the best, over all k-dimensional subspaces, of the worst quotient inside. Ernst Fischer "
            "proved it in 1905, and Richard Courant extended it in 1920. "
            "<bookmark mark='e'/> And here is chapter one's promise. Adding an edge adds a square to the energy of "
            "every vector, so every quotient rises, and with them every eigenvalue."
        ) as vo:
            self.play(FadeIn(head), Write(steps[0]))
            vo.wait_until("a")
            self.play(Create(cross), tr.animate.set_value(1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(tr.animate.set_value(2), run_time=2)
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(thm_g))
            vo.wait_until("e")
            self.play(FadeIn(cor))
        self.wait(0.4)
        self.clear_scene()

    def relax(self):
        head = label(r"A cut is a vector of $\pm 1$", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = two_clusters()
        g = draw(pos, edges, center=LEFT * 3.4 + UP * 0.4, scale=0.95, r=0.12)
        sign = [-1] * 6 + [1] * 6
        for d, s_ in zip(g[1], sign):
            d.set_color(DATA if s_ < 0 else KERN)
        bridge = g[0][len(edges) - 1]
        four = MathTex(r"(+1 - (-1))^2 = 4", font_size=26, color=HEAD).next_to(g, DOWN, buff=0.45)
        four.set_x(bridge.get_center()[0])
        four_arrow = Arrow(four.get_top(), bridge.get_center() + DOWN * 0.08, buff=0.08, color=HEAD,
                           stroke_width=2, max_tip_length_to_length_ratio=0.15)
        signs = VGroup(label(r"$x_i = -1$", font_size=21, color=DATA).next_to(g, DOWN, buff=0.2).shift(LEFT * 2.1),
                       label(r"$x_i = +1$", font_size=21, color=KERN).next_to(g, DOWN, buff=0.2).shift(RIGHT * 2.1))
        steps = VGroup(
            cmath(r"x^{\mathsf T} L x", r"=", r"\sum_{(i,j) \in E} (x_i - x_j)^2", r"=", r"4\,|E(S, \bar S)|",
                  font_size=30),
            cmath(r"\text{bisection}", r"=", r"\min_{x \in \{\pm 1\}^n,\ x \perp \mathbf{1}}",
                  r"\tfrac14\, x^{\mathsf T} L x", font_size=30),
            cmath(r"\text{bisection}", r"\ \ge\ ", r"\min_{x \in \mathbb{R}^n,\ x \perp \mathbf{1},\ \|x\|^2 = n}",
                  r"\tfrac14\, x^{\mathsf T} L x", font_size=30),
            cmath(r"\text{bisection}", r"\ \ge\ ", r"\tfrac{n}{4}\, \lambda_2", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.0 + UP * 0.55)
        if steps.width > 7.2:
            steps.scale_to_fit_width(7.2).move_to(RIGHT * 3.1 + UP * 0.55)
        steps[0][4].set_color(HEAD)
        steps[3][2].set_color(YES)
        tags = VGroup(label(r"balanced: \ $\sum x_i = 0$; \ NP-hard to minimize", font_size=19, color=NO),
                      label(r"relax: \ any real values", font_size=19, color=YES))
        tags[0].next_to(steps[1], DOWN, buff=0.08).align_to(steps[1], LEFT)
        tags[1].next_to(steps[2], DOWN, buff=0.08).align_to(steps[2], LEFT)
        n = 12
        lam2 = float(np.linalg.eigvalsh(lap(adjacency(n, edges)))[1])
        check = label(rf"here: \ $\tfrac{{12}}{{4}} \times {lam2:.2f} = {n * lam2 / 4:.2f} \le 1$, \ the bridge",
                      font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45).shift(RIGHT * 3.0)
        with self.voiceover(
            "Why should an eigenvector know where to cut? Write a cut as a vector: minus one on one side, plus one "
            "on the other. <bookmark mark='a'/> An edge inside a side contributes nothing to the energy; an edge "
            "across the cut contributes four. So the energy is four times the number of edges cut. "
            "<bookmark mark='b'/> Asking for the best cut into two equal halves, the minimum bisection, means "
            "minimizing the energy over vectors of plus and minus ones that sum to zero. That problem is NP-hard. "
            "<bookmark mark='c'/> So relax it: allow any real values with the same sum and the same length. The "
            "minimum can only drop, <bookmark mark='d'/> and by Courant–Fischer the relaxed minimum is n over four "
            "times lambda two: a lower bound on every bisection, and the vector that attains it is the second "
            "eigenvector."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(signs))
            vo.wait_until("a")
            self.play(bridge.animate.set_stroke(HEAD, width=5), FadeIn(four), GrowArrow(four_arrow), Write(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(tags[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(tags[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(check))
        self.wait(0.4)
        self.clear_scene()

    def vector(self):
        head = label(r"The Fiedler vector, \ drawn as colours", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = two_clusters()
        n = 12
        w, V = np.linalg.eigh(lap(adjacency(n, edges)))
        f = V[:, 1] * (1 if V[0, 1] > 0 else -1) * -1
        g = draw(pos, edges, center=LEFT * 3.3 + UP * 0.9, scale=0.95, r=0.13)
        gw, gh = 8, 4
        gpos = [(0.5 * x, 0.5 * y) for x in range(gw) for y in range(gh)]
        gedges = [(x * gh + y, (x + 1) * gh + y) for x in range(gw - 1) for y in range(gh)] + \
                 [(x * gh + y, x * gh + y + 1) for x in range(gw) for y in range(gh - 1)]
        wg, Vg = np.linalg.eigh(lap(adjacency(gw * gh, gedges)))
        fg = Vg[:, 1]
        grid_g = draw(gpos, gedges, center=RIGHT * 1.75 + UP * 0.15, scale=1.0, r=0.1, sw=1.5)
        gcap = label(r"an $8 \times 4$ grid: \ a slow wave along its length", font_size=19, color=GREY_A).next_to(
            grid_g, DOWN, buff=0.3)
        key = colour_key().next_to(head, DOWN, buff=0.25).to_edge(RIGHT, buff=0.6)
        nl = NumberLine(x_range=[-1, 1, 0.5], length=11.0, color=GREY_C, include_numbers=False).move_to(DOWN * 2.6)
        zero = label(r"$0$", font_size=18, color=GREY_B).next_to(nl.n2p(0), DOWN, buff=0.15)
        ncap = label(r"the Fiedler order: \ each vertex placed at its value", font_size=19, color=GREY_A).next_to(
            nl, DOWN, buff=0.45)
        mx = float(np.abs(f).max())
        order = np.argsort(f)
        targets = {}
        for rank, i in enumerate(order):
            targets[int(i)] = nl.n2p(f[i] / mx * 0.95) + UP * (0.22 if rank % 2 else -0.0) + UP * 0.12
        moved = VGroup(*[g[1][i].copy() for i in range(n)])
        split = DashedLine(nl.n2p(0) + UP * 0.7, nl.n2p(0) + DOWN * 0.1, color=HEAD)
        fied = label(r"Fiedler \ (1975): \ in a connected graph, \ the vertices with $v_2 \ge 0$ induce a "
                     r"connected piece", font_size=20, color=YES).move_to(DOWN * 1.2)
        with self.voiceover(
            "Here is the second eigenvector of the bridged graph, drawn as colours: blue for negative entries, "
            "orange for positive, brighter for larger. <bookmark mark='a'/> It is negative on one cluster and "
            "positive on the other, and smallest in size at the two ends of the bridge, where it changes sign. "
            "<bookmark mark='b'/> On a grid it is a slow wave along the long side, so the cut it suggests goes "
            "straight across the middle, the cheap cut of Part 18's city. <bookmark mark='c'/> Line the vertices "
            "up by their values, and you get the Fiedler order. Splitting it at zero separates the clusters. "
            "<bookmark mark='d'/> Fiedler showed in 1975 that this is no accident: in a connected graph, the "
            "vertices where the vector is not negative always form a connected piece."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(key))
            vo.wait_until("a")
            self.play(*[d.animate.set_color(vcolor(v, mx)) for d, v in zip(g[1], f)])
            vo.wait_until("b")
            self.play(Create(grid_g[0]), FadeIn(grid_g[1]), FadeIn(gcap))
            self.play(*[d.animate.set_color(vcolor(v, float(np.abs(fg).max()))) for d, v in zip(grid_g[1], fg)])
            vo.wait_until("c")
            for d, v in zip(moved, f):
                d.set_color(vcolor(v, mx))
            self.play(Create(nl), FadeIn(zero), FadeIn(ncap))
            self.play(*[d.animate.move_to(targets[i]) for i, d in enumerate(moved)], run_time=2)
            self.play(Create(split))
            vo.wait_until("d")
            self.play(FadeIn(fied))
        self.wait(0.4)
        self.clear_scene()

    def planted(self):
        p = load("partition")
        f = np.array(p["fiedler"])
        lab = np.array(p["labels"])
        f = f * (1 if f[lab == 0].mean() < 0 else -1)
        n, m, acc = p["n"], p["edges"], p["accuracy"]
        head = label(r"Planted communities, \ recovered", font_size=36).to_edge(UP, buff=0.3)
        ymax = 0.2
        ax = CornerAxes(x_range=[0, n, 20], y_range=[-ymax, ymax, 0.1], x_length=8.0, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 2.2 + DOWN * 0.35)
        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(n, 0), color=HEAD, stroke_width=1.5)
        yt = VGroup(*[label(rf"${v:+.1f}$" if v else r"$0$", font_size=16, color=GREY_B).next_to(
            ax.c2p(0, v), LEFT, buff=0.1) for v in (-0.2, -0.1, 0.0, 0.1, 0.2)])
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -ymax), DOWN, buff=0.1)
                      for v in (0, 60, 120)])
        xl = label(r"vertex \ (first 60: \ community A)", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"entry of the Fiedler vector", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(i + 0.5, float(np.clip(v, -ymax, ymax))), radius=0.045,
                            color=DATA if lab[i] == 0 else KERN) for i, v in enumerate(f)])
        side = VGroup(
            wrapped_label(rf"{n} vertices, \ {m} edges; \ two planted communities, \ A \ (blue) \ and B \ "
                          r"(orange)", 4.2, font_size=19, color=GREY_A),
            wrapped_label(r"the eigenvector is computed from the edges alone, \ without the labels", 4.2,
                          font_size=19, color=WHITE),
            wrapped_label(rf"its signs agree with the planted communities on {acc * 100:.0f}\% of the vertices",
                          4.2, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 4.5 + DOWN * 0.2)
        with self.voiceover(
            "Now a graph too large to read by eye: chapter one's hundred and twenty vertices in two planted "
            "communities. <bookmark mark='a'/> Compute the second eigenvector from the edges alone, without the "
            "labels, and plot each vertex's entry, with the first sixty vertices belonging to community A. "
            "<bookmark mark='b'/> Every vertex of A has a negative entry and every vertex of B a positive one. The "
            "signs recover the planted communities exactly. Nobody told the matrix which vertex belonged where."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(zero_line), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def clustering(self):
        head = label(r"Spectral clustering", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = three_clusters()
        n = 15
        w, V = np.linalg.eigh(lap(adjacency(n, edges)))
        g = draw(pos, edges, center=LEFT * 4.0 + DOWN * 0.15, scale=0.95, r=0.11)
        gcap = label(r"three clusters, \ one edge between each pair", font_size=19, color=GREY_A).next_to(
            g, DOWN, buff=0.3)
        ax = Axes(x_range=[-0.5, 0.5, 0.25], y_range=[-0.5, 0.5, 0.25], x_length=3.8, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(RIGHT * 0.1 + DOWN * 0.15)
        axl = VGroup(label(r"$v_2$", font_size=20, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1),
                     label(r"$v_3$", font_size=20, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1))
        acap = label(r"each vertex placed at $(v_2, v_3)$", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        moved = VGroup(*[g[1][i].copy() for i in range(n)])
        targets = [ax.c2p(float(V[i, 1]), float(V[i, 2])) for i in range(n)]
        cols = [DATA, KERN, LAM]
        side = VGroup(
            wrapped_label(r"embed by the bottom $k$ eigenvectors, \ then group the points \ (k-means): \ Shi and "
                          r"Malik \ (2000), \ Ng, \ Jordan and Weiss \ (2001)", 4.0, font_size=19, color=WHITE),
            wrapped_label(r"multilevel partitioners such as METIS \ (Karypis and Kumar, \ 1998) \ shard huge graphs "
                          r"faster, \ with the same goal: \ few cut edges, \ balanced parts", 4.0, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 4.6 + DOWN * 0.1)
        ill = note(r"illustrative graph; \ eigenvectors computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "With more than two communities, use more eigenvectors. <bookmark mark='a'/> This graph has three "
            "clusters, joined by one edge between each pair, so it has three small eigenvalues. "
            "<bookmark mark='b'/> Give each vertex the coordinates of its entries in the second and third "
            "eigenvectors. The clusters collapse into three tight clumps, and any simple clustering of points, "
            "such as k-means, separates them. <bookmark mark='c'/> That is spectral clustering, in the forms "
            "popularized by Jianbo Shi and Jitendra Malik in 2000 for segmenting images, and by Andrew Ng, Michael "
            "Jordan and Yair Weiss in 2001. <bookmark mark='d'/> For sharding graphs with billions of edges, "
            "multilevel partitioners such as METIS, by George Karypis and Vipin Kumar, are faster, but they chase "
            "the same goal: few cut edges, balanced parts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(g[0]), FadeIn(g[1]), FadeIn(gcap), FadeIn(ill))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(axl), FadeIn(acap))
            self.play(*[d.animate.move_to(t) for d, t in zip(moved, targets)], run_time=2.2)
            self.play(*[d.animate.set_color(cols[i // 5]) for i, d in enumerate(moved)],
                      *[d.animate.set_color(cols[i // 5]) for i, d in enumerate(g[1])])
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO, YES)
