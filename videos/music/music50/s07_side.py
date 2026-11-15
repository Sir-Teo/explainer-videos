from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Side(SoundScene):
    def construct(self):
        chapter(self, 6, r"Limiters, \ gates and sidechains", r"What else can a gain that follows a signal do?")
        self.family()
        self.duck()
        self.gate_()
        self.uses()
        self.lookahead()

    # ------------------------------------------------------------------
    def family(self):
        items = [
            (r"a limiter: \ a compressor with an infinite ratio and an instant attack, \ a ceiling nothing passes", WHITE),
            (r"often with look-ahead: \ the signal is delayed a few milliseconds so the gain can come down before the peak", WHITE),
            (r"a gate: \ the reverse, \ below a threshold the level is cut, \ silencing hiss and spill between notes", WHITE),
            (r"an expander: \ a gentle gate, \ widening the dynamics instead of narrowing them", TUNE),
            (r"Part 57 meets the limiter again, \ in mastering's loudness war", GREY_A),
        ]
        rows_scene(self, r"the family", items,
                   "The compressor has relatives. <bookmark mark='b'/> A limiter is a compressor with an infinite ratio and an "
                   "instant attack: a ceiling nothing passes. <bookmark mark='c'/> It often looks ahead: the signal is delayed a few "
                   "milliseconds, so the gain can come down before the peak arrives. <bookmark mark='d'/> A gate is the reverse: "
                   "below a threshold the level is cut, silencing hiss and spill between notes. <bookmark mark='e'/> An expander is "
                   "a gentle gate, widening the dynamics instead of narrowing them. <bookmark mark='f'/> Part 57 meets the limiter "
                   "again, in mastering's loudness war.", marks="bcdef")

    # ------------------------------------------------------------------
    def duck(self):
        d = load("duck")
        c = clip("duck.two")
        gr = np.array(d["gr"])
        tt = np.arange(len(gr)) * 240 / 48000
        ax = frame_axes(width=9.0, height=2.0, xlo=0, xhi=tt[-1], ylo=0, yhi=max(gr.max(), 1) * 1.1, center=DOWN * 1.0)
        cv = curve(tt, gr, ax.to, color=TUNE, width=3)
        beats = VGroup(*[Line(ax.to(k * d["beat"], 0), ax.to(k * d["beat"], gr.max() * 1.1), color=EAR, stroke_width=2, stroke_opacity=0.6) for k in range(4)])
        lab = label(r"the pad's gain reduction, \ dB, \ over one bar; \ pink: \ the kicks", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.15)
        diag = VGroup(RoundedRectangle(width=2.2, height=0.7, corner_radius=0.1, stroke_color=EAR), label(r"kick", font_size=18, color=EAR)).arrange(ORIGIN).move_to(UP * 1.6 + LEFT * 3.5)
        comp = VGroup(RoundedRectangle(width=3.4, height=0.7, corner_radius=0.1, stroke_color=TUNE), label(r"compressor on the pad", font_size=18, color=TUNE)).arrange(ORIGIN).move_to(UP * 1.6 + RIGHT * 1.5)
        arrow = Arrow(diag.get_right(), comp.get_left(), buff=0.1, color=GREY_A, stroke_width=3)
        sc = label(r"sidechain: \ the kick drives the detector", font_size=16, color=GREY_A).next_to(arrow, UP, buff=0.1)
        head = label(r"a sidechain", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A compressor's detector can listen to a different signal from the one it turns down: a sidechain. Here the kick "
            "drum drives a compressor on a sustained pad. Every kick pushes the pad down, and it swells back between them: "
            "the pumping sound of dance music, and the way engineers keep a bass out of the kick's way. Hear the pad plain, "
            "then ducked."
        ):
            self.play(FadeIn(head), FadeIn(diag), FadeIn(comp), GrowArrow(arrow), FadeIn(sc), FadeIn(ax), FadeIn(beats), FadeIn(lab), Create(cv))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"plain, \ then ducked", kind="synthesized", detail=r"Part 40's kick and pad", corner=DL, tag_corner=DR)
            pulse(snd, diag, st["plain"], st["ducked"] - 0.3, buff=0.08)
            pulse(snd, comp, st["ducked"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"de-essing: \ a compressor keyed by the sibilant band, \ taming a singer's `s' sounds", WHITE),
            (r"ducking: \ music that dips when a presenter speaks", WHITE),
            (r"multiband compression: \ separate compressors for the lows, \ mids and highs", WHITE),
            (r"broadcast processing: \ chains of them, \ so every station sounds equally loud", TUNE),
            (r"all are one idea: \ a gain that follows a level", GREY_A),
        ]
        rows_scene(self, r"more uses", items,
                   "The idea spreads. <bookmark mark='b'/> De-essing is a compressor keyed by the sibilant band, taming a singer's "
                   "s sounds. <bookmark mark='c'/> Ducking makes music dip when a presenter speaks. <bookmark mark='d'/> Multiband "
                   "compression splits the sound and compresses the lows, mids and highs separately. <bookmark mark='e'/> Broadcast "
                   "processors chain several, so that every station sounds equally loud. <bookmark mark='f'/> All of them are one "
                   "idea: a gain that follows a level.", marks="bcdef")

    # ------------------------------------------------------------------
    def gate_(self):
        d = load("gate")
        c = clip("gate.two")
        L1, L2 = np.array(d["levels"]["plain"]), np.array(d["levels"]["gated"])
        n = len(L1)
        a = frame_axes(width=5.0, height=1.8, xlo=0, xhi=n, ylo=-80, yhi=0, center=LEFT * 3.0 + DOWN * 0.6)
        b = frame_axes(width=5.0, height=1.8, xlo=0, xhi=n, ylo=-80, yhi=0, center=RIGHT * 3.0 + DOWN * 0.6)
        k = np.arange(n)
        g = VGroup(VGroup(a, curve(k, np.clip(L1, -80, 0), a.to, color=GREY_A, width=1.5), label(r"plain: \ the hiss fills every gap", font_size=16, color=GREY_A).next_to(a, UP, buff=0.1)),
                   VGroup(b, curve(k, np.clip(L2, -80, 0), b.to, color=TUNE, width=1.5), label(r"gated: \ silence between the hits", font_size=16, color=TUNE).next_to(b, UP, buff=0.1)))
        cap = label(r"level every 20 ms, \ dB", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"a gate", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear a gate. Six snare hits over a steady hiss, as if from a noisy old recording. Plain, the hiss fills every "
            "gap. Gated, the level is cut whenever it falls below the threshold, and the gaps go silent."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"plain, \ then gated", detail=r"Part 40's snare, \ with hiss", corner=DL, tag_corner=DR)
            pulse(snd, g[0], st["plain"], st["gated"] - 0.3, buff=0.1)
            pulse(snd, g[1], st["gated"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lookahead(self):
        items = [
            (r"a limiter must never let a sample through above its ceiling, \ yet must not distort", WHITE),
            (r"with no warning, \ the only way is to clip, \ and clipping is distortion", WHITE),
            (r"so the signal is delayed a few milliseconds while the detector reads ahead", WHITE),
            (r"the gain starts falling before the peak arrives, \ smoothly, \ and is just low enough when it does", TUNE),
            (r"the cost is latency: \ fine for mastering, \ a problem on stage", GREY_A),
        ]
        rows_scene(self, r"looking ahead", items,
                   "How does a limiter keep its promise? <bookmark mark='b'/> It must never let a sample through above its ceiling, "
                   "yet it must not distort. <bookmark mark='c'/> With no warning, the only way is to clip, and clipping is "
                   "distortion. <bookmark mark='d'/> So the signal is delayed a few milliseconds while the detector reads ahead, "
                   "<bookmark mark='e'/> and the gain starts falling before the peak arrives, smoothly, reaching just low enough as "
                   "it does. <bookmark mark='f'/> The cost is latency: fine for mastering, a problem on stage.", marks="bcdef")
