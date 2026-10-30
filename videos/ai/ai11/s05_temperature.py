from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import PART, lag, load, takeaway_card
from videos.ai.ai11.s04_sgd import B_COLORS, loss_axes

PUSH, KICK = C.TRUE_P, C.NEURAL  # the SDE's two parts
ETA_COLS = ["#4FA3D9", "#7FD3FF", C.BITS, C.SURPRISE]


class Temperature(VoiceoverScene):
    def construct(self):
        self.card()
        self.sde()
        self.stationary()
        self.measure()
        self.scaling()
        self.flat()
        self.takeaway()

    def card(self):
        c = chapter_card(4, r"Noise as temperature", r"How big is the cloud, and what is it for?", part=PART)
        with self.voiceover("Chapter four. Noise as temperature."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def sde(self):
        head = label(r"one step of SGD, \ and a stochastic differential equation", font_size=30).to_edge(UP, buff=0.3)
        cl = {r"\sqrt{\eta / B}": KICK, r"-\nabla L(\theta)\,dt": PUSH, r"\eta / B": KICK}
        rows = [
            cmath(r"\theta_{k+1}", "=", r"\theta_k - \eta\,\nabla L(\theta_k) - \eta\,\xi_k", r",\quad \operatorname{Cov}\xi_k = \Sigma/B",
                  font_size=34),
            cmath(r"\theta_{k+1} - \theta_k", "=", r"-\nabla L\;\eta - \sqrt{\eta}\,\sqrt{\eta / B}\;\Sigma^{1/2} z_k",
                  r",\quad z_k \sim \mathcal{N}(0, I)", font_size=34, colors=cl),
            cmath(r"d\theta", "=", r"-\nabla L(\theta)\,dt", "+", r"\sqrt{\eta / B}", r"\;\Sigma^{1/2}\,dW_t", font_size=38,
                  colors=cl),
        ]
        whys = [why(r"the batch's gradient: \ the true one plus noise"),
                why(r"write $\eta = dt$, \ the noise as $\sqrt{dt}$ times a Gaussian"),
                why(r"Euler--Maruyama, \ read backwards (Part 5)")]
        step = ladder(self, rows, whys, keep=3, top=2.2, x=-2.0, buff=0.6, edge=6.9)
        cite_ = cite(r"Q.~Li, C.~Tai \& W.~E (2017); \ S.~Mandt, M.~Hoffman \& D.~Blei (2017); \ S.~Smith \& Q.~Le (2018)",
                     corner=DL)
        with self.voiceover(
            "How big is the cloud? Part five's stochastic differential equations answer it. <bookmark mark='a'/> A "
            "step of stochastic gradient descent is the true gradient step, plus the batch's noise, with covariance "
            "sigma over B. <bookmark mark='b'/> Call the step size eta a small time interval, dt. The noise term is "
            "then the square root of dt, times a Gaussian, times the square root of eta over B. "
            "<bookmark mark='c'/> That is exactly one Euler step of a stochastic differential equation: a push "
            "downhill, plus random kicks whose strength is eta over B. The learning rate and the batch size enter "
            "only through their ratio. Physicists would call it a temperature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            parts = VGroup(brace_note(term(rows[2], r"-\nabla L(\theta)\,dt"), r"push downhill", color=PUSH, font_size=22),
                           brace_note(VGroup(term(rows[2], r"\sqrt{\eta / B}"), term(rows[2], r"\;\Sigma^{1/2}\,dW_t")),
                                      r"random kicks, \ temperature $\eta/B$", color=KICK, font_size=22))
            self.play(FadeOut(whys[2]), FadeIn(parts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stationary(self):
        t = load("temperature")
        head = label(r"near the bottom, \ $\nabla L \approx H\,(\theta - \theta^*)$", font_size=30).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"S", "=", r"(I - \eta H)\,S\,(I - \eta H) + \frac{\eta^2}{B}\,C", font_size=34),
            cmath(r"H S + S H", r"\approx", r"\frac{\eta}{B}\,C", font_size=34),
            cmath(r"\mathbb{E}\,\|\theta - \theta^*\|^2 = \operatorname{tr} S", r"\approx",
                  r"\frac{\eta}{2B}\,\operatorname{tr}\!\big(H^{-1} C\big)", font_size=34),
        ]
        whys = [why(r"$S$: \ the cloud's covariance, \ unchanged by a step"),
                why(r"drop the $\eta^2 H S H$ term: \ small $\eta$"),
                why(r"multiply by $H^{-1}$, \ take the trace")]
        step = ladder(self, rows, whys, keep=3, top=2.1, x=-1.6, buff=0.6, edge=6.9)
        tr = float(t["trHinvC"])
        fact = label(rf"for our loss: \ $\operatorname{{tr}}(H^{{-1}}C) = {tr:.2f}$, \ close to $2$, \ the number of "
                     r"weights: \\ at the bottom of a log-loss, \ the noise's covariance $C$ is nearly the curvature $H$",
                     font_size=22, color=C.BITS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Near the bottom the gradient is the Hessian times the distance, and the cloud stops changing: its "
            "covariance S comes out of each step the same as it went in. <bookmark mark='a'/> That is an equation "
            "for S. <bookmark mark='b'/> For small steps it simplifies to H S plus S H equals eta over B times the "
            "noise's covariance C. <bookmark mark='c'/> Take the trace: the cloud's mean squared size is eta over two "
            f"B, times the trace of H inverse C. <bookmark mark='d'/> For our two-weight loss that trace is {tr:.2f}, "
            "close to two, because at the bottom of a log-loss the gradient's noise and the curvature are nearly "
            "the same matrix."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            for k, mk in enumerate("bc"):
                vo.wait_until(mk)
                step(k + 1)
            vo.wait_until("d")
            self.play(FadeIn(fact))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        t = load("temperature")
        etas, Bs = list(t["etas"]), list(t["batches"])
        M = np.asarray(t["measured"])  # eta x B x seed
        P = np.asarray(t["predicted"])
        T = np.array([[e / b for b in Bs] for e in etas])
        lx, ly = np.log10(T), np.log10(M.mean(2))
        x0, x1 = math.floor(lx.min() * 2) / 2 - 0.1, math.ceil(lx.max() * 2) / 2 + 0.1
        y0, y1 = math.floor(ly.min() * 2) / 2 - 0.1, math.ceil(ly.max() * 2) / 2 + 0.1
        ax = CornerAxes(x_range=[x0, x1, 0.5], y_range=[y0, y1, 0.5], x_length=6.8, y_length=4.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.4, -0.4, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, y0), DOWN, buff=0.1)
                      for k in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, k), LEFT, buff=0.1)
                      for k in range(math.ceil(y0), math.floor(y1) + 1)])
        xn = label(r"temperature \ $\eta / B$", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"the cloud's mean squared size, \ $\mathbb{E}\,\|w - w^*\|^2$", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        pts = VGroup()
        for i, (e, col) in enumerate(zip(etas, ETA_COLS)):
            for j in range(len(Bs)):
                lo_, hi_ = np.log10(M[i, j].min()), np.log10(M[i, j].max())
                pts.add(VGroup(Line(ax.c2p(lx[i, j], lo_), ax.c2p(lx[i, j], hi_), color=col, stroke_width=2),
                               Dot(ax.c2p(lx[i, j], ly[i, j]), radius=0.06, color=col)))
        order = np.argsort(T.ravel())
        pred = DashedVMobject(curve(ax, lx.ravel()[order], np.log10(P.ravel()[order]), WHITE, 2.2),
                              num_dashes=36)
        key = VGroup(*[label(rf"$\eta = {e:g}$", font_size=22, color=col) for e, col in zip(etas, ETA_COLS)])
        key.add(label(r"batches $B = 1, 2, 4, \dots, 32$", font_size=20, color=GREY_A))
        key.add(label(r"dashed: \ the stationary $S$, \ predicted", font_size=20, color=WHITE))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, 1.2, 0])
        slope = float(t["slope"])
        ratio = np.asarray(t["ratio"])
        rlo, rhi = float(ratio.min()), float(ratio.max())
        res = label(rf"slope ${slope:.2f}$; \ measured over predicted: \ ${rlo:.2f}$ to ${rhi:.2f}$", font_size=22,
                    color=C.BITS).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        keep_in_frame(res)
        tag = note(r"each point: $30{,}000$ steps from the bottom, \ $3$ seeds (bar: \ min to max); \ computed").to_corner(DL, buff=0.2)
        good = 0.8 < slope < 1.2 and rlo > 0.7 and rhi < 1.4
        said1 = (f"they fall on one line, of slope {slope:.2f}: double the learning rate and double the batch, and "
            "the cloud is the same. "
            if 0.8 < slope < 1.2 else
            f"they rise with slope {slope:.2f}. ")
        said2 = (f"Measured over predicted, every point is between {rlo:.2f} and {rhi:.2f}."
            if good else
            f"Measured over predicted runs from {rlo:.2f} to {rhi:.2f}: the linear picture is only approximate "
            "here.")
        with self.voiceover(
            "Measure it. Four learning rates, six batch sizes, three seeds each: twenty-four clouds. "
            "<bookmark mark='a'/> Plotted against the temperature, eta over B, "
            + said1
            + "<bookmark mark='b'/> The dashed line is the predicted stationary size. "
            + said2
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            self.play(lag([FadeIn(p, scale=0.6) for p in pts], lag_ratio=0.04), FadeIn(key[:4]), FadeIn(key[4]), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(pts, scale_factor=1.05, color=WHITE), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(pred), FadeIn(key[5]), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scaling(self):
        rule = definition_card(r"The linear scaling rule", r"Multiply the batch by $k$: \ multiply the learning rate "
                               r"by $k$ too, \ and the noise per unit of progress is unchanged. \ With a short warmup "
                               r"it trained ImageNet with batches of $8{,}192$ in one hour \ (Goyal et al., 2017).",
                               width=6.6, font_size=22).to_corner(UL, buff=0.35)
        adam = definition_card(r"\dots and for Adam, \ a square root", r"Adam divides by the gradient's size, which a bigger "
                               r"batch also changes: \ its SDE says scale the learning rate by $\sqrt{k}$ \ (Malladi, Lyu, "
                               r"Panigrahi \& Arora, 2022).", width=6.6, font_size=22, color=C.MODEL_Q)
        adam.next_to(rule, DOWN, buff=0.35).align_to(rule, LEFT)
        # the rule breaks: steps to a target against batch, schematic hyperbola
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=4.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.0, 0.2, 0])
        bb = np.linspace(0, 4, 80)
        s = np.log10(1 + 10 ** (2.0 - bb)) + 1.0
        ideal = DashedLine(ax.c2p(0, 3.04), ax.c2p(2.04, 1.0), color=GREY_B, stroke_width=2)
        cur = curve(ax, bb, s, C.BITS, 3)
        xl = label(r"batch size \ (log)", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        yl = label(r"steps to a target loss \ (log)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1)
        kn = label(r"the critical batch: \\ Part 12, Chapter 6", font_size=20, color=C.BITS).next_to(ax.c2p(2, 1.3), UR, buff=0.1)
        sch = note(r"schematic").next_to(xl, DOWN, buff=0.1)
        with self.voiceover(
            "This explains a rule found by experiment. <bookmark mark='a'/> Multiply the batch by k, and the "
            "learning rate by k too: the temperature stays the same. In 2017 a Facebook team used it, with a short "
            "warmup, to train an ImageNet classifier on batches of eight thousand images in one hour. "
            "<bookmark mark='b'/> For Adam, which divides by the gradient's size, the analysis says scale by root k "
            "instead. <bookmark mark='c'/> And past a critical batch size the noise is already small, and bigger "
            "batches stop buying fewer steps; Part twelve measures where."
        ) as vo:
            self.play(FadeIn(rule, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch), Create(ideal))
            vo.wait_until("b")
            self.play(FadeIn(adam, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Create(cur), FadeIn(kn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flat(self):
        d = load("noise")
        ax, cont, star = loss_axes(d, center=(-3.2, 0.4), width=5.6)
        w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])

        def inside(P):
            P = np.asarray(P)
            return P[(P[:, 0] > w1[0]) & (P[:, 0] < w1[-1]) & (P[:, 1] > w2[0]) & (P[:, 1] < w2[-1])]

        c1 = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=B_COLORS[1], fill_opacity=0.6) for p in inside(d["cloud1"])])
        c16 = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=B_COLORS[16], fill_opacity=0.8) for p in inside(d["cloud16"])])
        sp1, sp16 = float(d["spread1"]), float(d["spread16"])
        cap = label(rf"batch $1$: \ spread ${sp1:.2f}$; \ batch $16$: \ ${sp16:.2f}$ \ ($\times {sp16 / sp1:.2f}$, \ "
                    r"$1/\sqrt{16} = 0.25$)", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.2)

        def land(x):
            return 0.95 - 0.8 * np.exp(-((x + 1.3) / 0.16) ** 2) - 0.75 * np.exp(-((x - 0.9) / 0.7) ** 2) + 0.04 * x * x

        lx0, ly0, sx, sy = 3.6, -0.6, 1.25, 1.5

        def lp(x, lift=0.0):
            return np.array([lx0 + sx * x, ly0 + sy * land(x) + lift, 0])

        lcurve = VMobject(color=GREY_A, stroke_width=3).set_points_smoothly([lp(x) for x in np.linspace(-2.3, 2.3, 140)])
        lsharp = label(r"sharp", font_size=20, color=C.SURPRISE).next_to(lp(-1.3), DOWN, buff=0.1)
        lwide = label(r"wide", font_size=20, color=C.INTERVAL).next_to(lp(0.9), DOWN, buff=0.1)
        hops = [-1.3, -1.22, -1.4, -1.18, -1.45, -1.05, -0.6, -0.1, 0.45, 0.8, 1.05, 0.85, 1.0, 0.9]
        ball = Dot(lp(hops[0], 0.09), radius=0.09, color=WHITE)
        sch = note(r"schematic").next_to(lp(0.0), DOWN, buff=0.9)
        head = label(r"a hot walker can't stay in a narrow hole", font_size=26, color=C.BITS).move_to([3.6, 2.6, 0])
        cite_ = cite(r"N.~Keskar et al.\ (2017); \ L.~Dinh, R.~Pascanu, S.~Bengio \& Y.~Bengio (2017)", corner=DR)
        caveat = label(r"but sharpness depends on how the weights are written: \\ rescale a layer and a sharp minimum "
                       r"looks flat", font_size=20, color=GREY_B).move_to([3.6, -2.6, 0])
        with self.voiceover(
            "Is the noise only a cost? <bookmark mark='a'/> On the real loss, sixteen times the batch gives a "
            f"cloud {sp1 / sp16:.1f} times narrower, close to root sixteen. <bookmark mark='b'/> Now picture a sharp "
            "pit beside a wide basin: a hot walker is kicked out of the pit and settles where the valley is wide. "
            "<bookmark mark='c'/> In 2017 Nitish Keskar and colleagues found that very large batches end in sharper "
            "minima that generalize worse. <bookmark mark='d'/> The same year Laurent Dinh and colleagues found the "
            "catch: rescale one layer up and the next down, and the same function has a different sharpness. "
            "Flatness is a useful picture, not a law."
        ) as vo:
            self.play(Create(cont), FadeIn(star))
            self.play(LaggedStart(*[FadeIn(p) for p in c1], lag_ratio=0.003), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in c16], lag_ratio=0.003), FadeIn(cap), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(head), Create(lcurve), FadeIn(lsharp), FadeIn(lwide), FadeIn(ball), FadeIn(sch))
            self.play(Succession(*[ball.animate(run_time=0.3, rate_func=smooth).move_to(lp(x, 0.09)) for x in hops[1:]]))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        r = np.asarray(load("temperature")["ratio"])
        t = takeaway_card(r"SGD runs at a temperature $\eta/B$",
                          r"Its stationary cloud has size $\frac{\eta}{2B}\operatorname{tr}(H^{-1}C)$ \ (measured here: "
                          rf"${r.min():.2f}$ to ${r.max():.2f}$ times that). \ Same ratio, \ same noise: \ the linear "
                          r"scaling rule.", r"Next: \ how big can $\eta$ be at all?")
        with self.voiceover(
            "So stochastic gradient descent runs at a temperature, eta over B, which sets the size of the cloud it "
            "ends in, and keeping that ratio fixed is the linear scaling rule. But how large can the step itself be?"
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
