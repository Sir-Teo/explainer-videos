from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


class Band(SoundScene):
    def construct(self):
        chapter(self, 6, r"The swing band", r"How do sixteen players swing together?")
        self.era()
        self.sections()
        self.riff()
        self.kc()
        self.arrangers()

    # ------------------------------------------------------------------
    def era(self):
        items = [
            (r"the swing era: \ big bands of the mid-1930s to the mid-1940s, \ playing for dancers", WHITE),
            (r"Fletcher Henderson's band and his arrangers set the pattern in New York in the 1920s", WHITE),
            (r"Benny Goodman's success in 1935 made swing the popular music of America", WHITE),
            (r"Duke Ellington, \ Count Basie, \ Chick Webb at Harlem's Savoy Ballroom, \ where the Lindy Hop was danced", TUNE),
            (r"music for dancing, \ written down by arrangers, \ with room for soloists", GREY_A),
        ]
        rows_scene(self, r"the swing era", items,
                   "From the mid-1930s to the mid-1940s, swing was the popular music of America, played by big bands for "
                   "dancers. <bookmark mark='b'/> Fletcher Henderson's band and its arrangers had set the pattern in New York in "
                   "the 1920s. <bookmark mark='c'/> Benny Goodman's success in 1935 carried it everywhere. <bookmark mark='d'/> "
                   "Duke Ellington, Count Basie, and Chick Webb at Harlem's Savoy Ballroom, where the Lindy Hop was danced, led "
                   "the great bands. <bookmark mark='e'/> It was music for dancing, written down by arrangers, with room for "
                   "soloists.", marks="bcde")

    # ------------------------------------------------------------------
    def sections(self):
        def section(name, n, col):
            seats = VGroup(*[Circle(radius=0.22, color=col, stroke_width=2, fill_opacity=0.25, fill_color=col) for _ in range(n)]).arrange(RIGHT, buff=0.12)
            return VGroup(seats, label(name, font_size=19, color=col)).arrange(DOWN, buff=0.15)
        saxes = section(r"saxophones: \ 2 alto, \ 2 tenor, \ baritone", 5, TUNE)
        trb = section(r"trombones", 4, BLUE)
        tpt = section(r"trumpets", 4, EAR)
        rhythm = section(r"rhythm: \ piano, \ guitar, \ bass, \ drums", 4, GREY_A)
        g = VGroup(tpt, trb, saxes).arrange(DOWN, buff=0.45).move_to(RIGHT * 1.2 + DOWN * 0.1)
        rhythm.next_to(g, LEFT, buff=1.0)
        roles = VGroup(label(r"sections play as units, \ in block chords", font_size=19, color=WHITE),
                       label(r"the rhythm section keeps four even beats", font_size=19, color=WHITE),
                       label(r"sections answer each other: \ call and response again", font_size=19, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
        head = label(r"a big band", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "A big band of the swing era had about sixteen players in four sections. <bookmark mark='a'/> Saxophones, "
            "usually five; trombones and trumpets, three or four each; and a rhythm section of piano, guitar, bass and drums. "
            "<bookmark mark='b'/> The horn sections play as units, in block chords, while the rhythm section keeps four even "
            "beats to the bar, and the sections answer one another: call and response again, now between groups of players."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(saxes, trb, tpt, rhythm).copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(saxes), FadeIn(trb), FadeIn(tpt), FadeIn(rhythm), lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in roles], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def riff(self):
        d = load("band")
        c = clip("band.riff")
        ch = chart(d["changes"], cell_w=2.5, cell_h=0.8, size=20).move_to(UP * 0.35)
        marks = VGroup()
        for b2 in range(6):
            marks.add(Rectangle(width=2.35, height=0.12, stroke_width=0, fill_color=TUNE, fill_opacity=0.9).next_to(ch.bars[2 * b2], DOWN, buff=-0.2))
            marks.add(Rectangle(width=2.35, height=0.12, stroke_width=0, fill_color=EAR, fill_opacity=0.9).next_to(ch.bars[2 * b2 + 1], DOWN, buff=-0.2))
        leg = VGroup(label(r"saxophones: \ the riff", font_size=18, color=TUNE), label(r"brass: \ the answer", font_size=18, color=EAR)).arrange(RIGHT, buff=0.8).next_to(ch, DOWN, buff=0.4)
        cap = label(rf"ours: \ a two-bar riff moved with the chords, \ {d['bpm']} beats a minute; \ the horns are additive, \ labelled synthesized", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.05)
        with self.voiceover(
            "Here is a riff chart of our own on the twelve-bar blues. The saxophones play a two-bar riff, moved with the "
            "chords; in its second bar the brass answer with three short punches. The rhythm section swings underneath. Six "
            "calls, six answers."
        ):
            self.play(FadeIn(ch), FadeIn(marks), FadeIn(leg), FadeIn(cap))
        bar = 4 * 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"a riff chart", kind="synthesized", detail=r"additive horns, \ string, \ cymbal and piano models", corner=DL, tag_corner=DR)
            for i in range(12):
                pulse(snd, ch.bars[i], i * bar, (i + 1) * bar - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kc(self):
        items = [
            (r"Kansas City in the 1930s: \ bands that built pieces from riffs, \ by ear, \ in rehearsal and on the stand", WHITE),
            (r"`head arrangements': \ memorised, \ not written", WHITE),
            (r"Count Basie's band: \ a light, \ even four from the rhythm section, \ riffs piled on riffs", WHITE),
            (r"a riff is a short figure repeated over changing chords: \ the chords move under it", TUNE),
            (r"riffs became the backbone of rhythm and blues and rock and roll", GREY_A),
        ]
        rows_scene(self, r"riffs and Kansas City", items,
                   "Riff charts came from Kansas City in the 1930s, where bands built pieces from riffs, by ear, in rehearsal "
                   "and on the stand. <bookmark mark='b'/> These were head arrangements, memorised rather than written. "
                   "<bookmark mark='c'/> Count Basie's band was the model: a light, even four from the rhythm section, and riffs "
                   "piled on riffs. <bookmark mark='d'/> A riff is a short figure repeated as the chords move under it. "
                   "<bookmark mark='e'/> Riffs became the backbone of rhythm and blues and rock and roll.", marks="bcde")

    # ------------------------------------------------------------------
    def arrangers(self):
        items = [
            (r"arrangers voiced each section as a chord moving in parallel: \ `block' or `soli' writing", WHITE),
            (r"a typical chart: \ the tune, \ solos over the form, \ a full-band `shout' chorus, \ the tune again", WHITE),
            (r"Ellington wrote for particular players, \ and with Billy Strayhorn, \ for particular sounds", WHITE),
            (r"Part 41's orchestration, \ applied to sixteen players and a rhythm section", TUNE),
            (r"chapter 7 opens up the rhythm section", GREY_A),
        ]
        rows_scene(self, r"the arrangers", items,
                   "Behind the bands were arrangers. <bookmark mark='b'/> They voiced each section as a chord moving in parallel, "
                   "which players call block or soli writing. <bookmark mark='c'/> A typical chart states the tune, opens the "
                   "form for solos, builds to a full-band shout chorus, and ends with the tune again. <bookmark mark='d'/> Duke "
                   "Ellington wrote for particular players, and with Billy Strayhorn for particular sounds. "
                   "<bookmark mark='e'/> It is Part 41's orchestration, applied to sixteen players. <bookmark mark='f'/> Chapter "
                   "seven opens up the rhythm section.", marks="cdef")
