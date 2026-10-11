from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (Raster, WaveView, ab_movie, corner_wheel, label, ladder, load, mtex, note,
                                    phase_rgba, plain_axes, polyline, wave_axes, why)
from videos.quantum2.compute import AB


def packet(x, x0=0.0, s=1.2, k=1.2):
    return (2 * np.pi * s * s) ** -0.25 * np.exp(-((x - x0) ** 2) / (4 * s * s) + 1j * k * x)


class Gauge(VoiceoverScene):
    def construct(self):
        self.local_phase()
        self.covariant()
        self.loop_phase()
        self.simulation()
        self.slide()
        self.tonomura()

    # ------------------------------------------------------------------
    def local_phase(self):
        x = np.linspace(-8, 8, 1600)
        chi = 1.6 * np.sin(1.3 * x) + 0.9 * np.cos(0.55 * x + 0.4) + 0.25 * x
        s = ValueTracker(0.0)
        top = wave_axes((-8, 8), (0, 0.4), x_length=11.0, y_length=2.1).move_to(UP * 1.2)
        wv = WaveView(top, x, packet(x), mode="density").follow(s, lambda v: packet(x) * np.exp(1j * v * chi))
        cax = wave_axes((-8, 8), (-3.8, 3.8), x_length=11.0, y_length=1.6).move_to(DOWN * 2.0)
        cl = polyline(cax, x, chi, color=C.GAUGE, stroke_width=3)
        cll = MathTex(r"q\chi(x)/\hbar", font_size=28, color=C.GAUGE).next_to(cax.c2p(-8, 3.8), RIGHT, buff=0.1)
        eq0 = MathTex(r"\psi", r"\;\to\;", r"e^{i\alpha}", r"\psi", font_size=40).to_edge(UP, buff=0.25)
        eq1 = MathTex(r"\psi(x)", r"\;\to\;", r"e^{\,iq\chi(x)/\hbar}", r"\,\psi(x)", font_size=40).to_edge(UP, buff=0.25)
        eq1[2].set_color(C.GAUGE)
        dens = label(r"$|\psi|^2$ unchanged everywhere", font_size=28, color=C.BORN).next_to(top, DOWN, buff=0.15)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        with self.voiceover(
            "Part 1 showed that multiplying the whole wavefunction by one phase, e to the i alpha, changes nothing. "
            "<bookmark mark='a'/> So here's a bolder question. What if we change the phase by a different amount at "
            "every point? <bookmark mark='b'/> The colors scramble, <bookmark mark='c'/> but every probability stays "
            "exactly the same."
        ) as vo:
            self.play(Create(top), FadeIn(wv), Write(eq0), FadeIn(wheel))
            vo.wait_until("a")
            self.play(TransformMatchingTex(eq0, eq1), Create(cax), Create(cl), FadeIn(cll))
            vo.wait_until("b")
            self.play(s.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(dens))
        wv.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def covariant(self):
        p0 = MathTex(r"-i\hbar\nabla\big(e^{iq\chi/\hbar}\psi\big)", r"=", r"e^{iq\chi/\hbar}\big(-i\hbar\nabla", r"+ q\nabla\chi", r"\big)\psi",
                     font_size=38).to_edge(UP, buff=0.5)
        p0[3].set_color(C.GAUGE)
        kick = label(r"an extra momentum $q\nabla\chi$ that varies from place to place: the physics would change", font_size=26,
                     color=GREY_A).next_to(p0, DOWN, buff=0.25)
        with self.voiceover(
            "The Schrödinger equation, however, notices. <bookmark mark='a'/> Apply the momentum operator to the new "
            "wavefunction. The product rule brings down an extra term, the gradient of the phase: <bookmark mark='b'/> "
            "as far as the equation is concerned, the particle has been given a momentum kick that varies from place to "
            "place. A pure change of bookkeeping would change the physics."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(p0))
            vo.wait_until("b")
            self.play(Indicate(p0[3], color=C.GAUGE), FadeIn(kick))
        rows = [
            MathTex(r"\mathbf A", r"\;\to\;", r"\mathbf A + \nabla\chi", font_size=38),
            MathTex(r"(-i\hbar\nabla - q\mathbf A')\,\psi'", r"=", r"e^{iq\chi/\hbar}\,(-i\hbar\nabla - q\mathbf A)\,\psi", font_size=38),
            MathTex(r"\phi", r"\;\to\;", r"\phi - \partial_t\chi", font_size=38),
            MathTex(r"\hat H", r"=", r"\frac{(\hat{\mathbf p} - q\mathbf A)^2}{2m} + q\phi", font_size=46),
        ]
        rows[0][2].set_color(C.GAUGE)
        rows[3].set_color(C.ENERGY)
        whys = [
            why(rows[0], r"a new field that shifts along with the phase"),
            why(rows[1], r"the extra terms cancel exactly"),
            why(rows[2], r"the same for $i\hbar\,\partial_t$"),
            why(rows[3], r"a charge in electromagnetic potentials"),
        ]
        for r, w in zip(rows, whys):
            r.shift(DOWN * 1.2)
        step = ladder(self, rows, whys, keep=4, top=1.55, x=-1.8, buff=0.42)
        fields = MathTex(r"\mathbf E = -\nabla\phi - \partial_t\mathbf A", r",\qquad", r"\mathbf B = \nabla\times\mathbf A", r"\quad\text{unchanged by }\chi",
                         font_size=32).to_edge(DOWN, buff=0.6)
        hist = note(r"Fock (1926), London (1927), Weyl (1929): local phase symmetry $\Rightarrow$ electromagnetism").to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "There's only one way to rescue the symmetry. <bookmark mark='a'/> Introduce a field, A, that shifts by the "
            "same gradient whenever the phase is changed, and use p minus q A in place of p. <bookmark mark='b'/> Now "
            "the extra terms cancel exactly: p minus q A acting on the new wavefunction is just the phase factor times p "
            "minus q A acting on the old one. <bookmark mark='c'/> Do the same with time, and you need a second field, "
            "phi."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='a'/> The Hamiltonian becomes p minus q A, squared, over 2m, plus q phi: exactly how a "
            "charge couples to the electromagnetic potentials, <bookmark mark='b'/> with the electric and magnetic "
            "fields, built from derivatives of A and phi, unchanged by the phase change. <bookmark mark='c'/> Fock, "
            "London and Weyl found this between 1926 and 1929: demand that local phase changes be a symmetry, and "
            "electromagnetism appears."
        ) as vo:
            vo.wait_until("a")
            step(3)
            vo.wait_until("b")
            self.play(Write(fields))
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop_phase(self):
        o = LEFT * 3.0 + DOWN * 0.4
        S, D = o + LEFT * 2.8, o + RIGHT * 2.8
        tube = Circle(radius=0.32, color=C.GAUGE, fill_color=C.GAUGE, fill_opacity=0.35, stroke_width=2).move_to(o)
        bl = MathTex(r"\mathbf B \neq 0", font_size=24, color=C.GAUGE).next_to(tube, DOWN, buff=0.12)
        up = ArcBetweenPoints(S, D, angle=-PI / 2.2, color=C.XPOS, stroke_width=4)
        dn = ArcBetweenPoints(S, D, angle=PI / 2.2, color=C.XPOS, stroke_width=4)
        tips = VGroup(Arrow(up.point_from_proportion(0.48), up.point_from_proportion(0.52), buff=0, color=C.XPOS, tip_length=0.2),
                      Arrow(dn.point_from_proportion(0.48), dn.point_from_proportion(0.52), buff=0, color=C.XPOS, tip_length=0.2))
        sd = VGroup(Dot(S), Dot(D))
        b0 = label(r"$\mathbf B = 0$ along both paths", font_size=24, color=GREY_B).next_to(up, UP, buff=0.15)
        f1 = MathTex(r"\psi_{\text{path}}", r"\;\propto\;", r"\exp\!\Big(\frac{iq}{\hbar}\int_{\text{path}}\mathbf A\cdot d\boldsymbol\ell\Big)", font_size=34)
        f2 = MathTex(r"\Delta\varphi", r"=", r"\frac{q}{\hbar}\oint\mathbf A\cdot d\boldsymbol\ell", r"=", r"\frac{q}{\hbar}\iint \mathbf B\cdot d\mathbf S",
                     r"=", r"\frac{q\,\Phi}{\hbar}", font_size=34)
        f2[6].set_color(C.GAUGE)
        f3 = MathTex(r"\Phi_0 = \frac{h}{e}", r"=", r"4.14\times 10^{-15}\ \text{Wb}", font_size=34)
        n = load("numbers")
        assert abs(float(n["h_over_e"]) - 4.1357e-15) < 1e-18
        col = VGroup(f1, f2, f3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 2.8 + UP * 0.6)
        if col.width > 7.4:
            col.width = 7.4
            col.move_to(RIGHT * 3.0 + UP * 0.6)
        motto = label(r"phase $=$ (flux through the loop) $\times\, q/\hbar$", font_size=28, color=C.HBAR).next_to(col, DOWN, buff=0.45)
        ab = note(r"Ehrenberg \& Siday (1949); Aharonov \& Bohm (1959)").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "This has a startling consequence. <bookmark mark='a'/> A charged particle moving along a path picks up an "
            "extra phase, q over h-bar times the integral of A along the path. <bookmark mark='b'/> For two paths that "
            "start and end together, the difference is the integral around the loop, which by Stokes' theorem is the "
            "magnetic flux through the loop. <bookmark mark='c'/> So the relative phase is q times the flux, over "
            "h-bar, even if the magnetic field is zero everywhere the particle goes. <bookmark mark='d'/> Phase equals "
            "area over h-bar again; this time the area is threaded by magnetic flux. Aharonov and Bohm pointed this out "
            "in 1959."
        ) as vo:
            self.play(FadeIn(tube), FadeIn(bl), FadeIn(sd))
            vo.wait_until("a")
            self.play(Create(up), Create(dn), FadeIn(tips), Write(f1))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(FadeIn(b0), Indicate(f2[6], color=C.GAUGE))
            vo.wait_until("d")
            self.play(FadeIn(motto), FadeIn(f3), FadeIn(ab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _movie(self, alpha, width, center, t):
        P = AB
        mv = ab_movie(alpha)
        ts = load("ab")["movie_t"]
        x0, x1, y0, y1 = 50, 290, -100, 100
        cols = slice(x0, x1)
        rows = slice(int(y0 + P["Y"] / 2), int(y1 + P["Y"] / 2))
        wallx = P["wall"][1] - x0
        gain = np.ones(x1 - x0, np.float32)
        gain[int(wallx) + 1:] = 3.0
        vmax = 0.016

        def draw(tt):
            k = int(np.clip(round(np.interp(tt, ts, np.arange(len(ts)))), 0, len(ts) - 1))
            f = np.asarray(mv[k, rows, cols], np.float32)
            psi = (f[..., 0] + 1j * f[..., 1])[::-1] * gain[None, :]
            return phase_rgba(psi, vmax=vmax, gamma=0.6)

        h = width * (y1 - y0) / (x1 - x0)
        img = Raster(draw, t, width, h, center=center)

        def to_screen(x, y):
            return np.array(center) + np.array([(x - (x0 + x1) / 2) / (x1 - x0) * width, (y - (y0 + y1) / 2) / (y1 - y0) * h, 0])

        plate = VGroup()
        a, w = P["d"] / 2, P["w"] / 2
        for ya, yb in ((y0, -a - w), (-a + w, a - w), (a + w, y1)):
            p0, p1 = to_screen(P["wall"][0], ya), to_screen(P["wall"][1], yb)
            plate.add(Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=C.WALL,
                                fill_opacity=1).move_to((p0 + p1) / 2))
        tube = Dot(to_screen(np.mean(P["wall"]), 0), radius=0.06, color=C.GAUGE)
        det = Line(to_screen(P["det"][0], y0), to_screen(P["det"][0], y1), color=GREY_A, stroke_width=2)
        return img, plate, tube, det

    def simulation(self):
        t = ValueTracker(0.0)
        L = self._movie(0.0, 6.3, LEFT * 3.4 + DOWN * 0.15, t)
        R = self._movie(0.5, 6.3, RIGHT * 3.4 + DOWN * 0.15, t)
        tl = MathTex(r"\Phi = 0", font_size=34, color=C.GAUGE).next_to(L[0], UP, buff=0.15)
        tr = MathTex(r"\Phi = \tfrac12\,h/e", font_size=34, color=C.GAUGE).next_to(R[0], UP, buff=0.15)
        u = load("ab")
        tmax = max(float(u[k]) for k in u if k.startswith("tube_max"))
        assert tmax < 3e-8
        tag = note(r"computed: Schr\"odinger equation on a $1280 \times 1152$ grid, flux tube (dot) inside the wall; "
                   r"color = phase, brightness = $|\psi|$ ($\times 3$ right of the wall)").to_edge(DOWN, buff=0.15)
        wheel = corner_wheel(corner=UR, buff=0.15, radius=0.25)
        with self.voiceover(
            "Here's the effect, simulated. <bookmark mark='a'/> An electron wave passes through two slits; hidden inside "
            "the wall between them is a thin tube of magnetic flux. <bookmark mark='b'/> The wave never reaches it: the "
            "density there stays below a ten-thousandth of its peak. <bookmark mark='c'/> On the left, no flux. On the "
            "right, half a flux quantum, and the bright central fringe has become a dark line."
        ) as vo:
            for g in (L, R):
                self.add(g[0])
            self.play(*[FadeIn(m) for g in (L, R) for m in g], FadeIn(tl), FadeIn(tr), FadeIn(tag), FadeIn(wheel))
            vo.wait_until("a")
            self.play(Flash(L[2], color=C.GAUGE), Flash(R[2], color=C.GAUGE), t.animate.set_value(60), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(120), run_time=max(2.0, vo.mark_time("c") - vo.elapsed()), rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(210), run_time=max(4.0, vo.remaining()), rate_func=linear)
        for g in (L, R):
            g[0].clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def slide(self):
        u = load("ab")
        y, det, al = u["y"], u["det"], u["alphas"]
        keep = np.abs(y) < 125
        yy = y[keep]
        D = det[:, keep] / det[0, keep].max()
        ax = plain_axes((-125, 125), (0, 1.15), 11.5, 3.6).move_to(DOWN * 0.6)
        yl = MathTex(r"\text{height on the screen}", font_size=26, color=GREY_B).next_to(ax.x_axis.get_end(), DOWN, buff=0.15).shift(LEFT * 1.2)
        k = ValueTracker(0.0)
        ref = polyline(ax, yy, D[0], color=GREY_C, stroke_width=2).set_stroke(opacity=0.6)
        cur = always_redraw(lambda: polyline(ax, yy, D[int(round(k.get_value()))], color=C.BORN, stroke_width=4))
        fr = ["0", r"\tfrac{1}{12}", r"\tfrac{1}{6}", r"\tfrac{1}{4}", r"\tfrac{1}{3}", r"\tfrac{5}{12}", r"\tfrac{1}{2}", r"\tfrac{7}{12}",
              r"\tfrac{2}{3}", r"\tfrac{3}{4}", r"\tfrac{5}{6}", r"\tfrac{11}{12}", ""]

        def flux_label():
            i = int(round(k.get_value()))
            body = r"\Phi = 0" if i == 0 else r"\Phi = " + fr[i] + r"\,h/e"
            return MathTex(body, font_size=40, color=C.GAUGE).to_corner(UR, buff=0.6)

        al_l = always_redraw(flux_label)
        # the phase of the central fringe component: one full turn per flux quantum
        shift = u["fringe_phase"]
        kf = float(u["fringe_k"])
        mk = always_redraw(lambda: Triangle(color=C.GAUGE, fill_opacity=1).scale(0.12).rotate(PI).move_to(
            ax.c2p(-shift[int(round(k.get_value()))] / kf, 1.12)))
        title = label(r"arrival pattern on the screen, computed for 13 values of the flux", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        res = label(r"one fringe per flux quantum $h/e$: the electrons never touch $\mathbf B$", font_size=28, color=C.GAUGE).to_edge(DOWN, buff=0.45)
        slope = float(u["fringe_slope"]) / (2 * np.pi)
        assert abs(abs(slope) - 1) < 0.08
        with self.voiceover(
            "Now turn the flux up slowly, and watch the pattern on the screen. <bookmark mark='a'/> The fringes slide "
            "sideways under a fixed envelope, <bookmark mark='b'/> by one whole fringe for each flux quantum, h over e, "
            "and then the pattern is exactly what it was. <bookmark mark='c'/> The electrons never touch the magnetic "
            "field, yet they know how much flux they went around."
        ) as vo:
            self.play(FadeIn(title), Create(ax), FadeIn(yl), FadeIn(ref), FadeIn(cur), FadeIn(al_l), FadeIn(mk))
            vo.wait_until("a")
            self.play(k.animate.set_value(6), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(12), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(res))
        for m in (cur, al_l, mk):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tonomura(self):
        # schematic: an electron wave passing around a ring magnet sealed in a superconductor
        o = LEFT * 3.4 + DOWN * 0.2
        ring_out = Annulus(inner_radius=0.55, outer_radius=1.05, color=GREY_B, fill_opacity=0.5).move_to(o)
        ring_sc = Annulus(inner_radius=0.45, outer_radius=1.15, color=C.XPOS, fill_opacity=0.0, stroke_width=3).move_to(o)
        ring_sc.set_stroke(C.XPOS, 3)
        lab_m = label(r"magnet (flux $\Phi$ inside)", font_size=22, color=GREY_A).next_to(ring_out, DOWN, buff=0.45)
        lab_s = label(r"superconducting niobium shell", font_size=22, color=C.XPOS).next_to(lab_m, DOWN, buff=0.1)
        waves = VGroup(*[Line(o + LEFT * 3 + UP * y, o + LEFT * 1.4 + UP * y, color=C.BORN, stroke_width=2) for y in np.linspace(-1.4, 1.4, 8)])
        sch = note(r"schematic").next_to(lab_s, DOWN, buff=0.15)
        lines = VGroup(
            label(r"Tonomura et al.\ (Hitachi, 1986): electrons around a $\sim 6\,\mu$m toroidal magnet", font_size=26),
            label(r"the superconductor traps flux only in units of $h/2e = 2.07\times 10^{-15}$ Wb", font_size=26),
            MathTex(r"\Delta\varphi = \frac{e}{\hbar}\cdot N\,\frac{h}{2e} = N\pi", font_size=34, color=C.GAUGE),
            label(r"observed: shifts of $0$ or half a fringe, with the field fully shielded", font_size=26, color=C.BORN),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.6)
        if lines.width > 7.6:
            lines.width = 7.6
            lines.move_to(RIGHT * 2.9)
        n = load("numbers")
        assert abs(float(n["h_over_2e"]) - 2.0678e-15) < 1e-18
        with self.voiceover(
            "In 1986 Akira Tonomura's group at Hitachi did it with electrons passing around a tiny ring-shaped magnet, "
            "<bookmark mark='a'/> sealed inside a superconductor so that no field could leak out. <bookmark mark='b'/> A "
            "superconducting ring traps flux only in multiples of h over 2e, half a flux quantum, <bookmark mark='c'/> "
            "so the fringes could only be shifted by zero or by half a fringe. <bookmark mark='d'/> That's exactly what "
            "they saw."
        ) as vo:
            self.play(FadeIn(ring_out), FadeIn(waves), FadeIn(lines[0]), FadeIn(lab_m), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(ring_sc), FadeIn(lab_s))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()
