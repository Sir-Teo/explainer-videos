from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, ellipse_curve, load, predict, show_card


class MLE(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("mle")
        self.card()
        self.hill(m)
        self.derive()
        self.ellipses(m)

    def card(self):
        c = chapter_card(7, r"Maximum likelihood", r"How sharply does the data pick the parameters?", part=PART)
        with self.voiceover("Chapter seven. Maximum likelihood."):
            show_card(self, c)
        self.play(FadeOut(c))

    def hill(self, m):
        nus, scs, G = np.asarray(m["grid_nu"]), np.asarray(m["grid_scale"]), np.asarray(m["grid_ll"])
        Z = -np.sqrt(np.maximum(-G, 0.0))  # a hill, its top at the maximum; square-root heights
        zmin = float(Z.min())
        itp = RegularGridInterpolator((scs, nus), Z)
        f = lambda nu, sc: float(itp([[np.clip(sc, scs[0], scs[-1]), np.clip(nu, nus[0], nus[-1])]])[0]) / -zmin * 3 + 3  # noqa: E731
        ax = ThreeDAxes(x_range=[nus[0], nus[-1], 1], y_range=[scs[0], scs[-1], 0.2], z_range=[0, 3.2, 1], x_length=7,
                        y_length=5, z_length=3.2, tips=False, axis_config={"stroke_color": GREY_D,
                                                                            "include_ticks": False, "stroke_width": 1.5})
        surf = loss_surface(ax, f, (nus[0], nus[-1]), (scs[0], scs[-1]), resolution=(30, 24), z_lo=0, z_hi=3)
        path = np.asarray(m["path"])
        pts = [(float(np.clip(nu, nus[0], nus[-1])), float(np.clip(sc, scs[0], scs[-1]))) for _, sc, nu in path]
        k = ValueTracker(0)

        def ball():
            i = k.get_value()
            j = int(min(np.floor(i), len(pts) - 2))
            u = i - j
            x = pts[j][0] * (1 - u) + pts[j + 1][0] * u
            y = pts[j][1] * (1 - u) + pts[j + 1][1] * u
            return surface_ball(ax, f, x, y, color=YELLOW, radius=0.12)
        b = always_redraw(ball)
        trail = always_redraw(lambda: surface_path(ax, f, pts[:int(np.floor(k.get_value())) + 1] + [
            (pts[min(int(np.floor(k.get_value())), len(pts) - 2)][0] * (1 - (k.get_value() % 1))
             + pts[min(int(np.floor(k.get_value())) + 1, len(pts) - 1)][0] * (k.get_value() % 1),
             pts[min(int(np.floor(k.get_value())), len(pts) - 2)][1] * (1 - (k.get_value() % 1))
             + pts[min(int(np.floor(k.get_value())) + 1, len(pts) - 1)][1] * (k.get_value() % 1))],
            color=YELLOW, stroke_width=4))
        nll = np.asarray(m["nll_path"])
        def ro_at(i):
            return MathTex(rf"\text{{Newton step }} {i}:\ -\ell = {nll[i]:,.0f}".replace(",", "{,}"), font_size=30,
                           color=YELLOW).to_corner(UR, buff=0.4)
        ro = ro_at(0)
        hint = VGroup(
            label(r"log-likelihood of a Student $t$ for daily US returns", font_size=22, color=WHITE),
            label(rf"{m['n']:,} days, July 1926 -- December 2020".replace(",", "{,}"), font_size=20, color=GREY_B),
            label(r"across: degrees of freedom $\nu$; depth: scale $\sigma$", font_size=20, color=GREY_B),
            label(r"height: $-\sqrt{\ell_{\max} - \ell}$", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        res = MathTex(rf"\hat\nu = {m['nu']:.2f},\ \ \hat\sigma = {m['scale']:.3f}\%,\ \ \hat\mu = {m['mu']:.3f}\%",
                      font_size=32, color=EST).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-60 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, res)
        self.remove(hint, res)
        with self.voiceover(
            "Part one measured the fat tails of daily returns. Now fit them: suppose daily returns are Student's t, "
            "with a location, a scale, and degrees of freedom nu that set the tails. The log-likelihood adds the log "
            "density over twenty-five thousand days. <bookmark mark='a'/> Over nu and the scale it is a landscape, and "
            "maximum likelihood is its summit. <bookmark mark='b'/> Start from a bad guess, nearly normal, with nu of "
            f"{path[0][2]:.0f}, and climb by Newton's method: fit a parabola using the slope and curvature, jump to its "
            f"top. <bookmark mark='c'/> {len(path) - 1} steps, and nu is {m['nu']:.2f}: tails so fat the variance barely "
            f"exists. Part one's kurtosis of {m['kurtosis']:.0f} said the same."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(surf), run_time=2.5)
            self.move_camera(theta=-45 * DEGREES, run_time=vo.until("b"))
            self.add(trail, b)
            self.add_fixed_in_frame_mobjects(ro)
            per = max(vo.until("c") / (len(pts) - 1), 0.4)
            for i in range(1, len(pts)):
                self.play(k.animate.set_value(i), Transform(ro, ro_at(i)), run_time=per, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(res))
            self.move_camera(phi=8 * DEGREES, theta=-90 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        for x in (b, trail):
            x.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, b, trail)), FadeOut(ro),
                                                                  FadeOut(hint), FadeOut(res)], run_time=1.2)
        self.clear_scene()

    def derive(self):
        C_ = {r"\mathcal{I}": EST, r"H^{-1} J H^{-1}": ALT}
        rows = [cmath(r"\mathbb{E}_{\theta_0}[s_t(\theta_0)]", r"=", r"0,\quad s_t = \nabla_\theta \log f(x_t; \theta)",
                      font_size=36, colors=C_),
                cmath(r"\mathcal{I}", r"=", r"-\mathbb{E}[\nabla^2 \log f] = \mathbb{E}[s_t s_t^\top]", font_size=36,
                      colors=C_),
                cmath(r"0 = s(\hat\theta) \approx s(\theta_0) + \nabla^2\ell(\theta_0)(\hat\theta - \theta_0)",
                      r"\Rightarrow", r"\sqrt T(\hat\theta - \theta_0) \to N(0, \mathcal{I}^{-1})", font_size=34,
                      colors=C_),
                cmath(r"\text{misspecified:}\ \sqrt T(\hat\theta - \theta^*)", r"\to", r"N(0,\ H^{-1} J H^{-1})",
                      font_size=36, colors=C_),
                cmath(r"\text{Gaussian linear model:}", r"\ ", r"\hat\beta_{ML} = \hat\beta_{OLS}", font_size=36,
                      colors=C_)]
        whys = [why(r"differentiate $\int f(x;\theta)\,dx = 1$ under the integral: the score has mean zero"),
                why(r"differentiate again: the information-matrix equality, curvature equals the score's variance"),
                why(r"Taylor-expand the first-order condition; a CLT for the score, a law of large numbers for the "
                    r"Hessian"),
                why(r"quasi-ML: if the model is wrong, $H \neq J$ and chapter one's sandwich returns"),
                why(r"maximise a normal likelihood in $\beta$ and you minimise squared errors (AI Part 6)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.75, edge=6.8)
        with self.voiceover(
            "Why the summit estimates anything, and how precisely. Differentiate the fact that a density integrates to "
            "one: the score averages zero at the truth. <bookmark mark='a'/> Differentiate again: the expected curvature "
            "equals the score's variance, the information matrix, an equality that holds only if the model is right. "
            "<bookmark mark='b'/> Expand the first-order condition: a central limit theorem for the score, a law of large "
            "numbers for the curvature, and the estimate is normal with variance the inverse information. A sharp peak "
            "is a precise estimate. <bookmark mark='c'/> If the model is wrong, the two forms differ and the variance "
            "is a sandwich again. <bookmark mark='d'/> And with normal errors in a linear model, maximum likelihood is "
            "least squares."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def ellipses(self, m):
        g = axes([1.9, 3.0], [0.53, 0.62], x_length=6.2, y_length=4.6, xlabel=r"degrees of freedom $\nu$",
                 ylabel=r"scale $\sigma$, \% a day", xticks=[2.0, 2.4, 2.8], yticks=[0.55, 0.58, 0.61],
                 font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        ctr = np.array([m["nu"], m["scale"]])
        sw = lambda V: np.asarray(V)[::-1, ::-1]  # noqa: E731  (sigma, nu) -> (nu, sigma)
        clip = ((1.9, 3.0), (0.53, 0.62))
        Tf = ValueTracker(1.0)
        e_naive = always_redraw(lambda: ellipse_curve(ax, ctr, sw(m["V_naive"]) / Tf.get_value(), EST, clip=clip))
        e_opg = ellipse_curve(ax, ctr, sw(m["V_sandwich"]), GREY_B, stroke_width=2)
        e_hac = always_redraw(lambda: ellipse_curve(ax, ctr, sw(m["V_hac"]) / Tf.get_value(), ALT, clip=clip))
        dot = Dot(ax.c2p(*ctr), radius=0.06, color=WHITE)
        sn, ss, sh = m["se_naive"], m["se_sandwich"], m["se_hac"]
        side = VGroup(
            label(r"95\% regions for $(\nu, \sigma)$", font_size=24, color=WHITE),
            MathTex(rf"\text{{inverse Hessian: se}}(\hat\nu) = {sn[2]:.3f}", font_size=28, color=EST),
            MathTex(rf"\text{{sandwich, independent days: }} {ss[2]:.3f}", font_size=28, color=GREY_B),
            MathTex(rf"\text{{sandwich, scores' long-run variance: }} {sh[2]:.3f}", font_size=28, color=ALT),
            wrapped_label(r"volatility clusters, so the scores of nearby days are correlated: the iid Student $t$ is "
                          r"the wrong model, and only the dependence-robust sandwich admits it", 5.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        Tro = always_redraw(lambda: MathTex(rf"\text{{sample}} \times {Tf.get_value():.1f}", font_size=28,
                                            color=WHITE).next_to(g, UP, buff=0.05).align_to(g, RIGHT))
        q = predict(r"Double the sample. What happens to the ellipse's area?", width=5.0).to_corner(DR, buff=0.3)  # off the axis label
        ratio = sh[2] / sn[2]
        with self.voiceover(
            "Look down on the summit. The curvature at the top gives the naive confidence region, in gold: a narrow "
            f"ellipse, a standard error for nu of {sn[2]:.3f}. <bookmark mark='a'/> But is the model right? Daily returns "
            "are not independent draws from one t distribution: volatility clusters, calm weeks and violent weeks. The "
            "sandwich that only replaces the curvature with the scores' variance, still treating days as independent, "
            f"hardly moves: {ss[2]:.3f}. <bookmark mark='b'/> The scores of neighbouring days are correlated, though: a "
            "violent day is followed by violent days, and each pushes nu the same way. So the score's variance needs "
            "chapter two's long-run variance. With it, the standard error of nu is "
            f"{sh[2]:.3f}, {ratio:.1f} times the naive one, the pink ellipse. The naive standard error trusts a model "
            "the data reject; the estimate itself, a quasi-maximum-likelihood estimate, is still fine. "
            "<bookmark mark='c'/> Pause and predict: double the sample. What happens to the ellipse? Each axis shrinks "
            "by the square root of two, so its area halves. Quadruple it, and both axes halve."
            " Likelihood needs the whole distribution. Next: a method that needs only moments."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dot), Create(e_naive), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(e_opg), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(e_hac), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("c")
            self.add(Tro)
            self.play(FadeIn(q, shift=UP * 0.2))
            self.play(Tf.animate.set_value(2.0), run_time=2)
            self.play(Tf.animate.set_value(4.0), run_time=2)
        for x in (e_naive, e_hac, Tro):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
