from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403

ROWS = [
    ("vigilance_decrement",
     "Four new rows. The first: in a long watch for rare signals, detection falls within the first half hour and "
     "keeps falling. <bookmark mark='a'/> The original: Mackworth's clock, 1948. <bookmark mark='b'/> The record: the "
     "meta-analysis by See and colleagues, and a review of vigilance as hard, stressful work. <bookmark mark='c'/> "
     "Rare signals, long watches and hard discriminations make it worse, and breaks, feedback and aids reduce it. "
     "<bookmark mark='d'/> Replicated."),
    ("surgical_checklist",
     "The second: a short surgical safety checklist reduces deaths and complications. <bookmark mark='a'/> The "
     "original: Haynes and colleagues, 2009, before and after in eight hospitals. <bookmark mark='b'/> The record: no "
     "change under Ontario's mandate, and fewer complications in a stepped-wedge trial. <bookmark mark='c'/> Where "
     "teams adopt it, it helps. Imposed as paperwork, the effect shrinks or vanishes. <bookmark mark='d'/> Contested."),
    ("automation_complacency",
     "The third: people monitoring reliable automation detect its rare failures less well, and less well the more "
     "reliable it has been. <bookmark mark='a'/> The original: Parasuraman, Molloy and Singh, 1993. "
     "<bookmark mark='b'/> The record: a review of complacency and automation bias across laboratory and field tasks, "
     "experts included. <bookmark mark='c'/> It's an allocation of attention that makes sense most of the time, which "
     "is why training alone barely removes it. <bookmark mark='d'/> Replicated."),
    ("fatigue_alcohol",
     "And the fourth: seventeen to twenty-four hours awake impairs performance about as much as a blood alcohol of "
     "zero point zero five to zero point one percent. <bookmark mark='a'/> The original: Dawson and Reid, 1997. "
     "<bookmark mark='b'/> The record: Williamson and Feyer's battery of tests, with a similar scale. "
     "<bookmark mark='c'/> The equivalence varies by task, but a long shift ends with an impairment the law forbids "
     "when it comes from a drink. <bookmark mark='d'/> Replicated."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("society",),
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
        assert len(rows) == 4
        head = heading(r"What the four have in common")
        items = rows_of([
            (r"three are effects of the person in the system: \ attention over time, \ attention under automation, \ "
             r"and the clock", WHITE),
            (r"those replicate well, \ because they rest on Parts 10, \ 12 and 18", GOOD),
            (r"the contested one is an intervention: \ it works through a team and a culture, \ and a mandate cannot "
             r"copy those", AUTH),
            (r"the human limits are stable; \ the fixes depend on the system they are put into", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> Three are effects of the person in the system: "
            "attention over time, attention under automation, and the clock. <bookmark mark='b'/> Those replicate "
            "well, because they rest on Parts 10, 12 and 18. <bookmark mark='c'/> The contested one is an "
            "intervention. It works through a team and a culture, and a mandate can't copy those. "
            "<bookmark mark='d'/> The human limits are stable. The fixes depend on the system they're put into."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
