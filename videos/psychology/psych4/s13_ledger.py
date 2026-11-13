from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403


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
        f = ledger.get("precognition")
        g = archive.BEM_2011.data["galak"]
        card = ledger_card(f, width=12.8, font_size=27)
        with self.voiceover(
            "The Ledger has been open since Part 1. Today you know why the series keeps it. Six rows, and the "
            "first is the one the part began with. The claim: people's responses are influenced by events that "
            "haven't happened yet. <bookmark mark='a'/> The original: Bem, 2011, nine experiments and more than "
            "a thousand participants. <bookmark mark='b'/> What happened next. Three preregistered attempts to "
            "repeat the recall experiment found nothing. Then seven more experiments, on more than three "
            f"thousand people, found nothing, and when every attempt was pooled the effect was {g['meta_d']:.2f}. "
            "<bookmark mark='c'/> The note matters more than the verdict. The methods were the field's ordinary "
            "methods. That's why the result counted: it showed what those methods could produce. "
            "<bookmark mark='d'/> Failed."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(card.note))
            vo.wait_until("d")
            self.play(FadeIn(card.status, scale=1.3))
        self.clear_scene()

    def rows(self):
        board = ledger_board(ledger.rows(part=PART), font_size=28)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "And the six together. <bookmark mark='a'/> Feeling the future: failed. <bookmark mark='b'/> "
            "Published studies are underpowered: replicated, and it's a finding about psychology itself, sixty "
            "years old. <bookmark mark='c'/> Published effects shrink when repeated: replicated, three times "
            "over. <bookmark mark='d'/> The flag: failed. <bookmark mark='e'/> The banknote: failed. "
            "<bookmark mark='f'/> Imagined contact: contested. <bookmark mark='g'/> "
            f"That makes {total} rows. From here on, every part ends this way. When the series shows you a "
            "finding, the Ledger says what became of it, with the sources, and the date somebody last checked. "
            "And when the record changes, the row changes."
        ) as vo:
            self.play(FadeIn(board.head))
            for mark, row in zip("abcdef", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(row, shift=RIGHT * 0.15))
            vo.wait_until("g")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
