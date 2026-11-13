from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Reed(SoundScene):
    def construct(self):
        chapter(self, 2, r"A valve that pressure closes", r"What is the reed doing?", lit=(1863, 1983), extra=((1963, r"Backus measures the clarinet reed"),))
        self.valve()
        self.loop()
        self.harder()
        self.why_a_third()

    # ------------------------------------------------------------------
    def mouthpiece(self, gap=0.22):
        body = Polygon(LEFT * 2.6 + UP * 0.55, RIGHT * 2.6 + UP * 0.55, RIGHT * 2.6 + DOWN * 0.55, LEFT * 1.2 + DOWN * 0.55, color=GREY_B, stroke_width=3)
        reed = Line(LEFT * 2.6 + UP * (0.55 - gap), LEFT * 0.9 + DOWN * 0.55, color=REED, stroke_width=7)
        lay = Line(LEFT * 2.6 + UP * 0.55, LEFT * 1.2 + DOWN * 0.55, color=GREY_B, stroke_width=3).set_opacity(0)
        return VGroup(body, reed, lay)

    def valve(self):
        d = load("reed")
        m = self.mouthpiece().move_to(LEFT * 3.3 + UP * 1.0)
        names = VGroup(label(r"the reed: \ a springy blade of cane", font_size=24, color=REED).next_to(m, DOWN, buff=0.3),
                       label(r"the player's mouth", font_size=24, color=GREY_A).next_to(m, UP, buff=0.2).align_to(m, LEFT),
                       label(r"to the pipe", font_size=24, color=AIR).next_to(m, UP, buff=0.2).align_to(m, RIGHT))
        g = axes([-0.1, 1.2], [-0.02, 0.16], x_length=5.4, y_length=3.4, xlabel=r"pressure across the reed, \ as a fraction of the pressure that shuts it", ylabel=r"flow through the gap", xticks=[0, 0.33, 0.67, 1.0],
                 yticks=[], xfmt=lambda v: {0: "0", 0.33: r"\tfrac13", 0.67: r"\tfrac23", 1.0: "1"}[round(v, 2)], font_size=20)
        g.move_to(RIGHT * 3.5 + DOWN * 0.4)
        mask = np.asarray(d["dp"]) >= 0
        cu = curve_from(g, np.asarray(d["dp"])[mask], np.asarray(d["flow"])[mask], REED)
        top = DashedLine(g.ax.c2p(1 / 3, 0), g.ax.c2p(1 / 3, 0.1348), color=GREY_B, stroke_width=1.5)
        up = label(r"the rising side: \\ more pressure, \ more flow", font_size=26, color=GOOD).move_to(LEFT * 3.5 + DOWN * 1.3)
        down = label(r"the falling side: \\ more pressure, \ \emph{less} flow. \ The gap is closing.", font_size=26, color=BAD).move_to(LEFT * 3.5 + DOWN * 2.5)
        shut = label(r"shut", font_size=22, color=GREY_B).next_to(g.ax.c2p(1.0, 0.0), UP, buff=0.1)
        with self.voiceover(
            "So a reed closes one end of the pipe. But it does a second job, and that is the one that makes "
            "the sound. <bookmark mark='a'/> A clarinet's reed is a thin blade of cane, held against the "
            "mouthpiece so that a narrow gap is left. The player's breath has to get through that gap. Blow, "
            "and the pressure in the mouth pushes air through; but the same pressure also pushes on the back "
            "of the reed and bends it towards the mouthpiece, narrowing the gap. <bookmark mark='b'/> Plot the "
            "flow of air against the pressure difference across the reed. At first, more pressure means more "
            "flow, as through any hole. <bookmark mark='c'/> But the gap is closing all the while, and beyond a "
            "certain point the narrowing wins: more pressure means less flow. Push hard enough and the reed "
            "is flat against the mouthpiece, and nothing gets through. The top of the curve is at exactly one "
            "third of the pressure that shuts the reed. Remember that number. <bookmark mark='d'/> And "
            "remember where you have seen this shape: it is the rosin of Part 7, whose grip fell as the "
            "string began to slide. A valve that passes less when pushed harder is what turns a steady push "
            "into a vibration."
        ) as vo:
            self.play(FadeIn(m), FadeIn(names[1]), FadeIn(names[2]))
            vo.wait_until("a")
            self.play(FadeIn(names[0]), Indicate(m[1], color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(cu), run_time=2.5)
            self.play(FadeIn(up))
            vo.wait_until("c")
            self.play(FadeIn(down), FadeIn(shut), Create(top))
            vo.wait_until("d")
            self.play(Indicate(cu, color=WHITE, scale_factor=1.0), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        d = load("reed")
        g = axes([0, 3], [-0.6, 0.6], x_length=6.4, y_length=2.6, xlabel=r"time, \ in periods of the note", ylabel=r"pressure in the mouthpiece", xticks=[0, 1, 2, 3], yticks=[0], font_size=20)
        g.move_to(LEFT * 3.2 + UP * 0.9)
        cu = curve_from(g, d["t"], d["p"], CLAR)
        hb = harmonic_bars(d["harmonics_db"], color=CLAR, width=5.2, height=2.3, floor_db=-40.0, font_size=18).move_to(RIGHT * 3.6 + UP * 0.8)
        hl = label(r"its harmonics (dB)", font_size=22, color=GREY_B).next_to(hb, UP, buff=0.15)
        notes = VGroup(label(r"a puff of pressure runs down the pipe, \ comes back upside down from the open end,", font_size=26, color=GREY_A),
                       label(r"and arrives as suction: \ the reed opens, \ the flow changes, \ and the suction is sent down in its turn", font_size=26, color=GREY_A),
                       label(rf"four trips of the pipe make one period: \ {d['hz']:.0f} Hz", font_size=30, color=TUNE)).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Put that valve on the end of the pipe, and follow one puff. A little extra pressure in the "
            "mouthpiece runs down the pipe. At the open end it is reflected upside down, as suction, and runs "
            "back. <bookmark mark='a'/> When the suction reaches the mouthpiece, the pressure difference "
            "across the reed changes, the flow through the gap responds, and what is sent back down the pipe "
            "is suction again. That returns as pressure. Down, back, down, back: four trips of the pipe for "
            f"one full cycle. <bookmark mark='b'/> Here is Monochord's reed on the sixty-centimetre pipe. The "
            "pressure in the mouthpiece flips between high and low: very nearly a square wave, at "
            f"{say(d['hz'])} hertz. <bookmark mark='c'/> And a square wave, Part 3 showed, is made of odd "
            "harmonics only. Inside the mouthpiece, the even ones are more than fifty decibels down. So the "
            "clarinet's hollow sound is not something added to it. It is the shape of a wave that spends "
            "half its time high and half its time low."
        ) as vo:
            tv = TubeView(width=9.0, bore=0.7, left="closed", right="open", color=CLAR).move_to(UP * 1.2)
            ends = VGroup(label(r"the reed", font_size=24, color=REED).next_to(tv, LEFT, buff=0.2), label(r"the open end", font_size=24, color=AIR).next_to(tv, RIGHT, buff=0.2))
            trip = ValueTracker(0.0)
            puff = always_redraw(lambda: Dot(tv.p(1 - abs(1 - (trip.get_value() % 2.0))), radius=0.16,
                                             color=BAD if int(trip.get_value() + 1) % 4 < 2 else AIR))
            sign = label(r"red: \ pressure. \ blue: \ suction", font_size=22, color=GREY_B).next_to(tv, DOWN, buff=0.3)
            self.play(FadeIn(tv), FadeIn(ends), FadeIn(puff), FadeIn(sign), FadeIn(notes[0]))
            self.play(trip.animate(rate_func=linear).set_value(2.0), run_time=max(vo.until("a") - 0.5, 1.0))
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]), trip.animate(rate_func=linear).set_value(8.0), run_time=max(vo.until("b") - 0.5, 1.0))
            puff.clear_updaters()
            self.play(FadeOut(tv), FadeOut(ends), FadeOut(puff), FadeOut(sign), run_time=0.4)
            self.play(FadeIn(g), Create(cu), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(hb), FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harder(self):
        d = load("reed")
        c = clip("reed.crescendo")
        q = listen_card(r"A player blows steadily harder for five seconds. \\ When does the sound begin? \ And what changes after that, \ besides the loudness?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        lo, hi = d["ramp"]
        g = axes([0, 5], [0.2, 0.9], x_length=8.0, y_length=2.8, xlabel=r"seconds", ylabel=r"blowing pressure", xticks=[0, 1, 2, 3, 4, 5], yticks=[0.33, 0.67], yfmt=lambda v: r"\tfrac13" if v < 0.5 else r"\tfrac23", font_size=20)
        g.move_to(DOWN * 1.0)
        line = Line(g.ax.c2p(0, lo), g.ax.c2p(5, hi), color=GREY_B, stroke_width=2)
        dot = Dot(g.ax.c2p(0, lo), radius=0.1, color=CLAR)
        with self.voiceover(
            "What does the player control? Mostly one thing: how hard to blow. So listen to Monochord's "
            "clarinet being blown steadily harder for five seconds, from almost nothing. When does the sound "
            "begin? And once it has begun, what changes, besides the loudness?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(line), FadeIn(dot))
        with self.listen(c) as snd:
            window(snd, r"a clarinet, \ blown harder and harder", detail=r"a model reed on a 60 cm pipe", corner=DL, tag_corner=DR)
            snd.drive(dot, lambda m, t: m.move_to(g.ax.c2p(min(t, 5.0), lo + (hi - lo) * min(t, 5.0) / 5.0)))
        mark = VGroup(DashedLine(g.ax.c2p(d["speaks_at"], 0.2), g.ax.c2p(d["speaks_at"], 0.9), color=CLAR, stroke_width=2),
                      label(r"it speaks", font_size=24, color=CLAR).next_to(g.ax.c2p(d["speaks_at"], 0.9), UP, buff=0.08))
        silent = label(r"breath, \ but no note", font_size=24, color=GREY_B).move_to(g.ax.c2p(0.8, 0.62))
        bright = label(r"louder, \ and brighter", font_size=24, color=TUNE).move_to(g.ax.c2p(3.6, 0.42))
        soft, loud = d["soft"], d["loud"]
        with self.voiceover(
            "For the first second and a half there is breath and no note. Then, quite suddenly, the clarinet "
            "speaks. There is a threshold, and below it no amount of patience will make a sound. "
            "<bookmark mark='a'/> And after it speaks, the note does not only get louder. It starts as "
            "something close to a pure tone and grows an edge. Just above the threshold the fifth harmonic "
            f"is {say(abs(soft['fifth_db']))} decibels below the first; at full breath it is "
            f"{say(abs(loud['fifth_db']))}. As with the piano's hammer, loud is bright. A clarinettist who "
            "wants a soft, dark sound plays just above the threshold, and a great deal of the art is living "
            "there without falling off."
        ) as vo:
            self.play(FadeOut(q), FadeIn(mark), FadeIn(silent))
            vo.wait_until("a")
            self.play(FadeIn(bright))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_a_third(self):
        d = load("reed")
        rows = d["rows"]
        g = axes([0.2, 1.0], [0, 1.0], x_length=5.2, y_length=3.4, xlabel=r"blowing pressure, \ as a fraction of the shutting pressure", ylabel=r"size of the note", xticks=[0.33, 0.67, 1.0],
                 yticks=[], xfmt=lambda v: {0.33: r"\tfrac13", 0.67: r"\tfrac23", 1.0: "1"}[round(v, 2)], font_size=20)
        g.move_to(LEFT * 3.9 + DOWN * 0.6)
        pts = VGroup(*[Dot(g.ax.c2p(r["gamma"], r["amp"]), radius=0.06, color=CLAR) for r in rows])
        third = DashedLine(g.ax.c2p(1 / 3, 0), g.ax.c2p(1 / 3, 1.0), color=GREY_B, stroke_width=1.5)
        th = label(rf"it speaks at {d['threshold']:.2f}", font_size=24, color=CLAR).next_to(g.ax.c2p(d["threshold"], 0.0), UR, buff=0.12)
        head = label(r"Why a third?", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        why = VGroup(label(r"below $\tfrac13$: \ the rising side of the reed's curve.", font_size=26, color=GOOD),
                     label(r"A returning pulse of pressure cuts the flow: \\ the valve fights the wave.", font_size=24, color=GREY_A),
                     label(r"above $\tfrac13$: \ the falling side.", font_size=26, color=BAD),
                     label(r"A returning pulse of pressure \emph{raises} the flow: \\ the valve feeds the wave.", font_size=24, color=GREY_A),
                     label(r"the little extra is what the pipe's walls \\ and its open end take away", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 0.3)
        with self.voiceover(
            "Where is the threshold? Here is every blowing pressure Monochord tried, and the size of the note "
            f"that resulted. Nothing, nothing, nothing; and then, at {say(d['threshold'], 2)} of the pressure "
            "that shuts the reed, a note. <bookmark mark='a'/> A third, and a little more. That is the top of "
            "the flow curve, and now you can see why. <bookmark mark='b'/> Below a third, the reed is on the "
            "rising side of its curve. When a pulse of pressure comes back up the pipe, the pressure "
            "difference across the reed drops, and so does the flow: the valve works against the wave, and "
            "any disturbance dies. <bookmark mark='c'/> Above a third, on the falling side, the same returning "
            "pulse makes the flow go up. The valve lets in air exactly when the pressure is already high. "
            "It feeds the wave. <bookmark mark='d'/> The little extra, between a third and where our pipe "
            "actually spoke, is what the walls of the pipe and its open end take away on each trip. The "
            "valve has to pay that back before anything is left over to grow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), run_time=3.0)
            self.play(FadeIn(th))
            vo.wait_until("a")
            self.play(Create(third))
            vo.wait_until("b")
            self.play(FadeIn(why[0]), FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[2]), FadeIn(why[3]))
            vo.wait_until("d")
            self.play(FadeIn(why[4]))
        self.wait(0.3)
        self.clear_scene()
