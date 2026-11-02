from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, PART, RATE, TRADE

ROWS = [
    (r"Share", r"a slice of a company", r"price per share", r"\$231.45", TRADE),
    (r"Bond", r"a loan: coupons, then the face value", r"clean price per 100 of face, or its yield",
     r"98.75\ \ (4.62\%)", RATE),
    (r"Future", r"an agreement to trade later, at a price fixed now, settled every day", r"the future price",
     r"6{,}125.50", TRADE),
    (r"Swap", r"an exchange of cash flows: fixed against floating", r"the fixed rate", r"3.85\%", RATE),
    (r"Option", r"a right, not an obligation, to buy or sell", r"premium, or implied volatility", r"4.20\ \ (18\%)",
     QC.OPTION),
    (r"ETF", r"a fund that trades like a share", r"price, beside its net asset value", r"512.33\ /\ 512.30", CASH),
]

COUPON, CLEAN = 5.0, 98.75  # a 5% semiannual bond quoted at 98.75 clean (illustrative)


class Instruments(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.dirty()
        self.contracts()
        self.notional()

    def card(self):
        c = chapter_card(1, r"Instruments and how they are quoted",
                         r"What exactly is being traded, and in what units?", part=PART)
        with self.voiceover("Chapter one. The instruments, and how they are quoted."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def table(self):
        hdr = [label(t, font_size=24, color=GREY_A) for t in (r"instrument", r"what it is", r"quoted as",
                                                             r"an example quote")]
        cells = list(hdr)
        rows = [VGroup(*hdr)]
        for name, what, quote, ex, col in ROWS:
            r_ = [label(name, font_size=26, color=col), wrapped_label(what, 4.6, 22, WHITE),
                  wrapped_label(quote, 3.4, 22, GREY_A), MathTex(ex, font_size=28, color=col)]
            cells += r_
            rows.append(VGroup(*r_))
        grid = VGroup(*cells).arrange_in_grid(len(ROWS) + 1, 4, buff=(0.45, 0.32), col_alignments="llll")
        if grid.width > 13.2:
            grid.scale_to_fit_width(13.2)
        grid.move_to(DOWN * 0.1)
        foot = note(r"example quotes are illustrative", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Six instruments carry almost everything in this series. A share: a slice of a company, quoted per share. "
            "<bookmark mark='a'/> A bond: a loan that pays coupons and then its face value, quoted per hundred of face or as "
            "the yield that price implies; Part eighteen builds the arithmetic. <bookmark mark='b'/> A future: an agreement "
            "to trade later at a price fixed now, settled every single day, which is why it needs margin. "
            "<bookmark mark='c'/> A swap: two parties exchange cash flows, typically fixed against floating, and the quote is "
            "the fixed rate. <bookmark mark='d'/> An option: a right without an obligation, quoted in dollars or in implied "
            "volatility. <bookmark mark='e'/> And an exchange-traded fund: a basket that trades like a share, kept near the "
            "value of what it holds by market makers who create and redeem its units, as Part thirty-eight shows."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(foot))
            for i, mark in enumerate("abcde", start=2):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i], shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def dirty(self):
        days = np.arange(0, 366)
        accrued = COUPON / 2 * ((days % 182.5) / 182.5)
        dirty = CLEAN + accrued
        g = axes([0, 365], [97.5, 102.0], x_length=6.0, y_length=4.0, xlabel=r"days held",
                 ylabel=r"price per 100 of face", xticks=[0, 182, 365], yticks=[98, 100, 102], font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        t = ValueTracker(0)
        clean = tracing(ax, days, np.full(len(days), CLEAN), t, RATE, stroke_width=3)
        dl = tracing(ax, days, dirty, t, QC.IDEA, stroke_width=3)
        wedge = always_redraw(lambda: band(ax, days[:int(t.get_value()) + 1], np.full(int(t.get_value()) + 1, CLEAN),
                                           dirty[:int(t.get_value()) + 1], QC.IDEA, 0.18)
                              if t.get_value() >= 1 else VGroup())
        leg = legend([(RATE, r"clean price: the quote"), (QC.IDEA, r"dirty price: what you pay")], font_size=20)
        leg.to_corner(UR, buff=0.5)
        rows = [cmath(r"P_{\text{dirty}}", r"=", r"P_{\text{clean}}", r"+", r"\tfrac{c}{2}\cdot\tfrac{\text{days since coupon}}{\text{days in the period}}", font_size=34),
                cmath(r"5\% \text{ bond, 91 days in}", r"=", r"98.75", r"+", r"1.25", r"= 100.00", font_size=34)]
        whys = [why(r"the seller has earned interest it will not collect: the buyer pays it", font_size=20),
                why(r"quoted clean, so the quote doesn't jump on coupon days", font_size=20)]
        for r_, w in zip(rows, whys):
            r_.scale(0.9)
        stack = VGroup(rows[0], whys[0], rows[1], whys[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stack.next_to(leg, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        if stack.width > 5.5:
            stack.scale_to_fit_width(5.5).to_edge(RIGHT, buff=0.35)
        q = desk_question(r"The clean price hasn't moved for a month. Did the holder earn anything?",
                          r"yes: a month of accrued interest, about 0.4 per 100 on this bond", width=6.0,
                          font_size=22).to_corner(DR, buff=0.3)
        src = note(r"illustrative bond: 5\% coupon, paid twice a year", font_size=17).to_corner(DL, buff=0.2)
        with self.voiceover(
            "Bond quotes hide one trap. Between coupons, interest accrues to whoever holds the bond. Bonds are quoted clean, "
            "without that interest, and the buyer pays the dirty price: clean plus accrued. The accrued part is the coupon "
            "times the fraction of the period that has passed since the last payment. Watch a year of a five percent bond "
            "paying twice a year, whose clean quote stays at ninety-eight seventy-five. <bookmark mark='a'/> What you pay "
            "climbs every day by the coupon's share, then drops by two and a half on each coupon date, when the interest is "
            "paid out: a saw-tooth over a flat line. <bookmark mark='b'/> Ninety-one days in, half a period, the buyer pays a "
            "hundred, of which one twenty-five is the seller's interest. Quoting clean keeps the quote from jumping on coupon "
            "days, so price changes mean what they should. Pause and predict: the clean price hasn't moved for a month. Did "
            "the holder earn anything?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.add(clean, dl, wedge)
            vo.wait_until("a")
            self.play(t.animate.set_value(365), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(stack))
        self.play(FadeOut(stack), FadeIn(q))
        self.wait(1.0)
        for m in (clean, dl, wedge):
            m.clear_updaters()
        self.clear_scene()

    def contracts(self):
        fut = definition_card(r"E-mini S\&P 500 future (CME)",
                              r"\$50 times the index; the tick is 0.25 index points, \$12.50; quarterly expiries "
                              r"(March, June, September, December); settled in cash; marked to market every day.",
                              width=6.0, color=TRADE, font_size=21, kind=r"Contract")
        opt = definition_card(r"A US equity option",
                              r"One contract is 100 shares; a strike, an expiry, American exercise for single "
                              r"stocks; every trade is cleared by the Options Clearing Corporation, which becomes "
                              r"buyer to every writer.", width=6.0, color=QC.OPTION, font_size=21, kind=r"Contract")
        pair = VGroup(fut, opt).arrange(RIGHT, buff=0.4, aligned_edge=UP).shift(UP * 0.9)
        ex = MathTex(r"6{,}125.50 \times \$50 = \$306{,}275\ \text{of exposure per contract}", font_size=34,
                     color=TRADE).next_to(pair, DOWN, buff=0.5)
        foot = note(r"CME contract specifications; OCC; the index level is illustrative", font_size=17)
        foot.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "A listed derivative is a standard contract. The E-mini S and P five hundred future is fifty dollars times the "
            "index, moves in quarter points, twelve fifty a tick, expires quarterly and settles in cash: at sixty-one "
            "twenty-five, three hundred thousand dollars of exposure. <bookmark mark='a'/> An American equity option is on a "
            "hundred shares, and every one is cleared by the Options Clearing Corporation."
        ) as vo:
            self.play(FadeIn(fut, shift=UP * 0.2), FadeIn(foot))
            self.play(Write(ex))
            vo.wait_until("a")
            self.play(FadeIn(opt, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def notional(self):
        d = definition_card(r"Notional", r"The size a derivative refers to, not its value. A swap on \$100 million "
                            r"notional exchanges interest computed on \$100 million, but its value may be a few "
                            r"hundred thousand; a future on \$1 million of an index can be held with \$50{,}000 of "
                            r"margin.", width=9.6, color=QC.IDEA).shift(UP * 1.4)
        rows = VGroup(
            MathTex(r"\text{leverage} = \frac{\text{notional exposure}}{\text{equity (margin)}}", font_size=40,
                    color=QC.HOUSE),
            MathTex(r"\text{swap value} \approx \text{DV01} \times \Delta y:\ \ "
                    r"\$100\text{m},\ 5\text{ years: } \approx\$45{,}000 \text{ per basis point}", font_size=30),
        ).arrange(DOWN, buff=0.4).next_to(d, DOWN, buff=0.5)
        with self.voiceover(
            "Keep one word straight: notional, the size a derivative refers to, not its value. A five-year swap on a hundred "
            "million dollars may be worth only a few hundred thousand, and gains or loses about forty-five thousand per basis "
            "point. A future on a million dollars of an index can be held with fifty thousand of margin. "
            "<bookmark mark='a'/> Exposure over the money put up is leverage, and leverage is what turns the plumbing of this "
            "part into a matter of survival."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(Write(rows[0]))
        self.wait(0.4)
        self.clear_scene()
