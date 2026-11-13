from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Box(SoundScene):
    def construct(self):
        chapter(self, 1, r"A string cannot be heard", r"Why does a string need a box?", lit=(1877,), extra=((1877, r"Rayleigh's \textit{Theory of Sound}"),))
        self.thin()
        self.pair()
        self.tap()

    # ------------------------------------------------------------------
    def thin(self):
        s = StringView(width=9.0).move_to(UP * 2.3)
        thin = label(r"a string is a millimetre wide: \ the air slips round it", font_size=28, color=GREY_A).next_to(s, DOWN, buff=0.3)
        plate = Rectangle(width=6.0, height=0.14, stroke_width=0, fill_color=WOOD, fill_opacity=0.9).move_to(DOWN * 0.9)
        bridge = Polygon([-0.25, 0, 0], [0.25, 0, 0], [0.12, 0.45, 0], [-0.12, 0.45, 0], stroke_width=0, fill_color=WOOD, fill_opacity=1).next_to(plate, UP, buff=0)
        string2 = Line(LEFT * 3.4 + UP * 0.02, RIGHT * 3.4 + UP * 0.02, color=STR, stroke_width=3).next_to(bridge, UP, buff=0).shift(DOWN * 0.02)
        waves = VGroup(*[Arc(radius=r, start_angle=PI + 0.5, angle=PI - 1.0, color=AIR, stroke_width=3).move_to(plate.get_center() + DOWN * (0.25 + 0.5 * r)) for r in (0.8, 1.4, 2.0)])
        names = VGroup(label(r"bridge", font_size=22, color=GREY_B).next_to(bridge, RIGHT, buff=0.5).shift(UP * 0.1), label(r"a wide, \ thin plate", font_size=22, color=WOOD).next_to(plate, RIGHT, buff=0.25))
        trade = VGroup(label(r"the string's force on the bridge drives the plate; \ the plate drives the air", font_size=28, color=AIR),
                       label(r"a box that takes the string's energy quickly is loud, \ and brief; \ slowly, \ quiet and long", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is something we have been ignoring for six parts. A string by itself is almost silent. It is "
            "a millimetre wide. When it moves, the air in front of it simply slips round to the back, and "
            "hardly any sound is launched. Stretch a guitar string between two nails in a brick wall, pluck it, "
            "and you will barely hear it. <bookmark mark='a'/> So every string instrument does the same thing. "
            "The string passes over a bridge, the bridge stands on a wide thin plate of wood, and the plate, "
            "which is big enough to push on the air properly, does the talking. What the plate feels is the "
            "force of the string on the bridge. That force is what Monochord has been computing all along. "
            "<bookmark mark='b'/> And there is a bargain to be struck, the one from Part 2. A plate that takes "
            "the string's energy quickly makes a loud sound that is over soon: that is a banjo. A solid plank "
            "that takes almost none leaves the string ringing for a long time, very quietly: that is an "
            "electric guitar, which needs an amplifier. Every instrument maker chooses a point between the two."
        ) as vo:
            self.play(FadeIn(s), FadeIn(thin))
            vo.wait_until("a")
            self.play(FadeIn(plate), FadeIn(bridge), FadeIn(string2), FadeIn(names), LaggedStart(*[Create(w) for w in waves], lag_ratio=0.3), FadeIn(trade[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(trade[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pair(self):
        d = load("body")
        c = clip("body.pair")
        q = listen_card(r"One plucked note, \ twice. \ A is the force on the bridge, \ as we have always played it. \\ B is the same force through a guitar's body. \ What has the body done?",
                        width=10.4, font_size=26).to_edge(UP, buff=0.35)
        g = axes([0, 3000], [-70, 5], x_length=9.6, y_length=3.0, xlabel=r"frequency (Hz)", ylabel=r"level (dB)", xticks=[0, 500, 1000, 1500, 2000, 2500, 3000], yticks=[-60, -40, -20, 0], font_size=20)
        g.move_to(DOWN * 1.2)
        bare = curve_from(g, d["spec_f"], np.maximum(d["spec_bare"] - d["spec_bare"].max(), -70), GREY_B, stroke_width=2.5)
        body = curve_from(g, d["spec_f"], np.maximum(d["spec_body"] - d["spec_body"].max(), -70), WOOD, stroke_width=2.5)
        leg = VGroup(label(r"A: \ the bare force", font_size=24, color=GREY_B), label(r"B: \ through the body", font_size=24, color=WOOD)).arrange(RIGHT, buff=0.8).next_to(g, UP, buff=0.1).shift(RIGHT * 1.5)
        with self.voiceover(
            "So what does a box do to a sound? Listen. One plucked note, an A on a guitar's fifth string. First "
            "the bare force on the bridge, the way we have always played it. Then exactly the same force, "
            "passed through Monochord's model of a guitar body."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(leg))
        self.add(bare, body)
        bare.set_stroke(opacity=0.15)
        body.set_stroke(opacity=0.15)
        with self.listen(c) as snd:
            window(snd, r"a plucked A: \ bare, \ then through the body", detail=r"a model guitar", corner=DL, tag_corner=DR)
            tb = snd.time_of("body")
            snd.drive(bare, lambda m, t: m.set_stroke(opacity=(0.75 + 0.25 * np.sin(16 * t)) if t < tb - 0.4 else 0.2))
            snd.drive(body, lambda m, t: m.set_stroke(opacity=(0.75 + 0.25 * np.sin(16 * t)) if t >= tb else 0.15))
        bare.set_stroke(opacity=0.8)
        body.set_stroke(opacity=1)
        with self.voiceover(
            "The bare force is thin and wiry, almost electric. Through the body the same note is rounder and "
            "warmer, with a soft thump at the start. <bookmark mark='a'/> The picture shows why. The string "
            "offers the same row of partials both times. The body does not pass them equally. It has "
            "resonances of its own, and a partial that falls on one comes out strong, while one that falls "
            "between two comes out weak. A body is a filter, and a fixed one: its peaks stay where they are "
            "whatever note is played. That is the difference between the timbre of a string and the timbre of "
            "an instrument."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(Indicate(body, color=WHITE, scale_factor=1.0), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tap(self):
        d = load("body")
        c = clip("body.tap")
        g = faxes(60, 6000, [-25, 32], x_length=10.4, y_length=3.4, ylabel=r"how strongly the body answers (dB)", yticks=[-20, 0, 20], fticks=(100, 200, 500, 1000, 2000, 5000), font_size=20)
        g.move_to(DOWN * 0.3)
        cu = fcurve(g, d["f"], d["response"], WOOD)
        marks = VGroup(*[Dot(g.at(hz, float(np.interp(hz, d["f"], d["response"]))), radius=0.06, color=TUNE) for hz, _ in d["modes"][:6]])
        head = label(r"the body's own sound: \ a knock on the bridge", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "You can hear a body's resonances without any string at all. Knock on the bridge of a guitar with a "
            "knuckle. Here is that knock on our model, twice."
        ):
            self.play(FadeIn(head), FadeIn(g), Create(cu), run_time=1.5)
        with self.listen(c) as snd:
            window(snd, r"two knocks on the bridge", detail=r"a model guitar", corner=DL, tag_corner=DR)
            snd.show(marks)
            for ev in ("t1", "t2"):
                t0 = snd.time_of(ev)
                snd.drive(cu, lambda m, t, t0=t0: m.set_stroke(width=3 + 5 * float(np.exp(-6 * (t - t0)))) if t >= t0 else m)
            snd.drive(marks, lambda m, t: m.set_opacity(0.5 + 0.5 * abs(np.sin(14 * t))))
        cu.set_stroke(width=3)
        note = VGroup(label(r"a low, \ dull thud with a pitch: \ the two lowest peaks, \ near 100 and 200 Hz", font_size=26, color=TUNE),
                      label(r"makers tap plates and listen: \ this curve is what they are tuning", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A soft thud, with a pitch you could almost sing: somewhere near the G at the bottom of a man's "
            "voice. That pitch belongs to the two lowest peaks of this curve, near a hundred and near two "
            "hundred hertz. Every guitar has that pair. Guitar makers and violin makers have always tapped "
            "their plates and listened as they carve; this curve is what they are tuning by ear. So where does "
            "that pair of peaks come from? From something we have already built."
        ):
            self.play(FadeIn(marks), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
