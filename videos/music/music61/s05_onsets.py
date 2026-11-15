from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Onsets(SoundScene):
    def construct(self):
        chapter(self, 4, r"Where notes begin", r"How does a machine hear a note start?")
        self.flux()
        self.heard()
        self.tradeoff()
        self.hard()

    # ------------------------------------------------------------------
    def flux(self):
        lines = VGroup(
            label(r"a note's start: \ energy appears, \ suddenly, \ in bands where there was little", font_size=21, color=WHITE),
            MathTex(r"\mathrm{SF}(n) = \sum_k \max\!\Big(0,\ \log(1 + C|X_{n,k}|) - \log(1 + C|X_{n-1,k}|)\Big)", font_size=34, color=TUNE),
            label(r"log compression: \ a quiet note's start counts as well as a loud one's", font_size=19, color=GREY_A),
            label(r"half-wave rectification: \ only increases count; \ a note ending is not a note beginning", font_size=19, color=GREY_A),
            label(r"then peak picking: \ a local maximum, \ above the local mean, \ not too soon after the last", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.38)
        head = label(r"spectral flux", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Notes have to begin somewhere. <bookmark mark='a'/> A note's start is energy appearing, suddenly, in frequency "
            "bands where there was little. <bookmark mark='b'/> Spectral flux measures exactly that: from each frame to the next, "
            "add up the increases of the log-compressed spectrum. <bookmark mark='c'/> The logarithm lets a quiet note's start "
            "count as well as a loud one's. <bookmark mark='d'/> Only increases count: a note ending is not a note beginning. "
            "<bookmark mark='e'/> Then pick peaks: a local maximum, above the local mean, and not too soon after the last one."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("onsets")
        c = clip("onsets.two")
        panels = VGroup()
        for i, (inst, name, col) in enumerate((("piano", r"piano", TUNE), ("strings", r"bowed strings", BLUE))):
            o = d[inst]
            t, odf = np.array(o["t"]), np.array(o["odf"])
            ax = frame_axes(width=11.0, height=1.5, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=[0, 1.1 - 2.6 * i, 0])
            cv = curve(t, odf, ax.to, color=col, width=2)
            refs = VGroup(*[Line(ax.to(r, 0), ax.to(r, -0.18), color=GREY_B, stroke_width=3) for r in o["ref"]])
            ests = VGroup(*[Triangle(fill_color=EAR, fill_opacity=1, stroke_width=0).scale(0.07).rotate(PI).move_to(ax.to(e, 1.1)) for e in o["est"]])
            tag = label(rf"{name}: \ F = {o['f']:.2f} \ ({o['hits']} of {len(o['ref'])} found, \ {len(o['est'])} reported)", font_size=16, color=col).next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
            panels.add(VGroup(ax, cv, refs, ests, tag))
        key = label(r"grey ticks: \ where notes really begin; \ red marks: \ what the detector found, \ within 50 ms to count", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(r"the Tune's opening, \ heard and detected", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover("Hear the Tune's opening, repeated notes and all, on the piano and then on bowed strings, with the flux and the detected onsets drawn under each."):
            self.play(FadeIn(head), FadeIn(VGroup(*[VGroup(p[0], p[2]) for p in panels])), FadeIn(key))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"piano, \ then strings", kind="physical model", detail=r"Parts 38 and 9", corner=DL, tag_corner=DR)
            for i, k in enumerate(("piano", "strings")):
                snd.show(panels[i][1], panels[i][3])
                snd.drive(panels[i][1], lambda m, t, s0=st[k]: m.set_opacity(1.0 if t >= s0 else 0.0))
                snd.drive(panels[i][3], lambda m, t, s0=st[k]: m.set_opacity(1.0 if t >= s0 else 0.0))
                pulse(snd, panels[i][0], st[k], st["strings"] - 0.3 if k == "piano" else c.duration, buff=0.1)
        self.add(panels[0][1], panels[0][3], panels[1][1], panels[1][3])
        p, s = d["piano"], d["strings"]
        with self.voiceover(
            f"The piano's hammers make sharp peaks, and the detector finds {say(p['hits'])} of {say(len(p['ref']))} onsets. A bow "
            f"starts a note gradually, and a repeated note on the strings barely changes the spectrum at all: {say(s['hits'])} of "
            f"{say(len(s['ref']))}."
        ):
            self.play(FadeIn(panels[0][4]), FadeIn(panels[1][4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tradeoff(self):
        d = load("onsets")
        ax = frame_axes(width=5.6, height=3.4, xlo=0, xhi=1.02, ylo=0, yhi=1.02, center=DOWN * 0.4 + LEFT * 1.0)
        xt = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 0.5, 1)])
        yt = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xl = label(r"recall", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"precision", font_size=15, color=GREY_A).rotate(PI / 2).next_to(yt, LEFT, buff=0.15)
        curves = VGroup()
        for inst, col in (("piano", TUNE), ("strings", BLUE)):
            sw = d[inst]["sweep"]
            pts = [ax.to(z["recall"], z["precision"]) for z in sw]
            curves.add(VGroup(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts), *[Dot(q, radius=0.05, color=col) for q in pts]))
        key = VGroup(label(r"piano", font_size=17, color=TUNE), label(r"bowed strings", font_size=17, color=BLUE),
                     label(r"each dot: \ one threshold, \ from 0.01 to 0.4", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.6)
        best = {k: max(d[k]["sweep"], key=lambda z: z["f"]) for k in ("piano", "strings")}
        note = label(rf"best F: \ piano {best['piano']['f']:.2f} \ (threshold {best['piano']['delta']:g}); \ strings {best['strings']['f']:.2f} \ (threshold {best['strings']['delta']:g})", font_size=16, color=WHITE).to_edge(DOWN, buff=0.3)
        head = label(r"one threshold, \ two kinds of error", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every detector has a threshold, and it trades one error for another. <bookmark mark='a'/> Lower it, and the "
            "detector finds more of the real onsets, but reports more false ones; raise it, and it reports fewer, missing more. "
            "Here is the trade, threshold by threshold, for the piano. <bookmark mark='b'/> And for the bowed strings, whose "
            "curve never reaches the piano's corner: no threshold separates their gentle starts from the swells within notes. "
            f"<bookmark mark='c'/> The best F-measures are {say(best['piano']['f'], 2)} and {say(best['strings']['f'], 2)}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(key[2]))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hard(self):
        items = [
            (r"soft onsets: \ bowed, \ blown and sung notes swell rather than strike", WHITE),
            (r"repeated notes: \ the same pitch again changes little but the loudness", WHITE),
            (r"vibrato and glides: \ pitch changes that are not new notes", WHITE),
            (r"so onset detectors add pitch and phase, \ and networks learn onsets from examples \ (Chapter 10's Onsets and Frames)", TUNE),
        ]
        rows_scene(self, r"what makes onsets hard", items,
                   "What makes onsets hard? <bookmark mark='b'/> Soft onsets: bowed, blown and sung notes swell rather than strike. "
                   "<bookmark mark='c'/> Repeated notes: the same pitch again changes little but the loudness. "
                   "<bookmark mark='d'/> Vibrato and glides: pitch changes that are not new notes. <bookmark mark='e'/> So onset "
                   "detectors add pitch and phase information, and networks learn onsets from examples, as Onsets and Frames does "
                   "in Chapter 10.", marks="bcde")
