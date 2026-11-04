from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, BOND_C, GOOD, HURDLE, PART, RP_C, SIXTY_C, SPY_C, fit_right, load

GCOL = {"equities": QC.SPOT, "bonds": QC.DELTA, "credit": QC.OPTION, "commodities": QC.P}


class RiskParity(VoiceoverScene):
    def construct(self):
        r = load("riskparity")
        self.card()
        self.sixty_forty()
        self.idea()
        self.firm()
        self.quadrants()
        self.weights(r)
        self.dial(r)
        self.results(r)
        self.financing()
        self.correlation(r)
        self.why_corr()
        self.question()

    def card(self):
        c = chapter_card(4, r"Risk parity and the stock--bond correlation", r"What if every asset class contributed the "
                         r"same risk?", part=PART)
        with self.voiceover("Chapter four. Part thirty met risk parity as an allocation rule on industries. Here it is "
                            "what it was invented to be: a way to hold whole asset classes, and a bet on how they move "
                            "together."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sixty_forty(self):
        rows = [cmath(r"w", r"=", r"(60\%\ \text{stocks},\ 40\%\ \text{bonds})", font_size=36),
                cmath(r"\sigma_S \approx 16\%,\ \sigma_B \approx 6\%", r":", r"\text{risk share of stocks} \approx "
                      r"\frac{0.6^2\cdot 0.16^2}{0.6^2\cdot 0.16^2 + 0.4^2\cdot 0.06^2} \approx 94\%", font_size=28,
                      colors={r"94\%": BAD}),
                cmath(r"\text{60/40}", r"\approx", r"\text{a stock portfolio with a bond cushion}", font_size=32)]
        whys = [why(r"the classic balanced portfolio, in dollars"),
                why(r"with uncorrelated stocks and intermediate Treasuries at typical volatilities, almost all of its "
                    r"risk is the stock market's"),
                why(r"so its return, and its crashes, are the stock market's; the bonds barely matter")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Start with the balanced portfolio. <bookmark mark='a'/> Sixty percent stocks, forty percent bonds, in "
            "dollars. <bookmark mark='b'/> Stocks are nearly three times as volatile as intermediate Treasuries, so in "
            "risk, the sixty-forty is about ninety-four percent stocks. <bookmark mark='c'/> It is a stock portfolio "
            "with a cushion. Diversified in dollars, concentrated in risk."
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

    def idea(self):
        rows = [cmath(r"w_i\,\sigma_i", r"=", r"\text{equal across classes}", font_size=38, colors={r"w_i\,\sigma_i": RP_C}),
                cmath(r"\sigma(w)", r"<", r"\sigma^*\ \Rightarrow\ \text{lever up}: L = \sigma^*/\sigma(w)", font_size=34),
                cmath(r"\text{why it can pay}", r":", r"\text{leverage-averse investors overpay for risky assets}",
                      font_size=30, colors={r"\text{why it can pay}": GOOD})]
        whys = [why(r"each asset class contributes the same risk (for uncorrelated classes; with correlations, the "
                    r"risk contributions of Part 30 are equalised)"),
                why(r"a portfolio of mostly bonds is calm, so reaching a stock-like volatility requires leverage"),
                why(r"Asness, Frazzini and Pedersen (2012): investors who cannot or will not borrow buy stocks for risk, "
                    r"so low-risk assets have higher risk-adjusted returns: Part 24's betting against beta, across "
                    r"asset classes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Risk parity turns it around. <bookmark mark='a'/> Give each asset class the same risk, not the same "
            "dollars. <bookmark mark='b'/> The result is mostly bonds, and calm; to reach the volatility investors want, "
            "lever it. <bookmark mark='c'/> Why might that pay? Cliff Asness, Andrea Frazzini and Lasse Pedersen argued "
            "that investors who cannot or will not borrow get their risk by buying stocks, bidding them up, so the safe "
            "assets offer more return per unit of risk: betting against beta, across asset classes."
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

    def firm(self):
        card = firm_card(r"Bridgewater's All Weather", r"launched in 1996 for Ray Dalio's own trust assets, as the firm "
                         r"describes it: a portfolio built to hold up across four economic environments, growth rising or "
                         r"falling and inflation rising or falling, by balancing risk across the assets that do well in "
                         r"each; later run for pension funds and endowments, and in 2025 offered as an ETF with State "
                         r"Street", source=r"Bridgewater, `The All Weather Story'; State Street Global Advisors (2025)",
                         kind=r"Firm file", width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The firm file. Bridgewater launched All Weather in 1996 for Ray Dalio's own trust, as the firm tells it, "
            "to hold up in any of four economic environments: growth rising or falling, inflation rising or falling. "
            "Each environment has assets that do well in it, and the portfolio balances risk across them. It later took "
            "money from pension funds and endowments, and in 2025 it was offered to the public as an exchange-traded "
            "fund with State Street. Its weakness is the environment it was least built for: inflation rising while "
            "growth falls."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def weights(self, r):
        gw, rs = r["group_gross"], r["risk_share"]
        keys = ["equities", "bonds", "credit", "commodities"]
        tot = sum(gw.values())
        bw = 9.0
        x0 = -4.5
        dol, risk = VGroup(), VGroup()
        for k in keys:
            dol.add(Rectangle(width=bw * gw[k] / tot, height=0.6, fill_color=GCOL[k], fill_opacity=0.85, stroke_width=0))
            risk.add(Rectangle(width=bw * rs[k], height=0.6, fill_color=GCOL[k], fill_opacity=0.85, stroke_width=0))
        dol.arrange(RIGHT, buff=0).move_to([0, 1.0, 0])
        risk.arrange(RIGHT, buff=0).move_to([0, -0.8, 0])
        dl = label(rf"dollars: {tot:.2f} of gross exposure per dollar of capital, on average", font_size=19,
                   color=GREY_A).next_to(dol, UP, buff=0.2)
        rl = label(r"risk contributions, on average", font_size=19, color=GREY_A).next_to(risk, UP, buff=0.2)
        leg = legend([(GCOL[k], k) for k in keys], font_size=16).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.9)
        foot = wrapped_label(r"10 ETFs: inverse-volatility weights within each class, equal risk across classes, levered to "
                             r"10\% on the trailing year's covariance, capped at 4, rebalanced monthly, 2007--2020",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The House's version, on ten of the funds. <bookmark mark='a'/> In dollars it is mostly bonds and credit: "
            f"{tot:.1f} dollars of exposure for each dollar of capital. <bookmark mark='b'/> In risk it is roughly "
            f"balanced, though not exactly: credit carried {100 * rs['credit']:.0f} percent, because high-yield and "
            "corporate bonds turned out to move with stocks."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in dol], lag_ratio=0.2), FadeIn(dl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in risk], lag_ratio=0.2), FadeIn(rl))
        self.wait(0.4)
        self.clear_scene()

    def dial(self, r):
        d = np.asarray(r["lev_path"]["dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        lev = np.asarray(r["lev_path"]["lev"], float)
        g = axes([x[0], x[-1]], [0, 4], x_length=7.6, y_length=4.2, xlabel=r"2007--2020",
                 ylabel=r"gross exposure per dollar", xticks=[2008, 2012, 2016, 2020], yticks=[0, 1, 2, 3, 4],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        one = DashedLine(ax.c2p(x[0], 1), ax.c2p(x[-1], 1), color=GREY_C, stroke_width=1.5)
        line = curve(ax, x, lev, RP_C, stroke_width=3)
        txt = wrapped_label(rf"from {r['lev_min']:.2f} in the volatility of 2009 to {r['lev_max']:.2f} when bonds were "
                            r"calm: leverage rises exactly when the assets look safest", 3.8, 17,
                            GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        fit_right(txt)
        with self.voiceover(
            "The leverage dial. <bookmark mark='a'/> It moves with volatility: down to "
            f"{r['lev_min']:.2f} in the turbulence after 2008, up to {r['lev_max']:.2f} when bonds were calm. "
            "<bookmark mark='b'/> Leverage rises exactly when the assets look safest, which is when a surprise in their "
            "correlation does the most damage."
        ) as vo:
            self.play(FadeIn(g), Create(one))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def results(self, r):
        hx = [-3.6, -0.8, 1.6, 3.8, 5.8]
        head = VGroup(label(r"book", font_size=18, color=GREY_B), label(r"Sharpe", font_size=18, color=GREY_B),
                      label(r"volatility", font_size=18, color=GREY_B), label(r"worst fall", font_size=18, color=GREY_B),
                      label(r"2008", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for nm, k, y8, col in ((r"risk parity", "rp", "rp", RP_C), (r"60/40", "sixty", "6040", SIXTY_C),
                               (r"US stocks", "spy", "spy", SPY_C)):
            s = r[k]
            tab.add(VGroup(label(nm, font_size=21, color=col), MathTex(f"{s['sharpe']:.2f}", font_size=26),
                           MathTex(rf"{100 * s['vol']:.1f}\%", font_size=26), MathTex(rf"{100 * s['maxdd']:.0f}\%", font_size=26),
                           MathTex(rf"{100 * r['y2008'][y8]:+.0f}\%", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        foot = wrapped_label(r"2007--2020, daily excess returns, before costs and the cost of borrowing beyond T-bills", 11.0,
                             17, GREY_A).to_edge(DOWN, buff=0.7)
        rp, sx = r["rp"], r["sixty"]
        with self.voiceover(
            "And the result, which is not what the brochure says. <bookmark mark='a'/> Over these fourteen years, risk "
            f"parity earned a Sharpe ratio of {rp['sharpe']:.2f}, below sixty-forty's {sx['sharpe']:.2f}. Its volatility "
            f"came in at {100 * rp['vol']:.1f} percent against a ten percent target, and its worst fall was "
            f"{abs(100 * rp['maxdd']):.0f} percent. <bookmark mark='b'/> In 2008 the levered credit lost with stocks. And "
            "sixty-forty had the best possible partner in these years: Treasuries that rallied every time stocks fell."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Indicate(tab[1][4], color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def correlation(self, r):
        sb = r["sb"]
        md = np.asarray(sb["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        rc = np.asarray(sb["rc36"], float)
        ok = np.isfinite(rc)
        g = axes([1962, 2021], [-0.8, 0.8], x_length=8.4, y_length=4.2, xlabel=r"1962--2020",
                 ylabel=r"correlation of stocks and 10-year Treasuries, 36 months", xticks=[1970, 1990, 2010],
                 yticks=[-0.6, 0, 0.6], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}", font_size=15)
        g.move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1962, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        line = curve(ax, x[ok], rc[ok], BOND_C, stroke_width=3)
        dec = sb["decades"]
        tags = VGroup(*[label(rf"{k}s: {v:+.2f}", font_size=15, color=GREY_A) for k, v in dec.items()])
        tags.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        fit_right(tags)
        foot = wrapped_label(r"Kenneth French's US market, and a constant-maturity 10-year Treasury built from FRED's daily "
                             r"yields (carry plus duration times the yield change); monthly returns", 11.6, 15,
                             GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "That partnership is younger than most investors think. <bookmark mark='a'/> Here is the correlation of "
            "American stocks with ten-year Treasuries over rolling three-year windows since 1962. "
            f"<bookmark mark='b'/> In the 1970s, 80s and 90s it was positive: about {dec['1970']:+.2f}, "
            f"{dec['1980']:+.2f} and {dec['1990']:+.2f} by decade. Bonds and stocks fell together. "
            f"<bookmark mark='c'/> Only after 2000 did it turn negative, {dec['2000']:+.2f} and then {dec['2010']:+.2f}. "
            "Every balanced and risk-parity backtest that starts after 2000 is built on that sign."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags[:4]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags[4:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def why_corr(self):
        cards = VGroup(
            desk_question(r"when inflation is the risk", r"news of higher inflation lowers both bond prices and the value "
                          r"of future profits: stocks and bonds fall together (the 1970s)", width=12.4, font_size=19),
            desk_question(r"when growth is the risk", r"bad news about growth lowers profits and rates, so bonds rally as "
                          r"stocks fall: Treasuries become a hedge (2000--2020)", width=12.4, font_size=19),
            desk_question(r"what the sign measures", r"Campbell, Sunderam and Viceira (2017): nominal bonds' beta moves "
                          r"with whether inflation is a good or a bad sign for the economy", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why does the sign change? <bookmark mark='a'/> When inflation is the main risk, news of higher inflation "
            "lowers both bond prices and the value of future profits, and the two fall together. "
            "<bookmark mark='b'/> When growth is the main risk, bad news lowers profits and interest rates at once, and "
            "bonds rally as stocks fall. <bookmark mark='c'/> John Campbell, Adi Sunderam and Luis Viceira showed that "
            "nominal bonds' beta moves with whether inflation is good or bad news for the economy. A risk-parity book "
            "is levered on that sign staying negative. The sealed years test it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def financing(self):
        rows = [cmath(r"r^{\text{RP}}", r"=", r"L\, r^{\text{unlevered}} - (L - 1)\,(r_f + s)", font_size=36,
                      colors={r"(L - 1)\,(r_f + s)": BAD}),
                cmath(r"SR^{\text{RP}}", r"=", r"SR^{\text{unlevered}} - \frac{(L - 1)\,s}{L\,\sigma^{\text{unlevered}}}",
                      font_size=34),
                cmath(r"L = 2,\ s = 0.5\%,\ \sigma = 5\%", r":", r"SR \text{ falls by } 0.05", font_size=32)]
        whys = [why(r"in excess-return terms the leverage costs the borrowing spread $s$ over bills on every borrowed "
                    r"dollar; futures embed a spread of their own"),
                why(r"so the levered book's Sharpe ratio is the unlevered one, less the spread per unit of levered risk"),
                why(r"small for cheap financing, large for an investor who borrows at retail rates: risk parity is an "
                    r"institutional strategy because the spread is")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Leverage is not free. <bookmark mark='a'/> Every borrowed dollar costs the bill rate plus a spread. "
            "<bookmark mark='b'/> So the levered book's Sharpe ratio is the unlevered one, less the spread cost per unit "
            "of risk. <bookmark mark='c'/> At twice leverage, a half-percent spread and five percent unlevered volatility, "
            "the Sharpe ratio falls by five hundredths. For an institution financing through futures, small; for an "
            "individual borrowing at retail rates, the whole edge."
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


    def quadrants(self):
        cells = VGroup()
        txt = [(r"growth rising", r"stocks, credit, commodities", QC.SPOT),
               (r"growth falling", r"nominal bonds", QC.DELTA),
               (r"inflation rising", r"inflation-linked bonds, commodities", QC.P),
               (r"inflation falling", r"stocks, nominal bonds", QC.REALIZED)]
        for k, (h, b, col) in enumerate(txt):
            box = RoundedRectangle(width=5.4, height=1.8, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.08)
            g = VGroup(box, VGroup(label(h, font_size=24, color=col), label(b, font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.15))
            g[1].move_to(box)
            cells.add(g)
        grid = VGroup(VGroup(cells[0], cells[1]).arrange(RIGHT, buff=0.3),
                      VGroup(cells[2], cells[3]).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.3).move_to(DOWN * 0.1)
        head = label(r"Four environments, a risk budget for each", font_size=30).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"as Bridgewater describes the idea; the assets are the usual examples, not its holdings", 11.0,
                             16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The four environments, as the firm describes them. <bookmark mark='a'/> When growth surprises upward, "
            "stocks, credit and commodities do well; when it surprises downward, nominal bonds. "
            "<bookmark mark='b'/> When inflation surprises upward, inflation-linked bonds and commodities; when it "
            "surprises downward, stocks and nominal bonds. Give each environment the same risk, and the portfolio "
            "should not depend on guessing which comes next. A risk-parity book with only stocks, bonds and credit "
            "covers the first two and is exposed to the third."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(grid[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid[1]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a risk-parity book is levered 2.5 times, mostly in bonds. Stocks fall 20\% and bonds 10\% in the "
                       r"same year. Roughly what does it lose?")
        with self.voiceover(
            "Pause and predict. A risk-parity book is levered two and a half times, mostly in bonds. In one year stocks "
            "fall twenty percent and bonds ten. Roughly what does the book lose?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
