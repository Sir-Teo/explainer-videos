from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Organum(SoundScene):
    def construct(self):
        chapter(self, 3, r"Parallel organum", r"What was the first harmony?", extra=((900, r"\textit{Musica enchiriadis}"),))
        self.handbook()
        self.quiz()
        self.rule()

    # ------------------------------------------------------------------
    def handbook(self):
        items = [
            (r"late ninth century: \ \textit{Musica enchiriadis}, \ a handbook, \ and its companion dialogue", WHITE),
            (r"the chant, \ the `principal voice', \ and below it an `organal voice' a fifth or a fourth down", WHITE),
            (r"either may be doubled at the octave: \ four voices, \ one melody", WHITE),
            (r"the first written description of singing in harmony in the West", TUNE),
            (r"Part 16 met it as the first stage of counterpoint; \ here is where the trouble began", GREY_A),
        ]
        rows_scene(self, r"the oldest handbook", items,
                   "The first written account of singing in harmony in the West comes from the late ninth century, in an "
                   "anonymous handbook called Musica enchiriadis and a dialogue that goes with it. <bookmark mark='b'/> "
                   "The chant, the principal voice, is sung as usual, and a second singer, the organal voice, sings the "
                   "same melody a fifth or a fourth lower. <bookmark mark='c'/> Either line may be doubled at the octave, "
                   "so that four singers sing one melody at four pitches. <bookmark mark='d'/> It is the first harmony we "
                   "can describe exactly. <bookmark mark='e'/> Part 16 met it as the first stage of counterpoint. Here is "
                   "the trouble it ran into at once.")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("organum")
        c = clip("organum.quiz")
        card = listen_card(r"Two organa at the fifth below the same psalm verse, \ which recites on F. \ In one, \ the lower voice sings B$\flat$ under F: \ "
                           r"a true fifth. \ In the other, \ B natural: \ a tritone. \ Which one has the tritone, \ A or B?", width=10.8)
        with self.voiceover(
            "Listen. Two organa at the fifth below the same psalm verse, which recites on F. In one, the lower voice sings "
            "B flat under every F, a true fifth. In the other it sings B natural, the note a strict parallel fifth gives "
            "in the white-note scale, and the interval is a tritone. Which one has the tritone, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ch = [[p, k, 1.0] for k, p in enumerate(d["chant"])]
        fa = [[p, k, 1.0] for k, p in enumerate(d["flat"])]
        fb = [[p, k, 1.0] for k, p in enumerate(d["fifths"])]
        gA = voices_roll([ch, fa], width=5.4, height=2.2, colors=[TUNE, BLUE], lo=53, hi=67).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll([ch, fb], width=5.4, height=2.2, colors=[TUNE, BLUE], lo=53, hi=67).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.35)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        u = d["unit"]
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"two synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, [ch, fa], d["starts"]["A"], u, colors=[TUNE, BLUE])
            flash_voices(snd, gB, [ch, fb], d["starts"]["B"], u, colors=[TUNE, BLUE])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        bad = VGroup(*[SurroundingRectangle(gB.parts[1].notes[k], color=RED, buff=0.04, stroke_width=2) for k, (p, q) in enumerate(zip(d["chant"], d["fifths"])) if (p - q) % 12 == 6])
        ans = VGroup(label(r"F over B$\flat$: \ a fifth", font_size=24, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(rf"F over B: \ a tritone, \ {d['tritones']['parallel']} times", font_size=24, color=RED).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            f"B has the tritone, {say(d['tritones']['parallel'])} times, every time the chant sits on its reciting tone. "
            "The tritone, mi against fa in the singers' terms, was the interval later theorists nicknamed the devil in music, and "
            "strict parallel motion walks straight into it whenever the chant touches F with a fifth below or B with a "
            "fourth below. Singers either flattened the B, as in A, or changed the rule."
        ):
            self.play(Create(bad), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        d = load("organum")
        c = clip("organum.enchiriadis")
        ch = [[p, k, 1.0] for k, p in enumerate(d["chant"])]
        en = [[p, k, 1.0] for k, p in enumerate(d["enchiriadis"])]
        g = voices_roll([ch, en], width=10.0, height=2.4, colors=[TUNE, BLUE], lo=57, hi=67).move_to(UP * 0.5)
        floor = DashedLine(g.frame.get_left() + UP * (g.frame.height * (60 - 57) / 10 - g.frame.height / 2), g.frame.get_right() + UP * (g.frame.height * (60 - 57) / 10 - g.frame.height / 2), color=GREY_B, stroke_width=1.5)
        fl = label(r"C: \ the organal voice may not go lower", font_size=18, color=GREY_B).next_to(floor, LEFT, buff=0.1).shift(DOWN * 0.25)
        fl.scale_to_fit_width(min(fl.width, 3.0))
        cap = VGroup(label(r"the organal voice holds on C while the chant moves: \ oblique motion", font_size=22, color=WHITE),
                     label(r"and the two meet in a unison at the end: \ the \textit{occursus}", font_size=22, color=TUNE),
                     label(r"for the first time, \ the two voices do different things", font_size=22, color=EAR)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The handbook's answer was a boundary. At the fourth, the organal voice follows the chant down but may not "
            "go below a fixed note, here C. When the chant is too low for a fourth below to stay above the boundary, the "
            "organal voice simply holds the boundary note, and at the end of the phrase the two voices come together "
            "on one note, which the theorists called the occursus, the running together. Listen to the lower voice "
            "sitting still."
        ):
            self.play(FadeIn(g), Create(floor), FadeIn(fl))
        with self.listen(c) as snd:
            window(snd, r"organum at the fourth, \ by the rule", detail=r"two synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, [ch, en], 0.0, d["unit"], colors=[TUNE, BLUE])
            cursor(snd, g, 0.0, d["unit"])
        with self.voiceover(
            "That sitting still is the important thing. <bookmark mark='a'/> While the chant moves and the organal voice "
            "holds, the two lines move differently, oblique motion, <bookmark mark='b'/> and they arrive together at the "
            "end, like a cadence. <bookmark mark='c'/> A rule invented to avoid one bad interval had, for the first time, "
            "made two voices into two different lines."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
        self.wait(0.4)
        self.clear_scene()
