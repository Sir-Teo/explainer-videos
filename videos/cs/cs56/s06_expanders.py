from __future__ import annotations

import itertools
import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def adjacency(n, edges):
    A = np.zeros((n, n))
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def petersen():
    """The Petersen graph: an outer pentagon, five spokes, an inner pentagram."""
    pos = [(1.55 * math.cos(math.pi / 2 + 2 * math.pi * k / 5), 1.55 * math.sin(math.pi / 2 + 2 * math.pi * k / 5))
           for k in range(5)]
    pos += [(0.75 * math.cos(math.pi / 2 + 2 * math.pi * k / 5), 0.75 * math.sin(math.pi / 2 + 2 * math.pi * k / 5))
            for k in range(5)]
    edges = [(k, (k + 1) % 5) for k in range(5)] + [(k, k + 5) for k in range(5)]
    edges += [(5 + k, 5 + (k + 2) % 5) for k in range(5)]
    return pos, edges


def random_regular_edges(n, d, seed):
    """A random simple d-regular graph by pairing stubs, restarting on a loop or a repeated edge."""
    rng = random.Random(seed)
    while True:
        stubs = [v for v in range(n) for _ in range(d)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for a, b in zip(stubs[::2], stubs[1::2]):
            if a == b or (min(a, b), max(a, b)) in edges:
                ok = False
                break
            edges.add((min(a, b), max(a, b)))
        if ok:
            return sorted(edges)


def ring(n, radius):
    return [(radius * math.cos(math.pi / 2 - 2 * math.pi * k / n), radius * math.sin(math.pi / 2 - 2 * math.pi * k / n))
            for k in range(n)]


class Expanders(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.mixing()
        self.proof()
        self.alon()
        self.measured()
        self.existence()

    def card(self):
        card = chapter_card(5, r"Expanders", r"Can a graph be sparse and yet impossible to cut?",
                            lit=(1973, 1988), extra=((1973, r"Pinsker: \ random expanders"),
                                                     (1988, r"Lubotzky, \ Phillips and Sarnak")), part=PART)
        with self.voiceover("Chapter five. Expanders: graphs that are sparse, and yet impossible to cut."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ three definitions
    def definitions(self):
        head = label(r"Three ways to say \emph{expands}", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = petersen()
        n = 10
        A = adjacency(n, edges)
        # every set of at most half the vertices, by brute force
        sets = [S for k in range(1, 6) for S in itertools.combinations(range(n), k)]
        h = min(A[list(S)][:, [v for v in range(n) if v not in S]].sum() / len(S) for S in sets)
        eig = np.linalg.eigvalsh(A)
        lam = max(abs(eig[0]), abs(eig[-2]))
        d = 3
        lam2 = eig[-2]
        g = draw(pos, edges, center=LEFT * 4.5 + DOWN * 0.1, r=0.11)
        S = [v < 5 for v in range(n)]
        defs = VGroup(
            VGroup(label(r"edge expansion", font_size=22, color=HEAD),
                   MathTex(r"h(G) = \min_{0 < |S| \le n/2} \frac{|E(S, \bar S)|}{|S|}", font_size=30)),
            VGroup(label(r"vertex expansion", font_size=22, color=LAM),
                   MathTex(r"\min_{0 < |S| \le n/2} \frac{|N(S) \setminus S|}{|S|}", font_size=30)),
            VGroup(label(r"spectral expansion", font_size=22, color=YES),
                   MathTex(r"\lambda(G) = \max_{i \ge 2} |\lambda_i(A)|", font_size=30)),
        )
        for blk in defs:
            blk.arrange(RIGHT, buff=0.35)
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(RIGHT * 2.15 + UP * 1.1)
        xcol = max(blk[0].get_right()[0] for blk in defs)
        for blk in defs:
            blk[1].next_to([xcol, blk[0].get_y(), 0], RIGHT, buff=0.35)
        notes = VGroup(
            label(rf"Petersen: \ 5 edges leave the outer 5; \ over all {len(sets)} sets, \ $h = {h:.0f}$",
                  font_size=18, color=GREY_A),
            label(r"the outer 5 reach 5 new vertices", font_size=18, color=GREY_A),
            label(rf"eigenvalues $3,\ 1,\ -2$: \ $\lambda = {lam:.0f}$", font_size=18, color=GREY_A),
        )
        for nt, blk in zip(notes, defs):
            nt.next_to(blk, DOWN, buff=0.1).align_to(blk[1], LEFT)
        lo, hi = (d - lam2) / 2, math.sqrt(2 * d * (d - lam2))
        ch = VGroup(
            label(r"Cheeger \ (chapter 3), \ for a $d$-regular graph:", font_size=20, color=GREY_A),
            MathTex(r"\frac{d - \lambda_2}{2} \ \le\ h(G) \ \le\ \sqrt{2d\,(d - \lambda_2)}", font_size=34,
                    color=YES),
            label(rf"Petersen: \ ${lo:.0f} \le {h:.0f} \le {hi:.2f}$", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.15)
        box = SurroundingRectangle(ch, color=YES, buff=0.2, corner_radius=0.12, stroke_width=1.5)
        chg = VGroup(box, ch).next_to(notes[2], DOWN, buff=0.4).set_x(2.2)
        ill = note(r"the Petersen graph: \ 10 vertices, \ degree 3; \ all values computed", font_size=16).next_to(
            g, DOWN, buff=0.45)
        cut_anims = [ln.animate.set_stroke(HEAD if S[a] != S[b] else GREY_C, width=5 if S[a] != S[b] else 2)
                     for ln, (a, b) in zip(g[0], edges)]
        with self.voiceover(
            "What makes a graph an expander? <bookmark mark='a'/> Take the Petersen graph, ten vertices of degree "
            "three, and pick the outer five. <bookmark mark='b'/> Edge expansion counts the edges leaving a set, per "
            "vertex: here five leave five, a ratio of one, and no set of at most half the vertices does better. "
            "<bookmark mark='c'/> Vertex expansion counts the new neighbours a set reaches: all five inner ones. "
            "<bookmark mark='d'/> Spectral expansion asks that every eigenvalue but the top one, d, be small in size:"
            " here three, one and minus two, so lambda is two. <bookmark mark='e'/> Cheeger's inequality from chapter"
            " three, rescaled for degree d, ties the first to the third: a wide gap below d means no cheap cut. Keep "
            "that gap as the graphs grow, and they form a family of expanders."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[dt.animate.set_color(DATA) for dt, s in zip(g[1], S) if s])
            vo.wait_until("b")
            self.play(*cut_anims, FadeIn(defs[0]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(*[dt.animate.set_color(LAM) for dt, s in zip(g[1], S) if not s], FadeIn(defs[1]),
                      FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(defs[2]), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(chg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the mixing lemma, stated
    def mixing(self):
        head = label(r"The expander mixing lemma", font_size=36).to_edge(UP, buff=0.3)
        n, d = 20, 3
        edges = random_regular_edges(n, d, seed=7)
        pos = ring(n, 2.05)
        Sset = {0, 1, 2, 3, 4, 5}
        Tset = {10, 11, 12, 13, 14, 15, 16, 17}
        g = draw(pos, edges, center=LEFT * 4.3 + DOWN * 0.35, r=0.1, sw=1.6)
        est = sum(1 for a, b in edges if (a in Sset and b in Tset) or (b in Sset and a in Tset))
        hl = [ln.animate.set_stroke(HEAD, width=4.5) for ln, (a, b) in zip(g[0], edges)
              if (a in Sset and b in Tset) or (b in Sset and a in Tset)]
        cols = [dt.animate.set_color(DATA if v in Sset else LAM) for v, dt in enumerate(g[1])
                if v in Sset or v in Tset]
        sl = label(r"$S$", font_size=26, color=DATA).next_to(g.pts[3], RIGHT, buff=0.2)
        tl = label(r"$T$", font_size=26, color=LAM).next_to(g.pts[13], LEFT, buff=0.2)
        count = VGroup(
            label(rf"$e(S, T) = {est}$ \ edges between them", font_size=21, color=HEAD),
            label(rf"a random graph's average: \ $d\,|S|\,|T|/n = {d * len(Sset) * len(Tset) / n:.1f}$",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, DOWN, buff=0.25)
        if count.get_left()[0] < -6.8:
            count.shift(RIGHT * (-6.8 - count.get_left()[0]))
        ill = note(r"illustrative graph \ (random, \ degree 3); \ counts computed", font_size=16).to_corner(
            DL, buff=0.2)
        lemma = MathTex(r"\left|\, e(S,T) - \frac{d\,|S|\,|T|}{n} \,\right| \ \le\ \lambda \sqrt{|S|\,|T|}",
                        font_size=38, color=YES)
        dens = MathTex(r"\left|\, \frac{e(S,T)}{dn} - \frac{|S|}{n}\cdot\frac{|T|}{n} \,\right| \ \le\ "
                       r"\frac{\lambda}{d} \sqrt{\frac{|S|}{n}\cdot\frac{|T|}{n}}", font_size=34)
        right = VGroup(
            wrapped_label(r"for every pair of vertex sets $S$ and $T$ of a $d$-regular graph with second "
                          r"eigenvalue $\lambda$ \ ($e$ counts pairs $s \in S$, \ $t \in T$ that are joined):",
                          5.9, font_size=20, color=GREY_A),
            lemma,
            label(r"divide by $dn$: \ in densities,", font_size=20, color=GREY_A),
            dens,
            wrapped_label(r"the edges between any two large sets are as many as in a random graph, \ up to an "
                          r"error controlled by $\lambda / d$", 5.9, font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.3 + DOWN * 0.15)
        with self.voiceover(
            "<bookmark mark='a'/> Take any two sets of vertices, S and T, and count the edges between them. <bookmark"
            " mark='b'/> A random graph of the same degree would have about d times S times T over n. <bookmark "
            "mark='c'/> The expander mixing lemma says that an expander comes close to that for every pair of sets at"
            " once: the error is at most lambda times the square root of the product of their sizes. <bookmark "
            "mark='d'/> Read it in densities: the fraction of edges running from S to T is the product of the two "
            "densities, up to lambda over d. A small lambda makes a fixed, sparse graph look random to every large "
            "set."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(ill))
            vo.wait_until("a")
            self.play(*cols, FadeIn(sl), FadeIn(tl))
            self.play(*hl, FadeIn(count[0]))
            vo.wait_until("b")
            self.play(FadeIn(count[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), Write(lemma))
            vo.wait_until("d")
            self.play(FadeIn(right[2]), FadeIn(dens, shift=DOWN * 0.1))
            self.play(FadeIn(right[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the proof
    def proof(self):
        head = label(r"Proof of the mixing lemma", font_size=36).to_edge(UP, buff=0.3)
        fs = 36
        steps = VGroup(
            cmath(r"e(S,T)", r"=", r"\mathbf{1}_S^{\mathsf T} A\, \mathbf{1}_T", font_size=fs),
            cmath(r"\mathbf{1}_S = \tfrac{|S|}{n}\mathbf{1} + x,", r"\quad",
                  r"\mathbf{1}_T = \tfrac{|T|}{n}\mathbf{1} + y,", r"\quad", r"x,\ y \perp \mathbf{1}", font_size=fs),
            cmath(r"e(S,T)", r"=", r"\frac{|S|\,|T|}{n^2}", r"\mathbf{1}^{\mathsf T} A\, \mathbf{1}", r"+",
                  r"x^{\mathsf T} A\, y", font_size=fs),
            cmath(r"e(S,T)", r"=", r"\frac{d\,|S|\,|T|}{n}", r"+", r"x^{\mathsf T} A\, y", font_size=fs),
            cmath(r"|x^{\mathsf T} A\, y|", r"\le", r"\lambda\, \|x\|\, \|y\|", r"\le",
                  r"\lambda \sqrt{|S|\,|T|}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.6).shift(DOWN * 0.15)
        steps[3][2].set_color(DATA)
        steps[4][4].set_color(YES)
        whys = VGroup(
            label(r"$\mathbf{1}_S$: \ one on $S$, \ zero elsewhere", font_size=20, color=GREY_B),
            wrapped_label(r"split each into its average and the rest", 4.3, font_size=20, color=GREY_B),
            wrapped_label(r"$A\mathbf{1} = d\,\mathbf{1}$ and $x \perp \mathbf{1}$: \ both cross terms vanish",
                          4.3, font_size=20, color=GREY_B),
            wrapped_label(r"$\mathbf{1}^{\mathsf T} A \mathbf{1} = dn$, \ the sum of all degrees", 4.3,
                          font_size=20, color=GREY_B),
            wrapped_label(r"$A$ keeps $\perp \mathbf{1}$ and stretches it by at most $\lambda$; \ "
                          r"Cauchy--Schwarz; \ $\|x\|^2 = |S| - |S|^2/n \le |S|$", 4.3, font_size=20,
                          color=GREY_B),
        )
        for w, s in zip(whys, steps):
            w.set_x(4.55).set_y(s.get_y())
        punch = label(r"so \ $\left|\, e(S,T) - d\,|S|\,|T|/n \,\right| \le \lambda \sqrt{|S|\,|T|}$ \ \ $\square$",
                      font_size=26, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Write the count as the indicator of S, times A, times the indicator of T. <bookmark"
            " mark='b'/> Split each indicator into its average, a multiple of the all-ones vector, and a remainder "
            "orthogonal to it. <bookmark mark='c'/> Expand. A sends all ones to d times all ones, so both cross terms"
            " vanish. <bookmark mark='d'/> All ones, A, all ones is the sum of the degrees, and the first term is "
            "exactly the random graph's count. <bookmark mark='e'/> The rest is the error. A keeps vectors orthogonal"
            " to all ones and stretches them by at most lambda, so by Cauchy–Schwarz the error is at most lambda "
            "times the two remainders' lengths, each shorter than its indicator. <bookmark mark='f'/> That is the "
            "lemma."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[0].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4], shift=DOWN * 0.1), FadeIn(whys[4]))
            vo.wait_until("f")
            self.play(FadeIn(punch))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Alon-Boppana
    def alon(self):
        head = label(r"How small can $\lambda$ be?", font_size=36).to_edge(UP, buff=0.3)
        # the 3-regular tree to depth 3, drawn radially
        center = LEFT * 4.6 + UP * 0.2
        pos, edges, parent = [(0.0, 0.0)], [], {0: None}
        level = [(0, -math.pi, math.pi)]
        radii = [0.0, 0.75, 1.45, 2.1]
        for depth in (1, 2, 3):
            nxt = []
            for v, a0, a1 in level:
                k = 3 if depth == 1 else 2
                for j in range(k):
                    b0 = a0 + (a1 - a0) * j / k
                    b1 = a0 + (a1 - a0) * (j + 1) / k
                    mid = (b0 + b1) / 2
                    pos.append((radii[depth] * math.cos(mid), radii[depth] * math.sin(mid)))
                    u = len(pos) - 1
                    edges.append((v, u))
                    parent[u] = v
                    nxt.append((u, b0, b1))
            level = nxt
        g = draw(pos, edges, center=center, r=0.07, color=GREY_A, sw=1.8)
        g[1][0].set_color(HEAD).scale(1.4)
        walk = [0, 1, 4, 1, 0, 2, 0]   # a closed walk of length 6 from the root
        walker = Dot(g.pts[0], radius=0.13, color=HEAD)
        tl = label(r"a closed walk of length $2k$ from the root", font_size=19, color=HEAD).next_to(
            g, DOWN, buff=0.3)
        fs = 30
        steps = VGroup(
            cmath(r"\operatorname{tr} A^{2k}", r"=", r"\sum_i \lambda_i^{2k}", r"\le",
                  r"d^{2k} + (n-1)\,\lambda^{2k}", font_size=fs),
            cmath(r"\operatorname{tr} A^{2k}", r"\ge", r"n\, C_k\, (d-1)^k", font_size=fs),
            cmath(r"\lambda^{2k}", r"\ge", r"\frac{n\, C_k\, (d-1)^k - d^{2k}}{n-1}", font_size=fs),
            cmath(r"\lambda", r"\ge", r"2\sqrt{d-1}", r"- o(1)", font_size=fs),
        )
        steps[3].set_color(YES)
        whys = VGroup(
            label(r"the trace counts closed walks; \ one eigenvalue is $d$, \ the rest at most $\lambda$ in size",
                  font_size=18, color=GREY_B),
            wrapped_label(r"every vertex has at least the tree's closed walks: \ $C_k$ shapes \ (Catalan), \ "
                          r"at least $d - 1$ choices for each step out", 6.6, font_size=18, color=GREY_B),
            label(r"put the two together", font_size=18, color=GREY_B),
            label(r"$C_k \approx 4^k / k^{3/2}$; \ take $k$ a small multiple of $\log n$", font_size=18,
                  color=GREY_B),
        )
        ladder = VGroup(*[VGroup(s, w).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for s, w in zip(steps, whys)])
        ladder.arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35).set_y(0.6)
        thm = VGroup(
            label(r"Alon--Boppana: \ $\lambda_2 \ge 2\sqrt{d-1} - o(1)$ \ as $n \to \infty$", font_size=22,
                  color=YES),
            label(r"\textbf{Ramanujan graph}: \ $\lambda \le 2\sqrt{d-1}$, \ the best possible "
                  r"\ (Lubotzky, \ Phillips and Sarnak, \ 1988)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How small can lambda be? <bookmark mark='a'/> Compare any regular graph with the infinite tree of degree"
            " d. <bookmark mark='b'/> The trace of A to the two k counts closed walks, and equals the sum of the "
            "eigenvalues to that power: d to the two k from the top one, at most lambda to the two k from each other."
            " <bookmark mark='c'/> But every vertex has at least the tree's closed walks: a Catalan number of shapes,"
            " with at least d minus one choices per step out. <bookmark mark='d'/> Combine, <bookmark mark='e'/> take"
            " k a small multiple of log n, and lambda can fall below twice the square root of d minus one by only a "
            "vanishing amount. <bookmark mark='f'/> That is the Alon–Boppana bound. Graphs that meet it are Ramanujan"
            " graphs; Lubotzky, Phillips and Sarnak built the first families in 1988."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(FadeIn(walker), FadeIn(tl))
            for v in walk[1:]:
                self.play(walker.animate.move_to(g.pts[v]), run_time=0.35)
            vo.wait_until("b")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2], shift=DOWN * 0.1), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(thm))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ measured
    def measured(self):
        rows = load("regular")["rows"]
        head = label(r"Random regular graphs are nearly Ramanujan", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[2, 13, 1], y_range=[0, 13, 2], x_length=5.4, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 3.5 + DOWN * 0.35)
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (3, 4, 6, 8, 12)])
        yt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(2, v), LEFT, buff=0.1)
                      for v in (0, 4, 8, 12)])
        xl = label(r"degree $d$", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"eigenvalue", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        triv = DashedLine(ax.c2p(2, 2), ax.c2p(13, 13), color=GREY_B, stroke_width=1.8)
        trl = label(r"$d$: \ the top eigenvalue", font_size=17, color=GREY_B).next_to(ax.c2p(9.5, 9.5), LEFT,
                                                                                   buff=0.15)
        ram = VMobject(color=HEAD, stroke_width=3).set_points_smoothly(
            [ax.c2p(2 + 0.25 * i, 2 * math.sqrt(1 + 0.25 * i)) for i in range(45)])
        raml = label(r"$2\sqrt{d-1}$", font_size=19, color=HEAD).next_to(ax.c2p(12.5, 2 * math.sqrt(11.5)), DOWN,
                                                                          buff=0.2)
        dots = VGroup(*[Dot(ax.c2p(r["d"], r["lambda"]), radius=0.07, color=YES) for r in rows])
        tab = grid_table([r"$d$", r"$\lambda$ measured", r"$2\sqrt{d-1}$", r"mixing error"],
                         [[rf"{r['d']:.0f}", rf"{r['lambda']:.3f}", rf"{r['ramanujan']:.3f}",
                           rf"{r['mixing_worst']:.2f}"] for r in rows],
                         widths=[0.6, 1.5, 1.35, 1.45], row_h=0.5, font_size=19,
                         colors=[[WHITE, YES, HEAD, LAM]] * len(rows), mono_cols=())
        tab.move_to(RIGHT * 3.55 + UP * 1.05)
        side = VGroup(
            wrapped_label(r"one random $d$-regular graph on 400 vertices for each $d$; \ $\lambda$: \ the largest "
                          r"eigenvalue in size after $d$", 5.4, font_size=18, color=GREY_A),
            wrapped_label(r"mixing error: \ the worst $|e(S,T) - d|S||T|/n| / \sqrt{|S||T|}$ over 200 random "
                          r"pairs of sets; \ the lemma allows up to $\lambda$", 5.4, font_size=18, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        with self.voiceover(
            "Now measure. <bookmark mark='a'/> One random regular graph on four hundred vertices for each of five "
            "degrees, from three to twelve. <bookmark mark='b'/> The top eigenvalue is always d; the yellow curve is "
            "the Ramanujan bound. <bookmark mark='c'/> Every measured lambda sits just below it: two point eight two "
            "against two point eight three at degree three, six point four two against six point six three at degree "
            "twelve. Coin flips come close to the best possible; chapter eleven says why. <bookmark mark='d'/> And "
            "the mixing lemma, on two hundred random pairs of sets: the worst error is between a fifth and a third, "
            "far inside lambda."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), *[FadeIn(r[0]) for r in tab.cells[1:]],
                      FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(triv), FadeIn(trl), Create(ram), FadeIn(raml))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.25),
                      *[FadeIn(VGroup(r[1], r[2])) for r in tab.cells[1:]])
            vo.wait_until("d")
            self.play(*[FadeIn(r[3]) for r in tab.cells[1:]], FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ existence by counting
    def existence(self):
        head = label(r"Expanders exist: \ count and union-bound", font_size=36).to_edge(UP, buff=0.3)
        n, d = 8, 3
        rng = random.Random(3)
        choice = [rng.sample(range(n), d) for _ in range(n)]
        L = [(-0.8, 1.55 - 0.45 * i) for i in range(n)]
        R = [(0.8, 1.55 - 0.45 * i) for i in range(n)]
        edges = [(i, n + j) for i in range(n) for j in choice[i]]
        g = draw(L + R, edges, center=LEFT * 5.2 + DOWN * 0.3, r=0.08, sw=1.4)
        S = {1, 4, 6}
        NS = {j for i in S for j in choice[i]}
        hl = [ln.animate.set_stroke(HEAD, width=3.5) for ln, (a, b) in zip(g[0], edges) if a in S]
        cols = [g[1][i].animate.set_color(DATA) for i in S] + [g[1][n + j].animate.set_color(YES) for j in NS]
        cap = label(rf"$|S| = {len(S)}$, \ $|N(S)| = {len(NS)}$", font_size=19, color=GREY_A).next_to(g, DOWN,
                                                                                                     buff=0.3)
        ill = note(r"illustrative: \ each left vertex picks 3 right neighbours", font_size=16).next_to(
            cap, DOWN, buff=0.12)
        if ill.get_left()[0] < -6.85:
            ill.shift(RIGHT * (-6.85 - ill.get_left()[0]))
        fs = 30
        steps = VGroup(
            cmath(r"\Pr[N(S) \subseteq T]", r"=", r"\left(\frac{|T|}{n}\right)^{d|S|}", font_size=fs),
            cmath(r"p_s", r"\le", r"\binom{n}{s}", r"\binom{n}{\alpha s}", r"\left(\frac{\alpha s}{n}\right)^{ds}",
                  font_size=fs),
            cmath(r"p_s", r"\le", r"\left(\frac{en}{s}\right)^{s}", r"\left(\frac{en}{\alpha s}\right)^{\alpha s}",
                  r"\left(\frac{\alpha s}{n}\right)^{ds}", font_size=fs),
            cmath(r"p_s", r"\le", r"\left[\, e^{1+\alpha}\, \alpha^{d-\alpha} \left(\frac{s}{n}\right)^{d-1-\alpha}"
                  r"\right]^{s}", font_size=fs),
            cmath(r"\sum_{s=1}^{\delta n} p_s", r"\le", r"\sum_{s=1}^{\delta n} 2^{-s}", r"<", r"1", font_size=fs),
        )
        steps[4][4].set_color(YES)
        whys = VGroup(
            wrapped_label(r"each of the $d|S|$ edges from $S$ lands in $T$ with chance $|T|/n$", 4.8,
                          font_size=19, color=GREY_B),
            wrapped_label(r"$p_s$: \ some $|S| = s$ has $|N(S)| \le \alpha s$; \ union bound over $S$ and $T$",
                          4.8, font_size=19, color=GREY_B),
            label(r"$\binom{n}{k} \le (en/k)^k$", font_size=19, color=GREY_B),
            label(r"collect the powers of $s/n$", font_size=19, color=GREY_B),
            wrapped_label(r"if $d > \alpha + 1$ and $s \le \delta n$ with $\delta$ small, \ the bracket is at "
                          r"most $\tfrac12$", 4.8, font_size=19, color=GREY_B),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.3)
        steps.set_x(-3.3 + steps.width / 2)
        for w, st in zip(whys, steps):
            w.next_to([2.0, st.get_y(), 0], RIGHT, buff=0)
        punch = label(r"so some degree-$d$ graph makes every set of up to $\delta n$ vertices expand by more than "
                      r"$\alpha$: \ Pinsker \ (1973)", font_size=20, color=YES).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Do expanders exist? Counting says yes, as in Part 2. <bookmark mark='a'/> Let each of n vertices on the "
            "left pick d random neighbours on the right. <bookmark mark='b'/> A set S has all its neighbours inside a"
            " set T only if all of its d times S edges land there. <bookmark mark='c'/> Take a union bound over every"
            " S of size s and every T of size alpha s, <bookmark mark='d'/> bound the binomials, <bookmark mark='e'/>"
            " and collect the powers: when d exceeds alpha plus one and sets are small, the bracket is below a half. "
            "<bookmark mark='f'/> Summed over all sizes, the chance that some small set fails is below one, so some "
            "graph never fails. Mark Pinsker used counting like this in 1973. <bookmark mark='g'/> But coin flips are"
            " not a construction: a random graph on two to the hundred vertices cannot even be stored."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(ill))
            vo.wait_until("a")
            self.play(*cols, *hl, FadeIn(cap))
            vo.wait_until("b")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(steps[4], shift=DOWN * 0.1), FadeIn(whys[4]))
            self.play(FadeIn(punch))
            vo.wait_until("g")
            self.play(Indicate(punch, color=HEAD))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, NO)
