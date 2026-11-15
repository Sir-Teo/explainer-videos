from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Brain(SoundScene):
    def construct(self):
        chapter(self, 6, r"The brain at a wrong chord", r"Does the brain parse harmony like grammar?")
        self.eran()
        self.neap()
        self.syntax()
        self.mmn()
        self.reward()

    # ------------------------------------------------------------------
    def eran(self):
        items = [
            (r"Stefan Koelsch and colleagues \ (2000): \ chord sequences ending on a tonic or on a Neapolitan sixth", WHITE),
            (r"the unexpected chord evoked an `early right anterior negativity' \ (ERAN) \ about 200 ms after it, \ in non-musicians too", WHITE),
            (r"its size tracks how improbable the chord is in the style", WHITE),
            (r"the brain predicts chords automatically, \ even while attending to something else", TUNE),
            (r"Part 19's Neapolitan, \ seen in an EEG", GREY_A),
        ]
        rows_scene(self, r"a response to an unexpected chord", items,
                   "What does the brain do at a wrong chord? <bookmark mark='b'/> In 2000 Stefan Koelsch and colleagues played "
                   "chord sequences ending either on the tonic or on a Neapolitan sixth. <bookmark mark='c'/> The unexpected "
                   "chord evoked a brain response about two hundred milliseconds later, the early right anterior negativity, in "
                   "non-musicians too, <bookmark mark='d'/> and its size tracks how improbable the chord is in the style. "
                   "<bookmark mark='e'/> The brain predicts chords automatically, even while attending to something else. "
                   "<bookmark mark='f'/> It is Part 19's Neapolitan, seen in an EEG.", marks="bcdef")

    # ------------------------------------------------------------------
    def syntax(self):
        items = [
            (r"Aniruddh Patel and colleagues \ (1998): \ out-of-key chords and ungrammatical words evoke similar late responses \ (the P600)", WHITE),
            (r"Patel's hypothesis: \ music and language share resources for integrating structure, \ not the structures themselves", WHITE),
            (r"some studies find interference: \ a harmonic surprise slows the reading of a hard sentence", WHITE),
            (r"the overlap is real but partial; \ amusia and aphasia can occur without each other", TUNE),
            (r"Part 47 returns to music and language", GREY_A),
        ]
        rows_scene(self, r"music and language", items,
                   "Is this like grammar? <bookmark mark='b'/> In 1998 Aniruddh Patel and colleagues found that out-of-key chords "
                   "and ungrammatical words evoke similar late brain responses. <bookmark mark='c'/> Patel proposed that music and "
                   "language share resources for integrating structure, but not the structures themselves. "
                   "<bookmark mark='d'/> Some studies find interference: a harmonic surprise slows the reading of a difficult "
                   "sentence. <bookmark mark='e'/> The overlap is real but partial: amusia and aphasia can each occur without the "
                   "other. <bookmark mark='f'/> Part 47 returns to music and language.", marks="bcdef")

    # ------------------------------------------------------------------
    def reward(self):
        items = [
            (r"pleasurable music engages the brain's reward circuits, \ as food and money do", WHITE),
            (r"Ferreri and colleagues \ (2019): \ a drug that raises dopamine increased musical pleasure; \ one that blocks it reduced it", WHITE),
            (r"musical anhedonia: \ a few per cent of people feel little reward from music, \ though they enjoy other things", WHITE),
            (r"the reward follows prediction: \ the wanting and the getting of the hook's chills", TUNE),
            (r"chapter 7: \ surprise and uncertainty together", GREY_A),
        ]
        rows_scene(self, r"reward", items,
                   "And reward. <bookmark mark='b'/> Pleasurable music engages the brain's reward circuits, as food and money do. "
                   "<bookmark mark='c'/> In 2019 Laura Ferreri and colleagues showed that a drug raising dopamine increased "
                   "musical pleasure, and one blocking it reduced it. <bookmark mark='d'/> A few per cent of people have musical "
                   "anhedonia: they feel little reward from music, though they enjoy other things. <bookmark mark='e'/> The reward "
                   "follows prediction: the wanting and the getting of the hook's chills. <bookmark mark='f'/> Chapter seven puts "
                   "surprise and uncertainty together.", marks="bcdef")

    # ------------------------------------------------------------------
    def neap(self):
        d = load("neap")
        c = clip("neap.two")
        cells = VGroup(label(r"I \ IV \ I$^6_4$ \ V \ I", font_size=24, color=TUNE), label(r"I \ IV \ I$^6_4$ \ V \ N$^6$", font_size=24, color=EAR)).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"the stimulus, \ in the manner of Koelsch's", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("Hear a sequence like Koelsch's: five chords ending on the tonic, then the same ending on a Neapolitan sixth."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"tonic, \ then Neapolitan", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["tonic"], st["neapolitan"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["neapolitan"], c.duration, buff=0.1)
        with self.voiceover(
            "The last chord of the second sequence is in tune and consonant; only its place is wrong. That is enough for "
            "the brain to flag it within a fifth of a second."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mmn(self):
        items = [
            (r"the mismatch negativity: \ a brain response to a deviant in a regular sequence, \ about 150 ms after it", WHITE),
            (r"it appears without attention, \ even in sleep and in newborns", WHITE),
            (r"musicians show larger mismatch responses to small pitch and timing deviations", WHITE),
            (r"prediction runs automatically, \ at every level from the brainstem to harmony", TUNE),
            (r"Part 4's ear, \ predicting", GREY_A),
        ]
        rows_scene(self, r"automatic prediction", items,
                   "Prediction goes deeper than harmony. <bookmark mark='b'/> The mismatch negativity is a brain response to a "
                   "deviant sound in a regular sequence, about a hundred and fifty milliseconds after it. <bookmark mark='c'/> It "
                   "appears without attention, even in sleep and in newborns. <bookmark mark='d'/> Musicians show larger mismatch "
                   "responses to small deviations of pitch and timing. <bookmark mark='e'/> Prediction runs automatically, at every "
                   "level from the brainstem to harmony: <bookmark mark='f'/> Part 4's ear, predicting.", marks="bcdef")
