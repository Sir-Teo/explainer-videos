from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class MFG(VoiceoverScene):
    def construct(self):
        m = load("mfg_crowd")
        self.card()
        self.derive()
        self.play_fictitious(m)
        self.lab(m)
        self.crowd(m)

    def card(self):
        c = chapter_card(15, r"Mean-field games: the crowd that sells together", r"How do you trade when everyone "
                         r"else is solving the same problem?", part=PART)
        with self.voiceover("Chapter fifteen. Mean-field games: the crowd that sells together."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"d(X + QS)", r"=", r"-\eta v^2\,dt - \kappa\,\bar v\,Q\,dt + Q\sigma\,dW", font_size=32),
                cmath(r"\min_Q", r"\ ", r"\int_0^T\big(\eta\,Q'^2 + \kappa\,m(t)\,Q + \phi\,Q^2\big)\,dt", font_size=32),
                cmath(r"2\eta\,Q''", r"=", r"\kappa\,m + 2\phi\,Q", font_size=32),
                cmath(r"m = -\tfrac{N-1}{N}Q'", r"\ \Rightarrow\ ", r"2\eta\,Q'' + \kappa\tfrac{N-1}{N}\,Q' - 2\phi\,Q = 0",
                      font_size=32, colors={r"m = -\tfrac{N-1}{N}Q'": ALT}),
                cmath(r"\phi = 0:\ \ Q'(t)", r"\propto", r"e^{-at},\qquad a = \frac{\kappa(N-1)}{2N\eta}", font_size=32,
                      colors={r"\phi = 0:\ \ Q'(t)": KELLY})]
        whys = [why(r"each of $N$ traders sells $v = -Q'$; temporary cost $\eta v^2$; the price drifts down by $\kappa$ "
                    r"times the average selling rate $\bar v$; own impact integrates to a constant", font_size=20),
                why(r"so the expected cost depends on the others' average rate $m$ (and a risk penalty $\phi Q^2$)",
                    font_size=20),
                why(r"the Euler--Lagrange equation: the trader's best response to $m$ (backward: an HJB in disguise)",
                    font_size=20),
                why(r"consistency: in a symmetric equilibrium the others do the same thing (forward: the crowd); the "
                    r"fixed point", font_size=20),
                why(r"$N = 1$: a straight line, TWAP (Almgren--Chriss with no risk aversion); $N \to \infty$: the "
                    r"mean-field game, a race to sell first", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.95, edge=6.9)
        with self.voiceover(
            "Now many traders face each other. In a mean-field game each player solves a control problem backwards, "
            "taking the crowd as given, while the crowd moves forwards, driven by everyone's choices. Lasry and Lions, and "
            "Huang, Malhamé and Caines, introduced it in 2006. <bookmark mark='a'/> A case with a closed form: N funds each "
            "sell a block by time T; selling fast costs a premium, and everyone's selling pushes the price down. "
            "<bookmark mark='b'/> A plan's cost depends on the others' average selling rate. <bookmark mark='c'/> The best "
            "response solves an Euler-Lagrange equation. <bookmark mark='d'/> Consistency, the others do the same, gives one "
            "linear equation. <bookmark mark='e'/> Alone, sell in a straight line; in a crowd, sell in a rush, before the "
            "others' selling lands in the price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
        self.wait(0.4)
        self.clear_scene()

    def play_fictitious(self, m):
        t = np.asarray(m["t"])
        reps = m["replay"]
        g = axes([0, 1], [0, 1.0], x_length=5.6, y_length=3.6, xlabel=r"time", ylabel=r"inventory $Q$ (from 1)",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        g2 = axes([0, 1], [0, 2.4], x_length=5.6, y_length=3.6, xlabel=r"time", ylabel=r"the crowd's selling rate $m$",
                  xticks=[0, 0.5, 1], yticks=[0, 1, 2], font_size=15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        arr1 = Arrow(g.get_corner(UR) + LEFT * 0.2 + UP * 0.35, g.get_corner(UL) + RIGHT * 0.4 + UP * 0.35, color=VALUE,
                     buff=0, stroke_width=3)
        a1 = label(r"each trader's plan: solved backwards", font_size=18, color=VALUE).next_to(arr1, UP, buff=0.05)
        arr2 = Arrow(g2.get_corner(UL) + RIGHT * 0.4 + UP * 0.35, g2.get_corner(UR) + LEFT * 0.2 + UP * 0.35, color=ALT,
                     buff=0, stroke_width=3)
        a2 = label(r"the crowd: rolled forwards", font_size=18, color=ALT).next_to(arr2, UP, buff=0.05)
        closed = curve(g.ax, t, np.asarray(m["runs"]["inf"]["closed"]), GREY_B, stroke_width=2)
        cm = -np.gradient(np.asarray(m["runs"]["inf"]["closed"]), t)
        closed_m = curve(g2.ax, t, np.clip(cm, 0, 2.4), GREY_B, stroke_width=2)

        def fr(i):
            return VGroup(curve(g.ax, t, np.asarray(reps[i]["Q"]), VALUE, stroke_width=4),
                          curve(g2.ax, t, np.clip(np.asarray(reps[i]["m"]), 0, 2.4), ALT, stroke_width=4),
                          MathTex(rf"\text{{iteration }} {i + 1}", font_size=28, color=GREY_A).to_edge(UP, buff=0.4))

        cur = fr(0)
        with self.voiceover(
            "How does a crowd find that equilibrium? One answer is fictitious play. On the left, a trader's plan, solved "
            "backwards from the deadline; on the right, the crowd's selling rate, rolled forwards. Start by assuming the crowd "
            "does nothing. <bookmark mark='a'/> The best response to a passive crowd is a straight line. Then let the crowd "
            "adopt that plan, and respond again; each round mixes half of the new crowd into the old. The curves overshoot, "
            "then settle, round by round, onto the grey equilibrium, where the plan produces exactly the crowd it assumed."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2), GrowArrow(arr1), FadeIn(a1), GrowArrow(arr2), FadeIn(a2), FadeIn(closed),
                      FadeIn(closed_m))
            vo.wait_until("a")
            self.play(FadeIn(cur))
            per = max(min((vo.remaining(6.0) - 1) / (len(reps) - 1), 1.2), 0.5)
            for i in range(1, len(reps)):
                self.play(Transform(cur, fr(i)), run_time=per)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, m):
        card = lab_card(r"fictitious play", [
            "def mfg_liquidation(N, kappa, eta, phi, T, n, iters, damping):",
            "    A = tridiag(2*eta/h**2, -4*eta/h**2 - 2*phi, 2*eta/h**2)",
            "    share = 1 - 1/N if isfinite(N) else 1.0",
            "    m = zeros(n + 1)                       # the crowd's rate",
            "    for _ in range(iters):",
            "        rhs = kappa*m[1:-1]; rhs[0] -= 2*eta/h**2 * q0",
            "        Q[1:-1] = solve_banded((1, 1), A, rhs)   # best response",
            "        new = share * -gradient(Q, h)       # what the crowd does",
            "        res.append(max(abs(new - m)))",
            "        m = (1 - damping)*m + damping*new",
            "    return Q, m, res",
        ], source="explainer/quant/house/control.py", width=8.4, font_size=17).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.3)
        R = m["runs"]
        res = np.asarray(R["inf"]["residual"])
        outs = [f"iter {i + 1:>2}: residual {res[i]:.1e}" for i in (0, 4, 9, 19, 29, 39, len(res) - 1)]
        outs.append("sold in the first fifth: " + "  ".join(
            f"N={k}: {100 * R[k]['share_fifth']:.1f}%" for k in ("1", "2", "10", "inf")))
        with self.voiceover(
            "Lab four: given the crowd's rate, the best response is one tridiagonal solve; the crowd's new rate is its "
            "slope; mix and repeat. <bookmark mark='a'/> The residual falls geometrically, below ten to the minus "
            f"{-int(np.floor(np.log10(res[-1])))} after {len(res)} rounds, matching the closed form to grid error. In the "
            f"first fifth of the time: {100 * R['1']['share_fifth']:.0f} percent alone, {100 * R['2']['share_fifth']:.1f} with "
            f"two funds, {100 * R['10']['share_fifth']:.1f} with ten, {100 * R['inf']['share_fifth']:.1f} in the limit."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["mfg_liquidation(inf, kappa=4, eta=1, phi=0, T=1, n=1000, iters=500, damping=0.5)"]
                    + outs, run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def crowd(self, m):
        t = np.asarray(m["t"])
        R = m["runs"]
        g = axes([0, 1], [0, 1.0], x_length=5.4, y_length=3.8, xlabel=r"time", ylabel=r"inventory left",
                 xticks=[0, 0.2, 0.5, 1], yticks=[0, 0.5, 1], font_size=15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"1": GREY_B, "2": UNDER, "10": VALUE, "inf": OVER}
        lines = {k: curve(ax, t, np.asarray(R[k]["Q"]), c_, stroke_width=4) for k, c_ in cols.items()}
        names = {"1": r"$N = 1$ (TWAP)", "2": r"$N = 2$", "10": r"$N = 10$", "inf": r"$N \to \infty$"}
        leg = legend([(cols[k], names[k]) for k in cols], font_size=17).next_to(g, UP, buff=0.05).align_to(g, LEFT)
        fifth = DashedLine(ax.c2p(0.2, 0), ax.c2p(0.2, 1), color=GREY_C, stroke_width=1.5)
        cr = m["crowd"]
        tc, Qc = np.asarray(cr["t"]), np.asarray(cr["Q"])
        g2 = axes([0, 1], [-0.1, 1.6], x_length=5.4, y_length=3.8, xlabel=r"time", ylabel=r"500 traders' inventories",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1, 1.5], font_size=15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        k = ValueTracker(0)
        rng = np.random.default_rng(3)
        jit = rng.uniform(-0.012, 0.012, Qc.shape[1])
        dots = VGroup(*[Dot(g2.ax.c2p(jit[j], Qc[0, j]), radius=0.02, color=ALT).set_opacity(0.6)
                        for j in range(Qc.shape[1])])

        def mv(grp):
            x = k.get_value()
            i = min(int(x), len(tc) - 2)
            f = x - i
            for j, d_ in enumerate(grp):
                y = Qc[i, j] * (1 - f) + Qc[i + 1, j] * f
                d_.move_to(g2.ax.c2p(tc[i] * (1 - f) + tc[i + 1] * f + jit[j], y))

        dots.add_updater(mv)
        q = pause_card(r"You know 9 other funds are selling the same stock this week. Sell faster or slower than "
                       r"alone?", width=5.4, font_size=20).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"Cardaliaguet and Lehalle (2018): trade crowding as a mean-field game of controls; Carlin, "
                             r"Lobo and Viswanathan (2007): predatory trading among a few; Lacker and Zariphopoulou "
                             r"(2019): competition on relative performance makes managers take more risk", 12.6, 18,
                             GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Pause and predict: you know nine other funds are selling the same stock this week. Do you sell faster or slower "
            "than you would alone? <bookmark mark='a'/> Faster. Alone, the straight line; with two funds the curve bends; "
            "with ten, more; in the mean-field limit the block goes in a rush. <bookmark mark='b'/> On the right, five hundred "
            "funds with different block sizes, each responding to the same crowd: the whole distribution of inventories runs "
            "toward zero early, and every fund pays for the others' haste. <bookmark mark='c'/> This is the mathematics of "
            "crowded trades. Pierre Cardaliaguet and Charles-Albert Lehalle modelled crowding this way in 2018; Carlin, Lobo "
            "and Viswanathan studied predatory trading among a few; and Lacker and Zariphopoulou showed that funds judged "
            "against each other take more risk. Parts thirty-six and thirty-seven return to it."
            " Next: can a machine learn these rules from experience alone?"
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), FadeIn(g), FadeIn(leg), Create(fifth), Create(lines["1"]))
            for kk in ("2", "10", "inf"):
                self.play(TransformFromCopy(lines["1"] if kk == "2" else lines[{"10": "2", "inf": "10"}[kk]],
                                            lines[kk]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(dots))
            self.play(k.animate.set_value(len(tc) - 1.001), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        dots.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
