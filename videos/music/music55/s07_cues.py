from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403

ICOL = {"500": GREY_A, "1500": BLUE, "4000": TUNE}


def head_top(R=1.0, center=ORIGIN):
    g = VGroup(Circle(radius=R, stroke_color=GREY_B, stroke_width=3).move_to(center))
    g.add(Triangle(stroke_color=GREY_B, stroke_width=3).scale(0.18).move_to(center + UP * (R + 0.12)))
    g.add(Ellipse(width=0.16, height=0.4, stroke_color=GREY_B, stroke_width=3).move_to(center + LEFT * (R + 0.05)),
          Ellipse(width=0.16, height=0.4, stroke_color=GREY_B, stroke_width=3).move_to(center + RIGHT * (R + 0.05)))
    return g


class Cues(SoundScene):
    def construct(self):
        chapter(self, 6, r"How we hear direction", r"With two ears and no eyes, \ how do you know where a sound is?")
        self.duplex()
        self.itd()
        self.ild()
        self.three()
        self.cone()
        self.quiz()
        self.resolve()

    # ------------------------------------------------------------------
    def duplex(self):
        items = [
            (r"Lord Rayleigh, \ 1876 to 1907: \ tuning forks on a lawn, \ a blindfolded listener turning towards them", WHITE),
            (r"a sound to one side reaches the near ear first: \ an interaural time difference \ (ITD)", WHITE),
            (r"and louder, \ because the head shadows the far ear: \ an interaural level difference \ (ILD)", WHITE),
            (r"the duplex theory: \ time for low frequencies, \ level for high ones, \ handing over near 1.5 kHz", TUNE),
            (r"the brain's coincidence detectors resolve time differences of about 10 microseconds", GREY_A),
        ]
        rows_scene(self, r"two ears", items,
                   "How do two ears find a direction? <bookmark mark='b'/> Lord Rayleigh asked, in experiments from 1876 to 1907, "
                   "with tuning forks on a lawn and a blindfolded listener turning towards them. <bookmark mark='c'/> A sound to one "
                   "side reaches the near ear first: an interaural time difference. <bookmark mark='d'/> And it is louder there, "
                   "because the head casts an acoustic shadow on the far ear: an interaural level difference. "
                   "<bookmark mark='e'/> Rayleigh's duplex theory: time differences locate low frequencies and level differences "
                   "high ones, handing over near one and a half kilohertz. <bookmark mark='f'/> And the brain's coincidence "
                   "detectors, in the brainstem, resolve time differences of about ten microseconds, a hundredth of the time a "
                   "neuron takes to fire.", marks="bcdef")

    # ------------------------------------------------------------------
    def itd(self):
        d = load("cues")
        az = np.array(d["az"])
        k = (az >= -90) & (az <= 90)
        ax = frame_axes(width=7.4, height=3.0, xlo=-90, xhi=90, ylo=-700, yhi=700, center=RIGHT * 1.6 + DOWN * 0.3)
        cv = curve(az[k], np.array(d["itd_us"])[k], ax.to, color=TUNE, width=3)
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=14, color=GREY_A).next_to(ax.to(v, -700), DOWN, buff=0.1) for v in (-90, -45, 0, 45, 90)])
        yt = VGroup(*[label(rf"{v} $\mu$s", font_size=14, color=GREY_A).next_to(ax.to(-90, v), LEFT, buff=0.1) for v in (-600, 0, 600)])
        hd = head_top(0.85, LEFT * 4.6 + DOWN * 0.2)
        src = Dot(hd[0].get_center() + 2.0 * np.array([np.sin(np.radians(60)), np.cos(np.radians(60)), 0]), radius=0.1, color=EAR)
        path = VGroup(Line(src.get_center(), hd[3].get_center(), color=EAR, stroke_width=2),
                      DashedLine(src.get_center(), hd[0].get_center() + 0.85 * UP, color=EAR, stroke_width=2))
        eq = MathTex(r"\Delta t = \frac{a}{c}\,(\theta + \sin\theta)", font_size=34, color=TUNE).to_edge(UP, buff=1.0).shift(RIGHT * 1.6)
        note = label(rf"Woodworth's formula for a sphere of radius 8.75 cm: \ up to {d['itd_max_us']:.0f} $\mu$s, \ straight to one side", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the time difference", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The time difference first. <bookmark mark='a'/> Treat the head as a sphere eight point seven five centimetres in "
            "radius. Sound from an angle theta reaches the far ear by a longer path, partly round the sphere, and Robert "
            "Woodworth's formula of 1938 gives the extra time: a over c times theta plus sine theta. <bookmark mark='b'/> It "
            f"rises from nothing straight ahead to {say(d['itd_max_us'])} microseconds straight to one side, two thirds of a "
            "millisecond. Steepest in front, where we locate best: one degree is about nine microseconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd), FadeIn(src), FadeIn(path), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ild(self):
        d = load("cues")
        az = np.array(d["az"])
        ax = frame_axes(width=9.6, height=3.0, xlo=-180, xhi=180, ylo=-17, yhi=17, center=DOWN * 0.3)
        cs = VGroup(*[curve(az, np.clip(d["ild"][f], -17, 17), ax.to, color=ICOL[f], width=3) for f in ("500", "1500", "4000")])
        key = VGroup(*[label(rf"{int(f)} Hz", font_size=17, color=ICOL[f]) for f in ("500", "1500", "4000")]).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=14, color=GREY_A).next_to(ax.to(v, -17), DOWN, buff=0.1) for v in (-180, -90, 0, 90, 180)])
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(-180, v), LEFT, buff=0.1) for v in (-15, 0, 15)])
        mx = {f: max(d["ild"][f]) for f in ("500", "1500", "4000")}
        note = label(rf"Brown and Duda's shadow filter: \ it starts above $c/2\pi a$ = {d['fc_head']:.0f} Hz; \ the right ear louder by up to {mx['500']:.0f}, \ {mx['1500']:.0f} and {mx['4000']:.0f} dB",
                     font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the level difference", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the level difference, all the way round, from behind on the left through the front to behind on the right. "
            "<bookmark mark='a'/> A head is small next to the wavelength of a low note, which bends round it: at five hundred "
            f"hertz the far ear is at most {say(mx['500'])} decibels quieter. <bookmark mark='b'/> Above about "
            f"{say(d['fc_head'])} hertz, the frequency whose wavelength is the head's circumference, the shadow deepens: "
            f"{say(mx['1500'])} decibels at fifteen hundred hertz, {say(mx['4000'])} at four thousand. This is Brown and Duda's "
            "spherical-head filter of 1998, Monochord's model of a head."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(key), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("cues")
        c = clip("cues.three")
        hd = head_top(0.9, UP * 0.3)
        src = Dot(hd[0].get_center() + 2.2 * np.array([np.sin(np.radians(60)), np.cos(np.radians(60)), 0]), radius=0.12, color=EAR)
        sl = label(r"60$^\circ$ right", font_size=16, color=EAR).next_to(src, RIGHT, buff=0.1)
        boxes = choice_boxes([r"time alone", r"level alone", r"both"], width=2.8, height=0.8, buff=0.8, size=20).to_edge(DOWN, buff=0.6)
        head = label(r"the two cues, \ apart and together", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear them separately, with headphones. Bursts of noise sixty degrees to the right: first with only the time "
            "difference, then with only the level difference, then with both."
        ):
            self.play(FadeIn(head), FadeIn(hd), FadeIn(src), FadeIn(sl), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three ways to the right", kind="rendered", detail=r"noise, \ a spherical head", corner=UL, tag_corner=UR)
            pulse(snd, boxes[0], st["time"], st["level"] - 0.3, buff=0.06)
            pulse(snd, boxes[1], st["level"], st["both"] - 0.3, buff=0.06)
            pulse(snd, boxes[2], st["both"], c.duration, buff=0.06)
            pulse(snd, src, 0, c.duration, rate=5.0, color=GREY_B, buff=0.05)
        with self.voiceover(
            "Each cue alone moves the sound to the right, but not always to the same place, and often inside the head. "
            "Together they agree, and the sound sits more firmly out to the right. In real life the two never disagree, so the "
            "brain combines them."
        ):
            self.play(boxes[2][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cone(self):
        d = load("cone")
        hd = head_top(0.8, LEFT * 2.6 + DOWN * 0.1)
        c0 = hd[0].get_center()
        f30 = c0 + 2.3 * np.array([np.sin(np.radians(30)), np.cos(np.radians(30)), 0])
        b150 = c0 + 2.3 * np.array([np.sin(np.radians(150)), np.cos(np.radians(150)), 0])
        pts = VGroup(Dot(f30, radius=0.11, color=TUNE), Dot(b150, radius=0.11, color=EAR))
        pl = VGroup(label(r"30$^\circ$ in front", font_size=16, color=TUNE).next_to(pts[0], RIGHT, buff=0.1),
                    label(r"150$^\circ$ behind", font_size=16, color=EAR).next_to(pts[1], RIGHT, buff=0.1))
        axis = DashedLine(c0 + LEFT * 3.0, c0 + RIGHT * 2.8, color=GREY_D, stroke_width=1.5)
        cone_l = DashedLine(f30, b150, color=BLUE, stroke_width=2.5)
        al = label(r"the line through the ears", font_size=14, color=GREY_A).next_to(axis, DOWN, buff=0.1).shift(LEFT * 1.8)
        items = [
            (rf"both: \ ITD {d['itd_30_us']:.0f} $\mu$s", WHITE),
            (r"for a sphere, \ both: \ the same level differences", WHITE),
            (r"every point on a cone round the ears' axis gives the same cues: \ the cone of confusion", TUNE),
            (r"front against back; \ and up against down", GREY_A),
        ]
        rows = text_rows(items, font_size=20, width=6.0).move_to(RIGHT * 3.4 + DOWN * 0.1)
        head = label(r"the cone of confusion", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "But the two cues have a blind spot. <bookmark mark='a'/> Take a sound thirty degrees to the right in front, and "
            "one a hundred and fifty degrees to the right, behind: the mirror image across the line through the ears. "
            f"<bookmark mark='b'/> Both reach the right ear {say(d['itd_30_us'])} microseconds early. <bookmark mark='c'/> And "
            "for a sphere, both are shadowed identically. <bookmark mark='d'/> In fact every point on a cone around the ears' "
            "axis gives the same time and level differences: the cone of confusion. <bookmark mark='e'/> Front cannot be told "
            "from back, nor up from down, by these cues alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd), FadeIn(axis), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), Create(cone_l))
            for mark, r in zip("cde", rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cone")
        c = clip("cone.two")
        card = listen_card(r"Headphones on. \ A voice rendered round a spherical head, \ twice: \ once 30 degrees to the right in front, \ "
                           r"once 150 degrees to the right, \ behind. \ Which was in front?", width=10.0)
        with self.voiceover(
            "Your turn, with headphones. A voice rendered round Monochord's spherical head, twice: once thirty degrees to the "
            "right in front, once a hundred and fifty degrees to the right, behind. Which was in front?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"neither"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"front or back?", kind="rendered", detail=r"Part 8's voice, \ a spherical head", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
            pulse(snd, boxes[2], 0, c.duration, rate=5.0, color=GREY_B, buff=0.08)
        res = label(r"the first was in front; \ but the two are the same to the last sample: \ no listener can tell", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first was in front, but you could not have known: the two renderings are identical, sample for sample. With a "
            "spherical head, front and back give exactly the same signals. If you heard a difference, it came from what you "
            "expected. The honest answer was neither."
        ):
            self.play(boxes[2][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resolve(self):
        items = [
            (r"the outer ear, \ the pinna, \ is not a sphere: \ its folds reflect sound into notches that move with direction, \ above about 5 kHz", WHITE),
            (r"Batteau \ (1967) \ and Shaw: \ those spectral cues tell front from back and up from down", WHITE),
            (r"turn your head: \ a sound in front moves the other way from one behind \ (Wallach, \ 1940)", WHITE),
            (r"distance: \ level, \ the loss of treble, \ and above all the ratio of direct sound to reverberation", WHITE),
            (r"all of this, \ for one listener, \ is a pair of filters for each direction: \ the head-related transfer function", TUNE),
        ]
        rows_scene(self, r"breaking the cone", items,
                   "Real listeners break the cone in two ways. <bookmark mark='b'/> The outer ear, the pinna, is not a sphere: its "
                   "folds reflect sound into notches in the spectrum that move with direction, above about five kilohertz. "
                   "<bookmark mark='c'/> Wayne Batteau in 1967, and Edgar Shaw's measurements, showed that those spectral cues tell "
                   "front from back and up from down. <bookmark mark='d'/> And we turn our heads: a sound in front moves one way and "
                   "a sound behind the other, as Hans Wallach showed in 1940. <bookmark mark='e'/> Distance has cues of its own: "
                   "level, the loss of treble, and above all the ratio of direct sound to reverberation. <bookmark mark='f'/> All "
                   "of this, for one listener, is a pair of filters for every direction, one for each ear: the head-related "
                   "transfer function, which we will use in Chapter 9.", marks="bcdef")
