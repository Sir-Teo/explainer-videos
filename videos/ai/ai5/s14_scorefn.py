from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, curve, load, normal_pdf

SF = C.INTERVAL  # the score-function estimate
REP = C.MODEL_Q  # the reparameterized estimate
BASE = C.BITS  # a baseline
PLAIN = C.SURPRISE


def valley(x, y):
    return (1 - x) ** 2 + 5 * (y - x * x) ** 2


class ScoreFn(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.derive()
        self.variance()
        self.es()

    def card(self):
        card = chapter_card(12, r"The gradient of an average", r"How do you differentiate through a random choice?",
                            part=PART)
        with self.voiceover("Chapter twelve. The gradient of an average."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        ax = Axes(x_range=[-3, 4, 1], y_range=[0, 1.2, 0.5], x_length=9.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-0.6, -0.8, 0])
        mu = ValueTracker(0.0)
        xs = np.linspace(-3, 4, 300)
        bell = always_redraw(lambda: curve(ax, xs, 2.2 * normal_pdf(xs, mu.get_value()), color=DATA, stroke_width=4))
        step = np.where((xs > 1.0) & (xs < 2.2), 1.0, 0.15)
        fc = curve(ax, xs, step, color=C.BITS, stroke_width=3)
        fl = label(r"$f(x)$: \ a reward, \ a judge's yes or no: \ no slope to follow", font_size=24, color=C.BITS)
        fl.next_to(ax.c2p(2.2, 1.0), UR, buff=0.1)
        ml = label(r"$p_\theta(x)$: \ what the model samples", font_size=24, color=DATA).next_to(ax.c2p(-1.0, 0.9), UL, buff=0.05)
        f = cmath(r"\nabla_\theta\, \mathbb{E}_{x \sim p_\theta}", r"\big[f(x)\big]", "=", r"\;?", font_size=44).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Much of machine learning ends with an average over random choices: the expected reward of a policy, "
            "the expected score of a sampled answer. <bookmark mark='a'/> We want its gradient, to improve the "
            "model. But the thing being averaged may have no slope at all: a reward that switches on and off, a "
            "judge who says yes or no. <bookmark mark='b'/> Only the distribution moves smoothly as the parameters "
            "change. How do we differentiate through the sampling?"
        ) as vo:
            self.play(Write(f), Create(ax), Create(bell), FadeIn(ml))
            vo.wait_until("a")
            self.play(Create(fc), FadeIn(fl))
            vo.wait_until("b")
            self.play(mu.animate.set_value(1.2), run_time=1.5)
            self.play(mu.animate.set_value(0.4), run_time=1.0)
        bell.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\nabla_\theta \log p_\theta(x)": SF, r"b": BASE}
        rows = [
            cmath(r"\nabla_\theta\, \mathbb{E}[f]", "=", r"\int \nabla_\theta\, p_\theta(x)\, f(x)\, dx", font_size=36),
            cmath(r"\nabla_\theta\, \mathbb{E}[f]", "=", r"\int p_\theta(x)\,", r"\nabla_\theta \log p_\theta(x)",
                  r"\, f(x)\, dx", colors=colors, font_size=36),
            cmath(r"\nabla_\theta\, \mathbb{E}[f]", "=", r"\mathbb{E}\big[f(x)\,", r"\nabla_\theta \log p_\theta(x)",
                  r"\big]", colors=colors, font_size=36),
            cmath(r"\nabla_\theta\, \mathbb{E}[f]", "=", r"\mathbb{E}\big[(f(x) - ", r"b", r")\,",
                  r"\nabla_\theta \log p_\theta(x)", r"\big]", colors=colors, font_size=36),
        ]
        whys = [why(r"only the density depends on $\theta$"),
                why(r"$\nabla p = p\, \nabla \log p$: \ the log-derivative trick"),
                why(r"an average: \ estimate it by sampling"),
                why(r"$\mathbb{E}[\nabla \log p] = 0$ \ (Chapter 4): \ any baseline $b$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.0, buff=0.55, edge=6.8)
        cite_ = cite(r"P.~W.~Glynn (1990); \ R.~J.~Williams, REINFORCE (1992)", corner=DR)
        with self.voiceover(
            "Move the gradient inside the integral: only the density depends on theta. <bookmark mark='a'/> Then "
            "the log-derivative trick: the gradient of p is p times the gradient of log p, <bookmark mark='b'/> and "
            "the gradient is again an average, of f times the score, which we met in chapter four. Sample, and "
            "average. f itself is never differentiated. <bookmark mark='c'/> And since the score averages to zero, "
            "any constant b can be subtracted from f without changing the answer: a baseline. Peter Glynn called "
            "this the likelihood-ratio method in 1990; Ronald Williams made it a learning rule for neural networks "
            "in 1992, REINFORCE."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variance(self):
        d = load("scorefn")
        bs, vb = np.asarray(d["bs"]), np.asarray(d["var_b"])
        v0, vstar, vrep, bstar = float(d["var_0"]), float(d["var_star"]), float(d["var_rep"]), float(d["b_star"])
        mean_sf = float(d["mean_sf"])
        head = label(r"$\nabla_\mu\, \mathbb{E}[x^2]$, \ $x \sim \mathcal{N}(\mu, 1)$, \ at $\mu = 1$: \ truly $2$",
                     font_size=30).to_edge(UP, buff=0.4)
        ax = Axes(x_range=[-2, 6, 1], y_range=[0, 40, 10], x_length=7.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.7, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (-2, 0, 2, 4, 6)])
        yt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(-2, v), LEFT, buff=0.1) for v in (0, 20, 40)])
        xl = label(r"baseline $b$", font_size=24, color=BASE).next_to(xt, DOWN, buff=0.1)
        yl = label(r"variance of one sample's estimate", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        cv = curve(ax, bs, np.minimum(vb, 40), color=SF, stroke_width=4)
        d0 = Dot(ax.c2p(0, v0), radius=0.08, color=PLAIN)
        l0 = label(rf"no baseline: \ ${v0:.1f}$", font_size=22, color=PLAIN).next_to(d0, LEFT, buff=0.15).shift(UP * 0.25)
        ds = Dot(ax.c2p(bstar, vstar), radius=0.08, color=BASE)
        ls = label(rf"best baseline, \ $b = {bstar:.2f}$: \ ${vstar:.1f}$", font_size=22, color=BASE).next_to(ds, UP, buff=0.2)
        rp = DashedLine(ax.c2p(-2, vrep), ax.c2p(6, vrep), color=REP, stroke_width=3)
        rl = label(rf"reparameterized, \ $x = \mu + \varepsilon$: \ ${vrep:.1f}$", font_size=22, color=REP).next_to(ax.c2p(6, vrep), UP, buff=0.12).align_to(ax.c2p(6, 0), RIGHT)
        rep = cmath(r"\nabla_\mu \mathbb{E}[f(\mu + \varepsilon)]", "=", r"\mathbb{E}[f'(\mu + \varepsilon)]", font_size=30,
                    colors={r"\mathbb{E}[f'(\mu + \varepsilon)]": REP}).move_to([4.4, 1.6, 0])
        repn = label(r"needs $f$ to have a slope \\ (Kingma \& Welling, 2013)", font_size=22, color=GREY_A).next_to(rep, DOWN, buff=0.15)
        n_ = int(d["N"])
        with self.voiceover(
            "The catch is noise. Take a case we can check: the gradient of the average of x squared, for a bell "
            f"centred at one; the answer is two. <bookmark mark='a'/> The estimator gets it right on average, "
            f"{mean_sf:.3f} over {n_:,} samples, but one sample's estimate has a variance of {v0:.0f}. "
            "<bookmark mark='b'/> A baseline cuts that: the best one here, near the average of f, brings it to "
            f"{vstar:.0f}. <bookmark mark='c'/> When f does have a slope, there is a better way: write the sample as "
            f"mu plus noise and differentiate through it, the reparameterization trick, with variance {vrep:.0f}. "
            "Variational autoencoders train that way, in part twenty; rewards and judges need the score function."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(d0), FadeIn(l0))
            vo.wait_until("b")
            self.play(FadeIn(ds), FadeIn(ls))
            vo.wait_until("c")
            self.play(Create(rp), FadeIn(rl), Write(rep), FadeIn(repn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def es(self):
        d = load("scorefn")
        PP, PB = np.asarray(d["paths_plain"]), np.asarray(d["paths_base"])
        sig, pop, lr, steps = float(d["sig"]), int(d["pop"]), float(d["lr"]), int(d["steps"])
        gp, gb, gm, g2 = (float(d[k]) for k in ("gerr_plain", "gerr_base", "gerr_mirror", "gnorm2"))
        dp, db = int(d["div_plain"]), int(d["div_base"])

        def panel(P, col, title, x0):
            ax = Axes(x_range=[-1.6, 1.6, 1], y_range=[-0.6, 2.2, 1], x_length=5.6, y_length=4.4, tips=False,
                      axis_config={"stroke_width": 0}).move_to([x0, -0.7, 0])
            cont = contour_lines(ax, valley, (-1.6, 1.6), (-0.6, 2.2), [0.05, 0.3, 1, 3, 8], n=(80, 70), stroke_width=1.4)
            cont.set_stroke(opacity=0.6)
            fr = SurroundingRectangle(ax, buff=0, color=GREY_D, stroke_width=1.5)
            star = Star(n=5, outer_radius=0.13, color=C.BITS, fill_opacity=1).move_to(ax.c2p(1, 1))
            t = label(title, font_size=24, color=col).next_to(fr, UP, buff=0.12)
            return ax, VGroup(fr, cont, star, t)

        a1, g1 = panel(PP, PLAIN, r"plain", -3.4)
        a2, g2_ = panel(PB, BASE, r"with a baseline", 3.4)
        tr = ValueTracker(0)

        def paths(ax, P, col):
            def make():
                k = max(int(tr.get_value()), 1)
                g = VGroup()
                for run in P:
                    pts = [ax.c2p(*np.clip(p, [-1.6, -0.6], [1.6, 2.2])) for p in run[:k + 1]]
                    g.add(VMobject(color=col, stroke_width=2, stroke_opacity=0.75).set_points_as_corners(pts))
                    g.add(Dot(pts[-1], radius=0.04, color=col))
                return g
            return always_redraw(make)

        pa, pb = paths(a1, PP, PLAIN), paths(a2, PB, BASE)
        head = cmath(r"\nabla \mathbb{E}_\varepsilon\big[f(\theta + \sigma\varepsilon)\big]", "=",
                     r"\tfrac{1}{\sigma}\, \mathbb{E}\big[f(\theta + \sigma\varepsilon)\,\varepsilon\big]", font_size=34)
        head.to_edge(UP, buff=0.3)
        hn = label(rf"evolution strategies: \ ${pop}$ random probes a step, \ $8$ runs each, \ same step size", font_size=22,
                   color=GREY_A).next_to(head, DOWN, buff=0.12)
        res = VGroup(label(rf"error of one gradient estimate: \ ${gp:.0f}$ \ (the gradient's own size: ${g2:.0f}$)",
                           font_size=22, color=PLAIN),
                     label(rf"with the baseline: \ ${gb:.0f}$; \ mirrored probes: \ ${gm:.0f}$", font_size=22, color=BASE))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.2)
        verdict = (f"Without the baseline, {dp} of the 8 runs blow up and leave the picture; with it, "
                   f"{'none do' if db == 0 else f'{db} do'}." if dp > db else
                   f"Here both reach the valley floor: {dp} plain runs and {db} with a baseline blow up.")
        with self.voiceover(
            "The same estimator trains models with no gradient at all. Smooth f by adding noise to the parameters, "
            "and its gradient is an average of f at random probes, times the probe: evolution strategies, used by "
            "Salimans and colleagues at OpenAI in 2017 to train simulated robots and Atari players. <bookmark mark='a'/> Here it "
            "descends a curved valley, sixteen probes a step. <bookmark mark='b'/> The baseline matters: measured at "
            f"the start, the squared error of one gradient estimate is {gp:.0f} without it and {gb:.0f} with it, "
            f"when the gradient itself is only {g2:.0f} in size. <bookmark mark='c'/> {verdict} Reinforcement "
            "learning's policy gradients are this estimator, with baselines, in part twenty-six."
        ) as vo:
            self.play(Write(head), FadeIn(hn))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2_))
            self.add(pa, pb)
            self.play(tr.animate.set_value(len(PP[0]) // 3), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(tr.animate.set_value(len(PP[0]) - 1), run_time=4.0, rate_func=linear)
        pa.clear_updaters()
        pb.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
