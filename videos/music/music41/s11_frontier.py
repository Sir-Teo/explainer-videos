from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ timbre measured", r"What is timbre, \ in numbers?")
        self.space()
        self.mapit()
        self.identity()
        self.treatises()
        self.machines()
        self.problem()

    # ------------------------------------------------------------------
    def space(self):
        items = [
            (r"timbre: \ what distinguishes two sounds of the same pitch, \ loudness and duration \ (a definition by elimination)", WHITE),
            (r"John Grey \ (1977) \ and Stephen McAdams and colleagues \ (1995): \ listeners rate how different pairs of sounds are", WHITE),
            (r"multidimensional scaling turns the ratings into a map: \ a `timbre space'", WHITE),
            (r"its axes correlate with the attack time, \ the spectral centroid, \ and how the spectrum changes", TUNE),
            (r"Part 45 builds a timbre space from Monochord's own instruments", GREY_A),
        ]
        rows_scene(self, r"timbre space", items,
                   "What is timbre? The standard definition is by elimination: what distinguishes two sounds of the same pitch, "
                   "loudness and duration. <bookmark mark='b'/> In 1977 John Grey, and later Stephen McAdams and colleagues in "
                   "1995, had listeners rate how different pairs of instrument sounds were, <bookmark mark='c'/> and turned the "
                   "ratings into a map by multidimensional scaling: a timbre space. <bookmark mark='d'/> Its axes correlate with "
                   "the attack time, the spectral centroid, and how the spectrum changes over a note. <bookmark mark='e'/> Part 45 "
                   "builds a timbre space from Monochord's own instruments.", marks="bcde")

    # ------------------------------------------------------------------
    def treatises(self):
        items = [
            (r"Berlioz \ (1844), \ Rimsky-Korsakov \ (1913), \ Adler \ (1982): \ orchestration taught by examples and rules of thumb", WHITE),
            (r"a project at McGill, \ `Analysis, \ Creation and Teaching of Orchestration', \ maps their claims to perception", WHITE),
            (r"blend, \ segregation into layers, \ and contrast: \ tested with listeners and scores", WHITE),
            (r"the treatises are hypotheses about hearing; \ some hold, \ some are style", TUNE),
            (r"a theory of orchestration grounded in perception is still being built", GREY_A),
        ]
        rows_scene(self, r"the treatises, tested", items,
                   "The orchestration treatises, Berlioz's of 1844, Rimsky-Korsakov's of 1913 and Samuel Adler's of 1982, teach "
                   "by examples and rules of thumb. <bookmark mark='b'/> A project led from McGill University, Analysis, Creation "
                   "and Teaching of Orchestration, maps their claims to perception, <bookmark mark='c'/> testing blend, the "
                   "separation of an orchestra into layers, and contrast, with listeners and scores. <bookmark mark='d'/> The "
                   "treatises turn out to be hypotheses about hearing: some hold, and some are style. <bookmark mark='e'/> A "
                   "theory of orchestration grounded in perception is still being built.", marks="bcde")

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"computer-aided orchestration searches sample libraries for combinations that match a target \ (chapter 9)", WHITE),
            (r"learned models now propose orchestrations of piano scores", WHITE),
            (r"evaluating them is hard: \ there is no single right orchestration", WHITE),
            (r"what counts as success: \ a target matched, \ an expert's preference, \ a performance that works", TUNE),
            (r"Part 65 returns to machines that compose", GREY_A),
        ]
        rows_scene(self, r"machines", items,
                   "Machines have joined in. <bookmark mark='b'/> Computer-aided orchestration searches sample libraries for "
                   "combinations that match a target, as chapter nine did in miniature. <bookmark mark='c'/> Learned models now "
                   "propose orchestrations of piano scores. <bookmark mark='d'/> Judging them is hard, because there is no single "
                   "right orchestration. <bookmark mark='e'/> Success might mean a target matched, an expert's preference, or a "
                   "performance that works. <bookmark mark='f'/> Part 65 returns to machines that compose.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"collect orchestral excerpts with scores and recordings, \ and listeners' judgements of blend and layering", WHITE),
            (r"predict those judgements from the score and the instruments' spectra: \ harmonicity, \ onsets, \ brightness", WHITE),
            (r"test the predictions on new excerpts and new listeners", WHITE),
            (r"$\bigstar$ \ research problem: \ can blend and layering be predicted from the score alone?", EAR),
            (r"an answer would turn the treatises' rules into a tested theory", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Collect orchestral excerpts with scores and recordings, and listeners' "
            "judgements of what blends and what forms separate layers. <bookmark mark='b'/> Predict those judgements from "
            "the score and the instruments' spectra: harmonicity, onsets, brightness. <bookmark mark='c'/> Test the "
            "predictions on new excerpts and new listeners. <bookmark mark='d'/> Can blend and layering be predicted from the "
            "score alone? <bookmark mark='e'/> An answer would turn the treatises' rules into a tested theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mapit(self):
        d = load("space")
        pts = d["points"]
        x0, y0, W, Hh = -4.5, -2.2, 9.0, 4.2
        def X(ms):
            return x0 + W * (np.log10(ms) - np.log10(0.5)) / (np.log10(100) - np.log10(0.5))
        cmax = max(p["centroid"] for p in pts.values())
        def Y(c):
            return y0 + Hh * c / (cmax * 1.1)
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + Hh, 0], color=GREY_B))
        xl = label(r"attack time \ (ms, \ logarithmic)", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.4, 0])
        yl = label(r"brightness at C4 \ (Hz)", font_size=16, color=GREY_A).move_to([x0 - 0.2, y0 + Hh + 0.3, 0])
        dots = VGroup()
        for name, p in pts.items():
            pos = [X(max(p["attack_ms"], 0.6)), Y(p["centroid"]), 0]
            dots.add(VGroup(Dot(pos, radius=0.09, color=TUNE), label(name.replace(" p", " (soft)").replace(" f", " (loud)"), font_size=14, color=WHITE).next_to(pos, RIGHT, buff=0.1)))
        head = label(r"our orchestra in two dimensions of timbre", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is our own orchestra placed in two of those dimensions: attack time across, brightness up. "
            "<bookmark mark='a'/> The struck instruments, celesta and harp, sit far to the left with near-instant attacks; "
            "the clarinet sits high, bright with its odd harmonics; the soft and loud trumpet are far apart vertically, the "
            "same instrument in two places. A real timbre space, built from listeners' judgements, needs a third dimension "
            "at least, and that is Part 45's task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def identity(self):
        items = [
            (r"we recognise instruments, \ and voices, \ in a fraction of a second", WHITE),
            (r"recognition uses the attack, \ the spectrum, \ and how both change with pitch and loudness", WHITE),
            (r"an instrument is not one timbre but a family of them across its range", WHITE),
            (r"which is why our one-spectrum orchestra sounds alike from note to note", TUNE),
            (r"Part 52 synthesises instruments whose spectra change as real ones do", GREY_A),
        ]
        rows_scene(self, r"timbre as identity", items,
                   "Timbre is also identity. <bookmark mark='b'/> We recognise instruments and voices in a fraction of a second, <bookmark mark='c'/> using the attack, the spectrum, and how both change with pitch and loudness. <bookmark mark='d'/> An instrument is not one timbre but a family of them across its range, <bookmark mark='e'/> which is why our one-spectrum orchestra sounds alike from note to note. <bookmark mark='f'/> Part 52 synthesises instruments whose spectra change as real ones do.", marks="cdef")
