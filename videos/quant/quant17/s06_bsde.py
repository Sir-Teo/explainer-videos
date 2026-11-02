from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, illustration, load


class BSDE(VoiceoverScene):
    def construct(self):
        b = load("bsde")
        self.card()
        self.curse()
        self.method(b)
        self.result(b)

    def card(self):
        c = chapter_card(5, r"A hundred dimensions: the deep BSDE", r"How do you solve a pricing PDE in 100 dimensions?",
                         part=PART)
        with self.voiceover("Chapter five. A hundred dimensions: the deep BSDE method."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curse(self):
        rows = [cmath(r"\partial_t u + \bar\mu\, x\cdot\nabla u + \tfrac{\bar\sigma^2}{2}\sum_{i=1}^{100} x_i^2\,\partial_{ii} u",
                      r"=", r"(1 - \delta)\,Q(u)\,u + R\,u", font_size=32, colors={r"=": WHITE}),
                cmath(r"u(T, x)", r"=", r"\min_i x_i", font_size=34, colors={r"u(T, x)": OPT})]
        whys = [why(r"Han, Jentzen and E (2018): a claim on 100 assets whose issuer can default; default is likelier when the "
                    r"claim is worth less ($Q$ falls from 20\% to 2\% a year as $u$ rises from 50 to 70), and the holder "
                    r"recovers $\delta = \tfrac23$. The price feeds back on itself: the equation is non-linear"),
                why(r"a grid of just 10 points per asset has $10^{100}$ nodes; Part 16's finite differences stop at two or "
                    r"three dimensions, and plain Monte Carlo cannot handle the non-linearity")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "Part sixteen's grids stopped at two dimensions. Here is a pricing equation in a hundred. Jiequn Han, Arnulf "
            "Jentzen and Weinan E took a claim on a hundred assets, paying the worst of them, whose issuer can default. "
            "Default becomes likelier as the claim loses value, and the holder then recovers two thirds. The price feeds "
            "back on itself, so the equation is non-linear. <bookmark mark='a'/> A grid with ten points per asset would "
            "have ten to the hundred nodes. And plain Monte Carlo cannot do it either, because of the non-linear term."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def method(self, b):
        p = b["params"]
        rows = [cmath(r"Y_{n+1}", r"=", r"Y_n - f(Y_n)\,\Delta t + Z_n\cdot\Delta W_n,\qquad Y_0 = u_0", font_size=36,
                      colors={r"Y_{n+1}": NET}),
                cmath(r"Z_n", r"=", r"\text{network}_n(X_{t_n}) \approx \bar\sigma\, X_{t_n}\cdot\nabla u", font_size=36,
                      colors={r"Z_n": NET}),
                cmath(r"\min_{u_0,\, Z_0,\, \theta}", r"\ ", r"\mathbb{E}\,\big|\,Y_N - \min_i X^i_T\,\big|^2", font_size=36,
                      colors={r"\min_{u_0,\, Z_0,\, \theta}": GOOD})]
        whys = [why(r"the price along a path satisfies a backward SDE: start from a guess of today's price and step it "
                    r"forward with the simulated noise"),
                why(rf"the unknown at each of the {p['N'] - 1} later dates is the hedge, $\sigma X \nabla u$; a small network "
                    r"learns it from the asset prices"),
                why(r"train so the simulated price lands on the payoff at expiry: when it does on every path, $u_0$ is the "
                    r"price and the networks are the hedge (Pardoux and Peng 1990)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.4, buff=0.75, edge=6.9)
        with self.voiceover(
            "The trick is to turn the equation into a learning problem. Along each simulated path, the price satisfies "
            "a backward stochastic differential equation: start from a guess of today's price, and step it forward with "
            "the same noise that moves the assets. <bookmark mark='a'/> At every date the step needs the hedge, the "
            "price's sensitivity to the hundred assets, and that is what a small network supplies, one per date. "
            "<bookmark mark='b'/> Then train everything, the guess and the networks, so that the simulated price lands "
            "on the payoff at expiry. When it does on every path, the starting guess is the price, and the networks are "
            "the hedge."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def result(self, b):
        cv = b["curve"]
        it = np.array([c["iter"] for c in cv])
        u = np.array([c["u0"] for c in cv])
        ref, nd = b["reference"], b["no_default_mc"]
        lo, hi = min(u.min(), ref) - 1.5, max(u.max(), nd) + 1.5
        g = axes([0, it.max()], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"training step",
                 ylabel=r"today's price $u_0$", xticks=[0, 1000, 2000, 3000, 4000],
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), yticks=[round(v) for v in np.linspace(lo + 1, hi - 1, 4)],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, it, u, NET, stroke_width=3)
        r1 = DashedLine(ax.c2p(0, ref), ax.c2p(it.max(), ref), stroke_color=REF, stroke_width=2)
        r2 = DashedLine(ax.c2p(0, nd), ax.c2p(it.max(), nd), stroke_color=BAD, stroke_width=2)
        leg = legend([(NET, r"the deep BSDE's $u_0$"), (REF, rf"reference {ref:.3f} (multilevel Picard)"),
                      (BAD, rf"ignoring default: {nd:.2f} (Monte Carlo)")], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"u_0 = {b['u0']:.2f}", font_size=40, color=NET),
            label(rf"error {100 * b['rel_error']:.2f}\% against the reference", font_size=20, color=GREY_A),
            wrapped_label(rf"{b['seconds'] / 60:.0f} minutes on a shared CPU, batches of 64 paths and {b['params']['N']} "
                          r"time steps. Han, Jentzen and E reported 0.46\% in 27 minutes. Ignoring default "
                          rf"overprices the claim by {nd - ref:.1f}", 4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"our run of the published example; without default, Monte Carlo gives {nd:.2f} $\pm$ "
                           rf"{b['no_default_se']:.2f} (the paper's {b['paper_no_default']:.3f} also leaves out discounting)")
        with self.voiceover(
            "Here is the training, as it happened. The guess for today's price starts at random. "
            f"<bookmark mark='a'/> It settles at {b['u0']:.2f}, against a reference of {ref:.1f} computed by a "
            f"different method altogether, an error of {100 * b['rel_error']:.2f} percent. "
            f"<bookmark mark='b'/> Ignore the default risk and the claim is worth {nd:.1f}: the non-linear term is worth "
            f"{nd - ref:.1f}. A hundred dimensions, on one CPU, in about {b['seconds'] / 60:.0f} minutes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(r1), Create(r2), FadeIn(leg[1]), FadeIn(leg[2]))
            self.play(Create(line), FadeIn(leg[0]), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.5)
        self.clear_scene()
