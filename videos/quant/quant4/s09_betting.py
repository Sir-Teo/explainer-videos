from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, MART, P_C, PART, Q_C, load, real_data


class Betting(VoiceoverScene):
    def construct(self):
        p = load("peeking")
        pc = load("peeking_curve")
        e = load("eprocess")
        self.card()
        self.ville()
        self.proof()
        self.peeking(p, pc)
        self.game()
        self.market(e)

    def card(self):
        c = chapter_card(15, r"Ville's inequality and testing by betting", r"How do you test a market you watch every "
                         r"day?", part=PART)
        with self.voiceover("Chapter fifteen. Ville's inequality, and testing by betting."):
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

    def peeking(self, p, pc):
        n = p["n"]
        g1 = axes([0, n], [-4, 4], x_length=5.6, y_length=3.6, xlabel=r"days", ylabel=r"$t$-statistic, checked daily",
                  xticks=[0, 1000, 2000], yticks=[-4, -2, 0, 2, 4], font_size=16)
        g2 = axes([0, n], [-2, 2], x_length=5.6, y_length=3.6, xlabel=r"days", ylabel=r"e-process (log scale)",
                  xticks=[0, 1000, 2000], yticks=[-2, -1, 0, 1, 2], yfmt=lambda u: f"{10 ** u:g}", font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        a1, a2 = g1.ax, g2.ax
        k = np.arange(0, n, 10)[: len(p["show_z"][0])]
        tk = ValueTracker(0.0)
        zs = VGroup(*[tracing(a1, k, np.clip(np.asarray(z), -4, 4), tk, P_C, stroke_width=1.3)
                      for z in p["show_z"]])
        es = VGroup(*[tracing(a2, k, np.clip(np.asarray(e), -2, 2), tk, MART, stroke_width=1.3)
                      for e in p["show_loge"]])
        days = np.asarray(pc["days"], float)
        tf, ef = np.asarray(pc["t_frac"]), np.asarray(pc["e_frac"])
        c1 = readout(r"\text{rejected so far:}", lambda: 100 * float(np.interp(at_index(k, tk), days, tf)), digits=1,
                     font_size=26, color=LOSS, unit=r"\%").next_to(g1, UP, buff=0.1)
        c2 = readout(r"\text{rejected so far:}", lambda: 100 * float(np.interp(at_index(k, tk), days, ef)), digits=1,
                     font_size=26, color=MART, unit=r"\%").next_to(g2, UP, buff=0.1)
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
            self.add(zs, c1)
            self.play(tk.animate.set_value(float(len(k) - 1)), run_time=6, rate_func=linear)
            for m_ in (*zs, c1):
                m_.clear_updaters()
            self.play(FadeIn(r1))
            vo.wait_until("b")
            tk.set_value(0.0)
            self.add(es, c2)
            self.play(tk.animate.set_value(float(len(k) - 1)), run_time=6, rate_func=linear)
            for m_ in (*es, c2):
                m_.clear_updaters()
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

    def proof(self):
        rows = [cmath(r"\tau = \inf\{n : W_n \ge c\}", r",", r"\quad W \ge 0,\ W_0 = 1,\ \text{a supermartingale}",
                      font_size=38),
                cmath(r"1 \ge \mathbb{E}W_{\tau \wedge n}", r"\ge", r"c\,P(\tau \le n)", font_size=40),
                cmath(r"P\big(\sup_n W_n \ge c\big)", r"\le", r"\frac{1}{c} \quad (c = 1/\alpha:\ \le \alpha)", font_size=40,
                      colors={r"\frac{1}{c} \quad (c = 1/\alpha:\ \le \alpha)": MART}),
                cmath(r"E \ge 0,\ \mathbb{E}_{H_0}E \le 1", r"\Rightarrow", r"P(E \ge 1/\alpha) \le \alpha; \quad "
                      r"p \mapsto \kappa p^{\kappa - 1} \text{ is an e-value}", font_size=36),
                cmath(r"\limsup_n \frac{|S_n|}{\sqrt{2n\log\log n}}", r"=", r"1 \;\Rightarrow\; |z_n| > 1.96 "
                      r"\text{ infinitely often}", font_size=36, colors={r"1 \;\Rightarrow\; |z_n| > 1.96 \text{ infinitely often}": LOSS})]
        whys = [why(r"the first time the gambler's wealth reaches $c$: a stopping time"),
                why(r"optional stopping at the bounded time $\tau \wedge n$ (chapter 6); on $\{\tau \le n\}$ the wealth is at "
                    r"least $c$, elsewhere at least 0"),
                why(r"let $n \to \infty$: Ville's inequality (1939), the maximal inequality of a nonnegative martingale"),
                why(r"an e-value is one bet's payoff: Markov's inequality; any p-value can be calibrated into one "
                    r"(Vovk and Wang 2021)"),
                why(r"the law of the iterated logarithm: a $t$-test checked forever rejects a true null with probability one")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.7, edge=6.9)
        with self.voiceover(
            "The proof uses only what you have. Let tau be the first time wealth reaches c. <bookmark mark='a'/> "
            "Stop at tau or n: optional stopping keeps the mean at most one, and on the event that tau came first "
            "the wealth is at least c. <bookmark mark='b'/> Let n run to infinity: Ville's inequality. "
            "<bookmark mark='c'/> A single bet's payoff with mean at most one under the null is an e-value, a test by "
            "Markov's inequality. <bookmark mark='d'/> And the law of the iterated logarithm says a fair walk's "
            "statistic crosses one point nine six forever: check daily and you eventually reject a true null."
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

    def game(self):
        players = VGroup()
        for name, what, col in ((r"Forecaster", r"announces a price for tomorrow (a mean, a probability)", P_C),
                                (r"Skeptic", r"bets against it, any amount, never risking more than it has", MART),
                                (r"Reality", r"moves; Skeptic's capital is settled", Q_C)):
            box = RoundedRectangle(width=3.6, height=1.9, corner_radius=0.15, stroke_color=col, stroke_width=2.5)
            t = VGroup(label(name, font_size=30, color=col), wrapped_label(what, 3.1, 20, GREY_A)).arrange(
                DOWN, buff=0.15).move_to(box)
            players.add(VGroup(box, t))
        players.arrange(RIGHT, buff=0.8).shift(UP * 0.8)
        arrows = VGroup(*[Arrow(players[i].get_right(), players[i + 1].get_left(), buff=0.1, color=GREY_B)
                          for i in range(2)])
        loop = CurvedArrow(players[2].get_bottom() + DOWN * 0.1, players[0].get_bottom() + DOWN * 0.1, angle=-0.6,
                           color=GREY_C)
        claim = wrapped_label(r"a probability statement is a claim that Skeptic cannot multiply its capital by a large "
                              r"factor; the forecasts are valid exactly when no strategy gets rich against them",
                              11.4, 23, QC.IDEA).to_edge(DOWN, buff=0.5)
        hist = history_card(2001, r"Shafer and Vovk, \textit{Probability and Finance: It's Only a Game!}",
                            r"probability built on betting instead of measure; \textit{Game-Theoretic Foundations for "
                            r"Probability and Finance} (2019)", width=8.0).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Shafer and Vovk rebuilt probability as a game. <bookmark mark='a'/> Forecaster announces prices, "
            "Skeptic bets against them without risking more than it has, Reality moves. <bookmark mark='b'/> "
            "Forecasts are good exactly when no strategy gets rich against them."
            " The skeptic still has to choose its bets. Next: learning them."
        ) as vo:
            self.play(FadeIn(hist))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(players[0]), GrowArrow(arrows[0]), FadeIn(players[1]), GrowArrow(arrows[1]),
                                  FadeIn(players[2]), lag_ratio=0.4), run_time=3)
            self.play(Create(loop))
            vo.wait_until("b")
            self.play(FadeIn(claim))
        self.wait(0.4)
        self.clear_scene()
