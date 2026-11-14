from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403

LYRIC = [r"Train left at midnight, \ took my good shoes and my song,",
         r"Train left at midnight, \ took my good shoes and my song,",
         r"Now I'm walking to Memphis, \ and the road is twelve bars long."]


class AAB(SoundScene):
    def construct(self):
        chapter(self, 3, r"Call and response: \ the blues lyric", r"How does a twelve-bar verse tell a story?")
        self.lyric()
        self.hear()
        self.answers()
        self.singers()
        self.why()

    # ------------------------------------------------------------------
    def lyric(self):
        lines = VGroup(*[label(l, font_size=24, color=c) for l, c in zip(LYRIC, (TUNE, TUNE, EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.6)
        tags = VGroup(*[label(t, font_size=24, color=c).next_to(l, LEFT, buff=0.4) for t, l, c in zip(("A", "A", "B"), lines, (TUNE, TUNE, EAR))])
        cap = VGroup(label(r"each line takes the first half of a four-bar line of the form", font_size=20, color=WHITE),
                     label(r"the second half is left for an answer", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        head = label(r"a verse of ours, \ AAB", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A blues verse fits the twelve bars in a particular way. Here is a verse of our own. <bookmark mark='a'/> A line "
            "is sung, and repeated, usually over the move to the subdominant, so the same words take on a new colour. "
            "<bookmark mark='b'/> Then a third line answers it, and rhymes. A, A, B. <bookmark mark='c'/> Each line fills "
            "only the first half of its four bars; the second half is left open, for an answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(tags[0]), FadeIn(lines[1]), FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(tags[2]))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("callresp")
        c = clip("callresp.aab")
        ch = chart(d["changes"], cell_w=2.5, cell_h=0.8, size=20).move_to(UP * 0.7)
        marks = VGroup()
        for line0, col, txt in ((0, TUNE, r"voice"), (4, TUNE, r"voice"), (8, EAR, r"voice")):
            for k in range(2):
                marks.add(Rectangle(width=2.4, height=0.12, stroke_width=0, fill_color=col, fill_opacity=0.9).next_to(ch.bars[line0 + k], DOWN, buff=-0.2))
            for k in range(2, 4):
                marks.add(Rectangle(width=2.4, height=0.12, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).next_to(ch.bars[line0 + k], DOWN, buff=-0.2))
        leg = VGroup(label(r"sung line", font_size=18, color=TUNE), label(r"guitar answer", font_size=18, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(ch, DOWN, buff=0.4)
        cap = label(r"the voice is Part 17's model: \ it sings vowels, \ not the words", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.05)
        with self.voiceover(
            "Hear the verse's shape, sung by Part 17's model voice, which sings vowels rather than words. Each sung line is "
            "answered by a guitar in the bars the voice leaves open. The thirds of the vocal line are blue, between E flat "
            "and E."
        ):
            self.play(FadeIn(ch), FadeIn(marks), FadeIn(leg), FadeIn(cap))
        bar = 4 * d["beat"]
        with self.listen(c) as snd:
            window(snd, r"an AAB blues", kind="synthesized", detail=r"a model voice and guitar, \ with piano, \ bass and cymbal", corner=DL, tag_corner=DR)
            for i in range(12):
                pulse(snd, ch.bars[i], i * bar, (i + 1) * bar - 0.03, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def answers(self):
        items = [
            (r"the answer may be a guitar, \ a piano, \ a harmonica, \ a horn, \ or the singer's own guitar", WHITE),
            (r"call and response \ (Part 37), \ now inside one performance", WHITE),
            (r"the answer comments on the line: \ it echoes, \ contradicts, \ or finishes the thought", WHITE),
            (r"in jazz, \ soloists `trade fours': \ four bars each, \ answering one another", TUNE),
            (r"a conversation built into the form", GREY_A),
        ]
        rows_scene(self, r"the answer", items,
                   "Who answers? <bookmark mark='b'/> A guitar, a piano, a harmonica, a horn, or the singer's own guitar. "
                   "<bookmark mark='c'/> It is Part 37's call and response, now inside a single performance. "
                   "<bookmark mark='d'/> The answer comments on the line: it echoes it, contradicts it, or finishes the thought. "
                   "<bookmark mark='e'/> In jazz, soloists trade fours, four bars each, answering one another. "
                   "<bookmark mark='f'/> A conversation built into the form.", marks="cdef")

    # ------------------------------------------------------------------
    def singers(self):
        items = [
            (r"`classic' blues of the 1920s: \ Ma Rainey and Bessie Smith, \ with bands, \ on the vaudeville stage", WHITE),
            (r"country blues: \ a singer with a guitar, \ free with the form, \ adding or dropping beats", WHITE),
            (r"Chicago in the 1940s and 50s: \ Muddy Waters and others electrify the Delta blues", WHITE),
            (r"the twelve-bar form was a norm, \ not a law: \ many early blues bend it", TUNE),
            (r"recordings show the variety; \ the textbook form is a later average", GREY_A),
        ]
        rows_scene(self, r"the singers", items,
                   "The form was carried by singers. <bookmark mark='b'/> The classic blues of the 1920s, Ma Rainey and Bessie "
                   "Smith, was sung with bands on the vaudeville stage. <bookmark mark='c'/> Country blues was a singer with a "
                   "guitar, free with the form, adding or dropping beats as the words required. <bookmark mark='d'/> In Chicago "
                   "in the 1940s and 50s, Muddy Waters and others electrified the blues of the Delta. <bookmark mark='e'/> The "
                   "twelve-bar form was a norm, not a law, and many early blues bend it. <bookmark mark='f'/> The recordings show "
                   "the variety; the textbook form is a later average.", marks="cdef")

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"the repeated line gives the singer time to find the third line, \ live", WHITE),
            (r"it lets the audience join in, \ and expect the punch line", WHITE),
            (r"the third line lands on the tonic: \ the rhyme and the cadence arrive together", WHITE),
            (r"a form shaped for improvising words, \ as ragtime's was shaped for the printed page", TUNE),
            (r"chapter 4: \ ragtime", GREY_A),
        ]
        rows_scene(self, r"why AAB?", items,
                   "Why A, A, B? <bookmark mark='b'/> The repeated line gives the singer time to find the third line, live. "
                   "<bookmark mark='c'/> It lets the audience join in, and expect the punch line. <bookmark mark='d'/> And the "
                   "third line lands on the tonic, so the rhyme and the cadence arrive together. <bookmark mark='e'/> It is a "
                   "form shaped for improvising words, as ragtime's form was shaped for the printed page. "
                   "<bookmark mark='f'/> Which is the next chapter.", marks="cdef")
