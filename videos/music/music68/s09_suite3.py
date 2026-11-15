from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class SuiteThree(SoundScene):
    def construct(self):
        chapter(self, 8, r"The suite, \ III: \ the mind, \ the studio, \ the machines", r"What did the Tune become in Acts VIII to XII?")
        self.before()
        self.movement()
        self.after()
        self.clear_scene()

    def movement(self):
        b = movement_board("three", r"III")
        self.play(FadeIn(b.head), FadeIn(b.cells), FadeIn(b.tags))
        c = clip("suite.three")
        with self.listen(c) as snd:
            window(snd, r"the suite, \ III", kind=c.meta.get("label", "synthesized"), detail=b.detail, corner=DL, tag_corner=DR)
            drive_movement(snd, b, c.duration)
        self.wait(0.3)

    def before(self):
        note = listen_note(r"Twenty-three: \ the Tune hidden and found, \ three endings, \ thirty singers; \ "
                           r"bits, \ rooms, \ tuning, \ synthesizers, \ a tracker; \ microphones, \ a mix, \ a master, \ a codec, \ an arena; \ "
                           r"then the machines that listen and write, \ and an edition.", width=10.6)
        with self.voiceover(
            "The third movement: Acts Eight to Twelve, twenty-three Variations. The mind: the Tune hidden in another line, "
            "three endings, a chain of thirty simulated singers. Electric sound: bits and dither, rooms and plates, hard-tuned "
            "voices, synthesizers, a tracker. The studio: microphones, a mix, a master, a codec, an arena. And then the machines "
            "that listen and write, and last the critical edition of Part 67. Here the instruments are mostly not new: the "
            "Tune is carried by what earlier parts built, and changed by what happens to sound after it is made."
        ):
            self.play(FadeIn(note))
        self.wait(0.5)
        self.play(FadeOut(note))

    def after(self):
        with self.voiceover(
            "That is all sixty-seven, about ten minutes of music made by sixty-seven parts. One Variation is missing: this "
            "part's own. It is the suite you have just heard."
        ):
            self.wait(0.2)
