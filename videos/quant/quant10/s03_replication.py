from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import CASH, DEL, GAM, OPT, PART, PP, SPOT, THE

C_ = {r"X": CASH, r"\mu": PP, r"r": CASH, r"\partial_t V": THE, r"\partial_S V": DEL, r"\partial_{SS} V": GAM, r"dW": SPOT,
      r"\Delta": DEL, r"dS": SPOT, r"S": SPOT, r"dV": OPT, r"V": OPT, r"\tfrac12\sigma^2 S^2": GAM}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derive()
        self.why_mu()

    def card(self):
        c = chapter_card(2, r"The riskless portfolio", r"What is an option worth if it can be copied?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter two. The riskless portfolio."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def setup_(self):
        stock = row(r"dS", r"=", r"\mu", r"S\,dt", r"+", r"\sigma", r"S\,", r"dW", fs=44)
        bond = row(r"dB", r"=", r"r", r"B\,dt", fs=44)
        opt = row(r"V", r"=", r"V(t, S)", r"\;?", fs=44)
        labels = [label(r"the stock: a drift $\mu$ nobody knows, and noise of size $\sigma$", font_size=26,
                        color=GREY_A),
                  label(r"the bond: grows at the riskless rate $r$", font_size=26, color=GREY_A),
                  label(r"the option: some function of time and the stock price", font_size=26, color=GREY_A)]
        grp = VGroup()
        for m, l in zip((stock, bond, opt), labels):
            grp.add(VGroup(m, l).arrange(DOWN, buff=0.18))
        grp.arrange(DOWN, buff=0.6)
        assumptions = note(r"assumptions: trade continuously, no costs, borrow and lend at $r$, $\sigma$ known "
                           r"and constant", font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Three things can be traded. A stock, whose price follows the geometric Brownian motion of Part five: "
            "it drifts at an expected rate mu, which nobody knows, and jiggles with volatility sigma. "
            "<bookmark mark='a'/> A bond, or a bank account, which grows at the riskless interest rate r. "
            "<bookmark mark='b'/> And an option, whose value V depends on time and on the stock price, through a "
            "function we do not yet know. <bookmark mark='c'/> The assumptions are heroic, and each one will be "
            "dropped later in the series: you can trade continuously, at no cost, borrow and lend at r, and you "
            "know sigma. Each broken assumption becomes a chapter, of this part or a later one."
        ) as vo:
            self.play(FadeIn(grp[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(grp[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(grp[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(assumptions))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            row(r"dX", r"=", r"\Delta", r"\,", r"dS", r"+", r"r", r"\,(X", r"-", r"\Delta", r"S", r")\,dt"),
            row(r"dV", r"=", r"\big(", r"\partial_t V", r"+", r"\mu", r"S", r"\partial_S V", r"+",
                r"\tfrac12\sigma^2 S^2", r"\partial_{SS} V", r"\big)\,dt", r"+", r"\sigma S", r"\partial_S V",
                r"\,", r"dW"),
            row(r"dX", r"=", r"\big(", r"r", r"X", r"+", r"(", r"\mu", r"-", r"r", r")", r"\Delta", r"S", r"\big)\,dt",
                r"+", r"\sigma", r"\Delta", r"S", r"\,", r"dW"),
            row(r"\Delta", r"=", r"\partial_S V"),
            row(r"\partial_t V", r"+", r"r", r"S", r"\partial_S V", r"+", r"\tfrac12\sigma^2 S^2",
                r"\partial_{SS} V", r"-", r"r", r"V", r"=", r"0", fs=38),
        ]
        whys = [why(r"self-financing: $\Delta$ shares, the rest $X - \Delta S$ in the bank, no money in or out"),
                why(r"It\^o's lemma (Part 5)"),
                why(r"substitute $dS = \mu S\,dt + \sigma S\,dW$"),
                why(r"$X$ tracks $V$ path by path: the $dW$ terms must match"),
                why(r"then the $dt$ terms must match: the $\mu$ terms cancel")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.4, buff=0.55, edge=6.9)
        cond = note(r"with $V(T, S) = \max(S - K, 0)$: a portfolio started at $X_0 = V(0, S_0)$ ends at the payoff "
                    r"(Shreve II, \S4.5)", font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the argument, done properly. Build a portfolio X that holds delta shares and keeps the rest in the "
            "bank. It is self-financing: no money comes in or goes out, so it changes only by what the shares gain "
            "and what the bank pays. <bookmark mark='a'/> The option changes, by Ito's lemma, by a drift term, "
            "with the time derivative, mu times S times the slope, and half sigma squared S squared times the "
            "curvature, plus a noise term: sigma S times the slope, times the Brownian increment. "
            "<bookmark mark='b'/> Put the stock's own equation into the portfolio's change and it too has a "
            "drift and a noise term. <bookmark mark='c'/> If the portfolio is to copy the option on every path, "
            "the noise terms must agree, and that fixes the hedge: delta is the slope of the option's value. "
            "<bookmark mark='d'/> Then the drift terms must agree too. Write it out, and the terms with mu appear "
            "on both sides and cancel. What is left is the Black-Scholes equation. Black and Scholes argued "
            "that a hedged position is riskless, so it earns the riskless rate; Merton's self-financing copy "
            "reaches the same equation and is the version that survives scrutiny."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            br1 = Brace(VGroup(*rows[1][2:12]), DOWN, buff=0.08, color=GREY_B)
            br2 = Brace(VGroup(*rows[1][13:17]), DOWN, buff=0.08, color=SPOT)
            t1 = label(r"drift", font_size=24, color=GREY_B).next_to(br1, DOWN, buff=0.1)
            t2 = label(r"noise", font_size=24, color=SPOT).next_to(br2, DOWN, buff=0.1)
            self.play(FadeOut(whys[1]), GrowFromCenter(br1), FadeIn(t1), GrowFromCenter(br2), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(br1, br2, t1, t2)), FadeIn(whys[1]), run_time=0.6)
            step(2)
            vo.wait_until("c")
            self.play(Indicate(VGroup(*rows[1][13:17]), color=SPOT), Indicate(VGroup(*rows[2][15:20]), color=SPOT))
            step(3)
            vo.wait_until("d")
            mus = VGroup(term(rows[1], r"\mu"), term(rows[2], r"\mu"))
            self.play(Indicate(mus, color=PP, scale_factor=1.5))
            step(4)
            box = SurroundingRectangle(rows[4], color=OPT, buff=0.18, corner_radius=0.1)
            self.play(Create(box), FadeIn(cond))
        self.wait(0.4)
        self.pde = VGroup(rows[4], box)
        self.clear_scene(self.pde)

    # ------------------------------------------------------------------
    def why_mu(self):
        pde = self.pde
        self.play(pde.animate.scale(0.9).to_edge(UP, buff=0.4))
        bull = VGroup(label(r"an optimist: $\mu = 30\%$", font_size=28, color=PP),
                      label(r"a pessimist: $\mu = -10\%$", font_size=28, color=PP)).arrange(DOWN, buff=0.25)
        same = label(r"same hedge, same price", font_size=34, color=OPT)
        reason = wrapped_label(r"The hedge removes the direction. What is left is the size of the moves: "
                               r"$\tfrac12\Gamma\,\sigma^2 S^2$ per unit of time, the same in every opinion.",
                               9.5, 28, GREY_A)
        g = VGroup(bull, same, reason).arrange(DOWN, buff=0.6).next_to(pde, DOWN, buff=0.8)
        arrow = Arrow(bull.get_bottom(), same.get_top(), buff=0.1, color=GREY_B, stroke_width=3)
        with self.voiceover(
            "This is the surprise that took economists a decade to find. Two traders who disagree completely about "
            "where the stock is going, one expecting thirty percent a year and the other a loss, "
            "<bookmark mark='a'/> agree on the option's price, because both can manufacture it the same way and "
            "neither's opinion enters the manufacturing. Pause and ask yourself: why can the hedger ignore mu, but "
            "not sigma? Because the hedge removes the direction, and what is left is the size of the moves: the "
            "term with sigma squared and the curvature, gamma, which no position in the stock can cancel. That "
            "term is the whole economics of an options desk, and chapter seven is about it."
        ) as vo:
            self.play(FadeIn(bull, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(same, scale=1.1))
            self.play(FadeIn(reason))
        self.wait(0.3)
        self.clear_scene(pde)
