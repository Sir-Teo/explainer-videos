from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

ROWS = [
    ("rosenhan_pseudopatients",
     "Five new rows today. The first: healthy people faking one symptom were admitted to psychiatric hospitals and "
     "never detected. <bookmark mark='a'/> The original: Rosenhan, 1973. <bookmark mark='b'/> The record: Cahalan's "
     "investigation of his papers. <bookmark mark='c'/> Never replicated, and the data are in serious doubt. "
     "<bookmark mark='d'/> Contested."),
    ("clinical_vs_statistical",
     "The second: formulas predict health and behaviour at least as well as expert judgment, and often better. "
     "<bookmark mark='a'/> The original: Meehl, 1954. <bookmark mark='b'/> The record: Dawes's improper models, and "
     "a meta-analysis of the comparisons. <bookmark mark='c'/> One of the most consistent findings in applied "
     "psychology. <bookmark mark='d'/> Replicated."),
    ("dimensional_structure",
     "The third: most disorders are continua with conventional cut-offs. <bookmark mark='a'/> The original: Haslam "
     "and colleagues' review, 2012. <bookmark mark='b'/> The record: their 2020 meta-analysis. "
     "<bookmark mark='c'/> A few may be categories; for most, the line is a decision. <bookmark mark='d'/> "
     "Replicated."),
    ("p_factor",
     "The fourth: one general factor, p, accounts for much of the overlap among disorders, and means a shared "
     "liability. <bookmark mark='a'/> The original: Caspi and colleagues, 2014. <bookmark mark='b'/> The record: "
     "the HiTOP consortium's hierarchy. <bookmark mark='c'/> The pattern is found again and again; what it means is "
     "argued. <bookmark mark='d'/> Contested."),
    ("diagnostic_biomarkers",
     "And the fifth: a laboratory test can diagnose a mental disorder, as the dexamethasone suppression test was "
     "once claimed to diagnose melancholic depression. <bookmark mark='a'/> The original: Carroll and colleagues, "
     "1981. <bookmark mark='b'/> The record: a review of why no such test has reached the clinic. "
     "<bookmark mark='c'/> No laboratory test is used to diagnose a common mental disorder. <bookmark mark='d'/> "
     "Failed."),
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
        head = heading(r"Part 39 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 2, "contested": 2, "failed": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ formulas beat clinical judgment, \ and most disorders are dimensions", GOOD),
            (r"what failed: \ laboratory tests for diagnosis, \ so far", AUTH),
            (r"what is argued: \ Rosenhan's study, \ and what the p factor means", YOU),
            (r"diagnosis became reliable by agreement; \ it has not yet become valid by explanation", MODEL),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: formulas beat clinical judgment, and most disorders are "
            "dimensions. <bookmark mark='b'/> What failed: laboratory tests for diagnosis, so far. "
            "<bookmark mark='c'/> What's argued: Rosenhan's study, and what the p factor means. "
            "<bookmark mark='d'/> Diagnosis became reliable by agreement. It hasn't yet become valid by explanation."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
