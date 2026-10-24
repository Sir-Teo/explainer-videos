from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (DDIM_C, EPS_C, F_C, HEUN_C, NOISE, PART, SCORE, X0_C, bars_chart, legend, load,
                                   log_axes, logcurve, take_away)

PNAME = {"eps": r"predict the noise", "x0": r"predict the clean point", "F": r"EDM's mixture $F$"}
PSPOKEN = {"eps": "predicting the noise", "x0": "predicting the clean point", "F": "EDM's mixture"}
PCOL = {"eps": EPS_C, "x0": X0_C, "F": F_C}


class EDM(VoiceoverScene):
    def construct(self):
        self.card()
        self.sigma()
        self.precondition()
        self.trained()
        self.heun()

    def card(self):
        card = chapter_card(8, r"EDM: preconditioning and Heun", r"What should the network actually output?", part=PART)
        with self.voiceover("Chapter eight. EDM: preconditioning and Heun."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sigma(self):
        rows = [
            cmath(r"x", r"=", r"x_0 + \sigma\, n", font_size=36),
            cmath(r"\nabla \log p_\sigma(x)", r"=", r"\big(D(x; \sigma) - x\big)\,/\,\sigma^2", font_size=36),
            cmath(r"\frac{dx}{d\sigma}", r"=", r"\frac{x - D(x; \sigma)}{\sigma}", font_size=36),
        ]
        whys = [why(r"no shrinking: \ $\sigma$ from $80$ down to $0.002$"), why(r"Tweedie, \ with $\alpha = 1$"),
                why(r"the probability-flow ODE, \ in $\sigma$")]
        step = ladder(self, rows, whys, keep=3, top=2.3, x=-1.8, buff=0.7, edge=6.85)
        d = definition_card(r"the denoiser", r"$D(x; \sigma) = \mathbb E[x_0 \mid x]$: \ the best guess of the clean "
                            r"point; \ every parameterization is a way of computing it", width=7.4).to_edge(DOWN, buff=0.45)
        zoo = VGroup(*[VGroup(label(a_, font_size=30, color=c_), label(b_, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15)
                       for a_, b_, c_ in ((r"schedule", r"which noise levels, \ and when", C.BITS),
                                          (r"parameterization", r"what the network outputs", SCORE),
                                          (r"sampler", r"how to walk back", HEUN_C))]).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        cite_ = cite(r"T.~Karras, M.~Aittala, T.~Aila \& S.~Laine, \textit{Elucidating the Design Space of Diffusion-Based "
                     r"Generative Models} (2022)", corner=UR, font_size=18)
        with self.voiceover(
            "By 2022 there were many diffusion models, each with its own schedule, parameterization and sampler. "
            "Tero Karras and colleagues at NVIDIA pulled them apart. <bookmark mark='a'/> Drop the shrinking: let "
            "x be the clean point plus noise of size sigma, with sigma running from eighty down to almost nothing. "
            "<bookmark mark='b'/> Tweedie, with alpha equal to one, says the score is the denoiser's correction over "
            "sigma squared. <bookmark mark='c'/> And the probability-flow ODE becomes very plain: the rate of change "
            "of x with sigma is x minus its denoised version, over sigma. <bookmark mark='d'/> Everything, every "
            "schedule and parameterization, is a way of computing the denoiser D."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(z_, shift=DOWN * 0.1) for z_ in zoo], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(zoo.animate.scale(0.75).to_edge(DOWN, buff=0.25).set_opacity(0.6))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(zoo), FadeIn(d, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def precondition(self):
        e = load("edmtargets")
        sd = float(e["sd"])
        rows = [
            cmath(r"D(x; \sigma)", r"=", r"c_{\text{skip}}\, x + c_{\text{out}}\; F_\theta\big(c_{\text{in}}\, x,\ \sigma\big)",
                  font_size=32),
            cmath(r"c_{\text{in}}", r"=", r"1 / \sqrt{\sigma^2 + \sigma_d^2}", font_size=32),
            cmath(r"c_{\text{skip}}", r"=", r"\sigma_d^2 / (\sigma^2 + \sigma_d^2)", font_size=32),
            cmath(r"c_{\text{out}}", r"=", r"\sigma\, \sigma_d / \sqrt{\sigma^2 + \sigma_d^2}", font_size=32),
        ]
        whys = [why(r"a skip, \ and a network"), why(r"the input has unit variance"),
                why(r"so the error is multiplied by as little as possible"), why(r"and the target has unit variance")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-3.4, buff=0.38, edge=6.85)
        ss = np.asarray(e["s"])
        g = log_axes([math.log10(ss[0]), math.log10(ss[-1])], [-3, 2], x_length=5.6, y_length=2.6,
                     xlabel=r"noise level $\sigma$", ylabel=r"how much an output error moves $D$",
                     xticks=[0.01, 1, 80], yticks=[0.001, 1, 100], xfmt=lambda v: f"{v:g}",
                     yfmt=lambda v: f"{v:g}", center=[-2.6, -2.0, 0])
        cur = VGroup(logcurve(g.ax, ss, np.asarray(e["amp_eps"]), EPS_C, dots=False),
                     logcurve(g.ax, ss, np.asarray(e["amp_x0"]), X0_C, dots=False),
                     logcurve(g.ax, ss, np.asarray(e["amp_F"]), F_C, dots=False))
        lg = legend([(EPS_C, r"noise: \ $D = x - \sigma\hat\varepsilon$, \ times $\sigma$"),
                     (X0_C, r"clean point: \ times $1$"), (F_C, r"EDM: \ times $c_{\text{out}} \le \min(\sigma, \sigma_d)$")],
                    font_size=19).move_to([3.7, -1.7, 0])
        tf = np.asarray(e["tgt_F"])
        with self.voiceover(
            "Their first idea is preconditioning: wrap the network so that its job looks the same at every noise "
            "level. Write the denoiser as a skip connection plus a scaled network. <bookmark mark='a'/> Scale the "
            "input to unit variance, <bookmark mark='b'/> choose the skip so that the network's errors are magnified "
            "as little as possible, <bookmark mark='c'/> and then the output scale that makes the target have unit "
            "variance too. <bookmark mark='d'/> Why it matters: predict the noise, and an error in the output moves "
            "the clean guess by sigma times as much, eighty times at the top. Predict the clean point, and the "
            "network must output the whole answer even at almost no noise. EDM's mixture is never worse than either. "
            f"On our letters, with a data spread sigma d of {sd:.2f}, its target's spread stays between "
            f"{tf.min():.2f} and {tf.max():.2f} at every noise level."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(g), LaggedStart(*[Create(c_) for c_ in cur], lag_ratio=0.3), FadeIn(lg), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trained(self):
        a = load("ablate")
        sig = [float(v) for v in a["sig"]]
        ps = ["eps", "x0", "F"]
        D = {p: np.asarray(a[f"logn_{p}_derr"]) for p in ps}
        vals = np.concatenate([np.maximum(D[p], 1e-6).ravel() for p in ps])
        lo, hi = math.floor(math.log10(vals.min())), math.ceil(math.log10(vals.max()))
        g = log_axes([math.log10(sig[0]) - 0.1, math.log10(sig[-1]) + 0.1], [lo, hi], x_length=6.0, y_length=3.8,
                     xlabel=r"noise level $\sigma$", ylabel=r"error against the exact denoiser", xticks=sig,
                     yticks=[10.0 ** k for k in range(lo, hi + 1)], yfmt=lambda v: f"10^{{{int(round(math.log10(v)))}}}",
                     center=[-3.0, -0.2, 0])
        lines = VGroup()
        for p in ps:
            lines.add(VGroup(band(g.ax, np.log10(sig), np.log10(np.maximum(D[p].min(0), 1e-6)),
                                  np.log10(np.maximum(D[p].max(0), 1e-6)), PCOL[p], 0.18),
                             logcurve(g.ax, sig, np.maximum(D[p].mean(0), 1e-6), PCOL[p])))
        heun = {p: np.asarray(a[f"logn_{p}_heun"]) for p in ps}
        ch = bars_chart([heun[p].mean() for p in ps], [PCOL[p] for p in ps], [r"noise", r"clean point", r"EDM"],
                        height=2.2, bar_w=0.8, gap=0.5, spread=[(heun[p].min(), heun[p].max()) for p in ps], digits=3,
                        font_size=18).move_to([4.2, -1.3, 0])
        chl = label(rf"distance from the data, \ Heun, $35$ evaluations \\ (floor ${float(a['floor']):.3f}$; \ "
                    rf"${len(heun['eps'])}$ seeds)", font_size=18, color=GREY_A).next_to(ch, UP, buff=0.3)
        lg = legend([(PCOL[p], PNAME[p]) for p in ps], font_size=19).move_to([4.2, 2.3, 0])
        top_err = {p: D[p][:, -1].mean() for p in ps}
        low_err = {p: D[p][:, 0].mean() for p in ps}
        worst_hi = max(ps, key=lambda p: top_err[p])
        worst_lo = max(ps, key=lambda p: low_err[p])
        best = min(ps, key=lambda p: heun[p].mean())
        f_good = all(D["F"].mean(0) <= 1.5 * np.minimum(D["eps"].mean(0), D["x0"].mean(0)) + 1e-5)
        claim = ("EDM's mixture is close to the better of the two at every level." if f_good else
                 "EDM's mixture is not the best at every level, but it avoids both failures.")
        with self.voiceover(
            "We tested it: the same network, the same noise levels from EDM's log-normal, the same budget, three "
            f"ways of reading its output, {len(heun['eps'])} seeds each. <bookmark mark='a'/> Against the exact "
            f"denoiser, at the highest noise, {PSPOKEN[worst_hi]} is furthest off; at the lowest, {PSPOKEN[worst_lo]}. "
            f"<bookmark mark='b'/> {claim} <bookmark mark='c'/> After sampling, {PSPOKEN[best]} lands closest to the "
            "data on average."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines[:2]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
            vo.wait_until("c")
            self.play(FadeIn(ch), FadeIn(chl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heun(self):
        s = load("solvers")
        # a schematic of one step along dx/ds = B'(s), B a quadratic Bezier: Euler follows the start's slope and
        # overshoots; Heun averages the slopes at the start and where Euler lands, and (B' being linear) lands exactly
        P0, Cc, P1 = np.array([-6.3, -3.0, 0]), np.array([-5.0, 0.0, 0]), np.array([-0.6, 0.8, 0])
        arc = VMobject(color=WHITE, stroke_width=3.5).set_points_as_corners(
            [(1 - u) ** 2 * P0 + 2 * u * (1 - u) * Cc + u ** 2 * P1 for u in np.linspace(0, 1, 60)])
        s0, s1 = 2 * (Cc - P0), 2 * (P1 - Cc)
        e_end = P0 + s0
        eu = Arrow(P0, e_end, buff=0, color=DDIM_C, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        sl2 = Arrow(e_end, e_end + 1.6 * s1 / np.linalg.norm(s1), buff=0, color=GREY_B, stroke_width=3,
                    max_tip_length_to_length_ratio=0.2)
        he = Arrow(P0, P0 + (s0 + s1) / 2, buff=0, color=HEUN_C, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        ends = VGroup(Dot(P0, radius=0.08, color=NOISE), Dot(P1, radius=0.08, color=WHITE))
        labs = VGroup(label(r"the true path", font_size=24, color=WHITE).next_to(P1, RIGHT, buff=0.2),
                      label(r"Euler: \ the slope \\ at the start: \ overshoots", font_size=24, color=DDIM_C)
                      .next_to(e_end, LEFT, buff=0.35).shift(DOWN * 0.15),
                      label(r"the slope \\ where Euler lands", font_size=22, color=GREY_B).next_to(sl2, DOWN, buff=0.12),
                      label(r"Heun: \ the average of the two, \\ lands on the path", font_size=24, color=HEUN_C)
                      .next_to(P1, DOWN, buff=0.55).shift(RIGHT * 1.3))
        keep_in_frame(labs[1])
        tag = note(r"schematic").to_corner(UL, buff=0.3)
        rows = {k: s[k] for k in ("ddim", "heun")}
        nfe_h = [r["nfe"] for r in rows["heun"]]
        err_h = [r["err"] for r in rows["heun"]]
        err_d = {r["nfe"]: r["err"] for r in rows["ddim"]}
        better = [e < err_d.get(n + 1, err_d.get(n, 9e9)) for n, e in zip(nfe_h, err_h)]
        first = next((i for i in range(len(better)) if all(better[i:])), None)  # Heun better from here on
        cross = nfe_h[first] if first is not None else None
        j31 = min(range(len(nfe_h)), key=lambda i: abs(nfe_h[i] - 31))
        j63 = min(range(len(nfe_h)), key=lambda i: abs(nfe_h[i] - 63))
        ratio = err_d.get(nfe_h[j31] + 1, err_d.get(nfe_h[j31], 1.0)) / max(err_h[j31], 1e-9)
        ratio63 = err_d.get(nfe_h[j63] + 1, err_d.get(nfe_h[j63], 1.0)) / max(err_h[j63], 1e-9)
        res = VGroup(label(r"measured, \ exact denoiser, \ same spacing:", font_size=22, color=GREY_A),
                     label(rf"Heun, ${nfe_h[j31]}$ evaluations: \ error ${err_h[j31]:.3f}$", font_size=22, color=HEUN_C),
                     label(rf"Euler (DDIM), ${nfe_h[j31] + 1}$: \ ${err_d.get(nfe_h[j31] + 1, float('nan')):.3f}$", font_size=22,
                           color=DDIM_C),
                     label(r"Karras et al., CIFAR-10: \ FID $1.79$ with $35$ evaluations", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.7, -2.0, 0])
        low = (f"below about {cross} evaluations the correction can do harm, and plain Euler is better; but " if first
               else "")
        with self.voiceover(
            "Their second idea is the solver. Euler's method follows the slope at the start of the step, and on a "
            "curved path it overshoots. <bookmark mark='a'/> Heun's method takes that Euler step, measures the slope "
            "where it lands, and redoes the step with the average of the two slopes: second order, so halving the "
            "step cuts the error by four, for two network evaluations a step. EDM's last step is plain Euler. "
            f"<bookmark mark='b'/> On our letters, {low}at {nfe_h[j31]} evaluations Heun's error is {ratio:.1f} times "
            f"smaller than Euler's, and at {nfe_h[j63]}, {ratio63:.1f} times. With these two ideas and a careful spacing of the steps, Karras and colleagues "
            "reached an FID of 1.79 on CIFAR-10 with thirty-five evaluations."
        ) as vo:
            self.play(FadeIn(tag), Create(arc), FadeIn(ends), FadeIn(labs[0]))
            self.play(GrowArrow(eu), FadeIn(labs[1]))
            vo.wait_until("a")
            self.play(GrowArrow(sl2), FadeIn(labs[2]))
            self.play(GrowArrow(he), FadeIn(labs[3]))
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
