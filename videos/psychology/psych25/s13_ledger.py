from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.row_fitts()
        self.row_bound()
        self.row_errors()
        self.row_lip()
        self.row_stop()
        self.tally()

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

    def row_fitts(self):
        card = ledger_card(self._row("fitts_law"), width=12.8, font_size=24)
        with self.voiceover(
            "Five rows today; Hick's law already has its row, from Part 1. The first: the time of an aimed movement grows with the logarithm of twice the distance over the "
            "width. <bookmark mark='a'/> The original: Fitts, 1954, with the tapping plates. <bookmark mark='b'/> "
            "The record: Fitts and Peterson's single movements in 1964, and decades of pointing studies with hands, "
            "feet, mice and fingers, summarized by Scott MacKenzie and colleagues. <bookmark mark='c'/> One of the "
            "most reliable laws in psychology, and an international standard for testing pointing devices. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_bound(self):
        card = ledger_card(self._row("speed_bound"), width=12.8, font_size=24)
        with self.voiceover(
            "The second: instructions to be fast or accurate act on the diffusion model's bound. "
            "<bookmark mark='a'/> The original: Ratcliff and Rouder, 1998. <bookmark mark='b'/> The record: Voss "
            "and colleagues' four manipulations in 2004, Wagenmakers and colleagues' seventeen people in 2008, "
            "refitted in this part, and Rae and colleagues in 2014, who found the drift moving too. "
            "<bookmark mark='c'/> The bound moves every time; it isn't the only thing that moves. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_errors(self):
        card = ledger_card(self._row("fast_slow_errors"), width=12.8, font_size=24)
        with self.voiceover(
            "The third: errors are faster than correct answers when speed is stressed, and slower when accuracy is. "
            "<bookmark mark='a'/> The original: Ratcliff and Rouder, 1998. <bookmark mark='b'/> The record: the "
            "seventeen people refitted in this part, thirteen with fast errors under speed and fourteen with slow "
            "errors under accuracy, and Ratcliff and McKoon's review of two-choice tasks in 2008. "
            "<bookmark mark='c'/> A regular pattern that four numbers can't produce, and the full model can. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_lip(self):
        card = ledger_card(self._row("lip_ramping"), width=12.8, font_size=24)
        with self.voiceover(
            "The fourth: single neurons in LIP accumulate evidence, ramping to a bound. <bookmark mark='a'/> The "
            "original: Roitman and Shadlen, 2002. <bookmark mark='b'/> The record: Latimer and colleagues' steps in "
            "2015, Shadlen and colleagues' reply in 2016, and Steinemann and colleagues' population recordings in "
            "2024. <bookmark mark='c'/> The population looks like diffusion; whether single neurons ramp or step is "
            "unsettled. <bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def row_stop(self):
        card = ledger_card(self._row("stop_race"), width=12.8, font_size=24)
        with self.voiceover(
            "And the fifth: stopping is a race between independent go and stop processes, from which the stop time "
            "can be read. <bookmark mark='a'/> The original: Logan and Cowan, 1984. <bookmark mark='b'/> The "
            "record: Verbruggen and colleagues' consensus guide in 2019, and Bissett and colleagues in 2021, who "
            "found independence badly violated at short delays. <bookmark mark='c'/> The race predicts the "
            "inhibition function well; its central assumption fails where the delays are short. "
            "<bookmark mark='d'/> Contested."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def tally(self):
        rows = ledger.rows(part=PART)
        head = heading(r"Part 25 in the Ledger")
        counts = {}
        for f in rows:
            counts[f.status] = counts.get(f.status, 0) + 1
        assert counts == {"replicated": 3, "contested": 2}
        table = VGroup()
        for f in rows:
            chip = word_chip(f.status, color=STATUS_COLOR[f.status], font_size=20, width=2.3)
            table.add(VGroup(chip, wrapped_label(f.title, 4.2, 22, WHITE)).arrange(RIGHT, buff=0.3))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-3.4, 0.2, 0])
        rows_ = rows_of([
            (r"the laws of choice and movement time hold, \ seventy years on", MODEL),
            (r"the model's parameters mostly mean what they claim, \ and the exceptions are measured", BOUND),
            (r"what is contested lies where models meet neurons and assumptions meet data: \ steps or ramps, \ "
             r"independent or not", LOST),
        ], 5.6, 23, 0.36).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The tally. <bookmark mark='a'/> Three rows replicated: the old laws of choice and movement time hold, "
            "seventy years on. <bookmark mark='b'/> The diffusion model's parameters mostly mean what they claim, "
            "and where they don't, the exceptions have been measured. <bookmark mark='c'/> What's contested lies "
            "where models meet neurons, and where assumptions meet data: whether single neurons ramp or step, and "
            "whether going and stopping really race independently."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in table], lag_ratio=0.3))
            for m, r in zip("abc", rows_):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
