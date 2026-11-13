from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.two_sounds()
        self.kac()
        self.plan()

    # ------------------------------------------------------------------
    def two_sounds(self):
        d = load("hook")
        c = clip("hook.pair")
        s = StringView(width=5.0).move_to(LEFT * 3.4 + UP * 2.2)
        drum = mode_diagram(0, 1, radius=0.9).move_to(RIGHT * 3.4 + UP * 2.2)
        ls = label(r"a string", font_size=30, color=STR).next_to(s, DOWN, buff=0.35)
        ld = label(r"a drum", font_size=30, color=SKIN).next_to(drum, DOWN, buff=0.2)
        self.play(FadeIn(s), FadeIn(drum), FadeIn(ls), FadeIn(ld), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"a string, \ then a drum, \ on the same note", detail=r"two models", corner=DL, tag_corner=DR)
            pulse(snd, ls, snd.time_of("string"), snd.time_of("string") + 2.0, buff=0.12)
            pulse(snd, ld, snd.time_of("drum"), snd.time_of("drum") + 2.0, buff=0.12)
        g = axes([0, 8.6], [0, 2.4], x_length=11.0, y_length=2.2, xlabel=r"frequency, \ in units of the lowest", ylabel="", xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[], font_size=20).move_to(DOWN * 1.6)
        r1 = tick_row(g, d["string"], 1.7, STR, fmt="{:.0f}")
        r2 = tick_row(g, d["drum"], 0.55, SKIN)
        with self.voiceover(
            "A string, and a drum. Their lowest frequencies are the same. The string plays a note you could "
            "sing back to me. The drum says thump. <bookmark mark='a'/> For eight parts, everything we have "
            "built has been long and thin: strings, and columns of air. And long thin things have overtones "
            "at two, three, four, five times their lowest frequency. Consonance, tuning, the ear's sense of "
            "pitch: Parts 4, 5 and 6 were all built on that. <bookmark mark='b'/> A drumhead is a string's "
            "nearest relation, a thing under tension, held at its edge. Its overtones are at one point five "
            "nine, two point one four, two point three, two point six five times the lowest. There is no "
            "pattern there that the ear can use. Nature tunes a drum badly, and a bar and a bell worse."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kac(self):
        d = load("shape")
        card = history_card(1966, r"Mark Kac, \ ``Can one hear the shape of a drum?''", r"if you knew every overtone of a drum, exactly, could you work out its shape?", width=6.0, font_size=22).to_edge(UP, buff=0.5)
        a = polygon_shape(d["drum1"], 0.85).move_to(LEFT * 3.0 + DOWN * 1.0)
        b = polygon_shape(d["drum2"], 0.85).move_to(RIGHT * 3.0 + DOWN * 1.0)
        q = label(r"?", font_size=80, color=EAR).move_to(DOWN * 1.0)
        cap = label(r"1992: \ two drums", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And yet those ugly numbers hold a great deal of information. In 1966 the mathematician Mark Kac "
            "asked a question in the title of a lecture: can one hear the shape of a drum? If you knew every "
            "overtone of a drum, exactly, could you work out what shape it must be? <bookmark mark='a'/> For "
            "twenty-six years nobody knew. Then, in 1992, three mathematicians drew these two shapes. By the "
            "end of this part Monochord will have computed the notes of both, and you will have heard them."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(q), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"nature tunes these things badly.", font_size=32, color=BAD), label(r"Makers learned to retune them.", font_size=32, color=GOOD)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"the modes of a skin, \ and why a drum goes thump",
            r"the kettledrum and the tabla: \ two ways to give a skin a note",
            r"bars: \ a knife under a marimba",
            r"bells, \ and the minor third inside every one of them",
            r"plates, \ gongs and cymbals; \ a steel drum from an oil barrel",
            r"and Kac's question: \ what a spectrum says about a shape",
        ], title=r"Part 9: \ Drums, \ Bars and Bells", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "Meanwhile instrument makers had been solving the opposite problem for three thousand years. "
            "Not: what shape has these overtones? But: how do I change this skin, this bar, this bell, so "
            "that its overtones are the ones I want? <bookmark mark='a'/> So this part goes through the "
            "things that are struck. A skin, and why it goes thump. <bookmark mark='b'/> Two drums that "
            "were taught to sing, by quite different means. <bookmark mark='c'/> A wooden bar, tuned with a "
            "knife. <bookmark mark='d'/> A bell, which has had a minor chord inside it for four hundred "
            "years. <bookmark mark='e'/> Plates, gongs and cymbals, and an instrument beaten out of an oil "
            "barrel. <bookmark mark='f'/> And at the end, the two drums of 1992."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
