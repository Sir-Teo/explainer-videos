from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Comp(SoundScene):
    def construct(self):
        chapter(self, 5, r"Compressors", r"How do you make the quiet parts louder without the loud ones clipping?")
        self.idea()
        self.curves()
        self.time()
        self.pumping()
        self.quiz()
        self.punch()
        self.detectors()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"a compressor turns the level down when it is high, \ and leaves it alone when it is low", WHITE),
            (r"above a threshold, \ every 4 dB more going in gives only 1 dB more coming out: \ a ratio of 4 to 1", WHITE),
            (r"then the whole signal can be turned up: \ make-up gain", WHITE),
            (r"the result is denser and louder on average, \ with smaller swings", TUNE),
            (r"it is nonlinear and time-varying: \ its gain depends on the signal itself", GREY_A),
        ]
        rows_scene(self, r"an automatic hand on the fader", items,
                   "The second family of effects controls level. <bookmark mark='b'/> A compressor turns the level down when it is "
                   "high, and leaves it alone when it is low. <bookmark mark='c'/> Above a threshold, every four decibels more "
                   "going in gives only one decibel more coming out: a ratio of four to one. <bookmark mark='d'/> Then the whole "
                   "signal can be turned up, with make-up gain. <bookmark mark='e'/> The result is denser and louder on average, "
                   "with smaller swings. <bookmark mark='f'/> And it is nonlinear and time-varying: its gain depends on the signal "
                   "itself.", marks="bcdef")

    # ------------------------------------------------------------------
    def curves(self):
        d = load("curves")
        lv = d["levels"]
        ax = frame_axes(width=4.6, height=4.0, xlo=-60, xhi=0, ylo=-60, yhi=0, center=DOWN * 0.3 + LEFT * 1.0)
        diag = DashedLine(ax.to(-60, -60), ax.to(0, 0), color=GREY_B, stroke_width=1.5)
        cols = {"2": BLUE, "4": TUNE, "10": EAR}
        cs = VGroup(*[curve(lv, d["curves"][r], ax.to, color=cols[r], width=3) for r in ("2", "4", "10")])
        key = VGroup(*[label(rf"ratio {r} : 1", font_size=18, color=cols[r]) for r in ("2", "4", "10")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5)
        th = VGroup(DashedLine(ax.to(-20, -60), ax.to(-20, 0), color=WHITE, stroke_width=1, stroke_opacity=0.5), label(r"threshold, \ -20 dB", font_size=15, color=GREY_A).next_to(ax.to(-20, 0), UP, buff=0.1))
        knee = label(r"a 6 dB soft knee: \ the bend is gradual", font_size=16, color=GREY_A).next_to(key, DOWN, buff=0.5)
        xl = label(r"level in, \ dB", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"level out", font_size=16, color=GREY_A).next_to(ax, LEFT, buff=0.2)
        eq = MathTex(r"y = T + \frac{x - T}{R} \quad (x > T + W/2)", font_size=30).to_corner(UR, buff=0.5).shift(DOWN * 0.4)
        head = label(r"the static curve", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Draw level out against level in, in decibels. <bookmark mark='a'/> Below the threshold, minus twenty here, the line "
            "is the diagonal: nothing happens. <bookmark mark='b'/> Above it, the slope is one over the ratio: two to one "
            "gently, four to one firmly, ten to one almost flat. <bookmark mark='c'/> A soft knee bends from one slope to the "
            "other over six decibels instead of at a corner. This is the gain computer of Dimitrios Giannoulis, Michael "
            "Massberg and Joshua Reiss's 2012 design, which our compressor follows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(diag), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(th))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.4), FadeIn(key), FadeIn(eq), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(knee))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def time(self):
        d = load("curves")
        env = np.array(d["env"])
        gr = np.array(d["gr"])
        tt = np.arange(len(env)) * 120 / 48000
        a1 = frame_axes(width=10.0, height=1.6, xlo=0, xhi=1.2, ylo=0, yhi=1, center=UP * 0.9)
        a2 = frame_axes(width=10.0, height=1.6, xlo=0, xhi=1.2, ylo=0, yhi=16, center=DOWN * 1.4)
        c1 = curve(tt, env, a1.to, color=GREY_A, width=1.2)
        c2 = curve(tt, gr, a2.to, color=TUNE, width=3)
        l1 = label(r"the input: \ quiet, \ then 24 dB louder for 0.4 s, \ then quiet", font_size=17, color=GREY_A).next_to(a1, UP, buff=0.1)
        l2 = label(rf"the gain reduction, \ dB: \ it reaches {d['steady_gr']:.1f} dB", font_size=17, color=TUNE).next_to(a2, UP, buff=0.1)
        head = label(r"attack and release", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "A compressor must also decide how fast to act. <bookmark mark='a'/> Feed it a tone that jumps twenty-four decibels "
            f"for four-tenths of a second. <bookmark mark='b'/> The gain reduction rises to {say(d['steady_gr'], 1)} decibels "
            f"in about {say(d['attack_ms'])} milliseconds: the attack. When the tone falls back, it lets go more slowly, "
            f"over about {say(d['release_ms'])} milliseconds: the release. A fast attack catches every peak; a slow release "
            "avoids pumping the level up and down with every beat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(a1, c1, a2, c2), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(l1), Create(c1))
            vo.wait_until("b")
            self.play(FadeIn(a2), FadeIn(l2), Create(c2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("comp")
        c = clip("comp.two")
        card = listen_card(r"A groove, \ twice, \ at the same average loudness. \ One is compressed. \ Which?", width=9.0)
        with self.voiceover("Your turn. A groove, twice, at the same average loudness. One is compressed. Which?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 1.5)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a groove, \ twice", detail=r"Part 40's drums, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        L1, L2 = np.array(d["levels"]["plain"]), np.array(d["levels"]["compressed"])
        n = len(L1)
        a = frame_axes(width=5.0, height=1.8, xlo=0, xhi=n, ylo=-50, yhi=0, center=LEFT * 3.0 + DOWN * 1.2)
        b = frame_axes(width=5.0, height=1.8, xlo=0, xhi=n, ylo=-50, yhi=0, center=RIGHT * 3.0 + DOWN * 1.2)
        k = np.arange(n)
        sp = d["spread"]
        g = VGroup(a, curve(k, np.clip(L1, -50, 0), a.to, color=GREY_A, width=1.5), label(rf"plain: \ level wanders over {sp['plain']:.1f} dB", font_size=16, color=GREY_A).next_to(a, UP, buff=0.1),
                   b, curve(k, np.clip(L2, -50, 0), b.to, color=TUNE, width=1.5), label(rf"compressed: \ over {sp['compressed']:.1f} dB", font_size=16, color=TUNE).next_to(b, UP, buff=0.1))
        with self.voiceover(
            "The second. Its level, measured in windows of twenty milliseconds, wanders over about "
            f"{say(sp['compressed'], 1)} decibels against {say(sp['plain'], 1)} for the plain groove: the bass and the "
            "tail of each drum come up to meet the hits. It sounds thicker and more even, even at the same average loudness."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(g))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def punch(self):
        d = load("comp")
        cr = d["crest"]
        items = [
            (rf"yet the compressed groove's crest factor, \ peak over average, \ rose: \ {cr['plain']:.1f} to {cr['compressed']:.1f} dB", WHITE),
            (r"the 3 ms attack lets the first instant of every hit through before the gain comes down", WHITE),
            (r"so the clicks stay sharp while the body is turned down: \ engineers call it punch", WHITE),
            (r"a faster attack would flatten the hits too; \ a slower one would leave more of each through", TUNE),
            (r"a compressor's sound lies in its timing as much as its ratio", GREY_A),
        ]
        rows_scene(self, r"punch", items,
                   "One measurement goes the other way. <bookmark mark='b'/> The compressed groove's crest factor, its peak over its "
                   f"average, rose, from {say(cr['plain'], 1)} to {say(cr['compressed'], 1)} decibels. <bookmark mark='c'/> The "
                   "three-millisecond attack lets the first instant of every hit through before the gain comes down, "
                   "<bookmark mark='d'/> so the clicks stay sharp while the body is turned down: engineers call it punch. "
                   "<bookmark mark='e'/> A faster attack would flatten the hits too; a slower one would leave more of each "
                   "through. <bookmark mark='f'/> A compressor's sound lies in its timing as much as in its ratio.", marks="bcdef")

    # ------------------------------------------------------------------
    def detectors(self):
        items = [
            (r"what level does a compressor see? \ the peak, \ instant by instant, \ or the RMS, \ an average over tens of milliseconds", WHITE),
            (r"peak detection catches every transient; \ RMS detection follows loudness, \ as the ear does", WHITE),
            (r"feedforward compressors measure the input; \ feedback ones measure their own output, \ as many classic units did", WHITE),
            (r"optical compressors used a lamp and a photocell, \ whose slow, \ level-dependent response gave them their character", TUNE),
            (r"every one of these choices changes the sound, \ which is why engineers own several", GREY_A),
        ]
        rows_scene(self, r"what the compressor hears", items,
                   "What level does a compressor see? <bookmark mark='b'/> The peak, instant by instant, or the RMS, an average over "
                   "tens of milliseconds. Peak detection catches every transient; RMS detection follows loudness, as the ear does. "
                   "<bookmark mark='d'/> Feedforward compressors measure their input; feedback ones measure their own output, as "
                   "many classic units did. <bookmark mark='e'/> Optical compressors used a lamp and a photocell, whose slow, "
                   "level-dependent response gave them their character. <bookmark mark='f'/> Every one of these choices changes the "
                   "sound, which is why engineers own several.", marks="bdef")

    # ------------------------------------------------------------------
    def pumping(self):
        d = load("pump")
        c = clip("pump.two")
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.2, corner_radius=0.15, stroke_color=col), label(t, font_size=22, color=WHITE)).arrange(ORIGIN)
                         for t, col in ((r"release 25 ms", EAR), (r"release 400 ms", TUNE))]).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        cap = label(r"both compressed hard: \ 10 to 1 above -30 dB, \ 2 ms attack", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"release, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear what the release does. The groove compressed hard, first with a twenty-five millisecond release, then with "
            "four hundred. Listen to the bass and the hi-hat between the kicks."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"fast, \ then slow release", detail=r"Part 40's drums, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["fast"], st["slow"] - 0.4, buff=0.08)
            pulse(snd, cells[1], st["slow"], c.duration, buff=0.08)
        with self.voiceover(
            "With the fast release, the level leaps back up after every hit, and the quiet parts surge and fall: pumping, and "
            "even a little distortion on the bass, as the gain follows its waveform. With the slow release the gain hardly "
            "moves between hits, and the groove is held down evenly."
        ):
            self.play(Indicate(cells[0], color=EAR, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
