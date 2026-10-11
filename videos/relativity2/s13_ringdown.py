from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (clamp_x, label, ladder, load, mtex, note, polyline, redraw, under)
from videos.relativity2.compute import L_SUN

WAVE, HOR, MAT = C.WAVE, C.CURVATURE, C.MATTER


def kerr_area_km2(m_sun, chi):
    """Horizon area 8 pi (GM/c^2)^2 (1 + sqrt(1 - chi^2)) in km^2."""
    Mk = m_sun * L_SUN / 1000
    return 8 * math.pi * Mk * Mk * (1 + math.sqrt(1 - chi * chi))


class Ringdown(VoiceoverScene):
    def construct(self):
        self.q = load("qnm")
        self.barrier()
        self.ringing()
        self.frequency()
        self.data()
        self.area_theorem()
        self.gw250114()

    # ------------------------------------------------------------------
    def barrier(self):
        q = self.q
        x, V = q["rw_x"], q["rw_V"]
        rows = [
            mtex(r"\frac{\partial^2\psi}{\partial t^2} - \frac{\partial^2\psi}{\partial r_*^2} + V(r)\,\psi", r"=", r"0", font_size=40),
            mtex(r"V(r)", r"=", r"\Big(1 - \frac{2M}{r}\Big)\Big(\frac{\ell(\ell+1)}{r^2} - \frac{6M}{r^3}\Big)", font_size=40),
        ]
        whys = [note(r"small ripples of a Schwarzschild hole (Regge \& Wheeler, 1957), in the tortoise coordinate"),
                note(r"for gravitational waves of angular pattern $\ell$; we use $\ell = 2$")]
        rows[0][0].set_color(WAVE)
        under(rows, whys, -0.4)
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-0.4, buff=0.6)
        ax = Axes(x_range=[-40, 60, 20], y_range=[0, 0.16, 0.04], x_length=8.5, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [-40, -20, 20, 40, 60]}).move_to([0, -2.0, 0])
        ok = (x > -40) & (x < 60)
        cur = polyline(ax, x[ok], V[ok], color=HOR, stroke_width=4)
        xl = label(r"$r_*/M$", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        k = int(np.argmax(V))
        rr = np.linspace(2.5, 4.5, 200001)
        r_peak = float(rr[np.argmax((1 - 2 / rr) * (6 / rr**2 - 6 / rr**3))])  # the exact peak of V for l = 2
        assert abs(r_peak - 3.28) < 0.01
        pk = label(r"peak near $r \approx 3.3M$, close to the photon sphere ($3M$)", font_size=22, color=HOR).next_to(
            ax.c2p(x[k], V[k]), UP, buff=0.1)
        lft = label(r"$\leftarrow$ horizon", font_size=20, color=GREY_B).next_to(ax.c2p(-40, 0.02), RIGHT, buff=0.05)
        rgt = label(r"far away $\rightarrow$", font_size=20, color=GREY_B).next_to(ax.c2p(60, 0.02), LEFT, buff=0.05)
        with self.voiceover(
            "When two black holes merge, the result is a single, distorted black hole, which settles down by ringing, "
            "like a struck bell. <bookmark mark='a'/> Small ripples of a black hole obey a wave equation in the tortoise "
            "coordinate, found by Tullio Regge and John Wheeler in 1957, <bookmark mark='b'/> with a potential barrier. "
            "<bookmark mark='c'/> The barrier peaks just outside the photon sphere, where light can orbit: waves near "
            "the hole are partly trapped there, leaking slowly inward to the horizon and outward to us."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(lft), FadeIn(rgt))
            self.play(Create(cur), FadeIn(pk))
        self.barrier_plot = VGroup(ax, cur, xl, lft, rgt, pk)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ringing(self):
        q = self.q
        x, V, snaps, st_ = q["rw_x"], q["rw_V"], q["rw_snaps"], q["rw_snap_t"]
        ot, ob = q["rw_obs_t"], q["rw_obs"]
        ax = Axes(x_range=[-60, 120, 20], y_range=[-1.1, 1.1, 0.5], x_length=11.5, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([0, 2.0, 0])
        ok = (x > -60) & (x < 120)
        vline = polyline(ax, x[ok], V[ok] / V.max() * 0.8, color=HOR, stroke_width=2.5).set_stroke(opacity=0.7)
        obs = DashedLine(ax.c2p(60, -1.1), ax.c2p(60, 1.1), color=GREY_B, stroke_width=2)
        obl = label(r"observer", font_size=20, color=GREY_B).next_to(ax.c2p(60, 1.1), UP, buff=0.05)
        k = ValueTracker(0.0)

        def psi():
            i = int(k.get_value() * (len(st_) - 1))
            return polyline(ax, x[ok], np.clip(snaps[i][ok], -1.1, 1.1), color=WAVE, stroke_width=3)

        P = redraw(psi)
        # observer's signal, log scale
        ax2 = Axes(x_range=[0, 420, 100], y_range=[-12, 0, 2], x_length=7.0, y_length=3.0, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [100, 200, 300, 400]},
                   y_axis_config={"numbers_to_include": [-10, -8, -6, -4, -2]}).move_to([-2.2, -1.7, 0])
        lab2 = label(r"$\log_{10}|\psi|$ at the observer vs $t/M$", font_size=22).next_to(ax2, UP, buff=0.1)

        def trace():
            tmax = st_[int(k.get_value() * (len(st_) - 1))]
            m = (ot <= tmax) & (ot > 1)
            if m.sum() < 3:
                return VGroup()
            return polyline(ax2, ot[m], np.log10(np.abs(ob[m]) + 1e-14), color=WAVE, stroke_width=2.5)

        T = redraw(trace)
        A, wr, wi, ph, t0 = q["rw_fit"]
        tt = np.linspace(t0, t0 + 120, 100)
        env = polyline(ax2, tt, np.log10(abs(A) * np.exp(-wi * (tt - t0))), color=C.LIGHT, stroke_width=2.5)
        envl = label(r"exponential decay: the ringing", font_size=20, color=C.LIGHT).next_to(ax2.c2p(t0 + 110, -5.6), RIGHT, buff=0.1)
        tail = label(rf"then a power-law tail, $|\psi| \sim t^{{{float(q['tail_slope']):.1f}}}$", font_size=20, color=GREY_A).next_to(
            ax2.c2p(330, -9.0), UP, buff=0.05)
        cap = note(r"computed: the Regge--Wheeler equation solved on a grid, from an ingoing Gaussian pulse").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Let's watch it happen. <bookmark mark='a'/> Send a pulse of gravitational waves toward the barrier, and "
            "solve the equation numerically. <bookmark mark='b'/> Part of the pulse crosses the barrier and falls into "
            "the hole. Part bounces back, and what comes back isn't a copy of the pulse: it's a ringing, at a definite "
            "frequency, dying away. <bookmark mark='c'/> On a logarithmic scale, the ringing's envelope is a straight "
            "line: an exponential decay, until a faint power-law tail takes over."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), Create(vline), Create(obs), FadeIn(obl), FadeIn(cap))
            self.add(P)
            vo.wait_until("b")
            self.add(T)
            self.play(Create(ax2), FadeIn(lab2))
            self.play(k.animate.set_value(0.45), run_time=vo.until("c"), rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(1.0), run_time=4, rate_func=linear)
            self.play(Create(env), FadeIn(envl), FadeIn(tail))
        P.clear_updaters()
        T.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def frequency(self):
        q = self.q
        wS = q["w_schw"]
        A, wr, wi, ph, t0 = q["rw_fit"]
        eik = q["w_eik"]
        assert abs(wr - 0.3737) < 0.005 and abs(wi - 0.0890) < 0.002
        rows = VGroup(
            label(r"the ringing of a Schwarzschild hole ($\ell = 2$, fundamental mode):", font_size=28),
            mtex(r"\text{our simulation:}\quad M\omega = " + f"{wr:.4f} - {wi:.4f}\\,i", font_size=36, color=WAVE),
            mtex(r"\text{Leaver's continued fraction:}\quad M\omega = " + f"{wS[0]:.5f} - {-wS[1]:.5f}\\,i", font_size=36, color=WAVE),
            mtex(r"\text{light orbiting at } 3M:\quad M\omega \approx \frac{\ell + \frac12}{\sqrt{27}} - \frac{i}{2\sqrt{27}} = "
                 + f"{eik[0]:.2f} - {-eik[1]:.3f}\\,i", font_size=34, color=C.LIGHT),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.4)
        hair = VGroup(
            label(r"Frequency and damping depend only on the final mass and spin:", font_size=28, color=HOR),
            label(r"black-hole spectroscopy, a direct test of ``no hair''", font_size=28, color=HOR),
        ).arrange(DOWN, buff=0.1).next_to(rows, DOWN, buff=0.5)
        gw = VGroup(
            label(r"GW150914's remnant ($68\,M_\odot$ at Earth, spin $0.67$):", font_size=28),
            mtex(rf"f = {float(q['gw150914_f']):.0f}\ \text{{Hz}},\qquad \tau = {float(q['gw150914_tau']) * 1e3:.1f}\ \text{{ms}}",
                 font_size=38, color=WAVE),
            note(r"Kerr modes from Leaver's method (the \texttt{qnm} package), checked against our Schwarzschild value"),
        ).arrange(DOWN, buff=0.15).next_to(hair, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Fitting the ringing in our simulation gives a frequency and a damping rate. "
            "<bookmark mark='b'/> They match, to a fraction of a percent, the exact quasinormal frequency, computed by "
            "a completely different method, Edward Leaver's continued fraction from 1985. <bookmark mark='c'/> And "
            "there's a simple picture behind it: the ringing is waves trapped near the photon sphere, so its frequency "
            "is roughly the orbital frequency of light there, and it leaks away at the rate light orbits there are "
            "unstable. <bookmark mark='d'/> The crucial point: the frequencies depend only on the final mass and spin. "
            "Measure them, and you test whether the remnant really is a Kerr black hole with no hair. "
            "<bookmark mark='e'/> For the black hole left by LIGO's first detection, the main tone is at about two "
            "hundred and fifty hertz, dying away in four milliseconds."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(hair, lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(gw, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def data(self):
        q = self.q
        t, H = q["gw_t"], q["gw_H"]
        tp = float(q["gw_peak"])
        coef = q["gw_coef"]
        f0, tau0 = float(q["gw150914_f"]), float(q["gw150914_tau"])
        assert float(q["gw_resid"]) < 0.4
        m = (t > tp - 0.06) & (t < tp + 0.03)
        ax = Axes(x_range=[-60, 30, 10], y_range=[-1.2, 1.2, 0.5], x_length=11.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [-60, -40, -20, 0, 20]}).move_to([0, -0.4, 0])
        sc = np.max(np.abs(H[m]))
        data = polyline(ax, (t[m] - tp) * 1e3, H[m] / sc, color=WHITE, stroke_width=2.5)
        tt = np.linspace(tp + 0.003, tp + 0.03, 300)
        model = (coef[0] * np.exp(-(tt - tp) / tau0) * np.cos(2 * np.pi * f0 * (tt - tp))
                 + coef[1] * np.exp(-(tt - tp) / tau0) * np.sin(2 * np.pi * f0 * (tt - tp)))
        mod = polyline(ax, (tt - tp) * 1e3, model / sc, color=WAVE, stroke_width=4)
        xl = label(r"ms after the peak", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        hdr = label(r"LIGO Hanford, GW150914 (whitened, 35--350 Hz): the last cycles", font_size=28).to_edge(UP, buff=0.4)
        leg = VGroup(label(r"data", font_size=24),
                     label(rf"ringdown with $f = {f0:.0f}$ Hz and $\tau = {tau0 * 1e3:.1f}$ ms fixed by theory", font_size=24, color=WAVE),
                     label(r"(only an amplitude and a phase fitted, from 3 ms after the peak)", font_size=20, color=GREY_A)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DL, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Here are the last cycles of LIGO's first signal, the real data. <bookmark mark='b'/> "
            "After the peak, lay on a ringing with the frequency and damping time predicted for the final black hole, "
            "fitting only its amplitude and phase. The signal is faint and noisy here, but the tail end of the "
            "collision rings just as a Kerr black hole should."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr), Create(ax), FadeIn(xl))
            self.play(Create(data), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(mod), FadeIn(leg[1:]), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def area_theorem(self):
        rows = [
            mtex(r"\frac{d\theta}{d\lambda}", r"\le", r"-\tfrac12\theta^2", font_size=42),
            mtex(r"\theta < 0", r"\Rightarrow", r"\text{generators meet within } \lambda = 2/|\theta|", font_size=40),
            mtex(r"\theta", r"\ge", r"0\quad\Rightarrow\quad \frac{dA}{d\lambda} \ge 0", font_size=44),
        ]
        whys = [
            note(r"Raychaudhuri, for the light rays that make up the horizon (null energy condition)"),
            note(r"but light rays that meet leave the horizon, and its generators never leave it"),
            note(r"so the horizon's light rays never converge: its area never decreases (Hawking, 1971)"),
        ]
        for r in rows:
            r[0].set_color(C.EXPANSION)
        rows[2][2].set_color(HOR)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.8, buff=0.75)
        bound = VGroup(
            label(r"merging two non-spinning holes of mass $m$: \ $16\pi M_f^2 \geq 2\times 16\pi m^2$", font_size=26),
            label(r"at most $1 - 1/\sqrt2 = 29\%$ of the mass can be radiated (GW150914: about 5\%)", font_size=26, color=WAVE),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1971, Stephen Hawking proved that this kind of collision can only make black holes bigger. "
            "<bookmark mark='a'/> The horizon is made of light rays, and Raychaudhuri's equation applies to them. "
            "<bookmark mark='b'/> If they ever started converging, they'd meet within a finite distance. But light rays "
            "that meet leave the horizon, and the horizon's light rays never leave it. <bookmark mark='c'/> So they "
            "never converge, and the horizon's area never decreases. <bookmark mark='d'/> That limits how much energy "
            "a merger can radiate: for two equal non-spinning holes, at most twenty-nine percent of their mass. "
            "LIGO's first event radiated about five percent, three solar masses' worth, in a fifth of a second."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(bound, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def gw250114(self):
        q = self.q
        A1, A2 = kerr_area_km2(33.6, 0.0), kerr_area_km2(32.2, 0.0)
        Af = kerr_area_km2(62.7, 0.68)
        Ai = A1 + A2
        assert abs(Ai / 1e5 - 2.37) < 0.01 and abs(Af / 1e5 - 3.73) < 0.01
        f_pred, tau_pred = float(q["gw250114_f"]), float(q["gw250114_tau"])
        assert abs(f_pred - 248.6) < 0.5
        hdr = VGroup(label(r"GW250114: the loudest signal yet (14 January 2025)", font_size=34),
                     label(r"$33.6 + 32.2\,M_\odot \rightarrow 62.7\,M_\odot$, spin $0.68$, \ signal-to-noise ratio $\approx 80$",
                           font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        s = 0.0042  # screen units per sqrt(km^2)
        c1 = Circle(radius=s * math.sqrt(A1 / math.pi), color=HOR, fill_color=HOR, fill_opacity=0.3).move_to([-4.6, -0.2, 0])
        c2 = Circle(radius=s * math.sqrt(A2 / math.pi), color=HOR, fill_color=HOR, fill_opacity=0.3).move_to([-3.2, -0.2, 0])
        cf = Circle(radius=s * math.sqrt(Af / math.pi), color=HOR, fill_color=HOR, fill_opacity=0.3).move_to([-0.4, -0.2, 0])
        arr = Arrow([-2.4, -0.2, 0], [-1.7, -0.2, 0], buff=0, color=GREY_B)
        la = label(rf"${Ai / 1e5:.2f}\times10^5$ km$^2$", font_size=26, color=HOR).next_to(VGroup(c1, c2), DOWN, buff=0.35)
        lf = label(rf"${Af / 1e5:.2f}\times10^5$ km$^2$", font_size=26, color=HOR).next_to(cf, DOWN, buff=0.35)
        cap = note(r"horizon areas $8\pi M^2(1 + \sqrt{1 - \chi^2})$ from the median masses and spins (circles to scale)").next_to(la, DOWN, buff=0.35).align_to(c1, LEFT)
        res = VGroup(
            label(r"area increase confirmed at $4.4\sigma$", font_size=28, color=HOR),
            label(r"(LIGO--Virgo--KAGRA, PRL 2025)", font_size=22, color=GREY_A),
            label(r"main ringdown tone:", font_size=26),
            mtex(rf"\text{{predicted }} {f_pred:.0f}\ \text{{Hz}},\ {tau_pred * 1e3:.1f}\ \text{{ms}}", font_size=32, color=WAVE),
            mtex(r"\text{measured } 252 \pm 5\ \text{Hz},\ 4.1 \pm 0.4\ \text{ms}", font_size=32),
            label(r"plus a first overtone, detected at $4.1\sigma$", font_size=24),
        ).arrange(DOWN, buff=0.15).move_to([4.2, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In January 2025, LIGO caught the loudest black-hole merger yet, two holes of about "
            "thirty-three solar masses each. <bookmark mark='b'/> From the inspiral, you can infer the areas of the two "
            "horizons before the merger; from the ringdown, the area after. Before: two hundred and thirty-seven "
            "thousand square kilometers. After: three hundred and seventy-three thousand. <bookmark mark='c'/> The "
            "collaboration found the area increased, with a confidence of four point four sigma: Hawking's area "
            "theorem, tested on real black holes. <bookmark mark='d'/> And the ringdown was loud enough to hear the "
            "main tone and its first overtone, at the frequencies a Kerr black hole of that mass and spin should have."
        ) as vo:
            self.play(FadeIn(hdr, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(GrowFromCenter(c1), GrowFromCenter(c2), FadeIn(la))
            self.play(GrowArrow(arr), GrowFromCenter(cf), FadeIn(lf), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(res[:2], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(res[2:], lag_ratio=0.2))
        with self.voiceover(
            "An area that can only grow. That's a lot like another quantity in physics that can only grow: entropy. "
            "Is the resemblance a coincidence?"
        ):
            pass
        self.clear_scene()
