from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, illustration, load


class BSDE(VoiceoverScene):
    def construct(self):
        b = load("bsde")
        self.card()
        self.curse()
        self.derive()
        self.method(b)
        self.shooting(load("bsde_seeds"), b)

    def card(self):
        c = chapter_card(8, r"A hundred dimensions: the deep BSDE", r"How do you solve a pricing PDE in 100 dimensions?",
                         part=PART)
        with self.voiceover("Chapter eight. A hundred dimensions: the deep BSDE method."):
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

    def derive(self):
        rows = [cmath(r"Y_t = u(t, X_t)", r"\Rightarrow", r"dY_t = \big(\partial_t u + \mathcal{L} u\big)\,dt + \nabla u^\top "
                      r"\sigma(X_t)\,dW_t", font_size=34, colors={r"Y_t = u(t, X_t)": NET}),
                cmath(r"\partial_t u + \mathcal{L} u", r"=", r"(1 - \delta)\,Q(u)\,u + R\,u =: f(Y_t)", font_size=38,
                      colors={r"\partial_t u + \mathcal{L} u": GOOD}),
                cmath(r"dY_t", r"=", r"f(Y_t)\,dt + Z_t\cdot dW_t,\qquad Z_t = \sigma(X_t)^\top \nabla u,\qquad Y_T = "
                      r"\min_i X_T^i", font_size=34, colors={r"dY_t": NET})]
        whys = [why(r"It\^o's formula (Part 5) for the price along a simulated path of the hundred assets; $\mathcal{L}$ is "
                    r"the generator, the drift and the second-order terms of the equation"),
                why(r"the pricing equation says exactly what $\partial_t u + \mathcal{L} u$ is: the non-linear default term"),
                why(r"so the price process solves a stochastic differential equation whose end is known and whose start is "
                    r"not: a backward SDE. Its noise coefficient $Z$ is the gradient of the price, the hedge")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The way out starts from Itô's formula. Follow the price along one simulated path of the hundred assets: "
            "Y at time t is u of t and X t. Itô says how it moves: a drift, which is the time derivative plus the "
            "generator of the equation, and a noise term, the gradient times the assets' volatility. "
            "<bookmark mark='a'/> But the equation tells us what that drift is: exactly the non-linear default term. "
            "<bookmark mark='b'/> So the price along the path solves a stochastic differential equation of its own, "
            "with the drift a function of the price, and a noise coefficient Z that is the hedge. We know where it "
            "must end, at the payoff, the worst of the hundred assets. We do not know where it starts: that is the "
            "price we want. A backward stochastic differential equation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def method(self, b):
        p = b["params"]
        rows = [cmath(r"Y_0", r"=", r"u(0, x_0)\ \ \text{for the unique pair } (Y, Z)", font_size=38,
                      colors={r"Y_0": GOOD}),
                cmath(r"Y_{n+1}", r"=", r"Y_n + f(Y_n)\,\Delta t + Z_n\cdot\Delta W_n,\qquad Z_n = \text{network}_n(X_{t_n})",
                      font_size=34, colors={r"Y_{n+1}": NET}),
                cmath(r"\min_{u_0,\, Z_0,\, \theta}", r"\ ", r"\mathbb{E}\,\big|\,Y_N - \min_i X^i_T\,\big|^2", font_size=36,
                      colors={r"\min_{u_0,\, Z_0,\, \theta}": GOOD}),
                cmath(r"\delta = 1", r"\Rightarrow", r"f = R\,Y,\quad Y_0 = e^{-RT}\,\mathbb{E}\min_i X^i_T", font_size=36,
                      colors={r"\Rightarrow": WHITE})]
        whys = [why(r"Pardoux and Peng (1990): for a Lipschitz $f$ the backward equation has exactly one solution, and its "
                    r"start is the PDE's solution: the non-linear Feynman--Kac formula (Part 5 had the linear one)"),
                why(rf"E, Han and Jentzen (2017): Euler steps forward from a guessed start $u_0$; the hedge at each of the "
                    rf"{p['N'] - 1} later dates is a small network of the hundred prices"),
                why(r"shoot: train the guess and the networks together so every path lands on its payoff. Zero loss "
                    r"means the guess was the price and the networks are the hedge; Han, Jentzen and E (2018, "
                    r"\textit{PNAS}) showed it at $d = 100$"),
                why(r"a check with a known answer: with no default the equation is linear, and the price is plain "
                    r"discounted Monte Carlo. Chapter 9 runs it")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Two facts make this usable. First, Étienne Pardoux and Shige Peng proved in 1990 that for such a drift "
            "the backward equation has exactly one solution, and that its starting value is the solution of the "
            "pricing equation: the non-linear Feynman–Kac formula. <bookmark mark='a'/> Second, Weinan E, Jiequn Han "
            "and Arnulf Jentzen turned it into a learning problem. Guess today's price. Step the equation forward with "
            "the simulated noise. At each date, the unknown hedge is supplied by a small network that looks at the "
            "hundred prices. <bookmark mark='b'/> Then train the guess and all the networks together so that every "
            "path lands on its own payoff at expiry. If the loss were zero, the guess would be the price and the "
            "networks would be the hedge. <bookmark mark='c'/> And there is a built-in check: switch default off, and "
            "the equation becomes linear, with an answer plain Monte Carlo can give."
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

    def shooting(self, bs, b):
        sn = bs["seed1"]["snaps"]
        its = ["0", "100", "300", "1000", "2000"]
        N = b["params"]["N"]
        tt = np.linspace(0, 1, N + 1)
        allY = np.concatenate([np.asarray(sn[i]["Ypath"]).ravel() for i in its] +
                              [np.asarray(sn[i]["g"])[:32] for i in its])
        lo, hi = float(np.percentile(allY, 1)) - 2, float(np.percentile(allY, 99)) + 2
        g = axes([0, 1.08], [lo, hi], x_length=7.6, y_length=4.6, xlabel=r"time (years)", ylabel=r"$Y_t$, the price along "
                 r"the path", xticks=[0, 0.5, 1], yticks=[round(v) for v in np.linspace(lo + 2, hi - 2, 4)],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax

        def fan(i):
            s_ = sn[its[i]]
            Yp = np.asarray(s_["Ypath"])
            gg = np.asarray(s_["g"])[:32]
            grp = VGroup()
            for y, tgt in zip(Yp, gg):
                grp.add(curve(ax, tt, np.clip(y, lo, hi), NET, stroke_width=1.2).set_stroke(opacity=0.6))
                grp.add(Line(ax.c2p(1.02, np.clip(tgt, lo, hi)), ax.c2p(1.06, np.clip(tgt, lo, hi)), stroke_color=WHITE,
                             stroke_width=2.5))
                grp.add(Line(ax.c2p(1.0, np.clip(y[-1], lo, hi)), ax.c2p(1.04, np.clip(tgt, lo, hi)), stroke_color=BAD,
                             stroke_width=1.5, stroke_opacity=0.8))
            miss = float(np.sqrt(np.mean((np.asarray(s_["Y"]) - np.asarray(s_["g"])) ** 2)))
            grp.add(Dot(ax.c2p(0, np.clip(s_["u0"], lo, hi)), radius=0.08, color=GOOD))
            txt = VGroup(label(rf"training step {its[i]}", font_size=22, color=NET),
                         MathTex(rf"u_0 = {s_['u0']:.2f}", font_size=30, color=GOOD),
                         label(rf"typical miss at expiry: {miss:.1f}", font_size=20, color=BAD)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
            return VGroup(grp, txt)
        cur = fan(0)
        leg = legend([(GOOD, r"today's guess $u_0$"), (NET, r"$Y$ stepped forward on 32 of the paths"),
                      (WHITE, r"each path's payoff, $\min_i X^i_T$"), (BAD, r"the miss")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        src = illustration(r"the 100-asset claim with default; a second run (seed 1), 256 fixed test paths")
        with self.voiceover(
            "Here is the shooting, on thirty-two of the paths. The green dot is today's guess. From it, each path's "
            "price is stepped forward with that path's own noise and the networks' hedges, and at expiry it should "
            "land on the white tick, that path's payoff. The red segments are the misses. "
            "<bookmark mark='a'/> Before training, the guess is arbitrary and the hedges are noise: the fan sprays "
            "everywhere. <bookmark mark='b'/> As training proceeds, the guess moves and the networks learn to steer: "
            "the fan narrows, and each path comes down close to its own target. The misses never vanish, because time "
            "is cut into forty steps; what matters is that the guess has stopped moving."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(cur))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            for i in range(1, len(its)):
                new = fan(i)
                self.play(Transform(cur, new), run_time=1.6)
        q = ask(r"double the dimension to 200. Does the cost of a training step double, or square?")
        with self.voiceover(
            "Before the next chapter: double the number of assets to two hundred. Does the work per training step "
            "double, or square, or explode like the grid?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
