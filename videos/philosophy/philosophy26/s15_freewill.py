from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class FreeWill(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Freedom, \ and quantum technology", r"What do the theorems buy us?",
                            lit=(2006,), part=PART)
        with self.voiceover("Chapter fourteen. Freedom, and quantum technology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.technology()
        self.neutral()

    def theorem(self):
        hc = history_card(2006, r"John Conway and Simon Kochen", r"`The Free Will Theorem'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"SPIN: \ squared spin components along three perpendicular axes are 1, 0, 1, \ in some "
                       r"order", WAVE),
                      (r"TWIN: \ two entangled particles give matching answers along the same axis", ALICE),
                      (r"MIN: \ the experimenters' choices of axes are not functions of the past", CLASS),
                      (r"then the particles' responses are not functions of the past either", GOAL),
                      (r"`if we have free will, \ so do electrons': \ a slogan for Kochen--Specker plus locality",
                       ABS)], font_size=21, aligned_edge=LEFT, width=11.6, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "In 2006 John Conway and Simon Kochen put the no-go theorems together under a provocative name. "
            "<bookmark mark='a'/>Their premises: squared spin components of a spin-one particle along three "
            "perpendicular axes always come out one, zero and one in some order; <bookmark mark='b'/>two entangled "
            "particles give matching answers along the same axis; <bookmark mark='c'/>and the experimenters' choices "
            "of axes are not determined by the past. <bookmark mark='d'/>Then, by Kochen and Specker's theorem and "
            "locality, the particles' responses are not determined by the past either. <bookmark mark='e'/>Their "
            "slogan: if we have free will, so do electrons. The content is less dramatic than the slogan. Part 32 "
            "takes up what free will needs, and whether a free choice is just an undetermined one."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def technology(self):
        head = label(r"Bell's theorem, \ at work", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"quantum key distribution", r"Ekert \ (1991): \ share entangled pairs, \ test CHSH; \ a violation "
                                          r"guarantees no eavesdropper holds the key", OK),
            (r"device independence", r"the security proof trusts only the observed statistics, \ not the hardware: "
                                     r"\ demonstrated in 2022", WAVE),
            (r"certified randomness", r"Pironio et al. \ (2010): \ a Bell violation proves the outcomes were not "
                                      r"written in advance", ALICE),
            (r"quantum computing", r"entanglement and interference as a resource: \ Shor's algorithm factors in "
                                   r"polynomial time", ABS),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.0, label_size=22, text_size=21)
        with self.voiceover(
            "Bell's theorem has become an engineering tool. <bookmark mark='a'/>In 1991 Artur Ekert proposed "
            "distributing cryptographic keys with entangled pairs: Alice and Bob test the CHSH inequality, and a "
            "violation guarantees that no eavesdropper can hold a copy of the key, because any such correlation "
            "would be a local hidden variable. <bookmark mark='b'/>In the device-independent version, the proof "
            "trusts nothing about the hardware, only the observed statistics; experiments demonstrated it in 2022. "
            "<bookmark mark='c'/>The same logic certifies randomness: a Bell violation proves the outcomes were not "
            "written in advance, as Stefano Pironio and colleagues showed in 2010. <bookmark mark='d'/>And quantum "
            "computers use entanglement and interference as a resource; Peter Shor's algorithm factors numbers in "
            "polynomial time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def neutral(self):
        head = label(r"The interpretations and the machines", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"shut up and calculate", r"every interpretation predicts the same outputs for the same circuits", OK),
            (r"Deutsch", r"where is a factorization computed, \ if not in many worlds at once?", WAVE),
            (r"the reply", r"interference, \ not parallel universes, \ does the work: \ Bohmians and QBists build the "
                           r"same machines", ABS),
            (r"the exception", r"collapse theories predict new effects for big superpositions: \ a large quantum "
                               r"computer is a test", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4, x_text=-2.0, label_size=22, text_size=21)
        with self.voiceover(
            "Does any of this tell us which interpretation is right? <bookmark mark='a'/>For practical purposes, "
            "no: every interpretation predicts the same outputs for the same circuits. <bookmark mark='b'/>David "
            "Deutsch disagrees: where, he asks, is a large number factored, if not in many worlds at once? "
            "<bookmark mark='c'/>The usual reply is that interference, not parallel universes, does the work, and "
            "Bohmians and QBists would build exactly the same machines. <bookmark mark='d'/>The exception is "
            "spontaneous collapse, which predicts that very large superpositions break down. A large enough quantum "
            "computer is, among other things, a test of GRW."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
