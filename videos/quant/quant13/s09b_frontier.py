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
        self.play(FadeOut(c), run_time=0.35)

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
            f"""Abi Jaber and De Carvalho's reversionary Heston work studies specific fast-reversion and vol-of-vol scalings. The normal-inverse-Gaussian limit belongs to its H at or below minus one-half regime; it is not a limit of every faster-reverting Heston fit. Here we only refit four finite kappa settings to the same input marks. <bookmark mark='p'/> What happens to fitted xi? <bookmark mark='a'/> Xi over root kappa goes from {r0['xi_over_sqrt_kappa']:.2f} to {rN['xi_over_sqrt_kappa']:.2f}. <bookmark mark='b'/> Three-day error goes from {r0['by_expiry']['3']:.1f} to {rN['by_expiry']['3']:.1f} points, while overall error goes from {r0['rmse_iv']:.2f} to {rN['rmse_iv']:.2f}. This finite sweep illustrates a calibration trade-off. It neither establishes the paper's asymptotic scaling nor proves that the market needs jumps or rough volatility."""
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
        self.clear_scene(run_time=0.35)

    def papers(self):
        cards = [
            history_card(2023, r"Abi Jaber, Illand and Li, \textit{Risk}",
                         'Quintic OU: six effective parameters plus an input forward-variance curve; reported joint fits on selected SPX/VIX data.', color=QC.IDEA,
                         width=4.1),
            history_card(2023, r"Guyon and Mustapha, \textit{Risk}",
                         "Learned one-factor volatility with path dependence: reported SPX/VIX fits within bid--ask on the authors\\' datasets.", color=QC.IDEA, width=4.1),
            history_card(2024, r"Choi and Kwok, \textit{EJOR}",
                         r"Heston simulated with Poisson conditioning: exact-type sampling without Bessel draws "
                         r"(chapter 5).", color=QC.IDEA, width=4.1),
            history_card(2025, r"Reisinger and Tsianni, arXiv",
                         'Regularized fixed-bandwidth SLV: particle and Euler-time convergence have distinct Feller and regularity conditions.', color=QC.IDEA, width=4.1),
            history_card(2026, r"Wang, Despr\'es, Dureau and Buet-Golfouse, arXiv",
                         'Synthetic benchmark: 98.5 vs 0.6 ms including 0.53 ms Dupire input; excludes ingestion and training. Exotic point errors have no reported confidence intervals.', color=QC.IDEA, width=4.1),
        ]
        top = VGroup(*cards[:3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        bot = VGroup(*cards[3:]).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        G = VGroup(top, bot).arrange(DOWN, buff=0.3)
        if G.height > 7.2:
            G.scale_to_fit_height(7.2)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            (
            """Recent papers offer several approaches. The quintic OU model uses six effective parameters plus an input forward-variance curve; its reported joint fits use selected SPX and VIX data. <bookmark mark='a'/> Guyon and Mustapha report joint fits within bid–ask on their datasets using a learned volatility factor and path-dependent structure. This is a reported calibration result, not a universal fit guarantee. <bookmark mark='b'/> Choi and Kwok's 2024 Poisson-conditioning work includes an exact Heston scheme and approximate variants. <bookmark mark='c'/> Reisinger and Tsianni analyze regularized fixed-bandwidth particles; their particle and Euler-time results have distinct conditions, as chapter eleven explained. <bookmark mark='d'/> Wang and co-authors' 2026 synthetic benchmark reports about ninety-eight point five milliseconds for particles versus point six for neural inference, including point five three milliseconds of Dupire input work. It excludes quote ingestion and training. Reported exotic point errors lack confidence intervals, so closeness is not established statistical equivalence. These papers motivate further tests; they do not certify this implementation."""
        )
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
        self.clear_scene(run_time=0.35)
