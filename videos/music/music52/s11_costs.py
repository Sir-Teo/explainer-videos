from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403

CTRL = {
    "additive, 40 sines": r"every partial's level and frequency",
    "subtractive: PolyBLEP and ladder": r"cutoff, \ resonance, \ envelopes",
    "FM, two operators": r"ratio and index",
    "FM engine, four operators": r"ratios, \ indices, \ envelopes per operator",
    "granular, 60 grains a second": r"position, \ density, \ length, \ pitch, \ scatter",
    "Karplus-Strong, tuned": r"pitch, \ decay, \ brightness",
    "waveguide clarinet": r"breath pressure, \ the reed, \ the bore",
    "modal string, 60 modes": r"each mode's frequency and decay",
    "finite-difference string": r"the physics itself: \ tension, \ stiffness, \ where it is struck",
}


class Costs(SoundScene):
    def construct(self):
        chapter(self, 10, r"What each method costs and controls", r"Which method for which job?")
        self.timings()
        self.controls()
        self.choosing()

    # ------------------------------------------------------------------
    def timings(self):
        d = load("costs")
        rows = d["rows"]
        lo, hi = np.log10(0.1), np.log10(300)
        bars = VGroup()
        for i, r in enumerate(rows):
            w = 6.0 * (np.log10(max(r["ms"], 0.1)) - lo) / (hi - lo)
            y = 2.0 - i * 0.48
            name = label(r["name"].replace("Karplus-Strong", r"Karplus--Strong"), font_size=16, color=WHITE).move_to([-3.6, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(w, 0.05), height=0.3, stroke_width=0, fill_color=TUNE, fill_opacity=0.8).move_to([-3.4 + w / 2, y, 0])
            val = label(f"{r['ms']:.1f} ms", font_size=15, color=GREY_A).next_to(bar, RIGHT, buff=0.12)
            bars.add(VGroup(name, bar, val))
        cap = label(r"time to compute one second of sound, \ in this part's code, \ on this computer \ (log scale)", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.45)
        ks = [r for r in rows if r["name"].startswith("Karplus")][0]
        add = [r for r in rows if r["name"].startswith("additive")][0]
        md = [r for r in rows if r["name"].startswith("modal")][0]
        fd = [r for r in rows if r["name"].startswith("finite")][0]
        head = label(r"what one second costs", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Time every method for one second of sound, in this part's code, on this computer. <bookmark mark='a'/> The "
            f"cheapest is Karplus-Strong, {say(ks['ms'], 1)} milliseconds: one delay line and one average. Two-operator FM is "
            f"next, a few sines. <bookmark mark='b'/> At the other end, forty sines summed directly take {say(add['ms'])} "
            f"milliseconds, sixty decaying modes {say(md['ms'])}, the bead simulation {say(fd['ms'])}. Every one runs "
            "faster than real time, but multiply by sixteen voices and a dozen tracks, and the order matters, as it did when a "
            "DX7 had to run on 1983's chips."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(VGroup(*[b[0] for b in bars])))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[1], LEFT) for b in bars], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[b[2] for b in bars])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def controls(self):
        d = load("costs")
        rows = VGroup()
        for r in d["rows"]:
            rows.add(VGroup(label(r["name"].replace("Karplus-Strong", r"Karplus--Strong"), font_size=16, color=TUNE), label(CTRL[r["name"]], font_size=16, color=WHITE)))
        rows.arrange(DOWN, buff=0.22)
        for r in rows:
            r[0].move_to([-2.0, r.get_y(), 0], aligned_edge=RIGHT)
            r[1].move_to([-1.6, r.get_y(), 0], aligned_edge=LEFT)
        rows.move_to(DOWN * 0.2)
        head = label(r"what a player gets to turn", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Cost is half the story; the other half is what a player gets to turn. <bookmark mark='a'/> Additive and modal "
            "synthesis offer a knob for every partial: complete, and overwhelming. Subtractive offers a few musical ones: "
            "cutoff, resonance, envelopes. FM offers ratios and indices, powerful and unintuitive. Granular synthesis offers "
            "time itself. <bookmark mark='b'/> And the physical models offer the physics: breath, bow and string, the things a "
            "player of the real instrument already knows how to control."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:5]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[5:]], lag_ratio=0.2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choosing(self):
        items = [
            (r"to copy a recorded instrument exactly, \ within its range: \ sample it", WHITE),
            (r"to play an instrument that reacts like one, \ breath, \ bow, \ hammer: \ model its physics", WHITE),
            (r"to design sounds nobody has heard: \ subtractive, \ FM, \ wavetables, \ grains", WHITE),
            (r"to transform a recording: \ grains and spectral models", WHITE),
            (r"real instruments in software mix all of these: \ a sampled attack, \ a modelled resonance, \ a filtered tail", TUNE),
        ]
        rows_scene(self, r"which method for which job", items,
                   "So which method for which job? <bookmark mark='b'/> To copy a recorded instrument exactly within its range, "
                   "sample it. <bookmark mark='c'/> To play an instrument that reacts like one, to breath, bow or hammer, model its "
                   "physics. <bookmark mark='d'/> To design sounds nobody has heard, use subtraction, FM, wavetables or grains. "
                   "<bookmark mark='e'/> To transform a recording, use grains and spectral models. <bookmark mark='f'/> And real "
                   "instruments in software mix them all: a sampled attack, a modelled resonance, a filtered tail.", marks="bcdef")
