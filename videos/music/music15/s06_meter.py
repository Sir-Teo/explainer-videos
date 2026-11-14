from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Meter(SoundScene):
    def construct(self):
        chapter(self, 5, r"Finding the key", r"How could a machine find home?", extra=((1990, r"the Krumhansl--Schmuckler key finder"),))
        self.method()
        self.tune()

    # ------------------------------------------------------------------
    def method(self):
        d = load("profile")
        prof = np.array(d["kk_major"])
        a = note_bars(np.array(d["corpus_major"]) * 100, NAMES12, width=5.2, height=1.5, color=BLUE, show_values=False, font_size=16, top=30).move_to(LEFT * 3.6 + UP * 1.1)
        b = note_bars(prof, NAMES12, width=5.2, height=1.5, color=TUNE, show_values=False, font_size=16, top=7).move_to(LEFT * 3.6 + DOWN * 1.7)
        la = label(r"the piece: \ how long each note sounds", font_size=22, color=BLUE).next_to(a, UP, buff=0.12)
        lb = label(r"a key's profile, \ slid to each of 12 notes, \ major and minor", font_size=22, color=TUNE).next_to(b, UP, buff=0.12)
        steps = VGroup(label(r"1. \ count how long each of the twelve notes sounds", font_size=26, color=WHITE), label(r"2. \ compare with the profile of each of 24 keys", font_size=26, color=WHITE),
                       label(r"3. \ the best match is the key", font_size=28, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.4 + UP * 0.3)
        with self.voiceover(
            "If a key is a profile, then finding the key is matching. In 1990 Krumhansl published an "
            "algorithm she had worked out with Mark Schmuckler. <bookmark mark='a'/> Take a piece of "
            "music, and count how long each of the twelve notes sounds. <bookmark mark='b'/> Compare "
            "that with the profile of C major; then slide the profile up a semitone and compare with D "
            "flat major; and so on round all twelve, and the same for the twelve minor keys. "
            "<bookmark mark='c'/> Whichever of the twenty-four matches best is the answer. No rules "
            "about chords or cadences. Just: which key's habits does this music have?"
        ) as vo:
            lead = label(r"if a key is a profile, \ finding the key is matching", font_size=32, color=GREY_A).to_edge(UP, buff=0.4)
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(steps[1]))
            self.play(b.animate.shift(RIGHT * 0.43), rate_func=there_and_back, run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("meter")
        c = clip("meter.tune")
        r = roll(d["pitches"], d["beats"], width=10.5, height=1.8, lo=-1, hi=10, lines=(0,), phrase_ends=(7,), color=TUNE).move_to(UP * 1.9)
        names = ["C major", "F major", "G major", "A minor"]
        m = key_meter(names, width=5.5, row=0.6, color=TUNE, font_size=28, values=[1 / 24] * 4).move_to(DOWN * 1.1 + RIGHT * 0.6)
        ml = label(r"how sure the key finder is, \ note by note", font_size=22, color=GREY_B).next_to(m, UP, buff=0.3)
        with self.voiceover(
            "Let the key finder listen to the Tune, one note at a time, and watch how sure it is of "
            "four keys. This version works with probabilities, after David Temperley, so the bars are "
            "its degrees of belief."
        ):
            self.play(FadeIn(r), FadeIn(m), FadeIn(ml))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ and the key finder", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r, d["times"], hot=WHITE, base=TUNE)
            for k, row in enumerate(d["rows"]):
                snd.wait_until(d["times"][k] + 0.05)
                m.set([row["c_major"], row["f_major"], row["g_major"], row["a_minor"]])
        peak = max(d["rows"], key=lambda x: x["f_major"])
        cap = VGroup(label(rf"after {peak['notes']} notes it believed F major, \ {100 * peak['f_major']:.0f} in a hundred", font_size=26, color=EAR),
                     label(rf"sure of C major only after {d['first_sure']}", font_size=26, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "It got there. But look at what happened in the middle. <bookmark mark='a'/> When the second "
            f"phrase began, on two long Fs, the machine believed F major, {say(100 * peak['f_major'])} "
            f"chances in a hundred, and it was not sure of C until the {say(d['first_sure'])}th note. "
            "You were never in doubt. The reason is in the notes of the Tune. It uses C, D, E, F, G "
            "and A: six notes, and never the seventh. Those six belong to C major and to F major "
            "alike. Chapter seven comes back to that."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap), Indicate(m.rows[1][0], color=EAR))
        self.wait(0.4)
        self.clear_scene()
