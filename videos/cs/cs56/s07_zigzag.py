from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono

ZZ = r"\mathbin{\text{\textcircled{\scriptsize z}}}"


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


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


def ring(n, radius, start=math.pi / 2):
    return [(radius * math.cos(start - 2 * math.pi * k / n), radius * math.sin(start - 2 * math.pi * k / n))
            for k in range(n)]


def clouds(center, R=2.15, rc=0.42):
    """G = K5 (degree D = 4) with every vertex replaced by a cloud of D ports joined in a 4-cycle (H, degree 2).
    Ports face their partner clouds.  Returns cloud centres, port positions, the rotation map and port order."""
    c = np.array(center, dtype=float)
    cen = [c + R * np.array([math.cos(math.pi / 2 + 2 * math.pi * v / 5),
                             math.sin(math.pi / 2 + 2 * math.pi * v / 5), 0.0]) for v in range(5)]
    partners, ports = {}, {}
    for v in range(5):
        mean = math.atan2(*(c - cen[v])[1::-1])
        others = [w for w in range(5) if w != v]

        def rel(w):
            a = math.atan2(*(cen[w] - cen[v])[1::-1]) - mean
            return (a + math.pi) % (2 * math.pi) - math.pi
        others.sort(key=rel)
        partners[v] = others
        for a, off in enumerate((-1.75, -0.6, 0.6, 1.75)):
            ports[(v, a)] = cen[v] + rc * np.array([math.cos(mean + off), math.sin(mean + off), 0.0])
    rot = {(v, a): (w, partners[w].index(v)) for v in range(5) for a, w in enumerate(partners[v])}
    return cen, ports, rot


