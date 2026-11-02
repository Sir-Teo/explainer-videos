from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load, real_data, tbar


class Kelly(VoiceoverScene):
    def construct(self):
        k = load("kelly_us")
        self.card()
        self.history()
        self.derive()
        self.fans(load("kelly_live"))
        self.race(load("breiman_race"))
        self.parabola(k)

    def card(self):
        c = chapter_card(8, r"Kelly and Breiman", r"What fraction grows wealth fastest, and why does it win?",
                         lit=(1956,), part=PART)
        with self.voiceover("Chapter eight. Kelly, and Breiman's theorem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self):
        h = history_card(r"1956", r"John Kelly, Bell Labs",
                         r"A gambler with a noisy private wire should bet so that his wealth grows at the wire's "
                         r"information rate: maximize the expected logarithm of wealth.", width=6.0)
        f = firm_card(r"Edward Thorp's partnership",
                      r"Claude Shannon showed Thorp Kelly's paper at MIT in 1960. Thorp used it at blackjack, then from "
                      r"3 November 1969 to size a convertible-hedging partnership.",
                      numbers=[(r"\approx 20\%", r"a year, Nov 1969 -- May 1998"), (r"\approx 6\%", r"standard deviation"),
                               (r"\approx 0", r"correlation with the market")],
                      source=r"Thorp (2006), \textit{Handbook of Asset and Liability Management}, ch.\ 9", width=6.4)
        VGroup(h, f).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(ORIGIN)
        with self.voiceover(
            "In 1956 John Kelly of Bell Labs asked how a gambler with a noisy private wire should bet. His answer: "
            "maximize the expected logarithm of wealth. <bookmark mark='a'/> In 1960 Claude Shannon showed the paper to "
            "Edward Thorp at MIT, who used it at blackjack and, from November 1969, to size an investment partnership. By "
            "Thorp's own 2006 account, through May 1998 it compounded at about twenty percent a year, with a standard "
            "deviation of about six and almost no correlation with the market."
        ) as vo:
            self.play(FadeIn(h, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(f, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"g(f) = p\log(1+f) + q\log(1-f)", r"\ \Rightarrow\ ", r"g'(f) = \frac{p}{1+f} - \frac{q}{1-f} = 0,"
                      r"\ \ f^* = p - q", font_size=30),
                cmath(r"d\log W", r"=", r"\big(r + f(\mu - r) - \tfrac12 f^2\sigma^2\big)\,dt + f\sigma\,dW", font_size=32),
                cmath(r"f^*", r"=", r"\frac{\mu - r}{\sigma^2},\qquad g^* - r = \tfrac12\theta^2", font_size=32,
                      colors={r"f^*": KELLY}),
                cmath(r"\tfrac1n \log W_n(f)", r"\to", r"g(f)\quad\text{almost surely}", font_size=32),
                cmath(r"\frac{W_n(f^*)}{W_n(f)}", r"=", r"e^{\,n(g(f^*) - g(f)) + o(n)}\ \to\ \infty", font_size=32,
                      colors={r"\frac{W_n(f^*)}{W_n(f)}": KELLY})]
        whys = [why(r"the coin: maximize the growth per bet; its derivative vanishes at $p - q$", font_size=21),
                why(r"a stock, continuously rebalanced: It\^o on $\log W$ (Part 5)", font_size=21),
                why(r"the vertex of that parabola: Merton's fraction at $\gamma = 1$; the Kelly growth is half the "
                    r"squared Sharpe ratio", font_size=21),
                why(r"$\log W_n$ is a sum of i.i.d.\ log-returns: the strong law of large numbers", font_size=21),
                why(r"Breiman (1961): any rival with lower $g$ falls behind by a factor that grows exponentially; the "
                    r"general case (any strategy) holds too", font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=0.4, buff=0.9, edge=6.9)
        with self.voiceover(
            "For the coin, set the derivative of the growth rate to zero: the Kelly fraction is p minus q. "
            "<bookmark mark='a'/> For a stock, Itô's formula makes log wealth's drift a parabola in f. "
            "<bookmark mark='b'/> Its vertex is excess return over variance, Merton at gamma one, earning half the squared "
            "Sharpe ratio above cash. <bookmark mark='c'/> Now why it wins. Log wealth is a sum of independent terms, so "
            "by the strong law, log wealth over n converges to g. <bookmark mark='d'/> Against any rival the wealth ratio "
            "grows like e to the n times the gap in growth rates: it goes to infinity. Breiman proved this in 1961, for "
            "every rival strategy."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def fans(self, L):
        t = np.asarray(L["t"])
        fans = L["fans"]
        keys, cols = ["0.5", "1.0", "2.0"], [UNDER, KELLY, OVER]
        g = axes([0, 40], [-1.5, 3.0], x_length=8.4, y_length=5.0, xlabel=r"years", ylabel=r"wealth (log scale)",
                 xticks=[0, 10, 20, 30, 40], yticks=[-1, 0, 1, 2, 3], yfmt=lambda u: f"10^{{{int(u)}}}", font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tk = ValueTracker(0)
        n = len(t)

        def fan(key, col):
            P = np.clip(np.asarray(fans[key]["paths"]), -1.5, 3.0)
            return always_redraw(lambda: VGroup(*[
                VMobject(stroke_color=col, stroke_width=1.0, stroke_opacity=0.25).set_points_as_corners(
                    [ax.c2p(t[j], row[j]) for j in range(0, max(int(tk.get_value()), 1) + 1, 3)]) for row in P[:30]]))

        def med(key, col):
            m = np.clip(np.asarray(fans[key]["median"]), -1.5, 3.0)
            return always_redraw(lambda: VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(
                [ax.c2p(t[j], m[j]) for j in range(0, max(int(tk.get_value()), 1) + 1, 3)]))

        fs = [fan(k_, c_) for k_, c_ in zip(keys, cols)]
        ms = [med(k_, c_) for k_, c_ in zip(keys, cols)]
        avg = VGroup(*[DashedLine(ax.c2p(0, 0), ax.c2p(40, min(40 * fans[k_]["g"] / np.log(10), 3.0)), color=c_,
                                  stroke_width=2.5) for k_, c_ in zip(keys, cols)])
        leg = legend([(c_, rf"{float(k_):g}$\times$ Kelly ({100 * fans[k_]['f']:.0f}\%): $g = "
                       rf"{100 * fans[k_]['g']:.1f}\%$") for k_, c_ in zip(keys, cols)], font_size=18)
        leg.to_corner(UR, buff=0.4)
        q = pause_card(r"At twice Kelly, what is the median growth rate?", width=4.6, font_size=21).next_to(
            leg, DOWN, buff=0.4).align_to(leg, LEFT)
        ans = wrapped_label(rf"the cash rate, {100 * L['r']:.0f}\%: no excess growth at all, though its luckiest paths "
                            r"are the richest", 4.6, 19, OVER).next_to(q, DOWN, buff=0.25).align_to(q, LEFT)
        src = illustration(r"simulation: $\mu - r = 6\%$, $\sigma = 18\%$, $r = 2\%$; 30 paths shown per fan, monthly")
        with self.voiceover(
            "Watch it: half Kelly, Kelly and twice Kelly in the same simulated markets for forty years, on a log scale. "
            "<bookmark mark='a'/> Pause and predict: at twice Kelly, what is the median growth rate? "
            "<bookmark mark='b'/> Twice Kelly's best paths shoot above everyone, which is the temptation, but its median "
            "barely leaves the ground. <bookmark mark='c'/> Lay the time-average lines over the fans: each median follows "
            f"its line, and twice Kelly's growth is the cash rate, {100 * L['r']:.0f} percent: all that risk for nothing."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.add(*fs, *ms)
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(tk.animate.set_value(n - 1), run_time=max(min(vo.remaining(8.0) - 1, 12), 7), rate_func=linear)
            vo.wait_until("c")
            self.play(Create(avg), FadeIn(ans), run_time=2)
        for m in fs + ms:
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def race(self, B):
        T = np.asarray(B["years"])
        g = axes([0, 100], [0.5, 1.0], x_length=7.0, y_length=4.0, xlabel=r"years",
                 ylabel=r"share of markets in which Kelly is ahead", xticks=[0, 25, 50, 75, 100],
                 yticks=[0.5, 0.75, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7)
        ax = g.ax
        lines = VGroup(curve(ax, T, np.asarray(B["vs_half"]), UNDER, stroke_width=4),
                       curve(ax, T, np.asarray(B["vs_double"]), OVER, stroke_width=4))
        cl = VGroup(curve(ax, T, np.asarray(B["closed_half"]), WHITE, stroke_width=1.5),
                    curve(ax, T, np.asarray(B["closed_double"]), WHITE, stroke_width=1.5))
        leg = legend([(UNDER, r"Kelly vs half Kelly"), (OVER, r"Kelly vs twice Kelly"), (WHITE, r"closed form")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        vh, vd = B["vs_half"], B["vs_double"]
        side = VGroup(
            MathTex(rf"10\text{{ y: }}{100 * vh[9]:.0f}\%,\ {100 * vd[9]:.0f}\%", font_size=28),
            MathTex(rf"100\text{{ y: }}{100 * vh[99]:.0f}\%,\ {100 * vd[99]:.0f}\%", font_size=28),
            wrapped_label(r"Breiman's ``eventually'' is slow: the gap in growth rates is small against the noise, "
                          r"so being ahead takes decades", 4.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        src = illustration(r"simulation: 10{,}000 markets, monthly, 100 years")
        with self.voiceover(
            "How long is eventually? In ten thousand markets, <bookmark mark='a'/> Kelly leads twice Kelly in "
            f"{100 * vd[9]:.0f} percent after ten years and {100 * vd[99]:.0f} after a hundred, but leads half Kelly in "
            f"only {100 * vh[9]:.0f} and {100 * vh[99]:.0f}. Breiman's theorem is true, and slow."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines), Create(cl), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.4))
        self.wait(0.4)
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
            "And Kelly's parabola from history: rebalance monthly to a fixed fraction of the American market from 1926 to "
            "2020, borrowing at the bill rate. <bookmark mark='a'/> All in grew at "
            f"{100 * k['growth_at_1']:.1f} percent a year; the peak, at {100 * k['best']:.0f} percent, grew at "
            f"{100 * k['growth_at_best']:.1f}. <bookmark mark='b'/> At {100 * k['ruin_leverage']:.0f} percent, September "
            "1931 alone would have wiped you out. Hindsight found that peak; next, what happens when you must guess it."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(src), Create(zero), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(ol), FadeIn(best), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(ruin), FadeIn(rl))
        self.wait(0.4)
        self.clear_scene()
