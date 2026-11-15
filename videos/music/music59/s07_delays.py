from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Delays(SoundScene):
    def construct(self):
        chapter(self, 6, r"Delay towers, \ air and weather", r"Why does a festival's back field hear the stage twice?")
        self.towers()
        self.quiz()
        self.weather()
        self.air()
        self.air_heard()

    # ------------------------------------------------------------------
    def towers(self):
        d = load("delay")
        stage = Rectangle(width=0.5, height=1.2, fill_color=GREY_B, fill_opacity=0.8, stroke_width=0).move_to([-5.5, -0.5, 0])
        tower = Rectangle(width=0.3, height=1.4, fill_color=BLUE, fill_opacity=0.8, stroke_width=0).move_to([-0.5, -0.4, 0])
        you = Dot([2.8, -1.0, 0], radius=0.14, color=EAR)
        ground = Line([-6.2, -1.15, 0], [6.2, -1.15, 0], color=GREY_D)
        l1 = DoubleArrow([-5.5, -1.6, 0], [2.8, -1.6, 0], color=GREY_A, buff=0, stroke_width=2)
        l2 = DoubleArrow([-0.5, -2.1, 0], [2.8, -2.1, 0], color=BLUE, buff=0, stroke_width=2)
        t1 = label(rf"{d['d_main']:.0f} m: \ {1000 * d['d_main'] / d['c']['20']:.0f} ms", font_size=15, color=GREY_A).next_to(l1, DOWN, buff=0.05)
        t2 = label(rf"{d['d_tower']:.0f} m: \ {1000 * d['d_tower'] / d['c']['20']:.0f} ms", font_size=15, color=BLUE).next_to(l2, DOWN, buff=0.05)
        names = VGroup(label(r"stage", font_size=15, color=GREY_B).next_to(stage, UP, buff=0.1), label(r"delay tower", font_size=15, color=BLUE).next_to(tower, UP, buff=0.1), label(r"you", font_size=15, color=EAR).next_to(you, UP, buff=0.1))
        eq = MathTex(r"\tau = \frac{d_{\text{main}} - d_{\text{tower}}}{c} + 10\ \text{ms}", font_size=34, color=TUNE).to_edge(UP, buff=1.0)
        res = label(rf"the tower plays {d['delay_ms']:.0f} ms late: \ its sound reaches you just after the stage's, \ so the ear hears the stage \ (Part 55's precedence effect)",
                    font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"a delay tower", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"At a festival the back field may be a hundred metres from the stage, too far for the main system. "
            "<bookmark mark='a'/> So a delay tower stands in the field. You are ninety metres from the stage and thirty from the "
            "tower: the stage's sound takes two hundred and sixty milliseconds to reach you, the tower's eighty-seven. "
            "<bookmark mark='b'/> Played at the same moment, the tower would be heard first, a sixth of a second ahead, and the "
            "stage would arrive as an echo. <bookmark mark='c'/> So the tower is delayed by the difference, plus ten "
            f"milliseconds: {say(d['delay_ms'])} in all. Its sound now reaches you just after the stage's, and by Part 55's "
            "precedence effect you hear the band on the stage, only louder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ground), FadeIn(stage), FadeIn(tower), FadeIn(you), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(l1), FadeIn(l2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("b")
            self.play(Indicate(tower, color=EAR))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("delay")
        c = clip("delay.two")
        card = listen_card(r"A voice heard 90 m from the stage and 30 m from a delay tower, \ twice: \ once with the tower delayed correctly, \ "
                           r"once not delayed at all. \ Which was aligned?", width=10.0)
        with self.voiceover("Your turn. A voice heard ninety metres from the stage and thirty from the tower, twice: once with the tower delayed correctly, once not at all. Which was aligned?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a tower, \ twice", kind="physical model", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"the first: \ one voice; \ the second: \ every note followed by its echo from the stage", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The first: a single, clear voice. In the second every note is followed a sixth of a second later by its echo from the stage."):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weather(self):
        d = load("delay")
        items = [
            (rf"sound travels faster in warm air: \ $c = 331.3 + 0.606\,T$: \ {d['c']['10']:.0f} m/s at 10$^\circ$C, \ {d['c']['30']:.0f} at 30", WHITE),
            (rf"a tower aligned in the afternoon heat drifts by {abs(d['drift_ms']['10']):.0f} ms when the night cools by 10$^\circ$C", WHITE),
            (r"temperature gradients bend sound: \ warm ground and cool air above \ (a sunny afternoon) \ bend it upwards, \ over the back of the field", WHITE),
            (r"a cool ground at night bends it down again: \ the neighbours hear the festival best after dark", WHITE),
            (r"wind adds to the speed downwind and subtracts upwind: \ the same bending, \ and a gusting, \ shifting sound at a distance", TUNE),
        ]
        rows_scene(self, r"weather", items,
                   "Outdoors, the air itself moves the sound. <bookmark mark='b'/> Sound travels faster in warm air, three hundred "
                   "and thirty-one metres a second plus nought point six for each degree. <bookmark mark='c'/> So a tower aligned "
                   f"in the afternoon heat drifts by {say(abs(d['drift_ms']['10']))} milliseconds when the night cools by ten degrees, "
                   "and engineers re-measure. <bookmark mark='d'/> Temperature gradients bend sound: warm ground under cooler air, on "
                   "a sunny afternoon, bends it upwards, over the heads at the back. <bookmark mark='e'/> A cool ground at night bends "
                   "it down again, which is why the neighbours hear the festival best after dark. <bookmark mark='f'/> And wind adds "
                   "to the speed of sound downwind and subtracts upwind: the same bending, and a gusting, shifting sound far away.", marks="bcdef")

    # ------------------------------------------------------------------
    def air(self):
        d = load("air")
        f = np.array(d["f"])
        ax = logf_axes(width=8.6, height=3.0, flo=100, fhi=20000, ylo=-3, yhi=0, center=DOWN * 0.4 + LEFT * 0.6, ticks=(100, 1000, 10000))
        cols = {"20C 50%": TUNE, "30C 20%": EAR, "10C 80%": BLUE}
        cs = VGroup(*[curve(f, np.clip(np.log10(np.maximum(np.array(v), 1e-5)), -3, 0), ax.to, color=cols[k], width=3) for k, v in d["curves"].items()])
        yt = VGroup(*[label(rf"{v} dB/m", font_size=13, color=GREY_A).next_to(ax.to(100, np.log10(v)), LEFT, buff=0.1) for v in (0.001, 0.01, 0.1, 1.0)])
        key = VGroup(*[label(k.replace("C", r"$^\circ$C,").replace("%", r"\% humidity"), font_size=15, color=c_) for k, c_ in cols.items()]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        lo = d["loss100"]
        note = label(rf"over 100 m at 20$^\circ$C: \ {lo['1000']:.1f} dB at 1 kHz, \ {lo['4000']:.0f} at 4 kHz, \ {lo['8000']:.0f} at 8 kHz, \ {lo['16000']:.0f} at 16 kHz", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"what the air takes \ (ISO 9613-1)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The air also absorbs, and not evenly. <bookmark mark='a'/> Here is the international standard's formula, ISO "
            "9613-1, for three kinds of weather, on a logarithmic scale of decibels per metre. Molecules of oxygen and "
            "nitrogen soak up sound, most of all at high frequencies, and how much depends on temperature and humidity. "
            f"<bookmark mark='b'/> Over a hundred metres on a mild day, half a decibel at one kilohertz, {say(lo['4000'])} at "
            f"four, {say(lo['8000'])} at eight, {say(lo['16000'])} at sixteen. The back of a festival hears a darker band, "
            "and engineers lift the treble of distant zones to match."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.3), FadeIn(key), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def air_heard(self):
        d = load("air")
        c = clip("air.two")
        boxes = choice_boxes([r"10 m of air", r"100 m of air"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.4)
        note = label(r"matched in loudness: \ only the air differs", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"the air, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear only the air: our mix after ten metres and after a hundred, matched in loudness."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"10 m, \ then 100 m", kind="physical model", detail=r"our mix, \ ISO 9613-1", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["near"], st["far"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["far"], c.duration, buff=0.08)
        with self.voiceover("At a hundred metres the hi-hat has lost its sparkle and the snare its crack: the same band, further away."):
            self.play(Indicate(boxes[1], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()
