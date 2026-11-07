from __future__ import annotations

import cmath as cm
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono


def dial(frac, color=HEAD, r=0.42):
    """A relative phase drawn as an arrow turned by ``frac`` of a full turn, from the right."""
    c = Circle(radius=r, color=GREY_C, stroke_width=1.5)
    a = Arrow(ORIGIN, r * np.array([math.cos(2 * PI * frac), math.sin(2 * PI * frac), 0]), buff=0, color=color,
              stroke_width=3, max_tip_length_to_length_ratio=0.3)
    zero = Line([r - 0.08, 0, 0], [r + 0.08, 0, 0], color=GREY_B, stroke_width=2)
    return VGroup(c, zero, a)


def box(tex, x, y, color=HEAD, w=0.6, h=0.42, size=20):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(
        [x, y, 0])
    return VGroup(r, MathTex(tex, font_size=size, color=color).move_to(r))


def phasor_chain(delta, T, length=4.0, color=HEAD):
    """The terms e^{2 pi i j delta}, j = 0..T-1, as arrows laid head to tail: their sum, divided by T, is the
    amplitude a_m."""
    step = length / T
    p = np.zeros(3)
    g = VGroup()
    for j in range(T):
        ang = 2 * PI * j * delta
        q = p + step * np.array([math.cos(ang), math.sin(ang), 0])
        g.add(Line(p, q, color=color, stroke_width=2.2))
        p = q
    total = Arrow(ORIGIN, p, buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.08)
    return g, total


