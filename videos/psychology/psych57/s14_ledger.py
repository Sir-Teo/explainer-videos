from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403

ROWS = [
    ("stress_infection",
     "Seven new rows. The first: people under more stress are more likely to catch a cold after exposure to the "
     "virus. <bookmark mark='a'/> The original: Cohen, Tyrrell and Smith, 1991. <bookmark mark='b'/> The record: "
     "chronic stressors raising the risk, and a mechanism in glucocorticoid resistance. <bookmark mark='c'/> One of "
     "the strongest results in the field. <bookmark mark='d'/> Replicated."),
    ("placebo_analgesia",
     "The second: placebos reduce reported pain, partly through the brain's own opioids. <bookmark mark='a'/> The "
     "original: Levine, Gordon and Fields, 1978. <bookmark mark='b'/> The record: the neurobiology reviewed, and a "
     "Cochrane review of placebo against no treatment. <bookmark mark='c'/> Real, modest and variable. "
     "<bookmark mark='d'/> Replicated."),
    ("placebo_objective",
     "The third: placebos produce large improvements generally, objective outcomes included. <bookmark mark='a'/> "
     "The original: Beecher, 1955. <bookmark mark='b'/> The record: trials with no-treatment arms, showing little "
     "effect on objective outcomes. <bookmark mark='c'/> Most improvement on placebo is natural recovery. "
     "<bookmark mark='d'/> Failed."),
    ("open_label_placebo",
     "The fourth: placebos given openly still improve symptoms. <bookmark mark='a'/> The original: Kaptchuk and "
     "colleagues, 2010. <bookmark mark='b'/> The record: a back-pain trial and a meta-analysis, all small and "
     "self-reported. <bookmark mark='c'/> Real, or reporting shaped by hope. <bookmark mark='d'/> Contested."),
    ("lifestyle_diabetes",
     "The fifth: an intensive lifestyle programme reduces type 2 diabetes in people at high risk. "
     "<bookmark mark='a'/> The original: the Finnish prevention study, 2001. <bookmark mark='b'/> The record: the "
     "American Diabetes Prevention Program and its ten-year follow-up. <bookmark mark='c'/> Behaviour is the "
     "treatment. <bookmark mark='d'/> Replicated."),
    ("type_a",
     "The sixth: the Type A pattern causes heart disease. <bookmark mark='a'/> The original: the Western "
     "Collaborative Group Study. <bookmark mark='b'/> The record: a larger cohort finding nothing, and a small "
     "association for hostility alone. <bookmark mark='c'/> Hostility remains, weaker. <bookmark mark='d'/> Failed."),
    ("maids_mindset",
     "And the seventh: telling hotel workers their work is exercise improves their health. <bookmark mark='a'/> The "
     "original: Crum and Langer, 2007. <bookmark mark='b'/> The record: a related study of beliefs about food, and "
     "no replication at scale. <bookmark mark='c'/> Plausible, and untested. <bookmark mark='d'/> Contested."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("society",),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
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
        assert len(rows) == 7
        head = heading(r"What the seven have in common")
        items = rows_of([
            (r"mind affects body through mechanisms that can be measured: \ stress hormones, \ opioids, \ "
             r"behaviour", GOOD),
            (r"the effects that hold are modest and specific; \ the sweeping ones, \ a powerful placebo or a "
             r"personality that breaks hearts, \ failed", AUTH),
            (r"the largest health effect in the list is a behaviour, \ changed by a programme", MODEL),
            (r"the mind gets into the body in measurable, \ modest ways; \ help gets to people through systems, \ "
             r"not single techniques", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the seven have in common. <bookmark mark='a'/> Mind affects body through mechanisms that can be "
            "measured: stress hormones, opioids and behaviour. <bookmark mark='b'/> The effects that hold are modest "
            "and specific. The sweeping ones, a powerful placebo or a personality that breaks hearts, failed. "
            "<bookmark mark='c'/> The largest health effect in the list is a behaviour, changed by a programme. "
            "<bookmark mark='d'/> So here's the answer to this part's question. The mind gets into the body in "
            "measurable, modest ways, and help gets to people through systems, not single techniques."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
