from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import DEL, IMP, LOSS, OPT, PART, SPOT, load


def datetime_str(d: str) -> str:
    import datetime as _dt
    return _dt.date(int(d[:4]), int(d[4:6]), int(d[6:])).strftime("%d %B %Y").lstrip("0")


def sci_tex(x: float) -> str:
    e = int(np.floor(np.log10(x)))
    m = x / 10 ** e
    return rf"{m:.1f}\times 10^{{{e}}}"


class Crash(VoiceoverScene):
    def construct(self):
        c = load("crash87")
        self.card()
        ins = load("insurance87")
        self.insurance(ins)
        self.replay(ins)
        self.day(c)
        self.after()

    def card(self):
        c = chapter_card(16, r"October 1987", r"What happens when everyone hedges the same way?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter sixteen. October 1987."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def insurance(self, ins):
        xs = np.linspace(70, 130, 241)
        g = axes([70, 130], [0, 1.05], x_length=6.6, y_length=3.6, xlabel=r"index level",
                 ylabel=r"fraction of the portfolio held in stocks", xticks=[80, 100, 120], yticks=[0, 0.5, 1],
                 font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        # a protective put struck at 95, a year out: stocks held = 1 + put delta, as a fraction of value
        sg, rr = ins["sigma"], ins["rate"]
        frac = xs * (1 + bs.greeks(xs, 95.0, 1.0, sg, rr, 0, -1)["delta"]) / (xs + bs.price(xs, 95.0, 1.0, sg, rr, 0, -1))
        line = curve(ax, xs, np.clip(frac, 0, 1), DEL, stroke_width=4)
        arr = Arrow(ax.c2p(118, 0.95), ax.c2p(86, 0.55), buff=0, color=LOSS, stroke_width=4,
                    max_tip_length_to_length_ratio=0.12)
        arr_lab = label(r"prices fall $\Rightarrow$ sell", font_size=26, color=LOSS).next_to(arr.get_center(), UP + LEFT,
                                                                                        buff=0.15)  # above the curve
        card = history_card(1981, r"Leland, O'Brien and Rubinstein", r"portfolio insurance: a floor under a "
                            r"portfolio, built not from bought puts but by replicating them, Black--Scholes delta "
                            r"hedging with index futures", width=5.4, font_size=24).to_edge(RIGHT, buff=0.5).shift(UP * 0.9)
        card2 = lab_card(r"portfolio insurance", [
            "for i in range(n):",
            "    tau = max(T - i / 252, 1e-6)",
            "    g = bs.greeks(S[i], floor, tau, sigma, rf[i] * 252, 0, -1)",
            "    w[i] = S[i] * (1 + g['delta']) / (S[i] + g['price'])",
            "    V[i + 1] = V[i] * (w[i] * (1 + ret[i])",
            "                       + (1 - w[i]) * (1 + rf[i]))",
            "    S[i + 1] = S[i] * (1 + ret[i])",
        ], source="explainer/quant/house/hedge.py (replicate_put, abridged)", width=6.6)
        card2.to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        with self.voiceover(
            "By the mid-1980s the hedge had become a product. Hayne Leland and Mark Rubinstein, with John O'Brien, "
            "sold portfolio insurance: a floor under a pension fund, built by replicating a put with index futures, "
            "the recipe Rubinstein and Leland published in 1981. <bookmark mark='a'/> Replicating a put means "
            "holding less stock as prices fall: under a one-year floor five percent below the market, a ten "
            f"percent fall makes this model sell {100 * ins['sold_on_10pct']:.0f} percent of its stock. "
            "<bookmark mark='b'/> In the House: four lines a day."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(card), FadeIn(g), Create(line))
            self.play(GrowArrow(arr), FadeIn(arr_lab))
            vo.wait_until("b")
            self.play(FadeIn(card2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self, ins):
        dates = [str(int(x)) for x in ins["dates"]]
        S, V, w = np.asarray(ins["S"], float), np.asarray(ins["V"], float), np.asarray(ins["w"], float)
        j1 = int(np.searchsorted(np.asarray(ins["dates"]), 19871031))
        n = j1
        xs = np.arange(len(S))
        g = axes([0, n], [70, 115], x_length=8.2, y_length=4.4, ylabel=r"value, 1 July 1987 $= 100$",
                 yticks=[80, 95, 110], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        fl = DashedLine(ax.c2p(0, ins["floor_value"]), ax.c2p(n, ins["floor_value"]), color=LOSS, stroke_width=2)
        fl_lab = label(rf"the floor at the horizon, {ins['floor_value']:.1f}", font_size=20, color=LOSS)
        fl_lab.next_to(ax.c2p(0, ins["floor_value"]), DOWN + RIGHT, buff=0.08)
        k = ValueTracker(1)
        mkt = always_redraw(lambda: curve(ax, xs[:max(int(k.get_value()) + 1, 2)], S[:max(int(k.get_value()) + 1, 2)],
                                          SPOT, stroke_width=2.5))
        port = always_redraw(lambda: curve(ax, xs[:max(int(k.get_value()) + 1, 2)], V[:max(int(k.get_value()) + 1, 2)],
                                           WHITE, stroke_width=3.5))
        frame = Rectangle(width=0.6, height=3.0, stroke_color=GREY_C, stroke_width=1.5).move_to([5.6, -0.6, 0])
        fill = always_redraw(lambda: Rectangle(width=0.6, height=max(3.0 * w[min(int(k.get_value()), len(w) - 1)], 0.01),
                                               stroke_width=0, fill_color=DEL, fill_opacity=0.85)
                             .align_to(frame, DOWN).align_to(frame, LEFT))
        wl = always_redraw(lambda: MathTex(rf"{100 * w[min(int(k.get_value()), len(w) - 1)]:.0f}\%", font_size=30,
                                           color=DEL).next_to(frame, UP, buff=0.12))
        wcap = wrapped_label(r"stock weight for the next return", 2.6, 22, DEL).next_to(frame, DOWN, buff=0.12)
        def state_date():
            j = min(int(k.get_value()), len(dates)-1)
            return ("close " + datetime_str(str(ins["end_oct"]["date"]))) if j >= n else ("before " + datetime_str(dates[j]))
        day = always_redraw(lambda: label(state_date(), font_size=26, color=GREY_A).to_corner(UR, buff=0.4))
        leg = legend([(SPOT, r"the US market (French)"), (WHITE, r"the insured portfolio")], font_size=20)
        leg.next_to(g, UP, buff=0.25).align_to(g, LEFT)
        params = note(rf"illustrative: one-year floor at {ins['floor']:.0f}, $\sigma = {100 * ins['sigma']:.0f}\%$, "
                      r"bills at the daily T-bill rate, rebalanced at each close", font_size=18).to_edge(DOWN, buff=0.25)
        i5 = dates.index(str(ins["oct5"]["date"]))
        i16 = dates.index(str(ins["oct16"]["date"]))
        i19 = dates.index(str(ins["oct19"]["date"]))
        i20 = dates.index(str(ins["oct20"]["date"]))
        o5, o16, o19, o20, eo = ins["oct5"], ins["oct16"], ins["oct19"], ins["oct20"], ins["end_oct"]
        floor_word = "below" if ins["breach"] else "above"
        brady = VGroup(
            label(r"The Brady Commission (1988):", font_size=24, color=IMP),
            label(r"``\$60 to \$90 billion of equity assets were under portfolio insurance administration''",
                  font_size=20, color=GREY_A),
            label(r"``stock sales in excess of 20 percent of a portfolio in response to a 10 percent decline''",
                  font_size=20, color=GREY_A),
            label(r"``\$12 billion ... should already have been sold. Less than \$4 billion had in fact been sold.''",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        brady.scale_to_fit_width(min(brady.width, 12.6)).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Run it on the real 1987, from the first of July, on Kenneth French's daily returns: white, the insured "
            "portfolio; blue, the market; yellow, the share in stocks, "
            f"{100 * o5['w']:.0f} percent on the fifth of October. <bookmark mark='a'/> The market falls for days, "
            f"and the rule sells: {100 * o16['w']:.0f} percent by Friday the sixteenth. <bookmark mark='b'/> On "
            f"Monday the market gaps down with the portfolio still {100 * o19['w']:.0f} percent in stocks, straight "
            f"through the floor; <bookmark mark='d'/> next morning the model sells down to {100 * o20['w']:.0f}. <bookmark mark='e'/> October ends at "
            f"{eo['V']:.1f}, {floor_word} the floor of {ins['floor_value']:.1f}. <bookmark mark='c'/> The Brady Commission: sixty to ninety billion "
            "dollars insured, models selling more than a fifth on a ten percent fall, and that Monday twelve "
            "billion that should have been sold, of which less than four had been. Pause and predict: what "
            "happens when everyone follows the rule?"
        ) as vo:
            self.play(FadeIn(g), Create(fl), FadeIn(fl_lab), FadeIn(leg), FadeIn(frame), FadeIn(wcap), FadeIn(params))
            self.add(mkt, port, fill, wl, day)
            self.play(k.animate.set_value(i5), run_time=max(vo.until("a") - 0.5, 4.0), rate_func=linear)
            self.play(k.animate.set_value(i16), run_time=max(vo.until("b") - 0.5, 2.0), rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(i19), run_time=0.6, rate_func=linear)
            vo.wait_until("d")
            self.play(k.animate.set_value(i20), run_time=0.6, rate_func=linear)
            vo.wait_until("e")
            self.play(k.animate.set_value(n), run_time=1.5, rate_func=linear)
            for m_ in (mkt, port, fill, wl, day):
                m_.clear_updaters()
            vo.wait_until("c")
            self.play(FadeOut(VGroup(leg, params)), FadeIn(brady, shift=DOWN * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def day(self, c):
        dates = [str(int(x)) for x in c["window_dates"]]
        r = np.asarray(c["window_ret"], float)
        n = len(r)
        g = axes([0, n], [-0.19, 0.1], x_length=10.0, y_length=4.4, ylabel=r"daily return of the US stock market",
                 yticks=[-0.15, -0.1, -0.05, 0, 0.05], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, v in enumerate(r):
            y0, y1 = ax.c2p(i + 0.5, 0)[1], ax.c2p(i + 0.5, v)[1]
            bars.add(Rectangle(width=ax.x_length / n * 0.7, height=max(abs(y1 - y0), 0.003), stroke_width=0,
                               fill_color=LOSS if v < 0 else SPOT, fill_opacity=0.9)
                     .move_to([ax.c2p(i + 0.5, 0)[0], (y0 + y1) / 2, 0]))
        i0 = dates.index("19871019")
        lab = MathTex(rf"{100 * c['ret']:.1f}\%", font_size=40, color=LOSS).next_to(bars[i0], DOWN, buff=0.15)
        day = label(r"Monday 19 October 1987", font_size=26, color=LOSS)
        # one row, left of the bar's foot, in the empty space under the small bars and above the axis
        VGroup(day, lab).arrange(RIGHT, buff=0.3).next_to(bars[i0].get_bottom(), LEFT, buff=0.2).shift(UP * 0.35)
        ticks = VGroup()
        for i, d_ in enumerate(dates):
            if d_[6:] in ("01", "02") or i == i0:
                pass
        src = note(r"Kenneth French's data library: the value-weighted US market (Mkt$-$RF $+$ RF), "
                   r"dividends included", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            f"""The Brady Commission described a feedback mechanism: portfolio-insurance sales pressured futures; index-arbitrage trades could transmit pressure to stocks, prompting further model sales. This was one mechanism among several, not evidence that every investor followed one rule. <bookmark mark='a'/> French's value-weighted US market fell {-100 * c['ret']:.1f} percent; the S and P five hundred fell 20.5. The log return is {-c['z']:.0f} times the preceding year's estimated daily standard deviation. A plug-in Gaussian tail is extraordinarily small, not mathematically impossible. Jackwerth and Rubinstein reported about ten to the minus one hundred and sixty for a separate futures calculation. Both comparisons challenge a calibrated distributional model; they are not directly observed event probabilities."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if r[i] < 0 else DOWN) for i, b_ in enumerate(bars) if i < i0],
                                  lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[i0], UP), run_time=1.5)
            self.play(FadeIn(lab), FadeIn(day))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if r[i] < 0 else DOWN) for i, b_ in enumerate(bars) if i > i0],
                                  lag_ratio=0.05, run_time=2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        k = np.linspace(-0.3, 0.2, 101)
        before = 0.17 + 0.0 * k
        after = 0.17 - 0.45 * k + 0.6 * k ** 2
        g = axes([-0.3, 0.2], [0.08, 0.36], x_length=6.4, y_length=3.6, xlabel=r"log-moneyness",
                 ylabel=r"implied volatility, index options", xticks=[-0.2, -0.1, 0, 0.1],
                 yticks=[0.1, 0.2, 0.3], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        l0 = curve(ax, k, before, GREY_B, stroke_width=3)
        l1 = curve(ax, k, after, IMP, stroke_width=4)
        leg = legend([(GREY_B, r"before 1987: nearly flat"), (IMP, r"after: the skew")], font_size=22)
        leg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        sch = note(r"schematic (Rubinstein 1994 documents the change in S\&P 500 options)", font_size=18)
        sch.next_to(g, DOWN, buff=0.1).align_to(g, LEFT)
        pts = VGroup(
            label(r"the formula's world broke, and the market priced the break:", font_size=26, color=GREY_A),
            label(r"crash protection has cost extra ever since", font_size=26, color=IMP),
            label(r"MacKenzie: the model shaped the market that seemed to fit it,", font_size=24, color=GREY_B),
            label(r"until the market stopped fitting it", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        if pts.width > 6.2:
            pts.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "And then options changed. Before October 1987, index options traded on implied volatilities that "
            "barely depended on the strike: the market priced roughly the Black-Scholes world. After it, "
            "out-of-the-money puts, crash insurance, became permanently dearer than the formula's single volatility "
            "allows. Mark Rubinstein, one of the portfolio insurers, documented it in 1994. That is the skew of "
            "chapter twelve, born here. <bookmark mark='a'/> The sociologist Donald MacKenzie read the episode as a "
            "case of performativity: for fourteen years the formula helped make the market look like the formula, "
            "and then, in one day, the market stopped looking like it. Part twelve is about that skew."
            " Ten years later two of its makers won the Nobel prize; a year after that, the fund they helped run collapsed. Next."
        ) as vo:
            self.play(FadeIn(g), Create(l0), FadeIn(leg[0]), FadeIn(sch))
            self.play(Create(l1), FadeIn(leg[1]))
            self.play(FadeIn(pts[:2]))
            vo.wait_until("a")
            self.play(FadeIn(pts[2:]))
        self.wait(0.4)
        self.clear_scene()
