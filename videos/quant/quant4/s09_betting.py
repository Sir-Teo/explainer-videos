from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, MART, P_C, PART, Q_C, load, real_data


class Betting(VoiceoverScene):
    def construct(self):
        p = load("peeking")
        e = load("eprocess")
        self.card()
        self.ville()
        self.peeking(p)
        self.market(e)

    def card(self):
        c = chapter_card(8, r"Testing by betting", r"How do you test a market you watch every day?", part=PART)
        with self.voiceover("Chapter eight. Testing by betting."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ville(self):
        th = theorem_card(r"Ville's inequality",
                          r"If $W_0 = 1, W_1, W_2, \dots$ is a nonnegative martingale, then for any $\alpha$, "
                          r"$P\big(W_n \ge 1/\alpha \text{ for some } n\big) \le \alpha$.", who=r"Ville (1939)",
                          color=MART, width=9.0, font_size=26).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the null hypothesis: a game is fair for a class of bets", font_size=24, color=GREY_A),
            label(r"a gambler starts with \$1 and bets, never more than they have", font_size=24, color=GREY_A),
            label(r"under the null the wealth $W$ is a nonnegative martingale: an \textbf{e-process}", font_size=24,
                  color=MART),
            label(r"reject when $W \ge 20$: wrong at most 5\% of the time, however often you look and whenever you stop",
                  font_size=24, color=QC.LOSS),
            wrapped_label(r"Shafer and Vovk, \textit{Probability and Finance: It's Only a Game!} (2001); Ramdas, "
                          r"Gr\"unwald, Vovk and Shafer, ``Game-theoretic statistics and safe anytime-valid inference'' "
                          r"(2023)", 11.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(th, DOWN, buff=0.5)
        with self.voiceover(
            "Ville's thesis contained a second idea, ignored for sixty years. If a gambler's wealth is a nonnegative "
            "martingale starting at one, the chance that it ever reaches twenty is at most one in twenty, ever, over "
            "the whole infinite future. <bookmark mark='a'/> Turn that into a test. State the null hypothesis as a "
            "claim that some game is fair. Let a gambler bet against it, never risking more than they have. If the "
            "null is true, the gambler's wealth is a nonnegative martingale, an e-process. <bookmark mark='b'/> "
            "Reject the null when the wealth reaches twenty. By Ville's inequality you will be wrong at most five "
            "percent of the time, however often you look, and whenever you decide to stop. Glenn Shafer and Vladimir "
            "Vovk rebuilt probability on this idea, and since 2020 it has become a field: anytime-valid inference."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()

    def peeking(self, p):
        n = p["n"]
        g1 = axes([0, n], [-4, 4], x_length=5.6, y_length=3.6, xlabel=r"days", ylabel=r"$t$-statistic, checked daily",
                  xticks=[0, 1000, 2000], yticks=[-4, -2, 0, 2, 4], font_size=16)
        g2 = axes([0, n], [-2, 2], x_length=5.6, y_length=3.6, xlabel=r"days", ylabel=r"e-process (log scale)",
                  xticks=[0, 1000, 2000], yticks=[-2, -1, 0, 1, 2], yfmt=lambda u: f"{10 ** u:g}", font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        a1, a2 = g1.ax, g2.ax
        k = np.arange(0, n, 10)[: len(p["show_z"][0])]
        zs = VGroup(*[curve(a1, k, np.clip(np.asarray(z), -4, 4), P_C, stroke_width=1.3).set_stroke(opacity=0.6)
                      for z in p["show_z"]])
        es = VGroup(*[curve(a2, k, np.clip(np.asarray(e), -2, 2), MART, stroke_width=1.3).set_stroke(opacity=0.6)
                      for e in p["show_loge"]])
        b1 = VGroup(DashedLine(a1.c2p(0, 1.96), a1.c2p(n, 1.96), color=LOSS, stroke_width=2),
                    DashedLine(a1.c2p(0, -1.96), a1.c2p(n, -1.96), color=LOSS, stroke_width=2))
        b2 = DashedLine(a2.c2p(0, np.log10(20)), a2.c2p(n, np.log10(20)), color=LOSS, stroke_width=2)
        r1 = MathTex(rf"\text{{ever rejects: }} {100 * p['t_reject']:.0f}\%", font_size=34, color=LOSS).next_to(g1, DOWN, buff=0.4)
        r2 = MathTex(rf"\text{{ever rejects: }} {100 * p['e_reject']:.1f}\%", font_size=34, color=MART).next_to(g2, DOWN, buff=0.4)
        cap = label(rf"{p['paths']:,} fair games of {n:,} days each; 30 shown".replace(",", "{,}"), font_size=21,
                    color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why does that matter? Because people look. Simulate two thousand perfectly fair games, each twenty-five "
            "hundred days long, about ten years of trading. Each day, test whether the game is fair with an ordinary "
            "t-test at the five percent level. <bookmark mark='a'/> The statistic wanders, and sooner or later "
            f"crosses the line. Half of these fair games, {100 * p['t_reject']:.0f} percent, are declared unfair at "
            "some point, just because someone checked every day. <bookmark mark='b'/> Now watch an e-process on the "
            f"same games. It reaches twenty in {100 * p['e_reject']:.1f} percent of them, under five, as Ville "
            "promised. A researcher, or a risk committee, that reviews a strategy every morning needs the second kind "
            "of test."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(cap), Create(b1), Create(b2))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(z) for z in zs], lag_ratio=0.05, run_time=4))
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in es], lag_ratio=0.05, run_time=4))
            self.play(FadeIn(r2))
        self.wait(0.4)
        self.clear_scene()

    def market(self, e):
        g = axes([0, 25], [-1, 6], x_length=7.6, y_length=4.4, xlabel=r"years since the bettor started",
                 ylabel=r"wealth from \$1 (log scale)", xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 2, 4, 6],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"19260701": P_C, "19750101": QC.GAIN, "20000101": MART, "btc": Q_C}
        names = {"19260701": r"US, from July 1926", "19750101": r"US, from 1975", "20000101": r"US, from 2000",
                 "btc": r"Bitcoin, from 2018"}
        lines, items = VGroup(), []
        for k, c in cols.items():
            t, l_ = np.asarray(e[k]["t"]), np.asarray(e[k]["loge"])
            m = (t - t[0]) <= 25
            lines.add(curve(ax, t[m] - t[0], np.clip(l_[m], -1, 6), c, stroke_width=2.6))
            cross = e[k]["cross"]
            tag = rf"past 20 in {str(cross)[:4]}" if cross else rf"max {e[k]['max']:.1f}"
            items.append((c, rf"{names[k]}: {tag}"))
        bar = DashedLine(ax.c2p(0, np.log10(20)), ax.c2p(25, np.log10(20)), color=LOSS, stroke_width=2)
        leg = legend(items, font_size=20)
        side = VGroup(
            leg,
            wrapped_label(r"the bet: today's return keeps yesterday's sign, with stakes sized by yesterday's volatility "
                          r"and capped, against the null that it can't be predicted", 4.6, 20, GREY_A),
            wrapped_label(r"the old index's positive autocorrelation (stale prices of small stocks, Part 1) was real; "
                          r"since 2000 there is nothing this bettor can collect", 4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        src = real_data(r"Kenneth French's daily US market; Binance BTCUSDT daily; the House's \texttt{EProcess}; "
                        r"curves clipped at $10^6$")
        with self.voiceover(
            "Back to the opening gambler, now as a test. The null hypothesis: yesterday's sign doesn't predict today's "
            "return. The bettor stakes a little each day on continuation or on reversal, sized by yesterday's "
            "volatility and capped, and the House's e-process mixes many such bettors. <bookmark mark='a'/> Started "
            "in 1926, it passes twenty within three years. Started in 1975, within fifteen months: the index's "
            "returns still kept their sign, partly because small stocks traded rarely, the stale prices of Part one. "
            "<bookmark mark='b'/> Started in 2000 it never gets there, and neither does a bettor on Bitcoin from 2018. "
            "<bookmark mark='c'/> Each of these verdicts is valid at every moment along the way, and it would have "
            "been valid had we stopped looking at any point. That is what anytime-valid means, and it is why the "
            "House's monitor is an e-process."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(bar), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(leg[:2]), run_time=3)
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(lines[2]), Create(lines[3]), FadeIn(leg[2:]), run_time=3)
            vo.wait_until("c")
            self.play(Indicate(bar, color=LOSS))
        self.wait(0.4)
        self.clear_scene()
