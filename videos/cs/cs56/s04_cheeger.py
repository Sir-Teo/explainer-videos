from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


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


def vcolor(v, vmax):
    """An eigenvector entry as a colour: blue below zero, orange above, grey at zero."""
    a = float(np.clip(v / vmax, -1, 1))
    return interpolate_color(ManimColor(GREY_C), ManimColor(KERN if a > 0 else DATA), abs(a) ** 0.7)


def toy():
    """Two hexagons with two chords each (12 vertices), joined by two parallel bridges."""
    pos, edges = [], []
    for c, off in ((-1.45, 0), (1.45, 6)):
        for k in range(6):
            a = 2 * math.pi * k / 6
            pos.append((c + 0.85 * math.cos(a), 0.85 * math.sin(a)))
        edges += [(off + k, off + (k + 1) % 6) for k in range(6)] + [(off, off + 2), (off + 3, off + 5)]
    return pos, edges + [(0, 9), (1, 8)]


def fiedler_normalized(A):
    """The second eigenvector of the normalized Laplacian, scaled by D^-1/2 (the sweep's order), and lambda_2."""
    d = A.sum(axis=1)
    N = np.eye(len(A)) - A / np.sqrt(np.outer(d, d))
    w, V = np.linalg.eigh(N)
    return V[:, 1] / np.sqrt(d), float(w[1])


def cut_stats(A, S):
    S = np.asarray(S, bool)
    d = A.sum(axis=1)
    cut = float(A[S][:, ~S].sum())
    return cut, float(d[S].sum()), float(d[~S].sum())


