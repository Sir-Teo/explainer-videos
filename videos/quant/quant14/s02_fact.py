from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, RV, VAR, load, real_data


class Fact(VoiceoverScene):
    def construct(self):
        s = load("skew")
        self.card()
        self.law(s)
        self.why()

    def card(self):
        c = chapter_card(1, r"The fact: an exploding skew", r"How fast does the skew grow as expiry nears?", part=PART)
        with self.voiceover("Chapter one. The fact: an exploding skew."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def law(self, s):
        T = np.asarray(s["T"])
        y = np.asarray(s["skew"])
        Tg = np.asarray(s["grid"])
        g = axes([np.log10(1 / 365), 0], [-1.6, 0.6], x_length=7.0, y_length=4.4, xlabel=r"years to expiry (log scale)",
                 ylabel=r"at-the-money skew $|\partial_k\sigma|$ (log scale)",
                 xticks=[np.log10(x) for x in (1 / 365, 7 / 365, 30 / 365, 0.25, 1.0)],
                 xfmt=lambda u: {0: "1y"}.get(round(u, 3), f"{365 * 10 ** u:.0f}d"), log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        for v in (0.05, 0.1, 0.3, 1, 3):
            g.add(label(f"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(np.log10(1 / 365), np.log10(v)), LEFT, buff=0.12))
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.07, color=WHITE) for a, b in zip(T, y) if b > 0.02])
        pw = curve(ax, np.log10(Tg), np.clip(np.log10(np.asarray(s["power_fit"])), -1.6, 0.6), MODEL_COL["power"],
                   stroke_width=2.5)
        sh = curve(ax, np.log10(Tg), np.clip(np.log10(np.asarray(s["shifted_fit"])), -1.6, 0.6), MODEL_COL["shifted"],
                   stroke_width=2.5)
        p, q = s["power"], s["shifted"]
        leg = legend([(WHITE, r"the Surface (Part 13)"), (MODEL_COL["power"], rf"power law: $T^{{-{p['a']:.2f}}}$"),
                      (MODEL_COL["shifted"], rf"bounded: $(T + {365 * q['eps']:.0f}\text{{d}})^{{-{q['a']:.2f}}}$")],
                     font_size=17).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = VGroup(
            MathTex(r"\psi(T) \sim T^{H - 1/2}", font_size=36, color=WHITE),
            wrapped_label(r"a rough volatility with Hurst exponent $H$ makes the skew grow like this as $T \to 0$ "
                          r"(Al\`os, Le\'on and Vives 2007; Fukasawa 2011); $H = \tfrac12$ is Brownian, smaller is "
                          r"rougher", 4.0, 19, GREY_A),
            wrapped_label(rf"the power law's slope says $H \approx {s['H_implied']:.2f}$; a skew that stays bounded below "
                          rf"about {365 * q['eps']:.0f} days fits these points better (log error {q['rmse_log']:.2f} "
                          rf"against {p['rmse_log']:.2f}): Guyon and El Amrani (2023) argue this for the S\&P 500",
                          4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        src = real_data(r"the Surface, 10 December 2025: SVI skew at each expiry")
        with self.voiceover(
            "Part thirteen ended with this picture: the at-the-money skew of the Surface against maturity, both on log "
            "scales. <bookmark mark='a'/> A straight line fits it, a power law, with exponent close to minus one half. "
            "Diffusions like Heston flatten out at short maturities; jumps explode like one over maturity. This is "
            "neither. <bookmark mark='b'/> In 2007 Elisa Alòs, Jorge León and Josep Vives showed what produces it: a "
            "volatility whose paths are rough, with a Hurst exponent H below one half, makes the skew grow like T to "
            "the power H minus a half. Read that way, Bitcoin's slope says H is nearly zero. <bookmark mark='c'/> But "
            "be careful. A skew that stops growing below about three weeks fits these points better, and Julien "
            "Guyon and Mehdi El Amrani argued in 2023 that the S&P 500's skew does the same: it is not a power law "
            "all the way down. The fact is real; its exact form is disputed."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                                                                         lag_ratio=0.1, run_time=2))
            vo.wait_until("a")
            self.play(Create(pw), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(sh), FadeIn(leg[2]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        rows = [cmath(r"\sigma_t", r"=", r"\sigma_0\exp\!\Big(\eta\,W^H_t\Big),\qquad W^H_t = \sqrt{2H}\int_0^t (t - s)^{H - 1/2}"
                      r"\,dW_s", font_size=34, colors={r"\sigma_t": VAR}),
                cmath(r"\mathbb{E}\big[(W^H_{t + \Delta} - W^H_t)^2\big]", r"\propto", r"\Delta^{2H}", font_size=36,
                      colors={r"\mathbb{E}\big[(W^H_{t + \Delta} - W^H_t)^2\big]": RV})]
        whys = [why(r"a Volterra process: today's volatility is a weighted sum of all past shocks, the recent ones weighted "
                    r"enormously when $H$ is small; not a Markov process"),
                why(r"over a short interval $\Delta$, it moves by about $\Delta^H$: far more than Brownian motion's "
                    r"$\Delta^{1/2}$ when $H \approx 0.1$. Rough paths look jagged at every scale")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "What does rough mean? Write log-volatility as a weighted sum of all past shocks, with a kernel that "
            "weights the recent ones enormously: t minus s to the power H minus a half. <bookmark mark='a'/> Over a "
            "short interval, such a process moves by about the interval to the power H. With H near a tenth, that is "
            "far more than Brownian motion's square root: the path is jagged at every scale, and over the next few "
            "days volatility can move a lot. That is exactly what short-dated options need to have a steep skew."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()
