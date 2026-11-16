from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Hear(SoundScene):
    def construct(self):
        chapter(self, 9, r"Can anyone hear it?", r"Do listeners perceive a row?")
        self.quiz()
        self.studies()
        self.lerdahl()
        self.what()
        self.screen()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hear")
        c = clip("hear.quiz")
        card = listen_card(r"Our row, \ then two more lines of twelve notes. \ One is a form of the row \ (transposed, \ inverted, \ reversed); \ "
                           r"the other only reorders its first half. \ Which is the form, \ A or B?", width=10.6)
        with self.voiceover(
            "A test for your ears. Our row, then two more lines of twelve notes. One is a genuine form of the row, "
            "transposed, inverted and reversed. The other keeps the row's notes but reorders its first half. Which is the "
            "form of the row, A or B? This is hard, and that is the point."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        def roll(r):
            return mroll([[60 + x, i, 1] for i, x in enumerate(r)], width=3.6, height=1.6, lo=58, hi=73, color=GREY_A)
        gP, gA, gB = roll(d["row"]).move_to(LEFT * 4.4 + DOWN * 0.2), roll(d["A"]).move_to(DOWN * 0.2), roll(d["B"]).move_to(RIGHT * 4.4 + DOWN * 0.2)
        lP = label(r"the row", font_size=26, color=GREY_A).next_to(gP, UP, buff=0.3)
        la = label(r"A", font_size=36, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=36, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gP), FadeIn(gA), FadeIn(gB), FadeIn(lP), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"the row, \ A, \ B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for g, k in ((gP, "P"), (gA, "A"), (gB, "B")):
                flash(snd, g.notes, [d["starts"][k] + i * d["unit"] for i in range(12)], hot=WHITE, base=GREY_A)
            pulse(snd, lP, d["starts"]["P"], d["starts"]["A"] - 0.5, buff=0.08)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.08)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.08)
        ans = VGroup(label(r"A: \ the row's notes, \ first half reordered: \ not a form", font_size=20, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ $RI_5$, \ a true form", font_size=20, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is the form: the retrograde inversion starting on F. A shares the row's second half exactly and so sounds "
            "closer, but it is not a form at all. If you chose A, you may have prioritized shared content or contour; this informal question does not diagnose your strategy or establish a population result: shared content and "
            "shared contour, not the abstract identity of the forms."
        ):
            self.play(FadeIn(ans), gB.animate.set_color(TUNE), gA.animate.set_color(BLUE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def studies(self):
        items = [
            (r"Francès \ (1958): \ trained musicians could not reliably tell which row a passage used", WHITE),
            (r"Krumhansl, \ Sandell and Sergeant \ (1987): \ some sensitivity to a row's order, \ mostly in trained listeners", WHITE),
            (r"listeners follow contour, \ register, \ rhythm and texture far better than row identity", WHITE),
            (r"what the ear does hear: \ no tonal centre, \ constant chromatic saturation, \ a distinct harmonic colour", TUNE),
            (r"a composer's method need not be a listener's experience", GREY_A),
        ]
        rows_scene(self, r"what experiments found", items,
                   "Psychologists have asked the same question. <bookmark mark='b'/> Robert Francès, in 1958, found that even "
                   "trained musicians could not reliably tell which row a passage used. <bookmark mark='c'/> Carol Krumhansl "
                   "and colleagues, in 1987, found some sensitivity to a row's order, mostly in listeners with training. "
                   "<bookmark mark='d'/> Listeners follow contour, register, rhythm and texture far better than the identity "
                   "of a row's forms. <bookmark mark='e'/> Listeners can respond to tonal cues and their absence, with task, training and context affecting the result, the "
                   "constant circulation of all twelve notes, and a characteristic harmonic colour. <bookmark mark='f'/> A "
                   "composer's method need not be a listener's experience; Part 46 takes up what listeners expect.", marks="cdef")

    # ------------------------------------------------------------------
    def what(self):
        d = load("hear")
        rows_ = text_rows([
            (r"a random reordering of the twelve notes shares the row's first hexachord", WHITE),
            (rf"by exact count: \ 1 time in 924; \ by simulation: \ {1000 * d['share_random']:.2f} in 1,000".replace(",", "{,}"), WHITE),
            (r"so a shared hexachord is strong evidence of a relation, \ for an analyst with the score", TUNE),
            (r"for a listener, \ the same evidence is spread over seconds and registers", WHITE),
            (r"the difference between analysis and perception is a difference in what is available", GREY_A),
        ], font_size=24)
        head = label(r"evidence for the eye, \ and for the ear", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There is a numerical way to see the gap. <bookmark mark='a'/> Ask how often a random ordering of the twelve "
            "notes happens to share the row's first six. <bookmark mark='b'/> Exactly one time in nine hundred and "
            "twenty-four, and a simulation agrees. <bookmark mark='c'/> So an analyst with the score who finds a shared "
            "hexachord has a selective match under this fixed-hexachord uniform-row null; searching many boundaries and transformations increases chance matches. <bookmark mark='d'/> A listener gets the same evidence spread over "
            "seconds and registers, with no score to look back at. <bookmark mark='e'/> The gap between analysis and "
            "perception is partly a gap in what is available."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def screen(self):
        items = [
            (r"Leonard Rosenman's score for \textit{The Cobweb} \ (1955): \ often called Hollywood's first twelve-tone score", WHITE),
            (r"Jerry Goldsmith, \ \textit{Planet of the Apes} \ (1968): \ serial and percussive, \ for an alien world", WHITE),
            (r"jazz players wrote twelve-tone tunes, \ and used rows for improvising", WHITE),
            (r"atonality as a sign: \ anxiety, \ the alien, \ the uncanny", TUNE),
            (r"listeners who would never sit through a serial concert hear it every week at the cinema", GREY_A),
        ]
        rows_scene(self, r"rows on screen and in jazz", items,
                   "Audiences meet this music in other places. <bookmark mark='b'/> Leonard Rosenman's score for The Cobweb, of 1955, is often called Hollywood's first twelve-tone score, <bookmark mark='c'/> and Jerry Goldsmith's music for Planet of the Apes, in 1968, used serial and percussive writing for an alien world. <bookmark mark='d'/> Jazz players wrote twelve-tone tunes and used rows to improvise. <bookmark mark='e'/> In these settings atonality is a sign, of anxiety, of the alien, of the uncanny. <bookmark mark='f'/> Listeners who would never sit through a serial concert hear it every week at the cinema.", marks="cdef")

    # ------------------------------------------------------------------
    def lerdahl(self):
        items = [
            (r"Fred Lerdahl \ (1988): \ `Cognitive constraints on compositional systems'", WHITE),
            (r"listeners build hierarchies: \ some events more stable, \ others elaborate them \ (Part 22)", WHITE),
            (r"serial organization, \ he argued, \ gives the ear no basis for such a hierarchy", WHITE),
            (r"a compositional grammar and a listening grammar can come apart", TUNE),
            (r"composers can respond by building hierarchy from register, \ rhythm and texture instead", GREY_A),
        ]
        rows_scene(self, r"an argument from cognition", items,
                   "The composer and theorist Fred Lerdahl turned these findings into an argument. <bookmark mark='b'/> In a 1988 essay on cognitive constraints on compositional systems, <bookmark mark='c'/> he started from the hierarchies listeners build, some events stable and others elaborating them, as Part 22's reductions showed. <bookmark mark='d'/> Serial organization, he argued, gives the ear no basis for such a hierarchy among pitches. <bookmark mark='e'/> The grammar a composer uses and the grammar a listener uses can come apart. <bookmark mark='f'/> Composers can respond by building hierarchy from register, rhythm and texture instead, which is what many of the best serial pieces do.", marks="cdef")
