from __future__ import annotations

import numpy as np
from scipy.linalg import eigh_tridiagonal

from explainer import *  # noqa: F403
from videos.quantum2.common import (WaveView, corner_wheel, label, ladder, lframe, load, mtex, note, plain_axes, polyline,
                                    tick_labels, wave_axes, why)
from videos.quantum2.compute import BANDS, kp_f, lattice


class Bands(VoiceoverScene):
    def construct(self):
        self.build()
        self.bloch()
        self.kronig_penney()
        self.filling()

    # ------------------------------------------------------------------
    def build(self):
        b = load("bands")
        bands = b["kp_bands"]
        Ns = BANDS["Ns"]
        ax = plain_axes((0, len(Ns)), (0, 60), 8.4, 5.6).move_to(RIGHT * 2.3 + DOWN * 0.3)
        el = MathTex(r"E", font_size=30, color=C.ENERGY).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        cols = VGroup()
        for i, N in enumerate(Ns):
            E = b[f"levels_{N}"]
            E = E[E < 60]
            g = VGroup(*[Line(ax.c2p(i + 0.12, e), ax.c2p(i + 0.88, e), color=C.ENERGY, stroke_width=2.2 if N < 8 else 1.2) for e in E])
            g.add(MathTex(str(N), font_size=26).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15))
            cols.add(g)
        nl = label(r"wells", font_size=24, color=GREY_B).next_to(ax.c2p(len(Ns) / 2, 0), DOWN, buff=0.6)
        shade = VGroup(*[Rectangle(width=ax.c2p(len(Ns), 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, hi)[1] - ax.c2p(0, lo)[1], 0.02),
                                   stroke_width=0, fill_color=C.ENERGY, fill_opacity=0.12).move_to((ax.c2p(len(Ns) / 2, lo) + ax.c2p(len(Ns) / 2, hi)) / 2)
                         for lo, hi in bands[:3]])
        bl = VGroup(*[label(r"band " + str(k + 1), font_size=22, color=C.ENERGY).next_to(ax.c2p(len(Ns), 0.5 * (lo + hi)), RIGHT, buff=0.1)
                      for k, (lo, hi) in enumerate(bands[:3])])
        # left: the potential and the two lowest states for two wells (computed here)
        x2, V2, h2 = lattice(2)
        d = 1 / h2**2 + V2
        e = np.full(len(x2) - 1, -0.5 / h2**2)
        E2, U2 = eigh_tridiagonal(d, e, select="i", select_range=(0, 1))
        U2 = U2 / np.sqrt(h2)
        pax = wave_axes((x2[0], x2[-1]), (-1.6, 1.6), x_length=4.6, y_length=2.2).move_to(LEFT * 4.3 + UP * 1.0)
        vpot = polyline(pax, x2, V2 / 60 * 1.4 - 0.0, color=C.POTENTIAL, stroke_width=2)
        s_ = U2[:, 0] * np.sign(U2[len(x2) // 3, 0])
        a_ = U2[:, 1] * np.sign(U2[len(x2) // 3, 1])
        ws = polyline(pax, x2, s_ / np.abs(s_).max() * 1.2, color=C.BOSON, stroke_width=3)
        wa = polyline(pax, x2, a_ / np.abs(a_).max() * 1.2, color=C.FERMION, stroke_width=3)
        wl = VGroup(MathTex(r"E = " + f"{E2[0]:.2f}", font_size=22, color=C.BOSON), MathTex(r"E = " + f"{E2[1]:.2f}", font_size=22, color=C.FERMION)
                    ).arrange(RIGHT, buff=0.4).next_to(pax, DOWN, buff=0.15)
        tw = label(r"two wells: even and odd combinations", font_size=22, color=GREY_A).next_to(pax, UP, buff=0.1)
        tun = label(r"split by tunneling\\through the barrier", font_size=22, color=GREY_B).next_to(wl, DOWN, buff=0.25)
        units = note(r"square wells (width $0.7$) and barriers ($0.3$, height $60$); $\hbar = m = 1$; computed").to_corner(DL, buff=0.2)
        with self.voiceover(
            "A solid is a lattice of atoms, each a potential well. Let's build one, well by well. <bookmark mark='a'/> "
            "One well has its own levels. <bookmark mark='b'/> Put a second well beside it, and each level splits in two: "
            "the particle can tunnel between the wells, and the even and odd combinations have slightly different "
            "energies. <bookmark mark='c'/> Three wells: each level becomes three. <bookmark mark='d'/> Eight, sixteen, "
            "thirty-two: each level becomes a band of closely spaced levels, with gaps in between where there are no "
            "states at all. <bookmark mark='e'/> The deepest band is the narrowest, because tunneling through the "
            "barriers is hardest there."
        ) as vo:
            self.play(Create(ax), FadeIn(el), FadeIn(nl), FadeIn(units))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]), Create(pax), Create(vpot), FadeIn(tw))
            self.play(Create(ws), Create(wa), FadeIn(wl), FadeIn(tun))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(cols[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in cols[4:]], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(shade), FadeIn(bl))
            vo.wait_until("e")
            self.play(Indicate(bl[0], color=C.ENERGY))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bloch(self):
        b = load("bands")
        rows = [
            MathTex(r"V(x + a) = V(x)", r"\;\Rightarrow\;", r"[\hat H, \hat T(a)] = 0", font_size=36),
            MathTex(r"\hat T(a)\psi = \lambda\psi,\ |\lambda| = 1", r"\;\Rightarrow\;", r"\psi(x + a) = e^{ika}\,\psi(x)", font_size=36),
            MathTex(r"\psi_k(x)", r"=", r"e^{ikx}\,u_k(x),\qquad u_k(x + a) = u_k(x)", font_size=40),
            MathTex(r"k", r"\sim", r"k + \frac{2\pi}{a}\qquad(\text{the Brillouin zone})", font_size=34),
        ]
        rows[2][2].set_color(C.MOMENTUM)
        whys = [why(rows[0], r"a periodic potential"), why(rows[1], r"a unitary's eigenvalue is a phase"),
                why(rows[2], r"Bloch's theorem (1928)"), why(rows[3], r"$k$ only matters modulo $2\pi/a$")]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-1.4, buff=0.38)
        x, psi = b["bloch_x"], b["bloch_psi"]
        V = b["ring_V"]
        ax = wave_axes((x[0], x[-1]), (0, 2.4), x_length=11.6, y_length=1.9).move_to(DOWN * 2.3)
        pot = polyline(ax, x, V / 60 * 0.4, color=C.POTENTIAL, stroke_width=2)
        wv = WaveView(ax, x, psi, mode="abs", scale=1.6 / np.abs(psi).max())
        cells = VGroup(*[MathTex(str(c + 1), font_size=20, color=GREY_B).next_to(ax.c2p(c + 0.65, 0), DOWN, buff=0.08) for c in range(8)])
        cap = note(r"a computed Bloch state on a ring of 8 cells, $ka = \pi/2$: height $|\psi|$, color = phase (a quarter turn per cell)").next_to(ax, UP, buff=0.12)
        wheel = corner_wheel(corner=DR, buff=0.15, radius=0.25)
        assert abs(float(b["bloch_k"]) - np.pi / 2) < 1e-6
        with self.voiceover(
            "For an infinite lattice, symmetry tells us what the states look like. <bookmark mark='a'/> The potential "
            "repeats with period a, so the Hamiltonian commutes with the translation by one period. <bookmark mark='b'/> "
            "They share eigenstates, and since the translation is unitary, its eigenvalue is a phase: shifting by a "
            "multiplies psi by e to the i k a. <bookmark mark='c'/> So every stationary state is a plane wave, e to the i "
            "k x, times a function with the period of the lattice. That's Bloch's theorem, from 1928. "
            "<bookmark mark='d'/> Here's one: the size repeats from cell to cell, and the color advances by a quarter "
            "turn per cell."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            step(3)
            vo.wait_until("d")
            self.play(Create(ax), Create(pot), FadeIn(wv), FadeIn(cells), FadeIn(cap), FadeIn(wheel))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kronig_penney(self):
        b = load("bands")
        P = BANDS
        Eg, f = b["kp_E"], b["kp_f"]
        sel = Eg <= 60
        ax = plain_axes((0, 60), (-3, 3), 6.0, 3.6).move_to(LEFT * 3.4 + DOWN * 1.2)
        strip = Rectangle(width=6.0, height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1], stroke_width=0, fill_color=C.ENERGY, fill_opacity=0.12).move_to(ax.c2p(30, 0))
        # draw f(E) only where it is on the chart (|f| <= 3), as separate pieces: no flat clipped plateaus
        Es, fs = Eg[sel], f[sel]
        inside = np.abs(fs) <= 3
        cuts = np.flatnonzero(np.diff(inside.astype(int))) + 1
        fc = VGroup(*[polyline(ax, Es[r], fs[r], color=WHITE, stroke_width=3) for r in np.split(np.arange(len(Es)), cuts) if inside[r[0]] and len(r) > 1])
        gaps = [(lo, hi) for lo, hi in zip([0.0] + [float(e) for e in b["kp_bands"][:, 1]], [float(e) for e in b["kp_bands"][:, 0]]) if lo < 60]
        gshade = VGroup(*[Rectangle(width=ax.c2p(min(hi, 60), 0)[0] - ax.c2p(lo, 0)[0], height=3.6, stroke_width=0, fill_color=GREY_D, fill_opacity=0.25)
                          .move_to(ax.c2p((lo + min(hi, 60)) / 2, 0)) for lo, hi in gaps]).set_z_index(-1)
        onl = VGroup(*[polyline(ax, Eg[sel][m], f[sel][m], color=C.ENERGY, stroke_width=5) for m in [(np.abs(f[sel]) <= 1) & (Eg[sel] >= lo) & (Eg[sel] <= hi)
                                                                                                     for lo, hi in b["kp_bands"][:3]]])
        el = MathTex(r"E", font_size=28, color=C.ENERGY).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        pm = VGroup(MathTex(r"+1", font_size=22, color=GREY_B).next_to(ax.c2p(0, 1), LEFT, buff=0.1),
                    MathTex(r"-1", font_size=22, color=GREY_B).next_to(ax.c2p(0, -1), LEFT, buff=0.1))
        fl = MathTex(r"\cos ka = \tfrac12\operatorname{tr}M(E) = f(E)", font_size=30).next_to(ax, UP, buff=0.6)
        M = MathTex(r"\begin{pmatrix}\psi\\ \psi'\end{pmatrix}_{x + a} = M(E)\begin{pmatrix}\psi\\ \psi'\end{pmatrix}_{x}", r",\quad \det M = 1", font_size=30).to_edge(UP, buff=0.3).shift(LEFT * 3.2)
        g0 = gaps[1]
        gap = label(r"$|f| > 1$: no real $k$ --- a gap", font_size=22, color=GREY_A).next_to(ax.c2p((g0[0] + g0[1]) / 2, 3), UP, buff=0.12)
        kp = note(r"Kronig \& Penney (1931): $f(E) = \cos qb\cosh\kappa c + \frac{\kappa^2 - q^2}{2q\kappa}\sin qb\sinh\kappa c$").to_corner(DL, buff=0.2)
        # E(k), reduced zone, with the ring of 8 cells' levels as dots
        a = float(b["a"])
        dax = plain_axes((-np.pi, np.pi), (0, 60), 5.0, 5.6).move_to(RIGHT * 4.0 + DOWN * 0.3)
        kl = MathTex(r"k a", font_size=26, color=C.MOMENTUM).next_to(dax.x_axis.get_end(), RIGHT, buff=0.1)
        ktk = VGroup(MathTex(r"-\pi", font_size=22).next_to(dax.c2p(-np.pi, 0), DOWN, buff=0.1), MathTex(r"\pi", font_size=22).next_to(dax.c2p(np.pi, 0), DOWN, buff=0.1),
                     MathTex(r"0", font_size=22).next_to(dax.c2p(0, 0), DOWN, buff=0.1))
        dk, dE = b["disp_k"], b["disp_E"]
        curves = VGroup()
        for kk, EE in zip(dk, dE):
            if EE.max() > 62:
                EE = np.minimum(EE, 60)
            curves.add(polyline(dax, kk * a, EE, color=C.ENERGY, stroke_width=3), polyline(dax, -kk * a, EE, color=C.ENERGY, stroke_width=3))
        rk, rE = b["ring_k"], b["ring_E"]
        dts = VGroup(*[Dot(dax.c2p(k * a, e), radius=0.06, color=WHITE) for k, e in zip(rk, rE)])
        dl = label(r"dots: a ring of 8 wells,\\ $k = 2\pi n/8a$", font_size=20, color=GREY_A).next_to(dax.c2p(0, 40), UP, buff=0)
        with self.voiceover(
            "Now we can find the bands exactly. <bookmark mark='a'/> Carry a solution across one cell with a two-by-two "
            "transfer matrix. Bloch's condition says its eigenvalues are e to the plus and minus i k a, "
            "<bookmark mark='b'/> so cos k a equals half its trace: an explicit function of the energy, worked out by "
            "Kronig and Penney in 1931. <bookmark mark='c'/> But a cosine lies between minus one and one. Wherever this "
            "function strays outside that strip, there's no real k: those energies are forbidden, the gaps."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(M))
            vo.wait_until("b")
            self.play(Write(fl), Create(ax), FadeIn(el), FadeIn(kp), Create(fc))
            vo.wait_until("c")
            self.play(FadeIn(strip), FadeIn(pm), Create(onl), FadeIn(gshade), FadeIn(gap))
        with self.voiceover(
            "<bookmark mark='a'/> Plot energy against k, and the bands are smooth curves. <bookmark mark='b'/> The levels "
            "of a ring of eight wells, computed separately, sit exactly on them, at the eight allowed values of k."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(dax), FadeIn(kl), FadeIn(ktk), Create(curves), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dts], lag_ratio=0.05), FadeIn(dl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def filling(self):
        b = load("bands")
        dk, dE = b["disp_k"], b["disp_E"]
        a = float(b["a"])

        def panel(center, frac, title, col):
            ax = plain_axes((-np.pi, np.pi), (21.5, 27.5), 4.6, 3.6).move_to(center)
            kk, EE = dk[1], dE[1]
            cv = VGroup(polyline(ax, kk * a, EE, color=C.ENERGY, stroke_width=3), polyline(ax, -kk * a, EE, color=C.ENERGY, stroke_width=3))
            ks = np.linspace(-np.pi, np.pi, 24, endpoint=False) + np.pi / 24
            Ek = np.interp(np.abs(ks), kk * a, EE) if kk[0] < kk[-1] else np.interp(np.abs(ks), (kk * a)[::-1], EE[::-1])
            order = np.argsort(Ek)
            nfill = int(round(frac * len(ks)))
            dts = VGroup(*[Dot(ax.c2p(k, e), radius=0.07, color=col if j in set(order[:nfill]) else GREY_D) for j, (k, e) in enumerate(zip(ks, Ek))])
            t = label(title, font_size=28, color=col).next_to(ax, UP, buff=0.25)
            return VGroup(ax, cv, dts, t)

        L = panel(LEFT * 3.4 + DOWN * 0.3, 0.5, r"1 electron per cell: half full", C.BORN)
        R = panel(RIGHT * 3.4 + DOWN * 0.3, 1.0, r"2 electrons per cell: full", C.BORN)
        ml = label(r"a metal: empty states right above the filled ones", font_size=24, color=C.BORN).next_to(L, DOWN, buff=0.3)
        mr = label(r"an insulator: the next empty states lie across a gap", font_size=24, color=GREY_A).next_to(R, DOWN, buff=0.3)
        top = label(r"each band holds 2 electrons per cell (one of each spin): the exclusion principle again", font_size=26).to_edge(UP, buff=0.35)
        wil = note(r"Wilson (1931); band 2 of the model above, filled at 24 $k$-points").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Now fill the bands with electrons. <bookmark mark='a'/> Each band holds two electrons per cell, one of each "
            "spin. <bookmark mark='b'/> With one electron per cell, a band is half full, and the electrons at the top of "
            "the filled states can move into empty ones with an arbitrarily small push: a metal. <bookmark mark='c'/> "
            "With two per cell, the band is full, and the nearest empty states are across a gap: an insulator. Alan "
            "Wilson worked this out in 1931. That's why copper conducts and diamond doesn't."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(wil))
            vo.wait_until("b")
            self.play(FadeIn(L), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(R), FadeIn(mr))
        self.wait(0.4)
        self.clear_scene()
