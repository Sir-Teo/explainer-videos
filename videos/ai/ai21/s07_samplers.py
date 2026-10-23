from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, DDIM_C, DDPM_C, NOISE, PART, SCORE, Panel, load

COL = {r"\hat\varepsilon": SCORE, r"\hat x_0": DATA}


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
        self.ddim()
        self.steps()

    def card(self):
        card = chapter_card(6, r"DDPM and DDIM", r"Walk back with noise, or without?", part=PART)
        with self.voiceover("Chapter six. DDPM and DDIM."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def walk(self):
        d = load("denoiser")
        P1, P2 = np.asarray(d["ddpm_path"]), np.asarray(d["ddim_path"])
        n = 150
        p1 = Panel(6.2, center=[-3.4, -0.5, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
        p2 = Panel(6.2, center=[3.4, -0.5, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
        d1, d2 = p1.dots(P1[0][:n], NOISE, radius=0.03), p2.dots(P2[0][:n], NOISE, radius=0.03)
        t1 = label(r"DDPM: \ $200$ steps, \ each with fresh noise", font_size=26, color=DDPM_C).next_to(p1, UP, buff=0.15)
        t2 = label(r"DDIM: \ $50$ steps, \ no noise added", font_size=26, color=DDIM_C).next_to(p2, UP, buff=0.15)
        trails = VGroup(p1.paths(P1[:, :n], DDPM_C, stroke_width=1.2, opacity=0.6, every=10),
                        p2.paths(P2[:, :n], DDIM_C, stroke_width=1.2, opacity=0.6, every=10))
        cite_ = cite(r"J.~Ho et al., \textit{DDPM} (2020); \ J.~Song, C.~Meng \& S.~Ermon, \textit{DDIM} (2021)", corner=DR)
        with self.voiceover(
            "Two ways to discretize the walk back, with our trained denoiser. DDPM, the 2020 recipe, discretizes "
            "the reverse SDE: at each step it guesses the clean point, steps to the Gaussian of chapter one, and "
            "adds a little fresh noise. <bookmark mark='a'/> Its paths wander, like the Brownian motion they "
            "reverse. <bookmark mark='b'/> DDIM, a year later, adds no noise at all: each point glides to a fixed "
            "destination, and in far fewer steps."
        ) as vo:
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(t1), FadeIn(t2), FadeIn(d1), FadeIn(d2), FadeIn(cite_))
            vo.wait_until("a")
            for k in range(1, len(P1)):
                self.play(*p1.move(d1, P1[k][:n]), run_time=0.12, rate_func=linear)
            vo.wait_until("b")
            for k in range(1, len(P2)):
                self.play(*p2.move(d2, P2[k][:n]), run_time=0.08, rate_func=linear)
            self.play(Create(trails), *[x.animate.set_color(DATA) for x in [*d1, *d2]], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ddim(self):
        rows = [
            cmath(r"\hat x_0", r"=", r"\big(x_t - \sigma_t\,", r"\hat\varepsilon", r"\big)\,/\,\alpha_t", colors=COL, font_size=36),
            cmath(r"x_s", r"=", r"\alpha_s\,", r"\hat x_0", r"+", r"\sigma_s\,", r"\hat\varepsilon", colors=COL, font_size=36),
            cmath(r"\frac{x_s}{\alpha_s}", r"=", r"\frac{x_t}{\alpha_t} + \Big(\frac{\sigma_s}{\alpha_s} - \frac{\sigma_t}{\alpha_t}\Big)\,",
                  r"\hat\varepsilon", colors=COL, font_size=36),
        ]
        whys = [why(r"Tweedie: \ the network's clean guess"), why(r"keep the noise's direction, \ change its size"),
                why(r"divide by $\alpha_s$: \ one Euler step of the ODE \ in $x/\alpha$ and $\sigma/\alpha$")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-2.4, buff=0.65, edge=6.85)
        eta = VGroup(label(r"DDIM's knob $\eta$: \ add back a fraction of fresh noise", font_size=24, color=GREY_A),
                     label(r"$\eta = 0$: \ the probability-flow ODE \qquad $\eta = 1$: \ DDPM's reverse SDE", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "DDIM's step is two lines. From the noisy point, the network's noise guess gives a guess of the clean "
            "point, by Tweedie. <bookmark mark='a'/> To step to a lower noise level, put the clean guess back with "
            "less noise, keeping the noise's direction: the same noise, smaller. <bookmark mark='b'/> Divide by "
            "alpha, and the step is exactly one Euler step of the probability-flow ODE, in the coordinates x over "
            "alpha and sigma over alpha. <bookmark mark='c'/> Song, Meng and Ermon derived it from a different forward "
            "process with the same marginals, and gave it a knob, eta: at zero, no noise, the ODE; at one, DDPM "
            "again. The network doesn't change, only the sampler."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(eta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        t = load("denoiser")
        ks = [int(k) for k in t["ddim_steps"]]
        sw = np.array([float(t[f"sw_ddim{k}"]) for k in ks])
        floor, ddpm = float(t["sw_floor"]), float(t["sw_ddpm"])
        lx = np.log10(ks)
        hi = max(sw.max(), ddpm) * 1.15
        ystep = next(v for v in (0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1.0) if v >= hi / 5)
        ax = Axes(x_range=[0.6, 2.1, 0.5], y_range=[0, hi, ystep], x_length=6.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.6, -0.6, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(math.log10(k), 0), DOWN, buff=0.1) for k in ks])
        xn = label(r"DDIM steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"distance from the real data \ (sliced Wasserstein)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        c = VGroup(curve(ax, lx, sw, DDIM_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=DDIM_C) for a, b in zip(lx, sw)])
        fl = DashedLine(ax.c2p(0.6, floor), ax.c2p(2.1, floor), color=GREY_B, stroke_width=1.5)
        fll = label(r"the floor: \ a fresh sample \\ of the data itself", font_size=20, color=GREY_B).next_to(fl.get_end(), RIGHT, buff=0.12)
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0.6, v), LEFT, buff=0.08)
                      for v in np.arange(ystep, hi + 1e-9, ystep)])
        dp = DashedLine(ax.c2p(0.6, ddpm), ax.c2p(2.1, ddpm), color=DDPM_C, stroke_width=1.5)
        dpl = label(r"DDPM, $200$ steps", font_size=20, color=DDPM_C).next_to(dp, UP, buff=0.05).align_to(dp, LEFT)
        snaps = Group()
        for k in (5, 20, 100):
            pn = Panel(2.4, xlim=(-2.7, 2.9), ylim=(-1.8, 1.6), frame=False)
            snaps.add(Group(pn, pn.scatter(np.asarray(t[f"ddim{k}"]), DDIM_C, radius_px=1.3, res=240),
                            label(rf"${k}$ steps", font_size=20, color=GREY_A).next_to(pn, DOWN, buff=0.05)))
        snaps.arrange(DOWN, buff=0.15).move_to([4.6, -0.3, 0])
        swc = gloss(r"sliced Wasserstein", r"drop both clouds onto many random lines, \\ and compare where the points fall",
                    sliced_picture(), width=4.6, color=GREY_A).move_to([4.4, 0.4, 0])
        k_close = next((k for k, v in zip(ks, sw) if v <= ddpm * 1.1), None)
        close = (f"by {k_close} it is about as close as DDPM's two hundred; " if k_close is not None else
                 "even at a hundred it trails DDPM's two hundred; ")
        with self.voiceover(
            "How few steps will do? Measure how far the samples land from the data, <bookmark mark='w'/> with the "
            "sliced Wasserstein distance: drop both clouds onto many random lines, and compare where their points "
            f"fall. <bookmark mark='a'/> With five DDIM steps the letters are blurred, at {sw[0]:.2f}; " + close
            + f"at a hundred, {sw[-1]:.3f}, against a floor of {floor:.3f} for a fresh sample of the data itself. "
            "<bookmark mark='b'/> Each step is one run of the network, so fewer steps is faster pictures. The paths "
            "are curved, and curved paths need many small steps: the next three chapters are about taking fewer."
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
