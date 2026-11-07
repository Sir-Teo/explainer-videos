from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load


def region_image(mask, color, width, opacity=0.6):
    """A stability region (1 inside) as a translucent picture; row 0 of the mask is the bottom (Im z = -3)."""
    m = np.flipud(np.asarray(mask, float))
    rgb = np.ones(m.shape + (3,)) * np.array(ManimColor(color).to_rgb())
    rgba = np.concatenate([rgb, (m * opacity)[..., None]], -1)
    img = ImageMobject((rgba * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.stretch_to_fit_width(width)
    return img.stretch_to_fit_height(width * m.shape[0] / m.shape[1])


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 2.2 x 10^{-3}."""
    e = math.floor(math.log10(abs(v)))
    return rf"{v / 10 ** e:.{digits}f} \times 10^{{{e}}}"


class Odes(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.control()
        self.stiffness()
        self.regions()
        self.symplectic()
        self.drift()

    def card(self):
        card = chapter_card(13, r"Differential equations", r"How do we step through time and stay on course?",
                            lit=(1895, 1901, 1963), extra=((1895, r"Runge"), (1901, r"Kutta"),
                                                           (1963, r"Dahlquist: \ A-stability")), part=PART)
        with self.voiceover("Chapter thirteen. Differential equations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def steps(self):
        head = label(r"Euler, \ then Runge and Kutta", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 8, 2], x_length=5.4, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.move_to([-3.7, -0.1, 0])
        ticks = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in (0, 1, 2)],
                       *[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                         for v in (0, 4, 8)])
        exact = ax.plot(math.exp, x_range=[0, 2, 0.01], color=WHITE, stroke_width=3)
        h, z = 0.5, 0.5
        r4 = 1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24
        eu = [(k * h, (1 + z) ** k) for k in range(5)]
        rk = [(k * h, r4 ** k) for k in range(5)]
        eul = VGroup(VMobject(color=KERN, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in eu]),
                     *[Dot(ax.c2p(*p), radius=0.06, color=KERN) for p in eu])
        rkl = VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=YES) for p in rk])
        tags = VGroup(label(rf"Euler: \ {eu[-1][1]:.2f}", font_size=18, color=KERN),
                      label(rf"RK4: \ {rk[-1][1]:.3f}", font_size=18, color=YES),
                      label(rf"exact: \ $e^2 = {math.exp(2):.3f}$", font_size=18, color=WHITE))
        tags.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(0.15, 6.6), aligned_edge=UL)
        ill = note(r"illustrative: \ $y' = y$, \ $y(0) = 1$, \ four steps of $h = \tfrac12$", font_size=16).next_to(
            ax, DOWN, buff=0.4)
        rows = VGroup(
            cmath(r"y(t + h)", r"=", r"y(t)", r"+", r"h\, y'(t)", r"+", r"O(h^2)", font_size=30),
            cmath(r"y_{n+1}", r"=", r"y_n", r"+", r"h\, f(t_n, y_n)", font_size=30),
            MathTex(r"k_1 = f(t_n, y_n), \quad k_2 = f(t_n + \tfrac h2,\ y_n + \tfrac h2 k_1)", font_size=25),
            MathTex(r"k_3 = f(t_n + \tfrac h2,\ y_n + \tfrac h2 k_2), \quad k_4 = f(t_n + h,\ y_n + h k_3)",
                    font_size=25),
            cmath(r"y_{n+1}", r"=", r"y_n", r"+", r"\tfrac h6 (k_1 + 2k_2 + 2k_3 + k_4)", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.3, 0.35, 0])
        rows.align_to([-0.45, 0, 0], LEFT)
        whys = VGroup(label(r"Taylor's series", font_size=18, color=GREY_B),
                      label(r"Euler: \ drop the rest; \ global error $O(h)$", font_size=18, color=KERN),
                      label(r"RK4: \ four slopes per step; \ global error $O(h^4)$", font_size=18, color=YES))
        for w, rr in zip(whys, (rows[0], rows[1], rows[4])):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        with self.voiceover(
            "A differential equation gives the slope of its solution everywhere, and a solver walks along"
            " it. <bookmark mark='a'/> By Taylor's series, the value a step h later is the value now, "
            "plus h times the slope, plus a term of order h squared. <bookmark mark='b'/> Dropping the "
            "rest is Euler's method: on y prime equals y, four steps of a half reach five, not seven "
            "point three nine. <bookmark mark='c'/> Carl Runge and Wilhelm Kutta sampled the slope four "
            "times per step, so that the errors cancel up to h to the fourth. <bookmark mark='d'/> The "
            "same four steps reach seven point three eight."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(exact), FadeIn(tags[2]), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(Create(eul), FadeIn(tags[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            self.play(FadeIn(rows[4]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rkl], lag_ratio=0.2), FadeIn(tags[1]))
        self.wait(0.4)
        self.clear_scene()

    def control(self):
        head = label(r"Choosing the step", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\text{tol}": YES, r"\text{err}": NO}
        rows = VGroup(
            cmath(r"\text{err}", r"=", r"\|y^{(5)} - y^{(4)}\|", r"\approx", r"C h^5", colors=cols, font_size=32),
            cmath(r"C h_{\text{new}}^5", r"=", r"\text{tol}", colors=cols, font_size=32),
            cmath(r"h_{\text{new}}", r"=", r"h", r"\left(\frac{\text{tol}}{\text{err}}\right)^{1/5}", colors=cols,
                  font_size=32),
            cmath(r"h_{\text{new}}", r"=", r"0.9\,", r"h", r"\left(\frac{\text{tol}}{\text{err}}\right)^{1/5}",
                  colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.68).move_to([-3.4, 0.25, 0])
        whys = VGroup(
            wrapped_label(r"two answers, \ of orders 5 and 4, \ from the same seven slopes \ (Dormand and Prince, "
                          r"\ 1980)", 5.6, font_size=18, color=GREY_B),
            label(r"aim the next step's error at the tolerance", font_size=18, color=GREY_B),
            label(r"divide by the first line: \ $C$ cancels", font_size=18, color=GREY_B),
            label(r"a safety factor, \ and at most fivefold either way", font_size=18, color=YES),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        lines = ["while t < t1:", "    h = min(h, t1 - t)", "    K = seven_slopes(f, t, y, h)",
                 "    y5 = y + h * (b5 @ K)", "    y4 = y + h * (b4 @ K)",
                 "    err = max(abs(y5 - y4) / (tol + tol * abs(y)))", "    if err <= 1:",
                 "        t, y = t + h, y5       # accept", "    else:",
                 "        rejected += 1          # retry, smaller",
                 "    h *= min(5, max(0.2, 0.9 * err ** (-1 / 5)))"]
        code = code_block(lines, size=14)
        code[5].set_color(NO)
        code[10].set_color(YES)
        ct = label(r"our instrument's loop \ (abridged)", font_size=18, color=GREY_A)
        cg = VGroup(ct, code).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, 0.6, 0])
        foot = wrapped_label(r"the same method is SciPy's default, \ \texttt{RK45}, \ and MATLAB's \texttt{ode45}",
                             6.0, font_size=19, color=WHITE).next_to(cg, DOWN, buff=0.4).align_to(cg, LEFT)
        with self.voiceover(
            "How large a step? Let the method decide. <bookmark mark='a'/> The formulas of John Dormand "
            "and Peter Prince, from 1980, give two answers from the same seven slopes, of fifth and "
            "fourth order. Their difference estimates the error, which grows like h to the fifth. "
            "<bookmark mark='b'/> Ask for the next step's error to equal the tolerance. <bookmark "
            "mark='c'/> Divide, and the constant cancels: scale h by the fifth root of tolerance over "
            "error. <bookmark mark='d'/> Add a safety factor, and retry any step that fails. <bookmark "
            "mark='e'/> That is our instrument's loop, and the method behind SciPy's default solver and "
            "MATLAB's ode45."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(cg), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def stiffness(self):
        rows_ = load("stiff")["rows"]
        head = label(r"Stiffness", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\lambda": HEAD}
        eqs = VGroup(
            cmath(r"y'", r"=", r"\lambda", r"(y - \cos t) - \sin t", r",\quad y(0) = 0", colors=cols, font_size=30),
            cmath(r"y(t)", r"=", r"\cos t - e^{", r"\lambda", r"t}", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.5, 2.15, 0])
        ax = Axes(x_range=[0, 2, 0.5], y_range=[-0.5, 1.3, 0.5], x_length=5.2, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.next_to(eqs, DOWN, buff=0.55).set_x(-3.5)
        tk = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -0.5), DOWN, buff=0.1)
                      for v in (0, 1, 2)], label(r"$t$", font_size=18, color=GREY_B).next_to(ax.c2p(2, -0.5),
                                                                                           RIGHT, buff=0.1))
        curves = VGroup()
        for lam, c in ((-1.0, GREY_B), (-100.0, DATA)):
            curves.add(ax.plot(lambda t, lam=lam: math.cos(t) - math.exp(lam * t), x_range=[0, 2, 0.002],
                               color=c, stroke_width=3))
        cl = VGroup(label(r"$\lambda = -1$", font_size=17, color=GREY_B).next_to(ax.c2p(0.55, 0.25), DOWN,
                                                                               buff=0.1),
                    label(r"$\lambda = -100$: \ a transient, \ then just $\cos t$", font_size=17, color=DATA)
                    .move_to(ax.c2p(0.12, 1.2), aligned_edge=LEFT))
        top = 4.0
        bars = VGroup()
        for r in rows_:
            lam = r["lam"]
            name = label(rf"$\lambda = {lam:g}$" if abs(lam) < 1000 else rf"$\lambda = -10^{{{round(math.log10(-lam))}}}$",
                         font_size=19, color=HEAD)
            b1 = Rectangle(width=3.4 * math.log10(r["rk45_steps"]) / top, height=0.32, stroke_width=0,
                           fill_color=NO, fill_opacity=0.85)
            t1 = label(rf"{r['rk45_steps']:,} steps \ ({r['rk45_rejected']} rejected)", font_size=17, color=NO)
            b2 = Rectangle(width=3.4 * math.log10(r["backward_euler_steps"]) / top, height=0.32, stroke_width=0,
                           fill_color=YES, fill_opacity=0.85)
            t2 = label(rf"{r['backward_euler_steps']} steps, \ error ${sci(r['backward_euler_error'])}$",
                       font_size=17, color=YES)
            bars.add(VGroup(name, b1, t1, b2, t2))
        for k, g in enumerate(bars):
            y = 1.6 - 1.45 * k
            g[0].move_to([0.5, y, 0], aligned_edge=LEFT)
            g[1].move_to([0.5, y - 0.42, 0], aligned_edge=LEFT)
            g[3].move_to([0.5, y - 0.82, 0], aligned_edge=LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.12)
            g[4].next_to(g[3], RIGHT, buff=0.12)
        key = VGroup(label(r"adaptive RK45, \ tolerance $10^{-6}$", font_size=18, color=NO),
                     label(r"backward Euler", font_size=18, color=YES)).arrange(RIGHT, buff=0.5)
        key.next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        sub = note(r"steps on $[0, 2]$, \ log scale, \ computed", font_size=16).next_to(key, UP, buff=0.12).align_to(
            key, LEFT)
        foot = wrapped_label(r"\textbf{stiff}: \ a decay that is already over still sets the explicit method's step "
                             r"\ (the word is Curtiss and Hirschfelder's, \ 1952)", 6.0, font_size=19,
                             color=WHITE).next_to(ax, DOWN, buff=0.45).set_x(-3.4)
        with self.voiceover(
            "Now a harder kind of equation. <bookmark mark='a'/> Its solution is cosine t minus e to the "
            "lambda t: for large negative lambda, a brief transient, then just the smooth cosine. "
            "<bookmark mark='b'/> With lambda minus one, the adaptive method takes eleven steps; with "
            "minus a hundred, a hundred and thirty-two. <bookmark mark='c'/> With minus ten thousand, six"
            " thousand and sixty-seven, though after the first instant the answer is the same gentle "
            "cosine. <bookmark mark='d'/> Backward Euler takes two hundred steps every time, and its "
            "error even shrinks. This is stiffness: a decay that is already over still dictates an "
            "explicit method's step."
        ) as vo:
            self.play(FadeIn(head), Write(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(eqs[1]), Create(ax), FadeIn(tk))
            self.play(Create(curves), FadeIn(cl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(sub), FadeIn(key[0]))
            for g in bars[:2]:
                self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(key[1]), *[GrowFromEdge(g[3], LEFT) for g in bars], *[FadeIn(g[4]) for g in bars])
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def regions(self):
        st = load("stability")
        head = label(r"Stability regions", font_size=36).to_edge(UP, buff=0.3)
        top = cmath(r"y' = \lambda y", r",\quad", r"z = h\lambda", r":\quad", r"y_{n+1} = R(z)\, y_n", r",\quad",
                    r"|R(z)| \le 1", font_size=30).next_to(head, DOWN, buff=0.3)
        W = 3.2
        specs = [("euler", KERN, r"Euler", [r"R(z) = 1 + z"]),
                 ("rk4", LAM, r"RK4", [r"R(z) = 1 + z + \tfrac{z^2}{2} + \tfrac{z^3}{6} + \tfrac{z^4}{24}"]),
                 ("backward_euler", YES, r"backward Euler", [r"y_{n+1} = y_n + z\, y_{n+1}",
                                                             r"R(z) = \frac{1}{1 - z}"])]
        panels, titles, extra = Group(), VGroup(), VGroup()
        for k, (key, c, name, tex) in enumerate(specs):
            ax = Axes(x_range=[-4, 2, 1], y_range=[-3, 3, 1], x_length=W, y_length=W, tips=False,
                      axis_config={"stroke_color": GREY_B, "include_ticks": True, "tick_size": 0.04,
                                   "stroke_width": 1.5})
            ax.move_to([-4.4 + 4.4 * k, -0.85, 0])
            img = region_image(st[key], c, W).move_to(ax.c2p(-1, 0))
            frame = Rectangle(width=W, height=W, stroke_color=GREY_D, stroke_width=1).move_to(img)
            nm = label(name, font_size=20, color=c).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
            panels.add(Group(img, frame, ax, nm))
            t = MathTex(tex[0], font_size=22, color=c).next_to(frame, DOWN, buff=0.15)
            titles.add(t)
            if len(tex) > 1:
                extra.add(MathTex(tex[1], font_size=22, color=c).move_to(t))
        m4 = label(r"$-4$", font_size=14, color=GREY_B).next_to(panels[0][2].c2p(-4, 0), DOWN, buff=0.08)
        rk_edge = min(x for x, row in zip(st["x"], np.asarray(st["rk4"]).T) if row.any())
        foot = wrapped_label(rf"Euler reaches $-2$ on the real axis, \ RK4 about ${rk_edge:.1f}$: \ for "
                             rf"$\lambda = -10^4$ an explicit step must stay below a few ten-thousandths. \ "
                             rf"\textbf{{A-stable}}: \ the whole left half-plane \ (Dahlquist, \ 1963); \ an explicit "
                             rf"$R(z)$ is a polynomial, \ unbounded, \ so never", 12.6, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.22)
        with self.voiceover(
            "Why? Test each method on y prime equals lambda y, with z equal to h times lambda: each step "
            "multiplies y by some R of z. <bookmark mark='a'/> Euler's factor is one plus z: stable only "
            "in a disc around minus one. <bookmark mark='b'/> Runge–Kutta four's is its Taylor "
            "polynomial: a larger region, but still bounded. <bookmark mark='c'/> Backward Euler takes "
            "the slope at the new point, which gives one over one minus z, <bookmark mark='d'/> smaller "
            "than one in the whole left half-plane. Germund Dahlquist named this A-stability in 1963. An "
            "explicit method's factor is a polynomial, unbounded, so no explicit method is A-stable."
        ) as vo:
            self.play(FadeIn(head), Write(top))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), FadeIn(titles[0]), FadeIn(m4))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(titles[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2][1:]), FadeIn(titles[2]))
            vo.wait_until("d")
            self.play(ReplacementTransform(titles[2], extra[0]))
            self.play(FadeIn(panels[2][0]), run_time=1.5)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def symplectic(self):
        kp = load("kepler")
        head = label(r"Leapfrog: \ a symplectic method", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"p_{n+1/2}": HEAD}
        rows = VGroup(
            cmath(r"p_{n+1/2}", r"=", r"p_n + \tfrac h2\, a(q_n)", colors=cols, font_size=30),
            cmath(r"q_{n+1}", r"=", r"q_n + h\,", r"p_{n+1/2}", colors=cols, font_size=30),
            cmath(r"p_{n+1}", r"=", r"p_{n+1/2}", r"+ \tfrac h2\, a(q_{n+1})", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-3.9, 1.6, 0])
        whys = VGroup(label(r"half a kick", font_size=18, color=GREY_B),
                      label(r"a full drift", font_size=18, color=GREY_B),
                      label(r"the other half kick", font_size=18, color=GREY_B))
        for w, rr in zip(whys, rows):
            w.next_to(rr, RIGHT, buff=0.3)
        # an illustrative shear of a square in the (q, p) plane: area is kept
        C = np.array([-4.6, -1.7, 0])
        sq = Polygon(C + [-0.5, -0.5, 0], C + [0.5, -0.5, 0], C + [0.5, 0.5, 0], C + [-0.5, 0.5, 0],
                     color=DATA, fill_color=DATA, fill_opacity=0.3, stroke_width=2)

        def shear_p(s):        # p += s q (a kick, harmonic force)
            return sq.copy().apply_function(lambda P: C + np.array([P[0] - C[0], P[1] - C[1] + s * (P[0] - C[0]),
                                                                    0]))

        def shear_q(m, s):     # q += s p (a drift)
            return m.copy().apply_function(lambda P: C + np.array([P[0] - C[0] + s * (P[1] - C[1]), P[1] - C[1],
                                                                   0]))
        s1 = shear_p(-0.5)
        s2 = shear_q(s1, 0.9)
        qa = VGroup(Arrow(C + [-1.3, 0, 0], C + [1.4, 0, 0], buff=0, stroke_width=1.5, color=GREY_C,
                          max_tip_length_to_length_ratio=0.06),
                    Arrow(C + [0, -1.2, 0], C + [0, 1.2, 0], buff=0, stroke_width=1.5, color=GREY_C,
                          max_tip_length_to_length_ratio=0.06))
        ql = VGroup(MathTex(r"q", font_size=22, color=GREY_B).next_to(qa[0], RIGHT, buff=0.05),
                    MathTex(r"p", font_size=22, color=GREY_B).next_to(qa[1], UP, buff=0.05))
        sn = wrapped_label(r"each part is a shear of phase space: \ areas are kept exactly, \ so the step is "
                           r"\textbf{symplectic} \ (illustrative shapes)", 3.4, font_size=18, color=WHITE).next_to(
            C, RIGHT, buff=1.55)
        # the orbits
        S, O = 1.55, np.array([3.4, 0.0, 0])
        e = kp["e"]
        a_, b_ = 1.0, math.sqrt(1 - e * e)
        ell = DashedVMobject(ParametricFunction(lambda t: O + S * np.array([a_ * math.cos(t) - e, b_ * math.sin(t),
                                                                              0]), t_range=[0, TAU], color=GREY_B),
                             num_dashes=60)
        sun = Dot(O, radius=0.08, color=HEAD)
        rk = VMobject(color=NO, stroke_width=2.5).set_points_as_corners(
            [O + S * np.array([x, y, 0]) for x, y in kp["rk4"]["last_orbits"]])
        lf = VMobject(color=YES, stroke_width=2.5).set_points_as_corners(
            [O + S * np.array([x, y, 0]) for x, y in kp["leapfrog"]["last_orbits"]])
        okey = VGroup(label(r"the true orbit", font_size=17, color=GREY_B),
                      label(r"RK4: \ shrunk", font_size=17, color=NO),
                      label(r"leapfrog: \ right size, \ turned", font_size=17, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        okey.move_to([3.6, -2.55, 0])
        ocap = label(rf"orbits {kp['orbits'] - 2}--{kp['orbits']}, \ $e = {e:g}$, \ {kp['steps_per_orbit']} steps "
                     rf"per orbit, \ computed", font_size=17, color=GREY_A).move_to([3.4, 2.3, 0])
        with self.voiceover(
            "Some problems care less about one moment than about what is conserved over millions of "
            "steps: planets, molecules, particle beams. <bookmark mark='a'/> Leapfrog, which Loup Verlet "
            "used for molecules in 1967, gives the momentum half a kick, lets the position drift a full "
            "step, then finishes the kick. <bookmark mark='b'/> Each part is a shear of phase space, "
            "which keeps areas exactly: the step is symplectic. <bookmark mark='c'/> We ran an orbit of "
            "eccentricity one half for a thousand revolutions, a hundred steps each. <bookmark mark='d'/>"
            " Runge–Kutta four's orbit has shrunk. Leapfrog's has the right size, but has turned."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for rr, w in zip(rows, whys):
                self.play(FadeIn(rr), FadeIn(w), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(qa), FadeIn(ql), FadeIn(sq), FadeIn(sn))
            self.play(Transform(sq, s1))
            self.play(Transform(sq, s2))
            vo.wait_until("c")
            self.play(Create(ell), FadeIn(sun), FadeIn(ocap), FadeIn(okey[0]))
            vo.wait_until("d")
            self.play(Create(rk), FadeIn(okey[1]), run_time=2)
            self.play(Create(lf), FadeIn(okey[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def drift(self):
        kp = load("kepler")
        rk, lf = kp["rk4"]["energy_drift"], kp["leapfrog"]["energy_drift"]
        head = label(r"Energy over a thousand orbits", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 1000, 250], y_range=[-3.5, 1.5, 1], x_length=6.6, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.4, 0.2, 0])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1000, 0), color=GREY_D, stroke_width=1.5)
        xt = VGroup(*[label(f"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -3.5), DOWN, buff=0.1)
                      for v in (0, 250, 500, 750, 1000)])
        yt = VGroup(*[label(f"{v:+g}\\%" if v else "0", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT,
                                                                                          buff=0.1)
                      for v in (-3, -2, -1, 0, 1)])
        xl = label(r"orbits", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"relative energy error, \ once per orbit, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.15).align_to(ax, LEFT)
        c_rk = VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [ax.c2p(i + 1, 100 * v) for i, v in enumerate(rk)])
        c_lf = VMobject(color=YES, stroke_width=2).set_points_as_corners(
            [ax.c2p(i + 1, 100 * v) for i, v in enumerate(lf)])
        top_lf = max(abs(v) for v in lf)
        cross = next(i + 1 for i, v in enumerate(rk) if abs(v) > top_lf)
        vline = DashedLine(ax.c2p(cross, -3.5), ax.c2p(cross, 1.5), color=HEAD, stroke_width=2)
        vl = label(rf"orbit {cross}", font_size=17, color=HEAD).next_to(ax.c2p(cross, -3.5), UP, buff=0.12)
        vl.shift(RIGHT * 0.55)
        tr = label(rf"RK4: \ {100 * rk[-1]:.2f}\% and falling", font_size=18, color=NO).move_to(
            ax.c2p(980, -3.05), aligned_edge=RIGHT)
        tl = label(rf"leapfrog: \ never beyond {100 * top_lf:.2f}\%", font_size=18, color=YES).move_to(
            ax.c2p(980, 0.17), aligned_edge=RIGHT)
        cols = {r"\tilde H": YES}
        rows = VGroup(
            cmath(r"\tilde H", r"=", r"H + h^2 H_2 + h^4 H_4 + \cdots", colors=cols, font_size=30),
        ).move_to([4.3, 1.3, 0])
        why = wrapped_label(r"a symplectic method conserves a nearby energy $\tilde H$, \ up to exponentially small "
                            r"errors, \ for exponentially long times; \ so $H$ can only wobble around it", 4.4,
                            font_size=18, color=GREY_B).next_to(rows, DOWN, buff=0.2)
        bk = wrapped_label(r"backward error analysis again \ (Chapter 2): \ the method solves a nearby problem "
                           r"almost exactly \ (Hairer, \ Lubich and Wanner)", 4.4, font_size=18, color=HEAD).next_to(
            why, DOWN, buff=0.35).align_to(why, LEFT)
        with self.voiceover(
            "Here is the energy after every orbit. <bookmark mark='a'/> Runge–Kutta four starts out more "
            "accurate, but its error grows steadily, to three percent after a thousand orbits. <bookmark "
            "mark='b'/> Leapfrog's is about one percent, and never grows. <bookmark mark='c'/> After "
            "about three hundred and seventy orbits leapfrog is ahead, and the gap only widens. <bookmark"
            " mark='d'/> The reason is a theorem: a symplectic method almost exactly conserves a slightly"
            " different energy, a modified Hamiltonian, so the true energy can only wobble around it. "
            "<bookmark mark='e'/> It is chapter two's backward error analysis again: the method solves a "
            "nearby problem, nearly exactly."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(zero))
            vo.wait_until("a")
            self.play(Create(c_rk), FadeIn(tr), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(c_lf), FadeIn(tl), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(vline), FadeIn(vl))
            vo.wait_until("d")
            self.play(FadeIn(rows), FadeIn(why))
            vo.wait_until("e")
            self.play(FadeIn(bk))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
