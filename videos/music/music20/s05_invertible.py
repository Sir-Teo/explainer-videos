from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403

STEP = ["unison", "2nd", "3rd", "4th", "5th", "6th", "7th", "octave", "9th", "10th", "11th", "12th"]


class Invertible(SoundScene):
    def construct(self):
        chapter(self, 4, r"Invertible counterpoint", r"Can two lines swap places?")
        self.idea()
        self.quiz()
        self.tables()

    # ------------------------------------------------------------------
    def idea(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"two lines, \ one above the other", WHITE),
            (r"move the upper line down an octave, \ below the other", WHITE),
            (r"every interval s scale steps wide becomes 7 $-$ s", WHITE),
            (r"third $\leftrightarrow$ sixth, \ unison $\leftrightarrow$ octave: \ fine; \ but fifth $\to$ fourth", EAR),
            (r"so a line that will swap places must avoid fifths, \ or treat them as dissonances", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"invertible counterpoint at the octave", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A fugue reuses its material in new arrangements, and one of the commonest is to swap two lines, the upper "
            "going below. <bookmark mark='a'/> Take two lines, one above the other. <bookmark mark='b'/> Move the "
            "upper one down an octave, so that it is now the lower. <bookmark mark='c'/> Every interval between them, "
            "counted in scale steps, turns into its complement: a third becomes a sixth, a sixth a third, an octave a "
            "unison. <bookmark mark='d'/> But a fifth becomes a fourth, and a fourth over the bass is a dissonance. "
            "<bookmark mark='e'/> So a counter-line meant to swap places at the octave must avoid fifths, or treat them "
            "like dissonances, passing through them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("invertible")
        c = clip("invertible.two")
        L = d["lines"]
        card = listen_card(r"Two counter-lines were written below the Tune's phrase. \ Each is now moved above it. \ Which survives the move, \ A or B?", width=10.0)
        with self.voiceover(
            "Two counter-lines were written below the Tune's first phrase by the solver: line A freely, line B with "
            "no fifths against the phrase. Each has now been moved above the phrase. Which still sounds right, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(L["plain"]["inverted"], width=5.4, height=3.0, lo=69, hi=93).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(L["safe"]["inverted"], width=5.4, height=3.0, lo=69, hi=93).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, gA, L["plain"]["inverted"], start=d["starts"]["A"])
            sing_voices(snd, gB, L["safe"]["inverted"], start=d["starts"]["B"])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        fa, fb = L["plain"]["faults_inverted"], L["safe"]["faults_inverted"]
        res = VGroup(label(rf"{fa['dissonant']} dissonant beats", font_size=24, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(rf"{fb['dissonant']} dissonant beats", font_size=24, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            f"B. Below the phrase, both lines were clean. Moved above it, line A's fifths have become fourths over the "
            f"bass, {say(fa['dissonant'])} of them on the beat; line B, written without fifths, comes through with "
            f"{say(fb['dissonant'])}. Bach planned his countersubjects like line B, so that they could go above or below "
            "the subject."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tables(self):
        d = load("invertible")
        cols = VGroup()
        for at, name in (("7", r"at the octave"), ("9", r"at the tenth"), ("11", r"at the twelfth")):
            tab = d["tables"][at]
            rows_ = VGroup()
            for s in ("0", "2", "4", "5", "7"):
                r = tab[s]
                b = r["becomes"]
                col = EAR if not r["consonant_after"] else (BLUE if (r["perfect_after"] and s == "2") else WHITE)
                rows_.add(label(rf"{STEP[int(s)]} $\to$ {STEP[b]}", font_size=27, color=col))
            rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            cols.add(VGroup(label(name, font_size=30, color=TUNE), rows_).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(UP * 0.3)
        cap = VGroup(label(r"pink: \ a consonance becomes a dissonance; \ blue: \ thirds become octaves \ (parallel thirds turn into parallel octaves)", font_size=21, color=GREY_A),
                     label(r"each kind of invertibility forbids something different", font_size=24, color=WHITE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Lines can also be swapped at other distances. <bookmark mark='a'/> At the octave, the fifth is the problem. "
            "<bookmark mark='b'/> At the tenth, every consonance stays a consonance, but thirds become octaves, so a "
            "pair of lines moving in parallel thirds, the sweetest thing in two voices, turns into forbidden parallel "
            "octaves. <bookmark mark='c'/> At the twelfth, fifths become octaves and thirds tenths, but the sixth "
            "becomes a seventh. Each kind of invertibility forbids something different, and the treatises of Bach's "
            "time taught them as separate crafts."
        ) as vo:
            self.play(FadeIn(cols[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
