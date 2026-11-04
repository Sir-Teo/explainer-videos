from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class Roll(VoiceoverScene):
    def construct(self):
        o = load("oil")
        self.card()
        self.decompose()
        self.mechanics()
        self.index(o)
        self.years(o)
        self.premium()
        self.optiver()

    def card(self):
        c = chapter_card(8, r"The roll and the commodity premium", r"What does holding futures pay?", lit=(2006,),
                         part=PART)
        with self.voiceover("Chapter eight. Rolling futures: what an investor in commodities actually earns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def decompose(self):
        rows = [cmath(r"\frac{F_{t+1,T} - F_{t,T}}{F_{t,T}}", r"\approx", r"\underbrace{\frac{S_{t+1} - S_t}{S_t}}_{"
                      r"\text{spot}} + \underbrace{\frac{F_{t+1,T} - S_{t+1}}{S_{t+1}} - \frac{F_{t,T} - S_t}{S_t}}_{"
                      r"\text{the curve rolls toward spot}}", font_size=30),
                cmath(r"\text{roll yield}", r"\approx", r"-\frac{1}{T_2 - T_1}\ln\frac{F_{T_2}}{F_{T_1}}", font_size=38,
                      colors={r"\text{roll yield}": BASIS})]
        whys = [why(r"a future converges to the spot price as it expires: a holder earns the spot's move plus the "
                    r"convergence, which is positive when the future started below spot"),
                why(r"so an investor who keeps buying the next contract and selling the expiring one earns the curve's "
                    r"slope: positive in backwardation, negative in contango, every month")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Nobody can hold oil for long without a tank, so investors hold futures instead, and futures expire. "
            "A future converges to the spot price as it nears delivery. So its return is the spot's move, plus the "
            "convergence. <bookmark mark='a'/> An investor who rolls, selling the expiring contract and buying the "
            "next, earns the slope of the curve on top of the spot: a positive roll yield in backwardation, a "
            "negative one in contango, month after month."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def mechanics(self):
        rows = [cmath(r"T_{\text{last}}", r"=", r"\text{the 25th of the month before delivery} - 3\ \text{business days}",
                      font_size=34, colors={r"T_{\text{last}}": BAD})]
        whys = [why(r"NYMEX's rule for WTI: the May 2020 contract stopped trading on 21 April 2020. An index holds "
                    r"the next contract, rolling early in each month (here on the fifth trading day), as the large "
                    r"commodity indices do, so it never holds a contract into its last days")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        box = VGroup(
            label(r"a fully collateralised futures index", font_size=24, color=OIL),
            wrapped_label(r"each day: the held contract's price change, divided by its price, plus (not shown) the "
                          r"interest on the cash that collateralises it. Built from the EIA's contract-1 and contract-2 "
                          r"settlements, re-labelled after each expiry", 11.0, 19, GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "To measure it, build the index an investor would hold. Crude futures stop trading three business days "
            "before the twenty-fifth of the month before delivery; the May 2020 contract's last day was the "
            "twenty-first of April. <bookmark mark='a'/> Hold the next contract, roll early each month, as the big "
            "commodity indices do, and record each day's price change as a fraction of the price: the return on a "
            "future fully backed by cash."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(box))
        self.wait(0.4)
        self.clear_scene()

    def index(self, o):
        t, idx, spot = np.asarray(o["t"]), np.asarray(o["index"]), np.asarray(o["spot"])
        g = axes([1986, 2025], [-0.6, 1.3], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"$\log_{10}$ growth of \$1",
                 xticks=[1990, 2000, 2010, 2020], yticks=[-0.5, 0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        ls = curve(ax, t, np.log10(np.maximum(spot, 1e-3)), OIL, stroke_width=2.2)
        li = curve(ax, t, np.log10(np.maximum(idx, 1e-3)), BASIS, stroke_width=2.6)
        side = VGroup(
            legend([(OIL, r"the front-month price"), (BASIS, r"the rolled futures index")], font_size=17),
            MathTex(rf"\text{{spot}}:\ {100 * o['cagr_spot']:.1f}\%\ \text{{a year}}", font_size=26, color=OIL),
            MathTex(rf"\text{{futures}}:\ {100 * o['cagr_index']:.1f}\%\ \text{{a year}}", font_size=26, color=BASIS),
            wrapped_label(r"1986 to April 2024, excess returns (before the interest on collateral). On balance the "
                          r"curve's contango cost the roller more than backwardation paid", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Thirty-eight years of WTI. <bookmark mark='a'/> The front-month price grew about "
            f"{100 * o['cagr_spot']:.0f} percent a year. <bookmark mark='b'/> The rolled futures index, what an "
            f"investor could actually own, grew {100 * o['cagr_index']:.1f}. The difference is the roll: in a market "
            "that sat in contango more often than not, every roll sold cheap and bought dear. For an investor, the "
            "price of oil and the return on oil are different things."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ls), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(li), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def years(self, o):
        ann = o["annual"][-14:]
        g = axes([-0.6, len(ann) - 0.4], [-60, 80], x_length=10.0, y_length=4.2, xlabel=r"", ylabel=r"\% in the year",
                 xticks=[], yticks=[-50, -25, 0, 25, 50, 75], font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(len(ann) - 0.4, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, a in enumerate(ann):
            grp = VGroup()
            for dx, v, c_ in ((-0.18, 100 * a["spot"], OIL), (0.18, 100 * a["futures"], BASIS)):
                v = float(np.clip(v, -60, 80))
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                grp.add(Rectangle(width=0.32, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=c_,
                                  fill_opacity=0.85).move_to([ax.c2p(i + dx, 0)[0], (y0 + y1) / 2, 0]))
            grp.add(label(str(a["y"]), font_size=14).next_to(ax.c2p(i, -60), DOWN, buff=0.08))
            bars.add(grp)
        leg = legend([(OIL, r"front-month price"), (BASIS, r"rolled futures")], font_size=17).to_corner(UR, buff=0.5)
        a20 = next(a for a in ann if a["y"] == 2020)
        with self.voiceover(
            "Year by year since 2010. <bookmark mark='a'/> In most years the two move together, the spot a little "
            "ahead in contango years and behind in backwardation. <bookmark mark='b'/> In 2020 the gap was "
            f"widest: the front-month price fell {abs(100 * a20['spot']):.0f} percent over the year, the rolled "
            f"futures {abs(100 * a20['futures']):.0f}, because the investor spent the spring rolling into a "
            "curve so steep that each new contract cost far more than the old one."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.1))
            vo.wait_until("b")
            k = [a["y"] for a in ann].index(2020)
            self.play(Indicate(bars[k], color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def premium(self):
        rows = [cmath(r"\mathbb{E}[F_{T,T}] - F_{t,T}", r"=", r"\mathbb{E}[S_T] - F_{t,T}\ \ (\text{the risk premium})",
                      font_size=36, colors={r"\mathbb{E}[F_{T,T}] - F_{t,T}": GOOD})]
        whys = [why(r"Keynes's normal backwardation (1930): producers hedge by selling futures, so speculators who buy "
                    r"them are paid to bear the risk; the future sits below the expected spot")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        cards = VGroup(
            desk_question(r"Gorton and Rouwenhorst (2006)", r"an equal-weighted index of commodity futures, 1959--2004: "
                          r"about the same excess return and Sharpe ratio as US stocks, with negative correlation to "
                          r"stocks and bonds, and positive to inflation", width=12.0, font_size=20),
            desk_question(r"and since", r"after 2004 index money poured in and many curves sat in contango; broad "
                          r"commodity indices returned far less. Our one commodity, WTI, earned 1.7\% a year in excess "
                          r"of cash since 1986", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Is there a premium for holding commodity futures at all? John Maynard Keynes thought so: producers sell "
            "futures to hedge, so the speculators who buy them must be paid, and futures sit below the expected spot "
            "price. <bookmark mark='a'/> In 2006 Gary Gorton and Geert Rouwenhorst found that an equal-weighted basket "
            "of commodity futures had matched stocks' excess return from 1959 to 2004, while moving against stocks "
            "and bonds and with inflation. <bookmark mark='b'/> Their paper helped send index money into commodities; "
            "the returns since have been far lower, and our one commodity earned under two percent a year over "
            "cash. A premium that becomes famous attracts the capital that shrinks it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def optiver(self):
        cc = crisis_card(r"March 2007", r"Optiver and the close",
                         r"the CFTC alleged that the trading firm made 19 attempts over 11 days to move NYMEX crude oil, "
                         r"heating oil and gasoline futures settlement prices by trading heavily into the close, "
                         r"'banging the close', to profit on positions priced at the settlement; settled in 2012 without "
                         r"admitting or denying the allegations",
                         stats=[(r"\$13\text{m} + \$1\text{m}", r"civil penalty and disgorgement (2012)"),
                                (r"19", r"alleged attempts in 11 days")], width=8.8, font_size=19).move_to(UP * 0.3)
        foot = wrapped_label(r"the roll and the settlement are where index money is most predictable; Part 34 returns to "
                             r"manipulation and surveillance", 11.0, 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Settlement prices matter: index rolls, and many contracts, are priced at them. In 2008 the Commodity "
            "Futures Trading Commission charged the trading firm Optiver with trying, nineteen times over eleven days "
            "in March 2007, to push crude, heating oil and gasoline settlement prices by trading heavily into the "
            "close. <bookmark mark='a'/> It settled in 2012 for a thirteen million dollar penalty and a million in "
            "disgorgement, without admitting or denying the charges. Where flows are predictable, someone will try "
            "to trade against them."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"CFTC press releases 5521-08 (July 2008) and 6239-12 (April 2012)"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"an oil fund holds the front-month future and the curve is in 5\% a month contango. If the spot price "
                r"stays flat for a year, roughly what does the fund lose?")
        with self.voiceover("An oil fund holds the front-month future, and the curve is in five percent a month "
                            "contango. If the spot price stays flat for a year, roughly what does the fund lose?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
