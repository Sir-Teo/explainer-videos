from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (F, LEARNC, PART, ROTC, RTNC, SMOOTHC, WEIGHTC, hbars, load, node_box)

COLORS = {r"Q": ROTC, r"x": C.TOKEN, r"W": WEIGHTC, r"E": WEIGHTC}


class Rotation(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariance()
        self.spread()
        self.results()
        self.learned()

    def card(self):
        card = chapter_card(11, r"Rotations: \ QuaRot and SpinQuant", r"Can turning the space make the outliers "
                            r"disappear?", part=PART)
        with self.voiceover("Chapter eleven. Rotations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def invariance(self):
        r = load("rotation")
        rows = [
            cmath(r"\mathrm{RMSNorm}(x)", r"=", r"\frac{x}{\|x\| / \sqrt d}\,\gamma", colors=COLORS, font_size=36),
            cmath(r"\mathrm{RMSNorm}(x Q)", r"=", r"\mathrm{RMSNorm}(x)\, Q", colors=COLORS, font_size=36),
            cmath(r"W_{\text{in}} \to W_{\text{in}} Q,", r"\quad", r"W_{\text{out}} \to Q^\top W_{\text{out}}",
                  colors=COLORS, font_size=36),
            cmath(r"E \to E\,Q,", r"\quad", r"W_{\text{head}} \to W_{\text{head}}\, Q", colors=COLORS, font_size=36),
        ]
        whys = [why(r"fold the gain $\gamma$ into the next weights first"), why(r"$\|xQ\| = \|x\|$ for a rotation $Q$"),
                why(r"layers that read the stream, \ and write to it"), why(r"the embedding and the head")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.42, edge=6.8)
        inv = float(r["invariance"])
        mant, ex = f"{inv:.1e}".split("e")
        res = label(rf"our model, \ rotated: \ the logits change by at most ${mant} \times 10^{{{int(ex)}}}$",
                    font_size=22, color=ROTC).to_edge(DOWN, buff=0.5)
        hc = history_card(2024, r"Saleh Ashkboos et al., \ QuaRot", rf"rotate the model, \ then $4$-bit weights, "
                          rf"activations and cache: \ {F.QUAROT['model']} within ${F.QUAROT['ppl']}$ perplexity",
                          width=4.4, font_size=16, color=ROTC).move_to([4.5, -0.45, 0])
        # a rotation keeps lengths (schematic)
        c0 = np.array([-5.0, -0.5, 0])
        circ = Circle(radius=0.8, stroke_color=GREY_D, stroke_width=1.5).move_to(c0)
        v0 = np.array([0.75, 0.28, 0])
        th = 0.9
        v1 = np.array([v0[0] * np.cos(th) - v0[1] * np.sin(th), v0[0] * np.sin(th) + v0[1] * np.cos(th), 0])
        ax_ = Arrow(c0, c0 + v0, buff=0, color=C.TOKEN, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        aq = Arrow(c0, c0 + v1, buff=0, color=ROTC, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        arc = Arc(radius=0.45, start_angle=np.arctan2(v0[1], v0[0]), angle=th, arc_center=c0, color=ROTC,
                  stroke_width=2)
        lx = MathTex(r"x", font_size=26, color=C.TOKEN).next_to(c0 + v0, RIGHT, buff=0.08)
        lq = MathTex(r"xQ", font_size=26, color=ROTC).next_to(c0 + v1, UP, buff=0.08)
        rot_pic = VGroup(circ, ax_, aq, arc, lx, lq)
        rot_l = label(r"a rotation: \ same length", font_size=18, color=GREY_A).next_to(circ, DOWN, buff=0.15)
        # the residual stream, rotated: who gets Q and who gets its transpose (schematic)
        sy = -2.3
        stream = Line([-6.2, sy, 0], [6.2, sy, 0], color=ROTC, stroke_width=3).set_stroke(opacity=0.5)
        boxes = VGroup()
        for xx, t_ in ((-5.2, r"$E\,Q$"), (-1.8, r"read: \ $W_{\text{in}}\,Q$"), (1.6, r"write: \ $Q^\top W_{\text{out}}$"),
                       (5.0, r"head: \ $W_{\text{head}}\,Q$")):
            boxes.add(node_box(t_, ROTC, font_size=18, pad=0.15).move_to([xx, sy, 0]))
        sl_ = label(r"the residual stream, \ rotated by $Q$ \ (schematic)", font_size=17, color=ROTC).next_to(
            stream, UP, buff=0.6).set_x(0)
        with self.voiceover(
            "In 2024 Saleh Ashkboos, Dan Alistarh and colleagues found a way to make outliers go away instead of "
            "working around them. <bookmark mark='a'/> Start from the normalization before each layer, RMSNorm: "
            "divide a vector by its length, then multiply by a learned gain, gamma, which can be folded into the "
            "next weights. <bookmark mark='b'/> What's left divides by the length, and a rotation doesn't change "
            "lengths, so normalizing a rotated vector gives the rotated normalized vector. "
            "<bookmark mark='c'/> So rotate the whole residual stream by Q: every layer that reads it gets W times "
            "Q, every layer that writes to it Q transposed times W, <bookmark mark='d'/> and the embedding and the "
            "output head get Q too. The network computes exactly the same function. We checked on ours: the "
            f"largest change in any logit is {mant} times ten to the {int(ex)}, rounding error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            self.play(Create(circ), GrowArrow(ax_), FadeIn(lx), FadeIn(rot_l))
            self.play(TransformFromCopy(ax_, aq), Create(arc), FadeIn(lq))
            vo.wait_until("c")
            step(2)
            self.play(Create(stream), FadeIn(sl_), FadeIn(boxes[1:3]), FadeIn(hc))
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(boxes[0]), FadeIn(boxes[3]))
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spread(self):
        r = load("rotation")
        a0, a1 = np.asarray(r["act_row"]), np.asarray(r["act_row_rot"])
        n = len(a0)
        top = float(max(np.abs(a0).max(), np.abs(a1).max()))

        def strip(v, col, y):
            return VGroup(*[Rectangle(width=11.0 / n * 0.9, height=max(abs(1.1 * x / top), 0.004), stroke_width=0,
                                      fill_color=col, fill_opacity=0.85)
                            .move_to([-5.5 + 11.0 * (i + 0.5) / n, y + 0.55 * x / top, 0]) for i, x in enumerate(v)])

        s0, s1 = strip(a0, C.TOKEN, 1.0), strip(a1, ROTC, -1.6)
        l0 = label(rf"one token's input to a layer, \ ${n}$ channels: \ peak $\div$ typical $= {r['crest']:.1f}$ "
                   r"(average over tokens)", font_size=20, color=C.TOKEN).move_to([0, 2.5, 0])
        l1 = label(rf"the same vector, \ rotated by a Hadamard matrix: \ ${r['crest_rot']:.1f}$", font_size=20,
                   color=ROTC).move_to([0, -0.15, 0])
        hm = MathTex(r"H_2 = \tfrac{1}{\sqrt2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix},\quad "
                     r"H_{2n} = \tfrac{1}{\sqrt2}\begin{pmatrix} H_n & H_n \\ H_n & -H_n \end{pmatrix}", font_size=28,
                     color=ROTC).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Which rotation? <bookmark mark='a'/> Here is one token's input to a layer of our model, channel by "
            f"channel. Its largest entry is {r['crest']:.1f} times its typical size, on average over tokens. "
            "<bookmark mark='b'/> Rotate it with a Hadamard matrix: entries of plus and minus one over root n, "
            "built by doubling, and applied in n log n steps, like a fast Fourier transform. Each output mixes all "
            "inputs equally, so a spike in one channel is spread across all of them. "
            f"<bookmark mark='c'/> Now the peak is {r['crest_rot']:.1f} times the typical size: one scale per token "
            "fits all its channels, and four-bit levels are no longer wasted."
        ) as vo:
            self.play(FadeIn(l0), LaggedStart(*[GrowFromCenter(b_) for b_ in s0], lag_ratio=0.004), run_time=1.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(hm))
            self.play(TransformFromCopy(s0, s1), FadeIn(l1), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(l1, color=ROTC))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        r = load("rotation")
        base = float(r["fp32"])
        L = r["loss"]
        rnd = [L[f"w4a4_random{s}"] - base for s in (11, 12, 13)]
        names = [r"plain rounding", r"SmoothQuant", r"Hadamard \ (QuaRot)", r"random rotations, \ $3$ seeds",
                 r"learned \ (SpinQuant, small)"]
        vals = [L["w4a4_plain"] - base, L["w4a4_smooth"] - base, L["w4a4_hadamard"] - base, float(np.mean(rnd)),
                L["w4a4_learned"] - base]
        cols = [RTNC, SMOOTHC, ROTC, GREY_A, LEARNC]
        b = hbars(vals, names, cols, width=4.4, row_h=0.55, font_size=21, lo=0, hi=max(vals) * 1.1,
                  fmt_v=lambda v: rf"{v:+.3f}")
        b.move_to([0.6, 0.2, 0])
        x_of = lambda v: b[0].bar.get_left()[0] + v / (max(vals) * 1.1) * 4.4  # noqa: E731
        spread = Line([x_of(min(rnd)), b[3].bar.get_y(), 0], [x_of(max(rnd)), b[3].bar.get_y(), 0], color=WHITE,
                      stroke_width=3)
        head = label(r"$4$-bit weights \emph{and} $4$-bit activations: \ extra loss on held-out novels \ (nats per "
                     r"token)", font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        ctx = VGroup(label(rf"weights only, \ $4$ bits: \ ${L['w4a16_plain'] - base:+.3f}$ \ plain, \ "
                           rf"${L['w4a16_hadamard'] - base:+.3f}$ \ rotated", font_size=19, color=GREY_A),
                     label(rf"$4$-bit weights, \ $8$-bit activations: \ ${L['w4a8_plain'] - base:+.3f}$ \ and \ "
                           rf"${L['w4a8_hadamard'] - base:+.3f}$", font_size=19, color=GREY_A))
        ctx.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.35)
        hc = history_card(2024, r"Zechun Liu et al., \ SpinQuant", rf"some random rotations are better than others, "
                          rf"\ by up to ${F.SPINQUANT['spread']}$ points; \ learn the rotation instead", width=4.2,
                          font_size=16, color=LEARNC).to_corner(UR, buff=0.2).shift(DOWN * 0.6)
        p, h_ = vals[0], vals[2]
        cut = 1 - h_ / p
        say = (f"the Hadamard rotation cuts it to {h_:.3f}, {100 * cut:.0f} percent less" if h_ < 0.9 * p else
               f"the Hadamard rotation barely changes it, {h_:.3f}")
        if max(rnd) - min(rnd) < 0.01:
            rnd_say = (f"Three different random rotations give {min(rnd):.3f} to {max(rnd):.3f}: on our model, nearly "
                       "the same. But in 2024 Zechun Liu and colleagues at Meta found that on large models, random "
                       "rotations can differ by up to thirteen points on a benchmark, and asked: why not learn the "
                       "rotation?")
        else:
            rnd_say = (f"Three different random rotations give {min(rnd):.3f} to {max(rnd):.3f}. In 2024 Zechun Liu "
                       "and colleagues at Meta noticed such differences, up to thirteen points on a benchmark, and "
                       "asked: why not learn the rotation?")
        lv = vals[4]
        if lv < h_ - 0.003:
            learn_say = f"We did, small: {lv:+.3f}, better than the Hadamard rotation it started from."
        elif lv <= h_ + 0.003:
            learn_say = f"We did, small: {lv:+.3f}, no better than the Hadamard rotation it started from."
        else:
            learn_say = f"We did, small: {lv:+.3f}, a little worse than the Hadamard rotation it started from."
        with self.voiceover(
            "Now the hard case: four-bit weights and four-bit activations, every block input rounded on the fly. "
            f"<bookmark mark='a'/> Plainly, our model loses {p:.3f} nats a token; SmoothQuant {vals[1]:.3f}. "
            "<bookmark mark='b'/> Rotate first, the residual stream by a Hadamard matrix and the input of each "
            "feed-forward output by a random rotation, and " + say + ". <bookmark mark='c'/> " + rnd_say +
            " <bookmark mark='d'/> " + learn_say
        ) as vo:
            self.play(FadeIn(head), FadeIn(ctx))
            vo.wait_until("a")
            self.play(*[AnimationGroup(FadeIn(b[i].name), GrowFromEdge(b[i].bar, LEFT), FadeIn(b[i].val)) for i in (0, 1)])
            vo.wait_until("b")
            self.play(FadeIn(b[2].name), GrowFromEdge(b[2].bar, LEFT), FadeIn(b[2].val))
            vo.wait_until("c")
            self.play(FadeIn(b[3].name), GrowFromEdge(b[3].bar, LEFT), FadeIn(b[3].val), Create(spread), FadeIn(hc))
            vo.wait_until("d")
            self.play(FadeIn(b[4].name), GrowFromEdge(b[4].bar, LEFT), FadeIn(b[4].val))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        r = load("rotation")
        sp = r["spin"]
        cv = np.asarray(sp["curve"])
        ev = np.asarray(sp["evals"])
        k = 9
        sm = np.convolve(cv[:, 1], np.ones(k) / k, mode="valid")
        xs = cv[k // 2: k // 2 + len(sm), 0]
        lo = float(min(sm.min(), ev[:, 1].min())) - 0.03
        hi = float(max(sm.max(), ev[:, 1].max())) + 0.03
        S = int(sp["steps"])
        g = axes([0, S + 2], [lo, hi], x_length=6.4, y_length=4.0, xlabel=r"step",
                 ylabel=r"loss of the $4$-bit model \ (nats per token)", xticks=[0, S // 2, S],
                 yticks=[round(lo + 0.03, 2), round(hi - 0.03, 2)], yfmt=lambda v: f"{v:.2f}", center=[-2.3, -0.3, 0])
        ax = g.ax
        tr = curve(ax, xs, sm, GREY_B, 2)
        evd = VGroup(*[Dot(ax.c2p(a, b_), radius=0.08, color=LEARNC) for a, b_ in ev])
        evl = curve(ax, ev[:, 0], ev[:, 1], LEARNC, 3)
        key = VGroup(label(r"training batches \ (smoothed)", font_size=20, color=GREY_B),
                     label(r"held-out text, \ every $20$ steps", font_size=20, color=LEARNC)).arrange(DOWN,
                                                                                                   aligned_edge=LEFT,
                                                                                                   buff=0.12)
        key.move_to([4.4, 1.6, 0])
        f_ = MathTex(r"Q = H\,(I + A)^{-1}(I - A), \quad A^\top = -A", font_size=28, color=LEARNC).move_to([4.4, -0.9, 0])
        fl = label(r"the Cayley map: \ any skew $A$ gives a rotation, \\ so plain gradient descent stays on rotations",
                   font_size=18, color=GREY_A).next_to(f_, DOWN, buff=0.15)
        tag = note(rf"computed: \ ${int(sp['steps'])}$ steps of Adam on batches of ${int(sp['batch'])}$ calibration "
                   rf"windows, \ ${sp['seconds'] / 60:.0f}$ minutes; \ $Q Q^\top = I$ to ${sp['orth_err']:.0e}$",
                   font_size=17).to_corner(DR, buff=0.2)
        gain = ev[0, 1] - ev[-1, 1]
        st = int(sp["steps"])
        if gain > 0.005:
            learn_say = (f"Over {st} steps the held-out loss fell from {ev[0, 1]:.3f} to {ev[-1, 1]:.3f}: the "
                         "rotation learned where our model's outliers are.")
        elif gain > -0.002:
            learn_say = (f"Over {st} steps the held-out loss went from {ev[0, 1]:.3f} to {ev[-1, 1]:.3f}: the "
                         "Hadamard start was already close to the best this training could find.")
        else:
            learn_say = (f"Over {st} steps the held-out loss rose from {ev[0, 1]:.3f} to {ev[-1, 1]:.3f}: the "
                         "rotation fitted its little calibration text, not the novels.")
        with self.voiceover(
            "Learning a rotation needs care, because a gradient step on a rotation matrix makes it something else. "
            "<bookmark mark='a'/> SpinQuant keeps it a rotation by construction. Write Q as the Hadamard matrix "
            "times the Cayley map of a skew-symmetric matrix A: every A gives a rotation, so A can be trained "
            "freely. <bookmark mark='b'/> We trained A on our model's loss with four-bit weights and activations, "
            "the rounding passed straight through for the gradient, starting from the Hadamard rotation. "
            "<bookmark mark='c'/> " + learn_say
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(f_), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(tr), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in evd], lag_ratio=0.2), Create(evl), FadeIn(key[1]))
        self.wait(0.3)
        self.clear_scene()
