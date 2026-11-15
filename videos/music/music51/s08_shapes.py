from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


class Shapes(SoundScene):
    def construct(self):
        chapter(self, 7, r"Pulse width, \ sync and unison", r"How do you make one oscillator move?")
        self.pulse_width()
        self.sync()
        self.heard()
        self.unison()
        self.unison_heard()
        self.history()

    # ------------------------------------------------------------------
    def pulse_width(self):
        d = load("pwmsync")
        cells = VGroup()
        for wd, t in (("0.5", r"50\%: \ a square"), ("0.25", r"25\%"), ("0.1", r"10\%")):
            w = float(wd)
            ph = np.linspace(0, 2, 400)
            ys = np.where((ph % 1.0) < w, 1.0, -1.0)
            wv = wave_path(ys, width=3.0, height=0.9, color=TUNE, stroke=2.5)
            bars = harm_bars(d["widths"][wd], width=0.1, gap=0.15, floor=-40.0, height=1.5, color=BLUE, labels=False)
            cells.add(VGroup(label(t, font_size=20, color=WHITE), wv, bars).arrange(DOWN, buff=0.35))
        cells.arrange(RIGHT, buff=0.8).move_to(UP * 0.1)
        eq = MathTex(r"|a_k| \propto \frac{|\sin(\pi k w)|}{k}", font_size=34).to_edge(DOWN, buff=1.0)
        note = label(r"a zero wherever $kw$ is a whole number: \ every 2nd harmonic at 50\%, \ every 4th at 25\%, \ every 10th at 10\%", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the pulse's width is a knob", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A pulse wave is high for a fraction w of each cycle, low for the rest. <bookmark mark='a'/> At half, it is the "
            "square: odd harmonics only. <bookmark mark='b'/> At a quarter, every fourth harmonic vanishes; at a tenth, every "
            "tenth, and the sound turns thin and nasal. <bookmark mark='c'/> The rule is one line: the k-th harmonic's size "
            "goes as the sine of pi k w, over k, which is zero wherever k times w is a whole number. Move w slowly with an LFO "
            "and the zeros sweep through the harmonics: pulse-width modulation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(cells[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sync(self):
        d = load("pwmsync")
        m = np.array(d["master"])
        mw = wave_path(m, width=3.4, height=0.9, color=GREY_A, stroke=2).move_to(UP * 1.6)
        ml = label(r"the master, \ two cycles", font_size=17, color=GREY_A).next_to(mw, LEFT, buff=0.4)
        cells = VGroup()
        for r in ("1.5", "2.5", "3.7"):
            cells.add(VGroup(wave_path(np.array(d["snaps"][r]), width=3.4, height=0.9, color=EAR, stroke=2.5), label(rf"slave at {r} times", font_size=16, color=EAR)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.4)
        note = label(r"the slave restarts with every master cycle: \ the pitch stays the master's, \ the shape changes", font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"hard sync", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hard sync ties two oscillators together. <bookmark mark='a'/> The master runs at the note. The slave runs at its "
            "own frequency, but every time the master starts a cycle, the slave is forced to start one too. "
            "<bookmark mark='b'/> At one and a half times the master, the slave gets through one ramp and half of another before "
            "it is cut short; at two and a half, two and a half; at three point seven, nearly four. <bookmark mark='c'/> The "
            "result always repeats at the master's rate, so the pitch stays put, while the shape, and so the harmonics, change "
            "as the slave's frequency moves: a tearing, vocal sweep. Each restart is a jump, so a clean digital sync needs "
            "Brandt's band-limited steps; here we run four times the rate and filter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(mw), FadeIn(ml))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(cc) for cc in cells], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pwmsync")
        c = clip("pwmsync.two")
        cells = choice_boxes([r"PWM: \ 50\% to 8\%", r"sync: \ 1 to 5 times"], width=4.0, buff=1.0, colors=[TUNE, EAR]).move_to(UP * 0.4)
        head = label(r"pulse width and sync, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"both on C3, \ 131 Hz; \ the pitch never changes", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear both on one held C. First the pulse width swinging from a half to eight per cent and back; then hard sync, "
            "the slave sweeping from one to five times the master and back."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"PWM, \ then sync", kind="synthesized", detail=r"one held C", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["pwm"], st["sync"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["sync"], c.duration, buff=0.08)
        with self.voiceover(
            "Pulse-width modulation gives a slow, chorus-like movement, the zeros sweeping through the spectrum, with a reedy "
            "nasal tone at the narrow end. Sync is harsher: a resonant, tearing sweep, like a filter but brighter, the sound "
            "of a thousand synth leads."
        ):
            self.play(Indicate(cells[1], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unison(self):
        d = load("unison")
        f8 = d["f8"]
        ax = frame_axes(width=9.0, height=2.2, xlo=f8 - 30, xhi=f8 + 30, ylo=0, yhi=1.1, center=DOWN * 0.2)
        one = stems([f8], [1.0], ax.to, color=GREY_A, r=0.07)
        sev = stems(d["lines"], [1 / np.sqrt(7) * 2.2] * 7, ax.to, color=TUNE, r=0.06)
        xt = VGroup(*[label(f"{v:.0f}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (f8 - 20, f8, f8 + 20)])
        xl = label(r"Hz, \ around the 8th harmonic of C3", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        t1 = label(r"one oscillator: \ one line", font_size=17, color=GREY_A).to_corner(UL, buff=0.6).shift(DOWN * 0.8)
        t2 = label(rf"seven, \ spread over 36 cents: \ seven lines over {d['beat_hz']:.0f} Hz, \ beating", font_size=17, color=TUNE).next_to(t1, DOWN, buff=0.2, aligned_edge=LEFT)
        note = label(r"the spread grows with the harmonic: \ the top of the spectrum shimmers most", font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"unison: \ many oscillators, \ slightly apart", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The last trick is to use many oscillators on one note, slightly detuned: unison. <bookmark mark='a'/> One sawtooth "
            "has one line at each harmonic; here is its eighth, near a kilohertz. <bookmark mark='b'/> Seven sawtooths spread "
            f"over thirty-six cents put seven lines there, over {say(d['beat_hz'])} hertz, and they beat against each other, "
            "never twice the same. <bookmark mark='c'/> The spread in hertz grows with the harmonic, so the top of the "
            "spectrum shimmers most: the same thickening that sixteen violins give in Part 41, made by arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeOut(one), FadeIn(sev), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unison_heard(self):
        d = load("unison")
        c = clip("unison.two")
        cells = choice_boxes([r"one a note", r"seven a note"], width=3.6, buff=1.0, colors=[GREY_A, TUNE]).move_to(UP * 0.4)
        cap = label(r"a C major chord: \ C3, \ E3, \ G3, \ C4", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a supersaw, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("A C major chord on one sawtooth a note, then on seven."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one, \ then seven", kind="synthesized", detail=r"sawtooths", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["one"], st["seven"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["seven"], c.duration, buff=0.08)
        with self.voiceover(
            "The single sawtooths are clear and a little buzzy, every note exact. The seven-voice chord is wide and moving, a "
            "wash. Roland's JP-8000 of 1996 offered exactly this, seven sawtooths a note, as its supersaw, and trance music "
            "built itself on it."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"an analogue oscillator drifts: \ its pitch wanders by cents as it warms", WHITE),
            (r"two of them never quite agree, \ so every analogue chord had a little unison in it", WHITE),
            (r"early digital synthesizers were exact, \ and sounded thin: \ designers added drift back on purpose", WHITE),
            (r"virtual analogue: \ the 1990s' name for imitating circuits, \ flaws and all", TUNE),
            (r"what to imitate, \ and what to improve, \ is still a matter of taste", GREY_A),
        ]
        rows_scene(self, r"perfect and imperfect", items,
                   "Unison began as a flaw. <bookmark mark='b'/> An analogue oscillator drifts; its pitch wanders by cents as it "
                   "warms. <bookmark mark='c'/> Two of them never quite agree, so every analogue chord had a little unison in it. "
                   "<bookmark mark='d'/> Early digital synthesizers were exact, and sounded thin beside them, so designers added the "
                   "drift back on purpose. <bookmark mark='e'/> Virtual analogue was the 1990s' name for imitating the circuits, "
                   "flaws and all. <bookmark mark='f'/> What to imitate, and what to improve, is still a matter of taste.",
                   marks="bcdef")
