from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load, pause


class Lift(VoiceoverScene):
    def construct(self):
        L = load("lift")
        lp = load("lift_paths")
        self.card()
        self.grow(L)
        self.derive()
        self.paths(lp)
        self.errors(L, lp)

    def card(self):
        c = chapter_card(10, r"Markovian lifts", r"Can a rough model be made Markovian?", lit=(2019,), part=PART)
        with self.voiceover("Chapter ten. Markovian lifts."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def grow(self, L):
        from scipy.special import gamma as G
        from explainer.quant.house import rough as R
        H = L["H"]
        a = H + 0.5
        t = np.exp(np.linspace(np.log(1e-3), np.log(1.0), 120))
        g = axes([-3, 0], [-1.0, 2.5], x_length=7.4, y_length=4.4, xlabel=r"lag $t$ (years, log scale)",
                 ylabel=r"kernel (log scale)", xticks=[-3, -2, -1, 0], xfmt=lambda u: f"10^{{{int(u)}}}",
                 yticks=[-1, 0, 1, 2], yfmt=lambda u: f"10^{{{int(u)}}}", log_x=True, font_size=15).to_edge(LEFT, buff=0.6)
        ax = g.ax
        exact = curve(ax, np.log10(t), np.log10(t ** (a - 1) / G(a)), ROUGH, stroke_width=4)
        N = ValueTracker(1)

        def parts():
            n = int(round(N.get_value()))
            c, x = R.lift_weights(H, n)
            grp = VGroup()
            for i in range(n):
                y = c[i] * np.exp(-x[i] * t)
                ok = y > 0.1
                if ok.sum() > 1:
                    grp.add(curve(ax, np.log10(t[ok]), np.clip(np.log10(y[ok]), -1.0, 2.5),
                                  interpolate_color(ManimColor(VAR), ManimColor(IV), i / max(n - 1, 1)), stroke_width=1.2))
            tot = (c[None, :] * np.exp(-x[None, :] * t[:, None])).sum(1)
            grp.add(curve(ax, np.log10(t), np.clip(np.log10(np.maximum(tot, 0.1)), -1.0, 2.5), YELLOW, stroke_width=3))
            return grp

        P = always_redraw(parts)
        Nr = readout(r"N =", lambda: round(N.get_value()), digits=0, font_size=34, color=YELLOW).to_corner(UR, buff=0.5)
        leg = legend([(ROUGH, r"the rough kernel"), (VAR, r"one exponential per factor"), (YELLOW, r"their sum")],
                     font_size=17).next_to(Nr, DOWN, buff=0.3).align_to(Nr, RIGHT)
        q = pause(r"One exponential per decade of time: how many to cover lags from one minute to one year?", width=5.0,
                  font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "A rough model has no Markovian state: today's volatility depends on the whole past, which makes "
            "simulation slow and hedging awkward. Eduardo Abi Jaber and Omar El Euch found a way back: the rough "
            "kernel is a mixture of exponentials. Watch the sum build. One exponential matches the kernel at one "
            "lag only. Add them "
            "one at a time, on geometrically spaced rates. Each new exponential is a thin curve, and the yellow sum "
            "crawls up the power law decade by decade. <bookmark mark='a'/> Pause and predict: if each decade of "
            "time needs about one exponential, how many cover lags from a minute to a year? "
            "<bookmark mark='b'/> A year is about half a million minutes: between five and six decades, so about "
            "six. The power law is scale invariance, and scale invariance costs one factor per decade."
        ) as vo:
            self.play(FadeIn(g), Create(exact), FadeIn(P), FadeIn(Nr), FadeIn(leg))
            self.play(N.animate.set_value(50), run_time=max(vo.remaining(0.0) * 0.5, 5), rate_func=rate_functions.ease_in_quad)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
        P.clear_updaters()
        Nr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\int_0^\infty e^{-xt}x^{-\alpha}\,dx", r"=", r"\Gamma(1 - \alpha)\,t^{\alpha - 1}", font_size=38,
                      colors={r"\int_0^\infty e^{-xt}x^{-\alpha}\,dx": GREY_A}),
                cmath(r"\frac{t^{\alpha - 1}}{\Gamma(\alpha)}", r"=", r"\int_0^\infty e^{-xt}\,\mu(dx),\quad \mu(dx) = "
                      r"\frac{x^{-\alpha}\,dx}{\Gamma(\alpha)\Gamma(1 - \alpha)}", font_size=36,
                      colors={r"\frac{t^{\alpha - 1}}{\Gamma(\alpha)}": ROUGH}),
                cmath(r"K(t)", r"\approx", r"\sum_{i = 1}^N c_i\,e^{-x_i t}", font_size=38, colors={r"K(t)": ROUGH}),
                cmath(r"V_t", r"=", r"g_0(t) + \sum_i c_i U^i_t,\quad dU^i_t = \big(-x_iU^i_t - \lambda V_t\big)dt + "
                      r"\nu\sqrt{V_t}\,dW_t", font_size=34, colors={r"V_t": VAR})]
        whys = [why(r"substitute $y = xt$: the Gamma function appears"),
                why(r"divide by $\Gamma(\alpha)\Gamma(1 - \alpha)$: the kernel is completely monotone, a mixture of exponentials "
                    r"(Bernstein)"),
                why(r"quantise the mixing measure on $N$ geometric nodes $x_i$ with weights $c_i$"),
                why(r"each exponential is one mean-reverting factor; the model is Markov in $N + 1$ dimensions (Abi Jaber "
                    r"2019, the lifted Heston)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.8, buff=0.75, edge=6.9)
        with self.voiceover(
            "Why is a power law a mixture of exponentials? Integrate e to the minus x t against x to the minus "
            "alpha: substitute y equals x t, and out comes gamma of one minus alpha times t to the alpha minus one. "
            "<bookmark mark='a'/> So the fractional kernel is exactly an integral of exponentials against a "
            "mixing measure: a completely monotone function. <bookmark mark='b'/> Replace the integral by N nodes "
            "with weights, and the kernel becomes a finite sum. <bookmark mark='c'/> Each exponential becomes a "
            "factor U i with its own mean reversion x i, all driven by the same Brownian motion. The variance is the "
            "initial curve plus a weighted sum of factors: a Markov model in N plus one dimensions, and Eduardo "
            "Abi Jaber's lifted Heston, practical with twenty factors."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def paths(self, lp):
        t = np.asarray(lp["t"]) * 365
        P = lp["paths"]
        ex = np.asarray(P["exact"])
        hi = float(np.percentile(np.abs(ex), 99.5)) * 1.2
        g = axes([0, t[-1]], [-0.2, hi], x_length=10.0, y_length=4.2, xlabel=r"days", ylabel=r"variance $V_t$",
                 xticks=[0, 30, 60, 90], yticks=[0, round(hi / 2, 1)], font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        ref = curve(ax, t, np.clip(ex, -0.2, hi), WHITE, stroke_width=2.4)
        cols = {"1": GREY_B, "5": VAR, "20": IV, "50": OPT, "200": RV}
        cur = curve(ax, t, np.clip(np.asarray(P["1"]), -0.2, hi), cols["1"], stroke_width=2)
        tag = label(r"lift, $N = 1$", font_size=24, color=cols["1"]).to_corner(UR, buff=0.4)
        leg = legend([(WHITE, r"exact kernel (fine Volterra scheme), the same shocks")], font_size=17).to_corner(UL, buff=0.4)
        src = illustration(r"rough Heston, $H = 0.1$ (chapter 7's fit); one path of 200", corner=DR)
        with self.voiceover(
            "Now a path. The white line is one rough Heston variance path from a fine scheme with the exact kernel. "
            "Drive the lift with the very same shocks, first with one factor: it is a Heston path, too smooth. "
            "<bookmark mark='a'/> Five factors, twenty, fifty, two hundred: the lifted path creeps toward the "
            "exact one, catching more of its fine wiggles with each new fast factor."
        ) as vo:
            self.play(FadeIn(g), Create(ref), FadeIn(leg), FadeIn(src), Create(cur), FadeIn(tag))
            vo.wait_until("a")
            for k in ("5", "20", "50", "200"):
                self.play(Transform(cur, curve(ax, t, np.clip(np.asarray(P[k]), -0.2, hi), cols[k], stroke_width=2)),
                          Transform(tag, label(rf"lift, $N = {k}$", font_size=24, color=cols[k]).to_corner(UR, buff=0.4)),
                          run_time=1.5)
                self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    def errors(self, L, lp):
        rows = L["rows"]
        tab = VGroup(VGroup(label(r"factors $N$", font_size=24, color=GREY_A),
                            label(r"30-day smile error (vol points)", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.8))
        for r in rows:
            tab.add(VGroup(MathTex(str(r["N"]), font_size=30), MathTex(f"{r['iv_err']:.2f}", font_size=30,
                                                                         color=RV if r["iv_err"] < 0.5 else BAD)))
        for row in tab[1:]:
            row[0].move_to(tab[0][0].get_center() * RIGHT + row[0].get_center() * UP)
            row[1].move_to(tab[0][1].get_center() * RIGHT + row[1].get_center() * UP)
        tab[1:].arrange(DOWN, buff=0.25)
        for row in tab[1:]:
            row[0].set_x(tab[0][0].get_x())
            row[1].set_x(tab[0][1].get_x())
        tab[1:].next_to(tab[0], DOWN, buff=0.35)
        tab.move_to(LEFT * 2.2)
        side = wrapped_label(r"against rough Heston with $H = 0.1$, fitted to the Surface in chapter 7, solved exactly by the fractional "
                             r"Adams scheme; the lift (Abi Jaber and El Euch 2019) is a Heston model with $N$ variance factors and no fractional calculus",
                             4.6, 20, GREY_A).to_edge(RIGHT, buff=0.6)
        src = illustration(r"13 strikes, $\pm 30\%$; the House's \texttt{lifted\_heston\_cf}")
        with self.voiceover(
            "How many factors are enough? Price the thirty-day smile of a rough Heston model with H of a tenth, fitted "
            "to the Surface in chapter seven, exactly, and with lifts of growing size. <bookmark mark='a'/> One factor "
            f"is a Heston model with the wrong memory, and misses by {rows[0]['iv_err']:.1f} volatility points. Ten "
            f"factors cut that to {rows[3]['iv_err']:.1f}, twenty to {rows[4]['iv_err']:.1f}, fifty to "
            f"{rows[5]['iv_err']:.2f}. In law, the lift converges fast. Path by path it converges slowly: the distance "
            f"between lifted and exact paths is still {lp['rows'][3]['dist']:.2f} standard deviations at fifty factors, "
            "because the kernel's spike lives below the fastest factor's time scale. The roughness was never magic: it is many time scales at once, and a model with enough of "
            "them prices the same."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(side), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()
