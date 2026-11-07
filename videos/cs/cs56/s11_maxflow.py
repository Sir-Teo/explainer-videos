from __future__ import annotations

from collections import deque

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart

# The chapter's network: s = 0, t = 7, twelve undirected edges with integer capacities.
POS = [(-3.0, 0.0), (-1.5, 1.2), (-1.5, -1.2), (0.0, 1.2), (0.0, -1.2), (1.5, 1.2), (1.5, -1.2), (3.0, 0.0)]
EDGES = [(0, 1), (0, 2), (1, 3), (2, 4), (1, 4), (3, 5), (4, 6), (3, 6), (5, 7), (6, 7), (1, 2), (5, 6)]
CAP = [2, 3, 4, 1, 3, 4, 2, 4, 4, 1, 1, 3]
S, T = 0, 7
EPS = 0.5
ROUNDS = 30


def laplacian_of(n, edges, w):
    L = np.zeros((n, n))
    for k, (a, b) in enumerate(edges):
        L[a, a] += w[k]
        L[b, b] += w[k]
        L[a, b] -= w[k]
        L[b, a] -= w[k]
    return L


def electrical(n, edges, cond, s, t, F):
    """The electrical flow of value F from s to t with the given conductances: one Laplacian solve."""
    b = np.zeros(n)
    b[s], b[t] = F, -F
    x = np.linalg.pinv(laplacian_of(n, edges, cond)) @ b
    return np.array([cond[k] * (x[a] - x[c]) for k, (a, c) in enumerate(edges)])


def max_flow(n, edges, cap, s, t):
    """Edmonds-Karp on the undirected network (each edge usable both ways): the value of a maximum flow."""
    C = np.zeros((n, n))
    for (a, b), c in zip(edges, cap):
        C[a, b] += c
        C[b, a] += c
    F = 0.0
    while True:
        par = [-1] * n
        par[s] = s
        q = deque([s])
        while q:
            u = q.popleft()
            for v in range(n):
                if par[v] < 0 and C[u, v] > 1e-12:
                    par[v] = u
                    q.append(v)
        if par[t] < 0:
            return F
        v, c = t, float("inf")
        while v != s:
            c = min(c, C[par[v], v])
            v = par[v]
        v = t
        while v != s:
            C[par[v], v] -= c
            C[v, par[v]] += c
            v = par[v]
        F += c


def mwu(n, edges, cap, s, t, F, eps=EPS, rounds=ROUNDS):
    """Multiplicative weights over electrical flows, after Christiano, Kelner, Madry, Spielman and Teng (2011),
    simplified: resistances r_e = w_e / u_e^2; raise each weight by its congestion; average the flows."""
    u = np.array(cap, float)
    w = np.ones(len(edges))
    acc = np.zeros(len(edges))
    hist = []
    for k in range(1, rounds + 1):
        f = electrical(n, edges, u ** 2 / w, s, t, F)
        c = np.abs(f) / u
        avg_ok = float((w * c ** 2).sum() / w.sum())
        acc += f
        avg = acc / k
        hist.append({"f": f, "cong": c, "weighted": avg_ok, "avg": avg.copy(),
                     "avg_cong": float((np.abs(avg) / u).max())})
        w = w * (1 + eps * c)
    return hist


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def cong_color(c):
    if c > 1.005:
        return ManimColor(NO)
    return interpolate_color(ManimColor(GREY_C), ManimColor(YES), max(0.0, min(1.0, float(c))))


def styled(lines, cong):
    """Edges recoloured by congestion |f_e| / u_e: grey to green up to capacity, red beyond it."""
    out = VGroup()
    for ln, c in zip(lines, cong):
        out.add(ln.copy().set_stroke(color=cong_color(c), width=2 + 5 * min(float(c), 1.6)))
    return out


