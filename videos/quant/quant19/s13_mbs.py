from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, CONV, GOOD, PAR, PART, ZERO, ask, fit_right, illustration, load
from videos.quant.quant19.common import POLICY as POLICY_C

MONTHS = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def ymd(x):
    return f"{x % 100} {MONTHS[x // 100 % 100]} {x // 10000}"


class MBS(VoiceoverScene):
    def construct(self):
        m = load("mbs")
        self.card()
        self.history(m)
        self.prepay(m)
        self.price(m)
        self.oas(m)
        self.hedging(m)
        self.tba()
        self.fed(m)

    def card(self):
        c = chapter_card(12, r"Mortgages and negative convexity",
                         r"Why does a mortgage bond lose when rates move either way?", part=PART)
        with self.voiceover("Chapter twelve. Mortgages: the largest option in the bond market, and who is short it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self, m):
        t, v = np.asarray(m["t"]), np.asarray(m["rate"])
        g = axes([1971, 2026], [0, 20], x_length=8.6, y_length=4.4, xlabel=r"year",
                 ylabel=r"30-year fixed mortgage rate, \%", xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                 yticks=[0, 5, 10, 15, 20], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, PAR, stroke_width=2.4)
        hi, lo = m["high"], m["low"]
        dh, dl = Dot(ax.c2p(hi["t"], hi["v"]), color=BAD), Dot(ax.c2p(lo["t"], lo["v"]), color=GOOD)
        side = VGroup(
            MathTex(rf"{hi['v']:.2f}\%\ \ (\text{{{int(hi['t'])}}})", font_size=28, color=BAD),
            MathTex(rf"{lo['v']:.2f}\%\ \ (\text{{{int(lo['t'])}}})", font_size=28, color=GOOD),
            MathTex(rf"{m['end']:.2f}\%\ \ (\text{{end of 2025}})", font_size=28),
            wrapped_label(r"an American borrower can repay a fixed-rate mortgage at any time, without penalty: when "
                          r"rates fall, they refinance. Pooled by Ginnie Mae, Fannie Mae and Freddie Mac into "
                          r"guaranteed pass-through securities, those mortgages are the agency MBS market", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "The thirty-year fixed-rate mortgage, as Freddie Mac's weekly survey has recorded it since 1971: "
            f"{hi['v']:.1f} percent in {int(hi['t'])}, {lo['v']:.2f} percent at the start of {int(lo['t'])}, and "
            f"{m['end']:.2f} at the end of 2025. <bookmark mark='a'/> The American mortgage comes with an option: "
            "the borrower can repay at any time, with no penalty. When rates fall, they refinance. Pooled and "
            "guaranteed by Ginnie Mae, Fannie Mae and Freddie Mac, these loans become the agency mortgage-backed "
            "securities, one of the largest bond markets in the world, and their buyers are short that option."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2.5)
            self.play(FadeIn(dh), FadeIn(dl), FadeIn(side[:3]))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"FRED: MORTGAGE30US (Freddie Mac PMMS)"))
        self.wait(0.4)
        self.clear_scene()

    def prepay(self, m):
        inc, cpr = np.asarray(m["inc"]) * 1e4, np.asarray(m["cpr"]) * 100
        g = axes([-300, 300], [0, 50], x_length=7.4, y_length=4.4, xlabel=r"incentive: loan rate minus current rate, bp",
                 ylabel=r"prepayment, \% of balance a year (CPR)", xticks=[-300, -150, 0, 150, 300],
                 yticks=[0, 10, 20, 30, 40, 50], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, inc, cpr, CONV, stroke_width=3.5)
        side = VGroup(
            wrapped_label(r"left: moving house, divorce, default; a steady few percent a year that no rate can stop", 3.6,
                          18, GREY_A),
            wrapped_label(r"right: refinancing, once the saving covers the cost; it saturates, because some borrowers "
                          r"never refinance", 3.6, 18, GREY_A),
            wrapped_label(r"the S-curve here is stylised (the House's \texttt{cpr\_scurve}); desks fit theirs to pools' "
                          r"actual speeds, by loan age, size, region and servicer", 3.6, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "How fast does a pool pay off? The prepayment curve, against the refinancing incentive: the loan's rate "
            "minus today's. <bookmark mark='a'/> With no incentive, a steady few percent a year, from people moving "
            "house. <bookmark mark='b'/> Once the saving covers the cost of refinancing, prepayments climb steeply, "
            "and then saturate, because some borrowers never refinance at all. This curve is stylised; desks fit "
            "theirs to the speeds of real pools."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def price(self, m):
        s, mbs, tsy = np.asarray(m["shifts"]) * 1e4, np.asarray(m["mbs"]), np.asarray(m["tsy"])
        g = axes([-300, 300], [88, 114], x_length=7.6, y_length=4.6, xlabel=r"parallel move in rates, bp",
                 ylabel=r"price per 100", xticks=[-300, -150, 0, 150, 300], yticks=[90, 100, 110], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lt = curve(ax, s, tsy, ZERO, stroke_width=3, smooth=True)
        lm = curve(ax, s, mbs, CONV, stroke_width=3.5, smooth=True)
        gap = Polygon(*[ax.c2p(a, b) for a, b in zip(s, tsy)], *[ax.c2p(a, b) for a, b in zip(s[::-1], mbs[::-1])],
                      stroke_width=0, fill_color=BAD, fill_opacity=0.25)
        side = VGroup(
            legend([(CONV, r"6.5\% pass-through"), (ZERO, r"a bond with the same duration")], font_size=17),
            MathTex(rf"D = {m['duration']:.1f}\ \text{{years}}", font_size=30),
            MathTex(rf"\text{{convexity}} = {m['convexity']:.0f}", font_size=30, color=BAD),
            wrapped_label('rate declines can accelerate repayment and limit appreciation; rate increases can slow prepayment and extend life. The shaded gap compares curvature, not a matched option value. Stylized Vasicek-rate Monte Carlo, 300 paths per point', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"This is a stylized six-and-a-half-percent pass-through, simulated with the stated prepayment rule across parallel rate shifts. The comparison bond is matched to its local duration at the base point. <bookmark mark='a'/> The ordinary fixed-cash-flow bond is convex. <bookmark mark='b'/> This pool has effective convexity {m['convexity']:.0f} under the example's bump definition. Lower rates accelerate prepayment and limit price appreciation; higher rates slow repayment and can extend duration. The result depends on coupon, rate level, prepayment assumptions and the spread held fixed. <bookmark mark='c'/> The shaded gap illustrates different curvature. It is not a pure option price, because the comparison bond does not have identical cash flows with only the prepayment right removed. A genuine option-value comparison needs a matched counterfactual and consistent discounting."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(side[1]), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(gap), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def oas(self, m):
        o = m["oas"]
        rows = [cmath(r"\text{price}", r"=", r"\mathbb{E}^{\mathbb{Q}}\Big[\textstyle\sum_k \text{CF}_k\,"
                      r"e^{-\int_0^{t_k}(r_s + \text{OAS})\,ds}\Big]", font_size=38, colors={r"\text{price}": CONV}),
                cmath(r"\text{option cost}", r"=", r"\text{zero-vol spread} - \text{OAS}", font_size=38,
                      colors={r"\text{option cost}": BAD})]
        whys = [why(r"the option-adjusted spread: the constant spread over the model's rates, on every simulated "
                    r"path with its own prepayments, that matches the market price"),
                why(r"switch the volatility off and solve again: the zero-volatility spread. The difference is "
                    r"a model-dependent volatility adjustment in spread units")]
        step = ladder(self, rows, whys, keep=2, top=2.8, x=-1.0, buff=0.8, edge=6.9)
        bars = VGroup()
        vals = [(r"zero-vol spread", o["zvs"], PAR), (r"OAS", o["oas"], GOOD), (r"option cost", o["zvs"] - o["oas"], BAD)]
        for i, (n_, v_, c_) in enumerate(vals):
            r_ = Rectangle(width=v_ * 1e4 / 30, height=0.42, stroke_width=0, fill_color=c_, fill_opacity=0.8)
            r_.move_to([-5.0 + r_.width / 2, -1.2 - 0.62 * i, 0])
            bars.add(VGroup(r_, label(n_, font_size=19).next_to(r_, LEFT, buff=0.2).align_to([-5.2, 0, 0], RIGHT),
                            MathTex(rf"{1e4 * v_:.0f}\ \text{{bp}}", font_size=26).next_to(r_, RIGHT, buff=0.2)))
        for b_ in bars:
            b_[1].next_to([-5.1, b_[0].get_y(), 0], LEFT, buff=0.1)
        bars.shift(RIGHT * 1.6)
        foot = wrapped_label(rf"the 6.5\% pool at an assumed market price of {o['mkt']:.0f}; illustrative. Mortgage "
                             r"desks quote, trade and hedge on OAS, and the number is only as good as the prepayment "
                             r"model inside it", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"An option-adjusted spread is a model-dependent constant added to simulated discount rates to match a target price, while cash flows respond to rates and the assumed prepayment law. <bookmark mark='a'/> Solve a second spread with volatility set to zero. The deterministic run can still include refinancing and prepayment; it does not remove the borrower's option. <bookmark mark='b'/> For this synthetic pool and assumed price {o['mkt']:.0f}, the zero-volatility spread is {10000.0 * o['zvs']:.0f} basis points and the OAS is {10000.0 * o['oas']:.0f}. Their {10000.0 * (o['zvs'] - o['oas']):.0f}-basis-point difference is often called an option-cost spread. It is a model and convention dependent volatility adjustment in yield units, not a dollar option value or a guaranteed excess return. No market mortgage option surface was used to calibrate this toy example."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hedging(self, m):
        y = m["y2003"]
        steps = [r"rates rise", r"prepayments slow; MBS duration lengthens",
                 r"hedgers sell duration: pay fixed in swaps, sell Treasuries", r"rates rise further"]
        nodes = VGroup(*[RoundedRectangle(corner_radius=0.15, width=4.4, height=0.9, stroke_color=BAD, stroke_width=2,
                                          fill_opacity=0) for _ in steps])
        pos = [UP * 1.6, RIGHT * 3.4, DOWN * 1.6, LEFT * 3.4]
        for n_, p_, s_ in zip(nodes, pos, steps):
            n_.move_to(p_ + UP * 0.2)
            n_.add(wrapped_label(s_, 4.0, 19).move_to(n_))
        arrows = VGroup(*[CurvedArrow(nodes[i].get_center() + (pos[(i + 1) % 4] - pos[i]) * 0.28,
                                      nodes[(i + 1) % 4].get_center() - (pos[(i + 1) % 4] - pos[i]) * 0.28,
                                      angle=-PI / 4, color=GREY_B, stroke_width=3) for i in range(4)])
        foot = wrapped_label(
            rf"summer 2003: the 10-year Treasury yield went from {y['low']['v']:.2f}\% on {ymd(y['low']['date'])} to "
            rf"{y['high']['v']:.2f}\% on {ymd(y['high']['date'])}, a move widely attributed in part to mortgage "
            r"convexity hedging. Who hedges: servicers, the agencies' own portfolios, and mortgage REITs, which fund "
            r"agency MBS with repo and lose book value when rates move a lot either way", 12.4, 18,
            GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Negative convexity can transmit mortgage risk to other rates markets. <bookmark mark='a'/> Rising rates can slow prepayments and lengthen a mortgage pool. <bookmark mark='b'/> An investor maintaining a duration hedge may then sell Treasuries or pay fixed in swaps. <bookmark mark='c'/> If many investors do this together, their flows can amplify a move; the size and even the net direction depend on other investors and positions. This is a possible feedback mechanism, not a causal estimate from this chart. <bookmark mark='d'/> The ten-year Treasury yield moved from {y['low']['v']:.2f} to {y['high']['v']:.2f} percent during the displayed summer-2003 interval. Contemporary accounts discuss convexity hedging alongside other causes. Servicing rights have different cash flows and exposures, so not every mortgage-market participant is short the same option in the same way."
        ) as vo:
            self.play(FadeIn(nodes[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(arrows[i]), FadeIn(nodes[i + 1]))
            self.play(Create(arrows[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.add(illustration(r"FRED: DGS10; attribution per Federal Reserve and market commentary of the time",
                              corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def tba(self):
        def box(t, c_, w=3.2):
            r_ = RoundedRectangle(corner_radius=0.15, width=w, height=1.0, stroke_color=c_, stroke_width=2.5)
            return VGroup(r_, wrapped_label(t, w - 0.3, 19).move_to(r_))
        seller = box(r"seller: an originator, a dealer", PAR).move_to(LEFT * 4.6 + UP * 1.3)
        buyer = box(r"buyer: a fund, a bank, the Fed", GOOD).move_to(RIGHT * 4.6 + UP * 1.3)
        trade = box(r"trade today: issuer, coupon, maturity, price, face; not the pools", WHITE, 4.2).move_to(UP * 1.3)
        notice = box(r"two days before settlement: the seller names the pools", CONV, 4.2).move_to(DOWN * 0.4)
        ctd = box(r"delivery flexibility favors cheap eligible pools", BAD, 4.2).move_to(DOWN * 2.1)
        a1 = Arrow(seller.get_right(), trade.get_left(), buff=0.1, color=GREY_B)
        a2 = Arrow(trade.get_right(), buyer.get_left(), buff=0.1, color=GREY_B)
        a3 = Arrow(trade.get_bottom(), notice.get_top(), buff=0.1, color=GREY_B)
        a4 = Arrow(notice.get_bottom(), ctd.get_top(), buff=0.1, color=GREY_B)
        side = wrapped_label(r"dollar roll: sell this month's TBA, buy next month's back, lower; the gap (the drop) "
                             r"prices a month of the pool's carry, prepayments included. Pools with traits that slow "
                             r"prepayment (small loans, low-income areas) trade above TBA as specified pools", 4.2, 17,
                             GREY_A).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.3)
        fit_right(side)
        with self.voiceover(
            "The agency to-be-announced market uses standardized forward delivery, rather than an exchange-traded futures contract. The parties agree key security and settlement terms before particular pools are allocated. <bookmark mark='a'/> The seller gives pool information under the applicable forty-eight-hour notification calendar and good-delivery rules. <bookmark mark='b'/> Delivery flexibility creates an economic incentive to choose relatively cheap eligible collateral. A TBA quote also reflects financing, liquidity, expectations and delivery options; it is not a mathematical identity with the price of the worst individual pool. <bookmark mark='c'/> In a dollar roll, an investor sells for a nearer settlement and buys a similar exposure for later settlement. This changes entitlement to interim principal and interest and can change delivered pools, so it is not simply a repo loan. Specified pools can command pay-ups for desirable prepayment characteristics, conditional on coupon and market conditions."
        ) as vo:
            self.play(FadeIn(seller), FadeIn(buyer), FadeIn(trade), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            self.play(GrowArrow(a3), FadeIn(notice))
            vo.wait_until("b")
            self.play(GrowArrow(a4), FadeIn(ctd))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.add(illustration(r"SIFMA good-delivery guidelines: 48-hour notification", corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def fed(self, m):
        f = m["fed"]
        t, v = np.asarray(f["t"]), np.asarray(f["v"])
        g = axes([2009, 2026], [0, 3], x_length=8.0, y_length=4.2, xlabel=r"year",
                 ylabel=r"agency MBS held by the Fed, \$ trillion", xticks=[2010, 2014, 2018, 2022, 2026],
                 yticks=[0, 1, 2, 3], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, POLICY_C, stroke_width=3)
        pk = f["peak"]
        side = VGroup(
            MathTex(rf"\text{{peak}} = \${pk['v']:.2f}\ \text{{trillion}}", font_size=28, color=POLICY_C),
            label(ymd(pk["date"]), font_size=19, color=GREY_A),
            MathTex(rf"\text{{end of 2025}} = \${f['end']:.2f}\ \text{{trillion}}", font_size=26),
            wrapped_label(r"in quantitative easing the Federal Reserve bought agency MBS and did not hedge their "
                          r"convexity: a large holder that does not feed the loop. Since 2022 it has let them run off "
                          r"as borrowers repay, which, at today's rates, is slowly", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"The Federal Reserve's monetary-policy portfolio is a different holder from a duration-hedging dealer. Its agency MBS holdings reached about {pk['v']:.2f} trillion dollars in April 2022 in this weekly series. <bookmark mark='a'/> Subsequent runoff depends on principal payments and reinvestment policy, including scheduled amortization as well as prepayments. Holdings end this sample at {f['end']:.2f} trillion. When outstanding mortgage coupons are low relative to refinancing rates, refinancing slows and runoff can be gradual. This chart alone does not estimate a convexity effect or explain the mortgage-Treasury spread. Changes in the Fed's purchases, rate volatility, liquidity, guarantee costs and lender margins can all affect market spreads; the series does not isolate their contributions."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[3]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
        q = ask(r"an MBS investor delta-hedges every day and rates end the year where they began. Why can they still "
                r"have lost money?")
        with self.voiceover("An investor in mortgage bonds hedges duration every day, and rates end the year where they "
                            "began. Why can they still have lost money?"):
            self.play(FadeIn(q))
        self.add(illustration(r"FRED: WSHOMCB"))
        self.wait(0.5)
        self.clear_scene()

