from __future__ import annotations

from videos.psychology.psych11.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.weber()
        self.stevens()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
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
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def weber(self):
        card = ledger_card(self._row("weber_law"), width=12.8, font_size=27)
        with self.voiceover(
            "Two rows today. The first. The claim: the smallest noticeable change in a stimulus is a "
            "constant fraction of its size. <bookmark mark='a'/> The original: Weber, 1834, with weights, "
            "touch and the length of lines. <bookmark mark='b'/> The record: Fechner's ten years of "
            "experiments, and a century and a half of laboratories since, among them the near miss for "
            "the loudness of tones in 1968. <bookmark mark='c'/> It holds over the middle of most ranges "
            "and fails at the edges: near the absolute threshold the fraction grows, and for loud tones "
            "it shrinks a little. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def stevens(self):
        card = ledger_card(self._row("stevens_power_law"), width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "The second. The claim: judged magnitude grows as a power of stimulus intensity. "
            "<bookmark mark='a'/> The original: Stevens, 1957, and a table of exponents from a third to "
            "three and a half. <bookmark mark='b'/> The record: the power form repeats, continuum after "
            "continuum. But Poulton's review in 1968 showed that the exponents move with the range of "
            "stimuli, the first one shown and the order. <bookmark mark='c'/> So the exponents are not "
            "constants of the senses. <bookmark mark='d'/> Replicated, for the power form. "
            f"<bookmark mark='e'/> That makes {total} rows. Both of today's are replicated, and both come "
            "with conditions attached. That's what a mature finding looks like: not a slogan, but a law "
            "with its range of validity written beside it."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
