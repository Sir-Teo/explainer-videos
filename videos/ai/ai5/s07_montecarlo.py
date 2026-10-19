from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, curve, load, normal_pdf

TAIL = C.SURPRISE


class MonteCarlo(VoiceoverScene):
    def construct(self):
        self.card()
        self.darts()
        self.rate()
        self.rare()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Answers from random samples", r"Can dice compute $\pi$?", part=5)
        with self.voiceover("Chapter six. Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def darts(self):
        d = load("montecarlo")
        pts, inside, est = np.asarray(d["pts"]), np.asarray(d["inside"], bool), np.asarray(d["est"])
        N = int(d["N"])
        c, R = np.array([-3.7, -0.3, 0]), 2.5
        sq = Square(2 * R, color=GREY_B, stroke_width=2).move_to(c)
        circ = Circle(radius=R, color=DATA, stroke_width=3).move_to(c)
        dots = VGroup(*[Dot(c + R * np.array([p[0], p[1], 0]), radius=0.03, color=DATA if i else GREY_C)
                        for p, i in zip(pts, inside)])
        ax = Axes(x_range=[0, math.log10(N), 1], y_range=[2.6, 3.7, 0.5], x_length=5.4, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.4, 0.0, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 2.6), DOWN, buff=0.12)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        xn = label(r"darts thrown", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        pi_l = DashedLine(ax.c2p(0, math.pi), ax.c2p(math.log10(N), math.pi), color=WHITE, stroke_width=2)
        pi_t = MathTex(r"\pi", font_size=34).next_to(pi_l, RIGHT, buff=0.1)
        ns = np.unique(np.round(np.logspace(0, math.log10(N), 300)).astype(int))
        band_hi = [ax.c2p(math.log10(n), min(math.pi + 1.64 / math.sqrt(n), 3.7)) for n in ns]
        band_lo = [ax.c2p(math.log10(n), max(math.pi - 1.64 / math.sqrt(n), 2.6)) for n in ns]
        band = Polygon(*band_hi, *band_lo[::-1], stroke_width=0, fill_color=DATA, fill_opacity=0.14)
        t = ValueTracker(1)

        def path():
            n = max(int(t.get_value()), 2)
            m = ns[ns <= n]
            return VMobject(color=C.BITS, stroke_width=3).set_points_as_corners(
                [ax.c2p(math.log10(k), float(np.clip(est[k - 1], 2.6, 3.7))) for k in m] or [ax.c2p(0, 3)])

        trace = always_redraw(path)
        ev = DecimalNumber(4.0, num_decimal_places=3, font_size=40, color=C.BITS)
        ev.add_updater(lambda m: m.set_value(est[max(int(t.get_value()), 1) - 1]))
        colors = {r"\pi": DATA}
        f = cmath(r"4 \times \frac{\text{inside}}{\text{all}}", r"\approx", r"\pi", colors=colors, font_size=40)
        VGroup(f, ev).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        why = label(r"the circle's share of the square: \ $\pi / 4$", font_size=26, color=GREY_A).next_to(sq, DOWN, buff=0.2)
        shown = len(dots)
        with self.voiceover(
            "Here's a strange way to compute pi. Throw darts at a square, completely at random. "
            "<bookmark mark='a'/> The share that lands inside the circle is the circle's share of the square's area: "
            "pi over four. So four times the fraction inside estimates pi. <bookmark mark='b'/> Watch the estimate "
            "as the darts pile up. It lurches around, then homes in."
        ) as vo:
            self.play(Create(sq), Create(circ))
            self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in dots[:24]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(why), Write(f))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(xn), Create(pi_l), FadeIn(pi_t), FadeIn(ev))
            self.add(trace)
            self.play(t.animate.set_value(24), run_time=1.0, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in dots[24:shown]], lag_ratio=0.002),
                      t.animate.set_value(N), run_time=6.0, rate_func=linear)
        with self.voiceover(
            rf"After four thousand darts: {est[-1]:.3f}. <bookmark mark='a'/> The shaded band is how far off a run "
            "like this typically is, and it narrows like one over the square root of the number of darts."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(band))
        trace.clear_updaters()
        ev.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        d = load("montecarlo")
        Ns, rms, slope = np.asarray(d["Ns"], float), np.asarray(d["rms"]), float(d["slope"])
        ax = Axes(x_range=[1, 5, 1], y_range=[-3, 0, 1], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=24, color=GREY_B).next_to(ax.c2p(v, -3), DOWN, buff=0.12)
                      for v in range(1, 6)])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=24, color=GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.12)
                      for v in range(-3, 1)])
        xn = label(r"darts", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        x10 = VGroup(*[label(r"$\times 10$", font_size=18, color=GREY_C).move_to([ax.c2p(v + 0.5, -3)[0], xl[0].get_y(), 0])
                       for v in range(1, 5)])
        yn = label(r"typical error", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(math.log10(n), math.log10(r)), radius=0.07, color=C.BITS) for n, r in zip(Ns, rms)])
        b = np.polyfit(np.log10(Ns), np.log10(rms), 1)
        fit = Line(ax.c2p(1, b[1] + b[0]), ax.c2p(5, b[1] + 5 * b[0]), color=WHITE, stroke_width=2.5)
        sl = label(rf"slope ${slope:.2f}$", font_size=30, color=WHITE).next_to(fit.point_from_proportion(0.55), UR, buff=0.15)
        colors = {r"\sigma": MODEL, r"N": DATA}
        f = cmath(r"\text{error}", r"\approx", r"\frac{\sigma}{\sqrt{N}}", colors=colors, font_size=48).move_to([4.7, 1.6, 0])
        notes = VGroup(label(r"one more digit: \ $100\times$ the samples", font_size=28, color=C.BITS),
                       label(r"the same rate in a million dimensions", font_size=28, color=GREY_A))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(f, DOWN, buff=0.5).set_x(4.4)
        cite_ = cite(r"N.~Metropolis \& S.~Ulam, \textit{The Monte Carlo Method} (1949)", corner=DR)
        with self.voiceover(
            "Repeat the experiment many times at each size, and measure the typical error. On log scales, where each "
            "tick is ten times the last, it falls on a straight line with slope minus a half. <bookmark mark='a'/> The error shrinks like one over the "
            "square root of the number of samples: every extra digit of accuracy costs a hundred times more "
            "samples. <bookmark mark='b'/> That's slow. But the rate doesn't care about dimension: averaging random "
            "samples works the same in a million dimensions, where any grid would be hopeless. That's why "
            "Monte Carlo, named by Ulam and Metropolis after the casino, is everywhere in machine learning."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(x10), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.15), run_time=1.5)
            self.play(Create(fit), FadeIn(sl))
            vo.wait_until("a")
            self.play(Write(f))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rare(self):
        d = load("montecarlo")
        true, plain, hits, is_est = float(d["true"]), float(d["plain_est"]), int(d["plain_hits"]), float(d["is_est"])
        n = int(d["n"])
        assert hits / n / true > 3 and abs(is_est / true - 1) < 0.05
        ax = Axes(x_range=[-4, 8, 1], y_range=[0, 0.45, 0.1], x_length=11.0, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.2, 0])
        xs = np.linspace(-4, 8, 300)
        p = curve(ax, xs, normal_pdf(xs), color=DATA, stroke_width=4)
        q = curve(ax, xs, normal_pdf(xs, 4.0), color=MODEL, stroke_width=4)
        pl = MathTex(r"p", font_size=40, color=DATA).next_to(ax.c2p(-1.2, normal_pdf(-1.2)), UL, buff=0.1)
        ql = MathTex(r"q", font_size=40, color=MODEL).next_to(ax.c2p(5.2, normal_pdf(1.2)), UR, buff=0.1)
        x4 = ax.c2p(4, 0)
        edge = DashedLine(x4, x4 + UP * 3.0, color=TAIL, stroke_width=2.5)
        tail_l = label(r"above $4$", font_size=26, color=TAIL).next_to(edge, UP, buff=0.1)
        g = np.random.default_rng(5)
        zs = g.normal(size=400)
        zs[:2] = [4.21, 4.47]  # two of the 10,000 (drawn here as 400) land above 4, as in the real run
        rug_p = VGroup(*[Line(ax.c2p(z, 0) + DOWN * 0.12, ax.c2p(z, 0) + DOWN * 0.32,
                              color=TAIL if z > 4 else DATA, stroke_width=2.5 if z > 4 else 1.2) for z in zs])
        ys = np.asarray(d["is_y"])
        rug_q = VGroup(*[Line(ax.c2p(y, 0) + DOWN * 0.42, ax.c2p(y, 0) + DOWN * 0.62,
                              color=MODEL if y > 4 else GREY_D, stroke_width=1.2) for y in ys])
        head = label(r"How often does a standard bell land above $4$?", font_size=32).to_edge(UP, buff=0.35)
        truth = label(rf"exactly: \ ${true * 1e5:.2f}$ in $100{{,}}000$", font_size=28, color=WHITE)
        truth.next_to(head, DOWN, buff=0.2)
        r1 = label(rf"draw from $p$: \ ${hits}$ of ${n:,}$ land there \ $\to$ ${plain * 1e5:.0f}$ in $100{{,}}000$"
                   .replace(",", "{,}").replace("{{,}}", "{,}"), font_size=28, color=DATA)
        r2 = label(rf"draw from $q$, \ weight by $p/q$: \ ${is_est * 1e5:.2f}$ in $100{{,}}000$", font_size=28, color=MODEL)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        colors = {r"p(x)": DATA, r"q(x)": MODEL, r"\mathbb{E}_p": DATA, r"\mathbb{E}_q": MODEL}
        f = cmath(r"\mathbb{E}_p", r"[f(x)]", "=", r"\mathbb{E}_q", r"\Big[f(x)\,", r"\frac{p(x)}{q(x)}", r"\Big]",
                  colors=colors, font_size=40).move_to([3.6, 2.0, 0])
        with self.voiceover(
            "Monte Carlo has one weakness: rare events. How often does a standard bell curve, the one centred at "
            "zero with a width of one, land above four? "
            "Exactly, about three times in a hundred thousand. <bookmark mark='a'/> Draw ten thousand samples, and "
            "only two land there. The estimate is off by a factor of six."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(p), FadeIn(pl))
            self.play(Create(edge), FadeIn(tail_l), FadeIn(truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rug_p], lag_ratio=0.004), run_time=1.5)
            self.play(Indicate(rug_p[0], color=TAIL, scale_factor=2.5), Indicate(rug_p[1], color=TAIL, scale_factor=2.5),
                      FadeIn(r1))
        with self.voiceover(
            "The fix is to cheat, and then correct for it. <bookmark mark='a'/> Draw from a different bell, one "
            "that lands out there half the time. <bookmark mark='b'/> Then weight each sample by how much more "
            "likely it was under the real distribution than under the one you drew from. <bookmark mark='c'/> Same "
            "number of samples, and now the answer is within one percent. This is importance sampling, and it comes "
            "back when models learn from samples drawn by an older version of themselves, in reinforcement learning."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(q), FadeIn(ql), LaggedStart(*[FadeIn(r) for r in rug_q], lag_ratio=0.004), run_time=1.8)
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()
