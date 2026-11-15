from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403


def box(text, color=GREY_B, w=1.9, h=0.8, size=17):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.5), label(text, font_size=size, color=color))


class Purpose(SoundScene):
    def construct(self):
        chapter(self, 1, r"What mastering is for", r"Why does a finished mix need another engineer?")
        self.jobs()
        self.chain_boxes()
        self.heard()
        self.album()

    # ------------------------------------------------------------------
    def jobs(self):
        items = [
            (r"the last creative step and the first technical one: \ between the mix and the listener", WHITE),
            (r"fresh ears in a better room: \ a mastering room is built for accuracy, \ not for mixing", WHITE),
            (r"translation: \ a gentle EQ so the mix works on every system \ (Part 56's phone)", WHITE),
            (r"loudness and peaks: \ a level that suits the medium, \ and peaks that will survive conversion", WHITE),
            (r"the album: \ songs matched to each other, \ the order, \ the gaps, \ the fades; \ then the delivery files", TUNE),
        ]
        rows_scene(self, r"between the mix and the listener", items,
                   "What is mastering? <bookmark mark='b'/> It is the last creative step in making a record and the first technical "
                   "one in delivering it. <bookmark mark='c'/> A mastering engineer brings fresh ears and a room built for "
                   "accuracy. <bookmark mark='d'/> They make the mix translate, with gentle equalization, so that it works on every "
                   "system, Part 56's phone included. <bookmark mark='e'/> They set a loudness that suits the medium, and peaks that "
                   "will survive conversion. <bookmark mark='f'/> And they make an album: songs matched to each other, the order, "
                   "the gaps and the fades, and then the files for every format.", marks="bcdef")

    # ------------------------------------------------------------------
    def chain_boxes(self):
        d = load("chain")["stages"]
        names = [(r"the mix", GREY_A), (r"tilt EQ", WHITE), (r"glue \ compression", WHITE), (r"look-ahead \ limiter", TUNE), (r"dither", WHITE), (r"files", GREY_A)]
        chain = VGroup(*[box(n, c_) for n, c_ in names]).arrange(RIGHT, buff=0.35).move_to(UP * 0.8)
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(len(chain) - 1)])
        stats = VGroup()
        for i, k in enumerate(("mix", "eq", "glue", "limited")):
            v = d[k]
            stats.add(label(rf"{v['lufs']:.0f} LUFS \ {v['tp']:.0f} dBTP \ crest {v['crest']:.0f} dB", font_size=13, color=GREY_A).next_to(chain[i], DOWN, buff=0.35))
        what = VGroup(label(r"+0.5 dB below 120 Hz, \ +1 dB above 8 kHz", font_size=14, color=WHITE).next_to(stats[1], DOWN, buff=0.25),
                      label(r"2 : 1 from $-18$ dBFS, \ slow", font_size=14, color=WHITE).next_to(stats[2], DOWN, buff=0.25),
                      label(r"pushed to $-10$ LUFS, \ ceiling $-1$ dBTP", font_size=14, color=TUNE).next_to(stats[3], DOWN, buff=0.25))
        head = label(r"Monochord's mastering chain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"\texttt{master.master(y, target)}: \ the gain into the limiter is found by iteration until the loudness is right", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the chain Monochord uses, the usual one. <bookmark mark='a'/> The mix arrives at minus twenty LUFS. A "
            "tilt equalizer lifts the extremes a little. <bookmark mark='b'/> A gentle compressor, two to one, slow, makes the "
            "mix move as one. <bookmark mark='c'/> Then the look-ahead limiter, which sets the loudness: the mix is pushed into "
            "it until it reads, here, minus ten, with no peak above minus one. <bookmark mark='d'/> Last, dither, when the "
            "word length is cut, and the files. The crest factor hardly moves until the limiter, which takes five decibels of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(chain, arrows), 0.25)), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(chain[:2]), FadeIn(arrows[0]), FadeIn(stats[:2]), FadeIn(what[0]))
            vo.wait_until("b")
            self.play(FadeIn(chain[2]), FadeIn(arrows[1]), FadeIn(stats[2]), FadeIn(what[1]))
            vo.wait_until("c")
            self.play(FadeIn(chain[3]), FadeIn(arrows[2]), FadeIn(stats[3]), FadeIn(what[2]))
            vo.wait_until("d")
            self.play(FadeIn(chain[4:]), FadeIn(arrows[3:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("chain")
        c = clip("chain.three")
        boxes = choice_boxes([r"the mix", r"after the glue", r"limited"], width=2.8, height=0.9, buff=0.9, size=20).move_to(UP * 0.4)
        note = label(r"each at its own level: \ the last is 10 dB louder", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"the chain, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear three stages, each at its own level: the mix, after the equalizer and the glue, and after the limiter."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three stages", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["mix"], st["glue"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["glue"], st["limited"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["limited"], c.duration, buff=0.08)
        with self.voiceover(
            "The glue is barely audible, as it should be; the limited master is much louder, and that is exactly the trap: "
            "louder sounds better for a moment, whatever else has changed."
        ):
            self.play(Indicate(boxes[2], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def album(self):
        items = [
            (r"songs matched in loudness and tone, \ so that none jumps out of the album", WHITE),
            (r"the order and the gaps: \ silence is part of the sequence, \ two seconds or none", WHITE),
            (r"fades and edits, \ start and end points to the sample", WHITE),
            (r"identifiers: \ ISRC codes for each track, \ the album's metadata", WHITE),
            (r"one master for each medium: \ streaming, \ CD, \ vinyl, \ broadcast", TUNE),
        ]
        rows_scene(self, r"an album, \ not a track", items,
                   "Mastering an album adds its own work. <bookmark mark='b'/> Songs are matched in loudness and tone, so that "
                   "none jumps out. <bookmark mark='c'/> The order and the gaps are chosen; silence is part of the sequence. "
                   "<bookmark mark='d'/> Fades and edits are made, start and end points set to the sample. <bookmark mark='e'/> "
                   "Each track gets its identifiers, and the album its metadata. <bookmark mark='f'/> And there is one master for "
                   "each medium: streaming, CD, vinyl and broadcast each want something different, as we will see.", marks="bcdef")
