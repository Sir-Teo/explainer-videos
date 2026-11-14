from __future__ import annotations

from videos.psychology.psych9.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.twins()
        self.candidates()
        self.score()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter twelve. The Ledger."
        ):
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

    def twins(self):
        card = ledger_card(self._row("twin_heritability"), width=12.8, font_size=27)
        with self.voiceover(
            "Three rows today. The first. The claim: on almost every psychological trait, identical twins "
            "are more alike than fraternal twins. <bookmark mark='a'/> An early summary: Bouchard and "
            "McGue's review of 111 studies, in 1981. <bookmark mark='b'/> The record: fifty years of twin "
            "studies, pooled in 2015. Nearly eighteen thousand traits, an average heritability of "
            "forty-nine percent, and almost no trait at zero. <bookmark mark='c'/> What repeats is the "
            "pattern of correlations. Reading it as a share for genes rests on the design's assumptions, "
            "and the share describes a population, not a person. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def candidates(self):
        card = ledger_card(self._row("candidate_genes"), width=12.8, font_size=26)
        with self.voiceover(
            "The second. The claim: common variants in a few named genes explain who becomes depressed "
            "after stress, or who scores higher on tests. <bookmark mark='a'/> The original: Caspi and "
            "colleagues, 2003, on the serotonin transporter. <bookmark mark='b'/> The record. A pooled "
            "analysis in 2009: nothing. Twelve variants for intelligence, retested in 2012: one "
            "significant test in thirty-two. Eighteen candidate genes for depression, tested in 2019 in "
            "up to four hundred and forty thousand people: none. <bookmark mark='c'/> Small samples, "
            "flexible analyses and journals that prefer a positive result. It's Part 4's mechanism, in a "
            "different field. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def score(self):
        card = ledger_card(self._row("education_polygenic_score"), width=12.8, font_size=26)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "And the third. The claim: a score added up from many common gene variants predicts how far a "
            "person goes in school. <bookmark mark='a'/> The original: Rietveld and colleagues, 2013. "
            "Three variants, and a score that predicted about two percent. <bookmark mark='b'/> The "
            "record: a million people in 2018, three million in 2022. Thousands of variants, and a score "
            "that predicts twelve to sixteen percent. <bookmark mark='c'/> It predicts groups far better "
            "than it predicts a person. Part of it is the parents' genes, acting through the home. And it "
            "predicts poorly in people whose ancestry differs from the samples it was built on. "
            f"<bookmark mark='d'/> Replicated. <bookmark mark='e'/> That makes {total} rows. Compare the "
            "second with the third. The same question, which genes, was asked twice. Once with small "
            "samples and a free hand, and once with enormous samples, a threshold fixed in advance, and a "
            "second sample to confirm. The first way produced a decade of results that weren't there."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
