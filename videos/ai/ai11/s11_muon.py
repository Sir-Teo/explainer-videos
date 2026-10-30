from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, load, takeaway_card

MU, AD = OPT_COLORS["muon"], OPT_COLORS["adam"]


class Muon(VoiceoverScene):
    def construct(self):
        self.card()
        self.orthogonalize()
        self.steepest()
        self.family()
        self.recipe()
        self.takeaway()

    def card(self):
        c = chapter_card(10, r"Muon, derived", r"What if every direction got the same push?", part=PART)
        with self.voiceover("Chapter ten. Muon, derived."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def orthogonalize(self):
        m = load("ns")
        before = np.asarray(m["sv_grad"], float)
        before = before / before.max()
        n = len(before)
        ax = Axes(x_range=[0, n, 64], y_range=[0, 1.2, 0.5], x_length=7.4, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.0, -1.3, 0])
        xl = label(rf"the gradient's ${n}$ singular values, \ largest first", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        bars_b = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, float(v)), color=GREY_B, stroke_width=2)
                          for i, v in enumerate(before)])
        bars_a = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, 1.0), color=MU, stroke_width=2,
                               stroke_opacity=0.35) for i in range(n)])
        bars_a.add(Line(ax.c2p(0, 1.0), ax.c2p(n, 1.0), color=MU, stroke_width=4))
        top10 = float((before[:10] ** 2).sum() / (before ** 2).sum())
        colors = {r"U": GREY_A, r"V^{\top}": GREY_A, r"\Sigma": GREY_B}
        svd = cmath(r"G", "=", r"U", r"\Sigma", r"V^{\top}", colors=colors, font_size=42).move_to([4.3, 1.8, 0])
        orth = cmath(r"\operatorname{orth}(G)", "=", r"U", r"V^{\top}", colors=colors, font_size=42).next_to(svd, DOWN, buff=0.4)
        on = label(r"every singular value set to $1$", font_size=24, color=MU).next_to(orth, DOWN, buff=0.2)
        frac = label(rf"the largest $10$ carry ${top10:.0%}$ \\ of the gradient's squared size".replace("%", r"\%"),
                     font_size=22, color=GREY_A).next_to(on, DOWN, buff=0.45)
        hist = history_card(2024, r"Keller Jordan et al.", r"Muon, \ \textit{MomentUm Orthogonalized by Newton--Schulz}: "
                            r"\ a speed record for training a small GPT \ (the NanoGPT speedrun)", width=5.2)
        hist.to_corner(UL, buff=0.3)
        tag = note(r"computed: \ the second hidden matrix's gradient, \ step $300$ of AdamW").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Adam treats every weight separately. But a layer's weights form a matrix, and a matrix has structure: "
            "part three's singular values. <bookmark mark='a'/> Here is a real gradient matrix from our character "
            f"model. A few directions dominate: the largest ten of its {n} singular values carry {top10:.0%} of its "
            "squared size. A step along it mostly pushes those few directions further. <bookmark mark='b'/> In "
            "December 2024 Keller Jordan and collaborators published Muon, after it set records in a public "
            "speedrun to train a small GPT. Muon replaces the gradient's singular values by ones: the same push in "
            "every direction."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars_b], lag_ratio=0.004), Write(svd), FadeIn(frac), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hist, shift=RIGHT * 0.2))
            self.play(ReplacementTransform(bars_b, bars_a), Write(orth), FadeIn(on), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steepest(self):
        colors = {r"G": GREY_A, r"\Delta W": MU, r"\eta": C.BITS}
        eqs = VGroup(
            cmath(r"\min_{\|", r"\Delta W", r"\|_2 \,\le\,", r"\eta", r"} \ \langle", r"G", r",", r"\Delta W", r"\rangle",
                  colors=colors, font_size=36),
            cmath(r"\langle", r"G", r",", r"\Delta W", r"\rangle = \sum_i \sigma_i\, u_i^{\top}", r"\Delta W", r"\, v_i \;\ge\; -",
                  r"\eta", r"\sum_i \sigma_i", colors=colors, font_size=36),
            cmath(r"\Delta W", r"= -", r"\eta", r"\, U V^{\top}", colors=colors, font_size=40),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.4)
        notes = VGroup(label(r"the best step that stretches no input by more than $\eta$", font_size=22, color=GREY_A),
                       label(r"each term is at least $-\eta\,\sigma_i$, \ since $|u^{\top} \Delta W v| \le \|\Delta W\|_2$",
                             font_size=22, color=GREY_A),
                       label(r"equality for every $i$ at once: \ Muon's step", font_size=22, color=MU))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.12)
        box = SurroundingRectangle(VGroup(eqs[2], notes[2]), color=MU, buff=0.15, corner_radius=0.1)
        cite_ = cite(r"J.~Bernstein \& L.~Newhouse, \textit{Old Optimizer, New Norm} (2024)", corner=DR)

        def stretched(center, sx, sy, col, angle=0.45):
            c = np.array(center)
            ring = DashedVMobject(Circle(radius=0.9, color=GREY_C, stroke_width=1.5), num_dashes=28).move_to(c)
            shape = Ellipse(width=1.8 * sx, height=1.8 * sy, color=col, stroke_width=3.5).rotate(angle).move_to(c)
            arrows = VGroup()
            for t in (0.0, 0.8, 1.6, 2.4):
                d = np.array([sx * math.cos(t), sy * math.sin(t)]) * 0.9
                d = np.array([d[0] * math.cos(angle) - d[1] * math.sin(angle), d[0] * math.sin(angle) + d[1] * math.cos(angle), 0])
                arrows.add(Arrow(c, c + d, buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.25,
                                 tip_length=0.14))
            return VGroup(ring, shape, arrows)

        pic_g = stretched([-5.3, 0.2, 0], 1.65, 0.3, GREY_A)
        pic_m = stretched([5.3, 0.2, 0], 1.0, 1.0, MU)
        cap_g = label(r"the gradient $G$: \\ a few directions dominate", font_size=20, color=GREY_A).next_to(pic_g, DOWN, buff=0.3)
        cap_m = label(r"Muon's step: \\ every direction moved by $\eta$", font_size=20, color=MU).next_to(pic_m, DOWN, buff=0.3)
        why_ = label(r"why the spectral norm? \ a layer computes $y = Wx$, \ and $\|\Delta W x\| \le \|\Delta W\|_2 \|x\|$: "
                     r"\\ it bounds how much the step can change any output", font_size=22, color=C.BITS).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Why set the singular values to one? Because it is the steepest step under the right notion of size. "
            "<bookmark mark='p'/> A layer multiplies its input by W. The most a step can change the output, relative "
            "to the input, is the step's largest stretch: its spectral norm. That is the natural size for a "
            "matrix. <bookmark mark='q'/> Picture what a matrix does to a circle of directions. The gradient "
            "stretches it into a long thin ellipse; Muon's step keeps it a circle. <bookmark mark='a'/> Ask for the "
            "step that lowers the loss fastest, to first order, among all steps that stretch nothing by more than "
            "eta. <bookmark mark='b'/> Write the gradient in its singular directions. Each term can be pushed down "
            "by at most eta times its singular value. <bookmark mark='c'/> And one step achieves every bound at "
            "once: minus eta times U V transpose."
        ) as vo:
            self.play(FadeIn(cite_), Create(pic_g[0]), Create(pic_m[0]), Write(eqs[0]))
            vo.wait_until("p")
            self.play(FadeIn(why_))
            self.play(TransformFromCopy(pic_g[0], pic_g[1]), *[GrowArrow(a_) for a_ in pic_g[2]], FadeIn(cap_g))
            self.play(TransformFromCopy(pic_m[0], pic_m[1]), *[GrowArrow(a_) for a_ in pic_m[2]], FadeIn(cap_m))
            vo.wait_until("q")
            self.play(Indicate(pic_g[1], color=WHITE), Indicate(pic_m[1], color=WHITE))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(*([] if k == 0 else [Write(eqs[k])]), FadeIn(notes[k]))
            self.play(Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        rows = [[r"a step bounded in", r"the steepest step", r"the optimizer"],
                [r"Euclidean norm, \ $\|\Delta\|_2 \le \eta$", r"$-\eta\, g/\|g\|$", r"(normalized) gradient descent"],
                [r"every weight, \ $\|\Delta\|_\infty \le \eta$", r"$-\eta\,\operatorname{sign}(g)$", r"Adam's limit, \ Lion"],
                [r"each matrix, \ $\|\Delta W\|_{2 \to 2} \le \eta$", r"$-\eta\, U V^\top$", r"Muon"]]
        cols = [GREY_A, WHITE, WHITE]
        tab = VGroup()
        for r_ in rows:
            tab.add(VGroup(*[label(c_, font_size=24, color=(GREY_A if r_ is rows[0] else cols[j])) for j, c_ in enumerate(r_)]))
        widths = [max(r_[j].width for r_ in tab) for j in range(3)]
        for i, r_ in enumerate(tab):
            x = -6.4
            for j, c_ in enumerate(r_):
                c_.move_to([x + c_.width / 2, 1.6 - 0.9 * i, 0])
                x += widths[j] + 0.6
        tab[2][2].set_color(AD)
        tab[3][2].set_color(MU)
        rule = Line([-6.5, 1.15, 0], [6.5, 1.15, 0], color=GREY_D, stroke_width=1.5)
        head = label(r"one recipe, \ three norms", font_size=34).to_edge(UP, buff=0.4)
        cite_ = cite(r"J.~Bernstein \& L.~Newhouse (2024); \ D.~Carlson et al., \textit{Stochastic Spectral Descent} (2015)", corner=DR)
        with self.voiceover(
            "This puts the optimizers of this part in one family. <bookmark mark='a'/> Bound the step by its "
            "Euclidean length, and the steepest step is the normalized gradient. <bookmark mark='b'/> Bound every "
            "weight separately, and it is the sign of the gradient: Adam's limit, and Lion. <bookmark mark='c'/> "
            "Bound each matrix by how much it can stretch a vector, and it is U V transpose: Muon. The difference "
            "between them is only the ruler."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]), Create(rule), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recipe(self):
        av = load("adamview")
        med = float(av["median1000"])
        lines = [
            r"for each hidden weight matrix $W$ \ ($m \times n$), \ every step:",
            r"$M \leftarrow 0.95\,M + G$ \quad (momentum)",
            r"$O \leftarrow \operatorname{NewtonSchulz}_5(G + 0.95\,M)$ \quad (orthogonalize the look-ahead)",
            r"$W \leftarrow (1 - \eta\lambda)\,W - \eta \cdot 0.2\sqrt{\max(m, n)}\; O$ \quad (decay, \ and Adam's size)",
            r"embeddings, \ the output layer, \ biases, \ norms: \ AdamW",
        ]
        box = VGroup(*[label(l_, font_size=24, color=(GREY_A if i in (0, 4) else WHITE)) for i, l_ in enumerate(lines)])
        box.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(UP * 0.8)
        frame = SurroundingRectangle(box, color=MU, buff=0.3, corner_radius=0.12, stroke_width=2)
        why02 = label(rf"$0.2\sqrt{{\max(m,n)}}$: \ an orthogonal $m \times n$ matrix has entries of size about "
                      rf"$1/\sqrt{{\max(m, n)}}$, \\ so Muon's step gets an RMS of $0.2$, \ like a typical Adam step \ "
                      rf"(ours, \ Chapter 6: \ median ${med:.2f}\,\eta$)", font_size=22, color=C.BITS).next_to(frame, DOWN, buff=0.4)
        cite_ = cite(r"K.~Jordan et al.\ (2024); \ J.~Liu et al., \textit{Muon is Scalable for LLM Training} (2025)", corner=DR)
        with self.voiceover(
            "Muon in practice, as Moonshot AI scaled it up in 2025. <bookmark mark='a'/> Keep momentum on the "
            "gradient, <bookmark mark='b'/> orthogonalize the look-ahead, with five rounds of Newton–Schulz, the "
            "next chapter, <bookmark mark='c'/> and step, with weight decay, scaled by zero point two times the "
            "square root of the larger dimension. <bookmark mark='d'/> That scale makes the typical entry of Muon's "
            "step about zero point two, the size of a typical AdamW step, so one learning rate can serve both. "
            f"Our own Adam, in Chapter six, moved its median weight by {med:.2f} eta. <bookmark mark='e'/> Muon is "
            "only for the hidden matrices; embeddings, the output layer and the small vectors stay with AdamW."
        ) as vo:
            self.play(FadeIn(box[0]), Create(frame), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(box[k + 1], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(why02))
            vo.wait_until("e")
            self.play(FadeIn(box[4]))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Muon: \ steepest descent in the spectral norm",
                          r"The steepest step that stretches no direction by more than $\eta$ is $-\eta\,UV^\top$: \ "
                          r"the gradient with its singular values set to one.",
                          r"Next: \ computing $UV^\top$ without an SVD")
        with self.voiceover(
            "So Muon is steepest descent when a matrix's step is measured by how far it can stretch a vector, and "
            "its step is the gradient with every singular value set to one. Computing that exactly takes an SVD, "
            "which is slow on a GPU. Next, how Muon avoids it."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
