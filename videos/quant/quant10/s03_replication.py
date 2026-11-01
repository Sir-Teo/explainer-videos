from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import CASH, DEL, GAM, OPT, PART, PP, SPOT, THE

C_ = {r"\mu": PP, r"r": CASH, r"\partial_t V": THE, r"\partial_S V": DEL, r"\partial_{SS} V": GAM, r"dW": SPOT,
      r"\Delta": DEL, r"dS": SPOT, r"S": SPOT, r"dV": OPT, r"V": OPT, r"\tfrac12\sigma^2 S^2": GAM}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derive()
        self.why_mu()
        self.heat()

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
            row(r"dV", r"=", r"\big(", r"\partial_t V", r"+", r"\mu", r"S", r"\partial_S V", r"+",
                r"\tfrac12\sigma^2 S^2", r"\partial_{SS} V", r"\big)\,dt", r"+", r"\sigma S", r"\partial_S V",
                r"\,", r"dW"),
            row(r"d\Pi", r"=", r"\big(", r"\partial_t V", r"+", r"\mu", r"S", r"(", r"\partial_S V", r"-",
                r"\Delta", r")", r"+", r"\tfrac12\sigma^2 S^2", r"\partial_{SS} V", r"\big)\,dt", r"+",
                r"\sigma S", r"(", r"\partial_S V", r"-", r"\Delta", r")", r"\,", r"dW"),
            row(r"d\Pi", r"=", r"\big(", r"\partial_t V", r"+", r"\tfrac12\sigma^2 S^2", r"\partial_{SS} V",
                r"\big)\,dt"),
            row(r"d\Pi", r"=", r"r", r"\,\Pi\,dt", r"=", r"r", r"(", r"V", r"-", r"S", r"\partial_S V", r")",
                r"\,dt"),
            row(r"0", r"=", r"\partial_t V", r"+", r"r", r"S", r"\partial_S V", r"+", r"\tfrac12\sigma^2 S^2",
                r"\partial_{SS} V", r"-", r"r", r"V", fs=38),
        ]
        whys = [why(r"It\^o's lemma (Part 5)"), why(r"hold the option, short $\Delta$ shares: $\Pi = V - \Delta S$"),
                why(r"choose $\Delta = \partial_S V$: the $dW$ term and $\mu$ vanish"),
                why(r"riskless, so it must earn $r$ (else: arbitrage)"),
                why(r"equate the two: the Black--Scholes PDE")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Now the argument. By Ito's lemma, a small change in the option's value has a drift term, with the "
            "time derivative, the expected growth mu times the slope, and one half sigma squared S squared times "
            "the curvature; and a noise term, sigma S times the slope, times the Brownian increment. "
            "<bookmark mark='a'/> Hold one option and sell delta shares of the stock. The portfolio Pi changes "
            "by the option's change minus delta times the stock's. Both the drift and the noise now contain the "
            "slope minus delta. <bookmark mark='b'/> So choose delta equal to the slope. The noise disappears: "
            "over the next instant this portfolio's change is certain. And look what else disappeared with it. "
            "Mu. The only place the stock's expected return entered was multiplied by slope minus delta. "
            "<bookmark mark='c'/> A portfolio whose change is certain must earn the riskless rate, or there is "
            "an arbitrage: if it earned more, borrow at r and buy it; if less, sell it and lend. So its change is "
            "r times its value, the option minus S times the slope. <bookmark mark='d'/> Set the two "
            "expressions equal, and out comes the Black-Scholes equation: a partial differential equation for "
            "the option's value, in which the stock's expected return does not appear."
        ) as vo:
            step(0)
            br1 = Brace(VGroup(*rows[0][2:12]), DOWN, buff=0.08, color=GREY_B)
            br2 = Brace(VGroup(*rows[0][13:17]), DOWN, buff=0.08, color=SPOT)
            t1 = label(r"drift: certain", font_size=24, color=GREY_B).next_to(br1, DOWN, buff=0.1)
            t2 = label(r"noise: random", font_size=24, color=SPOT).next_to(br2, DOWN, buff=0.1)
            self.play(FadeOut(whys[0]), GrowFromCenter(br1), FadeIn(t1))
            self.play(GrowFromCenter(br2), FadeIn(t2))
            vo.wait_until("a")
            self.play(FadeOut(VGroup(br1, br2, t1, t2)), FadeIn(whys[0]), run_time=0.6)
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            box = SurroundingRectangle(rows[4], color=OPT, buff=0.18, corner_radius=0.1)
            self.play(Create(box))
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
            "neither's opinion enters the manufacturing. The hedge removes the direction. What is left is the size "
            "of the moves: the term with sigma squared and the curvature, gamma. That term is the whole economics "
            "of an options desk, and chapter six is about it."
        ) as vo:
            self.play(FadeIn(bull, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(same, scale=1.1))
            self.play(FadeIn(reason))
        self.wait(0.3)
        self.clear_scene(pde)

    # ------------------------------------------------------------------
    def heat(self):
        pde = self.pde
        K, r, sig = 100.0, 0.05, 0.25
        ax_g = axes([50, 150], [0, 55], x_length=8.4, y_length=4.0, xlabel=r"stock price $S$",
                    ylabel=r"option value $V$", xticks=[50, 100, 150], yticks=[0, 25, 50], font_size=20)
        ax_g.to_edge(DOWN, buff=0.55).shift(LEFT * 1.5)
        ax = ax_g.ax
        tau = ValueTracker(0.0)
        xs = np.linspace(50, 150, 241)
        payoff = curve(ax, [50, 100, 150], [0, 0, 50], GREY_B, stroke_width=2.5)
        payoff_dash = DashedVMobject(payoff, num_dashes=50)

        def curve_now():
            t = max(tau.get_value(), 1e-6)
            return curve(ax, xs, bs.price(xs, K, t, sig, r), OPT, stroke_width=4)

        V = always_redraw(curve_now)
        dot = always_redraw(lambda: glow_dot(ax.c2p(110, float(bs.price(110, K, max(tau.get_value(), 1e-6), sig, r))),
                                             color=DEL, radius=0.06))

        def tangent():
            t = max(tau.get_value(), 1e-6)
            v0 = float(bs.price(110, K, t, sig, r))
            d = float(bs.greeks(110, K, t, sig, r)["delta"])
            return Line(ax.c2p(96, v0 - 14 * d), ax.c2p(124, v0 + 14 * d), color=DEL, stroke_width=3)

        tan = always_redraw(tangent)
        tlab = always_redraw(lambda: MathTex(rf"T - t = {tau.get_value():.2f}", font_size=30, color=THE)
                             .next_to(ax_g, RIGHT, buff=0.4).shift(UP * 1.2))
        dlab = always_redraw(lambda: MathTex(rf"\Delta = {float(bs.greeks(110, K, max(tau.get_value(), 1e-6), sig, r)['delta']):.2f}",
                                             font_size=30, color=DEL).next_to(tlab, DOWN, buff=0.35).align_to(tlab, LEFT))
        cond = cmath(r"V(T, S) = \max(S - K,\, 0)", font_size=30, color=GREY_B).next_to(dlab, DOWN, buff=0.5)
        cond.align_to(tlab, LEFT)
        params = note(r"$K = 100$, $r = 5\%$, $\sigma = 25\%$", font_size=20).next_to(cond, DOWN, buff=0.3)
        params.align_to(tlab, LEFT)
        with self.voiceover(
            "What does the equation do? It runs backwards from expiry. At maturity the option is worth its payoff, "
            "the grey hockey stick. <bookmark mark='a'/> Step back in time and the equation smooths it, the way "
            "heat spreads along a rod: in fact, after a change of variables, to log price and time remaining, it "
            "is exactly the heat equation. The kink at the strike melts into a curve. <bookmark mark='b'/> The "
            "slope of that curve at the current price, the yellow line, is delta: the number of shares in the "
            "hedge. And the curve sits above the payoff everywhere, by more the longer there is to go, because the "
            "right to wait is worth something. One year out, here is the price of a call with strike one hundred "
            "when the stock is at one hundred and ten. Solving this equation with this terminal condition gives "
            "the formula; the next chapter gets there by a different road."
        ) as vo:
            self.play(FadeIn(ax_g), Create(payoff_dash), FadeIn(cond), FadeIn(params))
            vo.wait_until("a")
            self.add(V)
            self.play(tau.animate.set_value(0.25), FadeIn(tlab), run_time=3)
            vo.wait_until("b")
            self.add(tan, dot)
            self.play(FadeIn(dlab))
            self.play(tau.animate.set_value(1.0), run_time=max(vo.remaining(1.0) - 1.0, 4.0), rate_func=smooth)
        self.wait(0.4)
        self.clear_scene()
