from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, CIRC, PART, SHORT, VAS, ask, fit_right, illustration, load


class ShortRate(VoiceoverScene):
    def construct(self):
        s = load("shortrate")
        self.card()
        self.models()
        self.fit(s)
        self.fans(s)

    def card(self):
        c = chapter_card(1, r"Short-rate models: Vasicek and CIR", r"What random process does the short rate follow?",
                         lit=(1977,), part=PART)
        with self.voiceover("Chapter one. Short-rate models: Vasicek, and Cox, Ingersoll and Ross."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def models(self):
        rows = [cmath(r"dr_t", r"=", r"a\,(b - r_t)\,dt + \sigma\,dW_t", font_size=44, colors={r"dr_t": VAS}),
                cmath(r"r_{t+\Delta}", r"\sim", r"\mathcal{N}\big(b + (r_t - b)e^{-a\Delta},\ \tfrac{\sigma^2}{2a}"
                      r"(1 - e^{-2a\Delta})\big)", font_size=38, colors={r"r_{t+\Delta}": VAS}),
                cmath(r"dr_t", r"=", r"a\,(b - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t", font_size=44, colors={r"dr_t": CIRC}),
                cmath(r"2ab", r"\ge", r"\sigma^2\quad\Rightarrow\quad r_t > 0", font_size=42, colors={r"2ab": CIRC})]
        whys = [why(r"Vasicek (1977): the short rate is pulled back toward $b$ at speed $a$, with constant noise: an "
                    r"Ornstein--Uhlenbeck process (Part 5)"),
                why(r"its exact transition is Gaussian, so a regression of next month on this month estimates it; "
                    r"nothing stops it going below zero"),
                why(r"Cox, Ingersoll and Ross (1985): the noise shrinks with the rate itself"),
                why(r"the Feller condition: the pull back to $b$ is strong enough to keep zero out of reach")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.8, buff=0.55, edge=6.9)
        with self.voiceover(
            "A term-structure model starts with the short rate: the rate for the next instant. Oldrich Vasicek, in "
            "1977, wrote it as a mean-reverting random walk: pulled back toward a long-run level b at speed a, with "
            "constant noise. <bookmark mark='a'/> Its transition over any interval is exactly normal, so fitting it is "
            "a regression of next month's rate on this month's. And a normal variable can be negative. "
            "<bookmark mark='b'/> In 1985 Cox, Ingersoll and Ross made the noise shrink as the rate falls, the square "
            "root of r. <bookmark mark='c'/> If the pull is strong enough relative to the noise, the Feller condition, "
            "zero is never reached."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def fit(self, s):
        t, x = np.asarray(s["t"]), np.asarray(s["x"]) * 100
        g = axes([1990, 2026], [0, 8.5], x_length=8.4, y_length=4.4, xlabel=r"year", ylabel=r"3-month bill, \%",
                 xticks=[1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, x, SHORT, stroke_width=2.5)
        v, c = s["vas"], s["cir"]
        side = VGroup(
            label(r"maximum likelihood, monthly, 1990--2025", font_size=19, color=GREY_A),
            MathTex(rf"\text{{Vasicek: }}a = {v['a']:.3f},\ b = {100 * v['b']:.2f}\%,\ \sigma = {100 * v['sigma']:.2f}\%",
                    font_size=24, color=VAS),
            MathTex(rf"\text{{CIR: }}a = {c['kappa']:.3f},\ b = {100 * c['theta']:.2f}\%,\ \sigma = {c['sigma']:.3f}",
                    font_size=24, color=CIRC),
            MathTex(rf"\text{{half-lives: }}{s['half_life_vas']:.1f}\ \text{{and}}\ {s['half_life_cir']:.1f}\ "
                    rf"\text{{years}}", font_size=24),
            MathTex(rf"2ab / \sigma^2 = {c['feller']:.2f}", font_size=26, color=CIRC),
            wrapped_label(rf"the long-run level comes out under 2\%: the bill was below 0.5\% in "
                          rf"{36 * np.mean(x < 0.5):.0f} of these 36 years", 4.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Here is the three-month Treasury bill, month by month since 1990: the closest thing to a short rate that "
            "trades. <bookmark mark='a'/> Fitted by maximum likelihood, Vasicek pulls the rate back with a half-life "
            f"of about {s['half_life_vas']:.0f} years, toward a level under two percent, because so many of these "
            "years were spent at zero. <bookmark mark='b'/> CIR finds almost the same pull, and its Feller ratio is "
            f"{c['feller']:.2f}: just above one, so zero is only barely out of reach. A model fitted to the past "
            "inherits the past's accidents."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[3]), FadeIn(side[5]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[4]))
        self.add(illustration(r"FRED: DTB3, month ends; Vasicek by exact AR(1), CIR by its non-central chi-square "
                              r"likelihood (the House's \texttt{sim.cir\_mle})"))
        self.wait(0.4)
        self.clear_scene()

    def fans(self, s):
        vp, cp = np.asarray(s["vas_paths"]) * 100, np.asarray(s["cir_paths"]) * 100
        tt = np.linspace(0, 10, vp.shape[1])
        g1 = axes([0, 10], [-4, 10], x_length=5.6, y_length=4.0, xlabel=r"years ahead", ylabel=r"Vasicek, \%",
                  xticks=[0, 5, 10], yticks=[-4, 0, 4, 8], font_size=13)
        g2 = axes([0, 10], [-4, 10], x_length=5.6, y_length=4.0, xlabel=r"years ahead", ylabel=r"CIR, \%",
                  xticks=[0, 5, 10], yticks=[-4, 0, 4, 8], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(DOWN * 0.5)
        f1 = VGroup(*[curve(g1.ax, tt, np.clip(p, -4, 10), VAS, stroke_width=1).set_stroke(opacity=0.35) for p in vp])
        f2 = VGroup(*[curve(g2.ax, tt, np.clip(p, -4, 10), CIRC, stroke_width=1).set_stroke(opacity=0.35)
                      for p in cp[:, :vp.shape[1]]])
        z1 = DashedLine(g1.ax.c2p(0, 0), g1.ax.c2p(10, 0), color=WHITE, stroke_width=1.5)
        z2 = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(10, 0), color=WHITE, stroke_width=1.5)
        head = label(rf"60 of 300 paths from today's bill rate, {100 * s['r0']:.2f}\%", font_size=24).to_edge(UP, buff=0.5)
        note_ = wrapped_label(rf"Vasicek: {100 * s['vas_neg_ever']:.0f}\% of paths go below zero within ten years. CIR: "
                              r"none can", 12.0, 20, BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now let each model run forward from today's bill rate for ten years. Vasicek's fan spreads quickly and "
            "settles around its long-run level; "
            f"<bookmark mark='a'/> about {100 * s['vas_neg_ever']:.0f} percent of its paths dip below zero at some point. "
            "<bookmark mark='b'/> CIR's fan is squeezed near zero, where its noise dies away. Which is right? Europe "
            "and Japan have since shown that rates can go negative; the next chapters keep Gaussian models, and "
            "chapter six prices what happens below zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), Create(z1), Create(z2))
            self.play(LaggedStart(*[Create(p) for p in f1], lag_ratio=0.02, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(note_))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in f2], lag_ratio=0.02, run_time=3))
        q = ask(r"Vasicek's fitted half-life is about six years. What does that say about how a 10-year yield should "
                r"react to a surprise in the short rate?")
        with self.voiceover("Pause on this: with a six-year half-life, how much should a ten-year yield react to a "
                            "surprise in today's short rate?"):
            self.play(FadeOut(note_), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
