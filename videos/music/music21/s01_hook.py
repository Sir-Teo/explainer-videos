from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.speech()
        self.repeat()
        self.plan()

    # ------------------------------------------------------------------
    def speech(self):
        d = load("hook")
        c = clip("hook.speech")
        card = history_card(1995, r"San Diego: \ Diana Deutsch", r"editing a recording of her own voice, \ she loops one phrase, \ and it begins to sing", width=10.4, font_size=26).to_edge(UP, buff=0.4)
        note = listen_note(r"A spoken phrase, \ ten times. \ Listen for the moment it stops being speech.", width=9.0).move_to(DOWN * 0.2)
        with self.voiceover(
            "In the mid-1990s the psychologist Diana Deutsch was checking a recording of her own voice, and left one "
            "phrase looping. After a few repetitions it was no longer speaking. It was singing. "
            "<bookmark mark='a'/> Here is a phrase spoken by this series' narrator, repeated ten times. Listen for the "
            "moment it stops being speech."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(note))
        self.play(FadeOut(note))
        dots = VGroup(*[Circle(radius=0.28, stroke_color=GREY_B, stroke_width=2) for _ in range(d["repeats"])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        words = label(rf"``{d['phrase']}''", font_size=34, color=WHITE).next_to(dots, UP, buff=0.6)
        self.play(FadeIn(dots), FadeIn(words))
        with self.listen(c) as snd:
            window(snd, r"one phrase, \ ten times", kind="synthesized", detail=r"the narrator's voice", corner=DL, tag_corner=DR)
            flash(snd, list(dots), [d["seconds_each"] * k for k in range(d["repeats"])], hot=TUNE, base=GREY_B, hold=d["seconds_each"] * 0.6)
            pulse(snd, words, 0.0, c.duration, buff=0.15)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def repeat(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"most listeners hear the words begin to sing after a few repetitions", WHITE),
            (r"heard again in its sentence, \ the phrase still sings", WHITE),
            (r"Deutsch, \ 2011: \ repetition alone, \ exact repetition, \ turns speech to song", TUNE),
            (r"music repeats far more than speech, \ poetry or prose", WHITE),
            (r"form is the plan of what comes back", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the speech-to-song illusion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Repeated speech can begin to sound songlike for some listeners; this synthesized example may vary in effectiveness: the syllables take on pitches, a rhythm, a tune. <bookmark mark='a'/> The altered percept can persist, even when you hear it again inside its original sentence. <bookmark mark='b'/> In 2011 Deutsch and her colleagues showed that repetition alone does it: when the repeats were changed slightly, transposed or jumbled, the effect weakened. <bookmark mark='c'/> Repetition is one important cue to musical organization. Repetition is prominent in many musical traditions, as it also is in some speech and poetry, and this part will measure how much. <bookmark mark='d'/> Form is the plan of what comes back, and when."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 21: \ Form", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=27, color=c_) for t, c_ in (
            (r"the small forms: \ phrase, \ period and sentence", WHITE),
            (r"the large ones: \ binary, \ ternary, \ rondo, \ variation, \ sonata, \ song", WHITE),
            (r"a picture of repetition: \ the self-similarity matrix", EAR),
            (r"a program that finds the sections from the sound alone", WHITE),
            (r"how much music repeats; \ the golden section, \ tested", WHITE),
            (r"and whether listeners hear form at all", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part goes from the small forms to the large. <bookmark mark='a'/> First the phrase, the period and "
            "the sentence. <bookmark mark='b'/> Then the forms of whole pieces: binary and ternary, rondo, variation, "
            "sonata, and the forms of songs. <bookmark mark='c'/> Along the way it builds a picture in which repetition "
            "can be seen, <bookmark mark='d'/> and a program that finds a piece's sections from its sound alone. "
            "<bookmark mark='e'/> It measures how much music repeats, and tests a famous claim about proportion. "
            "<bookmark mark='f'/> And it ends with the hardest question: does a listener actually hear form?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
