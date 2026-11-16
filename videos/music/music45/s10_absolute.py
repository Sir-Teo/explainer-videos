from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Absolute(SoundScene):
    def construct(self):
        chapter(self, 9, r"Absolute pitch and pitch memory", r"Can you name a note without a reference?")
        self.ap()
        self.memory_trial()
        self.memory()
        self.relative()
        self.tone()

    # ------------------------------------------------------------------
    def ap(self):
        items = [
            (r"absolute pitch: \ naming a note, \ or singing one, \ with no reference tone", WHITE),
            (r"prevalence depends on definition and sample; \\ often associated with early musical training", WHITE),
            (r"Deutsch and colleagues \ (2006): \ far more common among students who speak a tone language and trained early", WHITE),
            (r"early training and a critical period matter; \ genes probably do too", TUNE),
            (r"it is a labelling skill: \ possessors still hear melody by its intervals", GREY_A),
        ]
        rows_scene(self, r"absolute pitch", items,
                   "Some people can name a note with no reference tone at all. <bookmark mark='b'/> Population prevalence is uncertain and depends on the definition and sample; absolute pitch is uncommon in many Western unselected samples, and more common among musicians who began very early. <bookmark mark='c'/> Diana Deutsch and colleagues found in 2006 that it was far more common among conservatory students who spoke a tone language, such as Mandarin, and had trained early. <bookmark mark='d'/> Early training and a critical period matter, and genes probably do too. <bookmark mark='e'/> It is a labelling skill: possessors still hear a melody by its intervals.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def memory(self):
        items = [
            (r"Daniel Levitin \ (1994): \ people without absolute pitch sang familiar pop songs from memory", WHITE),
            (r"many reproduced a familiar recording's pitch within one or two semitones", WHITE),
            (r"Levitin and Cook \ (1996): \ familiar recordings can also support useful tempo memory", WHITE),
            (r"ordinary listeners keep absolute pitch and tempo for music they know well; \ they lack only the labels", TUNE),
            (r"the Tune is remembered in whatever key it was learned", GREY_A),
        ]
        rows_scene(self, r"everyday pitch memory", items,
                   "Everyone else remembers more than they think. <bookmark mark='b'/> In 1994 Daniel Levitin asked people without absolute pitch to sing familiar pop songs from memory, and many reproduced the recording's pitch within one or two semitones. <bookmark mark='c'/> With Perry Cook he showed in 1996 that familiar recordings can also support useful tempo memory. <bookmark mark='d'/> Many listeners retain useful pitch and tempo information for familiar recordings, without necessarily having precise note labels or uniformly accurate recall. <bookmark mark='e'/> A familiar tune's remembered key can reflect particular recordings and exposure; not everyone recalls its first-learned key.", marks="bcde")

    # ------------------------------------------------------------------
    def relative(self):
        items = [
            (r"relative pitch: \ hearing intervals and scale degrees, \ whatever the key \ (Part 15)", WHITE),
            (r"it is what melodies need: \ the Tune is the Tune in any key", WHITE),
            (r"infants already recognise a melody transposed; \ adults remember contour first, \ exact intervals later \ (Part 14)", WHITE),
            (r"musical training is mostly training relative pitch", TUNE),
            (r"and language shapes pitch too", GREY_A),
        ]
        rows_scene(self, r"relative pitch", items,
                   "Music mostly needs something else. <bookmark mark='b'/> Relative pitch, hearing intervals and scale degrees "
                   "whatever the key, as in Part 15, is what melodies need: the Tune is the Tune in any key. "
                   "<bookmark mark='c'/> Infants already recognise a melody transposed, and adults remember contour first and "
                   "exact intervals later, as Part 14 found. <bookmark mark='d'/> Musical training is mostly training relative "
                   "pitch. <bookmark mark='e'/> And language shapes pitch too.", marks="bcde")

    # ------------------------------------------------------------------
    def memory_trial(self):
        d = load("memory")
        c = clip("memory.two")
        cells = VGroup(*[VGroup(RoundedRectangle(width=4.2, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t in (r"trial 1: \ same or different?", r"trial 2: \ same or different?")]).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
        head = label(r"how well do you hold a pitch?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Try holding a pitch yourself. In each trial you will hear a tone, then six other tones, then a last tone. Is the "
            "last one the same as the first, or different?"
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two trials", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["first"], st["second"] - 0.4, buff=0.1)
            pulse(snd, cells[1], st["second"], c.duration, buff=0.1)
        ans = label(r"trial 1: \ the same; \ trial 2: \ a semitone higher", font_size=22, color=TUNE).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "The first was the same; the second was a semitone higher. Diana Deutsch showed in 1970 that the tones in between "
            "are what make this hard: a comparable silent delay often interferes less, six intervening tones disturb it, "
            "most of all when one of them is close in pitch to the tone being held. Pitch memory is fragile, and it is "
            "disturbed by other pitches."
        ):
            self.play(FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tone(self):
        items = [
            (r"in tone languages \ (Mandarin, \ Cantonese, \ Yoruba, \ Vietnamese), \ pitch changes the meaning of a word", WHITE),
            (r"speakers track pitch contours every day, \ and some musical pitch skills come easier", WHITE),
            (r"brainstem responses follow pitch more faithfully in both musicians and tone-language speakers", WHITE),
            (r"but tone languages do not make music easier in every way: \ contours, \ not intervals, \ carry the meaning", TUNE),
            (r"chapter 10: \ machines that hear scenes; \ Part 47: \ what music and language share", GREY_A),
        ]
        rows_scene(self, r"pitch in language", items,
                   "Language shapes pitch too. <bookmark mark='b'/> In tone languages, Mandarin, Cantonese, Yoruba, Vietnamese, "
                   "pitch changes the meaning of a word, <bookmark mark='c'/> so speakers track pitch contours every day, and some "
                   "musical pitch skills come easier. <bookmark mark='d'/> Brainstem responses follow pitch more faithfully in both "
                   "musicians and tone-language speakers. <bookmark mark='e'/> But tone languages do not make music easier in "
                   "every way: in speech, contours carry the meaning, not exact intervals. <bookmark mark='f'/> Chapter ten turns "
                   "to machines that hear scenes, and Part 47 asks what music and language share.", marks="bcdef")
