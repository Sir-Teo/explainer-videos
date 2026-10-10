from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (WaveView, boxed, corner_wheel, frames_at, label, load, mtex, note, num, polyline,
                                   stack, wave_axes, why)


class FreeParticle(VoiceoverScene):
    def construct(self):
        self.building()
        self.dispersion()
        self.packet_motion()
        self.spreading()
        self.real_numbers()

    # ------------------------------------------------------------------
    def building(self):
        p = load("packet")
        kk, wk = p["kk"], p["wk"]
        s0, k0 = 2.0, 2.0
        x = np.linspace(-22, 22, 2200)
        mid = len(kk) // 2
        n_tr = ValueTracker(1)

        def psi_n(n):
            sel = np.abs(np.arange(len(kk)) - mid) <= (n - 1) // 2
            s = (wk[sel, None] * np.exp(1j * kk[sel, None] * x[None, :])).sum(axis=0)
            return s / np.sqrt(np.trapezoid(np.abs(s) ** 2, x))

        top = wave_axes((-22, 22), (0, 0.45), x_length=11.5, y_length=2.4).move_to(DOWN * 1.6)
        wv = WaveView(top, x, psi_n(1), mode="density", scale=1.0, x_window=(-22, 22))
        wv.add_updater(lambda m: m.set_psi(psi_n(int(n_tr.get_value()))))
        # the components: little bars of weight w(k), drawn above
        kax = Axes(x_range=[k0 - 1.6, k0 + 1.6, 0.5], y_range=[0, 1.1, 1], x_length=6.5, y_length=1.9, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(UP * 1.9)

        def bars():
            n = int(n_tr.get_value())
            g = VGroup()
            for j, (k, w) in enumerate(zip(kk, wk)):
                on = abs(j - mid) <= (n - 1) // 2
                p0, p1 = kax.c2p(k, 0), kax.c2p(k, w)
                g.add(Line(p0, p1, color=C.MOMENTUM, stroke_width=5).set_opacity(1.0 if on else 0.18))
            return g

        bg = always_redraw(bars)
        kl = MathTex("k", font_size=30, color=C.MOMENTUM).next_to(kax.x_axis.get_end(), RIGHT, buff=0.1)
        phl = MathTex(r"\phi(k)", font_size=30, color=C.MOMENTUM).next_to(kax.y_axis.get_end(), UP, buff=0.1)
        cnt = always_redraw(lambda: MathTex(r"\text{plane waves added: }" + str(int(n_tr.get_value())), font_size=30)
                            .next_to(top, UP, buff=0.15).to_edge(RIGHT, buff=0.6))
        formula = MathTex(r"\psi(x, 0)", r"=", r"\frac{1}{\sqrt{2\pi}}\int \phi(k)\, e^{ikx}\,dk", font_size=38)
        formula.to_corner(UL, buff=0.4)
        wheel = corner_wheel(corner=DR, buff=0.2, radius=0.3)
        with self.voiceover(
            "A single plane wave has a perfectly definite momentum, but it's spread over all of space. To describe a "
            "particle that's somewhere, add plane waves together. <bookmark mark='a'/> Take wave numbers clustered "
            "around one value, with weights phi of k. <bookmark mark='b'/> One wave alone is flat. Add a few neighbors, "
            "and they reinforce in the middle and cancel elsewhere."
        ) as vo:
            self.play(Write(formula))
            vo.wait_until("a")
            self.play(Create(kax), FadeIn(kl), FadeIn(phl), FadeIn(bg), Create(top), FadeIn(wv), FadeIn(cnt), FadeIn(wheel))
            vo.wait_until("b")
            for n in (3, 5, 9):
                self.play(n_tr.animate.set_value(n), run_time=0.9, rate_func=lambda a: float(a >= 1))
                self.wait(0.6)
        with self.voiceover(
            "With more and more components, the cancellation away from the center becomes complete, and we get a wave "
            "packet: <bookmark mark='p'/> a lump of probability with a hue that cycles at the central wave number. "
            "In the limit it's an integral, a Fourier transform. A narrow spread of k gives a wide packet; a wide spread "
            "gives a narrow one."
        ) as vo:
            for n in (13, 19, 25):
                self.play(n_tr.animate.set_value(n), run_time=0.9, rate_func=lambda a: float(a >= 1))
                self.wait(0.5)
            vo.wait_until("p")
        wv.clear_updaters()
        bg.clear_updaters()
        cnt.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def dispersion(self):
        d1 = MathTex(r"\psi_k", r"=", r"e^{\,i(kx - \omega t)}", font_size=40)
        d2 = MathTex(r"\hbar\omega\,\psi_k", r"=", r"\frac{\hbar^2 k^2}{2m}\,\psi_k", font_size=40)
        d3 = MathTex(r"\omega(k)", r"=", r"\frac{\hbar k^2}{2m}", font_size=44)
        col = stack(d1, d2, d3, buff=0.4, align=1).to_edge(UP, buff=0.45).shift(LEFT * 3.6)
        d3[0].set_color(C.QTIME)
        w2 = why(d2, r"put it in the equation ($V = 0$)", font_size=22)
        db = boxed(d3, color=C.QTIME, buff=0.15)
        v1 = MathTex(r"v_{\text{phase}}", r"=", r"\frac{\omega}{k}", r"=", r"\frac{\hbar k}{2m}", font_size=40)
        v2 = MathTex(r"v_{\text{group}}", r"=", r"\frac{d\omega}{dk}", r"=", r"\frac{\hbar k}{m}", font_size=40)
        vv = stack(v1, v2, buff=0.35, align=1).to_edge(UP, buff=0.6).shift(RIGHT * 3.2)
        v2[4].set_color(C.MOMENTUM)
        pm = MathTex(r"= \frac{p}{m}", font_size=40, color=C.MOMENTUM).next_to(v2, RIGHT, buff=0.15)
        # two plane waves: their beats move at the group velocity, their colors at the phase velocity
        k1, k2 = 1.7, 2.3
        x = np.linspace(-12, 12, 2400)
        t = ValueTracker(0.0)
        ax = wave_axes((-12, 12), (0, 4.3), x_length=11.5, y_length=2.2).to_edge(DOWN, buff=0.8)

        def two(tt):
            return np.exp(1j * (k1 * x - k1**2 / 2 * tt)) + np.exp(1j * (k2 * x - k2**2 / 2 * tt))

        wv = WaveView(ax, x, two(0), mode="density", scale=1.0).follow(t, two)
        vg = (k1**2 - k2**2) / 2 / (k1 - k2)
        assert abs(vg - (k1 + k2) / 2) < 1e-12
        lab2 = note(r"two plane waves, $k = 1.7$ and $2.3$ ($\hbar = m = 1$): the beats move at $v_{\text{group}} = 2$, "
                    r"the colors at about $1$").next_to(ax, DOWN, buff=0.15)
        with self.voiceover(
            "Now let each component move. <bookmark mark='a'/> Put a single plane wave into the Schrödinger equation "
            "with no potential, and it works only if h-bar omega equals h-bar squared k squared over two m. "
            "<bookmark mark='b'/> So the frequency grows like the square of the wave number. This is the free particle's "
            "dispersion relation, and it means different components travel at different speeds."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(d1), Write(d2), FadeIn(w2))
            vo.wait_until("b")
            self.play(Write(d3), Create(db[0]))
        with self.voiceover(
            "There are two speeds here. <bookmark mark='p'/> A single crest moves at omega over k: h-bar k over two m. "
            "<bookmark mark='g'/> But the lump, where the waves reinforce, moves at d omega d k: h-bar k over m, which "
            "is p over m, exactly the classical velocity. <bookmark mark='s'/> Watch two plane waves: the bright beats "
            "glide along at the group velocity, while the colors inside them crawl at half that speed."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(v1))
            vo.wait_until("g")
            self.play(Write(v2), FadeIn(pm))
            vo.wait_until("s")
            self.play(Create(ax), FadeIn(wv), FadeIn(lab2))
            self.play(t.animate.set_value(5.0), run_time=vo.remaining() + 1.5, rate_func=linear)
        wv.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def packet_motion(self):
        p = load("packet")
        x, ts, fr, crest, mx = p["x"], p["ts"], p["frames"], p["crest"], p["mx"]
        t = ValueTracker(0.0)
        ax = wave_axes((-8, 24), (0, 0.22), x_length=12, y_length=3.0).shift(DOWN * 0.4)
        wv = WaveView(ax, x, fr[0], mode="density", x_window=(-8, 24)).follow(t, frames_at(ts, fr))
        rho_at = lambda xx, tt: float(np.interp(xx, x, np.abs(frames_at(ts, fr)(tt)) ** 2))  # noqa: E731

        def peak_mark():
            xx = float(np.interp(t.get_value(), ts, mx))
            return VGroup(DashedLine(ax.c2p(xx, 0), ax.c2p(xx, 0.215), color=WHITE, stroke_width=2),
                          MathTex(r"\langle x\rangle", font_size=26).next_to(ax.c2p(xx, 0.215), UP, buff=0.05))

        def crest_mark():
            xx = float(np.interp(t.get_value(), ts, crest))
            y = rho_at(xx, t.get_value())
            return VGroup(Dot(ax.c2p(xx, y), radius=0.08, color=WHITE),
                          Line(ax.c2p(xx, 0), ax.c2p(xx, y), color=WHITE, stroke_width=2))

        pk, cr = always_redraw(peak_mark), always_redraw(crest_mark)
        lab = VGroup(label(r"dashed: the peak, moving at $v_{\text{group}} = 2$", font_size=26),
                     label(r"dot: one crest (phase $= 0$), moving at $v_{\text{phase}} = 1$", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.5)
        sim = note(r"exact solution: $\sigma_0 = 2$, $k_0 = 2$, $\hbar = m = 1$").to_corner(DR, buff=0.3)
        wheel = corner_wheel(corner=UR, buff=0.25, radius=0.3)
        with self.voiceover(
            "Now the real thing: a Gaussian packet, evolved exactly. <bookmark mark='g'/> The dashed line marks its "
            "center, moving at the group velocity. The white dot rides on one crest, one particular color. "
            "<bookmark mark='r'/> It moves too, but at half the speed, so the colors slip backward through the packet. "
            "The particle goes where the group goes."
        ) as vo:
            self.play(Create(ax), FadeIn(wv), FadeIn(sim), FadeIn(wheel))
            vo.wait_until("g")
            self.add(pk, cr)
            self.play(FadeIn(lab))
            vo.wait_until("r")
            self.play(t.animate.set_value(6.5), run_time=vo.remaining() + 1.0, rate_func=linear)
        for m in (wv, pk, cr):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def spreading(self):
        p = load("packet")
        x, ts, fr, sx, sig_th, phik, k = p["x"], p["ts"], p["frames"], p["sx"], p["sig_th"], p["phik"], p["k"]
        s0 = 2.0
        t = ValueTracker(0.0)
        ax = wave_axes((-10, 100), (0, 0.22), x_length=8.2, y_length=2.4).move_to(LEFT * 2.3 + UP * 1.75)
        wv = WaveView(ax, x, fr[0], mode="density", x_window=(-10, 100)).follow(t, frames_at(ts, fr))
        kax = wave_axes((0.5, 3.5), (0, 1.2), x_length=3.6, y_length=2.4).move_to(RIGHT * 4.6 + UP * 1.75)
        kwv = WaveView(kax, k, phik.astype(complex), mode="density", scale=0.8, x_window=(0.5, 3.5))
        kwv.follow(t, lambda tt: phik * np.exp(-1j * k**2 / 2 * tt))
        xl = MathTex(r"|\psi(x)|^2", font_size=28).next_to(ax, UP, buff=0.05)
        kl = MathTex(r"|\phi(k)|^2", font_size=28, color=C.MOMENTUM).next_to(kax, UP, buff=0.05)
        kn = note(r"never changes").next_to(kax, DOWN, buff=0.1)
        sax = Axes(x_range=[0, 40, 10], y_range=[0, 12, 4], x_length=6.2, y_length=2.7, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.4 + DOWN * 2.1)
        curve = sax.plot(lambda tt: s0 * np.sqrt(1 + (tt / (2 * s0**2)) ** 2), x_range=[0, 40], color=C.XPOS, stroke_width=3)
        dots = VGroup(*[Dot(sax.c2p(tt, ss), radius=0.045, color=C.BORN) for tt, ss in zip(ts[::12], sx[::12])])
        tl = MathTex("t", font_size=28, color=C.QTIME).next_to(sax.x_axis.get_end(), RIGHT, buff=0.1)
        sl = MathTex(r"\sigma_x(t)", font_size=28, color=C.XPOS).next_to(sax.y_axis.get_end(), UP, buff=0.1)
        law = MathTex(r"\sigma_x(t)", r"=", r"\sigma_0\sqrt{1 + \Big(\frac{\hbar t}{2m\sigma_0^2}\Big)^2}", font_size=38)
        law.move_to(RIGHT * 3.6 + DOWN * 1.3)
        law[0].set_color(C.XPOS)
        heur = MathTex(r"\sigma_p = \frac{\hbar}{2\sigma_0}", r"\;\Rightarrow\;", r"\sigma_v = \frac{\hbar}{2m\sigma_0}",
                       font_size=32).next_to(law, DOWN, buff=0.35)
        heur[0].set_color(C.MOMENTUM)
        late = note(r"late times: $\sigma_x \approx \sigma_v\, t$").next_to(heur, DOWN, buff=0.12)
        dn = note(r"dots: measured on the simulation").next_to(sax, DOWN, buff=0.1)
        wheel = corner_wheel(corner=UL, buff=0.2, radius=0.28, labels=False, title=False)
        with self.voiceover(
            "And the packet spreads. <bookmark mark='a'/> Its momentum content, on the right, never changes at all: a "
            "free particle keeps its momentum. <bookmark mark='b'/> The faster components simply run ahead and the "
            "slower ones fall behind. You can see it in the colors: the hue cycles faster at the front."
        ) as vo:
            self.play(Create(ax), FadeIn(wv), FadeIn(xl), Create(kax), FadeIn(kwv), FadeIn(kl), FadeIn(wheel))
            vo.wait_until("a")
            self.play(FadeIn(kn), t.animate.set_value(14), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(30), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "How fast? A packet of width sigma zero has a momentum spread of h-bar over two sigma zero, a fact we'll "
            "derive with the uncertainty principle. <bookmark mark='v'/> Divide by the mass to get a spread of "
            "velocities, and at late times the width grows like that velocity spread times t. <bookmark mark='e'/> The "
            "exact law, from completing the square in the Fourier integral, is sigma zero times the square root of one "
            "plus h-bar t over two m sigma zero squared, all squared. <bookmark mark='d'/> The simulation sits right on "
            "it, to one part in ten thousand."
        ) as vo:
            self.play(Create(sax), FadeIn(tl), FadeIn(sl), FadeIn(heur[0]))
            vo.wait_until("v")
            self.play(FadeIn(heur[1:]), FadeIn(late))
            vo.wait_until("e")
            self.play(Write(law), Create(curve), t.animate.set_value(40), run_time=2.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08), FadeIn(dn))
        assert np.max(np.abs(sx / sig_th - 1)) < 1e-4
        for m in (wv, kwv):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_numbers(self):
        p = load("packet")
        we = float(p["width_e_1fs"][0]) * 1e10
        yrs = float(p["t_double_g"][0])
        assert abs(we - 5.9) < 0.05 and 0.9e6 < yrs < 1.2e6
        rows = VGroup(
            label(r"an electron, localized to $1$\,\AA", font_size=32),
            MathTex(r"\text{after } 1\text{ femtosecond: } \sigma \approx " + f"{we:.1f}" + r"\,\text{\AA}", font_size=34,
                    color=C.XPOS),
            label(r"a $1$-microgram grain, localized to $1\,\mu$m", font_size=32),
            MathTex(r"\text{time to double its width: about a million years}", font_size=34, color=C.XPOS),
        ).arrange(DOWN, buff=0.35)
        rows[2].shift(DOWN * 0.4)
        rows[3].shift(DOWN * 0.4)
        rule = MathTex(r"\tau = \frac{2m\sigma_0^2}{\hbar}", font_size=44).to_edge(UP, buff=0.6)
        rn = note(r"the spreading time: how long until the width has grown noticeably").next_to(rule, DOWN, buff=0.15)
        with self.voiceover(
            "The time scale for spreading is two m sigma zero squared over h-bar, so it depends enormously on mass. "
            "<bookmark mark='e'/> An electron squeezed into one angstrom, about the size of an atom, has spread to six "
            "angstroms after a single femtosecond. <bookmark mark='g'/> A one-microgram grain of dust, localized to a "
            "micron, would take about a million years just to double its width. That's one reason the everyday world "
            "looks so classical."
        ) as vo:
            self.play(Write(rule), FadeIn(rn))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("g")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
