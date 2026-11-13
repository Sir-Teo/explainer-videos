from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_a_ledger()
        self.first_rows()

    def card(self):
        card = chapter_card(12, r"The Ledger opens", r"How do we know? \ And what happened when someone ran it again?",
                            lit=(2011, 2015), part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter twelve. The Ledger opens."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_a_ledger(self):
        rng = np.random.default_rng(11)
        A = axes([0, 10], [0, 10], x_length=6.6, y_length=3.7, center=[0, 1.0, 0])
        pts = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.075, color=P.HUMAN) for x, y in
                       zip(rng.uniform(0.6, 9.4, 26), rng.uniform(1.5, 8.5, 26))])
        hope = DashedLine(A.ax.c2p(0.5, 2.6), A.ax.c2p(9.5, 7.6), color=P.ACCENT, stroke_width=5)
        who = little_person(1.1, color=P.ACCENT)
        wish = label(r"the investigator wants a result", font_size=36, color=P.ACCENT)
        hoping = VGroup(who, wish).arrange(RIGHT, buff=0.4).next_to(A, DOWN, buff=0.5)
        ill = note(r"illustrative").next_to(A, UP, buff=0.1).align_to(A, RIGHT)
        # the anatomy of one row
        anatomy = VGroup()
        for t, sub, c in ((r"the claim", r"in one sentence", WHITE),
                          (r"the original study", r"who, when, how many, how big", P.ARCHIVE),
                          (r"run again", r"replications, meta-analyses", STATUS_COLOR["replicated"]),
                          (r"the verdict", r"with its date", P.ACCENT)):
            txt = VGroup(label(t, font_size=30, color=c), label(sub, font_size=21, color=GREY_A)).arrange(DOWN, buff=0.1)
            box = RoundedRectangle(width=3.32, height=1.25, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                   fill_color=CARD_FILL, fill_opacity=1)
            txt.move_to(box)
            anatomy.add(VGroup(box, txt))
        anatomy.arrange(RIGHT, buff=0.14).move_to([0, 0.3, 0])
        chips = VGroup()
        for status, meaning in ledger.STATUSES.items():
            chip = status_chip(status, 28)
            txt = label(meaning, font_size=26, color=GREY_A)
            chips.add(VGroup(chip, txt))
        cw = max(r[0].width for r in chips)
        for r in chips:
            r[0].move_to(ORIGIN, aligned_edge=LEFT)
            r[1].move_to([cw + 0.45, 0, 0], aligned_edge=LEFT)
        chips.arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        for r in chips:
            r[1].set_x(r[0].get_left()[0] + cw + 0.45 + r[1].width / 2)
        if chips.width > 13.2:
            chips.width = 13.2
        chips.move_to([0, -1.0, 0])
        head = heading(r"The Replication Ledger")
        with self.voiceover(
            "Kant's third objection, that the observer disturbs what's observed, has a modern form. The "
            "investigator wants a result. <bookmark mark='a'/> And a hundred and fifty years of psychology have "
            "shown how reliably people find what they hope to find, in a horse, in a patient, or in their own "
            "data. Part 4 tells that story. <bookmark mark='b'/> So this series keeps a ledger. Every finding we "
            "present gets a row: what was claimed, by whom, on how many people; and then what happened when "
            "someone ran it again. <bookmark mark='c'/> There are seven verdicts. Replicated. Replicated, but "
            "smaller. Contested. Failed. Never directly tested. Retracted. And one for the cases where the "
            "finding is sound, but the story the textbooks tell about the study is wrong."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.03), FadeIn(ill), FadeIn(hoping))
            vo.wait_until("a")
            self.play(Create(hope), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(A, pts, ill, hoping, hope)), FadeIn(head))
            self.play(LaggedStart(*[FadeIn(a_, shift=RIGHT * 0.15) for a_ in anatomy], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("c")
            self.play(anatomy.animate.scale(0.72).next_to(head, DOWN, buff=0.3))
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.15) for r in chips], lag_ratio=0.55), run_time=10.5)
        self.clear_scene()

    def first_rows(self):
        card = ledger_card(ledger.get("donders_insertion"), width=12.6, font_size=29)
        board = ledger_board(ledger.rows(part=1), font_size=30)
        with self.voiceover(
            "Here is a row in full. The claim: Donders' two differences are the durations of pure stages. "
            "<bookmark mark='a'/> The original study, a hollow marker: one subject, Donders himself. "
            "<bookmark mark='b'/> What happened next, in filled markers: Wundt's objection, and the notebook. "
            "<bookmark mark='c'/> The verdict: contested. <bookmark mark='d'/> And today's five rows together. "
            "The nerve signal has a finite speed: replicated, after a fifteen-year argument that ended by "
            "finding temperature. <bookmark mark='e'/> Mental operations take measurable time, simple faster "
            "than go/no-go, faster than choice: replicated, as often as almost anything in the field. "
            "<bookmark mark='f'/> Donders' reading of the differences as pure stages: contested. "
            "<bookmark mark='g'/> Hick's law, a preview of Part 25: replicated. <bookmark mark='h'/> And one "
            "more, which is the subject of the frontier chapter."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
            vo.wait_until("a")
            self.play(FadeIn(card.original, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=3.0)
            self.play(FadeIn(card.note))
            vo.wait_until("c")
            self.play(FadeIn(card.status, scale=1.3))
            vo.wait_until("d")
            self.play(FadeOut(card), FadeIn(board.head))
            for mark, row in zip("defgh", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(row, shift=RIGHT * 0.15))
        self.clear_scene()
