from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data, ymd_to_year, axes, data_range, pause_card


class Crash(VoiceoverScene):
    def construct(self):
        b = load("book2024")
        m = load("market")
        self.card()
        self.file(m)
        self.book(b)
        self.derive()
        self.trades(b)
        self.debate()

    def card(self):
        c = chapter_card(9, r"January 2024: the snowballs melt", r"What happens when a crowded barrier breaks?",
                         lit=(2024,), part=PART)
        with self.voiceover("Chapter nine. January 2024: the snowballs melt."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self, m):
        f = m["fall_2024"]
        card = crisis_card(
            r"January -- February 2024", r"The snowball knock-ins",
            r"China's small-cap indices fell through the knock-in levels of snowballs sold in 2021--2023. Caixin, "
            r"citing Securities Association of China data via Bloomberg, put onshore snowballs at about \$27 billion at "
            r"the end of July 2023. On 11 January 2024 Bloomberg reported about \$13 billion near their loss triggers; "
            r"UBS analysts put the market at about \$50 billion (Asia Financial, 23 January). On 22 January, Risk.net "
            r"reported, the CSI 500 fell 4.7\% to a four-year low with up to a third of products at their knock-in. "
            r"In April, regulators told the largest brokers to stop growing their exposure.",
            stats=[(rf"{100 * f['drop']:.0f}\%", r"CSI 500 (ETF), 29 Dec to 5 Feb"), (r"\$13\text{bn}", r"near knock-in, 11 Jan"),
                   (r"\$50\text{bn}", r"UBS's estimate of the market")], width=11.8, font_size=23)
        card.move_to(ORIGIN)
        src = note(r"Caixin (27 Oct 2023); Bloomberg (11 Jan, 24 Apr 2024); Asia Financial (23 Jan 2024); Risk.net; "
                   r"Yahoo Finance (510500.SS)", font_size=17, color=GREY_B).to_corner(DR, buff=0.2)
        with self.voiceover(
            "In January 2024 China's small-cap indices fell through the knock-in levels of the snowballs sold over "
            "three years. Caixin, citing industry data, put onshore snowballs at about twenty-seven billion dollars "
            "in mid-2023. On the eleventh of "
            "January, Bloomberg reported about thirteen billion dollars of them close to their loss triggers, and "
            "UBS analysts estimated the whole market at around fifty billion. <bookmark mark='a'/> On the "
            "twenty-second, as Risk.net reported it, the CSI 500 fell 4.7 percent in a day to a four-year low, with "
            f"up to a third of products at their knock-in. Over five weeks the index fell {100 * abs(f['drop']):.0f} "
            "percent. In April, Bloomberg reported, regulators told the largest brokers to stop growing their "
            "exposure to these products."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(card.stats[0], color=QC.CRISIS))
        self.wait(0.5)
        self.clear_scene()

    def book(self, b):
        t = ymd_to_year(b["dates"])
        px = np.asarray(b["close"])
        ki = np.asarray(b["knocked_in"])
        dl = np.asarray(b["dealer_delta"])
        n = len(t)
        t0, t1 = t[0], t[-1]
        g1 = axes([t0, t1], [4.3, 5.9], x_length=8.6, y_length=1.9, ylabel=r"CSI 500 ETF", xticks=[], yticks=[4.5, 5.0, 5.5],
                  font_size=14)
        g2 = axes([t0, t1], [0, 12], x_length=8.6, y_length=1.6, ylabel=r"live notes knocked in", xticks=[], yticks=[0, 6, 12],
                  font_size=14)
        g3 = axes([t0, t1], [10, 27], x_length=8.6, y_length=1.9, ylabel=r"dealers' hedge", yticks=[10, 15, 20, 25],
                  xticks=[ymd_to_year([20231201])[0], ymd_to_year([20240102])[0], ymd_to_year([20240201])[0],
                          ymd_to_year([20240229])[0]],
                  xfmt=lambda u: {0: r"\text{1 Dec}", 1: r"\text{2 Jan}", 2: r"\text{1 Feb}", 3: r"\text{29 Feb}"}[int(np.argmin(np.abs(
                      ymd_to_year([20231201, 20240102, 20240201, 20240229]) - u)))], font_size=14)
        G = VGroup(g1, g2, g3).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.6).shift(UP * 0.15)  # clear of the source line
        tr = ValueTracker(0)
        l1 = tracing(g1.ax, t, px, tr, SPOT, stroke_width=2.5)
        kis = np.repeat(ki, 1).astype(float)
        l2 = tracing(g2.ax, t, kis, tr, BAD, stroke_width=3)
        l3 = tracing(g3.ax, t, dl, tr, DELTA, stroke_width=3)
        i_pk = int(np.argmax(dl))
        i_low = int(np.argmin(px))
        side = VGroup(
            wrapped_label(r"36 snowballs, one issued at the start of each month of 2021--2023 on the CSI 500 (knock-out "
                          r"103\% monthly, knock-in 75\% daily, 24 months), followed day by day on the index's real path",
                          3.4, 17, GREY_A),
            wrapped_label(rf"{b['n_ki_2024']} knocked in between 22 January and 5 February", 3.4, 19, BAD),
            wrapped_label(rf"the dealers' futures hedge, priced by the surrogate (chapter 16): it grew from {dl[0]:.0f} to "
                          rf"{dl[i_pk]:.0f} notes' worth as the index fell, then the knock-ins cut it to {dl[i_low]:.0f} on "
                          r"the day of the low: selling into the fall", 3.4, 17, DELTA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        src = illustration(r"stylized book, one note of notional 1 a month; the index path is real (510500.SS)", corner=DL)
        with self.voiceover(
            f"Reconstruct a hypothetical equal-notional book on the ETF closes: one specified note issued monthly during 2021 through 2023. The neural proxy holds the full 2021 to 2023 volatility estimate fixed, so this is a retrospective reconstruction. <bookmark mark='a'/> Eleven 2024 knock-ins in this book occur from January twenty-second through February fifth; these are contract states, not eleven realized losses. The lower line is cash hedge exposure for an issuer short the notes, not the issuer's unhedged position delta. <bookmark mark='b'/> It rises from {dl[0]:.0f} note-notionals to {dl[i_pk]:.0f}, then is {dl[i_low]:.0f} at the ETF low. The proxy has approximation error, and the record contains issue, aging, knock-out and knock-in effects. We have reconstructed positions under a hypothetical policy, not observed dealer trades or a realized hedging profit-and-loss history."
        ) as vo:
            self.play(FadeIn(G), FadeIn(side[0]), FadeIn(src))
            self.add(l1, l2, l3)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n - 1), run_time=8, rate_func=linear)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\Delta h_t", r"\approx", r"-\Gamma^{\text{issuer}}_t\,\Delta S_t + \sum_{i \in KI_t}\big(\Delta_i^{+} - "
                  r"\Delta_i^{-}\big)", font_size=38, colors={r"\Delta h_t": DELTA}),
            cmath(r"-\Gamma^{\text{issuer}}_t", r"=", r"\sum_i \partial_S h_i(S_t,t;\text{fixed states})", font_size=38,
                  colors={r"-\Gamma^{\text{issuer}}_t": QC.GAMMA}),
            cmath(r"\Delta_i^{+} - \Delta_i^{-}", r"<", r"0\ \text{in the illustrated reduction, not universally}", font_size=38,
                  colors={r"\Delta_i^{+} - \Delta_i^{-}": BAD}),
        ]
        whys = [why(r"the futures the hedgers trade on day $t$: Taylor for the smooth part, plus a jump in each note's "
                    r"hedge on the day it knocks in"),
                why(r"above the barrier the hedge grows as the index falls: the book's gamma makes the hedgers buy "
                    r"the dip"),
                why(r"on the knock-in the hedge jumps down to the knocked-in sheet of chapter 8: the hedgers sell, "
                    r"into the fall")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.8, buff=0.9, edge=6.9)
        pp = pause_card(r"As the index fell toward the barriers, did the hedgers buy or sell?", width=6.0)
        pp.to_corner(DR, buff=0.3)
        with self.voiceover(
            "Under a delta-neutral policy, separate units held from their cash exposure. <bookmark mark='a'/> If h is the positive hedge and issuer position delta is minus h, then the smooth hedge change is minus issuer gamma times the spot move. Time, new issues and redemptions contribute additional terms. <bookmark mark='b'/> A knock-in changes the state and may reduce the hedge, but its sign is model- and state-dependent. The cache's knock-in-day diagnostic compares today's note exposure with yesterday's, so it also contains spot and time changes; it does not isolate a pure state jump. To estimate rebalancing, first convert cash exposure to underlying units, then difference those units. Simply differencing dollar exposure includes mark-to-market changes even when the number of units is fixed."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp))
            step(0)
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def trades(self, b):
        t = ymd_to_year(b["dates"])
        dl = np.asarray(b["dealer_delta"])
        px = np.asarray(b["close"])
        trade = np.r_[0.0, px[1:] * np.diff(dl / px)]
        jump = np.asarray(b["ki_jump"])
        gam = np.asarray(b["dealer_gamma"])
        lim = float(np.max(np.abs(trade))) * 1.1 + 1e-9
        g = axes([t[0], t[-1]], [-lim, lim], x_length=10.5, y_length=3.6, ylabel=r"futures bought (+) or sold ($-$)",
                 yticks=[-round(lim * 0.8, 1), 0, round(lim * 0.8, 1)], xticks=[ymd_to_year([20231201])[0],
                 ymd_to_year([20240102])[0], ymd_to_year([20240201])[0], ymd_to_year([20240229])[0]],
                 xfmt=lambda u: {0: r"\text{1 Dec}", 1: r"\text{2 Jan}", 2: r"\text{1 Feb}", 3: r"\text{29 Feb}"}[int(np.argmin(np.abs(
                     ymd_to_year([20231201, 20240102, 20240201, 20240229]) - u)))], font_size=14).to_edge(UP, buff=0.8)
        ax = g.ax
        w = 0.8 * (ax.c2p(t[0] + np.diff(t).min(), 0)[0] - ax.c2p(t[0], 0)[0])
        bars = VGroup()
        for x, v, j in zip(t, trade, jump):
            y0, y1 = ax.c2p(x, 0)[1], ax.c2p(x, v)[1]
            col = BAD if abs(j) > 1e-6 else (GOOD if v > 0 else IV)
            bars.add(Rectangle(width=w, height=max(abs(y1 - y0), 0.005), stroke_width=0, fill_color=col,
                               fill_opacity=0.85).move_to([ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
        buys = float(trade[trade > 0].sum())
        sells = float(-trade[trade < 0].sum())
        jsum = float(-jump.sum())
        gmax = float(np.max(gam))
        leg = legend([(GOOD, r"hypothetical purchases"), (IV, r"hypothetical sales, other days"),
                      (BAD, r"a recorded knock-in day")], font_size=17)
        leg.arrange(RIGHT, buff=0.5).next_to(g, DOWN, buff=0.25)
        side = wrapped_label(rf"over the three months, the book's hedgers bought {buys:.1f} notes' worth of futures and "
                             rf"sold {sells:.1f}; orders are current spot times the change in underlying units, after the initial hedge. The cached knock-in-day exposure diagnostic totals {jsum:.1f}; it also includes spot/time effects. The "
                             rf"stored sensitivity is a separate diagnostic, not used to infer these orders", 11.6, 20,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"These are hypothetical cash notionals required to rebalance the proxy hedge after the first plotted day. We divide cash exposure by the observed ETF price to obtain underlying units, difference those units, and multiply by the new price. <bookmark mark='a'/> Red identifies days with a recorded knock-in, not a pure causal knock-in trade. Purchases total {buys:.1f} note-notionals and sales {sells:.1f}. The cached same-note exposure changes on knock-in days total a reduction of {jsum:.1f}; that separate diagnostic includes market moves and aging. These are model-implied sizes, not recorded orders. Scaling the book does not by itself establish liquidity, execution costs or market impact. Surrogate error, contract differences and other dealer positions can all change the result."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02, run_time=4),
                      FadeIn(leg[:2]))
            vo.wait_until("a")
            self.play(FadeIn(leg[2]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def debate(self):
        a = history_card(r"Risk.net", r"the selling side", r"Issuers' re-hedging after the knock-ins added to the sell-off "
                         r"in index futures, which pushed the indices toward more barriers: a feedback loop, like the "
                         r"inverse VIX notes of Part 12.", color=QC.CRISIS, width=5.8)
        b_ = history_card(r"SRP", r"the sceptics", r"Analysts quoted by StructuredRetailProducts argued that the "
                          r"outstanding notional was modest next to the futures market, and that hedges do not all move one "
                          r"way, so the knock-ins could not by themselves explain the fall.", color=QC.IDEA, width=5.8)
        VGroup(a, b_).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.3)
        foot = wrapped_label(r"how much the hedging moved the market is disputed; the model-dependent hedge reductions shown here are hypothetical, "
                             r"and do not identify actual flows or their causal price impact", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Did hedging cause the fall? Risk.net reported concern that re-hedging added futures selling and feedback. <bookmark mark='a'/> Other analysts questioned the scale relative to the market and emphasized different hedge directions. Our specified short-note book demonstrates one possible reduction in hedge demand. It neither observes the whole industry's positions nor identifies how much the trades moved prices. Contract states, model Greeks, execution and causal market impact are distinct questions. Korea provides another public episode, with equally important differences between knock-in and realized loss."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b_, shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
