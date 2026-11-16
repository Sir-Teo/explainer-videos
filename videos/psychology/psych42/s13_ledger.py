from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403

ROWS = [
    ("psychotherapy_vs_none",
     "Seven new rows today. The first: people who receive psychotherapy end better off than people who receive none. "
     "<bookmark mark='a'/> The original: Smith and Glass's meta-analysis, 1977. <bookmark mark='b'/> The record: "
     "decades of later trials, pooled again in 2019. <bookmark mark='c'/> The answer to Eysenck, with a size that "
     "depends on the control. <bookmark mark='d'/> Replicated."),
    ("published_effect_size",
     "The second: therapy for adult depression has an effect near zero point seven. <bookmark mark='a'/> The "
     "original: the whole literature, as pooled in 2019. <bookmark mark='b'/> The record: the unpublished trials, and "
     "the trials at low risk of bias. <bookmark mark='c'/> Real, but smaller. <bookmark mark='d'/> Replicated, "
     "smaller."),
    ("dodo_equivalence",
     "The third: all bona fide therapies are about equally effective. <bookmark mark='a'/> The original: Luborsky "
     "and colleagues, 1975. <bookmark mark='b'/> The record: a meta-analysis of direct comparisons, and one that "
     "found a small edge for cognitive behavioural therapy. <bookmark mark='c'/> Near-equivalence, with exceptions. "
     "<bookmark mark='d'/> Contested."),
    ("alliance_outcome",
     "The fourth: the alliance between client and therapist correlates with outcome. <bookmark mark='a'/> The "
     "original: Horvath and Symonds, 1991. <bookmark mark='b'/> The record: two hundred and ninety-five studies. "
     "<bookmark mark='c'/> The correlation holds; its direction is argued. <bookmark mark='d'/> Replicated."),
    ("dbt_self_harm",
     "The fifth: dialectical behaviour therapy reduces self-harm. <bookmark mark='a'/> The original: Linehan and "
     "colleagues, 1991. <bookmark mark='b'/> The record: a larger trial, and a meta-analysis. <bookmark mark='c'/> "
     "Smaller effects later, but there. <bookmark mark='d'/> Replicated."),
    ("debriefing",
     "The sixth: a session of debriefing after a trauma prevents post-traumatic stress. <bookmark mark='a'/> The "
     "original: Mitchell's method, 1983. <bookmark mark='b'/> The record: a Cochrane review, and a three-year "
     "follow-up. <bookmark mark='c'/> No prevention, and possible harm. <bookmark mark='d'/> Failed."),
    ("scared_straight",
     "And the seventh: confronting young offenders in prisons deters crime. <bookmark mark='a'/> The original: the "
     "programme and its documentary, 1978. <bookmark mark='b'/> The record: a review of the randomized trials. "
     "<bookmark mark='c'/> It increased offending. <bookmark mark='d'/> Failed."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
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
        head = heading(r"Part 42 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "replicated, smaller": 1, "contested": 1, "failed": 2}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=16, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 17, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ therapy beats no therapy, \ the alliance tracks outcome, \ and DBT reduces self-harm",
             GOOD),
            (r"what shrank or is argued: \ the published size of the effect, \ and the dodo bird",
             STATUS_COLOR["contested"]),
            (r"what failed: \ debriefing and Scared Straight, \ both of which did harm", AUTH),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: therapy beats no therapy, the alliance tracks outcome, and "
            "dialectical behaviour therapy reduces self-harm. <bookmark mark='b'/> What shrank, or is argued: the "
            "published size of the effect, and the dodo bird. <bookmark mark='c'/> What failed: debriefing and Scared "
            "Straight, both of which did harm."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
