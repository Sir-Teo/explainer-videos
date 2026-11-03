from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause, real_data


def yr(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


class ShortVol(VoiceoverScene):
    def construct(self):
        v = load("shortvol")
        self.card()
        self.books(v)
        self.cards()
        self.derive(v)

    def card(self):
        c = chapter_card(16, r"Crisis file: when short volatility blows up", r"Why doesn't everyone sell straddles?",
                         lit=(2018, 2020), part=PART)
        with self.voiceover("Chapter sixteen. A crisis file: when short volatility blows up."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def books(self, v):
        t = yr(v["dates"])
        lvl, vix = np.asarray(v["level"]), np.asarray(v["vix"])
        a, b = np.asarray(v["pnl near hedges"]), np.asarray(v["pnl deep hedges"])
        g1 = axes([2017, 2021], [0, 90], x_length=6.4, y_length=2.0, ylabel=r"VIX", yticks=[0, 40, 80],
                  font_size=15)
        g2 = axes([2017, 2021], [60, 160], x_length=6.4, y_length=1.6, ylabel=r"US stock market (French), start = 100",
                  yticks=[80, 120, 160], font_size=15)
        lo = min(a.min(), b.min()) - 2
        hi = max(a.max(), b.max()) + 2
        g3 = axes([2017, 2021], [lo, hi], x_length=6.4, y_length=2.2, ylabel=r"cumulative P\&L, per 100 of notional",
                  xticks=[2017, 2018, 2019, 2020, 2021], xfmt=lambda u: f"{int(u)}", yticks=[-20, 0, 10], font_size=15)
        VGroup(g2, g1, g3).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        tr = ValueTracker(0.0)
        sub = np.arange(0, len(t), 2)
        l1 = tracing(g1.ax, t[sub], np.clip(vix[sub], 0, 90), tr, THETA, stroke_width=2)
        l2 = tracing(g2.ax, t[sub], np.clip(lvl[sub], 60, 160), tr, SPOT, stroke_width=2)
        la = tracing(g3.ax, t[sub], a[sub], tr, VEGA, stroke_width=2.5)
        lb = tracing(g3.ax, t[sub], b[sub], tr, QC.LOSS, stroke_width=2.5)
        z = DashedLine(g3.ax.c2p(2017, 0), g3.ax.c2p(2021, 0), color=GREY_C, stroke_width=1)
        leg = legend([(VEGA, r"short a 3\%-OTM put, hedged with a put 17.5\% out"),
                      (QC.LOSS, r"the same, hedged with a put 40\% out")], font_size=16)
        leg.next_to(g3, RIGHT, buff=0.3).align_to(g3, DOWN)  # beside the P&L chart: below it is the frame's edge
        side = VGroup(
            label(r"before February 2020:", font_size=20, color=GREY_A),
            label(rf"near hedges {v['before near hedges']:+.1f}, deep hedges {v['before deep hedges']:+.1f}", font_size=20,
                  color=GREY_A),
            label(r"March 2020 drawdown:", font_size=20, color=GREY_A),
            label(rf"near {v['dd near hedges mar2020']:.1f}, deep {v['dd deep hedges mar2020']:.1f}", font_size=22,
                  color=QC.LOSS),
            label(rf"February 2018: near {v['dd near hedges feb2018']:.1f}, deep {v['dd deep hedges feb2018']:.1f}",
                  font_size=19, color=GREY_B),
            wrapped_label(r"illustrative: monthly rolls, Black--Scholes at the VIX plus a fixed skew; real books, with "
                          r"leverage, were many times larger", 4.4, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.35)
        src = real_data(r"French daily US market; FRED VIXCLS; 2017--2020", corner=UR)
        extra = v["before deep hedges"] - v["before near hedges"]
        worse = v["dd deep hedges mar2020"] - v["dd near hedges mar2020"]
        with self.voiceover(
            "Chapter six's premium is real, and here is what it pays for. Two illustrative books, run through 2017 to "
            "2020. Each sells a one-month put three percent below the market every month, and buys a hedge put further "
            "down: one at seventeen and a half percent out of the money, the other at forty. Both are marked every day "
            "at the VIX, with a fixed skew. <bookmark mark='a'/> In calm markets both earn; the cheaper, deeper hedge "
            "earns a little more. February 2018: the VIX doubles in a day. <bookmark mark='b'/> Then March 2020. The market falls by a third in a month and the VIX "
            f"passes eighty. Over three calm years the cheaper hedge had saved {extra:.1f} per hundred; in one month "
            f"its book lost {-worse:.1f} more than the other. <bookmark mark='c'/> In this illustration the deep-hedged "
            "book recovers afterwards, because a book still standing can sell expensive options. A fund that has "
            "been closed cannot."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), Create(z), FadeIn(leg), FadeIn(src))
            self.add(l1, l2, la, lb)
            i18 = int(np.searchsorted(t[sub], 2018.2))
            i20 = int(np.searchsorted(t[sub], 2020.35))
            self.play(tr.animate.set_value(i18), run_time=vo.until("a"), rate_func=linear)
            self.play(tr.animate.set_value(int(np.searchsorted(t[sub], 2020.1))), FadeIn(side[0]), FadeIn(side[1]),
                      FadeIn(side[4]), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(i20), FadeIn(side[2]), FadeIn(side[3]), run_time=vo.until("c"),
                      rate_func=linear)
            self.play(tr.animate.set_value(len(sub) - 1), FadeIn(side[5]), run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cards(self):
        c1 = crisis_card(
            r"February 2018", r"LJM",
            r"A firm running a short-volatility options strategy for its funds. The SEC's complaint of 27 May 2021 "
            r"says that a volatility spike in February 2018 caused losses of more than \$1 billion, over 80\% of the "
            r"funds' value, in two trading days, and alleges that investors and the funds' board were misled about "
            r"the strategy's risk. Allegations, which the defendants contested.",
            stats=[(r"> \$1\ \text{bn}", r"lost in two trading days"), (r"> 80\%", r"of the funds")], width=6.3,
            font_size=19)
        c2 = crisis_card(
            r"March 2020", r"Allianz Global Investors U.S.: Structured Alpha",
            r"Options funds that told investors they held hedges against a crash. They lost more than \$7 billion in "
            r"February and March 2020. In May 2022 the unit pleaded guilty to securities fraud; with its parent it "
            r"agreed to pay more than \$6 billion. The SEC said one risk report shrank a crash scenario's loss from "
            r"$-42.15\%$ to $-4.15\%$ by dropping a digit.",
            stats=[(r"> \$7\ \text{bn}", r"lost"), (r"\text{guilty plea}", r"May 2022")], width=6.3, font_size=19)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.2)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        src = note(r"SEC press release 2021-89 (LJM); SEC press release 2022-84 and the U.S. Attorney, S.D.N.Y., May "
                   r"2022 (Allianz Global Investors U.S.)", font_size=16, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Two real books. LJM ran short-volatility options strategies for its funds. According to the SEC's "
            "complaint of May 2021, the volatility spike of February 2018 cost them more than a billion dollars, over "
            "eighty percent of their value, in two trading days, and the SEC alleged that investors had been misled "
            "about the risk; the defendants contested it. <bookmark mark='a'/> Allianz Global Investors' Structured "
            "Alpha funds told investors they were hedged against a crash. In February and March 2020 they lost more "
            "than seven billion dollars. In May 2022 the American unit pleaded guilty to securities fraud, and with "
            "its parent agreed to pay more than six billion dollars. Prosecutors said the promised hedges were not "
            "bought, and the SEC said one risk report had turned a crash scenario's loss of forty-two percent into "
            "four, by dropping a single digit."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, v):
        rows = [
            cmath(r"d\Pi_{\text{short put}}", r"\approx", r"-\Delta\,dS - \tfrac12\Gamma\,dS^2 - \mathcal{V}\,d\sigma",
                  font_size=36),
            cmath(r"dS < 0,\ d\sigma > 0", r"\Rightarrow", r"\text{all three terms lose at once}", font_size=36),
            cmath(r"\text{loss}", r"\le", r"K_1 - K_2\quad \text{only if the hedge's strike } K_2 \text{ is near}",
                  font_size=34),
        ]
        whys = [why(r"chapter 1's Taylor series for a short put: long delta, short gamma, short vega"),
                why(r"in a crash the market falls, the move is large, and implied volatility jumps: every term has the "
                    r"same sign"),
                why(r"a put spread caps the loss at the strike gap, but a hedge far below lets the whole gap through: "
                    r"the hedge's moneyness is the risk")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.8, edge=6.9)
        pc = pause(rf"At VIX 15, per 100 of stock, a one-month put 20\% out costs {v['q_cost20']:.4f}, one 40\% out "
                   rf"under 0.00001. In a 35\% crash, at expiry, they pay {v['q_pay20']:.0f} and "
                   rf"{v['q_pay40']:.0f}. Which is cheap?", width=6.0, font_size=20)
        with self.voiceover(
            "Why do short-volatility books fail all at once? Chapter one's series for a short put: it is long delta, "
            "short gamma and short vega. <bookmark mark='a'/> In a crash the market falls, the move is large and "
            "implied volatility jumps, so all three terms lose together; nothing offsets. <bookmark mark='b'/> A put "
            "spread caps the loss at the gap between the strikes, but only if the hedge is close enough to matter. "
            "Move the hedge from twenty to forty percent out of the money and its price, which was already tiny, "
            "becomes nothing, and so does its payoff in a thirty-five percent crash. The premium of chapter six is "
            "paid for exactly the months the hedge was supposed to cover."
            " Next: who makes options markets for a living."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()
