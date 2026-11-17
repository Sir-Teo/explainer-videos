from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403

ROWS = [
    ("lm_classic_biases",
     "Five new rows. The first: language models show people's biases on the classic judgment problems. "
     "<bookmark mark='a'/> The original: Binz and Schulz, 2023. <bookmark mark='b'/> The record: the biases faded in "
     "later models. <bookmark mark='c'/> It depends on the model and the wording, and the items are in the training "
     "text. <bookmark mark='d'/> Contested."),
    ("lm_theory_of_mind",
     "The second: language models have a robust theory of mind. <bookmark mark='a'/> The original: Kosinski, 2023. "
     "<bookmark mark='b'/> The record: failures on trivial alterations, and a comparison with nineteen hundred "
     "people. <bookmark mark='c'/> Strong on familiar forms, disputed beyond them. <bookmark mark='d'/> Contested."),
    ("algorithm_aversion",
     "The third: after seeing an algorithm err, people avoid it, even when it's better. <bookmark mark='a'/> The "
     "original: Dietvorst, Simmons and Massey, 2015. <bookmark mark='b'/> The record: algorithm appreciation, and "
     "control that restores use. <bookmark mark='c'/> Both replicate; the task decides. <bookmark mark='d'/> "
     "Contested."),
    ("dialogue_belief_change",
     "The fourth: a short conversation with a model durably reduces belief in a conspiracy theory. "
     "<bookmark mark='a'/> The original: Costello, Pennycook and Rand, 2024. <bookmark mark='b'/> The record: so far, "
     "the paper's own two studies. <bookmark mark='c'/> Promising, and waiting for independent replication. "
     "<bookmark mark='d'/> Not directly tested."),
    ("social_media_harm",
     "And the fifth: smartphones and social media caused a large rise in adolescents' depressive symptoms. "
     "<bookmark mark='a'/> The original: Twenge and colleagues, 2018. <bookmark mark='b'/> The record: tiny "
     "associations across specifications, and a small benefit from deactivation in adults. <bookmark mark='c'/> The "
     "rise is real; the cause and its size are disputed. <bookmark mark='d'/> Contested."),
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
        assert len(rows) == 5
        head = heading(r"What the five have in common")
        items = rows_of([
            (r"four of five are contested: \ a young field, \ and subjects that change every year", AUTH),
            (r"the disputes are about method: \ contamination, \ perturbation, \ controls, \ causal "
             r"designs", MODEL),
            (r"every one is settled the same way: \ new items, \ many models, \ randomized experiments, \ "
             r"replication", GOOD),
            (r"psychology and AI can each tell the other a great deal, \ if both use psychology's methods", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the five have in common. <bookmark mark='a'/> Four of five are contested. It's a young field, and its "
            "subjects change every year. <bookmark mark='b'/> The disputes are about method: contamination, "
            "perturbation, controls and causal designs. <bookmark mark='c'/> And every one is settled the same way: "
            "new items, many models, randomized experiments and replication. <bookmark mark='d'/> So here's the "
            "answer to this part's question. Psychology and AI can each tell the other a great deal, if both use "
            "psychology's methods."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