class Zigzag(VoiceoverScene):
    def construct(self):
        self.card()
        self.explicit()
        self.product()
        self.bound()
        self.measured()
        self.recursion()
        self.reingold()

    def card(self):
        card = chapter_card(6, r"Explicit expanders: \ the zig-zag product",
                            r"How do you build an expander you can describe in a few lines?",
                            lit=(1973, 2005), extra=((1973, r"Margulis"),
                                                     (2000, r"Reingold, \ Vadhan and Wigderson"),
                                                     (2005, r"Reingold: \ SL = L")), part=PART)
        with self.voiceover("Chapter six. Explicit expanders, and the zig-zag product."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ what explicit means
    def explicit(self):
        head = label(r"What \emph{explicit} means", font_size=36).to_edge(UP, buff=0.3)
        box = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.12, stroke_color=KERN, stroke_width=2,
                               fill_color=BG, fill_opacity=1).move_to(LEFT * 3.6 + UP * 0.6)
        fn = mono("neighbour(v, i)", size=22, color=KERN).move_to(box)
        vin = VGroup(label(r"$v$:", font_size=22, color=DATA),
                     mono("0110 1011 ... 0101", size=20, color=DATA)).arrange(RIGHT, buff=0.15)
        vin.next_to(box, UP, buff=0.6)
        iin = label(r"$i \in \{1, \dots, D\}$", font_size=22, color=LAM).next_to(box, LEFT, buff=0.35)
        out = label(r"$w$, \ the $i$-th neighbour", font_size=22, color=YES).next_to(box, DOWN, buff=0.6)
        a1 = Arrow(vin.get_bottom(), box.get_top(), buff=0.08, color=GREY_B, stroke_width=2)
        a2 = Arrow(box.get_bottom(), out.get_top(), buff=0.08, color=GREY_B, stroke_width=2)
        bits = wrapped_label(r"$N = 2^{100}$ vertices, \ each named by 100 bits: \ the graph is never written "
                             r"down, \ only this function, \ which must run in time polynomial in $\log N$", 5.6,
                             font_size=19, color=GREY_A).next_to(out, DOWN, buff=0.4).set_x(-3.6)
        # the Margulis-style torus
        m = 7
        sp = 0.46
        origin = RIGHT * 3.7 + DOWN * 0.55

        def at(x, y):
            return origin + sp * np.array([x - (m - 1) / 2, y - (m - 1) / 2, 0.0])
        grid = VGroup(*[Dot(at(x, y), radius=0.05, color=GREY_B) for x in range(m) for y in range(m)])
        x0, y0 = 2, 1
        src = Dot(at(x0, y0), radius=0.1, color=HEAD)
        targets = [((x0 + y0) % m, y0), ((x0 - y0) % m, y0), (x0, (y0 + x0) % m), (x0, (y0 - x0) % m)]
        arrows = VGroup(*[CurvedArrow(at(x0, y0), at(*t), angle=-0.6, color=YES, stroke_width=2.5, tip_length=0.15)
                          for t in targets])
        tdots = VGroup(*[Dot(at(*t), radius=0.08, color=YES) for t in targets])
        maps = MathTex(r"(x, y) \mapsto (x \pm y,\ y),\ \ (x,\ y \pm x),\ \dots \pmod m", font_size=26,
                       color=YES).next_to(grid, UP, buff=0.35)
        tor = note(r"illustrative: \ shear maps on a $7 \times 7$ torus", font_size=16).next_to(grid, DOWN,
                                                                                               buff=0.25)
        hist = VGroup(
            label(r"Margulis \ (1973): \ pairs mod $m$, \ a few linear maps", font_size=19, color=GREY_A),
            label(r"Gabber and Galil \ (1981): \ an explicit bound on the gap", font_size=19, color=GREY_A),
            label(r"Lubotzky, \ Phillips and Sarnak \ (1988): \ Ramanujan, \ by number theory", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tor, DOWN, buff=0.3)
        if hist.get_right()[0] > 6.85:
            hist.shift(LEFT * (hist.get_right()[0] - 6.85))
        with self.voiceover(
            "Chapter five ended on a problem. <bookmark mark='a'/> Explicit means a short program that, given a "
            "vertex as a string of bits and an edge label, returns the neighbour in time polynomial in the string's "
            "length. <bookmark mark='b'/> The first family came from Grigory Margulis in 1973: the vertices are pairs"
            " of numbers modulo m, and the neighbours come from a few fixed linear maps. <bookmark mark='c'/> His "
            "proof gave no explicit constant; Ofer Gabber and Zvi Galil supplied one in 1981, and the Ramanujan "
            "graphs of Lubotzky, Phillips and Sarnak rest on deep number theory. In 2000 Omer Reingold, Salil Vadhan "
            "and Avi Wigderson found a construction with a proof a page long."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(box), FadeIn(fn), FadeIn(vin), FadeIn(iin), GrowArrow(a1))
            self.play(GrowArrow(a2), FadeIn(out), FadeIn(bits))
            vo.wait_until("b")
            self.play(FadeIn(grid), FadeIn(src), FadeIn(maps), FadeIn(tor))
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), FadeIn(tdots))
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the product, drawn
    def product(self):
        head = label(r"A step, \ a cloud move, \ a step", font_size=36).to_edge(UP, buff=0.3)
        center = LEFT * 3.35 + DOWN * 0.3
        cen, ports, rot = clouds(center)
        rings = VGroup(*[Circle(radius=0.66, color=GREY_D, stroke_width=1.5).move_to(c) for c in cen])
        big = VGroup()
        seen = set()
        for (v, a), (w, b) in rot.items():
            if (w, b) in seen:
                continue
            seen.add((v, a))
            big.add(Line(ports[(v, a)], ports[(w, b)], color=GREY_C, stroke_width=1.6))
        small = VGroup(*[Line(ports[(v, a)], ports[(v, (a + 1) % 4)], color=GREY_B, stroke_width=2)
                         for v in range(5) for a in range(4)])
        pdots = VGroup(*[Dot(ports[k], radius=0.075, color=WHITE) for k in sorted(ports)])
        gl = label(r"$G$: \ 5 vertices, \ degree $D = 4$", font_size=19, color=GREY_A)
        hl = label(r"$H$: \ a 4-cycle, \ degree $d = 2$, \ in every cloud", font_size=19, color=GREY_A)
        VGroup(gl, hl).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.3)
        v0, a0 = 0, 1
        a1 = (a0 + 1) % 4
        w1, b1 = rot[(v0, a1)]
        b2 = (b1 + 1) % 4
        walker = Dot(ports[(v0, a0)], radius=0.13, color=HEAD)
        zig = Line(ports[(v0, a0)], ports[(v0, a1)], color=HEAD, stroke_width=5)
        hop = Line(ports[(v0, a1)], ports[(w1, b1)], color=KERN, stroke_width=5)
        zag = Line(ports[(w1, b1)], ports[(w1, b2)], color=HEAD, stroke_width=5)
        arcs = VGroup()
        for s1 in (1, -1):
            aa = (a0 + s1) % 4
            w, b = rot[(v0, aa)]
            for s2 in (1, -1):
                arcs.add(ArcBetweenPoints(ports[(v0, a0)], ports[(w, (b + s2) % 4)], angle=-0.5, color=YES,
                                          stroke_width=3))
        first = next(i for i, ar in enumerate(arcs) if np.allclose(ar.get_end(), ports[(w1, b2)]))
        z = load("zigzag")
        side = VGroup(
            label(r"a vertex: \ a cloud $v$ and a port $a$", font_size=20, color=WHITE),
            label(r"zig: \ a step of $H$ inside the cloud", font_size=20, color=HEAD),
            label(r"the big step: \ $G$'s edge at that port", font_size=20, color=KERN),
            label(r"zag: \ a step of $H$ in the new cloud", font_size=20, color=HEAD),
            label(rf"$d \times d = {2 * 2}$ edges per vertex; \ $5 \cdot 4 = 20$ vertices", font_size=20,
                  color=YES),
            wrapped_label(rf"ours: \ $G$ random, \ degree {z['D']}, \ {z['N']} vertices; \ $H$ random, \ degree "
                          rf"{z['d']}, \ {z['D']} vertices; \ $G {ZZ} H$: \ {z['vertices']} vertices, \ degree "
                          rf"{z['degree']}, \ regular", 5.2, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.1)
        with self.voiceover(
            "<bookmark mark='a'/> Take a big graph G, here five vertices of degree four, and a small graph H with one"
            " vertex per edge at a vertex of G: a four-cycle. <bookmark mark='b'/> Replace every vertex of G by a "
            "cloud, a copy of H whose points are the ports where G's edges attach. A vertex of the product is a cloud"
            " and a port. <bookmark mark='c'/> An edge is three moves. Zig: a step of H inside the cloud. <bookmark "
            "mark='d'/> The big step: leave along G's edge at that port,. <bookmark mark='e'/> Zag: one more step of "
            "H, in the new cloud. <bookmark mark='f'/> Two choices for the zig, two for the zag: degree four, "
            "whatever G's degree. <bookmark mark='g'/> Ours is larger: G of degree eight on sixty vertices, H of "
            "degree three on eight, four hundred and eighty vertices of degree nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gl), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(rings), Create(big))
            vo.wait_until("b")
            self.play(Create(small), FadeIn(pdots), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(walker), FadeIn(side[1]))
            self.play(Create(zig), walker.animate.move_to(ports[(v0, a1)]))
            vo.wait_until("d")
            self.play(Create(hop), walker.animate.move_to(ports[(w1, b1)]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(Create(zag), walker.animate.move_to(ports[(w1, b2)]), FadeIn(side[3]))
            self.play(Create(arcs[first]))
            vo.wait_until("f")
            self.play(FadeOut(zig), FadeOut(hop), FadeOut(zag),
                      *[Create(ar) for i, ar in enumerate(arcs) if i != first], FadeIn(side[4]))
            vo.wait_until("g")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the eigenvalue bound
    def bound(self):
        head = label(r"Why the gap survives", font_size=36).to_edge(UP, buff=0.3)
        fs = 34
        lh = r"(1-\lambda_H)"
        steps = VGroup(
            cmath(r"Z", r"=", r"\tilde B\, \tilde A\, \tilde B", font_size=fs),
            cmath(r"B", r"=", lh + r"\, J", r"+", r"\lambda_H\, E", font_size=fs),
            cmath(r"Z", r"=", lh + r"^2\, \tilde J \tilde A \tilde J", r"+", r"\bigl(1 - " + lh + r"^2\bigr)\, F",
                  font_size=fs),
            cmath(r"\tilde J \tilde A \tilde J", r"=", r"G\text{'s walk, on cloud averages}", font_size=fs),
            cmath(r"\lambda_Z", r"\le", lh + r"^2\, \lambda_G", r"+", r"1 - " + lh + r"^2", font_size=fs),
            cmath(r"1 - \lambda_Z", r"\ge", lh + r"^2", r"(1 - \lambda_G)", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
        steps[5].set_color(YES)
        ww = 6.85 - (max(s.get_right()[0] for s in steps) + 0.4)
        whys = VGroup(
            wrapped_label(r"$\tilde B$: \ a step of $H$ in every cloud; \ $\tilde A$: \ "
                          r"the big step, \ a permutation", ww, font_size=20, color=GREY_B),
            wrapped_label(r"$J$: \ jump to a uniform port; \ $\|E\| \le 1$, \ "
                          r"since $H$ is $J$ up to $\lambda_H$", ww, font_size=20, color=GREY_B),
            wrapped_label(r"expand: \ one term has $J$ twice; \ "
                          r"the other three have norm $\le 1$, \ so $\|F\| \le 1$", ww, font_size=20, color=GREY_B),
            wrapped_label(r"average, \ big step, \ average: \ "
                          r"at most $\lambda_G$ on vectors $\perp \mathbf{1}$", ww, font_size=20, color=GREY_B),
            wrapped_label(r"so, \ on vectors $\perp \mathbf{1}$ \ "
                          r"(all eigenvalues normalized by the degree)", ww, font_size=20, color=GREY_B),
            wrapped_label(r"the gap shrinks by a fixed factor, \ and never closes", ww, font_size=20, color=YES),
        )
        right = max(s.get_right()[0] for s in steps) + 0.4
        for w, s in zip(whys, steps):
            w.next_to([right, s.get_y(), 0], RIGHT, buff=0)
            if w.get_right()[0] > 6.85:
                w.width = 6.85 - right
                w.next_to([right, s.get_y(), 0], RIGHT, buff=0)
        cite = note(r"after Vadhan's \emph{Pseudorandomness}; \ Reingold, \ Vadhan and Wigderson \ (2000) prove "
                    r"sharper bounds", font_size=17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Write one step as three matrices: a step of H in every cloud, the big step, which "
            "only permutes ports, and another step of H. <bookmark mark='b'/> H is an expander, so its step is nearly"
            " a jump to a uniform port: one minus lambda H of that jump, plus lambda H of a matrix of norm at most "
            "one. <bookmark mark='c'/> Multiply out. One term uses the uniform jump on both sides; the other three "
            "together are no bigger than their weight. <bookmark mark='d'/> That one term is G's own walk: average "
            "over a cloud, take G's edge from a random port, average again. Orthogonal to the uniform vector, it "
            "shrinks by lambda G. <bookmark mark='e'/> So lambda of the product is at most a mixture of lambda G and "
            "one. <bookmark mark='f'/> Rearranged: the product's gap is at least G's gap times one minus lambda H, "
            "squared: shrunk by a fixed factor, never closed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[0].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3], shift=DOWN * 0.1), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4], shift=DOWN * 0.1), FadeIn(whys[4]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(steps[4].copy(), steps[5]), FadeIn(whys[5]), FadeIn(cite))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ measured against the bounds
    def measured(self):
        z = load("zigzag")
        lg, lh, lz = z["lambda_G"], z["lambda_H"], z["lambda_Z"]
        gap_bound = 1 - (1 - lh) ** 2 * (1 - lg)
        head = label(rf"Our product: \ {z['vertices']} vertices, \ degree {z['degree']}", font_size=36).to_edge(
            UP, buff=0.3)
        items = [
            (r"$\lambda_G$ \ (degree 8)", lg, DATA),
            (r"$\lambda_H$ \ (degree 3)", lh, LAM),
            (rf"$\lambda_{{G {ZZ} H}}$, \ measured", lz, YES),
            (r"sharper bound \ (RVW)", z["bound"], HEAD),
            (r"gap bound, \ just proved", gap_bound, KERN),
            (r"$\lambda_G + \lambda_H + \lambda_H^2$", z["simple_bound"], NO),
        ]
        x0, unit, top = -2.7, 3.6, 2.2
        rows = VGroup()
        for k, (name, v, col) in enumerate(items):
            y = top - 0.72 * k
            nm = label(name, font_size=21, color=col)
            nm.next_to([x0 - 0.25, y, 0], LEFT, buff=0)
            bar = Rectangle(width=max(v * unit, 0.02), height=0.42, stroke_width=0, fill_color=col,
                            fill_opacity=0.85)
            bar.next_to([x0, y, 0], RIGHT, buff=0)
            val = label(rf"{v:.3f}", font_size=19, color=BLACK).move_to(bar.get_right() + LEFT * 0.38)
            rows.add(VGroup(nm, bar, val))
        one = DashedLine([x0 + unit, top + 0.45, 0], [x0 + unit, top - 0.72 * 5 - 0.4, 0], color=GREY_B,
                         stroke_width=2)
        onel = label(r"$\lambda = 1$: \ no expansion", font_size=18, color=GREY_B).next_to(one, UP, buff=0.1)
        tight = MathTex(r"f = \tfrac12 (1-\lambda_H^2)\,\lambda_G + \tfrac12 \sqrt{(1-\lambda_H^2)^2\,\lambda_G^2 "
                        r"+ 4\lambda_H^2}", font_size=26, color=HEAD)
        notes = VGroup(
            tight,
            wrapped_label(r"all $\lambda$s are second eigenvalues in size, \ divided by the degree; \ computed from "
                          r"the matrices we built", 12.0, font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the product we built. <bookmark mark='a'/> G, of degree eight, has normalized lambda about two "
            "thirds; H, of degree three on eight vertices, about three quarters. <bookmark mark='b'/> The product "
            "measures eighty-one hundredths: a real expander, of degree nine. <bookmark mark='c'/> The sharper bound "
            "of Reingold, Vadhan and Wigderson promises at most ninety-one hundredths; the gap bound we proved, "
            "ninety-eight. <bookmark mark='d'/> Their simplest bound, lambda G plus lambda H plus lambda H squared, "
            "is almost two here and says nothing. It is meant for an H with a small lambda."
        ) as vo:
            self.play(FadeIn(head), Create(one), FadeIn(onel))
            self.bring_to_back(one)
            vo.wait_until("a")
            self.play(*[FadeIn(r[0]) for r in rows[:2]], *[GrowFromEdge(r[1], LEFT) for r in rows[:2]],
                      *[FadeIn(r[2]) for r in rows[:2]])
            vo.wait_until("b")
            self.play(FadeIn(rows[2][0]), GrowFromEdge(rows[2][1], LEFT), FadeIn(rows[2][2]))
            vo.wait_until("c")
            self.play(*[FadeIn(r[0]) for r in rows[3:5]], *[GrowFromEdge(r[1], LEFT) for r in rows[3:5]],
                      *[FadeIn(r[2]) for r in rows[3:5]], FadeIn(notes))
            vo.wait_until("d")
            self.play(FadeIn(rows[5][0]), GrowFromEdge(rows[5][1], LEFT), FadeIn(rows[5][2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the recursion
    def recursion(self):
        head = label(r"Expanders from a seed", font_size=36).to_edge(UP, buff=0.3)
        fs = 32
        steps = VGroup(
            cmath(r"H", r":", r"(D^4,\ D,\ \tfrac15)", font_size=fs),
            cmath(r"G_{t+1}", r"=", r"G_t^2", ZZ, r"H", font_size=fs),
            cmath(r"G_t^2", r":", r"(D^{4t},\ D^4,\ \tfrac{4}{25})", font_size=fs),
            cmath(r"G_t^2", ZZ, r"H", r":", r"(D^{4t} \cdot D^4,\ D^2,\ \tfrac{4}{25} + \tfrac15 + \tfrac{1}{25})",
                  font_size=fs),
            cmath(r"G_{t+1}", r":", r"(D^{4(t+1)},\ D^2,\ \tfrac25)", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(LEFT, buff=0.6).shift(UP * 0.5)
        steps[4].set_color(YES)
        ww = 6.85 - (max(s.get_right()[0] for s in steps) + 0.4)
        whys = VGroup(
            wrapped_label(r"a fixed small expander: \ $D^4$ vertices, \ degree $D$; \ found once, \ "
                          r"by search", ww, font_size=20, color=GREY_B),
            wrapped_label(r"square to shrink $\lambda$; \ "
                          r"zig-zag to bring the degree back", ww, font_size=20, color=GREY_B),
            wrapped_label(r"if $G_t$ is $(D^{4t}, D^2, \tfrac25)$: \ "
                          r"squaring squares every eigenvalue", ww, font_size=20, color=GREY_B),
            wrapped_label(r"degree $D^4$ = the size of $H$; \ "
                          r"$\lambda \le \lambda_G + \lambda_H + \lambda_H^2$", ww, font_size=20, color=GREY_B),
            wrapped_label(r"the same degree and $\lambda$, \ "
                          r"on $D^4$ times as many vertices", ww, font_size=20, color=YES),
        )
        right = max(s.get_right()[0] for s in steps) + 0.4
        for w, s in zip(whys, steps):
            w.next_to([right, s.get_y(), 0], RIGHT, buff=0)
            if w.get_right()[0] > 6.85:
                w.width = 6.85 - right
                w.next_to([right, s.get_y(), 0], RIGHT, buff=0)
        blocks = VGroup()
        for t in range(1, 5):
            r = Rectangle(width=0.9 * t, height=0.42, stroke_color=YES, stroke_width=1.5, fill_color=YES,
                          fill_opacity=0.18)
            tx = MathTex(rf"G_{t}", font_size=24, color=YES).move_to(r)
            blocks.add(VGroup(r, tx))
        blocks.arrange(RIGHT, buff=0.25).next_to(steps, DOWN, buff=0.45).set_x(0)
        bl = label(r"each $D^4$ times bigger; \ degree $D^2$ and $\lambda \le \tfrac25$ throughout",
                   font_size=19, color=GREY_A).next_to(blocks, DOWN, buff=0.15)
        full = wrapped_label(r"fully explicit: \ tensor two half-size graphs before squaring, \ and a neighbour "
                             r"costs time polynomial in $\log N$ \ (Reingold, \ Vadhan and Wigderson)", 12.4,
                             font_size=20, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the construction. <bookmark mark='a'/> Fix one small expander H with D to the fourth vertices, "
            "degree D, and lambda at most a fifth. Being of constant size, it can be found by search. <bookmark "
            "mark='b'/> Then alternate: square, which squares lambda but multiplies the degree, and zig-zag with H, "
            "which brings the degree back. <bookmark mark='c'/> If G t has degree D squared and lambda at most two "
            "fifths, its square has degree D to the fourth, exactly the size of H, and lambda at most four twenty-"
            "fifths. <bookmark mark='d'/> The zig-zag adds a fifth and a twenty-fifth, <bookmark mark='e'/> which "
            "makes two fifths again: the same guarantee, on D to the fourth times as many vertices. <bookmark "
            "mark='f'/> One refinement, tensoring two half-size graphs before squaring, makes each neighbour cost "
            "time polynomial in log N."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2], shift=DOWN * 0.1), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(steps[2].copy(), steps[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]))
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in blocks], lag_ratio=0.3), FadeIn(bl))
            vo.wait_until("f")
            self.play(FadeIn(full))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ SL = L
    def reingold(self):
        head = label(r"Reingold: \ SL = L", font_size=36).to_edge(UP, buff=0.3)
        n = 14
        pos = ring(n, 1.55)
        cyc = [(k, (k + 1) % n) for k in range(n)]
        center = LEFT * 4.6 + UP * 0.45
        g0 = draw(pos, cyc, center=center, r=0.08, sw=2)
        g1 = draw(pos, random_regular_edges(n, 4, seed=5), center=center, r=0.08, sw=1.6)
        s_i, t_i = 0, 7
        for g in (g0, g1):
            g[1][s_i].set_color(DATA).scale(1.5)
            g[1][t_i].set_color(YES).scale(1.5)
        sl = label(r"$s$", font_size=24, color=DATA).next_to(g0.pts[s_i], UP, buff=0.12)
        tl = label(r"$t$", font_size=24, color=YES).next_to(g0.pts[t_i], DOWN, buff=0.12)
        cap0 = label(r"is $t$ reachable from $s$?", font_size=20, color=GREY_A).next_to(g0, DOWN, buff=0.45)
        cap1 = label(r"after the rounds: \ an expander", font_size=20, color=YES).move_to(cap0)
        # the gap, at least doubling each round (schematic)
        gaps = [min(0.03 * 2 ** k, 0.5) for k in range(7)]
        ax_o = np.array([-0.4, -1.6, 0])
        bars = VGroup()
        for k, gp in enumerate(gaps):
            h = 6.0 * gp
            b = Rectangle(width=0.45, height=h, stroke_width=0, fill_color=HEAD if gp < 0.5 else YES,
                          fill_opacity=0.85)
            b.move_to(ax_o + RIGHT * (0.4 + 0.7 * k) + UP * h / 2)
            bars.add(b)
        base = Line(ax_o, ax_o + RIGHT * 5.2, color=GREY_C, stroke_width=1.5)
        rl = VGroup(*[label(rf"{k}", font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.1).set_y(ax_o[1] - 0.2)
                      for k, b in enumerate(bars)])
        xl = label(r"round", font_size=17, color=GREY_A).next_to(rl, DOWN, buff=0.08)
        yl = label(r"spectral gap \ (schematic): \ at least doubles until it is a constant", font_size=18,
                   color=GREY_A).next_to(base, UP, buff=3.35).align_to(base, LEFT)
        tape = VGroup(*[tag_cell(t) for t in ("s", "3", "1", "4", "1", "2", "...", "4")]).arrange(RIGHT, buff=0.06)
        tlab = label(r"memory: \ a start and $O(\log N)$ edge labels, \ each from a constant range", font_size=19,
                     color=GREY_A)
        mem = VGroup(tape, tlab).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.45)
        hist = label(r"random walks: \ logarithmic memory, \ but coins \ (Aleliunas et al., \ 1979)",
                     font_size=18, color=GREY_B).next_to(mem, UP, buff=0.2)
        with self.voiceover(
            "It paid off in 2005. <bookmark mark='a'/> In an undirected graph, is t reachable from s? Breadth-first "
            "search remembers every vertex it has seen. A random walk needs only logarithmic memory, as Aleliunas and"
            " coauthors showed in 1979, but it needs coins. <bookmark mark='b'/> Omer Reingold removed them: repeat a"
            " round of zig-zag with a small fixed expander and a few squarings. <bookmark mark='c'/> Each round keeps"
            " the degree constant and at least doubles the spectral gap, until it is a constant. A connected graph "
            "starts with a gap of at least one over a polynomial in N, so logarithmically many rounds make every "
            "component an expander, of diameter order log N. <bookmark mark='d'/> Then try every walk of that length "
            "from s: a list of constant-size labels, in logarithmic memory. Symmetric logspace equals logspace."
        ) as vo:
            self.play(FadeIn(head), Create(g0[0]), FadeIn(g0[1]), FadeIn(sl), FadeIn(tl), FadeIn(cap0))
            vo.wait_until("a")
            self.play(FadeIn(hist))
            vo.wait_until("b")
            self.play(Create(base), FadeIn(rl), FadeIn(xl), FadeIn(yl))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=3)
            self.play(ReplacementTransform(g0, g1), ReplacementTransform(cap0, cap1))
            vo.wait_until("d")
            self.play(FadeIn(mem))
        self.wait(0.4)
        self.clear_scene()


def tag_cell(t):
    """One cell of a memory tape."""
    box = Square(side_length=0.42, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
    return VGroup(box, mono(t, size=18, color=HEAD if t != "s" else DATA).move_to(box))


_ = (BG, NO)
