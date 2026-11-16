from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ form at scale", r"What is known about form, \ and what is not?", extra=((2011, r"the SALAMI annotations"),),
                spoken="Frontier: form at scale")
        self.listeners()
        self.cycles()
        self.machines()
        self.open()

    # ------------------------------------------------------------------
    def listeners(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"local structure is heard at once: \ cadences, \ phrase ends, \ a wrong chord \ (Part 18)", WHITE),
            (r"global structure is heard weakly: \ scrambled pieces are judged nearly as coherent", WHITE),
            (r"Tillmann and Bigand: \ listeners are sensitive mostly to the last few seconds to a minute", WHITE),
            (r"but repetition at large scale is heard: \ a returning theme is recognized after minutes", TUNE),
            (r"form may work through memory for themes, \ not through the key plan", EAR))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what listeners hear", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What do listeners hear? <bookmark mark='a'/> Local structure, at once: cadences, phrase ends, a chord out of "
            "place, as Part 18 found in the brain's responses. <bookmark mark='b'/> Global structure, weakly: pieces "
            "whose sections have been reordered are judged nearly as coherent as the originals. "
            "<bookmark mark='c'/> Barbara Tillmann and Emmanuel Bigand, reviewing these experiments, concluded that "
            "these tasks often reveal stronger local than global effects, rather than a universal one-minute memory limit. "
            "<bookmark mark='d'/> But a returning theme is recognized after minutes, and the recognition is felt. "
            "<bookmark mark='e'/> Perhaps form works on listeners through memory for themes, the stripes in the picture, "
            "more than through the plan of keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cycles(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"European forms are journeys: \ away and back", WHITE),
            (r"Javanese gamelan: \ a cycle marked by the great gong, \ repeated, \ layered, \ sped up and slowed", WHITE),
            (r"a Hindustani raga performance: \ \textit{alap}, \ \textit{jor}, \ \textit{jhala}, \ a slow growth of pulse and density", WHITE),
            (r"a dance-music track: \ a loop, \ with layers added and taken away", WHITE),
            (r"form as a cycle, \ or as a growth, \ not as a return: \ Parts 31 and 40", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"other ways to hold time together", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The forms of this part are journeys, away and back. Not every tradition plans time that way. "
            "<bookmark mark='a'/> In Javanese gamelan, a piece is a cycle marked by the great gong, repeated with layers "
            "of elaboration, sped up and slowed down. <bookmark mark='b'/> One common instrumental Hindustani performance sequence grows: a "
            "free, unmetred opening, then a pulse, then faster and denser playing, then a composition with drums. "
            "<bookmark mark='c'/> A dance-music track is a loop, with layers added and taken away. "
            "<bookmark mark='d'/> Form as a cycle, or as a growth, rather than a return: Parts 34, 36 and 40 take these up, "
            "and they are a reminder that the self-similarity picture shows any of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def machines(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"2011: \ SALAMI: \ over a thousand recordings with structure annotated by experts", WHITE),
            (r"annual comparisons of segmenters: \ boundaries, \ and labels A, \ B, \ A$'$", WHITE),
            (r"two annotators of the same song often disagree: \ the ceiling is not 100", TUNE),
            (r"2018: \ Music Transformer: \ attention over long spans to make generated music repeat itself", WHITE),
            (r"the long-range plan remains an important evaluation challenge; these historical examples do not establish the performance ceiling of current systems", EAR))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what machines do", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Machines are measured on the same task as this part's program. <bookmark mark='a'/> In 2011 the SALAMI "
            "project published structural annotations by experts for well over a thousand recordings, "
            "<bookmark mark='b'/> and segmenters are compared on them every year, both on where the boundaries are and "
            "on which sections are the same. <bookmark mark='c'/> One lesson: two expert annotators of the same song "
            "often disagree, so evaluation depends on annotation choices; disagreement is not a mathematical ceiling on a score against one reference. <bookmark mark='d'/> For writing music, "
            "the 2018 Music Transformer used attention across long spans so that the music it generated would return to "
            "its own material. <bookmark mark='e'/> Even so, the long-range plan, the thing this part is about, is still "
            "where generated music is weakest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"open: \ which levels of form does a listener actually track, \ and for how long?", WHITE),
            (r"open: \ is form a property of the music, \ the listening, \ or the analysis?", WHITE),
            (r"$\bigstar$ \ research problem: \ an experiment that measures memory for themes and memory for keys separately", TUNE))]).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what is still open", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And the questions now. <bookmark mark='a'/> Which levels of form does a listener actually track, and for how "
            "long? <bookmark mark='b'/> Is form a property of the music, of the way it is listened to, or of the "
            "analysis? <bookmark mark='c'/> This part's research problem asks for an experiment that separates memory for "
            "themes from memory for keys, the two candidates for what holds a long piece together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
