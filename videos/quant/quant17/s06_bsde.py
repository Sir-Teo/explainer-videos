from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
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
                    r"three dimensions here. A single discounted terminal-payoff average does not account for nonlinear feedback; other Monte Carlo-based solvers exist")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "This published benchmark is a recursive valuation model for a claim on one hundred independent geometric-Brownian assets. It pays their minimum at one year, conditional on survival; recovery on default is two thirds of its current value. The specified default intensity depends on that value, producing nonlinear feedback. <bookmark mark='a'/> A full tensor grid with ten points per asset needs ten to the hundred nodes. A single discounted terminal-payoff average does not solve this nonlinear equation. Nested, branching or multilevel Monte Carlo constructions can address particular nonlinear settings; the neural BSDE method is one approach, not the only route beyond a grid."
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
                    r"not: a backward SDE. $Z$ is Brownian exposure; for nonzero diagonal asset volatility, shares are $Z_i/(\bar\sigma X_i)$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-3.3, buff=0.8, edge=6.9)  # long right sides
        with self.voiceover(
            "Assuming a smooth interior pricing function, apply Itô's formula along the model's asset paths. <bookmark mark='a'/> Substitute the PDE into its drift. Our sign convention writes that drift as f of Y, with a plus sign. <bookmark mark='b'/> The result is a backward SDE with a specified terminal payoff. Z is exposure to Brownian noise, not directly a number of shares: in this diagonal diffusion, divide its i-th component by sigma times asset i to obtain the Brownian delta. The nonlinear credit model still carries its own assumptions; this identity does not establish a perfect hedge of issuer default."
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
        whys = [why(r"Pardoux--Peng: Lipschitz generator, square-integrable terminal value and standard adaptedness/integrability assumptions give a unique square-integrable pair; with Markov/PDE regularity its "
                    r"start is the PDE's solution: the non-linear Feynman--Kac formula (Part 5 had the linear one)"),
                why(rf"E, Han and Jentzen (2017): Euler steps forward from a guessed start $u_0$; the hedge at each of the "
                    rf"{p['N'] - 1} later dates is a small network of the hundred prices"),
                why(r"shoot: train the guess and the networks together so every path lands on its payoff. Zero loss "
                    r"in the exact continuous-time population problem identifies the solution. A zero finite-batch Euler loss does not; Han, Jentzen and E (2018, "
                    r"\textit{PNAS}) showed it at $d = 100$"),
                why(r"a check with a known answer: with no default the equation is linear, and the price is plain "
                    r"discounted Monte Carlo. Chapter 9 runs it")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Under the usual Lipschitz, square-integrability and adaptedness assumptions, the BSDE has a unique square-integrable solution. Markovian coefficient regularity links it to the PDE. <bookmark mark='a'/> The numerical method instead guesses a starting value and Brownian exposures, then uses forty Euler steps and date-specific networks. <bookmark mark='b'/> Training minimizes sampled terminal mismatch. Zero population mismatch in the exact continuous-time problem would identify its solution; zero empirical loss on a finite Euler grid would not certify the continuous-time price. Generalization, time stepping, approximation and optimization errors remain. <bookmark mark='c'/> Switching off default gives a linear model with a discounted-expectation reference, providing a useful separate check."
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
        lo, hi = data_range(allY)
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
                grp.add(curve(ax, tt, y, NET, stroke_width=1.2).set_stroke(opacity=0.6))
                grp.add(Line(ax.c2p(1.02, tgt), ax.c2p(1.06, tgt), stroke_color=WHITE,
                             stroke_width=2.5))
                grp.add(Line(ax.c2p(1.0, y[-1]), ax.c2p(1.04, tgt), stroke_color=BAD,
                             stroke_width=1.5, stroke_opacity=0.8))
            miss = float(np.sqrt(np.mean((np.asarray(s_["Y"]) - np.asarray(s_["g"])) ** 2)))
            grp.add(Dot(ax.c2p(0, s_["u0"]), radius=0.08, color=GOOD))
            txt = VGroup(label(rf"training step {its[i]}", font_size=22, color=NET),
                         MathTex(rf"u_0 = {s_['u0']:.2f}", font_size=30, color=GOOD),
                         label(rf"256-path replay RMS miss: {miss:.1f}", font_size=20, color=BAD)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
            return VGroup(grp, txt)
        cur = fan(0)
        leg = legend([(GOOD, r"today's guess $u_0$"), (NET, r"$Y$ stepped forward on 32 of the paths"),
                      (WHITE, r"each path's payoff, $\min_i X^i_T$"), (BAD, r"the miss")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        src = illustration(r"seed 1; first 32 of 256 fixed replay paths; training-mode batch normalization; checkpoints reuse paths")
        with self.voiceover(
            "Here is the shooting, on thirty-two of the paths. The green dot is today's guess. From it, each path's "
            "price is stepped forward with that path's own noise and the networks' hedges, and at expiry it should "
            "land on the white tick, that path's payoff. The red segments are the misses. "
            "<bookmark mark='a'/> Before training, the guess is arbitrary and the hedges are noise: the fan sprays "
            "everywhere. <bookmark mark='b'/> As training proceeds, the guess moves and the networks learn to steer: "
            "the fan narrows, and each path comes down close to its own target."
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
            'With fixed time grid, batch and depth, the dense networks have width d plus ten. Their work grows quadratically in d at large dimension; doubling d then approaches four times the network work, while simulating paths is linear in d. This is work per update, not total cost for a fixed accuracy. More training or a finer grid may still be needed. Next: watching the solver converge.'
        ):
            self.play(FadeOut(src), FadeIn(q))  # the banner takes the foot of the frame
        self.wait(0.5)
        self.clear_scene()
