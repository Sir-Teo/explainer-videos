from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, sci


class Schemes(VoiceoverScene):
    def construct(self):
        p = load("picard")
        o = load("orders")
        m = load("mlmc")
        self.card()
        self.picard(p)
        self.lab(o)
        self.orders(o)
        self.multilevel(m)

    def card(self):
        c = chapter_card(5, r"SDEs: existence, and how to simulate them", r"When does $dX = a\,dt + b\,dW$ have a "
                         r"solution, and how do you compute it?", part=PART)
        with self.voiceover("Chapter five. Stochastic differential equations: when they have solutions, and how to "
                            "compute them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def picard(self, p):
        its = [np.asarray(x) for x in p["iterates"]]
        t = np.linspace(0, 1, len(its[0]))
        lo = min(x.min() for x in its[1:]) - 0.1
        hi = max(x.max() for x in its[1:]) + 0.1
        g = axes([0, 1], [lo, hi], x_length=7.0, y_length=4.2, xlabel=r"time", ylabel=r"$X^{(k)}_t$ on one Brownian path",
                 xticks=[0, 0.5, 1], yticks=[1, 2], font_size=18).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
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
        rows[0].to_edge(DOWN, buff=0.9).shift(LEFT * 1.2)
        why0.next_to(rows[0], DOWN, buff=0.15)
        with self.voiceover(
            "An equation like d X equals sine of X d t plus a half cosine of X d W: does it have a solution, and only "
            "one? Kiyosi Itô answered in 1951 with the same trick that solves ordinary differential equations: Picard "
            "iteration. Start with a guess, the constant x nought. <bookmark mark='a'/> Plug it into the right-hand "
            "side, integrate against the one Brownian path we have, and get a new path. Plug that in, and repeat. "
            "<bookmark mark='b'/> The iterates snap together. The largest gap between successive iterates falls from "
            f"{p['dist'][0]:.2f} to {p['dist'][3]:.3f} after four rounds, and to about one in a million after nine. "
            "<bookmark mark='c'/> Why: Doob's inequality and the isometry bound each gap by an integral of the "
            "previous one, so the gaps shrink like C t to the k over k factorial, and the factorial wins. If the "
            "coefficients are Lipschitz, the solution exists, is unique, and is a function of the driving path: a "
            "strong solution. <bookmark mark='d'/> Some equations have only weak solutions. Tanaka's d X equals the "
            "sign of X d W has solutions in law, but none built from a given path."
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
            self.play(FadeOut(dist), FadeIn(th))
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
            "To compute a solution, step it forward. Here is the House's code. Euler-Maruyama: the drift times the "
            "step, plus the volatility times the Brownian increment. Milstein adds one line, in purple. "
            "<bookmark mark='a'/> Where does it come from? Inside a step, the volatility itself moves. Expand it with "
            "the lemma: it changes by b prime times b times the Brownian move so far. Integrating that against d W "
            "gives the left-point integral of chapter three: a half of the squared increment minus the step. "
            "<bookmark mark='b'/> Run both on geometric Brownian motion, where the exact solution is known path by "
            "path, with twenty thousand shared paths."
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
            "The step shrinks from a quarter to one two-hundred-and-fifty-sixth, and each scheme's error is plotted "
            "as it arrives. <bookmark mark='a'/> A pause: halve the step, and by how much does Euler's path error "
            "shrink? <bookmark mark='b'/> By only the square root of two: strong order one half, measured at "
            f"{o['slope_strong_euler']:.2f}. Milstein's extra line buys strong order one, measured at "
            f"{o['slope_strong_milstein']:.2f}. <bookmark mark='c'/> For prices, which are averages, both schemes are "
            "already order one: the weak errors fall together. So choose by the question: a price needs weak accuracy, "
            "a hedging simulation needs strong."
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

    def multilevel(self, m):
        s0 = m["seeds"][0][-1]
        V = np.log2(np.asarray(s0["V"]))
        L = len(V)
        g = axes([-0.5, L - 0.5], [V.min() - 0.5, V.max() + 0.5], x_length=5.6, y_length=3.6,
                 xlabel=r"level $l$ (steps $2^l$)", ylabel=r"$\log_2 \operatorname{Var}(P_l - P_{l-1})$",
                 xticks=list(range(0, L, 2)), yticks=[int(np.floor(V.min())), int(np.ceil(V.max()))], font_size=16)
        g.to_corner(UL, buff=0.4).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.3, height=max(ax.c2p(0, v)[1] - ax.c2p(0, V.min() - 0.5)[1], 0.01),
                                  stroke_width=0, fill_color=ITO, fill_opacity=0.8).move_to(ax.c2p(l, V.min() - 0.5),
                                                                                           aligned_edge=DOWN)
                        for l, v in enumerate(V)])
        eq = MathTex(r"\mathbb{E}\,P_L = \mathbb{E}\,P_0 + \sum_{l=1}^{L} \mathbb{E}\,(P_l - P_{l-1})", font_size=30)
        eq.to_edge(UP, buff=0.35).shift(RIGHT * 2.6)
        eps = m["eps"]
        ratio = np.asarray(m["ratio"])
        g2 = axes([-0.2, 2.2], [0, max(ratio.max() * 1.15, 2)], x_length=4.6, y_length=3.2,
                  xlabel=r"target accuracy", ylabel=r"cost of standard MC $\div$ multilevel", xticks=[0, 1, 2],
                  xfmt=lambda u: [r"0.04", r"0.02", r"0.01"][int(u)], yticks=[0, int(ratio.max())], font_size=16)
        g2.to_corner(DR, buff=0.5)
        a2 = g2.ax
        bd = seed_band(a2, np.arange(3), ratio, DRIFT)
        sdots = VGroup(*[Dot(a2.c2p(j, r_), radius=0.05, color=DRIFT) for row in ratio for j, r_ in enumerate(row)])
        rm = np.asarray(m["ratio_mean"])
        grows = rm[-1] > rm[0]
        verdict = (f"The saving grows as the target tightens, from about {rm[0]:.0f} times to {rm[-1]:.0f} times, as "
                   "the theory predicts." if grows else
                   f"Here the saving does not grow with the target: {rm[0]:.0f} times at the loosest and {rm[-1]:.0f} "
                   "at the tightest, because the levels are few at these accuracies.")
        with self.voiceover(
            "Why do orders cost money? Because of Michael Giles's multilevel Monte Carlo, from 2008. Write the "
            "finest-grid price as the coarsest one plus a telescoping sum of corrections between neighbouring grids. "
            "<bookmark mark='a'/> Each correction is simulated with the same Brownian path on both grids, so its "
            "variance is small, and it falls level by level at a rate set by the strong order. Most samples go to the "
            "cheap coarse levels, few to the fine ones. <bookmark mark='b'/> For an Asian option, as in Part sixteen, "
            "four seeds, at three accuracies: " + verdict + " Strong order, a property of single paths, decides the "
            "cost of averages."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(g))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), run_time=2)
            vo.wait_until("a")
            self.play(Indicate(bars, color=ITO))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(bd), FadeIn(sdots))
        self.wait(0.4)
        self.clear_scene()
