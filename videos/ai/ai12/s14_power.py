from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import FIT, HIST, NCOL, PART, QUANT, load, width_ramp

DIM_COLORS = ["#7FD3FF", C.INTERVAL, C.BITS, C.SURPRISE]


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.manifold()
        self.quanta()
        self.toy()

    def card(self):
        card = chapter_card(13, r"Why power laws?", r"Where does the straight line on log axes come from?", part=PART)
        with self.voiceover("Chapter thirteen. Why power laws?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def manifold(self):
        z = load("manifold")
        dims = [int(d) for d in z["dims"]]
        Ns = np.asarray(z["pieces"], float)
        colors = {r"d": C.BITS, r"N": NCOL}
        rows = [
            cmath(r"\text{piece size}", r"\sim", r"N^{-1/d}", font_size=32, colors=colors),
            cmath(r"\text{error of a linear piece}", r"\sim", r"(\text{size})^2", font_size=32),
            cmath(r"\text{loss (squared)}", r"\sim", r"N^{-4/d}", font_size=32, colors=colors),
        ]
        whys = [why(r"$N$ pieces tile a $d$-dimensional surface"), why(r"Taylor: \ the curvature is left over"),
                why(r"square it")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.4, buff=0.3, edge=6.9)
        lN = np.log10(Ns)
        allv = np.log10(np.concatenate([np.asarray(z[f"err{d}"]).mean(0) for d in dims]))
        allv = allv[np.isfinite(allv)]
        y0, y1 = math.floor(max(allv.min(), -14)), math.ceil(allv.max())
        ax = CornerAxes(x_range=[lN.min() - 0.1, lN.max() + 0.1, 1], y_range=[y0, y1, 2], x_length=5.8, y_length=3.5, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -1.5, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in range(math.ceil(lN.min()), math.floor(lN.max()) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(ax.c2p(lN.min() - 0.1, v), LEFT, buff=0.08)
                      for v in range(y0, y1 + 1, 4)])
        xn = label(r"pieces $N$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.06)
        lines, labs = VGroup(), VGroup()
        for d, col in zip(dims, DIM_COLORS):
            e = np.asarray(z[f"err{d}"]).mean(0)
            keep = np.log10(e) >= y0
            lines.add(curve(ax, lN[keep], np.log10(e[keep]), col, 3))
            labs.add(label(rf"$d = {d}$: \ slope ${float(z[f'slope{d}']):.2f}$ \ (theory ${-4 / d:.2f}$)", font_size=22, color=col))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, -1.2, 0])
        tag = note(r"computed: \ a smooth function on a $d$-dimensional torus, \ cut into $N$ linear pieces").to_corner(DR, buff=0.2)
        cite_ = cite(r"U.~Sharma \& J.~Kaplan, \textit{A Neural Scaling Law from the Dimension of the Data Manifold} (2020)",
                     corner=UL).shift(DOWN * 0.0)
        cite_.to_edge(UP, buff=0.12).shift(RIGHT * 0.0)
        s8, t8 = float(z[f"slope{dims[-1]}"]), -4 / dims[-1]
        late = abs(s8 - t8) > 0.1
        with self.voiceover(
            "Why should loss fall as a power law at all? One answer, from Utkarsh Sharma and Jared Kaplan in 2020: "
            "real data lies near a surface of low dimension d inside its huge space. A model with N parameters cuts "
            "that surface into about N pieces, <bookmark mark='a'/> so each piece is about N to the minus one over d "
            "across. <bookmark mark='b'/> Fit each piece with a straight line, and what's left is the curvature, the "
            "square of the size. <bookmark mark='c'/> Square again for a squared loss: the loss falls like N to the "
            "minus four over d. A power law, with the exponent set by the data's dimension. "
            "<bookmark mark='d'/> Check it: a smooth function on surfaces of dimension 1, 2, 4 and 8. "
            + (f"The slopes match four over d, until eight dimensions, where even a hundred thousand pieces are still "
               f"too coarse: {s8:.2f}, on its way to {t8:.2f}." if late else
               "The slopes match four over d.")
            + " Low-dimensional data, steep laws; language, by this account, is high-dimensional."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(tag))
            for l_, lb in zip(lines, labs):
                self.play(Create(l_), FadeIn(lb), run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quanta(self):
        q = load("quanta")
        p = np.asarray(q["p"], float)
        T = int(q["tasks"])
        alpha = float(q["alpha"])
        colors = {r"\alpha": QUANT, r"n": NCOL}
        rows = [
            cmath(r"p_k", r"\propto", r"k^{-(\alpha + 1)}", font_size=34, colors=colors),
            cmath(r"L(n)", r"=", r"\textstyle\sum_{k > n} p_k", font_size=34, colors=colors),
            cmath(r"L(n)", r"\approx", r"\int_n^\infty k^{-(\alpha+1)}\, dk \;\propto\; n^{-\alpha}", font_size=34, colors=colors),
        ]
        whys = [why(r"skills used with Zipf's frequencies"), why(r"the $n$ most used are learned; \ the rest cost their share"),
                why(r"$n \propto N$: \ a power law in the size")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.6, buff=0.32, edge=6.9)
        bars = VGroup(*[Rectangle(width=0.22, height=max(3.0 * v / p.max(), 0.02), stroke_width=0, fill_color=QUANT,
                                  fill_opacity=0.85) for v in p]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        bars.move_to([-1.4, -2.0, 0], aligned_edge=DOWN)
        bars.shift(DOWN * (bars.get_bottom()[1] + 3.2))
        bl = label(rf"our toy: \ ${T}$ subtasks, \ $p_k \propto k^{{-{alpha + 1:.1f}}}$", font_size=22, color=QUANT)
        bl.next_to(bars, UP, buff=0.12).align_to(bars, LEFT)
        cut = DashedLine(bars[7].get_corner(DR) + RIGHT * 0.03, bars[7].get_corner(DR) + RIGHT * 0.03 + UP * 3.2, color=WHITE,
                         stroke_width=2)
        cl = label(r"learned \ $\leftarrow \ | \ \rightarrow$ \ not yet", font_size=20, color=WHITE).next_to(cut, UP, buff=0.05)
        task = label(r"each subtask: \ the parity of $3$ hidden bits out of $12$; \ a one-hot tag says which", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.15)
        cite_ = cite(r"E.~Michaud, Z.~Liu, U.~Girit \& M.~Tegmark, \textit{The Quantization Model of Neural Scaling} (2023)",
                     corner=UR)
        with self.voiceover(
            "A second answer, from Eric Michaud, Max Tegmark and colleagues in 2023: the quantization model. Suppose "
            "what a model knows comes in discrete chunks, quanta, each a skill that is either learned or not, and "
            "that they are used with Zipf's frequencies, a power law. <bookmark mark='a'/> A model with room for n "
            "quanta learns the n most used, and loses the share of the rest. <bookmark mark='b'/> Add up a power-law "
            "tail, and you get a power law in n, so in the model's size. <bookmark mark='c'/> They built a task to "
            f"test it, and we built a small version: {T} subtasks, each the parity of three hidden bits out of "
            "twelve, appearing with Zipfian frequencies."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(bars), FadeIn(bl), Create(cut), FadeIn(cl))
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(task))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toy(self):
        q = load("quanta")
        widths = [int(w) for w in q["widths"]]
        per = np.asarray(q["per_task"], float)  # W x seeds x T x tasks
        steps = np.asarray(q["steps"], float)
        mean = np.asarray(q["mean"], float)  # W x seeds x T
        Np = np.asarray(q["n_params"], float)
        T = int(q["tasks"])
        learned = np.asarray(q["learned"])
        # left: the subtasks of one run (width 128, seed 0), learned one at a time
        wi = widths.index(128) if 128 in widths else len(widths) // 2
        run = per[wi, 0]
        ax = CornerAxes(x_range=[0, steps.max(), steps.max() / 4], y_range=[0, 1.1, 0.5], x_length=5.8, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.3, -0.6, 0])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=18, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in np.linspace(0, steps.max(), 5)])
        xn = label(r"training steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(rf"each subtask's loss \ (bits), \ width ${widths[wi]}$", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        sub = VGroup(*[curve(ax, steps, np.minimum(run[:, k], 1.1), interpolate_color(ManimColor(QUANT), ManimColor(GREY_D), k / T),
                             2.2).set_stroke(opacity=0.9) for k in range(T)])
        avg = curve(ax, steps, np.minimum(mean[wi, 0], 1.1), WHITE, 4)
        al = label(r"white: \ the average", font_size=20, color=WHITE).next_to(ax.c2p(steps.max(), 1.0), DL, buff=0.1)
        # right: the average loss at the end, against the size
        fin = mean[:, :, -1]
        lx = np.log10(Np)
        ly = np.log10(np.maximum(fin, 1e-4))
        y0, y1 = math.floor(ly.min()), math.ceil(ly.max())
        bx = CornerAxes(x_range=[lx.min() - 0.1, lx.max() + 0.1, 1], y_range=[y0, y1, 1], x_length=4.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.6, -0.6, 0])
        bxt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(bx.c2p(v, y0), DOWN, buff=0.08)
                       for v in range(math.ceil(lx.min() - 0.1), math.floor(lx.max() + 0.1) + 1)])
        byt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(bx.c2p(lx.min() - 0.1, v), LEFT, buff=0.08)
                       for v in range(y0, y1 + 1)])
        bxn = label(r"parameters", font_size=20, color=GREY_A).next_to(bxt, DOWN, buff=0.08)
        byn = label(r"average loss at the end", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.12).align_to(bx, LEFT)
        pts = VGroup(*[Dot(bx.c2p(a, b), radius=0.06, color=width_ramp(i, len(widths))) for i, (a, row) in enumerate(zip(lx, ly))
                       for b in row])
        cl = curve(bx, lx, ly.mean(1), WHITE, 2.5)
        sN = float(q["slope_N"])
        nl = VGroup(*[MathTex(str(int(n_)), font_size=18, color=width_ramp(i, len(widths))).next_to(bx.c2p(a, b), UP, buff=0.08)
                      for i, (a, b, n_) in enumerate(zip(lx, ly.mean(1), learned.mean(1)))])
        nll = label(r"numbers: \ subtasks learned", font_size=18, color=GREY_A).next_to(bx, DOWN, buff=0.55).align_to(bx, LEFT)
        tag = note(r"two seeds per width").to_corner(DR, buff=0.2)
        n_learn = int((run[-1] < 0.1).sum())
        order = [int(steps[np.argmax(run[:, k] < 0.1)]) if (run[:, k] < 0.1).any() else 10 ** 9 for k in range(T)]
        in_order = np.corrcoef(np.arange(T)[np.array(order) < 10 ** 9], np.array(order)[np.array(order) < 10 ** 9])[0, 1] \
            if sum(o < 10 ** 9 for o in order) > 3 else 0.0
        with self.voiceover(
            f"Here is one network, of width {widths[wi]}, learning the subtasks. <bookmark mark='a'/> Each subtask's "
            "loss sits at one bit, a coin flip, and then drops, suddenly. "
            + ("The common subtasks drop first, the rare ones later. " if in_order > 0.5 else
               "The order roughly follows how common they are. ")
            + f"By the end it has learned {n_learn} of the {T}. <bookmark mark='b'/> The average over the mix, in white, "
            "is smooth: many sudden steps, added up. <bookmark mark='c'/> And across sizes, wider networks learn more "
            f"subtasks, and the average loss falls along a power law, slope {sN:.2f}. "
            + (f"The theory's exponent here is {float(q['alpha']):.1f}; ours is steeper, because a wider network also "
               "learns each subtask more cleanly." if sN < -float(q["alpha"]) - 0.2 else
               f"close to the theory's {float(q['alpha']):.1f}.")
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in sub], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(al))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bxt), FadeIn(byt), FadeIn(bxn), FadeIn(byn))
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in pts], lag_ratio=0.05), Create(cl), FadeIn(nl), FadeIn(nll))
        self.wait(0.3)
        self.clear_scene()
