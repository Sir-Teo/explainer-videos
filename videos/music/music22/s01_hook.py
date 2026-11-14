from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.levels()
        self.claim()
        self.plan()

    # ------------------------------------------------------------------
    def levels(self):
        d = load("hook")
        c = clip("hook.levels")
        rolls = VGroup()
        titles = [r"the Tune", r"a note every 2 beats", r"every 4", r"every 8", r"every 16"]
        for k, lv in enumerate(d["shown"]):
            g = mroll(d["levels"][lv], width=9.0, height=0.62, lo=70, hi=84, total=48.0, color=TUNE if k == 0 else BLUE)
            t = label(titles[k], font_size=18, color=GREY_A).next_to(g, LEFT, buff=0.3)
            rolls.add(VGroup(t, g))
        rolls.arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to(DOWN * 0.2 + RIGHT * 0.6)
        head = label(r"the Tune, \ and the Tune reduced", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the Tune, and below it the Tune reduced: at each level, every span keeps only its most important "
            "note, the one most stable in its harmony and on the strongest beat. Listen to the levels one after "
            "another, from the surface down to the skeleton."
        ):
            self.play(FadeIn(head), FadeIn(rolls))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ then four levels of reduction", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, lv in enumerate(d["shown"]):
                st = d["starts"][f"L{lv}"]
                notes = d["levels"][lv]
                flash(snd, rolls[k][1].notes, [st + n[1] * d["beat"] for n in notes], hot=WHITE, base=TUNE if k == 0 else BLUE)
                end = d["starts"][f"L{d['shown'][k + 1]}"] - 0.5 if k + 1 < len(d["shown"]) else c.duration
                pulse(snd, rolls[k][0], st, end, buff=0.08)
        with self.voiceover(
            "At two beats a note, the Tune becomes C, G, A, G, F, E, D, C: the climb to the fifth and the walk down. At "
            "sixteen beats, only C, G, C remain: home, the dominant, home. Every melody, a theory says, is the "
            "elaboration of something much simpler."
        ):
            self.wait(0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def claim(self):
        card = history_card(1935, r"Vienna: \ Heinrich Schenker, \ \textit{Der freie Satz}", r"every tonal masterpiece elaborates one descent to the tonic, \ over I--V--I", width=11.0, font_size=26).to_edge(UP, buff=0.4)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"the deepest level: \ a line falling by step to the tonic, \ 3--2--1 or 5--4--3--2--1", WHITE),
            (r"under it, \ the bass: \ tonic, \ dominant, \ tonic", WHITE),
            (r"everything else: \ elaboration, \ level upon level", WHITE),
            (r"the Tune does it on its surface: \ it climbs to G and walks down to C", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.6)
        with self.voiceover(
            "The theory belongs to Heinrich Schenker, a Viennese music theorist whose last book, Der freie Satz, "
            "appeared in 1935, the year of his death. <bookmark mark='a'/> His claim: at the deepest level, every "
            "tonal masterpiece is one line falling by step to the tonic, <bookmark mark='b'/> over a bass that goes "
            "from the tonic to the dominant and back. <bookmark mark='c'/> Everything else, every note you hear, is "
            "elaboration of that, level upon level. <bookmark mark='d'/> The Tune does it in plain sight: it climbs to "
            "G, the fifth, and walks down, F, E, D, C."
        ) as vo:
            self.play(FadeIn(card), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 22: \ Analysis", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=27, color=c_) for t, c_ in (
            (r"reduction, \ prolongation, \ and Schenker's \textit{Ursatz}", WHITE),
            (r"Lerdahl and Jackendoff: \ grouping, \ metre, \ reductions as preference rules", WHITE),
            (r"harmony as a grammar: \ trees, \ parsing, \ ambiguity", EAR),
            (r"a grammar trained on Bach, \ scored against chord pairs", WHITE),
            (r"a grammar that grows melodies; \ other ways to analyse", WHITE),
            (r"the argument over the theory and its author; \ is harmony recursive?", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part takes the claim seriously as a theory, and tests it. <bookmark mark='a'/> First what reduction "
            "means, and Schenker's fundamental structure. <bookmark mark='b'/> Then a version precise enough to compute, "
            "Lerdahl and Jackendoff's. <bookmark mark='c'/> Then harmony written as a grammar, with trees and parsing, "
            "<bookmark mark='d'/> trained on Bach's chorales and scored against the chord-pair model of Part 18. "
            "<bookmark mark='e'/> Then a grammar that grows melodies, and other ways to analyse. "
            "<bookmark mark='f'/> And then the arguments: about Schenker himself, and about whether harmony is "
            "recursive at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            for mark, s in zip("bcdef", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
