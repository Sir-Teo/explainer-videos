from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class SuiteTwo(SoundScene):
    def construct(self):
        chapter(self, 7, r"The suite, \ II: \ a thousand years, \ many musics, \ the craft", r"What did the Tune become in Acts IV to VII?")
        self.before()
        self.movement()
        self.after()
        self.clear_scene()

    def movement(self):
        b = movement_board("two", r"II")
        self.play(FadeIn(b.head), FadeIn(b.cells), FadeIn(b.tags))
        c = clip("suite.two")
        with self.listen(c) as snd:
            window(snd, r"the suite, \ II", kind=c.meta.get("label", "synthesized"), detail=b.detail, corner=DL, tag_corner=DR)
            drive_movement(snd, b, c.duration)
        self.wait(0.3)

    def before(self):
        note = listen_note(r"Twenty-two more: \ chant to Romantic Lied, \ then whole-tone, \ twelve-tone and phasing; \ "
                           r"Bilawal, \ Rast, \ the qin, \ an inherent pattern, \ a blues, \ bebop and a pop single; \ "
                           r"then orchestrated, \ composed by a searcher, \ performed.", width=10.6)
        with self.voiceover(
            "The second movement: Acts Four to Seven. First a thousand years of European style in five steps, from chant to a "
            "Romantic song. Then what is left after tonality: whole-tone planing, a twelve-tone row, the Tune phased against "
            "itself, paths on the Tonnetz. Then the world's other answers: a raga, three maqamat, the qin and the gamelan, an "
            "interlocking pattern, the blues, bebop and a pop single. And last the craft: orchestrated, composed by a search, "
            "and performed."
        ):
            self.play(FadeIn(note))
        self.wait(0.5)
        self.play(FadeOut(note))

    def after(self):
        with self.voiceover(
            "Through most of that movement the Tune's opening was there to be found, though some Variations, like the "
            "twelve-tone row, bury it on purpose. A melody survives modes, meters, tunings and whole "
            "traditions remarkably well, which is one reason the series could carry one tune through sixty-seven parts."
        ):
            self.wait(0.2)
