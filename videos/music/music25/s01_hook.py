from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.legend()
        self.quiz()
        self.galilei()
        self.plan()

    # ------------------------------------------------------------------
    def legend(self):
        card = history_card(1589, r"Florence: \ Vincenzo Galilei, \ lutenist, \ father of the astronomer", r"hangs weights on strings to test a story two thousand years old",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"the legend: \ Pythagoras heard hammers in a smithy, \ weighed them, \ found 2:1 for the octave", WHITE),
            (r"and the same ratios, \ the story said, \ hold for weights hung on strings", WHITE),
            (r"Galilei tried it", TUNE),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Florence, 1589. Vincenzo Galilei, a lutenist and the father of the astronomer Galileo, is hanging weights "
            "on strings. <bookmark mark='a'/> An old story said that Pythagoras, passing a smithy, heard hammers ringing "
            "in harmony, weighed them, and found that a hammer twice as heavy sounded an octave lower. "
            "<bookmark mark='b'/> The story added that the same ratios hold for weights hung on strings: double the "
            "weight, and the string goes up an octave. <bookmark mark='c'/> Galilei, who distrusted the authority of the "
            "ancients, tried it."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.weights")
        card = listen_card(r"Two equal strings, \ plucked one after the other, \ then together. \ In A the weights are 2:1; \ in B, \ 4:1. \ "
                           r"Which pair sounds an octave, \ A or B?", width=10.4)
        with self.voiceover(
            "Hear what he found. Two equal strings, one after the other, then together. In A, one string carries twice "
            "the weight of the other; in B, four times. Which pair sounds an octave, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes_ = boxes(("A", "B"), buff=2.4)
        wts = VGroup()
        for b, (k, w) in zip(boxes_, (("A", "2 : 1"), ("B", "4 : 1"))):
            wts.add(label(rf"weights \ {w}", font_size=24, color=GREY_A).next_to(b, DOWN, buff=0.3))
        self.play(FadeOut(card), FadeIn(boxes_), FadeIn(wts))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 1's string, \ plucked", corner=DL, tag_corner=DR)
            pulse(snd, boxes_[0], d["starts"]["A"], d["starts"]["B"] - 0.5)
            pulse(snd, boxes_[1], d["starts"]["B"], c.duration)
        ans = VGroup(label(rf"a ratio of $\sqrt{{2}}$: \ {d['pairs']['A']['cents']:.0f} cents, \ a tritone", font_size=22, color=RED).next_to(wts[0], DOWN, buff=0.3),
                     label(r"a ratio of 2: \ the octave", font_size=22, color=TUNE).next_to(wts[1], DOWN, buff=0.3))
        with self.voiceover(
            "B. Doubling the weight does not give an octave: it gives a ratio of the square root of two, six hundred "
            "cents, a tritone, the most dissonant interval of the old theory. To get an octave you need four times the "
            "weight. The legend was false, and had been repeated, unchecked, for two thousand years."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def galilei(self):
        d = load("hook")
        ms = d["mersenne"]
        rows_ = text_rows([
            (r"pitch goes as the square root of the tension: \ $f = \frac{1}{2L}\sqrt{T/\mu}$ \ (Mersenne, \ 1636)", WHITE),
            (rf"1 kg: \ {ms[0]['hz']:.0f} Hz; \ 4 kg: \ {ms[2]['hz']:.0f} Hz; \ 9 kg: \ {ms[3]['hz']:.0f} Hz \ (65 cm, \ 0.6 g a metre)", WHITE),
            (r"Galilei's conclusion: \ the numbers belong to the strings, \ not to heaven", TUNE),
            (r"so music should serve the words and the listener, \ not number: \ his \textit{Dialogue on ancient and modern music} \ (1581)", WHITE),
            (r"out of that quarrel came opera, \ the figured bass, \ and major and minor", EAR),
        ])
        head = label(r"the numbers belong to the strings", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The law behind it was written down by Marin Mersenne in 1636: <bookmark mark='a'/> a string's pitch goes as "
            f"the square root of its tension. <bookmark mark='b'/> One kilogram on a string sixty-five centimetres long, weighing six tenths of a gram a metre, gives "
            f"{say(round(ms[0]['hz']))} hertz; four kilograms, an octave higher; nine, an octave and a fifth. "
            "<bookmark mark='c'/> Galilei drew a polemical conclusion: the simple ratios belong to strings of equal "
            "tension, not to the structure of heaven, and music need not obey them. <bookmark mark='d'/> In his Dialogue "
            "on ancient and modern music, from 1581, he had already argued that music should serve the words and move the "
            "listener, as the Greeks were said to have done, rather than display counterpoint. "
            "<bookmark mark='e'/> Out of that argument, and the one between Artusi and Monteverdi, came opera, the "
            "figured bass, and the major and minor keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 25: \ The Baroque", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"monody, \ recitative and aria; \ opera", WHITE),
            (r"the figured bass: \ Corelli's violins against a realizer", WHITE),
            (r"affect and ornament; \ the suite", WHITE),
            (r"ritornello and concerto, \ and a program that finds the returns", EAR),
            (r"temperament and the colour of keys; \ from modes to major and minor", WHITE),
            (r"Bach, \ Handel, \ Rameau; \ what pitch, \ what tempo?", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part covers the century and a half from 1600 to Bach's death in 1750. <bookmark mark='a'/> The new "
            "song for one voice, and the opera built from it. <bookmark mark='b'/> The figured bass, tested on a real "
            "trio sonata by Corelli. <bookmark mark='c'/> Affect, ornament, and the dances of the suite. "
            "<bookmark mark='d'/> The concerto's ritornello, and a program that finds its returns. "
            "<bookmark mark='e'/> Temperament, the colour of keys, and how eight modes became two keys. "
            "<bookmark mark='f'/> Three great careers, and the question every modern performance has to answer: at what "
            "pitch, and how fast?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
