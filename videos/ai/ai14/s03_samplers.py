from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, DDIM_C, DDPM_C, NOISE, cloud, curve, load, move_cloud


def sliced_picture() -> VGroup:
    """One slice of the sliced Wasserstein distance: two small clouds dropped onto one line, and the points matched
    in order along it."""
    a = np.array([[-1.5, 0.85], [-1.1, 1.15], [-0.6, 0.9], [-0.2, 1.2], [0.3, 0.95]])
    b = np.array([[-0.9, 0.45], [-0.3, 0.65], [0.4, 0.5], [0.9, 0.7], [1.5, 0.55]])
    line = Line([-2.0, 0, 0], [2.0, 0, 0], color=GREY_B, stroke_width=2)
    g = VGroup(line)
    for pts, col, side in ((a, DATA, 1), (b, DDIM_C, -1)):
        for x, y in pts:
            g.add(Dot([x, y, 0], radius=0.07, color=col),
                  DashedLine([x, y - 0.08, 0], [x, 0.0, 0], color=col, stroke_width=1.2, dash_length=0.05).set_opacity(0.6),
                  Line([x, 0, 0], [x, 0.16 * side, 0], color=col, stroke_width=4))
    for xa, xb in zip(sorted(a[:, 0]), sorted(b[:, 0])):
        g.add(ArcBetweenPoints([xa, -0.3, 0], [xb, -0.3, 0], angle=PI / 2, color=GREY_A, stroke_width=1.5))
    g.add(label(r"real data", font_size=20, color=DATA).next_to(Dot([-1.5, 0.85, 0]), LEFT, buff=0.15),
          label(r"samples", font_size=20, color=DDIM_C).next_to(Dot([1.5, 0.55, 0]), RIGHT, buff=0.1),
          label(r"matched in order along the line", font_size=18, color=GREY_A).move_to([0, -0.7, 0]))
    return g


