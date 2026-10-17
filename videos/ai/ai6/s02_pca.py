from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, MONO, load, pca_picture, spin_pca


class PCA(VoiceoverScene):
    def construct(self):
        self.card()
        self.spectrum()
        self.meaning()
        self.cloud()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Principal components", r"Where does the data vary most?", part=6)
        with self.voiceover("Chapter one. Principal components."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def spectrum(self):
        p = load("pca")
        share = np.asarray(p["share"])
        from videos.ai.ai5 import compute as c5

        pg = c5.load("pages")
        X = np.asarray(pg["X"])
        Z = (X - X.mean(0)) / X.std(0)
        cov = Z.T @ Z / len(Z)
        n = cov.shape[0]
        cell = 3.6 / n
        dark, pos, neg = ManimColor("#121826"), ManimColor(C.BITS), ManimColor(C.TRUE_P)
        heat = VGroup()
        for i in range(n):
            for j in range(n):
                v = float(np.clip(cov[i, j], -1, 1))
                col = interpolate_color(dark, pos if v > 0 else neg, abs(v) ** 0.7)
                heat.add(Square(cell, stroke_width=0, fill_color=col, fill_opacity=1)
                         .move_to([-4.3 - 1.8 + (j + 0.5) * cell, 0.9 + 1.8 - (i + 0.5) * cell, 0]))
        hl = label(r"the $70 \times 70$ covariance matrix: \\ how every pair of word rates moves together", font_size=24,
                   color=GREY_A).next_to(heat, DOWN, buff=0.25)
        colors = {r"\mathbf{v}": C.BITS, r"\lambda": C.MODEL_Q}
        eig = cmath(r"C", r"\,", r"\mathbf{v}", "=", r"\lambda", r"\,", r"\mathbf{v}", colors=colors, font_size=46)
        eig.move_to([2.4, 2.6, 0])
        en = label(r"symmetric: \ perpendicular eigenvectors \ (Part 2)", font_size=24, color=GREY_A).next_to(eig, DOWN, buff=0.15)
        k = 15
        bars = VGroup(*[Rectangle(width=0.26, height=max(18 * s, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                  fill_opacity=0.85).move_to([0.1 + 0.36 * i, -2.4 + 9 * s, 0]) for i, s in enumerate(share[:k])])
        base = Line([-0.1, -2.4, 0], [0.1 + 0.36 * k, -2.4, 0], color=GREY_C)
        pct = VGroup(*[MathTex(rf"{100 * share[i]:.1f}\%", font_size=22, color=C.MODEL_Q).next_to(bars[i], UP, buff=0.06)
                       for i in range(3)])
        bl = label(r"share of all the variation, \ direction by direction", font_size=24, color=GREY_A)
        bl.next_to(base, DOWN, buff=0.2).align_to(base, LEFT)
        # a principal component in a picture: the pages on two word rates, and the line along which they spread most
        vocab = list(pg["vocab"])
        words = ("the", "not")
        Z2 = Z[:, [vocab.index(w) for w in words]]
        cov2 = Z2.T @ Z2 / len(Z2)
        th_best = float(np.arctan2(*np.linalg.eigh(cov2)[1][:, -1][::-1]))
        th = ValueTracker(th_best - 0.5 * np.pi)
        pcard = gloss(r"a principal component", r"the direction along which the data spreads most \\ "
                      rf"(shown here with two of the ${n}$ word rates)", pca_picture(Z2, words), corner=RIGHT, width=5.0,
                      color=C.MODEL_Q)
        pcard.move_to([3.6, 0.3, 0])
        spin_pca(pcard[1][2], cov2, th)
        with self.voiceover(
            "Principal components find the directions in which data varies the most. Start with the covariance "
            "matrix: seventy by seventy, how each pair of word rates moves together. <bookmark mark='a'/> It's "
            "symmetric, so, from part two, its eigenvectors are perpendicular, and each eigenvalue says how much of "
            "the variation lies along its eigenvector. <bookmark mark='b'/> The first direction holds "
            f"{100 * share[0]:.1f} percent of all the variation, the next {100 * share[1]:.1f}, and then they "
            "fall away."
        ) as vo:
            self.play(FadeIn(pcard, shift=UP * 0.2))
            self.play(th.animate.set_value(th_best), LaggedStart(*[FadeIn(s) for s in heat], lag_ratio=0.0002), FadeIn(hl),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(Write(eig), FadeIn(en))
            vo.wait_until("b")
            for m_ in pcard[1][2]:
                m_.clear_updaters()
            self.play(FadeOut(pcard))
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(bl),
                      run_time=1.5)
            self.play(FadeIn(pct))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        p = load("pca")
        top = p["top"]
        panels = VGroup()
        specs = ((r"direction 1", r"Austen's side", r"Dickens's side", AUSTEN, DICKENS),
                 (r"direction 2", r"narration", r"dialogue", GREY_B, C.BITS))
        for k, (title, lo, hi, c_lo, c_hi) in enumerate(specs):
            words = sorted(top[str(k)], key=lambda t: t[1])
            rows = VGroup()
            for i, (w, v) in enumerate(words):
                L = 2.2 * abs(v) / 0.3
                yv = -0.38 * i
                bar = Rectangle(width=L, height=0.26, stroke_width=0, fill_color=c_hi if v > 0 else c_lo,
                                fill_opacity=0.85).move_to([L / 2 if v > 0 else -L / 2, yv, 0])
                t = data_text(w, font=MONO, font_size=20, color=GREY_A).next_to(bar, RIGHT if v > 0 else LEFT, buff=0.1)
                rows.add(VGroup(bar, t))
            axis = Line([0, 0.25, 0], [0, -0.38 * (len(words) - 1) - 0.25, 0], color=GREY_C, stroke_width=2)
            head = label(title, font_size=30).next_to(axis, UP, buff=0.35)
            ends = VGroup(label(lo, font_size=24, color=c_lo).next_to(axis, DOWN, buff=0.3).shift(LEFT * 1.3),
                          label(hi, font_size=24, color=c_hi).next_to(axis, DOWN, buff=0.3).shift(RIGHT * 1.3))
            panels.add(VGroup(head, axis, rows, ends))
        panels[0].move_to([-3.4, -0.2, 0])
        panels[1].move_to([3.4, -0.2, 0])
        # a direction is a recipe: a weight for each of the word rates (the first direction's largest three, computed)
        d1 = sorted(top["0"], key=lambda t: -abs(t[1]))[:3]
        parts = [label(r"direction 1 $=$", font_size=28, color=GREY_A)]
        for i, (w, v) in enumerate(d1):
            sgn = "-" if v < 0 else ("+" if i else "")
            parts += [MathTex(rf"{sgn}{abs(v):.2f}\times", font_size=30, color=C.MODEL_Q),
                      data_text(w, font=MONO, font_size=24, color=WHITE)]
        parts += [MathTex(r"+\;\cdots", font_size=30, color=C.MODEL_Q),
                  label(rf"(all ${p['d']}$ word rates)", font_size=24, color=GREY_A)]
        recipe = VGroup(*parts).arrange(RIGHT, buff=0.14).to_edge(UP, buff=0.35)
        keep_in_frame(recipe)
        with self.voiceover(
            "What are these directions? Each one is a recipe for mixing the seventy word rates. "
            "<bookmark mark='a'/> The first weighs 'not', 'be', 'very' and 'she' against 'the', 'and' and 'out'. "
            "That's Austen against Dickens, found without ever being told who wrote what. <bookmark mark='b'/> The "
            "second weighs 'I', 'me', 'you', 'said' and 'my' against 'of' and 'their'. That's dialogue against "
            "narration: the other big difference between pages."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m_, shift=RIGHT * 0.1) for m_ in recipe], lag_ratio=0.12), run_time=2.0)
            for k, m in enumerate("ab"):
                vo.wait_until(m)
                head, axis, rows, ends = panels[k]
                x0 = axis.get_x()
                self.play(FadeIn(head), Create(axis),
                          LaggedStart(*[GrowFromEdge(r_[0], LEFT if r_[0].get_center()[0] > x0 else RIGHT) for r_ in rows],
                                      lag_ratio=0.08),
                          FadeIn(VGroup(*[r_[1] for r_ in rows])), FadeIn(ends), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        p = load("pca")
        xyz = np.asarray(p["proj"])[:, :3] / 3.2
        y = np.asarray(p["y"])
        cl = Cloud3D(xyz, [AUSTEN if v == 0 else DICKENS for v in y], scale=2.6, radius=0.05, tilt=0.35,
                     center=[-1.2, -0.3, 0])
        axes_ = VGroup()
        for k, (vec, name) in enumerate(((np.array([1.2, 0, 0]), r"1"), (np.array([0, 1.2, 0]), r"2"),
                                        (np.array([0, 0, 1.2]), r"3"))):
            arr = always_redraw(lambda vec=vec: Arrow(cl.project(np.zeros(3))[0], cl.project(vec)[0], buff=0,
                                                       color=GREY_A, stroke_width=3, max_tip_length_to_length_ratio=0.12))
            axes_.add(arr)
        split = label(rf"one cut along direction 1: \ ${100 * p['split']:.0f}\%$ of pages sorted right", font_size=28,
                      color=WHITE).to_edge(DOWN, buff=0.4)
        cap = label(r"the pages along the first three directions", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Seen along the first three directions, the authors already sit apart. <bookmark mark='a'/> A single cut "
            f"along the first direction sorts {100 * p['split']:.0f} percent of the pages correctly. PCA is part "
            "two's eigenvectors, put to work: the cheapest way to see a cloud of high-dimensional data."
        ) as vo:
            self.play(FadeIn(cl), FadeIn(axes_), FadeIn(cap))
            self.play(cl.angle.animate.set_value(1.1), run_time=4.0, rate_func=smooth)
            vo.wait_until("a")
            self.play(FadeIn(split), cl.angle.animate.set_value(0.0), cl.tilt.animate.set_value(0.0), run_time=3.0)
        for a in axes_:
            a.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
