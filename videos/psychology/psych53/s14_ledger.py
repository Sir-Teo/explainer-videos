from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403

ROWS = [
    ("hawthorne_effect",
     "Four new rows. The first: in the Hawthorne lighting studies, output rose whenever the lighting changed, "
     "because the workers knew they were studied. <bookmark mark='a'/> The original: Roethlisberger and Dickson's "
     "account, 1939. <bookmark mark='b'/> The record: Levitt and List's analysis of the rediscovered output records, "
     "with slight evidence. <bookmark mark='c'/> Being observed can matter, but Hawthorne is a poor example of it. "
     "<bookmark mark='d'/> Story and record."),
    ("structured_interviews",
     "The second: structured interviews predict job performance better than unstructured ones. <bookmark mark='a'/> "
     "The original: McDaniel and colleagues' meta-analysis, 1994. <bookmark mark='b'/> The record: Schmidt and "
     "Hunter in 1998, and Sackett and colleagues in 2022, where the gap grew. <bookmark mark='c'/> The sizes of every "
     "validity changed; the advantage of structure didn't. <bookmark mark='d'/> Replicated."),
    ("ability_validity",
     "The third: ability tests predict job performance with a corrected validity of about zero point five, the best "
     "single predictor. <bookmark mark='a'/> The original: Schmidt and Hunter, 1998. <bookmark mark='b'/> The "
     "record: Sackett and colleagues' revision to about zero point three, and a reply defending larger corrections. "
     "<bookmark mark='c'/> The argument is about corrections, not data. <bookmark mark='d'/> Contested."),
    ("daycare_fine",
     "And the fourth: a small fine for late pick-up at daycare increased late pick-ups. <bookmark mark='a'/> The "
     "original: Gneezy and Rustichini, 2000, in ten centres. <bookmark mark='b'/> The record: a review finding "
     "crowding out in some settings and not in others. <bookmark mark='c'/> One striking field experiment, not "
     "repeated at scale. <bookmark mark='d'/> Not directly tested."),
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
            (r"the famous stories, \ Hawthorne and the fine, \ are the least tested", AUTH),
            (r"the plain result, \ structure, \ is the best replicated, \ like Part 28's goal setting", GOOD),
            (r"and the biggest number in the field moved by a third when its corrections were rethought", MODEL),
            (r"work psychology predicts, \ modestly; \ its honest numbers are smaller than its stories", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> The famous stories, Hawthorne and the fine, are the "
            "least tested. <bookmark mark='b'/> The plain result, structure, is the best replicated, like Part 28's goal setting. "
            "<bookmark mark='c'/> And the biggest number in the field moved by a third when its corrections were "
            "rethought. <bookmark mark='d'/> So here's the answer to this part's question. Work psychology predicts, "
            "modestly, and its honest numbers are smaller than its stories."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
