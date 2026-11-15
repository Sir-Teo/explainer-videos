from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"A twelve-note chord, \ struck four times, \ twice over. \ Once every note starts together; \ once the notes "
                           r"arrive as MIDI 1.0 sends them, \ one after another down a cable. \ Which was the cable?", width=10.2)
        with self.voiceover(
            "A question for your ears. A twelve-note chord, struck four times, twice over. Once, every note starts together. "
            "Once, the notes arrive as MIDI sends them, one after another down a cable. Which was the cable?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one chord, \ twice over", kind="physical model", detail=r"Karplus--Strong strings", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        arr = np.array(d["arrivals_ms"])
        ax = frame_axes(width=10.0, height=3.2, xlo=0, xhi=9, ylo=0, yhi=13, center=DOWN * 0.4)
        bars = VGroup()
        for j, (k, a) in enumerate(zip(d["keys"], arr)):
            bars.add(VGroup(Line(ax.to(0, j + 1), ax.to(a, j + 1), color=GREY_D, stroke_width=1.5), Dot(ax.to(a, j + 1), radius=0.07, color=EAR)))
        xt = VGroup(*[label(f"{v} ms", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 2, 4, 6, 8)])
        yl = label(r"the twelve notes, \ bottom to top", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.2).rotate(PI / 2)
        note = label(rf"the last note arrives {d['spread_ms']:.1f} ms after the first: \ 320 microseconds a byte, \ two or three bytes a note", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the first was the cable", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The first was the cable. <bookmark mark='a'/> MIDI sends one byte every three hundred and twenty microseconds, and "
            "each note takes two or three bytes, so the twelve notes arrive one after another, the last "
            f"{say(d['spread_ms'], 1)} milliseconds after the first. That is too short to hear as an arpeggio; it is heard, if "
            "at all, as a softer, slightly smeared attack. Forty years of music have been played down this cable, and this is "
            "almost the worst it does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.12), FadeIn(note), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1981: \ Dave Smith of Sequential Circuits proposes a universal interface between synthesizers", WHITE),
            (r"Roland's Ikutaro Kakehashi and the Japanese makers join: \ rivals agree on a five-pin cable and a few pages of rules", WHITE),
            (r"January 1983, \ a trade show: \ a Prophet-600 and a Jupiter-6 are joined, \ and a key on one sounds the other", WHITE),
            (r"MIDI 1.0 \ (1983) \ is still spoken by nearly every electronic instrument; \ Smith and Kakehashi shared a Grammy for it \ (2013)", TUNE),
            (r"this part reads it byte by byte, \ then builds what sits on top", GREY_A),
        ]
        rows_scene(self, r"a five-pin cable", items,
                   "The cable has a story. <bookmark mark='b'/> In 1981 Dave Smith of Sequential Circuits proposed a universal "
                   "interface between synthesizers. <bookmark mark='c'/> Roland's Ikutaro Kakehashi and the Japanese makers joined, "
                   "and rivals agreed on a five-pin cable and a few pages of rules. <bookmark mark='d'/> In January 1983, at a trade "
                   "show, a Prophet-600 and a Jupiter-6 were joined, and a key pressed on one sounded the other. "
                   "<bookmark mark='e'/> MIDI 1.0 is still spoken by nearly every electronic instrument, and in 2013 Smith and "
                   "Kakehashi shared a technical Grammy for it. <bookmark mark='f'/> This part reads it byte by byte, then builds "
                   "what sits on top.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"machines that play: \ cylinders, \ rolls and Nancarrow",
            r"MUSIC N and the unit generator",
            r"MIDI byte by byte, \ its limits, \ MPE, \ MIDI 2.0 and files",
            r"sequencers, \ trackers and a small pattern language",
            r"the audio callback, \ its deadline and its timing",
            r"the processing graph, \ plug-ins and delay compensation",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Machines that play: cylinders, rolls and Nancarrow. <bookmark mark='b'/> MUSIC N and the unit "
            "generator. <bookmark mark='c'/> MIDI byte by byte, its limits, MPE, MIDI 2.0 and files. <bookmark mark='d'/> "
            "Sequencers, trackers and a small pattern language. <bookmark mark='e'/> The audio callback, its deadline and its "
            "timing. <bookmark mark='f'/> And the processing graph, plug-ins and delay compensation."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
