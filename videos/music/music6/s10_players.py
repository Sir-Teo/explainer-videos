from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Players(SoundScene):
    def construct(self):
        chapter(self, 9, r"What players do", r"What about instruments that can play any pitch?", lit=(1584,), extra=((1939, r"A = 440 Hz"),))
        self.free()
        self.strings()
        self.evidence()
        self.pitch()

    # ------------------------------------------------------------------
    def free(self):
        fixed = VGroup(label(r"fixed", font_size=34, color=NARROW), label(r"piano, \ organ, \ harp, \\ vibraphone, \ fretted guitar", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25)
        free = VGroup(label(r"free", font_size=34, color=GOOD), label(r"voices, \ violins, \ trombones; \\ and, \ within limits, \ every wind player's lips", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25)
        VGroup(fixed, free).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(UP * 1.6)
        habits = VGroup(
            label(r"a held chord: \ thirds drawn down towards pure", font_size=28, color=GOOD),
            label(r"a melody: \ leading notes pushed up, \ towards the Pythagorean", font_size=28, color=AIR),
            label(r"a barbershop seventh: \ tuned to 7 : 4, \ far below the piano's", font_size=28, color=TUNE),
            label(r"with a piano: \ everybody follows the piano", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.4)
        with self.voiceover(
            "Everything so far has been about instruments with fixed notes. Most music is not made on them. "
            "<bookmark mark='a'/> A voice, a violin, a trombone can produce any pitch at all, and wind players "
            "bend every note with their lips. For them tuning is not a table. It is a decision made afresh on "
            "every note. And good players make different decisions in different places. <bookmark mark='b'/> On "
            "a held chord, they draw the third down towards pure, because a beating third in a slow chord "
            "sounds sour. <bookmark mark='c'/> In a melody, they often do the opposite, and push a leading note "
            "up towards the note it is heading for: higher even than the piano's, close to the Pythagorean "
            "version. <bookmark mark='d'/> A barbershop quartet tunes its sevenths to seven to four, the "
            "nameless valley of Part 5, nearly a third of a semitone below the piano's seventh, and prizes the "
            "ring it makes. <bookmark mark='e'/> And when there is a piano in the room, everybody follows the "
            "piano."
        ) as vo:
            self.play(FadeIn(fixed))
            vo.wait_until("a")
            self.play(FadeIn(free))
            for mark, h in zip("bcde", habits):
                vo.wait_until(mark)
                self.play(FadeIn(h), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def strings(self):
        d = load("syntonic")
        notes = VGroup(*[VGroup(Line(LEFT * 0.0, RIGHT * 2.0, color=STR, stroke_width=4), label(n, font_size=36, color=TUNE if n in ("C", "E") else GREY_A)).arrange(DOWN, buff=0.2)
                         for n in ("C", "G", "D", "A", "E")]).arrange(RIGHT, buff=0.5).move_to(UP * 1.7)
        who = VGroup(label(r"the cello's four strings", font_size=24, color=GREY_B).next_to(notes[:4], UP, buff=0.3),
                     label(r"the violin's top string", font_size=24, color=GREY_B).next_to(notes[4], UP, buff=0.3))
        fifths = VGroup(*[MathTex(r"\tfrac32", font_size=28, color=AIR).move_to((a.get_right() + b.get_left()) / 2 + UP * 0.2) for a, b in zip(notes[:-1], notes[1:])])
        p, q = d["from_fifths"]
        res = VGroup(label(rf"open strings tuned in pure fifths: \ C to E is ${p}:{q}$, \ a comma wider than a pure third", font_size=28, color=BAD),
                     label(r"so a quartet's C major chord cannot use the violin's open E as it stands", font_size=26, color=GREY_A),
                     label(r"many quartets tune their fifths a shade narrow: \ a temperament, \ chosen by ear", font_size=28, color=GOOD)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            "The commas reach even the instruments that seem free of them. A string quartet tunes its open "
            "strings by listening to fifths. <bookmark mark='a'/> The cello's strings are C, G, D and A, and the "
            "violin carries the chain one fifth further, to E. Tune all of those fifths pure, as string players "
            "are taught to, and you have walked four fifths from the cello's C to the violin's E. "
            "<bookmark mark='b'/> We know what that gives: the wide third of eighty-one to sixty-four. So when "
            "the quartet plays a chord of C major, the violin's open E string is a comma too high for the "
            "cello's open C. <bookmark mark='c'/> Players deal with it by fingering the note instead, or by "
            "tuning their fifths a shade narrow in the first place. That is a temperament, small and unwritten, "
            "set by ear before every concert."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in notes[:4]], lag_ratio=0.25), FadeIn(who[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(notes[4]), FadeIn(who[1]), LaggedStart(*[FadeIn(f) for f in fifths], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        d = load("pump")
        rows = rows_card([
            (r"the prediction", rf"pure chords with held notes must drift: \ {abs(d['per_round']):.1f} cents each time round our progression"),
            (r"quartets, \ measured", r"singers given pieces written to pump the comma did drift, \\ as the arithmetic predicts, \ though not by the full amount \quad (Howard, 2007)"),
            (r"an ensemble, \ over a term", r"each singer's tuning lay closer to equal temperament than to just intonation; \\ the major thirds leaned towards pure \quad (D'Amario and colleagues, 2020)"),
            (r"the conclusion", r"real intonation is a moving compromise: \ pure where it is heard most, \\ and anchored so that the pitch stays where it began"),
        ], left=-6.4, text_left=-2.6, top=1.8, step=1.35, name_size=28, text_size=23, color=EAR)
        head = label(r"Do choirs really drift?", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "So do choirs really sink, as the comma pump says they must? <bookmark mark='a'/> The prediction is "
            "exact: a comma for every time round. <bookmark mark='b'/> When vocal quartets were recorded singing "
            "pieces written to pump the comma, they did drift, as the arithmetic predicts, though not by the "
            "full amount. "
            "<bookmark mark='c'/> But when an ensemble was followed through months of rehearsal, each singer's "
            "notes turned out to lie closer to equal temperament than to just intonation, with the major thirds "
            "leaning a little towards pure. <bookmark mark='d'/> Singers are not pure-interval machines. They "
            "tune the chords they are holding, and at the same time they remember where the key is, and those "
            "two aims pull against each other all the time. Real intonation is a moving compromise, and it is "
            "one of the things that makes a fine ensemble sound alive."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pitch(self):
        g = axes([1700, 2000], [380, 460], x_length=9.6, y_length=3.0, xlabel=r"year", ylabel=r"the A above middle C (Hz)", xticks=[1700, 1750, 1800, 1850, 1900, 1950, 2000], yticks=[380, 400, 420, 440, 460], font_size=20)
        g.move_to(DOWN * 0.6)
        marks = [(1740, 415, r"Baroque pitch, \ about 415"), (1810, 423, r"about 423"), (1859, 435, r"France, \ by law: \ 435"), (1939, 440, r"London, \ 1939: \ 440")]
        dots = VGroup(*[VGroup(Dot(g.ax.c2p(y, f), radius=0.08, color=HIST), label(t, font_size=22, color=GREY_A).next_to(g.ax.c2p(y, f), UP, buff=0.15)) for y, f, t in marks])
        line = Line(g.ax.c2p(1939, 440), g.ax.c2p(2000, 440), color=HIST, stroke_width=3)
        head = label(r"one more decision: \ where the whole system sits", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        tag = label(r"typical values; \ pitch varied from town to town", font_size=18, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is one more decision, and it is separate from all the others: where the whole system sits. A "
            "tuning fixes the ratios between notes. It does not say how many hertz any of them is. "
            "<bookmark mark='a'/> For most of history that was a local matter. An organ in one town could be a "
            "semitone away from an organ in the next. In the eighteenth century the A above middle C was "
            "typically somewhere near four hundred and fifteen hertz, and it crept upwards as orchestras "
            "looked for a more brilliant sound. <bookmark mark='b'/> France fixed it by law at four hundred and "
            "thirty-five in 1859. <bookmark mark='c'/> And in 1939 an international conference in London settled "
            "on four hundred and forty, which is what your tuner app assumes. It is a convention, not a fact of "
            "nature, and players of early music still tune to the old pitches."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(dots[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]))
            vo.wait_until("c")
            self.play(FadeIn(dots[3]), Create(line))
        self.wait(0.3)
        self.clear_scene()