class Samplers(VoiceoverScene):
    def construct(self):
        self.card()
        self.walk()
        self.steps()

    def card(self):
        card = chapter_card(2, r"Walking back from noise", r"How many steps does it take?", part=14)
        with self.voiceover("Chapter two. Walking back from noise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def walk(self):
        t = load("toy")
        P1, P2 = np.asarray(t["ddpm_path"]), np.asarray(t["ddim_path"])
        S = 0.62
        lsh, rsh = np.array([-3.5, -0.5]), np.array([3.5, -0.5])
        n = 150
        d1 = cloud(P1[0][:n], NOISE, radius=0.03, scale=S, shift=lsh)
        d2 = cloud(P2[0][:n], NOISE, radius=0.03, scale=S, shift=rsh)
        t1 = label(r"DDPM: \ $200$ steps, \ each with fresh noise", font_size=26, color=DDPM_C).move_to([-3.5, 2.7, 0])
        t2 = label(r"DDIM: \ $50$ steps, \ no noise added", font_size=26, color=DDIM_C).move_to([3.5, 2.7, 0])
        trails = VGroup()
        for P, sh, col in ((P1, lsh, DDPM_C), (P2, rsh, DDIM_C)):
            for i in range(0, n, 10):
                trails.add(VMobject(stroke_width=1.2, stroke_color=col, stroke_opacity=0.6).set_points_as_corners(
                    [[p[i, 0] * S + sh[0], p[i, 1] * S + sh[1], 0] for p in P]))
        cite_ = cite(r"J.~Ho et al., \textit{DDPM} (2020); \ J.~Song, C.~Meng \& S.~Ermon, \textit{DDIM} (2021)", corner=DR)
        with self.voiceover(
            "Now walk back. DDPM, the 2020 paper that made diffusion work, takes many small steps: at each, it uses "
            "the network to guess the clean point, steps partway towards it, and adds a little fresh noise. "
            "<bookmark mark='a'/> Its paths wander, like the Brownian motion they reverse. <bookmark mark='b'/> DDIM, a "
            "year later, noticed the same network also defines a deterministic path, with no noise added: each point "
            "glides to a fixed destination, and in far fewer steps."
        ) as vo:
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(d1), FadeIn(d2), FadeIn(cite_))
            vo.wait_until("a")
            for k in range(1, len(P1)):
                self.play(*move_cloud(d1, P1[k][:n], S, lsh), run_time=0.12, rate_func=linear)
            vo.wait_until("b")
            for k in range(1, len(P2)):
                self.play(*move_cloud(d2, P2[k][:n], S, rsh), run_time=0.08, rate_func=linear)
            self.play(Create(trails), *[d.animate.set_color(DATA) for d in [*d1, *d2]], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        t = load("toy")
        ks = [int(k) for k in t["ddim_steps"]]
        sw = np.array([float(t[f"sw_ddim{k}"]) for k in ks])
        noise, floor, ddpm = float(t["sw_noise"]), float(t["sw_floor"]), float(t["sw_ddpm"])
        lx = np.log10(ks)
        hi = max(sw.max(), ddpm) * 1.15
        ystep = next(v for v in (0.05, 0.1, 0.2, 0.25, 0.5, 1.0) if v >= hi / 5)  # round tick values
        ax = Axes(x_range=[0.6, 2.1, 0.5], y_range=[0, hi, ystep], x_length=6.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.6, -0.6, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(math.log10(k), 0), DOWN, buff=0.1) for k in ks])
        xn = label(r"sampling steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"distance from the real data \ (sliced Wasserstein)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        c = VGroup(curve(ax, lx, sw, DDIM_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=DDIM_C) for a, b in zip(lx, sw)])
        fl = DashedLine(ax.c2p(0.6, floor), ax.c2p(2.1, floor), color=GREY_B, stroke_width=1.5)
        fll = label(r"the floor: \\ two samples \\ of the data itself", font_size=20, color=GREY_B).next_to(fl.get_end(), RIGHT, buff=0.12)
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0.6, v), LEFT, buff=0.08)
                      for v in np.arange(ystep, hi + 1e-9, ystep)])
        dp = DashedLine(ax.c2p(0.6, ddpm), ax.c2p(2.1, ddpm), color=DDPM_C, stroke_width=1.5)
        dpl = label(r"DDPM, $200$ steps", font_size=20, color=DDPM_C).next_to(dp, UP, buff=0.05).align_to(dp, LEFT)
        S = 0.42
        snaps = VGroup()
        for i, k in enumerate((5, 20, 100)):
            pts = cloud(np.asarray(t[f"ddim{k}"])[:400], DATA, radius=0.018, scale=S)
            box = VGroup(pts, label(rf"${k}$ steps", font_size=20, color=GREY_A).next_to(pts, DOWN, buff=0.1))
            snaps.add(box)
        snaps.arrange(DOWN, buff=0.25).move_to([4.4, -0.3, 0])
        swc = gloss(r"sliced Wasserstein", r"drop both clouds onto many random lines, \\ and compare where the points fall",
                    sliced_picture(), width=4.6, color=GREY_A).move_to([4.4, 0.4, 0])
        with self.voiceover(
            "How few steps can you take? Measure how far the samples land from the real data, <bookmark mark='w'/> "
            "with the sliced Wasserstein distance: drop both clouds onto many random lines, and compare where "
            "their points fall. "
            f"<bookmark mark='a'/> With five DDIM steps, the letters are blurred; by twenty, they're nearly as good as "
            "DDPM's two hundred; beyond that, little changes. <bookmark mark='b'/> Each step is one run of the network, "
            "so fewer steps is faster pictures. Can we do better still? The paths are curved, and curved paths need "
            "many small steps."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(fl), FadeIn(fll), Create(dp), FadeIn(dpl))
            vo.wait_until("w")
            self.play(FadeIn(swc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(swc))
            self.play(Create(c[0]), FadeIn(c[1:]), LaggedStart(*[FadeIn(s_) for s_ in snaps], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()
