from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403

ROWS = [
    ("klm_accuracy",
     "Four new rows. The first: adding standard operator times predicts skilled users' task times to within about "
     "twenty percent. <bookmark mark='a'/> The original: Card, Moran and Newell, 1980, over twelve hundred "
     "predictions. <bookmark mark='b'/> The record: reviews by the Olsons and by John and Kieras, including models "
     "used in real design decisions like Project Ernestine. <bookmark mark='c'/> It predicts skilled, error-free "
     "work and nothing else; within that scope it holds up. <bookmark mark='d'/> Replicated."),
    ("graphical_perception",
     "The second: people judge quantities most accurately from position, then length, then angle, then area. "
     "<bookmark mark='a'/> The original: Cleveland and McGill, 1984. <bookmark mark='b'/> The record: Heer and "
     "Bostock's crowd-sourced replication in 2010, with the same order. <bookmark mark='c'/> The ranking is about "
     "judging values; for spotting a pattern or a trend, other encodings can do well. <bookmark mark='d'/> "
     "Replicated."),
    ("five_users",
     "The third: testing with five users finds about eighty-five percent of an interface's usability problems. "
     "<bookmark mark='a'/> The original: Nielsen and Landauer, 1993. <bookmark mark='b'/> The record: Spool and "
     "Schroeder's sites, and Faulkner's samples of five drawn from sixty users, finding far less, and very variable. "
     "<bookmark mark='c'/> The formula is right; its assumption that every problem is equally findable is not. "
     "<bookmark mark='d'/> Contested."),
    ("habit_21_days",
     "And the fourth: a new habit forms in about twenty-one days. <bookmark mark='a'/> The original: a remark in "
     "Maltz's self-help book of 1960. <bookmark mark='b'/> The record: Lally and colleagues' twelve-week study, with "
     "a median of sixty-six days and a range from eighteen to two hundred and fifty-four. <bookmark mark='c'/> The "
     "number was never a finding; the measured time is longer and varies widely. <bookmark mark='d'/> Failed."),
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
            (r"two are quantitative models of perception and action, \ tested against users: \ both replicate",
             GOOD),
            (r"two are rules of thumb that travelled faster than their evidence: \ one contested, \ one never a "
             r"finding", AUTH),
            (r"a design rule is only as good as the measurement under it", WHITE),
            (r"engineering with psychology works where the psychology is quantitative, \ and tested", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> Two are quantitative models of perception and action, "
            "tested against users, and both replicate. <bookmark mark='b'/> Two are rules of thumb that "
            "travelled faster than their evidence. One is contested, and one was never a finding at all. "
            "<bookmark mark='c'/> A design rule is only as good as the measurement under it. <bookmark mark='d'/> So "
            "here's the answer to this part's question. Engineering with psychology works where the psychology is "
            "quantitative, and tested."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
