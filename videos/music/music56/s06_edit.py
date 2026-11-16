from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403


class Edit(SoundScene):
    def construct(self):
        chapter(self, 5, r"Editing", r"How do you join two takes so that nobody can hear the join?")
        self.comping()
        self.splice()
        self.heard()
        self.laws()
        self.timing()

    # ------------------------------------------------------------------
    def comping(self):
        items = [
            (r"singers record several takes; \ the producer builds one from the best phrases: \ a comp", WHITE),
            (r"where to cut: \ in a silence; \ just before a consonant or a drum hit, \ where a change is expected", WHITE),
            (r"where not to: \ in the middle of a held note, \ unless the join is smoothed", WHITE),
            (r"the tool: \ the crossfade, \ one take fading out as the other fades in, \ over a few milliseconds", TUNE),
        ]
        rows_scene(self, r"takes and comps", items,
                   "Few records are single takes. <bookmark mark='b'/> Singers record several, and the producer builds one from the "
                   "best phrases of each: a comp. <bookmark mark='c'/> Where to cut? In a silence, or just before a consonant or a "
                   "drum hit, where the ear expects a change anyway. <bookmark mark='d'/> Where not to: in the middle of a held "
                   "note, unless the join is smoothed. <bookmark mark='e'/> The tool is the crossfade: one take fading out as the "
                   "other fades in, over a few milliseconds.", marks="bcde")

    # ------------------------------------------------------------------
    def splice(self):
        d = load("edit")
        t = np.linspace(0, 1, 400)
        a = np.sin(2 * np.pi * 4.3 * t)
        b = np.sin(2 * np.pi * 4.3 * t + 2.2)
        cut = 200
        y = np.r_[a[:cut], b[cut:]]
        ax = frame_axes(width=9.0, height=1.8, xlo=0, xhi=1, ylo=-1.2, yhi=1.2, center=UP * 1.2)
        wave = VMobject(stroke_color=TUNE, stroke_width=3).set_points_as_corners([ax.to(x, v) for x, v in zip(t, y)])
        jump = Line(ax.to(t[cut - 1], y[cut - 1]), ax.to(t[cut], y[cut]), color=RED, stroke_width=6)
        fo = 0.5 * (1 + np.cos(np.pi * np.clip((t - 0.45) / 0.1, 0, 1)))
        z = a * fo + b * (1 - fo)
        ax2 = frame_axes(width=9.0, height=1.8, xlo=0, xhi=1, ylo=-1.2, yhi=1.2, center=DOWN * 1.4)
        wave2 = VMobject(stroke_color=TUNE, stroke_width=3).set_points_as_corners([ax2.to(x, v) for x, v in zip(t, z)])
        zone = Rectangle(width=0.9, height=1.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.15).move_to(ax2.to(0.5, 0))
        l1 = label(r"a butt splice: \ the waveform jumps", font_size=17, color=RED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        l2 = label(r"a crossfade: \ the jump spread over the shaded span", font_size=17, color=BLUE).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)
        note = label(rf"in our edit the voice jumps by {d['jump']:.2f} of its full swing in one sample: \ a click", font_size=17, color=WHITE).to_edge(DOWN, buff=0.3)
        head = label(r"why a cut clicks", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Why does a cut click? <bookmark mark='a'/> Two takes can have different instantaneous waveform values at a splice. Join them with a butt splice and the waveform jumps, and a jump contains every frequency at once: a click. In our edit, in the middle of a note, the voice jumps by {say(d['jump'], 2)} of its full swing in a single sample. <bookmark mark='b'/> A crossfade spreads the jump over a few milliseconds, and the click becomes a smooth change of timbre the ear accepts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ax2), FadeIn(ghost(VGroup(wave, wave2), 0.3)))
            vo.wait_until("a")
            self.play(Create(wave), FadeIn(l1), run_time=1.2)
            self.play(Create(jump), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(zone), Create(wave2), FadeIn(l2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("edit")
        c = clip("edit.two")
        boxes = choice_boxes([r"butt splice", r"10 ms crossfade"], width=3.2, height=0.9, buff=1.2, size=22).move_to(UP * 0.4)
        note = label(rf"two takes of the Tune's first phrase, \ joined {d['cut_s']:.2f} s in, \ in the middle of a note", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"two joins, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear both joins: two takes of the Tune's first phrase, cut in the middle of a note. Listen for the moment of the cut."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a cut, \ twice", kind="physical model", detail=r"Part 8's voice, \ two takes", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["butt"], st["crossfade"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["crossfade"], c.duration, buff=0.08)
        with self.voiceover(
            "The butt splice ticks at the cut; the crossfade hides it, and leaves only the change from one take's vibrato to "
            "the other's."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        d = load("edit")
        t = np.array(d["t"])
        ax = frame_axes(width=8.6, height=3.0, xlo=0, xhi=1, ylo=-4, yhi=4, center=DOWN * 0.3 + LEFT * 0.6)
        cs = VGroup(curve(t, d["curves"]["linear"]["related"], ax.to, color=TUNE, width=3), curve(t, d["curves"]["linear"]["unrelated"], ax.to, color=BLUE, width=3),
                    curve(t, d["curves"]["power"]["related"], ax.to, color=EAR, width=3), curve(t, d["curves"]["power"]["unrelated"], ax.to, color=GREY_A, width=3))
        key = VGroup(label(r"linear, \ related takes", font_size=16, color=TUNE), label(r"linear, \ unrelated", font_size=16, color=BLUE),
                     label(r"equal power, \ related", font_size=16, color=EAR), label(r"equal power, \ unrelated", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        xt = VGroup(label(r"start", font_size=14, color=GREY_A).next_to(ax.to(0, -4), DOWN, buff=0.1), label(r"middle", font_size=14, color=GREY_A).next_to(ax.to(0.5, -4), DOWN, buff=0.1),
                    label(r"end", font_size=14, color=GREY_A).next_to(ax.to(1, -4), DOWN, buff=0.1))
        yt = VGroup(*[label(f"{v:+d} dB" if v else "0 dB", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (3, 0, -3)])
        note = label(r"the same take on both sides adds in amplitude; \ two different sounds add in power: \ choose the law to match", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"crossfade laws", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Which fade shape? It depends on what is being joined. <bookmark mark='a'/> If the two sides are nearly the same "
            "sound, say two pieces of one sustained take, their waves add in amplitude, and a linear fade, one gain falling as "
            "the other rises, keeps the level flat; <bookmark mark='b'/> but the same fade between unrelated sounds dips by "
            "three decibels in the middle, because unrelated sounds add in power. <bookmark mark='c'/> The equal-power fade, "
            "a cosine and a sine, fixes that, and bulges by three decibels on coherent, in-phase material. It is Part 55's pan law "
            "again, in time instead of space."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(cs[2]), Create(cs[3]), FadeIn(key[2]), FadeIn(key[3]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timing(self):
        items = [
            (r"timing: \ cut drum tracks at each hit and slide the pieces onto the grid, \ crossfading every gap", WHITE),
            (r"elastic audio: \ stretch between hits instead \ (Part 50's phase vocoder)", WHITE),
            (r"pitch: \ Part 50's correction, \ note by note \ (Melodyne, \ 2001)", WHITE),
            (r"every one of these can make a performance perfect, \ and lifeless: \ Part 43's expressive timing is what gets edited out", TUNE),
            (r"the craft is to fix what distracts, \ and keep what moves", GREY_A),
        ]
        rows_scene(self, r"time and pitch", items,
                   "Editing reaches inside performances too. <bookmark mark='b'/> Timing: cut a drum track at every hit and slide the pieces onto the grid, crossfading every gap. <bookmark mark='c'/> Or stretch the audio between the hits instead, with Part 50's phase vocoder. <bookmark mark='d'/> Pitch: Part 50's correction, note by note, as Melodyne has done since 2001. <bookmark mark='e'/> Every one of these can remove intended expression when applied indiscriminately: the expressive timing of Part 43 is exactly what gets edited out. <bookmark mark='f'/> The craft is to fix what distracts, and keep what moves.", marks="bcdef")
