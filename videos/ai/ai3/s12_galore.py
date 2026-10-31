from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import GRAD, HIST, chapter, dots_on, load

MC = {"adam": C.ADAMW, "galore32": C.REWARD, "galore8": C.BITS, "adamsplit": GREY_B}
MN = {"adam": r"Adam", "galore32": r"GaLore, \ rank $32$", "galore8": r"GaLore, \ rank $8$",
      "adamsplit": r"Adam, \ GaLore's step sizes"}


def runs_of(g, ctl, m):
    """The three seeds of a method at its best learning rate."""
    if m == "adamsplit":
        b = ctl["best_lr"]
        return [ctl["runs"][f"adamsplit_{b:g}_{s}"] for s in range(3)], b
    b = g["best_lr"][m]
    return [g["runs"][f"{m}_{b:g}_{s}"] for s in range(3)], b


class GaLore(VoiceoverScene):
    def construct(self):
        chapter(self, 11, r"Gradients are low rank", r"How much of a gradient matters?",
                "Chapter eleven. Gradients are low rank.")
        self.derive()
        self.measured()
        self.method()
        self.compare()
        self.lora()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\boldsymbol{\delta}_t": GRAD, r"\mathbf{x}_t^{\top}": C.TRUE_P, "G": GRAD}
        rows = [
            cmath(r"\mathbf{y}_t", "=", r"W\mathbf{x}_t", font_size=36),
            cmath(r"\frac{\partial L}{\partial W_{ij}}", "=", r"\textstyle\sum_t \frac{\partial L}{\partial y_{t,i}}\, x_{t,j}",
                  font_size=36),
            cmath("G", "=", r"\textstyle\sum_t", r"\boldsymbol{\delta}_t", r"\mathbf{x}_t^{\top}", font_size=40,
                  colors=colors),
            cmath(r"\operatorname{rank} G", r"\le", r"\min(T,\ m,\ n)", font_size=36),
        ]
        whys = [why(r"one token $t$ through a layer"), why(r"the chain rule"),
                why(r"a sum of outer products: \ rank one each"), why(r"at most one new direction per token")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.2, buff=0.45, edge=6.9)
        tag = note(r"$\boldsymbol{\delta}_t = \partial L/\partial \mathbf{y}_t$, \ the error signal arriving from above "
                   r"(Part 4)").to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A gradient is a matrix too, with its own singular values. <bookmark mark='a'/> A layer turns each "
            "token's vector x into W x. <bookmark mark='b'/> By the chain rule, Part 4's subject, the gradient for one "
            "weight sums, over tokens, the error at that output times the input. <bookmark mark='c'/> So the gradient is "
            "a sum of outer products, rank one per token. <bookmark mark='d'/> Its rank is at most the number of tokens. "
            "In practice it is often approximately low rank: errors and inputs concentrate in a few directions."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        g = load("galore")
        tr = g["track"]["tracked"]
        shape = tr[0]["shape"]
        n = len(tr[0]["s"])
        steps = [e["step"] for e in tr]
        pk = max(tr, key=lambda e: e["top8"])
        show = [tr[0], pk, tr[-1]]
        cols = [GREY_B, C.BITS, GRAD]
        ga = axes([0, n, 32], [-3.5, 0, 1], x_length=5.6, y_length=3.6, xticks=[0, 32, 64, 96, 128],
                  yticks=[-3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}" if v else "1",
                  xlabel=r"singular value, \ largest first", ylabel=r"$\sigma_i / \sigma_1$", center=[-3.4, -0.5, 0])
        ax = ga.ax
        spec = VGroup()
        leg = VGroup()
        for e, col in zip(show, cols):
            s = np.maximum(np.asarray(e["s"]), 10 ** -3.5)
            spec.add(curve(ax, np.arange(len(s)) + 0.5, np.log10(s), col, 3))
            leg.add(label(rf"step ${e['step']}$", font_size=20, color=col))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(n, 0), DL, buff=0.1)
        gb = axes([0, math.log10(600), 1], [0, 1.02, 0.25], x_length=5.0, y_length=3.6, xticks=[0, 1, 2],
                  yticks=[0, 0.5, 1.0], xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)],
                  xlabel=r"training step", ylabel=r"share of $\|G\|_F^2$ in the top $8$ directions",
                  center=[3.6, -0.5, 0])
        bx = gb.ax
        ls = np.log10(steps)
        t8 = [e["top8"] for e in tr]
        share = VGroup(curve(bx, ls, t8, GRAD, 3), dots_on(bx, ls, t8, GRAD, 0.05))
        replay_step = ValueTracker(float(steps[0]))
        cursor = always_redraw(lambda: Dot(bx.c2p(math.log10(replay_step.get_value()),
                                                 float(np.interp(math.log10(replay_step.get_value()), ls, t8))),
                                           radius=0.085, color=WHITE, stroke_color=BACKGROUND, stroke_width=1))
        cap = note(r"spectra: first, peak top-$8$ share, final step; \ cursor follows the same step \\ "
                   r"right: full measured trajectory; \ spectral ratios below $10^{-3.5}$ shown at the floor",
                   font_size=17).to_edge(DOWN, buff=0.15)
        head = label(rf"A real gradient: \ one ${shape[0]} \times {shape[1]}$ matrix of a small transformer, \ "
                     r"trained on the novels", font_size=28).to_edge(UP, buff=0.3)
        lo = min(t8)
        last = tr[-1]
        with self.voiceover(
            "Here is a real gradient, from a small transformer trained on the novels: one "
            f"{shape[0]} by {shape[1]} matrix. <bookmark mark='a'/> Its singular values, largest first, on a log scale. "
            f"At step {tr[0]['step']}, the top eight carry {100 * tr[0]['top8']:.1f} percent of squared gradient "
            f"energy. <bookmark mark='b'/> The largest measured top-eight share is at step {pk['step']}: "
            f"{100 * pk['top8']:.1f} percent. <bookmark mark='c'/> At the final step, {last['step']}, it is "
            f"{100 * last['top8']:.1f} percent, of {n} possible directions. The cursor aligns each spectrum with "
            "its position on the full energy-share trajectory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ga), FadeIn(gb))
            vo.wait_until("a")
            self.play(Create(spec[0]), FadeIn(leg[0]), Create(share))
            self.add(cursor)
            vo.wait_until("b")
            self.play(Create(spec[1]), FadeIn(leg[1]), replay_step.animate.set_value(pk["step"]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(spec[2]), FadeIn(leg[2]), replay_step.animate.set_value(last["step"]), run_time=2.0)
        cursor.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def method(self):
        g = load("galore")
        r_adam = g["runs"][f"adam_{g['best_lr']['adam']:g}_0"]
        mems = {m: g["runs"][f"{m}_{g['best_lr'][m]:g}_0"]["opt_numbers"] for m in ("adam", "galore32", "galore8")}
        W = int(r_adam["weights"])
        rows = [
            cmath(r"R", "=", r"P^{\top} G", font_size=36, colors={"R": C.REWARD, "G": GRAD}),
            cmath(r"\Delta W", "=", r"-\eta\, P\ \mathrm{Adam}(R)", font_size=36, colors={"R": C.REWARD}),
        ]
        whys = [why(r"left projection shown; \ implementation projects the shorter side \\ $P$: top $r$ singular vectors, refreshed every $T$ steps",
                    font_size=21),
                why(r"Adam's two running averages live on $R$, \ not on $G$")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-2.0, buff=0.45, edge=6.9)
        hist = history_card(2024, r"J.~Zhao, \ Y.~Tian, \ A.~Anandkumar et al., \ GaLore",
                            r"up to $65.5\%$ less optimizer memory in pretraining; \ with 8-bit states and per-layer "
                            r"updates, \ a 7-billion-parameter model pretrained on one 24-GB GPU", color=HIST,
                            width=5.6).move_to([-3.6, -1.6, 0])
        bars = VGroup()
        top = max(mems.values())
        for k, m in enumerate(("adam", "galore32", "galore8")):
            w = 4.2 * mems[m] / top
            y = -0.9 - 0.75 * k
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=MC[m], fill_opacity=0.85)
            b.move_to([1.6, y, 0], aligned_edge=LEFT)
            nm = label(MN[m], font_size=22, color=MC[m]).move_to([1.4, y, 0], aligned_edge=RIGHT)
            v = MathTex(fmt_int(mems[m]), font_size=24, color=MC[m]).next_to(b, RIGHT, buff=0.12)
            bars.add(VGroup(nm, b, v))
        bt = label(rf"numbers the optimizer keeps for our model's \\ ${fmt_int(W)}$ block weights",
                   font_size=22, color=GREY_A).next_to(bars, UP, buff=0.25)
        cells = VGroup()
        for k, (t_, col) in enumerate(((r"weight", C.ADAMW), (r"mean of $g$", C.REWARD), (r"mean of $g^2$", C.BITS))):
            box = Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.75)
            cells.add(VGroup(box, label(t_, font_size=20, color=BACKGROUND).move_to(box)))
        cells.arrange(RIGHT, buff=0.08)
        adam_pic = VGroup(cells, label(r"Adam keeps three numbers per weight", font_size=22, color=GREY_A)
                          .next_to(cells, UP, buff=0.12)).move_to([3.4, 0.55, 0])
        with self.voiceover(
            "That is GaLore's idea, from Jiawei Zhao, Anima Anandkumar, Yuandong Tian and colleagues in 2024. Adam keeps "
            "two running averages per weight: fourteen billion extra numbers for a seven-billion-parameter model. "
            "<bookmark mark='a'/> GaLore projects each gradient onto its top r singular directions <bookmark mark='b'/> "
            "and runs Adam there, refreshing the directions now and then. <bookmark mark='c'/> For our model: "
            f"{mems['adam']:,} numbers with Adam, {mems['galore32']:,} at rank 32, "
            f"{mems['galore8']:,} at rank 8. At scale the paper reports up to 65 percent less optimizer memory, "
            "and, with 8-bit states, a seven-billion-parameter model pretrained on one 24-gigabyte card."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.2))
            self.play(FadeIn(adam_pic))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(bt), LaggedStart(*[AnimationGroup(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
                                                for b_ in bars], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        g, ctl = load("galore"), load("galorectl")
        steps = int(g["steps"])
        methods = ("adam", "adamsplit", "galore32", "galore8")
        res = {m: runs_of(g, ctl, m) for m in methods}
        smoothing = 8
        smoothed = {m: np.array([np.convolve(np.asarray(r["curve"]), np.ones(smoothing) / smoothing, mode="valid")
                                 for r in res[m][0]]) for m in methods}
        low = min(v.min() for v in smoothed.values()) - 0.1
        high = max(v.max() for v in smoothed.values()) + 0.1
        ga = axes([0, steps, 100], [low, high, (high - low) / 4], x_length=6.0, y_length=3.8,
                  xticks=[0, 200, 400, 600], yticks=list(np.linspace(low, high, 5)), yfmt=lambda v: f"{v:.1f}",
                  xlabel=r"step", ylabel=r"training loss \ (nats per token)", center=[-3.3, -0.4, 0])
        ax = ga.ax
        curves = {}
        bands = {}
        for m in methods:
            values = smoothed[m]
            xs = (np.arange(values.shape[1]) + smoothing - 1) * 5 + 1
            curves[m] = curve(ax, xs, values.mean(axis=0), MC[m], 3)
            points = [ax.c2p(x, y) for x, y in zip(xs, values.min(axis=0))]
            points += [ax.c2p(x, y) for x, y in zip(xs[::-1], values.max(axis=0)[::-1])]
            bands[m] = Polygon(*points, stroke_width=0, fill_color=MC[m], fill_opacity=0.12)
        rows = VGroup()
        vals = {m: [r["val"] for r in res[m][0]] for m in methods}
        for m in methods:
            v = np.asarray(vals[m])
            rows.add(VGroup(label(MN[m], font_size=22, color=MC[m]),
                            MathTex(rf"{v.mean():.3f}", font_size=28, color=MC[m]),
                            MathTex(rf"[{v.min():.3f},\ {v.max():.3f}]", font_size=22, color=GREY_B),
                            MathTex(rf"\eta = {res[m][1]:g}", font_size=22, color=GREY_B)))
        hdr = VGroup(label(r"method", font_size=20, color=GREY_B), label(r"held-out loss", font_size=20, color=GREY_B),
                     label(r"3 seeds", font_size=20, color=GREY_B), label(r"best $\eta$", font_size=20, color=GREY_B))
        tab = VGroup(hdr, *rows)
        for r in tab:
            r.arrange(RIGHT, buff=0.3)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        regrid(tab, gap=0.3)
        if tab.width > 6.4:
            tab.scale_to_fit_width(6.4)
        tab.move_to([3.4, 0.2, 0])
        cap = note(r"$600$ steps of $16\times64$ tokens; \ three learning rates selected on seed $0$ validation \\ "
                   r"selected rate run on seeds $0,1,2$; \ mean with min--max band; \ $8$-sample moving average",
                   font_size=17).to_edge(DOWN, buff=0.15)
        mean = {m: float(np.mean(vals[m])) for m in methods}
        spread = max(max(vals[m]) - min(vals[m]) for m in methods)
        gap = mean["adam"] - mean["galore32"]
        split_share = (mean["adam"] - mean["adamsplit"]) / gap if gap > 0 else 0.0
        if gap > spread and split_share > 0.5 and mean["adamsplit"] > mean["galore32"] + spread / 2:
            verdict = (f"GaLore wins, but most of the gap, {100 * split_share:.0f} percent, comes from GaLore's smaller steps for the "
                       "matrices, which let the rest train at the full rate: Adam given the same step sizes reaches "
                       f"{mean['adamsplit']:.3f}. The low-rank window adds the remaining improvement in this experiment.")
        elif gap > spread and split_share > 0.5:
            verdict = ("The gap comes from GaLore's smaller steps for the matrices: Adam given the same step sizes "
                       f"does as well within the measured spread, {mean['adamsplit']:.3f}.")
        elif gap > spread:
            verdict = ("Adam given GaLore's step sizes does not close the gap: here, the low-rank window itself "
                       "helped.")
        elif abs(gap) <= spread:
            verdict = "GaLore matches Adam within the spread of the seeds, with a fraction of the memory."
        else:
            verdict = "GaLore falls short of Adam here, the price of its smaller memory at this scale."
        with self.voiceover(
            "Does a narrow window cost anything? We trained the model with Adam and with GaLore at ranks 32 and 8, "
            "each at its best of three learning rates chosen using seed zero's validation result. We then run "
            "that rate on seeds zero, one and two; the reported three include the tuning seed. "
            "<bookmark mark='a'/> Training curves show the mean and minimum-to-maximum band after an eight-sample "
            "moving average, with no hard loss clipping. <bookmark mark='b'/> The held-out loss: Adam "
            f"{mean['adam']:.3f}, rank 32 {mean['galore32']:.3f}, rank 8 {mean['galore8']:.3f}. <bookmark mark='c'/> "
            f"{verdict}"
        ) as vo:
            self.play(FadeIn(ga), FadeIn(cap))
            vo.wait_until("a")
            self.play(*[FadeIn(bands[m]) for m in ("adam", "galore32", "galore8")],
                      *[Create(curves[m]) for m in ("adam", "galore32", "galore8")], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr), *[FadeIn(rows[i]) for i in (0, 2, 3)])
            vo.wait_until("c")
            self.play(FadeIn(bands["adamsplit"]), Create(curves["adamsplit"]), FadeIn(rows[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lora(self):
        g = load("galore")
        name = "blocks.1.mlp.up.weight"
        r8 = g["runs"][f"galore8_{g['best_lr']['galore8']:g}_0"]["dW"][name]
        ra = g["runs"][f"adam_{g['best_lr']['adam']:g}_0"]["dW"][name]
        full = int(r8["rank"])
        lo = VGroup(MathTex(r"W + BA", font_size=40, color=C.REWARD),
                    label(r"LoRA (2021): \ the \textit{change} has rank $r$, \ always", font_size=26, color=GREY_A))
        ga = VGroup(MathTex(r"W - \eta\,\textstyle\sum_t P_t\,\mathrm{Adam}(R_t)", font_size=36, color=C.BITS),
                    label(r"GaLore: \ each \textit{step} has rank $r$; \ the window moves", font_size=26, color=GREY_A))
        for v in (lo, ga):
            v.arrange(DOWN, buff=0.2)
        VGroup(lo, ga).arrange(RIGHT, buff=1.2).move_to(UP * 1.3)
        res = VGroup(
            label(rf"measured, \ after $600$ steps: \ effective rank of the total change $\Delta W$ \ "
                  rf"(of ${full}$ possible)", font_size=26),
            label(rf"GaLore at rank $8$: \ ${r8['eff']:.0f}$; \qquad Adam: \ ${ra['eff']:.0f}$", font_size=30,
                  color=C.BITS),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        note_ = note(r"effective rank: \ $e^{\,\text{entropy of the normalized singular values}}$ (Roy \& Vetterli, "
                     r"2007)").to_edge(DOWN, buff=0.3)
        more = r8["eff"] > 8
        tail = ("so its total change is far richer than rank 8. That is GaLore's answer to LoRA's limit; Part 27 "
                "uses LoRA where a small change is all that's wanted." if more else
                "close to the window's own rank.")
        with self.voiceover(
            "Compare LoRA, Part 27's tool. <bookmark mark='a'/> LoRA fixes the change to the weights at rank r for good. "
            "<bookmark mark='b'/> GaLore makes each step low rank, but the window moves. <bookmark mark='c'/> After 600 "
            f"steps, the total change to one matrix has an effective rank of {r8['eff']:.0f} with the rank-8 window, "
            f"against {ra['eff']:.0f} for Adam: {tail}"
        ) as vo:
            self.play(FadeIn(lo[0]), FadeIn(ga[0]))
            vo.wait_until("a")
            self.play(FadeIn(lo[1]), Indicate(lo[0], color=C.REWARD))
            vo.wait_until("b")
            self.play(FadeIn(ga[1]), Indicate(ga[0], color=C.BITS))
            vo.wait_until("c")
            self.play(FadeIn(res), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
