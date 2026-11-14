from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


def half(steps, width: float = 3.0, color=None) -> VGroup:
    return step_bar(steps, width=width, height=0.5, colors=(LONG, SHORT, "#C4B5FD") if color is None else color, fmt="{:.0f}", font_size=22)


class Halves(SoundScene):
    def construct(self):
        chapter(self, 7, r"A scale in two halves", r"How were scales built before keyboards?", lit=(-530,), extra=((1660, r"the 72 melakartas"),))
        self.tetrachords()
        self.two()
        self.seventy_two()

    # ------------------------------------------------------------------
    def tetrachords(self):
        d = load("halves")
        frame = VGroup(Line(LEFT * 5.0, RIGHT * 5.0, color=GREY_C, stroke_width=2))
        marks = [(0, r"C"), (5, r"F"), (7, r"G"), (12, r"C")]
        for s, nm in marks:
            x = -5.0 + 10.0 * s / 12
            frame.add(Line([x, -0.2, 0], [x, 0.2, 0], color=WHITE, stroke_width=4), label(nm, font_size=30, color=WHITE).move_to([x, 0.55, 0]))
        frame.move_to(UP * 2.3)
        spans = VGroup(label(r"a fourth", font_size=24, color=TUNE).move_to(frame.get_center() + LEFT * 2.9 + DOWN * 0.5), label(r"a tone", font_size=24, color=GREY_B).move_to(frame.get_center() + DOWN * 0.5),
                       label(r"a fourth", font_size=24, color=TUNE).move_to(frame.get_center() + RIGHT * 2.9 + DOWN * 0.5))
        fills = VGroup(*[VGroup(half(t, width=2.6), label(" + ".join(str(x) for x in t), font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2) for t in d["tetrachords"]])
        fills.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.5)).move_to(DOWN * 1.2)
        with self.voiceover(
            "Before keyboards, and long before anyone drew a circle of twelve notes, scales were built in "
            "another way, by the Greeks and by nearly every tradition that learned from them. Fix the "
            "strong notes first: the home note, the fourth above it, the fifth, and the octave. "
            "<bookmark mark='a'/> That leaves two fourths to fill, with a whole tone between them. Fill "
            "each fourth with two more notes, and you have a scale of seven. A filled fourth is called a "
            "tetrachord: four strings. <bookmark mark='b'/> On our twelve notes a fourth is five "
            "semitones, and there are exactly six ways to cut five into three steps."
        ) as vo:
            self.play(FadeIn(frame))
            vo.wait_until("a")
            self.play(FadeIn(spans))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in fills], lag_ratio=0.3), run_time=3.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two(self):
        d = load("halves")
        c = clip("halves.two")
        rows = VGroup()
        for name, lo, hi in ((r"major", [2, 2, 1], [2, 2, 1]), (r"two halves of another kind", [1, 3, 1], [1, 3, 1])):
            bar = VGroup(half(lo, 3.0), step_bar([2], width=1.2, height=0.5, colors=(GREY_C,), fmt="{:.0f}", font_size=22), half(hi, 3.0)).arrange(RIGHT, buff=0.06)
            rows.add(VGroup(label(name, font_size=28, color=TUNE), bar).arrange(DOWN, buff=0.25))
        rows.arrange(DOWN, buff=0.9).move_to(UP * 0.4)
        note = listen_note(r"the lower half of a major scale; \ the upper half; \ the two joined. \ Then a scale made of two other halves", width=10.4, font_size=26).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The major scale is two tetrachords of the same shape, tone, tone, semitone, with a tone "
            "between. Sing the lower half and then the upper: they are the same four-note tune, a fifth "
            "apart. <bookmark mark='a'/> Use a different filling, semitone, three semitones, semitone, "
            "for both halves, and you get a scale that the major-minor system has no place for, but that "
            "is everyday in Arabic, Turkish, Greek and Indian music."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(note))
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"halves, \ and wholes", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            s = d["starts"]
            pulse(snd, rows[0][1][0], s[0], s[0] + 1.5, buff=0.08)
            pulse(snd, rows[0][1][2], s[1], s[1] + 1.5, buff=0.08)
            pulse(snd, rows[0][1], s[2], s[2] + 2.9, buff=0.12)
            pulse(snd, rows[1][1], s[3], s[3] + 2.9, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seventy_two(self):
        d = load("halves")
        eq = MathTex(r"2 \;\times\; 6 \;\times\; 6 \;=\; 72", font_size=64).move_to(UP * 1.5)
        under = VGroup(label(r"the fourth: \\ plain or raised", font_size=24, color=GREY_A), label(r"the second and third: \\ any two of four places", font_size=24, color=GREY_A),
                       label(r"the sixth and seventh: \\ any two of four places", font_size=24, color=GREY_A))
        under.arrange(RIGHT, buff=0.9).move_to(UP * 0.2)
        rule = label(r"Venkatamakhin's rule, \ seventeenth century", font_size=30, color=TUNE).to_edge(UP, buff=0.5)
        eq.move_to(UP * 1.6)
        maya = twelve(d["maya"], radius=1.2, color=TUNE, font_size=16).move_to(LEFT * 3.4 + DOWN * 2.0)
        ml = label(r"number 15 of the 72: \\ Mayamalavagowla, \\ the first scale a student in south India learns", font_size=24, color=GREY_A).next_to(maya, RIGHT, buff=0.6)
        with self.voiceover(
            "South Indian music made a complete catalogue out of this idea. In the seventeenth century "
            "the theorist Venkatamakhin laid down a rule. The home note and the fifth are fixed. "
            "<bookmark mark='a'/> The fourth is either plain or raised: two choices. The second and "
            "third notes take any two of the four places below the fourth: six choices. The sixth and "
            "seventh take any two of the four places above the fifth: six more. <bookmark mark='b'/> "
            "Two times six times six: seventy-two parent scales, the melakartas, each with a name and a "
            "number, and every raga of the tradition is assigned to one of them. Monochord generates all "
            f"seventy-two, and finds {say(d['modes_among'])} of our seven modes among them. "
            "<bookmark mark='c'/> Here is one that is not: the first scale a student in south India "
            "learns. You just heard it. It is the scale of two halves from a moment ago."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in under], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(maya), FadeIn(ml))
        self.wait(0.4)
        self.clear_scene()
