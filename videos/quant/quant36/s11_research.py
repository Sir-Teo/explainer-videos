from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MICRO_C, MID_C, PART, SIM_C, comma, fit_right, load, sci)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        self.card()
        self.setup_()
        self.first_step()
        self.strong_markov()
        self.converge()
        self.theorem()
        self.unique()
        self.asymmetric(r)
        self.numerics(r)
        self.halflife(r)
        self.sim(r)
        self.boundary(r)
        self.markov_test(r)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The microprice theorem", r"When is the expected mid after infinitely many moves well defined, "
                          r"and when is it a fair price?", part=PART)
        with self.voiceover("For the researcher. Chapter five used Stoikov's microprice, saw that the series converged, "
                            "and saw it fail on Bitcoin. This chapter proves the theorem behind it: when the limit exists, "
                            "what it equals, and why it is a martingale. Then it tests the hypotheses where they hold and "
                            "where they do not."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"X_t", r"\in", r"\{1, \dots, K\}", font_size=40, colors={r"X_t": MICRO_C}),
                cmath(r"\textbf{H1}", r":", r"(X_t, M_t)\ \text{is Markov additive}", font_size=34),
                cmath(r"\textbf{H2}", r":", r"x \mapsto \bar x\ \text{mirrors the book},\ \ \Delta M \mapsto -\Delta M",
                      font_size=32),
                cmath(r"\textbf{H3}", r":", r"\text{every state moves eventually; } B \text{ irreducible, aperiodic}",
                      font_size=30)]
        whys = [why(r"the state of the top of the book: imbalance bucket and spread"),
                why(r"the state is a Markov chain, and each mid change depends only on the transition it rides on, never "
                    r"on the level of the mid"),
                why(r"swapping bid and ask maps the dynamics to themselves with every mid change reversed"),
                why(r"the chain cannot sit forever without a mid change, and the state seen at mid changes mixes")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The setting. <bookmark mark='a'/> The state of the top of the book takes finitely many values. "
            "<bookmark mark='b'/> Hypothesis one: the state is a Markov chain, and each change of the mid depends only on "
            "the transition it rides on, never on the mid's level. A Markov additive process. <bookmark mark='c'/> "
            "Hypothesis two, symmetry: swapping bid and ask maps the dynamics to themselves with every move reversed. "
            "<bookmark mark='d'/> Hypothesis three: no state waits forever, and the state seen at mid changes mixes."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def first_step(self):
        rows = [cmath(r"g^1(x)", r"=", r"\mathbb E_x[M_{\tau_1} - M_0]", font_size=38, colors={r"g^1(x)": MICRO_C}),
                cmath(r"g^1", r"=", r"R + Q\,g^1", font_size=40),
                cmath(r"g^1", r"=", r"(\mathbb 1 - Q)^{-1} R", font_size=40, colors={r"g^1": MICRO_C})]
        whys = [why(r"the expected first mid change, starting in state $x$; $\tau_1$ is the time of that change"),
                why(r"condition on the first step: either the mid moves now, with expected change $R(x)$, or the chain "
                    r"moves to $y$ with no change, with probability $Q(x, y)$, and starts again"),
                why(r"by H3 the spectral radius of $Q$ is below one, so $\mathbb 1 - Q$ is invertible, and its inverse "
                    r"is the series $\sum_n Q^n$: the sum over the steps spent waiting")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, the first move. <bookmark mark='a'/> Let g one of x be the expected first change of the mid from "
            "state x. <bookmark mark='b'/> Condition on the first step: the mid moves now, with expected change R, or the "
            "chain moves to another state without a change, with probability Q, and starts again. <bookmark mark='c'/> "
            "By hypothesis three, Q's spectral radius is below one, so one minus Q is invertible: its inverse is the sum "
            "over all the steps spent waiting."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def strong_markov(self):
        rows = [cmath(r"B", r"=", r"(\mathbb 1 - Q)^{-1}\,T", font_size=40),
                cmath(r"g^{i+1}", r"=", r"B\,g^i", font_size=40),
                cmath(r"\mathbb E_x[M_{\tau_n}] - M_0", r"=", r"\textstyle\sum_{k=0}^{n-1} (B^k g^1)(x)", font_size=36,
                      colors={r"\mathbb E_x[M_{\tau_n}] - M_0": MICRO_C})]
        whys = [why(r"the law of the state just after the first mid change; its rows sum to one because $Q + T$ is "
                    r"stochastic: $B$ is a stochastic matrix"),
                why(r"by the strong Markov property at $\tau_i$ and H1, the $(i{+}1)$-th change depends on the past only "
                    r"through $X_{\tau_i}$, whose law is $B^i(x, \cdot)$"),
                why(r"Stoikov's $P^n$: the expected mid after $n$ changes is the mid plus $n$ terms")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, the later moves. <bookmark mark='a'/> The same summation gives the law of the state just after "
            "the first change: B, one minus Q inverse, times T. Its rows sum to one, so B is a stochastic matrix. "
            "<bookmark mark='b'/> By the strong Markov property at each change, the next change depends on the past only "
            "through the state there. <bookmark mark='c'/> So the expected mid after n changes is the mid plus the first "
            "n terms of the series."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def converge(self):
        rows = [cmath(r"B^k", r"\to", r"\mathbb 1\pi^\top", font_size=40),
                cmath(r"\pi^\top g^1", r"=", r"0", font_size=40, colors={r"0": GOOD}),
                cmath(r"\|B^k g^1\|", r"=", r"\|(B - \mathbb 1\pi^\top)^k g^1\| \le C\,|\lambda_2|^k", font_size=34),
                cmath(r"g", r"=", r"\textstyle\sum_k B^k g^1 = (\mathbb 1 - B + \mathbb 1\pi^\top)^{-1} g^1", font_size=34,
                      colors={r"g": MICRO_C})]
        whys = [why(r"Perron--Frobenius under H3: the powers of $B$ converge to its stationary law $\pi$ in every row"),
                why(r"H2: $\pi$ is mirror-symmetric and $g^1$ antisymmetric, so they are orthogonal; without symmetry, a "
                    r"drift $\pi^\top g^1 \ne 0$ is added at every move and the series diverges"),
                why(r"$(B - \mathbb 1\pi^\top)^k = B^k - \mathbb 1\pi^\top$ for $k \ge 1$, whose spectral radius is the "
                    r"second-largest eigenvalue modulus: geometric decay"),
                why(r"a Neumann series of $B - \mathbb 1\pi^\top$: the fundamental matrix of the chain")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Lemma three, convergence. <bookmark mark='a'/> By Perron and Frobenius, the powers of B converge to the "
            "stationary law in every row. <bookmark mark='b'/> By symmetry the stationary law is mirror-symmetric and the "
            "first move antisymmetric, so they are orthogonal. Without symmetry, a drift would be added at every move and "
            "the series would diverge. <bookmark mark='c'/> So the terms are powers of B minus its limit, whose spectral "
            "radius is the second eigenvalue: they decay geometrically. <bookmark mark='d'/> And the sum is a Neumann "
            "series, with a closed form: the chain's fundamental matrix applied to the first move."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"P^{\text{micro}}_t = \lim_{n\to\infty}\mathbb E[M_{\tau_n} \mid \mathcal F_t] = M_t + g(X_t),"
                            r"\qquad g = (\mathbb 1 - B + \mathbb 1\pi^\top)^{-1} g^1", font_size=30),
                    MathTex(r"\mathbb E[P^{\text{micro}}_{\tau_1} \mid \mathcal F_t] = M_t + g^1(X_t) + (B g)(X_t) = "
                            r"P^{\text{micro}}_t", font_size=30),
                    wrapped_label(r"under H1--H3 the limit exists, converges geometrically at the rate $|\lambda_2(B)|$, "
                                  r"is antisymmetric, and is a martingale at the times of mid changes: no estimate of "
                                  r"the form $M + f(X)$ that is predictably changing can be a fair price", 9.6, 20)).arrange(
            DOWN, buff=0.35)
        card = theorem_card(r"The microprice (Stoikov 2018)", st, r"this part's proof", width=11.8, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> Under the three hypotheses, the expected mid after infinitely many "
            "changes exists, and equals the mid plus g of the state, the fundamental matrix applied to the first move. "
            "<bookmark mark='b'/> And it is a martingale at the times of mid changes: its expected value at the next "
            "change is the mid, plus the first move, plus B times g, which is g again, because g is the first move plus "
            "B times g. That last identity is the whole proof."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def unique(self):
        rows = [cmath(r"M + f(X)\ \text{a martingale}", r"\iff", r"f = g^1 + B f", font_size=34),
                cmath(r"f - g", r"\in", r"\ker(\mathbb 1 - B) = \text{span}(\mathbb 1)", font_size=36),
                cmath(r"f\ \text{antisymmetric}", r"\Rightarrow", r"f = g", font_size=38, colors={r"f = g": MICRO_C})]
        whys = [why(r"the martingale condition at mid changes, for any adjustment that depends only on the state"),
                why(r"by H3 the only harmonic functions of an irreducible chain are constants"),
                why(r"a symmetric book fixes the constant at zero: the microprice is the only fair price of this form; "
                    r"the weighted mid $f = (I - \frac12) S\,\text{tick}$ solves the equation only by coincidence")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A corollary: uniqueness. <bookmark mark='a'/> Any adjustment f of the state makes the mid plus f a martingale "
            "exactly when f equals the first move plus B times f. <bookmark mark='b'/> Two solutions differ by a harmonic "
            "function of an irreducible chain, which is a constant. <bookmark mark='c'/> Symmetry sets the constant to "
            "zero. So the microprice is the only fair price of this form, and the weighted mid is one only by "
            "coincidence."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def asymmetric(self, r):
        a = r["asym"]
        rows = [cmath(r"\text{unmirrored fit}", r":", rf"\pi^\top g^1 = {a['pi_g1_ticks']:.3f}\ \text{{tick per move}}",
                      font_size=34),
                cmath(r"\textstyle\sum_{k<n} B^k g^1", r"\approx", r"n\,\pi^\top g^1 + \text{const}", font_size=36),
                cmath(r"n = 10, 100, 400", r":", rf"{a['partial'][0]:.1f},\ {a['partial'][1]:.1f},\ "
                      rf"{a['partial'][2]:.1f}\ \text{{ticks}}", font_size=34, colors={r"n = 10, 100, 400": BAD})]
        whys = [why(r"fitted without the mirror image, the two training days carry a small upward drift per mid move"),
                why(r"the orthogonality of Lemma three fails, and the drift is added once per move, for ever"),
                why(r"the partial sums (averaged over states) grow linearly in the number of moves: there is no "
                    r"microprice without H2, only a forecast of the trend")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why symmetry is not a technicality. <bookmark mark='a'/> Fit the chain without the mirror image, and the "
            f"two training days carry a drift of {a['pi_g1_ticks']:.2f} of a tick per mid move. <bookmark mark='b'/> "
            "The orthogonality of Lemma three fails, and the drift is added once per move, for ever. "
            f"<bookmark mark='c'/> After ten moves the sum is {a['partial'][0]:.1f} ticks, after a hundred "
            f"{a['partial'][1]:.1f}, after four hundred {a['partial'][2]:.1f}. There is no microprice without symmetry: "
            "only an extrapolated trend."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def numerics(self, r):
        nm = np.asarray(r["norms"], float)
        k = np.arange(len(nm))
        ok = nm > 1e-12
        lam2 = r["eig"][1]
        y = np.log10(nm[ok])
        lo = float(np.floor(y.min()))
        hi = float(np.ceil(y.max()))
        g = axes([0, int(k[ok].max())], [lo, hi], x_length=6.4, y_length=4.4, xlabel=r"$k$",
                 ylabel=r"$\max_x |(B^k g^1)(x)|$, dollars", xticks=[0, 10, 20, 30, 40], yticks=[lo, (lo + hi) / 2, hi],
                 yfmt=lambda v: f"10^{{{v:.0f}}}" if float(v).is_integer() else "", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=MICRO_C) for a, b in zip(k[ok], y)])
        rate = Line(ax.c2p(0, y[0]), ax.c2p(k[ok].max(), y[0] + k[ok].max() * np.log10(lam2)), color=HURDLE,
                    stroke_width=2.5)
        e_pi = sci(max(abs(r["pi_g1"]), 1e-18))
        e_cs = sci(max(r["closed_vs_series"], 1e-18))
        st = VGroup(label(rf"$|\lambda_1| = {r['eig'][0]:.3f}$", font_size=18),
                    label(rf"$|\lambda_2| = {lam2:.3f}$", font_size=18, color=HURDLE),
                    label(rf"$|\pi^\top g^1| = {e_pi}$", font_size=18),
                    label(rf"series vs closed form: ${e_cs}$", font_size=18)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        st.to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        fit_right(st)
        with self.voiceover(
            "Check one: the algebra, on Chapter five's fit to Bitcoin. <bookmark mark='a'/> B's largest eigenvalue is "
            f"one, and the second {lam2:.2f}. Symmetry makes the stationary law orthogonal to the first move, to "
            "machine precision. <bookmark mark='b'/> The terms fall on the line of slope the logarithm of the second "
            "eigenvalue, and the series agrees with the closed form to thirteen digits. The theorem's conclusions hold "
            "for the fitted chain, as they must. Whether they hold for the market is a different question."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(Create(rate))
        self.wait(0.4)
        self.clear_scene()

    def halflife(self, r):
        l_b = r["eig"][1]
        l_s = r["sim"]["eig2"]
        h_b = float(np.log(0.5) / np.log(l_b))
        rows = [cmath(r"|\lambda_2|", r"=", r"\text{the share of the lean that survives a move}", font_size=32),
                cmath(r"\text{Bitcoin}", r":", rf"|\lambda_2| = {l_b:.2f},\ \ \text{{half-life}}\ {h_b:.1f}\ "
                      r"\text{moves}", font_size=34, colors={r"\text{Bitcoin}": BAD}),
                cmath(r"\text{simulator}", r":", rf"|\lambda_2| = {l_s:.3f}", font_size=34,
                      colors={r"\text{simulator}": SIM_C}),
                cmath(r"g", r"\approx", r"g^1 / (1 - |\lambda_2|)", font_size=38, colors={r"g": MICRO_C})]
        whys = [why(r"after each mid change, the expected next change is $B$ applied to the last: the second "
                    r"eigenvalue measures how much of a lean the state carries through a move"),
                why(r"Bitcoin's fitted chain keeps two-thirds of the lean through each move, so it adds the first "
                    r"move's lean about three times over"),
                why(r"in the simulator both queues are redrawn after a move, so the lean is forgotten at once and the "
                    r"microprice is essentially the first move"),
                why(r"a rough multiplier along the slowest direction: the persistence the chain believes in is what "
                    r"inflates the lean, and what the market does not deliver")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What the second eigenvalue means. <bookmark mark='a'/> It is the share of a lean that survives one mid "
            f"change. <bookmark mark='b'/> Bitcoin's fitted chain keeps {l_b:.2f} of it through each move, a half-life "
            f"of {h_b:.1f} moves, so it adds the first move's lean about three times over. <bookmark mark='c'/> In the "
            "simulator, both queues are redrawn after a move, the lean is forgotten at once, and the microprice is "
            "essentially the first move. <bookmark mark='d'/> So the multiplier is roughly one over one minus the "
            "eigenvalue: the persistence the chain believes in is exactly what inflates Bitcoin's microprice."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, r):
        s = r["sim"]
        I = (np.arange(10) + 0.5) / 10
        cols = {"mid": MID_C, "weighted": GREY_B, "micro": MICRO_C}
        top = float(np.ceil(max(abs(v) for d in s["drift"].values() for v in d) * 10) / 10)
        g = axes([0, 1], [-top, top], x_length=6.4, y_length=4.4, xlabel=r"imbalance $I$",
                 ylabel=r"mean change over the next second, ticks", xticks=[0, 0.5, 1], yticks=[-top, 0, top],
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        curves = {k: VGroup(curve(ax, I, v, cols[k], stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.06, color=cols[k])
                                                                       for a, b in zip(I, v)])
                  for k, v in s["drift"].items()}
        leg = legend([(MID_C, r"mid"), (GREY_B, r"weighted mid"), (MICRO_C, r"microprice")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        md = max(abs(v) for v in s["drift"]["mid"])
        mc = max(abs(v) for v in s["drift"]["micro"])
        with self.voiceover(
            "Check two: where the hypotheses hold. The House's queue simulator of Chapter seven is a Markov chain of "
            "queues in a large-tick world. Fit the microprice on one long run and test it on another. "
            f"<bookmark mark='a'/> The mid drifts predictably, up to {md:.2f} of a tick in a second at the extremes. "
            f"<bookmark mark='b'/> The microprice does not drift: at most {mc:.3f} of a tick. In this book the weighted "
            "mid happens to be close to the microprice, and nearly flat too."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves["mid"]))
            vo.wait_until("b")
            self.play(Create(curves["micro"]), Create(curves["weighted"]))
        self.wait(0.4)
        self.clear_scene()

    def boundary(self, r):
        hs = np.log10(np.asarray(r["sim"]["h"], float) / 10)
        hb = np.log10(np.asarray(r["btc"]["h"], float) / 10)
        bs = np.asarray(r["sim"]["beta"], float)
        bb = np.asarray(r["btc"]["beta"], float)
        g = axes([-1, 2.5], [0, 1.4], x_length=6.4, y_length=4.4, xlabel=r"horizon, seconds",
                 ylabel=r"realised drift $\div$ microprice", xticks=[-1, 0, 1, 2], xfmt=lambda v: f"10^{{{v:g}}}",
                 yticks=[0, 0.5, 1.0], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        one = DashedLine(ax.c2p(-1, 1), ax.c2p(2.5, 1), color=GREY_B, stroke_width=1.5)
        cs = VGroup(curve(ax, hs, bs, SIM_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.06, color=SIM_C)
                                                                for a, b in zip(hs, bs)])
        cb = VGroup(curve(ax, hb, bb, BAD, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.06, color=BAD)
                                                              for a, b in zip(hb, bb)])
        leg = legend([(SIM_C, r"simulator: H1--H3 hold"), (BAD, r"Bitcoin, test days")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        peak = float(bb.max())
        settle = float(np.mean(bs[-2:]))
        with self.voiceover(
            "Check three, the theorem's limit itself. Over longer and longer horizons, the mean move from each state "
            "should approach the microprice. Plot the realised drift as a fraction of it. <bookmark mark='a'/> In the "
            "simulator it climbs to about one by ten seconds, and settles near "
            f"{settle:.2f}: a little above, because ten imbalance buckets are a coarse summary of two queues, so the "
            "chain is only nearly Markov. <bookmark mark='b'/> On Bitcoin it peaks at "
            f"{peak:.2f} and falls back: the market delivers less than half of the predicted lean, and then takes some "
            "of that back. Hypothesis one fails, and the theorem's conclusion fails with it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(one))
            vo.wait_until("a")
            self.play(Create(cs))
            vo.wait_until("b")
            self.play(Create(cb))
        self.wait(0.4)
        self.clear_scene()

    def markov_test(self, r):
        mk = r["markov"]
        rows = [cmath(r"\textbf{H1}", r"\Rightarrow", r"\mathbb E[s_{i+1} \mid s_i, X_{\tau_i}] = \mathbb E[s_{i+1} \mid "
                      r"X_{\tau_i}]", font_size=32),
                cmath(r"\Delta", r"=", r"\mathbb E[s_{i+1} \mid s_i = +, x] - \mathbb E[s_{i+1} \mid s_i = -, x]",
                      font_size=32),
                cmath(r"\Delta_{\text{sim}} = " + f"{mk['sim']:.2f}", r",", r"\Delta_{\text{BTC}} = " + f"{mk['btc']:.2f}",
                      font_size=38, colors={r"\Delta_{\text{BTC}} = " + f"{mk['btc']:.2f}": BAD})]
        whys = [why(r"given the state just after a mid change, the sign of the next change cannot depend on the sign "
                    r"of the last"),
                why(r"so compare the next sign after up-moves and after down-moves, state by state, and average"),
                why(rf"in the simulator, over {comma(mk['n_sim'])} moves, the gap is near zero; on Bitcoin's test days, "
                    rf"over {comma(mk['n_btc'])} moves, a move up makes the next move up far more likely in every "
                    r"state: the hypothesis is rejected directly")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And a direct test of hypothesis one. <bookmark mark='a'/> If the state is Markov, then given the state just "
            "after a mid change, the sign of the next change cannot depend on the sign of the last. <bookmark mark='b'/> "
            "So compare the next sign after up-moves and after down-moves, within each state, and average. "
            f"<bookmark mark='c'/> In the simulator the gap is {mk['sim']:.2f}, near zero. On Bitcoin it is "
            f"{mk['btc']:.2f}: the last move's direction carries information the state does not. The hypothesis fails "
            "directly, which is why the theorem's limit failed in the previous check."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Avellaneda, Reed and Stoikov (2011)", r"the probability of an up-move from the two best queues "
                          r"in a diffusion model with hidden liquidity: the one-step version of the microprice", width=12.4,
                          font_size=18),
            desk_question(r"Gould and Bonart (2016)", r"queue imbalance as a one-tick-ahead predictor across Nasdaq "
                          r"stocks: strong for large-tick stocks, weak for small-tick ones, which is this chapter's "
                          r"boundary", width=12.4, font_size=18),
            desk_question(r"Stoikov (2018)", r"the definition, the Markov-chain estimator and the convergence condition; "
                          r"tested on a large-tick and a smaller-tick US stock", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Marco Avellaneda, Josh Reed and Sasha Stoikov derived the probability "
            "of an up-move from the two best queues, with hidden liquidity: the one-step version. <bookmark mark='b'/> "
            "Martin Gould and Julius Bonart tested queue imbalance across Nasdaq stocks, and found it strong for "
            "large-tick stocks and weak for small-tick ones: the same boundary. <bookmark mark='c'/> And Stoikov's "
            "paper gives the definition, the estimator and the convergence condition proved here."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the smallest Markov state", r"which finite summary of a small-tick book (depth, recent "
                          r"flow, spread) makes H1 hold well enough that the microprice's limit matches the market's?",
                          width=12.4, font_size=18),
            desk_question(r"open: microprices with memory", r"under self-exciting (Hawkes) order flow the state is "
                          r"infinite-dimensional; a computable fair price with error bounds is not known", width=12.4,
                          font_size=18),
            desk_question(r"open: fragmented books", r"one asset on many venues, each with its own queues: the fair price "
                          r"of the consolidated book, and who leads, has no general theory", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> What is the smallest summary of a small-tick book that is Markov "
            "enough for the microprice's limit to match the market's? <bookmark mark='b'/> Under self-exciting order "
            "flow the state is infinite-dimensional: a computable fair price with error bounds is not known. "
            "<bookmark mark='c'/> And one asset traded on many venues, each with its own queues: the fair price of the "
            "consolidated book has no general theory."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two states, bid-heavy and offer-heavy. From bid-heavy the next mid change is $+1$ tick with "
                       r"probability $\frac34$, else $-1$; after any change the state stays the same with probability "
                       r"$p$. What is the microprice's lean for $p = \frac34$, and as $p \to 1$?")
        with self.voiceover(
            "Pause and predict. Two states, bid-heavy and offer-heavy. From bid-heavy, the next mid change is up one "
            "tick with probability three-quarters, otherwise down one. After any change the state stays the same with "
            "probability p. What is the microprice's lean when p is three-quarters, and what happens as p goes to one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
