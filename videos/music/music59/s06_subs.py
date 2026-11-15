from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Subs(SoundScene):
    def construct(self):
        chapter(self, 5, r"Subwoofer arrays", r"How do you aim a sound whose wavelength is longer than the truck?")
        self.problem()
        self.cardioid()
        self.heard()
        self.more()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"at 50 Hz the wavelength is 7 m: \ a subwoofer box is far too small to be directional", WHITE),
            (r"so subwoofers radiate everywhere: \ onto the stage, \ into the microphones, \ out of the back of the venue", WHITE),
            (r"and a row of subwoofers across the stage interferes with itself: \ loud and quiet stripes across the audience", WHITE),
            (r"directivity at low frequencies comes only from several sources, \ and the delays between them", TUNE),
        ]
        rows_scene(self, r"bass goes everywhere", items,
                   "Bass is the hardest part to aim. <bookmark mark='b'/> At fifty hertz the wavelength is seven metres; a "
                   "subwoofer box is far too small to be directional. <bookmark mark='c'/> So subwoofers radiate everywhere: onto "
                   "the stage, into the microphones, and out of the back of the venue to the neighbours. <bookmark mark='d'/> And a "
                   "row of them across the stage interferes with itself, leaving loud and quiet stripes across the audience. "
                   "<bookmark mark='e'/> At low frequencies, directivity comes only from several sources and the delays between "
                   "them.", marks="bcde")

    # ------------------------------------------------------------------
    def cardioid(self):
        d = load("subs")
        f = np.array(d["f"])
        ax = logf_axes(width=8.4, height=3.0, flo=25, fhi=200, ylo=-40, yhi=3, center=DOWN * 0.5 + LEFT * 0.8, ticks=(50, 100, 200))
        fr = curve(f, np.clip(d["front_db"], -40, 3), ax.to, color=TUNE, width=3)
        bk = curve(f, np.clip(d["back_db"], -40, 3), ax.to, color=EAR, width=3)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(25, v), LEFT, buff=0.1) for v in (0, -20, -40)])
        key = VGroup(label(r"in front", font_size=16, color=TUNE), label(r"behind \ (cancelled)", font_size=16, color=EAR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        diag = VGroup(Square(side_length=0.5, stroke_color=TUNE, stroke_width=3), Square(side_length=0.5, stroke_color=EAR, stroke_width=3)).arrange(LEFT, buff=0.4).to_edge(UP, buff=1.1).shift(LEFT * 3)
        dl = label(rf"the rear box: \ {d['spacing']:.1f} m behind, \ delayed {d['delay_ms']:.1f} ms, \ polarity inverted", font_size=16, color=EAR).next_to(diag, RIGHT, buff=0.4)
        note = label(r"0 dB: \ two boxes adding in step; \ behind, \ the rear box's sound meets the front box's exactly inverted", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"a cardioid pair", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest aimed bass is a cardioid pair. <bookmark mark='a'/> Put a second subwoofer ninety centimetres behind "
            f"the first, delay it by the time sound takes to cross that gap, {say(d['delay_ms'], 1)} milliseconds, and invert its "
            "polarity. <bookmark mark='b'/> Behind, the front box's sound arrives exactly when the rear box's inverted copy "
            "leaves, and they cancel, at every frequency: in this ideal model completely, in a real one by fifteen to twenty-five "
            "decibels. <bookmark mark='c'/> In front they arrive a little apart and mostly add; the sum is strongest where the gap "
            "is a quarter of a wavelength, near ninety-five hertz, and weaker towards the deepest bass. Part 54's gradient "
            "microphone, built out of loudspeakers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(VGroup(fr, bk), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(diag), FadeIn(dl))
            vo.wait_until("b")
            self.play(Create(bk), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(fr), FadeIn(key[0]), FadeIn(note), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("subs")
        c = clip("subs.two")
        boxes = choice_boxes([r"ordinary subwoofers", r"a cardioid pair"], width=3.4, height=0.9, buff=1.0, size=20).move_to(UP * 0.4)
        note = label(r"heard behind the stage, \ where the band stands", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"behind the stage, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear our mix from behind the stage, where the band stands: ordinary subwoofers, then a cardioid pair. You will need headphones or loudspeakers with real bass."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"plain, \ then cardioid", kind="physical model", detail=r"our mix, \ simulated subwoofers", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["plain"], st["cardioid"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["cardioid"], c.duration, buff=0.08)
        with self.voiceover("Behind a cardioid pair the bass all but disappears, leaving only what the main loudspeakers spill backwards: a quieter stage, and cleaner microphones."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def more(self):
        items = [
            (r"end-fire arrays: \ a row of subwoofers pointing at the audience, \ each delayed to travel with the sound: \ a forward beam", WHITE),
            (r"arc delays: \ a straight row across the stage, \ delayed as if it were curved, \ to widen the coverage evenly", WHITE),
            (r"flown subwoofers beside the arrays: \ less level difference between the front row and the back", WHITE),
            (r"all of it in the same delays and polarities as Part 54's microphone arrays", TUNE),
        ]
        rows_scene(self, r"more ways to aim bass", items,
                   "There are other shapes. <bookmark mark='b'/> End-fire arrays: a row of subwoofers pointing at the audience, each "
                   "delayed so its sound travels with the one behind it, making a forward beam. <bookmark mark='c'/> Arc delays: a "
                   "straight row across the stage, delayed as if it were curved, to spread the bass evenly. "
                   "<bookmark mark='d'/> Flown subwoofers beside the arrays, so that the front row is not shaken while the back row "
                   "hears nothing. <bookmark mark='e'/> All of it is the delays and polarities of Part 54's microphone arrays.", marks="bcde")
