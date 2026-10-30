from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, curve, hist_shape, load, normal_pdf

EST = {"mean": GREY_B, "med": C.INTERVAL, "mle": MODEL}
BOUND = C.BITS


def cauchy_pdf(x):
    return 1 / (math.pi * (1 + np.asarray(x) ** 2))


class Fisher(VoiceoverScene):
    def construct(self):
        self.card()
        self.cauchy()
        self.derive()
        self.measure()
        self.uses()

    def card(self):
        card = chapter_card(4, r"How precise can an estimate be?", r"Is there a limit to what data can tell you?",
                            part=PART)
        with self.voiceover("Chapter four. How precise can an estimate be?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cauchy(self):
        d = load("fisher")
        ax = Axes(x_range=[-6, 6, 2], y_range=[0, 0.42, 0.1], x_length=6.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, 1.5, 0])
        xs = np.linspace(-6, 6, 300)
        cc = curve(ax, xs, cauchy_pdf(xs), color=DATA, stroke_width=4)
        nc = curve(ax, xs, normal_pdf(xs), color=GREY_B, stroke_width=2.5).set_stroke(opacity=0.6)
        cl = label(r"Cauchy: \ $\dfrac{1}{\pi\,(1 + (x - \theta)^2)}$", font_size=24, color=DATA)
        cl.next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        nl = label(r"a bell, for comparison", font_size=20, color=GREY_B).next_to(ax.c2p(1.2, 0.3), RIGHT, buff=0.1)
        g = np.random.default_rng(3)
        sample = np.clip(g.standard_cauchy(40), -5.8, 5.8)
        rug = VGroup(*[Line(ax.c2p(v, 0) + DOWN * 0.1, ax.c2p(v, 0) + DOWN * 0.35, color=DATA, stroke_width=2)
                       for v in sample])
        rt = note(r"$40$ draws, \ illustration \ (the far ones clipped at the edge)").next_to(rug, DOWN, buff=0.1)
        # three estimators of the centre, from 4,000 samples of 100
        hx = Axes(x_range=[-1.2, 1.2, 0.4], y_range=[0, 4.2, 1], x_length=9.0, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_numbers": False}).move_to([0.0, -2.1, 0])
        hx.y_axis.set_stroke(opacity=0)
        edges = np.linspace(-1.2, 1.2, 49)
        R = int(d["R"])
        hs = {}
        for k in ("mean", "med", "mle"):
            h = np.asarray(d[f"{k}100"], float)
            hs[k] = hist_shape(hx, edges, np.minimum(h / R / (edges[1] - edges[0]), 4.2), color=EST[k],
                               opacity=0.55 if k == "mean" else 0.3, stroke_width=3 if k == "mean" else 2)
        names = VGroup(label(r"the average", font_size=22, color=EST["mean"]),
                       label(r"the median", font_size=22, color=EST["med"]),
                       label(r"maximum likelihood", font_size=22, color=EST["mle"])).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        names.scale(1.15).move_to([3.6, 1.3, 0])
        hl = label(rf"estimates of $\theta = 0$, \ from ${R:,}$ samples of $100$".replace(",", "{,}"), font_size=22,
                   color=GREY_A).next_to(hx, UP, buff=0.15)
        iqr = np.asarray(d["mean_iqr"])
        ns = [int(v) for v in d["ns"]]
        with self.voiceover(
            "Here is a distribution with heavy tails, the Cauchy. It looks like a bell, but its tails are so heavy "
            "that it has no average: now and then a draw lands absurdly far out. <bookmark mark='a'/> Try to "
            "estimate its centre from a hundred draws. The sample average is useless: its spread never shrinks; "
            f"the middle half of the averages spans {iqr[0]:.1f} at {ns[0]} draws and still {iqr[-1]:.1f} at "
            f"{ns[-1]}. <bookmark mark='b'/> The median does much better, <bookmark mark='c'/> and maximum "
            "likelihood better still. Is there a best possible?"
        ) as vo:
            self.play(Create(ax), Create(cc), Create(nc), FadeIn(cl), FadeIn(nl))
            self.play(LaggedStart(*[Create(r) for r in rug], lag_ratio=0.05), FadeIn(rt), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(hx), FadeIn(hl), FadeIn(hs["mean"]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(FadeIn(hs["med"]), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(FadeIn(hs["mle"]), FadeIn(names[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        d = load("fisher")
        colors = {r"s": C.INTERVAL, r"I(\theta)": BOUND, r"\hat\theta": MODEL}
        rows = [
            cmath(r"s", "=", r"\frac{\partial}{\partial\theta} \log p(x \mid \theta)", colors=colors, font_size=34),
            cmath(r"\mathbb{E}[s]", "=", r"\int \frac{\partial p}{\partial\theta}\, dx = \frac{\partial}{\partial\theta}"
                  r"\int p\, dx = 0", font_size=34),
            cmath(r"I(\theta)", "=", r"\mathbb{E}[s^2] = -\mathbb{E}\Big[\frac{\partial^2 \log p}{\partial\theta^2}\Big]",
                  colors=colors, font_size=34),
            cmath(r"\operatorname{Cov}(\hat\theta, s)", "=", r"\frac{\partial}{\partial\theta}\,\mathbb{E}[\hat\theta] = 1",
                  font_size=34),
            cmath(r"1", r"\le", r"\operatorname{Var}(\hat\theta)\; n\, I(\theta)", font_size=36),
        ]
        whys = [why(r"the score: \ how the log-likelihood tilts"),
                why(r"the density integrates to $1$"),
                why(r"Fisher information: \ the score's variance"),
                why(r"unbiased: \ $\mathbb{E}[\hat\theta] = \theta$, \ differentiated"),
                why(r"Cauchy--Schwarz; \ $n$ points add their information")]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-2.0, buff=0.3, edge=6.8)
        thm = theorem_card(r"Cram\'er--Rao", r"an unbiased estimate from $n$ independent points has variance at least "
                           r"$1 / (n\, I(\theta))$", who=r"C.~R.~Rao (1945), \ H.~Cram\'er (1946)", width=6.2,
                           color=BOUND).to_corner(DR, buff=0.25)
        sa = Axes(x_range=[-6, 6, 2], y_range=[-1.2, 1.2, 1], x_length=5.0, y_length=1.7, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).to_corner(DL, buff=0.3)
        uu = np.linspace(-6, 6, 200)
        sc_ = curve(sa, uu, 2 * uu / (1 + uu * uu), color=C.INTERVAL, stroke_width=3)
        scl = label(r"the score of one Cauchy draw, \ $2u/(1+u^2)$: \ far draws pull little", font_size=20,
                    color=C.INTERVAL).next_to(sa, UP, buff=0.08).align_to(sa, LEFT)
        sv = float(d["score_var"])
        with self.voiceover(
            "There is, and Fisher found the key in 1925. <bookmark mark='a'/> The score is the slope of the "
            "log-likelihood in the parameter: how much each observation pulls the estimate. <bookmark mark='b'/> "
            "At the true value it averages to zero, because the density always integrates to one. "
            "<bookmark mark='c'/> Its variance is the Fisher information: how sharply the data pins theta down. "
            f"For the Cauchy it is one half; over two hundred thousand draws we measure {sv:.3f}. "
            "<bookmark mark='d'/> An unbiased estimate moves one for one with theta, so its covariance with the "
            "score is one. <bookmark mark='e'/> And Cauchy-Schwarz says a covariance squared is at most the product "
            "of the variances. So no unbiased estimate can have variance below one over n times the information: "
            "the Cramer-Rao bound, proved by Rao in 1945 and Cramer in 1946."
        ) as vo:
            self.play(Create(sa), Create(sc_), FadeIn(scl))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        d = load("fisher")
        ns = np.asarray(d["ns"], float)
        mle, med = np.asarray(d["mle_nvar"]), np.asarray(d["med_nvar"])
        cr, ml = float(d["cr"]), float(d["med_limit"])
        ax = Axes(x_range=[0.6, 2.8, 1], y_range=[0, 7, 1], x_length=8.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.5, 0])
        xt = VGroup(*[MathTex(str(int(v)), font_size=22, color=GREY_B).next_to(ax.c2p(math.log10(v), 0), DOWN, buff=0.12)
                      for v in ns])
        yt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(0.6, v), LEFT, buff=0.12)
                      for v in (0, 2, 4, 6)])
        xl = label(r"sample size $n$", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yl = label(r"$n \times$ variance of the estimate", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lx = np.log10(ns)
        bound = DashedLine(ax.c2p(0.6, cr), ax.c2p(2.8, cr), color=BOUND, stroke_width=3)
        bl = label(r"Cram\'er--Rao: \ $1/I = 2$", font_size=24, color=BOUND).next_to(ax.c2p(2.8, cr), DOWN, buff=0.12).align_to(ax.c2p(2.8, 0), RIGHT)
        medl = DashedLine(ax.c2p(0.6, ml), ax.c2p(2.8, ml), color=EST["med"], stroke_width=2).set_stroke(opacity=0.5)
        medt = label(r"$\pi^2/4$", font_size=22, color=EST["med"]).next_to(ax.c2p(2.8, ml), RIGHT, buff=0.1)

        def series(v, col):
            return VGroup(curve(ax, lx, np.minimum(v, 7), color=col, stroke_width=3.5),
                          *[Dot(ax.c2p(a, min(b, 7)), radius=0.06, color=col) for a, b in zip(lx, v)])

        s_mle, s_med = series(mle, EST["mle"]), series(med, EST["med"])
        lm = label(r"maximum likelihood", font_size=22, color=EST["mle"]).move_to(ax.c2p(1.45, 4.2), aligned_edge=LEFT)
        ld = label(r"the median", font_size=22, color=EST["med"]).next_to(ax.c2p(lx[0], min(med[0], 7)), RIGHT, buff=0.15)
        hc = history_card(1925, r"R.~A.~Fisher", r"maximum likelihood is efficient: \ it reaches the bound as $n$ grows",
                          width=4.0).to_corner(UR, buff=0.3)
        reach = abs(mle[-1] - cr) / cr < 0.05
        verdict = (f"by {int(ns[-1])} draws it is {mle[-1]:.2f}, within a few percent of the bound." if reach else
                   f"by {int(ns[-1])} draws it is {mle[-1]:.2f}, still above the bound.")
        with self.voiceover(
            "Now measure it. Multiply each estimate's variance by n, so that a perfect one-over-n estimate is a "
            f"flat line; the bound is the line at two. <bookmark mark='a'/> The median levels off at {med[-1]:.2f}, "
            "close to its theoretical pi squared over four: about a quarter worse than the bound, forever. "
            f"<bookmark mark='b'/> Maximum likelihood starts high, {mle[0]:.1f} at five draws, but {verdict} "
            "<bookmark mark='c'/> That is Fisher's efficiency: in large samples, nothing beats maximum likelihood."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(bound), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(s_med), FadeIn(ld), Create(medl), FadeIn(medt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(s_mle), FadeIn(lm), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        head = label(r"Fisher information in today's training", font_size=36).to_edge(UP, buff=0.4)
        f = cmath(r"F", "=", r"\mathbb{E}\big[\nabla_\theta \log p\, \nabla_\theta \log p^\top\big]", font_size=40,
                  colors={r"F": BOUND}).next_to(head, DOWN, buff=0.6)
        fn = label(r"the same idea for many parameters: \ a matrix", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.15)
        cards = VGroup(
            history_card(1998, r"Amari: \ the natural gradient", r"measure a step by how much the model's predictions "
                         r"change, \ not the weights: \ $F^{-1}\nabla L$ \ (Part 11)", width=4.3, font_size=24),
            history_card(2017, r"Kirkpatrick et al.: \ elastic weight consolidation", r"protect the weights a learned "
                         r"task has high information about", width=4.3, font_size=24),
            history_card(r"today", r"curvature-aware optimizers", r"K-FAC approximates $F$ layer by layer; \ Shampoo "
                         r"uses a close cousin \ (Part 11)", width=4.3, font_size=24),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(fn, DOWN, buff=1.0)
        with self.voiceover(
            "With many parameters, the information becomes a matrix: the average outer product of the score. "
            "<bookmark mark='a'/> In 1998 Shun-ichi Amari proposed measuring steps of gradient descent by it, so "
            "that a step is judged by how much the model's predictions change, not its weights: the natural "
            "gradient. <bookmark mark='b'/> In 2017, elastic weight consolidation used it to protect what a network "
            "had learned. <bookmark mark='c'/> And today's curvature-aware optimizers approximate it, or a close cousin, layer by layer. "
            "Part eleven picks them up."
        ) as vo:
            self.play(FadeIn(head), Write(f), FadeIn(fn))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
