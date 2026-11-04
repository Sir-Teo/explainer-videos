from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, fixed, illustration, load, polyline, predict


class LCP(VoiceoverScene, ThreeDScene):
    def construct(self):
        f = load("fd")
        lc = load("lcp")
        a = load("american")
        self.card()
        self.ringing(f)
        self.surface(lc)
        self.proof()
        self.solvers(lc)
        self.lab(a, lc)

    def card(self):
        c = chapter_card(13, r"Finite differences II: ringing, and the American put", r"What does a grid do with early "
                         r"exercise?", part=PART)
        with self.voiceover("Chapter thirteen. Finite differences, part two: Crank–Nicolson's ringing, and the American "
                            "put as a complementarity problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ringing(self, f):
        # the highest-frequency mode under Crank-Nicolson with a large lambda: g close to -1, flipping every step
        top = axes([0, 20], [-1.2, 1.2], x_length=5.6, y_length=1.9, xlabel=r"grid point", ylabel=r"one mode, step $n$",
                   xticks=[], yticks=[-1, 0, 1], font_size=14).to_corner(UL, buff=0.5)
        ta = top.ax
        lam, s = 20.0, 1.0
        gcn = (1 - 2 * lam * s) / (1 + 2 * lam * s)
        gim = 1 / (1 + 4 * lam * s)
        j = np.arange(21)
        mode = np.where(np.abs(j - 10) <= 3, (-1.0) ** j, 0.0)
        frames = [mode * gcn ** n for n in range(6)]
        cur = polyline(ta, j, frames[0], BAD, stroke_width=2.5, radius=0.04)
        tag = MathTex(rf"g_{{\text{{CN}}}} = {gcn:.3f}", font_size=28, color=BAD).next_to(top, RIGHT, buff=0.3)
        tag2 = MathTex(rf"g_{{\text{{implicit}}}} = {gim:.4f}", font_size=28, color=GOOD).next_to(tag, DOWN, buff=0.2)
        S = np.asarray(f["gamma_S"])
        ge = np.asarray(f["gamma_exact"])
        lo, hi = np.percentile(ge, 1) * 1.6, np.percentile(ge, 99) * 1.6
        g = axes([85, 115], [lo, hi], x_length=6.4, y_length=2.9, xlabel=r"spot", ylabel=r"gamma of a digital, a week to expiry",
                 xticks=[90, 100, 110], yticks=[], font_size=14).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        ax = g.ax
        cn = curve(ax, np.asarray(f["gamma"]["cn"]["S"]), np.clip(np.asarray(f["gamma"]["cn"]["gamma"]), lo, hi), BAD,
                   stroke_width=2.5)
        rn = curve(ax, np.asarray(f["gamma"]["cn+rannacher"]["S"]),
                   np.clip(np.asarray(f["gamma"]["cn+rannacher"]["gamma"]), lo, hi), GOOD, stroke_width=3)
        ex = DashedVMobject(curve(ax, S, ge, WHITE, stroke_width=2), num_dashes=50)
        leg = legend([(WHITE, r"exact"), (BAD, r"Crank--Nicolson"), (GOOD, r"with Rannacher's start")], font_size=16)
        leg.next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        side = wrapped_label(r"cash-or-nothing call, 800 price points, 4 time steps ($\lambda \gg 1$): two fully "
                             r"implicit half-steps first (Rannacher 1984) damp the jump and keep second order. "
                             r"Exponential fitting (Duffy) is another cure", 4.6, 17, GREY_A).next_to(leg, DOWN, buff=0.3)
        side.align_to(leg, LEFT)
        with self.voiceover(
            "Chapter twelve ended with Crank–Nicolson's weak spot. With a large time step, its highest frequencies "
            f"have a growth factor near minus one: here {gcn:.3f}. A spike on the grid does not decay; it flips sign "
            "every step. <bookmark mark='a'/> A payoff with a jump is full of such spikes. The price looks fine, "
            "but its gamma, the second derivative, rings around the strike, and gamma is what the desk hedges. "
            "<bookmark mark='b'/> The fix, from Rolf Rannacher in 1984: take the first steps fully implicit, where the "
            f"same mode is multiplied by {gim:.4f}, then switch to Crank–Nicolson. The ringing is gone, and the "
            "scheme stays second order."
        ) as vo:
            self.play(FadeIn(top), FadeIn(cur), FadeIn(tag))
            for n in range(1, 6):
                self.play(Transform(cur, polyline(ta, j, frames[n], BAD, stroke_width=2.5, radius=0.04)), run_time=0.5)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(ex), FadeIn(leg[0]), Create(cn), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(tag2), Create(rn), FadeIn(leg[2]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, lc):
        s = lc["surface"]
        S = np.asarray(s["S"])
        tau = np.asarray(s["tau"])
        A = np.asarray(s["american"])
        Eu = np.asarray(s["european"])
        ax = ThreeDAxes(x_range=[50, 150, 25], y_range=[0, 1, 0.25], z_range=[0, 50, 10], x_length=7.0, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def surf(Z, colors, op):
            from scipy.interpolate import RegularGridInterpolator
            fn = RegularGridInterpolator((tau, S), Z)
            sf = Surface(lambda u, v: ax.c2p(u, v, float(np.clip(fn((v, u)), 0, 50))), u_range=[50, 150], v_range=[0, 1],
                         resolution=(40, 20), fill_opacity=op, stroke_width=0.3, stroke_color="#0E1117",
                         checkerboard_colors=False)
            sf.set_fill_by_value(axes=ax, colorscale=list(zip(colors, [0, 15, 45])), axis=2)
            return sf

        am = surf(A, [QC.SPOT, QC.OPTION, QC.LOSS], 0.85)
        eu = surf(Eu, [GREY_D, GREY_C, GREY_B], 0.5)
        b = np.asarray(s["boundary"], float)
        ok = np.isfinite(b)
        fb = VMobject(stroke_color=QC.DELTA, stroke_width=5).set_points_as_corners(
            [ax.c2p(bb, tt, 100 - bb + 0.4) for bb, tt in zip(b[ok], tau[ok])])
        floor = VGroup(*[Line(ax.c2p(50, tt, 50), ax.c2p(bb, tt, 100 - bb), stroke_color=BAD, stroke_width=1.5,
                              stroke_opacity=0.7) for bb, tt in zip(b[ok][::3], tau[ok][::3])])
        hint = VGroup(label(r"across: spot $S$", font_size=21, color=GREY_A),
                      label(r"back: time to expiry $\tau$", font_size=21, color=GREY_A),
                      label(r"up: the American put", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        t1 = label(r"red: the stopping region, where $V = K - S$", font_size=22, color=BAD).to_corner(UR, buff=0.4)
        t2 = label(r"gold: the free boundary $S^*(\tau)$", font_size=22, color=QC.DELTA).next_to(t1, DOWN, buff=0.15)
        t2.align_to(t1, RIGHT)
        t3 = label(r"grey: the European put beneath", font_size=22, color=GREY_B).next_to(t2, DOWN, buff=0.15)
        t3.align_to(t1, RIGHT)
        nums = MathTex(rf"S^*(\tau = 1) \approx {b[ok][-1]:.0f}", font_size=28, color=QC.DELTA).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        fixed(self, hint, t1, t2, t3, nums)
        with self.voiceover(
            "Now early exercise on a grid. Here is the American put's value over spot and time to expiry, from the "
            "House's solver. <bookmark mark='a'/> On the left the surface lies flat on the payoff: in the red region "
            "it is optimal to exercise, and the value is exactly the strike minus the spot. <bookmark mark='b'/> Its "
            "edge is the free boundary, in gold: at expiry it sits at the strike, and with a year to go it has "
            f"retreated to about {b[ok][-1]:.0f}. <bookmark mark='c'/> Beneath, in grey, the European put, which "
            "cannot be exercised early. The gap between the two surfaces is the early-exercise premium of Part ten, "
            "largest deep in the money."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(am), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(floor), FadeIn(t1))
            vo.wait_until("b")
            self.play(Create(fb), FadeIn(t2), FadeIn(nums))
            self.move_camera(theta=-25 * DEGREES, run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(eu), FadeIn(t3))
            self.move_camera(theta=-75 * DEGREES, phi=72 * DEGREES, run_time=max(vo.remaining(0.5), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, am, eu, fb, floor)), FadeOut(hint),
                                                                  FadeOut(t1), FadeOut(t2), FadeOut(t3), FadeOut(nums)],
                         run_time=1.5)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"V \ge h,\quad \partial_\tau V - \mathcal{L}V \ge 0", r",\quad", r"(V - h)\,(\partial_\tau V - \mathcal{L}V) = 0",
                  font_size=32, colors={r",\quad": GREY_B}),
            cmath(r"Ax \ge b,\ \ x \ge g", r",\quad", r"(x - g)^\top(Ax - b) = 0,\qquad A = I - \theta\Delta\tau L_h", font_size=32),
            cmath(r"x_j", r"\leftarrow", r"\max\Big(g_j,\ x_j + \omega\,(\tilde x_j - x_j)\Big)", font_size=34,
                  colors={r"x_j": GOOD}),
            cmath(r"(A + P(x))\,x", r"=", r"b + P(x)\,g,\qquad P_{jj} = \rho\,\mathbf{1}_{x_j < g_j}", font_size=34,
                  colors={r"(A + P(x))\,x": QC.THETA}),
        ]
        whys = [why(r"hold or stop (Part 8's variational inequality): in the continuation region the PDE holds; in the "
                    r"stopping region $V = h$; one of the two inequalities is always an equality"),
                why(r"a linear complementarity problem at each time step (Brennan and Schwartz 1978 first priced the "
                    r"American put this way)"),
                why(r"projected SOR (Cryer 1971): a Gauss--Seidel sweep, over-relaxed, then clipped up to the payoff; "
                    r"it converges for an M-matrix and $0 < \omega < 2$"),
                why(r"the penalty method (Forsyth and Vetzal 2002): a huge penalty $\rho$ where $x$ falls below the "
                    r"payoff; Newton on the active set stops in a few iterations")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.6, edge=6.9)
        q = predict(r"Where on the surface is $\partial_\tau V = \mathcal{L}V$ \emph{not} satisfied?", width=4.8,
                    font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "In symbols: the value is at least the payoff, the pricing equation holds as an inequality, and at every "
            "point one of the two is an equality: hold, or stop. <bookmark mark='a'/> On the grid, each time step becomes "
            "a linear complementarity problem; Michael Brennan and Eduardo Schwartz priced the American put this way "
            "in 1978. <bookmark mark='b'/> Projected over-relaxation, from Colin Cryer in 1971, sweeps the grid, "
            "updating each point and clipping it up to the payoff. <bookmark mark='c'/> The penalty method of Peter "
            "Forsyth and Kenneth Vetzal adds a huge penalty wherever the solution dips below the payoff, and solves "
            "with Newton's method. Pause and predict: where is the pricing equation not satisfied? In the red "
            "region of the surface we just saw, where the value is the payoff."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def solvers(self, lc):
        res = np.asarray(lc["psor_trace"]["res"])
        g = axes([0.5, len(res) + 0.5], [-11, 0], x_length=6.0, y_length=3.8, xlabel=r"PSOR sweep (first time step)",
                 ylabel=r"size of the update ($\log_{10}$)", xticks=[1, 5, 10, 15], yticks=[-10, -5, 0], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        k = ValueTracker(1)

        def make():
            n = int(np.clip(k.get_value(), 1, len(res)))
            return polyline(ax, np.arange(1, n + 1), np.log10(res[:n]), GOOD, radius=0.05)

        tr = always_redraw(make)
        pen, ps, tree = lc["penalty"], lc["psor"], lc["tree"]
        fac = (res[0] / res[-1]) ** (1 / (len(res) - 1))
        side = VGroup(
            MathTex(rf"\text{{PSOR}},\ {ps['grid']}\times{ps['grid']}:\ {ps['price']:.4f}\ \ ({ps['time']:.2f}\,\text{{s}})",
                    font_size=28, color=GOOD),
            MathTex(rf"\text{{penalty}},\ {pen['grid']}\times{pen['grid']}:\ {pen['price']:.4f}\ \ ({pen['time']:.2f}\,\text{{s}})",
                    font_size=28, color=QC.THETA),
            MathTex(rf"\text{{Newton iterations per step: mean}}\ {pen['its_mean']:.1f},\ \text{{max}}\ {pen['its_max']}",
                    font_size=26, color=GREY_A),
            MathTex(rf"\text{{binomial tree, 2{{,}}000 steps:}}\ {tree['price']:.4f}", font_size=28, color=WHITE),
            wrapped_label(r"PSOR here is a pure-Python double loop; the penalty method is two sparse solves per step, so it "
                          r"affords twice the grid. Times: one core, best of three", 4.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Watch PSOR solve one time step. The size of each sweep's update, on a log scale: it falls by a factor of "
            f"about {fac:.0f} per sweep, and after {len(res)} sweeps the step is solved to round-off. "
            "<bookmark mark='a'/> Over the whole year: PSOR on a two-hundred-point grid gives "
            f"{ps['price']:.4f}. The penalty method on a grid twice as fine needs on average {pen['its_mean']:.0f} "
            f"Newton iterations per step and gives {pen['price']:.4f}, against {tree['price']:.4f} from a two "
            "thousand step tree. <bookmark mark='b'/> In this Python code the penalty method buys twice the grid "
            f"for {pen['time'] / ps['time']:.1f} times the time."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tr))
            self.play(k.animate.set_value(len(res)), run_time=4, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        tr.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    def lab(self, a, lc):
        card = lab_card(r"projected SOR", [
            "for _it in range(500):",
            "    err = 0.0",
            "    for j in range(nS - 1):",
            "        left = x[j - 1] if j > 0 else lo",
            "        right = x[j + 1] if j < nS - 2 else 0.0",
            "        y = (rhs[j] + 0.5*(a[j]*left + c[j]*right)) / (1 - 0.5*b[j])",
            "        y = max(payoff[j + 1], x[j] + omega * (y - x[j]))",
            "        err += (y - x[j]) ** 2",
            "        x[j] = y",
            "    if err < tol:",
            "        break",
        ], source="explainer/quant/house/engine.py  fd_american_put", width=7.6).to_corner(UL, buff=0.35)
        with self.voiceover(
            "The House's PSOR is eleven lines: the Crank–Nicolson update for one point, relaxed, and the single "
            "word max that makes it American. <bookmark mark='a'/> On a three-hundred-point grid it prices the put "
            f"at {a['fd']:.3f}, against {a['tree2000']:.3f} from the tree."
            " Next: grids in two dimensions, for Heston."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, ["fd_american_put(100, 100, 1, 0.2, 0.05, nS=300, nt=300)",
                                 f"PDE (PSOR)          {a['fd']:.4f}", f"tree (2,000 steps)  {a['tree2000']:.4f}"])
        self.wait(0.5)
        self.clear_scene()
