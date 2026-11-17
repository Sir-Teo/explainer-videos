from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403

ROWS = [
    ("hollow_mask_schizophrenia",
     "Eight new rows today. The first: people with schizophrenia are fooled less often by the hollow mask. "
     "<bookmark mark='a'/> The original: Emrich, 1989. <bookmark mark='b'/> The record: two later studies, one with "
     "brain imaging. <bookmark mark='c'/> Replicated, in small samples; a large preregistered test is still missing. "
     "<bookmark mark='d'/> Replicated."),
    ("antipsychotic_efficacy",
     "The second: antipsychotics reduce positive symptoms and prevent relapse better than placebo. "
     "<bookmark mark='a'/> The original: Delay and Deniker, 1952. <bookmark mark='b'/> The record: meta-analyses of "
     "relapse prevention and of sixty years of trials. <bookmark mark='c'/> A real effect, with real costs. "
     "<bookmark mark='d'/> Replicated."),
    ("strong_prior_hallucinations",
     "The third: voice hearers weight priors more, and so hear conditioned tones more often. <bookmark mark='a'/> "
     "The original: Powers, Mathys and Corlett, 2017. <bookmark mark='b'/> The record: a follow-up by the same group. "
     "<bookmark mark='c'/> Few independent tests, and an open question about what the model predicts uniquely. "
     "<bookmark mark='d'/> Contested."),
    ("rat_park",
     "The fourth: rats in a social colony drink far less morphine than rats alone. <bookmark mark='a'/> The original: "
     "Alexander and colleagues, 1978. <bookmark mark='b'/> The record: a replication that found little difference. "
     "<bookmark mark='c'/> Told more often than tested. <bookmark mark='d'/> Contested."),
    ("contingency_management",
     "The fifth: paying for drug-free samples increases abstinence. <bookmark mark='a'/> The original: Higgins and "
     "colleagues, 1991. <bookmark mark='b'/> The record: a meta-analysis of the trials. <bookmark mark='c'/> It works "
     "while the incentives last. <bookmark mark='d'/> Replicated."),
    ("vaccines_autism",
     "The sixth: the measles, mumps and rubella vaccine causes autism. <bookmark mark='a'/> The original: Wakefield "
     "and colleagues, 1998. <bookmark mark='b'/> The record: the retraction, and a cohort of six hundred and "
     "fifty-seven thousand children. <bookmark mark='c'/> Misconduct, and no association. <bookmark mark='d'/> "
     "Retracted."),
    ("facilitated_communication",
     "The seventh: facilitated typing lets non-speaking autistic people communicate. <bookmark mark='a'/> The "
     "original: Biklen, 1990. <bookmark mark='b'/> The record: controlled tests, and a review. <bookmark mark='c'/> "
     "The messages came from the facilitators. <bookmark mark='d'/> Failed."),
    ("adhd_stimulants",
     "And the eighth: stimulants reduce ADHD symptoms more than behavioural treatment alone. <bookmark mark='a'/> "
     "The original: the MTA trial, 1999. <bookmark mark='b'/> The record: its three-year follow-up, and a network "
     "meta-analysis of short-term trials. <bookmark mark='c'/> Short-term benefit holds; the long-term advantage "
     "faded. <bookmark mark='d'/> Replicated, smaller."),
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
        head = heading(r"Part 41 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "contested": 2, "retracted": 1, "failed": 1, "replicated, smaller": 1}, counts
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=16, width=3.0)
            table.add(VGroup(chip, wrapped_label(f.title, 3.8, 17, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.1, -0.3, 0])
        rows_ = rows_of([
            (r"what holds: \ the hollow-mask difference, \ antipsychotics, \ contingency management, \ and "
             r"stimulants in the short term", GOOD),
            (r"what is argued: \ hallucinations as strong priors, \ and Rat Park", STATUS_COLOR["contested"]),
            (r"what fell: \ the vaccine fraud, \ and facilitated communication, \ both settled by plain controlled "
             r"tests", AUTH),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> What holds: the hollow-mask difference, antipsychotics, contingency "
            "management, and stimulants in the short term. <bookmark mark='b'/> What's argued: hallucinations as "
            "strong priors, and Rat Park. <bookmark mark='c'/> What fell: the vaccine fraud, and facilitated "
            "communication, both settled by plain controlled tests."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
