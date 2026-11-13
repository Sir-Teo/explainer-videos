from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_row()
        self.rows()

    def card(self):
        card = chapter_card(12, r"The Ledger", r"What happened when today's findings were run again?", lit=(),
                            part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter twelve. The Ledger."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_row(self):
        f = ledger.get("bright_rats")
        card = ledger_card(f, width=12.8, font_size=28)
        with self.voiceover(
            "Five rows today, and one of them needs care, so let's read it in full. The claim: rats labelled "
            "bright at random learn faster, because of what their experimenters expect. <bookmark mark='a'/> "
            "The original study: twelve students, sixty rats. <bookmark mark='b'/> What happened next: the same "
            "laboratory repeated it with a different apparatus, and reported the same result. "
            "<bookmark mark='c'/> And that's all we've been able to find. One small study, with one-tailed "
            "tests, confirmed by its own authors. <bookmark mark='d'/> So the verdict is: not directly tested. "
            "That's not the same as wrong. The broader point, that a handler's belief reaches an animal, is "
            "well supported, by Pfungst and by the dogs. But this famous experiment is quoted far more "
            "confidently than its record allows, and the Ledger exists to say so."
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
        self.clear_scene()

    def rows(self):
        board = ledger_board(ledger.rows(part=2), font_size=30)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "And the five together. <bookmark mark='a'/> An animal reads its handler: replicated, from a horse "
            "in 1904 to police dogs in 2011. <bookmark mark='b'/> The bright rats: not directly tested. "
            "<bookmark mark='c'/> Teachers' expectations raise IQ: replicated, but smaller, and only while the "
            "teacher has nothing else to go on. <bookmark mark='d'/> Subjects do what they think is wanted: "
            "replicated, and when it was finally measured, modest. <bookmark mark='e'/> And people can't be "
            "random: replicated for seventy years, which is why the shuffling is done by cards. "
            f"<bookmark mark='f'/> That makes {total} rows in the Ledger. Notice that two of today's five are not "
            "simply replicated. That's roughly the proportion to expect for the rest of the series."
        ) as vo:
            self.play(FadeIn(board.head))
            for mark, row in zip("abcde", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(row, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
