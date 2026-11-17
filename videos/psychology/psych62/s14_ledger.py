from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403

ROWS = [
    ("rotation_slope_reliability",
     "The last row of the Ledger is this dissertation's own. <bookmark mark='a'/> The original: this registered "
     "report, 2026, forty of fifty-four people. <bookmark mark='b'/> The record: none yet; it needs another data set, "
     "and a retest over weeks. <bookmark mark='c'/> One deviation, reported; the estimate leaned against the "
     "paradox. <bookmark mark='d'/> Not directly tested, like every new finding on the day it's made."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger: \ the last row", r"What does this part add?", lit=(), part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger: the last row."):
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
            if len(card.record):
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
        assert len(rows) == 1
        head = heading(r"Why the series ends on an open row")
        items = rows_of([
            (r"every row in the Ledger began like this one: \ a single study, \ honestly reported", MODEL),
            (r"whether it holds is decided by the studies that come after, \ not by the one that made it", PERSON),
            (r"the data and the code are open: \ anyone can rerun it, \ or run it on new people", GOOD),
            (r"the Ledger is not finished; \ it has a date, \ and the next row is yours", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "Why does the series end on an open row? <bookmark mark='a'/> Every row in the Ledger began like this "
            "one: a single study, honestly reported. <bookmark mark='b'/> Whether it holds is decided by the studies "
            "that come after, not by the one that made it. <bookmark mark='c'/> The data and the code are open, so "
            "anyone can rerun it, or run it on new people. <bookmark mark='d'/> The Ledger isn't finished. It has a "
            "date, and the next row is yours."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