class Cheeger(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.easy()
        self.shift()
        self.threshold()
        self.sweep()
        self.check()

    def card(self):
        card = chapter_card(3, r"Cheeger's inequality", r"Does a small eigenvalue promise a cheap cut?",
                            lit=(1970, 1985), extra=((1970, r"Cheeger: \ curved manifolds"),
                                                     (1985, r"Alon and Milman: \ graphs")), part=PART)
        with self.voiceover("Chapter three. Cheeger's inequality, and the sweep cut."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def define(self):
        head = label(r"Conductance: \ how cheap is the cheapest cut?", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = toy()
        n = 12
        A = adjacency(n, edges)
        g = draw(pos, edges, center=LEFT * 3.4 + UP * 0.85, scale=0.95, r=0.12)
        defs = VGroup(
            MathTex(r"\mathrm{vol}\,S = \sum_{i \in S} d_i", font_size=30),
            MathTex(r"\phi(S) = \frac{|E(S, \bar S)|}{\min(\mathrm{vol}\,S,\ \mathrm{vol}\,\bar S)}", font_size=30),
            MathTex(r"\phi(G) = \min_{S} \phi(S)", font_size=30, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + UP * 1.2)

        def show(S, col):
            cut, v1, v2 = cut_stats(A, S)
            anims = [d.animate.set_color(col if s else WHITE) for d, s in zip(g[1], S)]
            anims += [ln.animate.set_stroke(NO if S[a] != S[b] else GREY_C, width=5 if S[a] != S[b] else 2)
                      for ln, (a, b) in zip(g[0], edges)]
            t = label(rf"cut {cut:.0f} edges, \ volume {min(v1, v2):.0f}: \ $\phi = {cut / min(v1, v2):.2f}$",
                      font_size=22, color=col).next_to(g, DOWN, buff=0.35)
            return anims, t
        S1 = [i in (3, 4, 5) for i in range(n)]
        S2 = [i < 6 for i in range(n)]
        a1, t1 = show(S1, NO)
        a2, t2 = show(S2, YES)
        thm = VGroup(
            label(r"Cheeger's inequality, \ for $\lambda_2$ of the normalized Laplacian $N$:", font_size=22,
                  color=GREY_A),
            MathTex(r"\frac{\lambda_2}{2} \ \le\ \phi(G) \ \le\ \sqrt{2\,\lambda_2}", font_size=44, color=YES),
        ).arrange(DOWN, buff=0.25)
        box = SurroundingRectangle(thm, color=YES, buff=0.25, corner_radius=0.12, stroke_width=1.5)
        thm_g = VGroup(box, thm).to_edge(DOWN, buff=0.4)
        hist = wrapped_label(r"Cheeger \ (1970) \ for manifolds; \ for graphs, \ Dodziuk \ (1984) \ and Alon and "
                             r"Milman \ (1985)", 5.6, font_size=19, color=GREY_A).next_to(defs, DOWN, buff=0.45)
        hist.align_to(defs, LEFT)
        ill = note(r"illustrative graph", font_size=16).next_to(t1, DOWN, buff=0.1)
        with self.voiceover(
            "Chapter two cut graphs with an eigenvector; now we prove how well it cuts. <bookmark mark='a'/> The volume of a set of vertices is the sum of their degrees, "
            "<bookmark mark='b'/> and the conductance of a cut is the number of edges it crosses, divided by the "
            "volume of the smaller side. <bookmark mark='c'/> Cutting off three vertices crosses two edges, but "
            "the side is small: conductance a quarter. <bookmark mark='d'/> Cutting between the clusters crosses "
            "the same two edges with a far bigger side: one ninth. <bookmark mark='e'/> The conductance of the "
            "graph is that of its best cut, and finding it is NP-hard. <bookmark mark='f'/> Cheeger's inequality "
            "says lambda two of the normalized Laplacian pins it down from both sides: at least half of lambda "
            "two, at most the square root of twice lambda two. Jeff Cheeger proved it for curved manifolds in "
            "1970; the graph versions followed in the nineteen-eighties."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(Write(defs[0]))
            vo.wait_until("b")
            self.play(Write(defs[1]))
            vo.wait_until("c")
            self.play(*a1, FadeIn(t1), FadeIn(ill))
            vo.wait_until("d")
            self.play(*a2, ReplacementTransform(t1, t2))
            vo.wait_until("e")
            self.play(Write(defs[2]))
            vo.wait_until("f")
            self.play(FadeIn(thm_g), FadeIn(hist))
        self.wait(0.4)
        self.clear_scene()

    def easy(self):
        head = label(r"The easy side: \ $\lambda_2 \le 2\,\phi(G)$", font_size=36).to_edge(UP, buff=0.3)
        cut = r"|E(S, \bar S)|"
        steps = VGroup(
            cmath(r"\lambda_2", r"=", r"\min_{\sum_i d_i y_i = 0}",
                  r"\frac{\sum_{(i,j) \in E} (y_i - y_j)^2}{\sum_i d_i y_i^2}", font_size=30),
            cmath(r"y", r"=", r"a\,\mathbf{1}_S", r"-", r"b\,\mathbf{1}_{\bar S}", r",\quad",
                  r"a = \tfrac{1}{\mathrm{vol}\,S},\ \ b = \tfrac{1}{\mathrm{vol}\,\bar S}", font_size=30),
            cmath(r"\lambda_2", r"\le", r"\frac{" + cut + r"\,(a + b)^2}{\mathrm{vol}\,S\, a^2 + "
                  r"\mathrm{vol}\,\bar S\, b^2}", r"=", r"\frac{" + cut + r"\,(a + b)^2}{a + b}", font_size=30),
            cmath(r"\lambda_2", r"\le", cut, r"\,(a + b)", font_size=30),
            cmath(r"\lambda_2", r"\le", r"\frac{2\," + cut + r"}{\min(\mathrm{vol}\,S,\ \mathrm{vol}\,\bar S)}",
                  r"=", r"2\,\phi(S)", font_size=30),
        )
        steps[4][4].set_color(YES)
        whys = VGroup(
            label(r"$N$'s quotient, \ with $x = D^{1/2} y$", font_size=18, color=GREY_B),
            label(r"one value on $S$, \ another off it: \ $\sum d_i y_i = 1 - 1 = 0$", font_size=18,
                  color=GREY_B),
            label(r"only cut edges have a difference, \ $a + b$", font_size=18, color=GREY_B),
            label(r"cancel one factor", font_size=18, color=GREY_B),
            label(r"$a$ and $b$ are each at most $1/\min$", font_size=18, color=GREY_B),
        )
        pairs = VGroup(*[VGroup(s_, w).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for s_, w in zip(steps, whys)])
        pairs.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 2.3 + DOWN * 0.25)
        pos, edges = toy()
        g = draw(pos, edges, center=LEFT * 4.3 + UP * 0.6, scale=0.78, r=0.11)
        for d, i in zip(g[1], range(12)):
            d.set_color(KERN if i < 6 else DATA)
        for ln, (a, b) in zip(g[0], edges):
            if (a < 6) != (b < 6):
                ln.set_stroke(NO, width=5)
        vals = VGroup(label(r"$y = 1/\mathrm{vol}\,S$", font_size=19, color=KERN),
                      label(r"$y = -1/\mathrm{vol}\,\bar S$", font_size=19, color=DATA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(g, DOWN, buff=0.4)
        concl = wrapped_label(r"true for every $S$, \ so for the best one: \ $\lambda_2 / 2 \le \phi(G)$. \ A small "
                              r"cut forces a small $\lambda_2$", 4.4, font_size=20, color=YES).next_to(
            vals, DOWN, buff=0.4)
        with self.voiceover(
            "The easy direction says that a cheap cut forces a small eigenvalue. <bookmark mark='a'/> Write lambda "
            "two of the normalized Laplacian as a minimum over vectors y, by substituting x equals the square root "
            "of D times y. Now we need just one good test vector. <bookmark mark='b'/> Take any set S, and put one "
            "over its volume on S and minus one over the other side's volume off it. Its degree-weighted sum is "
            "zero, so it is allowed. <bookmark mark='c'/> Only the cut edges have a difference across them, all the "
            "same size. <bookmark mark='d'/> One factor cancels, <bookmark mark='e'/> and each of the two terms is "
            "at most one over the smaller volume. So lambda two is at most twice the conductance of S, for every "
            "S, and in particular for the best."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]), Create(g[0]), FadeIn(g[1]), FadeIn(vals))
            vo.wait_until("c")
            self.play(FadeIn(steps[2], shift=DOWN * 0.1), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]))
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()

    def shift(self):
        head = label(r"The hard side, \ step 1: \ one half of the Fiedler vector", font_size=36).to_edge(UP,
                                                                                                    buff=0.3)
        pos, edges = toy()
        A = adjacency(12, edges)
        d = A.sum(axis=1)
        f, lam2 = fiedler_normalized(A)
        f = f if f[0] > 0 else -f
        order = np.argsort(f)
        cum = np.cumsum(d[order])
        med = float(f[order[int(np.searchsorted(cum, d.sum() / 2))]])
        mx = float(max(np.abs(f).max(), np.abs(f - med).max())) * 1.05
        nl = NumberLine(x_range=[-1, 1, 0.5], length=11.5, color=GREY_C, include_numbers=False).move_to(UP * 0.45)
        z0 = label(r"$0$", font_size=18, color=GREY_B).next_to(nl.n2p(0), DOWN, buff=0.15)
        cap = label(r"the entries of $y$, \ the Fiedler vector of $N$ scaled by $D^{-1/2}$, \ for the two-bridge "
                    r"graph", font_size=19, color=GREY_A).next_to(nl, UP, buff=0.9)
        dots = VGroup()
        for rank, i in enumerate(order):
            dots.add(Dot(nl.n2p(f[i] / mx) + UP * (0.32 if rank % 2 else 0.14), radius=0.09,
                         color=vcolor(f[i], mx)))
        medl = DashedLine(nl.n2p(med / mx) + UP * 0.6, nl.n2p(med / mx) + DOWN * 0.25, color=HEAD)
        medt = label(r"weighted median $c$", font_size=18, color=HEAD).next_to(medl, UP, buff=0.08)
        steps = VGroup(
            MathTex(r"R(y - c\mathbf{1}) \ \le\ R(y) = \lambda_2", font_size=30),
            MathTex(r"(a - b)^2 \ \ge\ (a^+ - b^+)^2 + (a^- - b^-)^2", font_size=30),
            MathTex(r"z \ge 0,\quad \mathrm{vol}(\mathrm{supp}\, z) \le \tfrac12 \mathrm{vol}\,V,\quad R(z) \le "
                    r"\lambda_2", font_size=30, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(LEFT * 2.3 + DOWN * 1.9)
        whys = VGroup(
            label(r"the numerator is unchanged; \ $\sum d_i (y_i - c)^2 = \sum d_i y_i^2 + c^2\,\mathrm{vol}\,V$",
                  font_size=18, color=GREY_B),
            label(r"so the positive part or the negative part does as well", font_size=18, color=GREY_B),
            label(r"call that part $z$", font_size=18, color=GREY_B),
        )
        for w, s in zip(whys, steps):
            w.next_to(s, RIGHT, buff=0.35)
        shift_by = nl.n2p(0) - nl.n2p(med / mx)
        R = lambda y: float(sum((y[a] - y[b]) ** 2 for a, b in edges) / (d * y ** 2).sum())  # noqa: E731
        ys = f - med
        yp, ym = np.maximum(ys, 0), np.maximum(-ys, 0)
        rp, rm = R(yp), R(ym)
        keep_pos = rp <= rm
        fade = [k for k, i in enumerate(order) if (ys[i] <= 0 if keep_pos else ys[i] >= 0)]
        with self.voiceover(
            "The hard direction is the surprise: a small eigenvalue guarantees a cheap cut, and the proof finds it. "
            "Start from the eigenvector, y, whose quotient is lambda two. <bookmark mark='a'/> Lay its entries on "
            "a line. <bookmark mark='b'/> Find the point c where the volume on either side is at most half, and "
            "shift everything by c. That leaves the numerator alone and only grows the denominator. "
            "<bookmark mark='c'/> Now split the shifted vector into its positive and negative parts. "
            "Across any edge, the two parts' squared differences add up to at most the original one, so one of the "
            "parts has a quotient no bigger than lambda two. <bookmark mark='d'/> Call it z: never negative, "
            "living on at most half the volume, with quotient at most lambda two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(nl), FadeIn(z0), FadeIn(cap), LaggedStart(*[FadeIn(x_) for x_ in dots],
                                                                       lag_ratio=0.08))
            vo.wait_until("b")
            self.play(Create(medl), FadeIn(medt))
            self.play(VGroup(dots, medl, medt).animate.shift(shift_by), FadeIn(steps[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            self.play(*[dots[k].animate.set_color(GREY_D) for k in fade])
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()
        self.lam2 = lam2

    def threshold(self):
        head = label(r"The hard side, \ step 2: \ cut at a random threshold", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"\Pr[i \in S_t] = z_i^2,", r"\quad", r"\Pr[(i,j)\ \text{cut}] = |z_i^2 - z_j^2|",
                    font_size=28),
            cmath(r"\mathbb{E}\,|E(S_t, \bar S_t)|", r"=", r"\sum_{E} |z_i - z_j|\,(z_i + z_j)", font_size=28),
            cmath(r"\mathbb{E}\,|E(S_t, \bar S_t)|", r"\le", r"\sqrt{\textstyle\sum_E (z_i - z_j)^2}",
                  r"\sqrt{\textstyle\sum_E (z_i + z_j)^2}", font_size=28),
            cmath(r"\mathbb{E}\,|E(S_t, \bar S_t)|", r"\le", r"\sqrt{\textstyle\sum_E (z_i - z_j)^2}",
                  r"\sqrt{2 \textstyle\sum_i d_i z_i^2}", font_size=28),
            cmath(r"\frac{\mathbb{E}\,|E(S_t, \bar S_t)|}{\mathbb{E}\,\mathrm{vol}\,S_t}", r"\le",
                  r"\sqrt{2\,R(z)}", r"\le", r"\sqrt{2\,\lambda_2}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(LEFT * 1.95 + DOWN * 0.15)
        steps[4][4].set_color(YES)
        whys = VGroup(
            label(r"scale so $\max z = 1$; \ pick $t$ uniformly in $(0, 1]$; \ $S_t = \{i : z_i^2 \ge t\}$",
                  font_size=18, color=HEAD),
            label(r"$z_i^2 - z_j^2 = (z_i - z_j)(z_i + z_j)$", font_size=18, color=GREY_B),
            label(r"Cauchy--Schwarz", font_size=18, color=GREY_B),
            label(r"$(a + b)^2 \le 2a^2 + 2b^2$; \ each vertex in $d_i$ edges", font_size=18, color=GREY_B),
            label(r"$\mathbb{E}\,\mathrm{vol}\,S_t = \sum_i d_i z_i^2$", font_size=18, color=GREY_B),
        )
        for w, s in zip(whys[1:], steps[1:]):
            w.next_to(s, DOWN, buff=0.05).align_to(s, LEFT)
        whys[0].next_to(steps[0], UP, buff=0.12).align_to(steps[0], LEFT)
        concl = wrapped_label(r"the averages obey it, \ so some threshold does: \ $\phi(S_t) \le \sqrt{2\lambda_2}$, "
                              r"\ and every $S_t$ is a stretch of the Fiedler order: \ a \textbf{sweep cut}", 12.6,
                              font_size=21, color=YES).to_edge(DOWN, buff=0.25)
        # the threshold picture: z^2 for the toy graph's positive part, and a level t
        pos, edges = toy()
        A = adjacency(12, edges)
        d = A.sum(axis=1)
        f, _ = fiedler_normalized(A)
        f = f if f[0] > 0 else -f
        order = np.argsort(f)
        cum = np.cumsum(d[order])
        med = float(f[order[int(np.searchsorted(cum, d.sum() / 2))]])
        z = np.maximum(f - med, 0)
        z = z / z.max()
        ax = CornerAxes(x_range=[0, 7, 1], y_range=[0, 1, 0.5], x_length=2.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(RIGHT * 5.4 + UP * 0.1)
        yl = label(r"$z_i^2$", font_size=20, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        zs = sorted([float(v) ** 2 for v in z if v > 0], reverse=True)
        pts = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.07, color=KERN) for k, v in enumerate(zs)])
        t = ValueTracker(0.85)
        level = always_redraw(lambda: DashedLine(ax.c2p(0, t.get_value()), ax.c2p(7, t.get_value()), color=HEAD))
        tl = always_redraw(lambda: label(r"$t$", font_size=20, color=HEAD).next_to(ax.c2p(7, t.get_value()), RIGHT,
                                                                                 buff=0.08))

        def upd(g):
            for p_, v in zip(g, zs):
                p_.set_color(YES if v >= t.get_value() else KERN)
        pts.add_updater(upd)
        tcap = label(r"$S_t$: \ the dots above $t$", font_size=18, color=YES).next_to(ax, DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Scale z so its largest entry is one, pick t "
            "uniformly between zero and one, and keep the vertices whose squared value is at least t. A vertex is "
            "kept with probability z i squared, and an edge is cut when t falls between its two ends' squares. "
            "<bookmark mark='b'/> So the expected number of cut edges is a sum of differences of squares, "
            "<bookmark mark='c'/> which Cauchy–Schwarz splits into two square roots: <bookmark mark='d'/> the first "
            "is the numerator of z's quotient, and the second at most root two times its denominator. "
            "<bookmark mark='e'/> The expected volume is exactly that denominator. So, on average, cut edges over "
            "volume is at most the square root of twice lambda two. <bookmark mark='f'/> Some threshold must do at "
            "least as well as the average, and every threshold set is a stretch at one end of the Fiedler order. "
            "So some sweep cut meets the bound."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(pts), FadeIn(tcap))
            vo.wait_until("a")
            self.play(FadeIn(whys[0]), FadeIn(level), FadeIn(tl))
            self.play(Write(steps[0]), t.animate.set_value(0.3), run_time=2)
            self.play(t.animate.set_value(0.6), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]), FadeIn(whys[4]))
            vo.wait_until("f")
            self.play(FadeIn(concl), t.animate.set_value(0.15), run_time=1.5)
        self.wait(0.4)
        pts.clear_updaters()
        self.clear_scene()

    def sweep(self):
        p = load("partition")
        curve = p["sweep_curve"]
        kbest = int(np.argmin(curve)) + 1
        head = label(r"The sweep cut", font_size=36).to_edge(UP, buff=0.3)
        pos, edges = toy()
        n = 12
        A = adjacency(n, edges)
        f, _ = fiedler_normalized(A)
        order = np.argsort(f)
        g = draw(pos, edges, center=LEFT * 4.15 + UP * 1.25, scale=0.84, r=0.11)
        rank = {int(i): k for k, i in enumerate(order)}
        nums = VGroup(*[label(rf"{rank[i] + 1}", font_size=15, color=GREY_A).next_to(
            g.pts[i], UP if pos[i][1] >= 0 else DOWN, buff=0.1) for i in range(n)])
        ncap = label(r"numbers: \ the Fiedler order", font_size=17, color=GREY_A).next_to(g, DOWN, buff=0.4)
        ax = CornerAxes(x_range=[0, 12, 2], y_range=[0, 1, 0.5], x_length=4.2, y_length=2.0, tips=False,
                        axis_config={"stroke_color": GREY_C}).next_to(ncap, DOWN, buff=0.45)
        axy = VGroup(*[label(rf"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                       for v in (0, 0.5, 1)])
        axl = label(r"$\phi$ of the first $k$", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(
            ax, LEFT)
        phis = []
        for k in range(1, n):
            S = np.zeros(n, bool)
            S[order[:k]] = True
            c, v1, v2 = cut_stats(A, S)
            phis.append(c / min(v1, v2))
        kb = int(np.argmin(phis)) + 1
        pdots = VGroup(*[Dot(ax.c2p(k, min(v, 1.0)), radius=0.05, color=HEAD) for k, v in enumerate(phis, 1)])
        # the real experiment
        bx = CornerAxes(x_range=[0, 120, 20], y_range=[0, 1, 0.25], x_length=6.0, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(RIGHT * 2.9 + UP * 0.05)
        bxt = VGroup(*[label(rf"{v}", font_size=15, color=GREY_B).next_to(bx.c2p(v, 0), DOWN, buff=0.08)
                       for v in (0, 60, 120)])
        byt = VGroup(*[label(rf"{v:g}", font_size=15, color=GREY_B).next_to(bx.c2p(0, v), LEFT, buff=0.08)
                       for v in (0, 0.5, 1)])
        bxl = label(r"$k$: \ first $k$ vertices of the Fiedler order", font_size=17, color=GREY_A).next_to(
            bxt, DOWN, buff=0.08)
        byl = label(r"conductance of the sweep set, \ chapter 2's 120-vertex graph", font_size=17,
                    color=GREY_A).next_to(bx, UP, buff=0.12).align_to(bx, LEFT)
        line = VMobject(color=DATA, stroke_width=3).set_points_as_corners(
            [bx.c2p(k, min(v, 1.0)) for k, v in enumerate(curve, 1)])
        best = Dot(bx.c2p(kbest, curve[kbest - 1]), radius=0.08, color=YES)
        bestl = label(rf"best: \ $k = {kbest}$, \ $\phi = {p['sweep_phi']:.3f}$", font_size=19,
                      color=YES).next_to(bxl, DOWN, buff=0.22)
        truth = wrapped_label(rf"the planted split has $\phi = {p['true_phi']:.3f}$: \ the sweep found exactly it",
                              6.0, font_size=19, color=WHITE).next_to(bestl, DOWN, buff=0.12)
        ill = note(r"left: \ illustrative graph", font_size=15).to_corner(DL, buff=0.2)
        with self.voiceover(
            "So the algorithm is simple. <bookmark mark='a'/> Sort the vertices by their entry in the eigenvector. "
            "<bookmark mark='b'/> Take the first vertex, then the first two, then three, and compute the "
            "conductance of each prefix, updating the cut as each vertex crosses over. <bookmark mark='c'/> Keep "
            "the best. On our small graph the best prefix is the first six, the cut between the clusters. "
            "<bookmark mark='d'/> On chapter two's graph of a hundred and twenty vertices, the conductance curve "
            "dips to its minimum at sixty: <bookmark mark='e'/> exactly the planted split. One eigenvector, one "
            "sort; and Cheeger's inequality guarantees the answer is never far from the best "
            "possible, measured on the square-root scale."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(*[d_.animate.set_color(vcolor(v, float(np.abs(f).max()))) for d_, v in zip(g[1], f)],
                      FadeIn(nums), FadeIn(ncap))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(axy), FadeIn(axl))
            for k in range(1, n):
                S = np.zeros(n, bool)
                S[order[:k]] = True
                self.play(*[d_.animate.set_color(HEAD if S[i] else GREY_B) for i, d_ in enumerate(g[1])],
                          *[ln.animate.set_stroke(NO if S[a] != S[b] else GREY_C, width=4 if S[a] != S[b] else 1.5)
                            for ln, (a, b) in zip(g[0], edges)], FadeIn(pdots[k - 1]), run_time=0.45)
            vo.wait_until("c")
            S = np.zeros(n, bool)
            S[order[:kb]] = True
            self.play(*[d_.animate.set_color(YES if S[i] else GREY_B) for i, d_ in enumerate(g[1])],
                      *[ln.animate.set_stroke(NO if S[a] != S[b] else GREY_C, width=4 if S[a] != S[b] else 1.5)
                        for ln, (a, b) in zip(g[0], edges)], pdots[kb - 1].animate.set_color(YES).scale(1.6),
                      FadeIn(ill))
            vo.wait_until("d")
            self.play(Create(bx), FadeIn(bxt), FadeIn(byt), FadeIn(bxl), FadeIn(byl))
            self.play(Create(line), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(best, scale=0.5), FadeIn(bestl), FadeIn(truth))
        self.wait(0.4)
        self.clear_scene()

    def check(self):
        rows = load("cheeger")["rows"]
        head = label(r"Checked on random graphs", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 0.8, 0.2], y_range=[0, 1.3, 0.25], x_length=6.6, y_length=4.6, tips=False,
                        axis_config={"stroke_color": GREY_C}).move_to(LEFT * 2.6 + DOWN * 0.3)
        xt = VGroup(*[label(rf"{v:.1f}", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in (0, 0.2, 0.4, 0.6, 0.8)])
        yt = VGroup(*[label(rf"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in (0, 0.5, 1.0)])
        xl = label(r"$\lambda_2$ of $N$", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"conductance", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        up = ax.plot(lambda x: min(math.sqrt(2 * x), 1.3), x_range=[0.0005, 0.8, 0.005], color=NO, stroke_width=3)
        lo = ax.plot(lambda x: x / 2, x_range=[0, 0.8], color=DATA, stroke_width=3)
        upl = label(r"$\sqrt{2\lambda_2}$", font_size=20, color=NO).next_to(ax.c2p(0.5, 1.0), UP, buff=0.12)
        lol = label(r"$\lambda_2 / 2$", font_size=20, color=DATA).next_to(ax.c2p(0.8, 0.4), DOWN, buff=0.12)
        exact = VGroup(*[Dot(ax.c2p(r["lambda2"], r["phi"]), radius=0.055, color=HEAD) for r in rows])
        sw = VGroup(*[Circle(radius=0.085, color=LAM, stroke_width=2).move_to(ax.c2p(r["lambda2"], r["sweep"]))
                      for r in rows])
        nrow = len(rows)
        same = sum(abs(r["phi"] - r["sweep"]) < 1e-12 for r in rows)
        ok = all(r["lower"] <= r["phi"] + 1e-12 and r["sweep"] <= r["upper"] + 1e-12 for r in rows)
        side = VGroup(
            wrapped_label(rf"{nrow} connected random graphs on 12 vertices; \ $\phi(G)$ by brute force over all "
                          r"2,047 cuts \ (yellow)", 4.4, font_size=19, color=HEAD),
            wrapped_label(r"the sweep cut \ (purple rings)", 4.4, font_size=19, color=LAM),
            wrapped_label((rf"all {nrow} inside the bounds; \ " if ok else "") +
                          rf"the sweep found the best cut in {same} of {nrow}", 4.4, font_size=19, color=YES),
            wrapped_label(r"both sides are tight: \ the hypercube has $\phi = \lambda_2/2$ exactly; \ on a long "
                          r"cycle $\phi$ is of order $\sqrt{\lambda_2}$", 4.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 4.45 + DOWN * 0.2)
        with self.voiceover(
            "Finally, a check. <bookmark mark='a'/> Fifty-three connected random graphs on twelve vertices, small "
            "enough to find the best cut by trying all two thousand and forty-seven of them. "
            "<bookmark mark='b'/> Every graph lands between the two curves. <bookmark mark='c'/> The sweep cut "
            "also stays under the upper curve, as the proof promised, and finds the very best cut in "
            "thirty-two of the fifty-three. <bookmark mark='d'/> Neither side can be improved by more than a "
            "constant. The hypercube meets the lower bound exactly, and on a long cycle the conductance really is "
            "of the order of the square root of lambda two."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_, scale=0.5) for x_ in exact], lag_ratio=0.03), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(up), Create(lo), FadeIn(upl), FadeIn(lol))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in sw], lag_ratio=0.03), FadeIn(side[1]), run_time=2)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
