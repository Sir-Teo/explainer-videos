from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

K = 0.1  # the Weber fraction used in the pictures (illustrative: round numbers)
WEIGHT = "#C9A227"


def weight(grams: float, color=WEIGHT) -> VGroup:
    """A weight drawn with its area proportional to its mass."""
    side = 0.07 * np.sqrt(grams)
    body = RoundedRectangle(width=side, height=side * 0.8, corner_radius=0.06, stroke_color=WHITE, stroke_width=1.5,
                            fill_color=color, fill_opacity=0.9)
    knob = Rectangle(width=side * 0.3, height=side * 0.12, stroke_width=0, fill_color=color, fill_opacity=0.9)
    knob.next_to(body, UP, buff=0)
    t = MathTex(rf"{grams:.0f}\,\text{{g}}", font_size=28).move_to(body)
    if t.width > side * 0.85:
        t.scale_to_fit_width(side * 0.85)
    return VGroup(body, knob, t)


class Fechner(VoiceoverScene):
    def construct(self):
        self.card()
        self.weber()
        self.law()
        self.move()

    def card(self):
        card = chapter_card(5, r"Measuring a sensation", r"How do you put a number on how heavy something feels?",
                            lit={1834: r"Weber's fraction", 1850: r"Fechner's morning", 1860: r"Fechner's "
                                 r"\emph{Elements}"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter five. Measuring a sensation."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def weber(self):
        head = heading(r"The smallest difference you can notice")
        rows = VGroup()
        for g in (100, 200, 400):
            a, b = weight(g), weight(g * (1 + K), color="#E3B23C")
            vs = label(r"feels just heavier:", font_size=26, color=GREY_A)
            frac = MathTex(rf"\frac{{\Delta I}}{{I}} = \frac{{{g * K:.0f}}}{{{g}}} = \frac{{1}}{{{1 / K:.0f}}}",
                           font_size=34, color=P.ACCENT)
            row = VGroup(a, vs, b, frac)
            a.move_to([-4.6, 0, 0])
            vs.move_to([-2.4, 0, 0])
            b.move_to([0.0, 0, 0])
            frac.move_to([3.6, 0, 0])
            row.a, row.b, row.frac = a, b, frac
            rows.add(row)
        rows.arrange(DOWN, buff=0.4).move_to([0, 0.05, 0])
        for r in rows:
            for m, x in zip(r, (-4.6, -2.4, 0.0, 3.6)):
                m.set_x(x)
        rows.scale(1.3).move_to([0, 0.15, 0])
        law = label(r"Weber's law: \ the just-noticeable difference is a constant fraction of the stimulus",
                    font_size=30, color=P.ACCENT).to_edge(DOWN, buff=0.8)
        feel = VGroup(label(r"how heavy it \emph{feels}", font_size=44, color=KANT),
                      MathTex(r"=\ ?", font_size=56, color=KANT)).arrange(RIGHT, buff=0.3)
        w0 = weight(400).scale(1.25)
        grams = label(r"what the scale says", font_size=30, color=WEIGHT).next_to(w0, DOWN, buff=0.25)
        to = MathTex(r"\longrightarrow", font_size=60, color=GREY_B)
        ruler = VGroup(VGroup(w0, grams), to, feel).arrange(RIGHT, buff=0.8).move_to([0, 0.2, 0])
        tag = note(r"illustrative: \ a Weber fraction of one tenth, for round numbers").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Timing is one way to put a number on the mind. Fechner's was another, and it went at Kant's first "
            "objection head on. The objection was that a sensation has no size you can measure. You can't lay a "
            "ruler along how heavy something feels. <bookmark mark='a'/> Fechner's idea was to stop trying, and "
            "measure the world instead. Hold a weight. Now find the smallest extra weight that makes it feel "
            "just noticeably heavier. <bookmark mark='b'/> A physiologist in the same city, Ernst Weber, had "
            "already found the pattern. For a weight twice as heavy, you need twice as much extra. "
            "<bookmark mark='c'/> And twice as much again for the next. The just-noticeable difference is a "
            "constant fraction of what you start with."
        ) as vo:
            self.play(FadeIn(ruler[0], shift=UP * 0.2))
            self.play(FadeIn(to), FadeIn(feel, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(ruler), FadeIn(head), FadeIn(tag))
            self.play(FadeIn(rows[0].a), FadeIn(rows[0][1]), FadeIn(rows[0].b))
            self.play(FadeIn(rows[0].frac))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.15))
            self.play(FadeIn(law))
        self.clear_scene()

    def law(self):
        n = 24
        I = 100 * (1 + K) ** np.arange(n + 1)
        A = axes([100, 1000], [0, n + 1], x_length=6.8, y_length=4.6, xlabel=r"stimulus $I$ (grams)",
                 ylabel=r"sensation $S$, \ in just-noticeable steps", xticks=[100, 250, 500, 750, 1000],
                 yticks=[0, 8, 16, 24], center=[-2.95, -0.35, 0])
        ax = A.ax
        pts = [ax.c2p(I[0], 0)]
        for k in range(1, n + 1):
            pts += [ax.c2p(I[k], k - 1), ax.c2p(I[k], k)]
        stairs = VMobject(color=P.ACCENT, stroke_width=3).set_points_as_corners(pts)
        xs = np.linspace(100, 1000, 200)
        smooth = curve(ax, xs, np.log(xs / 100) / np.log(1 + K), WHITE, 3)
        # two steps picked out: the same rise, very different runs
        def run(k, color):
            a, b = ax.c2p(I[k], k), ax.c2p(I[k + 1], k)
            t = MathTex(rf"{I[k + 1] - I[k]:.0f}\,\text{{g}}", font_size=28, color=color)
            t.next_to(Line(a, b), DOWN, buff=0.1) if k else t.next_to(b, RIGHT, buff=0.3).shift(UP * 0.17)
            return VGroup(Line(a, b, color=color, stroke_width=6), t)

        lo, hi = run(0, P.RESP), run(n - 1, P.RESP)
        d_lo, d_hi = I[1] - I[0], I[n] - I[n - 1]
        steps = VGroup(
            MathTex(r"\frac{\Delta I}{I}", r"=", r"k", font_size=40),
            MathTex(r"\Delta S", r"=", r"1 \ \ \text{when}\ \ \Delta I = kI", font_size=40),
            MathTex(r"dS", r"=", r"\frac{1}{k}\,\frac{dI}{I}", font_size=40),
            MathTex(r"S", r"=", r"\frac{1}{k}\,\ln\frac{I}{I_0}", font_size=44),
        )
        whys = VGroup(why(r"Weber's law", 26), why(r"one noticeable step is one unit", 26), why(r"small steps", 26),
                      why(r"add them up", 26))
        steps.arrange(DOWN, buff=0.8)
        for s in steps:
            s.shift(RIGHT * (2.5 - s[1].get_x()))
        steps.shift(UP * (0.35 - steps.get_y()))
        for s, w_ in zip(steps, whys):
            w_.next_to(s, DOWN, buff=0.12).align_to(s[2], LEFT)
        steps[3].set_color(P.ACCENT)
        box = SurroundingRectangle(steps[3], color=P.ACCENT, buff=0.15, corner_radius=0.1)
        name = label(r"Fechner's law, 1860", font_size=30, color=P.ACCENT).next_to(box, DOWN, buff=0.25)
        tag = note(r"illustrative: \ $k = 1/10$").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now Fechner's step. Treat each just-noticeable difference as one unit of sensation, and count them. "
            "<bookmark mark='a'/> Start from a light weight, and climb. Each step up in sensation is the same "
            "size, by definition. But each step along the stimulus is bigger than the last, by the same "
            f"factor. Down here a step is {d_lo:.0f} grams. <bookmark mark='b'/> Up here it's {d_hi:.0f}. "
            "<bookmark mark='c'/> Equal steps of sensation for equal ratios of the stimulus: that's the "
            "signature of a logarithm. <bookmark mark='d'/> In symbols. Weber's law says the noticeable change "
            "is a fixed fraction of the stimulus. Call one noticeable change one unit of sensation. Then a small "
            "change in sensation is the change in the stimulus, divided by the stimulus. <bookmark mark='e'/> "
            "Add up the small changes, and sensation grows as the logarithm of the stimulus. "
            "<bookmark mark='f'/> That is Fechner's law. He published it in 1860, with ten years of "
            "measurements behind it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(stairs), run_time=5.0, rate_func=linear)
            self.play(FadeIn(lo))
            vo.wait_until("b")
            self.play(FadeIn(hi))
            vo.wait_until("c")
            self.play(Create(smooth), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(steps[0]), FadeIn(whys[0]))
            self.play(FadeIn(steps[1]), FadeIn(whys[1]))
            self.play(FadeIn(steps[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(Create(box), FadeOut(whys[3]), FadeIn(name))
        self.clear_scene()

    def move(self):
        inside = VGroup(label(r"inside", font_size=28, color=KANT),
                        label(r"how heavy it feels", font_size=40, color=KANT)).arrange(DOWN, buff=0.15)
        outside = VGroup(label(r"outside", font_size=28, color=WEIGHT),
                         label(r"grams, \ and a count of noticeable steps", font_size=40, color=WEIGHT))
        outside.arrange(DOWN, buff=0.15)
        arrow = MathTex(r"\Longleftarrow", font_size=60, color=GREY_B)
        row = VGroup(inside, arrow, outside).arrange(RIGHT, buff=0.6).move_to([0, 2.2, 0])
        if row.width > 13:
            row.width = 13
        math_reply = (r"a division (Helmholtz), \ a subtraction (Donders), \ a logarithm (Fechner)",
                      STATUS_COLOR["replicated"])
        board = wager_board((math_reply, None, None)).scale(0.92).move_to([0, -1.3, 0])
        law = MathTex(r"S", r"=", r"\frac{1}{k}\,\ln\frac{I}{I_0}", font_size=72, color=P.ACCENT)
        ask = label(r"Is it right? \ Part 11: \ you measure your own threshold.", font_size=32, color=GREY_A)
        opening = VGroup(law, ask).arrange(DOWN, buff=0.6)
        with self.voiceover(
            "Is the law right? That's Part 11, where you'll measure your own threshold, and meet the rival law "
            "that arrived a century later. What matters today is the move. <bookmark mark='a'/> A quantity "
            "inside the mind has been defined by things you can count outside it. <bookmark mark='b'/> So "
            "Kant's first objection now has three replies: a division, a subtraction, and a logarithm."
        ) as vo:
            self.play(FadeIn(law, shift=UP * 0.2))
            self.play(FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeOut(opening))
            self.play(FadeIn(inside, shift=RIGHT * 0.2), FadeIn(outside, shift=LEFT * 0.2), FadeIn(arrow))
            vo.wait_until("b")
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows],
                      *[FadeIn(r.reply) for r in board.rows[1:]])
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
        self.clear_scene()
