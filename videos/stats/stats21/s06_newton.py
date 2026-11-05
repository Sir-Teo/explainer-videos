from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Newton(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.landscape()
        self.digits()
        self.failure()
        self.gauss_newton()
        self.remedies()

    def card(self):
        card = chapter_card(5, r"Newton and Fisher scoring", r"Climb by the curvature", part=PART)
        with self.voiceover("Chapter five. Newton's method, and Fisher scoring."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\ell(\theta)", r"\approx", r"\ell(\theta_k) + g_k'(\theta - \theta_k) + \tfrac12 (\theta - \theta_k)' H_k (\theta - \theta_k)", font_size=28),
            cmath(r"\theta_{k+1}", r"=", r"\theta_k - H_k^{-1} g_k", font_size=32),
            cmath(r"\text{Fisher scoring}", r":", r"H_k \to -\mathcal{I}(\theta_k), \ \text{the expected information}", font_size=28),
            cmath(r"\text{logistic}", r":", r"\beta_{k+1} = (X'W_kX)^{-1} X'W_k z_k \ \ \text{(IRLS)}", font_size=28),
        ]
        rows[1][2].set_color(NEWT)
        whys = [why(r"a quadratic through the current point"), why(r"jump to the quadratic's peak"),
                why(r"Fisher (1925): \ always negative definite"), why(r"identical for a canonical link: \ Part 14")]
        with self.voiceover(
            "<bookmark mark='a'/> Newton's idea: near the current guess, approximate the log likelihood by a quadratic, using "
            "its gradient g and its Hessian H, the matrix of second derivatives. <bookmark mark='b'/> Then jump straight to the "
            "quadratic's peak: theta minus H inverse g. <bookmark mark='c'/> Fisher's scoring method, from 1925, replaces the "
            "Hessian by minus the expected information, which is always negative definite, so every step goes uphill in a "
            "useful direction. <bookmark mark='d'/> For logistic regression and any canonical link the two are identical, and "
            "each step is a weighted least squares fit: iteratively reweighted least squares, from Part 14."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def landscape(self):
        d = load("newton")
        b0s, b1s = d["b0s"], d["b1s"]
        A = axes([b0s[0], b0s[-1]], [b1s[0], b1s[-1]], x_length=6.6, y_length=5.2, xlabel=r"intercept $\beta_0$",
                 ylabel=r"slope $\beta_1$ \ (per $\log_{10}$ income)", xticks=[-5, -4, -3, -2, -1, 0, 1], yticks=[0, 1, 2, 3],
                 center=[-2.6, 0.1, 0], font_size=18)
        ax = A.ax
        mx = d["ll_max"]
        L = Landscape(ax, np.asarray(d["ll"]), (b0s[0], b0s[-1]), (b1s[0], b1s[-1]), [mx - v for v in (2, 8, 30, 100, 300, 700)],
                      color=LEVEL, stroke_width=1.8)
        newt = L.path(d["path"][:6], color=NEWT, radius=0.07)
        grad = L.path(d["gpath"][:60], color=GRAD, radius=0.035, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"the World's vote on log income, \ $n = {d['n']:,}$", font_size=22),
            label(r"contours: \ the log likelihood", font_size=22, color=LEVEL),
            label(r"red: \ gradient ascent, \ best fixed step", font_size=22, color=GRAD),
            label(r"blue: \ Newton", font_size=22, color=NEWT),
            label(r"a long, \ narrow ridge: \ intercept and slope trade off", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the log likelihood of a logistic regression of the World's vote on log income, two "
            "thousand adults, as contours over the intercept and slope. <bookmark mark='b'/> The peak sits at the end of a long, "
            "narrow ridge, because with an uncentred predictor the intercept and slope can trade off against each other. "
            "<bookmark mark='c'/> Gradient ascent, in red, always steps straight uphill. On a narrow ridge, uphill points "
            "mostly across the ridge rather than along it, so it creeps: after sixty steps it has covered about a quarter of "
            "the distance. "
            "<bookmark mark='d'/> Newton, in blue, knows the curvature, so it steps along the ridge. Five steps, and it's there."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(L.levels), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(grad[1][0]), FadeIn(rows[2]))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(p_)) for s_, p_ in zip(grad[0], grad[1][1:])], lag_ratio=0.3),
                      run_time=6.0)
            vo.wait_until("d")
            self.play(FadeIn(newt[1][0]), FadeIn(rows[3]))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(p_)) for s_, p_ in zip(newt[0], newt[1][1:])], lag_ratio=0.6),
                      run_time=3.0)
        self.wait(1.0)
        self.clear_scene()

    def digits(self):
        d = load("newton")
        err = d["err"]
        hdr = [r"\textbf{step}", r"\textbf{Newton: \ error}", r"\textbf{gradient: \ error}"]
        body = []
        for k in range(6):
            e = err[k] if k < len(err) else 0.0
            ge = d["gerr"][k]
            body.append([str(k), (f"{e:.1e}" if e > 0 else "0 (machine precision)"), f"{ge:.2f}"])
        body.append([r"400", r"---", f"{d['gerr'][-1]:.2f}"])
        t = table_rows([hdr] + body, font_size=24, col_buff=0.9, row_buff=0.26, colors=[GREY_A] + [None] * 7)
        for row in t[1:6]:
            row[1].set_color(NEWT)
            row[2].set_color(GRAD)
        t.move_to([0, 0.5, 0])
        foot = fit_rows(VGroup(
            label(r"Newton: \ the number of correct digits roughly doubles each step: \ quadratic convergence", font_size=22, color=NEWT),
            label(r"gradient: \ the error shrinks by a fixed factor: \ linear, \ slow when the problem is ill-conditioned", font_size=22, color=GRAD),
        ), 12.4, 0.25, [0, -2.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Count the error after each step, the distance to the maximum. Newton starts four units away; "
            "then point four five; then point zero one two; then nine millionths; then five trillionths; then nothing a "
            "computer can measure. <bookmark mark='b'/> The number of correct digits roughly doubles every step: quadratic "
            "convergence. <bookmark mark='c'/> Gradient ascent shrinks the error by a constant factor each step, and on this "
            "ridge the factor is close to one: after four hundred steps it's still point five eight away. The price of Newton is "
            "a linear system with the Hessian at each step, which for a few dozen parameters is nothing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in t[1:]], lag_ratio=0.4), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def failure(self):
        c = load("convex")
        d = load("newton")
        th, cl = np.asarray(c["theta"]), np.asarray(c["cauchy"])
        A = axes([-6, 10], [float(cl.min()), float(cl.max()) + 1], x_length=8.4, y_length=4.2, xlabel=r"location $\theta$",
                 ylabel=r"Cauchy log likelihood", xticks=[-6, -2, 0, 2, 6, 10], center=[-1.4, 0.4, 0])
        ax = A.ax
        cv = curve(ax, th, cl, RES, 3.5)
        at = lambda t: ax.c2p(t, float(np.interp(t, th, cl)))  # noqa: E731
        plain = VGroup(*[Dot(at(t), radius=0.08, color=GRAD) for t in d["cauchy_plain"]])
        safe = VGroup(*[Dot(at(t), radius=0.07, color=HIT) for t in d["cauchy_safe"]])
        rows = fit_rows(VGroup(
            label(r"start at $\theta = 1.2$, \ in the valley", font_size=22),
            label(rf"plain Newton $\to$ {d['cauchy_plain'][-1]:.2f}: \ a minimum!", font_size=22, color=GRAD),
            label(r"it finds where the slope is zero, \ not where the top is", font_size=22, color=GREY_A),
            label(rf"with a line search $\to$ {d['cauchy_safe'][-1]:.2f}: \ a peak", font_size=22, color=HIT),
            label(r"the higher of the two, \ here; \ not guaranteed", font_size=22, color=OBS),
        ), 3.45, 0.42, [5.1, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Newton can fail. Back to chapter one's Cauchy likelihood, with its two peaks, and start in the "
            "valley between them, at one point two. <bookmark mark='b'/> In the valley the curvature is positive, so the "
            "quadratic approximation is a bowl, and Newton jumps to the bottom of the bowl: it converges, quadratically, to "
            "point seven six, the lowest point of the valley. <bookmark mark='c'/> Newton looks for a zero of the gradient, and "
            "a minimum has one too. <bookmark mark='d'/> With a line search, which refuses any step that lowers the likelihood "
            "and falls back on the gradient when the curvature points the wrong way, it climbs instead, to three point nine nine. "
            "<bookmark mark='e'/> Here that's the higher peak. In general nothing local can promise the global one."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(plain[0], scale=1.5), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in plain[1:]], lag_ratio=0.4), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in safe], lag_ratio=0.2), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def gauss_newton(self):
        rows = [
            cmath(r"\min_\theta", r"", r"\textstyle\sum_i \big(y_i - m(x_i; \theta)\big)^2", font_size=30),
            cmath(r"\text{Hessian}", r"=", r"2J'J - 2\textstyle\sum_i r_i \nabla^2 m_i \approx 2J'J", font_size=30),
            cmath(r"\theta_{k+1}", r"=", r"\theta_k + (J'J)^{-1} J' r", font_size=30),
            cmath(r"\text{Levenberg--Marquardt}", r":", r"(J'J + \mu I)^{-1} J'r", font_size=30),
        ]
        rows[2][2].set_color(NEWT)
        whys = [why(r"nonlinear least squares: \ growth curves, \ dose--response"), why(r"$J$: \ the Jacobian; \ drop the residual term"),
                why(r"Gauss--Newton: \ a linear least-squares fit each step"), why(r"a trust region: \ $\mu$ large is a gradient step")]
        with self.voiceover(
            "<bookmark mark='a'/> A close relative handles nonlinear least squares, fitting a curve like a growth model or a "
            "dose-response curve. <bookmark mark='b'/> The Hessian has two parts: J transposed J, built from first derivatives "
            "only, and a term weighted by the residuals, which is small near a good fit. Gauss–Newton drops the second. "
            "<bookmark mark='c'/> Each step is then an ordinary least-squares regression of the residuals on the Jacobian, "
            "exactly as Fisher scoring is a weighted least-squares fit. <bookmark mark='d'/> Levenberg and Marquardt add a "
            "multiple of the identity, which shortens the step when the linearization can't be trusted: large mu gives a cautious "
            "gradient step, small mu a bold Gauss–Newton step."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def remedies(self):
        rows = fit_rows(VGroup(
            label(r"line search: \ shrink the step until the objective improves", font_size=24, color=HIT),
            label(r"trust region: \ trust the quadratic only within a radius \ (Levenberg--Marquardt)", font_size=24, color=NEWT),
            label(r"quasi-Newton: \ build the curvature from gradients \ (BFGS)", font_size=24, color=TEAL),
            label(r"several starting points, \ for problems that are not concave", font_size=24, color=OBS),
            label(r"cost: \ $O(p^3)$ per step; \ for millions of parameters, \ chapters seven to ten", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The standard repairs: a line search, which shrinks each step until the objective improves; "
            "<bookmark mark='b'/> a trust region, which trusts the quadratic only within a radius it adjusts as it goes, the "
            "Levenberg–Marquardt idea; <bookmark mark='c'/> quasi-Newton methods like BFGS, which build up the curvature from "
            "successive gradients without ever computing a Hessian; <bookmark mark='d'/> and several starting points for "
            "problems that aren't concave. <bookmark mark='e'/> Newton's real limit is cost: solving with a p by p matrix takes "
            "of order p cubed operations. With millions of parameters we need the cheaper methods of the coming chapters."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
