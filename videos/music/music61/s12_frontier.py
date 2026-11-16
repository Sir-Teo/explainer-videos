from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ many instruments, \ and scores", r"Can a machine transcribe a band?")
        self.many()
        self.scores()
        self.problem()

    # ------------------------------------------------------------------
    def many(self):
        items = [
            (r"MT3 \ (Gardner et al., \ 2022): \ a transformer reads a spectrogram and writes note events for every instrument, \ like a translation", WHITE),
            (r"Basic Pitch \ (2022): \ a compact instrument-agnostic transcriber, with limits on mixtures, range and playing conditions, \ light enough for a phone", WHITE),
            (r"multi-instrument results on real recordings still fall well short of solo piano \ (verify current results)", WHITE),
            (r"the bottleneck is again the answer key: \ real bands are rarely recorded with their exact notes", WHITE),
            (r"synthetic data, \ like Monochord's, \ helps; \ the gap between rendered and real sound is the open question", TUNE),
        ]
        rows_scene(self, r"many instruments \ (dated)", items,
                   "Two frontiers. The first is the whole band. <bookmark mark='b'/> In 2022 MT3, from Josh Gardner and "
                   "colleagues, had a transformer read a spectrogram and write note events for every instrument, like a "
                   "translation. <bookmark mark='c'/> The same year Basic Pitch offered a compact instrument-agnostic transcriber, with limits on mixtures, range and playing conditions, light "
                   "enough for a phone. <bookmark mark='d'/> On real recordings of many instruments, results still fall well "
                   "short of solo piano; check the latest numbers, which move each year. <bookmark mark='e'/> The bottleneck is "
                   "again the answer key: real bands are rarely recorded with their exact notes. <bookmark mark='f'/> Synthetic "
                   "data like Monochord's helps, and the gap between rendered and real sound is the open question.", marks="bcdef")

    # ------------------------------------------------------------------
    def scores(self):
        items = [
            (r"a note list is not a score: \ a score has a meter, \ bars, \ voices, \ a key and spelled notes", WHITE),
            (r"models now write scores directly, \ in score languages, \ from audio or from note lists", WHITE),
            (r"a score's errors are not a note list's: \ one wrong tempo misplaces every barline", WHITE),
            (r"evaluation is unsettled: \ how far is one score from another, \ as a musician would judge it?", TUNE),
        ]
        rows_scene(self, r"scores", items,
                   "The second is the score itself. <bookmark mark='b'/> A note list is not a score: a score has a meter, bars, "
                   "voices, a key and spelled notes. <bookmark mark='c'/> Models now write scores directly, in score languages, "
                   "from audio or from note lists. <bookmark mark='d'/> And a score's errors are not a note list's: one wrong "
                   "tempo misplaces every barline. <bookmark mark='e'/> So evaluation is unsettled: how far is one score from "
                   "another, as a musician would judge it?", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"render pieces on many instruments, \ with exact answer keys, \ and hold some timbres out", WHITE),
            (r"have a transcriber report, \ for every note, \ the probability that it is right", WHITE),
            (r"check those probabilities on the held-out timbres: \ are notes it calls 90\% sure right 90\% of the time?", WHITE),
            (r"$\bigstar$ \ research problem: \ can a transcriber stay calibrated on a timbre it has never heard?", EAR),
            (r"an answer would tell a musician which notes of a machine's transcription to check", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on, from Chapter 7. <bookmark mark='a'/> Render pieces on many instruments, with exact "
            "answer keys, and hold some timbres out. <bookmark mark='b'/> Have a transcriber report, for every note, the "
            "probability that it is right. <bookmark mark='c'/> Check those probabilities on the held-out timbres: are notes it "
            "calls ninety percent sure right ninety percent of the time? <bookmark mark='d'/> The question: can a transcriber stay "
            "calibrated on a timbre it has never heard? <bookmark mark='e'/> An answer would tell a musician which notes of a "
            "machine's transcription to check."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
