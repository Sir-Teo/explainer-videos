from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rough as R
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, illustration, load, pause

H0 = 0.1


class Hybrid(VoiceoverScene):
    def construct(self):
        h = load("hybrid_check")
        self.card()
        self.spike()
        self.derive()
        self.convolution()
        self.lab(h)

    def card(self):
        c = chapter_card(6, r"Simulating a rough path: the hybrid scheme", r"Why do naive schemes fail, and what works?",
                         part=PART)
        with self.voiceover("Chapter six. Simulating a rough path: the hybrid scheme."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def spike(self):
        a = H0 - 0.5
        n_cells = 6
        g = axes([-n_cells, 0], [0, 4.0], x_length=10.0, y_length=4.4, xlabel=r"time $s$, in steps before $t$",
                 ylabel=r"kernel $(t - s)^{H - 1/2}$, $H = 0.1$ (one step = 1)", xticks=list(range(-n_cells, 1)),
                 yticks=[0, 1, 2, 3, 4], font_size=15).move_to(DOWN * 0.3)
        ax = g.ax
        xs = -np.exp(np.linspace(np.log(n_cells), np.log(1e-3), 300))
        ker = curve(ax, xs, np.clip((-xs) ** a, 0, 4.0), WHITE, stroke_width=3)
        naive, hyb, miss = VGroup(), VGroup(), VGroup()
        for k in range(1, n_cells + 1):
            left, right = -k, -k + 1
            hv = k ** a                                   # left-point value: the kernel at the cell's far end
            naive.add(Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, hv)[1] - ax.c2p(0, 0)[1],
                                stroke_color=BAD, stroke_width=1.5, fill_color=BAD, fill_opacity=0.25).move_to(
                ax.c2p((left + right) / 2, hv / 2)))
            if k >= 2:
                bk = ((k ** (a + 1) - (k - 1) ** (a + 1)) / (a + 1)) ** (1 / a)
                bv = bk ** a
                hyb.add(Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, bv)[1] - ax.c2p(0, 0)[1],
                                  stroke_color=RV, stroke_width=1.5, fill_color=RV, fill_opacity=0.3).move_to(
                    ax.c2p((left + right) / 2, bv / 2)))
                hyb.add(Dot(ax.c2p(-bk, bv), radius=0.05, color=RV))
        x1 = -np.exp(np.linspace(0, np.log(1e-3), 80))
        exact = Polygon(*[ax.c2p(x, 0) for x in (-1, 0)], *[ax.c2p(x, min(y, 4.0)) for x, y in zip(x1[::-1], (-x1[::-1]) ** a)],
                        stroke_width=0, fill_color=RV, fill_opacity=0.55)
        x2 = np.linspace(-1, -1e-3, 80)
        miss_poly = Polygon(*[ax.c2p(x, min((-x) ** a, 4.0)) for x in x2], ax.c2p(-1e-3, 1.0), ax.c2p(-1, 1.0),
                            stroke_width=0, fill_color=BAD, fill_opacity=0.5)
        leg = legend([(BAD, r"naive: the kernel at each cell's left end"),
                      (RV, r"hybrid: the first cell exactly; the others at optimal points $b_k$")],
                     font_size=17).to_corner(UR, buff=0.35)
        q = pause(r"Which scheme's error grows as $H$ falls?", width=5.2, font_size=22).to_corner(UL, buff=0.3)
        src = illustration(r"the last six steps before $t$; heights clipped at 4")
        with self.voiceover(
            "Rough Bergomi's driver is an integral of past shocks against the kernel t minus s to the power H minus "
            "a half. Here it is over the last six time steps before t. At s equal to t it shoots to infinity: that "
            "spike is what makes the path rough. <bookmark mark='a'/> The naive scheme, a Riemann sum, samples the "
            "kernel once per cell at its left end and stacks bars under it. Far from t the bars are fine. In the "
            "last cell, they miss nearly everything: the red area. <bookmark mark='b'/> Pause and predict: as H "
            "falls, whose error grows? <bookmark mark='c'/> The naive one's: the smaller H, the more of the "
            "variance lives in the spike. <bookmark mark='d'/> Mikkel Bennedsen, Asger Lunde and Mikko Pakkanen's "
            "hybrid scheme does two things. It integrates the first cell exactly, spike and all, with a pair of "
            "correlated normal draws. And for the other cells it evaluates the kernel not at the edge, but at the "
            "point b k where a single bar has exactly the cell's area."
        ) as vo:
            self.play(FadeIn(g), Create(ker), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(naive), FadeIn(leg[0]), FadeIn(miss_poly))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Indicate(miss_poly, color=BAD))
            vo.wait_until("d")
            self.play(FadeOut(naive), FadeOut(miss_poly), FadeOut(q))
            self.play(FadeIn(exact), FadeIn(hyb), FadeIn(leg[1]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\Big(\Delta W_i,\ \int_{t_i}^{t_{i + 1}}(t_{i + 1} - s)^{H - \frac12}dW_s\Big)", r"\sim",
                  r"\mathcal{N}\Big(0, \begin{pmatrix}\Delta & \frac{\Delta^{H + 1/2}}{H + 1/2}\\ \frac{\Delta^{H + 1/2}}"
                  r"{H + 1/2} & \frac{\Delta^{2H}}{2H}\end{pmatrix}\Big)", font_size=32,
                  colors={r"\Big(\Delta W_i,\ \int_{t_i}^{t_{i + 1}}(t_{i + 1} - s)^{H - \frac12}dW_s\Big)": RV}),
            cmath(r"b_k", r"=", r"\Big(\frac{k^{H + 1/2} - (k - 1)^{H + 1/2}}{H + 1/2}\Big)^{1/(H - 1/2)}", font_size=36,
                  colors={r"b_k": RV}),
            cmath(r"Y_{t_i}", r"\approx", r"\sqrt{2H}\Big(\int_{t_{i-1}}^{t_i}\!\cdots + \sum_{k \ge 2}(b_k\Delta)^{H - "
                  r"\frac12}\,\Delta W_{i - k}\Big)", font_size=34, colors={r"Y_{t_i}": ROUGH}),
            cmath(r"\text{cost}", r"=", r"O(n\log n)\ \text{by FFT}\quad\text{vs}\quad O(n^3)\ \text{Cholesky}",
                  font_size=36, colors={r"\text{cost}": GREY_A})]
        whys = [why(r"the Itô isometry on one cell: the increment and the singular integral are a correlated Gaussian pair"),
                why(r"choose the point where the kernel equals its own average over cell $k$: the mean-square optimal "
                    r"step function"),
                why(r"the far cells form a causal convolution of fixed weights with the noise"),
                why(r"a convolution is a product after a Fourier transform; an exact Gaussian simulation factors an "
                    r"$n \times n$ covariance")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The algebra. On the first cell, the Brownian increment and the integral of the singular kernel are a "
            "correlated Gaussian pair, with this covariance, straight from the Itô isometry. Draw them together and "
            "the spike is handled exactly. <bookmark mark='a'/> For the cell k steps back, take the point b k where "
            "the kernel equals its own average over the cell. <bookmark mark='b'/> Then the rough driver is the exact "
            "first cell plus a sum of fixed weights times past increments: a causal convolution. "
            "<bookmark mark='c'/> And a convolution is computed by the fast Fourier transform in n log n operations "
            "per path, where an exact simulation factors an n by n covariance matrix."
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

    def convolution(self):
        n = 120
        dW = np.random.default_rng(4).standard_normal(n)
        a = H0 - 0.5
        k = np.arange(1, 25)
        w = np.r_[1.0, (k[1:] ** a)]
        g1 = axes([0, n], [-3, 3], x_length=11.0, y_length=1.6, ylabel=r"shocks $\Delta W$", xticks=[], yticks=[],
                  font_size=14)
        g2 = axes([0, n], [-4, 4], x_length=11.0, y_length=2.2, xlabel=r"time step", ylabel=r"rough driver $Y$",
                  xticks=[0, 40, 80, 120], yticks=[], font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.5).move_to(DOWN * 0.2)
        bars = VGroup(*[Line(g1.ax.c2p(i + 0.5, 0), g1.ax.c2p(i + 0.5, np.clip(z, -3, 3)), stroke_color=GREY_B,
                             stroke_width=2) for i, z in enumerate(dW)])
        Y = np.array([np.sum(w[: min(i + 1, len(w))] * dW[i::-1][: len(w)]) for i in range(n)])
        Y = Y / np.std(Y) * 1.3
        t = ValueTracker(0)
        win = always_redraw(lambda: VMobject(stroke_color=ROUGH, stroke_width=2.5).set_points_as_corners(
            [g1.ax.c2p(t.get_value() + 0.5 - j, 2.8 * w[j] / w.max() * 0.9) for j in range(min(len(w), int(t.get_value()) + 1))]
            + [g1.ax.c2p(t.get_value() + 0.5 - min(len(w), int(t.get_value()) + 1) + 1, 0)]))
        out = tracing(g2.ax, np.arange(n) + 0.5, np.clip(Y, -4, 4), t, ROUGH, stroke_width=2.5)
        cap = label(r"the kernel's weights slide along the shocks; each position gives one value of the rough driver",
                    font_size=19, color=GREY_A).to_edge(UP, buff=0.35)
        src = illustration(r"24 weights shown; the FFT does every position at once")
        with self.voiceover(
            "Here is that convolution, done slowly. The grey bars are the shocks. The rough kernel's weights, "
            "tallest on the newest shock, slide along them; at each position, the weighted sum is one value of the "
            "rough driver, drawn below. The fast Fourier transform computes every position at once."
        ):
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(bars), FadeIn(cap), FadeIn(src), FadeIn(win), FadeIn(out))
            self.play(t.animate.set_value(n - 1), run_time=9, rate_func=linear)
        win.clear_updaters()
        out.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, h):
        card = lab_card(r"the hybrid scheme", [
            "cov = [[dt, dt**(a+1)/(a+1)],",
            "       [dt**(a+1)/(a+1), dt**(2*a+1)/(2*a+1)]]",
            "Z = rng.standard_normal((n_paths, n, 2)) @ cholesky(cov).T",
            "dW, Y1 = Z[:, :, 0], Z[:, :, 1]          # the exact first cell",
            "Gk[2:] = (_b(k, a) * dt) ** a           # optimal points",
            "conv = irfft(rfft(dW, m) * rfft(Gk, m), m)",
            "Y = sqrt(2*H) * (Y1 + conv[:, :n])       # the rough driver",
            "v = xi * exp(eta*Y - 0.5*eta**2 * t**(2*H))",
        ], source="explainer/quant/house/rough.py: rbergomi_paths (abridged)", width=8.6).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        rows = h["var"]
        outs = ["Var Y_1 (exact 1.00), 20,000 paths, 100 steps:"] + [
            f"  H = {r_['H']:<5g} hybrid {r_['hybrid']:.2f}   left-point Riemann {r_['riemann']:.2f}" for r_ in rows]
        at = h["atm30"]
        outs.append(f"rBergomi 30-day ATM vol: hybrid {100 * at['hybrid']:.1f}%   Riemann {100 * at['riemann']:.1f}%")
        tim = h["timing"]
        tl = "  ".join(f"n={t_['n']}: {t_['hybrid']:.2f}s vs {t_['cholesky']:.2f}s" for t_ in tim)
        outs.append("time, 1,000 paths (hybrid vs Cholesky): " + tl)
        r05 = rows[0]
        slower = tim[-1]["cholesky"] > tim[-1]["hybrid"]
        verdict = ("and by four thousand steps the exact Cholesky factorisation is the slower of the two"
                   if slower else "though at these sizes an exact Cholesky factorisation is still competitive on this "
                                  "machine: the hybrid scheme's real advantage is accuracy on any grid, at a cost that "
                                  "grows gently")
        with self.voiceover(
            "The House's version, abridged to its essentials: the covariance of the first cell and its Cholesky "
            "factor, the optimal points, the convolution by FFT, and the variance. <bookmark mark='a'/> Run the "
            "check that matters: the variance of the rough driver at time one is exactly one. With H of 0.05, "
            f"the hybrid scheme gives {r05['hybrid']:.2f}; the naive sum gives {r05['riemann']:.2f}, losing more than "
            "half the variance in the spike. As H rises to three-tenths, the naive error shrinks, just as the "
            "picture said. <bookmark mark='b'/> In prices, the damage is enormous: rough Bergomi's thirty-day "
            f"at-the-money volatility is {100 * at['hybrid']:.0f} percent with the hybrid scheme and "
            f"{100 * at['riemann']:.0f} with the naive one. <bookmark mark='c'/> On speed, the hybrid scheme scales "
            f"like n log n, {verdict}."
            " Simulation is slow. Next: a rough model with a near-closed form, rough Heston."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            out = lab_run(self, card, outs[:4], run_time=3)
            vo.wait_until("b")
            o2 = Text(outs[4], font="DejaVu Sans Mono", font_size=17).next_to(out, DOWN, buff=0.12).align_to(out, LEFT)
            self.play(AddTextLetterByLetter(o2), run_time=1.2)
            vo.wait_until("c")
            o3 = Text(outs[5], font="DejaVu Sans Mono", font_size=15).next_to(o2, DOWN, buff=0.12).align_to(o2, LEFT)
            keep_in_frame(o3)
            self.play(AddTextLetterByLetter(o3), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()
