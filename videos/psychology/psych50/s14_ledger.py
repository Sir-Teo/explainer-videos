from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403

ROWS = [
    ("antidepressant_bias",
     "Five new rows. The first: the journal literature on antidepressants overstated their efficacy. "
     "<bookmark mark='a'/> The original: Turner and colleagues, 2008. <bookmark mark='b'/> The record: meta-analyses "
     "of the regulator's data, and a network meta-analysis of over five hundred trials, including unpublished ones. "
     "<bookmark mark='c'/> The drugs work, modestly. The published record made them look better. "
     "<bookmark mark='d'/> Replicated."),
    ("meta_inflation",
     "The second: meta-analyses of published studies estimate effects about as large as large preregistered "
     "replications do. <bookmark mark='a'/> The original: the ego-depletion meta-analysis of 2010, as an example. "
     "<bookmark mark='b'/> The record: the registered replication of Part 43, and Kvarven and colleagues' fifteen "
     "comparisons, with meta-analyses about three times larger. <bookmark mark='c'/> A meta-analysis inherits its "
     "literature's filter. <bookmark mark='d'/> Failed."),
    ("p_inconsistency",
     "The third: a substantial share of psychology articles report a p-value that doesn't match its own test "
     "statistic. <bookmark mark='a'/> The original: Bakker and Wicherts, 2011. <bookmark mark='b'/> The record: "
     "statcheck's sweep of a quarter of a million p-values, finding about half of articles with at least one. "
     "<bookmark mark='c'/> Most errors are small, and the gross ones lean towards significance. "
     "<bookmark mark='d'/> Replicated."),
    ("replication_prediction",
     "The fourth: researchers' pooled beliefs predict which findings will replicate. <bookmark mark='a'/> The "
     "original: Dreber and colleagues' prediction markets, 2015. <bookmark mark='b'/> The record: markets and "
     "surveys on later replication projects. <bookmark mark='c'/> The field could tell; it published the fragile "
     "findings anyway. <bookmark mark='d'/> Replicated."),
    ("rigour_replicability",
     "And the fifth: discoveries made with rigour-enhancing practices replicate at near the rate their power "
     "predicts. <bookmark mark='a'/> The original: Protzko and colleagues, 2023. <bookmark mark='b'/> The record: "
     "the article was retracted in 2024, after concerns about its own preregistration and reporting. "
     "<bookmark mark='c'/> The practices remain reasonable; this evidence for them is gone. <bookmark mark='d'/> "
     "Retracted."),
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
        assert len(rows) == 5
        head = heading(r"What the five have in common")
        items = rows_of([
            (r"all five are about the literature itself: \ what gets published, \ how it is pooled, \ how it is "
             r"reported, \ and how well the field knows its own weak spots", WHITE),
            (r"the filter was visible only where a denominator existed: \ a registry, \ a multi-lab protocol, \ a full "
             r"set of p-values", PERSON),
            (r"and the reformers' own work is held to the same standard: \ one row is a retraction", AUTH),
            (r"the weight of evidence is the weight of the studies that would have been seen whatever they found", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the five have in common. <bookmark mark='a'/> All five are about the literature itself: what gets "
            "published, how it's pooled, how it's reported, and how well the field knows its own weak spots. "
            "<bookmark mark='b'/> The filter was visible only where a denominator existed: a registry, a multi-lab "
            "protocol, a full set of p-values. <bookmark mark='c'/> And the reformers' own work is held to the same "
            "standard. One row is a retraction. <bookmark mark='d'/> So here's the answer to this part's question. "
            "The weight of evidence is the weight of the studies that would have been seen whatever they found."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
