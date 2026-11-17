from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403

ROWS = [
    ("glucose_self_control",
     "Three new rows. The first is a mediator: self-control draws on blood glucose, so depletion lowers it, and a "
     "sugary drink restores self-control. <bookmark mark='a'/> The original: Gailliot and colleagues, 2007. "
     "<bookmark mark='b'/> The record: a preregistered test of a glucose drink, and a meta-analysis of the glucose "
     "literature. <bookmark mark='c'/> A mediator chosen from a correlation failed when it was manipulated, and the "
     "parent effect, ego depletion, failed too. <bookmark mark='d'/> Failed."),
    ("factor_network_equivalence",
     "The second is a theorem. A latent-factor model and a network of direct interactions can imply exactly the same "
     "distribution of responses. <bookmark mark='a'/> The original: Kruis and Maris, 2016. <bookmark mark='b'/> The "
     "record: the network and item-response models related formally, by Marsman and colleagues. "
     "<bookmark mark='c'/> A theorem, not an experiment. Fit can't decide between a hidden cause and a system of "
     "mutual causes; interventions and time can. <bookmark mark='d'/> Replicated, as mathematics."),
    ("fit_cutoffs",
     "The third: fixed cut-offs for fit indices separate good models from bad ones in general. "
     "<bookmark mark='a'/> The original: Hu and Bentler, 1999. <bookmark mark='b'/> The record: a critique with "
     "simulations, and dynamic cut-offs computed for each model. <bookmark mark='c'/> Useful in the conditions they "
     "came from; as general rules, misleading. <bookmark mark='d'/> Failed."),
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
        assert len(rows) == 3
        head = heading(r"What the three have in common")
        items = rows_of([
            (r"each is a claim about a model, \ not about a single study's data", WHITE),
            (r"the mediator failed when it was moved by hand; \ the cut-offs failed outside their simulations; \ "
             r"the theorem holds because it is a theorem", MODEL),
            (r"a model is a claim too: \ it goes in the Ledger, \ and it can fail", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the three have in common. <bookmark mark='a'/> Each is a claim about a model, not about a single "
            "study's data. <bookmark mark='b'/> The mediator failed when it was moved by hand. The cut-offs failed "
            "outside the simulations they came from. The theorem holds because it is a theorem. "
            "<bookmark mark='c'/> A model is a claim too. It goes in the Ledger, and it can fail."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
