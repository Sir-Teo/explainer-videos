from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, HURDLE, MID_C, OFI_C, PART, comma, load)


class Events(VoiceoverScene):
    def construct(self):
        me = load("memory")
        self.card()
        self.hawkes(me)
        self.fit(me)
        self.critical()
        self.cluster()
        self.signs(me)
        self.split()
        self.signature_(me)
        self.pairs()
        self.question()

    def card(self):
        c = chapter_card(3, r"Events that cause events", r"Why do orders arrive in bursts, and why do their signs repeat?",
                         part=PART)
        with self.voiceover("Chapter three. Orders do not arrive like raindrops. They come in bursts, and buy orders "
                            "follow buy orders for minutes on end. Two facts, measured, and what they imply."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def hawkes(self, me):
        rows = [cmath(r"\lambda(t)", r"=", r"\mu + \textstyle\sum_{t_i < t} \alpha e^{-\beta (t - t_i)}", font_size=38,
                      colors={r"\lambda(t)": OFI_C}),
                cmath(r"n", r"=", r"\alpha/\beta\ \ \text{(the branching ratio)}", font_size=36),
                cmath(r"\text{mean rate}", r"=", r"\frac{\mu}{1 - n}", font_size=36)]
        whys = [why(r"Part 5's Hawkes process: every event raises the rate of further events, which then decays"),
                why(r"the expected number of events each event causes directly"),
                why(r"so a fraction $n$ of all events are caused by earlier events, and as $n \to 1$ the market runs on "
                    r"its own reactions")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Part five's Hawkes process, applied to trades. <bookmark mark='a'/> Every trade raises the rate of further "
            "trades, and the excess decays. <bookmark mark='b'/> The branching ratio n is the number of trades each trade "
            "causes directly. <bookmark mark='c'/> So the mean rate is the outside rate over one minus n, and a fraction n "
            "of all trades are reactions to earlier ones."
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

    def fit(self, me):
        h = me["hawkes"]
        dll = h["loglik"] - h["loglik_poisson"]
        rows = [cmath(r"\hat n", r"=", rf"{h['branching']:.2f}", font_size=40, colors={r"\hat n": OFI_C}),
                cmath(r"\Delta\log L", r"=", rf"{comma(dll)}\ \text{{over Poisson}}", font_size=34),
                cmath(r"\text{KS of rescaled gaps}", r"=", rf"{me['ks']:.3f}\ \ (\text{{Poisson: }}{me['ks_poisson']:.3f})",
                      font_size=30, colors={r"\text{KS of rescaled gaps}": BAD})]
        whys = [why(rf"one hour of BTCUSDT trades, {comma(me['n_events'])} arrivals, fitted by maximum likelihood with "
                    r"Part 5's code: about two thirds of trades are reactions"),
                why(r"the likelihood prefers self-excitation overwhelmingly"),
                why(r"but the rescaled waiting times are still not exponential: one exponential kernel cannot fit clustering "
                    r"on milliseconds and on minutes at once")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"One hour of Bitcoin's trades, {h['n']:,} of them. <bookmark mark='a'/> The fitted branching ratio is "
            f"{h['branching']:.2f}: about two thirds of trades are reactions to earlier trades. <bookmark mark='b'/> The "
            f"likelihood prefers self-excitation over a Poisson process by {dll:,.0f} log-points. "
            "<bookmark mark='c'/> But Part five's test, rescaling time by the fitted intensity, still fails: one decay rate "
            "cannot describe clustering on milliseconds and on minutes at once."
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

    def critical(self):
        cards = VGroup(
            desk_question(r"many time scales", r"with a power-law kernel spanning microseconds to hours, Hardiman, Bercot "
                          r"and Bouchaud (2013) estimated branching ratios close to one on index futures", width=12.4,
                          font_size=19),
            desk_question(r"near-criticality", r"a market where almost every order is a reaction to another: most activity "
                          r"is endogenous, and small shocks can cascade (Part 35's flash crash)", width=12.4, font_size=19),
            desk_question(r"and rough volatility", r"Part 14: nearly unstable Hawkes processes with power-law kernels "
                          r"produce, in the limit, exactly the rough volatility seen in daily data", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The deeper result. <bookmark mark='a'/> With a kernel that spans microseconds to hours, Stephen Hardiman, "
            "Nicolas Bercot and Jean-Philippe Bouchaud estimated branching ratios close to one on index futures. "
            "<bookmark mark='b'/> A market near criticality: almost every order is a reaction to another, and small shocks "
            "can cascade. <bookmark mark='c'/> And Part fourteen showed that exactly such nearly unstable Hawkes processes "
            "produce, in the limit, the rough volatility of daily prices. The microstructure explains the macro."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cluster(self):
        rows = [cmath(r"\lambda(t)", r"=", r"\mu + \textstyle\sum_{t_i < t} \alpha e^{-\beta (t - t_i)}", font_size=36),
                cmath(r"n", r"=", r"\alpha / \beta", font_size=40, colors={r"n": HURDLE}),
                cmath(r"\mathbb E[\text{cluster size}]", r"=", r"1 + n + n^2 + \cdots = \frac{1}{1 - n}", font_size=36),
                cmath(r"\bar\lambda", r"=", r"\frac{\mu}{1 - n}", font_size=40, colors={r"\bar\lambda": GOOD})]
        whys = [why(r"Hawkes (1971): every event raises the rate of future events, and the boost decays"),
                why(r"the branching ratio: the expected number of direct offspring of one event, the area under the "
                    r"kernel"),
                why(r"Hawkes and Oakes (1974): each background event starts a family tree of children, grandchildren "
                    r"and so on; the family is finite on average only if $n < 1$"),
                why(r"so the mean rate is the background rate times the mean family size; as $n \to 1$ nearly all events "
                    r"are caused by other events")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How to read a Hawkes process. <bookmark mark='a'/> Every event raises the rate of future events, and the "
            "boost decays. <bookmark mark='b'/> The branching ratio is the expected number of events one event triggers "
            "directly. <bookmark mark='c'/> Alan Hawkes and David Oakes saw the process as family trees: each background "
            "event has children, grandchildren and so on, and a family is finite on average only when the ratio is "
            "below one. <bookmark mark='d'/> So the mean rate is the background rate divided by one minus the ratio. Near "
            "one, almost every trade is a reaction to another trade."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def signs(self, me):
        lags = np.log10(np.asarray(me["lags"], float))
        acf = np.asarray(me["acf"], float)
        ok = acf > 0
        g = axes([0, 3.5], [-2.6, 0], x_length=7.0, y_length=4.4, xlabel=r"lag, trades ($\log_{10}$)",
                 ylabel=r"$\log_{10}$ autocorrelation of trade signs", xticks=[0, 1, 2, 3], yticks=[-2, -1, 0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, np.log10(b)), radius=0.07, color=OFI_C) for a, b in zip(lags[ok], acf[ok])])
        gm = me["gamma"]
        fit_ok = ok & (lags >= 1)
        b0 = float(np.mean(np.log10(acf[fit_ok]) + gm * lags[fit_ok]))
        line = Line(ax.c2p(1, b0 - gm), ax.c2p(3.4, b0 - 3.4 * gm), color=HURDLE, stroke_width=2)
        st = label(rf"slope $-\gamma = -{gm:.2f}$", font_size=18, color=HURDLE).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        with self.voiceover(
            "The second fact: signs repeat. <bookmark mark='a'/> The autocorrelation of trade signs, buy or sell, against "
            "the lag in trades, on logarithmic scales. <bookmark mark='b'/> A straight line: a power law with exponent "
            f"about {gm:.2f}. Fabrizio Lillo and Doyne Farmer found the same on the London Stock Exchange in 2004: a buy "
            "makes another buy more likely hundreds of trades later. A decay this slow means long memory."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def split(self):
        rows = [cmath(r"\text{metaorder}", r":", r"\text{a large order cut into many small ones}", font_size=32,
                      colors={r"\text{metaorder}": OFI_C}),
                cmath(r"\Pr(\text{size} > L)", r"\sim", r"L^{-\alpha}\ \Rightarrow\ C(\ell) \sim \ell^{-(\alpha - 1)}",
                      font_size=32),
                cmath(r"\text{efficiency}", r":", r"\text{signs predictable, prices not}", font_size=32,
                      colors={r"\text{efficiency}": HURDLE})]
        whys = [why(r"institutions slice their orders (Part 37), so the signs of child orders repeat"),
                why(r"Lillo, Mike and Farmer (2005): if metaorder sizes have a power-law tail, the sign autocorrelation "
                    r"decays as a power law, with an exponent set by the tail"),
                why(r"Part 35's puzzle: prices stay unpredictable because each trade's impact is smaller when its sign was "
                    r"expected; impact must be history-dependent")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why signs repeat. <bookmark mark='a'/> Institutions cut large orders into many small ones, so the child "
            "orders share a sign. <bookmark mark='b'/> If the sizes of those large orders have a power-law tail, the sign "
            "autocorrelation decays as a power law, with an exponent set by the tail: Lillo, Szabolcs Mike and Farmer's "
            "argument. <bookmark mark='c'/> And Part thirty-five's puzzle again: signs are predictable but prices are "
            "not, because a trade whose sign was expected moves the price less. Impact must depend on history."
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

    def signature_(self, me):
        steps = np.asarray(me["steps"], float)
        sig = np.asarray(me["signature"], float)
        x = np.log10(steps * 0.1)
        g = axes([-1.2, 2.0], [0.3, 0.46], x_length=7.0, y_length=4.4, xlabel=r"sampling interval, seconds ($\log_{10}$)",
                 ylabel=r"variance of mid changes per 100 ms, \$$^2$", xticks=[-1, 0, 1], yticks=[0.3, 0.38, 0.46],
                 xfmt=lambda v: f"{10 ** v:g}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, x, sig, MID_C, stroke_width=3)
        d1 = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=MID_C) for a, b in zip(x, sig)])
        rise = 100 * (sig.max() / sig[0] - 1)
        with self.voiceover(
            "And a third, which surprises. <bookmark mark='a'/> The signature plot: the variance of mid changes per unit "
            "of time, measured at different sampling intervals. For a random walk it is flat. For stock prices it usually "
            "falls at short intervals, because the bid-ask bounce adds noise. <bookmark mark='b'/> Here it rises, by "
            f"about {rise:.0f} percent from a tenth of a second to ten seconds. The mid's changes are positively "
            "correlated at the shortest scales."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(d1))
        self.wait(0.4)
        self.clear_scene()

    def pairs(self):
        rows = [cmath(r"\text{one-tick spread}", r":", r"\text{the offer empties} \Rightarrow \text{mid} + \tfrac12\text{tick}",
                      font_size=30),
                cmath(r"\text{then}", r":", r"\text{a new bid closes the gap} \Rightarrow \text{mid} + \tfrac12\text{tick}",
                      font_size=30),
                cmath(r"\text{mid moves}", r"\text{come in}", r"\text{same-direction pairs}", font_size=32,
                      colors={r"\text{same-direction pairs}": HURDLE})]
        whys = [why(r"when the best offer is exhausted, the spread opens to two ticks and the mid rises half a tick"),
                why(r"makers then post inside the gap, almost always on the side that just moved, and the mid rises again"),
                why(r"so a one-tick price move is two half-tick mid moves in the same direction, and the mid's changes are "
                    r"positively correlated: Chapter 7's simulator misses exactly this")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why. <bookmark mark='a'/> With a one-tick spread, when the best offer is exhausted the spread opens to two "
            "ticks and the mid rises half a tick. <bookmark mark='b'/> Then a maker posts a new bid inside the gap, and "
            "the mid rises half a tick again. <bookmark mark='c'/> So a one-tick move of the price is two half-tick moves "
            "of the mid, in the same direction. On Bitcoin a second cause adds to it: sweeps that take several levels "
            "arrive in bursts, this chapter's self-excitation, so successive jumps tend to continue. Mid prices trend at "
            "the finest scale while trade prices bounce: which one you sample decides what you see."
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
        q = pause_card(r"a Hawkes process has a background rate of 2 trades a second and a branching ratio of 0.68. What "
                       r"is its mean rate, and what if the branching ratio rises to 0.95?")
        with self.voiceover(
            "Pause and predict. A Hawkes process has a background rate of two trades a second and a branching ratio of "
            "point six eight. What is its mean rate? And if the branching ratio rises to point nine five?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
