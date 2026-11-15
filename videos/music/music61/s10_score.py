from __future__ import annotations

import numpy as np

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
        perf = d["perf"]
        tb = d["true_beats"]
        fx, tr = d["fixed"], d["track"]
        top = max(p[1] for p in perf) + 0.6
        ax0 = frame_axes(width=11.0, height=0.5, xlo=0, xhi=top, ylo=0, yhi=1, center=UP * 1.9)
        d0 = VGroup(*[Dot(ax0.to(p[1], 0.5), radius=0.07, color=BLUE) for p in perf])
        l0 = label(r"onsets as performed \ (seconds)", font_size=15, color=BLUE).next_to(ax0, UP, buff=0.08).align_to(ax0, LEFT)

        def row(q, center, title):
            ax = frame_axes(width=11.0, height=0.5, xlo=0, xhi=max(max(q), max(tb)) + 1, ylo=0, yhi=1, center=center)
            grid = VGroup(*[Line(ax.to(b_, 0), ax.to(b_, 1), stroke_width=1, color=GREY_D) for b_ in range(int(max(max(q), max(tb))) + 2)])
            dots = VGroup(*[Dot(ax.to(b_, 0.5), radius=0.07, color=TUNE if i < len(tb) and abs(b_ - tb[i]) < 1e-6 else EAR) for i, b_ in enumerate(q)])
            lab = label(title, font_size=15, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
            return VGroup(ax, grid, dots, lab)
        r1 = row(fx["beats"], UP * 0.3, rf"one fixed tempo \ ({60 * fx['bps']:.0f} a minute): \ {fx['ok']} of {len(tb)} onsets on the written beat")
        r2 = row(tr["beats"], DOWN * 1.3, rf"a tempo that may drift: \ {tr['ok']} of {len(tb)}")
        note = label(r"gold: \ on the beat the Tune is written on; \ red: \ not", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"quantization", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the Tune's opening played with rubato: a slower middle, a held phrase end. To study quantization alone, "
            "give the quantizer its onsets exactly, as a perfect transcriber would. <bookmark mark='a'/> In seconds, they "
            "drift. <bookmark mark='b'/> The simplest quantizer tries every fixed tempo and phase and snaps each onset to "
            f"the nearest half beat. It settles on {say(round(60 * fx['bps']))} beats a minute, and only {say(fx['ok'])} of the "
            f"{say(len(tb))} onsets land where the Tune is written: one tempo cannot fit a performance whose tempo moves. "
            "<bookmark mark='c'/> So let the tempo drift, a little from note to note, and prefer simple note values; find "
            f"the likeliest values and tempos together by dynamic programming. Now {say(tr['ok'])} of {say(len(tb))} land "
            "on their beats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(ax0), FadeIn(d0), FadeIn(l0))
            vo.wait_until("b")
            self.play(FadeIn(r1), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(r2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()
        tempo = np.array(tr["tempo"]) * 60
        ax = frame_axes(width=9.0, height=3.0, xlo=0, xhi=len(tempo) - 1, ylo=90, yhi=150, center=DOWN * 0.3)
        cv = curve(np.arange(len(tempo)), tempo, ax.to, color=TUNE, width=3)
        dots = VGroup(*[Dot(ax.to(i, v), radius=0.06, color=TUNE) for i, v in enumerate(tempo)])
        ref = DashedLine(ax.to(0, 120), ax.to(len(tempo) - 1, 120), color=GREY_B, stroke_width=1.5)
        ticks = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.12) for v in (90, 120, 150)])
        xl = label(r"note", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"tempo found \ (beats a minute)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        head = label(r"the rubato, \ recovered", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"And the tempos it chose are the rubato itself: slowing to {say(round(tempo.min()))} beats a minute through the "
            f"first phrase and pressing on to {say(round(tempo.max()))} in the second, around the 120 at which the Tune is "
            "written. A score and a tempo curve together describe the performance; the score alone is the plan. Cemgil and "
            "Kappen built quantizers like this in 2003; Part 62's beat tracker does the same job from audio."
        ):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ref), FadeIn(ticks), FadeIn(xl), FadeIn(yl), Create(cv), FadeIn(dots), run_time=1.6)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("score")
        c = clip("score.two")
        boxes = choice_boxes([r"the performance", r"the quantized score, \ played"], width=3.8, height=0.9, buff=1.0, size=20).move_to(UP * 0.5)
        note = label(r"the score keeps the notes and the beats, \ and loses the rubato: \ a score is a plan, \ not a performance", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"performance and score", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the performance, then the score the drifting-tempo quantizer wrote, played strictly at 120."):
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
