from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, CALL, FWD, PART, Q_C


class Continuous(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorems()
        self.numeraire()

    def card(self):
        c = chapter_card(4, r"Continuous time, and changing numeraire", r"What does no free lunch mean with infinitely "
                         r"many trades?", lit=(1981,), part=PART)
        with self.voiceover("Chapter four. Continuous time, and changing numeraire."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorems(self):
        items = [
            (r"1979", r"Harrison and Kreps", r"finitely many states and dates: no arbitrage $\iff$ an equivalent "
                                             r"martingale measure; prices are expectations under it"),
            (r"1981", r"Harrison and Pliska", r"continuous trading: self-financing strategies as stochastic integrals "
                                              r"(Part 5); complete $\iff$ the measure is unique"),
            (r"1990", r"Dalang, Morton and Willinger", r"discrete time, any probability space: the theorem holds without "
                                                       r"finiteness"),
            (r"1994", r"Delbaen and Schachermayer", r"continuous time in general: ``no free lunch with vanishing risk'' "
                                                    r"$\iff$ an equivalent (local, then sigma-) martingale measure"),
        ]
        cards = VGroup(*[history_card(y, n, t, width=6.2, font_size=21) for y, n, t in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(UP * 0.4)
        if cards.width > 13.0:
            cards.scale_to_fit_width(13.0)
        foot = MathTex(r"\frac{S_t}{B_t} = \mathbb{E}^Q\!\left[\frac{S_T}{B_T}\,\Big|\,\mathcal{F}_t\right]", font_size=38,
                       color=Q_C).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The one-period theorem grew up in four steps. Michael Harrison and David Kreps, in 1979, proved it for "
            "finitely many states and dates: no arbitrage if and only if there is an equivalent martingale measure, "
            "and prices are expectations under it. <bookmark mark='a'/> Harrison and Stanley Pliska, in 1981, "
            "brought in continuous trading, with the stochastic integrals of Part five as trading gains, and showed "
            "that a market is complete exactly when the measure is unique. <bookmark mark='b'/> Robert Dalang, "
            "Andrew Morton and Walter Willinger removed the finiteness in discrete time in 1990. <bookmark mark='c'/> "
            "And in 1994 Freddy Delbaen and Walter Schachermayer found the right condition for continuous time, no "
            "free lunch with vanishing risk, and proved the general theorem. In every version the conclusion is the "
            "same: prices, divided by the bank account, are martingales under Q, the fair games of Part four."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def numeraire(self):
        rows = [cmath(r"\frac{V_0}{N_0}", r"=", r"\mathbb{E}^{Q^N}\!\left[\frac{V_T}{N_T}\right],\qquad "
                      r"\frac{dQ^N}{dQ} = \frac{N_T / N_0}{B_T / B_0}", font_size=34, colors={r"\frac{V_0}{N_0}": FWD}),
                cmath(r"V_0", r"=", r"P(0, T)\,\mathbb{E}^{T}[V_T]", font_size=36, colors={r"V_0": CALL}),
                cmath(r"\frac{C - P}{F}", r"=", r"1 - \frac{K}{F}\quad\text{(paid in bitcoin)}", font_size=34,
                      colors={r"\frac{C - P}{F}": Q_C})]
        whys = [why(r"any positive asset can be the unit of account; each has its own martingale measure (Geman, El "
                    r"Karoui and Rochet 1995)"),
                why(r"the zero-coupon bond as numeraire: the $T$-forward measure, under which forwards are martingales "
                    r"(Part 19); the annuity gives the swaption formula"),
                why(r"Deribit's options use bitcoin itself as the numeraire: prices in BTC are expectations under the "
                    r"bitcoin measure, which is why parity took this form in the hook")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "There is nothing special about the bank account. Any asset with a positive price can be the unit of "
            "account, the numeraire, and each one comes with its own martingale measure. Hélyette Geman, Nicole El "
            "Karoui and Jean-Charles Rochet made this a tool in 1995. <bookmark mark='a'/> Choose the zero-coupon "
            "bond maturing at T, and you get the T-forward measure, under which the price of anything paid at T is "
            "the bond price times an expectation, and forward prices are martingales. The rates parts use it, and "
            "the annuity numeraire for swaptions. <bookmark mark='b'/> And Deribit already does this. Its options "
            "are priced and paid in Bitcoin, so Bitcoin is the numeraire, and that is why parity in the hook read "
            "one minus K over F."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
