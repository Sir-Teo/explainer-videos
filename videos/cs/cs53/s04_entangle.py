from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

EL, AZ = math.radians(18), math.radians(25)
R_VEC = np.array([-math.sin(AZ), math.cos(AZ), 0.0])
U_VEC = np.array([-math.sin(EL) * math.cos(AZ), -math.sin(EL) * math.sin(AZ), math.cos(EL)])
D_VEC = np.array([math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL)])


class Bloch(VGroup):
    """A Bloch sphere drawn in 2D: an orthographic view from slightly above, Bloch x toward the viewer (left),
    y to the right, z up.  Back halves of the circles are dimmed."""

    def __init__(self, center=ORIGIN, radius=2.0, labels=("0", "1", "+", "-", "+i", "-i"), font_size=24):
        super().__init__()
        self.c = np.array(center, dtype=float)
        self.r = radius
        self.add(Circle(radius=radius, color=GREY_C, stroke_width=2).move_to(self.c))
        for fn in (lambda t: (math.cos(t), math.sin(t), 0.0), lambda t: (math.sin(t), 0.0, math.cos(t))):
            self.add(self._circle(fn))
        for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            a = np.array(v, dtype=float) * 1.12
            self.add(DashedLine(self.p(-a), self.p(a), color=GREY_D, stroke_width=1.5, dash_length=0.07))
        pos = {"0": (0, 0, 1), "1": (0, 0, -1), "+": (1, 0, 0), "-": (-1, 0, 0), "+i": (0, 1, 0), "-i": (0, -1, 0)}
        self.labels = VGroup()
        for k in labels:
            v = np.array(pos[k], dtype=float)
            t = MathTex(rf"|{k}\rangle", font_size=font_size, color=GREY_A)
            out = self.p(v) - self.c
            t.move_to(self.p(v) + out / (np.linalg.norm(out) + 1e-9) * 0.38)
            if k in ("+i", "-i"):
                t.move_to([self.c[0] + (1 if k == "+i" else -1) * (radius + 0.42), self.p(v)[1], 0])
            self.labels.add(t)
        self.add(self.labels)

    def p(self, v):
        v = np.asarray(v, dtype=float)
        return self.c + self.r * (np.dot(v, R_VEC) * RIGHT + np.dot(v, U_VEC) * UP)

    def front(self, v) -> bool:
        return float(np.dot(v, D_VEC)) >= 0

    def _circle(self, fn, n=96):
        g = VGroup()
        ts = [2 * math.pi * k / n for k in range(n + 1)]
        for a, b in zip(ts, ts[1:]):
            va, vb = np.array(fn(a)), np.array(fn(b))
            on = self.front((va + vb) / 2)
            g.add(Line(self.p(va), self.p(vb), color=GREY_B if on else GREY_D, stroke_width=1.8 if on else 1.2,
                       stroke_opacity=0.9 if on else 0.45))
        return g

    def arrow(self, v, color=HEAD):
        tip = self.p(v)
        return VGroup(Line(self.c, tip, color=color, stroke_width=5), Dot(tip, radius=0.08, color=color))


def amp_bars(amps, names, scale=1.9, width=0.62, gap=0.38, font_size=24, values=None):
    """Signed amplitude bars on a common baseline, coloured by phase (0 blue, pi red); optional value labels."""
    g = VGroup()
    for i, (a, n) in enumerate(zip(amps, names)):
        col = DATA if a >= 0 else NO
        h = max(abs(a) * scale, 0.02)
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85 if abs(a) > 1e-9 else 0)
        x = i * (width + gap)
        r.move_to([x, 0, 0], aligned_edge=DOWN if a >= 0 else UP)
        t = MathTex(n, font_size=font_size, color=GREY_A).move_to([x, -0.32, 0])
        item = VGroup(r, t)
        if values is not None:
            item.add(MathTex(values[i], font_size=22, color=col).move_to([x, h + 0.25, 0]))
        g.add(item)
    base = Line([-width, 0, 0], [(len(amps) - 1) * (width + gap) + width, 0, 0], color=GREY_C, stroke_width=1.5)
    return VGroup(base, g)


