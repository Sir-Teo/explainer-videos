from __future__ import annotations

from videos.psychology.psych12.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.criterion()
        self.prevalence()
        self.zroc()

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

    def criterion(self):
        card = ledger_card(self._row("criterion_shift"), width=12.8, font_size=26)
        with self.voiceover(
            "Three rows today. The first is the foundation. The claim: changing the payoffs or the base rate moves "
            "where an observer says yes, while its sensitivity stays the same. <bookmark mark='a'/> The original: "
            "Tanner and Swets, 1954, with a faint spot of light and trained observers. <bookmark mark='b'/> The "
            "record: Swets, Tanner and Birdsall in 1961, who found that payoffs, probabilities and confidence "
            "ratings all trace one ROC, and Green and Swets's book of 1966, gathering laboratories across vision "
            "and hearing. <bookmark mark='c'/> It holds wherever it's been tested, with one qualification: people "
            "move their criterion in the right direction, but usually not as far as an ideal observer would. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.2)
        self.clear_scene()

    def prevalence(self):
        card = ledger_card(self._row("prevalence_effect"), width=12.8, font_size=26)
        with self.voiceover(
            "The second. The claim: when targets are rare, searchers miss more of them. <bookmark mark='a'/> The "
            "original: Wolfe, Horowitz and Kenner, 2005, with misses rising from eleven to fifty-two percent. "
            "<bookmark mark='b'/> The record: the effect repeats, and Fleck and Mitroff showed in 2007 that letting "
            "people correct a hasty answer removes much of it. <bookmark mark='c'/> So rare targets really are missed "
            "more; why is argued, among criterion, early quitting and speed. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.2)
        self.clear_scene()

    def zroc(self):
        card = ledger_card(self._row("zroc_slope"), width=12.8, font_size=26)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "The third. The claim: in recognition memory, the z ROC's slope is below one, about point eight. "
            "<bookmark mark='a'/> The original: Ratcliff, Sheu and Gronlund, 1992. <bookmark mark='b'/> The record: "
            "the slope repeats, and Yonelinas showed in 1994 that a recollection-plus-familiarity mixture also "
            "produces it. <bookmark mark='c'/> The slope is solid; its meaning is not settled. "
            f"<bookmark mark='d'/> Replicated. <bookmark mark='e'/> That makes {total} rows. Three today, all "
            "replicated, and each with an argument still running about what it means. Detection theory is very good "
            "at measuring. It's more modest about explaining."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
