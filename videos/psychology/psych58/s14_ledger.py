from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403

ROWS = [
    ("sparse_v1",
     "Four new rows. The first: a sparse code for natural images learns receptive fields like V1's simple cells. "
     "<bookmark mark='a'/> The original: Olshausen and Field, 1996. <bookmark mark='b'/> The record: independent "
     "component analysis, a comparison with measured cells, and a survey of real fields. <bookmark mark='c'/> The "
     "computation reproduces; the match is qualitative. <bookmark mark='d'/> Replicated."),
    ("efficient_bias",
     "The second: an efficient code predicts biases away from common values. <bookmark mark='a'/> The original: Wei "
     "and Stocker, 2015. <bookmark mark='b'/> The record: their lawful relation between bias and threshold, across "
     "many data sets. <bookmark mark='c'/> Strongest where the prior is measured. <bookmark mark='d'/> Replicated."),
    ("prediction_error_neurons",
     "The third: cortex has distinct prediction-error neurons, as predictive coding requires. <bookmark mark='a'/> "
     "The original: Rao and Ballard, 1999. <bookmark mark='b'/> The record: mismatch neurons in mouse V1, and a review "
     "of the evidence. <bookmark mark='c'/> Responses to the unexpected are robust; dedicated error units are not "
     "established. <bookmark mark='d'/> Contested."),
    ("free_energy",
     "And the fourth: everything a brain does minimizes free energy. <bookmark mark='a'/> The original: Friston, "
     "2010. <bookmark mark='b'/> The record: an analysis of what kind of claim it is. <bookmark mark='c'/> A "
     "framework, whose models must be tested one by one. <bookmark mark='d'/> Not directly tested, and the question "
     "is whether it can be."),
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
            (r"principles that predicted measured quantities held: \ efficient codes and their biases", GOOD),
            (r"the bigger the claim, \ the weaker the test: \ error neurons are contested, \ the free-energy "
             r"principle is not tested", AUTH),
            (r"each principle earns its keep through models with measured inputs", MODEL),
            (r"one principle does not yet explain the mind; \ several explain a great deal of perception", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> Principles that predicted measured quantities held: "
            "efficient codes and their biases. <bookmark mark='b'/> The bigger the claim, the weaker the test. Error "
            "neurons are contested, and the free-energy principle isn't tested. <bookmark mark='c'/> Each principle "
            "earns its keep through models with measured inputs. <bookmark mark='d'/> So here's the answer to this "
            "part's question. One principle doesn't yet explain the mind, but several explain a great deal of "
            "perception."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
