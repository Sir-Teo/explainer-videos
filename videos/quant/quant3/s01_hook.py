from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import PART, PRICE, VALUE, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        s = load("shiller")
        self.title_card()
        self.shiller(s)
        self.era()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What is a share a claim on?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part three. Value, accounting and the firm. Parts one and two treated a price as a number that moves "
            "and a thing that trades. But a share is a claim on something: a slice of a company's future cash. If "
            "prices are fair, they should be the value of that cash today. Are they?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def shiller(self, s):
        t = np.asarray(s["t"])
        P, ps, D = np.asarray(s["price"]), np.asarray(s["pstar"]), np.asarray(s["div"])
        lo, hi = np.log10(min(P.min(), ps.min()) * 0.8), np.log10(max(P.max(), ps.max()) * 1.2)
        g = axes([1871, 2021], [lo, hi], x_length=6.6, y_length=4.8, ylabel=r"S\&P composite, in 2020 dollars (log scale)",
                 xticks=[1880, 1920, 1960, 2000], yticks=[2, 3], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: rf"{10 ** v:,.0f}".replace(",", "{,}"), font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lp = curve(ax, t, np.log10(P), PRICE, stroke_width=2.5)
        n = len(t)
        k = ValueTracker(n - 1.0)

        def built():
            i = int(np.clip(np.floor(k.get_value()), 0, n - 1))
            pts = [ax.c2p(a, np.log10(b)) for a, b in zip(t[i:], ps[i:])]
            if len(pts) < 2:
                pts = pts + pts
            return VMobject(stroke_width=4, stroke_color=VALUE).set_points_as_corners(pts)

        def cursor():
            i = int(np.clip(np.floor(k.get_value()), 0, n - 1))
            p = ax.c2p(t[i], np.log10(ps[i]))
            bar_h = 0.9 * D[i] / D.max()
            bar = Rectangle(width=0.06, height=max(bar_h, 0.02), stroke_width=0, fill_color=QC.GAIN,
                            fill_opacity=0.9).move_to(ax.c2p(t[i], lo), aligned_edge=DOWN)
            yr = label(rf"{int(t[i])}", font_size=20, color=VALUE).next_to(p, UP, buff=0.12)
            return VGroup(glow_dot(p, color=VALUE, radius=0.06), bar, yr)

        line_ps = always_redraw(built)
        cur = always_redraw(cursor)
        rec = cmath(r"p^*_t", r"=", r"\frac{p^*_{t+1} + D_t}{1 + r}", font_size=36,
                    colors={r"p^*_t": VALUE}).to_edge(RIGHT, buff=0.8).shift(UP * 2.5)
        rec_why = why(r"walk backwards from 2020: each year, add that year's dividend and discount one year", 20)
        rec_why.next_to(rec, DOWN, buff=0.15).align_to(rec, LEFT)
        if rec_why.get_right()[0] > 6.8:
            rec_why.shift(LEFT * (rec_why.get_right()[0] - 6.8))
        leg = legend([(PRICE, r"the real price"), (VALUE, r"$p^*$: the present value of the dividends actually paid")],
                     font_size=20).to_edge(RIGHT, buff=0.35).shift(UP * 0.6)
        res = VGroup(
            label(r"how much each moves in a year:", font_size=24, color=GREY_A),
            MathTex(rf"\text{{price}}\ {100 * s['sd_dprice']:.1f}\%\qquad p^*\ {100 * s['sd_dpstar']:.1f}\%", font_size=34),
            MathTex(rf"\text{{years with a move above 20\%:}}\ {s['big_moves']}\ \text{{vs}}\ {s['big_moves_pstar']}",
                    font_size=28),
            wrapped_label(r"Shiller (1981), ``Do stock prices move by too much to be justified by subsequent changes in "
                          r"dividends?''", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.4)
        src = real_data(rf"Shiller's data, 1871--2020; discount rate {100 * s['r']:.1f}\% real, the average return; "
                        r"$p^*$ in 2020 starts from that year's price")
        with self.voiceover(
            "In 1981 Robert Shiller asked that question with a century of data; here it is with a century and a half. "
            "Start from the end. <bookmark mark='a'/> Suppose that in 2020 we knew the price and every dividend ever paid. "
            "Walk backwards a year at a time: last year's value is this year's plus the year's dividend, discounted one year at "
            "the market's average return. Each green bar is a dividend dropping into the sum. The gold line is what the market "
            "was worth to someone who knew the future dividends: Shiller's p star. <bookmark mark='b'/> Now the actual price. If "
            "prices were the best forecasts of p star, they should move less than it, as a forecast moves less than what it "
            f"forecasts. Instead the price moves {s['ratio_changes']:.0f} times as much from year to year: in {s['big_moves']} "
            "years it moved more than twenty percent, and p star never did. <bookmark mark='c'/> Either discount rates move a "
            "great deal, or prices move for reasons other than dividends. The debate shared the 2013 Nobel prize between "
            "Shiller, Eugene Fama and Lars Peter Hansen, and it runs through this part."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(rec))
            vo.wait_until("a")
            self.add(line_ps, cur)
            self.play(FadeIn(rec_why))
            self.play(k.animate.set_value(0), run_time=14.0, rate_func=linear)
            line_ps.clear_updaters()
            self.remove(cur)
            self.play(FadeIn(leg[1]), FadeOut(rec_why))
            vo.wait_until("b")
            self.play(Create(lp), FadeIn(leg[0]), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(r) for r in res[:3]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.4)
        self.clear_scene()

    def era(self):
        strip = timeline(lit=(1934, 1958, 1968, 1974, 1996)).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=36).to_edge(UP, buff=0.5)
        pac = label(r"1494: Luca Pacioli writes down double-entry bookkeeping, in Venice", font_size=22,
                    color=GREY_A).next_to(head, DOWN, buff=0.3)
        late = label(r"2001: Enron \quad 2009: every filing machine-readable (XBRL)", font_size=22,
                     color=QC.CRISIS).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "How we got here. The books came first: double-entry bookkeeping was written down in Venice by Luca Pacioli in 1494, "
            "and every statement in this part still balances by his rule. <bookmark mark='a'/> In 1934, after the crash, Benjamin "
            "Graham and David Dodd taught investors to read those statements, and in 1938 John Burr Williams wrote that a share is "
            "worth its discounted dividends. In 1958 Franco Modigliani and Merton Miller proved that how a firm is financed does not "
            "change that value, in a perfect market. <bookmark mark='b'/> In 1968 Ray Ball and Philip Brown showed that prices "
            "react to earnings; in 1974 Robert Merton priced a firm's equity as an option. In 1996 Richard Sloan showed that the "
            "market misread one part of earnings, and accounting became a source of trading signals. <bookmark mark='c'/> And in "
            "2001 Enron showed what happens when the numbers themselves are false. Since 2009 every American filing has been "
            "machine-readable, so this part can rebuild much of that history from the source."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pac))
            vo.wait_until("a")
            self.play(FadeIn(strip[:-2]), FadeIn(strip.leaders[:2]), FadeIn(strip.labels[:2]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(strip.leaders[2:]), FadeIn(strip.labels[2:]))
            vo.wait_until("c")
            self.play(FadeIn(late))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Time value, IRR and the growing perpetuity; the duration of a stock",
            r"The three statements as one double-entry machine; accruals; filings as point-in-time data",
            r"Discounted cash flow, the cost of capital the market implies, residual income, multiples",
            r"Modigliani and Miller, payout, and equity as a call on the firm",
            r"Earnings announcements and the drift; accounting signals that became factors, and their decay",
            r"Merger arbitrage, forensic accounting, the industry, and machines that read statements",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            "The plan. The arithmetic of time value, and why a stock behaves like a very long bond. The three financial statements, "
            "run as one machine, the accruals that separate earnings from cash, and the filings themselves as data with two dates. "
            "Valuation: discounted cash flow, the return the market's price implies, residual income and multiples, and Campbell "
            "and Shiller's identity. Capital structure and payout, and equity seen as an option. Earnings announcements, and two "
            "hundred accounting and price signals measured before and after they were published. Then merger arbitrage, the "
            "forensic screens, the firms that value companies for a living, and a model trained to forecast earnings."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part extends the data desk with a fundamentals store loaded from real filings. "
            "<bookmark mark='a'/> Its rule: a number is known from the day it was published, not the day the quarter ended."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
