from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


def box(text, color=GREY_B, w=2.2, h=0.8, size=17):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.5), label(text, font_size=size, color=color))


class Feedback(SoundScene):
    def construct(self):
        chapter(self, 1, r"Why a microphone howls", r"Can you predict the note a system will howl at?")
        self.loop()
        self.nyquist()
        self.response()
        self.quiz()
        self.howl()

    # ------------------------------------------------------------------
    def loop(self):
        mic = box(r"microphone")
        amp = box(r"amplifier, \ gain $G$", TUNE)
        spk = box(r"loudspeaker")
        room = box(r"the hall: \ $H(f)$", BLUE, w=3.0)
        g = VGroup(mic, amp, spk).arrange(RIGHT, buff=1.0).move_to(UP * 1.0)
        room.move_to(DOWN * 0.9)
        arrs = VGroup(Arrow(mic.get_right(), amp.get_left(), buff=0.05, color=GREY_B), Arrow(amp.get_right(), spk.get_left(), buff=0.05, color=GREY_B),
                      CurvedArrow(spk.get_bottom(), room.get_right(), color=BLUE, angle=-1.2), CurvedArrow(room.get_left(), mic.get_bottom(), color=BLUE, angle=-1.2))
        src = label(r"a voice, \ $x$", font_size=17, color=EAR).next_to(mic, UP, buff=0.3)
        eq = MathTex(r"y = x + G H\,y \quad\Rightarrow\quad y = \frac{x}{1 - G H(f)}", font_size=36, color=TUNE).to_edge(DOWN, buff=0.6)
        head = label(r"a loop", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "On a stage the microphone hears the loudspeaker. <bookmark mark='a'/> A voice goes into the microphone, through "
            "the amplifier's gain G, out of the loudspeaker, <bookmark mark='b'/> round the hall, whose response H includes "
            "every reflection, and back into the microphone, where it joins the voice and goes round again. "
            "<bookmark mark='c'/> The microphone's signal is the voice divided by one minus G H. When G H approaches one, the "
            "denominator approaches nothing, and the system rings; when it passes one, every trip round the loop is louder "
            "than the last, and the system howls."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(room), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]))
            vo.wait_until("b")
            self.play(Create(arrs[2]), Create(arrs[3]))
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nyquist(self):
        items = [
            (r"$G H(f)$ is complex: \ a gain and a phase at every frequency", WHITE),
            (r"the loop runs away where the returning sound arrives in step with what is already there: \ phase a whole number of cycles", WHITE),
            (r"and is louder than it: \ $|G H| \ge 1$; \ together, \ $G H(f)$ reaches $+1$ on the real axis", WHITE),
            (r"Nyquist \ (1932): \ as $G$ grows, \ the first frequency to go is the one where $H$'s real part is largest", TUNE),
            (r"the gain before feedback: \ $G_{\max} = 1 / \max_f \operatorname{Re} H(f)$; \ the howl: \ that frequency", TUNE),
        ]
        rows_scene(self, r"when a loop runs away", items,
                   "When exactly does it run away? <bookmark mark='b'/> G H is complex: a gain and a phase at every frequency. "
                   "<bookmark mark='c'/> The loop runs away where the returning sound arrives in step with what is already there, "
                   "its phase a whole number of cycles, <bookmark mark='d'/> and louder than it: together, G H reaches plus one on "
                   "the real axis. <bookmark mark='e'/> Harry Nyquist's criterion of 1932 follows: as the gain grows, the first "
                   "frequency to go is the one where H's real part is largest. <bookmark mark='f'/> So the gain before feedback is "
                   "one over the largest real part of H, and the howl is at that frequency.", marks="bcdef")

    # ------------------------------------------------------------------
    def response(self):
        d = load("feedback")
        f = np.array(d["zoom_f"])
        mag = np.array(d["zoom_mag"])
        re = np.array(d["zoom_re"])
        top = max(np.array(d["mag_db"]))
        ax = frame_axes(width=10.0, height=3.2, xlo=250, xhi=500, ylo=-40, yhi=2, center=DOWN * 0.4)
        xt = VGroup(*[label(f"{v} Hz", font_size=14, color=GREY_A).next_to(ax.to(v, -40), DOWN, buff=0.1) for v in (250, 300, 350, 400, 450, 500)])
        cm = VMobject(stroke_color=GREY_B, stroke_width=1.2).set_points_as_corners([ax.to(x, max(v - top, -40)) for x, v in zip(f, mag)])
        cr = VMobject(stroke_color=TUNE, stroke_width=1.5).set_points_as_corners([ax.to(x, max(v - top, -40)) for x, v in zip(f, re)])
        hz = d["howl_hz"]
        mark = VGroup(DashedLine(ax.to(hz, -40), ax.to(hz, 2), color=EAR, stroke_width=2), label(rf"{hz:.0f} Hz", font_size=16, color=EAR).next_to(ax.to(hz, 2), UP, buff=0.05))
        key = VGroup(label(r"$|H|$: \ the hall, \ loudspeaker to microphone", font_size=16, color=GREY_B), label(r"the real part of $H$", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(rf"a 20 by 14 by 8 m hall, \ the loudspeaker 5 m from the microphone: \ gain before feedback {d['max_gain_db']:.1f} dB \ (re the loop's peak path)", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"the loop's response", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a real-sized case: a hall twenty by fourteen by eight metres, simulated by Part 49's image method, with "
            "the loudspeaker five metres from the microphone. <bookmark mark='a'/> The hall's response from "
            "loudspeaker to microphone, shown here between two hundred and fifty and five hundred hertz, is a forest of peaks, "
            "one every few hertz, from all the reflections; across the whole range there are thousands. "
            "<bookmark mark='b'/> Its real part picks out where the phase comes round. <bookmark mark='c'/> The highest point "
            f"of the real part is at {say(hz)} hertz: that is the note this system will howl at, first, as the gain is raised."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(note), FadeIn(ghost(VGroup(cm, cr), 0.25)))
            vo.wait_until("a")
            self.play(Create(cm), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cr), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(mark))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("feedback")
        c = clip("feedback.three")
        card = listen_card(r"A clap into the microphone, \ three times, \ at three gains below the edge of feedback, \ in some order. "
                           r"\ Which was closest to howling?", width=10.0)
        with self.voiceover("Your turn. A clap into this microphone, three times, at three gains below the edge of feedback, in some order. Which was closest to howling?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three gains", kind="physical model", detail=r"a simulated hall and loop", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], st["third"] - 0.4, buff=0.08)
            pulse(snd, boxes[2], st["third"], c.duration, buff=0.08)
        res = label(rf"the second: \ 0.5 dB from the edge; \ it rings on at {d['howl_hz']:.0f} Hz \ (the first was 6 dB down, \ the third 2)", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The second, half a decibel from the edge: after the clap it rings on, a tone at {say(d['howl_hz'])} hertz that "
            "dies only slowly. Engineers call it a system ready to feed back. Six decibels down, the clap simply stops."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def howl(self):
        d = load("feedback")
        c = clip("feedback.howl")
        lab_ = VGroup(label(r"predicted by Nyquist's criterion", font_size=20, color=GREY_A), label(rf"{d['howl_hz']:.0f} Hz", font_size=40, color=TUNE),
                      label(r"found by running the loop", font_size=20, color=GREY_A), label(rf"{d['found_hz']:.0f} Hz", font_size=40, color=EAR)).arrange(DOWN, buff=0.25).move_to(UP * 0.3)
        head = label(r"over the edge", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Now a voice into the same loop with the gain six tenths of a decibel past the edge."):
            self.play(FadeIn(head), FadeIn(lab_[:2]))
        with self.listen(c) as snd:
            window(snd, r"a howl", kind="physical model", detail=r"Part 8's voice, \ the loop", corner=DL, tag_corner=DR)
            pulse(snd, lab_[1], 0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
        with self.voiceover(
            "The voice is swallowed by a rising whistle. Measured from the last second of the recording, it is at "
            f"{say(d['found_hz'])} hertz, the frequency predicted from the loop's real part before anything was played."
        ):
            self.play(FadeIn(lab_[2:]))
        self.wait(0.4)
        self.clear_scene()
