from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause, real_data


class India(VoiceoverScene):
    def construct(self):
        sd = load("shortdated")
        self.card()
        self.boom()
        self.tickets(sd)
        self.theory(sd)

    def card(self):
        c = chapter_card(14, r"India's expiry-day boom, and what lottery tickets pay", r"Who wins when retail buys "
                         r"weekly options?", lit=(2024,), part=PART)
        with self.voiceover("Chapter fourteen. India's expiry-day boom, and what lottery tickets pay."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def boom(self):
        stats = VGroup(
            VGroup(MathTex(r"91\%", font_size=56, color=THETA),
                   wrapped_label(r"of individual traders in equity derivatives lost money in 2023--24 (SEBI study, "
                                 r"September 2024)", 3.4, 19, GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(MathTex(r"\text{Rs } 1.8\ \text{lakh crore}", font_size=40, color=THETA),
                   wrapped_label(r"their net losses over 2021--22 to 2023--24, about \$21 billion", 3.4, 19,
                                 GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(MathTex(r"\text{Rs } 1.06\ \text{lakh crore}", font_size=40, color=THETA),
                   wrapped_label(r"losses in 2024--25 alone, after the rules were tightened (SEBI, July 2025)", 3.4, 19,
                                 GREY_A)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(UP, buff=0.7)
        rules = VGroup(
            label(r"SEBI's circular of 1 October 2024, effective 20 November 2024:", font_size=22, color=GREY_A),
            label(r"$\cdot$ weekly expiries on one benchmark index per exchange (the Nifty 50, the Sensex)", font_size=21),
            label(r"$\cdot$ minimum contract size raised to Rs 15 lakh", font_size=21),
            label(r"$\cdot$ an extra 2\% margin on short options on expiry day", font_size=21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(stats, DOWN, buff=0.6)
        foot = wrapped_label(r"weekly options are cheap and short-dated: lottery tickets with expiry every few days, "
                             r"priced with Part 10's gamma at its most extreme", 11.0, 20, GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "India's National Stock Exchange has been the world's largest derivatives exchange by number of contracts "
            "traded for several years, most of them short-dated index options, many bought by individuals. In September 2024 India's regulator, SEBI, "
            "published what happened to them: ninety-one percent of individual traders in equity derivatives lost "
            "money in the year to March 2024, and their net losses over three years came to about one point eight "
            "lakh crore rupees, some twenty-one billion dollars. <bookmark mark='a'/> SEBI tightened the rules from "
            "November 2024: weekly expiries on only one index per exchange, larger contracts, and extra margin on "
            "expiry day. <bookmark mark='b'/> Losses the following year were still above one lakh crore rupees, and "
            "ninety-one percent still lost. Somebody is on the other side of those trades."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats[:2]], lag_ratio=0.5, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(rules), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tickets(self, sd):
        tk = np.asarray(sd["tickets"])
        o = sd["otm"]
        cells = VGroup()
        for prem, pay, m, cp in tk:
            cells.add(RoundedRectangle(width=0.62, height=0.4, corner_radius=0.05, stroke_color=YELLOW, stroke_width=1.5,
                                       fill_color=YELLOW, fill_opacity=0.25))
        cells.arrange_in_grid(rows=6, cols=10, buff=(0.1, 0.12)).to_edge(LEFT, buff=0.6).shift(UP * 0.2)
        flips = []
        for c, (prem, pay, m, cp) in zip(cells, tk):
            if pay <= 0:
                flips.append(c.animate.set_fill(GREY_D, 0.6).set_stroke(GREY_C))
            else:
                mult = pay / prem
                col = QC.GAIN if mult > 1 else ALT
                flips.append(c.animate.set_fill(col, 0.85).set_stroke(col))
        mults = VGroup(*[MathTex(rf"{pay / prem:.0f}\times" if pay / prem >= 10 else rf"{pay / prem:.1f}\times",
                                 font_size=16).move_to(c) for c, (prem, pay, m, cp) in zip(cells, tk) if pay > 0])
        paid, back = float(tk[:, 0].sum()), float(tk[:, 1].sum())
        bar_g = axes([0, 2], [0, max(paid, back) * 1.15], x_length=2.6, y_length=2.6, ylabel=r"dollars",
                     yticks=[], font_size=15).next_to(cells, DOWN, buff=0.5).align_to(cells, LEFT)
        b1 = Rectangle(width=0.8, height=bar_g.ax.c2p(0, paid)[1] - bar_g.ax.c2p(0, 0)[1], stroke_width=0,
                       fill_color=YELLOW, fill_opacity=0.8).move_to(bar_g.ax.c2p(0.5, 0), aligned_edge=DOWN)
        b2 = Rectangle(width=0.8, height=max(bar_g.ax.c2p(0, back)[1] - bar_g.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                       fill_color=QC.GAIN, fill_opacity=0.8).move_to(bar_g.ax.c2p(1.5, 0), aligned_edge=DOWN)
        bl = VGroup(label(r"paid", font_size=16, color=YELLOW).next_to(b1, DOWN, buff=0.05),
                    label(r"paid back", font_size=16, color=QC.GAIN).next_to(bar_g.ax.c2p(1.5, 0), DOWN, buff=0.05))
        side = VGroup(
            label(rf"{o['n_buy']:,} out-of-the-money options bought".replace(",", "{,}"), font_size=21, color=GREY_A),
            label(r"by takers, expiring within two days:", font_size=21, color=GREY_A),
            label(rf"{100 * o['worthless']:.0f}\% expired worthless", font_size=22, color=GREY_B),
            label(rf"{100 * o['profitable']:.0f}\% paid more than their price", font_size=22, color=QC.GAIN),
            label(rf"buyers got back {100 * (1 + o['ret_buy']):.0f} cents per dollar", font_size=22, color=QC.LOSS),
            wrapped_label(rf"what takers sold would have returned {100 * o['ret_sell']:+.0f}\% to its buyer: Deribit's "
                          r"takers are not India's retail, and this compares the instrument, not the people", 4.6, 17,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.35)
        src = real_data(r"Deribit BTC trades, 100 Wednesdays 2024--2025; settled at Binance's 08:00 price (a proxy for "
                        r"Deribit's 30-minute average); tickets: 4 June 2025")
        with self.voiceover(
            "What does a short-dated, out-of-the-money option pay its buyer? India's retail data is aggregated, so "
            "measure the instrument on another market. Here are sixty real tickets: out-of-the-money Bitcoin options "
            "bought on Deribit one morning, each expiring within two days. <bookmark mark='a'/> Expiry. Most turn "
            "grey: worthless. A few pay several times their price. <bookmark mark='b'/> Over a hundred Wednesdays, "
            f"{o['n_buy']:,} such tickets: {100 * o['worthless']:.0f} percent expired worthless, and "
            f"{100 * o['profitable']:.0f} percent paid back more than they cost. Weighted by premium, buyers got back "
            f"{100 * (1 + o['ret_buy']):.0f} cents per dollar. <bookmark mark='c'/> One caution: the takers who sold "
            "such options did no better as a group, and Deribit's takers are not India's retail. This compares the "
            "instrument, not the people."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02, run_time=2), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*flips, lag_ratio=0.03, run_time=3))
            self.play(FadeIn(mults))
            vo.wait_until("b")
            self.play(FadeIn(bar_g), GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(bl))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[:5]], lag_ratio=0.3, run_time=2.5))
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theory(self, sd):
        taus = np.asarray(sd["taus_h"])
        ex, ap = np.asarray(sd["ratio_exact"]), np.asarray(sd["ratio_approx"])
        rows = [
            cmath(r"\frac{\mathbb{E}^P[\text{payoff}]}{\text{price}}", r"=", r"\frac{C(\sigma_r)}{C(\sigma_i)}",
                  font_size=34),
            cmath(r"C(\sigma)", r"\approx", r"\frac{S\,(\sigma\sqrt\tau)^3}{k^2\sqrt{2\pi}}\,e^{-k^2/(2\sigma^2\tau)}",
                  font_size=34),
            cmath(r"\frac{C(\sigma_r)}{C(\sigma_i)}", r"\approx", r"\Big(\frac{\sigma_r}{\sigma_i}\Big)^3 \exp\!\Big(-"
                  r"\frac{k^2}{2\tau}\Big(\frac{1}{\sigma_r^2} - \frac{1}{\sigma_i^2}\Big)\Big)", font_size=34),
        ]
        whys = [why(r"with no drift, an option's expected payoff is the same formula at the volatility that is realized"),
                why(r"for a fixed out-of-the-money strike $k = \ln K/S$ and $\tau \to 0$: Mills' ratio on $N(-d)$, twice"),
                why(r"so when implied exceeds realized, the ratio collapses as expiry nears: short-dated options "
                    r"magnify the premium")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.6, buff=0.4, edge=6.9)
        g = axes([np.log10(taus.min()), np.log10(taus.max())], [0, 1], x_length=5.6, y_length=2.4,
                 xlabel=r"hours to expiry (log scale)", ylabel=r"expected payoff / price", xticks=[0, 1, 2],
                 xfmt=lambda u: f"{10 ** u:.0f}", yticks=[0, 0.5, 1], font_size=15).to_edge(DOWN, buff=0.4).to_edge(
            LEFT, buff=0.8)
        le = curve(g.ax, np.log10(taus), np.clip(ex, 0, 1), GAMMA, stroke_width=3)
        la = DashedVMobject(curve(g.ax, np.log10(taus), np.clip(ap, 0, 1), WHITE, stroke_width=2), num_dashes=40)
        leg = legend([(GAMMA, r"exact"), (WHITE, r"the approximation")], font_size=16).next_to(g, RIGHT, buff=0.3)
        cap = label(r"a call 5\% out of the money, implied 50\%, realized 45\%", font_size=17, color=GREY_B).next_to(
            leg, DOWN, buff=0.2).align_to(leg, LEFT)
        pc = pause(r"Nine in ten lose. Does that prove the options were overpriced?", width=4.4, font_size=20,
                   corner=DR)
        with self.voiceover(
            "Why do short-dated options make the premium so stark? With no drift, an option's expected payoff is "
            "the Black-Scholes formula evaluated at the volatility that will be realized, while its price uses the "
            "implied one. <bookmark mark='a'/> For a strike a fixed distance out of the money, as expiry approaches, "
            "the price is dominated by an exponential, e to the minus k squared over two sigma squared tau. "
            "<bookmark mark='b'/> Take the ratio and the exponent is multiplied by one over tau: whenever implied is "
            "above realized, the expected payoff per dollar of premium collapses as expiry nears. For a call five "
            "percent out of the money, implied fifty and realized forty-five, a buyer gets back most of the premium "
            "with a month left, and almost none of it with a few hours left. The exact curve and the approximation "
            "agree. <bookmark mark='c'/> And pause and predict: nine in ten lose. Does that prove the options were "
            "overpriced? No: a fair lottery also loses most of the time. The premium-weighted return answers that "
            "question, and it was negative."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(g), Create(le), Create(la), FadeIn(leg), FadeIn(cap), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()
