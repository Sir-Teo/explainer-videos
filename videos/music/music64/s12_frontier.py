from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ generative and query-based separation", r"Can a separator invent what the mixture hid?")
        self.generative()
        self.query()
        self.problem()

    # ------------------------------------------------------------------
    def generative(self):
        items = [
            (r"a mask can only scale what the mixture contains; \ where a voice was buried, \ nothing is left to scale", WHITE),
            (r"generative separators model what a source sounds like, \ and fill in what was hidden \ (diffusion and token models; \ verify)", WHITE),
            (r"they can sound cleaner than any mask, \ and can also invent: \ a plausible note that was never sung", WHITE),
            (r"for restoration that is a question of honesty: \ which parts of the result were recorded?", TUNE),
        ]
        rows_scene(self, r"generative separation", items,
                   "Two frontiers. The first: a mask can only scale what the mixture contains, and where a voice was buried "
                   "there is nothing left to scale. <bookmark mark='b'/> Generative separators model what a source sounds like and "
                   "fill in what was hidden, with the diffusion and token models of Part 66; check the latest. "
                   "<bookmark mark='c'/> They can sound cleaner than any mask, and they can also invent: a plausible note that was "
                   "never sung. <bookmark mark='d'/> For restoration that is a question of honesty: which parts of the result were "
                   "recorded?", marks="bcd")

    # ------------------------------------------------------------------
    def query(self):
        items = [
            (r"fixed stems are a convention: \ vocals, \ bass, \ drums, \ other", WHITE),
            (r"query-based separation: \ `the saxophone', \ or an example of it, \ or a sentence, \ names the source to extract", WHITE),
            (r"metrics that track perception: \ SDR disagrees with listeners \ (Chapter 9); \ learned and listening-test measures are being built", WHITE),
            (r"Part 67's question again: \ how do we know a separation is good?", TUNE),
        ]
        rows_scene(self, r"query-based separation, \ and better metrics", items,
                   "The second: fixed stems are a convention. <bookmark mark='b'/> Query-based separation lets a word, an example or "
                   "a sentence name the source to extract: the saxophone, or the second guitar. <bookmark mark='c'/> And metrics that "
                   "track perception are needed, since SDR disagrees with listeners, as Chapter 9 heard; learned and listening-test "
                   "measures are being built. <bookmark mark='d'/> It is Part 67's question again: how do we know a separation is "
                   "good?", marks="bcd")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"render mixtures whose stems are known, \ on many instruments and rooms \ (Monochord can)", WHITE),
            (r"run listening tests: \ which of two separations is closer to the true stem?", WHITE),
            (r"fit a metric to the listeners, \ and test it on separators it never saw", WHITE),
            (r"$\bigstar$ \ research problem: \ can a metric rank separators as listeners do, \ including generative ones that invent?", EAR),
            (r"an answer would decide which separators are actually better", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Render mixtures whose stems are known, on many instruments "
            "and in many rooms, as Monochord can. <bookmark mark='b'/> Run listening tests: which of two separations is closer "
            "to the true stem? <bookmark mark='c'/> Fit a metric to the listeners, and test it on separators it never saw. "
            "<bookmark mark='d'/> The question: can a metric rank separators as listeners do, including generative ones that "
            "invent? <bookmark mark='e'/> An answer would decide which separators are actually better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
