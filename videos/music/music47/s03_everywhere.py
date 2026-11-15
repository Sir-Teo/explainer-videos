from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Everywhere(SoundScene):
    def construct(self):
        chapter(self, 2, r"Every society sings", r"Is there anything all music does?")
        self.ethnography()
        self.quiz()
        self.form()
        self.contexts()

    # ------------------------------------------------------------------
    def ethnography(self):
        items = [
            (r"Samuel Mehr and colleagues \ (2019): \ the Natural History of Song", WHITE),
            (r"ethnographies of 315 societies: \ music is described in every one", WHITE),
            (r"a discography of field recordings: \ dance songs, \ healing songs, \ love songs and lullabies from around the world", WHITE),
            (r"songs made for the same purpose share features across societies", TUNE),
            (r"and a typical society's songs vary more among themselves than societies differ from one another", GREY_A),
        ]
        rows_scene(self, r"the natural history of song", items,
                   "In 2019 Samuel Mehr and a large team published the Natural History of Song. <bookmark mark='b'/> They read "
                   "ethnographies of 315 societies and found music described in every one. <bookmark mark='c'/> They also "
                   "gathered field recordings of four kinds of song from around the world: dance songs, healing songs, love "
                   "songs and lullabies. <bookmark mark='d'/> Songs made for the same purpose turned out to share features "
                   "across societies. <bookmark mark='e'/> And within a typical society, the songs varied more among themselves "
                   "than societies differed from one another.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("lullaby")
        c = clip("lullaby.two")
        card = listen_card(r"One melody, \ sung two ways. \ One is meant for dancing, \ the other for a baby. \ Which is the lullaby?", width=10.0)
        with self.voiceover(
            "Try it yourself. One melody, the opening of Au clair de la lune, sung two ways. One version is meant for "
            "dancing; the other for a baby. Which is the lullaby?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        roll_ = mroll(mel_notes(d["notes"], base=60), width=9.0, height=1.2, lo=58, hi=66, color=TUNE).move_to(UP * 1.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.6)
        self.play(FadeOut(card), FadeIn(roll_), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one melody, \ two ways", kind="synthesized", detail=r"Part 8's voice, \ Part 40's drums", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        f = d["features"]
        rows_ = VGroup()
        for k, (a, b) in f.items():
            rows_.add(VGroup(label(k, font_size=18, color=GREY_A).set_width(5.2) if len(k) > 34 else label(k, font_size=18, color=GREY_A),
                             label(f"{a:g}", font_size=20, color=EAR), label(f"{b:g}", font_size=20, color=TUNE)))
        tab = VGroup()
        y = -1.9
        for r in rows_:
            r[0].move_to([-0.8, y, 0], aligned_edge=RIGHT)
            r[1].move_to([1.3, y, 0])
            r[2].move_to([3.6, y, 0])
            tab.add(r)
            y -= 0.45
        hdr = VGroup(label(r"dance", font_size=20, color=EAR).move_to([1.3, -1.45, 0]), label(r"lullaby", font_size=20, color=TUNE).move_to([3.6, -1.45, 0]))
        with self.voiceover(
            f"The lullaby was the second: {say(d['bpm']['lullaby'])} beats a minute against {say(d['bpm']['dance'])}, every "
            "note held to its full length, one soft voice, no drum. <bookmark mark='a'/> These are the very differences "
            "Mehr's team measured in real songs: lullabies are slower, smoother, quieter and simpler; dance songs faster, "
            "more accented and more rhythmic, and often with more performers. Here we chose them on purpose, so the question "
            "was easy. The surprise is that it is nearly as easy with songs from societies you have never heard of."
        ) as vo:
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
            vo.wait_until("a")
            self.play(boxes.animate.shift(UP * 0.5), FadeIn(hdr), FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def form(self):
        items = [
            (r"Mehr and colleagues \ (2018): \ listeners in 60 countries heard short excerpts of songs from 86 mostly small-scale societies", WHITE),
            (r"rating each for dancing, \ soothing a baby, \ healing or expressing love, \ they guessed the purpose above chance", WHITE),
            (r"dance songs and lullabies were recognized best: \ their features are near opposites", WHITE),
            (r"Constance Bainbridge and colleagues \ (2021): \ American infants relaxed to unfamiliar foreign lullabies", TUNE),
            (r"heart rate, \ pupil size and skin conductance all fell, \ more for lullabies than for other foreign songs", GREY_A),
        ]
        rows_scene(self, r"form follows function", items,
                   "In 2018 Mehr's team asked listeners in sixty countries to hear short excerpts of songs from eighty-six "
                   "mostly small-scale societies. <bookmark mark='b'/> Rating each for dancing, soothing a baby, healing or "
                   "expressing love, they guessed the purpose better than chance. <bookmark mark='c'/> Dance songs and "
                   "lullabies were recognized best, and their features are near opposites. <bookmark mark='d'/> In 2021 "
                   "Constance Bainbridge and colleagues played unfamiliar foreign lullabies to American infants, "
                   "<bookmark mark='e'/> and their heart rates, pupil sizes and skin conductance all fell, more than for other "
                   "foreign songs.", marks="bcde")

    # ------------------------------------------------------------------
    def contexts(self):
        items = [
            (r"across the ethnographies, \ song goes with infant care, \ healing, \ dance and love", WHITE),
            (r"and with mourning, \ war, \ processions and religious ritual", WHITE),
            (r"it is often performed in groups, \ and often by specialists as well as by everyone", WHITE),
            (r"the purposes repeat; \ the sounds that serve them are partly shared, \ partly local", TUNE),
            (r"chapter 3: \ which features of the sound itself are shared?", GREY_A),
        ]
        rows_scene(self, r"what song is for", items,
                   "Across the ethnographies, song goes with the same occasions. <bookmark mark='b'/> With infant care, healing, "
                   "dance and love, <bookmark mark='c'/> and with mourning, war, processions and religious ritual. "
                   "<bookmark mark='d'/> It is often performed in groups, and by specialists as well as by everyone. "
                   "<bookmark mark='e'/> The purposes repeat; the sounds that serve them are partly shared and partly local. "
                   "<bookmark mark='f'/> Chapter three asks which features of the sound itself are shared.", marks="bcdef")
