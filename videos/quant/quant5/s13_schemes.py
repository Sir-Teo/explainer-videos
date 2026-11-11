from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, sci


class Schemes(VoiceoverScene):
    def construct(self):
        p = load("picard")
        o = load("orders")
        self.card()
        self.picard(p)
        self.lab(o)
        self.orders(o)

    def card(self):
        c = chapter_card(5, r"SDEs: existence, and how to simulate them", r"When does $dX = a\,dt + b\,dW$ have a "
                         r"solution, and how do you compute it?", part=PART)
        with self.voiceover(
            'Chapter five. Stochastic differential equations: when they have solutions, and how to compute them.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def picard(self, p):
        its = [np.asarray(x) for x in p["iterates"]]
        t = np.linspace(0, 1, len(its[0]))
        lo = min(x.min() for x in its[1:]) - 0.1
        hi = max(x.max() for x in its[1:]) + 0.1
        g = axes([0, 1], [lo, hi], x_length=7.0, y_length=3.3, xlabel=r"time", ylabel=r"$X^{(k)}_t$ on one Brownian path",
                 xticks=[0, 0.5, 1], yticks=[1, 2], font_size=18).to_edge(LEFT, buff=0.5).shift(UP * 0.25)
        ax = g.ax
        cols = color_gradient([GREY_B, ITO], len(its))
        lines = [curve(ax, t, np.clip(x, lo, hi), c, stroke_width=2.5) for x, c in zip(its, cols)]
        eq = MathTex(r"X^{(k+1)}_t = x_0 + \int_0^t \sin X^{(k)}_s\,ds + \int_0^t \tfrac12 \cos X^{(k)}_s\,dW_s",
                     font_size=28).to_edge(UP, buff=0.35)
        dist = VGroup(*[MathTex(rf"k = {k + 1}:\ \sup_t |X^{{({k + 1})}} - X^{{({k})}}| = {sci(d)}", font_size=22,
                                color=cols[k + 1]) for k, d in enumerate(p["dist"])])
        dist.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        th = theorem_card(r"Existence and uniqueness", r"If $a$ and $b$ are Lipschitz and grow at most linearly, "
                          r"$dX = a(X)\,dt + b(X)\,dW$ has a unique strong solution: a process adapted to $W$, built "
                          r"path by path.", who=r"It\^o (1951)", color=ITO, width=6.4, font_size=20).to_corner(DR, buff=0.3)
        rows = [cmath(r"\big\| X^{(k+1)} - X^{(k)} \big\|^2_t", r"\le", r"C\int_0^t \big\|X^{(k)} - X^{(k-1)}\big\|^2_s\,ds "
                      r"\;\le\; \frac{(Ct)^k}{k!}", font_size=30)]
        why0 = why(r"Doob's inequality, the isometry and the Lipschitz bound; the factorial wins", 20)
        rows[0].to_edge(DOWN, buff=0.75).shift(LEFT * 1.2)  # under the shortened chart
        why0.next_to(rows[0], DOWN, buff=0.15)
        with self.voiceover(
            f'Does d X equals sine of X d t plus a half cosine of X d W have exactly one solution? Itô '
            f"answered in 1951 with Picard iteration. Start with a constant guess. <bookmark mark='a'/> "
            f'Plug it into the right-hand side, integrate along the one Brownian path we have, and '
            f"repeat. <bookmark mark='b'/> The iterates snap together: the largest gap falls from "
            f"{p['dist'][0]:.2f} to {p['dist'][3]:.3f}"
            f" in four rounds, and to a millionth in nine. <bookmark mark='c'/> Doob's inequality and "
            f'the isometry make the gaps shrink like a power over a factorial. Global spatial Lipschitz '
            f'and linear-growth bounds, with square-integrable initial data, give a unique strong '
            f"solution. The coefficients in this example satisfy those bounds. <bookmark mark='d'/> "
            f'Tanaka’s equation, d X equals sign of X d W with X initially zero and sign of zero defined'
            f' as one, has a weak solution but no strong solution driven by that Brownian motion.'
        ) as vo:
            self.play(FadeIn(g), FadeIn(eq), Create(lines[0]))
            vo.wait_until("a")
            for k in range(1, 4):
                self.play(Create(lines[k]), FadeIn(dist[k - 1]), run_time=1.0)
            vo.wait_until("b")
            for k in range(4, len(lines)):
                self.play(Create(lines[k]), FadeIn(dist[k - 1]), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(why0))
            vo.wait_until("d")
            self.play(FadeOut(dist), FadeOut(rows[0]), FadeOut(why0), FadeIn(th))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, o):
        card = lab_card(r"Euler--Maruyama and Milstein", [
            "def euler_maruyama(a, b, x0, T, dW):",
            "    n_paths, n = dW.shape; dt = T / n",
            "    X = np.empty((n_paths, n + 1)); X[:, 0] = x0",
            "    for k in range(n):",
            "        X[:, k+1] = X[:, k] + a(k*dt, X[:, k])*dt + b(k*dt, X[:, k])*dW[:, k]",
            "    return X",
            "",
            "def milstein(a, b, db, x0, T, dW):    # ... the same loop, plus",
            "        + 0.5 * b(t, x) * db(t, x) * (dW[:, k]**2 - dt)",
        ], source="explainer/quant/house/sim.py", width=8.4, font_size=17).to_edge(UP, buff=0.35)
        card.code[-1].set_color(ITO)
        outs = [f"scheme_orders(mu=0.05, sigma=0.4, n_paths=20000)",
                f"strong slope: Euler {o['slope_strong_euler']:.2f}   Milstein {o['slope_strong_milstein']:.2f}",
                f"weak slope:   Euler {o['slope_weak_euler']:.2f}   Milstein {o['slope_weak_milstein']:.2f}"]
        rows = [cmath(r"\int_t^{t+h} b(X_s)\,dW_s", r"\approx", r"b\,\Delta W + b'b \int_t^{t+h} (W_s - W_t)\,dW_s", font_size=28),
                cmath(r"\int_t^{t+h} (W_s - W_t)\,dW_s", r"=", r"\tfrac12\big(\Delta W^2 - h\big)", font_size=28,
                      colors={r"\tfrac12\big(\Delta W^2 - h\big)": ITO})]
        whys = [why(r"expand $b(X_s)$ by the lemma, to first order in $W_s - W_t$", 19),
                why(r"chapter 3's left-point integral of $W$ against itself", 19)]
        with self.voiceover(
            "To compute a solution, step it forward. Here is the House's code. Euler-Maruyama: the drift times "
            'the step, plus the volatility times the Brownian increment, exactly the left-point sum of chapter '
            "three. Milstein adds one line, in gold. <bookmark mark='a'/> Where does it come from? Inside a step "
            'the volatility itself moves. Expanded by the lemma, it changes by b prime times b times the Brownian'
            " move so far, and integrating that against d W gives chapter three's left-point integral: half the "
            "squared increment minus the step. <bookmark mark='b'/> Run both on geometric Brownian motion, where "
            'the exact solution is known path by path, with twenty thousand paths shared between the two schemes,'
            ' so that their errors can be compared path by path.'
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            step = ladder(self, rows, whys, keep=2, top=-0.6, x=-1.0, buff=0.5, edge=6.9)
            step(0)
            step(1)
            vo.wait_until("b")
            self.play(*[FadeOut(r) for r in rows], *[FadeOut(w) for w in whys])
            lab_run(self, card, outs, font_size=19)
        self.wait(0.4)
        self.clear_scene()

    def orders(self, o):
        dt = np.log10(np.asarray(o["dt"]))
        g = axes([dt.min() - 0.1, dt.max() + 0.1], [-4.5, -0.5], x_length=7.0, y_length=4.6,
                 xlabel=r"time step $\Delta t$ (log scale)", ylabel=r"error at $T = 1$ (log scale)",
                 xticks=list(np.log10([1 / 256, 1 / 64, 1 / 16, 1 / 4])),
                 xfmt=lambda u: {256: "1/256", 64: "1/64", 16: "1/16", 4: "1/4"}[round(10 ** -u)],
                 yticks=[-4, -3, -2, -1], yfmt=lambda u: rf"10^{{{int(u)}}}", font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        sets = [("strong_euler", JUMP), ("strong_milstein", ITO), ("weak_euler", BM), ("weak_milstein", STRAT)]
        dots = []
        for k, c in sets:
            y = np.log10(np.asarray(o[k]))
            dots.append([Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(dt[::-1], y[::-1])])
        fits = VGroup(*[curve(ax, dt, np.log10(np.asarray(o[k])), c, stroke_width=2.5) for k, c in sets])
        leg = legend([(JUMP, rf"Euler, strong: slope {o['slope_strong_euler']:.2f}"),
                      (ITO, rf"Milstein, strong: slope {o['slope_strong_milstein']:.2f}"),
                      (BM, rf"Euler, weak: slope {o['slope_weak_euler']:.2f}"),
                      (STRAT, rf"Milstein, weak: slope {o['slope_weak_milstein']:.2f}")], font_size=21)
        side = VGroup(leg,
                      wrapped_label(r"strong error $\mathbb{E}|X_T - S_T|$: how far each path is from the true one "
                                    r"(hedging, path-dependent risk); weak error $|\mathbb{E}\,g(X_T) - \mathbb{E}\,g(S_T)|$: "
                                    r"how far an average is (prices)", 4.8, 19, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        pc, ans = pause(r"Halve the step. Euler's path error shrinks by\,\ldots?", r"$1/\sqrt 2$: strong order one half.",
                        width=4.8, font_size=21)
        pc.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        ans.next_to(pc, DOWN, buff=0.1).align_to(pc, LEFT)
        with self.voiceover(
            f"The step shrinks from a quarter to one two-hundred-and-fifty-sixth, and each scheme's "
            f"error at time one is plotted as it arrives. <bookmark mark='a'/> A pause: halve the step, "
            f"and by how much does Euler's path error shrink? <bookmark mark='b'/> Only by the square "
            f"root of two: strong order one half, measured at {o['slope_strong_euler']:.2f}"
            f'. The reason is the term Euler drops, half b b prime times the squared increment minus the'
            f' step: it has size of order the step, but it is a martingale sum, so its errors add in '
            f'quadrature to the square root of the step. Milstein keeps it, and buys strong order one: '
            f"{o['slope_strong_milstein']:.2f}"
            f". <bookmark mark='c'/> For sufficiently smooth payoff expectations and regular "
            f'coefficients, both schemes have weak order one. The dropped term’s zero mean is part of '
            f'the explanation; nonsmooth payoffs need separate analysis. So choose by the question: '
            f'prices need weak accuracy, hedging simulations strong. And strong order, a property of '
            f'single paths, also sets the cost of averages: it decides how well multilevel Monte Carlo '
            f"works, Part sixteen's subject. Next: two equations every desk simulates, the mean-reverting ones."
        ) as vo:
            self.play(FadeIn(g))
            for k in range(len(dt)):
                self.play(*[FadeIn(d[k], scale=1.6) for d in dots[:2]], run_time=0.45)
            vo.wait_until("a")
            self.play(FadeIn(pc))
            vo.wait_until("b")
            self.play(FadeIn(ans), Create(fits[0]), Create(fits[1]), FadeIn(leg[0]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(VGroup(*d)) for d in dots[2:]], Create(fits[2]), Create(fits[3]), FadeIn(leg[2:]),
                      FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()
