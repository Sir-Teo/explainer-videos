from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Schroeder(SoundScene):
    def construct(self):
        chapter(self, 8, r"Schroeder's reverberator", r"Can a room be made of arithmetic?")
        self.design()
        self.diagram()
        self.density()
        self.hear()
        self.moorer()

    # ------------------------------------------------------------------
    def design(self):
        items = [
            (r"Manfred Schroeder \ (1962): \ simulating a room by image sources was far beyond 1960s computers", WHITE),
            (r"instead, \ imitate what a listener hears: \ dense echoes, \ decaying smoothly, \ with no colour", WHITE),
            (r"a feedback comb gives a train of echoes that decays at a rate we can set: \ chapter 2's poles", WHITE),
            (r"four combs with unrelated delays, \ 30 to 45 ms, \ in parallel: \ their echoes interleave", TUNE),
            (r"then two all-passes in series multiply the echoes without colouring the sound", GREY_A),
        ]
        rows_scene(self, r"imitate the ear, \ not the room", items,
                   "In 1962 Manfred Schroeder at Bell Labs could not simulate a room: image sources were far beyond the computers "
                   "of the day. <bookmark mark='b'/> Instead he imitated what a listener hears: dense echoes, decaying smoothly, "
                   "with no colour of their own. <bookmark mark='c'/> A feedback comb gives a train of echoes that decays at a "
                   "rate we can set, by chapter two's rule about poles. <bookmark mark='d'/> Four combs with unrelated delays, "
                   "between thirty and forty-five milliseconds, run in parallel, so their echoes interleave. "
                   "<bookmark mark='e'/> Then two all-passes in series multiply the echoes, without colouring the sound.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def diagram(self):
        d = load("schroeder")
        combs = VGroup()
        for i, ms in enumerate(d["combs_ms"]):
            combs.add(VGroup(RoundedRectangle(width=2.2, height=0.6, corner_radius=0.1, stroke_color=TUNE), label(rf"comb, \ {ms} ms", font_size=17, color=TUNE)).arrange(ORIGIN).move_to([-2.2, 1.5 - 0.85 * i, 0]))
        inp = label(r"in", font_size=20, color=WHITE).move_to([-5.2, 0.2, 0])
        summ = Circle(radius=0.25, stroke_color=WHITE).move_to([0.2, 0.2, 0])
        plus = label(r"$+$", font_size=24, color=WHITE).move_to(summ)
        aps = VGroup(*[VGroup(RoundedRectangle(width=2.0, height=0.6, corner_radius=0.1, stroke_color=BLUE), label(rf"all-pass, \ {ms} ms", font_size=16, color=BLUE)).arrange(ORIGIN).move_to([1.8 + 2.3 * i, 0.2, 0])
                       for i, (ms, g) in enumerate(d["allpass"])])
        out = label(r"out", font_size=20, color=WHITE).move_to([6.3, 0.2, 0])
        wires = VGroup()
        for cb in combs:
            wires.add(Line(inp.get_right() + RIGHT * 0.1, cb.get_left(), stroke_width=1.5, color=GREY_B), Line(cb.get_right(), summ.get_left(), stroke_width=1.5, color=GREY_B))
        wires.add(Line(summ.get_right(), aps[0].get_left(), stroke_width=1.5, color=GREY_B), Line(aps[0].get_right(), aps[1].get_left(), stroke_width=1.5, color=GREY_B),
                  Line(aps[1].get_right(), out.get_left(), stroke_width=1.5, color=GREY_B))
        cap = label(rf"each comb's feedback gain set so its echoes fall 60 dB in {d['t60']:.0f} s: \ $g = 10^{{-3D/(f_s T_{{60}})}}$", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"four combs and two all-passes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here it is, the whole reverberator. <bookmark mark='a'/> The input feeds four combs, of 29.7, 37.1, 41.1 and 43.7 "
            "milliseconds. <bookmark mark='b'/> Their outputs are summed, <bookmark mark='c'/> and pass through two all-passes "
            "of five and 1.7 milliseconds. <bookmark mark='d'/> Each comb's feedback gain is set so that its echoes fall sixty "
            f"decibels in the chosen time, here {say(d['t60'])} seconds: we measure {say(d['rt_schroeder'], 2)}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inp), FadeIn(out))
            vo.wait_until("a")
            self.play(FadeIn(combs), FadeIn(wires[:8]))
            vo.wait_until("b")
            self.play(FadeIn(summ), FadeIn(plus))
            vo.wait_until("c")
            self.play(FadeIn(aps), FadeIn(wires[8:]))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moorer(self):
        items = [
            (r"James Moorer \ (1979): \ `About this reverberation business'", WHITE),
            (r"a low-pass filter inside each comb's loop, \ so the highs die sooner, \ as air and walls make them", WHITE),
            (r"six combs instead of four, \ for a denser tail", WHITE),
            (r"early reflections taken from a real room's geometry, \ in front of the tail", TUNE),
            (r"the same three ideas run through every reverb since", GREY_A),
        ]
        rows_scene(self, r"Moorer's improvements", items,
                   "Schroeder's design was improved by James Moorer in 1979, in a paper called About this reverberation business. "
                   "<bookmark mark='b'/> He put a low-pass filter inside each comb's loop, so that the highs die sooner, as air and "
                   "walls make them. <bookmark mark='c'/> He used six combs instead of four, for a denser tail. "
                   "<bookmark mark='d'/> And he put early reflections, taken from a real room's geometry, in front of the tail. "
                   "<bookmark mark='e'/> The same three ideas run through every reverb since.", marks="bcde")

    # ------------------------------------------------------------------
    def density(self):
        d = load("schroeder")
        dens = d["density"]
        n = len(dens["room"])
        p = line_plot([dens["room"], dens["schroeder"], dens["fdn"]], width=8.0, height=3.2, ylo=0, yhi=1.3, xmax=n - 1, colors=[GREY_A, TUNE, BLUE],
                      xlabel=r"time, \ in steps of 10 ms", ylabel=r"echo density \ (1: \ as dense as noise)", yticks=(0, 0.5, 1.0), xticks=(0, 10, 20, 30, 39), size=16).move_to(DOWN * 0.2 + LEFT * 0.8)
        key = VGroup(label(r"the simulated room", font_size=17, color=GREY_A), label(r"Schroeder's reverberator", font_size=17, color=TUNE), label(r"a feedback delay network \ (chapter 9)", font_size=17, color=BLUE)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(p, RIGHT, buff=0.2)
        head = label(r"how thickly do the echoes arrive?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        r = dens["room"]
        s = dens["schroeder"]
        with self.voiceover(
            "How good is the imitation? Jonathan Abel and Patty Huang measure echo density: the share of the response that "
            "looks like noise, scaled so that true noise scores one. <bookmark mark='a'/> The simulated room reaches one "
            "within a few tens of milliseconds. <bookmark mark='b'/> Schroeder's reverberator never gets there: it stays "
            f"near {say(float(np.mean(s[10:])), 1)}, a sparse train of echoes whose pattern the ear can catch. That is the "
            "flutter you heard in the hook. <bookmark mark='c'/> The feedback delay network of chapter nine builds up more "
            "slowly, but keeps climbing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p[0]), FadeIn(p[2:]))
            vo.wait_until("a")
            self.play(Create(p.lines[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(p.lines[1]), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(p.lines[2]), FadeIn(key[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("schroeder")
        c = clip("schroeder.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t in (r"Schroeder's reverberator", r"a feedback delay network")]).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        cap = label(r"four snare hits, \ both reverbs set to 2 seconds", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"hard to fool with a snare", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Sharp sounds expose a reverb. Four snare hits, through Schroeder's design, then through a feedback delay network."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two reverbs", kind="synthesized", detail=r"Part 40's snare", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["schroeder"], st["fdn"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["fdn"], c.duration, buff=0.08)
        with self.voiceover(
            "Schroeder's tail rings with a metallic flutter; the network's is smoother. Schroeder knew his design's limits, and "
            "James Moorer improved it in 1979 with low-pass filters in the combs and early reflections in front. Chapter nine "
            "is the design that replaced it."
        ):
            self.play(Indicate(boxes[1], color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