class Entangle(VoiceoverScene):
    def construct(self):
        self.card()
        self.rotations()
        self.tensor()
        self.bell()
        self.game()
        self.quantum()
        self.cloning()

    def card(self):
        card = chapter_card(3, r"Gates, \ tensor products and entanglement",
                            r"What can two qubits do that two bits cannot?", lit=(1935, 1964, 1982),
                            extra=((1935, r"Einstein, \ Podolsky, \ Rosen"), (1964, r"Bell's inequality"),
                                   (1982, r"no-cloning: \ Wootters and Zurek; \ Dieks")), part=PART)
        with self.voiceover("Chapter three. Gates, tensor products and entanglement. What can two qubits do that "
                            "two bits cannot?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rotations(self):
        paths = load("bloch")
        head = label(r"Gates rotate the sphere", font_size=36).to_edge(UP, buff=0.3)
        B = Bloch(center=[-3.5, -0.45, 0], radius=2.35)
        cur = {"pts": [np.array(p) for p in paths["H on |0>"]]}
        k = ValueTracker(0.0)

        def vec():
            pts = cur["pts"]
            x = min(max(k.get_value(), 0.0), len(pts) - 1.0)
            i = min(int(x), len(pts) - 2)
            v = pts[i] * (1 - (x - i)) + pts[i + 1] * (x - i)
            return v / np.linalg.norm(v)
        arr = always_redraw(lambda: B.arrow(vec()))

        def path_line(pts, color):
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners([B.p(p) for p in pts])

        def card_(tex, cap, col):
            m = MathTex(tex, font_size=30, color=col)
            c = wrapped_label(cap, 2.7, font_size=18, color=GREY_A)
            body = VGroup(m, c).arrange(DOWN, buff=0.15)
            fr = RoundedRectangle(width=3.0, height=body.height + 0.35, corner_radius=0.12, stroke_color=GREY_D,
                                  stroke_width=1.5, fill_color=BG, fill_opacity=1)
            body.move_to(fr)
            return VGroup(fr, body)
        cards = VGroup(
            card_(r"H = \tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}", r"half turn about the axis between "
                  r"$x$ and $z$", HEAD),
            card_(r"T = \begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}", r"eighth turn about $z$", DATA),
            card_(r"S = T^2 = \begin{pmatrix}1&0\\0&i\end{pmatrix}", r"quarter turn about $z$", LAM),
            card_(r"R_x(\pi) = \begin{pmatrix}0&-i\\-i&0\end{pmatrix}", r"half turn about $x$: \ NOT, \ up to a "
                  r"phase", KERN),
        )
        hmax = max(c.height for c in cards)
        for c in cards:
            c[0].stretch_to_fit_height(hmax)
        cards.arrange_in_grid(rows=2, cols=2, buff=0.25).move_to([3.4, 0.75, 0])
        uni = VGroup(MathTex(r"U^\dagger U = I", font_size=34, color=YES),
                     wrapped_label(r"unitary: \ lengths kept, \ so probabilities still sum to 1; \ and $U^\dagger$ "
                                   r"undoes it: \ reversible, \ as chapter 1 asked", 4.4, font_size=19,
                                   color=WHITE)).arrange(RIGHT, buff=0.3).next_to(cards, DOWN, buff=0.35)
        src = note(r"paths: \ our simulator, \ the gates applied in small steps", font_size=16).to_corner(DL, buff=0.3)
        H_pts = cur["pts"]
        T_pts = [np.array(p) for p in paths["T on |+>"]]
        S_pts = [np.array(p) for p in paths["S on |+>"]]
        S2 = S_pts[len(S_pts) // 2:]
        X_pts = [np.array(p) for p in paths["Rx on |0>"]]

        def run(pts, color):
            cur["pts"] = pts
            k.set_value(0.0)
            self.play(k.animate.set_value(len(pts) - 1.0), Create(path_line(pts, color)), run_time=2.2,
                      rate_func=linear)
        with self.voiceover(
            "A one-qubit gate is a two by two unitary matrix: on the Bloch sphere, a rotation. <bookmark mark='a'/> "
            "The Hadamard gate is a half turn about the axis between x and z, carrying zero to plus. <bookmark "
            "mark='b'/> The T gate puts a phase of an eighth of a turn on the one amplitude: an eighth of a turn "
            "about the vertical axis. <bookmark mark='c'/> Two T gates make S, a quarter turn, to plus i. <bookmark "
            "mark='d'/> A half turn about x carries zero to one: a quantum NOT. <bookmark mark='e'/> Unitary means U "
            "dagger times U is the identity: lengths are kept, so probabilities still sum to one, and every gate can "
            "be undone."
        ) as vo:
            self.play(FadeIn(head), Create(B), FadeIn(src))
            cur["pts"] = H_pts
            self.play(FadeIn(arr))
            vo.wait_until("a")
            self.play(FadeIn(cards[0]), cards[0][0].animate.set_stroke(HEAD))
            run(H_pts, HEAD)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]), cards[1][0].animate.set_stroke(DATA))
            run(T_pts, DATA)
            vo.wait_until("c")
            self.play(FadeIn(cards[2]), cards[2][0].animate.set_stroke(LAM))
            run(S2, LAM)
            vo.wait_until("d")
            self.play(FadeIn(cards[3]), cards[3][0].animate.set_stroke(KERN))
            run(X_pts, KERN)
            vo.wait_until("e")
            self.play(FadeIn(uni))
        self.wait(0.4)
        self.clear_scene()

    def tensor(self):
        head = label(r"Two qubits: \ four amplitudes", font_size=36).to_edge(UP, buff=0.3)
        r0 = MathTex(r"(\alpha|0\rangle + \beta|1\rangle)", r"\otimes", r"(\gamma|0\rangle + \delta|1\rangle)",
                     font_size=34)
        r1 = MathTex(r"=", r"\alpha\gamma|00\rangle", r"+", r"\alpha\delta|01\rangle", r"+", r"\beta\gamma|10\rangle",
                     r"+", r"\beta\delta|11\rangle", font_size=34)
        r2 = MathTex(r"|\psi\rangle", r"=", r"a_{00}|00\rangle", r"+", r"a_{01}|01\rangle", r"+",
                     r"a_{10}|10\rangle", r"+", r"a_{11}|11\rangle", font_size=34, color=HEAD)
        VGroup(r0, r1, r2).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.4)
        w1 = label(r"a \textbf{product} of two independent qubits", font_size=18, color=GREY_B).next_to(r0, DOWN,
                                                                                                    buff=0.1)
        w2 = label(r"in general: \ any four amplitudes, \ squares summing to 1", font_size=18,
                   color=HEAD).next_to(r2, DOWN, buff=0.12)
        rows = VGroup()
        for n in range(1, 6):
            cells = VGroup(*[Square(side_length=0.13, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
                             for _ in range(2 ** n)]).arrange(RIGHT, buff=0.025)
            lab = label(rf"{n} qubit{'s' if n > 1 else ''}: \ $2^{{{n}}} = {2 ** n}$", font_size=19,
                        color=GREY_A)
            rows.add(VGroup(lab, cells))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        rows.next_to(w2, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        side = wrapped_label(r"a product state is described by $2n$ numbers; \ a general state needs all $2^n$: \ "
                             r"the difference is \textbf{entanglement}, \ and it is why Feynman's simulation is hard",
                             3.8, font_size=19, color=WHITE).next_to(rows, RIGHT, buff=0.5).align_to(rows, UP)
        with self.voiceover(
            "Now two qubits. <bookmark mark='a'/> Two independent qubits are described by the tensor product of "
            "their states. <bookmark mark='b'/> Multiplied out: one amplitude for each of the four outcomes. "
            "<bookmark mark='c'/> But any four amplitudes whose squares sum to one are allowed, not only those that "
            "factor. <bookmark mark='d'/> Each qubit doubles the count: n qubits have two to the n amplitudes. "
            "<bookmark mark='e'/> A product state needs only two n numbers. A state that does not factor is "
            "entangled, and in general needs all two to the n: that is why Feynman's simulation runs out of memory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r0), FadeIn(w1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r0.copy(), r1))
            vo.wait_until("c")
            self.play(TransformMatchingTex(r1.copy(), r2), FadeIn(w2))
            vo.wait_until("d")
            for r in rows:
                self.play(FadeIn(r[0]), LaggedStart(*[GrowFromCenter(c) for c in r[1]], lag_ratio=0.02),
                          run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def bell(self):
        b = load("bell")
        head = label(r"CNOT, \ and a state that does not factor", font_size=36).to_edge(UP, buff=0.3)
        y0, y1 = 2.0, 1.1
        xs = (-6.0, -1.0)
        wires = VGroup(*[Line([xs[0], y, 0], [xs[1], y, 0], color=GREY_B, stroke_width=2) for y in (y0, y1)])
        kets = VGroup(*[MathTex(r"|0\rangle", font_size=28, color=GREY_A).next_to([xs[0], y, 0], LEFT, buff=0.1)
                        for y in (y0, y1)])
        hb = VGroup(Square(side_length=0.55, stroke_color=HEAD, stroke_width=2.5, fill_color=BG, fill_opacity=1),
                    MathTex(r"H", font_size=30, color=HEAD)).move_to([-4.6, y0, 0])
        cx = -3.0
        cn = VGroup(Line([cx, y0, 0], [cx, y1 - 0.2, 0], color=WHITE, stroke_width=2.5), Dot([cx, y0, 0], radius=0.09),
                    Circle(radius=0.2, color=WHITE, stroke_width=2.5).move_to([cx, y1, 0]),
                    Line([cx - 0.2, y1, 0], [cx + 0.2, y1, 0], stroke_width=2.5),
                    Line([cx, y1 - 0.2, 0], [cx, y1 + 0.2, 0], stroke_width=2.5))
        cnl = label(r"CNOT: \ flip the second if the first is 1", font_size=18, color=GREY_A).next_to(
            VGroup(wires), DOWN, buff=0.3)
        marks = VGroup(*[DashedLine([x, y0 + 0.4, 0], [x, y1 - 0.4, 0], color=GREY_D, dash_length=0.06)
                         for x in (-5.4, -3.8, -2.0)])
        names = [r"|00\rangle", r"|01\rangle", r"|10\rangle", r"|11\rangle"]
        s2 = 1 / math.sqrt(2)
        stages = [[1, 0, 0, 0], [s2, 0, s2, 0], [a[0] for a in b["amplitudes"]]]
        anchor = np.array([-5.6, -2.3, 0])

        def make(i, values=None):
            g = amp_bars(stages[i], names, values=values)
            g.shift(anchor - g[0].get_left())
            return g
        bars = [make(0), make(1), make(2, values=[f"{p:.2f}" for p in b["probs"]])]
        blab = label(r"amplitudes \ (after each step)", font_size=18, color=GREY_B).next_to(bars[0], UP, buff=0.2)
        blab.set_y(-0.05)
        plab = label(r"probabilities on top: \ our simulator", font_size=16, color=GREY_B).next_to(
            bars[2], DOWN, buff=0.15)
        rows = VGroup(
            MathTex(r"\alpha\gamma", r"=", r"\beta\delta", r"=", r"\tfrac{1}{\sqrt2}", r",\quad", r"\alpha\delta", r"=",
                    r"\beta\gamma", r"=", r"0", font_size=30),
            MathTex(r"\alpha\delta", r"=", r"0", r"\;\Rightarrow\;", r"\alpha = 0", r"\text{ or }", r"\delta = 0",
                    font_size=30),
            MathTex(r"\;\Rightarrow\;", r"\alpha\gamma = 0", r"\text{ or }", r"\beta\delta = 0", font_size=30),
            MathTex(r"\text{contradiction: \ entangled}", font_size=30, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, 0.2, 0])
        why0 = label(r"if it were a product, \ matching the four amplitudes:", font_size=18,
                     color=GREY_B).next_to(rows[0], UP, buff=0.2).align_to(rows[0], LEFT)
        bottom = wrapped_label(r"measure either qubit: \ 0 or 1 at random, \ and the other always agrees", 4.8,
                               font_size=19, color=WHITE).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        with self.voiceover(
            "The basic two-qubit gate is the controlled-NOT, which flips the second qubit when the first is one. "
            "<bookmark mark='a'/> Start with both qubits at zero. <bookmark mark='b'/> A Hadamard on the first gives "
            "equal amplitudes on zero zero and one zero. <bookmark mark='c'/> The CNOT turns one zero into one one. "
            "Our simulator gives half a chance of zero zero, half of one one, and nothing else: a Bell state. "
            "<bookmark mark='d'/> Is it two separate qubits? Then alpha delta is zero, so alpha or delta is zero, "
            "and one of the surviving amplitudes would vanish too. Contradiction: the state is entangled. <bookmark "
            "mark='e'/> Measure either qubit: the result is random, but the other always agrees."
        ) as vo:
            self.play(FadeIn(head), Create(wires), FadeIn(kets), FadeIn(hb), FadeIn(cn), FadeIn(cnl))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(bars[0]), FadeIn(blab))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), ReplacementTransform(bars[0], bars[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2]), ReplacementTransform(bars[1], bars[2]), FadeIn(plab))
            vo.wait_until("d")
            self.play(FadeIn(why0), Write(rows[0]))
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(bottom))
        self.wait(0.4)
        self.clear_scene()

    def game(self):
        c = load("chsh")
        head = label(r"The CHSH game", font_size=36).to_edge(UP, buff=0.3)

        def box(t, col, w=1.7):
            r = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            return VGroup(r, label(t, font_size=22, color=col).move_to(r))
        ref = box(r"referee", GREY_A, w=2.0).move_to([-3.6, 1.9, 0])
        alice = box(r"Alice", DATA).move_to([-5.4, -0.1, 0])
        bob = box(r"Bob", LAM).move_to([-1.8, -0.1, 0])

        def link(a, b_, t, side):
            ar = Arrow(a, b_, buff=0.12, stroke_width=2.5, color=GREY_B, max_tip_length_to_length_ratio=0.15)
            return VGroup(ar, MathTex(t, font_size=28, color=WHITE).next_to(ar.get_center(), side, buff=0.15))
        lx = link(ref.get_bottom() + LEFT * 0.5, alice.get_top() + RIGHT * 0.2, r"x", LEFT)
        ly = link(ref.get_bottom() + RIGHT * 0.5, bob.get_top() + LEFT * 0.2, r"y", RIGHT)
        la = link(alice.get_bottom(), alice.get_bottom() + DOWN * 0.8, r"a", LEFT)
        lb = link(bob.get_bottom(), bob.get_bottom() + DOWN * 0.8, r"b", RIGHT)
        wall = DashedLine([-3.6, 0.7, 0], [-3.6, -1.4, 0], color=NO, dash_length=0.08)
        wl = label(r"no talking", font_size=17, color=NO).next_to(wall, DOWN, buff=0.1)
        rule = MathTex(r"\text{win if } a \oplus b = x \wedge y", font_size=32, color=HEAD).move_to([-3.6, -2.6, 0])
        rows = VGroup(
            MathTex(r"a_0 \oplus b_0 = 0,\;\; a_0 \oplus b_1 = 0,\;\; a_1 \oplus b_0 = 0,\;\; a_1 \oplus b_1 = 1",
                    font_size=26),
            MathTex(r"\text{XOR of the left sides: } 0", font_size=28),
            MathTex(r"\text{XOR of the right sides: } 1", font_size=28),
            MathTex(rf"\text{{at most 3 of 4 hold: \ win}} \le \tfrac34 = {c['classical']:.2f}", font_size=30,
                    color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([2.95, 0.15, 0])
        whys = VGroup(
            label(r"a deterministic strategy: \ $a_x$ for Alice, \ $b_y$ for Bob, \ all four cases", font_size=18,
                  color=GREY_B),
            label(r"each of $a_0, a_1, b_0, b_1$ appears twice", font_size=18, color=GREY_B),
            label(r"only the case $x = y = 1$ asks for a 1", font_size=18, color=GREY_B),
            label(r"shared random coins only mix such strategies: \ still $\tfrac34$", font_size=18, color=GREY_B),
        )
        whys[0].next_to(rows[0], UP, buff=0.15).align_to(rows[0], LEFT)
        for w, r in zip(whys[1:], rows[1:]):
            w.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        src = note(r"checked: \ our search over all 16 deterministic strategies", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Agreeing on random bits is easy: toss a coin in advance. This game needs more. <bookmark mark='a'/> A "
            "referee sends Alice a random bit x and Bob a random bit y, and they cannot talk. They win if the XOR of "
            "their answers equals x AND y: they must agree, unless both questions were one. <bookmark mark='b'/> A "
            "classical strategy fixes an answer for each question. <bookmark mark='c'/> XOR the four conditions. On "
            "the left each answer appears twice and cancels; on the right we get one. So at most three can hold. "
            "<bookmark mark='d'/> No classical strategy wins more than three quarters of the time, and our search "
            "through all sixteen confirms it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ref), FadeIn(alice), FadeIn(bob))
            vo.wait_until("a")
            self.play(GrowArrow(lx[0]), FadeIn(lx[1]), GrowArrow(ly[0]), FadeIn(ly[1]), Create(wall), FadeIn(wl))
            self.play(GrowArrow(la[0]), FadeIn(la[1]), GrowArrow(lb[0]), FadeIn(lb[1]), Write(rule))
            vo.wait_until("b")
            self.play(FadeIn(whys[0]), Write(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def quantum(self):
        c = load("chsh")
        head = label(r"Sharing a Bell pair wins more often", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"P(a = b)", r"=", r"\cos^2(A - B)", font_size=32),
            MathTex(r"|A - B| = \tfrac{\pi}{8}", r":\;\;", r"\text{win} = \cos^2\tfrac{\pi}{8}", font_size=32),
            MathTex(r"|A - B| = \tfrac{3\pi}{8}", r":\;\;", r"\text{win} = \sin^2\tfrac{3\pi}{8} = "
                    r"\cos^2\tfrac{\pi}{8}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([-3.3, 1.0, 0])
        whys = VGroup(
            wrapped_label(r"each measures the shared pair along an angle in the plane of real amplitudes", 5.8,
                          font_size=18, color=GREY_B),
            wrapped_label(r"Alice $A = 0$ or $\tfrac{\pi}{4}$; \ Bob $B = \pm\tfrac{\pi}{8}$: \ three cases need "
                          r"agreement", 5.8, font_size=18, color=GREY_B),
            wrapped_label(r"$x = y = 1$ needs disagreement, \ and gets it just as often", 5.8, font_size=18,
                          color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        ax_x0, ax_y0, H = 1.2, -1.6, 3.6
        items = [(r"classical best", c["classical"], NO), (r"quantum, \ exact", c["quantum"], YES),
                 (r"quantum, \ sampled", c["sampled"], DATA)]
        chart = VGroup()
        for i, (name, v, col) in enumerate(items):
            x = ax_x0 + 0.7 + i * 1.75
            r = Rectangle(width=1.1, height=v * H, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([x, ax_y0, 0], aligned_edge=DOWN)
            chart.add(VGroup(r, label(f"{v:.3f}", font_size=20, color=col).next_to(r, UP, buff=0.1),
                             label(name, font_size=17, color=GREY_A).next_to([x, ax_y0, 0], DOWN, buff=0.15)))
        base = Line([ax_x0, ax_y0, 0], [ax_x0 + 5.3, ax_y0, 0], color=GREY_C, stroke_width=1.5)
        half = DashedLine([ax_x0, ax_y0 + 0.75 * H, 0], [ax_x0 + 5.3, ax_y0 + 0.75 * H, 0], color=GREY_D,
                          dash_length=0.08)
        notes = wrapped_label(r"Tsirelson \ (1980): \ $\cos^2\tfrac{\pi}{8}$ is the best any quantum strategy can do; "
                              r"\ Part 27's MIP* = RE \ (2020) \ was built on games like this", 12.4, font_size=19,
                              color=HEAD).to_edge(DOWN, buff=0.35)
        exp = wrapped_label(r"no message passes: \ alone, \ each side's answers are fair coin flips", 5.8,
                            font_size=19, color=WHITE).next_to(whys[2], DOWN, buff=0.35).align_to(rows, LEFT)
        with self.voiceover(
            "Give Alice and Bob one qubit each of a Bell pair. <bookmark mark='a'/> Each measures along an angle set "
            "by the question; they agree with probability cosine squared of the difference. <bookmark mark='b'/> "
            "Alice uses zero or forty-five degrees, Bob plus or minus twenty-two and a half. In three cases the "
            "angles differ by twenty-two and a half degrees: agreement with probability cosine squared of pi over "
            "eight. <bookmark mark='c'/> In the fourth they differ by sixty-seven and a half, and disagree just as "
            "often. <bookmark mark='d'/> About eighty-five percent against seventy-five; our simulator agrees. No "
            "message passes. <bookmark mark='e'/> Boris Tsirelson proved in 1980 that no quantum strategy does "
            "better, and Part 27's MIP equals RE grew from games like this."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(half))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(it[0], DOWN) for it in chart], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(it[1], it[2])) for it in chart], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(exp))
            vo.wait_until("e")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def cloning(self):
        cl = load("cloning")
        head = label(r"No cloning, \ in three lines", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"U|\psi\rangle|0\rangle = |\psi\rangle|\psi\rangle", r",\quad",
                    r"U|\varphi\rangle|0\rangle = |\varphi\rangle|\varphi\rangle", font_size=29),
            MathTex(r"\langle\varphi|\psi\rangle", r"=", r"\langle\varphi|\psi\rangle^2", font_size=34),
            MathTex(r"\langle\varphi|\psi\rangle", r"=", r"0 \text{ or } 1", font_size=34, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to([-3.3, 1.1, 0])
        whys = VGroup(
            label(r"suppose one machine $U$ copies every state", font_size=18, color=GREY_B),
            wrapped_label(r"inner product of the two lines: \ $U$ preserves it, \ and $\langle 0|0\rangle = 1$", 5.8,
                          font_size=18, color=GREY_B),
            wrapped_label(r"only identical or orthogonal states: \ no machine copies them all \ (Wootters and "
                          r"Zurek; \ Dieks, \ 1982)", 5.8, font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        names = [r"|00\rangle", r"|01\rangle", r"|10\rangle", r"|11\rangle"]
        got = amp_bars(cl["state"], names, scale=1.7)
        want = amp_bars([0.5] * 4, names, scale=1.7)
        gl = label(r"CNOT on $|{+}\rangle|0\rangle$: \ a Bell pair", font_size=19, color=DATA)
        wl = label(r"two copies, \ $|{+}\rangle|{+}\rangle$, \ would be", font_size=19, color=GREY_A)
        right = VGroup(VGroup(gl, got).arrange(DOWN, buff=0.3), VGroup(wl, want).arrange(DOWN, buff=0.3)).arrange(
            DOWN, buff=0.55).move_to([3.7, 0.6, 0])
        fid = label(rf"overlap with two copies: \ {cl['fidelity']:.2f}", font_size=21, color=NO).next_to(
            right, DOWN, buff=0.3)
        foot = wrapped_label(r"CNOT copies $|0\rangle$ and $|1\rangle$ perfectly: \ classical bits can be copied, \ "
                             r"superpositions cannot; \ this is why error correction looked impossible \ (chapter "
                             r"12) \ and why eavesdroppers are caught \ (chapter 13)", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "No quantum computer can copy an unknown state; the proof takes three lines. <bookmark mark='a'/> "
            "Suppose one unitary machine copies every state: psi to psi psi, phi to phi phi. <bookmark mark='b'/> "
            "Take the inner product of the two lines. Unitaries preserve it, so the overlap of phi and psi equals "
            "its own square. <bookmark mark='c'/> So the overlap is zero or one: one machine copies only states that "
            "are identical or orthogonal. <bookmark mark='d'/> CNOT copies zero and one perfectly, but fed plus it "
            "makes a Bell pair, not two pluses: our simulator puts the overlap at one half. <bookmark mark='e'/> "
            "This made error correction look impossible, and it is why eavesdroppers get caught."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(right[0]))
            self.play(FadeIn(right[1]))
            self.play(FadeIn(fid))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG)
