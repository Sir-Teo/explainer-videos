from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class CIP(VoiceoverScene):
    def construct(self):
        c = load("cip")
        self.card()
        self.triangle()
        self.derive()
        self.worked(c)
        self.history(c)
        self.why()
        self.balance()

    def card(self):
        c = chapter_card(1, r"Covered interest parity", r"What must a currency forward cost?", lit=(2008,), part=PART)
        with self.voiceover("Chapter one. Covered interest parity: what a currency forward must cost, and why after "
                            "2008 it did not."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def triangle(self):
        def box(t, c_, pos):
            r_ = RoundedRectangle(corner_radius=0.15, width=3.6, height=1.1, stroke_color=c_, stroke_width=2.5).move_to(pos)
            return VGroup(r_, wrapped_label(t, 3.3, 19).move_to(r_))
        a = box(r"\$1 today", USD, LEFT * 4.4 + UP * 1.6)
        b = box(r"$1/Q$ pounds today", FOR, RIGHT * 4.4 + UP * 1.6)
        c_ = box(r"$(1 + r_\$ \tau)$ dollars in 3 months", USD, LEFT * 4.4 + DOWN * 1.4)
        d = box(r"$(1 + r_\pounds \tau)/Q$ pounds in 3 months", FOR, RIGHT * 4.4 + DOWN * 1.4)
        ab = Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B)
        ac = Arrow(a.get_bottom(), c_.get_top(), buff=0.1, color=USD)
        bd = Arrow(b.get_bottom(), d.get_top(), buff=0.1, color=FOR)
        dc = Arrow(d.get_left(), c_.get_right(), buff=0.1, color=GREY_B)
        l_ab = label(r"exchange at spot $Q$ (\$ per \pounds)", font_size=17, color=GREY_A).next_to(ab, UP, buff=0.1)
        l_ac = label(r"deposit dollars", font_size=17, color=USD).next_to(ac, LEFT, buff=0.1)
        l_bd = label(r"deposit pounds", font_size=17, color=FOR).next_to(bd, RIGHT, buff=0.1)
        l_dc = label(r"sell forward at $F$, agreed today", font_size=17, color=GREY_A).next_to(dc, DOWN, buff=0.1)
        eq = MathTex(r"F", r"=", r"Q\,\frac{1 + r_\$\,\tau}{1 + r_\pounds\,\tau}", font_size=40).move_to(DOWN * 0.0)
        eq[0].set_color(BASIS)
        with self.voiceover(
            "A dollar today can reach three months from now by two routes. <bookmark mark='a'/> Deposit it, and it "
            "grows at the dollar interest rate. <bookmark mark='b'/> Or change it into pounds at today's spot rate, "
            "deposit the pounds at the sterling rate, and agree today to sell them back for dollars at a forward rate. "
            "<bookmark mark='c'/> Both routes are riskless, and both end in dollars. So they must end with the same "
            "number of dollars, and that fixes the forward: the spot rate, times the ratio of the two interest "
            "accounts. That is covered interest parity. A currency with lower interest rates trades at a premium for "
            "future delivery, exactly enough to cancel its lower interest."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("a")
            self.play(GrowArrow(ac), FadeIn(l_ac), FadeIn(c_))
            vo.wait_until("b")
            self.play(GrowArrow(ab), FadeIn(l_ab), FadeIn(b))
            self.play(GrowArrow(bd), FadeIn(l_bd), FadeIn(d))
            self.play(GrowArrow(dc), FadeIn(l_dc))
            vo.wait_until("c")
            self.play(Write(eq))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\ln\frac{F}{Q}", r"=", r"(y_\$ - y_\pounds)\,\tau", font_size=40,
                      colors={r"\ln\frac{F}{Q}": BASIS}),
                cmath(r"x", r"=", r"y_\$ - y_\pounds - \tfrac{1}{\tau}\ln\frac{F}{Q}", font_size=40, colors={r"x": BASIS})]
        whys = [why(r"in continuously compounded rates the forward premium equals the interest differential: the "
                    r"currency with the lower rate is dearer for future delivery"),
                why(r"the cross-currency basis (Du, Tepper and Verdelhan, 2018): the gap between borrowing dollars "
                    r"directly and borrowing them synthetically, by borrowing pounds and swapping them. Parity says "
                    r"$x = 0$; $x < 0$ means synthetic dollars cost more")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "In logarithms it is cleaner. Using continuously compounded rates over exactly the forward's settlement horizon, covered parity equates the log forward premium to the rate differential. <bookmark mark='a'/> The residual is the basis: the direct dollar rate less the synthetic dollar funding rate. A negative basis means dollars obtained through the swap cost more. In the ideal matched-credit, frictionless setup, borrowing dollars directly and lending them through the swap captures that difference. Real trades also need credit lines, collateral, funding, settlement and balance sheet. Du, Tepper and Verdelhan documented persistent post-crisis deviations using carefully matched instruments; our next chart is a coarser public-series reconstruction."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def worked(self, c):
        w = c["worked"]
        rows = VGroup(
            label(rf"June 2016, monthly averages: one month in thirty years", font_size=22, color=GREY_A),
            MathTex(rf"Q = {w['S']:.4f},\quad r_\$ = {100 * w['r_usd']:.3f}\%,\quad r_\pounds = {100 * w['r_gbp']:.3f}\%",
                    font_size=32),
            MathTex(rf"F_{{\text{{parity}}}} = {w['S']:.4f}\times\frac{{1 + {w['r_usd']:.5f}/4}}{{1 + {w['r_gbp']:.5f}/4}}"
                    rf" = {w['F_parity']:.4f}", font_size=32, color=GOOD),
            MathTex(rf"F_{{\text{{market}}}} = {w['F']:.4f}", font_size=32, color=BASIS),
            MathTex(rf"x = {w['x_bp']:.1f}\ \text{{bp a year}}", font_size=36, color=BASIS),
            wrapped_label("spot and 3-month forward: the Bank of England's London quotes; rates: 3-month LIBOR in each currency (the dollar's on an actual/360 basis, put on one year). Averages and funding proxies have different clocks; this residual is descriptive, with no executable-arbitrage certification", 12.0, 18, GREY_A),
        ).arrange(DOWN, buff=0.32)
        with self.voiceover(
            f"Take one month, June 2016, as a descriptive calculation. <bookmark mark='a'/> These are monthly average sterling spot and three-month outright forward quotes, with a reconstructed dollar LIBOR proxy and sterling LIBOR. They do not form one simultaneously executable quote. <bookmark mark='b'/> Applying the simple-rate parity formula to these average inputs gives {w['F_parity']:.4f}. <bookmark mark='c'/> The average reported forward is {w['F']:.4f}; the saved reconstruction's average daily log residual is {w['x_bp']:.0f} basis points a year. Averaging before and after taking a logarithm need not agree exactly. Credit, quote clocks, day counts, transaction costs and collateral prevent this residual from certifying a riskless profit available to any trader."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(Indicate(rows[1], scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]), FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    def history(self, c):
        t, x = np.asarray(c["t"]), 1e4 * np.asarray(c["x"])
        g = axes([1986, 2017.5], [-160, 50], x_length=8.4, y_length=4.4, xlabel=r"year",
                 ylabel=r"sterling 3-month basis, bp a year", xticks=[1990, 2000, 2008, 2016],
                 yticks=[-150, -100, -50, 0, 50], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(1986, 0), ax.c2p(2017.5, 0), color=GREY_B, stroke_width=1.5)
        k1 = int(np.searchsorted(t, 2007.6))
        l1 = curve(ax, t[:k1], x[:k1], USD, stroke_width=2.4)
        l2 = curve(ax, t[k1 - 1:], x[k1 - 1:], BASIS, stroke_width=2.4)
        mn = c["min_ym"]
        side = VGroup(
            MathTex(rf"1986\text{{--mid }}2007:\ {c['mean_pre_bp']:+.0f}\pm{c['sd_pre_bp']:.0f}", font_size=24, color=USD),
            MathTex(rf"2007\text{{--}}09:\ {c['mean_crisis_bp']:+.0f};\ \min {c['min_bp']:.0f}\ ({mn // 100}\text{{-}}"
                    rf"{mn % 100:02d})", font_size=24, color=BASIS),
            MathTex(rf"2010\text{{--}}16:\ {c['mean_post_bp']:+.0f}\pm{c['sd_post_bp']:.0f}", font_size=24, color=BASIS),
            wrapped_label(r"monthly averages, so the quarter-end spikes the daily data shows are smoothed away. Before "
                          r"2007 the gap is a few basis points, about the cost of trading; after 2008 it is negative for "
                          r"years at a time", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Now the saved monthly reconstruction across thirty years. <bookmark mark='a'/> Before the crisis its mean residual is {c['mean_pre_bp']:.0f} basis points. This is descriptive agreement near zero, not a transaction-cost estimate. <bookmark mark='b'/> The monthly minimum is {c['min_bp']:.0f} basis points in November 2008, during severe dollar-funding stress. <bookmark mark='c'/> The 2010 through 2016 mean is {c['mean_post_bp']:.0f}. Persistent deviations in matched professional data motivated the balance-sheet explanation, but this mixed-clock proxy cannot separately identify that mechanism. The dollar proxy adds TED to a discount-basis Treasury bill quote; it is not an exact contemporaneous deposit yield. Monthly averaging also obscures quarter-end spikes."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"Bank of England XUDLUSS, XUDLDS3; FRED TEDRATE + DTB3 (dollar LIBOR), LIOR3MUKM"))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        rows = [cmath(r"\text{profit}", r"=", r"|x| - \text{cost of balance sheet}", font_size=40,
                      colors={r"\text{profit}": GOOD}),
                cmath(r"\text{cost of balance sheet}", r"\approx", r"\text{capital ratio}\times\text{hurdle rate}",
                      font_size=36, colors={r"\text{cost of balance sheet}": BAD})]
        whys = [why('Ideal matched trade: borrow dollars and lend synthetically. Actual credit, collateral, liquidity, settlement and balance-sheet costs remain'),
                why('Illustrative charge: 3\\% relevant leverage exposure times a 10\\% hurdle gives 30 bp/year. Actual exposure, netting, jurisdiction and date matter; this is not a charge on every gross notional')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Why might the basis persist? A matched covered trade eliminates the exchange-rate exposure, yet lending, collateral and settlement still require resources. <bookmark mark='a'/> As a rough illustration, three percent capital times a ten percent hurdle is thirty basis points a year per unit of relevant leverage exposure. This is not a universal charge on every gross notional: netting, derivatives exposure measures, jurisdiction and date matter. Quarter-end basis patterns are evidence consistent with reporting and balance-sheet constraints, alongside dollar hedging demand, funding liquidity and credit differences. The equation is a stylized economic cost comparison, rather than a complete regulatory capital formula."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def balance(self):
        cards = VGroup(
            desk_question(r"who pays", r"Japanese life insurers and European banks with dollar assets hedge them by "
                          r"swapping their own currency for dollars: they are the demand that pushes the basis negative",
                          width=12.0, font_size=21),
            desk_question(r"who could arbitrage", 'Other intermediaries and central-bank facilities can supply dollars, subject to their own access, credit and funding constraints. Swap lines can ease stress, with no universal hard basis cap', width=12.0, font_size=21),
            desk_question(r"what it means", r"a law of one price can fail without anyone being irrational: when "
                          r"arbitrage needs balance sheet, the price includes what balance sheet costs", width=12.0,
                          font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Dollar hedging demand can come from insurers, banks and other investors holding dollar assets. <bookmark mark='a'/> Supplying the other side requires funding, counterparties, collateral and capacity. Central-bank swap lines can ease systemic dollar stress, but access, eligible counterparties, pricing and distribution matter. They do not impose a universal hard ceiling on every quoted basis. <bookmark mark='b'/> Persistent price differences can be consistent with rational behavior when intermediation uses scarce resources. That explanation does not turn every measured residual into executable arbitrage: the currency quote, settlement dates, lending risks and financing terms still have to match."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"dollar rates are 5\% and yen rates 0\%. Is the yen forward at a premium or a discount, and by how much "
                r"over a year? Why doesn't carry arbitrage it away?")
        with self.voiceover("Dollar rates are five percent and yen rates zero. Is the yen at a forward premium or a "
                            "discount, and by how much over a year? And why doesn't anyone arbitrage it away?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
