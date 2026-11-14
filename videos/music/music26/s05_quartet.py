from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403

INST = [r"1st violin", r"2nd violin", r"viola", r"cello"]


class Quartet(SoundScene):
    def construct(self):
        chapter(self, 4, r"The string quartet: \ a conversation", r"Who has the tune?", extra=((1784, r"Mozart's `Hunt' quartet"),))
        self.genre()
        self.hunt()
        self.counted()
        self.minuet()
        self.op33()

    # ------------------------------------------------------------------
    def genre(self):
        items = [
            (r"two violins, \ viola, \ cello: \ four equal players, \ no continuo", WHITE),
            (r"Haydn wrote 68 quartets over forty years and made the genre", WHITE),
            (r"Goethe \ (1829): \ `four rational people conversing'", TUNE),
            (r"Mozart's six quartets dedicated to Haydn \ (1785): \ `the fruit of long and laborious toil'", WHITE),
            (r"music for players more than for audiences: \ chamber music", GREY_A),
        ]
        rows_scene(self, r"four rational people", items,
                   "The genre that best shows the style is the string quartet. <bookmark mark='b'/> Two violins, a viola "
                   "and a cello: four equal players and, for the first time, no continuo filling in the harmony. "
                   "<bookmark mark='c'/> Haydn wrote about seventy quartets over forty years and more or less invented the "
                   "genre. <bookmark mark='d'/> Goethe later described a quartet as four rational people conversing. "
                   "<bookmark mark='e'/> Mozart dedicated six quartets to Haydn in 1785, calling them the fruit of long and "
                   "laborious toil. <bookmark mark='f'/> It was music for the players first, played at home among friends: "
                   "chamber music.", marks="cdef")

    # ------------------------------------------------------------------
    def hunt(self):
        d = load("texture")
        c = clip("texture.hunt")
        vs = d["hunt"]
        g = voices_roll(vs, width=11.4, height=3.4, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.11).move_to(DOWN * 0.35)
        names = VGroup(*[label(INST[j], font_size=18, color=[TUNE, BLUE, EAR, GREY_A][j]) for j in range(4)]).arrange(RIGHT, buff=0.7).next_to(g, UP, buff=0.25)
        head = label(r"Mozart, \ String Quartet K. 458 \ (`The Hunt'), \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"a horn-call in 6/8: \ the first violin leads, \ the others answer and support", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "Here is how one opens: the first eight bars of Mozart's quartet K. 458, nicknamed The Hunt for its opening "
            "horn-call in six-eight time, sung by Part 7's bowed string from the encoding. Listen to the first violin "
            "lead, and the others answer and support it."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Mozart, \ `The Hunt'", detail=r"from the encoding, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("texture")["by"]
        groups = VGroup()
        for c in ("haydn", "mozart", "beethoven"):
            sh = d[c]["shares"]
            stack = VGroup()
            y = 0.0
            for j in range(4):
                h = 3.0 * sh[j]
                r = Rectangle(width=1.3, height=max(h, 0.02), stroke_width=0, fill_color=[TUNE, BLUE, EAR, GREY_A][j], fill_opacity=0.9).move_to([0, y + h / 2, 0])
                stack.add(VGroup(r, label(rf"{100 * sh[j]:.0f}", font_size=17, color=BLACK).move_to(r)))
                y += h
            groups.add(VGroup(stack, label(c.title(), font_size=21, color=WHITE).next_to(stack, DOWN, buff=0.25),
                              label(rf"changes hands in {100 * d[c]['changes']:.0f} bars in 100", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.2))
        groups.arrange(RIGHT, buff=1.0).move_to(LEFT * 1.8 + DOWN * 0.2)
        key = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=[TUNE, BLUE, EAR, GREY_A][j], fill_opacity=0.9), label(INST[j], font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15) for j in range(4)]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 5.0 + UP * 0.4)
        t = label(r"which instrument has the most notes in each bar, \ in 100 bars", font_size=21, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Is it a conversation, or a first violin with accompaniment? Count, bar by bar, which instrument has the most "
            "notes. <bookmark mark='a'/> In Haydn's movements the first violin leads in "
            f"{say(round(100 * d['haydn']['shares'][0]))} bars in a hundred; <bookmark mark='b'/> in Mozart's, "
            f"{say(round(100 * d['mozart']['shares'][0]))}, with the second violin busier; <bookmark mark='c'/> in "
            f"Beethoven's, {say(round(100 * d['beethoven']['shares'][0]))}, with the viola and cello taking more of the "
            "lead. The first violin is still the main speaker, but the others get the floor in a third to a half of the "
            "bars, and the lead changes hands in almost every other bar."
        ) as vo:
            self.play(FadeIn(t), FadeIn(key))
            for mark, gg in zip("abc", groups):
                vo.wait_until(mark)
                self.play(FadeIn(gg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def op33(self):
        items = [
            (r"1781: \ Haydn offers his Op. 33 quartets, \ `written in a new and special way'", WHITE),
            (r"a sales pitch, \ and a fair description: \ the motives pass between all four instruments", WHITE),
            (r"accompaniment and melody trade places: \ `obbligato' accompaniment", WHITE),
            (r"Mozart's answer: \ six quartets dedicated to Haydn, \ 1782--1785", TUNE),
            (r"Haydn to Mozart's father: \ `the greatest composer known to me in person or by name'", GREY_A),
        ]
        rows_scene(self, r"a new and special way", items,
                   "One letter marks the turn. <bookmark mark='b'/> In 1781 Haydn offered his Opus 33 quartets to subscribers as written in a new and special way. <bookmark mark='c'/> It was a sales pitch, and also a fair description: the motives pass between all four players, <bookmark mark='d'/> and accompaniment and melody trade places, so that no part is mere filler. <bookmark mark='e'/> Mozart answered with six quartets dedicated to Haydn, written between 1782 and 1785, the Hunt among them. <bookmark mark='f'/> After hearing some of them, Haydn told Mozart's father that his son was the greatest composer he knew in person or by name.", marks="cdef")

    # ------------------------------------------------------------------
    def minuet(self):
        d = load("minuet")
        c = clip("minuet.haydn")
        vs = d["voices"]
        g = voices_roll(vs, width=11.0, height=3.0, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(DOWN * 0.2)
        bb = d["bar_beats"]
        x0, W = g.frame.get_left()[0], g.frame.width
        ticks = VGroup(*[Line([x0 + W * k * bb / g.total, g.frame.get_bottom()[1] - 0.1, 0], [x0 + W * k * bb / g.total, g.frame.get_bottom()[1] - 0.3, 0], color=GREY_B, stroke_width=2) for k in range(9)])
        head = label(r"Haydn, \ Op. 74 No. 1, \ the minuet: \ eight bars in three", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        cap = label(rf"{d['in34']} of the {d['n']} movements are in 3/4: \ minuets, \ scherzos \ and others", font_size=21, color=GREY_A).next_to(ticks, DOWN, buff=0.3)
        with self.voiceover(
            "A Classical quartet usually has four movements: a fast sonata-form movement, a slow one, a minuet and trio, and "
            "a fast finale. The minuet is the one dance left from the Baroque suite of Part 25, still in three, still in two "
            f"repeated halves; {say(d['in34'])} of the thirty-three movements here are in three-four time. Haydn's minuets are "
            "rarely courtly; listen to this one's energy."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(ticks), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a minuet", detail=r"from the encoding, \ Part 7's bowed string", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["unit"], colors=[TUNE, BLUE, EAR, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()
