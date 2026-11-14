from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ attribution and ficta by machine", r"What would a trustworthy attribution test look like?")
        self.projects()
        self.pitfalls()
        self.problem()

    # ------------------------------------------------------------------
    def projects(self):
        items = [
            (r"the Josquin Research Project: \ hundreds of works by Josquin and his contemporaries, \ encoded and searchable", WHITE),
            (r"each work tagged by how secure its attribution is", WHITE),
            (r"classifiers trained on the secure works, \ then asked about the doubtful ones", WHITE),
            (r"features from counterpoint: \ cadences, \ dissonance figures, \ voice ranges, \ rhythmic habits", TUNE),
            (r"their verdicts are evidence to weigh with the sources, \ not a ruling", GREY_A),
        ]
        rows_scene(self, r"attribution by machine", items,
                   "Attribution by computer is now a research field. <bookmark mark='b'/> The Josquin Research Project at "
                   "Stanford has encoded hundreds of works by Josquin and his contemporaries, searchable note by note, "
                   "<bookmark mark='c'/> with each work tagged by how secure its attribution is. <bookmark mark='d'/> "
                   "Researchers train classifiers on the secure works and ask them about the doubtful ones, "
                   "<bookmark mark='e'/> with features drawn from counterpoint: how cadences are approached, which "
                   "dissonance figures appear, how the voices are spaced, which rhythms recur. <bookmark mark='f'/> The "
                   "answers are evidence to be weighed with the manuscripts and prints, not a ruling.")

    # ------------------------------------------------------------------
    def pitfalls(self):
        items = [
            (r"confounds: \ genre, \ date, \ number of voices, \ editor, \ encoder all leave fingerprints", WHITE),
            (r"chapter 7's 95 in 100 compared Masses with madrigals: \ the easy, \ wrong question", EAR),
            (r"circularity: \ a wrong attribution in the training set teaches the wrong style", WHITE),
            (r"small samples: \ a few pieces either way change the answer", WHITE),
            (r"the fair test holds everything fixed except the composer", TUNE),
        ]
        rows_scene(self, r"how such tests fail", items,
                   "Such tests fail in predictable ways. <bookmark mark='b'/> Genre, date, the number of voices, the editor "
                   "and the encoder all leave fingerprints, and a classifier will happily learn them instead of the "
                   "composer. <bookmark mark='c'/> Chapter seven's ninety-five in a hundred compared Masses with madrigals, "
                   "which is the easy and wrong question. <bookmark mark='d'/> Training on a work that is wrongly "
                   "attributed teaches the test the wrong style. <bookmark mark='e'/> And with a few dozen pieces, a few "
                   "pieces either way change the verdict. <bookmark mark='f'/> A fair test holds everything fixed except "
                   "the composer, which for this repertory is hard: the same genre, the same decade, the same kind of "
                   "source, and enough pieces to measure the error.")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"ficta by machine: \ learn from editions where editors added accidentals, \ predict them in new music", WHITE),
            (r"the target is not one right answer: \ editors disagree, \ and the disagreement is data", WHITE),
            (r"$\bigstar$ \ research problem: \ an attribution test held out by source", EAR),
            (r"train on pieces from some manuscripts and prints, \ test on pieces from others", WHITE),
            (r"if accuracy collapses, \ the test was recognizing scribes, \ not composers", TUNE),
        ])
        head = label(r"two problems", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Two open problems. <bookmark mark='a'/> The first is Part 23's: learn where editors add accidentals, and "
            "predict them in music nobody has edited. <bookmark mark='b'/> The target is not a single right answer, "
            "because editors disagree, and their disagreement is itself data. <bookmark mark='c'/> The second is this "
            "part's research problem: build an attribution test held out by source. <bookmark mark='d'/> Train on pieces "
            "from some manuscripts and prints and test on pieces from others. <bookmark mark='e'/> If the accuracy "
            "collapses, the test was recognizing scribes and printers, not composers."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
