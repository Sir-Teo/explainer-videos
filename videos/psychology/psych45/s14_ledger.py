from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403

ROWS = [
    ("cat_efficiency",
     "Two new rows. The first: an adaptive test reaches the precision of a fixed test with far fewer items, often "
     "about half. <bookmark mark='a'/> The original: David Weiss, 1982. <bookmark mark='b'/> The record: the adaptive "
     "testing programmes reviewed by Wainer and colleagues, and the adaptive health questionnaires of PROMIS. "
     "<bookmark mark='c'/> The saving depends on the bank, and exposure must be controlled. <bookmark mark='d'/> "
     "Replicated, as chapter seven computed."),
    ("deep_knowledge_tracing",
     "The second: a neural network predicts students' answers far better than Bayesian knowledge tracing. "
     "<bookmark mark='a'/> The original: Piech and colleagues, 2015. <bookmark mark='b'/> The record: knowledge "
     "tracing extended with forgetting and abilities matched it, and duplicated records had inflated the gain. "
     "<bookmark mark='c'/> Neural models do predict somewhat better on large logs, but much of the first gap came from "
     "a weak baseline and a data artefact. <bookmark mark='d'/> Replicated, smaller."),
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
        assert len(rows) == 2
        head = heading(r"What the two have in common")
        items = rows_of([
            (r"both are claims about efficiency: \ fewer items, \ better predictions", WHITE),
            (r"the first held because the model behind it was tested first: \ calibrated items, \ known information",
             GOOD),
            (r"the second shrank because the comparison was unfair: \ a strong new model against a weak old one", AUTH),
            (r"a new method's gain is only as large as the best version of the old one allows", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the two have in common. <bookmark mark='a'/> Both are claims about efficiency: fewer items, better "
            "predictions. <bookmark mark='b'/> The first held, because the model behind it had been tested first. "
            "<bookmark mark='c'/> The second shrank, because the comparison was unfair: a strong new model against a "
            "weak old one. <bookmark mark='d'/> A new method's gain is only as large as the best version of the old "
            "one allows."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
