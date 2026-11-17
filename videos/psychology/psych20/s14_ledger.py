from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.position()
        self.contiguity()
        self.levels()
        self.generation()
        self.specificity()
        self.divers()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _row(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo, marks="abcd"):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until(marks[0])
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until(marks[1])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def position(self):
        card = ledger_card(self._row("serial_position"), width=12.8, font_size=24)
        with self.voiceover(
            "Six rows today. The first: in free recall the first and the last few items of a list are recalled "
            "best, and recall usually starts at the end. <bookmark mark='a'/> The original: Murdock, 1962. "
            "<bookmark mark='b'/> The record: Glanzer and Cunitz's dissociation, Bjork and Whitten's long-term "
            "recency, and the PEERS data we measured today, where Healey and Kahana found the curve in almost every "
            "person. <bookmark mark='c'/> The shape is not in question. Its explanation moved from two stores to a "
            "drifting context. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def contiguity(self):
        card = ledger_card(self._row("contiguity"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: after recalling one item, people tend to recall next an item studied near it, more often "
            "forward than backward. <bookmark mark='a'/> The original: Kahana, 1996. <bookmark mark='b'/> The "
            "record: Howard and Kahana, under continual distraction; Healey and Kahana, person by person; and a "
            "2019 review by Healey, Nicole Long and Kahana that finds it across tasks, materials and time scales. "
            "<bookmark mark='c'/> It is weaker in some people and some designs, and strong almost everywhere. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def levels(self):
        card = ledger_card(self._row("levels_of_processing"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: words processed for meaning are remembered better than words processed for sound or "
            "appearance. <bookmark mark='a'/> The original: Craik and Tulving, 1975. <bookmark mark='b'/> The record: "
            "the effect has been found in countless studies, and Morris, Bransford and Franks showed its limit: a "
            "test that asks about sound reverses it. <bookmark mark='c'/> The effect is solid. Depth as a theory "
            "was criticised for having no measure of depth except the memory it was meant to explain. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def generation(self):
        card = ledger_card(self._row("generation_effect"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: words people generate are remembered better than words they read. "
            "<bookmark mark='a'/> The original: Slamecka and Graf, 1978. <bookmark mark='b'/> The record: Bertsch "
            "and colleagues' meta-analysis of eighty-six studies, and a larger one by Matthew McCurdy and colleagues "
            "in 2020. <bookmark mark='c'/> About half a standard deviation on average, and smallest in free recall, where it "
            "depends most on the design. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def specificity(self):
        card = ledger_card(self._row("encoding_specificity"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: a cue helps retrieval when it was part of what was encoded, and words can be recalled to a "
            "weak cue that were not recognised when seen. <bookmark mark='a'/> The original: Tulving and Thomson, "
            "1973. <bookmark mark='b'/> The record: Tulving and Wiseman's analysis of the many studies of "
            "recognition failure, which follow a lawful relation between recognition and recall. "
            "<bookmark mark='c'/> The phenomenon is robust; how general the principle is, and whether it can be "
            "tested without circularity, has been argued since. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def divers(self):
        card = ledger_card(self._row("underwater_context"), width=12.8, font_size=24)
        with self.voiceover(
            "And the sixth: divers recall words better in the environment where they learned them, on land or under "
            "water. <bookmark mark='a'/> The original: Godden and Baddeley, 1975. <bookmark mark='b'/> The record: "
            "Smith and Vela's meta-analysis of environmental context effects, and Murre's direct replication in "
            "2021. <bookmark mark='c'/> Context effects in general are real and small. The large underwater effect "
            "was not found again, in a replication that differed in important ways: a shallow, warm pool and a "
            "single session. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
