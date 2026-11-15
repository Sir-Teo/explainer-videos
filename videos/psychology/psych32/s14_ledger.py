from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_positive_manifold()
        self.row_gma_job_validity()
        self.row_flynn_effect()
        self.row_schooling_iq()
        self.row_heritability_age()
        self.row_ses_heritability()
        self.row_mozart_effect()
        self.row_multiple_intelligences()
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
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
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6),
                  run_time=1.5)
        vo.wait_until("c")
        self.play(FadeIn(card.note))
        vo.wait_until("d")
        self.play(FadeIn(card.status, scale=1.3))

    def row_positive_manifold(self):
        card = ledger_card(self._get("positive_manifold"), width=12.8, font_size=21)
        with self.voiceover(
            "Eight new rows today. The first: scores on different kinds of mental test correlate positively with one "
            "another. <bookmark mark='a'/> The original: Spearman's schoolboys, in 1904. <bookmark mark='b'/> The "
            "record: Holzinger and Swineford's children, recomputed in this part; John Carroll's reanalysis of more "
            "than four hundred and sixty data sets in 1993; and even the tests of Gardner's eight intelligences. "
            "<bookmark mark='c'/> It's among the most replicated findings in psychology. What causes it, one "
            "ability or many interacting ones, is a separate and open question. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_gma_job_validity(self):
        card = ledger_card(self._get("gma_job_validity"), width=12.8, font_size=21)
        with self.voiceover(
            "The second: general mental ability predicts job performance with a validity of about point five, "
            "better than any other single selection method. <bookmark mark='a'/> The original: Schmidt and Hunter's "
            "review of eighty-five years of studies, in 1998. <bookmark mark='b'/> The record: in 2022 Sackett and "
            "colleagues revisited the corrections for range restriction, and found about point three one. "
            "<bookmark mark='c'/> A real and useful predictor; the classic figure rested on corrections that were "
            "too large, chapter seven's statistics applied to a whole literature. <bookmark mark='d'/> Replicated, "
            "smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_flynn_effect(self):
        card = ledger_card(self._get("flynn_effect"), width=12.8, font_size=20)
        with self.voiceover(
            "The third: average scores on intelligence tests rose by about three points a decade through the "
            "twentieth century. <bookmark mark='a'/> The original: Flynn's American norming samples, in 1984. "
            "<bookmark mark='b'/> The record: fourteen nations in 1987; Wicherts's test of measurement invariance; "
            "a meta-analysis of about four million people; and a reversal within Norwegian families. "
            "<bookmark mark='c'/> The rise is real and large. What it's a rise in is unclear, since the tests "
            "aren't invariant across cohorts, and in several countries it has reversed. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_schooling_iq(self):
        card = ledger_card(self._get("schooling_iq"), width=12.8, font_size=22)
        with self.voiceover(
            "The fourth: an extra year of schooling raises scores on intelligence tests. <bookmark mark='a'/> The "
            "original: Stephen Ceci's review, in 1991. <bookmark mark='b'/> The record: Ritchie and Tucker-Drob's "
            "meta-analysis of more than six hundred thousand people, about one to five points a year. "
            "<bookmark mark='c'/> The effect holds across three quasi-experimental designs; whether schooling "
            "raises g, or the skills the tests sample, is open. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_heritability_age(self):
        card = ledger_card(self._get("heritability_age"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: the heritability of general cognitive ability rises from childhood to young adulthood. "
            "<bookmark mark='a'/> The original: Haworth and colleagues' eleven thousand twin pairs, in 2010. "
            "<bookmark mark='b'/> The record: Briley and Tucker-Drob's 2013 meta-analysis of longitudinal studies, "
            "with heritability rising after about age eight, mostly as earlier genetic influences grow stronger. "
            "<bookmark mark='c'/> A robust developmental pattern. One reading is that children increasingly select "
            "environments that suit them. <bookmark mark='d'/> Replicated. This row was promised in Part 9."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_ses_heritability(self):
        card = ledger_card(self._get("ses_heritability"), width=12.8, font_size=21)
        with self.voiceover(
            "The sixth, also promised in Part 9: among children raised in poverty, the heritability of IQ is close "
            "to zero. <bookmark mark='a'/> The original: Turkheimer and colleagues' three hundred and nineteen twin "
            "pairs aged seven, in 2003. <bookmark mark='b'/> The record: in 2016 Tucker-Drob and Bates pooled "
            "nearly twenty-five thousand twin and sibling pairs from six countries, and found the interaction in "
            "American samples, and none in Western Europe or Australia. <bookmark mark='c'/> A heritability that "
            "depends on the environment, as Part 9 argued it can; whether it does depends on the country. "
            "<bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_mozart_effect(self):
        card = ledger_card(self._get("mozart_effect"), width=12.8, font_size=21)
        with self.voiceover(
            "The seventh: listening to Mozart improves spatial reasoning. <bookmark mark='a'/> The original: "
            "Rauscher, Shaw and Ky, in Nature, in 1993. <bookmark mark='b'/> The record: a 2010 meta-analysis of "
            "about forty studies, with a small effect against no stimulus that varied by laboratory, and nothing "
            "specific to Mozart. <bookmark mark='c'/> If anything, music in general lifts arousal or mood for a "
            "while; and the authors never claimed a rise in general intelligence. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_multiple_intelligences(self):
        card = ledger_card(self._get("multiple_intelligences"), width=12.8, font_size=22)
        with self.voiceover(
            "The eighth: human abilities form several independent intelligences, rather than one general factor. "
            "<bookmark mark='a'/> The original: Howard Gardner's Frames of Mind, in 1983. <bookmark mark='b'/> The "
            "record: Visser, Ashton and Vernon's tests of the eight domains, with a positive manifold and a large "
            "general factor. <bookmark mark='c'/> A useful list of talents; the claim of independence is contradicted "
            "by the domains' own correlations. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 32 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 4, "replicated, smaller": 1, "contested": 1, "failed": 2}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=19, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.6, 20, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, -0.2, 0])
        rows_ = rows_of([
            (r"what holds: \ the positive manifold, \ the rise of scores across generations, \ the effect of "
             r"school, \ and heritability rising with age", GOOD),
            (r"what shrinks: \ the validity of tests for jobs, \ once the corrections are corrected", G),
            (r"what fails: \ a sonata that makes you cleverer, \ and intelligences that do not correlate; \ "
             r"what is argued: \ whether poverty lowers heritability outside the United States", LOST),
            (r"the strongest rows are correlations seen in every battery, \ and natural experiments with very large "
             r"samples", YOU),
        ], 5.6, 22, 0.36).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: the positive manifold, the rise of scores across "
            "generations, the effect of school, and heritability rising with age. <bookmark mark='b'/> What shrinks: the validity of tests for "
            "jobs, once the corrections are themselves corrected. <bookmark mark='c'/> What fails: a sonata that "
            "makes you cleverer, and intelligences that don't correlate. What's argued is whether poverty lowers "
            "heritability outside the United States. <bookmark mark='d'/> And the strongest "
            "rows are correlations seen in every battery ever given, and natural experiments with very large "
            "samples."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
