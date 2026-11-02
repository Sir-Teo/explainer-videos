from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, P_C, PART, PUT, Q_C, answer_under, illustration, load,
                                        pause_at)


def heat(M, size=0.36, lo=None, hi=None, color_lo=None, color_hi=None):
    M = np.asarray(M)
    lo = M.min() if lo is None else lo
    hi = M.max() if hi is None else hi
    g = VGroup()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = float(np.clip((M[i, j] - lo) / (hi - lo + 1e-12), 0, 1))
            g.add(Square(size, stroke_width=0.5, stroke_color=BACKGROUND,
                         fill_color=interpolate_color(ManimColor(color_lo or BACKGROUND), ManimColor(color_hi or Q_C), v),
                         fill_opacity=1).move_to([j * size, -i * size, 0]))
    return g


class Ross(VoiceoverScene):
    def construct(self):
        r, sw = load("ross"), load("ross_sweep")
        self.card()
        self.theorem()
        self.power(sw)
        self.economies(r)
        self.critique()
        self.sweep(sw)
        self.evidence()
        self.predict()

    def card(self):
        c = chapter_card(14, r"Ross recovery, and its critique", r"Can option prices reveal real probabilities?",
                         lit=(2015,), part=PART)
        with self.voiceover("Chapter fourteen. Ross recovery, and its critique."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        rows = [cmath(r"P_{ij}", r"=", r"\pi_{ij}\, m_{ij}", font_size=38, colors={r"P_{ij}": Q_C}),
                cmath(r"m_{ij}", r"=", r"\delta\,\frac{\phi_j}{\phi_i}", font_size=38, colors={r"m_{ij}": ALT}),
                cmath(r"\pi_{ij}", r"=", r"\frac{1}{\delta}\, P_{ij}\,\frac{\phi_i}{\phi_j}", font_size=38,
                      colors={r"\pi_{ij}": P_C}),
                cmath(r"\sum_j P_{ij} z_j", r"=", r"\delta z_i,\qquad z = 1/\phi", font_size=38, colors={r"\sum_j P_{ij} z_j": CALL}),
                cmath(r"P z = \delta z,\ \ z > 0", r"\Rightarrow", r"z\ \text{unique}\ \Rightarrow\ \pi\ \text{recovered}",
                      font_size=36, colors={r"P z = \delta z,\ \ z > 0": CALL})]
        whys = [why(r"state prices for moving from state $i$ to $j$: the real transition probability times the "
                    r"discount factor", 21),
                why(r"Ross's assumption (2015): a discount rate and a ratio of one function of the state, as for a "
                    r"representative investor's marginal utility", 21),
                why(r"solve for the real probabilities", 21),
                why(r"each row of $\pi$ sums to one", 21),
                why(r"Perron--Frobenius: an irreducible non-negative matrix has exactly one positive eigenvector", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "Option prices give Q. Can they give P, the probabilities the market really believes? Stephen Ross "
            "claimed in 2015 that they can. Suppose the economy moves between a few states, and options reveal the "
            "price of moving from state i to state j: the real transition probability times the discount factor. "
            "<bookmark mark='a'/> Ross's assumption: the discount factor is a constant discount rate times a ratio "
            "of one function of the state, the way a representative investor's marginal utility would be. "
            "<bookmark mark='b'/> Then the real probabilities are the state prices, rescaled. <bookmark mark='c'/> "
            "And because each row of real probabilities must sum to one, the reciprocal of that function is an "
            "eigenvector of the state-price matrix, with eigenvalue the discount rate. <bookmark mark='d'/> Oskar "
            "Perron and Georg Frobenius proved that a matrix like this has exactly one positive eigenvector. So it "
            "is pinned down, and so are the real probabilities. From prices alone."
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
        self.wait(0.3)
        self.clear_scene()

    def power(self, sw):
        with verbatim():
            card = lab_card(r"the Perron vector by power iteration", [
                "def power_iteration(P, k=40):",
                "    z = ones(len(P)) / len(P)",
                "    for _ in range(k):",
                "        w = P @ z               # multiply by the state prices",
                "        delta = w.sum() / z.sum()",
                "        z = w / w.sum()         # renormalize",
                "    return z, delta",
            ], source="explainer/quant/house/arbitrage.py", width=6.6, font_size=17).to_corner(UL, buff=0.35)
        Z = np.asarray(sw["z"])
        lam = np.asarray(sw["delta_iter"])
        n = Z.shape[1]
        g = axes([0, n], [0, Z.max() * 1.25], x_length=5.4, y_length=3.0, ylabel=r"the vector $z$ (normalized)",
                 xticks=[], yticks=[], font_size=15)
        g.to_corner(UR, buff=0.5)
        ax = g.ax
        k = ValueTracker(0)

        def bars():
            i = int(round(k.get_value()))
            return VGroup(*[Rectangle(width=0.45, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                      fill_color=CALL, fill_opacity=0.85).move_to(ax.c2p(j + 0.5, v / 2))
                            for j, v in enumerate(Z[i])])

        B = always_redraw(bars)
        rd = always_redraw(lambda: MathTex(rf"k = {int(round(k.get_value()))}:\ \ \delta_k = "
                                           rf"{lam[max(int(round(k.get_value())) - 1, 0)]:.5f}", font_size=30,
                                           color=CALL).next_to(g, DOWN, buff=0.3))
        sl = label(r"states: low consumption $\to$ high", font_size=17, color=GREY_B).next_to(g, DOWN, buff=0.9)
        dl = MathTex(rf"\text{{true }}\delta = {sw['delta']:.2f}", font_size=28, color=Q_C).next_to(sl, DOWN, buff=0.2)
        with self.voiceover(
            "The House finds that eigenvector the oldest way there is. Start from a flat vector and multiply it by "
            "the state-price matrix, again and again, renormalizing each time. <bookmark mark='a'/> On a nine-state "
            "test economy the vector wobbles for a few steps, then freezes into the Perron vector, and the growth "
            f"factor settles on the discount rate: {lam[0]:.4f} after one step, {lam[9]:.4f} after ten, "
            f"{lam[-1]:.5f} after sixty, against a true {sw['delta']:.2f}."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(g), FadeIn(sl), FadeIn(dl))
            self.add(B, rd)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(Z) - 1), run_time=max(vo.remaining(1.0) - 0.5, 4.0),
                      rate_func=rate_functions.ease_out_cubic)
        B.clear_updaters()
        rd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def economies(self, r):
        pi, rec, rec2 = (np.asarray(r[k]) for k in ("pi", "recovered", "recovered2"))
        hi = max(pi.max(), rec2.max())
        h1, h2, h3 = (heat(M, size=0.27, lo=0, hi=hi) for M in (pi, rec, rec2))
        h4 = heat(np.abs(rec2 - pi), size=0.27, lo=0, hi=np.abs(rec2 - pi).max(), color_hi=ARB)
        tl = [label(t, font_size=19, color=c) for t, c in ((r"the truth", GREY_A), (r"recovered: Ross's world", CALL),
                                                          (r"recovered: permanent shocks", ARB),
                                                          (r"its error, magnified", ARB))]
        blocks = VGroup(*[VGroup(t_, h).arrange(DOWN, buff=0.15) for t_, h in zip(tl, (h1, h2, h3, h4))])
        blocks.arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.6)
        sub = label(r"transition probabilities between 9 states of the economy (rows: today, columns: tomorrow)",
                    font_size=19, color=GREY_B).next_to(blocks, DOWN, buff=0.2)
        side = VGroup(
            MathTex(rf"\text{{Ross's world: largest error }} < 10^{{{int(np.ceil(np.log10(max(r['err1'], 1e-16))))}}}",
                    font_size=28, color=CALL),
            MathTex(rf"\text{{with permanent shocks: }} {r['err2']:.3f}", font_size=28, color=ARB),
            MathTex(rf"\text{{long-run consumption vs trend: true }} {100 * r['mean_true']:+.1f}\%,\ \text{{recovered }} "
                    rf"{100 * r['mean_rec2']:+.1f}\%", font_size=28, color=ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        src = illustration(r"two synthetic economies with a known truth")
        with self.voiceover(
            "Test it where the truth is known. A synthetic economy with nine states, and a representative investor "
            "with constant relative risk aversion: exactly Ross's assumption. <bookmark mark='a'/> From state prices "
            "alone, the recovered probabilities match the truth to the last digit. <bookmark mark='b'/> Now add what "
            "real economies have: a permanent component in the discount factor, shocks to wealth that do not wash "
            "out. The recovery still returns a clean answer, but the wrong one. It is pessimistic: it puts the "
            f"economy's long-run level {100 * abs(r['mean_rec2']):.1f} percent below trend when the truth is "
            f"{100 * r['mean_true']:.1f} percent above."
        ) as vo:
            self.play(FadeIn(blocks[0]), FadeIn(sub), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(blocks[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(blocks[2]), FadeIn(blocks[3]), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def critique(self):
        rows = [cmath(r"M_t", r"=", r"e^{-\rho t}\,\frac{\hat\phi(X_0)}{\hat\phi(X_t)}\,\hat M_t,\qquad \hat M\ "
                      r"\text{a martingale}", font_size=34, colors={r"M_t": ALT}),
                cmath(r"\text{eigen-recovery}", r"\Rightarrow", r"\hat P,\qquad \frac{d\hat P}{dP}\Big|_{\mathcal F_t} = "
                      r"\hat M_t", font_size=34, colors={r"\text{eigen-recovery}": CALL}),
                cmath(r"\hat P = P", r"\iff", r"\hat M \equiv 1", font_size=36, colors={r"\hat P = P": ARB})]
        whys = [why(r"Hansen and Scheinkman's factorization: a transient part, as Ross assumed, times a permanent "
                    r"martingale part", 21),
                why(r"the eigenvector finds the transient part; what it returns is $P$ tilted by the permanent part: "
                    r"the long-run risk-neutral measure, the measure with the long bond as numeraire (Martin and Ross "
                    r"2019; Qin and Linetsky 2016)", 21),
                why(r"so recovery is right exactly when the discount factor has no permanent part, and prices alone "
                    r"cannot tell (Borovi\v{c}ka, Hansen and Scheinkman 2016)", 21)]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "Jaroslav Borovička, Lars Hansen and José Scheinkman explained why, in 2016. Any discount factor of this "
            "kind factors into a transient part, exactly the shape Ross assumed, times a permanent part that is a "
            "martingale. <bookmark mark='a'/> The eigenvector finds the transient part. What comes out is not P but "
            "P tilted by the permanent part: a long-run risk-adjusted measure, which turns out to be the measure "
            "that uses the longest bond as numeraire, as Ian Martin and Stephen Ross themselves showed in 2019, and "
            "Likuan Qin and Vadim Linetsky in general. <bookmark mark='c'/> So recovery is right exactly when there "
            "is no permanent part, and nothing in prices can tell you whether there is."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    def sweep(self, sw):
        s = np.asarray(sw["strengths"])
        g = axes([0, 1], [0, 0.08], x_length=6.8, y_length=4.2, xlabel=r"strength of the permanent component",
                 ylabel=r"largest error in recovered probabilities", xticks=[0, 0.5, 1.0], yticks=[0, 0.02, 0.04, 0.06, 0.08],
                 font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bd = band(ax, s, np.asarray(sw["err_lo"]), np.minimum(np.asarray(sw["err_hi"]), 0.08), ARB, 0.2)
        med = curve(ax, s, np.asarray(sw["err_med"]), ARB, stroke_width=3)
        one = curve(ax, s, np.asarray(sw["err_one"]), CALL, stroke_width=4)
        leg = legend([(CALL, r"the economy above"), (ARB, rf"{sw['n_econ']} random economies: median, 5--95\%")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"each economy: random states, persistence, risk aversion and discount rate; the permanent "
                          r"shock's strength turned up from zero", 4.6, 20, GREY_A),
            MathTex(rf"\text{{at zero: error }} < 10^{{-12}}", font_size=28, color=CALL),
            MathTex(rf"\text{{at full strength: median }} {sw['err_med'][-1]:.3f}", font_size=28, color=ARB),
            wrapped_label(r"the error grows smoothly with the strength of the permanent part, in every economy: there "
                          r"is no threshold below which recovery is safe", 4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulated economies, seeded")
        with self.voiceover(
            "How fast does it go wrong? Turn the permanent component up from zero, in the economy we just saw, and "
            f"in {sw['n_econ']} random economies with different persistence, risk aversion and discount rates. "
            "<bookmark mark='a'/> At zero, recovery is exact in every one. As the permanent part grows, the error "
            f"grows with it, smoothly, to a median of {sw['err_med'][-1]:.3f} at full strength, with no threshold "
            "below which it is safe."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(med), Create(one), FadeIn(side[1]), run_time=2.5)
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            history_card(2019, r"Jensen, Lando and Pedersen", r"generalized recovery: drop the time-homogeneous Markov "
                         r"chain, use many maturities at once", width=4.2, font_size=18),
            history_card(2020, r"Jackwerth and Menner", r"on S\&P 500 options, the recovered distributions fail to "
                         r"predict future returns and variances; simple benchmarks (historical, power utility) are "
                         r"not rejected", width=4.2, font_size=18),
            history_card(2025, r"Horvath", r"arbitrage-based recovery from one maturity's state prices; over 26 years "
                         r"of S\&P 500 options it predicts the monthly return distribution, despite a permanent "
                         r"component", width=4.2, font_size=18),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.4)
        foot = wrapped_label(r"the debate is open; the House uses option-implied densities as prices, never as "
                             r"forecasts", 11.0, 22, QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "And the evidence. Christian Skov Jensen, David Lando and Lasse Pedersen generalized recovery in 2019, "
            "using many maturities instead of a Markov chain. <bookmark mark='a'/> Jens Jackwerth and Marco Menner "
            "tested Ross recovery on S&P 500 options in 2020: the recovered distributions failed to predict future "
            "returns and variances, while simple benchmarks, the historical distribution or a power-utility investor, "
            "could not be rejected. <bookmark mark='b'/> On the other side, Ferenc Horvath's arbitrage-based recovery, "
            "published in 2025, reports that it predicts the monthly distribution of S&P 500 returns over twenty-six "
            "years even with a permanent component. <bookmark mark='c'/> The debate is open. The House reads "
            "option-implied densities as prices, never as forecasts."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Ross recovery applied to index options gives a pessimistic distribution. Is that evidence "
                        r"that investors are pessimistic?")
        with self.voiceover(
            "Pause and predict. Applied to index options, Ross recovery gives a gloomy distribution of future "
            "returns. Is that evidence that investors are pessimistic? <bookmark mark='a'/> No. A permanent "
            "component in the discount factor tilts the recovered measure toward bad states in exactly the same way. "
            "From prices alone, pessimism and a risk adjustment cannot be told apart."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"no: a permanent component in the discount factor produces the same "
                                                r"tilt; prices cannot separate beliefs from risk adjustment")))
        self.wait(0.4)
        self.clear_scene()
