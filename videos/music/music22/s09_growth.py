from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403

RULE_TXT = {"keep": r"keep", "repeat": r"repeat: \ x $\to$ x x", "neighbour": r"neighbour: \ x $\to$ x n", "passing": r"passing: \ x \ y $\to$ x p \ y",
            "arpeggio": r"arpeggiate: \ x $\to$ x c"}


class Growth(SoundScene):
    def construct(self):
        chapter(self, 8, r"Growing a melody", r"Can a grammar run forwards and write music?")
        self.rules()
        self.quiz()
        self.copy_rule()
        self.three()

    # ------------------------------------------------------------------
    def rules(self):
        rows_ = VGroup(*[label(RULE_TXT[k], font_size=28, color=TUNE if k != "keep" else GREY_A) for k in ("repeat", "neighbour", "passing", "arpeggio", "keep")]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 3.2 + DOWN * 0.1)
        side = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"reduction run backwards: \ elaboration", WHITE),
            (r"each rule halves a note's time and adds a servant", WHITE),
            (r"start from the Tune's skeleton, \ a note every four beats", WHITE),
            (r"apply the rules twice, \ choosing at random", WHITE),
            (r"Schenker's levels, \ grown downwards", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.2 + DOWN * 0.1)
        with self.voiceover(
            "A grammar can run forwards as well as backwards. <bookmark mark='a'/> Reduction removes servants; "
            "elaboration adds them. <bookmark mark='b'/> Each rule halves a note's time and adds a servant: repeat the "
            "note, step to a neighbour, pass to the next note, or arpeggiate the chord. <bookmark mark='c'/> Start from "
            "the Tune's skeleton, the reduction of chapter four at a note every four beats. <bookmark mark='d'/> Apply "
            "the rules twice, choosing which at random, and a new surface grows. <bookmark mark='e'/> It is Schenker's "
            "levels, grown downwards instead of peeled away."
        ) as vo:
            self.play(FadeIn(rows_), FadeIn(side[0]))
            for mark, r in zip("bcde", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("growth")
        c = clip("growth.quiz")
        card = listen_card(r"Two melodies over the Tune's first strain of chords. \ One is the Tune; \ one was grown by the grammar from the Tune's skeleton. \ "
                           r"Which is the grammar's, \ A or B? \ (Try not to recognize the Tune: \ listen for shape.)", width=10.6)
        with self.voiceover(
            "Two melodies over the same chords. One is the Tune; the other was grown by the grammar from the Tune's "
            "skeleton. Which one is the grammar's, A or B? You will recognize the Tune, so listen also for what makes "
            "the other one sound less like a tune."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = mroll(d["quiz"]["A"], width=5.0, height=1.8, lo=68, hi=86, total=16.0).move_to(LEFT * 3.2 + DOWN * 0.2)
        gB = mroll(d["quiz"]["B"], width=5.0, height=1.8, lo=68, hi=86, total=16.0).move_to(RIGHT * 3.2 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, gA.notes, [d["starts"]["A"] + n[1] * d["beat"] for n in d["quiz"]["A"]], hot=WHITE, base=TUNE)
            flash(snd, gB.notes, [d["starts"]["B"] + n[1] * d["beat"] for n in d["quiz"]["B"]], hot=WHITE, base=TUNE)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"the grammar's", font_size=26, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(r"the Tune", font_size=26, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "A is the grammar's. It obeys the harmony and moves by sensible steps, but it has no explicit rule tying later elaborations to earlier motives, though chance and its fixed durations can produce repeats. The Tune's charm is its repetitions, C C G G A A G, which the rules, choosing independently at every note, never think to make. Part 21's lesson returns: what a listener hears as a tune is largely repetition, and this grammar has no rule for it."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copy_rule(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"the missing rule: \ copy \ (elaborate this span as an earlier one was elaborated)", WHITE),
            (r"unrestricted copying of arbitrary sequences exceeds context-free power", WHITE),
            (r"finite named motives and bounded copies can be encoded context-freely", WHITE),
            (r"music needs it: \ motives, \ sequences, \ rounds, \ fugues", TUNE),
            (r"this independent-elaboration grammar lacks a mechanism for planned motivic recurrence", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"a rule for repetition", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What rule is missing? <bookmark mark='a'/> A rule that says: elaborate this span the way an earlier span was elaborated. Copy. <bookmark mark='b'/> Unrestricted exact copying of an arbitrarily long unknown sequence is beyond a context-free grammar: the choice at one place depends on the choice made at another. <bookmark mark='c'/> But a finite stock of named motives or bounded copies can be encoded context-freely; computational cost depends on the formalism. <bookmark mark='d'/> Music needs it everywhere: motives, sequences, rounds, fugues. <bookmark mark='e'/> Part 20's canons and Part 21's repetitions are not captured by this small independent-elaboration grammar, without proving that every such musical pattern exceeds context-free power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("growth")
        g = VGroup()
        for k, key in enumerate(d["order"]):
            r = mroll(d["grown"][key]["notes"], width=10.0, height=0.9, lo=66, hi=88, total=48.0, color=[TUNE, BLUE, EAR][k])
            cnt = d["rule_counts"][key]
            t = label(r", \ ".join(rf"{n} {v}" for n, v in sorted(cnt.items())), font_size=16, color=GREY_B)
            g.add(VGroup(r, t).arrange(DOWN, buff=0.12))
        g.arrange(DOWN, buff=0.35).move_to(DOWN * 0.3)
        head = label(r"three derivations from the same skeleton", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here are three whole derivations from the same skeleton, with the rules each one used. Every one is a "
            "valid elaboration; none is the Tune. Schenker's levels say what a melody can be grown from; they do not "
            "say which of the countless growths a composer chose, or why. That choice, the composer's, is what "
            "analysis tries to explain, and what a grammar of this kind leaves out."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.4), run_time=2.5)
        c = clip("growth.three")
        with self.listen(c) as snd:
            window(snd, r"three derivations, \ in turn", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for row, key in zip(g, d["order"]):
                s0 = d["three_starts"][key]
                flash(snd, row[0].notes, [s0 + n[1] * d["beat"] for n in d["grown"][key]["notes"]], hot=WHITE, base=[TUNE, BLUE, EAR][list(d["order"]).index(key)])
        with self.voiceover("Three tunes, all lawful, their memorability has not been tested: the grammar knows what may follow, not what should."):
            self.play(Indicate(head, color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()
