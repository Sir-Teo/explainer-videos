from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ counterpoint by machine", r"Can rules write music, \ and can music test the rules?", extra=((1984, r"Schottstaedt's species program"),),
                spoken="Frontier: counterpoint by machine")
        self.machines()
        self.tests()
        self.open()

    def machines(self):
        rows = VGroup(label(r"1984: \ Bill Schottstaedt, \ Stanford: \ all five species, \ up to six voices", font_size=26, color=WHITE),
                      label(r"most rules as penalties, \ not prohibitions: \ Fux says most are guidelines", font_size=24, color=GREY_A),
                      label(r"1988: \ Kemal Ebcio\u{g}lu: \ Bach-style chorales from about 350 rules", font_size=26, color=WHITE),
                      label(r"today: \ constraint solvers formalize Fux exactly; \ neural networks learn from Bach", font_size=26, color=WHITE),
                      label(r"this part: \ counting by dynamic programming, \ sampling, \ search", font_size=26, color=TUNE)).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(UP * 0.1)
        head = label(r"counterpoint as constraint satisfaction", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Rules this exact are an invitation to a computer. <bookmark mark='a'/> In 1984 Bill "
            "Schottstaedt, at Stanford, wrote a program that worked all five of Fux's species in up to "
            "six voices. <bookmark mark='b'/> He gave most of the rules penalties rather than making "
            "them prohibitions, which is closer to Fux, who calls many of his rules advice. "
            "<bookmark mark='c'/> In 1988 Kemal Ebcioglu harmonized chorales "
            "in the style of Bach with a system of about three hundred and fifty rules. "
            "<bookmark mark='d'/> Today counterpoint is a standard test for constraint solvers, and "
            "neural networks are trained on Bach's chorales to write more. <bookmark mark='e'/> What "
            "this part did is the simplest version: count, sample and search."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    def tests(self):
        rows = VGroup(label(r"if the rules come from hearing, \ composers who never read Fux should obey them too", font_size=26, color=WHITE),
                      label(r"Huron: \ in polyphonic music, \ fused intervals are approached apart in time more than chance allows", font_size=24, color=GREY_A),
                      label(r"and in music meant as one voice, \ in harmony, \ the rules relax", font_size=24, color=GREY_A),
                      label(r"the test: \ shuffle the music, \ count again: \ the method of Part 14", font_size=28, color=TUNE)).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        head = label(r"can music test the rules?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The perceptual account also makes predictions that can be checked against music. "
            "<bookmark mark='a'/> If the rules come from hearing, then composers who never read Fux "
            "should obey them anyway, wherever they want independent voices. <bookmark mark='b'/> "
            "Huron's corpus studies found exactly that: fused intervals are approached with offset "
            "onsets, and by contrary motion, more than chance would give. <bookmark mark='c'/> And where "
            "the goal is a single thick voice, as in a hymn's chords moving together or a horn section "
            "in parallel, the rules relax. <bookmark mark='d'/> The method is the one Part 14 used for "
            "the leap rule: shuffle the music, count again, and see what is left over."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"the rules say what to avoid. \ What makes one good line better than another?", font_size=28, color=WHITE),
                      label(rf"over Fux's cantus there are {load('counting')['valid']} lines that obey every rule; \ teachers would not grade them equally", font_size=24, color=GREY_A),
                      label(r"no model yet ranks them as a good teacher would", font_size=28, color=TUNE)).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        with self.voiceover(
            "What remains open is the other half of the craft. The rules say what to avoid. They say "
            f"nothing about what to prefer. There are {say(load('counting')['valid'])} lines over "
            "Fux's cantus that break no rule, and a teacher would not grade them equally: some have a "
            "shape, a climax in the right place, a sense of going somewhere; others merely comply. "
            "Monochord's preference for contrary motion is a crude guess at that judgement. Whether a "
            "model can rank good lines as a good teacher does, and from what it would have to learn, "
            "is not settled."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in star], lag_ratio=0.5), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
