from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import PART, curve, load, predict_card, takeaway_card

ETA_COLORS = [C.TRUE_P, C.MODEL_Q]


class EdgeOfStability(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.predict()
        self.edge()
        self.why_()
        self.adam()
        self.takeaway()

    def card(self):
        c = chapter_card(5, r"The edge of stability", r"How big can a step be?", part=PART)
        with self.voiceover("Chapter five. The edge of stability."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def rule(self):
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 3, 1], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([-3.4, -0.6, 0])
        lam = 1.5
        par = ax.plot(lambda x: 0.5 * lam * x * x, x_range=[-2, 2], color=GREY_B, stroke_width=3)

        def bounces(eta, x0=1.6, n=7):
            xs = [x0]
            for _ in range(n):
                xs.append(xs[-1] * (1 - eta * lam))
            pts = []
            for a, b in zip(xs, xs[1:]):
                pts += [ax.c2p(a, 0.5 * lam * a * a), ax.c2p(b, 0.5 * lam * b * b)]
            return VMobject(stroke_width=3).set_points_as_corners(pts)

        good = bounces(1.0).set_color(C.INTERVAL)
        bad = bounces(1.42, x0=1.0, n=6).set_color(C.SURPRISE)
        colors = {r"\lambda": C.BITS, r"\eta": C.MODEL_Q}
        f = cmath(r"x", r"\;\to\;", r"(1 - ", r"\eta", r"\,", r"\lambda", r")\,x", colors=colors, font_size=40)
        f.move_to([3.2, 2.0, 0])
        fl = label(r"one step on a bowl of curvature $\lambda$", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cond = cmath(r"\text{stable only if}\;", r"\lambda", r"\;<\;", r"2 / \eta",
                     colors={r"\lambda": C.BITS, r"2 / \eta": C.MODEL_Q}, font_size=40).next_to(fl, DOWN, buff=0.6)
        notes = VGroup(label(r"$\eta\lambda < 2$: \ it settles", font_size=26, color=C.INTERVAL),
                       label(r"$\eta\lambda > 2$: \ every step overshoots further", font_size=26, color=C.SURPRISE))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cond, DOWN, buff=0.5).set_x(3.2)
        with self.voiceover(
            "Chapter one ended with a valley that threw the walker out. Here is the reason, on the simplest possible "
            "loss: a bowl with curvature lambda, and a step of size eta. Each step multiplies the distance from the "
            "bottom by one minus eta times lambda. <bookmark mark='a'/> If that's between minus one and one, the "
            "steps shrink and settle. <bookmark mark='b'/> If eta times lambda is more than two, each step "
            "overshoots further than the last, and it blows up. So gradient descent can only be stable where the "
            "curvature is below two over eta."
        ) as vo:
            self.play(Create(ax), Create(par), Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(Create(good), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(bad), FadeIn(notes[1]), run_time=2.0)
            self.play(Write(cond))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        pc = predict_card(r"Train a network by full-batch gradient descent at a fixed step $\eta$. \ The sharpness, \ "
                          r"the curvature $\lambda_{\max}$ along the steepest direction, \ starts small. \ What does it "
                          r"do as training goes on?")
        sharp = gloss(r"sharpness", r"how tightly the valley curves \\ along its steepest direction: \\ the Hessian's "
                      r"largest eigenvalue", corner=DR, width=4.4, color=C.BITS)
        pc.scale(0.8).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=6.0, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.4, -1.4, 0])
        edge_ = DashedLine(ax.c2p(0, 2), ax.c2p(4, 2), color=C.MODEL_Q, stroke_width=2)
        el = MathTex(r"2/\eta", font_size=30, color=C.MODEL_Q).next_to(edge_, RIGHT, buff=0.1)
        start = Dot(ax.c2p(0.05, 0.4), radius=0.07, color=C.TRUE_P)
        qm = MathTex(r"?", font_size=72, color=C.TRUE_P).move_to(ax.c2p(2.2, 1.2))
        axl = VGroup(label(r"sharpness $\lambda_{\max}$", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT),
                     label(r"training steps", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.1))
        with self.voiceover(
            "The classical advice follows: measure the sharpness, the largest curvature, the Hessian's top "
            "eigenvalue, and choose a step below two over it. But training changes the landscape it walks on. "
            "Pause and predict: on a real network, at a fixed step, what does the sharpness do as training goes on?"
        ):
            self.play(FadeIn(pc), Create(ax), FadeIn(axl), Create(edge_), FadeIn(el), FadeIn(start))
            self.play(FadeIn(sharp, shift=UP * 0.2), FadeIn(qm, scale=0.5))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        e = load("eos")
        etas = [float(x) for x in e["etas"]]
        top = max(2 / min(etas) * 1.4, max(float(np.asarray(e[f"curve{eta}"])[:, 2].max()) for eta in etas) * 1.1)
        ax = Axes(x_range=[0, 4000, 1000], y_range=[0, top, 10], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        yl = VGroup(*[MathTex(f"{v:.0f}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(0, top, 20)])
        xl = label(r"steps of full-batch gradient descent", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"sharpness: \ the Hessian's largest eigenvalue", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15)
        yn.align_to(ax, LEFT)
        groups = VGroup()
        for eta, col in zip(etas, ETA_COLORS):
            c = np.asarray(e[f"curve{eta}"])
            line = DashedLine(ax.c2p(0, 2 / eta), ax.c2p(4000, 2 / eta), color=col, stroke_width=2)
            ll = label(rf"$2/\eta = {2 / eta:.0f}$", font_size=24, color=col).next_to(line, UP, buff=0.05).align_to(line, RIGHT)
            groups.add(VGroup(curve(ax, c[:, 0], c[:, 2], col, 3.5), line, ll))
        names = VGroup(*[label(rf"$\eta = {eta}$", font_size=26, color=col) for eta, col in zip(etas, ETA_COLORS)])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.8, 0])
        med = {eta: float(e[f"late_median{eta}"]) for eta in etas}
        res = VGroup(*[label(rf"second half: \ median ${med[eta]:.1f}$", font_size=22, color=col)
                       for eta, col in zip(etas, ETA_COLORS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        res.next_to(names, DOWN, buff=0.35).align_to(names, LEFT)
        how = label(r"Part 9's spirals; \ power iteration \\ on Hessian-vector products", font_size=20, color=GREY_A)
        how.next_to(res, DOWN, buff=0.3).align_to(names, LEFT)
        col_ = VGroup(names, res, how)
        if col_.get_right()[0] > 6.8:
            col_.shift(LEFT * (col_.get_right()[0] - 6.8))
        cite_ = cite(r"J.~Cohen, S.~Kaur, Y.~Li, J.~Z.~Kolter \& A.~Talwalkar (2021)", corner=DR)
        lc = {eta: np.asarray(e[f"curve{eta}"]) for eta in etas}
        lmin = float(np.floor(min(np.log10(c[:, 1].min()) for c in lc.values()) * 2) / 2)
        lmax = float(np.ceil(max(np.log10(c[:, 1].max()) for c in lc.values()) * 2) / 2)
        lax = CornerAxes(x_range=[0, 4000, 1000], y_range=[lmin, lmax, 0.5], x_length=3.0, y_length=1.3, tips=False,
                         axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.9, -2.55, 0])
        lax_l = label(r"the loss, \ meanwhile \ (log scale)", font_size=18, color=GREY_A).next_to(lax, UP, buff=0.1)
        VGroup(lax, lax_l).shift(DOWN * max(0.0, lax_l.get_top()[1] - (how.get_bottom()[1] - 0.2)))
        t = ValueTracker(0)

        def upto(axes_, eta, col, k, f=lambda v: v, sw=3.5):
            c = lc[eta]
            n = max(2, int(np.searchsorted(c[:, 0], t.get_value(), side="right")))
            return VMobject(color=col, stroke_width=sw).set_points_as_corners([axes_.c2p(x, f(y)) for x, y in zip(c[:n, 0], c[:n, k])])

        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=WHITE).next_to(ax.get_corner(UR), UL, buff=0.1))
        e0, e1 = etas
        at_edge = all(abs(med[eta] - 2 / eta) < 0.15 * 2 / eta for eta in etas)
        fe = int(e[f"first_edge{e0}"])
        said1 = (f"and climbs, until it reaches two over eta, around step {fe:,}, and then it stays there, hovering at "
            "the edge, while the loss keeps going down, unevenly. "
            if at_edge and fe > 0 else
            "and climbs, towards two over eta, while the loss keeps going down. ")
        said2 = (f"the network settles at half the sharpness: a median of {med[e1]:.1f}, against two over eta of "
            f"{2 / e1:.0f}. "
            if at_edge else
            f"its sharpness settles near {med[e1]:.1f}, with two over eta at {2 / e1:.0f}. ")
        with self.voiceover(
            "Here is the answer, measured: the spirals from part nine, trained with the full gradient at two step "
            "sizes, the sharpness measured every forty steps by power iteration. <bookmark mark='a'/> It climbs, "
            + said1
            + "<bookmark mark='b'/> Double the step size, and "
            + said2
            + "Training doesn't stay away from the edge of stability: it goes there and lives on it. Jeremy Cohen and "
            "colleagues found this in 2021, and nobody had expected it."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(cite_), FadeIn(how))
            self.play(Create(lax), FadeIn(lax_l), run_time=0.8)
            vo.wait_until("a")
            self.add(cnt)
            for k, (eta, col) in enumerate(zip(etas, ETA_COLORS)):
                if k:
                    vo.wait_until("b")
                t.set_value(0)
                live = [always_redraw(lambda eta=eta, col=col: upto(ax, eta, col, 2)),
                        always_redraw(lambda eta=eta, col=col: upto(lax, eta, col, 1, lambda v: float(np.log10(v)), 2.5))]
                self.add(*live)
                self.play(t.animate.set_value(4000), Create(groups[k][1]), FadeIn(groups[k][2]), FadeIn(names[k]),
                          run_time=5.0, rate_func=linear)
                for m_ in live:
                    m_.clear_updaters()
                self.play(FadeIn(res[k]))
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_(self):
        steps = VGroup(
            label(r"1. \ progressive sharpening: \ while $\lambda_{\max} < 2/\eta$, \ training makes the valley steeper",
                  font_size=24, color=WHITE),
            label(r"2. \ past $2/\eta$, \ the walker starts to bounce along the steepest direction, \ growing each step",
                  font_size=24, color=C.SURPRISE),
            label(r"3. \ the bounce moves it to where that direction curves less: \ the sharpness falls back",
                  font_size=24, color=C.INTERVAL),
            label(r"4. \ the two balance at $\lambda_{\max} \approx 2/\eta$: \ \textit{self-stabilization}", font_size=24,
                  color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.1, 0])
        keep_in_frame(steps)
        # schematic: a ball bouncing across a valley whose walls flatten as it bounces
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 2.2, 1], x_length=5.0, y_length=2.2, tips=False,
                  axis_config={"stroke_width": 0}).move_to([0, -2.3, 0])
        k_ = ValueTracker(2.4)
        bowl = always_redraw(lambda: ax.plot(lambda x: 0.5 * k_.get_value() * x * x, x_range=[-1.3, 1.3], color=GREY_A,
                                             stroke_width=3))
        dot = Dot(ax.c2p(0.6, 0.5 * 2.4 * 0.36), radius=0.09, color=C.SURPRISE)
        sch = note(r"schematic").next_to(ax, RIGHT, buff=0.2)
        cite_ = cite(r"A.~Damian, E.~Nichani \& J.~D.~Lee, \textit{Self-Stabilization} (2022)", corner=DR)
        with self.voiceover(
            "Why? <bookmark mark='a'/> While the sharpness is below two over eta, training tends to make the valley "
            "steeper: progressive sharpening. <bookmark mark='b'/> Once it passes the edge, the walker starts to "
            "bounce along the steepest direction, further each step. <bookmark mark='c'/> But the bounce carries it "
            "to where that direction curves less, and the sharpness falls back. <bookmark mark='d'/> Alex Damian, "
            "Eshaan Nichani and Jason Lee showed in 2022 that the two effects balance exactly at the edge. Gradient "
            "descent regulates its own curvature."
        ) as vo:
            self.play(FadeIn(sch), FadeIn(cite_), Create(ax))
            self.add(bowl)
            self.play(FadeIn(dot))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(steps[k], shift=RIGHT * 0.2))
                if k == 1:
                    for s_ in (1, -1, 1, -1):
                        self.play(dot.animate.move_to(ax.c2p(0.75 * s_, 0.5 * k_.get_value() * 0.56)), run_time=0.35)
                if k == 2:
                    self.play(k_.animate.set_value(1.6), dot.animate.move_to(ax.c2p(0.4, 0.5 * 1.6 * 0.16)), run_time=1.5)
            bowl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def adam(self):
        rows = VGroup(
            cmath(r"\text{gradient descent:}\quad", r"\lambda_{\max}(H)", r"\;\to\;", r"2/\eta", font_size=36),
            cmath(r"\text{heavy ball, momentum } \beta:\quad", r"\lambda_{\max}(H)", r"\;\to\;", r"(2 + 2\beta)/\eta", font_size=36),
            cmath(r"\text{Adam, } \beta_1 = 0.9:\quad", r"\lambda_{\max}(P^{-1} H)", r"\;\to\;", r"38/\eta", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.6)
        notes = VGroup(label(r"the curvature Adam sees: \ after its preconditioner $P$, \ $\frac{2(1 + \beta_1)}{1 - \beta_1}$",
                             font_size=22, color=C.MODEL_Q)).next_to(rows, DOWN, buff=0.5)
        cite_ = cite(r"J.~Cohen et al., \textit{Adaptive Gradient Methods at the Edge of Stability} (2022)", corner=DL)
        lnk = label(r"one reason for warmup: \ Chapter 13", font_size=24, color=C.BITS).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The edge moves with the optimizer. <bookmark mark='a'/> With momentum beta, a step can survive more "
            "curvature, up to two plus two beta over eta. <bookmark mark='b'/> Adam lives at an edge too: the "
            "curvature measured after its rescaling rises to thirty-eight over eta, the same rule for its momentum "
            "of zero point nine. Jeremy Cohen and colleagues, with researchers at Google, measured it in 2022. "
            "<bookmark mark='c'/> It is one reason a run needs to start with small steps, which comes back in "
            "Chapter 13."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(notes))
            vo.wait_until("c")
            self.play(FadeIn(lnk))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        e = load("eos")
        t = takeaway_card(r"Training finds the edge, \ and stays there",
                          r"At a fixed step $\eta$ the sharpness rises until $\lambda_{\max} \approx 2/\eta$ \ (measured "
                          rf"here: ${float(e['late_median0.05']):.1f}$ for $2/\eta = 40$). \ The step size sets the "
                          r"curvature, \ not the other way round.", r"Next: \ a step size for every weight")
        with self.voiceover(
            "So the step size doesn't have to fit the landscape: the landscape comes to fit the step size. Next, "
            "optimizers that give every weight a step size of its own."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
