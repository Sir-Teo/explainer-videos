from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, DRIFT, MODEL, NOISE, SCORE, curve, follow, hist_shape, load, normal_pdf, ramp, swarm

K = 1.3  # the letters' plane, drawn 1.3 times life size (as in the hook)


class SDE(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.fokker_planck()
        self.reverse()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Randomness with a push", r"What happens to a whole cloud of random paths?", part=4,
                            lit=(2015,))
        with self.voiceover("Chapter nine. Stochastic differential equations."):
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
        ou_n = label(r"a spring pulling toward $0$, plus noise \\ (Ornstein--Uhlenbeck)", font_size=24, color=GREY_A)
        VGroup(ou, ou_n).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, 1.0, 0])
        settle = label(rf"settles to a bell: \ width $\sigma / \sqrt{{2\theta}} = {s_inf:.2f}$", font_size=24,
                       color=MODEL).next_to(ou_n, DOWN, buff=0.3).align_to(ou_n, LEFT)
        with self.voiceover(
            "Brownian motion is pure jiggle. Add a push, and you have a stochastic differential equation. At each "
            "instant, the change in x is a push, f of x times dt, <bookmark mark='a'/> plus a random kick: g times a "
            "small piece of Brownian motion. <bookmark mark='b'/> To simulate one, take small steps: push, then "
            "kick, with a kick the size of the square root of the step."
        ) as vo:
            self.play(Write(sde))
            self.play(FadeIn(b1))
            vo.wait_until("a")
            self.play(FadeIn(b2))
            vo.wait_until("b")
            self.play(Write(em), FadeIn(em_n))
        with self.voiceover(
            "The simplest interesting one is a spring pulling back toward zero, plus noise. Forty particles start at "
            "2.5. <bookmark mark='a'/> The push pulls them home, the noise keeps them stirred, <bookmark mark='b'/> "
            "and they settle into a bell around zero, its width set by the balance between the two. It's called the "
            "Ornstein–Uhlenbeck process, and it's the one diffusion models use."
        ) as vo:
            self.play(FadeOut(em), FadeOut(em_n), Create(ax), FadeIn(xl), FadeIn(ou), FadeIn(ou_n))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.02), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(band), Create(mline))
            vo.wait_until("b")
            self.play(Create(side), FadeIn(settle))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fokker_planck(self):
        d = load("diffusion")
        xs, fp, hist = np.asarray(d["xs"]), np.asarray(d["fp"]), np.asarray(d["fp_hist"])
        fp_ts = [float(t) for t in d["fp_ts"]]
        assert max(d["fp_err"]) < 0.01 and max(d["hist_err"]) < 0.08
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.6, 0.2], x_length=10.0, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -1.2, 0])
        edges = np.linspace(-4, 4, 81)
        hs = [hist_shape(ax, edges, np.minimum(h, 0.6), color=DATA, opacity=0.4, stroke_width=0) for h in hist]
        cs = [curve(ax, xs, np.minimum(p, 0.6), color=MODEL, stroke_width=4) for p in fp]
        tv = DecimalNumber(0, num_decimal_places=2, font_size=36, color=C.BITS)
        tl = VGroup(MathTex(r"t =", font_size=36), tv).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.5).shift(DOWN * 1.6)
        colors = {r"p": MODEL, r"f": DRIFT, r"g^2": NOISE}
        fpe = cmath(r"\frac{\partial p}{\partial t}", "=", r"-\frac{\partial}{\partial x}\big(", r"f", r"\,", r"p",
                    r"\big)", "+", r"\tfrac12", r"g^2", r"\frac{\partial^2 p}{\partial x^2}", colors=colors, font_size=42)
        fpe.to_edge(UP, buff=0.45)
        fpn = label(r"the Fokker--Planck equation: \ the density's own law, \ no randomness left", font_size=26,
                    color=GREY_A).next_to(fpe, DOWN, buff=0.25)
        legend = VGroup(label(r"$20{,}000$ random particles", font_size=24, color=DATA),
                        label(r"the equation's solution", font_size=24, color=MODEL))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.5).shift(DOWN * 1.6)
        end = label(r"all that's left: \ a standard bell", font_size=28, color=WHITE).next_to(ax, DOWN, buff=0.3)
        with self.voiceover(
            "And again, follow the density instead of the particles. <bookmark mark='a'/> Start with data that has "
            "two peaks, and let every point drift toward zero and jiggle, the way the Ornstein–Uhlenbeck process "
            "says. <bookmark mark='b'/> Twenty thousand random particles, and the solution of one deterministic "
            "equation, the Fokker–Planck equation, move together. <bookmark mark='c'/> Wait long enough, and every "
            "trace of the data is gone: what's left is a plain standard bell. That's exactly what a diffusion model "
            "does to its training images."
        ) as vo:
            self.play(Write(fpe), FadeIn(fpn))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(hs[0]), Create(cs[0]), FadeIn(tl), FadeIn(legend))
            vo.wait_until("b")
            h, c = hs[0], cs[0]
            for k in range(1, len(fp_ts) - 1):
                self.play(Transform(h, hs[k]), Transform(c, cs[k]), ChangeDecimalToValue(tv, fp_ts[k]), run_time=1.6)
            vo.wait_until("c")
            self.play(Transform(h, hs[-1]), Transform(c, cs[-1]), ChangeDecimalToValue(tv, fp_ts[-1]), run_time=2.0)
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reverse(self):
        d = load("diffusion")
        xs, dens, scores, alphas = (np.asarray(d[k]) for k in ("xs", "dens", "scores", "alphas"))
        colors = {r"f(x)": DRIFT, r"\nabla \log p_t(x)": SCORE, r"g\,d\bar W_t": NOISE, r"g^2": NOISE}
        rev = cmath(r"dx", "=", r"\big[", r"f(x)", "-", r"g^2", r"\nabla \log p_t(x)", r"\big]\,dt", "+",
                    r"g\,d\bar W_t", colors=colors, font_size=44).to_edge(UP, buff=0.4)
        rn = label(r"time running backwards \ (Anderson, 1982)", font_size=24, color=GREY_A).next_to(rev, DOWN, buff=0.85)
        sb = brace_note(term(rev, r"\nabla \log p_t(x)"), r"the score", color=SCORE, font_size=28)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.6, 0.2], x_length=10.0, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -1.0, 0])
        k = 2  # alpha = 0.5: halfway to noise
        assert abs(alphas[k] - 0.5) < 1e-9
        dc = curve(ax, xs, dens[k], color=DATA, stroke_width=4)
        arrows = VGroup()
        for x in np.linspace(-3.6, 3.6, 25):
            s = float(np.interp(x, xs, scores[k]))
            L = 0.55 * math.tanh(s / 2.5)
            base = ax.c2p(x, 0) + DOWN * 0.45
            if abs(L) > 0.04:
                arrows.add(Arrow(base, base + RIGHT * L, buff=0, color=SCORE, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.4))
        al = label(r"the score points uphill: \ toward where data is likelier", font_size=26, color=SCORE)
        al.next_to(ax, DOWN, buff=0.6)
        with self.voiceover(
            "Can the film run backwards, from the bell back to the data? In 1982, Brian Anderson showed that "
            "reversed in time, it's another stochastic differential equation, with one extra term: "
            "<bookmark mark='a'/> the score, the slope of the log of the density at that moment. "
            "<bookmark mark='b'/> The score points uphill, toward where the data is more likely."
        ) as vo:
            self.play(Write(rev), FadeIn(rn))
            vo.wait_until("a")
            self.play(FadeIn(sb))
            vo.wait_until("b")
            self.play(Create(ax), Create(dc))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.04), FadeIn(al), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()
        # the letters again: the score field in the plane, and the reverse flow
        s = load("shape")
        G = np.asarray(s["grid"])
        F = np.asarray(s["field0.5"])
        bwd = np.asarray(s["bwd"])
        field = VGroup()
        mag = np.linalg.norm(F, axis=1) + 1e-9
        ref = np.percentile(mag, 90)
        for p, v, m in zip(G * K, F, mag):
            L = 0.42 * min(1.0, m / ref)
            field.add(Arrow([p[0], p[1], 0], [p[0] + L * v[0] / m, p[1] + L * v[1] / m, 0], buff=0, color=SCORE,
                            stroke_width=2.5, max_tip_length_to_length_ratio=0.35, stroke_opacity=0.7))
        cols = ramp(bwd[-1][:, 0] + 0.35 * bwd[-1][:, 1], DATA, C.BITS)
        dots = swarm(bwd[0] * K, cols)
        t = ValueTracker(0.0)
        cap = label(r"the score of the noised letters, \ halfway to noise", font_size=26, color=SCORE).to_edge(DOWN, buff=0.3)
        nxt = label(r"Part 14: \ a network learns the score from millions of images", font_size=28, color=C.BITS)
        nxt.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Know the score at every noise level, and you can turn noise into data. <bookmark mark='a'/> It's the "
            "field of arrows from the start of this part. <bookmark mark='b'/> There, it was computed exactly from "
            "the letters. A diffusion model learns it from millions of images, with a network, and that's part "
            "fourteen."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.004), FadeIn(cap), run_time=1.5)
            self.play(FadeIn(dots))
            dots.add_updater(follow(dots, bwd, t, scale=K))
            vo.wait_until("b")
            self.play(t.animate.set_value(len(bwd) - 1), field.animate.set_opacity(0.15), FadeOut(cap), FadeIn(nxt),
                      run_time=5.0, rate_func=lambda a: 1 - (1 - a) ** 2.2)
            dots.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
