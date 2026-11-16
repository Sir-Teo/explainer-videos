from __future__ import annotations

import math

import numpy as np

from videos.music.music55.common import *  # noqa: F403


def phantom(p, law):
    """The tangent law's direction (degrees, positive to the right) for a pan position p from -1 to 1."""
    ratio = p if law == "linear" else math.tan(math.pi * p / 4)
    return math.degrees(math.atan(ratio * math.tan(math.radians(30))))


def speaker(at, angle_deg, color=GREY_B):
    b = Square(side_length=0.36, stroke_color=color, stroke_width=3).move_to(at)
    return b.rotate(-math.radians(angle_deg))


class Stereo(SoundScene):
    def construct(self):
        chapter(self, 7, r"Stereo and panning", r"How can two loudspeakers put a voice between them?")
        self.history()
        self.triangle()
        self.laws()
        self.heard()
        self.sweet()
        self.pairs()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1881: \ Clément Ader's théâtrophone: \ pairs of telephones along the stage of the Paris Opéra, \ one to each ear", WHITE),
            (r"1931: \ Alan Blumlein, \ at EMI, \ patents nearly all of stereo: \ crossed microphones, \ a two-channel groove, \ the shuffler", WHITE),
            (r"1933: \ Bell Labs relays the Philadelphia Orchestra to Washington over three channels: \ ``auditory perspective''", WHITE),
            (r"1958: \ the stereo LP, \ Blumlein's 45-degree groove; \ two loudspeakers became the standard", TUNE),
        ]
        rows_scene(self, r"two channels", items,
                   "Stereo is older than it seems. <bookmark mark='b'/> In 1881 Clément Ader laid pairs of telephone transmitters "
                   "along the stage of the Paris Opéra, and listeners across the city held one receiver to each ear. "
                   "<bookmark mark='c'/> In 1931 Alan Blumlein, an engineer at EMI, annoyed that a voice at the cinema came from the "
                   "wrong side of the screen, patented nearly all of stereo: crossed microphones, a two-channel groove, and a "
                   "circuit to make loudspeakers sound right. <bookmark mark='d'/> In 1933 Bell Labs relayed the Philadelphia "
                   "Orchestra to an audience in Washington over three channels, which they called auditory perspective. "
                   "<bookmark mark='e'/> And in 1958 came the stereo LP, cut with Blumlein's forty-five degree groove, and two "
                   "loudspeakers became the standard.", marks="bcde")

    # ------------------------------------------------------------------
    def triangle(self):
        d = load("pan")
        L0 = DOWN * 1.6
        R = 3.4
        spL = speaker(L0 + R * np.array([-math.sin(math.radians(30)), math.cos(math.radians(30)), 0]), -30)
        spR = speaker(L0 + R * np.array([math.sin(math.radians(30)), math.cos(math.radians(30)), 0]), 30)
        lis = Dot(L0, radius=0.12, color=WHITE)
        tri = VGroup(DashedLine(L0, spL.get_center(), color=GREY_D), DashedLine(L0, spR.get_center(), color=GREY_D), DashedLine(spL.get_center(), spR.get_center(), color=GREY_D))
        arc = Arc(radius=R, start_angle=math.radians(60), angle=math.radians(60), arc_center=L0, color=GREY_D, stroke_width=1.5)
        pans = [(-1.0, r"left"), (-0.5, r"half left"), (0.0, r"centre"), (0.5, r"half right"), (1.0, r"right")]
        ph = VGroup()
        for p, nm in pans:
            a = math.radians(phantom(p, "power"))
            ph.add(Dot(L0 + R * 0.88 * np.array([math.sin(a), math.cos(a), 0]), radius=0.09, color=TUNE))
        eq = MathTex(r"\frac{\tan\varphi}{\tan\varphi_0} = \frac{g_R - g_L}{g_R + g_L}", font_size=36, color=TUNE).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        vals = label(rf"constant-power pans: \ 0, \ {abs(d['phantom'][1]):.1f}$^\circ$ and 30$^\circ$ \ (centre, \ halfway, \ one side)", font_size=17, color=WHITE).next_to(eq, DOWN, buff=0.3)
        vals.scale_to_fit_width(min(vals.width, 4.6))
        head = label(r"the stereo triangle", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The standard is a triangle: two loudspeakers thirty degrees either side of the listener. <bookmark mark='a'/> Send "
            "a voice to both equally and you hear it in the middle, where there is no loudspeaker: a phantom image. Make one "
            "louder and the image moves towards it. <bookmark mark='b'/> Where to? At low frequencies the two loudspeakers' "
            "sounds add at each ear into a time difference, and the image follows the tangent law: the tangent of its angle, "
            "over the tangent of thirty degrees, is the difference of the gains over their sum. <bookmark mark='c'/> Pan halfway "
            f"with the usual law and the voice sits at {say(abs(d['phantom'][1]), 1)} degrees, not fifteen: images crowd towards "
            "the middle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(spL), FadeIn(spR), FadeIn(lis), FadeIn(tri), FadeIn(arc))
            vo.wait_until("a")
            self.play(FadeIn(ph[2]))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(ph[0]), FadeIn(ph[4]))
            vo.wait_until("c")
            self.play(FadeIn(ph[1]), FadeIn(ph[3]), FadeIn(vals))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        d = load("pan")
        p = np.array(d["p"])
        a1 = frame_axes(width=5.0, height=2.6, xlo=-1, xhi=1, ylo=0, yhi=1.05, center=LEFT * 3.3 + DOWN * 0.3)
        g = VGroup(curve(p, d["lin"][0], a1.to, color=GREY_A, width=3), curve(p, d["lin"][1], a1.to, color=GREY_A, width=3),
                   curve(p, d["pw"][0], a1.to, color=TUNE, width=3), curve(p, d["pw"][1], a1.to, color=TUNE, width=3))
        a2 = frame_axes(width=5.0, height=2.6, xlo=-1, xhi=1, ylo=-4, yhi=0.5, center=RIGHT * 3.3 + DOWN * 0.3)
        pw = VGroup(curve(p, d["lin_power_db"], a2.to, color=GREY_A, width=3), curve(p, d["pw_power_db"], a2.to, color=TUNE, width=3))
        t1 = label(r"the two gains", font_size=18, color=GREY_A).next_to(a1, UP, buff=0.2)
        t2 = label(r"squared-gain sum, \ dB", font_size=18, color=GREY_A).next_to(a2, UP, buff=0.2)
        xt = VGroup(*[VGroup(label(r"left", font_size=14, color=GREY_A).next_to(a.to(-1, a_lo), DOWN, buff=0.1), label(r"right", font_size=14, color=GREY_A).next_to(a.to(1, a_lo), DOWN, buff=0.1))
                      for a, a_lo in ((a1, 0), (a2, -4))])
        yt = VGroup(label(r"$-3$", font_size=14, color=GREY_A).next_to(a2.to(-1, -3), LEFT, buff=0.1), label(r"0", font_size=14, color=GREY_A).next_to(a2.to(-1, 0), LEFT, buff=0.1))
        key = VGroup(label(r"linear: \ $g_L = \frac{1-p}{2}$, \ $g_R = \frac{1+p}{2}$", font_size=17, color=GREY_A),
                     label(r"constant power: \ $g_L = \cos\frac{\pi(p+1)}{4}$, \ $g_R = \sin\frac{\pi(p+1)}{4}$", font_size=17, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.9)
        dip = min(d["lin_power_db"])
        head = label(r"pan laws", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"How should the gains change as a pan knob turns? <bookmark mark='a'/> The obvious way is linear: one gain falls as the other rises, always adding to one. <bookmark mark='b'/> But under a decorrelated or spatially averaged power model, we add squared gains; coherent loudspeaker signals also interfere, and in the middle the linear law's power is half: {say(-dip, 2)} decibels down, a hole in the middle. <bookmark mark='c'/> The constant-power law moves along a quarter circle instead, cosine and sine, so the sum of squared gains stays fixed. Mixing desks offer both, and compromises between them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(t1), FadeIn(t2), FadeIn(xt), FadeIn(yt), FadeIn(ghost(VGroup(g, pw), 0.25)))
            vo.wait_until("a")
            self.play(Create(g[0]), Create(g[1]), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(pw[0]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(g[2]), Create(g[3]), Create(pw[1]), FadeIn(key[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pan")
        c = clip("pan.two")
        L0 = DOWN * 1.9
        R = 3.2
        spL = speaker(L0 + R * np.array([-0.5, math.cos(math.radians(30)), 0]), -30)
        spR = speaker(L0 + R * np.array([0.5, math.cos(math.radians(30)), 0]), 30)
        lis = Dot(L0, radius=0.12, color=WHITE)
        img = Dot(L0 + R * 0.85 * np.array([-0.5, math.cos(math.radians(30)), 0]), radius=0.13, color=TUNE)
        boxes = choice_boxes([r"linear law", r"constant power"], width=3.0, height=0.8, buff=1.4, size=20).to_edge(UP, buff=1.0)
        head = label(r"a pan, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Hear the difference, with headphones: a voice panned slowly from the left loudspeaker to the right, by the linear "
            "law and then by constant power, the two loudspeakers rendered round a spherical head. Listen to the middle."
        ):
            self.play(FadeIn(head), FadeIn(spL), FadeIn(spR), FadeIn(lis), FadeIn(img), FadeIn(boxes))
        st = d["starts"]
        seg = st["power"] - 0.8

        def place(m, t):
            law = "linear" if t < st["power"] else "power"
            t0 = st["linear"] if law == "linear" else st["power"]
            p = float(np.clip(-1 + 2 * (t - t0) / seg, -1, 1))
            a = math.radians(phantom(p, law))
            m.move_to(L0 + R * 0.85 * np.array([math.sin(a), math.cos(a), 0]))

        with self.listen(c) as snd:
            window(snd, r"left to right, \ twice", kind="physical model", detail=r"Part 8's voice, \ two loudspeakers, \ a spherical head", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["linear"], st["power"] - 0.3, buff=0.06)
            pulse(snd, boxes[1], st["power"], c.duration, buff=0.06)
            snd.drive(img, place)
        with self.voiceover(
            'With the linear law the voice sinks as it crosses the middle, then comes back; constant-power gains preserve the squared-gain sum; perceived level can still vary with correlation, acoustics and listener position. Both cross the stage at the same pace, crowding a little towards the centre, as the tangent law predicts.'
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweet(self):
        items = [
            (r"the phantom image needs both loudspeakers to arrive together: \ the listener must sit on the centre line", WHITE),
            (r"move 60 cm to the left: \ the left loudspeaker's sound arrives about 1.7 ms sooner", WHITE),
            (r"by the precedence effect the first arrival wins: \ the voice jumps into the left loudspeaker", WHITE),
            (r"amplitude panning has a sweet spot; \ everyone else hears a different mix", TUNE),
            (r"stereo on headphones is another thing again: \ each ear hears one channel, \ and the image sits inside the head", GREY_A),
        ]
        rows_scene(self, r"the sweet spot", items,
                   "There is a catch. <bookmark mark='b'/> The phantom image needs the two loudspeakers' sounds to arrive "
                   "together, so the listener must sit on the centre line. <bookmark mark='c'/> Move sixty centimetres to the left, "
                   "and the left loudspeaker's sound arrives about one point seven milliseconds sooner. <bookmark mark='d'/> By the "
                   "precedence effect the first arrival wins, and the voice jumps into the left loudspeaker. "
                   "<bookmark mark='e'/> Amplitude panning has a sweet spot; everyone else in the room hears a different mix. "
                   "<bookmark mark='f'/> And stereo on headphones is another thing again: each ear hears only one channel, with no "
                   "crosstalk and no head in between, and the image sits on a line inside the head.", marks="bcdef")

    # ------------------------------------------------------------------
    def pairs(self):
        items = [
            (r"coincident pairs, \ XY and Blumlein's crossed figure-8s: \ one point in space, \ level differences only", WHITE),
            (r"spaced pairs, \ AB: \ omnis a metre or more apart, \ time differences, \ a wide and vague image", WHITE),
            (r"near-coincident, \ ORTF: \ two cardioids 17 cm apart at 110 degrees, \ a little of each", WHITE),
            (r"mid-side: \ a forward cardioid $M$ and a sideways figure-8 $S$; \ left $= M + S$, \ right $= M - S$: \ the width is a knob", TUNE),
            (r"Part 56 computes how each pair maps a stage onto the stereo triangle", GREY_A),
        ]
        rows_scene(self, r"microphones for stereo", items,
                   "Stereo also has to be recorded. <bookmark mark='b'/> Coincident pairs, two cardioids crossed in XY, or Blumlein's "
                   "crossed figure-8s, put both capsules at one point in space, so they make level differences only. "
                   "<bookmark mark='c'/> Spaced pairs, AB, are omnis a metre or more apart, making time differences, with a wide "
                   "and vaguer image. <bookmark mark='d'/> Near-coincident pairs, like French radio's ORTF, two cardioids seventeen "
                   "centimetres apart at a hundred and ten degrees, make a little of each. <bookmark mark='e'/> And mid-side, also "
                   "Blumlein's, puts a forward cardioid M with a sideways figure-8 S: left is M plus S, right is M minus S, and the "
                   "width of the image becomes a knob. <bookmark mark='f'/> Part 56 computes how each pair maps a stage onto the "
                   "stereo triangle.", marks="bcdef")
