from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

LEVEL = ("#F7D154", "#FF9F5A", "#7EC8F5")  # what is computed; by what algorithm; in what stuff


def neuron(scale=1.0, color=P.EXC) -> VGroup:
    soma = Circle(radius=0.28 * scale, stroke_width=0, fill_color=color, fill_opacity=0.9)
    rng = np.random.default_rng(4)
    den = VGroup()
    for a in np.linspace(1.9, 4.4, 5):
        end = np.array([np.cos(a), np.sin(a), 0]) * scale * (0.9 + 0.3 * rng.random())
        den.add(Line(np.array([np.cos(a), np.sin(a), 0]) * 0.25 * scale, end, color=color, stroke_width=3))
        for b in (-0.5, 0.5):
            tip = end + np.array([np.cos(a + b), np.sin(a + b), 0]) * 0.35 * scale
            den.add(Line(end, tip, color=color, stroke_width=2))
    axon = Line(RIGHT * 0.25 * scale, RIGHT * 2.0 * scale, color=color, stroke_width=3)
    ends = VGroup(*[Line(axon.get_end(), axon.get_end() + np.array([0.3, dy, 0]) * scale, color=color, stroke_width=2)
                    for dy in (-0.25, 0, 0.25)])
    return VGroup(den, axon, ends, soma)


def register() -> VGroup:
    """A cash register: a body, a display, a pad of keys, a drawer."""
    body = RoundedRectangle(width=2.9, height=2.3, corner_radius=0.15, stroke_color=GREY_A, stroke_width=2.5,
                            fill_color="#1A2130", fill_opacity=1)
    display = Rectangle(width=2.1, height=0.6, stroke_color=GREY_B, stroke_width=1.5, fill_color="#06120C",
                        fill_opacity=1).move_to(body.get_top() + DOWN * 0.5)
    total = MathTex(r"5.75", font_size=38, color="#7BD88F").move_to(display)
    keys = VGroup(*[RoundedRectangle(width=0.36, height=0.26, corner_radius=0.05, stroke_width=0, fill_color=GREY_B,
                                     fill_opacity=0.8) for _ in range(12)]).arrange_in_grid(3, 4, buff=0.1)
    keys.move_to(body.get_center() + DOWN * 0.45)
    drawer = RoundedRectangle(width=3.3, height=0.6, corner_radius=0.1, stroke_color=GREY_A, stroke_width=2.5,
                              fill_color="#141A26", fill_opacity=1).next_to(body, DOWN, buff=0)
    knob = Dot(drawer.get_center(), radius=0.06, color=GREY_A)
    g = VGroup(drawer, knob, body, display, total, keys)
    g.total = total
    return g


def level_card(i, title, body: Mobject, width=8.9) -> VGroup:
    color = LEVEL[i]
    num = label(rf"{i + 1}", font_size=44, color=color)
    t = label(title, font_size=32, color=color)
    head = VGroup(num, t).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(width=width, height=inner.height + 0.5, corner_radius=0.14, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.95)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    g = VGroup(box, inner)
    g.body = body
    return g


