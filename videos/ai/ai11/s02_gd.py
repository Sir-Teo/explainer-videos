from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import HIST, OPT_COLORS, PART, lag, load, predict_card, takeaway_card

UP_C, LO_C = C.SURPRISE, C.TRUE_P  # the upper (L) and lower (mu) quadratic bounds
GD = OPT_COLORS["gd"]


class GradientDescent(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.derive()
        self.convex()
        self.measure()
        self.predict()
        self.takeaway()

    def card(self):
        c = chapter_card(1, r"Gradient descent, derived", r"How fast does walking downhill get there?", part=PART)
        with self.voiceover("Chapter one. Gradient descent, derived."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def setup_(self):
        hist = history_card(1847, r"Augustin-Louis Cauchy", r"\textit{M\'ethode g\'en\'erale pour la r\'esolution des "
                            r"syst\`emes d'\'equations simultan\'ees}: \ to solve equations, step against the gradient of "
                            r"the error", width=5.6).to_corner(UL, buff=0.4)
        rule = cmath(r"x_{k+1}", "=", r"x_k - \eta\,\nabla f(x_k)", font_size=40).next_to(hist, DOWN, buff=0.5).align_to(hist, LEFT)
        # a smooth, strongly convex function between its two quadratic bounds at x0 (schematic)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 4.5, 1], x_length=5.6, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, -0.2, 0])

        def f(x):
            return 0.5 * x * x + 0.6 * math.log(math.cosh(1.4 * x)) + 0.2

        def df(x):
            return x + 0.84 * math.tanh(1.4 * x)

        x0, L, mu = -1.2, 1 + 0.84 * 1.4, 1.0
        fc = ax.plot(f, x_range=[-2.4, 2.4], color=WHITE, stroke_width=3.5)
        up = ax.plot(lambda x: f(x0) + df(x0) * (x - x0) + 0.5 * L * (x - x0) ** 2, x_range=[-2.4, 0.4], color=UP_C,
                     stroke_width=2.5)
        lo = ax.plot(lambda x: f(x0) + df(x0) * (x - x0) + 0.5 * mu * (x - x0) ** 2, x_range=[-2.4, 1.6], color=LO_C,
                     stroke_width=2.5)
        dot = Dot(ax.c2p(x0, f(x0)), radius=0.07, color=C.BITS)
        x1 = x0 - df(x0) / L
        step = Arrow(ax.c2p(x0, f(x0)), ax.c2p(x1, f(x1)), buff=0.05, color=C.BITS, stroke_width=3,
                     max_tip_length_to_length_ratio=0.2)
        ul = label(r"$L$-smooth: \ below this bowl", font_size=20, color=UP_C).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ll = label(r"$\mu$-strongly convex: \ above this one", font_size=20, color=LO_C).next_to(ul, DOWN, buff=0.08).align_to(ul, LEFT)
        sch = note(r"schematic").next_to(ax, DOWN, buff=0.1)
        defs = definition_card(r"$L$-smooth, \ $\mu$-strongly convex",
                               r"$\|\nabla f(x) - \nabla f(y)\| \le L\|x - y\|$: \ the curvature is at most $L$. \ "
                               r"$f(y) \ge f(x) + \nabla f(x)^\top (y - x) + \tfrac{\mu}{2}\|y - x\|^2$: \ at least $\mu$. "
                               r"\ The ratio $\kappa = L/\mu$ is the \textit{condition number}.", width=6.2, font_size=22)
        defs.to_corner(DL, buff=0.35)
        with self.voiceover(
            "In 1847, Augustin Cauchy wanted to solve the equations of astronomy, and proposed a general method: "
            "measure which way the error falls fastest, and step that way. Gradient descent. <bookmark mark='a'/> "
            "To say how fast it works, we need two numbers about the loss. <bookmark mark='b'/> It is L-smooth if "
            "its curvature is never more than L: at every point it lies below a bowl of curvature L. "
            "<bookmark mark='c'/> And it is mu-strongly convex if its curvature is never less than mu: it lies above a "
            "bowl of curvature mu. <bookmark mark='d'/> Their ratio, kappa, is the condition number: how much more "
            "steeply the valley curves one way than another."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2), Write(rule))
            vo.wait_until("a")
            self.play(Create(ax), Create(fc), FadeIn(dot), FadeIn(sch))
            vo.wait_until("b")
            self.play(FadeOut(hist), Create(up), FadeIn(ul), GrowArrow(step))
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(ll))
            vo.wait_until("d")
            self.play(FadeOut(rule), FadeIn(defs, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"one step, \ $x^+ = x - \eta\,\nabla f(x)$", font_size=30).to_edge(UP, buff=0.3)
        cl = {r"\kappa": C.BITS, r"\mu": LO_C, r"L": UP_C}
        rows = [
            cmath(r"f(x^+)", r"\le", r"f(x) - \eta\,\|\nabla f\|^2 + \tfrac{L \eta^2}{2}\,\|\nabla f\|^2", font_size=34),
            cmath(r"f(x^+)", r"\le", r"f(x) - \tfrac{1}{2L}\,\|\nabla f(x)\|^2", font_size=34),
            cmath(r"\|\nabla f(x)\|^2", r"\ge", r"2\mu\,\big(f(x) - f^*\big)", font_size=34),
            cmath(r"f(x^+) - f^*", r"\le", r"\big(1 - \tfrac{\mu}{L}\big)\big(f(x) - f^*\big)", font_size=34),
            cmath(r"f(x_k) - f^*", r"\le", r"\big(1 - \tfrac{1}{\kappa}\big)^{k}\,\big(f(x_0) - f^*\big)", font_size=34),
            cmath(r"k", r"\approx", r"\kappa\,\ln(1/\varepsilon)", font_size=36, colors=cl),
        ]
        whys = [why(r"$L$-smooth: \ below the bowl of curvature $L$"), why(r"$\eta = 1/L$, \ the best step in this bound"),
                why(r"$\mu$-strongly convex: \ minimize the lower bowl"), why(r"subtract $f^*$, \ combine the two"),
                why(r"repeat $k$ times; \ $\kappa = L/\mu$"), why(r"to shrink the error $\varepsilon$-fold")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.6, buff=0.5, edge=6.9)
        thm = theorem_card(r"Gradient descent, \ strongly convex", r"With $\eta = 1/L$ the error shrinks by a factor "
                           r"$1 - 1/\kappa$ every step: \ linear convergence, \ in about $\kappa\ln(1/\varepsilon)$ steps.",
                           width=7.6, font_size=24).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the derivation. <bookmark mark='a'/> Take one step. Because the loss lies below the bowl of "
            "curvature L, the step lowers it by eta times the gradient squared, minus a penalty of L eta squared over "
            "two. <bookmark mark='b'/> The best step this bound allows is eta equals one over L, and it guarantees a "
            "drop of the gradient squared over two L. <bookmark mark='c'/> Strong convexity says the gradient can't be "
            "small while we are far from the bottom: its square is at least two mu times the gap. "
            "<bookmark mark='d'/> Put the two together: each step shrinks the gap by a factor of one minus mu over L. "
            "<bookmark mark='e'/> Repeat, and the gap falls geometrically, one minus one over kappa per step. "
            "<bookmark mark='f'/> So the number of steps grows in proportion to the condition number. A valley "
            "a thousand times steeper one way than another needs about a thousand times more steps."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                step(k)
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convex(self):
        q = load("quad")
        ks = np.asarray(q["conv_k"], float)
        gd, bg = np.asarray(q["conv_gd"]), np.asarray(q["bound_gd"])
        sel = np.unique(np.round(np.geomspace(1, len(ks), 120)).astype(int)) - 1
        lk = np.log10(ks[sel])
        y0 = math.floor(np.log10(gd[sel].min())) - 0.2
        y1 = math.ceil(np.log10(bg[sel].max()))
        ax = CornerAxes(x_range=[0, lk.max(), 1], y_range=[y0, y1, 1], x_length=6.4, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.6, -0.6, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, y0), DOWN, buff=0.1)
                      for k in range(0, int(lk.max()) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.1)
                      for k in range(math.ceil(y0), y1 + 1)])
        xn = label(r"steps $k$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"$f(x_k) - f^*$", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        meas = curve(ax, lk, np.log10(gd[sel]), GD, 3.5)
        bound = DashedVMobject(curve(ax, lk, np.log10(bg[sel]), UP_C, 2.5), num_dashes=40)
        thm = theorem_card(r"Gradient descent, \ convex", r"Without strong convexity ($\mu = 0$): \ "
                           r"$f(x_k) - f^* \le \dfrac{L\,\|x_0 - x^*\|^2}{2k}$, \ a rate of $1/k$.", width=6.0,
                           font_size=22).move_to([3.7, 1.4, 0])
        lg = VGroup(label(r"measured", font_size=22, color=GD), label(r"the bound $L\|x_0 - x^*\|^2/2k$", font_size=22,
                                                                         color=UP_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lg.next_to(thm, DOWN, buff=0.5).align_to(thm, LEFT)
        tag = note(r"a quadratic with curvatures $1, \tfrac14, \tfrac19, \dots, 10^{-6}$; \ $\eta = 1/L$; \ computed").to_corner(DR, buff=0.25)
        held = bool((gd <= bg * (1 + 1e-9)).all())
        with self.voiceover(
            "If the loss is convex but not strongly convex, the bowl beneath it can be flat, and the guarantee "
            "weakens: the gap falls like one over k, the number of steps. <bookmark mark='a'/> Here is gradient "
            "descent on a quadratic whose curvatures run from one down to a millionth, with the bound drawn dashed. "
            + ("<bookmark mark='b'/> The measured gap stays under the bound at every step, as the theorem says it "
               "must, and its slope on these log axes is the slope of a power law, not of a geometric decay."
               if held else
               "<bookmark mark='b'/> The measured gap should stay under the bound; here it does not everywhere, which "
               "points to rounding at the smallest values.")
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(bound), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(meas), FadeIn(lg[0]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        q = load("quad")
        kap = np.asarray(q["kappas"], float)
        it = {m: np.asarray(q[f"iters_{m}"], float) for m in ("gd", "gd_opt")}
        pr = np.asarray(q["pred_gd"], float)
        rate, rpred = q["rate_gd"], q["rate_pred_gd"]
        slope = float(q["slope_gd"])
        lk = np.log10(kap)
        ax = CornerAxes(x_range=[0, 3, 1], y_range=[0, 4, 1], x_length=6.0, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -0.4, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1) for k in range(4)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.1) for k in range(5)])
        xn = label(r"condition number $\kappa$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"steps to a millionth of the starting error", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        dots_ = VGroup(*[Dot(ax.c2p(a, math.log10(b)), radius=0.07, color=GD) for a, b in zip(lk, it["gd"])])
        line = DashedVMobject(curve(ax, lk, np.log10(np.maximum(pr, 1)), UP_C, 2.5), num_dashes=30)
        rows = [[r"$\kappa$", r"derived $1 - 1/\kappa$", r"measured"]]
        for k_ in (10, 100, 1000):
            i = list(q["kappas"]).index(k_)
            rows.append([rf"${k_}$", rf"${rpred[i]:.4f}$", rf"${rate[i]:.4f}$"])
        tab = VGroup()
        for r_ in rows:
            tab.add(VGroup(*[label(c_, font_size=22, color=GREY_A if r_ is rows[0] else WHITE) for c_ in r_]))
        for r_ in tab:
            for j, c_ in enumerate(r_):
                c_.move_to([j * 1.9, 0, 0])
        tab.arrange(DOWN, buff=0.22)
        for j in range(3):
            xs_ = max(r_[j].width for r_ in tab)
            for r_ in tab:
                r_[j].set_x(j * 2.3 + xs_ / 2 - xs_ / 2)
        tab.move_to([3.9, 1.3, 0])
        th = label(r"the error's shrink per step, \ late in the run", font_size=22, color=GREY_A).next_to(tab, UP, buff=0.3)
        sl = label(rf"slope of the measured steps: \ ${slope:.2f}$", font_size=24, color=GD).next_to(tab, DOWN, buff=0.5)
        bl = label(r"dashed: \ $\kappa \ln(10^6)/2$, \ the worst case", font_size=20, color=UP_C).next_to(sl, DOWN, buff=0.2)
        tag = note(r"50 dimensions, \ curvatures spread evenly on a log scale from $\mu$ to $L$; \ computed").to_corner(DL, buff=0.25)
        i1000 = list(q["kappas"]).index(1000)
        close = all(abs(rate[i] - rpred[i]) < 2e-3 for i in range(1, len(rate)))
        with self.voiceover(
            "Check it. Quadratic valleys in fifty dimensions, with condition numbers from one to a thousand, and "
            "gradient descent with step one over L. <bookmark mark='a'/> The steps it needs, on log axes, rise along "
            f"a line of slope {slope:.2f}: "
            + ("close to one, in proportion to kappa, as derived. " if 0.8 < slope < 1.2 else
               "not the slope of one the worst case predicts. ")
            + "The dashed line is the worst case; these valleys do a little better, because only one direction is "
            "the slowest. <bookmark mark='b'/> Late in the run that slowest direction is all that is left, and the "
            + ("error shrinks per step by exactly the derived factor, one minus one over kappa, to three decimals: "
               f"at kappa a thousand, {rate[i1000]:.4f}."
               if close else
               f"error shrinks per step by {rate[i1000]:.4f} at kappa a thousand, against the derived "
               f"{rpred[i1000]:.4f}.")
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            self.play(Create(line))
            vo.wait_until("a")
            self.play(lag([FadeIn(d_, scale=0.5) for d_ in dots_], lag_ratio=0.15), FadeIn(sl), FadeIn(bl), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(th), lag([FadeIn(r_) for r_ in tab], lag_ratio=0.3), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        q = load("quad")
        pc = predict_card(r"On a valley with curvatures $1$ and $30$, \ the step $1/L = 1/30$ is safe. \ What happens "
                          r"at a step just over $2/L$?")
        ax = Axes(x_range=[-5, 1, 1], y_range=[-1.3, 1.3, 1], x_length=9.0, y_length=3.6, tips=False,
                  axis_config={"stroke_width": 0}).move_to(DOWN * 1.2)
        cont = contour_lines(ax, lambda x, y: 0.5 * (x * x + 30 * y * y), (-5, 1), (-1.3, 1.3), [0.3, 1.5, 4, 9, 16],
                             n=(120, 60), stroke_width=1.5)
        pg = np.asarray(q["path_gd"])
        pb = np.asarray(q["path_gd_big"])
        keep = np.abs(pb[:, 1]) < 1.3
        cut = int(np.argmin(keep)) if not keep.all() else len(pb)
        p1 = VMobject(color=GD, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in pg])
        p2 = VMobject(color=C.SURPRISE, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in pb[:max(cut, 2)]])
        lab = VGroup(label(r"$\eta = 1/L$", font_size=24, color=GD), label(r"$\eta = 2.06/L$", font_size=24, color=C.SURPRISE))
        lab.arrange(RIGHT, buff=1.0).next_to(ax, UP, buff=0.1)
        with self.voiceover(
            "Pause and predict. On a valley curving thirty times more steeply one way, a step of one over L is safe. "
            "What happens with a step just over two over L? <bookmark mark='a'/> The safe step slides down the long "
            "axis. <bookmark mark='b'/> The large one overshoots across the steep axis by more each time, and is "
            "thrown out of the valley. Along a direction of curvature lambda, a step multiplies the distance by one "
            "minus eta lambda; past two over lambda that factor is below minus one. Chapter five comes back to this "
            "edge."
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(pc.animate.scale(0.75).to_edge(UP, buff=0.3), Create(cont), FadeIn(lab[0]))
            self.play(Create(p1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(lab[1]), Create(p2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Steps grow with the condition number",
                          r"Gradient descent with $\eta = 1/L$ converges like $(1 - 1/\kappa)^k$ on a strongly convex "
                          r"loss, \ like $1/k$ on a convex one. \ Ill-conditioning is the enemy.",
                          r"Next: \ a heavy ball rolls through it in $\sqrt{\kappa}$ steps")
        with self.voiceover(
            "So: gradient descent's speed is set by the condition number, and ill-conditioned valleys are slow. "
            "Next, momentum, which turns kappa into its square root."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
