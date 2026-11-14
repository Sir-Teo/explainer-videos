from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Naples(SoundScene):
    def construct(self):
        chapter(self, 6, r"Naples and the partimento", r"How did a bass become a composition?", extra=((1716, r"Campion's rule of the octave"),))
        self.history()
        self.rule()
        self.realize()

    # ------------------------------------------------------------------
    def history(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"1716: \ Fran\c{c}ois Campion, \ Paris: \ the \textit{r\`egle de l'octave}", WHITE),
            (r"Naples: \ Francesco Durante \ (1684--1755), \ Leonardo Leo, \ later Fedele Fenaroli", WHITE),
            (r"partimenti: \ basses, \ some with figures, \ realized at the keyboard", WHITE),
            (r"the students: \ Pergolesi, \ Paisiello, \ Cimarosa, \ and hundreds of working musicians", WHITE),
            (r"rediscovered by Robert Gjerdingen \ (2007) \ and Giorgio Sanguinetti \ (2012)", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the partimento tradition", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The rule of the octave was first printed under that name in Paris, in 1716, by the guitarist and theorbo player "
            "François Campion. <bookmark mark='a'/> In Naples it became the backbone of a whole training. Masters "
            "such as Francesco Durante and Leonardo Leo wrote partimenti, bass lines, sometimes with figures, "
            "sometimes without, for students to realize at the keyboard. <bookmark mark='c'/> A student who had "
            "played through hundreds of them knew, without thinking, what goes above any bass. "
            "<bookmark mark='d'/> Pergolesi, Paisiello and Cimarosa came out of this training. "
            "<bookmark mark='e'/> The manuscripts sat in libraries until musicologists, Robert Gjerdingen and "
            "Giorgio Sanguinetti among them, read them again at the start of this century, and saw a way of "
            "learning composition that had been forgotten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows_[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        d = load("octave")
        c = clip("octave.updown")
        su = block_staff(d["up"], width=5.7, beats=2).move_to(LEFT * 3.5 + UP * 0.4)
        sd = block_staff(d["down"], width=5.7, beats=2).move_to(RIGHT * 3.5 + UP * 0.4)
        fu = VGroup(*[label(d["rule"]["up"][str(k)] if d["rule"]["up"][str(k)] != "5/3" else "", font_size=18, color=TUNE) for k in range(1, 9)])
        fd = VGroup(*[label(d["rule"]["down"][str(k)].replace("#", r"$\sharp$") if d["rule"]["down"][str(k)] != "5/3" else "", font_size=18, color=TUNE) for k in range(8, 0, -1)])
        for grp, stf in ((fu, su), (fd, sd)):
            for k, f in enumerate(grp):
                f.move_to([stf.get_left()[0] + 1.0 + (stf.width - 1.2) * (k + 0.5) / 8, stf.get_bottom()[1] - 0.35, 0])
        lu = label(r"rising", font_size=26, color=GREY_A).next_to(su, UP, buff=0.3)
        ld = label(r"falling", font_size=26, color=GREY_A).next_to(sd, UP, buff=0.3)
        note = VGroup(label(r"the same degree, \ a different chord on the way down: \ 6 rising, \ \#6/4/3 falling", font_size=22, color=WHITE),
                      label(r"a plain triad only on 1 and 5: \ the two pillars of the key", font_size=22, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the rule, rising and falling, with its figures under the bass. Listen for the two "
            "pillars: only the first and the fifth notes of the scale carry a plain triad. Every other note "
            "carries an inverted chord, its root somewhere above the bass, which pulls toward the next pillar."
        ):
            self.play(FadeIn(su), FadeIn(sd), FadeIn(lu), FadeIn(ld), FadeIn(fu), FadeIn(fd))
        with self.listen(c) as snd:
            window(snd, r"the rule of the octave, \ up and down", detail=r"a plucked string", corner=DL, tag_corner=DR)
            flash(snd, list(fu), d["times"]["up"], hot=WHITE, base=TUNE)
            flash(snd, list(fd), d["times"]["down"], hot=WHITE, base=TUNE)
            pulse(snd, lu, d["starts"]["up"], d["starts"]["down"] - 0.5, buff=0.1)
            pulse(snd, ld, d["starts"]["down"], c.duration, buff=0.1)
        with self.voiceover(
            "And the chords are not the same going up and coming down. On the sixth degree, rising, a plain "
            "first-inversion chord; falling, a chord with a raised sixth that leans toward the fifth degree, "
            "the dominant of the dominant. The rule knows the direction of travel. That is why it was learned "
            "in both directions, in every key, until the hands knew it."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def realize(self):
        d = load("more")["partimento"]
        c = clip("more.partimento")
        line = line_roll(d["bass"], width=10.0, height=1.4, lo=46, hi=60).move_to(UP * 1.7)
        g = chord_roll(d["chords"], width=10.0, height=2.6, lo=44, hi=80).move_to(DOWN * 1.2)
        how = VGroup(*[label(h.replace("rule, ", r"rule \ ").replace("leap: a triad", r"triad"), font_size=16, color=TUNE if h.startswith("rule") else GREY_B).move_to([g.xk(k), g.frame.get_bottom()[1] - 0.3, 0]) for k, h in enumerate(d["how"])])
        tl = label(r"a bass with no figures", font_size=24, color=VOICE_C[3]).next_to(line, UP, buff=0.2)
        tg = label(r"realized by a program: \ the rule where the bass steps, \ a plain triad where it leaps", font_size=22, color=GREY_A).next_to(g, UP, buff=0.25)
        with self.voiceover(
            "The rule turns harmonizing a bass into something a beginner, or a program, can do. Here is a bass with "
            "no figures at all. Monochord's partimento player looks at each note: where the bass moves by step, it "
            "takes the rule's chord for that degree and direction; where it leaps, a plain triad; and it moves the "
            "upper voices the shortest way, avoiding parallels. Hear the bass, and then what the program plays."
        ):
            self.play(FadeIn(line), FadeIn(tl), FadeIn(g), FadeIn(tg), FadeIn(how))
        with self.listen(c) as snd:
            window(snd, r"a bass, \ then its realization", detail=r"a plucked string", corner=DL, tag_corner=DR)
            flash(snd, list(line.dots), [d["starts"]["bass"] + t for t in d["times"]["bass"]], hot=WHITE, base=VOICE_C[3])
            sing_chords(snd, g, d["times"]["full"], start=d["starts"]["full"])
        with self.voiceover(
            "It is correct and a little dull, which is what a student's first realization was. The art came "
            "afterwards: the teacher's next lessons added suspensions, passing notes and imitation over the same "
            "bass, until the exercise became a piece. Chapter nine will hear one of those additions."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

