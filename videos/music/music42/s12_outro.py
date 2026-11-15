from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        c = clip("tune.variation42")
        head = VGroup(label(r"Variation 42", font_size=48, color=TUNE), label(r"the Tune, \ searched", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g = scored(d["melody"], d["chords"], width=11.4, height=1.9, lo=55, hi=81, size=14).move_to(UP * 0.5)
        ders = VGroup()
        for k, der in enumerate(d["derivations"]):
            txt = r"cadence" if k == len(d["derivations"]) - 1 else (r"the four notes" if der == [] else (r"bent" if der is None else r" + ".join(x.replace("first three notes", "3 notes") for x in der)))
            x = g.frame.get_left()[0] + 11.4 * (k + 0.5) / g.nb
            ders.add(label(txt, font_size=12, color=BLUE if der else (GREY_A if der is None else TUNE)).move_to([x, g.frame.get_bottom()[1] - 0.3 - 0.28 * (k % 2), 0]))
        thrown = VGroup(*[scored(s["melody"], None, width=2.6, height=0.8, lo=50, hi=86, color=GREY_B) for s in d["shown"]]).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=1.05)
        for t_ in thrown:
            VGroup(*t_.roll.notes).set_opacity(0.5)
        tl_ = label(rf"thrown away: \ {sum(d['rejected'].values()):,} of {d['drafts']:,} drafts, \ four of them here", font_size=16, color=GREY_A).next_to(thrown, UP, buff=0.12)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the searcher takes "
            "the Tune's first four notes, C, C, G, G, as its motive, and composes eight bars over chords of the Tune's kind. "
            f"Of {say(d['drafts'])} drafts it kept number {say(d['kept'])}; <bookmark mark='b'/> below, faint, are four of the "
            f"{say(sum(d['rejected'].values()))} it threw away. You will hear the Tune's first phrase, and then the variation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(ders))
            vo.wait_until("b")
            self.play(FadeIn(thrown), FadeIn(tl_))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"Variation 42", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            theme = label(r"first, \ the Tune's first phrase", font_size=20, color=EAR).next_to(g, UP, buff=0.15)
            snd.show(theme)
            snd.drive(theme, lambda m, t: m.set_opacity(1.0 if t < st["variation"] else 0.0))
            pulse(snd, theme, 0.0, st["variation"] - 0.1, buff=0.08)
            cursor(snd, g, st["variation"], 0.42)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row forty-two of the ledger: {say(v['seconds'], 1)} seconds; the measurement is the search itself: draft "
            f"{say(d['kept'])} of {say(d['drafts'])} kept, {say(sum(d['rejected'].values()))} rejected by the critics, and "
            f"{say(d['survivors'])} scored."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a motive and its operations: \ functions from melodies to melodies",
            r"developing variation: \ a phrase grown from four notes",
            r"tension can be planned, \ and measured against the plan",
            r"rules shrink the space: \ 2.5 billion melodies to 9,252",
            r"dice games put the knowledge in the table; \ generate and test puts it in the critics",
            r"more memory, \ more copying: \ plausibility bought with plagiarism",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A motive and its operations are functions from melodies to melodies. "
            "<bookmark mark='a'/> Developing variation grows a phrase from four notes. <bookmark mark='b'/> Tension can be "
            "planned, and measured against the plan. <bookmark mark='c'/> Rules shrink the space of melodies, from two and a "
            "half billion to nine thousand. <bookmark mark='d'/> The dice games put the composer's knowledge in the table; "
            "generate and test puts it in the critics. <bookmark mark='e'/> And a chain that remembers more copies more: "
            "plausibility bought with plagiarism."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A dice game has 16 bars; \ bar 8 and bar 16 have one option, \ the rest 11 distinct ones. \ How many distinct pieces?",
            r"Prove that the entropy of two dice's sum is about 3.27 bits, \ and that a piece's entropy is the sum over its bars.",
            r"\textbf{Ear.} \ The lab plays melodies from chains of random order; \ say which order made each.",
            r"\textbf{Build.} \ Add a critic of your own to the searcher and compare what it keeps.",
            r"$\bigstar$ \ Can novelty and value be measured separately, \ and do they trade off?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"performing: \ the search continues on stage", [43]),
            (r"expectation and emotion", [46]),
            (r"MIDI, \ sequencers and the workstation", [53]),
            (r"machines that compose", [65]),
            (r"generative audio", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In performing, where the search continues on stage. In expectation and emotion. In "
            "the sequencer and the workstation. In machines that compose. And in generative audio."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"composers", r"keep sketchbooks: \ many drafts, \ judged later with fresh ears"),
            (r"songwriters", r"write ten hooks to keep one"),
            (r"game composers", r"write rules and fragments that a program recombines in play"),
            (r"teachers", r"set constraints: \ a motive, \ a form, \ a time limit"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Composers keep sketchbooks, many drafts judged later with fresh ears. Songwriters write ten "
            "hooks to keep one. Game composers write rules and fragments that a program recombines during play, a dice game "
            "with a better table. And teachers set constraints: a motive, a form, a time limit."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. Schoenberg, \ \textit{Fundamentals of Musical Composition} \ (1967)",
             r"L. Hiller and L. Isaacson, \ \textit{Experimental Music} \ (1959)",
             r"M. Boden, \ \textit{The Creative Mind} \ (1990; \ 2nd ed. 2004)",
             r"D. Cope, \ \textit{Experiments in Musical Intelligence} \ (1996)"],
            [r"F. Lerdahl and C. L. Krumhansl, \ `Modeling tonal tension' \ (2007)",
             r"G. Ritchie, \ `Some empirical criteria for attributing creativity to a computer program' \ (2007)",
             r"A. Jordanous, \ `A standardised procedure for evaluating creative systems' \ (2012)",
             r"F. P. Brooks and others, \ `An experiment in musical composition' \ (1957)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what does a performer add that the score leaves out?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VII: \ the craft", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"A searcher wrote notes on a grid, \ every beat exactly in time.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 43", font_size=32, color=GREY_B), label(r"Performing", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Our searcher wrote notes on a grid, every beat exactly in time. <bookmark mark='a'/> What does a performer add "
            "that the score leaves out? <bookmark mark='b'/> Next time. Part 43: Performing."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
