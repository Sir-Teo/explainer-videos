from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import IMP, LOSS, PART, load


def ts_day(d) -> str:
    import datetime as _dt
    d = int(d)
    return _dt.date(d // 10000, d // 100 % 100, d % 100).strftime("%d %B").lstrip("0")


class LTCM(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.vix(load("ltcm98"))
        self.lesson()

    def card(self):
        c = chapter_card(17, r"The Nobel, and then LTCM", r"What does a perfect hedge assume?", lit=(1997, 1998),
                         part=PART)
        with self.voiceover("Chapter seventeen. The Nobel, and then LTCM."):
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
            r"as partners. Convergence trades in bonds and swaps, merger arbitrage, and short volatility: long-dated "
            r"equity-index options, sold in such size that, as Lowenstein reported, traders called it the central "
            r"bank of volatility.",
            numbers=[(r"\sim 28{:}1", r"balance-sheet leverage, end of 1997"),
                     (r"> \$1\,\text{tn}", r"notional derivatives, end of 1997"),
                     (r"\sim 90\%", r"of its capital lost, January to September 1998")],
            source=r"public record: GAO (1999); McDonough and Greenspan, testimony of 1 October 1998; "
                   r"Lowenstein (2000)",
            width=7.0, font_size=24)
        VGroup(nobel, firm).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.2)
        if VGroup(nobel, firm).width > 13.4:
            VGroup(nobel, firm).scale_to_fit_width(13.4).move_to(UP * 0.2)
        with self.voiceover(
            "In October 1997 Merton and Scholes received the Nobel prize. Both were partners in a hedge fund, "
            "Long-Term Capital Management, founded in 1994 by John Meriwether, who had run the bond-arbitrage group "
            "at Salomon Brothers. <bookmark mark='a'/> Its trades were hedged spreads: buy a cheap bond, sell an "
            "expensive near-identical one, and wait for the prices to converge. It also sold volatility, long-dated "
            "index options, in such size that, as Roger Lowenstein reported, other traders called it the central "
            "bank of volatility. At the end of 1997 its balance sheet was about twenty-eight times its capital, "
            "with more than a trillion dollars of derivatives on top, by the General Accounting Office's "
            "count. <bookmark mark='b'/> In August 1998 Russia defaulted. Investors everywhere fled to the most "
            "liquid assets; many convergence positions moved against LTCM together, and implied "
            "volatilities jumped. By the end of August it had lost more than half its capital, and by September "
            "almost ninety percent."
        ) as vo:
            self.play(FadeIn(nobel, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(firm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(firm, color=QC.CRISIS, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vix(self, v):
        from datetime import date

        d = np.asarray(v["date"], int)
        x = np.asarray(v["vix"], float)
        day = np.array([date(int(a) // 10000, int(a) // 100 % 100, int(a) % 100).timetuple().tm_yday for a in d])
        g = axes([1, 365], [10, 50], x_length=8.6, y_length=2.8, ylabel=r"VIX, 1998", xticks=[1, 182, 365],
                 yticks=[20, 30, 40], xfmt=lambda v_: {1: "Jan", 182: "Jul", 365: "Dec"}.get(int(v_), ""), font_size=18)
        g.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.7)
        b = axes([1, 365], [-30, 5], x_length=8.6, y_length=2.4, ylabel=r"short 1 vega per point",
                 xticks=[1, 182, 365], yticks=[-25, 0], xfmt=lambda v_: {1: "Jan", 182: "Jul", 365: "Dec"}.get(int(v_), ""),
                 font_size=18).next_to(g, DOWN, buff=0.45).align_to(g, LEFT)
        k = ValueTracker(1)
        book = np.asarray(v["book"], float)
        j0 = int(np.searchsorted(d, v["jul1_date"]))
        line = always_redraw(lambda: curve(g.ax, day[:max(int(k.get_value()), 2)], x[:max(int(k.get_value()), 2)],
                                           IMP, stroke_width=3))
        bl = always_redraw(lambda: curve(b.ax, day[j0:max(int(k.get_value()), j0 + 2)],
                                         np.clip(book[j0:max(int(k.get_value()), j0 + 2)], -30, 5), LOSS,
                                         stroke_width=3))
        nums = VGroup(MathTex(rf"1\ \text{{July}}:\ {v['jul1']:.1f}", font_size=30, color=IMP),
                      MathTex(rf"\text{{peak ({ts_day(v['peak_date'])}):}}\ {v['peak']:.1f}", font_size=30,
                              color=IMP)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        ill = wrapped_label(r"illustrative: the VIX is a 30-day index; LTCM's options were long-dated, and their "
                            r"volatilities moved less", 3.6, 20, GREY_B).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
        src = note(r"FRED: VIXCLS (Cboe), later-methodology historical backcast", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            f"""This is the Cboe VIXCLS historical series for 1998, reconstructed under the later S and P five hundred methodology. It differs from the contemporary index now called VXO. It reads {v['jul1']:.0f} on July first. <bookmark mark='a'/> Its peak is {v['peak']:.0f}. Below is an illustrative constant short-vega mark per volatility point, excluding theta, convexity, term structure and funding. It is not LTCM's actual option book or return. Volatility increases can produce losses and margin demands, with the outcome depending on the contract and the rest of the portfolio."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(b), FadeIn(src))
            self.add(line, bl)
            self.play(k.animate.set_value(j0), run_time=max(vo.until("a") - 0.5, 2.0), rate_func=linear)
            self.play(k.animate.set_value(len(d)), FadeIn(nums), run_time=5, rate_func=linear)
            line.clear_updaters()
            bl.clear_updaters()
            self.play(FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lesson(self):
        card = crisis_card(r"23 September 1998", r"The rescue",
                           r"The Federal Reserve Bank of New York convened fourteen banks and securities firms, which "
                           r"put about \$3.6 billion into the fund to take it over and unwind it slowly, rather than "
                           r"let its positions be dumped on markets already in distress.", width=7.4, font_size=25)
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
            "On the twenty-third of September the Federal Reserve Bank of New York gathered fourteen banks and "
            "securities firms, which put about three and a half billion dollars into the fund, took it over, and "
            "unwound it slowly. Most of the spreads did converge, eventually. Pause and predict: a hedge is "
            "riskless if you can trade continuously. What else must be true? "
            "<bookmark mark='a'/> What broke were the assumptions under every hedge in this part: that you can keep "
            "trading, that you can fund the position until it converges, and that the others are not all doing "
            "the same trade. 1987 broke the first. 1998 broke all three. Part forty-one tells the story with the "
            "data: margin spirals, fire sales, and why liquidity and financing require explicit models beyond this replication formula."
            " Next: the formula at work today."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in lessons], lag_ratio=0.4, run_time=3))
            self.play(FadeIn(fwd))
        self.wait(0.4)
        self.clear_scene()
