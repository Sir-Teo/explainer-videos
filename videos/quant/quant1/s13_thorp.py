from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAIN, GAUSS, LOSS, PART, REAL, hist_bars, load


class Thorp(VoiceoverScene):
    def construct(self):
        b = load("betting")
        self.card()
        self.doubling(b)
        self.stopping(b)
        self.counting(b)
        self.fund()

    def card(self):
        c = chapter_card(12, r"Beating the dealer", r"Can a fair game be beaten?", lit=(1962, 1967, 1969), part=PART)
        with self.voiceover("Chapter twelve. Beating the dealer."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def doubling(self, b):
        path = np.asarray(b["path"])
        n = len(path)
        lo = float(min(path.min(), -1100))
        hi = float(path.max() + 200)
        g = axes([0, n], [lo, hi], x_length=8.6, y_length=4.4, xlabel=r"sessions played",
                 ylabel=r"total winnings, \$", xticks=[0, 1000, 2000, 3000],
                 yticks=[v for v in (-2000, -1500, -1000, -500, 0, 500, 1000) if lo <= v <= hi],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, np.arange(1, n + 1), path, QC.IDEA, stroke_width=2.5)
        rule = VGroup(
            label(r"The doubling system, on a fair coin:", font_size=24),
            label(r"bet \$1; after a loss, double; stop at the first win", font_size=22, color=GREY_A),
            label(r"each session wins \$1, unless 10 losses in a row", font_size=22, color=GREY_A),
            label(r"empty the \$1{,}023 bankroll", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        res = VGroup(
            MathTex(rf"\text{{ruin: }}{100 * b['p_ruin']:.2f}\%\ \text{{of sessions}}", font_size=30, color=LOSS),
            MathTex(rf"\text{{average session: }}{b['mean_session']:+.2f} \pm {b['se_session']:.2f}", font_size=30),
            label(r"200{,}000 simulated sessions", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(rule, DOWN, buff=0.6).align_to(rule, LEFT)
        with self.voiceover(
            "Can a fair game be beaten by cleverness about how you bet? The oldest system is doubling, the "
            "martingale of the gambling halls, which gave the mathematical word its name. Bet a dollar on a fair "
            "coin. If you lose, double the bet. Stop at the first win. Every session ends one dollar up, unless you "
            "lose ten times in a row and your bankroll of a thousand and twenty-three dollars is gone. "
            "<bookmark mark='a'/> Here are three thousand sessions. Win, win, win, a staircase of dollars, for "
            "hundreds of sessions, and then a cliff. <bookmark mark='b'/> In two hundred thousand sessions, the "
            "average comes out at zero, within the noise. The system doesn't change the expected value. It changes "
            "the shape: many small wins, rare enormous losses. You will meet that shape again, in short volatility, "
            "in carry trades, in every strategy that looks too smooth."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(line), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def stopping(self, b):
        thm = theorem_card(r"The optional stopping theorem (Doob)", r"For a martingale $X$ and a stopping rule $\tau$ "
                           r"that can't see the future and doesn't run forever (or bets that are bounded), "
                           r"$\mathbb E[X_\tau] = X_0$. No rule for when to stop, or how much to bet, turns a fair game "
                           r"into a favourable one.", width=11.4, font_size=24).to_edge(UP, buff=0.45)
        cells = [label(r"stop when up", font_size=24, color=GREY_A), label(r"chance of reaching it", font_size=24,
                                                                              color=GREY_A),
                 label(r"average result", font_size=24, color=GREY_A), label(r"worst result", font_size=24,
                                                                              color=GREY_A)]
        for r_ in b["rules"]:
            cells += [MathTex(rf"+{r_['a']}", font_size=32), MathTex(rf"{100 * r_['p_hit']:.0f}\%", font_size=32,
                                                                      color=GAIN),
                      MathTex(rf"{r_['mean']:+.2f} \pm {r_['se']:.2f}", font_size=32),
                      MathTex(rf"{r_['worst']}", font_size=32, color=LOSS)]
        tab = VGroup(*cells).arrange_in_grid(len(b["rules"]) + 1, 4, buff=(0.8, 0.3), col_alignments="rrrr")
        tab.next_to(thm, DOWN, buff=0.6)
        foot = note(r"a fair $\pm 1$ coin game, at most 200 tosses; 100{,}000 players for each rule", font_size=18)
        foot.next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "This is a theorem, and its name is the optional stopping theorem. For a martingale, any stopping rule "
            "that can't see the future and can't go on forever leaves the expected value where it started. "
            "<bookmark mark='a'/> Quit when you're one dollar up: you get there ninety-four times in a hundred, and "
            "your average result is still zero, because the other six times hurt. Quit at three, quit at ten: "
            "different shapes, the same zero. The same mathematics that made prices unpredictable in chapter three "
            "makes betting systems useless. To beat a fair game you need the game not to be fair."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self, b):
        e = np.asarray(b["tc_edges"])
        h = np.asarray(b["tc_hist"])
        g = axes([-8.5, 8.5], [0, 0.42], x_length=7.6, y_length=4.2, xlabel=r"the true count before the hand",
                 ylabel=r"share of hands", xticks=[-8, -4, 0, 4, 8], yticks=[0, 0.1, 0.2, 0.3, 0.4],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        cols = [GAIN if (a + b_) / 2 >= 1.0 else GAUSS for a, b_ in zip(e[:-1], e[1:])]
        bb = VGroup()
        for (a, b_, v), c in zip(zip(e[:-1], e[1:], h), cols):
            bb.add(hist_bars(ax, [a, b_], [v], c, opacity=0.8))
        # the player's edge against the count: a second y-axis on the right
        tc = np.linspace(-5, 8, 50)
        edge_y = lambda x: 0.21 + (-0.005 + 0.005 * x) * 6.0  # 1% of edge -> 0.06 of axis height
        el = curve(ax, tc, edge_y(tc), QC.IDEA, stroke_width=3.5)
        zero_e = DashedLine(ax.c2p(-8.5, edge_y(1.0) - 0.0), ax.c2p(8.5, edge_y(1.0)), color=QC.IDEA, stroke_width=1.5)
        zero_e = DashedLine(ax.c2p(-8.5, 0.21 + 0.0), ax.c2p(8.5, 0.21), color=QC.IDEA, stroke_width=1.2)
        el_lab = label(r"player's edge, about $0.5\%$ per count", font_size=20, color=QC.IDEA).next_to(
            ax.c2p(8.5, edge_y(8)), LEFT, buff=0.1).shift(UP * 0.25)
        zl = label(r"edge 0", font_size=18, color=QC.IDEA).next_to(ax.c2p(-8.5, 0.21), RIGHT, buff=0.05).shift(UP * 0.15)
        card = history_card(1962, r"Edward Thorp, \textit{Beat the Dealer}",
                            r"blackjack is dealt from a shoe without replacement: the cards still to come change the "
                            r"odds, hand by hand. Count them, and bet big only when the game favours you.",
                            width=5.2, font_size=21).to_edge(RIGHT, buff=0.35).shift(UP * 1.5)
        res = VGroup(
            MathTex(rf"\text{{hands that favour the player: }}{100 * b['frac_positive']:.0f}\%", font_size=28, color=GAIN),
            MathTex(rf"\text{{flat bets: }}{100 * b['edge_flat']:+.2f}\%", font_size=28, color=LOSS),
            MathTex(rf"\text{{bets of 1 to 8 by count: }}{100 * b['edge_spread_per_unit']:+.2f}\%", font_size=28,
                    color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(card, DOWN, buff=0.4).align_to(card, LEFT)
        foot = note(r"simulated six-deck shoes dealt to 75\%; Hi-Lo true counts; the edge per count is the standard "
                    r"approximation", font_size=17).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "In 1961 a young mathematician, Edward Thorp, showed that one casino game is not fair. Blackjack is "
            "dealt from a shoe, without replacement. Cards that have gone are gone, so the cards still to come change "
            "the odds from hand to hand. When many small cards have been played, the remaining shoe is rich in tens "
            "and aces, and the player has the edge. <bookmark mark='a'/> Here is a simulation of six-deck shoes, "
            "with a running count that tracks the balance of big and small cards. Most hands, the grey bars, favour "
            f"the house. About {100 * b['frac_positive']:.0f} percent, in green, favour the player. "
            "<bookmark mark='b'/> Bet the same on every hand and you lose about half a percent: the house edge. Bet "
            "one unit when the count is low and up to eight when it is high, and the game turns: "
            f"{100 * b['edge_spread_per_unit']:+.2f} percent of everything you bet. Small, but positive, and a "
            "professional plays thousands of hands. A fair game was not made favourable by a betting system. The "
            "information was the edge; the betting only used it. Thorp's book, Beat the Dealer, became a "
            "bestseller, and casinos changed their rules: more decks, earlier shuffles."
        ) as vo:
            self.play(FadeIn(card, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(x) for x in bb], lag_ratio=0.05))
            self.play(Create(zero_e), FadeIn(zl), Create(el), FadeIn(el_lab))
            self.play(FadeIn(res[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
            self.play(FadeIn(res[2]))
        self.wait(0.4)
        self.clear_scene()

    def fund(self):
        f = firm_card(r"Princeton Newport Partners (1969--1988)",
                      r"Edward Thorp and Jay Regan's fund: hedged positions in warrants, convertible bonds and options, "
                      r"priced with Thorp's own formulas (Part 10); later statistical arbitrage (Part 33).",
                      [(r"19.1\%", r"a year before fees"), (r"15.1\%", r"after fees"),
                       (r"10.2\%", r"the S\&P 500, same years")],
                      r"as reported by Thorp, \textit{A Man for All Markets} (2017)", width=7.4, font_size=23)
        f.to_edge(LEFT, buff=0.6)
        thread = VGroup(label(r"Thorp's thread through the series:", font_size=24, color=GREY_A),
                        label(r"Part 8: how much to bet (Kelly)", font_size=24),
                        label(r"Part 10: his warrant formula, before Black--Scholes", font_size=24),
                        label(r"Part 33: the first statistical arbitrage", font_size=24),
                        label(r"Part 43: can you beat the market?", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        thread.to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Thorp took the same idea to Wall Street. His fund, Princeton Newport Partners, run with Jay Regan from "
            "1969 to 1988, hedged warrants and convertible bonds using his own pricing formulas. By his account it "
            "returned nineteen point one percent a year before fees and fifteen point one after, against ten point "
            "two for the S and P five hundred. <bookmark mark='a'/> He will keep "
            "coming back. In Part eight, for his answer to how much to bet. In Part ten, for the warrant formula "
            "he used before Black and Scholes published theirs. In Part thirty-three, as an early statistical "
            "arbitrageur. And in the finale, where the question of this part comes back: can you beat the market?"
            " Next: a month when the tails of this part came true, March 2020."
        ) as vo:
            self.play(FadeIn(f, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in thread], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
