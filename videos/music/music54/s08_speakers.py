from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403

SC = {"phone": EAR, "bookshelf": BLUE, "floor": TUNE}
SN = {"phone": r"a phone's speaker", "bookshelf": r"a sealed bookshelf speaker", "floor": r"a vented floor-stander"}


class Speakers(SoundScene):
    def construct(self):
        chapter(self, 7, r"Three loudspeakers", r"What does each size of loudspeaker leave out?")
        self.curves()
        self.measure()
        self.heard()
        self.ear()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("speakers")
        f = np.array(d["f"])
        ax = logf_axes(width=8.0, height=3.4, flo=20, fhi=20000, ylo=-40, yhi=6, center=LEFT * 0.8 + DOWN * 0.2)
        cs = VGroup(*[curve(f, np.maximum(np.array(d["curves"][k]) - np.median(np.array(d["curves"][k])[(f > 1500) & (f < 4000)]), -40), ax.to, color=SC[k], width=3) for k in ("phone", "bookshelf", "floor")])
        key = VGroup(*[label(rf"{SN[k]}: \ $-3$ dB at {d['f3'][k]:.0f} Hz", font_size=16, color=SC[k]) for k in ("phone", "bookshelf", "floor")]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.35)
        p = d["params"]
        note = label(rf"cone areas: \ {p['phone']['Sd_cm2']:.1f}, \ {p['bookshelf']['Sd_cm2']:.0f} and {p['floor']['Sd_cm2']:.0f} cm$^2$", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.45)
        yl = label(r"dB", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        head = label(r"three loudspeakers, \ simulated", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Three loudspeakers, simulated with the same circuit. <bookmark mark='a'/> A phone's: a cone of a square centimetre "
            f"in a tiny sealed chamber, down three decibels at {say(d['f3']['phone'])} hertz. <bookmark mark='b'/> A sealed "
            f"bookshelf speaker: {say(d['f3']['bookshelf'])} hertz. <bookmark mark='c'/> A vented floor-stander: "
            f"{say(d['f3']['floor'])} hertz. The bass a speaker can make is set by how much air it can move, the cone's area "
            "times its travel, and by the box."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(note), FadeIn(ghost(cs, 0.25)))
            for mark, i in zip("abc", range(3)):
                vo.wait_until(mark)
                self.play(Create(cs[i]), FadeIn(key[i]), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("speakers")
        c = clip("speakers.three")
        cells = choice_boxes([r"phone", r"bookshelf", r"floor-stander"], width=3.0, buff=0.7, colors=[EAR, BLUE, TUNE]).move_to(UP * 0.4)
        cap = label(r"a groove of Part 40's drums and a plucked bass, \ matched in loudness", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"one groove, \ three loudspeakers, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear one groove through each: the phone, the bookshelf speaker, the floor-stander."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        names = ["phone", "bookshelf", "floor"]
        with self.listen(c) as snd:
            window(snd, r"three loudspeakers", kind="physical model", detail=r"a groove", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "Through the phone the bass line all but disappears; you hear its upper harmonics and the click of the kick, and "
            "your ear rebuilds the rest, Part 4's missing fundamental. The bookshelf speaker gives the bass back but not the "
            "lowest thud of the kick; the floor-stander has both."
        ):
            self.play(Indicate(cells[2], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ear(self):
        items = [
            (r"mixes are checked on small speakers too: \ a bass line must survive as harmonics", WHITE),
            (r"phones add a little distortion on purpose, \ or a `virtual bass' processor, \ to make harmonics the ear can use", WHITE),
            (r"Part 4's missing fundamental does the rest", WHITE),
            (r"the room changes the bass more than the speaker does \ (Part 55)", WHITE),
            (r"and to get more sound from a small driver, \ a different shape helps: \ the horn", TUNE),
        ]
        rows_scene(self, r"bass you cannot hear", items,
                   "Engineers live with this. <bookmark mark='b'/> Mixes are checked on small speakers too, so that a bass line "
                   "survives as harmonics. <bookmark mark='c'/> Phones add a little distortion on purpose, or a virtual-bass "
                   "processor, to make harmonics the ear can use, <bookmark mark='d'/> and Part 4's missing fundamental does the "
                   "rest. <bookmark mark='e'/> Room modes can strongly change bass response alongside the speaker's own limits, which is Part 55. "
                   "<bookmark mark='f'/> And to get more sound out of a small driver, a different shape helps: the horn.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def measure(self):
        items = [
            (r"play Part 49's exponential sweep, \ record it with a measurement microphone, \ deconvolve", WHITE),
            (r"cut the impulse response off before the first reflection arrives: \ a gated, \ quasi-anechoic measurement", WHITE),
            (r"the gate's length limits the lowest frequency it can see: \ 5 ms, \ about 200 Hz", WHITE),
            (r"below that, \ measure close to the cone, \ or outdoors on a pole", WHITE),
            (r"and measure off axis too: \ off-axis radiation contributes strongly to room sound; its share depends on room, distance and directivity", TUNE),
        ]
        rows_scene(self, r"measuring a loudspeaker", items,
                   "Real loudspeakers are measured, not just simulated. <bookmark mark='b'/> Play Part 49's exponential sweep, record it with a measurement microphone, and deconvolve. <bookmark mark='c'/> Cut the impulse response off before the first reflection from the floor arrives: a gated, quasi-anechoic measurement. <bookmark mark='d'/> The gate's length limits the lowest frequency it can see: five milliseconds, about two hundred hertz. <bookmark mark='e'/> Below that, measure close to the cone, or outdoors on a pole. <bookmark mark='f'/> And measure off axis too, because off-axis radiation contributes strongly to room sound; its share depends on room, distance and directivity.", marks="bcdef")
