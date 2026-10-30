from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, OPT_NAMES, PART, load, takeaway_card

GD, HB, NE = OPT_COLORS["gd"], OPT_COLORS["hb"], OPT_COLORS["nesterov"]


class Momentum(VoiceoverScene):
    def construct(self):
        self.card()
        self.ball()
        self.derive()
        self.nesterov()
        self.measure()
        self.takeaway()

    def card(self):
        c = chapter_card(2, r"The heavy ball and Nesterov", r"Can memory beat the condition number?", part=PART)
        with self.voiceover("Chapter two. The heavy ball, and Nesterov."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def ball(self):
        q = load("quad")
        hist = history_card(1964, r"Boris Polyak", r"\textit{Some methods of speeding up the convergence of iteration "
                            r"methods}: \ add a fraction of the last step to this one", width=5.4).to_corner(UL, buff=0.35)
        rule = cmath(r"x_{k+1}", "=", r"x_k - \eta\,\nabla f(x_k)", r"+ \beta\,(x_k - x_{k-1})",
                     colors={r"+ \beta\,(x_k - x_{k-1})": HB}, font_size=36)
        rule.next_to(hist, RIGHT, buff=0.5).align_to(hist, UP).shift(DOWN * 0.3)
        keep_in_frame(rule)
        mom = brace_note(term(rule, r"+ \beta\,(x_k - x_{k-1})"), r"momentum: \ the last step, again", color=HB,
                         font_size=22)
        ax = Axes(x_range=[-5, 1, 1], y_range=[-1.2, 1.2, 1], x_length=10.0, y_length=4.0, tips=False,
                  axis_config={"stroke_width": 0}).move_to(DOWN * 1.6)
        cont = contour_lines(ax, lambda x, y: 0.5 * (x * x + 30 * y * y), (-5, 1), (-1.2, 1.2), [0.3, 1.5, 4, 9, 16],
                             n=(120, 60), stroke_width=1.5)
        paths = {k: VMobject(color=c_, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in np.asarray(q[f"path_{k}"])])
                 for k, c_ in (("gd", GD), ("hb", HB))}
        dots = {k: Dot(ax.c2p(*np.asarray(q[f"path_{k}"])[0]), radius=0.08, color=paths[k].get_color()) for k in paths}
        lab = VGroup(label(r"gradient descent, \ $\eta = 1/L$", font_size=22, color=GD),
                     label(r"heavy ball, \ tuned for $\kappa = 30$", font_size=22, color=HB)).arrange(RIGHT, buff=0.8)
        lab.next_to(ax, DOWN, buff=0.05)
        tag = note(r"the valley of Chapter 1, \ curvatures $1$ and $30$; \ $60$ steps each; \ computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 1964 Boris Polyak, in Moscow, asked how to speed gradient descent up, and answered with physics: "
            "give the walker mass. <bookmark mark='a'/> Each step adds a fraction beta of the previous step. "
            "<bookmark mark='b'/> On the steep axis, successive steps point in opposite directions, so the memory "
            "cancels them out; on the long, gentle axis they all point the same way, so the memory adds them up. "
            "<bookmark mark='c'/> A heavy ball rolls along the valley instead of rattling across it."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2), Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(mom))
            vo.wait_until("b")
            self.play(Create(cont), FadeIn(tag), FadeIn(lab[0]), FadeIn(dots["gd"]))
            self.play(Create(paths["gd"]), MoveAlongPath(dots["gd"], paths["gd"].copy()), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(lab[1]), FadeIn(dots["hb"]))
            self.play(Create(paths["hb"]), MoveAlongPath(dots["hb"], paths["hb"].copy()), run_time=2.5, rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"one direction of the valley, \ curvature $\lambda$", font_size=30).to_edge(UP, buff=0.3)
        cl = {r"\beta": HB, r"\sqrt{\beta}": HB}
        rows = [
            cmath(r"x_{k+1}", "=", r"(1 + \beta - \eta\lambda)\,x_k - \beta\,x_{k-1}", font_size=34),
            cmath(r"z^2", "=", r"(1 + \beta - \eta\lambda)\,z - \beta", font_size=34),
            cmath(r"|z|", "=", r"\sqrt{\beta}", r"\quad \text{when } (1 + \beta - \eta\lambda)^2 \le 4\beta", font_size=34,
                  colors=cl),
            cmath(r"1 + \beta - \eta\mu", "=", r"2\sqrt{\beta}, \quad 1 + \beta - \eta L = -2\sqrt{\beta}", font_size=34),
            cmath(r"\sqrt{\beta}", "=", r"\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}", r",\quad \eta = \frac{4}{(\sqrt{L} + \sqrt{\mu})^2}",
                  font_size=34, colors=cl),
            cmath(r"k", r"\approx", r"\tfrac{\sqrt{\kappa}}{2}\,\ln(1/\varepsilon)", font_size=36),
        ]
        whys = [why(r"$\nabla f = \lambda x$ along it"), why(r"try $x_k = z^k$"),
                why(r"complex roots: \ a spiral, \ shrinking by $\sqrt{\beta}$"),
                why(r"make every $\lambda$ in $[\mu, L]$ spiral"),
                why(r"solve the two"), why(r"$\sqrt{\beta} \approx 1 - 2/\sqrt{\kappa}$")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.8, buff=0.5, edge=6.9)
        thm = theorem_card(r"The heavy ball on a quadratic", r"Tuned to $[\mu, L]$, \ every direction shrinks by "
                           r"$\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ per step: \ $\sqrt{\kappa}$ in place of $\kappa$.",
                           who=r"B.~Polyak (1964)", width=7.4, font_size=24).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why does it work, and how fast? On a quadratic, every direction of the valley is separate. "
            "<bookmark mark='a'/> Along a direction of curvature lambda, the update is a recurrence in the last "
            "two positions. <bookmark mark='b'/> Try powers of a number z, and z must solve a quadratic equation. "
            "<bookmark mark='c'/> When its roots are complex, the position spirals inward, and shrinks by exactly the "
            "square root of beta every step, whatever lambda is. <bookmark mark='d'/> So choose eta and beta to "
            "put every curvature between mu and L into that spiralling regime: the two ends of the range just on "
            "its edge. <bookmark mark='e'/> Solving, the square root of beta is root kappa minus one over root kappa "
            "plus one. <bookmark mark='f'/> That is about one minus two over root kappa: the steps now grow with the "
            "square root of the condition number. A thousand becomes about thirty."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                step(k)
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nesterov(self):
        q = load("quad")
        hist = history_card(1983, r"Yurii Nesterov", r"\textit{A method for solving the convex programming problem with "
                            r"convergence rate $O(1/k^2)$}: \ take the gradient where momentum is about to carry you",
                            width=5.6).to_corner(UL, buff=0.35)
        rule = VGroup(cmath(r"y_k", "=", r"x_k + \beta\,(x_k - x_{k-1})", colors={r"y_k": NE}, font_size=34),
                      cmath(r"x_{k+1}", "=", r"y_k - \eta\,\nabla f(y_k)", colors={r"y_k": NE}, font_size=34))
        rule.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hist, DOWN, buff=0.45).align_to(hist, LEFT)
        ks = np.asarray(q["conv_k"], float)
        sel = np.unique(np.round(np.geomspace(1, len(ks), 120)).astype(int)) - 1
        lk = np.log10(ks[sel])
        gd, ne = np.asarray(q["conv_gd"])[sel], np.asarray(q["conv_nesterov"])[sel]
        bn = np.asarray(q["bound_nesterov"])[sel]
        y0 = math.floor(np.log10(ne.min())) - 0.2
        y1 = math.ceil(np.log10(bn.max()))
        ax = CornerAxes(x_range=[0, lk.max(), 1], y_range=[y0, y1, 1], x_length=5.6, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.4, -0.3, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, y0), DOWN, buff=0.1)
                      for k in range(0, int(lk.max()) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.1)
                      for k in range(math.ceil(y0), y1 + 1, 2)])
        yn = label(r"$f(x_k) - f^*$, \ the convex quadratic of Chapter 1", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        c_gd = curve(ax, lk, np.log10(gd), GD, 3)
        c_ne = curve(ax, lk, np.log10(ne), NE, 3.5)
        b_ne = DashedVMobject(curve(ax, lk, np.log10(bn), C.SURPRISE, 2.2), num_dashes=40)
        lg = VGroup(label(r"gradient descent", font_size=20, color=GD), label(r"Nesterov, \ $\beta_k = \frac{k}{k+3}$",
                                                                              font_size=20, color=NE),
                    label(r"the bound $2L\|x_0 - x^*\|^2/(k+1)^2$", font_size=20, color=C.SURPRISE))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax.c2p(0, y0), UR, buff=0.15)
        held = bool((np.asarray(q["conv_nesterov"]) <= np.asarray(q["bound_nesterov"]) * (1 + 1e-9)).all())
        ratio = float(np.asarray(q["conv_gd"])[-1] / np.asarray(q["conv_nesterov"])[-1])
        low = label(r"no method that only sees gradients can do better \\ in the worst case \ (Nemirovski \& Yudin)",
                    font_size=20, color=GREY_A).to_edge(DOWN, buff=0.25).set_x(-3.4)
        said1 = (f"<bookmark mark='b'/> On Chapter 1's convex quadratic it stays under its bound, and after "
            f"{len(ks):,} steps it is {ratio:.0f} times closer than gradient descent. "
            if held else
            f"<bookmark mark='b'/> On Chapter 1's convex quadratic, after {len(ks):,} steps, it is {ratio:.0f} times "
            "closer than gradient descent. ")
        with self.voiceover(
            "In 1983 Yurii Nesterov, also in Moscow, changed one thing: take the gradient not where you are, but "
            "where momentum is about to carry you. <bookmark mark='a'/> With that look-ahead, the acceleration is "
            "guaranteed on every smooth convex function, not only on quadratics: the gap falls like one over k "
            "squared instead of one over k. "
            + said1
            + "<bookmark mark='c'/> And Arkadi Nemirovski and David Yudin had shown that no method using only "
            "gradients can do better in the worst case: Nesterov's rate is optimal."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2), Write(rule))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yn), Create(b_ne), FadeIn(lg[2]))
            vo.wait_until("b")
            self.play(Create(c_gd), FadeIn(lg[0]), run_time=1.5)
            self.play(Create(c_ne), FadeIn(lg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(low))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        q = load("quad")
        kap = np.asarray(q["kappas"], float)
        lk = np.log10(kap)
        ax = CornerAxes(x_range=[0, 3, 1], y_range=[0, 4, 1], x_length=6.0, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -0.4, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1) for k in range(4)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.1) for k in range(5)])
        xn = label(r"condition number $\kappa$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"steps to a millionth of the starting error", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        groups, rows = VGroup(), VGroup()
        for m, col in (("gd", GD), ("hb", HB), ("nesterov", NE)):
            it = np.asarray(q[f"iters_{m}"], float)
            groups.add(VGroup(curve(ax, lk, np.log10(it), col, 2.5),
                              *[Dot(ax.c2p(a, math.log10(b)), radius=0.06, color=col) for a, b in zip(lk, it)]))
            i = list(q["kappas"]).index(1000)
            rows.add(VGroup(label(OPT_NAMES[m], font_size=24, color=col),
                            label(rf"slope ${q[f'slope_{m}']:.2f}$; \ at $\kappa = 1000$: \ ${int(it[i]):,}$ steps".replace(",", "{,}"),
                                  font_size=22, color=col)).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 1.0, 0])
        i = list(q["kappas"]).index(1000)
        rh, rhp = q["rate_hb"][i], q["rate_pred_hb"][i]
        rn, rnp = q["rate_nesterov"][i], q["rate_pred_nesterov"][i]
        rates = label(rf"per step at $\kappa = 1000$: \ heavy ball ${rh:.4f}$ \ (derived ${rhp:.4f}$); \\ Nesterov "
                      rf"${rn:.4f}$ \ (derived ${rnp:.4f}$)", font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.45)
        keep_in_frame(rates)
        caveat = label(r"on general convex losses the heavy ball can cycle forever \\ (Lessard, Recht \& Packard, "
                       r"2016); \ Nesterov's version has the proof", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        sh, sn, sg = float(q["slope_hb"]), float(q["slope_nesterov"]), float(q["slope_gd"])
        it_g, it_h, it_n = (int(q[f"iters_{m}"][i]) for m in ("gd", "hb", "nesterov"))
        said2 = ("close to one half, the square root of kappa. " if max(sh, sn) < 0.7 else "well below gradient descent's. ")
        with self.voiceover(
            "Back to Chapter 1's fifty-dimensional valleys, now with momentum. <bookmark mark='a'/> Gradient descent "
            f"rises with slope {sg:.2f}. <bookmark mark='b'/> The heavy ball and Nesterov rise with slopes "
            f"{sh:.2f} and {sn:.2f}: "
            + said2
            + f"At kappa a thousand that is {it_g:,} steps against {it_h:,} and {it_n:,}. <bookmark mark='c'/> And "
            f"late in the run the heavy ball shrinks the error by {rh:.4f} per step, against {rhp:.4f} derived; "
            f"Nesterov by {rn:.4f}, against {rnp:.4f}. "
            "<bookmark mark='d'/> One warning. The heavy ball's guarantee is for quadratics: on other convex losses "
            "there are examples where it circles forever. Nesterov's form is the one with a proof."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(groups[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(groups[1]), FadeIn(rows[1]))
            self.play(Create(groups[2]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rates))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Momentum turns $\kappa$ into $\sqrt{\kappa}$",
                          r"A remembered velocity cancels the zigzag and accumulates the slope: \ on a quadratic, "
                          r"$\sqrt{\kappa}$ steps where gradient descent needs $\kappa$.",
                          r"Next: \ gradients we can only estimate")
        with self.voiceover(
            "So momentum is memory: it cancels the zigzag and accumulates the slope, and turns kappa into its square "
            "root. But every gradient so far was exact. Real training can only estimate it."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
