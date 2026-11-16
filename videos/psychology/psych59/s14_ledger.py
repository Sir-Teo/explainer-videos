from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403

ROWS = [
    ("reliability_paradox",
     "Four new rows. The first: tasks with robust group effects measure individual differences poorly. "
     "<bookmark mark='a'/> The original: Hedge, Powell and Sumner, 2018. <bookmark mark='b'/> The record: a large "
     "retest study of self-regulation tasks, and a hierarchical account of the noise. <bookmark mark='c'/> The paradox "
     "is arithmetic. <bookmark mark='d'/> Replicated."),
    ("model_based_compulsivity",
     "The second: weaker model-based control goes with a compulsive dimension that cuts across diagnoses. "
     "<bookmark mark='a'/> The original: Gillan and colleagues, 2016. <bookmark mark='b'/> The record: an incentive "
     "study, and patients with and without a diagnosis of OCD. <bookmark mark='c'/> A small population association, "
     "limited by reliability. <bookmark mark='d'/> Replicated."),
    ("connectivity_biotypes",
     "The third: brain connectivity divides depression into four biotypes. <bookmark mark='a'/> The original: "
     "Drysdale and colleagues, 2017. <bookmark mark='b'/> The record: a methodological replication with unstable "
     "clusters. <bookmark mark='c'/> Circular selection guarantees clusters that differ. <bookmark mark='d'/> "
     "Contested."),
    ("cross_trial_prediction",
     "And the fourth: a model trained in one trial predicts who responds in others. <bookmark mark='a'/> The "
     "original: Chekroud and colleagues, 2016. <bookmark mark='b'/> The record: five antipsychotic trials, with models "
     "close to chance across them. <bookmark mark='c'/> Accuracy at home overstates accuracy abroad. "
     "<bookmark mark='d'/> Failed."),
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
            (r"group findings are real; \ measuring individuals is the bottleneck", GOOD),
            (r"the failures share one cause: \ an analysis that sees its own answer (circular clusters, \ in-sample "
             r"accuracy)", AUTH),
            (r"the fixes are old: \ reliability, \ held-out data, \ independent samples", MODEL),
            (r"a model of the mind can tell a clinician something new only after it passes Part 3's and Part 4's tests "
             r"in individuals; \ none has yet", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> The group findings are real. Measuring individuals is "
            "the bottleneck. <bookmark mark='b'/> The failures share one cause: an analysis that sees its own answer, "
            "in circular clusters and in-sample accuracy. <bookmark mark='c'/> The fixes are old: reliability, "
            "held-out data, and independent samples. <bookmark mark='d'/> So here's the answer to this part's "
            "question. A model of the mind can tell a clinician something new only after it passes Part 3's and Part "
            "4's tests in individuals, and none has yet."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
