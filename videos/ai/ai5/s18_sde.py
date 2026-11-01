from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, DRIFT, MODEL, NOISE, PART, curve, load, normal_pdf

K = 1.3  # the letters' plane, drawn 1.3 times life size (as in the hook)


class SDE(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.order()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(16, r"Randomness with a push", r"How do you simulate a random path?", part=PART)
        with self.voiceover("Chapter sixteen. Stochastic differential equations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def anatomy(self):
        d = load("diffusion")
        paths, ts = np.asarray(d["ou_paths"]), np.asarray(d["ou_t"])
        theta, sigma = float(d["theta"]), float(d["sigma"])
        colors = {r"f(x)\,dt": DRIFT, r"g\,dW_t": NOISE}
        sde = cmath(r"dx", "=", r"f(x)\,dt", "+", r"g\,dW_t", colors=colors, font_size=50).to_edge(UP, buff=0.4)
        b1 = brace_note(term(sde, r"f(x)\,dt"), r"a push", color=DRIFT, font_size=26)
        b2 = brace_note(term(sde, r"g\,dW_t"), r"a random kick", color=NOISE, font_size=26)
        colors2 = {r"f(x_k)\,\Delta t": DRIFT, r"g\sqrt{\Delta t}\,\xi_k": NOISE}
        em = cmath(r"x_{k+1}", "=", r"x_k", "+", r"f(x_k)\,\Delta t", "+", r"g\sqrt{\Delta t}\,\xi_k", colors=colors2,
                   font_size=38)
        em_n = label(r"in small steps; \ $\xi_k$ a standard bell \ (Euler--Maruyama)", font_size=24, color=GREY_A)
        VGroup(em, em_n).arrange(DOWN, buff=0.15).next_to(sde, DOWN, buff=1.0)
        ax = Axes(x_range=[0, 4, 1], y_range=[-1.6, 3.0, 1], x_length=8.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.4, -1.6, 0])
        xl = label(r"time", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        lines = VGroup(*[VMobject(color=interpolate_color(ManimColor(DATA), ManimColor(C.BITS), k / 39), stroke_width=1.6,
                                  stroke_opacity=0.75).set_points_as_corners([ax.c2p(t, v) for t, v in zip(ts, p)])
                         for k, p in enumerate(paths)])
        tt = np.linspace(0, 4, 120)
        mean = 2.5 * np.exp(-theta * tt)
        sd = np.sqrt(sigma ** 2 / (2 * theta) * (1 - np.exp(-2 * theta * tt)))
        band = Polygon(*[ax.c2p(t, m + 2 * s) for t, m, s in zip(tt, mean, sd)],
                       *[ax.c2p(t, m - 2 * s) for t, m, s in zip(tt[::-1], mean[::-1], sd[::-1])],
                       stroke_width=0, fill_color=DRIFT, fill_opacity=0.15)
        mline = curve(ax, tt, mean, color=DRIFT, stroke_width=4)
        s_inf = sigma / math.sqrt(2 * theta)
        ys = np.linspace(-1.6, 1.6, 100)
        x_end = ax.c2p(4, 0)[0]
        side = VMobject(color=MODEL, stroke_width=3).set_points_smoothly(
            [np.array([x_end + 1.1 * normal_pdf(y, 0, s_inf), ax.c2p(0, y)[1], 0]) for y in ys])
        ou = cmath(r"f(x) = -\theta x", font_size=36, color=DRIFT)
        ou_n = label(r"a spring pulling toward $0$, plus noise \\ (Ornstein--Uhlenbeck, 1930)", font_size=24, color=GREY_A)
        VGroup(ou, ou_n).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, 1.0, 0])
        settle = label(rf"settles to a bell: \ width $\sigma / \sqrt{{2\theta}} = {s_inf:.2f}$", font_size=24,
                       color=MODEL).next_to(ou_n, DOWN, buff=0.3).align_to(ou_n, LEFT)
        # dt and dW, pictured: one tiny step is a push along f, then a random kick
        p0 = np.array([-1.2, -0.2, 0])
        p1 = p0 + np.array([1.3, 0.35, 0])
        p2 = p1 + np.array([0.35, -0.55, 0])
        step_pic = VGroup(Dot(p0, radius=0.07, color=WHITE),
                          Arrow(p0, p1, buff=0.05, color=DRIFT, stroke_width=4, max_tip_length_to_length_ratio=0.2),
                          Arrow(p1, p2, buff=0.05, color=NOISE, stroke_width=4, max_tip_length_to_length_ratio=0.3),
                          Dot(p2, radius=0.07, color=WHITE))
        step_pic.add(label(r"push: \ $f(x)\,dt$", font_size=22, color=DRIFT).next_to(step_pic[1], UP, buff=0.08),
                     label(r"kick: \ $g\,dW_t$", font_size=22, color=NOISE).next_to(step_pic[2], RIGHT, buff=0.1))
        dd = gloss(r"$dt$, \ $dW_t$", r"$dt$: \ a tiny tick of time; \ $dW_t$: \ the tiny random kick\\ that "
                   r"Brownian motion makes in that tick", picture=step_pic, width=4.8, color=NOISE)
        dd.scale(1.25).to_edge(DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "Brownian motion is pure jiggle. Add a push, and you have a stochastic differential equation. At each "
            "instant, the change in x is a push, f of x times dt, where dt is a tiny tick of time, "
            "<bookmark mark='a'/> plus a random kick: g times dW, the tiny piece of Brownian motion in that tick. "
            "<bookmark mark='b'/> To simulate one, take small steps: push, then "
            "kick, with a kick the size of the square root of the step."
        ) as vo:
            self.play(Write(sde), FadeIn(dd))
            self.play(FadeIn(b1))
            vo.wait_until("a")
            self.play(FadeIn(b2))
            vo.wait_until("b")
            self.play(Write(em), FadeIn(em_n))
        with self.voiceover(
            "The simplest interesting one is a spring pulling back toward zero, plus noise. Forty particles start at "
            "2.5. <bookmark mark='a'/> The push pulls them home, the noise keeps them stirred, <bookmark mark='b'/> "
            "and they settle into a bell around zero, its width set by the balance between the two. Leonard Ornstein "
            "and George Uhlenbeck described it in 1930, and it is the forward process of diffusion models."
        ) as vo:
            # Clear the Euler supplement before the OU caption occupies the same row.
            # Preserve the original one-second transition and keep the top SDE held.
            self.play(Succession(
                AnimationGroup(FadeOut(em), FadeOut(em_n), FadeOut(dd)),
                AnimationGroup(Create(ax), FadeIn(xl), FadeIn(ou), FadeIn(ou_n)),
                run_time=1.0,
            ))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.02), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(band), Create(mline))
            vo.wait_until("b")
            self.play(Create(side), FadeIn(settle))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        d = load("em")
        hs, st, wk = np.asarray(d["hs"]), np.asarray(d["strong"]), np.asarray(d["weak"])
        ss, ws = float(d["strong_slope"]), float(d["weak_slope"])
        mu, sig, M = float(d["mu"]), float(d["sigma"]), int(d["M"])
        ex = np.asarray(d["exact_path"])
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 12, 4], x_length=5.6, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.4, 0.2, 0])
        te = np.linspace(0, 1, len(ex))
        exc = curve(ax, te, np.minimum(ex, 12), color=WHITE, stroke_width=3)
        cols = {4: C.SURPRISE, 16: C.BITS, 256: C.INTERVAL}
        ems = VGroup()
        for n in [int(v) for v in d["n_show"]]:
            p = np.asarray(d[f"em{n}"])
            ems.add(curve(ax, np.linspace(0, 1, n + 1), np.minimum(p, 12), color=cols[n], stroke_width=2.5))
        lg = VGroup(label(r"exact, \ from the same noise", font_size=20, color=WHITE),
                    *[label(rf"Euler--Maruyama, \ ${n}$ steps", font_size=20, color=cols[n]) for n in cols])
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        f = cmath(r"dX", "=", rf"{mu:g}\,X\,dt", "+", (r"X\,dW" if sig == 1 else rf"{sig:g}\,X\,dW"), font_size=34).next_to(lg, UP, buff=0.15).align_to(ax, LEFT)
        bx = CornerAxes(x_range=[-3, 0, 1], y_range=[-2, 1, 1], x_length=5.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.6, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(bx.c2p(v, -2), DOWN, buff=0.08)
                      for t, v in (("10^{-3}", -3), ("10^{-2}", -2), ("0.1", -1), ("1", 0))])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(bx.c2p(-3, v), LEFT, buff=0.08)
                      for t, v in (("0.01", -2), ("0.1", -1), ("1", 0), ("10", 1))])
        xl = label(r"step $h$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        lh = np.log10(hs)
        sc = VGroup(curve(bx, lh, np.log10(st), color=C.BITS, stroke_width=3),
                    *[Dot(bx.c2p(a, math.log10(b)), radius=0.05, color=C.BITS) for a, b in zip(lh, st)])
        wc = VGroup(curve(bx, lh, np.log10(np.maximum(wk, 1e-2)), color=C.INTERVAL, stroke_width=3),
                    *[Dot(bx.c2p(a, math.log10(max(b, 1e-2))), radius=0.05, color=C.INTERVAL) for a, b in zip(lh, wk)])
        sl = label(rf"strong error $\mathbb{{E}}|X_h - X|$: \ slope ${ss:.2f}$", font_size=20, color=C.BITS)
        wl = label(rf"weak error $|\mathbb{{E}}[X_h - X]|$: \ slope ${ws:.2f}$", font_size=20, color=C.INTERVAL)
        VGroup(sl, wl).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bx, UP, buff=0.1).align_to(bx, LEFT)
        tag = note(rf"${M:,}$ paths; \ geometric Brownian motion, \ whose exact solution is known".replace(",", "{,}"))
        tag.to_edge(DOWN, buff=0.25)
        cite_ = cite(r"G.~Maruyama (1955)", corner=DL).shift(UP * 0.35)
        half = abs(ss - 0.5) < 0.15
        one = abs(ws - 1.0) < 0.2
        v = (f"The path-by-path error shrinks like the square root of the step, slope {ss:.2f}: halve the step, and "
             f"the error falls by only {100 * (1 - 2 ** -ss):.0f} percent. The error in the average shrinks like the step itself, slope {ws:.2f}."
             if half and one else
             f"The path-by-path error falls with slope {ss:.2f}, the error in the average with slope {ws:.2f}.")
        with self.voiceover(
            "How good is that simple scheme? Test it where the exact answer is known: a quantity that grows by a "
            "random percentage each instant, geometric Brownian motion, the model of a stock price. "
            "<bookmark mark='a'/> With the same random kicks, coarse steps wander off the exact path, and fine steps "
            f"follow it. <bookmark mark='b'/> Over {M:,} paths: {v} <bookmark mark='c'/> Gisiro Maruyama proved "
            "the scheme converges in 1955. Diffusion models' samplers are, at heart, this scheme run backwards, and "
            "part twenty-one spends chapters on doing better with fewer steps."
        ) as vo:
            self.play(FadeIn(f), Create(ax), FadeIn(lg), Create(exc), Create(bx), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in ems], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tag))
            self.play(Create(sc), FadeIn(sl))
            self.play(Create(wc), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
