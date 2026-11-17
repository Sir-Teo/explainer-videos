from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403

ROWS = [
    ("interleaving",
     "Five new rows; testing and spacing are Part 21's. The first: mixing problem types during practice improves "
     "later performance, though blocked practice looks better during learning. <bookmark mark='a'/> The original: "
     "Rohrer and Taylor, 2007. <bookmark mark='b'/> The record: a classroom trial in mathematics, and a meta-analysis "
     "finding the benefit largest for confusable categories. <bookmark mark='c'/> It works by making the learner "
     "choose the method. <bookmark mark='d'/> Replicated."),
    ("learning_styles",
     "The second: teaching matched to a learner's preferred style improves learning. <bookmark mark='a'/> The "
     "original: the Dunns' model for teachers, 1978. <bookmark mark='b'/> The record: Pashler and colleagues' review "
     "of crossover tests, and a direct test finding no interaction. <bookmark mark='c'/> Preferences are real; "
     "matching to them doesn't help. <bookmark mark='d'/> Failed."),
    ("two_sigma",
     "The third: one-to-one tutoring raises achievement by about two standard deviations. <bookmark mark='a'/> The "
     "original: Bloom, 1984. <bookmark mark='b'/> The record: VanLehn's review at about zero point eight, and "
     "randomized school trials at about zero point four. <bookmark mark='c'/> Still among the largest effects in "
     "education. <bookmark mark='d'/> Replicated, smaller."),
    ("growth_mindset",
     "The fourth: teaching students that ability can grow improves achievement. <bookmark mark='a'/> The original: "
     "Blackwell, Trzesniewski and Dweck, 2007. <bookmark mark='b'/> The record: a meta-analysis at about zero point "
     "zero eight, and a national trial with effects for lower achievers in supportive schools. <bookmark mark='c'/> "
     "Small, cheap and heterogeneous. <bookmark mark='d'/> Replicated, smaller."),
    ("longhand_notes",
     "And the fifth: students who take notes by hand learn more than those who type. <bookmark mark='a'/> The "
     "original: Mueller and Oppenheimer, 2014. <bookmark mark='b'/> The record: a preregistered replication and a "
     "multi-site study, neither finding a reliable advantage. <bookmark mark='c'/> Typists transcribe more; whether "
     "that costs learning isn't established. <bookmark mark='d'/> Contested."),
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
        assert len(rows) == 5
        head = heading(r"What the five have in common")
        items = rows_of([
            (r"the techniques built on memory research, \ interleaving like testing and spacing, \ hold up", GOOD),
            (r"the popular ideas, \ styles and the pen, \ fail or wobble; \ the famous numbers, \ two sigma and "
             r"mindset, \ shrink", AUTH),
            (r"learners' own judgements point the wrong way: \ fluency feels like learning", MODEL),
            (r"the most effective way to learn feels harder, \ and that is why learners choose the opposite", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "What the five have in common. <bookmark mark='a'/> The techniques built on memory research, interleaving "
            "like testing and spacing, hold up. <bookmark mark='b'/> The popular ideas, learning styles and the pen, "
            "fail or wobble, and the famous numbers, two sigma and mindset, shrink. <bookmark mark='c'/> Learners' own "
            "judgements point the wrong way, because fluency feels like learning. <bookmark mark='d'/> So here's the "
            "answer to this part's question. The most effective way to learn feels harder, and that's why learners "
            "choose the opposite."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", items):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
