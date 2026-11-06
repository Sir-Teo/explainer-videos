from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import control as C
from videos.quant.quant8.common import predict, ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class SmoothFit(VoiceoverScene):
    def construct(self):
        p = load("perpetual_put")
        self.card()
        self.derive(p)
        self.slider(p)
        self.finite(load("american"), p)

    def card(self):
        c = chapter_card(12, r"Free boundaries: smooth fit and the American put", r"Where exactly should you stop?",
                         part=PART)
        with self.voiceover("Chapter twelve. Free boundaries: smooth fit, and the American put."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self, p):
        rows = [cmath(r"\tfrac12\sigma^2S^2V'' + rSV' - rV", r"=", r"0\quad (S > b)", font_size=32),
                cmath(r"V(S)", r"=", r"A\,S^{-\beta},\qquad \beta = \frac{2r}{\sigma^2}", font_size=32,
                      colors={r"V(S)": VALUE}),
                cmath(r"V_b(S)", r"=", r"(K - b)\Big(\frac{S}{b}\Big)^{-\beta}", font_size=32, colors={r"V_b(S)": VALUE}),
                cmath(r"\frac{d}{db}(K - b)\,b^{\beta} = 0", r"\ \Rightarrow\ ", r"b^* = \frac{\beta K}{1 + \beta}"
                      r"\iff V_{b^*}'(b^*) = -1", font_size=32, colors={r"b^* = \frac{\beta K}{1 + \beta}": KELLY})]
        whys = [why(r"no-dividend GBM under $Q$, $r,\sigma>0$, $0<b<K$, $S>b$: the perpetual Black--Scholes equation", font_size=21),
                why(r"try a power: $\frac12\sigma^2 k(k-1) + rk - r = 0$ has roots $1$ and $-\beta$; the put must vanish "
                    r"as $S \to \infty$", font_size=21),
                why(r"value matching: at $S = b$ you exercise and get $K - b$ (McKean 1965)", font_size=21),
                why(r"choose $b$ to make the value largest: the derivative condition is exactly that the curve leaves "
                    r"the payoff with the payoff's slope, $-1$: smooth fit", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "In continuous time the stopping rule becomes a boundary in space, and nobody tells you where it is. Take the "
            "simplest case: an American put that never expires, the right to sell a stock at K whenever you like. While you "
            "hold it, above some exercise level b, its value obeys the Black-Scholes equation with no time derivative. "
            "<bookmark mark='a'/> Try a power of S. The exponent solves a quadratic with roots one and minus beta, and only "
            "the negative root keeps the put worthless when the stock is huge. <bookmark mark='b'/> Value matching: at the "
            "level b you exercise and receive K minus b, which fixes the constant. Henry McKean solved this in 1965. "
            "<bookmark mark='c'/> Which level? The one that makes the value largest. Differentiate in b, and the condition "
            "is the same as asking the value to leave the payoff with the payoff's own slope, minus one, with no kink: smooth "
            f"fit. With five percent rates and thirty percent volatility, the boundary is {p['b_star']:.1f}."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def slider(self, p):
        K, r, s, beta, bs = p["K"], p["r"], p["sigma"], p["beta"], p["b_star"]
        g = axes([20, 160], [0, 80], x_length=6.6, y_length=4.4, xlabel=r"stock price $S$", ylabel=r"value",
                 xticks=[40, 60, 80, 100, 120, 140], yticks=[0, 20, 40, 60, 80], font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        S = np.linspace(20, 160, 281)
        pay = curve(ax, S, np.maximum(K - S, 0), GREY_B, stroke_width=3)
        b = ValueTracker(32.0)
        fam = always_redraw(lambda: curve(ax, S, np.minimum(C.perpetual_put_value(S, K, r, s, b.get_value()), 80),
                                          VALUE, stroke_width=4))
        bdot = always_redraw(lambda: Dot(ax.c2p(b.get_value(), K - b.get_value()), color=KELLY, radius=0.09))
        hund = always_redraw(lambda: Dot(ax.c2p(100, float(C.perpetual_put_value(100.0, K, r, s, b.get_value()))),
                                         color=UNDER, radius=0.08))
        g2 = axes([30, 95], [0, 25], x_length=4.6, y_length=2.6, xlabel=r"exercise level $b$",
                  ylabel=r"value at $S = 100$", xticks=[40, 60, 80], yticks=[15, 20, 25], font_size=15)
        g2.to_corner(UR, buff=0.5)
        bg, vb = np.asarray(p["b_grid"]), np.asarray(p["v_of_b"])
        vcurve = curve(g2.ax, bg, vb, UNDER, stroke_width=3)
        vdot = always_redraw(lambda: Dot(g2.ax.c2p(b.get_value(), float(C.perpetual_put_value(100.0, K, r, s, b.get_value()))), color=UNDER, radius=0.08))
        gap = DecimalNumber(-beta * (K - 32.0) / 32.0 + 1, num_decimal_places=2, include_sign=True, font_size=30,
                            color=KELLY)
        gap.add_updater(lambda m: m.set_value(-beta * (K - b.get_value()) / b.get_value() + 1))
        gl = VGroup(MathTex(r"V_b'(b^+) - (-1) =", font_size=30, color=KELLY), gap).arrange(RIGHT, buff=0.12)
        gl.next_to(g2, DOWN, buff=0.5).align_to(g2, LEFT)
        res = VGroup(
            MathTex(rf"b^* = {bs:.1f},\quad V(100) = {p['v100']:.2f}", font_size=30, color=KELLY),
            MathTex(rf"\text{{40-year tree: }} {p['tree_boundary0']:.1f},\ \ {p['tree_price']:.2f}", font_size=28,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(gl, DOWN, buff=0.4).align_to(gl, LEFT)
        q = predict(r"Rates rise. Does the exercise boundary move up or down?", width=4.8, font_size=20).next_to(
            res, DOWN, buff=0.35).align_to(gl, LEFT)
        with self.voiceover(
            "Watch the choice. The grey line is the payoff; the blue curve is the value of the rule 'exercise the first time "
            "the stock falls to b', for a level we can slide. <bookmark mark='a'/> With a low level the curve meets the payoff "
            "at a kink, coming in too steeply; the readout is the gap between the two slopes. Raise the level and the value at a "
            "hundred rises; raise it too far and the curve meets the payoff too flatly, and the value falls again. "
            f"<bookmark mark='b'/> The best level, {bs:.1f}, is exactly where the gap closes and the curve kisses the payoff. "
            f"The put is worth {p['v100']:.2f}. A forty-year binomial tree that knows nothing of smooth fit puts its boundary "
            f"at {p['tree_boundary0']:.1f} and its price at {p['tree_price']:.2f}. <bookmark mark='c'/> Pause and predict: if "
            "rates rise, does the boundary move up or down? <bookmark mark='d'/> Up: beta grows and the boundary moves toward "
            f"the strike, to {p['b_star_r7']:.1f} at seven percent. Waiting to receive K costs more interest, so you exercise "
            "sooner."
        ) as vo:
            self.play(FadeIn(g), Create(pay), FadeIn(g2), Create(vcurve))
            self.add(fam, bdot, hund, vdot)
            self.play(FadeIn(gl))
            vo.wait_until("a")
            self.play(b.animate.set_value(90.0), run_time=5, rate_func=smooth)
            self.play(b.animate.set_value(bs), run_time=3, rate_func=smooth)
            vo.wait_until("b")
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
        for m in (fam, bdot, hund, vdot, gap):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def finite(self, a, p):
        t = np.asarray(a["t"])
        b = np.asarray(a["boundary"])
        ok = np.isfinite(b)
        bs = b.copy()
        idx = np.where(ok)[0]
        bs[idx] = np.convolve(np.pad(b[idx], 12, mode="edge"), np.ones(25) / 25, mode="valid")
        g = axes([0, 1], [50, 100], x_length=6.6, y_length=3.8, xlabel=r"time (years)", ylabel=r"stock price",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[50, 60, 70, 80, 90, 100], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bl = curve(ax, t[ok], bs[ok], OVER, stroke_width=4)
        perp = DashedLine(ax.c2p(0, p["b_star"]), ax.c2p(1, p["b_star"]), color=KELLY, stroke_width=2)
        pl = label(rf"perpetual: {p['b_star']:.1f}", font_size=18, color=KELLY).next_to(ax.c2p(0.02, p["b_star"]), UP,
                                                                                       buff=0.08).align_to(ax, LEFT)
        region = Polygon(*[ax.c2p(x, 50) for x in (t[ok][0],)], *[ax.c2p(x, y) for x, y in zip(t[ok], bs[ok])],
                         ax.c2p(t[ok][-1], 50), stroke_width=0, fill_color=OVER, fill_opacity=0.18)
        ex = label(r"exercise", font_size=22, color=OVER).move_to(ax.c2p(0.6, 62))
        wt = label(r"wait", font_size=22, color=UNDER).move_to(ax.c2p(0.3, 92))
        side = VGroup(
            label(r"one year: $K = 100$, $\sigma = 30\%$, $r = 5\%$", font_size=21, color=GREY_A),
            MathTex(rf"\text{{American: }} {a['american']:.2f},\ \ \text{{European: }} {a['european']:.2f}", font_size=28,
                    color=VALUE),
            MathTex(r"\min\big(-V_t - \mathcal{L}V + rV,\ V - g\big) = 0", font_size=32, color=KELLY),
            wrapped_label(r"the variational inequality: a viscosity solution (chapter 4), and the value of a reflected "
                          r"BSDE (El Karoui et al.\ 1997; chapter 14). Part 10 prices it, Part 16 by simulation", 4.4,
                          19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"500-step CRR tree; displayed boundary smoothed over 25 nodes; $\mathcal L=rS\partial_S+\frac12\sigma^2S^2\partial_{SS}$")
        with self.voiceover(
            "With an expiry, the boundary rises toward the strike as time runs out. <bookmark mark='a'/> The right to "
            f"choose when is worth {a['american'] - a['european']:.2f} on a one-year put. <bookmark mark='b'/> In general "
            "the value solves a variational inequality, is a viscosity solution, and is the value of a reflected backward "
            "equation: chapter fourteen's subject. First, a question no solver answers: how people actually decide."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), Create(perp), FadeIn(pl))
            self.play(Create(bl), FadeIn(region), FadeIn(ex), FadeIn(wt), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
