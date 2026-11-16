from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403


class Transcode(SoundScene):
    def construct(self):
        chapter(self, 9, r"Generations", r"What happens when a compressed file is compressed again?")
        self.why()
        self.table()
        self.heard()
        self.practice()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a decoded file is not the original: \ it carries the first coder's noise, \ shaped to the first coder's masks", WHITE),
            (r"a second coder computes its own masks from that signal, \ and adds its own noise on top", WHITE),
            (r"the first noise is now part of the `music', \ to be coded faithfully, \ at the expense of the music itself", WHITE),
            (r"and frames that do not line up put new pre-echo where the old was hidden", TUNE),
        ]
        rows_scene(self, r"transcoding", items,
                   "Files are often compressed more than once: downloaded, edited, uploaded, streamed. <bookmark mark='b'/> A decoded "
                   "file is not the original; it carries the first coder's noise, shaped to the first coder's masks. "
                   "<bookmark mark='c'/> A second coder computes its own masks from that signal, and adds its own noise on top. "
                   "<bookmark mark='d'/> Worse, the first noise is now part of the music, to be coded as faithfully as the music "
                   "itself, with bits the music needed. <bookmark mark='e'/> And frames that do not line up put new errors where the "
                   "old ones were hidden.", marks="bcde")

    # ------------------------------------------------------------------
    def table(self):
        d = load("transcode")
        rows = VGroup(VGroup(label(r"generation", font_size=17, color=GREY_A), label(r"signal-to-noise ratio against the original", font_size=17, color=GREY_A)))
        for g in d["gens"]:
            col = TUNE if g["generation"] == 1 else (EAR if g["generation"] == 5 else WHITE)
            rows.add(VGroup(label(str(g["generation"]), font_size=19, color=col), label(f"{g['snr']:.1f} dB", font_size=19, color=col)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].set_x(-2.6)
            r[1].set_x(1.6)
        rows.move_to(UP * 0.1)
        note = label(rf"our mix through our coder at {d['kbps']} kbit/s, \ decoded and re-encoded, \ five times", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"five generations", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is our mix through our coder at {say(d['kbps'])} kilobits, decoded and re-encoded five times. "
            "<bookmark mark='a'/> The signal-to-noise ratio against the original falls from "
            f"{say(d['gens'][0]['snr'], 1)} decibels after one generation to about two by the fourth and fifth: the noise is "
            "now nearly as strong as the music, and much of it is no longer under any mask."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=1.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("transcode")
        c = clip("transcode.two")
        boxes = choice_boxes([r"one generation", r"five generations"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.4)
        head = label(r"generations, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear one generation, then five."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one, \ then five", kind="physical model", detail=r"Part 56's mix, \ Monochord's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["once"], st["five"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["five"], c.duration, buff=0.08)
        with self.voiceover("The fifth generation is hollow and gurgling, the cymbals turned to swirling noise: errors coded as if they were music."):
            self.play(Indicate(boxes[1], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"keep the lossless or high-resolution master; \ make every lossy file from it, \ once", WHITE),
            (r"never edit a lossy file and re-encode it if the master exists", WHITE),
            (r"streaming services ask for 24-bit masters and encode them themselves, \ at each rate", WHITE),
            (r"and leave a true-peak margin \ (Part 57): \ decoded peaks can change across encodings; overshoot is not guaranteed to increase monotonically", TUNE),
        ]
        rows_scene(self, r"in practice", items,
                   "The practice follows. <bookmark mark='b'/> Keep a lossless or high-resolution master, and make every lossy file from it, once. <bookmark mark='c'/> Never edit a lossy file and re-encode it if the master exists. <bookmark mark='d'/> Streaming services ask for twenty-four-bit masters and encode them themselves, at each rate they offer. <bookmark mark='e'/> And leave Part 57's true-peak margin, because decoded peaks can change across encodings; overshoot is not guaranteed to increase monotonically.", marks="bcde")
