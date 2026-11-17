from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403

ROWS = [
    ("exposure_efficacy",
     "Eight new rows today. The first: treatments built on exposure reduce anxiety more than control conditions. "
     "<bookmark mark='a'/> The original: Wolpe's systematic desensitization, 1958. <bookmark mark='b'/> The record: a "
     "meta-analysis of placebo-controlled trials, and the inhibitory-learning review. <bookmark mark='c'/> Among the "
     "best-supported treatments in psychology. <bookmark mark='d'/> Replicated."),
    ("fear_renewal",
     "The second: extinguished fear returns with a change of context, with time, or after a reminder. "
     "<bookmark mark='a'/> The original: Bouton and Bolles, 1979. <bookmark mark='b'/> The record: a review of animal "
     "and human studies. <bookmark mark='c'/> Extinction is new, context-bound learning. <bookmark mark='d'/> "
     "Replicated."),
    ("learned_helplessness",
     "The third: animals given uncontrollable shock later fail to escape. <bookmark mark='a'/> The original: "
     "Seligman and Maier, 1967. <bookmark mark='b'/> The record: their own 2016 review. <bookmark mark='c'/> The "
     "effect replicates; its explanation was reversed. <bookmark mark='d'/> Replicated."),
    ("attention_bias_modification",
     "The fourth: training attention away from threat reduces anxiety. <bookmark mark='a'/> The original: MacLeod "
     "and colleagues, 2002. <bookmark mark='b'/> The record: a meta-analysis of the trials. <bookmark mark='c'/> Small "
     "effects that vanished after correcting for bias. <bookmark mark='d'/> Failed."),
    ("serotonin_deficit",
     "The fifth: depression is a shortage of serotonin. <bookmark mark='a'/> The original: the monoamine "
     "hypothesis, 1965. <bookmark mark='b'/> The record: the 2022 umbrella review. <bookmark mark='c'/> No consistent "
     "evidence, as stated. <bookmark mark='d'/> Failed."),
    ("antidepressants_placebo",
     "The sixth: antidepressants beat placebo. <bookmark mark='a'/> The original analysis here: Kirsch and "
     "colleagues, 2008. <bookmark mark='b'/> The record: five hundred and twenty-two trials. <bookmark mark='c'/> A "
     "real average effect, and a modest one. <bookmark mark='d'/> Replicated, smaller."),
    ("httlpr_stress",
     "The seventh: stress causes depression more often in carriers of a serotonin gene variant. "
     "<bookmark mark='a'/> The original: Caspi and colleagues, 2003. <bookmark mark='b'/> The record: thirty-eight "
     "thousand people, and the candidate-gene tests of 2019. <bookmark mark='c'/> No interaction. "
     "<bookmark mark='d'/> Failed."),
    ("suicide_prediction",
     "And the eighth: known risk factors predict who will attempt suicide with useful accuracy. "
     "<bookmark mark='a'/> The original test: Pokorny, 1983. <bookmark mark='b'/> The record: fifty years of studies. "
     "<bookmark mark='c'/> Associations are real; individual prediction is poor. <bookmark mark='d'/> Failed."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
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
        head = heading(r"Part 40 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "replicated, smaller": 1, "failed": 4}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=16, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 17, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ exposure, \ the return of fear, \ helplessness, \ and a small advantage of "
             r"antidepressants over placebo", GOOD),
            (r"what failed: \ attention training, \ the serotonin-deficit story, \ a celebrated gene-by-stress "
             r"interaction, \ and predicting suicide from risk factors", AUTH),
            (r"the learning models hold up better than the chemical and genetic stories", MODEL),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: exposure, the return of fear, helplessness, and a small "
            "advantage of antidepressants over placebo. <bookmark mark='b'/> What failed: attention training, the "
            "serotonin-deficit story, a celebrated gene-by-stress interaction, and predicting suicide from risk "
            "factors. <bookmark mark='c'/> The learning models hold up better than the chemical and genetic stories."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
