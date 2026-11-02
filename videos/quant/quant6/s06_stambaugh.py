from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, real_data, show_card


class Stambaugh(VoiceoverScene):
    def construct(self):
        c = load("stambaugh_cloud")
        s = load("stambaugh")
        iv = load("ivx")
        self.card()
        self.cloud(c, s)
        self.derive(s)
        self.real(s, iv)

    def card(self):
        c = chapter_card(5, r"Predictive regressions: Stambaugh's bias", r"Why do persistent predictors look so good?",
                         part=PART)
        with self.voiceover("Chapter five. Predictive regressions, and Stambaugh's bias."):
            show_card(self, c)
        self.play(FadeOut(c))

    def cloud(self, c, s):
        g = axes([-0.35, 0.12], [-0.3, 0.42], x_length=6.6, y_length=5.0, xlabel=r"$\hat\rho - \rho$: error in the "
                 r"predictor's persistence", ylabel=r"$\hat\beta - \beta$: error in the slope", xticks=[-0.3, -0.2, -0.1, 0, 0.1],
                 yticks=[-0.2, 0, 0.2, 0.4], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        Ts = ["50", "75", "100", "150"]

        def cloud_of(T, n=900):
            d = c["T"][T]
            x, y = np.asarray(d["drho"])[:n], np.asarray(d["dbeta"])[:n]
            return VGroup(*[Dot(ax.c2p(np.clip(a, -0.35, 0.12), np.clip(b, -0.3, 0.42)), radius=0.018, color=DATA_C,
                                fill_opacity=0.55) for a, b in zip(x, y)])

        def centre_of(T):
            d = c["T"][T]
            return d["mean_drho"], d["mean_dbeta"]
        cl = cloud_of("50")
        phi = c["phi"]
        xs = np.array([-0.33, 0.1])
        tilt = DashedLine(ax.c2p(xs[0], phi * xs[0]), ax.c2p(xs[1], phi * xs[1]), color=ALT, stroke_width=3)
        tl = MathTex(rf"\text{{slope }} \phi = \sigma_{{uv}}/\sigma_v^2 = {phi:.2f}", font_size=24, color=ALT).next_to(
            ax.c2p(xs[0], phi * xs[0]), RIGHT, buff=0.1).shift(UP * 0.25)
        zero_v = DashedLine(ax.c2p(0, -0.3), ax.c2p(0, 0.42), color=GREY_C, stroke_width=1.5)
        zero_h = DashedLine(ax.c2p(-0.35, 0), ax.c2p(0.12, 0), color=GREY_C, stroke_width=1.5)
        mx, my = centre_of("50")
        ctr = Dot(ax.c2p(mx, my), radius=0.09, color=EST)
        proj_v = DashedLine(ax.c2p(mx, my), ax.c2p(0, my), color=EST, stroke_width=2.5)
        proj_tick = Line(ax.c2p(-0.02, my), ax.c2p(0.02, my), color=EST, stroke_width=5)
        T_now = ValueTracker(50)
        T_ro = always_redraw(lambda: MathTex(rf"T = {int(round(T_now.get_value()))}\ \text{{years}}", font_size=34,
                                             color=WHITE).next_to(g, UP, buff=0.05).align_to(g, RIGHT))
        n_ro = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"{int(n_ro.get_value()):,}\ \text{{simulated samples}}".replace(",", "{,}"),
                                            font_size=24, color=GREY_B).next_to(g, UP, buff=0.05).align_to(g, LEFT))
        rows = VGroup(*[MathTex(rf"T = {T}:\ \ \mathbb{{E}}[\hat\beta - \beta] = {c['T'][T]['mean_dbeta']:+.3f}\ "
                                rf"\ (\text{{formula}}\ {c['T'][T]['formula']:+.3f})", font_size=24, color=EST)
                        for T in Ts]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        head = VGroup(
            label(r"a world where the yield predicts nothing:", font_size=21, color=GREY_A),
            MathTex(rf"\beta = 0,\ \rho = {c['rho']},\ \mathrm{{corr}}(u, v) = {c['corr']}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The dividend yield is persistent, and its surprises mirror return surprises: when prices jump, the yield "
            f"falls. On annual data the two shocks correlate at {s['corr_uv']:.2f}. Robert Stambaugh showed in 1999 "
            "what that does. <bookmark mark='a'/> Simulate a world where the yield predicts nothing, fifty years at a "
            "time, thousands of times. Each sample gives two errors: in the estimated persistence, across, and in the "
            "slope, up. <bookmark mark='b'/> The cloud is tilted: samples that underestimate persistence overestimate the "
            "slope, along a line of slope phi. <bookmark mark='c'/> And its centre sits left of zero: an autoregression's "
            "persistence is biased down, as Kendall showed in 1954. Follow the tilt to the vertical axis: the slope's "
            f"bias, {c['T']['50']['mean_dbeta']:+.3f}. <bookmark mark='d'/> Grow the sample from fifty years to a hundred "
            "and fifty. The cloud shrinks and its centre crawls toward the origin, roughly like one over T."
        ) as vo:
            self.play(FadeIn(g), Create(zero_v), Create(zero_h), FadeIn(side[0]))
            self.add(cnt)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in cl], lag_ratio=0.002), n_ro.animate.set_value(4000),
                      run_time=vo.until("b"), rate_func=linear)
            self.play(Create(tilt), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeIn(ctr), Create(proj_v), FadeIn(proj_tick), FadeIn(rows[0]))
            vo.wait_until("d")
            self.add(T_ro)
            for T, row in zip(Ts[1:], rows[1:]):
                mx, my = centre_of(T)
                self.play(Transform(cl, cloud_of(T)), ctr.animate.move_to(ax.c2p(mx, my)),
                          Transform(proj_v, DashedLine(ax.c2p(mx, my), ax.c2p(0, my), color=EST, stroke_width=2.5)),
                          proj_tick.animate.move_to(ax.c2p(0, my)), T_now.animate.set_value(int(T)), FadeIn(row),
                          run_time=1.6)
        cnt.clear_updaters()
        T_ro.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self, s):
        C_ = {r"\phi": ALT, r"\hat\beta - \beta": EST, r"\hat\rho - \rho": DATA_C}
        rows = [cmath(r"r_{t+1} = \alpha + \beta x_t + u_{t+1}", r",", r"\ x_{t+1} = \theta + \rho x_t + v_{t+1}",
                      font_size=34, colors=C_),
                cmath(r"u", r"=", r"\phi\, v + e,\quad \phi = \sigma_{uv}/\sigma_v^2,\ e \perp v", font_size=34,
                      colors=C_),
                cmath(r"\hat\beta - \beta", r"=", r"\phi\,(\hat\rho - \rho) + \frac{\sum \tilde x_t e_{t+1}}{\sum \tilde x_t^2}",
                      font_size=34, colors=C_),
                cmath(r"\mathbb{E}[\hat\beta - \beta]", r"=", r"\phi\,\mathbb{E}[\hat\rho - \rho] \approx -\phi\,"
                      r"\frac{1 + 3\rho}{T}", font_size=34, colors=C_),
                cmath(r"\text{annual}", r":", rf"\ {-s['corr_uv'] * s['sd_u'] / s['sd_v']:.2f} \cdot "
                      rf"\frac{{1 + 3 \cdot {s['rho']:.2f}}}{{{s['T']}}} = {s['bias']:+.3f}", font_size=34, colors=C_)]
        whys = [why(r"the predictive system: returns on a persistent predictor, the predictor an AR(1)"),
                why(r"project the return shock on the predictor shock; $e$ is what is left"),
                why(r"the same regressor $x_t$ in both equations: the slope's error inherits $\phi$ times the "
                    r"persistence's error"),
                why(r"the second term has mean zero ($e \perp v$); Kendall's (1954) bias of an AR(1) coefficient"),
                why(r"Shiller's annual data, 1871--2020: $\hat\phi$, $\hat\rho$ and $T$ from the regression itself")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.75, edge=6.8)
        with self.voiceover(
            "Four lines. The predictive system: returns on a persistent predictor, the predictor an autoregression. "
            "<bookmark mark='a'/> Project the return shock on the predictor's shock: phi times v, plus e unrelated to v. "
            "<bookmark mark='b'/> Both equations share the regressor, so the slope's error is phi times the persistence "
            "error, plus a term in e. <bookmark mark='c'/> That term averages zero, and Kendall's bias is minus one plus "
            "three rho over T: the tilted cloud, in symbols. <bookmark mark='d'/> On the annual data, phi is "
            f"{s['corr_uv'] * s['sd_u'] / s['sd_v']:.2f}, rho {s['rho']:.2f}, T {s['T']}: a bias of {s['bias']:+.3f}."
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

    def real(self, s, iv):
        a, mth, post = iv["annual"], iv["monthly"], iv["monthly_post1952"]
        rows = VGroup(
            label(r"The dividend yield, corrected", font_size=32),
            MathTex(rf"\text{{annual OLS: }} \hat\beta = {s['beta']:.3f}\ (t = {s['t']:.1f})", font_size=30),
            MathTex(rf"\text{{minus Stambaugh's bias: }} {s['beta_corrected']:.3f}", font_size=30, color=EST),
            MathTex(rf"\text{{Amihud--Hurvich (2004), augmented: }} {a['aug']['beta']:.3f}\ (t = {a['aug']['t']:.2f})",
                    font_size=30, color=EST),
            MathTex(rf"\text{{IVX (Kostakis et al.\ 2015), annual: }} p = {a['ivx']['p']:.2f}", font_size=30, color=ALT),
            MathTex(rf"\text{{IVX, monthly 1871--2020: }} p = {mth['ivx']['p']:.3f};\ \ \text{{since 1952: }} "
                    rf"p = {post['ivx']['p']:.3f}", font_size=30, color=ALT),
            wrapped_label(r"IVX instruments $x_t$ with a filtered version of its own changes, $z_t = \sum_j "
                          r"\rho_z^{t-j}\Delta x_j$, $\rho_z = 1 - 1/T^{0.95}$: less persistent than $x$ whatever "
                          r"$x$'s persistence, so the Wald test is $\chi^2(1)$ without knowing $\rho$. (The House's "
                          r"version omits the finite-sample correction.)", 11.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(UP, buff=0.45)
        src = real_data(r"Shiller's data: annual (January) and monthly, 1871--2020; nominal annual, real monthly returns")
        mono = "rejects" if mth["ivx"]["p"] < 0.05 else "does not reject"
        q = predict(r"If the predictor's shocks were positively correlated with returns, which way would the bias "
                    r"go?").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"The real regression: annual data, a slope of {s['beta']:.3f}, t of {s['t']:.1f}. <bookmark mark='a'/> "
            f"Subtract the bias, and {s['beta_corrected']:.3f} is left. Amihud and Hurvich's augmented regression adds "
            "the predictor's estimated shock as a second regressor, purging the bias inside the regression: "
            f"{a['aug']['beta']:.3f}, t of {a['aug']['t']:.2f}. <bookmark mark='b'/> Kostakis, Magdalinos and "
            "Stamatogiannis's IVX, from 2015, needs no persistence estimate: instrument the yield with a filtered "
            "version of its own changes, mildly persistent by construction, and the test is chi-squared either way. "
            f"Annual p-value: {a['ivx']['p']:.2f}. On monthly data the House's simplified IVX {mono} at five percent, p "
            f"of {mth['ivx']['p']:.3f}. <bookmark mark='c'/> A small, fragile slope, overstated by its usual t; Part "
            "seven takes up persistence itself. <bookmark mark='d'/> A question: what if the "
            "predictor's shocks and the return's shocks moved together? Then the bias would flip sign, and the "
            "usual t would understate the slope instead. A biased slope in sample is one problem. Next: does it "
            "forecast at all, out of sample?"
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(rows[6]))
            self.play(FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
