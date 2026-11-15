from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403


class Phase(SoundScene):
    def construct(self):
        chapter(self, 3, r"Phase between microphones", r"Why can two good microphones sound worse than one?")
        self.two()
        self.comb()
        self.rule()
        self.snare()
        self.quiz()
        self.fixes()

    # ------------------------------------------------------------------
    def two(self):
        items = [
            (r"two microphones on one source: \ the far one hears it later, \ by the extra distance over $c$", WHITE),
            (r"summed, \ the two copies add where they are in step and cancel where they are half a cycle apart", WHITE),
            (r"for a delay $\tau$: \ cancellations at $1/2\tau$, \ $3/2\tau$, \ $5/2\tau$, \ ... \ evenly spaced: \ a comb filter \ (Part 49)", WHITE),
            (r"one microphone 1 m from a guitar, \ another 3 m away: \ 5.8 ms apart, \ the first notch at 86 Hz", TUNE),
        ]
        rows_scene(self, r"one source, \ two microphones", items,
                   "The commonest problem in a multitrack recording is the simplest physics. <bookmark mark='b'/> Put two "
                   "microphones on one source, and the far one hears it later, by the extra distance over the speed of sound. "
                   "<bookmark mark='c'/> Sum them, and the two copies add where they are in step and cancel where they are half a "
                   "cycle apart. <bookmark mark='d'/> For a delay tau the cancellations fall at one over two tau, three over two "
                   "tau, and so on, evenly spaced: a comb filter, as in Part 49. <bookmark mark='e'/> One microphone a metre from a "
                   "guitar and another three metres away are five point eight milliseconds apart, and the first notch is at "
                   "eighty-six hertz.", marks="bcde")

    # ------------------------------------------------------------------
    def comb(self):
        d = load("phase")
        f = np.array(d["f"])
        ax = logf_axes(width=10.0, height=3.0, flo=20, fhi=20000, ylo=-30, yhi=8, center=DOWN * 0.4)
        eq_ = curve(f, np.clip(d["combs"]["equal"], -30, 8), ax.to, color=EAR, width=2)
        tr_ = curve(f, np.clip(d["combs"]["three_to_one"], -30, 8), ax.to, color=TUNE, width=3)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.1) for v in (6, 0, -12, -24)])
        key = VGroup(label(r"two microphones at the same level", font_size=17, color=EAR), label(r"the far one 9.5 dB down \ (three times the distance)", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        hi, lo = d["extremes"]
        note = label(rf"at equal levels: \ +6 dB peaks, \ bottomless notches; \ at 9.5 dB down: \ +{hi:.1f} and {lo:.1f} dB", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"a comb filter, \ 5.8 ms", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is that comb, from twenty hertz to twenty kilohertz. <bookmark mark='a'/> If the two microphones are at the "
            "same level, the peaks are six decibels high and the notches bottomless: whole bands of the guitar disappear, and "
            "the sound turns hollow. <bookmark mark='b'/> But a microphone three times as far away hears the source nine and a "
            "half decibels quieter, by the inverse square law, and then the comb shrinks to plus "
            f"{say(hi, 1)} and minus {say(-lo, 1)} decibels: still there, but mild."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(note), FadeIn(ghost(VGroup(eq_, tr_), 0.25)))
            vo.wait_until("a")
            self.play(Create(eq_), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(tr_), FadeIn(key[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        eq = MathTex(r"20\log_{10}\Bigl(1 + \frac{1}{3}\Bigr) = +2.5\ \text{dB}, \qquad 20\log_{10}\Bigl(1 - \frac{1}{3}\Bigr) = -3.5\ \text{dB}", font_size=32, color=TUNE).move_to(UP * 1.4)
        items = [
            (r"the 3 : 1 rule: \ a second microphone should be at least three times as far from a source as that source's own microphone", WHITE),
            (r"then each source's comb in the other microphone stays within about $\pm 3$ dB", WHITE),
            (r"a rule for spaced spot microphones; \ it fails for two microphones on one instrument, \ on purpose", WHITE),
            (r"the worst case is two microphones on one drum, \ on opposite sides", GREY_A),
        ]
        rows = text_rows(items, font_size=21).move_to(DOWN * 0.9)
        head = label(r"the 3 : 1 rule", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Engineers turned that into a rule. <bookmark mark='a'/> The three to one rule: a second microphone should be at "
            "least three times as far from a source as the source's own microphone. <bookmark mark='b'/> Then the comb it adds "
            "stays within about three decibels either way. <bookmark mark='c'/> It is a rule for spot microphones spread over a "
            "band; it is broken on purpose when two microphones share one instrument. <bookmark mark='d'/> And the worst case is "
            "two microphones on one drum, facing each other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def snare(self):
        shell = Rectangle(width=3.0, height=1.0, stroke_color=GREY_B, stroke_width=3).move_to(LEFT * 3.0)
        top = Line(shell.get_corner(UL), shell.get_corner(UR), color=WHITE, stroke_width=5)
        bot = Line(shell.get_corner(DL), shell.get_corner(DR), color=WHITE, stroke_width=5)
        wires = VGroup(*[Line(shell.get_corner(DL) + RIGHT * (0.3 + 0.3 * i) + DOWN * 0.06, shell.get_corner(DL) + RIGHT * (0.45 + 0.3 * i) + DOWN * 0.06, color=GREY_A, stroke_width=2) for i in range(8)])
        m1 = VGroup(Circle(radius=0.16, stroke_color=TUNE, stroke_width=3), Line(ORIGIN, UP * 0.6 + RIGHT * 0.4, color=TUNE, stroke_width=3)).move_to(shell.get_top() + UP * 0.6 + LEFT * 0.6)
        m2 = VGroup(Circle(radius=0.16, stroke_color=EAR, stroke_width=3), Line(ORIGIN, DOWN * 0.6 + RIGHT * 0.4, color=EAR, stroke_width=3)).move_to(shell.get_bottom() + DOWN * 0.6 + LEFT * 0.6)
        arrows = VGroup(Arrow(shell.get_top() + UP * 0.05 + RIGHT * 0.6, shell.get_top() + DOWN * 0.45 + RIGHT * 0.6, color=WHITE, buff=0, stroke_width=4),
                        Arrow(shell.get_bottom() + UP * 0.05 + RIGHT * 0.6, shell.get_bottom() + DOWN * 0.45 + RIGHT * 0.6, color=WHITE, buff=0, stroke_width=4))
        items = text_rows([(r"the stick pushes the top head down", WHITE), (r"the top microphone sees the air pulled away from it", TUNE),
                           (r"the bottom microphone sees it pushed towards it: \ the same sound, \ inverted", EAR),
                           (r"summed as recorded, \ the body of the drum cancels; \ flip one, \ and it adds", WHITE)], font_size=20, width=6.6).move_to(RIGHT * 3.0)
        head = label(r"a snare from both sides", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Like this. A snare drum is often recorded from both sides: a microphone over the top head, for the crack, and one "
            "under the bottom, for the rattle of the wires. <bookmark mark='a'/> The stick pushes the top head down. "
            "<bookmark mark='b'/> To the top microphone the air is pulled away; <bookmark mark='c'/> to the bottom one, the air "
            "is pushed towards it: the same sound, inverted. <bookmark mark='d'/> Summed as recorded, the body of the drum "
            "cancels; flip one microphone's polarity, and it adds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(shell), FadeIn(top), FadeIn(bot), FadeIn(wires), FadeIn(m1), FadeIn(m2))
            vo.wait_until("a")
            self.play(FadeIn(items[0]), FadeIn(arrows))
            for mark, r in zip("bcd", items[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("phase")
        c = clip("phase.two")
        card = listen_card(r"Our snare, \ top and bottom microphones summed, \ twice: \ once with the bottom microphone's polarity "
                           r"flipped back, \ once left as recorded. \ Which was left as recorded?", width=10.0)
        with self.voiceover(
            "Your turn. Our snare, its top and bottom microphones summed, twice: once with the bottom microphone's polarity "
            "flipped back, and once left as recorded. Which was left as recorded?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a snare, \ twice", kind="physical model", detail=r"Part 40's snare, \ two microphones", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the second: \ the drum's body, \ 120 to 400 Hz, \ {d['low_loss_db']:.0f} dB weaker; \ thin, \ all wires", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The second. Its body, from a hundred and twenty to four hundred hertz, is {say(d['low_loss_db'])} decibels weaker: "
            "the drum turns thin and papery, all wires. One button on the console puts it back."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        items = [
            (r"polarity: \ the button marked $\varnothing$ on every channel, \ for microphones that face each other", WHITE),
            (r"time: \ slide the close microphone later by the extra distance, \ so that both copies line up", WHITE),
            (r"workstations find the delay by cross-correlation and align tracks automatically", WHITE),
            (r"but aligning is a choice, \ not a correction: \ the delay between a close and a room microphone is the room", TUNE),
            (r"and phase \ (Part 49's all-pass) \ can be rotated a little, \ band by band, \ as a tone control", GREY_A),
        ]
        rows_scene(self, r"putting it right", items,
                   "Putting it right. <bookmark mark='b'/> Polarity: the button marked with a slashed circle on every channel, for "
                   "microphones that face each other. <bookmark mark='c'/> Time: slide the close microphone's track later by the "
                   "extra distance, so the two copies line up. <bookmark mark='d'/> Workstations find the delay by cross-correlation "
                   "and align the tracks automatically. <bookmark mark='e'/> But aligning is a choice, not a correction: the delay "
                   "between a close and a room microphone is the sound of the room. <bookmark mark='f'/> And phase can be rotated "
                   "a little, band by band, with Part 49's all-passes, as a tone control of its own.", marks="bcdef")
