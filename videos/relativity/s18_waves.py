from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import boxed, label, ladder, load, mtex, note, polyline, rgba, sci, stack

SNAP = Path(__file__).resolve().parent / "data" / "gw150914.json"


class Waves(VoiceoverScene):
    def construct(self):
        self.linearize()
        self.polarizations()
        self.sources()
        self.chirp()
        self.data()

    # ------------------------------------------------------------------
    def linearize(self):
        title = label(r"Weak gravity, linearized", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"g_{\mu\nu}", r"=", r"\eta_{\mu\nu} + h_{\mu\nu},\qquad |h_{\mu\nu}| \ll 1", font_size=40),
            mtex(r"\bar h_{\mu\nu}", r"=", r"h_{\mu\nu} - \tfrac12\eta_{\mu\nu}h,\qquad \partial^\mu\bar h_{\mu\nu} = 0", font_size=40),
            mtex(r"G_{\mu\nu}", r"=", r"-\tfrac12\,\Box\,\bar h_{\mu\nu}", font_size=40),
            mtex(r"\Box\,\bar h_{\mu\nu}", r"=", r"-\frac{16\pi G}{c^4}\,T_{\mu\nu}", font_size=44),
            mtex(r"\Big(-\frac{1}{c^2}\frac{\partial^2}{\partial t^2} + \nabla^2\Big)\bar h_{\mu\nu}", r"=", r"0", font_size=44),
        ]
        whys = [
            note(r"a small ripple on flat spacetime; keep terms linear in $h$", font_size=22),
            note(r"trace-reversed $h$; choose coordinates (Lorenz gauge) to simplify", font_size=22),
            note(r"the Einstein tensor, to first order in $h$", font_size=22),
            note(r"Einstein's equation, linearized", font_size=22),
            note(r"in empty space: a wave equation, with speed $c$", font_size=22),
        ]
        rows[0][0].set_color(C.METRIC)
        rows[2][0].set_color(C.CURVATURE)
        rows[3][2].set_color(C.MATTER)
        rows[4][0].set_color(C.WAVE)
        x0 = -0.6
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.4, x=x0, buff=0.62)
        with self.voiceover(
            "Remember the problem with Newton's gravity: it acts instantly. Does Einstein's theory fix that? "
            "<bookmark mark='a'/> Look at weak gravity: the metric is the flat one plus a small ripple, h, and we keep "
            "only terms linear in h. <bookmark mark='b'/> There's freedom in choosing coordinates, and a clever choice, "
            "applied to the trace-reversed ripple, simplifies things enormously. <bookmark mark='c'/> The Einstein tensor "
            "becomes just minus one half the wave operator, box, acting on h bar."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> So Einstein's equation becomes box h bar equals minus sixteen pi G over c to the fourth "
            "times T. <bookmark mark='e'/> And in empty space, that's the wave equation. Ripples in the metric travel, and "
            "they travel at exactly the speed of light. Gravity has caught up with relativity."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(Circumscribe(rows[4], color=C.WAVE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def polarizations(self):
        tt = mtex(r"h_{ij}", r"=", r"\begin{pmatrix} h_+ & h_\times & 0 \\ h_\times & -h_+ & 0 \\ 0 & 0 & 0 \end{pmatrix}",
                  r"\cos\big(\omega(t - z/c)\big)", font_size=38)
        tt[0].set_color(C.WAVE)
        tt.to_edge(UP, buff=0.35)
        ttl = note(r"a wave moving along $z$ (out of the screen): only two of the ten components are physical",
                   font_size=22).next_to(tt, DOWN, buff=0.15)
        ph = ValueTracker(0.0)
        A = 0.32  # exaggerated amplitude
        n = 24
        ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
        base = np.stack([np.cos(ang), np.sin(ang)], 1)
        R = 1.25
        cl, cr = np.array([-3.4, -0.8, 0]), np.array([3.4, -0.8, 0])

        def ring(center, plus):
            def make():
                h = A * math.cos(ph.get_value())
                x, y = base[:, 0], base[:, 1]
                if plus:
                    dx, dy = 0.5 * h * x, -0.5 * h * y
                else:
                    dx, dy = 0.5 * h * y, 0.5 * h * x
                pts = center + R * np.stack([x + dx, y + dy, 0 * x], 1)
                g = VGroup(VMobject(stroke_color=C.WAVE, stroke_width=1.5, stroke_opacity=0.5).set_points_as_corners([*pts, pts[0]]))
                g.add(*[Dot(p, radius=0.07, color=C.WAVE) for p in pts])
                return g
            return always_redraw(make)

        rp, rx = ring(cl, True), ring(cr, False)
        lp = mtex(r"h_+", font_size=40, color=C.WAVE).next_to(cl + UP * R * 1.25, UP, buff=0.1)
        lx = mtex(r"h_\times", font_size=40, color=C.WAVE).next_to(cr + UP * R * 1.25, UP, buff=0.1)
        eq = mtex(r"\delta x = \tfrac12 h_+ x + \tfrac12 h_\times y,\qquad \delta y = -\tfrac12 h_+ y + \tfrac12 h_\times x",
                  font_size=32).to_edge(DOWN, buff=0.75)
        exn = note(r"a ring of free particles; amplitude exaggerated $\sim 10^{20}\times$").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "What does a gravitational wave do? <bookmark mark='m'/> With a further choice of coordinates, a wave moving "
            "along z is described by just two numbers: two polarizations, called plus and cross. <bookmark mark='r'/> "
            "Lay out a ring of free particles across its path. As the wave passes, the plus polarization stretches the "
            "ring along one axis while squeezing it along the other, then the reverse. <bookmark mark='x'/> The cross "
            "polarization does the same, along axes turned by forty-five degrees. <bookmark mark='w'/> Shape changes, no "
            "volume change: this is Weyl curvature, traveling through empty space at the speed of light."
        ) as vo:
            vo.wait_until("m")
            self.play(Write(tt), FadeIn(ttl))
            vo.wait_until("r")
            self.add(rp, rx)
            self.play(FadeIn(lp), FadeIn(lx), FadeIn(eq), FadeIn(exn))
            self.play(ph.animate.set_value(6 * np.pi), run_time=vo.remaining() + 1.0, rate_func=linear)
        rp.clear_updaters()
        rx.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def sources(self):
        q = mtex(r"h^{TT}_{ij}", r"=", r"\frac{2G}{c^4\, r}", r"\,\ddot I^{TT}_{ij}\big(t - r/c\big)", font_size=46)
        q[0].set_color(C.WAVE)
        q[3].set_color(C.MATTER)
        q.to_edge(UP, buff=0.6)
        ql = label(r"the quadrupole formula: an accelerating, non-spherical mass distribution radiates", font_size=26,
                   color=GREY_A).next_to(q, DOWN, buff=0.2)
        est = mtex(r"h", r"\sim", r"\frac{r_s}{r}\,\frac{v^2}{c^2}", font_size=44)
        est[0].set_color(C.WAVE)
        est.next_to(ql, DOWN, buff=0.7)
        estl = label(r"(Schwarzschild radius over distance, times speed squared over $c^2$)", font_size=26,
                     color=GREY_A).next_to(est, DOWN, buff=0.2)
        num = VGroup(
            label(r"two black holes, $66\,M_\odot$ in all ($r_s \approx 200$ km), moving near light speed,", font_size=28),
            label(r"1.4 billion light-years ($1.4\times10^{22}$ km) away:", font_size=28),
            mtex(r"h \sim 10^{-21}", font_size=44, color=C.WAVE),
        ).arrange(DOWN, buff=0.2).next_to(estl, DOWN, buff=0.6)
        with self.voiceover(
            "What makes them? <bookmark mark='q'/> Solving the wave equation with a source gives the quadrupole formula: "
            "the wave is proportional to the second time derivative of the mass distribution's quadrupole moment, "
            "measured at the retarded time. A spinning dumbbell radiates; a pulsating sphere doesn't. "
            "<bookmark mark='e'/> Roughly, the amplitude is the source's Schwarzschild radius divided by your distance "
            "from it, times its speed squared over c squared. <bookmark mark='n'/> For the most violent events in the "
            "universe, two black holes colliding at a good fraction of the speed of light, more than a billion light-years "
            "away, that's about ten to the minus twenty-one."
        ) as vo:
            vo.wait_until("q")
            self.play(Write(q), FadeIn(ql))
            vo.wait_until("e")
            self.play(Write(est), FadeIn(estl))
            vo.wait_until("n")
            self.play(FadeIn(num, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def chirp(self):
        g = load("gw")
        Mc = float(g["Mc_det"])
        tau35 = float(g["tau35"])
        assert abs(Mc - 31.2) < 0.1 and 0.15 < tau35 < 0.17
        f = mtex(r"f_{\text{GW}}(t)", r"=", r"\frac{1}{\pi}\Big(\frac{5}{256\,(t_c - t)}\Big)^{3/8}\Big(\frac{G\mathcal M}{c^3}\Big)^{-5/8}",
                 font_size=40)
        f[0].set_color(C.WAVE)
        f.to_corner(UR, buff=0.5)
        mc = mtex(r"\mathcal M = \frac{(m_1 m_2)^{3/5}}{(m_1 + m_2)^{1/5}}", font_size=34).next_to(f, DOWN, buff=0.3)
        mcl = label(r"the chirp mass", font_size=24, color=GREY_A).next_to(mc, DOWN, buff=0.1)
        # schematic binary, synchronized with a schematic chirp
        s = ValueTracker(0.0)
        cen = np.array([-3.6, 0.3, 0])

        def tau_of(v):
            return 0.35 * (1 - v) + 0.004

        def phase(v):
            tau = tau_of(v)
            return -2 * (5 * 1.5368e-4) ** (-5 / 8) * tau ** (5 / 8) / 2  # orbital phase = half the GW phase

        def binary():
            v = s.get_value()
            tau = tau_of(v)
            a = 0.25 + 1.7 * (tau / 0.354) ** 0.25
            p = phase(v)
            u = np.array([math.cos(p), math.sin(p), 0])
            return VGroup(Dot(cen + a * 0.55 * u, radius=0.2, color=GREY_A), Dot(cen - a * 0.45 * u, radius=0.18, color=GREY_A))

        bm = always_redraw(binary)
        ax = Axes(x_range=[-0.36, 0.0, 0.1], y_range=[-1.2, 1.2, 1], x_length=6.0, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([-3.4, -2.6, 0])
        tt = np.linspace(-0.354, -0.004, 1500)
        tau = -tt
        ph_gw = -2 * (5 * 1.5368e-4) ** (-5 / 8) * tau ** (5 / 8)
        amp = (0.004 / tau) ** 0.25
        wave = polyline(ax, tt, amp * np.cos(ph_gw), color=C.WAVE, stroke_width=2.5)
        wl = label(r"$h(t)$: frequency and amplitude both rise, a chirp", font_size=24, color=C.WAVE).next_to(ax, UP, buff=0.1)
        sch = note(r"schematic").to_corner(DL, buff=0.3)
        txt = VGroup(
            label(r"waves carry energy away $\Rightarrow$ the orbit shrinks", font_size=28),
            label(r"$\Rightarrow$ faster orbit, stronger waves $\Rightarrow$ \ldots", font_size=28),
            label(r"from 35 Hz to merger in 0.16 s (for $\mathcal M = 31\,M_\odot$)", font_size=28, color=C.WAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(mcl, DOWN, buff=0.5).align_to(f, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> Two black holes in orbit radiate. The waves carry away energy, so the orbit shrinks; a "
            "tighter orbit is faster, so it radiates more strongly; so it shrinks faster still. <bookmark mark='w'/> The "
            "result is a chirp: a wave whose frequency and amplitude sweep upward until the black holes merge. "
            "<bookmark mark='f'/> The quadrupole formula predicts the sweep exactly, and it depends on the masses through "
            "a single combination, the chirp mass. <bookmark mark='t'/> For thirty solar masses, the last stretch, from "
            "thirty-five hertz to the merger, takes about a sixth of a second."
        ) as vo:
            vo.wait_until("a")
            self.add(bm)
            self.play(FadeIn(sch), FadeIn(txt[:2]), s.animate.set_value(0.4), run_time=vo.until("w"), rate_func=linear)
            vo.wait_until("w")
            self.play(Create(ax), FadeIn(wl), s.animate.set_value(0.7), run_time=1.0, rate_func=linear)
            self.play(Create(wave), s.animate.set_value(1.0), run_time=3, rate_func=linear)
            vo.wait_until("f")
            self.play(Write(f), FadeIn(mc), FadeIn(mcl))
            vo.wait_until("t")
            self.play(FadeIn(txt[2]))
        bm.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def data(self):
        g = load("gw")
        snap = json.loads(SNAP.read_text())
        assert snap["mass_1_source"] == 35.6 and snap["mass_2_source"] == 30.6 and snap["final_mass_source"] == 63.1
        assert snap["E_rad"] == 3.1
        cst = load("consts")
        assert abs(float(cst["ligo_dL"]) - 4e-18) < 1e-30 and 400 < float(cst["proton_ratio"]) < 450
        t, H1, L1 = g["t"], g["H1"], g["L1"]
        sel = (t > -0.30) & (t < 0.05)
        sc = 1 / np.max(np.abs(H1[sel]))
        ax = Axes(x_range=[-0.30, 0.05, 0.05], y_range=[-1.2, 1.2, 1], x_length=11.5, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([0, 1.7, 0])
        cH = polyline(ax, t[sel], H1[sel] * sc, color=C.WAVE, stroke_width=2.5)
        cL = polyline(ax, t[sel], L1[sel] * sc, color=C.METRIC, stroke_width=2).set_stroke(opacity=0.8)
        leg = VGroup(label(r"Hanford", font_size=24, color=C.WAVE),
                     label(r"Livingston (shifted 7 ms, inverted)", font_size=24, color=C.METRIC)).arrange(RIGHT, buff=0.5)
        leg.next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        when = label(r"GW150914: 14 September 2015, 09:50:45 UTC", font_size=28).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        src = note(r"LIGO open data (gwosc.org), whitened, band-passed 35--350 Hz").next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        # time-frequency map with the chirp prediction
        P = g["power"]
        tf_t, freqs = g["tf_t"], g["freqs"]
        tsel = (tf_t > -0.30) & (tf_t < 0.05)
        Pm = P[:, tsel]
        v = np.clip(Pm / np.percentile(Pm, 99.7), 0, 1) ** 0.8
        col = np.array(ManimColor(C.WAVE).to_rgb())
        rgb = v[..., None] * (col * 0.9 + (1 - col) * np.clip(v - 0.6, 0, 1)[..., None] * 2)
        img = ImageMobject(rgba(np.flipud(rgb), 0.15 + 0.85 * np.flipud(v))).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        ax2 = Axes(x_range=[-0.30, 0.05, 0.05], y_range=[math.log10(20), math.log10(500), 1], x_length=11.5, y_length=3.0,
                   tips=False, axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([0, -1.75, 0])
        img.stretch_to_fit_width(ax2.x_length).stretch_to_fit_height(ax2.y_length).move_to(ax2)
        flab = VGroup(*[MathTex(f"{f_}", font_size=22, color=GREY_A).next_to(ax2.c2p(-0.30, math.log10(f_)), LEFT, buff=0.1)
                        for f_ in (30, 100, 300)])
        fl = label(r"Hz", font_size=22, color=GREY_A).next_to(flab, UP, buff=0.1)
        tc = float(g["t_c"])
        tau, fch = g["tau"], g["f_chirp"]
        ok = (fch > 25) & (fch < 400) & (tc - tau > -0.30)
        pred = polyline(ax2, tc - tau[ok], np.log10(fch[ok]), color=WHITE, stroke_width=3)
        pred = DashedVMobject(pred, num_dashes=40)
        pl = label(r"Einstein's chirp, $\mathcal M = 31\,M_\odot$", font_size=24).next_to(ax2.c2p(-0.2, math.log10(45)), UP, buff=0.15)
        facts = VGroup(
            label(r"$35.6 + 30.6\,M_\odot \to 63.1\,M_\odot$: \ $3.1\,M_\odot c^2$ radiated in a fraction of a second", font_size=26),
            label(r"4 km arms stretched by $4\times10^{-18}$ m: \ 1/400 of a proton's width", font_size=26),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Measuring that seemed hopeless. <bookmark mark='l'/> Then, on the fourteenth of September 2015, the two "
            "detectors of LIGO, in Washington State and Louisiana, three thousand kilometers apart, recorded this. "
            "<bookmark mark='h'/> This is the actual data, which LIGO makes public. Livingston saw the wave seven "
            "milliseconds before Hanford, within the ten milliseconds that light needs to travel between them, and "
            "flipped, because its arms point differently."
        ) as vo:
            vo.wait_until("l")
            self.play(Create(ax), FadeIn(when), FadeIn(src))
            self.play(Create(cH), run_time=2.5)
            vo.wait_until("h")
            self.play(Create(cL), FadeIn(leg), run_time=2)
        with self.voiceover(
            "<bookmark mark='m'/> Spread the signal out by frequency, and the chirp is unmistakable: a rising sweep, from "
            "about thirty-five hertz to a few hundred. <bookmark mark='p'/> And laid over it, the sweep that the quadrupole "
            "formula predicts for a chirp mass of thirty-one Suns. <bookmark mark='f'/> Two black holes, thirty-six and "
            "thirty-one times the mass of the Sun, merged into one of sixty-three. The missing three solar masses left as "
            "gravitational waves. By the time they reached Earth, they stretched LIGO's four kilometer arms by a four "
            "hundredth of the width of a proton."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(img), FadeIn(flab), FadeIn(fl))
            vo.wait_until("p")
            self.play(Create(pred), FadeIn(pl))
            vo.wait_until("f")
            self.play(FadeIn(facts, lag_ratio=0.3))
        self.clear_scene()
