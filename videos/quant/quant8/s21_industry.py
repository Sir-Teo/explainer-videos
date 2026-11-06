from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import predict, ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load, real_data


class Industry(VoiceoverScene):
    def construct(self):
        self.card()
        self.bettors()
        self.budgets()
        self.drawdown(load("drawdown_policy"))
        self.voltarget(load("vol_target"))
        self.desks()

    def card(self):
        c = chapter_card(17, r"Who sizes bets for a living", r"How do funds, syndicates and desks actually do it?",
                         lit=(1969,), part=PART)
        with self.voiceover("Chapter seventeen. Who sizes bets for a living."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bettors(self):
        a = firm_card(r"Thorp: Kelly, measured",
                      r"A 1994 field test of a sports-betting system, sized by Kelly with edge estimates "
                      r"``deliberately chosen to be conservative''. Over the partnership's life, about \$80 billion of "
                      r"trades in some 1.25 million bets.",
                      numbers=[(r"\$50{,}000", r"test bankroll"), (r"\$123{,}000", r"profit in 101 days")],
                      source=r"Thorp (2006), ch.\ 9, pp.\ 402--403, 420", width=4.3, font_size=19)
        b = firm_card(r"Benter: Hong Kong racing",
                      r"A computer handicapping syndicate. ``A conservative fractional Kelly betting strategy was "
                      r"employed throughout''; full Kelly's downswings of more than half the bankroll are ``a common "
                      r"occurrence''.",
                      numbers=[(r"\approx 470", r"races a year"), (r"\approx 19\%", r"track take"),
                               (r"4\ \text{of}\ 5", r"seasons profitable")],
                      source=r"Benter (1994), in Hausch, Lo and Ziemba (eds.)", width=4.3, font_size=19)
        c = firm_card(r"Berlekamp: from Kelly to Medallion",
                      r"Interned at Bell Labs in 1960 and 1962 under John Kelly. In 1989 he took control of Axcom, which "
                      r"ran the trading of Jim Simons's Medallion Fund, and reworked its system with Simons, Sandor "
                      r"Straus and Henry Laufer.",
                      numbers=[],
                      source=r"UC Senate, Elwyn Berlekamp memorial", width=4.3, font_size=19)
        VGroup(a, b, c).arrange(RIGHT, buff=0.2, aligned_edge=UP).move_to(ORIGIN)
        if VGroup(a, b, c).width > 13.6:
            VGroup(a, b, c).scale_to_fit_width(13.6)
        with self.voiceover(
            "First the bettors, from their own accounts. Thorp's 1994 sports-betting test: fifty thousand dollars, sized "
            "by Kelly with deliberately conservative edges, made a hundred and twenty-three thousand in a hundred and one "
            "days. <bookmark mark='a'/> William Benter's syndicate bet about four hundred and seventy Hong Kong races a "
            "year against a nineteen percent track take, profitably in four of five seasons, at a conservative fraction of "
            "Kelly, because at full Kelly losing half the bankroll is, in his words, a common occurrence. "
            "<bookmark mark='b'/> Elwyn Berlekamp worked under Kelly at Bell Labs as a student and in 1989 took control of "
            "Axcom, which traded for Jim Simons's Medallion Fund. How Medallion sizes its bets is not public, and we do not "
            "guess."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def budgets(self):
        rows = VGroup(
            VGroup(label(r"Norway's oil fund (NBIM)", font_size=24, color=QC.FIRM),
                   wrapped_label(r"the mandate caps expected relative volatility (tracking error) at 1.25 percentage "
                                 r"points", 8.4, 20, GREY_A)),
            VGroup(label(r"Bridgewater All Weather (1996)", font_size=24, color=QC.FIRM),
                   wrapped_label(r"``put equal risk on each scenario'' of four economic environments; ``leverage is an "
                                 r"implementation tool''", 8.4, 20, GREY_A)),
            VGroup(label(r"multi-manager platforms", font_size=24, color=QC.FIRM),
                   wrapped_label(r"as reported by the \textit{Wall Street Journal} (via \textit{Business Insider}, "
                                 r"October 2024): a Millennium manager who loses 5\% has capital halved, and at 7.5\% is "
                                 r"likely to be let go. Reported, not disclosed by the firm, which declined to comment.",
                                 8.4, 20, GREY_A)),
        )
        for r_ in rows:
            r_.arrange(RIGHT, buff=0.4, aligned_edge=UP)
            r_[1].align_to(rows, LEFT).shift(RIGHT * 4.6)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(UP, buff=0.7)
        for r_ in rows:
            r_[1].set_x(rows.get_left()[0] + 4.6 + r_[1].width / 2)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        math = VGroup(
            MathTex(r"\pi_t = \pi^*\,\frac{W_t - \alpha M_t}{W_t},\qquad M_t = \max_{s \le t} W_s", font_size=34,
                    color=KELLY),
            wrapped_label(r"log-utility continuous discounted-wealth theory: Kelly times the drawdown cushion. The following weekly nominal-wealth simulation is an illustration, not a discrete-trading guarantee", 12.0, 20, GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Most institutions work inside risk budgets, which are control constraints. Norway's oil fund caps its expected volatility relative to its benchmark at one and a quarter points; Bridgewater's All Weather, from 1996, puts equal risk on four economic environments. <bookmark mark='a'/> As reported by the Wall Street Journal in 2024, a Millennium manager who loses five percent has capital halved, and at seven and a half is likely let go; the firm did not comment. <bookmark mark='b'/> Grossman and Zhou solved the drawdown problem in 1993: never fall below a fraction alpha of the peak by holding Merton's fraction of the cushion above it: chapter two's floor, ratcheting up. The logarithmic Grossman-Zhou result constrains discounted wealth in a continuous diffusion. Our following weekly simulation uses a nominal-wealth cushion inspired by it; discrete trading and jumps need not preserve the floor."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(Write(math[0]), FadeIn(math[1]))
        self.wait(0.4)
        self.clear_scene()

    def drawdown(self, d):
        sk, sg, sm = (np.asarray(d[k]) for k in ("sample_k", "sample_g", "sample_m"))
        n = sk.shape[1]
        t = (4 * np.arange(n) + 1) / 52  # cached after weeks 1, 5, 9, ...
        display_lo = np.floor(min(sk[0].min(), sg[0].min(), (sm[0] + np.log10(d["alpha"])).min()))
        display_hi = np.ceil(max(sk[0].max(), sg[0].max(), sm[0].max()))
        g = axes([0, d["years"]], [display_lo, display_hi], x_length=7.4, y_length=4.4, xlabel=r"years",
                 ylabel=r"wealth (log scale)", xticks=[0, 10, 20, 30], yticks=[-1, 0, 1], yfmt=lambda u: f"10^{{{int(u)}}}",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(1)

        def tr(arr, col, sw, dash=False):
            return always_redraw(lambda: VMobject(stroke_color=col, stroke_width=sw, stroke_opacity=0.5 if dash else 1)
                                 .set_points_as_corners([ax.c2p(t[j], float(arr[j]))
                                                         for j in range(0, int(tk.get_value()) + 1)]))

        lines = [tr(sk[0], OVER, 2.5), tr(sg[0], UNDER, 3.5), tr(sm[0] + np.log10(d["alpha"]), UNDER, 1.5, True)]
        leg = legend([(OVER, r"Kelly, unconstrained"), (UNDER, r"GZ-inspired nominal cushion, $\alpha=0.8$"),
                      (GREY_B, r"faint: its floor, 80\% of the peak")], font_size=17).next_to(g, UP, buff=0.2).align_to(
            g, LEFT)
        res = VGroup(
            label(r"2{,}000 thirty-year paths, weekly:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{worst drawdown: Kelly }}{100 * d['worst_dd_kelly']:.0f}\%,\ \text{{GZ }}"
                    rf"{100 * d['worst_dd_gz']:.0f}\%", font_size=26),
            MathTex(rf"\text{{median growth: Kelly }}{100 * d['median_growth_kelly']:.1f}\%,\ \text{{GZ }}"
                    rf"{100 * d['median_growth_gz']:.1f}\%", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        q = predict(r"A pod is down 4.9\% against a 5\% limit. What does the Grossman--Zhou investor do with her "
                       r"stock fraction?", width=4.6, font_size=19).next_to(res, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        src = illustration(r"simulation: $\mu - r = 6\%$, $\sigma = 18\%$; Kelly fraction 185\%")
        with self.voiceover(
            f"One path each: Kelly in red, Grossman and Zhou with a floor at eighty percent of the peak in blue. As she falls toward the floor she sells, and on this illustrated path she stays above it. <bookmark mark='a'/> Over two thousand paths, Kelly's worst drawdown is {100 * d['worst_dd_kelly']:.0f} percent, hers {100 * d['worst_dd_gz']:.0f}. The price: {100 * d['median_growth_gz']:.1f} percent median growth against {100 * d['median_growth_kelly']:.1f}. <bookmark mark='b'/> Pause and predict: down four point nine against a five percent limit? Hold almost nothing: the cushion is a tenth of a percent. This nominal weekly illustration is not the exact discounted-wealth optimization. No breach in these sampled paths is not a guarantee."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.add(*lines)
            self.play(tk.animate.set_value(n - 1), run_time=7, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(q))
        for l_ in lines:
            l_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def voltarget(self, v):
        w = np.asarray(v["w"])
        d = np.asarray(v["dates"])
        yrs = d // 100 + (d % 100 - 1) / 12
        g = axes([1926, 2021], [0, np.ceil(w.max() * 1.05)], x_length=7.4, y_length=3.4, xlabel=r"year",
                 ylabel=r"exposure to the US market (average 1)", xticks=[1930, 1960, 1990, 2020], yticks=[0, 3, 6, 9],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        line = curve(ax, yrs, w, ALT, stroke_width=1.6)
        one = DashedLine(ax.c2p(1926, 1), ax.c2p(2021, 1), color=GREY_C, stroke_width=1.5)
        better = v["sr_scaled"] > v["sr_mkt"]
        side = VGroup(
            MathTex(r"\pi_t \propto \frac{1}{\hat\sigma_{t-1}^2}", font_size=36, color=KELLY),
            MathTex(rf"\text{{Sharpe: }}{v['sr_scaled']:.2f}\ \text{{vs}}\ {v['sr_mkt']:.2f}", font_size=28),
            MathTex(rf"\alpha = {100 * v['alpha']:.1f}\%\text{{ a year}},\ t = {v['alpha_t']:.1f}", font_size=28),
            wrapped_label(rf"exposure from {v['min_w']:.2f} to {v['max_w']:.1f}: an unconstrained version; real funds "
                          r"cap leverage", 4.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        src = real_data(r"Kenneth French daily, 1926--2020; registered with the trial counter")
        with self.voiceover(
            """Volatility targeting here scales exposure by inverse lagged realized variance. Moreira and Muir studied related rules in 2017. This existing registered historical calculation uses ninety-four years of French data. Although the variance signal is lagged, exposure is normalized to average one using the full sample, so the whole procedure uses hindsight. Gross returns omit trading and funding costs."""
        ):
            self.play(FadeIn(g), Create(one), FadeIn(src), FadeIn(side[0]))
            self.play(Create(line), run_time=3)
        with self.voiceover(
            f"It helped: a Sharpe ratio of {v['sr_scaled']:.2f} against {v['sr_mkt']:.2f}, and an alpha of "
            f"{100 * v['alpha']:.1f} percent a year, t of {v['alpha_t']:.1f}. The displayed t statistic is the cached homoskedastic OLS reference, not a HAC statistic; this association does not establish a causal mechanism; but the exposure swings are wild, and real funds cap them."
            if better else
            f"It did not help here: a Sharpe ratio of {v['sr_scaled']:.2f} against {v['sr_mkt']:.2f}."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in side[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def desks(self):
        cards = VGroup(
            firm_card(r"Execution desks",
                      r"Almgren and Chriss (2001): liquidating a block is a control problem, solved every day. Almgren, "
                      r"Thum, Hauptmann and Li (2005) fitted impact on Citigroup's US equity trades: it grows like the "
                      r"3/5 power of size. Part 37 in full.",
                      source=r"\textit{Journal of Risk} 3; \textit{Risk} 18(7)", width=6.4, font_size=20),
            firm_card(r"Elm Wealth",
                      r"Victor Haghani, of the coin experiment and once a partner at LTCM, runs a firm that sizes "
                      r"positions by Merton's rule, and wrote \textit{The Missing Billionaires} (2023, with James White; "
                      r"Wiley): why rich families did not stay rich: bad sizing and spending.",
                      source=r"Haghani and White (2023)", width=6.4, font_size=20),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(ORIGIN)
        with self.voiceover(
            "Execution desks solve a control problem daily: Almgren and Chriss, 2001; and Almgren, Thum, Hauptmann and Li "
            "fitted its impact on Citigroup's trades, a three-fifths power of size. <bookmark mark='a'/> And Victor "
            "Haghani, of the coin experiment, now sizes clients' portfolios with Merton's rule; his 2023 book with James "
            "White, The Missing Billionaires, blames lost fortunes on bad sizing and spending."
            " Last, the frontier."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
