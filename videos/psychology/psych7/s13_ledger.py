from __future__ import annotations

from videos.psychology.psych7.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.gage()
        self.broca()
        self.taxi()
        self.types()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("brain",), marr=("tissue",))
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

    def gage(self):
        card = ledger_card(self._row("gage"), width=12.8, font_size=27)
        with self.voiceover(
            "Four rows today. The first. The claim: damage to the frontal lobes turned a careful, capable "
            "man into an impulsive and unreliable one. <bookmark mark='a'/> The original: Harlow, 1868, one "
            "patient, written up by his doctor twenty years after the accident. <bookmark mark='b'/> The "
            "record: Malcolm Macmillan's history of the case, which went back to every surviving document. "
            "The evidence for a change of character is a few sentences, and afterwards the man held a "
            "demanding job for years. <bookmark mark='c'/> He survived, and something changed. How much, "
            "for how long, and whether he recovered aren't in the record. <bookmark mark='d'/> Story and "
            "record. The frontal lobes do matter for planning and restraint. Later patients, properly "
            "tested, show it. This case can't."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def broca(self):
        card = ledger_card(self._row("broca_area"), width=12.8, font_size=27)
        with self.voiceover(
            "The second. The claim: damage low in the left frontal lobe, toward the back, takes away fluent "
            "speech and spares understanding. <bookmark mark='a'/> The original: Broca, 1861, the patient "
            "who could say one syllable, and then more patients like him. <bookmark mark='b'/> The record. "
            "Broca kept the brains, and in 2007 Nina Dronkers and her colleagues put two of them in a "
            "scanner. The damage ran far beyond the area that carries his name, into deep tissue and one of "
            "the long cables. <bookmark mark='c'/> So the claim holds, and the map was drawn too small. The "
            "lasting loss of speech needs more damage than the textbook's patch. <bookmark mark='d'/> "
            "Replicated, with that refinement."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def taxi(self):
        card = ledger_card(self._row("taxi_hippocampus"), width=12.8, font_size=27)
        with self.voiceover(
            "The third. The claim: years of finding your way around London enlarge the back of the "
            "hippocampus. <bookmark mark='a'/> The original: Maguire and colleagues, 2000, sixteen drivers "
            "against matched controls. <bookmark mark='b'/> The record: Woollett and Maguire, 2011, who "
            "followed trainees through the training. Growth in those who qualified, none in those who "
            "failed or never trained. <bookmark mark='c'/> The first study couldn't say which came first. "
            "The second could. It's one laboratory and one skill. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def types(self):
        card = ledger_card(self._row("brain_types"), width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "And the fourth. The claim: people differ in which hemisphere dominates, and that makes them "
            "logical or creative. <bookmark mark='a'/> The original isn't a study. It's an extrapolation "
            "from the split-brain patients, and by 1973 a magazine headline could say we are left-brained "
            "or right-brained. <bookmark mark='b'/> The record: Nielsen and colleagues, 2013, a thousand "
            "and eleven people. Each connection leans one way or the other, and the leanings don't go "
            "together across a person's brain. <bookmark mark='c'/> The hemispheres do differ in what they "
            "do. What fails is the claim that a person is one or the other. <bookmark mark='d'/> Failed. "
            f"<bookmark mark='e'/> That makes {total} rows. Look at today's four together. The two that "
            "stood up were tested twice, by different methods. The two that didn't each began as a good "
            "story about one case, or a handful."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
