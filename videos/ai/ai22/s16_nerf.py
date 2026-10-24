from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, NERF_C, PART, PATCH, fmt_int, heat_image, load, rgb_image

RIE_C = C.SURPRISE


class NeRF(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.derive()
        self.check()
        self.replay()

    def card(self):
        card = chapter_card(15, r"Light through a volume", r"How do you learn a 3D scene from photographs?", part=PART)
        with self.voiceover("Chapter fifteen. Light through a volume."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        d = load("nerf")
        I = np.asarray(d["train_imgs"])
        cams = np.asarray(d["cams"])
        # a top view: the scene in the middle, the 24 cameras around it
        R = 2.0
        ctr = np.array([-3.6, 0.1, 0])
        ring = VGroup(*[Dot(ctr + R / 2.7 * np.array([c[0], c[2], 0]), radius=0.06, color=NERF_C) for c in cams])
        scene = VGroup(Square(0.9, stroke_color=PATCH, stroke_width=2, fill_color=PATCH, fill_opacity=0.15).move_to(ctr))
        rays = VGroup(*[Line(r_.get_center(), ctr, color=NERF_C, stroke_width=1, stroke_opacity=0.4) for r_ in ring[::3]])
        tv = label(r"seen from above: \ $24$ cameras", font_size=18, color=NERF_C).next_to(ring, DOWN, buff=0.2)
        photos = Group(*[rgb_image(I[k], 1.25) for k in (0, 4, 8, 12, 16, 20)]).arrange_in_grid(rows=2, cols=3, buff=0.12)
        photos.move_to([2.6, 1.2, 0])
        pl = label(r"six of the photographs \ ($32 \times 32$)", font_size=18, color=GREY_A).next_to(photos, UP, buff=0.12)
        f = MathTex(r"F_\theta:\ (x, y, z,\ \text{direction}) \;\mapsto\; (\sigma,\ \mathbf{c})", font_size=32).move_to([2.6, -1.4, 0])
        fl = label(r"density $\sigma$: \ how much stuff is there; \ colour $\mathbf c$: \ what light it gives off",
                   font_size=18, color=GREY_A).next_to(f, DOWN, buff=0.15)
        cite_ = cite(r"B.~Mildenhall, P.~Srinivasan, M.~Tancik, J.~Barron, R.~Ramamoorthi \& R.~Ng, \textit{NeRF} (2020)",
                     corner=DL)
        with self.voiceover(
            "So far, pictures and videos. Now the world behind them. Here is a small scene, a gold letter A and a "
            "blue ball, photographed from twenty-four cameras in a circle. <bookmark mark='a'/> Can a network "
            "learn the scene itself, so it can show it from anywhere? <bookmark mark='b'/> In 2020 Ben Mildenhall, "
            "Pratul Srinivasan, Matthew Tancik and colleagues represented a scene as a function: at every point in "
            "space, a density, how much stuff is there, and a colour, the light it gives off, which may depend on "
            "the viewing direction. A small network computes it: a neural radiance field, NeRF. To render a pixel, "
            "follow the ray through it and add up the light along the way."
        ) as vo:
            self.play(FadeIn(scene), LaggedStart(*[FadeIn(r_) for r_ in ring], lag_ratio=0.05), FadeIn(tv), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in photos], lag_ratio=0.2), FadeIn(pl), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in rays], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        # a ray from the camera through a blob of density
        o = np.array([-6.2, 2.4, 0])
        ray = Arrow(o, o + RIGHT * 4.6, buff=0, color=NERF_C, stroke_width=3, max_tip_length_to_length_ratio=0.05)
        blob = Ellipse(width=1.6, height=0.9, stroke_width=0, fill_color=PATCH, fill_opacity=0.35).move_to(o + RIGHT * 2.8)
        cam = Triangle(color=GREY_B, stroke_width=2).scale(0.18).rotate(-PI / 2).move_to(o + LEFT * 0.15)
        tl = MathTex(r"\mathbf r(t) = \mathbf o + t\,\mathbf d", font_size=26, color=NERF_C).next_to(ray, UP, buff=0.1)
        rows = [
            cmath(r"T(t + dt)", r"=", r"T(t)\,\big(1 - \sigma(t)\, dt\big)", font_size=32),
            cmath(r"T(t)", r"=", r"\exp\!\Big(-\int_0^t \sigma(s)\, ds\Big)", font_size=32),
            cmath(r"C", r"=", r"\int T(t)\, \sigma(t)\, \mathbf c(t)\, dt", font_size=32),
            cmath(r"\int_{t_i}^{t_{i+1}} T\, \sigma_i\, \mathbf c_i\, dt", r"=", r"T_i\, \big(1 - e^{-\sigma_i \delta_i}\big)\, \mathbf c_i",
                  font_size=32),
            cmath(r"C", r"=", r"\sum_i T_i\, \alpha_i\, \mathbf c_i, \quad \alpha_i = 1 - e^{-\sigma_i \delta_i}, \quad "
                  r"T_i = \prod_{j < i} (1 - \alpha_j)", font_size=32),
        ]
        whys = [why(r"$T$: \ the chance light gets through \ to depth $t$"),
                why(r"so $T' = -\sigma T$: \ solve"),
                why(r"light given off at $t$, \ times its chance to arrive"),
                why(r"$\sigma, \mathbf c$ constant on a segment of length $\delta_i$"),
                why(r"add the segments: \ alpha compositing")]
        step = ladder(self, rows, whys, keep=4, top=1.4, x=-1.2, buff=0.38, edge=6.8)
        with self.voiceover(
            "Here is the sum, derived. A ray leaves the camera, and T of t is the chance light from depth t gets "
            "back unblocked. <bookmark mark='a'/> Across a sliver dt, a fraction sigma dt is stopped. "
            "<bookmark mark='b'/> So T's rate of change is minus sigma times T, and T is the exponential of minus "
            "the density accumulated so far. <bookmark mark='c'/> The pixel's colour is the light given off at each "
            "depth, sigma times c, times its chance of arriving, added up along the ray. <bookmark mark='d'/> To "
            "compute it, cut the ray into segments where density and colour are constant: each segment's integral "
            "is exact, its transmittance times one minus e to the minus sigma delta, times its colour. "
            "<bookmark mark='e'/> Sum the segments: each contributes its opacity alpha, times its colour, times the "
            "chance of getting through everything in front. That's alpha compositing, the way graphics has layered "
            "transparent pictures since the 1980s."
        ) as vo:
            self.play(FadeIn(cam), GrowArrow(ray), FadeIn(blob), FadeIn(tl))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("nerf")
        q = d["quad"]
        Ns = [int(n) for n in q["Ns"]]
        lx = [math.log2(n) for n in Ns]
        s0 = "s8"
        rie = np.abs(np.asarray(q[s0]["riemann"], float))
        ner = np.abs(np.asarray(q[s0]["nerf"], float))
        lo = -7
        ly = lambda v: max(math.log10(max(v, 1e-12)), lo)  # noqa: E731
        ax = axes([lx[0], lx[-1]], [lo, 0.5], x_length=5.6, y_length=3.4, xlabel=r"samples along the ray",
                  ylabel=r"error in the pixel (log scale)", xticks=lx[::2], yticks=[-6, -4, -2, 0],
                  xfmt=lambda x: f"{2 ** x:.0f}", yfmt=lambda y: rf"10^{{{int(y)}}}", center=[-2.6, 0.0, 0], font_size=18)
        lr = VGroup(curve(ax.ax, lx, [ly(v) for v in rie], RIE_C), *[Dot(ax.ax.c2p(a, ly(v)), radius=0.05, color=RIE_C)
                                                                  for a, v in zip(lx, rie)])
        ln = VGroup(curve(ax.ax, lx, [ly(v) for v in ner], NERF_C), *[Dot(ax.ax.c2p(a, ly(v)), radius=0.05, color=NERF_C)
                                                                   for a, v in zip(lx, ner)])
        leg = legend([(RIE_C, r"Riemann sum: \ $\sum T_i\, \sigma_i \delta_i\, \mathbf c_i$"),
                      (NERF_C, r"NeRF's sum: \ $\sum T_i\, \alpha_i\, \mathbf c_i$")], font_size=20).move_to([3.8, 1.6, 0])
        setup = label(r"a ball of uniform density $\sigma = 8$, \ radius $1$, \\ a ray through its centre: \ exactly "
                      r"$C = 1 - e^{-16}$", font_size=20, color=GREY_A).move_to([3.8, -0.2, 0])
        r0 = float(np.asarray(q[s0]["riemann"])[0]) + float(q[s0]["exact"])
        over = r0 > 1
        better = all(n_ <= r_ + 1e-12 for n_, r_ in zip(ner, rie))
        if over:
            verdict = (f"With {Ns[0]} samples the Riemann sum gives {r0:.2f}, more light than exists; NeRF's sum is off "
                       f"by {ner[0]:.1e}.")
        else:
            verdict = f"With {Ns[0]} samples the Riemann sum gives {r0:.2f}; NeRF's sum is off by {ner[0]:.1e}."
        edge = ("At every number of samples, NeRF's sum is the more accurate: within a segment of constant density it "
                "is exact, and its error comes only from the segments that straddle the ball's edge." if better else
                "NeRF's sum is exact within a segment of constant density; its error comes only from the segments "
                "that straddle the ball's edge.")
        with self.voiceover(
            "Why not just add sigma times delta? Check it on a ball of uniform density, where the exact answer is "
            "known. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + edge
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(setup))
            vo.wait_until("a")
            self.play(Create(lr[0]), FadeIn(lr[1:]), Create(ln[0]), FadeIn(ln[1:]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("nerf")
        checks = [int(c) for c in d["checks"]]
        views = np.asarray(d["replay_views"])
        ps = [float(p) for p in d["replay_psnr"]]
        truth = np.asarray(d["test_imgs"])[1]
        S = 2.4
        tv = rgb_image(truth, S).move_to([-4.6, 0.9, 0])
        tl_ = label(r"a held-out view: \ the truth", font_size=18, color=GREY_A).next_to(tv, UP, buff=0.12)

        def view(k):
            return rgb_image(views[k], S).move_to([-1.6, 0.9, 0])

        cur = view(0)
        cl = label(r"our NeRF's render", font_size=18, color=NERF_C).next_to(cur, UP, buff=0.12)
        cv = np.asarray(d["curve"])
        top = float(np.ceil(max(cv[:, :, 1].max(), max(ps)) + 1))
        ax = axes([0, checks[-1]], [5, top], x_length=4.4, y_length=2.6, xlabel=r"training step",
                  ylabel=r"PSNR (dB): \ training batches; \ dots: held-out views", xticks=[0, checks[-1]],
                  yticks=[10, int(top)], center=[3.9, 1.0, 0], font_size=17, xfmt=lambda x: fmt_int(x))
        band_ = VGroup(*[curve(ax.ax, cv[s][:, 0], cv[s][:, 1], NERF_C, 1.5).set_stroke(opacity=0.5) for s in range(len(cv))])
        dots = VGroup(*[Dot(ax.ax.c2p(c, p), radius=0.06, color=PATCH) for c, p in zip(checks, ps)])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"step ${fmt_int(t.get_value())}$", font_size=22, color=NERF_C).next_to(cur, DOWN, buff=0.15))
        dep = heat_image(np.asarray(d["depth"]) * np.asarray(d["acc"]), 2.0, color=NERF_C, gamma=1.0).move_to([-1.6, -2.2, 0])
        dl = label(r"depth, \ from the same sum: \ $\sum T_i \alpha_i t_i$", font_size=18, color=NERF_C).next_to(dep, RIGHT, buff=0.3)
        pe = MathTex(r"\gamma(x) = \big(\sin 2^k \pi x,\ \cos 2^k \pi x\big)_{k = 0}^{5}", font_size=26).move_to([3.9, -1.3, 0])
        pel = label(r"positional encoding: \ without it, \\ an MLP draws only blurry fields \ (Tancik et al., 2020)",
                    font_size=17, color=GREY_A).next_to(pe, DOWN, buff=0.12)
        tp = np.asarray(d["test_psnr"], float)
        with self.voiceover(
            f"Now train one: an MLP of four layers, {int(d['params']):,} weights, fed the point's coordinates through "
            "sines and cosines of rising frequency, so it can draw sharp edges. <bookmark mark='a'/> Each step "
            f"renders {int(d['NR'])} random rays with {int(d['NS'])} samples each, and compares them with the "
            "photographs' pixels. <bookmark mark='b'/> Here is a view it never saw, at checkpoints. Its PSNR, the "
            f"higher the better, climbs from {ps[0]:.1f} decibels to {ps[-2]:.1f} by step {checks[-2]:,}, and ends "
            f"at {ps[-1]:.1f}; across three seeds, between {tp.min():.1f} and {tp.max():.1f}. <bookmark mark='c'/> The "
            "same weights give depth for free: the scene's shape, learned from flat photographs."
        ) as vo:
            self.play(FadeIn(tv), FadeIn(tl_), FadeIn(cur), FadeIn(cl), Create(ax), Write(pe), FadeIn(pel))
            self.add(cnt)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in band_], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dots[0]))
            for k in range(1, len(checks)):
                nxt = view(k)
                self.play(t.animate.set_value(checks[k]), FadeOut(cur), FadeIn(nxt), FadeIn(dots[k]), run_time=1.0)
                cur = nxt
            vo.wait_until("c")
            self.play(FadeIn(dep), FadeIn(dl))
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()
