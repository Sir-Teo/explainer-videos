from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes, square_axes


def wavelength_color(nm: float) -> ManimColor:
    """A rough visible-spectrum color for a wavelength in nanometres."""
    if nm < 440:
        r, g, b = (440 - nm) / 60, 0.0, 1.0
    elif nm < 490:
        r, g, b = 0.0, (nm - 440) / 50, 1.0
    elif nm < 510:
        r, g, b = 0.0, 1.0, (510 - nm) / 20
    elif nm < 580:
        r, g, b = (nm - 510) / 70, 1.0, 0.0
    elif nm < 645:
        r, g, b = 1.0, (645 - nm) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    return ManimColor((max(r, 0.25), max(g, 0.1), max(b, 0.1)))


GLOW_MAX = 12  # the glow saturates where the resolvent's norm reaches 10^12


def pseudo_image(Z, width, height):
    """log10 of the smallest singular value, from -GLOW_MAX (an eigenvalue in all but name) to 0, as a green glow."""
    v = np.clip(-Z / GLOW_MAX, 0, 1)[::-1]  # row 0 of the image is the top
    bg = np.array(ManimColor(BACKGROUND).to_rgb())
    col = np.array(ManimColor(C.SPECTRUM).to_rgb())
    rgb = bg + v[..., None] ** 0.7 * (col - bg)
    img = ImageMobject((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height)
    return img


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.two_spectra()
        self.shift()
        self.sections()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=9, highlight=10).scale(0.9)
        with self.voiceover(
            "Nine rows of the ledger are filled. The last part is about operators, <bookmark mark='l'/> and what it "
            "means to diagonalize one."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[9], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def two_spectra(self):
        R = 10967758.34  # the Rydberg constant for hydrogen, per metre
        ns = np.arange(3, 8)
        lam = 1e9 / (R * (1 / 4 - 1 / ns**2))
        assert abs(lam[0] - 656.47) < 0.05 and abs(lam[1] - 486.27) < 0.05
        strip = Rectangle(width=11.0, height=0.9, stroke_color=GREY_C, stroke_width=1.5, fill_color=BLACK,
                          fill_opacity=1).move_to([0, 1.7, 0])

        def X(nm):
            return -5.5 + 11.0 * (nm - 380) / (700 - 380)

        lines = VGroup(*[Line([X(l_), 1.25, 0], [X(l_), 2.15, 0], color=wavelength_color(l_), stroke_width=6)
                         for l_ in lam])
        labs = VGroup(*[MathTex(f"{l_:.1f}", font_size=20, color=GREY_A).next_to(ln, DOWN, buff=0.08)
                        for l_, ln in zip(lam, lines)])
        for k in range(1, len(labs)):  # lines closer than their labels: drop every other label a row lower
            a_, b_ = labs[k], labs[k - 1]
            close = min(a_.get_right()[0], b_.get_right()[0]) - max(a_.get_left()[0], b_.get_left()[0]) > -0.08
            if close and abs(a_.get_y() - b_.get_y()) < 0.1:
                a_.shift(DOWN * 0.28)
        sl = label(r"hydrogen's visible lines (nm): \ $\frac{1}{\lambda} = R\big(\frac14 - \frac{1}{n^2}\big)$, \ "
                   r"$n = 3, \ldots, 7$", font_size=24, color=GREY_A).next_to(strip, UP, buff=0.15)
        # energy levels: E_n = -13.6 eV / n^2 (n = 2 up, on a true scale; n = 1 is far below), and each visible line is
        # the jump from level n down to level 2
        E = lambda n_: -13.6 / n_**2  # noqa: E731
        ax = plain_axes([0, 1, 1], [-3.6, 0.2, 1], 2.2, 3.1, numbers=True, font_size=18,
                        x_axis_config={"include_numbers": False, "include_ticks": False},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}, "numbers_to_exclude": []})
        ax.move_to([-4.85, -1.65, 0])
        lev = VGroup(*[Line(ax.c2p(0.04, E(n_)), ax.c2p(1, E(n_)), color=C.SPECTRUM, stroke_width=3 if n_ <= 7 else 1.5)
                       for n_ in range(2, 21)])
        # each line's photon energy is E_n - E_2, and h c / (E_n - E_2) is its wavelength
        hc = 1239.84198  # eV nm
        assert np.allclose(hc / (E(ns) - E(2)), lam, rtol=2e-3)
        ys, last = {}, -1e9
        for n_ in range(2, 8):  # level labels, pushed up where the levels crowd, with a leader line when moved
            y_ = max(ax.c2p(1, E(n_))[1], last + 0.24)
            ys[n_], last = y_, y_
        lev_labs, leaders = VGroup(), VGroup()
        for n_ in range(2, 8):
            t_ = MathTex(rf"n = {n_}", font_size=22, color=C.SPECTRUM).move_to([ax.c2p(1, 0)[0] + 0.62, ys[n_], 0])
            lev_labs.add(t_)
            p0 = ax.c2p(1, E(n_)) + RIGHT * 0.04
            leaders.add(Line(p0, [t_.get_left()[0] - 0.05, ys[n_], 0], color=GREY_B, stroke_width=1))
        assert ys[7] < ax.get_top()[1] + 0.3
        lev_l = MathTex(r"E_n = -\tfrac{13.6\ \mathrm{eV}}{n^2}", font_size=24, color=C.SPECTRUM).next_to(ax, UP, buff=0.12)
        gnd = label(r"$n = 1$: \ $-13.6$ eV, \ off the scale below", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        jumps = VGroup(*[Arrow(ax.c2p(0.25 + 0.13 * i, E(n_)), ax.c2p(0.25 + 0.13 * i, E(2)), buff=0,
                               color=wavelength_color(l_), stroke_width=3, tip_length=0.12,
                               max_tip_length_to_length_ratio=0.5)
                         for i, (n_, l_) in enumerate(zip(ns, lam))])
        rows = VGroup(
            MathTex(r"\sigma(T) = \{\lambda \in \mathbb C : T - \lambda I \text{ has no bounded inverse}\}", font_size=30,
                    color=C.SPECTRUM),
            VGroup(label(r"the energies are the spectrum of the Hamiltonian $H$;", font_size=24),
                   label(r"the lines are their differences", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"the quantum videos assumed $H$ can be diagonalized;", font_size=24, color=C.EPS),
                   label(r"this part proves it", font_size=24, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to([-1.5, -1.6, 0], RIGHT, buff=0)
        assert rows.get_right()[0] <= 6.6 and rows.get_left()[0] > lev_labs.get_right()[0] + 0.4
        assert lev_l.get_top()[1] < labs.get_bottom()[1] - 0.1 and gnd.get_bottom()[1] > -3.6
        head = label(r"Two meanings of ``spectrum''", font_size=36).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Spectrum is the word for the lines of light a hot gas gives off. Hydrogen's visible "
            "lines sit at these wavelengths, computed from Rydberg's formula. <bookmark mark='b'/> And spectrum is the "
            "word for the set of complex numbers lambda where T minus lambda has no inverse. "
            "<bookmark mark='c'/> It's the same word for a reason: the energy levels of the atom are the spectrum of "
            "an operator, the Hamiltonian, and each line is a jump between two levels. <bookmark mark='d'/> The "
            "quantum videos assumed that such operators can be diagonalized. This part proves it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(strip), FadeIn(sl))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(labs), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(ax), LaggedStart(*[Create(l_) for l_ in lev], lag_ratio=0.05), FadeIn(lev_l),
                      FadeIn(lev_labs), FadeIn(leaders), FadeIn(gnd), FadeIn(rows[1]))
            self.play(LaggedStart(*[GrowArrow(j) for j in jumps], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shift(self):
        d = load("shift")
        lam, res, smin = d["lam"], d["res"], d["smin"]
        # the forward shift on coefficient boxes
        vals = [r"x_0", r"x_1", r"x_2", r"x_3", r"x_4", r"x_5"]  # every box filled: the sequence goes on past the window
        boxes = VGroup(*[Square(0.62, color=GREY_B, stroke_width=2) for _ in range(6)]).arrange(RIGHT, buff=0.06)
        boxes.move_to([-3.4, 1.7, 0])
        step = boxes[1].get_x() - boxes[0].get_x()
        ents = VGroup(*[MathTex(v, font_size=26, color=C.FUNC).move_to(boxes[i]) for i, v in enumerate(vals)])
        dots_ = MathTex(r"\cdots", font_size=30).next_to(boxes, RIGHT, buff=0.1)
        sl = MathTex(r"S(x_0, x_1, \ldots) = (0, x_0, x_1, \ldots)", font_size=28, color=C.OPERATOR).next_to(boxes, UP,
                                                                                                     buff=0.2)
        zero = MathTex(r"0", font_size=26, color=GREY_B).move_to(boxes[0])
        noeig = VGroup(
            MathTex(r"Sx = \lambda x: \ \ 0 = \lambda x_0, \ \ x_0 = \lambda x_1, \ \ldots \ \Rightarrow \ x = 0",
                    font_size=26),
            label(r"no eigenvalues at all", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, buff=0.12).next_to(boxes, DOWN, buff=0.4)
        cx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.45).move_to([3.6, -0.3, 0])
        disc = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=C.SPECTRUM, stroke_width=3,
                      fill_color=C.SPECTRUM, fill_opacity=0.15).move_to(cx.c2p(0, 0))
        dots = VGroup(*[Dot(cx.c2p(l_.real, l_.imag), radius=0.03, color=C.SPECTRUM) for l_ in lam])
        cl = MathTex(r"\lambda \in \mathbb C", font_size=22, color=GREY_B).next_to(cx, UP, buff=0.05).align_to(cx, LEFT)
        back = VGroup(
            MathTex(r"S^*(x_0, x_1, \ldots) = (x_1, x_2, \ldots)", font_size=26, color=C.OPERATOR),
            MathTex(r"S^*(1, \lambda, \lambda^2, \ldots) = \lambda\,(1, \lambda, \lambda^2, \ldots)", font_size=26),
            MathTex(rf"\text{{200 random }} |\lambda| < 0.95: \ \text{{residual}} \le {sci(res.max(), 0)}", font_size=22,
                    color=GREY_A),
            label(r"so $\sigma(S^*)$, \ and $\sigma(S)$, \ are the closed unit disc", font_size=26, color=C.SPECTRUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-3.2, -2.0, 0])
        assert res.max() < 1e-12 and np.all(smin >= 1 - np.abs(lam[:20]) - 1e-12)
        head = label(r"The shift: \ no eigenvalues, \ a whole disc of spectrum", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the first surprise. The shift on square-summable sequences moves every "
            "entry one slot to the right. <bookmark mark='b'/> It has no eigenvalues: S x equal to lambda x forces "
            "the first entry to vanish, then the next, then all of them. <bookmark mark='c'/> Its adjoint, the "
            "backward shift, drops the first entry, and for every lambda inside the unit disc the geometric "
            "sequence one, lambda, lambda squared is an eigenvector. Two hundred of them, checked. "
            "<bookmark mark='d'/> So the spectrum of the shift is the whole closed disc, though it has not a single "
            "eigenvalue."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(boxes), FadeIn(ents), FadeIn(dots_), FadeIn(sl))
            self.play(ents[:5].animate.shift(RIGHT * step), FadeOut(ents[5], shift=RIGHT * step), FadeIn(zero),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(noeig))
            vo.wait_until("c")
            self.play(FadeIn(back[:2]), Create(cx), FadeIn(cl))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.3) for d_ in dots], lag_ratio=0.01), FadeIn(back[2]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(DrawBorderThenFill(disc), FadeIn(back[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sections(self):
        d = load("shift")
        g = d["g"]
        levels = (2, 6)  # contours where the resolvent's norm is 10^2 and 10^6
        imgs, axs, labs, conts = Group(), VGroup(), VGroup(), VGroup()
        for k, (key, n) in enumerate((("p8", 8), ("p24", 24), ("p64", 64))):
            ax = square_axes([-1.5, 1.5, 1], [-1.5, 1.5, 1], 1.25).move_to([-4.4 + 4.4 * k, 0.2, 0])
            Z = d[key]
            img = pseudo_image(Z, ax.c2p(1.5, 0)[0] - ax.c2p(-1.5, 0)[0], ax.c2p(0, 1.5)[1] - ax.c2p(0, -1.5)[1])
            img.move_to(ax.c2p(0, 0))
            circ = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=WHITE, stroke_width=1.5).move_to(ax.c2p(0, 0))
            c_ = VGroup(circ)
            for lev, op in ((-levels[0], 0.9), (-levels[1], 0.6)):  # Z = log10 smallest singular value = -level
                c_.add(contour_mobject(ax, contour_segments(lambda X, Y, Z=Z: Z, g, g, level=lev), C.EPS, 2.0, op))
            e0 = Dot(ax.c2p(0, 0), radius=0.06, color=C.PATHOLOGY)
            imgs.add(img)
            axs.add(ax)
            conts.add(VGroup(c_, e0))
            labs.add(MathTex(rf"N = {n}", font_size=28).next_to(ax, UP, buff=0.1))
        # where the 10^-6 contour sits on the real axis: it moves out toward 1 as N grows
        radii = []
        for key in ("p8", "p24", "p64"):
            row = d[key][60]
            i = np.argmax((g > 0) & (row > -6))
            radii.append(float(g[i]))
        assert radii[0] < radii[1] < radii[2] < 1
        rows = VGroup(
            label(r"$N \times N$ sections of the shift: \ a Jordan block, \ the only eigenvalue is $0$ (red)", font_size=24),
            MathTex(rf"\text{{glow: }} \log_{{10}}\|(J_N - \lambda)^{{-1}}\| \text{{ from 0 to {GLOW_MAX}}}; \ \ "
                    rf"\text{{contours: }} \|(J_N - \lambda)^{{-1}}\| = 10^{{{levels[0]}}}, 10^{{{levels[1]}}}; \ \ "
                    r"\text{white: } |\lambda| = 1", font_size=24, color=GREY_A),
            label(r"the resolvent is astronomically large across the disc: \ the spectrum of the infinite shift shows "
                  r"through", font_size=24, color=C.SPECTRUM),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        assert max(r_.width for r_ in rows) <= 13.0
        head = label(r"Finite sections hide the spectrum, \ and the resolvent shows it", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A computer can only hold a finite piece of the shift: an N by N block whose only "
            "eigenvalue is zero. <bookmark mark='b'/> But measure how close T minus lambda is to failing to be "
            "invertible: the glow is the size of the inverse. Inside the disc it's astronomically large, like one over "
            "lambda to the N, and the contours spread outward as N grows. <bookmark mark='c'/> The eigenvalues "
            "lie, but the resolvent tells the truth. That's why the spectrum is defined by invertibility, not by "
            "eigenvectors."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]))
            for k in range(3):
                self.play(FadeIn(imgs[k]), Create(axs[k]), FadeIn(labs[k]), FadeIn(conts[k][1]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[Create(c_[0]) for c_ in conts], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Banach algebras", r"The spectrum", r"Functions of an operator", r"Gelfand theory",
            r"Operators on Hilbert space", r"Compact self-adjoint operators", r"A spectrum with no eigenvectors",
            r"The spectral theorem", r"Unbounded operators", r"The Cayley transform", r"Stone's theorem",
            r"What this proves about quantum mechanics",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=28) for i, t in enumerate(chapters)])
        colL = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-3.2, -0.5, 0])
        colR = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.0, -0.5, 0]).align_to(colL, UP)
        head = label(r"Part 10: \ Banach algebras and the spectral theorem", font_size=40).to_edge(UP, buff=0.4)
        sub = label(r"Rudin, \textit{Functional Analysis}, chapters 10--13, \ and \textit{Real and Complex Analysis}, "
                    r"chapter 18", font_size=24, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters ten to thirteen of Functional Analysis. <bookmark mark='a'/> First "
            "the algebra: Banach algebras, the spectrum, functions of an operator, and Gelfand's theory. "
            "<bookmark mark='b'/> Then Hilbert space, where the spectral theorem diagonalizes compact operators, "
            "then operators with no eigenvectors at all, then every normal operator. <bookmark mark='c'/> Then the "
            "unbounded operators of physics, and what all of it proves about quantum mechanics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 8)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(8, 12)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
