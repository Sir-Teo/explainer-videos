from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


def table_stack(tables, width=4.6, height=0.9, dx=0.32, dy=0.36, color=TUNE):
    """The stored cycles drawn one behind another, the first at the front."""
    g = VGroup()
    n = len(tables)
    for j in reversed(range(n)):
        w = wave_path(np.array(tables[j]), width=width, height=height, color=interpolate_color(BLUE, color, j / max(n - 1, 1)), stroke=2.2)
        w.shift(np.array([dx * j, dy * j, 0]))
        g.add(w)
    g.cycles = list(reversed(list(g)))
    return g


class Table(SoundScene):
    def construct(self):
        chapter(self, 8, r"Wavetables", r"What if the oscillator could hold any shape?")
        self.idea()
        self.stack()
        self.scan()
        self.spectra()
        self.mipmaps()
        self.today()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"an analogue oscillator offers a few shapes; \ a memory can hold any shape at all", WHITE),
            (r"store one cycle as 2048 numbers; \ read it round and round at the note's rate", WHITE),
            (r"store many cycles in a row, \ and let a knob choose where to read: \ the wavetable", WHITE),
            (r"Wolfgang Palm's PPG Wave \ (1981) \ scanned through 64 cycles under an envelope's control", TUNE),
            (r"a moving position is a moving spectrum, \ without a filter", GREY_A),
        ]
        rows_scene(self, r"a wave from memory", items,
                   "A digital oscillator need not imitate a circuit at all. <bookmark mark='b'/> An analogue oscillator offers a "
                   "few shapes; a memory can hold any shape. <bookmark mark='c'/> Store one cycle as two thousand and forty-eight "
                   "numbers, and read it round and round at the note's rate. <bookmark mark='d'/> Store many cycles in a row, and "
                   "let a knob choose where to read: that is a wavetable. <bookmark mark='e'/> Wolfgang Palm's PPG Wave of 1981 "
                   "scanned through sixty-four cycles under an envelope's control. <bookmark mark='f'/> A moving position is a "
                   "moving spectrum, without any filter.", marks="bcdef")

    # ------------------------------------------------------------------
    def stack(self):
        d = load("table")
        st = table_stack(d["tables"]).move_to(LEFT * 1.4 + DOWN * 0.1)
        lf = label(r"position 0: \ a sine", font_size=17, color=BLUE).next_to(st.cycles[0], DOWN, buff=0.25)
        lb = label(r"position 1: \ bright", font_size=17, color=TUNE).next_to(st.cycles[-1], UP, buff=0.2)
        side = VGroup(label(r"eight stored cycles", font_size=19, color=WHITE),
                      label(r"from a sine, \ through odd harmonics, \ to all 48", font_size=17, color=GREY_A),
                      label(r"between two cycles, \ the oscillator cross-fades", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        head = label(r"a table of cycles", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is our table: eight stored cycles. <bookmark mark='a'/> At the front, position zero, a sine. <bookmark mark='b'/> "
            "Moving back, odd harmonics grow in, then the even ones, until the last cycle has forty-eight harmonics, nearly a "
            "sawtooth. <bookmark mark='c'/> Between two stored cycles the oscillator cross-fades, so the position can move "
            "smoothly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(st, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(st.cycles[0]), FadeIn(lf), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(cyc) for cyc in st.cycles[1:]], lag_ratio=0.15), FadeIn(lb), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scan(self):
        d = load("table")
        c = clip("table.scan")
        st = table_stack(d["tables"]).move_to(DOWN * 0.1)
        head = label(r"a scan, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"a held C3: \ the position moves from the sine to the brightest and back over five seconds", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover("Hear one held C3 while the position moves from the sine to the brightest cycle and back."):
            self.play(FadeIn(head), FadeIn(st), FadeIn(cap))
        n = len(st.cycles)
        with self.listen(c) as snd:
            window(snd, r"a wavetable scan", kind="synthesized", detail=r"eight stored cycles", corner=DL, tag_corner=DR)
            box = SurroundingRectangle(st.cycles[0], color=EAR, buff=0.06, stroke_width=3)

            def upd(m, t):
                u = t / 2.5 if t < 2.5 else max(0.0, (5.0 - t) / 2.5)
                j = int(round(min(max(u, 0.0), 1.0) * (n - 1)))
                m.move_to(st.cycles[j].get_center())
                m.set_stroke(opacity=0.6 + 0.4 * np.sin(18 * t))
            snd.show(box)
            snd.drive(box, upd)
        with self.voiceover(
            "The tone opens like a filter sweep, but differently: no resonant whistle, and the order in which harmonics arrive "
            "is whatever the tables say. Odd harmonics came first here, so the middle of the scan sounded hollow, like a "
            "clarinet, before the even ones filled it in."
        ):
            self.play(Indicate(st, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectra(self):
        d = load("table")
        cells = VGroup()
        for p, t, col in (("0.0", r"position 0", BLUE), ("0.5", r"position 0.5", interpolate_color(BLUE, TUNE, 0.5)), ("1.0", r"position 1", TUNE)):
            bars = harm_bars(d["levels"][p], width=0.14, gap=0.22, floor=-50.0, height=2.0, color=col, labels=False)
            cells.add(VGroup(label(t, font_size=19, color=col), bars).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.9).move_to(UP * 0.1)
        cap = label(r"the first 16 harmonics, \ dB re the first \ (to $-50$)", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.1)
        half = d["levels"]["0.5"]
        note = label(rf"halfway: \ the odd harmonics at ${half[2]:.0f}$ and ${half[4]:.0f}$ dB, \ the even ones near ${half[1]:.0f}$", font_size=17, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"three positions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The spectra at three positions. <bookmark mark='a'/> At zero, one harmonic. <bookmark mark='b'/> Halfway, the odd "
            f"harmonics are strong, the third at {say(half[2])} decibels, and the even ones faint, near {say(half[1])}: the hollow "
            "middle you heard. <bookmark mark='c'/> At one, every harmonic, falling smoothly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(cells, 0.3)))
            for mark, cc in zip("abc", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.8)
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mipmaps(self):
        d = load("table")
        f6 = d["f6"]
        rows = VGroup(
            label(rf"the brightest cycle has 48 harmonics: \ at C6, \ {f6:.0f} Hz, \ the 48th would be {48 * f6 / 1000:.1f} kHz", font_size=20, color=WHITE),
            label(rf"read naively, \ aliasing: \ {-d['alias']['full']:.1f} dB below the note", font_size=20, color=EAR),
            label(rf"keep only the {d['keep']} harmonics below 20 kHz for that octave: \ {-d['alias']['limited']:.1f} dB", font_size=20, color=TUNE),
            label(r"so a wavetable synthesizer stores each table several times, \ fewer harmonics for each octave up", font_size=20, color=WHITE),
            label(r"the same trick as image mipmaps in graphics; \ it costs memory, \ not arithmetic", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"wavetables alias too", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Wavetables meet chapter three's problem again. <bookmark mark='a'/> The brightest cycle has forty-eight harmonics. "
            f"Play it at C six, {say(f6)} hertz, and the forty-eighth would be at {say(48 * f6 / 1000, 1)} kilohertz, far past "
            f"the limit. <bookmark mark='b'/> Read naively, the folded harmonics are only {say(-d['alias']['full'], 1)} decibels "
            f"below the note. <bookmark mark='c'/> Keep only the {say(d['keep'])} harmonics below twenty kilohertz for that "
            f"octave, and the aliasing falls to {say(-d['alias']['limited'], 1)}. <bookmark mark='d'/> So a wavetable "
            "synthesizer stores each table several times, with fewer harmonics for each octave up, <bookmark mark='e'/> the "
            "same trick as the mipmaps of computer graphics. It costs memory, not arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.25)))
            for mark, rr in zip("abcde", rows):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        items = [
            (r"PPG and Waldorf in the 1980s; \ in software, \ wavetables drawn, \ imported from recordings, \ or computed", WHITE),
            (r"one cycle cut from a voice or an instrument becomes a table: \ sampling's cousin \ (Part 52)", WHITE),
            (r"the table position becomes one more knob for envelopes and LFOs to turn", WHITE),
            (r"behind the knob, \ the same filter, \ envelopes and unison as before", WHITE),
            (r"the frontier asks the inverse: \ which settings make a given sound?", TUNE),
        ]
        rows_scene(self, r"wavetables now", items,
                   "Wavetables never went away. <bookmark mark='b'/> PPG and then Waldorf built them in the 1980s; in software they "
                   "are drawn, imported from recordings, or computed. One cycle cut from a voice or an instrument becomes a table, "
                   "sampling's cousin, which is Part 52. <bookmark mark='d'/> The table position is one more knob for envelopes and "
                   "LFOs to turn, <bookmark mark='e'/> with the same filter, envelopes and unison behind it. "
                   "<bookmark mark='f'/> And the frontier asks the inverse question: which settings make a given sound?",
                   marks="bdef")
