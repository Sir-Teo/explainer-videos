from __future__ import annotations

from videos.psychology.psych5.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_row()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's finding was checked?", lit=(), part=PART,
                            scale=("neuron",), marr=("how",))
        with self.voiceover(
            "Chapter twelve. The Ledger."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_row(self):
        rows = ledger.rows(part=PART)
        f = rows[0]
        c = load("cable")
        card = ledger_card(f, width=12.8, font_size=27)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One row today, and it's a different kind of row from Part 4's. The claim: sodium and potassium "
            "conductances that depend on voltage, measured under the voltage clamp, account for the nerve "
            "signal and its speed. <bookmark mark='a'/> The original: Hodgkin and Huxley, 1952, on squid giant "
            f"axons, with a computed speed of {c['published']} metres a second against {c['observed']} "
            "measured. <bookmark mark='b'/> What happened next. The equations have been integrated countless "
            f"times since; in this series, Psyche gets {c['velocity']:.1f}. <bookmark mark='c'/> And the note. "
            "The membrane's conductance had been shown to rise during the signal before the model existed, "
            "and the gates the model had to invent were later found, as proteins. It is a model of one "
            "membrane, and other cells need other channels. <bookmark mark='d'/> Replicated. Set this row "
            "beside the ones from Part 4 and you can see what made the difference. The claim was a number. "
            "The number was computed before it was compared. And the parts were measured separately from the "
            f"thing they were asked to explain. <bookmark mark='e'/> That makes {total} rows."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
