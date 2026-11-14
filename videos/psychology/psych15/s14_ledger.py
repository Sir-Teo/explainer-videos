from __future__ import annotations

from videos.psychology.psych15.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.mcgurk()
        self.categories()
        self.homunculus()
        self.rubber()
        self.tongue()
        self.odours()

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

    def mcgurk(self):
        card = ledger_card(self._row("mcgurk"), width=12.8, font_size=25)
        with self.voiceover(
            "Six rows today. The first: a voice saying one syllable, dubbed onto lips saying another, is often heard "
            "as a third. <bookmark mark='a'/> The original: McGurk and MacDonald, 1976. <bookmark mark='b'/> The record: "
            "it has been reproduced in laboratory after laboratory, and Mallick and colleagues in 2015 measured how "
            "much it varies, from never to always, depending on the person. <bookmark mark='c'/> The note: the "
            "illusion is easily reproduced, but at rates often far below the original ninety-eight percent, and it "
            "depends on the recording and the language. <bookmark mark='d'/> For the claim as stated, often: "
            "replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def categories(self):
        card = ledger_card(self._row("categorical_speech"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: along a continuum of speech sounds, people discriminate much better across a phoneme "
            "boundary than within a category. <bookmark mark='a'/> The original: Liberman, Harris, Hoffman and "
            "Griffith, 1957. <bookmark mark='b'/> The record: McMurray, Tanenhaus and Aslin, 2002, and many since, "
            "showing graded sensitivity inside categories. <bookmark mark='c'/> The peak at the boundary is robust; "
            "the story that listeners can't hear differences within a category is not. <bookmark mark='d'/> Story and "
            "record: the finding stands, the textbook account doesn't."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def homunculus(self):
        card = ledger_card(self._row("homunculus"), width=12.8, font_size=25)
        with self.voiceover(
            "The third is a row Part 7 promised: the body is mapped in order along the cortex, with the hands, lips and "
            "tongue given far more of it than the trunk. <bookmark mark='a'/> The original: Penfield and Boldrey, "
            "1937, stimulating the cortex of a hundred and twenty-six awake patients during surgery. "
            "<bookmark mark='b'/> The record: in 2018 Roux and colleagues repeated the stimulation in fifty patients "
            "and confirmed the order, though not every detail, and in 2023 precision imaging confirmed the motor map's "
            "regions, with others for whole-body action between them. <bookmark mark='c'/> The map has held for ninety "
            "years; the famous drawing is a summary, and its details keep being revised. <bookmark mark='d'/> "
            "Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def rubber(self):
        card = ledger_card(self._row("rubber_hand"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: stroke a visible rubber hand and a hidden real one together, and people feel the touch on "
            "the rubber hand and call it their own. <bookmark mark='a'/> The original: Botvinick and Cohen, 1998. "
            "<bookmark mark='b'/> The record: in 2020, Lush and colleagues found the reports track a person's "
            "responsiveness to suggestion. <bookmark mark='c'/> Synchronous stroking reliably beats asynchronous; "
            "whether the reports reflect changed bodily experience, or partly what people expect, is disputed. "
            "<bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tongue(self):
        card = ledger_card(self._row("tongue_map"), width=12.8, font_size=25)
        with self.voiceover(
            "The fifth: different parts of the tongue are sensitive to different tastes. <bookmark mark='a'/> The "
            "original: Hänig, 1901, who found small differences. <bookmark mark='b'/> The record: Collings, 1974: "
            "the differences are real but small, and every region with taste buds detects every taste. "
            "<bookmark mark='c'/> The map came from a replotting and a retelling, not from any data. "
            "<bookmark mark='d'/> Story and record."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def odours(self):
        card = ledger_card(self._row("trillion_odours"), width=12.8, font_size=25)
        with self.voiceover(
            "The sixth: people can discriminate more than a trillion smells. <bookmark mark='a'/> The original: "
            "Bushdid, Magnasco, Vosshall and Keller, 2014, with twenty-six people. <bookmark mark='b'/> The record: two "
            "reanalyses in 2015 argued the estimate could have come out almost anywhere, and that the data fit ten "
            "discriminable smells as well as a trillion. <bookmark mark='c'/> The experiments aren't in question; the "
            "number is, and nobody yet knows the true count. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
