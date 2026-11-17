from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403

ROWS = [
    ("sequential_lineups",
     "Six new rows. The first: sequential line-ups separate guilty from innocent suspects better than simultaneous "
     "ones. <bookmark mark='a'/> The original: Lindsay and Wells, 1985. <bookmark mark='b'/> The record: ROC analyses, "
     "a field test, and the 2020 recommendations, which dropped the preference. <bookmark mark='c'/> The ratio "
     "rewarded caution, not discrimination. <bookmark mark='d'/> Failed."),
    ("initial_confidence",
     "The second: under fair, double-blind procedures, an initial high-confidence identification is usually accurate. "
     "<bookmark mark='a'/> The original: Juslin, Olsson and Winman's calibration analysis, 1996. <bookmark mark='b'/> "
     "The record: the feedback studies showing why only the first statement counts, a police department's "
     "line-ups, and Wixted and Wells's review. "
     "<bookmark mark='c'/> Confidence at trial is much less informative. <bookmark mark='d'/> Replicated."),
    ("lab_false_confession",
     "The third: innocent people accused of a minor offence in a laboratory often sign a confession. "
     "<bookmark mark='a'/> The original: Kassin and Kiechel, 1996. <bookmark mark='b'/> The record: a second paradigm "
     "with guilty and innocent participants, and a scientific review. <bookmark mark='c'/> The mechanisms are the ones "
     "found in documented false confessions. <bookmark mark='d'/> Replicated."),
    ("lie_detection_chance",
     "The fourth: people judging lies are only slightly better than chance. <bookmark mark='a'/> The original: Bond "
     "and DePaulo's meta-analysis, 2006. <bookmark mark='b'/> The record: little reliable difference between judges, "
     "and weak cues as the reason. <bookmark mark='c'/> The signal is weak. <bookmark mark='d'/> Replicated."),
    ("forensic_context",
     "The fifth: forensic examiners' conclusions can be changed by irrelevant context. <bookmark mark='a'/> The "
     "original: Dror, Charlton and Peron, 2006. <bookmark mark='b'/> The record: experts inconsistent with their own "
     "earlier decisions, and handwriting judged differently after a confession. <bookmark mark='c'/> Strongest on "
     "ambiguous evidence. <bookmark mark='d'/> Replicated."),
    ("hungry_judges",
     "And the sixth: judges grant parole far more often after a food break. <bookmark mark='a'/> The original: "
     "Danziger, Levav and Avnaim-Pesso, 2011. <bookmark mark='b'/> The record: the order of cases, and simulations "
     "that produce the pattern without fatigue. <bookmark mark='c'/> The decline is real; its cause isn't settled. "
     "<bookmark mark='d'/> Contested."),
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
        assert len(rows) == 6
        head = heading(r"What the six have in common")
        items = rows_of([
            (r"the reliable findings are about procedure: \ what a line-up, \ an interrogation or an examination "
             r"does to the evidence", GOOD),
            (r"the failures came from measuring a procedure by one number, \ or reading a pattern without its "
             r"design", AUTH),
            (r"law took up the research, \ and then took up its correction", MODEL),
            (r"a court should trust a memory, \ a confession or an expert as far as the procedure that produced it "
             r"deserves", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the six have in common. <bookmark mark='a'/> The reliable findings are about procedure: what a "
            "line-up, an interrogation or an examination does to the evidence. <bookmark mark='b'/> The failures came "
            "from measuring a procedure by one number, or reading a pattern without its design. <bookmark mark='c'/> "
            "The law took up the research, and then took up its correction. <bookmark mark='d'/> So here's the "
            "answer to this part's question. A court should trust a memory, a confession or an expert as far as the "
            "procedure that produced it deserves."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
