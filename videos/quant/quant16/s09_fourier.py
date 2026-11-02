from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog


class Fourier(VoiceoverScene):
    def construct(self):
        f = load("fourier")
        r = load("race")
        self.card()
        self.methods(f)
        self.race(r)

    def card(self):
        c = chapter_card(8, r"Fourier methods, and the race", r"Which method should price this option?", part=PART)
        with self.voiceover("Chapter eight. Fourier methods, and the race."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def methods(self, f):
        rows = [cmath(r"C(k)", r"=", r"\frac{e^{-\alpha k}}{\pi}\int_0^\infty e^{-iuk}\,\frac{e^{-rT}\varphi(u - (\alpha + 1)i)}"
                      r"{\alpha^2 + \alpha - u^2 + i(2\alpha + 1)u}\,du", font_size=30, colors={r"C(k)": OPT})]
        whys = [why(r"Carr and Madan (1999): damp the call by $e^{\alpha k}$ so it has a Fourier transform, then one FFT "
                    r"prices a whole grid of strikes. COS (Fang and Oosterlee 2008, Part 13) expands the density in "
                    r"cosines instead, and converges exponentially for smooth densities")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.4, buff=1.0, edge=6.9)
        cos = [x for x in f["rows"] if x["method"] == "COS"]
        cm = [x for x in f["rows"] if x["method"] == "Carr-Madan"]
        tab = VGroup(VGroup(label(r"COS, terms", font_size=20, color=GREY_A), label(r"error", font_size=20, color=GREY_A),
                            label(r"Carr--Madan, points", font_size=20, color=GREY_A), label(r"error", font_size=20, color=GREY_A)))
        for i in range(max(len(cos), len(cm))):
            c1 = cos[i] if i < len(cos) else None
            c2 = cm[i] if i < len(cm) else None
            tab.add(VGroup(MathTex(str(c1["N"]) if c1 else "", font_size=26),
                           MathTex(f"{c1['err']:.1e}" if c1 else "", font_size=26, color=METHOD_COL["COS"]),
                           MathTex(str(c2["N"]) if c2 else "", font_size=26),
                           MathTex(f"{c2['err']:.1e}" if c2 else "", font_size=26, color=METHOD_COL["Carr-Madan FFT"])))
        xs = [-4.8, -2.4, 1.2, 4.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 0.2 - 0.5 * i, 0])
        with self.voiceover(
            "When a model has a characteristic function, as Heston, the Lévy models and rough Heston do, Fourier "
            "methods price a vanilla in microseconds. Peter Carr and Dilip Madan damped the call so it has a Fourier "
            "transform, and priced a whole grid of strikes with one fast Fourier transform. <bookmark mark='a'/> The "
            "COS method of Part thirteen expands the density in cosines instead. With a smooth density its error "
            "falls exponentially: a few dozen terms reach the precision that Carr–Madan needs thousands of points for."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def race(self, r):
        pts = r["points"]
        g = loglog(-4.5, 1.5, -8, 0, r"wall-clock time (seconds)", r"error in the price", x_length=7.4, y_length=4.6,
                   xt=[-4, -2, 0], yt=[-8, -6, -4, -2, 0])
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        groups = {}
        for p_ in pts:
            groups.setdefault(p_["method"], []).append(p_)
        lines = VGroup()
        order = ["Monte Carlo (QE, 50 steps)", "ADI (Craig-Sneyd)", "Carr-Madan FFT", "COS"]
        for m in order:
            rr = sorted(groups.get(m, []), key=lambda q: q["time"])
            if not rr:
                continue
            pp = [ax.c2p(np.clip(np.log10(q["time"]), -4.5, 1.5), np.clip(np.log10(max(q["err"], 1e-9)), -8, 0)) for q in rr]
            lines.add(VGroup(VMobject(stroke_color=METHOD_COL[m], stroke_width=3).set_points_as_corners(pp),
                             *[Dot(q_, radius=0.06, color=METHOD_COL[m]) for q_ in pp]))
        leg = legend([(METHOD_COL[m], m) for m in order], font_size=16).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = wrapped_label(r"the same European Heston call, priced every way the House knows: lower and to the left is "
                             r"better. For a vanilla, Fourier wins by orders of magnitude; the grid and the simulation are "
                             r"for what Fourier cannot do: early exercise, barriers, paths, many assets", 4.0, 18,
                             GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"one core; reference: COS with 4{,}096 terms")
        with self.voiceover(
            "Now the race: one Heston call, every method in the House, error against wall-clock time on one core. "
            "Lower and to the left is better. <bookmark mark='a'/> Monte Carlo crawls down its square-root line. The "
            "ADI grid is second order and much faster. The Fourier methods are in another world, COS above all: "
            "near machine precision in under a millisecond. <bookmark mark='b'/> So the rule is simple. Use Fourier "
            "when the model allows it and the product is a vanilla. Use grids for low-dimensional products with early "
            "exercise or barriers. Use simulation for everything else: many assets, long paths, and every product "
            "no one has written a PDE for."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4, run_time=4), FadeIn(leg))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
