from __future__ import annotations

from videos.psychology.psych8.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.n400()
        self.training()
        self.lies()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("brain", "mind"), marr=("what",))
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

    def n400(self):
        card = ledger_card(self._row("n400"), width=12.8, font_size=27)
        with self.voiceover(
            "Three rows today. The first. The claim: a word that doesn't fit the meaning of its sentence is "
            "followed, about four hundred milliseconds later, by a negative brain potential. "
            "<bookmark mark='a'/> The original: Kutas and Hillyard, 1980. <bookmark mark='b'/> The record: "
            "three decades of studies, reviewed by Kutas and Federmeier in 2011. It appears in reading, in "
            "listening, in sign language, and with pictures, and it grows as the word gets less expected. "
            "<bookmark mark='c'/> It's one of the most repeated effects in the whole field. What it "
            "measures is still argued: surprise, or the work of fitting a meaning in. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(0.5)
        self.clear_scene()

    def training(self):
        card = ledger_card(self._row("brain_training"), width=12.8, font_size=27)
        with self.voiceover(
            "The second. The claim: practising brain-training games improves abilities you didn't "
            "practise. <bookmark mark='a'/> One origin: Jaeggi and colleagues, 2008, who trained students "
            "on a memory task and reported gains on a test of reasoning. <bookmark mark='b'/> The record. "
            "In 2010 Adrian Owen and the BBC ran the experiment on eleven thousand four hundred and thirty "
            "people for six weeks. They got better at every game they practised, and no better at anything "
            "else. In 2016 a review went through the hundred and thirty-two papers the industry cites, and "
            "found little evidence of broad transfer. <bookmark mark='c'/> People improve at what they "
            "practise. What fails is the claim that it carries over to memory, attention or intelligence "
            "in general. <bookmark mark='d'/> Failed."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def lies(self):
        card = ledger_card(self._row("fmri_lie_detection"), width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "And the third. The claim: a brain scan can tell whether a particular person is lying. "
            "<bookmark mark='a'/> The original: Kozel and colleagues, 2005. Volunteers were told to lie "
            "about a mock theft, and most were classified correctly from their scans. <bookmark mark='b'/> "
            "The record: Ganis and colleagues, 2011. The same kind of test caught every liar. Then the "
            "volunteers were taught a trick, a tiny movement of a finger or toe at chosen moments, and it "
            "caught one in three. <bookmark mark='c'/> It's never been tested where it would be used: on "
            "people with something to lose, who don't want to be read. An American court excluded it in "
            "2010, and the appeal court agreed. <bookmark mark='d'/> Not directly tested. "
            f"<bookmark mark='e'/> That makes {total} rows. Look at the three. The one that stands is a "
            "measurement, repeated in a great many laboratories. The two that don't were products."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
