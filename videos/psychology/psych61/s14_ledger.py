from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403

ROWS = [
    ("life_outcomes_unpredictable",
     "Four new rows. The first: children's life outcomes are hard to predict, whatever the method. "
     "<bookmark mark='a'/> The original: Salganik and colleagues, 2020. <bookmark mark='b'/> The record: a hundred "
     "and sixty teams inside the one study; no other cohort yet. <bookmark mark='c'/> The ceiling is in the outcomes, "
     "not the methods. <bookmark mark='d'/> Not directly tested."),
    ("manylabs_heterogeneity",
     "The second: most effects vary little between labs and countries beyond sampling error. <bookmark mark='a'/> "
     "The original: Many Labs 1, 2014. <bookmark mark='b'/> The record: Many Labs 2, and a review of many replication "
     "projects. <bookmark mark='c'/> Context matters less than single studies suggest. <bookmark mark='d'/> "
     "Replicated."),
    ("web_equals_lab",
     "The third: experiments online give results comparable to the lab. <bookmark mark='a'/> The original: Germine "
     "and colleagues, 2012. <bookmark mark='b'/> The record: classic paradigms reproduced on a crowdsourcing "
     "platform. <bookmark mark='c'/> With care for data quality and timing. <bookmark mark='d'/> Replicated."),
    ("twitter_heart_disease",
     "And the fourth: county tweets predict heart disease deaths. <bookmark mark='a'/> The original: Eichstaedt and "
     "colleagues, 2015. <bookmark mark='b'/> The record: a reanalysis that found the result fragile. "
     "<bookmark mark='c'/> A population association at best. <bookmark mark='d'/> Contested."),
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
            if len(card.record):
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
        assert len(rows) == 4
        head = heading(r"What the four have in common")
        items = rows_of([
            (r"the methods of the next psychology already have records: \ online labs and many-labs designs "
             r"replicate", GOOD),
            (r"prediction sets humbling ceilings, \ and digital traces need validation at the right level", AUTH),
            (r"what changes a field is what it selects: \ registered results, \ shared data, \ big teams", MODEL),
            (r"designed today, \ psychology would be larger, \ broader, \ formal, \ and selected for "
             r"rigour", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> The methods of the next psychology already have "
            "records: online labs and many-labs designs replicate. <bookmark mark='b'/> Prediction sets humbling "
            "ceilings, and digital traces need validation at the right level. <bookmark mark='c'/> What changes a "
            "field is what it selects: registered results, shared data, and big teams. <bookmark mark='d'/> So "
            "here's the answer to this part's question. Designed today, psychology would be larger, broader and "
            "formal, and it would select for rigour."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
