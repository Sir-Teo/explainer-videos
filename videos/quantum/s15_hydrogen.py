from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (Raster, boxed, corner_wheel, label, load, mtex, note, num, num_table, orbital_image,
                                   place_whys, polyline, spectrum_color, stack, why)
from videos.quantum.compute import ORBITALS, tone


class Hydrogen(VoiceoverScene):
    def construct(self):
        self.setup_problem()
        self.separation()
        self.ground_state()
        self.quantization()
        self.gallery()
        self.real_orbitals()
        self.light()

    # ------------------------------------------------------------------
    def setup_problem(self):
        h = load("hydrogen")
        a0 = float(h["a0"][0]) * 1e10
        assert abs(a0 - 0.529) < 0.001
        eq = MathTex(r"-\frac{\hbar^2}{2m}\nabla^2\psi", r"-", r"\frac{e^2}{4\pi\varepsilon_0\,r}\,\psi", r"=", r"E\,\psi", font_size=46)
        eq[2].set_color(C.POTENTIAL)
        eq[4].set_color(C.ENERGY)
        eq.to_edge(UP, buff=0.7)
        n1 = label(r"one electron, bound to a proton by the Coulomb force", font_size=28, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        a0t = MathTex(r"a_0", r"=", r"\frac{4\pi\varepsilon_0\hbar^2}{m e^2}", r"=", rf"{a0:.3f}\ \text{{\AA}}", font_size=42)
        a0t[0].set_color(C.XPOS)
        a0t.move_to(DOWN * 0.6)
        a0n = label(r"the only length you can build from $\hbar$, $m$ and $e^2/4\pi\varepsilon_0$: the Bohr radius", font_size=26,
                    color=GREY_A).next_to(a0t, DOWN, buff=0.25)
        e0 = MathTex(r"\frac{e^2}{4\pi\varepsilon_0 a_0} = 27.2\ \text{eV}", font_size=36, color=C.ENERGY).next_to(a0n, DOWN, buff=0.45)
        with self.voiceover(
            "Now the system that started it all: the hydrogen atom. One electron, held by a proton through the Coulomb "
            "force. In three dimensions, the energy equation reads like this. <bookmark mark='a'/> Before solving "
            "anything, ask what length the answer can depend on. From h-bar, the electron's mass and the strength of the "
            "electric force, there's only one way to make a length: the Bohr radius, about half an angstrom. "
            "<bookmark mark='e'/> And the natural energy is the Coulomb energy at that distance, 27.2 electron volts."
        ) as vo:
            self.play(Write(eq), FadeIn(n1))
            vo.wait_until("a")
            self.play(Write(a0t), FadeIn(a0n))
            vo.wait_until("e")
            self.play(Write(e0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def separation(self):
        s1 = MathTex(r"\psi(r, \theta, \varphi)", r"=", r"R(r)", r"\,", r"Y_\ell^m(\theta, \varphi)", font_size=42)
        s1.to_edge(UP, buff=0.4)
        s2 = MathTex(r"Y_\ell^m", r"\propto", r"P_\ell^m(\cos\theta)", r"\,", r"e^{im\varphi}", font_size=38)
        s2[4].set_color(C.MOMENTUM)
        s3 = MathTex(r"\hat L^2 Y = \hbar^2\ell(\ell + 1)\,Y", r",\qquad", r"\hat L_z Y = m\hbar\,Y", font_size=34)
        VGroup(s2, s3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(s1, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        img = orbital_image("orb_211", height=2.6).move_to(RIGHT * 4.3 + UP * 1.4)
        il = MathTex(r"(n, \ell, m) = (2, 1, 1)", font_size=28).next_to(img, DOWN, buff=0.1)
        wn = label(r"the phase winds once around the vertical axis:\\angular momentum is written in the phase", font_size=24,
                   color=GREY_A).next_to(il, DOWN, buff=0.12)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        r1 = MathTex(r"u = r R:\quad", r"-\frac{\hbar^2}{2m}u''", r"+", r"V_{\text{eff}}(r)\,u", r"=", r"E\,u", font_size=36)
        r2 = MathTex(r"V_{\text{eff}}", r"=", r"-\frac{e^2}{4\pi\varepsilon_0 r}", r"+", r"\frac{\hbar^2\ell(\ell+1)}{2mr^2}", font_size=36)
        rr = VGroup(r1, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(DL, buff=0.5)
        r2[0].set_color(C.POTENTIAL)
        r2[4].set_color(C.MOMENTUM)
        ax = Axes(x_range=[0, 12, 2], y_range=[-1.1, 0.5, 0.5], x_length=4.6, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_corner(DR, buff=0.45)
        rs = np.linspace(0.05, 12, 600)
        cols = [interpolate_color(ManimColor(C.POTENTIAL), ManimColor(C.MOMENTUM), l / 2) for l in (0, 1, 2)]

        def veff_curve(l, c):
            v = -1 / rs + l * (l + 1) / (2 * rs**2)
            k = v <= 0.5  # draw only inside the axes (no flat clipped segments)
            return polyline(ax, rs[k], np.maximum(v[k], -1.1), color=c, stroke_width=3)

        curves = VGroup(*[veff_curve(l, c) for l, c in zip((0, 1, 2), cols)])
        cl = VGroup(*[MathTex(rf"\ell = {l}", font_size=24, color=c) for l, c in zip((0, 1, 2), cols)]).arrange(RIGHT, buff=0.3)
        cl.next_to(ax.c2p(12, 0.5), DL, buff=0.05)
        ax_l = note(r"$r$ in units of $a_0$").next_to(ax, DOWN, buff=0.08)
        with self.voiceover(
            "The potential depends only on the distance r, so separate the wavefunction into a radial part and an "
            "angular part. <bookmark mark='y'/> The angular parts are the spherical harmonics, labeled by two numbers, "
            "l and m, for the total angular momentum and its component along an axis. <bookmark mark='w'/> Notice the "
            "factor e to the i m phi: as you go around the vertical axis, the phase winds m times. Angular momentum is "
            "written in the phase, just as linear momentum was."
        ) as vo:
            self.play(Write(s1))
            vo.wait_until("y")
            self.play(Write(s2), Write(s3))
            vo.wait_until("w")
            self.play(FadeIn(img), FadeIn(il), FadeIn(wn), FadeIn(wheel))
        with self.voiceover(
            "What's left is a one-dimensional problem for u, r times R, <bookmark mark='v'/> in an effective potential: "
            "the Coulomb well plus a centrifugal barrier that keeps electrons with angular momentum away from the "
            "nucleus."
        ) as vo:
            self.play(Write(r1), FadeOut(wn))
            vo.wait_until("v")
            self.play(Write(r2), Create(ax), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(cl), FadeIn(ax_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ground_state(self):
        h = load("hydrogen")
        rr, P10 = h["rr"], h["P10"]
        g1 = MathTex(r"u", r"=", r"r^{\ell+1}e^{-\beta r}", font_size=38)
        g2 = MathTex(r"\frac{u''}{u}", r"=", r"\frac{\ell(\ell+1)}{r^2} - \frac{2\beta(\ell+1)}{r} + \beta^2", font_size=38)
        g3 = MathTex(r"\Big(\frac{\hbar^2\beta(\ell+1)}{m} - \frac{e^2}{4\pi\varepsilon_0}\Big)\frac{1}{r}", r"-", r"\frac{\hbar^2\beta^2}{2m}",
                     r"=", r"E", font_size=36)
        g4 = MathTex(r"\beta = \frac{1}{(\ell + 1)\,a_0}", r",\qquad", r"E = -\frac{13.6\ \text{eV}}{(\ell + 1)^2}", font_size=40)
        col = VGroup(g1, g2, g3, g4).arrange(DOWN, buff=0.38).to_edge(UP, buff=0.4).shift(LEFT * 1.0)
        g4[2].set_color(C.ENERGY)
        w1 = why(g1, r"guess: a power near $r = 0$, a decay far away")
        w2 = why(g2, r"differentiate twice")
        w3 = why(g3, r"put it in the radial equation")
        w4 = why(g4, r"the $1/r$ term must vanish")
        place_whys([g1, g2, g3, g4], [w1, w2, w3, w4])
        with self.voiceover(
            "Here's a short route to the ground state. <bookmark mark='a'/> Guess a solution that behaves like a power "
            "of r near the nucleus and decays exponentially far away. <bookmark mark='b'/> Differentiate it twice. "
            "<bookmark mark='c'/> Put it into the radial equation: you get a constant, plus a term proportional to one "
            "over r. For the equation to hold at every r, that term's coefficient must vanish. <bookmark mark='d'/> That "
            "fixes the decay rate, one over l plus one Bohr radii, and the energy: minus 13.6 electron volts over l plus "
            "one, squared."
        ) as vo:
            for m, l, w in zip("abcd", (g1, g2, g3, g4), (w1, w2, w3, w4)):
                vo.wait_until(m)
                self.play(Write(l), FadeIn(w))
        e1 = MathTex(r"\psi_{100}", r"=", r"\frac{e^{-r/a_0}}{\sqrt{\pi a_0^3}}", r",\qquad", r"E_1 = -13.6\ \text{eV}", font_size=40)
        e1[4].set_color(C.ENERGY)
        e1b = boxed(e1, color=C.ENERGY, buff=0.18).to_edge(DOWN, buff=1.6).shift(LEFT * 2.6)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 0.6, 0.2], x_length=4.6, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_corner(DR, buff=0.5)
        pc = polyline(ax, rr[rr <= 6], P10[rr <= 6], color=C.BORN, stroke_width=3)
        mk = DashedLine(ax.c2p(1, 0), ax.c2p(1, 0.6), color=C.XPOS, stroke_width=2)
        mkl = MathTex(r"r = a_0", font_size=26, color=C.XPOS).next_to(ax.c2p(1, 0.6), UP, buff=0.05)
        pl = MathTex(r"P(r) = 4\pi r^2|\psi|^2", font_size=26, color=C.BORN).next_to(ax, UP, buff=0.35).align_to(ax, RIGHT)
        mp = note(r"most probable radius: $r = a_0$, exactly Bohr's 1913 orbit").next_to(e1b, DOWN, buff=0.2).align_to(e1b, LEFT)
        real = note(r"(real hydrogen, with the proton's recoil: $-13.598$ eV)").next_to(mp, DOWN, buff=0.08).align_to(mp, LEFT)
        with self.voiceover(
            "For l equal to zero, that's the ground state: a simple exponential, <bookmark mark='g'/> with energy minus "
            "13.6 electron volts. <bookmark mark='p'/> The probability of finding the electron at distance r, counting "
            "the whole shell of that radius, peaks at exactly one Bohr radius: the radius of Bohr's 1913 orbit, now as "
            "the most likely distance in a cloud."
        ) as vo:
            self.play(FadeOut(VGroup(w1, w2, w3)), Write(e1), Create(e1b[0]))
            vo.wait_until("g")
            self.play(FadeIn(real))
            vo.wait_until("p")
            self.play(Create(ax), Create(pc), FadeIn(pl), Create(mk), FadeIn(mkl), FadeIn(mp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quantization(self):
        h = load("hydrogen")
        rs, ulo, uex, uhi = h["r_shoot"], h["u_lo"], h["u_ex"], h["u_hi"]
        keep = rs <= 8.0
        ax = Axes(x_range=[0, 8, 2], y_range=[-1.2, 1.2, 0.5], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.3 + UP * 0.9)
        def inside(u):
            out = np.nonzero(np.abs(u[keep]) > 1.2)[0]
            n = out[0] if len(out) else keep.sum()
            return rs[keep][:n], u[keep][:n]

        c_lo = polyline(ax, *inside(ulo), color=GREY_B, stroke_width=2.5)
        c_hi = polyline(ax, *inside(uhi), color=GREY_A, stroke_width=2.5)
        c_ex = polyline(ax, *inside(uex), color=C.ENERGY, stroke_width=4)
        labs = VGroup(MathTex(r"E = 1.04\,E_1", font_size=26, color=GREY_B).next_to(c_lo.get_end(), RIGHT, buff=0.12),
                      MathTex(r"E = 0.96\,E_1", font_size=26, color=GREY_A).next_to(c_hi.get_end(), RIGHT, buff=0.12),
                      MathTex(r"E = E_1", font_size=28, color=C.ENERGY).next_to(ax.c2p(7.0, 0.0), UP, buff=0.15))
        rl = MathTex(r"r/a_0", font_size=26).next_to(ax.x_axis.get_end(), RIGHT, buff=0.08)
        ul = MathTex(r"u(r)", font_size=26).next_to(ax.y_axis.get_end(), UP, buff=0.08)
        en = MathTex(r"E_n", r"=", r"-\frac{13.6\ \text{eV}}{n^2}", r",\qquad n = 1, 2, 3, \dots", font_size=40)
        en[0].set_color(C.ENERGY)
        enb = boxed(en, color=C.ENERGY, buff=0.18).to_edge(DOWN, buff=0.4).shift(LEFT * 2.6)
        sn = label(r"series solution: it must stop, or $u \sim e^{+r}$", font_size=26, color=GREY_A).next_to(enb, UP, buff=0.15).align_to(enb, LEFT)
        # matrix check: l = 0, 1, 2 give the same levels
        rows = []
        for n in range(1, 5):
            row = [str(n)]
            for l in (0, 1, 2):
                if n > l:
                    row.append(num(float(h[f"E_l{l}"][n - l - 1]), 4))
                else:
                    row.append(r"-")
            row.append(num(-0.5 / n**2, 4))
            rows.append(row)
        tab = num_table([r"n", r"\ell = 0", r"\ell = 1", r"\ell = 2", r"-\tfrac{1}{2n^2}"], rows, font_size=26,
                        col_colors=[WHITE, C.ENERGY, C.ENERGY, C.ENERGY, GREY_A]).to_corner(UR, buff=0.4)
        tn = note(r"radial equation as an $8{,}000 \times 8{,}000$ matrix\\(energies in Hartree, $= 27.2$ eV)")
        tn.next_to(tab, DOWN, buff=0.12).align_to(tab, RIGHT)
        with self.voiceover(
            "For the other states, the same idea works with a polynomial in front of the exponential. Integrate outward "
            "from the nucleus at a trial energy: <bookmark mark='s'/> if the energy is a little off, the solution blows "
            "up far from the atom, one way or the other. <bookmark mark='e'/> Only at special energies does it decay. "
            "<bookmark mark='q'/> Requiring that the series stops gives the famous result: minus 13.6 electron volts over "
            "n squared."
        ) as vo:
            self.play(Create(ax), FadeIn(rl), FadeIn(ul))
            vo.wait_until("s")
            self.play(Create(c_lo), Create(c_hi), FadeIn(labs[:2]), run_time=2)
            vo.wait_until("e")
            self.play(Create(c_ex), FadeIn(labs[2]))
            vo.wait_until("q")
            self.play(Write(en), Create(enb[0]), FadeIn(sn))
        with self.voiceover(
            "And here's something remarkable. <bookmark mark='t'/> Solve the radial equation numerically for l equals "
            "zero, one and two, and the energies line up: they depend only on n, not on l. That's an accidental "
            "degeneracy, the fingerprint of a hidden symmetry of the one-over-r force that Pauli used in 1926 to solve "
            "hydrogen with matrix mechanics."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3),
                      FadeIn(tn), run_time=2.5)
        assert np.allclose(h["E_l1"][:3], -0.5 / np.arange(2, 5) ** 2, rtol=6e-3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        keys = ["100", "200", "210", "211", "300", "310", "311", "320", "321", "322", "430", "432"]
        avail = {f"{n}{l}{m}" for n, l, m, _ in ORBITALS}
        keys = [k for k in keys if k in avail]
        imgs = Group()
        for k in keys:
            im = orbital_image(f"orb_{k}", height=1.75)
            lab = MathTex(rf"{k[0]},{k[1]},{k[2]}", font_size=24, color=GREY_A).next_to(im, DOWN, buff=0.02)
            imgs.add(Group(im, lab))
        imgs.arrange_in_grid(rows=2, buff=(0.15, 0.25)).move_to(DOWN * 0.15)
        title = MathTex(r"(n,\ \ell,\ m)", font_size=32, color=GREY_A).to_corner(UL, buff=0.4)
        cap = note(r"brightness: probability density, summed along the line of sight; color: phase; each image scaled to "
                   r"its own size ($\sim n^2 a_0$)").to_edge(DOWN, buff=0.2)
        wheel = corner_wheel(corner=UR, buff=0.15, radius=0.24)
        deg = MathTex(r"\text{states with energy } E_n:\ \sum_{\ell = 0}^{n-1}(2\ell + 1) = n^2", font_size=30, color=C.ENERGY)
        deg.next_to(title, RIGHT, buff=0.8).align_to(title, DOWN)
        with self.voiceover(
            "Here are the stationary states themselves, computed from the exact solutions and rendered as glowing "
            "clouds: the brightness is the probability density, the color is the phase. <bookmark mark='o'/> The first "
            "number is the energy level, the second the angular momentum, the third how many times the phase winds "
            "around the vertical axis. <bookmark mark='d'/> For each energy level there are n squared of them. These "
            "aren't orbits; they're stationary waves, and each would only rotate its colors as time passes."
        ) as vo:
            self.play(FadeIn(title), FadeIn(wheel), FadeIn(cap))
            vo.wait_until("o")
            self.play(LaggedStart(*[FadeIn(g) for g in imgs], lag_ratio=0.12), run_time=3)
            vo.wait_until("d")
            self.play(Write(deg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_orbitals(self):
        a = orbital_image("p+", height=2.6)
        b = orbital_image("p-", height=2.6)
        c = orbital_image("px", height=2.6)
        row = Group(a, MathTex(r"-", font_size=60), b, MathTex(r"\propto", font_size=60), c).arrange(RIGHT, buff=0.35)
        row.move_to(UP * 0.4)
        la = MathTex(r"m = -1", font_size=30).next_to(a, DOWN, buff=0.1)
        lb = MathTex(r"m = +1", font_size=30).next_to(b, DOWN, buff=0.1)
        lc = MathTex(r"p_x", font_size=34).next_to(c, DOWN, buff=0.1)
        expl = label(r"two opposite windings interfere: constructively on one side, destructively on the other", font_size=28,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        chem = note(r"the dumbbell-shaped orbitals of chemistry are these real combinations").next_to(expl, DOWN, buff=0.12)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        with self.voiceover(
            "And where do chemistry's dumbbell-shaped p orbitals come from? <bookmark mark='a'/> Take the states with m "
            "equals minus one and plus one: two rings of probability whose phases wind in opposite directions. "
            "<bookmark mark='b'/> Subtract them. On one side the phases agree and the waves add; on the other they "
            "cancel. The result is the dumbbell, a superposition of two angular momenta. Interference again."
        ) as vo:
            self.play(FadeIn(wheel))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la), FadeIn(row[1]), FadeIn(b), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(row[3]), FadeIn(c), FadeIn(lc), FadeIn(expl), FadeIn(chem))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def light(self):
        h = load("hydrogen")
        bal = h["balmer_air"]
        lya = float(h["lyman_a"][0])
        nu = float(h["nu_lya"][0])
        assert np.allclose(np.round(bal), [656, 486, 434, 410]) and abs(lya - 121.6) < 0.05 and abs(nu / 1e15 - 2.47) < 0.005
        cols, accs = h["slosh_col"], h["slosh_acc"]
        g = 2.5 / np.percentile(accs, 99.5)
        k = ValueTracker(0.0)
        img = Raster(lambda v: np.concatenate([tone(cols[int(v) % len(cols)], accs[int(v) % len(cols)], g),
                                               np.full(cols.shape[1:3] + (1,), 255, np.uint8)], axis=2), k, 3.4, 3.4,
                     center=LEFT * 4.3 + UP * 0.6)
        sup = MathTex(r"\tfrac{1}{\sqrt2}\big(\psi_{100}\,e^{-iE_1t/\hbar} + \psi_{210}\,e^{-iE_2t/\hbar}\big)", font_size=30)
        sup.next_to(img, DOWN, buff=0.2)
        f = MathTex(r"\nu", r"=", r"\frac{E_2 - E_1}{h}", r"=", rf"{nu / 1e15:.2f}\times 10^{{15}}\ \text{{Hz}}", font_size=36)
        f.move_to(RIGHT * 2.6 + UP * 2.6)
        f[0].set_color(C.QTIME)
        lam = MathTex(r"\lambda = c/\nu = " + f"{lya:.1f}" + r"\ \text{nm}", font_size=36).next_to(f, DOWN, buff=0.25)
        lyn = label(r"Lyman-$\alpha$, ultraviolet", font_size=26, color=GREY_A).next_to(lam, DOWN, buff=0.12)
        # the visible spectrum: Balmer lines
        strip = Rectangle(width=6.4, height=0.9, stroke_color=GREY_C, stroke_width=1.5, fill_color=BLACK, fill_opacity=1)
        strip.move_to(RIGHT * 2.6 + DOWN * 1.6)
        def xof(l):
            return strip.get_left()[0] + (l - 380) / (720 - 380) * strip.width
        grad = VGroup(*[Rectangle(width=strip.width / 85 + 0.01, height=0.12, stroke_width=0, fill_color=spectrum_color(l),
                                  fill_opacity=0.5).move_to([xof(l), strip.get_bottom()[1] - 0.1, 0]) for l in np.linspace(382, 718, 85)])
        lines = VGroup(*[Line([xof(l), strip.get_bottom()[1] + 0.05, 0], [xof(l), strip.get_top()[1] - 0.05, 0],
                              color=spectrum_color(l), stroke_width=5) for l in bal])
        ll = VGroup(*[MathTex(f"{l:.0f}", font_size=24, color=GREY_A).next_to([xof(l), strip.get_top()[1], 0], UP, buff=0.08)
                      for l in bal])
        tr = VGroup(*[MathTex(rf"{n}\to 2", font_size=22, color=GREY_B)
                      .next_to([xof(l), strip.get_bottom()[1] - 0.2 - 0.3 * (n == 6), 0], DOWN, buff=0.08)
                      for n, l in zip((3, 4, 5, 6), bal)])
        bt = label(r"the Balmer lines (nm, in air): $hc/\lambda = E_n - E_2$", font_size=26).next_to(strip, DOWN, buff=1.0)
        with self.voiceover(
            "Finally, light. Remember the box: a superposition of two energies sloshes back and forth at the difference "
            "frequency. <bookmark mark='s'/> Here's the same thing in hydrogen: the ground state plus the 2 p state. The "
            "electron cloud swings up and down, a tiny oscillating charge, <bookmark mark='n'/> at the Bohr frequency, "
            "E two minus E one over h: about two and a half million billion times per second. <bookmark mark='l'/> An "
            "oscillating charge radiates, at exactly that frequency: 121.6 nanometers, the Lyman alpha line, the "
            "strongest line hydrogen emits."
        ) as vo:
            self.add(img)
            vo.wait_until("s")
            self.play(FadeIn(img), FadeIn(sup), k.animate.set_value(48), run_time=2.5, rate_func=linear)
            vo.wait_until("n")
            self.play(Write(f), k.animate.set_value(96), run_time=2.5, rate_func=linear)
            vo.wait_until("l")
            self.play(Write(lam), FadeIn(lyn), k.animate.set_value(144), run_time=2.5, rate_func=linear)
        with self.voiceover(
            "Every spectral line is a Bohr frequency. <bookmark mark='b'/> Transitions down to the second level give "
            "the visible Balmer lines: the red line at 656 nanometers, then 486, 434 and 410, exactly where "
            "astronomers find them in glowing hydrogen clouds across the sky. The colors of the universe are "
            "differences between eigenvalues."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(strip), FadeIn(grad), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.25), FadeIn(ll), FadeIn(tr),
                      FadeIn(bt), k.animate.set_value(240), run_time=4, rate_func=linear)
        img.clear_updaters()
        self.clear_scene()
