from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403

ROWS = [
    ("weird_samples",
     "Nine new rows today. The first: most participants in psychology's leading journals come from WEIRD "
     "societies. <bookmark mark='a'/> The original count: Arnett, 2008. <bookmark mark='b'/> The record: the WEIRD "
     "review, Psychological Science in 2014, and the same six journals a decade on. <bookmark mark='c'/> Still true; "
     "the share from other Western countries grew, not the share from the majority world. "
     "<bookmark mark='d'/> Replicated."),
    ("self_construal",
     "The second: East Asians construe the self as interdependent, Westerners as independent, and questionnaires "
     "measure it. <bookmark mark='a'/> The original: Markus and Kitayama, 1991. <bookmark mark='b'/> The record: a "
     "meta-analysis of the scales, and the reference-group effect. <bookmark mark='c'/> Behaviour and attention "
     "replicate better than self-report scales. <bookmark mark='d'/> Contested."),
    ("rice_theory",
     "The third: rice farming makes thinking more holistic and interdependent. <bookmark mark='a'/> The original: "
     "Talhelm and colleagues, 2014. <bookmark mark='b'/> The record: a critical reanalysis, and a thirty-nine-"
     "country survey linking farming to relational mobility. <bookmark mark='c'/> Bold, and unsettled. "
     "<bookmark mark='d'/> Contested."),
    ("trolley_universal",
     "The fourth: everywhere, sacrificing one to save five is more acceptable by a switch than by a push. "
     "<bookmark mark='a'/> The original: Greene and colleagues, 2001. <bookmark mark='b'/> The record: forty-two "
     "countries in 2020, and forty-five in 2022. <bookmark mark='c'/> The order is universal in these samples; the "
     "level varies. <bookmark mark='d'/> Replicated."),
    ("moral_foundations_structure",
     "The fifth: five moral foundations, measured the same way across cultures. <bookmark mark='a'/> The original: "
     "Graham, Haidt and Nosek, 2009. <bookmark mark='b'/> The record: the questionnaire in twenty-seven countries. "
     "<bookmark mark='c'/> The five-factor structure doesn't travel cleanly. <bookmark mark='d'/> Contested."),
    ("infant_helper",
     "The sixth: infants prefer a helper to a hinderer. <bookmark mark='a'/> The original: Hamlin, Wynn and Bloom, "
     "2007. <bookmark mark='b'/> The record: ManyBabies 4, thirty-seven laboratories. <bookmark mark='c'/> Chance, "
     "in both conditions. <bookmark mark='d'/> Failed."),
    ("population_complexity",
     "The seventh: larger populations accumulate skills, and small isolated ones lose them. "
     "<bookmark mark='a'/> The original: Henrich's model of Tasmania, 2004. <bookmark mark='b'/> The record: Vaesen "
     "and colleagues' critique. <bookmark mark='c'/> Whether it explains the archaeological record is argued. "
     "<bookmark mark='d'/> Contested."),
    ("overimitation_culture",
     "The eighth: children copy a demonstrator's useless actions, in every culture tested. "
     "<bookmark mark='a'/> The original: Horner and Whiten, 2005. <bookmark mark='b'/> The record: San children in "
     "the Kalahari, Aka and Ngandu children in the Congo Basin, and a comparison across societies. "
     "<bookmark mark='c'/> Found wherever it has been tested; how much varies. <bookmark mark='d'/> Replicated."),
    ("moral_dumbfounding",
     "And the ninth: people keep moral judgments they can't justify once every reason is ruled out. "
     "<bookmark mark='a'/> The original: Haidt, 2001. <bookmark mark='b'/> The record: Royzman and colleagues' "
     "checks on beliefs about harm. <bookmark mark='c'/> Intuition shapes judgment; true dumbfounding is rarer "
     "than it seemed. <bookmark mark='d'/> Contested."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def row(self, key, text):
        card = ledger_card(self._get(key), width=12.8, font_size=21)
        with self.voiceover(text) as vo:
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
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 38 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "contested": 5, "failed": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=17, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 18, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ WEIRD sampling, \ the switch-footbridge order across countries, \ and overimitation",
             GOOD),
            (r"what failed: \ infants' preference for helpers at six to ten months", AUTH),
            (r"what is argued: \ self-construal scales, \ the rice theory, \ the five foundations, \ population "
             r"size, \ and moral dumbfounding", YOU),
            (r"the structure of a judgment often travels; \ its level, \ and the questionnaires, \ often do not", MODEL),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: WEIRD sampling, the order of the trolley cases across "
            "countries, and children's faithful copying. <bookmark mark='b'/> What failed: infants' preference for helpers at six to ten months. "
            "<bookmark mark='c'/> What's argued: self-construal scales, the rice theory, the five foundations, "
            "population size, and moral dumbfounding. <bookmark mark='d'/> The structure of a judgment often travels. Its level, and the "
            "questionnaires used to measure it, often don't."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abcd", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
