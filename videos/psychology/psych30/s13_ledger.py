from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_a_not_b()
        self.row_infant_object_permanence()
        self.row_infant_arithmetic()
        self.row_ans_math()
        self.row_false_belief_explicit()
        self.row_false_belief_implicit()
        self.row_neonatal_imitation()
        self.row_ids_preference()
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

    def _show(self, card, vo):
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

    def row_a_not_b(self):
        card = ledger_card(self._get("a_not_b"), width=12.8, font_size=22)
        with self.voiceover(
            "Eight new rows today. The first: infants of about eight to twelve months, having found a toy at A, "
            "search at A after seeing it hidden at B. <bookmark mark='a'/> The original: Piaget's observations of "
            "his own children, published in 1937. <bookmark mark='b'/> The record: Diamond's delays in 1985, "
            "Wellman, Cross and Bartsch's meta-analysis in 1987, and Smith and Thelen's manipulations of the task "
            "and posture in 1999. <bookmark mark='c'/> One of the most reliable findings in infancy; what it shows "
            "is argued. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_infant_object_permanence(self):
        card = ledger_card(self._get("infant_object_permanence"), width=12.8, font_size=22)
        with self.voiceover(
            "The second: infants of three to five months know that a hidden object still exists. <bookmark "
            "mark='a'/> The original: the drawbridge, 1985. <bookmark mark='b'/> The record: Baillargeon's younger "
            "infants in 1987, and Bogartz, Shinskey and Schilling's familiarization study in 2000. <bookmark "
            "mark='c'/> The looking pattern replicates in its laboratory; reading it as knowledge of hidden objects "
            "is argued. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_infant_arithmetic(self):
        card = ledger_card(self._get("infant_arithmetic"), width=12.8, font_size=22)
        with self.voiceover(
            "The third: five-month-olds expect one plus one to make two. <bookmark mark='a'/> The original: Wynn, "
            "1992. <bookmark mark='b'/> The record: a careful failure in 2000, and a meta-analysis of five hundred "
            "and fifty infants in 2017, with d of 0.34. <bookmark mark='c'/> Probably real and smaller; whether it's "
            "arithmetic is argued. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_ans_math(self):
        card = ledger_card(self._get("ans_math"), width=12.8, font_size=22)
        with self.voiceover(
            "The fourth: the acuity of the approximate number system predicts mathematics. <bookmark mark='a'/> The "
            "original: Halberda, Mazzocco and Feigenson, 2008. <bookmark mark='b'/> The record: two meta-analyses, "
            "in 2014 and 2017. <bookmark mark='c'/> A real correlation of about 0.2, partly shared with general "
            "ability. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_false_belief_explicit(self):
        card = ledger_card(self._get("false_belief_explicit"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: children begin to pass explicit false-belief tasks at about four. <bookmark mark='a'/> The "
            "original: Wimmer and Perner, 1983. <bookmark mark='b'/> The record: the Sally-Anne task in 1985, and "
            "the meta-analysis of a hundred and seventy-eight studies in 2001. <bookmark mark='c'/> One of the "
            "field's most robust findings. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_false_belief_implicit(self):
        card = ledger_card(self._get("false_belief_implicit"), width=12.8, font_size=22)
        with self.voiceover(
            "The sixth: fifteen-month-olds expect people to act on false beliefs. <bookmark mark='a'/> The original: "
            "Onishi and Baillargeon, 2005. <bookmark mark='b'/> The record: two sets of replications in 2018 that "
            "mostly failed. <bookmark mark='c'/> Multi-laboratory tests are under way. <bookmark mark='d'/> "
            "Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_neonatal_imitation(self):
        card = ledger_card(self._get("neonatal_imitation"), width=12.8, font_size=22)
        with self.voiceover(
            "The seventh: newborns imitate facial gestures. <bookmark mark='a'/> The original: Meltzoff and Moore, "
            "1977. <bookmark mark='b'/> The record: a hundred and six infants followed in 2016, and Meltzoff's "
            "reanalysis. <bookmark mark='c'/> The largest study found no imitation; one gesture is still disputed. "
            "<bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_ids_preference(self):
        card = ledger_card(self._get("ids_preference"), width=12.8, font_size=22)
        with self.voiceover(
            "And the eighth: infants prefer infant-directed speech. <bookmark mark='a'/> The original: Anne Fernald, "
            "1985. <bookmark mark='b'/> The record: ManyBabies, in sixty-five laboratories, recomputed here. "
            "<bookmark mark='c'/> Real, smaller than earlier estimates, and dependent on method, age and language. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 30 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "contested": 4, "replicated, smaller": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=19, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.6, 21, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-3.2, 0.0, 0])
        rows_ = rows_of([
            (r"what holds: \ behaviour that anyone can see, \ such as reaching to A, \ answering about Maxi, \ "
             r"turning to infant-directed speech", GOOD),
            (r"what is contested: \ rich readings of a few seconds of looking: \ objects, \ arithmetic, \ false "
             r"belief, \ imitation at birth", LOST),
            (r"the instrument is sound when used at scale and preregistered; \ the inference from a look to a "
             r"concept is where findings fail", LOOK),
        ], 5.6, 22, 0.36).move_to([3.6, 0.0, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds is behaviour anyone can see: reaching to A, answering about "
            "Maxi, turning toward infant-directed speech. <bookmark mark='b'/> What's contested is the rich reading "
            "of a few seconds of looking: knowledge of objects, arithmetic, false belief, imitation at birth. "
            "<bookmark mark='c'/> The instrument itself is sound when it's used at scale and preregistered. It's "
            "the inference from a look to a concept where findings fail."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
