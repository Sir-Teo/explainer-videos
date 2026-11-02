from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, OPT, PART, illustration, load, loglog


class ADI(VoiceoverScene):
    def construct(self):
        a = load("adi")
        self.card()
        self.split()
        self.results(a)

    def card(self):
        c = chapter_card(7, r"ADI for Heston", r"How do you step a two-dimensional PDE without a huge matrix?", part=PART)
        with self.voiceover("Chapter seven. ADI for Heston."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def split(self):
        rows = [cmath(r"\partial_\tau u", r"=", r"A_0 u + A_1 u + A_2 u", font_size=38, colors={r"\partial_\tau u": OPT}),
                cmath(r"(I - \tfrac12\Delta t A_1)\,Y_1", r"=", r"Y_0 - \tfrac12\Delta t A_1 U,\quad "
                      r"(I - \tfrac12\Delta t A_2)\,Y_2 = Y_1 - \tfrac12\Delta t A_2 U", font_size=30,
                      colors={r"(I - \tfrac12\Delta t A_1)\,Y_1": DELTA})]
        whys = [why(r"Heston's pricing equation in price and variance: $A_1$ acts along the price, $A_2$ along the variance, "
                    r"$A_0$ is the mixed term from the correlation"),
                why(r"alternating direction implicit: treat one direction implicitly at a time, so each solve is a set of "
                    r"tridiagonal systems; the mixed term stays explicit (Douglas; Craig and Sneyd 1988, which corrects it; "
                    r"in 't Hout and Foulon 2010 compared the variants)")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.2, buff=1.0, edge=6.9)
        with self.voiceover(
            "Stochastic volatility adds a dimension: Heston's equation lives on a grid of price and variance. A fully "
            "implicit step would need a large two-dimensional solve. <bookmark mark='a'/> Alternating direction "
            "implicit schemes split the operator: implicit along the price for one half-step, then implicit along the "
            "variance, each a stack of cheap tridiagonal solves, with the mixed correlation term handled explicitly. "
            "Craig and Sneyd's version adds a correction for that mixed term; Karel in 't Hout and Sean Foulon tested "
            "the variants on Heston in 2010."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def results(self, a):
        rows = a["rows"]
        g = loglog(np.log10(15), np.log10(220), -4, 0, r"grid points along the price", r"error against the Fourier price",
                   xt=[2], yt=[-4, -3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"do": BAD, "cs": GOOD}
        lines = VGroup()
        for sch in ("do", "cs"):
            rr = [r for r in rows if r["scheme"] == sch]
            pts = [ax.c2p(np.log10(r["nS"]), np.clip(np.log10(max(r["err"], 1e-6)), -4, 0)) for r in rr]
            lines.add(VGroup(VMobject(stroke_color=cols[sch], stroke_width=3).set_points_as_corners(pts),
                             *[Dot(p_, radius=0.06, color=cols[sch]) for p_ in pts]))
        leg = legend([(BAD, r"Douglas"), (GOOD, r"Craig--Sneyd")], font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        best = min(rows, key=lambda r: r["err"])
        side = VGroup(
            wrapped_label(r"non-uniform grids, dense near the strike and near zero variance (in 't Hout and Foulon 2010); "
                          r"half as many variance points as price points", 4.2, 18, GREY_A),
            MathTex(rf"\text{{reference (COS):}}\ {a['ref']:.4f}", font_size=28),
            MathTex(rf"{best['nS']}\times{best['nv']}:\ {best['price']:.4f}\ \ ({best['time']:.1f}\,\text{{s}})", font_size=28,
                    color=GOOD),
            wrapped_label(r"both schemes converge at second order; with Feller's condition broken and strong correlation the "
                          r"variants differ more, which is why desks keep several", 4.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = illustration(r"Heston: $v_0 = \theta = 0.04$, $\kappa = 1.5$, $\xi = 0.5$, $\rho = -0.7$; one-year call at the money")
        with self.voiceover(
            "Here they are on a one-year Heston call, against the exact Fourier price, as the grid is refined. "
            "<bookmark mark='a'/> Both converge at second order. On the finest grid, "
            f"{best['nS']} by {best['nv']} points, the price is {best['price']:.4f} against {a['ref']:.4f}, in about "
            f"{best['time']:.0f} seconds on one core. A Fourier method gets the European price faster, as the next "
            "chapter shows; the grid earns its keep for barriers, early exercise and the Greeks of a whole book."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(leg), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.wait(0.4)
        self.clear_scene()
