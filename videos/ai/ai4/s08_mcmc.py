from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, WALK, load
from videos.ai.ai4.compute import density2, rng

ACCEPT, REJECT = "#5BD17A", C.SURPRISE


def heat_image(f, x_range, y_range, w=400, h=300) -> ImageMobject:
    xs = np.linspace(*x_range, w)
    ys = np.linspace(*y_range, h)[::-1]
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    Z = (Z / Z.max()) ** 0.8
    stops = [np.array(ManimColor(c).to_rgb()) for c in ("#0B0F17", "#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B")]
    k = np.clip(Z * (len(stops) - 1), 0, len(stops) - 1 - 1e-9)
    i = k.astype(int)
    a = (k - i)[..., None]
    rgb = (1 - a) * np.array(stops)[i] + a * np.array(stops)[np.minimum(i + 1, len(stops) - 1)]
    img = ImageMobject((np.concatenate([rgb, np.ones_like(a)], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    return img


class MCMC(VoiceoverScene):
    def construct(self):
        self.card()
        self.walk()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Sampling the unsampleable", r"How do you draw from a shape you can only evaluate?",
                            part=4, lit=(1953,))
        with self.voiceover("Chapter seven. Markov chain Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def walk(self):
        d = load("mcmc")
        chain = np.asarray(d["chain"])
        # replay the first steps exactly as compute.py drew them, keeping the proposals too
        g = rng(1953)
        x, steps = np.array([-3.0, 2.0]), []
        for _ in range(16):
            y = x + g.normal(scale=0.7, size=2)
            ok = g.random() < density2(*y) / density2(*x)
            steps.append((x.copy(), y.copy(), bool(ok)))
            x = y if ok else x
        assert np.allclose(x, chain[16])
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8.0, y_length=6.0, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-2.4, -0.3, 0])
        img = heat_image(density2, (-4, 4), (-3, 3))
        img.stretch_to_fit_width(8.0).stretch_to_fit_height(6.0).move_to(ax)
        frame_ = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        cont = contour_lines(ax, density2, (-4, 4), (-3, 3), [0.1, 0.3, 0.5, 0.7, 0.9], n=(120, 90), stroke_width=1.2)
        cont.set_stroke(opacity=0.55)
        walker = glow_dot(ax.c2p(*steps[0][0]), color=WHITE, radius=0.1)
        trail = VGroup()
        # the rule
        colors = {r"p(\text{new})": ACCEPT, r"p(\text{now})": DATA}
        f = cmath(r"\text{accept with probability}", font_size=30)
        f2 = cmath(r"\min\Big(1,\;", r"\frac{p(\text{new})}{p(\text{now})}", r"\Big)", colors=colors, font_size=42)
        rule = VGroup(f, f2).arrange(DOWN, buff=0.2).move_to([4.6, 2.2, 0])
        steps_t = VGroup(label(r"1. \ propose a small random step", font_size=26),
                         label(r"2. \ uphill: \ always take it", font_size=26, color=ACCEPT),
                         label(r"3. \ downhill: \ only sometimes", font_size=26, color=REJECT))
        steps_t.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rule, DOWN, buff=0.45)
        cancel = label(r"only a ratio: \ the unknown total cancels", font_size=26, color=C.BITS)
        cancel.next_to(steps_t, DOWN, buff=0.45)
        tag = label(r"a density known only up to a constant", font_size=24, color=GREY_A).next_to(img, DOWN, buff=0.15)
        tag.align_to(img, LEFT)  # flush left under the picture, clear of the citation in the corner
        cite_ = cite(r"N.~Metropolis, A.~Rosenbluth, M.~Rosenbluth, A.~Teller \& E.~Teller (1953)", corner=DR)
        with self.voiceover(
            "Monte Carlo needs samples. But often there's no direct way to draw them. All we can do is evaluate how "
            "likely each point is, and often only up to an unknown constant. That's exactly Bayes's rule, where the "
            "rescaling is the hard part. <bookmark mark='a'/> Here's a density in the plane, bright where points crowd together, with two bumps. In "
            "1953, at Los Alamos, Metropolis and his colleagues found a way to sample anything like it. Take a "
            "random walk. <bookmark mark='b'/> Propose a small random step. If it goes uphill, take it. "
            "<bookmark mark='c'/> If it goes downhill, take it only sometimes, with probability equal to the ratio "
            "of the heights. Otherwise, stay where you are."
        ) as vo:
            self.play(FadeIn(img), Create(frame_), Create(cont), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(walker), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(steps_t[0]), FadeIn(steps_t[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps_t[2]), Write(rule))
            for k, (x0, y0, ok) in enumerate(steps):
                rt = 0.55 if k < 6 else 0.3
                arr = Arrow(ax.c2p(*x0), ax.c2p(*y0), buff=0.08, color=ACCEPT if ok else REJECT, stroke_width=3,
                            max_tip_length_to_length_ratio=0.25)
                self.play(GrowArrow(arr), run_time=rt)
                if ok:
                    trail.add(Line(ax.c2p(*x0), ax.c2p(*y0), color=WALK, stroke_width=2, stroke_opacity=0.6))
                    self.play(walker.animate.move_to(ax.c2p(*y0)), FadeOut(arr), FadeIn(trail[-1]), run_time=rt)
                else:
                    self.play(FadeOut(arr, scale=0.6), Indicate(walker, color=REJECT, scale_factor=1.3), run_time=rt)
        # many steps: the visits pile up like the density
        pts = chain[17::3]
        visits = VGroup(*[Dot(ax.c2p(*p), radius=0.028, color=WHITE, fill_opacity=0.75) for p in pts])
        assert abs(float(d["left"]) - 2 / 3) < 0.05
        # a running count, as the walk goes: the share of the visits drawn so far that are in the left bump
        in_left = np.cumsum(pts[:, 0] < 0) / np.arange(1, len(pts) + 1)
        left = float(in_left[-1])
        assert abs(left - 2 / 3) < 0.05
        share = label(rf"time in the left bump: \ ${100 * left:.0f}\%$ \\ its share of the density: \ $67\%$",
                      font_size=24, color=WHITE)
        share.next_to(cancel, DOWN, buff=0.4).align_to(cancel, LEFT)
        j = ValueTracker(0)
        run_v = DecimalNumber(100 * in_left[0], num_decimal_places=0, unit=r"\%", font_size=30, color=WALK)
        run_l = label(r"time in the left bump, so far:", font_size=24, color=WALK)
        running = VGroup(run_l, run_v).arrange(RIGHT, buff=0.15)
        running.next_to(cancel, DOWN, buff=0.4).align_to(cancel, LEFT)
        keep_in_frame(running)
        with self.voiceover(
            "Only the ratio appears, so the unknown constant cancels out. <bookmark mark='a'/> Keep walking. The "
            "places the walker visits pile up exactly like the density: it's a Markov chain whose stationary "
            "distribution is the one we wanted. <bookmark mark='b'/> The left bump holds two thirds of the "
            f"probability, and the walker spends {100 * left:.0f} percent of its time there. Markov chain Monte "
            "Carlo made Bayesian statistics practical, and it's still how physicists sample molecules."
        ) as vo:
            self.play(FadeIn(cancel))
            vo.wait_until("a")
            self.play(FadeIn(running), run_time=0.4)
            run_v.add_updater(lambda m: m.set_value(100 * in_left[min(int(j.get_value()), len(pts) - 1)]))
            self.play(FadeOut(trail), FadeOut(tag),
                      LaggedStart(*[FadeIn(v) for v in visits], lag_ratio=0.0015),
                      MoveAlongPath(walker, VMobject().set_points_as_corners([ax.c2p(*p) for p in chain[17::3]])),
                      j.animate.set_value(len(pts) - 1), run_time=7.0, rate_func=linear)
            run_v.clear_updaters()
            vo.wait_until("b")
            self.play(FadeTransform(running, share))
        self.wait(0.3)
        self.clear_scene()
