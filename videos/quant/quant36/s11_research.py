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
        with self.voiceover('For the researcher. Separate a mathematical theorem for a specified Markov-additive process from an estimator fitted to a coarse book summary. We prove the centered finite-state result, including the correct spectral bound and normalization. Then we inspect algebraic and empirical diagnostics. A Markov queue simulator is not proof that the bucketed state satisfies the theorem.'):
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
            "The hypotheses of a model theorem. <bookmark mark='a'/> A finite state describes the chosen process, with integrable first-move rewards. <bookmark mark='b'/> The joint state and price are Markov additive: translation of the price level does not alter the transition and increment law. <bookmark mark='c'/> A mirror involution reverses increments and preserves transition probabilities. It is a sufficient centering condition. <bookmark mark='d'/> The no-move operator has spectral radius below one; the post-move operator is stochastic, irreducible and aperiodic on the actual state support. These are hypotheses to verify, not consequences of labeling a grid with imbalance buckets."
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
                cmath(r"\|B^k g^1\|", r"=", '\\|(B - \\mathbb 1\\pi^\\top)^k g^1\\| \\le C_\\rho\\rho^k', font_size=34),
                cmath(r"g", r"=", r"\textstyle\sum_k B^k g^1 = (\mathbb 1 - B + \mathbb 1\pi^\top)^{-1} g^1", font_size=34,
                      colors={r"g": MICRO_C})]
        whys = [why(r"Perron--Frobenius under H3: the powers of $B$ converge to its stationary law $\pi$ in every row"),
                why('H2 is sufficient for $\\pi^\\top g^1=0$, not necessary; a nonzero stationary reward makes uncentered partial sums diverge'),
                why('$|\\lambda_2|<\\rho<1$ permits a finite $C_\\rho$; exact $|\\lambda_2|^k$ bounds need additional control of Jordan blocks'),
                why(r"a Neumann series of $B - \mathbb 1\pi^\top$: the fundamental matrix of the chain")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The centered convergence argument. <bookmark mark='a'/> A finite irreducible aperiodic stochastic B has a unique stationary distribution pi, and its powers tend to the all-rows stationary matrix. <bookmark mark='b'/> Mirroring makes the first-move reward antisymmetric and pi symmetric, so pi times g one is zero. Symmetry is sufficient, not necessary: an unmirrored chain can also have zero stationary reward. <bookmark mark='c'/> Let A be B minus its stationary projection. For any rho strictly above A's spectral radius and below one, a finite constant bounds the norm of A to the k by C rho to the k. Using exactly the second eigenvalue modulus can fail for Jordan blocks; diagonalizability supplies that stronger bound. <bookmark mark='d'/> The centered Neumann series therefore converges to the fundamental matrix applied to g one, with stationary mean zero."
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
                    wrapped_label('under H1--H3 and integrable rewards: centered limit, antisymmetry and a move-time martingale; geometric bound for every $|\\lambda_2|<\\rho<1$. This does not identify an executable price or fundamental value', 9.6, 20)).arrange(
            DOWN, buff=0.35)
        card = theorem_card(r"The microprice (Stoikov 2018)", st, r"this part's proof", width=11.8, font_size=22)
        with self.voiceover(
            "The conclusion under the stated hypotheses and integrability. <bookmark mark='a'/> The expected midpoint after n future moves converges to the current midpoint plus the centered state adjustment g. The inverse of identity minus B plus the stationary projection gives that adjustment. <bookmark mark='b'/> At move times, expected next price is the current midpoint plus g one plus B g, equal to midpoint plus g by the Poisson equation. This proves a martingale in the model's move-time filtration. It does not identify fundamental economic value, a tradable execution price or a physical-clock result without the corresponding stopping and timing conditions."
        ) as vo:
            self.wait(0.1)
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
                why('stationary mean zero fixes the additive constant; valid mirror antisymmetry also fixes it; this does not identify fundamental value')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The normalization is essential. <bookmark mark='a'/> A state-adjusted price is a move-time martingale exactly when f equals g one plus B f, under the model and integrability conditions. <bookmark mark='b'/> Any two solutions differ by a harmonic vector. For a finite irreducible stochastic chain, the maximum principle makes every harmonic vector constant. <bookmark mark='c'/> Thus solutions are unique up to an additive constant. Stationary mean zero fixes it; under a valid mirror symmetry, requiring antisymmetry also fixes it. The weighted midpoint solves this equation only for particular transition laws, rather than being universally excluded."
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
                why('this unmirrored fit has nonzero stationary reward; asymmetry alone does not prevent a centered limit')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""What nonzero stationary reward does. <bookmark mark='a'/> This particular unmirrored fit has stationary reward {a['pi_g1_ticks']:.2f} ticks per move. <bookmark mark='b'/> If that reward is nonzero, the expected n-move sum contains n times the stationary reward plus a bounded centered correction, so the uncentered limit cannot exist. <bookmark mark='c'/> The stored partial sums are {a['partial'][0]:.1f}, {a['partial'][1]:.1f} and {a['partial'][2]:.1f} ticks after ten, one hundred and four hundred moves. Removing mirror augmentation does not logically require nonzero drift. An asymmetric chain with zero stationary reward can still satisfy the centered theorem."""
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
            f"""An algebra check for the fitted operator. <bookmark mark='a'/> The largest eigenvalue is numerically one; the next modulus is {lam2:.2f}. The retained nominal state counts are all positive in this restored fit, though some two-tick states are sparsely observed. Mirroring yields a stationary reward near floating-point zero. <bookmark mark='b'/> The finite series agrees with the closed form at the displayed residual, and the sampled norms decay. This supports numerical consistency of these stored quantities. It does not independently verify irreducibility, all transition probabilities, sampling uncertainty or the Markov sufficiency of market observations."""
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
        rows = [cmath(r"|\lambda_2|", r"=", '\\text{dominant mode magnitude}', font_size=32),
                cmath(r"\text{Bitcoin}", r":", rf"|\lambda_2| = {l_b:.2f},\ \ \text{{half-life}}\ {h_b:.1f}\ "
                      r"\text{moves}", font_size=34, colors={r"\text{Bitcoin}": BAD}),
                cmath(r"\text{simulator}", r":", rf"|\lambda_2| = {l_s:.3f}", font_size=34,
                      colors={r"\text{simulator}": SIM_C}),
                cmath(r"g", r"\approx", 'g^1_{\\lambda}/(1-\\lambda)\\quad\\text{for one eigenmode}', font_size=38, colors={r"g": MICRO_C})]
        whys = [why('each eigenmode scales by its signed eigenvalue; a general reward combines modes and may have Jordan or nonnormal effects'),
                why('the displayed positive dominant mode has a magnitude half-life near 1.7 moves; its scalar multiplier is near three'),
                why('the simulator has a different projected spectrum; full-queue resets do not prove immediate forgetting after bucketing'),
                why(r"a rough multiplier along the slowest direction: the persistence the chain believes in is what "
                    r"inflates the lean, and what the market does not deliver")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""An eigenmode interpretation. <bookmark mark='a'/> A component aligned with an eigenvector of eigenvalue lambda is multiplied by lambda at each move. A general lean is a sum of modes and may have nonnormal or Jordan effects. <bookmark mark='b'/> For the dominant displayed positive mode, modulus {l_b:.2f} gives a magnitude half-life of {h_b:.1f} moves and a scalar geometric multiplier near three. <bookmark mark='c'/> The simulator's projected operator has a different spectrum; resetting full queues does not prove every imbalance bucket immediately forgets. <bookmark mark='d'/> One over one minus lambda is a mode-specific multiplier, not a universal multiplier of the entire first-move vector."""
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
            f"""A simulated diagnostic, with separate fit and evaluation runs. <bookmark mark='a'/> The full queue process is Markov by construction, while the fitted imbalance/spread projection can retain omitted-state dependence. Its extreme one-second midpoint mean is about {md:.2f} tick. <bookmark mark='b'/> The microprice's largest displayed absolute mean is {mc:.3f} tick; small plotted means do not certify an exact martingale. No robust uncertainty calculation or full conditional test is made. This is evidence about this simulator and this projection, not a setting in which every theorem hypothesis is automatically true."""
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
        leg = legend([(SIM_C, 'simulator: coarse projected state'), (BAD, r"Bitcoin, test days")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        peak = float(bb.max())
        settle = float(np.mean(bs[-2:]))
        with self.voiceover(
            f"""A finite-horizon comparison. <bookmark mark='a'/> Regress the mean future mid change across buckets on the fitted adjustment, using the displayed weighting convention. The simulator coefficient approaches roughly {settle:.2f} over the sampled horizons; four fixed evaluation runs give a descriptive spread, not a universal limit proof. Bucket coarseness and omitted queue scale are possible discrepancies. <bookmark mark='b'/> The Bitcoin coefficient peaks at {peak:.2f} and later declines. This is an aggregate regression coefficient, not the fraction of every individual state's lean realized, nor proof about an infinite-horizon limit. Day concatenation and dependence also affect interpretation."""
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
                why(f"in the simulator, over {comma(mk['n_sim'])} moves, the gap is near zero; on Bitcoin's test days, over {comma(mk['n_btc'])} moves; count-weighted signed difference over qualifying states, without a robust interval or every-state rejection")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""A necessary implication of the proposed observed state. <bookmark mark='a'/> Under the stated Markov-additive law, the next sign distribution conditional on the post-move state cannot additionally depend on the previous sign. <bookmark mark='b'/> The code compares conditional mean next signs only in states with more than twenty observations of both previous directions, then takes a count-weighted signed average. Opposite differences can cancel. <bookmark mark='c'/> The recorded averages are {mk['sim']:.2f} in simulation and {mk['btc']:.2f} for Bitcoin. With no robust interval and dependence across moves, they are diagnostics of omitted history. A small aggregate gap does not prove Markovity, and a large gap does not isolate its causal source."""
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
                if k_:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the smallest Markov state", r"which finite summary of a small-tick book (depth, recent "
                          r"flow, spread) makes H1 hold well enough that the microprice's limit matches the market's?",
                          width=12.4, font_size=18),
            desk_question(r"open: microprices with memory", 'exponential Hawkes kernels admit finite-dimensional intensity states; general kernels may need history approximations and model-specific error bounds', width=12.4,
                          font_size=18),
            desk_question(r"open: fragmented books", 'multi-venue models need explicit routing, latency, cross-venue dynamics and a target horizon', width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three research directions with precise limits. <bookmark mark='a'/> Find a manageable state whose forecasts and conditional diagnostics remain stable across markets and regimes; approximate sufficiency must be tested. <bookmark mark='b'/> Exponential Hawkes kernels admit finite-dimensional intensity states, while general history kernels may need an infinite-dimensional state or an approximation. Computable price adjustments and error bounds depend on the specified model, so there is no universal impossibility claim. <bookmark mark='c'/> Multi-venue queues add routing, latency and cross-venue dependence. A consolidated-price model must state those mechanics and a target horizon before any theorem or forecast claim."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                if k_:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('Solve the centered Poisson equation', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('B=\\begin{pmatrix}p&1-p\\\\1-p&p\\end{pmatrix},\\quad g^1=(2q-1)\\binom{1}{-1},\\quad p=q=\\tfrac34', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('At each move the increment is plus/minus one tick; integrable reward. Normalize by stationary mean zero.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Derive $g$ from $g=g^1+Bg$. What happens as $p$ approaches one with $q$ fixed above one half?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('Two mirror states have post-move persistence p. From the bid-heavy state the next midpoint change is plus one tick with probability q and minus one otherwise, with the mirror reward in the other state. Normalize the adjustment to stationary mean zero. Solve the displayed Poisson equation, evaluate p and q at three-quarters, and discuss the limit as p approaches one with q fixed. These are full-tick model increments, not the half-tick increments of every earlier example.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
