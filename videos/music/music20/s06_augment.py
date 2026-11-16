from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Augment(SoundScene):
    def construct(self):
        chapter(self, 5, r"Slower, and in riddles", r"What else can a canon change?", extra=((1490, r"Ockeghem's \textit{Missa prolationum}"),))
        self.hear()
        self.mensuration()
        self.riddles()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("augment")
        c = clip("augment.pair")
        g = voices_roll(d["lines"], width=11.0, height=3.2, total=16.0).move_to(DOWN * 0.3)
        head = label(r"augmentation: \ the phrase against itself, \ twice as slow, \ two octaves down", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        f = d["faults"]
        with self.voiceover(
            "A canon can also change speed. In augmentation the follower plays every note twice as long; in "
            "diminution, half as long. Here the Tune's first phrase is sung twice in the upper voice, while the bass "
            "sings it once, twice as slowly."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"the phrase, \ and the phrase in augmentation", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g, d["lines"])
            self.add(cursor(snd, g, 0.0))
        cap = label(rf"{f['dissonant']} of the {f['beats']} strong beats clash: \ the Tune was not written for this", font_size=24, color=EAR).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"It nearly works. On {say(f['dissonant'])} of the {say(f['beats'])} strong beats the two clash, because the "
            "Tune was not designed for it: when the fast voice moves to A, the slow one is still on G. Bach's subjects "
            "in The Art of Fugue were designed so that they would fit against their own augmentations and inversions, "
            "and he wrote canons of exactly this kind into it."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mensuration(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"fifteenth-century notation: \ the same notes could be read in different metres", WHITE),
            (r"a mensuration canon: \ one line, \ sung by several voices at once, \ each reading it at its own speed", WHITE),
            (r"Ockeghem's \textit{Missa prolationum}: \ a whole Mass built of such canons", WHITE),
            (r"one written line, \ several heard: \ composition as a puzzle in time", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"mensuration canons", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "This idea is old. <bookmark mark='a'/> In fifteenth-century notation, the same written notes could be "
            "read in different metres, depending on a sign at the start. <bookmark mark='b'/> So composers wrote "
            "mensuration canons: a single line, sung by several voices at once, each reading it at its own speed, the "
            "slow voices spreading the tune out under the fast ones. <bookmark mark='c'/> Johannes Ockeghem's Missa "
            "prolationum, from late in the fifteenth century, builds a whole Mass from such canons, at different "
            "intervals as well as different speeds. <bookmark mark='d'/> One line written, several heard: composition "
            "as a puzzle in time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def riddles(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"a puzzle canon: \ one line printed, \ the rest left to the reader", WHITE),
            (r"the clues: \ a sign where the second voice enters, \ a clef upside down, \ a motto", WHITE),
            (r"\textit{Quaerendo invenietis}: \ `seek and you shall find'", TUNE),
            (r"to solve one: \ try every entry, \ interval and form, \ and keep what fits", WHITE),
            (r"which is a search, \ like the solver's", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"canons as riddles", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Bach's canons in the Musical Offering continue this tradition of puzzles. <bookmark mark='a'/> Some puzzle canons leave a following voice to be inferred from the printed material. <bookmark mark='b'/> The clues are a sign where another voice enters, perhaps a clef printed upside down, or a Latin motto. <bookmark mark='c'/> Over one of them Bach wrote: quaerendo invenietis, seek and you shall find. <bookmark mark='d'/> To solve such a riddle, you try every entry point, every interval and selected transformations and rhythmic proportions, and check the proposed solutions against stylistic constraints. <bookmark mark='e'/> That is exactly a search over the possibilities, the kind the canon solver does. Riddle canons have more than one solution surprisingly often, and solvers since Bach's pupils have argued over which he meant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
