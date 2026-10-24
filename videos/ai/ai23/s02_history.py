from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, PART, SND_C, TEXT_C

SPEAK_C = C.MODEL_Q

# the time axis: 1935-2010 compressed, 2010-2027 stretched (where the milestones crowd)
X0, XB, X1 = -4.4, 0.9, 6.5


def tx(year: float) -> float:
    if year <= 2010:
        return X0 + (XB - X0) * (year - 1935) / (2010 - 1935)
    return XB + (X1 - XB) * (year - 2010) / (2027 - 2010)


LANES = [  # name, colour, y, events (year, label, side: 1 above / -1 below)
    (r"listening", SND_C, 2.1, [(1952, r"Audrey: \ ten digits", 1), (1975, r"hidden Markov models", -1),
                                (1978, r"time warping", 1), (2006, r"CTC", -1), (2012, r"deep acoustic models", 1),
                                (2014, r"Deep Speech", -1), (2020, r"wav2vec 2.0", 1), (2022, r"Whisper", -1)]),
    (r"speaking", SPEAK_C, 0.75, [(1939, r"the Voder", 1), (1980, r"formant synthesis", -1),
                                  (1996, r"unit selection", 1), (2016, r"WaveNet", -1), (2017, r"Tacotron", 1),
                                  (2023, r"VALL-E", -1), (2026, r"Qwen3-TTS", 1)]),
    (r"text", TEXT_C, -0.6, [(1951, r"Shannon's letters", 1), (1994, r"byte pairs, \ to compress", -1),
                             (2012, r"WordPiece", 1), (2016, r"BPE for translation", -1), (2018, r"SentencePiece", 1),
                             (2019, r"bytes (GPT-2)", -1), (2024, r"entropy patches", 1)]),
    (r"pictures", IMG_C, -1.95, [(2014, r"captions", 1), (2017, r"VQ-VAE", -1), (2021, r"CLIP", 1),
                                 (2022, r"Flamingo", -1), (2023, r"LLaVA", 1), (2026, r"early fusion", -1)]),
]


def lane_axis():
    g = VGroup()
    for name, col, y, _ in LANES:
        g.add(Line([X0 - 0.1, y, 0], [X1 + 0.1, y, 0], color=col, stroke_width=1.5, stroke_opacity=0.5))
        g.add(label(name, font_size=22, color=col).move_to([-5.7, y, 0]))
    ticks = VGroup()
    for yr in (1940, 1960, 1980, 2000, 2010, 2015, 2020, 2025):
        x = tx(yr)
        ticks.add(Line([x, -2.85, 0], [x, -2.75, 0], color=GREY_C, stroke_width=1.5))
        ticks.add(MathTex(str(yr), font_size=20, color=GREY_B).move_to([x, -3.05, 0]))
    ticks.add(Line([X0, -2.8, 0], [X1, -2.8, 0], color=GREY_C, stroke_width=1.5))
    brk = VGroup(Line([tx(2010) - 0.08, -2.95, 0], [tx(2010) - 0.02, -2.65, 0], color=GREY_B, stroke_width=2),
                 Line([tx(2010) + 0.02, -2.95, 0], [tx(2010) + 0.08, -2.65, 0], color=GREY_B, stroke_width=2))
    note_ = note(r"the scale changes at 2010", font_size=18).move_to([tx(2010), -3.45, 0])
    g.add(ticks, brk, note_)
    return g


def events(lane_i: int):
    name, col, y, evs = LANES[lane_i]
    g = VGroup()
    for yr, txt, side in evs:
        d = Dot([tx(yr), y, 0], radius=0.07, color=col)
        lab = label(rf"{yr}\ \ {txt}", font_size=17, color=col)
        lab.next_to(d, UP if side > 0 else DOWN, buff=0.08)
        if lab.get_right()[0] > 6.95:
            lab.shift(LEFT * (lab.get_right()[0] - 6.95))
        g.add(VGroup(d, lab))
    return g


