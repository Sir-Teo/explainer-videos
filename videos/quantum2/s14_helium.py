from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (label, ladder, lframe, load, mtex, note, phase_img, plain_axes, polyline, tick_labels, why)

BLOCK = {"s": "#7DD3FC", "p": "#FCA5A5", "d": "#BEF264", "f": "#FDE68A"}


def block(Z: int) -> str:
    if Z in (1, 2, 3, 4, 11, 12, 19, 20, 37, 38, 55, 56):
        return "s"
    if 57 <= Z <= 70:
        return "f"
    if 21 <= Z <= 30 or 39 <= Z <= 48 or 71 <= Z <= 80:
        return "d"
    return "p"


class Helium(VoiceoverScene):
    def construct(self):
        self.naive()
        self.first_order()
        self.variational()
        self.excited()
        self.periodic()

    # ------------------------------------------------------------------
    def naive(self):
        h = load("helium")
        H = MathTex(r"\hat H", r"=", r"-\tfrac12\nabla_1^2 - \tfrac12\nabla_2^2 - \frac{2}{r_1} - \frac{2}{r_2}", r"+", r"\frac{1}{r_{12}}", font_size=44).to_edge(UP, buff=0.6)
        H[4].set_color(C.PERTURB)
        au = note(r"atomic units: lengths in Bohr radii, energies in hartrees ($27.21$ eV)").next_to(H, DOWN, buff=0.15)
        r1 = MathTex(r"\text{drop } 1/r_{12}:\quad E = 2\times\big(-\tfrac{Z^2}{2}\big) = -4\ \text{hartree} = " + f"{float(h['E_naive']):.1f}" + r"\ \text{eV}", font_size=34).move_to(UP * 0.4)
        r2 = MathTex(r"\text{measured: } " + f"{float(h['E_exp']):.1f}" + r"\ \text{eV}", font_size=34, color=WHITE).next_to(r1, DOWN, buff=0.4)
        assert abs(float(h["E_naive"]) + 108.8) < 0.1 and abs(float(h["E_exp"]) + 79.0) < 0.05
        sp = label(r"both electrons in 1s: the spatial part is symmetric, so the spins pair up (a singlet)", font_size=24, color=GREY_B).next_to(r2, DOWN, buff=0.6)
        with self.voiceover(
            "Helium has two electrons, <bookmark mark='a'/> and the term that couples them, their repulsion, one over r "
            "one two, makes it impossible to solve exactly. <bookmark mark='b'/> Ignore that term, and each electron "
            "sits in a hydrogen-like orbit around a nucleus of charge two: an energy of minus 108.8 electron volts. "
            "<bookmark mark='c'/> The measured value is minus 79.0. The repulsion matters."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(H), FadeIn(au))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(sp))
            vo.wait_until("c")
            self.play(FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def first_order(self):
        h = load("helium")
        # Newton's shell theorem picture
        o = LEFT * 4.0 + DOWN * 0.3
        shells = VGroup(*[Circle(radius=r, color=C.BORN, stroke_width=2).set_stroke(opacity=0.25 + 0.5 * np.exp(-r)).move_to(o) for r in np.linspace(0.3, 2.2, 9)])
        inside = Dot(o + RIGHT * 0.6 + UP * 0.2, color=C.XPOS)
        outside = Dot(o + RIGHT * 2.6 + UP * 0.9, color=C.XPOS)
        il = label(r"inside a shell:\\ no force", font_size=22, color=GREY_A).next_to(o, DOWN, buff=2.4)
        ol = label(r"outside: as if all\\ at the center", font_size=22, color=GREY_A).next_to(outside, UP, buff=0.1)
        rows = [
            MathTex(r"E^1", r"=", r"\Big\langle \frac{1}{r_{12}}\Big\rangle = \iint \frac{\rho(r_1)\,\rho(r_2)}{\max(r_1, r_2)}\,dr_1\,dr_2", font_size=34),
            MathTex(r"E^1", r"=", r"\frac58 Z\ \text{hartree} = " + f"{5 / 8 * 2 * 27.211386:.1f}" + r"\ \text{eV}", font_size=38),
            MathTex(r"E", r"\approx", r"-108.8 + 34.0 = " + f"{float(h['E_first']):.1f}" + r"\ \text{eV}", font_size=38),
        ]
        rows[1][2].set_color(C.PERTURB)
        whys = [why(rows[0], r"shell theorem: 6 dimensions $\to$ 2"), why(rows[1], r"exact (checked symbolically)"), why(rows[2], r"now too high")]
        for r in rows:
            r.shift(RIGHT * 2.5)
        step = ladder(self, rows, whys, keep=3, top=2.2, x=0.4, buff=0.6)
        with self.voiceover(
            "First-order perturbation theory says: average the repulsion over the unperturbed state. "
            "<bookmark mark='a'/> Each electron is a spherical cloud, and by Newton's shell theorem, a spherical shell of "
            "charge acts like a point charge at its center from outside, and like nothing at all from inside. "
            "<bookmark mark='b'/> That reduces a six-dimensional integral to a two-dimensional one, "
            "<bookmark mark='c'/> and the answer is exactly five eighths of Z, in atomic units: 34 electron volts. "
            "<bookmark mark='d'/> So the estimate becomes minus 74.8: much better, but now too high."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in shells], lag_ratio=0.1), FadeIn(inside), FadeIn(outside), FadeIn(il), FadeIn(ol))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variational(self):
        h = load("helium")
        p1 = MathTex(r"\ket{\chi} = \sum_n c_n\ket{n}", r"\;\Rightarrow\;", r"\bra{\chi}\hat H\ket{\chi} = \sum_n |c_n|^2 E_n \;\ge\; E_0", font_size=34).to_edge(UP, buff=0.35)
        p1[2].set_color(C.APPROX)
        pv = label(r"every trial state gives an upper bound: the variational principle", font_size=26, color=C.APPROX).next_to(p1, DOWN, buff=0.15)
        tr = MathTex(r"\chi = \phi_{1s}^{(\zeta)}(r_1)\,\phi_{1s}^{(\zeta)}(r_2)", r"\;\Rightarrow\;", r"E(\zeta) = \zeta^2 - 2Z\zeta + \tfrac58\zeta", font_size=32).next_to(pv, DOWN, buff=0.3)
        zz, Ez = h["var_zeta"], h["var_E"]
        ax = plain_axes((1.0, 2.4), (-81, -66), 6.2, 3.5).move_to(LEFT * 2.6 + DOWN * 1.3)
        fr = lframe(ax)
        tks = VGroup(tick_labels(ax, xs=(1.2, 1.6, 2.0)), tick_labels(ax, ys=(-80, -75, -70)))
        zl = MathTex(r"\zeta", font_size=30).next_to(fr[0].get_end(), RIGHT, buff=0.1)
        el = MathTex(r"E\ (\text{eV})", font_size=26).next_to(fr[1].get_end(), LEFT, buff=0.15)
        cur = polyline(ax, zz, np.maximum(Ez, -81), color=C.APPROX, stroke_width=4)
        zmin = 27 / 16
        dmin = Dot(ax.c2p(zmin, float(h["E_var"])), radius=0.08, color=C.APPROX)
        dl = MathTex(r"\zeta = \tfrac{27}{16}:\ " + f"{float(h['E_var']):.2f}" + r"\ \text{eV}", font_size=26, color=C.APPROX).next_to(dmin, DOWN, buff=0.15)
        lines = VGroup()
        levels = [(float(h["E_first"]), r"\text{first order}", C.PERTURB), (float(h["E_var"]), r"\text{variational}", C.APPROX),
                  (float(h["E_swave"]), r"\text{numerical, }s\text{-waves only}", C.BOSON), (float(h["E_exp"]), r"\text{measured}", WHITE)]
        assert abs(levels[1][0] + 77.49) < 0.01 and abs(levels[2][0] + 78.33) < 0.02
        lad = VGroup()
        for E, name, col in levels:
            lad.add(VGroup(MathTex(name + r":\ " + f"{E:.2f}" + r"\ \text{eV}", font_size=28, color=col)))
        lad.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.6 + DOWN * 1.5)
        nv = note(r"$-108.8$ eV without the repulsion; the screening charge $\zeta < 2$: each electron partly hides the nucleus").to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "We can do better with the variational principle. <bookmark mark='a'/> Expand any trial state in the true "
            "eigenstates: its average energy is a weighted average of the eigenvalues, so it can never be below the "
            "lowest one. Every guess gives an upper bound, and the best guess in a family is the one with the lowest "
            "energy. <bookmark mark='b'/> Let each electron see an effective charge zeta instead of two, because each "
            "electron partly screens the nucleus from the other. <bookmark mark='c'/> The energy is a parabola in zeta, "
            "with its minimum at twenty-seven sixteenths, giving minus 77.5 electron volts."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(p1), FadeIn(pv))
            vo.wait_until("b")
            self.play(Write(tr), FadeIn(nv))
            vo.wait_until("c")
            self.play(Create(fr), FadeIn(tks), FadeIn(zl), FadeIn(el), Create(cur))
            self.play(FadeIn(dmin), FadeIn(dl), FadeIn(lad[0]), FadeIn(lad[1]))
        with self.voiceover(
            "<bookmark mark='a'/> A computer solution of the full two-electron equation, keeping only the spherically "
            "symmetric part of the repulsion, gets to minus 78.3. <bookmark mark='b'/> With everything included, theory "
            "and experiment agree at minus 79.0."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(lad[2]))
            vo.wait_until("b")
            self.play(FadeIn(lad[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def excited(self):
        h = load("helium")
        r = h["tp_r"]
        R = float(r[-1])
        sing, trip = h["tp_sing"], h["tp_trip"]

        def sq(m, center, size=3.6):
            img = phase_img(m[::-1].astype(complex), height=size, width=size, gamma=0.7).move_to(center)
            fr = Rectangle(width=size, height=size, stroke_color=GREY_C, stroke_width=1.5).move_to(center)
            dg = DashedLine(fr.get_corner(DL), fr.get_corner(UR), color=GREY_A, stroke_width=1.5, dash_length=0.08)
            return Group(img, fr, dg, MathTex(r"r_1", font_size=24, color=C.XPOS).next_to(fr, DOWN, buff=0.08),
                         MathTex(r"r_2", font_size=24, color=C.XPOS).next_to(fr, LEFT, buff=0.08))

        a, b = sq(sing, LEFT * 3.3 + DOWN * 0.5), sq(trip, RIGHT * 1.0 + DOWN * 0.5)
        la = label(r"spins opposite (singlet):\\ space symmetric", font_size=24, color=C.BOSON).next_to(a, UP, buff=0.2)
        lb = label(r"spins parallel (triplet):\\ space antisymmetric", font_size=24, color=C.FERMION).next_to(b, UP, buff=0.2)
        tl = label(r"helium 1s2s, computed on the plane of the two radii ($0$ to $" + f"{R:.0f}" + r"\,a_0$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        sm, se = float(h["split_model"]), float(h["split_exp"])
        assert abs(sm - 0.818) < 0.005 and abs(se - 0.796) < 0.001
        lv = VGroup(
            MathTex(r"E(^1S) - E(^3S)", font_size=30),
            MathTex(r"\text{computed: } " + f"{sm:.2f}" + r"\ \text{eV}", font_size=30, color=C.BOSON),
            MathTex(r"\text{measured: } " + f"{se:.2f}" + r"\ \text{eV}", font_size=30),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 5.0 + DOWN * 0.3)
        hund = label(r"the origin of Hund's rule and of ferromagnetism: an energy that depends on spin, from electric repulsion alone",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Now the excited state with one electron in 1s and one in 2s. <bookmark mark='a'/> Here the two electrons "
            "can have opposite spins or parallel ones. The total wavefunction must be antisymmetric, so parallel spins "
            "force an antisymmetric spatial part. <bookmark mark='b'/> Here are both states, computed on the plane of the "
            "two radii, r one and r two. <bookmark mark='c'/> The triplet's wavefunction vanishes along the diagonal: the "
            "electrons keep apart, repel each other less, and have lower energy. <bookmark mark='d'/> The computed "
            "splitting is 0.82 electron volts; the measured one is 0.80. <bookmark mark='e'/> That's the origin of "
            "Hund's rule, and of magnetism in materials: an energy that depends on spin, although no magnetic force is "
            "involved."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(b))
            vo.wait_until("c")
            self.play(Indicate(b[2], color=C.FERMION))
            vo.wait_until("d")
            self.play(FadeIn(lv))
            vo.wait_until("e")
            self.play(FadeIn(hund))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def periodic(self):
        h = load("helium")
        Z, E, sym = h["ion_Z"], h["ion_E"], h["ion_sym"]
        ax = plain_axes((0, 88), (0, 26), 11.6, 5.0).move_to(DOWN * 0.45)
        tks = VGroup(tick_labels(ax, xs=(1, 10, 20, 30, 40, 50, 60, 70, 80, 86)), tick_labels(ax, ys=(5, 10, 15, 20, 25)))
        zl = MathTex(r"Z", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        el = label(r"energy to remove the outermost electron (eV)", font_size=24).next_to(ax.y_axis.get_end(), UP, buff=0.1).shift(RIGHT * 2.2)
        line = polyline(ax, Z, E, color=GREY_C, stroke_width=1.5)
        pts = VGroup(*[Dot(ax.c2p(z, e), radius=0.045, color=BLOCK[block(int(z))]) for z, e in zip(Z, E)])
        noble = VGroup(*[label(sym[z - 1], font_size=24, color=WHITE).next_to(ax.c2p(z, E[z - 1]), UP, buff=0.08) for z in (2, 10, 18, 36, 54, 86)])
        alk = VGroup(*[label(sym[z - 1], font_size=22, color=BLOCK["s"]).next_to(ax.c2p(z, E[z - 1]), DOWN, buff=0.08) for z in (3, 11, 19, 37, 55)])
        leg = VGroup(*[VGroup(Dot(radius=0.06, color=c), label(k + r"-block", font_size=20, color=c)).arrange(RIGHT, buff=0.08) for k, c in BLOCK.items()]
                     ).arrange(RIGHT, buff=0.35)
        src = note(r"data: NIST Atomic Spectra Database (first ionization energies)").to_corner(DL, buff=0.2)
        fill = label(r"1s $\vert$ 2s 2p $\vert$ 3s 3p $\vert$ 4s 3d 4p $\vert$ 5s 4d 5p $\vert$ 6s 4f 5d 6p", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        leg.next_to(fill, DOWN, buff=0.2).align_to(ax, RIGHT)
        with self.voiceover(
            "With more electrons, <bookmark mark='a'/> the exclusion principle forces them into higher and higher "
            "orbitals, filling shells. <bookmark mark='b'/> Here is the energy needed to remove the outermost electron, "
            "for every element up to radon, from NIST's measurements. <bookmark mark='c'/> It peaks at the noble gases, "
            "where a shell has just been completed, <bookmark mark='d'/> and plunges at the alkali metals, whose one extra "
            "electron starts a new shell, far out and well screened. <bookmark mark='e'/> The periodic table is the "
            "exclusion principle, written in chemistry."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fill))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(tks), FadeIn(zl), FadeIn(el), FadeIn(src), FadeIn(leg))
            self.play(Create(line), LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.02), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in noble], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n) for n in alk], lag_ratio=0.2))
            vo.wait_until("e")
        self.wait(0.4)
        self.clear_scene()
