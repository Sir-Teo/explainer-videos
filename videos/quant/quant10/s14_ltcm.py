from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import IMP, LOSS, PART


class LTCM(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.lesson()

    def card(self):
        c = chapter_card(13, r"The Nobel, and then LTCM", r"What does a perfect hedge assume?", lit=(1997, 1998),
                         part=PART)
        with self.voiceover("Chapter thirteen. The Nobel, and then LTCM."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def story(self):
        nobel = history_card(1997, r"14 October: the Nobel prize in economics",
                             r"to Robert Merton and Myron Scholes, ``for a new method to determine the value of "
                             r"derivatives''", width=6.0, font_size=25)
        firm = firm_card(
            r"Long-Term Capital Management",
            r"Founded 1994 by John Meriwether, from Salomon Brothers' bond-arbitrage desk, with Merton and Scholes "
            r"as partners. Convergence trades in bonds and swaps, merger arbitrage, and short volatility: it sold "
            r"long-dated equity-index options in such size that traders called it the central bank of volatility.",
            numbers=[(r"\sim 40\%", r"returns after fees, 1995 and 1996"),
                     (r"\sim 25{:}1", r"balance-sheet leverage, early 1998"),
                     (r"\$4.6\,\text{bn}", r"lost, 1998")],
            source=r"public record: President's Working Group on Financial Markets (1999); Lowenstein (2000)",
            width=7.0, font_size=24)
        VGroup(nobel, firm).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.2)
        if VGroup(nobel, firm).width > 13.4:
            VGroup(nobel, firm).scale_to_fit_width(13.4).move_to(UP * 0.2)
        with self.voiceover(
            "In October 1997 Merton and Scholes received the Nobel prize. Both were partners in a hedge fund, "
            "Long-Term Capital Management, founded in 1994 by John Meriwether, who had run the bond-arbitrage group "
            "at Salomon Brothers. <bookmark mark='a'/> Its trades were hedged spreads: buy a cheap bond, sell an "
            "expensive near-identical one, and wait for the prices to converge. It also sold volatility, long-dated "
            "index options, in such size that other traders called it the central bank of volatility. It earned "
            "about forty percent a year after fees in 1995 and 1996, on a balance sheet some twenty-five times its "
            "capital. <bookmark mark='b'/> In August 1998 Russia defaulted. Investors everywhere fled to the most "
            "liquid assets; every spread LTCM was betting would narrow widened instead, all at once, and implied "
            "volatilities jumped. By September the fund had lost four and a half billion dollars, most of its "
            "capital."
        ) as vo:
            self.play(FadeIn(nobel, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(firm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(firm, color=QC.CRISIS, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lesson(self):
        card = crisis_card(r"23 September 1998", r"The rescue",
                           r"The Federal Reserve Bank of New York convened fourteen banks, which put \$3.6 billion "
                           r"into the fund to take it over and unwind it slowly, rather than let its positions be "
                           r"dumped on markets already in distress.", width=7.4, font_size=25)
        card.to_edge(UP, buff=0.5)
        lessons = VGroup(
            label(r"What the hedge assumes, and 1998 broke:", font_size=28, color=IMP),
            label(r"you can always keep trading, at a price near the last one", font_size=26, color=GREY_A),
            label(r"you can always fund the position until it converges", font_size=26, color=GREY_A),
            label(r"the others are not all doing the same trade", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(card, DOWN, buff=0.5)
        fwd = label(r"the full story, with the data: Part 41, Leverage, Liquidity and Crises", font_size=24,
                    color=LOSS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "On the twenty-third of September the Federal Reserve Bank of New York gathered fourteen banks, which "
            "put three point six billion dollars into the fund, took it over, and unwound it slowly. The models "
            "were not wrong about prices converging; most of the spreads did converge, eventually. "
            "<bookmark mark='a'/> What broke were the assumptions under every hedge in this part: that you can keep "
            "trading, that you can fund the position until it converges, and that the others are not all doing "
            "the same trade. 1987 broke the first. 1998 broke all three. Part forty-one tells the story with the "
            "data: margin spirals, fire sales, and why liquidity is the risk factor no formula prices."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in lessons], lag_ratio=0.4, run_time=3))
            self.play(FadeIn(fwd))
        self.wait(0.4)
        self.clear_scene()
