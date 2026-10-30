from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import chapter, dots_on, load


class HighDim(VoiceoverScene):
    def construct(self):
        chapter(self, 14, r"Life in 768 dimensions", r"What is a space with hundreds of dimensions like?",
                "Chapter fourteen. Life in seven hundred and sixty-eight dimensions.")
        self.angles()
        self.orthogonal()
        self.room()
        self.lengths()

    # ------------------------------------------------------------------
    def angles(self):
        h = load("highdim")
        dims = list(h["dims"])
        assert dims == [2, 3, 10, 100, 768]
        sd = {d: h[f"angle_sd{d}"] for d in dims}
        hist = {d: np.asarray(h[f"angles{d}"], float) / 20000 for d in dims}
        top = max(hist[768].max(), 0.01)
        bars = LiveBars(hist[2], max_value=top, height=4.6, bar_width=0.28, gap=0.06, colors=C.TRUE_P)
        bars.place(-2.35)
        x0, w = bars.base.get_start()[0] + 0.15, 36 * 0.34
        ticks = VGroup(*[MathTex(rf"{a}^\circ", font_size=28, color=GREY_B).move_to([x0 + w * a / 180 - 0.03, -2.65, 0])
                         for a in (0, 45, 90, 135, 180)])
        head = label(r"The angle between two random directions", font_size=34).to_edge(UP, buff=0.4)
        dl = MathTex(r"d =", font_size=48)
        dv = Integer(2, font_size=48, color=C.BITS)
        dread = VGroup(dl, dv).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.7)
        with self.voiceover(
            "Our intuition comes from three dimensions, and in seven hundred and sixty-eight it misleads us. "
            "<bookmark mark='a'/> Pick two directions at random. In two dimensions, the angle between them could be "
            "anything. <bookmark mark='b'/> In three, angles near a right angle are already the most common. "
            "<bookmark mark='c'/> "
            f"In a hundred, the angle strays from ninety degrees by only {sd[100]:.1f} degrees on average, "
            f"<bookmark mark='d'/> and in 768, by {sd[768]:.1f}. Random directions in high dimensions are nearly "
            "perpendicular."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(ticks), FadeIn(dread))
            vo.wait_until("a")
            self.play(Indicate(dread))
            for d, mark in zip(dims[1:], ["b", "c", "c", "d"]):
                vo.wait_until(mark)
                self.play(*bars.to(hist[d]), ChangeDecimalToValue(dv, d), run_time=1.2)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orthogonal(self):
        h = load("highdim")
        ds = np.asarray(h["var_dims"], float)
        var = np.asarray(h["cos_var"])
        nsd = np.asarray(h["norm_sd"])
        rows = [
            cmath(r"\cos\theta", "=", r"\frac{\mathbf{x}\cdot\mathbf{y}}{|\mathbf{x}|\,|\mathbf{y}|} \approx "
                  r"\frac{\mathbf{x}\cdot\mathbf{y}}{d}", font_size=34),
            cmath(r"\operatorname{Var}(\mathbf{x}\cdot\mathbf{y})", "=", r"\textstyle\sum_{i=1}^d "
                  r"\operatorname{Var}(x_i y_i) = d", font_size=34),
            cmath(r"\operatorname{Var}(\cos\theta)", r"\approx", r"d / d^2 = 1/d", font_size=38,
                  colors={r"d / d^2 = 1/d": C.BITS}),
        ]
        whys = [why(r"both lengths $\approx \sqrt d$ \ (below)"), why(r"independent terms, \ each of variance $1$"),
                why(r"exactly $1/d$ for uniform directions")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-2.6, buff=0.35, edge=6.9)
        g = axes([0, 4, 1], [-4, 0, 1], x_length=5.8, y_length=3.2, xticks=[0, 1, 2, 3, 4], yticks=[-4, -3, -2, -1, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}" if v > 1 else ("1" if v == 0 else "10"),
                 yfmt=lambda v: f"10^{{{int(v)}}}" if v < -1 else ("1" if v == 0 else "0.1"),
                 xlabel=r"dimension $d$", ylabel=r"variance of $\cos\theta$", center=[-1.5, -1.9, 0])
        ax = g.ax
        lx = np.log10(ds)
        pred = Line(ax.c2p(0, 0), ax.c2p(4, -4), color=C.BITS, stroke_width=2)
        pl = MathTex(r"1/d", font_size=28, color=C.BITS).next_to(ax.c2p(3.6, -3.6), UR, buff=0.05)
        meas = dots_on(ax, lx, np.log10(var), C.TRUE_P, 0.07)
        k768 = int(np.argmin(np.abs(ds - 768)))
        cap = note(r"computed: \ $20{,}000$ random pairs at each $d$").to_corner(DR, buff=0.25)
        read = label(rf"$d = 768$: \ measured ${var[k768]:.5f}$, \ $1/d = {1 / 768:.5f}$", font_size=26,
                     color=C.TRUE_P).move_to([4.2, -0.8, 0])
        with self.voiceover(
            "Why? Here is the calculation, and it is short. <bookmark mark='a'/> The cosine is the dot product over "
            "the two lengths, and in high dimensions each length is close to the square root of d; we'll see why in "
            "a moment. <bookmark mark='b'/> The dot product is a sum of d independent products, each with mean zero "
            "and variance one, so its variance is d. <bookmark mark='c'/> Divide by d squared: the cosine's variance "
            "is one over d, and its spread is one over root d. <bookmark mark='d'/> Measured at thirteen dimensions "
            f"from 2 to {int(ds[-1])}, on a log scale, the points sit on the line. At 768: {var[k768]:.5f}, against "
            f"{1 / 768:.5f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            self.play(Create(pred), FadeIn(pl))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in meas], lag_ratio=0.1), FadeIn(read), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def room(self):
        h = load("highdim")
        head = label(r"$10{,}000$ random directions in $768$ dimensions", font_size=36).to_edge(UP, buff=0.5)
        line1 = label(rf"every pair between ${h['worst_angle']:.0f}^\circ$ and ${180 - h['worst_angle']:.0f}^\circ$",
                      font_size=38, color=C.BITS).move_to(UP * 1.2)
        # a fan of nearly perpendicular arrows, drawn as if seen from far away: many directions, all apart
        g = np.random.default_rng(9)
        fan = VGroup()
        for k in range(60):
            a = g.uniform(0, 2 * PI)
            fan.add(Line(ORIGIN, [1.6 * np.cos(a), 1.6 * np.sin(a), 0], color=C.TRUE_P, stroke_width=2, stroke_opacity=0.7))
        fan.move_to(DOWN * 1.2)
        sup = label(r"more features than dimensions, if they need only be \textit{nearly} perpendicular: \\ "
                    r"\textit{superposition} \ (Part 30)", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = label(r"schematic", font_size=22, color=GREY_B).next_to(fan, RIGHT, buff=0.3)
        # a feature: a direction; how far a vector reaches along it says how strongly the idea is present
        fdir = Arrow(ORIGIN, [2.2, 0.6, 0], buff=0, color=C.BITS, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        vec = Arrow(ORIGIN, [1.0, 1.4, 0], buff=0, color=C.TRUE_P, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        u_ = np.array([2.2, 0.6, 0]) / np.linalg.norm([2.2, 0.6])
        foot = (np.array([1.0, 1.4, 0]) @ u_) * u_
        feat_pic = VGroup(fdir, vec, DashedLine([1.0, 1.4, 0], foot, color=GREY_B, stroke_width=2),
                          Line(ORIGIN, foot, color=C.BITS, stroke_width=9, stroke_opacity=0.6),
                          label(r"a feature's direction", font_size=20, color=C.BITS).next_to(fdir, DOWN, buff=0.12).align_to(fdir, RIGHT),
                          label(r"a word's vector", font_size=20, color=C.TRUE_P).next_to(vec.get_end(), UP, buff=0.08))
        feat = gloss(r"feature", r"one idea a model keeps track of, stored as a direction:\\ how far a vector reaches "
                     r"along it says how strongly the idea is there", picture=feat_pic, width=4.6)
        feat.to_edge(LEFT, buff=0.3).set_y(-0.6)
        with self.voiceover(
            "So a high-dimensional space is full of room. <bookmark mark='a'/> Ten thousand random directions in 768 "
            f"dimensions: every pair of them lies between {h['worst_angle']:.0f} and {180 - h['worst_angle']:.0f} "
            "degrees apart. "
            "<bookmark mark='b'/> A feature is one idea a model keeps track of, stored as a direction. A model can "
            "keep far more features than it has dimensions, as long as their directions only need to be nearly "
            "perpendicular. Packing in more directions than dimensions this way is called superposition, and it's "
            "how Part 30 reads the inside of a model."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in fan], lag_ratio=0.03), FadeIn(tag), run_time=1.8)
            self.play(FadeIn(line1))
            vo.wait_until("b")
            self.play(FadeIn(sup), FadeIn(feat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        h = load("highdim")
        dims = list(h["dims"])
        vd = [int(v) for v in h["var_dims"]]
        nsd = np.asarray(h["norm_sd"])
        hist = {d: np.asarray(h[f"norms{d}"], float) / 20000 for d in dims}
        top = max(hist[768].max(), 0.01)
        bars = LiveBars(hist[2], max_value=top, height=3.4, bar_width=0.15, gap=0.03, colors=C.MODEL_Q)
        bars.place(-2.0, x=-3.6)
        x0, w = bars.base.get_start()[0] + 0.15, 40 * 0.18
        ticks = VGroup(*[MathTex(t, font_size=26, color=GREY_B).move_to([x0 + w * v / 2 - 0.02, -2.2, 0])
                         for t, v in (("0", 0), (r"\sqrt d", 1), (r"2\sqrt d", 2))])
        head = label(r"The length of a random vector, \ $\mathbf{x} \sim \mathcal{N}(0, I_d)$", font_size=34)
        head.to_edge(UP, buff=0.35)
        dv = Integer(2, font_size=44, color=C.BITS)
        dread = VGroup(MathTex(r"d =", font_size=44), dv).arrange(RIGHT, buff=0.2).move_to([-3.6, 2.2, 0])
        rows = [
            cmath(r"|\mathbf{x}|^2", "=", r"\textstyle\sum_{i=1}^d x_i^2", font_size=32),
            cmath(r"\mathbb{E}|\mathbf{x}|^2", "=", r"d, \quad \operatorname{Var}|\mathbf{x}|^2 = 2d", font_size=32),
            cmath(r"\operatorname{sd}|\mathbf{x}|", r"\approx", r"\frac{\sqrt{2d}}{2\sqrt d} = \frac{1}{\sqrt 2}",
                  font_size=32),
        ]
        whys = [why(r"$d$ independent squares", font_size=22), why(r"$\mathbb{E}x_i^4 = 3$", font_size=22),
                why(r"$\sqrt{\cdot}$ near $d$ has \\ slope $1/(2\sqrt d)$", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=2.4, buff=0.4, edge=6.9)
        k768 = vd.index(768)
        meas = label(rf"measured spread at $d = 768$: \ ${nsd[k768]:.3f}$; \ $1/\sqrt 2 = 0.707$", font_size=26,
                     color=C.MODEL_Q).move_to([2.6, -1.6, 0])
        with self.voiceover(
            "Now lengths. <bookmark mark='a'/> Give a vector d independent random coordinates. As d grows, its "
            "length piles up ever more tightly around the square root of d. <bookmark mark='b'/> The squared length "
            "is a sum of d squares, <bookmark mark='c'/> with mean d and variance 2 d. <bookmark mark='d'/> The "
            "square root near d changes by one over two root d per unit, so the length's spread is about one over "
            "root two, whatever d is. The spread stays put while the length grows: relative to it, the spread "
            f"disappears. Measured at 768 dimensions, {nsd[k768]:.3f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(ticks), FadeIn(dread))
            vo.wait_until("a")
            for d in dims[1:]:
                self.play(*bars.to(hist[d]), ChangeDecimalToValue(dv, d), run_time=0.9)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            self.play(FadeIn(meas))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
        self.shell()

    # ------------------------------------------------------------------
    def shell(self):
        h = load("highdim")
        shell = h["shell"]
        balls = VGroup()
        for d in (3, 100, 768):
            frac = shell[str(d)]
            b = VGroup(Circle(radius=1.3, color=C.TRUE_P, stroke_width=3, fill_color=C.TRUE_P, fill_opacity=0.12),
                       Annulus(inner_radius=1.17, outer_radius=1.3, color=C.BITS, fill_opacity=0.25 + 0.7 * frac,
                               stroke_width=0))
            v = MathTex(rf"d = {d}: \ {100 * frac:.{2 if d == 768 else 1}f}\%", font_size=32,
                        color=C.BITS if d == 768 else GREY_A).next_to(b, DOWN, buff=0.3)
            balls.add(VGroup(b, v))
        balls.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
        head = label(r"The share of a ball's volume within $1\%$ of its surface: \ $1 - 0.99^d$", font_size=34)
        head.to_edge(UP, buff=0.5)
        tag = note(r"the outer $1\%$ of the radius, drawn wider than life").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Volume does something stranger. The volume inside a radius r grows like r to the d, so the inner ball, "
            "with ninety-nine percent of the radius, holds 0.99 to the d of the volume. <bookmark mark='a'/> In three "
            f"dimensions, the outer one percent holds {100 * shell['3']:.1f} percent of the volume. In a hundred, "
            f"{100 * shell['100']:.1f} percent. <bookmark mark='b'/> In 768, {100 * shell['768']:.2f} percent: nearly "
            "all of a high-dimensional ball is skin. Random vectors live on a thin shell, and nearly perpendicular "
            "to each other. Both facts drive the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(balls[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(balls[0][1]))
            self.play(FadeIn(balls[1]))
            vo.wait_until("b")
            self.play(FadeIn(balls[2]))
        self.wait(0.3)
        self.clear_scene()
