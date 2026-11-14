from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Steps(SoundScene):
    def construct(self):
        chapter(self, 2, r"Small steps", r"How does a tune move?")
        self.histogram()
        self.streams()
        self.quiz()

    # ------------------------------------------------------------------
    def histogram(self):
        d = load("steps")
        s = d["shares"]
        ks = list(range(-12, 13))
        vals = [d["histogram"][str(k)] for k in ks]
        hot = [k + 12 for k in (-2, -1, 1, 2)]
        ch = columns(vals, [str(k) if k % 2 == 0 else "" for k in ks], width=11.0, height=2.9, color=WEAK, hot=hot, hot_color=TUNE, font_size=18).move_to(UP * 0.2 + DOWN * 1.0)
        ch.bars[12].set_fill(BLUE)
        xl = label(r"the move from one note to the next, \ in semitones \quad ($-$ is down)", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(rf"every move in the {load('hook')['tunes']} tunes: \ {int(s['moves']):,}".replace(",", "{,}"), font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        tags = VGroup(label(rf"steps: \ {100 * s['step']:.0f}\%", font_size=30, color=TUNE), label(rf"repeats: \ {100 * s['repeat']:.0f}\%", font_size=30, color=BLUE),
                      label(rf"leaps: \ {100 * s['leap']:.0f}\%", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Take every move from one note to the next in the fifty-four tunes: "
            f"{say(s['moves'])} moves. <bookmark mark='a'/> Half of them are steps: one or two "
            "semitones. A quarter are repeats of the same note. A quarter are leaps, and nearly all of "
            f"those are small: {say(100 * s['within_fifth'])} moves in a hundred are a fifth or less. "
            f"The average move is {say(s['mean_size'], 1)} semitones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch), FadeIn(xl), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.9), run_time=5.0)
        asym = VGroup(label(rf"a whole tone: \ {d['down']['whole_tone']} down, \ {d['up']['whole_tone']} up", font_size=28, color=WHITE),
                      label(rf"a fourth: \ {d['up']['fourth']} up, \ {d['down']['fourth']} down", font_size=28, color=WHITE)).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "And there are two asymmetries. Steps go down more often than up: the commonest move of all "
            f"is a whole tone down, {say(d['down']['whole_tone'])} of them against "
            f"{say(d['up']['whole_tone'])} up. <bookmark mark='a'/> Leaps of a fourth go the other way: "
            f"{say(d['up']['fourth'])} up against {say(d['down']['fourth'])} down. Melodies climb by "
            "leaping, and come down by walking. The same pattern has been counted in collections of "
            "thousands of songs, from Europe, China, southern Africa and native America."
        ) as vo:
            self.play(FadeOut(tags), FadeIn(asym[0]), Indicate(ch.bars[10], color=TUNE), Indicate(ch.bars[14], color=TUNE))
            vo.wait_until("a")
            self.play(FadeIn(asym[1]), Indicate(ch.bars[17], color=EAR), Indicate(ch.bars[7], color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def streams(self):
        c = clip("steps.streams")
        ev = c.events

        def gallop(gap, color):
            g = VGroup()
            for k in range(6):
                for j, s in enumerate((0, gap, 0)):
                    g.add(Dot([k * 0.95 + j * 0.24, 0.16 * s, 0], radius=0.07, color=color))
            return g

        near, far = gallop(2, TUNE).move_to(LEFT * 3.4 + UP * 0.7), gallop(9, EAR).move_to(RIGHT * 3.4 + UP * 0.7)
        lf = label(r"nine semitones away", font_size=26, color=GREY_A).next_to(far, DOWN, buff=0.4)
        ln = label(r"the middle note a tone away", font_size=26, color=GREY_A).next_to(near, DOWN, buff=0.4).align_to(lf, DOWN)
        with self.voiceover(
            "Why steps? One reason is the voice: a small change of pitch is a small change in the "
            "tension of the vocal folds. The other reason is the ear. Listen to a three-note gallop, "
            "low, high, low, played fast. First with the middle note a tone away; then with it nine "
            "semitones away."
        ):
            self.play(FadeIn(near), FadeIn(ln), FadeIn(far), FadeIn(lf))
        with self.listen(c) as snd:
            window(snd, r"a gallop, \ twice", kind="synthesized", detail=r"organ tones, \ nine notes a second", corner=DL, tag_corner=DR)
            pulse(snd, near, ev["near"], ev["far"] - 0.4, buff=0.2)
            pulse(snd, far, ev["far"], c.duration, buff=0.2)
        res = VGroup(label(r"one line, \ galloping", font_size=28, color=TUNE).next_to(ln, DOWN, buff=0.3), label(r"two lines, \ and no gallop", font_size=28, color=EAR).next_to(lf, DOWN, buff=0.3))
        with self.voiceover(
            "The first is one line that gallops. The second splits into two lines, a high one and a "
            "low one, and the gallop is gone. <bookmark mark='a'/> Albert Bregman named this auditory "
            "streaming: at speed, the ear groups sounds by their nearness in pitch. A melody that leaps "
            "too far, too fast, stops being one melody. Bach used the effect on purpose, to make one "
            "violin sound like two."
        ) as vo:
            self.play(FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("steps")
        c = clip("steps.two")
        ev = c.events
        card = listen_card(r"Two melodies made by chance, \ on the white keys. \ Which sounds more like a tune: \ A or B?", width=9.0)
        with self.voiceover("An ear question. Two melodies made by chance, on the white keys. Which one sounds more like a tune: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        rA = roll(d["urn"], width=5.6, height=2.6, lo=-1, hi=13, lines=(0, 12), color=CHANCE_C).move_to(LEFT * 3.3 + UP * 0.6)
        rB = roll(d["walk"], width=5.6, height=2.6, lo=-1, hi=13, lines=(0, 12), color=REAL_C).move_to(RIGHT * 3.3 + UP * 0.6)
        la, lb = label(r"A", font_size=40, color=GREY_A).next_to(rA, UP, buff=0.2), label(r"B", font_size=40, color=GREY_A).next_to(rB, UP, buff=0.2)
        self.play(FadeOut(card), FadeIn(rA), FadeIn(rB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, rA, d["times"]["A"])
            sing(snd, rB, d["times"]["B"])
            pulse(snd, la, ev["A"], ev["B"] - 0.5, buff=0.12)
            pulse(snd, lb, ev["B"], c.duration, buff=0.12)
        ans = VGroup(label(rf"A: \ each \textit{{note}} drawn at random: \ {d['urn_mean']:.1f} semitones a move", font_size=26, color=CHANCE_C),
                     label(rf"B: \ each \textit{{move}} drawn from the tunes' own moves: \ {d['walk_mean']:.1f} semitones", font_size=26, color=REAL_C)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "B, for most listeners. In A, each note was drawn at random from the octave. In B, each "
            "move was drawn at random from the moves that our fifty-four tunes make: mostly steps and "
            "repeats. Neither was composed. Small moves are most of what makes a string of notes sound "
            "like a tune at all."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
