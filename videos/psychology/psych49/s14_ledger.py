from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403

ROWS = [
    ("analytic_variability",
     "Five new rows. The first: different defensible pipelines applied to the same brain data can reach different "
     "conclusions. <bookmark mark='a'/> The original: Joshua Carp, 2012. <bookmark mark='b'/> The record: the seventy "
     "teams of 2020, and many-analyst studies outside neuroscience. <bookmark mark='c'/> The variation is in the "
     "analysis, so report the forks and register the pipeline. <bookmark mark='d'/> Replicated."),
    ("default_mode",
     "The second: the default mode network. <bookmark mark='a'/> The original: Raichle and colleagues, 2001. "
     "<bookmark mark='b'/> The record: correlated at rest, and found again in thousands of scans. "
     "<bookmark mark='c'/> Its function is still argued, and its anticorrelations depend on the analysis. "
     "<bookmark mark='d'/> Replicated."),
    ("small_bwas",
     "The third: brain-behaviour correlations from a few dozen people are large and reproducible. "
     "<bookmark mark='a'/> The original: the studies Kanai and Rees reviewed in 2011. <bookmark mark='b'/> The record: "
     "a preregistered replication of seventeen such correlations found evidence for almost none, and samples of "
     "thousands found the true ones small. <bookmark mark='c'/> The associations are real but small, as chapter "
     "twelve computed. <bookmark mark='d'/> Failed."),
    ("lenient_clusters",
     "The fourth: cluster inference at a lenient threshold controls false positives at five percent. "
     "<bookmark mark='a'/> The original: Friston and colleagues' random field theory, 1994. <bookmark mark='b'/> The "
     "record: Woo, Krishnan and Wager's warning, and Eklund, Nichols and Knutsson's null analyses of real data. "
     "<bookmark mark='c'/> Stricter primary thresholds, or permutation, fix it. <bookmark mark='d'/> Failed."),
    ("category_decoding",
     "And the fifth: object categories can be decoded from patterns in ventral temporal cortex. "
     "<bookmark mark='a'/> The original: Haxby and colleagues, 2001. <bookmark mark='b'/> The record: the same "
     "structure in monkeys and humans, and decoding across people. <bookmark mark='c'/> Decodable means present, not "
     "necessarily used. <bookmark mark='d'/> Replicated."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("brain",),
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
            (r"three replicated: \ a network found in every large sample, \ a pattern found in every lab, \ and the "
             r"variability of analysis itself", GOOD),
            (r"two failed, \ and both are failures of method: \ samples too small, \ and an approximation that did "
             r"not hold", AUTH),
            (r"both failures were caught by testing methods where the truth was known, \ or by data large enough to "
             r"know it", PERSON),
            (r"a brain map is evidence when the pipeline was fixed in advance, \ the threshold matches the noise, \ "
             r"and the sample matches the effect", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the five have in common. <bookmark mark='a'/> Three replicated: a network found in every large "
            "sample, a pattern found in every lab, and the variability of analysis itself. <bookmark mark='b'/> Two "
            "failed, and both are failures of method: samples too small, and an approximation that didn't hold. "
            "<bookmark mark='c'/> Both were caught by testing methods where the truth was known, or with data large "
            "enough to know it. <bookmark mark='d'/> So here's the answer to this part's question. A brain map is "
            "evidence when the pipeline was fixed in advance, the threshold matches the noise, and the sample "
            "matches the size of the effect."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
