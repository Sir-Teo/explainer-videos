from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


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
        f = ledger.get("telling_more")
        card = ledger_card(f, width=12.8, font_size=28)
        with self.voiceover(
            "Three rows today. One of them carries a limit that matters as much as the finding, so let's read it "
            "in full. The claim: people's reports of why they acted are often inferences, and not observations "
            "of what moved them. <bookmark mark='a'/> The original is Nisbett and Wilson's review, in 1977. "
            "<bookmark mark='b'/> What happened next: for a long time, argument. Then choice blindness gave the "
            "claim a direct test, because once the outcome of a choice has been swapped, a report can be checked "
            "against what the person really chose. <bookmark mark='c'/> And the note. The finding is about "
            "reports of causes. It doesn't show that people can't tell you what they see, or feel, or intend, "
            "and how far it reaches is still argued. <bookmark mark='d'/> So the verdict is replicated, and the "
            "limit goes on the card with it. A verdict without its limit would be a jingle of its own: one word "
            "covering two very different claims."
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
        board = ledger_board(ledger.rows(part=PART), font_size=30)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=1.25)
        later = label(r"waiting for their parts: \ grit beyond conscientiousness (Part 28); \ the reliability "
                      r"paradox (Part 59)", font_size=24, color=GREY_B).next_to(tally, DOWN, buff=0.2)
        with self.voiceover(
            "And the three together. <bookmark mark='a'/> A general description feels personal: replicated, "
            "again and again since 1949. <bookmark mark='b'/> Telling more than we can know: replicated, for "
            "reports of causes. <bookmark mark='c'/> Choice blindness: replicated, with faces, and then with jam "
            f"and tea. <bookmark mark='d'/> That makes {total} rows in the Ledger. Two of today's findings have "
            "no row yet. Whether grit adds anything to conscientiousness is entered with motivation, in Part 28. "
            "And the reliability paradox gets its row in Part 59, where it's put to work. The Ledger records "
            "which findings are waiting, so that they can't quietly go missing."
        ) as vo:
            self.play(FadeIn(board.head))
            for mark, row in zip("abc", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(row, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(tally, shift=UP * 0.15))
            self.play(FadeIn(later))
        self.clear_scene()
