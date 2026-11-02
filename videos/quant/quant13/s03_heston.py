from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import stochvol as sv
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, real_data


class Heston(VoiceoverScene):
    def construct(self):
        c = load("calibrate")
        q = load("qe")
        self.card()
        self.model()
        self.rivers(c)
        self.fit(c)
        self.qe(q)

    def card(self):
        c = chapter_card(2, r"Heston's model", r"Can a second river price the smile in closed form?", lit=(1993,), part=PART)
        with self.voiceover("Chapter two. Heston's model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\frac{dS}{S}", r"=", r"\sqrt{v_t}\,dW^1_t", font_size=36, colors={r"\frac{dS}{S}": SPOT}),
                cmath(r"dv_t", r"=", r"\kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW^2_t,\quad dW^1 dW^2 = \rho\,dt",
                      font_size=36, colors={r"dv_t": VAR}),
                cmath(r"\mathbb{E}\big[e^{iu \ln S_T/F}\big]", r"=", r"e^{C(u, T) + D(u, T)\,v_0},\quad "
                      r"\partial_T D = \tfrac12\xi^2 D^2 - (\kappa - \rho\xi iu)D - \tfrac12(u^2 + iu)", font_size=32,
                      colors={r"\mathbb{E}\big[e^{iu \ln S_T/F}\big]": OPT}),
                cmath(r"2\kappa\theta", r"\ge", r"\xi^2", font_size=36, colors={r"2\kappa\theta": VAR})]
        whys = [why(r"the price, driven by the square root of a variance $v$"),
                why(r"the variance is Part 5's CIR process: pulled toward $\theta$ at speed $\kappa$, shaken by the vol of "
                    r"vol $\xi$; $\rho$ ties the two rivers"),
                why(r"Heston (1993): the characteristic function solves a Riccati equation in closed form; option prices "
                    r"follow by one Fourier integral (here, Fang and Oosterlee's COS method)"),
                why(r"Feller's condition: when it holds, the variance never touches zero")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.2, buff=0.65, edge=6.9)
        with self.voiceover(
            "Steven Heston's model, from 1993, is the simplest way to write the second river down. The price moves "
            "with the square root of a variance. <bookmark mark='a'/> The variance is Part five's mean-reverting "
            "square-root process: pulled toward a long-run level theta at speed kappa, and shaken by its own "
            "volatility, xi. Rho correlates the two noises, and rho is what tilts the smile. "
            "<bookmark mark='b'/> Heston's insight was that this model has a closed-form characteristic function: "
            "the exponent is linear in today's variance, with coefficients that solve a Riccati equation. One "
            "Fourier integral then prices any vanilla, in microseconds. <bookmark mark='c'/> And Feller's condition "
            "says when the variance stays strictly positive."
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

    def rivers(self, c):
        x = c["fits"]["Heston"]["x"]
        n, days = 120, 120
        S, v = sv.heston_qe(1.0, *x, days / 365, n, 6, seed=31, return_v=True)
        t = np.arange(n + 1)
        g1 = axes([0, days], [0.6, 1.5], x_length=9.0, y_length=2.4, ylabel=r"price", xticks=[0, 30, 60, 90, 120],
                  yticks=[0.75, 1.0, 1.25], font_size=16).to_edge(UP, buff=0.6)
        g2 = axes([0, days], [0, 1.6], x_length=9.0, y_length=2.4, xlabel=r"days", ylabel=r"volatility $\sqrt{v}$",
                  xticks=[0, 30, 60, 90, 120], yticks=[0, 0.5, 1.0, 1.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16).next_to(g1, DOWN, buff=0.35)
        VGroup(g1, g2).to_edge(LEFT, buff=0.6)
        cols = [SPOT, OPT, RV, IV, VAR, GREY_A]
        pS = VGroup(*[curve(g1.ax, t, np.clip(S[:, i], 0.6, 1.5), cols[i], stroke_width=2) for i in range(6)])
        pv = VGroup(*[curve(g2.ax, t, np.clip(np.sqrt(v[:, i]), 0, 1.6), cols[i], stroke_width=2) for i in range(6)])
        side = VGroup(
            wrapped_label(r"six paths of the Heston model fitted to the Surface: each price path (top) and its own "
                          r"volatility (bottom), in the same colour", 3.4, 19, GREY_A),
            wrapped_label(r"the volatility touches zero and leaps back: the fitted model breaks Feller's condition", 3.4,
                          19, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulated with Andersen's QE scheme, daily steps")
        with self.voiceover(
            "Here are the two rivers, simulated from the Heston model fitted to the Surface. Each colour is one "
            "world: its price on top, and its own volatility underneath. <bookmark mark='a'/> When a path's "
            "volatility spikes, its price swings harder, and, because rho is negative, the spikes tend to come with "
            "falls. Notice how violently the volatility moves, touching zero and leaping back. That is what it took "
            "to fit Bitcoin's smile."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[AnimationGroup(Create(a), Create(b)) for a, b in zip(pS, pv)], lag_ratio=0.25,
                                  run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, c):
        h = c["fits"]["Heston"]
        p = h["params"]
        days = sorted(int(d) for d in h["by_expiry"])
        bsx = [c["fits"]["BS"]["by_expiry"][str(d)] for d in days]
        hsx = [h["by_expiry"][str(d)] for d in days]
        g = axes([-0.6, len(days) - 0.4], [0, 8], x_length=6.6, y_length=3.6, xlabel=r"expiry (days)",
                 ylabel=r"fit error (vol points)", xticks=list(range(len(days))), xfmt=lambda u: str(days[int(round(u))]),
                 yticks=[0, 2, 4, 6, 8], font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        ax = g.ax
        w = 0.32

        def bar(i, v, dx, col):
            return Rectangle(width=w, height=max(abs(ax.c2p(0, min(v, 8))[1] - ax.c2p(0, 0)[1]), 1e-3), stroke_width=0,
                             fill_color=col, fill_opacity=0.85).move_to(ax.c2p(i + dx, min(v, 8) / 2))

        b1 = VGroup(*[bar(i, v, -0.18, MODEL_COL["BS"]) for i, v in enumerate(bsx)])
        b2 = VGroup(*[bar(i, v, 0.18, MODEL_COL["Heston"]) for i, v in enumerate(hsx)])
        leg = legend([(MODEL_COL["BS"], rf"Black--Scholes, one vol: {c['fits']['BS']['rmse']:.1f} overall"),
                      (MODEL_COL["Heston"], rf"Heston, five numbers: {h['rmse']:.2f} overall")], font_size=17).next_to(
            g, UP, buff=0.15).align_to(g, LEFT)
        tab = VGroup(*[MathTex(s, font_size=28) for s in (
            rf"\sqrt{{v_0}} = {100 * np.sqrt(p['v0']):.0f}\%,\ \ \sqrt{{\theta}} = {100 * np.sqrt(p['theta']):.0f}\%",
            rf"\kappa = {p['kappa']:.1f}\ \ (\text{{half-life}}\ {365 * np.log(2) / p['kappa']:.0f}\ \text{{days}})",
            rf"\xi = {p['xi']:.1f},\ \ \rho = {p['rho']:.2f}",
            rf"2\kappa\theta / \xi^2 = {c['feller']:.2f} < 1")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tab[3].set_color(BAD)
        note_ = wrapped_label(r"a vol of vol of several hundred percent: Heston fits the Surface only by making its "
                              r"variance violent; the 3-day options are still missed by several points", 4.6, 19, GREY_A)
        side = VGroup(tab, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"the Surface: {c['n']} quotes, vega-weighted, fitted by the House's calibrator")
        with self.voiceover(
            "Now fit it. The House's calibrator prices every option on the Surface by Fourier, compares implied "
            "volatilities, and moves the five parameters until the vega-weighted error is smallest. A single "
            f"Black–Scholes volatility misses by {c['fits']['BS']['rmse']:.1f} points. <bookmark mark='a'/> Heston "
            f"misses by {h['rmse']:.1f}. <bookmark mark='b'/> But look at what it took. Mean reversion with a "
            f"half-life of {365 * np.log(2) / p['kappa']:.0f} days. A volatility of volatility of "
            f"{100 * p['xi']:.0f} percent. Feller's condition fails by a factor of almost three. And the shortest "
            "expiry, three days, is still missed by five points. Heston can bend its smile only so fast: in "
            "chapter four, we will see where that limit comes from."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1],
                                                                          lag_ratio=0.1, run_time=1.5))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.1, run_time=1.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=2.5), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def qe(self, q):
        rows = q["rows"]
        ns = sorted({r["n"] for r in rows})
        ex = q["exact"]["1.0"]
        g = axes([np.log10(1.5), np.log10(180)], [-0.05, 0.25], x_length=6.8, y_length=4.0, xlabel=r"time steps (3 months)",
                 ylabel=r"error of the Monte Carlo price, \% of price", xticks=[np.log10(n) for n in ns],
                 xfmt=lambda u: f"{10 ** u:.0f}", yticks=[0, 0.1, 0.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16,
                 log_x=True).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax

        def line(scheme, col):
            pts = [(np.log10(r["n"]), r["bias"] / ex) for r in rows if r["scheme"] == scheme and r["K"] == 1.0]
            dots = VGroup(*[Dot(ax.c2p(*p_), radius=0.06, color=col) for p_ in pts])
            ln = VMobject(stroke_color=col, stroke_width=3).set_points_as_corners([ax.c2p(*p_) for p_ in pts])
            return VGroup(ln, dots)

        eu, qe = line("Euler", BAD), line("QE", RV)
        zero = DashedLine(ax.c2p(np.log10(1.5), 0), ax.c2p(np.log10(180), 0), stroke_color=GREY_C, stroke_width=1.5)
        leg = legend([(BAD, r"Euler, variance floored at zero"), (RV, r"Andersen's QE scheme (2008)")],
                     font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        e2 = next(r for r in rows if r["scheme"] == "Euler" and r["n"] == 2 and r["K"] == 1.0)
        q2 = next(r for r in rows if r["scheme"] == "QE" and r["n"] == 2 and r["K"] == 1.0)
        side = VGroup(
            wrapped_label(r"pricing a 3-month at-the-money call under the fitted Heston, 200{,}000 paths, against the exact "
                          r"Fourier price", 4.4, 19, GREY_A),
            wrapped_label(rf"with 2 steps, Euler is {100 * e2['rel']:.0f}\% too high and QE {100 * abs(q2['rel']):.0f}\% too "
                          r"low; from 16 steps, QE is inside the Monte Carlo noise", 4.4, 20, WHITE),
            wrapped_label(r"QE matches the variance's true conditional mean and variance step by step: a squared "
                          r"Gaussian when $v$ is large, a point mass at zero plus an exponential when it is small", 4.4,
                          19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "When Feller's condition fails, simulating Heston is hard: a plain Euler step drives the variance "
            "negative, and flooring it at zero biases the price. Here is the error in pricing a three-month "
            "at-the-money call, against the exact Fourier price. <bookmark mark='a'/> Euler, with two steps, is "
            f"{100 * e2['rel']:.0f} percent too high, and needs dozens of steps to get inside the noise. "
            "<bookmark mark='b'/> Leif Andersen's quadratic-exponential scheme, from 2008, draws the next variance "
            "from a distribution that matches its true conditional mean and variance: a squared Gaussian when the "
            "variance is large, a spike at zero plus an exponential tail when it is small. With two steps its error "
            f"is about {100 * abs(q2['rel']):.0f} percent, and from sixteen it disappears into the noise. It is the "
            "House's Heston simulator."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Create(eu[0]), FadeIn(eu[1]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(qe[0]), FadeIn(qe[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()
