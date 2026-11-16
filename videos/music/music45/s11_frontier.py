from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ machines that hear scenes", r"Do deep networks hear the way we do?")
        self.networks()
        self.separation()
        self.hearing()
        self.problem()

    # ------------------------------------------------------------------
    def networks(self):
        items = [
            (r"Kell and colleagues \ (2018): \ a deep network trained to recognise words and music genres in noise", WHITE),
            (r"its layers predicted responses in human auditory cortex, \ early layers primary cortex, \ later layers beyond", WHITE),
            (r"networks trained on natural sounds show some human illusions, \ and miss others", WHITE),
            (r"a model that matches the brain is a hypothesis about how it works, \ testable with new sounds", TUNE),
            (r"`model metamers': \ sounds a network treats as identical, \ which people may not", GREY_A),
        ]
        rows_scene(self, r"deep networks as models of hearing", items,
                   "The frontier asks whether machines hear scenes as we do. <bookmark mark='b'/> In 2018 Alexander Kell, Josh "
                   "McDermott and colleagues trained a deep network to recognise words and musical genres in noise, "
                   "<bookmark mark='c'/> and its layers predicted responses in human auditory cortex: early layers the primary "
                   "cortex, later layers the regions beyond. <bookmark mark='d'/> Networks trained on natural sounds show some "
                   "human illusions and miss others. <bookmark mark='e'/> A model that matches the brain is a hypothesis about "
                   "how it works, testable with new sounds, <bookmark mark='f'/> for example model metamers: sounds a network "
                   "treats as identical, which people may not.", marks="bcdef")

    # ------------------------------------------------------------------
    def separation(self):
        items = [
            (r"source separation: \ machines that undo the mixture, \ voice from band, \ violin from piano", WHITE),
            (r"learned grouping cues may overlap with human cues", WHITE),
            (r"a separated stem is the machine's scene analysis, \ written out as audio \ (Part 64)", WHITE),
            (r"whether they separate where people do, \ and fail where people fail, \ is open", TUNE),
            (r"the scale illusion is a test case: \ which melodies would a network report?", GREY_A),
        ]
        rows_scene(self, r"machines that separate", items,
                   "A related frontier is source separation. <bookmark mark='b'/> Machines now undo the mixture: voice from band, "
                   "violin from piano, <bookmark mark='c'/> using learned cues that may overlap with human grouping cues, without assuming the same internal mechanism. "
                   "<bookmark mark='d'/> A separated stem is the machine's scene analysis, written out as audio, Part 64's "
                   "subject. <bookmark mark='e'/> Whether they separate where people do, and fail where people fail, is open. "
                   "<bookmark mark='f'/> The scale illusion is a test case: which melodies would a network report?",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take the classic grouping demonstrations: \ streaming, \ interleaving, \ mistuning, \ continuity, \ the scale illusion", WHITE),
            (r"ask a trained separation or recognition network what it hears in each, \ by reading out its streams", WHITE),
            (r"compare its boundaries with van Noorden's and its answers with listeners'", WHITE),
            (r"$\bigstar$ \ research problem: \ do networks trained on natural sound reproduce human streaming boundaries?", EAR),
            (r"if yes, \ the boundaries follow from the statistics of natural sound; \ if not, \ something else shapes them", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Take the classic demonstrations of this part: streaming, "
            "interleaving, mistuning, continuity, the scale illusion. <bookmark mark='b'/> Ask a trained network what it "
            "hears in each, by reading out the streams it separates. <bookmark mark='c'/> Compare its boundaries with van "
            "Noorden's, and its answers with listeners'. <bookmark mark='d'/> Do networks trained on natural sound reproduce "
            "human streaming boundaries? <bookmark mark='e'/> If they do, the boundaries may follow from the statistics of "
            "natural sound; if not, something else shapes them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hearing(self):
        items = [
            (r"the cocktail party problem: \ following one voice among many \ (Colin Cherry, \ 1953)", WHITE),
            (r"with hearing loss or a cochlear implant, \ scene analysis fails first: \ sounds are heard but not separated", WHITE),
            (r"implants carry only a few channels: \ pitch and timbre cues blur, \ so streams merge", WHITE),
            (r"hearing aids now try to separate sources for the listener, \ with the methods of Part 64", TUNE),
            (r"music is often the hardest test for them: \ many sources, \ all wanted", GREY_A),
        ]
        rows_scene(self, r"when scene analysis fails", items,
                   "Scene analysis also matters when it fails. <bookmark mark='b'/> Colin Cherry named the cocktail party problem in 1953: following one voice among many. <bookmark mark='c'/> With hearing loss or a cochlear implant, difficulty separating sources can be a major challenge, alongside reduced audibility and spectral or temporal resolution. <bookmark mark='d'/> Implants carry only a few channels, so pitch and timbre cues blur and streams merge. <bookmark mark='e'/> Hearing aids now try to separate sources for the listener, with the methods of Part 64, <bookmark mark='f'/> and music is often their hardest test: many sources, all of them wanted.", marks="bcdef")
