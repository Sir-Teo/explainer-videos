from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.dark_room()
        self.funnel()
        self.not_pictures()
        self.objectives()

    def dark_room(self):
        src = archive.HECHT_1942
        head = heading(r"A dark room, \ New York, \ 1942")
        room = RoundedRectangle(width=6.4, height=4.4, corner_radius=0.15, stroke_color=GREY_D, stroke_width=2,
                                fill_color="#05070a", fill_opacity=1.0).move_to([-3.4, -0.4, 0])
        fix = Dot(room.get_center(), radius=0.05, color="#5a2020")
        flash_at = room.get_center() + np.array([-1.7, 0.6, 0])
        flash = Dot(flash_at, radius=0.09, color=LIGHT, fill_opacity=0.0)
        rows = rows_of([
            (r"forty minutes in the dark, \ eyes fixed on a faint point", WHITE),
            (r"a tiny, \ brief flash of blue-green light, \ off to one side", LIGHT),
            (r"``did you see it?'' \ \ said only when sure", GREY_A),
            (r"the light was measured in physics' own unit: \ the quantum", LIGHT),
            (r"how few quanta can a person see?", YOU),
        ], 5.6, 30, 0.36).move_to([3.5, -0.1, 0])
        keep_in_frame(rows)
        tag = historical_tag(src.cite)
        with self.voiceover(
            "New York, 1942. In a laboratory at Columbia University, an observer sits in total darkness for forty "
            "minutes, eyes fixed on a faint point of light. <bookmark mark='a'/> Then, off to one side, a flash: tiny, "
            "brief, and blue-green. <bookmark mark='b'/> Did you see it? The observers, most of "
            "them the authors themselves, had trained themselves to say yes only when they were sure. "
            "<bookmark mark='c'/> Selig Hecht, Simon Shlaer and Maurice Pirenne measured the energy of the flash in "
            "the units physics had given light early in the century: quanta, the indivisible packets of light energy. "
            "<bookmark mark='d'/> Their question was the oldest one in psychophysics, asked at its limit. How "
            "little light can a person see?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(room), FadeIn(fix), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            for _ in range(2):
                self.play(flash.animate.set_fill(opacity=0.95), run_time=0.12)
                self.play(flash.animate.set_fill(opacity=0.0), run_time=0.3)
                self.wait(0.6)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def funnel(self):
        d = load("quanta")
        head = heading(r"From the cornea to the rods")
        lo, hi = d["cornea"]
        stages = d["loss"]
        bars = VGroup()
        for i, (name, share) in enumerate(stages):
            w = 9.0 * share
            bar = Rectangle(width=max(w, 0.05), height=0.62, stroke_width=0, fill_color=LIGHT,
                            fill_opacity=0.35 + 0.15 * i)
            txt = label(rf"{name}: \ {round(lo * share)} to {round(hi * share)} quanta", font_size=27, color=WHITE)
            row = VGroup(bar, txt).arrange(RIGHT, buff=0.3)
            bars.add(row)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-0.6, 0.3, 0])
        keep_in_frame(bars)
        notes = rows_of([
            (r"4\% reflected by the cornea; \ about half absorbed on the way through the eye; \ of what reaches the "
             r"retina, \ at most a fifth caught by the rods' pigment", GREY_A),
            (rf"spread over about {archive.HECHT_1942.data['rods']} rods: \ seldom two in the same rod", LIGHT),
        ], 12.4, 26, 0.25).to_edge(DOWN, buff=0.95)
        tag = historical_tag(archive.HECHT_1942.cite)
        with self.voiceover(
            "Their answer. <bookmark mark='a'/> At the threshold, between fifty-four and a hundred and forty-eight "
            "quanta reached the front of the eye. But most never get to work. <bookmark mark='b'/> Four percent "
            "bounce off the cornea. About half are absorbed on the way through the eye. And of what reaches the "
            "retina, at most one in five is caught by the pigment in the rods. <bookmark mark='c'/> So the eye was "
            "seeing a flash when somewhere between five and fourteen quanta were absorbed. And they were spread over "
            "about five hundred rods, so it was rare for any one rod to catch two. <bookmark mark='d'/> A rod, then, "
            "must respond to a single quantum: the smallest amount of light there is. The eye is about as sensitive as "
            "physics allows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars[1:3]], lag_ratio=0.6), FadeIn(notes[0]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(bars[3], shift=RIGHT * 0.2), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Indicate(bars[3], color=LIGHT))
        self.clear_scene()

    def not_pictures(self):
        r = load("retina")
        head = heading(r"But the eye does not send a picture")
        a = picture(r["img"], 3.6, smooth=True, lo=-2.5, hi=2.5).move_to([-3.4, -0.3, 0])
        b = picture(r["out"], 3.6, smooth=True, lo=-2.5, hi=2.5).move_to([3.4, -0.3, 0])
        la = label(r"the light falling on the retina", font_size=26, color=GREY_A).next_to(a, UP, buff=0.2)
        lb = label(r"what the retina's output cells signal", font_size=26, color=CENTRE).next_to(b, UP, buff=0.2)
        arrow = Arrow(a.get_right(), b.get_left(), buff=0.25, color=GREY_B)
        cap = wrapped_label(r"differences: \ across space, \ across time, \ across wavelength", 12.0, 30, CENTRE)
        cap.to_edge(DOWN, buff=0.9)
        tag = psyche_tag(r"computed: \ a texture with natural images' statistics, \ through Psyche's retina")
        with self.voiceover(
            "And yet what the eye sends the brain is not a picture of the light. <bookmark mark='a'/> On the left, "
            "a texture with the statistics of natural images. <bookmark mark='b'/> On the right, the same light as "
            "the retina's output cells report it: the broad, slowly changing parts thrown away, the edges and changes "
            "kept. <bookmark mark='c'/> The eye sends differences: across space, across time, and across wavelength. "
            "And every step can be written down as a filter you could program."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(cap, shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 13", font_size=34, color=GREY_B), label(r"The Eye and the Code", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"counting quanta: \ how a curve's slope reveals a number no one can see",
            r"optics, \ the cone mosaic, \ and a range of light of ten billion to one",
            r"receptive fields as filters: \ the retina's centre and surround, \ the cortex's edges",
            r"your own contrast sensitivity, \ and what it hides from you",
            r"colour as linear algebra: \ three numbers, \ metamers, \ colour blindness",
            r"the dress, \ two visual streams, \ and the screens built on all of it",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 13 of Psychology, Built: the eye and the code. <bookmark mark='a'/> We'll count quanta, and "
            "see how the slope of a curve reveals a number nobody can observe directly. We'll follow light through "
            "the eye's optics, its mosaic of receptors, and a range of brightness of about ten billion to one. We'll "
            "write the retina and the first stage of the cortex as filters. You'll find your own contrast "
            "sensitivity, and see what it hides from you. Colour will turn out to be linear algebra: three numbers, "
            "lights that differ yet look identical, and colour blindness as a lost dimension. Then the dress that "
            "split the internet, the two streams of vision, and the screens in your pocket, which are built on all "
            "of it."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
