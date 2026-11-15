from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_word_superiority()
        self.row_statistical_segmentation()
        self.row_surprisal_reading()
        self.row_critical_period()
        self.row_color_relativity()
        self.row_bilingual_advantage()
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
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

    def row_word_superiority(self):
        card = ledger_card(self._row("word_superiority"), width=12.8, font_size=24)
        with self.voiceover(
            "Six rows today. The first: a letter is reported more accurately inside a briefly shown word than alone. "
            "<bookmark mark='a'/> The original: Reicher, 1969. <bookmark mark='b'/> The record: Wheeler's "
            "replication the next year, and many studies since, including with pronounceable non-words. "
            "<bookmark mark='c'/> A robust effect, and the founding data of interactive models. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_statistical_segmentation(self):
        card = ledger_card(self._row("statistical_segmentation"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: infants can find word boundaries from the transitional probabilities between syllables. "
            "<bookmark mark='a'/> The original: Saffran, Aslin and Newport, 1996. <bookmark mark='b'/> The record: "
            "Black and Bergmann's meta-analysis of the infant studies in 2017. <bookmark mark='c'/> Small and reliable "
            "in close replications, not reliable across all the designs that use transitional probabilities. "
            "<bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_surprisal_reading(self):
        card = ledger_card(self._row("surprisal_reading"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: reading time grows with a word's surprisal. <bookmark mark='a'/> The original: Smith and "
            "Levy, 2013, with eye-tracking and self-paced reading. <bookmark mark='b'/> The record: many corpora and "
            "language models since, and this part's fit to the Natural Stories corpus, with the cost landing on the "
            "next word. <bookmark mark='c'/> One of the steadiest relations in psycholinguistics, though which "
            "language model fits best is a live question. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_critical_period(self):
        card = ledger_card(self._row("critical_period"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: there is a sharp age after which a second language's grammar cannot be fully learned. "
            "<bookmark mark='a'/> The original: Johnson and Newport, 1989. <bookmark mark='b'/> The record: studies "
            "finding a gradual decline rather than a cut-off, and Hartshorne and colleagues' two-thirds of a million "
            "people, finding a decline after about seventeen. <bookmark mark='c'/> That ability declines with the age "
            "of starting is well supported; whether there is a sharp period, and why, is not settled. "
            "<bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_color_relativity(self):
        card = ledger_card(self._row("color_relativity"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: a language's colour words speed the discrimination of colours across their boundaries. "
            "<bookmark mark='a'/> The original: Winawer and colleagues' Russian blues, 2007. "
            "<bookmark mark='b'/> The record: several studies that did not find such category effects, and a 2020 "
            "study of Russian speakers with mixed results. <bookmark mark='c'/> Effects appear under some conditions "
            "and stimuli and not others. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_bilingual_advantage(self):
        card = ledger_card(self._row("bilingual_advantage"), width=12.8, font_size=24)
        with self.voiceover(
            "And the sixth: speaking two languages improves executive control. <bookmark mark='a'/> The original: "
            "Bialystok and colleagues, 2004. <bookmark mark='b'/> The record: Paap and Greenberg's failures to find "
            "it in 2013, and Lehtonen and colleagues' meta-analysis of a hundred and fifty-two studies in 2018. "
            "<bookmark mark='c'/> A very small advantage before correcting for publication bias, and none after. "
            "<bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 23 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        lines = VGroup(*[label(rf"{st}: \ {n}", font_size=30, color=GREY_A) for st, n in counts.items()]).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.2, 0.5, 0])
        rows_ = rows_of([
            (r"the measurements held: \ word superiority, \ the surprisal relation", MODEL),
            (r"the claims about language shaping minds, \ in colour and in control, \ did not hold up as first "
             r"reported", LOST),
            (r"the pattern of Part 4 again: \ small samples, \ flexible measures, \ appealing stories", STAT),
        ], 6.2, 22, 0.32).move_to([3.3, 0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> The measurements held: word superiority, and the relation between "
            "surprisal and reading time. <bookmark mark='b'/> The claims that a language shapes the mind's other "
            "abilities, in colour and in executive control, did not hold up as first reported. "
            "<bookmark mark='c'/> It's the pattern of Part 4 again: small samples, flexible measures, and stories "
            "people want to be true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
