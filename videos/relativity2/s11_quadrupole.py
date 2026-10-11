from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (Raster, boxed, clamp_x, label, ladder, load, mtex, note, part_card, polyline,
                                       redraw, rgba, sci, under)
from videos.relativity2.geometry import check_binary_luminosity

WAVE, MAT = C.WAVE, C.MATTER


def spiral_field(n=360, extent=7.0, r0=0.9, lam=2.2):
    """h_+ in the orbital plane of a circular binary (far-zone form, carried inward for the picture):
    h ~ cos(2 (omega (t - r) - phi)) / r, with the wavelength lam = pi / omega.  Returns a function of the
    orbital phase."""
    y, x = np.mgrid[extent:-extent:n * 1j, -extent:extent:n * 1j]
    r = np.hypot(x, y)
    ph = np.arctan2(y, x)
    k = 2 * np.pi / lam
    amp = 1 / np.maximum(r, r0) ** 0.75
    amp = amp / amp.max()
    fade = np.clip((r - 0.5 * r0) / (0.5 * r0), 0, 1) * np.clip((extent - r) / 1.0, 0, 1)
    pos = np.array(ManimColor(WAVE).to_rgb())
    neg = np.array(ManimColor(C.METRIC).to_rgb())

    def draw(orb_phase):
        h = np.cos(k * r - 2 * (ph - orb_phase)) * amp * fade
        rgb = np.where(h[..., None] > 0, pos, neg) * np.abs(h)[..., None] ** 0.8
        return rgba(rgb, np.clip(np.abs(h) * 1.6, 0, 1))

    return draw


