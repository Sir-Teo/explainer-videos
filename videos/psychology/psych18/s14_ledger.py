from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.latent()
        self.stroop()
        self.blindness()
        self.cueing()
        self.blink()
        self.media()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
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

    def latent(self):
        card = ledger_card(self._row("latent_inhibition"), width=12.8, font_size=25)
        with self.voiceover(
            "Six rows today, and the first was promised in Part 16: a stimulus presented many times without "
            "consequence is later learned about more slowly. <bookmark mark='a'/> The original: Lubow and Moore, "
            "1959, with sheep and goats. <bookmark mark='b'/> The record: Robert Lubow's 1989 review gathered "
            "decades of studies. The effect is robust in animals and in young children; in adults it usually appears "
            "only when a distracting task keeps them from noticing the pre-exposed stimulus. "
            "<bookmark mark='c'/> Whether it lowers attention to the cue, or only how the learning shows, is argued. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def stroop(self):
        card = ledger_card(self._row("stroop"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: naming the ink of a colour word is slower when the word names another "
            "colour. <bookmark mark='a'/> The original: Stroop, 1935, with cards of a hundred items. "
            "<bookmark mark='b'/> The record: by 1991 MacLeod could review more than seven hundred studies, and the "
            "effect appeared in every variant. <bookmark mark='c'/> It's so reliable that online studies use it to "
            "check that participants are paying attention. What it measures is the argued part. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def blindness(self):
        card = ledger_card(self._row("inattentional_blindness"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: people busy with a demanding task often miss an unexpected, plainly visible object. "
            "<bookmark mark='a'/> The original: Simons and Chabris, 1999, one hundred and ninety-two observers, "
            "forty-six percent of whom missed the visitor. <bookmark mark='b'/> The record: Most and colleagues "
            "showed in 2001 that what you attend decides what else you see, and in 2013 twenty of twenty-four "
            "radiologists missed a gorilla in a lung scan. <bookmark mark='c'/> The effect replicates widely; its "
            "size depends on load, similarity and what people are asked. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def cueing(self):
        card = ledger_card(self._row("posner_cueing"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: a cue to a location speeds responses there and slows them elsewhere, without moving the "
            "eyes. <bookmark mark='a'/> The original: Posner, 1980. <bookmark mark='b'/> The record: Posner and Cohen "
            "added inhibition of return in 1984, and the cueing effects have been reproduced in essentially every "
            "laboratory that has run them. <bookmark mark='c'/> Small effects, tens of milliseconds, but very "
            "reliable. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def blink(self):
        card = ledger_card(self._row("attentional_blink"), width=12.8, font_size=25)
        with self.voiceover(
            "The fifth: a second target in a rapid stream is often missed two to five hundred milliseconds after "
            "the first. <bookmark mark='a'/> The original: Raymond, Shapiro and Arnell, 1992. "
            "<bookmark mark='b'/> The record: Paul Dux and René Marois reviewed hundreds of studies in 2009, with "
            "letters, words, faces and sounds; the blink and its lag-one sparing appear almost everywhere. "
            "<bookmark mark='c'/> Why it happens is still argued. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def media(self):
        card = ledger_card(self._row("media_multitasking"), width=12.8, font_size=25)
        with self.voiceover(
            "The sixth: heavy media multitaskers are worse at filtering distraction. <bookmark mark='a'/> The "
            "original: Ophir, Nass and Wagner, 2009, a small sample with a large effect. <bookmark mark='b'/> The "
            "record: two careful replications found the effect in five of fourteen tests, and a meta-analysis put "
            "it near zero once small-study bias was accounted for. <bookmark mark='c'/> At most a small "
            "association, with no evidence about cause. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
