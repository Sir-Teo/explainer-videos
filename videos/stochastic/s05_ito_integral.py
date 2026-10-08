from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import boxed, hero, label, load, mtex, note, num, part_card, path_curve, polyline, tw_axes

N_STEP = 16


class ItoIntegral(VoiceoverScene):
    def construct(self):
        self.card()
        self.noise()
        self.integral_form()
        self.gamble()
        self.definition()

    def card(self):
        c = part_card(2, r"The It\^o integral", r"integrating against noise")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def noise(self):
        ode = MathTex(r"\frac{dX}{dt}", r"=", r"\mu(X)", font_size=44)
        ode[2].set_color(C.DRIFT)
        sde = MathTex(r"\frac{dX}{dt}", r"=", r"\mu(X)", r"+", r"\sigma(X)", r"\cdot", r"\text{noise}(t)", font_size=44)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        sde[6].set_color(C.BROWNIAN)
        ode.to_edge(UP, buff=0.5)
        sde.to_edge(UP, buff=0.5)
        q = MathTex(r"\text{noise}(t)", r"=", r"\frac{dW}{dt}", r"\;?", font_size=40).next_to(sde, DOWN, buff=0.35)
        q[0].set_color(C.BROWNIAN)
        q[2].set_color(C.BROWNIAN)

        ax = Axes(x_range=[0, 1, 0.25], y_range=[-260, 260, 100], x_length=11, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(DOWN * 1.5)
        yl = MathTex(r"\Delta W / \Delta t", font_size=30, color=C.BROWNIAN).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        ticks = VGroup(*[MathTex(f"{v}", font_size=22).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (-200, 0, 200)])

        def slopes(n):
            w = hero(n)
            s = np.diff(w) * n
            ts = np.linspace(0, 1, n + 1)
            xs = np.repeat(ts, 2)[1:-1]
            ys = np.repeat(s, 2)
            return polyline(ax, xs, np.clip(ys, -260, 260), color=C.BROWNIAN, stroke_width=1.5 if n > 256 else 2)

        cur = slopes(64)
        nl = MathTex(r"\Delta t = 1/64", font_size=32).next_to(ax, UP, buff=0.1).to_edge(RIGHT, buff=0.8)
        with self.voiceover(
            "Most of science is written in differential equations: <bookmark mark='o'/> the rate of change of X is some "
            "function of X. <bookmark mark='s'/> To add randomness, it's natural to write: rate of change equals a drift, "
            "plus some amplitude times noise. <bookmark mark='q'/> But what is the noise? It would have to be the "
            "derivative of Brownian motion, and we just saw that doesn't exist."
        ) as vo:
            vo.wait_until("o")
            self.play(Write(ode))
            vo.wait_until("s")
            self.play(TransformMatchingTex(ode, sde))
            vo.wait_until("q")
            self.play(Write(q))
        with self.voiceover(
            "Here's what happens if you try anyway: the slopes of our path over steps of one sixty-fourth, "
            "<bookmark mark='a'/> one two-fifty-sixth, <bookmark mark='b'/> and one four-thousandth. The finer you look, "
            "the bigger the spikes. There's no function there to converge to."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(ticks), Create(cur), FadeIn(nl))
            vo.wait_until("a")
            self.play(Transform(cur, slopes(256)), Transform(nl, MathTex(r"\Delta t = 1/256", font_size=32).move_to(nl)))
            vo.wait_until("b")
            self.play(Transform(cur, slopes(4096)), Transform(nl, MathTex(r"\Delta t = 1/4096", font_size=32).move_to(nl)))
        self.play(FadeOut(VGroup(ax, yl, ticks, cur, nl, q)))
        self.sde = sde

    # ------------------------------------------------------------------
    def integral_form(self):
        integ = MathTex(r"X_t", r"=", r"X_0", r"+", r"\int_0^t \mu(X_s)\,ds", r"+", r"\int_0^t \sigma(X_s)\,dW_s",
                        font_size=46)
        integ[4].set_color(C.DRIFT)
        integ[6].set_color(C.BROWNIAN)
        integ.move_to(UP * 0.6)
        b1 = Brace(integ[4], DOWN, color=C.DRIFT)
        b1l = label(r"ordinary integral", font_size=28, color=C.DRIFT).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(integ[6], DOWN, color=C.BROWNIAN)
        b2l = label(r"new: integrating against $W$", font_size=28, color=C.BROWNIAN).next_to(b2, DOWN, buff=0.1)
        lang = note(r"Langevin (1908) wrote the first such equation, for a Brownian particle's velocity").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The way out is to never differentiate. Integrate both sides instead. <bookmark mark='i'/> X at time t is its "
            "starting value, <bookmark mark='d'/> plus the integral of the drift, which is an ordinary integral, "
            "<bookmark mark='n'/> plus the integral of sigma d W. That last one is new. To make sense of noisy "
            "differential equations, we first have to define what it means to integrate against a Brownian path."
        ) as vo:
            vo.wait_until("i")
            self.play(ReplacementTransform(self.sde, integ), FadeIn(lang))
            vo.wait_until("d")
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("n")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gamble(self):
        n = N_STEP
        w = hero(n)
        ts = np.linspace(0, 1, n + 1)
        H = w[:-1]
        G = np.concatenate([[0], np.cumsum(H * np.diff(w))])
        X0, XL = -5.2, 11.0
        top = Axes(x_range=[0, 1, 0.25], y_range=[-1.0, 1.6, 0.5], x_length=XL, y_length=2.0, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False})
        mid = Axes(x_range=[0, 1, 0.25], y_range=[-1.0, 1.6, 0.5], x_length=XL, y_length=1.5, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False})
        bot = Axes(x_range=[0, 1, 0.25], y_range=[-0.4, 0.6, 0.2], x_length=XL, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False})
        panels = VGroup(top, mid, bot).arrange(DOWN, buff=0.55).move_to([X0 + XL / 2 + 0.6, -0.25, 0])
        for a in panels:
            a.x_axis.move_to(a.c2p(0.5, 0))
        names = VGroup(
            VGroup(MathTex(r"W_t", font_size=34, color=C.BROWNIAN), label(r"price", font_size=24, color=GREY_B)),
            VGroup(MathTex(r"H_t", font_size=34, color=C.STAKE), label(r"stake", font_size=24, color=GREY_B)),
            VGroup(MathTex(r"G_t", font_size=34, color=C.GAINS), label(r"winnings", font_size=24, color=GREY_B)),
        )
        for nm, a in zip(names, panels):
            nm.arrange(DOWN, buff=0.08).next_to(a, LEFT, buff=0.3)
        stake_bars = VGroup(*[Rectangle(width=XL / n * 0.9, height=max(abs(H[i]) * mid.y_length / 2.6, 0.005),
                                        stroke_width=0, fill_color=C.STAKE, fill_opacity=0.7)
                              .move_to(mid.c2p(ts[i] + 0.5 / n, 0), aligned_edge=DOWN if H[i] >= 0 else UP)
                              for i in range(n)])
        rule = MathTex(r"\text{gain on step } i", r"=", r"H_{t_i}", r"\cdot", r"\big(W_{t_{i+1}} - W_{t_i}\big)", font_size=36)
        rule[2].set_color(C.STAKE)
        rule[4].set_color(C.BROWNIAN)
        rule.to_edge(UP, buff=0.3)
        strat = label(r"strategy: hold $H = W$ shares (more when the price is high)", font_size=26, color=C.STAKE)
        strat.next_to(rule, DOWN, buff=0.15)

        with self.voiceover(
            "The cleanest way to think about it is gambling. <bookmark mark='w'/> Let W be the price of a stock, or your "
            "running score in a fair game. <bookmark mark='h'/> Let H be how many shares you hold: your stake. "
            "<bookmark mark='g'/> Over one short step, your gain is your stake times the change in the price, and your "
            "winnings, G, are the sum of all those gains."
        ) as vo:
            self.play(*[Create(a) for a in panels])
            vo.wait_until("w")
            self.play(FadeIn(names[0]))
            vo.wait_until("h")
            self.play(FadeIn(names[1]))
            vo.wait_until("g")
            self.play(FadeIn(names[2]), Write(rule))

        # The curtain: the future is hidden until each step happens
        top_rect = Rectangle(width=XL, height=2.0).move_to(top)
        curtain = Rectangle(width=XL + 0.1, height=panels.height + 0.3, stroke_width=0, fill_color=BACKGROUND,
                            fill_opacity=0.88)
        curtain.move_to(top_rect.get_left() + RIGHT * (XL / 2 + 0.05), aligned_edge=LEFT)
        curtain.align_to(panels, UP).shift(UP * 0.15)
        future = label(r"the future", font_size=26, color=GREY_B)
        future.add_updater(lambda m: m.move_to(curtain.get_center() + UP * 0.0).set_x(curtain.get_left()[0] + 1.2))
        now = always_redraw(lambda: DashedLine(curtain.get_corner(UL), curtain.get_corner(DL), color=WHITE, stroke_width=2))
        price_parts = VGroup(*[Line(top.c2p(ts[i], w[i]), top.c2p(ts[i + 1], w[i + 1]), color=C.BROWNIAN, stroke_width=3)
                               for i in range(n)])
        gain_parts = VGroup(*[Line(bot.c2p(ts[i], G[i]), bot.c2p(ts[i + 1], G[i + 1]), color=C.GAINS, stroke_width=3)
                              for i in range(n)])
        gdot = Dot(bot.c2p(0, 0), radius=0.06, color=C.GAINS)
        with self.voiceover(
            "Here's a strategy: hold as many shares as the current price. <bookmark mark='p'/> Watch it play out. At the "
            "start of each step, you choose your stake, looking only at the past. Then the curtain lifts, the price "
            "moves, and the gain, stake times move, goes into your winnings."
        ) as vo:
            self.play(FadeIn(strat))
            self.add(curtain, now, future)
            vo.wait_until("p")
            per = max(0.45, (vo.remaining() - 0.5) / n)
            for i in range(n):
                self.play(FadeIn(stake_bars[i], shift=UP * 0.1), run_time=per * 0.4)
                self.play(curtain.animate.shift(RIGHT * XL / n), Create(price_parts[i]), Create(gain_parts[i]),
                          gdot.animate.move_to(bot.c2p(ts[i + 1], G[i + 1])), run_time=per * 0.6)
            future.clear_updaters()
        self.remove(curtain, now, future)
        adapted = label(r"the stake at $t_i$ may depend only on what happened up to $t_i$: \ \emph{no peeking}",
                        font_size=28, color=C.QV).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Notice the one rule we followed. <bookmark mark='r'/> Each stake was set before the price moved: you could see "
            "the past, but the future was behind a curtain. A strategy that never peeks is called adapted, or "
            "non-anticipating, and it's the only kind of integrand we allow. It's also the only kind a real gambler, or a "
            "real investor, can use."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(adapted, shift=UP * 0.2))
        self.wait(0.3)
        self.gam = VGroup(panels, names, price_parts, stake_bars, gain_parts, gdot)
        self.top, self.mid, self.bot = top, mid, bot
        self.play(FadeOut(VGroup(rule, strat, adapted)))

    # ------------------------------------------------------------------
    def definition(self):
        defn = MathTex(r"\int_0^T H_t\,dW_t", r"=", r"\lim_{n\to\infty}", r"\sum_{i=0}^{n-1}", r"H_{t_i}",
                       r"\big(W_{t_{i+1}} - W_{t_i}\big)", font_size=42)
        defn[0].set_color(C.GAINS)
        defn[4].set_color(C.STAKE)
        defn[5].set_color(C.BROWNIAN)
        db = boxed(defn, color=C.GAINS, buff=0.2).to_edge(UP, buff=0.25)
        left = Brace(defn[4], DOWN, buff=0.08, color=C.LEFT_PT)
        left_l = label(r"left endpoint", font_size=24, color=C.LEFT_PT).next_to(left, DOWN, buff=0.05)
        top, mid, bot = self.top, self.mid, self.bot
        price_parts, stake_bars, gain_parts, gdot = self.gam[2], self.gam[3], self.gam[4], self.gam[5]
        h = load("hero")
        lefts = dict(zip(h["n"].tolist(), h["left"].tolist()))

        def curves(n):
            w = hero(n)
            ts = np.linspace(0, 1, n + 1)
            G = np.concatenate([[0], np.cumsum(w[:-1] * np.diff(w))])
            xs = np.repeat(ts, 2)[1:-1]
            stake = polyline(mid, xs, np.repeat(w[:-1], 2), color=C.STAKE, stroke_width=2)
            price = path_curve(top, w, stroke_width=2.4)
            gains = path_curve(bot, G, color=C.GAINS, stroke_width=2.6)
            return VGroup(price, stake, gains), G[-1]

        end_val = DecimalNumber(lefts[16], num_decimal_places=4, font_size=32, color=C.GAINS)
        end_lab = VGroup(MathTex(r"G_1 =", font_size=32, color=C.GAINS), end_val).arrange(RIGHT, buff=0.12)

        self.play(self.gam.animate.scale(0.86).shift(DOWN * 0.5))
        end_lab.next_to(bot, UP, buff=0.04).align_to(bot, RIGHT)
        with self.voiceover(
            "The Itô integral is what these winnings converge to as the steps shrink: <bookmark mark='d'/> the limit of "
            "the sum of H at the left end of each step, <bookmark mark='l'/> decided before the move, times the change in "
            "W across the step."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(defn), Create(db[0]))
            vo.wait_until("l")
            self.play(GrowFromCenter(left), FadeIn(left_l))
        g16, _ = curves(16)
        self.play(FadeIn(end_lab),
                  ReplacementTransform(VGroup(price_parts, stake_bars, gain_parts), g16), FadeOut(gdot))
        cur = g16
        with self.voiceover(
            "Despite the path's infinite length, these sums do converge, because the random gains and losses cancel "
            "each other in a controlled way; we'll see exactly how in a moment. <bookmark mark='a'/> Here's the same "
            "strategy with sixty-four steps, <bookmark mark='b'/> two hundred and fifty-six, <bookmark mark='c'/> four "
            "thousand. <bookmark mark='e'/> The winnings settle onto one curve, and at time one they settle onto a number "
            "we've seen before: 0.2847, the answer with the missing half."
        ) as vo:
            for mk, n in zip("abc", (64, 256, 4096)):
                vo.wait_until(mk)
                g, _ = curves(n)
                self.play(Transform(cur, g), end_val.animate.set_value(lefts[n]), run_time=1.2)
            vo.wait_until("e")
            end_val.num_decimal_places = 4
            self.play(end_val.animate.set_value(lefts[4194304]))
            self.play(Indicate(end_lab, color=C.GAINS))
        self.wait(0.5)
        self.clear_scene()
