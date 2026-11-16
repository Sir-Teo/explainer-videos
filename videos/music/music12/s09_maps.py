from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Maps(SoundScene):
    def construct(self):
        chapter(self, 8, r"Other maps of the octave", r"Must a scale use our twelve notes?")
        self.three()
        self.thirds()
        self.caution()

    # ------------------------------------------------------------------
    def three(self):
        d = load("maps")
        c = clip("maps.four")
        specs = [(r"a major scale", d["major"], (LONG, SHORT, BAD)), (r"Rast, \ a maqam of Arabic music", d["rast"], (LONG, "#C4B5FD", SHORT)),
                 (r"five equal steps: \ a rough proxy for slendro", d["five"], (LONG, SHORT, BAD)), (r"Mayamalavagowla", [100, 300, 100, 200, 100, 300, 100], ("#C4B5FD", LONG, SHORT))]
        rows = VGroup()
        for name, steps, cols in specs:
            rows.add(VGroup(label(name, font_size=26, color=GREY_A), step_bar(steps, width=10.0, height=0.5, colors=cols, font_size=20)).arrange(DOWN, buff=0.15))
        rows.arrange(DOWN, buff=0.45).move_to(UP * 0.3)
        scale = label(r"each bar is one octave; \ the numbers are cents", font_size=22, color=GREY_B).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Everything so far has lived on the twelve notes of a keyboard. Much of the world's music "
            "does not. Here is a first look; later parts go properly into each. <bookmark mark='a'/> A "
            "major scale, for reference: steps of two hundred cents and a hundred. <bookmark mark='b'/> "
            "A quarter-tone teaching approximation to Rast, an important Arabic maqam. Its third note lies between our minor "
            "third and our major third, about three quarters of a tone above the second. No piano key "
            "plays it. <bookmark mark='c'/> Five equal steps of two hundred and forty cents: a rough "
            "stand-in for slendro, one of the two tunings of the Javanese gamelan. <bookmark mark='d'/> "
            "And the south Indian scale from the last chapter. Listen to all four."
        ) as vo:
            self.play(FadeIn(scale), FadeIn(rows[0]))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r) if mark != "a" else Indicate(r[0], color=TUNE), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"four ways to divide an octave", detail=r"Part 7's piano, \ retuned", corner=DL, tag_corner=DR)
            for k, r in enumerate(rows):
                t0 = d["starts"][k]
                cells = r[1].cells
                pulse(snd, r[0], t0, t0 + 0.3 * (len(cells) + 2), buff=0.08)
                for j in range(len(cells)):
                    snd.wait_until(t0 + 0.3 * j)
                    self.play(cells[j].animate(rate_func=there_and_back).shift(UP * 0.12), run_time=0.2)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thirds(self):
        d = load("maps")
        c = clip("maps.thirds")
        card = listen_card(r"Three thirds above the same note. \ One is major, \ one is minor, \ and one is neither. \ Which is neither: \ A, \ B or C?", width=10.0, font_size=26)
        with self.voiceover("The note that no piano has deserves a closer listen. Here are three thirds above the same note. One is major, one is minor, and one is neither. Which is neither: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B", "C"), buff=0.8, width=2.0, height=1.1, font_size=44).move_to(UP * 1.2)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"Part 7's piano, \ retuned", corner=DL, tag_corner=DR)
            for k in range(3):
                pulse(snd, bx[k], d["thirds_starts"][k], d["thirds_starts"][k] + 1.6)
        g = axes([280, 420], [0, 1], x_length=9.0, y_length=0.5, xlabel=r"cents above the lower note", ylabel="", xticks=[300, 350, 400], yticks=[], font_size=22).move_to(DOWN * 1.6)
        marks = VGroup()
        for cents_, nm, col in ((400, r"A: \ major", TUNE), (350, r"B: \ neutral", "#C4B5FD"), (300, r"C: \ minor", SHORT)):
            p = g.ax.c2p(cents_, 0)
            marks.add(VGroup(Line(p, p + UP * 0.8, color=col, stroke_width=5), label(nm, font_size=26, color=col).next_to(p + UP * 0.8, UP, buff=0.1)))
        with self.voiceover(
            "B. It lies halfway between: three hundred and fifty cents, where minor is three hundred and "
            "major four hundred. It is called a neutral third. To an ear raised on keyboards it can sound "
            "out of tune, a major third gone flat. To an ear raised on maqam it is a note in its own "
            "right, a meaningful pitch region, whose intonation can vary by phrase, performer and tradition. Experience shapes tuning judgments alongside auditory constraints, and the "
            "scale you grew up with is the ruler you measure with."
        ):
            self.play(FadeIn(g), FadeIn(marks))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caution(self):
        rows = rows_card([
            (r"maqam", r"a scale is the least of it: \ each maqam has its own paths, \ resting notes and phrases, \\ and its neutral intervals differ a little from Cairo to Aleppo to Istanbul."),
            (r"raga", r"a parent scale says which notes; \ a raga says how to move among them, \\ which to dwell on, \ which to bend, \ and, \ in some traditions, \ time associations."),
            (r"slendro, \ pelog", r"many ensembles have individual tunings. \ Five nearly equal steps, \ or seven unequal ones, \\ fitted to bronze whose overtones are not a string's (Part 9)."),
        ], left=-6.3, text_left=-3.3, top=1.3, step=1.5, name_size=30, text_size=24)
        head = label(r"a scale is only the list of notes", font_size=32, color=TUNE).to_edge(UP, buff=0.45)
        common = label(r"frequent patterns, \ with exceptions: \ the octave, \ a fifth or a fourth, \ and five to seven notes", font_size=28, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A warning before we go on. Those were scales as a keyboard player would hear them: rows of pitches. In their own traditions they are more than that. <bookmark mark='a'/> A maqam is a way of moving through its notes, with its own resting places, and its in-between intervals are tuned a little differently from city to city. <bookmark mark='b'/> A raga has characteristic melodic behaviour and expressive associations; some traditions also associate ragas with times of day. its parent scale is only its list of ingredients. <bookmark mark='c'/> Many gamelans have individual tunings, with intervals and octave stretch varying by ensemble and tradition. Parts 34 to 36 take these traditions on their own terms. <bookmark mark='d'/> For today, notice what they have in common with the white keys. Octave relations, fourths or fifths, and collections of roughly five to seven notes recur in many documented traditions. These are frequent patterns, with exceptions, not laws for every scale. That last fact is the puzzle this part ends on."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(common))
        self.wait(0.4)
        self.clear_scene()
