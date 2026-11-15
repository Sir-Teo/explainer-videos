from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403


class Score(SoundScene):
    def construct(self):
        chapter(self, 9, r"From notes to a score", r"How do performed seconds become written beats?")
        self.gap()
        self.quantize()
        self.heard()
        self.key()
        self.rest()

    # ------------------------------------------------------------------
    def gap(self):
        items = [
            (r"a transcriber reports notes in seconds; \ a score is written in beats", WHITE),
            (r"players stretch and squeeze time: \ rubato, \ held phrase ends, \ a slower start", WHITE),
            (r"so: \ find the tempo, \ snap each onset to the nearest fraction of a beat, \ and read off the durations", WHITE),
            (r"then everything else a score needs: \ meter and barlines, \ key and spelling, \ voices and staves", TUNE),
        ]
        rows_scene(self, r"seconds are not beats", items,
                   "A list of notes is not yet a score. <bookmark mark='b'/> A transcriber reports notes in seconds; a score is "
                   "written in beats. <bookmark mark='c'/> And players stretch and squeeze time: rubato, held phrase ends, a slower "
                   "start. <bookmark mark='d'/> So the next step is to find the tempo, snap each onset to the nearest fraction of a "
                   "beat, and read off the durations. <bookmark mark='e'/> Then come the rest of a score's decisions: meter and "
                   "barlines, key and spelling, voices and staves.", marks="bcde")

    # ------------------------------------------------------------------
    def quantize(self):
        d = load("score")
        est = d["est"]
        q = d["beats"]
        tb = d["true_beats"]
        n = min(len(est), len(q))
        top = max(n_[1] for n_ in est) + 0.6
        ax1 = frame_axes(width=11.0, height=0.6, xlo=0, xhi=top, ylo=0, yhi=1, center=UP * 1.3)
        ax2 = frame_axes(width=11.0, height=0.6, xlo=0, xhi=max(q) + 2, ylo=0, yhi=1, center=DOWN * 0.9)
        d1 = VGroup(*[Dot(ax1.to(e[1], 0.5), radius=0.07, color=BLUE) for e in est])
        d2 = VGroup(*[Dot(ax2.to(b, 0.5), radius=0.07, color=TUNE if i < len(tb) and abs(b - tb[i]) < 1e-6 else EAR) for i, b in enumerate(q[:n])])
        links = VGroup(*[Line(ax1.to(est[i][1], 0.5), ax2.to(q[i], 0.5), stroke_width=1, color=GREY_D) for i in range(n)])
        grid = VGroup(*[Line(ax2.to(b, 0), ax2.to(b, 1), stroke_width=1, color=GREY_D) for b in range(int(max(q)) + 2)])
        l1 = label(r"onsets as performed \ (seconds)", font_size=16, color=BLUE).next_to(ax1, UP, buff=0.1).align_to(ax1, LEFT)
        l2 = label(r"onsets as written \ (beats)", font_size=16, color=TUNE).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)
        ok = sum(1 for i in range(min(n, len(tb))) if abs(q[i] - tb[i]) < 1e-6)
        note = label(rf"tempo found: \ {60 * d['bps']:.0f} beats a minute; \ {ok} of {len(tb)} onsets on the beat the Tune is written on", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"quantization", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the Tune's opening played with rubato, transcribed by the network. <bookmark mark='a'/> Its onsets, in "
            "seconds, drift: a slower start, a held phrase end. <bookmark mark='b'/> Monochord's quantizer tries every tempo and "
            "phase, snaps each onset to the nearest half beat, and keeps the tempo with the smallest error. "
            f"<bookmark mark='c'/> It finds {say(60 * d['bps'])} beats a minute, and {say(ok)} of the {say(len(tb))} onsets land "
            "on the beat where the Tune is written."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax1), FadeIn(d1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(ax2), FadeIn(grid), FadeIn(l2), Create(links), FadeIn(d2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("score")
        c = clip("score.two")
        boxes = choice_boxes([r"the performance", r"the quantized score, \ played"], width=3.8, height=0.9, buff=1.0, size=20).move_to(UP * 0.5)
        note = label(r"the score keeps the notes and the beats, \ and loses the rubato: \ a score is a plan, \ not a performance", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"performance and score", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the performance, then the quantized score played strictly."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"played, \ then written", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["performance"], st["score"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["score"], c.duration, buff=0.08)
        with self.voiceover("The score keeps the notes and the beats, and loses the rubato, as it should: a score is a plan for a performance, not a performance."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def key(self):
        d = load("score")
        rows_ = VGroup(*[VGroup(label(k, font_size=24, color=TUNE if i == 0 else WHITE), label(f"r = {r:.2f}", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.6)
                         for i, (k, r) in enumerate(zip(d["key"], d["key_r"]))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 2.5 + DOWN * 0.2)
        side = VGroup(
            label(r"Krumhansl and Schmuckler's key finder \ (Part 15), \ on the transcribed notes and their quantized durations", font_size=17, color=WHITE),
            label(r"the key decides the spelling: \ in C major, \ the note between F and G is F$\sharp$, \ not G$\flat$", font_size=17, color=WHITE),
            label(r"and the key signature, \ and which notes need accidentals", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.8 + DOWN * 0.2)
        head = label(r"key and spelling", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Next, the key. <bookmark mark='a'/> Part 15's key finder, run on the transcribed notes weighted by their quantized "
            f"durations, ranks {d['key'][0]} first, ahead of {d['key'][1]} and {d['key'][2]}. <bookmark mark='b'/> The key decides "
            "the spelling: in C major the note between F and G is written F sharp, not G flat. And it decides the key signature, "
            "and which notes need accidentals."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows_), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rest(self):
        items = [
            (r"meter: \ where the barlines go, \ from accents and harmony \ (Part 62's beat trackers)", WHITE),
            (r"key and spelling: \ is it G$\sharp$ or A$\flat$? \ the key finder of Part 15 decides", WHITE),
            (r"voices and staves: \ which notes belong to which hand, \ which line", WHITE),
            (r"tuplets, \ grace notes, \ ties across barlines: \ each a decision a musician makes without noticing", WHITE),
            (r"a readable score is the last and least solved step", TUNE),
        ]
        rows_scene(self, r"the rest of a score", items,
                   "Everything else a score needs is a further decision. <bookmark mark='b'/> Meter: where the barlines go, from "
                   "accents and harmony, which Part 62's beat trackers take up. <bookmark mark='c'/> Key and spelling: is a note G "
                   "sharp or A flat? The key finder of Part 15 decides. <bookmark mark='d'/> Voices and staves: which notes belong "
                   "to which hand, and which line. <bookmark mark='e'/> Tuplets, grace notes, ties across barlines: each a decision a "
                   "musician makes without noticing. <bookmark mark='f'/> A readable score is the last and least solved step.",
                   marks="bcdef")
