from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, CURV, GOOD, LEVEL, PART, SLOPE, ask, illustration, load


class RV(VoiceoverScene):
    def construct(self):
        f = load("fly")
        self.card()
        self.salomon()
        self.build(f)
        self.rule(f)
        self.verdict(f)

    def card(self):
        c = chapter_card(16, r"Relative value: the butterfly", r"Can you trade the curve's shape and nothing else?",
                         part=PART)
        with self.voiceover("Chapter sixteen. Relative value: trading the curve's shape."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def salomon(self):
        fc = firm_card(r"Salomon Brothers",
                       r"its bond arbitrage group, led by John Meriwether, bought cheap Treasuries and sold rich ones of "
                       r"nearly the same maturity, hedged and leveraged, and became famous for it in the 1980s. "
                       r"In 1991 its government desk was found to have submitted false bids to get around the Treasury's "
                       r"limit of 35\% of any auction per bidder; in the May 1991 two-year note auction Salomon "
                       r"controlled more than 90\% of the issue",
                       numbers=[(r"35\%", r"limit per bidder"), (r">90\%", r"of the May 1991 two-year notes"),
                                (r"\$290\,\text{m}", r"fines and restitution, 1992")],
                       source=r"SEC and DOJ settlements (1992); Federal Reserve Bank of Cleveland (1992)", width=6.6,
                       font_size=21).to_edge(LEFT, buff=0.5)
        after = VGroup(
            wrapped_label(r"Meriwether left Salomon in 1991. In 1994 he founded Long-Term Capital Management with "
                          r"several of the arbitrage group, and Robert Merton and Myron Scholes as partners", 5.4, 20,
                          GREY_A),
            wrapped_label(r"its trades were this chapter's, at scale: Part 41 tells how they ended in 1998", 5.4, 20,
                          QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The firm file for this chapter is Salomon Brothers. In the 1980s its bond arbitrage group, led by John "
            "Meriwether, bought Treasuries that looked cheap against nearly identical ones, sold the rich ones, hedged "
            "the rest, and levered the difference; the group became famous for it. <bookmark mark='a'/> In 1991 the firm's government bond desk was "
            "caught submitting false bids to get around the Treasury's rule that no bidder may take more than "
            "thirty-five percent of an auction; in the May two-year auction, Salomon ended up controlling more than "
            "ninety percent. The settlements in 1992 came to two hundred and ninety million dollars. "
            "<bookmark mark='b'/> Meriwether resigned. In 1994 he founded Long-Term Capital Management, with much of "
            "the old group and two future Nobel laureates. Part forty-one tells how it ended."
        ) as vo:
            self.play(FadeIn(fc))
            vo.wait_until("a")
            self.play(Indicate(fc, color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(after))
        self.wait(0.4)
        self.clear_scene()

    def build(self, f):
        w = np.asarray(f["weights"])
        rows = [cmath(r"F_t", r"=", rf"{w[0]:.2f}\,y^{{(2)}}_t + y^{{(5)}}_t {w[2]:+.2f}\,y^{{(10)}}_t", font_size=42,
                      colors={r"F_t": CURV}),
                cmath(r"\ell^\top w", r"=", r"0,\qquad s^\top w = 0", font_size=42,
                      colors={r"\ell^\top w": LEVEL}),
                cmath(r"\Delta F_t", r"\approx", r"(c^\top w)\,\Delta s_3 + \text{noise}", font_size=42,
                      colors={r"\Delta F_t": CURV})]
        whys = [why(r"a butterfly: long the 5-year belly, short the 2-year and 10-year wings, in DV01 units"),
                why(r"wings chosen so the trade has no exposure to the level and slope factors of chapter 10, "
                    r"estimated on 1990--2020 only (the House's \texttt{fly\_weights})"),
                why(r"what is left is curvature, and whatever the three factors miss")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "The cleanest version of that business is the butterfly. Own the five-year belly, and sell the two-year and "
            "ten-year wings against it. <bookmark mark='a'/> Choose the wing sizes so the trade has no exposure to the "
            f"level or the slope factor of chapter ten: here {abs(w[0]):.2f} of the two-year and {abs(w[2]):.2f} of the "
            "ten-year for each unit of the five-year, fitted on data that ends in 2020. <bookmark mark='b'/> What is "
            "left moves only with curvature and the noise the factors miss. If that combination is mean-reverting, buy "
            "it when it is low and sell it when it is high."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def rule(self, f):
        r = f["rule"]
        card = VGroup(
            label(r"Registered before the hold-out was opened", font_size=26, color=QC.HOUSE),
            label(r"signal: $z$ = the fly minus its 250-day mean, over its 250-day standard deviation", font_size=21),
            label(r"enter against the sign when $|z| > 1$; exit when $z$ crosses 0", font_size=21),
            label(rf"cost: {r['cost_bp']} bp of the fly per change of position; one configuration, no tuning",
                  font_size=21),
            label(r"in sample: 1991--2020.\ \ Sealed hold-out: 2021--2025, opened once", font_size=21, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6)
        box = SurroundingRectangle(card, color=QC.HOUSE, buff=0.25, corner_radius=0.12)
        foot = wrapped_label(rf"the trial counter: one more strategy tried, {f['trials']} in the series", 12, 22,
                             QC.HOUSE).next_to(box, DOWN, buff=0.5)
        with self.voiceover(
            "The House's rule says a strategy is written down, with every parameter, before anyone looks at the data it "
            "will be judged on. So here is the rule, registered first: a z-score of the fly against its own trailing "
            "year; enter against it beyond one standard deviation; exit when it crosses zero; half a basis point of "
            "cost per trade. <bookmark mark='a'/> One configuration, no tuning, and the last five years sealed. The "
            f"trial counter goes up by one, to {f['trials']}."
        ) as vo:
            self.play(Create(box), FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self, f):
        t, F, cum = np.asarray(f["t"]), np.asarray(f["F"]), np.asarray(f["cum"])
        keep = t >= 1990
        t, F, cum = t[keep], F[keep], cum[keep] - cum[keep][0]
        ok = np.isfinite(F)
        top = axes([1990, 2026], [np.nanmin(F) - 5, np.nanmax(F) + 5], x_length=8.6, y_length=2.2,
                   ylabel=r"the fly, bp", xticks=[], yticks=[], font_size=13)
        cmin, cmax = float(np.nanmin(cum)), float(np.nanmax(cum))
        bot = axes([1990, 2026], [cmin - 10, cmax + 10], x_length=8.6, y_length=2.6, xlabel=r"year",
                   ylabel=r"cumulative P\&L, bp of the fly", xticks=[1990, 2000, 2010, 2020],
                   yticks=[round(cmin, -1), 0, round(cmax, -1)], font_size=13)
        VGroup(top, bot).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(LEFT, buff=0.6)
        lf = curve(top.ax, t[ok], F[ok], CURV, stroke_width=2)
        lc = curve(bot.ax, t[np.isfinite(cum)], cum[np.isfinite(cum)], WHITE, stroke_width=2.5)

        def shade(g):
            ax = g.ax
            x0, x1 = ax.c2p(2021, 0)[0], ax.c2p(2026, 0)[0]
            y0, y1 = ax.get_bottom()[1], ax.get_top()[1]
            return Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=QC.IDEA,
                             fill_opacity=0.12).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        sh = VGroup(shade(top), shade(bot))
        i, o, gi, go = f["in"], f["out"], f["gross_in"], f["gross_out"]
        side = VGroup(
            label(r"in sample, 1991--2020", font_size=20, color=GREY_A),
            MathTex(rf"\text{{Sharpe}}\ {i['sharpe']:+.2f}\ \ (\text{{gross}}\ {gi['sharpe']:+.2f})", font_size=26),
            label(r"hold-out, 2021--2025", font_size=20, color=QC.IDEA),
            MathTex(rf"\text{{Sharpe}}\ {o['sharpe']:+.2f}\ \ (\text{{gross}}\ {go['sharpe']:+.2f})", font_size=26,
                    color=BAD),
            wrapped_label(rf"half-life of the fly: {f['hl_in']:.0f} trading days before 2021, {f['hl_out']:.0f} after. A "
                          r"one-year z-score expects it to revert within months", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is the fly since 1990, and what the rule made. The shaded years are the hold-out. "
            "<bookmark mark='a'/> It lost money in sample, with a Sharpe ratio of "
            f"{i['sharpe']:.2f}, and lost more in the hold-out: {o['sharpe']:.2f}. Without costs it still loses, so "
            "fees are not the story. <bookmark mark='b'/> The reason is in the fly's own dynamics: its half-life is "
            f"about {f['hl_in']:.0f} trading days. It does revert, but over years, while this rule bets on months, and "
            "keeps entering against moves that keep going. <bookmark mark='c'/> An honest negative result, and a common "
            "one. Salomon's traders were not running z-scores; they knew which bonds were cheap and why: an auction, a "
            "squeeze in repo, an index rebalance. Without that knowledge, a factor-neutral spread is not an edge."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(sh), Create(lf), run_time=2)
            self.play(Create(lc), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
            vo.wait_until("c")
            self.wait(0.3)
        q = ask(r"the fly is level- and slope-neutral. Name two risks it still carries.")
        with self.voiceover("The fly is neutral to level and slope. Name two risks it still carries."):
            self.play(FadeIn(q))
        self.add(illustration(r"GSW zero yields at 2, 5 and 10 years; weights from PCA on 1990--2020"))
        self.wait(0.5)
        self.clear_scene()
