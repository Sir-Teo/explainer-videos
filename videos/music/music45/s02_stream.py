from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Stream(SoundScene):
    def construct(self):
        chapter(self, 1, r"Streaming", r"When does one line of notes become two?")
        self.hear()
        self.ambig()
        self.principles()
        self.animals()
        self.buildup()

    # ------------------------------------------------------------------
    def pattern(self, st, trt, n=3):
        g = VGroup()
        w = 0.3
        for c in range(n):
            for j, k in enumerate("ABA"):
                y = 0.0 if k == "A" else 0.09 * st
                g.add(Rectangle(width=w, height=0.16, stroke_width=0, fill_color=TUNE if k == "A" else BLUE, fill_opacity=1.0).move_to([(4 * c + j) * 0.42, y, 0]))
        return g

    def hear(self):
        d = load("aba")
        c = clip("aba.four")
        cells = VGroup()
        for case in d["cases"]:
            p = self.pattern(case["semitones"], case["trt"])
            verdict = r"model: \ two streams" if case["model_streams"] else r"model: \ one gallop"
            cells.add(VGroup(label(case["name"].replace(",", r", \ "), font_size=19, color=WHITE), p,
                             label(verdict, font_size=16, color=EAR if case["model_streams"] else TUNE)).arrange(DOWN, buff=0.25))
        cells.arrange_in_grid(rows=2, cols=2, buff=(1.4, 0.6)).move_to(DOWN * 0.1)
        head = label(r"A B A, \ rest, \ A B A, \ rest ...", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the classic stimulus, from Leon van Noorden's thesis of 1975. A tone A, a tone B, A again, then a "
            "rest, over and over. Hear four versions. B three semitones above A, slowly: one line that gallops. Twelve "
            "semitones, slowly. Six semitones, slowly. And six semitones, fast."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        names = [x["name"] for x in d["cases"]]
        with self.listen(c) as snd:
            window(snd, r"four triplets", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[n], end, buff=0.1)
        with self.voiceover(
            "With a small interval you hear a gallop, da-di-da, da-di-da. With a large one the gallop falls apart into two "
            "separate rhythms, the A tones twice as fast as the B tones, as if two players were tapping. And the same six "
            "semitones that gallop when slow split into two when fast. Whether a sequence is one line or two depends on both "
            "how far apart the notes are, and how quickly they come."
        ):
            self.play(*[Indicate(c_[2]) for c_ in cells])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def principles(self):
        items = [
            (r"proximity in pitch: \ near notes group; \ a leap invites a new stream", WHITE),
            (r"proximity in time: \ the faster the notes, \ the smaller the leap that splits them", WHITE),
            (r"similarity of timbre and loudness: \ like sounds group \ (chapter 3)", WHITE),
            (r"good continuation: \ a smooth path is followed across a gap \ (chapter 5)", TUNE),
            (r"Gestalt principles of vision, \ found again in hearing", GREY_A),
        ]
        rows_scene(self, r"principles of sequential grouping", items,
                   "Bregman organised the findings as principles of grouping. <bookmark mark='b'/> Proximity in pitch: near "
                   "notes group, and a leap invites a new stream. <bookmark mark='c'/> Proximity in time: the faster the notes, "
                   "the smaller the leap that splits them. <bookmark mark='d'/> Similarity of timbre and loudness: like sounds "
                   "group, chapter three's subject. <bookmark mark='e'/> Good continuation: a smooth path is followed across a "
                   "gap, chapter five's. <bookmark mark='f'/> These are the Gestalt principles of vision, found again in "
                   "hearing.", marks="bcdef")

    # ------------------------------------------------------------------
    def buildup(self):
        items = [
            (r"streaming takes time to build: \ a sequence often starts as one line and splits after a few seconds", WHITE),
            (r"Anstis and Saida \ (1985) \ and later studies measured the build-up; \ a change of ear or a pause resets it", WHITE),
            (r"between the boundaries, \ perception flips back and forth: \ the sequence is ambiguous", WHITE),
            (r"attention can hold one organisation, \ within limits", TUNE),
            (r"chapter 2: \ where exactly the boundaries lie, \ and a model of them", GREY_A),
        ]
        rows_scene(self, r"streaming builds up", items,
                   "Streaming also takes time. <bookmark mark='b'/> A sequence often starts as one line and splits after a few "
                   "seconds. <bookmark mark='c'/> Stuart Anstis and Shinsuke Saida measured this build-up in 1985, and a change "
                   "of ear or a pause resets it. <bookmark mark='d'/> Between the boundaries perception flips back and forth, "
                   "because the sequence is ambiguous, <bookmark mark='e'/> and attention can hold one organisation, within "
                   "limits. <bookmark mark='f'/> Chapter two asks where exactly the boundaries lie, and models them.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def ambig(self):
        d = load("ambig")
        c = clip("ambig.long")
        p = self.pattern(d["semitones"], d["trt"], n=4).move_to(UP * 0.6)
        q = VGroup(label(r"one gallop", font_size=24, color=TUNE), label(r"or", font_size=20, color=GREY_A), label(r"two streams?", font_size=24, color=EAR)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.2)
        head = label(rf"{d['semitones']:.0f} semitones, \ {1000 * d['trt']:.0f} ms: \ near the boundary", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now a case near the boundary: six semitones, ninety milliseconds apart, thirty times over. Listen for how it "
            "changes as it goes on."
        ):
            self.play(FadeIn(head), FadeIn(p), FadeIn(q))
        with self.listen(c) as snd:
            window(snd, r"thirty triplets", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            pulse(snd, q[0], 0.0, c.duration / 3, buff=0.12)
            pulse(snd, q[2], c.duration / 3, c.duration, buff=0.12)
        with self.voiceover(
            "Many listeners hear a gallop at first, and then, after a few seconds, two streams; some hear it flip back and "
            "forth. The sound never changed. That slow build-up, and the flipping, are the next thing to explain."
        ):
            self.play(Indicate(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def animals(self):
        items = [
            (r"streaming is not only human: \ starlings trained on ABA- patterns treat them as we do \ (MacDougall-Shackleton and colleagues, \ 1998)", WHITE),
            (r"goldfish, \ bats and monkeys show it too", WHITE),
            (r"a sensible design: \ in the wild, \ one source rarely jumps far in pitch from moment to moment", WHITE),
            (r"so a big, \ fast jump is good evidence of a second source", TUNE),
            (r"music borrows a mechanism built for finding animals and voices", GREY_A),
        ]
        rows_scene(self, r"not only human", items,
                   "Streaming is not only human. <bookmark mark='b'/> Starlings trained on these patterns treat them as we do, "
                   "Scott MacDougall-Shackleton and colleagues found in 1998, <bookmark mark='c'/> and goldfish, bats and monkeys "
                   "show it too. <bookmark mark='d'/> It is a sensible design: in the wild, one source rarely jumps far in pitch "
                   "from one moment to the next, <bookmark mark='e'/> so a big, fast jump is good evidence of a second source. "
                   "<bookmark mark='f'/> Music borrows a mechanism built for finding animals and voices.", marks="bcdef")
