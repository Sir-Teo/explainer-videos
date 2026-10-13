from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import interval_band, load, plain_axes, polyline
from videos.analysis5.compute import trap


class NearlyContinuous(VoiceoverScene):
    def construct(self):
        self.card()
        self.principles()
        self.lusin()
        self.dense()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Measurable is nearly continuous", r"How wild can a measurable function be?", lit=(),
                            part=5)
        with self.voiceover("Chapter ten: how wild measurable functions can be, which is: not very."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def principles(self):
        head = label(r"Littlewood's three principles \ (1944)", font_size=34).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"1. \ every measurable set is nearly a finite union of intervals", font_size=27),
            label(r"2. \ every measurable function is nearly continuous \ (Lusin)", font_size=27, color=C.EPS),
            label(r"3. \ every convergent sequence is nearly uniformly convergent \ (Egorov, chapter 7)", font_size=27),
        )
        for r_ in rows:
            if r_.width > 9.6:
                r_.width = 9.6
        ys = [1.55, -0.2, -1.95]
        for r_, y in zip(rows, ys):
            r_.next_to([-2.65, y, 0], RIGHT, buff=0)
        # three small pictures, one per principle
        pics = VGroup()
        ax1 = plain_axes([0, 1, 1], [0, 1, 1], 3.6, 1.2).move_to([-4.85, ys[0], 0]).set_opacity(0)
        rng = np.random.default_rng(7)
        dust = []
        for c0, w0 in ((0.12, 0.16), (0.45, 0.22), (0.8, 0.12)):
            for _ in range(9):
                a = c0 + rng.uniform(-w0 / 2, w0 / 2)
                dust.append((a, a + rng.uniform(0.004, 0.02)))
        p1 = VGroup(interval_band(ax1, dust, ys[0] - 0.25, GREY_B, height=0.18),
                    interval_band(ax1, [(0.04, 0.21), (0.34, 0.57), (0.74, 0.87)], ys[0] + 0.25, C.MEASURE, height=0.18),
                    Line(ax1.c2p(0, 0), ax1.c2p(1, 0), color=GREY_D).set_y(ys[0] - 0.45))
        pics.add(p1)
        d = load("lusin")
        x, f, g = d["x"], d["f"], d["g"]
        m = x <= 0.2
        ax2 = plain_axes([0, 0.2, 0.1], [0, 1.05, 0.5], 3.6, 1.3).move_to([-4.85, ys[1], 0])
        pics.add(VGroup(ax2, polyline(ax2, x[m][::2], f[m][::2], color=GREY_B, stroke_width=6),
                        polyline(ax2, x[m][::2], g[m][::2], color=C.EPS, stroke_width=2)))
        ax3 = plain_axes([0, 1, 0.5], [0, 1, 0.5], 3.6, 1.3).move_to([-4.85, ys[2], 0])
        xx = np.linspace(0, 1, 200)
        bad = Rectangle(width=ax3.c2p(1, 0)[0] - ax3.c2p(0.9, 0)[0], height=1.3, stroke_width=0, fill_color=C.PATHOLOGY,
                        fill_opacity=0.3).move_to(ax3.c2p(0.95, 0.5))
        pics.add(VGroup(ax3, bad, *[polyline(ax3, xx, xx**n, color=C.FUNC, stroke_width=1.8).set_stroke(
            opacity=0.35 + 0.08 * k) for k, n in enumerate((1, 2, 4, 8, 16, 32, 64))]))
        assert 0.9**64 < 1.2e-3  # off [0.9, 1], x^n is uniformly within 0.0012 of 0 by n = 64
        foot = label(r"``nearly'' \ $=$ \ except on a set of measure as small as you like", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Littlewood summed up the theory in three principles. Every measurable set is "
            "nearly a finite union of intervals. <bookmark mark='b'/> Every measurable function is nearly "
            "continuous. <bookmark mark='c'/> And every convergent sequence of functions is nearly uniformly "
            "convergent, which was Egorov's theorem. <bookmark mark='d'/> Nearly means: except on a set of measure as "
            "small as you like."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i], shift=RIGHT * 0.15), FadeIn(pics[i]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lusin(self):
        d = load("lusin")
        x, f, g, bad, eps, jumps, delta = d["x"], d["f"], d["g"], float(d["bad"]), float(d["eps"]), d["jumps"], float(d["delta"])
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 9.6, 3.6).move_to([-1.2, -0.1, 0])
        # the step function, drawn as flat pieces
        idx = np.nonzero(np.diff(f) != 0)[0]
        cuts = np.concatenate([[0], idx + 1, [len(x)]])
        fsteps = VGroup(*[Line(ax.c2p(x[a], f[a]), ax.c2p(x[b - 1], f[a]), color=C.FUNC, stroke_width=3)
                          for a, b in zip(cuts[:-1], cuts[1:])])
        gg = polyline(ax, x, g, color=C.APPROX, stroke_width=2)
        badset = interval_band(ax, [(t - delta, t + delta) for t in jumps], ax.c2p(0, 0)[1] - 0.3, C.PATHOLOGY,
                               height=0.18, min_width=0.012)
        bl = MathTex(r"\{f \ne g\}", font_size=26, color=C.PATHOLOGY).next_to(badset, LEFT, buff=0.15)
        inset, decor = magnifier(ax, (0.30, 0.36), (0.0, 1.05), center=[5.0, 1.3, 0], width=2.6, height=2.0, color=GREY_B)
        m = (x >= 0.30) & (x <= 0.36)
        zf = VGroup(*[Line(inset.c2p(max(x[a], 0.30), f[a]), inset.c2p(min(x[b - 1], 0.36), f[a]), color=C.FUNC,
                           stroke_width=3) for a, b in zip(cuts[:-1], cuts[1:]) if x[b - 1] >= 0.30 and x[a] <= 0.36])
        zg = polyline(inset, x[m], g[m], color=C.APPROX, stroke_width=3)
        head = VGroup(label(r"\textbf{Lusin's theorem} \ (RCA 2.24): \ measurable $f$, \ $\varepsilon > 0$ "
                            r"$\Rightarrow$ continuous $g$ with $\mu\{f \ne g\} < \varepsilon$", font_size=28),
                      ).to_edge(UP, buff=0.25)
        out = VGroup(MathTex(rf"\text{{a 100-step }} f: \ \ \mu\{{f \ne g\}} = {bad:.4f} < \varepsilon = {eps}",
                             font_size=30, color=C.PATHOLOGY),
                     label(r"$g$ replaces each jump by a steep ramp; \ $\sup|g| \le \sup|f|$", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        assert bad < eps
        with self.voiceover(
            "<bookmark mark='a'/> Lusin's theorem makes the second principle precise: a measurable function agrees "
            "with a continuous one except on a set of measure less than epsilon. <bookmark mark='b'/> Here f is a "
            "step function with a hundred random steps. <bookmark mark='c'/> The continuous g replaces each jump by "
            "a steep ramp; zoom in on one. <bookmark mark='d'/> The two functions differ only on the little "
            "intervals around the jumps, of total measure just under a twentieth."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(fsteps), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(gg), run_time=1.5)
            self.play(FadeIn(decor), Create(zf), Create(zg))
            vo.wait_until("d")
            self.play(FadeIn(badset), FadeIn(bl))
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dense(self):
        d = load("lusin")
        x, f, g = d["x"], d["f"], d["g"]
        diff = np.abs(f - g)
        l1 = trap(diff, x)
        head = label(r"A consequence for Part 6: \ $C_c$ is dense in $L^1$ \ (RCA 3.14)", font_size=32).to_edge(
            UP, buff=0.35)
        ax = plain_axes([0, 1, 0.25], [0, 0.5, 0.25], 6.6, 2.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.05, 0.55, 0])
        pk = diff > 1e-9
        spikes = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, b), color=C.PATHOLOGY, stroke_width=2)
                          for a, b in zip(x[pk][::3], diff[pk][::3])])
        al = MathTex(r"|f - g|", font_size=26, color=C.PATHOLOGY).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        side = VGroup(MathTex(rf"\int_0^1 |f - g| = {l1:.5f}", font_size=36, color=C.EPS),
                      label(r"nonzero only on the ramps:", font_size=24, color=GREY_A),
                      label(r"a set of measure $< \varepsilon$, \ where $|f - g| \le 2 \sup|f|$", font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to([0.6, 0.6, 0], RIGHT,
                                                                                               buff=0)
        card = VGroup(label(r"\textbf{Vitali--Carath\'eodory} \ (RCA 2.25), \ in one line:", font_size=28),
                      label(r"every real integrable $f$ has $u \le f \le v$, \ $u$ upper and $v$ lower semicontinuous,", font_size=26),
                      label(r"whose integrals differ by less than $\varepsilon$", font_size=26)).arrange(DOWN, buff=0.12)
        card.move_to(DOWN * 2.45)
        frame = SurroundingRectangle(card, color=GREY_C, buff=0.25, corner_radius=0.1)
        assert l1 < 2 * 1.0 * 0.05 and 0.0035 < l1 < 0.0045  # "about four thousandths"
        assert diff.max() < 0.5 and trap(pk.astype(float), x) < 0.05
        with self.voiceover(
            "<bookmark mark='a'/> A consequence we'll need in Part 6: continuous functions with compact support are "
            "dense among integrable functions. For our step function, the area between f and its repair is about four "
            "thousandths. <bookmark mark='b'/> A close cousin, the Vitali–Carathéodory theorem, squeezes every "
            "real integrable function between semicontinuous ones whose integrals are as close as you like."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(al))
            self.play(LaggedStart(*[Create(l_) for l_ in spikes], lag_ratio=0.002), FadeIn(side), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(card), Create(frame))
        self.wait(0.4)
        self.clear_scene()
