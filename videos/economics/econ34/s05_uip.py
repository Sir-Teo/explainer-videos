from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class UIP(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Interest parity and the carry trade", r"Should high interest rates mean a falling currency?",
             "Chapter four. Interest parity and the carry trade.", lit={1984: r"Fama"}, scale=("market", "world"),
             horizon=("a month", "a year"))
        self.parity()
        self.fama()
        self.carry()

    def parity(self):
        rows = VGroup(
            label(r"two ways to hold money for a year", font_size=26, color=E.ACCENT),
            MathTex(r"\underbrace{1 + i}_{\text{dollars}} \quad\text{vs}\quad \underbrace{(1 + i^{*})\,"
                    r"\frac{S_{t+1}}{S_t}}_{\text{pounds, then back to dollars}}", font_size=36, color=WHITE),
            label(r"covered parity: \ lock in $S_{t+1}$ with a forward contract: \ it holds, \ by arbitrage \ "
                  r"(nearly)", font_size=22, color=CALM),
            MathTex(r"\text{uncovered parity:}\quad E_t\!\left[\frac{S_{t+1} - S_t}{S_t}\right] \approx i - i^{*}",
                    font_size=34, color=USD),
            label(r"a currency with higher interest rates should be expected to fall by the gap", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Krugman, \ Obstfeld and Melitz, \ \emph{International Economics}, \ ch.\ 14", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Exchange rates are asset prices, so the next idea comes from finance. <bookmark mark='a'/> An investor "
            "with dollars for a year can hold dollars and earn the dollar interest rate, <bookmark mark='b'/> or "
            "change them into pounds, earn the British rate, and change back at whatever the exchange rate is next "
            "year. <bookmark mark='c'/> If the rate to change back is fixed today, with a forward contract, the two "
            "must pay the same, or there is free money; this covered parity holds closely, apart from strains in "
            "and since 2008. <bookmark mark='d'/> If it is not fixed, and investors care only about the expected "
            "return, the same logic gives uncovered parity: <bookmark mark='e'/> a currency paying a higher "
            "interest rate should be expected to fall, by just the gap, so that no one gains by chasing high "
            "rates."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def fama(self):
        U = load("uip")
        F = U["fama"]
        order = list(F)
        n = len(order)
        ax = plane([0.4, n + 0.6], [-3.2, 2.4], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[], yticks=[-3, -2, -1, 0, 1, 2], ylabel=r"slope of the currency's change on the rate gap",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        one = seg(ax, 0.4, 1, n + 0.6, 1, CALM, 2.0, dashed=True)
        zero = seg(ax, 0.4, 0, n + 0.6, 0, GREY_C, 1.2)
        dots, bars, nms = VGroup(), VGroup(), VGroup()
        for k, c in enumerate(order):
            b, se = F[c]["beta"], F[c]["se"]
            col = CRISIS if b < 0 else PRICE
            bars.add(Line(ax.ax.c2p(k + 1, max(-3.2, b - 2 * se)), ax.ax.c2p(k + 1, min(2.4, b + 2 * se)),
                          color=col, stroke_width=3, stroke_opacity=0.6))
            dots.add(Dot(ax.ax.c2p(k + 1, b), radius=0.08, color=col))
            nms.add(wrapped_label(tex_safe(U["names"][c]), 1.1, 13, GREY_A).next_to(ax.ax.c2p(k + 1, -3.2), DOWN,
                                                                                    buff=0.1))
        side = VGroup(
            label(r"teal dashes: \ uncovered \\ parity says 1", font_size=18, color=CALM),
            label(rf"{U['negative']} of {n} slopes \\ are below zero", font_size=19, color=CRISIS),
            label(r"high-rate currencies \\ tended to rise, \ not fall", font_size=19, color=WHITE),
            label(r"lines: \ $\pm$ 2 standard errors \\ (overlapping horizons)", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"FRED: \ H.10 rates, \ OECD 3-month rates, \ 1979--2026; \ this film's regressions", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Eugene Fama tested it in 1984. Regress the change in a currency's value over the next three months on "
            "the interest gap at the start. <bookmark mark='a'/> Uncovered parity says the slope is one. "
            "<bookmark mark='b'/> Here are the slopes for seven currencies against the dollar since 1979, recomputed "
            f"from the data. {U['negative']} of the {n} are below zero. <bookmark mark='c'/> High-interest "
            "currencies did not fall by the gap; on average they tended to rise. The bands are wide, because "
            "exchange rates are so noisy, but the pattern has been found in nearly every sample since: the forward "
            "premium puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(nms))
            vo.wait_until("a")
            self.play(Create(one), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(d)) for b, d in zip(bars, dots)],
                                  lag_ratio=0.2), FadeIn(side[1]), FadeIn(side[3]), run_time=2.2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def carry(self):
        U = load("uip")
        C = U["carry"]
        cum = np.array(U["carry_cum"])
        ax = plane([1985, 2027], [-0.2, 1.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[1985, 1995, 2005, 2015, 2025], yticks=[0, 0.5, 1.0, 1.5],
                   ylabel=r"the carry trade: \ cumulative excess return, \ log", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, U["carry_t"], cum, DEM, 3.0, smooth=False)
        crash = vline(ax, 2008.75, -0.2, 1.8, CRISIS, 2.0)
        side = VGroup(
            label(r"each month: \ hold the two \\ highest-yielding currencies, \\ borrow the two lowest", font_size=18,
                  color=WHITE),
            label(rf"{100 * C['mean']:.1f}\% a year, \\ s.d.\ {100 * C['sd']:.1f}\%: \\ Sharpe ratio {C['sharpe']:.2f}",
                  font_size=19, color=DEM),
            label(rf"worst month: \ {C['worst'][0]}, \\ {100 * C['worst'][1]:.1f}\%", font_size=19, color=CRISIS),
            label(r"up by the stairs, \\ down by the lift", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"FRED: \ H.10 and OECD rates; \ the dollar and seven currencies; \ this film", corner=DR,
                       font_size=12)
        with self.voiceover(
            "If high-rate currencies do not fall, there is money in borrowing where rates are low and lending where "
            "they are high: the carry trade. <bookmark mark='a'/> Each month, hold the two highest-yielding of "
            "these eight currencies, the dollar among them, and borrow the two lowest. <bookmark mark='b'/> Since "
            f"1985 this has earned {100 * C['mean']:.1f} percent a year above the cost of funds, with a Sharpe "
            f"ratio of {C['sharpe']:.2f}, about that of the stock market. <bookmark mark='c'/> But not smoothly. "
            f"Its worst month was {C['worst'][0][:4]}'s autumn, minus {abs(100 * C['worst'][1]):.0f} percent, when "
            "the yen, the cheapest currency to borrow, soared and the Australian and New Zealand dollars, the "
            "favourite targets, fell, as everyone closed the same trade at once. "
            "<bookmark mark='d'/> Traders say carry goes up by the stairs and down by the lift. Perhaps the "
            "return is simply pay for bearing crash risk, and parity holds once that is priced; that is one of the "
            "leading explanations of the puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(side[1]), run_time=2.2)
            vo.wait_until("c")
            self.play(Create(crash), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
