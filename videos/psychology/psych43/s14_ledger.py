from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403

ROWS = [
    ("registered_reports",
     "Two new rows today, about replication itself. The first: studies accepted before their results are known "
     "report positive results far less often. <bookmark mark='a'/> The original: Allen and Mehler, 2019. "
     "<bookmark mark='b'/> The record: a comparison of registered reports with standard articles in psychology. "
     "<bookmark mark='c'/> Forty-four percent positive, against ninety-six. <bookmark mark='d'/> Replicated."),
    ("hidden_moderators",
     "The second: replications often fail because of hidden moderators of setting and sample. "
     "<bookmark mark='a'/> The original: Van Bavel and colleagues, 2016. <bookmark mark='b'/> The record: Many Labs "
     "2, and a study of heterogeneity across direct replications. <bookmark mark='c'/> For most effects, variation "
     "across labs is small. <bookmark mark='d'/> Contested."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.targets()

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

    def targets(self):
        rows = ledger.rows(part=PART)
        assert {f.status for f in rows} == {"replicated", "contested"} and len(rows) == 2
        head = heading(r"And the two targets")
        c = load("confirm")
        items = rows_of([
            (rf"verbal overshadowing (Part 21's row): \ this part's estimate, \ {-100 * c['vo_est']:.0f} fewer correct "
             rf"picks per 100, \ agrees with its status, \ replicated, \ smaller", GOOD),
            (rf"ego depletion (Part 28's row): \ this part's estimate, \ $g = {c['ed_est']:.2f}$, \ agrees with its "
             rf"status, \ failed", AUTH),
            (r"the Stroop effect (Part 18's row): \ yours, \ on the site, \ joins the thousands that hold", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "And the two targets. <bookmark mark='a'/> Verbal overshadowing, Part 21's row: this part's estimate agrees "
            "with its status, replicated, and smaller. <bookmark mark='b'/> Ego depletion, Part 28's row: this part's "
            "estimate agrees with its status, failed. <bookmark mark='c'/> And the Stroop effect, Part 18's row: your "
            "own run, on the site, joins the thousands that hold."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
