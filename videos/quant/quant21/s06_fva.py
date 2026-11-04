from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, DVA_C, FVA_C, GOOD, IM_C, PART, ask, fit_right, illustration, load


class FVA(VoiceoverScene):
    def construct(self):
        f = load("fva")
        v = load("cva")
        self.card()
        self.funding()
        self.debate()
        self.kva(f)
        self.stack(f, v)
        self.asym(load("fvaasym"))

    def card(self):
        c = chapter_card(5, r"FVA, KVA and MVA", r"What does it cost to fund, hold capital and post margin?", part=PART)
        with self.voiceover("Chapter five. Funding, capital and margin: the other valuation adjustments."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def funding(self):
        def box(t, c_, w=3.4):
            r_ = RoundedRectangle(corner_radius=0.15, width=w, height=1.0, stroke_color=c_, stroke_width=2.5)
            return VGroup(r_, wrapped_label(t, w - 0.3, 19).move_to(r_))
        client = box(r"client: no collateral", BAD).move_to(LEFT * 4.4 + UP * 1.2)
        bank = box(r"the bank's desk", WHITE).move_to(UP * 1.2)
        street = box(r"hedge with a dealer: collateralised", GOOD).move_to(RIGHT * 4.4 + UP * 1.2)
        a1 = DoubleArrow(client.get_right(), bank.get_left(), buff=0.1, color=GREY_B)
        a2 = DoubleArrow(bank.get_right(), street.get_left(), buff=0.1, color=GREY_B)
        cash = Arrow(bank.get_bottom() + RIGHT * 2.5, bank.get_bottom() + RIGHT * 2.5 + DOWN * 1.4, buff=0.1, color=FVA_C)
        lab = wrapped_label(r"when the trade is in the bank's favour, the hedge is against it: the bank posts collateral "
                            r"to the dealer, and must borrow it at its own funding spread, unsecured", 6.0, 19,
                            FVA_C).next_to(cash, DOWN, buff=0.15).shift(LEFT * 1.0)
        rows = cmath(r"\text{FVA}", r"=", r"s_F\sum_i \big(\text{EE}(t_i) + \text{ENE}(t_i)\big)\,P(0, t_i)\,\Delta t_i\,Q(t_i)",
                     font_size=34, colors={r"\text{FVA}": FVA_C}).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Where does funding come in? A bank trades with a client who posts no collateral, and hedges the trade "
            "with another dealer, under a collateral agreement. <bookmark mark='a'/> When the client's trade moves in "
            "the bank's favour, the hedge moves against it, and the bank must post cash to the dealer, cash it "
            "borrows at its own unsecured spread, while the client owes it the same amount without posting a cent. "
            "<bookmark mark='b'/> The cost of carrying that, over the trade's life, is the funding valuation "
            "adjustment: the spread times the expected exposure, discounted. When the trade moves the other way the "
            "bank receives collateral it can lend, a benefit."
        ) as vo:
            self.play(FadeIn(client), FadeIn(bank), FadeIn(street), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            self.play(GrowArrow(cash), FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(rows))
        self.wait(0.4)
        self.clear_scene()

    def debate(self):
        cards = VGroup(
            desk_question(r"Burgard and Kjaer (2011)", r"a replication argument with the bank's own funding: the "
                          r"derivative's value satisfies a PDE whose discount rate includes the bank's funding spread",
                          width=12.0, font_size=21),
            desk_question(r"Hull and White (2012): 'The FVA debate'", r"in a perfect market the funding cost of a "
                          r"project should not depend on who funds it; FVA mostly double counts DVA, and pricing with it "
                          r"breaks the law of one price between banks", width=12.0, font_size=21),
            desk_question(r"January 2014", r"J.P. Morgan reported a \$1.5 billion charge as it adopted FVA in its fourth "
                          r"quarter 2013 results; most large dealers had followed by then. Practice settled the debate "
                          r"the theory had not", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Should funding be in the price at all? Christoph Burgard and Mats Kjaer derived it in 2011 from the "
            "cost of replicating the trade with the bank's own funding. <bookmark mark='a'/> John Hull and Alan "
            "White replied in 2012 that it does not belong there: in a well-functioning market, the value of a "
            "project cannot depend on who finances it, and funding adjustments largely double count the bank's own "
            "default. <bookmark mark='b'/> In January 2014 J.P. Morgan took a one point five billion dollar charge to "
            "adopt FVA, and most large dealers had done the same. The market priced it before the theory agreed."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def kva(self, f):
        t = np.asarray(load("exposure")["times"])
        cap = np.asarray(f["capital_profile"])
        rows = [cmath(r"\text{KVA}", r"=", r"h\sum_i K(t_i)\,P(0, t_i)\,\Delta t_i", font_size=40, colors={r"\text{KVA}": BAD})]
        whys = [why(r"capital $K(t)$ must be held against the trade for its whole life, and shareholders want a return "
                    r"$h$ on it, here 10\% a year: KVA is that cost, discounted (Green, Kenyon and Dennis, 2014)")]
        step = ladder(self, rows, whys, keep=1, top=2.8, x=-0.4, buff=0.8, edge=6.9)
        g = axes([0, 10], [0, max(cap) * 1.25], x_length=6.6, y_length=2.8, xlabel=r"years", ylabel=r"capital, \$m",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.4, 0.8], font_size=13).to_edge(DOWN, buff=0.5).shift(LEFT * 2.6)
        ax = g.ax
        line = curve(ax, np.r_[0, t], np.r_[cap[0], cap], BAD, stroke_width=3)
        fn = ax.plot(lambda u: float(np.interp(u, np.r_[0, t], np.r_[cap[0], cap])), x_range=[0, 10, 0.05])
        area = ax.get_area(fn, x_range=[0, 10], color=BAD, opacity=0.25)
        side = VGroup(
            MathTex(rf"\text{{KVA}} = \${1e3 * f['KVA']:.0f}\text{{k}}", font_size=30, color=BAD),
            wrapped_label(r"capital here: a stand-in from the netting set's potential exposure, 1.4 times PFE, at 8\% "
                          r"and a 50\% risk weight (illustrative). The longer and larger the exposure, the more capital "
                          r"years the trade consumes", 4.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        fit_right(side, 6.85)
        with self.voiceover(
            "A third cost is capital. Regulators require the bank to hold capital against the trade for as long as "
            "it lives, and capital is the shareholders' money, on which they expect a return. <bookmark mark='a'/> "
            "The capital valuation adjustment, KVA, is that return, charged on the whole profile of capital the "
            "trade will need, and discounted. Andrew Green, Chris Kenyon and Chris Dennis gave it its name in 2014. "
            "<bookmark mark='b'/> On this netting set, with capital that follows its potential exposure and a ten "
            f"percent hurdle, KVA comes to about {1e3 * f['KVA']:.0f} thousand dollars: the area under the capital "
            "curve, times the hurdle rate."
        ) as vo:
            step(0)
            vo.wait_until("b")
            self.play(FadeIn(g), Create(line), FadeIn(area), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def stack(self, f, v):
        items = [("CVA", v["cva"], CVA_C), ("DVA", -v["dva"], DVA_C), ("FCA", f["FCA"], FVA_C), ("FBA", f["FBA"], GOOD),
                 ("KVA", f["KVA"], BAD), ("MVA", f["MVA"], IM_C)]
        g = axes([0.4, 6.6], [-0.4, 0.8], x_length=7.4, y_length=4.2, xlabel=r"", ylabel=r"\$ million (cost to the bank)",
                 xticks=[], yticks=[-0.2, 0, 0.2, 0.4, 0.6, 0.8], font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0.4, 0), ax.c2p(6.6, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, (n_, val, c_) in enumerate(items):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, val)[1]
            b_ = Rectangle(width=0.6, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=c_,
                           fill_opacity=0.8).move_to([ax.c2p(i + 1, 0)[0], (y0 + y1) / 2, 0])
            bars.add(VGroup(b_, MathTex(f"{val:+.2f}", font_size=22).next_to(b_, UP if val >= 0 else DOWN, buff=0.08),
                            label(n_, font_size=18).next_to(ax.c2p(i + 1, -0.4), DOWN, buff=0.1)))
        total = v["cva"] - v["dva"] + f["FVA"] + f["KVA"] + f["MVA"]
        side = VGroup(
            MathTex(rf"\text{{total XVA}} = \${total:.2f}\text{{m}}", font_size=30),
            wrapped_label(rf"funding spread {1e4 * f['spread']:.0f} bp both ways; capital at 10\% a year; initial margin "
                          r"from chapter 8. With symmetric spreads the funding cost and benefit nearly cancel; the cost "
                          r"of capital is the largest item for an uncollateralised client", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "All the adjustments on the same netting set, as costs to the bank. <bookmark mark='a'/> The credit "
            "adjustment, less the debit one. The funding cost and the funding benefit, which nearly cancel with "
            "symmetric spreads. <bookmark mark='b'/> The cost of holding regulatory capital against the trade for its "
            "whole life, KVA, here the largest. And the cost of funding initial margin, MVA. "
            f"<bookmark mark='c'/> Together about {total:.2f} million dollars on two hundred million of swaps: the "
            "difference between a price on a screen and a price a bank can offer a client."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bars[4]), FadeIn(bars[5]))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def asym(self, fa):
        rows = fa["rows"]
        hx = [-4.6, -2.4, -0.2, 2.0, 4.4]
        heads = [r"borrow at", r"lend at", r"funding cost", r"funding benefit", r"FVA"]
        tab = VGroup(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x, 1.9, 0]) for h_, x in zip(heads, hx)]))
        for i, r_ in enumerate(rows):
            y = 1.2 - 0.62 * i
            tab.add(VGroup(MathTex(rf"{1e4 * r_['borrow']:.0f}\text{{ bp}}", font_size=26).move_to([hx[0], y, 0]),
                           MathTex(rf"{1e4 * r_['lend']:.0f}\text{{ bp}}", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(rf"{1e3 * r_['FCA']:.0f}\text{{k}}", font_size=26, color=FVA_C).move_to([hx[2], y, 0]),
                           MathTex(rf"{1e3 * r_['FBA']:.0f}\text{{k}}", font_size=26, color=GOOD).move_to([hx[3], y, 0]),
                           MathTex(rf"{1e3 * r_['FVA']:.0f}\text{{k}}", font_size=28).move_to([hx[4], y, 0])))
        title = label(r"When borrowing costs more than lending earns", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"spreads over the risk-free rate. A bank's treasury rarely pays its desks for cash at the rate "
                             r"it charges them; when the two differ, the benefit of the client's posted value no longer "
                             r"offsets the cost of funding the exposure, and FVA becomes a real cost. A weaker bank's "
                             r"wider spread makes it uncompetitive on exactly the trades that need funding",
                             12.4, 18, GREY_A).to_edge(DOWN, buff=0.35)
        r0, r1, r2, r3 = rows
        with self.voiceover(
            "The cancellation depends on symmetry. <bookmark mark='a'/> If the bank borrows and lends at the same "
            f"eighty basis points, the funding cost of {1e3 * r0['FCA']:.0f} thousand is nearly paid back by the "
            f"benefit, and FVA is {1e3 * r0['FVA']:.0f} thousand. <bookmark mark='b'/> But a treasury seldom pays its "
            "desks for spare cash what it charges them for borrowing. Pay twenty basis points on the benefit side and "
            f"FVA becomes {1e3 * r1['FVA']:.0f} thousand; a bank whose borrowing spread is a hundred and fifty pays "
            f"{1e3 * r2['FVA']:.0f}. <bookmark mark='c'/> A strong bank at thirty both ways pays "
            f"{1e3 * r3['FVA']:.0f}. Cheap funding wins the uncollateralised business, and an expensive funder "
            "is left with the collateralised trades, which need no funding. Whether that is how it should be is the "
            "question to end the chapter."
        ) as vo:
            self.play(FadeIn(title), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"two banks quote the same uncollateralised swap. One funds at 20 bp over SOFR, the other at 150 bp. "
                r"Who wins the trade, and is that the right outcome?")
        with self.voiceover("Two banks quote the same uncollateralised swap; one funds at twenty basis points over SOFR, "
                            "the other at a hundred and fifty. Who wins the trade, and should they?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
