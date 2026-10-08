from __future__ import annotations

from explainer import *  # noqa: F403
from videos.stochastic.common import boxed, hero, label, mult_table, note
from videos.stochastic.compute import ZOOM_T
from videos.stochastic.s03_roughness import ZoomView, brownian_sampler


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.finale()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        W = hero()
        y0 = float(W[int(round(ZOOM_T * (len(W) - 1)))])
        z = ValueTracker(0.0)
        view = ZoomView(brownian_sampler(), ZOOM_T, y0, 0.7, 2.5, 4, 2, z, width=5.4, height=3.6, yc=0.24, stroke_width=2)
        view.to_edge(RIGHT, buff=0.45).shift(UP * 0.4)
        vl = note(r"our path, still zooming in: $4\times$ in time, $2\times$ in space").next_to(view.frame, DOWN, buff=0.15)

        def item(head, formula, color):
            h = label(head, font_size=28, color=GREY_A)
            f = MathTex(formula, font_size=32, color=color)
            return VGroup(h, f).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        items = VGroup(
            item(r"Brownian steps scale like $\sqrt{dt}$, so", r"(dW)^2 = dt", C.QV),
            item(r"fair (left-endpoint) integrals:", r"\int_0^t W\,dW = \tfrac12 W_t^2 - \tfrac12 t", C.GAINS),
            item(r"It\^o's lemma: noise on curvature makes drift", r"df = f'\,dW + \tfrac12 f''\,dt", C.QV),
            item(r"noisy growth compounds at", r"\mu - \tfrac12\sigma^2", C.MEDIAN),
            item(r"paths $\to$ PDEs: Fokker--Planck forward, Feynman--Kac backward",
                 r"\partial_t p = -\partial_x(\mu p) + \tfrac12\partial_x^2(\sigma^2 p)", C.PDF),
            item(r"hedge the noise away; change the odds",
                 r"V_t + rSV_S + \tfrac12\sigma^2S^2V_{SS} = rV", C.OPTION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.6)
        for it in items:
            if it.get_right()[0] > view.frame.get_left()[0] - 0.3:
                it.scale_to_fit_width(view.frame.get_left()[0] - 0.3 - it.get_left()[0]).align_to(items, LEFT)

        with self.voiceover(
            "Let's put it all together. <bookmark mark='a'/> It started with one fact: over a short time d t, Brownian "
            "motion moves about root d t. That makes its paths rough at every scale, with infinite length, but their "
            "squared increments add up to exactly the elapsed time: d W squared equals d t."
        ) as vo:
            self.play(Create(view.frame), FadeIn(vl))
            self.add(view.curve, view.dot)
            vo.wait_until("a")
            self.play(FadeIn(items[0], shift=RIGHT * 0.2), z.animate.set_value(1.0), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "That one rule decides everything else. <bookmark mark='b'/> Integrals against noise have to be taken at the "
            "left end of each step, so they're fair games, and the integral of W d W picks up a minus one half t. "
            "<bookmark mark='c'/> The chain rule picks up a correction, one half f double prime d t: noise acting on "
            "curvature creates drift. <bookmark mark='d'/> That's why noisy growth compounds at mu minus one half sigma "
            "squared."
        ) as vo:
            self.play(z.animate.set_value(1.6), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(items[1], shift=RIGHT * 0.2), z.animate.set_value(2.6), run_time=vo.until("c"), rate_func=linear)
            self.play(FadeIn(items[2], shift=RIGHT * 0.2), z.animate.set_value(3.4), run_time=vo.until("d"), rate_func=linear)
            self.play(FadeIn(items[3], shift=RIGHT * 0.2), z.animate.set_value(4.0), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "<bookmark mark='e'/> Averaging Itô's lemma turns random paths into deterministic equations: Fokker–Planck "
            "pushes densities forward in time, and Kolmogorov and Feynman–Kac pull averages backward, which is how random "
            "walkers solve Laplace's equation. <bookmark mark='f'/> And in finance it all comes together: Black and "
            "Scholes hedged the noise away to price an option, and Girsanov's theorem explains why that price is an "
            "average in a world where the stock grows at the risk-free rate."
        ) as vo:
            vo.wait_until("e")
            self.play(FadeIn(items[4], shift=RIGHT * 0.2), z.animate.set_value(4.8), run_time=vo.until("f"), rate_func=linear)
            self.play(FadeIn(items[5], shift=RIGHT * 0.2), z.animate.set_value(5.6), run_time=vo.remaining(), rate_func=linear)
        view.curve.clear_updaters()
        view.dot.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def finale(self):
        rule = MathTex(r"(dW)^2", r"=", r"dt", font_size=96)
        rule[0].set_color(C.QV)
        rule[2].set_color(C.CLOCK)
        rb = boxed(rule, color=C.QV, buff=0.35).move_to(UP * 1.1)
        table = mult_table(40).next_to(rb, DOWN, buff=0.7)
        with self.voiceover(
            "All of it, from one line. <bookmark mark='t'/> d W squared equals d t. Thanks for watching."
        ) as vo:
            self.play(Write(rule), Create(rb[0]), run_time=1.5)
            vo.wait_until("t")
            self.play(FadeIn(table, lag_ratio=0.1), run_time=1.2)
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        hist = VGroup(
            label(r"Brown (1827) \quad Bachelier (1900) \quad Einstein (1905) \quad Langevin (1908) \quad Wiener (1923)",
                  font_size=24, color=GREY_A),
            label(r"Ornstein \& Uhlenbeck (1930) \quad Kolmogorov (1931) \quad It\^o (1944, 1951) \quad Kakutani (1944)"
                  r" \quad Cameron \& Martin (1944)", font_size=24, color=GREY_A),
            label(r"Kac (1949) \quad Donsker (1951) \quad Girsanov (1960) \quad Wong \& Zakai (1965) \quad Stratonovich (1966)"
                  r" \quad Black, Scholes \& Merton (1973)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.2)
        made = VGroup(
            label(r"Every path, histogram and number in this video is a seeded simulation, checked against the theory it "
                  r"illustrates.", font_size=24),
            label(r"Animated with Manim Community; narrated by Kokoro-82M; source: \texttt{videos/stochastic}", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18)
        g = VGroup(label(r"The ideas in this video", font_size=34), hist, made).arrange(DOWN, buff=0.5)
        self.play(FadeIn(g, shift=UP * 0.2))
        self.wait(5)
        self.play(FadeOut(g))
