from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import HIST, NEURON, NORM, PART, RES, load

POST, PRE = C.SURPRISE, C.INTERVAL


class Norm(VoiceoverScene):
    def construct(self):
        self.card()
        self.batch_vs_layer()
        self.geometry()
        self.jacobian()
        self.pre_post()

    def card(self):
        card = chapter_card(12, r"Normalization", r"Why rescale the numbers inside every layer?", part=PART)
        with self.voiceover("Chapter twelve. Normalization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def batch_vs_layer(self):
        rows_, cols_ = 6, 8
        g = np.random.default_rng(5)  # a drawing of a batch of activations (illustrative)
        vals = g.normal(size=(rows_, cols_))

        def grid(center):
            cells = VGroup()
            for i in range(rows_):
                for j in range(cols_):
                    v = float(np.clip(vals[i, j] / 2.5, -1, 1))
                    col = interpolate_color(ManimColor("#141A24"), ManimColor(NEURON if v > 0 else C.MODEL_Q), abs(v))
                    cells.add(Square(0.42, stroke_width=1, stroke_color=GREY_D, fill_color=col, fill_opacity=1)
                              .move_to(center + np.array([(j - cols_ / 2 + 0.5) * 0.42, (rows_ / 2 - 0.5 - i) * 0.42, 0])))
            return cells

        gb, gl = grid(np.array([-3.5, 0.2, 0])), grid(np.array([3.5, 0.2, 0]))
        col_hl = SurroundingRectangle(VGroup(*[gb[i * cols_ + 2] for i in range(rows_)]), color=C.BITS, buff=0.03,
                                      stroke_width=4)
        row_hl = SurroundingRectangle(VGroup(*[gl[2 * cols_ + j] for j in range(cols_)]), color=NORM, buff=0.03,
                                      stroke_width=4)
        tb = label(r"BatchNorm \ (2015): \\ each feature, \ across the batch", font_size=26, color=C.BITS).next_to(gb, UP, buff=0.3)
        tl = label(r"LayerNorm \ (2016): \\ each example, \ across its features", font_size=26, color=NORM).next_to(gl, UP, buff=0.3)
        axes_l = VGroup(label(r"examples $\downarrow$ \ \ features $\rightarrow$", font_size=20, color=GREY_B).next_to(gb, DOWN, buff=0.2),
                        label(r"examples $\downarrow$ \ \ features $\rightarrow$", font_size=20, color=GREY_B).next_to(gl, DOWN, buff=0.2))
        eq = cmath(r"\hat h", r"=", r"\gamma \odot \frac{h - \mu}{\sigma} + \beta", font_size=34).to_edge(DOWN, buff=0.4)
        eql = label(r"subtract the mean, \ divide by the spread, \ then a learned scale and shift", font_size=22,
                    color=GREY_A).next_to(eq, UP, buff=0.15)
        tag = note(r"illustrative numbers").to_corner(DR, buff=0.2)
        bn_cards = VGroup(
            history_card(2015, r"Sergey Ioffe \& Christian Szegedy, \ Google", r"batch normalization: \ image networks "
                         r"train many times faster; \ the stated reason: \ ``internal covariate shift''", width=5.6,
                         color=C.BITS),
            history_card(2018, r"Shibani Santurkar et al., \ MIT", r"the reason disputed: \ it mostly makes the loss "
                         r"landscape smoother", width=5.6, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, 0.35, 0])
        with self.voiceover(
            "The second fix rescales the numbers inside the network as it trains. In 2015 Sergey Ioffe and Christian "
            "Szegedy introduced batch normalization. <bookmark mark='a'/> Take a batch of examples, and for each "
            "feature, subtract its average over the batch and divide by its spread; then let the network learn its "
            "own scale and shift. It let them train image networks much faster, though the reason they gave, "
            "reducing internal covariate shift, was later disputed: in 2018 a team at MIT argued it mostly makes the "
            "loss landscape smoother. <bookmark mark='b'/> But a batch norm makes each example depend on the others "
            "in its batch, and at test time it needs averages saved from training. In 2016 Jimmy Ba, Jamie Kiros and "
            "Geoffrey Hinton proposed layer normalization: the same arithmetic, across the features of a single "
            "example. Every transformer uses a version of that."
        ) as vo:
            self.play(FadeIn(gb), FadeIn(tb), FadeIn(axes_l[0]), FadeIn(tag), Write(eq), FadeIn(eql))
            self.play(FadeIn(bn_cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Create(col_hl))
            self.play(col_hl.animate.shift(RIGHT * 0.42 * 3), run_time=1.5)
            self.wait(4.0)
            self.play(FadeIn(bn_cards[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeOut(bn_cards))
            self.play(FadeIn(gl), FadeIn(tl), FadeIn(axes_l[1]), Create(row_hl))
            self.play(row_hl.animate.shift(DOWN * 0.42 * 2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        # what LayerNorm does to one vector (illustrative numbers): shift to mean 0, then squash to spread 1
        vec = np.array([4.2, 1.0, 5.0, 0.6, 3.4, 1.8])
        U, y0, x0 = 0.45, -1.0, -5.8

        def vbars(v, col):
            return VGroup(*[Rectangle(width=0.5, height=max(abs(u) * U, 0.01), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([x0 + 0.75 * i, y0 + u * U / 2, 0]) for i, u in enumerate(v)])

        b_raw = vbars(vec, NEURON)
        b_mid = vbars(vec - vec.mean(), NORM)
        b_end = vbars((vec - vec.mean()) / vec.std(), NORM)
        zl = DashedLine([x0 - 0.4, y0, 0], [x0 + 4.2, y0, 0], color=GREY_B, stroke_width=1.5)
        band = VGroup(*[DashedLine([x0 - 0.4, y0 + sgn * U, 0], [x0 + 4.2, y0 + sgn * U, 0], color=NORM, stroke_width=1,
                                   dash_length=0.06) for sgn in (1, -1)])
        s1 = label(r"1. \ shift: \ average $0$", font_size=28, color=NORM).move_to([-4.0, 2.6, 0])
        s2 = label(r"2. \ squash: \ spread $1$", font_size=28, color=NORM).next_to(s1, DOWN, buff=0.15).align_to(s1, LEFT)
        tag = note(r"illustrative").next_to(zl, DOWN, buff=1.6).align_to(zl, LEFT)
        # RMSNorm: vectors of different lengths, all sent to one sphere (a circle here)
        o, R = np.array([3.4, -0.3, 0]), 1.3
        ring = DashedVMobject(Circle(radius=R, color=NORM, stroke_width=2.5), num_dashes=40).move_to(o)
        angs, lens = (0.35, 1.75, 3.5, 5.2), (2.2, 0.7, 1.8, 0.45)
        dirs = [np.array([math.cos(a), math.sin(a), 0]) for a in angs]
        cols = (C.BITS, NEURON, C.MODEL_Q, C.SURPRISE)
        before = VGroup(*[Arrow(o, o + L * d, buff=0, color=c, stroke_width=5, max_tip_length_to_length_ratio=0.25)
                          for L, d, c in zip(lens, dirs, cols)])
        after = VGroup(*[Arrow(o, o + R * d, buff=0, color=c, stroke_width=5, max_tip_length_to_length_ratio=0.25)
                         for d, c in zip(dirs, cols)])
        rms = cmath(r"\operatorname{RMSNorm}(h)", r"=", r"g \odot \frac{h}{\sqrt{\tfrac1d \sum_i h_i^2}}", font_size=32)
        rms.move_to([3.4, 2.6, 0])
        rl = label(r"before gain, \ $\epsilon=0$: \\ nonzero vectors onto one sphere", font_size=22, color=GREY_A).next_to(rms, DOWN, buff=0.15)
        cite_ = cite(r"B.~Zhang \& R.~Sennrich, \textit{Root Mean Square Layer Normalization} (2019)", corner=DR)
        with self.voiceover(
            "Here is what layer normalization does to one vector. <bookmark mark='a'/> Shift its numbers so they "
            "average zero, <bookmark mark='b'/> then squash them so their spread is one. <bookmark mark='c'/> In "
            "2019 Biao Zhang and Rico Sennrich asked whether the shift is needed at all. Their RMSNorm only divides "
            "by the root mean square, the typical size of the numbers. Before the learned gain, and ignoring the small epsilon used in practice, it sends every nonzero vector, long or "
            "short, onto the same sphere, keeping only its direction. <bookmark mark='d'/> It's cheaper, works as "
            "well, and is what Llama, Qwen and DeepSeek use."
        ) as vo:
            self.play(Create(zl), FadeIn(b_raw), FadeIn(tag))
            vo.wait_until("a")
            self.play(Transform(b_raw, b_mid), FadeIn(s1), run_time=1.2)
            vo.wait_until("b")
            self.play(Transform(b_raw, b_end), Create(band), FadeIn(s2), run_time=1.2)
            vo.wait_until("c")
            self.play(Write(rms), FadeIn(rl), FadeIn(ring), *[GrowArrow(a) for a in before], FadeIn(cite_))
            self.play(ReplacementTransform(before, after), run_time=1.6)
            vo.wait_until("d")
            self.play(Indicate(ring, color=NORM))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jacobian(self):
        n = load("norms")
        colors = {r"\hat h": NORM}
        rows = [cmath(r"y", r"=", r"\sqrt{d}\ h \,/\, \|h\|", font_size=34, colors=colors),
                cmath(r"\frac{\partial y}{\partial h}", r"=", r"\frac{\sqrt{d}}{\|h\|}\big(I - ", r"\hat h", r"\hat h^{\top}",
                      r"\big)", font_size=34, colors=colors),
                cmath(r"\frac{\partial y}{\partial h}\, h", r"=", r"0", font_size=34),
                cmath(r"\frac{\partial\, \mathrm{LN}}{\partial h}", r"=", r"\frac{1}{\sigma}\big(I - \tfrac1d \mathbf{1}"
                      r"\mathbf{1}^{\top} - \hat u \hat u^{\top}\big)", font_size=34)]
        whys = [why(r"RMSNorm: \ gain $1$, \ $\epsilon=0$, \ $h\ne0$"), why(r"quotient rule; \ $\hat h = h / \|h\|$"),
                why(r"stretching $h$ changes nothing"), why(r"LayerNorm: \ blind to shifts too")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-3.6, buff=0.5, edge=6.9)
        d = int(n["d"])
        sv_ln, sv_rms = np.asarray(n["sv_ln"]), np.asarray(n["sv_rms"])
        top = max(sv_ln.max(), sv_rms.max())

        def bars(sv, col, x0):
            return VGroup(*[Rectangle(width=0.13, height=max(1.1 * v / top, 0.02), stroke_width=0, fill_color=col,
                                      fill_opacity=0.9).move_to([x0 + 0.17 * i, -3.25 + max(1.1 * v / top, 0.02) / 2, 0])
                            for i, v in enumerate(sv)])

        b_rms, b_ln = bars(sv_rms, NORM, 0.6), bars(sv_ln, C.BITS, 3.9)
        base = VGroup(Line([0.45, -3.25, 0], [0.6 + 0.17 * d, -3.25, 0], color=GREY_C, stroke_width=1.5),
                      Line([3.75, -3.25, 0], [3.9 + 0.17 * d, -3.25, 0], color=GREY_C, stroke_width=1.5))
        z_rms = int((sv_rms < 1e-6).sum())
        z_ln = int((sv_ln < 1e-6).sum())
        bl = VGroup(label(rf"RMSNorm: \ ${d - z_rms}$ equal, \ ${z_rms}$ zero", font_size=20, color=NORM).next_to(b_rms, UP, buff=0.12),
                    label(rf"LayerNorm: \ ${d - z_ln}$ equal, \ ${z_ln}$ zero", font_size=20, color=C.BITS).next_to(b_ln, UP, buff=0.12))
        bt = label(rf"the Jacobian's singular values, \ $d = {d}$, \ computed by autograd", font_size=20, color=GREY_A)
        bt.move_to([3.6, -3.65, 0])
        sc = np.asarray(n["scale"])  # scale, change of output, norm of Jacobian
        scale_l = label(rf"double $h$: \ the output is unchanged, \\ the Jacobian halves \ (${sc[1, 2]:.2f} \to {sc[2, 2]:.2f}$)",
                        font_size=24, color=GREY_A).move_to([-3.6, -2.5, 0])
        with self.voiceover(
            "What does normalization do to the gradient? Take RMSNorm without its gain, set epsilon to zero, and assume nonzero inputs. <bookmark mark='a'/> Its "
            "derivative, by the quotient rule, is a constant times the identity minus the projection onto h's own "
            "direction. <bookmark mark='b'/> So stretching h changes nothing, and the gradient never points along h: "
            "the idealized layer only cares about direction. Real implementations add epsilon, so that radial invariance is approximate. For nonconstant inputs, LayerNorm's derivative also removes the all-ones direction, since "
            f"shifting every number at once changes nothing either. <bookmark mark='c'/> Measured with autograd at "
            f"d equals {d}: RMSNorm's Jacobian has {d - z_rms} equal singular values and {z_rms} zero; LayerNorm's, "
            f"{d - z_ln} and {z_ln}, exactly as derived. <bookmark mark='d'/> And the constant in front is one over "
            "the vector's size: double h, and the gradient halves. Weights that grow large get proportionally small "
            "updates. The normalization stabilizes itself, and it interacts with weight decay in ways Part 11 takes up."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            step(3)
            vo.wait_until("c")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_rms], lag_ratio=0.03),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_ln], lag_ratio=0.03), FadeIn(bl), FadeIn(bt),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(scale_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pre_post(self):
        b = load("block")
        depth = int(b["depth"])
        post_eq = cmath(r"h_{l+1}", r"=", r"\operatorname{Norm}\big(h_l + F(h_l)\big)", font_size=32, color=POST)
        pre_eq = cmath(r"h_{l+1}", r"=", r"h_l + F\big(\operatorname{Norm}(h_l)\big)", font_size=32, color=PRE)
        post_l = label(r"post-norm: \ the 2017 Transformer, \ BERT", font_size=22, color=POST)
        pre_l = label(r"pre-norm: \ GPT-2 (2019) \ and almost everything since", font_size=22, color=PRE)
        eqs = VGroup(VGroup(post_eq, post_l).arrange(DOWN, buff=0.12), VGroup(pre_eq, pre_l).arrange(DOWN, buff=0.12))
        eqs.arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.35)
        gp, gq = np.asarray(b["gnorm0_post_ln"]), np.asarray(b["gnorm0_pre_ln"])
        lo = math.floor(np.log10(min(gp.min(), gq.min())) - 0.2)
        hi = math.ceil(np.log10(max(gp.max(), gq.max())) + 0.2)
        g1 = axes([1, depth], [lo, hi], x_length=5.2, y_length=3.0, xlabel=r"block", ylabel=r"gradient at the start \ (log)",
                  xticks=[1, depth], yticks=list(range(lo, hi + 1)), yfmt=lambda v: rf"10^{{{int(v)}}}",
                  center=[-3.4, -1.3, 0], font_size=18)
        ks = np.arange(1, depth + 1)
        c_post = curve(g1.ax, ks, np.log10(gp), POST, 3.5)
        c_pre = curve(g1.ax, ks, np.log10(gq), PRE, 3.5)
        P, Q = np.asarray(b["post_ln"]), np.asarray(b["pre_ln"])
        ymax = float(np.nanmax(np.r_[P[:, 1], Q[:, 1]]))
        ytop = math.ceil(min(ymax, 8.0))
        g2 = axes([0, int(b["steps"])], [1.5, ytop], x_length=5.2, y_length=3.0, xlabel=r"step",
                  ylabel=r"bits per character \ (held-out text)", xticks=[0, int(b["steps"])], yticks=[2, ytop],
                  center=[3.4, -1.3, 0], font_size=18)
        t_post = curve(g2.ax, P[:, 0], np.clip(P[:, 1], 1.5, ytop), POST, 3.5)
        t_pre = curve(g2.ax, Q[:, 0], np.clip(Q[:, 1], 1.5, ytop), PRE, 3.5)
        tag = note(rf"computed: \ ${depth}$ blocks, \ a character model on the novels, \ no warmup").to_corner(DR, buff=0.15)

        def box(tex, pos, col):
            b_ = RoundedRectangle(width=1.4, height=0.52, corner_radius=0.1, stroke_color=col, stroke_width=2.5,
                                  fill_color="#121722", fill_opacity=1).move_to(pos)
            return VGroup(b_, MathTex(tex, font_size=26).move_to(pos))

        def diagram(x, pre):
            sx, bx = x - 1.0, x + 0.8
            stream = Arrow([sx, -2.8, 0], [sx, 1.4, 0], buff=0, color=RES, stroke_width=5,
                           max_tip_length_to_length_ratio=0.04)
            plus = VGroup(Circle(radius=0.2, color=RES, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1),
                          MathTex(r"+", font_size=28, color=RES)).move_to([sx, -0.2, 0])
            f_ = box(r"F", [bx, -0.75, 0], NEURON)
            g_ = VGroup(stream, plus)
            g_.add(Line([sx, -2.2, 0], [bx, -2.2, 0], color=GREY_B, stroke_width=2.5))
            if pre:
                nb = box(r"\operatorname{Norm}", [bx, -1.6, 0], PRE)
                g_.add(Line([bx, -2.2, 0], nb.get_bottom(), color=GREY_B, stroke_width=2.5),
                       Arrow(nb.get_top(), f_.get_bottom(), buff=0, color=GREY_B, stroke_width=2.5,
                             max_tip_length_to_length_ratio=0.3), nb)
            else:
                g_.add(Arrow([bx, -2.2, 0], f_.get_bottom(), buff=0, color=GREY_B, stroke_width=2.5,
                             max_tip_length_to_length_ratio=0.15))
                nb = box(r"\operatorname{Norm}", [sx, 0.6, 0], POST)
                g_.add(nb, label(r"the stream itself \\ is normalized", font_size=22, color=POST).next_to(nb, RIGHT, buff=0.2))
            g_.add(Line(f_.get_top(), [bx, -0.2, 0], color=GREY_B, stroke_width=2.5),
                   Arrow([bx, -0.2, 0], plus.get_right(), buff=0, color=GREY_B, stroke_width=2.5,
                         max_tip_length_to_length_ratio=0.15), f_)
            return g_

        d_post, d_pre = diagram(-3.0, False), diagram(3.6, True)
        clean = label(r"the stream: \\ a clean running sum", font_size=22, color=RES).next_to(d_pre[0], LEFT, buff=0.2)
        d_pre.add(clean)
        rp, rq = float(gp[-1] / gp[0]), float(gq[-1] / gq[0])
        fp, fq = float(P[-1, 1]), float(Q[-1, 1])
        if not np.isfinite(fp) or fp > fq + 0.05:
            verdict = (f"Trained at the same learning rate with no warm-up, the pre-norm stack ends at {fq:.2f} bits per "
                       f"character and the post-norm stack at {fp:.2f}: post-norm needs a gentler start.")
        elif fq > fp + 0.05:
            verdict = (f"Trained at the same learning rate, the post-norm stack actually ends lower here, at {fp:.2f} "
                       f"bits per character against {fq:.2f}: at this depth and scale, it trains fine.")
        else:
            verdict = (f"Trained at the same learning rate, both end close together, {fp:.2f} and {fq:.2f} bits per "
                       "character: at this small scale the difference is in the gradients, not yet the result.")
        with self.voiceover(
            "Where does the normalization go? <bookmark mark='a'/> The 2017 Transformer normalized after adding each "
            "block's output to the stream: post-norm. <bookmark mark='b'/> GPT-2, in 2019, moved it to the branch, "
            "before each block, leaving the stream itself as a clean running sum: pre-norm. In 2020 Ruibin Xiong and "
            "colleagues showed why it matters: with post-norm, the gradients at the start of training are uneven "
            "across the layers, so it needs a learning-rate warm-up. <bookmark mark='c'/> In our own "
            f"{depth}-block model, the last block's starting gradient is {rp:.1f} times the first block's with post-norm, "
            f"and {rq:.1f} times with pre-norm. <bookmark mark='d'/> " + verdict + " <bookmark mark='e'/> The story "
            "isn't over: OLMo 2, at the end of 2024, normalizes each block's output instead, and a 2025 paper from Kaiming He, "
            "Yann LeCun and colleagues replaces normalization with a scaled tanh."
        ) as vo:
            self.play(FadeIn(eqs, shift=DOWN * 0.15))
            vo.wait_until("a")
            self.play(Indicate(eqs[0], color=POST, scale_factor=1.05), FadeIn(d_post))
            vo.wait_until("b")
            self.play(Indicate(eqs[1], color=PRE, scale_factor=1.05), FadeIn(d_pre))
            vo.wait_until("c")
            self.play(FadeOut(d_post), FadeOut(d_pre))
            self.play(FadeIn(g1), Create(c_post), Create(c_pre), FadeIn(tag), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(g2), Create(t_post), Create(t_pre), run_time=2.0)
            vo.wait_until("e")
            fr = label(r"OLMo 2 \ (2024): \ $h + \operatorname{Norm}(F(h))$; \ Zhu, Chen, He, LeCun \& Liu \ (2025): \ "
                       r"$\tanh(\alpha x)$ \ in place of Norm", font_size=22, color=GREY_A).next_to(eqs, DOWN, buff=0.25)
            self.play(FadeIn(fr))
        self.wait(0.3)
        self.clear_scene()
