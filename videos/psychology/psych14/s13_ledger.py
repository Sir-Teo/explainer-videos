from __future__ import annotations

from videos.psychology.psych14.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.cues()
        self.speed()
        self.culture()
        self.faces()

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

    def cues(self):
        card = ledger_card(self._row("cue_combination"), width=12.8, font_size=25)
        with self.voiceover(
            "Four rows today. The first: when two senses report the same property, people combine them roughly as an "
            "optimal observer would, each cue weighted by its reliability, and the combination less variable than "
            "either alone. <bookmark mark='a'/> The original: Ernst and Banks, 2002, with four observers. "
            "<bookmark mark='b'/> The record: Alais and Burr's ventriloquist in 2004, and many other pairs of cues "
            "since; and Rahnev and Denison's review of 2018, which lists the departures. <bookmark mark='c'/> The note: "
            "reliability weighting has been found again and again, but it isn't universal. Children come to it late, "
            "and the review lists many conditions where people fall short of the optimal weights. "
            "<bookmark mark='d'/> For the claim as stated, roughly optimal: replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def speed(self):
        card = ledger_card(self._row("contrast_speed"), width=12.8, font_size=25)
        with self.voiceover(
            "The second: a moving pattern of low contrast looks slower than the same pattern at high contrast. "
            "<bookmark mark='a'/> The original: Thompson, 1982. <bookmark mark='b'/> The record: Weiss, Simoncelli "
            "and Adelson's model in 2002 predicted it, along with several other illusions of motion, and it's been "
            "measured in many laboratories. <bookmark mark='c'/> The qualification: it holds for slow and moderate "
            "speeds. At high temporal frequencies the results are mixed, and some studies find low contrast speeds "
            "things up, which a single slow prior doesn't predict. <bookmark mark='d'/> Replicated, within that range."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def culture(self):
        card = ledger_card(self._row("muller_lyer_culture"), width=12.8, font_size=25)
        with self.voiceover(
            "The third: the Müller-Lyer illusion is much weaker in people who grow up without rectangular buildings. "
            "<bookmark mark='a'/> The original: Segall, Campbell and Herskovits, 1966. <bookmark mark='b'/> The "
            "record: in 2015, children who gained their sight after cataract surgery saw the illusion at once; and in "
            "2025, Amir and Firestone's review argued that the original differences may come from method, and noted "
            "that many animals see the illusion. <bookmark mark='c'/> The illusion is real; nobody doubts that. "
            "Whether its size depends on a carpentered world is now disputed, and the original study hasn't been "
            "repeated with modern methods. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def faces(self):
        card = ledger_card(self._row("face_area"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth: a region of the fusiform gyrus responds much more to faces than to other objects, in most "
            "people tested. <bookmark mark='a'/> The original: Kanwisher, McDermott and Chun, 1997, in twelve of "
            "fifteen people. <bookmark mark='b'/> The record includes Gauthier's greebles in 1999, and the region has "
            "been found in study after study since; it's now routinely located in a few minutes of scanning. "
            "<bookmark mark='c'/> The note keeps the dispute: what the region is selective for, faces as such or any "
            "category a person is expert at. <bookmark mark='d'/> For the claim as stated: replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()
