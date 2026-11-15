from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_big_five_structure()
        self.row_big_five_universal()
        self.row_trait_outcomes()
        self.row_person_situation()
        self.row_mbti_types()
        self.row_likes_prediction()
        self.row_psychographic_targeting()
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

    def row_big_five_structure(self):
        card = ledger_card(self._get("big_five_structure"), width=12.8, font_size=21)
        with self.voiceover(
            "Seven new rows today. The first: ratings and self-reports of personality are summarized by five broad "
            "recurring factors. <bookmark mark='a'/> The original: Tupes and Christal's Air Force report, in 1961. "
            "<bookmark mark='b'/> The record: Norman in 1963; McCrae and Costa's six translations in 1997; and the "
            "SAPA sample, recomputed in this part. <bookmark mark='c'/> Robust in literate samples, mostly Western "
            "and Asian, with a lexical sixth factor recurring too. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_big_five_universal(self):
        card = ledger_card(self._get("big_five_universal"), width=12.8, font_size=21)
        with self.voiceover(
            "The second: the same five factors describe personality in every human population. "
            "<bookmark mark='a'/> The original: McCrae and Costa, calling the structure a human universal, in 1997. "
            "<bookmark mark='b'/> The record: among the Tsimane of Bolivia, Gurven and colleagues found no robust "
            "five-factor structure, and Laajaj and colleagues found face-to-face surveys in twenty-three low- and "
            "middle-income countries of low validity, while internet samples from the same countries looked "
            "Western. <bookmark mark='c'/> Whether the five are universal, or partly a product of literacy, schooling "
            "and questionnaire habits, is unresolved. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_trait_outcomes(self):
        card = ledger_card(self._get("trait_outcomes"), width=12.8, font_size=22)
        with self.voiceover(
            "The third: personality traits predict consequential outcomes, from health to relationships to work. "
            "<bookmark mark='a'/> The original: Roberts and colleagues' review, in 2007. <bookmark mark='b'/> The "
            "record: Soto's seventy-eight preregistered replications, eighty-seven percent successful, with effects "
            "about three quarters the size. <bookmark mark='c'/> A strong record by Part 4's standards, though the "
            "replications used cross-sectional self-report panels. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_person_situation(self):
        card = ledger_card(self._get("person_situation"), width=12.8, font_size=21)
        with self.voiceover(
            "The fourth: traits predict behaviour only up to about point three, so behaviour is mostly situational. "
            "<bookmark mark='a'/> The original: Mischel's 1968 review. <bookmark mark='b'/> The record: Epstein's "
            "aggregation, Funder and Ozer's situational effects, and Fleeson's distributions of states. "
            "<bookmark mark='c'/> The point three was real for single acts. The story that personality doesn't exist "
            "was not. <bookmark mark='d'/> Story and record: the two came apart."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_mbti_types(self):
        card = ledger_card(self._get("mbti_types"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: people fall into distinct personality types that a questionnaire identifies reliably. "
            "<bookmark mark='a'/> The original: the type indicator's first manual, in 1962. <bookmark mark='b'/> The "
            "record: David Pittenger's 1993 review found weak evidence that the types are distinct, and frequent "
            "changes of type on retest; and the SAPA sample's extraversion has one hump, not two. "
            "<bookmark mark='c'/> Cutting a continuous trait at the middle makes types that are unstable near the "
            "cut and discard information. <bookmark mark='d'/> Failed, as types."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_likes_prediction(self):
        card = ledger_card(self._get("likes_prediction"), width=12.8, font_size=21)
        with self.voiceover(
            "The sixth: personality traits can be estimated from digital records such as likes. "
            "<bookmark mark='a'/> The original: Kosinski, Stillwell and Graepel, 2013. <bookmark mark='b'/> The "
            "record: the comparison with friends and spouses in 2015, Azucar's meta-analysis, and in 2024 a large "
            "language model reading status updates at about point two nine. <bookmark mark='c'/> Moderate accuracy, "
            "found again and again. The privacy questions are larger than the effect sizes. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_psychographic_targeting(self):
        card = ledger_card(self._get("psychographic_targeting"), width=12.8, font_size=22)
        with self.voiceover(
            "The seventh: ads matched to a person's personality are substantially more persuasive. "
            "<bookmark mark='a'/> The original: Matz and colleagues' field experiments, 2017. <bookmark mark='b'/> The "
            "record: Eckles, Gordon and Johnson's critique of the design. <bookmark mark='c'/> It's unresolved without "
            "randomized tests. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 33 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 2, "replicated, smaller": 1, "contested": 2, "story and record": 1,
                          "failed": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=19, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.6, 20, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.2, -0.2, 0])
        rows_ = rows_of([
            (r"what holds: \ five factors in literate samples, \ traits that predict lives, \ and footprints that "
             r"reveal traits", GOOD),
            (r"what fails: \ types", LOST),
            (r"what is argued: \ whether the five are universal, \ and whether targeting by personality works", YOU),
            (r"and one story that outran its record: \ that personality does not exist", P.ACCENT),
        ], 5.6, 22, 0.36).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: five factors in literate samples, traits that predict lives, "
            "and footprints that reveal traits. <bookmark mark='b'/> What fails: types. <bookmark mark='c'/> What's "
            "argued: whether the five are universal, and whether targeting by personality works. "
            "<bookmark mark='d'/> And one story that outran its record: that personality doesn't exist."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
