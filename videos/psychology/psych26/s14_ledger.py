from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_framing_disease()
        self.row_anchoring()
        self.row_allais()
        self.row_conjunction_fallacy()
        self.row_loss_aversion()
        self.row_hot_hand()
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until("a")
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until("b")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until("c")
        self.play(FadeIn(card.note))
        vo.wait_until("d")
        self.play(FadeIn(card.status, scale=1.3))

    def row_framing_disease(self):
        card = ledger_card(self._get("framing_disease"), width=12.8, font_size=24)
        with self.voiceover(
            'Six rows today. The first: described as lives saved, people choose the sure programme; described as '
            "deaths, the gamble. <bookmark mark='a'/> The original: Tversky and Kahneman, 1981. <bookmark "
            "mark='b'/> The record: Anton Kuhberger's meta-analysis in 1998, and the Many Labs project's "
            "thirty-six samples in 2014. <bookmark mark='c'/> One of the most reliable results in the field, "
            "though its size depends on the wording. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_anchoring(self):
        card = ledger_card(self._get("anchoring"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: an arbitrary number pulls an estimate toward it. <bookmark mark='a'/> The original: the "
            "wheel of fortune, 1974. <bookmark mark='b'/> The record: Karen Jacowitz and Kahneman in 1995, Many "
            'Labs in 2014, and Zacharias Maniadis, Fabio Tufano and John List, also in 2014, who found anchors '
            "from incidental numbers much weaker. <bookmark mark='c'/> Robust when the anchor is posed as a "
            "comparison; weaker when it's merely in the air. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_allais(self):
        card = ledger_card(self._get("allais"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: the Allais pattern. <bookmark mark='a'/> The original, as we saw it: Kahneman and "
            "Tversky, 1979, with seventy-two respondents. <bookmark mark='b'/> The record: Steffen Huck and "
            "Wieland Muller's large representative sample in 2012, and Kai Ruggeri and colleagues' replication of "
            "the 1979 problems in nineteen countries in 2020. <bookmark mark='c'/> Robust with large, "
            'hypothetical prizes, as in the original; weaker, and dependent on the design, with small real '
            "stakes. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_conjunction_fallacy(self):
        card = ledger_card(self._get("conjunction_fallacy"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: the conjunction fallacy. <bookmark mark='a'/> The original: Linda, 1983. <bookmark "
            "mark='b'/> The record: Klaus Fiedler's frequency version in 1988; Hertwig and Gigerenzer in 1999, "
            'who found that many people read probable as plausible; and an adversarial collaboration between '
            'Barbara Mellers, Hertwig and Kahneman in 2001, in which frequencies reduced the effect without '
            "removing it. <bookmark mark='c'/> The error replicates. What it means is still argued. <bookmark "
            "mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_loss_aversion(self):
        card = ledger_card(self._get("loss_aversion"), width=12.8, font_size=24)
        with self.voiceover(
            "The fifth: losses weigh about twice as much as gains. <bookmark mark='a'/> The original: prospect "
            "theory, 1979. <bookmark mark='b'/> The record: the coefficient of two point two five in 1992; "
            "Walasek and Stewart's ranges in 2015; David Gal and Derek Rucker's critique in 2018; a reply by "
            "Kellen Mrkva and colleagues in 2020, finding it robust and larger for larger stakes; and this part's "
            "own fit, one point one three on small stakes. <bookmark mark='c'/> Real for larger stakes; weak, "
            "absent or reversed at small ones and in some contexts. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_hot_hand(self):
        card = ledger_card(self._get("hot_hand"), width=12.8, font_size=24)
        with self.voiceover(
            "And the sixth: the hot-hand fallacy. <bookmark mark='a'/> The original: Gilovich, Vallone and "
            "Tversky, 1985. <bookmark mark='b'/> The record: Miller and Sanjurjo, 2018, who corrected the "
            "statistic and found a hot hand in the original data. <bookmark mark='c'/> The finding as taught was "
            'an artefact of the test; whether fans overestimate the hot hand is a separate question. <bookmark '
            "mark='d'/> Story and record."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 26 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 4, "contested": 1, "story and record": 1}
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=20, width=2.6)
            table.add(VGroup(chip, wrapped_label(f.title, 4.0, 22, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.3, 0.1, 0])
        rows_ = rows_of([
            (r"unlike much from its era, \ most of this replicates: \ framing, \ anchoring, \ Allais, \ Linda", GOOD),
            (r"what is contested is size and meaning: \ how much losses loom, \ and what the errors say about "
             r"rationality", LOSS),
            (r"and one textbook fallacy turned out to be the analysts'", HEUR),
        ], 5.6, 23, 0.36).move_to([3.6, 0.1, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> Unlike much of social psychology from the same decades, most of this "
            "replicates: framing, anchoring, the Allais pattern and Linda all come back, sample after sample. "
            "<bookmark mark='b'/> What's contested is size and meaning: how much losses really loom, and what the "
            "errors say about rationality. <bookmark mark='c'/> And one textbook fallacy turned out to be in the "
            "analysis, not the fans."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
