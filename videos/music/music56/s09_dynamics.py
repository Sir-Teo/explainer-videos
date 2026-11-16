from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403


class Dynamics(SoundScene):
    def construct(self):
        chapter(self, 8, r"Dynamics and buses", r"How does a mix keep a voice in front and the drums hitting?")
        self.vocal()
        self.parallel()
        self.heard()
        self.buses()
        self.automation()

    # ------------------------------------------------------------------
    def vocal(self):
        d = load("dynamics")["vox"]
        bars = VGroup()
        for i, (k, v, col) in enumerate((("as sung", d["spread_before"], GREY_A), ("compressed", d["spread_after"], TUNE))):
            w = 0.55 * v
            b = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.8)
            b.move_to([-3.0 + w / 2, 0.6 - 1.1 * i, 0])
            bars.add(VGroup(b, label(k, font_size=19, color=col).next_to(b, LEFT, buff=0.3), label(rf"{v:.1f} dB", font_size=19, color=WHITE).next_to(b, RIGHT, buff=0.2)))
        bars.scale(min(1.0, 12.6 / bars.width)).move_to(ORIGIN)
        cap = label(r"how far the voice's level wanders: \ the 95th minus the 10th percentile of its 50 ms levels", font_size=17, color=GREY_A).move_to(UP * 1.8)
        sett = label(rf"threshold $-26$ dBFS, \ ratio 4 : 1, \ attack 5 ms, \ release 120 ms: \ {d['gr_mean']:.0f} dB of gain reduction on average, \ {d['gr_max']:.0f} at most",
                     font_size=17, color=WHITE).to_edge(DOWN, buff=0.6)
        head = label(r"a compressor on the voice", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 50 built the compressor; many mixes use it on selected tracks. <bookmark mark='a'/> A singer's level wanders: "
            f"ours by {say(d['spread_before'], 1)} decibels between its quiet and loud moments. Over a band, the quiet words "
            "are masked and the loud ones jump out. <bookmark mark='b'/> A compressor at four to one, starting at minus "
            f"twenty-six, narrows that to {say(d['spread_after'], 1)}, turning the loudest notes down by up to "
            f"{say(d['gr_max'])} decibels, and the fader can then sit the whole voice in front of the band."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(bars, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(sett))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallel(self):
        d = load("dynamics")
        e = d["env"]
        t = np.array(e["t"])
        ax = frame_axes(width=10.0, height=2.6, xlo=0, xhi=t[-1], ylo=-60, yhi=0, center=DOWN * 0.8)
        cd = curve(t, np.clip(e["dry"], -60, 0), ax.to, color=GREY_A, width=2)
        cp = curve(t, np.clip(e["parallel"], -60, 0), ax.to, color=TUNE, width=2)
        xt = VGroup(*[label(f"{v} s", font_size=14, color=GREY_A).next_to(ax.to(v, -60), DOWN, buff=0.1) for v in range(0, int(t[-1]) + 1)])
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -30, -60)])
        dia = VGroup(label(r"drums", font_size=18, color=WHITE), MathTex(r"\to", font_size=30), label(r"dry", font_size=18, color=GREY_A), MathTex(r"+", font_size=30),
                     label(r"a copy crushed \ (10 : 1 at $-40$ dBFS, \ 0.05 ms attack), \ 6 dB down", font_size=18, color=TUNE)).arrange(RIGHT, buff=0.25).to_edge(UP, buff=1.0)
        key = VGroup(label(r"dry", font_size=16, color=GREY_A), label(r"with the crushed copy underneath", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.15)
        dr = d["drums"]
        note = label(rf"the peaks stay; \ the decays between them rise: \ level spread {dr['spread_dry']:.0f} dB $\to$ {dr['spread_parallel']:.0f} dB", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"parallel compression", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Drums are treated differently. <bookmark mark='a'/> Parallel compression, called New York compression after the "
            "studios that made it famous, keeps the dry drums and adds underneath a copy crushed flat: ten to one from minus "
            "forty, with an attack of a twentieth of a millisecond, mixed six decibels down. <bookmark mark='b'/> Here are the "
            "two levels, ten-millisecond by ten-millisecond. The hits keep their peaks, because the dry signal still has them; "
            "<bookmark mark='c'/> but between the hits, where the drums ring and decay, the crushed copy lifts the level, "
            f"and the spread from peak to decay shrinks from {say(dr['spread_dry'])} to {say(dr['spread_parallel'])} decibels: "
            "drums that hit hard and sound full."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(VGroup(cd, cp), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(dia))
            vo.wait_until("b")
            self.play(Create(cd), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(key[1]), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("dynamics")
        c = clip("dynamics.two")
        boxes = choice_boxes([r"dry", r"parallel"], width=3.0, height=0.9, buff=1.4, size=22).move_to(UP * 0.4)
        head = label(r"drums, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"matched in loudness; \ listen to the space between the hits", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover("Hear our drums dry, then with the crushed copy underneath, matched in loudness. Listen between the hits."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"dry, \ then parallel", kind="physical model", detail=r"Part 40's drums", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["dry"], st["parallel"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["parallel"], c.duration, buff=0.08)
        with self.voiceover("The second sounds thicker and closer: the snare's ring and the hi-hat's wash fill in, and the kit seems to be in a smaller, louder room."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def buses(self):
        items = [
            (r"groups: \ the drums, \ the backing voices, \ the strings, \ each summed to a bus with its own fader and compressor", WHITE),
            (r"bus compression: \ a gentle compressor on the whole mix, \ 2 dB of reduction, \ makes the parts move together: \ `glue'", WHITE),
            (r"side-chains \ (Part 50): \ the kick ducks the bass, \ the voice ducks the guitars, \ so that each gets out of the other's way", WHITE),
            (r"the wall of sound was this taken to its end: \ everything through one compressor, \ pushed until it saturated", TUNE),
        ]
        rows_scene(self, r"buses", items,
                   "Mixes are built in groups. <bookmark mark='b'/> The drums, the backing voices, the strings: each group is summed to a bus with its own fader and its own compressor. <bookmark mark='c'/> A gentle compressor on the whole mix, two decibels of reduction, makes the parts rise and fall together; engineers call it glue. <bookmark mark='d'/> Side-chains, from Part 50, let the kick duck the bass and the voice duck the guitars, so that each gets out of the other's way: masking handled in time rather than frequency. <bookmark mark='e'/> Our wall-of-sound illustration combines doubling, reverberation and strong compression; historical productions used varied recording chains.", marks="bcde")

    # ------------------------------------------------------------------
    def automation(self):
        items = [
            (r"a fader need not stay still: \ automation records its moves and plays them back", WHITE),
            (r"rides: \ the voice up a decibel on a quiet word, \ the guitar up for its solo", WHITE),
            (r"mutes and sends as gestures: \ the dub's drops and echo throws are automation, \ performed", WHITE),
            (r"console automation from the 1970s; \ in the workstation, \ every knob can move", TUNE),
        ]
        rows_scene(self, r"automation", items,
                   "And a mix moves. <bookmark mark='b'/> A fader need not stay still: automation records its moves and plays them "
                   "back. <bookmark mark='c'/> Rides: the voice up a decibel on a quiet word, the guitar up for its solo. "
                   "<bookmark mark='d'/> Mutes and sends become gestures: the dub's drop-outs and echo throws are automation, "
                   "performed, as King Tubby performed them by hand. <bookmark mark='e'/> Consoles automated their faders from the "
                   "1970s; in a workstation every knob can move.", marks="bcde")