class Phase(VoiceoverScene):
    def construct(self):
        self.card()
        self.eigen()
        self.powers()
        self.inverse()
        self.result()
        self.uses()

    def card(self):
        card = chapter_card(8, r"Phase estimation", r"How do we read an eigenvalue?", lit=(1995, 1998),
                            extra=((1995, r"Kitaev: \ phase estimation"),
                                   (1998, r"Cleve et al.: \ with the QFT")), part=PART)
        with self.voiceover("Chapter eight. Phase estimation. How do we read an eigenvalue?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ an eigenvalue is a phase
    def eigen(self):
        th = load("phase")["theta"]
        head = label(r"An eigenvalue is a phase", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"U|u\rangle", r"=", r"\lambda", r"|u\rangle", font_size=32),
            MathTex(r"\| U|u\rangle \|", r"=", r"\| |u\rangle \|", r"\;\Rightarrow\;", r"|\lambda| = 1", font_size=32),
            MathTex(r"\lambda", r"=", r"e^{2\pi i \theta},", r"\quad \theta \in [0, 1)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.75, 0])
        rows[2][2].set_color(HEAD)
        whys = VGroup(label(r"$|u\rangle$: \ an eigenvector of the unitary $U$", font_size=18, color=GREY_B),
                      label(r"unitaries keep lengths", font_size=18, color=GREY_B),
                      label(r"a point on the unit circle", font_size=18, color=GREY_B))
        for wl, r in zip(whys, rows):
            wl.next_to(r, LEFT, buff=0.35)
        kick = VGroup(
            MathTex(r"\tfrac{1}{\sqrt2}\big(|0\rangle|u\rangle + |1\rangle\,U|u\rangle\big)", font_size=30),
            MathTex(r"=", r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\theta}|1\rangle\big)", r"\otimes|u\rangle",
                    font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -1.0, 0])
        kick[1][1].set_color(HEAD)
        kl = wrapped_label(r"on $|u\rangle$ alone the phase is global, \ invisible \ (chapter 2); \ a controlled $U$ "
                           r"kicks it onto the control \ (chapter 5)", 5.6, font_size=19, color=WHITE).next_to(
            kick, UP, buff=0.3).align_to(kick, LEFT)
        # the circuit
        y1, y2 = 2.0, 1.1
        wires = VGroup(*[Line([-6.0, y, 0], [-3.0, y, 0], color=GREY_B, stroke_width=2) for y in (y1, y2)])
        kets = VGroup(MathTex(r"|{+}\rangle", font_size=28, color=GREY_A).next_to([-6.0, y1, 0], LEFT, buff=0.1),
                      MathTex(r"|u\rangle", font_size=28, color=GREY_A).next_to([-6.0, y2, 0], LEFT, buff=0.1))
        cu = VGroup(Line([-4.5, y1, 0], [-4.5, y2, 0], color=WHITE, stroke_width=2),
                    Dot([-4.5, y1, 0], radius=0.08), box(r"U", -4.5, y2, color=LAM, w=0.5, h=0.5, size=26))
        # the control qubit's equator, seen from above
        cc = np.array([-4.5, -1.5, 0])
        R = 1.25
        eqc = Circle(radius=R, color=GREY_C, stroke_width=1.8).move_to(cc)
        axes_ = VGroup(DashedLine(cc + LEFT * (R + 0.2), cc + RIGHT * (R + 0.2), color=GREY_D, dash_length=0.07),
                       DashedLine(cc + DOWN * (R + 0.2), cc + UP * (R + 0.2), color=GREY_D, dash_length=0.07))
        pts = VGroup(MathTex(r"|{+}\rangle", font_size=22, color=GREY_A).move_to(cc + RIGHT * (R + 0.5)),
                     MathTex(r"|{+}i\rangle", font_size=22, color=GREY_A).move_to(cc + UP * (R + 0.3)),
                     MathTex(r"|{-}\rangle", font_size=22, color=GREY_A).move_to(cc + LEFT * (R + 0.5)))
        arrow = Arrow(cc, cc + RIGHT * R, buff=0, color=HEAD, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        arc = Arc(radius=0.45, start_angle=0, angle=2 * PI * th, color=HEAD, stroke_width=2.5, arc_center=cc)
        al = MathTex(rf"2\pi\theta", font_size=22, color=HEAD).move_to(
            cc + 0.75 * np.array([math.cos(PI * th), math.sin(PI * th), 0]))
        el = label(rf"the control's equator, \ seen from above; \ here $\theta = {th}$", font_size=18,
                   color=GREY_B).next_to(eqc, DOWN, buff=0.3)
        with self.voiceover(
            "Every unitary has eigenvectors, states it only multiplies by a number. <bookmark mark='a'/> Because a "
            "unitary keeps lengths, that number has size one: it is a point on the unit circle, e to the two pi i "
            "theta. <bookmark mark='b'/> Applied to the eigenvector alone, "
            "the phase is global, and no measurement can see it. <bookmark mark='c'/> So control the unitary from a "
            "qubit in the plus state. The eigenvector comes out unchanged, and the phase is kicked back onto the "
            "control, as in chapter five. <bookmark mark='d'/> On the control's Bloch sphere, seen from above, its "
            "arrow turns about the vertical axis by two pi theta. Here theta is nought point three, a turn of a "
            "hundred and eight degrees. The question of this chapter is how to read that angle to many bits."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("b")
            self.play(FadeIn(kl))
            vo.wait_until("c")
            self.play(Create(wires), FadeIn(kets), FadeIn(cu))
            self.play(Write(kick[0]))
            self.play(TransformMatchingTex(kick[0].copy(), kick[1]))
            vo.wait_until("d")
            self.play(Create(eqc), FadeIn(axes_), FadeIn(pts), GrowArrow(arrow), FadeIn(el))
            self.play(Rotate(arrow, angle=2 * PI * th, about_point=cc), Create(arc), run_time=2)
            self.play(FadeIn(al))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ powers of U
    def powers(self):
        ph = load("phase")
        th, t = ph["theta"], ph["t"]
        head = label(r"Doubling the angle, \ one qubit per bit", font_size=36).to_edge(UP, buff=0.3)
        ys = [2.35 - 0.42 * q for q in range(t)]
        yu = ys[-1] - 0.62
        x0, x1 = -6.0, -0.75
        wires = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=1.8) for y in ys + [yu]])
        kets = VGroup(*[MathTex(r"|0\rangle", font_size=20, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.08)
                        for y in ys],
                      MathTex(r"|u\rangle", font_size=22, color=GREY_A).next_to([x0, yu, 0], LEFT, buff=0.08))
        hs = VGroup(*[box(r"H", -5.55, y, w=0.36, h=0.34, size=18) for y in ys])
        cus = VGroup()
        for i in range(t):
            q = t - 1 - i                       # the bottom counting qubit controls U^1, the top one U^(2^(t-1))
            x = -4.75 + 0.66 * i
            cus.add(VGroup(Line([x, ys[q], 0], [x, yu, 0], color=WHITE, stroke_width=1.6),
                           Dot([x, ys[q], 0], radius=0.06),
                           box(rf"U^{{{2 ** i}}}", x, yu, color=LAM, w=0.58, h=0.42, size=18)))
        cl = label(rf"$t = {t}$ counting qubits", font_size=18, color=GREY_B).next_to(wires, DOWN, buff=0.25)
        dials = VGroup()
        for i in range(t):
            f = (2 ** i * th) % 1
            d = dial(f)
            cap = MathTex(rf"U^{{{2 ** i}}}:\ {f:.1f}", font_size=22, color=HEAD)
            dials.add(VGroup(d, cap).arrange(DOWN, buff=0.12))
        dials.arrange_in_grid(rows=2, cols=3, buff=(0.75, 0.3)).move_to([3.7, 1.25, 0])
        dl = label(r"each control's turn: \ $2^k\theta$, \ whole turns dropped", font_size=18, color=GREY_B).next_to(
            dials, UP, buff=0.15)
        rows = VGroup(
            MathTex(r"\bigotimes_{k}", r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\, 2^k\theta}|1\rangle\big)", r"=",
                    r"\frac{1}{\sqrt T}\sum_{j=0}^{T-1} e^{2\pi i\, j\theta}\,|j\rangle", font_size=30),
        ).move_to([0, -1.75, 0])
        why = label(r"$T = 2^t$; \ the same product form as chapter 7's QFT: \ if $\theta = m/T$, \ this is "
                    r"$\mathrm{QFT}\,|m\rangle$", font_size=19, color=HEAD).next_to(rows, DOWN, buff=0.2)
        bin_ = label(r"$0.3 = 0.0100110011\ldots_2$: \ doubling shifts the binary point, \ so each qubit holds the "
                     r"bits from one place onward", font_size=19, color=GREY_A).next_to(why, DOWN, buff=0.2)
        with self.voiceover(
            "One qubit turned by theta gives at best a bit or two of theta. To get many bits, ask more qubits. "
            "<bookmark mark='a'/> Put t counting qubits in the plus state. The first controls U once, the next U "
            "twice, then four times, and so on, doubling. <bookmark mark='b'/> Each control picks up two to the k "
            "times theta, with whole turns dropped. For theta nought point three: three tenths, six tenths, two "
            "tenths, four, eight, and six again. <bookmark mark='c'/> Doubling shifts the binary point of theta, so "
            "each qubit holds theta's bits from one place onward. <bookmark mark='d'/> Multiply the qubits out, and "
            "the state is a sum over j of e to the two pi i j theta. That is exactly the product form of chapter "
            "seven. If theta is m over two to the t, the counting register holds the Fourier transform of m."
        ) as vo:
            self.play(FadeIn(head), Create(wires), FadeIn(kets))
            vo.wait_until("a")
            self.play(FadeIn(hs), FadeIn(cl))
            self.play(LaggedStart(*[FadeIn(c) for c in cus], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dl))
            for d, c in zip(dials, cus):
                self.play(FadeIn(d), Indicate(c, color=HEAD, scale_factor=1.1), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(bin_))
            vo.wait_until("d")
            self.play(Write(rows[0]))
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the inverse QFT
    def inverse(self):
        ph = load("phase")
        th, t = ph["theta"], ph["t"]
        T = 2 ** t
        P = ph["probs"]
        head = label(r"Reading the phase: \ the inverse QFT", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        rows = VGroup(
            MathTex(r"a_m", r"=", r"\frac{1}{T}\sum_{j=0}^{T-1} e^{2\pi i\, j(\theta - m/T)}", font_size=fs),
            MathTex(r"a_m", r"=", r"\frac{1}{T}\,\frac{1 - e^{2\pi i\, T\delta}}{1 - e^{2\pi i\,\delta}}",
                    r",\quad \delta = \theta - \tfrac{m}{T}", font_size=fs),
            MathTex(r"|a_m|^2", r"=", r"\frac{\sin^2(\pi T\delta)}{T^2 \sin^2(\pi\delta)}", font_size=fs),
            MathTex(r"|a_m|^2", r"\ge", r"\Big(\frac{\sin \pi T\delta}{\pi T\delta}\Big)^2", r"\ge",
                    r"\frac{4}{\pi^2}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        rows.move_to([0, 0.15, 0]).shift(RIGHT * (-6.4 - rows.get_left()[0]))
        rows[3][4].set_color(YES)
        whys = VGroup(label(r"the inverse QFT, \ row $m$", font_size=18, color=GREY_B),
                      label(r"a geometric series", font_size=18, color=GREY_B),
                      label(r"$|1 - e^{ix}| = 2|\sin\tfrac{x}{2}|$", font_size=18, color=GREY_B),
                      label(r"nearest $m$: \ $|T\delta| \le \tfrac12$", font_size=18, color=YES))
        for wl, r in zip(whys, rows):
            wl.next_to(r, DOWN, buff=0.06).align_to(r, LEFT).shift(RIGHT * 0.1)
        for i in range(1, 4):
            rows[i:].shift(DOWN * 0.3)
            whys[i:].shift(DOWN * 0.3)
        # the phasor chains
        m1 = round(th * T)
        m2 = m1 + 1
        g1, s1 = phasor_chain(th - m1 / T, T, length=4.2, color=YES)
        g2, s2 = phasor_chain(th - m2 / T, T, length=4.2, color=NO)
        c1 = VGroup(g1, s1).move_to([3.9, 1.35, 0])
        c2 = VGroup(g2, s2).move_to([3.9, -1.3, 0])
        l1 = label(rf"$m = {m1}$: \ the {T} terms nearly line up; \ $|a_m|^2 = {P[m1]:.3f}$", font_size=19,
                   color=YES).next_to(c1, DOWN, buff=0.2)
        l2 = label(rf"$m = {m2}$: \ they curl once round and mostly cancel; \ $|a_m|^2 = {P[m2]:.4f}$", font_size=19,
                   color=NO).next_to(c2, DOWN, buff=0.2)
        for lab_ in (l1, l2):
            if lab_.get_right()[0] > 6.85:
                lab_.shift(LEFT * (lab_.get_right()[0] - 6.85))
        cap = label(r"each term $e^{2\pi i j\delta}$ as an arrow, \ head to tail; \ their sum over $T$ is $a_m$",
                    font_size=18, color=GREY_B).next_to(c1, UP, buff=0.25)
        with self.voiceover(
            "Run the inverse Fourier transform on the counting register. <bookmark mark='a'/> The amplitude of "
            "outcome m is an average of T phases, each turning by theta minus m over T per step. "
            "<bookmark mark='b'/> Draw the terms as arrows, head to tail. For the m nearest to theta times T, they "
            "turn slowly and nearly line up, and the average is long. One outcome further on, they turn faster, curl "
            "once round, and mostly cancel. Interference again. <bookmark mark='c'/> The sum is a geometric series, and its size gives "
            "the probability of each outcome. <bookmark mark='d'/> For the nearest m, the leftover angle is at most "
            "half a step, and then the probability is at least four over pi squared, about forty per cent. In fact "
            "it is usually far more, and if theta is exactly m over T, it is one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap), Create(g1), run_time=2)
            self.play(GrowArrow(s1), FadeIn(l1))
            self.play(Create(g2), run_time=2.5)
            self.play(GrowArrow(s2), FadeIn(l2))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ our run
    def result(self):
        ph = load("phase")
        th, t, P = ph["theta"], ph["t"], ph["probs"]
        T = 2 ** t
        best = round(ph["best"] * T)
        head = label(rf"Our run: \ $\theta = {th}$, \ {t} counting qubits", font_size=36).to_edge(UP, buff=0.3)
        W, G, H = 0.13, 0.05, 3.4
        x0, y0 = -5.75, -1.55
        bars = VGroup()
        for m, p in enumerate(P):
            h = max(p * H, 0.004)
            bars.add(Rectangle(width=W, height=h, stroke_width=0, fill_color=YES if m == best else DATA,
                               fill_opacity=0.9).move_to([x0 + m * (W + G), y0, 0], aligned_edge=DOWN))
        base = Line([x0 - W, y0, 0], [x0 + (T - 1) * (W + G) + W, y0, 0], color=GREY_C, stroke_width=1.5)
        xs = [b.get_x() for b in bars]
        ticks = VGroup(*[label(f"{m}", font_size=16, color=GREY_A).move_to([xs[m], y0 - 0.25, 0])
                         for m in (0, 16, 32, 48, T - 1)])
        xl = label(r"measured $m$", font_size=18, color=GREY_B).next_to(ticks, DOWN, buff=0.12)
        xt = x0 + th * T * (W + G)
        mark = DashedLine([xt, y0, 0], [xt, y0 + H * 0.98 + 0.2, 0], color=HEAD, dash_length=0.06)
        ml = label(rf"$\theta T = {th * T:.1f}$", font_size=18, color=HEAD).next_to(mark, UP, buff=0.05).shift(
            LEFT * 0.6)
        vals = VGroup(
            label(f"{P[best]:.3f}", font_size=18, color=YES).next_to(bars[best], RIGHT, buff=0.15).shift(UP * 1.2),
            label(f"{P[best + 1]:.3f}", font_size=17, color=DATA).next_to(bars[best + 1], UP, buff=0.08).shift(
                RIGHT * 0.25),
            label(f"{P[best - 1]:.3f}", font_size=17, color=DATA).next_to(bars[best - 1], UP, buff=0.08).shift(
                LEFT * 0.25))
        read = VGroup(
            label(rf"measured \texttt{{{format(best, f'0{t}b')}}} $= {best}$", font_size=21, color=YES),
            label(rf"$\theta \approx {best}/{T} = {ph['best']}$", font_size=21, color=YES),
            label(rf"with probability {ph['p_best']:.3f}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        read.move_to([0, 1.95, 0]).shift(RIGHT * (1.9 - read.get_left()[0]))
        notes = VGroup(
            wrapped_label(rf"$0.3 \times {T} = {th * T:.1f}$ is not a whole number, \ so the peak leaks into its "
                          r"neighbours; \ the error of the nearest estimate is at most $1/2^{t+1}$", 4.8,
                          font_size=19, color=WHITE),
            wrapped_label(r"each extra counting qubit halves the error; \ a few more beyond the bits wanted make "
                          r"a wrong answer rare", 4.8, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(read, DOWN, buff=0.3).align_to(read, LEFT)
        with self.voiceover(
            "Here is our simulator's run: theta nought point three, six counting qubits. "
            "<bookmark mark='a'/> The distribution over the sixty-four outcomes. "
            "<bookmark mark='b'/> Theta times sixty-four is nineteen point two, between two outcomes, and the peak "
            "is at nineteen, measured with probability nought point eight seven five. <bookmark mark='c'/> In "
            "binary that reads nought point nought one nought nought one one, nineteen sixty-fourths, nought point "
            "two nine six eight seven five: theta to six bits. <bookmark mark='d'/> Because nineteen point two is not "
            "a whole number, some probability leaks to the neighbours, twenty and eighteen. Each extra counting "
            "qubit halves the error, and a few more qubits than the bits we want make a wrong answer rare."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ticks), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(ml))
            self.play(FadeIn(vals[0]), Indicate(bars[best], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(read))
            vo.wait_until("d")
            self.play(FadeIn(vals[1:]), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ uses, and the cost
    def uses(self):
        t = load("phase")["t"]
        head = label(r"Where phase estimation is used", font_size=36).to_edge(UP, buff=0.3)

        def tile(title, body, col, w=4.1, h=2.45):
            fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=1.8)
            tt = label(title, font_size=22, color=col)
            bb = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
            VGroup(tt, bb).arrange(DOWN, buff=0.18).move_to(fr)
            return VGroup(fr, tt, bb)
        tiles = VGroup(
            tile(r"factoring \ (chapter 9)", r"$U|y\rangle = |ay \bmod N\rangle$ has eigenvalues "
                 r"$e^{2\pi i s/r}$: \ estimate $s/r$, \ then recover the order $r$; \ the powers $U^{2^k}$ are "
                 r"cheap by repeated squaring \ (Part 30)", YES),
            tile(r"chemistry \ (chapter 13)", r"$U = e^{-iHt}$ for a molecule's Hamiltonian $H$: \ the phases "
                 r"give its energy levels, \ the numbers chemists want", DATA),
            tile(r"counting \ (chapter 10)", r"Grover's step is a rotation; \ estimating its angle counts the "
                 r"solutions \ (Brassard, \ H{\o}yer and Tapp, \ 1998)", LAM),
        ).arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.4)
        # the cost: 2^t - 1 applications of U
        unit = 0.17
        segs = VGroup()
        cols = [DATA, LAM, KERN, YES, HEAD, NO]
        for k in range(t):
            segs.add(Rectangle(width=unit * 2 ** k, height=0.4, stroke_color=BG, stroke_width=1.5,
                               fill_color=cols[k % len(cols)], fill_opacity=0.85))
        segs.arrange(RIGHT, buff=0).move_to([0, -1.25, 0])
        segl = VGroup(*[MathTex(rf"2^{{{k}}}", font_size=20, color=cols[k % len(cols)]).next_to(segs[k], UP,
                                                                                               buff=0.08)
                        for k in range(t) if 2 ** k * unit > 0.3])
        cost = label(rf"the controlled powers: \ $1 + 2 + \cdots + 2^{{t-1}} = 2^t - 1 = {2 ** t - 1}$ applications of "
                     rf"$U$ for $t = {t}$", font_size=20, color=WHITE).next_to(segs, DOWN, buff=0.2)
        foot = wrapped_label(r"each bit of precision doubles the work unless $U^{2^k}$ has a shortcut; \ Kitaev's "
                             r"original version \ (1995) \ used one control qubit at a time, \ estimating each "
                             r"doubled angle from repeated runs and combining them classically", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Phase estimation is the workhorse of quantum algorithms. <bookmark mark='a'/> Shor's algorithm in the "
            "next chapter is phase estimation of multiplication by a modulo N, whose eigenvalues reveal the order "
            "we need. <bookmark mark='b'/> In chemistry, the phases of a molecule's time evolution give its energy "
            "levels. <bookmark mark='c'/> Applied to Grover's rotation, it counts solutions. <bookmark mark='d'/> But "
            "precision is not free. The controlled powers apply U one, two, four, and up to thirty-two times: "
            "sixty-three applications for six bits, and each further bit doubles the work, unless the powers have a "
            "shortcut, as modular exponentiation does by repeated squaring. <bookmark mark='e'/> Alexei Kitaev's "
            "original version of 1995 used one control qubit at a time, estimating each doubled angle from repeated "
            "runs and combining the answers classically."
        ) as vo:
            self.play(FadeIn(head))
            for mk, tl in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(tl, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.5), FadeIn(segl), run_time=2.5)
            self.play(FadeIn(cost))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG, DATA, HEAD, mono, cm)
