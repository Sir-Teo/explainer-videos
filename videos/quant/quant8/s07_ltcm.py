from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import KELLY, OVER, PART, UNDER, illustration, load


class LTCM(VoiceoverScene):
    def construct(self):
        self.card()
        self.file()
        self.leverage(load("ltcm"))

    def card(self):
        c = chapter_card(6, r"Leverage beyond Kelly: LTCM, 1998", r"What happens when the volatility you sized for "
                         r"triples?", lit=(1998,), part=PART)
        with self.voiceover("Chapter six. Leverage beyond Kelly: Long-Term Capital Management, 1998."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self):
        card = crisis_card(
            r"17 August -- 23 September 1998", r"Long-Term Capital Management",
            r"A hedge fund founded in 1994 by John Meriwether, with Robert Merton and Myron Scholes among its partners, "
            r"ran convergence trades: long the cheap bond, short the dear one, levered many times. At the end of 1997 "
            r"it held \$129 billion of assets on \$4.7 billion of capital, and \$1.3 trillion of derivatives. After "
            r"Russia defaulted in August 1998, spreads widened instead of converging. By mid-September its capital was "
            r"under \$1 billion; on 23 September fourteen banks, brought together by the New York Fed, put in \$3.6 "
            r"billion and took it over.",
            stats=[(r"28 : 1", r"assets to capital, end of 1997"), (r"\$1.3\text{tn}", r"derivatives, notional"),
                   (r"< \$1\text{bn}", r"capital left, mid-September 1998")],
            width=11.0, font_size=25)
        card.move_to(ORIGIN)
        src = note(r"President's Working Group on Financial Markets, \textit{Hedge Funds, Leverage, and the Lessons of "
                   r"Long-Term Capital Management} (April 1999)", font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Long-Term Capital Management was founded in 1994 by the bond trader John Meriwether. Robert Merton, "
            "whose fraction we met in chapter three, and Myron Scholes were among its partners; both received the "
            "Nobel prize in 1997. The fund bought cheap bonds and sold similar dear ones, betting the spread between "
            "them would close: small, steady profits, levered many times. At the end of 1997 it held a hundred and "
            "twenty-nine billion dollars of assets on four point seven billion of capital, about twenty-eight to "
            "one, and derivatives with a notional value of one point three trillion. In August 1998 Russia "
            "defaulted, investors fled to safety, and the spreads widened instead of closing. By the middle of "
            "September the fund's capital was under a billion dollars. On the twenty-third, fourteen banks, brought "
            "together by the Federal Reserve Bank of New York, put in three point six billion and took it over."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def leverage(self, l_):
        L = np.asarray(l_["L"])
        gb, ga = np.asarray(l_["g_before"]), np.asarray(l_["g_after"])
        g = axes([0, 120], [-0.3, 0.6], x_length=6.4, y_length=4.4, xlabel=r"leverage (assets / capital)",
                 ylabel=r"growth of capital, a year", xticks=[0, 28, 50, 100], yticks=[-0.2, 0, 0.2, 0.4, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(120, 0), color=GREY_C, stroke_width=1.5)
        okb, oka = gb > -0.3, ga > -0.3
        lb = curve(ax, L[okb], gb[okb], UNDER, stroke_width=4)
        la = curve(ax, L[oka], ga[oka], OVER, stroke_width=4)
        mark = DashedLine(ax.c2p(28, -0.3), ax.c2p(28, 0.6), color=GREY_B, stroke_width=2)
        ml = label(r"28 : 1", font_size=20, color=GREY_B).next_to(ax.c2p(28, -0.27), RIGHT, buff=0.08)
        kb = Dot(ax.c2p(l_["kelly_before"], l_["kelly_before"] * l_["excess"] / 2), color=UNDER)
        ka = Dot(ax.c2p(l_["kelly_after"], l_["kelly_after"] * l_["excess"] / 2), color=OVER)
        side = VGroup(
            wrapped_label(r"a convergence trade, unlevered: earns 1\% a year with 1\% volatility", 4.4, 21, GREY_A),
            MathTex(rf"\text{{Kelly leverage}} = \frac{{\mu - r}}{{\sigma^2}} = {l_['kelly_before']:.0f}", font_size=30,
                    color=UNDER),
            MathTex(rf"\text{{volatility}} \times 3:\ \ \text{{Kelly}} = {l_['kelly_after']:.0f}", font_size=30, color=OVER),
            MathTex(rf"\text{{at }} 28:\ {100 * l_['g28_before']:+.0f}\% \ \to\ {100 * l_['g28_after']:+.0f}\%"
                    r"\text{ a year}", font_size=30),
            wrapped_label(r"Kelly leverage falls with the square of volatility: size by the calm, and a storm puts you "
                          r"far past twice Kelly. The full story, with funding and fire sales, is Part 41.", 4.4, 20,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"illustration: an assumed trade, not LTCM's books")
        with self.voiceover(
            "Kelly explains why this was so dangerous, with an illustration, not the fund's actual books. Take a "
            "convergence trade that earns one percent a year with one percent volatility. <bookmark mark='a'/> Its "
            "Kelly leverage is the excess return over the variance: a hundred to one. At twenty-eight to one the "
            "fund would be at a quarter of Kelly: cautious, by this measure. <bookmark mark='b'/> Now let the "
            "volatility triple, as calm spreads can in a crisis. Kelly leverage falls with the square of "
            "volatility, to eleven. The same twenty-eight to one is now two and a half times Kelly, and the growth "
            f"rate turns from {100 * l_['g28_before']:+.0f} percent a year to {100 * l_['g28_after']:.0f}. "
            "<bookmark mark='c'/> The lesson is the one from Part seven: sizing is only as good as the volatility "
            "forecast, and leverage sized in calm markets is far too high in a storm. Part forty-one tells the rest "
            "of the story: funding, margin calls, and fire sales."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(lb), FadeIn(side[0]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(kb), FadeIn(side[1]), Create(mark), FadeIn(ml))
            vo.wait_until("b")
            self.play(Create(la), FadeIn(ka), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
