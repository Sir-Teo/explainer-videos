from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load


class Lift(VoiceoverScene):
    def construct(self):
        L = load("lift")
        self.card()
        self.kernel(L)
        self.errors(L)

    def card(self):
        c = chapter_card(6, r"Markovian lifts", r"Can a rough model be made Markovian?", part=PART)
        with self.voiceover("Chapter six. Markovian lifts."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kernel(self, L):
        from scipy.special import gamma as G
        H = L["H"]
        a = H + 0.5
        t = np.exp(np.linspace(np.log(1e-3), np.log(1.0), 200))
        K = t ** (a - 1) / G(a)
        g = axes([-3, 0], [-0.5, 2.5], x_length=6.2, y_length=4.0, xlabel=r"lag $t$ (years, log scale)",
                 ylabel=r"kernel $K(t)$ (log scale)", xticks=[-3, -2, -1, 0], xfmt=lambda u: f"$10^{{{int(u)}}}$",
                 yticks=[0, 1, 2], yfmt=lambda u: f"$10^{{{int(u)}}}$", log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        exact = curve(ax, np.log10(t), np.log10(K), ROUGH, stroke_width=4)
        apps = VGroup()
        cols = [GREY_B, VAR, IV]
        for N, c in zip((2, 5, 20), cols):
            rN = 1 + 10 * N ** (-0.9)
            cc = (rN ** (1 - a) - 1) * rN ** ((a - 1) * (1 + N / 2)) / (G(a) * G(2 - a)) * rN ** ((1 - a) * np.arange(1, N + 1))
            x = (1 - a) / (2 - a) * (rN ** (2 - a) - 1) / (rN ** (1 - a) - 1) * rN ** (np.arange(1, N + 1) - 1 - N / 2)
            Ka = (cc[None, :] * np.exp(-x[None, :] * t[:, None])).sum(axis=1)
            apps.add(curve(ax, np.log10(t), np.clip(np.log10(np.maximum(Ka, 1e-3)), -0.5, 2.5), c, stroke_width=2.2))
        leg = legend([(ROUGH, rf"the rough kernel $t^{{H - 1/2}}/\Gamma(H + \tfrac12)$, $H = {H:.2f}$"),
                      (GREY_B, r"2 exponentials"), (VAR, r"5 exponentials"), (IV, r"20 exponentials")], font_size=16)
        leg.next_to(g, RIGHT, buff=0.35).align_to(g, UP)
        eq = MathTex(r"\frac{t^{\alpha - 1}}{\Gamma(\alpha)} \approx \sum_{i=1}^N c_i\,e^{-x_i t}", font_size=34).next_to(
            leg, DOWN, buff=0.45).align_to(leg, LEFT)
        note_ = wrapped_label(r"Abi Jaber and El Euch (2019): each exponential is one Heston-like factor; $N$ of them make a "
                              r"Markovian model with a closed-form Riccati system", 4.4, 19, GREY_A).next_to(eq, DOWN, buff=0.3).align_to(eq, LEFT)
        with self.voiceover(
            "A rough model has no Markovian state: today's volatility depends on the whole past. That makes simulation "
            "slow and dynamic hedging awkward. Eduardo Abi Jaber and Omar El Euch found a way back. The rough kernel, "
            "a power law, can be written as a mixture of exponentials. <bookmark mark='a'/> Cut the mixture to a "
            "finite number of terms, and each exponential becomes one mean-reverting factor, like Heston's. Two "
            "factors miss the short end badly; five do better; twenty follow the power law over three decades of "
            "time. <bookmark mark='b'/> The result, the lifted Heston model, is Markovian, with a closed-form "
            "characteristic function."
        ) as vo:
            self.play(FadeIn(g), Create(exact), FadeIn(leg[0]), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(a_), FadeIn(l_)) for a_, l_ in zip(apps, leg[1:])],
                                  lag_ratio=0.5, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def errors(self, L):
        rows = L["rows"]
        tab = VGroup(VGroup(label(r"factors $N$", font_size=24, color=GREY_A),
                            label(r"30-day smile error (vol points)", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.8))
        for r in rows:
            tab.add(VGroup(MathTex(str(r["N"]), font_size=30), MathTex(f"{r['iv_err']:.2f}", font_size=30,
                                                                         color=RV if r["iv_err"] < 0.5 else BAD)))
        for row in tab[1:]:
            row[0].move_to(tab[0][0].get_center() * RIGHT + row[0].get_center() * UP)
            row[1].move_to(tab[0][1].get_center() * RIGHT + row[1].get_center() * UP)
        tab[1:].arrange(DOWN, buff=0.25)
        for row in tab[1:]:
            row[0].set_x(tab[0][0].get_x())
            row[1].set_x(tab[0][1].get_x())
        tab[1:].next_to(tab[0], DOWN, buff=0.35)
        tab.move_to(LEFT * 2.2)
        side = wrapped_label(r"against rough Heston with $H = 0.1$, fitted to the Surface in chapter 4, solved exactly by the fractional "
                             r"Adams scheme; the lift is a Heston model with $N$ variance factors and no fractional calculus",
                             4.6, 20, GREY_A).to_edge(RIGHT, buff=0.6)
        src = illustration(r"13 strikes, $\pm 30\%$; the House's \texttt{lifted\_heston\_cf}")
        with self.voiceover(
            "How many factors are enough? Price the thirty-day smile of a rough Heston model with H of a tenth, fitted "
            "to the Surface in chapter four, exactly, and with lifts of growing size. <bookmark mark='a'/> One factor is a Heston model with the wrong memory, and "
            "misses. A handful of factors brings the error down, and twenty are close enough for a trading desk. The "
            "roughness was never magic: it is many time scales at once, and a model with enough of them behaves the "
            "same."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(side), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()
