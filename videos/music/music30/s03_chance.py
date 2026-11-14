from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Chance(SoundScene):
    def construct(self):
        chapter(self, 2, r"Chance and silence", r"What is left when the composer stops choosing?", extra=((1952, r"\textit{4'33''}"),))
        self.cage()
        self.silence()
        self.dice()
        self.indeterminacy()
        self.fluxus()

    # ------------------------------------------------------------------
    def cage(self):
        items = [
            (r"John Cage, \ 1912--1992: \ a pupil of Schoenberg in Los Angeles", WHITE),
            (r"the prepared piano \ (1940): \ screws, \ bolts and rubber between the strings", WHITE),
            (r"Zen Buddhism and the \textit{I Ching}: \ remove the composer's likes and dislikes", WHITE),
            (r"\textit{Music of Changes} \ (1951): \ every note chosen by tossing coins", TUNE),
            (r"chance as a discipline, \ not a careless shortcut", GREY_A),
        ]
        rows_scene(self, r"John Cage", items,
                   "In America, John Cage went another way. <bookmark mark='b'/> He had studied with Schoenberg in Los Angeles, "
                   "and in 1940 he invented the prepared piano, with screws, bolts and rubber wedged between the strings. "
                   "<bookmark mark='c'/> Through Zen Buddhism and the Chinese I Ching he set out to remove his own likes and "
                   "dislikes from his music. <bookmark mark='d'/> In Music of Changes, of 1951, every note was chosen by tossing "
                   "coins and consulting the I Ching's tables. <bookmark mark='e'/> For Cage chance was a discipline, a way of "
                   "letting sounds be themselves, not a careless shortcut.", marks="bcde")

    # ------------------------------------------------------------------
    def silence(self):
        items = [
            (r"Woodstock, \ New York, \ 29 August 1952: \ David Tudor sits at a piano and plays nothing", WHITE),
            (r"three movements, \ marked by closing and opening the keyboard lid", WHITE),
            (r"the music is what the audience hears: \ wind, \ rain on the roof, \ people leaving", WHITE),
            (r"Cage in an anechoic chamber \ (about 1951): \ he still heard two sounds, \ high and low, \ his own body", TUNE),
            (r"there is no silence: \ only sounds we have not chosen to listen to", EAR),
        ]
        rows_scene(self, r"4 minutes 33 seconds", items,
                   "Then came the most famous piece of the century in which nothing is played. <bookmark mark='b'/> At "
                   "Woodstock, New York, in August 1952, the pianist David Tudor sat at a piano, opened the lid, and played "
                   "nothing for four minutes and thirty-three seconds, <bookmark mark='c'/> marking three movements by closing "
                   "and opening the keyboard lid. <bookmark mark='d'/> The music was what the audience heard: wind in the trees, "
                   "rain on the roof, people talking and leaving. <bookmark mark='e'/> Cage had visited an anechoic room at "
                   "Harvard and still heard two sounds, one high and one low; he was told they were his nervous system and his "
                   "blood. <bookmark mark='f'/> His conclusion: there is no such thing as silence, only sounds we have not "
                   "chosen to hear.", marks="cdef")

    # ------------------------------------------------------------------
    def dice(self):
        d = load("chance")
        c = clip("chance.dice")
        notes = d["notes"]
        lo = min(n[0] for n in notes) - 1
        hi = max(n[0] for n in notes) + 1
        g = mroll(notes, width=11.0, height=3.0, lo=lo, hi=hi, color=TUNE, bar_h=0.12).move_to(DOWN * 0.2)
        head = label(r"the Tune's notes, \ with order, \ octave, \ length and silence chosen by dice \ (ours)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"twenty throws: \ the materials are the Tune's; \ the decisions are not", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the idea, in a sketch of our own. The materials are the Tune's six notes. Everything else, which note "
            "comes next, its octave, its length and the silence after it, is decided by a random number generator, the "
            "film's coin. Twenty throws. Listen for what the ear does with it: it still hunts for patterns, and finds some."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"twenty throws", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def indeterminacy(self):
        items = [
            (r"chance in composing \ (Cage) \ versus indeterminacy in performing \ (Feldman, \ Brown, \ Stockhausen)", WHITE),
            (r"graphic scores: \ Earle Brown's \textit{December 1952}, \ a page of lines and rectangles", WHITE),
            (r"Stockhausen's \textit{Klavierstück XI} \ (1956): \ the pianist chooses the order of nineteen fragments", WHITE),
            (r"every performance a different piece: \ what is the work?", TUNE),
            (r"Part 42 asks what composing is; \ Part 65, \ what a machine's random choices add", GREY_A),
        ]
        rows_scene(self, r"open works", items,
                   "Chance came in two kinds. <bookmark mark='b'/> Cage used it in composing; others, Morton Feldman, Earle "
                   "Brown, Stockhausen, left choices to the performer. <bookmark mark='c'/> Brown's December 1952 is a single "
                   "page of lines and rectangles. <bookmark mark='d'/> Stockhausen's Piano Piece Eleven, of 1956, lets the "
                   "pianist play its nineteen fragments in any order the eye happens to fall on. <bookmark mark='e'/> Every "
                   "performance is a different piece, which raises the question of what the work is. "
                   "<bookmark mark='f'/> Part 42 asks what composing is, and Part 65 what a machine's random choices add.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def fluxus(self):
        items = [
            (r"Black Mountain College, \ 1952: \ Cage's `Theatre Piece No. 1', \ an early happening", WHITE),
            (r"Fluxus \ (from 1962): \ George Maciunas, \ Yoko Ono, \ Nam June Paik, \ La Monte Young", WHITE),
            (r"`event scores': \ short written instructions, \ anyone may perform them", WHITE),
            (r"Yoko Ono's \textit{Grapefruit} \ (1964): \ a book of instruction pieces", TUNE),
            (r"the line between music, \ art and life deliberately blurred", GREY_A),
        ]
        rows_scene(self, r"happenings and Fluxus", items,
                   "Chance led beyond the concert hall. <bookmark mark='b'/> At Black Mountain College in 1952, Cage staged a simultaneous performance of music, dance, poetry and painting, often called the first happening. <bookmark mark='c'/> From 1962 the Fluxus movement, George Maciunas, Yoko Ono, Nam June Paik, La Monte Young, <bookmark mark='d'/> wrote event scores: short written instructions that anyone could perform. <bookmark mark='e'/> Yoko Ono's book Grapefruit, of 1964, is a collection of such instruction pieces. <bookmark mark='f'/> The line between music, art and everyday life was blurred on purpose.", marks="cdef")
