from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, pause, real_data


class Frontier(VoiceoverScene):
    def construct(self):
        rv = load("reversionary")
        self.card()
        self.reversionary(rv)
        self.papers()

    def card(self):
        c = chapter_card(18, r"Frontier, 2023--2026", r"Where is stochastic volatility research now?", part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def reversionary(self, rv):
        runs = rv["runs"]
        cols = [MODEL_COL["Heston"], IV, OPT, BAD]

        def smile_panel(day, lo, hi):
            a = axes([-0.35, 0.35], [lo, hi], x_length=4.2, y_length=3.2, xlabel=r"log-moneyness",
                     xticks=[-0.3, 0, 0.3], yticks=[round(lo + 0.1, 1), round((lo + hi) / 2, 1), round(hi - 0.1, 1)],
                     yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=13)
            s0 = runs[0]["smiles"][day]
            dots = VGroup(*[Dot(a.ax.c2p(x, np.clip(y, lo, hi)), radius=0.045, color=WHITE)
                            for x, y in zip(s0["k"], s0["q"]) if abs(x) <= 0.35])
            t = label(rf"{day} days", font_size=20, color=GREY_A).next_to(a, UP, buff=0.05)
            return VGroup(a, dots, t)

        p3, p9 = smile_panel("3", 0.3, 1.2), smile_panel("9", 0.3, 0.9)
        P = VGroup(p3, p9).arrange(RIGHT, buff=0.7).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)

        def curves(i):
            r = runs[i]
            out = VGroup()
            for pan, day, lo, hi in ((p3, "3", 0.3, 1.2), (p9, "9", 0.3, 0.9)):
                s = r["smiles"][day]
                kk = np.asarray(s["kk"])
                m = np.abs(kk) <= 0.35
                out.add(curve(pan[0].ax, kk[m], np.clip(np.asarray(s["iv"])[m], lo, hi), cols[i], stroke_width=3))
            info = VGroup(MathTex(rf"\kappa = {r['kappa']:.0f}", font_size=34, color=cols[i]),
                          MathTex(rf"\xi = {r['x'][3]:.1f},\ \ \xi/\sqrt\kappa = {r['xi_over_sqrt_kappa']:.2f}", font_size=28,
                                  color=cols[i]),
                          MathTex(rf"\text{{error: all}}\ {r['rmse_iv']:.2f},\ \ 3\text{{d}}\ {r['by_expiry']['3']:.1f}",
                                  font_size=26, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            info.to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
            return VGroup(out, info)

        cur = curves(0)
        r0, rN = runs[0], runs[-1]
        grow = rN["xi_over_sqrt_kappa"] / r0["xi_over_sqrt_kappa"]
        v1 = (f"The vol of vol it needs grows roughly like the square root of kappa: xi over root kappa goes from "
              f"{r0['xi_over_sqrt_kappa']:.2f} to {rN['xi_over_sqrt_kappa']:.2f}." if grow < 1.6 else
              f"The vol of vol it needs grows faster than the square root of kappa: xi over root kappa goes from "
              f"{r0['xi_over_sqrt_kappa']:.2f} to {rN['xi_over_sqrt_kappa']:.2f}.")
        better3 = rN["by_expiry"]["3"] < r0["by_expiry"]["3"]
        v2 = (f"The three-day smile improves, its error falling from {r0['by_expiry']['3']:.1f} to "
              f"{min(r['by_expiry']['3'] for r in runs):.1f} points, while the fit overall worsens from "
              f"{r0['rmse_iv']:.2f} to {rN['rmse_iv']:.2f}: the short end wants jumps, the long end does not." if better3 else
              f"The three-day error does not improve ({r0['by_expiry']['3']:.1f} to {rN['by_expiry']['3']:.1f}), and the "
              f"fit worsens overall from {r0['rmse_iv']:.2f} to {rN['rmse_iv']:.2f}.")
        cap = wrapped_label(r"Heston refitted with mean reversion held at 15, 30, 60 and 120; dots: the Surface's quotes", 6.0,
                            18, GREY_B).next_to(P, UP, buff=0.3).align_to(P, LEFT)
        pp = pause(r"Speed up mean reversion eightfold and keep the short skew. What must $\xi$ do?", width=4.6)
        pp.to_corner(DR, buff=0.3)
        src = real_data(r"the Surface; the House's calibrator with $\kappa$ fixed (zero-width bounds)", corner=DL)
        with self.voiceover(
            "Start with one computed tie-in. Eduardo Abi Jaber and Nathan De Carvalho showed in 2023 that Heston, "
            "with mean reversion sped up toward infinity and vol of vol scaled up with it, converges to jump "
            "processes of the normal inverse Gaussian type, or to rough-like limits: the reversionary Heston model. "
            "So hold kappa at fifteen, thirty, sixty and a hundred and twenty, and refit the other four to the "
            "Surface. <bookmark mark='p'/> Pause and predict: what must xi do to keep the short skew? "
            f"<bookmark mark='a'/> {v1} <bookmark mark='b'/> {v2} Our fitted Heston, at kappa fifteen, was already "
            "partway down this road: a diffusion straining to imitate jumps."
        ) as vo:
            self.play(FadeIn(P), FadeIn(cap), FadeIn(src), FadeIn(cur))
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp))
            per = max((vo.until("b") - 0.3) / (len(runs) - 1), 0.8)
            for i in range(1, len(runs)):
                self.play(Transform(cur, curves(i)), run_time=per)
        self.wait(0.4)
        self.clear_scene()

    def papers(self):
        cards = [
            history_card(2023, r"Abi Jaber, Illand and Li, \textit{Risk}",
                         r"The quintic Ornstein--Uhlenbeck model: volatility a degree-5 polynomial of one fast OU factor; "
                         r"joint SPX and VIX smiles with six effective parameters, Markovian and not rough.", color=QC.IDEA,
                         width=4.1),
            history_card(2023, r"Guyon and Mustapha, \textit{Risk}",
                         r"Neural joint S\&P 500/VIX calibration: a one-factor SLV with neural drift and diffusion fits SPX "
                         r"smiles, VIX futures and VIX smiles within bid--ask.", color=QC.IDEA, width=4.1),
            history_card(2024, r"Choi and Kwok, \textit{EJOR}",
                         r"Heston simulated with Poisson conditioning: exact-type sampling without Bessel draws "
                         r"(chapter 5).", color=QC.IDEA, width=4.1),
            history_card(2025, r"Reisinger and Tsianni, arXiv",
                         r"The calibrated particle SLV system: well-posed, propagation of chaos, strong rate one half "
                         r"(chapter 11).", color=QC.IDEA, width=4.1),
            history_card(2026, r"Wang, Despr\'es, Dureau and Buet-Golfouse, arXiv",
                         r"A neural operator returns the surface, Dupire's local vol, the leverage and the conditional "
                         r"moment at once: LSV calibration from 98.5 to 0.6 ms, exotics within a few tenths of a point of "
                         r"the particle method (synthetic tests, as reported).", color=QC.IDEA, width=4.1),
        ]
        top = VGroup(*cards[:3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        bot = VGroup(*cards[3:]).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        G = VGroup(top, bot).arrange(DOWN, buff=0.3)
        if G.height > 7.2:
            G.scale_to_fit_height(7.2)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            "Five papers from the last three years. Abi Jaber, Illand and Li's quintic Ornstein–Uhlenbeck model "
            "makes volatility a fifth-degree polynomial of a single fast factor, and fits S&P and VIX smiles "
            "together with six effective parameters, with no roughness at all: a Markovian answer to chapter "
            "fifteen's puzzle. <bookmark mark='a'/> Guyon and Mustapha fit both markets within bid–ask with a "
            "one-factor stochastic local volatility model whose drift and diffusion are neural networks. "
            "<bookmark mark='b'/> Choi and Kwok made Heston's exact simulation fast by conditioning on a Poisson "
            "variable. <bookmark mark='c'/> Reisinger and Tsianni gave the particle method its convergence theory. "
            "<bookmark mark='d'/> And this year, Wang and co-authors reported a neural operator that returns the "
            "whole local-stochastic calibration at once, from about a hundred milliseconds to under one, on "
            "synthetic tests. Part fourteen takes up rough volatility and the joint calibration; Part seventeen, "
            "neural calibrators and deep hedging."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(cards[4], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
