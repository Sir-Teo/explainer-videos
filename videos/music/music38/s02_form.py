from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


class Form(SoundScene):
    def construct(self):
        chapter(self, 1, r"The twelve-bar blues", r"Why has one twelve-bar pattern lasted a century?")
        self.origins()
        self.chart_()
        self.hear()
        self.variants()
        self.sevenths()
        self.everywhere()

    # ------------------------------------------------------------------
    def origins(self):
        items = [
            (r"the blues grew among African Americans in the Deep South, \ around 1900", WHITE),
            (r"from field hollers, \ work songs and spirituals, \ and the ballads of travelling songsters", WHITE),
            (r"W. C. Handy published \textit{The Memphis Blues} in 1912 and \textit{St. Louis Blues} in 1914", WHITE),
            (r"1920: \ Mamie Smith's \textit{Crazy Blues}, \ the first blues recorded by a Black singer, \ sold in huge numbers", TUNE),
            (r"Ma Rainey, \ Bessie Smith, \ and in the Delta Charley Patton and Robert Johnson", GREY_A),
        ]
        rows_scene(self, r"the blues", items,
                   "The blues grew among African Americans in the Deep South around 1900. <bookmark mark='b'/> It drew on field "
                   "hollers, work songs and spirituals, and on the ballads of travelling songsters. <bookmark mark='c'/> W. C. "
                   "Handy published The Memphis Blues in 1912 and St. Louis Blues in 1914. <bookmark mark='d'/> In 1920 Mamie "
                   "Smith's Crazy Blues, the first blues recorded by a Black singer, sold in huge numbers, and record companies "
                   "went looking for more. <bookmark mark='e'/> They found Ma Rainey and Bessie Smith, and in the Mississippi "
                   "Delta, Charley Patton and Robert Johnson.", marks="bcde")

    # ------------------------------------------------------------------
    def chart_(self):
        d = load("form")
        ch = chart(d["changes"], cell_w=2.4, cell_h=0.85).move_to(UP * 0.9)
        roman = VGroup(*[label(r, font_size=16, color=GREY_A).move_to(b[0].get_corner(DR) + UL * 0.2 + LEFT * 0.1) for r, b in zip(d["roman"], ch.bars)])
        lines = VGroup(label(r"bars 1--4: \ the tonic, \ I", font_size=20, color=TUNE),
                       label(r"bars 5--8: \ to the subdominant, \ IV, \ and back", font_size=20, color=BLUE),
                       label(r"bars 9--12: \ the dominant, \ V, \ IV, \ home, \ and V to start again", font_size=20, color=EAR)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(ch, DOWN, buff=0.45)
        g = VGroup(ch, roman, lines)
        head = label(r"the twelve-bar blues, \ in C", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The commonest blues form is twelve bars long, in three lines of four. <bookmark mark='a'/> The first line stays "
            "on the tonic chord, C. <bookmark mark='b'/> The second moves to the subdominant, F, and back. "
            "<bookmark mark='c'/> The third reaches the dominant, G, falls through F to C, and ends on G to send the music "
            "round again. Every chord is a dominant seventh: C seven, F seven, G seven. In Part 18's harmony C seven would "
            "have to resolve to F; in the blues it is simply home."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in ch.bars[:4]], *[FadeIn(r) for r in roman[:4]])
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(b) for b in ch.bars[4:8]], *[FadeIn(r) for r in roman[4:8]], FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(b) for b in ch.bars[8:]], *[FadeIn(r) for r in roman[8:]], FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("form")
        c = clip("form.twelve")
        ch = chart(d["changes"]).move_to(UP * 0.4)
        cap = label(rf"ours: \ piano on beats 2 and 4, \ a walking bass, \ ride and hi-hat; \ {d['bpm']} beats a minute", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Hear one chorus, as a blues player calls a time through the form: piano chords on beats two and four, a "
            "walking bass, ride cymbal and hi-hat. Follow the bars on the chart."
        ):
            self.play(FadeIn(ch), FadeIn(cap))
        bar = 4 * 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"a twelve-bar blues", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            for i in range(12):
                pulse(snd, ch.bars[i], i * bar, (i + 1) * bar - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variants(self):
        d = load("form")
        quick = chart(d["quick"], cell_w=1.9, cell_h=0.48, size=17, per_row=6)
        basic = chart(d["changes"], cell_w=1.9, cell_h=0.48, size=17, per_row=6)
        jazz = chart(d["jazz"], cell_w=1.9, cell_h=0.48, size=16, per_row=6)
        rows_ = VGroup(VGroup(label(r"basic", font_size=18, color=TUNE), basic).arrange(DOWN, buff=0.12),
                       VGroup(label(r"quick change: \ IV in bar 2", font_size=18, color=BLUE), quick).arrange(DOWN, buff=0.12),
                       VGroup(label(r"a jazz blues: \ ii--V's and passing chords", font_size=18, color=EAR), jazz).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.45)
        rows_.scale_to_fit_height(min(rows_.height, 6.6)).move_to(DOWN * 0.15)
        with self.voiceover(
            "The form has many variants. <bookmark mark='a'/> The quick change visits F in the second bar. "
            "<bookmark mark='b'/> A jazz blues fills the frame with more chords: a two-five into F in bar four, a diminished "
            "chord in bar six, a secondary dominant in bar eight, and two-fives back to the top. The skeleton stays the "
            "same: twelve bars, the move to the subdominant in bar five, the dominant in bar nine."
        ) as vo:
            self.play(FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sevenths(self):
        items = [
            (r"in the blues the seventh chord is the unit, \ not a dissonance that must resolve", WHITE),
            (r"the tonic itself is a dominant seventh: \ C E G B$\flat$", WHITE),
            (r"the B$\flat$ and the melody's blue notes come from the same place: \ a scale that is neither major nor minor", WHITE),
            (r"Part 18's rules describe one tradition; \ the blues keeps another", TUNE),
            (r"chapter 8 returns to sevenths, \ and the tones that define them", GREY_A),
        ]
        rows_scene(self, r"the seventh as home", items,
                   "Notice what the blues does with the seventh chord. <bookmark mark='b'/> It is the unit, not a dissonance "
                   "that must resolve. <bookmark mark='c'/> The tonic itself is a dominant seventh, C, E, G, B flat. "
                   "<bookmark mark='d'/> That B flat, and the melody's blue notes, come from the same place: a scale that is "
                   "neither major nor minor. <bookmark mark='e'/> Part 18's rules describe one tradition; the blues keeps "
                   "another. <bookmark mark='f'/> Chapter eight returns to sevenths, and to the tones that define them.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def everywhere(self):
        items = [
            (r"the twelve-bar form runs through jazz, \ rhythm and blues, \ rock and roll and soul", WHITE),
            (r"jam sessions use it because everyone knows it: \ a shared map", WHITE),
            (r"eight- and sixteen-bar blues exist too; \ the twelve-bar is the standard", WHITE),
            (r"a form simple enough to learn in a minute, \ open enough for a lifetime", TUNE),
            (r"chapter 2: \ the notes that give the blues its name", GREY_A),
        ]
        rows_scene(self, r"a shared map", items,
                   "The twelve-bar form runs through jazz, rhythm and blues, rock and roll and soul. <bookmark mark='b'/> Jam "
                   "sessions use it because everyone knows it: it is a shared map. <bookmark mark='c'/> There are eight- and "
                   "sixteen-bar blues too, but twelve is the standard. <bookmark mark='d'/> It is a form simple enough to learn "
                   "in a minute and open enough for a lifetime. <bookmark mark='e'/> Chapter two turns to the notes that give "
                   "the blues its name.", marks="bcde")
