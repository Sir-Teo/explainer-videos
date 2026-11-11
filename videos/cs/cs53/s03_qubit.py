from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES

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
            out = self.p(v * 1.0) - self.c
            n = out / (np.linalg.norm(out) + 1e-9)
            t.move_to(self.p(v) + n * 0.38 + (UP * 0.05 if k in "01" else 0))
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


def sph(theta, phi):
    return np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)])


def bars(values, names, colors, width=0.7, scale=2.0, gap=0.5, font_size=24):
    """Vertical bars from a common baseline; a negative value hangs below it."""
    g = VGroup()
    for v, n, c in zip(values, names, colors):
        h = max(abs(v) * scale, 0.02)
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
        r.move_to(ORIGIN, aligned_edge=DOWN if v >= 0 else UP)
        t = MathTex(n, font_size=font_size, color=GREY_A).move_to(DOWN * 0.3 if v >= 0 else UP * 0.3)
        g.add(VGroup(r, t))
    g.arrange(RIGHT, buff=gap, aligned_edge=ORIGIN)
    for b in g:
        b[1].set_x(b[0].get_x())
    return g


class Qubit(VoiceoverScene):
    def construct(self):
        self.card()
        self.amplitudes()
        self.phases()
        self.sphere()
        self.measure()
        self.holevo()

    def card(self):
        card = chapter_card(2, r"The qubit", r"What does one quantum bit hold?", lit=(1926, 1973, 1995),
                            extra=((1926, r"Born: \ the probability rule"),
                                   (1973, r"Holevo: \ $n$ qubits carry $n$ bits"),
                                   (1995, r"Schumacher names the qubit")), part=PART)
        with self.voiceover("Chapter two. The qubit. What does one quantum bit actually hold?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def amplitudes(self):
        head = label(r"Two amplitudes, \ and the Born rule", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-4.4, -0.4, 0])
        R = 1.75
        circ = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(c)
        ax = VGroup(Line(c + LEFT * (R + 0.3), c + RIGHT * (R + 0.3), color=GREY_D, stroke_width=1.5),
                    Line(c + DOWN * (R + 0.3), c + UP * (R + 0.3), color=GREY_D, stroke_width=1.5))
        k0 = MathTex(r"|0\rangle", font_size=26, color=DATA).next_to(c + RIGHT * (R + 0.3), RIGHT, buff=0.1)
        k1 = MathTex(r"|1\rangle", font_size=26, color=LAM).next_to(c + UP * (R + 0.3), UP, buff=0.08)
        t = ValueTracker(0.0)

        def tip():
            return c + R * (math.cos(t.get_value()) * RIGHT + math.sin(t.get_value()) * UP)
        vec = always_redraw(lambda: Arrow(c, tip(), buff=0, color=HEAD, stroke_width=5,
                                          max_tip_length_to_length_ratio=0.12))
        proj = always_redraw(lambda: VGroup(
            DashedLine(tip(), [tip()[0], c[1], 0], color=DATA, dash_length=0.06),
            DashedLine(tip(), [c[0], tip()[1], 0], color=LAM, dash_length=0.06)))
        eqs = VGroup(
            MathTex(r"|\psi\rangle", r"=", r"\alpha", r"|0\rangle", r"+", r"\beta", r"|1\rangle", font_size=36),
            MathTex(r"P(0) = |\alpha|^2, \quad P(1) = |\beta|^2", font_size=32),
            MathTex(r"|\alpha|^2 + |\beta|^2 = 1", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.45).move_to([0.6, 0.6, 0])
        eqs[0][2].set_color(DATA)
        eqs[0][5].set_color(LAM)
        base = np.array([3.6, -1.6, 0])
        S = 2.6

        def pbars():
            a, b = math.cos(t.get_value()), math.sin(t.get_value())
            g = VGroup()
            for i, (p, col, n) in enumerate(((a * a, DATA, r"P(0)"), (b * b, LAM, r"P(1)"))):
                x = base[0] + i * 1.4
                r = Rectangle(width=0.8, height=max(p * S, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([x, base[1], 0], aligned_edge=DOWN)
                g.add(r, MathTex(n, font_size=24, color=GREY_A).move_to([x, base[1] - 0.3, 0]),
                      MathTex(f"{p:.2f}", font_size=24, color=col).next_to(r, UP, buff=0.1))
            return g
        pb = always_redraw(pbars)
        frame = Line(base + LEFT * 0.7, base + RIGHT * 2.1, color=GREY_C, stroke_width=1.5)
        neg = wrapped_label(r"amplitudes may be negative \ (and complex): \ unlike probabilities they can cancel, "
                            r"\ which is chapter 5's interference", 4.4, font_size=19, color=HEAD)
        neg.next_to(eqs, DOWN, buff=0.5).set_x(0.3)
        ill = note(r"illustrative angles", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "A qubit's state is a vector with two components, called amplitudes: alpha times the state zero, plus "
            "beta times the state one. <bookmark mark='a'/> Draw the two basis states as perpendicular axes, and the "
            "state as a unit arrow between them. <bookmark mark='b'/> When we measure, we see zero with probability "
            "alpha squared and one with probability beta squared. This is the Born rule, from 1926, and it is why "
            "the arrow has length one: the probabilities must add to one. <bookmark mark='c'/> Turn the arrow and "
            "the odds change smoothly. <bookmark mark='d'/> But an amplitude can also be negative, and in general "
            "complex. This arrow gives the same probabilities as the first, yet it is a different state. "
            "Probabilities can only add up; amplitudes can cancel, and quantum algorithms are built on that "
            "difference."
        ) as vo:
            self.play(FadeIn(head), Write(eqs[0]))
            vo.wait_until("a")
            self.play(Create(circ), FadeIn(ax), FadeIn(k0), FadeIn(k1), FadeIn(vec), FadeIn(proj), FadeIn(ill))
            self.play(t.animate.set_value(math.pi / 4), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(frame), FadeIn(pb))
            self.play(FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(t.animate.set_value(math.pi / 2.6), run_time=1.5)
            self.play(t.animate.set_value(math.pi / 8), run_time=1.5)
            vo.wait_until("d")
            self.play(t.animate.set_value(3 * math.pi / 4),
                      run_time=2.0)
            self.play(FadeIn(neg))
        self.wait(0.4)
        self.clear_scene()

    def phases(self):
        head = label(r"Two angles are enough", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"|\psi\rangle", r"=", r"\alpha", r"|0\rangle", r"+", r"\beta", r"|1\rangle", font_size=34),
            MathTex(r"|\psi\rangle", r"=", r"|\alpha|", r"|0\rangle", r"+", r"e^{i\varphi}", r"|\beta|", r"|1\rangle",
                    font_size=34),
            MathTex(r"|\psi\rangle", r"=", r"\cos\tfrac{\theta}{2}", r"|0\rangle", r"+", r"e^{i\varphi}",
                    r"\sin\tfrac{\theta}{2}", r"|1\rangle", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.95).move_to([-3.0, 0.5, 0])
        whys = VGroup(
            wrapped_label(r"$\alpha, \beta$ complex: \ four real numbers, \ and $|\alpha|^2 + |\beta|^2 = 1$ leaves "
                          r"three", 6.2, font_size=18, color=GREY_B),
            wrapped_label(r"multiplying the whole state by $e^{i\gamma}$ changes no probability: \ drop it, \ keep "
                          r"the \textbf{relative phase} $\varphi$", 6.2, font_size=18, color=GREY_B),
            wrapped_label(r"$|\alpha|^2 + |\beta|^2 = 1$: \ write $|\alpha| = \cos\tfrac{\theta}{2}$, \ $|\beta| = "
                          r"\sin\tfrac{\theta}{2}$, \ with $0 \le \theta \le \pi$", 6.2, font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        punch = label(r"two angles, \ $\theta$ and $\varphi$: \ a point on a sphere", font_size=24,
                      color=HEAD).to_edge(DOWN, buff=0.45).set_x(-3.0)
        s2 = 1 / math.sqrt(2)
        plus = bars([s2, s2], [r"|0\rangle", r"|1\rangle"], [DATA, DATA], scale=1.6)
        minus = bars([s2, -s2], [r"|0\rangle", r"|1\rangle"], [DATA, NO], scale=1.6)
        pt = MathTex(r"|{+}\rangle = \tfrac{1}{\sqrt2}(|0\rangle + |1\rangle)", font_size=28)
        mt = MathTex(r"|{-}\rangle = \tfrac{1}{\sqrt2}(|0\rangle - |1\rangle)", font_size=28)
        right = VGroup(VGroup(pt, plus).arrange(DOWN, buff=0.3), VGroup(mt, minus).arrange(DOWN, buff=0.3)).arrange(
            DOWN, buff=0.5).move_to([3.9, 0.3, 0])
        same = wrapped_label(r"the same probabilities, \ $\tfrac12$ and $\tfrac12$, \ but different states: \ "
                             r"only the relative phase differs", 4.6, font_size=19, color=WHITE).next_to(
            right, DOWN, buff=0.35)
        key = note(r"bar colour: \ phase $0$ blue, \ phase $\pi$ red", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "How many numbers does a qubit need? <bookmark mark='a'/> Alpha and beta are complex, so four real "
            "numbers, with one constraint: three are left. <bookmark mark='b'/> Multiply the whole state by a phase "
            "and no measurement can tell the difference, so we may drop that overall phase. What remains physical is "
            "the relative phase between the two amplitudes, phi. <bookmark mark='c'/> And because the squared sizes "
            "add to one, they are the cosine and sine of one angle, which we call theta over two. <bookmark "
            "mark='d'/> Two angles: a point on a sphere. <bookmark mark='e'/> The relative phase is invisible to a "
            "measurement of zero against one. The plus state and the minus state both give fifty-fifty odds, "
            "differing only in one sign. Yet they are as different as two states can be: in the next chapter one "
            "gate turns the first into zero and the second into one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(punch))
            vo.wait_until("e")
            self.play(FadeIn(right[0]), FadeIn(key))
            self.play(FadeIn(right[1]))
            self.play(FadeIn(same))
        self.wait(0.4)
        self.clear_scene()

    def sphere(self):
        head = label(r"The Bloch sphere", font_size=36).to_edge(UP, buff=0.3)
        B = Bloch(center=[-3.0, -0.35, 0], radius=2.4)
        th, ph = ValueTracker(0.0), ValueTracker(0.0)
        arr = always_redraw(lambda: B.arrow(sph(th.get_value(), ph.get_value())))
        trail = TracedPath(lambda: B.p(sph(th.get_value(), ph.get_value())), stroke_color=HEAD, stroke_width=2,
                           stroke_opacity=0.6)
        eqs = VGroup(
            MathTex(r"x = \sin\theta\cos\varphi", font_size=32),
            MathTex(r"y = \sin\theta\sin\varphi", font_size=32),
            MathTex(r"z = \cos\theta", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.6, 0])
        notes = VGroup(
            wrapped_label(r"$\theta$: \ the latitude, \ from $|0\rangle$ at the north pole to $|1\rangle$ at the "
                          r"south", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"$\varphi$: \ the longitude, \ the relative phase: \ $|{+}\rangle$, \ $|{+}i\rangle$, \ "
                          r"$|{-}\rangle$, \ $|{-}i\rangle$ around the equator", 5.4, font_size=19, color=DATA),
            wrapped_label(r"the half angle $\theta/2$ doubles on the sphere: \ \textbf{orthogonal states are "
                          r"opposite points}, \ not a right angle apart", 5.4, font_size=19, color=HEAD),
            wrapped_label(r"for a spin, \ the arrow is the axis along which it is certainly up: \ the physics is in "
                          r"\textit{Quantum Mechanics, \ Visualized}", 5.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(eqs, DOWN, buff=0.4)
        with self.voiceover(
            "Felix Bloch's sphere draws every state of one qubit as a point on a ball. <bookmark mark='a'/> Theta is "
            "the latitude: zero sits at the north pole and one at the south. <bookmark mark='b'/> Tip the arrow down "
            "to the equator and we reach the plus state, an equal superposition. <bookmark mark='c'/> Phi is the "
            "longitude, the relative phase. Going once round the equator passes the states plus i, minus, and minus "
            "i, all with fifty-fifty odds. <bookmark mark='d'/> Notice what the half angle did. Zero and one are "
            "perpendicular vectors, but on the sphere they are opposite poles; plus and minus are opposite too. "
            "Every pair of orthogonal states sits at the two ends of a diameter. <bookmark mark='e'/> For an "
            "electron's spin, the arrow is the axis along which a measurement is certain to find the spin pointing "
            "up."
        ) as vo:
            self.play(FadeIn(head), Create(B), FadeIn(arr), FadeIn(eqs))
            self.add(trail)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(th.animate.set_value(math.pi / 2), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(ph.animate.set_value(2 * math.pi), run_time=4, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            self.play(th.animate.set_value(math.pi), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def measure(self):
        head = label(r"Measuring: \ the arrow's height", font_size=36).to_edge(UP, buff=0.3)
        B = Bloch(center=[-4.0, -0.4, 0], radius=2.2, labels=("0", "1", "+", "+i"))
        th = ValueTracker(math.pi / 3)
        phi = math.pi / 5

        def v():
            return sph(th.get_value(), phi)
        arr = always_redraw(lambda: B.arrow(v()))
        drop = always_redraw(lambda: VGroup(
            DashedLine(B.p(v()), B.p([0, 0, v()[2]]), color=GREY_A, dash_length=0.06),
            Dot(B.p([0, 0, v()[2]]), radius=0.07, color=YES)))
        rows = VGroup(
            MathTex(r"P(0)", r"=", r"|\alpha|^2", r"=", r"\cos^2\tfrac{\theta}{2}", font_size=34),
            MathTex(r"P(0)", r"=", r"\tfrac{1 + \cos\theta}{2}", font_size=34),
            MathTex(r"P(0)", r"=", r"\tfrac{1 + z}{2}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([0.9, 1.0, 0])
        whys = VGroup(label(r"the Born rule", font_size=18, color=GREY_B),
                      label(r"the double-angle formula", font_size=18, color=GREY_B),
                      label(r"$z = \cos\theta$: \ the arrow's height", font_size=18, color=HEAD))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        base = np.array([4.6, -1.2, 0])
        S = 2.4

        def pbars():
            z = v()[2]
            g = VGroup()
            for i, (p, col, n) in enumerate((((1 + z) / 2, YES, r"P(0)"), ((1 - z) / 2, NO, r"P(1)"))):
                x = base[0] + i * 1.3
                r = Rectangle(width=0.75, height=max(p * S, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([x, base[1], 0], aligned_edge=DOWN)
                g.add(r, MathTex(n, font_size=24, color=GREY_A).move_to([x, base[1] - 0.3, 0]))
            return g
        pb = always_redraw(pbars)
        line = Line(base + LEFT * 0.6, base + RIGHT * 1.9, color=GREY_C, stroke_width=1.5)
        after = wrapped_label(r"after measuring, \ the state \textbf{is} the answer: \ the arrow jumps to a pole",
                              5.4, font_size=19, color=WHITE).move_to([2.0, -2.45, 0])
        other = wrapped_label(r"to measure along another axis, \ first rotate that axis to $z$ \ (the gates of "
                              r"chapter 3)", 5.4, font_size=19, color=DATA).next_to(after, DOWN, buff=0.2)
        ill = note(r"illustrative state and outcome", font_size=16).to_corner(DL, buff=0.3)
        with self.voiceover(
            "What does a measurement see on the sphere? <bookmark mark='a'/> By the Born rule, the chance of a zero "
            "is the cosine squared of half of theta. <bookmark mark='b'/> The double-angle formula turns that into "
            "one plus cosine theta, over two. <bookmark mark='c'/> And cosine theta is just the arrow's height, z. "
            "The probability of zero is one plus the height, over two: certain at the north pole, impossible at the "
            "south, and even anywhere on the equator, whatever the phase. <bookmark mark='d'/> Measurement is not "
            "gentle. Afterwards the state is the answer we saw: the arrow has jumped to a pole, and the rest of the "
            "information is gone. <bookmark mark='e'/> To ask about a different axis, rotate it to the vertical "
            "first, and then measure."
        ) as vo:
            self.play(FadeIn(head), Create(B), FadeIn(arr), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]), FadeIn(drop), FadeIn(line),
                      FadeIn(pb))
            self.play(th.animate.set_value(0.15), run_time=1.5)
            self.play(th.animate.set_value(math.pi - 0.15), run_time=2.5)
            self.play(th.animate.set_value(math.pi / 2), run_time=1.5)
            vo.wait_until("d")
            self.play(th.animate.set_value(0.0), run_time=0.4)
            self.play(Flash(B.p([0, 0, 1]), color=YES), FadeIn(after))
            vo.wait_until("e")
            self.play(FadeIn(other))
        self.wait(0.4)
        self.clear_scene()

    def holevo(self):
        head = label(r"A continuum of states, \ one bit out", font_size=36).to_edge(UP, buff=0.3)
        B = Bloch(center=[-4.3, 0.75, 0], radius=1.55, labels=("0", "1"), font_size=22)
        import random
        rng = random.Random(7)
        dots = VGroup()
        for _ in range(60):
            z = rng.uniform(-1, 1)
            p = rng.uniform(0, 2 * math.pi)
            s = math.sqrt(1 - z * z)
            v = (s * math.cos(p), s * math.sin(p), z)
            dots.add(Dot(B.p(v), radius=0.045, color=DATA if B.front(v) else GREY_D))
        meter = RoundedRectangle(width=1.8, height=0.9, corner_radius=0.12, stroke_color=KERN, stroke_width=2,
                                 fill_color=BG, fill_opacity=1).move_to([-0.6, 0.75, 0])
        mt = label(r"measure", font_size=20, color=KERN).move_to(meter)
        out = VGroup(tag_box_local("0", YES), tag_box_local("1", NO)).arrange(DOWN, buff=0.3).move_to([2.0, 0.75, 0])
        a1 = Arrow(B.get_right() + RIGHT * 0.1, meter.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(meter.get_right(), out.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        hol = wrapped_label(r"Holevo, \ 1973: \ $n$ qubits sent on their own carry at most $n$ classical bits: "
                            r"\ the continuum is not storage", 3.5, font_size=19, color=HEAD).move_to([4.9, 0.75, 0])

        def tile(title, body, col):
            fr = RoundedRectangle(width=3.05, height=1.75, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                  fill_color=BG, fill_opacity=1)
            g = VGroup(label(title, font_size=20, color=col), wrapped_label(body, 2.8, font_size=17, color=GREY_A))
            g.arrange(DOWN, buff=0.12).move_to(fr)
            return VGroup(fr, g)
        tiles = VGroup(
            tile(r"superconducting circuits", r"the two lowest energy levels of a circuit cooled near absolute "
                 r"zero", DATA),
            tile(r"trapped ions", r"two levels of a single charged atom held by electric fields", YES),
            tile(r"neutral atoms", r"atoms held in a grid of laser tweezers", LAM),
            tile(r"photons", r"polarisation, \ or which of two paths a photon takes", KERN),
        ).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.45)
        cap = label(r"any two-level quantum system will do:", font_size=21, color=WHITE).next_to(tiles, UP, buff=0.25)
        with self.voiceover(
            "So a qubit's state takes a continuum of values. <bookmark mark='a'/> Can we store a whole real number "
            "in it? <bookmark mark='b'/> No. A measurement returns one bit, and destroys the rest. Alexander Holevo "
            "proved in 1973 that n qubits sent on their own can carry at most n bits of classical information. "
            "<bookmark mark='c'/> The power of quantum computers is not storage. It comes from what happens to many "
            "qubits together, before anyone looks: their amplitudes multiply in number and interfere. <bookmark "
            "mark='d'/> Physically, a qubit is any well-controlled two-level system: two energy levels of a "
            "superconducting circuit, or of a trapped ion; atoms held by laser tweezers; or a photon's polarisation. "
            "The mathematics is the same for all of them."
        ) as vo:
            self.play(FadeIn(head), Create(B))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(meter), FadeIn(mt))
            self.play(GrowArrow(a2), FadeIn(out))
            self.play(FadeIn(hol))
            vo.wait_until("c")
            self.play(Indicate(hol, color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.3),
                      run_time=2.5)
        self.wait(0.4)
        self.clear_scene()


def tag_box_local(text, color):
    t = MathTex(rf"\text{{{text}}}", font_size=30, color=color)
    box = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.08, stroke_color=color, stroke_width=1.8,
                           fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


_ = (KERN, LAM, NO, YES)
