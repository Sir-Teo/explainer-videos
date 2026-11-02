from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, polyline, predict, sci


class Fourier(VoiceoverScene):
    def construct(self):
        f = load("fourier")
        lw = load("lewis")
        self.card()
        self.damping(lw)
        self.derive()
        self.grid(f)
        self.lewis(lw)

    def card(self):
        c = chapter_card(15, r"Fourier I: Carr--Madan and Lewis", r"How do you price from a characteristic function?",
                         lit=(1999,), part=PART)
        with self.voiceover("Chapter fifteen. Fourier methods, part one: Carr and Madan, and Lewis."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def damping(self, lw):
        k = np.asarray(lw["k"])
        C = np.asarray(lw["C"])
        g = axes([-1.5, 1.0], [0, 100], x_length=6.2, y_length=4.0, xlabel=r"log-strike $k = \log K$ (relative to $S_0$)",
                 ylabel=r"$e^{\alpha k}\,C(k)$", xticks=[-1, 0, 1], yticks=[0, 50, 100], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        al = ValueTracker(0.0)
        cur = always_redraw(lambda: curve(ax, k, np.clip(np.exp(al.get_value() * k) * C, 0, 100), OPT, stroke_width=3))
        rd = readout(r"\alpha =", lambda: al.get_value(), digits=2, font_size=32, color=OPT)
        rd.next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        u = np.asarray(lw["u"])
        h = axes([0, 25], [-0.5, 1.0], x_length=4.6, y_length=3.0, xlabel=r"frequency $u$",
                 ylabel=r"its transform $\psi(u)$ ($\alpha = 1.5$)", xticks=[0, 10, 20], yticks=[0, 1], font_size=14)
        h.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        sc = max(np.abs(lw["psi_re"]).max(), 1e-9)
        re = curve(h.ax, u, np.asarray(lw["psi_re"]) / sc, GOOD, stroke_width=2.5)
        im = curve(h.ax, u, np.asarray(lw["psi_im"]) / sc, QC.THETA, stroke_width=2.5)
        leg = legend([(GOOD, r"real part"), (QC.THETA, r"imaginary part (scaled together)")], font_size=15)
        leg.next_to(h, UP, buff=0.1).align_to(h, LEFT)
        with self.voiceover(
            "When a model has a characteristic function, as Heston, the Lévy models and the affine models do, prices "
            "come from Fourier transforms. The call price as a function of log-strike is not transformable: as the "
            "strike goes to zero it rises to the stock price and stays there. <bookmark mark='a'/> Peter Carr and "
            "Dilip Madan's trick, in 1999: multiply by e to the alpha k. As alpha grows the curve bends into a hump "
            "that dies off on both sides. Now it has a transform. <bookmark mark='b'/> On the right, that transform: "
            "oscillating and decaying, computable in closed form from the characteristic function."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cur), FadeIn(rd))
            vo.wait_until("a")
            self.play(al.animate.set_value(1.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(h), Create(re), Create(im), FadeIn(leg))
        for x in (cur, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\psi(u)", r"=", r"\int e^{iuk}e^{\alpha k}c_T(k)\,dk = \frac{e^{-rT}\varphi(u - (\alpha + 1)i)}{\alpha^2 + "
                  r"\alpha - u^2 + i(2\alpha + 1)u}", font_size=30, colors={r"\psi(u)": OPT}),
            cmath(r"c_T(k)", r"=", r"\frac{e^{-\alpha k}}{\pi}\int_0^\infty e^{-iuk}\,\psi(u)\,du", font_size=34,
                  colors={r"c_T(k)": GOOD}),
            cmath(r"u_j = j\eta,\ \ k_m = -b + m\lambda", r",\quad", r"\lambda\eta = \frac{2\pi}{N}", font_size=34,
                  colors={r",\quad": GREY_B}),
            cmath(r"\mathbb{E}\big[S_T^{\alpha + 1}\big]", r"<", r"\infty", font_size=34, colors={r"<": BAD}),
        ]
        whys = [why(r"Fubini: swap the payoff's integral with the strike integral, then integrate $e^{(\alpha + iu)k}$ "
                    r"against $(e^x - e^k)^+$ in closed form"),
                why(r"invert; the price is real, so half the line suffices"),
                why(r"discretise for the FFT, whose kernel is $e^{-2\pi ijm/N}$: frequency step times strike step is "
                    r"forced (problem 8). Simpson weights tame the endpoint"),
                why(r"$\alpha$ needs that moment: for Heston it can fail at long maturities beyond a critical $\alpha$ "
                    r"(moment explosions; Andersen and Piterbarg)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "The derivation. Write the damped call's transform and swap the order of integration: the strike "
            "integral can be done in closed form, leaving the characteristic function evaluated at a shifted complex "
            "point, over a quadratic. <bookmark mark='a'/> Invert, and since the price is real, half the frequency "
            "line suffices. <bookmark mark='b'/> To use one fast Fourier transform for a whole grid of strikes, put "
            "frequencies at multiples of eta and log-strikes at multiples of lambda; the transform's kernel forces "
            "their product to be two pi over N. <bookmark mark='c'/> And alpha cannot be anything: the damped call "
            "needs the moment of order alpha plus one, which Heston loses at long maturities."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def grid(self, f):
        N = ValueTracker(4096)
        eta = ValueTracker(0.25)
        line_u = NumberLine(x_range=[0, 12, 1], length=10.0, include_numbers=False, color=GREY_C).shift(UP * 1.6)
        line_k = NumberLine(x_range=[-0.3, 0.3, 0.1], length=10.0, include_numbers=False, color=GREY_C).shift(DOWN * 0.4)

        def ticks_u():
            e = eta.get_value()
            return VGroup(*[Line(line_u.n2p(x) + UP * 0.15, line_u.n2p(x) + DOWN * 0.15, stroke_color=GOOD, stroke_width=2)
                            for x in np.arange(0, 12, e)][:200])

        def ticks_k():
            lam = 2 * np.pi / (N.get_value() * eta.get_value())
            xs = np.arange(-0.3, 0.3001, lam) if lam > 0.004 else np.arange(-0.3, 0.3001, 0.004)
            return VGroup(*[Line(line_k.n2p(x) + UP * 0.15, line_k.n2p(x) + DOWN * 0.15, stroke_color=OPT, stroke_width=2)
                            for x in xs])

        tu, tk = always_redraw(ticks_u), always_redraw(ticks_k)
        lu = label(r"frequency grid, step $\eta$", font_size=20, color=GOOD).next_to(line_u, UP, buff=0.3)
        lk = label(r"log-strike grid, step $\lambda = 2\pi/(N\eta)$ (around the money)", font_size=20, color=OPT)
        lk.next_to(line_k, UP, buff=0.3)
        rd = VGroup(readout(r"N =", lambda: N.get_value(), digits=0, font_size=30),
                    readout(r"\eta =", lambda: eta.get_value(), digits=3, font_size=30),
                    readout(r"\lambda =", lambda: 2 * np.pi / (N.get_value() * eta.get_value()), digits=4, font_size=30)
                    ).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.4)
        cm = [x for x in f["rows"] if x["method"] == "Carr-Madan"]
        tab = VGroup(*[MathTex(rf"N = {x['N']:,}".replace(",", "{,}") + rf":\ \ \text{{error}}\ {sci(x['err'], 1)}", font_size=26,
                               color=METHOD_COL["Carr-Madan FFT"]) for x in cm]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.to_edge(DOWN, buff=0.4)
        last = cm[-1]["err"]
        q = predict(r"$N$ doubles with $\eta$ fixed. What happens to the strike spacing?", width=4.8,
                    font_size=19).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The trade-off is a pair of rulers. The frequency grid has step eta; the strike grid has step lambda, "
            "and their product is fixed. <bookmark mark='a'/> Shrink eta to integrate more accurately, and the "
            "strikes spread apart until only a few land near the money. <bookmark mark='b'/> Pause and predict: "
            "double N with eta fixed. The strike spacing halves. The House's Carr–Madan price of the Heston call "
            f"improves from an error of {cm[0]['err']:.3f} with 512 points to about {last * 1e5:.1f} in a hundred "
            "thousand with sixteen thousand."
        ) as vo:
            self.play(Create(line_u), Create(line_k), FadeIn(tu), FadeIn(tk), FadeIn(lu), FadeIn(lk), FadeIn(rd))
            vo.wait_until("a")
            self.play(eta.animate.set_value(0.05), run_time=3)
            self.play(eta.animate.set_value(0.25), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(q), N.animate.set_value(8192), run_time=2)
            self.play(FadeIn(tab))
        for x in (tu, tk, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lewis(self, lw):
        u = np.asarray(lw["u"])
        integ = np.asarray(lw["lewis_integrand"])
        g = axes([0, 25], [-0.2, 1.1], x_length=5.4, y_length=3.2, xlabel=r"$u$",
                 ylabel=r"Lewis's integrand at $\mathrm{Im}\,u = -\tfrac12$", xticks=[0, 10, 20], yticks=[0, 1],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(UP * 0.8)
        cur = curve(g.ax, u, integ / integ.max(), GOOD, stroke_width=3)
        row = cmath(r"C", r"=", r"S_0 - \frac{\sqrt{S_0K}}{\pi}\int_0^\infty \mathrm{Re}\big[e^{iuk}\varphi(u - \tfrac i2)\big]"
                    r"\frac{du}{u^2 + \frac14}", font_size=32, colors={r"C": OPT}).to_edge(DOWN, buff=1.2)
        al = np.asarray(lw["alphas"])
        e = np.asarray(lw["cm_err"])
        h = axes([0, 4.2], [-3.5, 0.5], x_length=4.6, y_length=3.0, xlabel=r"damping $\alpha$",
                 ylabel=r"Carr--Madan error, $N = 4{,}096$ ($\log_{10}$)", xticks=[1, 2, 3, 4], yticks=[-3, -2, -1, 0],
                 font_size=14).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        ok = np.isfinite(e)
        ce = polyline(h.ax, al[ok], np.clip(np.log10(e[ok]), -3.5, 0.5), METHOD_COL["Carr-Madan FFT"], radius=0.05)
        diff = abs(lw["diff"])
        res = MathTex(rf"\text{{Lewis}}\ {lw['lewis']:.10f},\ \ \text{{COS}}\ {lw['ref']:.10f},\ \ |\text{{diff}}| < 10^{{-12}}"
                      if diff < 1e-12 else rf"\text{{Lewis}}\ {lw['lewis']:.10f},\ \ \text{{COS}}\ {lw['ref']:.10f}",
                      font_size=26, color=GOOD).to_edge(DOWN, buff=0.4)
        floor = e[ok][-1]
        digits = int(min(12, np.floor(-np.log10(max(diff, 1e-16)))))
        with self.voiceover(
            "Alan Lewis showed in 2001 that the damping is a choice of contour. Move the integration line in the "
            "complex plane to imaginary part minus one half, and the call becomes the stock price minus one real "
            "integral, whose integrand is smooth and decays fast. <bookmark mark='a'/> Done by adaptive quadrature, "
            f"it agrees with the cosine method of the next chapter to {digits} decimal places: two independent "
            "derivations, one number. <bookmark mark='b'/> And Carr–Madan's damping, measured: too little, and the "
            "error is large; from about one onward it no longer matters, because the floor of "
            f"{floor:.4f} is set by the grid of strikes, not by alpha."
        ) as vo:
            self.play(FadeIn(g), Create(cur), FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(h), Create(ce))
        self.wait(0.5)
        self.clear_scene()
