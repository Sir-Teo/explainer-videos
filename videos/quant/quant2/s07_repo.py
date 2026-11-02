from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, LOSS, PART, RATE, TRADE, node

HAIRCUTS = [(r"US Treasury bills and notes", 0.02), (r"investment-grade corporate bonds", 0.08),
            (r"large-company shares", 0.20), (r"small-company shares", 0.35), (r"Bitcoin, on a crypto lender", 0.50)]


class Repo(VoiceoverScene):
    def construct(self):
        self.card()
        self.repo()
        self.haircuts()
        self.prime()

    def card(self):
        c = chapter_card(6, r"Repo, lending and prime brokers", r"Where does the money for leverage come from?",
                         lit=(2021,), part=PART)
        with self.voiceover("Chapter six. Repo, securities lending and prime brokers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def repo(self):
        a, b = node(r"a fund", TRADE, width=2.4), node(r"a money fund or bank", CASH, width=2.9)
        VGroup(a, b).arrange(RIGHT, buff=4.6).shift(UP * 1.4)
        top = Arrow(a.get_right() + UP * 0.2, b.get_left() + UP * 0.2, buff=0.1, color=RATE, stroke_width=3)
        bot = Arrow(b.get_left() + DOWN * 0.2, a.get_right() + DOWN * 0.2, buff=0.1, color=CASH, stroke_width=3)
        tl = label(r"today: \$102 of Treasuries", font_size=22, color=RATE).next_to(top, UP, buff=0.08)
        bl = label(r"today: \$100 of cash", font_size=22, color=CASH).next_to(bot, DOWN, buff=0.08)
        back = label(r"tomorrow: the cash back, plus interest at the repo rate; the bonds back", font_size=24,
                     color=GREY_A).next_to(VGroup(a, b), DOWN, buff=1.2)
        d = definition_card(r"Repo (sale and repurchase)", r"A loan of cash against collateral, written as a sale and "
                            r"a promise to buy back. The collateral is worth more than the cash: the difference is "
                            r"the haircut. SOFR, the benchmark US interest rate, is the average overnight rate on "
                            r"Treasury repo.", width=10.0, color=RATE, font_size=23).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Most leverage in the financial system is funded overnight, by repo. A fund that owns Treasury bonds "
            "hands them to a lender, a money-market fund or a bank, and receives cash today; tomorrow it pays the "
            "cash back with interest and gets its bonds back. <bookmark mark='a'/> Legally it is a sale and a "
            "promise to repurchase; economically it is a secured loan. The collateral is worth a little more than "
            "the cash: that gap is the haircut. <bookmark mark='b'/> The rate on these overnight Treasury loans is "
            "SOFR, the benchmark interest rate of the United States, and chapter seven shows what happened the day "
            "it more than doubled."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b))
            self.play(GrowArrow(top), FadeIn(tl), GrowArrow(bot), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(back))
            vo.wait_until("b")
            self.play(FadeIn(d, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def haircuts(self):
        rows = [VGroup(label(r"collateral", font_size=24, color=GREY_A), label(r"haircut", font_size=24, color=GREY_A),
                       label(r"most leverage", font_size=24, color=GREY_A))]
        cells = list(rows[0])
        for name, h in HAIRCUTS:
            r_ = [label(name, font_size=24), MathTex(rf"{100 * h:.0f}\%", font_size=30, color=RATE),
                  MathTex(rf"{1 / h:.0f}\times", font_size=30, color=LOSS if h >= 0.35 else QC.HOUSE)]
            cells += r_
            rows.append(VGroup(*r_))
        grid = VGroup(*cells).arrange_in_grid(len(HAIRCUTS) + 1, 3, buff=(1.0, 0.3), col_alignments="lrr").shift(UP * 0.6)
        eq = MathTex(r"\text{most leverage} = \frac{1}{\text{haircut}}", font_size=40, color=QC.HOUSE)
        eq.next_to(grid, DOWN, buff=0.5)
        why_ = wrapped_label(r"each dollar of collateral funds $1 - h$ dollars, which buys more collateral, which funds "
                             r"more: the series $1 + (1-h) + (1-h)^2 + \dots = 1/h$; raise haircuts in a panic and "
                             r"everyone must sell at once (Part 41)", 11.6, 22, GREY_A).next_to(eq, DOWN, buff=0.3)
        foot = note(r"haircuts are typical levels, for illustration; they vary by lender, borrower and day", font_size=17)
        foot.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The haircut is a leverage limit. A dollar of collateral with a two percent haircut borrows ninety-eight "
            "cents, which buys more collateral, which borrows again: the series sums to one over the haircut. Two "
            "percent on Treasuries allows fifty times leverage. <bookmark mark='a'/> Riskier collateral gets bigger "
            "haircuts: a fifth on large-company shares, five times; a half on Bitcoin, two. <bookmark mark='b'/> "
            "And haircuts move. In a panic lenders raise them, and every borrower in the market must cut leverage "
            "at the same moment, by selling the same assets. That spiral is Part forty-one."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), Write(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:]], lag_ratio=0.4), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(why_))
        self.wait(0.4)
        self.clear_scene()

    def prime(self):
        d1 = definition_card(r"Prime broker", r"A bank's division that serves hedge funds: it lends them cash and "
                             r"securities, holds their assets, clears their trades, and nets their margin across "
                             r"everything they hold with it.", width=5.8, color=TRADE, font_size=22)
        d2 = definition_card(r"Total return swap", r"The bank holds the shares; the fund receives their gains and "
                             r"pays their losses plus a financing rate. The fund gets the exposure without owning "
                             r"anything, and without having to disclose it as a shareholder.", width=5.8, color=QC.IDEA,
                             font_size=22)
        pair = VGroup(d1, d2).arrange(RIGHT, buff=0.4, aligned_edge=UP).shift(UP * 1.2)
        c = crisis_card(r"March 2021", r"Archegos Capital Management",
                        r"A family office with concentrated positions in a few stocks, built through total return "
                        r"swaps with several prime brokers at once, none of which saw the whole. When the stocks fell "
                        r"it could not meet margin calls; the banks sold, and those that sold last lost most.",
                        stats=[(r"\sim\$5.5\,\text{bn}", r"Credit Suisse's loss"), (r"\sim\$2.9\,\text{bn}", r"Nomura's")],
                        width=11.0, font_size=21).next_to(pair, DOWN, buff=0.4)
        src = note(r"as the banks reported; Credit Suisse's own investigation (July 2021); the full story in Part 41",
                   font_size=17).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Hedge funds borrow through prime brokers: divisions of large banks that lend them cash and securities, "
            "hold their assets, clear their trades, and net their margin across everything they hold there. "
            "<bookmark mark='a'/> Much of that exposure is synthetic. In a total return swap the bank owns the "
            "shares, and the fund receives their gains and pays their losses plus a financing charge. The fund has "
            "the exposure without owning anything, and without appearing as a shareholder. <bookmark mark='b'/> In "
            "March 2021 a family office called Archegos had built enormous positions in a handful of stocks this way, "
            "through several prime brokers at once, none of which saw the whole. When the stocks fell it could not "
            "meet its margin calls, the banks raced to sell, and the last to sell lost most: about five and a half "
            "billion dollars at Credit Suisse and nearly three at Nomura, as the banks reported. Part forty-one "
            "tells it in full."
        ) as vo:
            self.play(FadeIn(d1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(d2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()
