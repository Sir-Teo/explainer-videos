from __future__ import annotations

from videos.music.music59.common import *  # noqa: F403


class RingOut(SoundScene):
    def construct(self):
        chapter(self, 2, r"Ringing out, \ and monitors", r"How do engineers buy a few more decibels before the howl?")
        self.notches()
        self.heard()
        self.geometry()
        self.pag()
        self.monitors()

    # ------------------------------------------------------------------
    def notches(self):
        d = load("feedback")
        rows = VGroup(VGroup(label(r"notches", font_size=17, color=GREY_A), label(r"cut at", font_size=17, color=GREY_A), label(r"gain before feedback", font_size=17, color=GREY_A),
                             label(r"next to howl", font_size=17, color=GREY_A)))
        base = d["ringout"][0]["max_gain_db"]
        for r in d["ringout"]:
            col = TUNE if r["notches"] else WHITE
            rows.add(VGroup(label(str(r["notches"]), font_size=18, color=col), label(f"{r['cut_hz']:.0f} Hz" if r["notches"] else r"--", font_size=18, color=WHITE),
                            label(rf"+{r['max_gain_db'] - base:.1f} dB" if r["notches"] else r"0 dB", font_size=18, color=col), label(f"{r['howl_hz']:.0f} Hz", font_size=18, color=WHITE)))
        rows.arrange(DOWN, buff=0.22)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.0 * i)
        rows.move_to(DOWN * 0.1)
        gain = d["ringout"][-1]["max_gain_db"] - base
        note = label(rf"six narrow notches \ (9 dB, \ Q 10) \ buy {gain:.1f} dB; \ each one exposes the next peak, \ only a little lower", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"ringing out", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Before a show, engineers ring out the system. <bookmark mark='a'/> Raise the gain until it starts to ring, find "
            "the frequency, cut it with a narrow notch, and raise the gain again until the next one rings. Here is Monochord "
            "doing that with the loop's response: the first notch goes at the predicted frequency, and each notch exposes "
            f"the next peak. <bookmark mark='b'/> Six notches buy {say(gain, 1)} decibels. A hall with thousands of nearly equal "
            "peaks gives up only a few; more than that, and the notches start to colour the voice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("feedback")
        c = clip("feedback.ringout")
        boxes = choice_boxes([r"before ringing out", r"after six notches"], width=3.4, height=0.9, buff=1.0, size=20).move_to(UP * 0.4)
        note = label(r"the same voice at the same gain, \ 0.5 dB under the original edge", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"ringing out, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the same voice at the same gain, half a decibel under the original edge: before ringing out, and after the six notches."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts_ro"]
        with self.listen(c) as snd:
            window(snd, r"before, \ then after", kind="physical model", detail=r"Part 8's voice, \ the loop", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["before"], st["after"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["after"], c.duration, buff=0.08)
        with self.voiceover("Before, every note leaves a ringing tail; after, the voice is clean, with nearly four decibels in hand."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        items = [
            (r"move the microphone closer to the source: \ every halving of the distance is 6 dB more voice for the same loop", WHITE),
            (r"aim the microphone's null at the loudspeaker: \ a cardioid's rear, \ a supercardioid's side nulls \ (Part 54)", WHITE),
            (r"keep loudspeakers in front of the microphones, \ and aimed away from them", WHITE),
            (r"use fewer open microphones: \ each one adds its own loop \ (10 log of the number)", WHITE),
            (r"geometry first, \ notches last", TUNE),
        ]
        rows_scene(self, r"the cheaper decibels", items,
                   "The cheaper decibels come from geometry. <bookmark mark='b'/> Move the microphone closer to the source: every "
                   "halving of the distance is six decibels more voice for the same loop. <bookmark mark='c'/> Aim the microphone's "
                   "null at the loudspeaker, a cardioid's rear or a supercardioid's side nulls, from Part 54. "
                   "<bookmark mark='d'/> Keep loudspeakers in front of the microphones and aimed away from them. "
                   "<bookmark mark='e'/> And keep few microphones open, since each adds its own loop. <bookmark mark='f'/> Geometry "
                   "first, notches last.", marks="bcdef")

    # ------------------------------------------------------------------
    def pag(self):
        d = load("feedback")["pag"]
        eq = MathTex(r"\text{PAG} = 20\log_{10}\frac{D_0\,D_1}{D_s\,D_2} - 10\log_{10}\text{NOM} - \text{FSM}", font_size=36, color=TUNE).move_to(UP * 1.4)
        items = [
            (r"Don and Carolyn Davis's potential acoustic gain \ (1970s): \ inverse-square distances only", WHITE),
            (r"$D_0$ talker to listener 20 m, \ $D_1$ microphone to loudspeaker 6 m, \ $D_s$ talker to microphone 0.3 m, \ $D_2$ loudspeaker to listener 12 m; \ one microphone, \ 6 dB margin", WHITE),
            (rf"PAG = {d['pag']:.1f} dB; \ to sound as if 1 m away, \ the listener needs {d['nag']:.1f} dB: \ not quite enough", WHITE),
            (r"halve $D_s$ \ (the microphone to 15 cm): \ 6 dB more, \ and 4.5 dB to spare", TUNE),
        ]
        rows = text_rows(items, font_size=20).move_to(DOWN * 0.9)
        head = label(r"potential acoustic gain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "System designers put the geometry into one formula. <bookmark mark='a'/> Don and Carolyn Davis's potential "
            "acoustic gain, from the 1970s, uses only the inverse-square law. <bookmark mark='b'/> Take a talker twenty metres "
            "from the listener, the microphone six metres from the loudspeaker, the talker thirty centimetres from the "
            "microphone, the loudspeaker twelve metres from the listener, one open microphone and six decibels of safety. "
            f"<bookmark mark='c'/> The potential gain is {say(d['pag'], 1)} decibels; to sound as if the talker were a metre "
            f"away the listener needs {say(d['nag'], 1)}: not quite enough. <bookmark mark='d'/> Bring the microphone to fifteen "
            "centimetres, six decibels more, and there are four and a half to spare."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monitors(self):
        items = [
            (r"the musicians need their own mix: \ wedges on the floor, \ aimed up at them", WHITE),
            (r"wedges are loudspeakers aimed at the microphones' backs: \ cardioids put the wedge in their null", WHITE),
            (r"a loud stage leaks into every microphone and the front-of-house mix", WHITE),
            (r"in-ear monitors \ (1990s on): \ each musician's mix in earphones, \ no loop at all, \ and a quieter stage", WHITE),
            (r"the cost: \ isolation from the room and the audience, \ restored with ambient microphones", TUNE),
        ]
        rows_scene(self, r"monitors", items,
                   "And the musicians need to hear themselves, the problem of Shea Stadium. <bookmark mark='b'/> Wedges on the floor, "
                   "aimed up at each player, give each a mix of their own. <bookmark mark='c'/> They are loudspeakers aimed at the "
                   "backs of the microphones, which is why stage microphones are cardioids with the wedge in their null. "
                   "<bookmark mark='d'/> And a loud stage leaks into every microphone and into the front-of-house mix. "
                   "<bookmark mark='e'/> From the 1990s, in-ear monitors put each musician's mix in earphones: no loop at all, and a "
                   "quieter stage. <bookmark mark='f'/> Their cost is isolation from the room and the audience, which engineers "
                   "restore with ambient microphones.", marks="bcdef")
