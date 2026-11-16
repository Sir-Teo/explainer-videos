from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ payout reform and training data", r"Can a court be told the odds?")
        self.payout()
        self.training()
        self.problem()

    # ------------------------------------------------------------------
    def payout(self):
        items = [
            (r"which division of the pool is fair? \ economists model it; \ services test it on their own data, \ rarely published", WHITE),
            (r"listeners respond: \ change how a stream pays, \ and what is made, \ and how it is played, \ changes", WHITE),
            (r"fraud is an arms race: \ farms of devices, \ generated tracks uploaded by the thousand", WHITE),
            (r"proposals: \ a per-listener floor, \ weights for active listening, \ minimum thresholds, \ public data", WHITE),
            (r"the measurement problems are Part 67's: \ what is fair, \ to whom, \ and how would we know?", TUNE),
        ]
        rows_scene(self, r"payout reform", items,
                   "Two frontiers. The first is how the pool is divided. <bookmark mark='b'/> Which division is fair? Economists "
                   "model it, and the services test it on their own data, which they rarely publish. <bookmark mark='c'/> And "
                   "listeners and musicians respond: change how a stream pays, and what is made, and how it is played, changes. "
                   "<bookmark mark='d'/> Fraud is an arms race, now with generated tracks uploaded by the thousand. "
                   "<bookmark mark='e'/> The proposals: a floor per listener, extra weight for active listening, minimum "
                   "thresholds, public data. <bookmark mark='f'/> The measurement problems are Part 67's: what is fair, to whom, "
                   "and how would we know?", marks="bcdef")

    # ------------------------------------------------------------------
    def training(self):
        items = [
            (r"licensing training data: \ who is paid, \ how much, \ and for which songs a model actually used?", WHITE),
            (r"attribution: \ can we measure how much one recording influenced one output? \ (influence functions; \ an open problem)", WHITE),
            (r"memorization: \ how often does a model reproduce its training data, \ phrase for phrase? \ (Part 65's plagiarism tests)", WHITE),
            (r"detection: \ watermarks and classifiers that tell generated audio from recorded", WHITE),
            (r"every one of these is a statistics problem with money attached", TUNE),
        ]
        rows_scene(self, r"training data", items,
                   "The second is training data. <bookmark mark='b'/> If models are licensed, who is paid, how much, and for which "
                   "songs a model actually used? <bookmark mark='c'/> Attribution: can we measure how much one recording influenced "
                   "one output? Influence functions try; it is an open problem. <bookmark mark='d'/> Memorization: how often does a "
                   "model reproduce its training data, phrase for phrase? Part 65's plagiarism tests ask exactly that. "
                   "<bookmark mark='e'/> Detection: watermarks and classifiers to tell generated audio from recorded. "
                   "<bookmark mark='f'/> Every one of these is a statistics problem with money attached.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"train melody models on large corpora of songs, \ with their dates, \ and hold out the songs at issue", WHITE),
            (r"for a disputed phrase, \ compute the chance it arises independently, \ given everything written before it", WHITE),
            (r"check the models' calibration on pairs known to be independent, \ and pairs known to be copied", WHITE),
            (r"$\bigstar$ \ research problem: \ can a model give a court a calibrated probability that a shared phrase arose by chance?", EAR),
            (r"an answer would add testable statistical evidence alongside musicological analysis; a collision probability is not the posterior probability of copying", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on, from Chapter 9. <bookmark mark='a'/> Train melody models on large corpora of songs, with their dates, holding out the songs at issue. <bookmark mark='b'/> For a disputed phrase, compute the chance it would arise independently, given everything written before it. <bookmark mark='c'/> Check the models' calibration on pairs known to be independent and pairs known to be copied. <bookmark mark='d'/> The question: can a model give a court a calibrated probability that a shared phrase arose by chance? <bookmark mark='e'/> An answer would add testable statistical evidence alongside musicological analysis; a collision probability is not the posterior probability of copying."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