class History(VoiceoverScene):
    def construct(self):
        self.card()
        axis = lane_axis()
        evs = [events(i) for i in range(len(LANES))]
        self.listening(axis, evs)
        self.reading(evs)
        self.meet(axis, evs)

    def card(self):
        card = chapter_card(1, r"How we got here", r"How did every sense become a token?", lit=(1951,), part=PART)
        with self.voiceover("Chapter one. How we got here."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def listening(self, axis, evs):
        ev_l, ev_s = evs[0], evs[1]
        with self.voiceover(
            "Machines were listening long before they could read. <bookmark mark='a'/> In 1952 Bell Labs built "
            "Audrey, a rack of electronics that recognized the ten digits spoken by one person, ninety-seven to "
            "ninety-nine times in a hundred. <bookmark mark='b'/> In the 1970s recognizers learned to stretch time to "
            "match a template, and then, at IBM and Carnegie Mellon, to treat speech as a hidden Markov model, Part "
            "7's statistics, which ruled for thirty years. <bookmark mark='c'/> Neural networks took over the sound "
            "model in 2012, and in 2022 Whisper transcribed nearly a hundred languages. <bookmark mark='d'/> Speaking "
            "went the same way: from the Voder, played on a keyboard at the 1939 World's Fair, to formant "
            "synthesizers and spliced recordings, and in 2016 to WaveNet, a network that writes sound one sample at a "
            "time."
        ) as vo:
            self.play(FadeIn(axis), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(ev_l[0], scale=1.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_l[1:4]], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_l[4:]], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_s[:4]], lag_ratio=0.4), run_time=2.4)

    def reading(self, evs):
        ev_s, ev_t, ev_p = evs[1], evs[2], evs[3]
        with self.voiceover(
            "Then speech became language modeling: Tacotron, then in 2023 VALL-E, which writes a voice as codes the "
            "way a language model writes words. <bookmark mark='a'/> Text needed units of its own. Word models choked "
            "on words they had never seen, and characters made sequences long. In 1994 Philip Gage published a way "
            "to compress files by replacing common pairs of bytes; in 2016 it became the standard way to cut text "
            "into tokens, and versions over bytes and over probabilities followed. <bookmark mark='b'/> Pictures met "
            "words around 2014, when networks learned to caption photographs; in 2021 CLIP learned from four "
            "hundred million captioned pictures off the web, and by 2023 a vision encoder bolted onto a language "
            "model could talk about an image."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_s[4:]], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_t], lag_ratio=0.35), run_time=3.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in ev_p], lag_ratio=0.35), run_time=3.0)

    def meet(self, axis, evs):
        band = Rectangle(width=tx(2027) - tx(2024), height=5.0, stroke_width=0, fill_color=WHITE, fill_opacity=0.08)
        band.move_to([(tx(2024) + tx(2027)) / 2, 0.1, 0])
        bl = label(r"one model, \\ every sense", font_size=24, color=WHITE).next_to(band, UP, buff=0.05)
        names = label(r"GPT-4o, \ Moshi, \ Qwen-Omni", font_size=20, color=GREY_A)
        names.next_to(bl, LEFT, buff=0.3)
        arrows = VGroup(*[Arrow([tx(2023.2), y, 0], [tx(2024.3), 0.1, 0], buff=0.05, color=col, stroke_width=2,
                                max_tip_length_to_length_ratio=0.12) for _, col, y, _ in LANES])
        with self.voiceover(
            "<bookmark mark='a'/> In the last few years the threads met. Once speech, pictures and text are all "
            "tokens, one transformer can read and write them all: GPT-4o in 2024, Moshi, Qwen's omni models. "
            "<bookmark mark='b'/> This part builds that idea from the bottom up: what a token is and what it is "
            "worth, how codes are learned, how sound and pictures become sequences, and how the senses are matched."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(band), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(bl), FadeIn(names),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(e[0], color=WHITE, scale_factor=1.6) for ev in evs for e in ev], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
