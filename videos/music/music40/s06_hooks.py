from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403

WEIGHT = [4, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0]


class Hooks(SoundScene):
    def construct(self):
        chapter(self, 5, r"Hooks and prosody", r"What makes a line stick, \ and words sit right?")
        self.hooks()
        self.prosody()
        self.lab_()
        self.title()
        self.earworms()

    # ------------------------------------------------------------------
    def hooks(self):
        items = [
            (r"a hook: \ the part of a song built to be remembered, \ often the chorus and its title", WHITE),
            (r"melodic hooks, \ rhythmic hooks, \ a sound \ (a riff, \ a vocal effect), \ a lyric", WHITE),
            (r"repetition is the main tool: \ the chorus returns, \ and repeats within itself", WHITE),
            (r"Part 14's melodies again: \ small range, \ steps, \ one leap that stands out", TUNE),
            (r"and the words must sit on the music the way they are spoken", GREY_A),
        ]
        rows_scene(self, r"hooks", items,
                   "A hook is the part of a song built to be remembered, often the chorus and its title. "
                   "<bookmark mark='b'/> It may be a melody, a rhythm, a sound such as a riff or a vocal effect, or a line of "
                   "words. <bookmark mark='c'/> Repetition is the main tool: the chorus returns, and repeats within itself. "
                   "<bookmark mark='d'/> The melodies are Part 14's again: a small range, mostly steps, and one leap that stands "
                   "out. <bookmark mark='e'/> Speech stress can guide a setting, while deliberate departures are common expressive devices.", marks="bcde")

    # ------------------------------------------------------------------
    def prosody(self):
        d = load("flow")
        cells = VGroup(*[Rectangle(width=0.6, height=0.35 + 0.18 * WEIGHT[k], stroke_width=1, stroke_color=GREY_B, fill_color=GREY_D, fill_opacity=0.6) for k in range(8)])
        cells.arrange(RIGHT, buff=0.06, aligned_edge=DOWN).move_to(UP * 0.8)
        def setting(sylls, col):
            g = VGroup()
            for txt, st, step in sylls:
                lab = label(txt, font_size=22 if st else 18, color=col if st else WHITE).next_to(cells[step], DOWN, buff=0.3)
                g.add(lab)
            return g
        good = setting([("BEAU", True, 0), ("ti", False, 2), ("ful", False, 3), ("DAY", True, 4)], TUNE)
        bad = setting([("beau", False, 0), ("TI", True, 2), ("FUL", True, 3), ("day", False, 5)], EAR)
        bad.shift(DOWN * 0.8)
        pr = d["prosody"]
        lab_good = label(rf"stress agrees with the beat: \ {round(100 * pr['good']['agree'])}\%", font_size=19, color=TUNE).next_to(good, RIGHT, buff=0.8)
        lab_bad = label(rf"stress fights the beat: \ {round(100 * pr['bad']['agree'])}\%", font_size=19, color=EAR).next_to(bad, RIGHT, buff=0.8)
        cap = label(r"bar heights: \ metrical weight of each sixteenth \ (Part 11)", font_size=18, color=GREY_A).next_to(cells, UP, buff=0.25)
        head = label(r"prosody: \ `beautiful day', \ set two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Prosody is how words sit on music. Spoken, beautiful day stresses BEAU and DAY. <bookmark mark='a'/> Set them "
            "on the strong positions of the bar, the tall bars here from Part 11's metrical grid, and every syllable agrees "
            "with the beat. <bookmark mark='b'/> Set them the other way, stresses on weak positions and weak syllables on "
            "strong ones, and the setting conflicts with this chosen speech-stress pattern. Dialect, duration and deliberate musical displacement can change the judgment. Monochord's measure is simply "
            "the share of syllables whose stress agrees with the strength of their position."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(good), FadeIn(lab_good))
            vo.wait_until("b")
            self.play(FadeIn(bad), FadeIn(lab_bad))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab_(self):
        items = [
            (r"songwriters check prosody by speaking the line over the beat", WHITE),
            (r"good settings put stressed syllables and important words on strong beats and long notes", WHITE),
            (r"deliberate mis-stress is a device: \ it makes a word stand out", WHITE),
            (r"in rap the words lead, \ and prosody becomes rhythm itself \ (chapter 8)", TUNE),
            (r"the lab lets you score a line of your own", GREY_A),
        ]
        rows_scene(self, r"setting words", items,
                   "Songwriters check prosody by speaking the line over the beat. <bookmark mark='b'/> Good settings put stressed "
                   "syllables and important words on strong beats and long notes. <bookmark mark='c'/> Deliberate mis-stress is "
                   "a device: it makes a word stand out. <bookmark mark='d'/> In rap the words lead, and prosody becomes the "
                   "rhythm itself, as chapter eight shows. <bookmark mark='e'/> The lab lets you score a line of your own.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def title(self):
        items = [
            (r"the title is usually the hook: \ the first or last line of the chorus, \ repeated", WHITE),
            (r"in the AABA song it opened or closed each A; \ in verse--chorus it anchors the chorus", WHITE),
            (r"L\'eveill\'e Gauvin found titles arriving earlier in later hits", WHITE),
            (r"a listener should be able to name the song after one chorus", TUNE),
            (r"the title is the song's address", GREY_A),
        ]
        rows_scene(self, r"the title", items,
                   "Where does the title go? <bookmark mark='b'/> Usually it is the hook itself: the first or the last line of the "
                   "chorus, repeated. <bookmark mark='c'/> In the AABA song it opened or closed each A section; in verse and "
                   "chorus it anchors the chorus. <bookmark mark='d'/> Léveillé Gauvin found titles arriving earlier in later "
                   "hits. <bookmark mark='e'/> A listener should be able to name the song after one chorus, <bookmark mark='f'/> "
                   "because the title is the song's address.", marks="cdef")

    # ------------------------------------------------------------------
    def earworms(self):
        items = [
            (r"earworms: \ tunes that replay involuntarily in the mind", WHITE),
            (r"Jakubowski and colleagues \ (2017): \ earworm tunes tend to be faster, \ with common contours and some unusual intervals", WHITE),
            (r"familiar shape, \ one surprise: \ Part 46's expectation, \ applied", WHITE),
            (r"chart success also depends on exposure, \ timing and luck, \ which no melody controls", TUNE),
            (r"chapter 6: \ the machine that made the beats", GREY_A),
        ]
        rows_scene(self, r"earworms", items,
                   "Some hooks stick too well. <bookmark mark='b'/> Earworms are tunes that replay involuntarily in the mind. "
                   "<bookmark mark='c'/> Kelly Jakubowski and colleagues found in 2017 that earworm tunes tend to be faster than "
                   "comparable songs, with common melodic contours and some unusual intervals: <bookmark mark='d'/> a familiar "
                   "shape with one surprise, Part 46's expectation at work. <bookmark mark='e'/> Chart success also depends on "
                   "exposure, timing and luck, which no melody controls. <bookmark mark='f'/> Chapter six turns to the machine "
                   "that made the beats.", marks="cdef")
