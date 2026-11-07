from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause


class SABRFix(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("sabr")
        p = load("sabr_pde")
        self.card()
        self.density(s)
        self.pde_eq(p)
        self.sheet(p)
        self.fixes()
        self.bartlett()

    def card(self):
        c = chapter_card(7, r"SABR II: negative densities and the fixes", r"What happens when an expansion is priced as a model?",
                         lit=(2002,), part=PART)
        with self.voiceover("Chapter seven. Where SABR's formula breaks, and how desks repaired it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def density(self, s):
        d10 = s["density"]["10"]
        d1 = s["density"]["1"]
        p = s["density_params"]
        K = np.asarray(d10["K"])
        g = axes([0, 0.09], [-140, 80], x_length=7.0, y_length=4.0, xlabel=r"strike (rate)", ylabel=r"implied density",
                 xticks=[0, 0.03, 0.06, 0.09], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[-140, -70, 0, 70],
                 font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, K, np.asarray(d1["pdf"]), RV, stroke_width=2.5)
        l10 = curve(ax, K, np.asarray(d10["pdf"]), BAD, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.09, 0), stroke_color=GREY_C, stroke_width=1.5)
        leg = legend([(RV, r"1 year"), (BAD, r"10 years")], font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        side = VGroup(
            wrapped_label('Negative density gives butterfly arbitrage. The finite strike-interval integral excludes boundary mass; it is not a total-probability test.', 4.6, 20, WHITE),
            wrapped_label(r"the fixes: solve SABR's effective PDE for the density (Hagan, Kumar, Lesniewski and Woodward "
                          r"2014), or price it exactly near zero (Antonov, Konikov and Spector 2015); the House runs Part "
                          r"9's checker on every SABR slice it quotes", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"a rates-like smile: forward {100 * p['F']:.0f}\%, $\beta = \tfrac12$, $\rho = {p['rho']}$, "
                           rf"$\nu = {p['nu']}$; at-the-money vol {100 * p['atm']:.0f}\%")
        with self.voiceover(
            (
            f"""Take a rates-like example with a three-percent forward and beta one half. The one-year implied density is positive on this plotted grid. <bookmark mark='a'/> At ten years, differentiating Hagan prices gives negative density at low strikes: a direct butterfly-arbitrage failure. Its integral over the finite displayed strike interval is {d10['mass']:.2f}; that interval integral excludes boundary mass and is not, by itself, a total-probability test. <bookmark mark='b'/> A repair models a nonnegative probability law with appropriate boundaries, instead of trusting the asymptotic implied-volatility formula far outside its reliable regime."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero), Create(l1), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l10), FadeIn(leg[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def pde_eq(self, p):
        rows = [cmath(r"\partial_T Q", r"=", r"\tfrac12\,\partial_F^2\big(D^2(F)\,E(T, F)\,Q\big),\qquad 0 < F < F_{\max}",
                      font_size=34, colors={r"\partial_T Q": RV}),
                cmath(r"D(F)", r"=", r"\sqrt{\alpha^2 + 2\alpha\rho\nu\,y + \nu^2 y^2}\ F^{\beta},\quad "
                      r"y = \frac{F^{1-\beta} - f^{1-\beta}}{1 - \beta}", font_size=32, colors={r"D(F)": RV}),
                cmath(r"E(T, F)", r"=", r"e^{\rho\nu\alpha\,\Gamma(F)\,T},\quad \Gamma(F) = \frac{F^\beta - f^\beta}{F - f}",
                      font_size=32, colors={r"E(T, F)": RV}),
                cmath(r"\frac{d}{dT}\Big(\int_0^{F_{\max}}\! Q\,dF + Q_L + Q_R\Big)", r"=", r"0", font_size=34,
                      colors={r"\frac{d}{dT}\Big(\int_0^{F_{\max}}\! Q\,dF + Q_L + Q_R\Big)": RV})]
        whys = [why(r"Hagan, Kumar, Lesniewski and Woodward (2014): integrate the volatility out of SABR's forward "
                    r"equation, to the same order as the 2002 formula, and keep the result as an equation for the density "
                    r"$Q$ of $F$ alone", 20),
                why(r"the effective local volatility of the forward: the 2002 expansion's ingredients", 20),
                why(r"a slowly varying time factor from the correlation", 20),
                why('Finite-domain effective PDE: retain both boundary masses. Nonnegative grid probabilities and mass conservation here do not imply the exact two-dimensional SABR law.', 20)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.0, buff=0.6, edge=6.9)
        with self.voiceover(
            (
            """Hagan and co-authors' 2014 arbitrage-free SABR approach derives an effective one-dimensional forward PDE to the expansion's order. It approximates the two-dimensional SABR dynamics. <bookmark mark='a'/> Its effective diffusion is D, <bookmark mark='b'/> with a time factor E that incorporates correlation. <bookmark mark='c'/> Probability absorbed at zero is retained as boundary mass. Our finite-domain implementation also keeps the upper-boundary mass. Nonnegative, mass-conserving discretization provides a coherent numerical distribution; that does not make it the exact full SABR law."""
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def sheet(self, p):
        F = np.asarray(p["F"])
        sh = p["sheet"]
        Ts = np.array([z["T"] for z in sh])
        m = F <= 0.1
        F = F[m]
        Qs = np.array([np.asarray(z["Q"])[m] for z in sh])
        Hs = np.array([np.asarray(z["hagan"])[m] for z in sh])
        bottom = 20 * np.floor(float(np.nanmin(Hs)) / 20)
        top = 20 * np.ceil(max(float(np.nanmax(Qs)), max(z["QL"] * 300 for z in sh)) / 20)
        ax = ThreeDAxes(x_range=[0, 0.1, 0.02], y_range=[0, 10, 2], z_range=[bottom, top, 50], x_length=6.6, y_length=5.6,
                        z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def line(vals, T, col, sw=3):
            return VMobject(stroke_color=col, stroke_width=sw).set_points_as_corners(
                [ax.c2p(x, T, float(z)) for x, z in zip(F, vals)])

        pde = VGroup(*[line(q, T, RV) for q, T in zip(Qs, Ts)])
        hag = VGroup(*[line(h, T, BAD, 2.5) for h, T in zip(Hs, Ts)])
        zero = Polygon(ax.c2p(0, 0, 0), ax.c2p(0.1, 0, 0), ax.c2p(0.1, 10, 0), ax.c2p(0, 10, 0), stroke_width=0,
                       fill_color=GREY_D, fill_opacity=0.25)
        bars = VGroup(*[Line(ax.c2p(0, T, 0), ax.c2p(0, T, z["QL"] * 300), color=VAR, stroke_width=8)
                        for z, T in zip(sh, Ts)])
        hint = VGroup(label(r"the density of a 3\% forward rate, over (rate 0 to 10\%, maturity 0 to 10 years)",
                            font_size=20, color=GREY_A),
                      legend([(RV, r"arbitrage-free SABR (the PDE)"), (BAD, r"Hagan's 2002 formula, differentiated twice"),
                              (VAR, r"mass absorbed at zero (scaled)")], font_size=18)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.12).to_corner(UL, buff=0.3)
        ql = [z["QL"] for z in sh]
        hmin = [float(np.min(h)) for h in Hs]
        txt = VGroup(MathTex(rf"\text{{total mass}} = {p['mass']:.10f}", font_size=26, color=RV),
                     MathTex(rf"Q_L(10\text{{y}}) = {p['QL']:.3f}", font_size=26, color=VAR),
                     MathTex(rf"\min Q = {p['min_Q']:.1e} \ge 0", font_size=26, color=RV),
                     MathTex(rf"\min\ \text{{Hagan}} = {hmin[-1]:.0f}", font_size=26, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        Kc = np.asarray(p["K"])
        lo = int(np.argmin(np.abs(Kc - 0.005)))
        self.set_camera_orientation(phi=66 * DEGREES, theta=-115 * DEGREES, zoom=0.82)
        self.add_fixed_in_frame_mobjects(hint, txt)
        self.remove(hint, txt)
        with self.voiceover(
            (
            (
            f"""Solve the effective PDE on {p['n']} cells through ten years. <bookmark mark='a'/> Boundary probability at zero reaches {100 * p['QL']:.0f} percent. <bookmark mark='b'/> Hagan's differentiated formula becomes negative, reaching minus {abs(hmin[-1]):.0f} on this grid. <bookmark mark='c'/> The PDE calculation preserves total mass to ten decimal places and has nonnegative grid probabilities here. Its ATM Black volatility is {100 * p['atm_pde']:.1f} percent, versus {100 * p['atm_hagan']:.1f} from Hagan. At a half-percent strike the values are {100 * p['pde_iv'][lo]:.0f} and {100 * p['hagan_iv'][lo]:.0f}. This comparison exposes unreliable tail prices; the differences also include effective-model and numerical approximation error."""
        )
        )
        ) as vo:
            self.play(Create(ax), FadeIn(zero), FadeIn(hint), run_time=1.2)
            self.play(LaggedStart(*[Create(l_) for l_ in pde], lag_ratio=0.3), run_time=3)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.2), run_time=2)
            self.move_camera(theta=-70 * DEGREES, phi=70 * DEGREES, run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in hag], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(txt))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, zero, pde, hag, bars)), FadeOut(hint),
                                                                  FadeOut(txt)], run_time=0.8)
        self.clear_scene(run_time=0.35)

    def fixes(self):
        c1 = history_card(2008, r"Ob\l\'oj, ``Fine-tune your smile''",
                          r"Corrects the leading term of Hagan's formula for $\beta < 1$ so that it is right in the "
                          r"$T \to 0$ limit (Berestycki--Busca--Florent).", color=QC.IDEA, width=4.1)
        c2 = history_card(2015, r"Antonov, Konikov and Spector, \textit{Wilmott}",
                          r"Free-boundary SABR: $dF = \alpha|F|^\beta dW$, so rates can go below zero, with near-exact "
                          r"pricing. Written for the negative euro rates of 2014--2021.", color=QC.IDEA, width=4.1)
        c3 = history_card(2015, r"Shifted and normal SABR",
                          r"The desk fix for negative rates: model $F + s$ instead of $F$, or quote normal (Bachelier) "
                          r"volatilities with $\beta = 0$.", color=QC.FIRM, width=4.1)
        G = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            (
            """Other developments include Obłój's corrected leading term in 2008. <bookmark mark='a'/> Antonov, Konikov and Spector extended SABR to permit negative rates through a free-boundary specification. <bookmark mark='b'/> Shifted models and normal-volatility quotes are also widely used. Their domain and boundaries must be specified: changing the quoting convention or adding a shift does not, on its own, repair every arbitrage defect of an asymptotic formula."""
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def bartlett(self):
        rows = [cmath(r"V", r"=", r"C_{\text{BS}}\big(F, K, T, \sigma_B(F, \alpha)\big)", font_size=36, colors={r"V": OPT}),
                cmath(r"\Delta_{\text{Hagan}}", r"=", r"\partial_F C_{\text{BS}} + \partial_\sigma C_{\text{BS}}\ "
                      r"\partial_F\sigma_B", font_size=36, colors={r"\Delta_{\text{Hagan}}": OPT}),
                cmath(r"\mathbb{E}\big[d\alpha \mid dF\big]", r"=", r"\frac{\rho\,\nu}{F^{\beta}}\,dF", font_size=36,
                      colors={r"\mathbb{E}\big[d\alpha \mid dF\big]": VAR}),
                cmath(r"\Delta_{\text{Bartlett}}", r"=", r"\partial_F C_{\text{BS}} + \partial_\sigma C_{\text{BS}}\Big("
                      r"\partial_F\sigma_B + \partial_\alpha\sigma_B\,\frac{\rho\,\nu}{F^{\beta}}\Big)", font_size=34,
                      colors={r"\Delta_{\text{Bartlett}}": OPT})]
        whys = [why(r"the price is Black's formula at SABR's implied vol", 20),
                why(r"the naive delta: move $F$ with $\alpha$ fixed; the smile moves along its backbone", 20),
                why(r"but $\alpha$ is correlated with $F$: regress $d\alpha$ on $dF$ (the same regression as Heston's "
                    r"short skew)", 20),
                why(r"Bartlett (2006): add the expected move of $\alpha$; with $\rho < 0$ the delta of a call is lower. "
                    r"Chapter 17 measures the same idea on bitcoin's real options", 20)]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.0, buff=0.6, edge=6.9)
        with self.voiceover(
            (
            """For the hedge, differentiate Black's price composed with the approximate SABR volatility. <bookmark mark='a'/> Holding alpha fixed gives one delta. <bookmark mark='b'/> The instantaneous linear regression of d-alpha on d-F contributes rho nu over F to the beta. This is a local covariance projection, not a forecast of a future alpha path. <bookmark mark='c'/> Adding its alpha sensitivity gives Bartlett's adjustment, which lowers the call delta in this example. Chapter seventeen examines the related minimum-variance principle using a synthetic Bitcoin option proxy; it is not a direct empirical test of SABR's Bartlett delta. Next, jumps."""
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
