from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, expo, load, log_axes, mant


def saddle_f(x, y):
    return 0.5 * x * x - 0.5 * y * y + 0.25 * y ** 4


def rate_comparison(gap):
    if not math.isfinite(gap):
        return "a finite comparison with the predicted rates is unavailable"
    if gap < 1e-6:
        return "match the predicted norm-error factors within one millionth"
    return f"have a largest absolute difference of {gap:.6f} from the predicted norm-error factors"


def escape_comparison(slope, predicted):
    if not (math.isfinite(slope) and math.isfinite(predicted) and predicted > 0):
        return "there are too few resolved escape runs for a finite slope comparison"
    if abs(slope - predicted) < 0.1 * predicted:
        return "the measured slope is within ten percent of the local linear prediction"
    if slope > predicted:
        return "the measured slope is larger than the local linear prediction"
    return "the measured slope is smaller than the local linear prediction"


def threshold_summary(record):
    hit = record["first_hit_step"]
    if record["status"] == "converged" and hit is not None:
        return f"the threshold was reached after {int(hit):,} updates"
    if record["status"] == "capped":
        return f"the threshold was not reached within the cap of {int(record['cap']):,} updates"
    return "the threshold crossing is unresolved; no converged step count is reported"


class Quadratic(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.valley()
        self.rates()
        self.saddle()

    def card(self):
        card = chapter_card(14, r"Descent on a quadratic; \ saddles", r"How fast can going downhill be?", part=PART)
        with self.voiceover("Chapter fourteen. How fast is downhill?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        col = {r"\eta": C.LR, r"\lambda_i": HESS}
        rows = [
            cmath(r"x_{t+1}", r"=", r"x_t - \eta H x_t = (I - \eta H)\, x_t", font_size=36),
            cmath(r"c_{i,\,t+1}", r"=", r"(1 - \eta \lambda_i)\, c_{i,\,t}", font_size=36),
            cmath(r"\text{converges}", r"\iff", r"0 < \eta < 2 / \lambda_{\max}", font_size=36),
            cmath(r"q", r"=", r"\max_i |1 - \eta\lambda_i| \;\ge\; \frac{\kappa - 1}{\kappa + 1}", font_size=36),
        ]
        whys = [why(r"$f = \frac12 x^\top H x$, \ so $\nabla f = H x$", font_size=22),
                why(r"in $H$'s eigenvectors \ (Part 3), \\ each coordinate $c_i$ on its own", font_size=22),
                why(r"$|1 - \eta\lambda_i| < 1$ for every $i$", font_size=22),
                why(r"best at $\eta = 2/(\lambda_{\min} + \lambda_{\max})$; \\ $\kappa = \lambda_{\max}/\lambda_{\min}$", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.6, edge=6.9)
        head = label(r"gradient descent on a quadratic bowl, \ $H = H^\top \succ 0$", font_size=28, color=GREY_A)
        head.to_edge(UP, buff=0.3)
        dc = definition_card(r"norm-error factor $q$", r"$\|x_{t+1}\|_2 \le q\,\|x_t\|_2$; \ the objective contracts by at most $q^2$. "
                             r"\quad $\kappa=\lambda_{\max}/\lambda_{\min}$", width=10.4, font_size=21).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "On a quadratic bowl with a positive-definite Hessian, gradient descent can be solved exactly. "
            "<bookmark mark='a'/> Each step multiplies the position by I minus eta H. "
            "<bookmark mark='b'/> In the Hessian's eigenvectors that matrix is diagonal, so each coordinate shrinks "
            "on its own, by one minus eta times its eigenvalue. <bookmark mark='c'/> Every factor must be less than one "
            "in size, so the step must be positive and smaller than two over the largest curvature. <bookmark mark='d'/> And the "
            "slowest coordinate sets the pace. The best step balances the two extremes, and the rate is kappa minus "
            "one over kappa plus one, where kappa, the condition number, is the largest curvature over the smallest. "
            "This factor bounds the position-error norm; the quadratic objective shrinks by at most its square."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=C.LR, scale_factor=1.04))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(dc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def valley(self):
        v = load("valley")
        H = np.asarray(v["H"])
        assert np.allclose(np.diag(H), [1.0, 25.0])
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1.2, 1.2, 0.5], x_length=11.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(DOWN * 0.6)

        def f(x, y):
            return 0.5 * (H[0, 0] * x * x + H[1, 1] * y * y)

        cont = contour_lines(ax, f, (-5, 5), (-1.2, 1.2), [0.25 * 2 ** k for k in range(8)], n=(200, 80))
        paths = {}
        for name, col in (("gd", WHITE), ("momentum", C.TRUE_P), ("newton", C.BITS)):
            pts = [ax.c2p(*q) for q in np.asarray(v[name])]
            paths[name] = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
        dots = {k: Dot(paths[k].get_start(), radius=0.08, color=paths[k].get_color()) for k in paths}
        gd_summary = threshold_summary(v["convergence"]["gd"])
        lab = {"gd": wrapped_label(rf"gradient descent: \ {gd_summary}", 7.8, font_size=22),
               "momentum": label(r"with momentum \ (Part 11)", font_size=24, color=C.TRUE_P),
               "newton": label(r"Newton: \ $-H^{-1}\nabla f$, \ one step", font_size=24, color=C.BITS)}
        VGroup(*lab.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4)
        curv = label(r"curvatures $1$ and $25$: \ $\kappa = 25$, \ a long, narrow valley", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        gd_final = float(np.linalg.norm(np.asarray(v["gd"])[-1]))
        mom_final = float(np.linalg.norm(np.asarray(v["momentum"])[-1]))
        momentum_verdict = ("Momentum has a smaller final position-error norm over this equal update budget."
                            if mom_final < gd_final else
                            "Momentum does not have a smaller final position-error norm over this equal update budget.")
        with self.voiceover(
            "Here is a valley with kappa of twenty-five: it bends twenty-five times more sharply across than along. "
            "<bookmark mark='a'/> The steepest way down points mostly at the opposite wall, so the steps zigzag from "
            f"wall to wall and crawl along the floor. For the objective to fall below one percent of its initial "
            f"value, {gd_summary}. <bookmark mark='b'/> Momentum carries speed from step to step. "
            f"{momentum_verdict} Part 11 derives the method. "
            "<bookmark mark='c'/> Newton's step undoes the curvature and lands at the bottom at once."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), FadeIn(curv), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots["gd"]), FadeIn(lab["gd"]))
            self.play(Create(paths["gd"]), MoveAlongPath(dots["gd"], paths["gd"]), run_time=3.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(dots["momentum"]), FadeIn(lab["momentum"]))
            self.play(Create(paths["momentum"]), MoveAlongPath(dots["momentum"], paths["momentum"]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(dots["newton"]), FadeIn(lab["newton"]))
            self.play(Create(paths["newton"]), MoveAlongPath(dots["newton"], paths["newton"]), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rates(self):
        q = load("quad")
        ks = np.asarray(q["kappas"], float)
        ro, rp = np.asarray(q["rate_opt"]), np.asarray(q["rate_opt_pred"])
        so = np.asarray(q["steps_opt"], float)
        kk = np.logspace(0, 3, 100)
        g1 = axes([0, 3, 1], [0, 1.0, 0.25], x_length=5.0, y_length=3.4, xlabel=r"condition number $\kappa$",
                  ylabel=r"norm-error factor per step", xticks=[0, 1, 2, 3],
                  xfmt=lambda v: {0: "1", 1: "10", 2: "100", 3: "1000"}[int(v)], yticks=[0, 0.5, 1], center=[-3.5, 0.3, 0])
        pred = curve(g1.ax, np.log10(kk), (kk - 1) / (kk + 1), GREY_B, 2.5)
        valid_rate = np.isfinite(ro) & np.isfinite(rp)
        meas = VGroup(*[Dot(g1.ax.c2p(math.log10(k), r), radius=0.07, color=GRAD)
                       for k, r in zip(ks[valid_rate], ro[valid_rate])])
        leg1 = VGroup(label(r"$(\kappa - 1)/(\kappa + 1)$", font_size=20, color=GREY_B),
                      label(r"measured", font_size=20, color=GRAD)).arrange(RIGHT, buff=0.4).next_to(g1, DOWN, buff=0.15)
        runs = q["convergence"]["opt"]
        resolved = np.asarray([r["status"] == "converged" and r["first_hit_step"] is not None for r in runs])
        work = np.asarray([r["iterations"] for r in runs], float)
        ok = np.isfinite(work) & (work >= 1)
        top_steps = max(4, math.ceil(math.log10(max(float(work[ok].max()), 1))))
        g2 = log_axes((0, 3), (0, top_steps), x_length=5.0, y_length=3.4, xlabel=r"condition number $\kappa$",
                      ylabel=r"updates: \ relative norm below $10^{-6}$", center=[3.6, 0.3, 0])
        c2 = VGroup()
        for k, s, done in zip(ks[ok], work[ok], resolved[ok]):
            point = g2.ax.c2p(math.log10(k), math.log10(s))
            marker = Dot(point, radius=0.07, color=GRAD) if done else Triangle(color=C.PENALTY).scale(0.07).move_to(point)
            c2.add(marker)
        lin = curve(g2.ax, np.log10(kk[kk > 1.5]), np.log10(kk[kk > 1.5] / 2 * math.log(1e6)), GREY_B, 2)
        worst = float(np.abs(ro[valid_rate] - rp[valid_rate]).max()) if valid_rate.any() else float("nan")
        etas, fin = np.asarray(q["etas"]), np.asarray(q["final"])
        start = float(np.linalg.norm([-4.5, 0.9]))  # the valley's starting point
        edge = float(etas[np.argmax(fin > start)]) if (fin > start).any() else float("nan")
        stability_verdict = (f"The first sampled step size whose norm after one hundred updates exceeds its initial "
                             f"norm is {edge:.3f}." if math.isfinite(edge) else
                             "No sampled step size has a norm after one hundred updates above its initial norm.")
        coverage = label(rf"${int(resolved.sum())}/{len(runs)}$ reached threshold; \ triangles: capped or unresolved; \ cap $20{{,}}000$",
                         font_size=20, color=GREY_A).next_to(g2, DOWN, buff=0.18)
        stab = wrapped_label(r"theoretical stability: \ $0<\eta<2/\lambda_{\max}=0.08$; \ numerical test: $100$ updates on a finite step-size grid",
                             12.7, font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(rf"measured on $\tfrac12(x^2 + \kappa y^2)$, \ best fixed step", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.35)
        k_big = int(ks[-1])
        verdict = rate_comparison(worst)
        step_verdict = threshold_summary(runs[-1])
        with self.voiceover(
            "Measured on bowls from kappa of one to a thousand: the rates, in orange, "
            f"{verdict}. <bookmark mark='a'/> The grey curve is the large-kappa norm-error estimate. At kappa "
            f"{k_big:,}, {step_verdict}. Triangles mark capped or unresolved runs, not converged counts. "
            f"<bookmark mark='b'/> The theoretical stability boundary is two over the largest curvature. "
            f"{stability_verdict} "
            "Real losses are not quadratics, but this is the calculus behind every learning-rate rule, and Part 11 "
            "builds the faster methods on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), Create(pred), FadeIn(leg1))
            self.play(LaggedStart(*[FadeIn(m) for m in meas], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(lin), FadeIn(coverage), LaggedStart(*[FadeIn(m) for m in c2], lag_ratio=0.15), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(stab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saddle(self):
        q = load("quad")
        ax = Axes(x_range=[-1.8, 1.8, 0.5], y_range=[-1.5, 1.5, 0.5], x_length=6.0, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.6, -0.5, 0])
        cont = contour_lines(ax, saddle_f, (-1.8, 1.8), (-1.5, 1.5), np.linspace(-0.24, 1.4, 14), n=(120, 100))
        cols = {"1e-02": C.TRUE_P, "1e-06": GRAD, "1e-10": C.BITS}
        paths = VGroup()
        for k, col in cols.items():
            pts = np.asarray(q[f"path_{k}"])
            paths.add(VMobject(color=col, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in pts]))
        stuck = np.asarray(q["stuck"])
        sp = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in stuck])
        sd = Dot(ax.c2p(0, 0), radius=0.08, color=WHITE)
        leg = VGroup(*[label(rf"$y_0 = 10^{{{int(k.split('e')[1])}}}$", font_size=20, color=c) for k, c in cols.items()],
                     label(r"$y_0 = 0$: \ stuck", font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg.arrange_in_grid(rows=2, cols=2, buff=(0.2, 0.12), cell_alignment=LEFT)
        leg.next_to(ax, UP, buff=0.18).align_to(ax, LEFT)
        y0s = np.asarray(q["y0s"])
        esc, pr = np.asarray(q["esc"], float), np.asarray(q["esc_pred"])
        e = -np.log10(y0s)
        escape_runs = q["convergence"]["escape"]
        solved = np.asarray([r["status"] == "converged" and r["first_hit_step"] is not None for r in escape_runs])
        top_escape = max(320, 100 * math.ceil(max(float(np.max(esc)), float(np.max(pr))) / 100))
        g2 = axes([0, 13, 2], [0, top_escape, max(100, top_escape // 4)], x_length=5.0, y_length=3.4, xlabel=r"$\log_{10}(1/y_0)$",
                  ylabel=r"updates until $|y|>0.5$", xticks=[0, 4, 8, 12], yticks=list(np.linspace(0, top_escape, 4)), center=[3.6, -0.2, 0])
        c_pr = curve(g2.ax, e, pr, GREY_B, 2.5)
        c_ms = VGroup(*[(Dot(g2.ax.c2p(a, b), radius=0.06, color=GRAD) if done else
                        Triangle(color=C.PENALTY).scale(0.07).move_to(g2.ax.c2p(a, b)))
                       for a, b, done in zip(e, esc, solved)])
        slope = float(np.polyfit(e[solved], esc[solved], 1)[0]) if solved.sum() >= 2 else float("nan")
        eta = 0.1
        pslope = math.log(10) / math.log(1 + eta)
        f_txt = MathTex(r"f = \tfrac12 x^2 - \tfrac12 y^2 + \tfrac14 y^4", font_size=30).to_edge(UP, buff=0.3).shift(LEFT * 3.4)
        sg = q["stuck_grad"]
        slope_note = (rf"resolved-run slope ${slope:.1f}$; \ local prediction ${pslope:.1f}$" if math.isfinite(slope) else
                      r"resolved-run slope unavailable")
        res = label(slope_note, font_size=21, color=GRAD).next_to(g2, UP, buff=0.2)
        coverage = label(rf"${int(solved.sum())}/{len(solved)}$ escaped; \ triangles: unresolved; \ cap $4{{,}}999$",
                         font_size=20, color=GREY_A).next_to(g2, DOWN, buff=0.18)
        cite_ = cite(r"Y.~Dauphin et al.\ (2014); \ C.~Jin et al.\ (2017)", corner=DR)
        verdict = escape_comparison(slope, pslope)
        with self.voiceover(
            "A saddle can delay descent. Here's a surface with a saddle at the centre and a minimum above and "
            "below it. <bookmark mark='a'/> Start almost on the line through the saddle, a tiny distance y nought off "
            "it. The walk slides in towards the saddle, where the gradient nearly vanishes, and waits, until the "
            "tiny offset has grown enough to fall off. <bookmark mark='b'/> Near the saddle the offset grows by one "
            "plus eta each step, so the local prediction is logarithmic in one over y nought. We fit only runs "
            f"that reached absolute y above one half; {verdict}. Capped runs are marked separately. "
            "<bookmark mark='c'/> Start exactly on the line "
            f"and it never leaves: the gradient falls to {mant(sg)} times ten to the minus {expo(sg)}, at a point that "
            "is not a minimum. Only the Hessian, with its negative eigenvalue, tells them apart. In practice the noise "
            "of stochastic gradients kicks a network off; Yann Dauphin and colleagues argued in 2014 that in many "
            "dimensions saddles, more than bad minima, are what slow training."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.05), FadeIn(f_txt), FadeIn(sd),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(leg[:3]), LaggedStart(*[Create(p) for p in paths], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(c_pr), FadeIn(coverage), LaggedStart(*[FadeIn(m) for m in c_ms], lag_ratio=0.1), FadeIn(res),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(Create(sp), FadeIn(leg[3]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
