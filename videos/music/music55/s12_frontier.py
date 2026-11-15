from __future__ import annotations

import math

from videos.music.music55.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ personal ears and real-time waves", r"Can a phone know your ears, \ and a game simulate a cathedral?")
        self.ears()
        self.cost()
        self.waves()
        self.zones()
        self.problem()

    # ------------------------------------------------------------------
    def ears(self):
        items = [
            (r"everyone's HRTF is different; \ measuring one takes an anechoic room and an hour", WHITE),
            (r"compute it instead: \ scan the head and ears, \ and solve the wave equation round the mesh \ (the boundary-element method)", WHITE),
            (r"or predict it: \ from photographs of the ear, \ or a phone's depth camera, \ by models trained on measured databases", WHITE),
            (r"or choose it: \ play a few test sounds and let the listener pick the set that sounds most real", WHITE),
            (r"since 2022, \ phones offer personalized spatial audio from an ear scan; \ how well it works is an open question", TUNE),
        ]
        rows_scene(self, r"personal ears", items,
                   "The first frontier is the listener's own ears. <bookmark mark='b'/> Everyone's HRTF is different, and measuring "
                   "one takes an anechoic room and an hour of keeping still. <bookmark mark='c'/> So compute it instead: scan the "
                   "head and ears into a mesh, and solve the wave equation round it, by the boundary-element method, frequency by "
                   "frequency. <bookmark mark='d'/> Or predict it, from photographs of the ear or a phone's depth camera, with "
                   "models trained on measured databases. <bookmark mark='e'/> Or choose it: play a few test sounds, and let the "
                   "listener pick the set that sounds most real. <bookmark mark='f'/> Since 2022 phones have offered personalized "
                   "spatial audio from an ear scan. How well any of these works, compared with one's own measured ears, is an open "
                   "question.", marks="bcdef")

    # ------------------------------------------------------------------
    def cost(self):
        fs = [250, 500, 1000, 2000, 4000, 8000, 16000]
        bars = VGroup()
        for i, f in enumerate(fs):
            lg = 4 * math.log10(f / 250)
            h = 0.4 + 0.5 * lg
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=TUNE if f <= 1000 else EAR, fill_opacity=0.8).move_to([-4.2 + 1.3 * i, -2.0 + h / 2, 0])
            rel = (f / 250) ** 4
            bars.add(VGroup(b, label(rf"$\times${rel:,.0f}" if rel < 1e6 else rf"$\times 1.7\times 10^7$", font_size=14, color=WHITE).next_to(b, UP, buff=0.08),
                            label(f"{f:,} Hz" if f < 1000 else f"{f // 1000} kHz", font_size=15, color=GREY_A).next_to([-4.2 + 1.3 * i, -2.0, 0], DOWN, buff=0.1)))
        xl = label(r"the top frequency of a wave simulation, \ and its cost relative to 250 Hz \ (a logarithmic scale)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        eq = MathTex(r"\text{cost} \propto \Bigl(\frac{V}{\lambda^3}\Bigr)\Bigl(\frac{T}{\Delta t}\Bigr) \propto V\,T\,f^4", font_size=34, color=TUNE).to_edge(UP, buff=1.0)
        head = label(r"why waves are expensive", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second frontier is simulation fast enough to hear while you move. <bookmark mark='a'/> A wave simulation's "
            "cost is the number of grid points, the volume over the wavelength cubed, times the number of time steps, the "
            "duration over the step: the volume times the duration times the frequency to the fourth. <bookmark mark='b'/> Each "
            "octave higher costs sixteen times as much: from two hundred and fifty hertz to sixteen kilohertz, seventeen "
            "million times. That is why the treble is left to rays."
        ) as vo:
            self.play(FadeIn(head), FadeIn(xl), FadeIn(ghost(bars, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def waves(self):
        items = [
            (r"precompute: \ simulate the waves offline from many points in a game's world, \ and store a few numbers per pair of points", WHITE),
            (r"Raghuvanshi and Snyder \ (2014): \ loudness, \ reverberation and the direction a sound seems to come from, \ round corners and through doors", WHITE),
            (r"graphics processors: \ wave simulation of a room at interactive rates, \ for the bass and middle", WHITE),
            (r"learned models: \ networks trained on simulations that predict a room's response from its shape, \ or from a photograph", WHITE),
            (r"the goal: \ a hall, \ a cathedral, \ a forest, \ simulated as you walk through it", TUNE),
        ]
        rows_scene(self, r"real-time waves", items,
                   "How is it done in real time? <bookmark mark='b'/> By precomputing: simulate the waves offline from many points in "
                   "a game's world, and store a few numbers for each pair of points. <bookmark mark='c'/> Nikunj Raghuvanshi and John "
                   "Snyder's method of 2014 stores loudness, reverberation and the direction a sound seems to come from, so sound "
                   "bends round corners and through doors as it should. <bookmark mark='d'/> By graphics processors, which now "
                   "simulate a room's waves at interactive rates, for the bass and middle. <bookmark mark='e'/> And by learned "
                   "models, networks trained on simulations to predict a room's response from its shape, or from a photograph of "
                   "it. <bookmark mark='f'/> The goal: a hall, a cathedral, a forest, simulated as you walk through it.", marks="bcdef")

    # ------------------------------------------------------------------
    def zones(self):
        items = [
            (r"room correction: \ measure the room at the seats, \ and correct the loudspeakers' response where it can be corrected", WHITE),
            (r"sound zones: \ arrays that play loud in one seat of a car and quiet in the next", WHITE),
            (r"active acoustics: \ microphones and loudspeakers in the walls that change a hall's reverberation at the turn of a knob", WHITE),
            (r"the room itself is becoming programmable", TUNE),
        ]
        rows_scene(self, r"rooms you can program", items,
                   "And the room itself is becoming something to program. <bookmark mark='b'/> Room correction measures the room "
                   "at the seats and corrects the loudspeakers where a correction is possible, cutting peaks, leaving nodes alone. "
                   "<bookmark mark='c'/> Sound zones use arrays to play loudly in one seat of a car and quietly in the next. "
                   "<bookmark mark='d'/> Active acoustics put microphones and loudspeakers in the walls of a hall, and change its "
                   "reverberation at the turn of a knob, from a lecture room to a cathedral. <bookmark mark='e'/> Sabine's cushions, "
                   "now in software.", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take measured HRTFs for many people, \ with scans of their heads and ears", WHITE),
            (r"predict each person's from less: \ a photograph, \ a depth scan, \ a few chosen test sounds", WHITE),
            (r"test the prediction by listening: \ front-back reversals, \ elevation, \ externalization, \ against the person's own", WHITE),
            (r"$\bigstar$ \ research problem: \ what is the least you need to know about a listener's ears to render space for them as well as their own HRTF would?", EAR),
            (r"an answer would decide how everyone hears spatial audio", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take measured HRTFs for many people, with scans of their heads "
            "and ears. <bookmark mark='b'/> Predict each person's from less: a photograph, a depth scan, a few chosen test "
            "sounds. <bookmark mark='c'/> Test the prediction by listening: front-back reversals, elevation and "
            "externalization, against the person's own. <bookmark mark='d'/> The question: what is the least you need to know "
            "about a listener's ears to render space for them as well as their own HRTF would? <bookmark mark='e'/> An answer "
            "would decide how everyone hears spatial audio."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
