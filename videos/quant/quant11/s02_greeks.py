from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import quoting as Q
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration

NAMES = ["straddle", "strangle", "risk reversal", "butterfly", "call spread", "calendar"]
BETS = {"straddle": r"a big move, either way; higher vol", "strangle": r"a bigger move, cheaper",
        "risk reversal": r"up, and the skew flattening", "butterfly": r"staying put; vol falling",
        "call spread": r"up, but not too far", "calendar": r"near-term calm, later vol"}


def pnl_tile(legs, size=0.15, lim=None):
    dS = np.linspace(-0.25, 0.25, 21)
    dv = np.linspace(-0.1, 0.1, 13)
    P = Q.pnl_surface(legs, 100.0, 0.5, dS, dv, 7 / 365)
    lim = lim or np.max(np.abs(P))
    g = VGroup()
    for i in range(len(dv)):
        for j in range(len(dS)):
            v = float(np.clip(P[i, j] / lim, -1, 1))
            col = interpolate_color(ManimColor(BACKGROUND), ManimColor(GAMMA if v > 0 else THETA), abs(v))
            g.add(Square(size, stroke_width=0, fill_color=col, fill_opacity=1).move_to([j * size, i * size, 0]))
    zero = VGroup(Line(g[len(dS) // 2].get_center() + DOWN * size, g[(len(dv) - 1) * len(dS) + len(dS) // 2].get_center()
                       + UP * size, color=GREY_C, stroke_width=1),
                  Line(g[(len(dv) // 2) * len(dS)].get_center() + LEFT * size,
                       g[(len(dv) // 2) * len(dS) + len(dS) - 1].get_center() + RIGHT * size, color=GREY_C, stroke_width=1))
    return VGroup(g, zero)


class Greeks(VoiceoverScene):
    def construct(self):
        self.card()
        self.second_order()
        self.strategies()

    def card(self):
        c = chapter_card(1, r"Positions as Greeks", r"What is each strategy a bet on?", part=PART)
        with self.voiceover("Chapter one. Positions as Greeks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def second_order(self):
        rows = [cmath(r"d\Pi", r"\approx", r"\Delta\,dS + \tfrac12\Gamma\,dS^2 + \Theta\,dt + \mathcal{V}\,d\sigma "
                      r"+ \text{vanna}\,dS\,d\sigma + \tfrac12\,\text{volga}\,d\sigma^2", font_size=32,
                      colors={r"d\Pi": OPT}),
                cmath(r"\text{vanna}", r"=", r"\frac{\partial \Delta}{\partial \sigma},\qquad \text{volga} = "
                      r"\frac{\partial \mathcal{V}}{\partial \sigma}", font_size=34, colors={r"\text{vanna}": VEGA})]
        whys = [why(r"a trader's book is a Taylor series: the first terms are what Part 10 hedged; the cross terms are "
                    r"where the smile lives"),
                why(r"vanna: delta moves when vol moves (the risk reversal's exposure); volga: vega moves when vol moves "
                    r"(the butterfly's); Part 12 prices the smile from them (Castagna and Mercurio 2007)")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "An options trader does not see a list of contracts. They see a Taylor series: how much the book makes "
            "for a move in the stock, the square of that move, the passing of a day, and a move in implied "
            "volatility. <bookmark mark='a'/> Two cross terms matter in practice. Vanna is how much delta changes "
            "when volatility moves; volga is how much vega changes. A risk reversal is mostly vanna, a butterfly "
            "mostly volga, and Part twelve will price the whole smile out of them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def strategies(self):
        st = Q.strategies(100.0, 30 / 365, 0.1)
        tiles = VGroup()
        for name in NAMES:
            t = pnl_tile(st[name])
            g = Q.book_greeks(st[name], 100.0, 0.5)
            cap = VGroup(label(name, font_size=22, color=WHITE),
                         label(BETS[name], font_size=17, color=GREY_A),
                         MathTex(rf"\Gamma {g['gamma']:+.3f}\ \ \mathcal{{V}} {g['vega'] / 100:+.2f}\ \ \Theta {g['theta'] / 365:+.2f}",
                                 font_size=20, color=GREY_B)).arrange(DOWN, buff=0.06)
            tiles.add(VGroup(t, cap).arrange(DOWN, buff=0.12))
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.6, 0.3)).move_to(DOWN * 0.2)
        if tiles.height > 6.6:
            tiles.scale_to_fit_height(6.6)
        key = VGroup(label(r"each square: P\&L after a week, across a spot move of $\pm 25\%$ (left to right) and a vol "
                           r"move of $\pm 10$ points (bottom to top)", font_size=18, color=GREY_B),
                     legend([(GAMMA, r"gain"), (THETA, r"loss")], font_size=17)).arrange(RIGHT, buff=0.5)
        key.to_edge(UP, buff=0.25)
        src = illustration(r"one-month options on a 100 underlying at 50\% vol; Greeks per unit (vega per vol point, "
                           r"theta per day)")
        with self.voiceover(
            "Here is what each standard structure is a bet on. Every square shows the P&L after a week, for spot moves "
            "left to right and implied-volatility moves bottom to top; green gains, red losses. <bookmark mark='a'/> "
            "The straddle and the strangle are long gamma and long vega: they want a big move, or rising volatility, "
            "and they lose quietly in the middle. <bookmark mark='b'/> The risk reversal is a directional bet with "
            "almost no vega: long the upside call, short the downside put. The butterfly is the opposite of the "
            "straddle: it wins if nothing happens. <bookmark mark='c'/> The call spread bets on a rise, but caps it. "
            "And the calendar, long the far month and short the near, bets that the near term stays calm while "
            "volatility further out holds up."
        ) as vo:
            self.play(FadeIn(key), FadeIn(src), FadeIn(tiles[0]), FadeIn(tiles[1]))
            vo.wait_until("a")
            self.play(Indicate(tiles[0][1][0]), Indicate(tiles[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(tiles[2]), FadeIn(tiles[3]))
            vo.wait_until("c")
            self.play(FadeIn(tiles[4]), FadeIn(tiles[5]))
        self.wait(0.4)
        self.clear_scene()
