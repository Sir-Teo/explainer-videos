from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (HURDLE, KERNEL_C, PART, PRICE_C, comma, fit_right, load)


class Prop(VoiceoverScene):
    def construct(self):
        p = load("propagator")
        self.card()
        self.model()
        self.response(p)
        self.fit_(p)
        self.balance(p)
        self.history_dep()
        self.question()

    def card(self):
        c = chapter_card(3, r"The propagator", r"If order signs are predictable, why are prices not?", part=PART)
        with self.voiceover("Chapter three, and the answer to the pause: the impact of each trade must decay. Buy "
                            "orders follow buy orders for hundreds of trades. If each one moved the price permanently, "
                            "the price would trend, predictably. It does not, so each trade's impact must fade, just "
                            "fast enough to cancel the predictability of the signs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"p_n", r"=", r"\textstyle\sum_{m<n} G(n - m)\,\varepsilon_m + \text{noise}", font_size=40,
                      colors={r"G(n - m)": KERNEL_C}),
                cmath(r"R(\ell)", r"=", r"\mathbb E[\varepsilon_n (p_{n+\ell} - p_n)]", font_size=38),
                cmath(r"C(\ell)", r"=", r"\mathbb E[\varepsilon_n \varepsilon_{n+\ell}] \sim \ell^{-\gamma}", font_size=38)]
        whys = [why(r"Bouchaud, Gefen, Potters and Wyart (2004): the price is the sum of every past trade's impact, as it "
                    r"stands now; $G$ is the propagator, in trade time"),
                why(r"the response function: how far the price has moved $\ell$ trades after a buy, which mixes $G$ with "
                    r"the trades that followed"),
                why(r"the sign autocorrelation of Part 36, a power law with $\gamma < 1$: long memory")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> Jean-Philippe Bouchaud, Yuval Gefen, Marc Potters and Matthieu Wyart wrote "
            "the price as the sum of every past trade's impact as it stands now. G, the propagator, is how much of a "
            "trade's impact remains after a given number of trades. <bookmark mark='b'/> The response function, how far "
            "the price has moved l trades after a buy, mixes G with the trades that followed. <bookmark mark='c'/> And "
            "the sign autocorrelation is Part thirty-six's power law."
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
        with self.voiceover(
            f"Measured on Bitcoin's tape, {comma(p['n'])} trades over four days, with the mid just before each trade. "
            "<bookmark mark='a'/> After a buy the price rises for hundreds of trades, because more buys follow, and "
            f"peaks at about {R.max():.0f} ticks some {p['lags'][k]} trades later. <bookmark mark='b'/> Then it "
            "flattens and bends down slightly. It does not keep growing, even though the buys keep coming."
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
            "Now separate the two. <bookmark mark='a'/> Regress each price change on the signs of the past thousand "
            "trades, which undoes the sign correlation, and sum the coefficients. That is the propagator: the impact of "
            f"one trade, rising to {p['G_peak']:.2f} of a tick about {p['G_peak_lag']} trades later, as the book "
            "absorbs it, <bookmark mark='b'/> and then decaying, slowly, like a power of the lag with exponent "
            f"{p['beta']:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
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
                why(r"for the price to diffuse, neither trending nor reverting, the exponent must be one: the decay "
                    r"exactly balances the memory of signs (Bouchaud et al. 2004)"),
                why(r"the same order of magnitude; our fit decays a little faster, over only four days and with a "
                    r"100-ms grid")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The balance. <bookmark mark='a'/> If the propagator decays as a power of the lag, <bookmark mark='b'/> then "
            "summing the correlated signs through it makes the price's variance grow like a power of time. "
            "<bookmark mark='c'/> For prices to diffuse, neither trending nor reverting, the decay exponent must be one "
            "minus gamma, over two: the market's memory of signs and the fading of impact cancel exactly. "
            "<bookmark mark='d'/> On Bitcoin the fit gives "
            f"{p['beta']:.2f} against a prediction of {p['beta_theory']:.2f}: the same order, decaying a little faster, "
            "from four days on a coarse grid."
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
        with self.voiceover(
            "What the propagator says. <bookmark mark='a'/> A trade that was expected moves the price less than one that "
            "surprised: the propagator is the linear way to say so. <bookmark mark='b'/> Send a metaorder through it, a "
            "steady stream of child orders each decaying, and the impact grows concavely while it runs, then decays "
            "when it stops: the shape of Chapter one. <bookmark mark='c'/> But a linear propagator cannot make impact "
            "a square root of size. That needs the nonlinearity of the latent book."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"suppose impact were permanent for a while and then vanished completely. Could a trader buy and "
                       r"sell back, and make money from their own impact alone?")
        with self.voiceover(
            "Pause and predict. Suppose each trade's impact lasted for a while and then vanished completely. Could a "
            "trader buy, then sell back, and make money from their own impact alone?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