def cap_labels(pts, edges, cap, size=17):
    out = VGroup()
    for (a, b), c in zip(edges, cap):
        mid = (pts[a] + pts[b]) / 2
        t = label(rf"{c}", font_size=size, color=GREY_A)
        bg = Circle(radius=0.15, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(mid)
        out.add(VGroup(bg, t.move_to(mid)))
    return out


def ladder(steps, whys, buff=0.26):
    """A derivation: each line with its grey reason under it, the pairs stacked flush left."""
    pairs = VGroup(*[VGroup(s_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for s_, w_ in zip(steps, whys)])
    return pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def chart_axes(x_range, y_range, x_length, y_length, xticks, yticks, fx=lambda v: f"{v:g}", fy=lambda v: f"{v:g}",
               x_label=None, y_label=None, font=16):
    """Axes meeting at the bottom-left corner whatever the ranges, with tick labels; a VGroup with .ax."""
    ax = CornerAxes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"stroke_color": GREY_C})
    g = VGroup(ax)
    g.add(VGroup(*[label(fx(x), font_size=font, color=GREY_B).next_to(ax.c2p(x, y_range[0]), DOWN, buff=0.1)
                   for x in xticks]))
    g.add(VGroup(*[label(fy(y), font_size=font, color=GREY_B).next_to(ax.c2p(x_range[0], y), LEFT, buff=0.1)
                   for y in yticks]))
    if x_label:
        g.add(label(x_label, font_size=17, color=GREY_A).next_to(g, DOWN, buff=0.12))
    if y_label:
        g.add(label(y_label, font_size=17, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT))
    g.ax = ax
    return g


def bfs_tree(n, edges, root):
    nb = {i: [] for i in range(n)}
    for k, (a, b) in enumerate(edges):
        nb[a].append((b, k))
        nb[b].append((a, k))
    par, used = {root: None}, set()
    q = deque([root])
    while q:
        u = q.popleft()
        for v, k in nb[u]:
            if v not in par:
                par[v] = (u, k)
                used.add(k)
                q.append(v)
    return par, used


class Maxflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.lemma()
        self.rounds()
        self.barrier()
        self.cycles()
        self.history()

    def card(self):
        card = chapter_card(10, r"From electrical flows to max-flow", r"Can current find the maximum flow?",
                            lit=(2011, 2022), extra=((2011, r"Christiano et al.: \ electrical flows"),
                                                     (2022, r"Chen et al.: \ almost-linear max-flow")), part=PART)
        with self.voiceover("Chapter ten. From electrical flows to maximum flow."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ current ignores capacities
    def problem(self):
        head = label(r"Current ignores capacities", font_size=36).to_edge(UP, buff=0.3)
        n = len(POS)
        F = max_flow(n, EDGES, CAP, S, T)
        u = np.array(CAP, float)
        f0 = electrical(n, EDGES, u ** 2, S, T, F)
        c0 = np.abs(f0) / u
        g = draw(POS, EDGES, center=LEFT * 2.6 + DOWN * 0.1, scale=1.1, r=0.11, ecolor=GREY_C, sw=2.5)
        names = VGroup(label(r"$s$", font_size=24, color=HEAD).next_to(g.pts[S], LEFT, buff=0.15),
                       label(r"$t$", font_size=24, color=HEAD).next_to(g.pts[T], RIGHT, buff=0.15))
        caps = cap_labels(g.pts, EDGES, CAP)
        worst = int(np.argmax(c0))
        right = VGroup(
            label(r"\textbf{maximum flow}: \ send as much as possible from $s$ to $t$", font_size=20),
            MathTex(r"|f_e| \le u_e \quad \text{(capacity)}", font_size=28, color=GREY_A),
            label(rf"Edmonds--Karp \ (Part 18): \ the maximum is {F:.0f}", font_size=20, color=YES),
            label(r"electrical flow of value 4, \ $r_e = 1/u_e^2$:", font_size=20, color=DATA),
            label(r"one Laplacian solve, \ nearly linear time", font_size=20, color=GREY_A),
            label(rf"but edge $s$--$a$ carries {abs(f0[worst]):.2f} \ $>$ \ {CAP[worst]}", font_size=20, color=NO),
            label(rf"congestion $|f_e| / u_e$ up to {c0.max():.2f}", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.85 + DOWN * 0.1)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        a_l = label(r"$a$", font_size=22, color=GREY_A).next_to(g.pts[1], UP, buff=0.15)
        legend = label(r"edge colour: \ congestion, \ green up to capacity, \ red beyond", font_size=18,
                       color=GREY_A).next_to(g, DOWN, buff=0.45)
        ill = note(r"illustrative network; \ flows computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Part 18 met maximum flow: push as much as possible from s to t without exceeding any edge's capacity, "
            "and it solved the problem with augmenting paths. <bookmark mark='a'/> Here is a network with "
            "capacities from one to four; its maximum flow is four. <bookmark mark='b'/> Electrical flow is "
            "tempting, because one Laplacian solve, in nearly linear time, routes the whole value at once, spread "
            "over every path. Give each edge resistance one over its capacity squared, so wide edges conduct well. "
            "<bookmark mark='c'/> But current knows nothing of capacities. The edge from s to a has capacity two "
            "and is asked to carry almost three: congestion one point four one."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names), FadeIn(a_l), FadeIn(right[0]),
                      FadeIn(right[1]))
            vo.wait_until("a")
            self.play(FadeIn(caps), FadeIn(right[2]))
            vo.wait_until("b")
            self.play(FadeIn(right[3]), FadeIn(right[4]), Transform(g[0], styled(g[0], c0)), FadeIn(legend))
            vo.wait_until("c")
            self.play(Indicate(g[0][worst], color=NO, scale_factor=1.05), FadeIn(right[5]), FadeIn(right[6]),
                      FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the key lemma, from Thomson
    def lemma(self):
        head = label(r"On average, \ electrical flow is not congested", font_size=36).to_edge(UP, buff=0.3)
        n = len(POS)
        F = max_flow(n, EDGES, CAP, S, T)
        hist = mwu(n, EDGES, CAP, S, T, F)
        cols = {r"\sum_e w_e": YES}
        steps = VGroup(
            cmath(r"r_e", r"=", r"\frac{w_e}{u_e^2}", font_size=30),
            cmath(r"\mathcal E(f)", r"\le", r"\mathcal E(f^*)", r"=", r"\sum_e \frac{w_e}{u_e^2}\, (f^*_e)^2",
                  r"\le", r"\sum_e w_e", colors=cols, font_size=30),
            cmath(r"\sum_e w_e \Big(\frac{f_e}{u_e}\Big)^2", r"\le", r"\sum_e w_e", colors=cols, font_size=30),
            cmath(r"\frac{\sum_e w_e\, \mathrm{cong}_e^2}{\sum_e w_e}", r"\le", r"1", font_size=32),
        )
        steps[3][2].set_color(YES)
        whys = VGroup(
            label(r"weights $w_e$, \ start at 1; \ wide edges conduct well", font_size=18, color=GREY_B),
            label(r"Thomson: \ $f$ electrical beats any flow $f^*$ of value $F$; \ take one within capacity",
                  font_size=18, color=GREY_B),
            label(r"the left side is $\mathcal E(f)$, \ written out", font_size=18, color=GREY_B),
            label(r"a weighted average of squared congestion is at most one", font_size=18, color=YES),
        )
        ladder(steps, whys, buff=0.3).to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
        c1 = hist[0]["cong"]
        ax = chart_axes([0, len(EDGES) + 1, 1], [0, 1.5, 0.5], 4.8, 2.6, xticks=[], yticks=[0, 0.5, 1.0, 1.5],
                        x_label=r"the twelve edges")
        ax.move_to(RIGHT * 4.1 + UP * 0.45)
        A = ax.ax
        bars = VGroup()
        for k, c in enumerate(c1, start=1):
            h = A.c2p(0, c)[1] - A.c2p(0, 0)[1]
            bars.add(Rectangle(width=0.26, height=max(h, 0.01), stroke_width=0, fill_color=cong_color(c),
                               fill_opacity=0.9).move_to(A.c2p(k, 0) + UP * h / 2))
        one = DashedLine(A.c2p(0, 1), A.c2p(len(EDGES) + 1, 1), color=GREY_B, stroke_width=1.5)
        cap_t = label(r"congestion of the first electrical flow", font_size=18, color=GREY_A).next_to(
            ax, UP, buff=0.15)
        read = VGroup(
            label(rf"largest: \ {c1.max():.2f}", font_size=20, color=NO),
            label(rf"weighted mean of squares: \ {hist[0]['weighted']:.2f} \ $\le 1$", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.35).align_to(ax, LEFT)
        with self.voiceover(
            "Current breaks capacities, but not by much on average, and the reason is Thomson's principle. "
            "<bookmark mark='a'/> Give each edge a weight, starting at one, and resistance weight over capacity "
            "squared. <bookmark mark='b'/> Suppose some flow of value F fits the capacities. The electrical "
            "flow's energy is no more than that flow's, which is at most the sum of the weights. "
            "<bookmark mark='c'/> Write the electrical energy out edge by edge, <bookmark mark='d'/> and it says: "
            "the weighted average of squared congestion is at most one. A few edges can overflow, but only a few. "
            "<bookmark mark='e'/> Our first electrical flow overflows one edge by forty-one percent, while the "
            "weighted mean of squares is far below one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(ax), FadeIn(cap_t), Create(one),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08))
            self.play(FadeIn(read))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ multiplicative weights, round by round
    def rounds(self):
        head = label(r"Multiplicative weights over electrical flows", font_size=36).to_edge(UP, buff=0.3)
        n = len(POS)
        F = max_flow(n, EDGES, CAP, S, T)
        hist = mwu(n, EDGES, CAP, S, T, F)
        g = draw(POS, EDGES, center=LEFT * 3.6 + UP * 1.0, scale=0.85, r=0.09, ecolor=GREY_C, sw=2.5)
        names = VGroup(label(r"$s$", font_size=22, color=HEAD).next_to(g.pts[S], LEFT, buff=0.12),
                       label(r"$t$", font_size=22, color=HEAD).next_to(g.pts[T], RIGHT, buff=0.12))
        code = VGroup(
            label(r"repeat $T$ times:", font_size=20, color=WHITE),
            label(r"$f \leftarrow$ electrical flow of value $F$, \ $r_e = w_e / u_e^2$", font_size=20, color=DATA),
            label(rf"$w_e \leftarrow w_e \,(1 + \varepsilon\, \mathrm{{cong}}_e)$ \ \ ($\varepsilon = {EPS}$)",
                  font_size=20, color=HEAD),
            label(r"return the average of the $f$'s", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        code[1:3].shift(RIGHT * 0.4)
        frame = SurroundingRectangle(code, color=GREY_D, buff=0.22, corner_radius=0.08, stroke_width=1.5)
        prog = VGroup(frame, code).next_to(g, DOWN, buff=0.45)
        ys = [h["avg_cong"] for h in hist]
        ax = chart_axes([0, ROUNDS, 5], [1.0, 1.5, 0.1], 5.2, 2.9, xticks=[0, 10, 20, 30],
                        yticks=[1.0, 1.1, 1.2, 1.3, 1.4, 1.5], fy=lambda v: f"{v:.1f}", x_label=r"round",
                        y_label=r"largest congestion of the averaged flow")
        ax.move_to(RIGHT * 3.3 + UP * 0.45)
        A = ax.ax
        pts = [A.c2p(k + 1, y) for k, y in enumerate(ys)]
        dot = Dot(pts[0], radius=0.06, color=HEAD)
        curve = VMobject(stroke_color=HEAD, stroke_width=3)
        curve.set_points_as_corners([pts[0], pts[0]])
        rd = label(rf"round 1: \ {ys[0]:.3f}", font_size=22, color=HEAD).next_to(ax, DOWN, buff=0.6)
        final = hist[-1]["avg"]
        scaled = F / ys[-1]
        end = wrapped_label(rf"divide by {ys[-1]:.3f}: \ a flow within every capacity, \ of value "
                            rf"{scaled:.2f}, \ {scaled / F * 100:.1f}\% of the maximum", 5.6, font_size=20,
                            color=YES).next_to(rd, DOWN, buff=0.25)
        cite = note(r"Christiano, \ Kelner, \ M{\fontencoding{T1}\selectfont\k{a}}dry, \ Spielman and Teng \ (2011): \ "
                    r"$(1 - \varepsilon)$-approximate, \ undirected, \ $\tilde O(m n^{1/3} \varepsilon^{-11/3})$",
                    font_size=18).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "So use the overflow to adjust the weights. <bookmark mark='a'/> Compute an electrical flow; raise the "
            "weight, and so the resistance, of every edge in proportion to its congestion; and repeat, averaging "
            "the flows. Edges that overflow become expensive, and the next current avoids them. "
            "<bookmark mark='b'/> This is the multiplicative weights method of Part 23, with an electrical flow "
            "as the expert's move. <bookmark mark='c'/> Round by round, the worst congestion of the average falls, "
            "from one point four one towards one. <bookmark mark='d'/> After thirty rounds, shrink the averaged flow "
            "until it fits: it carries ninety-seven percent of the maximum. <bookmark mark='e'/> In 2011 Paul "
            "Christiano, Jonathan Kelner, Aleksander Mądry, Daniel Spielman and Shang-Hua Teng refined this loop "
            "into the fastest algorithm then known for approximate maximum flow in undirected graphs."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(prog))
            vo.wait_until("b")
            self.play(FadeIn(ax), Transform(g[0], styled(g[0], np.abs(hist[0]["avg"]) / np.array(CAP))),
                      FadeIn(dot), FadeIn(rd))
            vo.wait_until("c")
            self.add(curve)
            u = np.array(CAP, float)
            for k in range(1, ROUNDS):
                new = curve.copy()
                new.add_points_as_corners([pts[k]])
                self.play(Transform(curve, new), dot.animate.move_to(pts[k]),
                          Transform(g[0], styled(g[0], np.abs(hist[k]["avg"]) / u)),
                          Transform(rd, label(rf"round {k + 1}: \ {ys[k]:.3f}", font_size=22,
                                              color=HEAD).move_to(rd)), run_time=0.3)
            vo.wait_until("d")
            self.play(FadeIn(end), Transform(g[0], styled(g[0], np.abs(final) / u / ys[-1])))
            vo.wait_until("e")
            self.play(FadeIn(cite))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ interior points: Newton steps are electrical
    def barrier(self):
        head = label(r"Interior points: \ every Newton step is an electrical flow", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"r_e": KERN}
        steps = VGroup(
            cmath(r"\max\ F", r"\quad", r"B^{\mathsf T} f = F\,(e_s - e_t),\ \ |f_e| < u_e", font_size=28),
            cmath(r"\Phi(f)", r"=", r"-\sum_e \big[\log(u_e - f_e) + \log(u_e + f_e)\big]", font_size=28),
            cmath(r"\min_{\delta}\ \ g^{\mathsf T}\delta + \tfrac12 \sum_e", r"r_e", r"\delta_e^2", r"\quad",
                  r"B^{\mathsf T}\delta = \text{given}", colors=cols, font_size=28),
            cmath(r"r_e", r"=", r"\frac{1}{(u_e - f_e)^2} + \frac{1}{(u_e + f_e)^2}", colors=cols, font_size=28),
            cmath(r"\text{one solve with}", r"\ \ ", r"B^{\mathsf T} R^{-1} B", r",\ \ ",
                  r"\text{a Laplacian}", font_size=28),
        )
        steps[4][2].set_color(YES)
        whys = VGroup(
            label(r"maximum flow as a linear program \ (Part 23)", font_size=18, color=GREY_B),
            label(r"the log barrier keeps every edge strictly inside its capacity", font_size=18, color=GREY_B),
            label(r"Newton's step: \ a quadratic model of objective plus barrier", font_size=18, color=GREY_B),
            label(r"the barrier's curvature: \ the resistance of edge $e$", font_size=18, color=GREY_B),
            label(r"conductances $1/r_e$: \ about $\sqrt{m}$ such steps in all", font_size=18, color=YES),
        )
        ladder(steps, whys, buff=0.2).to_edge(LEFT, buff=0.45).shift(DOWN * 0.2)
        ax = chart_axes([-1, 1, 0.5], [0, 50, 10], 4.2, 2.3, xticks=[-1, 0, 1], yticks=[0, 25, 50],
                        fx=lambda v: {-1: r"$-u$", 0: r"$0$", 1: r"$u$"}[int(v)],
                        x_label=r"flow $f_e$ on one edge \ ($u = 1$)")
        ax.move_to(RIGHT * 4.3 + UP * 1.35)
        A = ax.ax
        curve = A.plot(lambda x: 1 / (1 - x) ** 2 + 1 / (1 + x) ** 2, x_range=[-0.855, 0.855, 0.01],
                       color=KERN, stroke_width=3)
        rlab = label(r"$r_e$", font_size=22, color=KERN).next_to(A.c2p(0.86, 48), LEFT, buff=0.1)
        tr = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(A.c2p(tr.get_value(), 1 / (1 - tr.get_value()) ** 2 +
                                              1 / (1 + tr.get_value()) ** 2), radius=0.07, color=HEAD))
        n = len(POS)
        F = max_flow(n, EDGES, CAP, S, T)
        hist = mwu(n, EDGES, CAP, S, T, F)
        u = np.array(CAP, float)
        fs = 0.95 * hist[-1]["avg"] / hist[-1]["avg_cong"]
        r = 1 / (u - np.abs(fs)) ** 2 + 1 / (u + np.abs(fs)) ** 2
        lr = np.log(r * u ** 2)
        lr = (lr - lr.min()) / (lr.max() - lr.min())
        g = draw(POS, EDGES, center=RIGHT * 4.25 + DOWN * 1.9, scale=0.68, r=0.07, ecolor=GREY_D, sw=2)
        hot = VGroup(*[ln.copy().set_stroke(color=interpolate_color(ManimColor(GREY_C), ManimColor(KERN), float(v)),
                                            width=1.5 + 5 * float(v)) for ln, v in zip(g[0], lr)])
        g_cap = label(r"near the optimum, \ nearly full edges have huge resistance", font_size=18,
                      color=GREY_A).next_to(g, UP, buff=0.12)
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "The other road from circuits to flows runs through interior-point methods, met in Part 23 with "
            "Karmarkar. <bookmark mark='a'/> Maximum flow is a linear program. <bookmark mark='b'/> Replace the "
            "hard capacity limits by a logarithmic barrier that rises to infinity at either limit. "
            "<bookmark mark='c'/> Each Newton step minimizes a quadratic model, a linear term plus a weighted sum "
            "of squares, under flow conservation. <bookmark mark='d'/> That is the energy of an electrical flow, "
            "each edge's resistance the curvature of its barrier, which explodes as the edge fills. "
            "<bookmark mark='e'/> So each step is one Laplacian solve, and current steers around full edges by "
            "itself. About the square root of m steps gave exact flows in about m to the three halves; the next "
            "decade went into cutting the steps."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]), FadeIn(ax), Create(curve), FadeIn(rlab))
            self.add(dot)
            self.play(tr.animate.set_value(0.82), run_time=1.2)
            self.play(tr.animate.set_value(-0.82), run_time=1.6)
            self.play(tr.animate.set_value(0.0), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(whys[3]), Create(g[0]), FadeIn(g[1]), FadeIn(g_cap))
            self.play(Transform(g[0], hot), FadeIn(ill))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]), FadeIn(whys[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ 2022: steps along cycles
    def cycles(self):
        head = label(r"2022: \ steps along cycles", font_size=36).to_edge(UP, buff=0.3)
        n = len(POS)
        g = draw(POS, EDGES, center=LEFT * 3.4 + UP * 0.55, scale=1.0, r=0.1, ecolor=GREY_D, sw=2)
        names = VGroup(label(r"$s$", font_size=22, color=HEAD).next_to(g.pts[S], LEFT, buff=0.12),
                       label(r"$t$", font_size=22, color=HEAD).next_to(g.pts[T], RIGHT, buff=0.12))
        par, used = bfs_tree(n, EDGES, S)
        tree = VGroup(*[g[0][k].copy().set_stroke(color=YES, width=4) for k in sorted(used)])
        off = next(k for k in range(len(EDGES)) if k not in used and S not in EDGES[k] and T not in EDGES[k])
        a, b = EDGES[off]

        def up(v):
            path = [v]
            while par[path[-1]] is not None:
                path.append(par[path[-1]][0])
            return path
        pa, pb = up(a), up(b)
        common = next(v for v in pa if v in pb)
        cyc = pa[:pa.index(common) + 1] + pb[:pb.index(common)][::-1]
        cyc_pts = [g.pts[v] for v in cyc] + [g.pts[cyc[0]]]
        loop = VMobject(stroke_color=HEAD, stroke_width=6).set_points_as_corners(cyc_pts)
        offe = g[0][off].copy().set_stroke(color=HEAD, width=5)
        runner = Dot(cyc_pts[0], radius=0.09, color=HEAD)
        tcap = label(r"a spanning tree \ (green); \ one more edge closes one cycle", font_size=19,
                     color=GREY_A).next_to(g, DOWN, buff=0.4)
        steps = VGroup(
            cmath(r"\ell_2\text{: }", r"\min_\delta\ g^{\mathsf T}\delta + \tfrac12 \|R^{1/2}\delta\|_2^2",
                  font_size=28),
            cmath(r"\ell_1\text{: }", r"\min_{\Delta\ \text{circulation}}\ \frac{g^{\mathsf T}\Delta}"
                  r"{\|\mathrm{diag}(\ell)\,\Delta\|_1}", font_size=28),
        )
        steps[1][1].set_color(HEAD)
        whys = VGroup(
            label(r"the electrical step: \ spreads over every path", font_size=18, color=GREY_B),
            label(r"the \textbf{min-ratio cycle}: \ the best is one single cycle", font_size=18, color=HEAD),
        )
        lad = ladder(steps, whys, buff=0.3).move_to(RIGHT * 3.4 + UP * 1.45)
        if lad.get_right()[0] > 6.85:
            lad.shift(LEFT * (lad.get_right()[0] - 6.85))
        body = VGroup(
            wrapped_label(r"Chen, \ Kyng, \ Liu, \ Peng, \ Probst Gutenberg and Sachdeva \ (2022): \ an "
                          r"interior-point method of $m^{1 + o(1)}$ steps, \ each an approximate min-ratio cycle",
                          6.2, font_size=19, color=WHITE),
            wrapped_label(r"cycles found from low-stretch trees \ (chapter 9), \ kept up to date by dynamic data "
                          r"structures as lengths change: \ $m^{o(1)}$ amortized per step", 6.2, font_size=19,
                          color=GREY_A),
            wrapped_label(r"exact maximum flow, \ and min-cost flow, \ on directed graphs with integer capacities: "
                          r"\ time $m^{1 + o(1)}$", 6.2, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(lad, DOWN, buff=0.45).align_to(lad, LEFT)
        rgt = VGroup(lad, body)
        if rgt.get_right()[0] > 6.85:
            rgt.shift(LEFT * (rgt.get_right()[0] - 6.85))
        with self.voiceover(
            "In 2022 Li Chen, Rasmus Kyng, Yang Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant "
            "Sachdeva took the last step. <bookmark mark='a'/> An electrical step spreads a small change over "
            "every path, and needs a fresh solve each time. <bookmark mark='b'/> They replaced it by its cousin "
            "in another norm: the circulation with the best ratio of gain to length, and the best one is a single "
            "cycle. <bookmark mark='c'/> Lay down a spanning tree: every edge outside it closes exactly one "
            "cycle, <bookmark mark='d'/> and when the tree has low stretch, one of those cycles is within a "
            "modest factor of the best. <bookmark mark='e'/> Their method takes m to the one plus little o of one "
            "steps, and dynamic data structures keep the trees current, at m to the little o of one per step. "
            "<bookmark mark='f'/> The result: exact maximum flow and minimum-cost flow on directed graphs, in "
            "almost linear time."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Create(tree), FadeIn(tcap))
            self.play(Create(offe))
            vo.wait_until("d")
            self.play(Create(loop), FadeIn(runner))
            self.play(MoveAlongPath(runner, loop), run_time=2.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(body[0]), FadeIn(body[1]))
            vo.wait_until("f")
            self.play(FadeIn(body[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the exponent comes down
    def history(self):
        head = label(r"Maximum flow: \ the exponent comes down", font_size=36).to_edge(UP, buff=0.3)
        vals = [3.0, 1.5, 4 / 3, 1.0]
        names = [r"1972", r"1998", r"2011", r"2022"]
        cols = [NO, KERN, DATA, YES]
        ch = bar_chart(vals, names, cols, height=3.6, bar_w=1.1, gap=1.3, vmax=3.0,
                       fmt_=lambda v: {3.0: "3", 1.5: "1.5", 1.0: "1 + o(1)"}.get(round(v, 3), "4/3"),
                       font_size=24)
        ch.move_to(LEFT * 2.3 + UP * 0.05)
        who = VGroup(*[wrapped_label(t, 2.2, font_size=18, color=c) for t, c in zip(
            (r"Edmonds--Karp: \ $O(nm^2)$", r"Goldberg--Rao: \ $\tilde O(m^{3/2})$",
             r"Christiano et al.: \ approximate, \ undirected", r"Chen et al.: \ exact, \ directed"), cols)])
        for w_, b_ in zip(who, ch.names):
            w_.next_to(b_, DOWN, buff=0.15)
        cap = label(r"exponent of $m$, \ sparse graphs \ ($m \approx n$), \ logarithms ignored", font_size=19,
                    color=GREY_A).next_to(ch, UP, buff=0.35)
        side = VGroup(
            wrapped_label(r"Kirchhoff's equations \ $\to$ \ Laplacian solvers \ $\to$ \ electrical flows \ $\to$ "
                          r"\ interior points \ $\to$ \ cycles on low-stretch trees", 3.6, font_size=20, color=HEAD),
            wrapped_label(r"what remains open: \ simple, \ practical almost-linear flow \ (chapter 11)", 3.6,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 4.9 + DOWN * 0.1)
        with self.voiceover(
            "Step back and look at the exponent. <bookmark mark='a'/> In 1972 Edmonds and Karp's augmenting paths "
            "took n times m squared steps, cubic on sparse graphs. <bookmark mark='b'/> In 1998 Andrew Goldberg and "
            "Satish Rao reached about m to the three halves. <bookmark mark='c'/> Electrical flows broke that "
            "barrier in 2011 for approximate flows in undirected graphs, <bookmark mark='d'/> and in 2022 the "
            "exponent reached one, for exact flows in directed graphs. <bookmark mark='e'/> The road ran from "
            "Kirchhoff's equations, through fast Laplacian solvers, electrical flows and interior points, to cycles "
            "on low-stretch trees. The algorithm is still far too intricate to run in practice, which the frontier "
            "chapter lists among the open problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ch[0]))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]), FadeIn(who[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO, KERN)
