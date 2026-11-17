from __future__ import annotations

from videos.psychology.psych10.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.rem()
        self.loss()
        self.memory()
        self.mortality()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter twelve. The Ledger."
        ):
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
        if len(card.record):
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def rem(self):
        card = ledger_card(self._row("rem_sleep"), width=12.8, font_size=27)
        with self.voiceover(
            "Four rows today. The first. The claim: sleep contains recurring periods of rapid eye "
            "movement, and people woken from them usually report a dream. <bookmark mark='a'/> The "
            "original: Aserinsky and Kleitman, 1953. Twenty detailed dreams, from twenty-seven "
            "awakenings. <bookmark mark='b'/> The record: sleep laboratories ever since, on thousands of "
            "recorded nights, have found the same stages, in cycles of about ninety minutes. "
            "<bookmark mark='c'/> One part didn't hold: that dreaming happens only in REM sleep. Dreams "
            "are reported from the other stages too, less often and less vividly. <bookmark mark='d'/> "
            "Replicated."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def loss(self):
        card = ledger_card(self._row("sleep_loss_vigilance"), width=12.8, font_size=27)
        with self.voiceover(
            "The second. The claim: too little sleep, night after night, impairs sustained attention, "
            "and the impairment accumulates. <bookmark mark='a'/> The original: Van Dongen and "
            "colleagues, 2003. Eight, six or four hours in bed for two weeks, assigned by lot. "
            "<bookmark mark='b'/> The record: in the same year an army laboratory gave people three, "
            "five, seven or nine hours in bed for a week, and found the same graded decline. "
            "<bookmark mark='c'/> And the note that matters: people rated themselves only slightly "
            "sleepy, while their performance kept falling. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def memory(self):
        card = ledger_card(self._row("sleep_memory"), width=12.8, font_size=27)
        with self.voiceover(
            "The third. The claim: reactivating a memory during slow-wave sleep strengthens it. "
            "<bookmark mark='a'/> The original: Rasch and colleagues, 2007, with the smell of roses. "
            "<bookmark mark='b'/> The record: ninety-one experiments, pooled in 2020. A small effect in "
            "non-REM sleep, and none in REM sleep or in waking. <bookmark mark='c'/> So it's there, and "
            "it's small. And for a neighbouring method, the reported effects have been shrinking. "
            "<bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def mortality(self):
        card = ledger_card(self._row("short_sleep_mortality"), width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "And the fourth, which is here because you've read it in headlines. The claim: sleeping too "
            "little shortens your life. <bookmark mark='a'/> The evidence: sixteen studies, pooled in "
            "2010. One point four million people reported their usual sleep and were followed for "
            "years. Short sleepers were twelve percent more likely to die during the follow-up. But look "
            "at the other half of that line. Long sleepers were thirty percent more likely to die. If "
            "lost sleep were the cause, why would extra sleep be worse? <bookmark mark='c'/> Because "
            "this is Part 2's problem. Nobody assigned these people their sleep. Illness changes sleep "
            "years before it kills, and the sleep was reported by the sleepers. The association is "
            "real. The causal reading isn't established. <bookmark mark='d'/> Contested. "
            f"<bookmark mark='e'/> That makes {total} rows. And notice what separates the second row "
            "from the fourth. One assigned sleep by lot, to a small group, for two weeks. The other "
            "observed more than a million people, for years. The small experiment is the one you can "
            "believe."
        ) as vo:
            self._show(card, vo, marks="aacd")
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
