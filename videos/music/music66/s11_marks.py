from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Marks(SoundScene):
    def construct(self):
        chapter(self, 10, r"Watermarks and detection", r"Can generated sound carry a label that cannot be heard?")
        self.idea()
        self.quiz()
        self.table()
        self.detection()

    # ------------------------------------------------------------------
    def idea(self):
        lines = VGroup(
            label(r"a key seeds a pseudo-random sequence of $\pm 1$, \ filtered to 1 to 6 kHz", font_size=20, color=WHITE),
            label(r"add it, \ far below the music: \ 35 dB down", font_size=20, color=WHITE),
            MathTex(r"z = \frac{\sum_n \operatorname{sign}(y_n)\, p_n}{\sqrt{\sum_n p_n^2}}", font_size=38, color=TUNE),
            label(r"to detect: \ correlate with the key's sequence, \ and compare with 30 keys never used: \ by chance about $0 \pm 1$; \ with the mark, \ large", font_size=19, color=WHITE),
            label(r"spread spectrum, \ as in Part 58's era of audio watermarks; \ AudioSeal \ (2024) \ learns its marks", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"a spread-spectrum mark", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A generator can label what it makes. <bookmark mark='a'/> A secret key seeds a random sequence of plus and minus "
            "ones, filtered to the middle of the spectrum. <bookmark mark='b'/> Add it far below the music, thirty-five "
            "decibels down. <bookmark mark='c'/> To detect it, correlate the audio with the key's sequence. <bookmark mark='d'/> "
            "Compare the score with what thirty keys never used give, and by chance it is about nought, give or take one; with "
            "the mark, large. <bookmark mark='e'/> This is spread "
            "spectrum, the method of the first audio watermarks; newer ones, like AudioSeal in 2024, learn their marks with a "
            "network."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("watermark")
        c = clip("watermark.two")
        card = listen_card(r"A bowed phrase, \ twice. \ One carries a watermark 35 dB below the music. \ Which?", width=8.8)
        with self.voiceover("Your turn. A bowed phrase, twice. One carries the watermark, thirty-five decibels below the music. Which one?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"marked, \ or not?", kind="synthesized", detail=r"Part 9's string", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        z = d["rows"]["-35"]["marked"]
        res = label(rf"the first: \ its detection score is {z:.0f}; \ the second's, \ {d['clean']:.1f}", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(f"The first carried it. To the detector the difference is plain: a score of {say(round(z))} against {say(d['clean'], 1)}. To the ear, at thirty-five decibels down under a bowed string, it may be hard to hear; this demonstration does not measure audibility thresholds."):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("watermark")
        rows = d["rows"]
        g = VGroup()
        for k, name in (("marked", r"as marked"), ("coded", r"through Part 58's coder at 64 kbit/s"), ("shifted", r"moved 37 samples at 16 kHz (2.3 ms)"),
                        ("shifted_search", r"moved, \ detector searching shifts"), ("room", r"played in a room \ (searching shifts)"),
                        ("other_key", r"checked with ten wrong keys \ (the largest)")):
            g.add(VGroup(label(name, font_size=18, color=WHITE), label(f"{rows['-25'][k]:.1f}", font_size=18, color=TUNE), label(f"{rows['-35'][k]:.1f}", font_size=18, color=EAR)))
        g.add(VGroup(label(r"no mark at all", font_size=18, color=GREY_B), label(f"{d['clean']:.1f}", font_size=18, color=GREY_B), label(f"{d['clean']:.1f}", font_size=18, color=GREY_B)))
        g.arrange(DOWN, buff=0.28)
        for r in g:
            for i, x in enumerate((-3.0, 2.4, 4.6)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.3)
        top = VGroup(label(r"25 dB down", font_size=15, color=TUNE).move_to([2.4, g.get_top()[1] + 0.45, 0]), label(r"35 dB down", font_size=15, color=EAR).move_to([4.6, g.get_top()[1] + 0.45, 0]))
        note = label(r"standardized detector scores; \ threshold 5 is illustrative, \ not a calibrated false-alarm guarantee", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"what the mark survives", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        r35 = rows["-35"]
        with self.voiceover(
            f"What does it survive? <bookmark mark='a'/> A perceptual coder: through Part 58's coder at sixty-four kilobits, the "
            f"score at thirty-five decibels down is {say(r35['coded'], 1)}. <bookmark mark='b'/> A shift of thirty-seven "
            f"samples at sixteen kilohertz, about two point three milliseconds, sharply reduces the unaligned score, {say(r35['shifted'], 1)}, unless the detector searches over shifts, "
            f"{say(r35['shifted_search'], 1)}. Played in a room, {say(r35['room'], 1)}: the echoes smear it. Checked with ten wrong "
            f"keys, the largest score is {say(r35['other_key'], 1)} and the average {say(r35['other_key_mean'], 1)}: chance, "
            "with occasional high values. A threshold of five is an illustrative choice here, not a calibrated operational false-alarm guarantee. Real marks must also "
            "survive speed changes, re-recording through a room, and people trying to remove them, and the arms race is open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(note), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[2:]], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def detection(self):
        items = [
            (r"a mark only labels what its maker chose to mark; \ open models can be run without one", WHITE),
            (r"detectors trained to tell generated from recorded sound find artifacts of today's codecs and vocoders", WHITE),
            (r"they are horses in the sense of Part 63: \ a new generator, \ or one re-encoded, \ can fool them", WHITE),
            (r"provenance from the other side: \ signing recordings at capture, \ as some cameras now do \ (C2PA)", TUNE),
        ]
        rows_scene(self, r"detection", items,
                   "Marks have limits. <bookmark mark='b'/> A mark only labels what its maker chose to mark, and open models can be "
                   "run without one. <bookmark mark='c'/> Detectors trained to tell generated from recorded sound find the artifacts "
                   "of today's codecs and vocoders. <bookmark mark='d'/> They are horses in the sense of Part 63: a new generator, "
                   "or a generated file re-encoded, can fool them. <bookmark mark='e'/> So provenance is also being built from the "
                   "other side: signing recordings when they are made, as some cameras now do under the C2PA standard.",
                   marks="bcde")
