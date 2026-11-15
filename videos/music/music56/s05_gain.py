from __future__ import annotations

from videos.music.music56.common import *  # noqa: F403

GCOL = {"low": BLUE, "right": TUNE, "hot": EAR}


class Gain(SoundScene):
    def construct(self):
        chapter(self, 4, r"Gain staging", r"How loud should a signal be on its way in?")
        self.chain_rows()
        self.diagram()
        self.heard()
        self.bits()
        self.references()

    # ------------------------------------------------------------------
    def chain_rows(self):
        d = load("gain")
        r = d["rows"]["right"]
        items = [
            (rf"a voice peaking at {d['spl']:.0f} dB SPL into a condenser microphone of {d['sens_mv']:.0f} mV per pascal: \ {r['mic_dbu']:.0f} dBu, \ a few dozen millivolts", WHITE),
            (r"the preamplifier adds gain, \ and its own hiss \ (Part 54's noise budget), \ and the room's", WHITE),
            (r"the converter reaches full scale, \ 0 dBFS, \ at +18 dBu; \ above it there is nothing: \ the waveform is cut flat", WHITE),
            (r"below, \ the floor: \ the hiss carried along, \ and the converter's own \ (a 16-bit one near $-98$ dBFS)", WHITE),
            (r"gain staging: \ set each stage so that the peaks clear the ceiling and the quiet parts clear the floor", TUNE),
        ]
        rows_scene(self, r"from the air to the converter", items,
                   "Every recording passes through a chain of gains. <bookmark mark='b'/> A voice peaking at a hundred and four "
                   "decibels into a condenser microphone of twelve millivolts per pascal gives about minus twenty-six dBu, a few "
                   "dozen millivolts. <bookmark mark='c'/> The preamplifier adds gain, and its own hiss, as in Part 54's noise "
                   "budget, and the room's hiss rides along. <bookmark mark='d'/> The converter reaches full scale, nought dBFS, at "
                   "plus eighteen dBu; above that there is nothing, and the waveform is cut flat. <bookmark mark='e'/> Below is "
                   "the floor: the hiss carried along, and the converter's own, near minus ninety-eight for sixteen bits. "
                   "<bookmark mark='f'/> Gain staging is setting each stage so that the peaks clear the ceiling and the quiet "
                   "passages clear the floor.", marks="bcdef")

    # ------------------------------------------------------------------
    def diagram(self):
        d = load("gain")
        ax = frame_axes(width=9.0, height=4.4, xlo=0, xhi=3, ylo=-110, yhi=20, center=DOWN * 0.2 + RIGHT * 0.4)
        fs = DashedLine(ax.to(0, 0), ax.to(3, 0), color=RED, stroke_width=2)
        fsl = label(r"full scale, \ 0 dBFS", font_size=15, color=RED).next_to(ax.to(3, 0), RIGHT, buff=0.1)
        yt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (20, 0, -20, -40, -60, -80, -100)])
        cols = VGroup()
        names = {"low": r"gain 0 dB", "right": r"gain 28 dB", "hot": r"gain 52 dB"}
        for i, k in enumerate(("low", "right", "hot")):
            r = d["rows"][k]
            x = i + 0.5
            pk = min(r["peak_dbfs"], 18)
            band = Rectangle(width=0.7, height=abs(ax.to(0, pk)[1] - ax.to(0, r["noise_dbfs"])[1]), stroke_width=0, fill_color=GCOL[k], fill_opacity=0.35)
            band.move_to((ax.to(x, pk) + ax.to(x, r["noise_dbfs"])) / 2)
            top = Line(ax.to(x - 0.35, pk), ax.to(x + 0.35, pk), color=GCOL[k], stroke_width=5)
            bot = Line(ax.to(x - 0.35, r["noise_dbfs"]), ax.to(x + 0.35, r["noise_dbfs"]), color=GREY_A, stroke_width=4)
            t1 = label(rf"peak {r['peak_dbfs']:+.0f}", font_size=14, color=GCOL[k]).next_to(top, UP, buff=0.08)
            t2 = label(rf"floor {r['noise_dbfs']:.0f}", font_size=14, color=GREY_A).next_to(bot, DOWN, buff=0.08)
            nm = label(names[k], font_size=17, color=GCOL[k]).next_to(ax.to(x, -110), DOWN, buff=0.15)
            cols.add(VGroup(band, top, bot, t1, t2, nm))
        note = label(r"too low: \ the floor is the converter's, \ 54 dB down; \ right: \ 73 dB of range, \ 16 dB of headroom; \ too hot: \ 8 dB past the ceiling",
                     font_size=16, color=WHITE).to_edge(DOWN, buff=0.25)
        head = label(r"three gains, \ in dBFS", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the chain at three gain settings, in decibels relative to full scale. <bookmark mark='a'/> With no gain, "
            "the voice peaks at minus forty-four, and its floor is the converter's own: only fifty-four decibels of range. "
            "<bookmark mark='b'/> With twenty-eight decibels, the peaks reach minus sixteen, leaving sixteen decibels of "
            "headroom, and the floor is now the room and the preamplifier: seventy-three decibels of range, all the room "
            "allows. <bookmark mark='c'/> With fifty-two, the peaks would reach plus eight, eight decibels past the ceiling, "
            "and the range is no better, because the hiss was turned up with the voice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(fs), FadeIn(fsl), FadeIn(ghost(cols, 0.25)))
            for mark, cl in zip("abc", cols):
                vo.wait_until(mark)
                self.play(FadeIn(cl), run_time=0.8)
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("gain")
        c = clip("gain.three")
        boxes = choice_boxes([r"too low", r"right", r"too hot"], width=2.8, height=0.9, buff=0.9, size=22).move_to(UP * 0.4)
        note = label(r"each brought to the same loudness afterwards", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"three gains, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear all three through a sixteen-bit converter, each turned up or down afterwards to the same loudness. Listen "
            "for hiss in the first, and for the third's peaks."
        ):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"low, \ right, \ hot", kind="physical model", detail=r"Part 8's voice, \ a simulated chain", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["low"], st["right"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["right"], st["hot"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["hot"], c.duration, buff=0.08)
        with self.voiceover(
            "The first carries a grainy hiss once it is turned up. The third is clipped on every loud note, a buzz that no "
            "later stage can remove. Too low can be lived with; too hot cannot."
        ):
            self.play(Indicate(boxes[2], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bits(self):
        items = [
            (r"a 24-bit converter's floor is set by its analogue parts, \ near $-115$ dBFS: \ low levels cost almost nothing", WHITE),
            (r"so modern practice: \ peaks around $-18$ to $-12$ dBFS while recording, \ and never near 0", WHITE),
            (r"inside the workstation, \ 32-bit floating point: \ a range of over 1,500 dB, \ no ceiling to hit between plug-ins", WHITE),
            (r"but plug-ins modelled on analogue gear react to level, \ as the gear did \ (Part 50): \ drive them as their originals were driven", WHITE),
            (r"the ceiling returns at the end: \ the converter on the way out, \ and the file", TUNE),
        ]
        rows_scene(self, r"twenty-four bits and floating point", items,
                   "Modern equipment changes the balance. <bookmark mark='b'/> A twenty-four-bit converter's floor is set by its "
                   "analogue parts, near minus a hundred and fifteen dBFS, so recording low costs almost nothing. "
                   "<bookmark mark='c'/> Modern practice is to let the peaks reach about minus eighteen to minus twelve, and never "
                   "near nought. <bookmark mark='d'/> Inside the workstation, signals are thirty-two-bit floating point, with a "
                   "range of over fifteen hundred decibels and no ceiling to hit between plug-ins. <bookmark mark='e'/> But plug-ins "
                   "modelled on analogue gear react to level, as the gear did in Part 50, so drive them as their originals were "
                   "driven. <bookmark mark='f'/> The ceiling comes back at the end: the converter on the way out, and the file.", marks="bcdef")

    # ------------------------------------------------------------------
    def references(self):
        rows = VGroup(VGroup(label(r"level", font_size=17, color=GREY_A), label(r"in volts", font_size=17, color=GREY_A), label(r"where", font_size=17, color=GREY_A)))
        data = [(r"$-60$ to $-20$ dBu", r"1 to 80 mV", r"a microphone's output"), (r"$-10$ dBV", r"0.32 V", r"consumer line level"),
                (r"$+4$ dBu", r"1.23 V", r"professional line level, \ 0 VU"), (r"$+18$ to $+24$ dBu", r"6 to 12 V", r"a converter's full scale")]
        for a, b, c_ in data:
            rows.add(VGroup(label(a, font_size=19, color=WHITE), label(b, font_size=19, color=WHITE), label(c_, font_size=19, color=TUNE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.6 * i)
        rows.move_to(DOWN * 0.1)
        note = label(r"0 dBu = 0.775 V \ (a milliwatt into 600 ohms); \ 0 dBV = 1 V; \ so a converter at +18 dBu puts 0 VU at $-14$ dBFS", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"reference levels", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And the names of the levels. <bookmark mark='a'/> A microphone gives from minus sixty to minus twenty dBu, a "
            "millivolt to eighty. Consumer gear runs at minus ten dBV, a third of a volt; professional gear at plus four dBu, a "
            "volt and a quarter, which is nought on a VU meter; and a converter reaches full scale at plus eighteen to plus "
            "twenty-four dBu. <bookmark mark='b'/> Nought dBu is nought point seven seven five volts, a milliwatt into six "
            "hundred ohms, a relic of telephone lines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
