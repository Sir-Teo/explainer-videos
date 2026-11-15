from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_selection_content()
        self.row_belief_bias()
        self.row_mental_rotation()
        self.row_chess_chunking()
        self.row_ten_thousand_hours()
        self.row_everyday_prediction()
        self.tally()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _row(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo, marks="abcd"):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until(marks[0])
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until(marks[1])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def row_selection_content(self):
        card = ledger_card(self._row("selection_content"), width=12.8, font_size=24)
        with self.voiceover(
            "Six rows today. The first: the selection task is solved far more often when the rule is a familiar "
            "permission than when it is abstract. <bookmark mark='a'/> The original: Griggs and Cox, 1982, with the "
            "drinking age. <bookmark mark='b'/> The record: Cheng and Holyoak's permission rules in 1985, and "
            "Cosmides's social contracts in 1989, and many studies since. <bookmark mark='c'/> The effect is robust; "
            "what causes it is still argued. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_belief_bias(self):
        card = ledger_card(self._row("belief_bias"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: people accept believable conclusions more than unbelievable ones, most of all when they "
            "don't follow. <bookmark mark='a'/> The original: Evans, Barston and Pollard, 1983. "
            "<bookmark mark='b'/> The record: Klauer and colleagues' model of eight experiments in 2000, and Dube, "
            "Rotello and Heit's reanalysis in 2010, which reads the effect as a shift in the threshold for saying "
            "yes. <bookmark mark='c'/> One of the most reliable effects in reasoning, with its explanation argued. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_mental_rotation(self):
        card = ledger_card(self._row("mental_rotation"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: the time to compare two figures grows linearly with the angle between them. "
            "<bookmark mark='a'/> The original: Shepard and Metzler, 1971, with eight people. "
            "<bookmark mark='b'/> The record: Cooper and Shepard's rotated letters, and Ganis and Kievit's open data "
            "from fifty-four people, fitted in this part. <bookmark mark='c'/> One of the steadiest effects in "
            "cognition. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_chess_chunking(self):
        card = ledger_card(self._row("chess_chunking"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: chess experts recall positions from real games far better than novices, but not random "
            "positions. <bookmark mark='a'/> The original: Chase and Simon, 1973, with three players. "
            "<bookmark mark='b'/> The record: Gobet and Simon's finding in 1996 that a small advantage survives on "
            "random boards, and Sala and Gobet's meta-analysis in 2017, which found that small edge across fields "
            "of expertise. <bookmark mark='c'/> Replicated many times, with that small "
            "edge explained by chunks that turn up by chance. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_ten_thousand_hours(self):
        card = ledger_card(self._row("ten_thousand_hours"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: expert performance is mainly the product of about ten thousand hours of deliberate practice. "
            "<bookmark mark='a'/> The original: Ericsson, Krampe and Tesch-Römer, 1993. <bookmark mark='b'/> The "
            "record: Macnamara and colleagues' meta-analysis of eighty-eight studies, and a 2019 replication of the "
            "violin study. <bookmark mark='c'/> Practice matters, but the rule is not what the study found, and not "
            "what the record supports. <bookmark mark='d'/> Story and record."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_everyday_prediction(self):
        card = ledger_card(self._row("everyday_prediction"), width=12.8, font_size=24)
        with self.voiceover(
            "And the sixth: people's everyday predictions match the optimal Bayesian predictions for each domain. "
            "<bookmark mark='a'/> The original: Griffiths and Tenenbaum, 2006. <bookmark mark='b'/> The record: "
            "Mozer and colleagues' model of people who each recall a few examples, and Lewandowsky and colleagues' "
            "chains of learners, which found good priors in individuals. <bookmark mark='c'/> The group-level match "
            "is robust; how much each person knows is contested. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 24 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 5, "story and record": 1}
        lines = VGroup(*[label(rf"{st}: \ {n}", font_size=30, color=GREY_A) for st, n in counts.items()]).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.2, 0.5, 0])
        rows_ = rows_of([
            (r"reasoning's classic effects replicate: \ content, \ belief, \ rotation, \ chunks", MODEL),
            (r"what is argued is what they mean: \ schemas or information, \ bias or threshold, \ crowds or "
             r"individuals", LOGIC),
            (r"the one story that failed is the one that left the laboratory: \ ten thousand hours", LOST),
        ], 6.2, 23, 0.34).move_to([3.3, 0.3, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> Five rows replicated: the classic effects of reasoning are among the "
            "sturdiest in psychology. <bookmark mark='b'/> What's argued is what they mean: schemas or information, "
            "a change of reasoning or of threshold, wise crowds or wise individuals. <bookmark mark='c'/> And the "
            "one claim the record doesn't support is the one that left the laboratory and became a rule for life: "
            "ten thousand hours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
