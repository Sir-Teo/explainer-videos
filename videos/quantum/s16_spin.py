from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (BlochSphere, Projector, Raster, bloch_vector, boxed, complex_plane, glow, label, load,
                                   mtex, note, num, part_card, phasor, place_whys, polyline, splat, stack, why)


def sg_magnet(center, scale=1.0) -> VGroup:
    """A schematic Stern-Gerlach magnet seen end-on: a pointed north pole above a notched south pole."""
    c = np.array(center, dtype=float)
    n = Polygon(c + scale * np.array([-0.7, 1.2, 0]), c + scale * np.array([0.7, 1.2, 0]), c + scale * np.array([0.7, 0.55, 0]),
                c + scale * np.array([0.0, 0.25, 0]), c + scale * np.array([-0.7, 0.55, 0]), stroke_width=2,
                stroke_color=GREY_B, fill_color="#B5504A", fill_opacity=0.8)
    s = Polygon(c + scale * np.array([-0.7, -1.2, 0]), c + scale * np.array([0.7, -1.2, 0]), c + scale * np.array([0.7, -0.45, 0]),
                c + scale * np.array([0.25, -0.45, 0]), c + scale * np.array([0.25, -0.7, 0]), c + scale * np.array([-0.25, -0.7, 0]),
                c + scale * np.array([-0.25, -0.45, 0]), c + scale * np.array([-0.7, -0.45, 0]), stroke_width=2,
                stroke_color=GREY_B, fill_color="#4A6BB5", fill_opacity=0.8)
    return VGroup(n, s, MathTex("N", font_size=26).move_to(c + scale * np.array([0, 0.9, 0])),
                  MathTex("S", font_size=26).move_to(c + scale * np.array([0, -0.98, 0])))


