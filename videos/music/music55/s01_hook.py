from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.sequel()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"A voice in a lecture room, \ twice. \ Once in the room as it was built; \ once after the room was "
                           r"changed so that people could understand it. \ Which was the room as it was built?", width=10.0)
        with self.voiceover(
            'This part begins at Harvard, in 1895. Your ears go first. A voice in a lecture room, twice. Once in a simulated untreated room; once after absorption was increased in the model so that people could understand what was said in it. Which was the room as it was built?'
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one voice, \ one room, \ twice", kind="physical model", detail=r"Part 8's voice, \ a simulated room", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        T0, T1 = d["T"]
        ax = frame_axes(width=9.0, height=3.4, xlo=0, xhi=6.0, ylo=-60, yhi=0, center=DOWN * 0.3)
        a = Line(ax.to(0, 0), ax.to(T0, -60), color=EAR, stroke_width=4)
        b = Line(ax.to(0, 0), ax.to(T1, -60), color=TUNE, stroke_width=4)
        xt = VGroup(*[label(f"{v} s", font_size=15, color=GREY_A).next_to(ax.to(v, -60), DOWN, buff=0.12) for v in range(0, 7)])
        yt = VGroup(*[label(f"{v} dB", font_size=15, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.12) for v in (0, -20, -40, -60)])
        la = label(rf"as built: \ {T0:.1f} s", font_size=19, color=EAR).next_to(ax.to(T0, -60), UP, buff=0.25)
        lb = label(rf"changed: \ {T1:.1f} s", font_size=19, color=TUNE).next_to(ax.to(T1, -60), UP + RIGHT, buff=0.15)
        note = label(r"each word was still sounding when the next five arrived", font_size=19, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the first was the room as built", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The first. <bookmark mark='a'/> Clap your hands in a room and the sound does not stop; it dies away, losing a "
            f"fixed number of decibels every second. In the room as built, a sound took {say(T0, 1)} seconds to die by sixty "
            "decibels, about a millionth of its energy. <bookmark mark='b'/> Each word was still sounding when the next five "
            f"arrived. <bookmark mark='c'/> After the change, it took {say(T1, 1)} seconds, and the words came apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(VGroup(a, b), 0.3)))
            vo.wait_until("a")
            self.play(Create(a), FadeIn(la), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
            vo.wait_until("c")
            self.play(Create(b), FadeIn(lb), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1895: \ Harvard opens the lecture room of the new Fogg Art Museum; \ nobody can understand a word in it", WHITE),
            (r"the president asks a 27-year-old assistant professor of physics, \ Wallace Sabine, \ to fix it", WHITE),
            (r"for three years of nights he times how long an organ pipe's note lasts, \ by ear and a stopwatch", WHITE),
            (r"he borrows the seat cushions of Sanders Theatre and lays them out a few at a time", WHITE),
            (r"the time falls in a law: \ the room's volume over its absorption", TUNE),
            (r"1900: \ Boston's Symphony Hall, \ the first hall designed by a formula, \ still among the best in the world", GREY_A),
        ]
        rows_scene(self, r"a room nobody could understand", items,
                   "The room was real. <bookmark mark='b'/> In 1895 Harvard opened the lecture room of its new Fogg Art Museum, with severe reverberation that impaired speech intelligibility. <bookmark mark='c'/> The university's president asked a twenty-seven-year-old assistant professor of physics, Wallace Sabine, to fix it. <bookmark mark='d'/> For three years, at night when the city was quiet, Sabine timed how long an organ pipe's note went on sounding after it stopped, by ear and with a stopwatch. <bookmark mark='e'/> He borrowed the seat cushions of Sanders Theatre across the yard, and carried them in a few at a time. <bookmark mark='f'/> The times fell into a law: the room's volume over its absorption. <bookmark mark='g'/> In 1900 Boston's Symphony Hall opened, an early influential hall designed with quantitative acoustic advice, and it is still among the best in the world.", marks="bcdefg")

    # ------------------------------------------------------------------
    def sequel(self):
        items = [
            (r"1962: \ Philharmonic Hall opens at Lincoln Center, \ designed with every tool of acoustics then known", WHITE),
            (r"the reverberation time was close to its target; \ the sound was thin, \ the bass weak, \ the players could not hear each other", WHITE),
            (r"years of adjustments; \ in 1976 the inside was torn out and rebuilt, \ and again, \ reopening in 2022", WHITE),
            (r"one number was not enough: \ when reflections arrive, \ and from where, \ matters as much as how long they last", TUNE),
            (r"then the space itself became something to build: \ stereo, \ surround, \ sound for headphones", GREY_A),
        ]
        rows_scene(self, r"sixty years later", items,
                   "Sixty years later, the science failed in public. <bookmark mark='b'/> In 1962 Philharmonic Hall opened at New "
                   "York's Lincoln Center, designed with every tool acoustics then had. <bookmark mark='c'/> Its reverberation time "
                   "was close to the target, and yet the sound was thin, the bass weak, and the players could not hear each other. "
                   "<bookmark mark='d'/> There were years of adjustments; in 1976 the inside was torn out and rebuilt, and it has "
                   "been rebuilt again since, most recently reopening in 2022. <bookmark mark='e'/> One number was not enough: when "
                   "reflections arrive, and from which direction, matters as much as how long they last. <bookmark mark='f'/> And "
                   "then space itself became something we build: stereo, surround, sound for headphones.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"Sabine's law, \ derived from a diffuse field",
            r"a room's modes, \ counted, \ and where they stop mattering",
            r"absorption and diffusion, \ and the number theory in a diffuser",
            r"early reflections and the shape of a hall",
            r"how two ears hear direction",
            r"stereo, \ Ambisonics, \ binaural rendering and object audio",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Sabine's law, derived. <bookmark mark='b'/> A room's modes, counted, and the frequency above "
            "which they stop mattering. <bookmark mark='c'/> Absorption and diffusion, and the number theory hidden in a "
            "diffuser. <bookmark mark='d'/> Early reflections, and the shape of a hall. <bookmark mark='e'/> How two ears "
            "hear direction. <bookmark mark='f'/> And the ways we build space: stereo, Ambisonics, binaural rendering and "
            "object audio. Several of this part's sounds are rendered for headphones; put them on."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
