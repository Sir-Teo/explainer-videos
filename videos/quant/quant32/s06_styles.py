from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, CARRY_C, GOOD, HURDLE, PART, SPY_C, TREND_C, fit_right, load

SCOL = {"Value": QC.SPOT, "Momentum": QC.VEGA, "Carry": QC.P, "Defensive": QC.REALIZED, "Multi-style": QC.HOUSE}


class Styles(VoiceoverScene):
    def construct(self):
        s = load("styles")
        self.card()
        self.definitions()
        self.carry()
        self.sharpes(s)
        self.paths(s)
        self.corr(s)
        self.defensive()
        self.crises(s)
        self.everywhere()
        self.caveats()
        self.question()

    def card(self):
        c = chapter_card(5, r"Value, momentum, carry and defensive, everywhere", r"Are the alternative premia one idea "
                         r"or four?", part=PART)
        with self.voiceover("Chapter five. Value, momentum, carry and defensive are signal families applied across "
                            "several asset classes. We examine AQR's published research series through 2020, "
                            "with reconstructed history and different underlying start dates. These are provider "
                            "portfolios, rather than an investable fund record or universal premia."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definitions(self):
        items = [(r"Value", r"cheap against a fundamental anchor: the five-year reversal of an index or a commodity, "
                            r"purchasing-power parity for a currency, the real yield of a bond", SCOL["Value"]),
                 (r"Momentum", r"the past year's relative winners against the losers, across markets in each class",
                  SCOL["Momentum"]),
                 (r"Carry", r"what a position earns if prices do not move: the interest differential, the roll-down, the "
                            r"futures basis, the dividend yield", SCOL["Carry"]),
                 (r"Defensive", r"low risk and high quality: the safer, steadier markets within each class, levered to "
                                r"the same risk", SCOL["Defensive"])]
        rows = VGroup()
        for nm, d, col in items:
            rows.add(VGroup(label(nm, font_size=24, color=col), wrapped_label(d, 10.0, 18, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.15)
        head = label(r"Four styles, applied across markets", font_size=30).to_edge(UP, buff=0.4)
        self.play(FadeIn(head), FadeIn(VGroup(*rows[:2])))
        with self.voiceover(
            "The four, as AQR's researchers apply them across asset classes. All are long-short within a class: they "
            "rank markets against each other. <bookmark mark='a'/> Value: buy what is cheap against an anchor, such as "
            "an index or commodity that has fallen for five years, or a currency below purchasing-power parity. "
            "Momentum: buy the past year's relative winners. <bookmark mark='b'/> Carry: buy what earns the most if "
            "prices stand still. Defensive: buy the safer, steadier markets, levered to the same risk."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(VGroup(*rows[:2]), scale_factor=1.01))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[2:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def carry(self):
        rows = [cmath(r"\frac{S_T-F_0}{F_0}", r"=", r"C_0+\frac{S_T-S_0}{F_0},\quad C_0=\frac{S_0-F_0}{F_0}",
                      font_size=32, colors={r"C_t": CARRY_C}),
                cmath(r"\text{currency}", r":", r"C \approx i^{*} - i", font_size=34),
                cmath(r"\text{bond}", r":", r"C \approx y - r_f + \text{roll-down}", font_size=34),
                cmath(r"\text{commodity}", r":", r"C=(S_0-F_0)/F_0\ \ \text{at unchanged spot}", font_size=32),
                cmath(r"\text{equity index}", r":", r"C \approx \text{dividend yield} - r_f", font_size=34)]
        whys = [why(r"terminal long-contract profit divided by positive $F_0$, with settlement at $S_T$; "
                    r"not a return on margin or a universal futures total return"),
                why(r"the foreign interest rate over the domestic one (Part 22's carry trade)"),
                why(r"the yield over the short rate, plus the gain as the bond rolls down the curve (Part 18)"),
                why(r"a positive unchanged-spot component can be outweighed by falling terminal spot"),
                why(r"the dividend yield over the financing rate")]
        step = ladder(self, rows, whys, keep=5, top=3.0, x=-0.3, buff=0.38, edge=6.9)
        with self.voiceover(
            "Carry is an unchanged-price component under a stated convention. Koijen and coauthors "
            "study it across asset classes. <bookmark mark='a'/> For one long contract held to "
            "settlement, divide terminal profit by its positive initial forward price. The displayed "
            "decomposition is exact; that denominator is not posted margin. "
            "<bookmark mark='b'/> Currency deposit carry is approximately the rate differential. "
            "<bookmark mark='c'/> Bond excess carry includes yield over funding and local roll-down. "
            "<bookmark mark='d'/> A commodity's positive spot-forward gap does not guarantee profit. "
            "<bookmark mark='e'/> Equity carry includes dividends against financing. These "
            "conventions define signals, without certifying expected net returns."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def sharpes(self, s):
        keys = ["Value", "Momentum", "Carry", "Defensive", "Multi-style"]
        st = s["styles"]
        mx = max(st[k]["sharpe"] for k in keys)
        bars = VGroup()
        for j, k in enumerate(keys):
            v = st[k]["sharpe"]
            r = Rectangle(width=7.0 * v / mx, height=0.55, fill_color=SCOL[k], fill_opacity=0.85, stroke_width=0)
            r.move_to([-1.8, 1.8 - 0.9 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(k, font_size=22, color=SCOL[k]).next_to(r, LEFT, buff=0.3).align_to([-2.1, 0, 0], RIGHT),
                            r, MathTex(f"{v:.2f}", font_size=26).next_to(r, RIGHT, buff=0.2)))
        head = label(r"Sharpe ratios, all asset classes, 1926--2020", font_size=28).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"AQR's Century of Factor Premia, as published: long--short style portfolios across equity "
                             r"indices, bonds, currencies and commodities, and stock selection; gross of fees and costs; "
                             r"1,134 months; arithmetic monthly mean / population SD, times sqrt(12); "
                             r"provider construction and missing-data conventions apply", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.35)
        ms = st["Multi-style"]
        self.play(FadeIn(head), FadeIn(foot), FadeIn(VGroup(*bars[:4])))
        with self.voiceover(
            "Ninety-five years of the four styles across asset classes, as AQR has published them. "
            "<bookmark mark='a'/> Each earns a Sharpe ratio between about a half and seven tenths. "
            f"<bookmark mark='b'/> The provider's multi-style series has Sharpe {ms['sharpe']:.2f} "
            f"and annualised volatility {100 * ms['vol']:.1f} percent under this calculation. "
            "Its construction is not established by simply averaging the four displayed series. "
            "Monthly standard deviations use the population divisor here; annualisation is a "
            "convention, rather than a claim of independent returns. Diversification helps "
            "explain the attraction, while provider methodology and costs still matter."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(VGroup(*bars[:4]), scale_factor=1.01))
            vo.wait_until("b")
            self.play(FadeIn(bars[4], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, s):
        d = np.asarray(s["dates"], float)
        x = d // 100 + ((d % 100) - 0.5) / 12
        keys = ["Value", "Momentum", "Carry", "Defensive"]
        ys = {k: 100 * np.asarray(s["cum"][k], float) for k in keys}
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 100) * 100)
        g = axes([1926, 2021], [-50, hi], x_length=7.6, y_length=4.4, xlabel=r"1926--2020",
                 ylabel=r"cumulative log return, \%", xticks=[1930, 1960, 1990, 2020], yticks=[0, hi / 2, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, x, ys[k], SCOL[k], stroke_width=2.5) for k in keys])
        leg = legend([(SCOL[k], k) for k in keys], font_size=16).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        fit_right(leg)
        txt = wrapped_label(r"cumulative log wealth, not percentage wealth growth; reconstructed history, "
                            r"changing coverage and zero-filled missing returns require care", 3.6, 15,
                            GREY_A).next_to(leg, DOWN, buff=0.5)
        fit_right(txt)
        with self.voiceover(
            "The paths use cumulative log wealth multiplied by one hundred. "
            "<bookmark mark='a'/> They rise over this research sample but have extended "
            "setbacks. A value of one hundred on this axis means wealth multiplied "
            "by e, not a one-hundred-percent total return. <bookmark mark='b'/> Underlying "
            "coverage changes: currency carry, for example, begins much later than 1926. "
            "The calculation fills missing returns with zero before log accumulation. "
            "That convention and reconstructed history limit comparisons of early and "
            "late periods. A long plotted span is not a single live mandate."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def corr(self, s):
        C = np.asarray(s["corr"], float)
        keys = s["keys"]
        n = len(keys)
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                v = C[i, j]
                col = interpolate_color(ManimColor(BLUE_D), ManimColor(RED_D), (v + 1) / 2)
                sq = Square(1.1, fill_color=col, fill_opacity=0.85 if i != j else 0.3, stroke_color=GREY_D, stroke_width=1)
                sq.move_to([-1.6 + 1.15 * j, 1.6 - 1.15 * i, 0])
                cells.add(VGroup(sq, MathTex(f"{v:+.2f}", font_size=24).move_to(sq)))
        rl = VGroup(*[label(k, font_size=18, color=SCOL[k]).next_to(cells[i * n][0], LEFT, buff=0.15) for i, k in
                      enumerate(keys)])
        cl = VGroup(*[label(k, font_size=16, color=SCOL[k]).next_to(cells[j][0], UP, buff=0.12) for j, k in
                      enumerate(keys)])
        grid = VGroup(cells, rl, cl).move_to(LEFT * 1.2 + DOWN * 0.1)
        vm = C[0, 1]
        rows = [cmath(r"SR_{\text{combo}}", r"\approx", r"\overline{SR}\sqrt{\frac{K}{1 + (K - 1)\bar\rho}}", font_size=30,
                      colors={r"SR_{\text{combo}}": GOOD})]
        f = rows[0].to_edge(RIGHT, buff=0.4).shift(DOWN * 2.6)
        fit_right(f)
        with self.voiceover(
            "The reason is the correlations. <bookmark mark='a'/> Value and momentum are negatively correlated, "
            f"{vm:+.2f} in the provider series. Contrasting signals suggest a mechanism but do "
            "not identify its cause. <bookmark mark='b'/> For equal-volatility, equal-Sharpe "
            "strategies with equal weights, the formula relates combined Sharpe to average "
            "pair correlation. Four with zero average correlation double individual Sharpe "
            "under those assumptions. The provider portfolio has its own construction. "
            "Correlations can change, and they do not describe joint tails."
        ) as vo:
            self.play(FadeIn(grid))
            vo.wait_until("a")
            self.play(Indicate(VGroup(cells[1], cells[n]), color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(f))
        self.wait(0.4)
        self.clear_scene()

    def crises(self, s):
        hx = [-2.6, 0.4, 3.4]
        head = VGroup(label(r"year", font_size=18, color=GREY_B), label(r"equity indices", font_size=18, color=SPY_C),
                      label(r"the multi-style book", font_size=18, color=QC.HOUSE))
        tab = VGroup(head)
        for c in s["crises"]:
            tab.add(VGroup(MathTex(str(c["year"]), font_size=26), MathTex(rf"{100 * c['mkt']:+.0f}\%", font_size=26,
                                                                          color=BAD),
                           MathTex(rf"{100 * c['styles']:+.1f}\%", font_size=26, color=GOOD if c["styles"] > 0 else BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.3 - 0.62 * j, 0])
        foot = wrapped_label(r"six worst years selected after observing AQR's equity-index series, 1926--2020; "
                             r"same-sample comparison, not a prespecified crisis test", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
        with self.voiceover(
            "And in the worst years for stocks. <bookmark mark='a'/> In the six worst calendar years for world equity "
            "indices since 1926, including 1931, 1974, 2002 and 2008, the combined styles were roughly flat or up. They "
            "were selected after seeing the equity series. In 2008 the multi-style result "
            "was slightly negative. This same-sample comparison does not establish protection "
            "within each crisis or guarantee future crisis performance."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def caveats(self):
        cards = VGroup(
            desk_question(r"a published backtest", r"built by a manager of these strategies, gross of fees and trading "
                          r"costs, with early decades reconstructed from thin data: a prior, not a track record",
                          width=12.4, font_size=19),
            desk_question(r"risk or mispricing?", r"carry is paid for crash risk: currency carry has sharply negative "
                          r"skewness (Brunnermeier, Nagel and Pedersen 2008); value and momentum have both stories",
                          width=12.4, font_size=19),
            desk_question(r"crowding again", r"as the styles became products, the investors in them came to share "
                          r"positions and margin: Part 31's August 2007, for multi-asset books", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.play(FadeIn(cards[0], shift=UP * 0.2))
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> This is a published backtest by a manager of these strategies, gross "
            "of fees and costs, with early decades reconstructed from thin data: a prior, not a track record. "
            "<bookmark mark='b'/> Some of the premia are pay for risk: currency carry crashes, as Markus Brunnermeier, "
            "Stefan Nagel and Lasse Pedersen documented. <bookmark mark='c'/> And as the styles became products, their "
            "investors came to share positions, which is the crowding of Part thirty-one, at the level of asset "
            "classes."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[0], scale_factor=1.01) if k == 0
                          else FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def everywhere(self):
        cards = VGroup(
            desk_question(r"value and momentum everywhere", r"Asness, Moskowitz and Pedersen (2013): in stocks, bonds, "
                          r"currencies and commodities, value and momentum earn premia, and value in one class is "
                          r"correlated with value in the others", width=12.4, font_size=19),
            desk_question(r"a common factor", r"the comovement across unrelated markets points to a common driver; they "
                          r"study links to funding liquidity; associations depend on the measure and timing",
                          width=12.4, font_size=19),
            desk_question(r"why that matters", r"a common factor is not diversifiable: the multi-style book's crisis "
                          r"behaviour depends on which way funding moves", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.play(FadeIn(cards[0], shift=UP * 0.2))
        with self.voiceover(
            "A striking fact sits under this table. <bookmark mark='a'/> Cliff Asness, Tobias Moskowitz and Lasse "
            "Pedersen found that value in stocks is correlated with value in bonds, currencies and commodities, and the "
            "same for momentum, across markets with nothing in common. <bookmark mark='b'/> They traced part of the "
            "comovement to measures of funding liquidity. This association does not force every "
            "funding shock to give the same payoff signs. <bookmark mark='c'/> A shared exposure "
            "can survive asset-class diversification; its impact depends on the exposure, "
            "horizon and shock. Correlation alone does not identify a structural cause."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[0], scale_factor=1.01) if k == 0
                          else FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def defensive(self):
        rows = [cmath(r"\text{defensive}", r"=", r"\text{long low-beta, high-quality markets, levered;}\ "
                      r"\text{short high-beta ones}", font_size=30, colors={r"\text{defensive}": SCOL["Defensive"]}),
                cmath(r"\text{BAB hypothesis}", r":", r"\text{constraints can flatten the risk--return relation}", font_size=30),
                cmath(r"\text{bonds}", r":", r"\text{short maturities, levered, against long maturities}", font_size=30)]
        whys = [why(r"the cross-asset version of Part 24's betting against beta: within each class, the safer markets, "
                    r"scaled up to the same risk"),
                why(r"Frazzini and Pedersen (2014): if investors cannot lever, the flat security market line pays those "
                    r"who can; realised funding shocks can still hurt a leveraged defensive portfolio"),
                why(r"in Treasuries, short bonds have earned more per unit of risk than long ones: the same pattern, along "
                    r"the curve")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The fourth style needs a word, because it is risk parity's cousin. <bookmark mark='a'/> Defensive buys the "
            "safer markets in each class, levered to the same risk, and sells the riskier ones. "
            "<bookmark mark='b'/> Andrea Frazzini and Lasse Pedersen's betting against beta explains it: investors who "
            "cannot lever bid up the risky assets, so the safe ones pay more per unit of risk to whoever can. "
            "<bookmark mark='c'/> The research also examines duration risk along the Treasury curve. "
            "The leverage-constraint hypothesis connects defensive investing and risk budgeting, "
            "but a long-short defensive factor and a long-only risk-parity portfolio have "
            "different exposures. Neither earns a guaranteed premium when funding tightens."
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
        panel = VGroup(
            MathTex('K=4,\\quad {\\rm SR}_j=0.6,\\quad \\sigma_j=\\sigma', font_size=34),
            MathTex('{\\rm SR}_{\\rm combo}=0.6\\sqrt{\\frac{4}{1+3\\bar\\rho}}', font_size=34),
            MathTex('\\bar\\rho\\in\\{0,0.3\\}', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"four styles, each with Sharpe 0.6, average correlation zero. What is the Sharpe ratio of their "
                       r"equal-risk combination? And with correlation 0.3?")
        with self.voiceover(
            "Pause and predict. Four styles, each with a Sharpe ratio of point six and an average correlation of zero. "
            "What does their equal-risk combination earn? And if the correlation were point three?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
