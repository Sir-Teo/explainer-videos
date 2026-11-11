from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (HURDLE, IMPACT_C, KERNEL_C, PART, PRICE_C, comma, fit_right, load)


class Prop(VoiceoverScene):
    def construct(self):
        p = load("propagator")
        self.card()
        self.model()
        self.response(p)
        self.fit_(p)
        self.through(p)
        self.pitfalls()
        self.balance(p)
        self.history_dep()
        self.hdim()
        self.question()

    def card(self):
        c = chapter_card(3, r"The propagator", r"If order signs are predictable, why are prices not?", part=PART)
        with self.voiceover('Chapter three. A linear transient-impact model can reconcile persistent order signs with diffusive returns by a decaying kernel, under explicit scaling assumptions. That is one possible mechanism rather than a unique inference about efficient prices. We will distinguish the observed response function from a finite fitted projection and its illustrative superposition.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"p_n", r"=", r"\textstyle\sum_{m<n} G(n - m)\,\varepsilon_m + \text{noise}", font_size=40,
                      colors={r"G(n - m)": KERNEL_C}),
                cmath(r"R(\ell)", r"=", r"\mathbb E[\varepsilon_n (p_{n+\ell} - p_n)]", font_size=38),
                cmath(r"C(\ell)", r"=", r"\mathbb E[\varepsilon_n \varepsilon_{n+\ell}] \sim \ell^{-\gamma}", font_size=38)]
        whys = [why(r"Bouchaud, Gefen, Potters and Wyart (2004): the price is the sum of every past trade's impact, as it "
                    r"stands now; $G$ is the propagator, in trade time"),
                why('signed response averaged over all starting trades; includes correlated later flow and news'),
                why('theoretical asymptotic sign correlation, $0<\\gamma<1$; finite-lag fits alone do not prove it')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> Price is represented by a convolution of earlier trade signs with a lag kernel, plus noise under specified stationarity and convergence assumptions. <bookmark mark='b'/> The response is an unconditional signed average over all starting trades, not simply the conditional move after a buy unless additional symmetry holds. It includes correlated later flow and news. <bookmark mark='c'/> A theoretical long-memory sign process has autocorrelation proportional to lag to minus gamma, with gamma between zero and one. A short fitted range does not establish that asymptotic law."
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

    def response(self, p):
        lags = np.log10(p["lags"])
        R = np.asarray(p["R"], float)
        g = axes([0, 3.5], [0, float(np.ceil(R.max() / 5) * 5)], x_length=6.4, y_length=4.4, xlabel=r"lag, trades",
                 ylabel=r"$R(\ell)$, ticks", xticks=[0, 1, 2, 3], xfmt=lambda v: f"10^{{{v:.0f}}}",
                 yticks=[0, float(np.ceil(R.max() / 5) * 5)], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_ = VGroup(curve(ax, lags, R, PRICE_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.06, color=PRICE_C)
                                                                   for a, b in zip(lags, R)])
        k = int(np.argmax(R))
        n_tr = f"{int(p['n']):,}"
        r_max = float(R.max())
        lag_max = p["lags"][k]
        with self.voiceover(
            f"""Measured on {n_tr} aggregate-trade records from four date files. The mid comes from a 100-millisecond quote grid: the code selects the second preceding grid index, clips at available boundaries, and concatenates days after removing overnight price jumps. <bookmark mark='a'/> The signed response reaches about {r_max:.0f} ticks at sampled lag {lag_max}. <bookmark mark='b'/> Later sampled values bend down. This is descriptive, with no robust uncertainty interval or causal intervention; stale snapshots, partial spans and joins can affect it."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def fit_(self, p):
        L = np.asarray(p["G_lags"], float)
        G = np.asarray(p["G"], float)
        ok = L >= 5
        x = np.log10(L[ok])
        y = np.asarray(G[ok])
        g = axes([0.5, 3.1], [0, 1.0], x_length=6.4, y_length=4.4, xlabel=r"lag, trades",
                 ylabel=r"$G(\ell)$, ticks", xticks=[1, 2, 3], xfmt=lambda v: f"10^{{{v:.0f}}}", yticks=[0, 0.5, 1.0],
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_ = curve(ax, x, y, KERNEL_C, stroke_width=3)
        st = VGroup(label(rf"peak {p['G_peak']:.2f} ticks at lag {p['G_peak_lag']}", font_size=18, color=KERNEL_C),
                    label(rf"decay $\ell^{{-\beta}}$, $\beta = {p['beta']:.2f}$", font_size=18, color=KERNEL_C),
                    label(rf"signs: $\gamma = {p['gamma']:.2f}$", font_size=18, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            f"""A finite linear projection. <bookmark mark='a'/> The unchanged code uses centered signs, a thousand-lag Toeplitz correlation system and cumulative coefficients. The inferred kernel peaks at {p['G_peak']:.2f} ticks at lag {p['G_peak_lag']}. This projection does not causally isolate one trade. <bookmark mark='b'/> A log regression over lags one hundred to one thousand, flooring kernel values at a small positive number, gives decay estimate {p['beta']:.2f}. Omitted state, finite truncation and regularity assumptions remain; no uncertainty interval or out-of-sample forecast is supplied."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def through(self, p):
        G = np.asarray(p["G"], float)
        lags = np.asarray(p["G_lags"], float)
        step_ = lags[1] - lags[0]
        n_on, n_tot = 120, 200                       # a metaorder of 120 steps of 5 trades, then 80 steps of silence
        imp = []
        for t in range(n_tot):
            s = np.arange(min(t, n_on - 1) + 1)
            k = np.minimum(((t - s) * step_ / step_).astype(int), len(G) - 1)
            imp.append(float(np.sum(G[k])))
        imp = np.asarray(imp) / max(imp)
        x = np.arange(n_tot) * step_
        g = axes([0, float(x[-1])], [0, 1.1], x_length=8.4, y_length=4.0, xlabel=r"trades since the metaorder began",
                 ylabel=r"impact, relative to its peak", xticks=[0, 300, 600, 900], yticks=[0, 0.5, 1], font_size=15)
        g.move_to(DOWN * 0.3)
        ax = g.ax
        c_ = curve(ax, x, imp, IMPACT_C, stroke_width=3)
        stop = DashedLine(ax.c2p(n_on * step_, 0), ax.c2p(n_on * step_, 1.1), color=GREY_B, stroke_width=1.5)
        end = float(imp[-1])
        with self.voiceover(
            f"""An illustrative superposition through the fitted kernel. Add one positive impulse every five trade-clock units for six hundred units, then stop. <bookmark mark='a'/> Summing shifted sampled kernels gives the displayed normalized path; its final value is about {100*end:.0f} percent of the peak. This is an algebraic counterfactual holding the fitted kernel and other flow fixed. It does not simulate an interacting parent order, measure executable fills or establish a universal post-trade fraction."""
        ) as vo:
            self.play(FadeIn(g), Create(stop))
            vo.wait_until("a")
            self.play(Create(c_), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def pitfalls(self):
        cards = VGroup(
            desk_question(r"what a trade is", r"Binance's aggregated trades merge fills of one taker at one price; a sweep "
                          r"becomes several consecutive records, which bends the shortest lags", width=12.4, font_size=19),
            desk_question(r"the clock", 'the second preceding 100-ms grid index is clipped at boundaries; many records share a stale snapshot', width=12.4,
                          font_size=19),
            desk_question(r"stationarity", r"four days, two of them a weekend: the propagator changes with volatility "
                          r"and time of day, so one curve is an average over regimes", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three limitations. <bookmark mark='a'/> Aggregate-trade records merge same-price taker fills; a multilevel sweep may produce several records. <bookmark mark='b'/> Several records can share a stale quote snapshot, and the lookup uses the second preceding grid index rather than a message-level pretrade quote. <bookmark mark='c'/> Four date files include a weekend, partial recorded spans and artificial event-time joins. One average fit can mix regimes, and it provides neither causal identification nor a robust confidence band."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def balance(self, p):
        rows = [cmath(r"G(\ell)", r"\sim", r"\ell^{-\beta}", font_size=40, colors={r"G(\ell)": KERNEL_C}),
                cmath(r"\text{Var}(p_n)", r"\sim", r"n^{\,2 - \gamma - 2\beta}", font_size=40),
                cmath(r"\beta", r"=", r"\frac{1 - \gamma}{2}", font_size=44, colors={r"\beta": HURDLE}),
                cmath(r"\text{Bitcoin}", r":", rf"\beta = {p['beta']:.2f},\quad \tfrac{{1 - \gamma}}{{2}} = "
                      rf"{p['beta_theory']:.2f}", font_size=34)]
        whys = [why(r"a decaying propagator, a power law in the lag"),
                why(r"summing correlated signs through a decaying kernel: the price's variance grows like this power of "
                    r"time"),
                why('under the stated long-memory scaling, exponent one gives linear variance growth; this does not alone imply a martingale'),
                why('finite-lag estimates, without uncertainty or an asymptotic efficiency test')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""The conditional scaling argument. <bookmark mark='a'/> Assume a stationary long-memory sign process with exponent gamma, a regular power-law propagator with beta, and a well-defined return construction. <bookmark mark='b'/> In the relevant scaling regime, the correlated-flow contribution has variance exponent two minus gamma minus two beta. <bookmark mark='c'/> Equating it to one gives beta equal to one minus gamma over two. Diffusive variance alone is weaker than a martingale or absence of predictability, and an additional noise term may matter. <bookmark mark='d'/> Our finite-lag estimates are {p['beta']:.2f} and {p['beta_theory']:.2f}. Their numerical proximity is not a statistical validation of asymptotic efficiency."""
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def history_dep(self):
        cards = VGroup(
            desk_question(r"impact depends on surprise", r"a buy that was expected, in a run of buys, moves the price less "
                          r"than a surprising one: the propagator is how a linear model says this (Lillo and Farmer)",
                          width=12.4, font_size=19),
            desk_question(r"a metaorder through the propagator", r"a constant stream of child orders, each decaying as "
                          r"$\ell^{-\beta}$, adds up to an impact that grows like $t^{1-\beta}$ while it runs, concave, "
                          r"and decays after it stops", width=12.4, font_size=19),
            desk_question(r"its limit", r"the linear propagator cannot produce the square root in size: that needs "
                          r"nonlinearity, as in the latent book (Chapter 2)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "What this model can say. <bookmark mark='a'/> Past correlated flow can be encoded through a lag kernel, while surprise models encode unexpected signs directly. <bookmark mark='b'/> For a regular power-law kernel with beta between zero and one, a fixed-rate stream has impact growing roughly as time to one minus beta in its scaling range. <bookmark mark='c'/> At fixed duration a linear convolution is linear in the stream's amplitude, so it cannot by itself produce a square root in size across amplitudes. Changing duration along with quantity can change the apparent exponent; the experimental comparison must hold the right variables fixed."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def hdim(self):
        rows = [cmath(r"\text{TIM}", r":", r"p_n = \textstyle\sum G(n - m)\,\varepsilon_m", font_size=38),
                cmath(r"\text{HDIM}", r":", r"r_n = \textstyle\sum \kappa(n - m)\,(\varepsilon_m - \hat\varepsilon_m)",
                      font_size=36, colors={r"\text{HDIM}": KERNEL_C}),
                cmath(r"\text{both}", r":", '\\text{model reconciliations; empirical identification remains separate}', font_size=32)]
        whys = [why(r"the transient impact model of this chapter: every trade's impact decays by a fixed kernel"),
                why(r"history-dependent impact: only the surprise in each sign moves the price, so expected trades cost "
                    r"little (Lillo and Farmer's asymmetric liquidity; Taranto et al. 2018)"),
                why(r"two descriptions of one fact; they differ in how impact depends on the state of the book, and in "
                    r"what they predict for a single trader's metaorder")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Two ways to say it. <bookmark mark='a'/> The transient impact model of this chapter: every trade's impact "
            "decays by a fixed kernel. <bookmark mark='b'/> Or history-dependent impact: only the surprise in each sign "
            "moves the price, so an expected trade costs little. Lillo and Farmer called it asymmetric liquidity: the "
            "side that is expected to be hit fills up. <bookmark mark='c'/> Both reconcile predictable flow with "
            "unpredictable prices; they differ in what they predict for a single trader's metaorder."
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

    def question(self):
        head = label('3. Conditional propagator scaling', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$C(\\ell)\\sim\\ell^{-0.6}$; flow variance exponent $2-\\gamma-2\\beta$.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Which $\\beta$ makes the flow contribution diffusive? Does that prove a martingale?', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause three. Assume sign exponent gamma equals point six and the flow variance scaling exponent is two minus gamma minus two beta. Find beta for linear variance growth, and explain why this alone does not prove unpredictable returns.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
