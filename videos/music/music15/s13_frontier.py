from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ is a key learned?", r"Where do keys come from, \ and are they everywhere?", spoken="Frontier: is a key learned?")
        self.elsewhere()
        self.history()
        self.open()

    # ------------------------------------------------------------------
    def elsewhere(self):
        rows = VGroup(label(r"north India, \ 1984: \ ratings follow the raga's own notes, \ in newcomers too", font_size=26, color=WHITE),
                      label(r"Bali, \ 1984: \ villagers and American students, \ on each other's scales", font_size=26, color=WHITE),
                      label(r"Sami yoiks, \ 2000: \ Western listeners expect by their own habits; \ Sami listeners do not", font_size=26, color=WHITE),
                      label(r"a hierarchy of notes seems to be everywhere. \ Which hierarchy is learned.", font_size=30, color=TUNE)).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "Is the key a fact about music, or about European music? The probe-tone experiment has been "
            "taken round the world. <bookmark mark='a'/> In north Indian music, as we saw, listeners' "
            "ratings follow the notes of the raga. <bookmark mark='b'/> In Bali, in 1984, Edward "
            "Kessler, Christa Hansen and Roger Shepard tested villagers and American students on "
            "Western and Balinese scales, and each group heard the other's music partly through its "
            "own. <bookmark mark='c'/> In 2000 Krumhansl and Finnish colleagues tested expectations for "
            "Sami yoiks, a style with large leaps: Western listeners expected by Western habits, and "
            "Sami listeners did not. <bookmark mark='d'/> So the general finding is this. Some notes "
            "being more central than others seems to be nearly universal. Which notes, and in what "
            "order, is learned from what a listener hears."
        ) as vo:
            head = label(r"the probe-tone experiment, \ around the world", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        g = axes([1400, 1760], [0, 1.1], x_length=9.0, y_length=2.6, xlabel=r"year of composition", ylabel=r"how well the best major or minor profile fits \ (a sketch of the finding)", xticks=[1400, 1500, 1600, 1700, 1750], font_size=20).move_to(DOWN * 0.9)
        xs = np.linspace(1400, 1750, 60)
        ys = 0.45 + 0.5 / (1 + np.exp(-(xs - 1620) / 28))
        cv = curve_from(g, xs, ys, TUNE, stroke_width=4)
        head = label(r"when did major and minor begin?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"J. Albrecht and D. Huron \ (2014): \ note counts in music from 1400 to 1750", font_size=22, color=GREY_B).next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "If keys are learned from music, then they have a history, and it can be read from scores. "
            "In 2014 Joshua Albrecht and David Huron counted the notes in hundreds of pieces written "
            "between 1400 and 1750, fifty years at a time. <bookmark mark='a'/> The early music is "
            "spread over several modes, each with its own profile. Through the seventeenth century the "
            "profiles gather into two, and by 1700 they are the major and minor profiles of this part. "
            "Tonality was not invented. It condensed, over about a hundred years, and the listeners' "
            "ratings of 1982 are a fossil of that process."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cv), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"is ``key'' one thing?", font_size=34, color=WHITE),
                      label(r"rock and pop: \ IV as common as V; \ the flat seventh; \ songs that end away from home", font_size=24, color=GREY_A),
                      label(r"key finders tuned on classical music lose their way; \ listeners can disagree about home", font_size=24, color=GREY_A),
                      label(r"what does a listener learn: \ a profile, \ a grammar of chords, \ or both?", font_size=28, color=TUNE)).arrange(DOWN, buff=0.28).move_to(UP * 0.2)
        with self.voiceover(
            "And it has not stopped changing. <bookmark mark='a'/> In rock and pop, as Trevor de Clercq "
            "and David Temperley showed from a corpus of a hundred songs, the chord on four is as "
            "common as the chord on five, the flattened seventh is everywhere, and the progression five "
            "to four, rare in Mozart, is ordinary. <bookmark mark='b'/> Key finders tuned on classical "
            "music lose their way in it, and for a song that loops four chords, which of them is home "
            "can be a matter of opinion. <bookmark mark='c'/> So the open question is what exactly a "
            "listener learns. A profile of twelve numbers explains a great deal: this whole part. But "
            "it has no order in it, and chapter three showed that order matters. Whether a key is "
            "stored as counts of notes, as a grammar of chords, or as both, is not settled."
        ) as vo:
            self.play(FadeIn(star[0]), FadeIn(star[1]))
            vo.wait_until("a")
            self.play(FadeIn(star[2]))
            vo.wait_until("b")
            self.play(FadeIn(star[3]))
            vo.wait_until("c")
            self.play(FadeIn(star[4]))
        self.wait(0.4)
        self.clear_scene()
