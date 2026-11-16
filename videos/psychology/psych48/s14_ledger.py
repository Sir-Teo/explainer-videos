from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403

ROWS = [
    ("power_law_practice",
     "Two new rows. The first: response time falls with practice as a power function, for each learner. "
     "<bookmark mark='a'/> The original: Newell and Rosenbloom, 1981. <bookmark mark='b'/> The record: fitted person "
     "by person, practice data favour the exponential. <bookmark mark='c'/> The power law appears in averages, as "
     "chapter nine computed. <bookmark mark='d'/> Failed, at the level of the learner."),
    ("parameters_as_traits",
     "The second: fitted model parameters, such as a learning rate, are stable traits that generalize across tasks "
     "and can serve as clinical markers. <bookmark mark='a'/> The original: the programme of computational "
     "psychiatry, as Montague and colleagues set it out in 2012. <bookmark mark='b'/> The record: parameters that "
     "often fail to generalize across tasks, and test-retest reliabilities that are often low. "
     "<bookmark mark='c'/> Useful summaries within a task; as traits, not yet. <bookmark mark='d'/> Contested."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def row(self, key, text):
        card = ledger_card(self._get(key), width=12.8, font_size=21)
        with self.voiceover(text) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        assert len(rows) == 2
        head = heading(r"What the two have in common")
        items = rows_of([
            (r"both are claims about individuals made from fits", WHITE),
            (r"the first fitted an average and called it a learner; \ the second fitted learners and called the fit "
             r"a trait", AUTH),
            (r"both were caught by the checks of this part: \ fit person by person, \ and test recovery and "
             r"reliability before interpreting a parameter", GOOD),
            (r"a parameter is a measurement; \ Part 3's questions apply to it", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the two have in common. <bookmark mark='a'/> Both are claims about individuals made from fits. "
            "<bookmark mark='b'/> The first fitted an average and called it a learner. The second fitted learners and "
            "called the fit a trait. <bookmark mark='c'/> Both were caught by the checks of this part: fit person by "
            "person, and test recovery and reliability before interpreting a parameter. <bookmark mark='d'/> A "
            "parameter is a measurement, and Part 3's questions apply to it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
