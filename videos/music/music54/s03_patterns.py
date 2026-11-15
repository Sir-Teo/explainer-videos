from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403

PCOL = {"omni": GREY_A, "cardioid": TUNE, "supercardioid": BLUE, "hypercardioid": "#A3E635", "figure-8": EAR}


def polar(r, sign, R=1.0, color=TUNE):
    th = np.linspace(0, 2 * np.pi, len(r))
    pts = [np.array([R * a * np.sin(t), R * a * np.cos(t), 0]) for a, t in zip(r, th)]
    g = VGroup(Circle(radius=R, stroke_color=GREY_D, stroke_width=1), Line(DOWN * R, UP * R, color=GREY_D, stroke_width=1), Line(LEFT * R, RIGHT * R, color=GREY_D, stroke_width=1))
    g.add(VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts))
    return g


class Patterns(SoundScene):
    def construct(self):
        chapter(self, 2, r"Polar patterns", r"Why does a microphone hear some directions and not others?")
        self.two()
        self.family()
        self.walk()
        self.table()
        self.highs()
        self.quiz()
        self.choosing()

    # ------------------------------------------------------------------
    def two(self):
        items = [
            (r"a pressure microphone: \ a diaphragm closed at the back; \ pressure is the same from every direction: \ omnidirectional", WHITE),
            (r"a pressure-gradient microphone: \ open at both sides; \ it feels the difference between front and back", WHITE),
            (r"a wave from the side reaches both sides at once: \ no difference, \ no output: \ the figure-8, \ $\cos\theta$", WHITE),
            (r"add the two and the front adds while the back cancels: \ the cardioid, \ $\frac{1}{2}(1 + \cos\theta)$", TUNE),
            (r"mix them in other proportions and you get the whole family", GREY_A),
        ]
        rows_scene(self, r"pressure and its gradient", items,
                   "Direction comes from how the diaphragm meets the air. <bookmark mark='b'/> A pressure microphone's diaphragm is "
                   "closed at the back, and pressure is the same whichever way the sound comes from: it is omnidirectional. "
                   "<bookmark mark='c'/> A pressure-gradient microphone is open on both sides and feels the difference between front "
                   "and back. <bookmark mark='d'/> A wave from the side reaches both sides at once, so there is no difference and no "
                   "output: the figure-8, cosine theta. <bookmark mark='e'/> Add the two, and at the front they add while at the back "
                   "they cancel: the cardioid, a half of one plus cosine theta. <bookmark mark='f'/> Mix them in other proportions "
                   "and you get the whole family.", marks="bcdef")

    # ------------------------------------------------------------------
    def family(self):
        d = load("patterns")
        names = ["omni", "cardioid", "supercardioid", "hypercardioid", "figure-8"]
        cells = VGroup()
        for k in names:
            p = polar(np.array(d[k]["r"]), np.array(d[k]["sign"]), R=1.0, color=PCOL[k])
            cells.add(VGroup(p, label(k, font_size=17, color=PCOL[k]), label(rf"$A = {[1, 0.5, 0.366, 0.25, 0][names.index(k)]:g}$", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.2)
        eq = MathTex(r"r(\theta) = A + (1 - A)\cos\theta", font_size=36).to_edge(UP, buff=1.0)
        front = label(r"the front is up", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"the first-order family", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the family, r of theta equals A plus one minus A cosine theta, with the front at the top. "
            "<bookmark mark='a'/> A equals one: the omni, a circle. <bookmark mark='b'/> A half: the cardioid, the heart, with "
            "a null straight behind. <bookmark mark='c'/> Less pressure and more gradient: the supercardioid and the "
            "hypercardioid, narrower at the front, with a small lobe behind and two nulls off to the sides. "
            "<bookmark mark='d'/> And A zero: the figure-8, as loud behind as in front, deaf at the sides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(front), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]))
            vo.wait_until("c")
            self.play(FadeIn(cells[2]), FadeIn(cells[3]))
            vo.wait_until("d")
            self.play(FadeIn(cells[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("patterns")
        rows = VGroup(VGroup(label(r"pattern", font_size=17, color=GREY_A), label(r"directivity index", font_size=17, color=GREY_A),
                             label(r"distance factor", font_size=17, color=GREY_A), label(r"null", font_size=17, color=GREY_A)))
        for k in ("omni", "cardioid", "supercardioid", "hypercardioid", "figure-8"):
            v = d[k]
            rows.add(VGroup(label(k, font_size=19, color=PCOL[k]), label(rf"{v['DI']:.1f} dB", font_size=19, color=WHITE), label(rf"{v['distance']:.2f}", font_size=19, color=WHITE),
                            label(rf"{v['null_deg']:.0f}$^\circ$" if v["null_deg"] else r"none", font_size=19, color=WHITE)))
        rows.arrange(DOWN, buff=0.25)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.2 + 2.9 * i)
        rows.move_to(DOWN * 0.1)
        note = label(r"the hypercardioid is the most directional of the family: \ 6.0 dB, \ twice an omni's distance", font_size=18, color=TUNE).to_edge(DOWN, buff=0.4)
        head = label(r"how directional?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How directional is each? <bookmark mark='a'/> Average a pattern's squared response over every direction: that is "
            "how much of a room's reverberation it picks up. Its reciprocal is the directivity factor, and in decibels the "
            "directivity index. The cardioid and the figure-8 both reach four point eight decibels, rejecting two thirds of the "
            "room. <bookmark mark='b'/> The hypercardioid is the most directional of the family, six decibels: it can stand "
            "twice as far from a singer as an omni and hear the same balance of voice and room. And the nulls tell you where to "
            "put what you do not want to hear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("capture")
        c = clip("capture.three")
        card = listen_card(r"A singer in front of the microphone, \ a piano behind the singer and a little to one side, \ in a lively room. \ "
                           r"Three microphones: \ an omni, \ a cardioid, \ a figure-8, \ in some order. \ Which heard the least piano?", width=10.4)
        with self.voiceover(
            "Your turn. A singer in front of the microphone, a piano behind and a little to one side, in a lively room. Three "
            "microphones, an omni, a cardioid and a figure-8, in some order. Which heard the least piano?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        names = ["omni", "cardioid", "figure-8"]
        with self.listen(c) as snd:
            window(snd, r"three microphones", kind="physical model", detail=r"voice, \ piano, \ room", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = VGroup(label(r"first: \ omni: \ the piano at full strength, \ the most room", font_size=18, color=GREY_A),
                     label(rf"second: \ cardioid: \ the piano {-d['cardioid']['rear_db']:.0f} dB down, \ near its null", font_size=18, color=TUNE),
                     label(r"third: \ figure-8: \ the piano almost as loud as in front, \ but less room", font_size=18, color=EAR)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The second, the cardioid: the piano sits near its rear null, {say(-d['cardioid']['rear_db'])} decibels down. The "
            "omni hears it at full strength along with the most room; the figure-8 hears it almost as loud as the singer, "
            "because its back is as live as its front, though it takes in less of the room."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choosing(self):
        items = [
            (r"on stage: \ cardioids and supercardioids, \ their nulls aimed at the monitor loudspeakers", WHITE),
            (r"in a good room: \ omnis, \ for the room's sound as well as the source's", WHITE),
            (r"stereo pairs: \ two figure-8s crossed at 90 degrees \ (Blumlein, \ 1931) \ capture direction itself", WHITE),
            (r"real microphones are only first-order at low frequencies; \ at high ones the body and diaphragm narrow them", WHITE),
            (r"and a gradient microphone close to a source is not even flat", TUNE),
        ]
        rows_scene(self, r"choosing a pattern", items,
                   "Patterns are chosen for the job. <bookmark mark='b'/> On stage, cardioids and supercardioids, with their nulls "
                   "aimed at the monitor loudspeakers. <bookmark mark='c'/> In a good room, omnis, for the room's sound as well as "
                   "the source's. <bookmark mark='d'/> For stereo, two figure-8s crossed at ninety degrees, Alan Blumlein's pair of "
                   "1931, capture direction itself. <bookmark mark='e'/> Real microphones follow the first-order family only at low "
                   "frequencies; at high ones the body and diaphragm narrow them. <bookmark mark='f'/> And a gradient microphone "
                   "close to its source is not even flat.", marks="bcdef")

    # ------------------------------------------------------------------
    def highs(self):
        items = [
            (r"the first-order family assumes the microphone is small next to the wavelength", WHITE),
            (r"a 25 mm diaphragm is a quarter of a wavelength at about 3.4 kHz", WHITE),
            (r"above that, \ even an omni narrows towards the front, \ and sound from the side loses its treble", WHITE),
            (r"so off-axis sound is duller: \ a pattern is a family of patterns, \ one per frequency", TUNE),
            (r"small-diaphragm microphones keep their pattern higher; \ large ones colour the room", GREY_A),
        ]
        rows_scene(self, r"patterns at high frequencies", items,
                   "Real patterns change with frequency. <bookmark mark='b'/> The first-order family assumes the microphone is small next to the wavelength. <bookmark mark='c'/> A twenty-five millimetre diaphragm is a quarter of a wavelength at about three point four kilohertz, <bookmark mark='d'/> and above that even an omni narrows towards the front, so sound from the side loses its treble. <bookmark mark='e'/> Off-axis sound is duller: a pattern is really a family of patterns, one per frequency. <bookmark mark='f'/> Small-diaphragm microphones keep their pattern higher; large ones colour the room.", marks="bcdef")

    # ------------------------------------------------------------------
    def walk(self):
        d = load("patterns")
        c = clip("rotate.one")
        p = polar(np.array(d["cardioid"]["r"]), np.array(d["cardioid"]["sign"]), R=1.8, color=TUNE).move_to(DOWN * 0.3)
        mic = Dot(p.get_center(), radius=0.08, color=WHITE)
        singer = Dot(p.get_center() + UP * 2.4, radius=0.14, color=EAR)
        cap = label(r"a singer walking once round a cardioid, \ starting in front", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"round the cardioid, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear a cardioid's pattern directly: a singer walking once round it, starting in front."):
            self.play(FadeIn(head), FadeIn(p), FadeIn(mic), FadeIn(singer), FadeIn(cap))
        secs = load("rotate")["seconds"]
        centre = p.get_center()
        with self.listen(c) as snd:
            window(snd, r"a walk round the microphone", kind="physical model", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            snd.drive(singer, lambda m, t: m.move_to(centre + 2.4 * np.array([np.sin(2 * np.pi * t / secs), np.cos(2 * np.pi * t / secs), 0])))
        with self.voiceover(
            "The voice fades as the singer passes the side, all but vanishes behind, at the null, and returns as the singer "
            "comes round to the front: the heart shape, heard."
        ):
            self.play(Indicate(p, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
