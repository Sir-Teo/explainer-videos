from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import CONS, GRAD, HIST, PART, VALUE, expo, load, log_axes, mant

FIT = C.TRUE_P


def gradient_rate_comparison(rate, rho):
    if not (math.isfinite(rate) and math.isfinite(rho) and 0 < rho < 1 and rate > 0):
        return "a finite geometric-rate comparison is unavailable"
    if abs(rate - rho) < 0.15:
        return "within 0.15 of the spectral radius in this measured fit"
    if rate > rho:
        return "slower than the spectral-radius reference in this measured fit"
    return "faster than the spectral-radius reference in this measured fit"


def fixed_point_summary(record):
    if record["status"] == "converged":
        return f"the iteration met its residual tolerance after {int(record['iterations'])} updates"
    if record["status"] == "capped":
        return f"the iteration hit its cap of {int(record['cap'])} updates before meeting the residual tolerance"
    return "the iteration has a non-finite result; a converged fixed point is unavailable"


def comparison_floor(values):
    finite = [float(v) for v in values if math.isfinite(float(v)) and float(v) >= 0]
    if not finite:
        return "a finite comparison floor is unavailable"
    floor = min(finite)
    if floor == 0:
        return "the final comparisons include a numerically zero gradient difference"
    return f"the smallest final gradient-comparison difference is {floor:.6g}"


def loss_comparison(first, final):
    if not (math.isfinite(first) and math.isfinite(final)):
        return "a finite first-to-final loss comparison is unavailable"
    if final < first:
        return "the final recorded loss is lower than the initial loss"
    if final > first:
        return "the final recorded loss is higher than the initial loss"
    return "the initial and final recorded losses are equal"


