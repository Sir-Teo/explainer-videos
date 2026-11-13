from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.six()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        d = load("bent")
        c = clip("bent.pair")
        bx = boxes((r"A", r"B"), buff=1.6, width=3.4, height=1.7).move_to(UP * 0.9)
        tags = VGroup(label(r"an exact octave: \ 2 to 1", font_size=28, color=GREY_A).next_to(bx[0], DOWN, buff=0.25),
                      label(rf"too wide: \ {d['wide']:g} to 1", font_size=28, color=GREY_A).next_to(bx[1], DOWN, buff=0.25))
        scope = Scope(width=8.4, height=1.5, color=TUNE).move_to(DOWN * 2.0)
        self.play(FadeIn(bx), FadeIn(tags), FadeIn(scope), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"two notes together, \ twice", kind="synthesized", detail=r"sums of sines", corner=DL, tag_corner=DR)
            snd.drive(scope, scope.follow(c, window=0.03))
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        scope.set_wave(c.mono[int(3.2 * 48000): int(3.2 * 48000) + 1440].astype(float), 0.95 / float(np.abs(c.mono).max()))
        verdict = VGroup(label(r"rough", font_size=40, color=ROUGH).move_to(bx[0].get_center() + UP * 1.25),
                         label(r"smooth", font_size=40, color=SMOOTH).move_to(bx[1].get_center() + UP * 1.25))
        with self.voiceover(
            "Two notes sounding together, twice. In the first pair, the upper note has exactly twice the frequency "
            "of the lower: an octave, the simplest interval there is, the one every musical culture treats as the "
            "same note again. In the second pair the upper note is too high, by most of a semitone. "
            f"<bookmark mark='a'/> And yet the first pair is the sour one. The exact octave grinds, and the "
            "mistuned one is smooth. <bookmark mark='b'/> Nothing is wrong with your loudspeakers. One thing "
            "about these notes was changed, and it was not their pitch. By the end of this part you will know "
            "what it was, why it turns an octave into a dissonance, and how to do it yourself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(verdict[0]), FadeIn(verdict[1]))
            vo.wait_until("b")
            self.play(Indicate(bx[0][0], color=ROUGH), Indicate(bx[1][0], color=SMOOTH))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def six(self):
        head = label(r"Why do some notes belong together?", font_size=40).to_edge(UP, buff=0.45)
        cards = VGroup(
            history_card(r"c.\ 530 BC", r"Pythagoras", r"number: small whole ratios of string lengths", width=4.1, font_size=20),
            history_card(1638, r"Galileo", r"pulses that arrive at the ear together", width=4.1, font_size=20),
            history_card(1722, r"Rameau", r"the partials of a single sounding body", width=4.1, font_size=20),
            history_card(1739, r"Euler", r"a formula for sweetness", width=4.1, font_size=20),
            history_card(1863, r"Helmholtz", r"beats between partials, or the lack of them", width=4.1, font_size=20),
            history_card(1890, r"Stumpf", r"fusion: two notes heard as one", width=4.1, font_size=20),
        ).arrange_in_grid(2, 3, buff=0.3).move_to(DOWN * 0.5)
        with self.voiceover(
            "This part is about one question, the oldest in the science of music. Why do some notes belong "
            "together? Why is a fifth restful and a tritone tense? <bookmark mark='a'/> Pythagoras said: number. "
            "Consonances are small whole ratios. <bookmark mark='b'/> Galileo said: because their pulses strike "
            "the eardrum together. <bookmark mark='c'/> Rameau: because they are the partials of one sounding "
            "body. <bookmark mark='d'/> Euler wrote a formula for it. <bookmark mark='e'/> Helmholtz said it was "
            "the absence of beats. <bookmark mark='f'/> And Carl Stumpf said that consonant notes are simply the "
            "ones that fuse into one. Six answers in two and a half thousand years, each from one of the best "
            "minds of its time. With a string, a spectrum and an ear, we can now compute every one of them, and "
            "listen to where each one breaks."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c_ in zip("abcdef", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c_), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"what the theories of number predict, \ and the test they fail",
            r"beats: \ what two close tones do, \ and how tuners use them",
            r"roughness, \ measured: \ Plomp and Levelt's curve and the ear's bands",
            r"how the just ratios fall out of a curve that knows no ratios, \ and how to move them",
            r"fusion: \ the single pitch inside a chord, \ and why major is not minor",
            r"what is learned, \ and what is still not understood",
        ], title=r"Part 5: \ Consonance", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> First the theories of number, and one small test that defeats "
            "them all. <bookmark mark='b'/> Then beats: what two tones do when they are nearly the same, and how "
            "every piano tuner uses them. <bookmark mark='c'/> Then roughness, measured in a laboratory, and how "
            "it follows the bands of the ear that we found in Part 4. <bookmark mark='d'/> From that we will draw "
            "a curve that contains no ratios, and watch Pythagoras's ratios fall out of it. Then we will move "
            "them. <bookmark mark='e'/> We will find the single pitch hidden inside a chord, and use it to tell "
            "major from minor. <bookmark mark='f'/> And we will ask how much of all this is learned. Every curve "
            "in this part is computed by Monochord, from the ear of Part 4."
        ) as vo:
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
