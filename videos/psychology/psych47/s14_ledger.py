from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403

ROWS = [
    ("items_as_fixed",
     "Three new rows. The first: treating a study's stimuli as fixed, not as a sample, finds effects that don't "
     "generalize far more often than promised. <bookmark mark='a'/> The original: Clark, 1973. <bookmark mark='b'/> "
     "The record: simulations by Judd, Westfall and Kenny, and by Barr and colleagues. <bookmark mark='c'/> A result of "
     "arithmetic as much as of experiment, as the opening computed. <bookmark mark='d'/> Replicated."),
    ("emotional_inertia",
     "The second: emotions that linger predict depression, beyond how much they vary. <bookmark mark='a'/> The "
     "original: Kuppens, Allen and Sheeber, 2010. <bookmark mark='b'/> The record: across many diary datasets, "
     "dynamic measures added little beyond a person's mean and spread. <bookmark mark='c'/> Inertia relates to "
     "depression, but shares most of its signal with simpler summaries, and is hard to estimate. "
     "<bookmark mark='d'/> Contested."),
    ("early_warning_depression",
     "The third: rising autocorrelation and variance warn of a transition into or out of depression. "
     "<bookmark mark='a'/> The original: van de Leemput and colleagues, 2014. <bookmark mark='b'/> The record: one "
     "person followed through a relapse, and prospective tests in many people with weak signals. "
     "<bookmark mark='c'/> Sound in theory; unsettled for moods measured by diary. <bookmark mark='d'/> Contested."),
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
        assert len(rows) == 3
        head = heading(r"What the three have in common")
        items = rows_of([
            (r"each is about the level at which a claim is made: \ items, \ persons, \ or moments", WHITE),
            (r"the first is settled because it is arithmetic: \ ignore a source of variation, \ and the error rate "
             r"rises", GOOD),
            (r"the other two ask a lot of short, \ noisy series from single people", AUTH),
            (r"idiographic claims need idiographic data: \ many occasions, \ for each person", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the three have in common. <bookmark mark='a'/> Each is about the level at which a claim is made: "
            "items, persons, or moments. <bookmark mark='b'/> The first is settled because it's arithmetic. Ignore a "
            "source of variation, and the error rate rises. <bookmark mark='c'/> The other two ask a lot of short, "
            "noisy series from single people. <bookmark mark='d'/> Claims about a person need data about a person: "
            "many occasions, for each one."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