class Quadrupole(VoiceoverScene):
    def construct(self):
        assert check_binary_luminosity() == "ok"
        self.card()
        self.retarded()
        self.virial()
        self.energy()
        self.binary()

    def card(self):
        c = part_card("III", r"Gravitational waves, derived", r"the energy they carry, and the chirp")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def retarded(self):
        rows = [
            mtex(r"\Box\,\bar h_{\mu\nu}", r"=", r"-16\pi\,T_{\mu\nu}", font_size=42),
            mtex(r"\bar h_{\mu\nu}(t, \mathbf{x})", r"=", r"4\int\frac{T_{\mu\nu}(t - |\mathbf{x} - \mathbf{y}|,\ \mathbf{y})}{|\mathbf{x} - \mathbf{y}|}\,d^3y",
                 font_size=40),
            mtex(r"\bar h_{ij}", r"\approx", r"\frac{4}{r}\int T_{ij}(t - r,\ \mathbf{y})\,d^3y", font_size=42),
        ]
        whys = [
            note(r"part 1: the linearized field equation, a wave equation with a source"),
            note(r"its retarded solution: each bit of source counts as it was when its signal left (like Li\'enard--Wiechert)"),
            note(r"far away ($r \gg$ source) and slow ($v \ll 1$): the whole source at one retarded time"),
        ]
        rows[0][2].set_color(MAT)
        rows[2][0].set_color(WAVE)
        under(rows, whys, -1.0)
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.75)
        q = label(r"but $\int T_{ij}\,d^3y$ involves stresses inside the source. \ What is it?", font_size=28,
                  color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In part one, we found that ripples in spacetime obey a wave equation, and quoted the formula for the waves "
            "a source makes. Let's derive it. <bookmark mark='a'/> Start from the linearized field equation. "
            "<bookmark mark='b'/> Like the equations of electromagnetism, it's solved by a retarded integral: the "
            "field here and now adds up the source everywhere, as it was when the signal left it. "
            "<bookmark mark='c'/> Far from a slowly moving source, the delay is the same for all of it, and the "
            "spatial part of the wave is four over r times the integral of the stresses, T i j. "
            "<bookmark mark='d'/> That looks hard to know: it involves pressures and stresses deep inside the source."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    # ------------------------------------------------------------------
    def virial(self):
        rows = [
            mtex(r"\partial_t T^{00} + \partial_k T^{k0} = 0", r",", r"\quad \partial_t T^{0i} + \partial_k T^{ki} = 0", font_size=38),
            mtex(r"\partial_t^2 T^{00}", r"=", r"\partial_k\partial_l T^{kl}", font_size=40),
            mtex(r"\frac{d^2}{dt^2}\int T^{00}\,y^i y^j\,d^3y", r"=", r"\int \partial_k\partial_l T^{kl}\,y^iy^j\,d^3y = 2\int T^{ij}\,d^3y",
                 font_size=38),
            mtex(r"\bar h_{ij}", r"=", r"\frac{2}{r}\,\ddot I_{ij}(t - r),\qquad I_{ij} = \int\rho\,y^iy^j\,d^3y", font_size=42),
        ]
        whys = [
            note(r"energy and momentum are conserved ($\partial_\mu T^{\mu\nu} = 0$, part 1)"),
            note(r"differentiate the first in $t$, and use the second"),
            note(r"integrate by parts twice (the source is finite, so no boundary terms)"),
            note(r"the stresses are fixed by how the mass distribution moves: its second moment, accelerating"),
        ]
        rows[3][0].set_color(WAVE)
        rows[3][2].set_color(MAT)
        under(rows, whys, -0.6, align_index=1)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.62)
        fin = VGroup(mtex(r"h^{TT}_{ij}", r"=", r"\frac{2}{r}\,\ddot Q^{TT}_{ij}(t - r)", font_size=46),
                     label(r"$Q_{ij} = I_{ij} - \tfrac13\delta_{ij}I_{kk}$, keeping the part transverse to the direction of travel "
                           r"(part 1's formula, now derived)", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        fin[0][0].set_color(WAVE)
        fin[0][2].set_color(MAT)
        fin.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Conservation comes to the rescue. <bookmark mark='a'/> Energy and momentum are conserved: two equations, "
            "one for the energy density and one for the momentum density. <bookmark mark='b'/> Differentiate the first "
            "with respect to time and substitute the second: the second time derivative of the energy density is a "
            "double divergence of the stresses. <bookmark mark='c'/> Now multiply by y i y j and integrate by parts, "
            "twice. The left side becomes the second time derivative of the mass distribution's second moment; the "
            "right side, twice the integrated stress. <bookmark mark='d'/> So the wave is two over r, times the second "
            "time derivative of the quadrupole moment. Only its traceless, transverse part is physical, which is the "
            "formula we quoted in part one."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(fin, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        q = load("quad")
        assert abs(float(q["ratio"]) - 1) < 1e-4
        c = load("consts")
        c5g, beam = float(c["c5G"]), float(c["beam"])
        rows = [
            mtex(r"t^{\rm GW}_{\mu\nu}", r"=", r"\frac{1}{32\pi}\Big\langle\partial_\mu h^{TT}_{ij}\,\partial_\nu h^{TT}_{ij}\Big\rangle", font_size=40),
            mtex(r"L", r"=", r"\frac{r^2}{32\pi}\oint\Big\langle\dot h^{TT}_{ij}\dot h^{TT}_{ij}\Big\rangle d\Omega = \frac{1}{8\pi}\oint\Big\langle\dddot Q^{TT}_{ij}\dddot Q^{TT}_{ij}\Big\rangle d\Omega",
                 font_size=36),
            mtex(r"L", r"=", r"\frac{1}{5}\Big\langle\dddot Q_{ij}\,\dddot Q_{ij}\Big\rangle", font_size=48),
        ]
        whys = [
            note(r"the energy density of a wave, averaged over a few wavelengths (Isaacson, 1968)"),
            note(r"the flux through a large sphere, with $h^{TT} = \tfrac{2}{r}\ddot Q^{TT}$"),
            note(r"the angular integral of the transverse projection gives $\tfrac{8\pi}{5}$ (checked numerically: ratio $1.0000$)"),
        ]
        rows[0][0].set_color(WAVE)
        rows[2][0].set_color(WAVE)
        under(rows, whys, -1.2)
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7)
        units = VGroup(
            mtex(r"L = \frac{G}{5c^5}\big\langle\dddot Q\,\dddot Q\big\rangle,\qquad \frac{c^5}{G} = 3.6\times10^{52}\ \text{W}",
                 font_size=34),
            label(rf"a 490-tonne steel beam, 20 m long, spun at 28 rad/s: $L \approx {sci(beam, 1)}$ W", font_size=26,
                  color=GREY_A),
            label(r"to radiate strongly, you need $\sim$ a star's mass moving at near light speed: compact binaries",
                  font_size=26, color=WAVE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        assert abs(c5g / 3.63e52 - 1) < 0.01
        with self.voiceover(
            "How much energy does the wave carry? <bookmark mark='a'/> Gravitational waves carry energy and momentum, "
            "with an effective energy density, averaged over a few wavelengths, given by this expression, due to "
            "Richard Isaacson. <bookmark mark='b'/> Integrate the flux over a big sphere around the source, and insert "
            "our wave. <bookmark mark='c'/> The angular integral of the transverse projection comes out to eight pi "
            "over five, which we checked numerically, and the result is the quadrupole formula: the luminosity is one "
            "fifth of the third time derivative of Q, squared. <bookmark mark='d'/> In everyday units, there's a factor "
            "G over c to the fifth, which is tiny. A huge steel beam spun almost to breaking radiates about ten to the "
            "minus twenty-nine watts. To radiate appreciably, you need stars' worth of mass moving at a good fraction "
            "of the speed of light."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(units, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def binary(self):
        # the spiral pattern of h_+ in the orbital plane, rotating with the binary
        draw = spiral_field()
        phase = ValueTracker(0.0)
        W = 7.0
        img = Raster(lambda v: draw(v), phase, W, W, center=[-3.4, -0.1, 0])
        cen = np.array([-3.4, -0.1, 0])
        sc = W / 14.0

        def stars():
            p = phase.get_value()
            u = np.array([math.cos(p), math.sin(p), 0])
            return VGroup(Dot(cen + 0.55 * sc * 2 * u, radius=0.13, color=MAT), Dot(cen - 0.45 * sc * 2 * u, radius=0.11, color=MAT))

        S = redraw(stars)
        cap = note(r"computed $h_+$ in the orbital plane, $\propto \cos 2(\omega(t - r) - \phi)$; pink $+$, blue $-$").next_to(img, DOWN, buff=0.1)
        clamp_x(cap)
        rows = [
            mtex(r"I_{ij}", r"=", r"\mu a^2\,n_in_j,\quad \mathbf{n} = (\cos\omega t, \sin\omega t, 0)", font_size=34),
            mtex(r"\dddot Q_{ij}\dddot Q_{ij}", r"=", r"32\,\mu^2a^4\omega^6", font_size=36),
            mtex(r"L", r"=", r"\frac{32}{5}\,\mu^2a^4\omega^6 = \frac{32}{5}\,\frac{\mu^2M^3}{a^5}", font_size=40),
        ]
        whys = [
            note(r"two masses on a circle of separation $a$ ($\mu = m_1m_2/M$)"),
            note(r"$Q$ oscillates at twice the orbital frequency (sympy)"),
            note(r"with Kepler's $\omega^2 = M/a^3$"),
        ]
        rows[2][0].set_color(WAVE)
        for r in rows:
            r.scale(0.95)
        x0 = 3.2
        under(rows, whys, x0)
        step = ladder(self, rows, whys, keep=3, top=2.9, x=x0, buff=0.55)
        # radiation pattern: dL/dOmega ~ (1 + cos^2 th)^2 / 4 + cos^2 th
        th = np.linspace(0, 2 * np.pi, 400)
        f = (1 + np.cos(th) ** 2) ** 2 / 4 + np.cos(th) ** 2
        pat_f = lambda t_: (1 + np.cos(t_) ** 2) ** 2 / 4 + np.cos(t_) ** 2  # noqa: E731
        th2 = np.linspace(0, np.pi, 4001)
        tot = 2 * np.pi * np.trapezoid(pat_f(th2) * np.sin(th2), th2)
        assert abs(tot - 16 * np.pi / 5) < 1e-5 and abs(pat_f(0.0) / pat_f(np.pi / 2) - 8) < 1e-12
        pc = np.array([3.4, -2.4, 0])
        pat = VMobject(stroke_color=WAVE, stroke_width=3, fill_color=WAVE, fill_opacity=0.25)
        pat.set_points_as_corners([pc + 0.55 * fi * np.array([math.sin(t_), math.cos(t_), 0]) for fi, t_ in zip(f, th)])
        axl = Line(pc + DOWN * 1.3, pc + UP * 1.3, color=GREY_C, stroke_width=1.5)
        pl = label(r"power vs direction: $8\times$ stronger along the orbit's axis", font_size=22, color=WAVE).next_to(pc + DOWN * 1.2, DOWN, buff=0.05)
        with self.voiceover(
            "Now apply it to two stars, or black holes, in a circular orbit. <bookmark mark='a'/> The waves spiral out "
            "from the binary like water from a rotating sprinkler, here computed in the orbital plane. Pink is "
            "stretching in one direction, blue in the other. <bookmark mark='b'/> The quadrupole moment of the pair is "
            "mu a squared times n i n j, where n points along the line between them. <bookmark mark='c'/> It "
            "oscillates at twice the orbital frequency, because the pair looks the same after half a turn, and its "
            "third derivative squared is thirty-two mu squared a to the fourth omega to the sixth. "
            "<bookmark mark='d'/> With Kepler's law, the luminosity is thirty-two fifths mu squared M cubed over a to "
            "the fifth: closer orbits radiate ferociously. <bookmark mark='e'/> The radiation is strongest along the "
            "orbit's axis, eight times stronger than in its plane."
        ) as vo:
            self.add(img, S)
            self.play(FadeIn(cap), phase.animate.set_value(2 * np.pi), run_time=vo.until("b"), rate_func=linear)
            step(0)
            self.play(phase.animate.set_value(4 * np.pi), run_time=vo.until("c"), rate_func=linear)
            step(1)
            self.play(phase.animate.set_value(6 * np.pi), run_time=vo.until("d"), rate_func=linear)
            step(2)
            self.play(phase.animate.set_value(8 * np.pi), run_time=vo.until("e"), rate_func=linear)
            self.play(Create(axl), DrawBorderThenFill(pat), FadeIn(pl), phase.animate.set_value(10 * np.pi),
                      run_time=vo.remaining() + 0.5, rate_func=linear)
        img.clear_updaters()
        S.clear_updaters()
        self.clear_scene()
