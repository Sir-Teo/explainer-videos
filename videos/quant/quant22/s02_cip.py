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
        rows = [cmath(r"\ln\frac{F}{Q}", r"\approx", r"(y_\$ - y_\pounds)\,\tau", font_size=40,
                      colors={r"\ln\frac{F}{Q}": BASIS}),
                cmath(r"x", r"=", r"y_\$ - y_\pounds - \tfrac{1}{\tau}\ln\frac{F}{Q}", font_size=40, colors={r"x": BASIS})]
        whys = [why(r"in continuously compounded rates the forward premium equals the interest differential: the "
                    r"currency with the lower rate is dearer for future delivery"),
                why(r"the cross-currency basis (Du, Tepper and Verdelhan, 2018): the gap between borrowing dollars "
                    r"directly and borrowing them synthetically, by borrowing pounds and swapping them. Parity says "
                    r"$x = 0$; $x < 0$ means synthetic dollars cost more")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "In logarithms it is cleaner. The forward premium equals the interest differential times the horizon. "
            "<bookmark mark='a'/> Whatever is left over is the basis: the dollar rate, less the rate on dollars "
            "obtained synthetically, by borrowing pounds and swapping them into dollars. If parity holds, the basis is "
            "zero. If it is negative, dollars bought through the swap cost more than dollars borrowed directly, and "
            "anyone who can borrow dollars directly and lend them through the swap earns the difference, without "
            "risk. In 2018 Wenxin Du, Alexander Tepper and Adrien Verdelhan showed that after 2008 it was not zero, "
            "for years, in every major currency."
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
            wrapped_label(r"spot and 3-month forward: the Bank of England's London quotes; rates: 3-month LIBOR in each "
                          r"currency (the dollar's on an actual/360 basis, put on one year). The forward was dearer than "
                          r"parity allows: pounds swapped into dollars cost more than dollars", 12.0, 18, GREY_A),
        ).arrange(DOWN, buff=0.32)
        with self.voiceover(
            "Take one month, June 2016. <bookmark mark='a'/> Sterling at one point four two dollars; three-month dollar "
            "money at about two thirds of a percent, sterling at a little over half a percent. <bookmark mark='b'/> "
            f"Parity puts the three-month forward at {w['F_parity']:.4f}. <bookmark mark='c'/> The market's forward "
            f"was {w['F']:.4f}. The difference looks tiny, a few hundredths of a cent, but at three months it is a "
            f"basis of {w['x_bp']:.0f} basis points a year, on a trade with no risk at all, open to anyone with a "
            "balance sheet."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
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
            "Now every month for thirty years. <bookmark mark='a'/> Until 2007 the sterling basis stays within a few "
            f"basis points of zero, about {c['mean_pre_bp']:.0f} on average: the cost of doing the trade. Parity held. "
            "<bookmark mark='b'/> In the crisis it collapsed, to "
            f"{abs(c['min_bp']):.0f} basis points in the monthly average of November 2008: banks outside America "
            "could not borrow dollars, and paid almost any price to swap for them. <bookmark mark='c'/> And then it "
            f"did not come back. From 2010 to 2016 it averaged {c['mean_post_bp']:.0f}, month after month, with "
            "markets calm. A riskless profit, sitting in plain sight, for six years."
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
        whys = [why(r"the arbitrage borrows dollars and lends them through the swap: it is riskless, but it puts two "
                    r"large positions on a bank's balance sheet"),
                why(r"under a leverage ratio of 3\%, a bank must hold 3 dollars of capital per 100 of any asset; at a "
                    r"10\% hurdle that is 30 basis points a year, more than the basis. Du, Tepper and Verdelhan: the "
                    r"basis widens at quarter-ends, when non-US banks report their balance sheets")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Why does nobody take it? The trade is riskless, but it is not free. To earn the basis a bank borrows "
            "dollars and lends them through the swap, and both legs sit on its balance sheet. <bookmark mark='a'/> "
            "After 2008, every dollar of balance sheet needs capital, even a riskless one: the leverage ratio of Part "
            "twenty-one's chapter twelve. Three cents of capital per dollar, at a ten percent required return, is "
            "about thirty basis points a year, more than the basis. Du, Tepper and Verdelhan found the clinching "
            "evidence: the basis jumps at the ends of quarters, when banks outside America take the snapshot of their "
            "balance sheets that regulators see. The price of the basis is the price of balance sheet."
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
            desk_question(r"who could arbitrage", r"a US money fund or a central bank, which can lend dollars without "
                          r"the capital cost; the Fed's swap lines with other central banks, opened in December 2007, widened "
                          r"in 2008 and again in March 2020, cap how far the basis can go", width=12.0, font_size=21),
            desk_question(r"what it means", r"a law of one price can fail without anyone being irrational: when "
                          r"arbitrage needs balance sheet, the price includes what balance sheet costs", width=12.0,
                          font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "On one side are the investors who need dollars: Japanese insurers and European banks with American "
            "assets, who hedge them by swapping their own currency into dollars. <bookmark mark='a'/> On the other, "
            "the few who can lend dollars without the capital cost. When even they are not enough, the Federal "
            "Reserve's swap lines with other central banks put a ceiling on the price; they were opened at the end of "
            "2007, widened in 2008, and widened again in March 2020. <bookmark mark='b'/> The lesson is general. A law of one price can fail without "
            "anyone being foolish, when the arbitrage needs something scarce."
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
