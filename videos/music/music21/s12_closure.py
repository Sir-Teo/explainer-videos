from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Closure(SoundScene):
    def construct(self):
        chapter(self, 11, r"Must the ending be home?", r"Do listeners hear where a long piece ends up?", extra=((1987, r"Cook's tonal closure experiment"),))
        self.quiz()
        self.cook()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("closure")
        c = clip("closure.two")
        card = listen_card(r"Two short pieces on the Tune. \ Both begin in C. \ Which one ends in the key it began in, \ A or B?", width=9.6)
        with self.voiceover(
            "Two short pieces built on the Tune. Both begin in C major. Which one ends in the key it began in, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        bars = VGroup()
        for k, key in enumerate("AB"):
            s = strip([0, 8, 16], [r"C", r"to G", r"?"], 24, width=5.2, height=0.5, colors={"C": "#F5C542", "to": "#F472B6", "?": GREY_B}, font_size=22)
            bars.add(VGroup(label(key, font_size=40, color=GREY_A), s).arrange(DOWN, buff=0.3))
        bars.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        self.play(FadeOut(card), FadeIn(bars))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bars[0][0], d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, bars[1][0], d["starts"]["B"], c.duration, buff=0.1)
            pulse(snd, bars, 0.0, c.duration, buff=0.25, color=GREY_B)
        ends = VGroup(label(r"ends in G", font_size=26, color=EAR).next_to(bars[0], DOWN, buff=0.4),
                      label(r"ends in C: \ home", font_size=26, color=TUNE).next_to(bars[1], DOWN, buff=0.4))
        with self.voiceover(
            "B. Both pieces move to G in their middle; B comes back and closes in C, while A closes in G, a full cadence "
            "in the wrong key. These short examples invite a comparison; responses have not been measured here: A sounds finished, but somewhere else."
        ):
            self.play(FadeIn(ends))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cook(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"1987: \ Nicholas Cook rewrote the endings of classical pieces to finish in another key", WHITE),
            (r"listeners, \ trained and untrained, \ rated coherence and completeness", WHITE),
            (r"for pieces under about a minute: \ the home ending preferred", TUNE),
            (r"for longer ones: \ no reliable difference", EAR),
            (r"1992: \ a Mozart movement with its sections rearranged was liked about as well as the original", WHITE),
            (r"so is large-scale form heard, \ or only known?", GREY_A))]).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"how far does the ear reach?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "But does that hold for a whole movement? <bookmark mark='a'/> In 1987 Nicholas Cook took classical pieces and rewrote their endings to finish in a different key from their beginnings. <bookmark mark='b'/> Music students, and listeners without training, rated how complete and coherent each version sounded. <bookmark mark='c'/> For pieces shorter than about a minute, they preferred the version that ended at home. <bookmark mark='d'/> For longer pieces they showed no reliable preference: in that task, ratings did not reliably favor the original endings; this does not directly prove that tonic memory had vanished. <bookmark mark='e'/> In 1992 Michael Karno and Vladimir Konečni rearranged the sections of a Mozart symphony's first movement, and listeners liked the scrambled versions about as well. <bookmark mark='f'/> So is large-scale form something the ear hears, or something the mind knows from the score and from habit? That is the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcdef", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
