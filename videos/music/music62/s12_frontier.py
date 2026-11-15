from __future__ import annotations

from videos.music.music62.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ expressive and non-Western meter", r"Whose beat is the machine listening for?")
        self.meter()
        self.joint()
        self.realtime()
        self.problem()

    # ------------------------------------------------------------------
    def meter(self):
        items = [
            (r"most annotated data: \ Western popular music, \ 4/4, \ a steady tempo", WHITE),
            (r"Part 34's tala, \ Part 37's timelines, \ Balkan 7/8: \ cycles of unequal beats, \ which a 4/4 tracker misreads", WHITE),
            (r"datasets of other traditions exist \ (Carnatic, \ Hindustani, \ Turkish makam, \ Afro-Cuban) \ and change the picture", WHITE),
            (r"expressive music: \ a Chopin nocturne's tempo moves every bar; \ beat trackers still fail there \ (Chapter 3)", WHITE),
            (r"the beat a machine hears is the beat its training data annotated", TUNE),
        ]
        rows_scene(self, r"whose meter? \ (verify the latest)", items,
                   "Two frontiers. The first is meter itself. <bookmark mark='b'/> Most annotated data is Western popular music in "
                   "four-four at a steady tempo. <bookmark mark='c'/> Part 34's tala, Part 37's timelines and Balkan seven-eight "
                   "are cycles of unequal beats, which a four-four tracker misreads. <bookmark mark='d'/> Datasets of other "
                   "traditions, Carnatic, Hindustani, Turkish makam, Afro-Cuban, exist and change the picture. "
                   "<bookmark mark='e'/> And in expressive music, where a nocturne's tempo moves every bar, beat trackers still fail, "
                   "as Chapter 3 found. <bookmark mark='f'/> The beat a machine hears is the beat its training data annotated.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def joint(self):
        items = [
            (r"beats, \ downbeats, \ tempo, \ chords and sections depend on each other", WHITE),
            (r"joint models predict them together, \ each helping the others: \ downbeats where chords change, \ sections at downbeats", WHITE),
            (r"foundation models trained on large unlabelled collections now supply features for all of these tasks \ (verify)", WHITE),
            (r"Monochord's renders can test them where the answer is exact", TUNE),
        ]
        rows_scene(self, r"joint models", items,
                   "The second is doing it all at once. <bookmark mark='b'/> Beats, downbeats, tempo, chords and sections depend on "
                   "each other. <bookmark mark='c'/> Joint models predict them together, each helping the others: downbeats where "
                   "chords change, sections at downbeats. <bookmark mark='d'/> And models trained on large unlabelled collections "
                   "now supply features for all these tasks; check the current results. <bookmark mark='e'/> Monochord's renders "
                   "can test them where the answer is exact.", marks="bcde")

    # ------------------------------------------------------------------
    def realtime(self):
        items = [
            (r"live listening is harder than listening to a file: \ no future frames, \ a deadline every few milliseconds", WHITE),
            (r"a phone must track beats and chords as the music plays, \ for a light show, \ a game, \ a practice app", WHITE),
            (r"causal models, \ small enough to run on the device, \ with their latency measured, \ not assumed", WHITE),
            (r"the measure that matters live is not F-measure but how late the answer comes", TUNE),
        ]
        rows_scene(self, r"listening live", items,
                   "A third frontier is time itself. <bookmark mark='b'/> Live listening is harder than listening to a file: there "
                   "are no future frames, and a deadline every few milliseconds. <bookmark mark='c'/> A phone must track beats and "
                   "chords as the music plays, for a light show, a game or a practice app. <bookmark mark='d'/> That needs causal "
                   "models small enough to run on the device, with their latency measured, not assumed. <bookmark mark='e'/> Live, "
                   "the measure that matters is not the F-measure, but how late the answer comes.", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"an accompanist must play with a note, \ not after it: \ it has to predict", WHITE),
            (r"model a performer's timing: \ phrase arches, \ held phrase ends, \ the habits of Part 43's expressive performer", WHITE),
            (r"predict each next beat's time from the past, \ with an uncertainty, \ and play there", WHITE),
            (r"$\bigstar$ \ research problem: \ how close to a human accompanist can a predictive follower play, \ and on what music does it fail?", EAR),
            (r"an answer would decide when machines can join live ensembles", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on, from Chapter 8. <bookmark mark='a'/> An accompanist must play with a note, not "
            "after it: it has to predict. <bookmark mark='b'/> Model a performer's timing: phrase arches, held phrase ends, the "
            "habits of Part 43's expressive performer. <bookmark mark='c'/> Predict each next beat's time from the past, with an "
            "uncertainty, and play there. <bookmark mark='d'/> The question: how close to a human accompanist can a predictive "
            "follower play, and on what music does it fail? <bookmark mark='e'/> An answer would decide when machines can join "
            "live ensembles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