def metric_tex(value, digits=0):
    return sci(value, digits) if math.isfinite(value) else r"\mathrm{unavailable}"


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
                why(r"for $\mathcal L=\ell(z^*)$: \ one linear solve, \ no unrolling", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.5, edge=6.9)
        head = label(r"a layer defined by an equation", font_size=26, color=GREY_A).to_corner(UL, buff=0.3)
        box = VGroup(RoundedRectangle(width=1.9, height=0.9, corner_radius=0.12, color=GRAD, stroke_width=3),
                     MathTex(r"f(\,\cdot\,, \theta)", font_size=30))
        box[1].move_to(box[0])
        box.move_to([-1.6, -2.4, 0])
        zin = MathTex(r"z_k", font_size=32).next_to(box, LEFT, buff=1.2)
        zout = MathTex(r"z_{k+1}", font_size=32).next_to(box, RIGHT, buff=1.2)
        a1 = Arrow(zin.get_right(), box.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        a2 = Arrow(box.get_right(), zout.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        back = CurvedArrow(zout.get_bottom() + DOWN * 0.05, zin.get_bottom() + DOWN * 0.05, angle=-PI / 2.6, color=GREY_B)
        cap = label(r"iterate to a stated residual tolerance; \ a fixed point is $z^*$", font_size=22, color=GREY_A)
        cap.next_to(box, DOWN, buff=0.65)
        loop = VGroup(box, zin, zout, a1, a2, back, cap)
        tagl = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Some layers aren't a fixed list of steps. A deep equilibrium layer feeds its output back into itself until "
            "nothing changes: its output is the fixed point z star, which satisfies z star equals f of z star and "
            "theta. How do you backpropagate through that? <bookmark mark='a'/> Differentiate both sides of the "
            "equation. <bookmark mark='b'/> Collect the terms: the derivative of the solution is the inverse of I "
            "minus J, times the direct derivative, as long as that inverse exists, which is the implicit function "
            "theorem. <bookmark mark='c'/> For a loss, run it as a vector-Jacobian product: one linear solve at the "
            "fixed point, however many iterations it took to get there. No history of iteration states is needed, "
            "but parameters, local derivatives and the linear solver still take memory. If the loss also depends "
            "directly on theta, add that direct derivative."
        ) as vo:
            self.play(FadeIn(head), FadeIn(loop), FadeIn(tagl))
            self.play(ShowPassingFlash(back.copy().set_stroke(GRAD, width=6), time_width=0.5), run_time=1.2)
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
        ok = np.isfinite(errs) & (errs >= 0)
        high = max(0, math.ceil(math.log10(max(float(errs[ok].max()), 1e-14)))) if ok.any() else 0
        g = log_axes((0, 60), (-14, high), x_length=6.6, y_length=4.2, xlabel=r"unrolled steps $K$",
                     ylabel=r"unrolled gradient against implicit: \ relative gap", center=[-2.6, -0.5, 0], ystep=2,
                     xticks=[])
        for k in (0, 20, 40, 60):
            g.add(MathTex(str(k), font_size=20, color=GREY_B).next_to(g.ax.c2p(k, -14), DOWN, buff=0.12))
        c = VGroup()
        ids = np.flatnonzero(ok)
        for run in np.split(ids, np.flatnonzero(np.diff(ids) > 1) + 1):
            if len(run) > 1:
                c.add(curve(g.ax, Ks[run], np.log10(np.maximum(errs[run], 1e-14)), GRAD, 3.5))
        rho = float(d["rho"])
        pred = (curve(g.ax, Ks, np.maximum(Ks * math.log10(rho), -14), GREY_B, 1.8)
                if math.isfinite(rho) and 0 < rho < 1 else VGroup())
        initial = d["solves"]["initial"]
        solve_verdict = fixed_point_summary(initial)
        rho_note = (rf"$\rho(J)={rho:.3f}$; \ $\|W\|_2\le {d['contraction_caps']['initial']:g}$" if math.isfinite(rho) else
                    r"a finite spectral-radius measurement is unavailable")
        rate_note = (rf"fitted gradient-gap factor: \ ${d['rate']:.3f}$" if math.isfinite(d["rate"]) else
                     r"a finite fitted gradient-gap factor is unavailable")
        info = VGroup(
            wrapped_label(rf"$z = \tanh(W z + U x + b)$; \ state dimension ${d['initial_state_dimension']}$", 5.5, font_size=22, color=GREY_A),
            wrapped_label(solve_verdict, 5.5, font_size=21, color=GREY_A),
            wrapped_label(rho_note, 5.5, font_size=22, color=GREY_B),
            wrapped_label(rate_note, 5.5, font_size=22, color=GRAD),
            wrapped_label(r"activation history: \ $K$ states versus one equilibrium state", 5.5, font_size=21, color=CONS),
            wrapped_label(r"parameters, local derivatives and linear-solver workspace remain", 5.5, font_size=20, color=GREY_B),
            wrapped_label(rf"residual ${metric_tex(initial['residual'])}$; \ tolerance ${metric_tex(initial['tolerance'])}$; \ cap ${initial['cap']}$",
                          5.5, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.0, 0.55, 0])
        leg = label(r"grey: \ $\rho(J)^K$", font_size=20, color=GREY_B).next_to(g, DOWN, buff=0.05).align_to(g, RIGHT)
        floor_verdict = comparison_floor(errs[-10:])
        verdict = gradient_rate_comparison(float(d["rate"]), rho)
        rate_statement = (f"The fitted per-step factor is {d['rate']:.3f}, {verdict}." if math.isfinite(d["rate"]) else
                          "A finite fitted per-step gradient-gap factor is unavailable.")
        floor_note = wrapped_label(rf"display floor $10^{{-14}}$: ${int(np.count_nonzero(errs[ok] < 1e-14))}$ error values; "
                                  rf"${int(np.count_nonzero(~ok))}$ invalid values omitted; \ grey reference also floored",
                                  12.8, font_size=20, color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            f"Check it on a layer with an {d['initial_state_dimension']}-dimensional state; {solve_verdict}. "
            "The displayed residual and contraction bound describe this iteration solver; invertibility of I minus J "
            "is the separate differentiation condition. <bookmark mark='a'/> The usual alternative is to "
            "unroll: run K iterations and backpropagate through all of them with our library. As K grows, that "
            f"gradient is compared with the implicit candidate. <bookmark mark='b'/> {rate_statement} "
            f"For the final comparisons, {floor_verdict}. This is not a certified bound on fixed-point "
            "accuracy. <bookmark mark='c'/> Unrolling stores every iteration; implicit differentiation avoids that "
            "history while retaining the equilibrium state and linear-solver workspace."
        ) as vo:
            self.play(FadeIn(g), FadeIn(info[0]), FadeIn(info[1]), FadeIn(info[6]), FadeIn(floor_note))
            vo.wait_until("a")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(pred), FadeIn(leg), FadeIn(info[2]), FadeIn(info[3]))
            vo.wait_until("c")
            self.play(FadeIn(info[4]), FadeIn(info[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        d = load("deq")
        xs, ys, gx = np.asarray(d["xs"]), np.asarray(d["ys"]), np.asarray(d["gx"])
        fits = np.asarray(d["fits"])
        keep = [int(k) for k in d["keep"]]
        finite_y = np.r_[ys[np.isfinite(ys)], fits[np.isfinite(fits)]]
        low, high = min(-1.6, float(finite_y.min()) - 0.15), max(1.6, float(finite_y.max()) + 0.15)
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[low, high, 1], x_length=6.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.6, 0])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(xs, ys)])
        lines = [curve(ax, gx, f, FIT, 3.5) for f in fits]
        cv = np.asarray(d["curve"])
        ok = (cv[:, 0] > 0) & np.isfinite(cv[:, 1]) & (cv[:, 1] > 0)
        loss_logs = np.log10(cv[ok, 1])
        bottom = min(-6, math.floor(float(loss_logs.min()))) if len(loss_logs) else -6
        top = max(0, math.ceil(float(loss_logs.max()))) if len(loss_logs) else 0
        g2 = log_axes((0, math.log10(d["steps"])), (bottom, top), x_length=4.4, y_length=2.3, xlabel=r"step",
                      ylabel=r"loss", center=[3.8, 1.35, 0], ystep=max(1, math.ceil((top - bottom) / 4)), font_size=18)
        lc = VGroup()
        ids = np.flatnonzero(ok)
        for run in np.split(ids, np.flatnonzero(np.diff(ids) > 1) + 1):
            if len(run) > 1:
                lc.add(curve(g2.ax, np.log10(cv[run, 0]), np.log10(cv[run, 1]), C.LOSS, 2.5))
        it = np.asarray(d["iters_curve"])
        final_solve = fixed_point_summary(d["solves"]["final"])
        end_note = (rf"against $200$ unrolled steps: \ relative gradient gap ${sci(d['end_diff'], 0)}$"
                    if math.isfinite(d["end_diff"]) else r"the final finite gradient comparison is unavailable")
        info = VGroup(
            label(rf"state dimension ${d['training_state_dimension']}$; \ ${d['parameter_count']}$ trainable scalars", font_size=21, color=GREY_A),
            label(rf"loss: \ ${d['first_loss']:.3f} \to {sci(d['final_loss'], 1)}$", font_size=22, color=C.LOSS),
            label(rf"mean iteration work: \ ${it[0, 1]:.0f} \to {it[-1, 1]:.0f}$", font_size=22, color=GREY_A),
            wrapped_label(end_note, 5.7, font_size=21, color=GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.8, -1.05, 0])
        training, fit = d["solves"]["training"], d["solves"]["fit"]
        residual_note = (rf"max training residual ${sci(training['max_residual'], 0)}$" if math.isfinite(training["max_residual"]) else
                         r"finite maximum training residual unavailable")
        solves_note = wrapped_label(rf"training solves: ${training['converged']}/{training['count']}$ converged; "
                                   rf"${training['capped']}$ capped, ${training['nonfinite']}$ non-finite. "
                                   rf"Fit-grid solves: ${fit['converged']}/{fit['count']}$ converged. "
                                   rf"Residual tolerance ${sci(training['tolerance'], 0)}$; cap ${training['cap']}$. \ {residual_note}. "
                                   rf"Loss log plot omits step zero and ${int(np.count_nonzero((cv[:, 0] > 0) & ~ok))}$ nonpositive/invalid losses.",
                                   5.8, font_size=20, color=GREY_B).move_to([3.7, -2.5, 0])
        step_l = [label(rf"step ${k}$", font_size=22, color=FIT).next_to(ax, UP, buff=0.1).align_to(ax, LEFT) for k in keep]
        uses = label(r"also: \ meta-learning (iMAML, 2019), \ optimization layers (OptNet, 2017), \ hyperparameters",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        cite_ = cite(r"S.~Bai, J.~Z.~Kolter \& V.~Koltun, \textit{Deep Equilibrium Models} (2019)", corner=UR)
        it_v = (f"mean iteration work increases from {it[0, 1]:.0f} updates initially to {it[-1, 1]:.0f} finally"
                if it[-1, 1] > it[0, 1] else
                f"mean iteration work is {it[0, 1]:.0f} updates initially and {it[-1, 1]:.0f} finally")
        loss_verdict = loss_comparison(float(d["first_loss"]), float(d["final_loss"]))
        solve_counts = (f"Of {training['count']} training solves, {training['converged']} converged, "
                        f"{training['capped']} hit the cap and {training['nonfinite']} were non-finite.")
        with self.voiceover(
            f"And it trains. A deep equilibrium model with a {d['training_state_dimension']}-dimensional state and "
            f"{d['parameter_count']} trainable scalars is fitted using implicit candidate gradients, with its "
            f"feedback matrix kept at spectral norm at most {d['contraction_caps']['training']:g}. "
            f"<bookmark mark='a'/> The stored fits replay the run; {loss_verdict}, and {it_v}. {solve_counts} "
            f"Capped solves are not counted as converged equilibria. For the final comparison input, {final_solve}. "
            "<bookmark mark='b'/> Shaojie Bai, Zico Kolter "
            "and Vladlen Koltun proposed such models in 2019. "
            "The same trick differentiates through an inner optimization, in meta-learning, or through a solver used "
            "as a layer: wherever the answer is defined by an equation rather than a recipe."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), Create(lines[0]), FadeIn(step_l[0]), FadeIn(g2), Create(lc),
                      FadeIn(info[0]), FadeIn(cite_))
            vo.wait_until("a")
            for k in range(1, len(keep)):
                self.play(Transform(lines[0], lines[k]), Transform(step_l[0], step_l[k]), run_time=0.9)
            self.play(FadeIn(info[1]), FadeIn(info[2]), FadeIn(info[3]), FadeIn(solves_note))
            vo.wait_until("b")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
