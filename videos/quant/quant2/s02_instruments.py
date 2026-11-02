from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, PART, RATE, TRADE

ROWS = [
    (r"Share", r"a slice of a company", r"price per share", r"\$231.45", TRADE),
    (r"Bond", r"a loan: coupons, then the face value", r"price per 100 of face, or its yield", r"98.75\ \ (4.62\%)", RATE),
    (r"Future", r"an agreement to trade later, at a price fixed now, settled every day", r"the future price",
     r"6{,}125.50", TRADE),
    (r"Swap", r"an exchange of cash flows: fixed against floating", r"the fixed rate", r"3.85\%", RATE),
    (r"Option", r"a right, not an obligation, to buy or sell", r"premium, or implied volatility", r"4.20\ \ (18\%)",
     QC.OPTION),
    (r"ETF", r"a fund that trades like a share", r"price, beside its net asset value", r"512.33\ /\ 512.30", CASH),
]


class Instruments(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.notional()

    def card(self):
        c = chapter_card(1, r"The instruments", r"What exactly is being traded, and how is it quoted?", part=PART)
        with self.voiceover("Chapter one. The instruments."):
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
            "Six instruments carry almost everything in this series. A share: a slice of a company, quoted as a price "
            "per share. <bookmark mark='a'/> A bond: a loan that pays coupons and then its face value. Traders quote "
            "it as a price per hundred of face value, or as the yield that price implies; Part eighteen builds the "
            "arithmetic. <bookmark mark='b'/> A future: an agreement to trade later at a price fixed now, settled "
            "every single day, which is why it needs margin. <bookmark mark='c'/> A swap: two parties exchange cash "
            "flows, typically a fixed interest rate against a floating one, and the quote is that fixed rate. "
            "<bookmark mark='d'/> An option: a right without an obligation, quoted in dollars, or, as Part ten showed, "
            "in implied volatility. <bookmark mark='e'/> And an exchange-traded fund: a basket that trades like a share, "
            "whose price is kept close to the value of what it holds by market makers, as Part thirty-eight shows."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(foot))
            for i, mark in enumerate("abcde", start=2):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i], shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def notional(self):
        d = definition_card(r"Notional", r"The size a derivative refers to, not its value. A swap on \$100 million "
                            r"notional exchanges interest computed on \$100 million, but its value may be a few "
                            r"hundred thousand; a future on \$1 million of an index can be held with \$50{,}000 of "
                            r"margin.", width=9.6, color=QC.IDEA).shift(UP * 1.0)
        lev = MathTex(r"\text{leverage} = \frac{\text{notional exposure}}{\text{equity (margin)}}", font_size=44,
                      color=QC.HOUSE).next_to(d, DOWN, buff=0.6)
        with self.voiceover(
            "One word to keep straight: notional. A derivative refers to a size, the notional, which is not its value. "
            "A swap on a hundred million dollars exchanges interest on a hundred million, but may be worth a few "
            "hundred thousand. A future on a million dollars of an index can be held with fifty thousand of "
            "collateral. <bookmark mark='a'/> The ratio of exposure to the money put up is leverage, and leverage "
            "is what turns the plumbing of this part into a matter of survival, as chapter four will show on a real "
            "crash."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(lev))
        self.wait(0.4)
        self.clear_scene()
