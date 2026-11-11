from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

# The chapter's circuit: six vertices, nine one-ohm resistors; current enters at s = 0 and leaves at t = 5.
POS = [(-2.0, 0.0), (-0.8, 1.0), (-0.8, -1.0), (0.8, 1.0), (0.8, -1.0), (2.0, 0.0)]
EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5), (2, 3)]
S, T = 0, 5


def laplacian_of(n, edges, w=None):
    L = np.zeros((n, n))
    for k, (a, b) in enumerate(edges):
        c = 1.0 if w is None else w[k]
        L[a, a] += c
        L[b, b] += c
        L[a, b] -= c
        L[b, a] -= c
    return L


def potentials(n, edges, s, t):
    """Unit current in at s and out at t through unit resistors: v = L^+ (e_s - e_t), shifted so v_t = 0."""
    b = np.zeros(n)
    b[s], b[t] = 1.0, -1.0
    v = np.linalg.pinv(laplacian_of(n, edges)) @ b
    return v - v[t]


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def resistor(p, q, color=GREY_B, sw=2.0, teeth=4, amp=0.08, frac=0.46):
    """A straight lead, a zig-zag resistor symbol in the middle of the segment, and a lead again."""
    p, q = np.array(p), np.array(q)
    d = q - p
    ln = float(np.linalg.norm(d))
    u = d / ln
    nrm = np.array([-u[1], u[0], 0.0])
    lead = (1 - frac) / 2 * ln
    pts = [p, p + u * lead]
    for k in range(1, 2 * teeth):
        pts.append(p + u * (lead + frac * ln * k / (2 * teeth)) + nrm * amp * (1 if k % 2 else -1))
    pts += [p + u * (ln - lead), q]
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)


def circuit(center, scale=1.0, r=0.11):
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in POS]
    wires = VGroup(*[resistor(pts[a], pts[b]) for a, b in EDGES])
    dots = VGroup(*[Dot(p, radius=r, color=WHITE) for p in pts])
    g = VGroup(wires, dots)
    g.pts = pts
    return g


