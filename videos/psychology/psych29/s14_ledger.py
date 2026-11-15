from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_two_factor()
        self.row_bridge()
        self.row_faces()
        self.row_feedback()
        self.row_money()
        self.row_ratio()
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

    def row_two_factor(self):
        card = ledger_card(self._get("schachter_singer"), width=12.8, font_size=22)
        with self.voiceover(
            "Six new rows today. The first: unexplained arousal is felt as whatever emotion the situation suggests. "
            "<bookmark mark='a'/> The original: Schachter and Singer's adrenaline study, 1962. "
            "<bookmark mark='b'/> The record: Marshall and Zimbardo's repeat of the euphoria conditions in 1979, "
            "Maslach's unexplained arousal felt as unpleasant the same year, and Reisenzein's review in 1983. "
            "<bookmark mark='c'/> Arousal can be misattributed; the strong claim, that emotion is arousal plus a "
            "label, did not survive. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_bridge(self):
        card = ledger_card(self._get("bridge_misattribution"), width=12.8, font_size=23)
        with self.voiceover(
            "The second: men who met a woman on a frightening bridge were more attracted to her. "
            "<bookmark mark='a'/> The original: Dutton and Aron, 1974. <bookmark mark='b'/> The record: Foster and "
            "colleagues' meta-analysis of laboratory experiments on arousal and attraction, in 1998. "
            "<bookmark mark='c'/> Arousal does raise attraction in the laboratory, though perhaps not by "
            "misattribution; the bridge itself has never been repeated at scale. <bookmark mark='d'/> Not directly "
            "tested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_faces(self):
        card = ledger_card(self._get("universal_expressions"), width=12.8, font_size=21)
        with self.voiceover(
            "The third: people in every culture recognize the same six emotions from the same faces. "
            "<bookmark mark='a'/> The original: Ekman and Friesen in New Guinea, 1971. <bookmark mark='b'/> The "
            "record: Russell's review of the method in 1994, Gendron and colleagues' free sorting with the Himba in "
            "2014, and Barrett and colleagues' review in 2019. <bookmark mark='c'/> With a forced choice among a few "
            "labels, the classic pattern replicates widely. With free responses, and in small-scale societies, it "
            "weakens, and what faces signal is argued. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_feedback(self):
        card = ledger_card(self._get("facial_feedback"), width=12.8, font_size=21)
        with self.voiceover(
            "The fourth: moving the face into an expression changes the emotion felt. <bookmark mark='a'/> The "
            "original: Strack, Martin and Stepper's pens, 1988. <bookmark mark='b'/> The record: seventeen "
            "laboratories finding nearly nothing in 2016, Noah and colleagues' camera in 2018, the meta-analysis of "
            "two hundred and eighty-six effects in 2019, and the Many Smiles Collaboration in 2022. "
            "<bookmark mark='c'/> Deliberate expressions change feelings a little; the unobtrusive pen is "
            "unreliable. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_money(self):
        card = ledger_card(self._get("money_wellbeing"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: emotional well-being rises with income, but stops rising above a moderate income. "
            "<bookmark mark='a'/> The original: Kahneman and Deaton, 2010. <bookmark mark='b'/> The record: "
            "Killingsworth's smartphone samples in 2021, and the adversarial collaboration in 2023. "
            "<bookmark mark='c'/> Well-being rises with log income for most people; the plateau described the "
            "unhappiest, and the authors themselves reconciled the two findings. <bookmark mark='d'/> Replicated, "
            "with its scope now known."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_ratio(self):
        card = ledger_card(self._get("positivity_ratio"), width=12.8, font_size=22)
        with self.voiceover(
            "And the sixth: people flourish when their ratio of positive to negative emotions exceeds 2.9013. "
            "<bookmark mark='a'/> The original: Fredrickson and Losada, 2005. <bookmark mark='b'/> The record: "
            "Brown, Sokal and Friedman's analysis of the mathematics, and the journal's withdrawal of the "
            "modelling, both in 2013. <bookmark mark='c'/> The number went; the broader idea that positive emotion "
            "goes with better mental health stayed. <bookmark mark='d'/> Retracted."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 29 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"contested": 2, "not directly tested": 1, "replicated, smaller": 1, "replicated": 1,
                          "retracted": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=20, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.6, 22, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-3.2, 0.2, 0])
        rows_ = rows_of([
            (r"what holds: \ the body's state shapes feeling, \ and expressions and arousal change it a little", GOOD),
            (r"what fell: \ the strong versions: \ emotion as arousal plus a label, \ six fixed faces, \ a pen "
             r"that makes cartoons funnier, \ a magic ratio", LOST),
            (r"the survivor of the hardest fight, \ money and happiness, \ was saved by its rivals working "
             r"together", COG),
        ], 5.6, 23, 0.36).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: the body's state shapes what we feel, and expressions and "
            "arousal change it, a little. <bookmark mark='b'/> What fell were the strong versions: emotion as "
            "arousal plus a label, six fixed faces read the same everywhere, a pen that makes cartoons funnier, and "
            "a magic ratio. <bookmark mark='c'/> And the finding with the hardest fight, money and happiness, was "
            "settled by its rivals working together."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