class Spin(VoiceoverScene):
    def construct(self):
        self.card()
        self.stern_gerlach()
        self.qubit()
        self.operators()
        self.sequential()
        self.precession()

    def card(self):
        c = part_card(5, r"Spin and entanglement", r"the simplest quantum system, and the strangest")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def stern_gerlach(self):
        s = load("spin")
        beam, cl, qu = s["beam"], s["classical"], s["quantum"]
        oven = Rectangle(width=0.9, height=0.7, stroke_color=GREY_B, fill_color=GREY_D, fill_opacity=1).move_to(LEFT * 6.0 + UP * 1.4)
        ol = label(r"silver atoms", font_size=22, color=GREY_B).next_to(oven, DOWN, buff=0.1)
        mag = sg_magnet(LEFT * 2.6 + UP * 1.4, scale=0.75)
        ml = label(r"non-uniform\\magnetic field", font_size=22, color=GREY_B).next_to(mag, DOWN, buff=0.1)
        bm = Line(oven.get_right(), LEFT * 3.2 + UP * 1.4, color=GREY_A, stroke_width=3)
        up_b = Line(LEFT * 2.0 + UP * 1.4, RIGHT * 0.6 + UP * 2.2, color=C.SPIN_UP, stroke_width=3)
        dn_b = Line(LEFT * 2.0 + UP * 1.4, RIGHT * 0.6 + UP * 0.6, color=C.SPIN_DOWN, stroke_width=3)
        scr = Rectangle(width=0.12, height=2.6, stroke_width=0, fill_color=GREY_C, fill_opacity=1).move_to(RIGHT * 0.7 + UP * 1.4)
        sl = label(r"screen", font_size=22, color=GREY_B).next_to(scr, DOWN, buff=0.1)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        hist = label(r"Otto Stern \& Walther Gerlach, Frankfurt, February 1922", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        # screens seen face-on: classical expectation vs what was seen
        W, H = 2.6, 2.6
        ext = (-1.6, 1.6, -1.6, 1.6)
        def screen_img(defl):
            y = defl * 1.0 + beam[:, 0]
            x = beam[:, 1] * 2.8
            return glow(splat(x, y, ext, (220, 220), sigma=2.2) * 0.12, C.BORN, gain=1.4)
        cimg = ImageMobject(screen_img(cl)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        qimg = ImageMobject(screen_img(qu)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        for im in (cimg, qimg):
            im.width, im.height = W, H
        cimg.move_to(LEFT * 3.2 + DOWN * 2.15)
        qimg.move_to(RIGHT * 2.0 + DOWN * 2.15)
        frames = VGroup(*[Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=1.5).move_to(m.get_center()) for m in (cimg, qimg)])
        cl_l = label(r"classical expectation:\\a smear", font_size=24, color=C.CLASSICAL).next_to(frames[0], LEFT, buff=0.25)
        qu_l = label(r"observed:\\two spots", font_size=24, color=C.BORN).next_to(frames[1], RIGHT, buff=0.25)
        mc = note(r"Monte Carlo, 6{,}000 atoms").to_corner(DR, buff=0.3)
        with self.voiceover(
            "In February 1922, in Frankfurt, Otto Stern and Walther Gerlach sent a beam of silver atoms through a "
            "deliberately uneven magnetic field. <bookmark mark='m'/> Each atom is a tiny magnet, and the uneven field "
            "pushes it up or down depending on which way its magnet points. <bookmark mark='c'/> Classically, the magnets "
            "point every which way, so you'd expect a continuous smear on the screen. <bookmark mark='q'/> What they saw "
            "was two separate spots. Every atom was deflected either fully up or fully down, never in between."
        ) as vo:
            self.play(FadeIn(hist), FadeIn(oven), FadeIn(ol), FadeIn(mag), FadeIn(ml), FadeIn(scr), FadeIn(sl), FadeIn(tag))
            vo.wait_until("m")
            self.play(Create(bm), Create(up_b), Create(dn_b))
            vo.wait_until("c")
            self.play(FadeIn(cimg), Create(frames[0]), FadeIn(cl_l))
            vo.wait_until("q")
            self.play(FadeIn(qimg), Create(frames[1]), FadeIn(qu_l), FadeIn(mc))
        with self.voiceover(
            "The explanation came a few years later: the electron carries an intrinsic angular momentum, its spin, "
            "whose component along any axis you measure is only ever plus or minus h-bar over two. It's not a little "
            "spinning ball; it's a quantum system with exactly two outcomes, and the simplest one there is."
        ):
            pass
        self.clear_scene()

    # ------------------------------------------------------------------
    def qubit(self):
        q1 = MathTex(r"\ket{\psi}", r"=", r"\alpha\ket{\uparrow} + \beta\ket{\downarrow}", r",\qquad", r"|\alpha|^2 + |\beta|^2 = 1",
                     font_size=38)
        q2 = MathTex(r"\ket{\psi}", r"=", r"\cos\tfrac{\theta}{2}\ket{\uparrow} + e^{i\varphi}\sin\tfrac{\theta}{2}\ket{\downarrow}",
                     font_size=42)
        col = VGroup(q1, q2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        n1 = note(r"two complex numbers, length one, and an overall phase that doesn't matter: two angles are left").next_to(
            q1, DOWN, buff=0.08, aligned_edge=LEFT)
        q2.next_to(n1, DOWN, buff=0.35, aligned_edge=LEFT)
        proj = Projector(az=-0.5, el=0.25, scale=1.0, center=RIGHT * 3.3 + DOWN * 0.7)
        bs = BlochSphere(proj, radius=2.2)
        th, ph = ValueTracker(PI / 3), ValueTracker(0.6)
        arr = always_redraw(lambda: bs.arrow(bloch_vector(th.get_value(), ph.get_value())))
        ang = always_redraw(lambda: VGroup(
            MathTex(r"\theta = " + f"{np.degrees(th.get_value()):.0f}" + r"^\circ", font_size=30),
            MathTex(r"\varphi = " + f"{np.degrees(ph.get_value()):.0f}" + r"^\circ", font_size=30)).arrange(DOWN, aligned_edge=LEFT)
            .to_corner(DL, buff=0.6))
        anti = label(r"perpendicular states ($\ket{\uparrow}$, $\ket{\downarrow}$)\\are \emph{opposite} points: hence $\theta/2$",
                     font_size=26, color=C.BLOCH).to_corner(DL, buff=0.5).shift(UP * 1.4)
        with self.voiceover(
            "A spin state is a vector in a two-dimensional complex space: alpha times up plus beta times down, with "
            "the squared lengths adding to one. <bookmark mark='p'/> Two complex numbers is four real numbers; the "
            "length condition removes one, and the overall phase, which doesn't matter, removes another. Two angles "
            "remain, <bookmark mark='b'/> and every state can be written as cosine theta over two times up, plus e to "
            "the i phi sine theta over two times down."
        ) as vo:
            self.play(Write(q1))
            vo.wait_until("p")
            self.play(FadeIn(n1))
            vo.wait_until("b")
            self.play(Write(q2))
        with self.voiceover(
            "Two angles are a point on a sphere: the Bloch sphere. <bookmark mark='u'/> Up is the north pole, down the "
            "south pole, and their equal superpositions lie around the equator. <bookmark mark='a'/> Notice the half "
            "angles. Up and down are perpendicular vectors in the state space, but they sit at opposite poles: the "
            "sphere doubles every angle."
        ) as vo:
            self.play(FadeIn(bs))
            self.add(arr, ang)
            vo.wait_until("u")
            self.play(th.animate.set_value(0.02), run_time=1.5)
            self.play(th.animate.set_value(PI - 0.02), run_time=2.0)
            self.play(th.animate.set_value(PI / 2), ph.animate.set_value(TAU + 0.6), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(anti))
        for m in (arr, ang):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def operators(self):
        S = MathTex(r"\hat{\mathbf S} = \frac{\hbar}{2}\,\boldsymbol\sigma", font_size=40).to_edge(UP, buff=0.45)
        pm = VGroup(
            MathTex(r"\sigma_x = \begin{pmatrix} 0 & 1\\ 1 & 0\end{pmatrix}", font_size=36),
            MathTex(r"\sigma_y = \begin{pmatrix} 0 & -i\\ i & 0\end{pmatrix}", font_size=36),
            MathTex(r"\sigma_z = \begin{pmatrix} 1 & 0\\ 0 & -1\end{pmatrix}", font_size=36),
        ).arrange(RIGHT, buff=0.8).next_to(S, DOWN, buff=0.45)
        pl = label(r"the Pauli matrices (1927)", font_size=26, color=GREY_A).next_to(pm, DOWN, buff=0.2)
        ev = MathTex(r"\sigma_x:\quad \ket{\pm x} = \frac{\ket{\uparrow} \pm \ket{\downarrow}}{\sqrt 2}", font_size=36).next_to(pl, DOWN, buff=0.4)
        cm = MathTex(r"[\hat S_x, \hat S_y] = i\hbar\,\hat S_z", font_size=44, color=C.HBAR).next_to(ev, DOWN, buff=0.45)
        un = label(r"so no state has a definite value of two different components", font_size=28).next_to(cm, DOWN, buff=0.25)
        with self.voiceover(
            "The spin observables are two-by-two matrices: h-bar over two times the Pauli matrices. <bookmark mark='e'/> "
            "The eigenvectors of sigma z are up and down; the eigenvectors of sigma x are their sum and difference, on "
            "the sphere's equator. <bookmark mark='c'/> And the components don't commute: S x S y minus S y S x is i "
            "h-bar S z. <bookmark mark='u'/> So, by the uncertainty relation we derived, no state has definite values "
            "of two different components. Knowing spin up along z means knowing nothing about x."
        ) as vo:
            self.play(Write(S), FadeIn(pm), FadeIn(pl))
            vo.wait_until("e")
            self.play(Write(ev))
            vo.wait_until("c")
            self.play(Write(cm))
            vo.wait_until("u")
            self.play(FadeIn(un))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sequential(self):
        s = load("spin")
        th, ups, m = s["thetas"], s["ups"], int(s["m"][0])
        zxz = int(s["zxz"][0])
        assert m == 1000 and abs(zxz - 487) == 0
        d1 = MathTex(r"P(\uparrow_{\mathbf n})", r"=", r"\big|\braket{\uparrow_{\mathbf n}}{\uparrow}\big|^2", r"=", r"\cos^2\frac{\theta}{2}",
                     font_size=40).to_corner(UL, buff=0.5)
        d1[4].set_color(C.BORN)
        ax = Axes(x_range=[0, 180, 45], y_range=[0, 1.05, 0.5], x_length=6.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 2.6 + DOWN * 0.8)
        curve = ax.plot(lambda d: np.cos(np.radians(d) / 2) ** 2, x_range=[0, 180], color=C.BORN, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(np.degrees(t), u / m), radius=0.07, color=WHITE) for t, u in zip(th, ups)])
        xl = MathTex(r"\theta", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        ticks = VGroup(*[MathTex(s_, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                         for v, s_ in ((0, r"0^\circ"), (90, r"90^\circ"), (180, r"180^\circ"))])
        dn = note(r"dots: 1{,}000 simulated atoms per angle").next_to(ax, DOWN, buff=0.45)
        # z -> x -> z
        seq = VGroup()
        xs_ = [1.4, 3.6, 5.8]
        for i, (x0, axis) in enumerate(zip(xs_, ("z", "x", "z"))):
            box = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.1, stroke_color=GREY_B).move_to([x0, 1.6, 0])
            seq.add(VGroup(box, MathTex(rf"\text{{SG}}_{axis}", font_size=26).move_to(box)))
        arrows = VGroup(*[Arrow([xs_[i] + 0.6, 1.75, 0], [xs_[i + 1] - 0.6, 1.75, 0], buff=0.05, color=C.SPIN_UP, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for i in range(2)])
        blocks = VGroup(*[Line([xs_[i] + 0.65, 1.25, 0], [xs_[i] + 0.95, 1.25, 0], color=GREY_C, stroke_width=6) for i in range(2)])
        al = VGroup(MathTex(r"\uparrow_z", font_size=24, color=C.SPIN_UP).next_to(arrows[0], UP, buff=0.05),
                    MathTex(r"\uparrow_x", font_size=24, color=C.SPIN_UP).next_to(arrows[1], UP, buff=0.05))
        res = MathTex(r"\uparrow_z:\ " + str(zxz), r",\quad", r"\downarrow_z:\ " + str(1000 - zxz), font_size=30).next_to(seq[2], DOWN, buff=0.45)
        rn = label(r"measuring $x$ erased what we knew about $z$", font_size=26, color=GREY_A).next_to(res, DOWN, buff=0.2)
        if rn.get_right()[0] > 7.0:
            rn.shift(LEFT * (rn.get_right()[0] - 7.0))
        sch = note(r"schematic: the other beam is blocked after each magnet").next_to(seq, UP, buff=0.2)
        with self.voiceover(
            "Now chain measurements. Prepare atoms with spin up along z, then measure along a direction n tilted by an "
            "angle theta. <bookmark mark='p'/> The Born rule says the probability of up along n is the squared overlap, "
            "<bookmark mark='c'/> and with the half angles from the sphere, that's cosine squared of theta over two. "
            "<bookmark mark='d'/> A thousand simulated atoms at each angle land right on the curve: always up at zero "
            "degrees, fifty-fifty at ninety, never at one eighty."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(d1[:3]))
            vo.wait_until("c")
            self.play(Write(d1[3:]), Create(ax), FadeIn(xl), FadeIn(ticks), Create(curve))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08), FadeIn(dn))
        with self.voiceover(
            "Here's the strangest version. <bookmark mark='a'/> Select spin up along z. Then measure along x, and keep "
            "only the atoms that came out up along x. <bookmark mark='b'/> Now measure z again. Before, every one of "
            "these atoms was up along z. Now it's fifty-fifty: 487 up, 513 down. The x measurement didn't just reveal "
            "something; it replaced the state, and the z information is gone."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(seq[:2]), GrowArrow(arrows[0]), FadeIn(al[0]), FadeIn(blocks), FadeIn(sch))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(al[1]), FadeIn(seq[2]))
            self.play(FadeIn(res), FadeIn(rn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def precession(self):
        gam = float(load("numbers")["gamma_e"][0])
        assert abs(gam - 28.0) < 0.05
        h1 = MathTex(r"\hat H = \omega\,\hat S_z", r"\;\Rightarrow\;", r"\varphi(t) = \varphi_0 + \omega t", r",\quad", r"\omega = -\gamma B",
                     font_size=34).to_edge(UP, buff=0.4)
        h1[2].set_color(C.QTIME)
        hn = label(rf"Larmor precession: for an electron, $|\omega|/2\pi = {gam:.1f}$ GHz per tesla", font_size=26, color=GREY_A)
        hn.next_to(h1, DOWN, buff=0.15)
        proj = Projector(az=-0.5, el=0.3, scale=1.0, center=LEFT * 3.2 + DOWN * 0.6)
        bs = BlochSphere(proj, radius=2.0)
        wt = ValueTracker(0.0)
        th0, ph0 = PI / 3, 0.0
        arr = always_redraw(lambda: bs.arrow(bloch_vector(th0, ph0 + wt.get_value())))
        trail = always_redraw(lambda: VMobject(stroke_color=C.BLOCH, stroke_width=2, stroke_opacity=0.6).set_points_as_corners(
            bs.bloch_to_screen(np.array([bloch_vector(th0, ph0 + w) for w in np.linspace(0, max(wt.get_value(), 1e-3), 80)]))))
        # the spinor's two components as phasors: alpha e^{-i w t / 2}, beta e^{+i w t / 2}
        a0, b0 = np.cos(th0 / 2), np.sin(th0 / 2)
        cpos = [RIGHT * 2.1 + DOWN * 0.6, RIGHT * 5.0 + DOWN * 0.6]
        planes = VGroup(*[complex_plane(radius=1.15, font_size=20).move_to(c) for c in cpos])
        ph = always_redraw(lambda: VGroup(
            phasor(a0 * np.exp(-0.5j * wt.get_value()), origin=cpos[0], unit=1.05, stroke_width=5),
            phasor(b0 * np.exp(0.5j * wt.get_value()), origin=cpos[1], unit=1.05, stroke_width=5)))
        pl = VGroup(MathTex(r"\alpha(t)", font_size=30).next_to(planes[0], DOWN, buff=0.1),
                    MathTex(r"\beta(t)", font_size=30).next_to(planes[1], DOWN, buff=0.1))
        turns = always_redraw(lambda: MathTex(r"\text{rotation: }" + f"{np.degrees(wt.get_value()):.0f}" + r"^\circ", font_size=32,
                                              color=C.BLOCH).move_to(RIGHT * 3.6 + UP * 1.6))
        minus = MathTex(r"360^\circ:\ \ket{\psi} \to -\ket{\psi}", font_size=34, color=C.HBAR).move_to(RIGHT * 3.6 + DOWN * 2.6)
        plus = MathTex(r"720^\circ:\ \ket{\psi} \to +\ket{\psi}", font_size=34, color=C.HBAR).next_to(minus, DOWN, buff=0.2)
        with self.voiceover(
            "Finally, put the spin in a magnetic field along z. The Hamiltonian is proportional to S z, so the up and "
            "down components just pick up opposite phases, <bookmark mark='p'/> and on the Bloch sphere the arrow "
            "precesses around the field like a spinning top: Larmor precession, about 28 billion turns per second per "
            "tesla for an electron. It's how MRI machines read the spins of protons."
        ) as vo:
            self.play(Write(h1), FadeIn(hn), FadeIn(bs))
            self.add(arr, trail)
            vo.wait_until("p")
            self.play(wt.animate.set_value(PI), run_time=vo.remaining() + 0.5, rate_func=linear)
        with self.voiceover(
            "But watch the two components themselves. <bookmark mark='h'/> They turn at half the rate of the arrow. "
            "<bookmark mark='f'/> After one full turn of the arrow, three hundred sixty degrees, both components have "
            "turned only halfway: the state has come back to minus itself. <bookmark mark='t'/> It takes seven hundred "
            "twenty degrees to get back to where you started. An overall minus sign is invisible on its own, but not in "
            "interference with an unrotated beam: neutron interferometers confirmed the sign flip in 1975."
        ) as vo:
            self.play(FadeIn(planes), FadeIn(pl), FadeIn(ph))
            self.add(turns)
            vo.wait_until("h")
            self.play(wt.animate.set_value(TAU), run_time=3.5, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeIn(minus))
            vo.wait_until("t")
            self.play(wt.animate.set_value(2 * TAU), run_time=4.0, rate_func=linear)
            self.play(FadeIn(plus))
        for mm in (arr, trail, ph, turns):
            mm.clear_updaters()
        self.clear_scene()
