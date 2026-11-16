from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Crossover(SoundScene):
    def construct(self):
        chapter(self, 9, r"Crossovers and amplifiers", r"How do two drivers become one loudspeaker?")
        self.why()
        self.sums()
        self.heard()
        self.digital()
        self.amps()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a woofer must be big to move air; \ a big cone beams and breaks up at high frequencies", WHITE),
            (r"a tweeter is small and light; \ it would tear itself apart on bass", WHITE),
            (r"a crossover sends lows to one and highs to the other: \ a low-pass and a high-pass", WHITE),
            (r"the two must add back to a flat response, \ in level and in phase", TUNE),
            (r"which is harder than it sounds", GREY_A),
        ]
        rows_scene(self, r"two drivers, \ one speaker", items,
                   "Most loudspeakers use more than one driver. <bookmark mark='b'/> A woofer must be big to move air, and a big cone "
                   "beams and breaks up at high frequencies; <bookmark mark='c'/> a tweeter is small and light and would tear itself "
                   "apart on bass. <bookmark mark='d'/> A crossover sends the lows to one and the highs to the other: a low-pass and "
                   "a high-pass. <bookmark mark='e'/> The two must add back to a flat response, in level and in phase, "
                   "<bookmark mark='f'/> which is harder than it sounds.", marks="bcdef")

    # ------------------------------------------------------------------
    def sums(self):
        d = load("crossover")
        f = np.array(d["f"])
        cells = VGroup()
        for k, t, col in (("bw2", r"Butterworth, \ in phase", EAR), ("bw2_inv", r"Butterworth, \ tweeter inverted", GOLD), ("lr4", r"Linkwitz--Riley", TUNE)):
            ax = logf_axes(width=3.6, height=2.2, flo=100, fhi=40000, ylo=-30, yhi=6, ticks=(1000, 10000), size=12)
            lp = curve(f, np.maximum(d[k]["lp"], -30), ax.to, color=GREY_A, width=1.5)
            hp = curve(f, np.maximum(d[k]["hp"], -30), ax.to, color=GREY_A, width=1.5)
            sm = curve(f, np.maximum(d[k]["sum"], -30), ax.to, color=col, width=3)
            at = d[k]["at_fc"]
            cells.add(VGroup(label(t, font_size=17, color=col), VGroup(ax, lp, hp, sm), label(r"a hole at the crossover" if at < -20 else (rf"$+{at:.1f}$ dB at the crossover" if at > 0.5 else r"flat"), font_size=15, color=col)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        cap = label(r"grey: \ the two sections; \ colour: \ their sum; \ crossover at 2 kHz", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"adding the two back", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Add the two sections back and see. <bookmark mark='a'/> Two second-order Butterworth filters, in phase: at the "
            "crossover each is a quarter turn of phase away from the input in opposite directions, so they arrive half a cycle "
            "apart and cancel: a hole. <bookmark mark='b'/> Invert the tweeter and they add, but too well: three decibels "
            "too loud at the crossover. <bookmark mark='c'/> Siegfried Linkwitz and Russ Riley's answer, in 1976: square each "
            "Butterworth. Each section is six decibels down at the crossover, in phase with the other, and the sum is flat "
            "everywhere, to the arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(cells, 0.25)))
            for mark, cc in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def amps(self):
        items = [
            (r"class A: \ the output transistors always conduct: \ clean, \ hot, \ at best 25 to 50 per cent efficient", WHITE),
            (r"class B: \ one transistor for each half of the wave: \ at best $\pi/4$, \ 78.5 per cent; \ AB hides the hand-over", WHITE),
            (r"class D: \ switch fully on or off hundreds of thousands of times a second, \ and filter: \ over 90 per cent", WHITE),
            (r"class D is Part 48's delta-sigma idea at power: \ one bit, \ very fast, \ smoothed", TUNE),
            (r"every phone, \ smart speaker and most powered speakers now use it", GREY_A),
        ]
        rows_scene(self, r"amplifiers", items,
                   "The loudspeaker needs power. <bookmark mark='b'/> In a class A amplifier the output transistors always conduct: clean, hot, and at best twenty-five to fifty per cent efficient. <bookmark mark='c'/> Class B uses one transistor for each half of the wave, at best pi over four, seventy-eight and a half per cent, and class A B hides the hand-over between them. <bookmark mark='d'/> Class D switches fully on or off hundreds of thousands of times a second and filters the result: over ninety per cent. <bookmark mark='e'/> It is a fast switching power stage, using pulse-width or related modulation; it is not necessarily a delta-sigma converter: very few levels, very fast, smoothed. <bookmark mark='f'/> Class D is common in phones, smart speakers and powered loudspeakers.", marks="bcdef")

    # ------------------------------------------------------------------
    def digital(self):
        items = [
            (r"a passive crossover is coils and capacitors between the amplifier and the drivers; \ an active one comes before separate amplifiers", WHITE),
            (r"in software a crossover can be any filter, \ even linear-phase: \ the sections add in time as well as level", WHITE),
            (r"the same processor corrects each driver's own response and the room's \ (Part 55)", WHITE),
            (r"the cost of linear phase is latency, \ as Part 53's look-ahead was", WHITE),
            (r"loudspeakers have become computers with cones", TUNE),
        ]
        rows_scene(self, r"crossovers in software", items,
                   "Crossovers moved into software. <bookmark mark='b'/> A passive crossover is coils and capacitors between the amplifier and the drivers; an active one comes before separate amplifiers for each. <bookmark mark='c'/> In software a crossover can be any filter at all, even linear-phase, so that the sections add in time as well as in level. <bookmark mark='d'/> The same processor corrects each driver's own response, and the room's, which is Part 55. <bookmark mark='e'/> The price of linear phase is latency, like Part 53's look-ahead. <bookmark mark='f'/> Loudspeakers have become computers with cones.", marks="bcdef")


    # ------------------------------------------------------------------
    def heard(self):
        d = load("xover")
        c = clip("xover.two")
        cells = choice_boxes([r"Butterworth, \ in phase", r"Linkwitz--Riley"], width=4.0, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(r"a voice and piano, \ with a little hiss, \ through a crossover at 2 kHz", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a hole at the crossover, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the hole: a voice and piano through the in-phase Butterworth pair, then through Linkwitz-Riley."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a hole, \ then flat", kind="synthesized", detail=r"two crossovers", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["hole"], st["flat"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["flat"], c.duration, buff=0.08)
        with self.voiceover(
            "The difference is subtle: a narrow notch at two kilohertz takes a little presence out of the voice and a "
            "little bite out of the hiss, a hollowness more felt than heard. Over a whole loudspeaker, and off axis, such "
            "errors add up."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()
