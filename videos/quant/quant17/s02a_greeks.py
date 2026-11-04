from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, illustration, load

ACTS = [("SiLU", NET, r"SiLU"), ("ReLU", BAD, r"ReLU"), ("softplus", GOOD, r"softplus")]


def _mean(g, key, act):
    return float(np.mean([g["runs"][f"{act}_{s}"][key] for s in (0, 1)]))


class Greeks(VoiceoverScene):
    def construct(self):
        g = load("greeks_act")
        self.card()
        self.panels(g)
        self.derive()
        self.butterfly(g)
        self.verdict(g)

    def card(self):
        c = chapter_card(2, r"A network's Greeks", r"Your network prices well. Are its derivatives right?", part=PART)
        with self.voiceover("Chapter two. A network's Greeks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def panels(self, g):
        xs = np.asarray(g["xs"])
        b = g["bs"]
        specs = [("price", r"price $C/K$", [0, 0.2], [0, 0.1, 0.2]), ("delta", r"delta", [-0.1, 1.1], [0, 0.5, 1]),
                 ("gamma", r"gamma", [-1, 7], [0, 3, 6])]
        panels = VGroup()
        for key, yl, yr, yt in specs:
            ax_ = axes([0.8, 1.2], yr, x_length=3.9, y_length=3.2, xlabel=r"$S/K$", ylabel=yl, xticks=[0.8, 1.0, 1.2],
                       yticks=yt, font_size=13)
            ref = DashedVMobject(curve(ax_.ax, xs, np.clip(np.asarray(b[key]), *yr), REF, stroke_width=2.5), num_dashes=30)
            lines = VGroup(*[curve(ax_.ax, xs, np.clip(np.asarray(g["runs"][f"{a}_0"][key]), *yr), col, stroke_width=3)
                             for a, col, _ in ACTS])
            panels.add(VGroup(ax_, ref, lines))
        panels.arrange(RIGHT, buff=0.45).shift(DOWN * 0.3)
        leg = legend([(REF, r"Black--Scholes")] + [(col, rf"network with {t}") for _, col, t in ACTS], font_size=16)
        leg.arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        src = illustration(r"the HLP data of chapter 1; three networks of 3 $\times$ 64 units, 100 epochs each; six weeks "
                           r"to expiry")
        with self.voiceover(
            "Take chapter one's data and fit it three times, with the same network and three different activation "
            "functions: the SiLU used so far, the rectified linear unit, ReLU, the default of modern deep learning, and "
            "the softplus. <bookmark mark='a'/> Their prices: you cannot tell them apart, and all three lie on "
            "Black–Scholes. <bookmark mark='b'/> Their deltas, the first derivative: the smooth activations follow the "
            "formula; the ReLU network's delta is a staircase, because a ReLU network is piecewise linear, and its "
            "slope jumps at every kink. <bookmark mark='c'/> Their gammas, the second derivative: the smooth ones "
            "trace the formula's hump. The ReLU network's gamma is zero, everywhere it is defined. Three networks with "
            "the same price; one of them cannot hedge convexity at all."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][0]), Create(panels[0][1]), *[Create(l_) for l_ in panels[0][2]])
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), Create(panels[1][1]), *[Create(l_) for l_ in panels[1][2]])
            vo.wait_until("c")
            self.play(FadeIn(panels[2][0]), Create(panels[2][1]), *[Create(l_) for l_ in panels[2][2]])
        self.wait(0.5)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\hat c(x)", r"=", r"W_2\,\phi(W_1 x + b_1) + b_2", font_size=40, colors={r"\hat c(x)": NET}),
                cmath(r"\partial_x^2 \hat c", r"=", r"W_2\,\big(\phi''(W_1 x + b_1) \odot (W_1)^2\big)", font_size=40,
                      colors={r"\partial_x^2 \hat c": DELTA}),
                cmath(r"\phi = \text{ReLU}", r"\Rightarrow", r"\phi'' = 0\ \text{a.e.}\ \Rightarrow\ \hat\Gamma = 0",
                      font_size=40, colors={r"\Rightarrow": BAD}),
                cmath(r"\partial_K^2 C", r"=", r"e^{-r\tau}\, q(K) \ \ge\ 0", font_size=40, colors={r"\partial_K^2 C": OPT})]
        whys = [why(r"one hidden layer, for the algebra: weights $W$, biases $b$, activation $\phi$ applied to each unit"),
                why(r"differentiate twice by the chain rule: the curvature of the network is a weighted sum of the "
                    r"activation's own curvature"),
                why(r"a ReLU is linear on each side of its kink: its second derivative vanishes except at kinks, where it "
                    r"is undefined. Deeper ReLU networks are still piecewise linear. So the gamma a ReLU network offers is "
                    r"zero almost everywhere, however well it prices"),
                why(r"Breeden and Litzenberger (Part 12): the second strike derivative of a call is the discounted risk-"
                    r"neutral density, so a price must be convex in the strike. A network can break this, and a negative "
                    r"butterfly is an arbitrage. Remedies: build convexity into the architecture (Dugas et al.\ 2009) or "
                    r"penalize it (Ackerer, Tagasovska and Vatter 2020); Part 12 builds arbitrage-free surfaces")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why? Write a network with one hidden layer: weights, biases, and an activation applied to every unit. "
            "<bookmark mark='a'/> Differentiate twice with the chain rule. The curvature of the whole network is a "
            "weighted sum of the curvature of its activation. <bookmark mark='b'/> A ReLU is a straight line on each "
            "side of its kink, so its second derivative is zero except at the kinks, where it does not exist. Stack as "
            "many layers as you like: the network stays piecewise linear, and its gamma is zero almost everywhere. "
            "<bookmark mark='c'/> And a price has a shape it must keep. From Breeden and Litzenberger, the second "
            "strike derivative of a call is the risk-neutral density, so a butterfly can never have a negative price. "
            "A network knows none of this unless you build it in, or penalize it."
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

    def butterfly(self, g):
        Ks = np.asarray(g["Ks"])[1:-1]
        bf = np.asarray(g["bs"]["fly"])
        top = float(bf.max()) * 1.3
        charts = VGroup()
        for a, col, t in ACTS:
            fly = np.asarray(g["runs"][f"{a}_0"]["fly"])
            ax_ = axes([0.8, 1.2], [-top * 0.6, top], x_length=3.9, y_length=3.0, xlabel=r"strike $K$ (spot 1)",
                       ylabel=r"butterfly price" if a == "SiLU" else "", xticks=[0.8, 1.0, 1.2], yticks=[0],
                       font_size=13)
            w = (ax_.ax.c2p(Ks[1], 0)[0] - ax_.ax.c2p(Ks[0], 0)[0]) * 0.7
            bars = VGroup()
            for k, v in zip(Ks, fly):
                v = float(np.clip(v, -top * 0.6, top))
                p0, p1 = ax_.ax.c2p(k, 0), ax_.ax.c2p(k, v)
                bars.add(Rectangle(width=w, height=max(abs(p1[1] - p0[1]), 0.005), stroke_width=0,
                                   fill_color=col if v >= 0 else BAD, fill_opacity=0.9 if v < 0 else 0.6).move_to(
                    [p0[0], (p0[1] + p1[1]) / 2, 0]))
            ref = curve(ax_.ax, Ks, bf, REF, stroke_width=2)
            neg = 100 * _mean(g, "neg_fly", a)
            ttl = label(rf"{t}: {neg:.0f}\% negative", font_size=19, color=col).next_to(ax_, UP, buff=0.1)
            charts.add(VGroup(ax_, ref, bars, ttl))
        charts.arrange(RIGHT, buff=0.45).shift(DOWN * 0.2)
        foot = wrapped_label(r"each bar: the price of a butterfly $C(K - h) - 2C(K) + C(K + h)$ from the network, $h = 0.01$; "
                             r"white, Black--Scholes'. A negative bar is a portfolio with a non-negative payoff and a "
                             r"negative price: money for nothing. Shares averaged over two seeds", 12.4, 18,
                             GREY_A).to_edge(DOWN, buff=0.35)
        negs = {a: 100 * _mean(g, "neg_fly", a) for a, _, _ in ACTS}
        with self.voiceover(
            "So test it. Fix the spot, and price butterflies across forty strikes with each network: one bar per strike, "
            "against Black–Scholes in white. <bookmark mark='a'/> A negative bar is an arbitrage: a portfolio that can "
            "never pay less than zero, offered at a negative price. The SiLU network prices "
            f"{negs['SiLU']:.0f} percent of its butterflies below zero, the softplus network {negs['softplus']:.0f} "
            f"percent, and the ReLU network {negs['ReLU']:.0f} percent. Where the true butterflies are tiny, far from "
            "the money, a network's small wiggles are enough to turn them negative."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(c[0], c[1], c[3])) for c in charts], lag_ratio=0.3))
            self.play(*[LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in c[2]], lag_ratio=0.02) for c in charts],
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def verdict(self, g):
        head = VGroup(label(r"", font_size=20), label(r"price error (\% of $K$)", font_size=20, color=GREY_A),
                      label(r"delta error", font_size=20, color=GREY_A), label(r"gamma error", font_size=20, color=GREY_A))
        tab = VGroup(head)
        for a, col, t in ACTS:
            tab.add(VGroup(label(t, font_size=24, color=col),
                           *[MathTex(f"{_mean(g, k, a):.{d}f}", font_size=30, color=col)
                             for k, d in (("price_rmse", 3), ("delta_rmse", 3), ("gamma_rmse", 2))]))
        xs = [-4.4, -1.4, 1.6, 4.4]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.0 - 0.75 * i, 0])
        ttl = label(r"Root-mean-square errors at six weeks, mean of two seeds", font_size=28).to_edge(UP, buff=0.6)
        ratio = _mean(g, "gamma_rmse", "ReLU") / _mean(g, "gamma_rmse", "SiLU")
        pr = _mean(g, "price_rmse", "ReLU") / _mean(g, "price_rmse", "SiLU")
        foot = wrapped_label(rf"ReLU's gamma error is {ratio:.0f} times SiLU's, at {pr:.1f} times the price error. Dixon, "
                             r"Halperin and Bilokon (ch.\ 4--5) read a network's sensitivities as its Jacobian and Hessian: "
                             r"for a pricing network they are the Greeks, and they are what a risk system consumes",
                             12.0, 20, GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The scorecard, averaged over two seeds each. The price errors are of the same order. "
            f"<bookmark mark='a'/> The gamma errors are not: the ReLU network's is {ratio:.0f} times the SiLU "
            "network's. For a pricing network, the derivatives are not a by-product: they are the Greeks, and they "
            "are what the risk system uses. Choose a smooth activation, and check the Greeks, not just the prices."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tab[0]), *[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(*r_[2:])) for r_ in tab[1:]], FadeIn(foot))
        q = ask(r"which of the three networks hedges a short straddle's gamma risk worst?")
        with self.voiceover(
            "A question before moving on: which of the three would you least like to hedge a short straddle with?"
            " The ReLU network: its gamma is zero almost everywhere, so it would never warn you how fast a straddle's delta turns, exactly where the risk lives. Next: a network that learns a model's whole smile."
        ):
            self.play(FadeIn(q))
        self.wait(0.6)
        self.clear_scene()
