from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import CONS, GRAD, HIST, PART, VALUE, expo, load, log_axes, mant

FIT = C.TRUE_P


class Implicit(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.check()
        self.train()

    def card(self):
        card = chapter_card(17, r"Differentiating through a fixed point", r"Can you backpropagate through an equation?",
                            part=PART)
        with self.voiceover("Chapter seventeen. Differentiating through an equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        col = {r"J": GRAD, r"a": GRAD}
        rows = [
            cmath(r"z^*", r"=", r"f(z^*, \theta)", font_size=40),
            cmath(r"\frac{dz^*}{d\theta}", r"=", r"J\,\frac{dz^*}{d\theta} + \frac{\partial f}{\partial \theta}", font_size=38,
                  colors=col),
            cmath(r"\frac{dz^*}{d\theta}", r"=", r"(I - J)^{-1}\, \frac{\partial f}{\partial \theta}", font_size=38, colors=col),
            cmath(r"\nabla_\theta \mathcal L", r"=", r"a^\top \frac{\partial f}{\partial \theta}, \quad (I - J)^\top a = "
                  r"\nabla_{z} \mathcal L", font_size=36, colors=col),
        ]
        whys = [why(r"a fixed point: \ the layer's output, fed back in", font_size=22),
                why(r"differentiate both sides; \ $J = \partial f / \partial z$", font_size=22),
                why(r"if $I - J$ is invertible: \\ the implicit function theorem", font_size=22),
                why(r"a VJP: \ one linear solve, \ no unrolling", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.5, edge=6.9)
        head = label(r"a layer defined by an equation", font_size=26, color=GREY_A).to_corner(UL, buff=0.3)
        with self.voiceover(
            "Some layers aren't a fixed list of steps. A deep equilibrium layer feeds its output back into itself until "
            "nothing changes: its output is the fixed point z star, which satisfies z star equals f of z star and "
            "theta. How do you backpropagate through that? <bookmark mark='a'/> Differentiate both sides of the "
            "equation. <bookmark mark='b'/> Collect the terms: the derivative of the solution is the inverse of I "
            "minus J, times the direct derivative, as long as that inverse exists, which is the implicit function "
            "theorem. <bookmark mark='c'/> For a loss, run it as a vector-Jacobian product: one linear solve at the "
            "fixed point, however many iterations it took to get there, and nothing stored along the way."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("deq")
        Ks, errs = np.asarray(d["Ks"]), np.asarray(d["errs"])
        g = log_axes((0, 60), (-14, 0), x_length=6.6, y_length=4.2, xlabel=r"unrolled steps $K$",
                     ylabel=r"unrolled gradient against implicit: \ relative gap", center=[-2.6, -0.5, 0], ystep=2,
                     xticks=[])
        for k in (0, 20, 40, 60):
            g.add(MathTex(str(k), font_size=20, color=GREY_B).next_to(g.ax.c2p(k, -14), DOWN, buff=0.12))
        ok = errs > 0
        c = curve(g.ax, Ks[ok], np.clip(np.log10(errs[ok]), -14, 0), GRAD, 3.5)
        rho = float(d["rho"])
        pred = curve(g.ax, Ks, np.clip(Ks * math.log10(rho), -14, 0), GREY_B, 1.8)
        info = VGroup(
            label(r"$z = \tanh(W z + U x + b)$, \ $8$ numbers \ (computed)", font_size=22, color=GREY_A),
            label(rf"fixed point reached in ${int(d['iters'])}$ iterations", font_size=22, color=GREY_A),
            label(rf"spectral radius of $J$: \ ${rho:.3f}$", font_size=22, color=GREY_B),
            label(rf"measured shrink per step: \ ${d['rate']:.3f}$", font_size=22, color=GRAD),
            label(r"memory: \ unrolled keeps $K$ states; \ implicit keeps one", font_size=22, color=CONS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 0.6, 0])
        leg = label(r"grey: \ $\rho(J)^K$", font_size=20, color=GREY_B).next_to(g, DOWN, buff=0.05).align_to(g, RIGHT)
        floor = float(errs[-10:].min())
        close = abs(d["rate"] - rho) < 0.15
        verdict = ("close to the spectral radius of J, as the theory says it should be" if close else
                   "slower than the spectral radius alone would suggest")
        with self.voiceover(
            "Check it on a tiny equilibrium layer with eight numbers. <bookmark mark='a'/> The usual alternative is to "
            "unroll: run K iterations and backpropagate through all of them with our library. As K grows, that "
            "gradient closes in on the implicit one geometrically, <bookmark mark='b'/> shrinking by "
            f"{d['rate']:.3f} each step, {verdict}, until it reaches {mant(floor)} times ten to the minus "
            f"{expo(floor)}, the accuracy of the fixed point itself. <bookmark mark='c'/> Unrolling stores every "
            "iteration; the implicit gradient needs only the answer."
        ) as vo:
            self.play(FadeIn(g), FadeIn(info[0]), FadeIn(info[1]))
            vo.wait_until("a")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(pred), FadeIn(leg), FadeIn(info[2]), FadeIn(info[3]))
            vo.wait_until("c")
            self.play(FadeIn(info[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        d = load("deq")
        xs, ys, gx = np.asarray(d["xs"]), np.asarray(d["ys"]), np.asarray(d["gx"])
        fits = np.asarray(d["fits"])
        keep = [int(k) for k in d["keep"]]
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-1.6, 1.6, 1], x_length=6.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.6, 0])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(xs, ys)])
        lines = [curve(ax, gx, np.clip(f, -1.6, 1.6), FIT, 3.5) for f in fits]
        cv = np.asarray(d["curve"])
        g2 = log_axes((0, math.log10(d["steps"])), (-6, 0), x_length=4.4, y_length=2.4, xlabel=r"step",
                      ylabel=r"loss", center=[3.8, 1.2, 0], ystep=2, font_size=16)
        ok = cv[:, 0] > 0
        lc = curve(g2.ax, np.log10(cv[ok, 0]), np.clip(np.log10(cv[ok, 1]), -6, 0), C.LOSS, 2.5)
        it = np.asarray(d["iters_curve"])
        info = VGroup(
            label(rf"a DEQ with ${int(d['d'])}$ numbers, \ trained only with implicit gradients", font_size=21, color=GREY_A),
            label(rf"loss: \ ${d['first_loss']:.3f} \to {sci(d['final_loss'], 1)}$", font_size=22, color=C.LOSS),
            label(rf"iterations to the fixed point: \ ${it[0, 1]:.0f} \to {it[-1, 1]:.0f}$", font_size=22, color=GREY_A),
            label(rf"at the end, against $200$ unrolled steps: \ ${sci(max(d['end_diff'], 1e-16), 0)}$", font_size=22,
                  color=GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.8, -1.6, 0])
        step_l = [label(rf"step ${k}$", font_size=22, color=FIT).next_to(ax, UP, buff=0.1).align_to(ax, LEFT) for k in keep]
        uses = label(r"also: \ meta-learning (iMAML, 2019), \ optimization layers (OptNet, 2017), \ hyperparameters",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        cite_ = cite(r"S.~Bai, J.~Z.~Kolter \& V.~Koltun, \textit{Deep Equilibrium Models} (2019)", corner=UR)
        more = it[-1, 1] > it[0, 1]
        it_v = (f"and the equilibrium takes longer to reach as it learns, {it[0, 1]:.0f} iterations at first and "
                f"{it[-1, 1]:.0f} at the end" if more else
                f"and the equilibrium takes {it[0, 1]:.0f} iterations at first and {it[-1, 1]:.0f} at the end")
        with self.voiceover(
            f"And it trains. A deep equilibrium model with {int(d['d'])} numbers learns to fit this curve, with every "
            "gradient computed implicitly and its feedback matrix kept a contraction. <bookmark mark='a'/> The fit "
            f"sharpens as the loss falls from {d['first_loss']:.3f} to about {mant(d['final_loss'])} times ten to the "
            f"minus {expo(d['final_loss'])}, "
            f"{it_v}. <bookmark mark='b'/> Shaojie Bai, Zico Kolter and Vladlen Koltun proposed such models in 2019. "
            "The same trick differentiates through an inner optimization, in meta-learning, or through a solver used "
            "as a layer: wherever the answer is defined by an equation rather than a recipe."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), Create(lines[0]), FadeIn(step_l[0]), FadeIn(g2), Create(lc),
                      FadeIn(info[0]), FadeIn(cite_))
            vo.wait_until("a")
            for k in range(1, len(keep)):
                self.play(Transform(lines[0], lines[k]), Transform(step_l[0], step_l[k]), run_time=0.9)
            self.play(FadeIn(info[1]), FadeIn(info[2]), FadeIn(info[3]))
            vo.wait_until("b")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
