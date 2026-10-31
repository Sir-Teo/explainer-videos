from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import CONS, GRAD, HIST, PART, VALUE, lag_f, load


def bars(values, colors, width=4.4, height=2.0, labels=None, fmt="{:.3f}", font_size=18, vmax=None):
    n = len(values)
    vmax = vmax or max(values)
    bw = width / n * 0.7
    g = VGroup()
    base = Line([-width / 2 - 0.1, 0, 0], [width / 2 + 0.1, 0, 0], color=GREY_C, stroke_width=1.5)
    g.add(base)
    for i, v in enumerate(values):
        x = -width / 2 + (i + 0.5) * width / n
        h = max(height * float(v) / vmax, 0.01)
        c = colors[i] if isinstance(colors, (list, tuple)) else colors
        r = Rectangle(width=bw, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x, h / 2, 0])
        g.add(r, MathTex(fmt.format(v), font_size=font_size, color=c).next_to(r, UP, buff=0.06))
        if labels is not None:
            g.add(MathTex(labels[i], font_size=font_size + 2, color=GREY_B).next_to([x, 0, 0], DOWN, buff=0.1))
    return g


class Lagrange(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.derive()
        self.maxent()
        self.rl()

    def card(self):
        card = chapter_card(15, r"Constraints: Lagrange multipliers", r"How do you go downhill on a fence?", part=PART)
        with self.voiceover("Chapter fifteen. Optimizing under constraints."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def picture(self):
        d = load("lagrange")
        A, Cc = np.asarray(d["A"]), np.asarray(d["C"])
        ax = Axes(x_range=[-1.6, 2.6, 1], y_range=[-1.5, 1.9, 1], x_length=6.6, y_length=5.35, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-2.9, -0.5, 0])
        cont = contour_lines(ax, lag_f, (-1.6, 2.6), (-1.5, 1.9), [0.05 * 2 ** k for k in range(8)], n=(140, 110),
                             colors=("#2E6FB0", "#9CC3EA"))
        xu = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        yu = ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]
        circ = Ellipse(width=2 * xu, height=2 * yu, color=CONS, stroke_width=4).move_to(ax.c2p(0, 0))
        cl = MathTex(r"g(x) = \|x\|^2 - 1 = 0", font_size=26, color=CONS).move_to([2.5, 0.0, 0])
        th = ValueTracker(2.6)
        s = 0.32

        def arrows():
            t = th.get_value()
            p = np.array([math.cos(t), math.sin(t)])
            gf = 2 * A * (p - Cc)
            gg = 2 * p
            P = ax.c2p(*p)
            u = ax.c2p(*(p + s * gf)) - P
            w = ax.c2p(*(p + s * gg)) - P
            return VGroup(Arrow(P, P + u, buff=0, color=GRAD, stroke_width=5, max_tip_length_to_length_ratio=0.2),
                          Arrow(P, P + w, buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.2),
                          Dot(P, radius=0.07, color=WHITE))

        arr = always_redraw(arrows)
        th_ = np.asarray(d["th"])
        tang = np.asarray(d["tang"])
        rd = DecimalNumber(0, num_decimal_places=3, include_sign=True, font_size=34, color=GRAD)
        rd.add_updater(lambda m: m.set_value(float(np.interp(th.get_value(), th_, tang))))
        rd.update()
        read = VGroup(label(r"$\nabla f$ along the circle:", font_size=26, color=GREY_A), rd).arrange(RIGHT, buff=0.2)
        read.move_to([3.9, 2.4, 0])
        key = VGroup(label(r"$\nabla f$", font_size=24, color=GRAD), label(r"$\nabla g$", font_size=24, color=WHITE),
                     label(r"contours of $f$", font_size=24, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        key.move_to([2.4, 1.0, 0])
        hist = history_card(1788, r"Joseph-Louis Lagrange, \ \textit{M\'ecanique analytique}",
                            r"constraints handled by multipliers, \ for mechanics", width=5.4, font_size=19,
                            color=HIST).to_corner(DR, buff=0.3)
        t_star = float(d["t_star"])
        with self.voiceover(
            "Often the numbers aren't free: probabilities must add to one, a budget must be kept. Here, minimize f, "
            "whose contours are these ellipses, but only on the circle. <bookmark mark='a'/> Walk along the circle "
            "and watch two arrows: the gradient of f, and the gradient of the constraint, which points straight out "
            "of the circle. <bookmark mark='b'/> Wherever the gradient of f has a part along the circle, you can slide "
            "against that part and go lower. <bookmark mark='c'/> So at the constrained minimum that part is zero: the two "
            "gradients are parallel. <bookmark mark='d'/> Joseph-Louis Lagrange turned that picture into a method in "
            "1788, in his Mécanique analytique."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.08), run_time=1.5)
            self.play(Create(circ), FadeIn(cl))
            vo.wait_until("a")
            self.add(arr)
            self.play(FadeIn(key), FadeIn(read))
            vo.wait_until("b")
            self.play(th.animate.set_value(1.3), run_time=2.5)
            vo.wait_until("c")
            self.play(th.animate.set_value(t_star), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(hist, shift=UP * 0.2))
        arr.clear_updaters()
        rd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        d = load("lagrange")
        assert d["resid"] < 1e-6
        col = {r"\lambda": CONS, r"\nabla f": GRAD}
        rows = [
            cmath(r"\nabla f(x^*)", r"=", r"-\lambda\, \nabla g(x^*)", font_size=40, colors=col),
            cmath(r"\mathcal{L}(x, \lambda)", r"=", r"f(x) + \lambda\, g(x)", font_size=40, colors=col),
            cmath(r"\nabla_x \mathcal{L} = 0", r",", r"\;\; \partial_\lambda \mathcal{L} = g(x) = 0", font_size=40),
        ]
        whys = [why(r"regular constraint: \ $\nabla g \ne 0$"), why(r"the Lagrangian; \ $\lambda$: the multiplier"),
                why(r"necessary stationarity, \\ not sufficient for a minimum")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.4, buff=0.6, edge=6.9)
        x = np.asarray(d["x_star"])
        res = VGroup(
            label(rf"computed: \ $x^* = ({x[0]:.3f}, {x[1]:.3f})$, \ $\lambda = {d['lam']:.3f}$, \ "
                  rf"$\|\nabla f + \lambda \nabla g\| = {sci(d['resid'], 0)}$", font_size=24, color=WHITE),
            label(r"$\lambda$ is a price: \ $d f^* / dc = -\lambda$ \ when the constraint is $\|x\|^2 = c$", font_size=24,
                  color=CONS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Write it down: at the constrained minimum, the gradient of f is a multiple of the constraint's gradient, "
            "minus lambda times it. <bookmark mark='a'/> Lagrange's device folds the constraint into a single "
            "function, the Lagrangian, f plus lambda times g. <bookmark mark='b'/> Stationarity in x and lambda gives "
            "necessary conditions for a regular constrained optimum, not a guarantee of a minimum. The derivative "
            f"in lambda gives back the constraint. <bookmark mark='c'/> For the circle, the multiplier comes out at {d['lam']:.3f}. It is a "
            "price: how fast the best value would fall if the constraint were loosened a little."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maxent(self):
        d = load("lagrange")
        p = np.asarray(d["p_dice"])
        assert d["dice_diff"] < 1e-4
        rows = [
            cmath(r"\max_p\; -\textstyle\sum_i p_i \log p_i", r"\;\text{s.t.}\;",
                  r"\textstyle\sum_i p_i = 1, \;\; \sum_i i\, p_i = 4.5", font_size=32),
            cmath(r"-\log p_i - 1 - \alpha + \beta\, i", r"=", r"0", font_size=34, colors={r"\beta": CONS}),
            cmath(r"p_i", r"=", r"\frac{e^{\beta i}}{\sum_j e^{\beta j}}", font_size=36, colors={r"p_i": C.PROB}),
        ]
        whys = [why(r"the least committal die whose average is $4.5$", font_size=22),
                why(r"$\partial \mathcal L / \partial p_i = 0$, \ multipliers $\alpha$ and $\beta$", font_size=22),
                why(r"a softmax: \ the Boltzmann distribution", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.6, buff=0.5, edge=6.9)
        b = bars(list(p), C.PROB, width=4.6, height=1.7, labels=[str(i) for i in range(1, 7)]).move_to([-3.6, -2.0, 0])
        bl = label(rf"computed: \ $\beta = {d['beta']:.3f}$; \ a general solver agrees to ${sci(max(d['dice_diff'], 1e-12), 0)}$",
                   font_size=22, color=GREY_A).move_to([3.2, -1.4, 0])
        jl = label(r"E.~T.~Jaynes (1957): \ maximum entropy \\ as a principle of inference", font_size=22,
                   color=GREY_B).move_to([3.2, -2.4, 0])
        with self.voiceover(
            "A famous constrained problem: a die whose average roll is 4.5, not 3.5. Which probabilities assume the "
            "least beyond that? The ones with the most entropy. <bookmark mark='a'/> Set the Lagrangian's derivative "
            "to zero, with one multiplier for each constraint, <bookmark mark='b'/> and the answer is a softmax: each "
            "face's probability is e to the beta times the face, normalized. <bookmark mark='c'/> Computed, beta is "
            f"{d['beta']:.3f}, and a general-purpose solver lands on the same six numbers. Edwin Jaynes made this a "
            "principle of inference in 1957. It's where the softmax comes from: it is the maximum-entropy "
            "distribution with a fixed average score, and its temperature is a Lagrange multiplier."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(bl))
            self.play(FadeIn(jl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rl(self):
        d = load("lagrange")
        assert d["rl_diff"] < 1e-4
        pref, ps, rew = np.asarray(d["pref"]), np.asarray(d["pi_star"]), np.asarray(d["rew"])
        eq = cmath(r"\max_\pi\; \mathbb E_\pi[r] - \beta\, \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}})", r"\;\Rightarrow\;",
                   r"\pi^*(a) = \frac{\pi_{\text{ref}}(a)\, e^{r(a)/\beta}}{Z}", font_size=38).to_edge(UP, buff=0.5)
        sub = label(r"the same Lagrangian, \ with $\textstyle\sum_a \pi(a) = 1$", font_size=24, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        vmax = max(pref.max(), ps.max())
        b1 = bars(list(pref), GREY_B, width=5.0, height=2.6, labels=[f"a_{i + 1}" for i in range(6)], vmax=vmax).move_to([-3.4, -1.3, 0])
        b2 = bars(list(ps), C.REWARD, width=5.0, height=2.6, labels=[f"a_{i + 1}" for i in range(6)], vmax=vmax).move_to([3.4, -1.3, 0])
        l1 = label(r"$\pi_{\text{ref}}$", font_size=26, color=GREY_B).next_to(b1, UP, buff=0.3)
        l2 = label(rf"$\pi^*$, \ $\beta = {d['kl_beta']:g}$ \ (computed; \ solver agrees to ${sci(max(d['rl_diff'], 1e-12), 0)}$)",
                   font_size=22, color=C.REWARD).next_to(b2, UP, buff=0.3)
        with self.voiceover(
            "The same algebra gives reinforcement learning one of its closed forms. Maximize the expected reward, "
            "minus beta times the KL divergence from a reference policy. <bookmark mark='a'/> With the constraint that "
            "the probabilities add to one, the best policy is the reference, reweighted by e to the reward over beta. "
            "<bookmark mark='b'/> Here for six actions, computed and checked against a solver. Part 27's direct "
            "preference optimization starts from this formula."
        ) as vo:
            self.play(Write(eq), FadeIn(b1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(b2))
            vo.wait_until("b")
            self.play(FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()
