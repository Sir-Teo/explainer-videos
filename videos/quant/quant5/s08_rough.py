from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, real_data


class Rough(VoiceoverScene):
    def construct(self):
        f = load("fbm")
        r = load("rough")
        self.card()
        self.fbm(f)
        self.bitcoin(r)
        self.signature()

    def card(self):
        c = chapter_card(7, r"Beyond semimartingales: rough paths and signatures", r"How rough is volatility?",
                         part=PART)
        with self.voiceover("Chapter seven. Beyond semimartingales: rough paths, and signatures."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fbm(self, f):
        rows = VGroup()
        for H, col, txt in [(0.1, JUMP, r"$H = 0.1$: rough, increments anti-persistent"),
                            (0.5, BM, r"$H = 0.5$: Brownian motion"),
                            (0.9, DRIFT, r"$H = 0.9$: smooth, increments persistent")]:
            y = np.asarray(f[str(H)])
            y = (y - y.mean()) / (y.std() + 1e-12)
            g = axes([0, 1000], [-3, 3], x_length=7.4, y_length=1.5, xticks=[], yticks=[], font_size=14)
            line = curve(g.ax, np.arange(len(y)), np.clip(y, -3, 3), col, stroke_width=2)
            lab = label(txt, font_size=21, color=col).next_to(g, RIGHT, buff=0.3)
            rows.add(VGroup(g, line, lab))
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=0.6).shift(UP * 0.3)
        eq = MathTex(r"\mathbb{E}\big[(B^H_t - B^H_s)^2\big] = |t - s|^{2H}", font_size=34).to_edge(DOWN, buff=1.0)
        note_ = label(r"for $H \neq \tfrac12$ not a semimartingale: a price driven by it admits arbitrage (Rogers 1997); "
                      r"but a volatility driven by it does not", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Brownian increments are independent. Benoit Mandelbrot and John Van Ness generalised that in 1968: "
            "fractional Brownian motion, whose increments over a time lag have variance lag to the power two H. "
            "<bookmark mark='a'/> With H equal to a half it is Brownian motion. Above a half the increments are "
            "positively correlated, and the path is smooth and trending. Below a half they are negatively correlated, "
            "and the path is rougher than Brownian motion. <bookmark mark='b'/> For H not equal to a half, fractional "
            "Brownian motion is not a semimartingale, so Itô's calculus does not apply, and a stock price driven by "
            "it would allow arbitrage. But nothing forbids volatility from being rough."
        ) as vo:
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(rows[0]), FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def bitcoin(self, r):
        d = np.asarray(r["days"], float)
        lv = np.asarray(r["log_vol"])
        t = np.array([datetime.fromtimestamp(x, tz=timezone.utc).year + (datetime.fromtimestamp(x, tz=timezone.utc)
                                                                            .timetuple().tm_yday - 1) / 366 for x in d])
        g = axes([2019, 2021], [lv.min() - 0.2, lv.max() + 0.2], x_length=6.6, y_length=1.9,
                 ylabel=r"log daily volatility (5-minute returns)", xticks=[2019, 2020, 2021], xfmt=lambda u: f"{int(u)}",
                 yticks=[], font_size=16).to_corner(UL, buff=0.5)
        ax = g.ax
        line = curve(ax, t, lv, BM, stroke_width=1.8)
        h = r["hurst"]
        qs, zeta = np.asarray(h["qs"]), np.asarray(h["zeta"])
        g2 = axes([0, 3.2], [0, 0.5], x_length=5.0, y_length=2.7, xlabel=r"$q$", ylabel=r"$\zeta_q$: scaling of "
                  r"$\mathbb{E}|\Delta \log\sigma|^q$", xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5], font_size=16)
        g2.to_corner(DL, buff=0.55)
        a2 = g2.ax
        dots = VGroup(*[Dot(a2.c2p(q, z), radius=0.07, color=JUMP) for q, z in zip(qs, zeta)])
        fit = curve(a2, np.array([0, 3.2]), h["H"] * np.array([0, 3.2]), JUMP, stroke_width=2.5)
        bm = DashedVMobject(curve(a2, np.array([0, 1.0]), 0.5 * np.array([0, 1.0]), GREY_B, stroke_width=2), num_dashes=12)
        side = VGroup(
            MathTex(rf"H \approx {h['H']:.2f}", font_size=44, color=JUMP),
            label(rf"each $q$ alone: {min(h['H_each']):.2f} to {max(h['H_each']):.2f}", font_size=21, color=GREY_A),
            label(rf"the same estimator on simulated fBM: {r['fbm_check']['0.1']:.2f} for $H = 0.1$, "
                  rf"{r['fbm_check']['0.5']:.2f} for $0.5$", font_size=19, color=GREY_B),
            wrapped_label(r"Gatheral, Jaisson and Rosenbaum (2018), ``Volatility is rough'': $H \approx 0.1$ for equity "
                          r"indices; Bitcoin agrees. Rough volatility models return in Part 14.", 5.2, 20, ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        src = real_data(r"Binance BTCUSDT one-minute candles, 2019--2020; the House's \texttt{hurst\_from\_increments}")
        with self.voiceover(
            "How rough is volatility? Measure Bitcoin's volatility each day from its five-minute returns, for two "
            f"years, {r['n_days']} days, and take logs. <bookmark mark='a'/> For each power q, see how the average "
            "q-th power of its changes grows with the lag. For fractional Brownian motion the growth exponent is q "
            "times H: a straight line through the origin. <bookmark mark='b'/> The points lie on such a line, with "
            f"slope about {h['H']:.2f}, far below the half of Brownian motion, shown dashed. The same estimator "
            "recovers the right answer on simulated paths. <bookmark mark='c'/> In 2018 Jim Gatheral, Thibault "
            "Jaisson and Mathieu Rosenbaum found H near a tenth for stock indices, in a paper titled \"Volatility is "
            "rough\". Bitcoin agrees. Rough volatility models, built on this fact, are the subject of Part fourteen."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(bm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, scale=1.5) for dd in dots], lag_ratio=0.2), Create(fit))
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def signature(self):
        # two paths with the same start, end and increments, taken in a different order
        a = np.array([[0, 0], [1, 0], [1, 1]], float)
        b = np.array([[0, 0], [0, 1], [1, 1]], float)
        sa, sb = sim.signature2(a), sim.signature2(b)
        plane = NumberPlane(x_range=[-0.5, 1.5, 0.5], y_range=[-0.5, 1.5, 0.5], x_length=4.0, y_length=4.0,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1}).to_edge(LEFT, buff=0.8)
        pa = VMobject(stroke_color=BM, stroke_width=5).set_points_as_corners([plane.c2p(*p) for p in a])
        pb = VMobject(stroke_color=STRAT, stroke_width=5).set_points_as_corners([plane.c2p(*p) for p in b])
        chord = DashedLine(plane.c2p(0, 0), plane.c2p(1, 1), color=GREY_B, stroke_width=2)
        area = VGroup(Polygon(*[plane.c2p(*p) for p in [(0, 0), (1, 0), (1, 1)]], stroke_width=0, fill_color=BM,
                              fill_opacity=0.35),
                      Polygon(*[plane.c2p(*p) for p in [(0, 0), (0, 1), (1, 1)]], stroke_width=0, fill_color=STRAT,
                              fill_opacity=0.35))
        rows = VGroup(
            MathTex(r"S(X)_{s,t} = \Big(1,\ \int dX^i,\ \iint_{u<v} dX^i_u\,dX^j_v,\ \dots\Big)", font_size=30),
            label(r"the signature: every iterated integral of the path (Chen 1957; Lyons 1998)", font_size=21,
                  color=GREY_A),
            MathTex(rf"\text{{level 1 (both): }} ({sa['S1'][0]:.0f}, {sa['S1'][1]:.0f})", font_size=28),
            MathTex(rf"\text{{L\'evy area: }} {sa['levy_area'][0, 1]:+.1f} \text{{ (blue)}}, \ {sb['levy_area'][0, 1]:+.1f}"
                    r"\text{ (purple)}", font_size=28, color=ITO),
            wrapped_label(r"level 2 sees the order of moves, which increments alone cannot; the whole signature "
                          r"determines the path (up to retracing), and linear functions of it approximate any smooth "
                          r"function of the path: features for machine learning on paths (Parts 14, 17, 42)", 6.2, 21,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "One more tool from rough paths. Two paths: right then up, and up then right. Same start, same end, same "
            "total increments. Any statistic built from the increments alone can't tell them apart. "
            "<bookmark mark='a'/> Kuo-Tsai Chen showed in 1957 that a path is captured by its iterated integrals, "
            "and Terry Lyons built the theory of rough paths on them in 1998. Collected together they are the path's "
            "signature. <bookmark mark='b'/> The first level is the increments, the same for both. The second level "
            "contains the Lévy area, the signed area between the path and its chord: plus a half for one path, "
            "minus a half for the other. Order matters, and the signature records it. <bookmark mark='c'/> The full "
            "signature determines the path, and linear functions of it can approximate any smooth function of the "
            "path, which makes it a natural set of features for learning from price histories. It returns in Parts "
            "fourteen, seventeen and forty-two."
        ) as vo:
            self.play(FadeIn(plane), Create(pa), Create(pb), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(Create(chord), FadeIn(area), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
