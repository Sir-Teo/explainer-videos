from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.dopamine()
        self.twostep()
        self.latent()
        self.grid()

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

    def dopamine(self):
        card = ledger_card(self._row("dopamine_rpe"), width=12.8, font_size=25)
        with self.voiceover(
            "Four rows today. The first: midbrain dopamine neurons signal reward prediction errors. "
            "<bookmark mark='a'/> The original: Schultz, Dayan and Montague, 1997, drawing on Schultz's recordings in "
            "monkeys. <bookmark mark='b'/> The record: the error signature has been found across species and methods, "
            "and in 2013 Steinberg and colleagues showed that an artificial error, made with light, teaches like a "
            "real one. <bookmark mark='c'/> The core finding is among the best replicated in neuroscience. What else "
            "dopamine signals, ramps, movement and salience, is argued. <bookmark mark='d'/> Replicated, with its scope "
            "contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def twostep(self):
        card = ledger_card(self._row("two_step"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: in the two-step task, people's choices show both model-free and model-based signatures. "
            "<bookmark mark='a'/> The original: Daw and colleagues, 2011, seventeen people. <bookmark mark='b'/> The "
            "record: the pattern has been found in thousands of people since, online and in the laboratory; but Feher "
            "da Silva and Hare, in 2020, found that with careful instructions people look almost entirely "
            "model-based. <bookmark mark='c'/> The pattern replicates. Whether it measures two systems, or partly "
            "misunderstanding, is contested. <bookmark mark='d'/> Replicated; the reading contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def latent(self):
        card = ledger_card(self._row("latent_learning"), width=12.8, font_size=25)
        with self.voiceover(
            "The third: rats explore a maze without reward and learn its layout, showing it as soon as a reward "
            "appears. <bookmark mark='a'/> The original: Tolman and Honzik, 1930. <bookmark mark='b'/> The record: "
            "reviewed by Thistlethwaite in 1951, latent learning was found in most of the many experiments that "
            "looked, with failures in some designs. <bookmark mark='c'/> The effect is robust where the animal can "
            "explore freely; the theoretical war it started is over, and maps won. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def grid(self):
        card = ledger_card(self._row("grid_cells"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: cells in the entorhinal cortex fire on a triangular grid as an animal moves through space. "
            "<bookmark mark='a'/> The original: Hafting, Fyhn, Molden and the Mosers, 2005, in rats. "
            "<bookmark mark='b'/> The record: found in mice, bats and monkeys, and as grid-like signals in human "
            "imaging, beginning with Doeller, Barry and Burgess in 2010. <bookmark mark='c'/> The cells are as solid "
            "as anything in neuroscience; what grid-like signals mean in human thought is newer. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
