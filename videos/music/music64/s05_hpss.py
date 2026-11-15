from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Hpss(SoundScene):
    def construct(self):
        chapter(self, 4, r"Harmonic and percussive", r"Can a picture's lines be told from its stripes?")
        self.idea()
        self.mask()
        self.heard()
        self.sweep()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"in a spectrogram, \ a sustained note is a horizontal line: \ steady in frequency, \ long in time", WHITE),
            (r"a drum hit is a vertical stripe: \ brief in time, \ broad in frequency", WHITE),
            (r"a median filter along time keeps the lines and erases the stripes; \ along frequency, \ the opposite", WHITE),
            (r"compare the two in each bin, \ and share the bin between them: \ FitzGerald \ (2010)", WHITE),
            (r"one channel, \ no training, \ a few lines of code", TUNE),
        ]
        rows_scene(self, r"lines and stripes", items,
                   "On one channel, look at the picture. <bookmark mark='b'/> In a spectrogram a sustained note is a horizontal line, "
                   "steady in frequency and long in time. <bookmark mark='c'/> A drum hit is a vertical stripe, brief in time and "
                   "broad in frequency. <bookmark mark='d'/> A median filter along time keeps the lines and erases the stripes; "
                   "along frequency, the opposite. <bookmark mark='e'/> Compare the two in each bin and share the bin between them, "
                   "as Derry FitzGerald proposed in 2010. <bookmark mark='f'/> One channel, no training, a few lines of code.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def mask(self):
        d = load("hpss")
        M = np.array(d["mask"])
        pic = picture(M, 0, 1, 10.0, 3.6).move_to(DOWN * 0.2)
        note = label(r"the harmonic mask: \ bright where a bin is mostly harmonic \ (0 to 4.7 kHz, \ the first phrases)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the session's bins, \ shared", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the harmonic mask for the session: bright where a bin is mostly harmonic. The horizontal lines are the voice, bass, piano and guitar; the dark vertical stripes are the drum hits."):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(note))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("hpss")
        c = clip("hpss.two")
        boxes = choice_boxes([r"harmonic", r"percussive"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.5)
        res = label(rf"against the true stems: \ the tonal instruments {d['sdr_tonal']:.1f} dB, \ the drums only {d['sdr_drums']:.1f} dB: \ attacks of piano and guitar count as percussion, \ and the hi-hat's hiss as neither",
                    font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"split, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the two halves."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"harmonic, \ then percussive", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["harmonic"], st["percussive"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["percussive"], c.duration, buff=0.08)
        with self.voiceover(
            f"The harmonic half is the band without its drums, {say(d['sdr_tonal'], 1)} decibels from the true tonal stems. "
            f"The percussive half is less clean, {say(d['sdr_drums'], 1)} decibels: the attacks of the piano and guitar count as "
            "percussion too, and the hi-hat's hiss is neither line nor stripe. A good first step for remixing, and for Part 62's "
            "beat tracker, which wants the stripes."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("hpsssweep")
        n = np.array(d["sizes"], float)
        p2 = d["power"]["2"]
        p1 = d["power"]["1"]
        ax = frame_axes(width=8.5, height=3.2, xlo=np.log2(3), xhi=np.log2(63), ylo=-2, yhi=11, center=DOWN * 0.5 + LEFT * 0.8)
        lines_ = VGroup(curve(np.log2(n), p2["tonal"], ax.to, color=TUNE, width=3), curve(np.log2(n), p2["drums"], ax.to, color=EAR, width=3),
                        curve(np.log2(n), p1["tonal"], ax.to, color=TUNE, width=1.5), curve(np.log2(n), p1["drums"], ax.to, color=EAR, width=1.5))
        ticks = VGroup(*[label(f"{int(v)}", font_size=14, color=GREY_A).move_to(ax.to(np.log2(v), -2) + DOWN * 0.25) for v in n])
        xl = label(r"length of each median filter \ (frames or bins)", font_size=14, color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        yl = label(r"SDR \ (dB)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        key = VGroup(label(r"tonal stems", font_size=16, color=TUNE), label(r"drums", font_size=16, color=EAR),
                     label(r"thick: \ power 2; \ thin: \ power 1", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        head = label(r"the filter's length", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        best_t, best_d = max(p2["tonal"]), max(p2["drums"])
        with self.voiceover(
            "The method has two knobs: how long the median filters are, and how sharply the masks decide. "
            "<bookmark mark='a'/> Short filters cannot tell a line from a stripe; longer ones can. On this session both halves "
            f"keep improving up to sixty-three frames, the tonal stems to {say(best_t, 1)} decibels and the drums to "
            f"{say(best_d, 1)}, because its notes are long. <bookmark mark='b'/> Sharper masks, power two, help a little. The "
            "best settings depend on the music, which is why such knobs are tuned on examples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(lines_[0]), Create(lines_[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines_[2]), Create(lines_[3]), run_time=1.2)
        self.wait(0.6)
        self.clear_scene()
