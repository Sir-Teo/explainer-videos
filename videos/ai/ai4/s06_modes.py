from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HIST, PART, VALUE, load


def cheaper_mode_agreement(forward_work, reverse_work, forward_time, reverse_time):
    """A timing tie is not evidence that the cheaper mode was faster."""
    fw, rw, ft, rt = map(np.asarray, (forward_work, reverse_work, forward_time, reverse_time))
    different = fw != rw
    faster = ((fw < rw) & (ft < rt)) | ((rw < fw) & (rt < ft))
    return int((different & faster).sum()), int(different.sum())


def block(rows, cols, unit=0.32, color=VALUE, opacity=0.55, label_tex=None):
    """A matrix drawn as a rectangle of its shape (rows x cols cells)."""
    r = Rectangle(width=cols * unit, height=rows * unit, stroke_color=color, stroke_width=2.5, fill_color=color,
                  fill_opacity=opacity)
    g = VGroup(r)
    if label_tex:
        g.add(MathTex(label_tex, font_size=30, color=WHITE).move_to(r))
    return g


class Modes(VoiceoverScene):
    def construct(self):
        self.card()
        self.products()
        self.counted()
        self.parameters()
        self.history()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Forwards or backwards?", r"Which end of the chain should you start from?",
                            lit=(1970, 1986), part=PART)
        with self.voiceover("Chapter five. Forwards, or backwards?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def products(self):
        dc = definition_card(
            r"JVP and VJP",
            r"A \textbf{Jacobian-vector product} $v \mapsto J v$ pushes a change of the inputs forward to the outputs "
            r"(forward mode). \ A \textbf{vector-Jacobian product} $u \mapsto u^\top J$ pulls a sensitivity of the "
            r"outputs back to the inputs (reverse mode). \ Each costs about one pass through the computation.",
            width=12.8, font_size=22).to_edge(UP, buff=0.3)
        names = [r"\theta", r"h_1", r"h_2", r"h_3", r"\mathcal{L}"]
        xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        nodes = VGroup()
        for n_, x in zip(names, xs):
            c = Circle(radius=0.42, color=VALUE if n_ != r"\mathcal{L}" else C.LOSS, stroke_width=3).move_to([x, 0.1, 0])
            nodes.add(VGroup(c, MathTex(n_, font_size=36).move_to(c)))
        arrows = VGroup(*[Arrow(nodes[k][0].get_right(), nodes[k + 1][0].get_left(), buff=0.08, color=GREY_B,
                                stroke_width=3) for k in range(4)])
        jl = VGroup(*[MathTex(rf"J_{k + 1}", font_size=30, color=GREY_A).next_to(arrows[k], UP, buff=0.1) for k in range(4)])
        prod = MathTex(r"J", r"=", r"J_4\, J_3\, J_2\, J_1", font_size=44).move_to(DOWN * 1.25)
        jvp = MathTex(r"J v = J_4\big(J_3\big(J_2\,(J_1 v)\big)\big)", font_size=36, color=VALUE).move_to([-3.4, -2.5, 0])
        vjp = MathTex(r"u^\top J = \big(\big((u^\top J_4)\,J_3\big)\,J_2\big)\,J_1", font_size=36, color=GRAD)
        vjp.move_to([3.4, -2.5, 0])
        fwl = label(r"forward mode: \ in the order the network runs", font_size=22, color=VALUE).next_to(jvp, DOWN, buff=0.15)
        bwl = label(r"reverse mode: \ from the output back", font_size=22, color=GRAD).next_to(vjp, DOWN, buff=0.15)
        with self.voiceover(
            "There are two ways to use a Jacobian without ever writing it down. Push a direction forward: if the "
            "inputs move by v, the outputs move by J v, a Jacobian-vector product. Or pull a sensitivity back: if "
            "the outputs matter with weights u, the inputs matter by u transposed J, a vector-Jacobian product. "
            "<bookmark mark='a'/> A network is a chain of maps, from its parameters, theta, to the loss, and its "
            "Jacobian is a product of the links' Jacobians. <bookmark mark='b'/> A JVP multiplies that product from "
            "the right, in the order the network runs: forward mode. <bookmark mark='c'/> A VJP multiplies from the "
            "left, starting at the loss: reverse mode. Either one is about one pass through the network. For the "
            "whole Jacobian you need a JVP per input, or a VJP per output."
        ) as vo:
            self.play(FadeIn(dc, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.15),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(jl), Write(prod))
            vo.wait_until("b")
            self.play(Write(jvp), FadeIn(fwl))
            self.play(LaggedStart(*[a.animate.set_color(VALUE) for a in arrows], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("c")
            self.play(Write(vjp), FadeIn(bwl))
            self.play(LaggedStart(*[a.animate.set_color(GRAD) for a in reversed(arrows)], lag_ratio=0.3), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("modes")
        sizes = [int(v) for v in d["sizes"]]
        fwd, rev, prim = (np.asarray(d[k]) for k in ("fwd", "rev", "primal"))
        tf, tr = np.asarray(d["t_fwd"]), np.asarray(d["t_rev"])
        assert d["agree"] < 1e-9 and d["lib_diff"] < 1e-9
        k = len(sizes)
        cell = 0.74

        def grid(vals, color, x0, title):
            g = VGroup()
            vmax = np.log10(vals.max())
            for i in range(k):
                for j in range(k):
                    v = vals[i, j]
                    op = 0.12 + 0.8 * np.log10(v) / vmax
                    sq = Square(side_length=cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=color, fill_opacity=op)
                    sq.move_to([x0 + j * cell, 1.55 - i * cell, 0])
                    g.add(VGroup(sq, MathTex(f"{v:.0f}", font_size=22).move_to(sq)))
            rl = VGroup(*[MathTex(str(s), font_size=18, color=GREY_B).next_to(g[i * k][0], LEFT, buff=0.12) for i, s in enumerate(sizes)])
            cl = VGroup(*[MathTex(str(s), font_size=18, color=GREY_B).next_to(g[j][0], UP, buff=0.1) for j, s in enumerate(sizes)])
            t = label(title, font_size=24, color=color).next_to(cl, UP, buff=0.2)
            return VGroup(g, rl, cl, t)

        gf = grid(fwd / prim, VALUE, -5.4, r"forward mode")
        gr = grid(rev / prim, GRAD, 1.6, r"reverse mode")
        ax_lab = VGroup(label(r"rows: \ $n$ inputs \qquad columns: \ $m$ outputs", font_size=22, color=GREY_A),
                        label(r"whole Jacobian: \ derivative matrix-product and tanh work / reference primal work",
                              font_size=20, color=GREY_A),
                        label(r"timings also include primal computation and implementation overhead", font_size=18,
                              color=GREY_B)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=1.0)
        agree, total = cheaper_mode_agreement(fwd, rev, tf, tr)
        timed = label(rf"timed: \ the cheaper mode by count was faster in ${agree}$ of ${total}$ networks", font_size=24,
                      color=WHITE).to_edge(DOWN, buff=0.4)
        tail = (f"across the {total} networks where the counts differ, the cheaper mode by count was also the "
                "faster in every one." if agree == total else
                f"across the {total} networks where the counts differ, the cheaper mode by count was also the "
                f"faster in {agree} of them.")
        with self.voiceover(
            "Let's count. These are networks with two hidden layers of sixty-four, with n inputs and m outputs, "
            "from one to two hundred and fifty-six. We count dense derivative matrix products and tanh "
            "multiplications, relative to a reference primal pass; this is not every scalar operation. "
            "<bookmark mark='a'/> The full Jacobian takes n forward directions. <bookmark mark='b'/> Or m reverse "
            "directions. Few inputs and many outputs favor forward mode; many inputs and few outputs favor reverse "
            "mode. <bookmark mark='c'/> Timings include primal computation and implementation overhead, separately "
            "from the derivative count. In this recorded benchmark, " + tail
        ) as vo:
            self.play(FadeIn(ax_lab), FadeIn(gf[1:]), FadeIn(gr[1:]))
            self.play(LaggedStart(*[FadeIn(c) for c in gf[0]], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("a")
            self.play(Indicate(gf[3], color=VALUE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in gr[0]], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(timed))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parameters(self):
        d = load("modes")
        p = load("params")
        P = int(d["P"])
        cr = d["madds_fwd"] / d["madds_rev"]
        tr_ = d["t_param_fwd"] / d["t_param_rev"]
        bench = d["benchmark"]
        assert d["grad_diff"] < 1e-12
        fw = label(r"forwards: \ from $\theta$", font_size=30, color=VALUE).move_to([-3.6, 3.0, 0])
        bw = label(r"backwards: \ from $\mathcal{L}$", font_size=30, color=GRAD).move_to([3.6, 3.0, 0])
        divider = DashedLine([0, 2.6, 0], [0, -1.2, 0], color=GREY_D)
        u_ = 0.22
        f_steps = [block(4, 6, u_, VALUE), block(4, 6, u_, VALUE), block(4, 6, u_, VALUE), block(1, 6, u_, VALUE)]
        b_steps = [block(1, 4, u_, GRAD), block(1, 4, u_, GRAD), block(1, 4, u_, GRAD), block(1, 6, u_, GRAD)]
        f_lab = [r"J_1", r"J_2 J_1", r"J_3 J_2 J_1", r"J_4 J_3 J_2 J_1"]
        b_lab = [r"J_4", r"J_4 J_3", r"J_4 J_3 J_2", r"J_4 J_3 J_2 J_1"]
        frows, brows = VGroup(), VGroup()
        for k in range(4):
            frows.add(VGroup(f_steps[k], MathTex(f_lab[k], font_size=26, color=VALUE)).arrange(RIGHT, buff=0.3))
            brows.add(VGroup(b_steps[k], MathTex(b_lab[k], font_size=26, color=GRAD)).arrange(RIGHT, buff=0.3))
        frows.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.6, 0.65, 0])
        brows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.6, 0.9, 0])
        net = d["net"]
        res = VGroup(
            label(rf"a classifier, ${net[0]} \to {net[1]} \to {net[2]}$: \ ${P}$ parameters in, \ one loss out",
                  font_size=26, color=WHITE),
            label(rf"dense forward directions: \ ${cr:.0f}\times$ derivative work; \ ${tr_:.2f}\times$ observed call time",
                  font_size=24, color=VALUE),
            label(rf"one reverse pass: \ parameter gradients only, no $dX$; \ max gap ${sci(d['grad_diff'], 0)}$",
                  font_size=24, color=GRAD),
            label(rf"GPT-2: \ ${p['gpt2']:,}$ passes against one".replace(",", "{,}"), font_size=26, color=GREY_A),
            label(rf"timing means: \ ${bench['warmups']}$ warm-up; \ forward ${bench['parameter_forward_repeats']}$, "
                  rf"reverse ${bench['parameter_reverse_repeats']}$ repeats; \ no uncertainty interval",
                  font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        timing = (f"The observed forward-to-reverse call-time ratio is {tr_:.2f}. These means include different "
                  "implementation and graph-building costs, with no confidence interval; the work count is not a "
                  "universal lower bound for optimized forward differentiation.")
        with self.voiceover(
            "Training is the extreme case: every parameter is an input, and the loss is a single output. "
            "<bookmark mark='a'/> Forwards, you carry a matrix with a column for every parameter. <bookmark mark='b'/> "
            "Backwards, a single row, the size of the layer you've reached. <bookmark mark='c'/> Our small classifier "
            f"has {P} parameters. Forward mode pushes {P} directions through it: counted, {cr:.0f} times the "
            f"dense derivative work of one backward pass, counting matrix products and tanh multiplications. "
            f"Only parameter gradients are requested, not an input gradient. {timing} The measured gradient "
            f"difference is shown. <bookmark mark='d'/> For GPT-2 the same column-by-column strategy would require "
            f"{p['gpt2']:,} directions against one reverse pass. That is why standard large-parameter gradient "
            "training usually uses reverse mode, called backpropagation for neural networks. Forward and hybrid "
            "methods still have other uses."
        ) as vo:
            self.play(FadeIn(fw), FadeIn(bw), Create(divider))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in frows], lag_ratio=0.4), run_time=1.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in brows], lag_ratio=0.4), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in res[:3]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(res[3]), FadeIn(res[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1970, r"Seppo Linnainmaa, \ master's thesis, Helsinki",
                         r"reverse accumulation, \ to track how rounding errors add up through a program", width=4.2,
                         font_size=19, color=HIST),
            history_card(1974, r"Paul Werbos, \ PhD thesis, Harvard",
                         r"proposes the same backward pass to train networks \ (worked out for them in 1982)",
                         width=4.2, font_size=19, color=HIST),
            history_card(1986, r"David Rumelhart, Geoffrey Hinton, Ronald Williams, \ \textit{Nature}",
                         r"networks that learn their own internal representations by back-propagating errors",
                         width=4.2, font_size=19, color=HIST),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.6)
        pre = label(r"before them: \ the same backward recursion for flight paths, \ Henry Kelley (1960) and "
                    r"Arthur Bryson (1961)", font_size=22, color=GREY_A).next_to(cards, DOWN, buff=0.5)
        head = label(r"who ran the chain rule backwards", font_size=34).to_edge(UP, buff=0.35)
        tl = timeline(lit=(1970, 1986)).scale(0.95).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Reverse mode was found more than once. Seppo Linnainmaa described it in his 1970 master's thesis in "
            "Helsinki, to work out how rounding errors accumulate through a program. <bookmark mark='a'/> Paul "
            "Werbos proposed it for training networks in his 1974 thesis, <bookmark mark='b'/> and in 1986 David "
            "Rumelhart, Geoffrey Hinton and Ronald Williams showed, in Nature, what it could do: networks that "
            "learn their own internal representations. <bookmark mark='c'/> Control engineers had already used the "
            "same backward recursion around 1960, to steer rockets along the best flight paths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(pre))
        self.wait(0.3)
        self.clear_scene()
