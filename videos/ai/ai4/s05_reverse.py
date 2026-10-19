from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, VALUE, load


def block(rows, cols, unit=0.32, color=VALUE, opacity=0.55, label_tex=None):
    """A matrix drawn as a rectangle of its shape (rows x cols cells)."""
    r = Rectangle(width=cols * unit, height=rows * unit, stroke_color=color, stroke_width=2.5, fill_color=color,
                  fill_opacity=opacity)
    g = VGroup(r)
    if label_tex:
        g.add(MathTex(label_tex, font_size=30, color=WHITE).move_to(r))
    return g


class Reverse(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.costs()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Forwards or backwards?", r"Which end of the chain should you start from?", lit=(1986,), part=4)
        with self.voiceover("Chapter four. Forwards, or backwards?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def chain(self):
        names = [r"\theta", r"h_1", r"h_2", r"h_3", r"\mathcal{L}"]
        sizes = [r"6", r"4", r"4", r"4", r"1"]
        xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        nodes = VGroup()
        for n, s_, x in zip(names, sizes, xs):
            c = Circle(radius=0.48, color=VALUE if n != r"\mathcal{L}" else C.LOSS, stroke_width=3).move_to([x, 1.6, 0])
            nodes.add(VGroup(c, MathTex(n, font_size=38).move_to(c), MathTex(rf"\text{{{s_} number{'s' if s_ != '1' else ''}}}", font_size=24,
                                                                           color=GREY_B).next_to(c, DOWN, buff=0.15)))
        arrows = VGroup(*[Arrow(nodes[k][0].get_right(), nodes[k + 1][0].get_left(), buff=0.08, color=GREY_B, stroke_width=3)
                          for k in range(4)])
        jl = VGroup(*[MathTex(rf"J_{k + 1}", font_size=32, color=GRAD).next_to(arrows[k], UP, buff=0.1) for k in range(4)])
        prod = MathTex(r"\frac{\partial \mathcal{L}}{\partial \theta} = J_4 \, J_3 \, J_2 \, J_1", font_size=48).move_to(DOWN * 0.6)
        shapes = VGroup(block(1, 4, color=C.LOSS, label_tex=r"J_4"), block(4, 4, color=GRAD, label_tex=r"J_3"),
                        block(4, 4, color=GRAD, label_tex=r"J_2"), block(4, 6, color=GRAD, label_tex=r"J_1"))
        shapes.arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(DOWN * 2.4)
        key = label(r"$\theta$: \ all the adjustable numbers, the parameters \qquad $\mathcal{L}$: \ the loss, "
                    r"one number to make small", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A network is a long chain of maps, from its parameters, theta, all its adjustable numbers, to a single "
            "number at the end: the loss, script L. "
            "<bookmark mark='a'/> By the chain rule, the gradient is a product of Jacobians, one for each link. "
            "<bookmark mark='b'/> The product is the same whichever end you start multiplying from. The cost is not."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                                         lag_ratio=0.2), FadeIn(key), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(jl), Write(prod))
            vo.wait_until("b")
            self.play(FadeIn(shapes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self):
        p = load("params")
        fw = label(r"forwards: \ from $\theta$", font_size=30, color=VALUE).move_to([-3.6, 3.0, 0])
        bw = label(r"backwards: \ from $\mathcal{L}$", font_size=30, color=GRAD).move_to([3.6, 3.0, 0])
        divider = DashedLine([0, 2.6, 0], [0, -3.2, 0], color=GREY_D)
        # forwards: carry a matrix with one column per parameter; backwards: carry one row
        f_steps = [block(4, 6, color=VALUE), block(4, 6, color=VALUE), block(4, 6, color=VALUE), block(1, 6, color=VALUE)]
        b_steps = [block(1, 4, color=GRAD), block(1, 4, color=GRAD), block(1, 4, color=GRAD), block(1, 6, color=GRAD)]
        f_lab = [r"J_1", r"J_2 J_1", r"J_3 J_2 J_1", r"J_4 J_3 J_2 J_1"]
        b_lab = [r"J_4", r"J_4 J_3", r"J_4 J_3 J_2", r"J_4 J_3 J_2 J_1"]
        frows, brows = VGroup(), VGroup()
        for k in range(4):
            fr = VGroup(f_steps[k], MathTex(f_lab[k], font_size=28, color=VALUE)).arrange(RIGHT, buff=0.3)
            br = VGroup(b_steps[k], MathTex(b_lab[k], font_size=28, color=GRAD)).arrange(RIGHT, buff=0.3)
            frows.add(fr)
            brows.add(br)
        frows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.6, 0.2, 0])
        brows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.6, 0.6, 0])
        f_note = label(r"a column for every parameter", font_size=26, color=VALUE).move_to([-3.6, -2.6, 0])
        b_note = label(r"one row, \ the size of each layer", font_size=26, color=GRAD).move_to([3.6, -2.6, 0])
        n = f"{p['gpt2']:,}".replace(",", "{,}")
        scale = label(rf"GPT-2: \ ${n}$ columns forwards, \ against one row backwards", font_size=30, color=WHITE)
        scale.to_edge(DOWN, buff=0.35)
        hist = cite(r"S.~Linnainmaa (1970); \ D.~E.~Rumelhart, G.~E.~Hinton \& R.~J.~Williams, \textit{Nature} (1986)",
                    corner=UR)
        with self.voiceover(
            "Start from the parameters, and you carry a whole matrix along, with a column for every parameter: in "
            "effect, you redo the chain once for every knob. <bookmark mark='a'/> Start from the loss, and you carry "
            "a single row: one number for each value in the layer you've reached, and one pass backwards tells "
            "every knob its effect at once. <bookmark mark='b'/> With one loss and a hundred million parameters, going "
            "backwards is a hundred million times less work. That's reverse-mode differentiation. Applied to neural "
            "networks, it's called backpropagation: described by Seppo Linnainmaa in 1970, and made famous by "
            "Rumelhart, Hinton and Williams in 1986."
        ) as vo:
            self.play(FadeIn(fw), Create(divider))
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in frows], lag_ratio=0.4), FadeIn(f_note), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(bw))
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in brows], lag_ratio=0.4), FadeIn(b_note), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(scale))
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()
