from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ fugues by machine", r"Can a machine analyse, \ or write, \ a fugue?", extra=((2015, r"computational fugue analysis"),),
                spoken="Frontier: fugues by machine")
        self.analysis()
        self.generation()
        self.open()

    # ------------------------------------------------------------------
    def analysis(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"analysis: \ find every entry of the subject, \ real or tonal, \ altered or not", WHITE),
            (r"then countersubjects, \ episodes, \ cadences, \ pedals", WHITE),
            (r"2015: \ Giraud, \ Groult, \ Levé and colleagues: \ fugues of the \textit{Well-Tempered Clavier} analysed by program", WHITE),
            (r"the hard part: \ deciding which near-copies count as entries, \ as human analysts disagree too", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"fugues analysed by machine", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The tools of this part run both ways. <bookmark mark='a'/> To analyse a fugue, a program must find every "
            "entry of the subject, real or tonal, sometimes with altered notes or a changed ending. "
            "<bookmark mark='b'/> Then the countersubjects, the episodes, the cadences and pedals. "
            "<bookmark mark='c'/> In 2015 a team at Lille, Mathieu Giraud, Richard Groult, Florence Levé and others, "
            "published an analysis of the fugues of the Well-Tempered Clavier by program, compared with the "
            "analyses of human experts. <bookmark mark='d'/> The hard part is not matching notes; it is deciding which "
            "near-copies count as entries, the very question on which human analysts disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def generation(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"rules and search \ (this part): \ correct, \ exhaustive, \ plain", WHITE),
            (r"1980s--90s: \ David Cope's EMI recombines fragments of a composer's own music", WHITE),
            (r"2017--19: \ neural networks trained on Bach's chorales fill in missing voices; \ a 2019 web doodle let millions try", WHITE),
            (r"fugue is harder: \ long-range plans, \ entries, \ keys, \ a shape over minutes", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"fugues written by machine", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And to write one. <bookmark mark='a'/> Rules and search, as in this part, can exhaust the specified finite search space, without guaranteeing full stylistic correctness or musical quality. <bookmark mark='b'/> In the 1980s and 1990s, David Cope's program EMI wrote music in the style of Bach and others by recombining fragments of their own works. <bookmark mark='c'/> More recently, neural networks trained on Bach's chorales learned to fill in missing voices, and in 2019 a web page let millions of people write a melody and hear it harmonized in his style. <bookmark mark='d'/> Fugue is harder than chorale: it needs a plan over minutes, entries placed in keys, tension built and released. Models that write convincing local counterpoint still struggle with that long-range shape, which is Part 21's subject: form."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"open: \ can listeners hear an inverted or retrograde subject as the same theme?", WHITE),
            (r"experiments suggest: \ inversions sometimes, \ retrogrades rarely, \ without training", GREY_A),
            (r"open: \ how much of a fugue's structure does the ear follow, \ and how much is for the eye?", WHITE),
            (r"$\bigstar$ \ research problem: \ an experiment that tells the two apart", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what is still open", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And the old question that canons raise. <bookmark mark='a'/> When a subject is turned upside down or backwards, does the listener hear the same theme? <bookmark mark='b'/> Experiments suggest that recognition of inversions and retrogrades depends on task, familiarity, contour and training; retrogrades are often difficult, as chapter three's question may have shown you. <bookmark mark='c'/> So how much of a fugue's structure is for the ear, and how much for the eye of a reader of the score? <bookmark mark='d'/> Designing an experiment that separates the two is this part's research problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
