from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class SuiteOne(SoundScene):
    def construct(self):
        chapter(self, 6, r"The suite, \ I: \ Sound, \ Notes and Voices", r"What did the Tune become in Acts I to III?")
        self.before()
        self.movement()
        self.after()
        self.clear_scene()

    def movement(self):
        b = movement_board("one", r"I")
        self.play(FadeIn(b.head), FadeIn(b.cells), FadeIn(b.tags))
        c = clip("suite.one")
        with self.listen(c) as snd:
            window(snd, r"the suite, \ I", kind=c.meta.get("label", "synthesized"), detail=b.detail, corner=DL, tag_corner=DR)
            drive_movement(snd, b, c.duration)
        self.wait(0.3)

    def before(self):
        note = listen_note(r"Twenty-two Variations, \ eight and a half seconds each, \ in the order they were made. \ "
                           r"First the sound itself changes: \ a string, \ bottles, \ pure tones, \ missing fundamentals, \ tunings, \ "
                           r"the instruments. \ Then the Tune gains a written form, \ a meter, \ modes, \ chords, \ voices, \ a form.", width=10.6)
        with self.voiceover(
            "The first movement: Acts One to Three, twenty-two Variations, eight and a half seconds of each, in the order they "
            "were made, each from its first sound and brought to the same loudness. Listen first for the sound itself "
            "changing: a string, bottles of water, pure tones added one by one, a Tune whose fundamentals are missing, chords "
            "in eight tunings, then the instruments family by family. Then the Tune is written down, and gains a meter, modes, "
            "chords, voices, a canon and a form."
        ):
            self.play(FadeIn(note))
        self.wait(0.5)
        self.play(FadeOut(note))

    def after(self):
        with self.voiceover(
            "That was the foundation: what a musical sound is, and how sounds became notes and notes became voices. Every "
            "later Variation stands on these twenty-two."
        ):
            self.wait(0.2)
