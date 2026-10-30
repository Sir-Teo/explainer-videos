from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, curve, density_picture, hist_shape, load, narrow_hist, normal_pdf



class Likelihood(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("galton")
        x = np.asarray(d["bins"], float)
        self.m, self.v = float(x.mean()), float(x.var())
        self.counts = np.asarray(d["counts"], float)
        self.card()
        self.score()
        self.landscape()
        self.cross_entropy()
        self.bias()

    def ll(self, mu, s):
        """Average log-likelihood, nats per ball, of a normal(mu, s) at the 1,000 positions."""
        return -0.5 * math.log(2 * math.pi * s * s) - (self.v + (self.m - mu) ** 2) / (2 * s * s)

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Fitting a bell", r"Which curve explains the data best?", part=PART)
        with self.voiceover("Chapter three. Fitting a bell to data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def score(self):
        mle = load("mle")
        assert abs(mle["mu_hat"] - self.m) < 1e-9 and abs(mle["ll_hat"] - self.ll(self.m, math.sqrt(self.v))) < 1e-9
        ax = Axes(x_range=[-0.5, 12.5, 1], y_range=[0, 0.56, 0.1], x_length=8.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.2, -0.6, 0])
        dens = self.counts / self.counts.sum()
        hist = hist_shape(ax, np.arange(14) - 0.5, dens, color=DATA, opacity=0.45)
        hl = label(r"where the $1{,}000$ balls landed", font_size=26, color=DATA).next_to(ax, DOWN, buff=0.2)
        mu, sg = ValueTracker(3.4), ValueTracker(1.0)
        xs = np.linspace(-0.5, 12.5, 220)
        bell = always_redraw(lambda: curve(ax, xs, np.minimum(normal_pdf(xs, mu.get_value(), sg.get_value()), 0.56),
                                           color=MODEL, stroke_width=4))

        def sticks():
            g = VGroup()
            for k, c in enumerate(self.counts):
                if c == 0:
                    continue
                h = float(normal_pdf(k, mu.get_value(), sg.get_value()))
                g.add(Line(ax.c2p(k, 0), ax.c2p(k, min(h, 0.56)), color=MODEL, stroke_width=2.5, stroke_opacity=0.8),
                      Dot(ax.c2p(k, min(h, 0.56)), radius=0.045, color=MODEL))
            return g

        st = always_redraw(sticks)
        colors = {r"\log q(x_i)": MODEL, r"x_i": DATA}
        f = cmath(r"\text{score}", "=", r"\frac{1}{n}\sum_i", r"\log q(x_i)", colors=colors, font_size=40)
        f.to_corner(UR, buff=0.45)
        fn = label(r"the log of the bell's height at each ball, \ averaged", font_size=24, color=GREY_A)
        fn.next_to(f, DOWN, buff=0.2).align_to(f, RIGHT)
        sv = DecimalNumber(self.ll(3.4, 1.0), num_decimal_places=2, include_sign=True, font_size=40, color=MODEL)
        sv.add_updater(lambda m: m.set_value(self.ll(mu.get_value(), sg.get_value())))
        read = VGroup(MathTex(r"\text{score} =", font_size=40), sv).arrange(RIGHT, buff=0.2).move_to([4.6, 0.6, 0])
        best = label(r"the best: \ maximum likelihood", font_size=30, color=C.BITS).next_to(read, DOWN, buff=0.4)
        dcard = gloss(r"probability density", r"the curve's height: \ how crowded the outcomes are there;\\ the area "
                      r"between two points is the probability", picture=density_picture(), corner=DR, width=4.4,
                      color=MODEL)
        dp = dcard[1][-1]
        with self.voiceover(
            "Here are the thousand balls again. Which bell describes them best? <bookmark mark='a'/> Try one. Score "
            "it like this: at each ball, read off the bell's height. <bookmark mark='p'/> That height is a "
            "probability density: how crowded the outcomes are there. Make a histogram's bars narrower and "
            "narrower, and it becomes a smooth curve like this one; <bookmark mark='q'/> the area under it between "
            "two points is the probability of landing between them. Take the log of the height, and average over "
            "all the balls. That's the log-likelihood: how well this bell predicted where the balls actually went. "
            "<bookmark mark='b'/> A bell in the wrong place scores badly. <bookmark mark='c'/> So does one that's too "
            "narrow, <bookmark mark='d'/> or too wide. <bookmark mark='e'/> The best bell, the maximum likelihood "
            "fit, is the one under which the data was least surprising."
        ) as vo:
            self.play(Create(ax), FadeIn(hist), FadeIn(hl))
            vo.wait_until("a")
            self.play(Create(bell), FadeIn(st), Write(f), FadeIn(fn), FadeIn(read))
            vo.wait_until("p")
            self.play(FadeIn(dcard))
            self.play(Transform(dp[1], narrow_hist(dp)), run_time=1.5)
            vo.wait_until("q")
            self.play(dp[3].animate.set_fill(opacity=0.6), dp[4].animate.set_opacity(1))
            vo.wait_until("b")
            self.play(mu.animate.set_value(self.m), run_time=2.0)
            vo.wait_until("c")
            self.play(sg.animate.set_value(0.75), run_time=1.5)
            vo.wait_until("d")
            self.play(sg.animate.set_value(3.6), run_time=1.5)
            vo.wait_until("e")
            self.play(sg.animate.set_value(math.sqrt(self.v)), run_time=1.5)
            self.play(FadeIn(best), Indicate(read, color=C.BITS))
        sv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landscape(self):
        m, v = self.m, self.v
        s_hat = math.sqrt(v)
        top = self.ll(m, s_hat)
        axes = ThreeDAxes(x_range=[3, 9, 1], y_range=[0.9, 4.0, 1], z_range=[0, 1, 0.5], x_length=7.0, y_length=4.6,
                          z_length=2.4, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        axes.shift(RIGHT * 2.2 + DOWN * 0.3)

        def f(a, b):  # the fit, as a hill: e^(score - best score), 1 at the top
            return math.exp(self.ll(a, b) - top)

        surf = loss_surface(axes, f, [3, 9], [0.9, 4.0], resolution=(40, 26), z_lo=0.0, z_hi=1.0)
        # climb: gradient ascent on (mu, sigma)
        p = np.array([3.6, 3.5])
        path = [p.copy()]
        for _ in range(120):
            a, b = p
            g = np.array([(m - a) / b ** 2, -1 / b + (v + (m - a) ** 2) / b ** 3])
            p = p + 0.35 * g
            path.append(p.copy())
        assert np.abs(path[-1] - [m, s_hat]).max() < 0.01
        ball = surface_ball(axes, f, *path[0], color=WHITE, radius=0.1)
        cuts = [0, 2, 5, 10, 20, 40, 80, len(path) - 1]  # the climb in pieces: fast at first, then creeping to the top
        trails = [surface_path(axes, f, path[a:b + 1], color=WHITE, lift=0.05, stroke_width=4) for a, b in zip(cuts, cuts[1:])]
        tracks = [surface_path(axes, f, path[a:b + 1], color=WHITE, lift=0.12) for a, b in zip(cuts, cuts[1:])]
        # the bell each point of the climb stands for, over the balls, in a corner
        bx = Axes(x_range=[-0.5, 12.5, 1], y_range=[0, 0.4, 0.1], x_length=3.6, y_length=1.5, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).to_corner(DL, buff=0.5).shift(UP * 0.55)
        bh = hist_shape(bx, np.arange(14) - 0.5, self.counts / self.counts.sum(), color=DATA, opacity=0.45)
        xs = np.linspace(-0.5, 12.5, 160)

        def bell_at(q):
            return curve(bx, xs, np.minimum(normal_pdf(xs, q[0], q[1]), 0.4), color=MODEL, stroke_width=3)

        bell = bell_at(path[0])
        bl = label(r"the bell at the ball's position", font_size=18, color=MODEL).next_to(bx, UP, buff=0.08)
        head = label(r"The score of every bell", font_size=34).to_edge(UP, buff=0.35)
        legend = label(r"across: \ the centre $\mu$; \ back: \ the width $\sigma$; \ up: \ $e^{\text{score}}$, "
                       r"relative to the best", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        colors = {r"\hat\mu": DATA, r"\hat\sigma^2": MODEL}
        res = VGroup(cmath(r"\hat\mu", "=", r"\frac{1}{n}\sum_i x_i", "=", rf"{m:.2f}", colors=colors, font_size=36),
                     cmath(r"\hat\sigma^2", "=", r"\frac{1}{n}\sum_i (x_i - \hat\mu)^2", "=", rf"{s_hat:.2f}^2",
                           colors=colors, font_size=36))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UL, buff=0.45).shift(DOWN * 0.5)
        resn = label(r"the average, \ and the average squared spread", font_size=24, color=GREY_A)
        resn.next_to(res, DOWN, buff=0.2).align_to(res, LEFT)
        for mob in (head, res, resn, legend, bx, bh, bell, bl):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
        self.set_camera_orientation(phi=60 * DEGREES, theta=-62 * DEGREES, zoom=0.8)
        with self.voiceover(
            "Score every possible bell, every centre and every width, and the scores form a landscape. "
            "<bookmark mark='a'/> From part four, we know how to find its top: follow the gradient uphill. "
            "<bookmark mark='b'/> At the summit, the centre is the balls' average, 5.96, and the width is their "
            "spread, 1.71, close to the square root of three that the pegs predict. For a bell, maximum likelihood "
            "comes out as the two most natural summaries of the data."
        ) as vo:
            self.play(Create(axes), FadeIn(surf), FadeIn(head), FadeIn(legend), run_time=1.6)
            self.play(FadeIn(ball), FadeIn(bx), FadeIn(bh), FadeIn(bell), FadeIn(bl))
            vo.wait_until("a")
            for tr_, tk_, b in zip(trails, tracks, cuts[1:]):
                self.play(MoveAlongPath(ball, tk_), Create(tr_), Transform(bell, bell_at(path[b])), run_time=0.6,
                          rate_func=linear)
            vo.wait_until("b")
            self.play(Write(res[0]))
            self.play(Write(res[1]), FadeIn(resn))
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def cross_entropy(self):
        colors = {r"\log q(x_i)": MODEL, r"\hat p": DATA, r"q": MODEL, r"H(\hat p, q)": C.SURPRISE}
        a = cmath(r"\text{maximize}", r"\;\frac{1}{n}\sum_i", r"\log q(x_i)", colors=colors, font_size=50)
        b = cmath(r"\text{minimize}", r"\;-\frac{1}{n}\sum_i", r"\log q(x_i)", colors=colors, font_size=50)
        c = cmath(r"\text{minimize}", r"\;H(\hat p, q)", colors=colors, font_size=50)
        for m in (a, b, c):
            m.move_to(UP * 0.8)
        cap = label(r"$\hat p$: \ the data's own frequencies; \ $H$: \ Part 1's cross-entropy, \ the average surprise",
                    font_size=28, color=GREY_A).next_to(a, DOWN, buff=0.6)
        every = label(r"how every model in this series is trained", font_size=34, color=C.BITS).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "And here's the connection to everything else. Maximizing the average log-likelihood <bookmark mark='a'/> "
            "is the same as minimizing the average surprise, <bookmark mark='b'/> and that's part one's cross-entropy, "
            "measured against the data. <bookmark mark='c'/> Maximum likelihood is minimum cross-entropy. It's how "
            "every model in this series is trained, from a bell curve to a language model."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("a")
            morph(self, a, b)
            vo.wait_until("b")
            morph(self, b, c)
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(every))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias(self):
        d = load("mlebias")
        ns, mle, bes, th = (np.asarray(d[k], float) for k in ("ns", "mle", "bessel", "theory"))
        R = int(d["R"])
        rows = [
            cmath(r"\textstyle\sum_i (x_i - \bar x)^2", "=", r"\textstyle\sum_i (x_i - \mu)^2 - n(\bar x - \mu)^2",
                  font_size=32),
            cmath(r"\mathbb{E}\big[\textstyle\sum_i (x_i - \bar x)^2\big]", "=", r"n\sigma^2 - n \cdot \sigma^2 / n",
                  font_size=32),
            cmath(r"\mathbb{E}[\hat\sigma^2]", "=", r"\frac{n-1}{n}\,\sigma^2", font_size=36, colors={r"\hat\sigma^2": MODEL}),
        ]
        whys = [why(r"expand around $\mu$", font_size=22), why(r"an average of $n$ has variance $\sigma^2/n$",
                                                               font_size=22),
                why(r"divide by $n$: \ too small on average", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=3.25, x=-2.4, buff=0.35, edge=6.8)
        ax = Axes(x_range=[0, 2.1, 1], y_range=[0.4, 1.1, 0.2], x_length=5.8, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.9, -1.9, 0])
        xt = VGroup(*[MathTex(str(int(v)), font_size=20, color=GREY_B).next_to(ax.c2p(math.log10(v), 0.4), DOWN, buff=0.1)
                      for v in (2, 5, 10, 20, 50, 100)])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in (("0.5", 0.5), ("1", 1.0))])
        xl = label(r"sample size $n$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        lx = np.log10(ns)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(2.1, 1), color=GREY_B, stroke_width=2)
        thc = curve(ax, np.log10(np.linspace(2, 120, 200)), 1 - 1 / np.linspace(2, 120, 200), color=MODEL, stroke_width=2.5)
        md = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=MODEL) for a, b in zip(lx, mle)])
        bd = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=C.INTERVAL) for a, b in zip(lx, bes)])
        leg = VGroup(label(r"divide by $n$ \ (maximum likelihood)", font_size=20, color=MODEL),
                     label(r"divide by $n - 1$ \ (Bessel)", font_size=20, color=C.INTERVAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.08)
        leg.next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        hx = Axes(x_range=[0, 4, 1], y_range=[0, 0.8, 0.2], x_length=4.6, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.7, -2.0, 0])
        h5 = np.asarray(d["hist5"], float)
        edges = np.linspace(0, 4, len(h5) + 1)
        hh = hist_shape(hx, edges, h5 / h5.sum() / (edges[1] - edges[0]), color=MODEL, opacity=0.4)
        i5 = list(ns).index(5)
        mline = DashedLine(hx.c2p(mle[i5], 0), hx.c2p(mle[i5], 0.8), color=MODEL, stroke_width=2.5)
        tline = DashedLine(hx.c2p(1, 0), hx.c2p(1, 0.8), color=GREY_B, stroke_width=2)
        hl = label(rf"$\hat\sigma^2$ from ${R:,}$ samples of $5$: \ average ${mle[i5]:.3f}$".replace(",", "{,}"),
                   font_size=20, color=MODEL).next_to(hx, UP, buff=0.12)
        hc = history_card(1922, r"R.~A.~Fisher", r"names likelihood, \ and asks of an estimate: \ consistent? \ "
                          r"efficient? \ sufficient?", width=4.0).to_corner(UR, buff=0.3)
        good = abs(mle[i5] - th[i5]) < 0.02 and abs(bes[i5] - 1) < 0.02
        verdict = (f"Measured on {R:,} samples of five, the average is {mle[i5]:.3f}, against the predicted "
                   f"{th[i5]:.2f}; dividing by n minus one, Bessel's correction, gives {bes[i5]:.3f}." if good else
                   f"Measured on {R:,} samples of five, the average is {mle[i5]:.3f}, against the predicted "
                   f"{th[i5]:.2f}.")
        with self.voiceover(
            "Is maximum likelihood right on average? For the centre, yes. For the spread, no. "
            "<bookmark mark='a'/> Measure spread around the sample's own average and you lose a little: the "
            "average sits closer to the data than the true centre does. <bookmark mark='b'/> On average, the loss "
            "is exactly one sigma squared, <bookmark mark='c'/> so the maximum-likelihood variance is too small by a "
            f"factor n minus one over n. <bookmark mark='d'/> {verdict} The bias fades as n grows. Fisher, who "
            "named likelihood in 1922, cared less about bias than about efficiency: how small the error can be. "
            "That is the next chapter."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(one), Create(thc), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(x) for x in md], lag_ratio=0.1), LaggedStart(*[FadeIn(x) for x in bd],
                                                                                         lag_ratio=0.1))
            self.play(Create(hx), FadeIn(hh), Create(tline), Create(mline), FadeIn(hl))
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

