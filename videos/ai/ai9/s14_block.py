from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import GATE, NEURON, NORM, PART, PLAIN, RES, WEIGHT, load

VARIANT = {  # name on screen, colour
    "plain": (r"plain: \ no residual", PLAIN),
    "residual": (r"$+$ residual", RES),
    "post_ln": (r"$+$ post-LayerNorm", C.SURPRISE),
    "pre_ln": (r"$+$ pre-LayerNorm", NORM),
    "pre_rms": (r"$+$ pre-RMSNorm", C.TRUE_P),
    "pre_rms_swiglu": (r"$+$ pre-RMSNorm $+$ SwiGLU", GATE),
}

SPOKEN = {"plain": "the plain stack", "residual": "the residual stack without normalization",
          "post_ln": "post-LayerNorm", "pre_ln": "pre-LayerNorm", "pre_rms": "pre-RMSNorm without the gate",
          "pre_rms_swiglu": "the full block"}


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def sig(x):
    return 1 / (1 + math.exp(-x))


class Block(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.activations()
        self.gating()
        self.assembly()
        self.ablation()

    def card(self):
        card = chapter_card(13, r"The modern block", r"What is inside each layer of today's language models?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter thirteen. The modern block."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def activations(self):
        ax = CornerAxes(x_range=[-4, 4, 1], y_range=[-1.2, 4, 1], x_length=6.6, y_length=4.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.0, -0.5, 0])
        zero = VGroup(DashedLine(ax.c2p(-4, 0), ax.c2p(4, 0), dash_length=0.05, stroke_width=1, color=GREY_D),
                      DashedLine(ax.c2p(0, -1.2), ax.c2p(0, 4), dash_length=0.05, stroke_width=1, color=GREY_D))
        fns = [
            (r"sigmoid \ (1980s)", lambda x: sig(x), GREY_B),
            (r"tanh", math.tanh, GREY_C),
            (r"ReLU \ (2010)", lambda x: max(x, 0.0), NEURON),
            (r"GELU: \ $x\,\Phi(x)$ \ (2016)", lambda x: x * phi(x), C.BITS),
            (r"SiLU: \ $x\,\sigma(x)$ \ (2017)", lambda x: x * sig(x), C.MODEL_Q),
        ]
        plots = [ax.plot(f, x_range=[-4, 4, 0.02], color=c, stroke_width=3.5) for _, f, c in fns]
        names = VGroup(*[label(t, font_size=22, color=c) for t, _, c in fns]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        names.next_to(ax.c2p(-4, 4), DR, buff=0.15)
        colors = {r"\Phi(x)": C.BITS, r"m": GATE}
        rows = [cmath(r"\text{out}", r"=", r"x \cdot m,", r"\quad m \sim \text{Bernoulli}\big(", r"\Phi(x)", r"\big)",
                      font_size=30, colors=colors),
                cmath(r"\mathbb{E}[\text{out}]", r"=", r"x\, ", r"\Phi(x)", font_size=30, colors=colors)]
        whys = [why(r"keep $x$ with the probability that \\ a standard Gaussian is below it"),
                why(r"average over the coin: \ GELU")]
        step = ladder(self, rows, whys, keep=2, top=2.8, x=3.6, buff=0.6, edge=6.9, align_index=None)
        dead = label(r"ReLU's slope is $0$ for every $x < 0$: \\ a unit that never fires never learns", font_size=22,
                     color=GREY_A).move_to([3.6, -1.0, 0])
        where = label(r"GELU: \ BERT, GPT-2; \ \ SiLU: \ inside SwiGLU \\ (from the published configurations)",
                      font_size=22, color=GREY_A).move_to([3.6, -2.4, 0])
        cite_ = cite(r"D.~Hendrycks \& K.~Gimpel (2016); \ S.~Elfwing, E.~Uchibe \& K.~Doya (2017); \ P.~Ramachandran, "
                     r"B.~Zoph \& Q.~Le (2017)", corner=DL)
        with self.voiceover(
            "Inside today's blocks, the bend itself has changed. <bookmark mark='a'/> The S-shaped sigmoid and tanh of "
            "the eighties and nineties flatten out at both ends, which helped gradients vanish. <bookmark mark='b'/> The "
            "ReLU doesn't, on the positive side, but its slope is exactly zero for every negative input, so a unit "
            "that stops firing stops learning. <bookmark mark='c'/> In 2016 Dan Hendrycks and Kevin Gimpel derived a "
            "smooth version from a coin flip: keep the input x with the probability that a standard Gaussian falls "
            "below it. <bookmark mark='d'/> Averaged over the coin, that's x times Phi of x, the GELU, used in BERT "
            "and GPT-2. <bookmark mark='e'/> Its cousin, x times the sigmoid of x, called SiLU or Swish, came from "
            "reinforcement learning and from an automated search in 2017. Both are smooth, both dip slightly below "
            "zero, and both pass a little gradient for negative inputs."
        ) as vo:
            self.play(Create(ax), FadeIn(zero), FadeIn(cite_))
            self.play(Create(plots[0]), Create(plots[1]), FadeIn(names[0]), FadeIn(names[1]))
            vo.wait_until("a")
            self.play(Indicate(VGroup(plots[0], plots[1]), scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(plots[2]), FadeIn(names[2]), FadeIn(dead))
            vo.wait_until("c")
            step(0)
            vo.wait_until("d")
            step(1)
            self.play(Create(plots[3]), FadeIn(names[3]))
            vo.wait_until("e")
            self.play(Create(plots[4]), FadeIn(names[4]), FadeIn(where))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gating(self):
        cfg = load("configs")
        rows = {r["name"]: r for r in cfg["rows"]}
        ax = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-1.5, 1.5, 1], x_length=4.4, y_length=4.4,
                        z_length=2.6, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.shift(LEFT * 3.2 + DOWN * 0.2)
        silu = lambda x: x / (1 + math.exp(-x))  # noqa: E731

        def surf(f, col_lo, col_hi):
            s = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=[-2, 2], v_range=[-2, 2], resolution=(28, 28),
                        fill_opacity=0.85, stroke_width=0.3, stroke_color=BACKGROUND, checkerboard_colors=False)
            s.set_fill_by_value(axes=ax, colorscale=[(col_lo, -1.2), (GREY_D, 0.0), (col_hi, 1.2)], axis=2)
            return s

        s_relu = surf(lambda x, y: max(x, 0.0) * 0.6, NEURON, NEURON)
        s_gate = surf(lambda x, y: silu(x) * y * 0.35, C.MODEL_Q, GATE)
        colors = {r"\odot": GATE}
        glu = cmath(r"\operatorname{FFN}(x)", r"=", r"W_2\big(\operatorname{SiLU}(W_1 x)", r"\odot", r"W_3 x\big)",
                    colors=colors, font_size=32).to_corner(UR, buff=0.35)
        gl = label(r"SwiGLU: \ one projection gates the other, \ number by number", font_size=22, color=GREY_A)
        gl.next_to(glu, DOWN, buff=0.12).align_to(glu, RIGHT)
        cnt = cmath(r"3 \cdot d \cdot \tfrac{8}{3}d", r"=", r"8d^2", r"=", r"2 \cdot d \cdot 4d", font_size=30, color=C.BITS)
        cnt.next_to(gl, DOWN, buff=0.35).align_to(glu, RIGHT)
        cntl = label(r"three matrices instead of two: \ width $\tfrac83 d$ instead of $4d$", font_size=22, color=C.BITS)
        cntl.next_to(cnt, DOWN, buff=0.12).align_to(glu, RIGHT)
        tab = VGroup()
        for nm in ("GPT-2 (2019)", "Llama 2 7B (2023)", "Llama 3 8B (2024)", "Qwen3-8B (2025)"):
            r = rows[nm]
            tab.add(VGroup(label(nm, font_size=20, color=WHITE),
                           label(rf"$d = {r['d']:,}$".replace(",", "{,}"), font_size=20, color=GREY_A),
                           label(rf"MLP width ${r['f']:,}$".replace(",", "{,}") + (r" \ (gated)" if r["gated"] else ""),
                                 font_size=20, color=GATE if r["gated"] else NEURON),
                           label(rf"$= {r['ratio']:.2f}\,d$", font_size=20, color=C.BITS)))
        lefts = [0.35, 2.55, 3.85]
        for i, row in enumerate(tab):
            for j, m_ in enumerate(row):
                m_.move_to([0, -1.1 - 0.42 * i, 0])
                if j < 3:
                    m_.align_to([lefts[j], 0, 0], LEFT)
                else:
                    m_.align_to([6.9, 0, 0], RIGHT)
        src = note(r"published configurations \ (each model's config.json)").next_to(tab, DOWN, buff=0.15).align_to(tab, LEFT)
        surf_l1 = label(r"one ReLU unit: \ a fold", font_size=24, color=NEURON).to_corner(UL, buff=0.35)
        surf_l2 = label(r"one gated unit: \ $\operatorname{SiLU}(x_1) \cdot x_2$, \ a product", font_size=24,
                        color=GATE).to_corner(UL, buff=0.35)
        fixed = [glu, gl, cnt, cntl, *tab, src, surf_l1, surf_l2]
        for m_ in fixed:
            self.add_fixed_in_frame_mobjects(m_)
            self.remove(m_)
        l2 = rows["Llama 2 7B (2023)"]
        with self.voiceover(
            "The bigger change is the gate. <bookmark mark='a'/> A ReLU unit, as a surface over two inputs, is a "
            "fold: flat on one side, a ramp on the other. <bookmark mark='b'/> In 2016 Yann Dauphin and colleagues "
            "used gated units, which multiply one projection of the input by another. Here is the simplest: SiLU of "
            "one input, times the other. It's a saddle, a product: it can switch a feature on or off depending on "
            "something else. <bookmark mark='c'/> In 2020 Noam Shazeer tried variants inside the transformer's "
            "feed-forward layer, and SwiGLU won: SiLU of one projection, times a second projection, then a third "
            "matrix back down. His paper ends by attributing its success, as all else, to divine benevolence. "
            "<bookmark mark='d'/> Three matrices instead of two, so to keep the parameter count, the hidden width "
            "shrinks from four times the model width to eight thirds. <bookmark mark='e'/> In the published "
            f"configurations: GPT-2's plain MLP is four times its width; Llama 2's gated one, {l2['f']:,}, is eight "
            "thirds of 4,096 rounded up to a multiple of 256; later models go wider."
        ) as vo:
            self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.9)
            self.play(Create(ax), FadeIn(glu), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(s_relu), FadeIn(surf_l1))
            self.begin_ambient_camera_rotation(rate=0.12)
            vo.wait_until("b")
            self.play(Transform(s_relu, s_gate), FadeOut(surf_l1), FadeIn(surf_l2), run_time=2.0)
            vo.wait_until("d")
            self.play(Write(cnt), FadeIn(cntl))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.25), FadeIn(src), run_time=2.0)
            self.stop_ambient_camera_rotation()
        self.wait(0.3)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    @staticmethod
    def box(tex, pos, color, w=1.7, font_size=26):
        b = RoundedRectangle(width=w, height=0.62, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                             fill_color="#121722", fill_opacity=1).move_to(pos)
        return VGroup(b, MathTex(tex, font_size=font_size).move_to(pos))

    def assembly(self):
        cfg = load("configs")
        r = {x["name"]: x for x in cfg["rows"]}["Llama 3 8B (2024)"]
        xs = -4.4
        stream = Arrow([xs, -3.3, 0], [xs, 3.3, 0], buff=0, color=RES, stroke_width=6, max_tip_length_to_length_ratio=0.03)
        hin = MathTex(r"h", font_size=30, color=RES).next_to(stream.get_start(), DOWN, buff=0.08)
        plus1 = VGroup(Circle(radius=0.2, color=RES, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1),
                       MathTex(r"+", font_size=28, color=RES)).move_to([xs, -0.5, 0])
        plus2 = plus1.copy().move_to([xs, 1.9, 0])
        n1 = self.box(r"\operatorname{RMSNorm}", [-2.6, -1.5, 0], NORM)
        at = self.box(r"\text{attention}", [-0.6, -1.5, 0], C.TRUE_P)
        n2 = self.box(r"\operatorname{RMSNorm}", [-2.6, 0.9, 0], NORM)
        ml = self.box(r"\text{SwiGLU MLP}", [-0.6, 0.9, 0], GATE, w=2.0)

        def branch(y_from, nb, fb, y_to):
            return VGroup(Line([xs, y_from, 0], [xs + 0.4, y_from, 0], color=GREY_B, stroke_width=2.5),
                          Line([xs + 0.4, y_from, 0], [xs + 0.4, nb.get_y(), 0], color=GREY_B, stroke_width=2.5),
                          Arrow([xs + 0.4, nb.get_y(), 0], nb.get_left(), buff=0, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.3),
                          Arrow(nb.get_right(), fb.get_left(), buff=0, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.3),
                          Line(fb.get_right(), [fb.get_right()[0] + 0.3, fb.get_y(), 0], color=GREY_B, stroke_width=2.5),
                          Line([fb.get_right()[0] + 0.3, fb.get_y(), 0], [fb.get_right()[0] + 0.3, y_to, 0], color=GREY_B,
                               stroke_width=2.5),
                          Arrow([fb.get_right()[0] + 0.3, y_to, 0], [xs + 0.2, y_to, 0], buff=0, color=GREY_B,
                                stroke_width=2.5, max_tip_length_to_length_ratio=0.1))

        b1 = branch(-2.4, n1, at, -0.5)
        b2 = branch(0.0, n2, ml, 1.9)
        p13 = label(r"Part 13", font_size=20, color=C.TRUE_P).next_to(at, DOWN, buff=0.1)
        rep = label(r"$\times\, 32$", font_size=34, color=WHITE).move_to([1.6, 0.0, 0])
        brace = Brace(VGroup(n1, ml, b1, b2), RIGHT, color=GREY_B).next_to(VGroup(at, ml), RIGHT, buff=0.75)
        rep.next_to(brace, RIGHT, buff=0.15)
        M = 1e6
        tally = VGroup(
            label(r"Llama 3 8B, \ one block:", font_size=26, color=WHITE),
            label(rf"attention: \ ${r['attn'] / M:.1f}$ million", font_size=24, color=C.TRUE_P),
            label(rf"SwiGLU MLP: \ ${r['mlp'] / M:.1f}$ million", font_size=24, color=GATE),
            label(rf"two RMSNorm gains: \ ${2 * r['d']:,}$".replace(",", "{,}"), font_size=24, color=NORM),
            label(rf"$\times\, {r['layers']}$ blocks, \ $+$ embeddings: \ ${r['total'] / 1e9:.2f}$ billion", font_size=24,
                  color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.3, 0.4, 0])
        src = note(r"computed from the published configuration").next_to(tally, DOWN, buff=0.25).align_to(tally, LEFT)
        mlp_share = r["mlp"] / (r["attn"] + r["mlp"])
        with self.voiceover(
            "Now assemble the block. <bookmark mark='a'/> The residual stream runs straight up. <bookmark mark='b'/> "
            "A branch takes an RMS-normalized copy, runs attention, the subject of Part 13, and adds the result back. "
            "<bookmark mark='c'/> A second branch takes another normalized copy, runs the gated MLP, and adds that "
            "back. <bookmark mark='d'/> Stack it, here thirty-two times, and that's the body of Llama 3, and, with "
            "small changes, of Qwen, DeepSeek and the rest. <bookmark mark='e'/> Counting from Llama 3 8B's published "
            f"configuration: each block has {r['attn'] / M:.1f} million weights in attention and {r['mlp'] / M:.1f} "
            f"million in the MLP, so {100 * mlp_share:.0f} percent of the block is the gated MLP. Thirty-two blocks and "
            f"the embeddings come to {r['total'] / 1e9:.2f} billion: the eight billion of its name."
        ) as vo:
            self.play(GrowArrow(stream), FadeIn(hin))
            vo.wait_until("a")
            self.play(Indicate(stream, color=RES))
            vo.wait_until("b")
            self.play(Create(b1), FadeIn(n1), FadeIn(at), FadeIn(plus1), FadeIn(p13))
            vo.wait_until("c")
            self.play(Create(b2), FadeIn(n2), FadeIn(ml), FadeIn(plus2))
            vo.wait_until("d")
            self.play(GrowFromCenter(brace), FadeIn(rep))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tally], lag_ratio=0.3), FadeIn(src), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ablation(self):
        b = load("block")
        kinds = list(b["variants"])
        final = {k: float(np.asarray(b[k])[-1, 1]) for k in kinds}
        steps = int(b["steps"])
        finite = [v for v in final.values() if np.isfinite(v)]
        lo = math.floor(min(finite) * 2) / 2
        hi = math.ceil(min(max(finite), 5.0) * 2) / 2
        g = axes([0, steps], [lo, hi], x_length=6.2, y_length=4.4, xlabel=r"training step",
                 ylabel=r"bits per character \ (held-out text)", xticks=[0, steps // 2, steps],
                 yticks=[lo, (lo + hi) / 2, hi], center=[-2.6, -0.5, 0], font_size=18)
        lines = {k: curve(g.ax, np.asarray(b[k])[:, 0], np.clip(np.nan_to_num(np.asarray(b[k])[:, 1], nan=hi), lo, hi),
                          VARIANT[k][1], 3.5) for k in kinds}
        rows = VGroup()
        for k in kinds:
            v = final[k]
            rows.add(VGroup(label(VARIANT[k][0], font_size=22, color=VARIANT[k][1]),
                            label(rf"${v:.3f}$" if np.isfinite(v) else r"diverged", font_size=22, color=WHITE)))
        for i, r_ in enumerate(rows):
            r_[0].move_to([2.3, 2.0 - 0.55 * i, 0], aligned_edge=LEFT)
            r_[1].move_to([6.3, 2.0 - 0.55 * i, 0], aligned_edge=RIGHT)
        head = label(r"final bits per character", font_size=22, color=GREY_A).move_to([4.3, 2.6, 0])
        tag = note(rf"computed: \ ${int(b['depth'])}$ blocks of width ${int(b['d'])}$, \ "
                   rf"${steps:,}$ steps each, \ same data, \ same seed".replace(",", "{,}")).to_corner(DR, buff=0.2)
        best = min((k for k in kinds if np.isfinite(final[k])), key=lambda k: final[k])
        p, r_, s_ = final["plain"], final["residual"], final["pre_rms_swiglu"]
        first = (f"With no residual connections, the {int(b['depth'])}-block stack barely learns: {p:.2f} bits. "
                 if p > r_ + 0.2 else f"Even without residual connections it learns, to {p:.2f} bits. ")
        second = (f"The residual stream alone brings it to {r_:.2f}. " if np.isfinite(r_) else
                  "The residual stream alone, with no normalization, diverges at this learning rate. ")
        best_name = SPOKEN[best]
        third = (f"The full modern block ends best, at {s_:.2f}." if best == "pre_rms_swiglu" else
                 f"The full modern block reaches {s_:.2f}; on this small task the best was {best_name}, at "
                 f"{final[best]:.2f}, and differences of a few hundredths are within the noise of one run.")
        with self.voiceover(
            "Does each piece earn its place? We built the block up one piece at a time, as a character model on the "
            f"thirty novels: {int(b['depth'])} blocks deep, each version trained for {steps:,} steps on the same data, "
            "from the same seed. <bookmark mark='a'/> " + first + "<bookmark mark='b'/> " + second +
            "<bookmark mark='c'/> Then normalization, after the block and before it, LayerNorm and RMSNorm. "
            "<bookmark mark='d'/> " + third
        ) as vo:
            self.play(FadeIn(g), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines["plain"]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["residual"]), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Create(lines[k]) for k in ("post_ln", "pre_ln", "pre_rms")],
                      *[FadeIn(rows[i]) for i in (2, 3, 4)], run_time=2.0)
            vo.wait_until("d")
            self.play(Create(lines["pre_rms_swiglu"]), FadeIn(rows[5]), run_time=1.5)
            self.play(Indicate(rows[kinds.index(best)], color=WHITE))
        self.wait(0.3)
        self.clear_scene()
