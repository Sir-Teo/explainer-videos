from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.each()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.stereo")
        card = listen_card(r"Put on headphones. \ Each ear gets a stream of notes. \ "
                           r"Listen to the right ear: \ does its melody move by step, \ or jump around?", width=10.4)
        with self.voiceover(
            "Put on headphones for this one. Each ear will get its own stream of notes, both at once. Listen to what you "
            "hear on the right: does that melody move smoothly by step, or does it jump around?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ears = VGroup(label(r"left ear", font_size=22, color=BLUE), label(r"right ear", font_size=22, color=EAR)).arrange(RIGHT, buff=5.0).to_edge(UP, buff=0.6)
        box = VGroup(RoundedRectangle(width=5.0, height=2.4, corner_radius=0.2, stroke_color=GREY_B), label(r"listen", font_size=26, color=GREY_A)).arrange(ORIGIN).move_to(DOWN * 0.2)
        self.play(FadeOut(card), FadeIn(ears), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"each ear its own notes", kind="synthesized", detail=r"sine tones, \ stereo", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.1)
        self.play(FadeOut(box))
        L = keyroll(d["left"], width=5.0, height=1.6, lo=58, hi=74, colors=[BLUE] * 8).move_to(LEFT * 3.3 + UP * 0.9)
        R = keyroll(d["right"], width=5.0, height=1.6, lo=58, hi=74, colors=[EAR] * 8).move_to(RIGHT * 3.3 + UP * 0.9)
        got = label(r"what each ear was given", font_size=18, color=GREY_A).next_to(VGroup(L, R), UP, buff=0.15)
        H = keyroll(d["heard_high"], width=5.0, height=1.6, lo=58, hi=74, colors=[TUNE] * 8).move_to(RIGHT * 3.3 + DOWN * 1.6)
        Lo = keyroll(d["heard_low"], width=5.0, height=1.6, lo=58, hi=74, colors=[TUNE] * 8).move_to(LEFT * 3.3 + DOWN * 1.6)
        heard = label(r"what most right-handed listeners hear", font_size=18, color=TUNE).next_to(VGroup(H, Lo), UP, buff=0.15)
        with self.voiceover(
            "Most people hear a smooth melody on the right, going down and back up, and another on the left, going up and "
            "back down. <bookmark mark='a'/> But look at what each ear was actually given: notes jumping by "
            f"{say(d['leap_right'], 1)} semitones on average, an ascending and a descending scale chopped up and dealt "
            "alternately to the two ears. <bookmark mark='b'/> What you heard was regrouped by pitch: the higher notes, "
            f"wherever they came from, made one smooth line, moving {say(d['leap_heard'], 1)} semitones a step, and the "
            "lower notes another. Diana Deutsch found this scale illusion in 1975: the brain prefers a melody that "
            "moves by small steps to the truth about which ear heard what."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(L), FadeIn(R), FadeIn(got))
            vo.wait_until("b")
            self.play(FadeIn(H), FadeIn(Lo), FadeIn(heard))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"the ear receives one pressure wave per side: \ every voice and instrument summed together", WHITE),
            (r"the mind returns a scene: \ separate voices, \ each with its own pitch, \ timbre and place", WHITE),
            (r"Albert Bregman called the process `auditory scene analysis' \ (1990)", WHITE),
            (r"its rules can be measured, \ modelled and turned into music", TUNE),
            (r"and Part 16's rules of counterpoint fall out of them", GREY_A),
        ]
        rows_scene(self, r"one wave, \ a whole scene", items,
                   "The ear receives one pressure wave on each side, every voice and instrument summed together. "
                   "<bookmark mark='b'/> The mind returns a scene: separate voices, each with its own pitch, timbre and place. "
                   "<bookmark mark='c'/> Albert Bregman called the process auditory scene analysis, in his book of 1990. "
                   "<bookmark mark='d'/> Its rules can be measured, modelled and turned into music, <bookmark mark='e'/> and "
                   "Part 16's rules of counterpoint fall out of them.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"streaming: \ when a sequence splits into two",
            r"a model of the streaming boundary, \ fitted to the classic data",
            r"interleaved melodies, \ and what releases them",
            r"simultaneous grouping: \ harmonicity, \ onsets, \ continuity",
            r"counterpoint as scene analysis; \ a timbre space of our instruments",
            r"pitch illusions, \ absolute pitch and pitch memory",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Streaming: when a sequence of notes splits into two. <bookmark mark='b'/> A model of the "
            "streaming boundary, fitted to the classic data. <bookmark mark='c'/> Interleaved melodies, and what releases "
            "them. <bookmark mark='d'/> Simultaneous grouping: harmonicity, onsets and continuity. <bookmark mark='e'/> "
            "Counterpoint as scene analysis, and a timbre space of our own instruments. <bookmark mark='f'/> And the pitch "
            "illusions, absolute pitch and pitch memory."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def each(self):
        d = load("each")
        c = clip("each.two")
        L = keyroll(d["left"], width=5.0, height=1.8, lo=58, hi=74, colors=[BLUE] * 8).move_to(LEFT * 3.2 + UP * 0.4)
        R = keyroll(d["right"], width=5.0, height=1.8, lo=58, hi=74, colors=[EAR] * 8).move_to(RIGHT * 3.2 + UP * 0.4)
        labs = VGroup(label(r"left ear alone", font_size=20, color=BLUE).next_to(L, UP, buff=0.2), label(r"right ear alone", font_size=20, color=EAR).next_to(R, UP, buff=0.2))
        with self.voiceover("Check it. Here is the left ear's part alone, and then the right ear's."):
            self.play(FadeIn(L), FadeIn(R), FadeIn(labs))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one ear at a time", kind="synthesized", detail=r"sine tones, \ stereo", corner=DL, tag_corner=DR)
            flash(snd, L.notes, [st["left"] + i * d["ioi"] for i in range(8)], hot=WHITE, base=BLUE)
            flash(snd, R.notes, [st["right"] + i * d["ioi"] for i in range(8)], hot=WHITE, base=EAR)
        with self.voiceover(
            "Alone, each ear's part is a jagged, leaping line. Together, the brain trades them: it would rather hear two "
            "smooth melodies than believe each ear."
        ):
            self.play(Indicate(L), Indicate(R))
        self.wait(0.3)
        self.clear_scene()
