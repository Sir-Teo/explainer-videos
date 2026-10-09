from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import boxed, density, hist_shape, label, load, mtex, note, num, part_card, polyline
from videos.stochastic.compute import BS, bs_call


class BlackScholes(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_option()
        self.hedge()
        self.solution()
        self.replicate()
        self.errors()

    def card(self):
        c = part_card(5, r"Pricing and changing the odds", r"Black--Scholes and Girsanov")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def setup_option(self):
        K = BS["K"]
        sde = MathTex(r"dS", r"=", r"\mu S\,dt", r"+", r"\sigma S\,dW", font_size=40).to_corner(UL, buff=0.45)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        ax = Axes(x_range=[50, 150, 25], y_range=[0, 50, 10], x_length=6.2, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.6)
        xl = MathTex(r"S_T", font_size=30, color=C.BROWNIAN).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = label(r"payoff", font_size=26, color=C.OPTION).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        kl = MathTex("K", font_size=30).next_to(ax.c2p(K, 0), DOWN, buff=0.12)
        payoff = VMobject(color=C.OPTION, stroke_width=5)
        payoff.set_points_as_corners([ax.c2p(50, 0), ax.c2p(K, 0), ax.c2p(150, 50)])
        pf = MathTex(r"(S_T - K)^+", font_size=36, color=C.OPTION).next_to(ax.c2p(140, 40), LEFT, buff=0.2)
        what = label(r"a call option: the right, not the obligation,\\to buy the stock at price $K$ at time $T$",
                     font_size=28).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        q = MathTex(r"V(t, S)", r"=", r"\;?", font_size=44).next_to(what, DOWN, buff=0.6)
        q[0].set_color(C.OPTION)
        itov = MathTex(r"dV", r"=", r"\Big(V_t + \mu S V_S + \tfrac12\sigma^2 S^2 V_{SS}\Big)\,dt", r"+",
                       r"\sigma S\, V_S\, dW", font_size=34).to_edge(DOWN, buff=0.6).shift(RIGHT * 2.2)
        itov[2].set_color(C.DRIFT)
        itov[4].set_color(C.BROWNIAN)
        itol = label(r"It\^o's lemma, with $X = S$", font_size=24, color=GREY_B).next_to(itov, UP, buff=0.12)

        with self.voiceover(
            "Here's the application that made stochastic calculus famous. <bookmark mark='s'/> A stock follows geometric "
            "Brownian motion. <bookmark mark='o'/> A call option gives you the right, but not the obligation, to buy the "
            "stock at a fixed price K at a future time T. <bookmark mark='p'/> If the stock ends above K, you collect the "
            "difference; if not, you walk away with nothing. <bookmark mark='q'/> What is that right worth today?"
        ) as vo:
            self.play(Write(sde))
            vo.wait_until("o")
            self.play(FadeIn(what))
            vo.wait_until("p")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(kl))
            self.play(Create(payoff), FadeIn(pf))
            vo.wait_until("q")
            self.play(Write(q))
        with self.voiceover(
            "Call its value V, a function of time and the stock price. <bookmark mark='i'/> Itô's lemma tells us how V "
            "changes: a drift part, which includes the curvature term one half sigma squared S squared V S S, and a noise "
            "part, sigma S V S d W."
        ) as vo:
            vo.wait_until("i")
            self.play(Write(itov), FadeIn(itol))
        self.wait(0.3)
        self.play(FadeOut(VGroup(ax, xl, yl, kl, payoff, pf, what, q, itol)), itov.animate.to_edge(UP, buff=1.3).set_x(0),
                  sde.animate.to_corner(UL, buff=0.35))
        self.itov, self.sde = itov, sde

    # ------------------------------------------------------------------
    def hedge(self):
        itov = self.itov
        port = MathTex(r"\Pi", r"=", r"V", r"-", r"\Delta\, S", font_size=40).next_to(itov, DOWN, buff=0.45)
        port[0].set_color(C.HEDGE)
        portl = label(r"own the option, and sell $\Delta$ shares of the stock", font_size=24, color=GREY_B)
        portl.next_to(port, RIGHT, buff=0.4)
        dpi = MathTex(r"d\Pi", r"=", r"\Big(V_t + \mu S\,(V_S - \Delta) + \tfrac12\sigma^2S^2V_{SS}\Big)\,dt", r"+",
                      r"\sigma S\,(V_S - \Delta)\,dW", font_size=34).next_to(port, DOWN, buff=0.4)
        dpi[0].set_color(C.HEDGE)
        dpi[4].set_color(C.BROWNIAN)
        choose = MathTex(r"\Delta = V_S:", r"\qquad d\Pi", r"=", r"\Big(V_t + \tfrac12\sigma^2 S^2 V_{SS}\Big)\,dt",
                         font_size=38).next_to(dpi, DOWN, buff=0.45)
        choose[0].set_color(C.STAKE)
        gone = label(r"the noise is gone \ --- \ and so is $\mu$", font_size=28, color=C.QV).next_to(choose, DOWN, buff=0.2)
        riskless = MathTex(r"\text{riskless} \Rightarrow \; d\Pi", r"=", r"r\,\Pi\,dt", r"=", r"r\,(V - S V_S)\,dt",
                           font_size=36).next_to(gone, DOWN, buff=0.35)
        bs = MathTex(r"V_t", r"+", r"r S V_S", r"+", r"\tfrac12\sigma^2 S^2 V_{SS}", r"-", r"rV", r"=", r"0", font_size=44)
        bs[4].set_color(C.QV)
        bsb = boxed(bs, color=C.OPTION, buff=0.25).to_edge(DOWN, buff=0.35)
        bsb.shift(UP * 0.3)
        bsn = label(r"the Black--Scholes equation (1973)", font_size=26, color=C.OPTION).next_to(bsb, DOWN, buff=0.12)
        crossed = Cross(dpi[4], stroke_color=C.RIGHT_PT, stroke_width=4)

        with self.voiceover(
            "Black and Scholes, with Robert Merton, had a brilliant idea: hedge. <bookmark mark='p'/> Hold the option, and "
            "sell delta shares of the stock. <bookmark mark='d'/> The portfolio's change is the option's change minus delta "
            "times the stock's change. Both have noise in them, sigma S d W, and both have the drift mu."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(port), FadeIn(portl))
            vo.wait_until("d")
            self.play(Write(dpi), run_time=2.5)
        with self.voiceover(
            "<bookmark mark='c'/> Now choose delta to be exactly V S, the option's sensitivity to the stock. "
            "<bookmark mark='x'/> The noise term cancels. And so does mu: the stock's expected return has dropped out "
            "entirely. <bookmark mark='g'/> What's left is perfectly predictable."
        ) as vo:
            vo.wait_until("c")
            self.play(Indicate(dpi[2], color=C.STAKE), Indicate(dpi[4], color=C.STAKE))
            vo.wait_until("x")
            self.play(Create(crossed))
            vo.wait_until("g")
            self.play(Write(choose), FadeIn(gone))
        with self.voiceover(
            "A riskless portfolio must earn the risk-free interest rate, r, or there'd be free money to be made. "
            "<bookmark mark='r'/> Set the two equal, and rearrange: <bookmark mark='b'/> V t plus r S V S, plus one half "
            "sigma squared S squared V S S, minus r V, equals zero. That's the Black–Scholes equation. "
            "<bookmark mark='i'/> And the term that makes it work, the curvature term, is Itô's correction."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(riskless))
            vo.wait_until("b")
            self.play(Write(bs), Create(bsb[0]), FadeIn(bsn))
            vo.wait_until("i")
            self.play(Circumscribe(bs[4], color=C.QV))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def solution(self):
        d = load("hedge")
        price, mc, se = (float(x) for x in d["price"])
        S0, K, r, sig, T = BS["S0"], BS["K"], BS["r"], BS["sigma"], BS["T"]
        fk = MathTex(r"V(t, S)", r"=", r"e^{-r(T-t)}\;\mathbb E\big[(S_T - K)^+\big]", r",\quad",
                     r"dS = r S\,dt + \sigma S\,dW", font_size=36).to_edge(UP, buff=0.4)
        fk[0].set_color(C.OPTION)
        fk[4].set_color(C.DRIFT)
        fkn = label(r"Feynman--Kac: as if the stock grew at the rate $r$ \ (the ``risk-neutral'' world)", font_size=24,
                    color=GREY_B).next_to(fk, DOWN, buff=0.12)
        closed = MathTex(r"V", r"=", r"S\,N(d_1) - K e^{-r(T-t)} N(d_2)", font_size=34).next_to(fkn, DOWN, buff=0.3)
        closed[0].set_color(C.OPTION)
        dl = MathTex(r"d_{1,2} = \frac{\ln(S/K) + (r \pm \tfrac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}", font_size=28,
                     color=GREY_A).next_to(closed, DOWN, buff=0.15)
        ax = Axes(x_range=[60, 140, 20], y_range=[0, 45, 10], x_length=6.4, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_corner(DL, buff=0.6)
        ticks = VGroup(*[MathTex(f"{v}", font_size=22).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (60, 100, 140)])
        xl = MathTex("S", font_size=28, color=C.BROWNIAN).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        Ss = np.linspace(60, 140, 200)
        curves = VGroup()
        taus = [1.0, 0.5, 0.25, 0.08, 0.0]
        for i, tau in enumerate(taus):
            v, _ = bs_call(Ss, K, r, sig, tau)
            c = polyline(ax, Ss, v, color=C.OPTION, stroke_width=4 if tau == 0 else 2.5)
            c.set_stroke(opacity=1.0 if tau in (0.0, 1.0) else 0.55)
            curves.add(c)
        cl = VGroup(MathTex(r"T - t = 1", font_size=24, color=C.OPTION).next_to(ax.c2p(70, float(bs_call(70, K, r, sig, 1)[0])),
                                                                              UP, buff=0.15),
                    MathTex(r"\text{payoff}", font_size=24, color=C.OPTION).next_to(ax.c2p(130, 30), RIGHT, buff=0.1))
        nums = VGroup(
            MathTex(rf"S_0 = K = {S0:g},\;\; r = {r:g},\;\; \sigma = {sig:g},\;\; T = {T:g}", font_size=28),
            MathTex(r"\text{formula: }", num(price, 4), font_size=32),
            MathTex(r"\text{Monte Carlo, } 10^6 \text{ paths: }", num(mc, 4), r"\pm", num(se, 4), font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(DR, buff=0.6).shift(UP * 0.3)
        nums[1][1].set_color(C.OPTION)
        nums[2][1].set_color(C.OPTION)
        assert round(price, 4) == 10.4506 and abs(mc - price) < 2 * se

        with self.voiceover(
            "And we know how to solve equations like this one: Feynman–Kac. <bookmark mark='f'/> The option's value is "
            "the discounted average payoff, computed as if the stock grew at the risk-free rate r instead of mu. "
            "<bookmark mark='c'/> For a call, the average can be done in closed form: the famous Black–Scholes formula."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(fk), FadeIn(fkn), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(closed), FadeIn(dl))
        with self.voiceover(
            "Here's the value as a function of the stock price, <bookmark mark='a'/> a year before expiry, "
            "<bookmark mark='b'/> then closer and closer, <bookmark mark='p'/> until it becomes the hockey-stick payoff. "
            "<bookmark mark='n'/> With a stock at a hundred, a strike of a hundred, five percent interest and twenty "
            "percent volatility, the formula gives 10.4506. Averaging the payoff over a million simulated risk-neutral "
            "paths gives 10.4512, plus or minus 0.015."
        ) as vo:
            self.play(Create(ax), FadeIn(ticks), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(cl[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves[1:4]], lag_ratio=0.4), run_time=2)
            vo.wait_until("p")
            self.play(Create(curves[4]), FadeIn(cl[1]))
            vo.wait_until("n")
            self.play(FadeIn(nums[0]), FadeIn(nums[1]))
            self.play(FadeIn(nums[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replicate(self):
        d = load("hedge")
        S, t, V, P, D = d["path_S"], d["path_t"], d["path_V"], d["path_P"], d["path_D"]
        K = BS["K"]
        top = Axes(x_range=[0, 1, 0.25], y_range=[70, 130, 10], x_length=10.0, y_length=2.4, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_edge(UP, buff=0.9).shift(RIGHT * 0.5)
        bot = Axes(x_range=[0, 1, 0.25], y_range=[0, 25, 5], x_length=10.0, y_length=2.8, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).next_to(top, DOWN, buff=0.6)
        kline = DashedLine(top.c2p(0, K), top.c2p(1, K), color=GREY_C, stroke_width=1.5)
        kl = MathTex("K", font_size=26, color=GREY_B).next_to(top.c2p(1, K), RIGHT, buff=0.1)
        sl = MathTex(r"S_t", font_size=30, color=C.BROWNIAN).next_to(top, LEFT, buff=0.3)
        stock = polyline(top, t, S, color=C.BROWNIAN, stroke_width=3)
        opt = polyline(bot, t, V, color=C.OPTION, stroke_width=5).set_stroke(opacity=0.6)
        steps_x, steps_y = [t[0]], [P[0]]
        for k in range(1, len(t)):
            steps_x += [t[k]]
            steps_y += [P[k]]
        rep = polyline(bot, steps_x, steps_y, color=C.HEDGE, stroke_width=2.5)
        dots = VGroup(*[Dot(bot.c2p(tk, pk), radius=0.035, color=C.HEDGE) for tk, pk in zip(t, P)])
        leg = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.OPTION, stroke_width=5).set_stroke(opacity=0.6),
                   label(r"option value $V(t, S_t)$", font_size=24, color=C.OPTION)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=C.HEDGE, stroke_width=3),
                   label(r"cash $+$ $\Delta$ shares, rebalanced weekly", font_size=24, color=C.HEDGE)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(bot, DOWN, buff=0.2).align_to(bot, LEFT)
        mu_note = note(r"stock simulated with its real-world drift $\mu = 0.10$; \ the hedge never needs $\mu$")
        mu_note.to_corner(DR, buff=0.3)
        with self.voiceover(
            "The derivation is also a recipe. <bookmark mark='s'/> Here's a simulated stock over one year. "
            "<bookmark mark='v'/> Here's what the option is worth along the way. <bookmark mark='h'/> Now start with the "
            "option's price in cash, and each week, hold delta shares of the stock, financed from the cash. The portfolio "
            "tracks the option, week after week, and at expiry it lands within a dollar of the payoff, using nothing but "
            "the stock and a bank account."
        ) as vo:
            self.play(Create(top), FadeIn(sl), Create(kline), FadeIn(kl))
            vo.wait_until("s")
            self.play(Create(stock), run_time=1.5)
            vo.wait_until("v")
            self.play(Create(bot), Create(opt), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("h")
            self.play(Create(rep), LaggedStart(*[FadeIn(dt_) for dt_ in dots], lag_ratio=0.05), FadeIn(leg[1]),
                      FadeIn(mu_note), run_time=4)
        assert abs(P[-1] - max(S[-1] - K, 0)) < 1.0
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def errors(self):
        d = load("hedge")
        stds = d["stds"]
        price = float(d["price"][0])
        panels = VGroup()
        for n, sd in zip((4, 16, 64, 256), stds):
            ax = Axes(x_range=[-10, 10, 5], y_range=[0, 1.0, 0.5], x_length=3.0, y_length=2.6, tips=False,
                      axis_config={"stroke_color": GREY_B, "include_ticks": False})
            edges = np.linspace(-10, 10, 81)
            h = hist_shape(ax, edges, np.minimum(density(d[f"pnl{n}"], edges), 1.0), color=C.HEDGE, fill_opacity=0.5)
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.0), color=GREY_C, stroke_width=1.5)
            t = MathTex(rf"{n} \text{{ rebalances}}", font_size=28).next_to(ax, UP, buff=0.12)
            s = MathTex(rf"\text{{sd}} = {sd:.2f}", font_size=28, color=C.HEDGE).next_to(ax, DOWN, buff=0.15)
            ticks = VGroup(*[MathTex(f"{v}", font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.05) for v in (-10, 0, 10)])
            s.next_to(ticks, DOWN, buff=0.12)
            panels.add(VGroup(ax, h, zero, t, s, ticks))
        panels.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.3)
        title = label(rf"hedging error at expiry (the option sold for {price:.2f}), 5{{,}}000 simulated years each",
                      font_size=30).to_edge(UP, buff=0.5)
        rule = label(r"rebalance $4\times$ as often $\Rightarrow$ error halves: \ $\text{sd} \propto 1/\sqrt{n}$",
                     font_size=30, color=C.QV).to_edge(DOWN, buff=0.5)
        ratios = stds[:-1] / stds[1:]
        assert np.all(np.abs(ratios - 2) < 0.35)
        with self.voiceover(
            "How good is the hedge? <bookmark mark='a'/> Here's the leftover error after a year, across five thousand "
            "simulated years, rebalancing four times, <bookmark mark='b'/> sixteen, <bookmark mark='c'/> sixty-four, "
            "<bookmark mark='d'/> and two hundred fifty-six times. <bookmark mark='e'/> Each time you rebalance four times "
            "as often, the error halves, from 3.25 dollars down to 43 cents. In the continuous limit it vanishes: the "
            "option can be manufactured exactly, so its price is forced. And the leftover error on each step comes from how "
            "far delta W squared strays from delta t: the very fluctuation that dies away in the quadratic variation."
        ) as vo:
            self.play(FadeIn(title))
            for m, p in zip("abcd", panels):
                vo.wait_until(m)
                self.play(Create(p[0]), FadeIn(p[1], shift=UP * 0.2), FadeIn(p[2:]))
            vo.wait_until("e")
            self.play(FadeIn(rule))
        assert round(stds[0], 2) == 3.25 and round(stds[-1], 2) == 0.43
        self.wait(0.4)
        self.clear_scene()
