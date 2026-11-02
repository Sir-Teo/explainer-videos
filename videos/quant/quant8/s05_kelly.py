from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load, real_data, tbar


class Kelly(VoiceoverScene):
    def construct(self):
        k = load("kelly_us")
        fr = load("fractional")
        self.card()
        self.history()
        self.parabola(k)
        self.uncertainty(k)
        self.fractional(fr)

    def card(self):
        c = chapter_card(4, r"Kelly, fractional Kelly and Thorp", r"What fraction grows wealth fastest?", lit=(1956,),
                         part=PART)
        with self.voiceover("Chapter four. Kelly, fractional Kelly, and Thorp."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self):
        h = history_card(r"1956", r"John Kelly, Bell Labs",
                         r"A gambler with a noisy private wire should bet so that his wealth grows at the wire's "
                         r"information rate: maximize the expected logarithm of wealth. Breiman (1961) proved that this "
                         r"strategy eventually outgrows every other, and reaches any goal fastest.", width=6.4)
        f = firm_card(r"Princeton Newport Partners",
                      r"Edward Thorp counted cards at blackjack with Kelly bets (\textit{Beat the Dealer}, 1962), then "
                      r"ran a hedge fund on convertible and warrant arbitrage, sized the same way, from 1969 to 1988.",
                      numbers=[(r"\approx 15\%", r"a year after fees, 1969--1988"), (r"0", r"losing years")],
                      source=r"Thorp, \textit{A Man for All Markets} (2017)", width=6.0)
        VGroup(h, f).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(ORIGIN)
        with self.voiceover(
            "In 1956 John Kelly, a physicist at Bell Labs, asked how a gambler with an edge, a noisy private wire with "
            "the result of a race, should bet. His answer: maximize the expected logarithm of wealth, and wealth "
            "grows at the information rate of the wire. In 1961 Leo Breiman proved that this strategy eventually "
            "outgrows every other one, and reaches any target fastest. <bookmark mark='a'/> The mathematician Edward "
            "Thorp took it to the casino, counting cards at blackjack with Kelly bets, and then to Wall Street. His "
            "fund, Princeton Newport Partners, arbitraged convertible bonds and warrants from 1969 to 1988, sized by "
            "the same rule, and by his account returned about fifteen percent a year after fees, without a losing year."
        ) as vo:
            self.play(FadeIn(h, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(f, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def parabola(self, k):
        f, g = np.asarray(k["f"]), np.asarray(k["growth"])
        ok = np.isfinite(g) & (g > -0.1)
        gr = axes([0, 4], [-0.1, 0.15], x_length=7.4, y_length=4.4, xlabel=r"fraction of wealth in US stocks "
                  r"(rebalanced monthly, borrowing at the T-bill rate)", ylabel=r"realized growth, a year",
                  xticks=[0, 1, 2, 3, 4], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[-0.1, -0.05, 0, 0.05, 0.1, 0.15],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = gr.ax
        line = curve(ax, f[ok], g[ok], KELLY, stroke_width=4)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(4, 0), color=GREY_C, stroke_width=1.5)
        best = Dot(ax.c2p(k["best"], k["growth_at_best"]), color=KELLY)
        bl = MathTex(rf"{100 * k['best']:.0f}\%:\ {100 * k['growth_at_best']:.1f}\%", font_size=26, color=KELLY).next_to(
            best, UP, buff=0.12)
        one = Dot(ax.c2p(1, k["growth_at_1"]), color=UNDER)
        ol = MathTex(rf"100\%:\ {100 * k['growth_at_1']:.1f}\%", font_size=24, color=UNDER).next_to(one, DOWN + RIGHT,
                                                                                                   buff=0.05)
        ruin = DashedLine(ax.c2p(k["ruin_leverage"], -0.1), ax.c2p(k["ruin_leverage"], 0.15), color=OVER, stroke_width=2)
        rl = wrapped_label(rf"at {100 * k['ruin_leverage']:.0f}\%, the worst month (September 1931, "
                           rf"{100 * k['worst_month']:.1f}\%) wipes you out", 2.4, 18, OVER).next_to(
            ax.c2p(k["ruin_leverage"], 0.13), RIGHT, buff=0.1)
        src = real_data(r"Kenneth French: US market and T-bill, monthly, July 1926 -- December 2020")
        with self.voiceover(
            "Here is Kelly's parabola, not from a formula but from history. Take the American market from 1926 to "
            "2020, and imagine rebalancing every month to hold a fixed fraction of your wealth in it, borrowing at "
            "the Treasury bill rate when the fraction is above one. This is the realized growth rate for every "
            "fraction. <bookmark mark='a'/> All in, a hundred percent, grew at "
            f"{100 * k['growth_at_1']:.1f} percent a year. The peak is at {100 * k['best']:.0f} percent, more than "
            f"twice levered, at {100 * k['growth_at_best']:.1f}: the log-utility Merton fraction of the last chapter, "
            "measured directly. <bookmark mark='b'/> Beyond the peak, growth falls; and at "
            f"{100 * k['ruin_leverage']:.0f} percent a single month, September 1931, would have wiped you out."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(src), Create(zero), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(ol), FadeIn(best), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(ruin), FadeIn(rl))
        self.wait(0.4)
        self.clear_scene()

    def uncertainty(self, k):
        bs = np.asarray(k["best_bs"])
        bins = np.linspace(0, 4, 33)
        h, _ = np.histogram(bs, bins=bins)
        g = axes([0, 4], [0, max(h) * 1.15], x_length=6.4, y_length=3.6, xlabel=r"the best fraction, in resampled "
                 r"histories", xticks=[0, 1, 2, 3, 4], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        ax = g.ax
        bars = VGroup(*[tbar(ax, (bins[i] + bins[i + 1]) / 2, h[i], ALT, width=0.11) for i in range(len(h)) if h[i]])
        side = VGroup(
            label(r"400 histories, resampled in 12-month blocks:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{90\% of the best fractions: }} {100 * k['bs_p05']:.0f}\% \text{{ to }} "
                    rf"{100 * k['bs_p95']:.0f}\%", font_size=28, color=ALT),
            label(r"choose on 1926--1972, invest 1973--2020:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{chosen: }} {100 * k['split_f1']:.0f}\% \to {100 * k['split_g2_at_f1']:.1f}\% "
                    r"\text{ a year}", font_size=28, color=KELLY),
            MathTex(rf"\text{{half of it: }} {100 * k['split_f1'] / 2:.0f}\% \to {100 * k['split_g2_at_half']:.1f}\%",
                    font_size=28, color=UNDER),
            MathTex(rf"\text{{best in hindsight: }} {100 * k['split_f2']:.0f}\% \to {100 * k['split_g2_best']:.1f}\%",
                    font_size=28, color=GREY_B),
            wrapped_label(r"monthly rebalancing hides intramonth crashes: at twice levered, 19 October 1987 alone would "
                          r"have cost about 35\% (the market fell 17\%)", 4.6, 19, OVER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "How sure are we of that peak? Resample the history in blocks of a year, four hundred times, and find "
            f"the best fraction in each. Ninety percent of them lie between {100 * k['bs_p05']:.0f} and "
            f"{100 * k['bs_p95']:.0f} percent. The estimate of the edge, not the formula, is the weak link. "
            "<bookmark mark='a'/> And a test the House registered: choose the fraction on the first half of the "
            f"history, 1926 to 1972, and invest with it from 1973. The chosen {100 * k['split_f1']:.0f} percent grew "
            f"at {100 * k['split_g2_at_f1']:.1f} percent a year; half of it, {100 * k['split_g2_at_half']:.1f}. In "
            "this history full Kelly would have paid. <bookmark mark='b'/> But monthly rebalancing hides the worst "
            "days: at twice levered, the crash of October 1987 alone would have taken about thirty-five percent in a day."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03),
                      FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in side[2:6]], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()

    def fractional(self, fr):
        mult, rel = np.asarray(fr["mult"]), np.asarray(fr["growth_rel"])
        g = axes([0, 2.5], [-1.0, 1.1], x_length=6.0, y_length=3.0, xlabel=r"multiple of the Kelly fraction",
                 ylabel=r"excess growth, relative to Kelly", xticks=[0, 0.5, 1, 1.5, 2, 2.5], yticks=[-1, 0, 0.75, 1],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).to_edge(UP, buff=0.5)
        ax = g.ax
        line = curve(ax, mult, rel, KELLY, stroke_width=4)
        m = fr["by_mult"]
        rows = [(r"\tfrac12\ \text{Kelly}", m["0.5"], UNDER), (r"\text{Kelly}", m["1.0"], KELLY),
                (r"2\times\text{Kelly}", m["2.0"], OVER)]
        head = VGroup(label(r"", font_size=20), label(r"vol", font_size=20, color=GREY_B),
                      label(r"median after 10 y", font_size=20, color=GREY_B),
                      label(r"chance of halving", font_size=20, color=GREY_B))
        cells = [head]
        for name, d, col in rows:
            cells.append(VGroup(MathTex(name, font_size=26, color=col), MathTex(f"{100 * d['vol']:.0f}\\%", font_size=26),
                                MathTex(f"{d['median']:.2f}", font_size=26),
                                MathTex(f"{100 * d['p_dd50']:.0f}\\%", font_size=26, color=col)))
        tab = VGroup(*[x for r_ in cells for x in r_]).arrange_in_grid(rows=4, cols=4, buff=(0.45, 0.18),
                                                                    col_alignments="lrrr")
        tab.next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        if tab.get_bottom()[1] < -3.6:
            tab.shift(UP * (-3.6 - tab.get_bottom()[1]))
        side = VGroup(
            MathTex(r"g(c f^*) - r = (2c - c^2)\,\big(g(f^*) - r\big)", font_size=30),
            wrapped_label(r"half Kelly keeps three quarters of the growth with half the volatility; twice Kelly grows "
                          r"no faster than cash", 4.6, 21, GREY_A),
            wrapped_label(r"and if your edge is overestimated by half, full Kelly on the estimate is twice Kelly on "
                          r"the truth: practitioners bet a fraction (MacLean, Thorp and Ziemba 2011)", 4.6, 21, VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulation: $\mu - r = 6\%$, $\sigma = 18\%$, 4{,}000 ten-year daily paths")
        with self.voiceover(
            "This is why practitioners bet a fraction of Kelly. Measured as a share of Kelly's excess growth, the "
            "curve is the same parabola for any asset. <bookmark mark='a'/> Half Kelly keeps three quarters of the "
            "growth with half the volatility. Twice Kelly grows no faster than cash, with twice the volatility. "
            "<bookmark mark='b'/> In simulation, over ten years, full Kelly halves your wealth from its peak at some "
            f"point {100 * m['1.0']['p_dd50']:.0f} percent of the time; half Kelly, {100 * m['0.5']['p_dd50']:.0f} "
            "percent. <bookmark mark='c'/> And the edge itself is uncertain. If you overestimate it by half, full "
            "Kelly on your estimate is twice Kelly on the truth, which is why Thorp, and most of the industry, bet "
            "less."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[0]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.3, run_time=2.5))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
