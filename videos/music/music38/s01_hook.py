from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


def swing_grid(times, bpm, beats, width=11.0, color=TUNE, y=0.0):
    """Beats as tall ticks and each note as a dot at its true time: the long-short split made visible."""
    beat = 60.0 / bpm
    total = beats * beat
    x0 = -width / 2
    g = VGroup()
    g.ticks = VGroup()
    for b in range(beats + 1):
        x = x0 + width * b * beat / total
        g.ticks.add(Line([x, y - 0.45, 0], [x, y + 0.45, 0], color=GREY_B if b % 4 else WHITE, stroke_width=2 if b % 4 else 3))
    g.add(g.ticks)
    g.dots = VGroup(*[Dot([x0 + width * t / total, y, 0], radius=0.09, color=color) for t in times if t < total])
    g.add(g.dots)
    return g


def appear(snd, dots, times):
    """Each dot appears when its note sounds, and stays."""
    for dot, t in zip(dots, times):
        snd.show(dot)
        snd.drive(dot, lambda m, now, t=t: m.set_opacity(1.0 if now >= t else 0.0))


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.ask()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        card = listen_card(r"A line of ours over bass and cymbal: \ each beat is split into a long note and a short one. \ "
                           r"How much longer is the long note: \ about the same, \ twice, \ or three times?", width=10.4)
        with self.voiceover(
            "What is swing? Before anyone answers, measure it by ear. A line of our own, played over a walking bass and a ride cymbal. Each beat is split "
            "into two notes, a long one and a short one. How much longer is the long note than the short: about the same, "
            "twice as long, or three times?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        beats = 16
        g = swing_grid(d["times"]["swung"], d["bpm"], beats).move_to(UP * 0.4)
        cap = label(r"white ticks: \ bar lines; \ grey: \ beats; \ dots: \ the line's notes", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.1)
        self.play(FadeOut(card), FadeIn(g.ticks), FadeIn(cap))
        with self.listen(clip("hook.swung")) as snd:
            window(snd, r"a line, \ swung", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            appear(snd, g.dots, d["times"]["swung"])
            pulse(snd, g.ticks, 0.0, 16 * 60 / d["bpm"], buff=0.1)
        g.dots.set_opacity(1.0)
        self.add(g.dots)
        beat = 60.0 / d["bpm"]
        r = d["ratio"]
        x0, x1 = -3.0, 3.0
        xs = x0 + (x1 - x0) * r / (1 + r)
        long_ = Line([x0, -1.0, 0], [xs, -1.0, 0], color=TUNE, stroke_width=14)
        short = Line([xs, -1.0, 0], [x1, -1.0, 0], color=EAR, stroke_width=14)
        lab = VGroup(label(r"one beat, \ enlarged: \ long", font_size=20, color=TUNE).next_to(long_, DOWN, buff=0.15), label(r"short", font_size=20, color=EAR).next_to(short, DOWN, buff=0.15))
        ans = label(rf"about three times: \ at {d['bpm']} beats a minute the long note takes three quarters of the beat", font_size=21, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"About three times. At {say(d['bpm'])} beats a minute, the long note takes three quarters of the beat and the "
            f"short one a quarter, about {say(round(d['short_ms']))} milliseconds. Not the even split of written eighth notes, "
            "and not the two-to-one of a triplet either. Here is the same line played straight, for comparison."
        ):
            self.play(FadeOut(cap), Create(long_), Create(short), FadeIn(lab), FadeIn(ans))
        g2 = swing_grid(d["times"]["straight"], d["bpm"], beats, color=BLUE).move_to(DOWN * 2.55)
        self.play(FadeOut(ans), FadeIn(g2.ticks))
        with self.listen(clip("hook.straight")) as snd:
            window(snd, r"the same line, \ straight", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            appear(snd, g2.dots, d["times"]["straight"])
            pulse(snd, g2.ticks, 0.0, 16 * 60 / d["bpm"], buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ask(self):
        items = [
            (r"`What is swing?' \ The old answer: \ if you have to ask, \ you'll never know", WHITE),
            (r"but swing can be measured: \ the long-short ratio, \ and where notes fall against the band", WHITE),
            (r"the ratio is near three to one at slow tempos and falls to even at fast ones", WHITE),
            (r"soloists tend to place their downbeats a little late and their off-beats on time", TUNE),
            (r"this part builds the blues, \ ragtime and the swing band, \ and a model that swings", GREY_A),
        ]
        rows_scene(self, r"if you have to ask", items,
                   "What is swing? The proverbial answer, attributed to more than one jazz musician, is that if you have to "
                   "ask, you will never know. <bookmark mark='b'/> But swing can be measured: the ratio of long to short, and "
                   "where the notes fall against the band. <bookmark mark='c'/> The ratio is near three to one at slow tempos "
                   "and falls to even at fast ones. <bookmark mark='d'/> And soloists tend to place their downbeats a little late "
                   "and their off-beats on time. <bookmark mark='e'/> This part builds the blues, ragtime and the swing band, "
                   "and a model that swings.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the twelve-bar blues, \ blue notes, \ and call and response",
            r"ragtime: \ Joplin's \textit{Maple Leaf Rag} from the score, \ its syncopations counted",
            r"swing measured: \ the long-short ratio against tempo, \ and late downbeats",
            r"the swing band: \ riffs between sections",
            r"walking bass and guide tones, \ computed",
            r"ii--V--I, \ turnarounds and the tritone substitution",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The twelve-bar blues, its blue notes, and call and response. <bookmark mark='b'/> Ragtime, "
            "with Scott Joplin's Maple Leaf Rag played from the score and its syncopations counted. <bookmark mark='c'/> "
            "Swing measured: the long-short ratio against tempo, and late downbeats. <bookmark mark='d'/> The swing band, "
            "where sections trade riffs. <bookmark mark='e'/> Walking bass lines and guide tones, computed. "
            "<bookmark mark='f'/> And the harmony of jazz: two-five-one, turnarounds, and the tritone substitution. "
            "Joplin's rag is played from its encoding; every other line, riff and verse is ours."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
