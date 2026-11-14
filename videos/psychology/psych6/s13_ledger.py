from __future__ import annotations

from videos.psychology.psych6.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.ltp()
        self.inhibition()
        self.grid()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("neuron", "circuit"), marr=("how",))
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

    def ltp(self):
        f = self._row("ltp")
        card = ledger_card(f, width=12.8, font_size=27)
        with self.voiceover(
            "Three rows today. The first. The claim: a brief burst of strong activity leaves a synapse "
            "stronger for a long time. <bookmark mark='a'/> The original: Bliss and Lømo, 1973, in the "
            "hippocampus of anaesthetized rabbits. <bookmark mark='b'/> What happened next: it has been "
            "produced again and again, in many preparations, and Bi and Poo, in 1998, tied it to the timing "
            "of single spikes. <bookmark mark='c'/> The note matters. That synapses can be strengthened by use isn't in "
            "doubt. Whether that's how your memories are stored is a different claim, and it gets its own "
            "hearing in Part 20. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def inhibition(self):
        f = self._row("lateral_inhibition")
        card = ledger_card(f, width=12.8, font_size=27)
        with self.voiceover(
            "The second. The claim: neighbouring receptors in an eye inhibit one another, in proportion to "
            "how active each one is. <bookmark mark='a'/> The original: Hartline and Ratliff, 1957, recording "
            "from single fibres of the horseshoe crab's optic nerve. <bookmark mark='b'/> A year later they "
            "showed that the inhibition from several neighbours simply adds. <bookmark mark='c'/> These are "
            "the equations of one animal's eye, measured unit by unit, and they predict the bands Mach "
            "described a century before. <bookmark mark='d'/> Replicated. Like the row from Part 5, it's a "
            "claim stated as an equation, on parts that could be measured separately."
        ) as vo:
            self._show(card, vo)
        self.clear_scene()

    def grid(self):
        f = self._row("hermann_grid")
        card = ledger_card(f, width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "And the third, which uses the second. The claim: the grey spots of the Hermann grid are produced "
            "by centre-surround receptive fields. <bookmark mark='a'/> The original: Baumgartner's argument "
            "of 1960, repeated in textbooks ever since. <bookmark mark='b'/> The record: Geier and "
            "colleagues, 2008. Curve the streets, leave everything the account depends on in place, and the "
            "spots vanish. <bookmark mark='c'/> So the textbook explanation predicts spots where nobody sees "
            "them. Lateral inhibition is real. This famous application of it is at best incomplete, and what "
            "does cause the spots is still disputed. <bookmark mark='d'/> The status is one we've used "
            "before: story and record. The story is a tidy mechanism. The record says it fails a test it "
            f"should have passed. <bookmark mark='e'/> That makes {total} rows. And notice the pattern in "
            "today's three. The mechanisms stood up. The step from a mechanism to an experience is where "
            "it went wrong."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
