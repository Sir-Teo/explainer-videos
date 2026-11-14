from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.naples()
        self.bass()
        self.plan()

    # ------------------------------------------------------------------
    def naples(self):
        card = history_card(1700, r"Naples: \ four conservatories", r"orphanages that trained their boys as musicians; \ the best became the most employable composers in Europe", width=10.6, font_size=26).to_edge(UP, buff=0.4)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"the lesson: \ a bass line, \ written out by the master", WHITE),
            (r"the task: \ play the harmony above it, \ at the keyboard, \ at once", WHITE),
            (r"thousands of these basses, \ copied, \ played, \ memorized", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.9)
        with self.voiceover(
            "In eighteenth-century Naples there were four conservatories. The word meant orphanages: places "
            "that kept poor and orphaned boys, fed them, and trained them in a trade, and the trade was "
            "music. <bookmark mark='a'/> From them came Pergolesi, Paisiello, Cimarosa, and dozens of "
            "composers who ran the opera houses and chapels of Europe. <bookmark mark='b'/> How do you turn "
            "a ten-year-old into a working composer? The answer was a bass line. The master wrote one out; "
            "the boy played harmony above it at the keyboard, at sight. <bookmark mark='c'/> Thousands of "
            "these exercises, called partimenti, were copied and played and learned by heart."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass(self):
        d = load("hook")
        c = clip("hook.partimento")
        line = line_roll(d["bass"], width=10.6, height=1.5, lo=46, hi=62).move_to(UP * 1.6)
        g = chord_roll(d["chords"], width=10.6, height=2.6, lo=44, hi=80).move_to(DOWN * 1.4)
        tl = label(r"the bass alone", font_size=24, color=VOICE_C[3]).next_to(line, UP, buff=0.25)
        tg = label(r"and the harmony a Neapolitan student played above it", font_size=24, color=GREY_A).next_to(g, UP, buff=0.25)
        figs = VGroup(*[label(f.replace("#", r"$\sharp$") if f != "5/3" else "", font_size=16, color=GREY_B).move_to([g.xk(k), g.frame.get_bottom()[1] - 0.25, 0]) for k, f in enumerate(d["figures"])])
        with self.voiceover(
            "Here is the simplest one of all: a bass that climbs a scale and comes down again. First alone, "
            "and then with the harmony a student was taught to play above it, a chord for every note of "
            "the scale."
        ):
            self.play(FadeIn(line), FadeIn(tl), FadeIn(g), FadeIn(tg))
        with self.listen(c) as snd:
            window(snd, r"a bass, \ then its harmony", detail=r"a plucked string on Part 7's soundboard", corner=DL, tag_corner=DR)
            flash(snd, list(line.dots), [d["starts"]["bass"] + t for t in d["times"]["bass"]], hot=WHITE, base=VOICE_C[3])
            sing_chords(snd, g, d["times"]["full"], start=d["starts"]["full"])
            pulse(snd, tl, d["starts"]["bass"], d["starts"]["full"] - 0.5, buff=0.08)
            pulse(snd, tg, d["starts"]["full"], c.duration, buff=0.08)
        with self.voiceover(
            "Notice that the chords are not all the same kind. On some notes the bass carries a plain "
            "triad; on others the chord's third or seventh is in the bass. That recipe, which chord goes "
            "over which note of the scale, going up and going down, was called the rule of the octave, and "
            "every student knew it by heart. It is a piece of grammar: not a melody, not a chord, but a "
            "rule for how chords follow one another."
        ):
            self.play(FadeIn(figs))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 18: \ Progressions", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=28, color=c_) for t, c_ in (
            (r"the jobs chords do, \ and the order they do them in", WHITE),
            (r"how predictable harmony is, \ in bits", WHITE),
            (r"sequences, \ and when chords change", WHITE),
            (r"Naples: \ the rule of the octave, \ and the galant schemata", EAR),
            (r"ground basses, \ from the lament to the Folia", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Part 17 counted which chord follows which in Bach's chorales, and used the table without asking "
            "why. This part asks. <bookmark mark='a'/> We sort chords by the job they do and see that the jobs "
            "come in an order. <bookmark mark='b'/> We measure how predictable the next chord is. "
            "<bookmark mark='c'/> We hear sequences, and find where in the bar chords change. "
            "<bookmark mark='d'/> We go back to Naples for the rule of the octave and for the patterns, called "
            "schemata, that galant composers built their music from. <bookmark mark='e'/> And we hear the "
            "ground basses that musicians have repeated for four centuries."
        ) as vo:
            self.play(FadeIn(head))
            for mark, s in zip("abcde", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
