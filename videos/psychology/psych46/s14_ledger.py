from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403

ROWS = [
    ("attraction_effect",
     "Four new rows. The first: a decoy that is worse than one option, but not the other, raises the share of the "
     "option that dominates it. <bookmark mark='a'/> The original: Huber, Payne and Puto, 1982. <bookmark mark='b'/> "
     "The record: with pictures and realistic descriptions it was weak or absent, and in many product categories it "
     "did not appear. <bookmark mark='c'/> Robust with numbers in a table, much weaker when dominance has to be seen. "
     "<bookmark mark='d'/> Contested."),
    ("forbid_allow",
     "The second: asking whether something should be forbidden or allowed gives different answers. "
     "<bookmark mark='a'/> The original: Rugg, 1941. <bookmark mark='b'/> The record: Schuman and Presser's "
     "split-ballot experiments, and later studies across topics. <bookmark mark='c'/> Wording and order effects are "
     "among survey research's most reliable findings. <bookmark mark='d'/> Replicated."),
    ("acquiescence",
     "The third: some people agree with statements regardless of content. <bookmark mark='a'/> The original: "
     "Cronbach, 1946. <bookmark mark='b'/> The record: a separate style factor in balanced scales, and the style "
     "stable within people over a year. <bookmark mark='c'/> Balanced keys cancel it in a sum. <bookmark mark='d'/> "
     "Replicated."),
    ("nps_growth",
     "And the fourth: the net promoter score predicts growth better than other measures. <bookmark mark='a'/> The "
     "original: Reichheld, 2003. <bookmark mark='b'/> The record: tested over time, no better than the alternatives. "
     "<bookmark mark='c'/> A simple tracking number, not the best predictor of growth. <bookmark mark='d'/> Failed."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("person",),
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
        assert len(rows) == 4
        head = heading(r"What the four have in common")
        items = rows_of([
            (r"two are about the instrument: \ wording and styles change answers, \ reliably", GOOD),
            (r"one is about choice: \ the decoy is real where dominance is easy to see, \ and fragile elsewhere", AUTH),
            (r"one is about a business claim, \ made without the data to test it", AUTH),
            (r"the instrument effects replicate best: \ they are about how people answer, \ which is what surveys "
             r"measure most", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the four have in common. <bookmark mark='a'/> Two are about the instrument: wording and response "
            "styles change answers, reliably. <bookmark mark='b'/> One is about choice. The decoy is real where "
            "dominance is easy to see, and fragile elsewhere. <bookmark mark='c'/> One is a business claim, made "
            "without the data to test it. <bookmark mark='d'/> The effects of the instrument replicate best. They are "
            "about how people answer, which is what surveys measure most directly."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
