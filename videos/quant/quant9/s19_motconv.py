from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, Q_C, FullRangeReplay, answer_under, load, pause_at,
                                        real_data)


class MOTConverge(VoiceoverScene):
    def construct(self):
        m, gr, en = load("mot"), load("mot_grid"), load("mot_entropic")
        self.card()
        self.lab(m)
        self.grid(gr, m)
        self.entropic_math()
        self.entropic_run(en, m)
        self.predict()

    def card(self):
        c = chapter_card(16, r"Finite-grid bounds and numerical sensitivity", r"How much do the bounds depend on how "
                         r"we compute them?", part=PART)
        with self.voiceover("""Chapter sixteen. Finite-grid bounds and numerical sensitivity."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lab(self, m):
        with verbatim():
            card = lab_card(r"martingale optimal transport as one sparse LP", [
                "def mot_bounds(x, mu, y, nu, cost):",
                "    C = [[cost(a, b) for b in y] for a in x]",
                "    A = rows_sum_to(mu) + cols_sum_to(nu)    # marginals",
                "    A += [pi[i, :] @ (y - x[i]) == 0 for i]   # martingale",
                "    lo = linprog(+C, A_eq=A, b_eq=b, bounds=(0, None))",
                "    hi = linprog(-C, A_eq=A, b_eq=b, bounds=(0, None))",
                "    return lo.fun, -hi.fun, lo.x, hi.x",
            ], source="explainer/quant/house/arbitrage.py", width=8.0, font_size=17).to_edge(UP, buff=0.4)
        n1, n2 = len(m["x"]), len(m["y"])
        outs = [f"mot_bounds(x[{n1}], mu, y[{n2}], nu, lambda s1, s2: abs(s2 / s1 - 1))",
                f"lower = {m['lower']:.4f}   upper = {m['upper']:.4f}   ({n1 * n2:,} unknowns)",
                f"lognormal model: {m['model']:.4f}"]
        with self.voiceover(
            f"""Here is the existing linear program for the finite, forward-normalized marginals. One unknown per price pair; rows impose each marginal and the martingale constraint. <bookmark mark='a'/> Minimize and maximize the normalized claim. The {n1} by {n2} support gives {n1 * n2:,} unknowns and bounds {m['lower']:.3f} to {m['upper']:.3f}. Convex-order checks describe these discretized fitted marginals. Infeasibility would flag their inconsistency, rather than automatically proving an executable arbitrage in asynchronous market quotes."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            with verbatim():
                lab_run(self, card, outs, run_time=2.4, font_size=17)
        self.wait(1.5)
        self.clear_scene()

    def grid(self, gr, m):
        rows = [r for r in gr["rows"] if "upper" in r]
        n = len(rows)
        g = axes([0, n - 1], [0.11, 0.235], x_length=7.4, y_length=4.4, xlabel=r"atoms: first expiry $\times$ second",
                 ylabel=r"bounds on the forward-start straddle", xticks=[], yticks=[0.12, 0.15, 0.18, 0.21],
                 font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = g.ax
        ticks = VGroup(*[MathTex(rf"{r['atoms1']}\times{r['atoms2']}", font_size=16, color=GREY_B).next_to(
            ax.c2p(i, 0.11), DOWN, buff=0.12) for i, r in enumerate(rows)])
        k = ValueTracker(0)
        lo, up = np.array([r["lower"] for r in rows]), np.array([r["upper"] for r in rows])

        def walls():
            v = k.get_value()
            i = int(np.floor(v))
            out = VGroup()
            pts = [j for j in range(n) if j <= v + 1e-9]
            if len(pts) >= 2:
                out.add(band(ax, pts, lo[pts], up[pts], ALT, 0.25))
                out.add(curve(ax, pts, up[pts], ALT, stroke_width=3), curve(ax, pts, lo[pts], ALT, stroke_width=3))
            out.add(*[Dot(ax.c2p(j, lo[j]), radius=0.06, color=ALT) for j in pts],
                    *[Dot(ax.c2p(j, up[j]), radius=0.06, color=ALT) for j in pts])
            return out

        W = always_redraw(walls)
        ml = DashedLine(ax.c2p(0, m["model"]), ax.c2p(n - 1, m["model"]), color=CALL, stroke_width=2)
        mll = MathTex(rf"\text{{log-normal }} {m['model']:.3f}", font_size=22, color=CALL).next_to(ax.c2p(n - 1, m["model"]),
                                                                                              UP, buff=0.08).shift(LEFT * 0.8)
        widen = up[-1] - lo[-1] > up[0] - lo[0]
        side = VGroup(
            MathTex(rf"{rows[0]['atoms1']}\times{rows[0]['atoms2']}:\ [{lo[0]:.3f},\ {up[0]:.3f}]", font_size=26, color=ALT),
            MathTex(rf"{rows[-1]['atoms1']}\times{rows[-1]['atoms2']}:\ [{lo[-1]:.3f},\ {up[-1]:.3f}]", font_size=26,
                    color=ALT),
            wrapped_label(r"non-nested grids change the marginals; widening is observed, not a monotonicity theorem", 4.2, 20, GREY_A),
            wrapped_label(rf"last-grid changes: {1e3 * abs(up[-1] - up[-2]):.1f} and {1e3 * abs(lo[-1] - lo[-2]):.1f} thousandths; no continuum error certificate", 4.2, 20, Q_C),
            wrapped_label(r"every grid's marginals are checked for convex order before solving", 4.2, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        tail = ("It widens: a coarse grid cannot represent the most extreme joinings. " if widen else
                "It narrows as the grid refines. ")
        with self.voiceover(
            f"""The band depends on the discretization. Refine the existing grids from nine by twenty-five to eighty-one by three hundred and sixty-one atoms. <bookmark mark='a'/> The computed endpoints move from {lo[0]:.3f}, {up[0]:.3f} to {lo[-1]:.3f}, {up[-1]:.3f}. These are non-nested re-binnings with changed marginal measures, so their feasible sets are not ordered. <bookmark mark='b'/> The last two grids nearly agree in this example. That is a sensitivity check, not a proof of monotone convergence or a continuum error bound. The ATM lognormal proxy happens to lie inside; it does not reproduce both full fitted marginals and need not be a feasible calibrated model."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(ticks), Create(ml), FadeIn(mll))
            self.add(W)
            vo.wait_until("a")
            self.play(k.animate.set_value(n - 1), run_time=max(vo.until("b") - 1.0, 4.0), rate_func=linear)
            W.clear_updaters()
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        W.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def entropic_math(self):
        rows = [cmath(r"\max_\pi", r"\ ", r"\sum \pi\, c - \varepsilon\, \mathrm{KL}(\pi\,\|\,\mu\otimes\nu)", font_size=34),
                cmath(r"\pi_{ij}", r"=", r"\mu_i\nu_j\, e^{(c_{ij} - u_i - v_j - h_i(y_j - x_i))/\varepsilon}", font_size=34,
                      colors={r"\pi_{ij}": Q_C}),
                cmath(r"u_i", r"=", r"\varepsilon \ln \sum_j \nu_j\, e^{(c_{ij} - v_j - h_i(y_j - x_i))/\varepsilon}",
                      font_size=32, colors={r"u_i": HEDGE}),
                cmath(r"\sum_j \pi_{ij}(y_j - x_i)", r"=", r"0\quad\Leftarrow\quad h_i\ \text{by Newton}", font_size=32,
                      colors={r"\sum_j \pi_{ij}(y_j - x_i)": Q_C})]
        whys = [why(r"penalize the coupling's distance from independence: the problem becomes smooth and strictly "
                    r"concave", 21),
                why(r"the optimal coupling has this exponential form, the dual variables in the exponent", 21),
                why(r"setting the derivative in $u_i$ to zero gives it in closed form (and $v_j$ alike): Sinkhorn's "
                    r"scaling", 21),
                why(r"the martingale multiplier has no closed form: a one-dimensional Newton step per row; as "
                    r"$\varepsilon \to 0$ the value tends to the linear program's", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "A second method scales to far bigger problems. Add a small penalty for the joining's distance from independence, an entropy with weight epsilon. <bookmark mark='a'/> The best joining then has an explicit exponential form, the dual variables in the exponent. <bookmark mark='b'/> Each u, holding the others fixed, has a closed form, a log of a sum, and so does each v: Sinkhorn's matrix scaling. <bookmark mark='c'/> The martingale multiplier h has no closed form, but each one is a single-variable root, a Newton step. Cycle through the three, shrink epsilon, and the value approaches the program's. The penalty also makes the problem strictly concave, so the solution is unique; smooth sensitivity additionally needs regularity away from degeneracies. These finite-grid formulas assume positive reference masses and a nonempty feasible set; a fully converged entropy problem has a unique optimizer. Finite coordinate iterations have residual errors, and shrinking epsilon does not by itself prove that a finite run has converged."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def entropic_run(self, en, m):
        runs = [r for r in en["runs"] if r["side"] == "upper"]
        x, y = np.asarray(m["x"]), np.asarray(m["y"])
        steps, vals, ck = [], [], [0]
        off = 0
        for r in runs:
            t = np.asarray(r["trace"])[1:]
            steps += list(t[:, 0] + off)
            vals += list(t[:, 1])
            off += t[-1, 0]
            ck.append(off)
        steps, vals = np.array(steps), np.array(vals)
        ck[0] = steps[0]

        def frame(i):
            j = max(i - 1, 0)
            pi = np.asarray(runs[j]["pi"])
            a = axes([0.55, 1.6], [0.35, 2.1], x_length=3.8, y_length=3.6, xlabel=r"$S_1 / F_1$", ylabel=r"$S_2 / F_2$",
                     xticks=[0.6, 1.0, 1.4], yticks=[0.5, 1.0, 1.5, 2.0], font_size=13)
            top = pi.max()
            dots = VGroup(*[Dot(a.ax.c2p(x[p], y[q]), radius=0.1 * np.sqrt(pi[p, q] / top), color=Q_C).set_opacity(0.85)
                            for p in range(len(x)) for q in range(len(y)) if pi[p, q] > 1e-4 * top
                            and 0.55 < x[p] < 1.6 and 0.35 < y[q] < 2.1])
            eps = label(rf"$\varepsilon = {runs[j]['eps']:g}$", font_size=22, color=Q_C).next_to(a, UP, buff=0.05)
            return VGroup(a, dots, eps)

        rp = FullRangeReplay(steps, vals, frame, ck, ylabel=r"raw iterate payoff (may be infeasible)",
                            xlabel=r"coordinate-ascent sweeps, $\varepsilon$ shrinking", color=Q_C,
                            left=LEFT * 3.6 + DOWN * 0.2, right=RIGHT * 3.2 + DOWN * 0.2)
        lp = DashedLine(rp.ax.c2p(steps[0], m["upper"]), rp.ax.c2p(steps[-1], m["upper"]), color=HEDGE, stroke_width=2)
        lpl = MathTex(rf"\text{{LP}}\ {m['upper']:.4f}", font_size=22, color=HEDGE).next_to(lp, UP, buff=0.05).align_to(lp, RIGHT)
        finals = VGroup(*[MathTex(rf"\varepsilon = {r['eps']:g}:\ {r['value']:.4f}", font_size=22, color=Q_C)
                          for r in runs]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        finals.next_to(rp.g, DOWN, buff=0.35).align_to(rp.g, LEFT)
        guide = wrapped_label(r"left: final couplings in a central window; right: iteration payoffs after initialization (constraints may be violated)", 12.4, 18, GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"For the existing upper-side runs, shrink epsilon from a tenth to three thousandths. <bookmark mark='a'/> The plotted quantity is unpenalized expected payoff, not the entropy-adjusted objective. Its values are {runs[0]['value']:.4f}, {runs[1]['value']:.4f}, {runs[2]['value']:.4f}, and {runs[3]['value']:.4f}, versus the LP's {m['upper']:.4f}. <bookmark mark='b'/> At termination the largest L1 marginal error across these runs is {max((r['trace'][-1][2] for r in runs)):.1e}, and the largest L1 martingale error is {max((r['trace'][-1][3] for r in runs)):.1e}. Feasible couplings cannot exceed the LP maximum; finite tolerances still matter. Independence itself generally violates the martingale condition, even though the entropy reference is the product measure. The replay omits the unconstrained zero-iteration initialization and starts at the next logged sweep. Every remaining stored payoff is shown without percentile clipping; early infeasible iterates can exceed the LP value. The left-hand snapshots are final couplings for each epsilon, not all intermediate iterates."
        ) as vo:
            self.play(FadeIn(rp), Create(lp), FadeIn(lpl), FadeIn(guide))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.until("b") - 0.5, 5.0))
            self.play(FadeIn(finals))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"As the grid gets finer, can a model-free upper bound go down?")
        with self.voiceover(
            """Pause and predict. Can a finer grid give a lower upper endpoint? <bookmark mark='a'/> Yes. These re-binnings change the marginal measures, so no ordering follows. Monotonicity would need nested feasible sets with otherwise identical inputs. Report the discretization and numerical residuals."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"yes: changed marginals give non-nested feasible sets; no monotonicity or continuum error bound follows")))
        self.wait(0.4)
        self.clear_scene()
