from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import CONSONANT, HIDDEN, MONO, VOWEL, load

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"


def letter_color(ch):
    return GREY_B if ch == " " else VOWEL if ch in "aeiou" else CONSONANT


class HMM(VoiceoverScene):
    def construct(self):
        self.card()
        self.learn()
        self.decode()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Hidden Markov models", r"What hidden states are the letters coming from?", part=6)
        with self.voiceover("Chapter three. Hidden Markov models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def learn(self):
        h = load("hmm")
        A, Bs, lls = np.asarray(h["A"]), np.asarray(h["Bs"]), np.asarray(h["lls"])
        assert set("aeiou") <= set(h["vowel_side"])
        # two hidden states and their transitions
        s_pos = [np.array([-5.0, 1.9, 0]), np.array([-5.0, -1.1, 0])]
        states = VGroup(*[VGroup(Circle(radius=0.45, color=HIDDEN, stroke_width=4, fill_color=BACKGROUND, fill_opacity=1)
                                 .move_to(p_), MathTex(rf"s_{k + 1}", font_size=36, color=HIDDEN).move_to(p_))
                          for k, p_ in enumerate(s_pos)])
        sw = VGroup(CurvedArrow(s_pos[0] + DOWN * 0.45 + LEFT * 0.15, s_pos[1] + UP * 0.45 + LEFT * 0.15, angle=0.5,
                                color=GREY_B, stroke_width=3),
                    CurvedArrow(s_pos[1] + UP * 0.45 + RIGHT * 0.15, s_pos[0] + DOWN * 0.45 + RIGHT * 0.15, angle=0.5,
                                color=GREY_B, stroke_width=3))
        swl = VGroup(MathTex(f"{A[0, 1]:.2f}", font_size=26, color=GREY_A).next_to(sw[0], LEFT, buff=0.1),
                     MathTex(f"{A[1, 0]:.2f}", font_size=26, color=GREY_A).next_to(sw[1], RIGHT, buff=0.1))
        # each state's letters, as bars
        W, H = 0.3, 2.0
        x0 = -3.7

        def bars(B):
            g = VGroup()
            for k, yb in enumerate((1.2, -1.8)):
                for i, ch in enumerate(ALPHA27):
                    h_ = max(H * B[k][i] / 0.4, 0.01)
                    g.add(Rectangle(width=W * 0.8, height=h_, stroke_width=0, fill_color=letter_color(ch),
                                    fill_opacity=0.9).move_to([x0 + i * W, yb + h_ / 2, 0]))
            return g

        it = ValueTracker(0)
        bar_g = always_redraw(lambda: bars(Bs[int(round(it.get_value()))]))
        labs = VGroup(*[Text("␣" if ch == " " else ch, font=MONO, font_size=16, color=letter_color(ch))
                        .move_to([x0 + i * W, yb - 0.2, 0]) for yb in (1.2, -1.8) for i, ch in enumerate(ALPHA27)])
        links = VGroup(*[DashedLine(s_pos[k] + RIGHT * 0.45, [x0 - 0.3, yb + 0.6, 0], color=HIDDEN, stroke_width=2)
                         for k, yb in enumerate((1.2, -1.8))])
        itv = Integer(0, font_size=30)
        itl = VGroup(label(r"Baum--Welch round", font_size=24, color=GREY_A), itv).arrange(RIGHT, buff=0.15)
        itl.to_corner(UR, buff=0.4)
        bits = DecimalNumber(-lls[0], num_decimal_places=2, font_size=30, color=C.BITS)
        bitl = VGroup(label(r"bits per letter:", font_size=24, color=GREY_A), bits).arrange(RIGHT, buff=0.15)
        bitl.next_to(itl, DOWN, buff=0.15).align_to(itl, RIGHT)
        head = label(r"Each hidden state emits letters from its own table", font_size=28).to_edge(UP, buff=0.3).shift(LEFT * 1.0)
        found = label(r"$s_1$: \ space and a, e, i, o, u \quad $s_2$: \ every consonant", font_size=28, color=WHITE)
        found.to_edge(DOWN, buff=0.25)
        cite_ = cite(r"R.~J.~Cave \& L.~P.~Neuwirth (1980); \ L.~E.~Baum et al.\ (1970)", corner=UR).shift(DOWN * 0.9)
        n_it = len(Bs) - 1
        with self.voiceover(
            "Hidden states can also unfold in time. A hidden Markov model says there's a state we can't see, moving "
            "like part four's Markov chain, and each state emits a letter from its own table of chances. We see only "
            "the letters. <bookmark mark='a'/> Give it two hidden states, two hundred thousand letters of the books, "
            "and random first guesses. <bookmark mark='b'/> Fit it with EM again, which for this model is called "
            "Baum–Welch, and watch what each state learns to emit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(states))
            vo.wait_until("a")
            self.play(FadeIn(bar_g), FadeIn(labs), Create(links), FadeIn(itl), FadeIn(bitl))
            vo.wait_until("b")
            for k in (1, 2, 3, 5, 8, 12, 20, 35, n_it):
                self.play(it.animate.set_value(k), ChangeDecimalToValue(itv, k), ChangeDecimalToValue(bits, -lls[min(k, len(lls) - 1)]),
                          run_time=0.8)
        with self.voiceover(
            "One state ends up with the space, and a, e, i, o and u. The other takes every consonant. "
            f"<bookmark mark='a'/> And they take turns: after one, the other, about {100 * A[0, 1]:.0f} percent of "
            "the time. Nobody mentioned vowels. Cave and Neuwirth found exactly this in 1980."
        ) as vo:
            self.play(FadeIn(found), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(sw), FadeIn(swl))
        bar_g.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decode(self):
        h = load("hmm")
        sent, st = h["sentence"], [int(s) for s in h["states"]]
        letters = VGroup(*[Text("␣" if ch == " " else ch, font=MONO, font_size=34, color=WHITE) for ch in sent])
        letters.arrange(RIGHT, buff=0.08).move_to(UP * 0.2)
        if letters.width > 13:
            letters.scale_to_fit_width(13)
        marks = VGroup(*[Circle(radius=0.11, color=HIDDEN, stroke_width=2, fill_color=VOWEL if s == 0 else CONSONANT,
                                fill_opacity=0.9).next_to(letters[i], DOWN, buff=0.35) for i, s in enumerate(st)])
        links = VGroup(*[Line(marks[i].get_center(), marks[i + 1].get_center(), color=HIDDEN, stroke_width=1.5)
                         for i in range(len(st) - 1)])
        head = label(r"The most likely hidden states of Shannon's sentence \ (Viterbi)", font_size=30).to_edge(UP, buff=0.6)
        key = VGroup(label(r"$s_1$", font_size=28, color=VOWEL), label(r"$s_2$", font_size=28, color=CONSONANT))
        key.arrange(RIGHT, buff=0.6).next_to(marks, DOWN, buff=0.5)
        note_ = label(r"the same alternation Part 4's three-state chain had, \ but here the states were never named",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now decode: given a sentence, what's the most likely sequence of hidden states behind it? The Viterbi "
            "algorithm answers exactly, in one pass. <bookmark mark='a'/> Here's Shannon's sentence from part one, "
            "every letter labelled by its hidden state. <bookmark mark='b'/> Speech recognition ran on models like "
            "this for thirty years."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(l_) for l_ in letters], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.04), Create(links),
                      *[l_.animate.set_color(VOWEL if s == 0 else CONSONANT) for l_, s in zip(letters, st)],
                      FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
