from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import CONSONANT, HIDDEN, MONO, PART, SEEN, VOWEL, card_in, edge, load, node

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
FWD = C.BITS  # forward probabilities
VIT = C.SURPRISE  # the Viterbi path


def letter_color(ch):
    return GREY_B if ch == " " else VOWEL if ch in "aeiou" else CONSONANT


def sci_tex(v: float) -> str:
    e = int(np.floor(np.log10(v)))
    return rf"{v / 10 ** e:.1f}\!\times\!10^{{{e}}}"


class HMM(VoiceoverScene):
    def construct(self):
        card_in(self, 6, r"Hidden Markov models", r"What hidden states are the letters coming from?",
                "Chapter six. Hidden Markov models.")
        self.model()
        self.forward()
        self.viterbi()
        self.decode()

    # ------------------------------------------------------------------
    def model(self):
        h = load("hmm")
        A, B = np.asarray(h["A"]), np.asarray(h["B"])
        zs = [node(rf"z_{k}", [-6.2 + 1.6 * k, 1.5, 0]) for k in range(1, 5)]
        xs = [node(rf"x_{k}", [-6.2 + 1.6 * k, -0.3, 0], hidden=False) for k in range(1, 5)]
        chain = VGroup(*zs, *xs, *[edge(zs[k], zs[k + 1]) for k in range(3)], *[edge(zs[k], xs[k]) for k in range(4)])
        al = MathTex(r"A", font_size=30, color=HIDDEN).next_to(VGroup(zs[0], zs[1]), UP, buff=0.1)
        bl = MathTex(r"B", font_size=30, color=SEEN).next_to(edge(zs[0], xs[0]), LEFT, buff=0.1)
        defs = VGroup(
            label(r"hidden states $z_t$: \ a Markov chain, \ $A_{ij} = p(z_{t+1} = j \mid z_t = i)$", font_size=24,
                  color=HIDDEN),
            label(r"each state emits a letter: \ $B_j(x) = p(x_t = x \mid z_t = j)$", font_size=24, color=SEEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.5)
        # the trained two-state model of the letters (fitted in the next chapter)
        W = 0.12
        rows = VGroup()
        for s in range(2):
            g = VGroup()
            for i, ch in enumerate(ALPHA27):
                hh = max(1.1 * B[s][i] / 0.4, 0.01)
                g.add(Rectangle(width=W * 0.8, height=hh, stroke_width=0, fill_color=letter_color(ch),
                                fill_opacity=0.9).move_to([i * W, hh / 2, 0]))
            rows.add(g)
        rows.arrange(DOWN, buff=0.45).move_to([4.6, 0.9, 0])
        rl = VGroup(*[MathTex(rf"B_{s + 1}", font_size=26, color=HIDDEN).next_to(rows[s], LEFT, buff=0.15) for s in range(2)])
        tag = label(r"two states for the books' letters \\ (trained in the next chapter)", font_size=20,
                    color=GREY_A).next_to(rows, UP, buff=0.2)
        h1 = history_card(1966, r"L.~Baum \& T.~Petrie", r"probabilistic functions of Markov chains; \ Baum--Welch "
                          r"training, 1970", width=4.6).move_to([4.6, -2.2, 0])
        with self.voiceover(
            "Hidden states can also unfold in time. A hidden Markov model has a state we can't see, moving like part "
            "five's Markov chain, with transition probabilities A. <bookmark mark='a'/> At every step the state emits "
            "something we can see, a letter, from its own table of chances, B. <bookmark mark='b'/> Here is a "
            "two-state model of the letters in the books; we'll train it in the next chapter. One state prefers "
            "vowels and the space, the other consonants. <bookmark mark='c'/> Leonard Baum and his colleagues worked "
            "out the mathematics in the late 1960s, at the Institute for Defense Analyses. Three questions follow. "
            "How likely is a sentence? Which states produced it? And how do we learn A and B?"
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m) for m in chain], lag_ratio=0.04), FadeIn(al), FadeIn(defs[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows), FadeIn(rl), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(h1, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self, f, values=None, color=FWD):
        T = int(f["T"])
        letters = f["letters"]
        pos = [[np.array([-5.2 + 2.0 * t, 0.9 - 1.9 * s, 0]) for s in (0, 1)] for t in range(T)]
        nodes = VGroup(*[Circle(radius=0.26, color=VOWEL if s == 0 else CONSONANT, stroke_width=3,
                                fill_color=BACKGROUND, fill_opacity=1).move_to(pos[t][s]) for t in range(T) for s in (0, 1)])
        edges = VGroup(*[Line(pos[t][a], pos[t + 1][b], buff=0.28, color=GREY_D, stroke_width=1.5)
                         for t in range(T - 1) for a in (0, 1) for b in (0, 1)])
        lets = VGroup(*[Text("␣" if ch == " " else ch, font=MONO, font_size=30, color=letter_color(ch))
                        .move_to(pos[t][0] + UP * 1.0) for t, ch in enumerate(letters)])
        rows = VGroup(*[MathTex(rf"s_{s + 1}", font_size=28, color=VOWEL if s == 0 else CONSONANT)
                        .next_to(pos[0][s], LEFT, buff=0.35) for s in (0, 1)])
        vals = VGroup()
        if values is not None:
            for t in range(T):
                for s in (0, 1):
                    vals.add(MathTex(sci_tex(values[t][s]), font_size=24, color=color)
                             .move_to(pos[t][s] + (DOWN if s else UP) * 0.5))
        return pos, nodes, edges, lets, rows, vals

    def forward(self):
        f = load("forward")
        al = np.asarray(f["alpha"])
        T = int(f["T"])
        pos, nodes, edges, lets, rows, vals = self.lattice(f, al)
        for t in range(T):  # the s1 values sit above their circles, under the letters: move the letters up
            lets[t].shift(UP * 0.25)
        lat = VGroup(nodes, edges, lets, rows).shift(UP * 0.2)
        vals.shift(UP * 0.2)
        colors = {r"\alpha_t(j)": FWD, r"\alpha_{t-1}(i)": FWD, r"A_{ij}": HIDDEN, r"B_j(x_t)": SEEN}
        eq = VGroup(cmath(r"\alpha_t(j)", r"=", r"\sum_i", r"\alpha_{t-1}(i)", r"\,", r"A_{ij}", r"\,", r"B_j(x_t)",
                          colors=colors, font_size=40),
                    label(r"$\alpha_t(j) = p(x_1 \dots x_t,\ z_t = j)$: \ sum over the state before, \ by Markov",
                          font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        tot = al[-1].sum()
        res = label(rf"$p(\text{{``there''}}) = \sum_j \alpha_6(j) = {sci_tex(tot)}$ \ $=$ \ the sum over all "
                    rf"$2^{T} = {2 ** T}$ paths \ (checked)", font_size=24, color=FWD)
        res.to_edge(UP, buff=0.25)
        cost = label(rf"cost: \ $T \cdot S^2$ instead of $S^T$; \ for the whole sentence, ${f['n']} \times 4$ against "
                     rf"$2^{{{f['n']}}}$", font_size=22, color=GREY_A).next_to(res, DOWN, buff=0.12)
        with self.voiceover(
            "First: how likely is a sentence? Summing over every possible sequence of hidden states would take two to "
            "the power of its length. The forward algorithm does it in one sweep. <bookmark mark='a'/> Lay the states "
            "out as a lattice, one column per letter. Let alpha of a state be the probability of the letters so far, "
            "ending in that state. <bookmark mark='b'/> By the Markov property, each alpha is a sum over the state "
            "before: its alpha, times the chance of the move, times the chance of the new letter. "
            "<bookmark mark='c'/> Sweep left to right, and the last column adds up to the probability of the "
            f"letters. For 'there' and a space, that's about {tot * 1e7:.1f} in ten million, exactly the sum over all {2 ** T} paths. For the "
            f"whole {f['n']}-letter sentence, the sum has two to the {f['n']} terms; the sweep takes a few hundred "
            "multiplications. <bookmark mark='d'/> Part twenty-three's speech recognizers train with CTC, which runs "
            "this very recursion over the ways of lining up sound with text."
        ) as vo:
            self.play(FadeIn(lets), FadeIn(rows), FadeIn(nodes), Create(edges), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(Write(eq[0]), FadeIn(eq[1]))
            vo.wait_until("c")
            for t in range(1, T):
                into = VGroup(*edges[4 * (t - 1): 4 * t])
                self.play(into.animate.set_color(FWD).set_stroke(width=3), run_time=0.4)
                self.play(FadeIn(vals[2 * t]), FadeIn(vals[2 * t + 1]), into.animate.set_color(GREY_D).set_stroke(width=1.5),
                          run_time=0.5)
            self.play(FadeIn(res), FadeIn(cost))
            vo.wait_until("d")
            self.play(Indicate(eq[0], color=FWD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def viterbi(self):
        f = load("forward")
        de, back, vp = np.asarray(f["delta"]), np.asarray(f["back"]), [int(v) for v in f["vpath"]]
        T = int(f["T"])
        pos, nodes, edges, lets, rows, vals = self.lattice(f, de, color=VIT)
        for t in range(T):
            lets[t].shift(UP * 0.25)
        lat = VGroup(nodes, edges, lets, rows).shift(UP * 0.2)
        vals.shift(UP * 0.2)
        best = VGroup(*[Line(pos[t - 1][int(back[t][s])], pos[t][s], buff=0.28, color=GREY_A, stroke_width=3.5)
                        for t in range(1, T) for s in (0, 1)]).shift(UP * 0.2)
        path = VGroup(*[Line(pos[t][vp[t]], pos[t - 1][vp[t - 1]], buff=0.28, color=VIT, stroke_width=7)
                        for t in range(T - 1, 0, -1)]).shift(UP * 0.2)
        rings = VGroup(*[Circle(radius=0.32, color=VIT, stroke_width=5).move_to(pos[t][vp[t]] + UP * 0.2) for t in range(T)])
        eq = VGroup(cmath(r"\delta_t(j)", r"=", r"\max_i", r"\delta_{t-1}(i)", r"\,", r"A_{ij}", r"\,", r"B_j(x_t)",
                          colors={r"\delta_t(j)": VIT, r"\delta_{t-1}(i)": VIT, r"A_{ij}": HIDDEN, r"B_j(x_t)": SEEN},
                          font_size=40),
                    label(r"the same sweep with the sum replaced by a max, \ remembering the winner", font_size=22,
                          color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        h = history_card(1967, r"Andrew Viterbi", r"decoding convolutional codes; \ later Qualcomm's co-founder",
                         width=4.8).to_corner(UR, buff=0.25)
        with self.voiceover(
            "Second: which hidden states produced the letters? Change one thing: replace the sum with a maximum. "
            "<bookmark mark='a'/> Now each circle holds the probability of the single best path into it, and we "
            "keep a pointer to the state it came from: one bright arrow into each circle. <bookmark mark='b'/> At the "
            "end, take the better final state and follow the pointers back. That's the most likely path, found "
            "exactly, without trying all of them. <bookmark mark='c'/> Andrew Viterbi published it in 1967 for "
            "decoding error-correcting codes; it went into mobile phones and space probes, and it decoded speech for decades."
        ) as vo:
            self.play(FadeIn(lets), FadeIn(rows), FadeIn(nodes), Create(edges), Write(eq[0]), FadeIn(eq[1]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(vals[0]), FadeIn(vals[1]))
            for t in range(1, T):
                self.play(Create(best[2 * (t - 1)]), Create(best[2 * (t - 1) + 1]), FadeIn(vals[2 * t]),
                          FadeIn(vals[2 * t + 1]), run_time=0.6)
            vo.wait_until("b")
            self.play(Create(rings[-1]))
            self.play(LaggedStart(*[Create(p_) for p_ in path], lag_ratio=0.5), LaggedStart(*[Create(r_) for r_ in reversed(rings[:-1])],
                                                                                         lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(h, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decode(self):
        h = load("hmm")
        sent, st = h["sentence"], [int(s) for s in h["states"]]
        letters = VGroup(*[Text("␣" if ch == " " else ch, font=MONO, font_size=34, color=WHITE) for ch in sent])
        letters.arrange(RIGHT, buff=0.08).move_to(UP * 0.4)
        if letters.width > 13:
            letters.scale_to_fit_width(13)
        marks = VGroup(*[Circle(radius=0.11, color=HIDDEN, stroke_width=2, fill_color=VOWEL if s == 0 else CONSONANT,
                                fill_opacity=0.9).next_to(letters[i], DOWN, buff=0.35) for i, s in enumerate(st)])
        links = VGroup(*[Line(marks[i].get_center(), marks[i + 1].get_center(), color=HIDDEN, stroke_width=1.5)
                         for i in range(len(st) - 1)])
        head = label(r"The most likely hidden states of Shannon's sentence \ (Viterbi)", font_size=30).to_edge(UP, buff=0.6)
        key = VGroup(label(r"$s_1$", font_size=28, color=VOWEL), label(r"$s_2$", font_size=28, color=CONSONANT))
        key.arrange(RIGHT, buff=0.6).next_to(marks, DOWN, buff=0.5)
        note_ = label(r"the same alternation Part 5's three-state chain had, \ but here the states were never named",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here's Shannon's sentence from part one, every letter labelled by its most likely hidden state. "
            "<bookmark mark='a'/> Vowels and spaces on one side, consonants on the other, and the states alternate "
            "the way English does, though nobody ever told the model what a vowel is."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(l_) for l_ in letters], lag_ratio=0.03), run_time=1.5)
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.04), Create(links),
                      *[l_.animate.set_color(VOWEL if s == 0 else CONSONANT) for l_, s in zip(letters, st)],
                      FadeIn(key), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
