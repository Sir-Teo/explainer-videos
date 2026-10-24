from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (DATA, DDPM_C, PART, SOLVER_C, SOLVER_NAME, Panel, legend, load, log_axes, logcurve,
                                   take_away)

DET = ["euler_vp", "ddim", "heun", "dpm2", "dpmpp2m"]
SPOKEN = {"euler_vp": "plain Euler in time", "ddim": "DDIM", "heun": "Heun", "dpm2": "DPM-Solver-2",
          "dpmpp2m": "DPM-Solver plus plus"}


def at(rows, nfe):
    """The row whose number of evaluations is closest to nfe."""
    return min(rows, key=lambda r: abs(r["nfe"] - nfe))


class DPMSolver(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.second()
        self.compare()
        self.network()

    def card(self):
        card = chapter_card(9, r"DPM-Solver: an exact linear part", r"Can a solver use what it knows about the equation?",
                            part=PART)
        with self.voiceover("Chapter nine. DPM-Solver: an exact linear part."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\frac{dx}{d\sigma}", r"=", r"\frac{x}{\sigma} - \frac{D(x; \sigma)}{\sigma}", font_size=34),
            cmath(r"\frac{d}{d\sigma}\Big(\frac{x}{\sigma}\Big)", r"=", r"-\frac{D(x; \sigma)}{\sigma^2}", font_size=34),
            cmath(r"x_t", r"=", r"\frac{\sigma_t}{\sigma_s}\, x_s + \sigma_t \int_{\lambda_s}^{\lambda_t} e^{\lambda}\, "
                  r"D(x_\lambda)\, d\lambda, \qquad \lambda = -\log \sigma", font_size=32),
            cmath(r"x_t", r"=", r"\frac{\sigma_t}{\sigma_s}\, x_s + \Big(1 - \frac{\sigma_t}{\sigma_s}\Big)\, D(x_s)", font_size=34),
        ]
        whys = [why(r"a linear part, \ and the network's part"), why(r"the linear part, \ solved exactly"),
                why(r"integrate from $\sigma_s$ to $\sigma_t$"), why(r"$D$ held fixed: \ exactly DDIM's step")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.2, buff=0.5, edge=6.85)
        cite_ = cite(r"C.~Lu, Y.~Zhou, F.~Bao, J.~Chen, C.~Li \& J.~Zhu, \textit{DPM-Solver} (2022); \ \textit{DPM-Solver++} "
                     r"(2022)", corner=DR, font_size=18)
        with self.voiceover(
            "In 2022 Cheng Lu and colleagues at Tsinghua noticed that the ODE has a part that needs no network. "
            "<bookmark mark='a'/> The x over sigma term is linear in x, and can be solved exactly, the way you solve "
            "a linear equation with an integrating factor. <bookmark mark='b'/> What is left is an integral of the "
            "denoiser over the step, weighted by an exponential in lambda, minus the log of sigma. Only that "
            "integral needs approximating. Methods like this are called exponential integrators. "
            "<bookmark mark='c'/> Hold the denoiser fixed over the step, and out comes exactly DDIM's update. So "
            "DDIM was already the first-order exponential integrator; it is exact whenever the clean guess doesn't "
            "change during the step."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def second(self):
        g = axes([0, 4], [0, 3], x_length=7.0, y_length=3.0, xlabel=r"$\lambda = -\log\sigma$: \ noise falling",
                 ylabel=r"the denoiser's output along one path", xticks=[], yticks=[], center=[-2.4, 0.3, 0])
        xs = np.linspace(0, 4, 100)
        f = lambda x: 1.2 + 0.9 * np.tanh(1.1 * (x - 1.8)) + 0.15 * x
        true = curve(g.ax, xs, f(xs), DATA, 3, smooth=True)
        s0, s1, s2 = 1.0, 2.0, 3.0
        pts = VGroup(*[Dot(g.ax.c2p(x, f(x)), radius=0.07, color=WHITE) for x in (s0, s1)])
        held = Line(g.ax.c2p(s1, f(s1)), g.ax.c2p(s2, f(s1)), color=SOLVER_C["ddim"], stroke_width=4)
        slope = (f(s1) - f(s0)) / (s1 - s0)
        lin = Line(g.ax.c2p(s1, f(s1)), g.ax.c2p(s2, f(s1) + slope * (s2 - s1)), color=SOLVER_C["dpmpp2m"], stroke_width=4)
        mid = Dot(g.ax.c2p((s1 + s2) / 2, f((s1 + s2) / 2)), radius=0.07, color=SOLVER_C["dpm2"])
        labs = VGroup(label(r"first order: \ hold $D$ fixed \ (DDIM)", font_size=20, color=SOLVER_C["ddim"]),
                      label(r"DPM-Solver-2: \ one extra evaluation, \ halfway", font_size=20, color=SOLVER_C["dpm2"]),
                      label(r"DPM-Solver++(2M): \ reuse the last step's $D$, \ extend the line", font_size=20,
                            color=SOLVER_C["dpmpp2m"])).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.8, 0.9, 0])
        tag = note(r"schematic").to_corner(UL, buff=0.3)
        pub = label(r"DPM-Solver on CIFAR-10: \ FID $4.70$ in $10$ evaluations, \ $2.87$ in $20$", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To do better, approximate how the denoiser changes over the step. <bookmark mark='a'/> DPM-Solver-2 "
            "spends one extra evaluation halfway through the step, in lambda, and uses the denoiser there. "
            "<bookmark mark='b'/> DPM-Solver plus plus, in its two-step multistep form, spends nothing extra: it "
            "reuses the denoiser from the previous step and extends the line through the two. One network evaluation "
            "per step, second order. <bookmark mark='c'/> On CIFAR-10 the first version reached an FID of 4.70 in ten "
            "evaluations, and 2.87 in twenty; the multistep form ships in the common diffusion libraries."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(g), Create(true), FadeIn(pts), Create(held), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(mid, scale=1.5), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(Create(lin), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(FadeIn(pub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        s = load("solvers")
        errs = np.array([r["err"] for k in DET for r in s[k]])
        lo, hi = math.floor(math.log10(max(errs.min(), 1e-4))), math.ceil(math.log10(errs.max()))
        g = log_axes([math.log10(3), math.log10(130)], [lo, hi], x_length=7.0, y_length=4.8,
                     xlabel=r"network evaluations", ylabel=r"error at the end, \ against the exact solution",
                     xticks=[4, 8, 16, 32, 64, 128], yticks=[10.0 ** k for k in range(lo, hi + 1)],
                     yfmt=lambda v: f"10^{{{int(round(math.log10(v)))}}}", center=[-2.8, -0.2, 0])
        lines = VGroup(*[logcurve(g.ax, [r["nfe"] for r in s[k]], [max(r["err"], 10.0 ** lo) for r in s[k]],
                                  SOLVER_C[k], radius=0.04) for k in DET])
        lg = legend([(SOLVER_C[k], SOLVER_NAME[k]) for k in DET], font_size=18).move_to([4.6, 2.85, 0])
        # the same numbers, read off at three budgets
        budgets = (8, 16, 32)
        trow = [VGroup(label(r"about", font_size=18, color=GREY_B),
                       *[MathTex(str(b), font_size=22, color=GREY_A) for b in budgets])]
        for k in DET:
            trow.append(VGroup(label(SOLVER_NAME[k], font_size=17, color=SOLVER_C[k]),
                               *[MathTex(f"{at(s[k], b)['err']:.3f}", font_size=22, color=SOLVER_C[k]) for b in budgets]))
        tbl = VGroup()
        for i, r_ in enumerate(trow):
            for j, c_ in enumerate(r_):
                c_.move_to([2.6 + (0 if j == 0 else 0.9 + 0.9 * j), 1.1 - 0.33 * i, 0])
                if j == 0:
                    c_.align_to([1.75, 0, 0], LEFT)
            tbl.add(r_)
        tbh = label(r"error, \ at about this many evaluations", font_size=17, color=GREY_B).next_to(tbl, UP, buff=0.1)
        dd = s["ddpm"]
        fl = float(s["floor"])
        g2 = log_axes([math.log10(3), math.log10(130)], [-2, 0], x_length=3.6, y_length=1.5, xlabel=r"evaluations",
                      ylabel=r"DDPM: \ distance from the data", xticks=[4, 16, 64], yticks=[0.01, 0.1, 1],
                      center=[4.4, -2.45, 0], font_size=18)
        ddl = logcurve(g2.ax, [r["nfe"] for r in dd], [r["sw"] for r in dd], DDPM_C, radius=0.035)
        fll = DashedLine(g2.ax.c2p(math.log10(3), math.log10(fl)), g2.ax.c2p(math.log10(130), math.log10(fl)), color=GREY_B,
                         stroke_width=1.5)
        b8 = min(DET, key=lambda k: at(s[k], 8)["err"])
        b32 = min(DET, key=lambda k: at(s[k], 32)["err"])
        e8 = at(s[b8], 8)
        r32 = at(s["ddim"], 32)["err"] / max(at(s[b32], 32)["err"], 1e-9)
        eu, dm = at(s["euler_vp"], 16)["err"], at(s["ddim"], 16)["err"]
        euler_note = (f"One surprise: on our letters, plain Euler in the variance-preserving time beats DDIM, "
                      f"{eu:.3f} against {dm:.3f} at sixteen. DDIM is exact when the clean guess stays fixed; Euler, when "
                      "the velocity does. Which first-order method wins depends on the data." if eu < dm else
                      f"Plain Euler in time trails DDIM, {eu:.3f} against {dm:.3f} at sixteen: holding the clean guess "
                      "fixed is the better first-order bet.")
        n_ok = next((r["nfe"] for r in dd if r["sw"] < 1.5 * fl), None)
        ddpm_note = (f"DDPM, with its fresh noise, has no single path to compare; its samples come within half again of "
                     f"the floor only at {n_ok} evaluations." if n_ok else
                     "DDPM, with its fresh noise, has no single path to compare, and even at 128 evaluations its samples "
                     "are well short of the floor.")
        with self.voiceover(
            "Here is the whole family on our letters, run with the exact denoiser so that the only error is the "
            "solver's, all on EDM's spacing, from the same noise. The error is measured against the exact solution "
            "of the ODE. <bookmark mark='a'/> On log scales, a first-order method's line has slope minus one, a "
            "second-order method's minus two. <bookmark mark='b'/> With about eight evaluations the best is "
            f"{SPOKEN[b8]}, at {e8['err']:.3f}. With about thirty-two, {SPOKEN[b32]} is {r32:.0f} times more accurate "
            f"than DDIM. <bookmark mark='c'/> {euler_note} <bookmark mark='d'/> {ddpm_note}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("a")
            self.play(*[Indicate(l_[0], color=SOLVER_C[k], scale_factor=1.0) for l_, k in zip(lines, DET)], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(tbl), FadeIn(tbh), Indicate(lines[DET.index(b8)][0], color=SOLVER_C[b8]))
            vo.wait_until("c")
            self.play(Indicate(lines[0][0], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(g2), Create(ddl), Create(fll))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def network(self):
        s, n = load("solvers"), load("solvers_net")
        kinds = ["ddim", "heun", "dpmpp2m"]
        budget = 12
        panels = Group()
        for i, k in enumerate(kinds + ["ref"]):
            pn = Panel(3.2, center=[-5.025 + 3.35 * i, 1.2, 0])
            P = np.asarray(s["pic_ref"] if k == "ref" else s["pic_" + k + str(budget)])
            col = DATA if k == "ref" else SOLVER_C[k]
            nm = r"the exact solution" if k == "ref" else SOLVER_NAME[k]
            panels.add(Group(pn, pn.scatter(P, col, radius_px=1.4, res=260),
                             label(nm, font_size=20, color=col).next_to(pn, UP, buff=0.1)))
        sub = label(rf"about ${budget}$ evaluations, \ the same $600$ starting points", font_size=20, color=GREY_A).next_to(
            panels, DOWN, buff=0.15)
        r16 = {k: at(n[k], 16)["err"] for k in kinds}
        rs16 = {k: at(s[k], 16)["err"] for k in kinds}
        same_order = sorted(kinds, key=lambda k: r16[k]) == sorted(kinds, key=lambda k: rs16[k])
        net_ref, fl = float(n["ref_sw"]), float(n["floor"])
        tab = VGroup(label(r"with our trained network instead of the exact denoiser, \ about $16$ evaluations:", font_size=20,
                           color=GREY_A),
                     *[label(rf"{SOLVER_NAME[k]}: \ ${r16[k]:.3f}$ \ (exact: ${rs16[k]:.3f}$)", font_size=20, color=SOLVER_C[k])
                       for k in kinds],
                     label(rf"the network's own exact ODE: \ ${net_ref:.3f}$ from the data \ (floor ${fl:.3f}$)", font_size=20,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, -2.3, 0])
        eb = {k: at(s[k], budget)["err"] for k in kinds}
        bs, ws = SPOKEN[min(kinds, key=lambda k: eb[k])], SPOKEN[max(kinds, key=lambda k: eb[k])]
        close_note = f"{bs}'s points are the closest to it, and {ws}'s are the furthest off."
        verdict = ("With our trained network in place of the exact denoiser, the ranking is the same, "
                   if same_order else "With our trained network in place of the exact denoiser, the ranking shifts, ")
        with self.voiceover(
            f"Here are three of them after about {budget} evaluations, beside the exact solution. {close_note} "
            "<bookmark mark='a'/> " + verdict
            + f"and the network's own error sets a floor: solved exactly, its ODE lands {net_ref:.3f} from the data, "
            f"against {fl:.3f} for a fresh sample of the letters. <bookmark mark='b'/> Ten to thirty evaluations, then, "
            "with a solver that knows the equation. Fewer than that needs a different idea: chapter twelve."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.25), FadeIn(sub), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()
