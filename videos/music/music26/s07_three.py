from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Three(SoundScene):
    def construct(self):
        chapter(self, 6, r"Haydn, \ Mozart, \ Beethoven", r"What did each do with the same language?", extra=((1806, r"Beethoven's `Razumovsky' quartets"),))
        self.careers()
        self.measured()
        self.london()
        self.beethoven()
        self.wrong()
        self.quiz()
        self.figaro()
        self.gluck()

    # ------------------------------------------------------------------
    def careers(self):
        items = [
            (r"Haydn, \ 1732--1809: \ thirty years in the Esterházy household, \ then fame in London", WHITE),
            (r"economy: \ whole movements from one idea; \ wit; \ surprise", WHITE),
            (r"Mozart, \ 1756--1791: \ prodigy, \ freelance in Vienna, \ the opera ensembles of \textit{Figaro} and \textit{Don Giovanni}", WHITE),
            (r"Beethoven, \ 1770--1827: \ Haydn's pupil, \ then motives and expansion: \ longer, \ wider, \ louder", TUNE),
            (r"the three in one city, \ within one lifetime: \ the `Viennese Classics' is a later label", GREY_A),
        ]
        rows_scene(self, r"three careers", items,
                   "Three composers, one city, overlapping lives. <bookmark mark='b'/> Joseph Haydn spent thirty years "
                   "as music director to the Esterházy princes, then found fame in London in the 1790s. "
                   "<bookmark mark='c'/> His art is economy: whole movements spun from one idea, with wit and surprise. "
                   "<bookmark mark='d'/> Wolfgang Amadeus Mozart, a child prodigy, lived as a freelance in Vienna and "
                   "brought the style to opera, in the ensembles of Figaro and Don Giovanni. <bookmark mark='e'/> Ludwig "
                   "van Beethoven came to Vienna in 1792 to study with Haydn, and pushed the language outward: motives "
                   "worked to exhaustion, movements longer, wider and louder. <bookmark mark='f'/> Calling them together "
                   "the Viennese Classics is a later habit; they did not think of themselves as a school.", marks="cdef")

    # ------------------------------------------------------------------
    def measured(self):
        d = load("three")["stats"]
        names = ("haydn", "mozart", "beethoven")
        cols = [TUNE, BLUE, EAR]
        panels = VGroup()
        for key, lab_, top in (("bars", r"bars per movement", 320.0), ("span", r"semitones each instrument spans", 40.0)):
            bars = VGroup()
            for j, n in enumerate(names):
                v = d[n][key]
                h = 2.6 * v / top
                r = Rectangle(width=0.8, height=max(h, 0.02), stroke_width=0, fill_color=cols[j], fill_opacity=0.9).move_to([1.0 * j, h / 2, 0])
                bars.add(VGroup(r, label(rf"{v:.0f}", font_size=20, color=WHITE).next_to(r, UP, buff=0.08), label(n.title(), font_size=18, color=GREY_A).next_to(r, DOWN, buff=0.15)))
            panels.add(VGroup(bars, label(lab_, font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.55)))
        panels.arrange(RIGHT, buff=2.0, aligned_edge=DOWN).move_to(DOWN * 0.2)
        cnt = label(rf"single movements: \ Haydn {d['haydn']['movements']}, \ Mozart {d['mozart']['movements']}, \ Beethoven {d['beethoven']['movements']}", font_size=20, color=GREY_B).to_edge(UP, buff=0.5)
        cap = label(r"bars are not equal units \ (a bar of 3/8 is short): \ the lengths are rough", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The expansion can be measured on the corpus. <bookmark mark='a'/> Haydn's and Mozart's quartet movements "
            f"average about {say(round(d['haydn']['bars'], -1))} and {say(round(d['mozart']['bars'], -1))} bars; "
            f"Beethoven's, {say(round(d['beethoven']['bars'], -1))}, three times as long, though a bar is not a fixed unit "
            "of time and the figures are rough. <bookmark mark='b'/> And each of Beethoven's instruments covers about "
            f"{say(round(d['beethoven']['span']))} semitones on average, against about {say(round(d['haydn']['span']))} for "
            "Haydn and Mozart: nearly an octave more, the strings pushed higher and lower."
        ) as vo:
            self.play(FadeIn(cnt), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wrong(self):
        d = load("keys")
        c = clip("keys.wrong")
        vs = d["voices"]
        g = voices_roll(vs, width=11.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.09).move_to(UP * 0.5)
        bb = d["bar_beats"]
        x0, W = g.frame.get_left()[0], g.frame.width
        strip = VGroup()
        for w in d["plan4"]:
            if w["bar"] > 14:
                break
            k = tuple(w["key"])
            col = TUNE if k == (0, "major") else (EAR if k == (4, "minor") else GREY_B)
            a = x0 + W * w["bar"] * bb / g.total
            r = Rectangle(width=W * 2 * bb / g.total - 0.04, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([a + W * bb / g.total, -1.55, 0])
            strip.add(r)
        key_l = VGroup(label(r"C major", font_size=20, color=TUNE), label(r"E minor", font_size=20, color=EAR)).arrange(RIGHT, buff=0.6).next_to(strip, DOWN, buff=0.3)
        head = label(r"Beethoven, \ Op. 59 No. 2, \ finale: \ a movement in E minor", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the tracker, \ four bars at a time:", font_size=19, color=GREY_A)
        VGroup(cap, *key_l).arrange(RIGHT, buff=0.5).next_to(strip, DOWN, buff=0.3)
        with self.voiceover(
            "Here is that joke. The finale of Beethoven's second Razumovsky quartet is in E minor. But its theme begins "
            "firmly in C major, and only swerves to E minor at its cadence; then it starts again in C. Below the score, "
            "the tracker reads four bars at a time: C, E minor, C, E minor, as if it cannot decide. Listen for the swerve."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(strip), FadeIn(key_l), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"C major, \ or E minor?", detail=r"from the encoding, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        with self.voiceover(
            f"The theme keeps doing this, and the tracker only settles on E minor for good around bar {say(round(d['settle']))}. "
            "A listener who knows the style expects a movement to begin in its home key. Beethoven makes the home key "
            "something the movement has to win, and the expectation is what makes the joke work."
        ):
            self.play(Indicate(strip, color=WHITE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("three")
        c = clip("three.quiz")
        card = listen_card(r"Two quartet openings, \ half a century apart: \ Haydn's first, \ and one of Beethoven's middle period. \ "
                           r"Which is Beethoven, \ A or B? \ Listen for register and for who has the tune.", width=10.6)
        with self.voiceover(
            "Two openings, half a century apart: Haydn's very first quartet, and one of Beethoven's from 1806. Which is "
            "Beethoven, A or B? Listen for the register, and for who has the tune."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(d["A"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(d["B"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"from the encodings, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"], d["starts"]["A"], d["unitA"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash_voices(snd, gB, d["B"], d["starts"]["B"], d["unitB"], colors=[TUNE, BLUE, EAR, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"Haydn, \ Op. 1 No. 1 \ (about 1757)", font_size=22, color=TUNE).next_to(gA, DOWN, buff=0.35),
                     label(r"Beethoven, \ Op. 59 No. 1 \ (1806): \ the cello has the tune", font_size=22, color=EAR).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is Beethoven, the first of the quartets he wrote for Count Razumovsky in 1806, where the long opening tune "
            "is given to the cello, under a quietly pulsing accompaniment. A is Haydn's first quartet, from the 1750s, "
            "light and quick, the first violin on top."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beethoven(self):
        items = [
            (r"the Fifth Symphony \ (1808): \ four notes, \ short--short--short--long", WHITE),
            (r"the rhythm runs through every movement, \ in every instrument", WHITE),
            (r"development no longer a section: \ the whole movement develops", WHITE),
            (r"the codas grow into second developments", TUNE),
            (r"the Classical language, \ pushed until it carries a personal drama", GREY_A),
        ]
        rows_scene(self, r"a motive worked to exhaustion", items,
                   "Beethoven's other expansion was of the motive. <bookmark mark='b'/> His Fifth Symphony, of 1808, begins with four notes, three short and a long, <bookmark mark='c'/> and that rhythm runs through every movement and every instrument. <bookmark mark='d'/> Development stops being one section of the form and becomes what the whole movement does; <bookmark mark='e'/> the codas grow into second developments. <bookmark mark='f'/> It is the Classical language pushed until it carries what listeners heard as a personal drama, and that is where Part 27 begins.", marks="cdef")

    # ------------------------------------------------------------------
    def figaro(self):
        items = [
            (r"Mozart, \ \textit{The Marriage of Figaro} \ (1786): \ the end of Act II", WHITE),
            (r"twenty minutes of continuous music, \ characters entering one by one", WHITE),
            (r"each new turn of the plot: \ a new key, \ a new tempo, \ a new texture", WHITE),
            (r"by the end, \ seven singers at once, \ each in character", TUNE),
            (r"the sonata's drama of keys, \ put on a stage with real people", GREY_A),
        ]
        rows_scene(self, r"music that moves with the plot", items,
                   "Mozart's opera ensembles show what the language could do in a theatre. <bookmark mark='b'/> The end of the second act of The Marriage of Figaro, of 1786, <bookmark mark='c'/> is twenty minutes of continuous music in which characters arrive one at a time, <bookmark mark='d'/> each new turn of the plot marked by a new key, a new tempo, a new texture, <bookmark mark='e'/> until seven singers are singing at once, each still in character. <bookmark mark='f'/> It is the sonata's drama of keys put on a stage with real people.", marks="cdef")

    # ------------------------------------------------------------------
    def london(self):
        items = [
            (r"1790: \ Prince Nikolaus dies; \ the impresario Johann Peter Salomon brings Haydn to London", WHITE),
            (r"two visits, \ 1791--1795: \ twelve `London' symphonies for public concerts", WHITE),
            (r"the `Surprise' \ (No. 94): \ a quiet tune, \ then a sudden loud chord", WHITE),
            (r"a paying public, \ not a court: \ the music addresses them directly", TUNE),
            (r"he came home rich and famous: \ \textit{The Creation} \ (1798) followed", GREY_A),
        ]
        rows_scene(self, r"Haydn in London", items,
                   "Haydn's career turned in 1790. <bookmark mark='b'/> His prince died, the household orchestra was dismissed, and the violinist and impresario Johann Peter Salomon brought him to London. <bookmark mark='c'/> On two visits, between 1791 and 1795, he wrote twelve symphonies for London's public concerts. <bookmark mark='d'/> In the slow movement of the Surprise symphony, a quiet tune is interrupted by a sudden loud chord, a joke on an audience that might be dozing. <bookmark mark='e'/> This was music addressed to a paying public, not to a court. <bookmark mark='f'/> He came home rich and famous, and wrote the oratorio The Creation.", marks="cdef")

    # ------------------------------------------------------------------
    def gluck(self):
        items = [
            (r"Christoph Willibald Gluck, \ \textit{Orfeo ed Euridice} \ (Vienna, \ 1762)", WHITE),
            (r"against the singers' showpieces: \ the music must serve the drama", WHITE),
            (r"the preface to \textit{Alceste} \ (1769): \ `a beautiful simplicity'", WHITE),
            (r"recitative accompanied by the orchestra, \ the chorus in the action", TUNE),
            (r"Mozart's operas take the reform and add the sonata's drama of keys", GREY_A),
        ]
        rows_scene(self, r"opera reformed", items,
                   "Opera had its own revolution. <bookmark mark='b'/> In Vienna in 1762 Christoph Willibald Gluck staged Orfeo ed Euridice, <bookmark mark='c'/> and turned against the showpiece arias in which singers decorated the music to display themselves: the music should serve the drama. <bookmark mark='d'/> The preface to his Alceste, of 1769, asks for a beautiful simplicity. <bookmark mark='e'/> Recitative is accompanied by the whole orchestra, and the chorus takes part in the action. <bookmark mark='f'/> Mozart's operas inherit that reform and add to it the sonata's drama of keys.", marks="cdef")
