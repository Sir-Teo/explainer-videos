from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import credit as CR
from videos.quant.quant20.common import (BAD, GOOD, HAZ, PART, RISKY, ask, fit_right, house_lab, illustration, load,
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
        foot = wrapped_label(r"J.P. Morgan wrote the first in 1994: insurance on its credit line to Exxon, sold to the "
                             r"European Bank for Reconstruction and Development. The buyer need not own any bond: a CDS "
                             r"can hedge, or simply bet", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A credit default swap is insurance on a company's debt. <bookmark mark='a'/> The buyer of protection pays "
            "a fixed spread every quarter. <bookmark mark='b'/> If the company defaults, the seller pays the loss: "
            "face value minus what the company's bonds are worth afterwards. <bookmark mark='c'/> A team at J.P. "
            "Morgan wrote the first in 1994, to shed the risk of a credit line to Exxon. Unlike insurance, the buyer "
            "need not own the bonds: a CDS can be a hedge, or a pure bet on default."
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
                why(r"the par spread sets the two legs equal; with a flat hazard it is the credit triangle")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "Pricing it is the last chapter's survival curve, used twice. The premium leg: each payment, discounted, "
            "times the chance the company is still alive to make it necessary, plus the premium accrued when default "
            "falls between dates. <bookmark mark='a'/> The protection leg: the loss, discounted from the moment of "
            "default, weighted by the chance of default at each moment. <bookmark mark='b'/> The par spread makes "
            "them equal, and with a flat hazard it is the credit triangle again."
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
            "The market quotes par spreads at standard maturities. Bootstrap them, as Part eighteen bootstrapped a "
            "yield curve: <bookmark mark='a'/> the one-year quote fixes the hazard for the first year; the two-year "
            "quote, given that, fixes the second; and so on out to ten. <bookmark mark='b'/> The result is a hazard "
            "curve, rising here because the market expects this name to get riskier, and the survival curve it "
            "implies. Every other contract on the name is then priced off it."
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
            MathTex(rf"\text{{CS01}} \approx N \times \text{{RPV01}} \times 1\,\text{{bp}} = \${r['cs01']:,.0f}".replace(",", "{,}"),
                    font_size=24),
            MathTex(rf"\text{{jump to default}} = N(1 - R) = \${r['jtd'] / 1e6:.0f}\,\text{{m}}", font_size=24, color=BAD),
            wrapped_label(r"the mark-to-market is concave: as the spread widens the name is more likely to default soon, "
                          r"so fewer premiums remain to be saved. Risk desks report both numbers: the spread risk and "
                          r"the jump", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A desk that buys ten million dollars of protection at a hundred and fifty basis points has two kinds of "
            "risk. <bookmark mark='a'/> If the spread moves, the contract is revalued: each basis point is worth "
            f"about {r['cs01']:,.0f} dollars, the risky annuity times the notional, and the gain bends as the spread "
            "widens, because a riskier name has fewer premiums left to pay. <bookmark mark='b'/> And if the name "
            f"defaults, the jump: {r['jtd'] / 1e6:.0f} million dollars at once, the notional less the recovery. A "
            "seller of protection holds the mirror image: small steady income, and a large loss on one day."
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
                             r"defaults are settled by one auction for all contracts on a name (Lehman, 10 October 2008: "
                             r"8.625); standard contracts can be cleared centrally. Upfront = protection leg $-$ coupon "
                             r"$\times$ RPV01", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Until 2009 every contract had its own spread, and each default was settled bond by bond. On the eighth "
            "of April 2009, the Big Bang standardized the market. <bookmark mark='a'/> Contracts now pay a fixed "
            "coupon, one hundred or five hundred basis points, and the difference from the par spread changes hands "
            "upfront. A safe name trading at sixty pays back to the buyer; a distressed one at twelve hundred costs "
            "the buyer a fifth of the notional on day one. <bookmark mark='b'/> Defaults are settled by a single "
            "auction for every contract on a name, as Lehman's was, and standard contracts can go to a clearing house."
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
                    r"price, used for every contract on the name"),
                why(r"so a contract's value at default is fixed by one public price, whatever the holder owns")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.5, edge=6.9)
        with self.voiceover(
            "How is that single recovery price found? By an auction in two stages. <bookmark mark='a'/> First, "
            "dealers quote bids and offers on the defaulted bonds, and the midpoint of the best quotes is published. "
            "<bookmark mark='b'/> Then those who want to settle by delivering or receiving bonds say so, and their net "
            "demand is the open interest. <bookmark mark='c'/> A second round of orders absorbs it, and the price that "
            "clears it is final. <bookmark mark='d'/> For Lehman it was eight point six two five, and every contract "
            "paid ninety-one point three seven five percent of its notional."
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
        whys = [why(r"buy the bond and buy protection on it: default risk cancels, so the CDS spread should equal the "
                    r"bond's spread over the funding rate. In late 2008 the basis went deeply negative: bonds were "
                    r"cheap, but holding them needed balance sheet and funding that nobody had, the same lesson as "
                    r"Part 18's swap spreads")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        card = house_lab(r"bootstrapping a hazard curve", CR.bootstrap_hazard, "for T, s in zip", 7, width=7.6)
        card.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And one relation ties the swap to the bond. Buy a bond and buy protection on it, and the default risk "
            "cancels; what is left should earn the safe rate. So the swap's spread should match the bond's. In late "
            "2008 it did not: bonds yielded far more than the protection cost, a deeply negative basis, because "
            "holding bonds took funding and balance sheet that no one had to spare. <bookmark mark='a'/> The House's "
            "bootstrap, for the record: one hazard per quote, solved in order."
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