def ladder(steps, whys, buff=0.26):
    """A derivation: each line with its grey reason under it, the pairs stacked flush left."""
    pairs = VGroup(*[VGroup(s_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for s_, w_ in zip(steps, whys)])
    return pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def heat(v, vmax):
    return interpolate_color(ManimColor(DATA), ManimColor(KERN), max(0.0, min(1.0, float(v) / vmax)))


def flow_arrows(pts, edges, f, color=YES, k=7.0, off=0.17, length=0.42):
    """One arrow per edge carrying current, beside the edge, pointing with the current, thickness by |f|."""
    out = VGroup()
    for (a, b), x in zip(edges, f):
        if abs(x) < 1e-6:
            out.add(VectorizedPoint(pts[a]))
            continue
        p, q = (pts[a], pts[b]) if x > 0 else (pts[b], pts[a])
        u = (q - p) / np.linalg.norm(q - p)
        nrm = np.array([-u[1], u[0], 0.0])
        mid = (p + q) / 2 + nrm * off
        out.add(Arrow(mid - u * length / 2, mid + u * length / 2, buff=0, color=color,
                      stroke_width=1.5 + k * abs(x), max_tip_length_to_length_ratio=0.45,
                      max_stroke_width_to_length_ratio=30))
    return out


class Electrical(VoiceoverScene):
    def construct(self):
        self.card()
        self.kirchhoff()
        self.solve()
        self.resistance()
        self.thomson()
        self.commute()
        self.measured()
        self.polya()

    def card(self):
        card = chapter_card(8, r"Graphs as electrical networks", r"What does a graph do when current flows through it?",
                            lit=(1847, 1989), extra=((1847, r"Kirchhoff: \ circuit laws"),
                                                     (1989, r"Chandra et al.: \ commute times")), part=PART)
        with self.voiceover("Chapter eight. Graphs as electrical networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ Ohm and Kirchhoff give L v = b
    def kirchhoff(self):
        head = label(r"Ohm and Kirchhoff give $Lx = b$", font_size=36).to_edge(UP, buff=0.3)
        g = circuit(LEFT * 3.7 + UP * 0.5, scale=1.2)
        names = VGroup(label(r"$s$", font_size=24, color=HEAD).next_to(g.pts[S], LEFT, buff=0.15),
                       label(r"$t$", font_size=24, color=HEAD).next_to(g.pts[T], RIGHT, buff=0.15),
                       label(r"$u$", font_size=24, color=GREY_A).next_to(g.pts[1], UP, buff=0.15))
        cap = wrapped_label(r"every edge a resistor; \ conductance $w_{uv}$ \ (here every resistor is one ohm, "
                            r"$w = 1$)", 5.6, font_size=19, color=GREY_A).next_to(g, DOWN, buff=0.45)
        cols = {r"x_u": KERN, r"b_u": DATA, r"x": KERN, r"b": DATA}
        steps = VGroup(
            cmath(r"i_{uv}", r"=", r"w_{uv}", r"(x_u - x_v)", font_size=32),
            cmath(r"\sum_{v \sim u}", r"i_{uv}", r"=", r"b_u", colors=cols, font_size=32),
            cmath(r"\sum_{v \sim u}", r"w_{uv}", r"(x_u - x_v)", r"=", r"b_u", colors=cols, font_size=32),
            cmath(r"d_u", r"x_u", r"-", r"\sum_{v} w_{uv} x_v", r"=", r"b_u", colors=cols, font_size=32),
            cmath(r"L", r"x", r"=", r"b", colors=cols, font_size=40),
        )
        whys = VGroup(
            label(r"Ohm: \ current is conductance times voltage drop", font_size=18, color=GREY_B),
            label(r"Kirchhoff: \ net current out of $u$ is what is injected there", font_size=18, color=GREY_B),
            label(r"substitute Ohm into Kirchhoff", font_size=18, color=GREY_B),
            label(r"$d_u = \sum_v w_{uv}$, \ the weighted degree", font_size=18, color=GREY_B),
            label(r"row $u$ of the Laplacian, \ for every $u$ at once", font_size=18, color=YES),
        )
        ladder(steps, whys).move_to(RIGHT * 3.0 + UP * 0.35)
        box = SurroundingRectangle(steps[4], color=HEAD, buff=0.05, stroke_width=2)
        with self.voiceover(
            "Part 3 built logic from switches driven by voltages; now circuits return as mathematics. Make "
            "every edge of a graph a resistor, and give each vertex a voltage. <bookmark mark='a'/> Ohm's law: "
            "the current along an edge is its conductance times the voltage drop across it. <bookmark mark='b'/> "
            "Kirchhoff's law: the current leaving a vertex, summed over its edges, equals the current injected "
            "there from outside. <bookmark mark='c'/> Put Ohm into Kirchhoff. <bookmark mark='d'/> Expand: the "
            "vertex's voltage times its weighted degree, minus its neighbours' voltages. <bookmark mark='e'/> "
            "That is one row of the Laplacian. All the rows together say L x equals b: voltages in, injected "
            "currents out. Gustav Kirchhoff wrote these equations down in 1847."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names), FadeIn(cap))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(Write(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]))
            self.play(Create(box))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ voltages and currents drawn
    def solve(self):
        head = label(r"Push one amp from $s$ to $t$", font_size=36).to_edge(UP, buff=0.3)
        v = potentials(6, EDGES, S, T)
        f = [v[a] - v[b] for a, b in EDGES]
        g = draw(POS, EDGES, center=LEFT * 2.9 + DOWN * 0.15, scale=1.45, r=0.14, ecolor=GREY_D, sw=2.5)
        vals = VGroup(*[label(rf"{v[i]:.2f}", font_size=20, color=WHITE).next_to(
            g.pts[i], UP if POS[i][1] > 0 else (DOWN if POS[i][1] < 0 else (LEFT if i == S else RIGHT)),
            buff=0.16) for i in range(6)])
        vals[S].next_to(g.pts[S], UP, buff=0.18)
        vals[T].next_to(g.pts[T], UP, buff=0.18)
        names = VGroup(label(r"$s$", font_size=24, color=HEAD).next_to(g.pts[S], DOWN, buff=0.18),
                       label(r"$t$", font_size=24, color=HEAD).next_to(g.pts[T], DOWN, buff=0.18))
        inj = VGroup(Arrow(g.pts[S] + LEFT * 1.0, g.pts[S] + LEFT * 0.18, buff=0, color=DATA, stroke_width=4),
                     Arrow(g.pts[T] + RIGHT * 0.18, g.pts[T] + RIGHT * 1.0, buff=0, color=DATA, stroke_width=4))
        inj_l = VGroup(label(r"$+1$", font_size=20, color=DATA).next_to(inj[0], DOWN, buff=0.08),
                       label(r"$-1$", font_size=20, color=DATA).next_to(inj[1], DOWN, buff=0.08))
        arrows = flow_arrows(g.pts, EDGES, f)
        right = VGroup(
            MathTex(r"b = e_s - e_t", font_size=32, color=DATA),
            label(r"$\sum_u b_u = 0$, \ so $Lx = b$ has a solution", font_size=21, color=GREY_A),
            MathTex(r"x = L^{+} b", font_size=32, color=KERN),
            label(r"$L^{+}$: \ the pseudo-inverse, \ on vectors with $\sum = 0$", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.0 + UP * 1.6)
        a1, a2, a3 = (f[0], f[2], f[3])
        kcl = wrapped_label(rf"at the ringed vertex: \ ${a1:.2f}$ in \ $= {a2:.2f} + {a3:.2f}$ out", 4.6, font_size=21,
                            color=YES).next_to(right, DOWN, buff=0.55).align_to(right, LEFT)
        ring_a = Circle(radius=0.3, color=YES, stroke_width=3).move_to(g.pts[1])
        ill = note(r"illustrative circuit; \ voltages and currents computed", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Now drive the circuit. <bookmark mark='a'/> Inject one amp at s and draw it out at t: b is plus one "
            "at s and minus one at t. Its entries sum to zero, which is exactly what a Laplacian system needs to "
            "be solvable. <bookmark mark='b'/> The voltages are L's pseudo-inverse applied to b, up to a "
            "constant, so set t to zero, and colour each vertex by its voltage. <bookmark mark='c'/> Current runs "
            "downhill along every edge, thick where the drop is large. <bookmark mark='d'/> And at every inner "
            "vertex what flows in flows out: forty-five hundredths in here, nine and thirty-six hundredths out."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names))
            vo.wait_until("a")
            self.play(GrowArrow(inj[0]), GrowArrow(inj[1]), FadeIn(inj_l), FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("b")
            self.play(FadeIn(right[2]), FadeIn(right[3]),
                      *[d.animate.set_color(heat(x, v[S])) for d, x in zip(g[1], v)], FadeIn(vals))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in arrows],
                                  lag_ratio=0.12), FadeIn(ill))
            vo.wait_until("d")
            self.play(Create(ring_a), FadeIn(kcl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ effective resistance
    def resistance(self):
        head = label(r"Effective resistance is a quadratic form", font_size=36).to_edge(UP, buff=0.3)
        v = potentials(6, EDGES, S, T)
        R = float(v[S] - v[T])
        lhs = r"R_{\mathrm{eff}}(s,t)"
        cols = {lhs: HEAD, r"b": DATA, r"L^{+}": KERN, r"b^{\mathsf T}": DATA}
        steps = VGroup(
            cmath(lhs, r"=", r"x_s - x_t", colors=cols, font_size=32),
            cmath(lhs, r"=", r"(e_s - e_t)^{\mathsf T}", r"x", colors=cols, font_size=32),
            cmath(lhs, r"=", r"b^{\mathsf T}", r"L^{+}", r"b", colors=cols, font_size=32),
            cmath(r"\sum_{(u,v)\in E} w_{uv}(x_u - x_v)^2", r"=", r"x^{\mathsf T} L x", colors=cols, font_size=30),
            cmath(r"=", r"b^{\mathsf T}", r"L^{+} L L^{+}", r"b", r"=", lhs, colors=cols, font_size=30),
        )
        whys = VGroup(
            label(r"the voltage needed to push one amp", font_size=18, color=GREY_B),
            label(r"read off $x_s - x_t$ with the vector $e_s - e_t$", font_size=18, color=GREY_B),
            label(r"which is $b$ itself, \ and $x = L^{+} b$", font_size=18, color=GREY_B),
            label(r"chapter one's energy, \ at the voltages", font_size=18, color=GREY_B),
            label(r"so it is also the energy the current dissipates", font_size=18, color=YES),
        )
        ladder(steps, whys, buff=0.24).to_edge(LEFT, buff=0.5).shift(DOWN * 0.15)

        def two(series):
            a, b = np.array([-0.8, 0, 0]), np.array([0.8, 0, 0])
            if series:
                m = np.array([0.0, 0, 0])
                return VGroup(resistor(a, m, frac=0.6), resistor(m, b, frac=0.6), Dot(a, radius=0.07),
                              Dot(m, radius=0.07), Dot(b, radius=0.07))
            up, dn = np.array([0, 0.3, 0]), np.array([0, -0.3, 0])
            return VGroup(resistor(a + up, b + up, frac=0.5), resistor(a + dn, b + dn, frac=0.5),
                          Line(a + up, a + dn, color=GREY_B, stroke_width=2),
                          Line(b + up, b + dn, color=GREY_B, stroke_width=2), Dot(a, radius=0.07),
                          Dot(b, radius=0.07))
        bs = np.array([1.0, 0, -1])
        Rs = float(bs @ np.linalg.pinv(laplacian_of(3, [(0, 1), (1, 2)])) @ bs)
        bp = np.array([1.0, -1])
        Rp = float(bp @ np.linalg.pinv(laplacian_of(2, [(0, 1), (0, 1)])) @ bp)
        checks = VGroup(
            VGroup(two(True), MathTex(rf"R = 1 + 1 = {Rs:.0f}", font_size=28, color=HEAD)).arrange(DOWN, buff=0.2),
            VGroup(two(False), MathTex(rf"R = \tfrac{{1}}{{1 + 1}} = {Rp:.1f}", font_size=28,
                                       color=HEAD)).arrange(DOWN, buff=0.2),
            VGroup(circuit(ORIGIN, scale=0.5, r=0.06),
                   MathTex(rf"R_{{\mathrm{{eff}}}}(s,t) = {R:.2f}", font_size=28, color=HEAD)).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45).move_to(RIGHT * 4.9 + DOWN * 0.15)
        caps = VGroup(label(r"series", font_size=18, color=GREY_A).next_to(checks[0][0], LEFT, buff=0.3),
                      label(r"parallel", font_size=18, color=GREY_A).next_to(checks[1][0], LEFT, buff=0.3),
                      label(r"our circuit", font_size=18, color=GREY_A).next_to(checks[2][0], LEFT, buff=0.3))
        ill = note(r"computed from $b^{\mathsf T} L^{+} b$", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "How hard is it to push current from s to t? <bookmark mark='a'/> The effective resistance is the "
            "voltage it takes to push one amp. <bookmark mark='b'/> Read that voltage difference with the vector "
            "e s minus e t, <bookmark mark='c'/> which is b itself, while the voltages are L plus b: a quadratic "
            "form in the Laplacian's pseudo-inverse. <bookmark mark='d'/> It is also the energy the current "
            "burns: chapter one's sum of squared differences, at the voltages, <bookmark mark='e'/> collapses to "
            "the same form. <bookmark mark='f'/> Check it on circuits you know: two one-ohm resistors give two in "
            "series and a half in parallel. Our nine-resistor circuit comes to about one point three six."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Write(steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(VGroup(c, k)) for c, k in zip(checks, caps)], lag_ratio=0.5),
                      FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()


    # ------------------------------------------------------------------ Thomson's principle
    def thomson(self):
        head = label(r"Thomson's principle: \ current is lazy", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\mathcal E(f)": HEAD, r"\mathcal E(i)": YES, r"\mathcal E(c)": GREY_A}
        steps = VGroup(
            cmath(r"\mathcal E(f)", r"=", r"\sum_e r_e f_e^2", colors=cols, font_size=30),
            cmath(r"\mathcal E(f)", r"=", r"\mathcal E(i)", r"+", r"\mathcal E(c)", r"+",
                  r"2\sum_e r_e\, i_e c_e", colors=cols, font_size=30),
            cmath(r"\sum_e r_e\, i_e c_e", r"=", r"\sum_{(u,v)} (x_u - x_v)\, c_{uv}", r"=",
                  r"\sum_u x_u \cdot 0", colors=cols, font_size=30),
            cmath(r"\mathcal E(f)", r"\ \ge\ ", r"\mathcal E(i)", r"=", r"R_{\mathrm{eff}}(s,t)", colors=cols,
                  font_size=34),
        )
        steps[3][4].set_color(HEAD)
        whys = VGroup(
            label(r"the energy of any unit flow $f$ from $s$ to $t$", font_size=18, color=GREY_B),
            label(r"write $f = i + c$: \ $i$ electrical, \ $c$ a circulation", font_size=18, color=GREY_B),
            label(r"Ohm, \ then regroup by vertex: \ $c$ is balanced everywhere", font_size=18, color=GREY_B),
            label(r"the electrical flow has the least energy", font_size=18, color=YES),
        )
        ladder(steps, whys, buff=0.4).to_edge(LEFT, buff=0.5).shift(UP * 0.3)
        v = potentials(6, EDGES, S, T)
        elec = [v[a] - v[b] for a, b in EDGES]
        half = [0.5, 0.5, 0, 0.5, 0.5, 0, 0.5, 0.5, 0]
        one = [1, 0, 0, 1, 0, 0, 1, 0, 0]
        flows = [(elec, YES, r"electrical"), (half, LAM, r"half on each of two paths"),
                 (one, NO, r"all on one path")]
        centre = RIGHT * 3.9 + UP * 0.75
        g = draw(POS, EDGES, center=centre, scale=1.1, r=0.11, ecolor=GREY_D, sw=2.5)
        names = VGroup(label(r"$s$", font_size=22, color=HEAD).next_to(g.pts[S], LEFT, buff=0.15),
                       label(r"$t$", font_size=22, color=HEAD).next_to(g.pts[T], RIGHT, buff=0.15))

        def readout(k):
            fl, c, nm = flows[k]
            en = sum(x * x for x in fl)
            return VGroup(label(nm, font_size=21, color=c),
                          MathTex(rf"\mathcal E = {en:.2f}", font_size=32, color=c)).arrange(DOWN, buff=0.15).next_to(
                g, DOWN, buff=0.45)
        arr = [flow_arrows(g.pts, EDGES, fl, color=c, off=0.15, length=0.36) for fl, c, _ in flows]
        reads = [readout(k) for k in range(3)]
        mono_ = wrapped_label(r"\textbf{Rayleigh monotonicity}: \ lowering any resistance never raises "
                              r"$R_{\mathrm{eff}}$ \ (the old current is still allowed, \ and now cheaper)", 5.4,
                              font_size=19, color=HEAD).next_to(reads[0], DOWN, buff=0.4)
        with self.voiceover(
            "Which of all the ways to send one unit from s to t does current choose? <bookmark mark='a'/> Give "
            "each unit flow an energy: resistance times flow squared, summed over the edges. <bookmark mark='b'/> "
            "Write any flow as the electrical flow plus a circulation, balanced at every vertex. "
            "<bookmark mark='c'/> The cross term vanishes: by Ohm's law it is voltage drops times the "
            "circulation, and regrouped by vertex, each voltage multiplies a net flow of zero. "
            "<bookmark mark='d'/> So the electrical flow has the least energy, and that energy is the effective "
            "resistance: Thomson's principle. <bookmark mark='e'/> Splitting the unit over two paths costs one "
            "and a half; one path, three. <bookmark mark='f'/> A corollary: lowering any resistance cannot raise "
            "the effective resistance."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(names))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0].copy(), steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(whys[3]))
            self.play(LaggedStart(*[FadeIn(a) for a in arr[0]], lag_ratio=0.05), FadeIn(reads[0]))
            vo.wait_until("e")
            self.play(ReplacementTransform(arr[0], arr[1]), ReplacementTransform(reads[0], reads[1]))
            self.wait(1.2)
            self.play(ReplacementTransform(arr[1], arr[2]), ReplacementTransform(reads[1], reads[2]))
            vo.wait_until("f")
            self.play(FadeIn(mono_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ commute time = 2 m R_eff, derived
    def commute(self):
        head = label(r"Commute time $= 2m\,R_{\mathrm{eff}}$", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            cmath(r"\varphi_u", r"=", r"1 + \frac{1}{d_u} \sum_{v \sim u} \varphi_v", r",\quad \varphi_t = 0",
                  font_size=30),
            cmath(r"d_u \varphi_u - \sum_{v \sim u} \varphi_v", r"=", r"d_u", r"\quad (u \ne t)", font_size=30),
            cmath(r"L\varphi", r"=", r"d - 2m\, e_t", r",\qquad", r"L\psi", r"=", r"d - 2m\, e_s", font_size=30),
            cmath(r"L(\varphi - \psi)", r"=", r"2m\,(e_s - e_t)", font_size=30),
            cmath(r"H(s,t) + H(t,s)", r"=", r"2m\,R_{\mathrm{eff}}(s,t)", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        steps[0][0].set_color(KERN)
        steps[2][0].set_color(KERN)
        steps[2][4].set_color(DATA)
        steps[4][2].set_color(HEAD)
        whys = VGroup(
            label(r"$\varphi_u = H(u, t)$: \ expected steps from $u$ to reach $t$", font_size=18, color=GREY_B),
            label(r"multiply by $d_u$", font_size=18, color=GREY_B),
            label(r"row $t$ makes the sum zero; \ $\psi_u = H(u, s)$ likewise", font_size=18, color=GREY_B),
            label(r"so $\varphi - \psi$ is $2m$ times the voltages $x$, \ plus a constant", font_size=18,
                  color=GREY_B),
            label(r"read at $s$ minus $t$: \ $\varphi_s + \psi_t$", font_size=18, color=YES),
        )
        steps.to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
        if steps.width > 6.9:
            steps.scale_to_fit_width(6.9).to_edge(LEFT, buff=0.6)
        for w_, s_ in zip(whys, steps):
            w_.move_to(s_).align_to(RIGHT * 0.95, LEFT)
        defn = label(r"commute time: \ $C(s,t) = H(s,t) + H(t,s)$, \ the expected steps from $s$ to $t$ and back",
                     font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.3)
        cite = note(r"Chandra, \ Raghavan, \ Ruzzo, \ Smolensky and Tiwari \ (1989); \ Doyle and Snell \ (1984)",
                    font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now let a random walker loose. Its commute time is the expected number of steps from s to t and "
            "back. <bookmark mark='a'/> Let phi of u be the expected time to reach t from u: one step, then the "
            "neighbours' average. <bookmark mark='b'/> Multiply by the degree, <bookmark mark='c'/> and it is a "
            "Laplacian system: the degrees injected, all of two m drawn out at t. Hitting times to s, called psi, "
            "satisfy the same. <bookmark mark='d'/> Subtract: the degrees cancel, and phi minus psi is two m "
            "times the voltages of one amp. <bookmark mark='e'/> Read at s and t: the commute time is two m times "
            "the effective resistance, as Chandra, Raghavan, Ruzzo, Smolensky and Tiwari proved in 1989. Doyle "
            "and Snell's book of 1984 had already joined walks and circuits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defn))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]), FadeIn(cite))
            self.play(Circumscribe(steps[4], color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ measured on a grid
    def measured(self):
        c = load("commute")
        head = label(r"Measured: \ corner to corner on a $5 \times 5$ grid", font_size=36).to_edge(UP, buff=0.3)
        w = h = 5
        centre = LEFT * 3.4 + DOWN * 0.15
        pos = [(x - 2, y - 2) for x in range(w) for y in range(h)]
        edges = []
        for x in range(w):
            for y in range(h):
                i = x * h + y
                if x + 1 < w:
                    edges.append((i, i + h))
                if y + 1 < h:
                    edges.append((i, i + 1))
        g = draw(pos, edges, center=centre, scale=0.95, r=0.07, color=GREY_B, ecolor=GREY_D, sw=2)
        s_, t_ = 0, 24
        sd = Dot(g.pts[s_], radius=0.12, color=HEAD)
        td = Dot(g.pts[t_], radius=0.12, color=HEAD)
        names = VGroup(label(r"$s$", font_size=22, color=HEAD).next_to(g.pts[s_], DL, buff=0.08),
                       label(r"$t$", font_size=22, color=HEAD).next_to(g.pts[t_], UR, buff=0.08))
        nb = {i: [] for i in range(w * h)}
        for a, b in edges:
            nb[a].append(b)
            nb[b].append(a)
        rng = random.Random(3)
        walk, u = [s_], s_
        while len(walk) < 70:
            u = rng.choice(nb[u])
            walk.append(u)
        walker = Dot(g.pts[s_], radius=0.11, color=YES)
        trail = VMobject(stroke_color=YES, stroke_width=2, stroke_opacity=0.5)
        trail.set_points_as_corners([g.pts[s_], g.pts[s_]])
        rows = VGroup(
            MathTex(rf"m = {c['m']}", font_size=32),
            MathTex(rf"R_{{\mathrm{{eff}}}}(s,t) = {c['R_eff']:.3f}", font_size=32, color=HEAD),
            MathTex(rf"2m\,R_{{\mathrm{{eff}}}} = {c['predicted']:.1f}", font_size=32, color=HEAD),
            MathTex(rf"\text{{measured: }} {c['measured']:.1f}", font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.4 + UP * 0.6)
        sub = label(r"mean of 2{,}000 simulated round trips", font_size=19, color=GREY_A).next_to(
            rows[3], DOWN, buff=0.15).align_to(rows, LEFT)
        gap = (c['measured'] - c['predicted']) / c['predicted'] * 100
        agree = wrapped_label(rf"within {gap:.1f}\% \ (each round trip varies a lot, \ so the mean has sampling "
                              r"error)", 5.0, font_size=19, color=GREY_A).next_to(sub, DOWN, buff=0.35).align_to(
            rows, LEFT)
        ill = note(r"the walk drawn is one illustrative sample", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Test it. <bookmark mark='a'/> A five by five grid has forty edges. Corner to corner its effective "
            "resistance is about two point one four, so the formula predicts a commute time of about a hundred "
            "and seventy-one steps. <bookmark mark='b'/> Here is one walker, wandering. <bookmark mark='c'/> Two "
            "thousand simulated round trips averaged a hundred and seventy-four, within sampling error. A "
            "question about wandering has become one Laplacian system."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(sd), FadeIn(td), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.add(trail, walker)
            for k in range(1, len(walk)):
                p = g.pts[walk[k]]
                new = trail.copy()
                new.add_points_as_corners([p])
                self.play(walker.animate.move_to(p), Transform(trail, new), run_time=0.09, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(sub), FadeIn(agree), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Pólya's walks, by circuits
    def polya(self):
        head = label(r"Will a walker come home? \ Ask a circuit", font_size=36).to_edge(UP, buff=0.3)
        K = 4
        sp = 0.42
        centre = LEFT * 3.7 + DOWN * 0.2
        pts = {(x, y): centre + sp * np.array([x, y, 0.0]) for x in range(-K, K + 1) for y in range(-K, K + 1)}
        lines = VGroup()
        for (x, y), p in pts.items():
            if x < K:
                lines.add(Line(p, pts[(x + 1, y)], color=GREY_D, stroke_width=1.5))
            if y < K:
                lines.add(Line(p, pts[(x, y + 1)], color=GREY_D, stroke_width=1.5))
        dots = VGroup(*[Dot(p, radius=0.035, color=GREY_B) for p in pts.values()])
        origin = Dot(pts[(0, 0)], radius=0.09, color=HEAD)
        shell_cols = [KERN, LAM, DATA, YES]
        shorted, crossing, counts = VGroup(), VGroup(), VGroup()
        for k in range(K):
            col = shell_cols[k]
            shorted.add(Square(side_length=2 * k * sp, color=col, stroke_width=3.5).move_to(centre) if k
                        else VectorizedPoint(centre))
            cr = VGroup()
            for (x, y), p in pts.items():
                if max(abs(x), abs(y)) != k:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + dx, y + dy)
                    if q in pts and max(abs(q[0]), abs(q[1])) == k + 1:
                        cr.add(Line(p, pts[q], color=col, stroke_width=3))
            crossing.add(cr)
            counts.add(label(rf"{len(cr)}", font_size=20, color=col))
        counts.arrange(RIGHT, buff=0.5).next_to(VGroup(lines, dots), DOWN, buff=0.3)
        cnt_l = label(r"edges from shell $k$ to shell $k + 1$: \ $8k + 4$", font_size=18, color=GREY_A).next_to(
            counts, DOWN, buff=0.12)
        steps = VGroup(
            wrapped_label(r"P\'olya \ (1921): \ a walk on $\mathbb Z^2$ returns home for sure; \ on $\mathbb Z^3$ "
                          r"it may not", 6.4, font_size=20, color=WHITE),
            wrapped_label(r"it returns for sure \ $\iff$ \ the resistance from the origin to infinity is infinite",
                          6.4, font_size=20, color=GREY_A),
            wrapped_label(r"short each square shell into one node: \ by Rayleigh, \ $R$ only drops; \ what is left "
                          r"is bundles of $8k + 4$ parallel edges, \ in series", 6.4, font_size=18, color=GREY_B),
            cmath(r"R_{\mathrm{eff}}(0, \infty)", r"\ \ge\ ", r"\sum_{k \ge 0} \frac{1}{8k + 4}", r"=", r"\infty",
                  font_size=32),
            cmath(r"\mathbb Z^3", r":\ \ ", r"\mathcal E", r"\approx", r"\sum_k k^2 \cdot \Big(\frac{1}{k^2}\Big)^2",
                  r"<", r"\infty", font_size=30),
            wrapped_label(r"a unit flow spread evenly over shells of about $k^2$ edges: \ by Thomson, \ $R$ is "
                          r"finite", 6.4, font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.3 + DOWN * 0.1)
        steps[3][0].set_color(HEAD)
        steps[3][4].set_color(NO)
        steps[4][6].set_color(YES)
        with self.voiceover(
            "One classic from Doyle and Snell's book. <bookmark mark='a'/> George Pólya proved in 1921 that a "
            "random walk on the square lattice surely returns home; on the cubic lattice it may not. "
            "<bookmark mark='b'/> In circuit terms: it surely returns exactly when the resistance from the origin "
            "to infinity is infinite. <bookmark mark='c'/> In the plane, short each square shell into one node; "
            "by Rayleigh, that only lowers the resistance. <bookmark mark='d'/> What is left is bundles of four, "
            "twelve, twenty edges in parallel, joined in series. <bookmark mark='e'/> One over eight k plus four "
            "sums to infinity, so the walker comes home. <bookmark mark='f'/> In three dimensions a current "
            "spread over shells of about k squared edges has finite energy, so by Thomson the resistance is "
            "finite."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(dots), FadeIn(origin))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s) for s in shorted], lag_ratio=0.3), FadeIn(steps[2]))
            vo.wait_until("d")
            for k in range(K):
                self.play(Create(crossing[k]), FadeIn(counts[k]), run_time=0.6)
            self.play(FadeIn(cnt_l))
            vo.wait_until("e")
            self.play(Write(steps[3]))
            vo.wait_until("f")
            self.play(FadeIn(steps[4]), FadeIn(steps[5]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, NO)
