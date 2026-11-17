from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403

ROWS = [
    ("default_enrolment",
     "Six new rows. The first: making enrolment in a retirement plan the default greatly increases participation. "
     "<bookmark mark='a'/> The original: Madrian and Shea, 2001. <bookmark mark='b'/> The record: more companies' "
     "switches, and a review placing defaults among the strongest tools in retirement policy. <bookmark mark='c'/> "
     "Defaults set how much people save as well as whether. <bookmark mark='d'/> Replicated."),
    ("energy_reports",
     "The second: comparing a household's energy use with its neighbours' reduces consumption. "
     "<bookmark mark='a'/> The original: Schultz and colleagues, 2007. <bookmark mark='b'/> The record: Allcott's "
     "trials across six hundred thousand homes, about two percent, partly persistent. <bookmark mark='c'/> Small per "
     "home, and cheap. <bookmark mark='d'/> Replicated."),
    ("nudge_size",
     "The third: nudges change behaviour by about as much as published studies report. <bookmark mark='a'/> The "
     "original: Mertens and colleagues' meta-analysis, 2022. <bookmark mark='b'/> The record: a bias-corrected "
     "reanalysis, and every trial of two nudge units, at about a sixth of the published size. <bookmark mark='c'/> "
     "Nudges work on average, by much less. <bookmark mark='d'/> Replicated, smaller."),
    ("signing_first",
     "The fourth: signing an honesty pledge at the top of a form reduces cheating. <bookmark mark='a'/> The original: "
     "Shu and colleagues, 2012. <bookmark mark='b'/> The record: a large replication finding nothing. "
     "<bookmark mark='c'/> Then the field data were shown to be fabricated. <bookmark mark='d'/> Retracted."),
    ("choice_overload",
     "The fifth: more options reduce choosing and satisfaction. <bookmark mark='a'/> The original: Iyengar and Lepper's "
     "jams, 2000. <bookmark mark='b'/> The record: a meta-analysis near zero, and another naming the conditions. "
     "<bookmark mark='c'/> A pattern under conditions, not a law. <bookmark mark='d'/> Contested."),
    ("accuracy_prompts",
     "And the sixth: prompting people to think about accuracy improves what they share. <bookmark mark='a'/> The "
     "original: Pennycook and colleagues, 2021. <bookmark mark='b'/> The record: a smaller replication, and a "
     "meta-analysis with a small, reliable effect. <bookmark mark='c'/> Real, and not transformative. "
     "<bookmark mark='d'/> Replicated, smaller."),
]


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        for key, text in ROWS:
            self.row(key, text)
        self.tally()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What does this part add?", lit=(), part=PART, scale=("society",),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _get(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def row(self, key, text):
        card = ledger_card(self._get(key), width=12.8, font_size=21)
        with self.voiceover(text) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        assert len(rows) == 6
        head = heading(r"What the six have in common")
        items = rows_of([
            (r"the structural changes, \ defaults and reports sent to everyone, \ replicate", GOOD),
            (r"the clever one-line effects shrink, \ depend on conditions, \ or were never there", AUTH),
            (r"the gap between journals and practice is a filter (chapter five), \ and in one case fraud", MODEL),
            (r"a small change in how a choice is presented can move millions, \ by a little, \ unless it changes "
             r"what happens when nobody chooses", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the six have in common. <bookmark mark='a'/> The structural changes, defaults and reports sent to "
            "everyone, replicate. <bookmark mark='b'/> The clever one-line effects shrink, depend on conditions, or "
            "were never there. <bookmark mark='c'/> The gap between journals and practice is a filter, and in one case "
            "fraud. <bookmark mark='d'/> So here's the answer to this part's question. A small change in how a choice "
            "is presented can move millions of people, by a little, unless it changes what happens when nobody "
            "chooses."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
