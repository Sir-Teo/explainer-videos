from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, DICKENS, MONO, PART, card_in, load

KEEP = C.MODEL_Q  # the spread kept along a direction
LOSE = C.SURPRISE  # the squared distance lost


class PCA(VoiceoverScene):
    def construct(self):
        card_in(self, 1, r"Principal components, two ways", r"Where does the data vary most?",
                "Chapter one. Principal components, two ways.")
        self.twoways()
        self.derive()
        self.spectrum()
        self.svd()
        self.meaning()
        self.cloud()

    # ------------------------------------------------------------------
    def twoways(self):
        p = load("pca2")
        Z2 = np.asarray(p["Z2"])
        th_grid, along, lost = np.asarray(p["theta"]), np.asarray(p["along"]), np.asarray(p["lost"])
        total, th_best = float(p["total2"]), float(p["th_best"])
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], x_length=5.8, y_length=5.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.6, -0.35, 0])
        names = VGroup(data_text("the", font=MONO, font_size=22, color=GREY_A).next_to(ax.x_axis.get_right(), DOWN, buff=0.1),
                       data_text("not", font=MONO, font_size=22, color=GREY_A).next_to(ax.y_axis.get_top(), RIGHT, buff=0.1))
        P = np.clip(Z2, -3.1, 3.1)
        dots = VGroup(*[Dot(ax.c2p(*q), radius=0.035, color=GREY_B, fill_opacity=0.8) for q in P])
        th = ValueTracker(th_best - 1.2)
        sub = np.arange(0, len(P), 6)

        def u():
            return np.array([np.cos(th.get_value()), np.sin(th.get_value())])

        line = always_redraw(lambda: Line(ax.c2p(*(-3.4 * u())), ax.c2p(*(3.4 * u())), color=KEEP, stroke_width=4))
        segs = always_redraw(lambda: VGroup(*[Line(ax.c2p(*P[i]), ax.c2p(*((P[i] @ u()) * u())), color=LOSE,
                                                   stroke_width=1.6, stroke_opacity=0.8) for i in sub]))

        def interp(arr):
            return float(np.interp(th.get_value() % np.pi, th_grid, arr))

        BW, H = 0.7, 3.6
        x_bar = 2.6
        base = Line([x_bar - 0.6, -2.2, 0], [x_bar + 0.6, -2.2, 0], color=GREY_C)
        kept = always_redraw(lambda: Rectangle(width=BW, height=max(H * interp(along) / total, 0.01), stroke_width=0,
                                               fill_color=KEEP, fill_opacity=0.9)
                             .move_to([x_bar, -2.2 + H * interp(along) / total / 2, 0]))
        lostb = always_redraw(lambda: Rectangle(width=BW, height=max(H * interp(lost) / total, 0.01), stroke_width=0,
                                                fill_color=LOSE, fill_opacity=0.9)
                              .move_to([x_bar, -2.2 + H * interp(along) / total + H * interp(lost) / total / 2, 0]))
        topl = DashedLine([x_bar - 0.8, -2.2 + H, 0], [x_bar + 0.8, -2.2 + H, 0], color=WHITE, stroke_width=2)
        tl = label(rf"total $= {total:.2f}$", font_size=24).next_to(topl, UP, buff=0.1)
        kv = DecimalNumber(interp(along), num_decimal_places=2, font_size=30, color=KEEP)
        kv.add_updater(lambda m: m.set_value(interp(along)))
        lv = DecimalNumber(interp(lost), num_decimal_places=2, font_size=30, color=LOSE)
        lv.add_updater(lambda m: m.set_value(interp(lost)))
        kl = VGroup(label(r"spread along the line \\ (Hotelling: \ make it big)", font_size=22, color=KEEP), kv)
        kl.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, -1.2, 0])
        ll_ = VGroup(label(r"mean squared distance \\ (Pearson: \ make it small)", font_size=22, color=LOSE), lv)
        ll_.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, 1.0, 0])
        h1 = history_card(1901, r"Karl Pearson", r"\textit{On lines and planes of closest fit to systems of points in "
                          r"space}", width=5.4).move_to([3.4, 1.9, 0])
        h2 = history_card(1933, r"Harold Hotelling", r"\textit{Analysis of a complex of statistical variables into "
                          r"principal components}", width=5.4).next_to(h1, DOWN, buff=0.25)
        pyth = label(r"Pythagoras, for every page: \ $\|x\|^2 = $ (along)$^2 + $ (across)$^2$", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Pearson and Hotelling asked two different questions. <bookmark mark='h'/> Here are the pages again, on "
            "just two of the seventy word rates, 'the' and 'not', each rescaled to a spread of one. "
            "<bookmark mark='a'/> Pearson wanted the line that passes closest to the points: the smallest average "
            "squared distance, these little red segments. <bookmark mark='b'/> Hotelling wanted the direction along "
            "which the points spread the most. <bookmark mark='c'/> Turn the line, and watch both. Each page's squared "
            "length splits, by Pythagoras, into the part along the line and the part across it. So the spread kept "
            f"plus the distance lost is the same total, {total:.2f}, at every angle. <bookmark mark='d'/> The line "
            "closest to the points is the line of greatest spread. Two questions, one answer."
        ) as vo:
            self.play(FadeIn(h1, shift=UP * 0.2), FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("h")
            self.play(Create(ax), FadeIn(names), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(h1), FadeOut(h2))
            self.play(Create(line), FadeIn(segs), FadeIn(ll_), Create(base), FadeIn(lostb), FadeIn(kept))
            vo.wait_until("b")
            self.play(FadeIn(kl))
            vo.wait_until("c")
            self.play(FadeIn(pyth), Create(topl), FadeIn(tl))
            self.play(th.animate.set_value(th_best + 0.9), run_time=4.0, rate_func=there_and_back_with_pause)
            vo.wait_until("d")
            self.play(th.animate.set_value(th_best), run_time=2.0)
        for m in (line, segs, kept, lostb, kv, lv):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        p = load("pca2")
        err = np.asarray(p["err"])
        colors = {r"\mathbf{u}": KEEP, r"\lambda": KEEP, r"C": WHITE}
        rows = [
            cmath(r"\max_{\|\mathbf{u}\| = 1}", r"\;\mathbf{u}^{\top} C\, \mathbf{u}", colors=colors, font_size=40),
            cmath(r"\mathcal{L}", r"=", r"\mathbf{u}^{\top} C\, \mathbf{u}", r"-", r"\lambda", r"(\mathbf{u}^{\top}\mathbf{u} - 1)",
                  colors=colors, font_size=40),
            cmath(r"C\, \mathbf{u}", r"=", r"\lambda", r"\,\mathbf{u}", colors=colors, font_size=42),
            cmath(r"\mathbf{u}^{\top} C\, \mathbf{u}", r"=", r"\lambda", colors=colors, font_size=42),
            cmath(r"\mathbb{E}\,\|x - \mathbf{u}\mathbf{u}^{\top} x\|^2", r"=", r"\mathbb{E}\,\|x\|^2", r"-",
                  r"\mathbf{u}^{\top} C\, \mathbf{u}", colors=colors, font_size=40),
            cmath(r"\mathbb{E}\,\|x - V_k V_k^{\top} x\|^2", r"=", r"\lambda_{k+1} + \dots + \lambda_d", font_size=40),
        ]
        rows[5][2].set_color(LOSE)
        whys = [why(r"the spread along $\mathbf{u}$: \ $\mathrm{Var}(\mathbf{u}^{\top}x) = \mathbf{u}^{\top}C\mathbf{u}$"),
                why(r"a Lagrange multiplier \\ keeps $\|\mathbf{u}\| = 1$"),
                why(r"gradient $= 0$: \ an eigenvector"),
                why(r"multiply by $\mathbf{u}^{\top}$: \\ the spread is the eigenvalue"),
                why(r"Pythagoras: \ lost $=$ total $-$ kept"),
                why(r"$k$ directions: \ the eigenvalues \\ left out")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.55, edge=6.8)
        head = label(r"Why the answer is an eigenvector", font_size=34).to_edge(UP, buff=0.3)
        chk = label(rf"on the pages, $k = 5$: \ error $= {err[5]:.2f} =$ the $65$ eigenvalues left out \ "
                    r"(checked for every $k$)", font_size=24, color=C.BITS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here's why, in a few lines. The spread of the data along a unit vector u is u transpose C u, where C is "
            "the covariance matrix. <bookmark mark='a'/> We want the largest, keeping u at length one, so bring in a "
            "Lagrange multiplier, lambda. <bookmark mark='b'/> Set the gradient to zero, and out comes an eigenvector "
            "equation: C u equals lambda u. <bookmark mark='c'/> Multiply by u transpose: the spread along an "
            "eigenvector is its eigenvalue. So the best direction is the eigenvector with the largest eigenvalue. "
            "<bookmark mark='d'/> And the distance lost is the total minus the spread kept, so minimizing one "
            "maximizes the other. <bookmark mark='e'/> With k directions, the error left is exactly the sum of the "
            f"eigenvalues we leave out. On the pages, with five directions, that's {err[5]:.2f} of the seventy units "
            "of variance, and the identity holds for every k."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        p = load("pca")
        share = np.asarray(p["share"])
        from videos.ai.ai6 import compute as c6

        pg = c6.load("pages")
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
        en = label(r"symmetric: \ perpendicular eigenvectors \ (Part 3)", font_size=24, color=GREY_A).next_to(eig, DOWN, buff=0.15)
        k = 15
        bars = VGroup(*[Rectangle(width=0.26, height=max(18 * s, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                  fill_opacity=0.85).move_to([0.1 + 0.36 * i, -2.4 + 9 * s, 0]) for i, s in enumerate(share[:k])])
        base = Line([-0.1, -2.4, 0], [0.1 + 0.36 * k, -2.4, 0], color=GREY_C)
        pct = VGroup(*[MathTex(rf"{100 * share[i]:.1f}\%", font_size=22, color=C.MODEL_Q).next_to(bars[i], UP, buff=0.06)
                       for i in range(3)])
        bl = label(r"share of all the variation, \ direction by direction", font_size=24, color=GREY_A)
        bl.next_to(base, DOWN, buff=0.2).align_to(base, LEFT)
        with self.voiceover(
            "Principal components find the directions in which data varies the most. Start with the covariance "
            "matrix: seventy by seventy, how each pair of word rates moves together. <bookmark mark='a'/> It's "
            "symmetric, so, from part three, its eigenvectors are perpendicular, and each eigenvalue says how much of "
            "the variation lies along its eigenvector. <bookmark mark='b'/> The first direction holds "
            f"{100 * share[0]:.1f} percent of all the variation, the next {100 * share[1]:.1f}, and then they "
            "fall away."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s) for s in heat], lag_ratio=0.0002), FadeIn(hl), run_time=2.5)
            vo.wait_until("a")
            self.play(Write(eig), FadeIn(en))
            vo.wait_until("b")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(bl),
                      run_time=1.5)
            self.play(FadeIn(pct))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def svd(self):
        p = load("pca2")
        sv, vals, n = np.asarray(p["sv"]), np.asarray(p["vals"]), int(p["n"])
        dev = float(np.max(np.abs(sv ** 2 / n - vals)))
        colors = {r"V^{\top}": C.BITS, r"\Sigma": C.MODEL_Q}
        eq = cmath(r"Z", r"=", r"U", r"\Sigma", r"V^{\top}", colors=colors, font_size=60).move_to([-3.2, 1.6, 0])
        zl = label(rf"the data: \ ${n}$ pages $\times$ ${p['d']}$ rates", font_size=24, color=GREY_A)
        zl.next_to(eq, DOWN, buff=0.3)
        vl = label(r"rows of $V^{\top}$: \ the principal directions", font_size=26, color=C.BITS).next_to(zl, DOWN, buff=0.35)
        sl = label(r"$\sigma_i^2 / n$: \ the eigenvalues $\lambda_i$", font_size=26, color=C.MODEL_Q).next_to(vl, DOWN, buff=0.2)
        VGroup(vl, sl).align_to(zl, LEFT)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, float(vals[0]) * 1.1, 2], x_length=5.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, 0.1, 0])
        ev = VGroup(*[Dot(ax.c2p(i + 1, vals[i]), radius=0.07, color=C.MODEL_Q) for i in range(20)])
        sd = VGroup(*[Circle(radius=0.12, color=C.BITS, stroke_width=2).move_to(ax.c2p(i + 1, sv[i] ** 2 / n)) for i in range(20)])
        axl = label(r"the first $20$: \ eigenvalues (dots) \\ and $\sigma_i^2/n$ (rings)", font_size=22, color=GREY_A)
        axl.next_to(ax, UP, buff=0.15)
        chk = label(rf"largest difference: \ ${sci(max(dev, 1e-16), 1)}$ \ (rounding)", font_size=24, color=C.BITS)
        chk.next_to(ax, DOWN, buff=0.35)
        with self.voiceover(
            "In practice, nobody forms the covariance matrix. Part three's singular value decomposition of the data "
            "itself does the job: Z equals U, sigma, V transpose. <bookmark mark='a'/> The rows of V transpose are "
            "the principal directions, and each singular value, squared and divided by the number of pages, is an "
            "eigenvalue. <bookmark mark='b'/> On the pages the two agree to the last digits of floating point. "
            "Working on Z directly is also more accurate: squaring the data to make C squares its condition number."
        ) as vo:
            self.play(Write(eq), FadeIn(zl))
            vo.wait_until("a")
            self.play(FadeIn(vl), FadeIn(sl), Create(ax), FadeIn(axl), LaggedStart(*[FadeIn(d) for d in ev], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in sd], lag_ratio=0.05), FadeIn(chk))
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
        cloud_scale = 2.65 / max(float(np.linalg.norm(xyz, axis=1).max()), 1e-9)
        cl = Cloud3D(xyz, [AUSTEN if v == 0 else DICKENS for v in y], scale=cloud_scale, radius=0.05, tilt=0.35,
                     center=[0, -0.1, 0])
        axes_ = VGroup()
        for vec in (np.array([1.2, 0, 0]), np.array([0, 1.2, 0]), np.array([0, 0, 1.2])):
            arr = always_redraw(lambda vec=vec: Arrow(cl.project(np.zeros(3))[0], cl.project(vec)[0], buff=0,
                                                       color=GREY_A, stroke_width=3, max_tip_length_to_length_ratio=0.12))
            axes_.add(arr)
        split = label(rf"one cut along direction 1: \ ${100 * p['split']:.0f}\%$ of pages sorted right", font_size=28,
                      color=WHITE).to_edge(DOWN, buff=0.4)
        cap = label(r"the pages along the first three directions", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Seen along the first three directions, the authors already sit apart. <bookmark mark='a'/> A single cut "
            f"along the first direction sorts {100 * p['split']:.0f} percent of the pages correctly. PCA is part "
            "three's eigenvectors, put to work: the cheapest way to see a cloud of high-dimensional data."
        ) as vo:
            self.play(FadeIn(cl), FadeIn(axes_), FadeIn(cap))
            self.play(cl.angle.animate.set_value(1.1), run_time=4.0, rate_func=smooth)
            vo.wait_until("a")
            self.play(FadeIn(split), cl.angle.animate.set_value(0.0), cl.tilt.animate.set_value(0.0), run_time=3.0)
        for a in axes_:
            a.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
