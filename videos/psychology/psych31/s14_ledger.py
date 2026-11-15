from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_deprivation_foster_care()
        self.row_perry_long_run()
        self.row_word_gap()
        self.row_birth_order_personality()
        self.row_birth_order_iq()
        self.row_chronotype_age()
        self.row_moral_stage_sex()
        self.row_positivity_effect()
        self.row_adult_neurogenesis()
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

    def row_deprivation_foster_care(self):
        card = ledger_card(self._get("deprivation_foster_care"), width=12.8, font_size=22)
        with self.voiceover(
            "Nine new rows today. The first: early institutional deprivation harms development, and placement in a "
            "family early in life helps. <bookmark mark='a'/> The original: the Bucharest lottery, reported in "
            "2007. <bookmark mark='b'/> The record: the English and Romanian Adoptees followed into their twenties, "
            "and the trial itself at eighteen, nine IQ points apart. <bookmark mark='c'/> A randomized trial and a "
            "natural experiment agree, though the trial is one city, and its effect at eighteen sits near the edge "
            "of significance. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_perry_long_run(self):
        card = ledger_card(self._get("perry_long_run"), width=12.8, font_size=21)
        with self.voiceover(
            "The second: a preschool programme for poor three- and four-year-olds improved their lives as adults. "
            "<bookmark mark='a'/> The original: Perry Preschool at forty. <bookmark mark='b'/> The record: "
            "Anderson's correction for many outcomes, Heckman's rate of return with the compromised assignment "
            "modelled, and the Abecedarian trial's health results. <bookmark mark='c'/> Long-run effects survive, "
            "smaller and narrower than first claimed, in small trials. <bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_word_gap(self):
        card = ledger_card(self._get("word_gap"), width=12.8, font_size=22)
        with self.voiceover(
            "The third: by age four, children in poor families have heard thirty million fewer words. "
            "<bookmark mark='a'/> The original: Hart and Risley, 1995. <bookmark mark='b'/> The record: day-long "
            "automated recordings that find a smaller gap with wide variation, and a study that finds none once "
            "overheard speech is counted. <bookmark mark='c'/> Talk directed at children matters; the size, cause "
            "and measurement of the gap are disputed. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_birth_order_personality(self):
        card = ledger_card(self._get("birth_order_personality"), width=12.8, font_size=22)
        with self.voiceover(
            "The fourth: birth order shapes personality. <bookmark mark='a'/> The original: Frank Sulloway's Born to "
            "Rebel, 1996. <bookmark mark='b'/> The record: twenty thousand adults compared within families, and "
            "three hundred and seventy-seven thousand students. <bookmark mark='c'/> Nothing of practical size. "
            "<bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_birth_order_iq(self):
        card = ledger_card(self._get("birth_order_iq"), width=12.8, font_size=22)
        with self.voiceover(
            "The fifth: firstborns score slightly higher on intelligence tests. <bookmark mark='a'/> The original: "
            "nearly four hundred thousand Dutch men in 1973. <bookmark mark='b'/> The record: Norway's conscripts, "
            "with the rank in which a child is raised doing the work, and the two 2015 studies. "
            "<bookmark mark='c'/> Small, one to three points. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_chronotype_age(self):
        card = ledger_card(self._get("chronotype_age"), width=12.8, font_size=22)
        with self.voiceover(
            "The sixth: chronotype is latest at about twenty. <bookmark mark='a'/> The original: Roenneberg's "
            "survey of twenty-five thousand people, 2004. <bookmark mark='b'/> The record: twelve years of the "
            "American Time Use Survey. <bookmark mark='c'/> The curve replicates; reading its peak as the end of "
            "adolescence is a proposal. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_moral_stage_sex(self):
        card = ledger_card(self._get("moral_stage_sex"), width=12.8, font_size=22)
        with self.voiceover(
            "The seventh: Kohlberg's stages score women's moral reasoning lower than men's. <bookmark mark='a'/> "
            "The original: Carol Gilligan, 1982. <bookmark mark='b'/> The record: Walker's review of a hundred and "
            "eight studies, and Jaffee and Hyde's meta-analysis. <bookmark mark='c'/> Stage scores show few sex "
            "differences; the orientations differ slightly. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_positivity_effect(self):
        card = ledger_card(self._get("positivity_effect"), width=12.8, font_size=22)
        with self.voiceover(
            "The eighth: older adults favour positive over negative material. <bookmark mark='a'/> The original: "
            "Charles, Mather and Carstensen, 2003. <bookmark mark='b'/> The record: a meta-analysis of a hundred "
            "studies. <bookmark mark='c'/> Reliable on average and moderated by method; its explanation is argued. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_adult_neurogenesis(self):
        card = ledger_card(self._get("adult_neurogenesis"), width=12.8, font_size=21)
        with self.voiceover(
            "And the ninth: the adult human hippocampus keeps making new neurons into old age. "
            "<bookmark mark='a'/> The original: Eriksson and Gage, 1998. <bookmark mark='b'/> The record: one study "
            "finding none in adults, and two finding them into old age. <bookmark mark='c'/> The disagreement is "
            "largely about method. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 31 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 4, "replicated, smaller": 1, "contested": 2, "failed": 2}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=19, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.6, 20, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.2, -0.2, 0])
        rows_ = rows_of([
            (r"what holds: \ deprivation harms and families help; \ curves of sleep and emotion across life; \ "
             r"a small IQ edge for the eldest", GOOD),
            (r"what fails: \ stories about personality from birth order, \ and about women's moral reasoning", LOST),
            (r"what is argued: \ how large the word gap is, \ and whether adults grow new neurons", PERIOD),
            (r"the strongest rows rest on randomization or on very large samples compared within families", YOU),
        ], 5.6, 22, 0.36).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: deprivation harms and families help; the curves of sleep "
            "and emotion across life; and a small IQ edge for the eldest. <bookmark mark='b'/> What fails: stories "
            "about personality from birth order, and about women's moral reasoning. <bookmark mark='c'/> What's "
            "argued: how large the word gap is, and whether adults grow new neurons. <bookmark mark='d'/> And the "
            "strongest rows rest on randomization, or on very large samples compared within families: the designs "
            "this part has been about."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
