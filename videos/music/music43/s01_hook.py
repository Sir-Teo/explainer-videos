from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.hatto()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"Three recordings of the same two phrases, \ released under three pianists' names. \ "
                           r"Two of them are really the same recording. \ Which two?", width=10.4)
        with self.voiceover(
            "A question for your ears. Three synthetic model performances of the same two phrases, labeled as if released under three pianists' names; these are not Hatto recordings. Two "
            "of them are really one and the same recording. Which two?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        perfs = d["perfs"]
        names = ("one", "two", "three")
        rolls = VGroup(*[VGroup(label(rf"recording {k}", font_size=19, color=GREY_A), perf_roll(perfs[k], width=3.8, height=1.3, lo=58, hi=72, vel=True)).arrange(DOWN, buff=0.2) for k in names]).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(rolls))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three recordings", detail=r"Part 7's piano, \ model pianists", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, rolls[i], st[k], end, buff=0.1)
                flash(snd, rolls[i][1].notes, [st[k] + p["t"] for p in perfs[k]], hot=WHITE, base=TUNE)
        r = d["r"]
        ans = VGroup(label(r"the first and the third: \ the third is the first, \ slowed by 5\%", font_size=21, color=TUNE),
                     label(rf"their timing shapes correlate {r['one-three']:.2f}; \ the second's with either, \ {r['one-two']:.2f}", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The first and the third. The third is the first recording slowed down by five per cent, which moves every note "
            "but keeps the proportions between them. Measure each recording's timing shape, the pattern of long and short "
            f"notes after removing the overall tempo, and the first and third correlate {say(r['one-three'], 2)}; the "
            f"second correlates {say(r['one-two'], 2)} with either. In 2007 the same kind of measurement exposed one of the "
            "strangest frauds in recording history."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hatto(self):
        items = [
            (r"Joyce Hatto, \ an English pianist who had stopped giving concerts, \ issued over a hundred CDs late in life", WHITE),
            (r"critics praised them; \ in February 2007 one went into a computer, \ and the track database named another pianist", WHITE),
            (r"her husband, \ the producer, \ had copied other pianists' recordings, \ sometimes time-stretched or re-equalised", WHITE),
            (r"Nicholas Cook and Craig Sapp's timing analyses matched them note by note: \ no two pianists shape time alike", TUNE),
            (r"this part asks what a performer adds to the notes, \ and measures it in milliseconds", GREY_A),
        ]
        rows_scene(self, r"the Hatto affair", items,
                   "Joyce Hatto was an English pianist who had stopped giving concerts, and who late in life issued over a "
                   "hundred CDs on a small label. <bookmark mark='b'/> Critics praised them. In February 2007 one of the discs "
                   "went into a computer, and the online track database named a different pianist. <bookmark mark='c'/> Her "
                   "husband, the producer, had copied other pianists' recordings, sometimes time-stretched or re-equalised to "
                   "disguise them. <bookmark mark='d'/> Timing analyses, among them Nicholas Cook and Craig Sapp's, matched the "
                   "recordings note by note, because matching detailed timing and audio can provide strong evidence of a shared recording. <bookmark mark='e'/> This part asks what "
                   "a performer adds to the notes, and measures it in milliseconds.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"what a performer adds: \ timing, \ loudness, \ articulation",
            r"rules of expression, \ and the kinematics of slowing down",
            r"vibrato, \ and what pitch it is heard at",
            r"playing together: \ correction, \ and when it fails",
            r"who is playing? \ an identity test on timing",
            r"practice, \ anxiety and the performer's body",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. What a performer adds to the score: timing, loudness and articulation. "
            "<bookmark mark='b'/> Rules of expression, and the physics of slowing down. <bookmark mark='c'/> Vibrato, and "
            "the pitch it is heard at. <bookmark mark='d'/> Playing together: how players correct each other, and when "
            "correction fails. <bookmark mark='e'/> Who is playing: an identity test on timing. <bookmark mark='f'/> And "
            "practice, anxiety and the performer's body."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