class Marr(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.register_levels()
        self.apply()

    def card(self):
        card = chapter_card(9, r"Three levels of explanation", r"Neurons, or boxes and arrows: \ which one explains "
                            r"the mind?", lit=(1982,), part=PART, scale=("neuron", "mind"),
                            marr=("what", "how", "tissue"))
        with self.voiceover(
            "Chapter nine. Three levels of explanation."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        nr = neuron(1.25).move_to([-3.9, 1.35, 0])
        n_cap = VGroup(label(r"open the skull", font_size=34, color=P.EXC),
                       label(r"study neurons", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.1)
        n_cap.next_to(nr, DOWN, buff=0.25)
        boxes = VGroup(*[RoundedRectangle(width=1.35, height=0.7, corner_radius=0.1, stroke_color=DISC, stroke_width=2,
                                          fill_color=DISC, fill_opacity=0.12) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=3,
                                max_tip_length_to_length_ratio=0.4) for a, b in zip(boxes, boxes[1:])])
        flow = VGroup(boxes, arrows).move_to([3.7, 1.35, 0])
        f_cap = VGroup(label(r"never touch a brain", font_size=34, color=DISC),
                       label(r"study the flow of information", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.1)
        f_cap.next_to(flow, DOWN, buff=0.25).align_to(n_cap, UP)
        vs = label(r"Which one explains the mind?", font_size=40).to_edge(UP, buff=0.3)
        marr = history_card(1982, r"David Marr, \ \emph{Vision}", r"published two years after his death at "
                            r"thirty-five: \ both, \ and a third thing that matters more than either",
                            color=P.ACCENT, width=10.0, font_size=28).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So now there are two sciences of one thing. One group opens the skull, and studies neurons. "
            "<bookmark mark='a'/> The other draws information flowing between boxes, and never touches a brain. "
            "<bookmark mark='b'/> Which of them explains the mind? <bookmark mark='c'/> The clearest answer came "
            "from David Marr, a vision scientist who died of leukaemia at thirty-five. His book came out two "
            "years later, in 1982. His answer: both, and a third thing that matters more than either."
        ) as vo:
            self.play(FadeIn(nr, shift=UP * 0.2), FadeIn(n_cap))
            vo.wait_until("a")
            self.play(FadeIn(flow, shift=UP * 0.2), FadeIn(f_cap))
            vo.wait_until("b")
            self.play(FadeIn(vs, shift=DOWN * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(marr, shift=UP * 0.2))
        self.clear_scene()

    def register_levels(self):
        reg = register().scale(1.1).move_to([-5.1, 0.1, 0])
        b1 = VGroup(MathTex(r"3.50 + 2.25 = 5.75", font_size=40),
                    label(r"the order must not matter: \ $a + b = b + a$", font_size=28, color=GREY_A),
                    label(r"buying nothing costs nothing: \ $a + 0 = a$", font_size=28, color=GREY_A),
                    label(r"so: \ addition", font_size=30, color=LEVEL[0])).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        col = VGroup(MathTex(r"\phantom{+}\ 3.50", font_size=38), MathTex(r"+\ 2.25", font_size=38),
                     MathTex(r"\phantom{+}\ 5.75", font_size=38, color=LEVEL[1])).arrange(DOWN, buff=0.1,
                                                                                       aligned_edge=RIGHT)
        rule = Line(col[1].get_corner(DL) + DOWN * 0.04, col[1].get_corner(DR) + DOWN * 0.04, color=WHITE,
                    stroke_width=2)
        carry = MathTex(r"1", font_size=22, color=P.ACCENT).next_to(col[0], UP, buff=0.03).shift(RIGHT * 0.02)
        algo = VGroup(col, rule, carry)
        b2 = VGroup(algo, VGroup(label(r"decimal digits; \ add columns from the right; \ carry", font_size=28,
                                       color=GREY_A),
                                 label(r"or Roman numerals: \ the same sums, another way", font_size=28,
                                       color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        b2.arrange(RIGHT, buff=0.5)
        b3 = VGroup(VGroup(gear(0.24, color=LEVEL[2]), gear(0.17, color=LEVEL[2])).arrange(RIGHT, buff=-0.04),
                    label(r"gear wheels in an old register, \ transistors in a new one", font_size=28, color=GREY_A))
        b3.arrange(RIGHT, buff=0.35)
        cards = VGroup(level_card(0, r"What is computed, and why?", b1),
                       level_card(1, r"By what representation and algorithm?", b2),
                       level_card(2, r"In what hardware?", b3)).arrange(DOWN, buff=0.22)
        cards.move_to([2.35, 0, 0])
        if cards.height > 7.4:
            cards.height = 7.4
        with self.voiceover(
            "Take a cash register. You can describe it at three levels. <bookmark mark='a'/> First: what does it "
            "compute, and why? It adds prices. Why addition, and not something else? Because of what a fair total "
            "requires. The order you ring things up shouldn't matter. Buying nothing should cost nothing. "
            "Requirements like those single out addition. <bookmark mark='b'/> Second: how does it do it? Write "
            "the prices in decimal digits, add the columns from the right, and carry. That's a representation and "
            "an algorithm, and there are others. A register that worked in Roman numerals would compute the same "
            "sums a different way. <bookmark mark='c'/> Third: what is it made of? Gear wheels in an old "
            "register, transistors in a new one. <bookmark mark='d'/> Three questions, and three different kinds "
            "of answer. You can get one right while knowing nothing about the other two."
        ) as vo:
            self.play(FadeIn(reg, shift=UP * 0.2))
            for mark, c in zip("abc", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[Indicate(c[0], color=WHITE, scale_factor=1.02) for c in cards], lag_ratio=0.4))
        self.clear_scene()

    def apply(self):
        head = heading(r"Your reaction time, at three levels")
        chain = VGroup(*[RoundedRectangle(width=1.2, height=0.5, corner_radius=0.08, stroke_color=c, stroke_width=2,
                                          fill_color=c, fill_opacity=0.15) for c in (SENSE, DISC, CHOOSE, RESPOND)])
        chain.arrange(RIGHT, buff=0.25)
        b1 = label(r"decide that the light has changed: \ fast, with few false starts", font_size=31, color=WHITE)
        b2 = VGroup(chain, label(r"a chain of stages, if Donders is right", font_size=31, color=WHITE))
        b2.arrange(RIGHT, buff=0.4)
        nerve = Line(ORIGIN, RIGHT * 1.6, color=NERVE, stroke_width=6)
        b3 = VGroup(nerve, label(r"the nerves Helmholtz timed, \ and a brain not yet opened", font_size=31,
                                 color=WHITE)).arrange(RIGHT, buff=0.4)
        cards = VGroup(level_card(0, r"What is computed?", b1, width=13.0),
                       level_card(1, r"By what algorithm?", b2, width=13.0),
                       level_card(2, r"In what tissue?", b3, width=13.0)).arrange(DOWN, buff=0.2)
        if cards.height > 4.7:
            cards.height = 4.7
        cards.next_to(head, DOWN, buff=0.3)
        strip = levels_strip(scale=("mind",), marr=("how",), font_size=28, width=12.6).to_edge(DOWN, buff=0.75)
        s_note = label(r"on every chapter card: \ the scale, and the level", font_size=24, color=GREY_B)
        s_note.next_to(strip, UP, buff=0.25)
        quote = quote_card(r"Trying to understand perception by studying only neurons is like trying to understand "
                           r"bird flight by studying only feathers.", r"David Marr, \emph{Vision} (1982)", width=11.8,
                           font_size=40, color=P.ACCENT)
        with self.voiceover(
            "Now your reaction time. What is computed: a decision that the light has changed, made quickly, and "
            "without too many false starts. <bookmark mark='a'/> By what algorithm: a chain of stages, if "
            "Donders is right. <bookmark mark='b'/> In what tissue: the nerves Helmholtz timed, and a brain we "
            "haven't opened yet. <bookmark mark='c'/> Every chapter card in this series carries a strip that "
            "lights the level it's working at, and the scale, from molecules up to cultures. "
            "<bookmark mark='d'/> And Marr left a warning that this series takes to heart. Trying to understand "
            "perception by studying only neurons, he wrote, is like trying to understand bird flight by studying "
            "only feathers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(strip), FadeIn(s_note))
            for s_ in ("neuron", "brain", "person", "culture", "mind"):
                self.play(*[m.animate.set_color(P.ACCENT if k == s_ else GREY_C) for k, m in strip.scales.items()],
                          run_time=0.45)
            vo.wait_until("d")
            self.play(FadeOut(VGroup(head, cards, strip, s_note)))
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()
