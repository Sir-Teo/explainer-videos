from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, SPY_C, TREND_C, fit_right, illustration, load


def _years(months, cum):
    md = np.asarray(months)
    w = np.r_[1.0, 1 + np.asarray(cum, float)]
    r = w[1:] / w[:-1] - 1
    return {int(y): float(np.prod(1 + r[md // 100 == y]) - 1) for y in np.unique(md // 100)}


class Smile(VoiceoverScene):
    def construct(self):
        t, th = load("trend"), load("theory")
        self.card()
        self.scatter(t)
        self.why_short()
        self.years(t)
        self.lookback()
        self.march2020(t)
        self.straddle(th)
        self.cost()
        self.blend(t)
        self.question()

    def card(self):
        c = chapter_card(2, r"The smile and the crisis", r"Why does trend following make money when markets crash?",
                         part=PART)
        with self.voiceover("Chapter two. The claim that sells trend following is crisis alpha. Here is the evidence, "
                            "the mechanism, and the price."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def scatter(self, t):
        m, y = 100 * np.asarray(t["smile"]["m"], float), 100 * np.asarray(t["smile"]["t"], float)
        a2, a1, a0 = t["smile"]["fit"]
        g = axes([-25, 25], [-12, 16], x_length=6.6, y_length=4.6, xlabel=r"US stocks' excess return in the quarter, \%",
                 ylabel=r"trend book, \%", xticks=[-20, 0, 20], yticks=[-10, 0, 10], font_size=15)
        g.move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TREND_C, fill_opacity=0.8) for a, b in zip(m, y)])
        xs = np.linspace(-22, 22, 80)
        fit = curve(ax, xs, 100 * (a2 * (xs / 100) ** 2 + a1 * xs / 100 + a0), HURDLE, stroke_width=3)
        worst = np.argsort(m)[:2]
        tags = VGroup(*[label(rf"{m[i]:+.0f}\% $\to$ {y[i]:+.1f}\%", font_size=15, color=GOOD).next_to(
            ax.c2p(m[i], y[i]), UR, buff=0.08) for i in worst])
        txt = wrapped_label(r"each dot a quarter, 2007--2020; the curve a quadratic fit. On the House's 23 funds the "
                            r"curvature is faint, even slightly negative; Part 24 found a clear smile in AQR's 58 futures "
                            r"markets, 1985--2020", 4.0, 16, GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        fit_right(txt)
        with self.voiceover(
            "Each dot is a quarter: the stock market's return across, the trend book's up. <bookmark mark='a'/> In the "
            "two worst quarters for stocks, the last of 2008 and the first of 2020, the trend book made money. "
            "<bookmark mark='b'/> But fit a curve through all fifty-five quarters and the famous smile is faint here, "
            "even slightly bent the wrong way. Part twenty-four found a clear smile in AQR's fifty-eight futures markets "
            "over thirty-five years. Fourteen years of twenty-three funds is not enough to see the shape, though it is "
            "enough to see the crashes."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02))
            vo.wait_until("a")
            self.play(*[Indicate(dots[i], color=GOOD, scale_factor=2.0) for i in worst], FadeIn(tags))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def why_short(self):
        T = 160
        t = np.arange(T)
        price = np.where(t < 60, 100 + 0.15 * t, np.where(t < 120, 109 - 0.55 * (t - 60), 76 + 0.1 * (t - 120)))
        price = price + 1.2 * np.sin(t / 3.0)
        g = axes([0, T], [60, 120], x_length=7.4, y_length=3.0, xlabel=r"days", ylabel=r"price",
                 xticks=[0, 60, 120], yticks=[70, 100], font_size=15).move_to(UP * 0.9 + LEFT * 1.2)
        ax = g.ax
        line = curve(ax, t, price, SPY_C, stroke_width=3)
        sig = np.array([np.sign(price[k] - price[max(0, k - 40)]) for k in t])
        band = VGroup()
        for k in range(0, T - 1):
            col = GOOD if sig[k] > 0 else BAD
            band.add(Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=0.35, fill_color=col, fill_opacity=0.8,
                               stroke_width=0).move_to([ax.c2p(k + 0.5, 60)[0], g.get_bottom()[1] - 0.45, 0]))
        bl = label(r"position: long (green) or short (red), on the sign of the last 40 days", font_size=16,
                   color=GREY_A).next_to(band, DOWN, buff=0.15)
        ill = illustration(r"illustration: a slow decline")
        with self.voiceover(
            "The mechanism is simple. <bookmark mark='a'/> A market rises, and the rule is long. Then it starts to fall. "
            "<bookmark mark='b'/> For a while the rule is still long and loses; once the past return turns negative it "
            "flips short, and rides the rest of the decline down. <bookmark mark='c'/> Crashes that unfold over months, "
            "like 2008 or the bear markets of 1973 and 2000, are what the rule is built for: it needs the crisis to last "
            "longer than its lookback."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in band], lag_ratio=0.01, run_time=2.0), FadeIn(bl))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def years(self, t):
        yt = _years(t["months"], t["cum"]["trend"])
        ys = _years(t["months"], t["cum"]["spy"])
        yrs = [y for y in sorted(yt) if 2008 <= y <= 2020]
        g = axes([2007.4, 2020.6], [-40, 35], x_length=8.4, y_length=4.2, xlabel=r"calendar year",
                 ylabel=r"excess return, \%", xticks=[2008, 2012, 2016, 2020], yticks=[-30, 0, 30],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for y in yrs:
            for off, v, col in ((-0.18, ys[y], SPY_C), (0.18, yt[y], TREND_C)):
                h = 100 * v
                b = Rectangle(width=0.3 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=abs(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]),
                              fill_color=col, fill_opacity=0.85, stroke_width=0)
                b.move_to(ax.c2p(y + off, h / 2))
                bars.add(b)
        leg = legend([(SPY_C, r"US stocks"), (TREND_C, r"trend book")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 2.0)
        fit_right(leg)
        neg = [y for y in yrs if yt[y] < 0]
        with self.voiceover(
            "Year by year. <bookmark mark='a'/> In 2008 the trend book gained while stocks lost "
            f"{abs(100 * ys[2008]):.0f} percent. In 2009, as stocks rebounded {100 * ys[2009]:.0f} percent, it lost: it "
            "was still short when the market turned. <bookmark mark='b'/> Then a decade of small gains and occasional "
            f"losses, in {', '.join(str(y) for y in neg[1:-1])} and {neg[-1]}. No year was a disaster; few were "
            "exciting. That is what holding it feels like."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:4]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[4:]], lag_ratio=0.05))
        self.wait(0.4)
        self.clear_scene()

    def lookback(self):
        cards = VGroup(
            desk_question(r"slow crises", r"2008, 1973--74, 2000--02: months of decline, long enough for a 12-month "
                          r"signal to turn short and stay short; trend's best years", width=12.4, font_size=19),
            desk_question(r"fast crises", r"October 1987, August 2015, February 2018: a crash in days, too fast for any "
                          r"lookback of months; trend is still long when it happens", width=12.4, font_size=19),
            desk_question(r"reversals", r"2009: the market turns while the rule is short, and the rule loses on the way "
                          r"back up; momentum crashes (Daniel and Moskowitz 2016) are the same event in the cross-section",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So the claim needs a qualifier. <bookmark mark='a'/> Trend pays in slow crises, months long, which turn "
            "the signal short and keep it there. <bookmark mark='b'/> It does not pay in crashes of days, such as October "
            "1987, when it is still long as the floor gives way. <bookmark mark='c'/> And it loses in reversals, when "
            "the market turns while it is short: 2009, the same event that Kent Daniel and Tobias Moskowitz called a "
            "momentum crash in the cross-section."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def straddle(self, th):
        rows = [cmath(r"x_t", r"=", r"r_1 + \dots + r_{t-1}", font_size=36, colors={r"x_t": TREND_C}),
                cmath(r"P", r"=", r"\textstyle\sum_t x_t r_t = \tfrac12\Big[\big(\textstyle\sum_t r_t\big)^2 - "
                      r"\textstyle\sum_t r_t^2\Big]", font_size=34, colors={r"P": GOOD}),
                cmath(r"P", r"=", r"\tfrac12\big(S^2 - \mathrm{RV}\big)", font_size=40, colors={r"S^2": HURDLE})]
        whys = [why(r"the purest trend rule: within a block, hold a position equal to the return so far"),
                why(r"an identity, from $(\sum r)^2 = \sum r^2 + 2\sum_{s<t} r_s r_t$: no model, no assumption"),
                why(r"half the squared block return, a straddle's payoff, minus half the realised variance, its "
                    r"premium: proved and measured in the research chapter")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "There is an exact way to see why. <bookmark mark='a'/> Take the purest trend rule: within a block of days, "
            "hold a position equal to the return so far. <bookmark mark='b'/> Its profit is the sum of position times "
            "return, and by a line of algebra that is half the square of the block's total return, minus half the sum "
            "of the squared daily returns. <bookmark mark='c'/> Half the squared return is the payoff of a straddle: it "
            "pays on a big move either way. Half the realised variance is what the straddle costs. Trend following is "
            "long a straddle, financed by the market's own variance, and the research chapter proves what that "
            "implies."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def cost(self):
        cards = VGroup(
            desk_question(r"the premium", r"a straddle's buyer pays when nothing much happens: trend loses in choppy "
                          r"markets, a little at a time, as each small trend reverses", width=12.4, font_size=19),
            desk_question(r"the skew", r"many small losses and a few large gains: positive skewness, the opposite of "
                          r"selling insurance (Chapter 7)", width=12.4, font_size=19),
            desk_question(r"Fung and Hsieh (2001)", r"trend followers' returns are explained by portfolios of lookback "
                          r"straddles on bonds, currencies and commodities: an option replicated by trading", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The straddle explains the experience. <bookmark mark='a'/> Its buyer pays when nothing much happens, so "
            "trend loses in choppy markets, a little at a time. <bookmark mark='b'/> Many small losses and a few large "
            "gains: positive skewness, the mirror image of selling insurance. <bookmark mark='c'/> William Fung and "
            "David Hsieh found exactly this in 2001: trend followers' returns are explained by lookback straddles, "
            "options that pay the largest move over a period, replicated by trading the futures."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def blend(self, t):
        w = np.r_[1.0, 1 + np.asarray(t["cum"]["trend"], float)]
        rt = w[1:] / w[:-1] - 1
        w6 = np.r_[1.0, 1 + np.asarray(t["cum"]["6040"], float)]
        r6 = w6[1:] / w6[:-1] - 1

        def score(r):
            g = np.cumprod(1 + r)
            return r.mean() / r.std() * np.sqrt(12), float(np.min(g / np.maximum.accumulate(g) - 1))
        rows = []
        for k in (0.0, 0.2, 0.4):
            sr, dd = score((1 - k) * r6 + k * rt)
            rows.append((k, sr, dd))
        hx = [-3.0, 0.2, 3.2]
        head = VGroup(label(r"share in the trend book", font_size=18, color=TREND_C), label(r"Sharpe ratio", font_size=18,
                                                                                         color=GREY_B),
                      label(r"worst fall", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for k, sr, dd in rows:
            tab.add(VGroup(MathTex(rf"{100 * k:.0f}\%", font_size=28), MathTex(f"{sr:.2f}", font_size=28),
                           MathTex(rf"{100 * dd:.0f}\%", font_size=28, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label(r"60/40 with part of its capital moved into the trend book, rebalanced monthly, 2007--2020; "
                             r"before fees", 11.0, 17, GREY_A).to_edge(DOWN, buff=0.7)
        sr0, sr1 = rows[0][1], rows[1][1]
        dd0, dd1 = abs(100 * rows[0][2]), abs(100 * rows[1][2])
        with self.voiceover(
            "How investors actually use it: as a diversifier. <bookmark mark='a'/> Move a fifth of a sixty-forty "
            f"portfolio into the trend book, and the Sharpe ratio goes from {sr0:.2f} to {sr1:.2f}, while the worst fall "
            f"shrinks from {dd0:.0f} percent to {dd1:.0f}. <bookmark mark='b'/> With two fifths, the worst fall shrinks "
            "further. A modest return stream that is uncorrelated, and positive in the crash, is worth more in a "
            "portfolio than on its own."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()


    def march2020(self, t):
        m, y = np.asarray(t["smile"]["m"], float), np.asarray(t["smile"]["t"], float)
        md = np.asarray(t["months"])
        qs = np.unique((md // 100) * 10 + ((md % 100) - 1) // 3)
        i = int(np.flatnonzero(qs == 20200)[0])
        cards = VGroup(
            desk_question(r"a fast crash that paid", rf"the first quarter of 2020: stocks {100 * m[i]:+.0f}\%, the trend "
                          rf"book {100 * y[i]:+.1f}\%", width=12.4, font_size=20),
            desk_question(r"why", r"the trends that paid were already in place before the crash: long Treasuries, whose "
                          r"yields had been falling for a year, and short oil and other commodities, already weakening; "
                          r"the equity positions, still long, lost", width=12.4, font_size=19),
            desk_question(r"the lesson", r"crisis alpha comes from whichever markets were already trending the right way; "
                          r"it is diversification across markets, not a forecast of the crash", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "A counter-example worth understanding. <bookmark mark='a'/> The first quarter of 2020 was a crash of weeks, "
            f"not months, yet the trend book made {100 * y[i]:.0f} percent while stocks fell {abs(100 * m[i]):.0f}. "
            "<bookmark mark='b'/> The trends that paid were already in place: long Treasuries, whose yields had been "
            "falling for a year, and short commodities that were already weakening. The equity positions, still long, "
            "lost. <bookmark mark='c'/> Crisis alpha comes from whichever markets were already trending the right way. "
            "It is diversification across markets, not a forecast of the crash."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"over a quarter, a market's daily returns sum to zero, but it swung widely. Did the linear trend "
                       r"rule make or lose money?")
        with self.voiceover(
            "Pause and predict. Over a quarter, a market's daily returns sum to exactly zero, but it swung widely in "
            "between. Did the linear trend rule make money or lose it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
