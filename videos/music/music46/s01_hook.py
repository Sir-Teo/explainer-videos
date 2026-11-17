from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.chills()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"The Tune's last phrase, \ three times, \ each with a different last note. \ "
                           r"A model listener trained on fifty tunes heard them too. \ Which ending surprised it most, \ and which least?", width=10.4)
        with self.voiceover(
            "In 1956 Leonard Meyer argued that musical emotion is expectation, delayed and fulfilled. Test your own expectations first. The Tune's last phrase, three times, each with a different last note. A model "
            "listener, trained on fifty other tunes, heard them too. Which ending surprised it most, and which least?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.85)
                         for t in (r"first", r"second", r"third")]).arrange(RIGHT, buff=0.9).move_to(UP * 1.1)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        order = d["order"]
        with self.listen(c) as snd:
            window(snd, r"three endings", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, k in enumerate(order):
                end = st[order[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        ics = d["ics"]
        names = {"A": r"A, \ over A minor", "C": r"C, \ over C", "F sharp": r"F$\sharp$, \ over D"}
        bars = VGroup()
        for i, k in enumerate(order):
            h = 0.22 * ics[k]
            bars.add(VGroup(Rectangle(width=1.2, height=h, stroke_width=0, fill_color=EAR, fill_opacity=0.85),
                            label(rf"{ics[k]:.1f} bits", font_size=18, color=WHITE), label(names[k], font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12))
        for b, box in zip(bars, boxes):
            b.next_to(box, DOWN, buff=0.35).align_to(box, ORIGIN)
            b.set_x(box.get_x())
        with self.voiceover(
            f"Most surprising: the third, ending on F sharp, at {say(ics['F sharp'], 1)} bits. Least: the second, the "
            f"real ending on C, at {say(ics['C'], 1)}. The first, on A, sat between, at {say(ics['A'], 1)}. A bit is a "
            "yes-or-no question: the scores describe minus log probabilities, not literal counts of guesses or exact code lengths for each note. This part is about "
            "those numbers, and why they might have anything to do with feeling."
        ):
            self.play(FadeIn(bars))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chills(self):
        items = [
            (r"Valorie Salimpoor and colleagues \ (2011): \ listeners brought their own music that gave them chills", WHITE),
            (r"PET: striatal dopamine release; \\ fMRI: distinct anticipation and peak-related activity", WHITE),
            (r"the anticipation lit the caudate; \ the peak, \ the nucleus accumbens", WHITE),
            (r"pleasure in music has a phase of wanting before a phase of getting", TUNE),
            (r"Leonard Meyer had argued in 1956 that musical emotion is expectation, \ delayed and fulfilled", GREY_A),
        ]
        rows_scene(self, r"chills, \ and before them", items,
                   "In 2011 Valorie Salimpoor and colleagues asked listeners to bring music that gave them chills. <bookmark mark='b'/> PET provided evidence of striatal dopamine release during intensely pleasurable music, while fMRI distinguished anticipatory and peak-related activity. <bookmark mark='c'/> Anticipation was associated more with caudate activity, and peak pleasure with nucleus accumbens activity; these methods do not directly time two separate dopamine pulses. <bookmark mark='d'/> Pleasure in music has a phase of wanting before a phase of getting. <bookmark mark='e'/> Leonard Meyer had argued as much in 1956: musical emotion is expectation, delayed and fulfilled.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"Meyer, \ Huron, \ and expectation as prediction",
            r"statistical learning: \ how expectations are acquired",
            r"a listener model: \ surprise and uncertainty, \ note by note",
            r"three endings for the Tune: \ expected, \ delayed, \ denied",
            r"the brain, \ groove, \ and the cues of expressed emotion",
            r"sad music, \ preference, \ and what does not replicate",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Meyer, Huron, and expectation as prediction. <bookmark mark='b'/> Statistical learning: how "
            "expectations are acquired. <bookmark mark='c'/> A listener model that measures surprise and uncertainty note "
            "by note. <bookmark mark='d'/> Three endings for the Tune: expected, delayed and denied. <bookmark mark='e'/> The "
            "brain, groove, and the cues of expressed emotion. <bookmark mark='f'/> And sad music, preference, and what does "
            "not replicate."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
