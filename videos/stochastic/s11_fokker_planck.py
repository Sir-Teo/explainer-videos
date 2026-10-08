from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (Raster, boxed, density, gauss_pdf, glow, hist_shape, label, load, mtex, note,
                                      pdf_curve, polyline, raster_for, splat)
from videos.stochastic.compute import WELL_SIGMA, well_V


class FokkerPlanck(VoiceoverScene):
    def construct(self):
        self.question()
        self.derive()
        self.heat()
        self.double_well()
        self.stationary()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"If every particle follows \ $dX = \mu(X)\,dt + \sigma(X)\,dW$,\\"
                  r"how does the density $p(t, x)$ of the cloud evolve?", font_size=38)
        q.move_to(UP * 0.4)
        with self.voiceover(
            "So here's the question. If every particle in a cloud follows the same stochastic differential equation, "
            "each with its own independent noise, how does the density of the cloud change over time?"
        ):
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.3)
        self.play(FadeOut(q))

    # ------------------------------------------------------------------
    def derive(self):
        l1 = MathTex(r"d\varphi(X_t)", r"=", r"\Big(\mu\,\varphi'(X_t) + \tfrac12\sigma^2\varphi''(X_t)\Big)\,dt", r"+",
                     r"\sigma\,\varphi'(X_t)\,dW_t", font_size=38)
        l1[2].set_color(C.DRIFT)
        l1[4].set_color(C.BROWNIAN)
        l2 = MathTex(r"\frac{d}{dt}\,\mathbb E\big[\varphi(X_t)\big]", r"=",
                     r"\mathbb E\Big[\mu\,\varphi' + \tfrac12\sigma^2\varphi''\Big]", font_size=38)
        l3 = MathTex(r"\frac{d}{dt}\int \varphi\, p\,dx", r"=", r"\int \Big(\mu\,\varphi' + \tfrac12\sigma^2\varphi''\Big)\, p\,dx",
                     font_size=38)
        l4 = MathTex(r"\int \varphi\;\partial_t p\,dx", r"=",
                     r"\int \varphi\;\Big(-\partial_x(\mu p) + \tfrac12\partial_x^2\big(\sigma^2 p\big)\Big)\,dx", font_size=38)
        col = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.42).to_edge(UP, buff=0.5)
        for m in (l2, l3, l4):
            m.shift((l1[1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        n1 = label(r"It\^o's lemma, for any smooth test function $\varphi$", font_size=24, color=GREY_B)
        n2 = label(r"average: the $dW$ term has mean zero", font_size=24, color=GREY_B)
        n3 = label(r"averages are integrals against the density", font_size=24, color=GREY_B)
        n4 = label(r"integrate by parts: move the derivatives off $\varphi$", font_size=24, color=GREY_B)
        for n_, m in zip((n1, n2, n3, n4), (l1, l2, l3, l4)):
            n_.next_to(m, DOWN, buff=0.06)
        fp = MathTex(r"\partial_t p", r"=", r"-\partial_x\big(\mu\, p\big)", r"+", r"\tfrac12\,\partial_x^2\big(\sigma^2 p\big)",
                     font_size=50)
        fp[0].set_color(C.PDF)
        fp[2].set_color(C.DRIFT)
        fp[4].set_color(C.BROWNIAN)
        fpb = boxed(fp, color=C.PDF, buff=0.25).to_edge(DOWN, buff=0.35)
        name = label(r"the Fokker--Planck equation", font_size=28, color=C.PDF).next_to(fpb, RIGHT, buff=0.3)
        name.shift(LEFT * max(0, name.get_right()[0] - 6.9))

        with self.voiceover(
            "Itô's lemma answers it, with a classic trick: don't look at the density directly. <bookmark mark='a'/> Look "
            "at the average of some smooth test function, phi, of X. By Itô's lemma, phi of X changes by a drift term, "
            "mu phi prime plus one half sigma squared phi double prime, plus a noise term. <bookmark mark='b'/> Take the "
            "average, and the noise term vanishes: Itô integrals have mean zero."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(n1), run_time=2)
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(n2))
        with self.voiceover(
            "<bookmark mark='c'/> An average is an integral against the density p. <bookmark mark='d'/> Now integrate by "
            "parts: once to move the derivative off phi prime, twice for phi double prime. The boundary terms vanish, "
            "and we get phi times something, integrated. <bookmark mark='e'/> Since this holds for every test function "
            "phi, the somethings must be equal."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(n3))
            vo.wait_until("d")
            self.play(Write(l4), FadeIn(n4))
            vo.wait_until("e")
            self.play(Indicate(l4[0], color=C.PDF), Indicate(l4[2], color=C.PDF))
        with self.voiceover(
            "The result: <bookmark mark='f'/> the rate of change of the density is minus the slope of mu times p, plus one "
            "half the curvature of sigma squared times p. This is the Fokker–Planck equation, also called Kolmogorov's "
            "forward equation. <bookmark mark='g'/> The first term carries probability along with the drift. The second "
            "spreads it out. Randomness in each path became a perfectly deterministic equation for the cloud."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(fp), Create(fpb[0]), FadeIn(name))
            vo.wait_until("g")
            self.play(Indicate(fp[2], color=C.DRIFT))
            self.play(Indicate(fp[4], color=C.BROWNIAN))
        self.wait(0.3)
        self.play(FadeOut(VGroup(col, n1, n2, n3, n4, name)), fpb.animate.scale(0.75).to_corner(UR, buff=0.3))
        self.fpb = fpb

    # ------------------------------------------------------------------
    def heat(self):
        d = load("heat")
        F, ts = d["frames"], d["ts"]
        n_frames = len(ts) - 1
        heat_eq = MathTex(r"\mu = 0,\ \sigma = 1:", r"\quad \partial_t p = \tfrac12\,\partial_x^2 p", font_size=38)
        heat_eq[1].set_color(C.PDF)
        heat_eq.to_corner(UL, buff=0.4)
        hname = label(r"the heat equation (Einstein's diffusion equation)", font_size=26, color=GREY_A)
        hname.next_to(heat_eq, DOWN, buff=0.12).align_to(heat_eq, LEFT)
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1.6, 0.5], x_length=11, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(UP * 0.0)
        bx = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1, 1], x_length=11, y_length=1.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).next_to(ax, DOWN, buff=0.35)
        bx.y_axis.set_opacity(0)
        jitter = np.random.default_rng(9).uniform(0.06, 0.94, F.shape[1])
        k = ValueTracker(1.0)
        extent, shape, w, h, c = raster_for(bx, (-3.2, 3.2), (0, 1), px_per_unit=120)

        def draw(v):
            x = F[int(round(v))]
            return glow(splat(x, jitter, extent, shape, sigma=1.1), C.BROWNIAN, gain=1.3)

        cloud = Raster(draw, k, w, h, c)
        edges = np.linspace(-3.2, 3.2, 65)
        xs = np.linspace(-3.2, 3.2, 300)

        def hist():
            j = int(round(k.get_value()))
            return hist_shape(ax, edges, np.minimum(density(F[j], edges), 1.6), color=C.PDF, fill_opacity=0.35)

        def theory():
            t = max(ts[int(round(k.get_value()))], 1e-3)
            return pdf_curve(ax, xs, np.minimum(gauss_pdf(xs, 0, t), 1.6), color=WHITE, stroke_width=2.5)

        tval = DecimalNumber(0, num_decimal_places=2, font_size=30)
        tval.add_updater(lambda m: m.set_value(ts[int(round(k.get_value()))]))
        ro = VGroup(MathTex("t =", font_size=30), tval).arrange(RIGHT, buff=0.12).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        hs, tc = always_redraw(hist), always_redraw(theory)
        leg = note(r"4{,}000 simulated Brownian particles (vertical spread only for visibility); white: $\mathcal N(0, t)$",
                   font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Start with the simplest case: pure Brownian motion, no drift, sigma equal to one. <bookmark mark='h'/> Then "
            "Fokker–Planck is the heat equation: the density changes at a rate equal to one half its curvature. It's the "
            "same equation Einstein derived for diffusing particles. <bookmark mark='g'/> Here are four thousand "
            "particles released at one point. <bookmark mark='s'/> Their histogram spreads out, exactly along the bell "
            "curve with variance t, which solves the heat equation."
        ) as vo:
            vo.wait_until("h")
            self.play(Write(heat_eq), FadeIn(hname))
            vo.wait_until("g")
            self.play(Create(ax), Create(bx.x_axis), FadeIn(leg))
            self.add(cloud, hs, tc, ro)
            vo.wait_until("s")
            self.play(k.animate.set_value(36), run_time=vo.remaining() + 0.5, rate_func=linear)
        # curvature arrows at the current time
        t0 = ts[36]
        pts = np.linspace(-2.4, 2.4, 17)
        p = gauss_pdf(pts, 0, t0)
        p2 = p * (pts**2 / t0**2 - 1 / t0)
        arrows = VGroup()
        for x, pv, c2 in zip(pts, p, p2):
            L = float(np.clip(0.5 * c2 * 0.12, -0.9, 0.9))
            if abs(L) < 0.04:
                continue
            start = ax.c2p(x, min(pv, 1.6))
            arrows.add(Arrow(start, start + UP * L, buff=0, color=C.QV, stroke_width=3, max_tip_length_to_length_ratio=0.3))
        with self.voiceover(
            "You can see why it spreads. <bookmark mark='p'/> At the peak, the curve bends down, so the density falls. "
            "Out on the shoulders, it bends up, so the density rises. Peaks get shaved, valleys get filled, and the bell "
            "flattens. <bookmark mark='r'/> And the width grows like the square root of time."
        ) as vo:
            vo.wait_until("p")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("r")
            self.play(FadeOut(arrows))
            self.play(k.animate.set_value(n_frames), run_time=vo.remaining() + 1.0, rate_func=linear)
        self.wait(0.3)
        self.play(FadeOut(VGroup(heat_eq, hname, leg)))
        for m in (cloud, hs, tc, tval):
            m.clear_updaters()
        self.play(FadeOut(VGroup(ax, bx, hs, tc, ro)), FadeOut(cloud))

    # ------------------------------------------------------------------
    def double_well(self):
        d = load("well")
        F, ts, xc, dens, boltz = d["frames"], d["ts"], d["xc"], d["dens"], d["boltz"]
        n_frames = len(ts) - 1
        sig = WELL_SIGMA
        L = 2.0
        top = Axes(x_range=[-L, L, 1], y_range=[0, 2.2, 0.5], x_length=10.5, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_edge(UP, buff=1.25)
        pot = Axes(x_range=[-L, L, 1], y_range=[0, 2.0, 0.5], x_length=10.5, y_length=3.0, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False}).next_to(top, DOWN, buff=0.3)
        pot.y_axis.set_opacity(0)
        top.y_axis.set_opacity(0)
        xv = np.sqrt(1 + np.sqrt(2.0))  # V = 2 at the top of the axes
        vcurve = pot.plot(well_V, x_range=[-xv, xv, 0.01], color=C.LANDSCAPE, stroke_width=3)
        vl = MathTex(r"V(x) = (x^2 - 1)^2", font_size=30, color=C.LANDSCAPE).next_to(pot.c2p(xv, 1.9), RIGHT, buff=0.2)
        sde = MathTex(r"dX", r"=", r"-V'(X)\,dt", r"+", rf"{sig:g}\,dW", font_size=36).to_corner(UL, buff=0.35)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        k = ValueTracker(0.0)
        extent, shape, w, h, c = raster_for(pot, (-L, L), (0, 2.0), px_per_unit=120)
        lift = np.random.default_rng(10).uniform(0.03, 0.16, F.shape[1])

        def draw(v):
            x = F[int(round(v))]
            return glow(splat(x, well_V(x) + lift, extent, shape, sigma=1.2), C.BROWNIAN, gain=1.2)

        balls = Raster(draw, k, w, h, c)
        edges = np.linspace(-L, L, 61)

        def hist():
            j = int(round(k.get_value()))
            return hist_shape(top, edges, np.minimum(density(F[j], edges), 2.2), color=C.PDF, fill_opacity=0.35)

        def fp_curve():
            j = int(round(k.get_value()))
            m = (xc >= -L) & (xc <= L)
            return polyline(top, xc[m], np.minimum(dens[j][m], 2.2), color=WHITE, stroke_width=2.5)

        tval = DecimalNumber(0, num_decimal_places=1, font_size=28)
        tval.add_updater(lambda m: m.set_value(ts[int(round(k.get_value()))]))
        ro = VGroup(MathTex("t =", font_size=28), tval).arrange(RIGHT, buff=0.12).next_to(top, UP, buff=0.08)
        hs, fc = always_redraw(hist), always_redraw(fp_curve)
        leg = VGroup(label(r"histogram: 3{,}000 simulated particles", font_size=22, color=C.PDF),
                     label(r"white: Fokker--Planck, solved numerically", font_size=22)).arrange(RIGHT, buff=0.6)
        leg.to_edge(DOWN, buff=0.2)
        right = float(d["right"][0])

        with self.voiceover(
            "Now something richer. <bookmark mark='v'/> Let the drift be the downhill slope of a landscape with two "
            "valleys, so particles roll toward the bottoms, while the noise keeps shaking them. <bookmark mark='p'/> Drop "
            "three thousand particles into the left valley."
        ) as vo:
            self.play(Write(sde))
            vo.wait_until("v")
            self.play(Create(pot.x_axis), Create(vcurve), FadeIn(vl))
            vo.wait_until("p")
            self.play(Create(top), FadeIn(leg), FadeIn(ro))
            self.add(balls, hs, fc)
        with self.voiceover(
            "At first they huddle in the left valley, and the density there settles into a bell. <bookmark mark='h'/> "
            "But every so often, a run of unlucky kicks throws a particle over the ridge. <bookmark mark='r'/> Slowly, "
            "the right valley fills. <bookmark mark='w'/> And all along, the histogram of the simulated particles follows "
            "the Fokker–Planck equation, solved on a computer as a smooth curve, with no randomness at all."
        ) as vo:
            self.play(k.animate.set_value(60), run_time=vo.until("h"), rate_func=linear)
            self.play(k.animate.set_value(260), run_time=vo.until("w"), rate_func=linear)
            self.play(k.animate.set_value(n_frames * 0.75), run_time=vo.remaining() + 0.5, rate_func=linear)
        self.play(k.animate.set_value(n_frames), run_time=3, rate_func=linear)
        self.top, self.pot, self.boltz, self.xc = top, pot, boltz, xc
        self.right = right
        self.sde, self.ro = sde, ro

    # ------------------------------------------------------------------
    def stationary(self):
        top, xc, boltz = self.top, self.xc, self.boltz
        sig = WELL_SIGMA
        m = (xc >= -2) & (xc <= 2)
        bcurve = polyline(top, xc[m], np.minimum(boltz[m], 2.2), color=C.QV, stroke_width=3.5)
        bcurve.set_stroke(opacity=0.9)
        der = VGroup(
            MathTex(r"\partial_t p = 0", r"\;\Rightarrow\;", r"\mu\,p - \tfrac12\sigma^2\,\partial_x p = 0", font_size=34),
            MathTex(r"\;\Rightarrow\;", r"p_\infty(x) \;\propto\; e^{-2V(x)/\sigma^2}", font_size=38),
        ).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.3)
        der[1][1].set_color(C.QV)
        bname = label(r"Boltzmann's distribution, \ temperature $\sigma^2/2$", font_size=24, color=C.QV)
        half = label(rf"right valley at $t = 40$: {100 * self.right:.0f}\% of particles", font_size=24, color=GREY_A)
        VGroup(bname, half).arrange(RIGHT, buff=0.8).next_to(der, DOWN, buff=0.15)
        with self.voiceover(
            "Eventually the cloud stops changing. <bookmark mark='a'/> Setting the time derivative to zero, and the flow of "
            "probability to zero, gives a first-order equation we can solve: <bookmark mark='b'/> the stationary density "
            "is proportional to e to the minus two V over sigma squared. <bookmark mark='c'/> That's exactly Boltzmann's "
            "distribution from statistical mechanics, with the noise strength playing the role of temperature. "
            "<bookmark mark='d'/> Our simulated particles have found it: by the end, they're split nearly half and half "
            "between the valleys."
        ) as vo:
            self.play(FadeOut(VGroup(self.sde, self.fpb)), self.ro.animate.set_opacity(0))
            vo.wait_until("a")
            self.play(Write(der[0]))
            vo.wait_until("b")
            self.play(Write(der[1]))
            vo.wait_until("c")
            self.play(Create(bcurve), FadeIn(bname))
            vo.wait_until("d")
            self.play(FadeIn(half))
        self.wait(0.6)
        self.clear_scene()
