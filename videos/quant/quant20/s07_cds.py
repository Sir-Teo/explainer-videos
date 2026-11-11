from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import credit as CR
from videos.quant.quant20.common import (BAD, GOOD, HAZ, PART, RISKY, ask, comma, fit_right, house_lab, illustration, load,
                                         step_xy)


class CDS(VoiceoverScene):
    def construct(self):
        c = load("cds")
        self.card()
        self.contract()
        self.legs()
        self.bootstrap(c)
        self.risk(load("cdsrisk"))
        self.bigbang(c)
        self.auction()
        self.basis()
        self.feedback()

    def card(self):
        c = chapter_card(6, r"The credit default swap", r"What does insurance against default cost?", lit=(2008,),
                         part=PART)
        with self.voiceover("Chapter six. The credit default swap: insurance against a default, and the market built on "
                            "it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def contract(self):
        def box(t, c_, w=3.4):
            r_ = RoundedRectangle(corner_radius=0.15, width=w, height=1.1, stroke_color=c_, stroke_width=2.5)
            return VGroup(r_, wrapped_label(t, w - 0.3, 20).move_to(r_))
        buyer = box(r"protection buyer", GOOD).move_to(LEFT * 4.3 + UP * 0.8)
        seller = box(r"protection seller", BAD).move_to(RIGHT * 4.3 + UP * 0.8)
        ref = box(r"reference company: bonds and loans", GREY_B, 4.4).move_to(DOWN * 1.6)
        a1 = Arrow(buyer.get_right() + UP * 0.2, seller.get_left() + UP * 0.2, buff=0.1, color=GOOD)
        l1 = label(r"a spread $s$ a year, quarterly, until default or maturity", font_size=19).next_to(a1, UP, buff=0.1)
        a2 = Arrow(seller.get_left() + DOWN * 0.25, buyer.get_right() + DOWN * 0.25, buff=0.1, color=BAD)
        l2 = label(r"on default: face minus the auction's recovery", font_size=19).next_to(a2, DOWN, buff=0.1)
        dash = DashedLine(ref.get_top(), [0, -0.3, 0], color=GREY_B)
        foot = wrapped_label("a widely cited early modern CDS: J.P. Morgan's 1994 Exxon credit-line transaction with the EBRD. Earlier credit-risk transfers existed; owning the underlying bond is not required", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A credit default swap transfers specified credit-event risk under a contract. It resembles protection insurance economically, though its legal form and eligible events are defined by documentation. <bookmark mark='a'/> The buyer pays a contractual coupon, generally quarterly, plus any upfront payment. <bookmark mark='b'/> A qualifying credit event triggers the contractual settlement procedure, subject to deliverability and recovery-price rules. Counterparty failure can still impair payment. <bookmark mark='c'/> A widely cited early modern deal was J P Morgan's nineteen ninety-four transfer of an Exxon credit-line exposure. Credit-risk transfer existed earlier too. The protection buyer need not own the reference bonds, so a CDS can hedge an exposure or create a credit position."
        ) as vo:
            self.play(FadeIn(buyer), FadeIn(seller), FadeIn(ref), Create(dash))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def legs(self):
        rows = [cmath(r"\text{premium}", r"=", r"s\,\underbrace{\textstyle\sum_i \delta_i P(t_i) Q(t_i) + \text{accrued on "
                      r"default}}_{\text{RPV01}}", font_size=34, colors={r"\text{premium}": GOOD}),
                cmath(r"\text{protection}", r"=", r"(1 - R)\int_0^T P(t)\,(-dQ(t))", font_size=38,
                      colors={r"\text{protection}": BAD}),
                cmath(r"s_{\text{par}}", r"=", r"\frac{\text{protection}}{\text{RPV01}} \approx (1 - R)\,\lambda", font_size=40,
                      colors={r"s_{\text{par}}": RISKY})]
        whys = [why(r"the premium leg: each payment discounted, and paid only if the name has survived to that date"),
                why(r"the protection leg: the loss, paid at the moment of default, weighted by the chance of defaulting "
                    r"at each moment"),
                why(r"the par spread sets the two legs equal; with a flat hazard it is the continuous-premium credit triangle; quarterly pricing is approximate")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "For this simplified single-name pricer, discount factors are deterministic and survival probabilities are under the pricing measure, with fixed recovery and no counterparty default. The premium leg includes scheduled payments while alive and an approximation to accrual on default. <bookmark mark='a'/> The protection leg discounts the assumed loss payment at default and weights it by the default distribution. <bookmark mark='b'/> Their ratio gives the par spread. With continuous premiums, constant intensity and constant recovery it is exactly one minus recovery times intensity. Quarterly payments and accrued premium make the credit triangle an approximation to the implemented contract. Settlement delay and actual day-count conventions would also matter in production."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def bootstrap(self, c):
        ten = np.asarray(c["tenors"], float)
        sp = np.asarray(c["spreads"]) * 1e4
        hz = np.asarray(c["hazards"]) * 100
        Tq, Q = np.asarray(c["Tq"]), np.asarray(c["Q"])
        g1 = axes([0, 10.5], [0, 5], x_length=5.6, y_length=3.6, xlabel=r"years", ylabel=r"hazard, \% a year",
                  xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 1, 2, 3, 4, 5], font_size=13)
        g2 = axes([0, 10.5], [0.6, 1.0], x_length=5.6, y_length=3.6, xlabel=r"years", ylabel=r"survival $Q(t)$",
                  xticks=[0, 2, 4, 6, 8, 10], yticks=[0.6, 0.8, 1.0], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(DOWN * 0.6)
        xs, ys = step_xy(np.r_[0, ten], hz)
        hline = VMobject().set_points_as_corners([g1.ax.c2p(a, b) for a, b in zip(xs, ys)]).set_stroke(HAZ, 3.5)
        lq = curve(g2.ax, Tq, Q, HAZ, stroke_width=3.5)
        quotes = VGroup(*[MathTex(rf"{int(t)}\text{{y}}: {s_:.0f}", font_size=24) for t, s_ in zip(ten, sp)]).arrange(
            RIGHT, buff=0.45).to_edge(UP, buff=0.5)
        head = label(r"par spreads, bp (illustrative quotes); recovery 40\%, rates 4\%", font_size=19, color=GREY_A
                     ).next_to(quotes, DOWN, buff=0.15)
        foot = MathTex(rf"\text{{5-year RPV01}} = {c['rpv01_5']:.3f},\quad \lambda_{{\text{{triangle}}}} = "
                       rf"{100 * c['triangle_5']:.1f}\%", font_size=26).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The displayed par quotes are declared illustrations, not observed market quotes. Bootstrap a piecewise-constant pricing intensity while keeping discount and recovery conventions fixed. <bookmark mark='a'/> Solve the first interval from the first quote, then each later interval conditional on earlier ones, checking repricing and admissible nonnegative survival. <bookmark mark='b'/> A rising fitted intensity curve describes the risk-neutral model needed for these prices. It does not directly reveal the market's physical expectation of future defaults. Other instruments can be priced consistently within this convention, while recovery uncertainty, liquidity and model risk remain."
        ) as vo:
            self.play(FadeIn(quotes), FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(hline), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lq), FadeIn(foot), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def risk(self, r):
        sh, mtm = np.asarray(r["shifts_bp"]), np.asarray(r["mtm"]) / 1e6
        g = axes([-100, 300], [-1, 6.5], x_length=7.2, y_length=4.4, xlabel=r"change in the 5-year par spread, bp",
                 ylabel=r"protection buyer's gain, \$ million", xticks=[-100, 0, 100, 200, 300], yticks=[0, 2, 4, 6],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(-100, 0), ax.c2p(300, 0), color=GREY_C, stroke_width=1.2)
        line = curve(ax, sh, mtm, GOOD, stroke_width=3.5)
        jtd = DashedLine(ax.c2p(-100, r["jtd"] / 1e6), ax.c2p(300, r["jtd"] / 1e6), color=BAD, stroke_width=2.5)
        side = VGroup(
            label(rf"\$10 million of 5-year protection bought at {1e4 * r['s0']:.0f} bp", font_size=19, color=GREY_A),
            MathTex(rf"\text{{CS01}} \approx N \times \text{{RPV01}} \times 1\,\text{{bp}} = \${comma(r['cs01'])}",
                    font_size=24),
            MathTex(rf"\text{{gross default payment}} = N(1 - R) = \${r['jtd'] / 1e6:.0f}\,\text{{m}}", font_size=24, color=BAD),
            wrapped_label('concavity here is a property of this flat-curve example and bump convention. Spread sensitivity and the jump on default are separate risks', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Consider ten million dollars of five-year protection initially struck at par, one hundred fifty basis points. <bookmark mark='a'/> Near that initial par point, one basis point is worth about {r['cs01']:,.0f} dollars: notional times the risky annuity times one basis point. Away from par the annuity changes too; a full curve bump and repricing defines the actual sensitivity under a stated bump convention. <bookmark mark='b'/> With forty percent recovery, the gross default settlement is {r['jtd'] / 1000000.0:.0f} million dollars. That equals the clean jump from an initial zero mark only under this simplified setup. After a spread move, the jump is settlement less the pre-default mark, with accrual, recovery uncertainty and counterparty settlement rules included as appropriate. The seller has the opposite contract exposure, not a guaranteed stream of profits."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(jtd), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def bigbang(self, c):
        ups = c["upfronts"]
        rows = VGroup()
        hx = [-4.2, -1.2, 1.4, 4.2]
        heads = [r"name", r"par spread", r"coupon", r"upfront, \% of notional"]
        rows.add(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x, 1.9, 0]) for h_, x in zip(heads, hx)]))
        for i, (n_, u) in enumerate(ups.items()):
            y = 1.1 - 0.7 * i
            rows.add(VGroup(label(n_, font_size=20).move_to([hx[0], y, 0]),
                            MathTex(rf"{1e4 * u['par']:.0f}\ \text{{bp}}", font_size=28).move_to([hx[1], y, 0]),
                            MathTex(rf"{1e4 * u['coupon']:.0f}\ \text{{bp}}", font_size=28).move_to([hx[2], y, 0]),
                            MathTex(rf"{100 * u['upfront']:+.1f}", font_size=28,
                                    color=BAD if u["upfront"] > 0 else GOOD).move_to([hx[3], y, 0])))
        title = label(r"8 April 2009, the Big Bang: standard contracts", font_size=28).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"since 2009, North American contracts pay 100 or 500 bp, the difference settled upfront; "
                             r"defaults are settled by an auction for eligible covered contracts (Lehman, 10 October 2008: "
                             r"8.625); standard contracts can be cleared centrally. Upfront = protection leg $-$ coupon "
                             r"$\times$ RPV01", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The April two thousand nine Big Bang standardized important CDS conventions, building on auctions already used before then, including Lehman's. <bookmark mark='a'/> Standard North American corporate contracts commonly use one hundred or five hundred basis point coupons, with an upfront amount reconciling the coupon to the current price under the convention. This is not a universal coupon rule for every CDS market. The illustration assumes the displayed curve and recovery. <bookmark mark='b'/> Auction settlement, determination procedures and standardized documentation improve processing, but eligibility depends on the contract. Clearing applies to eligible contracts and manages counterparty exposure; it does not eliminate credit, liquidity or default-management risk."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def auction(self):
        rows = [cmath(r"\text{stage 1}", r":", r"\text{dealers quote bids and offers on the bonds} \to \text{the inside "
                      r"market midpoint}", font_size=30, colors={r"\text{stage 1}": GOOD}),
                cmath(r"\text{open interest}", r"=", r"\text{net requests to buy or sell bonds at the final price}",
                      font_size=30, colors={r"\text{open interest}": QC.IMPLIED}),
                cmath(r"\text{stage 2}", r":", r"\text{limit orders fill the open interest} \to \text{the final price } P",
                      font_size=30, colors={r"\text{stage 2}": BAD}),
                cmath(r"\text{payout}", r"=", r"N\,(1 - P),\ \ \text{Lehman: } P = 8.625\%", font_size=32,
                      colors={r"\text{payout}": BAD})]
        whys = [why(r"after a credit event, dealers submit two-way prices for the deliverable bonds; outliers are "
                    r"discarded and the inside market's midpoint is published"),
                why(r"protection buyers and sellers can ask to settle physically: their net demand to buy or sell bonds "
                    r"is the open interest"),
                why(r"a second round of limit orders absorbs that open interest; the price that clears it is the final "
                    r"price, used for covered auction-settled contracts"),
                why(r"so a contract's value at default is fixed by one public price, subject to eligibility, netting and counterparty performance")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.5, edge=6.9)
        with self.voiceover(
            "This is a schematic of an auction settlement mechanism, whose detailed rules depend on the relevant auction terms. <bookmark mark='a'/> Dealers submit initial markets, from which the initial market midpoint is determined under the rules. <bookmark mark='b'/> Physical-settlement requests contribute to net open interest. <bookmark mark='c'/> Limit orders then help establish the final price, subject to the auction's constraints. <bookmark mark='d'/> The Lehman auction final price was eight point six two five percent of par. Covered auction-settled protection therefore had a gross loss payment of ninety-one point three seven five percent of notional, before considering premiums, netting, hedges or counterparty failure. That is not the net cash exchanged on all outstanding Lehman contracts."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def basis(self):
        rows = [cmath(r"\text{basis}", r"=", r"s_{\text{CDS}} - s_{\text{bond}}", font_size=42, colors={r"\text{basis}": RISKY})]
        whys = [why('an ideal matched payoff motivates the basis relation; funding, deliverability and counterparty risks matter. In late 2008 negative basis trades faced costly funding and scarce balance-sheet capacity')]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        card = house_lab(r"bootstrapping a hazard curve", CR.bootstrap_hazard, "for T, s in zip", 7, width=7.6)
        card.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The cash-CDS basis compares a bond's credit spread with protection pricing under specified conventions. In an idealized matched trade, buying a bond and protection can offset a defined default payoff. In practice maturity, coupon, deliverability, recovery, funding, repo, liquidity and counterparty risks leave residual exposures. It is not automatically a riskless Treasury. In late two thousand eight funding and balance-sheet constraints contributed to large negative bases. <bookmark mark='a'/> The House's bootstrap solves one hazard interval at a time. A real basis trade also needs cash-flow matching, financing and stressed exit assumptions, rather than a spread comparison alone."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(card))
        q = ask(r"a 5-year CDS trades at 100 bp and recovery is 40\%. Roughly what annual default probability does it "
                r"imply?")
        with self.voiceover("A five-year CDS trades at one hundred basis points, recovery forty percent. Roughly what "
                            "annual default probability does that imply?"):
            self.play(FadeOut(card), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: distinguish intensity from event probability', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('$\\lambda^Q\\approx0.01/0.6=1.6667\\%$; $1-e^{-\\lambda^Q}=1.65\\%$ over one year and $1-e^{-5\\lambda^Q}=8.00\\%$ over five.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('The credit triangle gives risk-neutral intensity of about one point six six seven percent per year. The corresponding one-year probability is about one point six five percent, and five-year probability about eight percent under a flat intensity. It is not a physical forecast, and scheduled premium, recovery and settlement conventions affect the exact bootstrap.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
