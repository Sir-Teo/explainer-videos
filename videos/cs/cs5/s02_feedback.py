from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, ONE, PART, WIRE, YES, ZERO, gate, load,
                                  nand_latch, wave)


def val_col(v):
    return ONE if v else ZERO


class Feedback(VoiceoverScene):
    def construct(self):
        self.card()
        self.latch_live()
        self.waves()
        self.ring()

    def card(self):
        card = chapter_card(1, r"Feedback", r"How can gates hold a bit?", part=PART)
        with self.voiceover("Chapter one. Feedback."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def latch_live(self):
        head = label(r"The SR latch", font_size=40).to_edge(UP, buff=0.35)
        lat = nand_latch(scale=1.1).move_to(LEFT * 3.0 + DOWN * 0.1)
        rows = VGroup()
        hdr = VGroup(*[MathTex(t, font_size=28, color=GREY_B) for t in (r"\bar S", r"\bar R", r"Q", r"\text{meaning}")])
        rows.add(hdr)
        for s, r, q, m, c in ((0, 1, "1", r"\text{set}", YES), (1, 0, "0", r"\text{reset}", YES),
                              (1, 1, r"Q", r"\text{hold: remember}", HEAD),
                              (0, 0, r"?", r"\text{both outputs } 1\text{: forbidden}", NO)):
            rows.add(VGroup(MathTex(str(s), font_size=30, color=DATA), MathTex(str(r), font_size=30, color=DATA),
                            MathTex(q, font_size=30, color=c), MathTex(m, font_size=26, color=c)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                if j < 3:
                    m.move_to([1.2 + 0.85 * j, 1.6 - 0.62 * i, 0])
                else:
                    m.move_to([3.7, 1.6 - 0.62 * i, 0], aligned_edge=LEFT)
        why = label(r"a NAND outputs 1 whenever either input is 0: \\ so $\bar S = 0$ forces $Q = 1$, \ and then "
                    r"$\bar Q = \overline{1 \cdot 1} = 0$ holds it", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)

        def paint(s, r, q, qn):
            return [lat.s_in.animate.set_stroke(val_col(s)), lat.r_in.animate.set_stroke(val_col(r)),
                    lat.q_out.animate.set_stroke(val_col(q)), lat.w1.animate.set_stroke(val_col(q)),
                    lat.qn_out.animate.set_stroke(val_col(qn)), lat.w2.animate.set_stroke(val_col(qn))]

        with self.voiceover(
            "Here is the latch again, with its inputs named S bar and R bar, for set and reset; the bars mean they "
            "act when they are zero. <bookmark mark='a'/> A NAND gate outputs one whenever either of its inputs is "
            "zero. So pull S bar to zero, and Q becomes one. Then the lower gate sees R bar equal to one and Q equal to "
            "one, so its output, Q bar, becomes zero, and that zero feeds back to hold Q at one. "
            "<bookmark mark='b'/> Now let S bar go back to one. Nothing changes: Q bar, still zero, keeps Q at one. The "
            "latch remembers that it was set. <bookmark mark='c'/> Pull R bar to zero, and the same story runs the "
            "other way: Q becomes zero, and stays zero when R bar is released. <bookmark mark='d'/> One input pattern "
            "is forbidden: both at zero forces both outputs to one, which is not a stored value at all, and releasing "
            "both at once leaves the latch with no idea which way to fall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lat), FadeIn(hdr))
            self.play(*paint(1, 1, 0, 1))
            vo.wait_until("a")
            self.play(*paint(0, 1, 1, 0), FadeIn(rows[1]), FadeIn(why))
            vo.wait_until("b")
            self.play(*paint(1, 1, 1, 0), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(*paint(1, 0, 0, 1), FadeIn(rows[2]))
            self.play(*paint(1, 1, 0, 1))
            vo.wait_until("d")
            self.play(*paint(0, 0, 1, 1), FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def waves(self):
        d = load("latch")["sr"]
        n = len(d["Q"])
        head = label(r"Tick by tick, \ one gate delay per tick", font_size=36).to_edge(UP, buff=0.35)
        dx = 11.0 / n
        x0 = -5.2
        ws = VGroup(wave(d["S_"], x0=x0, y=1.4, dx=dx, color=DATA, name=r"\bar S"),
                    wave(d["R_"], x0=x0, y=0.5, dx=dx, color=DATA, name=r"\bar R"),
                    wave(d["Q"], x0=x0, y=-0.4, dx=dx, color=YES, name=r"Q"),
                    wave(d["Qn"], x0=x0, y=-1.3, dx=dx, color=YES, name=r"\bar Q"))
        phases = [(3, 7, r"set"), (7, 12, r"hold"), (12, 16, r"reset"), (16, 21, r"hold"), (21, 25, r"both 0"),
                  (25, n, r"released together")]
        marks = VGroup()
        for a, b, t in phases:
            col = NO if "both" in t or "released" in t else GREY_B
            marks.add(VGroup(DashedLine([x0 + dx * a, 2.1, 0], [x0 + dx * a, -1.5, 0], color=GREY_D, stroke_width=1),
                             label(t, font_size=20, color=col).move_to([x0 + dx * (a + b) / 2, 2.25, 0])))
        osc = label(r"in this idealized model the two gates chase each other forever: \\ each flips because the other "
                    r"just flipped", font_size=26, color=NO).to_edge(DOWN, buff=0.9)
        real = note(r"real gates are never perfectly matched: \ the latch falls one way, \ at a random time \ "
                    r"(chapters 2 and 5)", font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Simulated in this series' library, with every gate taking one tick to respond, here is the whole story. "
            "<bookmark mark='a'/> Set, and Q rises one tick later, Q bar one tick after that. Hold, and nothing moves. "
            "Reset, and the pair flips back. <bookmark mark='b'/> Then the forbidden input: both outputs go to one. "
            "And when both inputs are released on the same tick, something new happens. Each gate sees the other's "
            "one, and flips to zero; then each sees the other's zero, and flips back to one. In this perfectly "
            "symmetric model they chase each other forever. <bookmark mark='c'/> Real gates are never perfectly "
            "matched, so a real latch eventually falls into one state or the other. Which one, and when, is the "
            "subject of the next chapter and of chapter five."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[Create(w) for w in ws], lag_ratio=0.15), FadeIn(marks[:4]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(marks[4:]))
            self.play(FadeIn(osc))
            vo.wait_until("c")
            self.play(FadeIn(real))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring(self):
        d = load("latch")["ring"]
        head = label(r"An odd loop: \ the ring oscillator", font_size=38).to_edge(UP, buff=0.35)
        gs = VGroup(*[gate("NOT", size=0.8) for _ in range(3)]).arrange(RIGHT, buff=1.0).move_to(UP * 1.2)
        ws = VGroup(*[Line(gs[i].out(), gs[i + 1].inp[0](), color=WIRE, stroke_width=3) for i in range(2)])
        back = VMobject(color=WIRE, stroke_width=3).set_points_as_corners([
            gs[2].out(), gs[2].out() + RIGHT * 0.4, gs[2].out() + RIGHT * 0.4 + DOWN * 0.9,
            gs[0].inp[0]() + LEFT * 0.4 + DOWN * 0.9, gs[0].inp[0]() + LEFT * 0.4, gs[0].inp[0]()])
        w = wave(d, x0=-4.5, y=-1.0, dx=0.5, color=HEAD, name=r"x_0")
        txt = VGroup(label(r"three inverters: \ no stable state, \ so it oscillates with period $2 \times 3$ gate delays",
                           font_size=26, color=GREY_A),
                     label(r"used to measure gate delay on every new chip process, \ to make clocks, \\ and, with noise, "
                           r"\ to make random bits", font_size=24, color=HEAD)).arrange(DOWN, buff=0.25).to_edge(DOWN,
                                                                                                         buff=0.45)
        with self.voiceover(
            "Two gates in a loop make a memory. Three inverters in a loop make something else. <bookmark "
            "mark='a'/> Each inverter wants its output to be the opposite of its input, and with an odd number of "
            "them, going all the way round contradicts itself: there is no consistent binary state. In this "
            "unit-delay model, the ring oscillates. A physical ring needs sufficient gain and suitable delays; it "
            "also has an unstable analog operating point. A change runs round and round it, and each signal flips "
            "every three gate delays, repeating every six. <bookmark mark='b'/> This ring oscillator is how chip "
            "makers measure the speed of a new manufacturing process, it is a cheap on-chip clock, and the jitter "
            "of free-running rings is one of the sources of true random numbers inside processors. Loops, it "
            "turns out, are where circuits get interesting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gs), Create(ws), Create(back))
            vo.wait_until("a")
            self.play(Create(w), run_time=2.5)
            self.play(FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
        self.wait(0.3)
        self.clear_scene()
