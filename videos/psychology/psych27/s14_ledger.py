from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_blindsight()
        self.row_priming()
        self.row_libet()
        self.row_covert()
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until("a")
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until("b")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until("c")
        self.play(FadeIn(card.note))
        vo.wait_until("d")
        self.play(FadeIn(card.status, scale=1.3))

    def row_blindsight(self):
        card = ledger_card(self._get("blindsight"), width=12.8, font_size=22)
        with self.voiceover(
            "Four new rows today; the gorilla already has its row, from Part 18. The first: after damage to the "
            "primary visual cortex, people can locate and discriminate what they say they don't see. "
            "<bookmark mark='a'/> The original: Weiskrantz and colleagues with D.B., 1974. <bookmark mark='b'/> The "
            "record: the scattered-light critique of 1983, Cowey and Stoerig's monkeys, G.Y.'s wagers, the graded "
            "awareness scale in 2008, and Schmid and colleagues' silenced geniculate in 2010. <bookmark mark='c'/> "
            "The effect replicates in patients and monkeys. Whether it's degraded conscious vision is contested. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_priming(self):
        card = ledger_card(self._get("masked_semantic_priming"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: a masked word or number that can't be reported still speeds responses to a related one. "
            "<bookmark mark='a'/> The original: Dehaene and colleagues, 1998. <bookmark mark='b'/> The record: a "
            "meta-analysis by Eva Van den Bussche and colleagues in 2009, and a 2016 review by Miguel Vadillo, "
            "Emmanouil Konstantinidis and David Shanks showing that the tests of awareness were often too weak to "
            "prove the primes unseen. <bookmark mark='c'/> The priming is real, and smaller, and less certainly "
            "unconscious, than first claimed. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_libet(self):
        card = ledger_card(self._get("libet_timing"), width=12.8, font_size=23)
        with self.voiceover(
            "The third: the readiness potential begins several hundred milliseconds before people report the urge "
            "to move. <bookmark mark='a'/> The original: Libet and colleagues, 1983. <bookmark mark='b'/> The "
            "record: Patrick Haggard and Martin Eimer in 1999, Soon and colleagues' decoding in 2008, Trevena and "
            "Miller's ramp before not moving in 2010, and Schurger's accumulator in 2012. <bookmark mark='c'/> The "
            "timing replicates. That it reveals an unconscious decision is contested, and the accumulator explains "
            "the ramp without one. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_covert(self):
        card = ledger_card(self._get("covert_awareness"), width=12.8, font_size=24)
        with self.voiceover(
            "And the fourth: some patients who show no sign of awareness at the bedside follow commands with their "
            "brain activity. <bookmark mark='a'/> The original: Owen and colleagues, 2006. <bookmark mark='b'/> The "
            "record: Monti and colleagues' fifty-four patients in 2010, and Bodien and colleagues' three hundred and "
            "fifty-three in 2024. <bookmark mark='c'/> Found again in larger, multicentre samples, though how often "
            "depends on the method. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 27 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "replicated, smaller": 1}
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=20, width=2.8)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 22, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-3.3, 0.2, 0])
        rows_ = rows_of([
            (r"the phenomena replicate: \ blindsight, \ the readiness potential, \ hidden awareness", GOOD),
            (r"what they mean does not: \ degraded vision or none, \ a decision or a fluctuation", LOST),
            (r"unconscious processing is real but smaller than claimed, \ and proving a stimulus unseen is hard", HOT),
        ], 5.6, 23, 0.36).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> The phenomena replicate: blindsight, the readiness potential's timing, "
            "and awareness hidden in unresponsive patients. <bookmark mark='b'/> What they mean is another matter: "
            "degraded vision or none, a decision or a fluctuation. <bookmark mark='c'/> And unconscious processing "
            "is real but smaller than first claimed, because proving that a stimulus was unseen is so hard."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
