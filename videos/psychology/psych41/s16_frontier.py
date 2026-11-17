from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ precision, \ polygenic scores and new drugs", r"What is still unknown?",
                            lit=(), part=PART, scale=("molecule", "circuit", "person"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: precision, polygenic scores and new drugs."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        rows = rows_of([
            (r"precision: \ predictive-coding accounts must make predictions that rival accounts do not, \ and "
             r"measure precision in a person, \ not just fit it afterwards (Parts 58 and 59)", SYMP),
            (r"polygenic scores: \ they predict schizophrenia risk better than chance across a population, \ but "
             r"explain a small share of it, \ too little to diagnose or screen one person", MODEL),
            (r"new drugs: \ in 2024 the US regulator approved the first antipsychotic that does not act mainly by "
             r"blocking dopamine D2 receptors, \ but on muscarinic acetylcholine receptors", GOOD),
            (r"each tests the chapter's models: \ if psychosis runs through dopamine, \ a drug that works upstream "
             r"of it is a clue to the circuit", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "At the frontier, three ideas. <bookmark mark='a'/> Precision: predictive-coding accounts must make "
            "predictions that rival accounts don't, and measure precision in a person rather than fit it afterwards. "
            "That's Parts 58 and 59. <bookmark mark='b'/> Polygenic scores: they predict schizophrenia risk better "
            "than chance across a population, but explain a small share of it, too little to diagnose or screen one "
            "person. <bookmark mark='c'/> New drugs: in 2024 the American regulator approved the first antipsychotic "
            "that doesn't act mainly by blocking dopamine D2 receptors, but on muscarinic acetylcholine receptors. "
            "<bookmark mark='d'/> Each tests this part's models. If psychosis runs through dopamine, a drug that "
            "works upstream of it is a clue to the circuit."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"are priors too weak in psychosis, \ too strong, \ or both at different levels?", SYMP),
            (r"is hallucination-proneness a trait, \ a state, \ or both?", MODEL),
            (r"why do most people who use drugs never become addicted?", PERSON),
            (r"how much of the rise in autism and ADHD diagnoses is a change in people, \ and how much in "
             r"diagnosis?", GOOD),
            (r"can the transdiagnostic dials be measured reliably in one person?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. Are priors too weak in psychosis, too strong, or both at different levels? "
            "<bookmark mark='b'/> Is hallucination-proneness a trait, a state, or both? <bookmark mark='c'/> Why do "
            "most people who use drugs never become addicted? <bookmark mark='d'/> How much of the rise in autism and "
            "ADHD diagnoses is a change in people, and how much a change in diagnosis? <bookmark mark='e'/> And can "
            "the transdiagnostic dials be measured reliably in one person?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
