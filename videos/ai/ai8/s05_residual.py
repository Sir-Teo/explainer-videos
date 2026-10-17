from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import CLS_A, CLS_B, NEURON, curve, load, region_image

PLAIN, RES, NORM = C.SURPRISE, C.BITS, C.INTERVAL


class Residual(VoiceoverScene):
    def construct(self):
        self.card()
        self.block()
        self.curves()
        self.inside()
        self.modern()

    def card(self):
        card = chapter_card(4, r"The residual stream", r"How do you train forty layers?", part=8, lit=(2015,))
        with self.voiceover("Chapter four. Residual connections."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self):
        # a plain stack against a residual stack, drawn as boxes
        def stack(x, residual):
            g = VGroup()
            ys = [2.2 - 1.05 * k for k in range(4)]
            spine = Line([x, 2.8, 0], [x, -2.0, 0], color=RES if residual else GREY_D, stroke_width=6 if residual else 0)
            g.add(spine)
            for yv in ys:
                box = RoundedRectangle(width=1.6, height=0.6, corner_radius=0.12, stroke_color=NEURON, stroke_width=2.5,
                                       fill_color="#121722", fill_opacity=1).move_to([x + (1.3 if residual else 0), yv - 0.5, 0])
                g.add(box, MathTex(r"f_\ell", font_size=28).move_to(box))
                if residual:
                    g.add(Arrow([x, yv, 0], box.get_top() + LEFT * 0.3, buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          Arrow(box.get_bottom() + LEFT * 0.3, [x, yv - 1.0, 0], buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          MathTex(r"+", font_size=30, color=RES).move_to([x - 0.25, yv - 1.0, 0]))
                else:
                    g.add(Arrow([x, yv + 0.2, 0], box.get_top(), buff=0.03, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2))
            return g

        plain = stack(-4.2, False)
        res = stack(0.6, True)
        pt = label(r"plain: \ $h_{\ell+1} = f_\ell(h_\ell)$", font_size=28, color=PLAIN).next_to(plain, DOWN, buff=0.3)
        rt = label(r"residual: \ $h_{\ell+1} = h_\ell + f_\ell(h_\ell)$", font_size=28, color=RES).next_to(res, DOWN, buff=0.3)
        colors = {r"I": RES}
        jac = cmath(r"\frac{\partial h_{\ell+1}}{\partial h_\ell}", "=", r"I", "+", r"\frac{\partial f_\ell}{\partial h_\ell}",
                    colors=colors, font_size=38).move_to([4.8, 1.2, 0])
        jl = label(r"the identity always gets through: \\ gradients reach the first layers", font_size=24, color=GREY_A)
        jl.next_to(jac, DOWN, buff=0.3)
        cite_ = cite(r"K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Deep Residual Learning for Image Recognition} (2015)",
                     corner=DR)
        with self.voiceover(
            "Good initialization gets a signal through at the start, but training can still go wrong in a deep "
            "stack. In 2015, Kaiming He and colleagues found a fix so simple it's now everywhere. "
            "<bookmark mark='a'/> Instead of each layer replacing what came before, let it add to it. The layers "
            "become small corrections to a stream of numbers flowing straight through: the residual stream. "
            "<bookmark mark='b'/> By the chain rule, the derivative of each block is the identity plus a little "
            "extra, so gradients always have a clear path back to the first layer. Every transformer in this "
            "series is built this way."
        ) as vo:
            self.play(FadeIn(plain), FadeIn(pt), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(res), FadeIn(rt))
            vo.wait_until("b")
            self.play(Write(jac), FadeIn(jl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        r = load("residual")
        P, R, N = (np.asarray(r[k]) for k in ("plain", "residual", "residual_norm"))
        ax = Axes(x_range=[0, P[-1, 0], 500], y_range=[0.4, 1.0, 0.1], x_length=8.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.5, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 0.75, 1.0)])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"spiral points on the right side", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cp, cr, cn = (curve(ax, D[:, 0], D[:, 2], col, 4) for D, col in ((P, PLAIN), (R, RES), (N, NORM)))
        names = VGroup(label(rf"$40$ plain layers: \ ${100 * P[-1, 2]:.0f}\%$, \ a coin flip", font_size=26, color=PLAIN),
                       label(rf"$40$ residual layers: \ ${100 * R[-1, 2]:.0f}\%$", font_size=26, color=RES),
                       label(r"with LayerNorm too", font_size=26, color=NORM))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 0.8, 0])
        colors = {r"\mu": NORM, r"\sigma": NORM}
        ln = cmath(r"\mathrm{LN}(h) = \gamma \odot \frac{h - \mu}{\sigma} + \beta", colors=colors, font_size=32)
        ln.next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        lnl = label(r"rescale each vector to a standard size", font_size=22, color=GREY_A).next_to(ln, DOWN, buff=0.12)
        lnl.align_to(names, LEFT)
        with self.voiceover(
            "Here it is on the spirals, with forty layers. The plain stack never learns anything: it's stuck at a "
            "coin flip. <bookmark mark='a'/> The same forty layers with residual connections learn the spirals "
            "completely, within a few hundred steps. <bookmark mark='b'/> Add layer normalization, which rescales "
            "each layer's vector to a standard size, and training is steadier still. Residual streams and "
            "normalization: the two pieces of plumbing inside every modern model."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn))
            self.play(Create(cp), FadeIn(names[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(cr), FadeIn(names[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cn), FadeIn(names[2]), Write(ln), FadeIn(lnl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        """Why: the two forty-layer stacks as they train, their answers everywhere and the gradient reaching each layer."""
        r = load("residual")
        sp = load("spiral")
        X, y = np.asarray(sp["X"]), np.asarray(sp["y"])
        steps = [int(s_) for s_ in r["snap_steps"]]
        xs = np.asarray(r["xs"])
        nets = ("plain", "residual")
        cols = {"plain": PLAIN, "residual": RES}
        probs = {n: np.asarray(r[f"probs_{n}"]) for n in nets}
        gn = {n: np.log10(np.maximum(np.asarray(r[f"gnorm_{n}"]), 1e-30)) for n in nets}
        lo = float(min(g.min() for g in gn.values())) - 0.3
        hi = float(max(g.max() for g in gn.values())) + 0.1
        S, span = 3.4, 6.8
        cx = {"plain": -3.4, "residual": 3.4}
        cy = 1.05
        frames_ = Group()
        dots = VGroup()
        for n in nets:
            c = np.array([cx[n], cy, 0])
            frames_.add(Square(S, stroke_color=GREY_D, stroke_width=1.5).move_to(c))
            dots.add(*[Dot(c + np.array([p[0] * S / span, p[1] * S / span, 0]), radius=0.018,
                           color=CLS_A if v == 0 else CLS_B, fill_opacity=0.8) for p, v in zip(X, y)])

        def maps(k):
            return Group(*[region_image(probs[n][k], np.zeros_like(probs[n][k]), xs, S, S, boundary=False)
                           .move_to([cx[n], cy, 0]) for n in nets])

        BW, BH, by = 5.6, 1.5, -2.95  # the gradient bars: width of the forty, height of the range, baseline

        def bars(k):
            g = VGroup()
            for n in nets:
                for i, v in enumerate(gn[n][k]):
                    h = max(BH * (v - lo) / (hi - lo), 0.01)
                    x = cx[n] - BW / 2 + (i + 0.5) * BW / len(gn[n][k])
                    g.add(Rectangle(width=BW / len(gn[n][k]) * 0.7, height=h, stroke_width=0, fill_color=cols[n],
                                    fill_opacity=0.85).move_to([x, by + h / 2, 0]))
            return g

        base = VGroup(*[Line([cx[n] - BW / 2 - 0.1, by, 0], [cx[n] + BW / 2 + 0.1, by, 0], color=GREY_C, stroke_width=1.5)
                        for n in nets])
        heads = VGroup(*[label(rf"$40$ {'plain' if n == 'plain' else 'residual'} layers", font_size=24, color=cols[n])
                         .next_to(frames_[j], UP, buff=0.12) for j, n in enumerate(nets)])
        bl = VGroup(*[label(r"layer $1$ \ $\longrightarrow$ \ layer $40$", font_size=18, color=GREY_B)
                      .next_to(b_, DOWN, buff=0.1) for b_ in base])
        gl = label(r"how much gradient reaches each layer \ (log scale)", font_size=20, color=GREY_A).move_to([0, by + BH + 0.25, 0])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=30,
                                            color=WHITE).move_to([0, cy + 0.6, 0]))
        cur_m, cur_b = maps(0), bars(0)
        e = int(np.floor(gn["plain"][0, -1] - gn["plain"][0, 0]))  # the last layer's gradient over the first's, in powers of 10
        big = {9: "a billion", 10: "ten billion", 11: "a hundred billion", 12: "a trillion", 13: "ten trillion",
               14: "a hundred trillion", 15: "a quadrillion"}.get(e, f"ten to the {e}")
        rr = 10 ** float(gn["residual"][0].max() - gn["residual"][0].min())
        fade = float(gn["residual"][0].mean() - gn["residual"][-1].mean())
        with self.voiceover(
            "Why does the plain stack never learn? Look inside both of them as they train: on top, what each one says "
            "about every point of the plane; below, how much gradient reaches each of its forty layers, on a log "
            f"scale. <bookmark mark='a'/> At the start, the plain stack's gradients shrink layer by layer on the "
            f"way down: the first layer gets more than {big} times less than the last. The residual stack's "
            f"gradients are all about the same size, within a factor of {rr:.0f}, because each block adds to a "
            "stream the gradient flows straight back along. <bookmark mark='b'/> So as training runs, the residual "
            "stack's answer bends to follow the spirals, and its gradients shrink together, by a factor of "
            f"{'ten' if round(fade) == 1 else ['a hundred', 'a thousand', 'ten thousand', 'a hundred thousand', 'a million'][min(round(fade), 6) - 2]}"
            ", as there is less and less left to fix. The plain stack's answer stays one flat colour, the same "
            "everywhere, and its gradients only fade further."
        ) as vo:
            self.play(FadeIn(frames_), FadeIn(cur_m), FadeIn(dots), FadeIn(heads))
            self.add(cnt)
            self.play(Create(base), FadeIn(bl), FadeIn(gl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cur_b], lag_ratio=0.01),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(VGroup(*cur_b[:len(cur_b) // 2]), color=PLAIN, scale_factor=1.05), run_time=1.5)
            vo.wait_until("b")
            for k in range(1, len(steps)):
                nm, nb = maps(k), bars(k)
                self.play(FadeOut(cur_m), FadeIn(nm), Transform(cur_b, nb), t.animate.set_value(steps[k]), run_time=1.6)
                cur_m = nm
                self.bring_to_front(dots)
        self.wait(0.4)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modern(self):
        """Today's block: pre-norm, RMSNorm, and a gated MLP (SwiGLU), with the parameter count that keeps it fair."""
        import math

        colors = {r"\operatorname{RMS}": NORM, r"g": NORM, r"\odot": C.BITS}
        pre = MathTex(r"h_{l+1} = h_l + F\big(\operatorname{Norm}(h_l)\big)", font_size=32).move_to([-3.4, 2.5, 0])
        prel = label(r"pre-norm: \ the stream itself is never rescaled", font_size=20, color=GREY_A).next_to(pre, DOWN, buff=0.1)
        rms = cmath(r"\operatorname{RMSNorm}(h) = ", r"g", r"\odot \frac{h}{", r"\operatorname{RMS}", r"(h)}, \quad",
                    r"\operatorname{RMS}", r"(h) = \sqrt{\tfrac{1}{d}\textstyle\sum_i h_i^2}", colors=colors, font_size=30)
        rms.move_to([-3.4, 1.1, 0])
        keep_in_frame(rms, margin=0.4)
        rmsl = label(r"LayerNorm without the mean or the shift: \ cheaper, \ just as good", font_size=20, color=GREY_A).next_to(rms, DOWN, buff=0.1)
        keep_in_frame(rmsl, margin=0.4)
        glu = cmath(r"\operatorname{FFN}(x) = W_2\big(\operatorname{SiLU}(W_1 x)", r"\odot", r"W_3 x\big)", colors=colors, font_size=30)
        glu.move_to([-3.4, -0.4, 0])
        glul = label(r"SwiGLU: \ one branch gates the other, \ number by number", font_size=20, color=GREY_A).next_to(glu, DOWN, buff=0.1)
        cnt = MathTex(r"3 \cdot d \cdot \tfrac{8}{3}d = 8d^2 = 2 \cdot d \cdot 4d", font_size=30, color=C.BITS).move_to([-3.4, -1.9, 0])
        cntl = label(r"a width of $\tfrac83 d$ instead of $4d$: \ the same number of weights", font_size=20, color=C.BITS).next_to(cnt, DOWN, buff=0.1)
        # right: the activations, computed
        ax = CornerAxes(x_range=[-4, 4, 2], y_range=[-1, 4, 1], x_length=4.6, y_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, 0.6, 0])
        zero = DashedLine(ax.c2p(-4, 0), ax.c2p(4, 0), dash_length=0.05, stroke_width=1, color=GREY_D)
        relu = ax.plot(lambda x: max(x, 0.0), x_range=[-4, 4, 0.02], color=GREY_B, stroke_width=3)
        silu = ax.plot(lambda x: x / (1 + math.exp(-x)), x_range=[-4, 4, 0.02], color=C.BITS, stroke_width=3.5)
        kl = VGroup(label(r"ReLU", font_size=20, color=GREY_B), label(r"SiLU: \ $x\,\sigma(x)$", font_size=20, color=C.BITS))
        kl.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax.c2p(-4, 4), DR, buff=0.1)
        used = label(r"Llama, \ Qwen, \ DeepSeek, \ Mistral, \ gpt-oss: \\ pre-norm, \ RMSNorm, \ a gated MLP \ (as published)",
                     font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        cite_ = cite(r"B.~Zhang \& R.~Sennrich, \textit{RMSNorm} (2019); \ N.~Shazeer, \textit{GLU Variants Improve Transformer} (2020)",
                     corner=DR)
        with self.voiceover(
            "Three small refinements turn this into the block inside today's language models. <bookmark mark='a'/> "
            "First, normalize what goes into each layer, not the stream itself: the stream stays a clean running sum. "
            "<bookmark mark='b'/> Second, RMSNorm: divide by the root mean square and drop the mean and the shift. "
            "It's cheaper, and it works just as well. <bookmark mark='c'/> Third, a gated MLP. Two projections of "
            "the input, one passed through SiLU, a smooth cousin of the ReLU, multiplied number by number with the "
            "other. <bookmark mark='d'/> That's three matrices instead of two, so the hidden width shrinks from four "
            "times the model width to eight thirds, and the count of weights comes out the same. Noam Shazeer's "
            "paper tested it, and ended, famously, by attributing its success to divine benevolence. "
            "<bookmark mark='e'/> Llama, Qwen, DeepSeek and gpt-oss all use this block."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(pre), FadeIn(prel))
            vo.wait_until("b")
            self.play(Write(rms), FadeIn(rmsl))
            vo.wait_until("c")
            self.play(Write(glu), FadeIn(glul), Create(ax), Create(zero), Create(relu), FadeIn(kl[0]))
            self.play(Create(silu), FadeIn(kl[1]))
            vo.wait_until("d")
            self.play(Write(cnt), FadeIn(cntl))
            vo.wait_until("e")
            self.play(FadeIn(used))
        self.wait(0.3)
        self.clear_scene()
