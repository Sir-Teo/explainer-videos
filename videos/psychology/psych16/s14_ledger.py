from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.blocking()
        self.taste()
        self.tolerance()
        self.albert()
        self.matching()
        self.renewal()

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

    def blocking(self):
        card = ledger_card(self._row("blocking"), width=12.8, font_size=25)
        with self.voiceover(
            "Six rows today. The first: a cue paired with an outcome that another cue already predicts acquires "
            "little or no association. <bookmark mark='a'/> The original: Kamin, 1969, with rats. "
            "<bookmark mark='b'/> The record: blocking has been reported in many species and procedures since. But in "
            "2016 Tom Beckers's group published fifteen careful experiments, in people and in rodents, using "
            "procedures like or identical to published ones, and found no blocking in any of them. "
            "<bookmark mark='c'/> Critics answered that most used cues of the same sense, which theory says should "
            "weaken blocking. Either way, it's weaker and less dependable than the textbooks imply. "
            "<bookmark mark='d'/> Replicated, smaller."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def taste(self):
        card = ledger_card(self._row("taste_aversion"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: rats readily learn to avoid a taste followed by illness, even hours later, and a light or "
            "sound followed by shock, but not the reverse pairings. <bookmark mark='a'/> The original: Garcia and "
            "Koelling, 1966. <bookmark mark='b'/> The record: Domjan and Wilson, in 1972, found the same selectivity "
            "with the cues delivered the same way, answering the objection that taste and light differed in timing, "
            "and taste aversions have been found in many species, including people. <bookmark mark='c'/> It's among "
            "the most robust findings in learning. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tolerance(self):
        card = ledger_card(self._row("conditioned_tolerance"), width=12.8, font_size=25)
        with self.voiceover(
            "The third is a row Part 10 promised: tolerance to a drug is partly a conditioned response to the cues that "
            "come with it, so the same dose is more dangerous somewhere new. <bookmark mark='a'/> The original: Shepard "
            "Siegel and colleagues, 1982. Rats given heroin in one room were then given a large dose. A third died in "
            "the usual room, two thirds in a new one. <bookmark mark='b'/> The record: repeated with many drugs and "
            "species, reviewed by Siegel and Ramos in 2002. <bookmark mark='c'/> In people the evidence comes from "
            "survivors' reports and studies of reactions to drug cues: consistent, but observational. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def albert(self):
        card = ledger_card(self._row("little_albert"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: an infant was conditioned to fear a white rat, the fear spread to furry things, and it showed "
            "how phobias are learned. <bookmark mark='a'/> The original: Watson and Rayner, 1920: one infant, seven "
            "pairings. <bookmark mark='b'/> The record: Harris, in 1979, on how the story grew in the retelling; "
            "Powell and colleagues, in 2014, on whether we even know who Albert was. <bookmark mark='c'/> One child, "
            "unblinded notes, no removal of the fear: a demonstration, and an ethical lesson, not evidence. "
            "<bookmark mark='d'/> Story and record."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def matching(self):
        card = ledger_card(self._row("matching_law"), width=12.8, font_size=25)
        with self.voiceover(
            "The fifth: given two sources of reward, animals divide their responses in proportion to the rewards "
            "each provides. <bookmark mark='a'/> The original: Herrnstein, 1961, with pigeons. "
            "<bookmark mark='b'/> The record: Baum's 1979 survey of a hundred and three data sets from twenty-three "
            "studies: matching on average, with undermatching common. <bookmark mark='c'/> It holds across species, "
            "people included, and across kinds of reward, as a description of choice between interval schedules. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def renewal(self):
        card = ledger_card(self._row("renewal"), width=12.8, font_size=25)
        with self.voiceover(
            "The sixth: a fear extinguished in one context returns when the cue is met in the context where the fear "
            "was learned. <bookmark mark='a'/> The original: Bouton and Bolles, 1979. <bookmark mark='b'/> The record: "
            "reviewed by Vervliet, Craske and Hermans in 2013, renewal has been found across species, including human "
            "fear conditioning and patients after exposure therapy. <bookmark mark='c'/> Extinction adds learning "
            "tied to its context; it doesn't erase the first. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
