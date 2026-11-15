from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.bells()
        self.tomb()
        self.plan()
        self.listen2()

    # ------------------------------------------------------------------
    def bells(self):
        d = load("hook")
        c = clip("hook.bells")
        card = listen_card(r"Three bronze bells, \ each struck twice: \ once in the middle of its face, \ once near its edge. \ "
                           r"Does each bell give the same note both times, \ or two different notes?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three bronze bells, each struck twice, once in the middle of its face and once near "
            "its edge. Does each bell give the same note both times, or two different notes?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        shapes = VGroup()
        for i in range(3):
            body = VGroup(Ellipse(width=1.3 + 0.2 * (2 - i), height=1.8 + 0.25 * (2 - i), color=TUNE, stroke_width=3))
            mid = Dot(body.get_center() + DOWN * 0.3, radius=0.1, color=WHITE)
            side = Dot(body.get_center() + DOWN * 0.3 + RIGHT * (0.45 + 0.07 * (2 - i)), radius=0.1, color=EAR)
            shapes.add(VGroup(body, mid, side))
        shapes.arrange(RIGHT, buff=1.6).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(shapes))
        with self.listen(c) as snd:
            window(snd, r"three bells, \ centre then side", detail=r"a two-tone bell model", corner=DL, tag_corner=DR)
            pulse(snd, shapes, 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.35)
            for k, t0 in enumerate(d["times"]):
                pulse(snd, shapes[k // 2][1 + k % 2], t0, t0 + 1.4, buff=0.06)
        ans = label(r"two notes from every bell: \ the side strike sounds a minor third above the centre", font_size=22, color=TUNE).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Two different notes. Each bell sounds one pitch when struck at the centre and another, here a minor third "
            "higher, when struck near the edge. These are models of a kind of bell that was made in China two and a half "
            "thousand years ago, on purpose, by founders who understood exactly what they were doing."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tomb(self):
        items = [
            (r"1978, \ Suizhou, \ Hubei: \ the tomb of Marquis Yi of Zeng, \ sealed in 433 BCE", WHITE),
            (r"65 bronze bells, \ hung in three tiers on a lacquered frame, \ with stone chimes, \ zithers and pipes", WHITE),
            (r"each bell sounds two notes; \ inscriptions in gold name them, \ and how they relate to other states' systems", WHITE),
            (r"a tuning treatise in bronze, \ older than Aristoxenus", TUNE),
            (r"this part goes from those bells to the gamelan", GREY_A),
        ]
        rows_scene(self, r"a tomb in Hubei", items,
                   "In 1978 soldiers levelling a hill in Hubei province found a tomb. <bookmark mark='b'/> It was the tomb of "
                   "Marquis Yi of Zeng, sealed in 433 BCE. <bookmark mark='c'/> It held sixty-five bronze bells hung in three tiers "
                   "on a lacquered frame, with stone chimes, zithers and pipes. <bookmark mark='d'/> Each bell sounds two notes, "
                   "and inscriptions inlaid in gold name them and relate them to the pitch systems of neighbouring states. "
                   "<bookmark mark='e'/> It is a treatise on tuning cast in bronze, older than the Greek theorist Aristoxenus. "
                   "<bookmark mark='f'/> This part goes from those bells to the gamelan of Java and Bali.", marks="cdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the two-tone bell, \ and why it works",
            r"twelve pitches from cutting a pipe; \ Jing Fang's sixty, \ and the near-closing 53",
            r"five notes, \ five modes; \ the guqin's harmonics",
            r"heterophony, \ and the court music of Japan",
            r"gamelan: \ slendro and pelog with no standard, \ and bronze spectra",
            r"tuning apart on purpose; \ the gong cycle and interlocking parts",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The two-tone bell, and why it works. <bookmark mark='b'/> Twelve pitches from cutting a pipe, "
            "and Jing Fang's sixty, with the near-closing fifty-third. <bookmark mark='c'/> Five notes and five modes, and "
            "the guqin's harmonics. <bookmark mark='d'/> Heterophony, and the court music of Japan. <bookmark mark='e'/> "
            "Gamelan, whose scales have no standard, and the spectra of bronze. <bookmark mark='f'/> Instruments tuned apart "
            "on purpose, the gong cycle, and parts that interlock."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen2(self):
        items = [
            (r"these traditions are heard here through our own models and phrases", WHITE),
            (r"every named piece, \ instrument and ensemble deserves to be heard in real performance", WHITE),
            (r"recordings by Chinese, \ Japanese, \ Korean, \ Javanese and Balinese musicians are widely available", WHITE),
            (r"listen for texture and time as much as for pitch", TUNE),
            (r"the models show the mechanisms; \ the musicians make the music", GREY_A),
        ]
        rows_scene(self, r"listening across traditions", items,
                   "One more word before the details. <bookmark mark='b'/> These traditions are heard here only through our own models and phrases. <bookmark mark='c'/> Every piece, instrument and ensemble named deserves to be heard in real performance, <bookmark mark='d'/> and recordings by Chinese, Japanese, Korean, Javanese and Balinese musicians are easy to find. <bookmark mark='e'/> Listen for texture and time as much as for pitch. <bookmark mark='f'/> The models show the mechanisms; the musicians make the music.", marks="cdef")
