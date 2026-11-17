from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ chemistry and machines", r"What is still unknown about bonds?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: chemistry and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def machines(self):
        head = heading(r"New players")
        rows = rows_of([
            (r"people now bargain, \ trade and cooperate with software agents, \ and agents with each other", WHITE),
            (r"the same games become tests for machines: \ do language-model agents offer fair splits, \ punish, \ "
             r"or collude?", MODEL),
            (r"and for people: \ do they reject unfair offers from a machine as they do from a person? \ chapter "
             r"five's computer-chosen offers suggest less", CROWD),
            (r"the questions are empirical, \ and the methods are the ones in this part: \ games with real stakes, "
             r"\ and predictions tested on new cases", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "The newest players in these games aren't people. People now bargain, trade and "
            "cooperate with software agents, and the agents with each other. <bookmark mark='b'/> The same games "
            "become tests for machines. Do language-model agents offer fair splits, punish, or collude? "
            "<bookmark mark='c'/> And for people: do they reject unfair offers from a machine as they do from a "
            "person? Chapter five's computer-chosen offers suggest they reject them less. "
            "<bookmark mark='d'/> The questions are empirical, and the methods are the ones in this part: games "
            "with real stakes, and predictions tested on new cases."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"is there compatibility specific to a pair, \ and could anything measured before meeting detect it?",
             PERSON),
            (r"how much of fairness in games is a preference, \ and how much a wish to look fair?", CROWD),
            (r"why does punishment sometimes target cooperators, \ and what institutions prevent it?", AUTH),
            (r"does social connection cause longer life, \ and which interventions could test it?", GOOD),
            (r"how will cooperation change when many of the players are machines?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. Is there compatibility specific to a pair, and could "
            "anything measured before two people meet detect it? <bookmark mark='b'/> How much of fairness in "
            "games is a preference, and how much a wish to look fair? <bookmark mark='c'/> Why does punishment "
            "sometimes target cooperators, and what institutions prevent it? <bookmark mark='d'/> Does social "
            "connection cause longer life, and which interventions could test it? <bookmark mark='e'/> And how will "
            "cooperation change when many of the players are machines?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
