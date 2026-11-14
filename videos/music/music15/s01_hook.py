from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.probe()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def probe(self):
        d = load("hook")
        c = clip("hook.probe")
        kb = keys(41, 77, width=10.5, height=1.5).move_to(UP * 1.2)
        cols = VGroup()
        for name in ("C", r"F$\sharp$"):
            box = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2)
            cols.add(VGroup(box, label(name, font_size=54, color=GREY_A).move_to(box)))
        cols.arrange(RIGHT, buff=1.4).move_to(DOWN * 1.3)
        cap = label(r"four chords; \ then one tone. \ How well does the tone fit?", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here is an experiment that you can run on yourself. You will hear four chords, and then a "
            "single tone. Your only job is to say how well the tone fits with what came before: from "
            "one, not at all, to seven, perfectly. Then the same four chords, and a different tone."
        ):
            self.play(FadeIn(cap), FadeIn(kb), FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"four chords and a tone, \ twice", detail=r"Part 7's piano; \ then a tone with no octave", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["chords"] + d["chords"], d["times"]["fits"] + d["times"]["not"], end=c.duration)
            pulse(snd, cols[0], d["probe"]["fits"], d["probe"]["fits"] + 1.1, buff=0.1)
            pulse(snd, cols[1], d["probe"]["not"], d["probe"]["not"] + 1.1, buff=0.1)
        kb.clear()
        rate = VGroup(label(rf"listeners' average: \ {d['ratings']['C']:.1f} out of 7", font_size=26, color=TUNE).next_to(cols[0], DOWN, buff=0.25),
                      label(rf"{d['ratings']['F♯']:.1f} out of 7", font_size=26, color=EAR).next_to(cols[1], DOWN, buff=0.25))
        with self.voiceover(
            "You did not need to think. The first tone sat down as if a chair had been pulled out for "
            "it. The second was wrong: not ugly in itself, the same kind of sound, but in the wrong "
            f"place. <bookmark mark='a'/> When Carol Krumhansl and Edward Kessler ran this experiment "
            f"in 1982, their listeners gave the first tone {say(d['ratings']['C'], 1)} out of seven "
            f"and the second {say(d['ratings']['F♯'], 1)}, and people with no musical training at all "
            "give the same order."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rate), cols[0][1].animate.set_color(TUNE), cols[1][1].animate.set_color(EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        qs = VGroup(label(r"four chords set up an expectation for all twelve notes at once.", font_size=30, color=WHITE),
                    label(r"that expectation is what musicians call a key.", font_size=34, color=TUNE),
                    label(r"where is it? \ In the chords? \ In the scale? \ In you?", font_size=30, color=EAR)).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        with self.voiceover(
            "Think about what that means. Four chords, lasting three seconds, and your mind had already "
            "ranked all twelve notes: this one is home, these belong, those do not. <bookmark mark='a'/> "
            "That ranking is what musicians call a key. Part 14 kept running into it: tunes ended on "
            "the same degree ninety-six times in a hundred, and other notes leaned toward it. "
            "<bookmark mark='b'/> So where is a key? It is not in any one chord, and it is not in the "
            "scale, because seven keys share any scale's notes with a neighbour. This part will argue "
            "that it is in the listener, and that it got there by counting."
        ) as vo:
            self.play(FadeIn(qs[0]))
            vo.wait_until("a")
            self.play(FadeIn(qs[1]))
            vo.wait_until("b")
            self.play(FadeIn(qs[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"a key is a home note,", font_size=32, color=GREY_A), label(r"and a ranking of every other note around it.", font_size=32, color=TUNE)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"the probe-tone experiment: \ how well each of twelve notes fits",
            r"where the ranking comes from: \ the music a listener has heard",
            r"the three jobs of chords in a key, \ and four ways to end a phrase",
            r"finding the key by machine: \ how well, \ how fast, \ and from which notes",
            r"a map of the twenty-four keys, \ and how music travels on it",
            r"minor keys, \ and tunes that are in no key at all",
        ], title=r"Part 15: \ Key", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "This is the last part of Act Two, and it gathers the others up. Scales, chords and melody "
            "all turn out to be about one thing: home. <bookmark mark='a'/> We begin with the experiment "
            "you just did, for all twelve notes. <bookmark mark='b'/> We ask where the ranking comes "
            "from. <bookmark mark='c'/> We give the chords of a key their three jobs, and learn four "
            "ways to end a phrase. <bookmark mark='d'/> We build a machine that finds the key of a tune, "
            "and ask how well it does, how fast, and from which notes. <bookmark mark='e'/> We draw a map "
            "of the twenty-four keys, and travel on it. <bookmark mark='f'/> And we end with minor keys, "
            "and with tunes that are in no key at all."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
